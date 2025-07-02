# Claude Code Documentation

[![Update Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml/badge.svg)](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

A community-maintained mirror of Claude Code documentation with automatic updates.

> **✨ Quick Setup:** Clone → Open in Claude Code → Say "setup auto sync" → Done!

## 📋 Prerequisites

- **Git**: Must be installed and configured
- **Claude Code CLI** (optional): For automatic sync setup
- **Python 3.8+** (optional): Only needed if you want to manually update docs

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)
```bash
# Clone and setup in one command
git clone https://github.com/ericbuess/claude-code-docs.git && cd claude-code-docs && ./install.sh
```

That's it! The installer will:
- ✓ Check prerequisites 
- ✓ Test git connectivity
- ✓ Handle macOS permissions
- ✓ Configure automatic updates

### Option 2: Setup with Claude Code
```bash
# Clone this repository
git clone https://github.com/ericbuess/claude-code-docs.git
cd claude-code-docs

# Open in Claude Code
claude

# Tell Claude to set it up
"setup auto sync"
```

### Option 3: Manual Setup
```bash
# Clone and pull updates manually when needed
git clone https://github.com/ericbuess/claude-code-docs.git
cd claude-code-docs
git pull  # Run this whenever you want updates
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

### After Setup
Once you've cloned the repo and optionally set up auto-sync, you can:

```bash
# Ask Claude about any Claude Code feature
"How do I use MCP servers?"
"Show me the troubleshooting guide"
"What are hooks?"

# Search across all docs
"Search for information about GitHub Actions"

# Get specific docs
"Show me the settings documentation"
```

### Pointing Claude to the Docs
If you want Claude to reference these docs in another project:
```bash
# Local reference
"Use the Claude Code docs at /path/to/claude-code-docs"

# GitHub reference
"Use the docs at github.com/ericbuess/claude-code-docs"
```

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

2. **Your Local Copy** (requires manual or automated pull):
   - Run `git pull` to get the latest updates
   - OR use auto-sync to automate this (see Option 1 above)
   - Updates come from GitHub, not directly from Anthropic

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
./diagnose.sh
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
├── docs/                    # All documentation markdown files
│   └── docs_manifest.json   # Index of all docs with metadata
├── auto-sync/              # Optional scripts to automate git pull
│   ├── auto-sync.sh        # Automated git pull with safety checks
│   ├── check-updates.sh    # Check if updates are available
│   └── README.md           # Setup instructions for cron
├── fetch_claude_docs.py     # Script to dynamically fetch from Anthropic
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── update-docs.yml  # Automatic update workflow
├── CLAUDE.md               # Context file for Claude Code CLI
└── README.md               # This file
```

## 🔗 Stable URLs

- **Main branch**: Always contains the latest stable documentation
- **Direct docs folder**: https://github.com/ericbuess/claude-code-docs/tree/main/docs
- **Raw file access**: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md`

## 📝 License

This is a community project. The documentation content belongs to Anthropic.