#!/usr/bin/env python3
"""
Path Lookup and Validation Utility

Search, validate, and analyze documentation paths.

Features:
- Fuzzy search with relevance ranking
- URL reachability validation
- Batch validation with progress tracking
- Alternative suggestions for broken links
- Detailed validation reports
"""

import argparse
import json
import logging
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from difflib import get_close_matches
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from functools import lru_cache

import requests

# Configuration
BASE_URL = "https://code.claude.com/docs"
REQUEST_TIMEOUT = 10
MAX_WORKERS = 5  # Parallel validation threads

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationStats:
    """Track validation statistics"""

    def __init__(self):
        self.total = 0
        self.reachable = 0
        self.not_found = 0
        self.timeout = 0
        self.error = 0
        self.lock = threading.Lock()
        self.broken_paths: List[Dict] = []

    def add_result(self, path: str, status: str, status_code: Optional[int] = None):
        """Thread-safe result recording"""
        with self.lock:
            self.total += 1

            if status == 'reachable':
                self.reachable += 1
            elif status == 'not_found':
                self.not_found += 1
                self.broken_paths.append({
                    'path': path,
                    'status_code': status_code,
                    'reason': '404 Not Found'
                })
            elif status == 'timeout':
                self.timeout += 1
                self.broken_paths.append({
                    'path': path,
                    'status_code': None,
                    'reason': 'Timeout'
                })
            elif status == 'error':
                self.error += 1
                self.broken_paths.append({
                    'path': path,
                    'status_code': status_code,
                    'reason': 'HTTP Error'
                })

    def get_summary(self) -> Dict:
        """Get validation summary"""
        return {
            'total': self.total,
            'reachable': self.reachable,
            'not_found': self.not_found,
            'timeout': self.timeout,
            'error': self.error,
            'reachability_percent': round((self.reachable / self.total * 100), 2)
                                   if self.total > 0 else 0,
            'broken_paths': self.broken_paths
        }


def load_paths_manifest(manifest_path: Path) -> Dict:
    """
    Load paths manifest.

    Args:
        manifest_path: Path to manifest file

    Returns:
        Manifest dictionary

    Raises:
        FileNotFoundError: If manifest doesn't exist
    """
    return _load_paths_manifest_cached(str(manifest_path))


@lru_cache(maxsize=4)
def _load_paths_manifest_cached(manifest_path_str: str) -> Dict:
    """Cached implementation of load_paths_manifest"""
    manifest_path = Path(manifest_path_str)

    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_all_paths(manifest: Dict) -> List[str]:
    """
    Get flat list of all paths.

    Args:
        manifest: Paths manifest

    Returns:
        List of all paths
    """
    all_paths = []
    for category_paths in manifest.get('categories', {}).values():
        all_paths.extend(category_paths)

    return all_paths


def normalize_path_for_lookup(path: str) -> str:
    """
    Normalize path formats for consistent lookup.

    Handles different path formats between search index and manifest:
    - Search index: /en/docs/claude-code/hooks
    - Manifest: /docs/en/hooks

    Args:
        path: Original path

    Returns:
        Normalized path
    """
    # Handle Claude Code docs path conversion
    # /en/docs/claude-code/XXX -> /docs/en/XXX
    if path.startswith('/en/docs/claude-code/'):
        return path.replace('/en/docs/claude-code/', '/docs/en/')

    return path


def get_category_for_path(path: str, manifest: Dict) -> Optional[str]:
    """
    Get category for a given path.

    Handles path format differences between search index and manifest.

    Args:
        path: Documentation path
        manifest: Paths manifest

    Returns:
        Category name or None if not found
    """
    # Try exact match first
    for category, paths in manifest.get('categories', {}).items():
        if path in paths:
            return category

    # Try normalized path
    normalized = normalize_path_for_lookup(path)
    if normalized != path:
        for category, paths in manifest.get('categories', {}).items():
            if normalized in paths:
                return category

    return None


