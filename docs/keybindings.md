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

```json  theme={null}
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

| Context           | Description                                      |
| :---------------- | :----------------------------------------------- |
| `Global`          | Applies everywhere in the app                    |
| `Chat`            | Main chat input area                             |
| `Autocomplete`    | Autocomplete menu is open                        |
| `Settings`        | Settings menu (escape-only dismiss)              |
| `Confirmation`    | Permission and confirmation dialogs              |
| `Tabs`            | Tab navigation components                        |
| `Help`            | Help menu is visible                             |
| `Transcript`      | Transcript viewer                                |
| `HistorySearch`   | History search mode (Ctrl+R)                     |
| `Task`            | Background task is running                       |
| `ThemePicker`     | Theme picker dialog                              |
| `Attachments`     | Image/attachment bar navigation                  |
| `Footer`          | Footer indicator navigation (tasks, teams, diff) |
| `MessageSelector` | Rewind dialog message selection                  |
| `DiffDialog`      | Diff viewer navigation                           |
| `ModelPicker`     | Model picker effort level                        |
| `Select`          | Generic select/list components                   |
| `Plugin`          | Plugin dialog (browse, discover, manage)         |

## Available actions

Actions follow a `namespace:action` format, such as `chat:submit` to send a message or `app:toggleTodos` to show the task list. Each context has specific actions available.

### App actions

Actions available in the `Global` context:

| Action                 | Default | Description                 |
| :--------------------- | :------ | :-------------------------- |
| `app:interrupt`        | Ctrl+C  | Cancel current operation    |
| `app:exit`             | Ctrl+D  | Exit Claude Code            |
| `app:toggleTodos`      | Ctrl+T  | Toggle task list visibility |
| `app:toggleTranscript` | Ctrl+O  | Toggle verbose transcript   |

### History actions

Actions for navigating command history:

| Action             | Default | Description           |
| :----------------- | :------ | :-------------------- |
| `history:search`   | Ctrl+R  | Open history search   |
| `history:previous` | Up      | Previous history item |
| `history:next`     | Down    | Next history item     |

### Chat actions

Actions available in the `Chat` context:

| Action                | Default                   | Description              |
| :-------------------- | :------------------------ | :----------------------- |
| `chat:cancel`         | Escape                    | Cancel current input     |
| `chat:cycleMode`      | Shift+Tab\*               | Cycle permission modes   |
| `chat:modelPicker`    | Cmd+P / Meta+P            | Open model picker        |
| `chat:thinkingToggle` | Cmd+T / Meta+T            | Toggle extended thinking |
| `chat:submit`         | Enter                     | Submit message           |
| `chat:undo`           | Ctrl+\_                   | Undo last action         |
| `chat:externalEditor` | Ctrl+G                    | Open in external editor  |
| `chat:stash`          | Ctrl+S                    | Stash current prompt     |
| `chat:imagePaste`     | Ctrl+V (Alt+V on Windows) | Paste image              |

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

| Action                      | Default   | Description                   |
| :-------------------------- | :-------- | :---------------------------- |
| `confirm:yes`               | Y, Enter  | Confirm action                |
| `confirm:no`                | N, Escape | Decline action                |
| `confirm:previous`          | Up        | Previous option               |
| `confirm:next`              | Down      | Next option                   |
| `confirm:nextField`         | Tab       | Next field                    |
| `confirm:previousField`     | (unbound) | Previous field                |
| `confirm:cycleMode`         | Shift+Tab | Cycle permission modes        |
| `confirm:toggleExplanation` | Ctrl+E    | Toggle permission explanation |

### Permission actions

Actions available in the `Confirmation` context for permission dialogs:

| Action                   | Default | Description                  |
| :----------------------- | :------ | :--------------------------- |
| `permission:toggleDebug` | Ctrl+D  | Toggle permission debug info |

### Transcript actions

Actions available in the `Transcript` context:

| Action                     | Default        | Description             |
| :------------------------- | :------------- | :---------------------- |
| `transcript:toggleShowAll` | Ctrl+E         | Toggle show all content |
| `transcript:exit`          | Ctrl+C, Escape | Exit transcript view    |

### History search actions

Actions available in the `HistorySearch` context:

| Action                  | Default     | Description              |
| :---------------------- | :---------- | :----------------------- |
| `historySearch:next`    | Ctrl+R      | Next match               |
| `historySearch:accept`  | Escape, Tab | Accept selection         |
| `historySearch:cancel`  | Ctrl+C      | Cancel search            |
| `historySearch:execute` | Enter       | Execute selected command |

### Task actions

Actions available in the `Task` context:

| Action            | Default | Description             |
| :---------------- | :------ | :---------------------- |
| `task:background` | Ctrl+B  | Background current task |

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
| `attachments:exit`     | Down, Escape      | Exit attachment bar        |

### Footer actions

Actions available in the `Footer` context:

| Action                  | Default | Description               |
| :---------------------- | :------ | :------------------------ |
| `footer:next`           | Right   | Next footer item          |
| `footer:previous`       | Left    | Previous footer item      |
| `footer:openSelected`   | Enter   | Open selected footer item |
| `footer:clearSelection` | Escape  | Clear footer selection    |

### Message selector actions

Actions available in the `MessageSelector` context:

| Action                   | Default                                   | Description       |
| :----------------------- | :---------------------------------------- | :---------------- |
| `messageSelector:up`     | Up, K                                     | Move up in list   |
| `messageSelector:down`   | Down, J                                   | Move down in list |
| `messageSelector:top`    | Ctrl+Up, Shift+Up, Meta+Up, Shift+K       | Jump to top       |
| `messageSelector:bottom` | Ctrl+Down, Shift+Down, Meta+Down, Shift+J | Jump to bottom    |
| `messageSelector:select` | Enter                                     | Select message    |

### Diff actions

Actions available in the `DiffDialog` context:

| Action                | Default            | Description            |
| :-------------------- | :----------------- | :--------------------- |
| `diff:dismiss`        | Escape             | Close diff viewer      |
| `diff:previousSource` | Left               | Previous diff source   |
| `diff:nextSource`     | Right              | Next diff source       |
| `diff:previousFile`   | Up                 | Previous file in diff  |
| `diff:nextFile`       | Down               | Next file in diff      |
| `diff:viewDetails`    | Enter              | View diff details      |
| `diff:back`           | (context-specific) | Go back in diff viewer |

### Model picker actions

Actions available in the `ModelPicker` context:

| Action                       | Default | Description           |
| :--------------------------- | :------ | :-------------------- |
| `modelPicker:decreaseEffort` | Left    | Decrease effort level |
| `modelPicker:increaseEffort` | Right   | Increase effort level |

### Select actions

Actions available in the `Select` context:

| Action            | Default         | Description      |
| :---------------- | :-------------- | :--------------- |
| `select:next`     | Down, J, Ctrl+N | Next option      |
| `select:previous` | Up, K, Ctrl+P   | Previous option  |
| `select:accept`   | Enter           | Accept selection |
| `select:cancel`   | Escape          | Cancel selection |

### Plugin actions

Actions available in the `Plugin` context:

| Action           | Default | Description              |
| :--------------- | :------ | :----------------------- |
| `plugin:toggle`  | Space   | Toggle plugin selection  |
| `plugin:install` | I       | Install selected plugins |

### Settings actions

Actions available in the `Settings` context:

| Action            | Default | Description                         |
| :---------------- | :------ | :---------------------------------- |
| `settings:search` | /       | Enter search mode                   |
| `settings:retry`  | R       | Retry loading usage data (on error) |

## Keystroke syntax

### Modifiers

Use modifier keys with the `+` separator:

* `ctrl` or `control` - Control key
* `alt`, `opt`, or `option` - Alt/Option key
* `shift` - Shift key
* `meta`, `cmd`, or `command` - Meta/Command key

For example:

```
ctrl+k          Single key with modifier
shift+tab       Shift + Tab
meta+p          Command/Meta + P
ctrl+shift+c    Multiple modifiers
```

### Uppercase letters

A standalone uppercase letter implies Shift. For example, `K` is equivalent to `shift+k`. This is useful for vim-style bindings where uppercase and lowercase keys have different meanings.

Uppercase letters with modifiers (e.g., `ctrl+K`) are treated as stylistic and do **not** imply Shift — `ctrl+K` is the same as `ctrl+k`.

### Chords

Chords are sequences of keystrokes separated by spaces:

```
ctrl+k ctrl+s   Press Ctrl+K, release, then Ctrl+S
```

### Special keys

* `escape` or `esc` - Escape key
* `enter` or `return` - Enter key
* `tab` - Tab key
* `space` - Space bar
* `up`, `down`, `left`, `right` - Arrow keys
* `backspace`, `delete` - Delete keys

## Unbind default shortcuts

Set an action to `null` to unbind a default shortcut:

```json  theme={null}
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

