# Claude Code Documentation Mirror

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are automatically updated every 3 hours via GitHub Actions.

## Automatic Updates

If the user has configured the PreToolUse hook as described in README.md, git pull will run automatically before reading docs. Otherwise, manually run git pull first.

## Important Instructions

When working with this repo:
1. ALWAYS read from the docs/ subdirectory, never from the root directory
2. The documentation files are in docs/*.md (e.g., docs/hooks.md, docs/settings.md)
3. IMPORTANT: Only read files from the docs/ directory to answer questions about Claude Code
4. Do NOT read CLAUDE.md, README.md, or install.sh when answering user questions