> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Test iOS apps in the simulator

> Claude Code Desktop opens your app in the iOS Simulator pane when Claude builds, runs, or checks it, with a separate simulator for each session.

<Note>
  The iOS Simulator pane is in public beta in Claude Code Desktop on macOS. It's available on Pro, Max, and Team plans, and not available on the Enterprise plan.
</Note>

The iOS Simulator pane shows your app running in Apple's iOS Simulator next to your conversation in Claude Code Desktop. When Claude builds, installs, launches, or checks your app in a simulator, the pane opens automatically and streams the device screen live. Use it to watch Claude run and test your app, or to tap through the app yourself while Claude keeps working.

The simulator pane drives the simulator directly, so it doesn't need [computer use](/docs/en/desktop#let-claude-use-your-computer) and never takes over your screen or hides your other windows. From the CLI, Claude reaches the iOS Simulator through [computer use](/docs/en/computer-use#test-a-simulator-flow) instead, which controls the simulator on your screen the same way you would with a mouse.

## Requirements

The simulator pane uses Apple's simulator tooling, which the desktop app doesn't include. Before starting a session, make sure you have:

* Claude Desktop v1.24012.0 or later
* A Mac, since Apple's iOS Simulator runs only on macOS
* [Xcode](https://developer.apple.com/xcode/) with the iOS platform installed, which provides the simulator devices. If Xcode lists no simulators yet, see [The simulator pane says no simulators were found](#the-simulator-pane-says-no-simulators-were-found)

<Note>
  On this page, "device" refers to a simulated iPhone or iPad, one of the same simulator devices you manage in Xcode under **Window → Devices and Simulators**, not physical hardware.
</Note>

The simulator pane is available in local sessions only. In [cloud](/docs/en/desktop#run-long-running-tasks-remotely) and [SSH](/docs/en/desktop#ssh-sessions) sessions, Claude runs on a machine that can't reach the simulators on your Mac.

## Run your app in the simulator

You don't need a command or setting to open the simulator pane. Claude opens it when it runs your app in a simulator.

<Steps>
  <Step title="Open your iOS project">
    In Claude Code Desktop, open the **Code** tab and start a session with your app's project as the [project folder](/docs/en/desktop#start-a-session). Any project that builds an app for the iOS Simulator works.
  </Step>

  <Step title="Ask Claude to run or test the app">
    Phrase the task around running or verifying the app. For example:

    ```text theme={null}
    Build the app and run it in the simulator to check the onboarding flow.
    ```
  </Step>

  <Step title="Watch the app in the simulator pane">
    When the app launches in a simulator, the iOS Simulator pane opens next to the conversation. The first time Claude uses a device, the desktop app asks you to allow it; see [Grant Claude access to a device](#grant-claude-access-to-a-device). Claude installs the app, taps through it, and reads the screen to verify its own changes while you watch.
  </Step>
</Steps>

The simulator pane opens whenever Claude launches the app in a simulator, at any point in the session. When your request is about seeing the app, for example "does the new screen look right?", Claude starts a simulator before it begins the work. After Claude fixes a bug or changes a screen, ask it to verify the change: relaunching the app reopens the pane if it isn't open.

The simulator pane shows whichever device the app actually launched in. To test on a specific device, name it in your request, for example "run it on the iPhone SE simulator", and Claude targets that device when it builds and launches.

A device Claude boots also appears in Apple's Simulator app, and Claude can install the app on a device you already have booted.

You can also open the simulator pane yourself. Once the session has a simulator attached or has edited Swift files, the **Views** menu in the session toolbar shows an **iOS Simulator** entry. If the pane isn't showing a device yet, click **Attach simulator**, or pick a specific device from the device menu next to it; picking a shut-down device boots it. If Xcode or its simulators are missing, the pane shows the setup steps instead and checks them off as you complete them.

## Control the simulator yourself

The simulator pane is interactive, not only a viewer. While Claude works, or between tasks, you can:

* Tap and swipe by clicking and dragging on the device screen
* Press hardware buttons with the same shortcuts as Apple's Simulator app: **Cmd+Shift+H** for Home, **Cmd+L** to lock, **Cmd+Up Arrow** and **Cmd+Down Arrow** for volume
* Rotate the device a quarter turn clockwise with the rotate button or **Cmd+Right Arrow**
* Switch which device the pane shows from the device menu, which lists each simulator's OS version and whether it's booted
* Save a screenshot with **Cmd+S** or a screen recording with **Cmd+R**, using the pane's capture buttons or the shortcuts; the files are saved to your Desktop
* Stop streaming a device without shutting it down by clicking **Detach simulator**, which returns the pane to its **Attach simulator** state

The row under the device name tunes the video stream from the simulator. Lower **Frame rate** or **Resolution** if the pane strains your Mac, switch **Encoding** between H.264 and JPEG, or check **FPS** to display the frame rate the pane is receiving. These settings change how the pane displays the device, not how the app runs.

You and Claude drive the same device, so your taps change the app state Claude sees. To have Claude check a specific screen, navigate to it by tapping, then ask. While Claude is driving the device, the pane shows a **Claude is using this device** badge above the screen; hold off tapping until the badge clears, so the result reflects the app rather than your input.

## How sessions manage devices

Each device belongs to the session that launched it, so [parallel sessions](/docs/en/desktop#work-in-parallel-with-sessions) don't share a device: what you see in one session's pane reflects that session's work, not another's. Switching sessions in the sidebar switches the simulator view along with the conversation, and switching back resumes the same device where it left off. If Claude works with more than one device, each opens its own pane, up to 4 per session.

Claude Code Desktop shuts down the simulators it booted once they're no longer in use: when you quit the app, when you archive the session, or 10 minutes after you detach a device from its pane. Devices you boot yourself, whether from the pane or in Apple's Simulator app, are never shut down automatically. To shut down the attached device right away, use the shutdown button in the pane.

## Grant Claude access to a device

Claude asks for your consent before it controls a device, while building the app or opening a URL on it follows your session's permission mode. You or your organization can also turn Claude's access off entirely.

### Allow a device the first time

The first time Claude uses a simulator, the desktop app asks you to allow it. The consent covers controlling that device and taking screenshots of it, and you give it once per device rather than once per session. Claude's screenshots of the device are sent to Anthropic and kept under your normal conversation retention settings, so don't sign in to real accounts on a device Claude uses.

After you allow a device, Claude's actions on it, such as tapping, typing, launching the app, and taking screenshots, run without further prompts. They carry the same trust as you clicking in the pane, and they only touch the simulated device, so the pane doesn't need the macOS Accessibility and Screen Recording permissions that computer use requires.

If you decline, the device still boots and the pane still works for your own taps; only Claude's access stays off. To change your mind later, click **Let Claude use it** in the pane.

### Actions that follow your permission mode

Two actions follow your session's [permission mode](/docs/en/permissions#permission-modes) instead of the one-time consent:

* Opening a URL on the device, for example to test a deep link or load a page in the device's Safari, because a URL can carry data off the device.
* Building the app, because `xcodebuild` runs your project's build scripts on your Mac. Checking on a build already in progress doesn't prompt.

### Turn off simulator access

You can turn Claude's simulator access off in the desktop app's settings. Organizations have two ways to turn it off for everyone:

* The `disableMobileSimulatorTools` [managed setting](/docs/en/desktop#managed-settings) blocks Claude's simulator tools. The simulator pane stays usable for your own taps, and the setting can't be overridden from within the app.
* The `requireCoworkFullVmSandbox` policy key, which runs Claude's tools inside an isolated virtual machine instead of on your Mac, disables the simulator pane and Claude's simulator tools entirely, so the pane can't attach a device while it's set.

Claude tells you when either applies.

## Limitations

Claude drives simulated devices only and can't control a physical iPhone or iPad. To test on one, run the app on it from Xcode yourself, then describe what you see or attach a screenshot to the conversation for Claude to work from.

## Troubleshooting

### The simulator pane doesn't open when Claude runs the app

Claude may not have recognized that you wanted to run or test the app, or the simulator tooling may be missing. Check the following:

* State the goal explicitly, for example "run the app in the iOS Simulator and tap through the signup flow".
* Confirm Xcode and the iOS Simulator are installed by launching the Simulator app on its own.
* If your organization manages Claude Code, the [simulator tools may be disabled by policy](#turn-off-simulator-access).
* The simulator pane requires Claude Desktop v1.24012.0 or later. Open **Claude → Check for Updates**, then restart the app.

### The simulator pane says no simulators were found

Xcode is installed but has no iOS simulators to list. The simulator pane shows the setup steps to follow and checks them off as each one completes. To install the missing piece manually, download the iOS simulator runtime from Xcode's settings, or run `xcodebuild -downloadPlatform iOS`.

## See also

* [Computer use in Desktop](/docs/en/desktop#let-claude-use-your-computer): screen control for apps without a dedicated pane
* [Computer use from the CLI](/docs/en/computer-use): how the CLI reaches the iOS Simulator
* [Work in parallel with sessions](/docs/en/desktop#work-in-parallel-with-sessions): how sessions isolate changes
* [Get started with Claude Code Desktop](/docs/en/desktop-quickstart)
