"""
Configuration constants for the documentation fetcher.

This module contains all configuration values, URLs, and thresholds
used throughout the fetcher package.
"""

import logging

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# =============================================================================
# SITEMAP URLS - Documentation sources (verified working as of Dec 2025)
# =============================================================================
# Note: docs.claude.com and docs.anthropic.com are BROKEN (500/401 errors)
# Documentation is now split across these two domains:
SITEMAP_URLS = [
    "https://platform.claude.com/sitemap.xml",   # API, Agent SDK, Core docs, Prompt Library
    "https://code.claude.com/docs/sitemap.xml",  # Claude Code CLI documentation
]
# REMOVED (broken): docs.claude.com, docs.anthropic.com


# =============================================================================
# FILE CONFIGURATION
# =============================================================================
MANIFEST_FILE = "docs_manifest.json"


# =============================================================================
# HTTP REQUEST CONFIGURATION
# =============================================================================
# Headers to bypass caching and identify the script
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/3.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}


# =============================================================================
# RETRY CONFIGURATION
# =============================================================================
MAX_RETRIES = 3
RETRY_DELAY = 2  # initial delay in seconds
MAX_RETRY_DELAY = 30  # maximum delay in seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests


# =============================================================================
# SAFETY THRESHOLDS - Prevent catastrophic deletion from sitemap failures
# =============================================================================
MIN_DISCOVERY_THRESHOLD = 200      # Refuse to proceed if < 200 paths discovered
MAX_DELETION_PERCENT = 10          # Never delete > 10% of existing files
MIN_EXPECTED_FILES = 250           # Minimum expected file count after fetch
