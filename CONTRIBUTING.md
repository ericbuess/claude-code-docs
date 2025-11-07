# Contributing Guidelines

Thank you for contributing to the Enhanced Claude Code Documentation Mirror!

## Project Philosophy

This project maintains **two modes** to serve different user needs:

1. **Standard Mode** - Fully compatible with upstream ([ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs))
   - Shell-based (bash) implementation
   - No Python dependencies required
   - 269 core documentation files
   - Perfect for basic documentation access

2. **Enhanced Mode** - Optional Python-based features (opt-in)
   - Python 3.12+ required
   - 449 documentation paths (10x coverage)
   - Full-text search and validation
   - Advanced features for power users

**All contributions must preserve both modes.** Standard mode must continue to work without Python.

## Repository URL Strategy

This project uses a clear strategy for repository URLs across documentation:

### Functional URLs (Fork)

URLs for **functional purposes** point to this fork (`costiash/claude-code-docs`):
- **Installation scripts**: Users install from the fork
- **Issue tracking**: Bug reports and feature requests go to the fork
- **GitHub Actions**: CI/CD runs on the fork
- **Pull requests**: Contributions are made to the fork
- **Version badges**: Status indicators link to the fork

**Examples:**
```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
# Issues: https://github.com/costiash/claude-code-docs/issues
# Actions: https://github.com/costiash/claude-code-docs/actions
```

### Attribution URLs (Upstream)

URLs for **attribution and credit** point to upstream (`ericbuess/claude-code-docs`):
- **"Built on" acknowledgments**: Credit to original author
- **"Forked from" references**: Clear lineage documentation
- **Upstream compatibility notes**: Explain relationship to original
- **Upstream contribution guidance**: Direct contributors to original project

**Examples:**
```markdown
This is an enhanced fork of [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)
Built on the excellent foundation of [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)
For upstream contributions, see [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)
```

### Rationale

This dual-URL strategy achieves:
1. **Clear functionality**: Users interact with the fork for installation and support
2. **Proper attribution**: Original author receives credit for foundational work
3. **Upstream compatibility**: Clear path for contributing improvements back to original
4. **Community clarity**: Contributors understand relationship between projects

### When Making Changes

When updating documentation:
- **Use fork URLs** for anything users will click/execute (install, issues, actions)
- **Use upstream URLs** for credit, attribution, and original project references
- **Be consistent**: Follow existing patterns in each document
- **Ask if unsure**: Open a discussion if URL choice is ambiguous

## Branch Strategy

This fork uses a clear branching strategy to maintain independence while allowing clean contributions to upstream:

### Main Branches

- **`main`** - Fork's stable branch with all enhancements
- **`development`** - Active development for fork-specific features
- **`upstream-sync`** - Clean tracking of `upstream/main` for syncing and PRs

### Feature Branches

- **`pr/*`** - Branches for PRs to upstream (clean, upstream-compatible changes only)
- **`feature/*`** - Fork-specific feature development

### Workflow for Upstream PRs

When contributing to upstream ([ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)):

```bash
# 1. Update upstream-sync branch
git checkout upstream-sync
git pull upstream main
git push origin upstream-sync

# 2. Create clean PR branch from upstream-sync
git checkout -b pr/your-feature upstream-sync

# 3. Make ONLY upstream-compatible changes
# - No Python code (unless universally beneficial)
# - No fork-specific features
# - No test artifacts or development tools

# 4. Verify cleanliness
git diff upstream/main --stat
# Should show minimal, focused changes

# 5. Push and create PR
git push origin pr/your-feature
gh pr create --repo ericbuess/claude-code-docs \
  --base main \
  --head costiash:pr/your-feature \
  --title "feat: Your feature"
```

### Workflow for Fork Features

When developing fork-specific features:

```bash
# 1. Create feature branch from development
git checkout development
git pull origin development
git checkout -b feature/your-feature

# 2. Develop and test with comprehensive tests
pytest tests/ -v

# 3. Push and create PR to this fork
git push origin feature/your-feature
gh pr create --repo costiash/claude-code-docs \
  --base main \
  --title "[Enhanced] Your feature"
```

### Syncing with Upstream

Regularly sync the fork with upstream changes:

```bash
# Update upstream-sync
git checkout upstream-sync
git pull upstream main
git push origin upstream-sync

# Merge upstream changes to fork
git checkout main
git merge upstream-sync
# Resolve conflicts (expected in enhanced files)
git push origin main
```

## Getting Started

### Prerequisites

**For all contributors:**
- Git
- Bash
- Basic understanding of Claude Code documentation

**For enhanced features:**
- Python 3.12+
- pip package manager
- Understanding of Python development

### Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/claude-code-docs.git
cd claude-code-docs

