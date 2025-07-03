# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Local mirror of Claude Code documentation, updated every 3 hours.

## Why This Exists

- **Faster than web fetching** - Read from local files instantly
- **Works offline** - No internet required after cloning
- **Always up-to-date** - Auto-updates every 3 hours via GitHub Actions

## Installation

### Step 1: Clone the repository

```bash
git clone https://github.com/ericbuess/claude-code-docs.git
```

### Step 2: Create the slash command

**⚠️ IMPORTANT: Replace `/path/to/claude-code-docs` with YOUR actual path where you cloned the repo!**

```bash
echo "Read Claude Code docs about \$ARGUMENTS from /path/to/claude-code-docs/docs/" > ~/.claude/commands/docs.md
```

**Example:** If you cloned to your home directory:
```bash
echo "Read Claude Code docs about \$ARGUMENTS from ~/claude-code-docs/docs/" > ~/.claude/commands/docs.md
```

**Example:** If you cloned to `~/Projects`:
```bash
echo "Read Claude Code docs about \$ARGUMENTS from ~/Projects/claude-code-docs/docs/" > ~/.claude/commands/docs.md
```

## Usage

Now you can use the slash command:

### Basic usage:
```
/user:docs hooks
/user:docs mcp
/user:docs memory
```

### Creative examples:
```
/user:docs what environment variables exist and how do I use them?
/user:docs recommend some useful slash commands based on my usage so far
/user:docs please explain all recent changes to the docs
/user:docs how do I trigger custom commands on demand
/user:docs search all docs and find unique ways to use Claude Code CLI
```

Claude reads from your local docs instantly and can search across all documentation to answer complex questions!

## What's Included

All Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/

## Updating

```bash
cd claude-code-docs && git pull
```

The docs auto-update every 3 hours, so you'll always have the latest.

## License

Documentation content belongs to Anthropic.