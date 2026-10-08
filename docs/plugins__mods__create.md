> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create a mod

> Have Claude write a Claude Code mod from a description, or write one yourself that counts tool calls and adds a command. Learn the reload and validate loop.

A mod is a Claude Code [plugin](/docs/en/plugins/overview) with an entry file, called the hooks module: a JavaScript or TypeScript file whose functions Claude Code calls when events happen. To make one:

* **Ask Claude to write it**: [describe what you want](#ask-claude-for-a-mod) in a Claude Code session
* **Write it yourself**: [follow the tutorial](#write-a-mod-yourself) to learn how a mod's code works. You don't need Node.js, a bundler, or a build step, because Claude Code loads `.js` and `.ts` files directly.

If you haven't decided whether a mod is the right tool, read the [comparison on the overview](/docs/en/plugins/mods/overview#compare-mods-settings-hooks-skills-and-mcp-servers) first.

<Note>
  Use Claude Code v2.1.287 or later. In your shell, run `claude --version` to check. To see whether mods can load for you, see [Check whether mods can load](/docs/en/plugins/mods/troubleshoot#check-whether-mods-can-load).
</Note>

## Ask Claude for a mod

Describe the mod you want in an interactive Claude Code session, and Claude writes it. Claude works from a built-in [skill](/docs/en/skills) named `plugin-authoring`, which tells it where to write the mod, which events and methods your version has, and how the mod gets loaded. Claude can load the skill when you ask for a mod, or you can load it yourself by running `/plugin-authoring` at the Claude Code prompt.

The mod runs once you approve it, except in [sessions where a mod Claude writes can't load](#sessions-that-skip-the-approval).

<Steps>
  <Step title="Describe the mod">
    Ask for the mod in your own words, for example `make a mod that shows the current git branch above the prompt`. Claude writes the mod in a directory of its own in the session's mods folder, which is `~/.claude/dev-mods/` followed by the session's ID. A mod's full path looks like `~/.claude/dev-mods/3f2a9c1e-5b7d-4e8a-9c21-6d0f4b8a7e13/git-branch/`.

    <Note>
      In the `default` and `acceptEdits` [permission modes](/docs/en/permission-modes#protected-paths), Claude Code asks before Claude creates each of the mod's files, because `~/.claude` is a protected path. Approve each file as it comes up.
    </Note>
  </Step>

  <Step title="Approve the mod">
    When Claude saves the first file, Claude Code asks whether to enable hot reloading for the session. Hot reloading runs the mods Claude writes in this session and picks up each later change.

    Choose one of these answers:

    * **Enable for this session**: the mods in the session's mods folder load when the turn ends, and reload at the end of each turn that changes them. Your answer lasts for the session, including after you resume it.
    * **Not now**: nothing loads for now. The files stay where Claude wrote them, and the mods load the next time that session starts. To keep a mod from ever loading, delete its directory.
  </Step>

  <Step title="Check that the mod loaded">
    Run `/plugin` at the Claude Code prompt and press Tab until the **Installed** tab is selected. It lists the mod, and you can turn it off there.
  </Step>

  <Step title="Try the mod">
    Use what you asked for. For the example prompt, the current branch name appears above the prompt box. If the mod doesn't do what you wanted, tell Claude what to change. The mod reloads at the end of each turn that changes its files, so you can try the change as soon as Claude finishes.
  </Step>
</Steps>

### Use the mod in other sessions

A mod Claude wrote loads only in the session that made it, and Claude Code deletes that session's mods folder once it's older than [`cleanupPeriodDays`](/docs/en/settings-reference#cleanupperioddays). To keep the mod, copy its directory out of the mods folder to a place of your own, such as `~/mods/git-branch`. Then choose how to load it:

* **In a session you start**: in your shell, run `claude --plugin-dir ~/mods/git-branch`
* **For other people**: [add it to a marketplace](#share-your-mod) so they can install it

<h3 id="sessions-that-skip-the-approval">
  Sessions where a mod Claude writes can't load
</h3>

A mod Claude writes loads only after you approve it, in a trusted workspace where mods are allowed to run. In these sessions it doesn't load:

* **Nobody is there to approve**: the session can't show you a prompt, as in a `claude -p` run or [`dontAsk` mode](/docs/en/permission-modes)
* **The workspace isn't trusted**: you haven't accepted the trust prompt for the directory
* **Mods are disabled**: you started with `--safe-mode` or `--bare`, you set `disableAllHooks`, or your organization's [managed settings block it](/docs/en/plugins/mods/admin#choose-how-much-to-allow)

## Write a mod yourself

In this tutorial you build a mod named `first-mod` that counts the tool calls Claude makes, shows the count beside the spinner while Claude works, and adds a `/tally` command that prints it. You then read the type declarations Claude Code writes beside your mod and run `claude plugin validate`. Together they show you the events and methods your version offers and what Claude Code reads from your code.

This recording shows the finished mod. The spinner counts tool calls, `/tally` prints the count, and an edit to the code takes effect while the session runs:

<Frame>
  <video autoPlay muted loop playsInline controls className="w-full dark:hidden" src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-first-mod-light.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=eb561134afa90375777408453ba51c77" aria-label="In a Claude Code session, the prompt 'list the files here and read the README' is typed and sent. The spinner reads 'Thinking · tool calls: 1' and the count rises as Claude works. The /tally command prints 'first-mod: Claude has made 3 tool calls since this mod loaded'. A line says first-mod reloaded and lists its four hooks. On the next prompt the spinner reads 'Thinking · tools used: 1'." data-path="images/mods-first-mod-light.mp4" />

  <video autoPlay muted loop playsInline controls className="w-full hidden dark:block" src="https://mintcdn.com/claude-code/dgiVO_Od1X1faduV/images/mods-first-mod-dark.mp4?fit=max&auto=format&n=dgiVO_Od1X1faduV&q=85&s=09779dadc7ef66c2b1e2da0c2e31ac72" aria-label="In a Claude Code session, the prompt 'list the files here and read the README' is typed and sent. The spinner reads 'Thinking · tool calls: 1' and the count rises as Claude works. The /tally command prints 'first-mod: Claude has made 3 tool calls since this mod loaded'. A line says first-mod reloaded and lists its four hooks. On the next prompt the spinner reads 'Thinking · tools used: 1'." data-path="images/mods-first-mod-dark.mp4" />
</Frame>

You write three files:

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
* **`register.js`**: your code, called the hooks module

<Steps>
  <Step title="Create the plugin directory">
    Create the two directories that hold the files:

    <Tabs>
      <Tab title="Bash or Zsh">
        ```bash theme={null}
        mkdir -p first-mod/.claude-plugin first-mod/hooks
        ```
      </Tab>

      <Tab title="PowerShell">
        ```powershell theme={null}
        New-Item -ItemType Directory -Force first-mod\.claude-plugin, first-mod\hooks
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Write the manifest">
    A mod is a plugin, and a mod needs a [manifest](/docs/en/plugins/manifest-reference). This mod's manifest has no special fields. Save this as `first-mod/.claude-plugin/plugin.json`:

    ```json first-mod/.claude-plugin/plugin.json theme={null}
    {
      "name": "first-mod",
      "version": "0.1.0",
      "description": "Counts Claude's tool calls, shows the count beside the spinner, and adds a /tally command",
      "author": { "name": "Your Name" }
    }
    ```
  </Step>

  <Step title="Tell Claude Code where your code is">
    When Claude Code loads a plugin, it reads the plugin's `hooks/hooks.json`. The `modules` key in that file gives the path to your code, and having it is what makes the plugin a mod. List one path, relative to `hooks.json`. Here it points to `register.js`, which you write in the next step.

    Save this as `first-mod/hooks/hooks.json`:

    ```json first-mod/hooks/hooks.json theme={null}
    {
      "description": "The first-mod hooks module",
      "modules": ["./register.js"]
    }
    ```
  </Step>

  <Step title="Write the code">
    This file is the mod's code, called the hooks module. When the mod loads, Claude Code calls the `register` function the file exports and passes it a function named [`on`](/docs/en/plugins/mods/reference#the-hook-function). Each call to `on` registers an event handler, called a hook, for the event it names.

    Save this as `first-mod/hooks/register.js`:

    ```javascript first-mod/hooks/register.js theme={null}
    // The count, shared by the hooks below
    let calls = 0

    // Claude Code calls this once when the mod loads
    export function register(on) {
      // Runs when the session starts, before your first prompt
      on('session.start', async ($, e, next) => {
        // Add the /tally command
        await $.command.register({
          name: 'tally',
          description: 'Show how many tool calls Claude has made',
        })
        // Let the session start as usual
        return next(e)
      })

      // Runs each time Claude is about to use a tool
      on('tool.call', async ($, e, next) => {
        calls += 1
        // Ask Claude Code to draw the interface again, so the new count shows
        $.ui.invalidate('ui.render')
        // Let the tool run as usual
        return next(e)
      })

      // Runs when you type /tally, and only then, because of the matcher
      on('command.run', { command: 'tally' }, async () => {
        // The text to print in the transcript
        return { text: 'Claude has made ' + calls + ' tool calls since this mod loaded' }
      })

      // Runs each time Claude Code draws the spinner
      on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
        // Keep Claude Code's spinner, with the count added after its word
        return next({ ...e, props: { ...e.props, suffix: ' · tool calls: ' + calls + '…' } })
      })
    }
    ```

    The file keeps a count in `calls` and registers four hooks:

    * **[`session.start`](/docs/en/plugins/mods/reference#session)** runs when the session starts, before your first prompt, and again each time the mod reloads. It adds the `/tally` command to Claude Code.
    * **[`tool.call`](/docs/en/plugins/mods/reference#tools)** runs each time Claude is about to use a tool. It adds one to `calls` and asks Claude Code to draw the interface again.
    * **[`command.run`](/docs/en/plugins/mods/reference#commands-and-configuration)** runs when you type `/tally`. It returns the text to print.
    * **[`ui.render`](/docs/en/plugins/mods/reference#interface)** runs each time Claude Code draws the spinner. It adds the count after the spinner's word.

    [How the example mod works](#how-the-example-mod-works) explains the three arguments each hook takes and what each one returns.
  </Step>

  <Step title="Load the mod">
    Start Claude Code with the `--plugin-dir` flag, which loads a plugin directory for one session without installing it:

    ```bash theme={null}
    claude --plugin-dir ./first-mod
    ```
  </Step>

  <Step title="Try the mod">
    Ask Claude to do something that takes a few tool calls, such as `list the files here and read the README`. While Claude works, the spinner's word is followed by a count that rises, as in `Thinking · tool calls: 2…`. When Claude finishes, type `/tally` and press Enter. The transcript shows `first-mod: Claude has made 2 tool calls since this mod loaded`, with your own count. Claude Code puts the plugin's name in front of the command's text.

    To check the command without an interactive session, run it in non-interactive mode:

    ```bash theme={null}
    claude -p "/tally" --plugin-dir ./first-mod
    ```

    ```text theme={null}
    first-mod: Claude has made 0 tool calls since this mod loaded
    ```

    If `/tally` isn't in the command list, the module didn't load. See [Find out why a mod does nothing](/docs/en/plugins/mods/troubleshoot#find-out-why-a-mod-does-nothing).
  </Step>

  <Step title="Change the code while the session runs">
    Leave the session open. In `register.js`, change `' · tool calls: '` to `' · tools used: '` in the `ui.render` hook and save. The highlighted line is the one that changes:

    ```javascript first-mod/hooks/register.js {4} theme={null}
      // Runs each time Claude Code draws the spinner
      on('ui.render', { component: 'Spinner' }, async ($, e, next) => {
        // Keep Claude Code's spinner, with the count added after its word
        return next({ ...e, props: { ...e.props, suffix: ' · tools used: ' + calls + '…' } })
      })
    ```

    A line in the transcript says `first-mod` reloaded and lists its hooks, and the next spinner uses the new text, as in `Thinking · tools used: 1…`.
  </Step>
</Steps>

### How the example mod works

Each function you pass to `on` is a hook, which is an event handler. Claude Code passes every hook the same three arguments:

* **The mods API**, named `$`: every method a mod can call to reach outside itself, in [namespaces](/docs/en/plugins/mods/reference#mods-api-methods) such as `$.ui` and `$.command`
* **The event**, named `e`: the [event's input](/docs/en/plugins/mods/reference#events) as plain data, such as a tool call's name and arguments
* **The next handler**, named [`next`](/docs/en/plugins/mods/events#how-a-hook-handles-an-event): a function that passes the event on to the other mods and then to Claude Code's own behavior, and returns the result

The hooks in `first-mod` handle their events in these ways:

* **Observe**: the `session.start` hook registers the command, and the `tool.call` hook counts the call and asks for a redraw. Both return `next(e)`, so the session starts and the tool runs as usual.
* **Answer**: the `command.run` hook returns its own result and never calls `next`. The second argument to `on`, `{ command: 'tally' }`, is a filter, called a [matcher](/docs/en/plugins/mods/events#filter-which-events-a-hook-handles), so the hook runs only for `/tally`.
* **Rewrite**: the `ui.render` hook calls `next` with a copy of `e` whose `suffix` holds the count, so Claude Code draws its usual spinner with your text after the word

Claude Code watches a directory loaded with `--plugin-dir` and hot-reloads the hooks module when a file in it changes. Each reload runs `register` again, so `calls` resets to `0` and `/tally` starts counting again. To keep a value across reloads, see [Keep state](/docs/en/plugins/mods/interface#keep-state).

## Keep working on a mod

Once a mod loads, you can have Claude change it, check your code against the type definitions for your version, list the events and calls Claude Code finds in it, and test it.

### Change a mod with Claude

To change a mod you already have, start the session with `--plugin-dir` pointed at the mod's directory, so that what Claude writes loads in the same session:

```bash theme={null}
claude --plugin-dir ./first-mod
```

Then ask for the change, for example `add a /tally-reset command to this mod that sets the tally back to zero`. Claude edits the hooks module, runs `claude plugin validate`, and fixes what it reports. A directory you load with `--plugin-dir` is a [protected path](/docs/en/permission-modes#protected-paths), so in `default` and `acceptEdits` modes you're asked to approve each of Claude's edits to the mod. The protected paths table gives the result for the other permission modes.

Files Claude saves during its turn reload when the turn ends, so you can try `/tally-reset` as soon as Claude finishes.

<h3 id="get-the-types-for-your-build">
  Get type definitions for your version
</h3>

Each time Claude Code loads or reloads a mod from a directory you pass to `--plugin-dir`, or a mod [Claude wrote for you](#ask-claude-for-a-mod), it writes TypeScript declaration files, ending in `.d.ts`, into `.claude-plugin/types/` inside the mod's directory. They describe the exact events, mods API methods, and elements in the Claude Code version you're running, so your editor can autocomplete and type-check your hooks. To browse the declarations online, read [`mods/types/claude-code.d.ts`](https://github.com/anthropics/claude-code/blob/main/mods/types/claude-code.d.ts) in the Claude Code repository, whose first line names the version that wrote it. The directory holds these files:

| Path | What it declares |
| :- | :- |
| `claude-code/index.d.ts` | Every event and its input and result, every mods API namespace and method, and the elements each surface can draw |
| `claude-code-tools/index.d.ts` | The built-in tools' inputs and results, so that checking `e.tool === 'Bash'` narrows `e` |
| `claude-code-mcp/index.d.ts` | The inputs of the MCP tools that were connected the last time you saved a file in the mod |
| `index.d.ts` in a directory named for a plugin | What that plugin adds to the mods API. There's one directory for each plugin your `plugin.json` lists under `dependencies`. |
| `tsconfig.json` | Compiler options that fit a hooks module |

If your mod has no `tsconfig.json` of its own, Claude Code adds one at the mod's root that extends the generated one, so your editor and `tsc -p ./first-mod` type-check the mod without more setup.

The events and methods can change between releases, so trust these files over any page, this one included, when they disagree.

`claude-code/index.d.ts` is the fullest reference for your build, with a comment and an example for every mods API method. To look something up, search the file for its name, such as `'tool.call'`.

### Check what Claude Code reads from your mod

To see your mod the way Claude Code sees it, without running your code or starting a session, use `claude plugin validate`. It checks the manifest and runs the same static analysis on the hooks module's source that Claude Code runs when it loads a mod. In your shell, run it on the mod's directory:

```bash theme={null}
claude plugin validate ./first-mod
```

For `first-mod`, the output includes these lines.

```text theme={null}
  ❯ ./register.js hooks: session.start, tool.call, command.run{command=tally}, ui.render{component=Spinner}
  ❯ ./register.js calls: $.command.register, $.ui.invalidate

✔ Validation passed
```

Check the `hooks:` line for the events your module hooks, each with its filter in braces, and `calls:` for every mods API method it calls. If your module reads or sets environment variables, look for `env reads:` and `env writes:` lines too, and `state reads:` and `state writes:` if it uses [`$.state`](/docs/en/plugins/mods/interface#keep-state). You also see one line for each hook that can refuse an action, such as `gating hook without .catch: tool.call`, which says whether that hook has a [`.catch` handler](/docs/en/plugins/mods/events#handle-a-hook-that-fails).

If an event you meant to handle is missing from the first line, Claude Code won't call that hook either. The usual cause is a misspelled event name, which the command reports as an error such as `"tool.calls" is not an event`.

Follow these rules so that static analysis can find every hook and call:

* Write each mods API call in full: `$`, the namespace, then the method, as in `$.store.get('notes')`. You can pass `$` to a function declared at the top level of the same file, and for a function of yours named `loadNotes`, the `calls:` line then reads `$.store.get (via loadNotes)`. Passing `$` to a method, a function defined inside the hook, or a function you import from another of your files fails validation. The `read` and `update` functions that [`$.state`](/docs/en/plugins/mods/interface#keep-state) uses are the imports that can take it. Don't assign `$` or one of its namespaces to a variable, destructure it, or index it with a computed name. `const ui = $.ui` fails with `$.ui is used as a value`.
* Write the event name in each `on` call as a string literal, such as `'tool.call'`. A variable, or a loop over a list of names, fails with `the event name passed to on() is not a string literal`.
* Inside `register`, don't declare a second variable or parameter named `on`. Validation fails with `"on" is declared again (shadowed)`.
* Import only from files inside the plugin directory, by relative path. The one bare import allowed is `claude-code`, for types and a few helpers.
* Use `import` declarations at the top of the file, as in `import { name } from './file.js'`. A dynamic `import()` fails with `a dynamic import(); a hooks module imports its own files with an import declaration`.
* Write every file as an ES module, with `import` and not `require`. The [reference](/docs/en/plugins/mods/reference#files) lists the file extensions Claude Code loads.

### Test the mod

You can write automated tests for a mod and run them from your shell with `claude plugin test`, with no session, sign-in, or network. A test fires the events your hooks handle and checks what the hooks did.

This test fires two tool calls, runs `/tally`, and checks that the reply counts both. Save it as `first-mod/tests/first-mod.test.ts`:

```typescript first-mod/tests/first-mod.test.ts theme={null}
import { expect, test } from 'claude-code/testing'

test('/tally reports the tool calls the mod has seen', async ($, on) => {
  // Answer each tool call in Claude Code's place, so no tool runs
  on('tool.call', () => ({ result: 'ok' }))

  // Fire two tool calls, which the mod's tool.call hook counts
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

[Test a mod](/docs/en/plugins/mods/test) covers stubbing a model call or the store, and testing timers and drawings.

## Share your mod

A mod is a plugin, so you version it in the manifest and people install and update it with the `/plugin` commands. How you share it depends on who it's for:

* **A few people**: send them the plugin's directory or a `.zip` of it. See [Share a plugin without a marketplace](/docs/en/plugins/publish#share-a-plugin-without-a-marketplace)
* **Your team**: list it in [your own marketplace](/docs/en/plugins/publish#publish-through-your-own-marketplace), such as a private repository with one directory for each plugin. To add that marketplace for everyone who works in a repository, [register it in the repository's settings](/docs/en/plugins/host-marketplace#register-the-marketplace-for-everyone-in-a-repository)
* **Your whole organization**: an administrator can [install your organization's mods](/docs/en/plugins/mods/admin#install-your-organizations-mods) through managed settings
* **Anyone**: make your marketplace's repository public, or [submit the plugin to Anthropic's directory](/docs/en/plugins/publish#submit-to-anthropics-directory)

Before you do, check the plugin's `name`: `claude plugin validate` fails a name that [looks like one of Anthropic's own](/docs/en/plugins/manifest-reference#name), such as one that starts with `claude-`. The events and methods can change between releases, so your README is the place to say which Claude Code version you tested with.

Keep developing against the directory with `--plugin-dir`, not against an installed copy. Claude Code caches an installed plugin by version, so your edits don't reach the installed copy until you increment the version and install again.

## Next steps

* [Draw in the interface](/docs/en/plugins/mods/interface): open a pane, draw above the prompt, and add buttons and text fields
* [React to events](/docs/en/plugins/mods/events): hook tool calls, prompts, and turns
* [Use the mods API](/docs/en/plugins/mods/api): add commands and tools, call a model, and run work on a timer
* [Test a mod](/docs/en/plugins/mods/test): stub what Claude Code would answer, and test timers and drawings
* [Troubleshoot a mod](/docs/en/plugins/mods/troubleshoot): the reasons a mod does nothing, and the debug log
* [Read the source of built-in mods](/docs/en/plugins/mods/overview#read-the-source-of-built-in-mods): complete plugins, each with its hooks module and tests
