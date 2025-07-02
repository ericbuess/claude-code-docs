# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Give Claude instant access to its own documentation.

## Quick Setup

1. Configure Claude (one time):
```bash
curl -sSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/setup.sh | bash
```

2. In any project where you want docs:
```bash
git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
```

That's it! Now ask Claude about any Claude Code feature.

## How It Works

- The setup script tells Claude to look for `.claude-code-docs/` in your project
- Clone the docs to any project where you need them
- Claude reads from local files (fast, works offline)
- Docs auto-update every 3 hours via GitHub Actions

## What You Can Ask

- "How do I use MCP servers in Claude Code?"
- "What are Claude Code hooks?"
- "Show me Claude Code's memory management"
- "Explain Claude Code slash commands"

## Alternative: Global Install

If you have a directory that's always accessible (like `~/` or `~/Projects`), you can clone there once:

```bash
cd ~
git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
```

Then Claude can access the docs from any subdirectory.

## Manual Setup

Add to `~/.claude/CLAUDE.md`:
```
# Claude Code Docs

When asked about Claude Code features:
1. Check if .claude-code-docs/ exists in current directory or any parent
2. If not found, suggest: git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
3. Then read from .claude-code-docs/docs/
4. The docs auto-update every 3 hours via GitHub
```

## Why This Approach?

Claude Code has security restrictions - it can only access files within the current working directory tree. This approach works within those constraints by putting docs in your project directory.

## Updating

The docs auto-update via GitHub Actions. To get the latest:
```bash
cd .claude-code-docs && git pull
```

## Uninstall

Remove the docs:
```bash
rm -rf .claude-code-docs
```

Remove from `~/.claude/CLAUDE.md`: Delete the "Claude Code Docs" section.

## License

This is a community project. The documentation content belongs to Anthropic.