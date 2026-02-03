> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on desktop

> Run Claude Code tasks locally or on secure cloud infrastructure with the Claude desktop app

<Note>
  Claude Code on desktop is currently in preview.
</Note>

Claude Code is an AI coding assistant that works directly with your codebase. Unlike Claude.ai chat, it can read your project files, edit code, run terminal commands, and understand how different parts of your code connect. You watch changes happen in real time.

You can use Claude Code through the terminal ([CLI](/en/quickstart)) or through the desktop app described here. Both provide the same core capabilities. The desktop app adds a graphical interface and visual session management.

<CardGroup cols={2}>
  <Card title="New to Claude Code?" icon="rocket" href="#installation-and-setup">
    Start here to install and make your first edit
  </Card>

  <Card title="Coming from the CLI?" icon="terminal" href="#how-desktop-relates-to-cli">
    See what's shared and what's different
  </Card>
</CardGroup>

The desktop app has three tabs:

* **Chat**: A conversational interface for general questions and tasks (like Claude.ai)
* **Cowork**: An autonomous agent that works on tasks in the background
* **Code**: An AI coding assistant that reads and edits your project files directly

This documentation covers the **Code** tab. For the chat interface, see the [Claude Desktop support articles](https://support.claude.com/en/collections/16163169-claude-desktop).

## Installation and setup

<Steps>
  <Step title="Download the app">
    Download Claude for your platform. You'll need an Anthropic account ([sign up at claude.ai](https://claude.ai) if you don't have one).

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Universal build for Intel and Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        For x64 processors
      </Card>
    </CardGroup>

    For Windows ARM64, [download here](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs). Local sessions are not available on ARM64 devices, so use remote sessions instead.

    Linux is not currently supported.
  </Step>

  <Step title="Open the app and sign in">
    Launch Claude from your Applications folder (macOS) or Start menu (Windows). Sign in with your Anthropic account.
  </Step>

  <Step title="Select the Code tab">
    Click the **Code** tab in the top left. If clicking Code prompts you to sign in online, complete the sign-in and restart the app.
  </Step>
</Steps>

## Getting started

