# Interactive mode

> Complete reference for keyboard shortcuts, input modes, and interactive features in Claude Code sessions.

## Keyboard shortcuts

<Note>
  Keyboard shortcuts may vary by platform and terminal. Press `?` to see available shortcuts for your environment.

  **macOS users**: Option/Alt key shortcuts (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) require configuring Option as Meta in your terminal:

  * **iTerm2**: Settings → Profiles → Keys → Set Left/Right Option key to "Esc+"
  * **Terminal.app**: Settings → Profiles → Keyboard → Check "Use Option as Meta Key"
  * **VS Code**: Settings → Profiles → Keys → Set Left/Right Option key to "Esc+"

  See [Terminal configuration](/en/terminal-config) for details.
</Note>

### General controls

| Shortcut                                          | Description                        | Context                                                                                       |
| :------------------------------------------------ | :--------------------------------- | :-------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                          | Cancel current input or generation | Standard interrupt                                                                            |
| `Ctrl+D`                                          | Exit Claude Code session           | EOF signal                                                                                    |
| `Ctrl+L`                                          | Clear terminal screen              | Keeps conversation history                                                                    |
| `Ctrl+O`                                          | Toggle verbose output              | Shows detailed tool usage and execution                                                       |
| `Ctrl+R`                                          | Reverse search command history     | Search through previous commands interactively                                                |
| `Ctrl+V` or `Cmd+V` (iTerm2) or `Alt+V` (Windows) | Paste image from clipboard         | Pastes an image or path to an image file                                                      |
| `Ctrl+B`                                          | Background running tasks           | Backgrounds bash commands and agents. Tmux users press twice                                  |
| `Left/Right arrows`                               | Cycle through dialog tabs          | Navigate between tabs in permission dialogs and menus                                         |
| `Up/Down arrows`                                  | Navigate command history           | Recall previous inputs                                                                        |
| `Esc` + `Esc`                                     | Rewind the code/conversation       | Restore the code and/or conversation to a previous point                                      |
| `Shift+Tab` or `Alt+M` (some configurations)      | Toggle permission modes            | Switch between Auto-Accept Mode, Plan Mode, and normal mode                                   |
| `Option+P` (macOS) or `Alt+P` (Windows/Linux)     | Switch model                       | Switch models without clearing your prompt                                                    |
| `Option+T` (macOS) or `Alt+T` (Windows/Linux)     | Toggle extended thinking           | Enable or disable extended thinking mode. Run `/terminal-setup` first to enable this shortcut |

### Text editing

