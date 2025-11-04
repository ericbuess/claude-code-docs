# Claude Code Documentation Mirror

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are periodically updated via GitHub Actions.

## For /docs Command

When responding to /docs commands:
1. Follow the instructions in `~/.claude/commands/docs.md`
2. Execute `~/.claude-code-docs/scripts/claude-docs-helper.sh` with user's arguments
3. The helper script handles both standard and enhanced modes automatically
4. Read documentation files from the docs/ directory
5. Use the manifest to know available topics

## Files to think about

@install.sh
@README.md
@uninstall.sh
@UNINSTALL.md
@CONTRIBUTING.md
@scripts/
@.github/workflows/
