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

    Both domains now use /docs/en/ prefix, so we identify Claude Code CLI pages
    by their specific page names (a known, fixed set of ~46 pages).

    Args:
        path: Documentation path

    Returns:
        Appropriate base URL for the path
    """
    # Claude Code CLI pages - these specific page names are hosted on code.claude.com
    CLAUDE_CODE_CLI_PAGES = {
        'amazon-bedrock', 'analytics', 'checkpointing', 'claude-code-on-the-web',
        'cli-reference', 'common-workflows', 'costs', 'data-usage', 'desktop',
        'devcontainer', 'github-actions', 'gitlab-ci-cd', 'google-vertex-ai',
        'headless', 'hooks', 'hooks-guide', 'iam', 'interactive-mode', 'jetbrains',
        'legal-and-compliance', 'llm-gateway', 'mcp', 'memory', 'microsoft-foundry',
        'model-config', 'monitoring-usage', 'network-config', 'output-styles',
        'overview', 'plugin-marketplaces', 'plugins', 'plugins-reference',
        'quickstart', 'sandboxing', 'security', 'settings', 'setup', 'skills',
        'slash-commands', 'statusline', 'sub-agents', 'terminal-config',
        'third-party-integrations', 'troubleshooting', 'vs-code',
    }

    # Also check for SDK migration guide which is a nested path
    CLAUDE_CODE_CLI_NESTED = {
        'sdk/migration-guide',
    }

    # Extract page name from path
    if path.startswith('/docs/en/'):
        page_part = path[9:]  # len('/docs/en/') = 9
        if page_part in CLAUDE_CODE_CLI_PAGES or page_part in CLAUDE_CODE_CLI_NESTED:
            return BASE_URL_CODE

    # Everything else (including platform's /docs/en/ paths) is on platform.claude.com
    return BASE_URL_PLATFORM
