# Development Guide

Complete guide for contributors to the Claude Code Documentation Mirror project.

## Table of Contents

- [Setup for Contributors](#setup-for-contributors)
- [Code Structure](#code-structure)
- [Testing Guidelines](#testing-guidelines)
- [Code Style](#code-style)
- [Release Process](#release-process)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)
- [Resources](#resources)

## Setup for Contributors

### 1. Clone and Setup

```bash
# Fork the repository on GitHub first, then:
git clone https://github.com/YOUR_USERNAME/claude-code-docs.git
cd claude-code-docs

# Add upstream remote for tracking
git remote add upstream https://github.com/costiash/claude-code-docs.git

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### 2. Verify Installation

```bash
# Check Python version
python --version  # Should be 3.12+

# Run tests
pytest

# Try scripts
python scripts/lookup_paths.py --help
python scripts/main.py --help
```

### 3. Install Pre-commit Hooks (Recommended)

```bash
pip install pre-commit
pre-commit install
```

This will automatically check code style before each commit.

## Code Structure

### Main Scripts

#### `scripts/main.py` (662 lines)

**Purpose**: Enhanced documentation fetcher with direct markdown fetch

**Key Functions**:

```python
def fetch_page(url: str, session: requests.Session) -> str:
    """
    Fetch markdown content from URL with retry logic.

    Features:
    - Direct markdown fetching (no HTML parsing)
    - Exponential backoff retry (3 attempts)
    - Proper error handling
    - Rate limiting (0.5s between requests)
    """

def content_has_changed(path: str, new_content: str, manifest: dict) -> bool:
    """
    SHA256-based change detection.

    Only re-fetches pages that have actually changed,
    saving bandwidth and processing time.
    """

def save_documentation(path: str, content: str, output_dir: Path):
    """
    Save documentation with proper directory structure.

    Creates nested directories as needed.
    """

def update_documentation(paths: list, output_dir: Path, force: bool = False):
    """
    Main orchestration function.

    Features:
    - Progress tracking with tqdm
    - Parallel processing option (future)
    - Comprehensive error reporting
    - Statistics and summary
    """
```

**CLI Arguments**:
- `--update-all`: Fetch all 459 paths
- `--update-category <cat>`: Update specific category
- `--force`: Force re-fetch (ignore cache)
- `--verify`: Verify existing documentation
- `--log-level <level>`: Set logging level

#### `scripts/extract_paths.py` (534 lines)

**Purpose**: Path extraction and cleaning with categorization

**Key Functions**:

```python
def clean_path(path: str) -> str:
    """
    Remove trailing backslashes, whitespace, and artifacts.

    Handles:
    - Backslash escaping artifacts
    - Whitespace normalization
    - Special character filtering
    """

def is_valid_path(path: str) -> bool:
    """
    Validate path against rules.

    Rules:
    - Must start with /en/
    - No :slug* patterns
    - Minimum length requirement
    - Valid characters only
    """

def categorize_path(path: str) -> str:
    """
    Assign category based on path prefix.

    Categories:
    - core_documentation: /en/docs/ (excluding claude-code)
    - api_reference: /en/api/
    - claude_code: /en/docs/claude-code/
    - prompt_library: /en/prompt-library/
    - resources: /en/resources/
    - release_notes: /en/release-notes/
    - uncategorized: fallback
    """

def export_manifest(paths_by_category: dict, output_path: Path):
    """
    Export to paths_manifest.json with metadata.

    Format:
    {
      "metadata": {...},
      "categories": {
        "core_documentation": [...],
        ...
      }
    }
    """
```

**CLI Arguments**:
- `--source <file>`: Input HTML file (default: temp.html)
- `--output <file>`: Output JSON file (default: paths_manifest.json)
- `--stats`: Show statistics only
- `--validate`: Validate paths only

#### `scripts/lookup_paths.py` (597 lines)

**Purpose**: Path search and validation utility

**Key Functions**:

```python
def search_paths(query: str, paths: list) -> list:
    """
    Fuzzy search with relevance ranking.

    Features:
    - Case-insensitive matching
    - Substring matching
    - Relevance scoring (0-100)
    - Category filtering
    """

def validate_path(path: str) -> dict:
    """
    Check URL reachability (HTTP status).

    Returns:
    {
      "path": str,
      "reachable": bool,
      "status_code": int,
      "error": str or None
    }
    """

def batch_validate(paths: list) -> dict:
    """
    Validate multiple paths in parallel.

    Features:
    - ThreadPoolExecutor for parallelism
    - Progress bar
    - Summary statistics
    """

def suggest_alternatives(path: str, all_paths: list) -> list:
    """
    Find similar paths for broken links.

    Uses fuzzy matching to suggest valid alternatives.
    """
```

**CLI Arguments**:
- `<query>`: Search query (fuzzy match)
- `--validate-all`: Validate all 459 paths
- `--check <path>`: Check specific path
- `--batch-validate <file>`: Validate paths from file

#### `scripts/update_sitemap.py` (504 lines)

**Purpose**: Sitemap and search index generation

**Key Functions**:

```python
def generate_hierarchical_tree(paths: list) -> dict:
    """
    Build hierarchical tree structure from flat paths.

    Example:
    /en/docs/vision → {en: {docs: {vision: {}}}}
    """

def generate_search_index(paths: list) -> dict:
    """
    Create optimized search index.

    Includes:
    - Path list
    - Keywords
    - Categories
    - Fast lookup table
    """

def generate_sitemap(manifest_path: Path, output_dir: Path):
    """
    Generate docs/sitemap.json and docs/.search_index.json.

    Compatible with upstream format.
    """
```

### Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures (14 fixtures)
├── fixtures/                # Test data
│   ├── sample.html          # Sample documentation page
│   ├── sample_paths.txt     # Sample path list
│   ├── invalid_paths.txt    # Known broken paths
│   └── expected_output.md   # Expected markdown output
├── unit/                    # Unit tests (82 tests)
│   ├── test_path_extraction.py      # Path cleaning and validation
│   ├── test_url_validation.py       # URL format and validation
│   ├── test_file_operations.py      # File read/write
│   └── test_categorization.py       # Category assignment
├── integration/             # Integration tests (36 tests)
│   ├── test_full_workflow.py        # Complete fetch-save pipeline
│   ├── test_update_detection.py     # Change tracking
│   └── test_github_actions.py       # Workflow simulation
└── validation/              # Validation tests (56 tests)
    ├── test_path_reachability.py    # URL accessibility
    ├── test_content_validity.py     # Content quality
    ├── test_link_integrity.py       # Internal link checking
    └── test_sitemap_consistency.py  # Sitemap vs files
```

### Key Fixtures (conftest.py)

```python
@pytest.fixture
def sample_html():
    """Sample HTML for testing"""
    return Path('tests/fixtures/sample.html').read_text()

@pytest.fixture
def sample_paths():
    """Sample paths for testing"""
    return [
        '/en/docs/build-with-claude',
        '/en/api/overview',
        '/en/prompt-library/code-consultant'
    ]

@pytest.fixture
def mock_http_response(monkeypatch):
    """Mock HTTP requests"""
    # ... mocking logic

@pytest.fixture
def temp_docs_dir(tmp_path):
    """Temporary directory for file operations"""
    return tmp_path / "docs"
```

## Testing Guidelines

### Running Tests

```bash
# All tests (174 total)
pytest

# Specific suite
pytest tests/unit/              # 82 unit tests
pytest tests/integration/       # 36 integration tests
pytest tests/validation/        # 56 validation tests

# Specific file
pytest tests/unit/test_path_extraction.py

# Specific test
pytest tests/unit/test_path_extraction.py::test_clean_trailing_backslashes

# With coverage
pytest --cov=scripts --cov-report=html
pytest --cov=scripts --cov-report=term

# Verbose output
pytest -v

# Stop on first failure
pytest -x

# Run only fast tests (skip slow ones)
pytest -m "not slow"

# Run only network tests
pytest -m network
```

### Writing Tests

#### Unit Test Example

```python
# tests/unit/test_path_extraction.py

def test_clean_trailing_backslashes():
    """Test removal of backslash artifacts"""
    from scripts.extract_paths import clean_path

    # Arrange
    path = "/en/docs/build-with-claude\\"

    # Act
    result = clean_path(path)

    # Assert
    assert result == "/en/docs/build-with-claude"
    assert "\\" not in result
```

#### Integration Test Example

```python
# tests/integration/test_full_workflow.py

def test_full_pipeline(tmp_path, mock_http_response):
    """Test complete fetch-process-save workflow"""
    from scripts.main import update_documentation

    # Arrange
    paths = ["/en/docs/test-page"]
    output_dir = tmp_path / "docs"

    # Act
    result = update_documentation(paths, output_dir=output_dir)

    # Assert
    assert result['success_count'] == 1
    assert (output_dir / "en/docs/test-page.md").exists()
```

#### Validation Test Example

```python
# tests/validation/test_path_reachability.py

@pytest.mark.network
def test_path_reachable():
    """Test that path returns HTTP 200"""
    from scripts.lookup_paths import validate_path

    # Act
    result = validate_path("/en/docs/overview")

    # Assert
    assert result['reachable'] is True
    assert result['status_code'] == 200
```

### Test Coverage Requirements

- **Minimum coverage**: 85%
- **Current coverage**: 24%
- **Critical paths**: 100% (must test fetch, parse, save)
- **Edge cases**: Must test error conditions

### Coverage Targets by Module

| Module | Current | Target | Priority |
|--------|---------|--------|----------|
| main.py | 30% | 90% | HIGH |
| extract_paths.py | 45% | 85% | MEDIUM |
| lookup_paths.py | 20% | 85% | HIGH |
| update_sitemap.py | 15% | 80% | MEDIUM |

### Mocking External Dependencies

Always mock HTTP requests in tests:

```python
@pytest.fixture
def mock_http_response(monkeypatch):
    """Mock requests.get() to avoid actual network calls"""
    import requests

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = "<html>Test content</html>"

            def raise_for_status(self):
                pass

        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
```

## Code Style

### Python Style Guide

Follow **PEP 8** with these specifics:

- **Maximum line length**: 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Double quotes for strings, single for dict keys
- **Type hints**: Required for all public functions
- **Docstrings**: Required for all public functions (Google style)

### Type Hints

All public functions must have type hints:

```python
def fetch_page(url: str, timeout: int = 30) -> str:
    """
    Fetch HTML content from a URL.

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds (default: 30)

    Returns:
        HTML content as string

    Raises:
        requests.RequestException: If request fails after retries
    """
    # Implementation
```

### Docstrings

Use Google-style docstrings:

```python
def categorize_path(path: str) -> str:
    """
    Assign category based on path prefix.

    Categories are determined by path structure:
    - /en/docs/ (non-claude-code) → core_documentation
    - /en/api/ → api_reference
    - /en/docs/claude-code/ → claude_code
    - /en/prompt-library/ → prompt_library

    Args:
        path: Documentation path (e.g., "/en/docs/overview")

    Returns:
        Category name as string (e.g., "core_documentation")

    Example:
        >>> categorize_path("/en/docs/build-with-claude/vision")
        'core_documentation'
    """
    # Implementation
```

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

### Linting and Formatting

```bash
# Format code (automatic)
black scripts/ tests/

# Sort imports
isort scripts/ tests/

# Lint (check only)
flake8 scripts/ tests/
pylint scripts/

# Type checking
mypy scripts/
```

### Pre-commit Configuration

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.0.0
    hooks:
      - id: black
        language_version: python3.12

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Release Process

### 1. Version Bump

Update version in `pyproject.toml`:

```toml
[project]
version = "0.2.0"
```

### 2. Update Changelog

Add entry to `CHANGELOG.md`:

```markdown
## [0.2.0] - 2025-11-10

### Added
- Feature X: Description
- Feature Y: Description

### Changed
- Improvement Z: Description

### Fixed
- Bug fix W: Description

### Deprecated
- Feature V: Reason
```

### 3. Create Git Tag

```bash
# Commit changes
git add pyproject.toml CHANGELOG.md
git commit -m "chore: Bump version to 0.2.0"

# Create tag
git tag -a v0.2.0 -m "Release v0.2.0"

# Push
git push origin development
git push origin v0.2.0
```

### 4. Create GitHub Release

GitHub Actions will automatically create a release from the tag.

Alternatively, create manually:

```bash
# Using gh CLI
gh release create v0.2.0 --title "Release v0.2.0" --notes "See CHANGELOG.md"
```

### 5. Merge to Main

```bash
# Switch to main
git checkout main

# Merge development
git merge development

# Push
git push origin main
```

## Common Tasks

### Adding a New Path Category

1. **Update `extract_paths.py`**:

```python
def categorize_path(path: str) -> str:
    """Assign category based on path prefix"""
    if path.startswith("/en/docs/new-category/"):
        return "new_category"
    # ... existing categories
```

2. **Add tests**:

```python
# tests/unit/test_categorization.py
def test_new_category():
    """Test new category assignment"""
    from scripts.extract_paths import categorize_path

    path = "/en/docs/new-category/page"
    assert categorize_path(path) == "new_category"
```

3. **Update documentation**:
   - README.md (category list)
   - CAPABILITIES.md (category description)
   - paths_manifest.json (regenerate)

4. **Regenerate manifest**:

```bash
python scripts/extract_paths.py --source temp.html --output paths_manifest.json
```

### Adding a New Script

1. **Create script** in `scripts/`:

```python
#!/usr/bin/env python3
"""
New script description.
"""

import argparse
from pathlib import Path

def main():
    """Entry point"""
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--option", help="Option description")
    args = parser.parse_args()

    # Implementation

if __name__ == "__main__":
    main()
```

2. **Add to `pyproject.toml`** (optional):

```toml
[project.scripts]
new-script = "scripts.new_script:main"
```

3. **Write tests**:

```python
# tests/unit/test_new_script.py
def test_new_script_function():
    """Test new script functionality"""
    # Test implementation
```

4. **Document**:
   - README.md (usage section)
   - DEVELOPMENT.md (this file)
   - CAPABILITIES.md (if user-facing)

### Debugging

```bash
# Run with debug logging
python scripts/main.py --update-all --log-level DEBUG

# Use pytest debugging
pytest --pdb  # Drop into debugger on failure

# Profile performance
python -m cProfile -o profile.stats scripts/main.py --update-all

# Analyze profile
python -m pstats profile.stats
>>> sort cumtime
>>> stats 20
```

### Running GitHub Actions Locally

Use `act` tool:

```bash
# Install act
brew install act  # macOS
# or download from https://github.com/nektos/act

# List workflows
act -l

# Run workflow
act push  # Simulates push event

# Run specific job
act -j test
```

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError

**Problem**: Cannot import scripts modules

**Solution**:
```bash
# Install in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### 2. Tests Failing with Function Signature Mismatches

**Problem**: Tests expect different function signatures than actual implementation

**Current Status**: 24 tests failing due to this

**Solution**:
```bash
# Check actual function signature
python -c "from scripts.main import fetch_page; help(fetch_page)"

# Update test to match
# Example: fetch_page requires session parameter
def test_fetch_page(mock_session):
    result = fetch_page(url, session=mock_session)
```

#### 3. Coverage Below 85%

**Problem**: Code coverage is only 24%

**Solution**:
```bash
# Find uncovered lines
pytest --cov=scripts --cov-report=term-missing

# Add tests for uncovered code
# Focus on:
# - Error handling paths
# - Edge cases
# - Helper functions
```

#### 4. Rate Limiting Errors

**Problem**: Getting HTTP 429 errors during fetch

**Solution**:
```python
# Increase delay in scripts/main.py
RATE_LIMIT_DELAY = 1.0  # Increase from 0.5 to 1.0
```

#### 5. Import Errors in Tests

**Problem**: Tests can't find scripts modules

**Solution**:
```bash
# Ensure pytest is finding scripts
pytest --collect-only

# If not, add to conftest.py:
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
```

### Getting Help

- **Project Issues**: https://github.com/costiash/claude-code-docs/issues
- **Discussions**: https://github.com/costiash/claude-code-docs/discussions
- **Documentation**: See [README.md](./README.md)
- **Implementation Plan**: See [specs/IMPLEMENTATION_PLAN.md](./specs/IMPLEMENTATION_PLAN.md)

## Resources

### Python

- [Python 3.12 Documentation](https://docs.python.org/3.12/)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Testing

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-cov Plugin](https://pytest-cov.readthedocs.io/)
- [Mocking with pytest-mock](https://pytest-mock.readthedocs.io/)

### GitHub Actions

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [Testing Actions Locally (act)](https://github.com/nektos/act)

### Anthropic

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code/)
- [Model Context Protocol](https://docs.anthropic.com/en/docs/mcp/)

### Tools

- [Black (Formatter)](https://black.readthedocs.io/)
- [isort (Import Sorter)](https://pycqa.github.io/isort/)
- [flake8 (Linter)](https://flake8.pycqa.org/)
- [mypy (Type Checker)](http://mypy-lang.org/)

---

**Last Updated**: 2025-11-03

**Questions?** Open an issue or discussion on GitHub!
