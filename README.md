# Claude Code Documentation

[![Update Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml/badge.svg)](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

A community-maintained mirror of Claude Code documentation with automatic updates.

## 🚀 Quick Start for Users

### Option 1: Use Pre-Downloaded Docs (Recommended)
```bash
# Clone this repository
git clone https://github.com/ericbuess/claude-code-docs.git
cd claude-code-docs

# The docs/ directory contains all documentation files
ls docs/
```

**Note**: Git IS the autodownloader! Once cloned, just run `git pull` to get the latest docs. No special tools needed.

### Option 2: Fetch Latest from This Repo
```bash
# Clone and run the GitHub fetcher
git clone https://github.com/ericbuess/claude-code-docs.git
cd claude-code-docs
python3 fetch_from_github.py
```

### Option 3: Point Claude Code CLI to This Repo
You can reference these docs directly from GitHub using raw URLs:
```
https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md
```

For example:
- Overview: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/overview.md`
- Setup: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/setup.md`

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

This manifest can be used by Claude Code to:
1. Discover all available documentation files
2. Get direct URLs to any doc by combining the `base_url` with filenames
3. Check when docs were last updated

Example usage:
```python
# Fetch the manifest
manifest = fetch_json("https://raw.githubusercontent.com/.../docs_manifest.json")

# Get a specific doc
doc_url = manifest["base_url"] + "setup.md"
content = fetch(doc_url)
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

This repository automatically updates daily via GitHub Actions. The workflow:
- Runs every day at 2 AM UTC
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

## 📊 Track Changes

Stay informed about documentation updates:

- **[📅 View Update History](https://github.com/ericbuess/claude-code-docs/commits/main/docs)** - See all documentation changes with descriptive commit messages
- **[🔍 Latest Changes](https://github.com/ericbuess/claude-code-docs/commit/main)** - View the most recent documentation update
- **[📈 Compare Versions](https://github.com/ericbuess/claude-code-docs/compare/main@{7.days.ago}...main)** - See what changed in the last week
- **[⚙️ Workflow Runs](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)** - Check update status and history

### Understanding Commit Messages

Starting today, commit messages show exactly what changed:
- `Updated: setup.md, quickstart.md` - Files that were modified
- `Added: new-feature.md` - New documentation added
- `Removed: deprecated.md` - Documentation removed

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
├── fetch_claude_docs.py     # Script to dynamically fetch from Anthropic
├── fetch_from_github.py     # Script to fetch from this repo
├── requirements.txt         # Python dependencies
├── .github/
│   └── workflows/
│       └── update-docs.yml  # Automatic update workflow
└── README.md               # This file
```

## 🔗 Stable URLs

- **Main branch**: Always contains the latest stable documentation
- **Direct docs folder**: https://github.com/ericbuess/claude-code-docs/tree/main/docs
- **Raw file access**: `https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md`

## 📝 License

This is a community project. The documentation content belongs to Anthropic.