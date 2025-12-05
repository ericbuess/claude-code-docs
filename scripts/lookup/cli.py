"""
Command-line interface for the path lookup utility.

This module contains the main() function that handles all CLI operations
for searching and validating documentation paths.
"""

import argparse
import json
from pathlib import Path

from .config import MAX_WORKERS, logger
from .manifest import load_paths_manifest, get_all_paths
from .search import (
    search_paths,
    create_enriched_search_results,
    search_content,
    load_search_index,
    suggest_alternatives,
)
from .validation import validate_path, batch_validate, load_batch_file
from .formatting import (
    print_search_results,
    print_validation_report,
    format_content_search_json,
    format_content_result,
)


def main():
    """Main entry point for the lookup utility."""
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
    import logging
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
