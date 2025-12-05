"""
Path conversion and categorization utilities.

This module handles:
- Converting URL paths to safe filenames
- Categorizing paths by documentation type
- Converting between legacy and new path formats
- Determining correct base URLs for paths
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List

from .config import logger


def url_to_safe_filename(url_path: str, source_domain: str = None) -> str:
    """
    Convert a URL path to a safe filename with domain-based naming convention.

    Domain distinction strategy (to avoid naming conflicts):
    - Files from code.claude.com → claude-code__<page>.md (e.g., claude-code__hooks.md)
    - Files from platform.claude.com → docs__en__<path>.md (existing convention)

    This is necessary because BOTH domains use /docs/en/ URL prefix.

    Examples:
        /docs/en/hooks (code.claude.com) → claude-code__hooks.md
        /docs/en/api/messages (platform.claude.com) → docs__en__api__messages.md
        /docs/en/about-claude/pricing (platform.claude.com) → docs__en__about-claude__pricing.md

    Args:
        url_path: URL path like '/docs/en/hooks'
        source_domain: Source domain ('code.claude.com' or 'platform.claude.com')
                       If None, determines from path using is_claude_code_cli_page()

    Returns:
        Safe filename with appropriate prefix

    Raises:
        ValueError: If the resulting filename is empty or invalid
    """
    # Strip leading and trailing slashes
    path = url_path.strip('/')

    # Determine if this is a Claude Code CLI page
    is_cli_page = False
    if source_domain == 'code.claude.com':
        is_cli_page = True
    elif source_domain is None:
        # Auto-detect using the known list of CLI pages
        is_cli_page = is_claude_code_cli_page(url_path)

    if is_cli_page:
        # Claude Code CLI docs: /docs/en/hooks -> claude-code__hooks.md
        # Extract just the page name (last segment)
        page_name = path.rstrip('/').split('/')[-1]
        # Handle nested paths like sdk/migration-guide
        if path.startswith('docs/en/sdk/'):
            page_name = 'sdk__' + page_name
        safe_name = f"claude-code__{page_name}"
    else:
        # Platform docs: /docs/en/api/messages -> docs__en__api__messages.md
        safe_name = path.replace('/', '__')

    # Sanitize: only keep alphanumeric, hyphens, underscores, and dots
    # This prevents path traversal and injection attacks
    sanitized = ''.join(c for c in safe_name if c.isalnum() or c in '-_.')

    # Validate the result is not empty
    if not sanitized or sanitized == '.md':
        raise ValueError(f"Invalid URL path produces empty filename: {url_path}")

    # Add .md extension if not present
    if not sanitized.endswith('.md'):
        sanitized += '.md'

    return sanitized


def is_claude_code_cli_page(path: str) -> bool:
    """
    Check if a path is a Claude Code CLI page (hosted on code.claude.com).

    These are the ~46 pages from code.claude.com/docs/sitemap.xml that need
    the claude-code__ filename prefix to avoid conflicts with platform.claude.com.

    Args:
        path: Documentation path (e.g., /docs/en/hooks)

    Returns:
        True if this is a Claude Code CLI page
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
    # Path format: /docs/en/page-name or /docs/en/subdir/page-name
    if path.startswith('/docs/en/'):
        page_part = path[9:]  # len('/docs/en/') = 9
        if page_part in CLAUDE_CODE_CLI_PAGES or page_part in CLAUDE_CODE_CLI_NESTED:
            return True

    return False


