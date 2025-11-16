# Contributing Guidelines

Thank you for contributing to the Enhanced Claude Code Documentation Mirror!

## Project Philosophy

This project extends [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) with optional Python features:

**Core Principle: Graceful Degradation**
- Single installation (always 268 files + Python scripts)
- Python features activate only when Python 3.9+ is available
- Everything works without Python (basic `/docs` command)
- No separate "modes" - just feature detection at runtime

**Design Goals:**
1. **Honesty**: Accurate claims about what we deliver (270 paths, not 449)
2. **Simplicity**: One installation, automatic feature detection
3. **Compatibility**: Works with upstream, same `/docs` interface
4. **Testing**: High test coverage (78%), all changes tested

## Repository URL Strategy

This project uses clear URL conventions:

### Functional URLs (This Fork)
For **functional purposes**, use `costiash/claude-code-docs`:
- Installation scripts
- Issue tracking and bug reports
- GitHub Actions / CI/CD
- Pull requests
- Status badges

**Examples:**
```bash
# Installation
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash

# Issues
https://github.com/costiash/claude-code-docs/issues

# Actions
https://github.com/costiash/claude-code-docs/actions
```

### Attribution URLs (Upstream)
For **attribution and credit**, use `ericbuess/claude-code-docs`:
- "Built on" acknowledgments
- "Forked from" references
- Upstream compatibility notes
- Contribution guidance to original project

**Examples:**
```markdown
Built on [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)
For upstream contributions, see [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs)
```

## Getting Started

### Prerequisites

**Required for all contributors:**
- Git
- Bash
- Basic understanding of Claude Code

**For Python features:**
- Python 3.9+
- pip package manager

### Fork and Clone

```bash
# Fork on GitHub, then:
git clone https://github.com/YOUR_USERNAME/claude-code-docs.git
cd claude-code-docs

# Add upstream remote
git remote add upstream https://github.com/costiash/claude-code-docs.git
```

## Development Workflows

### For Shell Scripts

Working on installation, helper scripts, or core functionality:

```bash
# No Python setup needed
cd claude-code-docs

# Test installation
./install.sh

# Test basic commands
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh -t
~/.claude-code-docs/claude-docs-helper.sh what's new

# Test uninstall
./uninstall.sh
```

**Files to work on:**
- `install.sh` - Installation script
- `uninstall.sh` - Removal script
- `scripts/claude-docs-helper.sh` - Main entry point
- `.github/workflows/` - GitHub Actions
- `docs/` - Documentation files

### For Python Features

Working on search, validation, or Python tools:

```bash
# Setup Python virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Test Python commands
~/.claude-code-docs/claude-docs-helper.sh --search "mcp"
~/.claude-code-docs/claude-docs-helper.sh --validate

# Run tests (REQUIRED before submitting PR)
pytest tests/ -v  # Should see: 598 passed, 2 skipped
pytest --cov=scripts --cov-report=term  # Should see: ~78%

# Test specific changes
python scripts/lookup_paths.py "your test query"
python scripts/fetch_claude_docs.py --help
```

**Files to work on:**
- `scripts/fetch_claude_docs.py` - Documentation fetcher with auto-regeneration
- `scripts/lookup_paths.py` - Search & validation
- `scripts/build_search_index.py` - Full-text search indexing
- `tests/` - Test suite (600 tests)

## Code Standards

### Shell Scripts

**Style Guide:**
- Use `set -euo pipefail` at top
- Sanitize ALL user inputs (alphanumeric + safe chars only)
- Comment complex logic
- UPPERCASE for environment variables
- Test on both macOS and Linux

**Example:**
```bash
#!/bin/bash
set -euo pipefail

# Claude Code Docs Helper
# Handles documentation lookups with feature detection

DOCS_DIR="${HOME}/.claude-code-docs/docs"
TOPIC="${1:-}"

# Sanitize input to prevent injection
TOPIC="$(echo "$TOPIC" | tr -cd '[:alnum:]-_')"

if [[ -z "$TOPIC" ]]; then
    echo "Usage: $0 <topic>"
    exit 1
fi

# Implementation...
```

### Python Scripts

**Style Guide:**
- Python 3.9+ features encouraged
- Type hints required on all function signatures
- Docstrings required (Google style)
- Follow PEP 8 (max line length: 100 chars)
- Descriptive variable names (lowercase_with_underscores)
- Format with `black` (optional but recommended)

**Example:**
```python
#!/usr/bin/env python3
"""
Path search and validation tool.

Provides fuzzy search and HTTP validation for Claude documentation paths.
"""

from typing import List, Optional
import json


def search_paths(query: str, limit: int = 20, category: Optional[str] = None) -> List[str]:
    """
    Search for documentation paths matching the query.

    Uses fuzzy matching with Levenshtein distance for relevance ranking.

    Args:
        query: Search term (supports partial matches)
        limit: Maximum results to return (default: 20)
        category: Optional category filter (e.g., "core_documentation")

    Returns:
        List of matching paths, sorted by relevance score

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
    return []
```

## File Naming Standards

