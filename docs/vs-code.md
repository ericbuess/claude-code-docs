# Visual Studio Code

> Use Claude Code with Visual Studio Code through our native extension or CLI integration

<img src="https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=600835067c8b03557a0529978e3f0261" alt="Claude Code VS Code Extension Interface" data-og-width="2500" width="2500" data-og-height="1155" height="1155" data-path="images/vs-code-extension-interface.jpg" data-optimize="true" data-opv="3" srcset="https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?w=280&fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=c11a25932f84ca58124a368156b476d2 280w, https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?w=560&fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=3642697ed4d8a6c02396c403bf7aae44 560w, https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?w=840&fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=fb3cb16e752060fbeb0f5e8ba775798b 840w, https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?w=1100&fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=1c6073edc8fcfcbc8e237cbf5f25cdc6 1100w, https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?w=1650&fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=152628678fe3301018b79e932706c430 1650w, https://mintcdn.com/anthropic-claude-docs/Xfpgr-ckk38MZnw3/images/vs-code-extension-interface.jpg?w=2500&fit=max&auto=format&n=Xfpgr-ckk38MZnw3&q=85&s=7ac83b2db00366c9a745380571a748ab 2500w" />

## VS Code Extension (Beta)

The VS Code extension, available in beta, lets you see Claude's changes in real-time through a native graphical interface integrated directly into your IDE. The VS Code extension makes it easier to access and interact with Claude Code for users who prefer a visual interface over the terminal.

### Features

The VS Code extension provides:

* **Native IDE experience**: Dedicated Claude Code sidebar panel accessed via the Spark icon
* **Plan mode with editing**: Review and edit Claude's plans before accepting them
* **Auto-accept edits mode**: Automatically apply Claude's changes as they're made
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

### Updating

To update the VS Code extension:

1. Open the VS Code command palette with `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
2. Search for "Claude Code: Update"
3. Select the command to update to the latest version

### How It Works

Once installed, you can start using Claude Code through the VS Code interface:

1. Click the Spark icon in your editor's sidebar to open the Claude Code panel
2. Prompt Claude Code in the same way you would in the terminal
3. Watch as Claude analyzes your code and suggests changes
4. Review and accept edits directly in the interface
   * **Tip**: Drag the sidebar wider to see inline diffs, then click on them to expand for full details

### Using Third-Party Providers (Vertex and Bedrock)

The VS Code extension supports using Claude Code with third-party providers like Amazon Bedrock and Google Vertex AI. When configured with these providers, the extension will not prompt for login. To use third-party providers, configure environment variables in the VS Code extension settings:

1. Open VS Code settings
2. Search for "Claude Code: Environment Variables"
3. Add the required environment variables

#### Environment Variables

| Variable                      | Description                            | Required               | Example                                          |
| :---------------------------- | :------------------------------------- | :--------------------- | :----------------------------------------------- |
| `CLAUDE_CODE_USE_BEDROCK`     | Enable Amazon Bedrock integration      | Required for Bedrock   | `"1"` or `"true"`                                |
| `CLAUDE_CODE_USE_VERTEX`      | Enable Google Vertex AI integration    | Required for Vertex AI | `"1"` or `"true"`                                |
| `ANTHROPIC_API_KEY`           | API key for third-party access         | Required               | `"your-api-key"`                                 |
| `AWS_REGION`                  | AWS region for Bedrock                 |                        | `"us-east-2"`                                    |
| `AWS_PROFILE`                 | AWS profile for Bedrock authentication |                        | `"your-profile"`                                 |
| `CLOUD_ML_REGION`             | Region for Vertex AI                   |                        | `"global"` or `"us-east5"`                       |
| `ANTHROPIC_VERTEX_PROJECT_ID` | GCP project ID for Vertex AI           |                        | `"your-project-id"`                              |
| `ANTHROPIC_MODEL`             | Override primary model                 | Override model ID      | `"us.anthropic.claude-3-7-sonnet-20250219-v1:0"` |
| `ANTHROPIC_SMALL_FAST_MODEL`  | Override small/fast model              | Optional               | `"us.anthropic.claude-3-5-haiku-20241022-v1:0"`  |

For detailed setup instructions and additional configuration options, see:

* [Claude Code on Amazon Bedrock](/en/docs/claude-code/amazon-bedrock)
* [Claude Code on Google Vertex AI](/en/docs/claude-code/google-vertex-ai)

### Not Yet Implemented

The following features are not yet available in the VS Code extension:

* **Full MCP server configuration**: You need to [configure MCP servers through the CLI](/en/docs/claude-code/mcp) first, then the extension will use them
* **Subagents configuration**: Configure [subagents through the CLI](/en/docs/claude-code/sub-agents) to use them in VS Code
* **Checkpoints**: Save and restore conversation state at specific points
* **Advanced shortcuts**:
  * `#` shortcut to add to memory
  * `!` shortcut to run bash commands directly
* **Tab completion**: File path completion with tab key

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
* Try installing directly from the marketplace website

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

For additional help, see our [troubleshooting guide](/en/docs/claude-code/troubleshooting).
