> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continue local sessions from any device with Remote Control

> Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.

<Note>
  Remote Control is available on all plans. On Team and Enterprise, it is off by default until an Owner enables the Remote Control toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control connects [claude.ai/code](https://claude.ai/code) or the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) to a Claude Code session running on your machine. Start a task at your desk, then pick it up from your phone on the couch or a browser on another computer.

When you start a Remote Control session on your machine, Claude keeps running locally the entire time, so your code execution and filesystem access stay on your machine. With Remote Control you can:

* **Use your full local environment remotely**: your filesystem, [MCP servers](/docs/en/mcp), tools, and project configuration all stay available, and typing `@` autocompletes file paths from your local project.
* **Work from both surfaces at once**: the conversation and the progress of [subagents](/docs/en/sub-agents) and [dynamic workflows](/docs/en/workflows) stay in sync across all connected devices, so you can send messages from your terminal, browser, and phone interchangeably.
* **Send images and files from your phone or browser**: attach a photo or file in the Claude app or at claude.ai/code, with or without a caption. Claude sees attached photos directly as part of your message. Claude Code downloads other files to your machine and passes them to Claude as `@` file references.
* **Survive interruptions**: if your laptop sleeps or your network drops, Claude Code reconnects automatically when your machine comes back online. While the connection is rebuilding, Claude Code queues messages, permission prompts, and status updates from subagents and workflows, and delivers them once the connection recovers.

Unlike [Claude Code on the web](/docs/en/claude-code-on-the-web), which runs on cloud infrastructure, Remote Control sessions run directly on your machine and interact with your local filesystem. The web and mobile interfaces are a window into that local session.

This page covers setup, how to start and connect to sessions, and how Remote Control compares to Claude Code on the web.

## Requirements

Before using Remote Control, confirm that your environment meets these conditions:

* **Subscription**: available on Pro, Max, Team, and Enterprise plans. API keys are not supported. On Team and Enterprise, an Owner must first enable the Remote Control toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).
* **Authentication**: run `claude` and use `/login` to sign in through claude.ai if you haven't already. Without an eligible login, `claude remote-control` exits with an error, while `claude --remote-control` still starts an interactive session and shows a Remote Control failure notification shortly after launch.
* **API endpoint**: not available in any of these configurations:
  * You use Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry.
  * You point [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) at a host other than `api.anthropic.com`, such as an [LLM gateway](/docs/en/llm-gateway) or proxy. Unset the variable to use Remote Control. Before v2.1.196, Claude Code allowed Remote Control with a custom `ANTHROPIC_BASE_URL`.
  * You sign in through an enterprise [Claude apps gateway](/docs/en/claude-apps-gateway).