If you already use the CLI, you can skip to [How Desktop relates to CLI](#how-desktop-relates-to-cli) for a quick overview of differences.

<Steps>
  <Step title="Choose a folder and environment">
    Select **Local** to run Claude on your machine using your files directly. This is the best choice for getting started. Click **Select folder** and choose your project directory.

    You can also run [remote sessions](/en/claude-code-on-the-web) that continue in the cloud even if you close the app.
  </Step>

  <Step title="Start a session">
    Type what you want Claude to do:

    * "Find a TODO comment and fix it"
    * "Add tests for the main function"
    * "Create a CLAUDE.md with instructions for this codebase"

    A **session** is a conversation with Claude about your code. Each session tracks its own context and changes, so you can work on multiple tasks without them interfering with each other.
  </Step>

  <Step title="Review and accept changes">
    By default, Code is in **Ask** mode, where Claude proposes changes and waits for your approval before applying them. You'll see:

    1. **A diff view** showing exactly what will change in each file
    2. **Accept/Reject buttons** to approve or decline each change
    3. **Real-time updates** as Claude works through your request

    If you reject a change, Claude will ask how you'd like to proceed differently. Your files aren't modified until you accept.
  </Step>
</Steps>

The sections below cover commands, permission modes, parallel sessions, and ways to extend Claude Code with custom workflows and integrations.

## What you can do

Claude Code can edit files, run terminal commands, and understand how your code connects. Try prompts like:

* `Fix the bug in the login function`
* `Run the tests and fix any failures`
* `How does the authentication flow work?`

You can rename, resume, and archive sessions through the sidebar.

### Choose a permission mode

Control how Claude works using the mode selector next to the send button:

* **Ask** (recommended for new users): Claude asks for your approval before each file edit or command. You see a diff view and can accept or reject each change.
* **Code**: Claude auto-accepts file edits but still asks before running terminal commands. Use this when you trust file changes and want faster iteration.
* **Plan**: Claude creates a detailed plan for your approval before making any changes. Good for complex tasks where you want to review the approach first.

To stop Claude mid-task, click the stop button.

Remote sessions only support **Code** and **Plan** modes because they continue running in the background without requiring your active participation. See [permission modes](/en/permissions#permission-modes) for details on how these work internally.

### Work in parallel with sessions

Click **+ New session** in the sidebar to work on multiple tasks in parallel. For Git repositories, each session gets its own isolated copy of your project using worktrees, so changes in one session don't affect another until you commit them. Worktrees are stored in `~/.claude-worktrees/` by default.

<Note>
  Session isolation requires [Git](https://git-scm.com/downloads). Without Git, sessions in the same directory edit the same files, so changes in one session are immediately visible in others.
</Note>

To include files listed in your `.gitignore` (like `.env`) in new worktrees, create a `.worktreeinclude` file in your project root listing the file patterns to copy.

To manage a session, click its dropdown in the sidebar to rename it, archive it, or check context usage. When context fills up, Claude automatically summarizes the conversation. You can also ask Claude to compact if you want to free up space earlier.

### Run long-running tasks remotely

For large refactors, test suites, migrations, or other long-running tasks, select **Remote** instead of **Local** when starting a session. Remote sessions run on Anthropic's cloud infrastructure and continue even if you close the app or shut down your computer. Check back anytime to see progress or steer Claude in a different direction.

Remote sessions support **Code** and **Plan** modes. See [Claude Code on the web](/en/claude-code-on-the-web) for details on configuring remote environments.

### Review changes with diff view

After Claude makes changes to your code, the diff view lets you review modifications file by file before creating a pull request.

When Claude changes files, a diff stats indicator appears showing the number of lines added and removed (for example, `+12 -1`). Click this indicator to open the diff viewer, which displays a file list on the left and the changes for each file on the right.

To comment on specific lines, click any line in the diff to open a comment box. Type your feedback and press **Enter** to send. In the full diff view, press **Enter** to accept each comment, then **Cmd+Enter** to send them all. Claude reads your comments and makes the requested changes, which appear as a new diff you can review.

## Extend Claude Code

You can extend Claude Code with custom commands, automated workflows, and external integrations.

### Connect external tools

For local sessions, click the **...** button before starting and select **Connectors** to add integrations like Google Calendar, Slack, GitHub, Linear, Notion, and more. Connectors must be configured before the session starts and are only available for local sessions. Once connected, Claude can read your calendar, send messages, create issues, and interact with your tools directly. You can ask Claude what connectors are configured in your session.

Connectors are [MCP (Model Context Protocol) servers](/en/mcp) with built-in setup. You can also [create custom connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp) or add MCP servers manually via [configuration files](/en/mcp#configure-mcp-servers).

### Create custom skills

[Skills](/en/skills) are reusable prompts that extend Claude's capabilities. For example, you could create a `review` skill that runs your standard code review checklist, or a `deploy` skill that walks through your deployment steps. Skills are defined as markdown files in `.claude/skills/` and can include instructions, context, and even call other tools. Ask Claude what skills are available or to run a specific skill. Claude can also help you create a skill if you describe what you want, or see [skills](/en/skills) to learn how to write them yourself.

### Automate workflows with hooks

[Hooks](/en/hooks) run shell commands automatically in response to Claude Code events. For example, you could run a linter after every file edit, auto-format code, or send notifications when tasks complete. Hooks are configured in your [settings files](/en/settings). See [hooks](/en/hooks) for available events and configuration examples.

## Environment configuration

When starting a session, you choose between **Local** (runs on your machine) or **Remote** (runs on Anthropic's cloud).

**Local sessions** inherit environment variables from your shell. If you need additional variables, set them in your shell profile (`~/.zshrc`, `~/.bashrc`) and restart the desktop app. See [environment variables](/en/settings#environment-variables) for the full list of supported variables.

[Extended thinking](/en/common-workflows#use-extended-thinking-thinking-mode) is enabled by default, which improves performance on complex reasoning tasks but uses additional tokens. The thinking process runs in the background but isn't displayed in the Desktop interface. To disable it or adjust the budget, set `MAX_THINKING_TOKENS` in your shell profile (use `0` to disable).

**Remote sessions** run on Anthropic's cloud infrastructure and continue even if you close the app. Usage counts toward your subscription plan limits with no separate compute charges. See [Claude Code on the web](/en/claude-code-on-the-web) for details on configuring remote environments.

## How Desktop relates to CLI

If you already use the Claude Code CLI, Desktop runs the same underlying engine with a graphical interface. You can run both simultaneously on the same machine, even on the same project. Each maintains separate session history, but they share configuration and project memory (CLAUDE.md files).

### CLI flag equivalents

If you're used to CLI flags, the table below shows the Desktop equivalent for each. Some flags have no Desktop equivalent because they're designed for scripting or automation.

| CLI                                   | Desktop equivalent                             |
| ------------------------------------- | ---------------------------------------------- |
| `--model sonnet`                      | **...** menu > Model (before starting session) |
| `--resume`, `--continue`              | Click a session in the sidebar                 |
| `--allowedTools`, `--disallowedTools` | Not available in Desktop                       |
| `--dangerously-skip-permissions`      | Not available in Desktop                       |
| `--print`                             | Not available (Desktop is interactive)         |

### Shared configuration

Desktop and CLI read the same configuration files, so your setup carries over:

* **[CLAUDE.md](/en/memory)** and **CLAUDE.local.md** files in your project are used by both
* **[MCP servers](/en/mcp)** configured in `~/.claude.json` or `.mcp.json` work in both
* **[Hooks](/en/hooks)** and **[skills](/en/skills)** defined in settings apply to both
* **[Settings](/en/settings)** in `~/.claude.json` and `~/.claude/settings.json` are shared
* **Models** (Sonnet, Opus, Haiku) are available in both (Desktop requires selecting before starting a session)

<Note>
  MCP servers configured for the **Claude Desktop chat app** (in `claude_desktop_config.json`) are separate from Claude Code. To use MCP servers in Claude Code, configure them in `~/.claude.json` or your project's `.mcp.json` file. See [MCP configuration](/en/mcp#configure-mcp-servers) for details.
</Note>

### What's different

**Desktop adds:**

* Graphical interface with visual session management
* Built-in connectors for common integrations
* Automatic session isolation for Git repositories (each session gets its own worktree)

**CLI adds:**

* [Third-party API providers](/en/third-party-integrations) (Bedrock, Vertex, Foundry). If you use these, continue using CLI for those projects.
* [CLI flags](/en/cli-reference) for scripting (`--print`, `--resume`, `--continue`)
* [Programmatic usage](/en/headless) via the Agent SDK

## Troubleshooting

Solutions to common issues with the Claude desktop app. For CLI issues, see [CLI troubleshooting](/en/troubleshooting).

### Check your version

To see which version of the desktop app you're running:

* **macOS**: Click **Claude** in the menu bar, then **About Claude**
* **Windows**: Click **Help**, then **About**

Click the version number to copy it to your clipboard.

### "Branch doesn't exist yet" when opening in CLI

Remote sessions can create branches that don't exist on your local machine. Click the branch name in the session toolbar to copy it, then fetch it locally:

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### "Failed to load session" error

This error can occur for several reasons:

* The selected folder no longer exists or is inaccessible
* A Git repository requires Git LFS but it's not installed (see [Git LFS errors](#git-lfs-errors))
* File permissions prevent access to the project directory

Try selecting a different folder or restarting the desktop app.

### App won't quit

If the desktop app doesn't close properly:

* **macOS**: Press Cmd+Q. If the app doesn't respond, use Force Quit (Cmd+Option+Esc, select Claude, click Force Quit).
* **Windows**: Use Task Manager (Ctrl+Shift+Esc) to end the Claude process.

### Windows installation issues

If the installer fails silently or doesn't complete properly:

1. **PATH not updated**: After installation, open a new terminal window. The PATH updates only apply to new terminal sessions.
2. **Concurrent installation error**: If you see an error about another installation in progress but there isn't one, try running the installer as Administrator.

### Session not finding installed tools

If Claude can't find tools like `npm`, `node`, or other CLI commands:

1. Verify the tools work in your regular terminal
2. Check that your shell profile (`~/.zshrc`, `~/.bashrc`) properly sets up PATH
3. Restart the desktop app to reload environment variables

### MCP servers not working (Windows)

If MCP server toggles don't respond or servers fail to connect on Windows:

1. Check that the MCP server is properly configured in your settings
2. Restart the desktop app after making changes
3. Verify the MCP server process is running (check Task Manager)
4. Review the server logs for connection errors

### Git LFS errors

If you see "Git LFS is required by this repository but is not installed," your repository uses Git Large File Storage for large binary files. Install Git LFS before opening this repository:

1. Install Git LFS from [git-lfs.com](https://git-lfs.com/)
2. Run `git lfs install` in your terminal
3. Restart the desktop app

## Enterprise configuration

Organizations can disable local Claude Code use in the desktop application with the `isClaudeCodeForDesktopEnabled` [enterprise policy option](https://support.claude.com/en/articles/12622667-enterprise-configuration#h_003283c7cb). Additionally, Claude Code on the web can be disabled in your [admin settings](https://claude.ai/admin-settings/claude-code).

## Related resources

* [Claude Code on the web](/en/claude-code-on-the-web): Run remote sessions that continue in the cloud
* [CLI reference](/en/cli-reference): Use Claude Code in your terminal with flags and scripting
* [Common workflows](/en/common-workflows): Tutorials for debugging, refactoring, testing, and more
* [Settings reference](/en/settings): Configure Claude Code behavior with settings files
* [Claude Desktop support](https://support.claude.com/en/collections/16163169-claude-desktop): Help articles for the Chat tab and general desktop app usage
* [Enterprise configuration](https://support.claude.com/en/articles/12622667-enterprise-configuration): Admin policies for organizational deployments
