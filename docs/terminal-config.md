> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure your terminal for Claude Code

> Fix Shift+Enter for newlines, get a terminal bell when Claude finishes, configure tmux, match the color theme, and enable Vim mode in the Claude Code CLI.

Claude Code works in any terminal without configuration. This page is for when something specific is not behaving the way you expect. Find your symptom below. If everything already feels right, you do not need this page.

* [Shift+Enter submits instead of inserting a newline](#enter-multiline-prompts)
* [Option-key shortcuts do nothing on macOS](#enable-option-key-shortcuts-on-macos)
* [No sound or alert when Claude finishes](#get-a-terminal-bell-or-notification)
* [You run Claude Code inside tmux](#configure-tmux)
* [Display flickers or scrollback jumps](#switch-to-fullscreen-rendering)
* [You want Vim keys in the prompt](#edit-prompts-with-vim-keybindings)

This page is about getting your terminal to send the right signals to Claude Code. To change which keys Claude Code itself responds to, see [keybindings](/en/keybindings) instead.

## Enter multiline prompts

Pressing Enter submits your message. To add a line break without submitting, press Ctrl+J, or type `\` and then press Enter. Both work in every terminal with no setup.

In most terminals you can also press Shift+Enter, but support varies by terminal emulator:

| Terminal                                                                            | Shift+Enter for newline                     |
| :---------------------------------------------------------------------------------- | :------------------------------------------ |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                               | Works without setup                         |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                           | Run `/terminal-setup` once                  |
| Windows Terminal, gnome-terminal, JetBrains IDEs such as PyCharm and Android Studio | Not available; use Ctrl+J or `\` then Enter |

For VS Code, Cursor, Windsurf, Alacritty, and Zed, `/terminal-setup` writes Shift+Enter and other keybindings into the terminal's configuration file. In VS Code, Cursor, and Windsurf it also sets `terminal.integrated.mouseWheelScrollSensitivity` in the editor settings for smoother scrolling in [fullscreen mode](/en/fullscreen). Existing bindings and settings are left in place; if you see a message such as `VSCode terminal Shift+Enter key binding already configured`, no change was made. Run `/terminal-setup` directly in the host terminal rather than inside tmux or screen, since it needs to write to the host terminal's configuration.

If you are running inside tmux, Shift+Enter also requires the [tmux configuration below](#configure-tmux) even when the outer terminal supports it.

To bind newline to a different key, or to swap behavior so Enter inserts a newline and Shift+Enter submits, map the `chat:newline` and `chat:submit` actions in your [keybindings file](/en/keybindings).

## Enable Option key shortcuts on macOS

Some Claude Code shortcuts use the Option key, such as Option+Enter for a newline or Option+P to switch models. On macOS, most terminals do not send Option as a modifier by default, so these shortcuts do nothing until you enable it. The terminal setting for this is usually labeled "Use Option as Meta Key"; Meta is the historical Unix name for the key now labeled Option or Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Open Settings → Profiles → Keyboard and check "Use Option as Meta Key".

    If you accepted Claude Code's first-run prompt that offered "Option+Enter for newlines and visual bell", this is already done. That prompt runs `/terminal-setup` for you, which enables Option as Meta and switches the audio bell to a visual screen flash in your Apple Terminal profile.
  </Tab>

  <Tab title="iTerm2">
    Open Settings → Profiles → Keys → General and set Left Option key and Right Option key to "Esc+".

    Running `/terminal-setup` in iTerm2 enables "Applications in terminal may access clipboard" under Settings → General → Selection so the `/copy` command can write to your system clipboard. The command detects iTerm2 even when run from inside tmux. Restart iTerm2 for the change to take effect.
  </Tab>

  <Tab title="VS Code">
    Add `"terminal.integrated.macOptionIsMeta": true` to your VS Code settings.
  </Tab>
</Tabs>

For Ghostty, Kitty, and other terminals, look for an Option-as-Alt or Option-as-Meta setting in the terminal's configuration file.

## Get a terminal bell or notification

When Claude finishes a task or pauses for a permission prompt, it fires a notification event. Surfacing this as a terminal bell or desktop notification lets you switch to other work while a long task runs.

By default Claude Code sends a desktop notification only in Ghostty, Kitty, and iTerm2. In other terminals, set [`preferredNotifChannel`](/en/settings#available-settings) to `"terminal_bell"` to ring the terminal bell instead, or configure a [Notification hook](#play-a-sound-with-a-notification-hook) for a custom sound or command.

The desktop notification reaches your local machine over SSH, so a remote session can still alert you. Ghostty and Kitty forward it to your OS notification center without further setup. iTerm2 requires you to enable forwarding:

<Steps>
  <Step title="Open iTerm2 notification settings">
    Go to Settings → Profiles → Terminal.
  </Step>

  <Step title="Enable alerts">
    Check "Notification Center Alerts", then click "Filter Alerts" and enable "Send escape sequence-generated alerts".
  </Step>
</Steps>

If notifications still do not appear, confirm that your terminal application has notification permission in your OS settings, and if you are running inside tmux, [enable passthrough](#configure-tmux).

### Play a sound with a Notification hook

In any terminal you can configure a [Notification hook](/en/hooks-guide#get-notified-when-claude-needs-input) to play a sound or run a custom command when Claude needs your attention. Hooks run alongside the built-in notification rather than replacing it, so terminals that do not receive a desktop notification, such as Warp or the VS Code integrated terminal, can use a hook or set `preferredNotifChannel` to `"terminal_bell"` instead.

The example below plays a system sound on macOS. The linked guide has desktop notification commands for macOS, Linux, and Windows.

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Configure tmux

When Claude Code runs inside tmux, two things break by default: Shift+Enter submits instead of inserting a newline, and desktop notifications and the [progress bar](/en/settings#available-settings) never reach the outer terminal. Add these lines to `~/.tmux.conf`, then run `tmux source-file ~/.tmux.conf` to apply them to the running server:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

The `allow-passthrough` line lets notifications and progress updates reach iTerm2, Ghostty, or Kitty instead of being swallowed by tmux. The `extended-keys` lines let tmux distinguish Shift+Enter from plain Enter so the newline shortcut works.

## Match the color theme

Use the `/theme` command, or the theme picker in `/config`, to choose a Claude Code theme that matches your terminal. Selecting the auto option detects your terminal's light or dark background, so the theme follows OS appearance changes whenever your terminal does. Claude Code does not control the terminal's own color scheme, which is set by the terminal application.

To customize what appears at the bottom of the interface, configure a [custom status line](/en/statusline) that shows the current model, working directory, git branch, or other context.

### Create a custom theme

<Note>
  Custom themes require Claude Code v2.1.118 or later.
</Note>

In addition to the built-in presets, `/theme` lists any custom themes you have defined and any themes contributed by installed [plugins](/en/plugins-reference#themes). Select **New custom theme…** at the end of the list to create one interactively: you name the theme, then pick individual color tokens to override. Press `Ctrl+E` while a custom theme is highlighted to edit it.

Each custom theme is a JSON file in `~/.claude/themes/`. The filename without the `.json` extension is the theme's slug, and selecting the theme stores `custom:<slug>` as your theme preference. The file has three optional fields:

| Field       | Type   | Description                                                                                                                                     |
| :---------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | string | Display label shown in `/theme`. Defaults to the filename slug                                                                                  |
| `base`      | string | Built-in preset the theme starts from: `dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi`, or `light-ansi`. Defaults to `dark` |
| `overrides` | object | Map of color token names to color values. Tokens not listed here fall through to the base preset                                                |

Color values accept `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, or `ansi:<name>` where `<name>` is one of the 16 standard ANSI color names such as `red` or `cyanBright`. Unknown tokens and invalid color values are ignored, so a typo cannot break rendering.

The following example defines a theme that keeps the dark preset but recolors the prompt accent, error text, and success text:

```json ~/.claude/themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Claude Code watches `~/.claude/themes/` and reloads when a file changes, so edits made in your editor apply to a running session without a restart.

The reference below covers the tokens you can set in `overrides`. The interactive editor in `/theme` shows the same tokens with a live preview, plus a few single-purpose accents such as onboarding screen colors that are omitted here.

<Accordion title="Color token reference">
  The following example combines tokens from several of the groups below: the brand accent, the plan mode border, the diff backgrounds, and the fullscreen message background.

  ```json ~/.claude/themes/midnight.json theme={null}
  {
    "name": "Midnight",
    "base": "dark",
    "overrides": {
      "claude": "#a78bfa",
      "planMode": "#38bdf8",
      "diffAdded": "#14532d",
      "diffRemoved": "#7f1d1d",
      "userMessageBackground": "#1e1b4b"
    }
  }
  ```

  #### Text and accent colors

  Control the primary brand accent and the foreground text shades used throughout the interface.

  | Token         | Controls                                                         |
  | :------------ | :--------------------------------------------------------------- |
  | `claude`      | Primary brand accent, used for the spinner and assistant label   |
  | `text`        | Default foreground text                                          |
  | `inverseText` | Text drawn on top of a colored background, such as status badges |
  | `inactive`    | Secondary text such as hints, timestamps, and disabled items     |
  | `subtle`      | Faint borders and de-emphasized secondary text                   |
  | `suggestion`  | Autocomplete suggestions and selection highlight in pickers      |
  | `permission`  | Dialog borders, including permission prompts and pickers         |
  | `remember`    | Memory and `CLAUDE.md` indicators                                |

  #### Status colors

  Signal success, failure, and warning states across messages and indicators.

  | Token     | Controls                                             |
  | :-------- | :--------------------------------------------------- |
  | `success` | Success messages and passing checks                  |
  | `error`   | Error messages and failures                          |
  | `warning` | Warnings, caution messages, and the auto mode border |
  | `merged`  | Merged pull request status                           |

  #### Input box and mode indicators

  Set the input box border color and the accent shown while a permission mode or indicator is active.

  | Token          | Controls                                           |
  | :------------- | :------------------------------------------------- |
  | `promptBorder` | Input box border in the default permission mode    |
  | `planMode`     | Plan mode accent and border                        |
  | `autoAccept`   | Accept-edits mode accent and border                |
  | `bashBorder`   | Input box border when entering a `!` shell command |
  | `ide`          | IDE connection indicator                           |
  | `fastMode`     | Fast mode indicator                                |

  #### Diff rendering

  Color added and removed code in file edits and reviews.

  | Token               | Controls                                           |
  | :------------------ | :------------------------------------------------- |
  | `diffAdded`         | Background of added lines                          |
  | `diffRemoved`       | Background of removed lines                        |
  | `diffAddedDimmed`   | Background of unchanged context near added lines   |
  | `diffRemovedDimmed` | Background of unchanged context near removed lines |
  | `diffAddedWord`     | Word-level highlight within an added line          |
  | `diffRemovedWord`   | Word-level highlight within a removed line         |

  #### Fullscreen mode

  Apply only in [fullscreen rendering mode](/en/fullscreen), where messages have a background fill.

  | Token                        | Controls                                                           |
  | :--------------------------- | :----------------------------------------------------------------- |
  | `userMessageBackground`      | Background behind your messages in the transcript                  |
  | `userMessageBackgroundHover` | Background behind a message while hovered or expanded              |
  | `messageActionsBackground`   | Background behind the selected message when the action bar is open |
  | `bashMessageBackgroundColor` | Background behind `!` shell command entries in the transcript      |
  | `memoryBackgroundColor`      | Background behind `#` memory entries in the transcript             |
  | `selectionBg`                | Background of text selected with the mouse                         |

  #### Usage meter and speaker labels

  Adjust the bar shown in the `/usage` view and the labels that distinguish your messages from Claude's.

  | Token              | Controls                                          |
  | :----------------- | :------------------------------------------------ |
  | `rate_limit_fill`  | Filled portion of the usage meter                 |
  | `rate_limit_empty` | Unfilled portion of the usage meter               |
  | `briefLabelYou`    | Color of the `You` label on your messages         |
  | `briefLabelClaude` | Color of the `Claude` label on assistant messages |

  #### Shimmer variants and subagent colors

  Several tokens have a paired shimmer variant that supplies the lighter color used in the spinner's animated gradient. Override the shimmer alongside its base token if the animation looks mismatched.

  * `claude` and `claudeShimmer`
  * `warning` and `warningShimmer`
  * `permission` and `permissionShimmer`
  * `promptBorder` and `promptBorderShimmer`
  * `inactive` and `inactiveShimmer`
  * `fastMode` and `fastModeShimmer`

  Each [subagent](/en/sub-agents) and parallel task is shown in one of eight named colors so you can tell them apart in the transcript. The token names follow the pattern `<color>_FOR_SUBAGENTS_ONLY`, where `<color>` is `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`. Override these to change what each named color looks like. For example, a subagent with `color: blue` in its definition is drawn using the `blue_FOR_SUBAGENTS_ONLY` value.

  The [`ultrathink`](/en/model-config#use-ultrathink-for-one-off-deep-reasoning) and [`ultraplan`](/en/ultraplan) keywords in the prompt input are rendered with a seven-color rainbow gradient. The token names follow the pattern `rainbow_<color>` and `rainbow_<color>_shimmer`, where `<color>` is `red`, `orange`, `yellow`, `green`, `blue`, `indigo`, or `violet`.
</Accordion>

## Switch to fullscreen rendering

If the display flickers or the scroll position jumps while Claude is working, switch to [fullscreen rendering mode](/en/fullscreen). It draws to a separate screen the terminal reserves for full-screen apps instead of appending to your normal scrollback, which keeps memory usage flat and adds mouse support for scrolling and selection. In this mode you scroll with the mouse or PageUp inside Claude Code rather than with your terminal's native scrollback; see the [fullscreen page](/en/fullscreen#search-and-review-the-conversation) for how to search and copy.

Run `/tui fullscreen` to switch in the current session with your conversation intact. To make it the default, set the `CLAUDE_CODE_NO_FLICKER` environment variable before starting Claude Code:

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## Paste large content

When you paste more than 10,000 characters into the prompt, Claude Code collapses the input to a `[Pasted text]` placeholder so the input box stays usable. The full content is still sent to Claude when you submit.

The VS Code integrated terminal can drop characters from very large pastes before they reach Claude Code, so prefer file-based workflows there. For very large inputs such as entire files or long logs, write the content to a file and ask Claude to read it instead of pasting. This keeps the conversation transcript readable and lets Claude reference the file by path in later turns.

## Edit prompts with Vim keybindings

Claude Code includes a Vim-style editing mode for the prompt input. Enable it through `/config` → Editor mode, or by setting [`editorMode`](/en/settings#available-settings) to `"vim"` in `~/.claude/settings.json`. Set Editor mode back to `normal` to turn it off.

Vim mode supports a subset of NORMAL- and VISUAL-mode motions and operators, such as `hjkl` navigation, `v`/`V` selection, and `d`/`c`/`y` with text objects. See the [Vim editor mode reference](/en/interactive-mode#vim-editor-mode) for the full key table. Vim motions are not remappable through the keybindings file.

Pressing Enter still submits your prompt in INSERT mode, unlike standard Vim. Use `o` or `O` in NORMAL mode, or Ctrl+J, to insert a newline instead.

## Related resources

* [Interactive mode](/en/interactive-mode): full keyboard shortcut reference and the Vim key table
* [Keybindings](/en/keybindings): remap any Claude Code shortcut, including Enter and Shift+Enter
* [Fullscreen rendering](/en/fullscreen): details on scrolling, search, and copy in fullscreen mode
* [Hooks guide](/en/hooks-guide): more Notification hook examples for Linux and Windows
* [Troubleshooting](/en/troubleshooting): fixes for issues outside terminal configuration
