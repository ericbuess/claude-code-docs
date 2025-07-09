# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Local mirror of Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/, updated every 3 hours.

## Why This Exists

- **Faster than web fetching** - Read from local files instantly
- **Works offline** - No internet required after cloning
- **Always up-to-date** - Auto-updates every 3 hours via GitHub Actions

## Installation

Run this single command from wherever you want to store the docs:

```bash
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash
```

This will:
1. Clone the repository
2. Create the `/user:docs` slash command
3. Set up automatic git pull when reading docs

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
- The installer sets up a smart hook that pulls updates at most once every 3 hours
- The hook tracks when it last pulled to avoid unnecessary git operations
- No manual updates needed!

**Performance**: By default, `/user:docs` reads instantly with no checks. Use `/user:docs -t` when you want to verify documentation freshness or trigger an update.

## License

Documentation content belongs to Anthropic.