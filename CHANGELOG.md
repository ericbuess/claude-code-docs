# Changelog - Enhanced Edition

All notable changes to the enhanced edition of claude-code-docs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2025-12-06

### Breaking Changes
- **Filename Convention Changed**: All Claude Code CLI docs renamed to use domain-based prefix
  - Old: `docs__en__<topic>.md` (e.g., `docs__en__hooks.md`)
  - New: `claude-code__<topic>.md` (e.g., `claude-code__hooks.md`)
  - Platform docs use: `docs__en__<path>.md`
- **Scripts Restructured**: Monolithic scripts replaced with modular packages
  - Added: `scripts/fetcher/` (8 modules for documentation fetching)
  - Added: `scripts/lookup/` (7 modules for search and validation)
  - Removed: `main.py`, `update_sitemap.py`, `extract_paths.py`, `clean_manifest.py`

### Added
- **2x Documentation Coverage**: 571 files (up from ~270)
- **573 Tracked Paths**: Comprehensive coverage across 6 categories
  - API Reference: 377 paths (65.8%)
  - Core Documentation: 82 paths (14.3%)
  - Prompt Library: 65 paths (11.3%)
  - Claude Code: 46 paths (8.0%)
  - Release Notes: 2 paths
  - Resources: 1 path
- **Safety Thresholds**: Prevent catastrophic deletion during automated sync
  - `MIN_DISCOVERY_THRESHOLD`: 200 paths minimum from sitemaps
  - `MAX_DELETION_PERCENT`: 10% maximum deletion per sync
  - `MIN_EXPECTED_FILES`: 250 minimum files required
- **Modular Architecture**: Better code organization and testability
  - `fetcher/` package: config, manifest, paths, sitemap, content, safeguards, cli
  - `lookup/` package: config, manifest, search, validation, formatting, cli
- **Domain-Based Naming**: Clear source identification in filenames
  - `claude-code__*.md` from code.claude.com
  - `docs__en__*.md` from platform.claude.com
- **Version-Aware Upgrades**: Installer detects existing version and shows upgrade info

### Changed
- **Manifest Structure**: `paths_manifest.json` now tracks 573 paths in 6 categories
- **Search Index**: Updated to cover all 571 documentation files
- **Python Packages**: Thin wrappers (`fetch_claude_docs.py`, `lookup_paths.py`) for backward compatibility

### Upgrade Notes
- **Seamless Upgrade**: Run `install.sh` again to upgrade from any v0.4.x version
- **No Data Loss**: All user configs remain in `~/.claude/`
- **Atomic Operation**: Installation uses temp directory, moves atomically
- The installer will show before/after comparison during upgrade

## [0.4.2] - 2025-11-25

### Fixed
- **Critical Auto-Update Bug**: Fixed issue where `/docs -t` would destroy the installation directory
  - Root cause: Running `install.sh` from within `~/.claude-code-docs` caused the script to delete its own working directory
  - Solution: Replaced full reinstall with lightweight script sync after `git pull`
- **Template Fallback**: Enhanced helper now gracefully degrades if template is missing instead of failing completely
- **Security: Path Traversal Protection**: Added realpath validation in fallback mode to ensure files stay within docs directory
  - Input sanitization removes special characters (already existed)
  - New: Resolved path validation ensures no escape from docs directory
- **Silent Failure Logging**: sync_helper_script() now logs failures to stderr for debugging
  - Previously errors were silently suppressed with `|| true`
  - Now provides feedback when copy or move operations fail

### Removed
- **Useless Hook**: Removed the PreToolUse hook that did nothing (just `exit 0`)
  - The hook fired on every Read tool use but provided no functionality
  - Updates now happen on-demand via `/docs -t` command

### Added
- **Post-Installation Verification**: Installer now validates all critical components after installation
  - Checks helper script, template, docs directory, and command file
  - Reports issues instead of silently failing
- **Lock File Mechanism**: Added lock file to prevent concurrent update operations
  - Prevents race conditions when multiple `/docs` commands run simultaneously
  - Automatically cleans up stale locks (older than 60 seconds)
- **Integration Tests**: Added 9 new tests for critical bug fix scenarios (627 tests total)
  - Tests for sync_helper_script() atomic copy behavior
  - Tests verifying update doesn't delete working directory
  - Tests for template fallback functionality
  - Tests for lock file mechanism
  - Tests for path traversal protection

