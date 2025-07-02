# Claude Code Documentation

[![Update Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml/badge.svg)](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

A community-maintained mirror of Claude Code documentation with automatic updates.

## 🚀 Quick Start for Users

### Option 1: Clone the Repository (Recommended)
```bash
# Clone this repository
git clone https://github.com/ericbuess/claude-code-docs.git
cd claude-code-docs

# The docs/ directory contains all documentation files
ls docs/

# To update to latest docs:
git pull
```

**NEW: Auto-sync available!** Set up automatic updates with our [auto-sync scripts](auto-sync/). Just run:
```bash
./auto-sync/auto-sync.sh  # One-time sync
# OR
crontab -e  # Set up automatic syncing (see auto-sync/README.md)
```

### Option 2: Direct URL Access (No Download Required)
Reference docs directly from GitHub using raw URLs:
```
https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md
```

For example:
- Overview: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/overview.md`
- Setup: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/setup.md`

### Option 3: Fork for Your Own Copy
Fork this repository to maintain your own synchronized copy that updates automatically via GitHub Actions.

## 🤖 Using with Claude Code

This repository includes a `CLAUDE.md` file that provides context to Claude Code about the documentation structure. To use it:

### If you've cloned/forked the repo:
Claude Code will automatically detect and use the CLAUDE.md file when you run it in the repository directory.

### If you're using Claude Code remotely:
You can reference the CLAUDE.md file directly:
```
https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/CLAUDE.md
```

### Using the Documentation Manifest (Advanced)

The repository includes a `docs_manifest.json` file that serves as a complete index of all documentation:

```
https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/docs_manifest.json
```

This manifest provides comprehensive metadata for each doc:
- **`base_url` + filename**: Get the mirrored doc from this repo
- **`original_url`**: View the doc on Anthropic's website
- **`original_md_url`**: Get the raw markdown from Anthropic
- **`hash`**: SHA-256 hash to verify content integrity
- **`last_updated`**: When this doc was last fetched

Example usage:
```python
# Fetch the manifest
manifest = fetch_json("https://raw.githubusercontent.com/.../docs_manifest.json")

# Get a specific doc from this mirror
doc_url = manifest["base_url"] + "setup.md"
content = fetch(doc_url)

# Compare with original source
original = fetch(manifest["files"]["setup.md"]["original_md_url"])
```

The CLAUDE.md file helps Claude Code understand:
- The purpose and structure of this documentation mirror
- How to search and navigate the documentation efficiently
- Important maintenance and update information

## 📚 Available Documentation

The `docs/` directory contains all 27 Claude Code documentation pages:
- Getting started guides (overview, setup, quickstart, memory, common-workflows)
- Build with Claude resources (ide-integrations, mcp, github-actions, sdk, troubleshooting)
- Deployment options (third-party-integrations, amazon-bedrock, google-vertex-ai, etc.)
- Administration tools (iam, security, monitoring-usage, costs)
- Reference documentation (cli-reference, interactive-mode, slash-commands, settings, hooks)
- Legal and compliance information

## 🔄 Automatic Updates

This repository automatically updates every 6 hours via GitHub Actions. The workflow:
- Runs 4 times daily (00:00, 06:00, 12:00, 18:00 UTC)
- **Dynamically discovers all Claude Code pages from the sitemap**
- Fetches the latest documentation from Anthropic
- Commits any changes automatically
- Removes obsolete documentation files
- Can also be triggered manually from the Actions tab
- **Creates GitHub issues on failures** for notification

### Key Features (v3.0)
- **Fully Autonomous**: Uses sitemap.xml to automatically discover new pages
- **Smart File Naming**: Preserves directory structure to prevent collisions
- **Change Detection**: Only downloads files that have changed (SHA-256 hash comparison)
- **Safe Cleanup**: Only removes files it previously tracked (preserves manual additions)
- **Flexible URL Matching**: Handles URL structure changes gracefully
- **Better Error Handling**: Continues working even if some pages fail
- **Failure Notifications**: Creates GitHub issues when updates fail
- **Manifest Tracking**: Maintains a manifest of all fetched files with metadata

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

### Check Freshness

The `docs_manifest.json` file contains exact timestamps for each document:
```bash
# Check when each doc was last fetched
cat docs/docs_manifest.json | jq '.files["setup.md"].last_updated'
```

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
├── auto-sync/              # Optional automatic sync scripts
│   ├── auto-sync.sh        # Main sync script
│   ├── check-updates.sh    # Check for updates
│   └── README.md           # Setup instructions
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