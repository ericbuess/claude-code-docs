# Claude Code Documentation Mirror

[![Update Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml/badge.svg)](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Keep Claude Code documentation on your local machine, always up-to-date. This mirror automatically syncs with Anthropic's official docs every 6 hours, and Claude pulls fresh updates from this mirror whenever you ask about Claude Code features.

## 🚀 Quick Setup

### Let Claude Install It (Easiest!)
```
claude "install the claude code docs from github.com/ericbuess/claude-code-docs"
```

### Or Install Manually
Copy and run this entire block:
```bash
cd ~/.claude && \
git clone https://github.com/ericbuess/claude-code-docs.git && \
echo "" >> ~/.claude/CLAUDE.md && \
echo "# Claude Code Documentation" >> ~/.claude/CLAUDE.md && \
echo "Location: ~/.claude/claude-code-docs/" >> ~/.claude/CLAUDE.md && \
echo "Docs: All Claude Code documentation files" >> ~/.claude/CLAUDE.md && \
echo "Update: cd ~/.claude/claude-code-docs && git pull --quiet" >> ~/.claude/CLAUDE.md && \
echo "✅ Installation complete!"
```

That's it! Claude will now:
- Know where the docs are located  
- Pull fresh updates from this mirror before answering Claude Code questions
- Always have access to documentation that's at most 6 hours old

## 📚 What's Included

The `docs/` directory contains all Claude Code documentation:
- **Getting Started**: Overview, setup, quickstart, memory management, common workflows
- **Development**: IDE integrations, MCP, GitHub Actions, SDK, troubleshooting
- **Deployment**: Third-party integrations, Amazon Bedrock, Google Vertex AI, and more
- **Administration**: IAM, security, monitoring, usage tracking, costs
- **Reference**: CLI reference, interactive mode, slash commands, settings, hooks
- **Compliance**: Legal and data usage policies

## 🔄 How It Works

1. **This GitHub repository** fetches the latest docs from Anthropic every 6 hours (see the status badges above)
2. **Your local copy** gets updated when Claude runs `git pull` before reading docs
3. **You** get documentation that's always current - Claude pulls fresh updates from this mirror automatically

## 💡 Usage Examples

Once installed, just ask Claude naturally:
```
"How do I use MCP servers?"
"Show me the troubleshooting guide"
"Search claude docs for hooks"
```

Claude will automatically pull the latest docs and answer your questions.

## 📖 Alternative Access Methods

### Online Access (No Installation)
Claude can read directly from GitHub:
```
claude "check the claude code docs at github.com/ericbuess/claude-code-docs for MCP server setup"
```

### Custom Installation Location
If you prefer a different directory:
```bash
git clone https://github.com/ericbuess/claude-code-docs.git ~/my-docs-location
# Then update your CLAUDE.md with the new path
```

### Direct URLs
Access specific docs without cloning:
```
https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/[filename].md
```

## 🛠️ For Contributors

### Repository Structure
```
claude-code-docs/
├── docs/                    # All Claude Code documentation files
│   └── docs_manifest.json   # Index with metadata for all docs
├── fetch_claude_docs.py     # Fetches docs from Anthropic (used by GitHub Actions)
├── requirements.txt         # Python dependencies (for manual fetching only)
├── .github/
│   └── workflows/
│       └── update-docs.yml  # GitHub Actions automation
├── CLAUDE.md               # Instructions for Claude (not user docs)
└── README.md               # You are here
```

### Manual Documentation Fetching
If you want to update docs from Anthropic yourself:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python fetch_claude_docs.py
```

## 📊 Status & Updates

- **Update Frequency**: Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- **Last Update**: See the [commit history](https://github.com/ericbuess/claude-code-docs/commits/main/docs)
- **Update Status**: Check the [GitHub Actions workflow](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)

## 🔍 Troubleshooting

### Docs not updating?
```bash
cd ~/.claude/claude-code-docs
git pull
```

### Want to see what changed?
```bash
cd ~/.claude/claude-code-docs
git log --oneline -10 docs/
```

### Need a fresh start?
```bash
rm -rf ~/.claude/claude-code-docs
# Then run the setup again
```

## 📝 License

This is a community project. The documentation content belongs to Anthropic.