### Changed
- **Documentation Accuracy**: Updated README and installer messages to clarify update behavior
  - Removed misleading "Auto-updates: Enabled" claims
  - Clarified that updates are on-demand via `/docs -t`
- **Test Suite**: Updated from 618 to 627 passing tests (78.7% coverage maintained)

## [0.4.1] - 2025-11-24

### Fixed
- **Version Alignment**: Updated all version strings from v0.3.4 to v0.4.1 to match git tag
- **Path Count Accuracy**: Corrected all documentation from outdated 268/270 to accurate 273 paths tracked
- **File Count Clarity**: Clarified distinction between paths tracked (273) vs files downloaded (~266-270)
- **Category Breakdown**: Updated all category counts to match current manifest:
  - Core Documentation: 80 paths (29.3%)
  - API Reference: 79 paths (28.9%)
  - Prompt Library: 65 paths (23.8%)
  - Claude Code: 45 paths (16.5%)
  - Release Notes: 2 paths
  - Resources: 1 path
  - Uncategorized: 1 path

### Changed
- **Architecture Documentation**: Replaced outdated "Dual-Mode" concept with accurate "Single Installation with Graceful Degradation"
- **Enhancement Documentation**: Updated all enhancement docs (FEATURES.md, CAPABILITIES.md, README.md) with accurate numbers
- **Install Messages**: Updated installer output to show accurate, consistent information

## [0.4.0] - 2025-11-24

**Note**: This tag was created but version strings in code were not updated (still showed v0.3.4). Fixed in v0.4.1.

## [0.3.4] - 2025-11-06

### Added
- **Dual-Mode Architecture**: Choose between standard (shell-only) or enhanced (Python-powered) modes during installation
- **Extended Documentation Coverage**: 449 documentation paths across 7 categories (vs 269 in standard mode)
- **Full-Text Search**: Search across all documentation content using `--search` flag
- **Validation Tools**: Verify documentation integrity with `--validate` command
- **Category Organization**: Documentation organized into core docs, API reference, Claude Code, prompt library, resources, release notes
- **Enhanced Directory**: Comprehensive feature documentation in `enhancements/` directory
  - `enhancements/README.md` - Overview and navigation
  - `enhancements/FEATURES.md` - Technical feature specifications
  - `enhancements/CAPABILITIES.md` - Detailed capability documentation
  - `enhancements/EXAMPLES.md` - Practical usage examples
- **Test Suite**: 566 tests with 81.41% code coverage (target: 82%)
- **Performance Benchmarks**: Documented search, fetch, and validation performance characteristics

### Changed
- **README.md**: Updated to version 0.3.4 with enhanced features section
- **CLAUDE.md**: Comprehensive instructions for dual-mode architecture
- **Repository Structure**: Reorganized for clearer separation between standard and enhanced modes

### Improved
- **Installation**: Installer now prompts for mode selection (standard vs enhanced)
- **Mode Detection**: Helper script automatically detects Python availability and routes commands appropriately
- **Documentation**: All documentation verified against actual fetched content (449 paths confirmed)
- **Graceful Degradation**: Enhanced features fall back to standard mode when Python unavailable

### Fixed
- **File Count Accuracy**: Corrected documentation references from outdated counts to actual values
- **Manifest Alignment**: docs_manifest.json now accurately reflects 269 documentation files
- **Category Counts**: All category counts verified against paths_manifest.json

### Removed
- **Temporary Tracking Files**: Removed 20+ intermediate development tracking files
  - Phase reports (PHASE*.md)
  - Task summaries (TASK*.md)
  - Migration tracking (MIGRATION_*.md)
  - Analysis artifacts (analysis/execution/)
  - Development artifacts (docs-dev/)

## [0.3.3] - Upstream Baseline

### Inherited from Upstream
- Claude Code changelog integration
- Full macOS compatibility
- Linux support (Ubuntu, Debian, Fedora)
- Improved installer
- Documentation updates via GitHub Actions (repository-side)
- `/docs` slash command integration

---

## Feature Comparison

| Feature | Standard Mode | Enhanced Mode |
|---------|--------------|---------------|
| Documentation Files | 269 | 269 |
| Documentation Paths | 269 | 449 |
| Basic Search | ✓ | ✓ |
| Full-Text Search | ✗ | ✓ |
| Category Filtering | ✗ | ✓ |
| Validation Tools | ✗ | ✓ |
| Dependencies | Shell, git, jq | + Python 3.9+ |
| Test Coverage | ✗ | 577 tests (72%) |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this enhanced edition.

For upstream contributions, see [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs).
