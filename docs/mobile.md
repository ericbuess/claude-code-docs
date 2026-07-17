> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on mobile

> Start, monitor, and steer Claude Code tasks from your phone with the Claude app for iOS and Android.

The Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) is a client for Claude Code sessions rather than a place where code runs. From your phone you reach [cloud sessions](#start-and-monitor-cloud-sessions) on Anthropic-managed infrastructure, a session running on your own machine through [Remote Control](#continue-a-local-session-with-remote-control), or the Desktop app through [Dispatch](/en/desktop#sessions-from-dispatch).

<Note>
  Claude Code doesn't have a separate mobile app: cloud sessions and Remote Control both live in the **Code** tab in the Claude app, and Dispatch is a task you message in the app.
</Note>

## Get the app

<Steps>
  <Step title="Download the Claude app">
    Install the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) or [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude). On an iPad, install the same iOS app.

    <Tip>
      Run `/mobile` in a Claude Code session to display a download QR code you can scan. `/ios` and `/android` do the same thing.
    </Tip>
  </Step>

  <Step title="Sign in">
    Sign in with the same claude.ai account and organization you use for Claude Code. Cloud sessions and Remote Control require a claude.ai account, so they aren't reachable with an Anthropic Console API key or from a third-party provider such as Amazon Bedrock.
  </Step>

  <Step title="Open the Code tab">
    Tap **Code** in the app's navigation to reach your sessions, or open [claude.ai/code/new](https://claude.ai/code/new) on your phone to start a new Code session in the app. If you don't see the Code tab, your plan or organization may not include these features; see [availability by subscription plan](/en/feature-availability#availability-by-subscription-plan).
  </Step>
</Steps>

## Work from your phone

From the app you can start cloud sessions, drive a Claude Code session running on your computer, or message Dispatch a task. The app is the same for all three; they differ in where the work happens.

| Feature                                              | What you connect to                                 | When to use                                                                                                                                          |
| :--------------------------------------------------- | :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Claude Code on the web](/en/claude-code-on-the-web) | A cloud session on Anthropic-managed infrastructure | Your repository is on GitHub and the task should keep running after you put your phone away. See the [web quickstart](/en/web-quickstart) to set up. |
| [Remote Control](/en/remote-control)                 | A Claude Code session running on your computer      | The work needs your local filesystem, tools, or MCP servers.                                                                                         |
| [Dispatch](/en/desktop#sessions-from-dispatch)       | The Desktop app on your computer                    | You want to message a task and let Dispatch decide how to run it. Requires a Pro or Max plan.                                                        |

If your computer will be off, use cloud sessions: they run on Anthropic's infrastructure and continue with your laptop closed. Remote Control and Dispatch drive your own machine, so it needs to stay on with Claude Code or the Desktop app running. If your machine sleeps during a Remote Control session, the session reconnects when it comes back online.

For a fuller comparison that also covers Channels, Slack, and scheduled tasks, see [work when you are away from your terminal](/en/platforms#work-when-you-are-away-from-your-terminal).

Cloud sessions and Remote Control run from the **Code** tab and are covered below. For Dispatch, which you message as a task in the app, see [sessions from Dispatch](/en/desktop#sessions-from-dispatch).

### Start and monitor cloud sessions

Claude Code on the web runs tasks on Anthropic-managed cloud infrastructure, so a session continues after you put your phone away. From the Code tab, select a repository and branch, describe the task, and submit it. Sessions persist across devices: a task you start on your laptop is ready to review from your phone, and one you start from your phone is waiting when you're back at your desk.

Open a session in the app to check progress, answer Claude's questions, or steer it in a new direction. You can also tell Claude to [watch a pull request](/en/claude-code-on-the-web#auto-fix-pull-requests) and fix CI failures or review comments as they arrive. To connect GitHub and create your first environment, follow the [web quickstart](/en/web-quickstart), and see [Claude Code on the web](/en/claude-code-on-the-web) for everything cloud sessions can do.

### Continue a local session with Remote Control

Remote Control connects the Claude app to a Claude Code session running on your machine, so code execution and filesystem access stay local while you drive the session from your phone. Start the session on your computer with `claude remote-control`, or run `/remote-control` in a session that's already open. Then scan the session QR code the terminal can display, or open the Claude app, tap **Code**, and pick the session from the list. See [connect from another device](/en/remote-control#connect-from-another-device) for each option.

Attachments you add in the Claude app reach the local session too: Claude Code downloads the image or file to your machine and passes it to Claude as an `@` file reference. For requirements, invocation modes, and troubleshooting, see the [Remote Control overview](/en/remote-control).

### Get push notifications

When Remote Control is active, Claude can send push notifications to your phone, typically when a long-running task finishes or when it needs a decision from you. You can also ask for one in your prompt, such as `notify me when the tests finish`. See [mobile push notifications](/en/remote-control#mobile-push-notifications) for the two `/config` toggles and delivery troubleshooting.

Dispatch sends its own notification when a Code session it spawned finishes or needs your approval, described in [sessions from Dispatch](/en/desktop#sessions-from-dispatch).

## Limitations

The mobile client covers most of what a session needs, with a few limitations:

* **Local-only commands**: commands that only run in the terminal interface, such as `/plugin` and `/resume`, don't work from the app. The [Remote Control limitations](/en/remote-control#limitations) list the commands that do work from mobile and how their behavior differs.
* **Permission modes**: cloud sessions offer Accept edits, Plan, and Auto in the mode dropdown, and Remote Control sessions offer Manual, Accept edits, and Plan. You can't select Bypass permissions from the app in either case, and you can't select Auto for a Remote Control session. See [switch permission modes](/en/permission-modes#switch-permission-modes).
* **Dispatch plans**: Dispatch requires a Pro or Max plan and isn't available on Team or Enterprise.

## Related resources

* [Platforms and integrations](/en/platforms): compare every surface Claude Code runs on
* [Claude Code on the web](/en/claude-code-on-the-web): how cloud sessions run, network access, and moving work to and from your terminal
* [Remote Control](/en/remote-control): continue a local session from any device
* [Sessions from Dispatch](/en/desktop#sessions-from-dispatch): how Dispatch tasks become Code sessions in the Desktop app
* [Channels](/en/channels): ask Claude something from your phone via Telegram, Discord, or iMessage while the work runs on your machine
* [Claude Code in Slack](/en/slack): delegate coding tasks from your Slack workspace by mentioning `@Claude`
