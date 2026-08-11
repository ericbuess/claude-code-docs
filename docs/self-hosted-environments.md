> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Self-hosted environments

> Run Claude Code cloud sessions on infrastructure you control: set up a self-hosted environment, deploy runners, and route sessions to your own compute.

<Note>
  Self-hosted environments are in public beta on Team and Enterprise plans and are off by default. See [Availability and limitations](#availability-and-limitations) for the enablement path and what's excluded.
</Note>

A self-hosted environment executes Claude Code cloud sessions on infrastructure your organization operates. A [cloud session](/docs/en/claude-code-on-the-web) is any session that runs somewhere other than the developer's machine: developers start them from claude.ai, the mobile and desktop apps, the terminal with [`claude --cloud`](/docs/en/claude-code-on-the-web#from-terminal-to-web), and [scheduled routines](/docs/en/routines), and by default they execute on Anthropic's infrastructure. In a self-hosted environment, those same sessions execute inside your network, and the developer experience is otherwise the same apart from the differences in [Availability and limitations](#availability-and-limitations) and the deploy page's [known issues](/docs/en/self-hosted-environments-deploy#known-issues-and-limitations).

If your team doesn't use cloud sessions, there's nothing here to configure: sessions in a terminal or IDE always run on the developer's own machine. If you want to run Claude Code on your own always-on machine and drive it from other devices, use [Remote Control](/docs/en/remote-control), which is also available on Pro and Max plans. When you're ready to set up, go straight to the [quickstart](/docs/en/self-hosted-environments-quickstart); to review the security posture first, start with [Deploy to production](/docs/en/self-hosted-environments-deploy). The rest of this page explains how self-hosting works and when to choose it.

## How self-hosted environments work

Self-hosting has three parts:

* **Environment**: a named destination that cloud sessions can be sent to. Your organization creates environments in claude.ai admin settings, and each one groups a set of runners.
* **Runner**: a program running on hosts inside your network. Runners execute the sessions; the idea is the same as a self-hosted CI runner.
* **Session**: one Claude Code task a developer started.

When a developer starts a cloud session, the session-start UI shows an environment picker listing Anthropic-hosted environments alongside any your organization has created. If they choose yours, Anthropic's control plane places the session on your environment's queue, where a runner claims it, clones the repository the developer chose, and starts a Claude Code process on your host to run it. The runner authenticates to your git host with credentials you configure; [Configure git](/docs/en/self-hosted-environments-deploy#configure-git) covers the options. Sessions reach your internal services from inside your network, and your git host the same way when it's internal; the traffic to Anthropic, queue polling, the session's event stream, and model inference, is outbound HTTPS to `api.anthropic.com`, with the short list of further hosts sessions can reach in [Network requirements](/docs/en/self-hosted-environments-deploy#network-requirements). Anthropic never connects into your network.

<div style={{maxWidth: "640px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/Y0sJ2uDoOVbOVZrQ/images/self-hosted-network-paths.svg?fit=max&auto=format&n=Y0sJ2uDoOVbOVZrQ&q=85&s=8056103fc1c5564c7f0ef219d260b99d" className="dark:hidden" alt="Architecture diagram of a self-hosted environment: your network boundary contains a runner, two Claude Code session processes inside it, and your git host, with api.anthropic.com outside holding queue, session stream, and inference. The runner polls the queue and reaches the git host, each session process opens its own stream, inference, and git connections, and every connection is outbound from your network, with none inbound." width="680" height="320" data-path="images/self-hosted-network-paths.svg" />

    <img src="https://mintcdn.com/claude-code/Y0sJ2uDoOVbOVZrQ/images/self-hosted-network-paths-dark.svg?fit=max&auto=format&n=Y0sJ2uDoOVbOVZrQ&q=85&s=fec6aef3b0740d80eaf6d6a7000a2233" className="hidden dark:block" alt="Architecture diagram of a self-hosted environment: your network boundary contains a runner, two Claude Code session processes inside it, and your git host, with api.anthropic.com outside holding queue, session stream, and inference. The runner polls the queue and reaches the git host, each session process opens its own stream, inference, and git connections, and every connection is outbound from your network, with none inbound." width="680" height="320" data-path="images/self-hosted-network-paths-dark.svg" />
  </Frame>
</div>

The two Claude Code boxes in the diagram are session processes: one runner executing two sessions at once, up to its configured capacity. A runner serves one user at a time, locking to that user's account when it claims its first session, so checked-out code never mixes between users; [Runner lifecycle](#runner-lifecycle) covers the rule.

You can start runners yourself and keep them running, or run the [autoscaling orchestrator](/docs/en/self-hosted-environments-configuration#on-demand-runners), a second process you host, which starts runners as sessions queue; each runner exits on its own when its work finishes. Either way, you set the environment up once, and it appears in the picker on every supported surface.

## Availability and limitations

Check these before planning a rollout:

* **Plans**: public beta for Team and Enterprise organizations. Self-hosted environments are off by default; an [Owner or admin](/docs/en/cloud-environments#organization-shared-environments) turns on **Allow self-hosted environments** on the [**Cloud environments** admin page](https://claude.ai/admin-settings/cloud-environments), which requires [Claude Code on the web](/docs/en/claude-code-on-the-web) to be enabled for the organization.
* **Zero Data Retention**: unavailable for organizations with [Zero Data Retention](/docs/en/zero-data-retention) enabled.
* **Model inference**: sessions use the Anthropic API, and inference can't be routed through [Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry](/docs/en/third-party-integrations), or an [LLM gateway](/docs/en/llm-gateway).
* **Surfaces**: sessions started from [Claude Code on the web](/docs/en/claude-code-on-the-web), the mobile and desktop apps, [scheduled routines](/docs/en/routines), and the terminal, with [`claude --cloud`](/docs/en/claude-code-on-the-web#from-terminal-to-web) or an [`--environment` dispatch](/docs/en/self-hosted-environments-testing#run-the-test-loop), can run in self-hosted environments. [Claude Tag](https://claude.com/docs/claude-tag/overview), [Claude Security](/docs/en/claude-security), and [Code Review](/docs/en/code-review) sessions don't route to them yet. Support for those surfaces follows separately.
* **Repositories**: sessions check out repositories from GitHub; see [GitHub authentication options](/docs/en/claude-code-on-the-web#github-authentication-options).
* **Billing**: sessions in a self-hosted environment consume your organization's Claude Code usage the same way sessions in Anthropic-hosted environments do.

## Why self-host

Most teams are better served by Anthropic-hosted environments, which need no infrastructure to run or maintain. Self-hosting is for teams whose network, tooling, or compliance requirements call for keeping session execution on infrastructure they control. If that's you, plan for the operational ownership it carries: you build and maintain the runner image, operate the fleet, and control its network.

In exchange, self-hosting gives you network access, custom tooling, and compliance control:

* **Network access**: sessions run inside your network and can reach internal services, databases, and registries without exposing them to the public internet
* **Custom tooling**: pre-install compilers, SDKs, and internal CLIs in your runner image so every session starts ready to build
* **Compliance**: repository checkouts and build artifacts stay on infrastructure you control. Session content still goes to `api.anthropic.com` for model inference.

## Environments, runners, and sessions

Environments are managed on the **Cloud environments** page in claude.ai admin settings; runners are processes you start and manage on your own infrastructure.

### Key concepts

These terms appear throughout the self-hosted pages:

| Term               | What it is                                                                                                                                                                                              |
| :----------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Environment        | A named group of your runners, created in claude.ai settings. Sessions are routed to an environment, not to an individual runner.                                                                       |
| Environment secret | The single shared credential runners use to authenticate and register with the environment. Shown once at environment creation, labeled **environment key** in the admin UI.                            |
| Runner             | The long-lived process you deploy. A runner registers with the environment, receives a runner token, and polls for sessions.                                                                            |
| Session            | One Claude Code task, started from claude.ai, the mobile app, or another Anthropic surface such as a scheduled routine or an agent. Each session runs as a child Claude Code process the runner spawns. |

In API fields, token claims, and metric names, the environment appears as `pool`, and the environment ID is the `pool_id`. The [reference](/docs/en/self-hosted-environments-reference) maps the two spellings, including the deprecated `pool` flag names.

A runner serves one user at a time. The first session a runner picks up locks the runner to that user, and the runner then runs sessions only for that user, up to a configured capacity. The minimum fleet size is therefore the number of users you expect to be active at once.

### Session lifecycle

When a developer starts a session and selects your environment, Anthropic's control plane places the session on the environment's queue. From there:

1. A runner with free capacity claims the session and holds a lease on it.
2. The runner clones the repository into its working directory and spawns a child Claude Code process.
3. The child streams events back over HTTPS while the runner keeps polling; each poll refreshes the lease and doubles as the heartbeat.
4. If the runner stops polling for about 60 seconds, the server requeues the session for another runner.

### Runner lifecycle

The first session a runner picks up locks the runner to the account of the user who started that session, and the runner runs up to `--capacity` concurrent sessions for that account. While the runner has active sessions, the runner keeps claiming the locked account's queued work. What happens once they finish depends on [`--drain-grace-sec`](/docs/en/self-hosted-environments-reference#runner-cli-flags):

* **At the default of `0`**: the runner exits as soon as its active sessions finish, without polling for more, so the orchestrator you deploy it under, such as Kubernetes, can restart it with a fresh disk, ready to serve any account.
* **At a positive value**: the runner keeps polling the locked account's queue for that many seconds before exiting.

This lifecycle isolates each user's checked-out code without requiring the runner to delete disk state between users.

A kill that delivers `SIGTERM` needs no flag: the runner drains as [Shutdown timing](/docs/en/self-hosted-environments-deploy#shutdown-timing) describes. If your infrastructure instead destroys hosts at a known wall-clock time without a signal, or with a grace period too short to drain, such as a sandbox lifetime cap or spot-instance reclamation, pass `--retire-at <epoch-seconds>` set to a few minutes before that time. At the retire time:

1. The runner stops taking new work.
2. The runner releases each active session through the same release path the [`--release-idle-session-min`](/docs/en/self-hosted-environments-reference#runner-cli-flags) flag uses, so the session resumes on a fresh runner when the user sends their next message. A session that's mid-turn is released as soon as that turn finishes; a session whose finished turn left background tasks running gets up to 60 seconds of grace before releasing anyway.
3. The runner exits 0 once all its sessions are released.

A turn that outlives the kill is still lost; [Shutdown timing](/docs/en/self-hosted-environments-deploy#shutdown-timing) covers sizing the margin. Without `--retire-at`, a signal-less host kill is indistinguishable from a crash: the control plane records a lost worker rather than a clean release, and the session requeues to another runner.

### Network paths

The runner and its sessions make several kinds of outbound connection, and no inbound connectivity from Anthropic is required:

* **Control plane**: the runner polls `api.anthropic.com` for work and posts setup-progress and failure events, all outbound HTTPS. Polling doubles as the runner's heartbeat.
* **SCM connector**: the optional orchestrator [SCM connector](/docs/en/self-hosted-environments-reference#scm-connector-flags) tunnel is the only WebSocket connection.
* **Git**: the runner clones from and pushes to your git host over HTTPS or SSH, authenticated with credentials your deployment provides; [Configure git](/docs/en/self-hosted-environments-deploy#configure-git) covers the options, including per-session minted credentials and the [Anthropic git proxy](/docs/en/self-hosted-environments-deploy#use-the-anthropic-git-proxy), which routes git through `api.anthropic.com` instead.
* **Session child**: the child Claude Code process holds the session's event stream to `api.anthropic.com`, and makes its own outbound calls for model inference and for git commands run during the session. See [Network requirements](/docs/en/self-hosted-environments-deploy#network-requirements) for the full egress list. The [diagram above](#how-self-hosted-environments-work) shows these paths, apart from the optional SCM connector.

Model inference uses the Anthropic API. The control plane delivers the API endpoint to each session, and the session authenticates with an Anthropic-issued, session-scoped OAuth token, so inference can't be routed through [Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry](/docs/en/third-party-integrations), or an [LLM gateway](/docs/en/llm-gateway) in self-hosted environments.

Corporate egress proxies are supported. The runner and the optional [autoscaling orchestrator](/docs/en/self-hosted-environments-configuration#on-demand-runners) honor the proxy and mTLS environment variables described in [Network configuration](/docs/en/network-config), such as `HTTPS_PROXY` and `NO_PROXY`; set them in each process's environment. The variables cover control-plane calls, the orchestrator's [SCM connector](/docs/en/self-hosted-environments-reference#scm-connector-flags) WebSocket, and the built-in clone for HTTPS remotes, and sessions inherit them from the runner. Session streaming uses server-sent events over HTTPS, so a proxy in the path must not buffer responses.

## What stays on your infrastructure

Repository checkouts, build artifacts, secrets, and any files a session creates or modifies stay on the machines you provision. The conversation itself, including prompts, responses, and tool results, goes to `api.anthropic.com` for model inference, and Anthropic stores the session transcript so you can resume the session from another [supported surface](#availability-and-limitations).

Session orchestration, queueing, and the claude.ai interface remain Anthropic-hosted: a self-hosted environment moves session execution into your network, not the control plane.

## Get started

The self-hosted environments pages are organized by what you're doing:

* [Quickstart](/docs/en/self-hosted-environments-quickstart): install Claude Code, create an environment, start a runner, and route your first session
* [Deploy to production](/docs/en/self-hosted-environments-deploy): security hardening, network egress, git credentials, Kubernetes and Compose recipes, known issues, and troubleshooting
* [Customize sessions](/docs/en/self-hosted-environments-configuration): wrapper scripts for per-session credentials, lifecycle hooks, on-demand runners, MCP servers, and permissions
* [Test end to end](/docs/en/self-hosted-environments-testing): a CI smoke test that verifies a runner image before you promote it
* [Reference](/docs/en/self-hosted-environments-reference): every CLI flag, environment variable, metric, and the health endpoint
* [Verify session identity](/docs/en/self-hosted-environments-identity): validate the session token from your own services before granting access
