# Claude Code Documentation Mirror - Enhanced Edition

> Project instructions for Claude Code when working in this repository.

This repository extends [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) with optional Python-based enhancements while maintaining full backward compatibility with upstream.

## For /docs Command

The `/docs` command is a **unified interface** that handles both standard and enhanced features automatically:

**How it works:**
1. The command reads `~/.claude/commands/docs.md` for complete instructions
2. It analyzes user intent (natural language OR explicit flags)
3. Executes `~/.claude-code-docs/scripts/claude-docs-helper.sh` with appropriate arguments
4. The helper script detects available features and routes to the right implementation:
   - **Standard mode**: Shell scripts only (47 docs, no Python)
   - **Enhanced mode**: Python scripts when available (459 paths, advanced search)

**Key insight:** Users don't need to know which mode they're in. The command adapts automatically.

**Natural language examples:**
- `/docs search for mcp` → Auto-converts to `--search "mcp"` if enhanced mode
- `/docs find content about hooks` → Auto-converts to `--search-content "hooks"` if enhanced mode
- `/docs hooks` → Reads topic (works in both modes)

**Explicit flags** (for power users):
- `/docs --search "query"` → Fuzzy search (enhanced only)
- `/docs --search-content "query"` → Full-text search (enhanced only)
- `/docs --validate` → Path validation (enhanced only)
- `/docs --update-all` → Fetch all docs (enhanced only)

## Project Structure

### User Documentation
- `@README.md` - User guide and quick start (installation, usage, features)
- `@ENHANCEMENTS.md` - Enhanced features documentation (planned)
- `@UNINSTALL.md` - Uninstallation guide
- `@CHANGELOG.md` - Version history

### Developer Documentation
- `@CONTRIBUTING.md` - Contribution guidelines
- `@DEVELOPMENT.md` - Developer guide
- `@MIGRATION_PLAN.md` - Upstream alignment plan

### Planning & Implementation
- `@docs-dev/specs/IMPLEMENTATION_PLAN.md` - Complete 7-phase roadmap
- `@docs-dev/specs/IMPLEMENTATIONMONITOR.md` - Progress tracking
- `@docs-dev/specs/execution_template.md` - Phase execution templates

### Code Organization
- `@scripts/` - All Python and shell scripts
  - `scripts/claude-docs-helper.sh` - Enhanced wrapper (planned)
  - `scripts/claude-docs-helper.sh.template` - Standard helper from upstream
  - `scripts/fetch_claude_docs.py` - Upstream fetcher (reference)
  - `scripts/main.py` - Our enhanced fetcher (662 lines)
  - `scripts/lookup_paths.py` - Search & validation (597 lines)
  - `scripts/update_sitemap.py` - Sitemap management (504 lines)
  - `scripts/build_search_index.py` - Full-text search indexer
  - `scripts/extract_paths.py` - Path extraction (534 lines)
  - `scripts/clean_manifest.py` - Manifest cleaning (172 lines)
- `@tests/` - 174 tests (82 unit + 36 integration + 56 validation)
  - Run with: `pytest tests/ -v`
  - Check coverage: `pytest --cov=scripts --cov-report=term`
- `@.github/workflows/` - CI/CD automation
  - `update-docs.yml` - Auto-update docs every 3 hours
  - `test.yml` - Run tests on push/PR
  - `validate.yml` - Daily path validation
  - `coverage.yml` - Coverage reporting

### Documentation Files
- `@docs/` - 47 mirrored documentation files (from upstream)
  - `docs/sitemap.json` - Full sitemap of 459 paths
  - `docs/.search_index.json` - Search optimization (enhanced mode)
  - `docs/docs_manifest.json` - Upstream's manifest

## When Working on This Project

### Standard Features (Upstream Compatible)

**Philosophy:**
- Use shell scripts (bash) only
- Maintain backward compatibility with ericbuess/claude-code-docs
- Follow upstream conventions
- No Python dependencies required
- Must work on macOS and Linux

**Guidelines:**
- Reference `@scripts/claude-docs-helper.sh.template` for patterns
- Use `set -euo pipefail` in shell scripts
- Sanitize user inputs
- Comment complex logic
- Test on both macOS and Linux

### Enhanced Features (Python-Based)

