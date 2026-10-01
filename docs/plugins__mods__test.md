> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Test a mod

> Write automated tests for a Claude Code mod that raise events, stub Claude Code's answers, and press buttons, with no session, sign-in, or network.

You can write automated tests for a mod and run them from your shell with [`claude plugin test`](/docs/en/plugins/mods/reference#commands). A test raises the events your hooks handle and checks what the hooks did, so you catch a problem before it reaches a session. The first example tests the mod from [Create a mod](/docs/en/plugins/mods/create).

## Write a test

A test loads your mod, sends events through its hooks the way Claude Code would, and checks what the hooks did, without a session, a sign-in, or a network. You run tests from your shell with `claude plugin test`, and each test file imports the test kit, a test library in the `claude-code/testing` module.

Give each test file a name that ends in `.test.ts`, such as `first-mod.test.ts`, and save it anywhere in the plugin directory. Every test file needs at least one `test()`, or the run fails with `declares no test(): nothing ran`. A test file can import your mod's own files and sibling `.ts` helpers, so you can unit test plain functions, such as a game's rules, without the kit.

This test raises two tool calls, runs the `/tally` command from [Create a mod](/docs/en/plugins/mods/create), and checks that the reply counts both. Its first line is a [stub](#stub-what-claude-code-would-answer), which answers the tool calls in Claude Code's place. Save it as `first-mod/tests/first-mod.test.ts`:

```typescript first-mod/tests/first-mod.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

test('/tally reports the tool calls the mod has seen', async ($, on) => {
  // Answer each tool call in Claude Code's place, so no tool runs
  on('tool.call', () => ({ result: 'ok' }))

  // Raise two tool calls, which the mod's tool.call hook counts
  await $.tool.call({ tool: 'Bash', command: 'ls' })
  await $.tool.call({ tool: 'Read', file_path: 'README.md' })

  // Run /tally and check the text its hook returns
  const answer = await $.command.run({ command: 'tally', args: '' })
  expect(answer.text).toBe('Claude has made 2 tool calls since this mod loaded')
})
```

In your shell, run the tests from the `first-mod` directory:

```bash theme={null}
claude plugin test
```

The output names each test and whether it passed, with timings that vary from run to run:

```text theme={null}
tests/first-mod.test.ts:
(pass) /tally reports the tool calls the mod has seen [22.87ms]

 1 pass
 0 fail
Ran 1 test across 1 file. [0.19s]
```

Each `$.tool.call` went through the mod's [`tool.call`](/docs/en/plugins/mods/reference#tools) hook, which added one to its count and passed the call on to the stub. No `ls` ran and no file was read. `$.command.run` then went to the mod's [`command.run`](/docs/en/plugins/mods/reference#commands-and-configuration) hook, and `answer` is the object that hook returned.

The command exits with status 1 when a test fails, so it works in CI. If your own mods can't load in the shell that runs it, it prints a line starting `claude plugin test: hooks modules are turned off` with the reason, and exits with status 1.

### Stub what Claude Code would answer

No model, store, or tool runs in a test, so wherever your mod expects Claude Code to answer, the test supplies the answer with a stub. A test function receives two arguments for that:

* **`$`**: the test's own `$`, which stands where Claude Code does. It isn't the [mods API](/docs/en/plugins/mods/reference#mods-api-methods) that a hook receives. Each of its methods raises the event of the same name, sends it through your mod's hooks, and resolves to the result: `$.tool.call({ tool: 'Bash', command: 'ls' })` raises `tool.call`. `$.command.run`, `$.prompt.submit`, `$.session.start`, and `$.turn.complete` work the same way, and `$.classic.Stop` and the other `$.classic` methods raise a [settings hook event](/docs/en/plugins/mods/events#hook-the-settings-hook-events). A test can't raise a mods API call such as `ui.close` directly. Trigger it through your mod, for example by pressing the button that closes the pane.
* **`on`**: call it to register stubs, which are hooks that answer in Claude Code's place. Name a stub for a mods API call without the `$.`, so a stub registered as `store.get` answers your mod's `$.store.get`. When your mod calls [`$.model.complete`](/docs/en/plugins/mods/api#call-a-model) or [`$.store.get`](/docs/en/plugins/mods/interface#keep-state), a stub supplies the answer.

This example stubs a model call. The hook belongs to a mod named `grader`, and handles a `/grade` command that sends a sentence to a model and reports whether the reply starts with `PASS`. The file holds only the hook under test, so the mod also needs a `plugin.json` and a `hooks.json`, as in [Create a mod](/docs/en/plugins/mods/create#write-a-mod-yourself). To type `/grade` in a session, the mod also has to [register the command](/docs/en/plugins/mods/api#add-a-command):

```javascript grader/hooks/register.js theme={null}
export function register(on) {
  on('command.run', { command: 'grade' }, async ($, e) => {
    // e.args is the text typed after /grade
    const reply = await $.model.complete({
      model: 'haiku',
      system: 'Grade the sentence. Start your reply with PASS or FAIL.',
      prompt: e.args,
    })
    const passed = reply.isAnswered && reply.text.startsWith('PASS')
    return { text: passed ? 'Passed' : 'Try again' }
  })
}
```

This test stubs the model call to check what the hook does with a passing reply:

```typescript grader/tests/grader.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

test('a passing grade is reported', async ($, on) => {
  // Answer the mod's $.model.complete call with a fixed reply, so no model runs
  on('model.complete', () => ({
    value: {
      isAnswered: true,
      text: 'PASS\nNice sentence.',
      usage: { input_tokens: 10, output_tokens: 5, cache_read_input_tokens: 0, cache_creation_input_tokens: 0 },
    },
  }))

  // Run /grade, which makes the mod call the model
  const answer = await $.command.run({ command: 'grade', args: 'The cat sat on the mat.' })
  expect(answer.text).toBe('Passed')
})
```

The test passes because the hook's `reply` is the object under `value`, whose `text` starts with `PASS`. To check the other branch, add a second test whose stub returns a `text` that starts with `FAIL`, and expect `Try again`.

A stub for a mods API call returns an object with a `value` field, which holds what the call resolves to in your mod: `{ value: 7 }` makes `$.store.get` resolve to `7`. A stub for one of Claude Code's events, such as [`turn.step`](/docs/en/plugins/mods/reference#turns) or `tool.call`, returns that event's own result, such as `{ result: 'ok' }`. `$.session.send` and `$.prompt.fill` take their event's result too, as the table shows. [Look up what a stub returns](#look-up-what-a-stub-returns) shows which form each common name takes. Two errors mean a stub is wrong or missing. A failed test's output includes a block headed `the engine reported:`, and each error appears there:

* `returned neither { value } nor { deny }`: a stub for a mods API call returned a bare value
* `no implementation for` followed by a name: your mod made that call and no stub answers it

The kit also exports in-memory mocks that answer a whole namespace for you. `mock.clock(on)` answers [`$.clock`](/docs/en/plugins/mods/api#run-work-in-the-background), `mock.store(on, { count: 7 })` answers `$.store` from a store that starts with those entries, and `mock.env(on, { CI: 'true' })` answers `$.env.get` from those variables. `mock.clock` returns a mock clock that your test advances, so a test of a timer doesn't wait. `mock.store` returns nothing, so to check what your mod saved, write the two `store` stubs yourself as the [drawing test](#test-a-drawing) does.

### Follow the test kit's rules

The test kit has a few rules of its own, and breaking one produces the errors new test authors hit first:

* **Register every stub before the test's first call on `$`.** Calling `on` after that throws an error such as `on("ui.render") after the test first called $`.

* **[`session.start`](/docs/en/plugins/mods/reference#session) doesn't run by itself.** Each test starts with your module freshly loaded and none of its hooks called, so module-level variables hold their initial values. If a hook depends on what `session.start` sets up, raise it first:

  ```typescript theme={null}
  // Answer the event after your hook passes it on with next(e)
  on('session.start', () => ({ cwd: '/work' }))
  // Answer the $.command.register call your hook makes
  on('command.register', () => ({ value: undefined }))
  // Raise the event, which runs your session.start hook
  await $.session.start({ surface: 'terminal', isInteractive: true, cwd: '/work' })
  ```

  The second stub answers the `$.command.register` call that a `session.start` hook such as the [tutorial's](/docs/en/plugins/mods/create#write-a-mod-yourself) makes. Without it, that call rejects with `no implementation for command.register` and the kit skips your hook, so nothing after the call in the hook runs. The test doesn't fail at that point. The skipped hook is listed under `the engine reported:` only if a later check fails.

* **A hook that returns `next(e)` needs a stub to answer.** When your [`ui.render`](/docs/en/plugins/mods/reference#interface) hook returns `next(e)`, for example to draw nothing while Claude is idle, [mounting it](#test-a-drawing) fails with `no implementation for ui.render`. Register a stub that returns an element as plain data:

  ```typescript theme={null}
  // Stands for what Claude Code would draw at the site
  on('ui.render', () => ({ type: 'Text', props: {}, children: ['drawn by Claude Code'] }))
  ```

  With the stub registered, the mount succeeds, and `ui.find({ type: 'Text' })` returns that element whenever your hook returned `next(e)`.

* **A stub for `turn.step` is an async generator**, and the test reads the stream to its end to get the result:

  ```typescript theme={null}
  on('turn.step', async function* ($, e) {
    // Each yield is one piece of the model's streamed reply
    yield { kind: 'text', index: 0, text: 'ok' }
    // The return value is the result of the whole request
    return { turnId: e.turnId, index: e.index, answer: 'ok', toolUses: [], stopReason: 'end_turn', usage: null }
  })

  // Raise one request to the model, which runs your turn.step hook
  const stream = $.turn.step({ turnId: 't', index: 0, model: 'claude-test', messageCount: 1 })
  // Read every piece until the stream says it's done
  let step = await stream.next()
  while (step.done !== true) step = await stream.next()
  const result = step.value
  ```

  When the loop ends, `result` is the object the stub returned, after your `turn.step` hook has had the chance to change it. Here `result.answer` is `'ok'`.

* **Raise a tool call with the tool's name and arguments as fields**, such as `await $.tool.call({ tool: 'Bash', command: 'ls' })`, and register a `tool.call` stub that returns `{ result }`.

### Look up what a stub returns

Every mods API call your mod makes in a test needs a stub that answers in Claude Code's place, except the few the kit answers itself: [`$.ui.invalidate`](/docs/en/plugins/mods/interface#redraw-when-something-changes) and [`$.state`](/docs/en/plugins/mods/interface#keep-state) calls. For `$.clock` calls, use `mock.clock(on)`, or your mod's `$.clock.now()` fails with `no implementation for clock.now`.

This table lists the ones mods use most. The first column is the call your mod makes or the event it passes on with `next(e)`. The second is the function to pass to `on` under that name, so the `$.store.get` row becomes `on('store.get', ($, e) => ({ value: saved.get(e.key) }))`. A `'...'` in a stub marks text for you to fill in:

| Your mod calls or passes on | Stub |
| :- | :- |
| `$.command.register`, `$.tool.register`, `$.ui.toast`, `$.ui.log`, `$.ui.status`, `$.ui.close`, `$.store.set` | `() => ({ value: undefined })`. For `ui.toast` and `ui.log`, the text is `e.text`. |
| `$.store.get` | `($, e) => ({ value: saved.get(e.key) })` |
| `$.fs.read` | `($, e) => ({ value: e.path.endsWith('notes.md') ? '# Notes' : '' })`. `e.path` arrives as an absolute path, so compare with `endsWith`. |
| `$.ui.open` | `() => ({ value: { isPlaced: true } })` |
| `$.ui.ask` | A `tool.call` stub, because the question reaches it as a call to the `AskUserQuestion` tool: `($, e) => ({ result: { answers: { [e.questions[0].question]: 'Run it' } } })`. Check `e.tool` first if your mod passes on other tool calls. |
| `$.model.complete` | `() => ({ value: { isAnswered: true, text: '...', usage } })` |
| `$.process.run` | `($, e) => ({ value: { exitCode: 0, stdout: '...', stderr: '' } })`. `e.argv` is the argument list and `e.init` holds `cwd` and `timeoutMs`. |
| Any mods API call that should fail | `() => ({ deny: 'the reason' })`, which makes the call reject in your mod. A stub that throws is skipped instead. |
| `session.start` | `() => ({ cwd: '/work' })` |
| `turn.start` | `($, e) => ({ turnId: e.turnId })` |
| `tool.call` | `() => ({ result: '...' })` |
| `turn.complete` | `() => ({ text: '' })`. Raise it with `$.turn.complete({ turnId, answer, durationMs, isAborted: false, usage: null })`. |
| `prompt.submit` | `($, e) => ({ text: e.text })` |
| `prompt.fill` | `() => ({ isFilled: true })` |
| `$.prompt.read` | `() => ({ value: { text: '...', cursor: 0 } })` |
| `$.ui.copy` | `() => ({ value: { isCopied: true } })` |
| `$.session.messages` | `() => ({ value: [{ role: 'assistant', text: '...', toolUses: [] }] })` |
| `$.session.id`, `$.agent.list` | `() => ({ value: 'abc123' })`, `() => ({ value: [] })` |
| `session.send` | `() => ({ isDelivered: true })`. `e.to` arrives as a string even when your mod passed `{ sessionId }`. |
| `session.receive` | `($, e) => ({ text: e.text })`. Raise it with `$.session.receive({ origin: { kind: 'peer-send-message' }, text })`. |
| `ui.render` | `() => ({ type: 'Text', props: {}, children: ['...'] })` |

`expect` has the assertions `toBe`, `toEqual`, `toMatch`, `toMatchObject`, `toContain`, `toBeDefined`, `toBeUndefined`, and `toThrow`, and `.not` before any of them.

## Test a timer

A mod that runs work on a timer needs a clock the test controls, so the test can move time forward instead of waiting. `const clock = mock.clock(on)` returns a mock clock that starts at `0` and moves only when your test moves it. To start at another time, pass it in milliseconds, as in `mock.clock(on, { now: 5000 })`. The clock has these methods:

| Method | What it does |
| :- | :- |
| `await clock.advance(1000)` | Moves the time forward by that many milliseconds and runs each timer that comes due |
| `await clock.set(5000)` | Moves the time forward to that value, as `advance` would |
| `clock.now()` | Returns the time, which is what your mod's `$.clock.now()` resolves to |
| `await clock.settle()` | Runs timers that are already due, such as a chain of zero-delay `$.clock.after` calls, without moving the time |
| `await clock.sleep(2000)` | Inside a stub, makes that stub answer only once the test has advanced that far, which is how you simulate a slow model or process |

This hook belongs to a mod named `countdown`, and handles a `/countdown` command that takes a number of seconds, starts a one-second `$.clock.every` timer, and shows a toast at zero. As with `grader`, the file holds only the hook under test and doesn't register the command:

```javascript countdown/hooks/register.js theme={null}
export function register(on) {
  on('command.run', { command: 'countdown' }, async ($, e) => {
    // e.args is the text typed after /countdown
    let left = Number(e.args)
    const timer = $.clock.every(1000, () => {
      left -= 1
      if (left === 0) {
        timer.cancel()
        $.ui.toast('Time is up')
      }
    })
    // Print nothing in the transcript
    return {}
  })
}
```

This test runs `/countdown 3` and moves the mock clock, so it checks three seconds of behavior without waiting three seconds:

```typescript countdown/tests/countdown.test.ts theme={null}
import { expect, mock, test } from 'claude-code/testing'

test('the countdown ends with a toast', async ($, on) => {
  // Answer every $.clock call from a clock the test controls
  const clock = mock.clock(on)
  // Collect the text of each toast the mod shows
  const toasts: string[] = []
  on('ui.toast', ($, e) => {
    toasts.push(e.text)
    return { value: undefined }
  })

  await $.command.run({ command: 'countdown', args: '3' })
  // After two seconds the timer has fired twice, and no toast is due
  await clock.advance(2000)
  expect(toasts).toEqual([])
  // The third second brings the count to zero
  await clock.advance(1000)
  expect(toasts).toEqual(['Time is up'])
})
```

The first `expect` shows that the toast doesn't come early, and the second shows that it comes once. Each `advance` resolves after the timers that came due have run, so the check on the next line sees their effect.

## Test a drawing

A test can draw one of your mod's [render sites](/docs/en/plugins/mods/reference#render-sites), then press, type into, and find the elements it drew. `$.ui.mount` draws the site through your mod's `ui.render` hook and returns a handle with a method for each of those. To cover several apps in one test, set `surface` to the app to draw for. This test opens the pane from [Build a pane with tabs](/docs/en/plugins/mods/interface#build-a-pane-with-tabs), switches tabs, presses the button, and checks the count in the terminal and the Desktop app:

```typescript hello-tabs/tests/hello-tabs.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

// What Claude Code passes to a ui.render hook for this pane, apart from the app
const PANE = {
  plugin: 'hello-tabs',
  component: 'Pane',
  requestId: 'hello-tabs',
  viewport: { columns: 100, rows: 30 },
  props: {
    title: 'Hello tabs',
    isFocused: true,
    bodyColumns: 60,
    placement: 'inline',
    scroll: { offset: 0, bodyRows: 10 },
    view: {},
  },
} as const

test('the second tab counts presses and saves the count', async ($, on) => {
  // Stub $.store with a Map, so the test can read what the mod saved
  const saved = new Map<string, unknown>()
  on('store.get', ($, e) => ({ value: saved.get(e.key) }))
  on('store.set', ($, e) => {
    saved.set(e.key, e.value)
    return { value: undefined }
  })

  // Draw the pane once for each app
  for (const surface of ['terminal', 'desktop'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    // Press the buttons by the key the mod gave them
    await ui.press({ key: 'tab-two' })
    await ui.press({ key: 'more' })
    // The second tab's count line is in the drawing
    expect(await ui.find({ type: 'Text', text: /^Count: \d+$/ })).toBeDefined()
    await ui.unmount()
  }

  // One press in each app makes two
  expect(saved.get('count')).toBe(2)
})
```

In your shell, run `claude plugin test` from the `hello-tabs` directory. The test passes when both apps draw the count line and the mod has saved `2`. The count carries over from the first app to the second because both mounts use the same loaded module.

The handle that `$.ui.mount` returns has these methods, which address elements by the `key` you gave them:

| Method | What it does |
| :- | :- |
| `press({ key: 'more' })` | Presses the `Button` with that key |
| `input({ key: 'new-note', text: 'buy milk' })` | Types the text into the `Input` with that key and presses Enter. Add `kind: 'change'` to type without submitting. |
| `select({ key: 'size', value: 'large' })` | Picks the option with that value in the `Select` with that key |
| `find({ key: 'more' })` or `find({ type: 'Text', text: 'Count: 2' })` | Returns the first matching element as `{ type, props, children }`, or `undefined`. `text` can be a string or a regular expression. |
| `unmount()` | Removes the drawing |

Each method resolves after your handler has finished, so you can check the result on the next line. Set `props` to what Claude Code would pass for that site. The [render sites table](/docs/en/plugins/mods/reference#render-sites) lists each site's props, and [the types for your build](/docs/en/plugins/mods/create#get-the-types-for-your-build) have their types.

A drawing test checks the tree your hook returns and whether it's valid for that app. It doesn't check how the app paints it, so look at a new layout in a real session as well.

<h3 id="test-a-drawing-after-clear">
  Test a drawing after `/clear`
</h3>

Each test starts with every `$.state` value at its default, which is how `/clear` leaves them. To test what your mod does next, skip `session.start`, raise `classic.SessionStart` with `source: 'clear'`, and check what your mod draws.

This test checks the module from [Load a saved value again after `/clear`](/docs/en/plugins/mods/interface#load-a-saved-value-again-after-clear). Add it to the file from [Test a drawing](#test-a-drawing), where `PANE` is defined. That file's first test expects the button to save the count, as the button in [Save from more than one session](/docs/en/plugins/mods/interface#save-from-more-than-one-session) does:

```typescript hello-tabs/tests/hello-tabs.test.ts theme={null}
test('the saved count comes back after /clear', async ($, on) => {
  // The store already holds a count of 7
  on('store.get', () => ({ value: 7 }))
  // Answer the event after your hook passes it on with next(e)
  on('classic.SessionStart', () => ({}))

  // Raise the event that fires after /clear, which runs your hook
  await $.classic.SessionStart({ source: 'clear' })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  await ui.press({ key: 'tab-two' })
  // The pane shows the stored count, not the default of 0
  expect(await ui.find({ type: 'Text', text: 'Count: 7' })).toBeDefined()
})
```

The test passes when your `classic.SessionStart` hook has copied the stored `7` into `$.state` before the pane draws. Without that hook in your module, the pane draws `Count: 0`, `find` returns `undefined`, and the test fails at `toBeDefined`.

## Test a mod that judges other mods

A mod your organization lists in [`prependPlugins`](/docs/en/plugins/mods/admin) can refuse another mod before it loads. To test one, set your mod's tier and give the test a second mod for yours to admit or refuse:

* **`tier`**: call it once at the top of the test file, as in `tier('prepend')`, to load your mod as `prepend`, `append`, or `builtin`, its place in the [order mods run in](/docs/en/plugins/mods/events#the-order-mods-run-in). Without it, your mod loads as `user`.
* **`plugins`**: pass `test` an options object ahead of the test body. Its `plugins` array holds mods you write inline, each with a `name` and a `register` function. To load one somewhere other than `user`, add `tier` to it.

This test file loads the [policy mod from the admin page](/docs/en/plugins/mods/admin#enforce-a-policy-with-a-mod-of-your-own) first. It checks that the policy mod refuses a mod that starts a process and admits one that doesn't:

```typescript acme-guard/tests/guard.test.ts theme={null}
import { expect, test, tier } from 'claude-code/testing'

// Load the mod under test ahead of every other mod
tier('prepend')

// A second mod whose code calls $.process.run, which the policy blocks
const runner = {
  name: 'runner',
  register(on) {
    on('tool.call', async ($, e, next) => {
      await $.process.run(['ls'])
      return { result: 'runner answered' }
    })
  },
}

// A second mod that calls nothing the policy blocks
const reader = {
  name: 'reader',
  register(on) {
    on('tool.call', async ($, e, next) => {
      return { result: 'reader answered' }
    })
  },
}

test('refuses a mod that starts a process', { plugins: [runner] }, async ($, on) => {
  on('tool.call', () => ({ result: 'claude code answered' }))
  let message = ''
  try {
    // The first call on $ loads the mods, so the refusal is thrown here
    await $.tool.call({ tool: 'Bash', command: 'ls' })
  } catch (error) {
    message = error.message
  }
  expect(message).toBe('runner: refused by acme-guard: Acme policy: mods may not call process.run')
})

test('admits a mod that starts no process', { plugins: [reader] }, async ($, on) => {
  on('tool.call', () => ({ result: 'claude code answered' }))
  const out = await $.tool.call({ tool: 'Bash', command: 'ls' })
  // The answer comes from reader, which shows that it loaded
  expect(out).toEqual({ result: 'reader answered' })
})
```

In your shell, run `claude plugin test` from the `acme-guard` directory. Both tests pass with the policy mod as the admin page shows it.

The kit loads every mod at the test's first call on `$`. When your mod refuses one, that call throws, and the message names the refused mod, the mod that refused it, and your reason. In the second test nothing is refused, so `reader` answers the tool call before it reaches the stub.

## Next steps

* [Troubleshoot a mod](/docs/en/plugins/mods/troubleshoot): find out why a mod does nothing in a session
* [Mods reference](/docs/en/plugins/mods/reference): every event's input and result, for writing stubs
