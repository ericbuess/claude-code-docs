> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Desktop on Linux (beta)

> Install and update the Claude desktop app on Ubuntu and Debian

<Note>
  Linux support for the Claude desktop app is in beta. The Chat, Cowork, and Code tabs are all available.
</Note>

The desktop app on Linux gives you the same Chat, Cowork, and Claude Code experience as macOS and Windows: parallel sessions, visual diff review, an integrated terminal and editor, and live app preview. See [Use Claude Code Desktop](/docs/en/desktop) for the full feature reference.

## Requirements

* Ubuntu 22.04 or later, or Debian 12 or later
* x86\_64 or arm64

Other Debian-based distributions that meet these requirements may work but aren't officially tested.

## Install

Install from Anthropic's apt repository so that updates arrive through your system's regular package updates. Open a terminal and run the commands in each step.

<Steps>
  <Step title="Add Anthropic's apt repository">
    This step downloads the signing key with `curl` and verifies it with `gpg`, which fresh Debian and Ubuntu installations may not include. If either command reports `command not found`, install both first:

    ```bash theme={null}
    sudo apt install curl gnupg
    ```

    Download Anthropic's signing key:

    ```bash theme={null}
    sudo curl -fsSLo /usr/share/keyrings/claude-desktop-archive-keyring.asc https://downloads.claude.ai/claude-desktop/key.asc
    ```

    If this download fails, `apt update` later fails with `NO_PUBKEY BAA929FF1A7ECACE`. Confirm the key downloaded and belongs to Anthropic before continuing:

    ```bash theme={null}
    gpg --show-keys /usr/share/keyrings/claude-desktop-archive-keyring.asc
    ```

    The fingerprint gpg prints should be `31DDDE24DDFAB679F42D7BD2BAA929FF1A7ECACE`. If gpg reports that the file can't be opened or contains no valid OpenPGP data, the download failed or returned the wrong content: confirm your network can reach `downloads.claude.ai`, then rerun the download command.

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

    The Linux app signs in the same way as on macOS and Windows: with a claude.ai subscription, or through your organization's SSO. Desktop doesn't accept a Claude Console API key directly; use the [CLI](/docs/en/quickstart) for API-key authentication. For enterprise deployments that route Desktop to Google Cloud's Agent Platform or an LLM gateway, see [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) and [network configuration](/docs/en/network-config).
  </Step>
</Steps>

### Install from a downloaded file

If you can't install through the apt repository, download the `.deb` package directly from the repository's package pool. This command looks up the newest package for your architecture in the repository index, then downloads it to the current directory:

```bash theme={null}
curl -fLO "https://downloads.claude.ai/claude-desktop/apt/stable/$(curl -s "https://downloads.claude.ai/claude-desktop/apt/stable/dists/stable/main/binary-$(dpkg --print-architecture)/Packages" | grep '^Filename: pool/main/c/claude-desktop/claude-desktop_' | sort -V | tail -n 1 | cut -d' ' -f2)"
```

If the command fails with `Remote file name has no length`, the lookup returned no package path. This can mean the repository index couldn't be fetched, for example when your network blocks `downloads.claude.ai`, or that no package exists for your architecture. Confirm that your network can reach `downloads.claude.ai` and that `dpkg --print-architecture` prints `amd64` or `arm64`; the repository doesn't publish packages for other architectures.

To install without registering Anthropic's apt repository, first create `/etc/default/claude-desktop` with the line `CLAUDE_DESKTOP_ADD_REPO="false"`. Without the repository, apt doesn't deliver new versions; to update, re-run the download command and reinstall, or [register the repository](#install) later.

Then open the downloaded file with your software installer, such as GNOME Software, or install it with apt from the directory that contains the downloaded file:

```bash theme={null}
sudo apt install ./claude-desktop_*.deb
```

If apt reports `E: Unsupported file ./claude-desktop_*.deb given on commandline`, the pattern didn't match a `.deb` file in the current directory. Confirm the download completed, then run the command again from the directory that contains the file.

Installing the `.deb` also registers Anthropic's apt repository at `/etc/apt/sources.list.d/claude-desktop.list`, so future updates arrive with your system's [regular package updates](#update).

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

Uninstalling the package also removes the repository entry and signing key it registered. If you added the repository entry yourself with the [Add Anthropic's apt repository](#install) step, remove it too:

```bash theme={null}
sudo rm /etc/apt/sources.list.d/claude-desktop.list
```

## Troubleshoot

### Unable to locate package claude-desktop

If `sudo apt install claude-desktop` fails with `E: Unable to locate package claude-desktop`, apt didn't find the repository you added. Check the following:

* Confirm the repository entry was written. `cat /etc/apt/sources.list.d/claude-desktop.list` should show the `deb` line from the [Add Anthropic's apt repository](#install) step. If the file is empty or missing, run that step again.
* Confirm your architecture is supported. `dpkg --print-architecture` should print `amd64` or `arm64`. The repository doesn't publish packages for other architectures.
* Run `sudo apt update` again and check its output for errors related to `downloads.claude.ai`. A network or key error there means the repository was added but couldn't be reached or verified.

If the repository is in place and reachable and the package is still not found, [install from a downloaded file](#install-from-a-downloaded-file) instead.

## What's not in the Linux beta yet

* **Computer Use**: [app and screen control](/docs/en/desktop#let-claude-use-your-computer) isn't available on Linux.
* **Dictation**: voice input isn't available in the Linux desktop app. Use [voice dictation](/docs/en/voice-dictation) in the CLI instead.
* **Quick Entry global hotkey**: works on X11. On native Wayland it requires your desktop environment's GlobalShortcuts portal.
* **Fedora and RHEL**: only Debian-based distributions are supported today. Support for additional distributions is coming in the future.

For anything not yet available in the desktop app, the [CLI](/docs/en/quickstart) runs the same Claude Code engine and supports a wider range of Linux distributions; see the [system requirements](/docs/en/setup#system-requirements).
