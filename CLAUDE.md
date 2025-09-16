# Claude Code Documentation Mirror

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are periodically updated via GitHub Actions.

## For /docs Command

When responding to /docs commands:
1. Follow the instructions in the docs.md command file
2. Read documentation files from the docs/ directory only
3. Use the manifest to know available topics

## Project Structure

- **install.sh** - Installation script that sets up the tool
- **README.md** - Main documentation and user guide
- **uninstall.sh** - Smart uninstaller that finds all installations
- **UNINSTALL.md** - Uninstallation documentation
- **scripts/** - Core scripts including helper and fetcher
- **.github/workflows/** - GitHub Actions for auto-updates
- **docs/** - Mirrored documentation files from Anthropic