def get_product_label(category: str, path: str) -> str:
    """
    Map internal category to user-friendly product label.

    Args:
        category: Internal category name
        path: Documentation path (for disambiguation)

    Returns:
        User-friendly product label
    """
    # Category to product label mapping
    category_labels = {
        'claude_code': 'Claude Code CLI',
        'api_reference': 'Claude API',
        'core_documentation': 'Claude Documentation',
        'prompt_library': 'Prompt Library',
        'release_notes': 'Release Notes',
        'resources': 'Resources',
        'uncategorized': 'Uncategorized'
    }

    # Special case: Agent SDK paths within api_reference
    if category == 'api_reference' and '/docs/agent-sdk/' in path:
        return 'Claude Agent SDK'

    return category_labels.get(category, category.replace('_', ' ').title())


def search_paths(
    query: str,
    manifest: Dict,
    max_results: int = 20
) -> List[Tuple[str, float]]:
    """
    Fuzzy search for paths matching query.

    Args:
        query: Search query
        manifest: Paths manifest
        max_results: Maximum number of results to return

    Returns:
        List of (path, relevance_score) tuples, sorted by relevance
    """
    query_lower = query.lower()
    all_paths = get_all_paths(manifest)

    # Score each path
    scored_paths = []

    for path in all_paths:
        path_lower = path.lower()
        score = 0.0

        # Exact match (highest score)
        if query_lower == path_lower:
            score = 100.0

        # Substring match
        elif query_lower in path_lower:
            # Bonus for match at start or in last segment
            if path_lower.startswith(query_lower):
                score = 80.0
            elif query_lower in path_lower.split('/')[-1]:
                score = 70.0
            else:
                score = 60.0

        # Word match (query words in path)
        else:
            query_words = query_lower.replace('-', ' ').split()
            path_words = path_lower.replace('/', ' ').replace('-', ' ').split()

            matches = sum(1 for word in query_words if word in path_words)
            if matches > 0:
                score = 40.0 * (matches / len(query_words))

        # Fuzzy match as fallback
        if score == 0:
            # Use difflib for similarity
            similarity = sum(
                1 for q, p in zip(query_lower, path_lower) if q == p
            ) / max(len(query_lower), len(path_lower))

            if similarity > 0.3:
                score = similarity * 30.0

        if score > 0:
            scored_paths.append((path, score))

    # Sort by score (descending) and return top results
    scored_paths.sort(key=lambda x: x[1], reverse=True)

    return scored_paths[:max_results]


def create_enriched_search_results(
    results: List[Tuple[str, float]],
    manifest: Dict,
    query: str
) -> Dict:
    """
    Create enriched search results with product context.

    Args:
        results: List of (path, score) tuples from search
        manifest: Paths manifest
        query: Original search query

    Returns:
        Dictionary with enriched results and product summary
    """
    enriched_results = []
    product_counts = {}

    for path, score in results:
        category = get_category_for_path(path, manifest)
        product = get_product_label(category, path) if category else "Unknown"

        enriched_results.append({
            "path": path,
            "category": category,
            "product": product,
            "score": round(score, 1)
        })

        # Count products
        product_counts[product] = product_counts.get(product, 0) + 1

    return {
        "query": query,
        "total_results": len(enriched_results),
        "results": enriched_results,
        "product_summary": product_counts,
        "unique_products": len(product_counts)
    }


def format_content_search_json(
    results: List[Dict],
    query: str,
    manifest: Dict
) -> Dict:
    """
    Format content search results as JSON with product context.

    Args:
        results: Content search results
        query: Search query
        manifest: Paths manifest

    Returns:
        JSON-formatted results with product context
    """
    enriched_results = []
    product_counts = {}

    for result in results:
        path = result.get('path', '')
        category = get_category_for_path(path, manifest)
        product = get_product_label(category, path) if category else "Unknown"

        enriched_results.append({
            "path": path,
            "title": result.get('title', 'Untitled'),
            "category": category,
            "product": product,
            "score": result.get('score', 0),
            "preview": result.get('preview', '')[:150],
            "keywords": result.get('keywords', [])[:5]
        })

        # Count products
        product_counts[product] = product_counts.get(product, 0) + 1

    return {
        "query": query,
        "total_results": len(enriched_results),
        "results": enriched_results,
        "product_summary": product_counts,
        "unique_products": len(product_counts)
    }


