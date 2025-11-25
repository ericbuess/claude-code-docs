# Uninstalling Claude Code Documentation Mirror

## Quick Uninstall

### For v0.3+ (installed at ~/.claude-code-docs)

From anywhere, run:
```bash
~/.claude-code-docs/uninstall.sh
```

Or use the docs command:
```bash
/docs uninstall
```

### For v0.2 or older (custom installation locations)

Navigate to your installation directory and run:
```bash
./uninstall.sh
```

## What Gets Removed

The uninstaller will remove:

1. **The /docs command** from `~/.claude/commands/docs.md`
2. **Any legacy hooks** from `~/.claude/settings.json` (if present from older versions)
3. **The installation directory**:
   - v0.3+: `~/.claude-code-docs`
   - v0.2 or older: wherever you installed it

## Manual Uninstall

If you prefer to uninstall manually:

### 1. Remove the command file:
```bash
rm -f ~/.claude/commands/docs.md
```

### 2. Remove any legacy hooks from Claude settings (if present):
If you installed an older version (v0.4.1 or earlier), check `~/.claude/settings.json` and remove any PreToolUse hooks that reference claude-code-docs. Current versions (v0.4.2+) do not install hooks.

### 3. Remove the installation directory:

For v0.3+:
```bash
rm -rf ~/.claude-code-docs
```

For older versions:
```bash
rm -rf /path/to/your/claude-code-docs
```

## Multiple Installations

If you have multiple installations (e.g., from testing different versions), the uninstaller will notify you about other locations it finds. You'll need to remove each one separately.

To find all installations:
```bash
find ~ -name "claude-code-docs" -type d 2>/dev/null | grep -v ".claude-code-docs"
```

## Backup Created

The uninstaller may create a backup of your Claude settings at `~/.claude/settings.json.backup` before removing hooks, just in case.

## Complete Removal

After uninstalling, there should be no traces left except:
- The backup file `~/.claude/settings.json.backup` (if hooks were removed)
- Any custom files you added to the installation directory

## Reinstalling

To reinstall after uninstalling:
```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```
