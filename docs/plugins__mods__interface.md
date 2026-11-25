> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Draw in the interface with a mod

> Draw panes, a band above the prompt, buttons, and text fields from a Claude Code mod, handle presses and input, and keep state between redraws and sessions.

A mod can draw its own interface in Claude Code and change parts of the interface Claude Code already draws. Each place a mod can draw is called a [render site](https://code.claude.com/docs/en/plugins/mods/reference.md#render-sites), such as a pane, the band above the prompt, or the spinner. Claude Code fires the [`ui.render`](https://code.claude.com/docs/en/plugins/mods/reference#interface) event each time it's about to draw a render site, and your hook for that event returns what to draw there.

This map shows where a mod can draw in a terminal session:

![Map of a Claude Code terminal session in fullscreen rendering. A mod can add a pane as a sidebar on the right, a toast at the top right of the transcript, a log line in the transcript, a band above the prompt, and a status line under the prompt. A mod can redraw messages, tool call rows, and the spinner. The prompt is Claude Code's own.](https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-screen-map.svg?fit=max\&auto=format\&n=dgiVO_Od1X1faduV\&q=85\&s=5fda26b6609c62b68c6f9e528c1590ea)

In a narrower terminal, the pane sits above the prompt instead of beside the transcript.

Build your [first mod](https://code.claude.com/docs/en/plugins/mods/create.md) before you start here. Begin with the worked example, which builds a pane with two tabs and a counter, then read the section for each piece you want to change.

> [!NOTE]
>
> To look up one prop or limit, see the [reference](https://code.claude.com/docs/en/plugins/mods/reference.md#render-sites).

## Build a pane with tabs

In this section you build a mod that adds a `/hello-tabs` command, and the command opens a pane. A pane is a sidebar beside the transcript in a wide fullscreen terminal, or a framed region above the prompt otherwise. This pane shows two tabs, and the second tab has a button that adds one to a counter. The count is still there after you restart Claude Code.

The finished mod looks like this. The recording opens the pane, switches to the second tab, presses the button a few times, and returns to the first tab:

<video autoPlay muted loop playsInline controls src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-hello-tabs-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=49d520094d87b5b44bfe50fa49677f06" aria-label="The /hello-tabs command is typed at the Claude Code prompt and a framed pane opens above it, with '1: One' and '2: Two' across the top and the text 'This is the first tab.' The second tab shows an 'Add one' button beside 'Count: 1', and the count rises to 3. The pane then returns to the first tab." />

The tabs are two buttons in a row. The mod keeps track of which one is active and draws that tab's content under the row.

**1. Create the plugin**

A mod is a plugin with a manifest, a `hooks.json` that points to your code, and the code file. [Create a mod](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself) explains each one. Create a directory named `hello-tabs` with `.claude-plugin` and `hooks` directories inside it, then save the first two files.

Save the manifest as `hello-tabs/.claude-plugin/plugin.json`:

```json hello-tabs/.claude-plugin/plugin.json theme={null}
{
  "name": "hello-tabs",
  "version": "0.1.0",
  "description": "Opens a pane with two tabs and a counter",
  "author": { "name": "Your Name" }
}
```

Name your entry point in `hello-tabs/hooks/hooks.json`:

```json hello-tabs/hooks/hooks.json theme={null}
{
  "modules": ["./register.js"]
}
```

**2. Write the code**

This list says what each hook does, in the order they appear in the code:

* Adds the `/hello-tabs` command, and loads the count an earlier session saved
* Opens the pane when you run that command
* Draws the pane's content: the row of tabs and the open tab's body

Two module-level variables, `tab` and `count`, hold the pane's state.

Save this as `hello-tabs/hooks/register.js`:

```javascript hello-tabs/hooks/register.js theme={null}
// The pane's id, used to open the pane and to recognize it when drawing
const PANE = 'hello-tabs'

// What the pane shows: which tab is open, and the counter's value
let tab = 'one'
let count = 0

export function register(on) {
  // Runs before your first prompt, and again after a reload
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'hello-tabs', description: 'Open the hello-tabs pane' })
    // Load the count an earlier session saved, if there is one
    const saved = await $.store.get('count')
    if (typeof saved === 'number') count = saved
    return next(e)
  })

  // Runs when you type /hello-tabs
  on('command.run', { command: 'hello-tabs' }, async ($) => {
    // Open the pane, give it the keyboard, and let Esc close it
    await $.ui.open({ id: PANE, title: 'Hello tabs', focus: true, closeOnEscape: true })
    // Print nothing in the transcript
    return {}
  })

  // Runs each time Claude Code draws a pane
  on('ui.render', { component: 'Pane' }, async ($, e, next) => {
    // Leave other mods' panes alone
    if (e.requestId !== PANE) return next(e)
    // Get the elements this app can draw
    const { Box, Text, Button } = $.ui.resolve(e)
    // Ask Claude Code to run this hook again
    const redraw = () => $.ui.invalidate('ui.render')

    // One tab: a button that switches to its tab when pressed
    const tabButton = (name, label, hotkey) =>
      Button({
        key: 'tab-' + name,
        label,
        hotkey,
        plain: true,
        // Dim the tab that isn't open
        dimColor: tab !== name,
        onPress: () => {
          tab = name
          redraw()
        },
      })

    // What goes under the tabs, depending on which one is open
    const body =
      tab === 'one'
        ? [Text({ children: ['This is the first tab.'] })]
        : [
            Box({
              flexDirection: 'row',
              columnGap: 2,
              children: [
                Button({
                  key: 'more',
                  label: 'Add one',
                  hotkey: 'a',
                  onPress: async () => {
                    count += 1
                    redraw()
                    // Save the count so it's there after a restart
                    await $.store.set('count', count)
                  },
                }),
                Text({ children: ['Count: ' + count] }),
              ],
            }),
          ]

    // The whole pane: the row of tabs, a blank line, then the body
    return Box({
      flexDirection: 'column',
      children: [
        Box({
          flexDirection: 'row',
          columnGap: 3,
          children: [tabButton('one', 'One', '1'), tabButton('two', 'Two', '2')],
        }),
        Text({ children: [' '] }),
        ...body,
      ],
    })
  })
}
```

Each hook also does something the code doesn't make plain:

* **[`session.start`](https://code.claude.com/docs/en/plugins/mods/reference#session)** also reads the saved count from [`$.store`](#keep-state), a key-value store that persists between sessions.
* **[`command.run`](https://code.claude.com/docs/en/plugins/mods/api#add-a-command)** only tells Claude Code the pane exists. Opening a pane draws nothing by itself: Claude Code then fires `ui.render` to ask what goes in it.
* **`ui.render`** returns the element tree, a `Box` that holds other boxes, text, and buttons, and builds it again from `tab` and `count` each time it runs.

Pressing a button runs its `onPress` callback, which changes a variable and calls `redraw`. Claude Code then runs the `ui.render` hook again, and the hook builds a new tree from the new values. Every interactive drawing uses that render cycle: a callback changes state, and the hook renders again from the new state.

**3. Open the pane**

In your shell, start Claude Code with `claude --plugin-dir ./hello-tabs`. At the Claude Code prompt, run `/hello-tabs`. A pane opens with `1: One` and `2: Two` across the top. Press `2`, then press `a`, the hotkey for **Add one**, a few times. The count rises.

**4. Check that the count was saved**

Press Esc to close the pane, then exit the session. In your shell, start Claude Code again with the same `claude --plugin-dir ./hello-tabs` command, and at the Claude Code prompt run `/hello-tabs`. The count is where you left it.

To clear the count, have the mod call `$.store.delete('count')`. [Keep state](#keep-state) covers how long each kind of value lasts.

## Pick where to draw

To choose the render site a `ui.render` hook draws in, pass a filter, called a [matcher](https://code.claude.com/docs/en/plugins/mods/events.md#filter-which-events-a-hook-handles), as the second argument to `on`. `{ component: 'Pane' }` runs the hook only for panes. In the hook, `e.component` names the site, `e.surface` says which app is drawing, and `e.props` holds the site's own data. For a pane, `e.requestId` is the `id` you opened it with.

The pane and the band are empty until a mod fills them. Select a tab to see what each one is and how to draw in it:

> [tab] Pane
>
> A pane is a sidebar beside the transcript in a wide fullscreen terminal, or a framed region above the prompt otherwise. With several panes open, each gets a tab that shows its title.
>
> A pane appears when your mod calls `$.ui.open` with an `id` you choose, as in `$.ui.open({ id: 'hello-tabs' })`. [Open a pane at the right time](#open-a-pane-at-the-right-time) covers the other fields and when a pane waits for a wider terminal.
>
> To draw in your pane, filter on `{ component: 'Pane' }` and check that `e.requestId` is your `id`.

> [tab] Band above the prompt
>
> The band is a strip directly above the prompt input. Each mod that draws there gets its own row, and the rows stack from the top in the [order mods run in](https://code.claude.com/docs/en/plugins/mods/events.md#the-order-mods-run-in).
>
> To draw your mod's row, filter on `{ component: 'AbovePrompt' }` and return a [tree](#build-a-tree-from-elements). To draw nothing, return `next(e)`.
>
> Before v2.1.323, all mods shared one drawing in the band, and your tree replaced what the mods after yours drew. To support those releases too, put the result of `await next(e)` among the children of a [`Box` that stays valid](https://code.claude.com/docs/en/plugins/mods/troubleshoot#another-mods-band-shows-and-yours-doesnt). On v2.1.323 or later, that child doesn't draw other mods' rows.

A mod can also [place a row of its own in the transcript](#place-a-row-in-the-transcript).

### Change what Claude Code already draws

To change a part Claude Code draws, filter your `ui.render` hook on a render site from this table:

| Site | What it is |
| :- | :- |
| `UserMessage`, `AssistantMessage` | A message in the transcript |
| `ToolUse`, `ToolResult`, `ToolGroup` | A tool call's row, its result, and a collapsed group of calls |
| `CommandOutput` | The row a command printed |
| `AskUserQuestion` | The dialog Claude opens to ask you a question. A `ui.render` hook can't replace it. |
| `Spinner`, `ToolProgress`, `TurnDuration` | Status lines for a turn: the line that animates while Claude works, a running tool's live progress line, and the line that closes a turn |
| `InfoNotice`, `SessionMode`, `PromptHint` | Status lines under the logo, the mode labels in the footer, and the hint line under the prompt |
| `AgentRow` | A subagent's or teammate's row in the agent panel |

`Pane`, `AbovePrompt`, `AskUserQuestion`, `Spinner`, `UserMessage`, `AssistantMessage`, and the tool call sites work in the terminal, the Desktop app, and the VS Code extension. The [render sites table](https://code.claude.com/docs/en/plugins/mods/reference.md#render-sites) lists where each of the others is raised. To change the bubbles and font of messages in the Desktop app without a `ui.render` hook, [style the messages with a theme](#style-messages-in-the-desktop-app).

Select a tab to see a hook change a spinner detail, replace the spinner, or leave it alone. The examples read a `calls` variable that another hook counts, as in the [tutorial mod](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself).

> [tab] Change a detail
>
> To keep Claude Code's drawing and change one part of it, pass `next` a copy of the event with changed `props`. This hook changes the text after the spinner's word:
>
> ```javascript theme={null}
> on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
>   // Keep Claude Code's spinner, and change the text after its word
>   return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
> })
> ```
>
> The spinner keeps its animation and its word, and your text follows the word:
>
> ```text theme={null}
> Thinking · tool calls: 2…
> ```

> [tab] Replace the drawing
>
> To draw something of your own in the site's place, return a tree and don't call `next`. This hook draws one line of text where the spinner would be:
>
> ```javascript theme={null}
> on('ui.render', { component: 'Spinner' }, async ($, e) => {
>   const { Text } = $.ui.resolve(e)
>   // No call to next, so this line is drawn in the spinner's place
>   return Text({ children: ['Claude has made ' + calls + ' tool calls'] })
> })
> ```
>
> While Claude works, your line shows and Claude Code's spinner doesn't:
>
> ```text theme={null}
> Claude has made 2 tool calls
> ```

> [tab] Leave it alone
>
> To leave the site as Claude Code draws it, return `next(e)`. A hook often does that for some events and not others. This hook leaves the spinner alone until there's a call to count:
>
> ```javascript theme={null}
> on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
>   // Nothing to show yet, so pass the event on unchanged
>   if (calls === 0) return next(e)
>   return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
> })
> ```
>
> Before the first tool call, the spinner looks the way it does without the mod:
>
> ```text theme={null}
> Thinking…
> ```

At these sites, `next(e)` returns a reference to Claude Code's drawing, `{ type: 'engine', ref }`, unless a mod that runs after yours returned a tree of its own. To change what's in that drawing, pass `next` a copy of the event with different props, as the **Change a detail** tab does. You can return the reference as it is, or place it in a `Box` beside elements of your own:

```javascript theme={null}
on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
  const { Box, Text } = $.ui.resolve(e)
  const theirs = await next(e)
  return Box({ flexDirection: 'column', children: [theirs, Text({ children: ['under the spinner'] })] })
})
```

While Claude works, the spinner animates as before, and `under the spinner` appears below it.

The permission prompt isn't a render site, so a mod can't change what it shows. The question dialog, `AskUserQuestion`, is one, so a mod can change that dialog when Claude asks a question. A tree for the dialog has to hold the reference exactly once, with your elements above it. Otherwise, Claude Code draws its own dialog.

### Open a pane at the right time

A pane appears only when your mod opens it. How and when you open it decides whether it takes keyboard focus, how much room it asks for, and whether it shows at all in a narrow terminal.

To open a pane, call [`$.ui.open`](https://code.claude.com/docs/en/plugins/mods/reference#mods-api-methods) with an `id` you choose. The `id` is the pane's name: your `ui.render` hook checks for it, and you pass it again to close the pane. If another mod has a pane open with that `id`, the call rejects.

```javascript theme={null}
await $.ui.open({ id: 'hello-tabs', title: 'Hello tabs', focus: true })
```

To close the pane, call `$.ui.close` with the `id` you opened it with:

```javascript theme={null}
await $.ui.close({ id: 'hello-tabs' })
```

Besides `id`, `$.ui.open` takes these optional fields:

| Field | What it does |
| :- | :- |
| `title` | The pane's tab label when more than one pane is open |
| `focus` | Requests [keyboard focus](#know-which-keys-your-mod-can-receive) |
| `closeOnEscape` | Makes Esc close the pane |
| `holdToasts` | In the terminal, holds toasts while this pane is the one showing. See [Hold toasts behind a dialog](#hold-toasts-behind-a-dialog). |
| `rows` | The height to ask for when the pane sits above the prompt. The default is a third of the space. |
| `columns` | The width to ask for when the pane sits beside the transcript, at most 45% of the terminal's width. Once the user has resized a pane beside the transcript, in this session or an earlier one, panes open there at the width they set instead. The same 45% limit applies to that width. |

The [VS Code extension](#draw-in-the-vs-code-extension) ignores `rows` and `columns` and sizes the pane itself.

`focus`, `closeOnEscape`, and `holdToasts` are optional and accept only `true`. To leave one off, omit it. Passing `false` throws an error such as `ui.open: focus is true or left out`. To set one of them conditionally, add the field only when the condition holds. This call asks for keyboard focus only when `items` isn't empty:

```javascript theme={null}
const pane = { id: 'hello-tabs', title: 'Hello tabs' }
await $.ui.open(items.length > 0 ? { ...pane, focus: true } : pane)
```

To let a command open the pane while Claude is working, add `immediate: true` when you [register the command](https://code.claude.com/docs/en/plugins/mods/api.md#add-a-command). Without it, a command typed during a turn waits for the turn to end.

#### Hold toasts behind a dialog

Pass `holdToasts: true` to `$.ui.open` when the pane is a dialog the user answers and leaves, so toasts don't appear while they decide. In the terminal, the hold lasts while that pane is the one showing, and a toast raised in that time waits until the hold ends.

Claude Code holds other mods' toasts and its own short-lived notifications as well as the ones your mod raises with [`$.ui.toast`](https://code.claude.com/docs/en/plugins/mods/api#show-something-without-starting-a-turn). Leave the field off a pane that stays open, so the user keeps seeing them.

#### When a pane waits for a wider terminal

A pane your mod opens without being asked doesn't appear in a narrow terminal, so it can't take over a small screen. Whether it appears depends on what opened it:

* **Opened by something the user did**, such as a command they ran or a button they pressed, the pane appears at any width
* **Opened by your mod acting by itself**, such as from a timer or a [`turn.start`](https://code.claude.com/docs/en/plugins/mods/events#follow-a-turn) hook, the pane appears only in a terminal at least 144 columns wide. After the user has opened that pane once themselves, 110 columns is enough.

When the pane appears, `$.ui.open` resolves to `{ isPlaced: true }`. When the pane is waiting, `isPlaced` is `false` and `reason` is a string that says why. A waiting pane appears when the user opens it or widens the terminal. To say something is available without opening a pane, call `$.ui.toast('Your message')`, which shows a toast notification.

### Draw in the VS Code extension

In the VS Code extension, what a mod draws appears in the chat panel with extension version 2.1.299 or later. A session that [doesn't fetch feature flags](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching), such as one on Amazon Bedrock, needs 2.1.304 or later. In a `ui.render` hook for the panel, `e.surface` is `vscode`. To check which sites and elements the panel draws, and which props it ignores, see the [render sites](https://code.claude.com/docs/en/plugins/mods/reference.md#render-sites) and [elements](https://code.claude.com/docs/en/plugins/mods/reference.md#elements) tables.

To make a mod work in the panel as well as the terminal, account for these differences:

* **Panes**: in a panel 800 pixels or wider, panes dock beside the conversation, `e.props.placement` is `'dock'`, and `e.viewport.isFullscreen` is `true`. In a narrower panel, panes draw above the prompt box, `placement` is `'inline'`, and a pane shows 12 rows before it scrolls.
* **Toasts and status lines**: these sit in one stack directly above the prompt box, together with the panes when the panel is narrow, with one status line per mod. The stack is hidden while a permission request or a dialog shows.
* **Labels**: the panel frames what a mod draws or rewrites and labels it with the plugin's name, as in **From the token-chart plugin** or **Edited by the token-chart plugin**.
* **Keyboard**: buttons have no hotkeys, so the user clicks a button or presses Enter on it once it has focus.
* **Keyboard focus**: the panel grants a pane's `focus: true` request only when the panel has focus, Claude is idle with no question waiting, and the prompt box is empty.
* **The question dialog**: at `AskUserQuestion`, the panel keeps its own question card and draws your elements above it. Props you pass to `next` don't change the card.
* **Prompt suggestions**: `$.prompt.suggest` resolves with `isShown: false` and shows nothing, because the panel keeps the prompt box's dim suggestion text for Claude's own suggestions.
* **Text limits**: the panel cuts a status line at 200 characters or two rows, and a toast at 500 characters.

### Place a row in the transcript

A row is a line your mod adds to the transcript in the terminal, after the latest message. It stays at that spot as the conversation goes on, and Claude doesn't see it. `$.ui.place` requires Claude Code v2.1.314 or later.

**1. Place the row**

Call [`$.ui.place`](https://code.claude.com/docs/en/plugins/mods/reference#mods-api-methods) with an `id`. The `id` is a name you make up for the row, such as `build-status`. It can be 1 to 64 letters, digits, `_`, or `-`, and each row your mod has in the transcript needs its own.

**2. Draw the row**

Draw the row at the [`Placed`](https://code.claude.com/docs/en/plugins/mods/reference#render-sites) render site.

This example adds a `/build-status` command. When the user runs the command, the mod adds a row that shows `Build: passing`. The text is fixed to keep the example short, so a real mod would draw its own result:

```javascript theme={null}
export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'build-status', description: 'Show the build status' })
    return next(e)
  })

  on('command.run', { command: 'build-status' }, async ($) => {
    const placed = await $.ui.place({ id: 'build-status' })
    // Where nothing draws the row, reply with text instead
    return placed.isPlaced ? {} : { text: 'Build: passing' }
  })

  on('ui.render', { component: 'Placed' }, async ($, e, next) => {
    // This hook runs for every mod's rows, and another mod can use the same id
    if (e.props.plugin !== $.plugin.name || e.props.id !== 'build-status') return next(e)
    const { Text } = $.ui.resolve(e)
    return Text({ children: ['Build: passing'] })
  })
}
```

To try the example, put this code in a [mod](https://code.claude.com/docs/en/plugins/mods/create.md). In a terminal session, run `/build-status` at the Claude Code prompt. `Build: passing` appears as a row at the end of the transcript.

The call doesn't always show a row, and a row can go away later, so handle these cases in your mod:

* **The result**: `{ isPlaced: true, requestId }` when the terminal draws the row. Otherwise `isPlaced` is `false` and `reason` says why, as in `no attached surface draws placed rows yet`. One reason is the [limit on rows](https://code.claude.com/docs/en/plugins/mods/reference.md#limits) a mod can have at one time.
* **A second call with the same `id`**: while the first row is still in the transcript, the call adds no row and resolves with that row's `requestId`. To change what the row shows, [redraw the row](#redraw-when-something-changes).
* **When the row goes away**: when the conversation ends, when the user rewinds past the row, or, outside [fullscreen rendering](https://code.claude.com/docs/en/fullscreen.md), when the conversation is compacted. `--resume` doesn't bring the row back. To show the row again, call `$.ui.place` again.

### Put a backdrop behind the conversation

> [!NOTE]
>
> `$.theme.set` and `$.theme.clear` replace `$.ui.backdrop`, which Claude Code v2.1.319 removed. Change `$.ui.backdrop({ id: 'your-backdrop' })` to a `$.theme.set` call like the one in this section's example, and `$.ui.backdrop(undefined)` to `$.theme.clear()`, which removes any mod's backdrop.

To put a backdrop behind the conversation in the Desktop app or the mobile app, call [`$.theme.set`](https://code.claude.com/docs/en/plugins/mods/reference#mods-api-methods) with a `backdrop`, then draw the backdrop at the [`Backdrop`](https://code.claude.com/docs/en/plugins/mods/reference#render-sites) render site. To take the backdrop off, call `$.theme.clear()`. The terminal draws no backdrop. `$.theme.set` and `$.theme.clear` require Claude Code v2.1.319 or later.

This example requires Claude Code v2.1.323 or later, so [check your version](https://code.claude.com/docs/en/plugins/mods/overview.md#turn-mods-on-or-off) first. The mod sets a backdrop when the session starts, draws the backdrop, and adds a `/plain` command that takes the backdrop off:

```javascript theme={null}
export function register(on) {
  // Neither a reload of this mod nor --resume keeps the backdrop, so set it here
  on('session.start', async ($, e, next) => {
    await $.theme.set({ backdrop: { scene: 'night-sky' }, overrideColorScheme: 'dark' })
    await $.command.register({ name: 'plain', description: 'Take the backdrop off' })
    return next(e)
  })

  on('ui.render', { component: 'Backdrop' }, async ($, e, next) => {
    // This hook runs for every mod's backdrop, and another mod can use the same scene
    if (e.props.plugin !== $.plugin.name || e.props.scene !== 'night-sky') return next(e)
    const { Box, Text } = $.ui.resolve(e)
    return Box({ backgroundColor: 'blue', children: [Text({ children: ['Night sky'] })] })
  })

  on('command.run', { command: 'plain' }, async ($) => {
    const cleared = await $.theme.clear()
    return { text: cleared.reason }
  })
}
```

> [!NOTE]
>
> Before v2.1.323, write `id` in place of `scene` in the `$.theme.set` call and in `e.props`, and move `overrideColorScheme` into `backdrop` as `colorScheme`.

To try the example, put this code in a [mod](https://code.claude.com/docs/en/plugins/mods/create.md) and start a session in the Desktop app or the mobile app. To take the backdrop off, run `/plain` at the Claude Code prompt. The transcript shows `the theme is cleared` after the mod's name, as in `night-sky: the theme is cleared` for a mod named `night-sky`.

Check what `backdrop` takes, what the call's result tells you, and what other mods can change:

* **The `backdrop` fields**: `scene` is a [name](https://code.claude.com/docs/en/plugins/mods/reference.md#limits) you choose for a backdrop your hook draws. For the other fields and `overrideColorScheme`, see [the types for your build](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build).
* **Whether the backdrop is drawn**: `$.theme.set` resolves with `isDrawn: true` when a Desktop or mobile app connected to the session says it draws backdrops. Otherwise `isDrawn` is `false` and `reason` says why.
* **One theme for each session**: a mod that calls `$.theme.set` replaces the session's backdrop, [colors](#change-the-colors-of-the-desktop-app), [message style](#style-messages-in-the-desktop-app), and [sound](#add-sound-to-a-theme), and a mod that calls `$.theme.clear()` removes them, whichever mod set them. Call `$.theme.clear()` only when the user asks for it.

### Animate a backdrop with a shader

To make a [backdrop](#put-a-backdrop-behind-the-conversation) that moves and follows the user's pointer in the Desktop app's Code tab, wrap an `Svg` in a [`Shader`](https://code.claude.com/docs/en/plugins/mods/reference#elements) element. The element names a shader file, which is code that computes each pixel's color on the GPU. The app draws the result over the `Svg`. `Shader` requires Claude Code v2.1.326 or later in the Code tab, so [check the version there](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab) first.

These steps create a mod named `glow`. It draws a light under the pointer, and a click on the backdrop changes the color of the light.

**1. Save the manifest and hooks.json**

From [Write a mod yourself](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself), save `.claude-plugin/plugin.json` and `hooks/hooks.json` in `~/.claude/skills/glow/`, and change `first-mod` to `glow` in both files. A mod [under `~/.claude/skills/`](https://code.claude.com/docs/en/plugins/create#scaffold-a-plugin-that-loads-every-session) loads when you start a session.

**2. Write the shader**

Save this file as `~/.claude/skills/glow/hooks/glow.ts`. Claude Code provides the `claude-code/shader` module it imports.

The shader draws a light around the pointer, blue when `warm` is `0` and orange when it's `1`:

```typescript glow/hooks/glow.ts theme={null}
import {
  length, max, min, mix, picture, pointers, shader, smoothstep, values, vec2, vec3, vec4,
} from 'claude-code/shader'

// Declare each number the mod sets through the Shader's values, with its range
const { warm } = values({ warm: [0, 1] })

// This function runs once for every pixel and returns that pixel's color
const glow = picture(pixel => {
  let light = 0
  // The loop sees the mouse, each finger, and for one second each pointer that lifted
  // A mouse that rests for half a second counts as lifted
  for (const pointer of pointers) {
    // Subtracting two positions subtracts their x and their y, in points
    // The result is typed as a plain number, so vec2() marks it as a position again
    const near = smoothstep(200, 0, length(vec2(pixel.point - pointer.at)))
    // A pointer fades in over a quarter second, then out as gone counts from 0 to 1
    const fade = min(pointer.age * 4, 1) * (1 - pointer.gone)
    light = max(light, near * near * fade)
  }
  const color = mix(vec3(0.25, 0.55, 1), vec3(1, 0.45, 0), warm)
  const alpha = 0.7 * light
  // The color is premultiplied: red, green and blue are multiplied by alpha
  return vec4(color * alpha, alpha)
})

// A shader runs its passes in order, and this one has a single pass
export default shader({ passes: [glow] })
```

**3. Draw the backdrop**

Save this file as `~/.claude/skills/glow/hooks/register.js`. The mod sets the theme when a session starts, and draws a `Shader` with one `Svg` child.

The mod's [`ui.pointer`](https://code.claude.com/docs/en/plugins/mods/reference#interface) hook runs after a click, flips `warm`, and asks for a redraw:

```javascript glow/hooks/register.js theme={null}
const STILL =
  '<svg xmlns="http://www.w3.org/2000/svg"' +
  ' viewBox="0 0 1 1" preserveAspectRatio="none">' +
  '<rect width="1" height="1" fill="#1a3a9c"/>' +
  '</svg>'

let warm = 0

export function register(on) {
  on('session.start', async ($, e, next) => {
    // The scene is a name you choose for the backdrop your hook draws
    await $.theme.set({ backdrop: { scene: 'glow' }, overrideColorScheme: 'dark' })
    return next(e)
  })

  on('ui.render', { component: 'Backdrop' }, async ($, e, next) => {
    // This hook runs for every mod's backdrop, so pass on the others
    if (e.props.plugin !== $.plugin.name || e.props.scene !== 'glow') return next(e)
    const { Shader, Svg } = $.ui.resolve(e)
    // module must be a string literal, relative to this file
    return Shader({
      module: './glow.ts',
      values: { warm },
      children: [Svg({ source: STILL, alt: 'A dark blue background' })],
    })
  })

  on('ui.pointer', async ($, e, next) => {
    warm = 1 - warm
    $.ui.invalidate('ui.render')
    return next(e)
  })
}
```

**4. Check the shader**

This step is optional and needs [the CLI](https://code.claude.com/docs/en/quickstart.md), which has its own version number. Go to `~/.claude/skills/` in your shell, run `claude plugin validate ./glow`, and look for `shader hooks/glow.ts: runs on any GPU` in the output. If the output names a line in `glow.ts` as an error, fix that line.

A CLI older than v2.1.326 reports `"ui.pointer" is not an event`. If yours does, [update it](https://code.claude.com/docs/en/setup.md#update-claude-code) and run the command again.

**5. Try the backdrop**

Start a new local session in the Code tab by sending a message. The background turns dark blue. If it doesn't, turn off any other mod that sets a theme and start a new session, because a session has [one theme](#put-a-backdrop-behind-the-conversation). If the background still doesn't change, [find out why the mod does nothing](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing).

Move the pointer. A blue light follows it, and fades when you stop. If no light appears, see [Fix a backdrop that shows only the `Svg`](#fix-a-backdrop-that-shows-only-the-svg). Click the empty space beside the conversation, then move the pointer again. The light is now orange. If it's still blue, answer any permission prompt or question from Claude, then click again quickly without dragging, away from messages and buttons.

To try a change, save `glow.ts` or `register.js`, and the mod reloads in the running session. If the change doesn't show within a few seconds, send a message to load it. To turn the mod off, move `glow` out of `~/.claude/skills/` and start a new session.

Follow these rules for pointer input, the shader, and the `Svg` when you build on the example:

* **Clicks**: your mod gets `ui.pointer` when it has set the theme and the user clicks a part of the backdrop that the app doesn't cover. The app sends two clicks a second at most and drops the rest. To draw a press effect without changing your mod's state, use `pointer.down * (1 - pointer.gone)` in the shader, which is `1` during a press and then fades.
* **Click position**: `e.x` and `e.y` run from `0` to `1`, starting at the backdrop's top left. In the shader, `pixel.uv` has the same scale and starts at the bottom left. To draw at the click, send `e.x` and `1 - e.y` through `values`.
* **Movement**: read pointer movement from `pointers` in the shader, because moving the pointer doesn't fire `ui.pointer`. For motion over time, import `time`, the seconds since the shader started.
* **Presses**: to time an effect from a press, check every pointer in the loop for `down` at `1` and read its `age`, the seconds since the press. A press arrives as a new pointer, so it isn't always first in `pointers`.
* **`values`**: declare up to eight numbers in the shader file, and set them with the `values` prop. When your mod's state changes, call `$.ui.invalidate('ui.render')` to send the new numbers.
* **The shader file**: write a subset of TypeScript without `while` loops, recursion, or imports from other files. For the full rules and the functions you can call, [get the type definitions with the CLI](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build) and search them for `claude-code/shader`.
* **The `Svg`**: draw it as a finished picture, because users see it alone when the shader can't run.

#### Fix a backdrop that shows only the `Svg`

Check reduced motion first, because it keeps any shader from running, then these other causes:

* **Reduced motion is on**: if you don't need reduced motion, turn it off in your system settings and set **Motion** to **System** in the Desktop app's **Settings > General**.
* **The shader file breaks a rule**: in your shell, run `claude plugin validate` on the mod's directory and fix the line the output names.
* **The shader is too heavy for the GPU**: if `claude plugin validate` prints `needs a fast GPU`, simplify the shader until the output says `runs on any GPU`. Start with the lines the output ranks as costing the most.
* **The `Svg` holds content that blocks shaders**: replace the `Svg` source with `STILL` from the [`glow` example](#animate-a-backdrop-with-a-shader). If the shader then runs, restore your source without the content that blocks it, such as a lighting filter or `feTile`.
* **A shader from any mod ran and then stopped**: after the app stops a shader for flashing or running too slowly, it starts no shader for up to five minutes. Keep large changes in brightness or color under three a second, or simplify a slow shader. Then wait five minutes and start a new session.

### Change the colors of the Desktop app

To change the colors of the Desktop app's Code tab with a mod, [ask Claude for one](#ask-claude-for-a-colors-mod) or [write one yourself](#write-a-colors-mod-yourself). Both ways require Claude Code v2.1.324 or later in the Code tab, so [check the version there](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab) first. Claude Code in the terminal keeps its own colors.

#### Ask Claude for a colors mod

**1. Describe the colors**

Start a local session in the Code tab and tell Claude which colors you want. For example, enter `make a mod that makes the app cream in light mode and dark brown in dark mode`. Claude writes the mod's files.

**2. Approve the mod**

Answer the questions Claude Code asks about the mod's files and hot reloading. For what each answer does, see [Ask Claude for a mod](https://code.claude.com/docs/en/plugins/mods/create.md#ask-claude-for-a-mod).

**3. Check the colors**

The Code tab changes color when the mod loads. To adjust a color, tell Claude what to change. If nothing changes, see [Fix missing mod colors](#fix-missing-mod-colors-in-the-desktop-app).

#### Write a colors mod yourself

`makeColors` is a function that builds a theme from a few hex colors. These steps create a mod named `paper` that uses it.

**1. Have Claude copy makeColors**

Start a local session in the Code tab, and enter `copy make-colors.js and make-colors.d.ts from your plugin-authoring skill into ~/.claude/skills/paper/hooks/`. Check that both files are in that directory.

**2. Save the manifest and hooks.json**

From [Write a mod yourself](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself), save `.claude-plugin/plugin.json` and `hooks/hooks.json` in `~/.claude/skills/paper/`, and change `first-mod` to `paper` in both files. A mod [under `~/.claude/skills/`](https://code.claude.com/docs/en/plugins/create#scaffold-a-plugin-that-loads-every-session) loads when you start a session.

**3. Write the code**

Save this file as `~/.claude/skills/paper/hooks/register.js`. When a session starts, the code calls `$.theme.set` with the colors for light mode and dark mode:

```javascript theme={null}
import { makeColors } from './make-colors.js'

const { theme } = makeColors({
  label: 'Paper',
  // surface-0 is the background, text-primary is the main text, and text-muted is the faint text
  light: {
    gray: { anchors: { 'surface-0': '#efe6d3', 'text-primary': '#2a241d', 'text-muted': '#6a5f50' } },
  },
  dark: {
    gray: { anchors: { 'surface-0': '#1f1a15', 'text-primary': '#f0e7d7', 'text-muted': '#aca08d' } },
  },
})

export function register(on) {
  on('session.start', async ($, e, next) => {
    await $.theme.set({ colors: theme })
    return next(e)
  })
}
```

To use your own colors, replace the hex values with other six-digit hex colors.

**4. Check the colors**

Start a new local session in the Code tab. With the example's values, the background is cream in light mode and dark brown in dark mode. If nothing changes, see [Fix missing mod colors](#fix-missing-mod-colors-in-the-desktop-app).

### Fix missing mod colors in the Desktop app

If you use a [third-party provider](https://code.claude.com/docs/en/third-party-integrations.md) instead of a Claude account in [Claude Desktop v5.11492.5 or earlier](https://code.claude.com/docs/en/desktop.md#check-your-version), the Code tab keeps its own colors, so skip these checks. Otherwise, if a mod's colors don't appear in the Code tab, or if they disappear, check for these causes:

* **Old version**: [update the Desktop app](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab), restart it, and start a new local session in the Code tab. If Claude wrote the mod, ask for it again there.
* **Mod not loaded**: if Claude wrote the mod, see when it loads in [Ask Claude for a mod](https://code.claude.com/docs/en/plugins/mods/create.md#ask-claude-for-a-mod). If you wrote it, compare your files and their paths with [Write a colors mod yourself](#write-a-colors-mod-yourself).
* **Refused theme**: ask Claude to run the mod's [`makeColors`](#write-a-colors-mod-yourself) call. If the call throws an error, or its `problems` list has an entry that starts `Desktop won't paint this theme`, have Claude fix the theme. If you installed the mod, send what Claude finds to its author.
* **Another `$.theme` call**: when any mod in the session calls `$.theme.set` or `$.theme.clear()`, the colors, [backdrop](#put-a-backdrop-behind-the-conversation), [message style](#style-messages-in-the-desktop-app), and [sound](#add-sound-to-a-theme) from an earlier call disappear. In your own mod, pass every part of the theme in the same `$.theme.set` call. Use one mod at a time that sets a theme.

### Remove mod colors from the Desktop app

To take a mod's colors off the Code tab, turn off the mod first. A mod that's still on can set its colors again.

**1. Turn off the mod**

* **Claude wrote the mod**: move its directory out of the [mods folder](https://code.claude.com/docs/en/plugins/mods/create.md#ask-claude-for-a-mod) of the session where Claude wrote it.
* **You put the mod under `~/.claude/skills/`**: move its directory, such as `~/.claude/skills/paper/`, to a place outside `~/.claude/skills/`.
* **You installed the mod**: in the Desktop app, [disable or uninstall its plugin](https://code.claude.com/docs/en/desktop.md#install-plugins) from **Manage plugins**. If you don't see **Manage plugins** and you have [the CLI](https://code.claude.com/docs/en/quickstart.md), you can [disable or uninstall a marketplace plugin from your shell](https://code.claude.com/docs/en/plugins/install.md#manage-plugins-from-your-shell).

**2. Start a new session**

Start a new local session in the Code tab.

**3. Remove colors that stay**

If the colors are still there, open **Settings** from the Code tab, and search there for `code appearance`. Open the result, and select **Remove colors**.

### Style messages in the Desktop app

To give messages in the Desktop app's Code tab their own bubbles, font, and text size, write a mod that calls `$.theme.set` with a `style` object. This requires Claude Code v2.1.329 or later in the Code tab, so [check the version there](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab) first. The terminal, the VS Code extension, and the mobile app show messages without the style.

This mod sets a serif font for messages and puts each message in a rounded bubble. If `$.theme.set` rejects the style, the mod writes the error to the transcript:

```javascript theme={null}
const style = {
  Text: { fontFamily: ['serif'], fontSize: 15, lineHeight: 22 },
  // The corners run top left, top right, bottom right, bottom left
  UserMessage: { backgroundColor: '#1d5fd1', color: '#ffffff', radius: [18, 18, 4, 18], padding: 12 },
  AssistantMessage: { backgroundColor: '#e9e9ec', color: '#1c1c1f', radius: [18, 18, 18, 4], padding: 12 },
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    try {
      await $.theme.set({ style })
    } catch (error) {
      $.ui.log(error.message)
    }
    return next(e)
  })
}
```

To try the example:

**1. Save the mod**

Save the code as `~/.claude/skills/bubbles/hooks/register.js`. From [Write a mod yourself](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself), save `.claude-plugin/plugin.json` and `hooks/hooks.json` in `~/.claude/skills/bubbles/`, and change `first-mod` to `bubbles` in both files.

**2. Turn off other theme mods**

[Turn off any other mod](#remove-mod-colors-from-the-desktop-app) that calls `$.theme.set`, because each call replaces the whole theme. To use a style and colors together, see [Combine a style with colors or a backdrop](#combine-a-style-with-colors-or-a-backdrop).

**3. Check the style**

Start a new local session in the Code tab and send a message. Your message appears in a blue bubble and Claude's reply in a light gray one, both in a serif font. If nothing changes, see [Fix a missing message style](#fix-a-missing-message-style-in-the-desktop-app).

To take the style off, move `~/.claude/skills/bubbles/` out of `~/.claude/skills/` and start a new session.

#### Combine a style with colors or a backdrop

To use a message style with [colors](#write-a-colors-mod-yourself) or a [backdrop](#put-a-backdrop-behind-the-conversation), pass them all in one call from one mod, as in `$.theme.set({ colors: theme, style })`. Claude Code versions before v2.1.329 reject a call that includes `style` or [`sound`](#add-sound-to-a-theme). To keep your colors and backdrop on those versions, catch the error, log it, and repeat the call without `style` and `sound`.

#### Choose which parts of the conversation to style

Each key in the `style` object you pass to `$.theme.set` names a part of the conversation.

| Key | What it styles | What you can set |
| :- | :- | :- |
| `Text` | The words of your messages and Claude's replies, where `UserMessage` or `AssistantMessage` doesn't set the same property | Text properties |
| `Heading` | Headings in Claude's replies, which otherwise use the reply's font | Text properties |
| `UserMessage` | Your messages | Text properties, box properties, and `rotate` |
| `AssistantMessage` | Each block of text in Claude's replies | Text properties, box properties, and `rotate` |
| `ToolUse` | A tool call's row | `color`, `fontFamily`, and box properties |

Other parts keep the app's look, such as permission prompts, the questions Claude asks in a dialog, code blocks, and the prompt box.

Write sizes as numbers of points, such as `lineHeight: 22`. For the format and range of every value, see `ThemeStyle` in [the types for your build](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build).

* **Text properties**: `color`, `fontFamily`, `fontSize`, `fontWeight`, `italic`, `letterSpacing`, and `lineHeight`. Write `fontFamily` as a one-item list, such as `['serif']`. The item must be `sans`, `serif`, `mono`, `cursive`, or `code`, and `$.theme.set` rejects any other value. Use `code` for the app's code font.
* **Box properties**: `backgroundColor`, `radius`, `borderColor`, `borderWidth`, `shadow`, `fill`, and padding such as `padding` or `paddingTop`. Write a shadow as `{ x: 0, y: 2, blur: 8, color: 'rgba(0, 0, 0, 0.15)' }`. Use `fill` to draw a gradient or a vector drawing behind the text, as in `{ gradient: { stops: ['#dbe8ff', '#c4d6f5'] } }`.
* **`rotate`**: the number of degrees to tilt a message, from `-3` to `3`

To vary the bubbles, set `UserMessage` or `AssistantMessage` to a list of up to four objects. Each message gets one of the objects, in no set order, and keeps it.

#### Set message colors for light mode and dark mode

To give messages different colors in light mode and dark mode, add these message colors to `inputs.light` and `inputs.dark` in the theme that [`makeColors`](#write-a-colors-mod-yourself) returns:

* **Your messages**: `bg-user-message` for the bubble and `text-user-message` for the text
* **Claude's replies**: `bg-assistant-message` for the bubble and `text-assistant-message` for the text

Before you add them to a mod that passes `style`, remove `color` and `backgroundColor` from the matching `UserMessage` or `AssistantMessage`, because those properties take precedence over message colors.

This example colors your messages in the `paper` mod from [Write a colors mod yourself](#write-a-colors-mod-yourself). In that mod's `register.js`, add these lines between the `makeColors` call and the `register` function:

```javascript theme={null}
Object.assign(theme.inputs.light, { 'bg-user-message': '#d9c4a0', 'text-user-message': '#2a241d' })
Object.assign(theme.inputs.dark, { 'bg-user-message': '#4a3a2b', 'text-user-message': '#f0e7d7' })
```

Put `paper` under `~/.claude/skills/`, and move other theme mods, such as `bubbles`, out of that directory. Start a new local session and send a message. Your bubble is tan in light mode and brown in dark mode. If it isn't, see [Fix missing mod colors](#fix-missing-mod-colors-in-the-desktop-app) and [Fix a missing message style](#fix-a-missing-message-style-in-the-desktop-app).

#### Fix a missing message style in the Desktop app

If all or part of a message style doesn't appear in the Code tab, check for these causes:

* **Mod not loaded**: [find out why the mod does nothing](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing)
* **Rejected call**: catch the error from `$.theme.set` and write it to the transcript, as the [example](#style-messages-in-the-desktop-app) does. If the error includes `theme.set does not know the attribute "style"`, [update Claude Code](https://code.claude.com/docs/en/plugins/mods/overview.md#turn-mods-on-or-off) in the app that shows the error. If it names a property, as in `style.Text.fontSize is a number of points, 11 to 28`, change that property's value.
* **Another `$.theme` call**: if any mod in the session calls `$.theme.clear()`, or calls `$.theme.set` without your `style`, the style disappears. In your own mod, [pass the whole theme in one call](#combine-a-style-with-colors-or-a-backdrop). Turn off any other mod that sets a theme.
* **Low contrast**: when text has less than 3:1 contrast with its background, that message, heading, or tool row shows in the app's own colors. `$.theme.set` reports no error. Pick colors that are further apart, and check both light mode and dark mode.
* **Backdrop**: over a [backdrop](#put-a-backdrop-behind-the-conversation), a text color shows only on a background that's solid or nearly solid. Set a solid `backgroundColor` on `UserMessage`, `AssistantMessage`, and `ToolUse` wherever you color their text, including through `Text` or `Heading`.
* **Accessibility settings**: with higher contrast turned on in the app or the operating system, messages show without the style. With an accessibility font such as OpenDyslexic, messages keep that font. To see the whole style, turn these settings off.
* **Open prompt**: a new style waits while a permission prompt or a question from Claude is on screen. Answer it to see the style.

### Add sound to a theme

To give your theme background sound and short sounds for events in the Desktop app's Code tab, pass `sound` to [`$.theme.set`](https://code.claude.com/docs/en/plugins/mods/reference#mods-api-methods). `sound` requires Claude Code v2.1.329 or later in the Code tab, so [check the version there](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab) first. The terminal, the VS Code extension, and the mobile app play no theme sound.

You describe each sound as layers of tones and noise, with no audio file, and the Desktop app makes the audio.

This mod sets dark mode, plays soft noise in the background, and plays three bell notes when Claude finishes a turn:

```javascript theme={null}
// The rest of the theme, which still works without sound
const look = { overrideColorScheme: 'dark' }

const sound = {
  ambience: {
    // A layer with drone: true plays without a break
    // A layer with scatter plays now and then
    // gain is how loud a layer is, from 0 to 1
    layers: [{ wave: 'brown', drone: true, gain: 0.2 }],
  },
  cues: {
    done: {
      // step is the seconds from one note to the next
      layers: [{ wave: 'bell', notes: ['C5', 'E5', 'G5'], step: 0.15, gain: 0.3 }],
    },
  },
}

export function register(on) {
  on('session.start', async ($, e, next) => {
    try {
      await $.theme.set({ ...look, sound })
    } catch (error) {
      // A refused call sets nothing, so set the theme again without sound
      $.ui.log(error.message)
      await $.theme.set(look)
    }
    return next(e)
  })
}
```

For the other waves, fields, and ranges, see `ThemeSound` in [the types for your build](https://code.claude.com/docs/en/plugins/mods/create.md#get-the-types-for-your-build). To hear the example:

**1. Start a session**

Put the code in a [mod](https://code.claude.com/docs/en/plugins/mods/create.md#write-a-mod-yourself), and save the mod's directory [under `~/.claude/skills/`](https://code.claude.com/docs/en/plugins/create#scaffold-a-plugin-that-loads-every-session) so that it loads when you start a session. In the Code tab, send a first message to [start a local session](https://code.claude.com/docs/en/desktop.md#start-a-session). If no speaker button appears in the session's title bar, see [Fix a missing speaker button](#fix-a-missing-speaker-button).

**2. Turn on theme sound**

If the speaker button is crossed out, select it. The three notes play once to confirm that sound is on, and the noise fades in. To change the volume or turn off the noise, open the menu beside the button.

**3. Hear the cue**

Send another message. The three notes play when Claude finishes.

#### When each theme sound plays

Theme sound is off until the user turns it on with the speaker button. It then stays on for other sessions and themes on that device until the user turns it off, signs out, or switches accounts. Choose a `gain` that suits a user who hears your theme as soon as it loads.

The Desktop app plays each sound by itself at these moments, and a mod can't trigger one:

| Sound | When it plays |
| :- | :- |
| `ambience` | While the session's window has focus. It pauses after 10 minutes with no input and resumes at the next input. |
| `cues.send` | The user sends a message |
| `cues.tool` | Claude starts a tool call |
| `cues.compact` | The conversation is compacted |
| `cues.done` | Claude finishes a turn, unless the user stopped it or queued another message |
| `cues.ask` | A permission prompt or a question appears |
| `cues.error` | A turn ends in an error |
| `cues.click` | The user clicks the background where no message, control, or panel covers it |

When the user turns on sound or picks a volume, they also hear one cue, the first the theme has in this order: `send`, `done`, `tool`, `compact`, `ask`, `error`.

Expect fewer of the table's sounds during an unanswered prompt, during speech, and in a window without focus. To hear all of them again:

* **A permission prompt or a question is waiting**: answer it. Until then, only `cues.ask` can play.
* **Dictation, a voice call, or a reply read aloud is in progress**: end it. Until then, the ambience and cues stay silent.
* **The window doesn't have focus**: click in the window. Until then, only `cues.done` can play.

#### Fix a missing speaker button

If the session's title bar shows no speaker button, check your version, whether the mod loaded, and the `$.theme` calls in the session:

* **Old version**: if `/status` in the Code tab shows a version before v2.1.329, [update the Desktop app](https://code.claude.com/docs/en/desktop.md#claude-code-version-in-the-code-tab) and start a new local session. On those versions, the call fails with an error such as `theme.set does not know the attribute "sound"`.
* **Mod not loaded**: follow [Find out why a mod does nothing](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#find-out-why-a-mod-does-nothing).
* **Value out of range**: the call fails, so with the example's `catch` block the theme loads without sound. Find the error that the example logs in the transcript, and fix the field it names, as in `sound.cues.done.layers[0].gain is a number, 0 to 1`.
* **Another `$.theme` call**: when any mod makes a later `$.theme.set` call without `sound`, or calls `$.theme.clear()`, the sound and the button disappear. In your own mod, pass `sound` in the same call as the rest of the theme. Turn off any other mod that sets a theme.

## Build a tree from elements

What a `ui.render` hook returns is an element tree: a description of what to draw, made of boxes, text, and controls nested inside each other.

To get the elements, call `$.ui.resolve(e)` in your hook, as in `const { Box, Text, Button } = $.ui.resolve(e)`. Each element is a function. You pass it props, and you put the elements and strings that go inside it in `children`.

Select a tab to see each of the most common elements and how the terminal draws it:

> [tab] Text
>
> `Text` draws a string, with optional styling such as `bold` and `color`:
>
> ```javascript theme={null}
> Text({ children: ['This is the first tab.'] })
> ```
>
> ```text theme={null}
> This is the first tab.
> ```

> [tab] Box
>
> `Box` arranges what's inside it, in a row or a column. This one puts a button and a line of text side by side, two columns apart:
>
> ```javascript theme={null}
> Box({
>   flexDirection: 'row',
>   columnGap: 2,
>   children: [
>     Button({ key: 'more', label: 'Add one', onPress: addOne }),
>     Text({ children: ['Count: 0'] }),
>   ],
> })
> ```
>
> ```text theme={null}
> [ Add one ]  Count: 0
> ```

> [tab] Button
>
> `Button` is a control the user can press. It runs your `onPress` callback. With `plain: true` it has no brackets and shows its hotkey:
>
> ```javascript theme={null}
> Button({ key: 'more', label: 'Add one', onPress: addOne })
> Button({ key: 'tab-one', label: 'One', hotkey: '1', plain: true, onPress: showTabOne })
> ```
>
> ```text theme={null}
> [ Add one ]
> 1: One
> ```

> [tab] Input
>
> `Input` is a text field. It runs your `onSubmit` callback with the text when the user presses Enter:
>
> ```javascript theme={null}
> Input({
>   key: 'new-note',
>   label: 'Note',
>   placeholder: 'Type a note and press Enter',
>   value: '',
>   submitLabel: 'add',
>   onSubmit: addNote,
> })
> ```
>
> ```text theme={null}
> Note: Type a note and press Enter
> ```
>
> Set `rows` to 2 or more for [a field that holds several lines](https://code.claude.com/docs/en/plugins/mods/gallery.md#input).

The [interface gallery](https://code.claude.com/docs/en/plugins/mods/gallery.md) has samples and screenshots of most elements. This table lists the main elements:

| Element | What it draws | Where |
| :- | :- | :- |
| `Box` | A flex container that takes layout props such as `flexDirection`, [`borderStyle`](https://code.claude.com/docs/en/plugins/mods/reference#box-border-styles), `width`, and `overflowX`. Spacing props such as `columnGap` and `padding` take a number or a [step name](https://code.claude.com/docs/en/plugins/mods/reference.md#box-spacing-steps) from `'xs'` to `'xl'`. `overflowX` requires Claude Code v2.1.326 or later. | Everywhere |
| `Text` | Styled text. Takes `color`, `bold`, `dimColor`, `italic`, `wrap`, `maxLines`, and others such as [`weight`](https://code.claude.com/docs/en/plugins/mods/reference#text-typography). A `color` is a theme key or a color such as `'red'`. A `wrap` is a value such as `'wrap'`, `'truncate'`, `'truncate-start'`, `'truncate-middle'`, `'truncate-end'`, or `'clip'`. `maxLines` and `'clip'` require Claude Code v2.1.326 or later. | Everywhere |
| `Button` | A control that calls `onPress` | Everywhere |
| `Link`, `Code`, `Markdown` | A link with `href` and an optional `label`, a code block, and text formatted the way Claude's replies are. `Markdown` takes its content in a `text` prop, not in `children`, and needs a `key` when you pass `onLinkPress`. | Everywhere |
| `Input`, `Select` | A text field and a dropdown | Terminal, Desktop, VS Code |
| `Shader` | A [backdrop drawn on the GPU](#animate-a-backdrop-with-a-shader) over an `Svg` | Desktop |
| `Svg` | An SVG document | Desktop, VS Code |
| `Client` | A region drawn by a second file of yours, for animation and pointer input. That file gets no mods API. It reaches your hooks by posting data, which arrives as a `ui.message` event. If it fails to load, draw, or run, your hooks receive a [`ui.fault`](https://code.claude.com/docs/en/plugins/mods/reference#interface) event. | Terminal, Desktop |
| `Raster`, `Image` | A [grid of colored cells](#draw-a-grid-of-colored-cells), and a picture | Terminal |

If your module is a `.tsx` or `.jsx` file, you can write the tree as JSX. Destructure the elements from `$.ui.resolve(e)` first.

If your drawing doesn't show up, check its tree for a prop an element doesn't take or a child where none goes. A hook that returns such a tree [fails](https://code.claude.com/docs/en/plugins/mods/events.md#handle-a-hook-that-fails), and a [`hook skipped` line](https://code.claude.com/docs/en/plugins/mods/troubleshoot#a-pane-or-band-is-empty) names your mod and the rule the tree broke. For a `Text` in a pane with a prop named `bogusProp`, that line reads:

```text theme={null}
my-mod: ui.render hook skipped: returned the wrong shape (a tree Pane refuses: Text prop "bogusProp" is not allowed)
```

### `Link` in the Desktop app and VS Code

In the Desktop app and the VS Code extension, a `Link` draws as plain text unless its `href` meets these requirements:

* **Scheme and host**: an `https:` URL, or an `http://localhost` URL such as `http://localhost:3000`
* **No `@`**: write an `@` in the path or query as `%40`
* **Spelling**: what `new URL(href).href` returns, apart from a missing `/` after the host. That excludes an uppercase host, a space, and `:443` on an `https:` URL.

In the terminal, these requirements don't apply.

### When a `Client` fails

In the terminal, when the file a `Client` runs fails, a dimmed line such as `my-mod: Client client/spinner.js: boom` takes the `Client`'s place, and the rest of your drawing still shows.

If your mod handles [`ui.fault`](https://code.claude.com/docs/en/plugins/mods/reference#interface), Claude Code then [draws the site again](#when-claude-code-redraws-without-being-asked).

### Draw a grid of colored cells

For a heat map, a sparkline, or a game board in the terminal, draw one `Raster` and not a `Box` for each cell. A `Raster` takes a `key`, its size in `columns` and `rows`, and `cells`, a base64 string that packs every cell. Each cell is three numbers: the character's code point, its color, and its background color. A color is a 24-bit RGB value in hexadecimal, such as `0xc62828` for a red. The value `0x01000000`, one above that range, means the terminal's default.

Apps other than the terminal have no `Raster`, so check `e.surface` and draw text there. This pane body draws a three by two heat map:

```javascript theme={null}
// The value that means "use the terminal's default color"
const DEFAULT_COLOR = 0x01000000

// Pack rows of [character, color] pairs into the one string a Raster takes
// One cell is three numbers: the character's code point, its color, and its background
function cellsOf(rows) {
  const numbers = rows.flat().flatMap(([char, color]) => [char.codePointAt(0), color, DEFAULT_COLOR])
  return new Uint8Array(Uint32Array.from(numbers).buffer).toBase64()
}

on('ui.render', { component: 'Pane' }, async ($, e, next) => {
  // Draw only in the pane opened with the id 'heat'
  if (e.requestId !== 'heat') return next(e)
  const { Box, Text, Raster } = $.ui.resolve(e)
  // Two rows of three cells, each a block character and its color
  const rows = [
    [['█', 0x2e7d32], ['█', 0xf9a825], ['█', 0xc62828]],
    [['█', 0x2e7d32], ['█', 0x2e7d32], ['█', 0xf9a825]],
  ]
  if (e.surface !== 'terminal') {
    return Text({ children: ['The heat map needs the terminal.'] })
  }
  return Box({
    flexDirection: 'column',
    children: [Raster({ key: 'grid', columns: 3, rows: 2, cells: cellsOf(rows) })],
  })
})
```

In the terminal, the pane shows the grid:

![A pane in the terminal that holds a small grid of colored blocks, two rows of three. The top row is green, amber, and red. The bottom row is green, green, and amber.](https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-heat-map.svg?fit=max\&auto=format\&n=dgiVO_Od1X1faduV\&q=85\&s=b91bcce3bad74bc851149133d4acc5d5)

The `rows` array is the part you'd change, and `cellsOf` turns it into the packed string. The hook draws only in a pane whose `id` is `heat`, so open one with `$.ui.open({ id: 'heat' })` from a command, as the [`hello-tabs` example](#build-a-pane-with-tabs) opens its pane.

Each character has to be one cell wide. To animate a `Raster` that's already on screen, call `$.ui.blit` with the pane's `id` as `requestId`, the `Raster`'s `key`, the same size, and new cells. For this example, that's `$.ui.blit({ requestId: 'heat', key: 'grid', columns: 3, rows: 2, cells: cellsOf(newRows) })`. It repaints that one element without running your `ui.render` hook again.

## Respond to presses and typing

When the user presses a button, types into a field, or picks from a list your mod drew, Claude Code calls that control's callback, which runs in your module. Each control takes its own callbacks:

* **`Button`**: takes `onPress(e)`, where `e.surface` is the app the press came from
* **`Input`**: takes `onSubmit(value)` and `onInput(value)`
* **`Select`**: takes `onSelect(value)` with its choices in `options`, a list of at least one choice with unique values, such as `[{ value: 'sm', label: 'Small' }, { value: 'lg', label: 'Large' }]`

### Which controls need a `key`

Give every `Input` and `Select` a `key` prop, such as `key: 'size'`. A `Button` can go without a `key` when it has a `label` prop or a single string child. Its key is then the `label` value or that string.

Tests and other mods identify a control by its key:

* **Tests**: a [test](https://code.claude.com/docs/en/plugins/mods/test.md#test-a-drawing) presses or types into a control by its key.
* **Other mods**: Claude Code fires [`ui.press`, `ui.input`, or `ui.select`](https://code.claude.com/docs/en/plugins/mods/reference#interface) with the control's key in `e.element` before it runs the control's callback. Another mod's hook can also [run for that event](https://code.claude.com/docs/en/plugins/mods/events.md#hook-other-mods-drawings-and-controls). That hook sees what the user typed into your `Input` and can change that text or keep your callback from running. The mods API gives that mod no method to press your buttons.

If a message says `needs a key` or `is drawn twice`, [find the cause by that message](https://code.claude.com/docs/en/plugins/mods/troubleshoot.md#needs-a-key).

### Keyboard focus and hotkeys

Your mod never reads the keyboard itself. The user presses a key, Claude Code decides which of your controls it's for, and that control's callback runs. Apart from a [digit hotkey on the band or an `action` binding](https://code.claude.com/docs/en/plugins/mods/reference#elements), that happens only while your pane or band has keyboard focus. The rest of the time, keys go to the prompt.

In the [VS Code extension](#draw-in-the-vs-code-extension), buttons have no hotkeys: the user clicks a button or presses Enter on it, and types into fields.

#### How a pane gets keyboard focus

A pane gets keyboard focus when:

* Your mod opens it with `focus: true` from a command or a press
* The user presses Ctrl+X then Tab
* The user clicks it, which in the terminal needs [fullscreen rendering](https://code.claude.com/docs/en/fullscreen.md)

Claude Code grants `focus: true` only while the prompt is empty and nothing else has keyboard focus. A pane that opens while the user is typing doesn't take their keystrokes.

#### What each key does

This table lists what a key does while your pane or band has keyboard focus:

| Key | What it does |
| :- | :- |
| Tab | Moves to the next control |
| Up and Down | Move between controls while your drawing fits. When the pane or band has more rows than it can show, they scroll it. In an `Input` in the terminal, they [move between the field's rows](https://code.claude.com/docs/en/plugins/mods/gallery.md#input), and from its first or last row they move to the control before or after it. |
| Enter | Presses the focused `Button`, submits the focused `Input`, or picks in a `Select` |
| A button's hotkey | Presses that button. While an `Input` has the focus, every printable key goes to the field. |
| Page Up, Page Down, Home, and End | Scroll your pane or band when it has more rows than it can show |
| Ctrl+X then an arrow key | Resizes your pane. Left or Up gives it more room, and Right or Down gives the room back. A pane beside the transcript stops widening at 45% of the terminal's width. |
| Ctrl+X then X | Closes your pane, even while one of its fields has the focus |
| Ctrl+X then Ctrl+A | [Collapses the band](#when-the-user-collapses-the-band) to one row while a mod draws there, or expands it again. These keys also work while the prompt has the focus. |
| Esc | Returns keyboard focus to the prompt. With `closeOnEscape: true`, it also closes the pane. |

A mod can't bind Tab or the arrow keys to anything else, so a game steers with `w`, `a`, `s`, and `d`.

#### Set a hotkey and the first focus

* **`hotkey`**: to let the user press a `Button` with one key, give it a `hotkey` of one digit or one lowercase letter, as in `hotkey: 'a'`
* **`autoFocus`**: to choose which control has the focus when the pane opens, add `autoFocus: true` to it. In the [VS Code extension](#draw-in-the-vs-code-extension), `autoFocus` does nothing: the control draws as if you had left it out, and you don't need to change anything. The prop accepts only `true`, so omit it on the other controls.

How a hotkey shows depends on the button and the app:

| Button | In the terminal | In the Desktop app | In the VS Code extension |
| :- | :- | :- | :- |
| With brackets, the default | `[ Add one ]`, with no hotkey shown | The label with a small key beside it | The label, and the hotkey does nothing |
| With `plain: true` | `1: One` | The label with a small key beside it | The label, and the hotkey does nothing |

In the terminal, name the key in a bracketed button's label, or use `plain: true`, so the user can see what to press. The [elements reference](https://code.claude.com/docs/en/plugins/mods/reference.md#elements) has the other `Button` rules: `action`, digit hotkeys on the band, and two buttons on one hotkey.

#### When the user collapses the band

In the terminal, while a mod draws in the band, the user can collapse the band to one row to get it out of the way:

* **Click `[-]`**: while the band is expanded, Claude Code draws this mark at the right end of its first row. In [fullscreen rendering](https://code.claude.com/docs/en/fullscreen.md), the user clicks it to collapse the band.
* **Press Ctrl+X then Ctrl+A**: this works whether the prompt, the band, or a pane has keyboard focus. The user can [bind other keys](https://code.claude.com/docs/en/keybindings.md#above-prompt-actions) to it through the `abovePrompt:toggle` action.

A collapsed band hides everything the mods draw there and shows one dim row instead, which names the keys that expand it as the user has them bound:

```text theme={null}
▸ plugin panel hidden · ctrl+x ctrl+a or click to show
```

The same keys, or in fullscreen rendering a click on the row, expand the band again. Until then, nothing presses a button in it: no hotkey, no digit typed into an empty prompt, and no keybinding for a button's [`action`](https://code.claude.com/docs/en/plugins/mods/reference#elements). If the band has keyboard focus when the user collapses it, the focus returns to the prompt, and Ctrl+X then Tab skips the band while it's collapsed.

The band stays collapsed until the user expands it, even after `/clear`, and is expanded again the next time Claude Code starts. Your mod can't expand it. Don't make the band the only place your mod shows something the user has to answer. To show that elsewhere only while the band is collapsed, read `e.props.isCollapsed` in your `ui.render` hook, which keeps running. `isCollapsed` requires Claude Code v2.1.321 or later.

### Take typed input and draw a row for each item

Many panes are a text field with a list under it. The example in this section is a notes pane: you type a note and press Enter to add it, and each note has an `x` button that deletes it. With two notes added, the terminal draws the pane this way:

```text theme={null}
╭────────────────────────────────────────────────────────✕─╮
│ Note: Type a note and press Enter ⏎ add                  │
│ x buy milk                                               │
│ x call bob                                               │
╰──────────────────────────────────────────────────────────╯
```

The `✕` on the top border is Claude Code's own mark for closing the pane.

The example uses these techniques:

* **Take typed input**: an `Input` calls `onSubmit(value)` with the field's text when the user presses Enter, and `onInput(value)` on every change
* **Draw a list**: map your data to one row each, and give every row's button its own `key`

This hook draws the pane's content:

```javascript theme={null}
// The list the pane draws
let notes = []

on('ui.render', { component: 'Pane' }, async ($, e, next) => {
  // Draw only in the pane opened with the id 'notes'
  if (e.requestId !== 'notes') return next(e)
  const { Box, Text, Button, Input } = $.ui.resolve(e)
  const redraw = () => $.ui.invalidate('ui.render')

  return Box({
    flexDirection: 'column',
    children: [
      Input({
        key: 'new-note',
        label: 'Note',
        placeholder: 'Type a note and press Enter',
        // The text the field starts with
        value: '',
        submitLabel: 'add',
        autoFocus: true,
        // Runs when you press Enter in the field
        onSubmit: async (value) => {
          // Ignore an empty line
          if (!value.trim()) return
          notes = [...notes, value.trim()]
          redraw()
          await $.store.set('notes', notes)
        },
      }),
      // One row for each note: a delete button, then the note's text
      ...notes.map((note, i) =>
        Box({
          flexDirection: 'row',
          columnGap: 1,
          children: [
            Button({
              // A key of its own, so each row's button can be told apart
              key: 'delete-' + i,
              label: 'x',
              plain: true,
              onPress: async () => {
                notes = notes.filter((_, j) => j !== i)
                redraw()
                await $.store.set('notes', notes)
              },
            }),
            Text({ children: [note] }),
          ],
        }),
      ),
    ],
  })
})
```

To try the pane:

* **Add a note**: type a line and press Enter. The line appears as a new row, and the field empties.
* **Delete a note**: press Tab until the note's `x` button has the focus, then press Enter. The `x` is the button's label and not a hotkey, so typing the letter doesn't press it.

Each change follows the same render cycle as `hello-tabs`: the callback changes `notes`, calls `redraw`, and saves the list to `$.store`. If your hook draws the pane again while the user is typing a note, the field keeps their text as long as the hook passes the same `value` each time. To replace their text with your own, pass a different `value`.

The example saves the notes and doesn't load them. To bring them back in the next session, read them in a `session.start` hook, the way `hello-tabs` reads `count`.

These props make up the field's line, `Note: Type a note and press Enter ⏎ add`:

| Prop | In the example | What it is |
| :- | :- | :- |
| `label` | `Note` | The text before the field. The terminal draws `: ` after it. |
| `placeholder` | `Type a note and press Enter` | Dim text that shows while the field is empty |
| `value` | `''` | The text the field starts with. It's empty here, so the placeholder shows. |
| `submitLabel` | `add` | The word after `⏎` that says what Enter does |

Submitting an `Input` doesn't start a turn unless your callback calls [`$.prompt.submit`](https://code.claude.com/docs/en/plugins/mods/api#start-a-turn-from-a-background-job).

## Redraw a site

A drawing is a snapshot: it shows what your `ui.render` hook returned the last time the hook ran. To show something new, the hook has to run again. Claude Code runs it again for some changes, and your mod asks for the rest.

### When Claude Code redraws without being asked

Claude Code runs your `ui.render` hook again when the site's props change or the terminal's width changes. When a `Client` in the site fails and your mod handles [`ui.fault`](https://code.claude.com/docs/en/plugins/mods/reference#interface), Claude Code runs the hook once more after your `ui.fault` hooks return, so your `ui.render` hook can leave the `Client` out. It doesn't run the hook on a timer, and it can't tell when a variable in your module changes.

### Redraw when your data changes

To have your sites drawn again after your own data changes, call `$.ui.invalidate('ui.render')`. This pane counts presses. The button's callback changes `count`, then asks for a redraw:

```javascript theme={null}
let count = 0

on('ui.render', { component: 'Pane' }, async ($, e, next) => {
  if (e.requestId !== 'counter') return next(e)
  const { Box, Text, Button } = $.ui.resolve(e)
  return Box({
    flexDirection: 'row',
    columnGap: 2,
    children: [
      Button({
        key: 'more',
        label: 'Add one',
        onPress: () => {
          count += 1
          // The data changed, so ask Claude Code to draw the pane again
          $.ui.invalidate('ui.render')
        },
      }),
      Text({ children: ['Count: ' + count] }),
    ],
  })
})
```

Each press raises the number in the pane. The [`hello-tabs` example](#build-a-pane-with-tabs) wraps the same call in its `redraw` function.

A value you keep in [`$.state`](#keep-a-value-in-\$-state) doesn't need the call, because writing the value redraws the sites that read it.

### Redraw on a timer

To keep a clock, a countdown, or a value from outside the session current, redraw on a schedule. Start a timer in the module's `session.start` hook. If the module already has one, as `hello-tabs` does, add the [`$.clock.every`](https://code.claude.com/docs/en/plugins/mods/api#run-work-in-the-background) line to it:

```javascript theme={null}
on('session.start', async ($, e, next) => {
  // Every 1000 milliseconds, ask Claude Code to draw your sites again
  $.clock.every(1000, () => $.ui.invalidate('ui.render'))
  return next(e)
})
```

Claude Code now runs your `ui.render` hook once a second. The timer stops after the module reloads, and the new instance of the module starts its own.

### How often a site can redraw

Claude Code throttles redraws of a site, so your mod can call `$.ui.invalidate` as often as its data changes. For how often each site can redraw, see the [limits table](https://code.claude.com/docs/en/plugins/mods/reference.md#limits).

Calls that come faster than the limit are coalesced into one redraw. That redraw runs your hook once, and the hook reads your data as it is at that moment, so the latest value shows and the values in between don't. An animation can't run faster than the limit.

## Keep state

Where a mod keeps a value decides how long the value lasts: until the module reloads, until the session ends, or from one session to the next. Choose by how long the value has to last:

| Keep it in | It lasts until | Use it for |
| :- | :- | :- |
| A module-level variable | The module reloads, which happens every time you save a file during development | Values you can lose, as `tab` is in `hello-tabs` |
| `$.state` | The session ends, or the user runs `/clear`, `/resume`, or `/branch` | Values a drawing depends on that should survive a reload |
| `$.store` | Your mod deletes it, or no session reads or writes the store for [`cleanupPeriodDays`](https://code.claude.com/docs/en/settings-reference#cleanupperioddays). The store is a key-value store, saved as a JSON file of your plugin's own under `~/.claude/plugins/store/`. | Settings, history, anything the user expects to find next time |

`$.store.get(key)` resolves to the value or `undefined`, and `$.store.set(key, value)` takes any JSON value.

### Keep a value in `$.state`

`$.state` holds values for the length of a session, and it redraws for you. It's reactive state: a `ui.render` hook that reads a value subscribes to it, so Claude Code redraws that site each time you write the value, and you don't call `$.ui.invalidate`. A value in `$.state` also survives a reload of the module, which a variable doesn't.

To set it up, declare your values, point your manifest at the declaration, then define and use each value. The examples move the `count` from `hello-tabs` into `$.state`.

#### Declare the values

Declare the values in a type declaration file. The outer key is your plugin's name, and each entry under it is a value and its type. Save this as `hello-tabs/types/index.d.ts`:

```typescript hello-tabs/types/index.d.ts theme={null}
declare module 'claude-code' {
  interface PluginState {
    'hello-tabs': {
      tab: 'one' | 'two'
      count: number
    }
  }
}
```

#### Point the manifest at the declaration

To let `claude plugin validate` check your code against that file, add a `types` field to the manifest with its path:

```json hello-tabs/.claude-plugin/plugin.json theme={null}
{
  "name": "hello-tabs",
  "version": "0.1.0",
  "description": "Opens a pane with two tabs and a counter",
  "author": { "name": "Your Name" },
  "types": "./types/index.d.ts"
}
```

#### Define, read, and write a value

In your module, define each value with a default, read it while drawing, and write it from a callback. `atom` names a value and its default, `read` returns it, and `update` writes it. The three helpers call `$.state.get` and `$.state.set` for you:

```javascript theme={null}
import { atom, read, update } from 'claude-code'

// At the top of the module: name the value and give its default
const count = atom({ plugin: 'hello-tabs', key: 'count' }, 0)

// In the ui.render hook: read the value to draw it
const n = await read($, count)

// In a Button: write a new value from the old one
onPress: () => update($, count, (value) => value + 1)
```

Because the `ui.render` hook read `count`, Claude Code runs the hook again each time the button writes it.

These rules apply to the code:

* **Write `plugin` and `key` as string literals**: `claude plugin validate` reads them from your source
* **Hold the result of each `atom` call in a `const`**: if you declare `count` with `let`, validation fails with `takes a source the scan can read`
* **Declare every value in the type declaration file**: otherwise validation fails with `hello-tabs.count is not declared`
* **Write from a callback or another event's hook**: a `ui.render` hook can read state and can't write it, so write from `onPress`, `onSubmit`, or a hook for another event

#### Change `hello-tabs` to use `$.state`

To move `count` in `hello-tabs` into `$.state`, change every line that uses it:

* **At the top of the module**: add the `import` line, and replace `let count = 0` with the `atom` line
* **In the `ui.render` hook**: add the `read` line before `tabButton`, and draw `'Count: ' + n` in the `Text`
* **In the Add one button**: replace `onPress` with the one in [Save from more than one session](#save-from-more-than-one-session), which saves the count as well as writing it
* **In the `session.start` hook**: replace the two lines that read `saved` with the `loadCount` call from [Load a saved value again after `/clear`](#load-a-saved-value-again-after-clear)

Keep `redraw` for the tab buttons, because `tab` is still a variable.

### Load a saved value again after `/clear`

If your mod copies a saved value from `$.store` into `$.state` at `session.start`, it has to copy it again after `/clear`, `/resume`, or `/branch`. Those commands reset every `$.state` value to its default, and `session.start` doesn't fire again. [`classic.SessionStart`](https://code.claude.com/docs/en/plugins/mods/events#hook-the-settings-hook-events) does fire after each of them, with `e.source` set to `clear`, `resume`, or `fork`, so copy the value again in a hook on it. Otherwise your drawing shows the default, and a callback that saves the `$.state` value writes the default over what you stored.

This code loads `count` from both hooks. It builds on the `$.state` version of `hello-tabs`, where `count` is an atom and `update` is imported. Put `loadCount` above `register`, and add the `loadCount` call to the `session.start` hook you already have. `classic.SessionStart` also fires at startup and after compaction, which doesn't reset `$.state`, so the filter on `source` keeps the hook to the three resets:

```javascript theme={null}
// Copy the saved count from $.store into $.state, or 0 if nothing is saved
async function loadCount($) {
  const saved = Number((await $.store.get('count')) ?? 0)
  await update($, count, () => saved)
}

// Runs before your first prompt, and again after a reload
on('session.start', async ($, e, next) => {
  await loadCount($)
  return next(e)
})

// Runs again after /clear, /resume, and /branch, which reports fork
on('classic.SessionStart', { source: ['clear', 'resume', 'fork'] }, async ($, e, next) => {
  await loadCount($)
  return next(e)
})
```

With both hooks in place, the pane shows the saved count after `/clear` and not `0`, and the next press of **Add one** adds to the saved count.

`loadCount` writes the stored value over the one in `$.state`, and `session.start` fires again each time the module reloads. To keep the store from falling behind, save on every change, as the **Add one** button does.

To check the reload without a session, [test the drawing after `/clear`](https://code.claude.com/docs/en/plugins/mods/test#test-a-drawing-after-clear).

### Save from more than one session

Every session on your machine that runs your mod shares one `$.store`. A `get` followed by a `set` isn't atomic. When two sessions each read a value, change it, and write it back, they race, and the second write replaces the first.

To make that less likely:

* **Give each item its own key**: a `set` changes only its own key, so sessions that write different keys don't overwrite each other
* **Read again right before you write**: for a value that several sessions change, `get` the key in the callback and build the new value from that, not from a copy you loaded at `session.start`. Another session's write is still lost if it lands between your `get` and your `set`.

This button adds one to whatever the store holds now, then updates the drawing:

```javascript theme={null}
onPress: async () => {
  // Read what the store holds now, which another session may have changed
  const saved = Number((await $.store.get('count')) ?? 0)
  // Save the new count, then show it
  await $.store.set('count', saved + 1)
  await update($, count, () => saved + 1)
}
```

If a second session has pressed its own button three times since this session started, this press shows and saves a count that includes those three.

## Next steps

* [React to events](https://code.claude.com/docs/en/plugins/mods/events.md): feed your drawing from tool calls and turns
* [Use the mods API](https://code.claude.com/docs/en/plugins/mods/api.md): feed your drawing from timers and model calls
* [Test a drawing](https://code.claude.com/docs/en/plugins/mods/test.md#test-a-drawing): press your buttons from a test, on more than one surface
* [Render sites](https://code.claude.com/docs/en/plugins/mods/reference.md#render-sites) and [elements](https://code.claude.com/docs/en/plugins/mods/reference.md#elements): each site's props and each element's props
