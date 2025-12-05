"""
Configuration constants for the path lookup utility.

This module contains all configuration values for searching and validating
documentation paths.
"""

import logging

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# URL CONFIGURATION - Multi-domain support (as of Dec 2025)
# =============================================================================
# Documentation is split across two domains:
BASE_URL_CODE = "https://code.claude.com"       # Claude Code CLI docs (/docs/en/*)
BASE_URL_PLATFORM = "https://platform.claude.com"  # Everything else (/en/*)

# Legacy alias for backwards compatibility
BASE_URL = BASE_URL_CODE


# =============================================================================
# REQUEST CONFIGURATION
# =============================================================================
REQUEST_TIMEOUT = 10
MAX_WORKERS = 5  # Parallel validation threads


def get_base_url_for_path(path: str) -> str:
    """
    Determine the correct base URL for a given documentation path.

    Args:
        path: Documentation path

    Returns:
        Appropriate base URL for the path
    """
    # Claude Code CLI docs use /docs/en/ prefix
    if path.startswith('/docs/en/'):
        return BASE_URL_CODE
    # Everything else (API, Agent SDK, etc.) uses platform.claude.com
    return BASE_URL_PLATFORM
