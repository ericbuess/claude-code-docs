"""
Documentation fetcher package.

This package provides functionality for fetching Claude documentation
from multiple sitemaps with safety safeguards.

Main entry point: run_fetcher() or use fetch_claude_docs.py wrapper
"""

from .config import (
    SITEMAP_URLS,
    MANIFEST_FILE,
    HEADERS,
    MAX_RETRIES,
    RETRY_DELAY,
    MAX_RETRY_DELAY,
    RATE_LIMIT_DELAY,
    MIN_DISCOVERY_THRESHOLD,
    MAX_DELETION_PERCENT,
    MIN_EXPECTED_FILES,
)

from .manifest import (
    load_manifest,
    save_manifest,
    validate_repository_config,
)

from .paths import (
    url_to_safe_filename,
    categorize_path,
    convert_legacy_path_to_fetch_url,
    get_base_url_for_path,
    load_paths_from_manifest,
    update_paths_manifest,
)

from .sitemap import (
    discover_from_all_sitemaps,
    discover_sitemap_and_base_url,
    discover_claude_code_pages,
)

from .content import (
    validate_markdown_content,
    fetch_markdown_content,
    fetch_changelog,
    save_markdown_file,
    content_has_changed,
)

from .safeguards import (
    cleanup_old_files,
    validate_discovery_threshold,
)

from .cli import main as run_fetcher

__all__ = [
    # Config
    'SITEMAP_URLS',
    'MANIFEST_FILE',
    'HEADERS',
    'MAX_RETRIES',
    'RETRY_DELAY',
    'MAX_RETRY_DELAY',
    'RATE_LIMIT_DELAY',
    'MIN_DISCOVERY_THRESHOLD',
    'MAX_DELETION_PERCENT',
    'MIN_EXPECTED_FILES',
    # Manifest
    'load_manifest',
    'save_manifest',
    'validate_repository_config',
    # Paths
    'url_to_safe_filename',
    'categorize_path',
    'convert_legacy_path_to_fetch_url',
    'get_base_url_for_path',
    'load_paths_from_manifest',
    'update_paths_manifest',
    # Sitemap
    'discover_from_all_sitemaps',
    'discover_sitemap_and_base_url',
    'discover_claude_code_pages',
    # Content
    'validate_markdown_content',
    'fetch_markdown_content',
    'fetch_changelog',
    'save_markdown_file',
    'content_has_changed',
    # Safeguards
    'cleanup_old_files',
    'validate_discovery_threshold',
    # CLI
    'run_fetcher',
]
