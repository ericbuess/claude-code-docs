# Documentation Fetching Mechanism Analysis

**Script**: fetch_claude_docs.py (646 lines)
**Language**: Python 3.11+
**Dependencies**: requests==2.32.4 only
**Analysis Date**: 2025-11-03

## Overview

The fetching mechanism is a robust, production-ready system that:
1. Discovers documentation pages from sitemap.xml
2. Fetches markdown content from docs.anthropic.com
3. Validates content before saving
4. Tracks changes with SHA256 hashing
5. Generates comprehensive manifest
6. Handles errors gracefully with retries

## Script Inventory

### Primary Script: `fetch_claude_docs.py`

**Key Functions**:
- `discover_sitemap_and_base_url()` - Find sitemap and extract base URL
- `discover_claude_code_pages()` - Extract all Claude Code doc URLs from sitemap
- `fetch_markdown_content()` - Download markdown with retries
- `validate_markdown_content()` - Verify content is valid markdown
- `fetch_changelog()` - Fetch CHANGELOG.md from GitHub
- `load_manifest()` / `save_manifest()` - Manifest management
- `content_has_changed()` - SHA256-based change detection
- `url_to_safe_filename()` - Convert URL paths to safe filenames
- `cleanup_old_files()` - Remove obsolete files

**Configuration**:
```python
SITEMAP_URLS = [
    "https://docs.anthropic.com/sitemap.xml",
    "https://docs.anthropic.com/sitemap_index.xml",
    "https://anthropic.com/sitemap.xml"
]

HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/3.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

MAX_RETRIES = 3
RETRY_DELAY = 2  # initial delay in seconds
MAX_RETRY_DELAY = 30  # maximum delay
RATE_LIMIT_DELAY = 0.5  # delay between requests
```

## URL Construction Method

### Step 1: Discover Sitemap
```python
def discover_sitemap_and_base_url(session):
    for sitemap_url in SITEMAP_URLS:
        response = session.get(sitemap_url, headers=HEADERS, timeout=30)
        if response.status_code == 200:
            # Parse XML with security (forbid DTD, entities, external)
            root = ET.fromstring(response.content, parser=parser)
            # Extract first URL to determine base_url
            base_url = f"{parsed.scheme}://{parsed.netloc}"
            return sitemap_url, base_url
```

**Sitemap Discovery Strategy**:
1. Try primary sitemap: `docs.anthropic.com/sitemap.xml`
2. Fallback to sitemap index: `docs.anthropic.com/sitemap_index.xml`
3. Fallback to root sitemap: `anthropic.com/sitemap.xml`
4. Extract base URL from first valid URL found

### Step 2: Extract Claude Code Pages
```python
def discover_claude_code_pages(session, sitemap_url):
    # Parse sitemap XML
    root = ET.fromstring(response.content, parser=parser)

    # Filter for ENGLISH Claude Code docs only
    english_patterns = ['/en/docs/claude-code/']

    # Skip certain patterns
    skip_patterns = [
        '/tool-use/',
        '/examples/',
        '/legacy/',
        '/api/',
        '/reference/'
    ]

    # Extract matching URLs, remove duplicates, sort
    claude_code_pages = sorted(list(set(claude_code_pages)))
```

**Filtering Logic**:
- **Include**: `/en/docs/claude-code/` only (English Claude Code docs)
- **Exclude**: Tool-use, examples, legacy, API, reference pages
- **Result**: Clean list of paths like `/en/docs/claude-code/hooks`

### Step 3: Construct Markdown URLs
```python
def fetch_markdown_content(path, session, base_url):
    markdown_url = f"{base_url}{path}.md"
    # Example: https://docs.anthropic.com/en/docs/claude-code/hooks.md
```

**URL Pattern**:
- Base: `https://docs.anthropic.com`
- Path: `/en/docs/claude-code/hooks`
- Extension: `.md`
- Result: `https://docs.anthropic.com/en/docs/claude-code/hooks.md`

**Important**: The docs site serves markdown directly at `.md` URLs!

## HTML-to-Markdown Conversion

**Key Finding**: NO CONVERSION NEEDED!

The script fetches `.md` URLs directly:
```python
markdown_url = f"{base_url}{path}.md"
response = session.get(markdown_url, headers=HEADERS, timeout=30)
content = response.text
```

**Why This Works**:
- Anthropic's docs site serves raw markdown at `.md` URLs
- No HTML parsing required
- No markdown conversion libraries needed
- Clean, direct approach

