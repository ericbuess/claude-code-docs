# Add Claude Code to your IDE

> Learn how to add Claude Code to your favorite IDE

Claude Code works great with any Integrated Development Environment (IDE) that has a terminal. Just run `claude`, and you're ready to go.

In addition, Claude Code provides dedicated integrations for popular IDEs, which provide features like interactive diff viewing, selection context sharing, and more. These integrations currently exist for:

* **Visual Studio Code** (including popular forks like Cursor, Windsurf, and VSCodium)
* **JetBrains IDEs** (including IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm and GoLand)

## Features

* **Quick launch**: Use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open
  Claude Code directly from your editor, or click the Claude Code button in the
  UI
* **Diff viewing**: Code changes can be displayed directly in the IDE diff
  viewer instead of the terminal. You can configure this in `/config`
* **Selection context**: The current selection/tab in the IDE is automatically
  shared with Claude Code
* **File reference shortcuts**: Use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K`
  (Linux/Windows) to insert file references (e.g., @File#L1-99)
* **Diagnostic sharing**: Diagnostic errors (lint, syntax, etc.) from the IDE
  are automatically shared with Claude as you work

## Installation

<Tabs>
  <Tab title="VS Code+">
    To install Claude Code on VS Code and popular forks like Cursor, Windsurf, and VSCodium:

    1. Open VS Code
    2. Open the integrated terminal
    3. Run `claude` - the extension will auto-install
  </Tab>

  <Tab title="JetBrains">
    To install Claude Code on JetBrains IDEs like IntelliJ, PyCharm, Android Studio, WebStorm, PhpStorm and GoLand, find and install the [Claude Code plugin](https://docs.anthropic.com/s/claude-code-jetbrains) from the marketplace and restart your IDE.

    <Note>
      The plugin may also be auto-installed when you run `claude` in the integrated terminal. The IDE must be restarted completely to take effect.
    </Note>

    <Warning>
      **Remote Development Limitations**: When using JetBrains Remote Development, you must install the plugin in the remote host via `Settings > Plugin (Host)`.
    </Warning>
  </Tab>
</Tabs>

## Usage

### From your IDE

Run `claude` from your IDE's integrated terminal, and all features will be active.

### From external terminals

Use the `/ide` command in any external terminal to connect Claude Code to your IDE and activate all features.

If you want Claude to have access to the same files as your IDE, start Claude Code from the same directory as your IDE project root.

## Configuration

IDE integrations work with Claude Code's configuration system:

1. Run `claude`
2. Enter the `/config` command
3. Adjust your preferences. Setting the diff tool to `auto` will enable automatic IDE detection

## Troubleshooting

### VS Code extension not installing

* Ensure you're running Claude Code from VS Code's integrated terminal
* Ensure that the CLI corresponding to your IDE is installed:
  * For VS Code: `code` command should be available
  * For Cursor: `cursor` command should be available
  * For Windsurf: `windsurf` command should be available
  * For VSCodium: `codium` command should be available
  * If not installed, use `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows/Linux)
    and search for "Shell Command: Install 'code' command in PATH" (or the
    equivalent for your IDE)
* Check that VS Code has permission to install extensions

### JetBrains plugin not working

* Ensure you're running Claude Code from the project root directory
* Check that the JetBrains plugin is enabled in the IDE settings
* Completely restart the IDE. You may need to do this multiple times
* For JetBrains Remote Development, ensure that the Claude Code plugin is
  installed in the remote host and not locally on the client

For additional help, refer to our
[troubleshooting guide](/en/docs/claude-code/troubleshooting).
