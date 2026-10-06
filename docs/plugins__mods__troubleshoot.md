> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshoot a mod

> Find out why a Claude Code mod does nothing: match the symptom or message to its cause, look up refusal messages, and read the debug log.

When a mod's module or one of its hooks fails, Claude Code skips it and the session continues, so a broken mod can look like one that does nothing. Start by checking what Claude Code read from your mod and where it reports a problem, then find the symptom or message you have.

## Find out why a mod does nothing

When a mod does nothing, check what Claude Code reads from the mod's files, and the line it writes when it skips something. For the first, in your shell run [`claude plugin validate`](/docs/en/plugins/mods/create#check-what-claude-code-reads-from-your-mod) with the mod's directory, as in `claude plugin validate ./first-mod`. It catches a misspelled event, a bad manifest, and a module Claude Code can't read, without starting a session.

When a module doesn't load, a hook is skipped, or another mod refuses yours, Claude Code writes one line that names your mod. Where you read that line depends on the session:

* **A session that hot-reloads a plugin directory**: a dim line in the transcript. That's an interactive session you started with `--plugin-dir`, or one where you [enabled hot reloading](/docs/en/plugins/mods/create#ask-claude-for-a-mod) for mods Claude wrote.
* **Any other interactive session, such as one that runs a mod you installed from a marketplace**: the [debug log](#read-the-debug-log) only. To get one, start the session with `claude --debug`.
* **A `claude -p` run with `--plugin-dir`**: stderr, in the default text output format. A refusal by another mod goes to the debug log only.

## Check whether mods can load

To check whether your setup lets mods load at all, without installing one, run `claude plugin test` in your shell, from a directory that doesn't hold a mod. You don't need a session. The message it prints tells you the state:

| Message includes | What it means |
| :- | :- |
| `no hooks module to load` | Mods can load. The command found no mod to test in this directory. |
| `hooks modules are turned off here` | A setting is blocking your mods: `disableAllHooks` in your own settings, or your organization's policy |
| `hooks modules are turned off in this process` | Anthropic has turned installed mods off remotely. No setting on your machine turns them back on. |

An organization can also set `allowManagedModsOnly` to allow only its own mods, which this command doesn't report. In that case a mod you install doesn't load, and [a message says why](/docs/en/plugins/mods/troubleshoot#messages-from-the-built-in-guard).

## The mod doesn't load

Nothing the mod adds appears: no command, no drawing, and no change in behavior.

### Your version is too old

See [which version to use and how to check yours](/docs/en/plugins/mods/overview#turn-mods-on-or-off).

### The `mods active` line doesn't name the mod

Nothing the mod adds appears, and the [`mods active` line](/docs/en/plugins/mods/overview#see-which-mods-a-session-loaded) in `/plugin` doesn't name it. The hooks module didn't load. When Claude Code refused it, the debug log has a line that starts with `hooks module`, the mod's name, and `not loaded:`, as in `hooks module first-mod@inline not loaded: disableAllHooks in managed settings` for a mod loaded with `--plugin-dir`.

Read the reason after the colon. The [refusal messages](#refusal-messages) section lists each one. If the log has no such line, work through the other entries in this group.

Some settings stop a mod and leave the rest of its plugin working. [Turn mods on or off](/docs/en/plugins/mods/overview#turn-mods-on-or-off) names them.

### A `claude -p` run prints `hooks module not loaded`

The line starts with the mod's name and goes to stderr. The hooks module was refused. A non-interactive run has no transcript, so the message goes to stderr.

Read the reason after the colon. The [refusal messages](#refusal-messages) section lists each one.

### Refusal messages

Each of these follows `hooks module`, the mod's name, and `not loaded:` in the debug log.

| Message starts with | What it means |
| :- | :- |
| `hooks modules are turned off for installed plugins in this process` | Anthropic has turned installed mods off remotely. No setting on your machine turns them back on. |
| `disableAllHooks in managed settings` | Your organization turned off hooks from installed plugins |
| `only managed plugins and built-in plugins run` | `allowManagedHooksOnly` is set, or `disableAllHooks` is set in a settings file other than managed settings |
| `installed plugins that are not managed load no hooks module in this mode (--bare)` | You started Claude Code with `--bare` |
| `another plugin of that name loads first` | Two plugins share a name. The managed one, or the one loaded first, is used. |

### Messages from the built-in guard

On a machine with managed settings, or for a user signed in with a Team or Enterprise plan, the [built-in guard](/docs/en/plugins/mods/admin#know-what-happens-by-default) can refuse a mod or one of its answers. Each message names the option your organization's administrator sets to change the rule.

| Message contains | What it means | Where it appears |
| :- | :- | :- |
| `mods are limited to your organization's by policy (allowManagedModsOnly)` | Your organization allows only [its own mods](/docs/en/plugins/mods/admin#install-your-organizations-mods), so yours wasn't loaded | The debug log, and the transcript in a [session that hot-reloads a plugin directory](#find-out-why-a-mod-does-nothing) |
| `tried to lift a deny rule in your settings` | Your mod's [`tool.check`](/docs/en/plugins/mods/reference#tools) hook approved a call that a `deny` rule refuses. The call stays denied. | The transcript and the debug log, once for each mod in a session. In a `claude -p` run, the debug log only. |
| `the deny rules in your settings could not be checked for this call, so it is refused` | The guard failed while checking a call that a mod approved, so it refused the call | The reason Claude reads for the denied call |

### `validate` passes and lists no `hooks` line

`hooks/hooks.json` has no `modules` key, or the key is misspelled.

Add `"modules": ["./register.js"]`.

### `hooks module did not load`

The line starts with the mod's name, then `hooks module did not load:` and a reason, which gives the file and line when the problem is in your code. Claude Code couldn't load the module, for example because its top-level code threw.

Fix the error the reason names.

### `options do not fit plugin.json userConfig`

The line starts with the mod's name, then `hooks module did not load: options do not fit plugin.json userConfig:` and a reason. An option fails validation against its [`userConfig`](/docs/en/plugins/components#user-configuration) field, such as a number above the field's `max`, or a required field has no value.

Set or change the value. The end of the line names its `pluginConfigs` entry in `settings.json`.

### No mod loads in a directory you opened for the first time

You haven't answered the trust prompt for the directory.

Start an interactive session in that directory with `claude`, and accept the trust prompt it opens with.

### No installed plugin loads at all

You started Claude Code with `--safe-mode`.

Start without the flag.

## A hook is skipped or a mod is unloaded

The mod loaded, and then Claude Code skipped one of its hooks or unloaded it.

### `hook skipped`

The line names the mod and the event, then says `hook skipped:` and a reason, as in `first-mod: tool.call hook skipped: threw Error: boom`. A hook threw, exceeded its [time limit](/docs/en/plugins/mods/reference#limits), or returned a result of the wrong shape. The line appears once for each event and kind of failure until the mod reloads.

Fix the error. The debug log has a line for every occurrence.

### `no command.run hook answered it`

You run a command your mod added, and the reply names the mod and the command, as in `first-mod registered /tally but no command.run hook answered it`, then tells you to add a hook. Claude Code prints that reply when the command reaches the end of the chain with no answer, which happens in two cases:

* **No hook answered the command**: the module has no `command.run` hook, the hook's [filter](/docs/en/plugins/mods/events#filter-which-events-a-hook-handles) names a different command, or the hook returned `next(e)`
* **Claude Code skipped the hook**: [`hook skipped`](#hook-skipped) lists the reasons. Passing `focus: false` to [`$.ui.open`](/docs/en/plugins/mods/interface#open-a-pane-at-the-right-time) is one way to get there.

If the module already has the hook the reply describes, look for a `hook skipped` line that names `command.run`, which gives the reason. A [test](/docs/en/plugins/mods/test) that runs the command fails with the same reason.

### `it crashed the hooks worker`

The line starts with the mod's name, as in `first-mod was unloaded: it crashed the hooks worker`. Installed mods share one worker thread. The worker stopped responding or crashed, and Claude Code traced that to this mod and unloaded it. A hook that blocks the thread, such as a loop that never awaits, is one cause.

Fix the hook.

### `mods that run in the hooks worker are off for this session`

The line reads `hooks: mods that run in the hooks worker are off for this session: it crashed 3 times`. The worker stopped three times and Claude Code couldn't trace the stops to one mod, so it unloaded every mod that isn't built in, including mods your organization installs. This line reaches the transcript in every interactive session.

Run `/reload-plugins` to load them again.

## A tool call is denied

The mod loaded and its hooks run, and a tool call it touched is refused.

### `a hook changed this call's input after the model wrote it`

In auto mode, a denied tool call gives this reason. A hook changed the tool call's input after the [server-side classifier](/docs/en/permission-modes#server-side-classifier-review) reviewed it, so that review doesn't cover what would run. The hook can be a mod's [`tool.call`](/docs/en/plugins/mods/reference#tools) or [`turn.step`](/docs/en/plugins/mods/reference#turns) hook, or a [`PreToolUse`](/docs/en/hooks#pretooluse) settings hook. The message doesn't say which.

The message tells Claude to issue the call once more as recorded. If that's denied too, the hook changes the input every time, so turn off the mod or hook, or leave auto mode and approve the call yourself.

### A message about the deny rules in your settings

`tried to lift a deny rule in your settings` and `the deny rules in your settings could not be checked for this call, so it is refused` both come from the built-in guard.

Look them up in [Messages from the built-in guard](#messages-from-the-built-in-guard).

## A drawing doesn't appear or respond

The mod loaded, and its pane, band, or controls don't behave as you expect.

### A pane or band is empty or shows Claude Code's usual content

The [tree](/docs/en/plugins/mods/interface#build-a-tree-from-elements) your hook returned didn't validate. With `--plugin-dir`, the transcript says `ui.render (Pane) refused:` with the reason, as in `first-mod: ui.render (Pane) refused: Box prop "flexDirection" must be one of row, column, row-reverse, column-reverse; the engine drew its own`. The debug log has `a hook returned a tree that does not validate` with the same reason.

Read the reason on that line. Common causes are a prop the element doesn't take and an element the app doesn't have.

### `$.ui.open` runs and no pane appears

The call didn't come from something the user did, and the terminal is narrower than [the width that pane needs](/docs/en/plugins/mods/interface#when-a-pane-waits-for-a-wider-terminal).

Open the pane from a command or a button, or check the call's `isPlaced` result. See [Open a pane at the right time](/docs/en/plugins/mods/interface#open-a-pane-at-the-right-time).

### Hotkeys do nothing

Your pane doesn't have keyboard focus.

Press Ctrl+X then Tab, or click the pane. Open it with `focus: true` from a command.

### A drawing works in the terminal and not in the Desktop app

The site or element isn't available there.

Check the [render sites](/docs/en/plugins/mods/reference#render-sites) and [elements](/docs/en/plugins/mods/reference#elements) tables.

## An edit or a value is lost

The mod runs, and a change you made or a value it kept isn't there.

### Your edits don't take effect

You're editing a plugin you installed. Claude Code runs the cached copy for the installed version.

Develop with `--plugin-dir` pointed at your working copy, as in `claude --plugin-dir ./first-mod`, which reloads when you save.

### A value resets when the module reloads

Module-level variables are re-initialized on each reload.

[Keep the value in `$.state` or `$.store`](/docs/en/plugins/mods/interface#keep-state).

### A value resets after `/clear`, `/resume`, or `/branch`

A value resets, or a saved value is replaced by its default. Each of those commands resets `$.state` to its defaults, and `session.start` doesn't fire again.

[Load the saved value again](/docs/en/plugins/mods/interface#load-a-saved-value-again-after-clear) in a `classic.SessionStart` hook.

## Read the debug log

The debug log has a line for every module Claude Code loads or refuses, every hook that fails, and every result it refuses, so it's where to look when the transcript shows nothing. To write one, in your shell start Claude Code with `--debug`, or with `--debug-file <path>` to choose where it goes:

```bash theme={null}
claude --debug-file ./mod-debug.log --plugin-dir ./first-mod
```

In another terminal, follow the file and filter for your mod's name:

```bash theme={null}
tail -f ./mod-debug.log | grep first-mod
```

A mod that loaded has a line that names it and lists the events it handles. A mod loaded with `--plugin-dir` appears under its name followed by `@inline`:

```text theme={null}
hooks module first-mod@inline loaded (worker, environment 2, tier user); events: session.start,tool.call,command.run,ui.render
```

A drawing that didn't validate counts as a refused result and gets a line too. To write your own lines in the log, call [`$.ui.log`](/docs/en/plugins/mods/api#show-something-without-starting-a-turn) with a second argument, as in `$.ui.log('message', { to: 'debug' })`. Without the second argument, `$.ui.log` adds a dim line to the transcript.

While you edit a mod loaded with `--plugin-dir`, the transcript shows a line for each reload that names the mod and lists its hooks. If a save breaks the module, the line says `reload failed, the previous version stays loaded:` with the reason, and the last working version keeps running.

## Next steps

* [Test a mod](/docs/en/plugins/mods/test): catch problems before they reach a session
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting): problems with installing and loading a plugin that aren't specific to mods
