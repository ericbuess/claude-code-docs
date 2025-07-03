# Contributing to Claude Code Documentation Mirror

## How It Works

This repository automatically mirrors Claude Code documentation from Anthropic's official docs every 3 hours using GitHub Actions.

## Repository Structure

```
claude-code-docs/
├── docs/                          # Mirrored documentation files
├── scripts/
│   ├── fetch_claude_docs.py      # Documentation fetcher
│   └── requirements.txt          # Python dependencies
├── .github/
│   └── workflows/
│       └── update-docs.yml       # GitHub Actions workflow
├── README.md                     # User-facing documentation
├── CLAUDE.md                     # Instructions for Claude
├── INSTALL.md                    # Installation steps for Claude
├── UNINSTALL.md                  # Uninstallation steps for Claude
└── CONTRIBUTING.md               # This file
```

## Manual Documentation Fetching

If you want to test the fetching process locally:

```bash
cd scripts
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python fetch_claude_docs.py
```

## How the Fetcher Works

1. Discovers Claude Code pages from Anthropic's sitemap
2. Downloads markdown versions of each documentation page
3. Validates content to ensure it's proper markdown
4. Only updates files that have changed (using SHA-256 hashing)
5. Creates a manifest file with metadata

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Important Notes

- Don't modify files in the `docs/` directory directly - they're auto-generated
- The fetch script is in `scripts/` 
- Keep it simple - users just clone and tell Claude to "look locally"