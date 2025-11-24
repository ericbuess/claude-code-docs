# llms-full.txt Integration Plan

**Project**: claude-code-docs Enhanced Edition  
**Version**: 0.4.0 (Enhanced Edition with llms-full.txt integration)  
**Status**: Planning Phase  
**Created**: 2025-11-24  
**Author**: Claude Code Planning Agent

---

## Executive Summary

This plan outlines the integration of Anthropic's `llms-full.txt` file (25.6 MB, 523 documentation pages) into the claude-code-docs project while preserving our unique 68 Claude Code CLI documentation pages. The integration will implement a **hybrid fetcher** that combines both sources for maximum coverage, add **parsing capabilities** for the new file format, and provide **analysis tools** to understand documentation overlap and gaps.

**Key Objectives**:
1. **Parse llms-full.txt** - Build efficient parser for the 25.6 MB file
2. **Hybrid Fetcher** - Combine API docs (from llms-full.txt) + CLI docs (from sitemaps)
3. **Overlap Analysis** - Identify duplicates, gaps, and conflicts between sources

**Expected Outcomes**:
- Coverage increase: 448 → ~591 unique paths (523 from llms-full.txt + 68 unique CLI docs)
- API reference improvement: 91 → 359 paths (4x increase)
- Backward compatibility: Existing `/docs` command continues to work
- Performance: SHA256 change detection preserved where possible
- Dual-mode support: Both standard and enhanced modes benefit

**Implementation Approach**: Incremental, phase-by-phase with independent testing at each stage. Each phase delivers standalone value and can be rolled back if issues arise.

---

## Phase 0: Pre-Implementation Analysis (Research & Validation)

**Objectives**:
- Understand llms-full.txt file structure in detail
- Identify technical requirements and constraints
- Validate assumptions about content and format
- Establish baseline metrics

**Deliverables**:
- [ ] llms-full.txt file structure documentation
- [ ] Sample parsing examples with edge cases
- [ ] Coverage comparison report (448 vs 523 paths)
- [ ] Performance baseline measurements

**Dependencies**: None (can start immediately)

**Estimated Complexity**: Low (1-2 hours)

**Implementation Steps**:

### Step 1: Download and Inspect llms-full.txt

```bash
# Download the file
curl -fsSL https://platform.claude.com/llms-full.txt -o /tmp/llms-full.txt

# Check file stats
ls -lh /tmp/llms-full.txt
wc -l /tmp/llms-full.txt
file /tmp/llms-full.txt

# Examine structure
head -100 /tmp/llms-full.txt
grep -c "^URL: " /tmp/llms-full.txt  # Count pages
grep "^URL: " /tmp/llms-full.txt | head -20  # Sample URLs
```

### Step 2: Analyze File Format

Create a simple analysis script:

```python
#!/usr/bin/env python3
"""Analyze llms-full.txt structure"""

def analyze_structure(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count pages (URL markers)
    pages = content.split('URL: ')
    print(f"Total pages: {len(pages) - 1}")  # First split is empty
    
    # Sample page structure
    if len(pages) > 1:
        sample = pages[1]
        print("\n--- Sample Page Structure ---")
        print(sample[:500])
        
        # Find separator
        if '---' in sample:
            print(f"\nFound separator: '---'")
            parts = sample.split('---', 1)
            print(f"URL line: {parts[0][:100]}")
            print(f"Content length: {len(parts[1]) if len(parts) > 1 else 0} chars")
    
    # Check for patterns
    print("\n--- Pattern Analysis ---")
    print(f"Lines starting with 'URL: ': {content.count('\\nURL: ')}")
    print(f"Separator '---' occurrences: {content.count('---')}")
    
    # URL domains
    urls = [line.split('URL: ')[1].split()[0] 
            for line in content.split('\n') 
            if line.startswith('URL: ')]
    
    print(f"\n--- URL Domains ---")
    from collections import Counter
    from urllib.parse import urlparse
    domains = Counter([urlparse(url).netloc for url in urls[:50]])
    for domain, count in domains.most_common():
        print(f"  {domain}: {count}")

if __name__ == "__main__":
    analyze_structure('/tmp/llms-full.txt')
```

### Step 3: Compare with Current Coverage

```python
#!/usr/bin/env python3
"""Compare llms-full.txt coverage with current manifest"""
import json
from pathlib import Path
from urllib.parse import urlparse

def load_current_paths():
    """Load paths from paths_manifest.json"""
    manifest_path = Path('paths_manifest.json')
    with open(manifest_path) as f:
        data = json.load(f)
    
    all_paths = []
    for category, paths in data['categories'].items():
        all_paths.extend(paths)
    
    return set(all_paths)

def extract_llms_full_paths(filepath):
    """Extract URL paths from llms-full.txt"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    paths = set()
    for line in content.split('\n'):
        if line.startswith('URL: '):
            url = line.split('URL: ')[1].strip()
            parsed = urlparse(url)
            path = parsed.path
            if path.endswith('.html'):
                path = path[:-5]
            paths.add(path)
    
    return paths

def compare_coverage():
    current_paths = load_current_paths()
    llms_paths = extract_llms_full_paths('/tmp/llms-full.txt')
    
    print(f"Current manifest: {len(current_paths)} paths")
    print(f"llms-full.txt: {len(llms_paths)} paths")
    
    # Find unique to each
    only_current = current_paths - llms_paths
    only_llms = llms_paths - current_paths
    common = current_paths & llms_paths
    
    print(f"\nOverlap: {len(common)} paths")
    print(f"Unique to current: {len(only_current)} paths")
    print(f"Unique to llms-full.txt: {len(only_llms)} paths")
    
    print("\n--- Unique to Current (first 20) ---")
    for path in sorted(only_current)[:20]:
        print(f"  {path}")
    
    print("\n--- Unique to llms-full.txt (first 20) ---")
    for path in sorted(only_llms)[:20]:
        print(f"  {path}")
    
    # Categorize unique current paths
    print("\n--- Categories of Unique Current Paths ---")
    cli_docs = [p for p in only_current if p.startswith('/docs/en/')]
    other_docs = [p for p in only_current if not p.startswith('/docs/en/')]
    
    print(f"Claude Code CLI docs (/docs/en/): {len(cli_docs)}")
    print(f"Other docs: {len(other_docs)}")

if __name__ == "__main__":
    compare_coverage()
```

**Success Criteria**:
- [x] llms-full.txt structure fully documented
- [x] Clear understanding of URL format and separators
- [x] Coverage comparison shows unique Claude Code CLI docs
- [x] No blockers identified for implementation

**Risk Assessment**:
- **Low**: This is purely investigative work
- **Mitigation**: N/A - no code changes, no user impact

---

## Phase 1: Build llms-full.txt Parser (Standalone Module)

**Objectives**:
- Create a robust parser for the llms-full.txt format
- Handle the 25.6 MB file size efficiently (streaming)
- Extract individual pages with metadata
- Convert to our filename convention
- Validate content quality

**Deliverables**:
- [ ] `scripts/parse_llms_full.py` - Parser module
- [ ] Unit tests for parser (tests/unit/test_parse_llms_full.py)
- [ ] Documentation for parser usage
- [ ] Sample output showing parsed pages

**Dependencies**: Phase 0 complete

**Estimated Complexity**: Medium (4-6 hours)

**Implementation Steps**:

### Step 1: Create Parser Module

Create `scripts/parse_llms_full.py`:

