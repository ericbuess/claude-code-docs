> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Deploy self-hosted environments to production

> Run self-hosted runners in production: security hardening, network egress control, git credentials, Kubernetes and Compose recipes, and troubleshooting.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; [Availability and limitations](/docs/en/self-hosted-environments#availability-and-limitations) covers the enablement path. This page covers running the fleet in production; see the [quickstart](/docs/en/self-hosted-environments-quickstart) for your first runner and session.
</Note>

A [self-hosted environment](/docs/en/self-hosted-environments) runs Claude Code [cloud sessions](/docs/en/claude-code-on-the-web) on runners you deploy inside your network, and in production those sessions execute model-directed code on behalf of everyone who can dispatch a session to the environment. This page is for the operator taking a working environment to production. It works through the deployment in order: what to lock down before connecting real systems, the egress the fleet needs, how sessions authenticate to your git host, the deployment recipes themselves, and what to check when sessions misbehave.

## Harden your deployment

A self-hosted runner executes arbitrary, model-directed code on your infrastructure on behalf of everyone who can dispatch a session to its environment. That's any member of your Anthropic organization, and anyone who can start a [Claude Tag](https://claude.com/docs/claude-tag/overview) channel session in a scope an Owner routed to the environment. Work through each item before you connect an environment to production systems:

* **Ephemeral, per-session containers**: run each runner process in a fresh container or VM that's destroyed when the process exits, with `--capacity 1` and the default `--drain-grace-sec 0` so each container serves exactly one session. At a higher capacity, or with a positive drain grace, one container serves multiple sessions from the same [locked owner](/docs/en/self-hosted-environments#key-concepts); see [Runner lifecycle](/docs/en/self-hosted-environments#runner-lifecycle). Don't reuse a filesystem between runner restarts, except in the deliberate [pre-warmed checkout](#reuse-a-pre-warmed-checkout) setup, and never across owners.
* **No broad credentials in the image**: don't include long-lived SSH keys, cloud-provider credentials, or personal access tokens that grant more than a session needs. Mint credentials used during a session, such as push or API tokens, per session from your [wrapper script](/docs/en/self-hosted-environments-configuration#wrapper-scripts). For the initial clone, which happens before the wrapper runs, use a [`checkout` lifecycle hook](/docs/en/self-hosted-environments-configuration#checkout) or [`--use-anthropic-git-proxy`](#use-the-anthropic-git-proxy); see [Configure git](#configure-git).
* **Keep the environment secret off session-running hosts**: the environment secret can register runners and pick up any session queued on the environment. On a fixed fleet it lives on every runner host, where any session's code can read the secret file. Prefer [on-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners), where the secret stays on the orchestrator host, which never runs user code, and each runner receives a single-use work order that registers exactly one runner. On a fixed fleet, treat the environment-secret file as readable by every session and rotate the secret after any suspected session compromise.
* **Default-deny network egress**: restrict runner and session container outbound traffic at your own network boundary on every environment; [Default-deny egress](#default-deny-egress) covers what to allow and why.
* **Least-privilege host IAM**: the compute identity attached to the runner host, such as an instance profile or node service account, should grant only what the runner itself needs. Sessions should obtain their own credentials through your wrapper script rather than inheriting the host's.
* **Block the cloud metadata endpoint from sessions**: keeping sessions off the host identity requires blocking their access to the cloud metadata endpoint, and subnet-level egress policies don't intercept link-local metadata traffic, so block it in the container itself:

  * IMDSv2 with a hop limit of one
  * GKE Workload Identity with metadata concealment
  * An explicit deny for `169.254.169.254` in the session container's network namespace

  The block applies to your wrapper script and lifecycle hooks too, since they share the container. Authenticate any token exchange with the [session JWT](/docs/en/self-hosted-environments-identity) against your own token service over allowlisted egress, or use a file-based web identity such as IAM Roles for Service Accounts (IRSA) on Amazon EKS.
* **Per-runner filesystem isolation**: each runner process gets its own working directory that no other process on the host can read or write. Make `--hooks-dir`, the wrapper script, and the host's `~/.claude/` read-only to the session, either built into the image or mounted read-only.
* **Dispatch has no per-environment access control**: any member of your Anthropic organization can dispatch a session to any of its environments. If an Owner [routes Claude Tag channels to the environment](/docs/en/cloud-environments#set-the-environment-a-claude-tag-channel-uses), anyone the [Claude Tag access setting](https://claude.com/docs/claude-tag/admins/restrict-access#restrict-who-can-use-claude) admits can start channel sessions that run there. By default that's anyone in the connected Slack workspace, with or without a Claude account. Treat every runner host as reachable for code execution by everyone who can dispatch to it, and place on a runner host only data and credentials that all of those people are allowed to read. [`--lock-to-account`](/docs/en/self-hosted-environments-reference#runner-cli-flags) bounds which account's sessions a given host executes, but it doesn't narrow who can dispatch into the environment. To make self-hosted environments the only picker option, an [Owner](/docs/en/cloud-environments#organization-shared-environments) can hide Anthropic-hosted environments for the whole organization from the [**Cloud environments** page](https://claude.ai/admin-settings/cloud-environments).
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
| `storage.googleapis.com`             | 443  | At session runtime, for the plugin install counts and metadata shown in `/plugin`.                                                                                                                                                                                                      |
| `code.claude.com` and `claude.com`   | 443  | Documentation lookups by the built-in claude-code-guide agent and pre-approved WebFetch requests during sessions. Blocking these hosts only affects documentation lookups.                                                                                                              |
| `*.frame.claudeusercontent.com`      | 443  | Only when the [Artifact tool](/docs/en/artifacts#availability) is available for sessions in your organization; defaults vary by plan, per the availability table there. Set `CLAUDE_CODE_DISABLE_ARTIFACT=1` on the runner to keep the tool disabled regardless of the organization setting. |
| `registry.npmjs.org`                 | 443  | When a session installs a plugin, both for fetching npm-source plugin packages and for installing a plugin's Node.js dependencies, or when an `npx`-launched MCP server runs                                                                                                            |
| `http-intake.logs.us5.datadoghq.com` | 443  | Anthropic operational metrics. Only when `CLAUDE_CODE_BYOC_ENABLE_DATADOG=1` is set; off by default in self-hosted environments.                                                                                                                                                        |
| `browser-intake-us5-datadoghq.com`   | 443  | Anthropic error-report uploads, sent only when [error reporting](/docs/en/data-usage#telemetry-services) is enabled for the session's account. Suppressed by `DISABLE_ERROR_REPORTING=1` or `DISABLE_TELEMETRY=1`.                                                                           |

The runner doesn't reach `statsig.anthropic.com`, `*.sentry.io`, `claude.ai`, or `platform.claude.com`. These hosts appear in some older enterprise network checklists, but you don't need to allowlist them for runner or session traffic: feature-flag fetches go to `api.anthropic.com`, and the runner authenticates with the environment secret rather than interactive OAuth. Two host-side flows do reach `claude.ai`, so run them from a host whose egress allows it rather than widening session-container egress: the one-line installer fetches `install.sh` from `claude.ai` at install time, and interactive `claude auth login`, which the [guided setup](/docs/en/self-hosted-environments-quickstart#set-up-an-environment-and-runner), `doctor`'s signed-in mode, and [CI dispatch](/docs/en/self-hosted-environments-testing#authenticate-from-ci) use, signs in through `claude.ai`, `claude.com`, and `platform.claude.com`. `mcp-proxy.anthropic.com` isn't required either: self-hosted sessions don't use it, and delivery of your organization's claude.ai connectors to sessions, when enabled for your organization, routes through `api.anthropic.com`. See [MCP servers](/docs/en/self-hosted-environments-configuration#mcp-servers).

### Default-deny egress

Deploy runner and session containers in a network segment or namespace whose outbound traffic is limited to the hosts in the [network requirements table](#network-requirements), your git host, and the specific internal services sessions need to reach. The product can't verify or enforce this, so apply it at your own network boundary on every environment. Session code is model-directed and can attempt connections to arbitrary hosts; default-deny egress at the network layer bounds where those attempts can land. This applies regardless of permission mode: the default pre-approved tool set already includes `Bash`, so shell egress runs without a prompt even without [auto mode](/docs/en/self-hosted-environments-configuration#permissions-and-tool-approval).

For details on which telemetry each session emits and how to turn it off, see [Telemetry](/docs/en/self-hosted-environments-reference#telemetry).

### Authenticate to an egress proxy

Some corporate egress proxies require a `Proxy-Authorization` header on every connection. The token in that header often rotates too fast to write into the proxy URL you set in `HTTPS_PROXY`. Set `HTTPS_PROXY` or `HTTP_PROXY` to your proxy's URL as usual, then set `--proxy-authorization-command` or `--proxy-authorization-file` to tell the runner where to read the header value from. Both flags require Claude Code v2.1.238 or later.

#### Choose where the `Proxy-Authorization` value comes from

Pick the flag that matches how you produce the `Proxy-Authorization` token:

* **[`--proxy-authorization-command <command>`](/docs/en/self-hosted-environments-reference#runner-cli-flags)**: choose this for a token you generate on demand. The runner runs the shell command and uses its trimmed stdout as the header value, for example `Bearer <token>`.
* **[`--proxy-authorization-file <path>`](/docs/en/self-hosted-environments-reference#runner-cli-flags)**: choose this for a token another process rotates in place. The runner reads the file and uses its trimmed contents as the header value.

#### Configurations the runner refuses to start with

Each flag also has an environment variable form, listed beside it in the [runner CLI flags reference](/docs/en/self-hosted-environments-reference#runner-cli-flags). Before the runner contacts your proxy or the control plane, it checks the flags and their variables, and refuses to start in three cases:

* **Both flags set**: one flag plus the other flag's environment variable counts as setting both.
* **No proxy URL**: neither `HTTPS_PROXY` nor `HTTP_PROXY` holds an `http://` or `https://` URL. The runner reads both variables in upper or lower case, and doesn't consult `ALL_PROXY`.
* **Either flag passed to the orchestrator subcommand**: `self-hosted-runner orchestrator` doesn't accept the flags or their environment variables. Pass the flag to each runner the orchestrator starts instead.

#### What the runner changes while a proxy-authorization flag is set

With either flag set, the runner starts a listener of its own and sends proxy traffic from itself, its lifecycle hooks, and its sessions through that listener. The listener adds the `Proxy-Authorization` header on the way to your proxy.

* **Listener**: the listener is a forward proxy on `127.0.0.1`. The runner starts the listener before registering with the control plane, and exits at startup if the listener can't start.
* **Proxy variables**: the runner rewrites whichever of `HTTPS_PROXY` and `HTTP_PROXY` you set so that it points at the listener. That rewritten value reaches the runner itself, its lifecycle hooks, and every session it runs.
* **Token rotation**: a rotated token takes effect without a restart. For each connection the listener opens to your proxy, the runner runs your command or reads your file again and adds the result as the header.
* **Session environment**: a session reaches your proxy only through the listener. In each session's environment the runner removes `ALL_PROXY`, removes any spelling of `HTTPS_PROXY` or `HTTP_PROXY` that you didn't set, and pins `NO_PROXY` to the runner's own value.
* **Logs**: the runner never logs the header value.

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

Don't bake long-lived or broadly-scoped push credentials into a shared runner image: a credential in the image is available to every session the image runs, whoever started it. Instead, mint a short-lived, least-scoped token per session from your [wrapper script](/docs/en/self-hosted-environments-configuration#wrapper-scripts), using the session creator's identity decoded from the session JWT. Pair it with an ephemeral per-session container, which requires `--capacity 1`, so no credential outlives the session that minted it; see the [hardening section](#harden-your-deployment).

If you must configure push credentials at the image level, for example for a read-only deploy key, scope them as tightly as your git host allows:

* An SSH deploy key limited to one repository with a `url.<base>.insteadOf` rewrite
* A `credential.helper` that returns a minimally-scoped token
* `GIT_SSH_COMMAND` pointing at a narrowly-scoped key

Whichever mechanism you configure must work without a prompt, because the runner's built-in clone and fetch disable the prompts that git, SSH, and Git Credential Manager would otherwise show:

* The runner sets `GIT_TERMINAL_PROMPT=0`, so git doesn't ask for a username or password.
* The runner runs SSH with `BatchMode=yes`, appended to your `GIT_SSH_COMMAND` if you set one, so SSH doesn't ask for a passphrase or host confirmation.
* The runner sets `GCM_INTERACTIVE=never`, so Git Credential Manager doesn't open a sign-in dialog.
* The runner clears `core.askPass`, so if you use an askpass helper, set it through the `GIT_ASKPASS` environment variable instead.

If your git host rejects the credential, or you didn't configure one, the runner retries a few times and then fails repository preparation. The runner doesn't pass these settings into the session's environment.

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

The recipes below use `--capacity 4`, so one container serves up to four concurrent sessions from the same locked owner. That doesn't provide the per-session container isolation in the [hardening section](#harden-your-deployment): before connecting an environment to production systems, either run the recipes at `--capacity 1` with one container per session, or use [on-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners), which also keep the environment secret off session-running hosts.

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

## Size CPU and memory for sessions

Size a runner's container or host for the sessions it runs rather than for the runner process. The runner itself polls for work, prepares each session's checkout, runs your [lifecycle hooks](/docs/en/self-hosted-environments-configuration#lifecycle-hooks), and starts and supervises the session processes. The load comes from the sessions: each one is a Claude Code process plus whatever it starts, such as builds, test suites, package installs, and [MCP servers](/docs/en/mcp).

For one session, start with the following values, stated as Kubernetes requests and limits or your platform's equivalent, and treat them as a starting point rather than a requirement:

* **Memory**: a request and a limit of 4 GiB each, which meets the 4 GB minimum in Claude Code's [system requirements](/docs/en/setup#system-requirements). Keep the two equal so the scheduler accounts for the container's full memory. When the container reaches its memory limit, the kernel kills processes inside it, which can end a session mid-task.
* **CPU**: a request of 2 CPUs and a limit of 4 CPUs, so a session can burst above the request during builds. The kernel throttles a container at its CPU limit rather than killing processes in it, so sessions at the limit run slower but keep running.

In a Kubernetes container spec, set those starting values with the following `resources` block:

```yaml theme={null}
resources:
  requests:
    cpu: "2"
    memory: 4Gi
  limits:
    cpu: "4"
    memory: 4Gi
```

Builds and tests are usually the largest and most variable part of a session's load, so run a representative build of your repository, measure its peak CPU and memory, and raise any starting value that leaves no room for the Claude Code process on top of that peak.

The runner uses `--capacity` to cap how many sessions it runs at once. It doesn't divide CPU or memory between them, so the sessions on a runner share the container's CPU and memory. To cap one session's share, apply limits from your [wrapper script](/docs/en/self-hosted-environments-configuration#wrapper-scripts). What to give one container therefore depends on how many sessions it serves at once:

* **One session per runner**: give each container one session's values. Use this sizing at `--capacity 1`, which the [hardening section](#harden-your-deployment) recommends, and for [on-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners), where you set the values on the workload your [`spawn-runner` hook](/docs/en/self-hosted-environments-configuration#the-spawn-runner-hook) submits, such as a Kubernetes Job's pod template.
* **Several sessions per runner**: at a `--capacity` above one, multiply one session's values by the capacity, because up to that many sessions can run in the container at the same time. The [Kubernetes](#kubernetes) and [Docker Compose](#docker-compose) recipes run `--capacity 4` with no CPU or memory limits, so add limits sized for the capacity you run.

## Kubernetes

The runner serves `GET /healthz` on port 8080 by default, configurable with `--health-port`, so Kubernetes probes work with no extra setup. The endpoint returns `200` whenever the process is alive, so the probes below detect a dead process, not a stuck one; to catch a runner that stopped polling, alert on the `last_poll_age_seconds` series from [`/metrics`](/docs/en/self-hosted-environments-reference#prometheus-metrics). The Deployment below mounts the environment secret from a Kubernetes Secret, points the liveness and readiness probes at `/healthz`, and sets a 90-second termination grace period. See [Shutdown timing](#shutdown-timing) for why the grace period matters.

The manifest sets no CPU or memory `resources` on the runner container. Add a block sized for the capacity you run, as [Size CPU and memory for sessions](#size-cpu-and-memory-for-sessions) describes.

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

On `SIGTERM`, the runner stops taking new work and, unless you set [`--defer-shutdown-max-min`](#defer-the-drain-past-the-first-signal), waits up to `--drain-wait-sec`, zero by default, for in-flight turns to finish, terminates each session's process tree, and runs the [`post-session` lifecycle hook](/docs/en/self-hosted-environments-configuration#post-session). That process tree includes commands Claude was still running in the session.

The full drain path needs up to `--session-stop-grace-sec` + `--drain-wait-sec` + `--post-session-hook-timeout-sec`, plus 15 seconds of fixed overhead for process cleanup, plus 30 more seconds when [`--push-outcome-on-release`](/docs/en/self-hosted-environments-reference#runner-cli-flags) is set. That is 80 seconds at defaults, and the runner logs the total at startup. Sessions drain in parallel under this one budget, so the total doesn't grow with `--capacity`.

At the default `--drain-wait-sec 0`, a rolling restart interrupts in-flight turns; each session resumes on another runner, losing unpushed work as described under [Known issues](#additional-limitations). Set `--drain-wait-sec`, and raise the grace period to match, to let turns finish first.

Throughout that whole path, the runner keeps heartbeating to the control plane at zero capacity, so the session lease doesn't expire and get requeued to another runner while the `post-session` hook is still writing out uncommitted work. The heartbeat stops just before the runner deregisters.

Give the runner at least the total it logs at startup before the host stops it. Where you set that depends on how your hosts stop:

* **With a `SIGTERM` grace period**: set `terminationGracePeriodSeconds` on Kubernetes, `stop_grace_period` on Docker Compose, or your orchestrator's equivalent to at least that total. The Kubernetes default of 30 seconds is shorter than the runner's drain path, so Kubernetes stops the pod before the runner finishes draining.
* **With [`--retire-at`](/docs/en/self-hosted-environments-reference#runner-cli-flags)**: size the margin between the retire time and the host's stop time to cover typical turns, plus the background-task hold that [Runner lifecycle](/docs/en/self-hosted-environments#runner-lifecycle) describes, plus that same total. Compute the retire time at each launch, for example `date +%s` plus the runner's intended lifetime.
* **With [`--defer-shutdown-max-min`](#defer-the-drain-past-the-first-signal)**: add two more parts to the drain-path total. The first is the minutes you configure. The second is the post-release grace that [Defer the drain past the first signal](#defer-the-drain-past-the-first-signal) describes, 75 seconds at defaults. With the flag set, the runner also prints the combined figure at startup, after the drain-path total.

### Defer the drain past the first signal

Set [`--defer-shutdown-max-min <n>`](/docs/en/self-hosted-environments-reference#runner-cli-flags) if you want a runner you're restarting to go on serving the sessions it holds for up to `n` minutes, instead of draining them on the first signal. On the first `SIGTERM` or `SIGINT`, the runner stops taking new work and goes on serving the sessions it holds. It keeps polling so that the control plane doesn't requeue those sessions. Requires Claude Code v2.1.238 or later.

#### What happens to the sessions the runner holds after the first signal

In the first two stages that follow the signal, the runner releases sessions, and a released session resumes on a fresh runner when its user sends their next message. Counting from the first signal, the runner moves through three stages:

* **For the first `n` minutes**: the runner serves its sessions normally and keeps enforcing `--startup-timeout-min` and `--kill-session-after-min`. If you also set [`--release-idle-session-min`](/docs/en/self-hosted-environments-reference#runner-cli-flags), the runner releases any session whose user has been idle that long; without it, the runner releases no session early, apart from a startup timeout.
* **When the `n` minutes run out**: the runner releases every session it still holds, idle or not. The runner waits for a mid-turn session's turn to end, and up to 60 seconds more for a turn's background tasks, before releasing that session.
* **When the post-release grace runs out**: the runner drains whatever sessions it still holds, and the control plane requeues each drained session to another runner right away. The post-release grace starts when the `n` minutes run out and is 75 seconds at defaults. If you set `--drain-wait-sec` above 60 seconds, the post-release grace is `--drain-wait-sec` plus 15 seconds instead.

At any stage, the runner exits 0 as soon as it holds no sessions. A second signal cuts the stages short: the runner drains immediately, as it does on the first signal without `--defer-shutdown-max-min`. Once a drain is under way, the next signal force-exits the runner. That holds whether a second signal or the post-release grace running out started the drain.

#### Size the stop timeout

Give your host's stop timeout at least the sum of three parts: the `n` minutes you configure, the post-release grace, and the full drain path that [Shutdown timing](#shutdown-timing) describes. With default settings the post-release grace is 75 seconds and the drain path is 80 seconds, so allow `n` minutes plus 155 seconds. The runner prints this sum at startup whenever `--defer-shutdown-max-min` is set.

If the stop timeout runs out before the runner finishes, the host kills the runner. The sessions it still holds get no `post-session` hook. The runner doesn't deregister, and the control plane requeues the sessions about a minute later. If you can't give the stop timeout that sum, leave `--defer-shutdown-max-min` unset so the runner drains on the first signal instead.

### What reaches a running post-session hook

The `post-session` hook and the Claude session child each run in their own POSIX process group, separate from the runner's, so stop mechanisms reach them differently:

* **A `SIGTERM` while the runner is already draining**: force-exits the runner immediately, skipping whatever remains of the drain path. Without [`--defer-shutdown-max-min`](#defer-the-drain-past-the-first-signal), that is the second `SIGTERM` the runner receives. Nothing signals a mid-run `post-session` hook, so on a bare host where an init process adopts orphans, it finishes on its own, but unsupervised: its timeout budget no longer applies, and a write to the closed log pipe can kill it with `SIGPIPE`, so a hook that needs to survive a forced exit there should redirect its own output to a file. In the container recipes on this page the runner is the container's PID 1 and its exit ends the container, and under systemd's default `KillMode=control-group` the cgroup-wide kill reaches the hook too, as the **Cgroup-wide kills** entry describes; in both, treat a forced exit as fatal to the hook and rely on the grace period instead.
* **Process-group-wide signals**, such as `kill -- -<pid>` in a wrapper script, shell job control, or a group-wide watchdog: reach the runner and a mid-`checkout`-hook subprocess, which stays group-attached deliberately, but not a mid-run `post-session` hook or the session child.
* **Cgroup-wide kills**, such as systemd's default `KillMode=control-group` or the `SIGKILL` Kubernetes delivers to the whole container when `terminationGracePeriodSeconds` expires: reach everything, including the hook. Process-group isolation doesn't protect against these, which is why the grace period must cover the full drain path.
* **The hook's own timeout**: when a hook exceeds `--post-session-hook-timeout-sec`, the runner sends `SIGTERM` to the hook's whole process group, then `SIGKILL` two seconds later, so a worker the hook forked, such as tar, rsync, or git, terminates with the wrapper shell instead of surviving as an orphan. The runner's supervision ends once the hook's stdio closes: a worker that redirected its own output to a file and outlives the `SIGTERM` stage is past the runner's reach.

When the drain starts, and again on a forced exit, the runner logs how many `post-session` hooks are still running, so you can tell a quiet drain from one that's mid-snapshot.

## Keep the base directory and capacity identical across runners

If a runner dies mid-session, the server requeues the session and another runner in the environment picks it up. That runner derives the checkout path from its own `--base-dir` and `--capacity`: `--capacity 1` checks out directly under `--base-dir`, and a `--capacity` above `1` uses per-session worktrees instead. When runners in the same environment use different values for either flag, the resumed session's working directory changes, and absolute paths the agent recorded earlier, in edits, tool calls, or its own notes, point at a location that no longer exists.

Use the same `--base-dir` and `--capacity` on every runner in an environment, and don't use a per-host value such as an instance ID or hostname.

The base directory defaults to `/workspace`, with the exception the [`--base-dir` reference row](/docs/en/self-hosted-environments-reference#runner-cli-flags) records. The runner needs write access to it. At startup, before registering, the runner creates the directory and confirms it can write to it, and exits with `cannot create or write to base directory` when it can't. A runner started as root creates the default `/workspace` itself. For a non-root runner, create the directory and give the runner's user ownership before starting the runner, or point `--base-dir` at a directory that user already owns.

## Reuse a pre-warmed checkout

For large repositories, the clone can dominate session startup. At `--capacity 1` with no [`checkout` hook](/docs/en/self-hosted-environments-configuration#checkout), the runner keeps one canonical clone per repository at `<base-dir>/<repo-owner>/<repo>` and reuses it across sessions: it fetches the requested ref, detaches `HEAD`, and resets hard to it, which is near-instant when little has changed. To skip the cold clone, supply the clone in one of two ways:

* **Clone in the image**: build the clone into your runner image at that path. Every fresh container then starts with the warm clone without reusing a disk.
* **Clone on a persistent volume**: on runners you pre-lock to one user's account with [`--lock-to-account`](/docs/en/self-hosted-environments-reference#runner-cli-flags), point `--base-dir` at a persistent volume, so the disk only ever serves that account. A pre-locked runner never picks up Claude Tag channel sessions, so this option doesn't apply to runners that serve them.

What the reuse path does and doesn't guarantee:

* **Any clone shape works**: a full, shallow, or single-branch clone at the path is used as-is. The runner never passes `--depth` when fetching into an existing clone, so a full pre-warm keeps its full history and a shallow one stays shallow. `CLAUDE_RUNNER_FETCH_DEPTH` (`full`, `0`, or a number; default 50) controls only the cold clone the runner makes when no clone exists yet.
* **Tracked changes reset, untracked files persist**: each session starts from a hard reset that wipes the previous session's tracked modifications, but the runner never runs `git clean`, so untracked files from the locked owner's earlier sessions stay in the tree.
* **With the git proxy, the reset becomes a checkout**: with [`--use-anthropic-git-proxy`](#use-the-anthropic-git-proxy), the runner sanitizes the clone's `.git/` before each session, keeping the object store, refs, and shallow state but deleting the index, so each session pays a full working-tree checkout instead of a near-instant reset; it still never re-clones. Submodule pre-warms aren't supported under the proxy.
* **Long clones need no workaround**: the runner bounds each git operation with a 120-second no-progress watchdog and a 30-minute hard cap, not a flat timeout, so a slow cold clone that keeps reporting progress completes.

## Pin the version

Each session's child Claude Code process runs the runner's own binary, and the runner turns off auto-update inside the sessions it spawns, so every session runs the version you installed on the host or built into the image. A host-level update takes effect the next time the runner starts.

* **To hold a fleet on one version**: build the image with a pinned version, or on a bare host install a specific version and [disable auto-updates](/docs/en/setup#disable-auto-updates)
* **To upgrade**: install the newer version or rebuild the image, then restart the runners
* **Plugins**: plugin marketplaces don't auto-update either; set `FORCE_AUTOUPDATE_PLUGINS=1` in the runner's environment to let plugins auto-update while the binary stays pinned

## Scale the fleet

Your orchestrator decides when to add or remove runners. Because of the [one-owner-per-runner lock](/docs/en/self-hosted-environments#runner-lifecycle), the minimum replica count is the number of users and Claude Tag agents you expect to be active concurrently; `--capacity` controls parallelism within one owner's sessions, not across owners.

Two scaling approaches are available:

* **Fixed fleet**: run a static set of runner replicas and scale on the [Prometheus metrics](/docs/en/self-hosted-environments-reference#prometheus-metrics) each runner serves
* **On-demand runners**: run the `claude self-hosted-runner orchestrator` subcommand, which polls Anthropic for sessions that are queued with no runner available and invokes your `spawn-runner` hook to boot one per session. See [On-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners).

## Known issues and limitations

The following are the limitations in this release, with workarounds where one exists.

### Connector traffic leaves your network

Anthropic calls connector tools, such as GitHub, Slack, Linear, and the other claude.ai connectors, from its own infrastructure rather than from your runner, so when Claude uses a connector in a self-hosted session, that traffic goes through `api.anthropic.com` rather than originating inside your network boundary. To keep a connector out of self-hosted sessions, filter it like any other MCP server with the [`allowedMcpServers` and `deniedMcpServers` policy settings](/docs/en/managed-mcp#policy-based-control-with-allowlists-and-denylists). Claude Code applies these settings to the connectors Anthropic delivers as well as to the servers you configure, so if you deploy an allowlist for other servers, Claude Code blocks delivered connectors too. To keep connectors available alongside a URL-based allowlist, add entries that match the Anthropic proxy paths for delivered connectors:

* `https://api.anthropic.com/v2/ccr-sessions/*`
* `https://api.anthropic.com/v1/code/sessions/*`
* `https://api.anthropic.com/v1/code/mcp/*`

If tool traffic must stay inside your network, run the equivalent tools as local MCP servers on the runner image instead. See [MCP servers](/docs/en/self-hosted-environments-configuration#mcp-servers).

### Some sessions don't count as idle

A session holding a background task that never finishes doesn't count as idle, so `--release-idle-session-min` won't release that session's slot. A session that's waiting on an approval requested from inside a running tool call also doesn't count as idle. Always set `--kill-session-after-min` alongside it as a hard backstop so no session can hold a slot indefinitely.

`--kill-session-after-min` is a backstop for runaway sessions. The runner terminates any session that reaches the limit, even one someone is still using, so set the flag well above your longest expected session, such as `--kill-session-after-min 480` for 8 hours. To free slots from conversations that go idle, use `--release-idle-session-min` instead.

### Additional limitations

* **Resumed sessions lose unpushed work**: when a session is released, on idle timeout or on a runner restart, and the user sends another message, the session resumes on a fresh runner that clones the repository again from its starting branch, so work the session hadn't pushed is gone. Set [`--push-outcome-on-release`](/docs/en/self-hosted-environments-reference#runner-cli-flags) to have the runner make a best-effort push of the session's outcome branches before it releases, so the resumed session starts from those commits instead; this preserves committed work, not a dirty working tree. Before enabling it, restrict who can push to `claude/*` refs on the source remote, for example with a branch ruleset: on resume, the runner fetches the previously pushed branch without verifying who pushed it, so anyone with push access to those refs can place content into the resumed workspace. The runner also discards per-session configuration on resume, meaning the session's Claude config directory and any shell state the session wrote; `--push-outcome-on-release` doesn't cover those.
* **Private repositories can't be added mid-session**: a repository added to a session after it has started isn't cloned with credentials on a self-hosted runner, so the add fails. Select every repository the session needs when you create it.
* **Some connectors don't appear in self-hosted sessions**: a connector you haven't yet connected in claude.ai Settings isn't listed in a self-hosted session, and the session won't prompt you to connect it. Connect it in Settings first, then start a fresh session. Adding a connector to an already-running session also doesn't make its tools available to Claude; start a fresh session to pick up a newly added connector.

### Report an issue

For issues with self-hosted environments, contact your Anthropic account team.

## Troubleshooting

For guided diagnosis, run the doctor subcommand on the runner host. The doctor subcommand starts an interactive Claude Code session with the runner's logs and state attached. Sign in with `claude auth login` on that host first so the session can query your environment, its runners, and its queued sessions. Without that sign-in, for example when the host authenticates with an API key, it's limited to the local health endpoint, metrics, and the runner's log, and it reads the log only if you started the runner with `--log-file`.

```bash theme={null}
claude self-hosted-runner doctor
```

Common issues:

* **Runner doesn't appear in the environment**: confirm the host can reach `api.anthropic.com` over HTTPS, the environment secret is current, and the host clock is within five minutes of real time; larger skew causes authentication to fail. The runner logs `[runner:fatal]` with the rejection reason on auth failure.
* **Runner exits at startup with `cannot create or write to base directory`**: the runner can't create or write to `--base-dir`, which defaults to `/workspace`. Fix the directory's ownership or point `--base-dir` at a writable path, as described in [Keep the base directory and capacity identical across runners](#keep-the-base-directory-and-capacity-identical-across-runners). If the runner instead logs `[runner:fatal]` saying the base directory check timed out, the directory is on a hung NFS or CSI mount. Check mount health rather than permissions. The runner prints both of these startup failures to stderr before it opens `--log-file`, so look for them in the terminal or your platform's container logs rather than the log file. Before v2.1.225, the runner didn't check the base directory at startup, and this misconfiguration failed sessions after pickup instead.
* **Sessions stay queued**: every online runner may be locked to a different owner. Check each runner's `claude_code_self_hosted_runner_locked_account` [metric](/docs/en/self-hosted-environments-reference#prometheus-metrics) or the `locked_account` field of its `[runner:health]` log line to see who holds it. Both show the owner's email only after the runner has been issued a session token carrying an `act.email` claim, which a Claude Tag agent's sessions never do. Without the claim, the runner emits no `locked_account` series and logs `locked_account=yes`, which tells you the runner is locked but not to which owner. Add replicas, or wait for an existing runner to drain and restart. If the environment uses on-demand runners, check the orchestrator instead; see [On-demand runners](/docs/en/self-hosted-environments-configuration#on-demand-runners).
* **Sessions fail immediately after pickup**: open the session in claude.ai/code to see the error. The most common causes are missing [git credentials](#configure-git) in the runner image and build tools that aren't installed. An unwritable base directory stops the runner at startup instead of failing sessions. See the **Runner exits at startup with `cannot create or write to base directory`** entry in this list.
* **Sessions can't reach the network through an authenticating egress proxy**: when the source you set with [`--proxy-authorization-command` or `--proxy-authorization-file`](#authenticate-to-an-egress-proxy) fails, times out after 30 seconds, or yields an empty value, the runner answers that connection `502 Bad Gateway` and logs why. The runner redacts the command's stderr in that log and never logs the header value. With `--proxy-authorization-command`, run the command yourself on the host to confirm it prints the whole header value on stdout. If the runner instead exits at startup with `could not start the proxy-authorization listener`, it couldn't open its loopback listener.
* **Runner logs `Poll failed` lines containing `rejecting the malformed poll response`**: the runner received a work-poll response whose body isn't the queue's expected JSON, most often because something between the runner and `api.anthropic.com`, such as an intercepting proxy or a captive portal, answered with its own page. The runner rejects the response, counts it under the `transport` kind of the `claude_code_self_hosted_runner_poll_errors_total` [metric](/docs/en/self-hosted-environments-reference#prometheus-metrics), and retries on the failed-poll schedule described in [Session lifecycle](/docs/en/self-hosted-environments#session-lifecycle). The runner keeps serving its live sessions. Configure the proxy to pass responses from `api.anthropic.com` through unaltered. Before v2.1.246, the runner read such a response as an empty work queue, which could end its live sessions or make it exit.
* **A session's branch no longer exists on the remote**: for a git source the session only reads from, the runner skips that source and continues on the remaining ones. For the source the session pushes results to, a deleted branch, typically because it was merged and auto-deleted, fails the session with an error naming the repository and branch and asking you to restore the branch and retry. The runner fails the session with the same error when skipping would leave it with no repository at all. Before v2.1.228, such a session started in an empty directory.
* **Sessions take minutes to start**: the initial clone usually dominates. Watch the `claude_code_self_hosted_runner_session_init_duration_seconds` [metric](/docs/en/self-hosted-environments-reference#prometheus-metrics) to confirm, and cut the clone with a [pre-warmed checkout](#reuse-a-pre-warmed-checkout) or a smaller `CLAUDE_RUNNER_FETCH_DEPTH`.
* **Pod is killed mid-drain**: raise `terminationGracePeriodSeconds` to at least the value the runner logs at startup. See [Shutdown timing](#shutdown-timing).

Once logging is initialized, the runner writes its lifecycle log, including `[runner:fatal]` lines, to stdout, and debug output to stderr, all as plain-text lines rather than JSON. The startup failures described in the troubleshooting entries above print to stderr before that point. Capture both streams with `--log-file`, which also lets `self-hosted-runner doctor` tail them, or with your platform's log collection. Each session's child process writes a separate debug log. On failure the runner preserves the log, prints the log's path in the runner log, and surfaces the log's tail alongside the session in claude.ai/code.

## What's next

* [Customize sessions](/docs/en/self-hosted-environments-configuration): wrapper scripts, lifecycle hooks, on-demand runners, MCP servers, and permissions
* [Test end to end](/docs/en/self-hosted-environments-testing): verify a new runner image from CI before promoting it
* [Reference](/docs/en/self-hosted-environments-reference): every CLI flag, environment variable, and metric
