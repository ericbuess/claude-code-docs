> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure cloud environments

> Configure cloud environments for Claude Code cloud sessions: network access levels, environment variables, setup scripts, and environment caching.

<Note>
  Cloud environments require [Claude Code on the web](/docs/en/claude-code-on-the-web), which is in research preview for Pro, Max, and Team users, and for Enterprise users with [premium seats or Chat + Claude Code seats](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan).
</Note>

Each [cloud session](/docs/en/claude-code-on-the-web) runs in a cloud environment. You can configure an environment to allow or deny [network access](#access-levels), set environment variables for the session, and run a [setup script](#setup-scripts) before Claude starts working.

The same environments apply wherever you start a cloud session: [Claude Code on the web](/docs/en/claude-code-on-the-web), the terminal with [`claude --cloud`](/docs/en/claude-code-on-the-web#from-terminal-to-web), [Claude Tag](https://claude.com/docs/claude-tag/overview), [routines](/docs/en/routines), the [Claude mobile app](/docs/en/mobile), and the [Desktop app](/docs/en/desktop). Claude Tag sessions can't run in [self-hosted environments](/docs/en/self-hosted-environments) yet; the other surfaces can route to any environment.

<Info>
  [Remote Control](/docs/en/remote-control) sessions connect the web and mobile interfaces to a session on your own machine, which uses your machine's network and files, not a cloud environment. Claude Tag channel sessions use [shared environments](#organization-shared-environments) only.
</Info>

## The Default environment

Onboarding sets up the **Default** environment for you, whether you connect through [the web](/docs/en/web-quickstart#connect-github) or a CLI flow such as `/web-setup`; if web onboarding shows an environment form instead of creating the environment, keep the form's defaults to get the same **Default** environment. **Default** carries no configuration of its own:

* [**Trusted** network access](#access-levels): sessions reach package registries and other [allowlisted domains](#default-allowed-domains), and nothing else through the session's network.
* No other configuration: **Default** defines no environment variables or setup script, so sessions start with just the [pre-installed tools](#installed-tools).

With only **Default** available, every session runs in it. When you have more than one environment, sessions choose one per surface:

* On the web, the Desktop app, and the mobile app, sessions use the environment shown in the [selector](#configure-your-environment). An admin-set [organization default](#organization-shared-environments) fills the selection when you haven't picked one.
* From the CLI, sessions use your [`/remote-env` pick](#select-an-environment-from-the-cli), or fall back to your first available cloud environment. For a [self-hosted environment](/docs/en/self-hosted-environments), passing `--environment <environment-id>` with its `ccpool_` ID [when you dispatch a session](/docs/en/self-hosted-environments-testing#run-the-test-loop) overrides both for that invocation. The flag rejects Anthropic-hosted `env_` IDs, so use `/remote-env` to target those. The flag requires Claude Code v2.1.224 or later.

Configure an environment when the default isn't enough: when Claude needs to reach domains outside the [default allowlist](#default-allowed-domains), needs environment variables set for its sessions, or needs dependencies installed before it starts working.

## Configure your environment

Create, edit, and archive environments from the environment selector at [claude.ai/code](https://claude.ai/code), which you reach after [web onboarding](/docs/en/web-quickstart). Environments you create are personal to your account; [shared environments](#organization-shared-environments) created by your admins appear in the same selector. See [Installed tools](#installed-tools) for what's available without any configuration.

<Steps>
  <Step title="Open the environment selector">
    On [claude.ai/code](https://claude.ai/code), select the cloud icon showing the current environment's name, in the row above the message box. There's no settings page or direct URL for the selector.

    <Frame>
      <img src="https://mintcdn.com/claude-code/ZFId6l95856c5LSw/images/cloud-environment-selector.png?fit=max&auto=format&n=ZFId6l95856c5LSw&q=85&s=cc2813a5664519eaf5a89d793ce5af26" alt="The environment selector open above the message box at claude.ai/code. The cloud button showing the environment name Default sits in the row above the message box. The open menu lists a Local row with Download and Desktop only labels, a Cloud section where the Default environment is selected with a checkmark and shows a settings gear icon on hover, an Add cloud environment option, and a Remote Control section with setup instructions." width="1672" height="682" data-path="images/cloud-environment-selector.png" />
    </Frame>
  </Step>

  <Step title="Add or edit an environment">
    Select **Add cloud environment**, or hover over an existing environment and select the settings icon that appears on the right. The dialog includes the name, network access level, environment variables, and setup script.

    <Frame>
      <img src="https://mintcdn.com/claude-code/ZFId6l95856c5LSw/images/cloud-environment-dialog.png?fit=max&auto=format&n=ZFId6l95856c5LSw&q=85&s=30d4478b31d1f879f7ee287ddab32505" alt="The New cloud environment dialog. A Name field with the placeholder Default, a Network access selector set to Trusted with links to the network policy and access levels, an Environment variables box showing .env-format placeholder text with a note that values are visible to anyone using the environment, a Setup script box described as a Bash script that runs when a new session starts before Claude Code launches, and Cancel and Create environment buttons." width="874" height="1372" data-path="images/cloud-environment-dialog.png" />
    </Frame>
  </Step>
</Steps>

### Set environment variables

Environment variables use `.env` format, one `KEY=value` pair per line. Plain values don't need quotes, and if you quote a value with a matching pair, the quotes don't become part of the value. Quote a value that spans multiple lines or contains a `#`: in an unquoted value, `#` starts a comment and the rest of the line is dropped.

The following example defines three variables.

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

Each session copies the environment's values once, at startup, into ordinary environment variables that any command Claude runs can read. Because running sessions don't re-read the configuration, editing or adding variables affects sessions you start afterward; sessions already running keep the values they started with.

Anyone who uses the environment can read the values, and cloud environments have no dedicated secrets store, so don't add API keys or other credentials. If a session needs a credential anyway, see [What carries over from your setup](#what-carries-over-from-your-setup).

### Select an environment from the CLI

Run `/remote-env` in your terminal to choose the default environment for cloud sessions you create from the CLI, such as [`claude --cloud`](/docs/en/claude-code-on-the-web#from-terminal-to-web). The command opens a picker of your existing environments and saves your choice to the `remote.defaultEnvironmentId` key in your [user settings](/docs/en/settings#settings-files), so it applies in every project on your machine until you change it, unless the same key is set at a higher-precedence [settings layer](/docs/en/settings#settings-precedence), such as a repo's project settings.

A [self-hosted environment](/docs/en/self-hosted-environments) ID, which has the form `ccpool_...`, follows a stricter source rule. See [`remote.defaultEnvironmentId`](/docs/en/settings#available-settings) for the settings layers Claude Code honors it from.

`/remote-env` only sets the default: it doesn't start a session, and it can't add or edit environments. Manage them at [claude.ai/code](https://claude.ai/code).

### Archive an environment

To archive an environment, open it for editing and select **Archive**. You can't delete an environment, only archive it.

Archiving affects new sessions, not running ones:

* Sessions already running in the environment continue to work.
* The environment disappears from the selector and from `/remote-env`, so you can't pick it for new sessions.
* No new session can start in an archived environment, on any surface. If the environment was your saved [CLI default](#select-an-environment-from-the-cli), CLI cloud sessions fall back to your first available cloud environment. Anything configured with the environment explicitly, such as a [routine](/docs/en/routines#environments-and-network-access), can't start new sessions in it; point it at another environment.

### Organization-shared environments

Owners and admins on Team and Enterprise plans can create cloud environments that are shared with every member of the organization; the same roles manage everything else on the **Cloud environments** admin page, including [self-hosted environments](/docs/en/self-hosted-environments). Shared environments appear in each member's environment selector alongside their personal ones, so a team can standardize on one configuration instead of each member recreating it.

Create, edit, and archive shared environments from the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings). Each shared environment has a name, a [network access level](#access-levels), [environment variables](#set-environment-variables) in `.env` format, and a [setup script](#setup-scripts). Owners and admins choose the organization's [default environment](#the-default-environment) separately, at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

Values in a shared environment reach every member's sessions in that environment. Like personal environments, shared environments have no dedicated secrets store, so don't include secrets.

In [Claude Tag](https://claude.com/docs/claude-tag/overview) channels, Claude works as your organization's shared identity, not as any member, so channel sessions use shared environments only. You can set the environment a channel uses in two ways:

* Set a shared environment as the organization's [default environment](#the-default-environment) at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
* [Pin one to a channel](https://claude.com/docs/claude-tag/admins/troubleshooting#channel-sessions-use-the-wrong-environment-or-can%E2%80%99t-find-one) in the Claude Tag admin settings.

Shared environments add to members' selectors rather than replacing them.

## Network access

Each environment sets one network access level, which controls the outbound connections its sessions can make. The default level, **Trusted**, allows package registries and other [allowlisted domains](#default-allowed-domains); **Custom** takes your own domain list.

To change an environment's network access, [open it for editing](#configure-your-environment) and use the **Network access** selector in the dialog. The cloud icon that opens the selector appears on the app surfaces listed under [The Default environment](#the-default-environment) and in the [routine editor](/docs/en/routines#environments-and-network-access); personal environments don't have a separate page in your claude.ai account settings.

<Note>
  MCP connectors you enable on a session or routine work without adding their hosts to **Allowed domains**, because connector traffic travels through Anthropic's servers rather than the session's network. You configure connectors per session or per routine; remove any you don't need to limit which tools Claude can reach. This relies on the same Anthropic-bound channel noted under [Security and isolation](/docs/en/claude-code-on-the-web#security-and-isolation).
</Note>

### Access levels

The **Network access** field in the [environment dialog](#configure-your-environment) takes one of four levels:

| Level       | Outbound connections                                                                         |
| :---------- | :------------------------------------------------------------------------------------------- |
| **None**    | No outbound network access through the session's network                                     |
| **Trusted** | [Allowlisted domains](#default-allowed-domains) only: package registries, GitHub, cloud SDKs |
| **Full**    | Any domain                                                                                   |
| **Custom**  | Your own allowlist, optionally including the defaults                                        |

GitHub operations use a [separate proxy](#github-proxy) that is independent of this setting, and Claude Code's connection to the Anthropic API still works at **None**, as noted under [Security and isolation](/docs/en/claude-code-on-the-web#security-and-isolation).

### Allow specific domains

To allow domains that aren't in the Trusted list, select **Custom** in the environment's network access settings, then list one domain per line in the **Allowed domains** field. This example allows three hosts an internal project might need.

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

Sessions in this environment can now reach `api.example.com`, any subdomain of `internal.example.com`, and `registry.example.com`, and no other domains through the session's network; [GitHub traffic](#github-proxy) and [MCP connector traffic](#network-access) don't go through this allowlist. A leading `*.` matches every subdomain. To keep the [Trusted domains](#default-allowed-domains) too, check **Also include default list of common package managers**; leave it unchecked to allow only what you list.

Each environment has its own allowed-domains list; there's no organization-level allowlist that admins can push to every member's environments. [Server-managed settings](/docs/en/server-managed-settings) still apply inside cloud sessions, but none of them adds domains to the environment's network allowlist.

### GitHub proxy

In Anthropic-hosted environments, all GitHub operations go through a dedicated proxy that keeps your real GitHub credentials outside the session's VM, independent of the environment's [access level](#access-levels). Sessions in a self-hosted environment authenticate git operations with credentials your deployment provides; [Configure git](/docs/en/self-hosted-environments-deploy#configure-git) covers the options, including per-session minted credentials and an opt-in to this same proxy. The proxy provides:

* **Git credentials**: the git client inside the VM uses a scoped credential, which the proxy verifies and swaps for your actual GitHub token.
* **API requests**: requests from the built-in GitHub tools, and from `gh` under the [`proxy-injected` placeholder](#work-with-github-issues-and-pull-requests), go out with your real credentials substituted.
* **Push protection**: `git push` works only against the session's current working branch; cloning, fetching, and PR operations work normally.
* **Repository scope**: GitHub API and release-asset requests reach only repositories attached to the session, so a setup script that downloads release assets from an unattached repository gets a 403.
* **GraphQL restrictions**: the proxy serves only a pinned set of GraphQL operations for pull-request workflows. The proxy rejects everything else on the GraphQL endpoint with a 403 that says `This GraphQL query is not enabled for this session` and names the REST fallback, `gh api repos/{owner}/{repo}/...`. The restriction applies to every request through the proxy regardless of the credentials you supply, so a `GH_TOKEN` you set gets the same 403. Claude can't reach GitHub APIs that exist only in GraphQL, such as Projects v2, through the proxy.

Committed files from public repositories arrive through `raw.githubusercontent.com`, which the [security proxy](#security-proxy) handles instead. That domain is in the default [Trusted list](#default-allowed-domains), so those files stay reachable unless the environment's [access level](#access-levels) excludes it.

### Security proxy

Cloud sessions in Anthropic-hosted environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes; in a [self-hosted environment](/docs/en/self-hosted-environments-deploy#default-deny-egress), outbound traffic leaves through your own network boundary instead. All outbound internet traffic from an Anthropic-hosted session passes through this proxy, which provides:

* Protection against malicious requests
* Rate limiting and abuse prevention
* Content filtering for enhanced security
* A DNS-level audit trail of requested hostnames

## What's available in cloud sessions

In Anthropic-hosted environments, each session gets a fresh virtual machine (VM) running Ubuntu 24.04 on x86\_64, regardless of your own operating system and CPU architecture, with your repository cloned and common toolchains pre-installed. When a dependency provides precompiled binaries, such as Ruby gems with native extensions or prebuilt Python wheels, use its x86\_64 Linux build to match the VM. This section covers the Anthropic-hosted defaults, the built-in GitHub tools, how to [run tests and services](#run-tests-start-services-and-add-packages), and the [resource limits](#resource-limits) each VM gets.

<Note>
  Sessions your organization routes to a [self-hosted environment](/docs/en/self-hosted-environments) run on your own runners instead, with the tools your runner image provides.
</Note>

### What carries over from your setup

Cloud sessions start from a fresh clone of your repository. Anything you commit to the repo is available. Anything you've installed or configured only on your own machine isn't available in the session. Your organization's policy arrives separately through [server-managed settings](/docs/en/server-managed-settings).

|                                                                                                                                                                                           | Available in cloud sessions | Why                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Your repo's `CLAUDE.md`                                                                                                                                                                   | Yes                         | Part of the clone                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Your repo's `.claude/settings.json` hooks                                                                                                                                                 | Yes                         | Part of the clone                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Your repo's `.mcp.json` MCP servers                                                                                                                                                       | Yes                         | Part of the clone                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Your repo's `.claude/rules/`                                                                                                                                                              | Yes                         | Part of the clone                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Your repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/`                                                                                                                     | Yes                         | Part of the clone                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Plugins declared in `.claude/settings.json`                                                                                                                                               | Yes                         | Installed at session start from the [marketplace](/docs/en/plugin-marketplaces) you declared. Requires network access to reach the marketplace source                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Your organization's [server-managed settings](/docs/en/server-managed-settings)                                                                                                                | Yes                         | Fetched from Anthropic's servers when the session starts. See [Surface coverage](/docs/en/model-config#surface-coverage) for how `availableModels` is enforced in cloud sessions. Settings deployed to your device through MDM or managed settings files don't apply, because the session runs on an Anthropic-managed VM; in a [self-hosted environment](/docs/en/self-hosted-environments), sessions read the managed settings file in the runner image only when server-managed settings deliver no keys, per [settings precedence](/docs/en/server-managed-settings#settings-precedence) |
| Your user `~/.claude/CLAUDE.md`                                                                                                                                                           | No                          | Lives on your machine, not in the repo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Your user `~/.claude/skills/`, `~/.claude/agents/`, `~/.claude/commands/`                                                                                                                 | No                          | Live on your machine, not in the repo. Commit them to the repo's `.claude/` directory instead. Cloud sessions automatically load skills you enable on claude.ai                                                                                                                                                                                                                                                                                                                                                                                                               |
| Plugins enabled only in your user settings                                                                                                                                                | No                          | User-scoped `enabledPlugins` lives in `~/.claude/settings.json`. Declare them in the repo's `.claude/settings.json` instead                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| MCP servers you added with `claude mcp add` at the default local scope or the user scope                                                                                                  | No                          | Those write to `~/.claude.json` on your machine, not the repo. Add the server with `claude mcp add --scope project`, which writes the repo's [`.mcp.json`](/docs/en/mcp#project-scope), and commit that file                                                                                                                                                                                                                                                                                                                                                                       |
| Transport variables in your repo's `.claude/settings.json` `env` block, such as `NODE_EXTRA_CA_CERTS` and the [mTLS client certificate variables](/docs/en/network-config#mtls-authentication) | No                          | The hosting environment manages the session's API connection, so Claude Code ignores these keys and notes each ignored key in the session's debug log                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Static API tokens and credentials                                                                                                                                                         | No                          | No dedicated secrets store exists yet. See below                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Interactive auth like AWS SSO                                                                                                                                                             | No                          | Not supported. SSO requires browser-based login that can't run in a cloud session                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |

To make your own configuration available in cloud sessions, commit it to the repo.

A dedicated secrets store is not yet available, and the dialog warns against adding secrets or credentials: environment variables and setup scripts live in the environment configuration, where anyone who uses the environment can read them. If a session needs a credential anyway, add it with that visibility in mind.

### Installed tools

Cloud sessions come with common language runtimes, build tools, and databases pre-installed. The table below summarizes what's included by category.

| Category      | Included                                                                   |
| :------------ | :------------------------------------------------------------------------- |
| **Python**    | Python 3.x with pip, poetry, uv, black, mypy, pytest, ruff                 |
| **Node.js**   | 20, 21, and 22, with npm, yarn, pnpm, bun¹, eslint, prettier, chromedriver |
| **Ruby**      | 3.1, 3.2, 3.3 with gem, bundler, rbenv                                     |
| **PHP**       | 8.4 with Composer                                                          |
| **Java**      | OpenJDK 21 with Maven and Gradle                                           |
| **Go**        | latest stable with module support                                          |
| **Rust**      | rustc and cargo                                                            |
| **C/C++**     | GCC, Clang, cmake, ninja, conan                                            |
| **Docker**    | docker, dockerd, docker compose                                            |
| **Databases** | PostgreSQL 16, Redis 7.0                                                   |
| **Utilities** | git, jq, yq, ripgrep, tmux, vim, nano                                      |

¹ Bun is installed but has known [proxy compatibility issues](#install-dependencies-with-a-sessionstart-hook) for package fetching.

For exact versions, ask Claude to run `check-tools` in a cloud session. It's a shell command installed on the session VM, not a slash command; you ask Claude because [Claude runs all VM commands for you](#run-tests-start-services-and-add-packages).

Node.js versions are installed at `/opt/node20`, `/opt/node21`, and `/opt/node22`, with 22 on `PATH` by default. To work with a different version, ask Claude to prepend that version's `bin` directory, such as `/opt/node20/bin`, to `PATH`.

Toolchains outside this list, such as the .NET SDK, aren't pre-installed even when their package registries are on the [default allowlist](#default-allowed-domains). Install them with a [setup script](#setup-scripts).

### Work with GitHub issues and pull requests

Cloud sessions include built-in GitHub tools that let Claude read issues, list pull requests, fetch diffs, and post comments without any setup. These tools authenticate through the [GitHub proxy](#github-proxy) using whichever method you configured under [GitHub authentication options](/docs/en/claude-code-on-the-web#github-authentication-options), so your token never enters the container.

You can set `GH_TOKEN` or `GITHUB_TOKEN` yourself in [environment settings](#set-environment-variables), or leave both unset and let the [GitHub proxy](#github-proxy) authenticate for you:

* If you set a token, it passes through to the container unchanged, so your scripts, and GitHub's [`gh` CLI](https://cli.github.com) if you install it, use it directly.
* If you set neither and the [GitHub proxy](#github-proxy) is handling authentication for your session, both variables read as the placeholder string `proxy-injected` in the commands Claude runs, and the proxy substitutes your real credentials on outbound GitHub requests. `gh` works without a token of your own, but a script that reads `GITHUB_TOKEN` directly gets the placeholder, not a usable token.

A token you set is an ordinary environment variable, so anyone who uses the environment can read it; the proxy path keeps the credential out of the environment configuration and the session VM.

To check which case applies to your session, ask Claude to run `echo $GH_TOKEN`.

GitHub's [`gh` CLI](https://cli.github.com) isn't pre-installed. If you need a `gh` command the built-in tools don't cover, like `gh release` or `gh workflow run`, install and authenticate it yourself:

<Steps>
  <Step title="Install gh in your setup script">
    Add `apt update && apt install -y gh` to your [setup script](#setup-scripts).
  </Step>

  <Step title="Provide a token if the proxy is not handling authentication">
    If `echo $GH_TOKEN` prints `proxy-injected`, the [GitHub proxy](#github-proxy) authenticates `gh` for you and this step is unnecessary. Otherwise, add a `GH_TOKEN` environment variable to your [environment settings](#set-environment-variables) with a GitHub personal access token; like any environment variable, it's readable by anyone who uses the environment, so scope the token narrowly. `gh` reads `GH_TOKEN` automatically, so you don't need to run `gh auth login`.
  </Step>
</Steps>

### Link output back to the session

Each cloud session has a transcript URL on claude.ai, and the session can read its own ID from the `CLAUDE_CODE_REMOTE_SESSION_ID` environment variable. Use this to put a traceable link in PR bodies, commit messages, Slack posts, or generated reports so a reviewer can open the run that produced them.

Commits that Claude creates in a cloud session include a `Claude-Session: <url>` git trailer, and PR bodies include the session URL on its own line. This requires v2.1.179 or later. To omit the trailer and the PR-body link, set [`attribution.sessionUrl`](/docs/en/settings#attribution-settings) to `false`. The setting requires v2.1.182 or later.

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

The VM may stop tasks that need significantly more memory, such as large build jobs or memory-intensive tests. For workloads beyond these limits, use [Remote Control](/docs/en/remote-control) to run Claude Code on your own hardware, or run cloud sessions in a [self-hosted environment](/docs/en/self-hosted-environments) on compute your organization operates.

## Setup scripts

A setup script is a Bash script that runs when a new cloud session starts, before Claude Code launches. Use setup scripts to install dependencies, configure tools, or fetch anything the session needs that isn't pre-installed.

Scripts run as root on Ubuntu 24.04, so `apt install` and most language package managers work.

To add a setup script, open the environment settings dialog and enter your script in the **Setup script** field.

This example installs GitHub's [`gh` CLI](https://cli.github.com), which isn't pre-installed.

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

### Script requirements

A setup script has three constraints to write around:

* **Exit zero**: if the script exits non-zero, the session fails to start. Append `|| true` to non-critical commands so an intermittent install failure doesn't block the session.
* **Finish within five minutes**: keep the script's total runtime under roughly five minutes so the [environment cache](#environment-caching) can build. Run independent installs in parallel with `&` and `wait`, and move any single download that won't fit into a [SessionStart hook](#setup-scripts-vs-sessionstart-hooks) that launches it in the background.
* **Network access for installs**: package installs need to reach registries. The default **Trusted** level covers [common package registries](#default-allowed-domains) including npm, PyPI, RubyGems, and crates.io; with **None** network access, installs fail.

### Environment caching

The setup script runs the first time you start a session in an environment. After it completes, Anthropic snapshots the filesystem and reuses that snapshot as the starting point for later sessions. New sessions start with your dependencies, tools, and Docker images already on disk, and skip the setup script step. This keeps startup fast even when the script installs large toolchains or pulls container images.

The cache is a filesystem snapshot, so it keeps what the setup script writes to disk and loses anything that was only running. Packages you install, Docker images you pull, and files you write all carry over. A database the script started, a `docker compose up` stack, or any other background process doesn't; start those per session by asking Claude or with a [SessionStart hook](#setup-scripts-vs-sessionstart-hooks).

The setup script runs again to rebuild the cache when you change the environment's setup script or allowed network hosts, and when the cache reaches its expiry after roughly seven days. Resuming an existing session never re-runs the setup script.

You don't need to enable caching or manage snapshots yourself.

### Setup scripts vs. SessionStart hooks

Use a setup script to provision the VM itself: toolchains and CLI tools that aren't [pre-installed](#installed-tools). Use a [SessionStart hook](/docs/en/hooks#sessionstart) for project setup that should run everywhere, cloud and local, like `npm install`.

Setup scripts and SessionStart hooks run in a fixed order when a cloud session starts:

1. The setup script runs first, before Claude Code launches, and only when no [cached environment](#environment-caching) exists.
2. Claude Code launches and runs your SessionStart hooks, as it does at the start of every session, local or cloud.

|                              | Setup scripts                                                                                 | SessionStart hooks                                                                                                                                                                                            |
| ---------------------------- | --------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Where you configure them** | The environment dialog at [claude.ai/code](https://claude.ai/code)                            | A [settings file](/docs/en/settings#settings-files) such as your repo's `.claude/settings.json`; see [What carries over from your setup](#what-carries-over-from-your-setup) for which files reach a cloud session |
| **When they run**            | Before Claude Code launches, skipped when a [cached environment](#environment-caching) exists | After Claude Code launches, on every session including resumed                                                                                                                                                |
| **Where they run**           | Cloud sessions only                                                                           | Local and cloud sessions                                                                                                                                                                                      |

If you have SessionStart hooks in your user-level `~/.claude/settings.json`, don't expect them in the cloud: user-level settings stay on your machine. In a cloud session, Claude Code runs hooks from the repository and from your organization's [server-managed settings](/docs/en/server-managed-settings); sessions in a [self-hosted environment](/docs/en/self-hosted-environments-configuration#permissions-and-tool-approval) also run hooks the operator seeded from the runner host's `~/.claude/`.

### Install dependencies with a SessionStart hook

To install dependencies only in cloud sessions, pair a SessionStart hook with a script that checks where it's running.

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

Next, create the script at `scripts/install_pkgs.sh`. It exits immediately outside the cloud, then installs your dependencies:

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

The `CLAUDE_CODE_REMOTE` check is what scopes the install to cloud sessions: the session VM's environment carries that variable as `true`, it's never `true` locally, so on your laptop the script exits before installing anything.

Together, the two files give every cloud session a fresh `npm install` and `pip install` at startup while leaving local sessions untouched.

#### Limitations in cloud sessions

SessionStart hooks behave the same in the cloud as locally, with these caveats:

* **No cloud-only scoping**: hooks run in both local and cloud sessions. To skip local execution, check the `CLAUDE_CODE_REMOTE` environment variable as shown above.
* **Requires network access**: install commands need to reach package registries. If your environment uses **None** network access, these hooks fail. The [default allowlist](#default-allowed-domains) under **Trusted** covers npm, PyPI, RubyGems, and crates.io.
* **Proxy compatibility**: in Anthropic-hosted environments, all outbound traffic passes through a [security proxy](#security-proxy), and some package managers don't work correctly with it; Bun is a known example. In a [self-hosted environment](/docs/en/self-hosted-environments-deploy#default-deny-egress), outbound traffic goes through your own network boundary instead.
* **Adds startup latency**: hooks run each time a session starts or resumes, unlike setup scripts which benefit from [environment caching](#environment-caching). Keep install scripts fast by checking whether dependencies are already present before reinstalling.

To persist environment variables for subsequent Bash commands, write to the file at `$CLAUDE_ENV_FILE`. See [SessionStart hooks](/docs/en/hooks#sessionstart) for details.

To customize the base image, use a setup script to install what you need on top of the [provided image](#installed-tools), or run your own image as a container alongside Claude with `docker compose`. Replacing the base image entirely isn't supported yet.

## Default allowed domains

With **Trusted** network access, sessions can reach the following domains by default. Domains marked with `*` indicate wildcard subdomain matching, so `*.gcr.io` allows any subdomain of `gcr.io`.

<AccordionGroup>
  <Accordion title="Anthropic services">
    * api.anthropic.com
    * statsig.anthropic.com
    * docs.claude.com
    * platform.claude.com
    * code.claude.com
    * claude.ai
  </Accordion>

  <Accordion title="Version control">
    * github.com
    * [www.github.com](http://www.github.com)
    * api.github.com
    * npm.pkg.github.com
    * raw\.githubusercontent.com
    * pkg-npm.githubusercontent.com
    * objects.githubusercontent.com
    * release-assets.githubusercontent.com
    * codeload.github.com
    * avatars.githubusercontent.com
    * camo.githubusercontent.com
    * gist.github.com
    * gitlab.com
    * [www.gitlab.com](http://www.gitlab.com)
    * registry.gitlab.com
    * bitbucket.org
    * [www.bitbucket.org](http://www.bitbucket.org)
    * api.bitbucket.org
  </Accordion>

  <Accordion title="Container registries">
    * registry-1.docker.io
    * auth.docker.io
    * index.docker.io
    * hub.docker.com
    * [www.docker.com](http://www.docker.com)
    * production.cloudflare.docker.com
    * download.docker.com
    * gcr.io
    * \*.gcr.io
    * ghcr.io
    * mcr.microsoft.com
    * \*.data.mcr.microsoft.com
    * public.ecr.aws
  </Accordion>

  <Accordion title="Cloud platforms">
    * cloud.google.com
    * accounts.google.com
    * gcloud.google.com
    * \*.googleapis.com
    * storage.googleapis.com
    * compute.googleapis.com
    * container.googleapis.com
    * azure.com
    * portal.azure.com
    * microsoft.com
    * [www.microsoft.com](http://www.microsoft.com)
    * \*.microsoftonline.com
    * packages.microsoft.com
    * dotnet.microsoft.com
    * dot.net
    * visualstudio.com
    * dev.azure.com
    * \*.amazonaws.com
    * \*.api.aws
    * oracle.com
    * [www.oracle.com](http://www.oracle.com)
    * java.com
    * [www.java.com](http://www.java.com)
    * java.net
    * [www.java.net](http://www.java.net)
    * download.oracle.com
    * yum.oracle.com
  </Accordion>

  <Accordion title="JavaScript and Node package managers">
    * registry.npmjs.org
    * [www.npmjs.com](http://www.npmjs.com)
    * [www.npmjs.org](http://www.npmjs.org)
    * npmjs.com
    * npmjs.org
    * yarnpkg.com
    * registry.yarnpkg.com
  </Accordion>

  <Accordion title="Python package managers">
    * pypi.org
    * [www.pypi.org](http://www.pypi.org)
    * files.pythonhosted.org
    * pythonhosted.org
    * test.pypi.org
    * pypi.python.org
    * pypa.io
    * [www.pypa.io](http://www.pypa.io)
  </Accordion>

  <Accordion title="Ruby package managers">
    * rubygems.org
    * [www.rubygems.org](http://www.rubygems.org)
    * api.rubygems.org
    * index.rubygems.org
    * ruby-lang.org
    * [www.ruby-lang.org](http://www.ruby-lang.org)
    * rubyforge.org
    * [www.rubyforge.org](http://www.rubyforge.org)
    * rubyonrails.org
    * [www.rubyonrails.org](http://www.rubyonrails.org)
    * rvm.io
    * get.rvm.io
  </Accordion>

  <Accordion title="Rust package managers">
    * crates.io
    * [www.crates.io](http://www.crates.io)
    * index.crates.io
    * static.crates.io
    * rustup.rs
    * static.rust-lang.org
    * [www.rust-lang.org](http://www.rust-lang.org)
  </Accordion>

  <Accordion title="Go package managers">
    * proxy.golang.org
    * sum.golang.org
    * index.golang.org
    * golang.org
    * [www.golang.org](http://www.golang.org)
    * goproxy.io
    * pkg.go.dev
  </Accordion>

  <Accordion title="JVM package managers">
    * maven.org
    * repo.maven.org
    * central.maven.org
    * repo1.maven.org
    * repo.maven.apache.org
    * jcenter.bintray.com
    * gradle.org
    * [www.gradle.org](http://www.gradle.org)
    * services.gradle.org
    * plugins.gradle.org
    * kotlinlang.org
    * [www.kotlinlang.org](http://www.kotlinlang.org)
    * spring.io
    * repo.spring.io
  </Accordion>

  <Accordion title="Other package managers">
    * packagist.org (PHP Composer)
    * [www.packagist.org](http://www.packagist.org)
    * repo.packagist.org
    * nuget.org (.NET NuGet)
    * [www.nuget.org](http://www.nuget.org)
    * api.nuget.org
    * pub.dev (Dart/Flutter)
    * api.pub.dev
    * hex.pm (Elixir/Erlang)
    * [www.hex.pm](http://www.hex.pm)
    * cpan.org (Perl CPAN)
    * [www.cpan.org](http://www.cpan.org)
    * metacpan.org
    * [www.metacpan.org](http://www.metacpan.org)
    * api.metacpan.org
    * cocoapods.org (iOS/macOS)
    * [www.cocoapods.org](http://www.cocoapods.org)
    * cdn.cocoapods.org
    * haskell.org
    * [www.haskell.org](http://www.haskell.org)
    * hackage.haskell.org
    * swift.org
    * [www.swift.org](http://www.swift.org)
  </Accordion>

  <Accordion title="Linux distributions">
    * archive.ubuntu.com
    * security.ubuntu.com
    * ubuntu.com
    * [www.ubuntu.com](http://www.ubuntu.com)
    * \*.ubuntu.com
    * ppa.launchpad.net
    * launchpad.net
    * [www.launchpad.net](http://www.launchpad.net)
    * \*.nixos.org
  </Accordion>

  <Accordion title="Development tools and platforms">
    * dl.k8s.io (Kubernetes)
    * pkgs.k8s.io
    * k8s.io
    * [www.k8s.io](http://www.k8s.io)
    * releases.hashicorp.com (HashiCorp)
    * apt.releases.hashicorp.com
    * rpm.releases.hashicorp.com
    * archive.releases.hashicorp.com
    * hashicorp.com
    * [www.hashicorp.com](http://www.hashicorp.com)
    * repo.anaconda.com (Anaconda/Conda)
    * conda.anaconda.org
    * anaconda.org
    * [www.anaconda.com](http://www.anaconda.com)
    * anaconda.com
    * continuum.io
    * apache.org (Apache)
    * [www.apache.org](http://www.apache.org)
    * archive.apache.org
    * downloads.apache.org
    * eclipse.org (Eclipse)
    * [www.eclipse.org](http://www.eclipse.org)
    * download.eclipse.org
    * nodejs.org (Node.js)
    * [www.nodejs.org](http://www.nodejs.org)
    * developer.apple.com
    * developer.android.com
    * pkg.stainless.com
    * binaries.prisma.sh
  </Accordion>

  <Accordion title="Cloud services and monitoring">
    * statsig.com
    * [www.statsig.com](http://www.statsig.com)
    * api.statsig.com
    * sentry.io
    * \*.sentry.io
    * downloads.sentry-cdn.com
    * http-intake.logs.datadoghq.com
    * browser-intake-us5-datadoghq.com
    * \*.datadoghq.com
    * \*.datadoghq.eu
    * api.honeycomb.io
  </Accordion>

  <Accordion title="Content delivery and mirrors">
    * sourceforge.net
    * \*.sourceforge.net
    * packagecloud.io
    * \*.packagecloud.io
    * fonts.googleapis.com
    * fonts.gstatic.com
  </Accordion>

  <Accordion title="Schema and configuration">
    * json-schema.org
    * [www.json-schema.org](http://www.json-schema.org)
    * json.schemastore.org
    * [www.schemastore.org](http://www.schemastore.org)
  </Accordion>

  <Accordion title="Model Context Protocol">
    * \*.modelcontextprotocol.io
  </Accordion>
</AccordionGroup>

## Related resources

* [Claude Code on the web](/docs/en/claude-code-on-the-web): start, manage, and share cloud sessions
* [Web quickstart](/docs/en/web-quickstart): connect GitHub and start your first cloud session
* [Claude Tag](https://claude.com/docs/claude-tag/overview): sessions Claude starts from Slack run in the same Anthropic-hosted environments
* [Routines](/docs/en/routines): scheduled runs use the same environments and network access levels
* [Remote Control](/docs/en/remote-control): run sessions on your own machine's network and files instead
* [Self-hosted environments](/docs/en/self-hosted-environments): run cloud sessions on your organization's own infrastructure
* [SessionStart hooks](/docs/en/hooks#sessionstart): repo-committed setup that runs in local and cloud sessions
* [Server-managed settings](/docs/en/server-managed-settings): organization policy that reaches cloud sessions
