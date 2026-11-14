# Claude Code Documentation Mirror

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are periodically updated via GitHub Actions.

## For /docs Command

When responding to /docs commands:
1. Follow the instructions in the docs.md command file
2. Read documentation files from the docs/ directory only
3. Use the manifest to know available topics

## For /query Command

When responding to /query commands:
1. Invoke the `query-orchestrator` skill via the Skill tool
2. Follow the skill's 7-step procedure (parse → task ID → folder → template → batch dispatch → assemble → summary)
3. Subagents read from docs/ folder via DOCS_MAP.md
4. Outputs accumulate in ~/.claude-code-docs/query/

## Files to ultrathink about

@install.sh
@README.md
@uninstall.sh
@UNINSTALL.md
@claude-docs-helper.md
@scripts/
@.github/workflows/
@docs/DOCS_MAP.md
@claude-files/
