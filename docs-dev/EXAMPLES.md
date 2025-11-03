# Usage Examples

Practical examples, troubleshooting guides, and frequently asked questions for the Claude Code Documentation Mirror.

## Table of Contents

- [Common Queries](#common-queries)
- [Content Search Examples](#content-search-examples)
- [Update Examples](#update-examples)
- [Validation Examples](#validation-examples)
- [Claude Code Integration](#claude-code-integration)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## Common Queries

### 1. Search for Prompt Engineering Documentation

```bash
$ python scripts/lookup_paths.py "prompt engineering"

Found 20 matches:

1. /en/docs/build-with-claude/prompt-engineering/overview (score: 95)
   Category: core_documentation

2. /en/docs/build-with-claude/prompt-engineering/be-clear-direct (score: 90)
   Category: core_documentation

3. /en/docs/build-with-claude/prompt-engineering/use-examples (score: 88)
   Category: core_documentation

4. /en/docs/build-with-claude/prompt-engineering/give-claude-tools (score: 85)
   Category: core_documentation

5. /en/docs/build-with-claude/prompt-engineering/think-step-by-step (score: 83)
   Category: core_documentation

... (15 more results)

Search completed in 47ms.
```

**Use Case**: Find all documentation related to prompt engineering techniques.

### 2. Find MCP Documentation

```bash
$ python scripts/lookup_paths.py "mcp"

Found 8 matches:

1. /en/docs/claude-code/mcp/overview (score: 100)
   Category: claude_code

2. /en/docs/claude-code/mcp/quickstart (score: 95)
   Category: claude_code

3. /en/docs/mcp/overview (score: 100)
   Category: core_documentation

4. /en/docs/mcp/quickstart (score: 95)
   Category: core_documentation

5. /en/docs/agents-and-tools/mcp (score: 90)
   Category: core_documentation

6. /en/docs/claude-code/advanced/mcp-integration (score: 85)
   Category: claude_code

7. /en/docs/mcp/built-in-servers (score: 80)
   Category: core_documentation

8. /en/docs/claude-code/platform/mcp-proxy (score: 75)
   Category: claude_code

Search completed in 38ms.
```

**Use Case**: Quickly locate Model Context Protocol documentation across different sections.

### 3. Search API Documentation

```bash
$ python scripts/lookup_paths.py "api messages"

Found 12 matches:

1. /en/api/messages (score: 100)
   Category: api_reference

2. /en/api/messages-examples (score: 95)
   Category: api_reference

3. /en/api/messages-streaming (score: 90)
   Category: api_reference

4. /en/docs/build-with-claude/messages-api (score: 85)
   Category: core_documentation

5. /en/api/batches (score: 75)
   Category: api_reference

... (7 more results)

Search completed in 42ms.
```

**Use Case**: Find all information about the Messages API.

### 4. Find Admin API Endpoints

```bash
$ python scripts/lookup_paths.py "admin api users"

Found 6 matches:

1. /en/api/admin-api/users/get-user (score: 98)
   Category: api_reference

2. /en/api/admin-api/users/list-users (score: 95)
   Category: api_reference

3. /en/api/admin-api/users/update-user (score: 93)
   Category: api_reference

4. /en/api/admin-api/users/remove-user (score: 90)
   Category: api_reference

5. /en/api/admin-api/overview (score: 75)
   Category: api_reference

6. /en/api/admin-api/authentication (score: 70)
   Category: api_reference

Search completed in 35ms.
```

**Use Case**: Find user management endpoints in the Admin API.

### 5. Search Prompt Library

```bash
$ python scripts/lookup_paths.py "code review"

Found 5 matches:

1. /en/prompt-library/code-consultant (score: 95)
   Category: prompt_library

2. /en/prompt-library/code-generator (score: 85)
   Category: prompt_library

3. /en/docs/claude-code/workflows/code-review (score: 90)
   Category: claude_code

4. /en/docs/agents-and-tools/tool-use/code-examples (score: 75)
   Category: core_documentation

5. /en/prompt-library/debugging-assistant (score: 70)
   Category: prompt_library

Search completed in 40ms.
```

**Use Case**: Find prompts and workflows for code review tasks.

## Content Search Examples

### 1. Search Document Content (Full-Text)

First, build the search index:

```bash
$ python scripts/build_search_index.py

Building search index from docs/...
Indexing 49 markdown files...
  ✓ /CAPABILITIES
  ✓ /EXAMPLES
  ✓ /amazon-bedrock
  ... (46 more files)

Indexing complete:
  Success: 49
  Errors: 0

============================================================
✅ SEARCH INDEX SAVED
   Output: docs/.search_index.json
   Files indexed: 49
   File size: 37.1 KB
============================================================
```

### 2. Search for "MCP" in Content

```bash
$ python scripts/lookup_paths.py --search-content "mcp"

Searching content for: 'mcp'

✅ Found 8 matching documents:

1. Connect Claude Code to tools via MCP (score: 135)
   Path: /mcp
   Keywords: mcp, servers, server, true, https
   Preview: # Connect Claude Code to tools via MCP  > Learn how to connect Claude Code to your tools with the Model Context Protocol...

2. Plugins (score: 20)
   Path: /plugins
   Keywords: plugin, plugins, step, create, see
   Preview: # Plugins  > Extend Claude Code with custom commands, agents, hooks, Skills, and MCP servers through the plugin system...

3. Claude Code Changelog (score: 15)
   Path: /changelog
   Keywords: claude, fixed, added, mcp, now
   Preview: # Claude Code Changelog  > **Source**: https://github.com/anthropics/claude-code...

... (5 more results)
```

**Use Case**: Find documents that mention MCP in their content, even if "mcp" isn't in the path.

### 3. Difference: Path Search vs Content Search

**Path Search** - Searches URL paths only:
```bash
$ python scripts/lookup_paths.py "prompt"

Found 20 results for query: 'prompt'
1. /en/docs/build-with-claude/prompt-engineering/overview
2. /en/prompt-library/code-consultant
...
```

**Content Search** - Searches document content:
```bash
$ python scripts/lookup_paths.py --search-content "prompt"

✅ Found 5 matching documents:
1. System Prompts (score: 120)
   - Finds documents with "prompt" in title, content, or keywords
   - Not limited to path names
```

**When to Use Which**:
- **Path search**: When you know the general topic/section (e.g., "api", "mcp", "prompt engineering")
- **Content search**: When looking for specific concepts mentioned in the content (e.g., "extended thinking", "batch processing")

## Update Examples

### 1. Update All Documentation

```bash
$ python scripts/main.py --update-all

Loading paths manifest...
Found 459 paths across 7 categories.

Fetching documentation:
[=====>              ] 25% (115/459)  ETA: 2m 45s

Current: /en/docs/build-with-claude/vision
Rate: 2.1 pages/sec
Elapsed: 55s

[====================] 100% (459/459)  Completed!

Summary:
┌─────────────────┬─────────┐
│ Metric          │ Count   │
├─────────────────┼─────────┤
│ Total Fetched   │ 459     │
│ Updated         │ 23      │
│ Unchanged       │ 436     │
│ Errors          │ 0       │
│ Time            │ 3m 42s  │
│ Avg per page    │ 0.48s   │
└─────────────────┴─────────┘

Updated paths (23):
  1. /en/api/messages (content changed)
  2. /en/docs/claude-code/mcp/overview (content changed)
  3. /en/docs/build-with-claude/prompt-engineering/overview (content changed)
  ... (20 more)

Successfully updated all documentation!
```

**Use Case**: Fetch or update all 459 documentation pages.

### 2. Update Specific Category

```bash
$ python scripts/main.py --update-category prompt_library

Loading paths manifest...
Category: prompt_library (64 paths)

Fetching documentation:
[====================] 100% (64/64)  Completed!

Summary:
- Fetched: 64 pages
- Updated: 3 pages
- Unchanged: 61 pages
- Errors: 0
- Time: 32.5s

Updated paths:
  1. /en/prompt-library/code-consultant
  2. /en/prompt-library/data-organizer
  3. /en/prompt-library/meeting-scribe

Successfully updated prompt_library category!
```

**Use Case**: Update only the prompt library (faster than full update).

### 3. Force Re-fetch (Ignore Cache)

```bash
$ python scripts/main.py --force --update-category api_reference

Loading paths manifest...
Category: api_reference (91 paths)

Force mode: Ignoring cache, re-fetching all pages.

Fetching documentation:
[====================] 100% (91/91)  Completed!

Summary:
- Fetched: 91 pages
- Updated: 91 pages (forced)
- Unchanged: 0 pages
- Errors: 0
- Time: 45.8s

All 91 pages have been re-fetched and saved.
```

**Use Case**: Force re-download even if pages haven't changed (e.g., after format change).

### 4. Verify Existing Documentation

```bash
$ python scripts/main.py --verify

Verifying existing documentation...

Checking manifest against files:
[====================] 100% (459/459)  Completed!

Verification Results:
┌──────────────────────────┬─────────┐
│ Status                   │ Count   │
├──────────────────────────┼─────────┤
│ Files present            │ 47      │
│ Files missing            │ 412     │
│ Extra files (not in map) │ 0       │
│ Manifest entries         │ 459     │
└──────────────────────────┴─────────┘

Missing files (first 10):
  1. /en/docs/build-with-claude/overview
  2. /en/docs/build-with-claude/prompt-engineering/overview
  3. /en/api/messages
  ... (402 more)

Recommendation: Run 'python scripts/main.py --update-all' to fetch missing files.
```

**Use Case**: Check which documentation files are missing locally.

## Validation Examples

### 1. Validate All Paths

```bash
$ python scripts/lookup_paths.py --validate-all

Validating 459 paths...

Using 10 parallel workers.

[====================] 100% (459/459)  Completed!

Validation Results:
┌────────────────────┬─────────┬────────┐
│ Status             │ Count   │ %      │
├────────────────────┼─────────┼────────┤
│ Reachable (200)    │ 457     │ 99.6%  │
│ Broken (404)       │ 2       │ 0.4%   │
│ Error              │ 0       │ 0.0%   │
└────────────────────┴─────────┴────────┘

Broken paths (2):
1. /en/docs/deprecated-page
   Status: 404 Not Found
   Suggestion: /en/docs/new-page

2. /en/api/old-endpoint
   Status: 404 Not Found
   Suggestion: /en/api/current-endpoint

Validation completed in 28.3s.
Report saved to: validation-2025-11-03.txt
```

**Use Case**: Check if all 459 paths are still accessible on docs.anthropic.com.

### 2. Check Specific Path

```bash
$ python scripts/lookup_paths.py --check /en/docs/build-with-claude/vision

Checking path: /en/docs/build-with-claude/vision

Result:
✓ Path is reachable
  Status: 200 OK
  URL: https://docs.anthropic.com/en/docs/build-with-claude/vision.md
  Response time: 234ms
  Content-Type: text/markdown; charset=utf-8
  Content-Length: 15,432 bytes

Path is valid and accessible.
```

**Use Case**: Verify a specific path is working before fetching.

### 3. Batch Validate from File

```bash
$ python scripts/lookup_paths.py --batch-validate paths.txt

Reading paths from: paths.txt
Found 25 paths to validate.

Validating paths:
[====================] 100% (25/25)  Completed!

Results:
- Reachable: 24 (96%)
- Broken: 1 (4%)

Broken paths:
1. /en/docs/test-page (404 Not Found)

Validation completed in 5.2s.
```

**Use Case**: Validate a custom list of paths (e.g., recently added paths).

## Claude Code Integration

### 1. Natural Language Documentation Search

```
> /docs how do I use tool use with Python?

Searching documentation for "tool use with Python"...

Found 5 relevant pages:

1. Tool Use Overview
   /en/docs/agents-and-tools/tool-use/overview
   Learn the basics of tool use with Claude, including schema definition and implementation.

2. Tool Use Examples (Python SDK)
   /en/api/agent-sdk/python-sdk/tool-use
   Complete Python examples for implementing tool use with the Anthropic SDK.

3. Multiple Tool Handling
   /en/docs/agents-and-tools/tool-use/multiple-tools
   How to handle multiple tools and choose between them.

4. Tool Use Best Practices
   /en/docs/agents-and-tools/tool-use/best-practices
   Best practices for designing and implementing tools.

5. Fine-grained Tool Streaming
   /en/docs/agents-and-tools/tool-use/fine-grained-tool-streaming
   Stream tool calls and responses for better user experience.

Would you like me to summarize any of these pages?
```

### 2. Update Documentation from Claude Code

```
> /update-docs

Triggering documentation update...

Running: python scripts/main.py --update-all

Fetching documentation:
[====================] 100% (459/459)

Summary:
- Updated: 15 pages
- Unchanged: 444 pages
- Time: 3m 45s

Documentation updated successfully!
```

### 3. Search Documentation Paths

```
> /search-docs "prompt engineering"

Searching paths for "prompt engineering"...

Found 20 matches:

1. /en/docs/build-with-claude/prompt-engineering/overview
2. /en/docs/build-with-claude/prompt-engineering/be-clear-direct
3. /en/docs/build-with-claude/prompt-engineering/use-examples
4. /en/docs/build-with-claude/prompt-engineering/give-claude-tools
5. /en/docs/build-with-claude/prompt-engineering/think-step-by-step
... (15 more)

Select a path to view, or ask me to summarize specific topics.
```

### 4. Validate Documentation

```
> /validate-docs

Running validation on 459 paths...

[====================] 100% (459/459)

Results:
- Reachable: 457 (99.6%)
- Broken: 2 (0.4%)

Broken paths:
1. /en/docs/deprecated-page (404)
2. /en/api/old-endpoint (404)

Validation complete. See report for details.
```

## Troubleshooting

### Issue 1: Documentation Out of Date

**Problem**: Local documentation doesn't match the online version.

**Symptoms**:
- Old examples
- Missing new features
- Deprecated content

**Solution 1: Force Update All**
```bash
python scripts/main.py --force --update-all
```

**Solution 2: Manual GitHub Actions Trigger**
1. Visit: https://github.com/costiash/claude-code-docs/actions
2. Click "Update Documentation" workflow
3. Click "Run workflow" button
4. Select branch and click "Run workflow"

**Solution 3: Check Last Update**
```bash
git log -1 --format="%H %aI %s" docs/
```

### Issue 2: Broken Links

**Problem**: Some documentation links return 404 errors.

**Symptoms**:
- "404 Not Found" errors
- Missing pages
- Dead links

**Solution 1: Validate All Paths**
```bash
python scripts/lookup_paths.py --validate-all
```

**Solution 2: Check Specific Path**
```bash
python scripts/lookup_paths.py --check /en/docs/specific-page
```

**Solution 3: View Validation Report**
```bash
cat validation-2025-11-03.txt
```

**Solution 4: Use Alternative Suggestions**
The validation output includes suggestions for broken links:
```
Broken: /en/docs/old-page (404)
Suggestion: /en/docs/new-page
```

### Issue 3: Slow Search

**Problem**: Path search takes too long.

**Symptoms**:
- Search > 1 second
- Sluggish response
- High CPU usage

**Solution 1: Rebuild Search Index**
```bash
python scripts/update_sitemap.py
```

**Solution 2: Clear Cache**
```bash
rm docs/.search_index.json
python scripts/update_sitemap.py
```

**Solution 3: Check Index Size**
```bash
ls -lh docs/.search_index.json
# Should be < 1 MB
```

### Issue 4: Tests Failing

**Problem**: pytest tests fail with errors.

**Symptoms**:
```
FAILED tests/unit/test_path_extraction.py::test_fetch_page
```

**Solution 1: Check Function Signatures**
```bash
# Current issue: fetch_page requires session parameter
# Update test:
def test_fetch_page(mock_session):
    result = fetch_page(url, session=mock_session)
```

**Solution 2: Run Specific Test**
```bash
pytest tests/unit/test_path_extraction.py::test_clean_path -v
```

**Solution 3: Check Test Status**
```bash
pytest --collect-only  # List all tests
pytest -v              # Run with verbose output
```

**Current Status**:
- 174 tests total
- 140 passing (85% pass rate)
- 24 failing (mostly signature mismatches)

### Issue 5: Import Errors

**Problem**: `ModuleNotFoundError` when running scripts.

**Symptoms**:
```
ModuleNotFoundError: No module named 'scripts'
```

**Solution 1: Install in Editable Mode**
```bash
pip install -e .
```

**Solution 2: Set PYTHONPATH**
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

**Solution 3: Check Installation**
```bash
pip list | grep claude-code-docs
```

### Issue 6: Rate Limiting

**Problem**: Getting HTTP 429 (Too Many Requests) errors.

**Symptoms**:
```
Error fetching /en/docs/page: 429 Too Many Requests
```

**Solution 1: Increase Delay**
Edit `scripts/main.py`:
```python
RATE_LIMIT_DELAY = 1.0  # Increase from 0.5 to 1.0
```

**Solution 2: Use Smaller Batches**
```bash
# Instead of --update-all, update by category:
python scripts/main.py --update-category core_documentation
# Wait a bit
python scripts/main.py --update-category api_reference
```

**Solution 3: Check Rate Limits**
```bash
# Current settings:
# - 0.5s delay between requests
# - ~120 requests per minute
# - Safe for docs.anthropic.com
```

### Issue 7: GitHub Actions Failing

**Problem**: Automated update workflow fails.

**Symptoms**:
- Red X on commits
- Workflow errors in Actions tab
- Email notifications

**Solution 1: Check Workflow Logs**
1. Go to: https://github.com/costiash/claude-code-docs/actions
2. Click on failed workflow
3. Review error logs

**Solution 2: Test Workflow Locally**
```bash
# Using act tool
act push

# Or manually run the commands
python scripts/main.py --update-all
```

**Solution 3: Check Permissions**
```yaml
# .github/workflows/update-docs.yml
permissions:
  contents: write  # Required for git push
```

## FAQ

### General Questions

#### Q: How often is documentation updated?

**A**: Every 3 hours via GitHub Actions. The workflow runs at:
- 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00 UTC

You can also trigger updates manually:
```bash
python scripts/main.py --update-all
```

#### Q: Can I use this offline?

**A**: Yes! After the initial fetch, all 459 documentation pages are stored locally in the `docs/` directory. No internet connection is required to:
- Search documentation
- Read documentation
- Use Claude Code `/docs` command (reads local files)

Only these operations require internet:
- Fetching/updating documentation
- Validating path reachability

#### Q: How much disk space does it use?

**A**: Approximately:
- Documentation files: ~15 MB (459 markdown files)
- Scripts and tests: ~500 KB
- Git history: ~5 MB
- **Total**: ~20 MB

Very efficient storage!

#### Q: Can I contribute new paths?

**A**: Yes! Follow these steps:

1. Add paths to `paths_manifest.json`:
```json
{
  "categories": {
    "your_category": [
      "/en/new/path",
      "/en/another/path"
    ]
  }
}
```

2. Run extraction:
```bash
python scripts/extract_paths.py --validate
```

3. Fetch new paths:
```bash
python scripts/main.py --update-all
```

4. Submit a pull request with:
   - Updated `paths_manifest.json`
   - Fetched documentation files
   - Updated documentation (README.md, CAPABILITIES.md)

See [DEVELOPMENT.md](../DEVELOPMENT.md) for detailed contribution guidelines.

#### Q: Does this work on Windows?

**A**: Yes! Python 3.12+ is supported on Windows, macOS, and Linux.

**Windows Installation**:
```powershell
# Clone repository
git clone https://github.com/costiash/claude-code-docs.git
cd claude-code-docs

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -e .
```

All scripts work on Windows with proper path handling.

#### Q: Can I customize which categories to mirror?

**A**: Yes! Use the `--update-category` option:

```bash
# Update only specific categories
python scripts/main.py --update-category core_documentation
python scripts/main.py --update-category api_reference
python scripts/main.py --update-category claude_code
python scripts/main.py --update-category prompt_library
python scripts/main.py --update-category resources
python scripts/main.py --update-category release_notes
```

Or edit `paths_manifest.json` to include only desired categories.

### Technical Questions

#### Q: What's the difference between this and upstream?

**A**: This enhanced edition adds:

| Feature | Upstream | Enhanced Edition |
|---------|----------|------------------|
| Path coverage | 47 pages | 459 pages (10x more) |
| Categories | 1 | 7 categories |
| Testing | None | 174 tests |
| Search | Basic | Fuzzy search + relevance ranking |
| Validation | None | Automated path validation |
| Documentation | Basic | Comprehensive (4 docs) |

See [README.md](../README.md) for detailed comparison.

#### Q: How do I run tests?

**A**:
```bash
# All tests (174 total)
pytest

# Specific suite
pytest tests/unit/              # 82 unit tests
pytest tests/integration/       # 36 integration tests
pytest tests/validation/        # 56 validation tests

# With coverage
pytest --cov=scripts --cov-report=html
open htmlcov/index.html
```

**Current Status**:
- Total: 174 tests
- Passing: 140 (85% pass rate)
- Coverage: 24% (target: 85%+)

#### Q: What's the test coverage?

**A**: Currently 24%, with a target of 85%+.

**Coverage by Module**:
- main.py: 30% (target: 90%)
- extract_paths.py: 45% (target: 85%)
- lookup_paths.py: 20% (target: 85%)
- update_sitemap.py: 15% (target: 80%)

See [DEVELOPMENT.md](../DEVELOPMENT.md) for improving coverage.

#### Q: How do I report issues?

**A**: Open an issue on GitHub with:

1. **Description**: Clear description of the problem
2. **Steps to reproduce**: Exact commands to reproduce
3. **Expected behavior**: What should happen
4. **Actual behavior**: What actually happens
5. **System information**:
   - OS and version
   - Python version
   - Repository commit/branch
   - Error messages and stack traces

**Issue Tracker**: https://github.com/costiash/claude-code-docs/issues

#### Q: Can I use this for other documentation sites?

**A**: Yes, but with modifications:

1. **Update base URL** in `scripts/main.py`:
```python
BASE_URL = "https://your-docs-site.com"
```

2. **Update path patterns** in `scripts/extract_paths.py`:
```python
def categorize_path(path: str) -> str:
    # Update categories for your site
    if path.startswith("/docs/"):
        return "documentation"
    # ... etc
```

3. **Test fetching**:
```bash
python scripts/main.py --verify
```

4. **Adjust rate limiting** if needed:
```python
RATE_LIMIT_DELAY = 1.0  # Adjust based on site's limits
```

### Implementation Questions

#### Q: Why direct markdown fetching instead of HTML scraping?

**A**: Phase 1 analysis discovered that `docs.anthropic.com` serves markdown directly at `.md` URLs:

```python
# Old approach (not needed):
url = "https://docs.anthropic.com/en/docs/page"
html = fetch_html(url)
markdown = convert_html_to_markdown(html)  # Complex!

# New approach (simple):
url = "https://docs.anthropic.com/en/docs/page.md"
markdown = fetch_markdown(url)  # Direct!
```

**Benefits**:
- No HTML parsing needed (no BeautifulSoup4)
- No markdown conversion (no markdownify)
- Faster fetching
- More accurate content
- Simpler code

#### Q: How does change detection work?

**A**: SHA256-based hash comparison:

```python
def content_has_changed(path: str, new_content: str, manifest: dict) -> bool:
    """Check if content has changed using SHA256 hash"""
    new_hash = hashlib.sha256(new_content.encode()).hexdigest()
    old_hash = manifest.get(path, {}).get('hash', '')
    return new_hash != old_hash
```

**Benefits**:
- Only fetches changed pages
- Saves bandwidth
- Faster updates
- Accurate change detection

#### Q: What's the retry logic?

**A**: Exponential backoff with 3 retries:

```python
@retry_with_exponential_backoff(max_retries=3)
def fetch_page(url: str, session: requests.Session) -> str:
    # Attempt 1: immediate
    # Attempt 2: wait 1 second
    # Attempt 3: wait 2 seconds
    # Attempt 4 (final): wait 4 seconds
```

**Handles**:
- Transient network errors
- Temporary server issues
- Rate limiting (429 errors)
- Connection timeouts

---

**Last Updated**: 2025-11-03

**Version**: 0.1.0

**Need more help?** See [DEVELOPMENT.md](../DEVELOPMENT.md) or open an issue!