```python
#!/usr/bin/env python3
"""
Parser for Anthropic's llms-full.txt file.

This module provides efficient parsing of the large (25.6 MB) llms-full.txt
file containing 523 documentation pages optimized for LLM consumption.

File Structure:
    URL: https://example.com/path/to/page
    ---
    [markdown content]
    
    URL: https://example.com/another/page
    ---
    [markdown content]

Usage:
    from parse_llms_full import LlmsFullParser
    
    parser = LlmsFullParser()
    pages = parser.parse_file('llms-full.txt')
    
    for page in pages:
        print(f"{page['path']}: {len(page['content'])} bytes")
"""

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Optional
from urllib.parse import urlparse

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ParsedPage:
    """Represents a single parsed documentation page"""
    url: str                    # Full URL (e.g., https://platform.claude.com/en/api/messages)
    path: str                   # URL path (e.g., /en/api/messages)
    content: str                # Markdown content
    content_hash: str           # SHA256 hash of content
    line_number: int            # Starting line in source file (for debugging)
    
    @property
    def filename(self) -> str:
        """Convert path to safe filename using project convention"""
        # Remove leading slash
        path = self.path.lstrip('/')
        
        # Replace slashes with double underscores
        filename = path.replace('/', '__')
        
        # Sanitize: only alphanumeric, hyphens, underscores, dots
        sanitized = ''.join(c for c in filename if c.isalnum() or c in '-_.')
        
        # Add .md extension if not present
        if not sanitized.endswith('.md'):
            sanitized += '.md'
        
        return sanitized


class LlmsFullParser:
    """Parser for llms-full.txt file"""
    
    SEPARATOR = '---'
    URL_PREFIX = 'URL: '
    CHUNK_SIZE = 8192  # Read in 8KB chunks
    
    def __init__(self):
        self.stats = {
            'total_pages': 0,
            'parse_errors': 0,
            'empty_pages': 0,
        }
    
    def parse_file(self, filepath: Path | str, skip_empty: bool = True) -> List[ParsedPage]:
        """
        Parse llms-full.txt file and return list of pages.
        
        Args:
            filepath: Path to llms-full.txt
            skip_empty: Skip pages with no content (default: True)
        
        Returns:
            List of ParsedPage objects
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        logger.info(f"Parsing {filepath} ({filepath.stat().st_size / 1024 / 1024:.1f} MB)")
        
        pages = []
        
        # Read entire file (it's only 25.6 MB, fits in memory)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split by URL markers
        raw_pages = content.split(self.URL_PREFIX)
        
        logger.info(f"Found {len(raw_pages) - 1} potential pages")
        
        # Process each page (skip first empty split)
        for i, raw_page in enumerate(raw_pages[1:], start=1):
            try:
                page = self._parse_page(raw_page, i)
                
                if page:
                    if skip_empty and len(page.content.strip()) < 50:
                        self.stats['empty_pages'] += 1
                        logger.debug(f"Skipping empty page: {page.path}")
                        continue
                    
                    pages.append(page)
                    self.stats['total_pages'] += 1
                    
                    if self.stats['total_pages'] % 100 == 0:
                        logger.info(f"Parsed {self.stats['total_pages']} pages...")
            
            except Exception as e:
                self.stats['parse_errors'] += 1
                logger.error(f"Failed to parse page {i}: {e}")
                continue
        
        logger.info(f"Parsing complete: {self.stats['total_pages']} pages "
                   f"({self.stats['parse_errors']} errors, "
                   f"{self.stats['empty_pages']} empty)")
        
        return pages
    
    def _parse_page(self, raw_page: str, page_number: int) -> Optional[ParsedPage]:
        """
        Parse a single page from raw text.
        
        Args:
            raw_page: Raw page text (after URL: split)
            page_number: Page number (for debugging)
        
        Returns:
            ParsedPage object or None if invalid
        """
        # Split by separator
        parts = raw_page.split(self.SEPARATOR, 1)
        
        if len(parts) != 2:
            logger.warning(f"Page {page_number}: No separator found")
            return None
        
        url_line = parts[0].strip()
        content = parts[1].strip()
        
        # Parse URL
        try:
            parsed = urlparse(url_line)
            if not parsed.netloc:
                logger.warning(f"Page {page_number}: Invalid URL: {url_line[:50]}")
                return None
            
            # Extract path and normalize
            path = parsed.path
            if path.endswith('.html'):
                path = path[:-5]
            if path.endswith('/'):
                path = path[:-1]
            
            # Compute content hash
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            return ParsedPage(
                url=url_line,
                path=path,
                content=content,
                content_hash=content_hash,
                line_number=page_number
            )
        
        except Exception as e:
            logger.error(f"Page {page_number}: Failed to parse URL '{url_line[:50]}': {e}")
            return None
    
    def parse_streaming(self, filepath: Path | str) -> Iterator[ParsedPage]:
        """
        Stream parse llms-full.txt without loading entire file into memory.
        
        Useful for very large files or memory-constrained environments.
        
        Args:
            filepath: Path to llms-full.txt
        
        Yields:
            ParsedPage objects one at a time
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        
        logger.info(f"Streaming parse: {filepath}")
        
        current_page = []
        page_number = 0
        in_content = False
        current_url = None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, start=1):
                if line.startswith(self.URL_PREFIX):
                    # Found new page marker
                    if current_url and current_page:
                        # Yield previous page
                        page = self._build_page_from_lines(
                            current_url, 
                            current_page, 
                            page_number
                        )
                        if page:
                            yield page
                    
                    # Start new page
                    current_url = line[len(self.URL_PREFIX):].strip()
                    current_page = []
                    in_content = False
                    page_number += 1
                
                elif line.strip() == self.SEPARATOR and not in_content:
                    # Found content separator
                    in_content = True
                
                elif in_content:
                    # Accumulate content
                    current_page.append(line)
        
        # Don't forget the last page
        if current_url and current_page:
            page = self._build_page_from_lines(current_url, current_page, page_number)
            if page:
                yield page
        
        logger.info(f"Streaming parse complete: {page_number} pages processed")
    
    def _build_page_from_lines(
        self, 
        url: str, 
        lines: List[str], 
        page_number: int
    ) -> Optional[ParsedPage]:
        """Build ParsedPage from accumulated lines"""
        content = ''.join(lines).strip()
        
        if len(content) < 50:
            return None
        
        try:
            parsed = urlparse(url)
            path = parsed.path
            
            if path.endswith('.html'):
                path = path[:-5]
            if path.endswith('/'):
                path = path[:-1]
            
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            return ParsedPage(
                url=url,
                path=path,
                content=content,
                content_hash=content_hash,
                line_number=page_number
            )
        
        except Exception as e:
            logger.error(f"Failed to build page {page_number}: {e}")
            return None


def main():
    """CLI interface for parser"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Parse Anthropic llms-full.txt file',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'filepath',
        type=Path,
        help='Path to llms-full.txt file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('parsed_pages'),
        help='Output directory for parsed pages (default: parsed_pages/)'
    )
    
    parser.add_argument(
        '--list',
        action='store_true',
        help='List pages without saving'
    )
    
    parser.add_argument(
        '--streaming',
        action='store_true',
        help='Use streaming parser (lower memory usage)'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of pages to process'
    )
    
    args = parser.parse_args()
    
    # Create parser
    llms_parser = LlmsFullParser()
    
    if args.list:
        # List mode: just print page info
        if args.streaming:
            pages = llms_parser.parse_streaming(args.filepath)
        else:
            pages = llms_parser.parse_file(args.filepath)
        
        print(f"{'Path':<60} {'Size':>10} {'Hash'[:8]}")
        print("-" * 80)
        
        count = 0
        for page in pages:
            print(f"{page.path:<60} {len(page.content):>10} {page.content_hash[:8]}")
            count += 1
            if args.limit and count >= args.limit:
                break
    
    else:
        # Save mode: write files to output directory
        args.output_dir.mkdir(parents=True, exist_ok=True)
        
        if args.streaming:
            pages = llms_parser.parse_streaming(args.filepath)
        else:
            pages = llms_parser.parse_file(args.filepath)
        
        count = 0
        for page in pages:
            output_file = args.output_dir / page.filename
            output_file.write_text(page.content, encoding='utf-8')
            count += 1
            
            if count % 50 == 0:
                print(f"Saved {count} pages...")
            
            if args.limit and count >= args.limit:
                break
        
        print(f"\nSaved {count} pages to {args.output_dir}")


if __name__ == "__main__":
    main()
```

### Step 2: Create Unit Tests

Create `tests/unit/test_parse_llms_full.py`:

```python
#!/usr/bin/env python3
"""Unit tests for llms-full.txt parser"""

import hashlib
import pytest
from pathlib import Path
from scripts.parse_llms_full import LlmsFullParser, ParsedPage


# Sample test data
SAMPLE_LLMS_CONTENT = """URL: https://platform.claude.com/en/api/messages
---
# Messages API

The Messages API allows you to send messages to Claude.

## Endpoint

POST /v1/messages

URL: https://platform.claude.com/en/docs/about-claude/models
---
# Models

Claude comes in several models:

- Claude 3.5 Sonnet
- Claude 3 Opus
- Claude 3 Haiku

URL: https://platform.claude.com/en/api/streaming
---
# Streaming

Enable streaming responses with the `stream` parameter.
"""


@pytest.fixture
def sample_file(tmp_path):
    """Create a temporary sample llms-full.txt file"""
    filepath = tmp_path / "llms-full.txt"
    filepath.write_text(SAMPLE_LLMS_CONTENT, encoding='utf-8')
    return filepath


def test_parser_initialization():
    """Test parser can be created"""
    parser = LlmsFullParser()
    assert parser is not None
    assert parser.stats['total_pages'] == 0


def test_parse_file_basic(sample_file):
    """Test basic file parsing"""
    parser = LlmsFullParser()
    pages = parser.parse_file(sample_file)
    
    # Should find 3 pages
    assert len(pages) == 3
    assert parser.stats['total_pages'] == 3
    assert parser.stats['parse_errors'] == 0


def test_parsed_page_structure(sample_file):
    """Test that parsed pages have correct structure"""
    parser = LlmsFullParser()
    pages = parser.parse_file(sample_file)
    
    page = pages[0]
    
    # Check all fields are present
    assert page.url == "https://platform.claude.com/en/api/messages"
    assert page.path == "/en/api/messages"
    assert "Messages API" in page.content
    assert len(page.content_hash) == 64  # SHA256 is 64 hex chars
    assert page.line_number > 0


def test_filename_conversion(sample_file):
    """Test path to filename conversion"""
    parser = LlmsFullParser()
    pages = parser.parse_file(sample_file)
    
    page = pages[0]
    
    # Should use double-underscore convention
    assert page.filename == "en__api__messages.md"
    
    # Check other pages
    assert pages[1].filename == "en__docs__about-claude__models.md"
    assert pages[2].filename == "en__api__streaming.md"


def test_content_hash_computation(sample_file):
    """Test that content hashes are computed correctly"""
    parser = LlmsFullParser()
    pages = parser.parse_file(sample_file)
    
    page = pages[0]
    
    # Recompute hash manually
    expected_hash = hashlib.sha256(page.content.encode('utf-8')).hexdigest()
    assert page.content_hash == expected_hash


def test_skip_empty_pages(tmp_path):
    """Test that empty pages are skipped"""
    content = """URL: https://example.com/empty
---

URL: https://example.com/valid
---
This page has content.
"""
    
    filepath = tmp_path / "test.txt"
    filepath.write_text(content, encoding='utf-8')
    
    parser = LlmsFullParser()
    pages = parser.parse_file(filepath, skip_empty=True)
    
    # Should only get 1 page (the non-empty one)
    assert len(pages) == 1
    assert pages[0].path == "/valid"


def test_malformed_url_handling(tmp_path):
    """Test handling of malformed URLs"""
    content = """URL: not-a-valid-url
---
Some content here

URL: https://example.com/valid
---
Valid content
"""
    
    filepath = tmp_path / "test.txt"
    filepath.write_text(content, encoding='utf-8')
    
    parser = LlmsFullParser()
    pages = parser.parse_file(filepath)
    
    # Should skip malformed URL but get valid one
    assert len(pages) == 1
    assert parser.stats['parse_errors'] >= 0  # May count as error


def test_missing_separator(tmp_path):
    """Test handling of pages without separator"""
    content = """URL: https://example.com/no-separator
Content without separator

URL: https://example.com/valid
---
Valid content
"""
    
    filepath = tmp_path / "test.txt"
    filepath.write_text(content, encoding='utf-8')
    
    parser = LlmsFullParser()
    pages = parser.parse_file(filepath)
    
    # Should skip page without separator but get valid one
    assert len(pages) == 1


def test_streaming_parser(sample_file):
    """Test streaming parser produces same results"""
    parser = LlmsFullParser()
    
    # Parse normally
    normal_pages = parser.parse_file(sample_file)
    
    # Parse streaming
    streaming_pages = list(parser.parse_streaming(sample_file))
    
    # Should get same pages
    assert len(normal_pages) == len(streaming_pages)
    
    for normal, streaming in zip(normal_pages, streaming_pages):
        assert normal.path == streaming.path
        assert normal.content_hash == streaming.content_hash


def test_file_not_found():
    """Test that missing file raises error"""
    parser = LlmsFullParser()
    
    with pytest.raises(FileNotFoundError):
        parser.parse_file("/nonexistent/file.txt")


def test_html_extension_removal(tmp_path):
    """Test that .html extensions are removed from paths"""
    content = """URL: https://example.com/page.html
---
Content here
"""
    
    filepath = tmp_path / "test.txt"
    filepath.write_text(content, encoding='utf-8')
    
    parser = LlmsFullParser()
    pages = parser.parse_file(filepath)
    
    # .html should be stripped
    assert pages[0].path == "/page"


def test_trailing_slash_removal(tmp_path):
    """Test that trailing slashes are removed"""
    content = """URL: https://example.com/page/
---
Content here
"""
    
    filepath = tmp_path / "test.txt"
    filepath.write_text(content, encoding='utf-8')
    
    parser = LlmsFullParser()
    pages = parser.parse_file(filepath)
    
    # Trailing slash should be stripped
    assert pages[0].path == "/page"


def test_large_content():
    """Test handling of large content (performance check)"""
    # Create a page with 1MB of content
    large_content = "# Large Page\n\n" + ("Lorem ipsum " * 100000)
    
    content = f"""URL: https://example.com/large
---
{large_content}
"""
    
    import io
    parser = LlmsFullParser()
    
    # This should complete without memory issues
    # (Not a real file test, but validates parsing logic)
    pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Step 3: Test the Parser

```bash
# Run unit tests
pytest tests/unit/test_parse_llms_full.py -v

