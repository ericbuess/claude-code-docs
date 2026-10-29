> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Desktop application

> Get more out of Claude Code Desktop: parallel sessions with Git isolation, drag-and-drop pane layout, integrated terminal and file editor, side chats, computer use, Dispatch sessions from your phone, visual diff review, app previews, PR monitoring, connectors, and enterprise configuration.

In the Claude Desktop app, Claude Code is the **Code** tab. The app also has chat and [Cowork](https://claude.com/product/cowork), which handles Dispatch and longer agentic work. This page is the reference for the Code tab.

> **[Download for macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)**
>
> Universal build for Intel and Apple Silicon

> **[Download for Windows](https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs)**
>
> For x64 processors

> **[Get Claude for Linux (beta)](https://code.claude.com/docs/en/desktop-linux.md)**
>
> apt or .deb for Ubuntu and Debian

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). On Linux, install with apt; see [Claude Desktop on Linux](https://code.claude.com/docs/en/desktop-linux.md).

After installing, launch Claude, sign in, and click the **Code** tab. For a walkthrough of your first session, see the [Get started guide](https://code.claude.com/docs/en/desktop-quickstart.md).

In the Code tab, each conversation is a **session**: it has its own chat history and project folder, independent of any other session. The sidebar lists your sessions and lets you run several in parallel. Within a session you can:

* [Review and comment on diffs](#review-changes-with-diff-view), then [watch the resulting PR through CI](#monitor-pull-request-status)
* [Preview your running app](#preview-your-app) in the Browser pane while Claude verifies its own changes, and [open external sites](#browse-external-sites) alongside it
* Watch Claude [run and test your iOS app](https://code.claude.com/docs/en/desktop-ios-simulator.md) in the iOS Simulator pane
* [Arrange panes](#arrange-your-workspace) for the chat, diff, browser, terminal, and file editor side by side
* Ask a [side question](#ask-a-side-question-without-derailing-the-session) that uses the session's context without derailing it
* Let Claude [check on, message, or archive your other sessions](#work-across-sessions)
* [Connect external tools](#connect-external-tools) like GitHub, Slack, and Linear
* Let Claude [open apps and control your screen](#let-claude-use-your-computer)
* Run on your machine, in the [cloud](#run-long-running-tasks-in-the-cloud), or over [SSH](#ssh-sessions)

For [scheduled recurring work](https://code.claude.com/docs/en/desktop-scheduled-tasks.md), [keyboard shortcuts](#keyboard-shortcuts), or [sending tasks from your phone](#sessions-from-dispatch), see the linked pages and sections. If you already use the terminal-based CLI, see the [CLI comparison](#coming-from-the-cli) for what carries over.

## Start a session

Before you send your first message, choose the environment, project folder, permission mode, and model in the row under the prompt box:

* **Environment**: use the environment selector, the first control in the row, to choose where Claude runs. See [environment configuration](#environment-configuration).
  * If a new session shows no environment under the prompt box, follow the [earlier layout's steps](#check-which-layout-you-have).
* **Project folder**: click the project folder control, next to the environment selector, to choose the folder Claude works in.
  * **Cloud session**: select [repositories](#run-long-running-tasks-in-the-cloud) instead of a folder
  * **[Saved local or SSH environment](#create-a-saved-environment)**: the environment already holds its folders, so the row shows no project folder control. To change the folders, [edit the environment](#use-edit-or-remove-a-saved-environment).
* **Permission mode**: use the [mode selector](#choose-a-permission-mode) to choose how much autonomy Claude has. You can change the permission mode during the session.
* **Model**: pick a [model](https://code.claude.com/docs/en/model-config.md#available-models) from the model picker toward the right end of the row. You can change the model during the session.

Type your task and press **Enter** to start. Each session tracks its own context and changes independently.

## Work with code

Give Claude the right context, control how much it does on its own, and review what it changed.

### Use the prompt box

Type what you want Claude to do and press **Enter** to send. Claude reads your project files, makes changes, and runs commands based on your [permission mode](#choose-a-permission-mode). You can redirect Claude at any point: click the stop button to interrupt immediately, or type a correction and press **Enter** to send it without stopping the running action. Claude reads the correction as soon as the current action completes and adjusts before its next step.

Click the **+** button next to the prompt box for file attachments, [skills](#use-skills), [connectors](#connect-external-tools), and [plugins](#install-plugins).

### Accept a suggested prompt

After Claude replies, the Code tab can show a suggested next prompt as gray text in the empty prompt box. Claude Code [generates each suggestion](https://code.claude.com/docs/en/interactive-mode.md#prompt-suggestions) from your conversation with a short background request that counts toward your plan's usage limits or your API costs.

* **Use the suggestion**: press **Tab** or **Right arrow** to place it in the prompt box, edit it if you want, then press **Enter** to send it. Pressing **Enter** before you accept the suggestion doesn't send it.
* **Write your own prompt**: start typing. The suggestion shows only while the prompt box is empty and has no attached files.

Turn off **Prompt suggestions** in **Settings > Code** or **Settings > Claude Code** to stop suggestions. Each session stops showing them the next time it starts or resumes.

### Add files and context to prompts

To give Claude a file, @mention it or attach it in the prompt box:

* **@mention files**: type `@` followed by a filename to add a file to the conversation context.
  * **In a cloud session**: `@` can list files only after you send your first message. If `@` lists none, send your first message without the file, then @mention the file in your next message.
* **Attach files**: attach images, PDFs, and other files to your prompt from the **+** button next to the prompt box, or drag and drop files directly into the prompt. This is useful for sharing screenshots of bugs, design mockups, or reference documents.
  * **In a [WSL session](https://code.claude.com/docs/en/desktop-wsl.md)**: if the **+** menu shows **Add image** instead of **Add files or photos**, you can attach only images. To give Claude any other file from the session's folder, @mention it.

### Choose a permission mode

Permission modes control how much autonomy Claude has during a session: whether it asks before editing files, running commands, or both. You can switch permission modes at any time using the mode selector in the row under the prompt box. To approve each change yourself, switch to Manual.

To set a default mode for new local sessions, add `permissions.defaultMode` to your [settings file](https://code.claude.com/docs/en/settings.md#where-settings-live). The desktop app reads the same settings files as the CLI. A mode you pick in the selector is remembered per folder and takes precedence over `defaultMode` for that folder, except Plan, which applies to the current session only.

| Mode | Settings key | Behavior |
| - | - | - |
| **Manual** | `default` | Claude asks before editing files or running commands. You see a diff and can accept or reject each change. |
| **Accept edits** | `acceptEdits` | Claude auto-accepts file edits and common filesystem commands like `mkdir`, `touch`, and `mv`, but still asks before running other terminal commands. Use this when you trust file changes and want faster iteration. |
| **Plan** | `plan` | Claude reads files and runs commands to explore, then proposes a plan without editing your source code. Good for complex tasks where you want to review the approach first. |
| **Auto** | `auto` | Claude runs without routine prompts; before actions such as shell commands and network requests run, a background classifier checks that they align with your request. Appears when [auto mode is available](#auto-mode-availability); there is no separate Settings toggle for it. |
| **Bypass permissions** | `bypassPermissions` | Claude runs without permission prompts, except for the [actions no mode auto-approves](https://code.claude.com/docs/en/permission-modes.md#actions-no-mode-auto-approves), safety classifiers when Claude [acts on external sites](#browse-external-sites), or desktop actions such as deleting a session, though not [archiving one](#work-across-sessions). Equivalent to `--dangerously-skip-permissions` in the CLI. On Pro and Max plans, enable "Allow bypass permissions mode" in **Settings > Code** or **Settings > Claude Code**. On Team and Enterprise plans there is no Settings toggle, and organization policy controls it instead. Only use this in sandboxed containers or VMs. |

Earlier versions of the Code tab labeled these modes Ask permissions, Auto accept edits, and Plan mode.

The `dontAsk` permission mode is available only in the [CLI](https://code.claude.com/docs/en/permission-modes.md#allow-only-pre-approved-tools-with-dontask-mode).

> [!TIP]
>
> Start complex tasks in Plan so Claude maps out an approach before making changes. Once you approve the plan, switch to Accept edits or Manual to execute it. See [plan mode](https://code.claude.com/docs/en/permission-modes.md#analyze-before-you-edit-with-plan-mode) for more on this workflow.

Cloud sessions support Accept edits, Plan, and Auto. Accept edits corresponds to `default` mode: cloud sessions pre-approve file edits, so the selector shows Accept edits instead of Manual. Bypass permissions isn't available in cloud sessions, including sessions in a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments).

Enterprise admins can restrict which permission modes are available. See [enterprise configuration](#enterprise-configuration) for details.

#### Auto mode availability

Auto mode is available to all users on the Anthropic API and requires Claude Opus 4.6 or later, Sonnet 4.6 or later, Haiku 5.5, or a [Fable model](https://code.claude.com/docs/en/model-config.md#work-with-fable). Organization administrators can turn auto mode off with the `disableAutoMode` key in [managed settings](#managed-settings).

In Enterprise deployments that route Desktop to Google Cloud's Agent Platform, auto mode is also available by default; see [Auto mode on Bedrock, Agent Platform, or Foundry](https://code.claude.com/docs/en/permission-modes.md#enable-auto-mode-on-bedrock-agent-platform-or-foundry) for the supported models.

### Preview your app

Claude can start a dev server and open it in the Browser pane to verify its changes. This works for frontend web apps as well as backend servers: Claude can test API endpoints, view server logs, and iterate on issues it finds. In most cases, Claude starts the server automatically after editing project files. You can also ask Claude to preview at any time. By default, Claude [auto-verifies](#auto-verify-changes) changes after every edit.

In a local session, click an HTML, PDF, or video path in the chat to open it in the Browser pane.

> [!NOTE]
>
> In an [SSH session](#ssh-sessions), Claude can't open your app in the Browser pane, because it doesn't have the pane's tools there. To look at the app yourself, [forward its port to your computer](#reach-a-port-on-the-remote-machine).

If the Browser pane isn't open after Claude starts a server in a local session, click **Open** on the server's card in the chat.

From the Browser pane, you can:

* Interact with your running app directly in the Browser pane
* Watch Claude verify its own changes automatically: it takes screenshots, inspects the DOM, clicks elements, fills forms, and fixes issues it finds
* Start or stop servers, or stop them all at once, from the **Dev servers** menu in the Browser pane's header
* Choose whether the Browser keeps cookies after you quit the app with **Keep cookies** in the Browser pane's **⋮** menu, so you don't have to sign in again during development

Claude creates the initial server configuration based on your project. If your app uses a custom dev command, edit `.claude/launch.json` to match your setup. See [Configure preview servers](#configure-preview-servers) for the full reference.

To clear the Browser's saved data, select **Clear browsing data** in the Browser pane's **⋮** menu. To turn the Browser off entirely, turn off **Browser tools** in **Settings > Code** or **Settings > Claude Code**.

### Browse external sites

The Browser pane is a tabbed browser, so you can open documentation, issue trackers, or any other site next to your running app. To open the Browser, press **Cmd+Shift+B** on macOS or **Ctrl+Shift+B** on Windows, or click **Browser** in the session's title bar. You can sign in to sites in the pane, including popup sign-in flows such as Google OAuth.

The first time you click an external link in the chat, a dialog asks whether links open in the Browser pane or in your default browser. To change your choice later, use **Open links in built-in browser** in the Browser pane's **⋮** menu. **Cmd**-click on macOS or **Ctrl**-click on Windows opens a link in your default browser directly.

Claude can read and interact with external pages using the same tools it uses to [verify your app](#preview-your-app), with two additional safety checks:

* Safety classifiers review Claude's write actions on external pages, such as clicking and typing, in every permission mode. These are the same classifiers [auto mode](#choose-a-permission-mode) uses, and when they flag an action, you get a permission prompt regardless of mode.
* In permission modes other than Auto and Bypass permissions, a domain allowlist check also applies before Claude navigates to a new site.

#### Approve Claude's actions on a site

The first time Claude acts on an external site, a permission card appears and Claude waits for your choice: **Allow once**, **Always allow**, or **Deny**. **Allow once** approves the action without saving anything. **Always allow** saves the approval for that site on your device, and you can revoke it in Settings. Each site needs its own approval, including subdomains. Your local dev servers and project files don't need approval, so [auto-verify](#auto-verify-changes) keeps working without prompts.

Even on an approved site, Claude won't purchase items, create accounts, or bypass CAPTCHAs without your input. Browsing in the Browser pane uses the same safety model as the [Claude in Chrome extension](https://code.claude.com/docs/en/chrome.md). See [Using Claude in Chrome safely](https://support.claude.com/en/articles/12902428-using-claude-in-chrome-safely) for how Claude handles sensitive sites and risky actions.

#### Choose between the Browser and the Chrome extension

The Browser pane uses a clean browser profile, separate from your personal browser, with none of your saved logins or history. Use it for building and testing your app and for sites that don't need your identity. When you want Claude to act as you in your logged-in sessions, use the [Claude in Chrome extension](https://code.claude.com/docs/en/chrome.md) instead, which shares your browser's login state.

#### Restrict external browsing for your organization

The Browser follows the same [site allowlist and blocklist controls](https://support.claude.com/en/articles/13065128-claude-in-chrome-admin-controls) as the Claude in Chrome extension. If your organization already configured those lists for the extension, the Browser respects them automatically. Administrators can also turn off Claude's tools on external pages with the [`browserExternalPageTools` managed setting](#managed-settings). With tools disabled, users can still visit external sites; Claude's tools can't read or act on them.

To turn off external browsing entirely, set the [`disableBrowserExternalNavigation` managed setting](#managed-settings) to `true`. This blocks all external navigation in the Browser, including sites on your organization's allowlist; localhost dev servers and file previews keep working. Use `browserExternalPageTools` to let users keep browsing external sites without Claude's tools, and `disableBrowserExternalNavigation` to block external sites for both users and Claude.

### Review changes with diff view

After Claude makes changes to your code, the diff view lets you review modifications file by file before creating a pull request. To open the diff view, click the line counts, such as `+12 -1`, in the **Changes** card of the [session details panel](#see-session-details). You can also click **Changes** in the session's title bar. A cloud session's diff against the base branch can [leave out changes that aren't pushed yet](https://code.claude.com/docs/en/claude-code-on-the-web.md#troubleshoot-a-missing-file-in-the-diff-view).

To comment on specific lines, hover over a line and click the **+** that appears beside its line number to open a comment box. Type your feedback and press **Enter** to add the comment. After adding comments to multiple lines, submit all comments at once:

* **macOS**: press **Cmd+Enter**
* **Windows**: press **Ctrl+Enter**

Claude reads your comments and makes the requested changes, which appear as a new diff you can review.

### Review your code

To have Claude review your changes before you commit, enter `/code-review` in the [prompt box](#use-the-prompt-box). The findings arrive in the conversation when the review completes.

In local, [SSH](#ssh-sessions), and [WSL](https://code.claude.com/docs/en/desktop-wsl.md) sessions, the findings appear as a **Code review** card, grouped by file. Use the card to act on them:

* Click **Walk through in diff** to open the diff view and step through the findings one at a time. A finding in the current diff appears at its line, where you can click **Fix this one** or dismiss it.
* Click **Apply fixes** to ask Claude to fix the findings that are still open.

In any session, you can also ask Claude in the prompt box to fix what the review found. For what `/code-review` looks for and the arguments it takes, see [Review locally with `/code-review`](https://code.claude.com/docs/en/code-review-local).

### Monitor pull request status

To have Claude fix failing checks, or to have GitHub merge the pull request, turn on **Auto-fix** or **Merge when ready**. After you open a pull request, it appears in the **Changes** card of the [session details panel](#see-session-details) with the status of its CI checks. Open the **⋮** menu beside its title:

* **Auto-fix**: in a local session, Claude also addresses new review comments that someone other than you leaves. The comment's author has to be the repository's owner, an organization member, a collaborator, or a GitHub App.
* **Merge when ready**: turns on GitHub's auto-merge for the PR. In a local session, Desktop requests a squash merge unless the base branch uses a merge queue.
  * **In SSH and WSL sessions**: **Merge when ready** is disabled, so turn on auto-merge for the pull request on GitHub
  * **If the repository doesn't allow auto-merge**: **Merge when ready** doesn't turn on, so enable auto-merge in your [GitHub repository settings](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) first
* **[Earlier layout](#check-which-layout-you-have)**: once the session has a pull request, click **CI** on its status bar.

To archive the session automatically once the PR merges or closes, turn on [auto-archive](#archive-a-session) in **Settings > Code** or **Settings > Claude Code**.

> [!NOTE]
>
> PR monitoring requires the [GitHub CLI (`gh`)](https://cli.github.com/) to be installed and authenticated on your machine. If `gh` is not installed, Desktop prompts you to install it the first time you try to create a PR.
>
> In an [SSH session](#ssh-sessions), set up `git` and `gh` on the remote machine before you click **Create PR**, because Claude pushes the branch and runs `gh pr create` there. Install `gh` there yourself, because Desktop doesn't prompt you to in an SSH session. Then check there that `git push` works and that `gh auth status` reports that you are logged in.

## Arrange your workspace

The Code tab is built around panes you can arrange in any layout: chat, diff, browser, terminal, file, plan, tasks, and subagent, along with the [iOS Simulator](https://code.claude.com/docs/en/desktop-ios-simulator.md) on macOS. Drag a pane by its header to reposition it, or drag a pane edge to resize it. Press **Cmd+\\** on macOS or **Ctrl+\\** on Windows to close the focused pane.

To open another pane, click its icon button in the session's title bar. Hover to see each button's name, such as **Terminal**, **Changes** for the diff view, **Browser**, and **Files**. If the pane you want has no button in the title bar, select it from the **⋮** menu beside the buttons:

* **When the window is narrow**: buttons that don't fit move into the menu
* **For panes with no button**: panes such as **Background tasks** and **Plan** are listed once the session has something to show in those panes

To work across screens, pop a pane such as the diff or terminal out into its own window, and dock it back when you're done. Claude keeps working in the main window.

> [!NOTE]
>
> The pane layout, terminal, file editor, and view modes in this section require Claude Desktop v1.2581.0 or later. Open **Claude > Check for Updates…** on macOS or **Help > Check for Updates…** on Windows to update.

### See session details

The session details panel is a set of cards beside the chat that show where the session runs, what it changed, what it's running, and its context usage. The panel appears after you start a session, while the chat is wide enough for it.

#### Hide or show the session details panel

To hide or show the panel, click **Hide session rail** or **Show session rail** in the session's title bar, or in the bar's **⋮** menu. If you still don't see the panel, [check which Code tab layout you have](#check-which-layout-you-have).

### Run commands in the terminal

The integrated terminal lets you run commands alongside your session without switching to another app. Click **Terminal** in the session's title bar or press **Ctrl+\`** on macOS or Windows. The terminal opens in your session's working directory and shares the same environment as Claude, so commands like `npm test` or `git status` see the same files Claude is editing. To open a second terminal tab, click **+** in the terminal pane header or right-click a folder in the chat to choose **Open in terminal**.

If a WSL session has no terminal, see [If the terminal or connectors are unavailable](https://code.claude.com/docs/en/desktop-wsl.md#check-for-the-terminal-and-connectors). The terminal is available in local and [SSH](#ssh-sessions) sessions, with a limit on [Windows remote machines](#windows-remote-machines).

### Open and edit files

To open a file Claude mentions, click its path in the chat.

To edit a file yourself, use the [file pane](#arrange-your-workspace):

* **Local sessions**: you can edit files inside the session's working directory, except some view-only ones such as `.mcp.json` and `.claude/settings.json`. To change one, [open it in another app](#open-files-in-other-apps).
* **Cloud, SSH, and WSL sessions**: the file pane is view-only, so ask Claude to make edits.

#### Save edits in the file pane

By default, your edits in the file pane save on their own, so the pane shows no **Save** button. To save your edits yourself, uncheck **Auto save** in the pane's **⋮** menu. With **Auto save** off, click **Save** after you change a file to write your edits, or **Cancel** to revert them.

If the pane warns that the file changed on disk, click **Override** to write your edits over the version on disk, or **Discard** to drop your edits.

### Open files in other apps

Right-click any file path in the chat, diff viewer, or file pane to open a context menu:

* **Attach as context**: add the file to your next prompt
* **Open in**: open the file in an installed editor such as VS Code, Cursor, or Zed
* **Show in Finder** on macOS, **Show in Explorer** on Windows: open the containing folder
* **Copy**: a submenu that copies the file's **Absolute path**, **Relative path**, or **Filename**

### Switch view modes

View modes control how much detail appears in the chat transcript. To switch view modes, open the session menu from the caret beside the session title and select **Transcript view**, or press **Ctrl+O** on macOS or Windows to cycle through them. The Thinking mode appears in the menu only after Claude has produced thinking in the session you're viewing.

| Mode | What it shows |
| - | - |
| **Normal** | Tool calls collapsed into summaries, with full text responses |
| **Thinking** | Tool calls collapsed into summaries, plus Claude's thinking |
| **Verbose** | Every tool call, file read, and intermediate step Claude takes, plus Claude's thinking |

Use Thinking to follow Claude's reasoning with tool calls still collapsed. Use Verbose when debugging why Claude took a particular action. Claude Desktop versions before 1.46388.1 also list a Summary mode, and a session still set to Summary opens in Normal once you update.

### Keyboard shortcuts

Press **Cmd+/** on macOS or **Ctrl+/** on Windows to see all shortcuts available in the Code tab. The table in this section shows the macOS keys. On Windows and Linux, change these keys:

* **Cmd+Option**: press **Alt**
* **Cmd+Ctrl**: press **Ctrl+Alt**
* **Cmd**: press **Ctrl**

Shortcuts that start with `Ctrl` stay the same on every platform.

| Shortcut | Action |
| - | - |
| `Cmd` `/` | Show keyboard shortcuts |
| `Cmd` `N` | New session |
| `Cmd` `Option` `1`–`9` | On the new session screen in the [current layout](#check-which-layout-you-have), select an environment |
| `Cmd` `Option` `0` | On the new session screen in the current layout, open the [**New environment** dialog](#create-a-saved-environment) |
| `Cmd` `W` | Close session |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab` | Switch between sessions |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Next or previous session |
| `Esc` | Stop Claude's response |
| `Tab` / `Right arrow` | [Accept the suggested prompt](#accept-a-suggested-prompt) in an empty prompt box |
| `Cmd` `Shift` `D` | Toggle diff pane |
| `Cmd` `Shift` `B` | Toggle Browser pane |
| `Cmd` `Shift` `S` | Select an element in the Browser |
| `Ctrl` `` ` `` | Toggle terminal pane |
| `Cmd` `\` | Close focused pane |
| `Cmd` `Ctrl` `W` | Take focused session out of [split view](#work-in-parallel-with-sessions) |
| `Cmd` `;` | Open side chat |
| `Ctrl` `O` | Cycle view modes |
| `Cmd` `Shift` `M` | Open permission mode menu |
| `Cmd` `Shift` `I` | Open model menu |
| `Cmd` `Shift` `E` | Open effort menu |
| `1`–`9` | Select item in an open menu |

These shortcuts apply to the Code tab. In Desktop, `Shift+Tab` doesn't cycle permission modes as it does in the terminal's [interactive mode](https://code.claude.com/docs/en/interactive-mode.md#keyboard-shortcuts).

### Check usage

To see how full this session's context window is, find your Code tab layout:

* **Current layout**: the header of the **Context** card in the [session details panel](#see-session-details) shows it as a percentage. Open the card to see what is using the window by category.
* **[Earlier layout](#check-which-layout-you-have)**: click the usage ring next to the model picker. Its popover shows your context window usage.

In either layout, type `/context` in the prompt box to print a per-category breakdown of this session's context window in the chat.

Both layouts have the usage ring next to the model picker. Click it to see your plan usage, which is shared across all your Claude Code surfaces.

## Let Claude use your computer

Computer use lets Claude open your apps, control your screen, and work directly on your machine the way you would. Ask Claude to interact with a desktop tool that has no CLI, or automate something that only works through a GUI. For running and testing iOS apps, Desktop opens the dedicated [iOS Simulator pane](https://code.claude.com/docs/en/desktop-ios-simulator.md) instead of controlling your screen; the pane works without enabling computer use.

> [!NOTE]
>
> Computer use is a research preview on macOS and Windows that requires a Pro or Max plan. It is not available on Team or Enterprise plans. The Claude Desktop app must be running. On macOS, computer use requires macOS 14 or later.

Computer use is off by default. [Enable it in Settings](#enable-computer-use) before Claude can control your screen. On macOS, you also need to grant Accessibility and Screen Recording permissions.

On macOS, computer use can also run in the background: Claude works in the apps you've approved while you keep working.

> [!WARNING]
>
> Unlike the [sandboxed Bash tool](https://code.claude.com/docs/en/sandboxing.md), computer use runs on your actual desktop with access to whatever you approve. Claude checks each action and flags potential prompt injection from on-screen content, but the trust boundary is different. See the [computer use safety guide](https://support.claude.com/en/articles/14128542) for best practices.

### When computer use applies

Claude has several ways to interact with an app or service, and computer use is the broadest and slowest. It tries the most precise tool first:

* If you have a [connector](#connect-external-tools) for a service, Claude uses the connector.
* If the task is a shell command, Claude uses Bash.
* If the task is browser work and you have [Claude in Chrome](https://code.claude.com/docs/en/chrome.md) set up, Claude uses that.
* If the task is running or testing an iOS app, Claude uses the [iOS Simulator pane](https://code.claude.com/docs/en/desktop-ios-simulator.md), which doesn't use screen control.
* If none of those apply, Claude uses computer use.

The [per-app access tiers](#app-permissions) reinforce this: browsers are capped at view-only, and terminals and IDEs at click-only, steering Claude toward the dedicated tool even when computer use is active. Screen control is reserved for things nothing else can reach, like native apps, hardware control panels, or proprietary tools without an API.

### Enable computer use

Computer use is off by default. If you ask Claude to do something that needs it while it's off, Claude tells you it could do the task if you enable computer use in Settings.

**1. Update the desktop app**

Make sure you have the latest version of Claude Desktop. On macOS and Windows, download or update at [claude.com/download](https://claude.com/download); on Linux, update through your package manager ([instructions](https://code.claude.com/docs/en/desktop-linux.md)). Then restart the app.

**2. Turn on the toggle**

In the desktop app, open **Settings**, then:

* **If the Settings menu lists This computer**: go to **This computer > System**
* **Otherwise**: go to **Capabilities**

Under **Computer use**, turn on **Enable computer use**:

* **Windows**: the toggle takes effect immediately and setup is complete
* **macOS**: continue to the next step

If you don't see the toggle, confirm you're on macOS or Windows with a Pro or Max plan, then update and restart the app.

**3. Grant macOS permissions**

On macOS, grant two system permissions before the toggle takes effect:

* **Accessibility**: lets Claude click, type, and scroll
* **Screen Recording**: lets Claude see what's on your screen

The Settings page shows the current status of each permission. If either is denied, click the badge to open the relevant System Settings pane.

### App permissions

The first time Claude needs to use an app, a prompt appears in your session. Click **Allow for this session** or **Deny**. Approvals last for the current session, or 30 minutes in [Dispatch-spawned sessions](#sessions-from-dispatch).

The prompt also shows what level of control Claude gets for that app. These tiers are fixed by app category and can't be changed:

| Tier | What Claude can do | Applies to |
| :- | :- | :- |
| View only | See the app in screenshots | Browsers, trading platforms |
| Click only | Click and scroll, but not type or use keyboard shortcuts | Terminals, IDEs |
| Full control | Click, type, drag, and use keyboard shortcuts | Everything else |

Apps with broad reach, like terminals, Finder or File Explorer, and System Settings or Settings, show an extra warning in the prompt so you know what approving them grants.

In Settings, the **Computer use** section where you [turned computer use on](#enable-computer-use) includes these options:

* **Denied apps**: add apps here to reject them without prompting. Claude may still affect a denied app indirectly through actions in an allowed app, but it can't interact with the denied app directly.
* **Unhide apps when Claude finishes**: when computer use isn't running in the background, Claude hides your other windows while it works so it interacts with only the approved app. When Claude finishes, hidden windows are restored unless you turn this setting off.

## Manage sessions

Each session is an independent conversation with its own context and changes. You can run multiple sessions in parallel, branch off side chats, let Claude check on and message your other sessions, send work to the cloud, or let Dispatch start sessions for you from your phone.

### Work in parallel with sessions

Click **+ New** in the sidebar, or press **Cmd+N** on macOS or **Ctrl+N** on Windows, to work on multiple tasks in parallel. Press **Ctrl+Tab** and **Ctrl+Shift+Tab** to switch between sessions.

You can also open a second session next to the current session or in a window of its own:

* **Side by side**: hold **Option** on macOS or **Alt** on Windows and click a session in the sidebar, or right-click the session and select **Open in**, then **Split view**
* **In its own window**: hold **Cmd** on macOS or **Ctrl** on Windows and click a session, or right-click the session and select **Open in**, then **New window**

In the split view, the pane you opened or clicked last has focus, and the other pane is dimmed. To change which session a pane shows, click in that pane to give it focus, then click a session in the sidebar. To take the focused session out of the split view, press **Cmd+Ctrl+W** on macOS or **Ctrl+Alt+W** on Windows.

#### Run a session in its own worktree

In a project that's a Git repository, turn on **Worktree** before you start a session to run it in its own [Git worktree](https://code.claude.com/docs/en/worktrees.md), an isolated copy of the project. By default, **Worktree** is off and Claude works in the project folder itself. On the [current layout](#check-which-layout-you-have), turn on the **Worktree** button in the [row under the prompt box](#start-a-session).

* **With a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md)**: if the row under the prompt box shows the project folder control but no **Worktree** button, click that control and turn on **Worktree**
* **As the default for a [saved local or SSH environment](#create-a-saved-environment)**: set **Worktree** when you create or edit the environment
* **[Earlier layout](#check-which-layout-you-have)**: select the **worktree** checkbox beside the branch name, above the prompt box

Worktrees are stored in `<project-root>/.claude/worktrees/` by default. To store them in a custom directory instead:

* **Local sessions**: set **Worktree location** in **Settings > Code** or **Settings > Claude Code**
* **SSH sessions**: set **Worktree folder** on the [SSH connection](#choose-where-ssh-session-worktrees-go)

You can also set a **Branch prefix** in **Settings > Code** or **Settings > Claude Code**. Desktop prepends it to every worktree branch name, which is useful for keeping Claude-created branches organized.

To include gitignored files like `.env` in new worktrees, create a [`.worktreeinclude` file](https://code.claude.com/docs/en/worktrees#copy-gitignored-files-into-worktrees) in your project root. See [What worktrees share with the main checkout](https://code.claude.com/docs/en/worktrees.md#what-worktrees-share-with-the-main-checkout) for where a worktree session reads project settings, hooks, and skills.

> [!NOTE]
>
> Session isolation requires [Git](https://git-scm.com/downloads). Most Macs include Git by default. Run `git --version` in Terminal to check; if it prints a version number, Git is installed. If you run into Git errors, ask Claude in [Cowork](https://claude.com/product/cowork) to help troubleshoot your setup.

### Add folders to a session

Add folders before the session starts or while it runs:

* **Before a local session starts**: add the folders under **Folders** when you [create a saved environment](#create-a-saved-environment) or edit one, then [start the session from that saved environment](#use-edit-or-remove-a-saved-environment).
* **While a local or [SSH](#ssh-sessions) session runs**: click **+** next to the prompt box and select **Add folder**. Claude works in that folder itself, with no [worktree](#run-a-session-in-its-own-worktree).

### Archive a session

Before you archive a session whose worktree has uncommitted changes, see [Keep uncommitted changes when a session is archived](#keep-uncommitted-changes-when-a-session-is-archived). To archive a session, hover over it in the sidebar, open its menu, and select **Archive**. The session moves to your [archived sessions](#organize-and-find-sessions).

To have sessions archive themselves when their pull request merges or closes, turn on **Auto-archive after PR merge or close** in **Settings > Code** or **Settings > Claude Code**. Cloud sessions and sessions that are still running don't archive themselves.

#### Keep uncommitted changes when a session is archived

You can lose uncommitted changes in a session's worktree when the session is archived, so commit what you want to keep first:

* **If Desktop asks about the changes**: select **Archive anyway** to discard them, or cancel and commit them
* **If the only changes are untracked files**: commit the ones you want to keep before a pull request that Claude opened in the session merges, because Desktop can then delete them without asking
* **In any other case**: the worktree stays on disk with its changes. For a local session, Desktop removes both about 30 days after the session is archived or you last open it, whichever is later. To keep the changes, open the session from the [**Archived** tab](#organize-and-find-sessions) and select **Unarchive**

### Organize and find sessions

You group, sort, and find sessions from an icon in the sidebar's session list:

* **Current layout**: hover over a heading in the session list to show the **Group and sort** icon, then click it. To find archived sessions, select **View all**, the menu's last row, then open the **Archived** tab.
* **[Earlier layout](#check-which-layout-you-have)**: the **Filter** icon shows without hovering. Click it to arrange the list with **Group by** or **Sort by**. To show archived sessions, select **Status**, then **Archived**.

To rename a session, open it and click the session title in the title bar.

### Check and free up context

To check context usage, see [Check usage](#check-usage). When context fills up, Claude automatically summarizes the conversation and continues working. You can also type `/compact` to trigger summarization earlier and free up context space. See [the context window](https://code.claude.com/docs/en/how-claude-code-works.md#the-context-window) for details on how compaction works.

### Get notified when a session finishes

The desktop app sends an OS notification when a Code session finishes a task and you aren't currently viewing that session. For sessions that belong to a [project](https://code.claude.com/docs/en/claude-projects.md#see-what-needs-you-in-overview), you get the project's notifications instead.

### Ask a side question without derailing the session

A side chat lets you ask Claude a question that uses your session's context but doesn't add anything back to the main conversation. Use it when you want to understand a piece of code, check an assumption, or explore an idea without steering the session off course.

Press **Cmd+;** on macOS or **Ctrl+;** on Windows to open a side chat, or type `/btw` in the prompt box. The side chat can read everything in the main thread up to that point. When you're done, close the side chat and continue the main session where you left off.

Side chats are available in local, SSH, and WSL sessions. The desktop app doesn't save side chats to disk, so you can't return to one after you close the app.

### Watch background tasks

The tasks pane shows the background work running inside the current session: subagents, background shell commands, and [dynamic workflows](https://code.claude.com/docs/en/workflows.md). Once the session has background work, open the pane with **Background tasks** in the title bar's **⋮** menu.

Click any entry to see its output in the subagent pane or stop it. To see what other sessions are doing, use the [sidebar](#work-in-parallel-with-sessions), or ask Claude to [check on them for you](#work-across-sessions).

### Work across sessions

Claude can list your other Code tab sessions, read what each has been doing, and send messages between them. Ask in plain language: "which session touched the auth refactor?", "what did the API session conclude?", or "tell the payments session the schema changed".

You can also ask Claude to rename or archive a session. For example, ask it to archive the sessions whose PRs have merged.

Through this surface, Claude sees only the sessions the desktop app runs itself: local, [SSH](#ssh-sessions), and [WSL](https://code.claude.com/docs/en/desktop-wsl.md) sessions in the Code tab. Claude doesn't see cloud sessions, or sessions you started from the terminal CLI or the VS Code extension, even in worktrees of the same project, so with nine terminal worktrees open and two desktop sessions, Claude answering in one of them reports the one other desktop session. Claude never lists the session you're asking from. By default it sees the 20 most recently active sessions and skips archived sessions unless you ask for them. [Cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging.md) separately lets Claude message [your other Claude Code sessions](https://code.claude.com/docs/en/cross-session-messaging.md#see-which-sessions-claude-can-reach), including terminal sessions.

When Claude messages another session through this surface, Claude Code shows it there as a card labeled with the sending session's title and a link back, so you can always tell where a message came from. If the receiving session is mid-task, Claude Code holds the message and Claude reads it once the current work finishes. The receiving Claude can reply, and Claude Code delivers the reply back through this surface. Claude can't deliver to an archived session, and tells you when a message doesn't go through.

Claude Code applies three safety behaviors across sessions:

* You get an approval card before Claude archives a session, except in Auto mode and Bypass permissions mode, where Claude can archive a session without one. To be asked, switch to Manual.
* Claude Code checks each message from this surface against the receiving session's [inbound controls](https://code.claude.com/docs/en/cross-session-messaging.md#control-inbound-messages), even when the receiving session doesn't have [cross-session messaging](https://code.claude.com/docs/en/cross-session-messaging.md#availability) itself. If you set [`crossSessionInbound`](https://code.claude.com/docs/en/settings-reference#crosssessioninbound) to `refuse` in the receiving session, Claude Code drops messages from this surface. Claude Code reports the refusal to the Claude desktop app. Before v2.1.234, Claude Code dropped every message from this surface to a receiving session without cross-session messaging.
* Claude Code quotes each incoming message and attributes it to the session that sent it, and Claude still follows the receiving session's own permission settings when acting on one.

### Start a task that Claude suggests

When Claude notices something worth fixing outside your current task, it suggests that work as a task. In local and SSH sessions on the [current layout](#check-which-layout-you-have), the suggestion is a card in the chat, and its buttons either start the task or keep it in this session:

* **Start**: starts the task in another session. By default the task runs in the current session's environment. The card then shows the started session's state, and the [sidebar](#work-in-parallel-with-sessions) lists the started session under the current session.
* **Do it here**: sends the task to the current session as a message
* **Options**: review or change settings such as the environment, model, [worktree](#run-a-session-in-its-own-worktree), and permissions before you click **Start**
* **Start all**: when the card lists several tasks, starts each task in its own session without waiting for one task to finish before starting the next

In cloud sessions, and in local and SSH sessions on the earlier layout, the suggestion is a **Suggested task** card. To start the task where the card's main button says, for example **Send to cloud** or **Start with worktree**, click that button. Click the caret beside the main button for other ways to start the task, including **Do it here**.

### Run long-running tasks in the cloud

For large refactors, test suites, migrations, or other long-running tasks, select an environment under **Cloud** in the [environment selector](#start-a-session) when starting a session. Cloud sessions run on Anthropic-managed infrastructure by default and continue even if you close the app or shut down your computer. Check back anytime to see progress or steer Claude in a different direction. You can also monitor cloud sessions from [claude.ai/code](https://claude.ai/code) or the [Claude mobile app](https://code.claude.com/docs/en/mobile.md).

Cloud sessions also support multiple repositories. Choose the repositories:

* **Current layout**: in the row under the prompt box, once you select a cloud environment.
* **[Earlier layout](#check-which-layout-you-have)**: above the prompt box. To add another repository, click **+** beside the selected one.

See [Use Claude Code in the cloud](https://code.claude.com/docs/en/claude-code-on-the-web.md) for more on how cloud sessions work. When one body of work needs many cloud sessions, use a [project](https://code.claude.com/docs/en/claude-projects.md): Claude starts and tracks the sessions for you from one conversation. [Create a project](https://code.claude.com/docs/en/claude-projects.md#create-a-project) has the steps.

> [!NOTE]
>
> A task in an [SSH session](#ssh-sessions) can also [keep going while Desktop is disconnected](#keep-a-task-running-while-desktop-is-disconnected), but with a Claude account it can stop when its sign-in expires.

### Continue in another surface

To continue a session somewhere else, open the session menu from the caret beside the session title or from the session's row in the sidebar, then select **Open in**:

* Select **Cloud** to continue the session as a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md), with your conversation carried over as a summary. Before you confirm, the dialog states whether your files move too and whether this session is archived once the cloud one is ready. You can't move a session that runs over [SSH](#ssh-sessions) or in [WSL](https://code.claude.com/docs/en/desktop-wsl.md) this way.
* Select an installed editor or your file manager to open the session's folder on disk there.

### Control which sessions appear on your other devices

A local session shows up on your other devices once [Remote Control](https://code.claude.com/docs/en/remote-control.md) connects it. A connected session appears in the session list at [claude.ai/code](https://claude.ai/code) and in the Claude apps on devices signed in to your claude.ai account.

A local session connects when you turn Remote Control on for it, or when it connects automatically as it starts:

* **You turn it on for that session**: with the session's **Remote Control** switch, or by typing `/remote-control` in its prompt box.
* **It connects when it starts**: new sessions connect automatically while **Connect new sessions to Remote Control** is on in **Settings > Code** or **Settings > Claude Code**. If you've never changed that setting, Desktop follows [`remoteControlAtStartup`](https://code.claude.com/docs/en/settings-reference#remotecontrolatstartup) in your user or managed settings, then your organization's default.

To see whether a session is connected, check the **Remote Control** switch in the **Environment** card of its [session details panel](#see-session-details).

To keep sessions off your other devices, turn Remote Control off at the level you need:

* **One session**: turn off its **Remote Control** switch. In a session that connected when it started, typing `/remote-control` leaves Remote Control on and shows `Remote Control is already on. This session connected automatically when it started.` Click **Turn off** on that line to disconnect.
* **New Desktop sessions on this computer**: turn off **Connect new sessions to Remote Control** in **Settings > Code** or **Settings > Claude Code**. If it already shows off, turn it on and then off so Desktop saves your choice. Once saved, it takes precedence over `remoteControlAtStartup` and the defaults.
* **Any session on this computer, including the CLI**: set [`disableRemoteControl`](https://code.claude.com/docs/en/settings-reference#disableremotecontrol) to `true` in `~/.claude/settings.json` to stop sessions from connecting. A session that was already connected when you saved the file stays connected until you turn Remote Control off for it.

To hide a session that already appears on your other devices, archive it in Desktop. Desktop archives the session's Remote Control copy too, so it leaves the default session list on those devices. To view or delete it there, see [Archive sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md#archive-sessions).

### Sessions from Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) is a persistent conversation with Claude that lives in [Cowork](https://claude.com/product/cowork). You message Dispatch a task, and it decides how to handle it.

A task can end up as a Code session in two ways: you ask for one directly, such as "open a Claude Code session and fix the login bug", or Dispatch decides the task is development work and spawns one on its own. Tasks that typically route to Code include fixing bugs, updating dependencies, running tests, or opening pull requests. Research, document editing, and spreadsheet work stay in Cowork.

#### Follow a session that Dispatch started

The session that Dispatch starts appears in the Code tab's sidebar with your other sessions. With the sidebar's [default grouping and sorting](#organize-and-find-sessions), look for the newest session in the group for the folder it runs in. You get a push notification on your phone when it finishes or needs your approval.

If you have [computer use](#let-claude-use-your-computer) enabled, Dispatch-spawned Code sessions can use it too. App approvals in those sessions expire after 30 minutes and re-prompt, rather than lasting the full session like regular Code sessions.

#### Set up Dispatch

For setup, pairing, and Dispatch settings, see the [Dispatch help article](https://support.claude.com/en/articles/13947068). Dispatch requires a Pro or Max plan and is not available on Team or Enterprise plans.

Dispatch is one of several ways to work with Claude when you're away from your terminal. For a comparison with the other options, see [Platforms and integrations](https://code.claude.com/docs/en/platforms.md#work-when-you-are-away-from-your-terminal).

## Extend Claude Code

Connect external services, add reusable workflows, customize Claude's behavior, and configure preview servers. To manage connectors, skills, and plugins in one place, click **Customize** in the sidebar. [Cowork](https://claude.com/product/cowork) in the Desktop app sources its skills, plugins, and connectors from this Customize configuration, which syncs through your claude.ai account, not from the CLI's `~/.claude` directory.

Claude Code also loads the skills and plugins enabled for your claude.ai account in terminal sessions where you sign in with the same account. See [Skills synced from claude.ai](https://code.claude.com/docs/en/skills.md#how-synced-skills-behave) and [Plugins synced from claude.ai](https://code.claude.com/docs/en/plugins/loading.md#synced-plugins).

### Connect external tools

Connectors are [MCP servers](https://code.claude.com/docs/en/mcp.md) with a graphical setup flow.

Click **+** next to the prompt box, before or during the session, to add connectors in a local or [SSH](#ssh-sessions) session with a Claude account. Select **Add connectors** to open the connector directory. If the menu shows **Connectors** instead, select it, then **Browse connectors**.

> [!NOTE]
>
> These cases are covered on other pages:
>
> * **Connectors is grayed out in a WSL session**: see [If the terminal or connectors are unavailable](https://code.claude.com/docs/en/desktop-wsl.md#check-for-the-terminal-and-connectors)
> * **Cloud sessions**: see [How connectors reach Claude Code](https://code.claude.com/docs/en/mcp.md#how-connectors-reach-claude-code)

Once connected, Claude can read your calendar, send messages, create issues, and interact with your tools directly. You can ask Claude what connectors are configured in your session. To manage or disconnect connectors, click **Customize** in the sidebar and open **Connectors**.

For integrations not listed in Connectors, add MCP servers manually via [settings files](https://code.claude.com/docs/en/mcp.md#installing-mcp-servers). You can also [create custom connectors](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Use skills

[Skills](https://code.claude.com/docs/en/skills.md) extend what Claude can do. Claude loads them automatically when relevant, or you can invoke one directly: type `/` in the prompt box or click the **+** button and select **Slash commands** to browse what's available. This includes [built-in commands](https://code.claude.com/docs/en/commands.md), your [custom skills](https://code.claude.com/docs/en/skills.md#create-your-first-skill), project skills from your codebase, and skills from any [installed plugins](https://code.claude.com/docs/en/plugins/install.md). Select one and it appears highlighted in the input field. Type your task after it and send as usual.

You can send a command while Claude is working, the same as any other message, and the session returns to idle once the turn finishes.

Local sessions load your personal skills from `~/.claude/skills/`. An [SSH](#ssh-sessions) session reads `~/.claude/skills/` from the remote host's home directory, not from your machine.

Local and cloud sessions also load the skills enabled for your claude.ai account, except local sessions when your organization sets [`disableSideloadFlags`](https://code.claude.com/docs/en/settings-reference#disablesideloadflags). Cloud sessions load them instead of `~/.claude/skills/`, as [Skills in Cowork and cloud sessions](https://code.claude.com/docs/en/skills.md#skills-in-cowork-and-cloud-sessions) describes.

### Install plugins

[Plugins](https://code.claude.com/docs/en/plugins/overview.md) are reusable packages that add skills, agents, hooks, MCP servers, and LSP configurations to Claude Code. You can install plugins from the desktop app without using the terminal.

In a local session or an [SSH session](#ssh-sessions), click **+** next to the prompt box and select **Add plugins** to open the plugin browser. If the menu shows **Plugins** instead, select it, then **Browse plugins**, or **Manage plugins** to enable, disable, or uninstall plugins.

You can scope plugins to your user account, a specific project, or local-only. If your organization manages plugins centrally, those plugins are available in desktop sessions the same way they are in the CLI, except the ones the desktop app [withholds under `disableSideloadFlags`](https://code.claude.com/docs/en/settings-reference#disablesideloadflags).

The plugin browser is not available in cloud sessions, and plugins you install from the desktop app aren't available for cloud sessions. A cloud session also doesn't install plugins that the repository's `.claude/settings.json` declares, as [What carries over from your setup](https://code.claude.com/docs/en/cloud-environments.md#what-carries-over-from-your-setup) explains. Plugins aren't available in WSL sessions. For the full plugin reference including creating your own plugins, see [plugins](https://code.claude.com/docs/en/plugins/overview.md).

### Configure preview servers

Claude automatically detects your dev server setup and stores the configuration in `.claude/launch.json` at the root of the folder you selected when starting the session. Preview uses this folder as its working directory, so if you selected a parent folder, subfolders with their own dev servers won't be detected automatically. To work with a subfolder's server, either start a session in that folder directly or add a configuration manually.

To customize how your server starts, for example to use `yarn dev` instead of `npm run dev` or to change the port, edit `.claude/launch.json`. The file supports JSON with comments.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

You can define multiple configurations to run different servers from the same project, such as a frontend and an API. See the [examples](#examples) below.

#### Auto-verify changes

When `autoVerify` is enabled, Claude automatically verifies code changes after editing files. It takes screenshots, checks for errors, and confirms changes work before completing its response.

Auto-verify is on by default. Disable it per-project by adding `"autoVerify": false` to `.claude/launch.json`, or turn off **Auto-verify changes** in the Browser pane's **⋮** menu.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

When disabled, preview tools are still available and you can ask Claude to verify at any time. Auto-verify makes it automatic after every edit.

#### Configuration fields

Each entry in the `configurations` array accepts the following fields:

| Field | Type | Description |
| - | - | - |
| `name` | string | A unique identifier for this server |
| `runtimeExecutable` | string | The command to run, such as `npm`, `yarn`, or `node` |
| `runtimeArgs` | string\[] | Arguments passed to `runtimeExecutable`, such as `["run", "dev"]` |
| `port` | number | The port your server listens on. Defaults to 3000 |
| `cwd` | string | Working directory relative to your project root. Defaults to the project root. Use `${workspaceFolder}` to reference the project root explicitly |
| `env` | object | Additional environment variables as key-value pairs, such as `{ "NODE_ENV": "development" }`. Don't put secrets here since this file is committed to your repo. For secrets, see [Set environment variables for dev servers](#set-environment-variables-for-dev-servers). |
| `autoPort` | boolean | How to handle port conflicts. See [Port conflicts](#port-conflicts) |
| `program` | string | A script to run with `node`. See [when to use `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable) |
| `args` | string\[] | Arguments passed to `program`. Only used when `program` is set |
| `url` | string | The address the preview opens instead of `http://localhost:<port>`. See [open the preview at a specific URL](#open-the-preview-at-a-specific-url) |

##### When to use `program` vs `runtimeExecutable`

Use `runtimeExecutable` with `runtimeArgs` to start a dev server through a package manager. For example, `"runtimeExecutable": "npm"` with `"runtimeArgs": ["run", "dev"]` runs `npm run dev`.

Use `program` when you have a standalone script you want to run with `node` directly. For example, `"program": "server.js"` runs `node server.js`. Pass additional flags with `args`.

##### Open the preview at a specific URL

By default, the preview opens `http://localhost:<port>`. Set `url` when your server needs a different address. Common cases are servers that require local HTTPS, apps that use `*.localhost` subdomains, and apps that sign you in through a redirect.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 8443,
      "url": "https://localhost:8443"
    }
  ]
}
```

Localhost addresses open directly, exactly like the default port address. This includes `localhost`, any `*.localhost` subdomain, `127.0.0.1`, and `::1`. For security, a localhost `url` must be your server's origin alone, with no path or query. Its port must match the entry's port. To show a specific page, ask Claude to navigate there after the preview opens. A localhost `url` with a path, query, or mismatched port is reported as a configuration error that names the url and shows the fix.

For any other address, Desktop asks for your permission the first time the preview opens it, the same as when you browse to a new site in the preview. External addresses may include paths. Choose **Always allow** to skip the prompt for that site in the future. Organization policies that restrict external sites in the preview still apply.

To preview a server you already run yourself, set `url` without a command. Claude attaches the preview to your running server instead of starting one:

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "url": "https://app.localhost:3000"
    }
  ]
}
```

The `url` must be `http` or `https`, and must not contain a username or password.

#### Port conflicts

The `autoPort` field controls what happens when your preferred port is already in use:

* **`true`**: Claude finds and uses a free port automatically. Suitable for most dev servers.
* **`false`**: Claude fails with an error. Use this when your server must use a specific port, such as for OAuth callbacks or CORS allowlists.
* **Not set (default)**: your server gets the next free port, as with `true`, except in the one case below. Before Claude Desktop v2.37337.0, Claude asks whether the server needs that exact port instead, then saves your answer in `launch.json`.

If your preferred port is in use and `autoPort` is unset, your server stays stopped when all of these hold:

* You start the server through an `npm`, `yarn`, `pnpm`, or `bun` script.
* Your preferred port is hardcoded in that script, or Claude can't inspect the script.
* You don't pass the port in `runtimeArgs`.

In that case, free the port, remove the hardcoded value, or change `port` to match the script. Setting `"autoPort": true` instead works only for a script that reads `PORT`.

Have your server read its port from the `PORT` environment variable, which carries the assigned port. When Claude moves your server to a different port, it also rewrites a `--port` or `-p` value in `runtimeArgs` to match.

#### Examples

These configurations show common setups for different project types:

**Next.js**

This configuration runs a Next.js app using Yarn on port 3000:

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "web",
      "runtimeExecutable": "yarn",
      "runtimeArgs": ["dev"],
      "port": 3000
    }
  ]
}
```

**Multiple servers**

For a monorepo with a frontend and an API server, define multiple configurations. The frontend uses `autoPort: true` so it picks a free port if 3000 is taken, while the API server requires port 8080 exactly:

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "frontend",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "cwd": "apps/web",
      "port": 3000,
      "autoPort": true
    },
    {
      "name": "api",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "start"],
      "cwd": "server",
      "port": 8080,
      "env": { "NODE_ENV": "development" },
      "autoPort": false
    }
  ]
}
```

**Node.js script**

To run a Node.js script directly instead of using a package manager command, use the `program` field:

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "server",
      "program": "server.js",
      "args": ["--verbose"],
      "port": 4000
    }
  ]
}
```

## Environment configuration

The environment you pick when [starting a session](#start-a-session) determines where Claude executes and how you connect:

* **Local**: runs on your machine with direct access to your files
* **Cloud**: runs on Anthropic-managed infrastructure by default. Sessions continue even if you close the app.
* **SSH**: runs on a remote machine you connect to over SSH, such as your own servers, cloud VMs, or dev containers. A running task can [keep going while Desktop is disconnected](#keep-a-task-running-while-desktop-is-disconnected), but with a Claude account it can stop when its sign-in expires.
* **WSL** (Windows): runs inside a [WSL 2 distribution](https://code.claude.com/docs/en/desktop-wsl.md) on your machine, using its Linux toolchain and native paths

### Create a saved environment

A saved environment is an entry in the [environment selector](#start-a-session) that records where Claude runs, so you can start later sessions there. A local or SSH environment also holds the folders Claude works in. Saved local and SSH environments are part of the [current layout](#check-which-layout-you-have), so if you don't see them, check which layout you have and how to get the current one.

**1. Open the New environment dialog**

Open the environment selector under the prompt box and select **New environment** at the bottom of its menu.

**2. Choose where Claude runs**

Select the **Local**, **SSH**, or [**Cloud**](#cloud-sessions) tab and fill in the form on that tab. On the **SSH** tab, choose a [connection](#ssh-sessions) and a folder on the remote machine.

**3. Save the environment**

Select **Create environment**, or **Add environment** on the **Cloud** tab.

#### Environments that Desktop creates for you

If the environment selector lists local or SSH environments you didn't create, Desktop created them for you. The first time you open the Code tab in the [current layout](#check-which-layout-you-have), Desktop creates up to eight environments. The environments come from the local and SSH folders you used most in the last month. You can [edit or delete them](#use-edit-or-remove-a-saved-environment).

#### Use, edit, or remove a saved environment

Find the environment's entry in the [environment selector](#start-a-session):

* **Start a session**: select the entry.
* **Edit or delete**: hover over the entry and click the gear icon. To delete a local or SSH environment, click **Delete environment** in **Edit environment**.
* **Archive cloud environments**: see [Archive an environment](https://code.claude.com/docs/en/cloud-environments.md#archive-an-environment).

### Environment variables in local sessions

To set an environment variable for a local session, [add it to a saved local environment](#set-environment-variables-for-local-sessions), then start a new session from that environment.

Variables such as `PATH` and `CLAUDE_CONFIG_DIR` have their own instructions:

| Variable | What to do instead |
| :- | :- |
| `PATH`, the folders your system searches for programs such as `npm` | See [Session not finding installed tools](#session-not-finding-installed-tools). On Windows, Desktop doesn't read PowerShell profiles, so set `PATH` in your user or system environment variables, then quit and reopen Desktop. |
| A variable for an MCP server from [`claude_desktop_config.json`](#mcp-servers-from-the-claude-desktop-chat-app) | Quit Desktop, set it in that server's `env` block, then reopen Desktop |
| [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars#variables) or [`CLAUDE_CODE_TMPDIR`](https://code.claude.com/docs/en/env-vars#variables) | Set it in [one of the places you'd set a variable for dev servers](#set-environment-variables-for-dev-servers), then quit and reopen Desktop |
| `API_TIMEOUT_MS`, `ANTHROPIC_BASE_URL`, or another variable Desktop sets itself | See [Environment variables Desktop sets itself](#environment-variables-desktop-sets-itself) |

On macOS or Linux, if a variable you set with `export` is missing or wrong in a command Claude runs, see [Exported variable missing or wrong in commands Claude runs](#exported-variable-missing-or-wrong-in-commands-claude-runs).

#### Set environment variables for local sessions

Add the variables to a saved local environment and start your sessions from it. Desktop [sets some variables itself](#environment-variables-desktop-sets-itself), such as `API_TIMEOUT_MS`, and your sessions get its value for those instead of yours.

> [!NOTE]
>
> If a new session shows no environment under the prompt box, you have the [earlier layout](#check-which-layout-you-have), which has no saved local environments. Use the [local environment editor](#use-the-local-environment-editor) instead.

**1. Open a local environment's form**

* **To create a saved local environment**: select [**New environment**](#create-a-saved-environment) at the bottom of the environment selector's menu, then the **Local** tab
* **To change one you already have**: in the environment selector, hover over a saved environment under **Local** and click the gear icon to open [**Edit environment**](#use-edit-or-remove-a-saved-environment)

**2. Enter the variables**

Select **Environment variables**, enter one `KEY=value` per line, and select **Done**.

**3. Save the environment**

Select **Create environment** or **Save**.

Only sessions you start from that environment get the variables.

To set a variable for every local session, add it to the [`env` key](https://code.claude.com/docs/en/env-vars#set-variables-in-settings-files) in your `~/.claude/settings.json` file. Claude Code [ignores the value](https://code.claude.com/docs/en/settings-reference.md#how-env-values-interact-with-your-shell) if that variable is already in the environment Desktop starts the session with. See [environment variables](https://code.claude.com/docs/en/env-vars.md) for the full list of supported variables.

#### Set environment variables for dev servers

To give a dev server a secret without committing it to [`launch.json`](#configure-preview-servers), set it in one of these places, then restart Desktop:

* **macOS and Linux**: export it in your shell profile
* **Windows**: add it to your user or system environment variables
* **Any platform**: save it in the [local environment editor](#use-the-local-environment-editor), if you can open it

Dev servers don't get the variables you add to a [saved environment](#create-a-saved-environment) or to `~/.claude/settings.json`.

#### Use the local environment editor

To open the local environment editor, click the gear icon on the entry for your own computer, not the one on a saved environment:

* **Selector under the prompt box**: hover over the entry for your computer, the first under **Local**. If a gear icon appears, click it. If not, the editor isn't available, so set the variable for [local sessions](#set-environment-variables-for-local-sessions) or [dev servers](#set-environment-variables-for-dev-servers) another way.
* **Selector above the prompt box**: hover over **Local** and click the gear icon

Enter one `KEY=value` per line and select **Save changes**. Variables you save here are stored encrypted on your machine. Local sessions get them, except any variable that [Desktop sets itself](#environment-variables-desktop-sets-itself), such as `API_TIMEOUT_MS`. Restart Desktop to give your variables to dev servers.

#### Exported variable missing or wrong in commands Claude runs

If a command Claude runs on macOS or Linux doesn't get a variable you set with `export` in `~/.zshrc` or `~/.bashrc`, or gets the wrong value, try these in order:

**1. Start a new session**

Ask Claude to run the command again.

**2. Quit and reopen Desktop**

Then start a new session.

**3. Check your saved variables**

If a command gets the wrong value, check whether you also set the variable in a [saved environment](#use-edit-or-remove-a-saved-environment) or the [local environment editor](#use-the-local-environment-editor). If so, change the value there and start a new session.

**4. Use a saved environment**

Add the variable to a [saved local environment](#set-environment-variables-for-local-sessions), then start a new session from that environment. For a variable such as `PATH`, `CLAUDE_CONFIG_DIR`, or `API_TIMEOUT_MS`, follow [its own instructions](#environment-variables-in-local-sessions) instead.

Before v2.1.304, Claude Code doesn't pass exported variables to commands, so [check which version the session runs](#claude-code-version-in-the-code-tab).

#### Environment variables Desktop sets itself

If you set `API_TIMEOUT_MS` or `ANTHROPIC_BASE_URL` and nothing changed in your local sessions, it's because Desktop sets those [variables](https://code.claude.com/docs/en/env-vars.md#variables), among others, itself. A local session gets Desktop's value whether you set yours in your shell profile, your Windows user or system variables, the local environment editor, or a saved environment. Moving yours to a settings file doesn't help, because Claude Code [ignores that value](https://code.claude.com/docs/en/settings-reference.md#how-env-values-interact-with-your-shell) in a local session.

* `API_TIMEOUT_MS`: a local session gets `900000`, which is 15 minutes. For a longer timeout, [install the Claude Code CLI](https://code.claude.com/docs/en/quickstart.md) and use it instead of Desktop. [Set the variable in your shell](https://code.claude.com/docs/en/env-vars.md#set-variables-in-your-shell) and run `claude` in your terminal.
* `ANTHROPIC_BASE_URL`: a local session gets Anthropic's API host when you're signed in with a Claude account. To use a gateway, set up Desktop's [third-party inference configuration](https://code.claude.com/docs/en/llm-gateway-connect.md#desktop-app) instead.

#### Turn off extended thinking

[Extended thinking](https://code.claude.com/docs/en/model-config.md#extended-thinking) is enabled by default, which improves performance on complex reasoning tasks but uses additional tokens. To turn it off, set `MAX_THINKING_TOKENS` to `0` in a [saved local environment](#set-environment-variables-for-local-sessions) or the [local environment editor](#use-the-local-environment-editor). Thinking then turns off on the Anthropic API, except on Opus 5.5, Sonnet 5.5, Haiku 5.5, and the Fable models, which always use extended thinking.

On Opus 5, also select effort `high` or lower before you start the session. In the [current layout](#check-which-layout-you-have), open the model picker and select a level under **Effort**. If you started the session at a higher level, start a new one at `high` or lower.

#### Fixed thinking budgets

On models with [adaptive reasoning](https://code.claude.com/docs/en/model-config.md#adjust-effort-level), Claude Code ignores the number itself in a positive `MAX_THINKING_TOKENS` value because adaptive reasoning controls thinking depth instead. On Opus 4.6 and Sonnet 4.6, set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` to `1` to use a fixed thinking budget; Fable models, Sonnet 5 and later, Haiku 5.5, and Opus 4.7 and later always use adaptive reasoning and have no fixed-budget mode.

### Local sessions on managed devices

If the entry for your computer is grayed out in the environment selector, with the tooltip **Disabled by your organization**, your administrator has [turned off local sessions](#managed-settings). On Windows the [WSL](https://code.claude.com/docs/en/desktop-wsl.md) entry, whose availability on managed devices is [governed separately](https://code.claude.com/docs/en/admin-setup.md#wsl-sessions-in-claude-code-desktop), is grayed out the same way.

New sessions default to the first SSH connection if one is configured. If you try to continue an existing local session, Desktop shows a message that local sessions aren't available on this device. [Saved local environments](#create-a-saved-environment) show this error when you select one: `Couldn’t switch environments: the Local environment isn’t available anymore.` Choose an [SSH](#ssh-sessions) or [cloud](#cloud-sessions) environment instead, or contact your IT team.

### Cloud sessions

Cloud sessions continue in the background even if you close the app. Usage counts toward your [subscription plan limits](https://code.claude.com/docs/en/costs.md) with no separate compute charges.

To add, edit, or [archive](https://code.claude.com/docs/en/cloud-environments.md#archive-an-environment) a cloud environment, open the [environment selector](#start-a-session):

* **Add an environment**: select **New environment** at the bottom of the selector's menu, then the **Cloud** tab of the [**New environment** dialog](#create-a-saved-environment)
* **Edit or archive one of your own environments**: hover over it and click the gear icon

See [Configure cloud environments](https://code.claude.com/docs/en/cloud-environments.md) for details on configuring network access and environment variables.

### SSH sessions

SSH sessions let you run Claude Code on a remote machine while using the desktop app as your interface. This is useful for working with codebases that live on cloud VMs, dev containers, or servers with specific hardware or dependencies.

> [!NOTE]
>
> If you use Desktop with a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md), SSH sessions need their own setup. See [SSH remote sessions in Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions).

Add an SSH connection in the [**New environment** dialog](#create-a-saved-environment), then start a session on that connection. If a new session shows no environment under the prompt box, you have the earlier layout. See [Check which layout you have](#check-which-layout-you-have).

**1. Open the New environment dialog**

Before you start a session, open the environment selector under the prompt box and select **New environment** at the bottom of its menu.

**2. Add the connection**

On the **SSH** tab of the **New environment** dialog, open the **Host** list, select **Add SSH connection…**, and fill in the connection details:

* **Name**: a friendly label for this connection.
* **SSH host**: `user@hostname` or a host defined in `~/.ssh/config`.
* **SSH port**: defaults to 22 if left empty, or uses the port from your SSH config.
* **SSH key (optional)**: path to your private key, such as `~/.ssh/id_ed25519`. Leave empty to use your SSH config or SSH agent.
* **Worktree folder**: a folder on the remote machine, such as `~/worktrees`, where new sessions create their worktrees. Leave empty to use the [remote machine's default](#choose-where-ssh-session-worktrees-go).

Then select **Add SSH connection**.

**3. Start a session on the connection**

Select a folder on the remote machine and click **Create environment**. You keep the machine and folder together as a [saved environment](#create-a-saved-environment) for later sessions. Desktop selects it for the new session, so type your task and press **Enter**.

The remote machine can run Linux, macOS, or [Windows](#windows-remote-machines). Desktop installs Claude Code on the remote machine automatically the first time you connect. Once connected, SSH sessions support permission modes, connectors, plugins, and MCP servers.

#### Remote machine requirements for SSH sessions

A Linux or macOS remote machine needs a supported processor, an SSH server with SFTP, an install folder that isn't mounted `noexec`, a working shell, and network access. Check each requirement before you connect, or when a connection fails after you log in:

* **System**: an x86\_64 or arm64 processor. The machine also has to meet Claude Code's [system requirements](https://code.claude.com/docs/en/setup.md#system-requirements). On Linux, Claude Code needs glibc 2.17 or later, or musl. To see which one the machine has, run `ldd --version` there. On a musl-based distribution such as Alpine Linux, also install the [packages that Claude Code needs](https://code.claude.com/docs/en/setup.md#alpine-linux-and-musl-based-distributions).
* **SFTP**: the SSH server has to offer the SFTP subsystem, which a `Subsystem sftp` line in its `sshd_config` turns on. To check, connect to the same host and port with `sftp` in a terminal on your computer. A working server shows the `sftp>` prompt.
* **`MaxSessions 1` on the server**: to connect to a server whose `sshd_config` sets `MaxSessions 1`, do one of these:
  * **Your computer runs macOS or Linux**: update to Claude Desktop v3.1623.0 or later
  * **Your computer runs Windows**: make sure that Desktop [connects through the OpenSSH client](#use-your-ssh-configuration), because Desktop's built-in SSH client can't connect to that server
  * **You can change the server**: raise `MaxSessions`, for example to OpenSSH's default of 10
* **Logins with `MaxSessions 1`**: use a login that works without a prompt, such as a key that your SSH agent holds. Desktop logs in at least twice each time it connects or reconnects. Expect at least one more login for each [terminal](#run-commands-in-the-terminal) tab, and for each Desktop session in which you run commands that start with `!`. Expect none for commands that Claude runs.
* **One-time codes with `MaxSessions 1`**: if every login prompts you, as with one-time codes, `!` commands fail. Run those commands in a terminal tab instead, which prompts in its own pane.
* **Install folder**: Desktop installs a helper program and Claude Code under `~/.claude/remote/` in your home directory. It runs them from there, so that folder can't be on a file system mounted `noexec`. Allow about 1 GB of disk space in the home directory of each user who connects. For what that folder holds, see [Files and processes on the remote machine](#files-and-processes-on-the-remote-machine).
* **Shell**: the shell set for your account on the remote machine has to run commands sent over SSH, as Bash, Zsh, and `sh` do
* **Network**: Claude Code runs on the remote machine and makes its network requests from there, so the machine needs the [network access that Claude Code requires](https://code.claude.com/docs/en/network-config.md#network-access-requirements). If the machine can't download Claude Code, Desktop downloads it on your computer and uploads it. Claude Code's other requests still go out from the remote machine. On a Linux remote machine, if those requests need a proxy, [set it for SSH sessions](#set-a-proxy-or-a-ca-certificate-for-ssh-sessions).

#### Check a remote machine's host key

A host key is the key that a remote machine presents to prove which machine it is, and a fingerprint is a short form of that key. When you trust a key, your computer saves it and connects to whatever presents it, without asking again. Check a key before you trust it, because something may be intercepting the connection.

First find which machine the key belongs to, from where you see the fingerprint:

* **Desktop asks `Connect to <host> for the first time?`, or you selected Review new key**: the machine that Desktop names, `<host>`
* **Desktop asks `Connect through <jump host> for the first time?`**: the jump host, which is the machine that your connection passes through, not the machine that you want to reach
* **`ssh` asks or warns in a terminal**: the machine that its message names, which may not be the one that you typed

Get that machine's own fingerprint from the machine, not over the connection that you're checking:

* **Someone else manages the machine**: ask them for its host key fingerprint
* **You manage it, and it runs Linux or macOS**: run `ssh-keygen -lf /etc/ssh/ssh_host_<type>_key.pub` on it, at its console or over a connection that you already trust. For `<type>`, use the key type that Desktop or `ssh` shows beside the fingerprint, in lowercase: `ed25519` for `ED25519` or `ssh-ed25519`.

Then compare the machine's own fingerprint with the one that you were shown:

* **They match**: trust the key. Select **Trust and connect** or **Trust new key** in Desktop, or answer `yes` in the terminal.
* **They differ, or you can't check**: don't connect. Select **Cancel** in Desktop, or answer `no` in the terminal. If someone else manages the machine, tell them which fingerprint you were shown.

If a troubleshooting step sent you here, go back to that step after either result.

#### Set a proxy or a CA certificate for SSH sessions

If a Linux remote machine reaches the internet through a proxy or needs a CA certificate, add the [proxy and CA variables](https://code.claude.com/docs/en/network-config.md) under `env` in `~/.claude/settings.json` there. Add them even if you already export them in `~/.profile`, `~/.bash_profile`, `~/.zprofile`, or `~/.zshrc` on that machine.

In an SSH session, Claude Code doesn't get the variables from those files, even when `claude` in a terminal on that machine does. The session can then hang, or show **The connection from … to the API failed** or **Authentication failed**, and signing in again doesn't help.

**1. Add the variables**

For the CA file, use [`NODE_EXTRA_CA_CERTS`](https://code.claude.com/docs/en/network-config#custom-ca-certificates), because Claude Code doesn't trust a CA from `SSL_CERT_FILE` in `~/.claude/settings.json`. This example sets a proxy and a CA file:

```json ~/.claude/settings.json theme={null}
{
  "env": {
    "HTTPS_PROXY": "http://proxy.example.com:8080",
    "NODE_EXTRA_CA_CERTS": "/etc/ssl/certs/example-ca.pem"
  }
}
```

**2. Send your message again**

Send your message again, because a variable that you add or change in that file takes effect within seconds. Start a new session if it still fails.

##### Find a proxy or CA variable set elsewhere on the remote machine

Check whether the Linux remote machine sets the proxy or CA variable elsewhere, because sessions use that value and [ignore the one in any settings file](https://code.claude.com/docs/en/settings-reference.md#how-env-values-interact-with-your-shell):

**1. List the variables that the remote machine sets**

In a terminal on your computer, run `ssh devbox env`, with your own host.

**2. Change the variable where it is set**

If the list has the variable, change it in the file that sets it, such as `~/.zshenv`, `/etc/environment`, or `~/.bashrc` on the remote machine.

**3. Give sessions the new value**

Restart the remote machine, or quit Desktop and end the helper's processes, as in the first two steps to [remove the helper](#files-and-processes-on-the-remote-machine). Do this when no task is running, because either way interrupts Claude's work.

#### Use your SSH configuration

You can use your SSH configuration on macOS, Linux, and Windows when Desktop connects through the OpenSSH client on your computer:

* **macOS and Linux**: Desktop connects by running the OpenSSH client on your computer, so it uses your `~/.ssh/config`. Connecting through the OpenSSH client requires Claude Desktop v1.37937.0 or later.
* **Windows**: when Desktop connects through the OpenSSH client, it uses your `%USERPROFILE%\.ssh\config`. If you use a Claude account rather than a third-party provider, connecting through the OpenSSH client requires all of these:

  * Claude Desktop v2.2553.0 or later. To find your version, see [Check your version](#check-your-version).
  * Microsoft's OpenSSH 9.4 or later
  * Desktop installed with the download buttons at the top of this page, because Desktop from the Microsoft Store doesn't connect through the OpenSSH client

  If you can't meet these requirements, or you use a third-party provider, see [Connect on Windows without the OpenSSH client](#connect-on-windows-without-the-openssh-client).

With the OpenSSH client, enter a `Host` name from your configuration file in the **SSH host** field. Desktop then uses settings from that `Host` entry, such as `HostName`, `User`, `IdentityFile`, `CertificateFile`, `ProxyJump`, and `ProxyCommand`.

Before you add the connection, check the client and the entry in a terminal on your computer:

* **Client version on macOS and Linux**: run `ssh -V`. The client has to be OpenSSH 7.6 or later.
* **Client version on Windows**: Desktop tries the `ssh` on your `PATH` first, so run `ssh -V`. The client passes if the output shows `OpenSSH_for_Windows_` and 9.4 or later. If it doesn't pass, check the two folders that Desktop tries next: run `.\ssh.exe -V` in `C:\Windows\System32\OpenSSH`, then in `C:\Program Files\OpenSSH`.
* **No client passes on Windows**: add the **OpenSSH Client** optional feature in Windows and install pending Windows updates, or install [Microsoft's newer build](https://learn.microsoft.com/en-us/troubleshoot/windows-server/system-management-components/upgrade-in-box-openssh-to-latest-openssh-release). Then quit and reopen Desktop. To see whether Desktop found a usable OpenSSH client, look in [`ssh.log`](#get-desktops-logs-for-an-ssh-problem) for `Windows OpenSSH client:` and a version, or for `no usable Windows OpenSSH client`.
* **Entry**: on Windows, use the client that passed the version check. Run `ssh` with the `Host` name, such as `ssh devbox`. If that fails, fix the entry first.

You can leave the **SSH port** and **SSH key (optional)** fields empty. If you fill one in, Desktop uses it with the entry:

* **SSH port**: a value here overrides the entry's `Port`
* **SSH key (optional)**: with the OpenSSH client, Desktop offers the key file you pick in addition to the entry's `IdentityFile` and the keys in your SSH agent. On Windows, pick a key in OpenSSH format, because `ssh` doesn't read a PuTTY `.ppk` file.

##### Connect on Windows without the OpenSSH client

On Windows, you connect through Desktop's built-in SSH client if your computer doesn't meet [the requirements for the OpenSSH client](#use-your-ssh-configuration). With a third-party provider, you connect through the built-in client by default, and your administrator can change that. For the setting, see [SSH remote sessions in Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions).

With the built-in client, you can still enter a `Host` name from your SSH configuration in the **SSH host** field if your `PATH` has an `ssh` command, with these limits:

* **Settings from the entry**: Desktop takes `HostName`, `User`, `Port`, and `IdentityFile`. It also takes `ProxyCommand` if an `sh` shell is on your `PATH`.
* **SSH key (optional)**: leave this field empty to keep the entry's `IdentityFile`, because a key file that you pick here replaces the `IdentityFile`
* **`CertificateFile` and `ProxyJump`**: Desktop ignores `CertificateFile`, and the connection fails if the entry sets `ProxyJump`. To use either setting, [connect through the OpenSSH client](#use-your-ssh-configuration).

##### Reach a machine behind a jump host

To reach a machine behind a jump host, also called a bastion, set `ProxyJump` or `ProxyCommand` in the entry. The following entry reaches `devbox.internal.example.com` through `bastion.example.com`:

```text ~/.ssh/config theme={null}
Host devbox
  HostName devbox.internal.example.com
  User alice
  ProxyJump bastion.example.com
```

Enter `devbox` in the **SSH host** field.

If your administrator [restricts SSH hosts](#allow-jump-hosts), the jump host has to be on the list too. Run `ssh -G bastion.example.com` in a terminal on your computer, and ask them to allow the `hostname` that it prints.

##### Reach a container on a remote machine

To run a session inside a container that publishes no SSH port, reach it with a `ProxyCommand`, because Desktop doesn't run the `RemoteCommand` of the entry you connect to. If your entry uses `RemoteCommand` to step into the container, the session runs on the machine that the entry logs in to, not in the container.

**1. Add the entry**

Add the following entry at the end of your `~/.ssh/config`, or directly above your first `Host *` entry if you have one. Replace the Docker container `devbox`, its user `dev`, and the machine `build.example.com` with your own. The entry's command starts an SSH server inside the container for each connection:

```text ~/.ssh/config theme={null}
Host devbox-container
  User dev
  ProxyCommand ssh build.example.com docker exec -i devbox /usr/sbin/sshd -i
```

**2. Prepare the container**

* Install the OpenSSH server, with a host key that stays the same when you rebuild the image or recreate the container
* Give the account named in `User` a way to log in, such as an `authorized_keys` file
* Check that the container meets the [remote machine requirements](#remote-machine-requirements-for-ssh-sessions)

**3. Check the allowlist**

If your administrator [restricts SSH hosts](#restrict-which-ssh-hosts-users-can-connect-to), run `ssh -G devbox-container` in a terminal on your computer. Ask them to allow the `hostname` that it prints, here `devbox-container`, in `sshHostAllowlist`. When they allow that name, they allow whatever your entry's `ProxyCommand` connects to.

**4. Test the entry, then connect**

Run `ssh devbox-container` in a terminal on your computer. Fix what it reports, and run it again until it opens a shell in the container without asking you anything:

* **If `ssh` asks for a password, passphrase, or code**: switch to a login that works without a prompt, such as a key that your SSH agent holds
* **If `ssh` reports `Cannot execute command-line and remote command.` or `Bad packet length`**: take `RemoteCommand` and `RequestTTY` out of your entry for `build.example.com`. After that, `ssh build.example.com` in a terminal on your computer opens a shell on that machine, not in the container.
* **If `ssh` reports `Connection closed by UNKNOWN port 65535`**: run `ssh build.example.com docker exec devbox /usr/sbin/sshd -t` in the same terminal.
  * If it prints `Missing privilege separation directory: /run/sshd`, create that folder in the container.
  * If it prints `no hostkeys available` and the container has host keys, add `-u root` after `exec` in this command and in the entry.

Then enter `devbox-container` in the **SSH host** field.

##### Use variables from your shell in a `ProxyCommand`

On macOS and Linux, to use an environment variable of your own in a `ProxyCommand` or `Match exec` command, export it in a shell startup file, such as `~/.zshrc`. Then quit and reopen Desktop. When Desktop starts, it reads what your login shell exports, and it keeps those values until you quit.

This requires Claude Desktop v2.37337.0 or later and an `env` command that accepts `-0`, which you can check by running `env -0` in a terminal on your computer.

> [!NOTE]
>
> If your shell sets temporary AWS credentials, [give the AWS CLI a profile](#use-aws-credentials-in-a-proxycommand) instead of exporting `AWS_*` variables.

##### Use AWS credentials in a `ProxyCommand` on macOS and Linux

If you set temporary AWS credentials in a shell startup file, a `ProxyCommand` that runs the AWS CLI can connect in a terminal and fail in Desktop. When your shell exports `AWS_SESSION_TOKEN`, `AWS_SECURITY_TOKEN`, or `AWS_CREDENTIAL_EXPIRATION`, `ssh` and your `ProxyCommand` in Desktop don't get the shell's AWS credentials, `AWS_REGION`, or `AWS_PROFILE`.

If the AWS CLI has no other source for a region or credentials, it fails with `You must specify a region` or `Unable to locate credentials`. To connect from Desktop, give the AWS CLI a profile that it reads from `~/.aws/config`:

**1. Add a profile with a region and a source of credentials**

This example adds a profile named `corp` that gets its credentials from a helper program:

```ini ~/.aws/config theme={null}
[profile corp]
region = us-east-1
credential_process = /full/path/to/your-credential-helper
```

* **`region`**: give the AWS Region of the machines you connect to
* **`credential_process`**: give the full path of a program that prints credentials in the [JSON form that AWS documents](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sourcing-external.html). Choose a program that needs no input from you, because the AWS CLI runs it at every connection, including reconnects while you're away.
* **IAM Identity Center**: add the profile's [IAM Identity Center settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html) in place of `credential_process`. Run `aws sso login --profile corp` in a terminal before you connect, and again when that sign-in lapses.

**2. Name the profile in the ProxyCommand**

This example adds `--profile` to the [command that AWS documents for Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-enable-ssh-connections.html):

```text ~/.ssh/config theme={null}
Host i-*
  ProxyCommand sh -c "aws ssm start-session --profile corp --target %h --document-name AWS-StartSSHSession --parameters 'portNumber=%p'"
```

**3. Connect again**

Run `ssh` with the host in a terminal to confirm that the entry still connects there, then connect from Desktop.

##### Raise the SSH connection timeout

If your SSH configuration sets no `ConnectTimeout` for the host, Desktop gives `ssh` 30 seconds to connect. Through a jump host or a `ProxyCommand`, that time includes the time the route takes to connect. If your route needs longer, add a higher value to the entry:

```text ~/.ssh/config theme={null}
Host devbox
  HostName devbox.internal.example.com
  User alice
  ProxyJump bastion.example.com
  ConnectTimeout 120
```

`ssh` uses the first value it finds for a host, so keep the entry above any `Host *` entry that sets `ConnectTimeout`. To confirm, run `ssh -G devbox` in a terminal on your computer. Its output includes `connecttimeout 120`. After you change the value, quit and reopen Desktop.

If the remote machine itself waits for an approval on your phone, approve within 45 seconds, whatever `ConnectTimeout` you set. You can't raise this limit, because Desktop sets `ServerAliveInterval` and `ServerAliveCountMax` itself, and `ssh` then closes a login in which the remote machine sends nothing for that long. If a jump host or a `ProxyCommand` waits for you instead, raise `ConnectTimeout` in the remote machine's entry to cover that time.

##### Fix a `Match host` block that only Desktop applies

If Desktop uses a setting that `ssh devbox` in a terminal doesn't, look for a `Match host` block above the entry's `HostName` line. In a terminal, `ssh` reads a block there before the `HostName` line, so it compares the block with `devbox`. Desktop gives `ssh` the `HostName` value on the command line, so `ssh` compares the block with that value.

To check, run `ssh -G` in a terminal on your computer with the entry's `HostName` and `User` values on the command line, as Desktop does:

```bash theme={null}
ssh -G -o HostName=devbox.internal.example.com -l alice devbox
```

Compare the output with that of `ssh -G devbox`. If the block's settings, such as `proxycommand`, show only in the first output, the block takes effect only in Desktop. To have Desktop skip it too, add `!originalhost devbox` to its `Match` line:

```text ~/.ssh/config theme={null}
Match host *.internal.example.com !originalhost devbox
```

To confirm, run the first command again. The block's settings no longer show in its output.

##### Forwarding settings that Desktop leaves off

On its connection to the remote machine, Desktop leaves `ForwardAgent`, `ForwardX11`, `LocalForward`, `RemoteForward`, `DynamicForward`, and `Tunnel` off, even where your SSH configuration turns them on. In the [terminal](#run-commands-in-the-terminal) or a `!` command, expect your forwarding settings to apply [only sometimes](#limits-while-desktop-is-disconnected), because Desktop can start a separate `ssh` there that follows them.

* **To reach a port on the remote machine**: [forward it yourself](#reach-a-port-on-the-remote-machine)
* **To use your own keys from the remote machine**: set up a credential on the remote machine itself, for example for `git push`

To keep Desktop from forwarding your SSH agent or a port, run `ssh -G devbox` in a terminal on your computer. Then run it again as Desktop can run it, with the `hostname` and `user` values that it prints, as in `ssh -G -o HostName=devbox.internal.example.com -l alice devbox`. The second output can show settings from a `Match` block that the first skips.

Look in both outputs for a `forwardagent` line that says anything but `no`, and for lines that begin with `localforward`, `remoteforward`, or `dynamicforward`. If you find one, remove that setting from your SSH configuration. Do the same for a host that your `ProxyCommand` reaches with `ssh`.

#### Reach a port on the remote machine

To open a server that runs on the remote machine, such as a dev server on port 3000, forward the port yourself. In a terminal on your computer, run `ssh` with `-L` and the host you connect to, such as `devbox`:

```bash theme={null}
ssh -N -L 3000:localhost:3000 devbox
```

If you filled in **SSH port** or **SSH key (optional)** on the connection, add `-p` or `-i` with the same value. Leave that command running, and open `http://localhost:3000` in a browser on your computer to reach port 3000 of the remote machine. If `ssh` prints `open failed: administratively prohibited`, ask the machine's administrator to allow TCP forwarding, which `AllowTcpForwarding` in the SSH server's `sshd_config` controls.

#### Windows remote machines

A Windows remote machine requires Claude Desktop v2.31226.0 or later.

Use Microsoft's OpenSSH Server. The machine can be x64 or ARM64. The shell that the SSH server starts can be `cmd.exe`, Windows PowerShell 5.1, or Git Bash.

Windows remote machines get less testing than Linux ones. Try your own work there before you rely on it.

Expect these limits, among others, on a Windows remote machine:

* **Terminal**: the [terminal](#run-commands-in-the-terminal) doesn't open in a session whose folder is a Windows path, such as `C:/projects/app`
* **Sandbox**: Claude Code runs there on native Windows, where it runs commands unsandboxed. See [where the sandbox runs](https://code.claude.com/docs/en/sandboxing.md).
* **Plugins**: Desktop doesn't copy a plugin that holds a file or folder name Windows can't store, such as a name with `:`. The session lists the plugins that Desktop left out.
* **MCP servers**: on some Windows remote machines, Claude's calls to MCP servers from `claude_desktop_config.json` go through Desktop, so Claude can't call their tools [while Desktop is disconnected](#limits-while-desktop-is-disconnected). Before Claude Desktop v2.37337.0, this holds on every Windows remote machine.
* **Worktrees**: worktrees go in `<project-root>/.claude/worktrees/`. If you [choose another folder](#choose-where-ssh-session-worktrees-go), Desktop ignores it.
* **Earlier messages**: if the SSH server's shell is `cmd.exe` or Windows PowerShell, you may have to connect before you see a session's earlier messages
* **Forks**: if the SSH server's shell is `cmd.exe` or Windows PowerShell, you can fork a session only at its first message
* **Running while disconnected**: a task [keeps running while Desktop is disconnected](#keep-a-task-running-while-desktop-is-disconnected) only if the SSH server lets a program outlive the connection that started it. To find out, [test the remote machine](#prepare-a-long-task).
* **Leftover processes**: after a session ends, check the machine for programs that Claude Code started, because they can keep running. The [background helper](#keep-a-task-running-while-desktop-is-disconnected) that Desktop installs doesn't stop on its own there.

#### Keep a task running while Desktop is disconnected

If your computer sleeps, you lose your network, or you quit Desktop, the task goes on until it finishes, needs you, or reaches one of the [limits](#limits-while-desktop-is-disconnected). Closing the lid counts as sleep. A restart of Desktop or of your computer, including for an update, counts as a quit.

Claude Code runs as a process on the remote machine, under a background helper that Desktop installs there, so it doesn't need your SSH connection to keep running. The behavior in this section requires Claude Desktop v2.31226.0 or later.

> [!WARNING]
>
> If you sign in to Desktop with a Claude account, don't count on a task to run overnight. Desktop renews that sign-in for the task only while Desktop is running and connected, so the task's sign-in can expire after you disconnect, and the task then stops. How much time is left when you disconnect varies, and it can be only a few minutes.
>
> The work done so far stays on the remote machine, and you can continue with a message when you return.
>
> If the task must run through the night:
>
> * [Keep your computer awake](https://code.claude.com/docs/en/desktop-scheduled-tasks.md#how-scheduled-tasks-run) and online, with the lid open and Desktop running
> * Use a login that works without a prompt, such as a key that your SSH agent holds, for the remote machine and for any jump host on the way. Desktop can then reconnect on its own after a drop.
>
> For a task that must run while your computer is asleep or off, start a [cloud session](#run-long-running-tasks-in-the-cloud) instead.

* **After sleep or a network loss**: you get the running task back if the process [still runs](#limits-while-desktop-is-disconnected) and Desktop can log in without a prompt. If it can't, [send a message](#reconnect-after-sleep-or-a-network-loss).
* **After a quit**: the task keeps running, but you lose it when the session opens again unless Desktop can rejoin its process. Check [when Desktop can rejoin](#reopen-a-session-after-you-quit-desktop) before you quit. If you lost the task, send a message to continue.

When you come back and the task isn't done, check for word that Desktop can't reconnect, an authentication error, or a waiting request:

* **Desktop can't reconnect**: the session says why, and a notification may say so too. Desktop may [need you to log in](#reconnect-after-sleep-or-a-network-loss).
* **Authentication error**: the [sign-in token or credential](#limits-while-desktop-is-disconnected) may have expired. With a Claude account, send a message to continue. With a third-party provider, see [SSH remote sessions in Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions).
* **Waiting request**: [answer it](#handle-requests-that-arrive-while-you-are-away)
* **None of these**: send a message to continue

##### Prepare a long task

* **Update first**: update Desktop before you start a long task. On macOS and Windows, Desktop can restart on its own to install an update that it has downloaded. That restart waits while Claude is working on an SSH task. By default, once the update has waited 72 hours, the restart can go ahead during the task if Desktop can [rejoin the task afterward](#reopen-a-session-after-you-quit-desktop).
* **Check before you quit**: you don't always get the running task back after a quit or restart, for example after some Desktop updates. For the cases, see [Reopen a session after you quit Desktop](#reopen-a-session-after-you-quit-desktop).
* **On an older version, leave Desktop open**: on Windows with Claude Desktop before v3.1623.0, you don't get the running task back after Desktop quits or restarts. The same is true with a third-party provider on macOS or Linux before v2.42304.0. In both cases, leave Desktop open during the task. To find your version, see [Check your version](#check-your-version).
* **Reduce requests**: choose a permission mode, rules, or hooks that [make the task wait for you less often](#handle-requests-that-arrive-while-you-are-away)
* **Check the jump host**: if your jump host asks for a sign-in, for example a push to a phone, switch to a login that works without a prompt. Otherwise Desktop can send another push each time it tries to reconnect.
* **Test the remote machine**: start a short task, quit Desktop while the task is still running, and open the session again well after the task should be done. If the task isn't finished and the session shows no authentication error, check the remote machine for [what can end a task](#limits-while-desktop-is-disconnected).
* **Keep commands out of Desktop's terminal**: if the remote machine [logs out idle terminals](#limits-while-desktop-is-disconnected), run your own commands from an SSH login outside Desktop

##### Limits while Desktop is disconnected

A task that you leave running can end when its sign-in expires, when the remote machine ends it, or when the helper stops or is replaced:

* **Sign-in token or credential**: with a Claude account, the task stops with an authentication error when the token expires. With a third-party provider, the same holds for a credential that expires, such as one from single sign-on or a credential helper. See [SSH remote sessions in Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions). With a Claude account, [keep Desktop running and connected](#keep-a-task-running-while-desktop-is-disconnected) so that it can renew the sign-in.
* **The remote machine**: if the remote machine restarts, or ends your processes when your SSH connection closes, the running task ends. Nothing starts it again while Desktop is disconnected. Linux machines where systemd-logind's `KillUserProcesses` is `yes` and applies to your user end your processes this way. To keep a task running there, ask the administrator to exempt your user, for example with `KillExcludeUsers`.
* **Idle terminals**: some Linux remote machines log out a terminal that nobody types in for a set time (systemd-logind's `StopIdleSessionSec`). With Desktop on macOS or Linux, a session's [terminal](#run-commands-in-the-terminal) and `!` commands share Desktop's SSH connection by default. That logout then ends the connection while Desktop is connected, and the running task can end with it. Closing the terminal pane doesn't prevent it, so [keep commands out of that terminal](#prepare-a-long-task).
* **Desktop updates**: if an update brings a new helper, Desktop replaces the helper on the remote machine at a later connection, which can end a task that still runs
* **Long absences**: on a Linux or macOS remote machine, if Desktop doesn't connect for 30 days, the helper stops and ends every Claude Code process that runs under it. Connect before then.

File edits and some tools can fail while Desktop is disconnected. If the task needs them, keep Desktop connected:

* **Worktrees**: in a session that uses a [worktree](#run-a-session-in-its-own-worktree), Desktop checks each file edit before Claude makes it. While Desktop is disconnected, each edit waits about 30 seconds and then fails. Shell commands still run. On a Linux or macOS remote machine, [edits can keep working](#worktree-edits-while-disconnected). If you aren't sure, start the session without a worktree.
* **Folder restrictions**: if your organization restricts which folders sessions may use, Desktop checks each file read, search, and edit, with or without a worktree. While Desktop is disconnected, each one waits up to 10 minutes and then fails.
* **Connectors**: [connectors](#connect-external-tools) and other tools that Desktop provides run through Desktop, so while it is disconnected each call fails after about 30 seconds
* **Workflows**: Desktop checks each new [workflow](https://code.claude.com/docs/en/workflows.md) before it starts, so while Desktop is disconnected a new one waits up to 10 minutes and then fails
* **MCP servers**: MCP servers that Claude Code starts on the remote machine don't run through Desktop, so Claude can still call their tools. Servers from `claude_desktop_config.json` are among them only if Desktop doesn't use its [built-in SSH client](#worktree-edits-while-disconnected). Otherwise, and on [some Windows remote machines](#windows-remote-machines), Claude can't call their tools while Desktop is disconnected.

> **When edits in a worktree keep working**
>
> On a Linux or macOS remote machine, the check doesn't go through Desktop, so edits inside the worktree keep working while Desktop is disconnected. Before Claude Desktop v2.37337.0, this holds on a Linux remote machine only.
>
> Edits still fail in some cases, including these:
>
> * **Built-in SSH client**: Desktop uses it, for example in a Microsoft Store install, on a Windows computer without Microsoft's OpenSSH 9.4 or later, or by default on Windows with a third-party provider
> * **Repository location**: the repository is your home directory, a folder above it, or `~/.claude`
> * **macOS paths**: on a macOS remote machine, the repository is under `/Volumes`, or a folder name in the path of the repository or the worktree has a `~` or a non-ASCII character
> * **Folder restrictions**: your organization restricts which folders sessions may use
> * **Corporate launcher**: before Claude Desktop v2.37337.0, you sign in with a Claude account, and your organization starts Claude Code on the remote machine through a [corporate launcher](https://code.claude.com/docs/en/corporate-launcher.md)
>
> A session without a worktree has no such check, unless your organization restricts which folders sessions may use.

##### Handle requests that arrive while you are away

If Claude needs your approval or asks you a question while Desktop is disconnected, Claude waits on the remote machine. The wait has no time limit of its own. When Desktop rejoins the process, it shows you the request. If Desktop starts a new process instead, you lose the request.

If a request that waited for you is gone when you come back, one cause is that Desktop restarted on its own, for example to install an update. You keep a request through a restart only if Desktop can rejoin the process, so check [when Desktop can rejoin](#reopen-a-session-after-you-quit-desktop) before you leave a task running.

If you lose a request, send a message to continue.

To reduce how often a task stops to wait for you, and to hear from it while you are away, set up any of these before you leave:

* **Auto mode**: choose [Auto mode](#choose-a-permission-mode) if [it is available to you](#auto-mode-availability). After repeated blocks, you are [asked again](https://code.claude.com/docs/en/permission-modes.md#when-auto-mode-falls-back).
* **Allow rules**: in your user settings file on the remote machine, `~/.claude/settings.json`, add [allow rules](https://code.claude.com/docs/en/permissions.md#manage-permissions) for the commands the task needs. If your organization [accepts permission rules from managed settings only](https://code.claude.com/docs/en/settings-reference.md#allowmanagedpermissionrulesonly), ask your administrator to add them to the [managed settings](#managed-settings) that reach the remote machine. For allow rules in a project's `.claude/settings.json`, see [Project allow rules and workspace trust](https://code.claude.com/docs/en/permissions.md#project-allow-rules-and-workspace-trust).
* **A hook that answers**: configure a [`PermissionRequest` hook](https://code.claude.com/docs/en/hooks#permissionrequest) in `~/.claude/settings.json` on the remote machine to allow or deny requests in your place
* **A hook that alerts you**: configure a [`Notification` hook](https://code.claude.com/docs/en/hooks#notification) with the `permission_prompt` matcher in the same file to send yourself a message when a request is waiting
* **A hook that tells you when Claude is done**: configure a [`Stop` hook](https://code.claude.com/docs/en/hooks#stop) in the same file to send yourself a message when Claude has finished responding. It doesn't run when an API error ends the turn. For that case, configure a [`StopFailure` hook](https://code.claude.com/docs/en/hooks#stopfailure).

If your organization [runs managed hooks only](https://code.claude.com/docs/en/settings-reference.md#allowmanagedhooksonly), ask your administrator to add the hook to the [managed settings](#managed-settings) that reach the remote machine.

Claude Code doesn't auto-approve [a few actions](https://code.claude.com/docs/en/permission-modes.md#actions-no-mode-auto-approves) in any permission mode, including Bypass permissions. Depending on the permission mode, Claude Code denies such an action or asks you, and the task then waits for your answer.

##### Reconnect after sleep or a network loss

If Desktop hasn't reconnected when you come back, send a message in the session. Desktop reconnects on its own only where it can log in without a prompt, for example with a key that your SSH agent holds.

* **Remembered password**: a password that you let Desktop remember also works without a prompt, but for a long absence prefer a key that your SSH agent holds. If sign-ins with that password break off or hang, Desktop can stop reconnecting and wait for you.
* **Any other prompt**: if the remote machine prompts for anything else, such as a one-time code, you can get a notification on your computer. Click the notification, or send a message in the session, and Desktop shows the prompt.

> **If a jump host asks for a sign-in, the outage is long, output is missing, or the process is gone**
>
> * **Jump host, pushes stop while you're away**: this can happen with Desktop on macOS or Linux when nobody answers a jump host's sign-in, for example a push to a phone. Desktop then stops reconnecting while nobody is at your computer. When you unlock or use the computer, you can get another push, because Desktop can try again. After three unanswered attempts it waits until you retry or send a message.
> * **Jump host, pushes keep coming**: where Desktop can't tell that nobody answers, as with Desktop on Windows, it keeps trying while it has a process to rejoin, whether or not that process still runs. You can get another push with each attempt. To end the attempts, quit Desktop, which [can cost you the running task](#reopen-a-session-after-you-quit-desktop).
> * **Long outage**: Desktop slows to about one attempt every five minutes. To reconnect sooner, retry in the session or send a message, which Desktop delivers once it is connected.
> * **Missing output**: while Desktop is disconnected, the helper keeps each session's most recent Claude Code output in a 16 MiB buffer and drops older output. After Desktop reconnects, the session can show `Loading recent output from <host>…`. If Desktop can't load all of the output, you see the row `Some output produced while you were disconnected may be missing here.` The row doesn't mean that the task stopped.
> * **Process gone**: the process ended while Desktop was disconnected, as when the remote machine restarts. Desktop can then start a new one from the conversation's saved history and tell Claude to continue the task. If the task stays stopped, send a message. With a third-party provider, update to Claude Desktop v2.42304.0 or later, because earlier versions never continue the task on their own.

##### Reopen a session after you quit Desktop

After you quit Desktop, the task keeps running on the remote machine, but it stops when the session opens again unless Desktop can rejoin its process. While Desktop is closed, the task runs until it finishes, needs you, or reaches one of the [limits](#limits-while-desktop-is-disconnected).

* **Desktop on Windows, task started in a version before v3.1623.0**: you don't get the task back, even if Desktop has updated since. Start Desktop again only when you expect the task to be done, because the session can open as Desktop starts, and the task stops when the session opens. If you don't know which version you started the task in, also wait until you expect it to be done.
* **Third-party provider on macOS or Linux, task started in a version before v2.42304.0**: you don't get the task back. Start Desktop again only when you expect the task to be done.
* **Any other task**: start Desktop and open the session, and the task goes on if Desktop rejoins. It can't always rejoin, for example after some Desktop updates, so [update before a long task](#prepare-a-long-task).

When the task stops, the session can show `Restarting Claude Code on <host>…` while Desktop starts a new process. You also lose any approval or question that was waiting for you. If Claude doesn't continue on its own, send a message, and Claude continues from the conversation's saved history.

For third-party deployments, see [SSH remote sessions in Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions).

> [!WARNING]
>
> While a conversation's Claude Code process is still running, don't run [`claude --resume`](https://code.claude.com/docs/en/cli-reference#cli-flags) for it on the remote machine. Claude Code doesn't stop you, and both processes then write to the same conversation. If you aren't sure, add `--fork-session`, which continues in a copy of the conversation, but both processes still work on the same files.

#### Choose where SSH session worktrees go

Unless your organization restricts which folders sessions may use, new SSH sessions create their [worktrees](#run-a-session-in-its-own-worktree) in the first of these locations that is set:

1. **Worktree folder** on the SSH connection
2. [`worktree.location`](https://code.claude.com/docs/en/settings-reference#worktree-location) in `~/.claude/settings.json` on the remote machine
3. `<project-root>/.claude/worktrees/`, the default

Each project gets its own subfolder in the folder you set, so with `~/worktrees` a worktree's path is `~/worktrees/<project>-<id>/<worktree-name>`. If the folder you set is inside the project, Desktop ignores it for that project and uses the default. On a [Windows remote machine](#windows-remote-machines), Desktop always uses the default.

##### Set the worktree folder on an existing connection

Set **Worktree folder** in the settings of a connection you added earlier or one your organization manages. The field requires Claude Desktop v1.44121.0 or later. If your organization restricts which folders sessions may use, Desktop hides the field and keeps worktrees inside the project.

**1. Find the connection**

Open the [environment selector](#start-a-session) and find the connection under **SSH**.

**2. Open the connection's settings**

Hover over the connection and click the gear icon. If the dialog that opens shows **Edit connection…** next to **Host**, select **Edit connection…**.

**3. Set the folder**

In **Worktree folder**, enter a folder on the remote machine, such as `~/worktrees`, and select **Save changes**.

#### Files and processes on the remote machine

Desktop installs a helper program and Claude Code under `~/.claude/remote/` in the home directory of each user who connects to a Linux or macOS remote machine. The helper listens on no network port, but Claude Code and the programs it starts, such as MCP servers and development servers, can.

| Folder | Contents |
| - | - |
| `~/.claude/remote/srv/` | The helper, in one folder per version |
| `~/.claude/remote/ccd-cli/` | Claude Code, in one file per version |
| `~/.claude/remote/run/` | The helper's runtime files, such as its socket and log, in one folder per computer that connects |
| `~/.claude/remote/plugins/` | Plugins that Desktop copies from the user's computer |
| [`~/.claude/uploads/`](https://code.claude.com/docs/en/claude-directory#clear-local-data) | Files that the user attaches to messages, in one folder per session |

To list one user's processes, run `pgrep -fl "$HOME/.claude/remote/"` on the remote machine as that user, or with the user's home directory in place of `$HOME`:

* **Helper**: one or more `server` processes for each computer that connects
* **Claude Code**: the processes that the helper starts for the user's sessions, each from a file named after its version, such as `2.1.295-…`

Desktop reaches the helper through the user's SSH connection, over the Unix socket `rpc.sock` in the helper's folder under `~/.claude/remote/run/`. Apart from root, other users on the machine can't connect to that socket, because it has mode 600 and its folder has mode 700.

For when the helper stops on its own, see [Limits while Desktop is disconnected](#limits-while-desktop-is-disconnected).

To remove the helper and Claude Code for one user:

**1. Quit Desktop**

Quit Desktop on each computer that the user connects from. It installs both programs again the next time it connects, and it can reconnect on its own.

**2. End the processes**

Logged in as that user on the remote machine, run `kill` with the ID of each Claude Code process that [`pgrep`](#files-and-processes-on-the-remote-machine) lists. Once those are gone from the list, run `kill` with the ID of each `server` process. If you end a `server` process first, a command that Claude Code is running can keep running.

Then list the user's remaining processes, for example with `ps -u "$(id -un)" -f`, and end any that you recognize as started by Claude Code. Programs that it left in the background can keep running after it ends, without being in the `pgrep` list.

**3. Delete the folder**

Delete `~/.claude/remote/`. To remove Claude Code's own files in `~/.claude/` and `~/.claude.json`, see [Remove configuration files](https://code.claude.com/docs/en/setup.md#remove-configuration-files).

##### End one session's process

To end one session's Claude Code process, [archive the session](#archive-a-session) in Desktop while Desktop is connected to the remote machine. The process keeps running after its task is done and after you quit Desktop.

Before you archive a session whose worktree has uncommitted changes, see [Keep uncommitted changes when a session is archived](#keep-uncommitted-changes-when-a-session-is-archived).

##### See which user the processes run as

The helper and Claude Code run as the user that Desktop logs in as over SSH. Installing and starting them takes no `sudo`. To check the user, run `ps -o user= -p` on the remote machine with a process ID that [`pgrep`](#files-and-processes-on-the-remote-machine) lists.

Programs that Claude Code starts, such as shell commands and MCP servers, start as that user too. Review that user's rights on the remote machine, its `sudo` rules included, as you would for a person who runs commands there.

##### See who connected to the remote machine

To find out who connected to a remote machine, read the SSH server's log on that machine, where a login from Desktop looks like one from a terminal. With Desktop on macOS or Linux, expect an entry each time Desktop connects, not one for each session.

If the server sets `MaxSessions 1`, expect at least two entries each time Desktop connects or reconnects. Expect at least one more for each terminal tab, and for each Desktop session in which you run commands that start with `!`.

You won't find Desktop's SSH connections in Claude Code's [metrics and events](https://code.claude.com/docs/en/monitoring-usage.md#available-metrics-and-events). To find out from them which remote machine an SSH session ran on, see [Attribute telemetry to Desktop SSH sessions](https://code.claude.com/docs/en/monitoring-usage.md#attribute-telemetry-to-desktop-ssh-sessions). For Desktop's own record of its connections, see [Get Desktop's logs for an SSH problem](#get-desktops-logs-for-an-ssh-problem).

#### Connections that close before login

If the SSH server's log shows connections that close before any login, they can be Desktop's tests of the SSH port. Desktop tests whether a machine answers, for example after a connection to it failed. It opens a connection to the port and closes it at once, without sending anything. Expect one test or several in a row, for example eight in about two minutes.

If nothing bans or refuses addresses for such connections, you don't have to do anything about Desktop's tests. If an address that Desktop connects from is refused or banned, check [whether the SSH server itself refuses the address](#check-whether-the-ssh-server-itself-refuses-the-address) and [whether fail2ban counts Desktop's tests](#check-whether-fail2ban-counts-desktops-tests).

##### Recognize a test in the SSH server's log

Compare the lines in your log with those that an OpenSSH server on Linux writes for a test at the default `LogLevel`, in the row for your server's version. You can see the lines in the last column instead if the server's greeting arrives before Desktop closes the connection:

| OpenSSH version | Lines for a test | Lines if the greeting arrives first |
| - | - | - |
| 6.6 to 7.9 | A line with `Did not receive identification string from 203.0.113.7` | The same line |
| 8.0 to 8.2 | `error: kex_exchange_identification: Connection closed by remote host` | `error: kex_exchange_identification: read: Connection reset by peer` |
| 8.3 to 9.4 | `error: kex_exchange_identification: Connection closed by remote host`, then `Connection closed by 203.0.113.7 port 51234` | `error: kex_exchange_identification: read: Connection reset by peer`, then `Connection reset by 203.0.113.7 port 51234` |
| 9.5 to 10.2 | `Connection closed by 203.0.113.7 port 51234` | `error: kex_exchange_identification: read: Connection reset by peer`, then `Connection reset by 203.0.113.7 port 51234` |
| 10.3 to 10.5 | `Connection closed by 203.0.113.7 port 51234 [preauth]` | `error: kex_exchange_identification: read: Connection reset by peer [preauth]`, then `Connection reset by 203.0.113.7 port 51234 [preauth]` |

Other programs that open the port and close it can leave the same lines. Where a line has an address, check that it is one that a computer with Desktop connects from.

The lines of 8.0 to 8.2 have no address. To get one, set `LogLevel VERBOSE` in `sshd_config` and run `sshd -T | grep -i loglevel` as root. If it prints `loglevel VERBOSE`, reload the SSH server. Then look for a line with `Connection from 203.0.113.7 port 51234` before the test's line.

##### Check whether the SSH server itself refuses the address

If connections are refused from an address that many computers with Desktop share, look in the SSH server's log for a line that ends like this one:

```text theme={null}
drop connection #0 from [203.0.113.7]:51234 on [192.0.2.10]:22 penalty: connections without attempting authentication
```

With the default `LogLevel`, OpenSSH 9.8 and later can write such a line when refusing an address for connections that closed without trying to log in, as Desktop's tests do. With the default settings, you don't see such a line after a few tests alone.

To prevent the refusal, set `PerSourcePenaltyExemptList` in `sshd_config` to the addresses that people connect from, for example `PerSourcePenaltyExemptList 203.0.113.7`. The server then applies none of its penalties to those addresses, including those for failed logins. To check the file, run `sshd -T | grep -i persourcepenalt` as root. If it prints your list, reload the SSH server.

##### Check whether fail2ban counts Desktop's tests

If fail2ban 0.10.5 or later banned an address that Desktop connects from, find your jail's mode in `jail.conf`, `jail.local` or under `jail.d/`:

* **A `filter` line that names a mode in brackets**, such as `filter = sshd[mode=aggressive]`: use that mode.
* **Only the stock `filter` line**, with `[mode=%(mode)s]`: use the `mode` line, or `normal` if there is none.

If the mode is `normal`, fail2ban doesn't count the lines of Desktop's tests, so look for another cause of the ban.

For another mode, copy the lines from your own log to a file on the remote machine. Copy each line whole, from its date to its end, and both lines where a test leaves two. Run `fail2ban-regex` there with the file and your jail's mode, for example `aggressive`:

```bash theme={null}
fail2ban-regex -o ip lines.log "sshd[mode=aggressive]"
```

For each failure that fail2ban counts, the command prints the address on a line of its own, such as `203.0.113.7`. In that case, [prevent a ban](#prevent-a-ban-by-fail2ban). If it prints nothing, fail2ban counts none of those lines in that mode, so look for another cause of the ban.

##### Prevent a ban by fail2ban

To keep fail2ban from banning an address for Desktop's tests, change one of two settings of the jail, each at a cost:

* **`mode`**: set it to `normal` wherever your jail sets it, in a `mode` line or in the brackets of a line such as `filter = sshd[mode=aggressive]`. You give up every count that only the other modes make, for example of clients that connect and leave without trying to log in.
* **`ignoreip`**: set it to the addresses that people connect from, for example `ignoreip = 203.0.113.7`. fail2ban then counts nothing from those addresses, failed logins included.

#### Use MCP servers set up on the remote machine

To use an [MCP server](https://code.claude.com/docs/en/mcp.md) from `~/.claude.json` or a project's `.mcp.json` in an SSH session, set it up in those files on the remote machine. Claude Code starts their stdio servers there, so install the commands those servers run on the remote machine. For servers from `claude_desktop_config.json`, see [Limits while Desktop is disconnected](#limits-while-desktop-is-disconnected).

#### Open an SSH session from a link

A `claude://code/new` link opens Desktop's new-session page, and it can name an SSH connection. Put such a link in a runbook, dashboard, or wiki page to open Desktop set up for the right machine and folder. For platforms that strip such links, see [The link renders as plain text instead of being clickable](https://code.claude.com/docs/en/deep-links.md#the-link-renders-as-plain-text-instead-of-being-clickable).

SSH links require Claude Desktop v2.110.0 or later.

The following link names the user `dev` on `build.example.com`, port 2222, and the folder `/srv/payments`, and fills in a prompt:

```text theme={null}
claude://code/new?ssh_host=dev%40build.example.com&ssh_port=2222&ssh_folder=/srv/payments&q=Investigate%20the%20failed%20deploy
```

An SSH link takes these parameters, and only `ssh_host` is required:

| Parameter | Value |
| :- | :- |
| `ssh_host` | `host` or `user@host`, written as in the **SSH host** field. The value can't start with `-`, and the host part takes only letters, digits, `.`, `_`, `:`, and `-` |
| `ssh_port` | A port number from 1 to 65535 |
| `ssh_folder` | A folder on the remote machine. Start it with `/` or `~/`, or use `~` |
| `q` | URL-encoded text for the prompt box |

An alias from `~/.ssh/config` works as `ssh_host` only for people who have that entry. To match a connection people already have, give the link the same user, host, and port as that connection.

When you open the link, Desktop asks you to confirm before it selects the connection:

* **A connection you already have**: if the host, user, and port match one of your connections, Desktop asks whether to use it, and shows you the connection's name and host, and the folder if the link names one.
* **A new connection**: otherwise Desktop opens the dialog for adding an SSH connection. When you add the connection, Desktop asks whether to connect before it saves anything, and shows you the host from the link, and the port and folder if the link names them.

Until you confirm, Desktop doesn't save the host, port, or folder from the link, and doesn't select or open a connection with them. If an SSH connection is already selected, the new-session page can still connect to it on its own, as it does without a link, even when the link names the same host. A link can't carry a key file, a password, or a command.

Anyone can write a link, so check what it filled in:

* **Before you confirm**: check the host and folder.
* **Before you send**: check the prompt and the selected environment.

Desktop fills in the prompt when the link opens, in place of any text you haven't sent, and never sends it for you. It treats the prompt as plain text, so a leading `/` or `!` and an `@` file mention don't act as a command or a mention. If you cancel, the prompt stays in the box and the environment you had selected doesn't change.

A link doesn't bypass [`sshHostAllowlist`](#restrict-which-ssh-hosts-users-can-connect-to). Desktop checks the allowlist when it connects.

If the link opens Desktop without a dialog about the connection, look for one of these causes:

* **You're signed out**: sign in, then open the link again.
* **Another dialog is open**: close it, then open the link again.
* **The link isn't valid**: Desktop shows a message that says what to fix, and doesn't fill in the prompt.
* **Desktop is older than v2.110.0**: earlier versions ignore the SSH parameters and open the new-session page with only the prompt.
* **SSH sessions are turned off**: if your administrator sets the allowlist to an empty array, Desktop refuses SSH links.

#### Create an SSH connection from a command

If a command-line tool makes your remote machines on demand, add its command to `sshHostCommands` in [`~/.claude/settings.json`](https://code.claude.com/docs/en/settings#settings-files). The environment selector then lists an item named after your entry, such as **Create Dev box**. When you select it, Desktop runs the command on your computer, saves the host that the command prints as an SSH connection, and connects.

> [!NOTE]
>
> Connections from a command require Claude Desktop v3.6556.0 or later on macOS or Linux, signed in with a Claude account. Administrators can [distribute commands to a team](#distribute-commands-to-your-team).

Each entry is one connection, with one host at a time. Desktop runs the command only when you create the connection or [replace its host](#replace-the-host), not each time you connect. To keep two machines at once, add a second entry.

> [!WARNING]
>
> Desktop doesn't stop or delete machines. Each of these keeps running, and can keep costing money, until you delete it with your tool:
>
> * A host that you replaced
> * The host of an entry that you removed from the file, or whose `id` you changed
> * A machine that your command made without Desktop saving its host, for example in these cases:
>   * The command fails or runs out of time
>   * Desktop can't use the printed host, another connection already uses it, or your organization doesn't allow it
>   * While the command runs, you cancel it, remove its entry, change its `command` or `id`, or quit Desktop

The following example adds a connection named Dev box. If the file doesn't exist, create it. If it already holds settings, add the key beside them. The command `acme-dev create` stands for your own tool, and `~/project` is the folder that Desktop selects on each machine your command makes:

```json ~/.claude/settings.json theme={null}
{
  "sshHostCommands": [
    {
      "id": "devbox",
      "name": "Dev box",
      "command": "acme-dev create",
      "startDirectory": "~/project"
    }
  ]
}
```

Each entry takes these fields, and `id`, `name`, and `command` are required:

| Field | Value |
| :- | :- |
| `id` | Up to 64 ASCII letters, digits, `.`, `_`, and `-`, starting with a letter or digit. Use an `id` that no other entry in `sshHostCommands` or [`sshConfigs`](#pre-configure-ssh-connections-for-your-team) has. Desktop keeps the connection's host under it, so if you change it, the connection starts over with no host and the old machine keeps running. |
| `name` | The connection's name in the environment selector, up to 200 characters on one line |
| `command` | A program and its arguments, as [Write the command](#write-the-command) describes |
| `sshIdentityFile` | Path to your private key, such as `~/.ssh/id_ed25519`. Leave it out to use your SSH configuration or SSH agent. |
| `startDirectory` | The default folder on the remote machine. Start it with `/` or `~/`, or use `~`. |

To change or remove the connection, edit its entry in the file, because the app's SSH connection dialog doesn't open for it. You don't need to restart Desktop after you edit the file. If the entry doesn't show up or you can't select it, see [If a command is missing or gray](#if-a-command-is-missing-or-gray).

##### Write the command

Desktop starts the program directly, with no shell and no terminal:

* **Program**: write its name, or its full path from `/`, without spaces. Desktop looks for a bare name on the `PATH` that your login shell exports. Relative paths such as `./acme-dev`, paths that start with `~`, and shell aliases and functions don't work.
* **Arguments**: separate plain arguments with spaces. The command can hold only spaces, ASCII letters, digits, and the characters `+,-./:=@_~`, and no word can start with `~`.
* **Scripts**: if the command needs anything else, such as quotes, pipes, variables, or a URL with `?` or `&`, put it in a script. Make the script executable, start it with a `#!` line, and set `command` to its full path, such as `/Users/you/bin/make-devbox`. On macOS, keep the script out of the Documents, Desktop, and Downloads folders, where macOS can block it.
* **Input**: the program gets no input and no terminal, so it can't prompt you there. If your tool signs you in through a browser or a prompt, sign in from a terminal first, and again whenever that sign-in lapses.
* **Environment**: the program runs in your home directory with the variables that your login shell exports. Desktop reads them when it starts, as it does for [a `ProxyCommand`](#use-variables-from-your-shell-in-a-proxycommand), so quit and reopen Desktop after you change them.
* **Time limit**: Desktop stops a program that is still running after 10 minutes. Desktop's progress message doesn't show the program's output. To stop the program sooner, select **Cancel** next to that message.

The program has to exit with code 0 and print only the host on standard output, in one of two forms:

* **One line**: `host` or `user@host`, written as for `ssh_host` in [an SSH link](#open-an-ssh-session-from-a-link). To name a port, use the JSON form.
* **One JSON object**: `sshHost`, and optionally a numeric `sshPort` and a `startDirectory` that replaces the entry's, such as `{"sshHost": "dev@devbox-1234.example.com", "sshPort": 2222}`

To see the output that Desktop reads, run the command in a terminal with no input and with standard output in a file:

```bash theme={null}
acme-dev create < /dev/null > host.txt
```

The file has to hold only the host. When you run this test, your tool makes a machine too, so delete it with your tool afterward.

If your tool prints other lines before the host, such as progress messages, wrap it in a script that prints only the host. The following script prints the last line of your tool's output. If your tool fails, the script exits with the same code, so that Desktop reports the failure:

```bash theme={null}
#!/bin/bash
out=$(mktemp) || exit
trap 'rm -f "$out"' EXIT
acme-dev create > "$out" || exit
tail -n 1 "$out"
```

If the command fails, **View details** in Desktop's message shows the last line that the command wrote to standard error, if any.

##### Connect to a new host

Answer two questions the first time you connect to each new host:

* **Host key**: with OpenSSH's default host key checking, check the key's fingerprint, then choose whether to connect. To skip the question, have your command add the key to `~/.ssh/known_hosts` before it prints the host, using a key that your tool learned when it made the machine. For a port other than 22, that line starts with `[host]:port`. If your tool reuses host names, remove the old key's line too.
* **Folder**: choose whether you trust the folder that you open there

Keep host key checking on for these hosts, and keep a `known_hosts` file for them. If `StrictHostKeyChecking` is `no` or `accept-new` and `UserKnownHostsFile` is also `/dev/null` or `none`, nothing records the key. When your tool then reuses a name, you can connect to a different machine without a warning.

##### Replace the host

Once Dev box has a host, the selector lists Dev box among your SSH connections, and **Create Dev box** becomes **Replace Dev box's host**. If that item isn't in the list, look under **More**.

Select it when the machine is gone or you want a fresh one. On the new-session page, the message that says Desktop can't reach the host offers it too. Desktop runs the command again, and new sessions use the new host.

* **A new host**: the item is gray for 10 minutes after Desktop saves a host, because a new machine can take a while to start. While a new host doesn't answer, the new-session page keeps trying to connect for those 10 minutes.
* **Sessions on the old host**: they stay on it, and Desktop doesn't connect to that host unless you add it back. To continue one, open the session and select **Add SSH connection**. Desktop fills in the old host. Save it as a connection of its own.

##### Distribute commands to your team

To give your team a connection, set `sshHostCommands` in Claude Code's [managed settings](https://code.claude.com/docs/en/managed-settings.md) file or MDM policy on each computer, not in the desktop app's own [device management policy](#device-management-policies). Users see your entries alongside their own, and the app offers no way to edit or remove an entry, theirs or yours.

The following managed settings file gives users a connection named Dev box and turns off their own entries, along with Claude Code hooks from user, project, and local settings:

```json managed-settings.json theme={null}
{
  "sshHostCommands": [
    {
      "id": "acme-devbox",
      "name": "Dev box",
      "command": "/usr/local/bin/acme-dev create"
    }
  ],
  "strictPluginOnlyCustomization": ["hooks"]
}
```

Before you deploy the key, settle each of these:

* **Where to put the key**: if your MDM policy for Claude Code already sets a [policy key](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources), put it there. Otherwise, put it in the managed settings file. By default, such a policy outranks the file, and Desktop then ignores entries in the file. Set it on the computer even where [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md) apply: Desktop ignores the key there, and in project and local settings.
* **The `id`**: if a user's `sshHostCommands` entry has your `id`, only yours works. If any other SSH connection has it, such as one in a user's `sshConfigs`, your entry is gray. Pick an `id` that users are unlikely to choose.
* **The program**: give its full path, because Desktop looks up a bare name on each user's own `PATH`. The program runs as the user, with the variables that their login shell exports.
* **Users' own entries**: Desktop treats a user's entry like a [hook](https://code.claude.com/docs/en/hooks.md), because both run a program on the computer. To allow only your entries, set [`strictPluginOnlyCustomization`](https://code.claude.com/docs/en/settings-reference#strictpluginonlycustomization) to `["hooks"]`, or add `"hooks"` to its list. You also stop Claude Code hooks from user, project, and local settings, with no way to keep them. If you set that key or [`allowManagedHooksOnly`](https://code.claude.com/docs/en/settings-reference#allowmanagedhooksonly) to `true` instead, you block more, as each key's entry lists.
* **Every entry**: to turn off your entries too, set [`disableAllHooks`](https://code.claude.com/docs/en/settings-reference#disableallhooks) in managed settings. If you set [`disableDesktopLocalSessions`](https://code.claude.com/docs/en/settings-reference#disabledesktoplocalsessions), or an `sshHostAllowlist` that allows no host, the selector lists no **Create** or **Replace** items.
* **Where the locks count**: for these entries, Desktop reads `allowManagedHooksOnly`, `strictPluginOnlyCustomization`, and `disableAllHooks` from server-managed settings and from the computer's own file or policy, and applies the stricter result. Every entry stays gray until Desktop has checked claude.ai for server-managed settings, even if your organization has none.
* **Allowed hosts**: if you set [`sshHostAllowlist`](#restrict-which-ssh-hosts-users-can-connect-to), make sure that a pattern matches each hostname that your tool prints, and leave `user@` out of the pattern. Desktop checks the printed name only after the command has run, so a machine that the list refuses already exists, and the user has to delete it with your tool. At each connection, the resolved `HostName` has to match too.

After you deploy the key, restart Desktop on a test computer. In the Code tab's environment selector, look under **SSH**, or in the single **SSH** row. Your entry shows as a **Create** item, or as a gray item that gives the reason when you hover over it. If it's missing, check where you put the key, then the cases in [If a command is missing or gray](#if-a-command-is-missing-or-gray).

##### If a command is missing or gray

The environment selector lists no **Create** or **Replace** item in these cases:

* **The file**: `~/.claude/settings.json` has [invalid JSON or a value that the schema rejects](https://code.claude.com/docs/en/settings.md#fix-a-broken-settings-file), you misspelled the key, or you put it in a project's settings. Fix the file.
* **Platform and account**: you use Windows, or a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md) instead of a Claude account. Add each host as an [SSH connection](#ssh-sessions) yourself.
* **Your organization's settings**: your administrator turned off local sessions, or turned off SSH sessions. Ask them whether you can use commands.
* **No `ssh` program**: Desktop couldn't start the OpenSSH client on your computer. Install it, or ask your administrator to allow it, then restart Desktop.

An entry that you can't select is gray. Hover over it to see the reason:

* **A mistake in the entry**: fix the field or the command that the message names. If the `id` is in use, give the entry another one.
* **A broken settings file**: while your own settings file is broken, your administrator's entries may be gray, with a message that names the file. [Fix the file](https://code.claude.com/docs/en/settings.md#fix-a-broken-settings-file).
* **A new host**: you can [replace a host](#replace-the-host) once it's 10 minutes old.
* **Hooks are off or restricted**: your own entries work only where your own hooks can run. Remove `disableAllHooks` from your settings, or ask your administrator.
* **Settings are still loading**: every entry is gray until Desktop has loaded your organization's [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md), usually a few seconds after launch. If the entries stay gray, check your connection to claude.ai.

#### Pre-configure SSH connections for your team

Administrators can distribute SSH connections to team members by setting `sshConfigs` in [managed settings](https://code.claude.com/docs/en/managed-settings.md).

* **What users see**: connections defined this way appear in each user's environment selector automatically.
* **What users can change**: users can select a managed connection and [set their own **Worktree folder**](#set-the-worktree-folder-on-an-existing-connection) for it. They can't edit its other fields or delete it in the app.

The following example pre-configures a single connection:

```json theme={null}
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519"
    }
  ]
}
```

Each entry requires `id`, `name`, and `sshHost`. The `sshPort` and `sshIdentityFile` fields are optional. Users can also add `sshConfigs` to their own `~/.claude/settings.json`.

If you leave `user@` out of `sshHost`, Desktop connects as the `User` that each developer's `~/.ssh/config` sets for the host, or else as their username on their own computer.

#### Restrict which SSH hosts users can connect to

Administrators can limit Desktop's SSH sessions to an approved set of hosts by setting `sshHostAllowlist` in [managed settings](https://code.claude.com/docs/en/managed-settings.md). When set, users can only connect to hosts whose resolved hostname matches one of the patterns. Set it to an empty array to disable SSH sessions. The [`sshHostAllowlist` reference entry](https://code.claude.com/docs/en/settings-reference#sshhostallowlist) says how an empty array combines with lists in other managed sources.

The following example allows connections to any host under `devboxes.example.com` and to a single named bastion host:

```json theme={null}
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

> [!WARNING]
>
> If your organization delivers [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md), set `sshHostAllowlist` there. By default, Desktop reads the key only from the [highest-ranked managed source that delivers a policy key](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources). If that source leaves the key unset, Desktop ignores a list in a lower-ranked MDM policy or managed settings file and treats the key as [unset](https://code.claude.com/docs/en/settings-reference.md#sshhostallowlist). Desktop shows no warning.
>
> Also keep the same list on each user's machine, in the highest-ranked MDM policy or managed settings file there. Desktop fetches server-managed settings at launch and keeps no cached copy, so until a fetch succeeds the machine's list is the one that applies.

Patterns are case-insensitive. `*` matches any host, and `*.example.com` matches `example.com` and any subdomain. Anything else is an exact match. The check runs against the hostname after `~/.ssh/config` resolution via `ssh -G`, so a `Host` alias is permitted as long as its resolved `HostName` matches. A session's [jump hosts](#allow-jump-hosts) have to match too.

`sshHostAllowlist` is read from managed settings only; values in user or project settings are ignored. Only the Claude Desktop app honors this setting; the Claude Code CLI and IDE extensions do not read it, and it does not restrict `ssh` commands run through the Bash tool. It governs which hosts the Desktop app connects to, not network egress, so pair it with your organization's network or zero-trust controls if you need a hard boundary.

##### Allow jump hosts

Add each jump host that Desktop checks to `sshHostAllowlist`, by its own resolved `HostName`. Add the jump hosts before users update to Claude Desktop v3.1623.0 or later, or they can't connect through them.

> [!WARNING]
>
> The list has one kind of entry, so users can also start a session on any host that you list. List only jump hosts that you'd also let users run sessions on.

Desktop checks jump hosts in the `ProxyJump` that the user's `~/.ssh/config` sets for the session's host, or in a `ProxyCommand` written as `ssh -W %h:%p <host>`. If one that it checks isn't on the list when Desktop connects or reconnects a session, the connection fails. When a user starts a session or sends a message, the error's details give that jump host's `HostName`, which is the name to add:

```text theme={null}
SSH host "bastion.example.com" is not allowed by your organization's managed settings. It is a jump host on the way to "devbox".
```

If the message says `managed settings on this computer`, add the name to the list on the user's computer. If more than one jump host is missing, the error names one at a time. To find every name before users update, use a terminal on a user's computer:

**1. Find the route**

Run `ssh -G` with a host that users connect to, such as `ssh -G devbox`. Look for a `proxyjump` line, or a `proxycommand` line written as `ssh -W %h:%p <host>`. The command still counts with any of `-l`, `-p`, `-J`, `-q`, `-v`, `-N`, `-T`, `-x`, or `-a`, and the hosts after `-J` are jump hosts too. If a `proxycommand` line runs a program other than `ssh`, add nothing for it.

**2. Look up each jump host**

Run `ssh -G` with each jump host on that line, without any `:port`, and note the `hostname` that it prints. If the output for the first jump host on that line has a line of either kind, repeat this step with it. Ignore such a line in a later jump host's output.

**3. Add the names**

Add each hostname, or a wildcard that covers it, to `sshHostAllowlist` in every managed source where you set a list. Then have users quit and reopen Desktop, because it fetches server-managed settings at launch.

#### Turn off local sessions and distribute SSH connections

To turn off local sessions and limit SSH sessions to hosts that you choose, deploy [`disableDesktopLocalSessions`](https://code.claude.com/docs/en/settings-reference#disabledesktoplocalsessions), [`sshConfigs`](#pre-configure-ssh-connections-for-your-team), and [`sshHostAllowlist`](#restrict-which-ssh-hosts-users-can-connect-to) together.

> [!NOTE]
>
> This setup is for users who sign in with a Claude account. With a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md), SSH sessions are off by default, and setting `sshHostAllowlist` can turn them on. Read [SSH remote sessions in Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/ssh-remote-sessions) before you deploy these keys.

The following example turns off local sessions, adds one connection, and limits SSH sessions to that connection's host:

```json managed-settings.json theme={null}
{
  "disableDesktopLocalSessions": true,
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "dev.example.com"
    }
  ],
  "sshHostAllowlist": ["dev.example.com"]
}
```

The keys apply to the desktop app. They leave other ways to run Claude Code as they are, such as the CLI, Cowork, and cloud sessions:

* **The CLI**: none of the keys stops a developer from running the Claude Code CLI on their own computer
* **Cowork**: none of the keys applies to [Cowork](https://claude.com/docs/cowork/overview) sessions or Cowork scheduled tasks
* **Cloud sessions**: none of the keys changes whether [cloud sessions](#cloud-sessions) are available. To turn them off, use the **Cloud sessions** setting under [Admin console controls](#admin-console-controls).

When you adapt the example, check the hostnames, the Desktop version, and the file's permissions:

* **Hostnames**: make sure that a pattern in `sshHostAllowlist` matches the hostname of each `sshConfigs` entry, without `user@`, or developers can't connect to it. Also add a pattern that matches each [jump host](#allow-jump-hosts) that Desktop checks on the way to it. For how Desktop matches a hostname, see [Restrict which SSH hosts users can connect to](#restrict-which-ssh-hosts-users-can-connect-to).
* **Version**: `disableDesktopLocalSessions` requires Claude Desktop v1.37937.0 or later
* **File permissions**: make sure that each developer's account on the computer can read the managed settings file. Desktop doesn't apply the keys in a file that the account can't read, and Claude Code [starts without them](https://code.claude.com/docs/en/managed-settings.md#find-entries-claude-code-dropped) too.

Put the three keys in one [managed source](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources), the highest-ranked one that you deliver. If you deliver [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md), also keep a copy of the three keys in the highest-ranked MDM policy or managed settings file on each computer. Desktop fetches server-managed settings at launch, and the copy on the computer applies until a fetch succeeds.

To confirm that the settings apply, check a developer's computer:

**1. Check the environment selector**

Quit and reopen Desktop, then open the [environment selector](#start-a-session). The settings applied if it shows:

* The entry for that computer, in gray
* **Shared Dev VM** under **SSH**. If it isn't listed there, click the single **SSH** row, or **More** at the end of the group.

If the entry for the computer is still available, check for these causes:

* **Desktop version**: update Desktop if it's earlier than v1.37937.0.
* **Managed settings file**: make sure that the file is valid JSON.
* **Managed source**: make sure that the computer reads the [managed source](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources) that holds the keys.

**2. Add a host that isn't on the allowlist**

[Add an SSH connection](#ssh-sessions) with a hostname that isn't on the allowlist, such as `other.example.com`. Desktop saves the connection but refuses to connect, and says that your organization's settings don't allow the connection.

## Enterprise configuration

Organizations on Team or Enterprise plans can manage desktop app behavior through admin console controls, managed settings files, and device management policies.

### Admin console controls

These settings are configured through the [admin settings console](https://claude.ai/admin-settings/claude-code):

* **Desktop**: control whether users in your organization can access Claude Code in the desktop app
* **Cloud sessions**: enable or disable [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md) for your organization
* **Remote Control**: enable or disable [Remote Control](https://code.claude.com/docs/en/remote-control.md) for your organization

In Enterprise organizations that have HIPAA enabled, the **Desktop** toggle is off by default and an [Owner](https://code.claude.com/docs/en/server-managed-settings.md#access-control) can turn it on. Applying the [HIPAA configuration](https://code.claude.com/docs/en/hipaa-setup.md) turns it off, even if it was on, so an Owner has to turn it on afterward. **Cloud sessions** and **Remote Control** are also off by default, and an Owner can't turn them on once the organization has the HIPAA configuration applied.

> [!NOTE]
>
> The OpenTelemetry form for Cowork under **Monitoring** in the admin console's [Data and privacy settings](https://claude.ai/admin-settings/data-privacy-controls) applies to Cowork sessions only. In a Cowork session on this machine, the desktop app passes that collector to Claude Code as `OTEL_*` environment variables, so the form takes effect even though Claude Code in that session [never fetches admin-console settings](#managed-settings).
>
> To export telemetry from Code tab sessions, set `CLAUDE_CODE_ENABLE_TELEMETRY` and the `OTEL_*` variables in the `env` block of your Claude Code managed settings, as shown in [administrator configuration for monitoring](https://code.claude.com/docs/en/monitoring-usage.md#administrator-configuration). Local, cloud, and SSH sessions each read [managed settings from different sources](#managed-settings). For the hosts a cloud session can reach, see [network access](https://code.claude.com/docs/en/cloud-environments.md#network-access). For the `service.name` that Code tab sessions report, see [service information](https://code.claude.com/docs/en/monitoring-usage.md#service-information).
>
> To find out which remote machine an SSH session ran on, see [Attribute telemetry to Desktop SSH sessions](https://code.claude.com/docs/en/monitoring-usage.md#attribute-telemetry-to-desktop-ssh-sessions).

### Managed settings

Managed settings override project and user settings and apply to Claude Code sessions in Desktop. You can set these keys in your organization's [managed settings](https://code.claude.com/docs/en/managed-settings.md) file or push them remotely through the admin console, unless a key's row says otherwise.

| Key | Description |
| - | - |
| `permissions.disableBypassPermissionsMode` | set to `"disable"` to prevent users from enabling Bypass permissions mode. |
| `disableAutoMode` | set to `"disable"` to remove [Auto](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) mode from the mode selector. Also accepted under `permissions`. |
| `autoMode` | customize what the auto mode classifier trusts and blocks across your organization. See [Configure auto mode](https://code.claude.com/docs/en/auto-mode-config.md). |
| `browserExternalPageTools` | set to `"disabled"` to prevent Claude from using tools to read or act on external pages in the [Browser pane](#browse-external-sites). Users can still navigate to external sites themselves, and local dev server previews are unaffected. |
| `disableMobileSimulatorTools` | set to `true` to block Claude's tools for controlling and capturing devices in the [iOS Simulator pane](https://code.claude.com/docs/en/desktop-ios-simulator.md#turn-off-simulator-access). The pane stays usable for the user's own taps; only Claude's access is removed. The value must be the JSON boolean `true`; the string `"true"` is ignored. |
| `disableBrowserExternalNavigation` | set to `true` to turn off external browsing in the [Browser pane](#browse-external-sites) entirely. Neither users nor Claude can navigate to external sites, and localhost dev server previews are unaffected. The value must be the JSON boolean `true`; the string `"true"` is ignored. |
| `sshConfigs` | pre-configure [SSH connections](#pre-configure-ssh-connections-for-your-team) that appear in the environment selector. Users can't delete managed connections or edit anything but their own **Worktree folder**. |
| `sshHostCommands` | give users [SSH connections whose host comes from a command](#distribute-commands-to-your-team), alongside their own. Desktop reads it from the managed settings file or MDM policy on the computer, and ignores it in [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md). Requires Claude Desktop v3.6556.0 or later on macOS or Linux, signed in with a Claude account. |
| `sshHostAllowlist` | restrict [SSH sessions](#restrict-which-ssh-hosts-users-can-connect-to) to hosts whose resolved hostname matches one of these patterns. Read from managed settings only. |
| `disableDesktopLocalSessions` | set to `true` to turn off [Code sessions that run on the device](#local-sessions-on-managed-devices), leaving SSH sessions to other hosts and cloud sessions available. The value must be the JSON boolean `true`. Read from managed settings only. Requires Claude Desktop v1.37937.0 or later. |
| `disableSshSavedPasswords` | set to `true` to stop Desktop from offering to remember SSH passwords and from using or showing the ones it saved earlier. Turning it on doesn't delete them. Read from managed settings only. Requires Claude Desktop v1.49585.0 or later. |
| `managedMcpServers` | push MCP server configurations to all users. Available in third-party (3P) Desktop deployments only. In each entry, set a transport of `"http"`, `"sse"`, or `"stdio"`, connection details, and optionally a `toolPolicy` map to restrict which of that server's tools users can invoke. Deliver it through the managed settings file, MDM, or a Claude apps gateway policy's [`desktop` block](https://code.claude.com/docs/en/claude-apps-gateway-config#claude-desktop-overlay), since 3P deployments don't receive admin-console settings. To deliver it through the gateway, you need Claude Code v2.1.232 or later on the gateway server. This is the desktop app's own key; Claude Code reads a [same-named managed setting](https://code.claude.com/docs/en/managed-mcp.md#provide-servers-through-managed-settings) of its own, with a different entry shape. |

Which managed settings reach a Desktop session depends on where that session runs. Model restrictions such as [`availableModels`](https://code.claude.com/docs/en/model-config#restrict-model-selection) are enforced in Desktop's Claude Code sessions the same way as in the terminal CLI; see [surface coverage](https://code.claude.com/docs/en/model-config.md#surface-coverage).

* **Local sessions on this machine**: a managed settings file deployed to disk applies. Managed settings pushed remotely through the admin console also reach these sessions on Anthropic's API when the session authenticates with an [eligible login](https://code.claude.com/docs/en/server-managed-settings.md#platform-availability), following the same [settings precedence](https://code.claude.com/docs/en/settings.md#settings-precedence) as the terminal CLI.
* **[Cloud sessions](#cloud-sessions)**: receive [server-managed settings](https://code.claude.com/docs/en/server-managed-settings.md); device-deployed files don't reach them, because they run on Anthropic-managed VMs. Sessions routed to a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments) also read the managed settings file in the runner image. [How Claude Code combines managed sources](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources) says when that file applies.
* **[SSH sessions](#ssh-sessions)**: the session reads the managed settings file from the remote host. Desktop itself reads `sshConfigs`, `sshHostAllowlist`, `disableSshSavedPasswords`, and `disableDesktopLocalSessions` on the local machine. If you deliver more than one managed source, it reads them from [one by default](https://code.claude.com/docs/en/managed-settings.md#how-claude-code-combines-managed-sources).
* **[Cowork](https://claude.com/docs/cowork/overview) sessions**: in a Cowork session on this machine, Claude Code never fetches admin-console settings, even when the user signs in with a Team or Enterprise account, and reads policy deployed to the machine unless your Claude Desktop configuration sets `requireCoworkFullVmSandbox`. Remote Cowork sessions receive neither. See [where and when a policy applies](https://code.claude.com/docs/en/managed-settings.md#where-and-when-a-policy-applies) for which device files reach Cowork, and [MCP permission rules](https://code.claude.com/docs/en/permissions.md#mcp) for how `Bash` and `WebFetch` rules apply to Cowork's tools.

In local and SSH sessions, the desktop app delivers each user's connected claude.ai connectors to Claude Code directly. No MCP setting or `managed-mcp.json` reaches those connectors, whichever settings source or file location you use. To block a connector's tools in these sessions, use your organization's [connector tool controls](https://code.claude.com/docs/en/mcp.md#organization-controls-on-connector-tools). [How connectors reach Claude Code](https://code.claude.com/docs/en/mcp.md#how-connectors-reach-claude-code) shows which settings govern connectors in each kind of session.

`permissions.disableBypassPermissionsMode` and `disableAutoMode` also work in user and project settings, but placing them in managed settings prevents users from overriding them.

For the permission, plugin, and delivery keys only a managed source can set, see [Keys only managed settings can set](https://code.claude.com/docs/en/managed-settings.md#managed-only-settings).

### Device management policies

IT teams can manage the desktop app through MDM on macOS, group policy on Windows, or a policy file on Linux. Available policies include enabling or disabling the Claude Code feature, controlling auto-updates on macOS and Windows, and setting a custom deployment URL.

* **macOS**: configure via `com.anthropic.claudefordesktop` preference domain using tools like Jamf or Kandji
* **Windows**: configure via registry at `SOFTWARE\Policies\Claude`
* **Linux**: configure via a root-owned file at `/etc/claude-desktop/managed-settings.json`, which holds the policy keys as a JSON object. Desktop refuses the file if anyone but root can write to it or to its folder. It's a different file from Claude Code's [managed settings file](https://code.claude.com/docs/en/managed-settings.md).

#### Restrict sign-in to your organization

To restrict which claude.ai organizations can sign in to Claude Desktop, set `forceLoginOrgUUID` in the Claude Desktop policy.

The key requires Claude Desktop v1.2581.0 or later.

On Linux, a policy file that sets only this key reads:

```json /etc/claude-desktop/managed-settings.json theme={null}
{
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

Replace the placeholder with your claude.ai organization ID, shown in [claude.ai admin settings](https://claude.ai/admin-settings/organization). It's the same ID that Claude Code's [`forceLoginOrgUUID`](https://code.claude.com/docs/en/settings-reference#forceloginorguuid) setting takes. For macOS and Windows samples that set this key, see [Deploy the Claude Desktop policy](https://claude.com/docs/cowork/hipaa-setup#deploy-the-claude-desktop-policy) in the Cowork guide for HIPAA-ready organizations.

If you set `forceLoginMethod` and `forceLoginOrgUUID` in Claude Code's [managed settings](https://code.claude.com/docs/en/managed-settings.md), you don't change the Claude Desktop sign-in screen.

### Network access requirements

Desktop loads its application code and user content from Anthropic CDN hosts.

```text theme={null}
anthropic.com
*.anthropic.com
claude.ai
*.claude.ai
claude.com
*.claude.com
claude.app
*.claude.app
*.claudeusercontent.com
*.claudemcpcontent.com
```

Traffic is HTTPS on port 443 unless you configure a custom port for [OTLP](https://code.claude.com/docs/en/monitoring-usage.md), an LLM gateway, or an MCP server.

For proxy servers, custom certificate authorities, mTLS, and the domains the standalone CLI needs, see [network configuration](https://code.claude.com/docs/en/network-config.md).

To reduce the number of firewall wildcards, allow these Anthropic hosts instead. Certain subdomains are dynamically generated and must remain wildcards.

```text theme={null}
anthropic.com
api.anthropic.com
a-api.anthropic.com
a-cdn.anthropic.com
s-cdn.anthropic.com
assets-proxy.anthropic.com
claude.ai
a.claude.ai
assets.claude.ai
downloads.claude.ai
*.livepreview.claude.ai
claude.com
platform.claude.com
sso.claude.com
*.livepreview.claude.app
*.claudeusercontent.com
*.claudemcpcontent.com
```

If your organization has [IP allowlisting](https://support.claude.com/en/articles/13200993-restrict-access-to-claude-with-ip-allowlisting) enabled for Claude, route `bridge.claudeusercontent.com` through the same proxy egress as `claude.ai` and `api.anthropic.com`. If you can't route it that way, add the egress address your proxy uses for that host to your organization's IP allowlist, but only when that address is dedicated to your organization: a shared proxy egress range also admits the proxy vendor's other customers.

Anthropic checks connections to that host against your organization's IP allowlist using the address they arrive from. If your proxy sends traffic for it out through an address that isn't on that allowlist, Claude in Chrome and other features that connect through the bridge stop working while the rest of the app keeps working.

An [artifact](https://code.claude.com/docs/en/artifacts.md) that loads a typeface from [Google Fonts](https://code.claude.com/docs/en/artifacts.md#improve-the-visual-design) also requests `fonts.googleapis.com` and `fonts.gstatic.com`. Both hosts are optional. If you block them, artifacts render in fallback typefaces. Block with a fast rejection rather than a silent drop so the font request fails immediately instead of delaying the page's first render.

Artifacts can also load JavaScript libraries, such as React or a charting package, from `cdnjs.cloudflare.com`, `cdn.jsdelivr.net`, `cdn.tailwindcss.com`, `code.jquery.com`, and `unpkg.com`, and from no other external host. If you block those hosts, the parts of an artifact that depend on a library don't work, and unlike a blocked font, a blocked library has no fallback. Block with a fast rejection here too, so a blocked library request fails at once rather than hanging until it times out.

### Authentication and SSO

Team and Enterprise organizations can require SSO for all users. See [authentication](https://code.claude.com/docs/en/authentication.md) for plan-level details and [Setting up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) for SAML configuration; OIDC setup is covered in the [Claude Enterprise Administrator Guide](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide).

### Data handling

Claude Code processes your code locally in local sessions, or in cloud sessions on Anthropic-managed infrastructure, unless your organization routes them to a [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments). Cloud sessions, including in a self-hosted environment, send conversations and code context to Anthropic's API for processing; local and SSH sessions send them to whichever [model provider](#feature-comparison) your deployment configures, Anthropic's API by default. See [data handling](https://code.claude.com/docs/en/data-usage.md) for details on data retention, privacy, and compliance.

### Deployment

Desktop can be distributed through enterprise deployment tools:

* **macOS**: distribute via MDM such as Jamf or Kandji using the `.dmg` installer
* **Windows**: deploy via the MSIX package. See [Deploy Claude Desktop for Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) for enterprise deployment options including silent installation

For the domains to allowlist in your firewall, see [network access requirements](#network-access-requirements) above. For proxy settings, custom certificate authorities, and LLM gateways, see [network configuration](https://code.claude.com/docs/en/network-config.md).

For the full enterprise configuration reference, see the [enterprise configuration guide](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Coming from the CLI?

If you already use the Claude Code CLI, Desktop runs the same underlying engine with a graphical interface. You can run both simultaneously on the same machine, even on the same project. Each keeps its own session list, and you can bring a CLI session into Desktop. They share configuration and project memory via CLAUDE.md files.

To move a CLI session into Desktop, run `/desktop` in the terminal. Claude saves your session and opens it in the desktop app, then exits the CLI. This command is available on macOS and x64 Windows when you are signed in with a Claude subscription. It is not available with API key authentication or on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry.

From your shell, [`claude --desktop`](https://code.claude.com/docs/en/cli-reference#cli-flags) opens Desktop directly without starting a terminal session. It requires Claude Code v2.1.285 or later and has the same platform and sign-in requirements as `/desktop`. With no other arguments, it opens Desktop on the current directory. To open an existing CLI session in Desktop, add `--continue` for the most recent conversation in this directory, or `--resume` with the session ID that `/status` shows:

```bash theme={null}
claude --desktop --resume <session-id>
```

Claude Code prints `Opening session <session-id> in Claude Desktop`, the session opens in the app, and the command exits. A session name doesn't work in place of the ID. Claude Code doesn't move a session that is open in another terminal or still running in the background. If Claude Desktop isn't installed, the command prints a download link and exits.

You can also pick up a CLI session from inside Desktop with `/resume`. The command is available in local sessions, not in SSH, WSL, or cloud sessions.

To continue a terminal session in Desktop:

1. Close the session in the terminal.
2. In the Desktop prompt box, type `/resume`. Desktop lists the sessions you started from the CLI on this computer. Search by title, folder, or branch, and preview where each one left off.
3. Select the session. It continues in the app with its full conversation and context.

Desktop continues the same session rather than a copy, so `claude --resume` in the terminal still finds it afterwards.

> [!TIP]
>
> When to use Desktop vs CLI: use Desktop when you want to manage parallel sessions in one window, arrange panes side by side, or review changes visually. Use the CLI when you need scripting, automation, or prefer a terminal workflow.

### CLI flag equivalents

This table shows the desktop app equivalent for common CLI flags. Flags not listed have no desktop equivalent because they are designed for scripting or automation.

| CLI | Desktop equivalent |
| - | - |
| `--model sonnet` | Model picker in the row under the prompt box |
| `--resume`, `--continue` | Click a session in the sidebar, or type `/resume` in the prompt box to pick up a session you started from the CLI |
| `--permission-mode` | Mode selector in the row under the prompt box |
| `--dangerously-skip-permissions` | Bypass permissions mode. On Pro and Max plans, enable "Allow bypass permissions mode" in **Settings > Code** or **Settings > Claude Code**; on Team and Enterprise plans, organization policy controls it |
| `--add-dir` | [Add folders to a session](#add-folders-to-a-session) in local and SSH sessions, or select [several repositories](#run-long-running-tasks-in-the-cloud) in a cloud session |
| `--allowedTools`, `--disallowedTools` | No per-session equivalent. Permission rules in [settings files](https://code.claude.com/docs/en/settings.md) still apply. |
| `--verbose` | [Verbose view mode](#switch-view-modes) |
| `--print`, `--output-format` | Not available. Desktop is interactive only. |
| `ANTHROPIC_MODEL` env var | Model picker in the row under the prompt box |
| `MAX_THINKING_TOKENS` env var | See [Turn off extended thinking](#turn-off-extended-thinking) |

### Shared configuration

Desktop and CLI read the same configuration files, so your setup carries over:

* **[CLAUDE.md](https://code.claude.com/docs/en/memory.md)** and `CLAUDE.local.md` files in your project are used by both
* **[MCP servers](https://code.claude.com/docs/en/mcp.md)** configured in `~/.claude.json` or `.mcp.json` work in both
* **[Hooks](https://code.claude.com/docs/en/hooks.md)** and **[skills](https://code.claude.com/docs/en/skills.md)** defined in settings apply to both
* **[Settings](https://code.claude.com/docs/en/settings.md)** in `~/.claude.json` and `~/.claude/settings.json` are shared. Permission rules, allowed tools, and other settings in `settings.json` apply to Desktop sessions.
* **Models**: the same [models](https://code.claude.com/docs/en/model-config.md#available-models) are available in both. In Desktop, select the model from the model picker in the row under the prompt box. You can change the model mid-session from the same picker.

#### MCP servers from the Claude Desktop chat app

The Desktop app loads MCP servers from `claude_desktop_config.json` into local Code tab sessions, alongside servers from `~/.claude.json` and `.mcp.json`. A server you define in `claude_desktop_config.json` is available in both the Desktop chat surface and local Code tab sessions.

If you define the same server name in `claude_desktop_config.json` and in `~/.claude.json` or `.mcp.json`, the Code tab in local sessions connects once and uses the `claude_desktop_config.json` definition.

The app also re-delivers stdio servers from `~/.claude.json` to the embedded CLI in local sessions. When the top level of `~/.claude.json` (user scope) and `.mcp.json` define the same stdio server name, the Code tab uses the `~/.claude.json` definition, departing from the CLI [scope hierarchy](https://code.claude.com/docs/en/mcp.md#scope-hierarchy-and-precedence).

> [!NOTE]
>
> The standalone CLI does not read `claude_desktop_config.json`. On macOS and WSL, run `claude mcp add-from-claude-desktop` to copy those servers into `~/.claude.json`. See [Import MCP servers from Claude Desktop](https://code.claude.com/docs/en/mcp.md#import-mcp-servers-from-claude-desktop) for the import flow and scope options.

### Feature comparison

This table compares core capabilities between the CLI and Desktop. For a full list of CLI flags, see the [CLI reference](https://code.claude.com/docs/en/cli-reference.md).

| Feature | CLI | Desktop |
| - | - | - |
| Permission modes | All modes including `dontAsk` | Manual, Accept edits, Plan, and Auto. Bypass permissions appears in the mode selector once enabled: through the Settings toggle on Pro and Max plans, or through organization policy on Team and Enterprise plans |
| [Third-party providers](https://code.claude.com/docs/en/third-party-integrations.md) | Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry | Anthropic's API by default. For gateway routing, see [connect the desktop app to a gateway](https://code.claude.com/docs/en/llm-gateway-connect.md#desktop-app). To run the Code tab on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or a self-hosted LLM gateway, see [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview). |
| [MCP servers](https://code.claude.com/docs/en/mcp.md) | Configure in settings files | Connectors UI for local and SSH sessions, or settings files |
| [Plugins](https://code.claude.com/docs/en/plugins/overview.md) | `/plugin` command | Plugin manager UI |
| @mention files | Text-based | With autocomplete, except for a cloud session's first message |
| File attachments | Not available | Images, PDFs |
| Session isolation | [`--worktree`](https://code.claude.com/docs/en/cli-reference) flag | [Run a session in its own worktree](#run-a-session-in-its-own-worktree) |
| Multiple sessions | Separate terminals | Sidebar tabs |
| Recurring tasks | Cron jobs, CI pipelines | [Scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks.md) |
| Computer use | [Enable via `/mcp`](https://code.claude.com/docs/en/computer-use) on macOS | [App and screen control](#let-claude-use-your-computer) on macOS and Windows |
| iOS simulator | Drive the simulator via [computer use](https://code.claude.com/docs/en/computer-use.md#test-a-simulator-flow) | [iOS Simulator pane](https://code.claude.com/docs/en/desktop-ios-simulator.md) opens automatically |
| Dispatch integration | Not available | [Dispatch sessions](#sessions-from-dispatch) in the sidebar |
| Scripting and automation | [`--print`](https://code.claude.com/docs/en/cli-reference), [Agent SDK](https://code.claude.com/docs/en/headless.md) | Not available |

### What's not available in Desktop

The following features aren't available in Desktop, except where noted:

* **Third-party providers**: Desktop connects to Anthropic's API by default. To route Desktop through a gateway, or to run the Code tab on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or a self-hosted LLM gateway, follow the links in the [Third-party providers row](#feature-comparison).
* **Linux (beta)**: Computer Use isn't yet available in the Linux desktop app. See [Claude Desktop on Linux](https://code.claude.com/docs/en/desktop-linux.md).
* **Inline code suggestions**: Desktop doesn't offer autocomplete-style code completions. It works through conversational prompts and explicit code changes, and can [suggest your next prompt](#accept-a-suggested-prompt) after Claude replies.
* **Agent teams**: coordinated teams, where Claude as the team lead assigns tasks to teammates from a shared task list, are available in the [CLI](https://code.claude.com/docs/en/agent-teams.md), not in Desktop. For multi-agent work inside one session, use [dynamic workflows](https://code.claude.com/docs/en/workflows.md), which run in Desktop; Claude can also [message and manage your other sessions](#work-across-sessions) directly.
* **Terminal-dialog commands**: built-in commands that open an interactive panel in the terminal behave differently in the Code tab. Edit [settings files](https://code.claude.com/docs/en/settings.md) directly to manage permission rules and configuration, or run the commands from the standalone CLI.
  * Commands with no argument form, such as `/permissions`, reply with `isn't available in this environment`.
  * `/config` opens **Settings > Code** or **Settings > Claude Code**.

## Troubleshooting

The sections below cover issues specific to the desktop app. For runtime API errors that appear in the chat such as `API Error: 500`, `529 Overloaded`, `429`, or `Prompt is too long`, see the [Error reference](https://code.claude.com/docs/en/errors.md).

### Check your version

To see which version of the desktop app you're running:

* **macOS**: click **Claude** in the menu bar, then **About Claude**
* **Windows**: click **Help**, then **About Claude**

Click the version number to copy it to your clipboard.

#### Claude Code version in the Code tab

To see which version of Claude Code a session runs, type `/status` in a local session in the **Code** tab and read the **Claude Code** row, which shows a version such as `2.1.286`.

To get a newer version for local sessions, open **Claude > Check for Updates…** on macOS or **Help > Check for Updates…** on Windows, then start a new session.

In a local session, the **Code** tab runs its own copy of Claude Code, which has its own version number. The desktop app downloads and updates that copy, so it can differ from the `claude` command in your terminal, and updating one doesn't update the other.

### Check which layout you have

If a new session shows the [environment](#start-a-session) above the prompt box instead of under it, you have the earlier layout:

* **[Desktop older than v2.37337.0](#check-your-version)**: update to get the current layout. Select **Claude > Check for Updates…** on macOS or **Help > Check for Updates…** on Windows.
* **[Third-party provider](https://code.claude.com/docs/en/third-party-integrations.md) with sessions on your computer**: the current layout requires Claude Desktop v3.1623.0 or later, so [check your version](#check-your-version). To update, select **Claude > Check for Updates…** on macOS or **Help > Check for Updates…** on Windows. If your organization [turns off auto-updates](#device-management-policies), **Check for Updates…** is hidden, so ask your administrator for v3.1623.0 or later.
* **Third-party provider with sessions on your organization's infrastructure**: the current layout requires Claude Desktop v4.29.0 or later, so [check your version](#check-your-version). If you're on an older version, ask your administrator for v4.29.0 or later. If you don't know where your sessions run, ask your administrator.

In the earlier layout, choose the environment and any project folder or repository above the prompt box, and the permission mode and model in the row under it. The earlier layout lacks the [session details panel](#see-session-details) and [saved local and SSH environments](#create-a-saved-environment).

### 403 or authentication errors in the Code tab

If you see `Error 403: Forbidden` or other authentication failures when using the Code tab:

1. Sign out and back in from the app menu. This is the most common fix.
2. Verify you have an active paid subscription: Pro, Max, Team, or Enterprise.
3. If the CLI works but Desktop does not, quit the desktop app completely, not just close the window, then reopen and sign in again.
4. Check your internet connection and proxy settings.

### Blank or stuck screen on launch

If the app opens but shows a blank or unresponsive screen:

1. Restart the app.
2. Check for pending updates. On macOS and Windows the app auto-updates on launch; on Linux, update through apt as described in [Claude Desktop on Linux](https://code.claude.com/docs/en/desktop-linux.md).
3. On a managed network, confirm your firewall allows the CDN hosts in [network access requirements](#network-access-requirements).
4. On Windows, check Event Viewer for crash logs under **Windows Logs → Application**.

### "Failed to load session"

If you see `Failed to load session`, the selected folder may no longer exist, a Git repository may require Git LFS that isn't installed, or file permissions may prevent access. Try selecting a different folder or restarting the app.

### Session not finding installed tools

If Claude can't find tools like `npm`, `node`, or other CLI commands, verify the tools work in your regular terminal, check that your shell profile properly sets up PATH, and restart the desktop app to reload environment variables.

### Git and Git LFS errors

Sessions that run in their own worktree need Git. If you see "Git is required," install [Git](https://git-scm.com/downloads), or [Git for Windows](https://git-scm.com/downloads/win) on Windows, and try again. On Windows, Claude Desktop versions before 1.49585.0 asked for Git before starting any local session; if you see that prompt and aren't using worktrees, update the app.

If you see "Git LFS is required by this repository but is not installed," install Git LFS from [git-lfs.com](https://git-lfs.com/), run `git lfs install`, and restart the app.

### MCP servers not working on Windows

If MCP server toggles don't respond or servers fail to connect on Windows, check that the server is properly configured in your settings, restart the app, verify the server process is running in Task Manager, and review server logs for connection errors.

### SSH host key verification failed

Each of these messages means that Desktop refused a [host key](#check-a-remote-machines-host-key):

* `SSH host key verification failed` or `Host denied (verification failed)` under **View details** on a `Couldn't connect to <host>` card
* `Connection failed: Host key changed or not trusted` by the prompt box or after **Test connection**
* `<host>'s host key is not trusted` or `<host>'s host key has changed` on a disconnected session

Desktop usually refuses a key because it differs from the one saved on your computer, or because no key is saved for that machine. A machine that was rebuilt or reinstalled usually presents a new key, and so does something that intercepts the connection. Check the key before you connect again, starting from what Desktop shows with the message:

* **You're on Windows, and Desktop says `Connection failed: Host key changed or not trusted`**: first rule out a [missing OpenSSH client](#ssh-host-key-refused-on-windows-without-an-openssh-client)
* **Desktop tells you to set `UserKnownHostsFile`**: in `~/.ssh/config`, set it to `~/.ssh/known_hosts`, then [check the key from a terminal](#check-the-host-key-from-a-terminal)
* **You see a Review new key button**: select it, and [compare](#check-a-remote-machines-host-key) the fingerprint that Desktop shows with the machine's own. If they match, select **Trust new key** to replace the saved key. Otherwise select **Cancel**.
* **You see no Review new key button, Desktop shows `Couldn't show the new key`, or Desktop refuses the key again after Trust new key**: [check the key from a terminal](#check-the-host-key-from-a-terminal)

#### Check the host key from a terminal

Run `ssh <SSH host>` on your computer, with the **SSH host** value of your [SSH connection](#ssh-sessions) in Desktop. Add `-p <SSH port>` if the connection has an **SSH port** value. On Windows, use PowerShell, because Desktop doesn't connect with the `ssh` in Git Bash or WSL. If PowerShell finds no `ssh`, [install Microsoft's OpenSSH client](#ssh-host-key-refused-on-windows-without-an-openssh-client).

Note which machine `ssh` names in its message, which can be a jump host and not `<SSH host>`, then follow the case that fits:

* **`ssh` asks whether to continue connecting**: [compare](#check-a-remote-machines-host-key) the fingerprint that it shows with that machine's own. Answer `yes` only if they match.
* **`ssh` warns that the host key has changed**: [compare](#check-a-remote-machines-host-key) the warning's fingerprint with that machine's own. Only if they match, delete the line that `Offending <type> key in <file>:<line>` names and rerun `ssh`. If `ssh` warns again about another line, compare, delete and rerun as before.
* **`ssh` refuses a key that it doesn't know, without asking**: get that machine's `known_hosts` line from whoever manages it, not over the connection that you're checking. Add the line to your `known_hosts` file, with the name from `ssh`'s message as its host name, and rerun `ssh`.
* **`ssh` goes on to sign in without asking you about the host key**: don't type a password yet. [Check the keys that `ssh` already trusts](#check-the-keys-that-ssh-already-trusts).

Once `ssh` accepts a key that you checked or added, retry in Desktop. If Desktop refuses the key again, see [Get Desktop's logs for an SSH problem](#get-desktops-logs-for-an-ssh-problem).

##### Check the keys that `ssh` already trusts

Rerun the same `ssh` command with `-v -S none` added. In its output, a `Server host key:` line shows a fingerprint, and the next `Host '<name>' is known` line names the machine that it belongs to. [Compare](#check-a-remote-machines-host-key) each fingerprint that you find with that machine's own.

* **A jump host has no `Server host key:` line**: run `ssh -v -S none <jump host>` too, and compare that fingerprint in the same way.
* **A fingerprint doesn't match, or you can't check it**: don't connect again. Remove the saved key: under `Host '<name>' is known`, the line `Found key in <file>:<line>` names the file that holds it. Run `ssh-keygen -R "<name>" -f <file>`. If you keep host keys in more than one file, remove the key from each. If you can't change a file, tell whoever manages your computer.
* **Every fingerprint matches**: retry in Desktop. If Desktop refuses the key again, see [Get Desktop's logs for an SSH problem](#get-desktops-logs-for-an-ssh-problem).

### SSH host key refused on Windows without an OpenSSH client

On Windows without an OpenSSH client, Desktop refuses even a correct host key, with `Connection failed: Host key changed or not trusted`. It needs the client to look up saved keys. To see whether you have one, run `ssh` in PowerShell. If PowerShell doesn't recognize `ssh`, install [Microsoft's OpenSSH client](https://learn.microsoft.com/windows-server/administration/openssh/openssh_install_firstuse) and restart Desktop.

Then connect again. If Desktop asks whether to connect for the first time, [check the machine's host key](#check-a-remote-machines-host-key) before you trust it. If Desktop still refuses the key, follow the other cases under [SSH host key verification failed](#ssh-host-key-verification-failed).

### SSH connection fails after you log in

Find the card's title, or the code that ends the error message, in this table, then do what the last column says. To see the message, select **View details** on the failure card.

| Title on the card | Code | What to do |
| - | - | - |
| `<host>'s SSH server has SFTP turned off` | `[SFTP_UNAVAILABLE]` | Turn on SFTP in the server's `sshd_config`, as described under [remote machine requirements](#remote-machine-requirements-for-ssh-sessions) |
| `SFTP doesn't start on <host>` | `[SFTP_NOT_STARTED]` | Connect to the same host with `sftp` in a terminal on your computer to see what stops it, then check the settings and files that Desktop's message names |
| `<host> allows too few SSH sessions per connection` | `[SESSION_LIMIT]` | Update to Claude Desktop v3.1623.0 or later, or raise `MaxSessions` in the server's `sshd_config`, for example to OpenSSH's default of 10 |
| `<host> is out of disk space` | `[ENOSPC]` or `[EDQUOT]` | Free space or quota on the remote machine, in your home directory or `/tmp` |
| `Free up disk space on this computer` | `[ENOSPC]` or `[EDQUOT]`, in a message that starts with `Couldn't prepare the deploy locally` | Free space on your computer |
| `Claude Code won't start on <host>` | `[CLI_UNRESPONSIVE]` | Wait a minute, then try again. If it keeps failing, run the command that the message names on the remote machine to see whether Claude Code answers there. |

For any other message, check the [remote machine requirements](#remote-machine-requirements-for-ssh-sessions).

### Get Desktop's logs for an SSH problem

You get `ssh.log`, Desktop's record of its SSH connections, in a zip file of Desktop's logs that you save from the **Help** menu. To save it, open **Help > Troubleshooting** and select the item for your system:

* **macOS**: **Show Logs in Finder**
* **Windows**: **Show Logs in File Explorer**
* **Linux**: **Show Logs in File Manager**

Look through the files before you send them, because they can include names and other details from your environment. `<host>` and `<user>` stand for names that Desktop replaced. Desktop doesn't replace every name, and an SSH host or user name can still appear as written. If you send the zip file to someone, tell them which host failed and when, because the logs may not name it.

The zip file doesn't hold the log of the helper program that Desktop installs on the remote machine. To get that log as well, copy `remote-server.log` from the helper's folder under [`~/.claude/remote/run/`](#files-and-processes-on-the-remote-machine) in the home directory of the user who connected. Look through that file too before you send it.

### App won't quit

* **macOS**: press Cmd+Q. If the app doesn't respond, use Force Quit with Cmd+Option+Esc, select Claude, and click Force Quit.
* **Windows**: use Task Manager with Ctrl+Shift+Esc to end the Claude process.

### Windows-specific issues

* **PATH not updated after install**: open a new terminal window. PATH updates only apply to new terminal sessions.
* **Concurrent installation error**: if you see an error about another installation in progress but there isn't one, try running the installer as Administrator.

### "Branch doesn't exist yet" when opening in CLI

Cloud sessions can create branches that don't exist on your local machine. Click the branch name in the session and select **Copy branch name**, then fetch it locally:

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Still stuck?

* Open Help → Get Support in the desktop app, or visit the [Claude support center](https://support.claude.com/) directly
* For problems that also reproduce in the standalone `claude` CLI, search or file a bug on [GitHub Issues](https://github.com/anthropics/claude-code/issues)

When reporting a problem, include your desktop app version, your operating system, the exact error message, and relevant logs. On macOS, check Console.app. On Windows, check Event Viewer → Windows Logs → Application. Review log excerpts before posting them to a public issue; they can include file paths and other details from your environment.
