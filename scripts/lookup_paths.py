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

import requests

# Configuration
BASE_URL = "https://docs.anthropic.com"
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
    url = f"{base_url}{path}.md"

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


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Path lookup and validation utility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for paths
  %(prog)s "prompt engineering"
  %(prog)s "mcp"

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

    args = parser.parse_args()

    # Configure logging
    logger.setLevel(getattr(logging, args.log_level))

    try:
        # Load manifest
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
            return 0 if summary['not_found'] == 0 else 1

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