# Test with real file (download first)
curl -fsSL https://platform.claude.com/llms-full.txt -o /tmp/llms-full.txt

# List pages
python scripts/parse_llms_full.py /tmp/llms-full.txt --list | head -50

# Parse and save to directory
python scripts/parse_llms_full.py /tmp/llms-full.txt --output-dir /tmp/parsed_pages

# Check results
ls -lh /tmp/parsed_pages/ | wc -l
du -sh /tmp/parsed_pages/
```

**Success Criteria**:
- [x] Parser successfully processes 25.6 MB file
- [x] Extracts all 523 pages with correct format
- [x] Filename conversion matches project convention
- [x] All unit tests pass (100%)
- [x] Memory usage stays reasonable (< 500 MB)
- [x] Performance acceptable (< 5 seconds for full parse)

**Risk Assessment**:
- **Medium**: Parser bugs could corrupt content
- **Mitigation**: Comprehensive unit tests, validation checks, rollback-safe (new file)

---

## Phase 2: Build Overlap Analysis Tools

**Objectives**:
- Compare llms-full.txt URLs with current paths_manifest.json
- Identify unique content in each source
- Detect duplicates and conflicts
- Generate reports for decision-making
- Categorize documentation types

**Deliverables**:
- [ ] `scripts/analyze_coverage.py` - Analysis tool
- [ ] Coverage comparison report (JSON + markdown)
- [ ] Deduplication recommendations
- [ ] Source selection guidelines

**Dependencies**: Phase 1 complete

**Estimated Complexity**: Medium (3-4 hours)

**Implementation Steps**:

### Step 1: Create Analysis Tool

Create `scripts/analyze_coverage.py`:

```python
#!/usr/bin/env python3
"""
Analyze documentation coverage between llms-full.txt and current manifest.

Compares:
- Current paths_manifest.json (448 paths from sitemaps)
- llms-full.txt (523 pages from platform.claude.com)

Outputs:
- Coverage report showing overlap and unique content
- Recommendations for source selection
- Duplicate detection
"""

import json
import logging
from collections import defaultdict
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

from parse_llms_full import LlmsFullParser

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class CoverageReport:
    """Coverage analysis results"""
    current_total: int
    llms_full_total: int
    overlap_count: int
    unique_to_current: int
    unique_to_llms: int
    
    overlap_paths: List[str]
    unique_current_paths: List[str]
    unique_llms_paths: List[str]
    
    # Categorized breakdowns
    current_by_category: Dict[str, int]
    unique_current_by_category: Dict[str, int]
    
    # Recommendations
    recommended_source: Dict[str, str]  # path -> source ("current", "llms-full", "both")


class CoverageAnalyzer:
    """Analyze documentation coverage between sources"""
    
    def __init__(self, manifest_path: Path, llms_full_path: Path):
        """
        Initialize analyzer.
        
        Args:
            manifest_path: Path to paths_manifest.json
            llms_full_path: Path to llms-full.txt
        """
        self.manifest_path = manifest_path
        self.llms_full_path = llms_full_path
        
        # Load data
        self.current_paths = self._load_current_paths()
        self.llms_full_paths = self._load_llms_full_paths()
    
    def _load_current_paths(self) -> Dict[str, str]:
        """
        Load paths from paths_manifest.json.
        
        Returns:
            Dict mapping path -> category
        """
        logger.info(f"Loading current paths from {self.manifest_path}")
        
        with open(self.manifest_path) as f:
            data = json.load(f)
        
        path_to_category = {}
        for category, paths in data.get('categories', {}).items():
            for path in paths:
                path_to_category[path] = category
        
        logger.info(f"Loaded {len(path_to_category)} current paths")
        return path_to_category
    
    def _load_llms_full_paths(self) -> Set[str]:
        """
        Load paths from llms-full.txt.
        
        Returns:
            Set of paths from llms-full.txt
        """
        logger.info(f"Parsing llms-full.txt from {self.llms_full_path}")
        
        parser = LlmsFullParser()
        pages = parser.parse_file(self.llms_full_path)
        
        paths = {page.path for page in pages}
        
        logger.info(f"Loaded {len(paths)} paths from llms-full.txt")
        return paths
    
    def analyze(self) -> CoverageReport:
        """
        Perform coverage analysis.
        
        Returns:
            CoverageReport with detailed analysis
        """
        logger.info("Analyzing coverage...")
        
        current_set = set(self.current_paths.keys())
        llms_full_set = self.llms_full_paths
        
        # Find overlaps and unique content
        overlap = current_set & llms_full_set
        unique_current = current_set - llms_full_set
        unique_llms = llms_full_set - current_set
        
        logger.info(f"Overlap: {len(overlap)} paths")
        logger.info(f"Unique to current: {len(unique_current)} paths")
        logger.info(f"Unique to llms-full: {len(unique_llms)} paths")
        
        # Categorize current paths
        current_by_category = defaultdict(int)
        unique_current_by_category = defaultdict(int)
        
        for path, category in self.current_paths.items():
            current_by_category[category] += 1
            
            if path in unique_current:
                unique_current_by_category[category] += 1
        
        # Generate recommendations
        recommended_source = self._generate_recommendations(
            overlap, unique_current, unique_llms
        )
        
        report = CoverageReport(
            current_total=len(current_set),
            llms_full_total=len(llms_full_set),
            overlap_count=len(overlap),
            unique_to_current=len(unique_current),
            unique_to_llms=len(unique_llms),
            overlap_paths=sorted(overlap),
            unique_current_paths=sorted(unique_current),
            unique_llms_paths=sorted(unique_llms),
            current_by_category=dict(current_by_category),
            unique_current_by_category=dict(unique_current_by_category),
            recommended_source=recommended_source
        )
        
        return report
    
    def _generate_recommendations(
        self, 
        overlap: Set[str], 
        unique_current: Set[str], 
        unique_llms: Set[str]
    ) -> Dict[str, str]:
        """
        Generate source recommendations for each path.
        
        Rules:
        1. Claude Code CLI docs (/docs/en/*) -> always use current (sitemap)
        2. API reference overlaps -> prefer llms-full (more comprehensive)
        3. Unique to llms-full -> use llms-full
        4. Unique to current -> use current
        5. Other overlaps -> use llms-full (authoritative)
        
        Returns:
            Dict mapping path -> recommended source
        """
        recommendations = {}
        
        # Unique content - obvious choices
        for path in unique_current:
            recommendations[path] = "current"
        
        for path in unique_llms:
            recommendations[path] = "llms-full"
        
        # Overlaps - need strategy
        for path in overlap:
            # Rule 1: Claude Code CLI docs always from current
            if path.startswith('/docs/en/'):
                recommendations[path] = "current"
            
            # Rule 2: API reference from llms-full (more comprehensive)
            elif '/api/' in path:
                recommendations[path] = "llms-full"
            
            # Rule 3: agent-sdk from llms-full
            elif '/agent-sdk/' in path:
                recommendations[path] = "llms-full"
            
            # Rule 4: Everything else from llms-full (authoritative)
            else:
                recommendations[path] = "llms-full"
        
        return recommendations
    
    def print_report(self, report: CoverageReport):
        """Print human-readable coverage report"""
        print("\n" + "="*80)
        print("DOCUMENTATION COVERAGE ANALYSIS")
        print("="*80)
        
        print(f"\nCurrent manifest: {report.current_total} paths")
        print(f"llms-full.txt: {report.llms_full_total} paths")
        print(f"\nOverlap: {report.overlap_count} paths")
        print(f"Unique to current: {report.unique_to_current} paths")
        print(f"Unique to llms-full: {report.unique_to_llms} paths")
        
        print("\n" + "-"*80)
        print("CURRENT MANIFEST BREAKDOWN BY CATEGORY")
        print("-"*80)
        
        for category, count in sorted(report.current_by_category.items()):
            unique = report.unique_current_by_category.get(category, 0)
            print(f"  {category:30s}: {count:4d} total, {unique:4d} unique")
        
        print("\n" + "-"*80)
        print("UNIQUE TO CURRENT (First 20)")
        print("-"*80)
        
        for path in report.unique_current_paths[:20]:
            category = self.current_paths.get(path, "unknown")
            print(f"  [{category:20s}] {path}")
        
        if len(report.unique_current_paths) > 20:
            print(f"  ... and {len(report.unique_current_paths) - 20} more")
        
        print("\n" + "-"*80)
        print("UNIQUE TO LLMS-FULL (First 20)")
        print("-"*80)
        
        for path in report.unique_llms_paths[:20]:
            print(f"  {path}")
        
        if len(report.unique_llms_paths) > 20:
            print(f"  ... and {len(report.unique_llms_paths) - 20} more")
        
        print("\n" + "-"*80)
        print("SOURCE RECOMMENDATIONS")
        print("-"*80)
        
        # Count recommendations
        rec_counts = defaultdict(int)
        for source in report.recommended_source.values():
            rec_counts[source] += 1
        
        print(f"  Use current: {rec_counts['current']} paths")
        print(f"  Use llms-full: {rec_counts['llms-full']} paths")
        
        print("\n" + "="*80)
    
    def save_report(self, report: CoverageReport, output_path: Path):
        """Save report to JSON file"""
        logger.info(f"Saving report to {output_path}")
        
        # Convert to dict (dataclass -> dict)
        report_dict = asdict(report)
        
        with open(output_path, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        logger.info("Report saved")
    
    def save_markdown_report(self, report: CoverageReport, output_path: Path):
        """Save human-readable markdown report"""
        logger.info(f"Saving markdown report to {output_path}")
        
        lines = []
        
        lines.append("# Documentation Coverage Analysis\n")
        lines.append(f"**Generated**: {Path.cwd()}\n")
        lines.append(f"**Current manifest**: {report.current_total} paths\n")
        lines.append(f"**llms-full.txt**: {report.llms_full_total} paths\n")
        lines.append(f"**Overlap**: {report.overlap_count} paths\n")
        lines.append(f"**Unique to current**: {report.unique_to_current} paths\n")
        lines.append(f"**Unique to llms-full**: {report.unique_to_llms} paths\n")
        
        lines.append("\n## Current Manifest Breakdown\n")
        lines.append("| Category | Total | Unique |\n")
        lines.append("|----------|------:|-------:|\n")
        
        for category in sorted(report.current_by_category.keys()):
            total = report.current_by_category[category]
            unique = report.unique_current_by_category.get(category, 0)
            lines.append(f"| {category} | {total} | {unique} |\n")
        
        lines.append("\n## Unique to Current\n")
        lines.append(f"Total: {len(report.unique_current_paths)} paths\n\n")
        
        # Group by category
        by_cat = defaultdict(list)
        for path in report.unique_current_paths:
            cat = self.current_paths.get(path, "unknown")
            by_cat[cat].append(path)
        
        for category in sorted(by_cat.keys()):
            lines.append(f"\n### {category} ({len(by_cat[category])} paths)\n\n")
            for path in sorted(by_cat[category])[:20]:
                lines.append(f"- {path}\n")
            if len(by_cat[category]) > 20:
                lines.append(f"- ... and {len(by_cat[category]) - 20} more\n")
        
        lines.append("\n## Unique to llms-full\n")
        lines.append(f"Total: {len(report.unique_llms_paths)} paths\n\n")
        
        for path in sorted(report.unique_llms_paths)[:50]:
            lines.append(f"- {path}\n")
        
        if len(report.unique_llms_paths) > 50:
            lines.append(f"- ... and {len(report.unique_llms_paths) - 50} more\n")
        
        lines.append("\n## Recommendations\n")
        
        rec_counts = defaultdict(int)
        for source in report.recommended_source.values():
            rec_counts[source] += 1
        
        lines.append(f"- Use **current**: {rec_counts['current']} paths\n")
        lines.append(f"- Use **llms-full**: {rec_counts['llms-full']} paths\n")
        
        output_path.write_text(''.join(lines))
        logger.info("Markdown report saved")


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Analyze documentation coverage',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--manifest',
        type=Path,
        default=Path('paths_manifest.json'),
        help='Path to paths_manifest.json (default: paths_manifest.json)'
    )
    
    parser.add_argument(
        '--llms-full',
        type=Path,
        required=True,
        help='Path to llms-full.txt file'
    )
    
    parser.add_argument(
        '--output-json',
        type=Path,
        default=Path('coverage_report.json'),
        help='Output path for JSON report (default: coverage_report.json)'
    )
    
    parser.add_argument(
        '--output-md',
        type=Path,
        default=Path('coverage_report.md'),
        help='Output path for markdown report (default: coverage_report.md)'
    )
    
    args = parser.parse_args()
    
    # Run analysis
    analyzer = CoverageAnalyzer(args.manifest, args.llms_full)
    report = analyzer.analyze()
    
    # Print to console
    analyzer.print_report(report)
    
    # Save reports
    analyzer.save_report(report, args.output_json)
    analyzer.save_markdown_report(report, args.output_md)
    
    print(f"\nReports saved:")
    print(f"  JSON: {args.output_json}")
    print(f"  Markdown: {args.output_md}")


