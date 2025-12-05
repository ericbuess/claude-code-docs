"""
Command-line interface for the documentation fetcher.

This module contains the main() function that orchestrates the entire
documentation fetching process.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

from .config import RATE_LIMIT_DELAY, logger
from .manifest import load_manifest, save_manifest, validate_repository_config
from .sitemap import discover_from_all_sitemaps, discover_sitemap_and_base_url
from .paths import load_paths_from_manifest, update_paths_manifest
from .content import (
    fetch_markdown_content,
    fetch_changelog,
    save_markdown_file,
    content_has_changed,
)
from .safeguards import cleanup_old_files, validate_discovery_threshold


def main():
    """Main function with improved robustness."""
    start_time = datetime.now()
    logger.info("Starting documentation update (updating existing local files only)")

    # Log configuration
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'costiash/claude-code-docs')
    logger.info(f"GitHub repository: {github_repo}")

    # Create docs directory at repository root
    docs_dir = Path(__file__).parent.parent.parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {docs_dir}")

    # Load manifest
    manifest = load_manifest(docs_dir)

    # Validate repository configuration
    validate_repository_config(manifest)

    # Statistics
    successful = 0
    failed = 0
    failed_pages = []
    fetched_files = set()
    new_manifest = {"files": {}}

    # Create a session for connection pooling
    sitemap_url = None
    with requests.Session() as session:
        # Discover sitemap and base URL
        try:
            sitemap_url, base_url = discover_sitemap_and_base_url(session)
        except Exception as e:
            logger.error(f"Failed to discover sitemap: {e}")
            logger.info("Using fallback configuration...")
            base_url = "https://platform.claude.com"  # Primary docs domain
            sitemap_url = None

        # Discover ALL documentation paths from sitemaps
        logger.info("Discovering all /en/ documentation paths from sitemaps...")
        try:
            documentation_pages = discover_from_all_sitemaps(session)

            # Auto-regenerate paths_manifest.json with fresh discovered paths
            try:
                update_paths_manifest(documentation_pages)
                logger.info("Successfully regenerated paths_manifest.json from sitemap discovery")
            except Exception as e:
                logger.warning(f"Failed to update paths_manifest.json: {e}")
                # Non-fatal - continue with fetch

        except Exception as e:
            logger.error(f"Sitemap discovery failed: {e}")
            logger.warning("Falling back to local file detection...")
            # Fallback: load paths for existing local files
            documentation_pages = load_paths_from_manifest()

        # Validate discovery threshold (safeguard)
        documentation_pages = validate_discovery_threshold(documentation_pages)

        # Fetch each discovered page
        for i, page_path in enumerate(documentation_pages, 1):
            logger.info(f"Processing {i}/{len(documentation_pages)}: {page_path}")

            try:
                filename, content = fetch_markdown_content(page_path, session, base_url)

                # Check if content has changed OR file doesn't exist on disk
                old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
                old_entry = manifest.get("files", {}).get(filename, {})
                file_path = docs_dir / filename
                file_exists = file_path.exists()

                if content_has_changed(content, old_hash) or not file_exists:
                    content_hash = save_markdown_file(docs_dir, filename, content)
                    if not file_exists:
                        logger.info(f"Created: {filename}")
                    else:
                        logger.info(f"Updated: {filename}")
                    # Only update timestamp when content actually changes
                    last_updated = datetime.now().isoformat()
                else:
                    content_hash = old_hash
                    logger.info(f"Unchanged: {filename}")
                    # Keep existing timestamp for unchanged files
                    last_updated = old_entry.get("last_updated", datetime.now().isoformat())

                new_manifest["files"][filename] = {
                    "original_url": f"{base_url}{page_path}",
                    "original_md_url": f"{base_url}{page_path}.md",
                    "hash": content_hash,
                    "last_updated": last_updated
                }

                fetched_files.add(filename)
                successful += 1

                # Rate limiting
                if i < len(documentation_pages):
                    time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                logger.error(f"Failed to process {page_path}: {e}")
                failed += 1
                failed_pages.append(page_path)

    # Fetch Claude Code changelog
    logger.info("Fetching Claude Code changelog...")
    try:
        filename, content = fetch_changelog(session)

        # Check if content has changed
        old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
        old_entry = manifest.get("files", {}).get(filename, {})

        if content_has_changed(content, old_hash):
            content_hash = save_markdown_file(docs_dir, filename, content)
            logger.info(f"Updated: {filename}")
            last_updated = datetime.now().isoformat()
        else:
            content_hash = old_hash
            logger.info(f"Unchanged: {filename}")
            last_updated = old_entry.get("last_updated", datetime.now().isoformat())

        new_manifest["files"][filename] = {
            "original_url": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
            "original_raw_url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
            "hash": content_hash,
            "last_updated": last_updated,
            "source": "claude-code-repository"
        }

        fetched_files.add(filename)
        successful += 1

    except Exception as e:
        logger.error(f"Failed to fetch changelog: {e}")
        failed += 1
        failed_pages.append("changelog")

    # Clean up old files (only those we previously fetched)
    cleanup_old_files(docs_dir, fetched_files, manifest)

    # Add metadata to manifest
    new_manifest["fetch_metadata"] = {
        "last_fetch_completed": datetime.now().isoformat(),
        "fetch_duration_seconds": (datetime.now() - start_time).total_seconds(),
        "total_pages_discovered": len(documentation_pages),
        "pages_fetched_successfully": successful,
        "pages_failed": failed,
        "failed_pages": failed_pages,
        "sitemap_url": sitemap_url,
        "base_url": base_url,
        "total_files": len(fetched_files),
        "fetch_tool_version": "3.0"
    }

    # Save new manifest
    save_manifest(docs_dir, new_manifest)

    # Summary
    duration = datetime.now() - start_time
    logger.info("\n" + "="*50)
    logger.info(f"Fetch completed in {duration}")
    logger.info(f"Discovered pages: {len(documentation_pages)}")
    logger.info(f"Successful: {successful}/{len(documentation_pages)}")
    logger.info(f"Failed: {failed}")

    if failed_pages:
        logger.warning("\nFailed pages (will retry next run):")
        for page in failed_pages:
            logger.warning(f"  - {page}")
        # Don't exit with error - partial success is OK
        if successful == 0:
            logger.error("No pages were fetched successfully!")
            sys.exit(1)
    else:
        logger.info("\nAll pages fetched successfully!")


if __name__ == "__main__":
    main()
