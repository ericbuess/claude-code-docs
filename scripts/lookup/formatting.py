"""
Output formatting utilities.

This module provides functions for formatting search results
and validation reports for display.
"""

import json
from typing import Dict, List, Tuple

from .manifest import get_category_for_path, get_product_label
from .validation import ValidationStats


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


def format_content_result(result: Dict, index: int) -> str:
    """
    Format content search result for display.

    Args:
        result: Search result dictionary
        index: Result index number

    Returns:
        Formatted string for display
    """
    return (
        f"\n{index}. {result['title']} (score: {result['score']})\n"
        f"   Path: {result['path']}\n"
        f"   Keywords: {', '.join(result['keywords'])}\n"
        f"   Preview: {result['preview'][:150]}{'...' if len(result['preview']) > 150 else ''}\n"
    )
