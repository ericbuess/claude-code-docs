# Claude Code Documentation Mirror - Enhanced Edition

This repository contains local copies of Claude Code documentation from https://docs.anthropic.com/en/docs/claude-code/

The docs are periodically updated via GitHub Actions.

## Dual-Mode Architecture

This repository supports TWO modes:

1. **Standard Mode** (upstream-compatible)
   - Shell scripts only
   - 270 documentation files
   - Works exactly like upstream

2. **Enhanced Mode** (Python-powered, optional)
   - 449 documentation paths
   - Full-text search capabilities
   - Validation tools
   - Extended API reference and prompt library
   - Requires Python 3.12+

The installer prompts users to choose their mode during installation.

## For /docs Command

When responding to /docs commands:

1. Read `~/.claude/commands/docs.md` for complete instructions
2. Execute `~/.claude-code-docs/scripts/claude-docs-helper.sh` with user's arguments
3. The helper script automatically detects available features:
   - Checks for Python availability
   - Routes to enhanced scripts if available
   - Falls back to standard implementation otherwise
4. Read documentation files from `docs/` directory
5. Support both explicit flags (`--search`) and natural language ("search for mcp")

## Enhanced Features (if Python available)

When Python 3.12+ is installed, these additional capabilities are available:

- **Full-text search**: `--search "keyword"` searches across all documentation content
- **Category filtering**: `--category api` lists paths in specific categories
- **Path validation**: `--validate` checks documentation integrity
- **Extended coverage**: Access to 449 paths across 7 categories:
  - Core Documentation (151 paths)
  - API Reference (91 paths)
  - Claude Code (68 paths)
  - Resources (68 paths)
  - Prompt Library (64 paths)
  - Release Notes (4 paths)
  - Uncategorized (3 paths)

See `enhancements/` directory for comprehensive feature documentation and examples.

## Repository Structure

```
/
├── docs/                   # 270 documentation files (standard edition)
│   ├── docs_manifest.json  # Standard manifest
│   └── .search_index.json  # Full-text search index (enhanced mode)
├── scripts/
│   ├── claude-docs-helper.sh       # Main helper (mode detection)
│   ├── main.py                     # Enhanced fetcher (Python)
│   ├── lookup_paths.py             # Search & validation (Python)
│   └── build_search_index.py       # Index builder (Python)
├── paths_manifest.json     # Enhanced manifest (449 paths)
├── enhancements/          # Feature documentation
│   ├── README.md          # Overview
│   ├── FEATURES.md        # Technical specs
│   ├── CAPABILITIES.md    # Detailed capabilities
│   └── EXAMPLES.md        # Usage examples
├── tests/                 # Test suite (174 tests)
├── install.sh            # Dual-mode installer
└── CLAUDE.md             # This file

```

## Files to Think About

When working on this repository:

### Always Review
@install.sh - Handles both mode installations
@README.md - User documentation
@CONTRIBUTING.md - Contribution guidelines
@enhancements/ - Feature documentation

### For Standard Mode
@scripts/claude-docs-helper.sh - Routes between modes
@uninstall.sh - Clean removal
@.github/workflows/ - Auto-update workflows

### For Enhanced Mode
@scripts/*.py - Python scripts
@paths_manifest.json - Enhanced manifest
@tests/ - Test suite
@enhancements/ - Documentation

## Working on This Repository

**Critical Rule**: Changes must work in BOTH modes (standard and enhanced).

### Mode Detection
The helper script checks at runtime:
```bash
if command -v python3 &> /dev/null && [ -f "$SCRIPTS_DIR/lookup_paths.py" ]; then
    # Use enhanced Python features
else
    # Use standard shell implementation
fi
```

### Testing Both Modes
```bash
# Test standard mode
./scripts/claude-docs-helper.sh hooks

# Test enhanced mode (if Python available)
python3 scripts/lookup_paths.py --search "mcp"
pytest tests/ -v
```

## Upstream Compatibility

This enhanced edition maintains compatibility with upstream (ericbuess/claude-code-docs):
- Standard mode is functionally equivalent to upstream
- Enhanced features are opt-in during installation
- Both modes use the same `/docs` command interface
- Changes don't break upstream workflows
