# Claude Code Documentation Fetcher

A Python script to download all Claude Code documentation pages as markdown files.

## Features

- Downloads all 27 Claude Code documentation pages
- Saves as markdown files in `docs/` directory
- Bypasses cache to get latest versions
- Includes retry logic and error handling
- Progress tracking with detailed logging
- Rate limiting to be respectful to servers

## Setup

Using uv (recommended):
```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Using pip:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python fetch_claude_docs.py
```

The script will:
1. Create a `docs/` directory if it doesn't exist
2. Download all Claude Code documentation pages
3. Save them as markdown files (e.g., `overview.md`, `setup.md`)
4. Show progress and any errors

## Files

- `fetch_claude_docs.py` - Main script
- `requirements.txt` - Python dependencies
- `docs/` - Output directory for markdown files

## Documentation Pages

The script downloads documentation for:
- Getting started guides
- Build with Claude resources
- Deployment options
- Administration tools
- Reference documentation
- Legal and compliance information