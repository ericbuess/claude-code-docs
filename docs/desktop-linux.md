> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Desktop on Linux (beta)

> Install and update the Claude desktop app on Ubuntu and Debian

<Note>
  Linux support for the Claude desktop app is in beta. The Chat, Cowork, and Code tabs are all available.
</Note>

The desktop app on Linux gives you the same Chat, Cowork, and Claude Code experience as macOS and Windows: parallel sessions, visual diff review, an integrated terminal and editor, and live app preview. See [Use Claude Code Desktop](/en/desktop) for the full feature reference.

## Requirements

* Ubuntu 22.04 or later, or Debian 12 or later
* x86\_64 or arm64

Other Debian-based distributions that meet these requirements may work but aren't officially tested.

## Install

Install from Anthropic's apt repository so that updates arrive through your system's regular package updates.

<Steps>
  <Step title="Add Anthropic's apt repository">
    This step downloads the signing key with `curl`, which fresh Debian and Ubuntu installations may not include. If the download command fails with `sudo: curl: command not found`, install curl first:

    ```bash theme={null}
    sudo apt install curl
    ```

    Download Anthropic's signing key:

    ```bash theme={null}
    sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc https://downloads.claude.ai/claude-desktop/key.asc
    ```

    Register the repository:

    ```bash theme={null}
    echo "deb [arch=amd64,arm64 signed-by=/usr/share/keyrings/claude-desktop-archive-keyring.asc] https://downloads.claude.ai/claude-desktop/apt/stable stable main" | sudo tee /etc/apt/sources.list.d/claude-desktop.list
    ```
  </Step>

  <Step title="Install the package">
    ```bash theme={null}
    sudo apt update && sudo apt install claude-desktop
    ```
  </Step>

  <Step title="Launch and sign in">
    Launch **Claude** from your application launcher, or run `claude-desktop` from a terminal, and sign in with your Anthropic account.

    The Linux app signs in the same way as on macOS and Windows: with a claude.ai subscription, or through your organization's SSO. Desktop doesn't accept a Claude Console API key directly; use the [CLI](/en/quickstart) for API-key authentication. For enterprise deployments that route Desktop to Google Cloud's Agent Platform or an LLM gateway, see the [enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration) and [network configuration](/en/network-config).
  </Step>
</Steps>

<Accordion title="Verify the signing key">
  You can confirm the downloaded signing key belongs to Anthropic:

  ```bash theme={null}
  gpg --show-keys /usr/share/keyrings/claude-desktop-archive-keyring.asc
  ```

  The fingerprint should be `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`.
</Accordion>

### Install from a downloaded file

If you can't use the apt repository, first download the `.deb` package for your architecture, x64 or arm64, from [claude.com/download](https://claude.com/download). Then open the downloaded file with your software installer, or install it with apt from the directory that contains the downloaded file:

```bash theme={null}
sudo apt install ./claude-desktop_*.deb
```

If apt reports `E: Unsupported file ./claude-desktop_*.deb given on commandline`, the pattern didn't match a `.deb` file in the current directory. Confirm the download completed, then run the command again from the directory that contains the file.

A `.deb` installed this way doesn't receive updates. To get updates through apt, add the repository as shown above, or uncomment the `deb` line in the placeholder entry the package writes to `/etc/apt/sources.list.d/claude-desktop.list`.

## Update

The desktop app doesn't update itself on Linux. Updates arrive with your system's regular package updates:

```bash theme={null}
sudo apt update && sudo apt upgrade
```

Your distribution's graphical software updater will also pick up new versions.

## Uninstall

```bash theme={null}
sudo apt remove claude-desktop
```

This removes the signing key along with the app, so if you added the repository entry during install, remove it too:

```bash theme={null}
sudo rm /etc/apt/sources.list.d/claude-desktop.list
```

## What's not in the Linux beta yet

* **Computer Use**: [app and screen control](/en/desktop#let-claude-use-your-computer) isn't available on Linux.
* **Dictation**: voice input isn't available in the Linux desktop app. Use [voice dictation](/en/voice-dictation) in the CLI instead.
* **Quick Entry global hotkey**: works on X11. On native Wayland it requires your desktop environment's GlobalShortcuts portal.
* **Fedora and RHEL**: only Debian-based distributions are supported today. Support for additional distributions is coming in the future.

For anything not yet available in the desktop app, the [CLI](/en/quickstart) runs the same Claude Code engine and supports a wider range of Linux distributions; see the [system requirements](/en/setup#system-requirements).
