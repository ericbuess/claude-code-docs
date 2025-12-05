"""
Manifest file operations for tracking fetched documentation.

This module handles loading, saving, and validating the docs_manifest.json
file that tracks all fetched documentation files.
"""

import json
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict

from .config import MANIFEST_FILE, logger


def load_manifest(docs_dir: Path) -> Dict:
    """
    Load the manifest of previously fetched files.

    Args:
        docs_dir: Path to the docs directory

    Returns:
        Manifest dictionary with 'files' and 'last_updated' keys
    """
    manifest_path = docs_dir / MANIFEST_FILE
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            # Ensure required keys exist
            if "files" not in manifest:
                manifest["files"] = {}
            return manifest
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
    return {"files": {}, "last_updated": None}


def save_manifest(docs_dir: Path, manifest: Dict) -> None:
    """
    Save the manifest of fetched files.

    Args:
        docs_dir: Path to the docs directory
        manifest: Manifest dictionary to save
    """
    manifest_path = docs_dir / MANIFEST_FILE
    manifest["last_updated"] = datetime.now().isoformat()

    # Get GitHub repository from environment or use default
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'costiash/claude-code-docs')
    github_ref = os.environ.get('GITHUB_REF_NAME', 'main')

    # Validate repository name format (owner/repo)
    if not re.match(r'^[\w.-]+/[\w.-]+$', github_repo):
        logger.warning(f"Invalid repository format: {github_repo}, using default")
        github_repo = 'costiash/claude-code-docs'

    # Validate branch/ref name
    if not re.match(r'^[\w.-]+$', github_ref):
        logger.warning(f"Invalid ref format: {github_ref}, using default")
        github_ref = 'main'

    manifest["base_url"] = f"https://raw.githubusercontent.com/{github_repo}/{github_ref}/docs/"
    manifest["github_repository"] = github_repo
    manifest["github_ref"] = github_ref
    manifest["description"] = "Claude Code documentation manifest. Keys are filenames, append to base_url for full URL."
    manifest_path.write_text(json.dumps(manifest, indent=2))


def validate_repository_config(manifest: Dict) -> None:
    """
    Validate that manifest repository matches actual git repository.

    Warns if there's a mismatch to catch configuration issues.

    Args:
        manifest: Manifest dictionary to validate
    """
    try:
        # Get actual git repository from remote origin
        result = subprocess.run(
            ['git', 'remote', 'get-url', 'origin'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            git_url = result.stdout.strip()

            # Extract owner/repo from git URL
            # Handles both HTTPS and SSH formats:
            # - https://github.com/costiash/claude-code-docs.git
            # - git@github.com:costiash/claude-code-docs.git
            if 'github.com' in git_url:
                # Extract the owner/repo part
                if git_url.startswith('git@github.com:'):
                    repo_part = git_url.replace('git@github.com:', '').replace('.git', '')
                elif 'github.com/' in git_url:
                    repo_part = git_url.split('github.com/')[-1].replace('.git', '')
                else:
                    return  # Can't parse, skip validation

                # Compare with manifest
                manifest_repo = manifest.get('github_repository', '')

                if manifest_repo and repo_part != manifest_repo:
                    logger.warning("=" * 70)
                    logger.warning("⚠️  REPOSITORY MISMATCH DETECTED!")
                    logger.warning(f"   Git repository: {repo_part}")
                    logger.warning(f"   Manifest repository: {manifest_repo}")
                    logger.warning("   This may cause documentation to be fetched from wrong source.")
                    logger.warning("   Consider updating GITHUB_REPOSITORY environment variable or")
                    logger.warning("   updating the default in this script.")
                    logger.warning("=" * 70)
    except Exception as e:
        # Don't fail on validation errors - this is just a warning
        logger.debug(f"Could not validate repository config: {e}")
