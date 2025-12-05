"""
Safety safeguards to prevent catastrophic file deletion.

This module contains safeguard functions that prevent mass deletion
of documentation files when sitemap discovery fails.
"""

import sys
from pathlib import Path
from typing import List, Set

from .config import (
    MANIFEST_FILE,
    MIN_DISCOVERY_THRESHOLD,
    MAX_DELETION_PERCENT,
    MIN_EXPECTED_FILES,
    logger,
)
from .paths import load_paths_from_manifest


def cleanup_old_files(docs_dir: Path, current_files: Set[str], manifest: dict) -> None:
    """
    Remove only files that were previously fetched but no longer exist.

    Preserves manually added files.

    SAFEGUARDS (prevent catastrophic deletion from sitemap failures):
    - Refuses to delete > MAX_DELETION_PERCENT of files
    - Refuses if current_files < MIN_EXPECTED_FILES

    Args:
        docs_dir: Path to the docs directory
        current_files: Set of filenames that should be kept
        manifest: Previous manifest with file tracking
    """
    previous_files = set(manifest.get("files", {}).keys())
    files_to_remove = previous_files - current_files

    # SAFEGUARD 1: Check deletion percentage
    if previous_files:
        deletion_percent = (len(files_to_remove) / len(previous_files)) * 100
        if deletion_percent > MAX_DELETION_PERCENT:
            logger.error("=" * 70)
            logger.error("🚨 SAFEGUARD TRIGGERED: Mass deletion prevented!")
            logger.error(f"   Would delete {len(files_to_remove)} of {len(previous_files)} files "
                        f"({deletion_percent:.1f}%)")
            logger.error(f"   Threshold: {MAX_DELETION_PERCENT}%")
            logger.error("   This likely indicates sitemap discovery failure.")
            logger.error("   Files preserved. Manual investigation required.")
            logger.error("=" * 70)
            return

    # SAFEGUARD 2: Check minimum file count
    if len(current_files) < MIN_EXPECTED_FILES:
        logger.error("=" * 70)
        logger.error("🚨 SAFEGUARD TRIGGERED: Insufficient files!")
        logger.error(f"   Only {len(current_files)} files in current set "
                    f"(minimum: {MIN_EXPECTED_FILES})")
        logger.error("   This likely indicates sitemap discovery failure.")
        logger.error("   Files preserved. Manual investigation required.")
        logger.error("=" * 70)
        return

    # Safe to proceed with deletion
    if files_to_remove:
        logger.info(f"Removing {len(files_to_remove)} obsolete files (within safe threshold)")

    for filename in files_to_remove:
        if filename == MANIFEST_FILE:  # Never delete the manifest
            continue

        file_path = docs_dir / filename
        if file_path.exists():
            logger.info(f"Removing obsolete file: {filename}")
            file_path.unlink()


def validate_discovery_threshold(documentation_pages: List[str]) -> List[str]:
    """
    Validate that discovery returned enough paths.

    If insufficient paths are discovered, attempts to use the existing
    manifest as a fallback. If both fail, exits to prevent data loss.

    Args:
        documentation_pages: List of discovered documentation paths

    Returns:
        Validated list of paths (may be from fallback)

    Raises:
        SystemExit: If both discovery and fallback fail
    """
    if len(documentation_pages) < MIN_DISCOVERY_THRESHOLD:
        logger.error("=" * 70)
        logger.error("🚨 SAFEGUARD TRIGGERED: Insufficient paths discovered!")
        logger.error(f"   Only {len(documentation_pages)} paths discovered "
                    f"(minimum: {MIN_DISCOVERY_THRESHOLD})")
        logger.warning("Attempting to use existing manifest as fallback...")

        fallback_paths = load_paths_from_manifest()
        if len(fallback_paths) >= MIN_DISCOVERY_THRESHOLD:
            logger.info(f"✅ Using {len(fallback_paths)} paths from manifest fallback")
            return fallback_paths
        else:
            logger.critical("=" * 70)
            logger.critical("🚨 CRITICAL: Both discovery AND fallback failed!")
            logger.critical(f"   Discovery: {len(documentation_pages)} paths")
            logger.critical(f"   Fallback: {len(fallback_paths)} paths")
            logger.critical(f"   Required minimum: {MIN_DISCOVERY_THRESHOLD}")
            logger.critical("   Aborting to prevent data loss.")
            logger.critical("=" * 70)
            sys.exit(1)

    if not documentation_pages:
        logger.error("No documentation pages discovered!")
        sys.exit(1)

    logger.info(f"✅ Discovery validated: {len(documentation_pages)} paths to process")
    return documentation_pages