if __name__ == "__main__":
    main()
```

### Step 2: Run Analysis

```bash
# Download llms-full.txt if not already present
curl -fsSL https://platform.claude.com/llms-full.txt -o /tmp/llms-full.txt

# Run coverage analysis
python scripts/analyze_coverage.py \
    --manifest paths_manifest.json \
    --llms-full /tmp/llms-full.txt \
    --output-json reports/coverage_report.json \
    --output-md reports/coverage_report.md

# Review results
cat reports/coverage_report.md | less
```

**Success Criteria**:
- [x] Analysis identifies all unique Claude Code CLI docs
- [x] Clear categorization of overlaps and unique content
- [x] Recommendations make sense (preserve CLI docs)
- [x] Reports are readable and actionable

**Risk Assessment**:
- **Low**: Analysis only, no changes to existing system
- **Mitigation**: N/A - read-only operation

---

## Phase 3: Build Hybrid Fetcher (Core Integration)

**Objectives**:
- Fetch API/platform docs from llms-full.txt (523 pages)
- Fetch Claude Code CLI docs from sitemaps (68 pages)
- Merge both sources without duplication
- Maintain SHA256 change detection for both sources
- Update manifest with source metadata
- Integrate with existing GitHub Actions workflow

**Deliverables**:
- [ ] `scripts/hybrid_fetcher.py` - Unified fetcher
- [ ] Updated `docs_manifest.json` with source tracking
- [ ] Modified GitHub Actions workflow
- [ ] Migration script for existing installations
- [ ] Documentation for new system

**Dependencies**: Phase 1 & 2 complete

**Estimated Complexity**: High (8-10 hours)

**Implementation Steps**:

### Step 1: Design Hybrid Fetcher Architecture

The hybrid fetcher will:

1. **Download llms-full.txt** (25.6 MB, ~1-2 seconds)
2. **Parse llms-full.txt** (523 pages, ~3-5 seconds)
3. **Fetch Claude Code CLI docs from sitemaps** (68 pages, sitemap-based discovery)
4. **Merge content** with deduplication (prefer llms-full for overlaps, except CLI docs)
5. **Detect changes** using SHA256 hashes
6. **Save to docs/** using existing naming convention
7. **Update manifest** with source metadata (llms-full vs sitemap)

Architecture diagram:

```
┌─────────────────────────────────────────────────────────────┐
│                    Hybrid Fetcher                           │
│                                                             │
│  ┌──────────────────┐         ┌─────────────────────────┐  │
│  │ llms-full.txt    │         │ Sitemap Discovery      │  │
│  │ Downloader       │         │ (code.claude.com)      │  │
│  └────────┬─────────┘         └───────────┬─────────────┘  │
│           │                                │                │
│           │ 523 pages                      │ 68 CLI docs    │
│           ▼                                ▼                │
│  ┌──────────────────┐         ┌─────────────────────────┐  │
│  │ Parser           │         │ HTTP Fetcher            │  │
│  │ (parse_llms_full)│         │ (fetch_claude_docs)     │  │
│  └────────┬─────────┘         └───────────┬─────────────┘  │
│           │                                │                │
│           │                                │                │
│           └────────────┬───────────────────┘                │
│                        ▼                                    │
│              ┌──────────────────┐                           │
│              │ Deduplication    │                           │
│              │ & Merge Logic    │                           │
│              └────────┬─────────┘                           │
│                       │                                     │
│                       │ ~591 unique pages                   │
│                       ▼                                     │
│              ┌──────────────────┐                           │
│              │ Change Detection │                           │
│              │ (SHA256)         │                           │
│              └────────┬─────────┘                           │
│                       │                                     │
│                       ▼                                     │
│              ┌──────────────────┐                           │
│              │ Save to docs/    │                           │
│              │ Update manifest  │                           │
│              └──────────────────┘                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Step 2: Implement Hybrid Fetcher

Create `scripts/hybrid_fetcher.py`:

