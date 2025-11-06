#!/usr/bin/env python3
"""
Sitemap and Index Management

Generates sitemap and search indexes for Claude documentation mirror.

Features:
- Category-specific indexes
- Full sitemap generation
- Search index optimization
- Hierarchical tree generation
- Compatibility with upstream format
"""

import argparse
import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_paths_manifest(manifest_path: Path) -> Dict:
    """
    Load paths manifest.

    Args:
        manifest_path: Path to paths_manifest.json

    Returns:
        Manifest dictionary

    Raises:
        FileNotFoundError: If manifest doesn't exist
        json.JSONDecodeError: If manifest is invalid
    """
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_docs_manifest(manifest_path: Path) -> Dict:
    """
    Load documentation manifest with metadata.

    Args:
        manifest_path: Path to docs_manifest.json

    Returns:
        Docs manifest or empty dict if doesn't exist
    """
    if not manifest_path.exists():
        logger.warning(f"Docs manifest not found: {manifest_path}")
        return {}

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    # Handle upstream format (nested under "files" key)
    if 'files' in manifest and isinstance(manifest['files'], dict):
        return manifest['files']

    return manifest


def build_path_tree(paths: List[str]) -> Dict:
    """
    Build hierarchical tree from flat path list.

    Args:
        paths: List of documentation paths

    Returns:
        Nested dictionary representing path hierarchy

    Example:
        ['/en/docs/foo', '/en/docs/foo/bar']
        -> {'en': {'docs': {'foo': {'bar': {}}}}}
    """
    tree = {}

    for path in paths:
        # Remove leading slash and split
        parts = path.lstrip('/').split('/')

        # Navigate/create tree structure
        current = tree
        for part in parts:
            if part not in current:
                current[part] = {}
            current = current[part]

    return tree


def count_tree_leaves(tree: Dict) -> int:
    """
    Count leaf nodes in tree (endpoints).

    Args:
        tree: Nested dictionary

    Returns:
        Number of leaf nodes
    """
    if not tree:
        return 1  # Empty dict is a leaf

    return sum(count_tree_leaves(subtree) for subtree in tree.values())


def tree_to_list(tree: Dict, prefix: str = "") -> List[str]:
    """
    Convert tree back to flat list of paths.

    Args:
        tree: Nested dictionary
        prefix: Current path prefix

    Returns:
        List of paths
    """
    paths = []

    if not tree:  # Leaf node
        if prefix:
            paths.append(prefix)
        return paths

    for key, subtree in tree.items():
        new_prefix = f"{prefix}/{key}" if prefix else f"/{key}"
        paths.extend(tree_to_list(subtree, new_prefix))

    return paths


def path_to_filename(path: str) -> str:
    """Convert path to filename format (upstream uses filenames as keys)."""
    if path.startswith('/'):
        path = path[1:]
    filename = path.replace('/', '__') + '.md'
    # Upstream uses direct filename without en__ prefix
    if filename.startswith('en__'):
        filename = filename[4:]  # Remove en__ prefix
    return filename


def generate_category_index(
    category_name: str,
    paths: List[str],
    docs_manifest: Dict
) -> Dict:
    """
    Generate index for a category.

    Args:
        category_name: Category name
        paths: List of paths in category
        docs_manifest: Documentation manifest with metadata

    Returns:
        Category index dictionary
    """
    # Build hierarchical tree
    tree = build_path_tree(paths)

    # Gather statistics
    total_size = 0
    last_updated = None

    for path in paths:
        # Try to find entry by path or by filename
        filename = path_to_filename(path)
        entry = docs_manifest.get(path) or docs_manifest.get(filename)

        if entry and isinstance(entry, dict):
            # Handle different manifest formats
            size = entry.get('size', 0)
            if size == 0:
                # Estimate size if not present (won't be in upstream format)
                size = 0

            total_size += size

            updated_str = entry.get('last_updated')
            if updated_str:
                try:
                    updated = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
                    if last_updated is None or updated > last_updated:
                        last_updated = updated
                except (ValueError, AttributeError):
                    pass

    return {
        'category': category_name,
        'count': len(paths),
        'total_size_bytes': total_size,
        'last_updated': last_updated.isoformat() if last_updated else None,
        'tree': tree,
        'paths': sorted(paths)
    }


