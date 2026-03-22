> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Push events into a running session with channels

> Use channels to push messages, alerts, and webhooks into your Claude Code session from an MCP server. Forward CI results, chat messages, and monitoring events so Claude can react while you're away.

<Note>
  Channels are in [research preview](#research-preview) and require Claude Code v2.1.80 or later. They require claude.ai login. Console and API key authentication is not supported. Team and Enterprise organizations must [explicitly enable them](#enterprise-controls).
</Note>

A channel is an MCP server that pushes events into your running Claude Code session, so Claude can react to things that happen while you're not at the terminal. Channels can be two-way: Claude reads the event and replies back through the same channel, like a chat bridge. Events only arrive while the session is open, so for an always-on setup you run Claude in a background process or persistent terminal.

Unlike integrations that spawn a fresh cloud session or wait to be polled, the event arrives in the session you already have open: see [how channels compare](#how-channels-compare).

You install a channel as a plugin and configure it with your own credentials. Telegram and Discord are included in the research preview.

When Claude replies through a channel, you see the inbound message in your terminal but not the reply text. The terminal shows the tool call and a confirmation (like "sent"), and the actual reply appears on the other platform.

This page covers:

* [Supported channels](#supported-channels): Telegram and Discord setup
* [Install and run a channel](#quickstart) with fakechat, a localhost demo
* [Who can push messages](#security): sender allowlists and how you pair
* [Enable channels for your organization](#enterprise-controls) on Team and Enterprise
* [How channels compare](#how-channels-compare) to web sessions, Slack, MCP, and Remote Control

To build your own channel, see the [Channels reference](/en/channels-reference).

## Supported channels

Each supported channel is a plugin that requires [Bun](https://bun.sh). For a hands-on demo of the plugin flow before connecting a real platform, try the [fakechat quickstart](#quickstart).

<Tabs>
  <Tab title="Telegram">
    View the full [Telegram plugin source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram).

    <Steps>
      <Step title="Create a Telegram bot">
        Open [BotFather](https://t.me/BotFather) in Telegram and send `/newbot`. Give it a display name and a unique username ending in `bot`. Copy the token BotFather returns.
      </Step>

      <Step title="Install the plugin">
        In Claude Code, run:

        ```
        /plugin install telegram@claude-plugins-official
        ```

        If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you haven't added it before. Then retry the install.

        After installing, run `/reload-plugins` to activate the plugin's configure command.
      </Step>

      <Step title="Configure your token">
        Run the configure command with the token from BotFather:

        ```
        /telegram:configure <token>
        ```

        This saves it to `~/.claude/channels/telegram/.env`. You can also set `TELEGRAM_BOT_TOKEN` in your shell environment before launching Claude Code.
      </Step>

      <Step title="Restart with channels enabled">
        Exit Claude Code and restart with the channel flag. This starts the Telegram plugin, which begins polling for messages from your bot:

        ```bash  theme={null}
        claude --channels plugin:telegram@claude-plugins-official
        ```
      </Step>

      <Step title="Pair your account">
        Open Telegram and send any message to your bot. The bot replies with a pairing code.

        <Note>If your bot doesn't respond, make sure Claude Code is running with `--channels` from the previous step. The bot can only reply while the channel is active.</Note>

        Back in Claude Code, run:

        ```
        /telegram:access pair <code>
        ```

        Then lock down access so only your account can send messages:

        ```
        /telegram:access policy allowlist
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Discord">
    View the full [Discord plugin source](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord).

    <Steps>
      <Step title="Create a Discord bot">
        Go to the [Discord Developer Portal](https://discord.com/developers/applications), click **New Application**, and name it. In the **Bot** section, create a username, then click **Reset Token** and copy the token.
      </Step>

      <Step title="Enable Message Content Intent">
        In your bot's settings, scroll to **Privileged Gateway Intents** and enable **Message Content Intent**.
      </Step>

      <Step title="Invite the bot to your server">
        Go to **OAuth2 > URL Generator**. Select the `bot` scope and enable these permissions:

        * View Channels
        * Send Messages
        * Send Messages in Threads
        * Read Message History
        * Attach Files
        * Add Reactions

        Open the generated URL to add the bot to your server.
      </Step>

      <Step title="Install the plugin">
        In Claude Code, run:

        ```
        /plugin install discord@claude-plugins-official
        ```

        If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you haven't added it before. Then retry the install.

        After installing, run `/reload-plugins` to activate the plugin's configure command.
      </Step>

      <Step title="Configure your token">
        Run the configure command with the bot token you copied:

        ```
        /discord:configure <token>
        ```

        This saves it to `~/.claude/channels/discord/.env`. You can also set `DISCORD_BOT_TOKEN` in your shell environment before launching Claude Code.
      </Step>

      <Step title="Restart with channels enabled">
        Exit Claude Code and restart with the channel flag. This connects the Discord plugin so your bot can receive and respond to messages:

        ```bash  theme={null}
        claude --channels plugin:discord@claude-plugins-official
        ```
      </Step>

      <Step title="Pair your account">
        DM your bot on Discord. The bot replies with a pairing code.

        <Note>If your bot doesn't respond, make sure Claude Code is running with `--channels` from the previous step. The bot can only reply while the channel is active.</Note>

        Back in Claude Code, run:

        ```
        /discord:access pair <code>
        ```

        Then lock down access so only your account can send messages:

        ```
        /discord:access policy allowlist
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

You can also [build your own channel](/en/channels-reference) for systems that don't have a plugin yet.

## Quickstart

Fakechat is an officially supported demo channel that runs a chat UI on localhost, with nothing to authenticate and no external service to configure.

Once you install and enable fakechat, you can type in the browser and the message arrives in your Claude Code session. Claude replies, and the reply shows up back in the browser. After you've tested the fakechat interface, try out [Telegram](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/telegram) or [Discord](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/discord).

To try the fakechat demo, you'll need:

* Claude Code [installed and authenticated](/en/quickstart#step-1-install-claude-code) with a claude.ai account
* [Bun](https://bun.sh) installed. The pre-built channel plugins are Bun scripts. Check with `bun --version`; if that fails, [install Bun](https://bun.sh/docs/installation).
* **Team/Enterprise users**: your organization admin must [enable channels](#enterprise-controls) in managed settings

<Steps>
  <Step title="Install the fakechat channel plugin">
    Start a Claude Code session and run the install command:

    ```text  theme={null}
    /plugin install fakechat@claude-plugins-official
    ```

    If Claude Code reports that the plugin is not found in any marketplace, your marketplace is either missing or outdated. Run `/plugin marketplace update claude-plugins-official` to refresh it, or `/plugin marketplace add anthropics/claude-plugins-official` if you haven't added it before. Then retry the install.
  </Step>

  <Step title="Restart with the channel enabled">
    Exit Claude Code, then restart with `--channels` and pass the fakechat plugin you installed:

    ```bash  theme={null}
    claude --channels plugin:fakechat@claude-plugins-official
    ```

    The fakechat server starts automatically.

    <Tip>
      You can pass several plugins to `--channels`, space-separated.
    </Tip>
  </Step>

  <Step title="Push a message in">
    Open the fakechat UI at [http://localhost:8787](http://localhost:8787) and type a message:

    ```text  theme={null}
    hey, what's in my working directory?
    ```

    The message arrives in your Claude Code session as a `<channel source="fakechat">` event. Claude reads it, does the work, and calls fakechat's `reply` tool. The answer shows up in the chat UI.
  </Step>
</Steps>

If Claude hits a permission prompt while you're away from the terminal, the session pauses until you respond. Channel servers that declare the [permission relay capability](/en/channels-reference#relay-permission-prompts) can forward these prompts to you so you can approve or deny remotely. For unattended use, [`--dangerously-skip-permissions`](/en/permissions#permission-modes) bypasses prompts entirely, but only use it in environments you trust.

## Security

Every approved channel plugin maintains a sender allowlist: only IDs you've added can push messages, and everyone else is silently dropped.

Telegram and Discord bootstrap the list by pairing:

1. Find your bot in Telegram or Discord and send it any message
2. The bot replies with a pairing code
3. In your Claude Code session, approve the code when prompted
4. Your sender ID is added to the allowlist

On top of that, you control which servers are enabled each session with `--channels`, and on Team and Enterprise plans your organization controls availability with [`channelsEnabled`](#enterprise-controls).

Being in `.mcp.json` isn't enough to push messages: a server also has to be named in `--channels`.

The allowlist also gates [permission relay](/en/channels-reference#relay-permission-prompts) if the channel declares it. Anyone who can reply through the channel can approve or deny tool use in your session, so only allowlist senders you trust with that authority.

## Enterprise controls

Channels are controlled by the `channelsEnabled` setting in [managed settings](/en/settings).

| Plan type                  | Default behavior                                               |
| :------------------------- | :------------------------------------------------------------- |
| Pro / Max, no organization | Channels available; users opt in per session with `--channels` |
| Team / Enterprise          | Channels disabled until an admin explicitly enables them       |

### Enable channels for your organization

Admins can enable channels from [**claude.ai → Admin settings → Claude Code → Channels**](https://claude.ai/admin-settings/claude-code), or by setting `channelsEnabled` to `true` in managed settings.

Once enabled, users in your organization can use `--channels` to opt channel servers into individual sessions. If the setting is disabled or unset, the MCP server still connects and its tools work, but channel messages won't arrive. A startup warning tells the user to have an admin enable the setting.

## Research preview

Channels are a research preview feature. Availability is rolling out gradually, and the `--channels` flag syntax and protocol contract may change based on feedback.

During the preview, `--channels` only accepts plugins from an Anthropic-maintained allowlist. The channel plugins in [claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins) are the approved set. If you pass something that isn't, Claude Code starts normally but the channel doesn't register, and the startup notice tells you why.

To test a channel you're building, use `--dangerously-load-development-channels`. See [Test during the research preview](/en/channels-reference#test-during-the-research-preview) for information about testing custom channels that you build.

Report issues or feedback on the [Claude Code GitHub repository](https://github.com/anthropics/claude-code/issues).

## How channels compare

Several Claude Code features connect to systems outside the terminal, each suited to a different kind of work:

| Feature                                              | What it does                                                          | Good for                                                  |
| ---------------------------------------------------- | --------------------------------------------------------------------- | --------------------------------------------------------- |
| [Claude Code on the web](/en/claude-code-on-the-web) | Runs tasks in a fresh cloud sandbox, cloned from GitHub               | Delegating self-contained async work you check on later   |
| [Claude in Slack](/en/slack)                         | Spawns a web session from an `@Claude` mention in a channel or thread | Starting tasks directly from team conversation context    |
| Standard [MCP server](/en/mcp)                       | Claude queries it during a task; nothing is pushed to the session     | Giving Claude on-demand access to read or query a system  |
| [Remote Control](/en/remote-control)                 | You drive your local session from claude.ai or the Claude mobile app  | Steering an in-progress session while away from your desk |

Channels fill the gap in that list by pushing events from non-Claude sources into your already-running local session.

* **Chat bridge**: ask Claude something from your phone via Telegram or Discord, and the answer comes back in the same chat while the work runs on your machine against your real files.
* **[Webhook receiver](/en/channels-reference#example-build-a-webhook-receiver)**: a webhook from CI, your error tracker, a deploy pipeline, or other external service arrives where Claude already has your files open and remembers what you were debugging.

## Next steps

Once you have a channel running, explore these related features:

* [Build your own channel](/en/channels-reference) for systems that don't have plugins yet
* [Remote Control](/en/remote-control) to drive a local session from your phone instead of forwarding events into it
* [Scheduled tasks](/en/scheduled-tasks) to poll on a timer instead of reacting to pushed events