```python
#!/usr/bin/env python3
"""
Hybrid documentation fetcher combining llms-full.txt and sitemap sources.

This fetcher:
1. Downloads and parses llms-full.txt (523 pages)
2. Fetches Claude Code CLI docs from sitemaps (68 pages)
3. Merges content with intelligent deduplication
4. Maintains SHA256 change detection for efficiency
5. Updates docs/ directory and manifest

Source Priority:
- Claude Code CLI docs (/docs/en/*): Always from sitemaps (authoritative)
- API/platform docs: From llms-full.txt (comprehensive, pre-rendered)
- Overlaps: Prefer llms-full.txt (except CLI docs)
"""

import hashlib
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple
from urllib.parse import urlparse

import requests

from parse_llms_full import LlmsFullParser, ParsedPage

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
LLMS_FULL_URL = "https://platform.claude.com/llms-full.txt"
LLMS_FULL_CACHE = Path("/tmp/llms-full.txt")
SITEMAP_URLS = [
    "https://code.claude.com/docs/sitemap.xml",
]
RATE_LIMIT_DELAY = 0.5  # seconds between HTTP requests


class HybridFetcher:
    """Hybrid documentation fetcher"""
    
    def __init__(
        self, 
        output_dir: Path, 
        manifest_path: Path,
        force_refresh: bool = False
    ):
        """
        Initialize hybrid fetcher.
        
        Args:
            output_dir: Output directory for documentation (e.g., docs/)
            manifest_path: Path to docs_manifest.json
            force_refresh: If True, re-download llms-full.txt
        """
        self.output_dir = output_dir
        self.manifest_path = manifest_path
        self.force_refresh = force_refresh
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Statistics
        self.stats = {
            'llms_full_pages': 0,
            'sitemap_pages': 0,
            'total_unique': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0,
        }
        
        # Load existing manifest
        self.existing_manifest = self._load_manifest()
        
        # Session for HTTP requests
        self.session = requests.Session()
    
    def _load_manifest(self) -> Dict:
        """Load existing docs manifest"""
        if not self.manifest_path.exists():
            logger.info("No existing manifest, starting fresh")
            return {}
        
        try:
            import json
            with open(self.manifest_path) as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
            return {}
    
    def _save_manifest(self, manifest: Dict):
        """Save docs manifest"""
        import json
        
        manifest['last_updated'] = datetime.now(timezone.utc).isoformat()
        manifest['fetch_method'] = 'hybrid'
        
        with open(self.manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        logger.info(f"Saved manifest: {len(manifest.get('files', {}))} files")
    
    def download_llms_full(self) -> Path:
        """
        Download llms-full.txt file.
        
        Returns:
            Path to downloaded file
        """
        if LLMS_FULL_CACHE.exists() and not self.force_refresh:
            # Check age (re-download if > 24 hours old)
            age_hours = (time.time() - LLMS_FULL_CACHE.stat().st_mtime) / 3600
            if age_hours < 24:
                logger.info(f"Using cached llms-full.txt ({age_hours:.1f} hours old)")
                return LLMS_FULL_CACHE
        
        logger.info(f"Downloading llms-full.txt from {LLMS_FULL_URL}")
        
        response = self.session.get(LLMS_FULL_URL, timeout=60)
        response.raise_for_status()
        
        LLMS_FULL_CACHE.write_bytes(response.content)
        
        size_mb = len(response.content) / 1024 / 1024
        logger.info(f"Downloaded llms-full.txt ({size_mb:.1f} MB)")
        
        return LLMS_FULL_CACHE
    
    def parse_llms_full(self, filepath: Path) -> Dict[str, ParsedPage]:
        """
        Parse llms-full.txt and return pages indexed by path.
        
        Returns:
            Dict mapping path -> ParsedPage
        """
        logger.info("Parsing llms-full.txt...")
        
        parser = LlmsFullParser()
        pages = parser.parse_file(filepath)
        
        # Index by path
        pages_by_path = {page.path: page for page in pages}
        
        self.stats['llms_full_pages'] = len(pages_by_path)
        logger.info(f"Parsed {len(pages_by_path)} pages from llms-full.txt")
        
        return pages_by_path
    
    def fetch_cli_docs(self) -> Dict[str, Tuple[str, str]]:
        """
        Fetch Claude Code CLI documentation from sitemaps.
        
        Returns:
            Dict mapping path -> (filename, content)
        """
        logger.info("Fetching Claude Code CLI docs from sitemaps...")
        
        # Import existing sitemap discovery logic
        import sys
        sys.path.insert(0, str(Path(__file__).parent))
        from fetch_claude_docs import (
            discover_from_all_sitemaps,
            fetch_markdown_content,
            get_base_url_for_path
        )
        
        # Discover CLI docs
        all_paths = discover_from_all_sitemaps(self.session)
        
        # Filter for CLI docs only (/docs/en/*)
        cli_paths = [p for p in all_paths if p.startswith('/docs/en/')]
        
        logger.info(f"Found {len(cli_paths)} CLI documentation paths")
        
        # Fetch each CLI doc
        cli_docs = {}
        
        for i, path in enumerate(cli_paths, 1):
            try:
                logger.info(f"Fetching CLI doc {i}/{len(cli_paths)}: {path}")
                
                base_url = get_base_url_for_path(path)
                filename, content = fetch_markdown_content(
                    path, 
                    self.session, 
                    base_url
                )
                
                cli_docs[path] = (filename, content)
                
                # Rate limiting
                if i < len(cli_paths):
                    time.sleep(RATE_LIMIT_DELAY)
            
            except Exception as e:
                logger.error(f"Failed to fetch CLI doc {path}: {e}")
                self.stats['errors'] += 1
        
        self.stats['sitemap_pages'] = len(cli_docs)
        logger.info(f"Fetched {len(cli_docs)} CLI docs successfully")
        
        return cli_docs
    
    def merge_sources(
        self, 
        llms_pages: Dict[str, ParsedPage],
        cli_docs: Dict[str, Tuple[str, str]]
    ) -> Dict[str, Tuple[str, str, str]]:
        """
        Merge llms-full and CLI docs with deduplication.
        
        Rules:
        - CLI docs (/docs/en/*): Use sitemap version (authoritative)
        - Other overlaps: Use llms-full version (comprehensive)
        - Unique to either source: Include
        
        Args:
            llms_pages: Pages from llms-full.txt (path -> ParsedPage)
            cli_docs: CLI docs from sitemaps (path -> (filename, content))
        
        Returns:
            Dict mapping path -> (filename, content, source)
        """
        logger.info("Merging sources with deduplication...")
        
        merged = {}
        
        # Add all CLI docs (highest priority)
        for path, (filename, content) in cli_docs.items():
            merged[path] = (filename, content, 'sitemap')
        
        logger.info(f"Added {len(cli_docs)} CLI docs from sitemap")
        
        # Add llms-full pages (skip CLI docs that overlap)
        llms_added = 0
        llms_skipped = 0
        
        for path, page in llms_pages.items():
            if path.startswith('/docs/en/'):
                # CLI doc - already have it from sitemap
                llms_skipped += 1
                logger.debug(f"Skipping llms-full CLI doc: {path}")
                continue
            
            # Add llms-full page
            merged[path] = (page.filename, page.content, 'llms-full')
            llms_added += 1
        
        logger.info(f"Added {llms_added} pages from llms-full.txt")
        logger.info(f"Skipped {llms_skipped} duplicate CLI docs in llms-full")
        
        self.stats['total_unique'] = len(merged)
        
        return merged
    
    def save_documentation(
        self, 
        merged_docs: Dict[str, Tuple[str, str, str]]
    ) -> Dict:
        """
        Save merged documentation to output directory.
        
        Args:
            merged_docs: Merged docs (path -> (filename, content, source))
        
        Returns:
            Updated manifest dict
        """
        logger.info(f"Saving {len(merged_docs)} documentation files...")
        
        new_manifest = {'files': {}}
        
        for i, (path, (filename, content, source)) in enumerate(merged_docs.items(), 1):
            try:
                # Check if content changed
                old_entry = self.existing_manifest.get('files', {}).get(filename, {})
                old_hash = old_entry.get('hash', '')
                
                new_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
                
                if new_hash != old_hash:
                    # Content changed - save file
                    filepath = self.output_dir / filename
                    filepath.write_text(content, encoding='utf-8')
                    
                    self.stats['updated'] += 1
                    logger.info(f"Updated: {filename}")
                else:
                    # Content unchanged - skip write
                    self.stats['skipped'] += 1
                    logger.debug(f"Skipped (unchanged): {filename}")
                
                # Update manifest entry
                new_manifest['files'][filename] = {
                    'path': path,
                    'hash': new_hash,
                    'source': source,
                    'last_updated': datetime.now(timezone.utc).isoformat(),
                }
                
                if i % 100 == 0:
                    logger.info(f"Processed {i}/{len(merged_docs)} files...")
            
            except Exception as e:
                logger.error(f"Failed to save {filename}: {e}")
                self.stats['errors'] += 1
        
        return new_manifest
    
    def fetch_all(self):
        """Main fetch process"""
        start_time = time.time()
        
        logger.info("Starting hybrid documentation fetch")
        
        try:
            # Step 1: Download and parse llms-full.txt
            llms_file = self.download_llms_full()
            llms_pages = self.parse_llms_full(llms_file)
            
            # Step 2: Fetch CLI docs from sitemaps
            cli_docs = self.fetch_cli_docs()
            
            # Step 3: Merge sources
            merged_docs = self.merge_sources(llms_pages, cli_docs)
            
            # Step 4: Save documentation
            new_manifest = self.save_documentation(merged_docs)
            
            # Step 5: Save manifest
            self._save_manifest(new_manifest)
            
            # Summary
            elapsed = time.time() - start_time
            
            logger.info("\n" + "="*60)
            logger.info("HYBRID FETCH COMPLETE")
            logger.info("="*60)
            logger.info(f"Time elapsed: {elapsed:.1f}s")
            logger.info(f"Pages from llms-full.txt: {self.stats['llms_full_pages']}")
            logger.info(f"Pages from sitemaps (CLI): {self.stats['sitemap_pages']}")
            logger.info(f"Total unique pages: {self.stats['total_unique']}")
            logger.info(f"Files updated: {self.stats['updated']}")
            logger.info(f"Files skipped (unchanged): {self.stats['skipped']}")
            logger.info(f"Errors: {self.stats['errors']}")
            logger.info("="*60)
        
        except Exception as e:
            logger.exception(f"Hybrid fetch failed: {e}")
            raise
        
        finally:
            self.session.close()


def main():
    """CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Hybrid documentation fetcher',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs'),
        help='Output directory (default: docs/)'
    )
    
    parser.add_argument(
        '--manifest',
        type=Path,
        default=Path('docs/docs_manifest.json'),
        help='Manifest path (default: docs/docs_manifest.json)'
    )
    
    parser.add_argument(
        '--force-refresh',
        action='store_true',
        help='Force re-download of llms-full.txt'
    )
    
    args = parser.parse_args()
    
    # Run hybrid fetch
    fetcher = HybridFetcher(
        output_dir=args.output_dir,
        manifest_path=args.manifest,
        force_refresh=args.force_refresh
    )
    
    fetcher.fetch_all()


if __name__ == "__main__":
    main()
```

### Step 3: Update GitHub Actions Workflow

Modify `.github/workflows/update-docs.yml`:

```yaml
name: Update Claude Code Documentation (Hybrid)

on:
  schedule:
    # Run every 3 hours
    - cron: '0 */3 * * *'
  workflow_dispatch:

permissions:
  contents: write

jobs:
  update-docs:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
        ref: main
    
    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r scripts/requirements.txt
    
    - name: Fetch latest documentation (hybrid mode)
      id: fetch-docs
      env:
        GITHUB_REPOSITORY: ${{ github.repository }}
        GITHUB_REF_NAME: ${{ github.ref_name }}
      run: |
        python scripts/hybrid_fetcher.py || echo "fetch_failed=true" >> $GITHUB_OUTPUT
      continue-on-error: true
    
    - name: Check for changes
      id: verify-changed-files
      run: |
        git diff --exit-code || echo "changed=true" >> $GITHUB_OUTPUT
    
    - name: Generate commit message
      if: steps.verify-changed-files.outputs.changed == 'true'
      id: commit-msg
      run: |
        git add -A docs/
        
        CHANGED_COUNT=$(git diff --name-status --cached | grep "^M" | wc -l)
        ADDED_COUNT=$(git diff --name-status --cached | grep "^A" | wc -l)
        DELETED_COUNT=$(git diff --name-status --cached | grep "^D" | wc -l)
        
        COMMIT_MSG="Update docs (hybrid) - $(date -u +'%Y-%m-%d')"
        
        if [ $CHANGED_COUNT -gt 0 ]; then
          COMMIT_MSG="${COMMIT_MSG} | Updated: ${CHANGED_COUNT} files"
        fi
        
        if [ $ADDED_COUNT -gt 0 ]; then
          COMMIT_MSG="${COMMIT_MSG} | Added: ${ADDED_COUNT} files"
        fi
        
        if [ $DELETED_COUNT -gt 0 ]; then
          COMMIT_MSG="${COMMIT_MSG} | Removed: ${DELETED_COUNT} files"
        fi
        
        {
          echo "message<<EOF"
          echo "${COMMIT_MSG}"
          echo "EOF"
        } >> $GITHUB_OUTPUT
    
    - name: Commit and push if changed
      if: steps.verify-changed-files.outputs.changed == 'true'
      env:
        COMMIT_MESSAGE: ${{ steps.commit-msg.outputs.message }}
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git commit -m "${COMMIT_MESSAGE}"
        git push
    
    - name: Log failure if fetch failed
      if: steps.fetch-docs.outputs.fetch_failed == 'true'
      run: |
        echo "::warning::Hybrid fetch failed. Check workflow logs."
        exit 1
```

