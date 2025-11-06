# Changelog - Enhanced Edition

All notable changes to the enhanced edition of claude-code-docs will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.4] - 2025-11-06

### Added
- **Dual-Mode Architecture**: Choose between standard (shell-only) or enhanced (Python-powered) modes during installation
- **Extended Documentation Coverage**: 449 documentation paths across 7 categories (vs 270 in standard mode)
- **Full-Text Search**: Search across all documentation content using `--search` flag
- **Validation Tools**: Verify documentation integrity with `--validate` command
- **Category Organization**: Documentation organized into core docs, API reference, Claude Code, prompt library, resources, release notes
- **Enhanced Directory**: Comprehensive feature documentation in `enhancements/` directory
  - `enhancements/README.md` - Overview and navigation
  - `enhancements/FEATURES.md` - Technical feature specifications
  - `enhancements/CAPABILITIES.md` - Detailed capability documentation
  - `enhancements/EXAMPLES.md` - Practical usage examples
- **Test Suite**: 174 tests with 80% code coverage
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
- **Manifest Alignment**: docs_manifest.json now accurately reflects 270 documentation files
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
- Automatic documentation updates via GitHub Actions
- `/docs` slash command integration
- PreToolUse Read hook for automatic updates

---

## Feature Comparison

| Feature | Standard Mode | Enhanced Mode |
|---------|--------------|---------------|
| Documentation Files | 270 | 270 |
| Documentation Paths | 270 | 449 |
| Basic Search | ✓ | ✓ |
| Full-Text Search | ✗ | ✓ |
| Category Filtering | ✗ | ✓ |
| Validation Tools | ✗ | ✓ |
| Dependencies | Shell, git, jq | + Python 3.12+ |
| Test Coverage | ✗ | 174 tests (80%) |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this enhanced edition.

For upstream contributions, see [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs).
