> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploy self-hosted environments to production

> Run self-hosted runners in production: security hardening, network egress control, git credentials, Kubernetes and Compose recipes, and troubleshooting.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; [Availability and limitations](/docs/en/self-hosted-environments#availability-and-limitations) covers the enablement path. This page covers running the fleet in production; see the [quickstart](/docs/en/self-hosted-environments-quickstart) for your first runner and session.
</Note>

A [self-hosted environment](/docs/en/self-hosted-environments) runs Claude Code [cloud sessions](/docs/en/claude-code-on-the-web) on runners you deploy inside your network, and in production those sessions execute model-directed code on behalf of anyone in your organization. This page is for the operator taking a working environment to production. It works through the deployment in order: what to lock down before connecting real systems, the egress the fleet needs, how sessions authenticate to your git host, the deployment recipes themselves, and what to check when sessions misbehave.

## Harden your deployment

A self-hosted runner executes arbitrary, model-directed code on your infrastructure on behalf of any member of your Anthropic organization. Work through each item before you connect an environment to production systems:

* **Ephemeral, per-session containers**: run each runner process in a fresh container or VM that's destroyed when the process exits, with `--capacity 1` and the default `--drain-grace-sec 0` so each container serves exactly one session. At a higher capacity, or with a positive drain grace, one container serves multiple sessions from the same locked account instead of one session each; see [Runner lifecycle](/docs/en/self-hosted-environments#runner-lifecycle). Don't reuse a filesystem between runner restarts, except in the deliberate [pre-warmed checkout](#reuse-a-pre-warmed-checkout) setup, and never across accounts.
* **No broad credentials in the image**: don't include long-lived SSH keys, cloud-provider credentials, or personal access tokens that grant more than a session needs. Mint credentials used during a session, such as push or API tokens, per session from your [wrapper script](/docs/en/self-hosted-environments-configuration#wrapper-scripts). For the initial clone, which happens before the wrapper runs, use a [`checkout` lifecycle hook](/docs/en/self-hosted-environments-configuration#checkout) or [`--use-anthropic-git-proxy`](#use-the-anthropic-git-proxy); see [Configure git](#configure-git).
* **Keep the environment secret off session-running hosts**: the environment secret can register runners and pick up any org member's queued sessions. On a fixed fleet it lives on every runner host, where any session's code can read the secret file. Prefer [on-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners), where the secret stays on the orchestrator host, which never runs user code, and each runner receives a single-use work order that registers exactly one runner. On a fixed fleet, treat the environment-secret file as readable by every session and rotate the secret after any suspected session compromise.
* **Default-deny network egress**: restrict runner and session container outbound traffic at your own network boundary on every environment; [Default-deny egress](#default-deny-egress) covers what to allow and why.
* **Least-privilege host IAM**: the compute identity attached to the runner host, such as an instance profile or node service account, should grant only what the runner itself needs. Sessions should obtain their own credentials through your wrapper script rather than inheriting the host's.
* **Block the cloud metadata endpoint from sessions**: keeping sessions off the host identity requires blocking their access to the cloud metadata endpoint, and subnet-level egress policies don't intercept link-local metadata traffic, so block it in the container itself:

  * IMDSv2 with a hop limit of one
  * GKE Workload Identity with metadata concealment
  * An explicit deny for `169.254.169.254` in the session container's network namespace

  The block applies to your wrapper script and lifecycle hooks too, since they share the container. Authenticate any token exchange with the [session JWT](/docs/en/self-hosted-environments-identity) against your own token service over allowlisted egress, or use a file-based web identity such as IAM Roles for Service Accounts (IRSA) on Amazon EKS.
* **Per-runner filesystem isolation**: each runner process gets its own working directory that no other process on the host can read or write. Make `--hooks-dir`, the wrapper script, and the host's `~/.claude/` read-only to the session, either built into the image or mounted read-only.
* **Dispatch is organization-wide**: any member of your Anthropic organization can dispatch a session to any of its environments, and there's no per-environment access control on dispatch. Treat every runner host as reachable for code execution by every org member, and don't place data or credentials on a runner host that any org member shouldn't be able to read. [`--lock-to-account`](/docs/en/self-hosted-environments-reference#runner-cli-flags) bounds which account's sessions a given host executes, but dispatch into the environment itself stays organization-wide. To make self-hosted environments the only picker option, an [Owner or admin](/docs/en/cloud-environments#organization-shared-environments) can hide Anthropic-hosted environments for the whole organization from the [**Cloud environments** page](https://claude.ai/admin-settings/cloud-environments).
* **Enforce the repo-settings guard**: choose the guard mode with [`--confine-repo-settings`](/docs/en/self-hosted-environments-reference#runner-cli-flags). The default `warn` logs a violation and still spawns the session, `enforce` refuses the session, and `off` disables the scan. The runner scans each repository's committed settings for:

  * A grant that resolves outside that session's own workspace: an `additionalDirectories` entry, an `Edit`, `Write`, or `NotebookEdit` rule in `permissions.allow`, or a `sandbox.filesystem.allowWrite` or `allowRead` entry
  * A non-empty `env` block
  * An operator-posture override such as `sandbox.enabled: false`

  The guard runs regardless of [`--trust-workspace`](/docs/en/self-hosted-environments-reference#runner-cli-flags), and doesn't cover repository hooks, `.mcp.json`, or Bash rules; see [Permissions and tool approval](/docs/en/self-hosted-environments-configuration#permissions-and-tool-approval) for where those grants belong.

<Note>
  Your organization's IP allowlist doesn't cover self-hosted runner traffic by default. Don't rely on it as a network control for runner or session traffic; apply default-deny egress at your own network boundary instead, and contact your Anthropic account team if you want IP-allowlist enforcement for your organization.
</Note>

## Network requirements

The runner and the session children it spawns make outbound connections to the hosts below. Restrict session-container egress to these hosts and the specific internal services sessions need to reach; [Default-deny egress](#default-deny-egress) covers how and why.

These hosts are always required:

| Host                                                               | Port                                       | Used for                                                                                                                                                                                                                                                                                                                                                                      |
| :----------------------------------------------------------------- | :----------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`                                                | 443, HTTPS; WSS for the SCM connector only | Runner control plane and session streaming, model inference, feature flags, product analytics, [JWKS](/docs/en/self-hosted-environments-identity) key fetches, commit signing, the git proxy when `--use-anthropic-git-proxy` is set, and the orchestrator's [SCM connector](/docs/en/self-hosted-environments-reference#scm-connector-flags) tunnel when `--scm-connector-host` is set |
| Your git host, such as `github.com` or your GitHub Enterprise host | 443 or 22                                  | Cloning and pushing repositories. Not needed if the runner uses `--use-anthropic-git-proxy`, which routes git traffic through `api.anthropic.com`.                                                                                                                                                                                                                            |

Whether these hosts are needed depends on your configuration:

| Host                                 | Port | When required                                                                                                                                                                                                                                                                           |
| :----------------------------------- | :--- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `downloads.claude.ai`                | 443  | At install time, when you install or update Claude Code on the host with the native installer; the `install.sh` script itself is served from `claude.ai`. At session runtime, only when sessions install plugins from the official Anthropic marketplace.                               |
| `storage.googleapis.com`             | 443  | At session runtime, for marketplace plugin catalog fetches and Artifact publishing when the Artifact tool is enabled; Artifact publishing falls back to `api.anthropic.com` when this host is blocked.                                                                                  |
| `code.claude.com` and `claude.com`   | 443  | Documentation lookups by the built-in claude-code-guide agent and pre-approved WebFetch requests during sessions. Blocking these hosts only affects documentation lookups.                                                                                                              |
| `*.frame.claudeusercontent.com`      | 443  | Only when the [Artifact tool](/docs/en/artifacts#availability) is available for sessions in your organization; defaults vary by plan, per the availability table there. Set `CLAUDE_CODE_DISABLE_ARTIFACT=1` on the runner to keep the tool disabled regardless of the organization setting. |
| `raw.githubusercontent.com`          | 443  | Only for the changelog fetch behind `/release-notes` and the release notes shown after a CLI version change. Suppressed by `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`.                                                                                                                |
| `registry.npmjs.org`                 | 443  | When a session installs a plugin, both for fetching npm-source plugin packages and for installing a plugin's Node.js dependencies, or when an `npx`-launched MCP server runs                                                                                                            |
| `http-intake.logs.us5.datadoghq.com` | 443  | Anthropic operational metrics. Only when `CLAUDE_CODE_BYOC_ENABLE_DATADOG=1` is set; off by default in self-hosted environments.                                                                                                                                                        |
| `browser-intake-us5-datadoghq.com`   | 443  | Anthropic error-report uploads, sent only when [error reporting](/docs/en/data-usage#telemetry-services) is enabled for the session's account. Suppressed by `DISABLE_ERROR_REPORTING=1` or `DISABLE_TELEMETRY=1`.                                                                           |

The runner doesn't reach `statsig.anthropic.com`, `*.sentry.io`, `claude.ai`, or `platform.claude.com`. These hosts appear in some older enterprise network checklists, but you don't need to allowlist them for runner or session traffic: feature-flag fetches go to `api.anthropic.com`, and the runner authenticates with the environment secret rather than interactive OAuth. Two host-side flows do reach `claude.ai`, so run them from a host whose egress allows it rather than widening session-container egress: the one-line installer fetches `install.sh` from `claude.ai` at install time, and interactive `claude auth login`, which the [guided setup](/docs/en/self-hosted-environments-quickstart#set-up-an-environment-and-runner), `doctor`'s signed-in mode, and [CI dispatch](/docs/en/self-hosted-environments-testing#authenticate-from-ci) use, signs in through `claude.ai`, `claude.com`, and `platform.claude.com`. `mcp-proxy.anthropic.com` isn't required either: self-hosted sessions don't use it, and delivery of your organization's claude.ai connectors to sessions, when enabled for your organization, routes through `api.anthropic.com`. See [MCP servers](/docs/en/self-hosted-environments-configuration#mcp-servers).

### Default-deny egress

Deploy runner and session containers in a network segment or namespace whose outbound traffic is limited to the hosts in the [network requirements table](#network-requirements), your git host, and the specific internal services sessions need to reach. The product can't verify or enforce this, so apply it at your own network boundary on every environment. Session code is model-directed and can attempt connections to arbitrary hosts; default-deny egress at the network layer bounds where those attempts can land. This applies regardless of permission mode: the default pre-approved tool set already includes `Bash`, so shell egress runs without a prompt even without [auto mode](/docs/en/self-hosted-environments-configuration#permissions-and-tool-approval).

For details on which telemetry each session emits and how to turn it off, see [Telemetry](/docs/en/self-hosted-environments-reference#telemetry).

## Configure git

The runner manages repository checkouts but doesn't configure git identity or credentials by default. You control the runner's image and process environment, so you control the git config. Choose one of two approaches:

* **Let the runner configure git**: start the runner with `--configure-git` to have it write the same identity and commit-signing config that Anthropic-hosted sessions use
* **Ship git config in your image**: set identity and push credentials yourself, for example to commit under your own bot identity

Git version floors on the runner host: [`--configure-git`](#let-the-runner-configure-git) SSH commit signing requires Git 2.34 or newer, [`--use-anthropic-git-proxy`](#use-the-anthropic-git-proxy) requires 2.32 or newer, and resuming sessions from branches pushed by [`--push-outcome-on-release`](/docs/en/self-hosted-environments-reference#runner-cli-flags) requires 2.29 or newer. Git 2.24 is sufficient if you omit all three and manage git identity yourself.

### Let the runner configure git

Start the runner with `--configure-git`, or set `SELF_HOSTED_RUNNER_CONFIGURE_GIT=1`, to have it write global git config at startup:

* `user.name = Claude` and `user.email = noreply@anthropic.com`, matching Anthropic-hosted sessions
* SSH-format commit and tag signing, routed through a runner-managed shim that signs each commit via Anthropic's signing service using the session's own credentials. Signatures are verifiable on GitHub against Anthropic's published SSH signing key.

Commit signing requires git 2.34 or newer; the runner checks at startup and exits with an error if your git is older. This flag doesn't configure push credentials, which you still provide in the image.

### Ship git config in your image

Git identity is required for any commit. Set it system-wide in your Dockerfile so the config applies regardless of which user the runner process runs as:

```dockerfile theme={null}
RUN git config --system user.name "Claude" && \
    git config --system user.email "noreply@anthropic.com"
```

Without an identity, `git commit` fails with `Please tell me who you are` and sessions can't make progress. You can use your own bot identity instead; the runner doesn't override these values.

Don't bake long-lived or broadly-scoped push credentials into a shared runner image: a credential in the image is available to every session the image runs, across every member of your organization. Instead, mint a short-lived, least-scoped token per session from your [wrapper script](/docs/en/self-hosted-environments-configuration#wrapper-scripts), using the session creator's identity decoded from the session JWT. Pair it with an ephemeral per-session container, which requires `--capacity 1`, so no credential outlives the session that minted it; see the [hardening section](#harden-your-deployment).

If you must configure push credentials at the image level, for example for a read-only deploy key, scope them as tightly as your git host allows:

* An SSH deploy key limited to one repository with a `url.<base>.insteadOf` rewrite
* A `credential.helper` that returns a minimally-scoped token
* `GIT_SSH_COMMAND` pointing at a narrowly-scoped key

If checkout directories are owned by a different uid than the runner process, git refuses to operate on them; add `safe.directory`:

```dockerfile theme={null}
RUN git config --system --add safe.directory '*'
```

### Use the Anthropic git proxy

Start the runner with `--use-anthropic-git-proxy`, or set `CLAUDE_RUNNER_USE_GIT_PROXY=1`, to have it clone through Anthropic's git proxy, authenticated with the session's own short-lived token. For ordinary user sessions, the proxy uses the GitHub or GitHub Enterprise OAuth token stored for the session creator; for bot and agent sessions, it uses your organization's GitHub App installation token. Either way, the runner image needs no git credentials at all: no SSH keys, no credential helper, no `.netrc`. This is the same auth path Anthropic-hosted environments use.

The proxy requires `--capacity 1` because the proxy URL is per-session, and git 2.32 or newer because older git ignores the configuration mechanism the proxy uses to isolate sessions from each other. The runner refuses to start if either requirement is unmet. Because the proxy fetches from Anthropic's side, your git host must be reachable from Anthropic infrastructure, the same requirement Anthropic-hosted sessions have; for a git host that's only routable inside your network, use a [`checkout` lifecycle hook](/docs/en/self-hosted-environments-configuration#checkout) instead. Each runner process handles one session at a time, so run more replicas for parallelism. When the proxy is enabled, `--git-host-rewrite` and `--git-ssh-rewrite` have no effect: the proxy URL points at `api.anthropic.com`, not your git host.

### Rewrite git URLs for private networks

Repository URLs arrive from the control plane as HTTPS, with the hostname of your git host; for GitHub Enterprise, that's the hostname you configured for the [GitHub Enterprise integration](/docs/en/github-enterprise-server) in Claude Code admin settings on claude.ai. Two repeatable flags rewrite those URLs before clone:

* `--git-host-rewrite <from>=<to>`: for split-horizon DNS, where Anthropic reaches your git host via an external hostname but runners must use an internal one
* `--git-ssh-rewrite <host>`: for git hosts that only accept SSH, rewriting `https://<host>/owner/repo` to `git@<host>:owner/repo`

Host rewriting runs first, so list the internal hostname in `--git-ssh-rewrite` if you need both. For full control over checkout, use a [`checkout` lifecycle hook](/docs/en/self-hosted-environments-configuration#checkout).

## Build the runner image

Anthropic doesn't publish a pre-built runner image. Build your own around the `claude` binary, layering in whatever toolchain your repositories need: language runtimes, compilers, package managers, and [MCP](/docs/en/mcp) sidecars.

The recipes below use `--capacity 4`, so one container serves up to four concurrent sessions from the same locked account. That doesn't provide the per-session container isolation in the [hardening section](#harden-your-deployment): before connecting an environment to production systems, either run the recipes at `--capacity 1` with one container per session, or use [on-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners), which also keep the environment secret off session-running hosts.

This Dockerfile is a minimal starting point:

```dockerfile theme={null}
FROM debian:bookworm-slim
ARG CLAUDE_CODE_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends git curl ca-certificates openssh-client \
 && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL "https://downloads.claude.ai/claude-code-releases/${CLAUDE_CODE_VERSION:?set with --build-arg CLAUDE_CODE_VERSION}/linux-x64/claude" \
      -o /usr/local/bin/claude && chmod +x /usr/local/bin/claude
RUN git config --system user.name "Claude" \
 && git config --system user.email "noreply@anthropic.com" \
 && git config --system --add safe.directory '*'
ENTRYPOINT ["claude"]
```

Swap `linux-x64` for `linux-arm64` if your nodes are ARM, or for `linux-x64-musl` or `linux-arm64-musl` on a musl-based image such as Alpine; see [Alpine Linux setup](/docs/en/setup#alpine-linux-and-musl-based-distributions) for the extra packages musl images need. The URL is the standard Claude Code release location, so you can verify the downloaded binary against the release's signed manifest as described in [Binary integrity and code signing](/docs/en/setup#binary-integrity-and-code-signing). Build the image with Claude Code version 2.1.224 or later, then push it to your registry and reference it in the recipes below:

```bash theme={null}
docker build --build-arg CLAUDE_CODE_VERSION=2.1.224 -t <your-registry>/claude-runner:latest .
```

## Kubernetes

The runner serves `GET /healthz` on port 8080 by default, configurable with `--health-port`, so Kubernetes probes work with no extra setup. The endpoint returns `200` whenever the process is alive, so the probes below detect a dead process, not a stuck one; to catch a runner that stopped polling, alert on the `last_poll_age_seconds` series from [`/metrics`](/docs/en/self-hosted-environments-reference#prometheus-metrics). The Deployment below mounts the environment secret from a Kubernetes Secret, points the liveness and readiness probes at `/healthz`, and sets a 90-second termination grace period. See [Shutdown timing](#shutdown-timing) for why the grace period matters.

```yaml theme={null}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: claude-runner
  namespace: claude-runners
spec:
  replicas: 3
  selector:
    matchLabels:
      app: claude-runner
  template:
    metadata:
      labels:
        app: claude-runner
        app.kubernetes.io/part-of: claude-code-self-hosted-runner
    spec:
      terminationGracePeriodSeconds: 90
      containers:
        - name: runner
          image: <your-registry>/claude-runner:latest
          args:
            - self-hosted-runner
            - --environment-secret-file
            - /etc/claude/environment-secret
            - --capacity
            - "4"
          volumeMounts:
            - name: environment-secret
              mountPath: /etc/claude
              readOnly: true
          ports:
            - name: health
              containerPort: 8080
          readinessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 30
      volumes:
        - name: environment-secret
          secret:
            secretName: claude-runner-environment-secret
```

The Deployment above lives in a `claude-runners` namespace. Create the namespace first:

```bash theme={null}
kubectl create namespace claude-runners
```

Create the backing Secret from a local file holding the value you copied in the admin UI's [**Copy environment key** step](/docs/en/self-hosted-environments-quickstart#set-up-an-environment-and-runner), so the secret never appears in your shell history. Run `(umask 077 && cat > ./environment-secret)`, paste the secret, press Enter, then Ctrl-D. Then create the Secret and delete the file:

```bash theme={null}
kubectl create secret generic claude-runner-environment-secret -n claude-runners --from-file=environment-secret=./environment-secret
```

## Docker Compose

The Compose service below restarts the runner whenever it exits, which covers both crashes and the normal exit after draining. A Docker restart policy restarts the same container with its writable layer intact, so the runner comes back on a reused filesystem rather than the fresh one the [hardening posture](#harden-your-deployment) recommends; use this recipe for evaluation, and for production either recreate the container per run or use an orchestrator that does.

```yaml theme={null}
services:
  claude-runner:
    image: <your-registry>/claude-runner:latest
    command:
      - self-hosted-runner
      - --environment-secret-file
      - /run/secrets/environment-secret
      - --capacity
      - "4"
    secrets:
      - environment-secret
    restart: always
    stop_grace_period: 90s

secrets:
  environment-secret:
    file: ./environment-secret
```

## Shutdown timing

On `SIGTERM`, the runner stops taking new work, waits up to `--drain-wait-sec`, zero by default, for in-flight turns to finish, terminates each child process, and runs the [`post-session` lifecycle hook](/docs/en/self-hosted-environments-configuration#post-session). The full drain path needs up to `--session-stop-grace-sec` + `--drain-wait-sec` + `--post-session-hook-timeout-sec`, plus 15 seconds of fixed overhead for process cleanup, plus 30 more seconds when [`--push-outcome-on-release`](/docs/en/self-hosted-environments-reference#runner-cli-flags) is set. That is 80 seconds at defaults, and the runner logs the total at startup. Sessions drain in parallel under this one budget, so the total doesn't grow with `--capacity`.

At the default `--drain-wait-sec 0`, a rolling restart interrupts in-flight turns; each session resumes on another runner, losing unpushed work as described under [Known issues](#additional-limitations). Set `--drain-wait-sec`, and raise the grace period to match, to let turns finish first.

Throughout that whole path, the runner keeps heartbeating to the control plane at zero capacity, so the session lease doesn't expire and get requeued to another runner while the `post-session` hook is still writing out uncommitted work. The heartbeat stops just before the runner deregisters.

Set `terminationGracePeriodSeconds` on Kubernetes, `stop_grace_period` on Docker Compose, or your orchestrator's equivalent to at least the total the runner logs, so a container-wide kill never lands while a `post-session` hook is mid-run. If your hosts die at a known wall-clock time and you pass [`--retire-at`](/docs/en/self-hosted-environments-reference#runner-cli-flags), size the margin between the retire time and the kill to cover typical turns plus this same budget, and compute the value at each launch, for example `date +%s` plus the runner's intended lifetime, rather than baking a static value into a restartable manifest. The Kubernetes default of 30 seconds is shorter than the runner's drain path and will kill the pod mid-cleanup. For the flags that control each phase, see the [runner CLI reference](/docs/en/self-hosted-environments-reference#runner-cli-flags).

### What reaches a running post-session hook

The `post-session` hook and the Claude session child each run in their own POSIX process group, separate from the runner's, so stop mechanisms reach them differently:

* **A second `SIGTERM` to the runner**: force-exits the runner immediately, skipping whatever remains of the drain path. Nothing signals a mid-run `post-session` hook, so on a bare host where an init process adopts orphans, it finishes on its own, but unsupervised: its timeout budget no longer applies, and a write to the closed log pipe can kill it with `SIGPIPE`, so a hook that needs to survive a forced exit there should redirect its own output to a file. In the container recipes on this page the runner is the container's PID 1 and its exit ends the container, and under systemd's default `KillMode=control-group` the cgroup kill in the third bullet applies; in both, treat a forced exit as fatal to the hook and rely on the grace period instead.
* **Process-group-wide signals**, such as `kill -- -<pid>` in a wrapper script, shell job control, or a group-wide watchdog: reach the runner and a mid-`checkout`-hook subprocess, which stays group-attached deliberately, but not a mid-run `post-session` hook or the session child.
* **Cgroup-wide kills**, such as systemd's default `KillMode=control-group` or the `SIGKILL` Kubernetes delivers to the whole container when `terminationGracePeriodSeconds` expires: reach everything, including the hook. Process-group isolation doesn't protect against these, which is why the grace period must cover the full drain path.
* **The hook's own timeout**: when a hook exceeds `--post-session-hook-timeout-sec`, the runner sends `SIGTERM` to the hook's whole process group, then `SIGKILL` two seconds later, so a worker the hook forked, such as tar, rsync, or git, terminates with the wrapper shell instead of surviving as an orphan. The runner's supervision ends once the hook's stdio closes: a worker that redirected its own output to a file and outlives the `SIGTERM` stage is past the runner's reach.

On the first `SIGTERM`, and again on a forced exit, the runner logs how many `post-session` hooks are still running, so you can tell a quiet drain from one that's mid-snapshot.

## Keep the base directory and capacity identical across runners

If a runner dies mid-session, the server requeues the session and another runner in the environment picks it up. That runner derives the checkout path from its own `--base-dir` and `--capacity`: `--capacity 1` checks out directly under `--base-dir`, and a `--capacity` above `1` uses per-session worktrees instead. When runners in the same environment use different values for either flag, the resumed session's working directory changes, and absolute paths the agent recorded earlier, in edits, tool calls, or its own notes, point at a location that no longer exists.

Use the same `--base-dir` and `--capacity` on every runner in an environment, and don't use a per-host value such as an instance ID or hostname.

The base directory defaults to `/workspace`. The runner needs write access to it. At startup, before registering, the runner creates the directory and confirms it can write to it, and exits with `cannot create or write to base directory` when it can't. A runner started as root creates the default `/workspace` itself. For a non-root runner, create the directory and give the runner's user ownership before starting the runner, or point `--base-dir` at a directory that user already owns.

## Reuse a pre-warmed checkout

For large repositories, the clone can dominate session startup. At `--capacity 1` with no [`checkout` hook](/docs/en/self-hosted-environments-configuration#checkout), the runner keeps one canonical clone per repository at `<base-dir>/<owner>/<repo>` and reuses it across sessions: it fetches the requested ref, detaches `HEAD`, and resets hard to it, which is near-instant when little has changed. To skip the cold clone, bake a clone into your runner image at that path, which gives every fresh container the warm clone without reusing a disk, or point `--base-dir` at a persistent volume paired with [`--lock-to-account`](/docs/en/self-hosted-environments-reference#runner-cli-flags) so the disk only ever serves one account.

What the reuse path does and doesn't guarantee:

* **Any clone shape works**: a full, shallow, or single-branch clone at the path is used as-is. The runner never passes `--depth` when fetching into an existing clone, so a full pre-warm keeps its full history and a shallow one stays shallow. `CLAUDE_RUNNER_FETCH_DEPTH` (`full`, `0`, or a number; default 50) controls only the cold clone the runner makes when no clone exists yet.
* **Tracked changes reset, untracked files persist**: each session starts from a hard reset that wipes the previous session's tracked modifications, but the runner never runs `git clean`, so untracked files from the locked account's earlier sessions stay in the tree.
* **With the git proxy, the reset becomes a checkout**: with [`--use-anthropic-git-proxy`](#use-the-anthropic-git-proxy), the runner sanitizes the clone's `.git/` before each session, keeping the object store, refs, and shallow state but deleting the index, so each session pays a full working-tree checkout instead of a near-instant reset; it still never re-clones. Submodule pre-warms aren't supported under the proxy.
* **Long clones need no workaround**: the runner bounds each git operation with a 120-second no-progress watchdog and a 30-minute hard cap, not a flat timeout, so a slow cold clone that keeps reporting progress completes.

## Pin the version

Each session's child Claude Code process runs the runner's own binary, and the runner turns off auto-update inside the sessions it spawns, so every session runs the version you installed on the host or built into the image. A host-level update takes effect the next time the runner starts.

* **To hold a fleet on one version**: build the image with a pinned version, or on a bare host install a specific version and [disable auto-updates](/docs/en/setup#disable-auto-updates)
* **To upgrade**: install the newer version or rebuild the image, then restart the runners
* **Plugins**: plugin marketplaces don't auto-update either; set `FORCE_AUTOUPDATE_PLUGINS=1` in the runner's environment to let plugins auto-update while the binary stays pinned

## Scale the fleet

Your orchestrator decides when to add or remove runners. Because of the [one-user-per-runner lock](/docs/en/self-hosted-environments#runner-lifecycle), the minimum replica count is the number of users you expect to be active concurrently; `--capacity` controls parallelism within one user's sessions, not across users.

Two scaling approaches are available:

* **Fixed fleet**: run a static set of runner replicas and scale on the [Prometheus metrics](/docs/en/self-hosted-environments-reference#prometheus-metrics) each runner serves
* **On-demand runners**: run the `claude self-hosted-runner orchestrator` subcommand, which polls Anthropic for sessions that are queued with no runner available and invokes your `spawn-runner` hook to boot one per session. See [On-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners).

## Known issues and limitations

The following are the limitations in this release, with workarounds where one exists.

### Connector traffic leaves your network

Connector tools, such as GitHub, Slack, Linear, and the other claude.ai connectors, are called from Anthropic's side rather than from your runner, so when a self-hosted session uses a connector, that traffic routes through `api.anthropic.com`, not from inside your network boundary. To keep a connector out of self-hosted sessions, filter it like any other MCP server with the [`allowedMcpServers` and `deniedMcpServers` policy settings](/docs/en/managed-mcp#policy-based-control-with-allowlists-and-denylists), which apply to server-delivered connectors too. An allowlist you deploy for other servers also blocks delivered connectors. To keep connectors available alongside a URL-based allowlist, add an entry matching the session proxy URL, such as `https://api.anthropic.com/v2/ccr-sessions/*`. If tool traffic must stay inside your network, run the equivalent tools as local MCP servers on the runner image instead. See [MCP servers](/docs/en/self-hosted-environments-configuration#mcp-servers).

### Some sessions don't count as idle

A session holding a background task that never finishes doesn't count as idle, so `--release-idle-session-min` won't release that session's slot. A session that's waiting on an approval requested from inside a running tool call also doesn't count as idle. Always set `--kill-session-after-min` alongside it as a hard backstop so no session can hold a slot indefinitely.

### Additional limitations

* **Resumed sessions lose unpushed work**: when a session is released, on idle timeout or on a runner restart, and the user sends another message, the session resumes on a fresh runner that clones the repository again from its starting branch, so work the session hadn't pushed is gone. Set [`--push-outcome-on-release`](/docs/en/self-hosted-environments-reference#runner-cli-flags) to have the runner make a best-effort push of the session's outcome branches before it releases, so the resumed session starts from those commits instead; this preserves committed work, not a dirty working tree. Before enabling it, restrict who can push to `claude/*` refs on the source remote, for example with a branch ruleset: on resume, the runner fetches the previously pushed branch without verifying who pushed it, so anyone with push access to those refs can place content into the resumed workspace. The runner also discards per-session configuration on resume, meaning the session's Claude config directory and any shell state the session wrote; `--push-outcome-on-release` doesn't cover those.
* **Private repositories can't be added mid-session**: a repository added to a session after it has started isn't cloned with credentials on a self-hosted runner, so the add fails. Select every repository the session needs when you create it.
* **Some connectors don't appear in self-hosted sessions**: a connector you haven't yet connected in claude.ai Settings isn't listed in a self-hosted session, and the session won't prompt you to connect it. Connect it in Settings first, then start a fresh session. Adding a connector to an already-running session also doesn't make its tools available to Claude; start a fresh session to pick up a newly added connector.

### Report an issue

For issues with self-hosted environments, contact your Anthropic account team.

## Troubleshooting

For guided diagnosis, run the doctor subcommand on the runner host. It starts an interactive Claude Code session with read-only access to the runner's logs and state; the only change it can make is requeuing a stuck session. Sign in with `claude auth login` on that host first so the session can query your environment, its runners, and its queued sessions. Without that sign-in, for example when the host authenticates with an API key, it's limited to the local health endpoint, metrics, and the runner's log, and it reads the log only if you started the runner with `--log-file`.

```bash theme={null}
claude self-hosted-runner doctor
```

Common issues:

* **Runner doesn't appear in the environment**: confirm the host can reach `api.anthropic.com` over HTTPS, the environment secret is current, and the host clock is within five minutes of real time; larger skew causes authentication to fail. The runner logs `[runner:fatal]` with the rejection reason on auth failure.
* **Runner exits at startup with `cannot create or write to base directory`**: the runner can't create or write to `--base-dir`, which defaults to `/workspace`. Fix the directory's ownership or point `--base-dir` at a writable path, as described in [Keep the base directory and capacity identical across runners](#keep-the-base-directory-and-capacity-identical-across-runners). If the runner instead logs `[runner:fatal]` saying the base directory check timed out, the directory is on a hung NFS or CSI mount. Check mount health rather than permissions. The runner prints both of these startup failures to stderr before it opens `--log-file`, so look for them in the terminal or your platform's container logs rather than the log file. Before v2.1.225, the runner didn't check the base directory at startup, and this misconfiguration failed sessions after pickup instead.
* **Sessions stay queued**: every online runner may be locked to a different account. Check each runner's `claude_code_self_hosted_runner_locked_account` [metric](/docs/en/self-hosted-environments-reference#prometheus-metrics) or its `Picked up session` log lines to see which account holds it. Add replicas, or wait for an existing runner to drain and restart. If the environment uses on-demand runners, check the orchestrator instead; see [On-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners).
* **Sessions fail immediately after pickup**: open the session in claude.ai/code to see the error. The most common causes are missing [git credentials](#configure-git) in the runner image and build tools that aren't installed. An unwritable base directory stops the runner at startup instead of failing sessions. See the **Runner exits at startup with `cannot create or write to base directory`** entry in this list.
* **A session's branch no longer exists on the remote**: for a git source the session only reads from, the runner skips that source and continues on the remaining ones. For the source the session pushes results to, a deleted branch, typically because it was merged and auto-deleted, fails the session with an error naming the repository and branch and asking you to restore the branch and retry. The runner fails the session with the same error when skipping would leave it with no repository at all. Before v2.1.228, such a session started in an empty directory.
* **Sessions take minutes to start**: the initial clone usually dominates. Watch the `claude_code_self_hosted_runner_session_init_duration_seconds` [metric](/docs/en/self-hosted-environments-reference#prometheus-metrics) to confirm, and cut the clone with a [pre-warmed checkout](#reuse-a-pre-warmed-checkout) or a smaller `CLAUDE_RUNNER_FETCH_DEPTH`.
* **Pod is killed mid-drain**: raise `terminationGracePeriodSeconds` to at least the value the runner logs at startup. See [Shutdown timing](#shutdown-timing).

Once logging is initialized, the runner writes its lifecycle log, including `[runner:fatal]` lines, to stdout, and debug output to stderr, all as plain-text lines rather than JSON. The startup failures described in the troubleshooting entries above print to stderr before that point. Capture both streams with `--log-file`, which also lets `self-hosted-runner doctor` tail them, or with your platform's log collection. Each session's child process writes a separate debug log. On failure the runner preserves the log, prints the log's path in the runner log, and surfaces the log's tail alongside the session in claude.ai/code.

## What's next

* [Customize sessions](/docs/en/self-hosted-environments-configuration): wrapper scripts, lifecycle hooks, on-demand runners, MCP servers, and permissions
* [Test end to end](/docs/en/self-hosted-environments-testing): verify a new runner image from CI before promoting it
* [Reference](/docs/en/self-hosted-environments-reference): every CLI flag, environment variable, and metric
