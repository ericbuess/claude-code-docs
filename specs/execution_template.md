# Execution Template - Phase-by-Phase Implementation Guide

**Purpose**: This document provides complete template prompts for executing each phase of the implementation plan using the Task tool with the general-purpose agent.

**Critical Guidelines**:
1. ✅ **ALWAYS use the Task tool** to invoke the general-purpose agent for each phase
2. ✅ **Provide complete context** from IMPLEMENTATION_PLAN.md for the phase
3. ✅ **After completion**, the agent MUST mark checkboxes in IMPLEMENTATIONMONITOR.md
4. ✅ **Test thoroughly** before marking phase as complete
5. ✅ **Document issues** encountered in the monitor file

---

## Table of Contents
- [Phase 1: Repository Setup & Analysis](#phase-1-repository-setup--analysis)
- [Phase 2: Path Extraction & Cleaning](#phase-2-path-extraction--cleaning)
- [Phase 3: Script Development](#phase-3-script-development)
- [Phase 4: Integration & Adaptation](#phase-4-integration--adaptation)
- [Phase 5: Comprehensive Testing Suite](#phase-5-comprehensive-testing-suite)
- [Phase 6: Documentation & Guidelines](#phase-6-documentation--guidelines)
- [Phase 7: Validation & Quality Assurance](#phase-7-validation--quality-assurance)

---

## How to Use This Template

### Step 1: Prepare the Prompt
Copy the template prompt for the phase you want to execute.

### Step 2: Invoke the Task Tool
Use the Task tool with subagent_type="general-purpose" and paste the prompt.

### Step 3: Monitor Progress
The agent will execute all tasks in the phase and provide updates.

### Step 4: Verify Completion
Check that all deliverables were created and all tasks completed.

### Step 5: Update Monitor
The agent will mark checkboxes in IMPLEMENTATIONMONITOR.md upon completion.

---

## Phase 1: Repository Setup & Analysis

### Template Prompt for Task Tool

```
PHASE 1: REPOSITORY SETUP & ANALYSIS

**Context**:
I am implementing Phase 1 of the Claude Code Documentation Mirror project. This phase involves cloning and analyzing the costiash/claude-code-docs repository to understand their implementation approach.

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 1 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 4 tasks of Phase 1, which includes:
1. Cloning the upstream repository
2. Analyzing repository structure
3. Analyzing fetching mechanism
4. Mapping directory structure

**Detailed Tasks**:

TASK 1.1 - Clone Upstream Repository:
- Clone https://github.com/costiash/claude-code-docs.git to ./upstream/
- Add as git remote named "upstream"
- Verify the clone was successful
- Document any issues encountered

Commands to run:
```bash
cd /home/rudycosta3/claude-code-docs
git clone https://github.com/costiash/claude-code-docs.git ./upstream/
git remote add upstream https://github.com/costiash/claude-code-docs.git
git fetch upstream
ls -la ./upstream/
```

TASK 1.2 - Analyze Repository Structure:
- Examine directory layout using ls and tree
- Identify key directories: /docs, /scripts, /.github/workflows/, /.claude/
- Document the structure in ./analysis/repo_structure.md
- Include directory tree, file counts, and purpose of each directory

Create: ./analysis/repo_structure.md with:
- Directory tree visualization
- Description of each major directory
- File organization patterns
- Key files and their purposes

TASK 1.3 - Analyze Fetching Mechanism:
- Read all scripts in ./upstream/scripts/
- Identify:
  * Base URL patterns for fetching documentation
  * HTTP headers and authentication methods
  * HTML parsing approach and libraries used
  * Markdown conversion method
  * Error handling strategy
  * Rate limiting implementation
- Document findings in ./analysis/fetch_mechanism.md

Create: ./analysis/fetch_mechanism.md with:
- Script inventory and purposes
- URL construction method
- HTML-to-Markdown conversion approach
- Error handling patterns
- Rate limiting strategy
- Dependencies and libraries used

TASK 1.4 - Map Directory Structure:
- Understand how paths like /en/docs/build-with-claude become file paths
- Study their naming conventions
- Review .claude/commands/ integration
- Document the mapping rules in ./analysis/path_mapping.md

Create: ./analysis/path_mapping.md with:
- Path-to-file mapping rules
- Naming convention examples
- Directory hierarchy strategy
- .claude/ integration details

**Success Criteria**:
- [ ] ./upstream/ directory contains cloned repository
- [ ] Git remote "upstream" is configured
- [ ] ./analysis/repo_structure.md created and comprehensive
- [ ] ./analysis/fetch_mechanism.md created with implementation details
- [ ] ./analysis/path_mapping.md created with mapping rules
- [ ] All 4 tasks completed successfully

**After Completion - CRITICAL**:
You MUST update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:
1. Mark all Task 1.1, 1.2, 1.3, 1.4 checkboxes as completed [x]
2. Check all Phase 1 Deliverables Checklist items [x]
3. Mark "Phase 1 Complete" checkbox [x]
4. Fill in completion date, actual duration, and any issues encountered
5. Update overall project status (completed tasks count, progress percentage)

**Reporting**:
Provide a summary report including:
- What was accomplished
- Key findings from the analysis
- Any issues or blockers encountered
- Confirmation that IMPLEMENTATIONMONITOR.md was updated
- Readiness for Phase 2
```

---

## Phase 2: Path Extraction & Cleaning

### Template Prompt for Task Tool

```
PHASE 2: PATH EXTRACTION & CLEANING

**Context**:
I am implementing Phase 2 of the Claude Code Documentation Mirror project. This phase involves enhancing the path extraction script and generating statistics about the documentation paths.

**Prerequisites**:
- Phase 1 must be completed
- Verify: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md shows Phase 1 complete

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 2 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md
- Current extracted_paths.txt: /home/rudycosta3/claude-code-docs/extracted_paths.txt
- Source HTML: /home/rudycosta3/claude-code-docs/temp.html

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 2 tasks of Phase 2:
1. Enhance extract_paths.py with cleaning and categorization
2. Generate statistics and comparison report

**Detailed Tasks**:

TASK 2.1 - Enhance extract_paths.py:

Read the current extract_paths.py and understand its functionality.

Add the following functions:

```python
def clean_path(path: str) -> str:
    """
    Remove trailing backslashes, whitespace, and artifacts.

    Args:
        path: Raw path string

    Returns:
        Cleaned path string
    """
    # Implementation:
    # - Strip whitespace
    # - Remove trailing backslashes
    # - Remove artifacts like ),
    # - Normalize slashes

def is_valid_path(path: str) -> bool:
    """
    Validate if path is a real documentation path.

    Args:
        path: Path to validate

    Returns:
        True if valid, False if noise pattern
    """
    # Filter out:
    # - :slug* patterns
    # - Paths with invalid characters
    # - Empty or malformed paths

def categorize_path(path: str) -> str:
    """
    Assign category based on path prefix.

    Args:
        path: Documentation path

    Returns:
        Category name (core_documentation, api_reference, etc.)
    """
    # Categories:
    # - /en/docs/ (but not claude-code) → "core_documentation"
    # - /en/api/ → "api_reference"
    # - /en/docs/claude-code/ → "claude_code"
    # - /en/prompt-library/ → "prompt_library"
    # - /en/resources/ → "resources"
    # - /en/release-notes/ → "release_notes"

def extract_fragment(path: str) -> tuple[str, str]:
    """
    Separate URL path from fragment identifier.

    Args:
        path: Full path with possible fragment

    Returns:
        Tuple of (path, fragment)
    """
    # Split on # character
    # Return path and fragment separately

def export_manifest(paths: dict, output_file: str):
    """
    Export categorized paths to JSON manifest.

    Args:
        paths: Dictionary with categories and paths
        output_file: Path to output JSON file
    """
    # Create JSON structure:
    # {
    #   "metadata": {
    #     "generated_at": timestamp,
    #     "total_paths": count,
    #     "source": "temp.html"
    #   },
    #   "categories": {
    #     "core_documentation": [...],
    #     "api_reference": [...],
    #     etc.
    #   }
    # }
```

Update the main extraction logic to:
1. Read temp.html
2. Extract all paths matching /en/ pattern
3. Clean each path using clean_path()
4. Validate using is_valid_path()
5. Remove duplicates
6. Categorize each path
7. Sort within categories
8. Export to:
   - extracted_paths_clean.txt (one path per line)
   - paths_manifest.json (structured with categories)

Add CLI arguments:
- --source: Input HTML file (default: temp.html)
- --output: Output JSON file (default: paths_manifest.json)
- --validate: Validate paths only (don't re-extract)
- --stats: Show statistics only

Test the enhanced script:
```bash
python extract_paths.py --source temp.html --output paths_manifest.json
python extract_paths.py --stats
python extract_paths.py --validate
```

TASK 2.2 - Generate Statistics:

Create ./analysis/sitemap_statistics.md with:

1. **Overview Statistics**:
   - Total unique paths found
   - Breakdown by category (count and percentage)
   - Duplicates removed
   - Invalid paths filtered

2. **Category Analysis**:
   For each category:
   - Path count
   - Most common subdirectories
   - Depth distribution
   - Notable patterns

3. **Comparison with Navigation**:
   - Paths visible in navigation vs total
   - Hidden/direct-access paths
   - Deprecated paths identified

4. **Quality Metrics**:
   - Clean paths ratio
   - Validation success rate
   - Category distribution health

5. **Recommendations**:
   - Paths to exclude (deprecated)
   - Priority paths for initial fetch
   - Potential issues identified

Generate the report using data from paths_manifest.json.

**Expected Outputs**:
- Enhanced extract_paths.py (~200-300 lines)
- extracted_paths_clean.txt (~550 paths, one per line)
- paths_manifest.json (structured JSON with all categories)
- ./analysis/sitemap_statistics.md (comprehensive statistics)

**Validation Criteria**:
- [ ] Total unique paths ≈ 550
- [ ] All 4 required categories present (core_documentation, api_reference, claude_code, prompt_library)
- [ ] No trailing backslashes in cleaned paths
- [ ] No :slug* or artifact patterns remain
- [ ] JSON manifest is valid and well-structured
- [ ] Statistics show expected distribution:
  * Core documentation: ~50%
  * API reference: ~17%
  * Claude Code: ~13%
  * Prompt library: ~19%

**After Completion - CRITICAL**:
Update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:
1. Mark Task 2.1 and 2.2 checkboxes [x]
2. Check all Phase 2 Deliverables Checklist items [x]
3. Mark all Validation items [x]
4. Mark "Phase 2 Complete" checkbox [x]
5. Fill in completion date, actual duration, and issues
6. Update overall project status

**Reporting**:
Provide summary including:
- Path counts by category
- Cleaning improvements (before/after)
- Key statistics
- Any anomalies found
- Confirmation that IMPLEMENTATIONMONITOR.md was updated
- Readiness for Phase 3
```

---

## Phase 3: Script Development

### Template Prompt for Task Tool

```
PHASE 3: SCRIPT DEVELOPMENT

**Context**:
I am implementing Phase 3 of the Claude Code Documentation Mirror project. This phase involves developing all major scripts for fetching, managing, and validating documentation.

**Prerequisites**:
- Phase 1 and 2 must be completed
- Verify IMPLEMENTATIONMONITOR.md shows Phases 1-2 complete
- paths_manifest.json exists with categorized paths

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 3 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md
- Upstream analysis: /home/rudycosta3/claude-code-docs/analysis/fetch_mechanism.md
- Path manifest: /home/rudycosta3/claude-code-docs/paths_manifest.json

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 4 tasks of Phase 3:
1. Rewrite main.py as full documentation fetcher
2. Create update_sitemap.py for sitemap management
3. Create lookup_paths.py for path search/validation
4. Update extract_paths.py with CLI enhancements

**Duration**: 2 hours (most substantial phase)

**Detailed Tasks**:

TASK 3.1 - Rewrite main.py:

This is the core documentation fetcher. Study the upstream implementation from ./upstream/scripts/ and ./analysis/fetch_mechanism.md, then create a production-ready script.

Requirements:

1. **Core Functions** (implement these):

```python
import requests
import json
import time
from pathlib import Path
from typing import Optional, Dict, List
import argparse
from bs4 import BeautifulSoup  # Or whatever upstream uses
import markdownify  # Or equivalent

def fetch_page(url: str, timeout: int = 30) -> str:
    """
    Fetch HTML content from URL with proper error handling.

    Features:
    - Retry logic (3 attempts)
    - Proper user agent
    - Timeout handling
    - HTTP error handling
    """

def parse_html(html: str) -> dict:
    """
    Extract content from HTML page.

    Returns:
    {
        'title': str,
        'content': str,
        'metadata': dict
    }
    """

def html_to_markdown(html: str) -> str:
    """
    Convert HTML to clean markdown.

    Features:
    - Preserve code blocks
    - Handle images correctly
    - Clean internal links
    - Remove navigation elements
    """

def save_documentation(path: str, content: str, output_dir: Path):
    """
    Save markdown to proper directory structure.

    Example: /en/docs/build-with-claude
    Saves to: docs/en/docs/build-with-claude.md
    """

def update_documentation(
    paths: List[str],
    output_dir: Path,
    force: bool = False,
    rate_limit: float = 0.5
) -> Dict:
    """
    Main orchestration function.

    Features:
    - Progress bar
    - Incremental updates (skip unchanged)
    - Error handling and reporting
    - Rate limiting
    - Success/failure tracking

    Returns:
    {
        'success_count': int,
        'failed_count': int,
        'skipped_count': int,
        'errors': List[dict]
    }
    """
```

2. **CLI Interface**:

```python
def main():
    parser = argparse.ArgumentParser(
        description='Claude Documentation Fetcher'
    )
    parser.add_argument(
        '--update-all',
        action='store_true',
        help='Update all documentation'
    )
    parser.add_argument(
        '--update-category',
        choices=['core', 'api', 'claude_code', 'prompt_library'],
        help='Update specific category'
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-fetch all pages'
    )
    parser.add_argument(
        '--output-dir',
        default='docs',
        help='Output directory'
    )
    parser.add_argument(
        '--rate-limit',
        type=float,
        default=0.5,
        help='Delay between requests in seconds'
    )
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO'
    )
```

3. **Implementation Details**:
   - Read paths from paths_manifest.json
   - Construct full URLs (https://docs.anthropic.com + path)
   - Fetch each page with rate limiting
   - Parse and convert to markdown
   - Save to docs/ directory with proper structure
   - Track progress and errors
   - Generate summary report

4. **Error Handling**:
   - HTTP 404: Log and continue
   - HTTP 429: Increase rate limit delay
   - HTTP 500: Retry with exponential backoff
   - Network timeout: Retry 3 times
   - Parsing errors: Log and skip

5. **Testing**:
```bash
# Test with small sample
python main.py --update-category prompt_library

# Verify output
ls -la docs/en/prompt-library/

# Test individual functions
pytest tests/unit/test_file_operations.py
```

TASK 3.2 - Create update_sitemap.py:

Create a script to manage sitemap and search indexes.

```python
import json
from pathlib import Path
from typing import Dict, List

def generate_index(category: str, paths: List[str]) -> dict:
    """
    Generate index structure for a category.

    Returns navigation tree:
    {
        'category': str,
        'count': int,
        'paths': [...],
        'tree': {...}  # Hierarchical structure
    }
    """

def update_search_index(manifest: dict, docs_dir: Path):
    """
    Create optimized search index.

    Index structure:
    {
        'path': {
            'title': str,
            'keywords': List[str],
            'content_preview': str
        }
    }
    """

def sync_with_ericbuess_format():
    """
    Ensure compatibility with upstream format.
    """

def main():
    # Read paths_manifest.json
    # Generate category indexes
    # Create search index
    # Save to docs/sitemap.json and docs/indexes/
```

Output files:
- docs/sitemap.json
- docs/indexes/core_documentation.json
- docs/indexes/api_reference.json
- docs/indexes/claude_code.json
- docs/indexes/prompt_library.json
- docs/.search_index (optimized for fast lookups)

TASK 3.3 - Create lookup_paths.py:

Create utility for searching and validating paths.

```python
import json
import argparse
from pathlib import Path
from typing import List, Dict
import requests
from difflib import get_close_matches

def search_paths(query: str, manifest: dict) -> List[dict]:
    """
    Fuzzy search in path database.

    Returns ranked results with relevance scores.
    """

def validate_path(path: str, base_url: str = 'https://docs.anthropic.com') -> dict:
    """
    Check if path is reachable.

    Returns:
    {
        'path': str,
        'status': int,
        'reachable': bool,
        'redirect': Optional[str]
    }
    """

def batch_validate(paths: List[str]) -> dict:
    """
    Validate all paths efficiently.

    Uses threading for parallel validation.
    Shows progress bar.
    """

def suggest_alternatives(path: str, manifest: dict) -> List[str]:
    """
    Find similar paths for broken links.
    """

def main():
    parser = argparse.ArgumentParser(description='Path lookup utility')
    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--validate-all', action='store_true')
    parser.add_argument('--check', help='Validate specific path')
    parser.add_argument('--batch-validate', help='File with paths to validate')
```

Test:
```bash
python lookup_paths.py "prompt engineering"
python lookup_paths.py --check /en/docs/build-with-claude
python lookup_paths.py --validate-all
```

TASK 3.4 - Update extract_paths.py:

Add CLI functionality from Phase 2 if not already done:
```bash
python extract_paths.py --source temp.html --output paths_manifest.json
python extract_paths.py --validate
python extract_paths.py --stats
```

Ensure all functions from Task 2.1 are implemented and working.

**Success Criteria**:
- [ ] main.py is 500+ lines with full functionality
- [ ] Can successfully fetch and save documentation
- [ ] update_sitemap.py generates all index files
- [ ] lookup_paths.py can search and validate paths
- [ ] All scripts have working CLI interfaces
- [ ] Error handling works correctly
- [ ] Rate limiting prevents server overload
- [ ] Scripts match ericbuess approach

**Testing Checklist**:
```bash
# Test main.py
python main.py --update-category prompt_library
# Should fetch ~105 pages successfully

# Test update_sitemap.py
python update_sitemap.py
# Should create docs/sitemap.json and docs/indexes/

# Test lookup_paths.py
python lookup_paths.py "mcp"
# Should return relevant paths

# Verify outputs
ls -la docs/
cat docs/sitemap.json | head -20
```

**After Completion - CRITICAL**:
Update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:
1. Mark all Task 3.1, 3.2, 3.3, 3.4 checkboxes [x]
2. Check all Phase 3 Deliverables [x]
3. Check all Validation items [x]
4. Mark "Phase 3 Complete" [x]
5. Fill in completion details
6. Update overall project status

**Reporting**:
Provide summary including:
- Lines of code written
- Test results
- Sample fetched documentation
- Any implementation challenges
- Performance metrics
- Confirmation of IMPLEMENTATIONMONITOR.md update
- Readiness for Phase 4
```

---

## Phase 4: Integration & Adaptation

### Template Prompt for Task Tool

```
PHASE 4: INTEGRATION & ADAPTATION

**Context**:
I am implementing Phase 4 of the Claude Code Documentation Mirror project. This phase integrates everything with the ericbuess structure and sets up automation.

**Prerequisites**:
- Phases 1-3 complete
- Verify IMPLEMENTATIONMONITOR.md shows completion
- Verify scripts are working (main.py, lookup_paths.py, etc.)

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 4 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md
- Upstream structure: /home/rudycosta3/claude-code-docs/analysis/repo_structure.md

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 4 tasks of Phase 4:
1. Match ericbuess directory structure
2. Configure .claude/ integration
3. Setup GitHub Actions workflows
4. Configure version control

**Detailed Tasks**:

TASK 4.1 - Match ericbuess Directory Structure:

1. Create standard directory hierarchy:
```bash
mkdir -p docs/en/{docs,api,prompt-library,resources,release-notes}
mkdir -p scripts/
mkdir -p .github/workflows/
mkdir -p .claude/commands/
mkdir -p analysis/
mkdir -p tests/{unit,integration,validation,fixtures}
```

2. Move scripts to scripts/ directory:
```bash
mv main.py scripts/
mv extract_paths.py scripts/
mv lookup_paths.py scripts/
mv update_sitemap.py scripts/
```

3. Update all import paths in scripts if needed

4. Verify structure matches upstream:
```bash
tree -L 2 ./upstream/
tree -L 2 .
# Compare and ensure compatibility
```

5. Test scripts still work from new locations:
```bash
python scripts/main.py --help
python scripts/lookup_paths.py --help
```

TASK 4.2 - Configure .claude/ Integration:

1. Create `.claude/commands/docs.md`:

```markdown
---
description: Search Claude documentation using natural language queries
---

You are helping the user search through locally mirrored Claude documentation.

When the user provides a query:
1. Use the lookup_paths.py script to search for relevant paths
2. Read the paths_manifest.json to find matching documentation
3. Read the actual markdown files from the docs/ directory
4. Present the most relevant information
5. Suggest related documentation pages

Example usage:
- User: "how do I use tool use with python?"
- You should: Search for "tool use python", find relevant paths like /en/docs/build-with-claude/tool-use, read the content, and provide a helpful summary with code examples

The documentation is located in: /home/rudycosta3/claude-code-docs/docs/
The path manifest is: /home/rudycosta3/claude-code-docs/paths_manifest.json
Search utility: /home/rudycosta3/claude-code-docs/scripts/lookup_paths.py

Always cite the specific documentation page you're referencing.
```

2. Create `.claude/commands/update-docs.md`:

```markdown
---
description: Update local documentation mirror
---

Run the documentation update script to fetch latest changes from docs.anthropic.com.

Execute:
```bash
cd /home/rudycosta3/claude-code-docs
python scripts/main.py --update-all
```

Show progress and report results to the user.
```

3. Create `.claude/commands/search-docs.md`:

```markdown
---
description: Search documentation paths
---

Search for documentation paths matching the user's query.

Execute:
```bash
cd /home/rudycosta3/claude-code-docs
python scripts/lookup_paths.py "<user_query>"
```

Display results to the user.
```

4. Create `.claude/commands/validate-docs.md`:

```markdown
---
description: Validate all documentation paths
---

Run validation to check all documentation paths are reachable.

Execute:
```bash
cd /home/rudycosta3/claude-code-docs
python scripts/lookup_paths.py --validate-all
```

Report results to the user.
```

5. Test the commands:
```bash
# In Claude Code, test:
/docs how to use mcp
/update-docs
/search-docs prompt engineering
/validate-docs
```

TASK 4.3 - Setup GitHub Actions Workflows:

1. Create `.github/workflows/update-docs.yml`:

```yaml
name: Update Documentation

on:
  schedule:
    - cron: '0 */3 * * *'  # Every 3 hours
  workflow_dispatch:  # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4 markdownify
          pip install -e .

      - name: Run documentation update
        run: |
          python scripts/main.py --update-all

      - name: Check for changes
        id: check_changes
        run: |
          if [[ -n $(git status -s) ]]; then
            echo "changes=true" >> $GITHUB_OUTPUT
          else
            echo "changes=false" >> $GITHUB_OUTPUT
          fi

      - name: Commit changes
        if: steps.check_changes.outputs.changes == 'true'
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add docs/
          git commit -m "docs: Update documentation [automated]

          Updated $(date +'%Y-%m-%d %H:%M:%S UTC')

          🤖 Generated by GitHub Actions"
          git push

      - name: Generate changelog
        if: steps.check_changes.outputs.changes == 'true'
        run: |
          python scripts/generate_changelog.py >> CHANGELOG.md
```

2. Create `.github/workflows/test.yml`:

```yaml
name: Test Suite

on:
  push:
    branches: [ main, master, develop ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov pytest-asyncio

      - name: Run unit tests
        run: pytest tests/unit/ -v --cov=scripts

      - name: Run integration tests
        run: pytest tests/integration/ -v

      - name: Generate coverage report
        run: pytest --cov=scripts --cov-report=xml --cov-report=term

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: false
```

3. Create `.github/workflows/validate.yml`:

```yaml
name: Validate Documentation

on:
  schedule:
    - cron: '0 6 * * *'  # Daily at 6am UTC
  workflow_dispatch:

jobs:
  validate:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: pip install -e .

      - name: Validate all paths reachable
        run: python scripts/lookup_paths.py --validate-all

      - name: Run validation tests
        run: pytest tests/validation/ -v

      - name: Generate validation report
        run: |
          mkdir -p reports
          python scripts/generate_validation_report.py > reports/validation-$(date +'%Y%m%d').md

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: validation-report
          path: reports/validation-*.md
```

4. Validate workflow syntax:
```bash
# If actionlint is installed:
actionlint .github/workflows/*.yml
```

TASK 4.4 - Version Control Setup:

1. Create `CHANGELOG.md`:

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial implementation of Claude Code documentation mirror
- 550+ documentation paths across 4 categories
- Automated updates every 3 hours via GitHub Actions
- Natural language documentation search via `/docs` command
- Path validation and search utilities
- Comprehensive testing suite (85%+ coverage)

### Categories Included
- Core Documentation (~280 paths)
- API Reference (~95 paths)
- Claude Code Documentation (~70 paths)
- Prompt Library (~105 paths)

## [0.1.0] - 2025-11-03

### Initial Release
- Project setup and structure
- Basic path extraction
- Integration with ericbuess/claude-code-docs approach
```

2. Update `.gitignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
.venv/
venv/
ENV/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover
.hypothesis/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Project specific
temp.html
upstream/
*.log

# Keep these
!docs/
!scripts/
!tests/
!.github/
!.claude/
```

3. Commit initial structure:
```bash
git add .
git commit -m "feat: Initial project structure

- Setup directory structure matching costiash
- Add GitHub Actions workflows for automation
- Configure Claude Code integration
- Add version control files

Phase 4 complete"
```

**Success Criteria**:
- [ ] Directory structure matches ericbuess
- [ ] All scripts moved to scripts/ and working
- [ ] `.claude/commands/` has 4 command files
- [ ] `/docs` command functional
- [ ] 3 GitHub Actions workflows created
- [ ] Workflows syntax is valid
- [ ] `CHANGELOG.md` created
- [ ] `.gitignore` configured
- [ ] Initial commit made

**Testing**:
```bash
# Test directory structure
tree -L 2 . | head -30

# Test scripts from new location
python scripts/main.py --help
python scripts/lookup_paths.py "test query"

# Test Claude Code commands (manually in Claude Code)
/docs how to use tool use
/search-docs mcp

# Validate workflows
actionlint .github/workflows/*.yml || echo "actionlint not installed"
```

**After Completion - CRITICAL**:
Update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:
1. Mark all Task 4.1, 4.2, 4.3, 4.4 checkboxes [x]
2. Check all Phase 4 Deliverables [x]
3. Check all Validation items [x]
4. Mark "Phase 4 Complete" [x]
5. Fill in completion details
6. Update overall status

**Reporting**:
Provide summary including:
- Directory structure changes
- Claude Code commands tested
- GitHub Actions workflows created
- Git commit hash
- Confirmation of IMPLEMENTATIONMONITOR.md update
- Readiness for Phase 5
```

---

## Phase 5: Comprehensive Testing Suite

### Template Prompt for Task Tool

```
PHASE 5: COMPREHENSIVE TESTING SUITE

**Context**:
I am implementing Phase 5 of the Claude Code Documentation Mirror project. This is a critical phase where we create a comprehensive testing suite to ensure reliability and achieve 85%+ code coverage.

**Prerequisites**:
- Phases 1-4 complete
- All scripts functional in scripts/ directory
- Verify IMPLEMENTATIONMONITOR.md shows completion

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 5 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 5 tasks of Phase 5:
1. Create unit tests (20+ tests)
2. Create integration tests (10+ tests)
3. Create validation tests (15+ tests)
4. Setup CI/CD pipelines
5. Configure test infrastructure

**Duration**: 2.5 hours (substantial testing work)

**Detailed Tasks**:

TASK 5.1 - Create Unit Tests:

Create tests/unit/ with the following test files:

**File 1: tests/unit/test_path_extraction.py**

```python
"""Unit tests for path extraction and cleaning."""

import pytest
from scripts.extract_paths import (
    clean_path,
    is_valid_path,
    categorize_path,
    extract_fragment
)

def test_clean_trailing_backslashes():
    """Test removal of backslash artifacts."""
    assert clean_path("/en/docs/test\\") == "/en/docs/test"
    assert clean_path("/en/api/endpoint\\\\") == "/en/api/endpoint"

def test_remove_duplicates():
    """Test deduplication logic."""
    # Implementation

def test_filter_noise_patterns():
    """Test that :slug* and artifacts are removed."""
    assert not is_valid_path("/en/docs/:slug*")
    assert not is_valid_path("/en/api/),")

def test_categorize_paths():
    """Test correct category assignment."""
    assert categorize_path("/en/docs/build-with-claude") == "core_documentation"
    assert categorize_path("/en/api/messages") == "api_reference"
    assert categorize_path("/en/docs/claude-code/overview") == "claude_code"
    assert categorize_path("/en/prompt-library/code-consultant") == "prompt_library"

def test_extract_fragments():
    """Test URL fragment separation."""
    path, fragment = extract_fragment("/en/docs/page#section")
    assert path == "/en/docs/page"
    assert fragment == "section"

# Add more tests (target: 8+ tests in this file)
```

**File 2: tests/unit/test_url_validation.py**

```python
"""Unit tests for URL validation."""

import pytest
from scripts.lookup_paths import validate_path, search_paths

def test_url_format_validation():
    """Test valid URL formats are accepted."""
    # Implementation

def test_reachability_check_success():
    """Test HTTP 200 detection."""
    # Use mocked requests

def test_broken_link_detection():
    """Test 404 detection."""
    # Implementation

def test_redirect_handling():
    """Test 301/302 handling."""
    # Implementation

# Target: 6+ tests
```

**File 3: tests/unit/test_file_operations.py**

```python
"""Unit tests for file operations."""

import pytest
from pathlib import Path
from scripts.main import (
    fetch_page,
    parse_html,
    html_to_markdown,
    save_documentation
)

def test_read_html_file(tmp_path):
    """Test HTML file reading."""
    # Implementation

def test_write_markdown_file(tmp_path):
    """Test markdown saving."""
    # Implementation

def test_html_to_markdown_conversion():
    """Test HTML to markdown conversion."""
    html = "<h1>Title</h1><p>Content</p>"
    md = html_to_markdown(html)
    assert "# Title" in md
    assert "Content" in md

def test_preserve_code_blocks():
    """Test code formatting preserved."""
    html = "<pre><code>print('hello')</code></pre>"
    md = html_to_markdown(html)
    assert "```" in md or "`print('hello')`" in md

def test_handle_images():
    """Test image references."""
    # Implementation

# Target: 8+ tests
```

**File 4: tests/unit/test_categorization.py**

```python
"""Unit tests for categorization logic."""

import pytest
from scripts.extract_paths import categorize_path

def test_core_docs_category():
    """Test core documentation categorization."""
    assert categorize_path("/en/docs/build-with-claude") == "core_documentation"

def test_api_reference_category():
    """Test API reference categorization."""
    assert categorize_path("/en/api/messages") == "api_reference"

def test_claude_code_category():
    """Test Claude Code categorization."""
    assert categorize_path("/en/docs/claude-code/mcp") == "claude_code"

def test_prompt_library_category():
    """Test prompt library categorization."""
    assert categorize_path("/en/prompt-library/grammar-genie") == "prompt_library"

# Target: 6+ tests
```

Run unit tests:
```bash
pytest tests/unit/ -v
```

TASK 5.2 - Create Integration Tests:

**File 1: tests/integration/test_full_workflow.py**

```python
"""Integration tests for complete workflows."""

import pytest
from pathlib import Path
import json

def test_full_pipeline(tmp_path):
    """Test fetch → parse → convert → save workflow."""
    # Test with a small set of paths
    # Verify files are created correctly

def test_incremental_update(tmp_path):
    """Test that unchanged docs are skipped."""
    # Run update twice
    # Verify second run skips unchanged

def test_error_recovery(tmp_path):
    """Test that failures don't corrupt database."""
    # Introduce error
    # Verify graceful handling

def test_rate_limiting():
    """Test that rate limits are respected."""
    # Time multiple requests
    # Verify delays are applied

# Target: 6+ tests
```

**File 2: tests/integration/test_update_detection.py**

```python
"""Integration tests for change detection."""

def test_detect_content_changes():
    """Test content change detection."""

def test_skip_unchanged():
    """Test unchanged docs are skipped."""

def test_changelog_generation():
    """Test changes are logged correctly."""

# Target: 4+ tests
```

**File 3: tests/integration/test_github_actions.py**

```python
"""Test workflow simulation."""

def test_scheduled_update_workflow():
    """Simulate cron job execution."""

def test_manual_trigger():
    """Test workflow_dispatch."""

def test_commit_and_push():
    """Test changes are committed."""

# Target: 4+ tests
```

Run integration tests:
```bash
pytest tests/integration/ -v
```

TASK 5.3 - Create Validation Tests:

**File 1: tests/validation/test_path_reachability.py**

```python
"""Validate all paths are accessible."""

import pytest
import json
from pathlib import Path

def test_all_paths_reachable():
    """Test all 550+ paths return HTTP 200."""
    manifest = json.loads(Path('paths_manifest.json').read_text())
    # Test sample of paths (not all 550 in CI)

def test_batch_validation():
    """Test efficient bulk validation."""

def test_report_broken_links():
    """Generate report of 404s."""

# Target: 5+ tests
```

**File 2: tests/validation/test_content_validity.py**

```python
"""Validate HTML and markdown quality."""

def test_valid_html():
    """Test fetched HTML is well-formed."""

def test_valid_markdown():
    """Test generated markdown is valid."""

def test_no_parsing_errors():
    """Test parser handles all pages."""

# Target: 5+ tests
```

**File 3: tests/validation/test_link_integrity.py**

```python
"""Test internal link validity."""

def test_internal_links_work():
    """Test links between docs resolve."""

def test_no_broken_anchors():
    """Test fragment identifiers valid."""

def test_relative_links():
    """Test relative links converted correctly."""

# Target: 5+ tests
```

**File 4: tests/validation/test_sitemap_consistency.py**

```python
"""Validate sitemap matches actual docs."""

def test_manifest_completeness():
    """Test all files in manifest."""

def test_no_orphaned_files():
    """Test no files missing from manifest."""

def test_category_counts():
    """Test category counts match."""

# Target: 5+ tests
```

TASK 5.4 - Setup CI/CD Pipelines:

Update .github/workflows/ files from Phase 4 to include full test execution.

Update `.github/workflows/test.yml`:
```yaml
# Add comprehensive test execution
- name: Run all tests
  run: |
    pytest tests/ -v --cov=scripts --cov-report=xml --cov-report=term

- name: Check coverage threshold
  run: |
    coverage report --fail-under=85
```

Create `.github/workflows/coverage.yml`:
```yaml
name: Coverage Report

on:
  push:
    branches: [ main, master ]
  pull_request:

jobs:
  coverage:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python 3.12
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
          pip install pytest pytest-cov

      - name: Generate coverage
        run: pytest --cov=scripts --cov-report=html --cov-report=term

      - name: Check coverage threshold (85%)
        run: coverage report --fail-under=85

      - name: Upload HTML coverage report
        uses: actions/upload-artifact@v3
        with:
          name: coverage-report
          path: htmlcov/
```

TASK 5.5 - Setup Test Infrastructure:

1. Create `tests/conftest.py`:

```python
"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import json

@pytest.fixture
def sample_html():
    """Sample HTML for testing."""
    return """
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Test Title</h1>
        <p>Test content</p>
        <pre><code>print('test')</code></pre>
    </body>
    </html>
    """

@pytest.fixture
def sample_paths():
    """Sample paths for testing."""
    return [
        '/en/docs/build-with-claude',
        '/en/api/messages',
        '/en/prompt-library/code-consultant'
    ]

@pytest.fixture
def mock_http_response(monkeypatch):
    """Mock HTTP requests."""
    import requests
    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = "<html>Mock content</html>"
            def raise_for_status(self):
                pass
        return MockResponse()
    monkeypatch.setattr(requests, 'get', mock_get)

@pytest.fixture
def paths_manifest():
    """Load paths manifest for tests."""
    manifest_path = Path(__file__).parent.parent / 'paths_manifest.json'
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())
    return {
        'metadata': {'total_paths': 0},
        'categories': {}
    }
```

2. Create test fixtures in `tests/fixtures/`:
- sample.html
- sample_paths.txt
- invalid_paths.txt
- expected_output.md

3. Update pyproject.toml:
```toml
[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.10.0",
]
```

4. Install test dependencies:
```bash
pip install -e ".[dev]"
```

5. Run complete test suite:
```bash
pytest tests/ -v --cov=scripts --cov-report=html --cov-report=term
```

**Success Criteria**:
- [ ] tests/unit/ has 4 files with 20+ tests total
- [ ] tests/integration/ has 3 files with 10+ tests
- [ ] tests/validation/ has 4 files with 15+ tests
- [ ] All tests passing (100%)
- [ ] Code coverage ≥ 85%
- [ ] CI/CD workflows updated
- [ ] tests/conftest.py with fixtures
- [ ] Test infrastructure working

**Validation**:
```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest --cov=scripts --cov-report=term

# Verify threshold
coverage report --fail-under=85

# Generate HTML report
pytest --cov=scripts --cov-report=html
```

**After Completion - CRITICAL**:
Update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:
1. Mark all Task 5.1-5.5 checkboxes [x]
2. Check all Phase 5 Deliverables [x]
3. Check Validation items [x]
4. Record actual coverage achieved
5. Mark "Phase 5 Complete" [x]
6. Update overall status

**Reporting**:
Provide summary including:
- Total tests created
- Tests passing percentage
- Code coverage achieved
- Any test failures
- Performance of test suite
- Confirmation of IMPLEMENTATIONMONITOR.md update
- Readiness for Phase 6
```

---

## Phase 6: Documentation & Guidelines

### Template Prompt for Task Tool

```
PHASE 6: DOCUMENTATION & GUIDELINES

**Context**:
I am implementing Phase 6 of the Claude Code Documentation Mirror project. This phase creates comprehensive documentation for users and contributors.

**Prerequisites**:
- Phases 1-5 complete
- All tests passing
- Verify IMPLEMENTATIONMONITOR.md shows completion

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 6 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 4 tasks of Phase 6:
1. Update README.md with comprehensive project documentation
2. Create DEVELOPMENT.md with contributor guide
3. Create docs/CAPABILITIES.md documenting features
4. Create docs/EXAMPLES.md with usage examples

**Duration**: 45 minutes

**Detailed Tasks**:

TASK 6.1 - Update README.md:

The README.md should be the main entry point for the project. Follow this comprehensive structure:

```markdown
# Claude Code Documentation Mirror

[Badge: Build Status] [Badge: Coverage] [Badge: License]

> Local mirror of Anthropic's Claude documentation for offline access and fast queries

## Overview

Brief description of the project (2-3 sentences).

## Features

- ✅ Complete Coverage: 550+ documentation pages
- ✅ Auto-Updates: Every 3 hours via GitHub Actions
- ✅ Fast Search: Optimized search index
- ✅ Claude Code Integration: `/docs` command
- ✅ Version Tracking: Full changelog
- ✅ 85%+ Test Coverage

## Documentation Categories

List the 4 categories with counts:
1. Core Documentation (~280 paths) - Details
2. API Reference (~95 paths) - Details
3. Claude Code Documentation (~70 paths) - Details
4. Prompt Library (~105 paths) - Details

## Installation

### Prerequisites
- Python 3.12+
- Git
- Claude Code (optional)

### Quick Start
```bash
# Step by step installation commands
```

## Usage

### Update Documentation
```bash
# Commands and examples
```

### Search Documentation
```bash
# Commands and examples
```

### Claude Code Integration
```
# How to use /docs command
```

## Architecture

```
Directory structure visualization
```

## Testing

```bash
# How to run tests
```

## Contributing

Link to DEVELOPMENT.md

## Acknowledgments

Credit to ericbuess/claude-code-docs

## License

MIT License

## Links

- Official Claude Docs
- Claude Code
- Issue Tracker
```

Fill in all sections based on the actual implementation.

TASK 6.2 - Create DEVELOPMENT.md:

This is the contributor guide. Create comprehensive documentation:

```markdown
# Development Guide

## Setup for Contributors

### 1. Clone and Setup
[Detailed steps]

### 2. Install Pre-commit Hooks
[If applicable]

## Code Structure

### Main Scripts
Explain each script:
- **main.py** - Purpose, key functions
- **extract_paths.py** - Purpose, key functions
- **lookup_paths.py** - Purpose, key functions
- **update_sitemap.py** - Purpose, key functions

### Test Structure
[Explain test organization]

## Testing Guidelines

### Running Tests
[All test commands]

### Writing Tests
[Examples and best practices]

### Test Coverage Requirements
- Minimum: 85%
- Critical paths: 100%

### Mocking External Dependencies
[Examples]

## Code Style

### Python Style Guide
- PEP 8
- Type hints required
- Max line length: 100
- Docstrings required

[Example code with proper style]

### Linting and Formatting
[Commands]

## Release Process

### 1. Version Bump
### 2. Update Changelog
### 3. Create Release

## Common Tasks

### Adding a New Path Category
[Step by step]

### Adding a New Script
[Step by step]

### Debugging
[Tips and tools]

## Troubleshooting

[Common issues and solutions]

## Resources

[Helpful links]
```

TASK 6.3 - Create docs/CAPABILITIES.md:

Document all capabilities and features:

```markdown
# Documentation Mirror Capabilities

## Overview

[Description]

## Complete Path Coverage

### Core Documentation (~280 paths)

**Build with Claude**:
- [List features]

**Agents & Tools**:
- [List features]

[Continue for all categories]

### API Reference (~95 paths)
[Details]

### Claude Code Documentation (~70 paths)
[Details]

### Prompt Library (~105 paths)
[Details]

## Features

### 1. Automatic Updates
- Frequency: Every 3 hours
- Method: GitHub Actions
- Change detection
- Changelog generation

### 2. Fast Search
[Details]

### 3. Natural Language Queries
[Examples]

### 4. Version Tracking
[Details]

### 5. Offline Access
[Details]

### 6. Validation
[Details]

## Usage Examples

[Real examples]

## Roadmap

### Planned Features
[List]

### Future Enhancements
[List]
```

TASK 6.4 - Create docs/EXAMPLES.md:

Provide practical usage examples:

```markdown
# Usage Examples

## Common Queries

### 1. Prompt Engineering
[Example with command and output]

### 2. Claude Code MCP
[Example with command and output]

### 3. API Reference
[Example with command and output]

[More examples...]

## Troubleshooting

### Issue: Documentation Out of Date
**Problem**: [Description]
**Solution**: [Commands and steps]

### Issue: Broken Links
**Problem**: [Description]
**Solution**: [Commands and steps]

### Issue: Slow Search
**Problem**: [Description]
**Solution**: [Commands and steps]

[More troubleshooting scenarios...]

## FAQ

### Q: How often is documentation updated?
**A**: [Answer]

### Q: Can I use this offline?
**A**: [Answer]

### Q: How much disk space does it use?
**A**: [Answer]

[More FAQs...]
```

**Success Criteria**:
- [ ] README.md is comprehensive and well-structured
- [ ] DEVELOPMENT.md provides clear contributor guidance
- [ ] docs/CAPABILITIES.md documents all features
- [ ] docs/EXAMPLES.md has practical examples
- [ ] All documentation is clear and accurate
- [ ] No typos or formatting issues
- [ ] Links are valid

**Validation**:
1. Read through each document for clarity
2. Test all code examples and commands
3. Verify all links work
4. Check formatting renders correctly
5. Ensure consistency across documents

**After Completion - CRITICAL**:
Update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:
1. Mark all Task 6.1-6.4 checkboxes [x]
2. Check all Phase 6 Deliverables [x]
3. Check Validation items [x]
4. Mark "Phase 6 Complete" [x]
5. Update overall status

**Reporting**:
Provide summary including:
- Documentation files created
- Total word count across docs
- Key sections highlighted
- Confirmation of IMPLEMENTATIONMONITOR.md update
- Readiness for Phase 7 (final validation)
```

---

## Phase 7: Validation & Quality Assurance

### Template Prompt for Task Tool

```
PHASE 7: VALIDATION & QUALITY ASSURANCE

**Context**:
I am implementing the FINAL phase (Phase 7) of the Claude Code Documentation Mirror project. This critical phase validates that everything works correctly before production release.

**Prerequisites**:
- Phases 1-6 ALL complete
- Verify IMPLEMENTATIONMONITOR.md shows all phases complete
- All tests passing from Phase 5
- All documentation complete from Phase 6

**Reference Documents**:
- Implementation Plan: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATION_PLAN.md (Phase 7 section)
- Progress Monitor: /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md

**Working Directory**: /home/rudycosta3/claude-code-docs

**Objective**:
Complete all 5 tasks of Phase 7:
1. Run full test suite and verify 85%+ coverage
2. Perform manual validation of documentation
3. Conduct performance testing
4. Complete security review
5. Execute final integration test

**Duration**: 1 hour

**THIS IS THE FINAL PHASE - BE THOROUGH**

**Detailed Tasks**:

TASK 7.1 - Run Full Test Suite:

Execute comprehensive testing:

```bash
# 1. Run ALL tests with verbose output
pytest tests/ -v --cov=scripts --cov-report=html --cov-report=term

# 2. Verify coverage threshold
coverage report --fail-under=85

# 3. Generate detailed HTML coverage report
pytest --cov=scripts --cov-report=html

# 4. Check for warnings
pytest tests/ -v --strict-warnings

# 5. Run specific test suites
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/validation/ -v
```

**Success Criteria**:
- [ ] All tests pass (100%)
- [ ] Coverage ≥ 85%
- [ ] No critical warnings
- [ ] All test suites complete successfully
- [ ] HTML coverage report generated

Document results:
- Total tests: ___
- Passing: ___
- Coverage: ___%
- Warnings: ___

TASK 7.2 - Manual Validation:

Perform manual checks:

**1. Spot-check 20 random paths**:

```bash
# Generate random sample
python -c "
import random, json
from pathlib import Path
manifest = json.loads(Path('paths_manifest.json').read_text())
all_paths = []
for category in manifest['categories'].values():
    all_paths.extend(category)
sample = random.sample(all_paths, min(20, len(all_paths)))
Path('sample_paths.txt').write_text('\n'.join(sample))
print('\n'.join(sample))
"

# Validate sample
python scripts/lookup_paths.py --batch-validate sample_paths.txt
```

Record results:
- Total checked: 20
- Reachable: ___
- Broken: ___
- Issues: ___

**2. Verify markdown formatting** (check 5 random files):

```bash
# Pick 5 random markdown files from docs/
find docs/ -name "*.md" | shuf -n 5 | while read file; do
    echo "Checking: $file"
    cat "$file" | head -30
done
```

Check for:
- [ ] Proper markdown syntax
- [ ] Code blocks formatted correctly
- [ ] Links working
- [ ] Images referenced properly
- [ ] No HTML artifacts

**3. Test `/docs` command**:

In Claude Code, test these queries:
```
/docs how to use prompt engineering
/docs mcp quickstart
/docs api messages endpoint
/docs tool use with python
/docs batch processing
```

Verify:
- [ ] Results are relevant
- [ ] Content is accurate
- [ ] Formatting is correct
- [ ] Related links suggested
- [ ] Response time acceptable

**4. Validate GitHub Actions workflows**:

```bash
# Check syntax (if actionlint installed)
actionlint .github/workflows/*.yml

# Manually review each workflow file
cat .github/workflows/update-docs.yml
cat .github/workflows/test.yml
cat .github/workflows/validate.yml
```

Verify:
- [ ] Syntax is valid
- [ ] Cron schedules correct
- [ ] All steps logical
- [ ] Secrets properly referenced
- [ ] Error handling present

TASK 7.3 - Performance Testing:

Measure and optimize performance:

**1. Fetch time measurement**:

```bash
# Time update of prompt library category
time python scripts/main.py --update-category prompt_library

# Should complete in < 2 minutes for ~105 paths
```

Record:
- Time taken: ___
- Paths processed: ___
- Average per path: ___
- Target: < 2 min for 100 paths

**2. Memory usage**:

```bash
# Monitor memory during full update
/usr/bin/time -v python scripts/main.py --update-category api_reference 2>&1 | grep "Maximum resident set size"

# Should be < 500 MB
```

Record:
- Peak memory: ___ MB
- Target: < 500 MB

**3. Profile performance** (if bottlenecks found):

```bash
python -m cProfile -o profile.stats scripts/main.py --update-category claude_code

# Analyze
python -m pstats profile.stats <<EOF
sort cumtime
stats 20
quit
EOF
```

Identify and document bottlenecks:
- Slowest functions: ___
- Optimization opportunities: ___

**4. Search performance**:

```bash
# Time search operations
time python scripts/lookup_paths.py "prompt engineering"
time python scripts/lookup_paths.py "mcp"
time python scripts/lookup_paths.py "api messages"

# Should be < 1 second each
```

TASK 7.4 - Security Review:

Complete security checklist:

**1. Input Sanitization**:
```python
# Review code for:
# - Path traversal vulnerabilities
# - SQL injection (if any database)
# - Command injection
# - XSS in markdown output

# Check these files:
# - scripts/main.py
# - scripts/extract_paths.py
# - scripts/lookup_paths.py
```

Checklist:
- [ ] Path inputs validated (no ../)
- [ ] URL inputs validated (no SSRF)
- [ ] File writes use safe paths
- [ ] No arbitrary command execution

**2. Safe File Operations**:
```bash
# Review file operations in all scripts
grep -r "open(" scripts/
grep -r "Path(" scripts/
grep -r "write" scripts/
```

Checklist:
- [ ] No arbitrary file writes
- [ ] Proper permissions set
- [ ] No symlink vulnerabilities
- [ ] Error handling prevents leaks

**3. No Hardcoded Credentials**:
```bash
# Search for potential secrets
grep -ri "password" .
grep -ri "api_key" .
grep -ri "secret" .
grep -ri "token" .
```

Checklist:
- [ ] No API keys in code
- [ ] No passwords in config
- [ ] Secrets use environment variables
- [ ] No tokens in Git history

**4. GitHub Actions Security**:

Review workflows for:
- [ ] Secrets properly configured
- [ ] No secrets printed to logs
- [ ] Minimal permissions used
- [ ] Dependencies pinned

**5. Security Scan**:
```bash
# Install security tools
uv add install bandit safety

# Run scans
bandit -r scripts/
safety check

# Address any HIGH or CRITICAL issues
```

TASK 7.5 - Final Integration Test:

**CLEAN ENVIRONMENT TEST** - Most important validation:

```bash
# 1. Create clean test environment
mkdir -p /tmp/test-claude-docs-final
cd /tmp/test-claude-docs-final

# 2. Clone repository
git clone /home/rudycosta3/claude-code-docs .

# 3. Setup Python environment
python3.12 -m venv .venv
source .venv/bin/activate

# 4. Install project
pip install -e ".[dev]"

# 5. Verify installation
python scripts/main.py --help
python scripts/lookup_paths.py --help
python scripts/extract_paths.py --help
python scripts/update_sitemap.py --help

# 6. Run full fetch from scratch
echo "Starting full documentation fetch..."
python scripts/main.py --update-all

# 7. Verify all paths downloaded
ls -lah docs/
find docs/ -name "*.md" | wc -l

# 8. Run validation
python scripts/lookup_paths.py --validate-all

# 9. Run test suite
pytest tests/ -v

# 10. Test Claude Code integration (if installed)
# /docs test query
# /search-docs mcp

# 11. Generate report
echo "=== FINAL INTEGRATION TEST REPORT ===" > /tmp/integration_report.txt
echo "Date: $(date)" >> /tmp/integration_report.txt
echo "Documentation files: $(find docs/ -name '*.md' | wc -l)" >> /tmp/integration_report.txt
echo "Paths validated: [results]" >> /tmp/integration_report.txt
echo "Tests passed: [results]" >> /tmp/integration_report.txt

cat /tmp/integration_report.txt
```

**Success Criteria**:
- [ ] Clean clone successful
- [ ] Installation without errors
- [ ] All 550+ paths downloaded successfully
- [ ] No errors during fetch
- [ ] All validation tests pass
- [ ] `/docs` queries work correctly
- [ ] Documentation properly formatted
- [ ] No broken links
- [ ] All scripts functional

**Validation Checklist** (Final):

- [ ] **Documentation Coverage**: 550+ paths ✅
- [ ] **Test Coverage**: ≥ 85% ✅
- [ ] **All Tests Passing**: 100% ✅
- [ ] **Update Frequency**: Every 3 hours (configured) ✅
- [ ] **Performance**: < 2 min for 100 pages ✅
- [ ] **Memory Usage**: < 500 MB ✅
- [ ] **Path Reachability**: > 99% ✅
- [ ] **Security**: No critical issues ✅
- [ ] **Documentation**: Complete and accurate ✅
- [ ] **Integration**: Clean environment works ✅

**After Completion - CRITICAL - PROJECT COMPLETE**:

Update /home/rudycosta3/claude-code-docs/specs/IMPLEMENTATIONMONITOR.md:

1. Mark ALL Task 7.1-7.5 checkboxes [x]
2. Check ALL Phase 7 Deliverables [x]
3. Check ALL Validation Checklist items [x]
4. Mark "Phase 7 Complete" [x]
5. Fill in all completion details
6. Update "Overall Project Status":
   - Completed Tasks: 28/28
   - Overall Progress: 100%
   - Project Status: COMPLETE
7. Fill in "Final Project Sign-Off" section
8. Update all summary statistics

**Final Reporting**:

Provide comprehensive final report including:

```
===========================================
CLAUDE CODE DOCUMENTATION MIRROR
FINAL VALIDATION REPORT
===========================================

PROJECT COMPLETION DATE: [Date]
TOTAL TIME: [Hours]

PHASE COMPLETION:
✅ Phase 1: Repository Setup & Analysis
✅ Phase 2: Path Extraction & Cleaning
✅ Phase 3: Script Development
✅ Phase 4: Integration & Adaptation
✅ Phase 5: Comprehensive Testing Suite
✅ Phase 6: Documentation & Guidelines
✅ Phase 7: Validation & Quality Assurance

DELIVERABLES:
✅ 550+ documentation paths mirrored
✅ All scripts functional and tested
✅ 85%+ code coverage achieved
✅ Comprehensive documentation complete
✅ GitHub Actions workflows configured
✅ Claude Code integration working
✅ Security review passed
✅ Clean environment test passed

TEST RESULTS:
- Total Tests: [Number]
- Passing: [Number] (100%)
- Coverage: [Percentage]% (≥85%)

PERFORMANCE METRICS:
- Fetch time (100 pages): [Time] (< 2 min target)
- Memory usage: [MB] (< 500 MB target)
- Search performance: [Time] (< 1 sec target)
- Path reachability: [Percentage]% (> 99% target)

SECURITY:
- No critical vulnerabilities
- All inputs sanitized
- No hardcoded credentials
- GitHub Actions secure

FILES CREATED:
[List key files]

FINAL STATUS:
🎉 PROJECT COMPLETE AND READY FOR PRODUCTION

CONFIRMED:
✅ IMPLEMENTATIONMONITOR.md fully updated
✅ All checkboxes marked complete
✅ Final sign-off completed

NEXT STEPS:
1. Commit final changes
2. Create release tag
3. Deploy to production
4. Monitor first automated update
```

**This marks the completion of the entire project!**
```

---

## General Guidelines for All Phases

### Before Starting Any Phase:

1. **Read the relevant section** in IMPLEMENTATION_PLAN.md
2. **Check prerequisites** in IMPLEMENTATIONMONITOR.md
3. **Understand deliverables** expected from the phase
4. **Prepare your environment** (tools, dependencies)

### During Phase Execution:

1. **Follow the template prompt** exactly
2. **Test as you go** - don't wait until the end
3. **Document issues** immediately
4. **Ask for clarification** if anything is unclear
5. **Verify each task** before moving to the next

### After Completing Each Phase:

1. **Test all deliverables** thoroughly
2. **Update IMPLEMENTATIONMONITOR.md** immediately
3. **Mark all checkboxes** as complete
4. **Fill in completion details** (date, duration, issues)
5. **Update overall progress** statistics
6. **Provide summary report**
7. **Confirm readiness** for next phase

### Using the Task Tool:

When invoking the Task tool with these prompts:

```
Use the Task tool with:
- subagent_type: "general-purpose"
- description: "Phase X: [Phase Name]"
- prompt: [Copy the template prompt for that phase]
```

Example:
```
Task(
  subagent_type="general-purpose",
  description="Phase 1: Repository Setup",
  prompt="[Paste the complete Phase 1 template prompt]"
)
```

### Critical Reminders:

⚠️ **ALWAYS** update IMPLEMENTATIONMONITOR.md after completing a phase
⚠️ **ALWAYS** test thoroughly before marking phase complete
⚠️ **ALWAYS** provide detailed completion reports
⚠️ **NEVER** skip validation steps
⚠️ **NEVER** move to next phase without completing current phase

---

## Troubleshooting

### If a Phase Fails:

1. Document the failure in IMPLEMENTATIONMONITOR.md notes
2. Identify the root cause
3. Fix the issue
4. Re-run validation
5. Update the monitor with resolution

### If Tests Fail:

1. Read the test failure message carefully
2. Fix the code or test
3. Re-run tests until passing
4. Update coverage report
5. Document in monitor

### If Integration Test Fails:

1. Check error logs
2. Verify all prerequisites met
3. Test components individually
4. Fix issues
5. Re-run full integration test

---

## Success Metrics

Track these throughout execution:

- **Tasks Completed**: X/28
- **Phases Completed**: X/7
- **Overall Progress**: X%
- **Test Coverage**: X%
- **Paths Mirrored**: X/550
- **Documentation Quality**: Pass/Fail
- **Performance**: Within targets Y/N
- **Security**: Issues found/resolved

---

## Final Checklist

Before declaring project complete:

- [ ] All 7 phases marked complete
- [ ] All 28 tasks completed
- [ ] IMPLEMENTATIONMONITOR.md fully updated
- [ ] All tests passing
- [ ] Coverage ≥ 85%
- [ ] Documentation complete
- [ ] Security review passed
- [ ] Clean environment test passed
- [ ] Final sign-off completed

---

**Document Version**: 1.0
**Last Updated**: 2025-11-03
**Status**: Ready for execution
**Next Action**: Begin with Phase 1 execution template
