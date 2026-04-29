> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Use Claude Code with JetBrains IDEs including IntelliJ, PyCharm, WebStorm, and more

Claude Code integrates with JetBrains IDEs through a dedicated plugin, providing features like interactive diff viewing, selection context sharing, and more.

## Supported IDEs

The Claude Code plugin works with most JetBrains IDEs, including:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Features

* **Quick launch**: use `Cmd+Esc` (Mac) or `Ctrl+Esc` (Windows/Linux) to open Claude Code directly from your editor, or click the Claude Code button in the UI
* **Diff viewing**: code changes can be displayed directly in the IDE diff viewer instead of the terminal
* **Selection context**: the current selection or tab in the IDE is automatically shared with Claude Code
* **File reference shortcuts**: use `Cmd+Option+K` (Mac) or `Alt+Ctrl+K` (Linux/Windows) to insert file references such as `@src/auth.ts#L1-99`
* **Diagnostic sharing**: diagnostic errors from the IDE, such as lint and syntax errors, are automatically shared with Claude as you work

## Installation

### Marketplace installation

Find and install the [Claude Code plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) from the JetBrains marketplace and restart your IDE.

If you haven't installed Claude Code yet, see the [quickstart guide](/en/quickstart) for installation instructions.

<Note>
  After installing the plugin, you may need to restart your IDE completely for it to take effect.
</Note>

## Usage

### From your IDE

Run `claude` from your IDE's integrated terminal, and all integration features will be active.

### From external terminals

Use the `/ide` command in any external terminal to connect Claude Code to your JetBrains IDE and activate all features:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

If you want Claude to have access to the same files as your IDE, start Claude Code from the same directory as your IDE project root.

## Configuration

### Claude Code settings

Configure IDE integration through Claude Code's settings:

1. Run `claude`
2. Enter the `/config` command
3. Set the diff tool to `auto` to show diffs in the IDE, or `terminal` to keep them in the terminal

### Plugin settings

Configure the Claude Code plugin by going to **Settings → Tools → Claude Code \[Beta]**:

#### General settings

* **Claude command**: specify a custom command to run Claude, for example `claude`, `/usr/local/bin/claude`, or `npx @anthropic-ai/claude-code`
* **Suppress notification for Claude command not found**: skip notifications about not finding the Claude command
* **Enable using Option+Enter for multi-line prompts**: on macOS only. When enabled, Option+Enter inserts new lines in Claude Code prompts. Disable if the Option key is being captured unexpectedly. Requires a terminal restart.
* **Enable automatic updates**: automatically check for and install plugin updates, applied on restart

<Tip>
  For WSL users: Set `wsl -d Ubuntu -- bash -lic "claude"` as your Claude command (replace `Ubuntu` with your WSL distribution name)
</Tip>

#### ESC key configuration

If the ESC key doesn't interrupt Claude Code operations in JetBrains terminals:

1. Go to **Settings → Tools → Terminal**
2. Either:
   * Uncheck "Move focus to the editor with Escape", or
   * Click "Configure terminal keybindings" and delete the "Switch focus to Editor" shortcut
3. Apply the changes

This allows the ESC key to properly interrupt Claude Code operations.

## Special configurations

### Remote development

<Warning>
  When using JetBrains Remote Development, you must install the plugin in the remote host via **Settings → Plugin (Host)**.
</Warning>

The plugin must be installed on the remote host, not on your local client machine.

### WSL configuration

If you're using Claude Code on WSL2 with a JetBrains IDE and see "No available IDEs detected", the cause is usually WSL2's NAT networking or Windows Firewall blocking the connection between WSL2 and the IDE running on the Windows host. WSL1 uses the host's network directly and isn't affected.

#### Allow WSL2 traffic through Windows Firewall

This is the recommended fix because it keeps your existing WSL2 networking mode.

<Steps>
  <Step title="Find your WSL2 IP address">
    From inside your WSL shell, run:

    ```bash theme={null}
    hostname -I
    ```

    Note the subnet, for example `172.21.123.45` is in `172.21.0.0/16`.
  </Step>

  <Step title="Create a firewall rule">
    Open PowerShell as Administrator and run the following, adjusting the IP range to match your subnet:

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="Restart your IDE and Claude Code">
    Close and reopen both so the new rule takes effect.
  </Step>
</Steps>

#### Switch WSL2 to mirrored networking

Mirrored networking requires Windows 11 22H2 or later. If you're on Windows 10, use the firewall rule above instead.

Add this to `.wslconfig` in your Windows user directory:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Then restart WSL with `wsl --shutdown` from PowerShell.

## Troubleshooting

### Plugin not working

If the plugin is installed but Claude Code features don't appear in your IDE:

* Ensure you're running Claude Code from the project root directory
* Check that the JetBrains plugin is enabled in the IDE settings
* Completely restart the IDE (you may need to do this multiple times)
* For Remote Development, ensure the plugin is installed in the remote host

### IDE not detected

If running `claude` shows "No available IDEs detected":

* Verify the plugin is installed and enabled
* Restart the IDE completely
* Check that you're running Claude Code from the integrated terminal
* For WSL users, see [WSL configuration](#wsl-configuration) above

### Command not found

If clicking the Claude icon shows "command not found":

1. Verify Claude Code is installed by running `claude --version` in a terminal
2. Configure the Claude command path in plugin settings
3. For WSL users, use the WSL command format mentioned in the configuration section

## Security considerations

When Claude Code runs in a JetBrains IDE with auto-edit permissions enabled, it may be able to modify IDE configuration files that can be automatically executed by your IDE. This may increase the risk of running Claude Code in auto-edit mode and allow bypassing Claude Code's permission prompts for bash execution.

When running in JetBrains IDEs, consider:

* Using manual approval mode for edits
* Taking extra care to ensure Claude is only used with trusted prompts
* Being aware of which files Claude Code has access to modify

For Claude Code installation or login problems outside the IDE, see [Troubleshoot installation and login](/en/troubleshoot-install).
