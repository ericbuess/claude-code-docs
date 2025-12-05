"""
Content fetching and validation functionality.

This module handles:
- Fetching markdown content from documentation URLs
- Validating markdown content
- Saving markdown files
- Fetching the Claude Code changelog
"""

import hashlib
import random
import time
from pathlib import Path
from typing import Tuple

import requests

from .config import (
    HEADERS,
    MAX_RETRIES,
    RETRY_DELAY,
    MAX_RETRY_DELAY,
    logger,
)
from .paths import (
    url_to_safe_filename,
    convert_legacy_path_to_fetch_url,
    get_base_url_for_path,
)


def validate_markdown_content(content: str, filename: str) -> None:
    """
    Validate that content is proper markdown.

    Args:
        content: The content to validate
        filename: The filename (for error messages)

    Raises:
        ValueError: If validation fails
    """
    # Check for HTML content
    if not content or content.startswith('<!DOCTYPE') or '<html' in content[:100]:
        raise ValueError("Received HTML instead of markdown")

    # Check minimum length
    if len(content.strip()) < 50:
        raise ValueError(f"Content too short ({len(content)} bytes)")

    # Check for common markdown elements
    lines = content.split('\n')
    markdown_indicators = [
        '# ',      # Headers
        '## ',
        '### ',
        '```',     # Code blocks
        '- ',      # Lists
        '* ',
        '1. ',
        '[',       # Links
        '**',      # Bold
        '_',       # Italic
        '> ',      # Quotes
    ]

    # Count markdown indicators
    indicator_count = 0
    for line in lines[:50]:  # Check first 50 lines
        for indicator in markdown_indicators:
            if line.strip().startswith(indicator) or indicator in line:
                indicator_count += 1
                break

    # Require at least some markdown formatting
    if indicator_count < 3:
        raise ValueError(f"Content doesn't appear to be markdown (only {indicator_count} markdown indicators found)")

    # Check for common documentation patterns
    doc_patterns = ['installation', 'usage', 'example', 'api', 'configuration', 'claude', 'code']
    content_lower = content.lower()
    pattern_found = any(pattern in content_lower for pattern in doc_patterns)

    if not pattern_found:
        logger.warning(f"Content for {filename} doesn't contain expected documentation patterns")


def fetch_markdown_content(path: str, session: requests.Session, base_url: str) -> Tuple[str, str]:
    """
    Fetch markdown content with better error handling and validation.

    Args:
        path: URL path from manifest (may be legacy format like /en/docs/claude-code/hooks)
        session: Requests session
        base_url: Base URL for fetching (DEPRECATED - automatically determined from path)

    Returns:
        Tuple of (filename, content) where filename uses legacy naming convention
    """
    # Determine the correct base URL based on the path
    # This overrides the passed base_url parameter to handle the multi-domain setup
    actual_base_url = get_base_url_for_path(path)

    # Convert legacy path to new fetch URL format
    fetch_path = convert_legacy_path_to_fetch_url(path)

    # Build full fetch URL using the correct domain
    markdown_url = f"{actual_base_url}{fetch_path}.md"

    # Keep original path for consistent filename (legacy convention)
    # This ensures files keep their existing names even as URLs change
    filename = url_to_safe_filename(path)

    logger.info(f"Fetching: {markdown_url} -> {filename}")

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(markdown_url, headers=HEADERS, timeout=30, allow_redirects=True)

            # Handle specific HTTP errors
            if response.status_code == 429:  # Rate limited
                wait_time = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            # Get content and validate
            content = response.text
            validate_markdown_content(content, filename)

            logger.info(f"Successfully fetched and validated {filename} ({len(content)} bytes)")
            return filename, content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {filename}: {e}")
            if attempt < MAX_RETRIES - 1:
                # Exponential backoff with jitter
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                # Add jitter to prevent thundering herd
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.info(f"Retrying in {jittered_delay:.1f} seconds...")
                time.sleep(jittered_delay)
            else:
                raise Exception(f"Failed to fetch {filename} after {MAX_RETRIES} attempts: {e}")

        except ValueError as e:
            logger.error(f"Content validation failed for {filename}: {e}")
            raise


def fetch_changelog(session: requests.Session) -> Tuple[str, str]:
    """
    Fetch Claude Code changelog from GitHub repository.

    Args:
        session: Requests session

    Returns:
        Tuple of (filename, content)
    """
    changelog_url = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
    filename = "changelog.md"

    logger.info(f"Fetching Claude Code changelog: {changelog_url}")

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(changelog_url, headers=HEADERS, timeout=30, allow_redirects=True)

            if response.status_code == 429:  # Rate limited
                wait_time = int(response.headers.get('Retry-After', 60))
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()

            content = response.text

            # Add header to indicate this is from Claude Code repo, not docs site
            header = """# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
>
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository. For documentation, see other topics via `/docs`.

---

"""
            content = header + content

            # Basic validation
            if len(content.strip()) < 100:
                raise ValueError(f"Changelog content too short ({len(content)} bytes)")

            logger.info(f"Successfully fetched changelog ({len(content)} bytes)")
            return filename, content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for changelog: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.info(f"Retrying in {jittered_delay:.1f} seconds...")
                time.sleep(jittered_delay)
            else:
                raise Exception(f"Failed to fetch changelog after {MAX_RETRIES} attempts: {e}")

        except ValueError as e:
            logger.error(f"Changelog validation failed: {e}")
            raise


def save_markdown_file(docs_dir: Path, filename: str, content: str) -> str:
    """
    Save markdown content and return its hash.

    Args:
        docs_dir: Directory to save the file in
        filename: Name of the file
        content: Content to write

    Returns:
        SHA256 hash of the content
    """
    file_path = docs_dir / filename

    try:
        file_path.write_text(content, encoding='utf-8')
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        logger.info(f"Saved: {filename}")
        return content_hash
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise


def content_has_changed(content: str, old_hash: str) -> bool:
    """
    Check if content has changed based on hash.

    Args:
        content: New content to check
        old_hash: Previous content hash

    Returns:
        True if content has changed, False otherwise
    """
    new_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return new_hash != old_hash
