# ⛔ INTERNAL CLAUDE CODE CLI INSTRUCTIONS

> ### ⚠️ WARNING: This file is NOT user documentation!
> 
> This file contains behavioral instructions for Claude when working with this repository.
> 
> **🚨 Users should refer to [README.md](README.md) for all documentation.**

---

## Claude Code Documentation Mirror - Project Context

This repository is an automatically-updated mirror of the official Claude Code documentation from Anthropic. It provides offline access and version tracking for Claude Code docs.

## 🔄 Automatic Updates

This repository has two update mechanisms:
1. **GitHub Actions**: Updates the GitHub repository every 6 hours automatically
2. **Local Auto-Sync**: Optional cron job to pull updates to your local copy

## 📋 When User Says "setup auto sync" or Similar

When the user asks to setup automatic syncing (phrases like "setup auto sync", "enable auto updates", "configure automatic updates"), follow these steps:

1. **Check current status:**
   ```bash
   crontab -l 2>/dev/null | grep -q "claude-code-docs.*auto-sync" && echo "CONFIGURED" || echo "NOT_CONFIGURED"
   ```

2. **If NOT_CONFIGURED, show this message:**
   > **📚 Setting up Automatic Sync for Claude Code Docs**
   > 
   > This will keep your local copy automatically updated with the latest documentation.
   > 
   > **What this will do:**
   > - ✓ Add a cron job that runs `git pull` every 6 hours
   > - ✓ Only pull when updates are available
   > - ✓ Log all updates to `auto-sync/sync.log`
   > - ✓ Include safety checks to prevent conflicts
   > 
   > **Note for macOS users**: You'll need to grant cron Full Disk Access in System Settings → Privacy & Security → Full Disk Access → Add `/usr/sbin/cron`
   > 
   > **Shall I proceed with the setup?** (yes/no)

3. **If CONFIGURED, show:**
   > ✅ Auto-sync is already configured! Your docs will update automatically every 6 hours.
   > 
   > To check sync status: `tail auto-sync/sync.log`

4. **If user says yes to setup, follow the auto-setup instructions below.**

## 🚀 How to Use These Docs with Claude Code CLI

### Recommended: Point Claude to the Repository Root

```bash
# For local clone
"Use the Claude Code docs at /Users/myname/claude-code-docs"

# For GitHub reference  
"Use the docs at github.com/ericbuess/claude-code-docs"
```

This gives Claude access to:
- This CLAUDE.md file for context
- The docs/ directory with all documentation
- The manifest for efficient searching

### Example Commands After Setup:

```bash
# Search across all docs
"Search the Claude Code docs for information about MCP"

# Read specific documentation
"Show me the troubleshooting guide"

# List available docs
"What documentation is available?"
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

## 🤖 Auto-Setup Instructions for Claude

When the user agrees to set up automatic updates (or asks for it), follow these steps:

1. **Check their system**: Run `uname` to see if they're on macOS or Linux
2. **Test the sync script**: Run `./auto-sync/auto-sync.sh` to ensure it works
3. **Get the repository path**: Run `pwd` to get the full path
4. **Set up cron**: 
   - For macOS: First remind them about Full Disk Access for cron (System Settings → Privacy & Security → Full Disk Access → Add `/usr/sbin/cron`)
   - Run `crontab -e` and add: `30 */6 * * * cd [FULL_PATH] && ./auto-sync/auto-sync.sh --quiet`
5. **Verify**: Run `crontab -l` to confirm it was added

For detailed instructions, see `auto-sync/README.md`.