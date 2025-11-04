# Claude Code Documentation Mirror

[![Build Status](https://img.shields.io/badge/build-passing-success)](https://github.com/costiash/claude-code-docs)
[![Test Coverage](https://img.shields.io/badge/coverage-24%25-yellow)](./tests)
[![Tests](https://img.shields.io/badge/tests-140%2F164%20passing-orange)](./tests)
[![Python](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

> **Local mirror of Anthropic's Claude documentation with optional enhanced features.**

Fast offline access to Claude Code documentation with automated updates. Choose between standard mode (47 core docs, shell-based) or enhanced mode (459 paths with Python-powered search and validation).

## Why This Exists

- **Offline Access**: Work with Claude Code docs when internet is unavailable
- **Fast Lookups**: Instant local search instead of web browsing
- **Auto-Updates**: GitHub Actions keep docs fresh automatically
- **Claude Integration**: Natural language queries via `/docs` command
- **Optional Enhancements**: Advanced search, validation, and 10x more content (opt-in)

## Installation

### Quick Install

One-line installation to `~/.claude-code-docs`:

```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

During installation, you'll be prompted:

**Installation Mode:**
- **Standard (N - default)**: 47 documentation topics, no Python required, shell-based commands
- **Enhanced (Y)**: 459 documentation paths, Python 3.12+, advanced search and validation

**Standard Mode** is perfect for most users. **Enhanced Mode** is for power users who want comprehensive coverage and advanced features.

### Prerequisites

**Standard Mode:**
- Git
- Bash
- jq, curl (usually pre-installed)
- Claude Code (for `/docs` integration)

**Enhanced Mode (additional):**
- Python 3.12+
- pip (Python package manager)

### Manual Installation (Developers)

For development or customization:

```bash
# Clone repository
git clone https://github.com/costiash/claude-code-docs.git
cd claude-code-docs

# For enhanced features: Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Verify installation
python scripts/lookup_paths.py --help
```

## Usage

### Standard Commands

Available in both standard and enhanced modes:

```bash
# List all documentation topics
/docs

# Read specific documentation
/docs hooks
/docs mcp
/docs prompt engineering

# Check for updates
/docs -t

# View recent changes
/docs what's new

# View Claude Code changelog
/docs changelog
```

### Enhanced Commands (Enhanced Mode Only)

Additional commands when Python 3.12+ is installed:

```bash
# Fuzzy search across 459 paths
/docs --search "prompt engineering"
/docs --search "mcp quickstart"

# Full-text search in documentation content
/docs --search-content "extended thinking"
/docs --search-content "tool use examples"

# Validate all documentation paths
/docs --validate

# Update all 459 documentation files
/docs --update-all

# Show all available options
/docs --help
```

## Features

### Standard Mode

**What you get:**
- 47 core Claude Code documentation files
- Simple topic-based search
- Auto-updates via git pull (every 3 hours)
- PreToolUse Read hook for automatic freshness checks
- Zero Python dependencies
- Works on macOS and Linux

**Perfect for:**
- Quick documentation lookups
- Users who prefer minimal setup
- Environments without Python
- Basic Claude Code reference needs

### Enhanced Mode

**Everything in Standard Mode, plus:**
- **459 documentation paths** (10x coverage) across:
  - Core Documentation (151 paths)
  - API Reference (91 paths)
  - Claude Code Documentation (68 paths)
  - Prompt Library (64 paths)
  - Resources (68 paths)
  - Release Notes (4 paths)
- **Full-text search** - Search documentation content, not just titles
- **Fuzzy path search** - Find paths with relevance ranking
- **Path validation** - HTTP reachability testing for all paths
- **Selective updates** - SHA256-based change detection
- **174 tests** (140 passing) for reliability

**Perfect for:**
- Power users who want comprehensive coverage
- Developers who need advanced search capabilities
- Users working with multiple Claude documentation areas
- Contributors who want to test and validate

See [ENHANCEMENTS.md](./ENHANCEMENTS.md) for detailed feature documentation.

## Feature Comparison

| Feature | Standard Mode | Enhanced Mode |
|---------|---------------|---------------|
| Documentation files | 47 core topics | 459 paths (all categories) |
| Search | Topic name only | Full-text + fuzzy search |
| Validation | None | HTTP reachability testing |
| Updates | Git pull (3-hour schedule) | Selective fetch (SHA256) |
| Testing | None | 174 tests with pytest |
| Python required | No | Yes (3.12+) |
| Dependencies | git, jq, curl | + Python, requests |
| Perfect for | Quick lookups | Comprehensive reference |

## Updating

### Automatic Updates (Both Modes)

Documentation automatically updates every 3 hours via GitHub Actions. The PreToolUse Read hook ensures you always read the latest version.

### Manual Updates

**Standard Mode:**
```bash
cd ~/.claude-code-docs
git pull
```

**Enhanced Mode:**
```bash
# Update all 459 documentation files
/docs --update-all

# Or use Python directly
cd ~/.claude-code-docs
python scripts/main.py --update-all
```

## Documentation Structure

This mirror organizes Claude documentation into categories:

1. **Core Documentation** (151 paths) - Messages API, prompt engineering, vision, PDFs, streaming, caching, tools
2. **API Reference** (91 paths) - REST API, Admin API, SDKs, platform APIs, versioning
3. **Claude Code** (68 paths) - Installation, commands, integrations, MCP, workflows, troubleshooting
4. **Prompt Library** (64 paths) - Curated prompts for code, content, analysis, business, creative tasks
5. **Resources** (68 paths) - Guides, references, model cards, additional materials
6. **Release Notes** (4 paths) - Product updates and changelogs

See [docs/sitemap.json](./docs/sitemap.json) for the complete documentation tree.

## Troubleshooting

### Standard Mode Issues

**Problem**: `/docs` command not found

**Solution**:
```bash
# Re-run installation
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
```

**Problem**: Documentation seems outdated

**Solution**:
```bash
# Check sync status
/docs -t

# Manually update
cd ~/.claude-code-docs && git pull
```

**Problem**: PreToolUse Read hook not triggering

**Solution**:
```bash
# Check Claude settings
cat ~/.claude/settings.json | jq '.hooks.PreToolUse'

# Re-run installer to fix hooks
~/.claude-code-docs/install.sh
```

### Enhanced Mode Issues

**Problem**: Enhanced commands not available after installation

**Solution**:
```bash
# Check Python version (must be 3.12+)
python3 --version

# Verify requests library installed
pip3 list | grep requests

# Reinstall enhanced features
~/.claude-code-docs/install.sh
# Answer 'Y' to enhanced features
```

**Problem**: `--search-content` returns no results

**Solution**:
```bash
# Rebuild search index
cd ~/.claude-code-docs
python scripts/build_search_index.py
```

**Problem**: `--validate` command fails

**Solution**:
```bash
# Check internet connectivity
curl -I https://docs.anthropic.com

# Run validation with verbose output
cd ~/.claude-code-docs
python scripts/lookup_paths.py --validate-all
```

**Problem**: Import errors or missing modules

**Solution**:
```bash
# Reinstall dependencies
cd ~/.claude-code-docs
pip install -r scripts/requirements.txt
```

## Contributing

We welcome contributions! This project maintains two modes:

1. **Standard Mode** - Shell-based, upstream-compatible (no Python)
2. **Enhanced Mode** - Python-based optional features

**All contributions must preserve both modes.**

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines on:
- Development workflow (standard vs enhanced features)
- Code standards (shell scripts vs Python)
- Testing requirements
- PR guidelines and review process
- Release process

### Quick Start for Contributors

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/claude-code-docs.git
cd claude-code-docs

# For enhanced features
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Make changes, add tests
pytest tests/ -v

# Submit PR
```

## Testing

**Enhanced mode only** - Comprehensive test suite:

```bash
# Run all tests (174 total)
pytest

# Run specific suites
pytest tests/unit/          # 82 unit tests
pytest tests/integration/   # 36 integration tests
pytest tests/validation/    # 56 validation tests

# Check coverage
pytest --cov=scripts --cov-report=term
```

Current status: 140/174 tests passing (85% pass rate), 24% code coverage (target: 85%).

## Performance

### Standard Mode
- **Update time**: ~0.4 seconds (git pull)
- **Search time**: Instant topic matching
- **Memory usage**: < 50 MB

### Enhanced Mode
- **Fetch time**: ~1.5 minutes per 100 pages
- **Search time**: < 100ms per query
- **Path validation**: ~30 seconds for 459 paths (parallel)
- **Memory usage**: ~320 MB during full fetch

## Project Status

**Current Phase**: 5/7 Complete (Documentation alignment in progress)

**Progress**: 68% (19/28 tasks)

| Phase | Status | Description |
|-------|--------|-------------|
| Phase 1 | ✅ Complete | Repository setup & analysis |
| Phase 2 | ✅ Complete | Path extraction & cleaning |
| Phase 3 | ✅ Complete | Script development |
| Phase 4 | ✅ Complete | Integration & adaptation |
| Phase 5 | 🔄 In Progress | Documentation alignment |
| Phase 6 | ⏳ Pending | Testing & validation |
| Phase 7 | ⏳ Pending | Quality assurance |

See [docs-dev/specs/IMPLEMENTATIONMONITOR.md](./docs-dev/specs/IMPLEMENTATIONMONITOR.md) for detailed progress tracking.

## Acknowledgments

This project extends [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) with optional Python-based enhancements.

**Built on excellent work by:**
- **[ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)** - Original implementation
- **[Anthropic](https://www.anthropic.com/)** - Claude Code and documentation

**Special thanks for:**
- Proven installation mechanism (538-line battle-tested installer)
- PreToolUse Read hook pattern for auto-updates
- GitHub Actions workflows
- Community feedback and testing

**What this enhanced edition adds:**
- 459 paths vs 47 (10x coverage)
- Full-text search and fuzzy matching
- Path validation and reachability testing
- 174 tests for reliability
- Comprehensive developer documentation

## Documentation

### User Documentation
- **[README.md](./README.md)** - This file (quick start and usage)
- **[ENHANCEMENTS.md](./ENHANCEMENTS.md)** - Enhanced features documentation
- **[UNINSTALL.md](./UNINSTALL.md)** - Uninstallation guide
- **[CHANGELOG.md](./CHANGELOG.md)** - Version history

### Developer Documentation
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Contribution guidelines
- **[docs-dev/DEVELOPMENT.md](./docs-dev/DEVELOPMENT.md)** - Developer guide
- **[CLAUDE.md](./CLAUDE.md)** - Project instructions for Claude Code

### Planning & Analysis
- **[MIGRATION_PLAN.md](./MIGRATION_PLAN.md)** - Upstream alignment plan
- **[docs-dev/specs/IMPLEMENTATION_PLAN.md](./docs-dev/specs/IMPLEMENTATION_PLAN.md)** - 7-phase roadmap
- **[docs-dev/specs/IMPLEMENTATIONMONITOR.md](./docs-dev/specs/IMPLEMENTATIONMONITOR.md)** - Progress tracking

## License

Documentation content © Anthropic. Used under fair use for educational purposes.

This mirror tool and enhancements are open source. See [LICENSE](./LICENSE) for details.

## Links

- **Official Claude Docs**: https://docs.anthropic.com/
- **Claude Code**: https://claude.ai/code
- **Anthropic**: https://www.anthropic.com/
- **Upstream Project**: https://github.com/ericbuess/claude-code-docs
- **Issue Tracker**: https://github.com/costiash/claude-code-docs/issues

---

**Status**: Active Development | Phase 5 In Progress

**Built with Claude Code** | Following Anthropic's best practices
