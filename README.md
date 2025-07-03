# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Local mirror of Claude Code documentation, updated every 3 hours.

## Installation

Clone anywhere you like:
```bash
git clone https://github.com/ericbuess/claude-code-docs.git
```

## Usage

When you want Claude to read from local docs instead of fetching from the web:

```
You: what are hooks?
Claude: [tries to WebFetch]
You: look locally
Claude: [reads from local docs]
```

Or be explicit from the start:
```
You: read about hooks from the local claude-code-docs
```

## Why This Exists

- Faster than web fetching
- Works offline
- Always up-to-date (auto-updates every 3 hours)

## Optional: Environment Variable

If you want to set a default location:
```bash
export CLAUDE_DOCS_PATH="$HOME/claude-code-docs"
```

Then tell Claude: "check $CLAUDE_DOCS_PATH for docs"

## What's Included

All 27+ Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/

## Updating

```bash
cd claude-code-docs && git pull
```

## License

Documentation content belongs to Anthropic.