> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# React to events with a mod

> Handle Claude Code events from a mod: observe, rewrite, or answer tool calls, prompts, and turns, filter which events a hook handles, and plan for other mods.

A hook is an event handler: a function that Claude Code runs when a named event happens. Claude Code fires an event at each point where it's about to act, such as when it runs a tool, submits a prompt, sends a request to the model, or starts or ends a session. Your hook runs before Claude Code acts, so it can observe the event, rewrite it, or answer it in Claude Code's place. You register a hook with [`on(eventName, handler)`](/docs/en/plugins/mods/reference#the-hook-function).

Build your [first mod](/docs/en/plugins/mods/create) before you start here. For every event and its exact fields, see the [reference](/docs/en/plugins/mods/reference#events) or read [the types for your build](/docs/en/plugins/mods/create#get-the-types-for-your-build).

## How a hook handles an event

A hook sits between an event and what Claude Code would do about it, so it can observe the event, rewrite it, or answer it itself. It receives three arguments: the [mods API](/docs/en/plugins/mods/api) as `$`, the event as `e`, and the next handler as `next`. The handlers for an event form a middleware chain. `next(e)` calls the next handler, which is another mod's hook or, at the end of the chain, Claude Code's own behavior, and it resolves to the result. What your hook does with `next` decides which of the three it does.

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

To change what Claude Code acts on, such as the text of a prompt, call `next` with a modified copy of the event. The event itself is immutable: it's frozen at every depth, and assigning to a field throws. This hook trims each prompt before it's sent:

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

When Claude tries a Bash command, the command doesn't run, and Claude reads the `deny` text as the tool's result. Each event has its own result shape, which the [events reference](/docs/en/plugins/mods/reference#events) lists.

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

The event name can be a wildcard. `'classic.*'` matches every [settings hook event](#hook-the-settings-hook-events). `'*'` matches every event except the [telemetry events](/docs/en/plugins/mods/reference#telemetry), which you hook by name or as `'telemetry.*'`.

Register each event once per matcher. If you call `on` twice for `session.start` with no matcher, the module fails to load with `on("session.start") is registered twice without a matcher`. Put everything your mod does at session start in one hook.

## Hook what Claude is doing

Hook these events to see or change a tool call, a prompt, or a turn as it happens. For every event and what a hook can return, see the [events reference](/docs/en/plugins/mods/reference#events).

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

To act after a tool has run, `await next(e)`, do your work, and return what `next` gave you. This hook logs each `.mdx` file Claude changes, with [`$.ui.log`](/docs/en/plugins/mods/api#show-something-without-starting-a-turn), which adds a dim line to the transcript that Claude doesn't read:

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

To change a call, pass changed arguments to `next`. To retry a call, call `next(e)` again: a hook that sees `isError` on the first result can run the tool a second time and return that result. To answer a call yourself, return an object with a `result` field, such as `{ result: 'Skipped by my-mod' }`, without calling `next`. When you do that, no permission prompt appears and the tool doesn't run, so the result you return is all Claude learns about what happened.

Hooks in your organization's [managed settings](/docs/en/server-managed-settings) run before any mod's `tool.call` hook, and a block from one of them is final.

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

Keep the wait inside a mods API call such as `$.ui.ask`, because that time doesn't count against the hook's [10-second time limit](/docs/en/plugins/mods/reference#limits). Time spent awaiting a promise of your own does count. Claude Code skips a hook that times out, so the held command would run.

#### Approve or refuse a tool call before the user is asked

To decide whether a tool call may run, handle [`tool.check`](/docs/en/plugins/mods/reference#tools), the event where Claude Code makes that decision. It fires after the permission rules and the settings hooks have decided, and `next(e)` resolves to their decision: `allow`, `ask`, or `deny`. Your hook returns that decision or a different one. `e.input` holds the tool's arguments, such as `command` for Bash.

For a fixed command or path, use a [permission rule](/docs/en/permissions#permission-rule-syntax) such as `Bash(npm test)`, which takes no code. Handle `tool.check` when the decision depends on what's true at that moment, such as the current Git branch or a value another hook recorded.

This hook refuses `git push` while the current branch is `main`:

```javascript theme={null}
on('tool.check', { tool: 'Bash' }, async ($, e, next) => {
  // What the permission rules and settings hooks decided: 'allow', 'ask', or 'deny'
  const decided = await next(e)
  if (!e.input.command.includes('git push')) return decided
  const branch = await $.process.run(['git', 'branch', '--show-current'])
  if (branch.stdout.trim() !== 'main') return decided
  return { decision: 'deny', reason: 'Push from a branch other than main' }
})
```

On `main`, the hook returns `deny`, even when a rule allows `git push`. On another branch, and for other commands, the call gets the decision it would get without the mod.

The hook matches the text of the command, so treat it as a reminder for Claude. To block pushes to `main` for everyone, protect the branch on your Git host.

A hook can return any of the three decisions, so it can also approve a call that a `PreToolUse` hook outside managed settings blocked. [Extend permissions with hooks](/docs/en/permissions#extend-permissions-with-hooks) lists which decisions hold over a mod.

### Rewrite or add to a prompt

A `prompt.submit` hook sees each prompt before the turn starts, so it can rewrite the text or add to it. `e.text` is what was typed.

| To do this | Return this |
| :- | :- |
| Rewrite the prompt. The message in the transcript shows the new text. | `next({ ...e, text: newText })` |
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

[Other events](/docs/en/plugins/mods/reference#prompts-and-what-claude-reads) cover the rest of what Claude reads: `prompt.section` for each section of the system prompt, `prompt.context` for the context sent with the first message, and `skill.prompt` for a skill's text. Text from these hooks that changes between requests [invalidates the prompt cache](/docs/en/prompt-caching).

### Follow a turn

A turn is everything Claude does in answer to one prompt. Hook `turn.start`, `turn.step`, and `turn.complete` to follow one:

| Event | When it fires | What a hook can do |
| :- | :- | :- |
| `turn.start` | A turn begins | Observe. `e.turnId` identifies the turn in the other two events. |
| `turn.step` | Claude Code is about to send one request to the model. A turn with tool calls has several. `e.agentId` is set for a subagent's request. | Read each request's token usage, send it to a different model with `next({ ...e, model })`, or answer without calling the model |
| `turn.complete` | The turn ended, including a turn the user interrupted, where `e.isAborted` is `true`. `e.answer` is Claude's final text, `e.durationMs` how long it took, and `e.usage` the turn's token totals. A subagent's turn fires it with `e.agentId` set. | Observe, or return an object with a `text` field, such as `{ text: 'Done in 12 seconds' }`, to show a line under the answer |

Write a `turn.step` hook as an async generator, because the event streams. `yield* next(e)` forwards the response as it streams and evaluates to the finished result. This hook logs how much of each request the Claude API served from the [prompt cache](/docs/en/prompt-caching):

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

`result.usage` holds the four token counts the Claude API reports for a request, plus the `model` that answered: `input_tokens`, `output_tokens`, `cache_read_input_tokens`, and `cache_creation_input_tokens`. The hook runs for subagents' requests too, so check `e.agentId` when you want only the main conversation.

### Hook the settings hook events

Settings hooks are the command, HTTP, prompt, and agent hooks you configure in settings files. Each [settings hook event](/docs/en/hooks#hook-events), such as `Stop`, `SessionEnd`, or `PostToolUse`, is also an event named `classic.` followed by the settings hook event's name, such as `classic.Stop`. `e` is the JSON a settings hook receives on stdin, including `transcript_path`.

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

Several mods can hook the same event, and any one of them can fail. If your mod blocks tool calls, check its position in the chain and what happens when its hook fails.

### The order mods run in

Hooks on the same event form one middleware chain. Each mod's `next` calls the following mod's hook, and the last `next` reaches Claude Code's own behavior. The first mod is outermost: it sees the event before the others and the result after them, and it decides whether the others run at all. A later mod can't stop an earlier one from seeing an event.

Claude Code orders the chain by where each mod comes from:

1. The built-in guard `sec-default@builtin`, a mod built into Claude Code that `/plugin` lists as `cc-plugin-sec-default`, where [it loads](/docs/en/plugins/mods/admin#know-what-happens-by-default), mods your organization lists in [`prependPlugins`](/docs/en/plugins/mods/admin#install-your-organizations-mods), and then any other mod that counts as your organization's and isn't in `appendPlugins`
2. Mods you install
3. Mods your organization lists in `appendPlugins`
4. Other mods built into Claude Code

Among the mods you install, a mod runs before the mods it lists under `dependencies` in its manifest. Within one module, hooks run in the order `register` called `on`.

#### Where settings hooks run in the order

The `PreToolUse` hooks configured in settings files also run during a tool call, at fixed points in the chain of mods:

* **`PreToolUse` hooks from managed settings**: run before the first mod's `tool.call` hook, and a block from one of them is final, so no mod sees the call.
* **`PreToolUse` hooks from every other settings file and from plugins' `hooks/hooks.json`**: run after the last mod calls `next`, as part of Claude Code's own behavior. A mod that answers `tool.call` without calling `next` keeps them from running, and a mod that calls `next` sees their decision in the result it returns.

[`tool.check`](#approve-or-refuse-a-tool-call-before-the-user-is-asked) fires after those hooks and the permission rules have decided, so a hook on it can approve a call that a hook in the second group blocked.

### Handle a hook that fails

A hook that fails doesn't break the session, and you can decide what happens instead. When a hook with no `.catch` handler throws, times out, or returns a result of the wrong shape, what happens next depends on whether it had called `next`:

* **It failed before calling `next`**: Claude Code skips it, and the next handler runs in its place
* **It failed after `next` resolved**: that result stands, and nothing runs a second time

One line names the mod, the event, and the reason, such as `my-mod: tool.call hook skipped: threw Error: boom`. Where you read it depends on the session, as [Find out why a mod does nothing](/docs/en/plugins/mods/troubleshoot#find-out-why-a-mod-does-nothing) lists. A `ui.render` hook whose drawing doesn't validate is reported differently, as [Build a tree from elements](/docs/en/plugins/mods/interface#build-a-tree-from-elements) describes.

To make a hook that blocks calls fail closed, add a `.catch` error handler that answers in its place. Here, `guard` is your hook function:

```javascript theme={null}
// on returns a registration, and .catch attaches a handler to that one hook
on('tool.call', { tool: 'Bash' }, guard).catch(async ($, e, next) => {
  // next.error.kind is 'throw' or 'timeout', which says how guard failed
  return { deny: 'The command guard failed, so this command was not run: ' + next.error.kind }
})
```

While `guard` works, the handler never runs. When `guard` throws or times out on a Bash call, Claude Code calls the handler with the same event. The handler returns `{ deny }`, so the command doesn't run, and Claude reads the text with `throw` or `timeout` at the end. Without the handler, Claude Code would skip `guard` and run the command. The handler has [one second](/docs/en/plugins/mods/reference#limits) to answer.

## Next steps

* [Use the mods API](/docs/en/plugins/mods/api): add commands and tools, call a model, and run work on a timer
* [Draw in the interface](/docs/en/plugins/mods/interface): show what your hooks collect in a pane or above the prompt
* [Test a mod](/docs/en/plugins/mods/test): raise any of these events from a test
* [Mods reference](/docs/en/plugins/mods/reference): every event, every mods API method, and the limits
