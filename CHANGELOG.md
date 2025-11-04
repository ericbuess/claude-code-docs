# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2025-11-04

### Phase 5: Documentation Alignment Complete ✅

**Migration Progress**: 5/7 phases complete (71%)

This release completes Phase 5 of the upstream migration plan, aligning all documentation with dual-mode architecture while preparing for contribution back to upstream.

### Changed

**README.md** - User-focused dual-mode documentation:
- Clear installation instructions for both standard and enhanced modes
- Natural language interface section for `/docs` command
- Feature comparison table (standard vs enhanced)
- Updated troubleshooting for both modes
- Project status updated to reflect Phase 5 completion

**CLAUDE.md** - Appropriate guidance for dual-mode repository:
- Explains dual-mode architecture (standard vs enhanced)
- Documents mode detection and routing logic
- Provides critical rules for maintaining both modes
- Shows common workflows for each mode
- Migration context for upstream contribution
- 182 lines (balanced - not too minimal, not bloated)

**CONTRIBUTING.md** - Comprehensive contribution guidelines (NEW):
- Separate workflows for standard vs enhanced features
- Code standards for shell scripts and Python
- Testing requirements for both modes
- Pull request templates and examples
- Release process documentation
- 571 lines of professional contribution guidance

### Documentation Philosophy

This phase establishes the right balance:
- NOT copying upstream's minimal docs (our repo has more complexity)
- NOT over-documenting with implementation details
- PROPERLY explaining dual-mode architecture
- GUIDING contributors to work with both modes safely

### Testing

- ✅ All documentation files validated
- ✅ Internal links verified (16 file references)
- ✅ Natural language examples tested
- ✅ Installation instructions accurate for both modes
- ✅ Path references updated to docs-dev/ structure

### Next Phase

**Phase 6: Testing & Validation**
- Fix test suite failures (140/174 passing → 174/174)
- Improve code coverage (24% → 85%+)
- Add installation tests
- Update CI/CD workflows
- End-to-end testing

## [0.4.0] - 2025-11-04

### Added - Enhanced Installation System

**Dual-Mode Installation:**
- ✅ Optional enhanced features during installation
- ✅ Standard mode: 47 docs, no Python required (upstream compatible)
- ✅ Enhanced mode: 449 paths, Python 3.12+ features
- ✅ Graceful degradation when Python not available

**Enhanced Helper Script** (`scripts/claude-docs-helper.sh`):
- New `--search <query>` - Fuzzy search 449 paths
- New `--search-content <term>` - Full-text content search
- New `--validate` - Validate all paths for reachability
- New `--update-all` - Fetch all 449 documentation pages
- New `--version` - Show version and feature status
- New `--status` - Show installation status
- New `--help` - Show all available commands
- Auto-detection of Python availability
- Automatic fallback to standard template when enhanced features unavailable

**Installation Improvements:**
- One-line installation with mode selection
- Python version check (3.12+ required for enhanced features)
- Automatic dependency installation (requests library)
- Enhanced manifest download (459 paths)
- Search index building (if available)
- Detailed status reporting

**Documentation Updates:**
- Updated README.md with dual-mode installation instructions
- Enhanced .claude/commands/docs.md with all commands documented
- Clear distinction between standard and enhanced features
- Installation examples for both modes

### Changed
- Modified install.sh to offer enhanced features as opt-in (line 512+)
- .claude/commands/docs.md now documents both standard and enhanced commands
- Helper script location: `~/.claude-code-docs/scripts/claude-docs-helper.sh`

### Backward Compatibility
- ✅ 100% backward compatible with upstream (ericbuess/claude-code-docs)
- ✅ Standard installation unchanged (47 docs, shell-only)
- ✅ Enhanced features only activated if user opts in
- ✅ Graceful degradation without Python

### Migration Notes
- Existing installations unaffected
- Re-run installer to add enhanced features
- Answer 'Y' when prompted for enhanced edition
- Python 3.12+ required for enhanced features

## [0.3.0] - 2025-11-03

### Added
- Initial implementation of Claude Code documentation mirror
- 459 unique documentation paths across 6 categories
- Automated updates every 3 hours via GitHub Actions
- Natural language documentation search via `/docs` command
- Path validation and search utilities
- Enhanced path extraction with categorization
- Direct markdown fetching (no HTML conversion needed)
- SHA256-based change detection
- Comprehensive error handling and retry logic

### Categories Included
- Core Documentation (156 paths - 34.0%)
- API Reference (91 paths - 19.8%)
- Claude Code Documentation (68 paths - 14.8%)
- Prompt Library (64 paths - 13.9%)
- Resources (72 paths - 15.7%)
- Release Notes (5 paths - 1.1%)
- Uncategorized (3 paths - 0.7%)

### Scripts
- `main.py` - Enhanced documentation fetcher (662 lines)
- `extract_paths.py` - Path extraction and cleaning (534 lines)
- `lookup_paths.py` - Path search and validation (597 lines)
- `update_sitemap.py` - Sitemap management (483 lines)

### Claude Code Integration
- `/docs` - Natural language documentation search
- `/update-docs` - Update documentation mirror
- `/search-docs` - Search documentation paths
- `/validate-docs` - Validate all paths

### GitHub Actions Workflows
- `update-docs.yml` - Auto-update every 3 hours
- `test.yml` - Run tests on push/PR
- `validate.yml` - Daily path validation

## [0.1.0] - 2025-11-03

### Initial Release
- Project setup and structure
- Repository analysis (Phase 1)
- Path extraction and cleaning (Phase 2)
- Script development (Phase 3)
- Integration and adaptation (Phase 4)
- Match ericbuess/claude-code-docs structure
- Configure .claude/ integration
- Setup GitHub Actions automation
- Version control configuration
