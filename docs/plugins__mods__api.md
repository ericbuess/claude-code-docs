> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use the mods API

> Call the mods API from a Claude Code mod to add commands and tools, call a model, run work on a timer, message other sessions, and reach files and the network.

The mods API is the set of methods a mod calls to act: add commands and tools, call a model, run work between events, and reach the file system, processes, and the network. Every hook receives it as its first argument, `$`, with the methods grouped in namespaces such as `$.ui` and `$.fs`. [Events](/docs/en/plugins/mods/events) decide when a hook runs, and the mods API is what the hook calls once it does.

Build your [first mod](/docs/en/plugins/mods/create) before you start here. For every method, see [mods API methods](/docs/en/plugins/mods/reference#mods-api-methods) or read [the types for your build](/docs/en/plugins/mods/create#get-the-types-for-your-build).

## Add a command or a tool

A mod can add a command for the user to run and a tool for Claude to call. Register both in a [`session.start`](/docs/en/plugins/mods/reference#session) hook. Claude Code waits for that hook before the first prompt, so what you register is available from the first turn.

### Add a command

A command is for the user. Register it, then handle [`command.run`](/docs/en/plugins/mods/reference#commands-and-configuration) for its name. This example adds a `/standup` command that takes an optional number of days:

```javascript theme={null}
on('session.start', async ($, e, next) => {
  // Add /standup to the command list, with the description the user sees there
  await $.command.register({ name: 'standup', description: 'Summarize what changed today', argumentHint: '[days]' })
  return next(e)
})

// The matcher limits the hook to /standup, so other commands don't reach it
on('command.run', { command: 'standup' }, async ($, e) => {
  // e.args is the text typed after the command name, or an empty string
  return { text: 'Summary for the last ' + (e.args || '1') + ' day(s): ...' }
})
```

After the session starts, `/standup` appears with its description in the list you see when you type `/`. The `argumentHint` shows in the prompt after you type the command and a space, as in `/standup [days]`. When you run `/standup 3`, the second hook returns `Summary for the last 3 day(s): ...`, and the transcript shows that text after the plugin's name. The hook never calls `next`, because the command has no behavior other than yours.

The `text` you return prints in the transcript and Claude reads it. To print nothing, as a command that only opens a [pane](/docs/en/plugins/mods/interface#pick-where-to-draw) does, return `{}`. To let the command run while Claude is working, add `immediate: true` to the registration.

Pick a name that no built-in command uses. Type `/` in a session to see them. `$.command.register` throws for a taken name, with a message such as `"/focus" refused: it is the built-in /focus`. A hook that throws is skipped, so the rest of your `session.start` hook doesn't run either. Register commands last in that hook, or wrap the call in `try` and `catch`.

### Add a tool

A tool is for Claude. Register it with a name, a description Claude reads, and a JSON Schema for its input. Claude sees it under a longer name made of `mcp__`, your plugin's name, two underscores, and the name you registered. You handle its calls in a [`tool.call`](/docs/en/plugins/mods/events#guard-or-change-a-tool-call) hook filtered to that full name. This example, from a plugin named `my-mod`, registers `ticket`, so the full name is `mcp__my-mod__ticket`. It gives Claude a tool that looks up a ticket in an issue tracker:

```javascript theme={null}
on('session.start', async ($, e, next) => {
  await $.tool.register({
    name: 'ticket',
    // Claude decides when to call the tool from this description
    description: 'Look up a ticket by its id and return its title and status',
    // The arguments Claude has to send: one required string named id
    inputSchema: { type: 'object', properties: { id: { type: 'string' } }, required: ['id'] },
  })
  return next(e)
})

// The full tool name is mcp__, the plugin's name, and the registered name
on('tool.call', { tool: 'mcp__my-mod__ticket' }, async ($, e) => {
  // The tool's arguments are fields of e, so the id is e.id
  const response = await $.http.fetch('https://tickets.example.com/api/' + encodeURIComponent(e.id))
  // Return a result either way, so Claude learns when the lookup failed
  return { result: response.ok ? response.text : 'Lookup failed with status ' + response.status }
})
```

When you ask about a ticket, Claude can call `mcp__my-mod__ticket` with its id. The second hook fetches the ticket and returns the response body, which Claude reads as the tool's result. When the server answers with an error status, Claude reads `Lookup failed with status` and the number.

<Tip>
  When [MCP tool search](/docs/en/mcp#scale-with-mcp-tool-search) defers a registered tool, Claude sees its name but not its description until it searches for it. If Claude should consider the tool on every turn, add [`isDeferred: false`](/docs/en/plugins/mods/reference#tools) to the registration to [load the full tool upfront](/docs/en/mcp#exempt-a-server-from-deferral). The field requires Claude Code v2.1.293 or later, and earlier versions ignore it.
</Tip>

## Call a model

A mod can ask a model a question of its own, outside the conversation, for a small job such as sorting or summarizing a piece of text. `$.model.complete` sends one prompt to a model with your session's credentials and resolves to the reply. It has no conversation history.

This hook answers a `/triage` command, [registered as a command](#add-a-command), by asking a small model to label the text typed after it:

```javascript theme={null}
on('command.run', { command: 'triage' }, async ($, e) => {
  const r = await $.model.complete({
    model: 'haiku',
    // The system prompt sets the job, and the prompt carries the text to label
    system: 'Reply with one word: bug, feature, or question.',
    prompt: e.args,
    // One word needs few tokens, and the call gives up after 15 seconds
    maxTokens: 20,
    timeoutMs: 15000,
  })
  // r.text exists only when the model answered, so check r.isAnswered first
  const label = r.isAnswered ? r.text.trim() : 'unknown'
  return { text: 'Label: ' + label }
})
```

When you run `/triage the export button does nothing`, the mod sends that text to the model and prints its answer, such as `Label: bug`. Claude's conversation isn't part of the request. When the model doesn't answer, the label is `unknown`.

A Claude API failure doesn't reject the call, so check `r.isAnswered`, and read `r.reason` when it's `false`. The call rejects for a request Claude Code won't send, such as a model your organization blocks. [The types for your build](/docs/en/plugins/mods/create#get-the-types-for-your-build) list the other options, such as `effort`, and the [limits](/docs/en/plugins/mods/reference#limits) give the `maxTokens` default.

`$.model.fork({ prompt })` asks one question over the current conversation instead, with the same model and system prompt, so the Claude API serves most of it from the prompt cache.

These calls use the user's plan or API key.

## Run work in the background

Work that outlives one event, such as checking on something once a minute, runs on a timer you start from `session.start`. A hook itself runs for one event and has a [time limit](/docs/en/plugins/mods/reference#limits) on its own execution time. Time spent waiting on `next` or on a mods API call doesn't count, except a `$.clock.sleep`. `$.clock.every` and `$.clock.after` take the place of `setInterval` and `setTimeout`, with the delay in milliseconds first: `$.clock.after(5000, fn)` calls `fn` once, five seconds from now. Each returns a timer with a `cancel()` method, and `await $.clock.now()` gives the time in milliseconds.

This hook looks up a pull request's checks once a minute and shows the result under the prompt. `summarize` is a function of your own that turns the command's JSON output into a few words:

```javascript theme={null}
on('session.start', async ($, e, next) => {
  // Call the function every 60,000 milliseconds, starting one minute from now
  $.clock.every(60_000, async () => {
    const status = await $.process.run(['gh', 'pr', 'checks', '--json', 'state'])
    // Replace the line under the prompt with the latest summary
    $.ui.status('checks: ' + summarize(status.stdout))
  })
  // Return without waiting for the timer, so the session starts right away
  return next(e)
})
```

The session starts as usual. A minute later, a line appears under the prompt with a `⚠`, the mod's name, and then `checks:` and your summary. It's replaced once a minute after that. The timer's callback runs outside any event, so it keeps running between turns and doesn't start one. If the callback throws, the error goes to the [debug log](/docs/en/plugins/mods/troubleshoot#read-the-debug-log) and the timer runs again at the next interval.

### Show something without starting a turn

A background job can show the user something without starting a turn. Each of these calls puts text in a different place:

| Call | What the user sees |
| :- | :- |
| `$.ui.status(text)` | One line under the prompt that stays until you change it. It starts with `⚠` and the mod's name, as in `⚠ my-mod: checks: 3 passing`. |
| `$.ui.toast(text)` | A toast notification at the top right, with the mod's name above the text, that disappears after a few seconds |
| `$.ui.log(text)` | A dim line in the transcript that Claude doesn't read. It starts with `●` and the mod's name, as in `● my-mod: build finished`. |

### Start a turn from a background job

When a background job finds something that needs Claude's attention, it can start a turn by submitting a prompt with `$.prompt.submit({ text })`. Claude reads the text after a sentence that names your mod as the sender. To send it as the user's own words, without that sentence, add `asUser: true`. The call waits until the session is idle and then starts a new turn. It resolves when that turn starts, so don't `await` it in a handler that runs while Claude is working.

### Stop background work

Timers stop when the module reloads. For long-running work inside a hook, [`next.signal`](/docs/en/plugins/mods/reference#the-hook-function) is an `AbortSignal` that aborts when the event your hook is handling is abandoned, for example when the user interrupts, so pass it to anything long-running.

## Send and receive messages between sessions

A mod can send a plain-text message to another of your sessions or to one of this session's subagents, and observe the messages that arrive and leave. `$.session.send({ to, text })` sends one, the same delivery the SendMessage tool makes. `to` is `{ sessionId }` for a session, `{ agentId }` for a subagent from `$.agent.list()`, or the string address a received message came from. The call resolves once the message is queued, with `{ isDelivered: true }`. When nothing was delivered it resolves with `{ isDelivered: false, reason }`, and `reason` says why.

This hook answers a `/ping` command, [registered as a command](#add-a-command), by asking the session whose id you type after it for a status:

```javascript theme={null}
on('command.run', { command: 'ping' }, async ($, e) => {
  // e.args is the session id typed after /ping
  const sent = await $.session.send({ to: { sessionId: e.args }, text: 'Status? One line.' })
  // The call resolves either way, so check isDelivered to learn what happened
  if (!sent.isDelivered) $.ui.toast('Not delivered: ' + sent.reason)
  // An empty result prints nothing in this session's transcript
  return {}
})
```

When the message is queued, nothing appears in your session, and the other session's Claude reads `Status? One line.` When nothing was delivered, a toast notification gives the reason.

`session.receive` and `session.send` let a mod observe the messages. Return `next(e)` from both to pass each message through unchanged:

| Event | Fires when | Useful fields |
| :- | :- | :- |
| `session.receive` | A message arrives for this session, before Claude reads it | `e.text`, and `e.origin.kind`, such as `peer` or `peer-send-message` for another session or agent, `task-notification`, or `scheduled-trigger`. Return `{ consumed: reason }` to keep it from Claude. |
| `session.send` | A message is about to leave, from the SendMessage tool or a mod | `e.to`, `e.text`, and `e.origin.kind`, which is `model` or `plugin` |

A session set to [refuse inbound messages](/docs/en/cross-session-messaging#control-inbound-messages) refuses a message before `session.receive` fires, so a hook never sees it. A message that's held for your approval reaches the hook first, so a mod can read a message you haven't approved yet. The hook's `next(e)` rejects when the message isn't delivered.

The sender's name on a received message is whatever the sender wrote, so don't base a decision on it.

## Reach files, processes, and the network

A mod reaches the file system, processes, and the network through the mods API, with the same permissions as the user running Claude Code. The hooks module itself has no Node.js APIs, no timer globals such as `setTimeout`, and no network or file access of its own. Standard JavaScript and web APIs such as `URL`, `TextEncoder`, `AbortController`, and `crypto.subtle` are available. Each namespace below covers one kind of access:

| Namespace | What it does |
| :- | :- |
| `$.fs` | `read(path)`, `write(path, text)`, `exists(path)`, `stat(path)`, and `list(path)` work on files and directories |
| `$.process` | `run(['git', 'status'])` starts a command and resolves when it exits. `spawn` streams a long-running command's output. |
| `$.http` | `fetch(url, init)` over `http` or `https`. It resolves to `{ status, ok, headers, text }` once the body is read. |
| `$.store` | A JSON key-value store of your plugin's own, kept between sessions |
| `$.env` | `get` and `set` environment variables. Write the name as a string literal. |
| `$.settings` | `read` what the settings files and managed policy hold |
| `$.session` | `messages()` returns the transcript as a list of `{ role, text, toolUses }`. Also the working directory, model, and more. [`usage()`](/docs/en/plugins/mods/reference#mods-api-methods) returns context window use and plan limits. |
| `$.mcp` | `call` a tool on a connected MCP server |

Files and processes have a few rules of their own:

* **Paths**: a relative path resolves against the session's working directory
* **`$.fs.list`**: returns one directory's entries as `{ name, kind, size, isLink }` and isn't recursive
* **`$.process.run`**: takes an argument list and uses no shell. It resolves to `{ exitCode, stdout, stderr }` whatever the exit code. It rejects if the program can't start or is still running at the timeout, which is 30 seconds by default, so wrap it in `try` and `catch`.

Every one of these calls is itself an event, named for its namespace and method without the `$.`, such as `fs.read` for `$.fs.read`. A mod [earlier in the chain](/docs/en/plugins/mods/events#the-order-mods-run-in) can observe, rewrite, or refuse your call, which is how an organization restricts what mods reach.

A mod can refuse your `$.process.spawn` call after the command has produced output or exited, and nothing the command did is undone. The call then rejects with a message that ends with one of these strings and the refusing mod's reason:

* **`$.process.spawn started, and a plugin withheld its result:`**: the refusing mod hadn't read the command's output to the end. Claude Code stops the command if it's still running.
* **`$.process.spawn ran, and a plugin withheld its result:`**: the refusing mod had read the command's output to the end, so the command had exited

## Next steps

* [React to events](/docs/en/plugins/mods/events): hook tool calls, prompts, and turns
* [Draw in the interface](/docs/en/plugins/mods/interface): show what your mod collects in a pane or above the prompt
* [Test a mod](/docs/en/plugins/mods/test): stub any of these calls in a test
* [Mods reference](/docs/en/plugins/mods/reference): events, mods API methods, and limits