# Add upstream remote for syncing
git remote add upstream https://github.com/costiash/claude-code-docs.git
```

## Development Workflows

### For Standard Features (Shell/Git)

**Working on shell scripts, installation, or core functionality:**

```bash
# No Python setup needed
cd claude-code-docs

# Test standard mode installation
./install.sh
# Answer 'N' to enhanced features

# Verify standard commands work
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh -t
~/.claude-code-docs/claude-docs-helper.sh what's new

# Make changes to shell scripts or docs

# Test your changes
~/.claude-code-docs/claude-docs-helper.sh [your-test-command]

# Submit PR (see PR Guidelines below)
```

**What to work on:**
- Installation scripts (`install.sh`, `uninstall.sh`)
- Helper scripts (`scripts/claude-docs-helper.sh.template`)
- GitHub Actions workflows (`.github/workflows/`)
- Core documentation files (`docs/`)
- Shell-based functionality

### For Enhanced Features (Python)

**Working on search, validation, or Python tools:**

```bash
# Clone repository
cd claude-code-docs

# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Test enhanced mode installation
./install.sh
# Answer 'Y' to enhanced features

# Verify enhanced commands work
~/.claude-code-docs/claude-docs-helper.sh --search "mcp"
~/.claude-code-docs/claude-docs-helper.sh --validate

# Make changes to Python scripts

# Run tests (IMPORTANT!)
pytest tests/ -v
pytest --cov=scripts --cov-report=term

# Test your specific changes
python scripts/lookup_paths.py "your test query"
python scripts/main.py --verify

