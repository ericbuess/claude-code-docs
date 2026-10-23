> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure cloud environments

> Configure cloud environments for Claude Code cloud sessions: network access levels, environment variables, setup scripts, and environment caching.

> [!NOTE]
>
> Cloud environments apply to [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md), which are available on Pro, Max, and Team plans, and for Enterprise users with [premium seats or Chat + Claude Code seats](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan).

Each [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md) runs in a cloud environment. You can configure an environment to allow or deny [network access](#access-levels), [set environment variables](#set-environment-variables) for the session, store [network secrets](#add-network-secrets) that sessions use without seeing them, and run a [setup script](#setup-scripts) before Claude starts working.

The same environments apply wherever you start a cloud session:

* The [Desktop app](https://code.claude.com/docs/en/desktop.md)
* The [Claude mobile app](https://code.claude.com/docs/en/mobile.md)
* Your browser at [claude.ai/code](https://claude.ai/code)
* The terminal with [`claude --cloud`](https://code.claude.com/docs/en/claude-code-on-the-web#from-terminal-to-cloud)
* [Cloud scheduled tasks](https://code.claude.com/docs/en/routines.md)
* [Claude Tag](https://claude.com/docs/claude-tag/overview)

Each of these surfaces can also route to a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments). [Availability and limitations](https://code.claude.com/docs/en/self-hosted-environments#availability-and-limitations) covers what Claude can't use yet when a Claude Tag session runs in one.

> [!NOTE]
>
> [Remote Control](https://code.claude.com/docs/en/remote-control.md) sessions connect the web and mobile interfaces to a session on your own machine, which uses your machine's network and files, not a cloud environment. Claude Tag channel sessions use organization-level environments only, either [shared environments](#organization-shared-environments) or [self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments).

## The Default environment

If you don't have an environment yet, onboarding sets up the **Default** environment. How depends on where you onboard:

* **CLI flows such as `/web-setup`**: create **Default** for you
* **Web onboarding on Pro and Max**: creates **Default** for you
* **Web onboarding on Team and Enterprise**: shows a **Create your first cloud environment** form unless an Owner has turned on [Quick setup](https://code.claude.com/docs/en/claude-code-on-the-web.md#quick-setup-for-team-and-enterprise); keep the form's defaults and click **Create & finish** to get the same **Default** environment

**Default** carries no configuration of its own:

* [**Trusted** network access](#access-levels): sessions reach package registries and other [allowlisted domains](#default-allowed-domains), and nothing else through the session's network.
* No other configuration: **Default** defines no environment variables or setup script, so sessions start with just the [pre-installed tools](#installed-tools).

With only **Default** available, every session runs in it. When you have more than one environment, sessions choose one per surface:

* In the Desktop app, the mobile app, and at claude.ai/code, sessions you start yourself use the environment shown in the [selector](#configure-your-environment). An [organization default](#organization-shared-environments) set by an Owner fills the selection when you haven't picked one. Threads in a [project](https://code.claude.com/docs/en/claude-projects.md#project-settings-reference) use the environment set in the project's settings instead.
* From the CLI, Claude Code uses your [`/remote-env` pick](#select-an-environment-from-the-cli), or falls back to the Anthropic-hosted environment when your list has one, and otherwise to the first environment in your list that isn't a bridge environment, an entry [Remote Control](https://code.claude.com/docs/en/remote-control.md) registers to represent your own machine rather than a cloud environment. For a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments), passing `--environment <environment-id>` with its `ccpool_` ID [when you dispatch a session](https://code.claude.com/docs/en/self-hosted-environments-testing.md#run-the-test-loop) overrides the `/remote-env` pick and the fallback for that invocation. Claude Code rejects Anthropic-hosted `env_` IDs passed to the flag, so use `/remote-env` to target those. The flag requires Claude Code v2.1.224 or later.

Configure an environment when the default isn't enough: when Claude needs to reach domains outside the [default allowlist](#default-allowed-domains), needs environment variables set for its sessions, or needs dependencies installed before it starts working.

## Configure your environment

Add, edit, and archive environments from the environment selector under the message box on the screen where you start a new session at [claude.ai/code](https://claude.ai/code). To reach that screen, complete [web onboarding](https://code.claude.com/docs/en/web-quickstart.md). For the Desktop app, see [Cloud sessions](https://code.claude.com/docs/en/desktop.md#cloud-sessions). Environments you create are personal to your account; [shared environments](#organization-shared-environments) created by an Owner appear in the selector alongside them. See [Installed tools](#installed-tools) for what's available without any configuration.

The selector appears only until you send a new session's first message. To edit the environment of a running cloud session of your own, select the caret after the session title at the top, then select **Edit cloud environment**.

**1. Open the environment selector**

On the new-session screen, select the first control in the row under the message box.

**2. Add or edit an environment**

* **Add an environment**: select **New environment** at the bottom of the menu to open the **New environment** dialog. Fill in the form and select **Add environment**. Your new session then uses the environment you added.
* **Edit an environment**: find its row under **Cloud**. If **Cloud** is a single row, select it to open the list. If your environment isn't listed under **Cloud**, select the **More** row under that heading. Hover over the environment's row and select the settings icon that appears on its right to open its dialog.

When you add an environment or edit one of your own, select the dialog's [**Network access**](#network-access), [**Setup script**](#add-a-setup-script), or [**Environment variables**](#set-environment-variables) row to open that setting. After your last change, save with **Add environment** for a new environment or **Save changes** for an existing one. To store a key that sessions use without seeing it, see [Add network secrets](#add-network-secrets).

### Set environment variables

Environment variables use `.env` format, one `KEY=value` pair per line. Plain values don't need quotes, and if you quote a value with a matching pair, the quotes don't become part of the value. Quote a value that spans multiple lines or contains a `#`: in an unquoted value, `#` starts a comment and the rest of the line is dropped.

The following example defines three variables.

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

A session reads the environment's values into ordinary environment variables that any command Claude runs can read, except `OTEL_*` variables. Claude Code uses those for its own [telemetry export](https://code.claude.com/docs/en/monitoring-usage.md#telemetry-from-cloud-sessions-and-claude-tag) and doesn't pass them to the commands it runs.

In an Anthropic-hosted environment, a session reads the environment's values when you create it and again each time Claude Code starts in the session's VM afterward, which happens in two cases:

* **The VM is restored after being idle**: after a few minutes without activity, a session's VM pauses with its files saved. Your next message restores the same VM and starts Claude Code again.
* **The VM was reclaimed and is rebuilt**: if the paused VM has since been [reclaimed](https://code.claude.com/docs/en/claude-code-on-the-web.md#environment-expired), reopening the session provisions a fresh VM.

After you edit, add, or remove a variable, an existing session in an Anthropic-hosted environment keeps the values it last read until its VM is next restored or rebuilt, and uses your change from then on. Its VM pauses on its own once the session is idle, and you can't pause it yourself. To use a new value right away, ask Claude to set it on the command it runs, for example `LOG_LEVEL=trace npm test`, or start a new session.

A cloud session also sets some variables itself when it starts. For [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](https://code.claude.com/docs/en/claude-code-on-the-web#manage-context), the value the session sets overrides one you add here, so adding that key here has no effect.

Anyone who uses the environment can read the values. In an Anthropic-hosted environment, use a [network secret](#add-network-secrets) instead for a key the agent proxy can attach to a request. The [requests that never get a secret](#requests-that-never-get-the-credential) are listed there.

### Add network secrets

A network secret is an API key or token you store on a cloud environment so Claude can call that API from any session in the environment without seeing the key. Anthropic's agent proxy adds the key to requests for the hosts you list, after each request leaves the session's VM, so the key itself stays outside the VM.

Network secrets are available on Pro, Max, Team, and Enterprise plans. To check whether you can add one yourself, see [Requirements](#requirements).

#### Requirements

These requirements decide whether you can add a secret and whether the agent proxy can use it once added:

* **Role**: on Pro, Max, and Team plans, you can add and delete secrets on your own environments whatever your role. On Team and Enterprise, Owners hold an organization admin role in your claude.ai organization and Admins don't, which changes what you see in these cases:
  * **Your own environment on Enterprise**: with an organization admin role, you add and delete secrets. Without it, the **Network secrets** row opens the secrets list with the note "Only an organization admin can add or delete network secrets" and no **Add secret** or delete button. Ask an Owner to add the secret to a [shared environment](#organization-shared-environments), then run your sessions there
  * **A shared environment**: Owners [add and delete its secrets](#add-a-credential) from admin settings. Without an organization admin role, ask an Owner to add the secret, because the environment's dialog has no **Network secrets** section
  * **Your own environment on Team**: without an organization admin role, **Add secret** opens a [shorter form](#add-a-secret-without-the-role) that takes one host
* **Environment type**: an Anthropic-hosted cloud environment that already exists. A [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments) doesn't have network secrets
* **API reachability**: the API accepts connections from the internet, because requests leave from Anthropic's network
* **Encryption keys**: if your organization uses customer-managed encryption keys, you can't save network secrets

#### Add a secret

You add secrets one at a time, and you can't edit a secret after you add it. To change a secret's hosts or value, delete it and add it again.

To add a secret to a [shared environment](#organization-shared-environments), open it for editing from the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings), then continue from step 2 in its **Network secrets** section. If you're on a Team plan and don't hold an [organization admin role](#requirements), follow step 1 on your own environment, then [fill in the shorter form](#add-a-secret-without-the-role).

**1. Open the environment's network secrets**

[Open the environment for editing](#configure-your-environment) at [claude.ai/code](https://claude.ai/code). In the **Edit cloud environment** dialog, select the **Network secrets** row. You see the secrets already on the environment, each with the hosts it applies to.

**2. Add the secret**

Select **Add secret** and fill in the form. Keep the default **Secret type**, **Bearer**, for an API key that travels in a request header, and fill in these fields:

* **Name**: a label for the secret, such as `Internal billing API`
* **Allowed websites**: the API's hosts, such as `api.example.com`. A leading `*.` matches every subdomain
* **Custom headers**: one row for the header that carries the key. The row starts with `Authorization` as the header's **Name** and `Bearer` as its **Prefix**; paste the key itself as the **Value**. For a header like `X-Api-Key` that takes the bare value, change the name and clear the prefix

For an API that authenticates another way, pick a different **Secret type**. The list is the same one [Claude Tag](https://claude.com/docs/claude-tag/overview), the Slack integration for Team and Enterprise plans, offers for [connections](https://claude.com/docs/claude-tag/admins/add-connections).

**3. Save the secret**

Select **Add**. The secret appears in the list with its hosts, saved without the dialog's **Save changes** button. You can't view the value again after saving.

To confirm the secret works, start a session in the environment and ask Claude to call the API, for example with `curl`. The API answers as if the key were in the request, and the key doesn't appear in the session's environment variables or in any file. If the list marks a secret **Not sent** instead, the note under it says why and what to do. Two secrets whose hosts overlap without matching exactly get no marker, and the agent proxy sends only one of them.

#### Add a secret on a Team plan without an organization admin role

If you're on a Team plan and don't hold an [organization admin role](#requirements), the **Add secret** form takes one secret for one host. Select your environment's [**Network secrets** row](#add-a-credential) and then **Add secret**. Fill in these fields and select the form's **Add secret** button:

* **Host**: the one host that gets the secret, such as `api.example.com`. The form doesn't accept a `*.` wildcard
* **Name**: an optional label for the secret
* **Secret type**: **Token** for a key that travels in a request header, or **Username and password**. For a token, paste the key as the **Value**

#### Which requests get the secret

The agent proxy attaches a secret to a request when the request's host matches one you listed on that secret. Sessions can reach those hosts even when the environment's [network access level](#access-levels) wouldn't otherwise allow them, except the [hosts that never get the secret](#requests-that-never-get-the-credential). The secret applies in every session that runs in the environment, whoever started it, until you delete it.

#### Requests that never get the secret

The agent proxy never attaches a secret you add to these requests:

* **GitHub**: the [GitHub proxy](#github-proxy) authenticates requests to GitHub instead, so you don't need a network secret for it
* **The Anthropic API and public package registries**: `api.anthropic.com`, `registry.npmjs.org`, `jsr.io`, `npm.jsr.io`, `pypi.org`, `files.pythonhosted.org`, `index.crates.io`, and `proxy.golang.org`
* **Setup script requests**: Claude Code connects to the agent proxy when it launches, after the [setup script](#setup-scripts) has run
* **Claude Code's telemetry export**: Claude Code sends its [telemetry export](https://code.claude.com/docs/en/monitoring-usage.md#telemetry-from-cloud-sessions-and-claude-tag) itself rather than through a command it runs, and that request doesn't go through the agent proxy

### Select an environment from the CLI

Run `/remote-env` in your terminal to choose the default environment for cloud sessions you create from the CLI, such as [`claude --cloud`](https://code.claude.com/docs/en/claude-code-on-the-web#from-terminal-to-cloud). The command opens a picker of your existing environments and saves your choice to the `remote.defaultEnvironmentId` key in your [user settings](https://code.claude.com/docs/en/settings.md#where-settings-live), so it applies in every project on your machine until you change it, unless the same key is set at a higher-precedence [settings layer](https://code.claude.com/docs/en/settings.md#settings-precedence), such as a repo's project settings.

A [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments) ID, which has the form `ccpool_...`, follows a stricter source rule. See [`remote.defaultEnvironmentId`](https://code.claude.com/docs/en/settings-reference#remote-defaultenvironmentid) for the settings layers Claude Code honors it from.

`/remote-env` only sets the default: it doesn't start a session, and it can't add or edit environments. Manage them from the [environment selector](#configure-your-environment).

### Archive an environment

To archive one of your own environments, open it for editing, then select **Archive environment** and confirm. If the environment is [shared with your organization](#organization-shared-environments), an Owner archives it from the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings) instead, so ask an Owner unless you are one.

Archiving affects new sessions, not running ones:

* Sessions already running in the environment continue to work.
* The environment disappears from the selector and from `/remote-env`, so you can't pick it for new sessions.
* Network secrets on the environment stay attached in its running sessions. Delete any you no longer want before you archive.
* No new session can start in an archived environment, on any surface:
  * **Saved CLI default**: if the environment was your saved [CLI default](#select-an-environment-from-the-cli), Claude Code starts CLI cloud sessions in the Anthropic-hosted environment when your list has one. Otherwise, it starts them in the first environment in your list that isn't a [Remote Control bridge environment](#the-default-environment).
  * **Configured explicitly**: anything configured with the environment explicitly, such as a [cloud scheduled task](https://code.claude.com/docs/en/routines.md#environments-and-network-access), can't start new sessions in it. Point it at another environment.

When you no longer need an Anthropic-hosted environment, archive it. Neither the environment dialog nor the **Cloud environments** admin page has an option to delete an Anthropic-hosted environment. If the environment is [self-hosted](https://code.claude.com/docs/en/self-hosted-environments), an Owner can delete it from the **Cloud environments** page in admin settings. If you aren't an Owner, ask one to delete it.

### Organization-shared environments

On Team and Enterprise plans, an Owner can create cloud environments that are shared with every member of the organization. The same role manages everything else on the **Cloud environments** admin page, including [self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments); the Admin role can't open the page. The full list of roles that can open it is the one for [managing server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md#access-control).

Shared environments appear in each member's [environment selector](#configure-your-environment) under an **Organization** heading, after the member's own environments under **Personal**, so a team can standardize on one configuration instead of each member recreating it. Selecting a shared environment's settings icon there opens a read-only summary of its configuration for every member, Owners included.

An Owner makes an environment available to the organization in one of two ways:

* **Create a shared environment**: use the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings), which is also where Owners edit and archive shared environments. Each one has a name, a [network access level](#access-levels), [environment variables](#set-environment-variables) in `.env` format, and a [setup script](#setup-scripts).
* **Share a personal environment**: open one of your own environments for editing in the environment selector, then share it from the **Who can use it** row. The environment keeps its ID, so sessions and scheduled tasks that already use it aren't affected, and every member can then see it and start sessions in it.

Owners choose the organization's [default environment](#the-default-environment) separately, at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

To give a shared environment's sessions a key they can't read, add a [network secret](#add-network-secrets) when you edit the environment on the **Cloud environments** page. Don't include secrets in its variables, because every member's sessions read them.

### Set the environment a Claude Tag channel uses

In [Claude Tag](https://claude.com/docs/claude-tag/overview) channels, Claude works as your organization's shared identity, not as any member, so channel sessions use organization-level environments only, either shared environments or [self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments). To give a channel a toolchain that isn't [pre-installed](#installed-tools), such as .NET, an Owner can create a [shared environment](#organization-shared-environments) from the **Cloud environments** admin page with a [setup script](#setup-scripts) that installs it. Point the channel at an environment in one of two ways:

* Set a shared or self-hosted environment as the organization's [default environment](#the-default-environment) at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
* [Pin one to a channel](https://claude.com/docs/claude-tag/admins/troubleshooting#channel-sessions-use-the-wrong-environment-or-can%E2%80%99t-find-one) in the Claude Tag admin settings.

## Network access

Each environment sets one network access level, which controls the outbound connections its sessions can make. The default level, **Trusted**, allows package registries and other [allowlisted domains](#default-allowed-domains); **Custom** takes your own domain list.

To change an environment's network access, [open it for editing](#configure-your-environment) and use the **Network access** selector in the dialog. A [shared environment](#organization-shared-environments) opens read-only there, so an Owner changes its network access from the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings) instead. The control that opens the selector appears on the app surfaces listed under [The Default environment](#the-default-environment) and in the [cloud scheduled task editor](https://code.claude.com/docs/en/routines.md#environments-and-network-access). Personal environments don't have a separate page in your claude.ai account settings.

When you change an Anthropic-hosted environment's network access, its existing sessions follow the new setting within about a minute, for requests that go through the session's [network allowlist](#access-levels). You don't need to start a new session.

> [!NOTE]
>
> MCP connectors you enable on a session or scheduled task work without adding their hosts to **Allowed domains**, because connector traffic travels through Anthropic's servers rather than the session's network. This relies on the same Anthropic-bound channel noted under [Security and isolation](https://code.claude.com/docs/en/claude-code-on-the-web.md#security-and-isolation). Turn off any connector you don't need to limit which tools Claude can reach.

### Access levels

The **Network access** field in the [environment dialog](#configure-your-environment) takes one of four levels:

| Level | Outbound connections |
| :- | :- |
| **None** | No outbound network access through the session's network |
| **Trusted** | [Allowlisted domains](#default-allowed-domains) only: package registries, GitHub, cloud SDKs |
| **Full** | Any domain |
| **Custom** | Your own allowlist, optionally including the defaults |

Whichever level you pick, sessions can still reach these, because each one takes a path that doesn't go through the session's network allowlist:

* GitHub, through its [separate proxy](#github-proxy)
* [MCP connectors](#network-access) you enable, whose traffic travels through Anthropic's servers
* The hosts you listed on the environment's [network secrets](#add-network-secrets), except the [hosts that never get the secret](#requests-that-never-get-the-credential)
* The Anthropic API, for Claude Code's own requests, even at **None**, as noted under [Security and isolation](https://code.claude.com/docs/en/claude-code-on-the-web.md#security-and-isolation)

### Allow specific domains

To allow domains that aren't in the Trusted list, select **Custom** in the environment's network access settings, then list one domain per line in the **Allowed domains** field. This example allows three hosts an internal project might need.

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

Sessions in this environment can now reach `api.example.com`, any subdomain of `internal.example.com`, and `registry.example.com`, and no other domains through the session's network. [GitHub traffic](#github-proxy), [MCP connector traffic](#network-access), and requests to the hosts of the environment's [network secrets](#add-network-secrets), other than the [hosts that never get the secret](#requests-that-never-get-the-credential), don't go through this allowlist. A leading `*.` matches every subdomain. To keep the [Trusted domains](#default-allowed-domains) too, check **Also include default list of common package managers**; leave it unchecked to allow only what you list.

If your organization uses [artifacts](https://code.claude.com/docs/en/artifacts.md#availability), you don't need `*.frame.claudeusercontent.com` in the list for sessions to read them. When the list leaves that host out, Claude Code reads artifact content through the session's connection to Anthropic instead. Keep the host in an allowlist in two situations:

* **Sessions in this environment open another organization's public artifacts**: Claude Code fetches those from the host directly, so add it to this list.
* **You're configuring the local CLI or a self-hosted runner**: keep the host in that allowlist. See [network access requirements](https://code.claude.com/docs/en/network-config.md#network-access-requirements) and the self-hosted [network requirements](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#network-requirements).

Each environment has its own allowed-domains list; there's no organization-level allowlist that admins can push to every member's environments. No [server-managed setting](https://code.claude.com/docs/en/server-managed-settings.md) adds domains to an environment's network allowlist either. To give a team one standard list, an Owner can create an [organization-shared environment](#organization-shared-environments) with **Custom** network access and that list.

### GitHub proxy

In Anthropic-hosted environments, all GitHub operations go through a dedicated proxy that keeps your real GitHub credentials outside the session's VM, independent of the environment's [access level](#access-levels). Sessions in a self-hosted environment authenticate git operations with credentials your deployment provides; [Configure git](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#configure-git) covers the options, including per-session minted credentials and an opt-in to this same proxy. The proxy provides:

* **Git credentials**: the git client inside the VM uses a scoped credential, which the proxy verifies and swaps for your actual GitHub token.
* **API requests**: requests from the built-in GitHub tools, and from `gh` under the [`proxy-injected` placeholder](#work-with-github-issues-and-pull-requests), go out with your real credentials substituted.
* **Push restrictions**: the proxy rejects branch deletions and pushes of anything other than a branch, such as a tag. It doesn't limit which branches a push can update. To do that, use branch protection rules or rulesets on GitHub.
* **Repository scope**: the proxy serves GitHub API requests for the repositories attached to the session. An API request for another repository gets a 403 whose message starts with `GitHub access to` and contains `is not enabled for this session`. A source archive you fetch over a `github.com/{owner}/{repo}/archive/` or `codeload.github.com` URL gets that same 403 when the repository isn't attached, even a public one.
* **GraphQL restrictions**: the proxy rejects requests to GitHub's GraphQL endpoint with a 403 whose message starts with `GitHub GraphQL is not available from Claude Code sessions` and names the REST fallback, `gh api repos/{owner}/{repo}/...`. `gh` subcommands that use GraphQL, such as `gh pr` and `gh issue`, get the same 403. The restriction applies to every request through the proxy regardless of the credentials you supply, so a `GH_TOKEN` you set gets the same 403. Claude can't reach GitHub APIs that exist only in GraphQL, such as Projects v2, through the proxy.

Committed files from public repositories arrive through `raw.githubusercontent.com`, which the [security proxy](#security-proxy) handles instead. That domain is in the default [Trusted list](#default-allowed-domains), so those files stay reachable unless the environment's [access level](#access-levels) excludes it.

### Security proxy

Cloud sessions in Anthropic-hosted environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes; in a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#default-deny-egress), outbound traffic leaves through your own network boundary instead. All outbound internet traffic from an Anthropic-hosted session passes through this proxy, which provides:

* Protection against malicious requests
* Rate limiting and abuse prevention

## What's available in cloud sessions

In Anthropic-hosted environments, each session gets a fresh virtual machine (VM) running Ubuntu 24.04 on x86\_64, regardless of your own operating system and CPU architecture, with your repository cloned and common toolchains pre-installed. When a dependency provides precompiled binaries, such as Ruby gems with native extensions or prebuilt Python wheels, use its x86\_64 Linux build to match the VM. This section covers the Anthropic-hosted defaults, the built-in GitHub tools, how to [run tests and services](#run-tests-start-services-and-add-packages), the [resource limits](#resource-limits) each VM gets, and the [time limits](#time-limits) on long-running work.

> [!NOTE]
>
> Sessions your organization routes to a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments) run on your own runners instead, with the tools your runner image provides.

### What carries over from your setup

> [!NOTE]
>
> Of the repository configuration in this table, a cloud thread in a [project](https://code.claude.com/docs/en/claude-projects.md) loads only the repository root's `CLAUDE.md`, `.claude/CLAUDE.md`, and `.claude/rules/` files that aren't [path-specific](https://code.claude.com/docs/en/memory.md#path-specific-rules). See [What threads pick up from your repositories](https://code.claude.com/docs/en/claude-projects.md#what-threads-pick-up-from-your-repositories).

Cloud sessions start from a fresh clone of your repository. Anything you commit to the repo is available. Anything you've installed or configured only on your own machine isn't available in the session. Your organization's policy arrives separately through [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md).

| | Available in cloud sessions | Why |
| :- | :- | :- |
| Your repo's `CLAUDE.md` | Yes | Part of the clone |
| Your repo's `.claude/settings.json` hooks and permission rules | Yes, in a session with one repository | Part of the clone. For a session with several repositories, see [which settings it reads](https://code.claude.com/docs/en/settings.md#settings-in-cloud-sessions) |
| Your repo's `.mcp.json` MCP servers | Yes, in a session with one repository | Part of the clone, found from the session's working directory. For a self-hosted environment, see [which repository's settings apply](https://code.claude.com/docs/en/self-hosted-environments-configuration.md#repository-settings-in-sessions-with-several-repositories) |
| Your repo's `.claude/rules/` | Yes | Part of the clone |
| Your repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/` | Yes | Part of the clone |
| Plugins and marketplaces declared in your repo's `.claude/settings.json` | No | A cloud session doesn't install the plugins a repository turns on under [`enabledPlugins`](https://code.claude.com/docs/en/settings-reference#enabledplugins), including ones from the marketplaces it lists under [`extraKnownMarketplaces`](https://code.claude.com/docs/en/settings-reference#extraknownmarketplaces) |
| Your organization's [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md) | Yes, except in [Claude Tag](https://claude.com/docs/claude-tag/overview) sessions | Fetched from Anthropic's servers when the session starts. See [Surface coverage](https://code.claude.com/docs/en/model-config.md#surface-coverage) for how `availableModels` is enforced in cloud sessions. Settings deployed to your device through MDM or managed settings files don't apply, because the session runs on an Anthropic-managed VM; in a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments), sessions also read the managed settings file in the runner image, per [how Claude Code combines managed sources](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources) |
| Your user `~/.claude/CLAUDE.md` | No | Lives on your machine, not in the repo. See [Add personal preferences without committing to the repo](#add-personal-preferences-without-committing-to-the-repo) |
| Your user `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/commands/` | No | Live on your machine, not in the repo. Commit them to the repo's `.claude/` directory instead. Cloud sessions automatically load [skills you enable on claude.ai](https://code.claude.com/docs/en/skills.md#skills-in-cowork-and-cloud-sessions) |
| Plugins enabled only in your user settings | No | User-scoped `enabledPlugins` lives in `~/.claude/settings.json` on your machine |
| MCP servers you added with `claude mcp add` at the default local scope or the user scope | No | Those write to `~/.claude.json` on your machine, not the repo. Add the server with `claude mcp add --scope project`, which writes the repo's [`.mcp.json`](https://code.claude.com/docs/en/mcp#project-scope), and commit that file. A session with one repository loads it |
| Transport variables in your repo's `.claude/settings.json` `env` block, such as `NODE_EXTRA_CA_CERTS` and the [mTLS client certificate variables](https://code.claude.com/docs/en/network-config.md#mtls-authentication) | No | The hosting environment manages the session's API connection, so Claude Code ignores these keys and notes each ignored key in the session's debug log |
| API keys and tokens for services Claude calls | In an Anthropic-hosted environment, as [network secrets](#add-network-secrets) | You add the key once on the environment and the agent proxy attaches it to requests for the hosts you list. A key the agent proxy [can't attach](#requests-that-never-get-the-credential) stays in an environment variable |
| Interactive auth like AWS SSO | No | Not supported. SSO requires browser-based login that can't run in a cloud session |

To make your own configuration available in cloud sessions, commit it to the repo.

Anyone who uses the environment can read its environment variables and setup script. The dialog's note under **Environment variables** says so and warns against putting secrets there. In an Anthropic-hosted environment, store a key the agent proxy can attach as a [network secret](#add-network-secrets) instead.

#### Add personal preferences without committing to the repo

In an Anthropic-hosted environment, add a [setup script](#setup-scripts) that writes `~/.claude/CLAUDE.md` for preferences you'd rather not put in a shared repository. Claude Code loads that file as [user instructions](https://code.claude.com/docs/en/memory.md#choose-where-to-put-claude-md-files) in the session. This example sets a commit-message preference:

```bash theme={null}
#!/bin/bash
mkdir -p ~/.claude
cat > ~/.claude/CLAUDE.md <<'EOF'
Use conventional commit messages.
EOF
```

Put the script on one of your own environments rather than a [shared one](#organization-shared-environments).

Run `/context` in your next cloud session and confirm `/root/.claude/CLAUDE.md` appears under **Memory files**.

### Installed tools

Cloud sessions come with common language runtimes, build tools, and databases pre-installed. The table below summarizes what's included by category.

| Category | Included |
| :- | :- |
| **Python** | Python 3.x with pip, poetry, uv, black, mypy, pytest, ruff |
| **Node.js** | 20, 21, and 22, with npm, yarn, pnpm, bun¹, eslint, prettier, chromedriver |
| **Ruby** | 3.1, 3.2, 3.3 with gem, bundler, rbenv |
| **PHP** | 8.3 with Composer |
| **Java** | OpenJDK 21 with Maven and Gradle |
| **Go** | Go with module support |
| **Rust** | rustc and cargo |
| **C/C++** | GCC, Clang, cmake, ninja, conan |
| **Docker** | docker, dockerd, docker compose |
| **Databases** | PostgreSQL 16, Redis 7.0 |
| **Utilities** | git, gh, jq, yq, ripgrep, tmux, vim, nano |

¹ Bun is installed but has known [proxy compatibility issues](#install-dependencies-with-a-sessionstart-hook) for package fetching.

To get the versions of most of the tools in this table, ask Claude to run `check-tools` in a cloud session. It's a shell command installed on the session VM, not a command you type with `/`; you ask Claude because [Claude runs all VM commands for you](#run-tests-start-services-and-add-packages). For a tool it doesn't report, such as Ruby, PHP, bun, PostgreSQL, or Redis, ask Claude to run the tool's own version command, for example `psql --version`.

Node.js versions are installed at `/opt/node20`, `/opt/node21`, and `/opt/node22`, with 22 on `PATH` by default. To work with a different version, ask Claude to prepend that version's `bin` directory, such as `/opt/node20/bin`, to `PATH`.

Toolchains outside this list, such as the .NET SDK, aren't pre-installed even when their package registries are on the [default allowlist](#default-allowed-domains). Install them with a [setup script](#setup-scripts).

### Work with GitHub issues and pull requests

Cloud sessions include built-in GitHub tools that let Claude read issues, list pull requests, fetch diffs, and post comments without any setup. These tools authenticate through the [GitHub proxy](#github-proxy) using whichever method you configured under [GitHub authentication options](https://code.claude.com/docs/en/claude-code-on-the-web.md#github-authentication-options), so your token never enters the container.

You can set `GH_TOKEN` or `GITHUB_TOKEN` yourself in [environment settings](#set-environment-variables), or leave both unset and let the [GitHub proxy](#github-proxy) authenticate for you:

* If you set a token, it passes through to the container unchanged, so your scripts and GitHub's [`gh` CLI](https://cli.github.com) use it directly.
* If you set neither and the [GitHub proxy](#github-proxy) is handling authentication for your session, both variables read as the placeholder string `proxy-injected` in the commands Claude runs, and the proxy substitutes your real credentials on outbound GitHub requests. `gh api` calls for attached repositories work without a token of your own, but a script that reads `GITHUB_TOKEN` directly gets the placeholder, not a usable token.

A token you set is an ordinary environment variable, so anyone who uses the environment can read it; the proxy path keeps the credential out of the environment configuration and the session VM.

To check which case applies to your session, ask Claude to run `echo $GH_TOKEN`.

GitHub's [`gh` CLI](https://cli.github.com) is pre-installed. If you need a GitHub operation the built-in tools don't cover, ask Claude to call the REST API with `gh api`. `gh` subcommands that use the REST API, such as `gh workflow list`, work too. The proxy [rejects subcommands that use GraphQL](#github-proxy), such as `gh pr` and `gh issue`. `gh` reads `GH_TOKEN` automatically, so you don't need to run `gh auth login`.

### Link output back to the session

Each cloud session has a transcript URL on claude.ai, and the session can read its own ID from the `CLAUDE_CODE_REMOTE_SESSION_ID` environment variable. Use this to put a traceable link in PR bodies, commit messages, Slack posts, or generated reports so a reviewer can open the run that produced them.

Commits that Claude creates in a cloud session include a `Claude-Session: <url>` git trailer, and PR bodies include the session URL on its own line. To omit the trailer and the PR-body link, set [`attribution.sessionUrl`](https://code.claude.com/docs/en/settings-reference#attribution-sessionurl) to `false`.

To include the session link in something other than a commit or PR, such as a Slack message Claude posts or a report file it writes, have Claude run the following command and use its output. The command converts the `cse_` prefix in the environment variable's value to the `session_` prefix that the transcript URL expects:

```bash theme={null}
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/#cse_/session_}"
```

### Run tests, start services, and add packages

You don't get a shell into the session VM. Claude runs every command for you, so phrase the tasks in this section as requests in your prompt.

#### Run tests

Claude runs tests as part of working on a task. Ask for it in your prompt, like "fix the failing tests in `tests/`" or "run pytest after each change." Test runners that come with the [pre-installed toolchains](#installed-tools), like pytest and cargo test, work without additional setup. A runner your project declares as a dependency, like jest, installs with your dependencies.

#### Start services

PostgreSQL and Redis are pre-installed but not running by default. Ask Claude to start whichever you need; the commands it runs are:

```bash theme={null}
service postgresql start
```

```bash theme={null}
service redis-server start
```

Docker is available for running containerized services. Ask Claude to run `docker compose up` to start your project's services. Network access to pull images follows your environment's [access level](#access-levels), and the [Trusted defaults](#default-allowed-domains) include Docker Hub and other common registries.

If your images are large or slow to pull, add `docker compose pull` or `docker compose build` to your [setup script](#setup-scripts). The [environment cache](#environment-caching) keeps the pulled images, so each new session has them on disk. The cache stores files only, not running processes, so Claude still starts the containers each session.

#### Add packages

To add packages that aren't pre-installed, use a [setup script](#setup-scripts). The [environment cache](#environment-caching) keeps what the script installs, so packages you install there are available at the start of every session without reinstalling each time. You can also ask Claude to install packages mid-session, but those installs don't carry over to other sessions.

### Resource limits

Cloud sessions in Anthropic-hosted environments run with approximate resource ceilings that may change over time:

* 4 vCPUs
* 16 GB of RAM
* 30 GB of disk

The VM may stop tasks that need significantly more memory, such as large build jobs or memory-intensive tests. For workloads beyond these limits, use [Remote Control](https://code.claude.com/docs/en/remote-control.md) to run Claude Code on your own hardware, or run cloud sessions in a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments) on compute your organization operates.

### Time limits

In Anthropic-hosted environments, these time limits apply to long-running work in a cloud session, such as a build, an install, or a test run. Each entry links to the section that defines the limit.

* **Commands Claude runs**: a cloud environment doesn't set its own command timeout, so the Bash tool's defaults apply. Claude waits 2 minutes for a foreground command by default and can ask for up to 10 minutes.

  When a command reaches its [timeout](https://code.claude.com/docs/en/tools-reference.md#timeout-and-output-limits), Claude Code [moves it to the background](https://code.claude.com/docs/en/tools-reference.md#foreground-commands-that-move-to-the-background) instead of stopping it, unless the command starts with `sleep`. A command moved this way can keep running for up to 30 more minutes before Claude Code stops it at its [background time limit](https://code.claude.com/docs/en/tools-reference.md#time-limit-for-background-commands). Setting `BASH_DEFAULT_TIMEOUT_MS` above `1800000` milliseconds lengthens that limit as well as the foreground default.
* **SessionStart hooks**: Claude Code cancels a `command` hook after 600 seconds unless you set [`timeout`](https://code.claude.com/docs/en/hooks#common-fields), in seconds, on the hook entry. Claude Code doesn't enforce the timeout on a hook you run with [`async: true`](https://code.claude.com/docs/en/hooks#run-hooks-in-the-background).
* **Setup script**: a script that takes longer than roughly five minutes isn't cached. [Script requirements](#script-requirements) covers how to stay under that.
* **Idle sessions**: after a few minutes without activity, a session's VM pauses with its files saved, and a paused VM can later be reclaimed. [Set environment variables](#set-environment-variables) describes what a session picks up in each case, and [Environment expired](https://code.claude.com/docs/en/claude-code-on-the-web.md#environment-expired) covers how to reopen a session whose VM was reclaimed.

To raise the command timeouts for an environment's sessions, add [`BASH_DEFAULT_TIMEOUT_MS` and `BASH_MAX_TIMEOUT_MS`](https://code.claude.com/docs/en/env-vars#variables) to its [environment variables](#set-environment-variables). Both take milliseconds. For example, `BASH_DEFAULT_TIMEOUT_MS=600000` makes 10 minutes the default.

## Setup scripts

A setup script is a Bash script that runs when a new cloud session starts, before Claude Code launches. Use setup scripts to install dependencies, configure tools, or fetch anything the session needs that isn't pre-installed.

Scripts run as root on Ubuntu 24.04, so `apt install` and most language package managers work.

### Add a setup script

To add a setup script to your own environment, you can type or paste it, or load a text file such as `setup.sh`. [Add or edit the environment](#configure-your-environment) and select the **Setup script** row. Enter the script in the box that opens, or select **Choose file** to replace the box's contents with the text of a file up to 64 KB. Then select **Add environment** or **Save changes**.

This example installs [ShellCheck](https://www.shellcheck.net/), which isn't pre-installed.

```bash theme={null}
#!/bin/bash
apt update && apt install -y shellcheck
```

### Script requirements

A setup script has three constraints to write around:

* **Exit zero**: if the script exits non-zero, the session fails to start. Append `|| true` to non-critical commands so an intermittent install failure doesn't block the session.
* **Finish within five minutes**: keep the script's total runtime under roughly five minutes so the [environment cache](#environment-caching) can build. When setup takes longer than that, the environment isn't cached. Run independent installs in parallel with `&` and `wait`, and move any single download that won't fit into a [SessionStart hook](#setup-scripts-vs-sessionstart-hooks) that launches it in the background. If new sessions stall or fail during setup, see [New sessions hang or time out during setup](https://code.claude.com/docs/en/web-quickstart.md#new-sessions-hang-or-time-out-during-setup).
* **Network access for installs**: package installs need to reach registries. The default **Trusted** level covers [common package registries](#default-allowed-domains) including npm, PyPI, RubyGems, and crates.io; with **None** network access, installs fail.

### Environment caching

The setup script runs the first time you start a session in an environment. When setup completes within [roughly five minutes](#script-requirements), Anthropic snapshots the filesystem and reuses that snapshot as the starting point for later sessions. New sessions start with your dependencies, tools, and Docker images already on disk, and skip the setup script step. This keeps startup fast even when the script installs large toolchains or pulls container images. If setup takes longer than roughly five minutes, the environment isn't cached.

The cache is a filesystem snapshot, so it keeps what the setup script writes to disk and loses anything that was only running. Packages you install, Docker images you pull, and files you write all carry over. A database the script started, a `docker compose up` stack, or any other background process doesn't; start those per session by asking Claude or with a [SessionStart hook](#setup-scripts-vs-sessionstart-hooks).

The setup script runs again to rebuild the cache when you change the environment's setup script or allowed network hosts, and when the cache reaches its expiry after roughly seven days. In an Anthropic-hosted environment, the setup script doesn't run when a session's VM is [restored after being idle](#set-environment-variables), so a change to the script reaches an existing session only when its VM was [reclaimed](https://code.claude.com/docs/en/claude-code-on-the-web.md#environment-expired) and is rebuilt. To apply a change right away, run the commands in the session or start a new session.

You don't need to enable caching or manage snapshots yourself.

### Setup scripts vs. SessionStart hooks

Use a setup script to provision the VM itself: toolchains and CLI tools that aren't [pre-installed](#installed-tools). Use a [SessionStart hook](https://code.claude.com/docs/en/hooks.md#sessionstart) for project setup that should run everywhere, cloud and local, like `npm install`.

Setup scripts and SessionStart hooks run in a fixed order when a cloud session starts. The table compares where you configure them, when they run, and where they run.

| | Setup scripts | SessionStart hooks |
| - | - | - |
| **Where you configure them** | The environment dialog at [claude.ai/code](https://claude.ai/code), plus the **Cloud environments** admin page for [shared environments](#organization-shared-environments) | A [settings file](https://code.claude.com/docs/en/settings.md#where-settings-live) such as your repo's `.claude/settings.json`; see [What carries over from your setup](#what-carries-over-from-your-setup) for which files reach a cloud session |
| **When they run** | Before Claude Code launches, skipped when a [cached environment](#environment-caching) exists | After Claude Code launches, on every session including resumed |
| **Where they run** | Cloud sessions only | Local and cloud sessions |

If you have SessionStart hooks in your user-level `~/.claude/settings.json`, don't expect them in the cloud. User-level settings stay on your machine. Which other hooks run depends on where the session runs:

* **Anthropic-hosted environment**: Claude Code runs hooks from your organization's [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md) and, outside a [project](https://code.claude.com/docs/en/claude-projects.md#what-threads-pick-up-from-your-repositories) thread, from the repository. [Claude Tag](https://claude.com/docs/claude-tag/overview) sessions don't receive server-managed settings, so hooks from server-managed settings don't run there.
* **[Self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments-configuration.md#permissions-and-tool-approval)**: Claude Code also runs the hooks the operator seeded from the runner host's `~/.claude/`, and the hooks in the runner image's managed settings file when that file is one of the [managed sources Claude Code applies](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources).

### Install dependencies with a SessionStart hook

To install dependencies only in cloud sessions outside a [project](https://code.claude.com/docs/en/claude-projects.md#what-threads-pick-up-from-your-repositories)'s threads, pair a SessionStart hook with a script that checks where it's running.

First, add a SessionStart hook to your repo's `.claude/settings.json`. This configuration tells Claude Code to run `scripts/install_pkgs.sh` from your repository whenever a session starts or resumes:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

The `matcher` limits the hook to the `startup` and `resume` events, and `$CLAUDE_PROJECT_DIR` resolves to the repository root, so the hook finds the script regardless of the session's working directory.

Next, create the script at `scripts/install_pkgs.sh`. It exits immediately outside the cloud, then installs your dependencies. It skips `npm install` while `package.json`, `package-lock.json`, and the script itself are unchanged since the last successful install:

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

cd "$CLAUDE_PROJECT_DIR" || exit 1
hashes=node_modules/.install_pkgs.sha256

if ! sha256sum --check --status "$hashes" 2>/dev/null; then
  # Delete the old hashes first, so a failed install runs again next time
  rm -f "$hashes"
  if npm install; then
    sha256sum scripts/install_pkgs.sh package.json package-lock.json > "$hashes" || rm -f "$hashes"
  fi
fi

# pip skips requirements that are already satisfied
pip install -r requirements.txt
exit 0
```

The `CLAUDE_CODE_REMOTE` check is what scopes the install to cloud sessions: the session VM's environment carries that variable as `true`, it's never `true` locally, so on your laptop the script exits before installing anything.

To confirm `npm install` succeeded, start a cloud session and ask Claude to show `node_modules/.install_pkgs.sha256`. The file lists a hash for each of the three files. If the file is missing, ask Claude to run `npm install` and report the error.

> [!NOTE]
>
> If `npm install` reads other files, such as a workspace's `package.json`, an `.npmrc`, or your `postinstall` script's inputs, add them to the `sha256sum` command that saves the hashes. Otherwise, you keep the old packages after one of those files changes.

#### Limitations in cloud sessions

SessionStart hooks behave the same in the cloud as locally, with these caveats:

* **One repository per session**: in an Anthropic-hosted environment, a session with several repositories doesn't load hooks from any repository's `.claude/settings.json`, so a SessionStart hook you define there doesn't run. Install dependencies for those sessions with a [setup script](#setup-scripts) instead. For a self-hosted environment, see [which repository's settings apply](https://code.claude.com/docs/en/self-hosted-environments-configuration.md#repository-settings-in-sessions-with-several-repositories).
* **Not in a project's cloud threads**: a cloud thread in a [project](https://code.claude.com/docs/en/claude-projects.md#what-threads-pick-up-from-your-repositories) doesn't run hooks from a repository's `.claude/settings.json`, whatever the number of repositories. In an Anthropic-hosted environment, install dependencies for threads with a [setup script](#setup-scripts). In a self-hosted environment, use a hook in the [runner host's settings](https://code.claude.com/docs/en/self-hosted-environments-configuration.md#repository-settings-in-sessions-with-several-repositories) instead.
* **No cloud-only scoping**: hooks run in both local and cloud sessions. To skip local execution, exit early unless the `CLAUDE_CODE_REMOTE` environment variable is `true`, the way the [dependency install script](#install-dependencies-with-a-sessionstart-hook) does.
* **Requires network access**: install commands need to reach package registries. If your environment uses **None** network access, these hooks fail. The [default allowlist](#default-allowed-domains) under **Trusted** covers npm, PyPI, RubyGems, and crates.io.
* **Proxy compatibility**: in Anthropic-hosted environments, all outbound traffic passes through a [security proxy](#security-proxy), and some package managers don't work correctly with it; Bun is a known example. In a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#default-deny-egress), outbound traffic goes through your own network boundary instead.
* **Adds startup latency**: hooks run each time a session starts or resumes, unlike setup scripts which benefit from [environment caching](#environment-caching). Keep install scripts fast by skipping work that's already done, the way the [dependency install script](#install-dependencies-with-a-sessionstart-hook) does.

To customize the base image, use a setup script to install what you need on top of the [provided image](#installed-tools), or run your own image as a container alongside Claude with `docker compose`. Replacing the base image entirely isn't supported yet.

## Default allowed domains

With **Trusted** network access, sessions can reach the following domains by default. Domains marked with `*` indicate wildcard subdomain matching, so `*.gcr.io` allows any subdomain of `gcr.io`.

> **Anthropic services**
>
> * api.anthropic.com
> * docs.claude.com
> * platform.claude.com
> * code.claude.com
> * claude.ai
> * claude.com
> * support.claude.com
> * anthropic.com
> * [www.anthropic.com](http://www.anthropic.com)

> **Version control**
>
> * github.com
> * [www.github.com](http://www.github.com)
> * api.github.com
> * npm.pkg.github.com
> * raw\.githubusercontent.com
> * pkg-npm.githubusercontent.com
> * objects.githubusercontent.com
> * release-assets.githubusercontent.com
> * codeload.github.com
> * avatars.githubusercontent.com
> * camo.githubusercontent.com
> * gist.github.com
> * gitlab.com
> * [www.gitlab.com](http://www.gitlab.com)
> * registry.gitlab.com
> * bitbucket.org
> * [www.bitbucket.org](http://www.bitbucket.org)
> * api.bitbucket.org

> **Container registries**
>
> * registry-1.docker.io
> * auth.docker.io
> * index.docker.io
> * hub.docker.com
> * [www.docker.com](http://www.docker.com)
> * production.cloudflare.docker.com
> * production.cloudfront.docker.com
> * download.docker.com
> * gcr.io
> * \*.gcr.io
> * ghcr.io
> * mcr.microsoft.com
> * \*.data.mcr.microsoft.com
> * public.ecr.aws

> **Cloud platforms**
>
> * cloud.google.com
> * accounts.google.com
> * gcloud.google.com
> * \*.googleapis.com
> * storage.googleapis.com
> * compute.googleapis.com
> * container.googleapis.com
> * azure.com
> * portal.azure.com
> * microsoft.com
> * [www.microsoft.com](http://www.microsoft.com)
> * \*.microsoftonline.com
> * packages.microsoft.com
> * dotnet.microsoft.com
> * dot.net
> * visualstudio.com
> * dev.azure.com
> * \*.amazonaws.com
> * \*.api.aws
> * oracle.com
> * [www.oracle.com](http://www.oracle.com)
> * java.com
> * [www.java.com](http://www.java.com)
> * java.net
> * [www.java.net](http://www.java.net)
> * download.oracle.com
> * yum.oracle.com
> * \*.r2.cloudflarestorage.com

> **JavaScript and Node package managers**
>
> * registry.npmjs.org
> * [www.npmjs.com](http://www.npmjs.com)
> * [www.npmjs.org](http://www.npmjs.org)
> * npmjs.com
> * npmjs.org
> * yarnpkg.com
> * registry.yarnpkg.com
> * jsr.io
> * npm.jsr.io

> **Python package managers**
>
> * pypi.org
> * [www.pypi.org](http://www.pypi.org)
> * files.pythonhosted.org
> * pythonhosted.org
> * test.pypi.org
> * pypi.python.org
> * pypa.io
> * [www.pypa.io](http://www.pypa.io)

> **Ruby package managers**
>
> * rubygems.org
> * [www.rubygems.org](http://www.rubygems.org)
> * api.rubygems.org
> * index.rubygems.org
> * ruby-lang.org
> * [www.ruby-lang.org](http://www.ruby-lang.org)
> * rubyforge.org
> * [www.rubyforge.org](http://www.rubyforge.org)
> * rubyonrails.org
> * [www.rubyonrails.org](http://www.rubyonrails.org)
> * rvm.io
> * get.rvm.io

> **Rust package managers**
>
> * crates.io
> * [www.crates.io](http://www.crates.io)
> * index.crates.io
> * static.crates.io
> * rustup.rs
> * static.rust-lang.org
> * [www.rust-lang.org](http://www.rust-lang.org)

> **Go package managers**
>
> * proxy.golang.org
> * sum.golang.org
> * index.golang.org
> * golang.org
> * [www.golang.org](http://www.golang.org)
> * goproxy.io
> * pkg.go.dev

> **JVM package managers**
>
> * maven.org
> * repo.maven.org
> * central.maven.org
> * repo1.maven.org
> * repo.maven.apache.org
> * maven.google.com
> * jcenter.bintray.com
> * gradle.org
> * [www.gradle.org](http://www.gradle.org)
> * services.gradle.org
> * plugins.gradle.org
> * plugins-artifacts.gradle.org
> * kotlinlang.org
> * [www.kotlinlang.org](http://www.kotlinlang.org)
> * spring.io
> * repo.spring.io

> **Other package managers**
>
> * packagist.org (PHP Composer)
> * [www.packagist.org](http://www.packagist.org)
> * repo.packagist.org
> * nuget.org (.NET NuGet)
> * [www.nuget.org](http://www.nuget.org)
> * api.nuget.org
> * pub.dev (Dart/Flutter)
> * api.pub.dev
> * hex.pm (Elixir/Erlang)
> * [www.hex.pm](http://www.hex.pm)
> * cpan.org (Perl CPAN)
> * [www.cpan.org](http://www.cpan.org)
> * metacpan.org
> * [www.metacpan.org](http://www.metacpan.org)
> * api.metacpan.org
> * cocoapods.org (iOS/macOS)
> * [www.cocoapods.org](http://www.cocoapods.org)
> * cdn.cocoapods.org
> * haskell.org
> * [www.haskell.org](http://www.haskell.org)
> * hackage.haskell.org
> * swift.org
> * [www.swift.org](http://www.swift.org)

> **Linux distributions**
>
> * archive.ubuntu.com
> * security.ubuntu.com
> * ubuntu.com
> * [www.ubuntu.com](http://www.ubuntu.com)
> * \*.ubuntu.com
> * ppa.launchpad.net
> * launchpad.net
> * [www.launchpad.net](http://www.launchpad.net)
> * \*.nixos.org

> **Development tools and platforms**
>
> * dl.k8s.io (Kubernetes)
> * pkgs.k8s.io
> * k8s.io
> * [www.k8s.io](http://www.k8s.io)
> * releases.hashicorp.com (HashiCorp)
> * apt.releases.hashicorp.com
> * rpm.releases.hashicorp.com
> * archive.releases.hashicorp.com
> * hashicorp.com
> * [www.hashicorp.com](http://www.hashicorp.com)
> * repo.anaconda.com (Anaconda/Conda)
> * conda.anaconda.org
> * anaconda.org
> * [www.anaconda.com](http://www.anaconda.com)
> * anaconda.com
> * continuum.io
> * apache.org (Apache)
> * [www.apache.org](http://www.apache.org)
> * archive.apache.org
> * downloads.apache.org
> * eclipse.org (Eclipse)
> * [www.eclipse.org](http://www.eclipse.org)
> * download.eclipse.org
> * nodejs.org (Node.js)
> * [www.nodejs.org](http://www.nodejs.org)
> * developer.apple.com
> * developer.android.com
> * pkg.stainless.com
> * binaries.prisma.sh

> **Cloud services and monitoring**
>
> * http-intake.logs.datadoghq.com
> * \*.datadoghq.com
> * \*.datadoghq.eu
> * api.honeycomb.io

> **Content delivery and mirrors**
>
> * sourceforge.net
> * \*.sourceforge.net
> * packagecloud.io
> * \*.packagecloud.io
> * fonts.googleapis.com
> * fonts.gstatic.com

> **Schema and configuration**
>
> * json-schema.org
> * [www.json-schema.org](http://www.json-schema.org)
> * json.schemastore.org
> * [www.schemastore.org](http://www.schemastore.org)

> **Model Context Protocol**
>
> * \*.modelcontextprotocol.io

## Related resources

* [Cloud sessions reference](https://code.claude.com/docs/en/claude-code-on-the-web.md): start, manage, and share cloud sessions
* [Cloud sessions quickstart](https://code.claude.com/docs/en/web-quickstart.md): connect GitHub and start your first cloud session
* [Claude Tag](https://claude.com/docs/claude-tag/overview): sessions Claude starts from Slack run in the same environments
* [Cloud scheduled tasks](https://code.claude.com/docs/en/routines.md): scheduled runs use the same environments and network access levels
* [Remote Control](https://code.claude.com/docs/en/remote-control.md): run sessions on your own machine's network and files instead
* [Self-hosted environments](https://code.claude.com/docs/en/self-hosted-environments): run cloud sessions on your organization's own infrastructure
* [SessionStart hooks](https://code.claude.com/docs/en/hooks.md#sessionstart): repo-committed setup that runs in local and cloud sessions
* [Server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md): organization policy delivered from the admin console
