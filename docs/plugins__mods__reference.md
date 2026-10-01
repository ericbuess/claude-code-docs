> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mods reference

> Complete reference for Claude Code mods: hooks module layout, every event, every mods API method, render sites, elements by surface, limits, and settings.

Look up any event a [mod](/docs/en/plugins/mods/overview) can hook, mods API method it can call, or render site it can draw in, for the Claude Code CLI and the Desktop app as of v2.1.287. Each entry gives the name and a one-line description, and links to the guide section that explains it where there is one.

<Note>
  The complete reference is Claude Code's [TypeScript declarations for mods](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts), which describe every event, method, and element, with examples. The copy on GitHub can be older than the Claude Code version you have installed. When the two disagree, trust [the copy Claude Code writes for your version](/docs/en/plugins/mods/create#get-the-types-for-your-build).
</Note>

## Files

A mod is a plugin directory with these files:

| File | Required | Contents |
| :- | :- | :- |
| `.claude-plugin/plugin.json` | Yes | The plugin [manifest](/docs/en/plugins/manifest-reference). Mods add no required fields. |
| `hooks/hooks.json` | Yes | `modules`: an array with one path, relative to this file, to the hooks module, as in `"modules": ["./register.js"]`. Can also hold [settings hooks](/docs/en/hooks) under `hooks`. |
| The hooks module, such as [`hooks/register.js`](/docs/en/plugins/mods/create#write-a-mod-yourself) | Yes | The mod's entry point. Exports `register(on, options)`. Named `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts`, or `.tsx`. An ES module. |
| [`types/index.d.ts`](/docs/en/plugins/mods/interface#declare-the-values), named by `types` in the manifest | When the mod uses `$.state` or adds a namespace to the mods API | Declares `PluginState` values and any namespace the mod adds |
| Files whose names end in `.test.ts` or `.test.tsx` | No | Tests that [`claude plugin test`](/docs/en/plugins/mods/test#write-a-test) runs |

`register` receives `on` and `options`. `options` holds the values of the [`userConfig`](/docs/en/plugins/components#user-configuration) fields the manifest declares, with defaults filled in.

## The hook function

A mod registers each of its hooks, which are event handlers, by calling `on` inside `register`. `on` takes the event's name, an optional [matcher](/docs/en/plugins/mods/events#filter-which-events-a-hook-handles), which is a filter on the event's fields, and the hook, as in `on('tool.call', { tool: 'Bash' }, async ($, e, next) => next(e))`. `on` returns a registration with one method, `.catch(handler)`, which sets the hook's [error handler](/docs/en/plugins/mods/events#handle-a-hook-that-fails).

| Argument | What it is |
| :- | :- |
| [`$`](/docs/en/plugins/mods/events#how-a-hook-handles-an-event) | The mods API: every method in [mods API methods](#mods-api-methods). Write each call in full, namespace then method, as in `$.fs.read('notes.md')`. |
| [`e`](/docs/en/plugins/mods/events#how-a-hook-handles-an-event) | The event's input, as deeply frozen plain data. To change it, pass a copy to `next`. |
| [`next(e)`](/docs/en/plugins/mods/events#how-a-hook-handles-an-event) | The next handler, as in middleware. Runs the hooks after this one, then Claude Code's behavior. Resolves to the event's result. |
| [`next.signal`](/docs/en/plugins/mods/api#stop-background-work) | An `AbortSignal` that fires when the event is abandoned |
| `next.origin` | `{ plugin, tier }` of whoever raised the event. Claude Code itself is `{ plugin: 'engine', tier: 'core' }`. A mod's `tier` is its priority group in the [order mods run in](/docs/en/plugins/mods/events#the-order-mods-run-in): `prepend`, `user`, `append`, or `builtin`. |
| `next.budget` | The hook's time limit in milliseconds: `next.budget.ms` is the whole limit, and `next.budget.remainingMs` is what's left now |
| `next.to(e, tier)` | Skips to a later tier, which is `append`, `builtin`, or `core`. `next.to(e, 'append')` skips the mods a user installed. Only a mod in `prependPlugins` or `appendPlugins` can call it. |
| `next.error`, `next.called` | In a `.catch` handler only. `next.error.kind` is `throw` or `timeout`, `next.error.message` is the error's text, and `next.called` is `true` when the failed hook had called `next`. |

## Events

Every event a mod can hook is listed here, grouped by what it concerns, with when it fires and what a hook on it can return. Hooks on `turn.step` and `process.spawn` are async generators, and every other hook is an async function.

The last column of each table uses shorthand. `next(e)` passes the event on unchanged. `next({ ...e, text })` passes on a copy with the named field changed, as in `next({ ...e, text: e.text.trim() })`. An object answers the event without calling `next`, and a word such as `reason` stands for a string you write, as in `{ deny: 'Use the file tools.' }`.

### Tools

Tool events fire around each tool call Claude makes, from the description Claude reads to the decision on whether the call runs:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`tool.call`](/docs/en/plugins/mods/events#guard-or-change-a-tool-call) | A tool is about to run | `next(e)`, `{ deny: reason }`, or `{ result }` |
| [`tool.check`](/docs/en/plugins/mods/events#where-settings-hooks-run-in-the-order) | Claude Code decides whether a tool call may run, after the `tool.call` and `PreToolUse` hooks. `next(e)` resolves to the decision the rules, the permission mode, and those hooks reached. | `{ decision }`, which is `allow`, `ask`, or `deny` |
| `tool.describe` | Once for each tool, when its description is first sent to Claude | `{ description }` |

### Prompts and what Claude reads

Prompt events cover the text the user types and the text Claude Code sends to Claude on its own, such as the system prompt and reminders:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`prompt.submit`](/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | A prompt is submitted | `next({ ...e, text })`, `next({ ...e, context })`, or `{ drop: reason }` |
| `prompt.fill`, `prompt.suggest` | Text is about to go into the prompt box as a draft, or as a dim suggestion | `next(e)` with changed text |
| `prompt.edit` | The user edits the prompt box | `next(e)` |
| `prompt.compose` | Claude Code renders a system prompt | `{ sections }`, a list of `{ id, text, scope }` in the order they're sent |
| [`prompt.section`](/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | Once for each named section of the system prompt. `e.name` is the section's `id` in `prompt.compose`. | `{ text }`, or `{ text: null }` to leave the section out |
| [`prompt.context`](/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | Once for each conversation, for the context sent with the first message | `{ blocks }` |
| `prompt.attachment` | Claude Code adds a message of its own for Claude, such as a reminder. `e.type` names the kind, and for the kinds the types declare, `e.detail` holds the facts the text was written from. | `{ text }`, or `{ text: null }` to leave it out |
| [`skill.prompt`](/docs/en/plugins/mods/events#rewrite-or-add-to-a-prompt) | A skill's text is expanded for Claude | `{ text }` |
| `attribution.text` | Claude Code composes commit or pull request attribution text | `{ text }` |

### Commands and configuration

Command and configuration events fire when a command runs or is listed, and when a `/config` row is shown or changed:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`command.run`](/docs/en/plugins/mods/api#add-a-command) | A command is about to run | `{ text }`, `{}`, or `next(e)` |
| `command.describe` | Once for each command, for the command list | `{ description, argumentHint, isHidden }` |
| `config.set` | A `/config` row is about to change | `next({ ...e, value })` or `{ deny: reason }` |
| `config.describe` | Once for each `/config` row | `{ label, description, isHidden }` |

### Turns

Turn events follow one answer from start to finish, including each request to the model within it:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`turn.start`](/docs/en/plugins/mods/events#follow-a-turn) | A turn begins | `next(e)` |
| [`turn.step`](/docs/en/plugins/mods/events#follow-a-turn) | One request is about to go to the model | `yield* next(e)`, or `next({ ...e, model })`, `next({ ...e, effort })` |
| [`turn.complete`](/docs/en/plugins/mods/events#follow-a-turn) | A turn ended | `next(e)`, or `{ text }` to show a line under the answer |

<h3 id="session">
  Session
</h3>

Session events mark the session starting, ending, compacting, and exchanging messages with other sessions:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`session.start`](/docs/en/plugins/mods/api#add-a-command-or-a-tool) | Once for each loaded mod, before the first prompt, and again after a reload of that mod. Not after `/clear`, `/resume`, or `/branch`. | `next(e)` |
| `session.end` | The session ends, or `/clear`, `/resume`, or `/branch` runs. `e.reason` is `clear`, `resume`, `logout`, `prompt_input_exit`, or `other`. `/branch` reports `resume`. | `next(e)` |
| `session.compact` | The conversation is about to be compacted | `{ skip: reason }` |
| [`session.receive`](/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions), [`session.send`](/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions) | A message arrives from, or is about to go to, another agent or session. See [Send and receive messages between sessions](/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions). | `{ consumed: reason }` for `receive`, `{ isDelivered: false, reason }` for `send` |
| `session.append` | Once for each row the conversation keeps, such as a prompt, a response block, a tool result, or a notice, before it's stored | `next({ ...e, message })` to rewrite the row's `content` |
| `session.attach`, `session.detach` | Another app connects to or disconnects from the session | `next(e)` |
| `session.measure` | After each turn, and when a plan limit's percent used changes | `next(e)` |

### Subagents

Subagent events fire when a subagent type is offered to Claude and when one is about to start:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| `agent.offer` | A subagent type is offered to Claude | `{ isOffered: false }` to withhold it |
| `agent.spawn` | A subagent is about to start | `{ model }` or `{ deny: reason }` |

### Interface

Interface events fire when Claude Code draws a render site and when the user uses a control a mod drew. [Draw in the interface](/docs/en/plugins/mods/interface) shows what a `ui.render` hook returns:

| Event | Fires when |
| :- | :- |
| [`ui.render`](/docs/en/plugins/mods/interface#pick-where-to-draw) | A [render site](#render-sites) is about to be drawn |
| `ui.resolve` | Mods load, once for each app, render site, and mod. The result is the element table that `$.ui.resolve(e)` reads. |
| [`ui.press`](/docs/en/plugins/mods/interface#respond-to-presses-and-typing), [`ui.input`](/docs/en/plugins/mods/interface#respond-to-presses-and-typing), [`ui.select`](/docs/en/plugins/mods/interface#respond-to-presses-and-typing) | A `Button`, `Input`, or `Select` a mod drew is used |
| `ui.focus`, `ui.scroll` | The focused control or the scroll position of a pane or the band is about to change |
| `ui.close` | A pane is about to close. `e.id` is the pane and `e.origin.kind` is `plugin`, `person`, or `unload`. |
| [`ui.message`](/docs/en/plugins/mods/interface#build-a-tree-from-elements) | A `Client` element posts data to its mod |

### Other mods

Two events let a mod act on other mods as they load, to refuse one or change the mods API it receives:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| [`plugin.register`](/docs/en/plugins/mods/admin#enforce-a-policy-with-a-mod-of-your-own) | A hooks module is about to load. `e.uses` lists its events, mods API calls, environment variables, and state, as `claude plugin validate` prints them. Each call is spelled without the `$.` prefix, such as `fs.read`. | `{ refuse: reason }` |
| `engine.create` | The mods API is being built for this mod | A changed mods API, to add a namespace or withhold one |

### Telemetry

Telemetry events fire for the usage records Claude Code logs:

| Event | Fires when | A hook can return |
| :- | :- | :- |
| `telemetry.log`, `telemetry.mark` | A telemetry record is about to be logged, or one use of a feature is marked. Hook them by name or as `telemetry.*`, because `*` in a mod you install doesn't select them. | `next(e)`, or `{ deny: reason }` |

### Settings hook events

Each [settings hook event](/docs/en/hooks#hook-events) is an event named `classic.<Event>`, such as `classic.Stop` or `classic.PostToolUse`. `e` is the hook's stdin JSON.

### Mods API calls

Every [mods API method](#mods-api-methods) is also an event, named for its namespace and method, such as `fs.read`, `model.complete`, or `ui.open`. A hook on one intercepts calls from the mods that run after it, and can return `next(e)`, `{ deny: reason }`, or `{ value }`.

## Mods API methods

The mods API is the `$` argument every hook receives. Its methods are grouped in namespaces, such as `$.ui`. This table lists each namespace's methods by name, so `open` in the `$.ui` row is the call `$.ui.open(...)`. The guides show the common ones in use, and [the types for your build](/docs/en/plugins/mods/create#get-the-types-for-your-build) document every method with an example.

| Namespace | Methods |
| :- | :- |
| `$.plugin` | `name`, `root`: this plugin's name and directory |
| [`$.ui`](/docs/en/plugins/mods/interface#pick-where-to-draw) | `resolve`, `invalidate`, `open`, `close`, `panes`, `focus`, `scroll`, `toast`, `status`, `log`, `notice`, `ask`, `copy`, `blit` |
| [`$.command`](/docs/en/plugins/mods/api#add-a-command) | `register`, `run`, `list` |
| [`$.tool`](/docs/en/plugins/mods/api#add-a-tool) | `register`, `call`, `check`, `list` |
| `$.agent` | `register`, `spawn`, `list` |
| [`$.model`](/docs/en/plugins/mods/api#call-a-model) | `complete`, `fork`, `classify` |
| [`$.prompt`](/docs/en/plugins/mods/api#start-a-turn-from-a-background-job) | `submit`, `read`, `fill`, `suggest`, `compose`. Claude reads text from `submit({ text })` after a sentence that names your mod as the sender. `submit({ text, asUser: true })` sends the text as the user's own words, without that sentence. |
| `$.turn` | `abort` |
| [`$.session`](/docs/en/plugins/mods/api#send-and-receive-messages-between-sessions) | `messages`, `cwd`, `root`, `model`, `turns`, `id`, `repo`, `surfaces`, `usage`, `version`, `compact`, `send`, `append`, `authorize`. `usage()` returns `{ startedAt, context, rateLimits, cost }`: `context` has `tokens`, `window`, and `percent`, and `rateLimits` is a list of `{ kind, percentUsed, resetsAt }`. |
| `$.config` | `list`, `set` |
| [`$.settings`](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `read` |
| [`$.env`](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `get`, `set` |
| [`$.fs`](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `read`, `write`, `list`, `exists`, `stat`, `ancestors`. `write` isn't atomic: it replaces the file's content in place, so another process can read a partly written file. Keep data that several sessions change in `$.store`. |
| [`$.store`](/docs/en/plugins/mods/interface#keep-state) | `get`, `set`, `delete`, `keys`. A key-value store that every session on the machine shares. See [Save from more than one session](/docs/en/plugins/mods/interface#save-from-more-than-one-session). |
| [`$.state`](/docs/en/plugins/mods/interface#keep-a-value-in-\$-state) | Reactive state: `get`, `set`, with the helpers `atom`, `read`, `update`, `derive`, and `memberOf` imported from `claude-code` |
| [`$.clock`](/docs/en/plugins/mods/api#run-work-in-the-background) | `now`, `sleep`, `after`, `every` |
| [`$.http`](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `fetch` |
| [`$.process`](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `run`, `spawn` |
| [`$.mcp`](/docs/en/plugins/mods/api#reach-files-processes-and-the-network) | `call`, `connect`. `connect(server)` connects an MCP server that your own plugin's manifest lists. |
| `$.audio` | `play`, `speak` |
| `$.telemetry` | `log`, `mark`. A record is sent only when Claude Code or a built-in mod raised it. |

## Render sites

A render site is an extension point in Claude Code's interface. Each row is a value of `e.component` in a `ui.render` hook, with the fields of `e.props` and the apps that raise it. `e.surface` is `terminal` or `desktop`. [Change what Claude Code already draws](/docs/en/plugins/mods/interface#change-what-claude-code-already-draws) shows what a hook can do at a site, with an example of each choice.

| Site | `e.props` | `e.requestId` | Raised on |
| :- | :- | :- | :- |
| [`Pane`](/docs/en/plugins/mods/interface#pick-where-to-draw) | `title`, `isFocused`, `bodyColumns`, `placement`, `scroll`, `view` | The pane's `id` | Terminal, Desktop |
| [`AbovePrompt`](/docs/en/plugins/mods/interface#pick-where-to-draw) | `hasSurvey`, `isWorking`, `maxRows`, `bodyColumns`, `scroll`, `view` | One instance | Terminal, Desktop |
| `UserMessage` | `text`, `origin`, `isExpanded`, and `task` or `from` by origin | The message id | Terminal, Desktop |
| `AssistantMessage` | The reply's text | The message id | Terminal, Desktop |
| `ToolUse`, `ToolResult`, `ToolGroup` | The tool's name, input, and result | The tool call id | Terminal, Desktop |
| `CommandOutput` | `command`, `text` | The message id | Terminal, Desktop |
| [`AskUserQuestion`](/docs/en/plugins/mods/interface#change-what-claude-code-already-draws) | The question and options | The tool call id | Terminal, Desktop |
| `ToolProgress` | `kind` | The tool call id | Terminal |
| [`Spinner`](/docs/en/plugins/mods/interface#change-what-claude-code-already-draws) | `word`, `message`, `suffix`, `mode` | The agent id | Terminal, Desktop |
| `TurnDuration` | `word`, `durationMs` | The message id | Terminal |
| `InfoNotice` | `text`, `command` | The message id | Terminal |
| `SessionMode` | `modes` | One instance | Terminal, Desktop |
| `PromptHint` | `isDraft`, `isWorking`, `hint` | One instance | Terminal, Desktop |

`e.viewport` holds `columns`, `rows`, and `isFullscreen`. It's absent until the app has measured its window. Its `rows` is the height of the whole window, not of your pane.

To fit a tree to its site, read these props in the hook:

* **Width of a `Pane` or the band**: draw to `e.props.bodyColumns`
* **Height of a `Pane` beside the transcript**: where `e.props.placement` is `'dock'`, `e.props.scroll.bodyRows` is the number of rows the pane has
* **Height of a `Pane` above the prompt**: where `e.props.placement` is `'inline'`, the pane grows with your tree up to a limit, and `bodyRows` counts only the rows showing now. The [`rows` field of `$.ui.open`](/docs/en/plugins/mods/interface#open-a-pane-at-the-right-time) asks for a different limit.

A tree taller than the pane scrolls as a whole.

## Elements

Elements are the building blocks of a tree a `ui.render` hook returns, and you get them from `$.ui.resolve(e)`. [Build a tree from elements](/docs/en/plugins/mods/interface#build-a-tree-from-elements) shows the common ones with how the terminal draws them. A check mark means the app can draw the element.

| Element | Main props | Terminal | Desktop |
| :- | :- | :-: | :-: |
| [`Box`](/docs/en/plugins/mods/interface#build-a-tree-from-elements) | `key`, flex layout, `gap`, `padding`, `margin`, `width`, `height`, `borderStyle`, `backgroundColor`, `position`, `hover` | ✓ | ✓ |
| [`Text`](/docs/en/plugins/mods/interface#build-a-tree-from-elements) | `color`, `backgroundColor`, `bold`, `italic`, `underline`, `dimColor`, `inverse`, `wrap` | ✓ | ✓ |
| [`Button`](/docs/en/plugins/mods/interface#respond-to-presses-and-typing) | `key`, `label`, `onPress`, `hotkey`, `plain`, `dimColor`, `autoFocus`, `action` | ✓ | ✓ |
| `Link` | `href`, `label` | ✓ | ✓ |
| `Code` | The code, up to 10,000 characters | ✓ | ✓ |
| `Markdown` | `text`, up to 10,000 characters, `key`, `dimColor`, `onLinkPress`, `pressableLinks` | ✓ | ✓ |
| [`Input`](/docs/en/plugins/mods/interface#take-typed-input-and-draw-a-row-for-each-item) | `key`, `label`, `placeholder`, `value`, `submitLabel`, `onSubmit`, `onInput`, `autoFocus` | ✓ | ✓ |
| `Select` | `key`, `label`, `options`, `value`, `onSelect`, `autoFocus` | ✓ | ✓ |
| `Svg` | An SVG document, up to 131,072 characters | | ✓ |
| [`Client`](/docs/en/plugins/mods/interface#build-a-tree-from-elements) | `module`, `key` | ✓ | ✓ |
| [`Raster`](/docs/en/plugins/mods/interface#draw-a-grid-of-colored-cells) | `key`, `columns` up to 512, `rows` up to 256, `cells`. See [Draw a grid of colored cells](/docs/en/plugins/mods/interface#draw-a-grid-of-colored-cells). | ✓ | |
| `Image` | PNG or RGBA bytes up to 2 MiB, or a file path | ✓ | |

Three more `Button` rules: `action` names one of Claude Code's own [keybinding actions](/docs/en/keybindings), and the user's binding for it presses the button when that binding is a chord or a modified key. A digit `hotkey` on a button in the band also fires when the user types that digit alone into an empty prompt and pauses. When two buttons in one drawing name the same `hotkey`, the later one gets it. Claude Code refuses `autoFocus: false` on any control, so leave the prop off instead.

## Limits

Hooks and mods API calls run under time and size limits. Claude Code skips a hook that runs past a time limit and rejects a call that passes a size limit.

| Limit | Value |
| :- | :- |
| A hook's own running time for one event, not counting time inside `next` or a mods API call other than `$.clock.sleep` | 10 seconds |
| A `.catch` handler's running time | 1 second |
| All `session.end` hooks together | 1.5 seconds |
| `$.process.run` timeout | 30 seconds by default, 10 minutes at most |
| `$.model.complete` `maxTokens` | 1024 by default, up to 64,000 or the model's output limit |
| `$.fs.read` and `$.fs.write` | 4 MiB for one file |
| One string child of a `Text` | 10,000 characters |
| `$.store` | 4 MiB of JSON in total |
| `$.session.messages()` | The newest 4,096 entries |
| `$.ui.invalidate('ui.render')` redraws | Throttled to 10 a second, 30 for the visible pane and the band. Calls that come sooner are coalesced. |
| `$.ui.toast` | Shown for 4 seconds unless you pass `{ timeoutMs }` |
| A pane opened without the user asking | Placed from 144 terminal columns, 110 after they've opened it once |
| Command, tool, subagent type, and pane names | Letters, digits, `_`, and `-`, up to 64 characters |
| One `claude plugin test` test | 5 seconds unless the test sets `timeoutMs` |

## Settings and environment variables

These are the settings and environment variables that affect mods. The Where column says which settings file or environment each one is read from:

| Name | Where | What it does |
| :- | :- | :- |
| `CLAUDE_CODE_PLUGIN_DIRS` | Environment, or `env` in `~/.claude/settings.json` | Plugin directories to load as `--plugin-dir` does, for apps you can't pass a flag to. Absolute paths separated by `:`, or `;` on Windows. |
| `CLAUDE_CODE_PLUGIN_DIR_WATCH` | Environment | `1` makes a long-running non-interactive session reload `--plugin-dir` mods on save |
| `prependPlugins`, `appendPlugins` | Managed settings. User settings only on a machine with no managed settings, for a user who isn't signed in with a Team or Enterprise plan. | Lists of plugin ids, such as `acme-guard@acme-tools`. Mods in `prependPlugins` run before every mod a user installs, and mods in `appendPlugins` run after, in the listed order. See [The order mods run in](/docs/en/plugins/mods/events#the-order-mods-run-in). |
| `allowManagedModsOnly` | Managed settings, as an [option on the built-in guard](/docs/en/plugins/mods/admin#set-options-on-the-built-in-guard) | Only mods that [count as your organization's](/docs/en/plugins/mods/admin#install-your-organizations-mods), and mods built into Claude Code, load. Users' settings hooks keep running. |
| `allowModsToOverrideDenyRules` | Managed settings, as an [option on the built-in guard](/docs/en/plugins/mods/admin#set-options-on-the-built-in-guard) | Lets a mod a user installed approve a tool call that a `deny` rule refuses |
| `allowManagedHooksOnly` | Managed settings | Blocks hooks and installed mods that aren't your organization's. See [what keeps running](/docs/en/settings-reference#what-runs-under-allowmanagedhooksonly). |
| `disableAllHooks` | Any settings file | In managed settings, no mod or hook from an installed plugin runs. In your own settings, what your organization manages keeps running. See [`disableAllHooks`](/docs/en/settings-reference#disableallhooks). |
| `disableSideloadFlags` | Managed settings | Rejects `--plugin-dir` and `--plugin-url` at startup |
| `pluginConfigs` | User or managed settings | Holds `userConfig` values for a mod, keyed by the plugin's id, such as `acme-guard@acme-tools`, or its name and `@inline`, such as `first-mod@inline`, for one loaded with `--plugin-dir` |

`sec-default@builtin` is a guard built into Claude Code, listed as `cc-plugin-sec-default` in `/plugin` and the debug log. It loads ahead of every mod a person installs on a machine with managed settings, or for a user signed in with a Team or Enterprise plan. If managed `prependPlugins` is set, the guard loads only when that list names it, at the position listed. Its source is in the [`mods/sec-default` directory of the Claude Code repository](https://github.com/anthropics/claude-code/tree/main/mods/sec-default).

## Commands

These commands and flags load, inspect, and test a mod. The `claude` commands run in your shell and the `/` commands at the Claude Code prompt. In the table, `<directory>` stands for a path you type, as in `claude plugin validate ./first-mod`. Square brackets mark an argument you can leave out.

| Command | What it does |
| :- | :- |
| [`/plugin`](/docs/en/plugins/mods/overview#see-which-mods-a-session-loaded) | Shows a line such as `1 mod active · first-mod` under its tabs when a mod that isn't built in has loaded |
| [`claude plugin validate <directory>`](/docs/en/plugins/mods/create#check-what-claude-code-reads-from-your-mod) | Reads a plugin's manifest and hooks module and reports errors, the events it hooks, and the mods API calls it makes. `--strict` treats warnings as errors and `--json` prints a machine-readable report. |
| [`claude plugin test [directory]`](/docs/en/plugins/mods/test#write-a-test) | Runs every file under the directory, or the current directory when you give none, whose name ends in `.test.ts` or `.test.tsx`. Exits with status 1 when a test fails. |
| [`claude --plugin-dir <directory>`](/docs/en/plugins/mods/create#write-a-mod-yourself) | Loads a plugin directory for one session and reloads its hooks module when you save. Repeat the flag to load several. |
| `/reload-plugins` | Reloads plugins when you run it |
