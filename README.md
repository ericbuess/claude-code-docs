# Claude Code Documentation Mirror

[![Update Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml/badge.svg)](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Keep Claude Code documentation on your local machine, always up-to-date. This mirror automatically syncs with Anthropic's official docs every 6 hours.

> **✨ Quick Setup:** Just tell Claude: `"install claude code docs"`

## Why Use This?

- 📚 **Offline Access**: Read Claude Code docs without internet
- 🔄 **Always Current**: Automatically pulls latest updates  
- 📝 **Version History**: See how docs changed over time with git
- 🚀 **Zero Configuration**: Claude handles everything for you

## 📋 Prerequisites

- **Git**: Must be installed and configured
- **Python 3.8+** (optional): Only needed if you want to manually fetch docs from Anthropic's servers

## 🚀 Quick Start

### Option 1: Let Claude Do Everything (Recommended)
```bash
# Just tell Claude to install the docs
claude "install claude code docs"
```

Claude will:
- ✓ Clone to ~/.claude/claude-code-docs/
- ✓ Set up automatic updates
- ✓ Handle all permissions
- ✓ Add to Claude's memory for instant access

### Option 2: Manual Installation
```bash
# If you prefer to do it yourself
git clone https://github.com/ericbuess/claude-code-docs.git && cd claude-code-docs && ./install.sh
```

### Option 3: No Installation Needed
```bash
# Just ask Claude to use the GitHub version
claude "use the claude code docs at github.com/ericbuess/claude-code-docs"
```

## 📖 Alternative Access Methods

### Direct URL Access (No Clone Required)
Reference docs directly from GitHub using raw URLs:
```
https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md
```

For example:
- Overview: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/overview.md`
- Setup: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/setup.md`

### Fork for Your Own Copy
Fork this repository to maintain your own synchronized copy that updates automatically via GitHub Actions.

## 🤖 Using with Claude Code

### After Installation
Once Claude installs the docs (or you do it manually), just ask questions naturally:

```bash
# Ask about any Claude Code feature
"How do I use MCP servers?"
"Show me the troubleshooting guide"  
"What are hooks?"

# Search across all docs
"Search claude docs for GitHub Actions"

# Get specific docs
"Show me the settings documentation from claude docs"
```

### If You Haven't Installed Yet
You can still use the docs directly from GitHub:
```bash
# Tell Claude to use the online version
"Use the claude code docs at github.com/ericbuess/claude-code-docs"

# Or just install them for offline access
"Install claude code docs"
```

### How Claude Knows About The Docs

After installation, Claude automatically imports the documentation into its memory using the CLAUDE.md import feature. This means:
- Claude always knows where your docs are located
- You don't need to specify paths when asking questions
- The docs are part of Claude's context in every conversation

### Documentation Index

The repository includes a `docs_manifest.json` file that lists all available documentation with metadata. This is primarily used by Claude Code for efficient searching and by the update scripts.

## 📚 Available Documentation

The `docs/` directory contains all Claude Code documentation organized by category:
- **Getting Started**: Overview, setup, quickstart, memory management, common workflows
- **Development**: IDE integrations, MCP, GitHub Actions, SDK, troubleshooting
- **Deployment**: Third-party integrations, Amazon Bedrock, Google Vertex AI, and more
- **Administration**: IAM, security, monitoring, usage tracking, costs
- **Reference**: CLI reference, interactive mode, slash commands, settings, hooks
- **Compliance**: Legal and data usage policies

Check `docs/` for the complete list of available documentation.

## 🔄 How Updates Work

The documentation is automatically updated on GitHub every 6 hours:

1. **GitHub Actions** (runs on GitHub's servers):
   - Runs 4 times daily (00:00, 06:00, 12:00, 18:00 UTC)
   - Fetches latest docs from Anthropic's website
   - Commits changes to this GitHub repository
   - Creates issues if updates fail

2. **Your Local Copy** (requires setup):
   - **With auto-sync**: Updates automatically 30 minutes after each GitHub update
   - **Without auto-sync**: Run `git pull` manually whenever you want updates
   - Updates flow: Anthropic → GitHub → Your machine

**Key Features:**
- **Fully Autonomous**: Uses sitemap.xml to automatically discover new pages
- **Smart Updates**: Only downloads files that have changed (SHA-256 hash comparison)
- **Safe Cleanup**: Only removes files it previously tracked (preserves manual additions)
- **Flexible URL Matching**: Handles URL structure changes gracefully
- **Error Resilient**: Continues working even if some pages fail
- **Failure Notifications**: Creates GitHub issues when updates fail
- **Manual Trigger**: Can be triggered manually from the Actions tab


## 📊 Status & Change Tracking

### Current Status
- **Last Check**: View the timestamp on the [latest workflow run](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
- **Last Update**: See the [most recent documentation changes](https://github.com/ericbuess/claude-code-docs/commits/main/docs)
- **Update Frequency**: Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)

### Track Documentation Changes

- **[📅 Full History](https://github.com/ericbuess/claude-code-docs/commits/main/docs)** - Browse all documentation updates with descriptive commit messages
- **[🔍 Latest Changes](https://github.com/ericbuess/claude-code-docs/commit/main)** - View the most recent changes in detail
- **[📈 Compare Versions](https://github.com/ericbuess/claude-code-docs/compare/main@{1.day.ago}...main)** - See what changed in the last 24 hours
- **[⚙️ Workflow Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)** - Check if updates are running successfully

### View Specific Changes

To see what changed in a specific file:
```bash
# View history of a specific doc
git log -p docs/setup.md

# Compare current version with previous
git diff HEAD~1 docs/setup.md

# See when a doc was last modified
git log -1 --format="%ai" -- docs/setup.md
```

### Understanding Commit Messages

Commit messages clearly indicate what changed:
- `Updated: setup.md, quickstart.md` - Files that were modified
- `Added: new-feature.md` - New documentation added
- `Removed: deprecated.md` - Documentation removed

### Check Update History

View the commit history to see when docs were last updated:
```bash
# See recent updates
git log --oneline -10 docs/

# Check when a specific doc was last modified
git log -1 --format="%ai" -- docs/setup.md
```

## 🔍 Troubleshooting

### Quick Diagnosis

Run the diagnostic script to check your setup:
```bash
# If Claude installed it
~/.claude/claude-code-docs/diagnose.sh

# If you installed it elsewhere
cd /path/to/claude-code-docs && ./diagnose.sh
```

This will check all prerequisites and common issues automatically.

### Auto-sync not working?

1. **Run the installer to fix most issues:**
   ```bash
   ./install.sh
   ```

2. **Check if auto-sync is set up:**
   ```bash
   crontab -l | grep claude-code-docs
   ```

3. **View sync logs:**
   ```bash
   tail -20 auto-sync/sync.log
   ```

4. **Common issues:**
   - **macOS**: Ensure cron has Full Disk Access (System Settings → Privacy & Security)
   - **Git authentication**: Run `git pull` manually to check credentials
   - **Wrong path**: Verify the path in your crontab is correct

### Updates not appearing?

- Check GitHub Actions status: https://github.com/ericbuess/claude-code-docs/actions
- Manual update: `git pull`
- The GitHub repo updates every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)

## 📖 For Contributors

### Fetching Documentation from Source
If you want to update the docs manually:

```bash
# Setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Fetch latest docs from Anthropic
python fetch_claude_docs.py
```

### Repository Structure
```
claude-code-docs/
├── docs/                    # All Claude Code documentation files
│   └── docs_manifest.json   # Index with metadata for all docs
├── install.sh              # One-command setup script
├── diagnose.sh             # Troubleshooting helper
├── auto-sync/              # Auto-update scripts
│   ├── auto-sync.sh        # Main sync script (runs via cron)
│   ├── check-updates.sh    # Check for available updates
│   └── README.md           # Detailed sync documentation
├── fetch_claude_docs.py     # Fetches docs from Anthropic (used by GitHub Actions)
├── requirements.txt         # Python dependencies (for manual fetching only)
├── .github/
│   └── workflows/
│       └── update-docs.yml  # GitHub Actions automation
├── CLAUDE.md               # Instructions for Claude Code CLI (not user docs)
└── README.md               # You are here
```

## 🔗 Stable URLs

- **Main branch**: Always contains the latest stable documentation
- **Direct docs folder**: https://github.com/ericbuess/claude-code-docs/tree/main/docs
- **Raw file access**: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md`

## 📍 Default Installation Location

When Claude installs the docs, they go to:
```
~/.claude/claude-code-docs/
```

This follows Claude Code's convention of storing user-level resources in `~/.claude/`.

## 📝 License

This is a community project. The documentation content belongs to Anthropic.