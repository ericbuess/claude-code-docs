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

**Optional: Auto-sync** - Automatically run `git pull` on a schedule with our [auto-sync scripts](auto-sync/):
```bash
./auto-sync/auto-sync.sh  # Manually pull latest changes (same as git pull but with safety checks)
# OR
crontab -e  # Set up automatic git pull every 6 hours (see auto-sync/README.md)
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

## 🤖 Using with Claude Code CLI

For best results, point Claude Code to the **repository root** (not just the docs folder):

### Option A: Local Repository
```bash
# Clone the repo
git clone https://github.com/ericbuess/claude-code-docs.git

# Tell Claude to use it
"Use the Claude Code docs at /path/to/claude-code-docs"
```

### Option B: Direct GitHub Reference
```bash
"Use the Claude Code docs at github.com/ericbuess/claude-code-docs"
```

**Why the repository root?** The `CLAUDE.md` file provides Claude with:
- Understanding of the repository structure
- How to search and navigate docs efficiently  
- Access to both documentation and manifest

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

### Check Freshness

The `docs_manifest.json` file contains metadata for all documents:
```bash
# View all available docs
cat docs/docs_manifest.json | jq '.files | keys'

# Check when a specific doc was last fetched
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