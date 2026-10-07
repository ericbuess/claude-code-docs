> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Draw in the interface with a mod

> Draw panes, a band above the prompt, buttons, and text fields from a Claude Code mod, handle presses and input, and keep state between redraws and sessions.

A mod can draw its own interface in Claude Code and change parts of the interface Claude Code already draws. Each place a mod can draw is called a [render site](/docs/en/plugins/mods/reference#render-sites), such as a pane, the band above the prompt, or the spinner. Claude Code fires the [`ui.render`](/docs/en/plugins/mods/reference#interface) event each time it's about to draw a render site, and your hook for that event returns what to draw there.

This map shows where a mod can draw in a terminal session:

<img src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-screen-map.svg?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=5fda26b6609c62b68c6f9e528c1590ea" className="dark:hidden" alt="Map of a Claude Code terminal session. A mod can add a pane as a sidebar on the right, a toast at the top right of the transcript, a log line in the transcript, a band above the prompt, and a status line under the prompt. A mod can redraw messages, tool call rows, and the spinner. The prompt is Claude Code's own." width="600" height="336" data-path="images/mods-screen-map.svg" />

<img src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-screen-map-dark.svg?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=5b4161581a1bd2c0450b0c8b57bc1225" className="hidden dark:block" alt="Map of a Claude Code terminal session. A mod can add a pane as a sidebar on the right, a toast at the top right of the transcript, a log line in the transcript, a band above the prompt, and a status line under the prompt. A mod can redraw messages, tool call rows, and the spinner. The prompt is Claude Code's own." width="600" height="336" data-path="images/mods-screen-map-dark.svg" />

In a narrower terminal, the pane sits above the prompt instead of beside the transcript.

Build your [first mod](/docs/en/plugins/mods/create) before you start here. Begin with the worked example, which builds a pane with two tabs and a counter, then read the section for each piece you want to change.

<Note>
  To look up one prop or limit, see the [reference](/docs/en/plugins/mods/reference#render-sites).
</Note>

## Build a pane with tabs

In this section you build a mod that adds a `/hello-tabs` command, and the command opens a pane. A pane is a sidebar beside the transcript in a wide fullscreen terminal, or a framed region above the prompt otherwise. This pane shows two tabs, and the second tab has a button that adds one to a counter. The count is still there after you restart Claude Code.

The finished mod looks like this. The recording opens the pane, switches to the second tab, presses the button a few times, and returns to the first tab:

<Frame>
  <video autoPlay muted loop playsInline controls className="w-full dark:hidden" src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-hello-tabs-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=49d520094d87b5b44bfe50fa49677f06" aria-label="The /hello-tabs command is typed at the Claude Code prompt and a framed pane opens above it, with '1: One' and '2: Two' across the top and the text 'This is the first tab.' The second tab shows an 'Add one' button beside 'Count: 1', and the count rises to 3. The pane then returns to the first tab." data-path="images/mods-hello-tabs-light.mp4" />

  <video autoPlay muted loop playsInline controls className="w-full hidden dark:block" src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-hello-tabs-dark.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=ff7a14d713d6e5d3b0000efa8522ea4b" aria-label="The /hello-tabs command is typed at the Claude Code prompt and a framed pane opens above it, with '1: One' and '2: Two' across the top and the text 'This is the first tab.' The second tab shows an 'Add one' button beside 'Count: 1', and the count rises to 3. The pane then returns to the first tab." data-path="images/mods-hello-tabs-dark.mp4" />
</Frame>

The tabs are two buttons in a row. The mod keeps track of which one is active and draws that tab's content under the row.

<Steps>
  <Step title="Create the plugin">
    A mod is a plugin with a manifest, a `hooks.json` that points to your code, and the code file. [Create a mod](/docs/en/plugins/mods/create#write-a-mod-yourself) explains each one. Create a directory named `hello-tabs` with `.claude-plugin` and `hooks` directories inside it, then save the first two files.

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
  </Step>

  <Step title="Write the code">
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

    * **[`session.start`](/docs/en/plugins/mods/reference#session)** also reads the saved count from [`$.store`](#keep-state), a key-value store that persists between sessions.
    * **[`command.run`](/docs/en/plugins/mods/api#add-a-command)** only tells Claude Code the pane exists. Opening a pane draws nothing by itself: Claude Code then fires `ui.render` to ask what goes in it.
    * **`ui.render`** returns the element tree, a `Box` that holds other boxes, text, and buttons, and builds it again from `tab` and `count` each time it runs.

    Pressing a button runs its `onPress` callback, which changes a variable and calls `redraw`. Claude Code then runs the `ui.render` hook again, and the hook builds a new tree from the new values. Every interactive drawing uses that render cycle: a callback changes state, and the hook renders again from the new state.
  </Step>

  <Step title="Open the pane">
    In your shell, start Claude Code with `claude --plugin-dir ./hello-tabs`. At the Claude Code prompt, run `/hello-tabs`. A pane opens with `1: One` and `2: Two` across the top. Press `2`, then press `a`, the hotkey for **Add one**, a few times. The count rises.
  </Step>

  <Step title="Check that the count was saved">
    Press Esc to close the pane, then exit the session. In your shell, start Claude Code again with the same `claude --plugin-dir ./hello-tabs` command, and at the Claude Code prompt run `/hello-tabs`. The count is where you left it.

    To clear the count, have the mod call `$.store.delete('count')`. [Keep state](#keep-state) covers how long each kind of value lasts.
  </Step>
</Steps>

## Pick where to draw

A `ui.render` hook runs for every render site unless you narrow it to the one you want to draw in. To choose the render site, pass a filter, called a [matcher](/docs/en/plugins/mods/events#filter-which-events-a-hook-handles), as the second argument to `on`. `{ component: 'Pane' }` runs the hook only for panes. In the hook, `e.component` names the site, `e.surface` says which app is drawing, and `e.props` holds the site's own data. For a pane, `e.requestId` is the `id` you opened it with.

The pane and the band are empty until a mod fills them. Select a tab to see what each one is and how to draw in it:

<Tabs>
  <Tab title="Pane">
    A pane is a sidebar beside the transcript in a wide fullscreen terminal, or a framed region above the prompt otherwise. With several panes open, each gets a tab that shows its title.

    A pane appears when your mod calls `$.ui.open` with an `id` you choose, as in `$.ui.open({ id: 'hello-tabs' })`. [Open a pane at the right time](#open-a-pane-at-the-right-time) covers the other fields and when a pane waits for a wider terminal.

    To draw in your pane, filter on `{ component: 'Pane' }` and check that `e.requestId` is your `id`.
  </Tab>

  <Tab title="Band above the prompt">
    The band is a strip directly above the prompt input. It's always there, and every mod shares it.

    Your hook returns a tree to show something in the band, or `next(e)` to show nothing. A tree replaces what the mods [after yours](/docs/en/plugins/mods/events#the-order-mods-run-in) draw there. To keep theirs, put the result of `await next(e)` among the children of a [`Box`](#build-a-tree-from-elements) in your tree.

    To draw in the band, filter on `{ component: 'AbovePrompt' }`.
  </Tab>
</Tabs>

### Change what Claude Code already draws

Claude Code draws most of its interface itself: messages, tool call rows, the spinner, and more. Each of those parts is a render site too, so a mod can restyle or replace it. To change one, filter your `ui.render` hook on its name from this table:

| Site | What it is |
| :- | :- |
| `UserMessage`, `AssistantMessage` | A message in the transcript |
| `ToolUse`, `ToolResult`, `ToolGroup` | A tool call's row, its result, and a collapsed group of calls |
| `CommandOutput` | The row a command printed |
| `AskUserQuestion` | The dialog Claude opens to ask you a question |
| `Spinner`, `ToolProgress`, `TurnDuration` | Status lines for a turn: the line that animates while Claude works, a running tool's live progress line, and the line that closes a turn |
| `InfoNotice`, `SessionMode`, `PromptHint` | Status lines under the logo, the mode labels in the footer, and the hint line under the prompt |

At a site Claude Code already draws, your hook can change a detail, replace the drawing, or leave it alone. Select a tab to see each one applied to the spinner. The examples read a `calls` variable that another hook counts, as in the [tutorial mod](/docs/en/plugins/mods/create#write-a-mod-yourself).

<Tabs>
  <Tab title="Change a detail">
    To keep Claude Code's drawing and change one part of it, pass `next` a copy of the event with changed `props`. This hook changes the text after the spinner's word:

    ```javascript theme={null}
    on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
      // Keep Claude Code's spinner, and change the text after its word
      return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
    })
    ```

    The spinner keeps its animation and its word, and your text follows the word:

    ```text theme={null}
    Thinking · tool calls: 2…
    ```
  </Tab>

  <Tab title="Replace the drawing">
    To draw something of your own in the site's place, return a tree and don't call `next`. This hook draws one line of text where the spinner would be:

    ```javascript theme={null}
    on('ui.render', { component: 'Spinner' }, async ($, e) => {
      const { Text } = $.ui.resolve(e)
      // No call to next, so this line is drawn in the spinner's place
      return Text({ children: ['Claude has made ' + calls + ' tool calls'] })
    })
    ```

    While Claude works, your line shows and Claude Code's spinner doesn't:

    ```text theme={null}
    Claude has made 2 tool calls
    ```
  </Tab>

  <Tab title="Leave it alone">
    To leave the site as Claude Code draws it, return `next(e)`. A hook often does that for some events and not others. This hook leaves the spinner alone until there's a call to count:

    ```javascript theme={null}
    on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
      // Nothing to show yet, so pass the event on unchanged
      if (calls === 0) return next(e)
      return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
    })
    ```

    Before the first tool call, the spinner looks the way it does without the mod:

    ```text theme={null}
    Thinking…
    ```
  </Tab>
</Tabs>

At these sites, `next(e)` returns a reference to Claude Code's drawing, `{ type: 'engine', ref }`, unless a mod that runs after yours returned a tree of its own. To change what's in that drawing, pass `next` a copy of the event with different props, as the **Change a detail** tab does. You can return the reference as it is, or place it in a `Box` beside elements of your own:

```javascript theme={null}
on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
  const { Box, Text } = $.ui.resolve(e)
  const theirs = await next(e)
  return Box({ flexDirection: 'column', children: [theirs, Text({ children: ['under the spinner'] })] })
})
```

While Claude works, the spinner animates as before, and `under the spinner` appears below it.

The permission prompt isn't a render site, so a mod can't change what it shows. The question dialog, `AskUserQuestion`, is one, so a mod can change that. A tree for the dialog has to hold the reference exactly once, with your elements above it. Otherwise, Claude Code draws its own dialog.

The terminal and the Desktop app don't raise all the same sites. `Pane`, `AbovePrompt`, `Spinner`, and the transcript sites work in both. A few other status lines are raised in the terminal only. The [render sites table](/docs/en/plugins/mods/reference#render-sites) lists where each one is raised.

### Open a pane at the right time

A pane appears only when your mod opens it. How and when you open it decides whether it takes keyboard focus, how much room it asks for, and whether it shows at all in a narrow terminal.

To open a pane, call [`$.ui.open`](/docs/en/plugins/mods/reference#mods-api-methods) with an `id` you choose. The `id` is the pane's name: your `ui.render` hook checks for it, and you pass it again to close the pane.

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
| `holdToasts` | Holds toasts, the small notices from [`$.ui.toast`](/docs/en/plugins/mods/api#show-something-without-starting-a-turn), until the pane closes |
| `rows` | The height to ask for when the pane sits above the prompt. The default is a third of the space. |
| `columns` | The width to ask for when the pane sits beside the transcript |

`focus`, `closeOnEscape`, and `holdToasts` are optional and accept only `true`. To leave one off, omit it. Passing `false` throws an error such as `ui.open: focus is true or left out`. To set one of them conditionally, add the field only when the condition holds. This call asks for keyboard focus only when `items` isn't empty:

```javascript theme={null}
const pane = { id: 'hello-tabs', title: 'Hello tabs' }
await $.ui.open(items.length > 0 ? { ...pane, focus: true } : pane)
```

To let a command open the pane while Claude is working, add `immediate: true` when you [register the command](/docs/en/plugins/mods/api#add-a-command). Without it, a command typed during a turn waits for the turn to end.

#### When a pane waits for a wider terminal

A pane your mod opens without being asked doesn't appear in a narrow terminal, so it can't take over a small screen. Whether it appears depends on what opened it:

* **Opened by something the user did**, such as a command they ran or a button they pressed, the pane appears at any width
* **Opened by your mod acting by itself**, such as from a timer or a [`turn.start`](/docs/en/plugins/mods/events#follow-a-turn) hook, the pane appears only in a terminal at least 144 columns wide. After the user has opened that pane once themselves, 110 columns is enough.

When the pane appears, `$.ui.open` resolves to `{ isPlaced: true }`. When the pane is waiting, `isPlaced` is `false` and `reason` is a string that says why. A waiting pane appears when the user opens it or widens the terminal. To say something is available without opening a pane, call `$.ui.toast('Your message')`, which shows a toast notification.

## Build a tree from elements

What a `ui.render` hook returns is an element tree: a description of what to draw, made of boxes, text, and controls nested inside each other. You describe the drawing, and Claude Code renders it in the terminal or the Desktop app.

To get the elements, call `$.ui.resolve(e)` in your hook, as in `const { Box, Text, Button } = $.ui.resolve(e)`. Each element is a function. You pass it props, and you put the elements and strings that go inside it in `children`.

Select a tab to see each of the most common elements and how the terminal draws it:

<Tabs>
  <Tab title="Text">
    `Text` draws a string, with optional styling such as `bold` and `color`:

    ```javascript theme={null}
    Text({ children: ['This is the first tab.'] })
    ```

    ```text theme={null}
    This is the first tab.
    ```
  </Tab>

  <Tab title="Box">
    `Box` arranges what's inside it, in a row or a column. This one puts a button and a line of text side by side, two columns apart:

    ```javascript theme={null}
    Box({
      flexDirection: 'row',
      columnGap: 2,
      children: [
        Button({ key: 'more', label: 'Add one', onPress: addOne }),
        Text({ children: ['Count: 0'] }),
      ],
    })
    ```

    ```text theme={null}
    [ Add one ]  Count: 0
    ```
  </Tab>

  <Tab title="Button">
    `Button` is a control the user can press. It runs your `onPress` callback. With `plain: true` it has no brackets and shows its hotkey:

    ```javascript theme={null}
    Button({ key: 'more', label: 'Add one', onPress: addOne })
    Button({ key: 'tab-one', label: 'One', hotkey: '1', plain: true, onPress: showTabOne })
    ```

    ```text theme={null}
    [ Add one ]
    1: One
    ```
  </Tab>

  <Tab title="Input">
    `Input` is a text field. It runs your `onSubmit` callback with the text when the user presses Enter:

    ```javascript theme={null}
    Input({
      key: 'new-note',
      label: 'Note',
      placeholder: 'Type a note and press Enter',
      value: '',
      submitLabel: 'add',
      onSubmit: addNote,
    })
    ```

    ```text theme={null}
    Note: Type a note and press Enter
    ```
  </Tab>
</Tabs>

The [interface gallery](/docs/en/plugins/mods/gallery) has samples and screenshots of most elements. This table lists every element:

| Element | What it draws | Where |
| :- | :- | :- |
| `Box` | A flex container. Takes layout props such as `flexDirection`, `columnGap`, `padding`, [`borderStyle`](/docs/en/plugins/mods/reference#box-border-styles), and `width`. | Everywhere |
| `Text` | Styled text. Takes `color`, `bold`, `dimColor`, `italic`, and `wrap`. A `color` is a theme key or a color such as `'red'`. A `wrap` is `'wrap'`, `'truncate'`, `'truncate-start'`, `'truncate-middle'`, or `'truncate-end'`. | Everywhere |
| `Button` | A control that calls `onPress` | Everywhere |
| `Link`, `Code`, `Markdown` | A link with `href` and an optional `label`, a code block, and text formatted the way Claude's replies are. `Markdown` takes its content in a `text` prop, not in `children`, and needs a `key` when you pass `onLinkPress`. | Everywhere |
| `Input`, `Select` | A text field and a dropdown | Terminal, Desktop |
| `Svg` | An SVG document | Desktop |
| `Client` | A region drawn by a second file of yours, for animation and pointer input. That file gets no mods API. It reaches your hooks by posting data, which arrives as a `ui.message` event. If it fails to load, draw, or run, your hooks receive a [`ui.fault`](/docs/en/plugins/mods/reference#interface) event. | Terminal, Desktop |
| `Raster`, `Image` | A [grid of colored cells](#draw-a-grid-of-colored-cells), and a picture | Terminal |

If your module is a `.tsx` or `.jsx` file, you can write the tree as JSX. Destructure the elements from `$.ui.resolve(e)` first.

If a tree uses an element the app doesn't have, a prop an element doesn't take, or a child where none goes, Claude Code draws its own version of the site.

In a session started with `--plugin-dir`, a transcript line says so, such as `ui.render (Pane) refused: Text prop "bogusProp" is not allowed; the engine drew its own`. The [debug log](/docs/en/plugins/mods/troubleshoot#read-the-debug-log) records it as `ui.render (Pane): a hook returned a tree that does not validate` with the same reason. Nothing else appears in the session, so when a drawing doesn't show up, check that line or the log.

### Draw a grid of colored cells

For a heat map, a sparkline, or a game board in the terminal, draw one `Raster` and not a `Box` for each cell. A `Raster` takes a `key`, its size in `columns` and `rows`, and `cells`, a base64 string that packs every cell. Each cell is three numbers: the character's code point, its color, and its background color. A color is a 24-bit RGB value in hexadecimal, such as `0xc62828` for a red. The value `0x01000000`, one above that range, means the terminal's default.

The Desktop app has no `Raster`, so check `e.surface` and draw text there. This pane body draws a three by two heat map:

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

<img src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-heat-map.svg?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=b91bcce3bad74bc851149133d4acc5d5" alt="A pane in the terminal that holds a small grid of colored blocks, two rows of three. The top row is green, amber, and red. The bottom row is green, green, and amber." width="360" height="132" data-path="images/mods-heat-map.svg" />

The `rows` array is the part you'd change, and `cellsOf` turns it into the packed string. The hook draws only in a pane whose `id` is `heat`, so open one with `$.ui.open({ id: 'heat' })` from a command, as the [`hello-tabs` example](#build-a-pane-with-tabs) opens its pane.

Each character has to be one cell wide. To animate a `Raster` that's already on screen, call `$.ui.blit` with the pane's `id` as `requestId`, the `Raster`'s `key`, the same size, and new cells. For this example, that's `$.ui.blit({ requestId: 'heat', key: 'grid', columns: 3, rows: 2, cells: cellsOf(newRows) })`. It repaints that one element without running your `ui.render` hook again.

## Respond to presses and typing

When the user presses a button, types into a field, or picks from a list your mod drew, Claude Code calls that control's callback, which runs in your module. Each control takes its own callbacks:

* **`Button`**: takes `onPress(e)`, where `e.surface` is the app the press came from
* **`Input`**: takes `onSubmit(value)` and `onInput(value)`
* **`Select`**: takes `onSelect(value)` with its choices in `options`, a list of at least one choice with unique values, such as `[{ value: 'sm', label: 'Small' }, { value: 'lg', label: 'Large' }]`

A test presses or types into a control by its `key`, so give each control one. Each use of a control also fires [`ui.press`, `ui.input`, or `ui.select`](/docs/en/plugins/mods/reference#interface) with the `key` in `e.element`, and another mod can handle those events. Its hook runs before your callback, so it sees what the user types into your `Input` and can change it or answer in place of your callback. The mods API has no method that presses another mod's button.

<h3 id="know-which-keys-your-mod-can-receive">
  Keyboard focus and hotkeys
</h3>

Your mod never reads the keyboard itself. The user presses a key, Claude Code decides which of your controls it's for, and that control's callback runs. Apart from a [digit hotkey on the band](/docs/en/plugins/mods/reference#elements), that happens only while your pane or band has keyboard focus. The rest of the time, keys go to the prompt.

#### How a pane gets keyboard focus

A pane gets keyboard focus when:

* Your mod opens it with `focus: true` from a command or a press
* The user presses Ctrl+X then Tab
* The user clicks it

Claude Code grants `focus: true` only while the prompt is empty and nothing else has keyboard focus. A pane that opens while the user is typing doesn't take their keystrokes.

#### What each key does

This table lists what a key does while your pane or band has keyboard focus:

| Key | What it does |
| :- | :- |
| Tab | Moves to the next control |
| Up and Down | Move between controls while your drawing fits. When the pane or band has more rows than it can show, they scroll it. |
| Enter | Presses the focused `Button`, submits the focused `Input`, or picks in a `Select` |
| A button's hotkey | Presses that button. While an `Input` has the focus, every printable key goes to the field. |
| Page Up, Page Down, Home, and End | Scroll your pane or band when it has more rows than it can show |
| Ctrl+X then an arrow key | Resizes your pane. Left or Up gives it more room, and Right or Down gives the room back. |
| Ctrl+X then X | Closes your pane, even while one of its fields has the focus |
| Esc | Returns keyboard focus to the prompt. With `closeOnEscape: true`, it also closes the pane. |

A mod can't bind Tab or the arrow keys to anything else, so a game steers with `w`, `a`, `s`, and `d`.

#### Set a hotkey and the first focus

These props on a control decide how the keyboard reaches it:

* **`hotkey`**: to let the user press a `Button` with one key, give it a `hotkey` of one digit or one lowercase letter, as in `hotkey: 'a'`
* **`autoFocus`**: to choose which control has the focus when the pane opens, add `autoFocus: true` to it. The prop accepts only `true`, so omit it on the other controls.

How a hotkey shows depends on the button and the app:

| Button | In the terminal | In the Desktop app |
| :- | :- | :- |
| With brackets, the default | `[ Add one ]`, with no hotkey shown | The label with a small key beside it |
| With `plain: true` | `1: One` | The label with a small key beside it |

In the terminal, name the key in a bracketed button's label, or use `plain: true`, so the user can see what to press. The [elements reference](/docs/en/plugins/mods/reference#elements) has the other `Button` rules: `action`, digit hotkeys on the band, and two buttons on one hotkey.

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
        // Draw the field empty each time, which clears it after a submit
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

Each change follows the same render cycle as `hello-tabs`: the callback changes `notes`, calls `redraw`, and saves the list to `$.store`.

The field empties after each submit because of its `value` prop. `value` is the text the field holds when it's drawn, and the user's typing replaces it until your hook draws the field again. The example always draws the field with `''`.

The example saves the notes and doesn't load them. To bring them back in the next session, read them in a `session.start` hook, the way `hello-tabs` reads `count`.

These props make up the field's line, `Note: Type a note and press Enter ⏎ add`:

| Prop | In the example | What it is |
| :- | :- | :- |
| `label` | `Note` | The text before the field. The terminal draws `: ` after it. |
| `placeholder` | `Type a note and press Enter` | Dim text that shows while the field is empty |
| `submitLabel` | `add` | The word after `⏎` that says what Enter does |

Submitting an `Input` doesn't start a turn unless your callback calls [`$.prompt.submit`](/docs/en/plugins/mods/api#start-a-turn-from-a-background-job).

<h2 id="redraw-when-something-changes">
  Redraw a site
</h2>

A drawing is a snapshot: it shows what your `ui.render` hook returned the last time the hook ran. To show something new, the hook has to run again. Claude Code runs it again for some changes, and your mod asks for the rest.

### When Claude Code redraws without being asked

Claude Code runs your `ui.render` hook again when the site's props change or the terminal's width changes. When a `Client` in the site fails and your mod handles [`ui.fault`](/docs/en/plugins/mods/reference#interface), Claude Code runs the hook once more after your `ui.fault` hooks return, so your `ui.render` hook can leave the `Client` out. It doesn't run the hook on a timer, and it can't tell when a variable in your module changes.

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

To keep a clock, a countdown, or a value from outside the session current, redraw on a schedule. Start a timer in the module's `session.start` hook. If the module already has one, as `hello-tabs` does, add the [`$.clock.every`](/docs/en/plugins/mods/api#run-work-in-the-background) line to it:

```javascript theme={null}
on('session.start', async ($, e, next) => {
  // Every 1000 milliseconds, ask Claude Code to draw your sites again
  $.clock.every(1000, () => $.ui.invalidate('ui.render'))
  return next(e)
})
```

Claude Code now runs your `ui.render` hook once a second. The timer stops when the module reloads, and the new instance of the module starts its own.

### How often a site can redraw

Claude Code throttles redraws of a site, so your mod can call `$.ui.invalidate` as often as its data changes. For how often each site can redraw, see the [limits table](/docs/en/plugins/mods/reference#limits).

Calls that come faster than the limit are coalesced into one redraw. That redraw runs your hook once, and the hook reads your data as it is at that moment, so the latest value shows and the values in between don't. An animation can't run faster than the limit.

## Keep state

Where a mod keeps a value decides how long the value lasts: until the module reloads, until the session ends, or from one session to the next. Choose by how long the value has to last:

| Keep it in | It lasts until | Use it for |
| :- | :- | :- |
| A module-level variable | The module reloads, which happens every time you save a file during development | Values you can lose, as `tab` is in `hello-tabs` |
| `$.state` | The session ends, or the user runs `/clear`, `/resume`, or `/branch` | Values a drawing depends on that should survive a reload |
| `$.store` | Your mod deletes it, or no session reads or writes the store for [`cleanupPeriodDays`](/docs/en/settings-reference#cleanupperioddays). The store is a key-value store, saved as a JSON file of your plugin's own under `~/.claude/plugins/store/`. | Settings, history, anything the user expects to find next time |

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
* **Declare every value in the type declaration file**: otherwise validation fails with `hello-tabs.count is not declared`
* **Write from a callback or another event's hook**: a `ui.render` hook can read state and can't write it, so write from `onPress`, `onSubmit`, or a hook for another event

#### Change `hello-tabs` to use `$.state`

To move `count` in `hello-tabs` into `$.state`, change every line that uses it:

* **At the top of the module**: add the `import` line, and replace `let count = 0` with the `atom` line
* **In the `ui.render` hook**: add the `read` line before `tabButton`, and draw `'Count: ' + n` in the `Text`
* **In the Add one button**: replace `onPress` with the one in [Save from more than one session](#save-from-more-than-one-session), which saves the count as well as writing it
* **In the `session.start` hook**: replace the two lines that read `saved` with the `loadCount` call from [Load a saved value again after `/clear`](#load-a-saved-value-again-after-clear)

Keep `redraw` for the tab buttons, because `tab` is still a variable.

<h3 id="load-a-saved-value-again-after-clear">
  Load a saved value again after `/clear`
</h3>

If your mod copies a saved value from `$.store` into `$.state` at `session.start`, it has to copy it again after `/clear`, `/resume`, or `/branch`. Those commands reset every `$.state` value to its default, and `session.start` doesn't fire again. [`classic.SessionStart`](/docs/en/plugins/mods/events#hook-the-settings-hook-events) does fire after each of them, with `e.source` set to `clear`, `resume`, or `fork`, so copy the value again in a hook on it. Otherwise your drawing shows the default, and a callback that saves the `$.state` value writes the default over what you stored.

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

To check the reload without a session, [test the drawing after `/clear`](/docs/en/plugins/mods/test#test-a-drawing-after-clear).

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

* [React to events](/docs/en/plugins/mods/events): feed your drawing from tool calls and turns
* [Use the mods API](/docs/en/plugins/mods/api): feed your drawing from timers and model calls
* [Test a drawing](/docs/en/plugins/mods/test#test-a-drawing): press your buttons from a test, on more than one surface
* [Render sites](/docs/en/plugins/mods/reference#render-sites) and [elements](/docs/en/plugins/mods/reference#elements): each site's props and each element's props
