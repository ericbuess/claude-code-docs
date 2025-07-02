# Claude Code Documentation Mirror - Project Context

This repository is an automatically-updated mirror of the official Claude Code documentation from Anthropic. It provides offline access and version tracking for Claude Code docs.

## 🚀 How to Use These Docs with Claude Code CLI

### Direct Commands You Can Give Claude:

```bash
# Ask about a specific topic
"Read the setup guide from https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/setup.md"

# Reference the entire documentation set
"Use the docs at github.com/ericbuess/claude-code-docs to help me understand MCP"

# Check available documentation
"What Claude Code docs are available at https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/docs_manifest.json?"

# If you've cloned the repo locally
"Look at the troubleshooting guide in ./claude-code-docs/docs/troubleshooting.md"
```

## 📋 Documentation Manifest

The repository includes a `docs_manifest.json` file that provides a complete index:
- **Manifest URL**: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/docs_manifest.json`
- **Contents**: All documentation filenames, their source URLs, and last update times
- **Usage**: The manifest keys are the actual filenames. Combine the `base_url` field with any filename to get the direct URL.

Example programmatic usage:
```python
# Claude can use the manifest to find specific docs
manifest = fetch_json("https://raw.githubusercontent.com/.../docs_manifest.json")
doc_url = manifest["base_url"] + "settings.md"
content = fetch(doc_url)
```

## Repository Purpose
- Mirrors official Claude Code documentation every 6 hours
- Provides stable URLs for documentation access
- Enables offline documentation viewing
- Tracks documentation changes over time

## Key Features
- **Automatic Updates**: GitHub Actions fetches latest docs every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- **Dynamic Discovery**: Uses sitemap.xml to find new documentation pages
- **URL Pattern Robustness**: Automatically handles multiple URL patterns for Claude Code docs
- **Change Detection**: Only downloads modified files using SHA-256 hashing
- **Failure Notifications**: Creates GitHub issues if updates fail
- **Graceful Degradation**: If Anthropic changes URLs, existing docs remain available while an issue is created

## Working with This Repository

### For Documentation Tasks
When asked to search, read, or analyze Claude Code documentation:
1. The `docs/` directory contains all current documentation files
2. Use `docs_manifest.json` to see file metadata and last update times
3. Documentation files use consistent markdown formatting

### Quick Tips for Claude Code Users
- **No setup required**: Just reference the GitHub URLs directly
- **Always fresh**: Documentation updates every 6 hours
- **Offline access**: Clone the repo for local use without internet
- **Version history**: Use git history to see how docs changed over time

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
- **Automation**: `/.github/workflows/update-docs.yml`