> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continue local sessions from any device with Remote Control

> Continue a local Claude Code session from your phone, tablet, or any browser using Remote Control. Works with claude.ai/code and the Claude mobile app.

<Note>
  Remote Control is available as a research preview on Pro and Max plans. It is not available on Team or Enterprise plans.
</Note>

Remote Control connects [claude.ai/code](https://claude.ai/code) or the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) to a Claude Code session running on your machine. Start a task at your desk, then pick it up from your phone on the couch or a browser on another computer.

When you start a Remote Control session on your machine, Claude keeps running locally the entire time, so nothing moves to the cloud. With Remote Control you can:

* **Use your full local environment remotely**: your filesystem, [MCP servers](/en/mcp), tools, and project configuration all stay available
* **Work from both surfaces at once**: the conversation stays in sync across all connected devices, so you can send messages from your terminal, browser, and phone interchangeably
* **Survive interruptions**: if your laptop sleeps or your network drops, the session reconnects automatically when your machine comes back online

Unlike [Claude Code on the web](/en/claude-code-on-the-web), which runs on cloud infrastructure, Remote Control sessions run directly on your machine and interact with your local filesystem. The web and mobile interfaces are just a window into that local session.

This page covers setup, how to start and connect to sessions, and how Remote Control compares to Claude Code on the web.

## Requirements

Before using Remote Control, confirm that your environment meets these conditions:

* **Subscription**: requires a Pro or Max plan. API keys are not supported.
* **Authentication**: run `claude` and use `/login` to sign in through claude.ai if you haven't already.
* **Workspace trust**: run `claude` in your project directory at least once to accept the workspace trust dialog.

## Start a Remote Control session

You can start a new session directly in Remote Control, or connect a session that's already running.

<Tabs>
  <Tab title="New session">
    Navigate to your project directory and run:

    ```bash  theme={null}
    claude remote-control
    ```

    The process stays running in your terminal, waiting for remote connections. It displays a session URL you can use to [connect from another device](#connect-from-another-device), and you can press spacebar to show a QR code for quick access from your phone. While a remote session is active, the terminal shows connection status and tool activity.

    This command supports the following flags:

    * **`--verbose`**: show detailed connection and session logs
    * **`--sandbox`** / **`--no-sandbox`**: enable or disable [sandboxing](/en/sandboxing) for filesystem and network isolation during the session. Sandboxing is off by default.
  </Tab>

  <Tab title="From an existing session">
    If you're already in a Claude Code session and want to continue it remotely, use the `/remote-control` (or `/rc`) command:

    ```
    /remote-control
    ```

    This starts a Remote Control session that carries over your current conversation history and displays a session URL and QR code you can use to [connect from another device](#connect-from-another-device). The `--verbose`, `--sandbox`, and `--no-sandbox` flags are not available with this command.

    <Tip>
      Use `/rename` before running `/remote-control` to give the session a descriptive name. This makes it easier to find in the session list across devices.
    </Tip>
  </Tab>
</Tabs>

### Connect from another device

Once a Remote Control session is active, you have a few ways to connect from another device:

* **Open the session URL** in any browser to go directly to the session on [claude.ai/code](https://claude.ai/code). Both `claude remote-control` and `/remote-control` display this URL in the terminal.
* **Scan the QR code** shown alongside the session URL to open it directly in the Claude app. With `claude remote-control`, press spacebar to toggle the QR code display.
* **Open [claude.ai/code](https://claude.ai/code) or the Claude app** and find the session by name in the session list. Remote Control sessions show a computer icon with a green status dot when online.

The remote session takes its name from your last message, your `/rename` value, or "Remote Control session" if there's no conversation history. If the environment already has an active session, you'll be asked whether to continue it or start a new one.

If you don't have the Claude app yet, use the `/mobile` command inside Claude Code to display a download QR code for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Enable Remote Control for all sessions

By default, Remote Control only activates when you explicitly run `claude remote-control` or `/remote-control`. To enable it automatically for every session, run `/config` inside Claude Code and set **Enable Remote Control for all sessions** to `true`. Set it back to `false` to disable.

Each Claude Code instance supports one remote session at a time. If you run multiple instances, each one gets its own environment and session.

## Connection and security

Your local Claude Code session makes outbound HTTPS requests only and never opens inbound ports on your machine. When you start Remote Control, it registers with the Anthropic API and polls for work. When you connect from another device, the server routes messages between the web or mobile client and your local session over a streaming connection.

All traffic travels through the Anthropic API over TLS, the same transport security as any Claude Code session. The connection uses multiple short-lived credentials, each scoped to a single purpose and expiring independently.

## Remote Control vs Claude Code on the web

Remote Control and [Claude Code on the web](/en/claude-code-on-the-web) both use the claude.ai/code interface. The key difference is where the session runs: Remote Control executes on your machine, so your local MCP servers, tools, and project configuration stay available. Claude Code on the web executes in Anthropic-managed cloud infrastructure.

Use Remote Control when you're in the middle of local work and want to keep going from another device. Use Claude Code on the web when you want to kick off a task without any local setup, work on a repo you don't have cloned, or run multiple tasks in parallel.

## Limitations

* **One remote session at a time**: each Claude Code session supports one remote connection.
* **Terminal must stay open**: Remote Control runs as a local process. If you close the terminal or stop the `claude` process, the session ends. Run `claude remote-control` again to start a new one.
* **Extended network outage**: if your machine is awake but unable to reach the network for more than roughly 10 minutes, the session times out and the process exits. Run `claude remote-control` again to start a new session.

## Related resources

* [Claude Code on the web](/en/claude-code-on-the-web): run sessions in Anthropic-managed cloud environments instead of on your machine
* [Authentication](/en/authentication): set up `/login` and manage credentials for claude.ai
* [CLI reference](/en/cli-reference): full list of flags and commands including `claude remote-control`
* [Security](/en/security): how Remote Control sessions fit into the Claude Code security model
* [Data usage](/en/data-usage): what data flows through the Anthropic API during local and remote sessions
