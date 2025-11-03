# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
