> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Desktop on Linux (beta)

> Install and update the Claude desktop app on Ubuntu and Debian

<Note>
  Linux support for the Claude desktop app is in beta.
</Note>

The desktop app on Linux gives you the same Chat, Cowork, and Claude Code experience as on macOS and Windows: parallel sessions, visual diff review, an integrated terminal and editor, and live app preview. See [Use Claude Code Desktop](/docs/en/desktop) for the feature reference.

## Requirements

* Ubuntu 22.04 or later, or Debian 12 or later
* x86\_64 or arm64

Other Debian-based distributions that meet these requirements may work but aren't officially tested. On distributions that aren't Debian-based, such as Fedora or Arch, run the [CLI](/docs/en/setup#system-requirements) instead. If you work on Windows with WSL 2, install the Windows desktop app and run sessions inside your distribution; see [Claude Code Desktop in WSL](/docs/en/desktop-wsl).

### Cowork requirements

Cowork is the desktop tab for [Dispatch and longer agentic work](https://claude.com/docs/cowork/overview). On Linux, Cowork runs those tasks in a virtual machine that the desktop app hosts with QEMU and KVM. To use Cowork, your machine needs:

* **Hardware virtualization**: turned on in your firmware settings. Without it, the Cowork tab reports "Cowork requires hardware virtualization (KVM)".
* **QEMU and UEFI firmware**: `qemu-system-x86`, `ovmf`, and `virtiofsd` on x86\_64, or `qemu-system-arm`, `qemu-efi-aarch64`, and `virtiofsd` on arm64. `apt install claude-desktop` installs them by default as recommended packages. If you installed with `--no-install-recommends`, or your system is a minimal image that skips recommended packages, the Cowork tab reports "Cowork requires QEMU" and shows the `apt install` command to run. Ubuntu 22.04 has no `virtiofsd` package; the app uses a bundled copy there.
* **Access to `/dev/kvm`**: add your user to the `kvm` group with `sudo usermod -aG kvm $USER`, then log out and back in. Some desktop environments grant the logged-in user access to `/dev/kvm` without the group, but Cowork also needs `/dev/vhost-vsock`, which only `kvm` group members can open. Join the group even if `/dev/kvm` already works for you.

The app checks these requirements once at launch: restart it after installing packages, and log out and back in after joining the group. If your kernel has no module directory under `/lib/modules`, which is common on ChromeOS and in container-based Linux environments, the Cowork tab reports that the kernel doesn't include the virtualization support Cowork needs and that it can't be added manually.

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

    The command prints nothing when it succeeds and a `curl:` error when it doesn't. A missing or wrong key makes `apt update` fail later with `NO_PUBKEY BAA929FF1A7ECACE`, so confirm the key downloaded and belongs to Anthropic before continuing:

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

* Run `sudo apt update` after adding the repository. `apt install` on its own doesn't see a repository you added after the last time you ran `apt update`.
* Confirm the repository entry was written. `cat /etc/apt/sources.list.d/claude-desktop.list` should show the `deb` line from the [Add Anthropic's apt repository](#install) step. If the file is empty or missing, run that step again.
* Confirm your architecture is supported. `dpkg --print-architecture` should print `amd64` or `arm64`. The repository doesn't publish packages for other architectures.
* Run `sudo apt update` again and check its output for errors related to `downloads.claude.ai`. A network or key error there means the repository was added but couldn't be reached or verified.

If the repository is in place and reachable and the package is still not found, [install from a downloaded file](#install-from-a-downloaded-file) instead.

### Unmet dependencies

If `apt` stops with `The following packages have unmet dependencies` or `Unsatisfied dependencies`, read which dependency it names:

* `libc6 (>= 2.34)`: your distribution is older than the package supports. Ubuntu 20.04 ships `libc6` 2.31. Upgrade to Ubuntu 22.04 or later, or Debian 12 or later.
* All missing dependencies show `not installable` with an `:amd64` or `:arm64` suffix: you downloaded the `.deb` for a different architecture than your machine's. Run `dpkg --print-architecture` and download the matching `.deb`, or [install from the apt repository](#install), which selects the package for your architecture.

### Running as root without --no-sandbox is not supported

If `claude-desktop` exits with this message, you launched it as root. Log in as a regular user and launch it from there.

### Cowork isn't available

If the Cowork tab shows one of these messages, fix the requirement it names, then restart the app:

* **Cowork requires QEMU**: install the [QEMU and UEFI firmware packages](#cowork-requirements) the message lists.
* **Cowork requires hardware virtualization (KVM)**: turn on [hardware virtualization](#cowork-requirements) in your firmware settings.
* **Claude doesn't have permission to use virtualization (/dev/kvm)**: add your user to the [`kvm` group](#cowork-requirements), then log out and back in.
* **Cowork requires the `vhost_vsock` kernel module**: run `sudo modprobe vhost_vsock`, then restart the app. That loads the module for the current boot only. To load it on every boot, run `echo vhost_vsock | sudo tee /etc/modules-load.d/vhost_vsock.conf`.

## What's not in the Linux beta yet

* **Computer Use**: [app and screen control](/docs/en/desktop#let-claude-use-your-computer) isn't available on Linux.
* **Dictation**: voice input isn't available in the Linux desktop app. Use [voice dictation](/docs/en/voice-dictation) in the CLI instead.
* **Quick Entry global hotkey**: works on X11. On native Wayland it requires your desktop environment's GlobalShortcuts portal.
* **Fedora and RHEL**: only Debian-based distributions are supported today. Support for additional distributions is coming in the future.

For anything not yet available in the desktop app, the [CLI](/docs/en/quickstart) runs the same Claude Code engine and supports a wider range of Linux distributions; see the [system requirements](/docs/en/setup#system-requirements).