def categorize_path(path: str) -> str:
    """
    Categorize documentation path based on URL structure.

    Handles both old format (/en/...) and new format (/docs/en/...).

    Args:
        path: Documentation path (e.g., /en/api/messages or /docs/en/hooks)

    Returns:
        Category name as string
    """
    # Normalize path - handle both /docs/en/... and /en/... formats
    # The /docs/en/... format comes from code.claude.com sitemap
    normalized = path
    if path.startswith('/docs/en/'):
        # Remove /docs prefix to normalize: /docs/en/api/... -> /en/api/...
        normalized = path[5:]  # '/docs/en/...' -> '/en/...'

    # API Reference: /en/api/* or /en/docs/agent-sdk/*
    if normalized.startswith('/en/api/') or normalized.startswith('/en/agent-sdk/'):
        return 'api_reference'

    # Claude Code CLI docs: specific CLI-related pages
    # These are the actual Claude Code CLI documentation pages
    claude_code_pages = [
        '/en/amazon-bedrock', '/en/analytics', '/en/checkpointing',
        '/en/claude-code-on-the-web', '/en/cli-reference', '/en/common-workflows',
        '/en/costs', '/en/data-usage', '/en/devcontainer', '/en/github-actions',
        '/en/gitlab-ci-cd', '/en/google-vertex-ai', '/en/headless', '/en/hooks',
        '/en/hooks-guide', '/en/iam', '/en/interactive-mode', '/en/jetbrains',
        '/en/legal-and-compliance', '/en/llm-gateway', '/en/mcp', '/en/memory',
        '/en/microsoft-foundry', '/en/model-config', '/en/monitoring-usage',
        '/en/network-config', '/en/output-styles', '/en/overview',
        '/en/plugin-marketplaces', '/en/plugins', '/en/plugins-reference',
        '/en/quickstart', '/en/sandboxing', '/en/security', '/en/settings',
        '/en/setup', '/en/skills', '/en/slash-commands', '/en/statusline',
        '/en/sub-agents', '/en/terminal-config', '/en/third-party-integrations',
        '/en/troubleshooting', '/en/vs-code', '/en/desktop',
        '/en/sdk/migration-guide',
    ]
    if normalized in claude_code_pages or any(normalized.startswith(p + '/') for p in claude_code_pages):
        return 'claude_code'

    # Prompt Library
    if normalized.startswith('/en/resources/prompt-library/'):
        return 'prompt_library'

    # Resources (but not prompt-library)
    if normalized.startswith('/en/resources/'):
        return 'resources'

    # Release Notes
    if normalized.startswith('/en/release-notes/'):
        return 'release_notes'

    # Uncategorized
    if normalized in ['/en/home', '/en/prompt-library']:
        return 'uncategorized'

    # Core Documentation: about-claude, build-with-claude, agents-and-tools, test-and-evaluate, etc.
    core_prefixes = [
        '/en/about-claude/', '/en/build-with-claude/', '/en/agents-and-tools/',
        '/en/test-and-evaluate/', '/en/get-started', '/en/intro', '/en/mcp',
    ]
    if any(normalized.startswith(prefix) or normalized == prefix.rstrip('/') for prefix in core_prefixes):
        return 'core_documentation'

    # Default: if it doesn't match anything specific, categorize as core_documentation
    # This catches paths like /en/docs/... that aren't Agent SDK
    return 'core_documentation'


def convert_legacy_path_to_fetch_url(path: str) -> str:
    """
    Convert legacy manifest paths to correct fetch URLs.

    Documentation is now split across two domains:
    1. code.claude.com - Claude Code docs with URL structure: /docs/en/{page}
    2. platform.claude.com - Everything else with URL structure: /en/{category}/{page}

    Mapping rules:
        Claude Code (code.claude.com):
            /en/docs/claude-code/hooks → /docs/en/hooks

        Everything else (platform.claude.com):
            /en/api/messages → /en/api/messages (no change)
            /en/docs/about-claude/models → /en/docs/about-claude/models (no change)

    Args:
        path: Legacy path from paths_manifest.json (e.g., /en/docs/claude-code/hooks)

    Returns:
        Fetch URL path appropriate for the domain
    """
    # If already in new format (/docs/en/...), return as-is
    if path.startswith('/docs/en/'):
        return path

    # Remove leading /en/ prefix check
    if not path.startswith('/en/'):
        # Path doesn't match expected format, return as-is
        return path

    # Strip /en/ prefix for analysis
    without_en = path[4:]  # Remove '/en/'

    # Handle special case: /en/docs/claude-code/* → /docs/en/*
    # This is for Claude Code docs hosted on code.claude.com
    if without_en.startswith('docs/claude-code/'):
        page_name = without_en.replace('docs/claude-code/', '')
        return f'/docs/en/{page_name}'

    # All other paths stay in /en/* format for platform.claude.com
    return path


