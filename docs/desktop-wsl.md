> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code Desktop in WSL

> Run Code sessions inside a WSL 2 distribution on Windows

On Windows, the Code tab can run a session inside a WSL 2 distribution instead of on Windows itself. The session's Claude Code process, its tools, and git all execute inside the distribution, using its Linux toolchain and native Linux paths, the same environment your project targets.

Use a WSL session when your repository lives inside the distribution's filesystem. Working on those files from Windows goes through a network filesystem, which is slow and breaks file watching; running the session inside the distribution avoids both.

## Requirements

* Windows 10 or 11 with [WSL 2](https://learn.microsoft.com/windows/wsl/install). WSL 1 isn't supported.
* At least one installed distribution (for example, Ubuntu).
* `git` installed inside the distribution.

## Start a WSL session

<Steps>
  <Step title="Pick a distribution">
    Start a new session in the Code tab and open the environment picker. Your installed WSL 2 distributions appear in a **WSL** section. Pick one.
  </Step>

  <Step title="Choose a folder">
    The session starts in the distribution's home directory. Use the folder picker to choose a project folder. Browsing happens inside the distribution, with Linux paths like `/home/you/project`.
  </Step>

  <Step title="Trust the folder">
    The first session in a folder shows the workspace trust dialog. Trust is granted per distribution and folder; trusting a folder in one distribution doesn't apply to another distribution or to the same path on Windows.
  </Step>
</Steps>

The first session in a distribution takes a little longer while Claude sets up inside it. You can also open a `\\wsl.localhost\...` folder from the normal folder picker, and it reopens inside that distribution.

Folders you've used recently appear in the picker per distribution, so reconnecting to a project is one click.

## What works in a WSL session

Parallel sessions, side chats, visual diff review, branch and pull request status, and worktrees all work, backed by the git and toolchain inside the distribution. "Open in editor" opens VS Code connected to the distribution through [Remote - WSL](https://code.visualstudio.com/docs/remote/wsl).

A few features aren't available in WSL sessions yet: the integrated terminal, connectors and plugins, session forking, the file browser pane, and file suggestions when you type `@` in the composer.

## Managed devices

On devices managed by an organization, WSL sessions may be unavailable. If session start fails with a message that the device is managed, that's controlled by your administrator. Administrators: see [how settings reach devices](/docs/en/admin-setup#decide-how-settings-reach-devices) in the deployment guide.
