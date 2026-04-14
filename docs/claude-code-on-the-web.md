> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code on the web

> Configure cloud environments, setup scripts, network access, and Docker in Anthropic's sandbox. Move sessions between web and terminal with `--remote` and `--teleport`.

<Note>
  Claude Code on the web is in research preview for Pro, Max, and Team users, and for Enterprise users with premium seats or Chat + Claude Code seats.
</Note>

Claude Code on the web runs tasks on Anthropic-managed cloud infrastructure at [claude.ai/code](https://claude.ai/code). Sessions persist even if you close your browser, and you can monitor them from the Claude mobile app.

<Tip>
  New to Claude Code on the web? Start with [Get started](/en/web-quickstart) to connect your GitHub account and submit your first task.
</Tip>

This page covers:

* [GitHub authentication options](#github-authentication-options): two ways to connect GitHub
* [The cloud environment](#the-cloud-environment): what config carries over, what tools are installed, and how to configure environments
* [Setup scripts](#setup-scripts) and dependency management
* [Network access](#network-access): levels, proxies, and the default allowlist
* [Move tasks between web and terminal](#move-tasks-between-web-and-terminal) with `--remote` and `--teleport`
* [Work with sessions](#work-with-sessions): reviewing, sharing, archiving, deleting
* [Auto-fix pull requests](#auto-fix-pull-requests): respond automatically to CI failures and review comments
* [Security and isolation](#security-and-isolation): how sessions are isolated
* [Limitations](#limitations): rate limits and platform restrictions

## GitHub authentication options

Cloud sessions need access to your GitHub repositories to clone code and push branches. You can grant access in two ways:

| Method           | How it works                                                                                                                                 | Best for                                        |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| **GitHub App**   | Install the Claude GitHub App on specific repositories during [web onboarding](/en/web-quickstart). Access is scoped per repository.         | Teams that want explicit per-repo authorization |
| **`/web-setup`** | Run `/web-setup` in your terminal to sync your local `gh` CLI token to your Claude account. Access matches whatever your `gh` token can see. | Individual developers who already use `gh`      |

Either method works. [`/schedule`](/en/routines) checks for either form of access and prompts you to run `/web-setup` if neither is configured. See [Connect from your terminal](/en/web-quickstart#connect-from-your-terminal) for the `/web-setup` walkthrough.

The GitHub App is required for [Auto-fix](#auto-fix-pull-requests), which uses the App to receive PR webhooks. If you connect with `/web-setup` and later want Auto-fix, install the App on those repositories.

Team and Enterprise admins can disable `/web-setup` with the Quick web setup toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

<Note>
  Organizations with [Zero Data Retention](/en/zero-data-retention) enabled cannot use `/web-setup` or other cloud session features.
</Note>

## The cloud environment

Each session runs in a fresh Anthropic-managed VM with your repository cloned. This section covers what's available when a session starts and how to customize it.

### What's available in cloud sessions

Cloud sessions start from a fresh clone of your repository. Anything committed to the repo is available. Anything you've installed or configured only on your own machine is not.

|                                                                       | Available in cloud sessions | Why                                                                                                                                              |
| :-------------------------------------------------------------------- | :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| Your repo's `CLAUDE.md`                                               | Yes                         | Part of the clone                                                                                                                                |
| Your repo's `.claude/settings.json` hooks                             | Yes                         | Part of the clone                                                                                                                                |
| Your repo's `.mcp.json` MCP servers                                   | Yes                         | Part of the clone                                                                                                                                |
| Your repo's `.claude/rules/`                                          | Yes                         | Part of the clone                                                                                                                                |
| Your repo's `.claude/skills/`, `.claude/agents/`, `.claude/commands/` | Yes                         | Part of the clone                                                                                                                                |
| Plugins declared in `.claude/settings.json`                           | Yes                         | Installed at session start from the [marketplace](/en/plugin-marketplaces) you declared. Requires network access to reach the marketplace source |
| Your user `~/.claude/CLAUDE.md`                                       | No                          | Lives on your machine, not in the repo                                                                                                           |
| Plugins enabled only in your user settings                            | No                          | User-scoped `enabledPlugins` lives in `~/.claude/settings.json`. Declare them in the repo's `.claude/settings.json` instead                      |
| MCP servers you added with `claude mcp add`                           | No                          | Those write to your local user config, not the repo. Declare the server in [`.mcp.json`](/en/mcp#project-scope) instead                          |
| Static API tokens and credentials                                     | No                          | No dedicated secrets store exists yet. See below                                                                                                 |
| Interactive auth like AWS SSO                                         | No                          | Not supported. SSO requires browser-based login that can't run in a cloud session                                                                |

To make configuration available in cloud sessions, commit it to the repo. A dedicated secrets store is not yet available. Both environment variables and setup scripts are stored in the environment configuration, visible to anyone who can edit that environment. If you need secrets in a cloud session, add them as environment variables with that visibility in mind.

### Installed tools

Cloud sessions come with common language runtimes, build tools, and databases pre-installed. The table below summarizes what's included by category.

| Category      | Included                                                                           |
| :------------ | :--------------------------------------------------------------------------------- |
| **Python**    | Python 3.x with pip, poetry, uv, black, mypy, pytest, ruff                         |
| **Node.js**   | 20, 21, and 22 via nvm, with npm, yarn, pnpm, bun¹, eslint, prettier, chromedriver |
| **Ruby**      | 3.1, 3.2, 3.3 with gem, bundler, rbenv                                             |
| **PHP**       | 8.4 with Composer                                                                  |
| **Java**      | OpenJDK 21 with Maven and Gradle                                                   |
| **Go**        | latest stable with module support                                                  |
| **Rust**      | rustc and cargo                                                                    |
| **C/C++**     | GCC, Clang, cmake, ninja, conan                                                    |
| **Docker**    | docker, dockerd, docker compose                                                    |
| **Databases** | PostgreSQL 16, Redis 7.0                                                           |
| **Utilities** | git, jq, yq, ripgrep, tmux, vim, nano                                              |

¹ Bun is installed but has known [proxy compatibility issues](#install-dependencies-with-a-sessionstart-hook) for package fetching.

For exact versions, ask Claude to run `check-tools` in a cloud session. This command only exists in cloud sessions.

### Work with GitHub issues and pull requests

Cloud sessions include built-in GitHub tools that let Claude read issues, list pull requests, fetch diffs, and post comments without any setup. These tools authenticate through the [GitHub proxy](#github-proxy) using whichever method you configured under [GitHub authentication options](#github-authentication-options), so your token never enters the container.

The `gh` CLI is not pre-installed. If you need a `gh` command the built-in tools don't cover, like `gh release` or `gh workflow run`, install and authenticate it yourself:

<Steps>
  <Step title="Install gh in your setup script">
    Add `apt update && apt install -y gh` to your [setup script](#setup-scripts).
  </Step>

  <Step title="Provide a token">
    Add a `GH_TOKEN` environment variable to your [environment settings](#configure-your-environment) with a GitHub personal access token. `gh` reads `GH_TOKEN` automatically, so no `gh auth login` step is needed.
  </Step>
</Steps>

### Run tests, start services, and add packages

Claude runs tests as part of working on a task. Ask for it in your prompt, like "fix the failing tests in `tests/`" or "run pytest after each change." Test runners like pytest, jest, and cargo test work out of the box since they're pre-installed.

PostgreSQL and Redis are pre-installed but not running by default. Start each one in a [setup script](#setup-scripts) or ask Claude to start it during the session:

```bash  theme={null}
service postgresql start
```

```bash  theme={null}
service redis-server start
```

Docker is available for running containerized services. Network access to pull images follows your environment's [access level](#access-levels).

To add packages that aren't pre-installed, use a [setup script](#setup-scripts) so they're available at session start. You can also ask Claude to install packages during the session, but those installs don't persist across sessions.

### Resource limits

Cloud sessions run with approximate resource ceilings that may change over time:

* 4 vCPUs
* 16 GB of RAM
* 30 GB of disk

Tasks requiring significantly more memory, such as large build jobs or memory-intensive tests, may fail or be terminated. For workloads beyond these limits, use [Remote Control](/en/remote-control) to run Claude Code on your own hardware.

### Configure your environment

Environments control [network access](#network-access), environment variables, and the [setup script](#setup-scripts) that runs before a session starts. See [Installed tools](#installed-tools) for what's available without any configuration. You can manage environments from the web interface or the terminal:

| Action                         | How                                                                                                                                                                                                                      |
| :----------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Add an environment             | Select the current environment to open the selector, then select **Add environment**. The dialog includes name, network access level, environment variables, and setup script.                                           |
| Edit an environment            | Select the settings icon to the right of the environment name.                                                                                                                                                           |
| Archive an environment         | Open the environment for editing and select **Archive**. Archived environments are hidden from the selector but existing sessions keep running.                                                                          |
| Set the default for `--remote` | Run `/remote-env` in your terminal. If you have a single environment, this command shows your current configuration. `/remote-env` only selects the default; add, edit, and archive environments from the web interface. |

Environment variables use `.env` format with one `KEY=value` pair per line. Don't wrap values in quotes, since quotes are stored as part of the value.

```text  theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

## Setup scripts

A setup script is a Bash script that runs when a new cloud session starts, before Claude Code launches. Use setup scripts to install dependencies, configure tools, or fetch anything the session needs that isn't pre-installed.

Scripts run as root on Ubuntu 24.04, so `apt install` and most language package managers work.

To add a setup script, open the environment settings dialog and enter your script in the **Setup script** field.

This example installs the `gh` CLI, which isn't pre-installed:

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Setup scripts run only when creating a new session. They are skipped when resuming an existing session.

If the script exits non-zero, the session fails to start. Append `|| true` to non-critical commands to avoid blocking the session on an intermittent install failure.

<Note>
  Setup scripts that install packages need network access to reach registries. The default **Trusted** network access allows connections to [common package registries](#default-allowed-domains) including npm, PyPI, RubyGems, and crates.io. Scripts will fail to install packages if your environment uses **None** network access.
</Note>

### Setup scripts vs. SessionStart hooks

Use a setup script to install things the cloud needs but your laptop already has, like a language runtime or CLI tool. Use a [SessionStart hook](/en/hooks#sessionstart) for project setup that should run everywhere, cloud and local, like `npm install`.

Both run at the start of a session, but they belong to different places:

|               | Setup scripts                                     | SessionStart hooks                                             |
| ------------- | ------------------------------------------------- | -------------------------------------------------------------- |
| Attached to   | The cloud environment                             | Your repository                                                |
| Configured in | Cloud environment UI                              | `.claude/settings.json` in your repo                           |
| Runs          | Before Claude Code launches, on new sessions only | After Claude Code launches, on every session including resumed |
| Scope         | Cloud environments only                           | Both local and cloud                                           |

SessionStart hooks can also be defined in your user-level `~/.claude/settings.json` locally, but user-level settings don't carry over to cloud sessions. In the cloud, only hooks committed to the repo run.

### Install dependencies with a SessionStart hook

To install dependencies only in cloud sessions, add a SessionStart hook to your repo's `.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Create the script at `scripts/install_pkgs.sh` and make it executable with `chmod +x`. The `CLAUDE_CODE_REMOTE` environment variable is set to `true` in cloud sessions, so you can use it to skip local execution:

```bash  theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

SessionStart hooks have some limitations in cloud sessions:

* **No cloud-only scoping**: hooks run in both local and cloud sessions. To skip local execution, check the `CLAUDE_CODE_REMOTE` environment variable as shown above.
* **Requires network access**: install commands need to reach package registries. If your environment uses **None** network access, these hooks fail. The [default allowlist](#default-allowed-domains) under **Trusted** covers npm, PyPI, RubyGems, and crates.io.
* **Proxy compatibility**: all outbound traffic passes through a [security proxy](#security-proxy). Some package managers don't work correctly with this proxy. Bun is a known example.
* **Adds startup latency**: hooks run each time a session starts or resumes. Keep install scripts fast by checking whether dependencies are already present before reinstalling.

To persist environment variables for subsequent Bash commands, write to the file at `$CLAUDE_ENV_FILE`. See [SessionStart hooks](/en/hooks#sessionstart) for details.

Custom environment images and snapshots are not yet supported.

## Network access

Network access controls outbound connections from the cloud environment. Each environment specifies one access level, and you can extend it with custom allowed domains. The default is **Trusted**, which allows package registries and other [allowlisted domains](#default-allowed-domains).

### Access levels

Choose an access level when you create or edit an environment:

| Level       | Outbound connections                                                                         |
| :---------- | :------------------------------------------------------------------------------------------- |
| **None**    | No outbound network access                                                                   |
| **Trusted** | [Allowlisted domains](#default-allowed-domains) only: package registries, GitHub, cloud SDKs |
| **Full**    | Any domain                                                                                   |
| **Custom**  | Your own allowlist, optionally including the defaults                                        |

GitHub operations use a [separate proxy](#github-proxy) that is independent of this setting.

### Allow specific domains

To allow domains that aren't in the Trusted list, select **Custom** in the environment's network access settings. An **Allowed domains** field appears. Enter one domain per line:

```text  theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

Use `*.` for wildcard subdomain matching. Check **Also include default list of common package managers** to keep the [Trusted domains](#default-allowed-domains) alongside your custom entries, or leave it unchecked to allow only what you list.

### GitHub proxy

For security, all GitHub operations go through a dedicated proxy service that transparently handles all git interactions. Inside the sandbox, the git client authenticates using a custom-built scoped credential. This proxy:

* Manages GitHub authentication securely: the git client uses a scoped credential inside the sandbox, which the proxy verifies and translates to your actual GitHub authentication token
* Restricts git push operations to the current working branch for safety
* Enables cloning, fetching, and PR operations while maintaining security boundaries

### Security proxy

Environments run behind an HTTP/HTTPS network proxy for security and abuse prevention purposes. All outbound internet traffic passes through this proxy, which provides:

* Protection against malicious requests
* Rate limiting and abuse prevention
* Content filtering for enhanced security

### Default allowed domains

When using **Trusted** network access, the following domains are allowed by default. Domains marked with `*` indicate wildcard subdomain matching, so `*.gcr.io` allows any subdomain of `gcr.io`.

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

## Move tasks between web and terminal

These workflows require the [Claude Code CLI](/en/quickstart) signed in to the same claude.ai account. You can start new cloud sessions from your terminal, or pull cloud sessions into your terminal to continue locally. Cloud sessions persist even if you close your laptop, and you can monitor them from anywhere including the Claude mobile app.

<Note>
  From the CLI, session handoff is one-way: you can pull cloud sessions into your terminal with `--teleport`, but you can't push an existing terminal session to the web. The `--remote` flag creates a new cloud session for your current repository. The [Desktop app](/en/desktop#continue-in-another-surface) provides a Continue in menu that can send a local session to the web.
</Note>

### From terminal to web

Start a cloud session from the command line with the `--remote` flag:

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

This creates a new cloud session on claude.ai. The session clones your current directory's GitHub remote at your current branch, so push first if you have local commits, since the VM clones from GitHub rather than your machine. `--remote` works with a single repository at a time. The task runs in the cloud while you continue working locally.

<Note>
  `--remote` creates cloud sessions. `--remote-control` is unrelated: it exposes a local CLI session for monitoring from the web. See [Remote Control](/en/remote-control).
</Note>

Use `/tasks` in the Claude Code CLI to check progress, or open the session on claude.ai or the Claude mobile app to interact directly. From there you can steer Claude, provide feedback, or answer questions just like any other conversation.

#### Tips for cloud tasks

**Plan locally, execute remotely**: for complex tasks, start Claude in plan mode to collaborate on the approach, then send work to the cloud:

```bash  theme={null}
claude --permission-mode plan
```

In plan mode, Claude reads files, runs commands to explore, and proposes a plan without editing source code. Once you're satisfied, save the plan to the repo, commit, and push so the cloud VM can clone it. Then start a cloud session for autonomous execution:

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

This pattern gives you control over the strategy while letting Claude execute autonomously in the cloud.

**Plan in the cloud with ultraplan**: to draft and review the plan itself in a web session, use [ultraplan](/en/ultraplan). Claude generates the plan on Claude Code on the web while you keep working, then you comment on sections in your browser and choose to execute remotely or send the plan back to your terminal.

**Run tasks in parallel**: each `--remote` command creates its own cloud session that runs independently. You can start multiple tasks and they'll all run simultaneously in separate sessions:

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Monitor all sessions with `/tasks` in the Claude Code CLI. When a session completes, you can create a PR from the web interface or [teleport](#from-web-to-terminal) the session to your terminal to continue working.

#### Send local repositories without GitHub

When you run `claude --remote` from a repository that isn't connected to GitHub, Claude Code bundles your local repository and uploads it directly to the cloud session. The bundle includes your full repository history across all branches, plus any uncommitted changes to tracked files.

This fallback activates automatically when GitHub access isn't available. To force it even when GitHub is connected, set `CCR_FORCE_BUNDLE=1`:

```bash  theme={null}
CCR_FORCE_BUNDLE=1 claude --remote "Run the test suite and fix any failures"
```

Bundled repositories must meet these limits:

* The directory must be a git repository with at least one commit
* The bundled repository must be under 100 MB. Larger repositories fall back to bundling only the current branch, then to a single squashed snapshot of the working tree, and fail only if the snapshot is still too large
* Untracked files are not included; run `git add` on files you want the cloud session to see
* Sessions created from a bundle can't push back to a remote unless you also have [GitHub authentication](#github-authentication-options) configured

### From web to terminal

Pull a cloud session into your terminal using any of these:

* **Using `--teleport`**: from the command line, run `claude --teleport` for an interactive session picker, or `claude --teleport <session-id>` to resume a specific session directly. If you have uncommitted changes, you'll be prompted to stash them first.
* **Using `/teleport`**: inside an existing CLI session, run `/teleport` (or `/tp`) to open the same session picker without restarting Claude Code.
* **From `/tasks`**: run `/tasks` to see your background sessions, then press `t` to teleport into one
* **From the web interface**: select **Open in CLI** to copy a command you can paste into your terminal

When you teleport a session, Claude verifies you're in the correct repository, fetches and checks out the branch from the cloud session, and loads the full conversation history into your terminal.

`--teleport` is distinct from `--resume`. `--resume` reopens a conversation from this machine's local history and doesn't list cloud sessions; `--teleport` pulls a cloud session and its branch.

#### Teleport requirements

Teleport checks these requirements before resuming a session. If any requirement isn't met, you'll see an error or be prompted to resolve the issue.

| Requirement        | Details                                                                                                                  |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------ |
| Clean git state    | Your working directory must have no uncommitted changes. Teleport prompts you to stash changes if needed.                |
| Correct repository | You must run `--teleport` from a checkout of the same repository, not a fork.                                            |
| Branch available   | The branch from the cloud session must have been pushed to the remote. Teleport automatically fetches and checks it out. |
| Same account       | You must be authenticated to the same claude.ai account used in the cloud session.                                       |

#### `--teleport` is unavailable

Teleport requires claude.ai subscription authentication. If you're authenticated via API key, Bedrock, Vertex AI, or Microsoft Foundry, run `/login` to sign in with your claude.ai account instead. If you're already signed in via claude.ai and `--teleport` is still unavailable, your organization may have disabled cloud sessions.

## Work with sessions

Sessions appear in the sidebar at claude.ai/code. From there you can review changes, share with teammates, archive finished work, or delete sessions permanently.

### Manage context

Cloud sessions support [built-in commands](/en/commands) that produce text output. Commands that open an interactive terminal picker, like `/model` or `/config`, are not available.

For context management specifically:

| Command    | Works in cloud sessions | Notes                                                                                                                    |
| :--------- | :---------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `/compact` | Yes                     | Summarizes the conversation to free up context. Accepts optional focus instructions like `/compact keep the test output` |
| `/context` | Yes                     | Shows what's currently in the context window                                                                             |
| `/clear`   | No                      | Start a new session from the sidebar instead                                                                             |

Auto-compaction runs automatically when the context window approaches capacity, the same as in the CLI. To trigger it earlier, set [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/en/env-vars) in your [environment variables](#configure-your-environment). For example, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` compacts at 70% capacity instead of the default \~95%. To change the effective window size for compaction calculations, use [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/en/env-vars).

[Subagents](/en/sub-agents) work the same way they do locally. Claude can spawn them with the Task tool to offload research or parallel work into a separate context window, keeping the main conversation lighter. Subagents defined in your repo's `.claude/agents/` are picked up automatically. [Agent teams](/en/agent-teams) are off by default but can be enabled by adding `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to your [environment variables](#configure-your-environment).

### Review changes

Each session shows a diff indicator with lines added and removed, like `+42 -18`. Select it to open the diff view, leave inline comments on specific lines, and send them to Claude with your next message. See [Review and iterate](/en/web-quickstart#review-and-iterate) for the full walkthrough including PR creation. To have Claude monitor the PR for CI failures and review comments automatically, see [Auto-fix pull requests](#auto-fix-pull-requests).

### Share sessions

To share a session, toggle its visibility according to the account types below. After that, share the session link as-is. Recipients see the latest state when they open the link, but their view doesn't update in real time.

#### Share from an Enterprise or Team account

For Enterprise and Team accounts, the two visibility options are **Private** and **Team**. Team visibility makes the session visible to other members of your claude.ai organization. Repository access verification is enabled by default, based on the GitHub account connected to the recipient's account. Your account's display name is visible to all recipients with access. [Claude in Slack](/en/slack) sessions are automatically shared with Team visibility.

#### Share from a Max or Pro account

For Max and Pro accounts, the two visibility options are **Private** and **Public**. Public visibility makes the session visible to any user logged into claude.ai.

Check your session for sensitive content before sharing. Sessions may contain code and credentials from private GitHub repositories. Repository access verification is not enabled by default.

To require recipients to have repository access, or to hide your name from shared sessions, go to Settings > Claude Code > Sharing settings.

### Archive sessions

You can archive sessions to keep your session list organized. Archived sessions are hidden from the default session list but can be viewed by filtering for archived sessions.

To archive a session, hover over the session in the sidebar and select the archive icon.

### Delete sessions

Deleting a session permanently removes the session and its data. This action cannot be undone. You can delete a session in two ways:

* **From the sidebar**: filter for archived sessions, then hover over the session you want to delete and select the delete icon
* **From the session menu**: open a session, select the dropdown next to the session title, and select **Delete**

You will be asked to confirm before a session is deleted.

## Auto-fix pull requests

Claude can watch a pull request and automatically respond to CI failures and review comments. Claude subscribes to GitHub activity on the PR, and when a check fails or a reviewer leaves a comment, Claude investigates and pushes a fix if one is clear.

<Note>
  Auto-fix requires the Claude GitHub App to be installed on your repository. If you haven't already, install it from the [GitHub App page](https://github.com/apps/claude) or when prompted during [setup](/en/web-quickstart#connect-github-and-create-an-environment).
</Note>

There are a few ways to turn on auto-fix depending on where the PR came from and what device you're using:

* **PRs created in Claude Code on the web**: open the CI status bar and select **Auto-fix**
* **From your terminal**: run [`/autofix-pr`](/en/commands) while on the PR's branch. Claude Code detects the open PR with `gh`, spawns a web session, and turns on auto-fix in one step
* **From the mobile app**: tell Claude to auto-fix the PR, for example "watch this PR and fix any CI failures or review comments"
* **Any existing PR**: paste the PR URL into a session and tell Claude to auto-fix it

### How Claude responds to PR activity

When auto-fix is active, Claude receives GitHub events for the PR including new review comments and CI check failures. For each event, Claude investigates and decides how to proceed:

* **Clear fixes**: if Claude is confident in a fix and it doesn't conflict with earlier instructions, Claude makes the change, pushes it, and explains what was done in the session
* **Ambiguous requests**: if a reviewer's comment could be interpreted multiple ways or involves something architecturally significant, Claude asks you before acting
* **Duplicate or no-action events**: if an event is a duplicate or requires no change, Claude notes it in the session and moves on

Claude may reply to review comment threads on GitHub as part of resolving them. These replies are posted using your GitHub account, so they appear under your username, but each reply is labeled as coming from Claude Code so reviewers know it was written by the agent and not by you directly.

<Warning>
  If your repository uses comment-triggered automation such as Atlantis, Terraform Cloud, or custom GitHub Actions that run on `issue_comment` events, be aware that Claude can reply on your behalf, which can trigger those workflows. Review your repository's automation before enabling auto-fix, and consider disabling auto-fix for repositories where a PR comment can deploy infrastructure or run privileged operations.
</Warning>

## Security and isolation

Each cloud session is separated from your machine and from other sessions through several layers:

* **Isolated virtual machines**: each session runs in an isolated, Anthropic-managed VM
* **Network access controls**: network access is limited by default, and can be disabled. When running with network access disabled, Claude Code can still communicate with the Anthropic API, which may allow data to exit the VM.
* **Credential protection**: sensitive credentials such as git credentials or signing keys are never inside the sandbox with Claude Code. Authentication is handled through a secure proxy using scoped credentials.
* **Secure analysis**: code is analyzed and modified within isolated VMs before creating PRs

## Limitations

Before relying on cloud sessions for a workflow, account for these constraints:

* **Rate limits**: Claude Code on the web shares rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel consumes more rate limits proportionately. There is no separate compute charge for the cloud VM.
* **Repository authentication**: you can only move sessions from web to local when you are authenticated to the same account
* **Platform restrictions**: repository cloning and pull request creation require GitHub. Self-hosted [GitHub Enterprise Server](/en/github-enterprise-server) instances are supported for Team and Enterprise plans. GitLab, Bitbucket, and other non-GitHub repositories can be sent to cloud sessions as a [local bundle](#send-local-repositories-without-github), but the session can't push results back to the remote

## Related resources

* [Routines](/en/routines): automate work on a schedule, via API call, or in response to GitHub events
* [Hooks configuration](/en/hooks): run scripts at session lifecycle events
* [Settings reference](/en/settings): all configuration options
* [Security](/en/security): isolation guarantees and data handling
* [Data usage](/en/data-usage): what Anthropic retains from cloud sessions