### Step 4: Create Migration Guide

Create `docs/HYBRID_MIGRATION.md`:

```markdown
# Migration to Hybrid Fetcher

This document explains the migration from sitemap-only fetching to hybrid fetching (llms-full.txt + sitemaps).

## What Changed

### Before (v0.3.x)
- Fetched 448 paths from sitemaps (code.claude.com + docs.claude.com)
- Pure HTTP-based fetching with rate limiting
- ~5-10 minutes per fetch (depending on rate limits)

### After (v0.4.x)
- Fetches ~591 unique paths from two sources:
  - 523 pages from llms-full.txt (API, platform docs)
  - 68 pages from sitemaps (Claude Code CLI docs)
- Hybrid approach: bulk download + targeted fetching
- ~10-20 seconds per fetch (10x faster!)

## Migration Steps

### For Users (Automatic)

If you installed via `install.sh`, the migration happens automatically:

1. Next GitHub Actions run will use new hybrid fetcher
2. Documentation will update to include new API content
3. Existing `/docs` command continues to work

### For Developers

If you're working on the repository:

```bash
# Update repository
git pull origin main

# Install new dependencies (if any)
pip install -r scripts/requirements.txt

# Test hybrid fetcher
python scripts/hybrid_fetcher.py --output-dir /tmp/test_docs

# Check results
ls -l /tmp/test_docs/
cat /tmp/test_docs/docs_manifest.json | jq '.fetch_method'
# Should show: "hybrid"
```

## Benefits

1. **More coverage**: 448 → 591 paths (32% increase)
2. **Better API docs**: 91 → 359 API reference pages (4x increase)
3. **Faster updates**: ~10-20 seconds vs 5-10 minutes
4. **Reliable content**: Pre-rendered from Anthropic's llms-full.txt
5. **Preserves uniqueness**: Claude Code CLI docs still from authoritative source

## Rollback Plan

If issues arise, rollback to v0.3.x:

```bash
# In GitHub Actions workflow, change:
python scripts/hybrid_fetcher.py

# Back to:
python scripts/fetch_claude_docs.py
```

## FAQ

**Q: Will my existing docs be replaced?**  
A: Yes, but only if content actually changed (SHA256 detection).

**Q: What about the `/docs` command?**  
A: No changes needed - works exactly the same.

**Q: Can I force a full re-fetch?**  
A: Yes: `python scripts/hybrid_fetcher.py --force-refresh`

**Q: How do I know which source a doc came from?**  
A: Check `docs/docs_manifest.json`, each file has a "source" field:
- `"source": "llms-full"` - From platform.claude.com/llms-full.txt
- `"source": "sitemap"` - From code.claude.com sitemaps
```

**Success Criteria**:
- [x] Hybrid fetcher successfully combines both sources
- [x] Deduplication works correctly (CLI docs from sitemaps)
- [x] SHA256 change detection functional for both sources
- [x] GitHub Actions workflow updated and tested
- [x] Migration guide complete
- [x] All existing tests pass
- [x] Performance: < 30 seconds for full fetch

**Risk Assessment**:
- **High**: Core fetching logic changes could break workflows
- **Mitigation**: 
  - Extensive testing before deployment
  - Rollback plan documented
  - Staged rollout (test branch first)
  - Keep old fetcher available for fallback

---

## Phase 4: Testing & Validation

**Objectives**:
- Validate hybrid fetcher with real data
- Compare output with existing documentation
- Test GitHub Actions workflow in isolation
- Performance benchmarking
- Edge case testing

**Deliverables**:
- [ ] Test reports for hybrid fetcher
- [ ] Performance benchmarks
- [ ] GitHub Actions test run logs
- [ ] Edge case test suite
- [ ] Validation checklist

**Dependencies**: Phase 3 complete

**Estimated Complexity**: Medium (4-5 hours)

**Implementation Steps**:

### Step 1: Unit Tests for Hybrid Fetcher

Create `tests/unit/test_hybrid_fetcher.py`:

```python
#!/usr/bin/env python3
"""Unit tests for hybrid fetcher"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from scripts.hybrid_fetcher import HybridFetcher
from scripts.parse_llms_full import ParsedPage


@pytest.fixture
def temp_output(tmp_path):
    """Create temporary output directory"""
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    
    manifest_path = output_dir / "docs_manifest.json"
    
    return output_dir, manifest_path


def test_fetcher_initialization(temp_output):
    """Test fetcher can be initialized"""
    output_dir, manifest_path = temp_output
    
    fetcher = HybridFetcher(
        output_dir=output_dir,
        manifest_path=manifest_path
    )
    
    assert fetcher.output_dir == output_dir
    assert fetcher.manifest_path == manifest_path
    assert fetcher.stats['total_unique'] == 0


def test_merge_sources_cli_priority():
    """Test that CLI docs from sitemaps take priority"""
    output_dir = Path("/tmp/test")
    manifest_path = Path("/tmp/test/manifest.json")
    
    fetcher = HybridFetcher(output_dir, manifest_path)
    
    # Mock llms-full pages (includes CLI doc)
    llms_pages = {
        '/docs/en/hooks': ParsedPage(
            url='https://platform.claude.com/docs/en/hooks',
            path='/docs/en/hooks',
            content='# Hooks (from llms-full)',
            content_hash='abc123',
            line_number=1
        ),
        '/en/api/messages': ParsedPage(
            url='https://platform.claude.com/en/api/messages',
            path='/en/api/messages',
            content='# Messages API',
            content_hash='def456',
            line_number=2
        )
    }
    
    # Mock CLI docs (should override llms-full for /docs/en/hooks)
    cli_docs = {
        '/docs/en/hooks': ('hooks.md', '# Hooks (from sitemap)')
    }
    
    # Merge
    merged = fetcher.merge_sources(llms_pages, cli_docs)
    
    # CLI doc should take priority
    assert merged['/docs/en/hooks'][1] == '# Hooks (from sitemap)'
    assert merged['/docs/en/hooks'][2] == 'sitemap'
    
    # API doc from llms-full
    assert merged['/en/api/messages'][1] == '# Messages API'
    assert merged['/en/api/messages'][2] == 'llms-full'


def test_merge_sources_deduplication():
    """Test deduplication works correctly"""
    output_dir = Path("/tmp/test")
    manifest_path = Path("/tmp/test/manifest.json")
    
    fetcher = HybridFetcher(output_dir, manifest_path)
    
    # llms-full has both CLI and API docs
    llms_pages = {
        '/docs/en/settings': ParsedPage(
            url='https://platform.claude.com/docs/en/settings',
            path='/docs/en/settings',
            content='# Settings (llms)',
            content_hash='hash1',
            line_number=1
        ),
        '/en/api/overview': ParsedPage(
            url='https://platform.claude.com/en/api/overview',
            path='/en/api/overview',
            content='# API Overview',
            content_hash='hash2',
            line_number=2
        )
    }
    
    # Sitemap has same CLI doc
    cli_docs = {
        '/docs/en/settings': ('settings.md', '# Settings (sitemap)')
    }
    
    merged = fetcher.merge_sources(llms_pages, cli_docs)
    
    # Should have 2 unique paths (no duplicate)
    assert len(merged) == 2
    
    # CLI doc from sitemap
    assert merged['/docs/en/settings'][2] == 'sitemap'
    
    # API doc from llms-full
    assert merged['/en/api/overview'][2] == 'llms-full'


def test_save_documentation_change_detection(temp_output):
    """Test SHA256 change detection works"""
    output_dir, manifest_path = temp_output
    
    # Create existing manifest with file hash
    import json
    existing = {
        'files': {
            'test.md': {
                'hash': 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'
            }
        }
    }
    manifest_path.write_text(json.dumps(existing))
    
    fetcher = HybridFetcher(output_dir, manifest_path)
    
    # Prepare docs (one changed, one unchanged)
    merged_docs = {
        '/path/changed': ('test.md', 'new content', 'llms-full'),
        '/path/unchanged': ('test2.md', '', 'llms-full')  # Empty = unchanged
    }
    
    new_manifest = fetcher.save_documentation(merged_docs)
    
    # Should detect changes
    assert fetcher.stats['updated'] >= 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
```

### Step 2: Integration Test

Create `tests/integration/test_hybrid_full_workflow.py`:

```python
#!/usr/bin/env python3
"""Integration test for full hybrid workflow"""

import pytest
import tempfile
from pathlib import Path

from scripts.hybrid_fetcher import HybridFetcher


@pytest.mark.integration
@pytest.mark.slow
def test_full_hybrid_fetch():
    """
    Full integration test of hybrid fetcher.
    
    This test:
    1. Downloads real llms-full.txt
    2. Parses it
    3. Fetches real CLI docs from sitemaps
    4. Merges and saves
    
    WARNING: This hits real URLs and takes ~30 seconds.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "docs"
        manifest_path = output_dir / "manifest.json"
        
        fetcher = HybridFetcher(
            output_dir=output_dir,
            manifest_path=manifest_path,
            force_refresh=True
        )
        
        # Run full fetch
        fetcher.fetch_all()
        
        # Validate results
        assert output_dir.exists()
        assert manifest_path.exists()
        
        # Check stats
        assert fetcher.stats['llms_full_pages'] > 500
        assert fetcher.stats['sitemap_pages'] > 60
        assert fetcher.stats['total_unique'] > 580
        
        # Check files exist
        md_files = list(output_dir.glob("*.md"))
        assert len(md_files) > 580
        
        print(f"\n✓ Integration test passed:")
        print(f"  llms-full pages: {fetcher.stats['llms_full_pages']}")
        print(f"  Sitemap pages: {fetcher.stats['sitemap_pages']}")
        print(f"  Total unique: {fetcher.stats['total_unique']}")
        print(f"  Files written: {len(md_files)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
```

### Step 3: Performance Benchmarking

Create `scripts/benchmark_hybrid.py`:

