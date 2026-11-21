# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![Beta](https://img.shields.io/badge/status-early%20beta-orange)](https://github.com/ericbuess/claude-code-docs/issues)

Local mirror of Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/, updated every 3 hours.

## ⚠️ Early Beta Notice

**This is an early beta release**. There may be errors or unexpected behavior. If you encounter any issues, please [open an issue](https://github.com/ericbuess/claude-code-docs/issues) - your feedback helps improve the tool!

## 🆕 Version 0.3.3 - Changelog Integration

**New in this version:**
- 📋 **Claude Code Changelog**: Access the official Claude Code release notes with `/docs changelog`
- 🍎 **Full macOS compatibility**: Fixed shell compatibility issues for Mac users
- 🐧 **Linux support**: Tested on Ubuntu, Debian, and other distributions
- 🔧 **Improved installer**: Better handling of updates and edge cases

To update:
```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

## Why This Exists

- **Faster access** - Reads from local files instead of fetching from web
- **Automatic updates** - Attempts to stay current with the latest documentation
- **Track changes** - See what changed in docs over time
- **Claude Code changelog** - Quick access to official release notes and version history
- **Better Claude Code integration** - Allows Claude to explore documentation more effectively

## Platform Compatibility

- ✅ **macOS**: Fully supported (tested on macOS 12+)
- ✅ **Linux**: Fully supported (Ubuntu, Debian, Fedora, etc.)
- ⏳ **Windows**: Not yet supported - [contributions welcome](#contributing)!

### Prerequisites

This tool requires the following to be installed:
- **git** - For cloning and updating the repository (usually pre-installed)
- **jq** - For JSON processing in the auto-update hook (pre-installed on macOS; Linux users may need `apt install jq` or `yum install jq`)
- **curl** - For downloading the installation script (usually pre-installed)
- **Claude Code** - Obviously :)

## Installation

Run this single command:

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

This will:
1. Install to `~/.claude-code-docs` (or migrate existing installation)
2. Create the `/docs` slash command to pass arguments to the tool and tell it where to find the docs
3. Set up a 'PreToolUse' 'Read' hook to enable automatic git pull when reading docs from the ~/.claude-code-docs`

**Note**: The command is `/docs (user)` - it will show in your command list with "(user)" after it to indicate it's a user-created command.

## Usage

The `/docs` command provides instant access to documentation with optional freshness checking.

### Default: Lightning-fast access (no checks)
```bash
/docs hooks        # Instantly read hooks documentation
/docs mcp          # Instantly read MCP documentation
/docs memory       # Instantly read memory documentation
```

You'll see: `📚 Reading from local docs (run /docs -t to check freshness)`

### Check documentation sync status with -t flag
```bash
/docs -t           # Show sync status with GitHub
/docs -t hooks     # Check sync status, then read hooks docs
/docs -t mcp       # Check sync status, then read MCP docs
```

### See what's new
```bash
/docs what's new   # Show recent documentation changes with diffs
```

### Read Claude Code changelog
```bash
/docs changelog    # Read official Claude Code release notes and version history
```

The changelog feature fetches the latest release notes directly from the official Claude Code repository, showing you what's new in each version.

### Uninstall
```bash
/docs uninstall    # Get commnd to remove claude-code-docs completely
```

### Multi-question research with /query

`/query` parses your input into sub-questions, dispatches research subagents in batches of 3 in parallel, and assembles a structured answer file.

```bash
/query What is a hook?                          # single question
/query Explain hooks and MCP, then compare them # multi-part
/query 1. ... 2. ... 3. ...                     # explicit numbering
```

Each query produces a folder under `~/.claude-code-docs/query/QUERY-TASK-<keyword>-<id>/`
containing the full structured answer with citations. Useful for non-trivial questions that span multiple docs.

### Customize command name

If you prefer a different command name (e.g., `/claude-docs` instead of `/docs`), you can easily customize it:

```bash
# Rename the command file
mv ~/.claude/commands/docs.md ~/.claude/commands/claude-docs.md

# Now use /claude-docs instead of /docs
/claude-docs hooks
/claude-docs mcp
```

You can use any name you prefer: `/cdocs`, `/claude-code-docs`, etc. The command file name determines the slash command.

### Creative usage examples
```bash
# Natural language queries work great
/docs what environment variables exist and how do I use them?
/docs explain the differences between hooks and MCP

# Check for recent changes
/docs -t what's new in the latest documentation?
/docs changelog    # Check Claude Code release notes

# Search across all docs
/docs find all mentions of authentication
/docs how do I customize Claude Code's behavior?
```

## How Updates Work

The documentation attempts to stay current:
- GitHub Actions runs periodically to fetch new documentation
- When you use `/docs`, it checks for updates
- Updates are pulled when available
- You may see "🔄 Updating documentation..." when this happens

Note: If automatic updates fail, you can always run the installer again to get the latest version.

## Updating from Previous Versions

Regardless of which version you have installed, simply run:

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

The installer will handle migration and updates automatically.

## Troubleshooting

### Command not found
If `/docs` returns "command not found":
1. Check if the command file exists: `ls ~/.claude/commands/docs.md`
2. Restart Claude Code to reload commands
3. Re-run the installation script

### Documentation not updating
If documentation seems outdated:
1. Run `/docs -t` to check sync status and force an update
2. Manually update: `cd ~/.claude-code-docs && git pull`
3. Check if GitHub Actions are running: [View Actions](https://github.com/ericbuess/claude-code-docs/actions)

### Installation errors
- **"git/jq/curl not found"**: Install the missing tool first
- **"Failed to clone repository"**: Check your internet connection
- **"Failed to update settings.json"**: Check file permissions on `~/.claude/settings.json`

## Uninstalling

To completely remove the docs integration:

```bash
/docs uninstall
```

Or run:
```bash
~/.claude-code-docs/uninstall.sh
```

See [UNINSTALL.md](UNINSTALL.md) for manual uninstall instructions.

## Security Notes

- The installer modifies `~/.claude/settings.json` to add an auto-update hook
- The hook only runs `git pull` when reading documentation files
- All operations are limited to the documentation directory
- No data is sent externally - everything is local
- **Repository Trust**: The installer clones from GitHub over HTTPS. For additional security, you can:
  - Fork the repository and install from your own fork
  - Clone manually and run the installer from the local directory
  - Review all code before installation

## What's New

### v0.3.3 (Latest)
- Added Claude Code changelog integration (`/docs changelog`)
- Fixed shell compatibility for macOS users (zsh/bash)
- Improved documentation and error messages
- Added platform compatibility badges

### v0.3.2
- Fixed automatic update functionality  
- Improved handling of local repository changes
- Better error recovery during updates

## Contributing

**Contributions are welcome!** This is a community project and we'd love your help:

- 🪟 **Windows Support**: Want to help add Windows compatibility? [Fork the repository](https://github.com/ericbuess/claude-code-docs/fork) and submit a PR!
- 🐛 **Bug Reports**: Found something not working? [Open an issue](https://github.com/ericbuess/claude-code-docs/issues)
- 💡 **Feature Requests**: Have an idea? [Start a discussion](https://github.com/ericbuess/claude-code-docs/issues)
- 📝 **Documentation**: Help improve docs or add examples

You can also use Claude Code itself to help build features - just fork the repo and let Claude assist you!

## Known Issues

As this is an early beta, you might encounter some issues:
- Auto-updates may occasionally fail on some network configurations
- Some documentation links might not resolve correctly

If you find any issues not listed here, please [report them](https://github.com/ericbuess/claude-code-docs/issues)!

## License

Documentation content belongs to Anthropic.
This mirror tool is open source - contributions welcome!
