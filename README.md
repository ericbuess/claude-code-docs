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
git clone https://github.com/ericbuess/claude-code-docs.git && cd claude-code-docs && echo "Read Claude Code docs about \$ARGUMENTS from $(pwd)/" > ~/.claude/commands/docs.md && cd .. && echo "✅ Installation complete! Use /user:docs to access documentation."
```

That's it! The command will:
1. Clone the repository
2. Create the slash command with the correct path automatically
3. Return to your original directory

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
/user:docs how do I trigger custom commands on demand?
/user:docs search all docs and find unique ways to use Claude Code CLI
```

Claude reads from your local docs instantly and can search across all documentation to answer complex questions!

## Keeping Docs Updated

The GitHub repository automatically updates every 3 hours. To update your local copy manually:

```bash
cd /path/to/where/you/cloned/claude-code-docs && git pull
```

However, manual updates shouldn't be needed because Claude automatically runs `git pull` before reading the docs. This behavior is configured in [CLAUDE.md](./CLAUDE.md) which tells Claude to:

> 1. Always run: git pull --quiet (to get latest docs)
> 2. Then read from docs/ directory

## License

Documentation content belongs to Anthropic.