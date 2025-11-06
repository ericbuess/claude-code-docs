#!/usr/bin/env python3
"""
Claude Code Documentation Fetcher

Production-ready script for fetching and maintaining local mirror of
Anthropic's Claude documentation.

Features:
- Direct markdown fetching (no HTML parsing needed)
- Retry logic with exponential backoff
- SHA256-based change detection
- Rate limiting and throttling
- Comprehensive error handling
- Progress tracking
- Incremental updates

Based on analysis of costiash/claude-code-docs implementation.
"""

import argparse
import hashlib
import json
import logging
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

import requests

# Configuration
BASE_URL = "https://docs.anthropic.com"
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/1.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

MAX_RETRIES = 3
RETRY_DELAY = 2  # initial delay in seconds
MAX_RETRY_DELAY = 30  # maximum delay
RATE_LIMIT_DELAY = 0.5  # delay between requests in seconds
REQUEST_TIMEOUT = 30  # request timeout in seconds

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FetchStats:
    """Track fetching statistics"""

    def __init__(self):
        self.success_count = 0
        self.failed_count = 0
        self.skipped_count = 0
        self.updated_count = 0
        self.errors: List[Dict] = []
        self.start_time = time.time()

    def add_success(self, _path: str, updated: bool = False):
        """Record successful fetch"""
        self.success_count += 1
        if updated:
            self.updated_count += 1

    def add_skip(self, _path: str):
        """Record skipped (unchanged) file"""
        self.skipped_count += 1

    def add_error(self, path: str, error: str):
        """Record error"""
        self.failed_count += 1
        self.errors.append({'path': path, 'error': error})

    def get_summary(self) -> Dict:
        """Get statistics summary"""
        elapsed = time.time() - self.start_time
        return {
            'total_processed': self.success_count + self.skipped_count,
            'success': self.success_count,
            'updated': self.updated_count,
            'skipped': self.skipped_count,
            'failed': self.failed_count,
            'elapsed_seconds': round(elapsed, 2),
            'errors': self.errors
        }


def load_paths_manifest(manifest_path: Path) -> Dict:
    """
    Load paths from manifest file.

    Args:
        manifest_path: Path to paths_manifest.json

    Returns:
        Dictionary containing metadata and categorized paths

    Raises:
        FileNotFoundError: If manifest file doesn't exist
        json.JSONDecodeError: If manifest is invalid JSON
    """
    logger.info(f"Loading paths from {manifest_path}")

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest file not found: {manifest_path}")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    logger.info(f"Loaded {manifest['metadata']['total_paths']} paths "
                f"across {manifest['metadata']['categories_count']} categories")

    return manifest


def load_docs_manifest(manifest_path: Path) -> Dict:
    """
    Load existing documentation manifest (for change detection).

    Args:
        manifest_path: Path to docs_manifest.json

    Returns:
        Dictionary mapping paths to metadata (hash, last_updated, etc.)
    """
    if not manifest_path.exists():
        logger.info("No existing docs manifest found, creating new one")
        return {}

    try:
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        logger.warning("Invalid docs manifest, starting fresh")
        return {}


def save_docs_manifest(manifest_path: Path, manifest: Dict):
    """
    Save documentation manifest with metadata.

    Args:
        manifest_path: Path to docs_manifest.json
        manifest: Manifest dictionary to save
    """
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved manifest to {manifest_path}")


def compute_content_hash(content: str) -> str:
    """
    Compute SHA256 hash of content.

    Args:
        content: Text content to hash

    Returns:
        Hex digest of SHA256 hash
    """
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def content_has_changed(content: str, old_hash: Optional[str]) -> bool:
    """
    Check if content has changed by comparing hashes.

    Args:
        content: New content
        old_hash: Previous content hash (or None)

    Returns:
        True if content changed or no previous hash exists
    """
    if old_hash is None:
        return True

    new_hash = compute_content_hash(content)
    return new_hash != old_hash


def validate_markdown_content(content: str, path: str) -> bool:
    """
    Validate that content appears to be valid markdown.

    Args:
        content: Content to validate
        path: Path (for logging)

    Returns:
        True if content appears valid, False otherwise
    """
    # Check it's not HTML
    if content.startswith('<!DOCTYPE') or '<html' in content[:100].lower():
        logger.error(f"Received HTML instead of markdown for {path}")
        return False

    # Check minimum length
    if len(content.strip()) < 50:
        logger.error(f"Content too short ({len(content)} bytes) for {path}")
        return False

    # Check for markdown indicators in first 50 lines
    lines = content.split('\n')[:50]
    markdown_indicators = ['# ', '## ', '```', '- ', '[', '**', '_', '> ']
    indicator_count = sum(1 for line in lines
                         for indicator in markdown_indicators
                         if indicator in line)

    if indicator_count < 3:
        logger.warning(f"Content doesn't appear to be markdown for {path} "
                      f"(only {indicator_count} indicators found)")
        return False

    return True


