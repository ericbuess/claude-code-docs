# Claude Code Documentation Mirror - Project Context

This repository is an automatically-updated mirror of the official Claude Code documentation from Anthropic. It provides offline access and version tracking for Claude Code docs.

## Repository Purpose
- Mirrors official Claude Code documentation daily
- Provides stable URLs for documentation access
- Enables offline documentation viewing
- Tracks documentation changes over time

## Key Features
- **Automatic Updates**: GitHub Actions fetches latest docs daily at 2 AM UTC
- **Dynamic Discovery**: Uses sitemap.xml to find new documentation pages
- **Change Detection**: Only downloads modified files using SHA-256 hashing
- **Failure Notifications**: Creates GitHub issues if updates fail

## Working with This Repository

### For Documentation Tasks
When asked to search, read, or analyze Claude Code documentation:
1. The `docs/` directory contains all current documentation files
2. Use `docs_manifest.json` to see file metadata and last update times
3. Documentation files use consistent markdown formatting

### Common Patterns
- **Search across docs**: Use grep/glob patterns in the `docs/` directory
- **Find specific topics**: File names generally match their content (e.g., `setup.md` for setup instructions)
- **Check freshness**: Reference `docs_manifest.json` for last update timestamps

### Important Notes
- This is a read-only mirror - don't edit documentation files directly
- The official source is https://docs.anthropic.com/en/docs/claude-code/
- Manual additions to `docs/` are preserved (the updater only removes files it previously fetched)

## Maintenance Reminders
- The fetch_claude_docs.py script handles all updates
- GitHub Actions workflow runs automatically
- Check GitHub Issues for any update failures
- The manifest tracks all fetched files to enable safe cleanup

## Quick Reference
- **All docs**: `/docs/*.md`
- **Manifest**: `/docs/docs_manifest.json`
- **Fetcher**: `/fetch_claude_docs.py`
- **GitHub fetcher**: `/fetch_from_github.py`
- **Automation**: `/.github/workflows/update-docs.yml`