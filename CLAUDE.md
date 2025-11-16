# Claude Code Documentation Mirror - Enhanced Edition

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are periodically updated via GitHub Actions.

## Architecture: Single Installation with Optional Python Features

This repository uses a **graceful degradation** approach:

**Installation** (always the same):
- 268 documentation files (.md format)
- Python scripts for enhanced features
- 270 active documentation paths tracked in manifest
- Full test suite and GitHub workflows

**Runtime Features** (Python-dependent):
- **Without Python 3.9+**: Basic documentation reading via shell scripts
- **With Python 3.9+**: Full-text search, path validation, fuzzy matching, auto-regeneration

There is NO separate "standard mode installation" - the full repository is always installed. Python features simply activate when Python 3.9+ is available.

## For /docs Command - AI-Powered Semantic Search

**IMPORTANT**: The `/docs` command is **AI-powered** and leverages Claude's semantic understanding instead of primitive keyword matching.

When responding to /docs commands:

1. **Read AI Instructions**: `~/.claude/commands/docs.md` contains comprehensive AI instructions on how to:
   - Analyze user intent semantically
   - Route to appropriate helper functions
   - Present results naturally with context

2. **Semantic Analysis**: Use your language understanding to classify user intent:
   - **Direct lookup**: User names a specific topic (e.g., `/docs hooks`)
   - **Information search**: User asks questions (e.g., `/docs what are best practices for SDK in Python?`)
   - **Path discovery**: User wants to find available docs (e.g., `/docs show me all MCP documentation`)
   - **Freshness check**: User wants update status (e.g., `/docs -t`)
   - **What's new**: User wants recent changes (e.g., `/docs what's new`)

3. **Intelligent Routing**: Based on semantic understanding, route to appropriate functions:
   - `--search-content "<keywords>"` for semantic information searches (requires Python 3.9+)
   - `--search "<keywords>"` for path discovery (requires Python 3.9+)
   - `<topic>` for direct documentation lookups
   - `-t` for freshness checks
   - `"what's new"` for recent changes

4. **Graceful Degradation**: The helper script automatically detects Python availability:
   - **With Python 3.9+**: Full AI-powered search with content search, path search, validation
   - **Without Python**: Basic documentation reading, explain limitations gracefully

5. **Natural Presentation**: Don't dump raw tool output - present information naturally:
   - Summarize search results with context
   - Provide official documentation links
   - Combine multiple sources when helpful
   - Explain your routing decisions if uncertain

**Example AI-Powered Workflow**:
```
User: /docs what are the best practices and recommended workflows using Claude Agent SDK in Python?

Your Analysis:
- User wants information (not a specific doc name)
- Key concepts: best practices, workflows, Agent SDK, Python
- Route to content search

Your Actions:
1. Extract keywords: "best practices workflows Agent SDK Python"
2. Execute: ~/.claude-code-docs/claude-docs-helper.sh --search-content "best practices workflows Agent SDK Python"
3. Read matching documentation sections
4. Present naturally: "Based on the official documentation, here are the best practices..."
5. Include links to relevant docs

Result: User gets semantic answer with documentation context, not raw file paths
```

## Python-Enhanced Features

When Python 3.9+ is installed, these additional capabilities are available:

- **Full-text search**: `--search "keyword"` searches across all documentation content
- **Category filtering**: `--category api` lists paths in specific categories
- **Path validation**: `--validate` checks documentation integrity
- **Active documentation**: Access to 270 active paths across 7 categories:
  - Core Documentation (79 paths, 29.3%)
  - API Reference (78 paths, 28.9%)
  - Prompt Library (65 paths, 24.1%)
  - Claude Code (44 paths, 16.3%)
  - Release Notes (2 paths)
  - Resources (1 path)
  - Uncategorized (1 path)

See `enhancements/` directory for comprehensive feature documentation and examples.

## Repository Structure

```
/
├── docs/                   # 268 documentation files (.md format)
│   ├── docs_manifest.json  # File tracking manifest (268 files)
│   └── .search_index.json  # Full-text search index (Python-generated)
├── scripts/
│   ├── claude-docs-helper.sh       # Main helper (feature detection)
│   ├── fetch_claude_docs.py        # Documentation fetcher with auto-regeneration
│   ├── lookup_paths.py             # Search & validation (Python)
│   └── build_search_index.py       # Index builder (Python)
├── paths_manifest.json     # Active paths manifest (270 paths)
├── enhancements/          # Feature documentation
│   ├── README.md          # Overview
│   ├── FEATURES.md        # Technical specs
│   ├── CAPABILITIES.md    # Detailed capabilities
│   └── EXAMPLES.md        # Usage examples
├── tests/                 # Test suite (600 tests, 598 passing)
├── install.sh            # Installation script
└── CLAUDE.md             # This file (AI context)

```

## Files to Think About

When working on this repository:

### Core Files
@install.sh - Installation script
@README.md - User documentation
@CONTRIBUTING.md - Contribution guidelines
@scripts/claude-docs-helper.sh - Main entry point (feature detection)
@uninstall.sh - Clean removal

### Python Features
@scripts/fetch_claude_docs.py - Documentation fetcher with auto-regeneration
@scripts/lookup_paths.py - Search & validation
@scripts/build_search_index.py - Full-text search indexing
@paths_manifest.json - Active paths manifest (270 paths)
@tests/ - Test suite (600 tests)

### Automation
@.github/workflows/ - Auto-update workflows (runs every 3 hours)

## Working on This Repository

**Critical Rule**: Changes must maintain graceful degradation - work with AND without Python.

### Feature Detection
The helper script checks Python availability at runtime:
```bash
if command -v python3 &> /dev/null && [ -f "$SCRIPTS_DIR/lookup_paths.py" ]; then
    # Python features available - use enhanced search/validation
else
    # Python not available - use basic shell features only
fi
```

### Testing
```bash
# Test basic features (always works)
./scripts/claude-docs-helper.sh hooks

# Test Python features (requires Python 3.9+)
python3 scripts/lookup_paths.py --search "mcp"
pytest tests/ -v

# Run full test suite
pytest tests/ -q  # Should see: 598 passed, 2 skipped
```

## Upstream Compatibility

This enhanced edition maintains compatibility with upstream (ericbuess/claude-code-docs):
- Same installation location (~/.claude-code-docs)
- Same `/docs` command interface
- Python features are additive, not breaking
- Works without Python (graceful degradation)
