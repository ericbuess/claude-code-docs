> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Advanced setup

> System requirements, platform-specific installation, version management, and uninstallation for Claude Code.

This page covers system requirements, platform-specific installation details, updates, and uninstallation. For a guided walkthrough of your first session, see the [quickstart](/en/quickstart). If you've never used a terminal before, see the [terminal guide](/en/terminal-guide).

## System requirements

Claude Code runs on the following platforms and configurations:

* **Operating system**:
  * macOS 13.0+
  * Windows 10 1809+ or Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Hardware**: 4 GB+ RAM, x64 or ARM64 processor
* **Network**: internet connection required. See [network configuration](/en/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell, or CMD. Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win). WSL setups do not.
* **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

### Additional dependencies

* **ripgrep**: usually included with Claude Code. If search fails, see [search troubleshooting](/en/troubleshooting#search-and-discovery-issues).

## Install Claude Code

<Tip>
  Prefer a graphical interface? The [Desktop app](/en/desktop-quickstart) lets you use Claude Code without the terminal. Download it for [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) or [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs).

  New to the terminal? See the [terminal guide](/en/terminal-guide) for step-by-step instructions.
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

    **Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it. WSL setups do not need it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

After installation completes, open a terminal in the project you want to work in and start Claude Code:

```bash theme={null}
claude
```

If you encounter any issues during installation, see the [troubleshooting guide](/en/troubleshooting).

### Set up on Windows

You can run Claude Code natively on Windows or inside WSL. Pick based on where your projects are located and which features you need:

| Option         | Requires                                             | [Sandboxing](/en/sandboxing) | When to use                                     |
| -------------- | ---------------------------------------------------- | ---------------------------- | ----------------------------------------------- |
| Native Windows | [Git for Windows](https://git-scm.com/downloads/win) | Not supported                | Windows-native projects and tools               |
| WSL 2          | WSL 2 enabled                                        | Supported                    | Linux toolchains or sandboxed command execution |
| WSL 1          | WSL 1 enabled                                        | Not supported                | If WSL 2 is unavailable                         |

**Option 1: Native Windows with Git Bash**

Install [Git for Windows](https://git-scm.com/downloads/win), then run the install command from PowerShell or CMD. You do not need to run as Administrator.

Whether you install from PowerShell or CMD only affects which install command you run. Your prompt shows `PS C:\Users\YourName>` in PowerShell and `C:\Users\YourName>` without the `PS` in CMD. If you're new to the terminal, the [terminal guide](/en/terminal-guide#windows) walks through each step.

After installation, launch `claude` from PowerShell, CMD, or Git Bash. Claude Code uses Git Bash internally to execute commands regardless of where you launched it. If Claude Code can't find your Git Bash installation, set the path in your [settings.json file](/en/settings):

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code can also run PowerShell natively on Windows. The PowerShell tool is rolling out progressively; set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` to opt in or `0` to opt out. See [PowerShell tool](/en/tools-reference#powershell-tool) for setup and limitations.

**Option 2: WSL**

Open your WSL distribution and run the Linux installer from the [install instructions](#install-claude-code) above. You install and launch `claude` inside the WSL terminal, not from PowerShell or CMD.

### Alpine Linux and musl-based distributions

The native installer on Alpine and other musl/uClibc-based distributions requires `libgcc`, `libstdc++`, and `ripgrep`. Install these using your distribution's package manager, then set `USE_BUILTIN_RIPGREP=0`.

This example installs the required packages on Alpine:

```bash theme={null}
apk add libgcc libstdc++ ripgrep
```

Then set `USE_BUILTIN_RIPGREP` to `0` in your [`settings.json`](/en/settings#available-settings) file:

```json theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Verify your installation

After installing, confirm Claude Code is working:

```bash theme={null}
claude --version
```

For a more detailed check of your installation and configuration, run [`claude doctor`](/en/troubleshooting#get-more-help):

```bash theme={null}
claude doctor
```

## Authenticate

Claude Code requires a Pro, Max, Team, Enterprise, or Console account. The free Claude.ai plan does not include Claude Code access. You can also use Claude Code with a third-party API provider like [Amazon Bedrock](/en/amazon-bedrock), [Google Vertex AI](/en/google-vertex-ai), or [Microsoft Foundry](/en/microsoft-foundry).

After installing, log in by running `claude` and following the browser prompts. See [Authentication](/en/authentication) for all account types and team setup options.

## Update Claude Code

Native installations automatically update in the background. You can [configure the release channel](#configure-release-channel) to control whether you receive updates immediately or on a delayed stable schedule, or [disable auto-updates](#disable-auto-updates) entirely. Homebrew and WinGet installations require manual updates.

### Auto-updates

Claude Code checks for updates on startup and periodically while running. Updates download and install in the background, then take effect the next time you start Claude Code.

<Note>
  Homebrew and WinGet installations do not auto-update. For Homebrew, run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed. For WinGet, run `winget upgrade Anthropic.ClaudeCode`.

  **Known issue:** Claude Code may notify you of updates before the new version is available in these package managers. If an upgrade fails, wait and try again later.

  Homebrew keeps old versions on disk after upgrades. Run `brew cleanup` periodically to reclaim disk space.
</Note>

### Configure release channel

Control which release channel Claude Code follows for auto-updates and `claude update` with the `autoUpdatesChannel` setting:

* `"latest"`, the default: receive new features as soon as they're released
* `"stable"`: use a version that is typically about one week old, skipping releases with major regressions

Configure this via `/config` → **Auto-update channel**, or add it to your [settings.json file](/en/settings):

```json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

For enterprise deployments, you can enforce a consistent release channel across your organization using [managed settings](/en/permissions#managed-settings).

Homebrew installations choose a channel by cask name instead of this setting: `claude-code` tracks stable and `claude-code@latest` tracks latest.

### Pin a minimum version

The `minimumVersion` setting establishes a floor. Background auto-updates and `claude update` refuse to install any version below this value, so moving to the `"stable"` channel does not downgrade you if you are already on a newer `"latest"` build.

Switching from `"latest"` to `"stable"` via `/config` prompts you to either stay on the current version or allow the downgrade. Choosing to stay sets `minimumVersion` to that version. Switching back to `"latest"` clears it.

Add it to your [settings.json file](/en/settings) to pin a floor explicitly:

```json theme={null}
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

In [managed settings](/en/permissions#managed-settings), this enforces an organization-wide minimum that user and project settings cannot override.

### Disable auto-updates

Set `DISABLE_AUTOUPDATER` to `"1"` in the `env` key of your [`settings.json`](/en/settings#available-settings) file:

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Update manually

To apply an update immediately without waiting for the next background check, run:

```bash theme={null}
claude update
```

## Advanced installation options

These options are for version pinning, migrating from npm, and verifying binary integrity.

### Install a specific version

The native installer accepts either a specific version number or a release channel (`latest` or `stable`). The channel you choose at install time becomes your default for auto-updates. See [configure release channel](#configure-release-channel) for more information.

To install the latest version (default):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

To install the stable version:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

To install a specific version number:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Deprecated npm installation

npm installation is deprecated. The native installer is faster, requires no dependencies, and auto-updates in the background. Use the [native installation](#install-claude-code) method when possible.

#### Migrate from npm to native

If you previously installed Claude Code with npm, switch to the native installer:

```bash theme={null}
# Install the native binary
curl -fsSL https://claude.ai/install.sh | bash

# Remove the old npm installation
npm uninstall -g @anthropic-ai/claude-code
```

You can also run `claude install` from an existing npm installation to install the native binary alongside it, then remove the npm version.

#### Install with npm

If you need npm installation for compatibility reasons, you must have [Node.js 18+](https://nodejs.org/en/download) installed. Install the package globally:

```bash theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks. If you encounter permission errors, see [troubleshooting permission errors](/en/troubleshooting#permission-errors-during-installation).
</Warning>

### Binary integrity and code signing

Each release publishes a `manifest.json` containing SHA256 checksums for every platform binary. The manifest is signed with an Anthropic GPG key, so verifying the signature on the manifest transitively verifies every binary it lists.

#### Verify the manifest signature

Steps 1-3 require a POSIX shell with `gpg` and `curl`. On Windows, run them in Git Bash or WSL. Step 4 includes a PowerShell option.

<Steps>
  <Step title="Download and import the public key">
    The release signing key is published at a fixed URL.

    ```bash theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Display the fingerprint of the imported key.

    ```bash theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Confirm the output includes this fingerprint:

    ```text theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Download the manifest and signature">
    Set `VERSION` to the release you want to verify.

    ```bash theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Verify the signature">
    Verify the detached signature against the manifest.

    ```bash theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    A valid result reports `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` also prints `WARNING: This key is not certified with a trusted signature!` for any freshly imported key. This is expected. The `Good signature` line confirms the cryptographic check passed. The fingerprint comparison in Step 1 confirms the key itself is authentic.
  </Step>

  <Step title="Check the binary against the manifest">
    Compare the SHA256 checksum of your downloaded binary with the value listed under `platforms.<platform>.checksum` in `manifest.json`.

    <Tabs>
      <Tab title="Linux">
        ```bash theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  Manifest signatures are available for releases from `2.1.89` onward. Earlier releases publish checksums in `manifest.json` without a detached signature.
</Note>

#### Platform code signatures

In addition to the signed manifest, individual binaries carry platform-native code signatures where supported.

* **macOS**: signed by "Anthropic PBC" and notarized by Apple. Verify with `codesign --verify --verbose ./claude`.
* **Windows**: signed by "Anthropic, PBC". Verify with `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: use the manifest signature above to verify integrity. Linux binaries are not individually code-signed.

## Uninstall Claude Code

To remove Claude Code, follow the instructions for your installation method.

### Native installation

Remove the Claude Code binary and version files:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Homebrew installation

Remove the Homebrew cask you installed. If you installed the stable cask:

```bash theme={null}
brew uninstall --cask claude-code
```

If you installed the latest cask:

```bash theme={null}
brew uninstall --cask claude-code@latest
```

### WinGet installation

Remove the WinGet package:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Remove the global npm package:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Remove configuration files

<Warning>
  Removing configuration files will delete all your settings, allowed tools, MCP server configurations, and session history.
</Warning>

The VS Code extension, the JetBrains plugin, and the Desktop app also write to `~/.claude/`. If any of them is still installed, the directory is recreated the next time it runs. To remove Claude Code completely, uninstall the [VS Code extension](/en/vs-code#uninstall-the-extension), the JetBrains plugin, and the Desktop app before deleting these files.

To remove Claude Code settings and cached data:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    # Remove user settings and state
    rm -rf ~/.claude
    rm ~/.claude.json

    # Remove project-specific settings (run from your project directory)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    # Remove user settings and state
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Remove project-specific settings (run from your project directory)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
