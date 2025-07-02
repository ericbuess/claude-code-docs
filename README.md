# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Give Claude instant access to its own documentation.

## Install in 5 Seconds

```
claude "install the claude code docs from github.com/ericbuess/claude-code-docs"
```

That's it! Claude now has access to all its documentation.

## Test It Works

```
claude "test claude code docs access"
```

## What You Can Now Ask

- "How do I use MCP servers in Claude Code?"
- "What are Claude Code hooks and how do I set them up?"
- "How do I configure Claude Code with GitHub Actions?"
- "Explain Claude Code's memory management system"
- "Show me all Claude Code slash commands"

## Alternative Installation

If you prefer to install manually:

```bash
# Clone and configure
cd ~/.claude && \
git clone https://github.com/ericbuess/claude-code-docs.git && \
echo "" >> ~/.claude/CLAUDE.md && \
echo "# Claude Code Docs" >> ~/.claude/CLAUDE.md && \
echo "" >> ~/.claude/CLAUDE.md && \
echo "Local mirror of Claude Code documentation." >> ~/.claude/CLAUDE.md && \
echo "" >> ~/.claude/CLAUDE.md && \
echo "Pull latest: cd ~/.claude/claude-code-docs && git pull --quiet" >> ~/.claude/CLAUDE.md && \
echo "Docs location: ~/.claude/claude-code-docs/docs/" >> ~/.claude/CLAUDE.md && \
echo "✅ Installation complete!"
```

**Note**: Start a new Claude session for changes to take effect:
- Exit: `/exit`  
- Start fresh: `claude`
- Continue last: `claude -c`
- Resume from list: `claude -r`

## Uninstall

```
claude "uninstall the claude code docs mirror"
```

## What This Does

- Gives Claude offline access to all its documentation (27+ markdown files)
- Updates automatically every 3 hours from Anthropic's official docs
- Works instantly - no web fetching needed when you ask questions

## License

This is a community project. The documentation content belongs to Anthropic.