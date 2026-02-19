> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code Desktop

> Get more out of Claude Code Desktop: parallel sessions with Git isolation, visual diff review, permission modes, connectors, and enterprise configuration.

The Code tab in the Desktop app lets you use Claude Code through a graphical interface instead of the terminal. You get visual diff review with inline comments, permission modes that control how much Claude does on its own, parallel sessions with automatic Git isolation, and connectors that integrate tools like GitHub, Slack, and Linear. Sessions can run locally, on a remote machine over [SSH](#ssh-sessions), or in [the cloud](#run-long-running-tasks-remotely).

<Tip>
  New to Desktop? Start with [Get started](/en/desktop-quickstart) to install the app and make your first edit.
</Tip>

This page covers [working with code](#work-with-code), [managing sessions](#manage-sessions), [extending Claude Code](#extend-claude-code), and [configuration](#environment-configuration). It also includes a [CLI comparison](#coming-from-the-cli) and [troubleshooting](#troubleshooting).

## Start a session

Before you send your first message, configure four things in the prompt area:

* **Environment**: choose where Claude runs. Select **Local** for your machine, a **cloud environment** for Anthropic-hosted sessions, or an [**SSH connection**](#ssh-sessions) for a remote machine you manage. See [environment configuration](#environment-configuration).
* **Project folder**: select the folder or repository Claude works in. For remote sessions, you can add [multiple repositories](#run-long-running-tasks-remotely).
* **Model**: pick a [model](/en/overview#models) from the dropdown next to the send button. The model is locked once the session starts.
* **Permission mode**: choose how much autonomy Claude has from the [mode selector](#choose-a-permission-mode). You can change this during the session.

Type your task and press **Enter** to start. Each session tracks its own context and changes independently.

## Work with code

Give Claude the right context, control how much it does on its own, and review what it changed.

### Use the prompt box

Type what you want Claude to do and press **Enter** to send. Claude reads your project files, makes changes, and runs commands based on your [permission mode](#choose-a-permission-mode). You can interrupt Claude at any point: click the stop button or type your correction and press **Enter**. Claude stops what it's doing and adjusts based on your input.

The **+** button next to the prompt box gives you access to file attachments, [skills](#use-skills), [connectors](#connect-external-tools), and [plugins](#install-plugins).

### Add files and context to prompts

The prompt box supports two ways to bring in external context:

* **@mention files**: type `@` followed by a filename to add a file to the conversation context. Claude can then read and reference that file.
* **Attach files**: attach images, PDFs, and other files to your prompt using the attachment button, or drag and drop files directly into the prompt. This is useful for sharing screenshots of bugs, design mockups, or reference documents.

### Choose a permission mode

Permission modes control how much autonomy Claude has during a session: whether it asks before editing files, running commands, or both. You can switch modes at any time using the mode selector next to the send button. Start with Ask mode to see exactly what Claude does, then move to Code or Plan as you get comfortable.

| Mode     | Settings key        | Behavior                                                                                                                                                                                                                                                                     |
| -------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ask**  | `default`           | Claude asks for your approval before each file edit or command. You see a diff view and can accept or reject each change. Recommended for new users.                                                                                                                         |
| **Code** | `acceptEdits`       | Claude auto-accepts file edits but still asks before running terminal commands. Use this when you trust file changes and want faster iteration.                                                                                                                              |
| **Plan** | `plan`              | Claude analyzes your code and creates a plan without modifying files or running commands. Good for complex tasks where you want to review the approach first.                                                                                                                |
| **Act**  | `bypassPermissions` | Claude runs without any permission prompts, equivalent to `--dangerously-skip-permissions` in the CLI. Enable in your Settings → Claude Code under "Allow bypass permissions mode". Only use this in sandboxed containers or VMs. Enterprise admins can disable this option. |

The `dontAsk` permission mode is available only in the [CLI](/en/permissions#permission-modes).

<Tip title="Best practice">
  Start complex tasks in Plan mode so Claude maps out an approach before making changes. Once you approve the plan, switch to Code or Ask mode to execute it. See [explore first, then plan, then code](/en/best-practices#explore-first-then-plan-then-code) for more on this workflow.
</Tip>

Remote sessions support Code mode and Plan mode. Ask mode is not available because remote sessions auto-accept file edits by default, and Act mode is not available because the remote environment is already sandboxed.

Enterprise admins can restrict which permission modes are available. See [enterprise configuration](#enterprise-configuration) for details.

### Review changes with diff view

After Claude makes changes to your code, the diff view lets you review modifications file by file before creating a pull request.

When Claude changes files, a diff stats indicator appears showing the number of lines added and removed, such as `+12 -1`. Click this indicator to open the diff viewer, which displays a file list on the left and the changes for each file on the right.

To comment on specific lines, click any line in the diff to open a comment box. Type your feedback and press **Enter** to add the comment. After adding comments to multiple lines, submit all comments at once:

* **macOS**: press **Cmd+Enter**
* **Windows**: press **Ctrl+Enter**

Claude reads your comments and makes the requested changes, which appear as a new diff you can review.

## Manage sessions

Each session is an independent conversation with its own context and changes. You can run multiple sessions in parallel or send work to the cloud.

### Work in parallel with sessions

Click **+ New session** in the sidebar to work on multiple tasks in parallel. For Git repositories, each session gets its own isolated copy of your project using [Git worktrees](/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), so changes in one session don't affect other sessions until you commit them.

Worktrees are stored in `<project-root>/.claude/worktrees/` by default. You can change this to a custom directory in Settings → Claude Code under "Worktree location". You can also set a branch prefix that gets prepended to every worktree branch name, which is useful for keeping Claude-created branches organized. To remove a worktree when you're done, hover over the session in the sidebar and click the archive icon.

<Note>
  Session isolation requires [Git](https://git-scm.com/downloads). Most Macs include Git by default. Run `git --version` in Terminal to check. On Windows, [download Git](https://git-scm.com/downloads) if you don't have it.

  Without Git, sessions share the same files and changes in one session are immediately visible in others.
</Note>

Use the filter icon at the top of the sidebar to filter sessions by status (Active, Archived) and environment (Local, Cloud). To rename a session or check context usage, click the session title in the toolbar at the top of the active session. When context fills up, Claude automatically summarizes the conversation and continues working. You can also type "compact this conversation" to trigger summarization earlier and free up context space. See [the context window](/en/how-claude-code-works#the-context-window) for details on how compaction works.

### Run long-running tasks remotely

For large refactors, test suites, migrations, or other long-running tasks, select **Remote** instead of **Local** when starting a session. Remote sessions run on Anthropic's cloud infrastructure and continue even if you close the app or shut down your computer. Check back anytime to see progress or steer Claude in a different direction. You can also monitor remote sessions from [claude.ai/code](https://claude.ai/code) or the Claude iOS app.

Remote sessions also support multiple repositories. After selecting a cloud environment, click the **+** button next to the repo pill to add additional repositories to the session. Each repo gets its own branch selector. This is useful for tasks that span multiple codebases, such as updating a shared library and its consumers.

See [Claude Code on the web](/en/claude-code-on-the-web) for more on how remote sessions work.

### Continue in another surface

The **Continue in** menu, accessible from the VS Code icon in the bottom right of the session toolbar, lets you move your session to another surface:

* **Claude Code on the Web**: sends your local session to continue running remotely. Desktop pushes your branch, generates a summary of the conversation, and creates a new remote session with the full context. You can then choose to archive the local session or keep it. This requires a clean working tree, and is not available for SSH sessions.
* **Your IDE**: opens your project in a supported IDE at the current working directory.

## Extend Claude Code

Connect external services, add reusable workflows, and customize Claude's behavior for your project.

### Connect external tools

For local and [SSH](#ssh-sessions) sessions, click the **+** button next to the prompt box and select **Connectors** to add integrations like Google Calendar, Slack, GitHub, Linear, Notion, and more. You can add connectors before or during a session. Connectors are not available for remote sessions.

To manage or disconnect connectors, go to Settings → Connectors in the desktop app, or select **Manage connectors** from the Connectors menu in the prompt box.

Once connected, Claude can read your calendar, send messages, create issues, and interact with your tools directly. You can ask Claude what connectors are configured in your session.

Connectors are [MCP servers](/en/mcp) with a graphical setup flow. Use them for quick integration with supported services. For integrations not listed in Connectors, add MCP servers manually via [settings files](/en/mcp#installing-mcp-servers). You can also [create custom connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Use skills

[Skills](/en/skills) extend what Claude can do. Claude loads them automatically when relevant, or you can invoke one directly: type `/` in the prompt box or click the **+** button and select **Slash commands** to browse what's available. This includes [built-in commands](/en/interactive-mode#built-in-commands), your [custom skills](/en/skills#create-custom-skills), project skills from your codebase, and skills from any [installed plugins](/en/plugins). Select one and it appears highlighted in the input field. Type your task after it and send as usual.

### Install plugins

[Plugins](/en/plugins) are reusable packages that add skills, agents, hooks, MCP servers, and LSP configurations to Claude Code. You can install plugins from the desktop app without using the terminal.

For local and [SSH](#ssh-sessions) sessions, click the **+** button next to the prompt box and select **Plugins** to see your installed plugins and their commands. To add a plugin, select **Add plugin** from the submenu to open the plugin browser, which shows available plugins from your configured [marketplaces](/en/plugin-marketplaces) including the official Anthropic marketplace. Select **Manage plugins** to enable, disable, or uninstall plugins.

Plugins can be scoped to your user account, a specific project, or local-only. Plugins are not available for remote sessions. For the full plugin reference including creating your own plugins, see [plugins](/en/plugins).

## Environment configuration

When starting a session, you choose between three environments:

* **Local**: runs on your machine with direct access to your files
* **Remote**: runs on Anthropic's cloud infrastructure. Sessions continue even if you close the app.
* **SSH**: runs on a remote machine you connect to over SSH, such as your own servers, cloud VMs, or dev containers

### Local sessions

Local sessions inherit environment variables from your shell. If you need additional variables, set them in your shell profile, such as `~/.zshrc` or `~/.bashrc`, and restart the desktop app. See [environment variables](/en/settings#environment-variables) for the full list of supported variables.

[Extended thinking](/en/common-workflows#use-extended-thinking-thinking-mode) is enabled by default, which improves performance on complex reasoning tasks but uses additional tokens. To disable it or adjust the budget, set `MAX_THINKING_TOKENS` in your shell profile. Use `0` to disable.

### Remote sessions

Remote sessions continue in the background even if you close the app. Usage counts toward your [subscription plan limits](/en/costs) with no separate compute charges.

You can create custom cloud environments with different network access levels and environment variables. Select the environment dropdown when starting a remote session and choose **Add environment**. See [cloud environments](/en/claude-code-on-the-web#cloud-environments) for details on configuring network access and environment variables.

### SSH sessions

SSH sessions let you run Claude Code on a remote machine while using the desktop app as your interface. This is useful for working with codebases that live on cloud VMs, dev containers, or servers with specific hardware or dependencies.

To add an SSH connection, click the environment dropdown before starting a session and select **+ Add SSH connection**. The dialog asks for:

* **Name**: a friendly label for this connection
* **SSH Host**: `user@hostname` or a host defined in `~/.ssh/config`
* **SSH Port**: defaults to 22 if left empty, or uses the port from your SSH config
* **Identity File**: path to your private key, such as `~/.ssh/id_rsa`. Leave empty to use the default key or your SSH config.

Once added, the connection appears in the environment dropdown. Select it to start a session on that machine. Claude runs on the remote machine with access to its files and tools.

SSH sessions support permission modes, connectors, plugins, and MCP servers. Claude Code must be installed on the remote machine.

## Enterprise configuration

Organizations on Teams or Enterprise plans can manage desktop app behavior through admin console controls, managed settings files, and device management policies.

### Admin console controls

These settings are configured through the [admin settings console](https://claude.ai/admin-settings/claude-code):

* **Enable or disable the Code tab**: control whether users in your organization can access Claude Code in the desktop app
* **Disable Act mode**: prevent users in your organization from enabling bypass permissions mode
* **Disable Claude Code on the web**: enable or disable remote sessions for your organization

### Managed settings

Managed settings override project and user settings and apply when Desktop spawns CLI sessions. You can set these keys in your organization's [managed settings](/en/settings#settings-precedence) file or push them remotely through the admin console.

| Key                                        | Description                                                                                                      |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `permissions.disableBypassPermissionsMode` | set to `"disable"` to prevent users from enabling Act mode. See [permissions](/en/permissions#managed-settings). |

Remote managed settings uploaded through the admin console currently apply to CLI and IDE sessions only. For Desktop-specific restrictions, use the admin console controls above.

### Device management policies

IT teams can manage the desktop app through MDM on macOS or group policy on Windows. Available policies include enabling or disabling the Claude Code feature, controlling auto-updates, and setting a custom deployment URL.

* **macOS**: configure via `com.anthropic.Claude` preference domain using tools like Jamf or Kandji
* **Windows**: configure via registry at `SOFTWARE\Policies\Claude`

### Authentication and SSO

Enterprise organizations can require SSO for all users. See [authentication](/en/authentication) for plan-level details and [Setting up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) for SAML and OIDC configuration.

### Data handling

Claude Code processes your code locally in local sessions or on Anthropic's cloud infrastructure in remote sessions. Conversations and code context are sent to Anthropic's API for processing. See [data handling](/en/data-usage) for details on data retention, privacy, and compliance.

### Deployment

Desktop can be distributed through enterprise deployment tools:

* **macOS**: distribute via MDM such as Jamf or Kandji using the `.dmg` installer
* **Windows**: deploy via MSIX package or `.exe` installer. See [Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) for enterprise deployment options including silent installation

For network configuration such as proxy settings, firewall allowlisting, and LLM gateways, see [network configuration](/en/network-config).

For the full enterprise configuration reference, see the [enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Coming from the CLI?

If you already use the Claude Code CLI, Desktop runs the same underlying engine with a graphical interface. You can run both simultaneously on the same machine, even on the same project. Each maintains separate session history, but they share configuration and project memory via CLAUDE.md files.

To move a CLI session into Desktop, run `/desktop` in the terminal. Claude saves your session and opens it in the desktop app, then exits the CLI. This command is available on macOS and Windows only.

<Tip>
  When to use Desktop vs CLI: use Desktop when you want visual diff review, file attachments, or session management in a sidebar. Use the CLI when you need scripting, automation, third-party providers, or prefer a terminal workflow.
</Tip>

### CLI flag equivalents

This table shows the desktop app equivalent for common CLI flags. Flags not listed have no desktop equivalent because they are designed for scripting or automation.

| CLI                                   | Desktop equivalent                                                                                            |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                      | model dropdown next to the send button, before starting a session                                             |
| `--resume`, `--continue`              | click a session in the sidebar                                                                                |
| `--permission-mode`                   | mode selector next to the send button                                                                         |
| `--dangerously-skip-permissions`      | Settings → Claude Code → "Allow bypass permissions mode". Enterprise admins can disable this setting.         |
| `--add-dir`                           | add multiple repos with the **+** button in remote sessions                                                   |
| `--allowedTools`, `--disallowedTools` | not available in Desktop                                                                                      |
| `--verbose`                           | not available. Check system logs: Console.app on macOS, Event Viewer → Application on Windows                 |
| `--print`, `--output-format`          | not available. Desktop is interactive only.                                                                   |
| `ANTHROPIC_MODEL` env var             | model dropdown next to the send button                                                                        |
| `MAX_THINKING_TOKENS` env var         | set in shell profile; applies to local sessions. See [environment configuration](#environment-configuration). |

### Shared configuration

Desktop and CLI read the same configuration files, so your setup carries over:

* **[CLAUDE.md](/en/memory)** and **CLAUDE.local.md** files in your project are used by both
* **[MCP servers](/en/mcp)** configured in `~/.claude.json` or `.mcp.json` work in both
* **[Hooks](/en/hooks)** and **[skills](/en/skills)** defined in settings apply to both
* **[Settings](/en/settings)** in `~/.claude.json` and `~/.claude/settings.json` are shared. Permission rules, allowed tools, and other settings in `settings.json` apply to Desktop sessions.
* **Models**: Sonnet, Opus, and Haiku are available in both. In Desktop, select the model from the dropdown next to the send button before starting a session. You cannot change the model during an active session.

<Note>
  **MCP servers: desktop chat app vs Claude Code**: MCP servers configured for the Claude Desktop chat app in `claude_desktop_config.json` are separate from Claude Code and will not appear in the Code tab. To use MCP servers in Claude Code, configure them in `~/.claude.json` or your project's `.mcp.json` file. See [MCP configuration](/en/mcp#installing-mcp-servers) for details.
</Note>

### Feature comparison

This table compares core capabilities between the CLI and Desktop. For a full list of CLI flags, see the [CLI reference](/en/cli-reference).

| Feature                                               | CLI                                                       | Desktop                                                      |
| ----------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| Permission modes                                      | all modes including `dontAsk`                             | Ask, Code, Plan, and Act via Settings                        |
| `--dangerously-skip-permissions`                      | CLI flag                                                  | Settings → Claude Code → "Allow bypass permissions mode"     |
| [Third-party providers](/en/third-party-integrations) | Bedrock, Vertex, Foundry                                  | not available. Desktop connects to Anthropic's API directly. |
| [MCP servers](/en/mcp)                                | configure in settings files                               | Connectors UI for local and SSH sessions, or settings files  |
| [Plugins](/en/plugins)                                | `/plugin` command                                         | plugin manager UI                                            |
| @mention files                                        | text-based                                                | with autocomplete                                            |
| File attachments                                      | not available                                             | images, PDFs                                                 |
| Session isolation                                     | manual via git worktrees                                  | automatic worktrees                                          |
| Multiple sessions                                     | separate terminals                                        | sidebar tabs                                                 |
| Scripting and automation                              | [`--print`](/en/cli-reference), [Agent SDK](/en/headless) | not available                                                |

### What's not available in Desktop

* **Third-party providers**: Desktop connects to Anthropic's API directly. Use the [CLI](/en/quickstart) with Bedrock, Vertex, or Foundry instead.
* **Linux**: the desktop app is available on macOS and Windows only.
* **Inline code suggestions**: Desktop does not provide autocomplete-style suggestions. It works through conversational prompts and explicit code changes.
* **Agent teams**: multi-agent orchestration is available via the [CLI](/en/agent-teams) and [Agent SDK](/en/headless), not in Desktop.

## Troubleshooting

### Check your version

To see which version of the desktop app you're running:

* **macOS**: click **Claude** in the menu bar, then **About Claude**
* **Windows**: click **Help**, then **About**

Click the version number to copy it to your clipboard.

### 403 or authentication errors in the Code tab

If you see `Error 403: Forbidden` or other authentication failures when using the Code tab:

1. Sign out and back in from the app menu. This is the most common fix.
2. Verify you have an active paid subscription: Pro, Max, Teams, or Enterprise.
3. If the CLI works but Desktop does not, quit the desktop app completely, not just close the window, then reopen and sign in again.
4. Check your internet connection and proxy settings.

### Blank or stuck screen on launch

If the app opens but shows a blank or unresponsive screen:

1. Restart the app.
2. Check for pending updates. The app auto-updates on launch.
3. On Windows, check Event Viewer for crash logs under **Windows Logs → Application**.

### "Failed to load session"

If you see `Failed to load session`, the selected folder may no longer exist, a Git repository may require Git LFS that isn't installed, or file permissions may prevent access. Try selecting a different folder or restarting the app.

### Session not finding installed tools

If Claude can't find tools like `npm`, `node`, or other CLI commands, verify the tools work in your regular terminal, check that your shell profile properly sets up PATH, and restart the desktop app to reload environment variables.

### Git and Git LFS errors

Git is required for session isolation and worktrees. If you see "Git is required," install Git from [git-scm.com](https://git-scm.com/downloads) and restart the app.

If you see "Git LFS is required by this repository but is not installed," install Git LFS from [git-lfs.com](https://git-lfs.com/), run `git lfs install`, and restart the app.

### MCP servers not working on Windows

If MCP server toggles don't respond or servers fail to connect on Windows, check that the server is properly configured in your settings, restart the app, verify the server process is running in Task Manager, and review server logs for connection errors.

### App won't quit

* **macOS**: press Cmd+Q. If the app doesn't respond, use Force Quit with Cmd+Option+Esc, select Claude, and click Force Quit.
* **Windows**: use Task Manager with Ctrl+Shift+Esc to end the Claude process.

### Windows-specific issues

* **PATH not updated after install**: open a new terminal window. PATH updates only apply to new terminal sessions.
* **Concurrent installation error**: if you see an error about another installation in progress but there isn't one, try running the installer as Administrator.
* **ARM64 limitations**: Windows ARM64 devices can run the desktop app but do not support local sessions. Use **Remote** sessions instead.

### Cowork tab unavailable on Intel Macs

The Cowork tab requires Apple Silicon, M1 or later. The Chat and Code tabs work normally on Intel Macs.

### "Branch doesn't exist yet" when opening in CLI

Remote sessions can create branches that don't exist on your local machine. Click the branch name in the session toolbar to copy it, then fetch it locally:

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Still stuck?

* Search or file a bug on [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visit the [Claude support center](https://support.claude.com/)

When filing a bug, include your desktop app version, your operating system, the exact error message, and relevant logs. On macOS, check Console.app. On Windows, check Event Viewer → Application.
