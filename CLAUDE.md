# Claude Code Documentation Mirror

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are automatically updated every 3 hours via GitHub Actions.

## Development Workflow

**IMPORTANT**: All changes MUST be made on the `dev` branch first:
1. Create/switch to dev branch: `git checkout -b dev` or `git checkout dev`
2. Make and test all changes on dev branch
3. Only merge to main after user approval
4. The install.sh script is macOS-only (untested on other platforms)

## For /user:docs Command

When responding to /user:docs commands:
1. Follow the instructions in the docs.md command file
2. Report update times from docs_manifest.json and .last_pull
3. Read documentation files from the docs/ directory only