## Reserved shortcuts

These shortcuts cannot be rebound:

| Shortcut | Reason                     |
| :------- | :------------------------- |
| Ctrl+C   | Hardcoded interrupt/cancel |
| Ctrl+D   | Hardcoded exit             |

## Terminal conflicts

Some shortcuts may conflict with terminal multiplexers:

| Shortcut | Conflict                          |
| :------- | :-------------------------------- |
| Ctrl+B   | tmux prefix (press twice to send) |
| Ctrl+A   | GNU screen prefix                 |
| Ctrl+Z   | Unix process suspend (SIGTSTP)    |

## Vim mode interaction

When vim mode is enabled (`/vim`), keybindings and vim mode operate independently:

* **Vim mode** handles input at the text input level (cursor movement, modes, motions)
* **Keybindings** handle actions at the component level (toggle todos, submit, etc.)
* The Escape key in vim mode switches INSERT to NORMAL mode; it does not trigger `chat:cancel`
* Most Ctrl+key shortcuts pass through vim mode to the keybinding system
* In vim NORMAL mode, `?` shows the help menu (vim behavior)

## Validation

Claude Code validates your keybindings and shows warnings for:

* Parse errors (invalid JSON or structure)
* Invalid context names
* Reserved shortcut conflicts
* Terminal multiplexer conflicts
* Duplicate bindings in the same context

Run `/doctor` to see any keybinding warnings.
