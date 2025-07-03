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

**Example:** If you cloned to `~/Documents`:
```bash
echo "Read Claude Code docs about \$ARGUMENTS from ~/Documents/claude-code-docs/docs/" > ~/.claude/commands/docs.md
```

## Usage

Now you can use the slash command:

```
/user:docs hooks
/user:docs mcp
/user:docs memory
```

That's it! Claude reads from your local docs instantly.

## What's Included

All Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/

## Updating

```bash
cd claude-code-docs && git pull
```

The docs auto-update every 3 hours, so you'll always have the latest.

## License

Documentation content belongs to Anthropic.