# Changelog - Enhanced Edition

All notable changes to the enhanced edition of claude-code-docs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