def validate_path(
    path: str,
    base_url: str = BASE_URL,
    timeout: int = REQUEST_TIMEOUT
) -> Dict:
    """
    Validate that a path is reachable.

    Args:
        path: Documentation path to validate
        base_url: Base URL for documentation site
        timeout: Request timeout in seconds

    Returns:
        Validation result dictionary
    """
    # Note: code.claude.com URLs don't use .md extension
    url = f"{base_url}{path}"

    try:
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True
        )

        return {
            'path': path,
            'url': url,
            'status_code': response.status_code,
            'reachable': response.status_code == 200,
            'redirect': response.url if response.url != url else None,
            'error': None
        }

    except requests.exceptions.Timeout:
        return {
            'path': path,
            'url': url,
            'status_code': None,
            'reachable': False,
            'redirect': None,
            'error': 'Timeout'
        }

    except requests.exceptions.RequestException as e:
        return {
            'path': path,
            'url': url,
            'status_code': None,
            'reachable': False,
            'redirect': None,
            'error': str(e)
        }


def batch_validate(
    paths: List[str],
    base_url: str = BASE_URL,
    max_workers: int = MAX_WORKERS
) -> ValidationStats:
    """
    Validate multiple paths in parallel.

    Args:
        paths: List of paths to validate
        base_url: Base URL for documentation site
        max_workers: Number of parallel workers

    Returns:
        ValidationStats object
    """
    stats = ValidationStats()

    logger.info(f"Validating {len(paths)} paths with {max_workers} workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_path = {
            executor.submit(validate_path, path, base_url): path
            for path in paths
        }

        # Process results as they complete
        for i, future in enumerate(as_completed(future_to_path), 1):
            path = future_to_path[future]

            try:
                result = future.result()

                # Update stats
                if result['reachable']:
                    stats.add_result(path, 'reachable')
                    logger.debug(f"✓ {path}")
                elif result['error'] == 'Timeout':
                    stats.add_result(path, 'timeout')
                    logger.warning(f"⏱ Timeout: {path}")
                elif result['status_code'] == 404:
                    stats.add_result(path, 'not_found', 404)
                    logger.warning(f"✗ 404: {path}")
                else:
                    stats.add_result(path, 'error', result['status_code'])
                    logger.warning(f"✗ Error: {path} ({result['error']})")

                # Progress indicator
                if i % 10 == 0 or i == len(paths):
                    progress = (i / len(paths)) * 100
                    logger.info(f"Progress: {i}/{len(paths)} ({progress:.1f}%)")

            except Exception as e:
                logger.error(f"Exception validating {path}: {e}")
                stats.add_result(path, 'error')

    return stats


def suggest_alternatives(
    path: str,
    manifest: Dict,
    max_suggestions: int = 5
) -> List[str]:
    """
    Suggest alternative paths for a broken link.

    Args:
        path: Broken path
        manifest: Paths manifest
        max_suggestions: Maximum suggestions to return

    Returns:
        List of suggested alternative paths
    """
    all_paths = get_all_paths(manifest)

    # Use difflib for fuzzy matching
    matches = get_close_matches(
        path,
        all_paths,
        n=max_suggestions,
        cutoff=0.6
    )

    return matches