# Submit PR (see PR Guidelines below)
```

**What to work on:**
- Python scripts (`scripts/*.py`)
- Search functionality (`scripts/lookup_paths.py`, `scripts/build_search_index.py`)
- Documentation fetching (`scripts/main.py`)
- Path validation and cleaning
- Test suite (`tests/`)

## Code Standards

### Shell Scripts (Standard Mode)

**Style Guide:**
- Follow upstream's style (see `scripts/claude-docs-helper.sh.template`)
- Use `set -euo pipefail` at the top of all scripts
- Sanitize user inputs to prevent injection
- Comment complex logic clearly
- Use descriptive variable names (UPPERCASE for environment variables)
- Test on both macOS and Linux

**Example:**
```bash
#!/bin/bash
set -euo pipefail

# Claude Code Docs Helper - Standard Mode
# This script handles basic documentation lookups

DOCS_DIR="${HOME}/.claude-code-docs/docs"
TOPIC="${1:-}"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $0 <topic>"
    exit 1
fi

# Sanitize input
TOPIC="$(echo "$TOPIC" | tr -cd '[:alnum:]-_')"

# Rest of implementation...
```

### Python Scripts (Enhanced Mode)

**Style Guide:**
- Python 3.12+ features allowed and encouraged
- Type hints required on all function signatures
- Docstrings required for all public functions (use Google style)
- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use descriptive variable names (lowercase_with_underscores)
- Format with `black` (optional but recommended)

**Example:**
```python
#!/usr/bin/env python3
"""
Path search and validation tool.

This module provides fuzzy search and HTTP validation for Claude documentation paths.
"""

from typing import List, Optional
import json


def search_paths(query: str, limit: int = 20, category: Optional[str] = None) -> List[str]:
    """
    Search for documentation paths matching the query.

    Uses fuzzy matching with Levenshtein distance to find relevant paths.
    Results are ranked by relevance score.

    Args:
        query: Search term (supports partial matches)
        limit: Maximum number of results to return (default: 20)
        category: Optional category filter (e.g., "core_documentation")

    Returns:
        List of matching paths, sorted by relevance score (highest first)

    Raises:
        ValueError: If query is empty or limit is negative

    Example:
        >>> search_paths("prompt engineering", limit=5)
        ['/en/docs/build-with-claude/prompt-engineering/overview', ...]
    """
    if not query:
        raise ValueError("Query cannot be empty")

    if limit < 0:
        raise ValueError("Limit must be non-negative")

    # Implementation...
    results = []
    return results
```

## File Naming Standards

All documentation files in this project follow a **consistent naming convention** for easy organization and URL mapping:

### Format

```
en__section__subsection__page.md
```

### Examples

Documentation URLs map directly to filenames:

| URL Path | Filename |
|----------|----------|
| `/en/docs/claude-code/hooks` | `en__docs__claude-code__hooks.md` |
| `/en/api/overview` | `en__api__overview.md` |
| `/en/docs/build-with-claude/prompt-engineering/overview` | `en__docs__build-with-claude__prompt-engineering__overview.md` |
| `/en/docs/agents-and-tools/mcp` | `en__docs__agents-and-tools__mcp.md` |

### Benefits

- **Flat directory structure** - All files in single `docs/` directory
- **Direct URL↔filename mapping** - Easy to locate files by URL
- **Consistent naming** - No ambiguity in file organization
- **Full-text search compatible** - Easy to search and index
- **Deduplication-friendly** - Prevents accidental duplicate files

### Rules

1. **Always use lowercase** - File names must be lowercase
2. **Use double underscores** - Separate path segments with `__` (not single underscore)
3. **No special characters** - Only alphanumeric, hyphens, and underscores
4. **Keep file extension** - All files are `.md`
5. **Place in docs/ directory** - All documentation files go in `/docs/` directory

### Implementation Note

During Phase 1 (Manifest Cleanup & Deduplication), all 269 documentation files were standardized to follow this naming convention. This ensures consistency across the repository and prevents duplicate content.

## Testing Requirements

### Standard Mode Testing

**Manual testing required:**
- Test on macOS (12+) and Ubuntu (22.04+)
- Verify installation works without Python
- Test all shell script functionality
- Ensure backward compatibility with upstream
- Check that auto-update hooks work

**Test checklist:**
```bash
# Installation
./install.sh  # Answer 'N' to enhanced
~/.claude-code-docs/claude-docs-helper.sh --help

# Core functionality
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh -t
~/.claude-code-docs/claude-docs-helper.sh what's new

# Updates
cd ~/.claude-code-docs && git pull

# Uninstallation
./uninstall.sh
```

### Enhanced Mode Testing

**Automated testing required:**
- All new Python code must have unit tests
- Integration tests for workflows
- Validation tests for external APIs
- **Target: 82%+ code coverage** (currently 81.41%)

**Running tests:**
```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/unit/              # 82 unit tests
pytest tests/integration/       # 36 integration tests
pytest tests/validation/        # 56 validation tests

# Check coverage
pytest --cov=scripts --cov-report=html
pytest --cov=scripts --cov-report=term

# Run specific test file
pytest tests/unit/test_lookup_paths.py -v

# Run with verbose output
pytest -v

# Stop on first failure
pytest -x
```

**Writing tests:**
```python
# tests/unit/test_search.py
import pytest
from scripts.lookup_paths import search_paths


def test_search_paths_basic():
    """Test basic path search functionality."""
    results = search_paths("hooks")
    assert len(results) > 0
    assert any("hooks" in path.lower() for path in results)


def test_search_paths_empty_query():
    """Test that empty query raises ValueError."""
    with pytest.raises(ValueError, match="Query cannot be empty"):
        search_paths("")


def test_search_paths_with_limit():
    """Test limit parameter."""
    results = search_paths("mcp", limit=5)
    assert len(results) <= 5
```

**Current test status:**
- Total: 566 tests
- Passing: 564 tests (99.6% pass rate)
- Skipped: 2 tests (intentional - require development-time artifacts)
- Failing: 0 tests
- Coverage: 81.41% (target: 82%+)

**Skipped tests:**
- `tests/unit/test_manifest_validation.py:45` - Requires `broken_paths_categorized.json` (only created during manifest cleaning)
- `tests/validation/test_link_integrity.py:37` - Requires internal links in sample markdown files

## Pull Request Guidelines

### For Standard Features

**PR Title Format:** `[Standard] Brief description`

**PR Description Template:**
```markdown
## Summary
[Brief description of changes]

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Tested on macOS [version]
- [ ] Tested on Ubuntu [version]
- [ ] Verified backward compatibility
- [ ] Standard mode works without Python

## Related Issues
Fixes #123
```

**Example PR:**
```markdown
[Standard] Fix hook-check race condition

## Summary
Fixes race condition where hook-check could read stale documentation
if git fetch completes after status check.

## Changes Made
- Add mutex to ensure git fetch completes before status check
- Improve error handling in hook-check function
- Add timeout to prevent hanging

## Testing
- [x] Tested on macOS 14.0
- [x] Tested on Ubuntu 22.04
- [x] Verified backward compatibility
- [x] Standard mode works without Python

## Related Issues
Fixes #123
```

### For Enhanced Features

**PR Title Format:** `[Enhanced] Brief description`

**PR Description Template:**
```markdown
## Summary
[Brief description of enhancement]

## Changes Made
- Change 1
- Change 2

## Requirements
- Python 3.12+
- Additional dependencies: [list]

## Testing
- [ ] All tests pass (pytest)
- [ ] Coverage: [percentage]%
- [ ] New tests added: [count] tests
- [ ] Tested enhanced mode installation
- [ ] Standard mode still works

## Documentation
- [ ] Updated ENHANCEMENTS.md
- [ ] Updated relevant examples
- [ ] Added docstrings

## Related Issues
Fixes #456
```

**Example PR:**
```markdown
[Enhanced] Add --search-content for full-text search

## Summary
Adds full-text content search across all documentation, not just path names.
Users can search for keywords within documentation content.

## Changes Made
- Added `build_search_index.py` for indexing documentation content
- Enhanced `lookup_paths.py` with `--search-content` flag
- Added keyword extraction and stop word filtering
- Implemented relevance ranking algorithm

## Requirements
- Python 3.12+
- Additional dependencies: None (uses existing requests library)

## Testing
- [x] All tests pass (pytest)
- [x] Coverage: 92%
- [x] New tests added: 15 tests in tests/unit/test_search_content.py
- [x] Tested enhanced mode installation
- [x] Standard mode still works

## Documentation
- [x] Updated ENHANCEMENTS.md
- [x] Updated EXAMPLES.md with search examples
- [x] Added docstrings to all public functions

## Performance
- Index build time: ~2 seconds for 459 docs
- Search time: < 100ms per query
- Index size: ~45KB

## Related Issues
Fixes #456
```

### Review Process

1. **Automated Checks**: CI/CD runs tests automatically
2. **Code Review**: Maintainer reviews code quality and design
3. **Testing**: Verify functionality on macOS and Linux
4. **Documentation**: Ensure changes are documented
5. **Merge**: Approved PRs are merged to `migration-to-upstream` branch

## Documentation Requirements

**All features must be documented:**

| Feature Type | Documentation Required |
|-------------|----------------------|
| Standard features | Update README.md |
| Enhanced features | Update ENHANCEMENTS.md |
| Usage examples | Add to EXAMPLES.md (if exists) |
| API changes | Update DEVELOPMENT.md |
| New commands | Update command documentation |

**Documentation checklist:**
- [ ] Feature described clearly
- [ ] Usage examples provided
- [ ] Prerequisites listed
- [ ] Troubleshooting section added (if applicable)
- [ ] Links to related documentation

## Release Process

### Standard Releases (Upstream Sync)

**When to release:**
- After syncing with upstream
- No breaking changes to standard mode
- All standard features tested

**Process:**
```bash
# Sync with upstream
git fetch upstream
git merge upstream/main

# Test standard mode
./install.sh  # Answer 'N'
~/.claude-code-docs/claude-docs-helper.sh hooks

# Verify all standard features work
# ... test commands ...

# Tag release
git tag v0.x.x-standard
git push origin v0.x.x-standard

# Update CHANGELOG.md
```

### Enhanced Releases

**When to release:**
- New enhanced features complete
- All tests passing (100%)
- Documentation updated
- Tested on macOS and Linux

**Process:**
```bash
# Ensure tests pass
pytest

# Check coverage
pytest --cov=scripts --cov-report=term

# Update version
# Edit install.sh: ENHANCED_VERSION="0.x.x"

# Update CHANGELOG.md
# Add release notes

# Test both modes
./install.sh  # Test 'N' (standard)
./install.sh  # Test 'Y' (enhanced)

# Verify all features work
# ... test commands ...

# Tag release
git tag v0.x.x-enhanced
git push origin v0.x.x-enhanced
```

## Getting Help

**Questions:**
- Open a [GitHub Discussion](https://github.com/costiash/claude-code-docs/discussions)
- Ask in the discussion thread

**Bug Reports:**
- Open a [GitHub Issue](https://github.com/costiash/claude-code-docs/issues)
- Use the bug report template
- Include: OS version, Python version (if enhanced), steps to reproduce

**Feature Requests:**
- Open a [GitHub Issue](https://github.com/costiash/claude-code-docs/issues)
- Use label: `[Feature Request]`
- Explain: what feature, why it's useful, standard or enhanced mode

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors.

**Expected Behavior:**
- Be respectful and inclusive
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what's best for the project and community
- Show empathy towards others

**Unacceptable Behavior:**
- Harassment, discrimination, or offensive comments
- Trolling, insulting, or derogatory remarks
- Personal or political attacks
- Publishing others' private information
- Any conduct that creates an intimidating environment

**Reporting:**
If you experience or witness unacceptable behavior, please report it to the maintainers.

## License

By contributing, you agree to license your contributions under the same license as this project (MIT License). See [LICENSE](./LICENSE) for details.

## Acknowledgments

This project builds upon:
- [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) - Upstream implementation
- [Anthropic](https://www.anthropic.com/) - Claude Code and documentation

Thank you for contributing to make Claude Code documentation more accessible!

---

**Questions?** Open a Discussion on GitHub or check the [README.md](./README.md) for more information.

**Ready to contribute?** Fork the repository and start coding!
