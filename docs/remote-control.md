> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continue local sessions from any device with Remote Control

> Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.

<Note>
  Remote Control is in research preview and available on all plans. On Team and Enterprise, it is off by default until an Owner enables the Remote Control toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control connects [claude.ai/code](https://claude.ai/code) or the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) to a Claude Code session running on your machine. Start a task at your desk, then pick it up from your phone on the couch or a browser on another computer.

When you start a Remote Control session on your machine, Claude keeps running locally the entire time, so nothing moves to the cloud. With Remote Control you can:

* **Use your full local environment remotely**: your filesystem, [MCP servers](/en/mcp), tools, and project configuration all stay available, and typing `@` autocompletes file paths from your local project
* **Work from both surfaces at once**: the conversation stays in sync across all connected devices, so you can send messages from your terminal, browser, and phone interchangeably
* **Survive interruptions**: if your laptop sleeps or your network drops, the session reconnects automatically when your machine comes back online

Unlike [Claude Code on the web](/en/claude-code-on-the-web), which runs on cloud infrastructure, Remote Control sessions run directly on your machine and interact with your local filesystem. The web and mobile interfaces are just a window into that local session.

<Note>
  Remote Control requires Claude Code v2.1.51 or later. Check your version with `claude --version`.
</Note>

This page covers setup, how to start and connect to sessions, and how Remote Control compares to Claude Code on the web.

## Requirements

Before using Remote Control, confirm that your environment meets these conditions:

* **Subscription**: available on Pro, Max, Team, and Enterprise plans. API keys are not supported. On Team and Enterprise, an Owner must first enable the Remote Control toggle in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code).
* **Authentication**: run `claude` and use `/login` to sign in through claude.ai if you haven't already.
* **API endpoint**: not available on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. {/* min-version: 2.1.196 */}As of v2.1.196, Remote Control is also disabled when [`ANTHROPIC_BASE_URL`](/en/env-vars) points at a host other than `api.anthropic.com`, such as an [LLM gateway](/en/llm-gateway) or proxy. Unset the variable to use Remote Control.
* **Workspace trust**: run `claude` in your project directory at least once to accept the workspace trust dialog.

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
    | `-c`, `--continue`                              | {/* min-version: 2.1.200 */}Resume the most recent Remote Control session started from this directory instead of creating a new one. Can't be combined with `--session-id`, `--spawn`, `--capacity`, or `--create-session-in-dir`. Requires Claude Code v2.1.200 or later; earlier versions reject the flag as an unknown argument.                                                                                                                                                |
    | `--session-id <id>`                             | {/* min-version: 2.1.200 */}Resume a specific Remote Control session by its ID. Can't be combined with `--continue`, `--spawn`, `--capacity`, or `--create-session-in-dir`. Requires Claude Code v2.1.200 or later; earlier versions reject the flag as an unknown argument.                                                                                                                                                                                                       |
    | `--spawn <mode>`                                | How the server creates sessions.<br />• `same-dir` (default): all sessions share the current working directory, so they can conflict if editing the same files.<br />• `worktree`: each on-demand session gets its own [git worktree](/en/worktrees). Requires a git repository.<br />• `session`: single-session mode. Serves exactly one session and rejects additional connections. Set at startup only.<br />Press `w` at runtime to toggle between `same-dir` and `worktree`. |
    | `--capacity <N>`                                | Maximum number of concurrent sessions. Default is 32. Cannot be used with `--spawn=session`.                                                                                                                                                                                                                                                                                                                                                                                       |
    | `--[no-]create-session-in-dir`                  | Pre-create one session in the current directory when the server starts, so you have somewhere to type immediately. In `worktree` mode this session stays in the current directory while on-demand sessions get isolated worktrees. On by default; pass `--no-create-session-in-dir` to start with none.                                                                                                                                                                            |
    | `--verbose`                                     | Show detailed connection and session logs.                                                                                                                                                                                                                                                                                                                                                                                                                                         |
    | `--sandbox` / `--no-sandbox`                    | Enable or disable [sandboxing](/en/sandboxing) for filesystem and network isolation. Off by default.                                                                                                                                                                                                                                                                                                                                                                               |
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
    In the [Claude Code VS Code extension](/en/vs-code), type `/remote-control` or `/rc` in the prompt box, or open the command menu with `/` and select it. Requires Claude Code v2.1.79 or later.

    ```text theme={null}
    /remote-control
    ```

    A banner appears above the prompt box showing connection status. Once connected, click **Open in browser** in the banner to go directly to the session, or find it in the session list at [claude.ai/code](https://claude.ai/code). The session URL is also posted in the conversation.

    To disconnect, click the close icon on the banner or run `/remote-control` again.

    Unlike the CLI, the VS Code command does not accept a name argument or display a QR code. The session title is derived from your conversation history or first prompt.
  </Tab>
</Tabs>

### Check connection status

In an interactive terminal session, a `/rc active` indicator sits in the footer below the input box while the connection is up, and is hidden if the terminal is too narrow to fit it. The indicator text is a link to the session on claude.ai. Select it with the down arrow key and press Enter, or run `/remote-control` again, to open a status panel with the session URL and a QR code you can use to [connect from another device](#connect-from-another-device).

If the connection fails, a notification appears with the failure reason and the indicator disappears from the footer. Run `/remote-control` again to retry.

### Connect from another device

Once a Remote Control session is active, you have a few ways to connect from another device:

* **Open the session URL** in any browser to go directly to the session on [claude.ai/code](https://claude.ai/code).
* **Scan the QR code** shown alongside the session URL to open it directly in the Claude app. With `claude remote-control`, press spacebar to toggle the QR code display.
* **Open [claude.ai/code](https://claude.ai/code) or the Claude app** and find the session by name in the session list. In the Claude mobile app, tap **Code** in the navigation to reach the session list. Remote Control sessions show a computer icon with a green status dot when online.

The remote session title is chosen in this order:

1. The name you passed to `--name`, `--remote-control`, or `/remote-control`
2. The title you set with `/rename`
3. The last meaningful message in existing conversation history
4. An auto-generated name like `myhost-graceful-unicorn`, where `myhost` is your machine's hostname or the prefix you set with `--remote-control-session-name-prefix`

If you didn't set an explicit name, the title updates to reflect your prompt once you send one. {/* min-version: 2.1.176 */}As of Claude Code v2.1.176, auto-generated titles match the language of your conversation, or the [`language`](/en/settings#available-settings) setting if one is configured. Renaming a session from claude.ai or the Claude app also updates the local title shown in `claude --resume`.

If the environment already has an active session, you'll be asked whether to continue it or start a new one.

If you don't have the Claude app yet, use the `/mobile` command inside Claude Code to display a download QR code for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Enable Remote Control for all sessions

Remote Control only activates when you explicitly run `claude remote-control`, `claude --remote-control`, or `/remote-control`, unless auto-connect is turned on. To enable it automatically for every interactive session, run `/config` inside Claude Code and set **Enable Remote Control for all sessions** to `true`. Set it to `false` to never auto-connect, or leave it unset to follow your organization's default. In the Desktop app, you can also toggle this from **Settings → Claude Code → Enable remote control by default**.

With this setting on, each interactive Claude Code process registers one remote session. If you run multiple instances, each one gets its own environment and session. To run multiple concurrent sessions from a single process, use [server mode](#start-a-remote-control-session) instead.

## Connection and security

Your local Claude Code session makes outbound HTTPS requests only and never opens inbound ports on your machine. When you start Remote Control, it registers with the Anthropic API and polls for work. When you connect from another device, the server routes messages between the web or mobile client and your local session over a streaming connection.

All traffic travels through the Anthropic API over TLS, the same transport security as any Claude Code session. The connection uses multiple short-lived credentials, each scoped to a single purpose and expiring independently.

## Trusted Devices

<Note>
  Trusted Devices is currently in beta. Features and functionality may evolve as the experience is refined.

  Trusted Devices is available on Team and Enterprise plans. It is off by default until an admin enables it.
</Note>

Trusted Devices is an organization-wide setting that requires members to verify their device before they can view or steer Remote Control sessions from claude.ai, the Claude mobile apps, or Claude Desktop. It ties Remote Control access to a known device and a recent authentication, not just a signed-in account.

When the setting is on, interacting with a Remote Control session requires both of the following:

* **An enrolled device**: each browser, phone, or desktop app a member uses for Remote Control enrolls its own credential. Enrollment is only offered shortly after a full sign-in, so a device joins the trusted list as part of a real authentication rather than silently in the background.
* **A recent sign-in**: the member's sign-in must be no more than 18 hours old. Instead of signing in again each day, members confirm presence with Face ID, Touch ID, Windows Hello, or a passkey. This biometric step-up refreshes the session immediately.

Biometric checks run on the device through the operating system or browser, the same mechanism as passkey sign-in. Anthropic never receives or stores fingerprints, face data, or any other biometric information. Only the device's public key and basic metadata such as display name, platform, and enrollment time are stored.

The setting applies only to Remote Control. Regular Claude chat, Claude Code in the terminal, and API usage are unaffected.

### Enable Trusted Devices for your organization

Admins enable the setting from the Claude Code admin console.

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

Remote Control and [Claude Code on the web](/en/claude-code-on-the-web) both use the claude.ai/code interface. The key difference is where the session runs: Remote Control executes on your machine, so your local MCP servers, tools, and project configuration stay available. Claude Code on the web executes in Anthropic-managed cloud infrastructure.

Use Remote Control when you're in the middle of local work and want to keep going from another device. Use Claude Code on the web when you want to kick off a task without any local setup, work on a repo you don't have cloned, or run multiple tasks in parallel.

## Mobile push notifications

When Remote Control is active, Claude can send push notifications to your phone.

Claude decides when to push. It typically sends one when a long-running task finishes or when it needs a decision from you to continue. You can also request a push in your prompt, for example `notify me when the tests finish`. Beyond the two on/off toggles below, there is no per-event configuration.

<Note>
  Mobile push notifications require Claude Code v2.1.110 or later.
</Note>

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

Claude Code skips mobile push notifications while you are typing in or focused on the connected terminal. {/* min-version: 2.1.181 */}As of v2.1.181, you can set [`CLAUDE_CLIENT_PRESENCE_FILE`](/en/env-vars) to a marker file path to extend this to any time you are at the machine, even in another window: notifications are skipped while the file exists. Configure a screen-lock listener or similar tool to create the file when your screen unlocks and delete it when your screen locks.

## Limitations

* **One remote session per interactive process**: outside of server mode, each Claude Code instance supports one remote session at a time. Use [server mode](#start-a-remote-control-session) to run multiple concurrent sessions from a single process.
* **Local process must keep running**: Remote Control runs as a local process. If you close the terminal, quit VS Code, or otherwise stop the `claude` process, the session ends.
* **Extended network outage**: if your machine is awake but unable to reach the network for more than roughly 10 minutes, the session times out and the process exits. Run `claude remote-control` again to start a new session.
* **Ultraplan disconnects Remote Control**: starting an [ultraplan](/en/ultraplan) session disconnects any active Remote Control session because both features occupy the claude.ai/code interface and only one can be connected at a time.
* **Some commands are local-only**: commands that open an interactive picker in the terminal, such as `/plugin` or `/resume`, work only from the local CLI. The following work from mobile and web:
  * Text-output commands: `/compact`, `/clear`, `/context`, `/usage`, `/exit`, `/usage-credits`, `/recap`, `/reload-plugins`
  * {/* min-version: 2.1.166 */}`/mcp`, from v2.1.166: returns a text summary of server status instead of opening the picker, and accepts the `reconnect`, `enable`, and `disable` [subcommands](/en/commands#all-commands). Unlike the local CLI, `/mcp reconnect` without a server name reconnects every server that has failed or needs authentication.
  * {/* min-version: 2.1.181 */}`/config`, from v2.1.181: pass `key=value` to set a setting, or run it with no argument to list the keys you can set.

## Troubleshooting

### "Remote Control requires a claude.ai subscription"

You're not authenticated with a claude.ai account. Run `claude auth login` and choose the claude.ai option. If `ANTHROPIC_API_KEY` is set in your environment, unset it first.

### "Remote Control requires a full-scope login token"

You're authenticated with a long-lived token from `claude setup-token` or the `CLAUDE_CODE_OAUTH_TOKEN` environment variable. These tokens are limited to inference-only and cannot establish Remote Control sessions. Run `claude auth login` to authenticate with a full-scope session token instead.

### "Unable to determine your organization for Remote Control eligibility"

Your cached account information is stale or incomplete. Run `claude auth login` to refresh it.

### "Remote Control is not yet enabled for your account"

The Remote Control rollout has not reached your account, or your cached entitlements are out of date. If you recently changed plans, run `claude auth logout` then `claude auth login` to refresh them. Run `claude doctor` to see which individual eligibility check failed. Environment-variable conflicts, unreachable checks, and organization policy each produce their own message, so this error means the rollout gate itself.

### "Couldn't verify Remote Control eligibility"

Claude Code could not reach the feature-flag service to check whether Remote Control is enabled for your account, typically because you are offline or a proxy is blocking the request. Retry once you have network access, or run `claude doctor` for details. The related message "Couldn't verify your organization's Remote Control policy" has the same cause and the same fix. Both messages were added in v2.1.178.

### "Remote Control is only available when using Claude via api.anthropic.com"

The session isn't talking to the Anthropic API directly, so there is no claude.ai backend to pair with. This happens on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. {/* min-version: 2.1.196 */}As of v2.1.196 it also happens when [`ANTHROPIC_BASE_URL`](/en/env-vars) points at a host other than `api.anthropic.com`, such as an [LLM gateway](/en/llm-gateway) or proxy, even if you sign in with claude.ai. Unset `ANTHROPIC_BASE_URL` and restart the session to use Remote Control.

### "Remote Control is disabled by your organization's policy"

This error has four distinct causes. Run `/status` first to see which login method and subscription you're using.

* **You're authenticated with an API key or Console account**: Remote Control requires claude.ai OAuth. Run `/login` and choose the claude.ai option. If `ANTHROPIC_API_KEY` is set in your environment, unset it.
* **An Owner hasn't enabled it for your organization**: Remote Control is off by default on Team and Enterprise plans. An Owner can enable it at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) by turning on the **Remote Control** toggle. This toggle is a server-side organization setting.
* **The admin toggle is grayed out**: your organization has a data retention or compliance configuration that is incompatible with Remote Control. This cannot be changed from the admin panel. Contact Anthropic support to discuss options.
* **The error mentions `disableRemoteControl`**: your IT administrator has disabled Remote Control on this device through [managed settings](/en/settings#settings-files), independent of the organization-wide toggle.

### "Remote credentials fetch failed"

Claude Code could not obtain a short-lived credential from the Anthropic API to establish the connection. Re-run with `--verbose` to see the full error:

```bash theme={null}
claude remote-control --verbose
```

Common causes:

* Not signed in: run `claude` and use `/login` to authenticate with your claude.ai account. API key authentication is not supported for Remote Control.
* Network or proxy issue: a firewall or proxy may be blocking the outbound HTTPS request. Remote Control requires access to the Anthropic API on port 443.
* Session creation failed: if you also see `Session creation failed — see debug log`, the failure happened earlier in setup. Check that your subscription is active.

### "Couldn't reconnect to your Remote Control session"

When you resume a conversation with `claude --resume` or `claude --continue`, Claude Code reconnects to the Remote Control session recorded in that conversation. This message means the reconnection failed for a reason that may be temporary, such as a network interruption or a server error, so Claude Code can't confirm whether the remote session still exists. When the server confirms the previous session no longer exists, Claude Code creates a new Remote Control session without showing this message.

Your local session keeps running without Remote Control. Run `/remote-control` to retry the connection, or start Claude Code without `--resume` to create a new Remote Control session.

{/* min-version: 2.1.200 */}Before v2.1.200, a reconnection failure created a new Remote Control session instead of showing this message, which left extra sessions in the session list at claude.ai/code.

### "Your organization requires Trusted Devices for Remote Control, but this device is not enrolled"

Your organization has [Trusted Devices](#trusted-devices) enabled and this machine has not enrolled yet. Run `/login` in Claude Code. Enrollment happens as part of sign-in, and there is no separate enrollment command.

### "session expired for trusted-device check"

Your sign-in is more than 18 hours old. Run `/login` in Claude Code, or confirm with Face ID, Touch ID, Windows Hello, or a passkey when claude.ai or the mobile app prompts you. See [Trusted Devices](#trusted-devices).

## Choose the right approach

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                               | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                       | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                           | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                              | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop-scheduled-tasks), or [cloud](/en/routines) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## Related resources

* [Claude Code on the web](/en/claude-code-on-the-web): run sessions in Anthropic-managed cloud environments instead of on your machine
* [Ultraplan](/en/ultraplan): launch a cloud planning session from your terminal and review the plan in your browser
* [Channels](/en/channels): forward Telegram, Discord, or iMessage into a session so Claude reacts to messages while you're away
* [Dispatch](/en/desktop#sessions-from-dispatch): message a task from your phone and it can spawn a Desktop session to handle it
* [Authentication](/en/authentication): set up `/login` and manage credentials for claude.ai
* [CLI reference](/en/cli-reference): full list of flags and commands including `claude remote-control`
* [Security](/en/security): how Remote Control sessions fit into the Claude Code security model
* [Data usage](/en/data-usage): what data flows through the Anthropic API during local and remote sessions
