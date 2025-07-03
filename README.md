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

For frequent use, create `~/.claude/commands/docs.md`:
```markdown
Read Claude Code docs about $ARGUMENTS from ~/claude-code-docs/docs/
```

Then use: `/user:docs hooks`

## What's Included

All 27+ Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/

## Updating

```bash
cd claude-code-docs && git pull
```

## License

Documentation content belongs to Anthropic.