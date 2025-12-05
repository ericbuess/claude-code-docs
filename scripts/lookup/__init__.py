"""
Path lookup and validation package.

This package provides functionality for searching and validating
documentation paths.

Main entry point: run_lookup() or use lookup_paths.py wrapper
"""

from .config import (
    BASE_URL_CODE,
    BASE_URL_PLATFORM,
    BASE_URL,
    REQUEST_TIMEOUT,
    MAX_WORKERS,
    get_base_url_for_path,
)

from .manifest import (
    load_paths_manifest,
    _load_paths_manifest_cached,  # Exposed for testing
    get_all_paths,
    normalize_path_for_lookup,
    get_category_for_path,
    get_product_label,
)

from .search import (
    search_paths,
    create_enriched_search_results,
    search_content,
    load_search_index,
    suggest_alternatives,
)

from .validation import (
    ValidationStats,
    validate_path,
    batch_validate,
    load_batch_file,
)

from .formatting import (
    print_search_results,
    print_validation_report,
    format_content_search_json,
    format_content_result,
)

from .cli import main as run_lookup

__all__ = [
    # Config
    'BASE_URL_CODE',
    'BASE_URL_PLATFORM',
    'BASE_URL',
    'REQUEST_TIMEOUT',
    'MAX_WORKERS',
    'get_base_url_for_path',
    # Manifest
    'load_paths_manifest',
    '_load_paths_manifest_cached',
    'get_all_paths',
    'normalize_path_for_lookup',
    'get_category_for_path',
    'get_product_label',
    # Search
    'search_paths',
    'create_enriched_search_results',
    'search_content',
    'load_search_index',
    'suggest_alternatives',
    # Validation
    'ValidationStats',
    'validate_path',
    'batch_validate',
    'load_batch_file',
    # Formatting
    'print_search_results',
    'print_validation_report',
    'format_content_search_json',
    'format_content_result',
    # CLI
    'run_lookup',
]
