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
| `hooks modules are turned off in this process: the rollout switch served off` | Anthropic has turned installed mods off remotely. |
| `hooks modules are turned off in this process: the rollout switch was saved off by an earlier session` | The command used a value an earlier session saved, which may be out of date. Start `claude` once to refresh it, then run the command again. |

An organization can also set `allowManagedModsOnly` to allow only its own mods, which this command doesn't report. In that case Claude Code refuses a mod you install, and [a message says why](/docs/en/plugins/mods/troubleshoot#messages-from-the-built-in-guard).

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
| `hooks modules are turned off for installed plugins in this process: the rollout switch served off` | Anthropic has turned installed mods off remotely. |
| `hooks modules are turned off for installed plugins in this process: the rollout switch was saved off by an earlier session` | The session used a value an earlier session saved, which may be out of date. Start Claude Code again to refresh it. |
| `disableAllHooks in managed settings` | Your organization turned off hooks from installed plugins |
| `only managed plugins and built-in plugins run` | `allowManagedHooksOnly` is set, or `disableAllHooks` is set in a settings file other than managed settings |
| `installed plugins that are not managed load no hooks module in this mode (--bare)` | You started Claude Code with `--bare` |
| `another plugin of that name loads first` | Another enabled plugin has the same name as your mod and [holds the name](/docs/en/plugins/loading#hooks-when-two-enabled-plugins-share-a-name), so your hooks module doesn't load |

### Messages from the built-in guard

On a machine with managed settings, or for a user signed in with a Team or Enterprise plan, the [built-in guard](/docs/en/plugins/mods/admin#know-what-happens-by-default) can refuse a mod or one of its answers. Each message names the option your organization's administrator sets to change the rule.

| Message contains | What it means | Where it appears |
| :- | :- | :- |
| `mods are limited to your organization's by policy (allowManagedModsOnly)` | Your organization allows only [its own mods](/docs/en/plugins/mods/admin#install-your-organizations-mods), so yours was refused | The debug log, and the transcript in a [session that hot-reloads a plugin directory](#find-out-why-a-mod-does-nothing) |
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

### `code nested too deep to scan: more than 2000 scopes`

The line starts with the mod's name, then `hooks module did not load:`, the file, and `code nested too deep to scan: more than 2000 scopes`. A file in a hooks module can't nest scopes, such as functions, blocks, and loops, more than [2,000 deep](/docs/en/plugins/mods/reference#limits). [`claude plugin validate`](/docs/en/plugins/mods/create#check-what-claude-code-reads-from-your-mod) reports the same reason.

Rewrite the code so its scopes nest less deeply.

### No mod loads in a directory you opened for the first time

You haven't answered the trust prompt for the directory.

Start an interactive session in that directory with `claude`, and accept the trust prompt it opens with.

### No installed plugin loads at all

You started Claude Code with `--safe-mode`.

Start without the flag.

### Claude Code stops asking to enable hot reloading

Claude writes a mod in an interactive session, nothing loads, and Claude Code doesn't ask again [whether to enable hot reloading](/docs/en/plugins/mods/create#ask-claude-for-a-mod). If the question ends three times without an answer picked, hot reloading stays off. For example, the question ends that way when you set [`askUserQuestionTimeout`](/docs/en/settings-reference#askuserquestiontimeout) and the time passes before you answer. That setting applies here because Claude Code asks in the same [question dialog that `AskUserQuestion` uses](/docs/en/tools-reference#question-auto-continue-timeout). A question you dismiss yourself doesn't count toward the three.

To run the mod, [copy its directory out of the mods folder](/docs/en/plugins/mods/create#use-the-mod-in-other-sessions), then in your shell start a new session with `--plugin-dir`, as in `claude --plugin-dir ~/mods/git-branch`.

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

### `its session.start ran again in a fresh copy`

The line starts with the mod's name and names a `$.prompt.submit`, `$.command.run`, or `$.agent.spawn` call, as in `first-mod: its session.start ran again in a fresh copy; the $.prompt.submit call it had already made was not made again`. Claude Code loaded the mod's module again, for example after the hooks worker crashed and was replaced, and the fresh copy's [`session.start`](/docs/en/plugins/mods/reference#session) hook ran. The call the line names resolved with the result of its first run instead of running again, so your mod doesn't submit the prompt, run the command, or start the subagent twice. The rest of the hook ran as usual.

There's nothing to fix.

Before v2.1.292, the call ran a second time, so the prompt was submitted, the command run, or the subagent started twice.

### `$.agent.register refused: the hooks module that made the call is no longer loaded`

The line starts with your mod's name, as in `first-mod: $.agent.register refused: the hooks module that made the call is no longer loaded (it was reloaded or removed)`, and the agent isn't registered. Your mod was reloaded or unloaded before the call. A reload loads a fresh copy of the hooks module, and this call came from code still running in the old copy, such as a hook that hadn't returned yet.

If that hook doesn't catch the rejection, it fails and Claude Code [skips it](#hook-skipped). To register the agent from the copy that stays loaded, make the call in your [`session.start`](/docs/en/plugins/mods/reference#session) hook, which runs again in each fresh copy after a reload.

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

The mod loaded, and its pane, band, toast, or controls don't behave as you expect.

### A pane or band is empty or shows Claude Code's usual content

The [tree](/docs/en/plugins/mods/interface#build-a-tree-from-elements) your hook returned didn't validate. With `--plugin-dir`, the transcript says `ui.render (Pane) refused:` with the reason, as in `first-mod: ui.render (Pane) refused: Box prop "flexDirection" must be one of row, column, row-reverse, column-reverse; the engine drew its own`. The debug log has `a hook returned a tree that does not validate` with the same reason.

Read the reason on that line. Common causes are a prop the element doesn't take and an element the app doesn't have.

### A `ui.render` line says `threw while drawn`

The line names the [render site](/docs/en/plugins/mods/reference#render-sites), then says `threw while drawn:` and the error, as in `first-mod: ui.render (ToolUse) threw while drawn: <error>; the engine drew its own`. Claude Code hit that error while drawing the tree your [`ui.render`](/docs/en/plugins/mods/reference#interface) hook returned, or while drawing the site from the [`props` your hook passed to `next`](/docs/en/plugins/mods/interface#change-what-claude-code-already-draws). The ending `the engine drew its own` means the site shows Claude Code's usual content.

Read the error and fix the value in your hook that caused it.

Before v2.1.289, this error in a transcript row ended the session with [`Claude Code exited after an unrecoverable interface error`](/docs/en/errors#exited-after-an-unrecoverable-interface-error).

### `the module failed without a message`

A [`Client`](/docs/en/plugins/mods/interface#when-a-client-fails) failed with an error that has no message, such as `throw new Error()`. The line in its place reads like `my-mod: Client client/spinner.js: the module failed without a message`.

Find the throw in your `Client`'s code and give the error a message. The line then shows that message.

Before v2.1.289, the line showed `Error` as the reason instead.

### `$.ui.open` runs and no pane appears

The call didn't come from something the user did, and the terminal is narrower than [the width that pane needs](/docs/en/plugins/mods/interface#when-a-pane-waits-for-a-wider-terminal).

Open the pane from a command or a button, or check the call's `isPlaced` result. See [Open a pane at the right time](/docs/en/plugins/mods/interface#open-a-pane-at-the-right-time).

### A toast doesn't appear

Your mod calls [`$.ui.toast`](/docs/en/plugins/mods/api#show-something-without-starting-a-turn) in an interactive terminal session and you don't see the toast. To confirm that the call ran, look in the [debug log](#read-the-debug-log) for a line with your mod's name and the toast's text, as in `$.ui.toast (first-mod): build finished`. Then check for causes such as these:

* **The line for the call is missing**: look for one that says why Claude Code refused the call, as in `first-mod: $.ui.toast dropped: timeoutMs is a whole number of ms, 1 to 60000`.
* **A pane is holding toasts**: your mod or another one passed [`holdToasts`](/docs/en/plugins/mods/interface#hold-toasts-behind-a-dialog) when it opened the pane that's showing. Close the pane to end the hold. If the pane is yours and is meant to stay open, remove `holdToasts` from its `$.ui.open` call and open the pane again.
* **The toast is under the prompt**: in the [classic renderer](/docs/en/fullscreen#enable-fullscreen-rendering), look at the right under the prompt. A toast there is one line that starts with the mod's name, rather than a box at the top right.
* **Your mod raised a newer toast**: in the classic renderer, a newer toast from your mod can take the place of one that's showing or waiting to show. The debug log has another line for the older toast, which ends with `gave way, cut short` when it was showing, or `gave way, unseen` when it never appeared. To show both messages, put them in one toast.
* **The toast ran out of time undrawn**: in fullscreen rendering, Claude Code draws at most three toasts at a time, so a toast can run out of time before it's drawn. The debug log has another line for that toast, which ends with `left the stack, never drawn`. When your mod raises several at once, put the messages in one toast.

Before v2.1.290, Claude Code dropped a toast raised within two seconds of the last one it showed for your mod, and the debug log line for the dropped toast said `within 2000ms of the last; dropped`.

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

While you edit a mod loaded with `--plugin-dir`, the transcript shows a line for each reload that names the mod and lists its hooks. If a save breaks the module, the line says `reload failed, the previous version stays loaded:` with the reason, and the last working version keeps running until Claude Code next reloads plugins, such as when you run `/reload-plugins`.

## Next steps

* [Test a mod](/docs/en/plugins/mods/test): catch problems before they reach a session
* [Troubleshoot plugins](/docs/en/plugins/troubleshooting): problems with installing and loading a plugin that aren't specific to mods
