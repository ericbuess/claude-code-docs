> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# React to events with a mod

> Handle Claude Code events from a mod: observe, rewrite, or answer tool calls, prompts, and turns, filter which events a hook handles, and plan for other mods.

A hook is an event handler: a function that Claude Code runs when a named event happens. Claude Code fires an event at each point where it's about to act, such as when it runs a tool, submits a prompt, sends a request to the model, or starts or ends a session. Your hook runs before Claude Code acts, so it can observe the event, rewrite it, or answer it in Claude Code's place. You register a hook with [`on(eventName, handler)`](https://code.claude.com/docs/en/plugins/mods/reference#the-hook-function).

Build your [first mod](https://code.claude.com/docs/en/plugins/mods/create.md) before you start here. For every event and its exact fields, see the [reference](https://code.claude.com/docs/en/plugins/mods/reference.md#events) or read [the types for your build](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build).

## How a hook handles an event

A hook sits between an event and what Claude Code would do about it, so it can observe the event, rewrite it, or answer it itself. It receives three arguments: the [mods API](https://code.claude.com/docs/en/plugins/mods/api.md) as `$`, the event as `e`, and the next handler as `next`. The handlers for an event form a middleware chain. `next(e)` calls the next handler, which is another mod's hook or, at the end of the chain, Claude Code's own behavior, and it resolves to the result. What your hook does with `next` decides which of the three it does.

### Observe an event

To observe an event without changing it, do your work and return `next(e)`. This hook logs each tool Claude is about to use:

```javascript theme={null}
on('tool.call', async ($, e, next) => {
  // Runs before the tool does
  $.ui.log('Claude is about to use ' + e.tool)
  // Pass the event on unchanged
  return next(e)
})
```

Before each tool runs, a dim line such as `● my-mod: Claude is about to use Bash` appears in the transcript, where `my-mod` is your plugin's name. The tool runs as it would without the mod.

To act after the event, `await next(e)`, do your work, and return the result. This hook logs each tool after it has run:

```javascript theme={null}
on('tool.call', async ($, e, next) => {
  // Let the tool run, and wait for its result
  const result = await next(e)
  // Runs after the tool does
  $.ui.log(e.tool + ' finished')
  // Give the result back unchanged
  return result
})
```

The line now appears after each tool finishes. Claude reads the same result either way, because the hook returns what `next(e)` resolved to.

### Rewrite an event

To change what Claude Code acts on, such as the text of a prompt, call `next` with a modified copy of the event. The event itself is immutable: it's deeply frozen, and assigning to a field throws. This hook trims each prompt before it's sent:

```javascript theme={null}
on('prompt.submit', async ($, e, next) => {
  // Pass on a copy of the event with its text changed
  return next({ ...e, text: e.text.trim() })
})
```

Later handlers and Claude Code receive the trimmed prompt and never see the original. You can also change the result: `await next(e)`, then return a copy of the result with a field replaced.

### Answer an event

To handle an event yourself, return a result without calling `next`. That short-circuits the chain, so later mods and Claude Code's own behavior don't run. This hook refuses every Bash command:

```javascript theme={null}
on('tool.call', { tool: 'Bash' }, async () => {
  // No call to next, so the command never runs
  return { deny: 'Bash is turned off in this project. Use the file tools.' }
})
```

When Claude tries a Bash command, the command doesn't run, and Claude reads the `deny` text as the tool's result. Each event has its own result shape, which the [events reference](https://code.claude.com/docs/en/plugins/mods/reference.md#events) lists.

### Filter which events a hook handles

To run a hook for some events only, pass a filter as the second argument to `on`. Claude Code calls the filter a matcher. It's an object whose fields are compared with the event's, and the hook runs only when every field matches. A field can be a value, an array of allowed values, or a regular expression.

Each line in this example registers the same function, `hook`, for a narrower set of tool calls:

```javascript theme={null}
// A string matches one value: Bash calls only
on('tool.call', { tool: 'Bash' }, hook)
// An array matches any value in it: Edit calls and Write calls
on('tool.call', { tool: ['Edit', 'Write'] }, hook)
// A regular expression matches by pattern: every tool of one MCP server
on('tool.call', { tool: /^mcp__github__/ }, hook)
```

`hook` runs once for a Bash, Edit, or Write call, and once for a call to a tool whose name starts with `mcp__github__`. A call to any other tool, such as Read, matches none of the three, so `hook` doesn't run for it.

The event name can be a wildcard. `'classic.*'` matches every [settings hook event](#hook-the-settings-hook-events). `'*'` matches every event except the [telemetry events](https://code.claude.com/docs/en/plugins/mods/reference.md#telemetry), which take their own name and a `{ to: 'collector' }` filter.

Register each event once per matcher. If you call `on` twice for `session.start` with no matcher, the module fails to load with `on("session.start") is registered twice without a matcher`. Put everything your mod does at session start in one hook.

## Hook what Claude is doing

Handle these events to see or change a tool call, a prompt, a turn, or a settings read as it happens. For every event and what a hook can return, see the [events reference](https://code.claude.com/docs/en/plugins/mods/reference.md#events).

### Guard or change a tool call

A `tool.call` hook sees each tool Claude is about to use, so it can refuse the call, change its arguments, or let it through. `tool.call` fires when Claude Code is about to run a tool, including calls a subagent makes and calls to MCP tools. `e.tool` is the tool's name and the tool's arguments are fields of `e`, such as `e.command` for Bash. When you call `next(e)`, Claude Code runs the permission check and then the tool.

This hook refuses a Bash command that force-pushes, and tells Claude why:

```javascript theme={null}
// The matcher limits the hook to Bash calls, so e.command is the shell command
on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
  if (/git push .*--force/.test(e.command)) {
    // Returning without calling next answers the event, so the command never runs
    return { deny: 'Force pushes are not allowed in this repository. Push to a new branch instead.' }
  }
  // Every other command goes on to the permission check and then to Bash
  return next(e)
})
```

When Claude tries `git push --force`, the command doesn't run and no permission prompt appears, because the hook never calls `next`. Claude reads the `deny` text as the tool's result, so write it as an instruction Claude can act on. Every other Bash command runs as it would without the mod.

If this hook throws or times out, Claude Code skips it and the command goes on as it would without the mod. To refuse the command instead, [add a `.catch` handler](#handle-a-hook-that-fails) to the hook.

To act after a tool has run, `await next(e)`, do your work, and return what `next` gave you. This hook logs each `.mdx` file Claude changes, with [`$.ui.log`](https://code.claude.com/docs/en/plugins/mods/api#show-something-without-starting-a-turn), which adds a dim line to the transcript that Claude doesn't read:

```javascript theme={null}
on('tool.call', { tool: ['Edit', 'Write'] }, async ($, e, next) => {
  // Wait for the permission check and the tool, and keep what they produced
  const result = await next(e)
  // A refused call comes back as { deny }, and a failed one has isError set
  const changed = !result.deny && !result.isError
  if (changed && e.file_path.endsWith('.mdx')) $.ui.log('Claude changed ' + e.file_path)
  // Return the result as it came, so Claude reads what the tool returned
  return result
})
```

After Claude edits or writes an `.mdx` file, a dim line in the transcript names the file. Nothing is logged for another kind of file, or for a call that was refused or failed. Claude's view of the call doesn't change, because the hook returns the result it received.

Your hook can also change a call, retry it, answer it itself, or withhold its result:

* **Change the call**: pass changed arguments to `next`.
* **Retry the call**: call `next(e)` again. A hook that sees `isError` on the first result can run the tool a second time and return that result.
* **Answer the call yourself**: return an object with a `result` field, without calling `next`, and for a built-in tool, give `result` the shape that tool's own result has in [the types for your build](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build). No permission prompt appears and the tool doesn't run, so the result you return is all Claude learns about what happened.
* **Withhold the result from Claude**: return `{ deny: reason }` after `await next(e)`. Claude reads your reason in place of what `next` returned. When the tool ran, the deny keeps its result from Claude and undoes nothing the tool did. When the tool ran and succeeded, the reason follows a note such as `Bash ran, and a plugin withheld its result:`.

Hooks in your organization's [managed settings](https://code.claude.com/docs/en/server-managed-settings.md) run before any mod's `tool.call` hook. When a managed hook blocks the call, no mod's `tool.call` hook runs for that call.

#### Hold a tool call until the user decides

A hook can pause a tool call and ask the user what to do before it goes ahead. A `tool.call` hook can `await` before it calls `next` or returns, and the tool call stays pending until then. To put the question to the user, call `$.ui.ask`. It shows your question above a numbered list of your options, in the dialog Claude uses to ask you something, and resolves to the label the user picks. After your options, the dialog adds a row for typing a different answer and a **Chat about this** row.

The `RISKY` pattern in this example matches `rm -r`, `rm -rf`, `git reset --hard`, and `git push` with `--force`, and it misses other spellings such as `git push -f`. This module asks before it runs a Bash command that matches the pattern:

```javascript theme={null}
const RISKY = /\brm\s+-rf?\b|\bgit\s+reset\s+--hard\b|\bgit\s+push\b.*--force/

export function register(on) {
  on('tool.call', { tool: 'Bash' }, async ($, e, next) => {
    // Let every other command through without a question
    if (!RISKY.test(e.command)) return next(e)
    // Start from the safe answer, so a question nobody answers refuses the command
    let answer = 'Refuse'
    try {
      // The tool call waits here until the user picks one of the two labels
      answer = await $.ui.ask('Run this command? ' + e.command, ['Run it', 'Refuse'])
    } catch {
      // The user dismissed the question, or this is a claude -p run with nobody to ask
    }
    if (answer !== 'Run it') {
      // Answer without calling next, so the command doesn't run
      return { deny: 'The user declined this command. Ask before trying a different approach.' }
    }
    return next(e)
  })
}
```

When Claude tries a command such as `rm -rf build`, the question appears with the command in it, and the command waits for the answer:

* **The user picks Run it**: the hook calls `next(e)`, and the usual permission check still runs after it
* **The user picks Refuse**: the command doesn't run, and Claude reads the `deny` text
* **The user types an answer**: `$.ui.ask` resolves to the typed text. The hook compares it with `Run it`, so any other text refuses the command.
* **Nobody answers**: `$.ui.ask` rejects when the user dismisses the question or picks **Chat about this**, and in a `claude -p` run, so the `catch` block leaves the answer at `Refuse`

Keep the wait inside a mods API call such as `$.ui.ask`, because that time doesn't count against the hook's [time limit](https://code.claude.com/docs/en/plugins/mods/reference.md#limits). Time spent awaiting a promise of your own does count.

Claude Code skips a hook that times out, so the held command would run. To refuse it instead, chain [a `.catch` handler](#handle-a-hook-that-fails) onto the registration that `on` returns. That handler is separate from the `catch` block inside the hook.

#### Approve or refuse a tool call before the user is asked

To decide whether a tool call may run, handle [`tool.check`](https://code.claude.com/docs/en/plugins/mods/reference#tools), the event where Claude Code makes that decision.

For a fixed command or path, use a [permission rule](https://code.claude.com/docs/en/permissions.md#permission-rule-syntax) such as `Bash(npm test)`, which takes no code. Handle `tool.check` when the decision depends on what's true at that moment, such as the current Git branch or a value another hook recorded.

* **What to return**: to decide the call yourself, return an object of your own, such as `{ decision: 'allow' }` or `{ decision: 'deny', reason }`. To leave the decision alone, return what `await next(e)` gives you.
* **What `await next(e)` gives you**: Claude Code's own decision, as an object whose `decision` is `allow`, `ask`, or `deny`. No permission prompt appears while `next(e)` runs.
* **Arguments**: `e.input` holds the tool's arguments, such as `command` for Bash
* **When `tool.check` fires**: after the [`PreToolUse` hooks](https://code.claude.com/docs/en/hooks#pretooluse) run, and before the permission prompt, [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode)'s classifier, or a [`PermissionRequest`](https://code.claude.com/docs/en/hooks#permissionrequest) hook

This hook refuses `git push` while the current branch is `main`:

```javascript theme={null}
on('tool.check', { tool: 'Bash' }, async ($, e, next) => {
  // Claude Code's own decision
  const decided = await next(e)
  if (!e.input.command.includes('git push')) return decided
  const branch = await $.process.run(['git', 'branch', '--show-current'])
  if (branch.stdout.trim() !== 'main') return decided
  return { decision: 'deny', reason: 'Push from a branch other than main' }
})
```

The hook denies `git push` on `main` and passes every other call through:

* **On `main`**: the hook returns `deny`, even when a rule allows `git push`
* **On another branch, and for other commands**: the call gets the decision it would get without the mod
* **The hook throws or times out**: the call also gets the decision it would get without the mod. To refuse the call instead, [add a `.catch` handler](#handle-a-hook-that-fails) that returns `{ decision: 'deny', reason: 'the reason' }`.

The hook matches the text of the command, so treat it as a reminder for Claude. To block pushes to `main` for everyone, protect the branch on your Git host.

> [!NOTE]
>
> A `tool.check` hook can also return `allow` or `ask`. In [plan mode](https://code.claude.com/docs/en/permissions.md#hook-approvals-in-plan-mode), for a call that isn't read-only, such as a file edit, your hook can tighten the decision `next(e)` returns but can't loosen it. For the permission rules and `PreToolUse` hook decisions your hook's `allow` can't replace, see [Extend permissions with hooks](https://code.claude.com/docs/en/permissions.md#precedence-among-rules-hooks-and-mods).

#### Check whether a tool call is read-only

In a [`tool.check`](#approve-or-refuse-a-tool-call-before-the-user-is-asked) hook, `e.isReadOnly` is `true` when the tool reports the call as read-only. Otherwise the field is absent, not `false`. `e.isReadOnly` requires Claude Code v2.1.304 or later.

Some tools, such as Read, Grep, Glob, and WebSearch, report every call as read-only. Bash and MCP tools report a call as read-only in these cases:

* **Bash**: the command passes Claude Code's built-in [read-only command check](https://code.claude.com/docs/en/permissions.md#read-only-commands)
* **An MCP tool**: the server sets the tool's `readOnlyHint` annotation to `true`

The value is the tool's own report, so don't approve a call on this field alone. For example, WebFetch and Agent calls report as read-only, though [WebFetch](https://code.claude.com/docs/en/tools-reference.md#webfetch-tool-behavior) requests a URL and [Agent](https://code.claude.com/docs/en/tools-reference.md#agent-tool-behavior) starts a subagent that runs tools of its own.

This hook returns an `ask` for every `mcp__github__` call that isn't read-only and wasn't already denied:

```javascript theme={null}
on('tool.check', { tool: /^mcp__github__/ }, async ($, e, next) => {
  const decided = await next(e)
  // Read-only calls and denied calls pass through unchanged
  if (e.isReadOnly || decided.decision === 'deny') return decided
  return { decision: 'ask', reason: 'This tool can change the GitHub repository' }
})
```

#### Filter a `tool.check` hook by whether the call is read-only

To limit which calls your hook handles by [`e.isReadOnly`](#check-whether-a-tool-call-is-read-only), use the [matcher](#filter-which-events-a-hook-handles) for read-only calls and the hook body for the rest:

* **Read-only calls only**: add `isReadOnly: true` to the matcher, as in `on('tool.check', { tool: 'Bash', isReadOnly: true }, hook)`
* **Calls that aren't read-only**: test `e.isReadOnly` in the hook body, as the [`mcp__github__` example](#check-whether-a-tool-call-is-read-only) does. If you put `isReadOnly: false` in a matcher, your hook never runs.

### Rewrite or add to a prompt

A `prompt.submit` hook sees each prompt before the turn starts, so it can rewrite the text or add to it. `e.text` is what was typed.

| To do this | Return this |
| :- | :- |
| Rewrite the prompt. The transcript and your [prompt history](https://code.claude.com/docs/en/interactive-mode.md#command-history) show the new text. | `next({ ...e, text: newText })` |
| Add text only Claude reads, after the prompt | `next({ ...e, context: [...(e.context ?? []), extraText] })` |
| Stop the prompt from being sent | `{ drop: 'the reason' }` |

This hook adds the current branch name for Claude whenever a prompt mentions a pull request:

```javascript theme={null}
on('prompt.submit', async ($, e, next) => {
  // Pass on a prompt that doesn't mention a pull request as it is
  if (!/\bPR\b|pull request/i.test(e.text)) return next(e)
  const git = await $.process.run(['git', 'branch', '--show-current'])
  // Outside a git repository the command fails, so there's no branch to add
  if (git.exitCode !== 0) return next(e)
  // Keep any context an earlier hook added, and add one more line for Claude
  return next({ ...e, context: [...(e.context ?? []), 'Current branch: ' + git.stdout.trim()] })
})
```

When you send a prompt such as `open a PR for this change`, your message looks the same in the transcript, and Claude also reads a line such as `Current branch: feature/auth` after it. A prompt that doesn't mention a pull request goes through unchanged, and `git` doesn't run.

To stop a prompt, return `{ drop: 'the reason' }` without calling `next`. The text goes back into the user's prompt input, and they see `Prompt dropped by a hook:` followed by your reason, so address the reason to them. The prompt still goes through in these cases:

* **Your hook returns a `drop` after its `next(e)` call let the prompt through**: the turn still runs, and the hook [fails](#handle-a-hook-that-fails) with a message that includes `a drop after its next() was answered`
* **Your hook throws or times out**: Claude Code skips it and sends the prompt. [Add a `.catch` handler](#handle-a-hook-that-fails) so that a failure doesn't send a prompt the hook would have stopped.

[Other events](https://code.claude.com/docs/en/plugins/mods/reference.md#prompts-and-what-claude-reads) cover the rest of what Claude reads: `prompt.section` for each section of the system prompt, `prompt.context` for the context sent with the first message, and `skill.prompt` for a skill's text. Text from these hooks that changes between requests [invalidates the prompt cache](https://code.claude.com/docs/en/prompt-caching.md). In a `skill.prompt` hook, you can also read [which plugin or file the skill came from](https://code.claude.com/docs/en/plugins/mods/reference.md#skill-prompt-fields).

### Follow a turn

A turn is everything Claude does in answer to one prompt. Handle `turn.start`, `turn.step`, and `turn.complete` to follow one:

| Event | When it fires | What a hook can do |
| :- | :- | :- |
| `turn.start` | A turn begins | Observe. `e.turnId` identifies the turn in the other two events. |
| `turn.step` | Claude Code is about to send one request to the model. A turn with tool calls has several. `e.agentId` is set for a subagent's request. | Read each request's token usage, send it to a different model with `next({ ...e, model })`, or answer without calling the model |
| `turn.complete` | The turn ended, including a turn the user interrupted, where `e.isAborted` is `true`. `e.answer` is Claude's final text, `e.durationMs` how long it took, and `e.usage` the turn's token totals. A subagent's turn fires it with `e.agentId` set. | Observe, or return an object with a `text` field, such as `{ text: 'Done in 12 seconds' }`, to show a line under the answer |

Write a `turn.step` hook as an async generator, because the event streams. `yield* next(e)` forwards the response as it streams and evaluates to the finished result. This hook logs how much of each request the Claude API served from the [prompt cache](https://code.claude.com/docs/en/prompt-caching.md):

```javascript theme={null}
// function* makes the hook a generator, which can pass the response on piece by piece
on('turn.step', async function* ($, e, next) {
  // Send the request, forward each piece as it arrives, and keep the finished result
  const result = yield* next(e)
  // Skip a result that reports no token counts
  if (result.usage) {
    $.ui.log('cache read ' + result.usage.cache_read_input_tokens + ' · wrote ' + result.usage.cache_creation_input_tokens)
  }
  // Return the result unchanged, so the turn continues as usual
  return result
})
```

Claude's response streams to the screen as it does without the mod. After each request finishes, a dim line in the transcript gives the number of tokens read from the cache and the number written to it. A turn with tool calls has several requests, so it adds several lines.

`result.usage` holds the token counts the Claude API reports for a request, plus the `model` that answered: `input_tokens`, `output_tokens`, `cache_read_input_tokens`, and `cache_creation_input_tokens`. The hook runs for subagents' requests too, so check `e.agentId` when you want only the main conversation.

To see the tool calls that the API ran itself during the request, such as calls to the [advisor tool](https://code.claude.com/docs/en/advisor.md), read `result.serverToolUses`. Claude Code doesn't run these calls, so no `tool.call` or `tool.check` hook fires for them. The field is absent when the response has no such calls, and it requires Claude Code v2.1.290 or later.

### Change or refuse a settings read

A `settings.read` hook runs on a mod's read and on Claude Code's own read:

* **A mod's read**: a mod calls [`$.settings.read`](https://code.claude.com/docs/en/plugins/mods/api#read-one-source-or-one-key).
* **Claude Code's own read**: Claude Code builds the session's merged settings. This read repeats when settings or the loaded plugins change.

Before you rely on either read, check the guard and your version:

* **The built-in guard**: with managed settings, or with a Team or Enterprise [`/login`](https://code.claude.com/docs/en/authentication#authentication-precedence) as the session's credential, the [built-in guard](https://code.claude.com/docs/en/plugins/mods/admin.md#know-what-happens-by-default) can skip this hook in a mod you install or load with `--plugin-dir`. To check, search the [debug log](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#read-the-debug-log) for `settings.read bypassed by cc-plugin-sec-default`. If a line with that text names your mod, ask your organization's administrator to [install the mod as one of the organization's mods](https://code.claude.com/docs/en/plugins/mods/admin.md#install-your-organizations-mods).
* **The version**: the event firing on Claude Code's own read, and the `e.layers` field, require Claude Code v2.1.304 or later.

#### What a `settings.read` hook receives

| Field | Type | What it holds |
| :- | :- | :- |
| `e.layers` | array | One `{ source, settings }` object for each source in use that holds settings, lowest [precedence](https://code.claude.com/docs/en/settings.md#settings-precedence) first: `plugin`, `user`, `project`, `local`, `flag`, `policy`. Empty in `claude plugin test`. |
| `e.source` | string | The one source a mod asked for, as in `$.settings.read({ source: 'policy' })`. `e.layers` then holds that layer alone. Absent on Claude Code's own read and on any other read of the merged settings. |

In `e.layers`, `plugin` holds settings that enabled plugins supply, and is a layer name only, not a `source` you can pass to `$.settings.read`. `flag` holds the settings passed with `--settings`, and `policy` holds managed settings.

#### Tell Claude Code's own read from a mod's read

On [Claude Code's own read](#settings-read-hook), [`next.origin`](https://code.claude.com/docs/en/plugins/mods/reference#the-hook-function) is `{ plugin: 'engine', tier: 'core' }`, and on a mod's read `next.origin.plugin` is the calling mod's name.

#### What a `settings.read` hook can return

Your hook can return [`next(e)`](https://code.claude.com/docs/en/plugins/mods/reference#the-hook-function)'s result unchanged, a `{ value }` of its own, or `{ deny: reason }`. On [Claude Code's own read](#settings-read-hook) and a mod's read, a `{ value }` replaces what the read gives and `{ deny: reason }` refuses the read:

| Return | On Claude Code's own read | On a mod's read |
| :- | :- | :- |
| `{ value }` | For each key you change, what you return replaces that key's whole value in the session's merged settings, if it [fits the key's schema](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#settings-read-key-refused) | That mod's call resolves to your `value`, or to the `key` it asked for taken from your `value`, so return a whole object and not an array |
| `{ deny: reason }` | The session keeps the settings as they were merged before any hook answered, and the [debug log records your `reason`](https://code.claude.com/docs/en/plugins/mods/troubleshoot#settings-read-refused) | That mod's call rejects with `<calling mod>: $.settings.read: <reason>` |

On Claude Code's own read, build your `{ value }` from [`next(e)`'s `value`](#settings-read-next), since a key you leave out is unset. Where Claude Code reads a key such as `env` from each source separately, changing it in your `value` [has no effect](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#settings-read-key-no-effect).

#### What `next(e)` gives a `settings.read` hook

`next(e)` resolves to `{ value }` or to `{ deny }`:

* **`{ value }`**: `value` is the merged settings, or one source's settings when [`e.source`](#settings-read-receives) is set. If a hook that [runs after yours](#the-order-mods-run-in) returned a `{ value }` of its own, you get that hook's `value` instead.
* **`{ deny }`**: a hook that runs after yours refused the read. Return that `{ deny }` unchanged.

#### Change one setting from a `settings.read` hook

First check [which mods get this event, and from which version](#settings-read-hook).

To change one key, spread the `value` from [`next(e)`](https://code.claude.com/docs/en/plugins/mods/reference#the-hook-function) and set that key, as this hook does with [`spinnerTipsEnabled`](https://code.claude.com/docs/en/settings-reference#spinnertipsenabled). The hook doesn't check [`next.origin`](#settings-read-origin), so the hook changes the key on [Claude Code's own read](#settings-read-hook) and on a mod's merged read alike:

```javascript theme={null}
on('settings.read', async ($, e, next) => {
  const read = await next(e)
  // Pass through a read of one source, so that only the merged settings change.
  // Pass through a { deny } from a later hook too: it has no value.
  if (e.source || !read.value) return read
  // Keep every other key and change this one
  return { value: { ...read.value, spinnerTipsEnabled: false } }
})
```

On Claude Code's own read, if your hook returns a value outside the key's schema, such as a string, that key alone keeps the value merged before any hook answered. The debug log then says [`the answer for <key> is no value the key can hold`](https://code.claude.com/docs/en/plugins/mods/troubleshoot#settings-read-key-refused). If your value fits and the key still doesn't change, see [why a returned key has no effect](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#settings-read-key-no-effect).

### Handle the settings hook events

Settings hooks are the command, HTTP, prompt, and agent hooks you configure in settings files. Each [settings hook event](https://code.claude.com/docs/en/hooks.md#hook-events), such as `Stop`, `SessionEnd`, or `PostToolUse`, is also an event named `classic.` followed by the settings hook event's name, such as `classic.Stop`. `e` is the JSON a settings hook receives on stdin, including `transcript_path`. Where the [built-in guard](https://code.claude.com/docs/en/plugins/mods/admin.md#know-what-happens-by-default) loads, [a hook on these events in a mod you install doesn't run](https://code.claude.com/docs/en/plugins/mods/admin.md#hooks-the-guard-passes-over).

This hook uses `Stop`, which fires when Claude finishes responding, to log where the session's transcript is saved:

```javascript theme={null}
on('classic.Stop', async ($, e, next) => {
  // e has the same fields a Stop hook in a settings file reads from stdin
  $.ui.log('Transcript saved at ' + e.transcript_path)
  // Pass the event on, so Stop hooks in your settings files still run
  return next(e)
})
```

Each time Claude finishes responding, a dim line in the transcript gives the path of the transcript file. The hook returns `next(e)`, so it observes the event and changes nothing about how the turn ends.

## Run alongside other mods

Several mods can handle the same event, and any one of them can fail. If your mod blocks tool calls, check its position in the chain and what happens when its hook fails.

### The order mods run in

Hooks on the same event form one middleware chain. Each mod's `next` calls the following mod's hook, and the last `next` reaches Claude Code's own behavior. The first mod is outermost: it sees the event before the others and the result after them, and it decides whether the others run at all. A later mod can't stop an earlier one from seeing an event.

Claude Code orders the chain by where each mod comes from:

1. The built-in guard `sec-default@builtin`, a mod built into Claude Code that `/plugin` lists as `cc-plugin-sec-default`, where [it loads](https://code.claude.com/docs/en/plugins/mods/admin.md#know-what-happens-by-default), mods your organization lists in [`prependPlugins`](https://code.claude.com/docs/en/plugins/mods/admin#install-your-organizations-mods), and then any other mod that counts as your organization's and isn't in `appendPlugins`
2. Mods you install
3. Mods your organization lists in `appendPlugins`
4. Other mods built into Claude Code

Among the mods you install, a mod runs before the mods it lists under `dependencies` in its manifest. Within one module, hooks run in the order `register` called `on`.

#### Where settings hooks run in the order

The `PreToolUse` hooks configured in settings files also run during a tool call, at fixed points in the chain of mods:

* **`PreToolUse` hooks from managed settings**: run before the first mod's `tool.call` hook. When a managed hook blocks the call, no mod's `tool.call` hook runs for that call.
* **`PreToolUse` hooks from every other settings file and from plugins' `hooks/hooks.json`**: run after the last mod calls `next`, as part of Claude Code's own behavior. A mod that answers `tool.call` without calling `next` keeps them from running, and a mod that calls `next` sees their decision in the result it returns.

[`tool.check`](#approve-or-refuse-a-tool-call-before-the-user-is-asked) fires after the `PreToolUse` hooks have run. For the permission rules and `PreToolUse` hook decisions a `tool.check` hook's `allow` can't replace, see [Extend permissions with hooks](https://code.claude.com/docs/en/permissions.md#precedence-among-rules-hooks-and-mods).

### Handle a hook that fails

A hook that fails doesn't break the session, and you can decide what happens instead. When a hook with no `.catch` handler throws, times out, or returns a result of the wrong shape, what happens next depends on whether it had called `next`:

* **It failed before calling `next`**: Claude Code skips it, and the next handler runs in its place
* **It failed after `next` resolved**: that result stands, and nothing runs a second time

One line names the mod, the event, and the reason, such as `my-mod: tool.call hook skipped: threw Error: boom`. Where you read it depends on the session, as [Find out why a mod does nothing](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing) lists. A `ui.render` hook whose [tree doesn't validate](https://code.claude.com/docs/en/plugins/mods/interface.md#build-a-tree-from-elements) counts as one that returned the wrong shape.

To make a hook that blocks calls fail closed, add a `.catch` error handler that answers in its place. Here, `guard` is your hook function, and the handler tests [`next.called`](https://code.claude.com/docs/en/plugins/mods/reference#the-hook-function) to tell whether `guard` had already called `next` when it failed:

```javascript theme={null}
// on returns a registration, and .catch attaches a handler to that one hook
on('tool.call', { tool: 'Bash' }, guard).catch(async ($, e, next) => {
  // guard had already called next, so return what came back
  if (next.called) return next(e)
  // next.error.kind says why the handler was asked, such as 'throw' or 'timeout'
  return { deny: 'The command guard failed, so this command was not run: ' + next.error.kind }
})
```

When `guard` throws or times out on a Bash call, Claude Code calls the handler with the same event:

* **`guard` failed before it called `next`**: the command doesn't run, and Claude reads the `deny` text with the kind at the end
* **`guard` failed after it called `next`**: the handler's `next(e)` resolves to the result that `guard`'s call produced without running the command again, and Claude reads that result

The handler has a shorter [time limit](https://code.claude.com/docs/en/plugins/mods/reference.md#limits) of its own. If the handler itself throws or times out, Claude Code skips the hook as if it had no handler. When `guard` hadn't called `next`, the command then goes on as it would without the mod.

The same handler shape fits a guard on `prompt.submit` or `config.set`. When `next.called` is false, return the refusal that the [events reference](https://code.claude.com/docs/en/plugins/mods/reference.md#events) lists for that event: `{ drop: 'the reason' }` for `prompt.submit`, `{ deny: 'the reason' }` for `config.set`.

At `tool.check` and `plugin.register`, a refusal returned after `next` resolved still holds, so return it without testing `next.called`:

* **`tool.check`**: return `{ decision: 'deny', reason: 'the reason' }`
* **`plugin.register`**: return `{ refuse: 'the reason' }`, as [Refuse mods when your check fails](https://code.claude.com/docs/en/plugins/mods/admin.md#refuse-mods-when-your-check-fails) shows

At `tool.call`, a `deny` returned after `next` resolved [withholds the result from Claude](#guard-or-change-a-tool-call).

## Next steps

* [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api.md): add commands and tools, call a model, and run work on a timer
* [Draw in the interface](https://code.claude.com/docs/en/plugins/mods/interface.md): show what your hooks collect in a pane or above the prompt
* [Test a mod](https://code.claude.com/docs/en/plugins/mods/test.md): fire any of these events from a test
* [Mods reference](https://code.claude.com/docs/en/plugins/mods/reference.md): every event, every mods API method, and the limits
