> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Customize keyboard shortcuts

> Customize keyboard shortcuts in Claude Code with a keybindings configuration file.

Claude Code supports customizable keyboard shortcuts. Run `/keybindings` to create or open your configuration file at `~/.claude/keybindings.json`.

## Configuration file

The keybindings configuration file is an object with a `bindings` array. Each block specifies a context and a map of keystrokes to actions.

<Note>Changes to the keybindings file are automatically detected and applied without restarting Claude Code.</Note>

| Field      | Description                                        |
| :--------- | :------------------------------------------------- |
| `$schema`  | Optional JSON Schema URL for editor autocompletion |
| `$docs`    | Optional documentation URL                         |
| `bindings` | Array of binding blocks by context                 |

This example binds `Ctrl+E` to open an external editor in the chat context, and unbinds `Ctrl+U`:

```json theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## Contexts

Each binding block specifies a **context** where the bindings apply:

| Context           | Description                                                  |
| :---------------- | :----------------------------------------------------------- |
| `Global`          | Applies everywhere in the app                                |
| `Chat`            | Main chat input area                                         |
| `Autocomplete`    | Autocomplete menu is open                                    |
| `Settings`        | Settings menu                                                |
| `Confirmation`    | Permission and confirmation dialogs                          |
| `Tabs`            | Tab navigation components                                    |
| `Help`            | Help menu is visible                                         |
| `Transcript`      | Transcript viewer                                            |
| `HistorySearch`   | History search mode (Ctrl+R)                                 |
| `Task`            | Background task is running                                   |
| `ThemePicker`     | Theme picker dialog                                          |
| `Attachments`     | Image attachment navigation in select dialogs                |
| `Footer`          | Footer indicator navigation (tasks, teams, diff, artifacts)  |
| `MessageSelector` | Rewind and summarize dialog message selection                |
| `DiffDialog`      | Diff viewer navigation                                       |
| `ModelPicker`     | Model picker effort level                                    |
| `Select`          | Generic select/list components                               |
| `Plugin`          | Plugin dialog (browse, discover, manage)                     |
| `Scroll`          | Conversation scrolling and text selection in fullscreen mode |

Before v2.1.205, a `Doctor` context and a `doctor:fix` action existed for the `/doctor` diagnostics screen.

## Available actions

Actions follow a `namespace:action` format, such as `chat:submit` to send a message or `app:toggleTodos` to show the task list. Each context has specific actions available.

### App actions

Actions available in the `Global` context:

| Action                 | Default   | Description                                                                                                  |
| :--------------------- | :-------- | :----------------------------------------------------------------------------------------------------------- |
| `app:interrupt`        | Ctrl+C    | Cancel current operation                                                                                     |
| `app:exit`             | Ctrl+D    | Exit Claude Code. Press twice within 800ms to confirm                                                        |
| `app:redraw`           | (unbound) | Force terminal redraw                                                                                        |
| `app:toggleTodos`      | Ctrl+T    | Toggle visibility of Claude's to-do checklist. This is not the [`/tasks`](/docs/en/commands) background-task view |
| `app:toggleTranscript` | Ctrl+O    | Toggle verbose transcript                                                                                    |

### History actions

Actions for navigating command history:

| Action             | Default | Description           |
| :----------------- | :------ | :-------------------- |
| `history:search`   | Ctrl+R  | Open history search   |
| `history:previous` | Up      | Previous history item |
| `history:next`     | Down    | Next history item     |

### Chat actions

Actions available in the `Chat` context:

| Action                | Default                           | Description                                                                                                                                                                                                                                                                                              |
| :-------------------- | :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `chat:cancel`         | Escape                            | Cancel current input                                                                                                                                                                                                                                                                                     |
| `chat:clearInput`     | Ctrl+L                            | Force a full screen redraw, preserving input and conversation                                                                                                                                                                                                                                            |
| `chat:clearScreen`    | Cmd+K                             | Force a full screen redraw, preserving input and conversation. See [Clear the conversation](/docs/en/fullscreen#clear-the-conversation) for how Cmd+K behaves on iTerm2 and Terminal.app                                                                                                                      |
| `chat:killAgents`     | Ctrl+X Ctrl+K                     | Stop all running [background subagents](/docs/en/sub-agents#run-subagents-in-foreground-or-background) in this session and turn off [artifact auto-replies](/docs/en/artifacts#let-claude-reply-to-comments-on-its-own) for the rest of it                                                                         |
| `chat:cycleMode`      | Shift+Tab\*                       | Cycle permission modes                                                                                                                                                                                                                                                                                   |
| `chat:modelPicker`    | Meta+P                            | Open model picker                                                                                                                                                                                                                                                                                        |
| `chat:fastMode`       | Meta+O                            | Toggle fast mode                                                                                                                                                                                                                                                                                         |
| `chat:thinkingToggle` | Meta+T                            | Toggle extended thinking                                                                                                                                                                                                                                                                                 |
| `chat:submit`         | Enter                             | Submit message                                                                                                                                                                                                                                                                                           |
| `chat:queueSubmit`    | Ctrl+X Enter                      | Submit the message, marked to wait its turn: while Claude is working, Claude Code [queues it](/docs/en/interactive-mode#queue-messages-while-claude-works) and never interrupts the turn. Unlike `chat:submit`, it submits the draft even while autocomplete suggestions are open. Requires v2.1.247 or later |
| `chat:newline`        | Ctrl+J                            | Insert a newline without submitting                                                                                                                                                                                                                                                                      |
| `chat:undo`           | Ctrl+\_, Ctrl+Shift+-             | Undo last action                                                                                                                                                                                                                                                                                         |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E             | Open in external editor                                                                                                                                                                                                                                                                                  |
| `chat:stash`          | Ctrl+S                            | Stash current prompt                                                                                                                                                                                                                                                                                     |
| `chat:imagePaste`     | Ctrl+V (Alt+V on Windows and WSL) | Paste image from clipboard. On WSL, both shortcuts are bound by default                                                                                                                                                                                                                                  |

\*On Windows without VT mode (Node \<24.2.0/\<22.17.0, Bun \<1.2.23), defaults to Meta+M.

### Autocomplete actions

Actions available in the `Autocomplete` context:

| Action                  | Default | Description         |
| :---------------------- | :------ | :------------------ |
| `autocomplete:accept`   | Tab     | Accept suggestion   |
| `autocomplete:dismiss`  | Escape  | Dismiss menu        |
| `autocomplete:previous` | Up      | Previous suggestion |
| `autocomplete:next`     | Down    | Next suggestion     |

### Confirmation actions

Actions available in the `Confirmation` context:

| Action                      | Default     | Description                                                                                                                                                                                                                                                                           |
| :-------------------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `confirm:yes`               | Y, Enter    | Confirm action                                                                                                                                                                                                                                                                        |
| `confirm:no`                | N, Escape   | Decline action                                                                                                                                                                                                                                                                        |
| `confirm:previous`          | Up          | Previous option                                                                                                                                                                                                                                                                       |
| `confirm:next`              | Down        | Next option                                                                                                                                                                                                                                                                           |
| `confirm:nextField`         | Tab         | Next field                                                                                                                                                                                                                                                                            |
| `confirm:previousField`     | (unbound)   | Previous field                                                                                                                                                                                                                                                                        |
| `confirm:toggle`            | Space       | Toggle selection                                                                                                                                                                                                                                                                      |
| `confirm:cycleMode`         | Shift+Tab\* | Cycle permission modes. On a file permission prompt, closes an open [comment field](/docs/en/permissions#add-a-comment-when-you-answer-a-permission-prompt); with no field open, selects the option that allows the action for the rest of the session, when the prompt offers that option |
| `confirm:toggleExplanation` | Ctrl+E      | Toggle a model-generated [explanation of the command](/docs/en/permissions#permission-system) on Bash and PowerShell permission prompts                                                                                                                                                    |

\*On Windows without VT mode (Node \<24.2.0/\<22.17.0, Bun \<1.2.23), defaults to Meta+M.

### Permission actions

Actions available in the `Confirmation` context for permission dialogs:

| Action                   | Default   | Description                                                                                                         |
| :----------------------- | :-------- | :------------------------------------------------------------------------------------------------------------------ |
| `permission:toggleDebug` | (unbound) | Toggle permission debug info. The previous default of Ctrl+D was removed in v2.1.146 because it shadowed `app:exit` |

### Transcript actions

Actions available in the `Transcript` context:

| Action                     | Default           | Description             |
| :------------------------- | :---------------- | :---------------------- |
| `transcript:toggleShowAll` | Ctrl+E            | Toggle show all content |
| `transcript:exit`          | q, Ctrl+C, Escape | Exit transcript view    |

`transcript:toggleShowAll` applies in the classic renderer only; in [fullscreen rendering](/docs/en/fullscreen), the transcript viewer doesn't offer a show-all toggle.

### History search actions

Actions available in the `HistorySearch` context:

| Action                     | Default     | Description                               |
| :------------------------- | :---------- | :---------------------------------------- |
| `historySearch:next`       | Ctrl+R      | Next match                                |
| `historySearch:accept`     | Escape, Tab | Accept selection                          |
| `historySearch:cancel`     | Ctrl+C      | Cancel search                             |
| `historySearch:execute`    | Enter       | Execute selected command                  |
| `historySearch:cycleScope` | Ctrl+S      | Cycle scope: session, project, everywhere |

The `historySearch:next`, `historySearch:accept`, `historySearch:cancel`, and `historySearch:execute` defaults apply to the inline history search in the classic renderer, which always searches prompts from all projects. `historySearch:cycleScope` takes effect only in [fullscreen rendering](/docs/en/fullscreen), where `Ctrl+R` opens a search dialog instead and `Ctrl+S` cycles its scope. The dialog's other keys are fixed and can't be rebound: `Enter` or `Tab` places the highlighted match in the prompt input and `Esc` cancels.

### Task actions

Actions available in the `Task` context:

| Action            | Default               | Description                                                                                                     |
| :---------------- | :-------------------- | :-------------------------------------------------------------------------------------------------------------- |
| `task:background` | Ctrl+B, Ctrl+X Ctrl+B | Background current task. The Ctrl+X Ctrl+B chord requires v2.1.169 or later and avoids the tmux prefix conflict |

### Theme actions

Actions available in the `ThemePicker` context:

| Action                           | Default | Description                |
| :------------------------------- | :------ | :------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T  | Toggle syntax highlighting |

### Help actions

Actions available in the `Help` context:

| Action         | Default | Description     |
| :------------- | :------ | :-------------- |
| `help:dismiss` | Escape  | Close help menu |

### Tabs actions

Actions available in the `Tabs` context:

| Action          | Default         | Description  |
| :-------------- | :-------------- | :----------- |
| `tabs:next`     | Tab, Right      | Next tab     |
| `tabs:previous` | Shift+Tab, Left | Previous tab |

### Attachments actions

Actions available in the `Attachments` context:

| Action                 | Default           | Description                |
| :--------------------- | :---------------- | :------------------------- |
| `attachments:next`     | Right             | Next attachment            |
| `attachments:previous` | Left              | Previous attachment        |
| `attachments:remove`   | Backspace, Delete | Remove selected attachment |
| `attachments:exit`     | Down, Escape      | Exit attachment navigation |

### Footer actions

Actions available in the `Footer` context:

| Action                  | Default           | Description                                                                                                                                                                                   |
| :---------------------- | :---------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `footer:next`           | Right             | Next footer item                                                                                                                                                                              |
| `footer:previous`       | Left              | Previous footer item                                                                                                                                                                          |
| `footer:up`             | Up                | Navigate up in footer (deselects at top)                                                                                                                                                      |
| `footer:down`           | Down              | Navigate down in footer                                                                                                                                                                       |
| `footer:openSelected`   | Enter             | Open selected footer item                                                                                                                                                                     |
| `footer:clearSelection` | Escape            | Clear footer selection                                                                                                                                                                        |
| `footer:dismiss`        | Backspace, Delete | Dismiss the selected [artifact](/docs/en/artifacts) link from the footer; the published artifact itself is unaffected. On other footer rows, these keys have no effect. Requires v2.1.217 or later |

### Message selector actions

Actions available in the `MessageSelector` context:

| Action                   | Default                                   | Description       |
| :----------------------- | :---------------------------------------- | :---------------- |
| `messageSelector:up`     | Up, K, Ctrl+P                             | Move up in list   |
| `messageSelector:down`   | Down, J, Ctrl+N                           | Move down in list |
| `messageSelector:top`    | Ctrl+Up, Shift+Up, Meta+Up, Shift+K       | Jump to top       |
| `messageSelector:bottom` | Ctrl+Down, Shift+Down, Meta+Down, Shift+J | Jump to bottom    |
| `messageSelector:select` | Enter                                     | Select message    |

### Diff actions

Actions available in the `DiffDialog` context:

| Action                | Default   | Description                                                                                                                                         |
| :-------------------- | :-------- | :-------------------------------------------------------------------------------------------------------------------------------------------------- |
| `diff:dismiss`        | Escape    | Close diff viewer; from the detail view, returns to the file list instead                                                                           |
| `diff:previousSource` | Left      | Previous diff source                                                                                                                                |
| `diff:nextSource`     | Right     | Next diff source                                                                                                                                    |
| `diff:previousFile`   | Up, K     | Previous file in the file list; scroll up one line in the detail view                                                                               |
| `diff:nextFile`       | Down, J   | Next file in the file list; scroll down one line in the detail view                                                                                 |
| `diff:viewDetails`    | Enter     | View diff details                                                                                                                                   |
| `diff:back`           | (unbound) | Go back in diff viewer. Escape performs the back action via `diff:dismiss`. The previous default of Left in the detail view was removed in v2.1.203 |

The diff detail view also binds pager-style keys to the standard [scroll actions](#scroll-actions). These bindings are part of the `DiffDialog` context and apply only in the detail view; the `Scroll` context defaults listed under [Scroll actions](#scroll-actions) are unchanged.

| Action                | Default        | Description                 |
| :-------------------- | :------------- | :-------------------------- |
| `scroll:pageUp`       | PageUp         | Scroll up half a viewport   |
| `scroll:pageDown`     | PageDown       | Scroll down half a viewport |
| `scroll:fullPageUp`   | Shift+Space, B | Scroll up a full viewport   |
| `scroll:fullPageDown` | Space          | Scroll down a full viewport |
| `scroll:top`          | G, Home        | Jump to the top             |
| `scroll:bottom`       | Shift+G, End   | Jump to the bottom          |

### Model picker actions

Actions available in the `ModelPicker` context:

| Action                        | Default | Description                                  |
| :---------------------------- | :------ | :------------------------------------------- |
| `modelPicker:decreaseEffort`  | Left    | Decrease effort level                        |
| `modelPicker:increaseEffort`  | Right   | Increase effort level                        |
| `modelPicker:thisSessionOnly` | s       | Apply highlighted model to this session only |

### Select actions

Actions available in the `Select` context:

| Action            | Default         | Description                   |
| :---------------- | :-------------- | :---------------------------- |
| `select:next`     | Down, J, Ctrl+N | Next option                   |
| `select:previous` | Up, K, Ctrl+P   | Previous option               |
| `select:pageUp`   | PageUp          | Move up one page of options   |
| `select:pageDown` | PageDown        | Move down one page of options |
| `select:first`    | Home            | First option                  |
| `select:last`     | End             | Last option                   |
| `select:accept`   | Enter           | Accept selection              |
| `select:cancel`   | Escape          | Cancel selection              |

Claude Code applies your `select:pageUp`, `select:pageDown`, `select:first`, and `select:last` bindings in the `/skills` menu. In most other lists, such as the `/model` picker, Claude Code pages with PageUp and PageDown regardless of your bindings and ignores Home and End.

### Plugin actions

Actions available in the `Plugin` context:

| Action            | Default | Description                                                                |
| :---------------- | :------ | :------------------------------------------------------------------------- |
| `plugin:toggle`   | Space   | Toggle plugin selection                                                    |
| `plugin:install`  | I       | Install selected plugins                                                   |
| `plugin:favorite` | F       | Favorite the selected plugin so it sorts near the top of the Installed tab |

### Settings actions

Actions available in the `Settings` context. The `select:accept` and `confirm:no` actions are reused from the [Select](#select-actions) and [Confirmation](#confirmation-actions) contexts with Settings-specific behavior: changes apply to each setting as soon as you change it, so Escape closes the panel with your changes saved rather than declining.

| Action            | Default      | Description                                     |
| :---------------- | :----------- | :---------------------------------------------- |
| `settings:search` | /            | Enter search mode                               |
| `settings:retry`  | R            | Retry loading usage data on error               |
| `select:accept`   | Enter, Space | Change the selected setting or open its submenu |
| `confirm:no`      | Escape       | Close the panel. Changes are already saved      |

### Voice actions

Actions available in the `Chat` context when [voice dictation](/docs/en/voice-dictation) is enabled:

| Action             | Default | Description                                              |
| :----------------- | :------ | :------------------------------------------------------- |
| `voice:pushToTalk` | Space   | Dictate a prompt. Hold or tap depending on `/voice` mode |

### Scroll actions

Actions available in the `Scroll` context when [fullscreen rendering](/docs/en/fullscreen) is enabled:

| Action                      | Default              | Description                                                                                               |
| :-------------------------- | :------------------- | :-------------------------------------------------------------------------------------------------------- |
| `scroll:lineUp`             | `wheelup`            | Scroll up one line. Mouse wheel scrolling triggers this action                                            |
| `scroll:lineDown`           | `wheeldown`          | Scroll down one line. Mouse wheel scrolling triggers this action                                          |
| `scroll:pageUp`             | PageUp               | Scroll up half the viewport height                                                                        |
| `scroll:pageDown`           | PageDown             | Scroll down half the viewport height                                                                      |
| `scroll:top`                | Ctrl+Home            | Jump to the start of the conversation                                                                     |
| `scroll:bottom`             | Ctrl+End             | Jump to the latest message and re-enable auto-follow                                                      |
| `scroll:halfPageUp`         | (unbound)            | Scroll up half the viewport height. Same behavior as `scroll:pageUp`, provided for vi-style rebinds       |
| `scroll:halfPageDown`       | (unbound)            | Scroll down half the viewport height. Same behavior as `scroll:pageDown`, provided for vi-style rebinds   |
| `scroll:fullPageUp`         | (unbound)            | Scroll up the full viewport height                                                                        |
| `scroll:fullPageDown`       | (unbound)            | Scroll down the full viewport height                                                                      |
| `selection:copy`            | Ctrl+Shift+C / Cmd+C | Copy the selected text to the clipboard                                                                   |
| `selection:clear`           | (unbound)            | Clear the active text selection. Requires v2.1.234 or later                                               |
| `selection:extendLeft`      | Shift+Left           | Extend the active selection one column left                                                               |
| `selection:extendRight`     | Shift+Right          | Extend the active selection one column right                                                              |
| `selection:extendUp`        | Shift+Up             | Extend the active selection one row up. Scrolls the viewport when the selection reaches the top edge      |
| `selection:extendDown`      | Shift+Down           | Extend the active selection one row down. Scrolls the viewport when the selection reaches the bottom edge |
| `selection:extendLineStart` | Shift+Home           | Extend the active selection to the start of the line                                                      |
| `selection:extendLineEnd`   | Shift+End            | Extend the active selection to the end of the line                                                        |

## Keystroke syntax

### Modifiers

Use modifier keys with the `+` separator:

* `ctrl` or `control` - Control key
* `shift` - Shift key
* `alt`, `opt`, `option`, or `meta` - Alt key on Windows and Linux, Option key on macOS
* `cmd`, `command`, `super`, or `win` - Command key on macOS, Windows key on Windows, Super key on Linux

The `cmd` group is only detected in terminals that report the Super modifier, such as those supporting the Kitty keyboard protocol or xterm's `modifyOtherKeys` mode. Most terminals do not send it, so use `ctrl` or `meta` for bindings you want to work everywhere.

For example:

```text theme={null}
ctrl+k          Ctrl + K
shift+tab       Shift + Tab
meta+p          Option + P on macOS, Alt + P elsewhere
ctrl+shift+c    Multiple modifiers
```

### Uppercase letters

Claude Code parses key names case-insensitively, so `K` is the same binding as `k` and `ctrl+K` is the same as `ctrl+k`. To bind Shift and a letter, write `shift+k`.

### Non-US keyboard layouts

Write the key names of Ctrl shortcuts as Latin characters even when your active keyboard layout types other characters.

How Claude Code matches the key you press to a binding depends on the kind of layout:

* Under a non-Latin layout such as Cyrillic, Claude Code matches Ctrl shortcuts by the key's US-layout position when the terminal uses the Kitty keyboard protocol and reports that position. In such a terminal, with a Russian layout active, pressing Ctrl and the physical W key triggers `ctrl+w`. In a terminal that doesn't report the position, Claude Code matches whatever the terminal sends for the keypress: an ASCII control code triggers the Latin shortcut, and a keypress that arrives as the Cyrillic character matches no binding
* Under layouts that rearrange Latin letters, such as AZERTY, Claude Code matches the letter that the key types, so pressing Ctrl and the key labeled A triggers `ctrl+a`

Before v2.1.247, pressing a Ctrl shortcut under a non-Latin layout didn't trigger its binding in terminals that use the Kitty keyboard protocol, such as Ghostty, Kitty, WezTerm, and iTerm2.

### Chords

Chords are sequences of keystrokes separated by spaces:

```text theme={null}
ctrl+k ctrl+s   Press Ctrl+K, release, then Ctrl+S
```

### Special keys

* `escape` or `esc` - Escape key
* `enter` or `return` - Enter key
* `tab` - Tab key
* `space` - Space bar
* `up`, `down`, `left`, `right` - Arrow keys
* `pageup`, `pagedown` - Page Up and Page Down keys
* `home`, `end` - Home and End keys
* `backspace`, `delete` - Delete keys
* `wheelup`, `wheeldown` - Mouse wheel scroll events

## Unbind default shortcuts

Set an action to `null` to unbind a default shortcut:

```json theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