**Philosophy:**
- Python 3.12+ required
- Optional add-ons (don't break standard mode)
- Add comprehensive tests
- Document in ENHANCEMENTS.md
- Graceful degradation when Python unavailable

**Guidelines:**
- Type hints required: `def func(x: str) -> int:`
- Docstrings required for public functions
- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use descriptive variable names
- Test coverage target: 85%+

**Example:**
```python
def search_paths(query: str, limit: int = 20) -> List[str]:
    """
    Search for paths matching the query.

    Args:
        query: Search term (fuzzy matching)
        limit: Maximum results to return

    Returns:
        List of matching paths, sorted by relevance
    """
    # Implementation...
```

## Current Development Status

**Branch**: `migration-to-upstream`
**Phase**: 5/7 (Documentation alignment in progress)
**Progress**: 68% (19/28 tasks)

### Phase Status

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Repository setup & analysis |
| Phase 2 | ✅ Complete | Path extraction & cleaning |
| Phase 3 | ✅ Complete | Script development |
| Phase 4 | ✅ Complete | Integration & adaptation |
| Phase 5 | 🔄 In Progress | Documentation alignment |
| Phase 6 | ⏳ Pending | Testing & validation |
| Phase 7 | ⏳ Pending | Quality assurance |

### Current Tasks (Phase 5)

- ✅ Update README.md for dual-mode installation
- 🔄 Update CLAUDE.md with project guidance
- ⏳ Create CONTRIBUTING.md for contributors
- ⏳ Validate all documentation links
- ⏳ Commit Phase 5 changes

## Contributing

Enhancements should be:

1. **Optional** - Don't require Python in standard mode
2. **Well-tested** - Add tests to `tests/` directory
3. **Documented** - Update ENHANCEMENTS.md and other relevant docs
4. **Backward compatible** - Work with upstream (ericbuess/claude-code-docs)
5. **Graceful** - Degrade gracefully when dependencies unavailable

See `@CONTRIBUTING.md` for detailed guidelines.

## Git Workflow

### Development
- **Current branch**: `migration-to-upstream`
- **Main branch**: Production-ready code only
- **Commit messages**: Descriptive, reference file:line when discussing code

### Before Making Changes

1. Read relevant specs in `@docs-dev/specs/IMPLEMENTATION_PLAN.md`
2. Check `@docs-dev/specs/IMPLEMENTATIONMONITOR.md` for current progress
3. Review `@MIGRATION_PLAN.md` for alignment strategy

### After Completing Work

1. Update `@docs-dev/specs/IMPLEMENTATIONMONITOR.md` checkboxes
2. Run tests (if Python features): `pytest tests/ -v`
3. Update documentation if adding features
4. Commit with descriptive message

## Common Commands

### For Standard Mode Work
```bash
# Test standard installation
./install.sh
# Answer 'N' to enhanced features

# Verify standard commands
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh -t
```

### For Enhanced Mode Work
```bash
# Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Test enhanced installation
./install.sh
# Answer 'Y' to enhanced features

# Run tests
pytest tests/ -v
pytest --cov=scripts --cov-report=term

# Test enhanced commands
~/.claude-code-docs/claude-docs-helper.sh --search "mcp"
~/.claude-code-docs/claude-docs-helper.sh --validate
```

### For Development
```bash
# Check project status
git status
git branch --show-current

# Search documentation
python scripts/lookup_paths.py "prompt engineering"
python scripts/lookup_paths.py --search-content "tool use"

# Update documentation
python scripts/main.py --update-all

# Validate paths
python scripts/lookup_paths.py --validate-all

# Build search index
python scripts/build_search_index.py
```

## Testing Requirements

### Standard Mode
- Manual testing on macOS and Linux
- Verify shell script behavior
- Test without Python installed

### Enhanced Mode
- **Minimum coverage**: 85% (currently 24%)
- **Required suites**: Unit, Integration, Validation
- All tests must pass before marking phase complete

**Running tests:**
```bash
# Run all 174 tests
pytest

# Run specific suites
pytest tests/unit/          # 82 unit tests
pytest tests/integration/   # 36 integration tests
pytest tests/validation/    # 56 validation tests

# With coverage
pytest --cov=scripts --cov-report=html
pytest --cov=scripts --cov-report=term

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

**Current status**: 140/174 tests passing (85% pass rate)

## Technical Specifications

### Path Categorization
- `/en/docs/` (excluding claude-code) → `core_documentation` (151 paths)
- `/en/api/` → `api_reference` (91 paths)
- `/en/docs/claude-code/` → `claude_code` (68 paths)
- `/en/prompt-library/` → `prompt_library` (64 paths)
- Resources, release notes, uncategorized (75 paths)
- **Total**: 459 unique paths

### Fetching Implementation
**Key Discovery**: Anthropic's docs site serves markdown directly at `.md` URLs!

```python
# No HTML parsing needed
url = f"https://docs.anthropic.com{path}.md"
response = requests.get(url)
markdown_content = response.text
```

**Features**:
- Only need `requests==2.32.4` (no beautifulsoup4 or markdownify)
- SHA256-based change detection (only fetch what changed)
- Retry logic with exponential backoff
- Rate limiting (0.5s between requests)

## Performance Targets

### Standard Mode
- Update time: ~0.4 seconds (git pull) ✅
- Search time: Instant topic matching ✅
- Memory usage: < 50 MB ✅

### Enhanced Mode
- Fetch time: < 2 minutes per 100 pages ✅ (~1.5 min actual)
- Memory usage: < 500 MB ✅ (~320 MB actual)
- Search performance: < 1 second ✅ (< 100ms actual)
- Path reachability: > 99% (target)

## Dependencies

### Standard Mode
- Git
- Bash
- jq, curl (usually pre-installed)

### Enhanced Mode (Additional)
- Python 3.12+
- requests==2.32.4
- pytest + pytest-cov (testing only)

## Success Criteria

### Installation
- ✅ Standard install works without Python
- ✅ Enhanced install detects Python 3.12+
- ⏳ Migration from upstream works seamlessly
- ⏳ Uninstall removes everything cleanly
- ⏳ Works on macOS 12+ and Ubuntu 22.04+

### Functionality
- ✅ All upstream features preserved
- ⏳ /docs command works for all modes
- ✅ 459 paths validated and reachable (97.8%)
- ✅ Full-text search works correctly
- ✅ Path validation completes in < 60s (~30s actual)
- ⏳ Auto-update hook works

### Testing
- ⏳ 174 tests all passing (100%) - currently 140 (85%)
- ⏳ CI/CD runs tests on push/PR
- ⏳ Coverage reporting works
- ⏳ Tests pass on macOS and Linux

### Documentation
- 🔄 README.md clear for users
- ⏳ ENHANCEMENTS.md complete
- ⏳ CONTRIBUTING.md helpful for contributors
- ⏳ All examples working

## Useful File References

### User-Facing Documentation
- `@README.md` - Project overview and quick start
- `@ENHANCEMENTS.md` - Enhanced features (to be created)
- `@CONTRIBUTING.md` - Contribution guidelines (to be created)
- `@CHANGELOG.md` - Version history

### Development Documentation
- `@DEVELOPMENT.md` - Contributor guide
- `@MIGRATION_PLAN.md` - Upstream alignment strategy

### Implementation Planning
- `@docs-dev/specs/IMPLEMENTATION_PLAN.md` - Complete 7-phase roadmap with rationale
- `@docs-dev/specs/IMPLEMENTATIONMONITOR.md` - Detailed progress tracking
- `@docs-dev/specs/execution_template.md` - Phase execution templates

### Analysis Documents
- `@docs-dev/analysis/repo_structure.md` - Upstream repository analysis
- `@docs-dev/analysis/fetch_mechanism.md` - Fetching implementation details
- `@docs-dev/analysis/path_mapping.md` - Path-to-file mapping rules
- `@docs-dev/analysis/sitemap_statistics.md` - Comprehensive path statistics

## Important Rules

### For Claude Code When Working Here

1. **Use @ to reference files** - Example: `@README.md`, `@scripts/main.py`
2. **Update progress tracking** - Always update `@docs-dev/specs/IMPLEMENTATIONMONITOR.md` after completing tasks
3. **Test before committing** - Run pytest for Python changes
4. **Reference file:line numbers** - When discussing code, use format like `scripts/main.py:42`
5. **Preserve both modes** - Ensure standard mode continues to work without Python
6. **Document changes** - Update relevant documentation files

### Phase Execution

- Execute phases in order: 1→2→3→4→5→6→7
- Each phase builds on the previous
- Don't skip phases
- Update docs-dev/specs/IMPLEMENTATIONMONITOR.md after each task completion

---

**Remember**: This is a dual-mode project. Standard mode must always work (no Python), while enhanced mode provides optional power features. All contributions must preserve both modes.

**Status**: Active Development | Phase 5 In Progress

**Built with Claude Code** | Following Anthropic's best practices
