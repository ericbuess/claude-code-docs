> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Quickstart

> Install Claude Code in your terminal, sign in, and use the CLI to explore your codebase and make your first code change.

This quickstart covers Claude Code in your terminal: installing the CLI, signing in from your first session, and using it for common development tasks in your own project.

## Before you begin

Make sure you have:

* A terminal or command prompt open
* A code project to work with
* A [Claude subscription](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_prereq) (Pro, Max, Team, or Enterprise), [Claude Console](https://platform.claude.com/) account, or access through a [supported cloud provider](https://code.claude.com/docs/en/third-party-integrations.md)

> [!NOTE]
>
> These cases are covered on other pages:
>
> * **Never used a terminal before**: start with the [terminal guide](https://code.claude.com/docs/en/terminal-guide)
> * **Want Claude Code somewhere other than the terminal**: Claude Code is also available on the [web](https://claude.ai/code), as a [desktop app](https://code.claude.com/docs/en/desktop.md), in [VS Code](https://code.claude.com/docs/en/vs-code.md) and [JetBrains IDEs](https://code.claude.com/docs/en/jetbrains.md), in [Slack](https://code.claude.com/docs/en/slack.md), and in CI/CD with [GitHub Actions](https://code.claude.com/docs/en/github-actions.md) and [GitLab](https://code.claude.com/docs/en/gitlab-ci-cd.md). See [all interfaces](https://code.claude.com/docs/en/overview.md#use-claude-code-everywhere).

## Step 1: Install Claude Code

To install Claude Code, open a terminal and run the command for your system. If you haven't used a terminal before, the [terminal guide](https://code.claude.com/docs/en/terminal-guide) shows how to open one and paste the command.

**Native Install (Recommended)**

**macOS, Linux, WSL:**

```bash theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

On Windows, your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

**Windows PowerShell:**

```powershell theme={null}
irm https://claude.ai/install.ps1 | iex
```

**Windows CMD:**

```batch theme={null}
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

The install command shows no progress while it downloads Claude Code. When the installer finishes, open a new terminal window and run `claude --version`. A working installation prints a version number. If your shell says `claude` isn't found or isn't recognized, the install directory isn't on your PATH yet: see [Fix your PATH](https://code.claude.com/docs/en/troubleshoot-install.md#command-not-found-claude-after-installation).

If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell.

If the install command fails with `syntax error near unexpected token '<'`, a `403`, or any other error, see [Troubleshoot installation](https://code.claude.com/docs/en/troubleshoot-install.md#find-your-error) to match the error to a fix and for alternative install methods.

[Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

> [!NOTE]
>
> Native installations automatically update in the background to keep you on the latest version.

**Homebrew**

```bash theme={null}
brew install --cask claude-code
```

Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

> [!NOTE]
>
> Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.

**WinGet**

```powershell theme={null}
winget install Anthropic.ClaudeCode
```

> [!NOTE]
>
> WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.

You can also install with [apt, dnf, or apk](https://code.claude.com/docs/en/setup.md#install-with-linux-package-managers) on Debian, Fedora, RHEL, and Alpine.

To confirm the installation worked, run:

```bash theme={null}
claude --version
```

The command prints a version number followed by `(Claude Code)`.

## Step 2: Start your first session

Open your terminal in any project directory and start Claude Code:

```bash theme={null}
cd /path/to/your/project
claude
```

Replace `/path/to/your/project` with the path to the project you want to work on.

Claude Code prompts you to log in on first use. For Claude subscription or Console accounts, follow the prompts to complete authentication in your browser. If you've set the `ANTHROPIC_API_KEY` environment variable and you approve the key when Claude Code asks whether to use it, Claude Code skips the login prompt.

You can log in using any of these account types:

* [Claude Pro, Max, Team, or Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_login) (recommended)
* [Claude Console](https://platform.claude.com/) (API access with pre-paid credits). On first login, a "Claude Code" workspace is automatically created in the Console for centralized cost tracking.
* [Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry](https://code.claude.com/docs/en/third-party-integrations.md) (enterprise cloud providers)
* A self-hosted [Claude apps gateway](https://code.claude.com/docs/en/claude-apps-gateway), if your organization runs one: your admin pre-configures the gateway URL, and `/login` opens directly on the **Cloud gateway** screen for you to sign in with corporate SSO

Once logged in, your credentials are stored and you won't need to log in again. Learn more in [Credential Management](https://code.claude.com/docs/en/authentication.md#credential-management).

The Claude Code prompt appears with the version, current model, and working directory shown above it. Type `/help` for available commands or `/resume` to continue a previous conversation. To switch accounts later or re-authenticate, type `/login` inside the running session.

## Step 3: Ask your first question

Try one of these commands:

```text wrap theme={null}
what does this project do?
```

Claude will analyze your files and provide a summary. You can also ask more specific questions:

```text wrap theme={null}
what technologies does this project use?
```

```text wrap theme={null}
where is the main entry point?
```

```text wrap theme={null}
explain the folder structure
```

You can also ask Claude about its own capabilities:

```text wrap theme={null}
what can Claude Code do?
```

```text wrap theme={null}
how do I create custom skills in Claude Code?
```

```text wrap theme={null}
can Claude Code work with Docker?
```

> [!NOTE]
>
> Claude Code reads your project files as needed. You don't have to manually add context.

## Step 4: Make your first code change

Try a small task:

```text wrap theme={null}
add a hello world function to the main file
```

Claude Code finds the appropriate file and shows you the change. If it asks before making the change, select **Yes** to approve.

The session's [permission mode](https://code.claude.com/docs/en/permission-modes.md) sets which actions Claude can take without asking you first. Press `Shift+Tab` at any time to switch the permission mode of the session you're in.

## Step 5: Use Git with Claude Code

Claude Code makes Git operations conversational:

```text wrap theme={null}
what files have I changed?
```

```text wrap theme={null}
commit my changes with a descriptive message
```

You can also prompt for more complex Git operations:

```text wrap theme={null}
create a new branch called feature/quickstart
```

```text wrap theme={null}
show me the last 5 commits
```

```text wrap theme={null}
help me resolve merge conflicts
```

## Step 6: Fix a bug or add a feature

Describe what you want in natural language:

```text wrap theme={null}
add input validation to the user registration form
```

Or fix existing issues:

```text wrap theme={null}
there's a bug where users can submit empty forms - fix it
```

## Step 7: Test out other common workflows

Try a few more prompts. You can ask Claude to refactor code, write tests, update documentation, or review your changes:

```text wrap theme={null}
refactor the authentication module to use async/await instead of callbacks
```

```text wrap theme={null}
write unit tests for the calculator functions
```

```text wrap theme={null}
update the README with installation instructions
```

```text wrap theme={null}
review my changes and suggest improvements
```

> [!TIP]
>
> Talk to Claude like you would a helpful colleague. Describe what you want to achieve, and it will help you get there.

## Essential commands

Here are the most important commands for daily use, grouped by where you run them.

### Shell commands

Run these from your terminal to start or resume Claude Code.

| Command | What it does | Example |
| - | - | - |
| `claude` | Start interactive mode | `claude` |
| `claude "task"` | Start interactive mode with an initial prompt | `claude "fix the build error"` |
| `claude -p "query"` | Run one-off query, then exit | `claude -p "explain this function"` |
| `claude -c` | Continue most recent conversation in current directory | `claude -c` |
| `claude -r` | Resume a previous conversation | `claude -r` |

See the [CLI reference](https://code.claude.com/docs/en/cli-reference.md) for the complete list of shell commands.

### Session commands

Run these inside Claude Code after it starts.

| Command | What it does | Example |
| - | - | - |
| `/clear` | Clear conversation history | `/clear` |
| `/help` | Show available commands | `/help` |
| `/exit` or Ctrl+D twice | Exit Claude Code | `/exit` |

See the [commands reference](https://code.claude.com/docs/en/commands.md) for the complete list of session commands.

## Pro tips for beginners

For more, see [best practices](https://code.claude.com/docs/en/best-practices.md) and [common workflows](https://code.claude.com/docs/en/common-workflows.md).

> **Be specific with your requests**
>
> Instead of: "fix the bug"
>
> Try: "fix the login bug where users see a blank screen after entering wrong credentials"

> **Use step-by-step instructions**
>
> Break complex tasks into steps:
>
> ```text wrap theme={null}
> 1. create a new database table for user profiles
> 2. create an API endpoint to get and update user profiles
> 3. build a webpage that allows users to see and edit their information
> ```

> **Let Claude explore first**
>
> Before making changes, let Claude understand your code:
>
> ```text wrap theme={null}
> analyze the database schema
> ```
>
> ```text wrap theme={null}
> build a dashboard showing products that are most frequently returned by our UK customers
> ```

> **Save time with shortcuts**
>
> * Type `/` to see the commands and skills available to you
> * Use Tab for command completion
> * Press ↑ for command history
> * Press `Shift+Tab` to cycle permission modes

## What's next?

Now that you've learned the basics, explore more advanced features:

* [How Claude Code works](https://code.claude.com/docs/en/how-claude-code-works.md): understand the agentic loop, built-in tools, and how Claude Code interacts with your project
* [Best practices](https://code.claude.com/docs/en/best-practices.md): get better results with effective prompting and project setup
* [Common workflows](https://code.claude.com/docs/en/common-workflows.md): step-by-step guides for common tasks
* [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md): customize with CLAUDE.md, skills, hooks, MCP, and more

See [advanced setup](https://code.claude.com/docs/en/setup.md) for installation options, manual updates, or uninstallation instructions.

## Getting help

* **In Claude Code**: type `/help` or ask a "how do I" question
* **Documentation**: browse the other guides on this site
* **Courses**: take [Claude Code 101](https://academy.claude.com/courses/claude-code-101) and other free self-paced courses on [Claude Academy](https://academy.claude.com/)
* **Community**: join the [Discord server](https://www.anthropic.com/discord) for tips and support