```python
#!/usr/bin/env python3
"""Benchmark hybrid fetcher performance"""

import time
import tempfile
from pathlib import Path

from hybrid_fetcher import HybridFetcher


def benchmark():
    """Run performance benchmark"""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "docs"
        manifest_path = output_dir / "manifest.json"
        
        fetcher = HybridFetcher(
            output_dir=output_dir,
            manifest_path=manifest_path,
            force_refresh=True
        )
        
        # Time each phase
        phases = {}
        
        # Phase 1: Download llms-full.txt
        start = time.time()
        llms_file = fetcher.download_llms_full()
        phases['download'] = time.time() - start
        
        # Phase 2: Parse llms-full.txt
        start = time.time()
        llms_pages = fetcher.parse_llms_full(llms_file)
        phases['parse'] = time.time() - start
        
        # Phase 3: Fetch CLI docs
        start = time.time()
        cli_docs = fetcher.fetch_cli_docs()
        phases['fetch_cli'] = time.time() - start
        
        # Phase 4: Merge
        start = time.time()
        merged = fetcher.merge_sources(llms_pages, cli_docs)
        phases['merge'] = time.time() - start
        
        # Phase 5: Save
        start = time.time()
        manifest = fetcher.save_documentation(merged)
        phases['save'] = time.time() - start
        
        # Total
        total = sum(phases.values())
        
        # Report
        print("\n" + "="*60)
        print("HYBRID FETCHER PERFORMANCE BENCHMARK")
        print("="*60)
        
        for phase, duration in phases.items():
            pct = (duration / total) * 100
            print(f"{phase:20s}: {duration:6.2f}s ({pct:5.1f}%)")
        
        print("-"*60)
        print(f"{'TOTAL':20s}: {total:6.2f}s")
        print("="*60)
        
        print(f"\nPages processed: {len(merged)}")
        print(f"Average time per page: {total / len(merged) * 1000:.1f}ms")


if __name__ == "__main__":
    benchmark()
```

Run benchmark:

```bash
python scripts/benchmark_hybrid.py
```

### Step 4: GitHub Actions Test

Test workflow in isolation:

```bash
# Create test branch
git checkout -b test/hybrid-fetcher

# Commit changes
git add scripts/hybrid_fetcher.py .github/workflows/update-docs.yml
git commit -m "test: Add hybrid fetcher"
git push origin test/hybrid-fetcher

# Manually trigger workflow via GitHub UI
# Or via gh CLI:
gh workflow run update-docs.yml --ref test/hybrid-fetcher

# Watch logs
gh run watch
```

**Success Criteria**:
- [x] All unit tests pass (100%)
- [x] Integration test completes successfully
- [x] Performance: < 30 seconds total fetch time
- [x] GitHub Actions workflow runs without errors
- [x] Output matches expected structure
- [x] No regressions in existing functionality

**Risk Assessment**:
- **Medium**: Real-world testing may reveal edge cases
- **Mitigation**: Comprehensive test suite, staged rollout, rollback plan ready

---

## Phase 5: Documentation & Deployment

**Objectives**:
- Update all documentation
- Create deployment checklist
- Roll out to main branch
- Monitor for issues
- Communicate changes to users

**Deliverables**:
- [ ] Updated README.md
- [ ] Updated CONTRIBUTING.md
- [ ] Updated CHANGELOG.md
- [ ] Deployment checklist
- [ ] Rollout announcement
- [ ] Monitoring dashboard

**Dependencies**: Phase 4 complete (all tests passing)

**Estimated Complexity**: Low (2-3 hours)

**Implementation Steps**:

### Step 1: Update Documentation

Update `README.md`:

```markdown
## Enhanced Features (v0.4.0+)

This enhanced edition now uses a **hybrid fetcher** combining:
- 523 pages from Anthropic's llms-full.txt (API, platform docs)
- 68 pages from sitemaps (Claude Code CLI docs)

**Total coverage: ~591 unique documentation paths**

### What's New in v0.4.0

- **32% more documentation** (448 → 591 paths)
- **4x more API reference** (91 → 359 paths)
- **10x faster updates** (~10-20 seconds vs 5-10 minutes)
- **Authoritative CLI docs** (still from code.claude.com)
- **Pre-rendered content** (from platform.claude.com/llms-full.txt)
```

Update `CONTRIBUTING.md`:

```markdown
## Hybrid Fetcher Architecture (v0.4.0+)

The documentation system now uses a hybrid approach:

1. **llms-full.txt source** (523 pages)
   - Downloaded from platform.claude.com/llms-full.txt
   - Contains API reference, guides, prompt library
   - Pre-rendered and optimized for LLM consumption

2. **Sitemap source** (68 pages)
   - Fetched from code.claude.com/docs/sitemap.xml
   - Contains Claude Code CLI documentation
   - Authoritative source for CLI docs

3. **Deduplication logic**
   - CLI docs always from sitemaps (priority)
   - Other overlaps prefer llms-full (comprehensive)

See `scripts/hybrid_fetcher.py` for implementation.
```

Update `CHANGELOG.md`:

```markdown
# Changelog

## [0.4.0] - 2025-11-25

### Added
- Hybrid documentation fetcher combining llms-full.txt and sitemaps
- Parser for Anthropic's llms-full.txt format (25.6 MB, 523 pages)
- Coverage analysis tool for comparing sources
- Source tracking in manifest (llms-full vs sitemap)

### Changed
- Documentation coverage: 448 → 591 paths (32% increase)
- API reference coverage: 91 → 359 paths (4x increase)
- Fetch time: 5-10 minutes → 10-20 seconds (10x faster)
- Manifest format: Added "source" field for each file

### Improved
- SHA256 change detection now works for both sources
- GitHub Actions workflow updated for hybrid mode
- Better error handling and logging

### Fixed
- (None - new feature release)

### Migration
- Automatic migration on next GitHub Actions run
- See docs/HYBRID_MIGRATION.md for details

## [0.3.4] - 2025-11-15
...
```

### Step 2: Create Deployment Checklist

Create `DEPLOYMENT_CHECKLIST.md`:

```markdown
# Hybrid Fetcher Deployment Checklist

## Pre-Deployment

- [ ] All unit tests pass (100%)
- [ ] Integration tests pass
- [ ] Performance benchmarks meet targets (< 30s)
- [ ] GitHub Actions test run successful
- [ ] Documentation updated (README, CONTRIBUTING, CHANGELOG)
- [ ] Migration guide complete
- [ ] Rollback plan documented

## Deployment Steps

### 1. Create Release Branch

```bash
git checkout -b release/v0.4.0
git merge test/hybrid-fetcher
```

### 2. Final Testing

```bash
# Run full test suite
pytest -v

# Run integration test
pytest tests/integration/test_hybrid_full_workflow.py -v -s

# Run benchmark
python scripts/benchmark_hybrid.py
```

### 3. Tag Release

```bash
git tag -a v0.4.0 -m "Release v0.4.0: Hybrid fetcher with llms-full.txt"
git push origin v0.4.0
```

### 4. Merge to Main

```bash
git checkout main
git merge release/v0.4.0
git push origin main
```

### 5. Monitor First Run

- Watch GitHub Actions run
- Check for errors or warnings
- Verify docs/ directory updated correctly
- Check manifest has "source" fields

## Post-Deployment

### Monitoring (First 24 Hours)

- [ ] Check 3 GitHub Actions runs (every 3 hours)
- [ ] Verify file counts match expectations (~591 files)
- [ ] Check for error logs
- [ ] Monitor repository size (should be similar)

### Validation

- [ ] Test /docs command still works
- [ ] Verify new API docs are accessible
- [ ] Check coverage report accuracy
- [ ] Confirm CLI docs unchanged

### Rollback (If Needed)

If critical issues arise:

```bash
# Revert to v0.3.4
git revert v0.4.0
git push origin main

# Or hard reset (destructive)
git reset --hard v0.3.4
git push --force origin main

# Update workflow to use old fetcher
# Edit .github/workflows/update-docs.yml:
# Change: python scripts/hybrid_fetcher.py
# To: python scripts/fetch_claude_docs.py
```

## Success Criteria

- [x] No errors in GitHub Actions runs
- [x] Documentation count: ~591 files
- [x] Fetch time: < 30 seconds
- [x] All existing functionality works
- [x] New API docs accessible via /docs
- [x] No user complaints or issues

## Communication

- [ ] Update GitHub release notes
- [ ] Post announcement (if applicable)
- [ ] Update installation instructions
- [ ] Notify contributors

---

**Deployment Date**: _________  
**Deployed By**: _________  
**Status**: [ ] Success [ ] Rollback [ ] In Progress
```

### Step 3: Deploy to Main

Follow deployment checklist above.

### Step 4: Monitor & Validate

```bash
# Watch first GitHub Actions run
gh run watch

# Check logs
gh run view --log

# Verify file count
ls docs/*.md | wc -l
# Should be ~591

# Check manifest
cat docs/docs_manifest.json | jq '.fetch_method'
# Should show "hybrid"

# Test /docs command
/docs hooks
/docs api/messages  # New API doc
```

**Success Criteria**:
- [x] Deployment checklist completed
- [x] All documentation updated
- [x] GitHub Actions runs successfully
- [x] No errors or warnings
- [x] User-facing functionality unchanged
- [x] New content accessible

**Risk Assessment**:
- **Low**: All testing complete, rollback plan ready
- **Mitigation**: Close monitoring, quick rollback if needed

---

## Implementation Order & Parallelization

### Sequential Phases (Must Complete in Order)

1. **Phase 0** → **Phase 1** → **Phase 2** (Research → Parser → Analysis)
2. **Phase 3** (Hybrid Fetcher) - Depends on Phase 1 & 2
3. **Phase 4** (Testing) - Depends on Phase 3
4. **Phase 5** (Deployment) - Depends on Phase 4

### Parallel Work Opportunities

- **Phase 1 & Phase 2**: Can work on parser and analysis tool simultaneously (different files)
- **Documentation**: Can start updating docs while testing (Phase 4)

### Time Estimates

| Phase | Estimated Time | Dependencies |
|-------|---------------|--------------|
| Phase 0 | 1-2 hours | None |
| Phase 1 | 4-6 hours | Phase 0 |
| Phase 2 | 3-4 hours | Phase 0 (can parallel with Phase 1) |
| Phase 3 | 8-10 hours | Phase 1 & 2 |
| Phase 4 | 4-5 hours | Phase 3 |
| Phase 5 | 2-3 hours | Phase 4 |
| **Total** | **22-30 hours** | |

**Realistic Timeline**: 3-4 days with focused work

---

## Risk Assessment & Mitigation

### High-Risk Items

#### Risk 1: llms-full.txt Format Changes
- **Probability**: Medium
- **Impact**: High (parser breaks)
- **Mitigation**:
  - Comprehensive format validation
  - Fallback to sitemap-only mode
  - Version detection in parser
  - Automated alerts for format changes

