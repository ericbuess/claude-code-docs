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

## 📋 When User Says "install claude code docs" or Similar

When the user asks to install/setup Claude Code documentation (phrases like "install claude code docs", "set up claude documentation", "keep claude docs updated"), follow these steps:

### Option A: Full Automated Install (Recommended)

1. **Check if already installed:**
   ```bash
   [ -d "$HOME/.claude/claude-code-docs" ] && echo "ALREADY_INSTALLED" || echo "NOT_INSTALLED"
   ```

2. **If NOT_INSTALLED, show this message:**
   > **📚 Installing Claude Code Documentation**
   > 
   > I'll set up a local copy of Claude Code documentation that stays automatically updated.
   > 
   > **What I'll do:**
   > - ✓ Clone docs to ~/.claude/claude-code-docs/
   > - ✓ Configure automatic updates every 6 hours
   > - ✓ Add to your Claude memory for easy access
   > - ✓ Handle all setup complexity
   > 
   > This will take about 30 seconds. Proceed? (yes/no)

3. **If ALREADY_INSTALLED:**
   > ✅ Claude Code docs are already installed at ~/.claude/claude-code-docs/
   > 
   > To check for updates: `cd ~/.claude/claude-code-docs && git pull`

### Option B: Setup Existing Clone

If the user already cloned the repo and asks to "setup auto sync", follow these steps:

1. **Verify we're in the claude-code-docs repository:**
   ```bash
   pwd | grep -q "claude-code-docs" && [ -f "./install.sh" ] && echo "IN_REPO" || echo "NOT_IN_REPO"
   ```

2. **If IN_REPO, run the installer (see Auto-Setup Instructions below)**

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

### For Full Automated Install (Option A):

When the user agrees to install, execute these steps:

1. **Create ~/.claude directory if needed**:
   ```bash
   mkdir -p "$HOME/.claude"
   ```

2. **Clone the repository**:
   ```bash
   cd "$HOME/.claude" && git clone https://github.com/ericbuess/claude-code-docs.git
   ```

3. **Run the installer**:
   ```bash
   cd "$HOME/.claude/claude-code-docs" && CLAUDE_CODE_CLI=true ./install.sh
   ```

4. **Add to user's Claude memory** (if not already present):
   ```bash
   # Check if already imported
   if ! grep -q "@$HOME/.claude/claude-code-docs/CLAUDE.md" "$HOME/.claude/CLAUDE.md" 2>/dev/null; then
       echo -e "\n# Claude Code Documentation\n@$HOME/.claude/claude-code-docs/CLAUDE.md" >> "$HOME/.claude/CLAUDE.md"
   fi
   ```

5. **Handle installer responses**:
   - If `CLAUDE_SUCCESS: AUTO_SYNC_CONFIGURED` - installation complete!
   - If `CLAUDE_ERROR: MACOS_CRON_PERMISSION_REQUIRED` - guide user through macOS setup

6. **Confirm success**:
   > ✅ Claude Code documentation installed successfully!
   > 
   > The docs are now available at ~/.claude/claude-code-docs/ and will update automatically.
   > 
   > You can now ask me questions like:
   > - "How do I use MCP servers?"
   > - "Show me the troubleshooting guide"
   > - "Search claude docs for hooks"

### For Existing Clone Setup (Option B):

1. **Run the installer with Claude mode**:
   ```bash
   CLAUDE_CODE_CLI=true ./install.sh
   ```

2. **Verify setup**:
   ```bash
   crontab -l | grep claude-code-docs && echo "✓ Auto-sync is configured"
   ```