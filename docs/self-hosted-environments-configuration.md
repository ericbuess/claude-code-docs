> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Customize sessions in self-hosted environments

> Customize self-hosted environment sessions with wrapper scripts for per-session credentials, lifecycle hooks, and on-demand runner spawning.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; an [Owner](/docs/en/cloud-environments#organization-shared-environments) enables them by turning on **Allow self-hosted environments** on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments). This page assumes a working runner; see the [quickstart](/docs/en/self-hosted-environments-quickstart) for setup and [Deploy to production](/docs/en/self-hosted-environments-deploy) for the fleet recipes.
</Note>

A [self-hosted environment](/docs/en/self-hosted-environments) runs Claude Code [cloud sessions](/docs/en/claude-code-on-the-web) on your own infrastructure, executed by a runner process you deploy. With no configuration, that runner clones the session's repository, spawns Claude Code, and cleans up. This page is for the platform engineer operating the runners: it covers the extension points for when those defaults don't fit, from per-session credential provisioning to replacing checkout entirely. Wrappers and hooks run as executable files on the runner host, which is Linux or macOS, and the examples on this page assume a POSIX shell.

A few hook environment variables on this page still use `pool`, such as `CLAUDE_RUNNER_POOL_ID`; the CLI flag and env var names use `environment`, such as `--environment-secret-file`.

## Wrapper scripts

Use a wrapper script when each session needs setup the runner can't do on its own: provisioning short-lived credentials scoped to the session creator, exporting environment-specific secrets, preparing language toolchains, or applying resource limits around the child process. The runner starts your wrapper in place of the Claude Code binary, once per session. End the wrapper by `exec`-ing into `$CLAUDE_RUNNER_CLAUDE_BIN`, the runner's own binary, so signals and exit codes propagate correctly.

Point `--exec-path`, or `SELF_HOSTED_RUNNER_EXEC_PATH`, at the wrapper when you start the runner:

```bash theme={null}
claude self-hosted-runner --environment-secret-file /etc/claude/environment-secret --exec-path /etc/claude/session-wrapper.sh
```

The runner sets the following in the wrapper's environment:

| Variable | Description |
| :- | :- |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | The session JWT, prefixed `sk-ant-cc-`. Its `act` claim identifies the session creator, with the creator's email when the creating surface recorded it. The value is the token at spawn time; refreshes arrive over the child's stdin, so a wrapper sees only the initial value. See [Verify session identity](/docs/en/self-hosted-environments-identity). |
| `CCR_SESSION_ACCOUNT_EMAIL` | The session creator's email, pre-extracted by the runner from the token's `act.email` claim without signature verification. Suitable for labelling, such as commit trailers. When the email gates credential issuance, verify the token and read the claim from it instead. See [Provision credentials scoped to the session creator](#provision-credentials-scoped-to-the-session-creator). Unset when the token carries no creator email, for example in sessions your organization's service identity creates. Treat as personally identifiable information. |
| `CLAUDE_RUNNER_CLIENT_PLATFORM` | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, `ios`, `claude_code_cli`, or `scheduled_trigger`. Anthropic records the value once at session creation, so the wrapper and every lifecycle hook see the same value. Use it for adoption analytics and labelling only, not as an authorization signal. Unset when the session has no recorded or recognized surface. Requires Claude Code v2.1.229 or later. |
| `CLAUDE_RUNNER_CLAUDE_BIN` | Absolute path to the runner's own Claude Code binary. End your wrapper with `exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@"` to pass control to the pinned binary without hardcoding an install path. |
| `CLAUDE_CODE_REMOTE_SESSION_ID` | Session ID in the tagged `cse_...` form. This is the same session the [lifecycle hooks](#lifecycle-hooks) see as `CLAUDE_RUNNER_SESSION_ID` in `session_...` form; the UUID variables match across both, and substituting the `cse_` prefix with `session_` yields the ID shown in the session URL. |
| `CLAUDE_CODE_REMOTE_SESSION_UUID` | The same session ID in canonical UUID form, for systems that key on UUIDs. |
| `CLAUDE_CODE_REMOTE_SLACK_THREAD_URL` | For a [Claude Tag](https://claude.com/docs/claude-tag/overview) session that belongs to one Slack thread, the link to that thread. Unset for other sessions, and can be unset for a thread session too. |
| `CLAUDE_CODE_REMOTE_SLACK_THREAD_TS` | For a Claude Tag session that belongs to one Slack thread, that thread's Slack timestamp, such as `1700000000.000100`. Can be unset, and can be set when `CLAUDE_CODE_REMOTE_SLACK_THREAD_URL` isn't, so check each variable on its own. |
| `CLAUDE_SESSION_INGRESS_TOKEN_FILE` | Absolute path to a per-session file holding the current session JWT, kept fresh across token refreshes. Shell subprocesses read it for their `Authorization` header when downloading attachments the user added to the session. `exec` preserves the variable automatically; a wrapper that rebuilds the child's environment must carry the variable over, or attachment downloads silently stop working. |
| `CLAUDE_CONFIG_DIR` | Per-session Claude config directory, written at session start from the snapshot of the runner host's config that the runner captures at startup; see [Permissions and tool approval](#permissions-and-tool-approval). Writes here are isolated to this session. The directory stays under `<base-dir>/_sessions/` after the session ends unless you start the runner with [`--remove-session-state`](/docs/en/self-hosted-environments-reference#runner-cli-flags); see [Reuse a pre-warmed checkout](/docs/en/self-hosted-environments-deploy#reuse-a-pre-warmed-checkout). |
| `ANTHROPIC_BASE_URL` | The API base URL the child will use, delivered by the control plane per session and normally `https://api.anthropic.com`. Don't override it: the session's inference credential is an Anthropic-issued OAuth token that other providers don't accept. |
| `CLAUDE_CODE_OAUTH_TOKEN` | The short-lived OAuth access token the child uses for model inference, scoped to model inference and file upload only, with a lifetime of about 30 minutes. The runner re-mints it before expiry and delivers the rotation over the child's stdin, so a wrapper that doesn't [keep stdin attached](#keep-stdin-and-file-descriptor-3-attached) sees only the initial value. Don't rely on your organization's IP allowlist to bound this token's use: treat it as a bearer credential that stays usable for roughly 30 minutes if it leaks, and don't log it, write it to disk, or forward it outside the session container. |

The wrapper also inherits the rest of the child's managed environment, including any server-provided environment variables. `exec` propagates all of it automatically; if your wrapper spawns the child another way, forward the full environment.

`CLAUDE_CODE_REMOTE_SLACK_THREAD_URL` and `CLAUDE_CODE_REMOTE_SLACK_THREAD_TS` reach your wrapper or [`command` hook](#command). They also reach what the session runs, such as shell commands, git hooks, and Claude Code hooks. The `checkout`, `post-session`, and `spawn-runner` hooks don't receive them.

### Give a default to variables that can be unset

`CCR_SESSION_ACCOUNT_EMAIL`, `CLAUDE_RUNNER_CLIENT_PLATFORM`, `CLAUDE_CODE_REMOTE_SLACK_THREAD_URL`, and `CLAUDE_CODE_REMOTE_SLACK_THREAD_TS` can each be unset. If your script uses `set -u`, Bash stops with `unbound variable` when it expands one that's unset, so expand them with a default, such as `${CCR_SESSION_ACCOUNT_EMAIL:-}`.

Wherever a shell expands the Slack thread link, take these precautions:

* **Quote it**: the link can contain characters a shell acts on, such as `?` and `&`, so quote the variable, as in `"${CLAUDE_CODE_REMOTE_SLACK_THREAD_URL:-}"`.
* **Keep its value out of `eval` and `sh -c` strings**: don't substitute its value into a string that `eval` or `sh -c` runs, even inside quotes. Have that string reference the variable instead.

### Keep stdin and file descriptor 3 attached

The child's stdin is the runner's control channel. Token rotations and session-end signals arrive on it. The runner also opens a pipe on file descriptor 3 and reads the child's activity signals from it to drive idle and startup timeouts. A plain `exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@"` preserves both automatically.

If your wrapper backgrounds the child with a bare `&`, it severs the child's stdin. The session looks healthy until the initial OAuth token's roughly 30-minute lifetime expires, and then every API call that uses the token fails with `401 authentication_error`. If your wrapper must background the child, for example to keep a teardown trap alive, save stdin on file descriptor 4 or higher and re-attach it explicitly:

```bash theme={null}
exec 4<&0
"$CLAUDE_RUNNER_CLAUDE_BIN" "$@" <&4 4<&- &
CHILD=$!
trap 'teardown' EXIT
wait "$CHILD"
```

You can redirect the child's stdout. Keep file descriptor 3 and stderr attached to the runner:

* **File descriptor 3**: carries the child's activity signals to the runner. Don't close it or reuse it in the wrapper.
* **stderr**: when the wrapper or the child exits non-zero, the runner posts the last lines of stderr to the session and prints them in its own log. The session's user sees those lines, so don't print secrets to stderr, and remove `set -x` before you deploy the wrapper. If you redirect stderr, sessions still run, but the runner reports a failure with the exit code alone.

### Pass the system prompt flags through

The system prompt and appended system prompt that Anthropic's control plane sends for a session reach your wrapper as file paths, not as inline text. The runner writes each prompt to a file in the session's config directory, `CLAUDE_CONFIG_DIR`, and passes its path in the arguments your wrapper receives, as [`--system-prompt-file <path>` or `--append-system-prompt-file <path>`](/docs/en/cli-reference#system-prompt-flags).

Runners on Claude Code v2.1.281 or later deliver the prompts as files. Before v2.1.281, the runner passed them as `--system-prompt <text>` and `--append-system-prompt <text>`.

In your wrapper script or [`command` hook](#command), handle these flags as follows:

* **Pass them through**: end the wrapper with `exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@"`, which forwards the file flags along with every other argument. Don't drop or rewrite them. If a session loses a prompt file flag, it runs without the instructions the control plane sent for it.
* **On a runner at v2.1.281 or later, a file flag you append replaces the server's, never adds to it**: each prompt file flag takes a single value and Claude Code keeps the last occurrence, so if you append `--append-system-prompt-file <path>` after `"$@"`, your file's contents replace the server's appended instructions. To add instructions on top of the server's, put them in the runner image's `CLAUDE.md`, which the runner [seeds into every session's user-level config](#how-each-session’s-config-is-assembled).

### Provision credentials scoped to the session creator

Use the `decode-token` subcommand to read claims from the session JWT. It reads the token from an argument, from `CLAUDE_CODE_SESSION_ACCESS_TOKEN`, or from stdin, in that order; see [Verify the token inside the session](/docs/en/self-hosted-environments-identity#verify-the-token-inside-the-session) for what it checks. The example below decodes the creator identity, exchanges it for short-lived AWS credentials, and execs into Claude Code:

```bash theme={null}
#!/bin/bash
# Key on the stable Anthropic user ID and require a human creator.
CREATOR_SUB=$("$CLAUDE_RUNNER_CLAUDE_BIN" self-hosted-runner decode-token \
  | jq -re '.act.sub // "" | select(startswith("user:"))') \
  || { echo "decode-token: verification failed or no human creator" >&2; exit 1; }

creds=$(your-sts-helper assume-role --subject "$CREATOR_SUB") \
  || { echo "credential exchange failed" >&2; exit 1; }
eval "$creds"

exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@"
```

Use `jq -re` rather than `jq -r` when the extracted claim gates an auth decision, so an absent claim exits non-zero instead of passing the literal string `null` downstream. Sessions created by an organization service identity, such as bot and agent sessions, carry an `agent:` subject rather than `user:`, so this example refuses them; if your environment serves those sessions, decide explicitly whether the wrapper falls back to a default credential for them instead of exiting. When your credential exchange needs the email instead, read `.act.email` and handle its absence: the token carries it only when the creating surface recorded it, and a [CLI-dispatched session](/docs/en/self-hosted-environments-testing#run-the-test-loop) can lack it. For the full claim reference and verification from services outside the runner, see [Verify session identity](/docs/en/self-hosted-environments-identity).

## Lifecycle hooks

Lifecycle hooks replace stages of the runner's per-session pipeline with your own scripts. Point the runner at a directory of hooks with `--hooks-dir <path>`, or `SELF_HOSTED_RUNNER_HOOKS_DIR`. The runner looks for executable files with well-known names; any hook that isn't present falls through to the built-in behavior, so you only write the ones you need. Hooks run with the runner's own privileges, and session children share that UID, so mount the hooks directory read-only, or bake it into the image, so session code can't modify it; see the [hardening section](/docs/en/self-hosted-environments-deploy#harden-your-deployment).

These hooks are distinct from [Claude Code hooks](/docs/en/hooks), which run inside the session; lifecycle hooks run on the runner, around the session.

### checkout

Runs once per repository, in place of the runner's built-in clone and fetch. Use the hook to clone from a read-through mirror that you reach over HTTPS or SSH, seed a working tree from an archive, or apply per-session git auth. The runner sets these variables, and may set other `CLAUDE_RUNNER_` variables that the table doesn't list:

| Variable | Description |
| :- | :- |
| `CLAUDE_RUNNER_REPO_URL` | Repository URL to clone, after any `--git-host-rewrite` and `--git-ssh-rewrite` have been applied |
| `CLAUDE_RUNNER_REPO_REF` | Revision to check out, as the session requested it: a branch, tag, commit SHA, or full reference name such as `refs/pull/<number>/head`. Empty means the repository's default branch. |
| `CLAUDE_RUNNER_CHECKOUT_PATH` | Absolute path where the working tree must be left |
| `CLAUDE_RUNNER_SESSION_ID` | Session ID in the tagged `session_...` form, for logging and correlation |
| `CLAUDE_RUNNER_SESSION_UUID` | The same session ID in canonical UUID form |
| `CLAUDE_RUNNER_API_BASE_URL` | Anthropic API base URL for session-scoped calls |
| `CLAUDE_RUNNER_CLIENT_PLATFORM` | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, or `ios`. Unset when the session has no recorded or recognized surface, so reference it as `${CLAUDE_RUNNER_CLIENT_PLATFORM:-}` under `set -u`. Requires Claude Code v2.1.229 or later. |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | The session access token, for session-scoped API calls |
| `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_n`, `GIT_CONFIG_VALUE_n` | Git settings the runner fixes for the git your hook runs. [Git configuration inside lifecycle hooks](#git-configuration-inside-lifecycle-hooks) describes them. Requires Claude Code v2.1.280 or later. |

The script must leave a working tree at `CLAUDE_RUNNER_CHECKOUT_PATH` checked out at the requested revision. A detached HEAD works, because the runner creates the session's working branch on top.

After your hook returns, the runner verifies that `CLAUDE_RUNNER_CHECKOUT_PATH` contains a `.git`. If your hook materializes a non-git source such as Perforce or an unpacked tarball, set `CLAUDE_RUNNER_SKIP_GIT_VERIFY=1` in the runner's environment to skip that check. Git-based flows such as working-branch creation and pushing results require a git checkout, so export outcomes from non-git trees with a [`post-session` hook](#post-session).

#### Get git credentials in the hook

The runner doesn't pass a git credential to the hook. The `decode-token` subcommand isn't available here either, because `CLAUDE_RUNNER_CLAUDE_BIN` isn't set in the checkout-hook environment. Mint a per-session clone credential from the session's identity instead, or fall back to the host's own git authentication:

* **Per-session clone credential**: verify `CLAUDE_CODE_SESSION_ACCESS_TOKEN` with a standard JWT library against the JWKS endpoint under `CLAUDE_RUNNER_API_BASE_URL`, as described in [Verify the token from your service](/docs/en/self-hosted-environments-identity#verify-the-token-from-your-service). Then have your credential service issue a short-lived clone credential for the identity in the token's `act` claim. Key that credential on `act.sub`, and don't require `act.email`.
* **Host git authentication**: use whatever git authentication the host already has, such as an SSH agent, credential helper, or `.netrc`.

#### When the hook fails

The hook fails when it exits non-zero, or exits 0 without leaving a usable checkout behind:

* **A repository the session pushes results to**: the runner fails the session, and on a non-zero exit surfaces the tail of the script's stderr to the user.
* **A repository the session only reads from**, such as a repository added to a running session: the runner logs a `[runner:warn]` line with the failure detail, posts a `Skipped` step to the session, removes whatever the hook left at the checkout path, and continues with the remaining repositories. If skipping leaves the session with no repository at all, the runner fails the session anyway.

When the hook succeeds, the runner removes the checkout path after the session ends.

### post-session

Runs once per session, after the Claude Code child has exited and before the runner tears the workspace down. This hook is your only chance to save uncommitted work: at `--capacity` above one, the runner deletes per-session worktrees right after the hook returns, and at `--capacity 1` the reused [canonical clone](/docs/en/self-hosted-environments-deploy#reuse-a-pre-warmed-checkout) is hard-reset when the next session starts, so uncommitted tracked changes don't survive on either path. Typical uses are pushing a snapshot branch of uncommitted changes, archiving logs, or emitting a session-ended event to your own systems.

The hook fires on every session end where a child process was spawned, whatever the cause; the `CLAUDE_RUNNER_EXIT_REASON` values below enumerate the cases. It can't fire when the runner terminates abruptly, such as a VM preemption or a power loss; if you need guarantees against abrupt termination, snapshot periodically from inside the session with a Claude Code `PostToolUse` hook instead. The runner sets:

| Variable | Description |
| :- | :- |
| `CLAUDE_RUNNER_SESSION_ID` | Session ID in the tagged `session_...` form |
| `CLAUDE_RUNNER_SESSION_UUID` | The same session ID in canonical UUID form |
| `CLAUDE_RUNNER_EXIT_REASON` | How the session ended; see the values below the table |
| `CLAUDE_RUNNER_WORKSPACE_PATHS` | Colon-separated absolute paths of the session's working trees. Empty for zero-repo sessions. |
| `CLAUDE_RUNNER_DEBUG_LOG_PATH` | Path to the session's debug log, still on disk while the hook runs |
| `CLAUDE_RUNNER_API_BASE_URL` | Anthropic API base URL for session-scoped calls |
| `CLAUDE_RUNNER_CLIENT_PLATFORM` | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, or `ios`. Unset when the session has no recorded or recognized surface, so reference it as `${CLAUDE_RUNNER_CLIENT_PLATFORM:-}` under `set -u`. Requires Claude Code v2.1.229 or later. |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | The session access token, for session-scoped API calls |
| `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_n`, `GIT_CONFIG_VALUE_n` | Git settings the runner fixes for the git your hook runs. [Git configuration inside lifecycle hooks](#git-configuration-inside-lifecycle-hooks) describes them. Requires Claude Code v2.1.280 or later. |

`CLAUDE_RUNNER_EXIT_REASON` takes one of four values:

* `completed`: the session ended cleanly. The Claude Code process exited normally, or exited by itself after the session was archived or deleted.
* `failed`: the Claude Code process crashed, or setup failed after it started.
* `interrupted`: the runner stopped the session, in one of these cases:
  * The runner released the session to free the slot.
  * The session timed out at startup.
  * The server moved the session off this runner.
  * The runner's poll noticed an archive or delete before the process exited.
  * The runner was draining.
  * The session outlasted its [`--kill-session-after-min`](/docs/en/self-hosted-environments-reference#runner-cli-flags) limit.
* `abandoned`: reserved for a session another runner claimed. The hook doesn't currently fire in that case.

If you compare hook receipts with the [session lifecycle counters](/docs/en/self-hosted-environments-reference#session-lifecycle-counter-semantics), expect some `interrupted` receipts to count as `completed` there. The counters count a release, a startup timeout, a server move, and an archive or delete that the runner's poll noticed first as `completed`, because the runner handed the slot back cleanly.

The hook's exit status never affects the session outcome; a failure is logged and ignored. The runner waits up to `--post-session-hook-timeout-sec`, 60 seconds by default, on every session end including runner shutdown. This example saves uncommitted work to a rescue branch:

```bash theme={null}
#!/usr/bin/env bash
set -u
export GIT_ALLOW_PROTOCOL=${GIT_ALLOW_PROTOCOL:-https:http:ssh}
IFS=':'
# -c overrides beat repo-local settings, blocking session-written fsmonitor,
# hook-path, and gpg-program config from executing code with the hook's
# privileges. -c commit.gpgsign=false also leaves these rescue commits
# unsigned under --configure-git.
# Repo-local credential.helper and pushurl still apply, and on a runner
# before v2.1.280 so does core.sshCommand; if the hook holds credentials
# the session didn't, see the note below the script.
g() { git -c core.fsmonitor=false -c core.hooksPath=/dev/null \
        -c commit.gpgsign=false "$@"; }
for ws in $CLAUDE_RUNNER_WORKSPACE_PATHS; do
  cd "$ws" 2>/dev/null || continue
  [ -z "$(g status --porcelain 2>/dev/null)" ] && continue
  g add -A
  g commit -q -m "runner snapshot: $CLAUDE_RUNNER_SESSION_ID ($CLAUDE_RUNNER_EXIT_REASON)" || continue
  g push -q origin "HEAD:refs/heads/rescue/$CLAUDE_RUNNER_SESSION_ID" || true
done
```

The `GIT_ALLOW_PROTOCOL` line in the script limits git to HTTPS, HTTP, and SSH remotes. If the runner's environment already sets a non-empty `GIT_ALLOW_PROTOCOL` list of its own, the script keeps that list.

The hook pushes with whatever git credentials are available in its own environment on the runner host. Under the [no-credentials-in-the-image posture](/docs/en/self-hosted-environments-deploy#configure-git), including when the built-in clone goes through the Anthropic git proxy, there are none, so mint a short-lived push credential inside the hook before pushing: exchange the session token the hook receives in `CLAUDE_CODE_SESSION_ACCESS_TOKEN` with your own token service, verifying it as [Verify session identity](/docs/en/self-hosted-environments-identity) describes. When the hook holds a credential the session didn't, replace `origin` with an operator-supplied URL and pass `-c credential.helper=` plus your own helper. [Git configuration inside lifecycle hooks](#git-configuration-inside-lifecycle-hooks) describes what session-written configuration can still affect.

#### Hook timing when the runner releases a session

A released session can resume on another runner. On a runner on v2.1.236 or later, what the session was doing at release decides whether it can resume before this hook finishes:

* **Idle after a turn, or timed out at startup**: the runner stops the child and runs this hook to completion. Only then does it release the session. A user message sent while the hook runs can't resume the session on another runner before the hook finishes.
* **Waiting for the user to answer a prompt, such as a permission prompt**: the runner releases the session first, then runs this hook. A user message sent while the hook runs can resume the session on another runner before the hook finishes.

This applies whenever the runner releases a session: at the idle timeout, at the [`--retire-at`](/docs/en/self-hosted-environments-reference#runner-cli-flags) time, and, on a runner on v2.1.260 or later, at a session's [`--kill-session-after-min`](/docs/en/self-hosted-environments-reference#runner-cli-flags) limit. A session whose turn has ended and that holds only background tasks counts as idle here. Before v2.1.236, the runner released the session first and then ran this hook in both cases.

During a `SIGTERM` drain, the runner holds the session lease until the hook finishes; see [Shutdown timing](/docs/en/self-hosted-environments-deploy#shutdown-timing).

### Git configuration inside lifecycle hooks

The `checkout` and `post-session` hooks run with the session's access token in their environment, and the git they run reads configuration files that sessions can write, such as `~/.gitconfig` and a checkout's `.git/config`. Before either hook runs, the runner sets git settings in the hook's environment, including the ones below, as `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` pairs and git environment variables. Git ranks those above every configuration file, and they apply only to the git your hooks run, not to the session's own git. At startup, the runner prints a `[runner:git] lifecycle hooks:` line that shows the hooks path, allowed protocols, gpg programs, and signing mode in effect. Requires Claude Code v2.1.280 or later.

* **Git hooks**: unless you supply a value, `core.hooksPath` is `/dev/null`, so git skips the hooks in a repository's `.git/hooks` and any hooks directory that `~/.gitconfig` names. To supply one, export `core.hooksPath` as a `GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` pair in the runner's environment. The runner also reads `core.hooksPath` from the system git configuration, and uses it only when the runner's user can't write that file, the directory it names, or the hook files in it. When the runner ignores a value, a `[runner:warn]` line at startup names the value and the reason.
* **File system monitor**: `core.fsmonitor` is empty, so git in your hook doesn't run a monitor program that a configuration file names.
* **Remote protocols**: `GIT_ALLOW_PROTOCOL` is `https:http:ssh`. A clone, fetch, or push that uses a local path, a `file://` URL, or a `git://` URL fails with `fatal: transport 'file' not allowed` or `fatal: transport 'git' not allowed`.
* **SSH command and credential prompt**: git in your hook ignores `core.sshCommand` and `core.askPass` from configuration files. To use your own SSH command, set `GIT_SSH_COMMAND` in the runner's environment. To use a credential prompt program, set `GIT_ASKPASS` there. Sessions inherit the runner's environment, so both variables also reach the session's own git. Don't put a credential in either.
* **gpg programs**: `gpg.program`, `gpg.openpgp.program`, `gpg.x509.program`, and `gpg.ssh.program` are paths the runner sets, never values from a configuration file.
* **Commit signing**: with [`--configure-git`](/docs/en/self-hosted-environments-deploy#let-the-runner-configure-git), commits you make from a hook are signed as the session. Without the flag, `commit.gpgsign` and `tag.gpgsign` are `false`.

To change one of these settings, use the runner's environment or a `git -c` option inside the hook:

* **Configuration pairs**: a `GIT_CONFIG_KEY_n`/`GIT_CONFIG_VALUE_n` pair you export in the runner's environment replaces the runner's value for the same key. Number your pairs from `0` and set `GIT_CONFIG_COUNT` to how many there are. When the last pair the count announces is missing, the runner ignores all of your pairs and logs a `[runner:warn]` line at startup.
* **Git environment variables**: the runner leaves `GIT_ALLOW_PROTOCOL`, `GIT_SSH_COMMAND`, and `GIT_ASKPASS` as you set them in its environment.
* **`git -c` options**: a `git -c` option inside the hook overrides a `GIT_CONFIG_KEY_n` pair, the runner's or yours. It doesn't change `GIT_ALLOW_PROTOCOL`, `GIT_SSH_COMMAND`, or `GIT_ASKPASS`, which git reads ahead of any configuration.

Git in your hook still reads every setting the runner doesn't set, such as credential helpers, `url.*.insteadOf` rewrites, and filter drivers, from every configuration file, including the ones sessions can write. A credential helper or filter driver named in one of those files runs as a program with your hook's privileges, and configuration in those files can still change where a push from your hook goes, including a push to a URL you pass on the command line.

Before v2.1.280, the runner set none of these settings, and under `--configure-git` a commit made from a hook failed unless the hook passed `-c commit.gpgsign=false`.

### command

Runs once per session after checkout, in place of the built-in child spawn. The hook receives the same environment as a [wrapper script](#wrapper-scripts) and should `exec` into `"$CLAUDE_RUNNER_CLAUDE_BIN"` the same way. Use the `command` hook to keep all customization in one hooks directory; use `--exec-path` when the wrapper lives elsewhere. If `--exec-path` is also set, the flag takes precedence and the `command` hook is ignored.

Always `exec` the runner's own binary rather than a PATH-resolved `claude`; otherwise you defeat [version pinning](/docs/en/self-hosted-environments-deploy#pin-the-version).

## On-demand runners

Instead of running a fixed fleet, you can boot one runner per session. The orchestrator is a separate, stateless subcommand that polls Anthropic for spawn requests, one per session that's queued with no runner available, and runs your `spawn-runner` hook for each. Your hook submits a workload to your platform: a Kubernetes Job, an EC2 instance, a Nomad dispatch.

On-demand runners improve credential hygiene. On a fixed fleet, the environment secret lives on every runner host, which is the same host that runs user sessions. With the orchestrator, the environment secret stays only on the orchestrator host, which never runs user code; each spawned runner receives a single-use work order that registers exactly one runner and then expires.

To start the orchestrator, pass the environment secret and a hooks directory containing an executable `spawn-runner` script:

```bash theme={null}
claude self-hosted-runner orchestrator \
  --environment-secret-file /etc/claude/environment-secret \
  --hooks-dir /etc/claude/hooks
```

The orchestrator keeps no state between polls, so you can run two or more replicas against the same environment for availability. Each spawn request is claimed server-side by exactly one replica. All replicas must use the same `--expected-spawn-seconds` value; see the [hook contract](#the-spawn-runner-hook).

### The spawn-runner hook

The orchestrator runs `${hooks-dir}/spawn-runner` once per spawn request. The hook must submit work asynchronously, without waiting for the runner to boot, and return within `--hook-timeout`, 60 seconds by default. The hook receives:

| Variable | Description |
| :- | :- |
| `CLAUDE_RUNNER_WORK_ORDER_FILE` | Path to a temp file containing the signed work-order JWT the new runner registers with. Deleted after the hook exits. Don't log the file's contents. |
| `CLAUDE_RUNNER_ORDER_ID` | Opaque idempotency key, unique per spawn request and safe for Kubernetes resource names. Use only the order ID as your provisioner's dedup key. |
| `CLAUDE_RUNNER_SESSION_ID` | The session this request is for. It repeats on every re-request for the session, so use it for logging and routing, not as a dedup key. Empty for pre-warming requests, which boot a standby runner ahead of any specific session when [`--min-idle`](/docs/en/self-hosted-environments-reference#orchestrator-cli-flags) is set, so don't assume the variable is set. |
| `CLAUDE_RUNNER_SESSION_UUID` | The same session ID in canonical UUID form. Empty for pre-warming requests. |
| `CLAUDE_RUNNER_ATTEMPT` | A per-session counter to use for logging. It isn't a retry count or a request count. `0` for pre-warming requests, though a request for a session can carry `0` too. |
| `CLAUDE_RUNNER_ORDER_SERVER_TIME` | Server time from the poll response's HTTP `Date` header. When the hook verifies the work-order JWT's `exp`, compare against this value instead of the local clock to tolerate skew. Empty when the gateway omitted the header. |
| `CLAUDE_RUNNER_POOL_ID` | The ID of the environment the new runner should join, in `ccpool_...` form |
| `CLAUDE_RUNNER_ACCOUNT_ID` | Tagged ID of the account that enqueued the session, for per-account routing, quota, or chargeback. Empty when unavailable, and always empty for Claude Tag channel sessions, which no account enqueues. |
| `CLAUDE_RUNNER_ACCOUNT_EMAIL` | Email of the account that enqueued the session. Empty when unavailable. Treat the email as personally identifiable information and don't log it. |
| `CLAUDE_RUNNER_PRIMARY_REPO_URL` | URL of the session's first git source, for routing to a runner with that repository pre-warmed. Empty when the session has no git sources. |
| `CLAUDE_RUNNER_PRIMARY_REPO_REVISION` | Revision of the session's first git source: branch, SHA, tag, or full reference name. Empty when unspecified. |
| `CLAUDE_RUNNER_REPO_SOURCES` | JSON array of `{url, revision}` for all the session's git sources, for hooks that route on a secondary repository. Empty when there are no sources. |
| `CLAUDE_RUNNER_CORRELATION_ID` | The correlation ID supplied at session create, echoed back so the hook can map this work order to the request that created the session. Empty when the session has none. |
| `CLAUDE_RUNNER_CLIENT_PLATFORM` | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, `ios`, or `scheduled_trigger`, for adoption analytics. Unset when the session has no recorded or recognized surface, and for pre-warming requests; check it with `[ -n "${CLAUDE_RUNNER_CLIENT_PLATFORM:-}" ]`, which stays safe under `set -u`. |

The spawned runner registers with the work order in place of the environment secret:

* **Start it with the work order**: point [`--environment-secret-file`](/docs/en/self-hosted-environments-reference#runner-cli-flags) at a file containing the work-order JWT, or set `SELF_HOSTED_RUNNER_ENVIRONMENT_SECRET` to the JWT value.
* **Copy the JWT before the hook exits**: the orchestrator deletes the work-order file after the hook exits, so copy the JWT into the workload you submit, such as a Kubernetes Secret on the spawned Job, rather than passing the file path through.
* **Use `--capacity 1` on spawned runners**: a session-bound work order registers exactly one runner bound to that session, so a higher capacity adds slots that never receive work, and the runner logs a warning at startup.
* **Pre-warming work orders register unbound**: the standby runner isn't bound to a session and claims queued work like a fixed-fleet runner.

The contract has four rules, whichever platform your hook provisions on:

1. **Be idempotent on `CLAUDE_RUNNER_ORDER_ID`.** Redelivery of the same request must spawn at most one runner. Derive a deterministic resource name from the order ID and let your platform reject the duplicate. Don't key on `CLAUDE_RUNNER_SESSION_ID` instead. Every re-request for a session carries the same session ID with a new order ID, so a workload named or deduplicated by the session ID is created once and never again for that session.
2. **Don't retry the workload.** One order ID means at most one created workload. If the runner never registers, Anthropic re-requests with a fresh order ID after `--expected-spawn-seconds`.
3. **Use the exit-code contract.** Exit with the status that matches the outcome:

   * **Exit 0**: submitted.
   * **Exit 1**: retryable failure. The session backs off and is re-offered.
   * **Exit 2 or higher**: non-retryable failure. The session is blocked from spawning again until a user sends it a new message or an [Owner](/docs/en/cloud-environments#organization-shared-environments) selects **Retry** on it in the environment's **Activity** tab.

   On non-zero exit, the tail of the hook's stderr appears in the **Activity** tab as the failure reason, so write the actionable error to stderr and never write secrets there. In a shell hook, [keep transient failures retryable](#keep-transient-failures-retryable-in-a-shell-hook).

   A pre-warming request has no session to fail: the orchestrator logs a non-zero exit locally only, and the server re-requests the spawn after the `--expected-spawn-seconds` lease expires.
4. **Set `--expected-spawn-seconds` to at least your p99 time from spawn request to runner registration.** Measure from when the orchestrator receives the spawn request, and include any wait for capacity on your platform as well as boot time. This value is the server-side lease, and the work order expires with it, so a runner whose workload takes longer can't register. All orchestrator replicas must use the same value.

Everything the hook writes to stdout or stderr appears in the orchestrator's log with credentials automatically redacted. If sessions stay queued, check the orchestrator's `/healthz` body for queue counts, then open your environment's **Activity** tab on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments): expand a failed session there for its spawn error, and select **Retry** to re-request it.

A session that stays queued with no spawn error in the **Activity** tab can mean the hook is keyed on the session ID. To confirm, check whether your platform has a workload for that session's first spawn request and none for the re-requests. If so, key the workload on `CLAUDE_RUNNER_ORDER_ID` instead.

#### Keep transient failures retryable in a shell hook

In a shell hook that uses `set -e`, a failure that a retry could have cleared can block the session. The hook stops at the failing command and exits with that command's own status, and the orchestrator applies the exit-code contract to that status. Many failures return a status of 2 or higher, such as `127` when a command isn't installed and `22` from `curl --fail` on an HTTP error, so they block the session at its first failure.

A session the hook has already blocked stays blocked until a user sends it a new message or an [Owner](/docs/en/cloud-environments#organization-shared-environments) selects **Retry** on it in the environment's **Activity** tab.

To turn such a failure into exit 1 instead, put these lines directly below the hook's `#!` line, above anything that can fail:

```bash theme={null}
set -e
PERMANENT=; permanent() { printf '%s\n' "$*" >&2; PERMANENT=1; exit 2; }
trap 'rc=$?; [ "$rc" -eq 0 ] || [ -n "${PERMANENT:-}" ] || exit 1' EXIT
```

These lines change how the rest of the hook behaves, so check it for each of these patterns after you add them:

* **Bare `exit 2` or higher**: with the trap set, it becomes exit 1. For an error that no retry can fix, call `permanent` with the reason instead, such as `permanent "namespace claude-runners does not exist"`. Call it in the main shell, not inside `$( )`, `( )`, or a pipe.
* **`exec`**: don't start the hook's last command with `exec`, because `exec` replaces the shell and the trap doesn't run.
* **Second `EXIT` trap**: a second `trap ... EXIT` replaces the first, so merge the two into a single trap. Put your cleanup commands directly after `rc=$?;` and end each with `|| true;`. Cleanup then runs on failure as well as on success, and a failing cleanup command doesn't set the hook's exit status. This merged trap shows the shape, with `your-cleanup-command` standing in for your own:

  ```bash theme={null}
  trap 'rc=$?; your-cleanup-command || true; [ "$rc" -eq 0 ] || [ -n "${PERMANENT:-}" ] || exit 1' EXIT
  ```
* **Commands that are allowed to fail**: if the hook didn't use `set -e` before, it now stops at the first command that returns non-zero, such as a lookup that finds nothing or a duplicate submit that your platform rejects. If the hook acts on the result, make that command the condition of an `if`. If it ignores the result, follow the command with `|| true`.

To confirm the trap works, add a line directly below the `trap` line that calls a command that doesn't exist, such as `no-such-command`. Run the hook file from your shell and check that `echo $?` prints `1`, then remove the line.

## Send model requests to Bedrock or Agent Platform

If your organization needs model requests to go through its own AWS or Google Cloud account, configure the runner for [Amazon Bedrock](/docs/en/amazon-bedrock) or [Google Cloud's Agent Platform, formerly Vertex AI](/docs/en/google-vertex-ai). Every session that runner starts then calls the model in your cloud account, with your cloud credentials. Without this configuration, sessions send model requests to the Anthropic API.

The runner still polls Anthropic for sessions, and each session still sends its event stream to `api.anthropic.com`. The event stream carries prompts, responses, and tool results. The plan requirement and the Zero Data Retention exclusion in [Availability and limitations](/docs/en/self-hosted-environments#availability-and-limitations) still apply.

Sessions are routed to an environment, not to a runner, and a requeued or resumed session can run on a different runner. Configure every runner in the environment the same way. Before you start, read [what differs on these providers](#what-differs-from-sessions-on-the-anthropic-api).

<Steps>
  <Step title="Prepare the cloud account and your egress rules">
    Set up model access, a narrowly scoped policy or role, and network access:

    * **Amazon Bedrock**: [submit use case details](/docs/en/amazon-bedrock#1-submit-use-case-details), then create the policy in [IAM configuration](/docs/en/amazon-bedrock#iam-configuration), limiting `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` to the inference profiles your sessions use and the foundation models behind them
    * **Agent Platform**: [enable the API](/docs/en/google-vertex-ai#1-enable-agent-platform-api) and [request model access](/docs/en/google-vertex-ai#2-request-model-access), then create the custom role that [IAM configuration](/docs/en/google-vertex-ai#iam-configuration) describes, with only `aiplatform.endpoints.predict`
    * **Egress**: allow your provider's endpoints through your egress rules. See [Network requirements](/docs/en/self-hosted-environments-deploy#network-requirements). If sessions can't reach them, Claude Code can keep retrying for hours before the session shows an error.
  </Step>

  <Step title="Give sessions narrowly scoped credentials">
    Attach the policy or role from step 1 to an identity that can do nothing else. For the methods Claude Code accepts, see [Configure AWS credentials](/docs/en/amazon-bedrock#2-configure-aws-credentials) and [Configure GCP credentials](/docs/en/google-vertex-ai#3-configure-gcp-credentials).

    <Warning>
      Anyone who can get code to run in a session, including through prompt injection, can use these credentials at your cost for as long as the credentials are valid. Claude Code runs inside the session, so the credential it calls the model with has to be readable there.

      The shell commands Claude runs, your [Claude Code hooks](/docs/en/hooks), and stdio MCP servers inherit the session's environment and run as the same user as Claude Code. As a result, they can read credential variables and credential files.

      When you [harden your deployment](/docs/en/self-hosted-environments-deploy#harden-your-deployment), you keep host credentials out of sessions, but you can't keep this credential out. Give the identity behind it nothing beyond the policy or role from step 1.
    </Warning>

    Check the method you choose against these runner behaviors:

    * **Metadata endpoint**: if you deny sessions the [cloud metadata endpoint](/docs/en/self-hosted-environments-deploy#harden-your-deployment) outright, credentials served from it, such as an instance profile, don't reach Claude Code either. A file-based web identity, such as IAM Roles for Service Accounts (IRSA) on Amazon EKS or a Workload Identity Federation credential file, doesn't depend on it.
    * **Renewal**: a session can outlive a credential, so use a method that renews itself, such as a file-based web identity
    * **Wrapper script**: the runner starts your [wrapper script](#provision-credentials-scoped-to-the-session-creator) once per session, so credentials it exports aren't renewed. Claude Code reads AWS credentials from its environment, so if your wrapper already exports AWS credentials for other work, Claude Code can sign model requests with them.
  </Step>

  <Step title="Set one provider's variables in the runner's environment">
    Set exactly one provider's variables where you set the runner's other environment variables, such as the container spec or service unit, then restart the runner. The examples show them as shell exports. With [on-demand runners](#on-demand-runners), set them on the workload your `spawn-runner` hook starts.

    Start these runners with [`--confine-repo-settings enforce`](/docs/en/self-hosted-environments-deploy#harden-your-deployment). It refuses sessions on repositories whose committed settings it flags, so run in the default `warn` mode first and clear what it logs.

    <Tabs>
      <Tab title="Amazon Bedrock">
        Replace the region with your own:

        ```bash theme={null}
        export CLAUDE_CODE_USE_BEDROCK=1
        export AWS_REGION=us-east-1
        ```

        For how Claude Code resolves the region, see [Configure Claude Code](/docs/en/amazon-bedrock#3-configure-claude-code). For which inference profile prefix Claude Code uses for your region, see [Cross-region inference profile prefixes](/docs/en/amazon-bedrock#cross-region-inference-profile-prefixes).
      </Tab>

      <Tab title="Google Cloud's Agent Platform">
        Replace the region and project ID with your own:

        ```bash theme={null}
        export CLAUDE_CODE_USE_VERTEX=1
        export CLOUD_ML_REGION=global
        export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID
        ```

        To choose a region, see [Region configuration](/docs/en/google-vertex-ai#region-configuration).
      </Tab>
    </Tabs>
  </Step>

  <Step title="Check that the variables reached a session">
    Your own shell on the host is a different process, so check from inside a session. Start one in the environment and ask Claude to run this command:

    ```bash theme={null}
    env | grep -E 'CLAUDE_CODE_USE_(BEDROCK|VERTEX)'
    ```

    A line that sets `CLAUDE_CODE_USE_BEDROCK` or `CLAUDE_CODE_USE_VERTEX` to `1` means the variable reached the session. If both appear, Claude Code uses Amazon Bedrock. No output means neither reached it.

    The command shows configuration, not traffic. To confirm the requests themselves, look for them in your cloud account's own metrics or request logs. If the first message fails instead, see troubleshooting for [Amazon Bedrock](/docs/en/amazon-bedrock#troubleshooting) or [Agent Platform](/docs/en/google-vertex-ai#troubleshooting).
  </Step>
</Steps>

### What differs from sessions on the Anthropic API

A session that sends model requests to Amazon Bedrock or Google Cloud's Agent Platform differs from a session on the Anthropic API in these ways:

* **Policy from claude.ai**: [server-managed settings](/docs/en/server-managed-settings) don't reach these sessions. Neither do the organization policies an Owner sets in Claude Code admin settings, so Claude Code doesn't enforce them inside the session. Put the rules you rely on in the runner image's [managed settings file](/docs/en/managed-settings#delivery-mechanisms).
* **Account skills**: these sessions don't download the skills enabled for a person's claude.ai account. See [How each session's config is assembled](#how-each-session’s-config-is-assembled).
* **Files**: files that people attach to a session in claude.ai or the mobile or desktop app don't reach it, and Claude can't send files back with the [`SendUserFile` tool](/docs/en/tools-reference). Put input files in the repository or on the runner instead.
* **Model selection**: Anthropic's control plane sends each session's model, and when a session starts without one, Claude Code uses its default for the provider. You can't choose the model with `ANTHROPIC_MODEL` or `ANTHROPIC_DEFAULT_MODEL` in the runner's environment, but you can pin what an alias resolves to:
  * **`ANTHROPIC_MODEL` and `ANTHROPIC_DEFAULT_MODEL`**: the runner removes them from the environment it passes to sessions, even though the provider pages' examples set `ANTHROPIC_MODEL`.
  * **Per-family pinning variables**: the variables in Pin model versions for [Amazon Bedrock](/docs/en/amazon-bedrock#4-pin-model-versions) and [Agent Platform](/docs/en/google-vertex-ai#5-pin-model-versions) do reach sessions. They decide what an alias such as `opus` resolves to, not what a full model ID resolves to.
* **Models your account doesn't serve**: a session can fail on a message with an error that names the model. Enable the models your developers can choose, the background model described in Pin model versions, and the classifier model that [auto mode](/docs/en/permission-modes#enable-auto-mode-on-bedrock-agent-platform-or-foundry) uses. On Amazon Bedrock, allow each of them in your policy.
* **Web search and fast mode**: [web search](/docs/en/tools-reference#websearch-tool-behavior) isn't available on Amazon Bedrock, and [fast mode](/docs/en/fast-mode) isn't available on either provider. For other capabilities that differ by provider, see [CLI capabilities that vary by provider](/docs/en/feature-availability#cli-capabilities-that-vary-by-provider).

## MCP servers

To make [MCP servers](/docs/en/mcp) available in every session, add them at image build time with the same `claude mcp add` command used on a desktop install. If your runner is a bare process rather than a container, run the same command as the runner's user on the host, then restart the runner: it reads host config once at startup. The `--scope user` flag is required; the default local scope writes under a per-directory key that the runner doesn't seed into sessions. For example, in your Dockerfile:

```dockerfile theme={null}
RUN claude mcp add --scope user sidecar -- /usr/local/bin/mcp-sidecar
RUN claude mcp add --scope user --transport http internal http://mcp-gateway.svc.cluster.local:8080
```

The runner snapshots the host's config once at startup. The snapshot captures the `mcpServers` key from the host's `.claude.json`, which lives next to rather than inside `~/.claude/`, and the runner seeds only that key into each session's isolated config; account state and project history are dropped. To confirm the servers reached sessions, start a session on the environment and ask Claude to list its MCP tools; the runner also logs a startup warning for any captured entry whose `type` it doesn't recognize and drops the entry, so you can see why that server is missing from sessions. When `SELF_HOSTED_RUNNER_HOST_CONFIG_DIR` is set, the runner reads `.claude.json` from that directory instead, so pointing the variable at an empty directory disables MCP seeding too.

Claude Code also loads MCP servers from other sources:

* The enterprise-scope [managed MCP file](/docs/en/managed-mcp) at its standard system path: `/etc/claude-code/managed-mcp.json` on Linux runner hosts, `/Library/Application Support/ClaudeCode/managed-mcp.json` on macOS hosts. Use it for locked-down fleets where only administrator-listed servers may load. See [exclusive control with managed-mcp.json](/docs/en/managed-mcp#exclusive-control-with-managed-mcp-json) for the precedence rules. When this file is on the runner host, Claude Code skips the MCP servers Anthropic's control plane delivers to a session, including claude.ai connectors, and names them in a warning on the session child's stderr, which the runner records at the `debug` log level. Before v2.1.229, those sessions exited at startup with `You cannot dynamically configure MCP servers when an enterprise MCP config is present`.
* The [`managedMcpServers`](/docs/en/settings-reference#managedmcpservers) key in [managed settings](/docs/en/managed-settings) on the runner host: provides HTTP and SSE servers without taking exclusive control, so servers from the other sources still load. Requires Claude Code v2.1.259 or later.
* `<repo>/.mcp.json`: project scope. Commit the file to the repository; its servers are auto-approved in cloud sessions. In a session with several repositories, [at most one repository's file loads](#repository-settings-in-sessions-with-several-repositories).

When connector delivery is enabled for your organization, Anthropic's control plane delivers the connectors you've configured on claude.ai to interactively-created sessions through server-provided MCP configuration, routed through `api.anthropic.com`. Sessions created programmatically, such as [CLI dispatches](/docs/en/self-hosted-environments-testing#run-the-test-loop), don't receive connector delivery; give them MCP servers through any of the other sources this section lists instead. The child's OAuth token doesn't carry a scope for fetching connectors directly, so the child doesn't attempt that fetch itself; delivery is server-driven.

`settings.json` doesn't carry MCP server definitions, and there is no top-level `mcpServers` field in the settings schema. In managed settings, provide servers with the [`managedMcpServers`](/docs/en/settings-reference#managedmcpservers) key instead.

Sessions inherit the runner's environment, so set [`ENABLE_TOOL_SEARCH`](/docs/en/mcp#scale-with-mcp-tool-search) there to control MCP tool search for every session a runner spawns; the MCP page covers the values.

<a id="connection-timing" />

### Wait for MCP servers before the first turn

A self-hosted session waits briefly for MCP servers that are still connecting, at two separate points. A server that misses a wait has its tools missing when the first turn starts, and they become available later with no action on your part. The two waits are:

* **Session startup**: before the tool list is first taken, the session waits up to 5 seconds by default for an HTTP or SSE server whose entry sets [`alwaysLoad: true`](/docs/en/mcp#exempt-a-server-from-deferral), or for all servers when you set [`MCP_CONNECTION_NONBLOCKING=0`](/docs/en/env-vars) in the runner's environment. HTTP and SSE servers otherwise connect in the background. While the session waits here, it's slower to initialize. [`MCP_CONNECT_TIMEOUT_MS`](/docs/en/env-vars) changes the 5-second default.
* **First turn**: after the message arrives, the first turn waits up to 2 seconds for stdio servers that are still connecting. While the session waits here, the first reply is slower. To change how long this wait lasts, set [`CLAUDE_CODE_MCP_STARTUP_WAIT_MS`](/docs/en/env-vars) in the runner's environment. It doesn't change which servers the wait covers. Requires Claude Code v2.1.274 or later.

`claude mcp add` has no `alwaysLoad` flag. To set the key, add the server with `claude mcp add-json` instead, which takes it in the server's JSON and writes it to `.claude.json`. In your Dockerfile:

```dockerfile theme={null}
RUN claude mcp add-json core '{"type":"http","url":"https://mcp.example.com/mcp","alwaysLoad":true}' --scope user
```

If a server's tools don't appear on later turns either, check whether the server reached the session at all, as [MCP servers](#mcp-servers) describes.

### Turn off built-in session tools

Anthropic's control plane attaches its own MCP server, named Claude Code Remote, to cloud sessions. Claude uses the server's tools to schedule [routines](/docs/en/routines), start and steer other cloud sessions, attach more repositories, and follow pull request activity.

To turn off the whole server, add a [server-level deny rule](/docs/en/permissions#mcp) to your settings. The control plane registers the server under one of three names, depending on how the session was created. Claude Code matches the name in a rule exactly, including case, so write the rule once per name as shown:

```json theme={null}
{
  "permissions": {
    "deny": [
      "mcp__Claude_Code_Remote",
      "mcp__claude-code-remote",
      "mcp__bf7c680d-5fdc-5ef4-b4a0-abadb619bf0a"
    ]
  }
}
```

A rule that names the whole server covers tools the server gains later too. To turn off one tool and keep the rest, append two more underscores and the tool name to each rule, as in `mcp__Claude_Code_Remote__add_repo`. To block the server from connecting at all rather than removing its tools, add the three names without the `mcp__` prefix as `serverName` entries under [`deniedMcpServers`](/docs/en/managed-mcp#policy-based-control-with-allowlists-and-denylists) instead.

Put the rules in [server-managed settings](/docs/en/server-managed-settings) to reach sessions with no change to the runner, or in `~/.claude/settings.json` on the runner. On a runner that [sends model requests to Bedrock or Agent Platform](#send-model-requests-to-bedrock-or-agent-platform), use that file, because server-managed settings don't reach those sessions. [Permissions and tool approval](#permissions-and-tool-approval) explains how settings on the runner reach sessions.

To confirm the rules took effect, start a session on the environment and ask Claude to list its MCP tools. Claude Code removes a denied tool from Claude's context, so the denied tools are absent from its answer.

## Prompt sessions to push their work

Anthropic-hosted sessions run a [`Stop` hook](/docs/en/hooks#stop), the Claude Code hook that runs when Claude finishes responding, that prompts Claude to commit and push its work. The runner doesn't install one. Without it, a session that ends with uncommitted changes leaves that work only on the runner's disk, and the **Create PR** button in claude.ai/code stays inactive until the branch exists on the remote.

The reference implementation below has two parts. Merge the settings block into `~/.claude/settings.json` on the runner host, which the runner seeds into every session, and save the script as `~/.claude/hooks/stop-hook-nudge.sh` on the runner host and make it executable:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "timeout": 10,
            "command": "\"$CLAUDE_CONFIG_DIR/hooks/stop-hook-nudge.sh\""
          }
        ]
      }
    ]
  }
}
```

```sh theme={null}
#!/bin/sh
# Stop-hook reference implementation for self-hosted runners.
#
# Nudges Claude once per turn if the project directory has uncommitted
# changes OR unpushed commits, so work isn't lost when an idle session
# is released and so the "Create PR" button on claude.ai/code lights up.
#
# Runner-level (no repo changes): drop this file at ~/.claude/hooks/ on
# the runner host and merge the accompanying Stop-hook settings block
# into ~/.claude/settings.json — the runner seeds both into every session.
# Repo-level alternative: commit to <repo>/.claude/hooks/ and change the
# settings.json command path to $CLAUDE_PROJECT_DIR/.claude/hooks/.
#
# stdin: hook JSON payload (see https://code.claude.com/docs/en/hooks)
# stdout: {"decision":"block","reason":"..."} to nudge, or nothing to allow stop.

# Re-entry guard: the harness sets stop_hook_active=true when re-invoking
# the Stop hook after a block. Bail so we only nudge once per turn. The
# harness emits compact JSON (no space after the colon), which this
# pattern relies on; use jq if you need a whitespace-tolerant check.
in=$(cat)
case "$in" in *'"stop_hook_active":true'*) exit 0 ;; esac

d="$CLAUDE_PROJECT_DIR"

# Not a git repo → nothing to nudge.
git -C "$d" rev-parse --git-dir >/dev/null 2>&1 || exit 0

# No remote → "push to the remote" is unsatisfiable; bail.
[ -z "$(git -C "$d" remote 2>/dev/null)" ] && exit 0

# Uncommitted changes (staged, unstaged, or untracked). Exclude .claude/
# entirely — operator-seeded settings and CLI-written runtime state
# (scheduler lock, worktrees, routine state) live there and neither is
# "uncommitted work" the model needs to push.
s=$(git -C "$d" status --porcelain -- . ':(exclude).claude/' 2>/dev/null)
if [ -n "$s" ]; then
  printf '{"decision":"block","reason":"There are uncommitted changes in the repository. Please commit and push these changes to the remote branch."}'
  exit 0
fi

# Unpushed commits. Count commits on HEAD not reachable from any
# remote-tracking ref or FETCH_HEAD. This works uniformly for:
#   - init+fetch checkouts (runner default: only FETCH_HEAD exists)
#   - clone-based checkouts (origin/* exist)
#   - the runner default: the child starts on the session's outcome
#     branch, which the runner creates after checkout
#   - detached HEAD, when a custom setup skips that branch creation
# With no reference point at all (never fetched), stay silent rather
# than false-positive on a read-only turn.
base=""
git -C "$d" rev-parse --verify -q FETCH_HEAD >/dev/null && base="FETCH_HEAD"
if [ -z "$base" ] && [ -z "$(git -C "$d" for-each-ref --count=1 refs/remotes/origin 2>/dev/null)" ]; then
  exit 0
fi
# shellcheck disable=SC2086  # $base is either "" or "FETCH_HEAD", intentional word-split
unpushed=$(git -C "$d" rev-list HEAD --not $base --remotes=origin --count 2>/dev/null) || unpushed=0
if [ "$unpushed" -gt 0 ]; then
  branch=$(git -C "$d" symbolic-ref --short -q HEAD)
  if [ -n "$branch" ]; then
    # $branch is attacker-influenced — git-check-ref-format(1) allows `"`
    # in ref names. `\` is forbidden (rule 10) but escaped anyway as cheap
    # defense-in-depth.
    # Escape JSON metacharacters before interpolating into the hand-built
    # payload so a branch like x","continue":false can't inject keys into
    # the hook-output JSON the harness parses. $unpushed is safe — the
    # -gt guard above rejects anything that isn't a plain integer.
    branch_esc=$(printf '%s' "$branch" | sed 's/\\/\\\\/g; s/"/\\"/g')
    printf '{"decision":"block","reason":"There are %s unpushed commit(s) on branch '\''%s'\''. Please push these changes to the remote repository."}' "$unpushed" "$branch_esc"
  else
    printf '{"decision":"block","reason":"There are %s unpushed commit(s) on a detached HEAD. Please create a branch and push it to the remote repository."}' "$unpushed"
  fi
  exit 0
fi

exit 0
```

The hook prompts Claude to commit and push before the session ends, and stays silent when the directory isn't a git repository or has no remote. For a session with several repositories, see [what `$CLAUDE_PROJECT_DIR` names](#repository-settings-in-sessions-with-several-repositories).

## Permissions and tool approval

A self-hosted session has no terminal attached, so an unanswered permission prompt stalls the turn until the user responds in the UI. Anthropic's control plane sends each session's tool list and permission rules with the work payload; the default configuration pre-approves routine tool calls, including `Bash`, and cloud sessions [pre-approve file edits regardless of mode](/docs/en/permission-modes#switch-permission-modes). A call that nothing pre-approves prompts through the session UI.

<Note>
  Only pin auto mode on an environment whose session containers run with [default-deny network egress](/docs/en/self-hosted-environments-deploy#default-deny-egress) and the rest of the [hardening section](/docs/en/self-hosted-environments-deploy#harden-your-deployment) in place. Routine tool calls, including `Bash` network requests, run without a human in the loop on both the default pre-approved tool set and in auto mode, so the network boundary is what limits where those calls can reach.
</Note>

To keep prompts to a minimum regardless of what the control plane sends, pin [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) from your wrapper script or [`command` hook](#command). Auto mode lets sessions run without routine permission prompts: a separate classifier model reviews actions before they run and blocks the ones it rejects, and explicit ask rules still force a prompt; the permission modes page covers what the classifier checks. The runner appends server-computed flags before invoking the wrapper, and for single-value flags such as `--permission-mode` the parser honors the last occurrence, so a flag you append after `"$@"` overrides the server-sent value:

```bash theme={null}
#!/bin/bash
exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@" --permission-mode auto
```

To pre-approve specific tools instead, append `--allowed-tools` with your rules, for example `--allowed-tools "Bash(bazel *) Bash(yarn *) mcp__internal__*"`. List flags such as `--allowed-tools` and `--disallowed-tools` accumulate across occurrences rather than overriding, so your rules apply on top of any rules the control plane sends. To narrow, append `--disallowed-tools`, which denies tools even if another rule allows them.

### How each session's config is assembled

The runner gives each session its own config directory, seeded from a snapshot of the host's `~/.claude/` that the runner captures once at startup: `settings.json`, `CLAUDE.md`, hooks, agents, commands, and skills in your runner image apply to every session as the user-level baseline. If you change config on a running host, the change takes effect only after you restart the runner.

Set `SELF_HOSTED_RUNNER_HOST_CONFIG_DIR` to seed from a different path, or point it at an empty directory to disable seeding.

Sessions also read these settings files:

* **Project settings**: a repository-committed `.claude/settings.json` layers on top of the user-level baseline. In a session with several repositories, [at most one repository's file takes effect](#repository-settings-in-sessions-with-several-repositories).
* **Managed settings**: sessions read [`managed-settings.json`](/docs/en/settings#where-settings-live) from the standard system path in your runner image. For whether its keys apply alongside [server-managed settings](/docs/en/server-managed-settings), see [how Claude Code combines managed sources](/docs/en/managed-settings#how-claude-code-combines-managed-sources).

For the order these sources apply in, see [settings precedence](/docs/en/settings#settings-precedence).

When Anthropic's control plane supplies a session with [Claude Code hooks](/docs/en/hooks), the runner installs them alongside, not over, your own configuration. Requires Claude Code v2.1.229 or later.

* **Where they land**: the runner writes each supplied hook script to a reserved `hooks/.ccr-launcher/` subdirectory of the session's config directory and registers the scripts in a separate settings file it passes to the session with `--settings`, leaving the seeded `settings.json` and your own scripts at `hooks/<name>` untouched. The runner recreates the reserved subdirectory for each session and doesn't seed host content at `~/.claude/hooks/.ccr-launcher/` into sessions.
* **Who authors them**: the control plane populates the scripts from fixed constants in its own deployment, never from per-session or third-party input.
* **What still governs them**: hooks delivered through `--settings` enter the ordinary merged hook configuration, not the managed tier, so your managed settings still apply. `disableAllHooks` disables them, and they are not among the categories [`allowManagedHooksOnly`](/docs/en/settings-reference#allowmanagedhooksonly) keeps loaded.

When a person starts their own session, Claude Code also downloads the [skills enabled for their claude.ai account](/docs/en/skills#skills-in-cowork-and-cloud-sessions) into that session's config directory. A [routine](/docs/en/routines) run doesn't get its owner's skills, and a session that [sends model requests to Bedrock or Agent Platform](#send-model-requests-to-bedrock-or-agent-platform) doesn't download any. For a skill those sessions need, commit it to the repository's `.claude/skills/` or add it to your runner image.

Outside [Claude Tag](https://claude.com/docs/claude-tag/overview) sessions, a session in a self-hosted environment runs with [auto memory](/docs/en/memory#auto-memory) off by default. For instructions that should carry across sessions, use the `CLAUDE.md` in your runner image or in the repository.

The runner's snapshot of the host's `~/.claude/` leaves out the `projects/` directory. Auto memory's default storage location is under that directory. If you put memory files there, the runner doesn't seed them into sessions, and they don't turn auto memory on.

### Repository settings in sessions with several repositories

In a session with several repositories, Claude Code reads project settings from the directory the session starts in, so at most one repository's `.claude/settings.json` takes effect as project settings. A hook defined in another repository's file doesn't run, a deny rule in it doesn't apply, and its `env` isn't set.

* **`--capacity 1`, the default, with the built-in checkout**: the session starts in the first repository in its list of repositories. That repository's `.claude/settings.json` takes effect as project settings and its `.mcp.json` loads, and the other repositories' don't.
* **A `--capacity` above one, or a [`checkout` hook](#checkout)**: the session starts in a per-session directory that contains the checkouts. No repository's `.claude/settings.json` takes effect as project settings, no repository's `.mcp.json` loads, and [`$CLAUDE_PROJECT_DIR`](/docs/en/hooks#reference-scripts-by-path) in a hook command is that directory, not a checkout.

Each repository's `CLAUDE.md` and skills load wherever the session starts. The runner passes every repository to Claude Code as an [additional directory](/docs/en/permissions#additional-directories-grant-file-access-not-configuration), so Claude Code also reads the `enabledPlugins` and `extraKnownMarketplaces` keys from each repository's `.claude/settings.json`.

To run a hook or apply a permission rule in every session, put it in `~/.claude/settings.json` on the runner host. The runner [seeds the host file into every session](#how-each-session’s-config-is-assembled), wherever the session starts. Write a path in a `Read` or `Edit` rule as a `//` absolute or `~/` home-relative [pattern](/docs/en/permissions#read-and-edit), because other patterns anchor at the settings source or the current directory.

### Repository-committed permission rules

Don't put a bare `"Edit"`, `"Write"`, or `"NotebookEdit"` entry in a repository-committed `permissions.allow`. A bare file-tool rule matches the tool regardless of path, granting writes anywhere on the host rather than only the workspace, so the runner's write-scope confine guard flags the session; with [`--confine-repo-settings enforce`](/docs/en/self-hosted-environments-reference#runner-cli-flags) it refuses to spawn the session instead of logging and continuing. See the [hardening section](/docs/en/self-hosted-environments-deploy#harden-your-deployment).

A repository needs no file-tool rule at all: cloud sessions [pre-approve file edits regardless of mode](/docs/en/permission-modes#switch-permission-modes). If you do commit a rule, scope it to the workspace, such as `"Edit(/**)"`; a single leading slash is relative to the project root, which is the session's workspace. Bare file-tool rules are fine in the operator's host-level `settings.json`, since that file isn't repository-committed.

A `defaultMode` of `auto` is only honored from the image-wide or user-level settings file, so a checked-out repository can't grant itself auto mode. For which modes cloud sessions accept and the full rule syntax, see [permission modes](/docs/en/permission-modes).

## What's next

* [Reference](/docs/en/self-hosted-environments-reference): every CLI flag, environment variable, and metric
* [Verify session identity](/docs/en/self-hosted-environments-identity): validate the session token from services outside the runner
