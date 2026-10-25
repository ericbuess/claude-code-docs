> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mods reference

> Complete reference for Claude Code mods: hooks module layout, events, mods API methods, render sites, elements by surface, limits, and settings.

Look up any event a [mod](https://code.claude.com/docs/en/plugins/mods/overview.md) can handle, mods API method it can call, or render site it can draw in. Entries cover the Claude Code CLI and the Desktop app as of v2.1.290, and the VS Code extension as of v2.1.299. Each entry gives the name and a one-line description, and links to the guide section that explains it where there is one.

> [!NOTE]
>
> The complete reference is Claude Code's [TypeScript declarations for mods](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts), which describe every event, method, and element, with examples. The copy on GitHub can be older than the Claude Code version you have installed. When the two disagree, trust [the copy Claude Code writes for your version](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build).

## Files

A mod is a plugin directory with these files:

| File | Required | Contents |
| :- | :- | :- |
| `.claude-plugin/plugin.json` | Yes | The plugin [manifest](https://code.claude.com/docs/en/plugins/manifest-reference.md). Mods add no required fields. |
| `hooks/hooks.json` | Yes | `modules`: an array with one path, relative to this file, to the hooks module, as in `"modules": ["./register.js"]`. Can also hold [settings hooks](https://code.claude.com/docs/en/hooks.md) under `hooks`. |
| The hooks module, such as [`hooks/register.js`](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself) | Yes | The mod's entry point. Exports `register(on, options)`. Named `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts`, or `.tsx`. An ES module. |
| [`types/index.d.ts`](https://code.claude.com/docs/en/plugins/mods/interface#declare-the-values), unless `types` in the manifest names another path | When the mod uses `$.state` or adds a namespace to the mods API | Declares `PluginState` values and any namespace the mod adds. To leave `types` out of the manifest, you need v2.1.299 or later. |
| Files whose names end in `.test.ts` or `.test.tsx` | No | Tests that [`claude plugin test`](https://code.claude.com/docs/en/plugins/mods/test#write-a-test) runs |

`register` receives `on` and `options`. `options` holds the values of the [`userConfig`](https://code.claude.com/docs/en/plugins/components#user-configuration) fields the manifest declares, with defaults filled in.

## The hook function

A mod registers each of its hooks, which are event handlers, by calling `on` inside `register`. `on` takes the event's name, an optional [matcher](https://code.claude.com/docs/en/plugins/mods/events.md#filter-which-events-a-hook-handles), which is a filter on the event's fields, and the hook, as in `on('tool.call', { tool: 'Bash' }, async ($, e, next) => next(e))`. `on` returns a registration with one method, `.catch(handler)`, which sets the hook's [error handler](https://code.claude.com/docs/en/plugins/mods/events.md#handle-a-hook-that-fails).

| Argument | What it is |
| :- | :- |
| [`$`](https://code.claude.com/docs/en/plugins/mods/events#how-a-hook-handles-an-event) | The mods API: every method in [mods API methods](#mods-api-methods). Write each call in full, namespace then method, as in `$.fs.read('notes.md')`. |
| [`e`](https://code.claude.com/docs/en/plugins/mods/events#how-a-hook-handles-an-event) | The event's input, as deeply frozen plain data. To change it, pass a copy to `next`. |
| [`next(e)`](https://code.claude.com/docs/en/plugins/mods/events#how-a-hook-handles-an-event) | The next handler, as in middleware. Runs the hooks after this one, then Claude Code's behavior. Resolves to the event's result. |
| [`next.signal`](https://code.claude.com/docs/en/plugins/mods/api#stop-background-work) | An `AbortSignal` that aborts when the event is abandoned |
| `next.origin` | `{ plugin, tier }` of whoever fired the event. Claude Code itself is `{ plugin: 'engine', tier: 'core' }`. A mod's `tier` is its priority group in the [order mods run in](https://code.claude.com/docs/en/plugins/mods/events.md#the-order-mods-run-in): `prepend`, `user`, `append`, or `builtin`. |
| `next.budget` | The hook's time limit in milliseconds: `next.budget.ms` is the whole limit, and `next.budget.remainingMs` is what's left now |
| `next.to(e, tier)` | Skips to a later tier, which is `append`, `builtin`, or `core`. `next.to(e, 'append')` skips the mods a user installed. Only a mod in `prependPlugins` or `appendPlugins` can call it. |
| `next.error` | In a `.catch` handler only. `kind` is `throw` or `timeout` when the hook failed, and `message` is the error's text. `kind` is `re-entry` when the hook was skipped because the event came from inside a mods API call by that hook or by your mod's code outside its hooks. `re-entry` requires Claude Code v2.1.292 or later. |
| `next.error.cause` | Set only when `kind` is `re-entry`. `rewritten` if a `tool.call` or [`PreToolUse`](https://code.claude.com/docs/en/hooks#pretooluse) hook changed the mods API call the event came from, or an `agent.spawn` hook changed an agent started by that call. `lent` when a method another mod adds to the mods API fired that event, unless `rewritten` also applies. `lent` requires Claude Code v2.1.292 or later and `rewritten` v2.1.300 or later. |
| `next.called` | In a `.catch` handler only. `true` when the hook had called `next`. |

## Events

Events are grouped by what they concern, each with when it fires and what a hook on it can return. Hooks on `turn.step` and `process.spawn` are async generators, and other hooks are async functions.

The last column of each table uses shorthand. `next(e)` passes the event on unchanged. `next({ ...e, text })` passes on a copy with the named field changed, as in `next({ ...e, text: e.text.trim() })`. An object answers the event without calling `next`, and a word such as `reason` stands for a string you write, as in `{ deny: 'Use the file tools.' }`.

### Tools

Tool events fire around each tool call Claude makes, from the description Claude reads to the decision on whether the call runs:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`tool.call`](https://code.claude.com/docs/en/plugins/mods/events#guard-or-change-a-tool-call) | A tool is about to run | `next(e)`, `{ deny: reason }`, or `{ result }` |
| [`tool.check`](https://code.claude.com/docs/en/plugins/mods/events#where-settings-hooks-run-in-the-order) | Claude Code decides whether a tool call may run, after the `tool.call` and `PreToolUse` hooks. `next(e)` resolves to the decision the rules, the permission mode, and those hooks reached. | `next(e)` or `{ decision }`, with `decision` set to `allow`, `ask`, or `deny` and an optional `reason` |
| `tool.describe` | Once for each tool, when its description is first sent to Claude. A second time for an MCP tool when Claude loads it through [tool search](https://code.claude.com/docs/en/mcp.md#scale-with-mcp-tool-search), with `e.description` set to the text Claude reads for the loaded tool. | `{ description }`, optionally with `isDeferred` set to `true` to put the tool behind tool search or `false` to load it upfront |

#### Agent and organization fields on `tool.check`

In a `tool.check` hook, read these fields to tell a subagent's call from the main conversation's, and to see whether your organization requires approval for a connector tool:

* **`e.agentId`**: set when a [subagent](https://code.claude.com/docs/en/sub-agents.md) or an [in-process teammate](https://code.claude.com/docs/en/agent-teams.md#choose-a-display-mode) makes the call, and absent when the main conversation does
* **`e.ceiling`**: `ask` for a connector tool your organization set to `ask`, in [sessions where that setting reaches Claude Code](https://code.claude.com/docs/en/mcp.md#organization-controls-on-connector-tools)

On `tool.check`, `e.agentId` and `e.ceiling` require Claude Code v2.1.290 or later.

#### The `e.isReadOnly` field on `tool.check`

In a `tool.check` hook, `e.isReadOnly` is `true` when the tool reports this call as read-only. Otherwise the field is absent, not `false`. The value is the tool's own report, so read [Check whether a tool call is read-only](https://code.claude.com/docs/en/plugins/mods/events.md#check-whether-a-tool-call-is-read-only) before you approve a call on this field alone.

On `tool.check`, `e.isReadOnly` requires Claude Code v2.1.304 or later.

### Prompts and what Claude reads

Prompt events cover the text the user types and the text Claude Code sends to Claude on its own, such as the system prompt and reminders:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`prompt.submit`](https://code.claude.com/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | A prompt is submitted | `next({ ...e, text })`, `next({ ...e, context })`, or `{ drop: reason }` |
| `prompt.fill`, `prompt.suggest` | Text is about to go into the prompt box as a draft, or as a dim suggestion | `next(e)` with changed text |
| `prompt.edit` | The user edits the prompt box | `next(e)` |
| `prompt.autocomplete` | The user types in the prompt box and a word ends at the cursor. `e.token` is that word. Claude Code doesn't wait for the hook: its own autocomplete rows show first. | `{ suggestions }`, a list of `{ text, label, description }` rows shown below Claude Code's own. Choosing a row writes its `text` over the word. |
| `prompt.compose` | Claude Code renders a system prompt | `{ sections }`, a list of `{ id, text, scope }` in the order they're sent |
| [`prompt.section`](https://code.claude.com/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | Once for each named section of the system prompt. `e.name` is the section's `id` in `prompt.compose`. | `{ text }`, or `{ text: null }` to omit the section |
| [`prompt.context`](https://code.claude.com/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | Once for each conversation, for the context sent with the first message | `{ blocks }` |
| `prompt.attachment` | Claude Code adds a message of its own for Claude, such as a reminder. `e.type` names the kind, and for the kinds the types declare, `e.detail` holds the facts the text was written from. | `{ text }`, or `{ text: null }` to omit it |
| `prompt.mention` | Claude Code is about to read a file that a prompt @-mentions. Requires Claude Code v2.1.290 or later. | `next({ ...e, path })` to read a different file, or `{ deny: reason }` |
| [`skill.prompt`](https://code.claude.com/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | A skill's text is expanded for Claude | `{ text }` |
| `attribution.text` | Claude Code composes commit or pull request attribution text | `{ text }` |

#### Source and frontmatter fields on `skill.prompt`

In a `skill.prompt` hook, you can read these fields along with the skill's name in `e.skill` and the text Claude reads in `e.text`:

| Field | Type | What it holds |
| :- | :- | :- |
| `e.source` | string | Who provides the skill: `policySettings`, `userSettings`, or `projectSettings` for a skill in the enterprise, personal, or project [location](https://code.claude.com/docs/en/skills.md#where-skills-live), respectively. Other sources give a word such as `plugin`, `mcp`, `syncedSkills`, or `built-in`. |
| `e.pluginName` | string | The plugin's name, for a skill whose `e.source` is `plugin` |
| `e.path` | string | The absolute path of the skill's `SKILL.md` file, or of its `.md` file for a skill written as a [command file](https://code.claude.com/docs/en/skills.md#where-skills-live). Absent when the skill has no file on this machine, as with a built-in skill. |
| `e.frontmatter` | object | The frontmatter of the skill's file, as plain data |
| `e.frontmatterProblem` | string | The reason `e.frontmatter` is missing the file's frontmatter or one of its keys, as in `is a list or a single value, not a table`. Absent when `e.frontmatter` holds the whole frontmatter or the skill has none. |

A hook can pass a changed `text` or `frontmatter` to `next`: the hooks after it read both, and Claude reads the final `text`. A hook that changes any other field [fails](https://code.claude.com/docs/en/plugins/mods/events.md#handle-a-hook-that-fails).

On `skill.prompt`, `e.source`, `e.pluginName`, `e.path`, `e.frontmatter`, and `e.frontmatterProblem` require Claude Code v2.1.299 or later.

### Commands and configuration

Command and configuration events fire when a command runs or is listed, when a `/config` row is shown or changed, and on a settings read:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`command.run`](https://code.claude.com/docs/en/plugins/mods/api#add-a-command) | A command is about to run | `{ text }`, `{}`, or `next(e)` |
| `command.describe` | Once for each command, for the command list | `{ description, argumentHint, isHidden }` |
| `config.set` | A `/config` row is about to change | `next({ ...e, value })` or `{ deny: reason }` |
| `config.describe` | Once for each `/config` row | `{ label, description, isHidden }` |
| [`settings.read`](https://code.claude.com/docs/en/plugins/mods/events#settings-read-hook) | A mod calls [`$.settings.read`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network), or Claude Code builds the session's merged settings | `next(e)`, `{ value }`, or `{ deny: reason }` |

#### `e.layers` and `e.source` on `settings.read`

* **`e.layers`**: one `{ source, settings }` object for each source in use that holds settings, lowest [precedence](https://code.claude.com/docs/en/settings.md#settings-precedence) first. See [What a `settings.read` hook receives](https://code.claude.com/docs/en/plugins/mods/events#settings-read-receives).
* **`e.source`**: the one source a mod asked for, as in `$.settings.read({ source: 'policy' })`. Absent on Claude Code's own read and on any other read of the merged settings

On `settings.read`, the event firing on Claude Code's own read and the `e.layers` field require Claude Code v2.1.304 or later. For when the hook runs and what the hook can return, with an example, see [Change or refuse a settings read](https://code.claude.com/docs/en/plugins/mods/events.md#settings-read-hook).

### Turns

Turn events follow one answer from start to finish, including each request to the model within it:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`turn.start`](https://code.claude.com/docs/en/plugins/mods/events#follow-a-turn) | A turn begins | `next(e)` |
| [`turn.step`](https://code.claude.com/docs/en/plugins/mods/events#follow-a-turn) | One request is about to go to the model | `yield* next(e)`, or `next({ ...e, model })`, `next({ ...e, effort })` |
| [`turn.complete`](https://code.claude.com/docs/en/plugins/mods/events#follow-a-turn) | A turn ended | `next(e)`, or `{ text }` to show a line under the answer |

### Session

Session events mark the session starting, ending, compacting, and exchanging messages with other sessions:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`session.start`](https://code.claude.com/docs/en/plugins/mods/api#add-a-command-or-a-tool) | Once for each loaded mod, before the first prompt, and again after a reload of that mod. Not after `/clear`, `/resume`, or `/branch`. | `next(e)` |
| `session.end` | The session ends, or `/clear`, `/resume`, or `/branch` runs. `e.reason` is `clear`, `resume`, `logout`, `prompt_input_exit`, or `other`. `/branch` reports `resume`. | `next(e)` |
| `session.compact` | The conversation is about to be compacted | `{ skip: reason }` |
| [`session.receive`](https://code.claude.com/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions), [`session.send`](https://code.claude.com/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions) | A message arrives from, or is about to go to, another agent or session. See [Send and receive messages between sessions](https://code.claude.com/docs/en/plugins/mods/api.md#send-and-receive-messages-between-sessions). | `{ consumed: reason }` for `receive`, `{ isDelivered: false, reason }` for `send` |
| `session.append` | Once for each row the conversation keeps, such as a prompt, a response block, a tool result, or a notice, before it's stored | `next({ ...e, message })` with a changed `message.content`, to rewrite the row's text blocks or the `content` of a `tool_result` block in it |
| `session.attach`, `session.detach` | Another app connects to or disconnects from the session | `next(e)` |
| `session.measure` | After each turn, and when a plan limit's percent used changes | `next(e)` |

### Subagents

Subagent events fire when a subagent type is offered to Claude and when a subagent or an agent-team teammate is about to start:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| `agent.offer` | A subagent type is offered to Claude | `{ isOffered: false }` to withhold it |
| `agent.spawn` | A subagent or an [agent team](https://code.claude.com/docs/en/agent-teams.md) teammate is about to start. For a teammate, `e.isTeammate` is `true`. | `next({ ...e, model })` to choose its model, or `{ deny: reason }` |

When Claude resumes a subagent with the [`SendMessage`](https://code.claude.com/docs/en/sub-agents#resume-subagents) tool, your `agent.spawn` hook doesn't run again. To refuse the `SendMessage` calls that resume a subagent, match that tool in a [`tool.call`](https://code.claude.com/docs/en/plugins/mods/events#guard-or-change-a-tool-call) hook.

### Interface

Interface events fire when Claude Code draws a render site and when the user uses a control a mod drew. [Draw in the interface](https://code.claude.com/docs/en/plugins/mods/interface.md) shows what a `ui.render` hook returns:

| Event | Fires when |
| :- | :- |
| [`ui.render`](https://code.claude.com/docs/en/plugins/mods/interface#pick-where-to-draw) | A [render site](#render-sites) is about to be drawn |
| `ui.resolve` | Mods load, once for each app, render site, and mod. The result is the element table that `$.ui.resolve(e)` reads. |
| [`ui.press`](https://code.claude.com/docs/en/plugins/mods/interface#respond-to-presses-and-typing), [`ui.input`](https://code.claude.com/docs/en/plugins/mods/interface#respond-to-presses-and-typing), [`ui.select`](https://code.claude.com/docs/en/plugins/mods/interface#respond-to-presses-and-typing) | A `Button`, `Input`, or `Select` a mod drew is used |
| `ui.focus`, `ui.scroll` | The focused control or the scroll position of a pane or the band is about to change |
| `ui.close` | A pane is about to close. `e.id` is the pane and `e.origin.kind` is `plugin`, `person`, or `unload`. |
| [`ui.message`](https://code.claude.com/docs/en/plugins/mods/interface#build-a-tree-from-elements) | A `Client` element posts data to its mod |
| [`ui.fault`](https://code.claude.com/docs/en/plugins/mods/interface#redraw-when-something-changes) | A `Client` element your mod drew failed to load, draw, or run. `e.phase` is `load`, `render`, or `run`, and `e.reason` is the error message. Requires Claude Code v2.1.289 or later. |

### Other mods

These events let a mod act on other mods as they load, to refuse one or change the mods API it receives:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`plugin.register`](https://code.claude.com/docs/en/plugins/mods/admin#enforce-a-policy-with-a-mod-of-your-own) | A hooks module is about to load. `e.uses` lists its events, mods API calls, environment variables, and state, as `claude plugin validate` prints them. Each call is written without the `$.` prefix, such as `fs.read`. | `{ refuse: reason }` |
| `engine.create` | The mods API is being built for this mod | A changed mods API, to add a namespace. A mod outside the `user` [tier](#the-hook-function) can also withhold one. |

When another mod's hook calls a method on a namespace you added in `engine.create`, your method's `$` calls run in that hook's context until every hook on that event returns. For example, a relative path resolves against that hook's working directory, and `$.prompt.submit` rejects while the turn is waiting on that hook. Calls your method makes after that run in your mod's own context.

### Telemetry

Telemetry events fire for the usage records Claude Code logs:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| `telemetry.log`, `telemetry.mark` | A telemetry record is about to be logged, or one use of a feature is marked. In a mod you install, give a telemetry hook the filter `{ to: 'collector' }`, as in `on('telemetry.log', { to: 'collector' }, hook)`. Without the filter, the mod fails `claude plugin validate`. `*` doesn't match these events. | `next(e)`, or `{ deny: reason }` |

### Settings hook events

Each [settings hook event](https://code.claude.com/docs/en/hooks.md#hook-events) is an event named `classic.<Event>`, such as `classic.Stop` or `classic.PostToolUse`. `e` is the hook's stdin JSON.

### Mods API calls

Every [mods API method](#mods-api-methods) is also an event, named for its namespace and method, such as `fs.read`, `model.complete`, or `ui.open`. A hook on one intercepts calls from the mods that run after it, and can return `next(e)`, `{ deny: reason }`, or `{ value }`.

## Mods API methods

The mods API is the `$` argument every hook receives. Its methods are grouped in namespaces, such as `$.ui`. This table lists each namespace's methods by name, so `open` in the `$.ui` row is the call `$.ui.open(...)`. The guides show the common ones in use, and [the types for your build](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build) document every method with an example.

| Namespace | Methods |
| :- | :- |
| `$.plugin` | `name`, `root`: this plugin's name and directory |
| [`$.ui`](https://code.claude.com/docs/en/plugins/mods/interface#pick-where-to-draw) | `resolve`, `invalidate`, `open`, `close`, `panes`, `focus`, `scroll`, `toast`, `notify`, `status`, `log`, `notice`, `ask`, `copy`, `selection`, `blit` |
| [`$.command`](https://code.claude.com/docs/en/plugins/mods/api#add-a-command) | `register`, `run`, `list` |
| [`$.tool`](https://code.claude.com/docs/en/plugins/mods/api#add-a-tool) | `register`, `call`, `check`, `list` |
| `$.agent` | `register`, `spawn`, `list`. `list()` returns this session's subagents and teammates, each with a `status` of `pending`, `running`, `waiting`, `idle`, `completed`, `failed`, or `killed`, where `idle` and `waiting` require Claude Code v2.1.289 or later. |
| [`$.model`](https://code.claude.com/docs/en/plugins/mods/api#call-a-model) | `complete`, `fork`, `classify` |
| [`$.prompt`](https://code.claude.com/docs/en/plugins/mods/api#start-a-turn-from-a-background-job) | `submit`, `read`, `fill`, `suggest`, `compose`. Claude reads text from `submit({ text })` after a sentence that names your mod as the sender. `submit({ text, asUser: true })` sends the text as the user's own words, without that sentence. |
| `$.turn` | `abort` |
| [`$.session`](https://code.claude.com/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions) | `messages`, `cwd`, `root`, `model`, `turns`, `id`, `repo`, `surfaces`, `usage`, `version`, `compact`, `send`, `append`, `authorize`. `usage()` returns `{ startedAt, context, rateLimits, cost }`: `context` has `tokens`, `window`, and `percent`, and `rateLimits` is a list of `{ kind, percentUsed, resetsAt }`. |
| `$.config` | `list`, `set` |
| [`$.settings`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `read` |
| [`$.env`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `get`, `set` |
| [`$.fs`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `read`, `write`, `list`, `exists`, `stat`, `ancestors`. `write` isn't atomic: it replaces the file's content in place, so another process can read a partly written file. Keep data that several sessions change in `$.store`. |
| [`$.store`](https://code.claude.com/docs/en/plugins/mods/interface#keep-state) | `get`, `set`, `delete`, `keys`. A key-value store that every session on the machine shares. See [Save from more than one session](https://code.claude.com/docs/en/plugins/mods/interface.md#save-from-more-than-one-session). |
| [`$.state`](https://code.claude.com/docs/en/plugins/mods/interface#keep-a-value-in-\$-state) | Reactive state: `get`, `set`, with the helpers `atom`, `read`, `update`, `derive`, and `memberOf` imported from `claude-code` |
| [`$.clock`](https://code.claude.com/docs/en/plugins/mods/api#run-work-in-the-background) | `now`, `sleep`, `after`, `every` |
| [`$.http`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `fetch` |
| [`$.process`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `run`, `spawn` |
| [`$.mcp`](https://code.claude.com/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `call`, `connect`. `connect(server)` connects an MCP server that your own plugin's manifest lists. |
| `$.audio` | `play`, `speak` |
| `$.telemetry` | `log`, `mark`. A record is sent only when Claude Code or a built-in mod makes the call. |

## Render sites

A render site is an extension point in Claude Code's interface. Each row is a value of `e.component` in a `ui.render` hook, with the fields of `e.props` and the apps that render it. `e.surface` names the app that's drawing, such as `terminal`, `desktop`, or `vscode`. [Change what Claude Code already draws](https://code.claude.com/docs/en/plugins/mods/interface.md#change-what-claude-code-already-draws) shows what a hook can do at a site, with an example of each choice.

Rendering in the VS Code extension requires extension version 2.1.299 or later. A session that [doesn't fetch feature flags](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching) needs 2.1.304 or later. [Draw in the VS Code extension](https://code.claude.com/docs/en/plugins/mods/interface.md#draw-in-the-vs-code-extension) lists what the extension draws differently.

| Site | `e.props` | `e.requestId` | Rendered on |
| :- | :- | :- | :- |
| [`Pane`](https://code.claude.com/docs/en/plugins/mods/interface#pick-where-to-draw) | `title`, `isFocused`, `bodyColumns`, `placement`, `scroll`, `view` | The pane's `id` | Terminal, Desktop, VS Code |
| [`AbovePrompt`](https://code.claude.com/docs/en/plugins/mods/interface#pick-where-to-draw) | `hasSurvey`, `isWorking`, `maxRows`, `bodyColumns`, `scroll`, `view` | One instance | Terminal, Desktop |
| `UserMessage` | `text`, `origin`, `isExpanded`, and `task` or `from` by origin | The message id | Terminal, Desktop, VS Code |
| `AssistantMessage` | The reply's text | The message id | Terminal, Desktop, VS Code |
| `ToolUse`, `ToolResult`, `ToolGroup` | The tool's name, input, and result | The tool call id | Terminal, Desktop, VS Code |
| `CommandOutput` | `command`, `text` | The message id | Terminal, Desktop |
| [`AskUserQuestion`](https://code.claude.com/docs/en/plugins/mods/interface#change-what-claude-code-already-draws) | The question and options | The tool call id | Terminal, Desktop, VS Code |
| `ToolProgress` | `kind` | The tool call id | Terminal |
| [`Spinner`](https://code.claude.com/docs/en/plugins/mods/interface#change-what-claude-code-already-draws) | `word`, `message`, `suffix`, `mode` | The agent id | Terminal, Desktop, VS Code |
| `TurnDuration` | `word`, `durationMs` | The message id | Terminal |
| `InfoNotice` | `text`, `command` | The message id | Terminal |
| `SessionMode` | `modes` | One instance | Terminal, Desktop |
| `PromptHint` | `isDraft`, `isWorking`, `hint` | One instance | Terminal, Desktop |

`e.viewport` holds `columns`, `rows`, and `isFullscreen`. In the terminal and the Desktop app, it's absent until the app has measured its window. There, its `rows` is the height of the whole window, not of your pane. In the VS Code extension, it's always present.

To fit a tree to its site, read these props in the hook:

* **Width of a `Pane` or the band**: draw to `e.props.bodyColumns`
* **Height of a `Pane` beside the transcript**: where `e.props.placement` is `'dock'`, `e.props.scroll.bodyRows` is the number of rows the pane has for your tree
* **Height of a `Pane` above the prompt**: where `e.props.placement` is `'inline'`, the pane grows with your tree up to a limit, and `bodyRows` is that limit. To ask for a different limit, see the [`rows` field of `$.ui.open`](https://code.claude.com/docs/en/plugins/mods/interface#open-a-pane-at-the-right-time).

A tree taller than the pane scrolls as a whole.

## Elements

Elements are the building blocks of a tree a `ui.render` hook returns, and you get them from `$.ui.resolve(e)`. [Build a tree from elements](https://code.claude.com/docs/en/plugins/mods/interface.md#build-a-tree-from-elements) shows the common ones with how the terminal draws them, and the [interface gallery](https://code.claude.com/docs/en/plugins/mods/gallery.md) has screenshots of most. A check mark means the app can draw the element.

| Element | Main props | Terminal | Desktop | VS Code |
| :- | :- | :-: | :-: | :-: |
| [`Box`](https://code.claude.com/docs/en/plugins/mods/interface#build-a-tree-from-elements) | `key`, flex layout, [`gap`, `padding`, `margin`](#box-spacing-steps), `width`, `height`, `minWidth`, `minHeight`, [`borderStyle`](#box-border-styles), `borderColor`, `borderDimColor`, `backgroundColor`, `position`, `top`, `left`, `right`, `bottom`, `overflow`, `display`, `hover` | ✓ | ✓ | ✓ |
| [`Text`](https://code.claude.com/docs/en/plugins/mods/interface#build-a-tree-from-elements) | `color`, `backgroundColor`, [`bold`](#text-bold), `italic`, `underline`, `strikethrough`, `dimColor`, `inverse`, `wrap`, [`size`, `weight`, `mono`, `tabular`](#text-typography), `hover` | ✓ | ✓ | ✓ |
| [`Button`](https://code.claude.com/docs/en/plugins/mods/interface#respond-to-presses-and-typing) | `key`, `label`, `onPress`, `hotkey`, `plain`, `dimColor`, `autoFocus`, `action`, `hover` | ✓ | ✓ | ✓ |
| [`Link`](https://code.claude.com/docs/en/plugins/mods/interface#link-in-the-desktop-app) | `href`, `label`. See [Limits](#limits). | ✓ | ✓ | ✓ |
| [`Code`](https://code.claude.com/docs/en/plugins/mods/gallery#show-code-and-changes) | `source`, `language`, `path`, `startLine`, `format`, `wrap` | ✓ | ✓ | ✓ |
| `Markdown` | `text`, `key`, `dimColor`, `onLinkPress`, `pressableLinks` | ✓ | ✓ | ✓ |
| [`Input`](https://code.claude.com/docs/en/plugins/mods/interface#take-typed-input-and-draw-a-row-for-each-item) | `key`, `label`, `placeholder`, `value`, `submitLabel`, `onSubmit`, `onInput`, `autoFocus` | ✓ | ✓ | ✓ |
| `Select` | `key`, `label`, `options`, `value`, `onSelect`, `autoFocus` | ✓ | ✓ | ✓ |
| `Svg` | a `source` of SVG markup up to 131,072 characters, `alt` text, `width`, `height`, and `isInteractive` | | ✓ | ✓ |
| [`Client`](https://code.claude.com/docs/en/plugins/mods/interface#build-a-tree-from-elements) | `module`, `key`, `props`, `width`, `height`, `flexGrow` | ✓ | ✓ | |
| [`Raster`](https://code.claude.com/docs/en/plugins/mods/interface#draw-a-grid-of-colored-cells) | `key`, `columns` up to 512, `rows` up to 256, `cells`. See [Draw a grid of colored cells](https://code.claude.com/docs/en/plugins/mods/interface.md#draw-a-grid-of-colored-cells). | ✓ | | |
| `Image` | `key`, a `source` such as PNG or RGBA bytes up to 2 MiB, or a file path, `columns` and `rows` up to 255, and `alt` text. See [which terminals draw it](https://code.claude.com/docs/en/plugins/mods/gallery.md#image-and-client). | ✓ | | |

More `Button` rules:

* **`action`**: names one of Claude Code's own [keybinding actions](https://code.claude.com/docs/en/keybindings.md), and the user's binding for it presses the button when that binding is a chord or a modified key
* **Digit hotkeys on the band**: a digit `hotkey` on a button in the band also fires when the user types that digit alone into an empty prompt and pauses
* **A collapsed band**: while the band is [collapsed](https://code.claude.com/docs/en/plugins/mods/interface.md#when-the-user-collapses-the-band), neither an `action` binding nor a hotkey presses a button in it
* **Two buttons on one hotkey**: when two buttons in one drawing name the same `hotkey`, the later one gets it

`autoFocus` accepts only `true` on any control, so omit the prop to leave it off.

The VS Code extension ignores some element props and draws the element as if you had left them out:

* **`Box`**: `position` with its `top`, `left`, `right`, and `bottom`, `alignSelf`, `borderDimColor`, and `hover`
* **`Text`**: `size`, `mono`, `tabular`, and `hover`
* **`Button`**: `hotkey`, `plain`, `autoFocus`, `action`, and `hover`, so the user presses a button there with a click, or with Enter once it has focus
* **`Code`**: `language`, `path`, `startLine`, `format`, and `wrap`, so code draws without colors or line numbers, and a `format: 'diff'` block shows the diff's raw text
* **`Input` and `Select`**: `autoFocus`
* **`Svg`**: `isInteractive`

### `Box` border styles

To draw a border around a `Box`, set its `borderStyle` to one of these names, as in `borderStyle: 'round'`. Each row says what the terminal draws for that name and shows the top edge of the border.

| `borderStyle` | What the terminal draws | Top edge |
| :- | :- | :- |
| `'single'` | Thin lines with square corners | `┌──┐` |
| `'double'` | Double lines | `╔══╗` |
| `'round'` | Thin lines with rounded corners | `╭──╮` |
| `'bold'` | Thick lines | `┏━━┓` |
| `'singleDouble'` | Thin lines on the top and bottom, double lines on the sides | `╓──╖` |
| `'doubleSingle'` | Double lines on the top and bottom, thin lines on the sides | `╒══╕` |
| `'classic'` | The ASCII characters `+`, `-`, and `\|` | `+--+` |
| `'arrow'` | Arrows that point into the `Box` | `↘↓↓↙` |
| `'dashed'` | Dashed lines with blank corners | `╌╌` |
| `'quote'` | A bar, `▎`, down the left side and blank cells on the other three sides | Blank |

A `Box` whose `borderStyle` names anything else, such as `'rounded'`, draws with no border.

### `Box` spacing steps

The `Box` spacing props are `gap`, `columnGap`, `rowGap`, `padding`, `margin`, and the one-side and one-axis forms of `padding` and `margin`, such as `paddingX` and `marginTop`. Each takes a number of terminal cells such as `gap: 1`, or a step name such as `gap: 'md'`. In the terminal and the VS Code extension, each step is this many cells:

| Step | Cells across | Cells down |
| :- | :- | :- |
| `'xs'` | 1 | 0 |
| `'sm'` | 1 | 0 |
| `'md'` | 2 | 1 |
| `'lg'` | 3 | 1 |
| `'xl'` | 4 | 2 |

If you set `gap`, `padding`, or `margin` to a step, the step applies across and down at once. For example, in the terminal and the VS Code extension, `padding: 'md'` is two cells at each side and one row above and below.

Step names require Claude Code v2.1.299 or later. On an earlier release, Claude Code [draws its own version of the site](https://code.claude.com/docs/en/plugins/mods/interface.md#build-a-tree-from-elements) in place of a tree that uses a step name.

### `Text` typography props

Set `size`, `weight`, `mono`, or `tabular` on a `Text` to ask the app drawing your tree for a text size, a weight, a monospaced typeface, or equal-width digits. Before you rely on a prop, check what the terminal and the VS Code extension do with it. If an app ignores a prop you set, your tree still draws there, with the text as if you'd left that prop out.

| Prop | Values | In the terminal | In the VS Code extension |
| :- | :- | :- | :- |
| `size` | `'caption'`, `'footnote'`, `'body'`, `'heading'`, or `'title'` | Ignored: the terminal has one text size | Ignored |
| `weight` | `'regular'`, `'medium'`, `'semibold'`, or `'bold'` | `semibold` and `bold` draw as bold text | `semibold` and `bold` draw as bold text |
| `mono` | `true` to ask for the app's monospaced typeface | Ignored: the terminal is always monospaced | Ignored, so text keeps the extension's own typeface |
| `tabular` | `true` to ask for digits of equal width, so that a number that updates in place or a column of numbers stays aligned | Ignored: the terminal's digits are already one cell wide | Ignored |

These four props require Claude Code v2.1.299 or later. On an earlier release, Claude Code [draws its own version of the site](https://code.claude.com/docs/en/plugins/mods/interface.md#build-a-tree-from-elements) in place of a tree that sets `size`, `weight`, `mono`, or `tabular`.

#### Replace `bold` with `weight`

`bold` on a `Text` is deprecated in favor of `weight` and still works. To replace it on a `Text` with no `weight`, change `bold: true` to `weight: 'semibold'` for the same result on Claude Code v2.1.299 or later.

On a release earlier than v2.1.299, a tree that sets `weight` doesn't draw, and Claude Code [draws its own version of the site](https://code.claude.com/docs/en/plugins/mods/interface.md#build-a-tree-from-elements) instead. If you set both `bold` and `weight` on a `Text`, `bold` has no effect.

## Limits

Hooks and mods API calls run under time and size limits. Claude Code skips a hook that exceeds a time limit.

| Limit | Value |
| :- | :- |
| A hook's own execution time for one event, not counting time inside `next` or a mods API call other than `$.clock.sleep` | 10 seconds, or 50 milliseconds for a `prompt.edit` hook |
| A `.catch` handler's execution time | 1 second |
| All `session.end` hooks together | As long as the [SessionEnd hook budget](https://code.claude.com/docs/en/hooks.md#sessionend-input), 1.5 seconds unless you change it, counted from when your settings `SessionEnd` hooks finish |
| `$.process.run` timeout | 30 seconds by default, 10 minutes at most |
| `$.model.complete` `maxTokens` | 1024 by default, up to 64,000 or the model's output limit |
| `$.fs.read` and `$.fs.write` | 4 MiB for one file |
| A `$.http.fetch` request body | 4 MiB, counted in characters. A call with a larger body rejects. |
| A `$.http.fetch` response body | 4 MiB. `text` holds the first 4 MiB and the rest isn't read. When the `Content-Length` header declares more, the call rejects instead, with a reason that ends `is over the 4194304-byte limit`, except when the last request after any redirects uses the `HEAD` method. The `HEAD` exemption requires Claude Code v2.1.296 or later. |
| One `$.http.fetch` call, redirects and body included | 30 seconds |
| Redirects one `$.http.fetch` call follows | 5 |
| A hook's `drop` reason or `config.set` `deny` reason | 4,096 characters. The end of a longer reason is cut, and the drop or deny still applies. The cut requires Claude Code v2.1.292 or later, and on earlier versions the hook [fails](https://code.claude.com/docs/en/plugins/mods/events.md#handle-a-hook-that-fails) instead. |
| Text in one tree | The first 100,000 characters are drawn |
| A `Code`'s `language` or `path`, a `Select` option's `value`, or a `Client`'s `module` | 10,000 characters. If one is longer, Claude Code [draws its own version of the site](https://code.claude.com/docs/en/plugins/mods/interface.md#build-a-tree-from-elements). |
| A `Link`'s `href` | 2,048 characters. A longer `href` keeps the whole tree from drawing. |
| `$.store` | 4 MiB of JSON in total |
| `$.session.messages()` | The newest 4,096 entries |
| `$.ui.invalidate('ui.render')` redraws | Throttled to 10 a second, or 30 in the terminal for the visible pane, the expanded band, and the hint line under the prompt. Calls that come sooner are coalesced. |
| `$.ui.toast` | Shown for 4 seconds unless you pass `{ timeoutMs }` |
| A pane opened without the user asking | Placed from 144 terminal columns, 110 after they've opened it once |
| Scopes, such as functions, blocks, and loops, nested inside one another in one file of a hooks module | 2,000 |
| Command, tool, subagent type, and pane names | Letters, digits, `_`, and `-`, up to 64 characters |
| One `claude plugin test` test | 5 seconds unless the test sets `timeoutMs` |

## Settings and environment variables

These are the settings and environment variables that affect mods. The Where column says which settings file or environment each one is read from:

| Name | Where | What it does |
| :- | :- | :- |
| `CLAUDE_CODE_PLUGIN_DIRS` | Environment, or `env` in `~/.claude/settings.json` | Plugin directories to load as `--plugin-dir` does, for apps you can't pass a flag to. Absolute paths separated by `:`, or `;` on Windows. |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH` | Environment | `1` makes a long-running non-interactive session reload `--plugin-dir` mods on save |
| `prependPlugins`, `appendPlugins` | Managed settings. User settings only on a machine with no managed settings, in a session whose credential isn't a Team or Enterprise `/login`. | Lists of plugin ids, such as `acme-guard@acme-tools`. Mods in `prependPlugins` run before every mod a user installs, and mods in `appendPlugins` run after, in the listed order. See [The order mods run in](https://code.claude.com/docs/en/plugins/mods/events.md#the-order-mods-run-in). |
| `allowManagedModsOnly` | Managed settings, as an [option on the built-in guard](https://code.claude.com/docs/en/plugins/mods/admin.md#set-options-on-the-built-in-guard) | Only mods that [count as your organization's](https://code.claude.com/docs/en/plugins/mods/admin.md#install-your-organizations-mods), and mods built into Claude Code, run their hooks. Users' settings hooks keep running. |
| `allowModsToOverrideDenyRules` | Managed settings, as an [option on the built-in guard](https://code.claude.com/docs/en/plugins/mods/admin.md#set-options-on-the-built-in-guard) | Lets a mod a user installed approve a tool call that a `deny` rule refuses |
| `allowManagedHooksOnly` | Managed settings | Blocks hooks and installed mods that aren't your organization's. See [what keeps running](https://code.claude.com/docs/en/settings-reference.md#what-runs-under-allowmanagedhooksonly). |
| `disableAllHooks` | Any settings file | In managed settings, no mod or hook from an installed plugin runs. In your own settings, what your organization manages keeps running. See [`disableAllHooks`](https://code.claude.com/docs/en/settings-reference#disableallhooks). |
| `disableSideloadFlags` | Managed settings | Rejects `--plugin-dir` and `--plugin-url` at startup |
| `pluginConfigs` | User or managed settings | Holds `userConfig` values for a mod, keyed by the plugin's id, such as `acme-guard@acme-tools`, or its name and `@inline`, such as `first-mod@inline`, for one loaded with `--plugin-dir` |

`sec-default@builtin` is a guard built into Claude Code, listed as `cc-plugin-sec-default` in `/plugin` and the debug log. It loads ahead of every mod a person installs on a machine with managed settings, or in a session whose credential is a Team or Enterprise [`/login`](https://code.claude.com/docs/en/authentication#authentication-precedence). If managed `prependPlugins` is set, the guard loads only when that list names it, at the position listed.

Its source is in the [`mods/sec-default` directory of the Claude Code repository](https://github.com/anthropics/claude-code/tree/main/mods/sec-default).

## Commands

These commands and flags load, inspect, and test a mod. The `claude` commands run in your shell and the `/` commands at the Claude Code prompt. In the table, `<directory>` stands for a path you type, as in `claude plugin validate ./first-mod`. Square brackets mark an optional argument.

| Command | What it does |
| :- | :- |
| [`/plugin`](https://code.claude.com/docs/en/plugins/mods/overview#see-which-mods-a-session-loaded) | Shows a line such as `1 mod active · first-mod` under its tabs when a mod that isn't built in has loaded |
| [`claude plugin validate <directory>`](https://code.claude.com/docs/en/plugins/mods/create#check-what-claude-code-reads-from-your-mod) | Reads a plugin's manifest and hooks module and reports errors, the events it handles, and the mods API calls it makes. `--strict` treats warnings as errors and `--json` prints a machine-readable report. |
| [`claude plugin test [directory]`](https://code.claude.com/docs/en/plugins/mods/test#write-a-test) | Runs every file under the directory, or the current directory when you give none, whose name ends in `.test.ts` or `.test.tsx`. Exits with status 1 when a test fails. |
| [`claude --plugin-dir <directory>`](https://code.claude.com/docs/en/plugins/mods/create#write-a-mod-yourself) | Loads a plugin directory for one session and reloads its hooks module when you save. Repeat the flag to load several. |
| `/reload-plugins` | Reloads plugins when you run it |
