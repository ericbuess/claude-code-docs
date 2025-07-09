# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Local mirror of Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/, updated every 3 hours.

## Why This Exists

- **Faster than web fetching** - Read from local files instantly
- **Works offline** - No internet required after cloning
- **Always up-to-date** - Auto-updates every 3 hours via GitHub Actions

## Prerequisites

This tool requires the following to be installed:
- **git** - For cloning and updating the repository
- **jq** - For JSON processing in the auto-update hook
- **curl** - For downloading the installation script
- **Claude Code** - Obviously :)

**Platform Support**: Currently macOS only. Linux support contributions welcome!

## Installation

Run this single command from wherever you want to store the docs:

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

This will:
1. Clone the repository (or use existing if found)
2. Create the `/user:docs` slash command
3. Set up automatic git pull when reading docs

**Note**: The command is `/user:docs` (not `/docs`). If you have a different docs command from another installation, both will coexist.

## Usage

The `/user:docs` command provides instant access to documentation with optional freshness checking.

### Default: Lightning-fast access (no checks)
```bash
/user:docs hooks        # Instantly read hooks documentation
/user:docs mcp          # Instantly read MCP documentation  
/user:docs memory       # Instantly read memory documentation
```

You'll see: `📚 Reading from local docs (run /user:docs -t to check freshness)`

### Optional: Check documentation freshness with -t flag
```bash
/user:docs -t           # Show when docs were last updated
/user:docs -t hooks     # Check freshness, then read hooks docs
/user:docs -t mcp       # Check freshness, then read MCP docs
```

The `-t` flag shows:
- When GitHub last updated the docs
- When your local copy last synced
- Triggers a sync if it's been 3+ hours

### Creative usage examples
```bash
# Natural language queries work great
/user:docs what environment variables exist and how do I use them?
/user:docs explain the differences between hooks and MCP

# Check for recent changes
/user:docs -t what's new in the latest documentation?

# Search across all docs
/user:docs find all mentions of authentication
/user:docs how do I customize Claude Code's behavior?
```

### Performance notes
- **Default mode**: Zero overhead - reads docs instantly
- **With -t flag**: Checks timestamps and syncs if needed (only every 3 hours)
- **Error handling**: If docs are missing, you'll see instructions to reinstall

## How Updates Work

The docs automatically stay up-to-date:
- GitHub Actions updates the repository every 3 hours
- The hook compares GitHub's timestamp with your local sync time
- If GitHub has newer content, it automatically syncs before reading
- You'll see "🔄 Updating docs to latest version..." when this happens
- No manual updates needed!

**Performance**: 
- `/user:docs` reads instantly and the hook ensures content is always current
- `/user:docs -t` shows you exact timestamps of GitHub updates vs local sync

## Troubleshooting

### Command not found
If `/user:docs` returns "command not found":
1. Check if the command file exists: `ls ~/.claude/commands/docs.md`
2. Restart Claude Code to reload commands
3. Re-run the installation script

### Documentation not updating
If documentation seems outdated:
1. Run `/user:docs -t` to check sync status and force an update
2. Manually update: `cd /path/to/claude-code-docs && git pull`
3. Check if GitHub Actions are running: [View Actions](https://github.com/ericbuess/claude-code-docs/actions)

### Installation errors
- **"git/jq/curl not found"**: Install the missing tool first
- **"Failed to clone repository"**: Check your internet connection
- **"Failed to update settings.json"**: Check file permissions on `~/.claude/settings.json`

### Hook not working
If docs aren't auto-updating:
1. Check your Claude settings: `cat ~/.claude/settings.json | jq .hooks`
2. Look for error messages when using `/user:docs`
3. Re-run the installer to reset the hook

## Uninstalling

To completely remove the docs integration:

1. **Remove the command file:**
   ```bash
   rm ~/.claude/commands/docs.md
   ```

2. **Remove the auto-update hook:**
   - Run `/hooks` in Claude Code
   - Find "PreToolUse - Matcher: Read"
   - Select the hook and remove it

3. **Delete the repository:**
   ```bash
   rm -rf /path/to/claude-code-docs
   ```

## Security Notes

- The installer modifies `~/.claude/settings.json` to add an auto-update hook
- The hook only runs `git pull` when reading documentation files
- All operations are limited to the documentation directory
- No data is sent externally - everything is local
- **Repository Trust**: The installer clones from GitHub over HTTPS. For additional security, you can:
  - Fork the repository and install from your own fork
  - Clone manually and run the installer from the local directory
  - Review all code before installation

## License

Documentation content belongs to Anthropic.