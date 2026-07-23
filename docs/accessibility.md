> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code with a screen reader

> Set up Claude Code for screen readers such as VoiceOver and NVDA, plus settings for screen magnifiers, reduced motion, and colorblind-friendly themes.

Claude Code has a screen reader mode that replaces its visual terminal interface with plain, linear text. Instead of boxes, progress animations, and in-place redraws, the mode prints labeled lines that a screen reader such as VoiceOver or NVDA reads in order, so you can hold a full conversation, approve tool permissions, and review output end to end.

Screen reader mode is opt-in. If you use a screen magnifier, reduced motion, or a colorblind-friendly theme instead of a screen reader, see [Accessibility settings beyond screen reader mode](#accessibility-settings-beyond-screen-reader-mode).

<Note>
  Screen reader mode requires Claude Code v2.1.181 or later. Earlier versions reject the `--ax-screen-reader` flag with `error: unknown option '--ax-screen-reader'`.
</Note>

## Turn on screen reader mode

Pick the method that matches how often you use a screen reader:

* For one session: run `claude --ax-screen-reader`.
* For sessions started from one shell: set the `CLAUDE_AX_SCREEN_READER` environment variable to `1`. In Bash or Zsh, run `export CLAUDE_AX_SCREEN_READER=1`; in PowerShell, run `$env:CLAUDE_AX_SCREEN_READER = "1"`. Add the line to your shell profile to cover every shell.
* For every session on the machine: add `"axScreenReader": true` to your user [settings file](/docs/en/settings). This covers any terminal, including the VS Code integrated terminal.

<Note>
  The methods are listed in precedence order: the [`--ax-screen-reader`](/docs/en/cli-reference#cli-flags) flag overrides the [`CLAUDE_AX_SCREEN_READER`](/docs/en/env-vars) environment variable, which overrides the [`axScreenReader`](/docs/en/settings#available-settings) setting.
</Note>

If you use Claude Code over SSH, set the environment variable or setting on the remote machine where Claude Code runs.

When the mode is on, the first thing Claude Code prints is a confirmation line naming the method that turned it on: `[Screen Reader Mode: on via flag]`, `[Screen Reader Mode: on via env]`, or `[Screen Reader Mode: on via settings]`. The method-naming format requires Claude Code v2.1.206 or later. When Claude Code relaunches itself, for example to finish installing an update, the new process inherits the mode through the `CLAUDE_AX_SCREEN_READER` environment variable, so its confirmation line reads `[Screen Reader Mode: on via env]` regardless of which method you used.
{/* max-version: 2.1.205 */}Earlier versions print `[Accessible screen reader mode: on]`.

## Turn off screen reader mode

Reverse whichever method turned the mode on: start without the flag, unset the environment variable, or set `axScreenReader` to `false`. Setting `CLAUDE_AX_SCREEN_READER=0` keeps the mode off even when the setting is `true`.

## What your screen reader hears

In screen reader mode, Claude Code writes flat text:

* no box-drawing characters for the interface chrome
* no color-only cues
* no redraws of content that hasn't changed; progress spinners render as static text
* tables in Claude's replies read as `Header: value` sentences instead of a box-character grid. {/* min-version: 2.1.198 */}Requires Claude Code v2.1.198 or later; earlier versions draw tables as grids even in screen reader mode.

Output accumulates in your terminal's scrollback, so you can re-read earlier turns with your screen reader's review commands or your terminal's search.

Screen reader mode renders as plain scrolling text, even if you've turned on [fullscreen rendering](/docs/en/fullscreen) with the [`tui` setting](/docs/en/settings#available-settings); the setting has no effect while the mode is active. Attached background sessions still render fullscreen; see [Known limitations](#known-limitations).

Each message in the transcript starts with a label your screen reader announces, naming what it is: your messages, Claude's replies, tool activity, errors, and prompts. The labels are also searchable, so you can jump between sections of the transcript by searching your terminal's scrollback:

| Label                  | Meaning                                                                                   |
| :--------------------- | :---------------------------------------------------------------------------------------- |
| `you:`                 | Your messages                                                                             |
| `claude:`              | Claude's replies                                                                          |
| `tool:`                | Tool activity, such as a file edit or a command run                                       |
| `tool error:`          | A tool that failed                                                                        |
| `error:`               | An error in the conversation, such as a failed API request                                |
| `Permission Required:` | A permission prompt waiting for your answer                                               |
| `Cost:`                | The session cost summary when Claude Code exits, if your account [shows costs](/docs/en/costs) |

The terminal cursor follows the input caret, so a screen reader's read-current-line command answers "where am I" with the prompt you're editing.

{/* min-version: 2.1.218 */}When you delete a word or a line in the input, Claude Code announces the deleted text. Requires Claude Code v2.1.218 or later. The announcement covers:

* Deleting a word with `Ctrl+W`, `Option+Delete` on macOS, or `Ctrl+Backspace` on Windows
* Deleting to the start of the line with `Ctrl+U` or `Cmd+Backspace`
* Deleting to the end of the line with `Ctrl+K`

See the [text editing shortcuts](/docs/en/interactive-mode#text-editing) for what each key does.

{/* min-version: 2.1.210 */}Cycling [permission modes](/docs/en/permission-modes) with `Shift+Tab` announces the mode you land on, such as `[plan mode on]` or `[accept edits on]`. Claude Code prints the announcement once and doesn't repeat it on later redraws. Requires Claude Code v2.1.210 or later.

### Jump between turns

Claude Code emits OSC 133 shell-integration markers at turn boundaries, so your terminal's jump-to-previous-prompt key moves between turns without reading through the whole transcript:

* iTerm2: Cmd+Shift+Up
* VS Code terminal: Ctrl+Up on Windows, Cmd+Up on macOS
* Windows Terminal: no key by default; bind the `scrollToMark` action in its settings
* Kitty and Ghostty: check the terminal's documentation for its jump-to-prompt key

macOS Terminal doesn't act on the markers, and Claude Code doesn't emit them in WezTerm. In those terminals, search the scrollback for the `you:` label instead.

## Answer menus and prompts

In screen reader mode, menus you'd normally navigate with the arrow keys, including permission prompts, become numbered lists. Each option is announced as a numbered line, followed by an `Enter selection` prompt that names the valid range. Type the number of the option you want and press Enter.

* To cancel a dismissible menu: press Escape. Its prompt ends with `or Escape to cancel`.
* If you type a number that isn't on the list: Claude Code announces the valid range and lets you try again.

Yes-or-no prompts ask for a typed answer instead of a two-option menu. Answer `y` or `n` and press Enter. `yes` and `no` also work.

## Hear when Claude Code needs you

In screen reader mode, Claude Code rings the terminal bell when it needs your attention, so you don't have to keep checking the transcript. The bell rings when:

* Claude finishes a reply
* a permission prompt appears
* a tool that ran longer than 5 seconds finishes

The bell is your terminal's standard alert. To silence it, change the bell setting in your terminal application. The bell doesn't require screen reader mode: outside the mode, set [`preferredNotifChannel`](/docs/en/settings#available-settings) to `"terminal_bell"` for similar alerts when Claude is waiting on you. See [Get a terminal bell or notification](/docs/en/terminal-config#get-a-terminal-bell-or-notification).

## Accessibility settings beyond screen reader mode

These options address accessibility needs outside of screen reader mode. All of them work alongside it.

* The `CLAUDE_CODE_ACCESSIBILITY` [environment variable](/docs/en/env-vars) is for screen magnifiers. Set `CLAUDE_CODE_ACCESSIBILITY=1` to keep the native terminal cursor visible so that magnifiers, such as macOS Zoom, can track the cursor position. The cursor follows keyboard focus: the input caret while you type, and the highlighted row as you move through menus and panels, such as `/config` and `/plugin`, with the arrow keys. {/* min-version: 2.1.218 */}Row tracking in menus and panels requires Claude Code v2.1.218 or later.
* The `prefersReducedMotion` [setting](/docs/en/settings#available-settings) reduces or disables spinners, shimmer, and other animations without changing the rest of the interface.
* The `theme` [setting](/docs/en/settings#available-settings) selects the interface colors, including the colorblind-friendly `dark-daltonized` and `light-daltonized` themes.

## Known limitations

Some behaviors aren't adapted for screen reader mode:

* Screen reader mode doesn't turn on automatically when a screen reader is running.
* Claude Code doesn't announce a permission mode change made in any way other than cycling with `Shift+Tab`, such as entering [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) from a command.
* Attaching to a [background session](/docs/en/agent-view) with `claude attach` or from agent view enters the terminal's alternate screen, which has no native scrollback. This is the [same behavior as other attached sessions](/docs/en/fullscreen). To get back out, press Left Arrow on an empty prompt, or Ctrl+Z if a dialog has focus.
* Claude Code announces costs in the summary it prints at exit, not per turn.
* Screen reader mode doesn't change [non-interactive mode](/docs/en/headless) with the `-p` flag. Non-interactive mode already writes plain text and remains an alternative for scripting.

## Report an issue

If something doesn't work with your screen reader, magnifier, or terminal, open an issue on the [Claude Code issue tracker](https://github.com/anthropics/claude-code/issues) and mention your assistive technology in the title. Include your operating system, terminal application, and assistive technology name and version in the report.

## Related resources

These pages hold the full reference entries and related setup for what this page covers:

* [Settings](/docs/en/settings#available-settings): the `axScreenReader`, `prefersReducedMotion`, `theme`, and `preferredNotifChannel` entries
* [Environment variables](/docs/en/env-vars): the `CLAUDE_AX_SCREEN_READER` and `CLAUDE_CODE_ACCESSIBILITY` entries
* [CLI reference](/docs/en/cli-reference#cli-flags): the `--ax-screen-reader` flag
* [Terminal configuration](/docs/en/terminal-config): bells, notifications, and themes outside screen reader mode
* [Non-interactive mode](/docs/en/headless): scripted `claude -p` runs, which write plain text without screen reader mode