This also works for chord bindings. Unbinding every chord that shares a prefix frees that prefix for use as a single-key binding. A chord in any active context keeps its prefix reserved, so you must unbind each chord in the context that defines it.

Claude Code binds these default chords on the `ctrl+x` prefix: `ctrl+x ctrl+k`, `ctrl+x ctrl+e`, and `ctrl+x enter` in `Chat`, and `ctrl+x ctrl+b` in `Task`. The `ctrl+x enter` chord requires v2.1.247 or later. To reclaim `ctrl+x` itself as a single-key binding, unbind all of them:

```json theme={null}
{
  "bindings": [
    {
      "context": "Task",
      "bindings": {
        "ctrl+x ctrl+b": null
      }
    },
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x enter": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

If you unbind some but not all chords on a prefix, pressing the prefix still enters chord-wait mode for the remaining bindings.

## Reserved shortcuts

These shortcuts cannot be rebound:

| Shortcut  | Reason                                                                                                                                                                                                                                             |
| :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ctrl+C    | Hardcoded interrupt/cancel                                                                                                                                                                                                                         |
| Ctrl+D    | Hardcoded exit                                                                                                                                                                                                                                     |
| Ctrl+M    | Claude Code always receives it as Enter                                                                                                                                                                                                            |
| Ctrl+\[   | Claude Code always receives it as Escape                                                                                                                                                                                                           |
| Ctrl+I    | Claude Code always receives it as Tab                                                                                                                                                                                                              |
| Ctrl+H    | Sends the ASCII backspace byte. [How Claude Code reads it on Windows](/docs/en/terminal-config#fix-backspace-deleting-a-whole-word-on-windows) depends on your terminal and the [`CLAUDE_CODE_BS_AS_CTRL_BACKSPACE`](/docs/en/env-vars) environment variable |
| Caps Lock | Not delivered to terminal applications                                                                                                                                                                                                             |

## Terminal conflicts

Some shortcuts may conflict with terminal multiplexers:

| Shortcut | Conflict                          |
| :------- | :-------------------------------- |
| Ctrl+B   | tmux prefix (press twice to send) |
| Ctrl+A   | GNU screen prefix                 |
| Ctrl+Z   | Unix process suspend (SIGTSTP)    |

## Vim mode interaction

When vim mode is enabled via `/config` → Editor mode, keybindings and vim mode operate independently:

* **Vim mode** handles input at the text input level (cursor movement, modes, motions)
* **Keybindings** handle actions at the component level (toggle todos, submit, etc.)
* The Escape key in vim mode switches INSERT to NORMAL mode; it does not trigger `chat:cancel`
* Most Ctrl+key shortcuts pass through vim mode to the keybinding system
* Vim keys aren't remappable through the keybindings file. To map a two-key INSERT-mode sequence such as `jj` to Escape, use the [`vimInsertModeRemaps`](/docs/en/interactive-mode#remap-insert-mode-key-sequences) setting
* In vim NORMAL mode, `?` shows the help menu (vim behavior)
* In vim NORMAL mode, `/` opens history search, the same as Ctrl+R in standard mode

## Validation

Claude Code validates your keybindings and shows warnings for:

* Parse errors (invalid JSON or structure)
* Invalid context names
* Invalid action values, such as an action that isn't a string or `null`
* Unknown action names, such as a typo of a registered action. Claude Code skips the binding and keeps any default binding for that key in effect. Before v2.1.246, a binding with an unknown action name silently disabled that key
* Reserved shortcut conflicts
* Duplicate bindings in the same context

Claude Code reports warnings when the file loads and writes each one to the debug log. Start Claude Code with [`--debug`](/docs/en/cli-reference#cli-flags) to see the details.