**Content Validation**:
```python
def validate_markdown_content(content, filename):
    # Check it's not HTML
    if content.startswith('<!DOCTYPE') or '<html' in content[:100]:
        raise ValueError("Received HTML instead of markdown")

    # Check minimum length
    if len(content.strip()) < 50:
        raise ValueError(f"Content too short ({len(content)} bytes)")

    # Check for markdown indicators
    markdown_indicators = ['# ', '## ', '```', '- ', '[', '**', '_', '> ']
    indicator_count = count_indicators_in_first_50_lines(content)
    if indicator_count < 3:
        raise ValueError("Content doesn't appear to be markdown")

    # Check for documentation keywords
    doc_patterns = ['installation', 'usage', 'example', 'api', 'configuration', 'claude', 'code']
    if not any(pattern in content.lower() for pattern in doc_patterns):
        logger.warning(f"Content doesn't contain expected patterns")
```

## Error Handling Patterns

### Retry Logic with Exponential Backoff
```python
for attempt in range(MAX_RETRIES):
    try:
        response = session.get(markdown_url, headers=HEADERS, timeout=30)

        # Handle rate limiting
        if response.status_code == 429:
            wait_time = int(response.headers.get('Retry-After', 60))
            time.sleep(wait_time)
            continue

        response.raise_for_status()
        return filename, content

    except requests.exceptions.RequestException as e:
        if attempt < MAX_RETRIES - 1:
            # Exponential backoff with jitter
            delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
            jittered_delay = delay * random.uniform(0.5, 1.0)
            time.sleep(jittered_delay)
```

**Error Handling Features**:
- **Retry Attempts**: 3 max per request
- **Exponential Backoff**: 2s → 4s → 8s (up to 30s max)
- **Jitter**: Random 50-100% of delay to prevent thundering herd
- **Rate Limit Handling**: Respects `Retry-After` header
- **Timeout**: 30 seconds per request
- **Connection Pooling**: Uses `requests.Session()` for efficiency

### Validation Errors
```python
except ValueError as e:
    logger.error(f"Content validation failed for {filename}: {e}")
    raise
```

Validation failures are logged and re-raised (no retry for bad content).

## Rate Limiting Strategy

### Request Throttling
```python
RATE_LIMIT_DELAY = 0.5  # seconds between requests

for i, page_path in enumerate(documentation_pages, 1):
    # Fetch page
    filename, content = fetch_markdown_content(page_path, session, base_url)

    # Rate limiting (except on last page)
    if i < len(documentation_pages):
        time.sleep(RATE_LIMIT_DELAY)
```

**Strategy**:
- 0.5 second delay between requests
- No delay after last request
- Additional backoff on errors/rate limits

### Rate Limit Response Handling
```python
if response.status_code == 429:
    wait_time = int(response.headers.get('Retry-After', 60))
    logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
    time.sleep(wait_time)
    continue
```

## Change Detection

### SHA256 Hashing
```python
def content_has_changed(content, old_hash):
    new_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return new_hash != old_hash
```

**Process**:
1. Load old hash from manifest
2. Compute SHA256 of new content
3. Compare hashes
4. Only save file if hash differs
5. Only update timestamp if content changed

**Benefits**:
- Prevents unnecessary file writes
- Preserves git history (no commits if no changes)
- Accurate change tracking
- Efficient storage

## Filename Conversion

### URL Path to Filename
```python
def url_to_safe_filename(url_path):
    # Remove known prefixes
    for prefix in ['/en/docs/claude-code/', '/docs/claude-code/', '/claude-code/']:
        if prefix in url_path:
            path = url_path.split(prefix)[-1]
            break

    # If no subdirectories, just use filename
    if '/' not in path:
        return path + '.md'

    # For subdirectories, replace slashes with double underscores
    safe_name = path.replace('/', '__')
    if not safe_name.endswith('.md'):
        safe_name += '.md'
    return safe_name
```

**Examples**:
- `/en/docs/claude-code/hooks` → `hooks.md`
- `/en/docs/claude-code/advanced/setup` → `advanced__setup.md`
- `/en/docs/claude-code/sub/dir/page` → `sub__dir__page.md`

**Strategy**: Flat file structure with double-underscore for nested paths

## Dependencies and Libraries

### Python Standard Library
- `xml.etree.ElementTree` - XML parsing with security
- `hashlib` - SHA256 hashing
- `pathlib` - Path handling
- `logging` - Structured logging
- `datetime` - Timestamps
- `json` - Manifest file handling
- `urllib.parse` - URL parsing
- `os`, `sys`, `re`, `random`, `time` - Utilities

### External Dependencies
- **requests==2.32.4** ONLY
  - HTTP requests
  - Session management (connection pooling)
  - Retry handling
  - Timeout management

**No Additional Libraries Needed For**:
- HTML parsing (not needed - direct markdown fetch)
- Markdown conversion (not needed - already markdown)
- CLI parsing (not implemented in fetcher)

## Security Considerations

### XML Parsing Security
```python
try:
    # Prevent XXE attacks
    parser = ET.XMLParser(
        forbid_dtd=True,
        forbid_entities=True,
        forbid_external=True
    )
    root = ET.fromstring(response.content, parser=parser)
except TypeError:
    # Fallback for older Python versions
    logger.warning("XMLParser security parameters not available")
    root = ET.fromstring(response.content)
```

### Input Validation
- URL validation before fetching
- Content validation before saving
- Path sanitization for filenames
- Hash verification for integrity

### Safe File Operations
```python
def cleanup_old_files(docs_dir, current_files, manifest):
    # Only remove files previously fetched by this script
    previous_files = set(manifest.get("files", {}).keys())
    files_to_remove = previous_files - current_files
    # Never delete the manifest
    if filename == MANIFEST_FILE:
        continue
```

## Manifest Generation

### Manifest Structure
```python
new_manifest = {
    "files": {
        "filename.md": {
            "original_url": "https://docs.anthropic.com/path",
            "original_md_url": "https://docs.anthropic.com/path.md",
            "hash": "sha256...",
            "last_updated": "2025-11-03T12:00:00"
        }
    },
    "fetch_metadata": {
        "last_fetch_completed": "2025-11-03T12:05:00",
        "fetch_duration_seconds": 45.3,
        "total_pages_discovered": 47,
        "pages_fetched_successfully": 47,
        "pages_failed": 0,
        "failed_pages": [],
        "sitemap_url": "https://docs.anthropic.com/sitemap.xml",
        "base_url": "https://docs.anthropic.com",
        "total_files": 47,
        "fetch_tool_version": "3.0"
    },
    "base_url": "https://raw.githubusercontent.com/owner/repo/branch/docs/",
    "github_repository": "owner/repo",
    "github_ref": "main",
    "last_updated": "2025-11-03T12:05:00"
}
```

### Manifest Usage
1. **Change Detection**: Compare content hashes
2. **URL Mapping**: Link local files to official docs
3. **Status Tracking**: Last update times, fetch statistics
4. **Cleanup**: Identify obsolete files
5. **User Interface**: Generate topic lists

## Special Case: Changelog Fetching

### GitHub Repository Fetch
```python
def fetch_changelog(session):
    changelog_url = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"

    # Same retry/rate-limit logic as docs
    response = session.get(changelog_url, headers=HEADERS, timeout=30)

    # Add header to identify source
    header = """# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
>
> This is the official Claude Code release changelog...

---

"""
    content = header + response.text
    return "changelog.md", content
```

**Why Separate**:
- Different source (GitHub vs docs site)
- Different URL pattern (raw.githubusercontent.com)
- Special header annotation
- Independent versioning

## Logging and Output

### Structured Logging
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

**Log Levels Used**:
- `INFO`: Normal operation (fetching, saving, completion)
- `WARNING`: Non-fatal issues (retry, validation warnings)
- `ERROR`: Fatal errors (failed fetches, validation failures)

### Summary Report
```python
logger.info("\n" + "="*50)
logger.info(f"Fetch completed in {duration}")
logger.info(f"Discovered pages: {len(documentation_pages)}")
logger.info(f"Successful: {successful}/{len(documentation_pages)}")
logger.info(f"Failed: {failed}")

if failed_pages:
    logger.warning("\nFailed pages (will retry next run):")
    for page in failed_pages:
        logger.warning(f"  - {page}")
```

## Performance Characteristics

**Expected Performance**:
- ~50 pages at 0.5s/page = ~25 seconds base time
- Plus: retry delays, network latency, validation
- Total: 30-60 seconds for full fetch (when changes exist)
- When no changes: Very fast (hash comparison only)

**Optimization Techniques**:
- Session connection pooling
- SHA256 change detection (skip unchanged files)
- Parallel-ready design (could add concurrent fetching)
- Efficient XML parsing
- Minimal validation overhead

## Key Takeaways for Implementation

1. **Direct Markdown Fetching**: No HTML parsing/conversion needed
2. **Sitemap Discovery**: Dynamic page discovery vs hardcoded list
3. **Robust Error Handling**: Retries, backoff, rate limiting
4. **Change Detection**: SHA256 hashing prevents unnecessary writes
5. **Security**: XML parser hardening, input validation
6. **Logging**: Comprehensive, structured logging
7. **Manifest-Driven**: Rich metadata for all operations
8. **Single Dependency**: Only requests library needed
9. **Flat File Structure**: Simple, effective organization
10. **GitHub Integration**: Separate changelog fetching from GitHub
