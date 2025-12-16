# Use Claude Code in VS Code

> Install and configure the Claude Code extension for VS Code. Get AI coding assistance with inline diffs, @-mentions, plan review, and keyboard shortcuts.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="VS Code editor with the Claude Code extension panel open on the right side, showing a conversation with Claude" data-og-width="2500" width="2500" data-og-height="1155" height="1155" data-path="images/vs-code-extension-interface.jpg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=280&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=87630c671517a3d52e9aee627041696e 280w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=560&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=716b093879204beec8d952649ef75292 560w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=840&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=c1525d1a01513acd9d83d8b5a8fe2fc8 840w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=1100&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=1d90021d58bbb51f871efec13af955c3 1100w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=1650&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=7babdd25440099886f193cfa99af88ae 1650w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=2500&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=08c92eedfb56fe61a61e480fb63784b6 2500w" />

The VS Code extension provides a native graphical interface for Claude Code, integrated directly into your IDE. This is the recommended way to use Claude Code in VS Code.

With the extension, you can review and edit Claude's plans before accepting them, auto-accept edits as they're made, @-mention files with specific line ranges from your selection, access conversation history, and open multiple conversations in separate tabs or windows.

## Prerequisites

* VS Code 1.98.0 or higher
* An Anthropic account (you'll sign in when you first open the extension). If you're using a third-party provider like Amazon Bedrock or Google Vertex AI, see [Use third-party providers](#use-third-party-providers) instead.

You don't need to install the Claude Code CLI first. However, some features like MCP server configuration require the CLI. See [VS Code extension vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) for details.

## Install the extension

Click the link for your IDE to install directly:

* [Install for VS Code](vscode:extension/anthropic.claude-code)
* [Install for Cursor](cursor:extension/anthropic.claude-code)

Or in VS Code, press `Cmd+Shift+X` (Mac) or `Ctrl+Shift+X` (Windows/Linux) to open the Extensions view, search for "Claude Code", and click **Install**.

<Note>You may need to restart VS Code or run "Developer: Reload Window" from the Command Palette after installation.</Note>

## Get started

Once installed, you can start using Claude Code through the VS Code interface:

<Steps>
  <Step title="Open the Claude Code panel">
    Throughout VS Code, the Spark icon indicates Claude Code: <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=a734d84e785140016672f08e0abb236c" alt="Spark icon" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} data-og-width="16" width="16" data-og-height="16" height="16" data-path="images/vs-code-spark-icon.svg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=280&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=9a45aad9a84b9fa1701ac99a1f9aa4e9 280w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=560&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=3f4cb9254c4d4e93989c4b6bf9292f4b 560w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=840&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=e75ccc9faa3e572db8f291ceb65bb264 840w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=1100&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=f147bd81a381a62539a4ce361fac41c7 1100w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=1650&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=78fe68efaee5d6e844bbacab1b442ed5 1650w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-spark-icon.svg?w=2500&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=efb8dbe1dfa722d094edc6ad2ad4bedb 2500w" />

    The quickest way to open Claude is to click this icon in the **Editor Toolbar** (top-right corner of the editor). Note: This icon only appears when you have a file open—opening just a folder isn't enough.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="VS Code editor showing the Spark icon in the Editor Toolbar" data-og-width="2796" width="2796" data-og-height="734" height="734" data-path="images/vs-code-editor-icon.png" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=280&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=56f218d5464359d6480cfe23f70a923e 280w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=560&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=344a8db024b196c795a80dc85cacb8d1 560w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=840&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=f30bf834ee0625b2a4a635d552d87163 840w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=1100&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=81fdf984840e43a9f08ae42729d1484d 1100w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=1650&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=8b60fb32de54717093d512afaa99785c 1650w, https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?w=2500&fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=893e6bda8f2e9d42c8a294d394f0b736 2500w" />

    Other ways to open Claude Code:

    * **Command Palette**: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux), type "Claude Code", and select an option like "Open in New Tab"
    * **Activity Bar**: Run "Claude Code: Open in Side Bar" from the Command Palette once, and a Spark icon will appear in the left sidebar. This is useful if you want quick access without having a file open.

    You can drag the Claude panel to reposition it anywhere in VS Code, including to the Activity Bar if the Spark icon isn't showing there. See [Customize your workflow](#customize-your-workflow) for details.
  </Step>

  <Step title="Send a prompt">
    Prompt Claude Code in the same way you would in the terminal.
  </Step>

  <Step title="Review changes">
    Watch as Claude analyzes your code and suggests changes. Review and accept edits directly in the interface.
  </Step>
</Steps>

## Customize your workflow

Once you're up and running, you can reposition the Claude panel or switch to terminal mode.

### Change the layout

You can drag the Claude panel to reposition it anywhere in VS Code. Grab the panel's tab or title bar and drag it to:

* **Activity Bar**: The left sidebar with icons for Explorer, Search, etc.
* **Secondary sidebar**: The right side of the window
* **Editor area**: Opens Claude as a tab alongside your files

This lets you position Claude wherever works best for your workflow.

### Switch to terminal mode

By default, the extension opens a graphical chat panel. If you prefer the CLI-style interface, open the [Use Terminal setting](vscode://settings/claudeCode.useTerminal) and check the box.

You can also open VS Code settings (`Cmd+,` on Mac or `Ctrl+,` on Windows/Linux), go to Extensions → Claude Code, and check **Use Terminal**.

<Note>
  In terminal mode, the Activity Bar icon (left vertical menu) still opens the graphical panel, while the Editor Toolbar icon (top-right of editor) opens terminal mode. You can use both entry points to switch between interfaces without changing settings.
</Note>

## VS Code commands and shortcuts

Open the Command Palette (`Cmd+Shift+P` on Mac or `Ctrl+Shift+P` on Windows/Linux) and type "Claude Code" to see all available VS Code commands for the Claude Code extension:

<Note>
  These are VS Code commands for controlling the extension. For Claude Code slash commands (like `/help` or `/compact`), not all CLI commands are available in the extension yet. See [VS Code extension vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) for details.
</Note>

| Command                    | Shortcut                                                 | Description                                                                        |
| -------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Toggle focus between editor and Claude                                             |
| Open in Side Bar           | —                                                        | Open Claude in the left sidebar                                                    |
| Open in Terminal           | —                                                        | Open Claude in terminal mode                                                       |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Open a new conversation as an editor tab                                           |
| Open in New Window         | —                                                        | Open a new conversation in a separate window                                       |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Start a new conversation (when Claude is focused)                                  |
| Insert @-Mention Reference | `Alt+K`                                                  | Insert a reference to the current file (includes line numbers if text is selected) |
| Show Logs                  | —                                                        | View extension debug logs                                                          |
| Logout                     | —                                                        | Sign out of your Anthropic account                                                 |

Use **Open in New Tab** or **Open in New Window** to run multiple conversations simultaneously. Each tab or window maintains its own conversation history and context.

## Configure settings

The extension has two types of settings:

* **Extension settings**: Open with `Cmd+,` (Mac) or `Ctrl+,` (Windows/Linux), then go to Extensions → Claude Code.

  | Setting                            | Description                                                                                                                                                                  |
  | ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | Selected Model                     | Default model for new conversations. Change per-session with `/model`.                                                                                                       |
  | Use Terminal                       | Launch Claude in terminal mode instead of graphical panel                                                                                                                    |
  | Initial Permission Mode            | Controls approval prompts for file edits and commands. Defaults to `default` (ask before each action).                                                                       |
  | Preferred Location                 | Default location: sidebar (right) or panel (new tab)                                                                                                                         |
  | Autosave                           | Auto-save files before Claude reads or writes them                                                                                                                           |
  | Use Ctrl+Enter to Send             | Use Ctrl/Cmd+Enter instead of Enter to send prompts                                                                                                                          |
  | Enable New Conversation Shortcut   | Enable Cmd/Ctrl+N to start a new conversation                                                                                                                                |
  | Respect Git Ignore                 | Exclude .gitignore patterns from file searches                                                                                                                               |
  | Environment Variables              | Set environment variables for the Claude process. **Not recommended**—use [Claude Code settings](/en/settings) instead so configuration is shared between extension and CLI. |
  | Disable Login Prompt               | Skip authentication prompts (for third-party provider setups)                                                                                                                |
  | Allow Dangerously Skip Permissions | Bypass all permission prompts. **Use with extreme caution**—recommended only for isolated sandboxes with no internet access.                                                 |
  | Claude Process Wrapper             | Executable path used to launch the Claude process                                                                                                                            |

* **Claude Code settings** (`~/.claude/settings.json`): These settings are shared between the VS Code extension and the CLI. Use this file for allowed commands and directories, environment variables, hooks, and MCP servers. See the [settings documentation](/en/settings) for details.

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

## VS Code extension vs. Claude Code CLI

The extension doesn't yet have full feature parity with the CLI. If you need CLI-only features, you can run `claude` directly in VS Code's integrated terminal.

| Feature             | CLI                            | VS Code Extension                        |
| ------------------- | ------------------------------ | ---------------------------------------- |
| Slash commands      | [Full set](/en/slash-commands) | Subset (type `/` to see available)       |
| MCP server config   | Yes                            | No (configure via CLI, use in extension) |
| Checkpoints         | Yes                            | Coming soon                              |
| `#` memory shortcut | Yes                            | No                                       |
| `!` bash shortcut   | Yes                            | No                                       |
| Tab completion      | Yes                            | No                                       |

### Run CLI in VS Code

To use the CLI while staying in VS Code, open the integrated terminal (`` Ctrl+` `` on Windows/Linux or `` Cmd+` `` on Mac) and run `claude`. The CLI automatically integrates with your IDE for features like diff viewing and diagnostic sharing.

If using an external terminal, run `/ide` inside Claude Code to connect it to VS Code.

### Switch between extension and CLI

The extension and CLI share the same conversation history. To continue an extension conversation in the CLI, run `claude --resume` in the terminal. This opens an interactive picker where you can search for and select your conversation.

## Security considerations

With auto-edit permissions enabled, Claude Code can modify VS Code configuration files (like `settings.json` or `tasks.json`) that VS Code may execute automatically. This could potentially bypass Claude Code's normal permission prompts.

To reduce risk when working with untrusted code:

* Enable [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) for untrusted workspaces
* Use manual approval mode instead of auto-accept for edits
* Review changes carefully before accepting them

## Fix common issues

### Extension won't install

* Ensure you have a compatible version of VS Code (1.98.0 or later)
* Check that VS Code has permission to install extensions
* Try installing directly from the Marketplace website

### Spark icon not visible

There are two places the Spark icon can appear:

* **Editor Toolbar** (top-right of editor): Only visible when a file is open
* **Activity Bar** (left sidebar): Only visible after running "Claude Code: Open in Side Bar" from the Command Palette

If you don't see the icon:

1. **Open a file**: The Editor Toolbar icon requires a file to be open—having just a folder open isn't enough
2. **Enable the Activity Bar icon**: Run "Claude Code: Open in Side Bar" from the Command Palette once, and the icon will appear in the Activity Bar permanently
3. **Check VS Code version**: Requires 1.98.0 or higher (Help → About)
4. **Restart VS Code**: Run "Developer: Reload Window" from the command palette
5. **Disable conflicting extensions**: Temporarily disable other AI extensions (Cline, Continue, etc.)
6. **Check workspace trust**: The extension doesn't work in Restricted Mode
7. **Use the Command Palette**: Open with `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux), then type "Claude Code: Open in Side Bar"

### Claude Code never responds

If Claude Code isn't responding to your prompts:

1. **Check your internet connection**: Ensure you have a stable internet connection
2. **Start a new conversation**: Try starting a fresh conversation to see if the issue persists
3. **Try the CLI**: Run `claude` from the terminal to see if you get more detailed error messages
4. **File a bug report**: If the problem continues, [file an issue on GitHub](https://github.com/anthropics/claude-code/issues) with details about the error

### Standalone CLI not connecting to IDE

* Ensure you're running Claude Code from VS Code's integrated terminal (not an external terminal)
* Ensure the CLI for your IDE variant is installed:
  * VS Code: `code` command should be available
  * Cursor: `cursor` command should be available
  * Windsurf: `windsurf` command should be available
  * VSCodium: `codium` command should be available
* If the command isn't available, install it from the Command Palette → "Shell Command: Install 'code' command in PATH"

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


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt