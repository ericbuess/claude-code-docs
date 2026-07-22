> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get started with the desktop app

> Install Claude Code on desktop and start your first coding session

The desktop app gives you Claude Code with a graphical interface built for running multiple sessions side by side: a sidebar for managing parallel work, a drag-and-drop layout with an integrated terminal and file editor, visual diff review, live app preview, GitHub PR monitoring with auto-merge, and scheduled tasks. No terminal required.

<CardGroup cols={3}>
  <Card title="Download for macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
    Universal build for Intel and Apple Silicon
  </Card>

  <Card title="Download for Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs">
    For x64 processors
  </Card>

  <Card title="Get Claude for Linux (beta)" icon="linux" href="/docs/en/desktop-linux">
    apt or .deb for Ubuntu and Debian
  </Card>
</CardGroup>

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). On Linux, install with apt; see [Claude Desktop on Linux](/docs/en/desktop-linux).

<Note>
  Claude Code requires a [Pro, Max, Team, or Enterprise subscription](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing).
</Note>

This page walks through installing the app and starting your first session. If you're already set up, see [Use Claude Code Desktop](/docs/en/desktop) for the full reference.

The desktop app has three tabs:

* **Chat**: General conversation with no file access, similar to claude.ai.
* **Cowork**: An autonomous background agent that works on tasks in a sandboxed virtual machine with its own environment, running independently while you do other work. On-device Cowork sessions run the VM on your computer; remote Cowork sessions run on an Anthropic-managed VM instead.
* **Code**: An interactive coding assistant with direct access to your local files. You review and approve each change in real time.

Chat and Cowork are covered in the [Claude Help Center](https://support.claude.com/); installing and deploying the desktop app is covered in the [Claude Desktop support articles](https://support.claude.com/en/collections/16163169-claude-desktop). This page focuses on the **Code** tab.

## Install

<Steps>
  <Step title="Install and sign in">
    On macOS and Windows, download the installer from the links above and run it. On Linux, follow the install steps in [Claude Desktop on Linux](/docs/en/desktop-linux). Launch Claude from your Applications folder on macOS, the Start menu on Windows, or your application launcher on Linux, then sign in with your Anthropic account.
  </Step>

  <Step title="Open the Code tab">
    Click the **Code** tab at the top center. If clicking Code prompts you to upgrade, you need to [subscribe to a paid plan](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_upgrade) first. If it prompts you to sign in online, complete the sign-in and restart the app. If you see a 403 error, see [authentication troubleshooting](/docs/en/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

The desktop app includes Claude Code. You don't need to install Node.js or the CLI separately. To use `claude` from the terminal, install the CLI separately. See [Get started with the CLI](/docs/en/quickstart).

## Start your first session

With the Code tab open, choose a project and give Claude something to do.

<Steps>
  <Step title="Choose an environment and folder">
    Select **Local** to run Claude on your machine using your files directly. Click **Select folder** and choose your project directory.

    <Tip>
      Start with a small project you know well. It's the fastest way to see what Claude Code can do. On Windows, [Git](https://git-scm.com/downloads/win) must be installed for local sessions to work. Most Macs include Git by default.
    </Tip>

    You can also select:

    * **Cloud**: Run sessions on Anthropic's cloud infrastructure that continue even if you close the app. Cloud sessions use the same infrastructure as [Claude Code on the web](/docs/en/claude-code-on-the-web).
    * **SSH**: Connect to a remote machine over SSH, such as your own servers, cloud VMs, or dev containers. Desktop installs Claude Code on the remote machine automatically the first time you connect.
    * **WSL** (Windows): Run the session inside a [WSL 2 distribution](/docs/en/desktop-wsl); Claude Code, tools, and git execute on the Linux side with native paths.
  </Step>

  <Step title="Choose a model">
    Select a model from the dropdown next to the send button. See [models](/docs/en/model-config#available-models) for a comparison of the available models. You can change the model later from the same dropdown.
  </Step>

  <Step title="Tell Claude what to do">
    Type what you want Claude to do:

    * `Find a TODO comment and fix it`
    * `Add tests for the main function`
    * `Create a CLAUDE.md with instructions for this codebase`

    A [session](/docs/en/desktop#work-in-parallel-with-sessions) is a conversation with Claude about your code. Each session tracks its own context and changes, so you can work on multiple tasks without them interfering with each other.
  </Step>

  <Step title="Review and accept changes">
    By default, the Code tab starts in [Manual mode](/docs/en/desktop#choose-a-permission-mode), where Claude proposes changes and waits for your approval before applying them. You'll see:

    1. A [diff view](/docs/en/desktop#review-changes-with-diff-view) showing exactly what will change in each file
    2. Accept/Reject buttons to approve or decline each change
    3. Real-time updates as Claude works through your request

    If you reject a change, Claude will ask how you'd like to proceed differently. Your files aren't modified until you accept.
  </Step>
</Steps>

## Now what?

You've made your first edit. For the full reference on everything Desktop can do, see [Use Claude Code Desktop](/docs/en/desktop). Here are some things to try next.

**Interrupt and steer.** You can redirect Claude at any point. Click the stop button to interrupt immediately, or type a correction and press **Enter** to send it without stopping the running action. Either way, you don't have to wait for it to finish or start over.

**Give Claude more context.** Type `@filename` in the prompt box to pull a specific file into the conversation, attach images and PDFs using the attachment button, or drag and drop files directly into the prompt. The more context Claude has, the better the results. See [Add files and context](/docs/en/desktop#add-files-and-context-to-prompts).

**Use skills for repeatable tasks.** Type `/` or click **+** → **Slash commands** to browse [built-in commands](/docs/en/commands), [custom skills](/docs/en/skills), and plugin skills. Skills are reusable prompts you can invoke whenever you need them, like code review checklists or deployment steps.

**Review changes before committing.** After Claude edits files, a `+12 -1` indicator appears. Click it to open the [diff view](/docs/en/desktop#review-changes-with-diff-view), review modifications file by file, and comment on specific lines. Claude reads your comments and revises. Click **Review code** to have Claude evaluate the diffs itself and leave inline suggestions.

**Adjust how much control you have.** Your [permission mode](/docs/en/desktop#choose-a-permission-mode) sets how much Claude can do without asking for approval:

* **Manual**: the default. Claude asks before editing files or running commands.
* **Accept edits**: Claude auto-accepts file edits for faster iteration.
* **Plan**: Claude proposes an approach without editing any files, which is useful before a large refactor.

**Add plugins for more capabilities.** Click the **+** button next to the prompt box and select **Plugins** to browse and install [plugins](/docs/en/desktop#install-plugins) that add skills, agents, MCP servers, and more.

**Arrange your workspace.** Drag the chat, diff, terminal, file, and browser panes into whatever layout you want. Open the terminal with **Ctrl+\`** to run commands alongside your session, or click a file path to open it in the file pane. See [Arrange your workspace](/docs/en/desktop#arrange-your-workspace).

**Preview your app.** When you run your dev server in the desktop, your app opens in the Browser pane, which can also [open external sites](/docs/en/desktop#browse-external-sites). Claude can view the running app, test endpoints, inspect logs, and iterate on what it sees. See [Preview your app](/docs/en/desktop#preview-your-app).

**Track your pull request.** After opening a PR, Claude Code monitors CI check results and can automatically fix failures or merge the PR once all checks pass. See [Monitor pull request status](/docs/en/desktop#monitor-pull-request-status).

**Put Claude on a schedule.** Set up [scheduled tasks](/docs/en/desktop-scheduled-tasks) to run Claude automatically on a recurring basis: a daily code review every morning, a weekly dependency audit, or a briefing that pulls from your connected tools.

**Scale up when you're ready.** Open [parallel sessions](/docs/en/desktop#work-in-parallel-with-sessions) from the sidebar to work on multiple tasks at once, each in its own Git worktree, and open the [tasks pane](/docs/en/desktop#watch-background-tasks) to watch the subagents and background commands a session has running. Open a [side chat](/docs/en/desktop#ask-a-side-question-without-derailing-the-session) to ask a question without derailing the main thread. Send [long-running work to the cloud](/docs/en/desktop#run-long-running-tasks-remotely) so it continues even if you close the app, or [continue a session on the web or in your IDE](/docs/en/desktop#continue-in-another-surface) if a task takes longer than expected. [Connect external tools](/docs/en/desktop#extend-claude-code) like GitHub, Slack, and Linear to bring your workflow together.

## Coming from the CLI?

Desktop runs the same engine as the CLI with a graphical interface. You can run both simultaneously on the same project, and they share configuration (CLAUDE.md files, MCP servers, hooks, skills, and settings). For a full comparison of features, flag equivalents, and what's not available in Desktop, see [CLI comparison](/docs/en/desktop#coming-from-the-cli).

## What's next

* [Use Claude Code Desktop](/docs/en/desktop): permission modes, parallel sessions, diff view, connectors, and enterprise configuration
* [Troubleshooting](/docs/en/desktop#troubleshooting): solutions to common errors and setup issues
* [Best practices](/docs/en/best-practices): tips for writing effective prompts and getting the most out of Claude Code
* [Common workflows](/docs/en/common-workflows): tutorials for debugging, refactoring, testing, and more