All documentation files follow a consistent naming convention:

### Format

```
en__section__subsection__page.md
# OR (for Claude Code docs)
docs__en__page.md
```

### Examples

| URL Path | Filename |
|----------|----------|
| `/en/docs/claude-code/hooks` | `en__docs__claude-code__hooks.md` |
| `/docs/en/hooks` | `docs__en__hooks.md` |
| `/en/api/overview` | `en__api__overview.md` |

### Rules

1. **Lowercase only**
2. **Double underscores** for path separators
3. **No special characters** except alphanumeric, hyphens, underscores
4. **Keep `.md` extension**
5. **Place in `docs/` directory**

## Testing Requirements

### Manual Testing (Shell Scripts)

Test on both macOS and Linux:

```bash
# Installation
./install.sh
~/.claude-code-docs/claude-docs-helper.sh --help

# Core functionality
~/.claude-code-docs/claude-docs-helper.sh hooks
~/.claude-code-docs/claude-docs-helper.sh -t
~/.claude-code-docs/claude-docs-helper.sh what's new

# Updates
cd ~/.claude-code-docs && git pull

# Uninstall
./uninstall.sh
```

### Automated Testing (Python Features)

**All new Python code must have unit tests.**

**Running tests:**
```bash
# Run all tests
pytest

# Run specific test suites
pytest tests/unit/              # 82 unit tests
pytest tests/integration/       # 36 integration tests
pytest tests/validation/        # 56 validation tests

# Check coverage (target: 78%+)
pytest --cov=scripts --cov-report=html
pytest --cov=scripts --cov-report=term

# Run specific test file
pytest tests/unit/test_lookup_paths.py -v

# Verbose output
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
- Total: 600 tests
- Passing: 598 (99.7%)
- Skipped: 2 (intentional)
- Coverage: 78.32%

## Pull Request Guidelines

### PR Title Format

```
[scope] Brief description

Examples:
[fix] Update outdated path counts in helper script
[feat] Add full-text content search
[docs] Clarify installation methods in README
[test] Add tests for auto-regeneration feature
```

### PR Description Template

```markdown
## Summary
[Brief description of changes]

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] All tests pass (pytest)
- [ ] Coverage maintained or improved
- [ ] Manual testing completed
- [ ] Works without Python (if touching shell scripts)
- [ ] Works with Python 3.9+ (if touching Python code)

## Documentation
- [ ] Updated relevant docs (README, CLAUDE.md, etc.)
- [ ] Added docstrings to new functions
- [ ] Updated examples if needed

## Related Issues
Fixes #123
```

### Review Process

1. **Automated Checks**: CI/CD runs tests automatically
2. **Code Review**: Maintainer reviews code quality
3. **Testing**: Functionality verified on macOS and Linux
4. **Documentation**: Changes must be documented
5. **Merge**: Approved PRs merged to main branch

## Documentation Requirements

| Feature Type | Documentation Required |
|-------------|----------------------|
| Shell scripts | Update README.md |
| Python features | Update docstrings + README.md |
| New commands | Update command documentation |
| Architecture changes | Update CLAUDE.md |

## Release Process

### Standard Releases

**When to release:**
- Bug fixes merged
- Documentation updates
- No breaking changes

**Process:**
```bash
# Update version in install.sh
# Update CHANGELOG.md

# Tag release
git tag v0.x.x
git push origin v0.x.x
```

### Feature Releases

**When to release:**
- New Python features complete
- All tests passing (600/600 or 598/600)
- Documentation updated

**Process:**
```bash
# Ensure tests pass
pytest

# Check coverage
pytest --cov=scripts --cov-report=term  # Should be ~78%

# Update versions
# Edit install.sh, README.md

# Test both basic and Python features
./install.sh
pytest tests/ -v

# Tag release
git tag v0.x.x-feature
git push origin v0.x.x-feature
```

## Getting Help

**Questions:**
- [GitHub Discussions](https://github.com/costiash/claude-code-docs/discussions)

**Bug Reports:**
- [GitHub Issues](https://github.com/costiash/claude-code-docs/issues)
- Use bug report template
- Include: OS, Python version, reproduction steps

**Feature Requests:**
- [GitHub Issues](https://github.com/costiash/claude-code-docs/issues)
- Label: `[Feature Request]`
- Explain: what, why, and which features (shell or Python)

## Code of Conduct

**Expected Behavior:**
- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism gracefully
- Focus on what's best for the project
- Show empathy

**Unacceptable Behavior:**
- Harassment or discrimination
- Trolling or derogatory remarks
- Personal attacks
- Publishing others' private information

**Reporting:**
Report to maintainers via GitHub Issues or email.

## License

By contributing, you agree to license your contributions under the MIT License. See [LICENSE](./LICENSE) for details.

## Acknowledgments

- [ericbuess/claude-code-docs](https://github.com/ericbuess/claude-code-docs) - Original implementation
- [Anthropic](https://www.anthropic.com/) - Claude Code and documentation

---

**Ready to contribute?** Fork the repository and start coding! We're excited to see your contributions.
