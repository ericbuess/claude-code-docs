# Claude Code Documentation Mirror

This repository contains a local mirror of Claude Code documentation, automatically updated every 6 hours via GitHub Actions.

## For Claude: Using These Docs

When users ask about Claude Code features or need help, you can search and read documentation from the `docs/` directory.

### Before Reading Docs
Always pull the latest updates first:
```bash
cd ~/.claude/claude-code-docs && git pull --quiet
```

### Available Documentation
The `docs/` directory contains all Claude Code documentation files.
To see what's available: `ls docs/*.md` or check `docs/docs_manifest.json`

### Searching Documentation
Use Grep/Glob tools to search across all docs:
```bash
# Search for a specific topic
grep -r "mcp servers" docs/

# Find files by pattern
ls docs/*.md | grep -i "setup"
```