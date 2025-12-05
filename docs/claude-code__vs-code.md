# Visual Studio Code

> Use Claude Code with Visual Studio Code through our native extension or CLI integration

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Claude Code VS Code Extension Interface" data-og-width="2500" width="2500" data-og-height="1155" height="1155" data-path="images/vs-code-extension-interface.jpg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=280&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=87630c671517a3d52e9aee627041696e 280w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=560&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=716b093879204beec8d952649ef75292 560w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=840&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=c1525d1a01513acd9d83d8b5a8fe2fc8 840w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=1100&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=1d90021d58bbb51f871efec13af955c3 1100w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=1650&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=7babdd25440099886f193cfa99af88ae 1650w, https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?w=2500&fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=08c92eedfb56fe61a61e480fb63784b6 2500w" />

## VS Code Extension (Beta)

The VS Code extension, available in beta, lets you see Claude's changes in real-time through a native graphical interface integrated directly into your IDE. The VS Code extension makes it easier to access and interact with Claude Code for users who prefer a visual interface over the terminal.

### Features

The VS Code extension provides:

* **Native IDE experience**: Dedicated Claude Code sidebar panel accessed via the Spark icon
* **Plan mode with editing**: Review and edit Claude's plans before accepting them
* **Auto-accept edits mode**: Automatically apply Claude's changes as they're made
* **Extended thinking**: Toggle extended thinking on/off using the Extended Thinking button in the bottom-right corner of the prompt input
* **File management**: @-mention files or attach files and images using the system file picker
* **MCP server usage**: Use Model Context Protocol servers configured through the CLI
* **Conversation history**: Easy access to past conversations
* **Multiple sessions**: Run multiple Claude Code sessions simultaneously
* **Keyboard shortcuts**: Support for most shortcuts from the CLI
* **Slash commands**: Access most CLI slash commands directly in the extension

### Requirements

* VS Code 1.98.0 or higher

### Installation

Download and install the extension from the [Visual Studio Code Extension Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code).

### How It Works

Once installed, you can start using Claude Code through the VS Code interface:

1. Click the Spark icon in your editor's sidebar to open the Claude Code panel
2. Prompt Claude Code in the same way you would in the terminal
3. Watch as Claude analyzes your code and suggests changes
4. Review and accept edits directly in the interface
   * **Tip**: Drag the sidebar wider to see inline diffs, then click on them to expand for full details

### Configuration

The VS Code extension reads the same `settings.json` files as the CLI. See the [settings documentation](/en/settings) for details.

#### Third-Party Providers and Gateways

To use the VS Code extension with third-party providers (Amazon Bedrock, Google Vertex AI, Microsoft Foundry) or gateways that handle authentication:

1. Add the appropriate environment variables for your provider or gateway to your Claude Code `settings.json`:
   ```json  theme={null}
   {
     "env": {
       "CLAUDE_CODE_USE_BEDROCK": "1",
       "AWS_REGION": "us-east-2",
       "AWS_PROFILE": "your-profile"
     }
   }
   ```

2. Disable the VS Code extension login prompt via [`vscode://settings/claudeCode.disableLoginPrompt`](vscode://settings/claudeCode.disableLoginPrompt) or in VS Code's settings:
   ```json  theme={null}
   {
     "claudeCode.disableLoginPrompt": true
   }
   ```

For detailed setup instructions and additional configuration options, see:

* [Claude Code on Amazon Bedrock](/en/amazon-bedrock)
* [Claude Code on Google Vertex AI](/en/google-vertex-ai)
* [Claude Code on Microsoft Foundry](/en/microsoft-foundry)

### Not Yet Implemented

The following features are not yet available in the VS Code extension:

* **MCP server and Plugin configuration UI**: Type `/mcp` to open the terminal-based MCP server configuration, or `/plugin` for Plugin configuration. Once configured, MCP servers and Plugins will work in the extension. You can also [configure MCP servers through the CLI](/en/mcp) first, then the extension will use them.
* **Subagents configuration**: Configure [subagents through the CLI](/en/sub-agents) to use them in VS Code
* **Checkpoints**: Save and restore conversation state at specific points
* **Conversation rewinding**: The `/rewind` command is coming soon
* **Advanced shortcuts**:
  * `#` shortcut to add to memory (not supported)
  * `!` shortcut to run bash commands directly (not supported)
* **Tab completion**: File path completion with tab key
* **Model selection UI for older models**: To use older model versions like `claude-sonnet-4-20250514`, open VS Code settings for Claude Code (the `/General Config` command) and insert the model string directly into the 'Selected Model' field

We are working on adding these features in future updates.

## Security Considerations

When Claude Code runs in VS Code with auto-edit permissions enabled, it may be able to modify IDE configuration files that can be automatically executed by your IDE. This may increase the risk of running Claude Code in auto-edit mode and allow bypassing Claude Code's permission prompts for bash execution.

When running in VS Code, consider:

* Enabling [VS Code Restricted Mode](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) for untrusted workspaces
* Using manual approval mode for edits
* Taking extra care to ensure Claude is only used with trusted prompts

## Legacy CLI Integration

The first VS Code integration that we released allows Claude Code running in the terminal to interact with your IDE. It provides selection context sharing (current selection/tab is automatically shared with Claude Code), diff viewing in the IDE instead of terminal, file reference shortcuts (`Cmd+Option+K` on Mac or `Alt+Ctrl+K` on Windows/Linux to insert file references like @File#L1-99), and automatic diagnostic sharing (lint and syntax errors).

The legacy integration auto-installs when you run `claude` from VS Code's integrated terminal. Simply run `claude` from the terminal and all features activate. For external terminals, use the `/ide` command to connect Claude Code to your VS Code instance. To configure, run `claude`, enter `/config`, and set the diff tool to `auto` for automatic IDE detection.

Both the extension and CLI integration work with Visual Studio Code, Cursor, Windsurf, and VSCodium.

## Troubleshooting

### Extension Not Installing

* Ensure you have a compatible version of VS Code (1.85.0 or later)
* Check that VS Code has permission to install extensions
* Try installing directly from the Marketplace website

### Claude Code Never Responds

If Claude Code is not responding to your prompts:

1. **Check your internet connection**: Ensure you have a stable internet connection
2. **Start a new conversation**: Try starting a fresh conversation to see if the issue persists
3. **Try the CLI**: Run `claude` from the terminal to see if you get more detailed error messages
4. **File a bug report**: If the problem continues, [file an issue on GitHub](https://github.com/anthropics/claude-code/issues) with details about the error

### Legacy Integration Not Working

* Ensure you're running Claude Code from VS Code's integrated terminal
* Ensure the CLI for your IDE variant is installed:
  * VS Code: `code` command should be available
  * Cursor: `cursor` command should be available
  * Windsurf: `windsurf` command should be available
  * VSCodium: `codium` command should be available
* If the command isn't installed:
  1. Open command palette with `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
  2. Search for "Shell Command: Install 'code' command in PATH" (or equivalent for your IDE)

For additional help, see our [troubleshooting guide](/en/troubleshooting).


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt