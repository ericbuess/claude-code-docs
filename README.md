# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Give Claude instant access to its own documentation.

## Quick Setup (2 steps)

1. **Configure Claude** (one time):
```bash
curl -sSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/setup.sh | bash
```

2. **Install docs** to your home directory:
```bash
cd ~ && git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
```

Done! Now Claude can access the docs from anywhere in your home directory.

## Test It

```bash
cd ~/any/project
claude 'what are claude code hooks?'
```

Claude will read from the local docs instantly.

## How It Works

- Docs live at `~/.claude-code-docs/`
- Claude can access them from any subdirectory of `~`
- No web fetching - reads directly from disk
- Auto-updates every 3 hours via GitHub Actions

## Manual Setup

If you prefer to configure manually, add to `~/.claude/CLAUDE.md`:
```
# Claude Code Docs

Local docs: ~/.claude-code-docs/docs/
When asked about Claude Code features, read from there.
If missing, tell user: cd ~ && git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
```

## Updating

The GitHub repo updates automatically. To pull latest changes:
```bash
cd ~/.claude-code-docs && git pull
```

## Uninstall

```bash
rm -rf ~/.claude-code-docs
```

Then remove the "Claude Code Docs" section from `~/.claude/CLAUDE.md`.

## Why Home Directory?

Claude Code can only access files within the current working directory tree. By installing in your home directory, the docs are accessible from any project under `~/`.

## License

This is a community project. The documentation content belongs to Anthropic.