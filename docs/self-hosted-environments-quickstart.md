> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Self-hosted environments quickstart

> Set up your first self-hosted environment: install Claude Code, create the environment, start a runner, and route a session to it.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans; [Availability and limitations](/docs/en/self-hosted-environments#availability-and-limitations) covers the enablement path. This page gets your first session running; see [Self-hosted environments](/docs/en/self-hosted-environments) for what they are and [Deploy to production](/docs/en/self-hosted-environments-deploy) for hardening and fleet recipes.
</Note>

A [self-hosted environment](/docs/en/self-hosted-environments) runs Claude Code [cloud sessions](/docs/en/claude-code-on-the-web) on infrastructure your organization operates, executed by runner processes you deploy. This quickstart stands up your first one, the smallest that works: one runner on a single host, running one test session. There are two steps: [create the environment, start a runner, and route a session to it](#set-up-an-environment-and-runner), then [message that session from your terminal](#send-a-follow-up-message-to-a-running-session). You'll move between two surfaces: claude.ai for creating the environment, checking its status, and routing a session, and a terminal on the host for everything the runner does.

By the end you'll have an environment on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments), a runner polling for work, and a session running on your host. Before you connect real repositories or internal systems, work through [Deploy to production](/docs/en/self-hosted-environments-deploy), which covers the security posture, egress control, git credentials, and orchestration.

## Prerequisites

### Organization and roles

The claude.ai side needs:

* **Allow self-hosted environments** turned on by an [Owner](/docs/en/cloud-environments#organization-shared-environments) on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments); the **New** button doesn't appear until it is. If you don't hold the role, someone who does can create the environment and hand you its secret; the runner and terminal steps on this page need no claude.ai role, and where a step checks status in the admin UI, the runner's own log lines give you the same signal.
* A [GitHub connection](/docs/en/claude-code-on-the-web#github-authentication-options) for your organization, so developers can pick repositories when they start sessions.

### Host and network

The runner host needs:

* A Linux or macOS host or container with outbound HTTPS to `api.anthropic.com`, to `claude.ai` and the download hosts it redirects to for the install step below, and to your git host for the clone; the [network requirements table](/docs/en/self-hosted-environments-deploy#network-requirements) has the full list. Windows isn't supported as a runner host; run the runner in a Linux container instead. Developer workstations aren't affected, since sessions start from claude.ai in a browser.
* A repository for the test session: a public one, or one this host can already clone by its HTTPS URL without being asked for credentials.
* A clock synchronized to real time, for example with NTP. Authentication fails when the clock is more than five minutes off; see [Troubleshooting](/docs/en/self-hosted-environments-deploy#troubleshooting).

### Software on the runner host

Install on the host before you start:

* **Claude Code v2.1.224 or later**, with any of the [standard install methods](/docs/en/setup). The runner is part of the standard `claude` binary, and earlier versions don't recognize the `self-hosted-runner` subcommand. The native installer's default `latest` channel carries each release as soon as it's published; the `stable` channel, the Homebrew `claude-code` cask, and the stable apt, dnf, and apk repositories trail by about a week. To pin the exact version your fleet runs, see [Install a specific version](/docs/en/setup#install-a-specific-version). For container images, see the Dockerfile in [Deploy to production](/docs/en/self-hosted-environments-deploy#build-the-runner-image).
* **Git 2.24 or newer**. Some git options on the deploy page need newer versions; [Configure git](/docs/en/self-hosted-environments-deploy#configure-git) states each floor.

Confirm the host is ready:

```bash theme={null}
claude self-hosted-runner --help
```

A ready host prints the runner's usage text, listing flags such as `--environment-secret-file`. On versions older than 2.1.224, the command prints the general `claude --help` output instead; upgrade with `claude update` or reinstall from the `latest` channel.

## Set up an environment and runner

Use either the [guided setup](#run-the-guided-setup) or the [manual steps](#set-up-manually). The guided setup is a single command that starts an interactive Claude Code session and walks you through the rest. Use the manual steps instead on a host where an interactive session isn't possible. Also use them when someone who holds the Owner role created the environment and handed you its secret, since the guided setup needs an Owner sign-in.

### Run the guided setup

The guided setup walks you through creating the environment in the admin UI, starts a local runner with the secret file you save, confirms that the runner registers, and writes a cheat sheet to `./runner-setup/CHEAT-SHEET.md`. Before you run it, confirm your sign-in and version:

* **Sign-in**: run it on a machine where you've signed in with `claude auth login` using an account that holds an Owner role. With only an API key or a third-party model provider, the session starts but its organization checks fail.
* **Version**: confirm the [version check](#software-on-the-runner-host) passed. On versions older than 2.1.224, the setup command starts a Claude session with the words as the prompt instead of the guided setup.

To start the guided setup, run the setup subcommand in your shell and follow the prompts:

```bash theme={null}
claude self-hosted-runner setup
```

The setup doesn't start a test session itself: it tells you to start one at claude.ai/code. The setup's last step stops the runner it started. If you leave the setup before that step, the runner keeps running. To keep going after the last step, start the runner again in your shell with the command in `./runner-setup/CHEAT-SHEET.md`, then [route a session to the environment](#route-a-session).

### Set up manually

Create the environment on claude.ai, start the runner from a terminal on the host, then return to claude.ai to confirm the runner appears and route a session to it. If someone who holds the Owner role already created the environment and handed you its secret, start at step 2.

<Steps>
  <Step title="Create an environment">
    Go to the [**Cloud environments** page](https://claude.ai/admin-settings/cloud-environments) in admin settings. Under **Self-hosted environments**, select **New**, name the environment, and select **Create**. On the wizard's second step, select **Copy environment key** to copy the environment secret, which the admin UI labels an environment key. claude.ai shows the secret once, and you can't retrieve it later; it expires 365 days after creation. The environment's `ccpool_...` ID stays visible in its detail dialog; you'll need it for the `aud` check in [token verification](/docs/en/self-hosted-environments-identity) and for dispatching [test sessions from CI](/docs/en/self-hosted-environments-testing#run-the-test-loop).

    If you lose the secret or need to rotate it, create a new secret from the environment's **Configuration** tab, roll the new secret out to your runners, then revoke the old one. Runners holding a revoked secret fail their next authenticated poll and exit, logging `poll auth failed`, and your orchestrator restarts them with the new secret.
  </Step>

  <Step title="Start a runner">
    Create the secret directory. This command and the next use `/etc/claude`, which needs root, and the secret file they create is readable only by the user who runs them. If the runner will run as another user, it exits with `error: Failed to read environment secret file <path> (EACCES: permission denied, open '<path>')`. In that case, run both commands as the runner's user with a directory that user can write to in place of `/etc/claude`, and pass the same path to `--environment-secret-file`. Any path the runner process can read works.

    ```bash theme={null}
    mkdir -p /etc/claude
    ```

    Write the environment secret to a file. The command below reads from your terminal so the secret stays out of shell history: paste the value you copied, press Enter, then Ctrl-D, and the subshell's `umask` makes the file readable only by its owner.

    ```bash theme={null}
    (umask 077 && cat > /etc/claude/environment-secret)
    ```

    Choose a base directory, replacing `<writable-dir>` in the runner command below with an absolute path that the runner can write to or create. The runner creates the directory at startup, then checks repositories out and creates per-session directories under it. Without `--base-dir` it uses `/workspace`, which only works if that directory already exists and is writable or you start the runner as root.

    If the runner can't create or write to the path, it exits at startup with an error naming the directory instead of registering. See [Troubleshooting](/docs/en/self-hosted-environments-deploy#troubleshooting).

    Then start the runner with `--environment-secret-file` and `--base-dir`:

    ```bash theme={null}
    claude self-hosted-runner --environment-secret-file '/etc/claude/environment-secret' --base-dir '<writable-dir>'
    ```

    The runner logs `Registered: runner_id=<runner-id>` once it has registered with your environment, then begins polling for work. If the runner exits later, restart it yourself. See [If the runner exits](#if-the-runner-exits) for when that happens.
  </Step>

  <Step title="Verify the runner appears">
    Return to the [**Cloud environments** page](https://claude.ai/admin-settings/cloud-environments). Your environment's status changes from **No runners deployed** to **Healthy** within a few seconds of the runner starting; open the environment and select **Activity** to see the runner itself. If you don't have access to the admin page, the `Registered: runner_id=<runner-id>` line in the runner's log from the previous step gives you the same signal.
  </Step>

  <Step title="Route a session to the environment">
    <span id="route-a-session" />Start a session at claude.ai/code and select your environment from the environment picker, where self-hosted environments appear alongside Anthropic-hosted ones. For the repository, pick the one from the [prerequisites](#host-and-network): a public repository, or one this host can already clone. The runner clones with whatever git credentials the host already has.

    The next available runner picks up the queued session and logs `Picked up session <session-id>` along with its active count and capacity, so you can confirm from the runner's own output which host took the session. Watch the session work and read Claude's replies at [claude.ai/code](https://claude.ai/code).

    If the session doesn't start working, match what you see:

    * **The session sits queued**: see [Troubleshooting](/docs/en/self-hosted-environments-deploy#troubleshooting).
    * **The session fails to start with a git error**: the error appears in the session and in the runner's log. If it includes git's `could not read Username for` followed by your git host's URL, the runner had no HTTPS credentials for that host. See [Configure git](/docs/en/self-hosted-environments-deploy#configure-git), which also covers credential options for private repositories in production.
  </Step>
</Steps>

### If the runner exits

If the runner exits during this quickstart, start it again with the same command. The runner can exit on its own:

* **Sessions finished**: the log shows `[runner:exit] account workload drained — exiting`. The runner exits by design once its active sessions finish. See [Runner lifecycle](/docs/en/self-hosted-environments#runner-lifecycle).
* **Lost contact**: the log shows a `[runner:fatal]` line with `runner record gone server-side` or with `poll auth failed`. If the runner loses contact with Anthropic for a while, for example because the host sleeps, it can exit when it next reaches Anthropic.

A finished turn doesn't end your test session. After the first turn the session is still attached and the runner is still up, so you can [send the session a follow-up message](#send-a-follow-up-message-to-a-running-session) without restarting the runner first.

For production, deploy the runner under an orchestrator that restarts it on exit and waits longer between restarts when the runner keeps exiting right after it starts. See [Deploy to production](/docs/en/self-hosted-environments-deploy) and [When the runner exits](/docs/en/self-hosted-environments-deploy#when-the-runner-exits).

## Send a follow-up message to a running session

Once a session is running on your environment, send it a follow-up from the `claude` CLI on any machine where you're logged in with `claude auth login`; the command doesn't need to run from the machine that started the session. The command posts one message:

```bash theme={null}
claude -p "your message" --cloud <session-id>
```

For `<session-id>`, pass the bare `session_...` or `cse_...` ID or the session's claude.ai/code URL. A successful send prints `Sent to cloud session.` with the session ID and a view link. Accepted ID forms, JSON output, and the account and policy requirements are on [Send follow-ups from the CLI](/docs/en/claude-code-on-the-web#send-follow-ups-from-the-cli), since the command works the same against Anthropic-hosted sessions.

## What's next

* [Deploy to production](/docs/en/self-hosted-environments-deploy): harden the deployment, control egress, configure git credentials, and run the fleet under Kubernetes or Compose
* [Customize sessions](/docs/en/self-hosted-environments-configuration): wrapper scripts, lifecycle hooks, on-demand runners, MCP servers, and permissions
* [Test end to end](/docs/en/self-hosted-environments-testing): a CI smoke test that dispatches a session and reads Claude's replies
