> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mods overview

> Add panes, commands, and tool call rules to Claude Code with a mod. See what a mod can do, how to make or install one, and where mods run.

A mod is a [plugin](https://code.claude.com/docs/en/plugins/overview.md) that changes how Claude Code looks and behaves. It's made of JavaScript or TypeScript event handlers: Claude Code calls one when an event happens, such as a tool call, a submitted prompt, or a part of the interface being drawn, and the handler can watch the event, change it, or take it over. Use a mod to add a feature of your own to Claude Code, such as a pane that charts how full your context is after each request. For the files in a mod and a complete example, see [How a mod works](#how-a-mod-works).

> [!NOTE]
>
> Claude Code's existing [hooks](https://code.claude.com/docs/en/hooks.md) also run on events, as a shell command, HTTP request, or prompt you configure in a settings file. A mod's handlers are functions that run inside Claude Code instead. Claude Code calls both kinds hooks: on these pages, "hook" means a mod's handler, and the settings-file kind is a "settings hook".

## What a mod can do

Settings hooks, skills, status lines, and MCP servers work from outside Claude Code: each one runs a script, or gives Claude text or tools. A mod runs inside Claude Code, so it can do things they can't:

* **Draw an interface you can use**: a pane beside the transcript or a band above the prompt, with tabs, buttons, and text fields. See [Draw in the interface](https://code.claude.com/docs/en/plugins/mods/interface.md).
* **Redraw Claude Code's own interface**: replace or restyle parts Claude Code draws itself, such as a tool call's row, the spinner, or the dialog Claude asks questions in. See [Change what Claude Code already draws](https://code.claude.com/docs/en/plugins/mods/interface.md#change-what-claude-code-already-draws).
* **Step into a tool call or a request**: for example, hold a tool call while you ask the user a question, answer it without running the tool, or send one request to a different model. See [Guard or change a tool call](https://code.claude.com/docs/en/plugins/mods/events.md#guard-or-change-a-tool-call) and [Follow a turn](https://code.claude.com/docs/en/plugins/mods/events.md#follow-a-turn).
* **Run your own code on a command**: a `/command` that runs your function at once, with no Claude turn, even while Claude is working. See [Add a command or a tool](https://code.claude.com/docs/en/plugins/mods/api.md#add-a-command-or-a-tool).
* **Share data between hooks**: a mod's hooks share the variables in its file, so what one hook records, another can show. For example, one hook can count tool calls while another shows the count beside the spinner, or one can read each request's token usage while another charts it in a pane. See [React to events](https://code.claude.com/docs/en/plugins/mods/events.md).

Mods work in the Claude Code CLI, the Code tab of the Claude Desktop app, and the VS Code extension. See [Where mods run](#where-mods-run) for how they behave elsewhere, such as in `claude -p` and cloud sessions. If a settings hook, a skill, or an MCP server already does what you need, [compare them](#compare-mods-settings-hooks-skills-and-mcp-servers) before you write a mod. To manage mods for an organization, see [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin.md).

## Get a mod

To start with a mod:

* **Use one you already have**: some of Claude Code's own features are mods, such as `/diff`. See [Mods built into Claude Code](#mods-built-into-claude-code).
* **Make one**: describe what you want in a Claude Code session, and Claude writes the mod. See [Ask Claude for a mod](https://code.claude.com/docs/en/plugins/mods/create.md#ask-claude-for-a-mod). To learn how a mod's code works, [write one yourself](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself).
* **Install one**: see [Install or update a mod](#install-or-update-a-mod), or [try a sample mod](#try-a-sample-mod)

### Install or update a mod

> [!WARNING]
>
> A mod is code that runs with your permissions. It can read and write your files, start processes, and make network requests. Install mods only from authors and marketplaces you trust. See [Decide whether to trust a mod](#decide-whether-to-trust-a-mod).

A mod installs as a plugin, from a marketplace. Give the plugin's name, an `@`, and the marketplace's name. These examples install a plugin named `token-chart` from a marketplace named `your-org`:

* In a Claude Code session, run `/plugin install token-chart@your-org`.
* In your shell, run `claude plugin install token-chart@your-org`.

[Install plugins](https://code.claude.com/docs/en/plugins/install.md) covers marketplaces, scopes, the VS Code extension and the Desktop app, and [keeping plugins updated](https://code.claude.com/docs/en/plugins/install.md#keep-plugins-updated), all of which apply to a plugin that contains a mod without changes.

If you install or update a mod from your shell while a session is open, run `/reload-plugins` in that session to load it. Otherwise it loads the next time you start Claude Code.

### Try a sample mod

Anthropic shares sample mods in the [`claude-code/mods` directory of the `claude-code-playground` repository](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods). Each one is a complete plugin, and its README says how it was built. The repository shares them as they are, without support.

* [`token-weather`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/token-weather): draws a forecast of your context window above the prompt
* [`blast-radius`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/blast-radius): holds a risky shell command, such as `rm -rf` or a force push, and shows what it would change, with buttons to proceed or cancel
* [`replay-theater`](https://github.com/anthropics/claude-code-playground/tree/main/claude-code/mods/replay-theater): adds a `/replay` command that steps through the file edits Claude made in the last turn

A sample mod runs with your permissions. To see what one does before you load it, [list its hooks and calls](#list-what-a-mod-does-before-you-install-one).

To try one, clone the repository and [load the mod's directory for one session](https://code.claude.com/docs/en/plugins/create.md#load-a-directory-or-archive-for-one-session) with `--plugin-dir`. To confirm the mod loaded, [check which mods the session loaded](#see-which-mods-a-session-loaded).

To keep one, [add the clone's `claude-code/mods` directory as a marketplace](https://code.claude.com/docs/en/plugins/install#add-a-marketplace), then install the mod from `claude-code-playground-mods`. The marketplace points at your clone, so the mod stops loading if you move or delete it.

## Decide whether to trust a mod

A mod is code that runs with your permissions, inside Claude Code. Install mods only from authors and [marketplaces you trust](https://code.claude.com/docs/en/plugins/security.md).

### What a mod can reach

A mod runs with your permissions, so before you install one, know what it has access to. Once it loads, a mod can:

* **Act on your machine as you**: read and write files anywhere your user account can, start programs, and make network requests
* **Read your secrets**: environment variables and settings files, including an API key you keep in either
* **See your session**: every prompt you send and every tool call Claude makes
* **Change your session**: rewrite a prompt or a tool call, submit a prompt as if you had typed it, or send a message to another of your sessions
* **Act without asking you**: approve a tool call before you're asked
* **Spend your usage**: call a model on your plan or API key

Mods aren't sandboxed. If you turn on [sandboxing](https://code.claude.com/docs/en/sandboxing.md), the sandbox isolates the Bash commands Claude runs, and a process that a mod starts runs outside it.

With [managed settings](https://code.claude.com/docs/en/settings.md#check-what-your-organization-enforces) or a Team or Enterprise [`/login`](https://code.claude.com/docs/en/authentication#authentication-precedence) as the session's credential, by default a mod's approval doesn't get a call past your `ask` rules or `PreToolUse` hooks. Without either, a mod can approve a call that an `ask` rule would prompt for, or that your `PreToolUse` hook blocked. To check when a mod can also approve a call that a `deny` rule refuses, see [Extend permissions with hooks](https://code.claude.com/docs/en/permissions.md#precedence-among-rules-hooks-and-mods).

A mod can restyle much of Claude Code's interface, but not the permission prompt. It can't change what a prompt shows you.

### List what a mod does before you install one

Before you install a mod, you can list which events it handles and what it asks Claude Code to do, such as read a file or make a network request, without running it. Get the plugin's files first, for example by cloning its repository. Then, in your shell, run `claude plugin validate` on the plugin's directory:

```bash theme={null}
claude plugin validate ./some-mod
```

The `hooks:` and `calls:` lines in the output list the events the mod handles and what it asks Claude Code to do. [Review what a mod can do](https://code.claude.com/docs/en/plugins/mods/admin.md#review-what-a-mod-can-do) shows the output and which calls to look for.

## Turn mods on or off

Mods are on by default. In the terminal, use Claude Code v2.1.287 or later. The Desktop app includes its own copy of Claude Code, and mods work there from v2.1.286. Check the version in the place you use mods:

* **Terminal**: in your shell, run `claude --version`. If yours is older, [update Claude Code](https://code.claude.com/docs/en/setup.md#update-claude-code).
* **Desktop app**: in a local session in the Code tab, enter `/status` and read the **Claude Code** row, which shows a version such as `2.1.286`. If yours is older, [update the Desktop app](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab).

To turn mods off, choose how many to stop, and for how long. To turn them back on, undo the same change:

* **One mod**: disable or uninstall its plugin from the [**Installed** tab in `/plugin`](https://code.claude.com/docs/en/plugins/install#manage-installed-plugins)
* **Every installed mod, for one session**: start Claude Code with [`--safe-mode`](https://code.claude.com/docs/en/cli-reference#cli-flags), which also disables your other customizations
* **Every mod you installed, in every session**: set [`"disableAllHooks": true`](https://code.claude.com/docs/en/settings-reference#disableallhooks) in `~/.claude/settings.json`. Your settings hooks and custom status line stop too. What your organization manages keeps running.

If you use Claude Code through an organization, an administrator can also limit which mods load. Administrators start at [Stop user-installed mods from loading](https://code.claude.com/docs/en/plugins/mods/admin.md#stop-user-installed-mods-from-loading).

`disableAllHooks` and your organization's `allowManagedModsOnly` stop a mod and leave the rest of its plugin in place: the plugin stays installed, and its skills, commands, agents, and MCP servers load. Other settings and flags reach further. [`disableAllHooks`](https://code.claude.com/docs/en/settings-reference#disableallhooks) and [What runs under `allowManagedHooksOnly`](https://code.claude.com/docs/en/settings-reference#what-runs-under-allowmanagedhooksonly) list what each one does to a plugin and its settings hooks.

To find out whether mods can load for you, see [Check whether mods can load](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#check-whether-mods-can-load).

> [!NOTE]
>
> If you set `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` during early access, remove it. Claude Code v2.1.287 and later ignores it, so setting it to `0` doesn't keep mods off.

### See which mods a session loaded

To see which mods a terminal session loaded, run `/plugin` at the Claude Code prompt. A dim line under the tabs gives the count and the names, such as `1 mod active · first-mod`. If a mod you installed isn't named there, see [Find out why a mod does nothing](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing).

## How a mod works

A mod is a [plugin](https://code.claude.com/docs/en/plugins/overview.md) whose code registers event handlers, called hooks. Claude Code runs a hook when its event happens, such as when Claude calls a tool or when the spinner is drawn. A small mod has three files:

```text theme={null}
first-mod/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── register.js
```

* **`plugin.json`**: the plugin's [manifest](https://code.claude.com/docs/en/plugins/manifest-reference.md)
* **`hooks.json`**: [points to your code file](https://code.claude.com/docs/en/plugins/mods/reference.md#files)
* **`register.js`**: [your code](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself), called the hooks module. It tells Claude Code which events to run your functions on.

This is a complete `register.js`. It counts the tool calls Claude makes and shows the count beside the spinner while Claude works, as in `Thinking · tool calls: 3…`.

```javascript hooks/register.js theme={null}
// The count, shared by the two hooks below
let calls = 0

// Claude Code calls this once when the mod loads
export function register(on) {
  // Runs each time Claude is about to use a tool
  on('tool.call', async ($, e, next) => {
    calls += 1
    // Ask Claude Code to draw the interface again, so the new count shows
    $.ui.invalidate('ui.render')
    // Let the tool run as usual
    return next(e)
  })

  // Runs each time Claude Code draws the spinner
  on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
    // Keep Claude Code's spinner, with the count added after its word
    return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
  })
}
```

The file registers two hooks, and both use the `calls` variable at the top:

* **The [`tool.call`](https://code.claude.com/docs/en/plugins/mods/reference#tools) hook** runs each time Claude is about to use a tool. It adds one to `calls`, asks Claude Code to draw the interface again, and lets the tool run as usual.
* **The [`ui.render`](https://code.claude.com/docs/en/plugins/mods/reference#interface) hook** runs each time Claude Code draws the spinner. It keeps Claude Code's own spinner and adds the count after the word.

This recording shows the mod at work. Watch the spinner line above the prompt box: while Claude lists a directory and reads two files, it reads `Thinking · tool calls: 1…`, then `2…`, then `3…`.

<video autoPlay muted loop playsInline controls src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-overview-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=00a18aa0743b59a700f0275ce226e6d1" aria-label="In a Claude Code session, the prompt 'list the files here and read the README' is typed and sent. While Claude works, the spinner reads 'Thinking · tool calls: 1', then 2, then 3, as Claude lists the files and reads two of them." />

### What a hook can do with an event

Claude Code runs your hook before it acts on the event, so the hook decides what happens next. It can:

* **Observe**: note what's happening and let it continue unchanged, as the `tool.call` hook in the example does
* **Rewrite**: change the event before it continues, as the `ui.render` hook does when it adds the count to the spinner
* **Answer**: handle the event itself, so the usual behavior doesn't run, such as refusing a command

To do anything outside its own code, such as draw, add a command, call a model, read a file, start a process, or make a network request, a hook calls the mods API. A hook has no other way to do those things, which is why Claude Code can [list what a mod does](#list-what-a-mod-does-before-you-install-one) before you install it.

For the code behind each choice, see [React to events](https://code.claude.com/docs/en/plugins/mods/events.md#how-a-hook-handles-an-event). For what a hook can call, see [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api.md).

### Where mods run

A mod's hooks run in every kind of session that loads the plugin, whichever provider serves the model, including Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. Drawing is narrower: what a mod draws appears in the terminal, the Desktop app, and the VS Code extension. This table lists each place you might run Claude Code:

| Where you run Claude Code | Hooks run | What the mod draws appears |
| :- | :- | :- |
| `claude` in a terminal, including an editor's integrated terminal and the JetBrains plugin | Yes | Yes |
| The Code tab of the Desktop app, except in a WSL session | Yes | Yes, except elements the [elements table](https://code.claude.com/docs/en/plugins/mods/reference.md#elements) marks terminal-only |
| A [WSL session](https://code.claude.com/docs/en/desktop-wsl.md) in the Desktop app | No, because plugins aren't available in WSL sessions | No |
| The VS Code extension's chat panel | Yes | Yes, with extension version 2.1.299 or later. A session that [doesn't fetch feature flags](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching), such as one on Amazon Bedrock, needs 2.1.304 or later. The [render sites](https://code.claude.com/docs/en/plugins/mods/reference.md#render-sites) and [elements](https://code.claude.com/docs/en/plugins/mods/reference.md#elements) tables mark what the panel draws. |
| `claude -p` and the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview.md) | Yes | No |
| [Remote Control](https://code.claude.com/docs/en/remote-control.md) from claude.ai or the mobile app | Yes, in the session on your machine | In the terminal on your machine |
| A [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md) | Yes, for a plugin that [reaches the cloud session](https://code.claude.com/docs/en/cloud-environments.md#what-carries-over-from-your-setup) | No |

A mod that draws can check which app it's running in, and fall back to a line in the transcript or a command's text reply where nothing draws.

## Control mods for your organization

Administrators decide whether mods run and which ones, through [managed settings](https://code.claude.com/docs/en/managed-settings.md). [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin.md) covers what happens by default, how to review a mod, and how to enforce a policy with a mod of your own.

## Compare mods, settings hooks, skills, and MCP servers

Mods, settings hooks, skills, and MCP servers overlap. This table shows what each one is and when to pick it.

| | Mod | Settings hook | Skill | MCP server |
| :- | :- | :- | :- | :- |
| What it is | Functions in a plugin that Claude Code calls in its own process | A shell command, HTTP request, or prompt that Claude Code runs on a lifecycle event | A `SKILL.md` file of instructions Claude reads | An external process or service that gives Claude tools |
| What it can change | Tool calls, prompts, commands, turns, and what the interface draws | Whether a tool call or prompt goes ahead, a tool call's arguments and result, and context added for Claude | What Claude knows and does | Which tools Claude has |
| Can it draw in the interface | Yes | No | No | No |
| What you write | JavaScript or TypeScript | A script and a `settings.json` entry | Markdown | A server in any language |
| Pick it when | You want a pane, a band above the prompt, a custom command, or to rewrite an event | You want to block, allow, or log an event with a script you already have | You keep pasting the same instructions into chat | Claude needs to reach an external system |

Each of the others has its own page: [Hooks](https://code.claude.com/docs/en/hooks.md), [Skills](https://code.claude.com/docs/en/skills.md), and [MCP](https://code.claude.com/docs/en/mcp.md). A plugin can hold all of them, so a mod can ship in the same plugin as a skill and an MCP server.

## Mods built into Claude Code

Some of Claude Code's own features are mods. To see the ones your session has, run `/plugin` at the Claude Code prompt and go to the **Installed** tab, which lists them under **Built-in**. You can't update or uninstall a built-in mod, and the table's last column says how to turn each one off. The [`mods active` line](#see-which-mods-a-session-loaded) omits built-in mods.

This table lists each entry by the name `/plugin` shows:

| Name in `/plugin` | What it does | Where it's on | How to turn it off |
| :- | :- | :- | :- |
| `cc-plugin-agents-md` | Loads `AGENTS.md` as project instructions | Every session, apart from [the ones that can't read `AGENTS.md`](https://code.claude.com/docs/en/memory#when-agents-md-support-is-unavailable) | Disable it in `/plugin`, or [choose which instruction files load](https://code.claude.com/docs/en/memory.md#choose-which-instruction-files-load) |
| `cc-plugin-diff` | Takes over [`/diff`](https://code.claude.com/docs/en/interactive-mode#review-changes-with-%2Fdiff) and draws its pane | Interactive terminal sessions | Disable it in `/plugin`. `/diff` stays, and Claude Code's built-in version of the command answers it. |
| `cc-plugin-plugin-authoring` | Gives Claude the [`plugin-authoring` skill](https://code.claude.com/docs/en/plugins/mods/create#ask-claude-for-a-mod) for writing mods. It holds a skill and no mod code. | Unless Anthropic has turned installed mods off remotely | Disable it in `/plugin` |
| `cc-plugin-sec-default` | Guards what your organization manages from the mods a user installs | [Where the guard loads](https://code.claude.com/docs/en/plugins/mods/admin.md#know-what-happens-by-default) | You can't. An administrator [sets the order](https://code.claude.com/docs/en/plugins/mods/admin.md#install-your-organizations-mods) in managed settings |
| `cc-plugin-telemetry` | Sends the analytics records that Claude Code and its built-in mods log | Wherever Claude Code's own analytics are on | Disable it in `/plugin`, or turn analytics off, for example with [`DISABLE_TELEMETRY`](https://code.claude.com/docs/en/env-vars) |
| `cc-plugin-you-should-know` | [You should know](https://code.claude.com/docs/en/interactive-mode.md#you-should-know-suggestions): a side agent shows a note above the prompt when it finds something you might have missed | Off until you [turn it on](https://code.claude.com/docs/en/interactive-mode.md#you-should-know-suggestions) | Disable it in `/plugin` |

The settings and flags that stop installed mods, such as `disableAllHooks`, `--bare`, and `--safe-mode`, don't stop built-in mods.

### Read the source of built-in mods

The source of some of these mods is public in the [`mods` directory of the Claude Code repository](https://github.com/anthropics/claude-code/tree/main/mods). Each one is a complete plugin with its hooks module and tests:

* [`diff`](https://github.com/anthropics/claude-code/tree/main/mods/diff): the `/diff` pane, with buttons bound to keyboard actions and scrolling the mod handles itself
* [`agents-md`](https://github.com/anthropics/claude-code/tree/main/mods/agents-md): loads `AGENTS.md` as project instructions, with a [`userConfig`](https://code.claude.com/docs/en/plugins/components#user-configuration) option
* [`sec-default`](https://github.com/anthropics/claude-code/tree/main/mods/sec-default): the guard described in [Know what happens by default](https://code.claude.com/docs/en/plugins/mods/admin.md#know-what-happens-by-default), a model for a mod that enforces policy
* [`telemetry`](https://github.com/anthropics/claude-code/tree/main/mods/telemetry): adds methods that other mods can call, and ships their types

## Next steps

* [Create a mod](https://code.claude.com/docs/en/plugins/mods/create.md): build one that counts tool calls, shows the count beside the spinner, and adds a command, and learn the edit and reload loop
* [Draw in the interface](https://code.claude.com/docs/en/plugins/mods/interface.md): panes, the band above the prompt, buttons, text fields, and state
* [React to events](https://code.claude.com/docs/en/plugins/mods/events.md): tool calls, prompts, turns, and the order mods run in
* [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api.md): commands, tools, model calls, timers, and files
* [Test a mod](https://code.claude.com/docs/en/plugins/mods/test.md): automated tests that run without a session
* [Troubleshoot a mod](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md): the reasons a mod does nothing, and the debug log
* [Manage mods for your organization](https://code.claude.com/docs/en/plugins/mods/admin.md): defaults, managed settings, reviewing a mod, and policy mods
* [Mods reference](https://code.claude.com/docs/en/plugins/mods/reference.md): events, methods, elements, and limits
