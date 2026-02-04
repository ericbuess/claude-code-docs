> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

* **Operating System**:
  * macOS 13.0+
  * Windows 10 1809+ or Windows Server 2019+ ([see setup notes](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([additional dependencies required](#platform-specific-setup))
* **Hardware**: 4 GB+ RAM
* **Network**: Internet connection required (see [network configuration](/en/network-config#network-access-requirements))
* **Shell**: Works best in Bash or Zsh
* **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

### Additional dependencies

* **ripgrep**: Usually included with Claude Code. If search fails, see [search troubleshooting](/en/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)**: Only required for [deprecated npm installation](#npm-installation-deprecated)

## Installation

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```sh  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

After the installation process completes, navigate to your project and start Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

If you encounter any issues during installation, consult the [troubleshooting guide](/en/troubleshooting).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Platform-specific setup

**Windows**: Run Claude Code natively (requires [Git Bash](https://git-scm.com/downloads/win)) or inside WSL. Both WSL 1 and WSL 2 are supported, but WSL 1 has limited support and does not support features like Bash tool sandboxing.

**Alpine Linux and other musl/uClibc-based distributions**:

The native installer on Alpine and other musl/uClibc-based distributions requires `libgcc`, `libstdc++`, and `ripgrep`. Install these using your distribution's package manager, then set `USE_BUILTIN_RIPGREP=0`.

On Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Authentication

#### For individuals

1. **Claude Pro or Max plan** (recommended): Subscribe to Claude's [Pro or Max plan](https://claude.ai/pricing) for a unified subscription that includes both Claude Code and Claude on the web. Manage your account in one place and log in with your Claude.ai account.
2. **Claude Console**: Connect through the [Claude Console](https://console.anthropic.com) and complete the OAuth process. Requires active billing in the Anthropic Console. A "Claude Code" workspace is automatically created for usage tracking and cost management. You can't create API keys for the Claude Code workspace; it's dedicated exclusively for Claude Code usage.

#### For teams and organizations

1. **Claude for Teams or Enterprise** (recommended): Subscribe to [Claude for Teams](https://claude.com/pricing#team-&-enterprise) or [Claude for Enterprise](https://anthropic.com/contact-sales) for centralized billing, team management, and access to both Claude Code and Claude on the web. Team members log in with their Claude.ai accounts.
2. **Claude Console with team billing**: Set up a shared [Claude Console](https://console.anthropic.com) organization with team billing. Invite team members and assign roles for usage tracking.
3. **Cloud providers**: Configure Claude Code to use [Amazon Bedrock, Google Vertex AI, or Microsoft Foundry](/en/third-party-integrations) for deployments with your existing cloud infrastructure.

### Install a specific version

The native installer accepts either a specific version number or a release channel (`latest` or `stable`). The channel you choose at install time becomes your default for auto-updates. See [Configure release channel](#configure-release-channel) for more information.

To install the latest version (default):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

To install the stable version:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

To install a specific version number:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Binary integrity and code signing

* SHA256 checksums for all platforms are published in the release manifests, currently located at `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (example: replace `{VERSION}` with `2.0.30`)
* Signed binaries are distributed for the following platforms:
  * macOS: Signed by "Anthropic PBC" and notarized by Apple
  * Windows: Signed by "Anthropic, PBC"

## NPM installation (deprecated)

NPM installation is deprecated. Use the [native installation](#installation) method when possible. To migrate an existing npm installation to native, run `claude install`.

**Global npm installation**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [troubleshooting permission errors](/en/troubleshooting#command-not-found-claude-or-permission-errors) for recommended solutions.
</Warning>

## Windows setup

**Option 1: Claude Code within WSL**

* Both WSL 1 and WSL 2 are supported
* WSL 2 supports [sandboxing](/en/sandboxing) for enhanced security. WSL 1 does not support sandboxing.

**Option 2: Claude Code on native Windows with Git Bash**

* Requires [Git for Windows](https://git-scm.com/downloads/win)
* For portable Git installations, specify the path to your `bash.exe`:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

* **Update checks**: Performed on startup and periodically while running
* **Update process**: Downloads and installs automatically in the background
* **Notifications**: You'll see a notification when updates are installed
* **Applying updates**: Updates take effect the next time you start Claude Code

<Note>
  Homebrew and WinGet installations do not auto-update. Use `brew upgrade claude-code` or `winget upgrade Anthropic.ClaudeCode` to update manually.

  **Known issue:** Claude Code may notify you of updates before the new version is available in these package managers. If an upgrade fails, wait and try again later.
</Note>

### Configure release channel

Configure which release channel Claude Code follows for both auto-updates and `claude update` with the `autoUpdatesChannel` setting:

* `"latest"` (default): Receive new features as soon as they're released
* `"stable"`: Use a version that is typically about one week old, skipping releases with major regressions

Configure this via `/config` → **Auto-update channel**, or add it to your [settings.json file](/en/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

For enterprise deployments, you can enforce a consistent release channel across your organization using [managed settings](/en/permissions#managed-settings).

### Disable auto-updates

Set the `DISABLE_AUTOUPDATER` environment variable in your shell or [settings.json file](/en/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash  theme={null}
claude update
```

## Uninstall Claude Code

If you need to uninstall Claude Code, follow the instructions for your installation method.

### Native installation

Remove the Claude Code binary and version files:

**macOS, Linux, WSL:**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell:**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD:**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Homebrew installation

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet installation

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### NPM installation

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Clean up configuration files (optional)

<Warning>
  Removing configuration files will delete all your settings, allowed tools, MCP server configurations, and session history.
</Warning>

To remove Claude Code settings and cached data:

**macOS, Linux, WSL:**

```bash  theme={null}
# Remove user settings and state
rm -rf ~/.claude
rm ~/.claude.json

# Remove project-specific settings (run from your project directory)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# Remove user settings and state
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Remove project-specific settings (run from your project directory)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM Remove user settings and state
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Remove project-specific settings (run from your project directory)
rmdir /s /q ".claude"
del ".mcp.json"
```
