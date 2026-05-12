> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fullscreen rendering

> Enable a smoother, flicker-free rendering mode with mouse support and stable memory usage in long conversations.

<Note>
  Fullscreen rendering is an opt-in [research preview](#research-preview) and requires Claude Code v2.1.89 or later. Run `/tui fullscreen` to switch in your current conversation, or set `CLAUDE_CODE_NO_FLICKER=1` on versions before v2.1.110. Behavior may change based on feedback.
</Note>

Fullscreen rendering is an alternative rendering path for the Claude Code CLI that eliminates flicker, keeps memory usage flat in long conversations, and adds mouse support. It draws the interface on the terminal's alternate screen buffer, like `vim` or `htop`, and only renders messages that are currently visible. This reduces the amount of data sent to your terminal on each update.

The difference is most noticeable in terminal emulators where rendering throughput is the bottleneck, such as the VS Code integrated terminal, tmux, and iTerm2. If your terminal scroll position jumps to the top while Claude is working, or the screen flashes as tool output streams in, this mode addresses those.

<Note>
  The term fullscreen describes how Claude Code takes over the terminal's drawing surface, the way `vim` does. It has nothing to do with maximizing your terminal window, and works at any window size.
</Note>

## Enable fullscreen rendering

Run `/tui fullscreen` inside any Claude Code conversation. The CLI saves the [`tui` setting](/en/settings#available-settings) and relaunches into fullscreen with your conversation intact, so you can switch mid-session without losing context. Run `/tui` with no argument to print which renderer is active.

You can also set the `CLAUDE_CODE_NO_FLICKER` environment variable before starting Claude Code:

```bash theme={null}
CLAUDE_CODE_NO_FLICKER=1 claude
```

The `tui` setting and the environment variable are equivalent. The `/tui` command clears `CLAUDE_CODE_NO_FLICKER` from the relaunched process so the setting it writes takes effect.

## What changes

Fullscreen rendering changes how the CLI draws to your terminal. The input box stays fixed at the bottom of the screen instead of moving as output streams in. If the input stays put while Claude is working, fullscreen rendering is active. Only visible messages are kept in the render tree, so memory stays constant regardless of conversation length.

Because the conversation lives in the alternate screen buffer instead of your terminal's scrollback, a few things work differently:

| Before                                              | Now                                                                            | Details                                                                   |
| :-------------------------------------------------- | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------ |
| `Cmd+f` or tmux search to find text                 | `Ctrl+o` for transcript mode, then `/` to search or `[` to write to scrollback | [Search and review the conversation](#search-and-review-the-conversation) |
| Terminal's native click-and-drag to select and copy | In-app selection, copies automatically on mouse release                        | [Use the mouse](#use-the-mouse)                                           |
| `Cmd`-click to open a URL                           | Click the URL                                                                  | [Use the mouse](#use-the-mouse)                                           |

If mouse capture interferes with your workflow, you can [turn it off](#keep-native-text-selection) while keeping the flicker-free rendering.

## Use the mouse

Fullscreen rendering captures mouse events and handles them inside Claude Code:

* **Click in the prompt input** to position your cursor anywhere in the text you're typing.
* **Click a collapsed tool result** to expand it and see the full output. Click again to collapse. The tool call and its result expand together. Only messages that have more to show are clickable.
* **Click a URL or file path** to open it. File paths in tool output, like the ones printed after an Edit or Write, open in your default application. Plain `http://` and `https://` URLs open in your browser. In most terminals this replaces native `Cmd`-click or `Ctrl`-click, which mouse capture intercepts. In the VS Code integrated terminal and similar xterm.js-based terminals, keep using `Cmd`-click. Claude Code defers to the terminal's own link handler there to avoid opening links twice.
* **Click and drag** to select text anywhere in the conversation. Double-click selects a word, matching iTerm2's word boundaries so a file path selects as one unit. Triple-click selects the line.
* **Scroll with the mouse wheel** to move through the conversation.

Selected text copies to your clipboard automatically on mouse release. To turn this off, toggle Copy on select in `/config`. With it off, press `Ctrl+Shift+c` to copy manually. On terminals that support the kitty keyboard protocol, such as kitty, WezTerm, Ghostty, and iTerm2, `Cmd+c` also works. If you have a selection active, `Ctrl+c` copies instead of cancelling.

With a selection active, hold `Shift` and press the arrow keys to extend it from the keyboard. `Shift+↑` and `Shift+↓` scroll the viewport when the selection reaches the top or bottom edge. `Shift+Home` and `Shift+End` extend to the start or end of the current line.

## Scroll the conversation

Fullscreen rendering handles scrolling inside the app. Use these shortcuts to navigate:

| Shortcut        | Action                                               |
| :-------------- | :--------------------------------------------------- |
| `PgUp` / `PgDn` | Scroll up or down by half a screen                   |
| `Ctrl+Home`     | Jump to the start of the conversation                |
| `Ctrl+End`      | Jump to the latest message and re-enable auto-follow |
| Mouse wheel     | Scroll a few lines at a time                         |

On keyboards without dedicated `PgUp`, `PgDn`, `Home`, or `End` keys, like MacBook keyboards, hold `Fn` with the arrow keys: `Fn+↑` sends `PgUp`, `Fn+↓` sends `PgDn`, `Fn+←` sends `Home`, and `Fn+→` sends `End`. That makes `Ctrl+Fn+→` the jump-to-bottom shortcut. If that feels awkward, scroll to the bottom with the mouse wheel to resume following, or rebind `scroll:bottom` to something reachable.

These actions are rebindable. See [Scroll actions](/en/keybindings#scroll-actions) for the full list of action names, including half-page and full-page variants that have no default binding.

### Auto-follow

Scrolling up pauses auto-follow so new output does not pull you back to the bottom. Press `Ctrl+End` or scroll to the bottom to resume following.

To turn auto-follow off entirely so the view stays where you leave it, open `/config` and set Auto-scroll to off. With auto-scroll disabled, the view never jumps to the bottom on its own. Permission prompts and other dialogs that need a response still scroll into view regardless of this setting.

### Mouse wheel scrolling

Mouse wheel scrolling requires your terminal to forward mouse events to Claude Code. Most terminals do this whenever an application requests it. iTerm2 makes it a per-profile setting: if the wheel does nothing but `PgUp` and `PgDn` work, open Settings → Profiles → Terminal and turn on Enable mouse reporting. The same setting is also required for click-to-expand and text selection to work.

If mouse wheel scrolling feels slow, your terminal may be sending one scroll event per physical notch with no multiplier. Some terminals, like Ghostty and iTerm2 with faster scrolling enabled, already amplify wheel events. Others, including the VS Code integrated terminal, send exactly one event per notch. Claude Code cannot detect which.

Set `CLAUDE_CODE_SCROLL_SPEED` to multiply the base scroll distance:

```bash theme={null}
export CLAUDE_CODE_SCROLL_SPEED=3
```

A value of `3` matches the default in `vim` and similar applications. The setting accepts values from 1 to 20.

To adjust scroll speed interactively, run `/scroll-speed`. The dialog shows a ruler you can scroll while it is open so you can feel the change immediately. Press `←` and `→` to adjust, `r` to reset to the auto-detected default, and `Enter` to save. The command writes the same value the `CLAUDE_CODE_SCROLL_SPEED` environment variable sets, persisted to `~/.claude/settings.json`. The command is not available in the JetBrains IDE terminal.

### Scroll in the JetBrains IDE terminal

In the JetBrains IDE terminal, Claude Code applies its own scroll handling and ignores `CLAUDE_CODE_SCROLL_SPEED`. The terminal sends scroll events at a much higher rate than other emulators, so a multiplier tuned elsewhere overshoots here.

In 2025.2, the terminal also has scroll-wheel bugs that produce spurious arrow keys and wrong-direction events. Claude Code detects these at runtime and mitigates them automatically, so trackpad and mouse wheel scrolling work without configuration. For the best scroll experience, upgrade to 2025.3 or later. Claude Code shows a hint the first time you scroll if it detects the bug.

## Search and review the conversation

`Ctrl+o` toggles between the normal prompt and transcript mode. For a quieter view that shows only your last prompt, a one-line summary of tool calls with edit diffstats, and the final response, run `/focus`. The setting persists across sessions. Run `/focus` again to turn it off.

Transcript mode gains `less`-style navigation and search:

| Key                                  | Action                                                                                                 |
| :----------------------------------- | :----------------------------------------------------------------------------------------------------- |
| `/`                                  | Open search. Type to find matches, `Enter` to accept, `Esc` to cancel and restore your scroll position |
| `n` / `N`                            | Jump to next or previous match. Works after you've closed the search bar                               |
| `j` / `k` or `↑` / `↓`               | Scroll one line                                                                                        |
| `g` / `G` or `Home` / `End`          | Jump to top or bottom                                                                                  |
| `Ctrl+u` / `Ctrl+d`                  | Scroll half a page                                                                                     |
| `Ctrl+b` / `Ctrl+f` or `Space` / `b` | Scroll a full page                                                                                     |
| `Ctrl+o`, `Esc`, or `q`              | Exit transcript mode and return to the prompt                                                          |

Your terminal's `Cmd+f` and tmux search don't see the conversation because it lives in the alternate screen buffer, not the native scrollback. To hand the content back to your terminal, press `Ctrl+o` to enter transcript mode first, then:

* **`[`**: writes the full conversation into your terminal's native scrollback buffer, with all tool output expanded. The conversation is now ordinary text in your terminal, so `Cmd+f`, tmux copy mode, and any other native tool can search or select it. Long sessions may pause for a moment while this happens. This lasts until you exit transcript mode with `Esc` or `q`, which returns you to fullscreen rendering. The next `Ctrl+o` starts fresh.
* **`v`**: writes the conversation to a temporary file and opens it in `$VISUAL` or `$EDITOR`.

Press `Esc` or `q` to return to the prompt.

## Clear the conversation

Press `Ctrl+L` twice within two seconds to run `/clear` and start a new conversation. The first press redraws the screen and shows a hint; the second press clears the conversation. On macOS, double-pressing `Cmd+K` also runs `/clear`.

## Use with tmux

Fullscreen rendering works inside tmux, with three caveats.

Mouse wheel scrolling requires tmux's mouse mode. If your `~/.tmux.conf` does not already enable it, add this line and reload your config:

```bash theme={null}
set -g mouse on
```

Without mouse mode, wheel events go to tmux instead of Claude Code. Keyboard scrolling with `PgUp` and `PgDn` works either way. Claude Code prints a one-time hint at startup if it detects tmux with mouse mode off.

Fullscreen rendering is incompatible with iTerm2's tmux integration mode, which is the mode you enter with `tmux -CC`. In integration mode, iTerm2 renders each tmux pane as a native split rather than letting tmux draw to the terminal. The alternate screen buffer and mouse tracking do not work correctly there: the mouse wheel does nothing, and double-click can corrupt the terminal state. Don't enable fullscreen rendering in `tmux -CC` sessions. Regular tmux inside iTerm2, without `-CC`, works fine.

tmux does not support synchronized output, so you may see more flicker during redraws than when running Claude Code directly in your terminal. If the flicker is noticeable, especially over SSH, run Claude Code in its own terminal tab outside tmux.

## Keep native text selection

Mouse capture is the most common friction point, especially over SSH or inside tmux. When Claude Code captures mouse events, your terminal's native copy-on-select stops working. The selection you make with click-and-drag exists inside Claude Code, not in your terminal's selection buffer, so tmux copy mode, Kitty hints, and similar tools don't see it.

Claude Code tries to write the selection to your clipboard, but the path it uses depends on your setup. Inside tmux it writes to the tmux paste buffer. Over SSH it falls back to OSC 52 escape sequences, which some terminals block by default. iTerm2 blocks them until you turn on Settings → General → Selection → Applications in terminal may access clipboard. Running [`/terminal-setup`](/en/terminal-config) in iTerm2 enables this for you. Claude Code prints a toast after each copy telling you which path it used.

For a one-off native selection, hold your terminal's bypass modifier while you click and drag: `Option` in iTerm2, or `Shift` in most Linux and Windows terminals. The modifier tells your terminal to handle the selection itself instead of forwarding mouse events to Claude Code, so `Cmd+C` and your terminal's other copy shortcuts work on it.

If you rely on native selection all the time, set `CLAUDE_CODE_DISABLE_MOUSE=1` to opt out of mouse capture while keeping the flicker-free rendering and flat memory:

```bash theme={null}
CLAUDE_CODE_NO_FLICKER=1 CLAUDE_CODE_DISABLE_MOUSE=1 claude
```

With mouse capture disabled, keyboard scrolling with `PgUp`, `PgDn`, `Ctrl+Home`, and `Ctrl+End` still works, and your terminal handles selection natively. You lose click-to-position-cursor, click-to-expand tool output, URL clicking, and wheel scrolling inside Claude Code.

## Research preview

Fullscreen rendering is a research preview feature. It has been tested on common terminal emulators, but you may encounter rendering issues on less common terminals or unusual configurations.

If you encounter a problem, run `/feedback` inside Claude Code to report it, or open an issue on the [claude-code GitHub repo](https://github.com/anthropics/claude-code/issues). Include your terminal emulator name and version.

To turn fullscreen rendering off, run `/tui default`, or unset `CLAUDE_CODE_NO_FLICKER` if you enabled it that way. To force the classic renderer regardless of the saved `tui` setting, set `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1`. The classic renderer keeps the conversation in your terminal's native scrollback so `Cmd+f` and tmux copy mode work as usual.
