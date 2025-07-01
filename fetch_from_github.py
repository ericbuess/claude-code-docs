#!/usr/bin/env python3
"""
Fetch Claude Code documentation from GitHub repository.
This allows users to get the latest docs without running the scraper themselves.
"""

import requests
import json
from pathlib import Path
import logging
from typing import Dict, List
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# GitHub API configuration
GITHUB_API_BASE = "https://api.github.com"
REPO_OWNER = "ericbuess"
REPO_NAME = "claude-code-docs"
BRANCH = "main"  # Use main branch for stable version

def get_docs_list() -> List[Dict[str, str]]:
    """
    Fetch the list of documentation files from GitHub.
    
    Returns:
        List of dictionaries containing file information
    """
    url = f"{GITHUB_API_BASE}/repos/{REPO_OWNER}/{REPO_NAME}/contents/docs?ref={BRANCH}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch file list: {e}")
        raise


def download_file(file_info: Dict[str, str], output_dir: Path) -> None:
    """
    Download a single documentation file.
    
    Args:
        file_info: GitHub API file information
        output_dir: Directory to save the file
    """
    filename = file_info['name']
    download_url = file_info['download_url']
    
    try:
        response = requests.get(download_url)
        response.raise_for_status()
        
        file_path = output_dir / filename
        file_path.write_text(response.text, encoding='utf-8')
        
        logger.info(f"Downloaded: {filename}")
    except Exception as e:
        logger.error(f"Failed to download {filename}: {e}")
        raise


def main():
    """Download all Claude Code documentation from GitHub."""
    logger.info(f"Fetching Claude Code docs from GitHub ({REPO_OWNER}/{REPO_NAME})")
    
    # Create output directory
    output_dir = Path(__file__).parent / 'docs'
    output_dir.mkdir(exist_ok=True)
    
    try:
        # Get list of files
        files = get_docs_list()
        logger.info(f"Found {len(files)} documentation files")
        
        # Download each file
        for i, file_info in enumerate(files, 1):
            if file_info['type'] == 'file' and file_info['name'].endswith('.md'):
                logger.info(f"[{i}/{len(files)}] Downloading {file_info['name']}")
                download_file(file_info, output_dir)
        
        logger.info("Successfully downloaded all documentation files!")
        
    except Exception as e:
        logger.error(f"Failed to fetch documentation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()