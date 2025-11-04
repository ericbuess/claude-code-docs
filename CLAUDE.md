# Claude Code Documentation Mirror - Enhanced Edition

This repository extends [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) with optional Python-based enhancements while maintaining full backward compatibility with upstream.

**Key principle**: All changes must preserve both standard and enhanced modes.

## Project Architecture

### Dual-Mode System

This project supports TWO installation modes:

1. **Standard Mode** (upstream-compatible)
   - Shell scripts only (bash)
   - No Python dependencies
   - 47 core documentation files
   - Works exactly like upstream

2. **Enhanced Mode** (optional, opt-in)
   - Python 3.12+ with advanced features
   - 459 documentation paths (10x coverage)
   - Full-text search, validation, fuzzy matching
   - Graceful degradation to standard mode if Python unavailable

**The installer (`install.sh`) prompts users to choose their mode.**

## For /docs Command

When responding to /docs commands:

1. Read `~/.claude/commands/docs.md` for complete instructions
2. Execute `~/.claude-code-docs/scripts/claude-docs-helper.sh` with user's arguments
3. The helper script automatically detects available features and routes accordingly:
   - Checks for Python availability
   - Routes to Python scripts if enhanced mode installed
   - Falls back to standard shell implementation otherwise
4. Supports both explicit flags (`--search`) and natural language ("search for mcp")
5. Read documentation files from `docs/` directory

## Repository Structure

### Standard Mode Files (upstream-compatible)
- `install.sh` - Dual-mode installer (prompts for standard vs enhanced)
- `uninstall.sh` - Clean removal
- `scripts/claude-docs-helper.sh.template` - Standard helper (upstream reference)
- `scripts/claude-docs-helper.sh` - Enhanced helper with mode detection
- `docs/` - 47 mirrored documentation files
- `docs/docs_manifest.json` - Standard manifest (upstream)
- `.github/workflows/` - GitHub Actions for auto-updates

### Enhanced Mode Files (our additions)
- `scripts/main.py` - Enhanced fetcher (662 lines)
- `scripts/lookup_paths.py` - Search & validation (597 lines)
- `scripts/update_sitemap.py` - Sitemap management (504 lines)
- `scripts/build_search_index.py` - Full-text search indexer
- `paths_manifest.json` - Enhanced manifest (459 paths)
- `tests/` - 174 tests (140 passing, 85% pass rate)

### Documentation
- `@README.md` - User guide (dual-mode installation and usage)
- `@CONTRIBUTING.md` - Contribution guidelines (separate workflows for each mode)
- `@UNINSTALL.md` - Uninstallation guide
- `@CHANGELOG.md` - Version history

## Working on This Project

### Critical Rules

1. **Preserve Both Modes**: Standard mode MUST work without Python
2. **Test Both Modes**: Changes must be tested in both configurations
3. **Graceful Degradation**: Enhanced features should fail gracefully if unavailable
4. **Upstream Compatibility**: Standard mode should remain compatible with upstream

### For Standard Mode Changes

Work on these files:
- Shell scripts (`.sh` files)
- Installation/uninstallation logic
- GitHub Actions workflows
- Core documentation updates
- Helper script template

**Testing**:
```bash
./install.sh  # Answer 'N' to enhanced features
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh -t
```

### For Enhanced Mode Changes

Work on these files:
- Python scripts (`scripts/*.py`)
- Enhanced manifest (`paths_manifest.json`)
- Search and validation features
- Test suite (`tests/`)

**Testing**:
```bash
./install.sh  # Answer 'Y' to enhanced features
pytest tests/ -v
~/.claude-code-docs/claude-docs-helper.sh --search "mcp"
~/.claude-code-docs/claude-docs-helper.sh --validate
```

### Mode Detection Logic

The helper script detects mode at runtime:

```bash
# Check if Python and enhanced scripts are available
if command -v python3 &> /dev/null && [ -f "$SCRIPTS_DIR/lookup_paths.py" ]; then
    PYTHON_AVAILABLE="true"
    # Route to Python implementation
else
    PYTHON_AVAILABLE="false"
    # Use standard shell implementation
fi
```

**When adding new features**: Always check `$PYTHON_AVAILABLE` and provide fallback.

## Common Workflows

### Adding a New Enhanced Feature

1. Implement in Python script (`scripts/your_feature.py`)
2. Add mode detection to helper script
3. Write tests (`tests/unit/test_your_feature.py`)
4. Update README.md Enhanced Commands section
5. Update CONTRIBUTING.md
6. Test both modes still work
7. Submit PR with `[Enhanced]` prefix

### Syncing with Upstream

1. Fetch upstream changes: `git fetch upstream`
2. Review what changed in standard mode files
3. Merge carefully: `git merge upstream/main`
4. **Ensure enhanced features still work**
5. Test both installation modes
6. Update CHANGELOG.md

## Files to Think About

When making changes, consider impact on:

### Always Review
- `@install.sh` - Handles both mode installations
- `@scripts/claude-docs-helper.sh` - Routes between modes
- `@README.md` - Documents dual-mode usage
- `@CONTRIBUTING.md` - Guides contributors

### For Standard Features
- `@scripts/claude-docs-helper.sh.template` - Upstream reference
- `@uninstall.sh` - Must remove both modes cleanly
- `@.github/workflows/` - Auto-update workflows

### For Enhanced Features
- `@scripts/` - All Python scripts
- `@paths_manifest.json` - 459-path enhanced manifest
- `@tests/` - Test suite (target: 85%+ coverage)

## Migration Context

**This branch (`migration-to-upstream`)** is preparing enhanced features for potential contribution back to upstream. Key considerations:

- Standard mode remains fully compatible with upstream
- Enhanced features are cleanly separated (opt-in during install)
- Changes don't break existing upstream workflows
- Documentation clearly explains dual-mode architecture
- Both modes are well-tested and production-ready

## Getting Help

- **User issues**: See README.md troubleshooting
- **Development questions**: See CONTRIBUTING.md
- **Technical details**: See docs-dev/DEVELOPMENT.md (if exists)

---

**Remember**: Every change must work in both modes. Test accordingly!
