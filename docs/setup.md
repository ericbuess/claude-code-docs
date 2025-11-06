# Set up Claude Code

> Install, authenticate, and start using Claude Code on your development machine.

## System requirements

* **Operating Systems**: macOS 10.15+, Ubuntu 20.04+/Debian 10+, or Windows 10+ (with WSL 1, WSL 2, or Git for Windows)
* **Hardware**: 4GB+ RAM
* **Software**: [Node.js 18+](https://nodejs.org/en/download) (only required for NPM installation)
* **Network**: Internet connection required for authentication and AI processing
* **Shell**: Works best in Bash, Zsh or Fish
* **Location**: [Anthropic supported countries](https://www.anthropic.com/supported-countries)

### Additional dependencies

* **ripgrep**: Usually included with Claude Code. If search functionality fails, see [search troubleshooting](/en/troubleshooting#search-and-discovery-issues).

## Standard installation

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **Homebrew (macOS, Linux):**

    ```sh  theme={null}
    brew install --cask claude-code
    ```

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
  </Tab>

  <Tab title="NPM">
    If you have [Node.js 18 or newer installed](https://nodejs.org/en/download/):

    ```sh  theme={null}
    npm install -g @anthropic-ai/claude-code
    ```
  </Tab>
</Tabs>

<Note>
  Some users may be automatically migrated to an improved installation method.
</Note>

After the installation process completes, navigate to your project and start Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Claude Code offers the following authentication options:

1. **Claude Console**: The default option. Connect through the Claude Console and complete the OAuth process. Requires active billing at [console.anthropic.com](https://console.anthropic.com). A "Claude Code" workspace will be automatically created for usage tracking and cost management. Note that you cannot create API keys for the Claude Code workspace - it is dedicated exclusively for Claude Code usage.
2. **Claude App (with Pro or Max plan)**: Subscribe to Claude's [Pro or Max plan](https://claude.com/pricing) for a unified subscription that includes both Claude Code and the web interface. Get more value at the same price point while managing your account in one place. Log in with your Claude.ai account. During launch, choose the option that matches your subscription type.
3. **Enterprise platforms**: Configure Claude Code to use [Amazon Bedrock or Google Vertex AI](/en/third-party-integrations) for enterprise deployments with your existing cloud infrastructure.

<Note>
  Claude Code securely stores your credentials. See [Credential Management](/en/iam#credential-management) for details.
</Note>

## Windows setup

**Option 1: Claude Code within WSL**

* Both WSL 1 and WSL 2 are supported

**Option 2: Claude Code on native Windows with Git Bash**

* Requires [Git for Windows](https://git-scm.com/downloads/win)
* For portable Git installations, specify the path to your `bash.exe`:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Alternative installation methods

Claude Code offers multiple installation methods to suit different environments.

If you encounter any issues during installation, consult the [troubleshooting guide](/en/troubleshooting#linux-permission-issues).

<Tip>
  Run `claude doctor` after installation to check your installation type and version.
</Tip>

### Native installation options

The native installation is the recommended method and offers several benefits:

* One self-contained executable
* No Node.js dependency
* Improved auto-updater stability

If you have an existing installation of Claude Code, use `claude install` to migrate to the native binary installation.

For advanced installation options with the native installer:

**macOS, Linux, WSL:**

```bash  theme={null}
# Install stable version (default)
curl -fsSL https://claude.ai/install.sh | bash

# Install latest version
curl -fsSL https://claude.ai/install.sh | bash -s latest

# Install specific version number
curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
```

<Note>
  **Alpine Linux and other musl/uClibc-based distributions**: The native build requires you to install `libgcc`, `libstdc++`, and `ripgrep`. Install (Alpine: `apk add libgcc libstdc++ ripgrep`) and set `USE_BUILTIN_RIPGREP=0`.
</Note>

<Note>
  Claude Code installed via Homebrew will auto-update outside of the brew directory unless explicitly disabled with the `DISABLE_AUTOUPDATER` environment variable (see [Auto updates](#auto-updates) section).
</Note>

**Windows PowerShell:**

```powershell  theme={null}
# Install stable version (default)
irm https://claude.ai/install.ps1 | iex

# Install latest version
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) latest

# Install specific version number
& ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
```

**Windows CMD:**

```batch  theme={null}
REM Install stable version (default)
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd

REM Install latest version
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd latest && del install.cmd

REM Install specific version number
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
```

<Tip>
  Make sure that you remove any outdated aliases or symlinks before installing.
</Tip>

### NPM installation

For environments where NPM is preferred or required:

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Do NOT use `sudo npm install -g` as this can lead to permission issues and security risks.
  If you encounter permission errors, see [configure Claude Code](/en/troubleshooting#linux-permission-issues) for recommended solutions.
</Warning>

### Local installation

* After global install via npm, use `claude migrate-installer` to move to local
* Avoids autoupdater npm permission issues
* Some users may be automatically migrated to this method

## Running on AWS or GCP

By default, Claude Code uses the Claude API.

For details on running Claude Code on AWS or GCP, see [third-party integrations](/en/third-party-integrations).

## Update Claude Code

### Auto updates

Claude Code automatically keeps itself up to date to ensure you have the latest features and security fixes.

* **Update checks**: Performed on startup and periodically while running
* **Update process**: Downloads and installs automatically in the background
* **Notifications**: You'll see a notification when updates are installed
* **Applying updates**: Updates take effect the next time you start Claude Code

**Disable auto-updates:**

Set the `DISABLE_AUTOUPDATER` environment variable in your shell or [settings.json file](/en/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Update manually

```bash  theme={null}
claude update
```
