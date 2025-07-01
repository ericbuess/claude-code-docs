# Add Claude Code to your IDE

> Learn how to add Claude Code to your favorite IDE

Claude Code seamlessly integrates with popular Integrated Development
Environments (IDEs) to enhance your coding workflow. This integration allows you
to leverage Claude's capabilities directly within your preferred development
environment.

## Supported IDEs

Claude Code currently supports two major IDE families:

* **Visual Studio Code** (including popular forks like Cursor and Windsurf)
* **JetBrains IDEs** (including PyCharm, WebStorm, IntelliJ, and GoLand)

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

### VS Code

1. Open VSCode
2. Open the integrated terminal
3. Run `claude` - the extension will auto-install

Going forward you can also use the `/ide` command in any external terminal to
connect to the IDE.

<Note>
  These installation instructions also apply to VS Code forks like Cursor and
  Windsurf.
</Note>

### JetBrains IDEs

Install the
[Claude Code plugin](https://docs.anthropic.com/s/claude-code-jetbrains) from
the marketplace and restart your IDE.

<Note>
  The plugin may also be auto-installed when you run `claude` in the integrated
  terminal. The IDE must be restarted completely to take effect.
</Note>

<Warning>
  **Remote Development Limitations**: When using JetBrains Remote Development,
  you must install the plugin in the remote host via `Settings > Plugin (Host)`.
</Warning>

## Configuration

Both integrations work with Claude Code's configuration system. To enable
IDE-specific features:

1. Connect Claude Code to your IDE by running `claude` in the built-in terminal
2. Run the `/config` command
3. Set the diff tool to `auto` for automatic IDE detection
4. Claude Code will automatically use the appropriate viewer based on your IDE

If you're using an external terminal (not the IDE's built-in terminal), you can
still connect to your IDE by using the `/ide` command after launching Claude
Code. This allows you to benefit from IDE integration features even when running
Claude from a separate terminal application. This works for both VS Code and
JetBrains IDEs.

<Note>
  When using an external terminal, to ensure Claude has default access to the
  same files as your IDE, start Claude from the same directory as your IDE
  project root.
</Note>

## Troubleshooting

### VS Code extension not installing

* Ensure you're running Claude Code from VS Code's integrated terminal
* Ensure that the CLI corresponding to your IDE is installed:
  * For VS Code: `code` command should be available
  * For Cursor: `cursor` command should be available
  * For Windsurf: `windsurf` command should be available
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
[troubleshooting guide](/en/docs/claude-code/troubleshooting) or reach out to
support.
