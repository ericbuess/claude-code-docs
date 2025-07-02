# Claude Code Documentation Mirror

[![Update Status](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml/badge.svg)](https://github.com/ericbuess/claude-code-docs/actions/workflows/update-docs.yml)
[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Keep Claude Code documentation on your local machine, always up-to-date. This mirror automatically syncs with Anthropic's official docs every 6 hours.

## 🚀 Quick Setup

```bash
# 1. Clone to Claude's directory
cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git

# 2. Add to ~/.claude/CLAUDE.md:
cat >> ~/.claude/CLAUDE.md << 'EOF'

# Claude Code Documentation  
Location: ~/.claude/claude-code-docs/
Docs: All Claude Code documentation files
Update: cd ~/.claude/claude-code-docs && git pull --quiet
EOF
```

That's it! Claude will now:
- Know where the docs are located
- Pull updates automatically when you ask about Claude Code
- Have instant access to all documentation

## 📚 What's Included

The `docs/` directory contains all Claude Code documentation:
- **Getting Started**: Overview, setup, quickstart, memory management, common workflows
- **Development**: IDE integrations, MCP, GitHub Actions, SDK, troubleshooting
- **Deployment**: Third-party integrations, Amazon Bedrock, Google Vertex AI, and more
- **Administration**: IAM, security, monitoring, usage tracking, costs
- **Reference**: CLI reference, interactive mode, slash commands, settings, hooks
- **Compliance**: Legal and data usage policies

## 🔄 How It Works

1. **GitHub Actions** updates this repository every 6 hours from Anthropic's official docs
2. **Claude** pulls updates via `git pull` when you ask questions
3. **You** get always-current documentation with zero maintenance

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
```
claude "use the claude code docs at github.com/ericbuess/claude-code-docs"
```

### Manual Installation
If you prefer a different location:
```bash
git clone https://github.com/ericbuess/claude-code-docs.git
# Then tell Claude where you put it
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