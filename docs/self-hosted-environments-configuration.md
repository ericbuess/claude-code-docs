> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Customize sessions in self-hosted environments

> Customize self-hosted environment sessions with wrapper scripts for per-session credentials, lifecycle hooks, and on-demand runner spawning.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; an [Owner or admin](/docs/en/cloud-environments#organization-shared-environments) enables them by turning on **Allow self-hosted environments** on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments). This page assumes a working runner; see the [quickstart](/docs/en/self-hosted-environments-quickstart) for setup and [Deploy to production](/docs/en/self-hosted-environments-deploy) for the fleet recipes.
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

| Variable                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN`  | The session JWT, prefixed `sk-ant-cc-`. Its `act` claim identifies the session creator, with the creator's email and upstream identity-provider subject when the creating surface recorded them. The value is the token at spawn time; refreshes arrive over the child's stdin, so a wrapper sees only the initial value. See [Verify session identity](/docs/en/self-hosted-environments-identity).                                                                                                                                                                                                                              |
| `CCR_SESSION_ACCOUNT_EMAIL`         | The session creator's email, pre-extracted by the runner from the token's `act.email` claim without signature verification. Suitable for labelling, such as commit trailers. When the email gates credential issuance, verify the token and read the claim from it instead; see [Provision credentials scoped to the session creator](#provision-credentials-scoped-to-the-session-creator). Unset when the token carries no creator email. Treat as personally identifiable information.                                                                                                                                    |
| `CLAUDE_RUNNER_CLIENT_PLATFORM`     | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, `ios`, `claude_code_cli`, or `scheduled_trigger`. Anthropic records the value once at session creation, so the wrapper and every lifecycle hook see the same value. Use it for adoption analytics and labelling only, not as an authorization signal. Unset when the session has no recorded or recognized surface, so reference it as `${CLAUDE_RUNNER_CLIENT_PLATFORM:-}` under `set -u`. Requires Claude Code v2.1.229 or later.                                                                                                     |
| `CLAUDE_RUNNER_CLAUDE_BIN`          | Absolute path to the runner's own Claude Code binary. End your wrapper with `exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@"` to hand off to the pinned binary without hardcoding an install path.                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `CLAUDE_CODE_REMOTE_SESSION_ID`     | Session ID in the tagged `cse_...` form. This is the same session the [lifecycle hooks](#lifecycle-hooks) see as `CLAUDE_RUNNER_SESSION_ID` in `session_...` form; the UUID variables match across both, and substituting the `cse_` prefix with `session_` yields the ID shown in the session URL.                                                                                                                                                                                                                                                                                                                          |
| `CLAUDE_CODE_REMOTE_SESSION_UUID`   | The same session ID in canonical UUID form, for systems that key on UUIDs.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `CLAUDE_SESSION_INGRESS_TOKEN_FILE` | Absolute path to a per-session file holding the current session JWT, kept fresh across token refreshes. Shell subprocesses read it for their `Authorization` header when downloading attachments the user added to the session. `exec` preserves the variable automatically; a wrapper that rebuilds the child's environment must carry the variable over, or attachment downloads silently stop working.                                                                                                                                                                                                                    |
| `CLAUDE_CONFIG_DIR`                 | Per-session Claude config directory, written at session start from the snapshot of the runner host's config that the runner captures at startup; see [Permissions and tool approval](#permissions-and-tool-approval). Writes here are isolated to this session.                                                                                                                                                                                                                                                                                                                                                              |
| `ANTHROPIC_BASE_URL`                | The API base URL the child will use, delivered by the control plane per session and normally `https://api.anthropic.com`. Don't override it: the session's inference credential is an Anthropic-issued OAuth token that other providers don't accept, so inference in self-hosted environments isn't routable elsewhere.                                                                                                                                                                                                                                                                                                     |
| `CLAUDE_CODE_OAUTH_TOKEN`           | The short-lived OAuth access token the child uses for model inference, scoped to model inference and file upload only, with a lifetime of about 30 minutes. The runner re-mints it before expiry and delivers the rotation over the child's stdin, so a wrapper that doesn't [keep stdin attached](#keep-stdin-and-file-descriptor-3-attached) sees only the initial value. Don't rely on your organization's IP allowlist to bound this token's use: treat it as a bearer credential that stays usable for roughly 30 minutes if it leaks, and don't log it, write it to disk, or forward it outside the session container. |

The wrapper also inherits the rest of the child's managed environment, including any server-provided environment variables. `exec` propagates all of it automatically; if your wrapper spawns the child another way, forward the full environment.

### Keep stdin and file descriptor 3 attached

The child's stdin is the runner's control channel. Token rotations and session-end signals arrive on it. The runner also opens a pipe on file descriptor 3 and reads the child's activity signals from it to drive idle and startup timeouts. A plain `exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@"` preserves both automatically.

If your wrapper backgrounds the child with a bare `&`, it severs the child's stdin: the session looks healthy until the initial OAuth token's roughly 30-minute lifetime expires, then every API call fails with `401 authentication_error`. If your wrapper must background the child, for example to keep a teardown trap alive, save stdin on file descriptor 4 or higher and re-attach it explicitly:

```bash theme={null}
exec 4<&0
"$CLAUDE_RUNNER_CLAUDE_BIN" "$@" <&4 4<&- &
CHILD=$!
trap 'teardown' EXIT
wait "$CHILD"
```

Don't close or reuse file descriptor 3 in the wrapper. Redirecting the child's stdout and stderr is fine.

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

Use `jq -re` rather than `jq -r` when the extracted claim gates an auth decision, so an absent claim exits non-zero instead of passing the literal string `null` downstream. Sessions created by an organization service identity, such as bot and agent sessions, carry an `agent:` subject rather than `user:`, so this example refuses them; if your environment serves those sessions, decide explicitly whether the wrapper falls back to a default credential for them instead of exiting. When your credential exchange needs the SSO subject or email instead, read `.act.attested_by.sub` or `.act.email` and handle their absence: the token carries them only when the creating surface recorded them, and a [CLI-dispatched session](/docs/en/self-hosted-environments-testing#run-the-test-loop) can lack both. For the full claim reference and verification from services outside the runner, see [Verify session identity](/docs/en/self-hosted-environments-identity).

## Lifecycle hooks

Lifecycle hooks replace stages of the runner's per-session pipeline with your own scripts. Point the runner at a directory of hooks with `--hooks-dir <path>`, or `SELF_HOSTED_RUNNER_HOOKS_DIR`. The runner looks for executable files with well-known names; any hook that isn't present falls through to the built-in behavior, so you only write the ones you need. Hooks run with the runner's own privileges, and session children share that UID, so mount the hooks directory read-only, or bake it into the image, so session code can't modify it; see the [hardening section](/docs/en/self-hosted-environments-deploy#harden-your-deployment).

These hooks are distinct from [Claude Code hooks](/docs/en/hooks), which run inside the session; lifecycle hooks run on the runner, around the session.

### checkout

Runs once per repository, in place of the runner's built-in clone and fetch. Use the hook to clone from a read-through mirror, seed a working tree from an archive, or apply per-session git auth. The runner sets:

| Variable                           | Description                                                                                                                                                  |
| :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_RUNNER_REPO_URL`           | Repository URL to clone, after any `--git-host-rewrite` and `--git-ssh-rewrite` have been applied                                                            |
| `CLAUDE_RUNNER_REPO_REF`           | Revision to check out: branch, tag, or commit SHA as the session requested it. Empty means the repository's default branch.                                  |
| `CLAUDE_RUNNER_CHECKOUT_PATH`      | Absolute path where the working tree must be left                                                                                                            |
| `CLAUDE_RUNNER_SESSION_ID`         | Session ID in the tagged `session_...` form, for logging and correlation                                                                                     |
| `CLAUDE_RUNNER_SESSION_UUID`       | The same session ID in canonical UUID form                                                                                                                   |
| `CLAUDE_RUNNER_API_BASE_URL`       | Anthropic API base URL for session-scoped calls                                                                                                              |
| `CLAUDE_RUNNER_CLIENT_PLATFORM`    | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, or `ios`. Unset when the session has no recorded or recognized surface. |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | The session access token, for session-scoped API calls                                                                                                       |

The script must leave a working tree at `CLAUDE_RUNNER_CHECKOUT_PATH` checked out at the requested revision. Detached HEAD is fine; the runner creates the session's working branch on top. The runner verifies the path contains a `.git` afterwards; if your hook materializes a non-git source such as Perforce or an unpacked tarball, set `CLAUDE_RUNNER_SKIP_GIT_VERIFY=1` in the runner's environment to skip that check. Git-based flows such as working-branch creation and pushing results require a git checkout, so export outcomes from non-git trees with a [`post-session` hook](#post-session).

The runner doesn't pass a git credential to the hook. Instead, mint a per-session clone credential from the session's identity: verify `CLAUDE_CODE_SESSION_ACCESS_TOKEN` with a standard JWT library against the JWKS endpoint under `CLAUDE_RUNNER_API_BASE_URL`, as described in [Verify the token from your service](/docs/en/self-hosted-environments-identity#verify-the-token-from-your-service), then have your credential service issue a short-lived clone credential for the identity in the token's `act` claim. `CLAUDE_RUNNER_CLAUDE_BIN` isn't set in the checkout-hook environment, so the `decode-token` subcommand isn't available here. Falling back to whatever git authentication the host already has, such as an SSH agent, credential helper, or `.netrc`, is also an option.

When the hook exits non-zero, or exits 0 without leaving a usable checkout behind, what the runner does depends on the repository:

* **A repository the session pushes results to**: the runner fails the session, and on a non-zero exit surfaces the tail of the script's stderr to the user.
* **A repository the session only reads from**, such as a repository added to a running session: the runner logs a `[runner:warn]` line with the failure detail, posts a `Skipped` step to the session, removes whatever the hook left at the checkout path, and continues with the remaining repositories. When the runner can't remove the path immediately, it retries the removal at session end. If skipping leaves the session with no repository at all, the runner fails the session anyway.

Before v2.1.228, the runner failed the session on a hook failure for any repository, so a read-only repository the hook couldn't serve failed the session again on every fresh runner the session resumed on.

The runner removes the checkout path after the session ends.

### post-session

Runs once per session, after the Claude Code child has exited and before the runner tears the workspace down. This hook is your only chance to save uncommitted work: at `--capacity` above one, the runner deletes per-session worktrees right after the hook returns, and at `--capacity 1` the reused [canonical clone](/docs/en/self-hosted-environments-deploy#reuse-a-pre-warmed-checkout) is hard-reset when the next session starts, so uncommitted tracked changes don't survive on either path. Typical uses are pushing a snapshot branch of uncommitted changes, archiving logs, or emitting a session-ended event to your own systems.

The hook fires on every session end where a child process was spawned, whatever the cause; the `CLAUDE_RUNNER_EXIT_REASON` values below enumerate the cases. It can't fire when the runner terminates abruptly, such as a VM preemption or a power loss; if you need guarantees against abrupt termination, snapshot periodically from inside the session with a Claude Code `PostToolUse` hook instead. The runner sets:

| Variable                           | Description                                                                                                                                                  |
| :--------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_RUNNER_SESSION_ID`         | Session ID in the tagged `session_...` form                                                                                                                  |
| `CLAUDE_RUNNER_SESSION_UUID`       | The same session ID in canonical UUID form                                                                                                                   |
| `CLAUDE_RUNNER_EXIT_REASON`        | How the session ended; see the values below the table                                                                                                        |
| `CLAUDE_RUNNER_WORKSPACE_PATHS`    | Colon-separated absolute paths of the session's working trees. Empty for zero-repo sessions.                                                                 |
| `CLAUDE_RUNNER_DEBUG_LOG_PATH`     | Path to the session's debug log, still on disk while the hook runs                                                                                           |
| `CLAUDE_RUNNER_API_BASE_URL`       | Anthropic API base URL for session-scoped calls                                                                                                              |
| `CLAUDE_RUNNER_CLIENT_PLATFORM`    | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, or `ios`. Unset when the session has no recorded or recognized surface. |
| `CLAUDE_CODE_SESSION_ACCESS_TOKEN` | The session access token, for session-scoped API calls                                                                                                       |

`CLAUDE_RUNNER_EXIT_REASON` takes one of four values:

* `completed`: a clean exit, including a session archived or deleted while the child was still connected.
* `failed`: a child crash or a setup failure after spawn.
* `interrupted`: an idle release, startup timeout, server deassign, drain, watchdog kill, or the [`released=false` backstop](/docs/en/self-hosted-environments-reference#session-lifecycle-counter-semantics).
* `abandoned`: reserved for sessions another runner claimed; the hook doesn't currently fire in that case.

The [session lifecycle counter semantics](/docs/en/self-hosted-environments-reference#session-lifecycle-counter-semantics) classify an idle release, a startup timeout, and a server deassign as `completed` instead: those are clean handoffs from the session's perspective even though this hook reports them as `interrupted`.

The hook's exit status never affects the session outcome; a failure is logged and ignored. The runner waits up to `--post-session-hook-timeout-sec`, 60 seconds by default, on every session end including runner shutdown. This example saves uncommitted work to a rescue branch:

```bash theme={null}
#!/usr/bin/env bash
set -u
IFS=':'
# Pin config the session could have planted in the checkout's .git/config:
# -c overrides beat repo-local settings, blocking session-written fsmonitor,
# hook-path, and gpg-program config from executing code with the hook's
# privileges. Repo-local credential.helper, core.sshCommand, and pushurl
# still apply; if the hook holds credentials the session didn't, pin the
# push URL and helper too (see the note below the script).
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

The hook pushes with whatever git credentials are available in its own environment on the runner host. Under the [no-credentials-in-the-image posture](/docs/en/self-hosted-environments-deploy#configure-git), including when the built-in clone goes through the Anthropic git proxy, there are none, so mint a short-lived push credential inside the hook before pushing: exchange the session token the hook receives in `CLAUDE_CODE_SESSION_ACCESS_TOKEN` with your own token service, verifying it as [Verify session identity](/docs/en/self-hosted-environments-identity) describes. When the hook holds a credential the session didn't, also pin where it pushes: replace `origin` with an operator-supplied URL and pass `-c credential.helper=` plus your own helper, so repo-local config the session wrote can't redirect the credentialed push.

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

| Variable                              | Description                                                                                                                                                                                                                                                                                                                           |
| :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CLAUDE_RUNNER_WORK_ORDER_FILE`       | Path to a temp file containing the signed work-order JWT the new runner registers with. Deleted after the hook exits. Don't log the file's contents.                                                                                                                                                                                  |
| `CLAUDE_RUNNER_ORDER_ID`              | Opaque idempotency key, unique per spawn request and safe for Kubernetes resource names. Use it as your provisioner's dedup key.                                                                                                                                                                                                      |
| `CLAUDE_RUNNER_SESSION_ID`            | The session this request is for. Empty for pre-warming requests, which boot a standby runner ahead of any specific session when [`--min-idle`](/docs/en/self-hosted-environments-reference#orchestrator-cli-flags) is set, so don't assume the variable is set.                                                                            |
| `CLAUDE_RUNNER_SESSION_UUID`          | The same session ID in canonical UUID form. Empty for pre-warming requests.                                                                                                                                                                                                                                                           |
| `CLAUDE_RUNNER_ATTEMPT`               | How many spawn requests this session has had. `0` for pre-warming requests.                                                                                                                                                                                                                                                           |
| `CLAUDE_RUNNER_ORDER_SERVER_TIME`     | Server time from the poll response's HTTP `Date` header. When the hook verifies the work-order JWT's `exp`, compare against this value instead of the local clock to tolerate skew. Empty when the gateway omitted the header.                                                                                                        |
| `CLAUDE_RUNNER_POOL_ID`               | The ID of the environment the new runner should join, in `ccpool_...` form                                                                                                                                                                                                                                                            |
| `CLAUDE_RUNNER_ACCOUNT_ID`            | Tagged ID of the account that enqueued the session, for per-account routing, quota, or chargeback. Empty when unavailable.                                                                                                                                                                                                            |
| `CLAUDE_RUNNER_ACCOUNT_EMAIL`         | Email of the account that enqueued the session. Empty when unavailable. Treat the email as personally identifiable information and don't log it.                                                                                                                                                                                      |
| `CLAUDE_RUNNER_PRIMARY_REPO_URL`      | URL of the session's first git source, for routing to a runner with that repository pre-warmed. Empty when the session has no git sources.                                                                                                                                                                                            |
| `CLAUDE_RUNNER_PRIMARY_REPO_REVISION` | Revision of the session's first git source: branch, SHA, or tag. Empty when unspecified.                                                                                                                                                                                                                                              |
| `CLAUDE_RUNNER_REPO_SOURCES`          | JSON array of `{url, revision}` for all the session's git sources, for hooks that route on a secondary repository. Empty when there are no sources.                                                                                                                                                                                   |
| `CLAUDE_RUNNER_CORRELATION_ID`        | The correlation ID supplied at session create, echoed back so the hook can map this work order to the request that created the session. Empty when the session has none.                                                                                                                                                              |
| `CLAUDE_RUNNER_CLIENT_PLATFORM`       | The client surface that created the session, such as `web_claude_ai`, `desktop_app`, `ios`, or `scheduled_trigger`, for adoption analytics. Unset when the session has no recorded or recognized surface, and for pre-warming requests; check it with `[ -n "${CLAUDE_RUNNER_CLIENT_PLATFORM:-}" ]`, which stays safe under `set -u`. |

The spawned runner registers with the work order in place of the environment secret:

* **Start it with the work order**: point [`--environment-secret-file`](/docs/en/self-hosted-environments-reference#runner-cli-flags) at a file containing the work-order JWT, or set `SELF_HOSTED_RUNNER_ENVIRONMENT_SECRET` to the JWT value.
* **Copy the JWT before the hook exits**: the orchestrator deletes the work-order file after the hook exits, so copy the JWT into the workload you submit, such as a Kubernetes Secret on the spawned Job, rather than passing the file path through.
* **Use `--capacity 1` on spawned runners**: a session-bound work order registers exactly one runner bound to that session, so a higher capacity adds slots that never receive work, and the runner logs a warning at startup.
* **Pre-warming work orders register unbound**: the standby runner isn't bound to a session and claims queued work like a fixed-fleet runner.

The contract has four provisioner-agnostic rules:

1. **Be idempotent on `CLAUDE_RUNNER_ORDER_ID`.** Redelivery of the same request must spawn at most one runner. Derive a deterministic resource name from the ID and let your platform reject the duplicate.
2. **Don't retry the workload.** One order ID means at most one created workload. If the runner never registers, Anthropic re-requests with a fresh order ID after `--expected-spawn-seconds`.
3. **Use the exit-code contract.** Exit 0 means submitted. Exit 1 means retryable failure; the session backs off and is re-offered. Exit 2 or higher means non-retryable; the session is blocked from spawning again until an [Owner or admin](/docs/en/cloud-environments#organization-shared-environments) selects **Retry** on it in the environment's **Activity** tab. On non-zero exit, the tail of the hook's stderr appears there as the failure reason, so write the actionable error to stderr and never secrets. For a pre-warming request there is no session to fail: the orchestrator logs a non-zero exit locally only, and the server re-requests the spawn after the lease.
4. **Set `--expected-spawn-seconds` to at least your p99 boot time.** This is the server-side lease. All orchestrator replicas must use the same value.

Everything the hook writes to stdout or stderr appears in the orchestrator's log with credentials automatically redacted. If sessions stay queued, check the orchestrator's `/healthz` body for queue counts, then open your environment's **Activity** tab on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments): expand a failed session there for its spawn error, and select **Retry** to re-request it.

## MCP servers

To make [MCP servers](/docs/en/mcp) available in every session, add them at image build time with the same `claude mcp add` command used on a desktop install. If your runner is a bare process rather than a container, run the same command as the runner's user on the host, then restart the runner: it reads host config once at startup. The `--scope user` flag is required; the default local scope writes under a per-directory key that the runner doesn't seed into sessions. For example, in your Dockerfile:

```dockerfile theme={null}
RUN claude mcp add --scope user sidecar -- /usr/local/bin/mcp-sidecar
RUN claude mcp add --scope user --transport http internal http://mcp-gateway.svc.cluster.local:8080
```

The runner snapshots the host's config once at startup. The snapshot captures the `mcpServers` key from the host's `.claude.json`, which lives next to rather than inside `~/.claude/`, and the runner seeds only that key into each session's isolated config; account state and project history are dropped. To confirm the servers reached sessions, start a session on the environment and ask Claude to list its MCP tools; the runner also logs a startup warning for any captured entry whose `type` it doesn't recognize and drops the entry, so you can see why that server is missing from sessions. When `SELF_HOSTED_RUNNER_HOST_CONFIG_DIR` is set, the runner reads `.claude.json` from that directory instead, so pointing the variable at an empty directory disables MCP seeding too.

Two other sources work as well:

* The enterprise-scope [managed MCP file](/docs/en/managed-mcp) at its standard system path: `/etc/claude-code/managed-mcp.json` on Linux runner hosts, `/Library/Application Support/ClaudeCode/managed-mcp.json` on macOS hosts. Use it for locked-down fleets where only administrator-listed servers may load. See [exclusive control with managed-mcp.json](/docs/en/managed-mcp#exclusive-control-with-managed-mcp-json) for the precedence rules. When this file is on the runner host, Claude Code skips the MCP servers Anthropic's control plane delivers to a session, including claude.ai connectors, and names them in a warning on the session child's stderr, which the runner records at the `debug` log level. Before v2.1.229, those sessions exited at startup with `You cannot dynamically configure MCP servers when an enterprise MCP config is present`.
* `<repo>/.mcp.json`: project scope. Commit the file to the repository; its servers are auto-approved in cloud sessions.

When connector delivery is enabled for your organization, Anthropic's control plane delivers the connectors you've configured on claude.ai to interactively-created sessions through server-provided MCP configuration, routed through `api.anthropic.com`. Sessions created programmatically, such as [CLI dispatches](/docs/en/self-hosted-environments-testing#run-the-test-loop), don't receive connector delivery; give them MCP servers through the host snapshot, the [managed MCP file](/docs/en/managed-mcp), or `<repo>/.mcp.json` instead. The child's OAuth token doesn't carry a scope for fetching connectors directly, so the child doesn't attempt that fetch itself; delivery is server-driven.

`settings.json` and `managed-settings.json` don't carry MCP server definitions; there is no top-level `mcpServers` field in the settings schema.

Sessions inherit the runner's environment, so set [`ENABLE_TOOL_SEARCH`](/docs/en/mcp#scale-with-mcp-tool-search) there to control MCP tool search for every session a runner spawns; the MCP page covers the values.

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
#     branch, which the runner creates with checkout -B after checkout
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

The hook prompts Claude to commit and push before the session ends, and stays silent when the directory isn't a git repository or has no remote.

## Permissions and tool approval

A self-hosted session has no terminal attached, so an unanswered permission prompt stalls the turn until the user responds in the UI. Anthropic's control plane sends each session's tool list and permission rules with the work payload; the default configuration pre-approves routine tool calls, including `Bash`, and cloud sessions [pre-approve file edits regardless of mode](/docs/en/permission-modes#switch-permission-modes). A call that nothing pre-approves prompts through the session UI.

<Note>
  Only enable auto mode on an environment whose session containers run with [default-deny network egress](/docs/en/self-hosted-environments-deploy#default-deny-egress) and the rest of the [hardening section](/docs/en/self-hosted-environments-deploy#harden-your-deployment) in place. Routine tool calls, including `Bash` network requests, run without a human in the loop on both the default pre-approved tool set and in auto mode, so the network boundary is what limits where those calls can reach.
</Note>

To keep prompts to a minimum regardless of what the control plane sends, pin [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) from your wrapper script or [`command` hook](#command). Auto mode lets sessions run without routine permission prompts: a separate classifier model reviews actions before they run and blocks the ones it rejects, and explicit ask rules still force a prompt; the permission modes page covers what the classifier checks. The runner appends server-computed flags before invoking the wrapper, and for single-value flags such as `--permission-mode` the parser honors the last occurrence, so a flag you append after `"$@"` overrides the server-sent value:

```bash theme={null}
#!/bin/bash
exec "$CLAUDE_RUNNER_CLAUDE_BIN" "$@" --permission-mode auto
```

To pre-approve specific tools instead, append `--allowed-tools` with your rules, for example `--allowed-tools "Bash(bazel *) Bash(yarn *) mcp__internal__*"`. List flags such as `--allowed-tools` and `--disallowed-tools` accumulate across occurrences rather than overriding, so your rules apply on top of any rules the control plane sends. To narrow, append `--disallowed-tools`, which denies tools even if another rule allows them.

### How each session's config is assembled

The runner gives each session its own config directory, seeded from an in-memory snapshot of the host's `~/.claude/` that the runner captures once at startup: `settings.json`, `CLAUDE.md`, hooks, agents, commands, and skills in your runner image apply to every session as the user-level baseline. Because the snapshot is taken at startup, config changes on a running host take effect only after a runner restart. Set `SELF_HOSTED_RUNNER_HOST_CONFIG_DIR` to seed from a different path, or point it at an empty directory to disable seeding.

Repository-committed `.claude/settings.json` layers on top as project settings. Sessions also read [`managed-settings.json`](/docs/en/settings#settings-files) from the standard system path in your runner image, but the managed tier uses one source at a time, and [server-managed settings](/docs/en/server-managed-settings) are checked first: if your organization delivers any server-managed keys, sessions ignore the runner image's managed file, except that `env` blocks merge per key across managed sources. See [settings precedence](/docs/en/settings#settings-precedence).

When Anthropic's control plane supplies a session with [Claude Code hooks](/docs/en/hooks), the runner installs them alongside, not over, your own configuration. Requires Claude Code v2.1.229 or later.

* **Where they land**: the runner writes each supplied hook script to a reserved `hooks/.ccr-launcher/` subdirectory of the session's config directory and registers the scripts in a separate settings file it passes to the session with `--settings`, leaving the seeded `settings.json` and your own scripts at `hooks/<name>` untouched. The runner recreates the reserved subdirectory for each session and doesn't seed host content at `~/.claude/hooks/.ccr-launcher/` into sessions.
* **Who authors them**: the control plane populates the scripts from fixed constants in its own deployment, never from per-session or third-party input.
* **What still governs them**: hooks delivered through `--settings` enter the ordinary merged hook configuration, not the managed tier, so your managed settings still apply. `disableAllHooks` disables them, and they are not among the categories [`allowManagedHooksOnly`](/docs/en/settings#hook-configuration) keeps loaded.

### Repository-committed permission rules

Don't put a bare `"Edit"`, `"Write"`, or `"NotebookEdit"` entry in a repository-committed `permissions.allow`. A bare file-tool rule matches the tool regardless of path, granting writes anywhere on the host rather than only the workspace, so the runner's write-scope confine guard flags the session; with [`--confine-repo-settings enforce`](/docs/en/self-hosted-environments-reference#runner-cli-flags) it refuses to spawn the session instead of logging and continuing. See the [hardening section](/docs/en/self-hosted-environments-deploy#harden-your-deployment).

A repository needs no file-tool rule at all: cloud sessions [pre-approve file edits regardless of mode](/docs/en/permission-modes#switch-permission-modes). If you do commit a rule, scope it to the workspace, such as `"Edit(/**)"`; a single leading slash is relative to the project root, which is the session's workspace. Bare file-tool rules are fine in the operator's host-level `settings.json`, since that file isn't repository-committed.

A `defaultMode` of `auto` is only honored from the image-wide or user-level settings file, so a checked-out repository can't grant itself auto mode. For which modes cloud sessions accept and the full rule syntax, see [permission modes](/docs/en/permission-modes).

## What's next

* [Reference](/docs/en/self-hosted-environments-reference): every CLI flag, environment variable, and metric
* [Verify session identity](/docs/en/self-hosted-environments-identity): validate the session token from services outside the runner