def get_base_url_for_path(path: str) -> str:
    """
    Determine the correct base URL for a given documentation path.

    Documentation is hosted on two different domains (as of Dec 2025):
    - code.claude.com: Claude Code CLI-specific documentation (~46 pages)
    - platform.claude.com: Everything else (API, Agent SDK, Prompt Library, Core docs, etc.)

    NOTE: Both domains now use /docs/en/ prefix, so we identify Claude Code CLI pages
    by their specific page names (a known, fixed set).

    NOTE: docs.claude.com and docs.anthropic.com are BROKEN and should not be used!

    Args:
        path: Documentation path (e.g., /docs/en/api/messages or /docs/en/hooks)

    Returns:
        Base URL (https://code.claude.com or https://platform.claude.com)
    """
    if is_claude_code_cli_page(path):
        return 'https://code.claude.com'

    # Everything else (including platform's /docs/en/ paths) is on platform.claude.com
    # This includes: /docs/en/api/, /docs/en/agent-sdk/, /docs/en/about-claude/, etc.
    return 'https://platform.claude.com'


def load_paths_from_manifest() -> List[str]:
    """
    Load paths for files that already exist locally in ./docs/

    This is a FALLBACK used only if sitemap discovery fails.
    Normally, we discover ~573 paths from sitemaps and fetch all of them.

    Returns:
        List of paths corresponding to existing local files (~267 files)
    """
    try:
        docs_dir = Path(__file__).parent.parent.parent / 'docs'
        manifest_path = Path(__file__).parent.parent.parent / 'paths_manifest.json'

        if not manifest_path.exists():
            logger.warning(f"paths_manifest.json not found at {manifest_path}")
            return []

        # Get list of existing local files
        local_files = set()
        if docs_dir.exists():
            for md_file in docs_dir.glob('*.md'):
                if md_file.name == 'docs_manifest.json':
                    continue
                local_files.add(md_file.stem)  # filename without .md extension

        if not local_files:
            logger.warning("No local documentation files found")
            return []

        # Load manifest to get all paths
        with open(manifest_path) as f:
            data = json.load(f)

        # Collect paths that have corresponding local files
        paths_to_update = []
        all_manifest_paths = []

        for category, paths in data.get('categories', {}).items():
            all_manifest_paths.extend(paths)

        # Convert each path to expected filename and check if file exists locally
        for path in all_manifest_paths:
            expected_filename = url_to_safe_filename(path)
            # Remove .md extension for comparison
            if expected_filename.endswith('.md'):
                expected_filename = expected_filename[:-3]

            if expected_filename in local_files:
                paths_to_update.append(path)

        logger.info(f"Found {len(paths_to_update)} paths with existing local files (out of {len(all_manifest_paths)} total paths)")

        return sorted(paths_to_update)

    except Exception as e:
        logger.error(f"Failed to load paths from manifest: {e}")
        return []


def update_paths_manifest(paths: List[str], manifest_file: Path = None) -> None:
    """
    Update paths_manifest.json with newly discovered paths from sitemaps.

    Args:
        paths: List of documentation paths discovered from sitemaps
        manifest_file: Optional path to manifest file (defaults to paths_manifest.json)
    """
    if manifest_file is None:
        manifest_file = Path(__file__).parent.parent.parent / 'paths_manifest.json'
    elif isinstance(manifest_file, str):
        manifest_file = Path(manifest_file)

    # Categorize all paths
    categorized = {}
    for path in paths:
        category = categorize_path(path)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(path)

    # Sort paths within each category
    for category in categorized:
        categorized[category] = sorted(categorized[category])

    # Build manifest structure
    manifest = {
        "metadata": {
            "generated_at": datetime.now().isoformat() + "Z",
            "total_paths": len(paths),
            "source": "sitemap_discovery",
            "last_regenerated": datetime.now().isoformat() + "Z",
        },
        "categories": categorized
    }

    # Write to file
    manifest_file.write_text(json.dumps(manifest, indent=2))
    logger.info(f"Updated paths_manifest.json with {len(paths)} paths across {len(categorized)} categories")
