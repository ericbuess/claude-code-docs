# Troubleshooting

> Discover solutions to common issues with Claude Code installation and usage.

## Common installation issues

### Windows installation issues: errors in WSL

You might encounter the following issues in WSL:

**OS/platform detection issues**: If you receive an error during installation, WSL may be using Windows `npm`. Try:

* Run `npm config set os linux` before installation
* Install with `npm install -g @anthropic-ai/claude-code --force --no-os-check` (Do NOT use `sudo`)

**Node not found errors**: If you see `exec: node: not found` when running `claude`, your WSL environment may be using a Windows installation of Node.js. You can confirm this with `which npm` and `which node`, which should point to Linux paths starting with `/usr/` rather than `/mnt/c/`. To fix this, try installing Node via your Linux distribution's package manager or via [`nvm`](https://github.com/nvm-sh/nvm).

**nvm version conflicts**: If you have nvm installed in both WSL and Windows, you may experience version conflicts when switching Node versions in WSL. This happens because WSL imports the Windows PATH by default, causing Windows nvm/npm to take priority over the WSL installation.

You can identify this issue by:

* Running `which npm` and `which node` - if they point to Windows paths (starting with `/mnt/c/`), Windows versions are being used
* Experiencing broken functionality after switching Node versions with nvm in WSL

To resolve this issue, fix your Linux PATH to ensure the Linux node/npm versions take priority:

**Primary solution: Ensure nvm is properly loaded in your shell**

The most common cause is that nvm isn't loaded in non-interactive shells. Add the following to your shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.):

```bash  theme={null}
# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

Or run directly in your current session:

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**Alternative: Adjust PATH order**

If nvm is properly loaded but Windows paths still take priority, you can explicitly prepend your Linux paths to PATH in your shell configuration:

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  Avoid disabling Windows PATH importing (`appendWindowsPath = false`) as this breaks the ability to easily call Windows executables from WSL. Similarly, avoid uninstalling Node.js from Windows if you use it for Windows development.
</Warning>

### Linux and Mac installation issues: permission or command not found errors

When installing Claude Code with npm, `PATH` problems may prevent access to `claude`.
You may also encounter permission errors if your npm global prefix is not user writable (eg. `/usr`, or `/usr/local`).

#### Recommended solution: Native Claude Code installation

Claude Code has a native installation that doesn't depend on npm or Node.js.

<Note>
  The native Claude Code installer is currently in beta.
</Note>

Use the following command to run the native installer.

**macOS, Linux, WSL:**

```bash  theme={null}
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

**Windows PowerShell:**

```powershell  theme={null}
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58

```

This command installs the appropriate build of Claude Code for your operating system and architecture and adds a symlink to the installation at `~/.local/bin/claude`.

<Tip>
  Make sure that you have the installation directory in your system PATH.
</Tip>

#### Alternative solution: Migrate to local installation

Alternatively, if Claude Code will run, you can migrate to a local installation:

```bash  theme={null}
claude migrate-installer
```

This moves Claude Code to `~/.claude/local/` and sets up an alias in your shell configuration. No `sudo` is required for future updates.

After migration, restart your shell, and then verify your installation:

On macOS/Linux/WSL:

```bash  theme={null}
which claude  # Should show an alias to ~/.claude/local/claude
```

On Windows:

```powershell  theme={null}
where claude  # Should show path to claude executable
```

Verify installation:

```bash  theme={null}
claude doctor # Check installation health
```

## Permissions and authentication

### Repeated permission prompts

