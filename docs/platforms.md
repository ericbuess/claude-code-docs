> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Platforms and integrations

> Choose where to run Claude Code and what to connect it to. Compare the CLI, Desktop, VS Code, JetBrains, web, mobile, and integrations like Chrome, Slack, and CI/CD.

Claude Code runs the same underlying engine everywhere, but each surface is tuned for a different way of working. This page helps you pick the right platform for your workflow and connect the tools you already use.

## Where to run Claude Code

Choose a platform based on how you like to work and where your project lives.

| Platform | Best for | What you get |
| :- | :- | :- |
| [CLI](/docs/en/quickstart.md) | Terminal workflows, scripting, remote servers | Full feature set, [Agent SDK](/docs/en/headless.md), [computer use](/docs/en/computer-use.md) on macOS (Pro and Max), third-party providers |
| [Desktop](/docs/en/desktop.md) | Visual review, parallel sessions, managed setup | Diff viewer, app preview, [computer use](/docs/en/desktop.md#let-claude-use-your-computer) and [Dispatch](/docs/en/desktop.md#sessions-from-dispatch) on Pro and Max |
| [VS Code](/docs/en/vs-code.md) | Working inside VS Code without switching to a terminal | Inline diffs, integrated terminal, file context |
| [JetBrains](/docs/en/jetbrains.md) | Working inside IntelliJ, PyCharm, WebStorm, or other JetBrains IDEs | Diff viewer, selection sharing, terminal session |
| [Web](/docs/en/claude-code-on-the-web.md) | Long-running tasks that don't need much steering, or work that should continue when you're offline | Cloud, Anthropic-managed by default; continues after you disconnect |
| [Mobile](/docs/en/mobile.md) | Starting and monitoring tasks while away from your computer | Cloud sessions from the Claude app for iOS and Android, [Remote Control](/docs/en/remote-control.md) for local sessions, [Dispatch](/docs/en/desktop.md#sessions-from-dispatch) to Desktop on Pro and Max |

The CLI is the most complete surface for terminal-native work: scripting and the Agent SDK are CLI-only. Third-party providers also work in [VS Code](/docs/en/vs-code.md#use-third-party-providers) and in [JetBrains](/docs/en/feature-availability.md#features-available-on-every-provider), which runs the CLI in your IDE's terminal. Enterprise [Desktop](/docs/en/desktop.md) deployments support Google Cloud's Agent Platform, and Desktop supports [gateway providers](/docs/en/llm-gateway-connect.md#desktop-app); for Amazon Bedrock or Microsoft Foundry, use the CLI or an IDE extension, or [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview), which runs the Code tab on those providers. Desktop and the IDE extensions trade some CLI-only features for visual review and tighter editor integration. The web runs in the cloud, so tasks keep going after you disconnect. Mobile is a thin client into those same cloud sessions or into a local session via Remote Control, and can send tasks to Desktop with Dispatch.

You can mix surfaces on the same project. Configuration, project memory, and MCP servers are shared across the local surfaces.

## Connect your tools

Integrations let Claude work with services outside your codebase.

| Integration | What it does | Use it for |
| :- | :- | :- |
| [Chrome](/docs/en/chrome.md) | Controls your browser with your logged-in sessions | Testing web apps, filling forms, automating sites without an API |
| [GitHub Actions](/docs/en/github-actions.md) | Runs Claude in your CI pipeline | Automated PR reviews, issue triage, scheduled maintenance |
| [GitLab CI/CD](/docs/en/gitlab-ci-cd.md) | Same as GitHub Actions for GitLab | CI-driven automation on GitLab |
| [Code Review](/docs/en/code-review.md) | Reviews every PR automatically | Catching bugs before human review |
| [Slack](/docs/en/slack.md) | Responds to `@Claude` mentions in your channels, under your own account | Turning bug reports into pull requests from team chat on Pro and Max plans |
| [Claude Tag](https://claude.com/docs/claude-tag) | Runs `@Claude` as your organization's shared identity with admin-configured access | Shared team access on Team and Enterprise plans, instead of per-user Slack sessions |

For integrations not listed here, [MCP servers](/docs/en/mcp.md) and [connectors](/docs/en/desktop.md#connect-external-tools) let you connect almost anything: Linear, Notion, Google Drive, or your own internal APIs.

## Work when you are away from your terminal

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

| | Trigger | Claude runs on | Setup | Best for |
| :- | :- | :- | :- | :- |
| [Dispatch](/docs/en/desktop.md#sessions-from-dispatch) | Message a task from the Claude mobile app | Your machine (Desktop) | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068) | Delegating work while you're away, minimal setup |
| [Remote Control](/docs/en/remote-control.md) | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI, Desktop, or VS Code) | Run [`claude remote-control` or `/remote-control`](/docs/en/remote-control#start-a-remote-control-session) | Steering in-progress work from another device |
| [Channels](/docs/en/channels.md) | Push events from a chat app like Telegram or Discord, or your own server | Your machine (CLI) | [Install a channel plugin](/docs/en/channels.md#quickstart) or [build your own](/docs/en/channels-reference.md) | Reacting to external events like CI failures or chat messages |
| [Slack](/docs/en/slack.md) | Mention `@Claude` in a team channel | Anthropic cloud | [Install the Slack app](/docs/en/slack.md#setting-up-claude-code-in-slack) with [Claude Code on the web](/docs/en/claude-code-on-the-web.md) enabled, on Pro and Max plans | PRs and reviews from team chat |
| [Self-hosted environments](/docs/en/self-hosted-environments) | Start a [cloud session](/docs/en/claude-code-on-the-web.md) and pick your organization's environment | Your organization's infrastructure | [Deploy runners](/docs/en/self-hosted-environments-quickstart.md), on Team and Enterprise plans | Cloud sessions that must run inside your network |
| [Scheduled tasks](/docs/en/scheduled-tasks.md) | Set a schedule | [CLI](/docs/en/scheduled-tasks.md), [Desktop](/docs/en/desktop-scheduled-tasks.md), or [cloud](/docs/en/routines.md) | Pick a frequency | Recurring automation like daily reviews |

If you're not sure where to start, [install the CLI](/docs/en/quickstart.md) and run it in a project directory. If you'd rather not use a terminal, [Desktop](/docs/en/desktop-quickstart.md) gives you the same engine with a graphical interface.

## Related resources

### Platforms

* [CLI quickstart](/docs/en/quickstart.md): install and run your first command in the terminal
* [Desktop](/docs/en/desktop.md): visual diff review, parallel sessions, computer use, and Dispatch
* [VS Code](/docs/en/vs-code.md): the Claude Code extension inside your editor
* [JetBrains](/docs/en/jetbrains.md): the extension for IntelliJ, PyCharm, and other JetBrains IDEs
* [Web](/docs/en/claude-code-on-the-web.md): cloud sessions from your browser at claude.ai/code that keep running when you disconnect
* [Projects](/docs/en/claude-projects.md): one conversation where Claude coordinates many cloud sessions for a body of work and reports back
* [Mobile](/docs/en/mobile.md): the Claude app for [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) and [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) for starting and monitoring tasks while away from your computer

### Integrations

* [Chrome](/docs/en/chrome.md): automate browser tasks with your logged-in sessions
* [Computer use](/docs/en/computer-use.md): let Claude open apps and control your screen on macOS
* [GitHub Actions](/docs/en/github-actions.md): run Claude in your CI pipeline
* [GitLab CI/CD](/docs/en/gitlab-ci-cd.md): the same for GitLab
* [Code Review](/docs/en/code-review.md): automatic review on every pull request
* [Slack](/docs/en/slack.md): send tasks from team chat and get PRs back, on Pro and Max plans
* [Claude Tag](https://claude.com/docs/claude-tag): run `@Claude` as your organization's shared identity on Team and Enterprise plans

### Remote access

* [Dispatch](/docs/en/desktop.md#sessions-from-dispatch): message a task from your phone and it can spawn a Desktop session
* [Remote Control](/docs/en/remote-control.md): drive a running session from your phone or browser
* [Channels](/docs/en/channels.md): push events from chat apps or your own servers into a session
* [Scheduling options](/docs/en/scheduled-tasks.md#compare-scheduling-options): run prompts on a recurring schedule
