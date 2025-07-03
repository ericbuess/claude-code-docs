# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Local mirror of Claude Code documentation, updated every 3 hours.

## Installation

Clone anywhere you like:
```bash
git clone https://github.com/ericbuess/claude-code-docs.git
```

## Usage

Just tell Claude where to look:

```
You: read about hooks from ~/claude-code-docs
```

That's it. Claude reads from your local files instead of fetching from the web.

## Why This Exists

- Faster than web fetching
- Works offline
- Always up-to-date (auto-updates every 3 hours)

## Optional: Create a Slash Command

For frequent use, you can create a shortcut:

```bash
# Create the commands directory if it doesn't exist
mkdir -p ~/.claude/commands

# Create the command (replace PATH with where you cloned)
echo "Read Claude Code docs about \$ARGUMENTS from PATH/claude-code-docs/docs/" > ~/.claude/commands/docs.md
```

Example if you cloned to your home directory:
```bash
echo "Read Claude Code docs about \$ARGUMENTS from ~/claude-code-docs/docs/" > ~/.claude/commands/docs.md
```

Now you can use: `/user:docs hooks` instead of typing the full path each time.

## What's Included

All 27+ Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/

## Updating

```bash
cd claude-code-docs && git pull
```

## License

Documentation content belongs to Anthropic.