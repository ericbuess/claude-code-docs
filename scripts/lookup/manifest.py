"""
Manifest loading and path utilities.

This module handles loading the paths manifest and provides
utilities for working with documentation paths.
"""

import json
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional


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
    """Cached implementation of load_paths_manifest."""
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