def generate_search_index(
    paths_manifest: Dict,
    docs_manifest: Dict,
    docs_dir: Path
) -> Dict:
    """
    Generate optimized search index.

    Args:
        paths_manifest: Paths manifest
        docs_manifest: Documentation manifest
        docs_dir: Directory with documentation files

    Returns:
        Search index dictionary
    """
    search_index = {}

    # Get all paths
    all_paths = []
    for category_paths in paths_manifest.get('categories', {}).values():
        all_paths.extend(category_paths)

    logger.info(f"Building search index for {len(all_paths)} paths")

    for path in all_paths:
        # Extract title from path (last segment)
        title = path.rstrip('/').split('/')[-1].replace('-', ' ').title()

        # Extract keywords from path
        keywords = [
            part.lower()
            for part in path.split('/')
            if part and part not in ['en', 'docs']
        ]

        # Try to extract content preview from file
        content_preview = ""
        try:
            # Convert path to filename
            filename = path.lstrip('/').replace('/', '__') + '.md'
            file_path = docs_dir / filename

            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[:10]  # First 10 lines
                    # Skip front matter and headers
                    content_lines = [
                        line.strip()
                        for line in lines
                        if line.strip() and not line.startswith('#')
                    ]
                    content_preview = ' '.join(content_lines[:3])[:200]

        except Exception as e:
            logger.debug(f"Couldn't extract preview for {path}: {e}")

        # Get metadata
        metadata = docs_manifest.get(path, {})

        search_index[path] = {
            'title': title,
            'keywords': keywords,
            'content_preview': content_preview,
            'size': metadata.get('size', 0),
            'last_updated': metadata.get('last_updated')
        }

    return search_index


def generate_full_sitemap(
    paths_manifest: Dict,
    docs_manifest: Dict,
    category_indexes: Dict[str, Dict]
) -> Dict:
    """
    Generate complete sitemap.

    Args:
        paths_manifest: Paths manifest
        docs_manifest: Documentation manifest
        category_indexes: Dictionary of category indexes

    Returns:
        Full sitemap dictionary
    """
    # Count total paths across all categories
    total_paths = sum(
        len(paths)
        for paths in paths_manifest.get('categories', {}).values()
    )

    # Count documented paths
    documented_count = len(docs_manifest)

    # Find most recent update
    last_updated = None
    for entry in docs_manifest.values():
        if isinstance(entry, dict):
            updated_str = entry.get('last_updated')
            if updated_str:
                try:
                    updated = datetime.fromisoformat(updated_str.replace('Z', '+00:00'))
                    if last_updated is None or updated > last_updated:
                        last_updated = updated
                except (ValueError, AttributeError):
                    pass

    return {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'total_paths': total_paths,
        'documented_paths': documented_count,
        'coverage_percent': round((documented_count / total_paths * 100), 2)
                           if total_paths > 0 else 0,
        'last_updated': last_updated.isoformat() if last_updated else None,
        'categories': {
            name: {
                'count': index['count'],
                'last_updated': index['last_updated']
            }
            for name, index in category_indexes.items()
        },
        'paths_by_category': paths_manifest.get('categories', {})
    }


def save_json(path: Path, data: Dict):
    """
    Save dictionary as formatted JSON.

    Args:
        path: Output file path
        data: Dictionary to save
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    logger.info(f"Saved {path}")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Generate sitemap and search indexes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all indexes
  %(prog)s

  # Specify custom paths
  %(prog)s --manifest paths_manifest.json --docs-dir docs/

  # Generate only sitemap
  %(prog)s --sitemap-only
        """
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
        '--docs-dir',
        type=Path,
        default=Path('docs'),
        help='Documentation directory (default: docs/)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=Path('docs'),
        help='Output directory for indexes (default: docs/)'
    )

    parser.add_argument(
        '--sitemap-only',
        action='store_true',
        help='Generate only sitemap, skip category indexes'
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
        # Load manifests
        logger.info("Loading manifests...")
        paths_manifest = load_paths_manifest(args.manifest)
        docs_manifest = load_docs_manifest(args.docs_manifest)

        # Generate category indexes
        category_indexes = {}

        if not args.sitemap_only:
            logger.info("Generating category indexes...")

            indexes_dir = args.output_dir / 'indexes'
            indexes_dir.mkdir(parents=True, exist_ok=True)

            for category_name, paths in paths_manifest.get('categories', {}).items():
                logger.info(f"Processing category: {category_name}")

                # Generate index
                index = generate_category_index(
                    category_name,
                    paths,
                    docs_manifest
                )

                category_indexes[category_name] = index

                # Save category index
                index_path = indexes_dir / f"{category_name}.json"
                save_json(index_path, index)

            logger.info(f"Generated {len(category_indexes)} category indexes")

        # Generate search index
        logger.info("Generating search index...")
        search_index = generate_search_index(
            paths_manifest,
            docs_manifest,
            args.docs_dir
        )

        search_index_path = args.output_dir / '.search_index.json'
        save_json(search_index_path, search_index)

        # Generate full sitemap
        logger.info("Generating full sitemap...")
        sitemap = generate_full_sitemap(
            paths_manifest,
            docs_manifest,
            category_indexes
        )

        sitemap_path = args.output_dir / 'sitemap.json'
        save_json(sitemap_path, sitemap)

        # Summary
        logger.info("\n" + "="*60)
        logger.info("SITEMAP GENERATION SUMMARY")
        logger.info("="*60)
        logger.info(f"Total paths: {sitemap['total_paths']}")
        logger.info(f"Documented: {sitemap['documented_paths']}")
        logger.info(f"Coverage: {sitemap['coverage_percent']}%")
        logger.info(f"Categories: {len(category_indexes)}")
        logger.info(f"Search index entries: {len(search_index)}")
        logger.info("="*60)

        logger.info("Sitemap generation completed successfully!")
        return 0

    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        return 1

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
