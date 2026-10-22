> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get started with the desktop app

> Install the Claude desktop app, open the Code tab, and start your first Claude Code session on a project folder on your computer.

The desktop app gives you Claude Code with a graphical interface. You can ask Claude to work on the code in a folder on your computer and review its changes without using a terminal.

Claude Code is in the **Code** tab at the top of the app's sidebar. This page walks through installing the app and starting your first session there. Claude Code requires a [Pro, Max, Team, or Enterprise subscription](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing).

> **[Download for macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)**
>
> Universal build for Intel and Apple Silicon

> **[Download for Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)**
>
> For x64 processors

> **[Get Claude for Linux (beta)](/docs/en/desktop-linux.md)**
>
> apt or .deb for Ubuntu and Debian

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). On Linux, install with apt; see [Claude Desktop on Linux](/docs/en/desktop-linux.md).

> [!NOTE]
>
> These cases are covered on other pages:
>
> * **Already set up**: see [Use Claude Code Desktop](/docs/en/desktop.md) for everything the Code tab can do
> * **Want `claude` in your terminal**: [install the CLI](/docs/en/quickstart.md) separately
> * **Using chat or Cowork**: see the [Claude Help Center](https://support.claude.com/)
> * **Need more on installing or deploying the desktop app**: see the [Claude Desktop support articles](https://support.claude.com/en/collections/16163169-claude-desktop)

## Install

**1. Install and sign in**

On macOS and Windows, download the installer from the links above and run it. On Linux, follow the install steps in [Claude Desktop on Linux](/docs/en/desktop-linux.md). Launch Claude from your Applications folder on macOS, the Start menu on Windows, or your application launcher on Linux, then sign in with your Anthropic account.

**2. Open the Code tab**

Click the **Code** tab at the top of the sidebar. If the tabs show only icons, hover over one to see its name. If a prompt or an error appears after you click **Code**, follow the matching fix:

* **Prompt to upgrade**: you need to [subscribe to a paid plan](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_upgrade) first
* **Prompt to sign in online**: complete the sign-in and restart the app
* **403 error**: see [authentication troubleshooting](/docs/en/desktop.md#403-or-authentication-errors-in-the-code-tab)

The desktop app includes Claude Code, so you don't need to install Node.js or the CLI to use the Code tab.

## Start your first session

With the Code tab open, choose a project and give Claude something to do.

**1. Choose an environment and folder**

In the [row under the prompt box](/docs/en/desktop.md#start-a-session), click the first control, the environment selector, and select the top entry in the **Local** group. Then click the project folder control beside the environment selector, select **Open folder…**, and choose your project's directory.

If no environment selector appears under your prompt box, you have the earlier layout. See [Check which layout you have](/docs/en/desktop.md#check-which-layout-you-have).

> [!TIP]
>
> Start with a small project you know well. It's the fastest way to see what Claude Code can do.

You can also select:

* **Cloud**: Run sessions in the cloud that continue even if you close the app. See [Use Claude Code in the cloud](/docs/en/claude-code-on-the-web.md) for how cloud sessions work.
* **SSH**: Connect to a remote machine over SSH, such as your own servers, cloud VMs, or dev containers. [Add a connection](/docs/en/desktop.md#ssh-sessions) first. Desktop installs Claude Code on the remote machine automatically the first time you connect. A running task can [keep going while Desktop is disconnected](/docs/en/desktop.md#keep-a-task-running-while-desktop-is-disconnected), but with a Claude account it can stop when its sign-in expires.
* **WSL** (Windows): Run the session inside a [WSL 2 distribution](/docs/en/desktop-wsl.md); Claude Code, tools, and git execute on the Linux side with native paths.

**2. Choose a model**

Select a model from the model picker toward the right end of the row under the prompt box. See [models](/docs/en/model-config.md#available-models) for a comparison of the available models. You can change the model later from the model picker.

**3. Tell Claude what to do**

Type what you want Claude to do:

* `Find a TODO comment and fix it`
* `Add tests for the main function`
* `Create a CLAUDE.md with instructions for this codebase`

A [session](/docs/en/desktop.md#work-in-parallel-with-sessions) is a conversation with Claude about your code. Each session tracks its own context and changes.

**4. Review and accept changes**

Check your [permission mode](/docs/en/desktop.md#choose-a-permission-mode) in the row under the prompt box to see whether Claude waits for your approval:

* **Auto or Accept edits**: Claude applies its file changes, and an indicator such as `+12 -1` appears so you can review them in the [diff view](/docs/en/desktop.md#review-changes-with-diff-view)
* **Manual**: Claude proposes each change and waits for your approval before applying it

In Manual mode, you'll see:

1. A diff showing exactly what will change
2. Buttons to approve or decline each change
3. Real-time updates as Claude works through your request

## Now what?

You've made your first edit. For the full reference on everything Desktop can do, see [Use Claude Code Desktop](/docs/en/desktop.md). Here are some things to try next.

**Interrupt and steer.** You can redirect Claude at any point. Click the stop button to interrupt immediately, or type a correction and press **Enter** to send it without stopping the running action. Either way, you don't have to wait for it to finish or start over.

**Give Claude more context.** Type `@filename` in the prompt box to pull a specific file into the conversation. The more context Claude has, the better the results. See [Add files and context](/docs/en/desktop.md#add-files-and-context-to-prompts).

**Use skills for repeatable tasks.** Type `/` or click **+** → **Slash commands** to browse [built-in commands](/docs/en/commands.md), [custom skills](/docs/en/skills.md), and plugin skills. Skills are reusable prompts you can invoke whenever you need them, like code review checklists or deployment steps.

**Review changes before committing.** After Claude edits files, a `+12 -1` indicator appears. Click it to open the [diff view](/docs/en/desktop.md#review-changes-with-diff-view), review modifications file by file, and comment on specific lines. Claude reads your comments and revises. To have Claude review the changes itself, enter [`/code-review`](/docs/en/desktop#review-your-code) in the prompt box.

**Adjust how much control you have.** Your [permission mode](/docs/en/desktop.md#choose-a-permission-mode) sets how much Claude can do without asking for approval:

* **Auto**: a classifier reviews actions in the background and blocks the risky ones instead of asking you.
* **Manual**: Claude asks before editing files or running commands.
* **Accept edits**: Claude auto-accepts file edits for faster iteration.
* **Plan**: Claude proposes an approach without editing any files, which is useful before a large refactor.

**Add plugins for more capabilities.** Install [plugins](/docs/en/desktop.md#install-plugins) that add skills, agents, MCP servers, and more.

**Arrange your workspace.** Drag the chat, diff, terminal, file, and browser panes into whatever layout you want. Open the terminal with **Ctrl+\`** to run commands alongside your session, or click a file path to open it. See [Arrange your workspace](/docs/en/desktop.md#arrange-your-workspace).

**Preview your app.** When you run your dev server in the desktop, your app opens in the Browser pane, which can also [open external sites](/docs/en/desktop.md#browse-external-sites). Claude can view the running app, test endpoints, inspect logs, and iterate on what it sees. See [Preview your app](/docs/en/desktop.md#preview-your-app).

**Track your pull request.** After opening a PR, Claude Code monitors CI check results and can automatically fix failures. See [Monitor pull request status](/docs/en/desktop.md#monitor-pull-request-status).

**Put Claude on a schedule.** Set up [scheduled tasks](/docs/en/desktop-scheduled-tasks.md) to run Claude automatically on a recurring basis: a daily code review every morning, a weekly dependency audit, or a briefing that pulls from your connected tools.

**Scale up when you're ready.** Open [parallel sessions](/docs/en/desktop.md#work-in-parallel-with-sessions) from the sidebar to work on multiple tasks at once, optionally each in its own Git worktree, and open the [tasks pane](/docs/en/desktop.md#watch-background-tasks) to watch the subagents and background commands a session has running. Open a [side chat](/docs/en/desktop.md#ask-a-side-question-without-derailing-the-session) to ask a question without derailing the main thread. Send [long-running work to the cloud](/docs/en/desktop.md#run-long-running-tasks-in-the-cloud) so it continues even if you close the app, or [move a session you already started to the cloud](/docs/en/desktop.md#continue-in-another-surface) if a task takes longer than expected. [Connect external tools](/docs/en/desktop.md#extend-claude-code) like GitHub, Slack, and Linear to bring your workflow together.

## What's next

* [Use Claude Code Desktop](/docs/en/desktop.md): permission modes, parallel sessions, diff view, connectors, and enterprise configuration
* [Coming from the CLI?](/docs/en/desktop.md#coming-from-the-cli): run Desktop and the CLI on the same project, and compare features, flag equivalents, and what's not available in Desktop
* [Troubleshooting](/docs/en/desktop.md#troubleshooting): solutions to common errors and setup issues
* [Best practices](/docs/en/best-practices.md): tips for writing effective prompts and getting the most out of Claude Code
* [Common workflows](/docs/en/common-workflows.md): tutorials for debugging, refactoring, testing, and more