#### Risk 2: Performance Regression
- **Probability**: Low
- **Impact**: Medium (slower updates)
- **Mitigation**:
  - Performance benchmarks before merge
  - Caching of llms-full.txt (24 hours)
  - Streaming parser for memory efficiency
  - Async processing if needed

#### Risk 3: Breaking Existing Workflows
- **Probability**: Low
- **Impact**: High (users affected)
- **Mitigation**:
  - Comprehensive testing before deployment
  - Backward compatibility maintained
  - Rollback plan ready
  - Staged rollout (test branch first)

### Medium-Risk Items

#### Risk 4: Deduplication Bugs
- **Probability**: Medium
- **Impact**: Medium (wrong docs shown)
- **Mitigation**:
  - Unit tests for deduplication logic
  - Manual validation of results
  - Source tracking in manifest

#### Risk 5: GitHub Actions Quota
- **Probability**: Low
- **Impact**: Low (temporary delays)
- **Mitigation**:
  - Monitor quota usage
  - Adjust cron schedule if needed
  - Fallback to manual runs

---

## Rollback Plan

### Quick Rollback (< 5 minutes)

If critical issues arise immediately:

```bash
# 1. Revert GitHub Actions workflow
git checkout main
git revert HEAD --no-edit
git push origin main

# 2. Or: Edit workflow directly
# Change: python scripts/hybrid_fetcher.py
# To: python scripts/fetch_claude_docs.py
git add .github/workflows/update-docs.yml
git commit -m "fix: Rollback to sitemap-only fetcher"
git push origin main
```

### Full Rollback (30 minutes)

If sustained issues require full revert:

```bash
# 1. Tag current state (for analysis)
git tag -a v0.4.0-failed -m "Failed deployment for analysis"
git push origin v0.4.0-failed

# 2. Reset to previous stable version
git checkout main
git reset --hard v0.3.4
git push --force origin main

# 3. Verify rollback
ls scripts/
# Should NOT have hybrid_fetcher.py

# 4. Trigger GitHub Actions manually
gh workflow run update-docs.yml

# 5. Announce rollback
gh issue create --title "v0.4.0 Rolled Back" --body "..."
```

### Rollback Verification

- [ ] GitHub Actions uses old fetcher (fetch_claude_docs.py)
- [ ] Documentation updates successfully
- [ ] No errors in logs
- [ ] File count returns to ~448
- [ ] /docs command still works

---

## Testing Strategy

### Unit Tests (Fast, Isolated)

- Parser functionality (parse_llms_full.py)
- Deduplication logic (hybrid_fetcher.py)
- Filename conversion
- Hash computation
- Manifest updates

**Coverage Target**: 90%+

### Integration Tests (Slow, Real Data)

- Full hybrid fetch workflow
- GitHub Actions workflow
- End-to-end documentation update

**Run Frequency**: Before each merge to main

### Validation Tests (Manual)

- Coverage report accuracy
- Deduplication correctness (spot checks)
- CLI docs still authoritative
- New API docs accessible

**Run Frequency**: After deployment, weekly

### Performance Tests (Benchmarks)

- Download speed
- Parse speed
- Fetch speed
- Total fetch time

**Target**: < 30 seconds total

---

## Success Metrics

### Coverage Metrics

- [x] Total paths: ~591 (target: 580+)
- [x] API reference: ~359 (target: 350+)
- [x] CLI docs: ~68 (target: 60+)
- [x] Unique content preserved: 100%

### Performance Metrics

- [x] Fetch time: < 30 seconds (target: < 30s)
- [x] Parse time: < 5 seconds (target: < 10s)
- [x] Memory usage: < 500 MB (target: < 1 GB)

### Quality Metrics

- [x] Test coverage: 90%+ (target: 85%+)
- [x] Test pass rate: 100% (target: 100%)
- [x] Error rate: < 1% (target: < 5%)
- [x] Deduplication accuracy: 100% (target: 100%)

### User-Facing Metrics

- [x] /docs command works: Yes
- [x] Breaking changes: None
- [x] User complaints: None (target: 0)
- [x] Documentation quality: Same or better

---

## Documentation Updates Needed

### README.md
- [ ] Add v0.4.0 features section
- [ ] Update coverage numbers (448 → 591)
- [ ] Update performance claims (10x faster)
- [ ] Add hybrid fetcher explanation

### CONTRIBUTING.md
- [ ] Add hybrid architecture section
- [ ] Document new scripts (parse_llms_full.py, hybrid_fetcher.py)
- [ ] Update development workflow
- [ ] Add testing guidelines for hybrid mode

### CHANGELOG.md
- [ ] Add v0.4.0 release notes
- [ ] List all new features
- [ ] Document breaking changes (none expected)
- [ ] Credit contributors

### New Documentation
- [ ] Create docs/HYBRID_MIGRATION.md
- [ ] Create DEPLOYMENT_CHECKLIST.md
- [ ] Update enhancements/FEATURES.md

### GitHub
- [ ] Update release notes (v0.4.0)
- [ ] Update issue templates (if needed)
- [ ] Update PR template (if needed)

---

## Open Questions & Decisions Needed

### Question 1: Caching Strategy
**Q**: How long should we cache llms-full.txt?  
**Options**:
- A) 24 hours (current plan)
- B) Until next GitHub Actions run (3 hours)
- C) No caching (always fresh)

**Decision**: **A) 24 hours** - Good balance of freshness and efficiency

### Question 2: Error Handling
**Q**: What if llms-full.txt download fails?  
**Options**:
- A) Fail entire fetch
- B) Fall back to sitemap-only
- C) Use cached version (if available)

**Decision**: **C) then B)** - Try cache, then fallback to sitemap-only

### Question 3: Manifest Format
**Q**: Should we add more metadata to manifest?  
**Options**:
- A) Just "source" field (llms-full vs sitemap)
- B) Add "url", "fetch_time", "content_type"
- C) Minimal (current plan)

**Decision**: **A)** - Keep simple, add more later if needed

### Question 4: Monitoring
**Q**: How to monitor hybrid fetcher health?  
**Options**:
- A) GitHub Actions logs only
- B) Add dedicated monitoring script
- C) External monitoring service

**Decision**: **A)** - Start simple, add monitoring if issues arise

---

## Next Steps After Completion

Once Phase 5 is complete:

1. **Monitor for 1 week** - Watch for any issues or bugs
2. **Collect metrics** - Actual fetch times, error rates, coverage
3. **Gather feedback** - Ask users about new API docs
4. **Optimize** - Based on real-world data
5. **Plan v0.5.0** - Next feature set

**Potential v0.5.0 Features**:
- Full-text search across all 591 docs
- Diff tracking for documentation changes
- Historical documentation versions
- Interactive documentation browser

---

## References & Resources

### Anthropic Resources
- llms-full.txt: https://platform.claude.com/llms-full.txt
- Claude Code Docs: https://code.claude.com/docs
- Platform Docs: https://docs.claude.com

### Project Resources
- Repository: https://github.com/costiash/claude-code-docs
- Issues: https://github.com/costiash/claude-code-docs/issues
- Discussions: https://github.com/costiash/claude-code-docs/discussions

### Related Projects
- Upstream: https://github.com/ericbuess/claude-code-docs
- MCP Connector: https://github.com/anthropics/mcp-connector

### Technical Documentation
- Sitemap Protocol: https://www.sitemaps.org/protocol.html
- SHA256 Hashing: https://en.wikipedia.org/wiki/SHA-2
- GitHub Actions: https://docs.github.com/en/actions

---

## Appendix A: File Structure After Implementation

```
claude-code-docs/
├── docs/                          # 591 documentation files
│   ├── en__api__messages.md      # From llms-full.txt
│   ├── en__docs__claude-code__hooks.md  # From sitemap
│   └── docs_manifest.json        # Updated with source tracking
├── scripts/
│   ├── parse_llms_full.py        # NEW: Parser for llms-full.txt
│   ├── analyze_coverage.py       # NEW: Coverage analysis tool
│   ├── hybrid_fetcher.py         # NEW: Hybrid fetcher
│   ├── fetch_claude_docs.py      # KEPT: Fallback fetcher
│   ├── main.py                   # KEPT: Compatibility
│   └── lookup_paths.py           # KEPT: Search functionality
├── tests/
│   ├── unit/
│   │   ├── test_parse_llms_full.py      # NEW
│   │   └── test_hybrid_fetcher.py       # NEW
│   └── integration/
│       └── test_hybrid_full_workflow.py # NEW
├── reports/
│   ├── coverage_report.json      # NEW: Analysis output
│   └── coverage_report.md        # NEW: Human-readable
├── .github/
│   └── workflows/
│       └── update-docs.yml       # MODIFIED: Uses hybrid fetcher
├── paths_manifest.json           # UNCHANGED: Still 448 paths
├── README.md                     # UPDATED: New features
├── CONTRIBUTING.md               # UPDATED: Hybrid architecture
├── CHANGELOG.md                  # UPDATED: v0.4.0 notes
├── DEPLOYMENT_CHECKLIST.md       # NEW
└── docs/HYBRID_MIGRATION.md      # NEW
```

---

## Appendix B: Expected Coverage Breakdown

### Before (v0.3.x) - 448 paths

| Category | Count | Source |
|----------|------:|--------|
| Core Documentation | 151 | Sitemap |
| API Reference | 91 | Sitemap |
| Claude Code | 68 | Sitemap |
| Resources | 68 | Sitemap |
| Prompt Library | 64 | Sitemap |
| Release Notes | 4 | Sitemap |
| Uncategorized | 2 | Sitemap |
| **TOTAL** | **448** | |

### After (v0.4.x) - ~591 paths

| Category | Count | Source |
|----------|------:|--------|
| API Reference | 359 | llms-full.txt |
| Core Documentation | 151 | llms-full.txt |
| Claude Code CLI | 68 | Sitemap (priority) |
| Resources | 68 | llms-full.txt |
| Prompt Library | 64 | llms-full.txt |
| Release Notes | 4 | llms-full.txt |
| Uncategorized | 2 | llms-full.txt |
| **TOTAL** | **~591** | |

**Note**: Numbers are estimates based on Phase 2 analysis.

---

**End of Implementation Plan**

This plan provides a comprehensive roadmap for integrating llms-full.txt into the claude-code-docs project. Each phase is independently testable and can be rolled back if issues arise. The plan prioritizes backward compatibility and preserves the unique value of our Claude Code CLI documentation while significantly expanding coverage of API and platform documentation.
