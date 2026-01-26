> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code in VS Code

> Install and configure the Claude Code extension for VS Code. Get AI coding assistance with inline diffs, @-mentions, plan review, and keyboard shortcuts.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="VS Code editor with the Claude Code extension panel open on the right side, showing a conversation with Claude" data-og-width="2500" width="2500" data-og-height="1155" height="1155" data-path="images/vs-code-extension-interface.jpg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=280&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=87630c671517a3d52e9aee627041696e 280w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=560&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=716b093879204beec8d952649ef75292 560w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=840&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=c1525d1a01513acd9d83d8b5a8fe2fc8 840w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=1100&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=1d90021d58bbb51f871efec13af955c3 1100w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=1650&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=7babdd25440099886f193cfa99af88ae 1650w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=2500&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=08c92eedfb56fe61a61e480fb63784b6 2500w" />

The VS Code extension provides a native graphical interface for Claude Code, integrated directly into your IDE. This is the recommended way to use Claude Code in VS Code.

With the extension, you can review and edit Claude's plans before accepting them, auto-accept edits as they're made, @-mention files with specific line ranges from your selection, access conversation history, and open multiple conversations in separate tabs or windows.

## Prerequisites

* VS Code 1.98.0 or higher
* An Anthropic account (you'll sign in when you first open the extension). If you're using a third-party provider like Amazon Bedrock or Google Vertex AI, see [Use third-party providers](#use-third-party-providers) instead.

<Tip>
  The extension includes the CLI (command-line interface), which you can access from VS Code's integrated terminal for advanced features. See [VS Code extension vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) for details.
</Tip>

## Install the extension

Click the link for your IDE to install directly:

* [Install for VS Code](vscode:extension/anthropic.claude-code)
* [Install for Cursor](cursor:extension/anthropic.claude-code)

Or in VS Code, press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux) to open the Extensions view, search for "Claude Code", and click **Install**.

<Note>If the extension doesn't appear after installation, restart VS Code or run "Developer: Reload Window" from the Command Palette.</Note>

## Get started

Once installed, you can start using Claude Code through the VS Code interface:

<Steps>
  <Step title="Open the Claude Code panel">
    Throughout VS Code, the Spark icon indicates Claude Code: <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=a734d84e785140016672f08e0abb236c" alt="Spark icon" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} data-og-width="16" width="16" data-og-height="16" height="16" data-path="images/vs-code-spark-icon.svg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=280&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=9a45aad9a84b9fa1701ac99a1f9aa4e9 280w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=560&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=3f4cb9254c4d4e93989c4b6bf9292f4b 560w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=840&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=e75ccc9faa3e572db8f291ceb65bb264 840w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=1100&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=f147bd81a381a62539a4ce361fac41c7 1100w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=1650&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=78fe68efaee5d6e844bbacab1b442ed5 1650w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=2500&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=efb8dbe1dfa722d094edc6ad2ad4bedb 2500w" />

    The quickest way to open Claude is to click the Spark icon in the **Editor Toolbar** (top-right corner of the editor). The icon only appears when you have a file open.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="VS Code editor showing the Spark icon in the Editor Toolbar" data-og-width="2796" width="2796" data-og-height="734" height="734" data-path="images/vs-code-editor-icon.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=280&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=56f218d5464359d6480cfe23f70a923e 280w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=560&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=344a8db024b196c795a80dc85cacb8d1 560w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=840&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=f30bf834ee0625b2a4a635d552d87163 840w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=1100&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=81fdf984840e43a9f08ae42729d1484d 1100w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=1650&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=8b60fb32de54717093d512afaa99785c 1650w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=2500&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=893e6bda8f2e9d42c8a294d394f0b736 2500w" />

    Other ways to open Claude Code:

    * **Command Palette**: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux), type "Claude Code", and select an option like "Open in New Tab"
    * **Status Bar**: Click **✱ Claude Code** in the bottom-right corner of the window. This works even when no file is open.

    You can drag the Claude panel to reposition it anywhere in VS Code. See [Customize your workflow](#customize-your-workflow) for details.
  </Step>

  <Step title="Send a prompt">
    Ask Claude to help with your code or files, whether that's explaining how something works, debugging an issue, or making changes.

    <Tip>Claude automatically sees your selected text. Press `Option+K` (Mac) / `Alt+K` (Windows/Linux) to also insert an @-mention reference (like `@file.ts#5-10`) into your prompt.</Tip>

    Here's an example of asking about a particular line in a file:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="VS Code editor with lines 2-3 selected in a Python file, and the Claude Code panel showing a question about those lines with an @-mention reference" data-og-width="3288" width="3288" data-og-height="1876" height="1876" data-path="images/vs-code-send-prompt.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?w=280&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=f40bde7b2c245fe8f0f5b784e8106492 280w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?w=560&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=fad66a27a9a6faa23b05370aa4f398b2 560w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?w=840&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=4539c8a3823ca80a5c8771f6c088ce9e 840w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?w=1100&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=fae8ebf300c7853409a562ffa46d9c71 1100w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?w=1650&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=22e4462bb8cf0c0ca20f8102bc4c971a 1650w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?w=2500&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=739bfd045f70fe7be1a109a53494590e 2500w" />
  </Step>

  <Step title="Review changes">
    When Claude wants to edit a file, it shows a side-by-side comparison of the original and proposed changes, then asks for permission. You can accept, reject, or tell Claude what to do instead.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code showing a diff of Claude's proposed changes with a permission prompt asking whether to make the edit" data-og-width="3292" width="3292" data-og-height="1876" height="1876" data-path="images/vs-code-edits.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?w=280&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=cb5d41b81087f79b842a56b5a3304660 280w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?w=560&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=90bb691960decdc06393c3c21cd62c75 560w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?w=840&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=9a11bf878ba619e850380904ff4f38e8 840w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?w=1100&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=6dddbf596b4f69ec6245bdc5eb6dd487 1100w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?w=1650&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ef2713b8cbfd2cee97af817d813d64c7 1650w, https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?w=2500&fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=1f7e1c52919cdfddf295f32a2ec7ae59 2500w" />
  </Step>
</Steps>

For more ideas on what you can do with Claude Code, see [Common workflows](/en/common-workflows).

<Tip>
  The extension includes two built-in tutorials:

  * **VS Code walkthrough**: Run "Claude Code: Open Walkthrough" from the Command Palette for a guided tour of the basics.
  * **Interactive checklist**: Click the graduation cap icon in the Claude panel header to work through features like writing code, using Plan mode, and setting up rules.
</Tip>

## Use the prompt box

The prompt box supports several features:

* **Permission modes**: Click the mode indicator at the bottom of the prompt box to switch modes. In normal mode, Claude asks permission before each action. In Plan mode, Claude describes what it will do and waits for approval before making changes. In auto-accept mode, Claude makes edits without asking. Set the default in VS Code settings under `claudeCode.initialPermissionMode`.
* **Command menu**: Click `/` or type `/` to open the command menu. Options include attaching files, switching models, toggling extended thinking, and viewing plan usage (`/usage`). The Customize section provides access to MCP servers, hooks, memory, permissions, and plugins. Items with a terminal icon open in the integrated terminal.
* **Context indicator**: The prompt box shows how much of Claude's context window you're using. Claude automatically compacts when needed, or you can run `/compact` manually.
* **Extended thinking**: Lets Claude spend more time reasoning through complex problems. Toggle it on via the command menu (`/`). See [Extended thinking](/en/common-workflows#use-extended-thinking-thinking-mode) for details.
* **Multi-line input**: Press `Shift+Enter` to add a new line without sending.

### Reference files and folders

Use @-mentions to give Claude context about specific files or folders. When you type `@` followed by a file or folder name, Claude reads that content and can answer questions about it or make changes to it. Claude Code supports fuzzy matching, so you can type partial names to find what you need:

```
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

When you select text in the editor, Claude can see your highlighted code automatically. The prompt box footer shows how many lines are selected. Press `Option+K` (Mac) / `Alt+K` (Windows/Linux) to insert an @-mention with the file path and line numbers (e.g., `@app.ts#5-10`). Click the selection indicator to toggle whether Claude can see your highlighted text - the eye-slash icon means the selection is hidden from Claude.

You can also hold `Shift` while dragging files into the prompt box to add them as attachments. Click the X on any attachment to remove it from context.

### Resume past conversations

Click the dropdown at the top of the Claude Code panel to access your conversation history. You can search by keyword or browse by time (Today, Yesterday, Last 7 days, etc.). Click any conversation to resume it with the full message history. For more on resuming sessions, see [Common workflows](/en/common-workflows#resume-previous-conversations).

### Resume remote sessions from Claude.ai

If you use [Claude Code on the web](/en/claude-code-on-the-web), you can resume those remote sessions directly in VS Code. This requires signing in with **Claude.ai Subscription**, not Anthropic Console.

<Steps>
  <Step title="Open Past Conversations">
    Click the **Past Conversations** dropdown at the top of the Claude Code panel.
  </Step>

  <Step title="Select the Remote tab">
    The dialog shows two tabs: Local and Remote. Click **Remote** to see sessions from claude.ai.
  </Step>

  <Step title="Select a session to resume">
    Browse or search your remote sessions. Click any session to download it and continue the conversation locally.
  </Step>
</Steps>

<Note>
  Only web sessions started with a GitHub repository appear in the Remote tab. Resuming loads the conversation history locally; changes are not synced back to claude.ai.
</Note>

## Customize your workflow

Once you're up and running, you can reposition the Claude panel, run multiple sessions, or switch to terminal mode.

### Choose where Claude lives

You can drag the Claude panel to reposition it anywhere in VS Code. Grab the panel's tab or title bar and drag it to:

* **Secondary sidebar**: The right side of the window. Keeps Claude visible while you code.
* **Primary sidebar**: The left sidebar with icons for Explorer, Search, etc.
* **Editor area**: Opens Claude as a tab alongside your files. Useful for side tasks.

<Tip>
  Use the sidebar for your main Claude session and open additional tabs for side tasks. Claude remembers your preferred location. Note that the Spark icon only appears in the Activity Bar when the Claude panel is docked to the left. Since Claude defaults to the right side, use the Editor Toolbar icon to open Claude.
</Tip>

### Run multiple conversations

Use **Open in New Tab** or **Open in New Window** from the Command Palette to start additional conversations. Each conversation maintains its own history and context, allowing you to work on different tasks in parallel.

When using tabs, a small colored dot on the spark icon indicates status: blue means a permission request is pending, orange means Claude finished while the tab was hidden.

### Switch to terminal mode

By default, the extension opens a graphical chat panel. If you prefer the CLI-style interface, open the [Use Terminal setting](vscode://settings/claudeCode.useTerminal) and check the box.

You can also open VS Code settings (`Cmd+,` on Mac or `Ctrl+,` on Windows/Linux), go to Extensions → Claude Code, and check **Use Terminal**.

## Manage plugins

The VS Code extension includes a graphical interface for installing and managing [plugins](/en/plugins). Type `/plugins` in the prompt box to open the **Manage plugins** interface.

### Install plugins

The plugin dialog shows two tabs: **Plugins** and **Marketplaces**.

In the Plugins tab:

* **Installed plugins** appear at the top with toggle switches to enable or disable them
* **Available plugins** from your configured marketplaces appear below
* Search to filter plugins by name or description
* Click **Install** on any available plugin

When you install a plugin, choose the installation scope:

* **Install for you**: Available in all your projects (user scope)
* **Install for this project**: Shared with project collaborators (project scope)
* **Install locally**: Only for you, only in this repository (local scope)

### Manage marketplaces

Switch to the **Marketplaces** tab to add or remove plugin sources:

* Enter a GitHub repo, URL, or local path to add a new marketplace
* Click the refresh icon to update a marketplace's plugin list
* Click the trash icon to remove a marketplace

After making changes, a banner prompts you to restart Claude Code to apply the updates.

<Note>
  Plugin management in VS Code uses the same CLI commands under the hood. Plugins and marketplaces you configure in the extension are also available in the CLI, and vice versa.
</Note>

For more about the plugin system, see [Plugins](/en/plugins) and [Plugin marketplaces](/en/plugin-marketplaces).

## VS Code commands and shortcuts

Open the Command Palette (`Cmd+Shift+P` on Mac or `Ctrl+Shift+P` on Windows/Linux) and type "Claude Code" to see all available VS Code commands for the Claude Code extension.

Some shortcuts depend on which panel is "focused" (receiving keyboard input). When your cursor is in a code file, the editor is focused. When your cursor is in Claude's prompt box, Claude is focused. Use `Cmd+Esc` / `Ctrl+Esc` to toggle between them.

<Note>
  These are VS Code commands for controlling the extension. Not all built-in Claude Code commands are available in the extension. See [VS Code extension vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) for details.
</Note>

| Command                    | Shortcut                                                 | Description                                                                          |
| -------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Toggle focus between editor and Claude                                               |
| Open in Side Bar           | -                                                        | Open Claude in the left sidebar                                                      |
| Open in Terminal           | -                                                        | Open Claude in terminal mode                                                         |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Open a new conversation as an editor tab                                             |
| Open in New Window         | -                                                        | Open a new conversation in a separate window                                         |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Start a new conversation (requires Claude to be focused)                             |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Insert a reference to the current file and selection (requires editor to be focused) |
| Show Logs                  | -                                                        | View extension debug logs                                                            |
| Logout                     | -                                                        | Sign out of your Anthropic account                                                   |

## Configure settings

The extension has two types of settings:

* **Extension settings** in VS Code: Control the extension's behavior within VS Code. Open with `Cmd+,` (Mac) or `Ctrl+,` (Windows/Linux), then go to Extensions → Claude Code. You can also type `/` and select **General Config** to open settings.
* **Claude Code settings** in `~/.claude/settings.json`: Shared between the extension and CLI. Use for allowed commands, environment variables, hooks, and MCP servers. See [Settings](/en/settings) for details.

### Extension settings

| Setting                           | Default   | Description                                                                                           |
| --------------------------------- | --------- | ----------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default` | Model for new conversations. Change per-session with `/model`.                                        |
| `useTerminal`                     | `false`   | Launch Claude in terminal mode instead of graphical panel                                             |
| `initialPermissionMode`           | `default` | Controls approval prompts: `default` (ask each time), `plan`, `acceptEdits`, or `bypassPermissions`   |
| `preferredLocation`               | `panel`   | Where Claude opens: `sidebar` (right) or `panel` (new tab)                                            |
| `autosave`                        | `true`    | Auto-save files before Claude reads or writes them                                                    |
| `useCtrlEnterToSend`              | `false`   | Use Ctrl/Cmd+Enter instead of Enter to send prompts                                                   |
| `enableNewConversationShortcut`   | `true`    | Enable Cmd/Ctrl+N to start a new conversation                                                         |
| `hideOnboarding`                  | `false`   | Hide the onboarding checklist (graduation cap icon)                                                   |
| `respectGitIgnore`                | `true`    | Exclude .gitignore patterns from file searches                                                        |
| `environmentVariables`            | `[]`      | Set environment variables for the Claude process. Use Claude Code settings instead for shared config. |
| `disableLoginPrompt`              | `false`   | Skip authentication prompts (for third-party provider setups)                                         |
| `allowDangerouslySkipPermissions` | `false`   | Bypass all permission prompts. **Use with extreme caution.**                                          |
| `claudeProcessWrapper`            | -         | Executable path used to launch the Claude process                                                     |

## VS Code extension vs. Claude Code CLI

Claude Code is available as both a VS Code extension (graphical panel) and a CLI (command-line interface in the terminal). Some features are only available in the CLI. If you need a CLI-only feature, run `claude` in VS Code's integrated terminal.

| Feature             | CLI                                           | VS Code Extension                        |
| ------------------- | --------------------------------------------- | ---------------------------------------- |
| Commands and skills | [All](/en/interactive-mode#built-in-commands) | Subset (type `/` to see available)       |
| MCP server config   | Yes                                           | No (configure via CLI, use in extension) |
| Checkpoints         | Yes                                           | Yes                                      |
| `!` bash shortcut   | Yes                                           | No                                       |
| Tab completion      | Yes                                           | No                                       |

### Rewind with checkpoints

The VS Code extension supports checkpoints, which track Claude's file edits and let you rewind to a previous state. Hover over any message to reveal the rewind button, then choose from three options:

* **Fork conversation from here**: start a new conversation branch from this message while keeping all code changes intact
* **Rewind code to here**: revert file changes back to this point in the conversation while keeping the full conversation history
* **Fork conversation and rewind code**: start a new conversation branch and revert file changes to this point

For full details on how checkpoints work and their limitations, see [Checkpointing](/en/checkpointing).

### Run CLI in VS Code

To use the CLI while staying in VS Code, open the integrated terminal (`` Ctrl+` `` on Windows/Linux or `` Cmd+` `` on Mac) and run `claude`. The CLI automatically integrates with your IDE for features like diff viewing and diagnostic sharing.

If using an external terminal, run `/ide` inside Claude Code to connect it to VS Code.

### Switch between extension and CLI

The extension and CLI share the same conversation history. To continue an extension conversation in the CLI, run `claude --resume` in the terminal. This opens an interactive picker where you can search for and select your conversation.

### Include terminal output in prompts

Reference terminal output in your prompts using `@terminal:name` where `name` is the terminal's title. This lets Claude see command output, error messages, or logs without copy-pasting.

### Monitor background processes

When Claude runs long-running commands, the extension shows progress in the status bar. However, visibility for background tasks is limited compared to the CLI. For better visibility, have Claude output the command so you can run it in VS Code's integrated terminal.

### Connect to external tools with MCP

MCP (Model Context Protocol) servers give Claude access to external tools, databases, and APIs. Configure them via CLI, then use them in both extension and CLI.

To add an MCP server, open the integrated terminal (`` Ctrl+` `` or `` Cmd+` ``) and run:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Once configured, ask Claude to use the tools (e.g., "Review PR #456"). Some servers require authentication: run `claude` in the terminal, then type `/mcp` to authenticate. See the [MCP documentation](/en/mcp) for available servers.

## Work with git

Claude Code integrates with git to help with version control workflows directly in VS Code. Ask Claude to commit changes, create pull requests, or work across branches.

### Create commits and pull requests

Claude can stage changes, write commit messages, and create pull requests based on your work:

```
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

When creating pull requests, Claude generates descriptions based on the actual code changes and can add context about testing or implementation decisions.

### Use git worktrees for parallel tasks

Git worktrees allow multiple Claude Code sessions to work on separate branches simultaneously, each with isolated files:

```bash  theme={null}
# Create a worktree for a new feature
git worktree add ../project-feature-a -b feature-a

# Run Claude Code in each worktree
cd ../project-feature-a && claude
```

Each worktree maintains independent file state while sharing git history. This prevents Claude instances from interfering with each other when working on different tasks.

For detailed git workflows including PR reviews and branch management, see [Common workflows](/en/common-workflows#create-pull-requests).

## Use third-party providers

By default, Claude Code connects directly to Anthropic's API. If your organization uses Amazon Bedrock, Google Vertex AI, or Microsoft Foundry to access Claude, configure the extension to use your provider instead:

<Steps>
  <Step title="Disable login prompt">
    Open the [Disable Login Prompt setting](vscode://settings/claudeCode.disableLoginPrompt) and check the box.

    You can also open VS Code settings (`Cmd+,` on Mac or `Ctrl+,` on Windows/Linux), search for "Claude Code login", and check **Disable Login Prompt**.
  </Step>

  <Step title="Configure your provider">
    Follow the setup guide for your provider:

    * [Claude Code on Amazon Bedrock](/en/amazon-bedrock)
    * [Claude Code on Google Vertex AI](/en/google-vertex-ai)
    * [Claude Code on Microsoft Foundry](/en/microsoft-foundry)

    These guides cover configuring your provider in `~/.claude/settings.json`, which ensures your settings are shared between the VS Code extension and the CLI.
  </Step>
</Steps>

## Security and privacy

Your code stays private. Claude Code processes your code to provide assistance but does not use it to train models. For details on data handling and how to opt out of logging, see [Data and privacy](/en/data-usage).

With auto-edit permissions enabled, Claude Code can modify VS Code configuration files (like `settings.json` or `tasks.json`) that VS Code may execute automatically. To reduce risk when working with untrusted code:

* Enable [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) for untrusted workspaces
* Use manual approval mode instead of auto-accept for edits
* Review changes carefully before accepting them

## Fix common issues

### Extension won't install

* Ensure you have a compatible version of VS Code (1.98.0 or later)
* Check that VS Code has permission to install extensions
* Try installing directly from the [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### Spark icon not visible

The Spark icon appears in the **Editor Toolbar** (top-right of editor) when you have a file open. If you don't see it:

1. **Open a file**: The icon requires a file to be open. Having just a folder open isn't enough.
2. **Check VS Code version**: Requires 1.98.0 or higher (Help → About)
3. **Restart VS Code**: Run "Developer: Reload Window" from the Command Palette
4. **Disable conflicting extensions**: Temporarily disable other AI extensions (Cline, Continue, etc.)
5. **Check workspace trust**: The extension doesn't work in Restricted Mode

Alternatively, click "✱ Claude Code" in the **Status Bar** (bottom-right corner). This works even without a file open. You can also use the **Command Palette** (`Cmd+Shift+P` / `Ctrl+Shift+P`) and type "Claude Code".

### Claude Code never responds

If Claude Code isn't responding to your prompts:

1. **Check your internet connection**: Ensure you have a stable internet connection
2. **Start a new conversation**: Try starting a fresh conversation to see if the issue persists
3. **Try the CLI**: Run `claude` from the terminal to see if you get more detailed error messages

If problems persist, [file an issue on GitHub](https://github.com/anthropics/claude-code/issues) with details about the error.

## Uninstall the extension

To uninstall the Claude Code extension:

1. Open the Extensions view (`Cmd+Shift+X` on Mac or `Ctrl+Shift+X` on Windows/Linux)
2. Search for "Claude Code"
3. Click **Uninstall**

To also remove extension data and reset all settings:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

For additional help, see the [troubleshooting guide](/en/troubleshooting).

## Next steps

Now that you have Claude Code set up in VS Code:

* [Explore common workflows](/en/common-workflows) to get the most out of Claude Code
* [Set up MCP servers](/en/mcp) to extend Claude's capabilities with external tools. Configure servers using the CLI, then use them in the extension.
* [Configure Claude Code settings](/en/settings) to customize allowed commands, hooks, and more. These settings are shared between the extension and CLI.
