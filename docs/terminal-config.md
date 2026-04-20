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

For VS Code, Cursor, Windsurf, Alacritty, and Zed, `/terminal-setup` writes Shift+Enter and other keybindings into the terminal's configuration file. If it reports a conflict such as `Found existing VSCode terminal Shift+Enter key binding`, remove that entry from the terminal's own keybindings file, for example VS Code's `keybindings.json`, and run the command again. Run `/terminal-setup` directly in the host terminal rather than inside tmux or screen, since it needs to write to the host terminal's configuration.

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
  </Tab>

  <Tab title="VS Code">
    Add `"terminal.integrated.macOptionIsMeta": true` to your VS Code settings.
  </Tab>
</Tabs>

For Ghostty, Kitty, and other terminals, look for an Option-as-Alt or Option-as-Meta setting in the terminal's configuration file.

## Get a terminal bell or notification

When Claude finishes a task or pauses for a permission prompt, it fires a notification event. Surfacing this as a terminal bell or desktop notification lets you switch to other work while a long task runs.

Claude Code sends a desktop notification only in Ghostty, Kitty, and iTerm2; every other terminal needs a [Notification hook](#play-a-sound-with-a-notification-hook) instead. The notification also reaches your local machine over SSH, so a remote session can still alert you. Ghostty and Kitty forward it to your OS notification center without further setup. iTerm2 requires you to enable forwarding:

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

In any terminal you can configure a [Notification hook](/en/hooks-guide#get-notified-when-claude-needs-input) to play a sound or run a custom command when Claude needs your attention. Hooks run alongside the desktop notification rather than replacing it. Terminals such as Warp or Apple Terminal rely on a hook alone since Claude Code does not send them a desktop notification.

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

When Claude Code runs inside tmux, two things break by default: Shift+Enter submits instead of inserting a newline, and desktop notifications and the [progress bar](/en/settings#global-config-settings) never reach the outer terminal. Add these lines to `~/.tmux.conf`, then run `tmux source-file ~/.tmux.conf` to apply them to the running server:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

The `allow-passthrough` line lets notifications and progress updates reach iTerm2, Ghostty, or Kitty instead of being swallowed by tmux. The `extended-keys` lines let tmux distinguish Shift+Enter from plain Enter so the newline shortcut works.

## Match the color theme

Use the `/theme` command, or the theme picker in `/config`, to choose a Claude Code theme that matches your terminal. Selecting the auto option detects your terminal's light or dark background, so the theme follows OS appearance changes whenever your terminal does. The available themes are built in; there is no custom theme file. Claude Code does not control the terminal's own color scheme, which is set by the terminal application.

To customize what appears at the bottom of the interface, configure a [custom status line](/en/statusline) that shows the current model, working directory, git branch, or other context.

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

Claude Code includes a Vim-style editing mode for the prompt input. Enable it through `/config` → Editor mode, or by setting the [`editorMode`](/en/settings#global-config-settings) global config key to `"vim"` in `~/.claude.json`. Set Editor mode back to `normal` to turn it off.

Vim mode supports a subset of NORMAL-mode motions and operators, such as `hjkl` navigation and `d`/`c`/`y` with text objects. See the [Vim editor mode reference](/en/interactive-mode#vim-editor-mode) for the full key table. Vim motions are not remappable through the keybindings file.

Pressing Enter still submits your prompt in INSERT mode, unlike standard Vim. Use `o` or `O` in NORMAL mode, or Ctrl+J, to insert a newline instead.

## Related resources

* [Interactive mode](/en/interactive-mode): full keyboard shortcut reference and the Vim key table
* [Keybindings](/en/keybindings): remap any Claude Code shortcut, including Enter and Shift+Enter
* [Fullscreen rendering](/en/fullscreen): details on scrolling, search, and copy in fullscreen mode
* [Hooks guide](/en/hooks-guide): more Notification hook examples for Linux and Windows
* [Troubleshooting](/en/troubleshooting): fixes for issues outside terminal configuration
