"""
Search functionality for documentation paths.

This module provides:
- Fuzzy search for paths
- Full-text content search
- Alternative suggestions for broken links
"""

import json
from difflib import get_close_matches
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from .config import logger
from .manifest import get_all_paths, get_category_for_path, get_product_label


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


@lru_cache(maxsize=1)
def load_search_index() -> Optional[Dict]:
    """Load full-text search index (cached)."""
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

    Args:
        query: Search query
        index: Search index dictionary
        max_results: Maximum results to return

    Returns:
        List of matching documents with relevance scores
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
