#!/usr/bin/env python3
"""
Path lookup and validation utility.

This is a thin wrapper that imports functionality from the lookup package.
The actual implementation is split across multiple modules for maintainability:

- lookup/config.py       - Configuration constants
- lookup/manifest.py     - Manifest loading and path utilities
- lookup/search.py       - Search functionality
- lookup/validation.py   - Path validation
- lookup/formatting.py   - Output formatting
- lookup/cli.py          - Main entry point

For backwards compatibility, all public functions are re-exported here.
"""

# Re-export everything for backwards compatibility
from lookup import (
    # Config
    BASE_URL_CODE,
    BASE_URL_PLATFORM,
    BASE_URL,
    REQUEST_TIMEOUT,
    MAX_WORKERS,
    get_base_url_for_path,
    # Manifest
    load_paths_manifest,
    _load_paths_manifest_cached,  # Exposed for testing
    get_all_paths,
    normalize_path_for_lookup,
    get_category_for_path,
    get_product_label,
    # Search
    search_paths,
    create_enriched_search_results,
    search_content,
    load_search_index,
    suggest_alternatives,
    # Validation
    ValidationStats,
    validate_path,
    batch_validate,
    load_batch_file,
    # Formatting
    print_search_results,
    print_validation_report,
    format_content_search_json,
    format_content_result,
    # CLI
    run_lookup as main,
)

if __name__ == "__main__":
    exit(main())