If you find yourself repeatedly approving the same commands, you can allow specific tools
to run without approval using the `/permissions` command. See [Permissions docs](/en/iam#configuring-permissions).

### Authentication issues

If you're experiencing authentication problems:

1. Run `/logout` to sign out completely
2. Close Claude Code
3. Restart with `claude` and complete the authentication process again

If problems persist, try:

```bash  theme={null}
rm -rf ~/.config/claude-code/auth.json
claude
```

This removes your stored authentication information and forces a clean login.

## Performance and stability

### High CPU or memory usage

Claude Code is designed to work with most development environments, but may consume significant resources when processing large codebases. If you're experiencing performance issues:

1. Use `/compact` regularly to reduce context size
2. Close and restart Claude Code between major tasks
3. Consider adding large build directories to your `.gitignore` file

### Command hangs or freezes

If Claude Code seems unresponsive:

1. Press Ctrl+C to attempt to cancel the current operation
2. If unresponsive, you may need to close the terminal and restart

### Search and discovery issues

If Search tool, `@file` mentions, custom agents, and custom slash commands aren't working, install system `ripgrep`:

```bash  theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Then set `USE_BUILTIN_RIPGREP=0` in your [environment](/en/settings#environment-variables).

### Slow or incomplete search results on WSL

Disk read performance penalties when [working across file systems on WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) may result in fewer-than-expected matches (but not a complete lack of search functionality) when using Claude Code on WSL.

<Note>
  `/doctor` will show Search as OK in this case.
</Note>

**Solutions:**

1. **Submit more specific searches**: Reduce the number of files searched by specifying directories or file types: "Search for JWT validation logic in the auth-service package" or "Find use of md5 hash in JS files".

2. **Move project to Linux filesystem**: If possible, ensure your project is located on the Linux filesystem (`/home/`) rather than the Windows filesystem (`/mnt/c/`).

3. **Use native Windows instead**: Consider running Claude Code natively on Windows instead of through WSL, for better file system performance.

## IDE integration issues

### JetBrains IDE not detected on WSL2

If you're using Claude Code on WSL2 with JetBrains IDEs and getting "No available IDEs detected" errors, this is likely due to WSL2's networking configuration or Windows Firewall blocking the connection.

#### WSL2 networking modes

WSL2 uses NAT networking by default, which can prevent IDE detection. You have two options:

**Option 1: Configure Windows Firewall** (recommended)

1. Find your WSL2 IP address:
   ```bash  theme={null}
   wsl hostname -I
   # Example output: 172.21.123.456
   ```

2. Open PowerShell as Administrator and create a firewall rule:
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   (Adjust the IP range based on your WSL2 subnet from step 1)

3. Restart both your IDE and Claude Code

**Option 2: Switch to mirrored networking**

Add to `.wslconfig` in your Windows user directory:

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

Then restart WSL with `wsl --shutdown` from PowerShell.

<Note>
  These networking issues only affect WSL2. WSL1 uses the host's network directly and doesn't require these configurations.
</Note>

For additional JetBrains configuration tips, see our [IDE integration guide](/en/vs-code#jetbrains-plugin-settings).

### Reporting Windows IDE integration issues (both native and WSL)

If you're experiencing IDE integration problems on Windows, please [create an issue](https://github.com/anthropics/claude-code/issues) with the following information: whether you are native (git bash), or WSL1/WSL2, WSL networking mode (NAT or mirrored), IDE name/version, Claude Code extension/plugin version, and shell type (bash/zsh/etc)

### ESC key not working in JetBrains (IntelliJ, PyCharm, etc.) terminals

If you're using Claude Code in JetBrains terminals and the ESC key doesn't interrupt the agent as expected, this is likely due to a keybinding clash with JetBrains' default shortcuts.

To fix this issue:

1. Go to Settings → Tools → Terminal
2. Either:
   * Uncheck "Move focus to the editor with Escape", or
   * Click "Configure terminal keybindings" and delete the "Switch focus to Editor" shortcut
3. Apply the changes

This allows the ESC key to properly interrupt Claude Code operations.

## Markdown formatting issues

Claude Code sometimes generates markdown files with missing language tags on code fences, which can affect syntax highlighting and readability in GitHub, editors, and documentation tools.

### Missing language tags in code blocks

If you notice code blocks like this in generated markdown:

````markdown  theme={null}
```
function example() {
  return "hello";
}
```
````

Instead of properly tagged blocks like:

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```
````

**Solutions:**

1. **Ask Claude to add language tags**: Simply request "Please add appropriate language tags to all code blocks in this markdown file."

2. **Use post-processing hooks**: Set up automatic formatting hooks to detect and add missing language tags. See the [markdown formatting hook example](/en/hooks-guide#markdown-formatting-hook) for implementation details.

3. **Manual verification**: After generating markdown files, review them for proper code block formatting and request corrections if needed.

### Inconsistent spacing and formatting

If generated markdown has excessive blank lines or inconsistent spacing:

**Solutions:**

1. **Request formatting corrections**: Ask Claude to "Fix spacing and formatting issues in this markdown file."

2. **Use formatting tools**: Set up hooks to run markdown formatters like `prettier` or custom formatting scripts on generated markdown files.

3. **Specify formatting preferences**: Include formatting requirements in your prompts or project [memory](/en/memory) files.

### Best practices for markdown generation

To minimize formatting issues:

* **Be explicit in requests**: Ask for "properly formatted markdown with language-tagged code blocks"
* **Use project conventions**: Document your preferred markdown style in [CLAUDE.md](/en/memory)
* **Set up validation hooks**: Use post-processing hooks to automatically verify and fix common formatting issues

## Getting more help

If you're experiencing issues not covered here:

1. Use the `/bug` command within Claude Code to report problems directly to Anthropic
2. Check the [GitHub repository](https://github.com/anthropics/claude-code) for known issues
3. Run `/doctor` to check the health of your Claude Code installation
4. Ask Claude directly about its capabilities and features - Claude has built-in access to its documentation