def load_batch_file(file_path: Path) -> List[str]:
    """
    Load paths from a file (one per line).

    Args:
        file_path: Path to file

    Returns:
        List of paths
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        paths = [line.strip() for line in f if line.strip()]

    return paths


def print_search_results(results: List[Tuple[str, float]], query: str):
    """
    Print formatted search results.

    Args:
        results: List of (path, score) tuples
        query: Original search query
    """
    if not results:
        print(f"\nNo results found for query: '{query}'")
        return

    print(f"\nFound {len(results)} results for query: '{query}'\n")
    print("="*70)

    for i, (path, score) in enumerate(results, 1):
        # Determine relevance indicator
        if score >= 80:
            indicator = "★★★"
        elif score >= 60:
            indicator = "★★"
        else:
            indicator = "★"

        print(f"{i:2d}. {indicator} {path}")
        print(f"    Relevance: {score:.1f}%")
        print()

    print("="*70)


def print_validation_report(stats: ValidationStats):
    """
    Print formatted validation report.

    Args:
        stats: ValidationStats object
    """
    summary = stats.get_summary()

    print("\n" + "="*70)
    print("VALIDATION REPORT")
    print("="*70)
    print(f"Total paths validated: {summary['total']}")
    print(f"  Reachable (200 OK): {summary['reachable']} "
          f"({summary['reachability_percent']}%)")
    print(f"  Not found (404): {summary['not_found']}")
    print(f"  Timeout: {summary['timeout']}")
    print(f"  Other errors: {summary['error']}")
    print()

    if summary['broken_paths']:
        print(f"BROKEN PATHS ({len(summary['broken_paths'])}):")
        print("-"*70)

        for broken in summary['broken_paths'][:20]:  # Show first 20
            status = broken['status_code'] if broken['status_code'] else "N/A"
            print(f"  [{status}] {broken['path']}")
            print(f"       {broken['reason']}")

        if len(summary['broken_paths']) > 20:
            remaining = len(summary['broken_paths']) - 20
            print(f"\n  ... and {remaining} more broken paths")

    print("="*70)


@lru_cache(maxsize=1)
def load_search_index() -> Optional[Dict]:
    """Load full-text search index (cached)"""
    index_file = Path("docs/.search_index.json")
    if not index_file.exists():
        return None

    try:
        with open(index_file) as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading search index: {e}")
        return None


def search_content(query: str, index: Dict, max_results: int = 20) -> List[Dict]:
    """
    Search document content for query.

    Returns list of matching documents with relevance scores.
    """
    if not index or "index" not in index:
        return []

    query_lower = query.lower()
    query_words = set(query_lower.split())

    results = []

    for path, doc in index["index"].items():
        # Calculate relevance score
        score = 0

        # Title match (highest weight)
        if query_lower in doc.get("title", "").lower():
            score += 100

        # Keyword match (medium weight)
        keywords = doc.get("keywords", [])
        keyword_matches = len(query_words & set(keywords))
        score += keyword_matches * 10

        # Preview match (low weight)
        preview = doc.get("content_preview", "")
        if query_lower in preview.lower():
            score += 20

        # Exact word matches in keywords (bonus)
        for word in query_words:
            if word in keywords:
                score += 5

        if score > 0:
            results.append({
                "path": path,
                "title": doc.get("title", "Untitled"),
                "score": score,
                "preview": preview,
                "file": doc.get("file_path", ""),
                "keywords": keywords[:5]  # Top 5 keywords
            })

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:max_results]


def format_content_result(result: Dict, index: int) -> str:
    """Format content search result for display"""
    return (
        f"\n{index}. {result['title']} (score: {result['score']})\n"
        f"   Path: {result['path']}\n"
        f"   Keywords: {', '.join(result['keywords'])}\n"
        f"   Preview: {result['preview'][:150]}{'...' if len(result['preview']) > 150 else ''}\n"
    )


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Path lookup and validation utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for paths (by name)
  %(prog)s "prompt engineering"
  %(prog)s "mcp"

  # Search documentation content (full-text)
  %(prog)s --search-content "extended thinking"
  %(prog)s --search-content "tool use"

  # Validate specific path
  %(prog)s --check /en/docs/claude-code/hooks

  # Validate all paths
  %(prog)s --validate-all

  # Validate paths from file
  %(prog)s --batch-validate sample_paths.txt

  # Get suggestions for broken path
  %(prog)s --suggest /en/docs/old-page
        """
    )

    parser.add_argument(
        'query',
        nargs='?',
        help='Search query (if no other options specified)'
    )

    parser.add_argument(
        '--check',
        metavar='PATH',
        help='Validate specific path'
    )

    parser.add_argument(
        '--validate-all',
        action='store_true',
        help='Validate all paths in manifest'
    )

    parser.add_argument(
        '--batch-validate',
        metavar='FILE',
        type=Path,
        help='Validate paths from file (one per line)'
    )

    parser.add_argument(
        '--suggest',
        metavar='PATH',
        help='Suggest alternatives for broken path'
    )

    parser.add_argument(
        '--search-content',
        metavar='QUERY',
        help='Search documentation content (full-text search)'
    )

    parser.add_argument(
        '--manifest',
        type=Path,
        default=Path('paths_manifest.json'),
        help='Path to paths manifest (default: paths_manifest.json)'
    )

    parser.add_argument(
        '--max-results',
        type=int,
        default=20,
        help='Maximum search results (default: 20)'
    )

    parser.add_argument(
        '--max-workers',
        type=int,
        default=MAX_WORKERS,
        help=f'Parallel validation workers (default: {MAX_WORKERS})'
    )

    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help='Logging level (default: INFO)'
    )

    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON with product context'
    )

    args = parser.parse_args()

    # Configure logging
    logger.setLevel(getattr(logging, args.log_level))

    try:
        # Handle content search first (doesn't need manifest initially)
        if args.search_content:
            index = load_search_index()
            if not index:
                print("❌ Search index not found.")
                print("Run: python scripts/build_search_index.py")
                return 1

            results = search_content(args.search_content, index, args.max_results)

            if args.json:
                # Load manifest for product context
                manifest = load_paths_manifest(args.manifest)
                json_output = format_content_search_json(results, args.search_content, manifest)
                print(json.dumps(json_output, indent=2))
            else:
                print(f"Searching content for: '{args.search_content}'")
                if results:
                    print(f"\n✅ Found {len(results)} matching documents:\n")
                    for i, result in enumerate(results, 1):
                        print(format_content_result(result, i))
                else:
                    print("No matching documents found.")

            return 0

        # Load manifest for path-based operations
        manifest = load_paths_manifest(args.manifest)

        # Determine operation mode
        if args.check:
            # Validate single path
            logger.info(f"Validating path: {args.check}")
            result = validate_path(args.check)

            print(f"\nPath: {result['path']}")
            print(f"URL: {result['url']}")
            print(f"Status: {result['status_code']}")
            print(f"Reachable: {'Yes' if result['reachable'] else 'No'}")

            if result['redirect']:
                print(f"Redirected to: {result['redirect']}")

            if result['error']:
                print(f"Error: {result['error']}")

            return 0 if result['reachable'] else 1

        elif args.validate_all:
            # Validate all paths
            all_paths = get_all_paths(manifest)
            stats = batch_validate(all_paths, max_workers=args.max_workers)
            print_validation_report(stats)

            summary = stats.get_summary()
            # Allow a small number of broken paths (< 5%)
            # Some paths may be temporarily unavailable or deprecated
            failure_rate = (summary['not_found'] + summary['timeout']) / summary['total'] if summary['total'] > 0 else 0
            if failure_rate > 0.05:
                logger.warning(f"Validation warning: {failure_rate*100:.1f}% of paths unreachable ({summary['not_found'] + summary['timeout']}/{summary['total']})")
                return 1
            else:
                logger.info(f"✅ Validation passed: {100-failure_rate*100:.1f}% of paths reachable")
                return 0

        elif args.batch_validate:
            # Validate paths from file
            paths = load_batch_file(args.batch_validate)
            logger.info(f"Loaded {len(paths)} paths from {args.batch_validate}")

            stats = batch_validate(paths, max_workers=args.max_workers)
            print_validation_report(stats)

            summary = stats.get_summary()
            return 0 if summary['not_found'] == 0 else 1

        elif args.suggest:
            # Suggest alternatives
            suggestions = suggest_alternatives(args.suggest, manifest)

            print(f"\nSuggested alternatives for: {args.suggest}\n")

            if suggestions:
                for i, suggestion in enumerate(suggestions, 1):
                    print(f"{i}. {suggestion}")
            else:
                print("No suggestions found")

            return 0

        elif args.query:
            # Search for paths
            results = search_paths(args.query, manifest, args.max_results)

            if args.json:
                json_output = create_enriched_search_results(results, manifest, args.query)
                print(json.dumps(json_output, indent=2))
            else:
                print_search_results(results, args.query)

            return 0

        else:
            parser.error("Must specify query, --check, --validate-all, "
                        "--batch-validate, or --suggest")

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    except KeyboardInterrupt:
        logger.warning("\nInterrupted by user")
        return 130

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
