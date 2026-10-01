> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mods overview

> Add panes, commands, and tool call rules to Claude Code with a mod. See what a mod can do, how to make or install one, and where mods run.

A mod is a [plugin](/docs/en/plugins/overview) that changes how Claude Code looks and behaves. It's made of JavaScript or TypeScript event handlers: Claude Code calls one when an event happens, such as a tool call, a submitted prompt, or a part of the interface being drawn, and the handler can watch the event, change it, or take it over. Use a mod to add a feature of your own to Claude Code, such as a pane that charts how full your context is after each request. For the files in a mod and a complete example, see [How a mod works](#how-a-mod-works).

<Note>
  Claude Code's existing [hooks](/docs/en/hooks) also run on events, as a shell command, HTTP request, or prompt you configure in a settings file. A mod's handlers are functions that run inside Claude Code instead. Claude Code calls both kinds hooks: on these pages, "hook" means a mod's handler, and the settings-file kind is a "settings hook".
</Note>

## What a mod can do

Settings hooks, skills, status lines, and MCP servers work from outside Claude Code: each one runs a script, or gives Claude text or tools. A mod runs inside Claude Code, so it can do things they can't:

* **Draw an interface you can use**: a pane beside the transcript or a band above the prompt, with tabs, buttons, and text fields. See [Draw in the interface](/docs/en/plugins/mods/interface).
* **Redraw Claude Code's own interface**: replace or restyle parts Claude Code draws itself, such as a tool call's row, the spinner, or the dialog Claude asks questions in. See [Change what Claude Code already draws](/docs/en/plugins/mods/interface#change-what-claude-code-already-draws).
* **Step into a tool call or a request**: for example, hold a tool call while you ask the user a question, answer it without running the tool, or send one request to a different model. See [Guard or change a tool call](/docs/en/plugins/mods/events#guard-or-change-a-tool-call) and [Follow a turn](/docs/en/plugins/mods/events#follow-a-turn).
* **Run your own code on a command**: a `/command` that runs your function at once, with no Claude turn, even while Claude is working. See [Add a command or a tool](/docs/en/plugins/mods/api#add-a-command-or-a-tool).
* **Share data between hooks**: a mod's hooks share the variables in its file, so what one hook records, another can show. For example, one hook can count tool calls while another shows the count beside the spinner, or one can read each request's token usage while another charts it in a pane. See [React to events](/docs/en/plugins/mods/events).

Mods work in the Claude Code CLI and in the Code tab of the Claude Desktop app. See [Where mods run](#where-mods-run) to understand how they behave elsewhere, such as in the VS Code extension, `claude -p`, and cloud sessions. If a settings hook, a skill, or an MCP server already does what you need, [compare them](#compare-mods-settings-hooks-skills-and-mcp-servers) before you write a mod. To manage mods for an organization, see [Manage mods for your organization](/docs/en/plugins/mods/admin).

## Get a mod

You can start with a mod in one of three ways:

* **Use one you already have**: some of Claude Code's own features are mods, such as `/diff`. See [Mods built into Claude Code](#mods-built-into-claude-code).
* **Make one**: describe what you want in a Claude Code session, and Claude writes the mod. See [Ask Claude for a mod](/docs/en/plugins/mods/create#ask-claude-for-a-mod). To learn how a mod's code works, [write one yourself](/docs/en/plugins/mods/create#write-a-mod-yourself).
* **Install one**: see [Install or update a mod](#install-or-update-a-mod)

### Install or update a mod

<Warning>
  A mod is code that runs with your permissions. It can read and write your files, start processes, and make network requests. Install mods only from authors and marketplaces you trust. See [Decide whether to trust a mod](#decide-whether-to-trust-a-mod).
</Warning>

A mod installs as a plugin, from a marketplace. Give the plugin's name, an `@`, and the marketplace's name. These examples install a plugin named `token-chart` from a marketplace named `your-org`:

* In a Claude Code session, run `/plugin install token-chart@your-org`.
* In your shell, run `claude plugin install token-chart@your-org`.

[Install plugins](/docs/en/plugins/install) covers marketplaces, scopes, the VS Code extension and the Desktop app, and [keeping plugins updated](/docs/en/plugins/install#keep-plugins-updated), all of which apply to a plugin that contains a mod without changes.

If you install or update a mod from your shell while a session is open, run `/reload-plugins` in that session to load it. Otherwise it loads the next time you start Claude Code.

## Decide whether to trust a mod

A mod is code that runs with your permissions, inside Claude Code. Install mods only from authors and [marketplaces you trust](/docs/en/plugins/security).

### What a mod can reach

A mod runs with your permissions, so before you install one, know what it has access to. Once it loads, a mod can:

* **Act on your machine as you**: read and write files anywhere your user account can, start programs, and make network requests
* **Read your secrets**: environment variables and settings files, including an API key you keep in either
* **See your session**: every prompt you send and every tool call Claude makes
* **Change your session**: rewrite a prompt or a tool call, submit a prompt as if you had typed it, or send a message to another of your sessions
* **Act without asking you**: approve a tool call before you're asked
* **Spend your usage**: call a model on your plan or API key

A mod that approves tool calls can approve one that an `ask` rule would prompt for, or that one of your own `PreToolUse` hooks blocked. [Extend permissions with hooks](/docs/en/permissions#extend-permissions-with-hooks) lists what such a mod can approve, including when it can approve a call that a `deny` rule refuses.

A mod can restyle much of Claude Code's interface, but not the permission prompt. It can't change what a prompt shows you.

### List what a mod does before you install one

Before you install a mod, you can list which events it hooks and what it asks Claude Code to do, such as read a file or make a network request, without running it. Get the plugin's files first, for example by cloning its repository. Then, in your shell, run `claude plugin validate` on the plugin's directory:

```bash theme={null}
claude plugin validate ./some-mod
```

The `hooks:` and `calls:` lines in the output list the events the mod handles and what it asks Claude Code to do. [Review what a mod can do](/docs/en/plugins/mods/admin#review-what-a-mod-can-do) shows the output and which calls to look for.

## Turn mods on or off

Mods require Claude Code v2.1.287 or later, and they're on by default. In your shell, run `claude --version` to check, and update Claude Code if yours is older.

To turn mods off, choose how many to stop, and for how long. To turn them back on, undo the same change:

* **One mod**: disable or uninstall its plugin from the [**Installed** tab in `/plugin`](/docs/en/plugins/install#manage-installed-plugins)
* **Every installed mod, for one session**: start Claude Code with [`--safe-mode`](/docs/en/cli-reference#cli-flags), which also leaves out your other customizations
* **Every mod you installed, in every session**: set [`"disableAllHooks": true`](/docs/en/settings-reference#disableallhooks) in `~/.claude/settings.json`. Your settings hooks and custom status line stop too. What your organization manages keeps running.

If you use Claude Code through an organization, an administrator can also limit which mods load. Administrators start at [Stop user-installed mods from loading](/docs/en/plugins/mods/admin#stop-user-installed-mods-from-loading).

To find out whether mods can load for you, see [Check whether mods can load](/docs/en/plugins/mods/troubleshoot#check-whether-mods-can-load).

<Note>
  If you set `CLAUDE_CODE_ENABLE_FUNCTION_HOOKS` during early access, remove it. Claude Code v2.1.287 and later ignores it, so setting it to `0` doesn't keep mods off.
</Note>

### See which mods a session loaded

To see which mods a terminal session loaded, run `/plugin` at the Claude Code prompt. A dim line under the tabs gives the count and the names, such as `1 mod active · first-mod`. If a mod you installed isn't named there, see [Find out why a mod does nothing](/docs/en/plugins/mods/troubleshoot#find-out-why-a-mod-does-nothing).

## How a mod works

A mod is a [plugin](/docs/en/plugins/overview) whose code registers event handlers, called hooks. Claude Code runs a hook when its event happens, such as when Claude calls a tool or when the spinner is drawn. A small mod has three files:

```text theme={null}
first-mod/
├── .claude-plugin/
│   └── plugin.json
└── hooks/
    ├── hooks.json
    └── register.js
```

* **`plugin.json`**: the plugin's [manifest](/docs/en/plugins/manifest-reference)
* **`hooks.json`**: [points to your code file](/docs/en/plugins/mods/reference#files)
* **`register.js`**: [your code](/docs/en/plugins/mods/create#write-a-mod-yourself), called the hooks module. It tells Claude Code which events to run your functions on.

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

* **The [`tool.call`](/docs/en/plugins/mods/reference#tools) hook** runs each time Claude is about to use a tool. It adds one to `calls`, asks Claude Code to draw the interface again, and lets the tool run as usual.
* **The [`ui.render`](/docs/en/plugins/mods/reference#interface) hook** runs each time Claude Code draws the spinner. It keeps Claude Code's own spinner and adds the count after the word.

This recording shows the mod at work. Watch the spinner line above the prompt box: while Claude lists a directory and reads two files, it reads `Thinking · tool calls: 1…`, then `2…`, then `3…`.

<Frame>
  <video autoPlay muted loop playsInline controls className="w-full dark:hidden" src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-overview-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=00a18aa0743b59a700f0275ce226e6d1" aria-label="In a Claude Code session, the prompt 'list the files here and read the README' is typed and sent. While Claude works, the spinner reads 'Thinking · tool calls: 1', then 2, then 3, as Claude lists the files and reads two of them." data-path="images/mods-overview-light.mp4" />

  <video autoPlay muted loop playsInline controls className="w-full hidden dark:block" src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-overview-dark.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=d5223da2fef16ceaaa214a36d72c0536" aria-label="In a Claude Code session, the prompt 'list the files here and read the README' is typed and sent. While Claude works, the spinner reads 'Thinking · tool calls: 1', then 2, then 3, as Claude lists the files and reads two of them." data-path="images/mods-overview-dark.mp4" />
</Frame>

### What a hook can do with an event

Claude Code runs your hook before it acts on the event, so the hook decides what happens next. It has three choices:

* **Observe**: note what's happening and let it continue unchanged, as the `tool.call` hook in the example does
* **Rewrite**: change the event before it continues, as the `ui.render` hook does when it adds the count to the spinner
* **Answer**: handle the event itself, so the usual behavior doesn't run, such as refusing a command

To do anything outside its own code, such as draw, add a command, call a model, read a file, start a process, or make a network request, a hook calls the mods API. A hook has no other way to do those things, which is why Claude Code can [list what a mod does](#list-what-a-mod-does-before-you-install-one) before you install it.

For the code behind each choice, see [React to events](/docs/en/plugins/mods/events#how-a-hook-handles-an-event). For what a hook can call, see [Use the mods API](/docs/en/plugins/mods/api).

### Where mods run

A mod's hooks run in every kind of session that loads the plugin. Drawing is narrower: only the terminal and the Desktop app show a mod's panes, bands, and replaced rows. This table lists each place you might run Claude Code:

| Where you run Claude Code | Hooks run | What the mod draws appears |
| :- | :- | :- |
| `claude` in a terminal, including an editor's integrated terminal and the JetBrains plugin | Yes | Yes |
| The Code tab of the Desktop app, except in a WSL session | Yes | Yes, except elements the [elements table](/docs/en/plugins/mods/reference#elements) marks terminal-only |
| A [WSL session](/docs/en/desktop-wsl) in the Desktop app | No, because plugins aren't available in WSL sessions | No |
| The VS Code extension's chat panel | Yes | No |
| `claude -p` and the [Agent SDK](/docs/en/agent-sdk/overview) | Yes | No |
| [Remote Control](/docs/en/remote-control) from claude.ai or the mobile app | Yes, in the session on your machine | In the terminal on your machine |
| A [cloud session](/docs/en/claude-code-on-the-web) | Yes, for a plugin that [reaches the cloud session](/docs/en/cloud-environments#what-carries-over-from-your-setup) | No |

A mod that draws can check which app it's running in, and fall back to a line in the transcript or a command's text reply where nothing draws.

## Control mods for your organization

Administrators decide whether mods run and which ones, through [managed settings](/docs/en/managed-settings). [Manage mods for your organization](/docs/en/plugins/mods/admin) covers what happens by default, how to review a mod, and how to enforce a policy with a mod of your own.

## Compare mods, settings hooks, skills, and MCP servers

Mods, settings hooks, skills, and MCP servers overlap. This table shows what each one is and when to pick it.

| | Mod | Settings hook | Skill | MCP server |
| :- | :- | :- | :- | :- |
| What it is | Functions in a plugin that Claude Code calls in its own process | A shell command, HTTP request, or prompt that Claude Code runs on a lifecycle event | A `SKILL.md` file of instructions Claude reads | An external process or service that gives Claude tools |
| What it can change | Tool calls, prompts, commands, turns, and what the interface draws | Whether a tool call or prompt goes ahead, a tool call's arguments and result, and context added for Claude | What Claude knows and does | Which tools Claude has |
| Can it draw in the interface | Yes | No | No | No |
| What you write | JavaScript or TypeScript | A script and a `settings.json` entry | Markdown | A server in any language |
| Pick it when | You want a pane, a band above the prompt, a custom command, or to rewrite an event | You want to block, allow, or log an event with a script you already have | You keep pasting the same instructions into chat | Claude needs to reach an external system |

Each of the others has its own page: [Hooks](/docs/en/hooks), [Skills](/docs/en/skills), and [MCP](/docs/en/mcp). A plugin can hold all four, so a mod can ship in the same plugin as a skill and an MCP server.

## Mods built into Claude Code

Some of Claude Code's own features are mods. To see the ones your session has, run `/plugin` at the Claude Code prompt and go to the **Installed** tab, which lists them under **Built-in**. You can't update or uninstall a built-in mod, and the table's last column says how to turn each one off. The [`mods active` line](#see-which-mods-a-session-loaded) leaves built-in mods out.

This table lists each entry by the name `/plugin` shows:

| Name in `/plugin` | What it does | Where it's on | How to turn it off |
| :- | :- | :- | :- |
| `cc-plugin-agents-md` | Loads `AGENTS.md` as project instructions | Every session, apart from [the ones that can't read `AGENTS.md`](/docs/en/memory#when-agents-md-support-is-unavailable) | Disable it in `/plugin`, or [choose which instruction files load](/docs/en/memory#choose-which-instruction-files-load) |
| `cc-plugin-diff` | Takes over [`/diff`](/docs/en/interactive-mode#review-changes-with-%2Fdiff) and draws its pane | Interactive terminal sessions | Disable it in `/plugin`. `/diff` stays, and Claude Code's built-in version of the command answers it. |
| `cc-plugin-plugin-authoring` | Gives Claude the [`plugin-authoring` skill](/docs/en/plugins/mods/create#ask-claude-for-a-mod) for writing mods. It holds a skill and no mod code. | Unless Anthropic has turned installed mods off remotely | Disable it in `/plugin` |
| `cc-plugin-sec-default` | Guards what your organization manages from the mods a user installs | [Where the guard loads](/docs/en/plugins/mods/admin#know-what-happens-by-default) | You can't. An administrator [sets the order](/docs/en/plugins/mods/admin#install-your-organizations-mods) in managed settings |
| `cc-plugin-telemetry` | Sends the analytics records that Claude Code and its built-in mods log | Wherever Claude Code's own analytics are on | Disable it in `/plugin`, or turn analytics off, for example with [`DISABLE_TELEMETRY`](/docs/en/env-vars) |
| `cc-plugin-you-should-know` | Runs a side agent that watches your back while Claude works on longer tasks. When it finds something worth knowing that you might miss, it shows you a note above the prompt. | Disabled by default. Listed in `/plugin` -> **Installed** -> **Show disabled** if available for your org. Enable with [`/plugin enable cc-plugin-you-should-know@builtin`](/docs/en/plugins/cli-reference#plugin-in-a-session). | Disable it in `/plugin` |

The settings and flags that stop installed mods, such as `disableAllHooks`, `--bare`, and `--safe-mode`, don't stop built-in mods.

### Read the source of built-in mods

The source of four of these mods is public in the [`mods` directory of the Claude Code repository](https://github.com/anthropics/claude-code/tree/main/mods). Each one is a complete plugin with its hooks module and tests:

* [`diff`](https://github.com/anthropics/claude-code/tree/main/mods/diff): the `/diff` pane, with buttons bound to keyboard actions and scrolling the mod handles itself
* [`agents-md`](https://github.com/anthropics/claude-code/tree/main/mods/agents-md): loads `AGENTS.md` as project instructions, with a [`userConfig`](/docs/en/plugins/components#user-configuration) option
* [`sec-default`](https://github.com/anthropics/claude-code/tree/main/mods/sec-default): the guard described in [Know what happens by default](/docs/en/plugins/mods/admin#know-what-happens-by-default), a model for a mod that enforces policy
* [`telemetry`](https://github.com/anthropics/claude-code/tree/main/mods/telemetry): adds methods that other mods can call, and ships their types

## Next steps

* [Create a mod](/docs/en/plugins/mods/create): build one that counts tool calls, shows the count beside the spinner, and adds a command, and learn the edit and reload loop
* [Draw in the interface](/docs/en/plugins/mods/interface): panes, the band above the prompt, buttons, text fields, and state
* [React to events](/docs/en/plugins/mods/events): tool calls, prompts, turns, and the order mods run in
* [Use the mods API](/docs/en/plugins/mods/api): commands, tools, model calls, timers, and files
* [Test a mod](/docs/en/plugins/mods/test): automated tests that run without a session
* [Troubleshoot a mod](/docs/en/plugins/mods/troubleshoot): the reasons a mod does nothing, and the debug log
* [Manage mods for your organization](/docs/en/plugins/mods/admin): defaults, managed settings, reviewing a mod, and policy mods
* [Mods reference](/docs/en/plugins/mods/reference): every event, method, element, and limit