def fetch_page(
    path: str,
    session: requests.Session,
    base_url: str = BASE_URL
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Fetch markdown content for a documentation page.

    Args:
        path: Documentation path (e.g., /en/docs/claude-code/hooks)
        session: Requests session for connection pooling
        base_url: Base URL for documentation site

    Returns:
        Tuple of (success, content, error_message)
    """
    markdown_url = f"{base_url}{path}.md"

    for attempt in range(MAX_RETRIES):
        try:
            logger.debug(f"Fetching {markdown_url} (attempt {attempt + 1}/{MAX_RETRIES})")

            response = session.get(
                markdown_url,
                headers=HEADERS,
                timeout=REQUEST_TIMEOUT
            )

            # Handle rate limiting
            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited for {path}. Waiting {wait_time}s...")
                time.sleep(wait_time)
                continue

            # Handle not found
            if response.status_code == 404:
                logger.warning(f"Page not found: {path}")
                return False, None, "404 Not Found"

            # Raise for other HTTP errors
            response.raise_for_status()

            # Get content
            content = response.text

            # Validate content
            if not validate_markdown_content(content, path):
                return False, None, "Content validation failed"

            logger.debug(f"Successfully fetched {path} ({len(content)} bytes)")
            return True, content, None

        except requests.exceptions.Timeout:
            logger.warning(f"Timeout fetching {path} (attempt {attempt + 1})")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.debug(f"Retrying after {jittered_delay:.1f}s...")
                time.sleep(jittered_delay)
            else:
                return False, None, "Timeout after retries"

        except requests.exceptions.RequestException as e:
            logger.warning(f"Request error fetching {path}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.debug(f"Retrying after {jittered_delay:.1f}s...")
                time.sleep(jittered_delay)
            else:
                return False, None, f"Request failed: {str(e)}"

    return False, None, "Max retries exceeded"


@lru_cache(maxsize=1024)
def path_to_filename(path: str) -> str:
    """
    Convert documentation path to safe filename.

    Args:
        path: Documentation path (e.g., /en/docs/claude-code/hooks)

    Returns:
        Safe filename with .md extension

    Example:
        /en/docs/claude-code/hooks -> en__docs__claude-code__hooks.md
    """
    # Remove leading slash
    if path.startswith('/'):
        path = path[1:]

    # Replace slashes with double underscores (flat structure)
    filename = path.replace('/', '__')

    # Add .md extension if not present
    if not filename.endswith('.md'):
        filename += '.md'

    return filename


def save_documentation(
    path: str,
    content: str,
    output_dir: Path
) -> bool:
    """
    Save documentation content to file.

    Args:
        path: Documentation path
        content: Markdown content
        output_dir: Output directory for documentation

    Returns:
        True if saved successfully, False otherwise
    """
    try:
        # Create output directory if needed
        output_dir.mkdir(parents=True, exist_ok=True)

        # Convert path to filename
        filename = path_to_filename(path)
        file_path = output_dir / filename

        # Write content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.debug(f"Saved {path} to {file_path}")
        return True

    except IOError as e:
        logger.error(f"Failed to save {path}: {e}")
        return False


def update_documentation(
    paths: List[str],
    output_dir: Path,
    manifest_path: Path,
    force: bool = False,
    rate_limit: float = RATE_LIMIT_DELAY
) -> FetchStats:
    """
    Update documentation for specified paths.

    Args:
        paths: List of documentation paths to fetch
        output_dir: Directory to save documentation
        manifest_path: Path to docs_manifest.json
        force: If True, re-fetch all pages regardless of changes
        rate_limit: Delay between requests in seconds

    Returns:
        FetchStats object with statistics
    """
    stats = FetchStats()

    # Load existing manifest for change detection
    docs_manifest = load_docs_manifest(manifest_path)

    # Create session for connection pooling
    session = requests.Session()

    logger.info(f"Starting update of {len(paths)} documentation pages")
    if force:
        logger.info("Force mode: re-fetching all pages")

    total = len(paths)

    for i, path in enumerate(paths, 1):
        # Progress indicator
        progress_pct = (i / total) * 100
        logger.info(f"[{i}/{total}] ({progress_pct:.1f}%) Processing {path}")

        # Fetch page
        success, content, error = fetch_page(path, session)

        if not success:
            logger.error(f"Failed to fetch {path}: {error}")
            stats.add_error(path, error or "Unknown error")
            continue

        # Check if content changed (unless force mode)
        old_entry = docs_manifest.get(path, {})
        old_hash = old_entry.get('hash')

        if not force and not content_has_changed(content, old_hash):
            logger.info(f"Skipping {path} (unchanged)")
            stats.add_skip(path)
            # Rate limiting even for skipped files
            if i < total:
                time.sleep(rate_limit)
            continue

        # Save documentation
        if save_documentation(path, content, output_dir):
            # Update manifest entry
            new_hash = compute_content_hash(content)
            docs_manifest[path] = {
                'hash': new_hash,
                'last_updated': datetime.now(timezone.utc).isoformat(),
                'size': len(content)
            }

            is_new = old_hash is None
            if is_new:
                logger.info(f"Added new page: {path}")
            else:
                logger.info(f"Updated page: {path}")

            stats.add_success(path, updated=(not is_new))
        else:
            stats.add_error(path, "Failed to save file")

        # Rate limiting (except on last page)
        if i < total:
            time.sleep(rate_limit)

    # Save updated manifest
    save_docs_manifest(manifest_path, docs_manifest)

    # Log summary
    summary = stats.get_summary()
    logger.info("\n" + "="*60)
    logger.info("UPDATE SUMMARY")
    logger.info("="*60)
    logger.info(f"Total processed: {summary['total_processed']}")
    logger.info(f"  Success: {summary['success']}")
    logger.info(f"    New: {summary['success'] - summary['updated']}")
    logger.info(f"    Updated: {summary['updated']}")
    logger.info(f"  Skipped (unchanged): {summary['skipped']}")
    logger.info(f"  Failed: {summary['failed']}")
    logger.info(f"Time elapsed: {summary['elapsed_seconds']}s")

    if summary['errors']:
        logger.info("\nERRORS:")
        for error in summary['errors'][:10]:  # Show first 10 errors
            logger.info(f"  {error['path']}: {error['error']}")
        if len(summary['errors']) > 10:
            logger.info(f"  ... and {len(summary['errors']) - 10} more")

    logger.info("="*60)

    return stats


def get_category_paths(manifest: Dict, category: str) -> List[str]:
    """
    Get all paths for a specific category.

    Args:
        manifest: Paths manifest dictionary
        category: Category name (core_documentation, api_reference, etc.)

    Returns:
        List of paths in category

    Raises:
        ValueError: If category doesn't exist
    """
    categories = manifest.get('categories', {})

    if category not in categories:
        available = ', '.join(categories.keys())
        raise ValueError(f"Category '{category}' not found. "
                        f"Available: {available}")

    return categories[category]


def get_all_paths(manifest: Dict) -> List[str]:
    """
    Get all paths from all categories.

    Args:
        manifest: Paths manifest dictionary

    Returns:
        Flat list of all paths
    """
    all_paths = []
    for category_paths in manifest.get('categories', {}).values():
        all_paths.extend(category_paths)

    return all_paths


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Claude Code Documentation Fetcher',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update all documentation
  %(prog)s --update-all

  # Update specific category
  %(prog)s --update-category core_documentation

  # Force re-fetch all pages
  %(prog)s --update-all --force

  # Verify existing docs (dry run)
  %(prog)s --verify
        """
    )

    parser.add_argument(
        '--update-all',
        action='store_true',
        help='Update all documentation across all categories'
    )

    parser.add_argument(
        '--update-category',
        metavar='CATEGORY',
        help='Update specific category (core_documentation, api_reference, '
             'claude_code, prompt_library, resources, release_notes)'
    )

    parser.add_argument(
        '--force',
        action='store_true',
        help='Force re-fetch all pages (ignore change detection)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs'),
        help='Output directory for documentation (default: docs/)'
    )

    parser.add_argument(
        '--manifest',
        type=Path,
        default=Path('paths_manifest.json'),
        help='Path to paths manifest (default: paths_manifest.json)'
    )

    parser.add_argument(
        '--docs-manifest',
        type=Path,
        default=Path('docs/docs_manifest.json'),
        help='Path to docs manifest (default: docs/docs_manifest.json)'
    )

    parser.add_argument(
        '--rate-limit',
        type=float,
        default=RATE_LIMIT_DELAY,
        help=f'Delay between requests in seconds (default: {RATE_LIMIT_DELAY})'
    )

    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )

    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify mode: check existing docs without fetching'
    )

    args = parser.parse_args()

    # Configure logging
    logger.setLevel(getattr(logging, args.log_level))

    # Validate arguments
    if not args.update_all and not args.update_category and not args.verify:
        parser.error("Must specify --update-all, --update-category, or --verify")

    try:
        # Load paths manifest
        manifest = load_paths_manifest(args.manifest)

        # Determine which paths to process
        if args.update_all:
            paths = get_all_paths(manifest)
            logger.info(f"Processing all {len(paths)} paths")
        elif args.update_category:
            paths = get_category_paths(manifest, args.update_category)
            logger.info(f"Processing {len(paths)} paths in category "
                       f"'{args.update_category}'")
        else:  # verify mode
            logger.info("Verify mode - checking existing documentation")
            docs_manifest = load_docs_manifest(args.docs_manifest)
            logger.info(f"Found {len(docs_manifest)} documented pages")
            return 0

        # Update documentation
        stats = update_documentation(
            paths=paths,
            output_dir=args.output_dir,
            manifest_path=args.docs_manifest,
            force=args.force,
            rate_limit=args.rate_limit
        )

        # Exit with error if any failures
        summary = stats.get_summary()
        if summary['failed'] > 0:
            logger.error(f"Completed with {summary['failed']} failures")
            return 1

        logger.info("Update completed successfully!")
        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    except ValueError as e:
        logger.error(f"Invalid input: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 130

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
