# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Give Claude instant access to its own documentation.

## Install in 5 Seconds

```
claude 'install claude docs: mkdir -p ~/.claude && cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git'
```

Then add to your `~/.claude/CLAUDE.md`:
```
# Claude Code Docs

Local mirror: ~/.claude/claude-code-docs/docs/
Update: cd ~/.claude/claude-code-docs && git pull --quiet
```

## Verify Installation

```
claude 'are my claude code docs installed?'
```

Claude will check if the local docs exist and confirm.

## What You Can Now Ask

- "How do I use MCP servers in Claude Code?"
- "What are Claude Code hooks and how do I set them up?"
- "How do I configure Claude Code with GitHub Actions?"
- "Explain Claude Code's memory management system"
- "Show me all Claude Code slash commands"

## Start New Session After Install

After installation, restart Claude to load the changes:
```
/exit              # Exit current session
claude             # Start fresh
claude -c          # Or continue your last session
```

## Uninstall

```
claude 'uninstall the claude code docs mirror'
```

## What This Does

- Gives Claude instant local access to all its documentation
- No more web fetching - reads directly from disk
- Updates automatically every 3 hours from Anthropic

## Details

- Installation steps: See [INSTALL.md](INSTALL.md)
- Uninstall steps: See [UNINSTALL.md](UNINSTALL.md)
- Contributing: See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

This is a community project. The documentation content belongs to Anthropic.