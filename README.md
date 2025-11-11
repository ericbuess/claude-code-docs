# Claude Code Documentation Tool

[![Last Update](https://img.shields.io/github/last-commit/costiash/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/costiash/claude-code-docs/commits/main)
[![Tests](https://img.shields.io/badge/tests-573%20passing-success)](https://github.com/costiash/claude-code-docs/actions)
[![Coverage](https://img.shields.io/badge/coverage-72%25-green)](https://github.com/costiash/claude-code-docs)
[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey)](https://github.com/costiash/claude-code-docs)

> **⭐ This is an enhanced fork of [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)**
>
> This project builds upon Eric Buess's excellent foundation, adding enhanced search capabilities, extended documentation coverage, and validation tools. All credit for the original concept and implementation goes to the upstream repository.
>
> **For the original, simpler implementation, see [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)**

---

**Comprehensive local documentation for Claude Code with instant search and validation.**

Stop hunting through scattered docs. This tool provides fast, searchable access to all 449 Claude Code documentation paths - API references, guides, examples, and changelogs.

### Key Features

- 🔍 **Instant Full-Text Search** - Find information in < 100ms across all documentation
- 📚 **Comprehensive Coverage** - 449 paths across 7 categories (API, guides, prompts, resources)
- ✅ **Automated Validation** - Keeps docs fresh, detects broken links automatically
- 🎯 **Dual Mode** - Simple shell-only or Python-powered enhanced features
- 🧪 **Well-Tested** - 577 tests (99.3% pass rate), 72% coverage, reliable and stable
- 🔄 **Auto-Updates** - Syncs with latest Claude Code documentation every 3 hours

## Installation

**One command, 2 minutes:**

```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

**The installer automatically detects your system:**
- **Standard mode** - Always works, shell-only, 269 core files
- **Enhanced mode** - Enables automatically if Python 3.9+ is available (449 paths, full-text search)

Installation succeeds regardless of Python availability. Enhanced features activate automatically when supported.

**Requirements:**
- macOS 12+ or Linux (Ubuntu, Debian, Fedora, etc.)
- git, jq, curl (usually pre-installed)
- Python 3.9+ (optional, enables enhanced features)

See [enhancements/](enhancements/) for complete feature documentation and examples.

## The Problem This Solves

**Claude Code ships features rapidly.** New APIs, enhanced capabilities, updated workflows - documentation spreads across 449+ unique pages.

**Finding information mid-coding?** 5-10 minutes of context switching, hunting docs, getting distracted. Multiply by 10-20 times a day = hours lost weekly.

**This tool solves that:**
- Find information in seconds, not minutes
- Search across all content, not just file names
- Stay current with automated updates
- Validate docs are accurate and reachable
- Work offline when needed

## Use Cases

- 💻 **During coding sessions** - Quick lookup without leaving terminal
- 📝 **API exploration** - Search all endpoints and examples instantly
- 🔧 **Troubleshooting** - Find relevant guides fast
- 📚 **Learning** - Explore features systematically across categories
- 🤖 **CI/CD** - Offline docs in build environments
- 🎓 **Team onboarding** - Comprehensive local reference for new developers

## Platform Compatibility

- ✅ **macOS**: Fully supported (tested on macOS 12+)
- ✅ **Linux**: Fully supported (Ubuntu, Debian, Fedora, etc.)
- ⏳ **Windows**: Not yet supported - [contributions welcome](#contributing)!

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
3. Check if GitHub Actions are running: [View Actions](https://github.com/costiash/claude-code-docs/actions)
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

Enhanced mode requires Python 3.9+ and provides additional features like full-text search.

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

### Defense-in-Depth Approach

This project implements multiple security layers to protect against injection attacks and malicious inputs:

- **Input Sanitization**: All URL paths are sanitized using a whitelist approach (alphanumeric, hyphens, underscores, dots only)
- **Path Traversal Protection**: Prevents `../` attacks and directory escape attempts
- **Shell Injection Prevention**: Proper escaping in all GitHub Actions workflows using heredocs and environment variables
- **Comprehensive Testing**: 13 dedicated security test cases covering XSS, SQL injection, command injection, and Unicode attacks

### Operational Security

- The installer modifies `~/.claude/settings.json` to add an auto-update hook
- The hook only runs `git pull` when reading documentation files
- All operations are limited to the documentation directory
- No data is sent externally - everything is local
- **Repository Trust**: The installer clones from GitHub over HTTPS. For additional security, you can:
  - Fork the repository and install from your own fork
  - Clone manually and run the installer from the local directory
  - Review all code before installation

### Security Validation

All security enhancements are verified through automated testing with 99.3% test pass rate (573/577 tests) and 72% code coverage. See [CONTRIBUTING.md](CONTRIBUTING.md) for details on our security testing approach.

## Contributing

**Contributions are welcome!** This is a community project and we'd love your help:

### Contributing to This Fork (Enhanced Features)

- 🪟 **Windows Support**: Want to help add Windows compatibility? [Fork the repository](https://github.com/costiash/claude-code-docs/fork) and submit a PR!
- 🐛 **Bug Reports**: Found something not working? [Open an issue](https://github.com/costiash/claude-code-docs/issues)
- 💡 **Feature Requests**: Have an idea? [Start a discussion](https://github.com/costiash/claude-code-docs/issues)
- 📝 **Documentation**: Help improve docs or add examples

### Contributing to Upstream

If you want to contribute improvements that benefit the original project:

- 🔄 **Upstream Contributions**: Check out [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) for the original implementation
- 💝 **Core Features**: Contributions to core functionality should ideally go to upstream first
- 🤝 **Collaboration**: We aim to keep compatibility with upstream and contribute improvements back when possible

You can also use Claude Code itself to help build features - just fork the repo and let Claude assist you!

## Known Issues

Some edge cases to be aware of:
- Auto-updates may occasionally fail on certain network configurations
- Some documentation links might not resolve correctly

If you find any issues not listed here, please [report them](https://github.com/costiash/claude-code-docs/issues)!

## Acknowledgments

This enhanced edition is built upon the excellent work of:

- **[Eric Buess](https://github.com/ericbuess)** - Creator of [claude-code-docs](https://github.com/ericbuess/claude-code-docs), the original implementation that made local Claude Code documentation access possible
- **[Anthropic](https://www.anthropic.com/)** - For Claude Code and the comprehensive documentation

The original [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) provides a simpler, shell-only implementation that works great for basic documentation access. This fork extends that foundation with additional features for users who need advanced search and validation capabilities.

## License

Documentation content belongs to Anthropic.
This mirror tool is open source - contributions welcome!
