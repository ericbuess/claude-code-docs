#!/usr/bin/env python3
"""
Build full-text search index from documentation files.

This script:
1. Reads all markdown files in docs/
2. Extracts title, content, keywords
3. Builds searchable index
4. Saves to docs/.search_index.json
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set
from collections import Counter
import time


DOCS_DIR = Path("docs")
INDEX_FILE = DOCS_DIR / ".search_index.json"
STOP_WORDS = {
    'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
    'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
    'to', 'was', 'will', 'with', 'or', 'but', 'not', 'can', 'this',
    'we', 'you', 'all', 'if', 'have', 'do', 'use', 'your', 'how'
}


def extract_title(content: str) -> str:
    """Extract title from markdown (first # heading)"""
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    return match.group(1).strip() if match else "Untitled"


def extract_keywords(content: str, top_n: int = 20) -> List[str]:
    """Extract top keywords from content"""
    # Remove markdown syntax
    text = re.sub(r'```[\s\S]*?```', '', content)  # Code blocks
    text = re.sub(r'`[^`]+`', '', text)  # Inline code
    text = re.sub(r'##+\s*', '', text)  # Headers
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)  # Links
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)  # Non-alpha chars

    # Extract words
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())

    # Filter stop words
    words = [w for w in words if w not in STOP_WORDS]

    # Count and return top N
    counter = Counter(words)
    return [word for word, count in counter.most_common(top_n)]


def path_from_file(file_path: Path, docs_dir: Path) -> str:
    """
    Convert file path back to URL path.

    docs/en/docs/build-with-claude__prompt-engineering.md
    -> /en/docs/build-with-claude/prompt-engineering
    """
    relative_path = file_path.relative_to(docs_dir)
    path_str = str(relative_path.with_suffix(''))

    # Handle double underscore conversion
    path_str = path_str.replace('__', '/')

    # Ensure starts with /
    if not path_str.startswith('/'):
        path_str = '/' + path_str

    return path_str


def index_file(file_path: Path, docs_dir: Path) -> tuple[str, Dict]:
    """Index a single markdown file"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        print(f"  ✗ Error reading {file_path}: {e}")
        return None, None

    # Extract path
    doc_path = path_from_file(file_path, docs_dir)

    # Extract metadata
    title = extract_title(content)
    keywords = extract_keywords(content)
    word_count = len(content.split())

    # Content preview (first 200 chars, cleaned)
    preview = content[:300].replace('\n', ' ').strip()
    if len(preview) == 300:
        preview = preview[:200] + "..."

    doc_data = {
        "title": title,
        "content_preview": preview,
        "keywords": keywords,
        "word_count": word_count,
        "file_path": str(file_path)
    }

    return doc_path, doc_data


def build_index(docs_dir: Path = DOCS_DIR) -> Dict:
    """Build search index from all markdown files"""
    index = {}

    # Find all markdown files
    md_files = sorted(docs_dir.rglob("*.md"))

    print(f"Indexing {len(md_files)} markdown files...")

    success_count = 0
    error_count = 0

    for md_file in md_files:
        doc_path, doc_data = index_file(md_file, docs_dir)
        if doc_path and doc_data:
            index[doc_path] = doc_data
            success_count += 1
            print(f"  ✓ {doc_path}")
        else:
            error_count += 1

    print(f"\nIndexing complete:")
    print(f"  Success: {success_count}")
    print(f"  Errors: {error_count}")

    return {
        "version": "1.0",
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "indexed_files": len(index),
        "index": index
    }


def save_index(index: Dict, output_file: Path = INDEX_FILE):
    """Save index to JSON file"""
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w') as f:
        json.dump(index, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ SEARCH INDEX SAVED")
    print(f"   Output: {output_file}")
    print(f"   Files indexed: {index['indexed_files']}")
    print(f"   File size: {output_file.stat().st_size / 1024:.1f} KB")
    print(f"{'='*60}")


if __name__ == "__main__":
    import sys

    docs_directory = DOCS_DIR
    if len(sys.argv) > 1:
        docs_directory = Path(sys.argv[1])

    print(f"Building search index from {docs_directory}/...")
    index = build_index(docs_directory)
    save_index(index)

    print(f"\n✅ Complete! Search index ready for use.")