* **Feature-flag evaluation**: [`DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, and `DISABLE_GROWTHBOOK`](/docs/en/env-vars) each disable the feature-flag evaluation that Remote Control availability depends on. Unset the variable wherever it's set, in your shell environment or in the `env` block of a [`settings.json` file](/docs/en/settings-reference#all-settings), to use Remote Control.
* **Workspace trust**: run `claude` in your project directory at least once to accept the workspace trust dialog. The startup trust dialog never saves trust for your home directory, so start Remote Control from a project directory.

## Start a Remote Control session

You can start a Remote Control session from the CLI or the VS Code extension. The CLI offers three invocation modes; VS Code uses the `/remote-control` command.

<Tabs>
  <Tab title="Server mode">
    Navigate to your project directory and run:

    ```bash theme={null}
    claude remote-control
    ```

    The process stays running in your terminal in server mode, waiting for remote connections. It displays a session URL you can use to [connect from another device](#connect-from-another-device), and you can press spacebar to show a QR code for quick access from your phone. While a remote session is active, the terminal shows connection status and tool activity.

    Available flags:

    | Flag                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
    | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`                           | Set a custom session title visible in the session list at claude.ai/code.                                                                                                                                                                                                                                                                                                                                                                                                          |
    | `--remote-control-session-name-prefix <prefix>` | Prefix for auto-generated session names when no explicit name is set. Defaults to your machine's hostname, producing names like `myhost-graceful-unicorn`. Set `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` for the same effect.                                                                                                                                                                                                                                                    |
    | `-c`, `--continue`                              | Bring back the session that the last server in this directory started with, instead of creating a new one. See [Resume sessions after stopping the server](#resume-sessions-after-stopping-the-server). Can't be combined with `--session-id`, `--spawn`, `--capacity`, or `--create-session-in-dir`. Requires Claude Code v2.1.200 or later; earlier versions reject the flag as an unknown argument.                                                                             |
    | `--session-id <id>`                             | Bring back one session by its ID. See [Resume sessions after stopping the server](#resume-sessions-after-stopping-the-server). Can't be combined with `--continue`, `--spawn`, `--capacity`, or `--create-session-in-dir`. Requires Claude Code v2.1.200 or later; earlier versions reject the flag as an unknown argument.                                                                                                                                                        |
    | `--spawn <mode>`                                | How the server creates sessions.<br />• `same-dir` (default): all sessions share the current working directory, so they can conflict if editing the same files.<br />• `worktree`: each on-demand session gets its own [git worktree](/docs/en/worktrees). Requires a git repository.<br />• `session`: single-session mode. Serves exactly one session and rejects additional connections. Set at startup only.<br />Press `w` at runtime to toggle between `same-dir` and `worktree`. |
    | `--capacity <N>`                                | Maximum number of concurrent sessions. Default is 32. Cannot be used with `--spawn=session`.                                                                                                                                                                                                                                                                                                                                                                                       |
    | `--[no-]create-session-in-dir`                  | Pre-create one session in the current directory when the server starts, so you have somewhere to type immediately. In `worktree` mode this session stays in the current directory while on-demand sessions get isolated worktrees. On by default. If you pass `--no-create-session-in-dir` to start with none, Claude Code archives the server's sessions when you stop it, so there's nothing to [resume](#resume-sessions-after-stopping-the-server).                            |
    | `--permission-mode <mode>`                      | Set the starting [permission mode](/docs/en/permission-modes) for the server's sessions, such as `acceptEdits`. Accepts `manual` as an alias for `default`; an unrecognized mode stops the server at startup and lists the valid modes.                                                                                                                                                                                                                                                 |
    | `--debug-file <path>`                           | Write debug logs to the given file.                                                                                                                                                                                                                                                                                                                                                                                                                                                |
    | `--verbose`                                     | Show detailed connection and session logs.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
    | `--sandbox` / `--no-sandbox`                    | Enable or disable [sandboxing](/docs/en/sandboxing) for filesystem and network isolation. Off by default.                                                                                                                                                                                                                                                                                                                                                                               |

    Give these flags after `remote-control`.

    If you pass a global `claude` flag before `remote-control`, or a wrapper script adds one, Claude Code doesn't carry the flag over to the sessions the server creates. Claude Code lets the flag through only when dropping it is known not to change what those sessions can do, such as `--verbose` or `--model`. For any other flag, such as `--settings`, Claude Code [refuses to start](/docs/en/errors#not-carried-over-to-the-sessions-remote-control-starts) and names the flag to remove. Before v2.1.248, any option before `remote-control` made Claude Code reject the flags after it with an `unknown option` error.

    Claude Code checks Remote Control eligibility before printing help, so `claude remote-control --help` returns an error instead of this flag list when you aren't signed in with an eligible account.
  </Tab>

  <Tab title="Interactive session">
    To start a normal interactive Claude Code session with Remote Control enabled, use the `--remote-control` flag (or `--rc`):

    ```bash theme={null}
    claude --remote-control
    ```

    Optionally pass a name for the session:

    ```bash theme={null}
    claude --remote-control "My Project"
    ```

    This gives you a full interactive session in your terminal that you can also control from claude.ai or the Claude app. Unlike `claude remote-control` (server mode), you can type messages locally while the session is also available remotely.
  </Tab>

  <Tab title="From an existing session">
    If you're already in a Claude Code session and want to continue it remotely, use the `/remote-control` (or `/rc`) command:

    ```text theme={null}
    /remote-control
    ```

    Pass a name as an argument to set a custom session title:

    ```text theme={null}
    /remote-control My Project
    ```

    This starts a Remote Control session that carries over your current conversation history.

    The `--verbose`, `--sandbox`, and `--no-sandbox` flags are not available with this command.
  </Tab>

  <Tab title="VS Code">
    In the [Claude Code VS Code extension](/docs/en/vs-code), type `/remote-control` or `/rc` in the prompt box.

    ```text theme={null}
    /remote-control
    ```

    While Remote Control is on, Claude Code shows a **Remote Control** indicator in the prompt box footer. Once the session connects, click the indicator to go directly to the session, or find it in the session list at [claude.ai/code](https://claude.ai/code). Claude Code also posts the session URL in the conversation. To disconnect, run `/remote-control` again.

    Unlike the CLI, the VS Code command does not accept a name argument or display a QR code. The session title is derived from your conversation history or first prompt.
  </Tab>
</Tabs>

### Check connection status

In an interactive terminal session, a `/rc active` indicator sits in the footer below the input box while the connection is up, and is hidden if the terminal is too narrow to fit it. The indicator text is a link to the session on claude.ai. Select it with the down arrow key and press Enter, or run `/remote-control` again, to open a status panel with the session URL and a QR code you can use to [connect from another device](#connect-from-another-device). The status panel also offers a disconnect option. Select it to turn Remote Control off; your local session keeps running in the terminal.

If the connection fails, Claude Code shows a notification with the failure reason and switches the indicator to a failure state that stays in the footer. To read the reason again, select the indicator with the down arrow key and press Enter. To reconnect, run `/remote-control`, unless the [reason says the session was taken over or ended elsewhere, or that the server can't find it](#session-ended-elsewhere).

<span id="session-ended-elsewhere" />Read the reason before you reconnect. When the session was taken over or ended from another device, app, or Claude Code session, or the server can't find it, the reason says which, and Claude Code leaves out its usual advice to run `/remote-control`:

* **Another device or Claude Code session took the session over**: run `/remote-control` only if you want to take it back from that device.
* **You ended or archived the session from another device or app**: run `/remote-control` only if you want it back; Claude Code reopens an archived session.
* **The server can't find the session**: it may have been deleted from another device or app.

### Session URL reminders

While Remote Control is connected, Claude Code reminds you of the session URL when switching to your phone or browser helps most, so you don't have to find the link in `/remote-control`. A reminder appears above the prompt box at either of these moments:

* **Long turn**: when a turn runs longer than a server-tuned threshold, Claude Code shows a **Still working** notification with a **Check in from your phone** link, so you can follow the turn from your phone or browser instead of waiting at the terminal. Claude Code removes it when the turn ends.
* **Repeated permission prompts**: after you answer several [permission prompts](/docs/en/permissions) in a session, an **Approve tool calls from your phone** notification shows the session URL. Claude Code removes it when your next turn starts.

The reminders can appear in any connected session, including ones where Remote Control [connects automatically](#enable-remote-control-for-all-sessions). They don't appear every time these conditions occur, and each one appears only a few times in total across sessions. You can't configure or turn them off; each clears on its own.

### Connect from another device

Once a Remote Control session is active, you have a few ways to connect from another device:

* **Open the session URL** in any browser to go directly to the session on [claude.ai/code](https://claude.ai/code).
* **Scan the QR code** shown alongside the session URL to open it directly in the Claude app. With `claude remote-control`, press spacebar to toggle the QR code display.
* **Open [claude.ai/code](https://claude.ai/code) or the Claude app** and find the session by name in the session list. In the Claude mobile app, tap **Code** in the navigation to reach the session list. Remote Control sessions show a computer icon with a green status dot when online.

When you connect, the device shows any subagents and workflows the session already has running in the background. Stop one of them from the device, and Claude Code stops that task on your machine.

The remote session title is chosen in this order:

1. The name you passed to `--name`, `--remote-control`, or `/remote-control`
2. The title you set with `/rename`
3. The last meaningful message in existing conversation history
4. An auto-generated name like `myhost-graceful-unicorn`, where `myhost` is your machine's hostname or the prefix you set with `--remote-control-session-name-prefix`

If you didn't set an explicit name, Claude Code updates the title to reflect your prompt once you send one. Claude Code matches auto-generated titles to the language of your conversation, or to the [`language`](/docs/en/settings-reference#language) setting if one is configured; the language matching requires Claude Code v2.1.176 or later.

When you rename a session from claude.ai or the Claude app, Claude Code also updates the local title shown in `claude --resume`. Claude Code applies the same rename to the session name shown on the prompt bar, and in the `claude agents` listing when the session [runs in the background](/docs/en/agent-view). Before v2.1.221, renaming from the session list at claude.ai or in the Claude app updated only the title, and the CLI kept its previous session name; `/rename`, which runs in the CLI itself, set the name on any version.

If you don't have the Claude app yet, use the `/mobile` command inside Claude Code to display a download QR code for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### What connected devices see

A connected device shows the conversation in your terminal as it happens. These cases go beyond ordinary messages:

* **Compaction and `/clear`**: while Claude Code [compacts the conversation](/docs/en/context-window#what-survives-compaction), connected devices show the progress and then where the conversation was compacted. When you run `/clear`, the conversation resets on connected devices too.
* **Switching conversations with `/resume`**: the connected device doesn't receive the switched-to conversation's title or earlier history, but new messages in both directions go to and from whichever conversation is open in your terminal. To work on the original conversation from the device again, run `/resume` in your terminal and switch back to it.
* **Messages from your other sessions**: with [cross-session messaging](/docs/en/cross-session-messaging), the same connection carries messages between your own sessions on different machines and from your [Claude Code on the web](/docs/en/claude-code-on-the-web) sessions, through Anthropic servers like the rest of Remote Control traffic. [Message sessions on other machines](/docs/en/cross-session-messaging#message-sessions-on-other-machines) covers the delivery rules and [Control inbound messages](/docs/en/cross-session-messaging#control-inbound-messages) covers the inbound controls. Requires Claude Code v2.1.224 or later.
* **Prompts you send mid-turn**: when you send a prompt from a connected device before the current turn ends, Claude Code queues it and keeps it in the device's transcript after that turn finishes.
* **Diff of your changes**: when the session's directory is in a git repository, a connected device's diff pane shows the diff of your uncommitted changes. The device requests the diff over the connection, and Claude Code computes it on your machine. When your working tree is clean, Claude Code instead serves your branch's changes since it diverged from the default branch. Before v2.1.247, Claude Code reported the diff to connected devices only in sessions served by `claude remote-control`.
* **Model**: when you pick a [model](/docs/en/model-config) from a connected device, Claude Code runs the session on that model. The terminal's `/model` picker, `/status`, and `/config` show that model. A pick from the device's model control lasts for the current session only. `/model <name>` sent from the device also sets your default for new sessions, the same as typing it in the terminal.
* **Effort level**: when you set the [effort level](/docs/en/model-config#adjust-effort-level) from a connected device, with `/effort` or the device's effort control, Claude Code applies it to the session on your machine, and claude.ai/code shows the level the session is using. If you pinned a level with `CLAUDE_CODE_EFFORT_LEVEL`, the session keeps that level, and Claude Code refuses a different pick from the effort control. A level you pick from the effort control applies to the current session only and doesn't change your saved default. Picking a level from the effort control requires Claude Code v2.1.234 or later on your machine.
* **Reconnecting after a connection failure**: run `/remote-control` to reconnect. If compaction rewrote the conversation or you switched conversations with `/resume` in the meantime, Claude Code archives the server session it was using instead of leaving it in the session list. You can still find it by [filtering for archived sessions](/docs/en/claude-code-on-the-web#archive-sessions). Switching conversations while a device is still connected doesn't archive the session.

### Enable Remote Control for all sessions

Remote Control only activates when you explicitly run `claude remote-control`, `claude --remote-control`, or `/remote-control`, unless auto-connect is turned on. To turn auto-connect on for every interactive session, run `/config` inside Claude Code and set **Enable Remote Control for all sessions**. The toggle takes three values:

* **`true`**: connect automatically when an interactive session starts.
* **`false`**: turn auto-connect off, though a `true` from [managed settings](/docs/en/managed-settings) outranks it, because Claude Code saves the choice to your user settings. A `false` in project or local settings (`.claude/settings.json`, `.claude/settings.local.json`) turns auto-connect off even over a managed `true`.
* **`default`**: clear your choice and follow your organization's admin default if one is set, otherwise Claude Code's current default.

The same toggle appears outside the CLI:

* **Desktop app**: **Settings > Claude Code > Enable remote control by default**.
* **VS Code extension**: **Enable Remote Control for all sessions** in the [command menu's](/docs/en/vs-code#use-the-prompt-box) Settings section. Requires Claude Code v2.1.203 or later.

To turn auto-connect on from a settings file instead, set [`remoteControlAtStartup`](/docs/en/settings-reference#remotecontrolatstartup) to `true` in your user `~/.claude/settings.json` or in [managed settings](/docs/en/managed-settings). In project or local settings (`.claude/settings.json`, `.claude/settings.local.json`), Claude Code honors a `false` and turns auto-connect off for that repository, but ignores a `true`, so a checked-in file can't turn on Remote Control for everyone who opens the repository.

Auto-connect signs in with your own claude.ai account, so a session it starts appears only in your own account's Claude apps and grants no one else access.

With this setting on, each interactive Claude Code process registers one remote session. If you run multiple instances, each one gets its own remote session. To run multiple concurrent sessions from a single process, use [server mode](#start-a-remote-control-session) instead.

### Resume sessions after stopping the server

When you stop `claude remote-control` with Ctrl+C, the sessions it was serving stop responding from your phone or browser. As long as you weren't running another `claude remote-control` in the same directory and didn't start this one with `--no-create-session-in-dir`, Claude Code doesn't archive them. To bring them back, run one of these commands in the same directory:

* **`claude remote-control`**: brings back every session the server was serving.
* **`claude remote-control --continue`**: brings back only the session the server started with, and exits when that session ends. If this directory has no record, Claude Code uses the newest one from this repository's other git worktrees.
* **`claude remote-control --session-id <id>`**: brings back only the session whose ID you pass, and exits when that session ends. The ID is the part of the session's URL at claude.ai/code between `/code/` and any `?`.

These commands work for about four hours after the server stopped. After that, run `claude remote-control` to start a new session. If you archived a session in the meantime, `--continue` and `--session-id` unarchive it on Claude Code v2.1.228 or later.

To bring back a session you started with `claude --remote-control` or `/remote-control`, resume the conversation with `claude --continue` or `claude --resume`. Whether Claude Code reconnects, and to which session, depends on the conversation's [reconnection record](#resume-outcomes).

If you resume the conversation in a second terminal while the first one still has Remote Control on, Claude Code prints a notice in the second terminal and leaves Remote Control off there instead of taking the session away from the first. While Remote Control stays off there, Claude in that terminal doesn't see [your sessions on other machines](/docs/en/cross-session-messaging#see-which-sessions-claude-can-reach), and they can't reach it. Run `/remote-control` in the second terminal to move Remote Control to it.

When you resume a conversation in Claude Desktop or an IDE extension that had Remote Control on, Claude Code reattaches it to the existing claude.ai session instead of adding a new one to the session list.

## Connection and security

Your local Claude Code session makes outbound HTTPS requests only and never opens inbound ports on your machine. When you start Remote Control, it registers with the Anthropic API and polls for work. When you connect from another device, the server routes messages between the web or mobile client and your local session over a streaming connection.

All traffic travels through the Anthropic API over TLS, the same transport security as any Claude Code session. The connection uses multiple short-lived credentials, each scoped to a single purpose and expiring independently.

While Remote Control is connected, the session transcript, including your messages, Claude's responses, and tool activity, is stored on Anthropic servers. The stored transcript keeps the conversation in sync across your devices and lets the session reconnect after a network drop. Execution and filesystem access stay on your machine, and stored transcripts are retained under the [Data usage](/docs/en/data-usage) policy.

To turn Remote Control off entirely, use the [`disableRemoteControl`](/docs/en/settings-reference#disableremotecontrol) setting. Organizations with compliance requirements such as Zero Data Retention can't enable Remote Control.

## Trusted Devices

<Note>
  Trusted Devices is currently in beta. Features and functionality may evolve as the experience is refined.

  Trusted Devices is available on Team and Enterprise plans. It is off by default until an Owner enables it.
</Note>

Trusted Devices is an organization-wide setting that requires members to verify their device before they can view or steer Remote Control sessions from claude.ai, the Claude mobile apps, or Claude Desktop. It ties Remote Control access to a known device and a recent authentication, not just a signed-in account.

When the setting is on, interacting with a Remote Control session requires both of the following:

* **An enrolled device**: each browser, phone, or desktop app a member uses for Remote Control enrolls its own credential. Enrollment is only offered shortly after a full sign-in, so a device joins the trusted list as part of a real authentication rather than silently in the background.
* **A recent sign-in**: the member's sign-in must be no more than 18 hours old. Instead of signing in again each day, members confirm presence with Face ID, Touch ID, Windows Hello, or a passkey. This biometric step-up refreshes the session immediately.

Biometric checks run on the device through the operating system or browser, the same mechanism as passkey sign-in. Anthropic never receives or stores fingerprints, face data, or any other biometric information. Only the device's public key and basic metadata such as display name, platform, and enrollment time are stored.

The setting applies only to Remote Control. Regular Claude chat, Claude Code in the terminal, and API usage are unaffected.

### Enable Trusted Devices for your organization

An Owner enables the setting from the Claude Code admin console.

<Steps>
  <Step title="Open Claude Code admin settings">
    Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code). The **Require trusted devices** toggle appears under the Remote Control setting.
  </Step>

  <Step title="Turn on Require trusted devices">
    The setting applies to every member of the organization and to Remote Control sessions started after you enable it. Sessions that were already running before the toggle was turned on are not retroactively protected and continue without the device requirement until they end. Per-team or per-project scoping is not available.
  </Step>

  <Step title="Tell members what to expect">
    The first time a member views or steers a new Remote Control session from a browser, phone, or desktop app after the setting is enabled, they are prompted to enroll that device. Letting them know ahead of time avoids confusion.
  </Step>
</Steps>

### What members see

Enrollment is a one-time step per device. After that, the only visible change is an occasional biometric prompt.

* **First use on each device**: the member is asked to enroll. If their sign-in is not recent, they sign in first through your normal flow, including SSO if configured, then confirm enrollment.
* **Day to day**: members with an enrolled device and a recent sign-in see no prompts. When the sign-in ages past 18 hours, the next Remote Control interaction shows a single Face ID, Touch ID, Windows Hello, or passkey prompt.
* **Unenrolled devices**: Remote Control sessions cannot be viewed or steered until the device is enrolled. Regular Claude chat on that device is unaffected.
* **No platform authenticator**: members on a machine without Face ID, Touch ID, or Windows Hello can use a hardware security key, or sign in again instead of stepping up.
* **In the terminal**: the machine running Claude Code receives its own credential automatically when the developer signs in to the CLI. There is no separate enrollment step in the terminal.

### Manage enrolled devices

Members can review and revoke their own devices from account settings.

Open [claude.ai/settings/account](https://claude.ai/settings/account#trusted-devices) and find the **Trusted devices** section to see every enrolled device with its name, platform, and enrollment date. Removing a device revokes its credential immediately, and the device can re-enroll later after a fresh sign-in. Credentials also expire on their own if not renewed, so an unused device drops off the trusted list automatically.

For a lost or stolen device, the member removes it from this page. If the member cannot sign in, an admin can use **Sign out everywhere** in the admin console to revoke every session and enrolled device for that member, after which the member re-enrolls the devices they still hold.

## Remote Control vs Claude Code on the web

Remote Control and [Claude Code on the web](/docs/en/claude-code-on-the-web) both use the claude.ai/code interface. The key difference is where the session runs: Remote Control executes on your machine, so your local MCP servers, tools, and project configuration stay available. Claude Code on the web executes in the cloud.

Use Remote Control when you're in the middle of local work and want to keep going from another device. Use Claude Code on the web when you want to kick off a task without any local setup, work on a repo you don't have cloned, or run multiple tasks in parallel.

## Mobile push notifications

When Remote Control is active, Claude can send push notifications to your phone.

Claude decides when to push. It typically sends one when a long-running task finishes or when it needs a decision from you to continue. You can also request a push in your prompt, for example `notify me when the tests finish`. Beyond the two on/off toggles below, there is no per-event configuration.

To set up mobile push notifications:

<Steps>
  <Step title="Install the Claude mobile app">
    Download the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).
  </Step>

  <Step title="Sign in with your Claude Code account">
    Use the same account and organization you use for Claude Code in the terminal.
  </Step>

  <Step title="Allow notifications">
    Accept the notification permission prompt from the operating system.
  </Step>

  <Step title="Enable push in Claude Code">
    In your terminal, run `/config` and enable **Push when Claude decides** for proactive notifications, **Push when actions required** for permission prompts and questions, or both.
  </Step>
</Steps>

If notifications don't arrive:

* If `/config` shows **No mobile registered**, open the Claude app on your phone so it can refresh its push token. The warning clears the next time Remote Control connects.
* On iOS, Focus modes and notification summaries can suppress or delay pushes. Check Settings → Notifications → Claude.
* On Android, aggressive battery optimization can delay delivery. Exempt the Claude app from battery optimization in system settings.

Claude Code skips mobile push notifications while you are typing in or focused on the connected terminal. As of v2.1.181, you can set [`CLAUDE_CLIENT_PRESENCE_FILE`](/docs/en/env-vars) to a marker file path to extend this to any time you are at the machine, even in another window: notifications are skipped while the file exists. Configure a screen-lock listener or similar tool to create the file when your screen unlocks and delete it when your screen locks.

## Limitations

* **One remote session per interactive process**: outside of server mode, each Claude Code instance supports one remote session at a time. Use [server mode](#start-a-remote-control-session) to run multiple concurrent sessions from a single process.
* **Local process must keep running**: Remote Control runs as a local process. If you close the terminal, quit VS Code, or otherwise stop the `claude` process, the session goes offline until you [bring it back](#resume-sessions-after-stopping-the-server). Unless Claude is in the middle of a task, claude.ai and the Claude app show the session as offline within seconds after the process exits. To keep a session running on a remote machine after you disconnect from SSH, start it inside `tmux` or `screen`.
* **Crashed sessions in server mode**: if a session served by `claude remote-control` crashes, send it a message from a connected device. Claude Code serves it again. You don't have to restart the server.
* **HTTP 403 refusals on a connected session**: once an interactive session is connected, Claude Code keeps retrying for up to three minutes when something between your machine and Anthropic's servers answers with HTTP 403, as can happen after a VPN or network change. If the refusals last longer, Claude Code disconnects, and the reason names what refused: a network edge, or a proxy, VPN, or firewall on your own network.
* **Extended network outage**: if your machine is awake but can't reach the network, what you do next depends on the mode:
  * **Server mode**: Claude Code gives up after roughly 10 minutes and the `claude remote-control` process exits. Run `claude remote-control` again to start a new session.
  * **Interactive session**: keep working locally. Claude Code retries for as long as the outage lasts and reconnects on its own when the network returns.
* **Presence heartbeats failing**: if an interactive session disconnects with `could not reach the Remote Control server for about 30 minutes`, run `/remote-control` to reconnect. Claude Code shows this message only when the session's presence heartbeats have been failing while the rest of the connection stayed up; it re-registers the session for about 30 minutes before disconnecting.
* **Forwarded dialogs expire**: Claude Code keeps permission prompts and `AskUserQuestion` questions open until you answer them. When Claude Code forwards another kind of dialog to the remote session, such as the model-choice prompt shown after a safety refusal, it waits five minutes by default, then closes the dialog and continues with the dialog's no-action default. The mid-session [Fable usage-credits consent prompt](/docs/en/model-config#fable-and-usage-credits) follows the same deadline but isn't forwarded: Claude Code shows it only in the terminal where the session runs, and if nobody has answered there by the deadline, it ends the turn without sending the request. Your model selection is unchanged, and Claude Code asks again on your next message. Set [`dialogExpiry`](/docs/en/settings-reference#dialogexpiry) to adjust or disable the deadline. Requires Claude Code v2.1.224 or later. Claude Code applies the same deadline to the approval dialog for a held cross-session message. [The held-message expiry rules](/docs/en/cross-session-messaging#control-inbound-messages) cover the cases where Claude Code keeps the dialog open past it.
* **Some commands are local-only**: commands that only run in the terminal interface, such as `/plugin` or `/resume`, work only from the local CLI, whether or not you pass an argument. The following work from mobile and web:
  * Text-output commands: `/compact`, `/clear`, `/context`, `/usage`, `/exit`, `/usage-credits` (prints the billing URL instead of opening a browser), `/recap`, `/reload-plugins`
  * `/model`, `/effort`, `/fast`, `/color`, and `/rename`: pass the value as an argument, for example `/model sonnet` or `/effort high`. From mobile and web, `/model` and `/effort` take the argument in place of the terminal picker or slider.
  * `/mcp`, from v2.1.166: from the mobile app, returns a text summary of server status instead of opening the picker. On the web, `/mcp` on its own opens a directory of [claude.ai connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) instead of returning the summary. The `reconnect`, `enable`, and `disable` [subcommands](/docs/en/commands#all-commands) work from both. Unlike the local CLI, `/mcp reconnect` without a server name reconnects every server that has failed or needs authentication.
  * `/config`, from v2.1.181: from the mobile app, pass `key=value` to set a setting, or run it with no argument to list the keys you can set. On the web, `/config` opens the Claude Code section of your settings instead, and ignores text after the command.
  * On Team and Enterprise, `/usage-credits` from mobile or web doesn't send a [usage-credits request to your admin](/docs/en/costs#add-usage-credits-to-your-subscription). Sending requires a confirmation that appears only in the interactive CLI, so the command tells you to run it there instead. Before v2.1.211, the text form sent the request without confirmation.
  * `/autocompact`, from v2.1.221: pass the window size as an argument, for example `/autocompact 500k`. With no argument, it prints the current window size as text instead of opening the dialog the command shows in a terminal session.

## Troubleshooting

### "Remote Control requires a claude.ai subscription"

You're not authenticated with a claude.ai account. Run `claude auth login` and choose the claude.ai option. If `ANTHROPIC_API_KEY` is set in your environment, unset it first.

Before v2.1.206, running `/remote-control` while signed out reported `Unknown command: /remote-control` instead of this message.

### "Remote Control requires a full-scope login token"

You're authenticated with a long-lived token from `claude setup-token` or the `CLAUDE_CODE_OAUTH_TOKEN` environment variable. These tokens can only make model requests, so they can't establish Remote Control sessions. Run `claude auth login` to authenticate with a full-scope session token instead.

### "Unable to determine your organization for Remote Control eligibility"

Your cached account information is stale or incomplete. Run `claude auth login` to refresh it.

### "Remote Control isn't enabled for this account"

Claude Code checked Remote Control availability for the account you're signed in with and the check came back off. The usual cause is cached entitlements that are out of date after a plan change. Run `claude auth logout` then `claude auth login` to refresh them, and update Claude Code if you're on an old version.

Run `claude doctor` to see which individual eligibility check failed. Environment-variable conflicts, unreachable checks, and your organization's Remote Control setting each produce their own message, so this error means the account-level check itself.

Before v2.1.239, this message read "Remote Control is not yet enabled for your account". Before v2.1.154, a variable that disables feature-flag evaluation, such as `DISABLE_TELEMETRY` or `DO_NOT_TRACK`, also produced this message; the "Remote Control requires feature-flag evaluation" entry below covers that configuration.

### "Couldn't verify Remote Control eligibility"

Claude Code could not reach the feature-flag service to check whether Remote Control is enabled for your account, typically because you are offline or a proxy is blocking the request. Retry once you have network access, or run `claude doctor` for details. The related message "Couldn't verify your organization's Remote Control policy" has the same cause and the same fix. Both messages were added in v2.1.178.

### "Remote Control requires feature-flag evaluation"

One of these variables is set: [`DISABLE_TELEMETRY`, `DO_NOT_TRACK`, `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`, or `DISABLE_GROWTHBOOK`](/docs/en/env-vars). Each of them disables the feature-flag evaluation that Remote Control availability depends on, and the full message names the variable Claude Code found. Unset that variable wherever it's set, in your shell environment or in the `env` block of a [`settings.json` file](/docs/en/settings-reference#all-settings). On versions before 2.1.154, the same configuration produces "Remote Control is not yet enabled for your account" instead.

### "Remote Control is only available when using Claude via api.anthropic.com"

The session isn't talking to the Anthropic API directly, so there is no claude.ai backend to pair with. This happens on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. It also happens when [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) points at a host other than `api.anthropic.com`, such as an [LLM gateway](/docs/en/llm-gateway) or proxy, even if you sign in with claude.ai. Before v2.1.196, Claude Code didn't show this message for a custom `ANTHROPIC_BASE_URL`. See the [error reference](/docs/en/errors#remote-control-requires-the-anthropic-api) for the full cause list.

The message names what routed the session away from the Anthropic API, such as `CLAUDE_CODE_USE_BEDROCK` or a custom `ANTHROPIC_BASE_URL`. If you have an eligible claude.ai login, unset the named variable, remove it from the `env` key in [settings](/docs/en/settings) if you set it there, and restart the session. Before v2.1.219, the message was only the sentence in this section's header, so on older versions check your environment yourself for provider variables such as `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_VERTEX`, and for `ANTHROPIC_BASE_URL`.

### "Remote Control is disabled by your organization's policy"

A policy blocks Remote Control. Check these causes in order:

* **The error mentions `disableRemoteControl`**: your IT administrator has disabled Remote Control on this device through [managed settings](/docs/en/managed-settings), independent of the organization-wide toggle and of how you're signed in.
* **Your claude.ai plan is Pro or Max**: Claude Code is still signed in under a Team or Enterprise organization from an earlier login, so it checks that organization's Remote Control policy. Run `/status` to see which plan and organization your sign-in uses. Run `claude auth logout` then `claude auth login` to sign in again under your current plan.
* **Otherwise, an Owner hasn't enabled it for your organization**: this form appears when you're signed in with an eligible claude.ai account but Remote Control is off, the default on Team and Enterprise plans. An Owner can enable it at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) by turning on the **Remote Control** toggle. This toggle is a server-side organization setting.

### "Remote Control isn't available for your organization due to its compliance policy"

Your organization has a data retention or compliance configuration that is incompatible with Remote Control; the parenthetical at the end of the message names it. In this state the admin panel's Remote Control toggle is grayed out, so an Owner can't change it there. Contact Anthropic support to discuss options.

### "Remote credentials fetch failed"

Claude Code could not obtain a short-lived credential from the Anthropic API to establish the connection. Re-run with `--verbose` to see the full error:

```bash theme={null}
claude remote-control --verbose
```

Common causes:

* Not signed in: run `claude` and use `/login` to authenticate with your claude.ai account. API key authentication is not supported for Remote Control.
* Network or proxy issue: a firewall or proxy may be blocking the outbound HTTPS request. Remote Control requires access to the Anthropic API on port 443.
* Session creation failed: if you also see `Session creation failed — see debug log`, the failure happened earlier in setup. Check that your subscription is active.

A stale login token doesn't cause this error. When the Anthropic API rejects the saved token, for example because another Claude Code process already refreshed it, Claude Code refreshes the token and retries on its own. Before v2.1.224, a stale token failed Remote Control startup with this message, so sessions set to [connect automatically](#enable-remote-control-for-all-sessions) could fail intermittently at launch.

### "Couldn't reconnect to your Remote Control session"

When you resume a conversation with `claude --resume` or `claude --continue`, Claude Code reconnects to the Remote Control session recorded in that conversation. This message means the reconnection failed for a reason that may be temporary, such as a network interruption or a server error, so Claude Code can't confirm whether the remote session still exists.

Run `/remote-control` to retry the connection, or start a new session with `claude --remote-control` to create a new Remote Control session. Your local session keeps running without Remote Control in the meantime.

<span id="resume-outcomes" />When you resume, you can also get one of these outcomes instead of this message:

* **The server reports the recorded session gone, or the reconnection record names a different account**: Claude Code goes by what the conversation's reconnection record says:
  * **The record names your signed-in account**: Claude Code starts a replacement session with an auto-generated name and leaves the conversation's earlier messages out of it. You get this after you delete the session from claude.ai or the Claude app, for example.
  * **The record names a different account**: Claude Code starts a new session without the conversation's earlier messages and without showing a message, whether or not the recorded session still exists.
  * **The record doesn't say which account owned the session, or Claude Code can't read your saved sign-in**: Claude Code shows [`Previous session is unavailable — run /remote-control to start a new one`](#previous-session-is-unavailable) instead of this message, starts nothing, and removes the record from the conversation.
* **You turned Remote Control off before resuming**: unless the app hosting Claude Code had told it that the app owns the claude.ai session, Claude Code removed the reconnection record when you turned Remote Control off from the CLI's [status panel](#check-connection-status), the VS Code extension, or a host built on the [Agent SDK](/docs/en/agent-sdk/overview), so it doesn't reconnect. When an owning app turned it off, Claude Code kept the record and reconnects.
* **Another Claude Code on this machine still has the session**: you see a notice that starts with `Remote Control not started here`, and Claude Code [leaves Remote Control off in the resumed session](#resume-sessions-after-stopping-the-server). Run `/remote-control` there to move it.

<span id="reconnect-history" />Before v2.1.232, Claude Code responded differently when the server reported the recorded session gone. From v2.1.227 through v2.1.231, Claude Code refused to start a replacement even when the record matched your account. Through v2.1.226, Claude Code started a replacement whether or not the record matched your account, and in v2.1.224 through v2.1.226 created it under the account signed in on that machine, never another account's, without uploading the conversation's earlier messages to it. Before v2.1.200, Claude Code created a new session after any reconnection failure.

<h3 id="previous-session-is-unavailable">
  "Previous session is unavailable — run /remote-control to start a new one"
</h3>

Claude Code couldn't bring back the previous Remote Control session and stopped instead of starting a new one on its own. You can see this message after you resume a conversation with `claude --resume` or `claude --continue`, or after Claude Code [reconnects on its own following a disconnect](/docs/en/errors#remote-control-couldnt-refresh-your-login).

Run `/remote-control` to start a new Remote Control session under the current login; your local session keeps running without Remote Control in the meantime. The related message `Remote Control could not verify the signed-in account — run /remote-control to reconnect` has the same fix; Claude Code shows it when the signed-in account changed or couldn't be read between validating it and reconnecting. If you run `/remote-control` after `Previous session is unavailable` without restarting Claude Code first, Claude Code leaves the conversation's earlier messages out of the new session.

On resume, Claude Code [starts a new session in its place](#resume-outcomes) only if the conversation's reconnection record names the account that owned the session, because the server reports a session you deleted and a session owned by another account the same way. Claude Code before v2.1.227 didn't record that account, and Claude Code can't check the record when it can't read your saved sign-in. Claude Code before v2.1.232 showed `Remote Control could not resume the previous session under the current login — run /remote-control to start fresh` instead, in [a different set of cases](#reconnect-history).

### "Remote Control got an unexpected server response"

The Remote Control server accepted a request but replied in a form this version of Claude Code couldn't read, while creating the remote session or fetching its credentials. Retrying on the same version fails the same way. Run `claude update`, then run `/remote-control` to reconnect. This message was added in v2.1.225.

### "Your organization requires Trusted Devices for Remote Control, but this device is not enrolled"

Your organization has [Trusted Devices](#trusted-devices) enabled and this machine has not enrolled yet. Run `/login` in Claude Code. Enrollment happens as part of sign-in, and there is no separate enrollment command.

### "session expired for trusted-device check"

Your sign-in is more than 18 hours old. Run `/login` in Claude Code, or confirm with Face ID, Touch ID, Windows Hello, or a passkey when claude.ai or the mobile app prompts you. See [Trusted Devices](#trusted-devices).

## Choose the right approach

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                          | Trigger                                                                                        | Claude runs on                                                                               | Setup                                                                                                                                | Best for                                                      |
| :------------------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/docs/en/desktop#sessions-from-dispatch)           | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                       | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/docs/en/remote-control)                     | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/docs/en/channels)                                 | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                           | [Install a channel plugin](/docs/en/channels#quickstart) or [build your own](/docs/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/docs/en/slack)                                       | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                              | [Install the Slack app](/docs/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/docs/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Self-hosted environments](/docs/en/self-hosted-environments) | Start a [cloud session](/docs/en/claude-code-on-the-web) and pick your organization's environment   | Your organization's infrastructure                                                           | [Deploy runners](/docs/en/self-hosted-environments-quickstart), on Team and Enterprise plans                                              | Cloud sessions that must run inside your network              |
| [Scheduled tasks](/docs/en/scheduled-tasks)                   | Set a schedule                                                                                 | [CLI](/docs/en/scheduled-tasks), [Desktop](/docs/en/desktop-scheduled-tasks), or [cloud](/docs/en/routines) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## Related resources

* [Claude Code on the web](/docs/en/claude-code-on-the-web): run sessions in the cloud instead of your machine, configured through [cloud environments](/docs/en/cloud-environments)
* [Cross-session messaging](/docs/en/cross-session-messaging): let Claude message your sessions on other machines or on [Claude Code on the web](/docs/en/claude-code-on-the-web)
* [Channels](/docs/en/channels): forward Telegram, Discord, or iMessage into a session so Claude reacts to messages while you're away
* [Dispatch](/docs/en/desktop#sessions-from-dispatch): message a task from your phone and it can spawn a Desktop session to handle it
* [Authentication](/docs/en/authentication): set up `/login` and manage credentials for claude.ai
* [CLI reference](/docs/en/cli-reference): full list of flags and commands including `claude remote-control`
* [Security](/docs/en/security): how Remote Control sessions fit into the Claude Code security model
* [Data usage](/docs/en/data-usage): what data flows through the Anthropic API during local and remote sessions
