# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Give Claude instant access to its own documentation.

## Quick Setup

Run this command:
```bash
curl -sSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/setup.sh | bash
```

That's it! Now when you ask Claude about Claude Code features, it will:
- Check if docs exist locally
- Auto-install them if needed
- Read from local files (fast!)

## How It Works

The setup script adds instructions to your `~/.claude/CLAUDE.md` that tell Claude:
1. Where to find local docs (`~/.claude/claude-code-docs/docs/`)
2. How to install them if missing
3. How to update them

## What You Can Now Ask

- "How do I use MCP servers in Claude Code?"
- "What are Claude Code hooks?"
- "Show me Claude Code's memory management"
- "Explain Claude Code slash commands"

Claude will automatically install the docs on first use!

## Manual Setup

If you prefer to set up manually:

1. Add to `~/.claude/CLAUDE.md`:
```
# Claude Code Docs

Local mirror: ~/.claude/claude-code-docs/docs/
Update: cd ~/.claude/claude-code-docs && git pull --quiet

When asked about Claude Code features:
1. ALWAYS check if ~/.claude/claude-code-docs/docs/ exists first
2. If missing, install it: cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git
3. Then read from local files at ~/.claude/claude-code-docs/docs/
4. NEVER use WebFetch for docs.anthropic.com/en/docs/claude-code/ if local docs available
```

2. Start a new Claude session (`/exit` then `claude`)

## Verify It Works

```
claude 'what are claude code hooks?'
```

Claude will check for local docs, install if needed, then answer from local files.

## Uninstall

```
claude 'uninstall the claude code docs mirror'
```

## What This Does

- Gives Claude instructions to auto-install docs when needed
- Docs update automatically every 3 hours (via GitHub Actions)
- Everything runs locally after first install

## License

This is a community project. The documentation content belongs to Anthropic.