| Shortcut                 | Description                  | Context                                                                                                       |
| :----------------------- | :--------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `Ctrl+K`                 | Delete to end of line        | Stores deleted text for pasting                                                                               |
| `Ctrl+U`                 | Delete entire line           | Stores deleted text for pasting                                                                               |
| `Ctrl+Y`                 | Paste deleted text           | Paste text deleted with `Ctrl+K` or `Ctrl+U`                                                                  |
| `Alt+Y` (after `Ctrl+Y`) | Cycle paste history          | After pasting, cycle through previously deleted text. Requires [Option as Meta](#keyboard-shortcuts) on macOS |
| `Alt+B`                  | Move cursor back one word    | Word navigation. Requires [Option as Meta](#keyboard-shortcuts) on macOS                                      |
| `Alt+F`                  | Move cursor forward one word | Word navigation. Requires [Option as Meta](#keyboard-shortcuts) on macOS                                      |

### Theme and display

| Shortcut | Description                                | Context                                                                                                      |
| :------- | :----------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| `Ctrl+T` | Toggle syntax highlighting for code blocks | Only works inside the `/theme` picker menu. Controls whether code in Claude's responses uses syntax coloring |

<Note>
  Syntax highlighting is only available in the native build of Claude Code.
</Note>

### Multiline input

| Method           | Shortcut       | Context                                                 |
| :--------------- | :------------- | :------------------------------------------------------ |
| Quick escape     | `\` + `Enter`  | Works in all terminals                                  |
| macOS default    | `Option+Enter` | Default on macOS                                        |
| Shift+Enter      | `Shift+Enter`  | Works out of the box in iTerm2, WezTerm, Ghostty, Kitty |
| Control sequence | `Ctrl+J`       | Line feed character for multiline                       |
| Paste mode       | Paste directly | For code blocks, logs                                   |

<Tip>
  Shift+Enter works without configuration in iTerm2, WezTerm, Ghostty, and Kitty. For other terminals (VS Code, Alacritty, Zed, Warp), run `/terminal-setup` to install the binding.
</Tip>

### Quick commands

| Shortcut     | Description       | Notes                                                         |
| :----------- | :---------------- | :------------------------------------------------------------ |
| `/` at start | Slash command     | See [slash commands](/en/slash-commands)                      |
| `!` at start | Bash mode         | Run commands directly and add execution output to the session |
| `@`          | File path mention | Trigger file path autocomplete                                |

## Vim editor mode

Enable vim-style editing with `/vim` command or configure permanently via `/config`.

### Mode switching

| Command | Action                      | From mode |
| :------ | :-------------------------- | :-------- |
| `Esc`   | Enter NORMAL mode           | INSERT    |
| `i`     | Insert before cursor        | NORMAL    |
| `I`     | Insert at beginning of line | NORMAL    |
| `a`     | Insert after cursor         | NORMAL    |
| `A`     | Insert at end of line       | NORMAL    |
| `o`     | Open line below             | NORMAL    |
| `O`     | Open line above             | NORMAL    |

### Navigation (NORMAL mode)

| Command         | Action                                              |
| :-------------- | :-------------------------------------------------- |
| `h`/`j`/`k`/`l` | Move left/down/up/right                             |
| `w`             | Next word                                           |
| `e`             | End of word                                         |
| `b`             | Previous word                                       |
| `0`             | Beginning of line                                   |
| `$`             | End of line                                         |
| `^`             | First non-blank character                           |
| `gg`            | Beginning of input                                  |
| `G`             | End of input                                        |
| `f{char}`       | Jump to next occurrence of character                |
| `F{char}`       | Jump to previous occurrence of character            |
| `t{char}`       | Jump to just before next occurrence of character    |
| `T{char}`       | Jump to just after previous occurrence of character |
| `;`             | Repeat last f/F/t/T motion                          |
| `,`             | Repeat last f/F/t/T motion in reverse               |

### Editing (NORMAL mode)

| Command        | Action                  |
| :------------- | :---------------------- |
| `x`            | Delete character        |
| `dd`           | Delete line             |
| `D`            | Delete to end of line   |
| `dw`/`de`/`db` | Delete word/to end/back |
| `cc`           | Change line             |
| `C`            | Change to end of line   |
| `cw`/`ce`/`cb` | Change word/to end/back |
| `yy`/`Y`       | Yank (copy) line        |
| `yw`/`ye`/`yb` | Yank word/to end/back   |
| `p`            | Paste after cursor      |
| `P`            | Paste before cursor     |
| `>>`           | Indent line             |
| `<<`           | Dedent line             |
| `J`            | Join lines              |
| `.`            | Repeat last change      |

### Text objects (NORMAL mode)

Text objects work with operators like `d`, `c`, and `y`:

| Command   | Action                                   |
| :-------- | :--------------------------------------- |
| `iw`/`aw` | Inner/around word                        |
| `iW`/`aW` | Inner/around WORD (whitespace-delimited) |
| `i"`/`a"` | Inner/around double quotes               |
| `i'`/`a'` | Inner/around single quotes               |
| `i(`/`a(` | Inner/around parentheses                 |
| `i[`/`a[` | Inner/around brackets                    |
| `i{`/`a{` | Inner/around braces                      |

## Command history

Claude Code maintains command history for the current session:

* History is stored per working directory
* Cleared with `/clear` command
* Use Up/Down arrows to navigate (see keyboard shortcuts above)
* **Note**: History expansion (`!`) is disabled by default

### Reverse search with Ctrl+R

Press `Ctrl+R` to interactively search through your command history:

1. **Start search**: Press `Ctrl+R` to activate reverse history search
2. **Type query**: Enter text to search for in previous commands - the search term will be highlighted in matching results
3. **Navigate matches**: Press `Ctrl+R` again to cycle through older matches
4. **Accept match**:
   * Press `Tab` or `Esc` to accept the current match and continue editing
   * Press `Enter` to accept and execute the command immediately
5. **Cancel search**:
   * Press `Ctrl+C` to cancel and restore your original input
   * Press `Backspace` on empty search to cancel

The search displays matching commands with the search term highlighted, making it easy to find and reuse previous inputs.

## Background bash commands

Claude Code supports running bash commands in the background, allowing you to continue working while long-running processes execute.

### How backgrounding works

When Claude Code runs a command in the background, it runs the command asynchronously and immediately returns a background task ID. Claude Code can respond to new prompts while the command continues executing in the background.

To run commands in the background, you can either:

* Prompt Claude Code to run a command in the background
* Press Ctrl+B to move a regular Bash tool invocation to the background. (Tmux users must press Ctrl+B twice due to tmux's prefix key.)

**Key features:**

* Output is buffered and Claude can retrieve it using the BashOutput tool
* Background tasks have unique IDs for tracking and output retrieval
* Background tasks are automatically cleaned up when Claude Code exits

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`. See [Environment variables](/en/settings#environment-variables) for details.

**Common backgrounded commands:**

* Build tools (webpack, vite, make)
* Package managers (npm, yarn, pnpm)
* Test runners (jest, pytest)
* Development servers
* Long-running processes (docker, terraform)

### Bash mode with `!` prefix

Run bash commands directly without going through Claude by prefixing your input with `!`:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Bash mode:

* Adds the command and its output to the conversation context
* Shows real-time progress and output
* Supports the same `Ctrl+B` backgrounding for long-running commands
* Does not require Claude to interpret or approve the command

This is useful for quick shell operations while maintaining conversation context.

## See also

* [Slash commands](/en/slash-commands) - Interactive session commands
* [Checkpointing](/en/checkpointing) - Rewind Claude's edits and restore previous states
* [CLI reference](/en/cli-reference) - Command-line flags and options
* [Settings](/en/settings) - Configuration options
* [Memory management](/en/memory) - Managing CLAUDE.md files


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt