# Claude Code Documentation

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

### Key Features
- **Fully Autonomous**: Uses sitemap.xml to automatically discover new pages
- **Handles Changes**: Automatically adapts to added, removed, or renamed pages
- **Resilient**: Falls back to essential pages if sitemap is unavailable
- **Partial Success**: Continues working even if some pages fail to download

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