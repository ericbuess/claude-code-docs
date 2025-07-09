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

Now you can use the slash command:

### Basic usage (instant, no checks):
```
/user:docs hooks        # Read hooks documentation instantly
/user:docs mcp          # Read MCP documentation instantly  
/user:docs memory       # Read memory documentation instantly
```

### Check documentation freshness:
```
/user:docs -t           # Show when docs were last updated
/user:docs -t hooks     # Check freshness, then read hooks docs
```

### Creative examples:
```
/user:docs what environment variables exist and how do I use them?
/user:docs recommend some useful slash commands based on my usage so far
/user:docs -t please explain all recent changes to the docs
/user:docs how do I trigger custom commands on demand?
/user:docs search all docs and find unique ways to use Claude Code CLI
```

Claude reads from your local docs instantly and can search across all documentation to answer complex questions!

## How Updates Work

The docs automatically stay up-to-date:
- GitHub Actions updates the repository every 3 hours
- The installer sets up a smart hook that pulls updates at most once every 3 hours
- The hook tracks when it last pulled to avoid unnecessary git operations
- No manual updates needed!

**Performance**: By default, `/user:docs` reads instantly with no checks. Use `/user:docs -t` when you want to verify documentation freshness or trigger an update.

## License

Documentation content belongs to Anthropic.