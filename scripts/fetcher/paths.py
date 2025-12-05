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


def url_to_safe_filename(url_path: str) -> str:
    """
    Convert a URL path to a safe filename using standardized en__ naming convention.

    Preserves full URL path structure by converting slashes to double underscores.
    Sanitizes characters to whitelist: alphanumeric, hyphens, underscores, and dots.

    Examples:
        /en/docs/claude-code/hooks → en__docs__claude-code__hooks.md
        /en/api/messages → en__api__messages.md
        /en/docs/build-with-claude/prompt-engineering/overview → en__docs__build-with-claude__prompt-engineering__overview.md

    Args:
        url_path: URL path like '/en/docs/claude-code/hooks'

    Returns:
        Safe filename like 'en__docs__claude-code__hooks.md'

    Raises:
        ValueError: If the resulting filename is empty or invalid
    """
    # Strip leading and trailing slashes
    path = url_path.strip('/')

    # Replace all slashes with double underscores
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


def categorize_path(path: str) -> str:
    """
    Categorize documentation path based on URL structure.

    Args:
        path: Documentation path (e.g., /en/api/messages or /docs/en/hooks)

    Returns:
        Category name as string
    """
    if path.startswith('/en/api/') or path.startswith('/en/docs/agent-sdk/'):
        return 'api_reference'

    if path.startswith('/docs/en/'):
        return 'claude_code'

    if path.startswith('/en/prompt-library/') or path.startswith('/en/resources/prompt-library/'):
        return 'prompt_library'

    if path.startswith('/en/resources/'):
        return 'resources'

    if path.startswith('/en/release-notes/'):
        return 'release_notes'

    if path.startswith('/en/home') or path == '/en/prompt-library':
        return 'uncategorized'

    # Everything else (guides, about-claude, build-with-claude, etc.)
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
    - code.claude.com: Paths starting with /docs/en/ (Claude Code CLI docs)
    - platform.claude.com: Paths starting with /en/ (API, Agent SDK, Prompt Library, etc.)

    NOTE: docs.claude.com and docs.anthropic.com are BROKEN and should not be used!

    Args:
        path: Documentation path (e.g., /en/api/messages or /docs/en/analytics)

    Returns:
        Base URL (https://code.claude.com or https://platform.claude.com)
    """
    # Claude Code CLI docs on code.claude.com use /docs/en/ prefix
    if path.startswith('/docs/en/'):
        return 'https://code.claude.com'

    # Everything else (starting with /en/) is on platform.claude.com
    # This includes: /en/api/, /en/docs/agent-sdk/, /en/docs/about-claude/, etc.
    return 'https://platform.claude.com'


def load_paths_from_manifest() -> List[str]:
    """
    Load paths for files that already exist locally in ./docs/

    This is a FALLBACK used only if sitemap discovery fails.
    Normally, we discover ~273 active paths from sitemaps and fetch all of them.

    Returns:
        List of paths corresponding to existing local files (~266-270 files)
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
