#!/usr/bin/env python3
"""
Claude Code documentation fetcher with safety safeguards.

This is a thin wrapper that imports functionality from the fetcher package.
The actual implementation is split across multiple modules for maintainability:

- fetcher/config.py      - Configuration constants and thresholds
- fetcher/manifest.py    - Manifest file operations
- fetcher/paths.py       - Path conversion and categorization
- fetcher/sitemap.py     - Sitemap discovery and parsing
- fetcher/content.py     - Content fetching and validation
- fetcher/safeguards.py  - Safety checks to prevent mass deletion
- fetcher/cli.py         - Main entry point

For backwards compatibility, all public functions are re-exported here.
"""

# Re-export everything for backwards compatibility
from fetcher import (
    # Config
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
    # Manifest
    load_manifest,
    save_manifest,
    validate_repository_config,
    # Paths
    url_to_safe_filename,
    categorize_path,
    convert_legacy_path_to_fetch_url,
    get_base_url_for_path,
    load_paths_from_manifest,
    update_paths_manifest,
    # Sitemap
    discover_from_all_sitemaps,
    discover_sitemap_and_base_url,
    discover_claude_code_pages,
    # Content
    validate_markdown_content,
    fetch_markdown_content,
    fetch_changelog,
    save_markdown_file,
    content_has_changed,
    # Safeguards
    cleanup_old_files,
    validate_discovery_threshold,
    # CLI
    run_fetcher as main,
)

if __name__ == "__main__":
    main()
