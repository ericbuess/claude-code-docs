> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code with a screen reader

> Set up Claude Code for screen readers such as VoiceOver and NVDA, plus settings for screen magnifiers, reduced motion, and colorblind-friendly themes.

Claude Code has a screen reader mode that replaces its visual terminal interface with plain, linear text. Instead of boxes, progress animations, and in-place redraws, Claude Code prints labeled lines that a screen reader such as VoiceOver or NVDA reads in order. You can hold a full conversation, approve tool permissions, and review output end to end.

Screen reader mode is opt-in. If you use a screen magnifier, reduced motion, or a colorblind-friendly theme instead of a screen reader, set `CLAUDE_CODE_ACCESSIBILITY`, `prefersReducedMotion`, or `theme` from the [Accessibility settings](#accessibility-settings) table. Screen reader mode adapts the terminal interface only, so you don't need it in the VS Code extension's chat panel. On Claude Code v2.1.236 or later, the extension [announces conversation activity to your screen reader](/docs/en/vs-code#use-a-screen-reader) there without any setting.

Screen reader mode requires Claude Code v2.1.181 or later. Earlier versions reject the `--ax-screen-reader` flag with `error: unknown option '--ax-screen-reader'`.

## Turn on screen reader mode

Pick the method that matches how often you use a screen reader:

* For one session: run `claude --ax-screen-reader`.
* For sessions started from one shell: set the `CLAUDE_AX_SCREEN_READER` environment variable to `1`. In Bash or Zsh, run `export CLAUDE_AX_SCREEN_READER=1`. In PowerShell, run `$env:CLAUDE_AX_SCREEN_READER = "1"`. Add that line to your shell profile to keep it for future shells.
* For every session on the machine: add `"axScreenReader": true` to your user [settings file](/docs/en/settings). The setting applies in any terminal, including the VS Code integrated terminal.

If you combine methods, Claude Code applies the [`--ax-screen-reader`](/docs/en/cli-reference#cli-flags) flag over the [`CLAUDE_AX_SCREEN_READER`](/docs/en/env-vars#variables) environment variable, and the variable over the [`axScreenReader`](/docs/en/settings-reference#axscreenreader) setting.

If you use Claude Code over SSH, set the environment variable or setting on the remote machine where Claude Code runs.

The first line Claude Code prints confirms the mode: `[Screen Reader Mode: on via flag]`, `[Screen Reader Mode: on via env]`, or `[Screen Reader Mode: on via settings]`.

## Turn off screen reader mode

Reverse whichever method turned the mode on: start without the flag, unset the environment variable, or set `axScreenReader` to `false`. If you set `CLAUDE_AX_SCREEN_READER` to `0`, Claude Code keeps the mode off even when the setting is `true`.

## Accessibility settings

The table lists each accessibility option, whether you set it as a flag, an environment variable, or a setting, and what it changes.

| Option                                                                  | Type                 | What it changes                                                                                                                                                                                                                                          |
| :---------------------------------------------------------------------- | :------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`--ax-screen-reader`](/docs/en/cli-reference#cli-flags)                     | Flag                 | Screen reader mode for one session.                                                                                                                                                                                                                      |
| [`CLAUDE_AX_SCREEN_READER`](/docs/en/env-vars#variables)                     | Environment variable | Screen reader mode for sessions started from the shell where you set it.                                                                                                                                                                                 |
| [`axScreenReader`](/docs/en/settings-reference#axscreenreader)               | Setting              | Screen reader mode for every session when `true`.                                                                                                                                                                                                        |
| [`CLAUDE_AX_STARTUP_QUIET_MS`](/docs/en/env-vars#variables)                  | Environment variable | How long Claude Code waits after the confirmation line before it draws the first prompt in screen reader mode. Requires Claude Code v2.1.217 or later.                                                                                                   |
| [`CLAUDE_AX_PREPARK_MS`](/docs/en/env-vars#variables)                        | Environment variable | How long Claude Code waits, with the cursor at the start of the line, before it writes a new or changed line in screen reader mode. Requires Claude Code v2.1.233 or later.                                                                              |
| [`CLAUDE_CODE_ACCESSIBILITY`](/docs/en/env-vars#variables)                   | Environment variable | A terminal cursor that stays visible for screen magnifiers such as macOS Zoom when you set it to `1`. The cursor follows the input caret and, on Claude Code v2.1.218 or later, the highlighted row in menus and panels such as `/config` and `/plugin`. |
| [`prefersReducedMotion`](/docs/en/settings-reference#prefersreducedmotion)   | Setting              | Reduced or no spinners, shimmer, and other animations when `true`.                                                                                                                                                                                       |
| [`theme`](/docs/en/settings-reference#theme)                                 | Setting              | The interface colors, including the colorblind-friendly `dark-daltonized` and `light-daltonized` themes. You can also pick one with [`/theme`](/docs/en/commands#all-commands).                                                                               |
| [`preferredNotifChannel`](/docs/en/settings-reference#preferrednotifchannel) | Setting              | With the value `"terminal_bell"`, a terminal bell outside screen reader mode when Claude is waiting on you.                                                                                                                                              |

## What your screen reader hears

In screen reader mode, Claude Code writes flat text:

* No box-drawing characters for the interface chrome
* No color-only cues
* No redraws of content that hasn't changed. Progress spinners render as static text
* Tables in Claude's replies read as `Header: value` sentences instead of a box-character grid

Claude Code leaves everything it prints in your terminal's scrollback, so you can re-read earlier turns with your screen reader's review commands or your terminal's search. Claude Code ignores the [`tui` setting](/docs/en/settings-reference#tui) in screen reader mode. Apart from the attached background sessions listed under [Known limitations](#known-limitations), it prints scrolling text instead of [fullscreen rendering](/docs/en/fullscreen).

Claude Code also waits at two points so your screen reader can keep up:

* After Claude Code prints the confirmation line, it waits 3 seconds before it draws the prompt, so your screen reader can finish the line. Press any key to end the wait. To change the length of the wait, set [`CLAUDE_AX_STARTUP_QUIET_MS`](/docs/en/env-vars#variables).
* Before Claude Code writes a new or changed line, such as a hint or more of Claude's reply, it moves the cursor to the start of the line and waits 50 milliseconds. Your screen reader then reads the line from its first character. Characters you type or delete at the end of the input line appear immediately. To change the length of the wait, set [`CLAUDE_AX_PREPARK_MS`](/docs/en/env-vars#variables).

Each message in the transcript starts with a label your screen reader announces, naming what it is: your messages, Claude's replies and thinking, tool activity, errors and warnings, and prompts. The labels are also searchable, so you can jump between sections of the transcript by searching your terminal's scrollback:

| Label                  | Meaning                                                                                   |
| :--------------------- | :---------------------------------------------------------------------------------------- |
| `you:`                 | Your messages                                                                             |
| `claude:`              | Claude's replies                                                                          |
| `thinking:`            | Claude's thinking                                                                         |
| `tool:`                | Tool activity, such as a file edit or a command run                                       |
| `tool error:`          | A tool that failed                                                                        |
| `error:`               | An error in the conversation, such as a failed API request                                |
| `warning:`             | A warning from Claude Code, such as a switch to a fallback model                          |
| `Permission Required:` | A permission prompt waiting for your answer                                               |
| `Cost:`                | The session cost summary when Claude Code exits, if your account [shows costs](/docs/en/costs) |

Claude Code keeps the terminal cursor on the input caret, so your screen reader's read-current-line command reads the prompt you're editing.

As you type at the end of the input line, or press `Backspace` there, Claude Code writes only the characters that change. Your screen reader echoes only those characters.

When you delete a word or a line with one of the [text editing shortcuts](/docs/en/interactive-mode#text-editing), Claude Code announces the deleted text:

* Deleting words with `Ctrl+W` or `Alt+D`, or with `Option+Delete` on macOS or `Ctrl+Backspace` on Windows
* Deleting to the start of the line with `Ctrl+U` or `Cmd+Backspace`
* Deleting to the end of the line with `Ctrl+K`

When you cycle [permission modes](/docs/en/permission-modes) with `Shift+Tab`, Claude Code announces the permission mode you land on, such as `[plan mode on]` or `[accept edits on]`. Claude Code prints the announcement once and doesn't repeat it on later redraws.

### Jump between turns

Claude Code emits OSC 133 shell-integration markers at turn boundaries, so your terminal's jump-to-previous-prompt key moves between turns without reading through the whole transcript:

* iTerm2: Cmd+Shift+Up
* VS Code terminal: Ctrl+Up on Windows, Cmd+Up on macOS
* Windows Terminal: no key by default; bind the `scrollToMark` action in its settings
* Kitty and Ghostty: check the terminal's documentation for its jump-to-prompt key

macOS Terminal doesn't act on the markers, and Claude Code doesn't emit them in WezTerm. In those terminals, search the scrollback for the `you:` label instead.

## Answer menus and prompts

In screen reader mode, menus you'd normally navigate with the arrow keys, including permission prompts, become numbered lists. Claude Code announces each option as a numbered line, then an `Enter selection` prompt that names the valid range. Type the number of the option you want and press Enter.

* Press Escape to cancel a menu whose prompt ends with `or Escape to cancel`.
* If you type a number that isn't on the list, Claude Code announces the valid range and lets you try again.

The [`/effort`](/docs/en/model-config#adjust-effort-level) selector, which is a slider outside screen reader mode, becomes the same kind of numbered list.

Yes-or-no prompts ask for a typed answer instead of a two-option menu. Answer `y` or `n` and press Enter. `yes` and `no` also work.

## Hear when Claude Code needs you

In screen reader mode, Claude Code rings the terminal bell when it needs your attention, so you don't have to keep checking the transcript. The bell rings when:

* Claude finishes a reply
* A prompt or dialog needs your answer, such as a permission prompt
* A tool that ran longer than 5 seconds finishes

The bell is your terminal's standard alert. To silence it, change the bell setting in your terminal application. Outside screen reader mode, set [`preferredNotifChannel`](/docs/en/settings-reference#preferrednotifchannel) to `"terminal_bell"` to get a [similar bell](/docs/en/terminal-config#get-a-terminal-bell-or-notification) when Claude is waiting on you.

## Known limitations

Some behaviors aren't adapted for screen reader mode:

* Screen reader mode doesn't turn on automatically when a screen reader is running.
* Claude Code doesn't announce a permission mode change made in any way other than cycling with `Shift+Tab`, such as entering [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) from a command.
* Attaching to a [background session](/docs/en/agent-view) with `claude attach` or from agent view enters the terminal's alternate screen, which has no native scrollback. This is the [same behavior as other attached sessions](/docs/en/fullscreen). To get back out, press Left Arrow on an empty prompt, or Ctrl+Z if a dialog has focus.
* Claude Code announces costs in the summary it prints at exit, not per turn.
* Screen reader mode doesn't change [non-interactive mode](/docs/en/headless) with the `-p` flag. Non-interactive mode already writes plain text and remains an alternative for scripting.

## Report an issue

If something doesn't work with your screen reader, magnifier, or terminal, open an issue on the [Claude Code issue tracker](https://github.com/anthropics/claude-code/issues) and mention your assistive technology in the title. Include your operating system, terminal application, and assistive technology name and version in the report.
