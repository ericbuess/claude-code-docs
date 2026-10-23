> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 13 · March 23–27, 2026

> Auto mode for hands-off permissions, computer use built in, PR auto-fix in the cloud, transcript search, and a PowerShell tool for Windows.

Releases [v2.1.83 → v2.1.85](https://code.claude.com/docs/en/changelog.md#2-1-83)
6 features · March 23–27

Auto mode
research preview

Auto mode hands your permission prompts to a classifier. Safe edits and commands run without interrupting you; anything destructive or suspicious gets blocked and surfaced. It's the middle ground between approving every file write and running with `--dangerously-skip-permissions`.

![Claude Code prompt footer showing 'auto mode on (shift+tab to cycle)' indicator in yellow](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-mode.png?fit=max\&auto=format\&n=CfffsX01JHFnIKvD\&q=85\&s=367c9e9d4ba5bc57ec4b935154bf1fbb)

Cycle to auto with Shift+Tab, or set it as your default:

```json ~/.claude/settings.json {3} theme={null}
{
  "permissions": {
    "defaultMode": "auto"
  }
}
```

[Permission modes guide](https://code.claude.com/docs/en/permission-modes.md)

Computer use
Desktop

Claude can now control your actual desktop from the Claude Code Desktop app: open native apps, click through the iOS simulator, drive hardware control panels, and verify changes on screen. It's off by default and asks before each action. Best for the things nothing else can reach: apps without an API, proprietary tools, anything that only exists as a GUI.

![Claude Desktop settings with the Computer use toggle enabled, showing the option to let Claude take screenshots and control your keyboard and mouse in apps you allow](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/computer-use.png?fit=max\&auto=format\&n=CfffsX01JHFnIKvD\&q=85\&s=d631de2017edafff463505f8ddbc0f51)

Enable it in Settings, grant the OS permissions, then ask Claude to verify a change end to end:

```text title="Claude Code" wrap theme={null}
Open the iOS simulator, tap through the onboarding flow, and screenshot each step
```

[Computer use guide](https://code.claude.com/docs/en/desktop.md#let-claude-use-your-computer)

PR auto-fix
Web

Flip a switch when you open a PR and walk away. Claude watches CI, fixes the failures, handles the nits, and pushes until it's green. No more babysitting a PR through six rounds of lint errors.

![Claude Code web CI panel showing the Auto fix toggle enabled, with description 'Proactively fix CI failures and review comments'](https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/auto-fix.png?fit=max\&auto=format\&n=CfffsX01JHFnIKvD\&q=85\&s=c62b181c6c5d96929f0b43525f9f3584)

After creating a PR on Claude Code web, toggle Auto fix in the CI panel.

[Auto-fix pull requests](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests)

Transcript search
v2.1.83

Press `/` in transcript mode to search your conversation. `n` and `N` step through matches. Finally a way to find that one Bash command Claude ran 400 messages ago.

Open transcript mode and search:

```text Claude Code theme={null}
Ctrl+O    # open transcript
/migrate  # search for "migrate"
n         # next match
N         # previous match
```

[Fullscreen guide](https://code.claude.com/docs/en/fullscreen.md#search-and-review-the-conversation)

PowerShell tool
preview
v2.1.84

Windows gets a native PowerShell tool alongside Bash. Claude can run cmdlets, pipe objects, and work with Windows-native paths without translating everything through Git Bash.

Opt in from settings:

```json .claude/settings.json {3} theme={null}
{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}
```

[PowerShell tool docs](https://code.claude.com/docs/en/tools-reference.md#powershell-tool)

Conditional hooks
v2.1.85

Hooks can now declare an `if` field using permission rule syntax. Your pre-commit check only spawns for `Bash(git commit *)` instead of every bash call, cutting the process overhead on busy sessions.

Scope a hook to git commits only:

```json .claude/settings.json {5} theme={null}
{
  "hooks": {
    "PreToolUse": [{
      "hooks": [{
        "if": "Bash(git commit *)",
        "type": "command",
        "command": ".claude/hooks/lint-staged.sh"
      }]
    }]
  }
}
```

[Hooks reference](https://code.claude.com/docs/en/hooks.md)

Other wins

Plugin `userConfig` now public: prompt for settings at enable time, keychain-backed secretsPasted images insert `[Image #N]` chips you can reference positionally`managed-settings.d/` drop-in directory for layered policy fragments`CwdChanged` and `FileChanged` hook events for direnv-style setupsAgents can declare `initialPrompt` in frontmatter to auto-submit a first turn`Ctrl+X Ctrl+E` opens your external editor, matching readlineInterrupting before any response restores your input automatically`/status` now works while Claude is respondingDeep links open in your preferred terminal, not first-detectedIdle-return nudge to `/clear` after 75+ minutes awayVS Code: rate limit banner, Esc-twice rewind picker

[Full changelog for v2.1.83–v2.1.85 →](https://code.claude.com/docs/en/changelog.md#2-1-83)
