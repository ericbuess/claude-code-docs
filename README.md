# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/costiash/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/costiash/claude-code-docs/commits/main)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-blue)]()
[![Beta](https://img.shields.io/badge/status-early%20beta-orange)](https://github.com/costiash/claude-code-docs/issues)
[![Tests](https://img.shields.io/badge/tests-566%20passing-success)](https://github.com/costiash/claude-code-docs/actions)

Local mirror of Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/, updated every 3 hours.

**Enhanced Edition:** This is an enhanced fork of [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) with extended features. The standard edition (270 files, shell-only) remains fully compatible, with optional enhanced mode (449 paths, Python-powered) for advanced features.

## ⚠️ Early Beta Notice

**This is an early beta release**. There may be errors or unexpected behavior. If you encounter any issues, please [open an issue](https://github.com/costiash/claude-code-docs/issues) - your feedback helps improve the tool!

## 🆕 Current Version: 0.3.4 - Enhanced Edition

**Key Features:**
- 🚀 **Extended Coverage**: 449 documentation paths across 270 files (enhanced mode provides access to all URL paths)
- 🔍 **Full-Text Search**: Search across all documentation content
- ✅ **Validation Tools**: Verify documentation integrity and reachability
- 📚 **Seven Categories**: Core docs, API reference, Claude Code, prompt library, resources, release notes, and more
- 🎯 **Dual-Mode Support**: Choose between standard (shell-only) or enhanced (Python-powered) modes during installation

> **Note:** The difference between "270 files" and "449 paths" - There are 270 physical markdown files in the `docs/` directory. The enhanced edition's manifest (`paths_manifest.json`) tracks 449 unique URL paths from the Anthropic documentation site. Some documentation paths don't have corresponding local files yet, but the enhanced mode can fetch them on-demand or validate their existence.

**Latest Updates (v0.3.4 - Enhanced Edition):**
- Extended documentation coverage to 449 paths across 7 categories
- Added full-text search capabilities (enhanced mode)
- Added validation tools for documentation integrity
- Dual-mode support: standard (shell-only) vs enhanced (Python-powered)

**Previous Releases:**

**v0.3.3 (Upstream):**
- Added Claude Code changelog integration (`/docs changelog`)
- Fixed shell compatibility for macOS users (zsh/bash)
- Improved documentation and error messages
- Added platform compatibility badges

**v0.3.2:**
- Fixed automatic update functionality
- Improved handling of local repository changes
- Better error recovery during updates

See [enhancements/](enhancements/) for complete feature documentation, capabilities, and usage examples.

**To install or update:**
```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

The installer handles fresh installations, migrations, and updates automatically.

## Why This Exists

- **Faster access** - Reads from local files instead of fetching from web
- **Extended coverage** - 449 paths across 7 documentation categories (enhanced mode)
- **Full-text search** - Find content across all documentation instantly (enhanced mode)
- **Automatic updates** - Attempts to stay current with the latest documentation
- **Track changes** - See what changed in docs over time
- **Claude Code changelog** - Quick access to official release notes and version history
- **Better Claude Code integration** - Allows Claude to explore documentation more effectively

## Platform Compatibility

- ✅ **macOS**: Fully supported (tested on macOS 12+)
- ✅ **Linux**: Fully supported (Ubuntu, Debian, Fedora, etc.)
- ⏳ **Windows**: Not yet supported - [contributions welcome](#contributing)!

### Prerequisites

**Standard mode:**
- **git** - For cloning and updating the repository (usually pre-installed)
- **jq** - For JSON processing in the auto-update hook (pre-installed on macOS; Linux users may need `apt install jq` or `yum install jq`)
- **curl** - For downloading the installation script (usually pre-installed)
- **Claude Code** - Obviously :)

**Enhanced mode** (optional, for advanced features):
- **Python 3.12+** - For full-text search and validation tools
- All standard mode prerequisites

## Installation

Run this single command:

```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

This will:
1. Install to `~/.claude-code-docs` (or migrate existing installation)
2. Create the `/docs` slash command to pass arguments to the tool and tell it where to find the docs
3. Set up a 'PreToolUse' 'Read' hook to enable automatic git pull when reading docs from the ~/.claude-code-docs`

**Note**: The command is `/docs (user)` - it will show in your command list with "(user)" after it to indicate it's a user-created command.

## Usage

The `/docs` command provides instant access to documentation with optional freshness checking.

### Basic Commands

**Quick access (default - no freshness check):**
```bash
/docs hooks        # Instantly read hooks documentation
/docs mcp          # Instantly read MCP documentation
/docs memory       # Instantly read memory documentation
```

You'll see: `📚 Reading from local docs (run /docs -t to check freshness)`

**With freshness check (using -t flag):**
```bash
/docs -t           # Show sync status with GitHub
/docs -t hooks     # Check sync status, then read hooks docs
/docs -t mcp       # Check sync status, then read MCP docs
```

**Special commands:**
```bash
/docs what's new   # Show recent documentation changes with diffs
/docs changelog    # Read official Claude Code release notes and version history
/docs uninstall    # Get command to remove claude-code-docs completely
```

### Natural Language Queries

The `/docs` command works great with natural language - just ask what you need:

```bash
# Ask questions directly
/docs what environment variables exist and how do I use them?
/docs explain the differences between hooks and MCP
/docs how do I customize Claude Code's behavior?

# Search for specific topics
/docs find all mentions of authentication
/docs show me everything about memory features

# Combine with freshness checks
/docs -t what's new in the latest documentation?
/docs -t are there updates to the API reference?
```

## How Updates Work

The documentation attempts to stay current through multiple mechanisms:

1. **Automatic updates**: GitHub Actions runs periodically to fetch new documentation
2. **Pre-command check**: When you use `/docs`, it checks for updates from GitHub
3. **Auto-pull**: Updates are automatically pulled when available
4. **Visual feedback**: You may see "🔄 Updating documentation..." when updates occur

**Manual update:** If automatic updates fail, re-run the installer:
```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

The installer handles fresh installations, migrations from previous versions, and updates automatically.

## Troubleshooting & FAQ

### Command not found
**Problem:** `/docs` returns "command not found"

**Solution:**
1. Check if the command file exists: `ls ~/.claude/commands/docs.md`
2. Restart Claude Code to reload commands
3. Re-run the installation script if needed

### Documentation not updating
**Problem:** Documentation seems outdated or not syncing

**Solution:**
1. Run `/docs -t` to check sync status and force an update
2. Manually update: `cd ~/.claude-code-docs && git pull`
3. Check if GitHub Actions are running: [View Actions](https://github.com/ericbuess/claude-code-docs/actions)
4. Re-run the installer as a last resort

### Installation errors
**Common issues and solutions:**
- **"git/jq/curl not found"**: Install the missing tool first (see [Prerequisites](#prerequisites))
- **"Failed to clone repository"**: Check your internet connection and GitHub access
- **"Failed to update settings.json"**: Check file permissions on `~/.claude/settings.json`

### Which version do I have?
Check your installation:
```bash
cat ~/.claude-code-docs/README.md | grep "Version"
```

Or check the helper script version:
```bash
~/.claude-code-docs/claude-docs-helper.sh --version
```

### How do I switch between standard and enhanced modes?
Re-run the installer and choose your preferred mode:
```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

Enhanced mode requires Python 3.12+ and provides additional features like full-text search.

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
