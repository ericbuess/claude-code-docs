#!/usr/bin/env python3
"""
Fetch all Claude Code documentation pages as markdown files.
This script downloads the latest versions without caching.
"""

import requests
import time
from pathlib import Path
from typing import List, Tuple
import logging
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Base URL for the documentation
BASE_URL = "https://docs.anthropic.com"

# All Claude Code documentation pages
# NOTE: This list is hardcoded. If Anthropic adds/removes pages, update this list.
# TODO: Consider implementing dynamic page discovery if/when an API becomes available.
DOCUMENTATION_PAGES = [
    # Getting started
    "/en/docs/claude-code/overview",
    "/en/docs/claude-code/setup",
    "/en/docs/claude-code/quickstart",
    "/en/docs/claude-code/memory",
    "/en/docs/claude-code/common-workflows",
    
    # Build with Claude
    "/en/docs/claude-code/ide-integrations",
    "/en/docs/claude-code/mcp",
    "/en/docs/claude-code/github-actions",
    "/en/docs/claude-code/sdk",
    "/en/docs/claude-code/troubleshooting",
    
    # Deployment
    "/en/docs/claude-code/third-party-integrations",
    "/en/docs/claude-code/amazon-bedrock",
    "/en/docs/claude-code/google-vertex-ai",
    "/en/docs/claude-code/corporate-proxy",
    "/en/docs/claude-code/llm-gateway",
    "/en/docs/claude-code/devcontainer",
    
    # Administration
    "/en/docs/claude-code/iam",
    "/en/docs/claude-code/security",
    "/en/docs/claude-code/monitoring-usage",
    "/en/docs/claude-code/costs",
    
    # Reference
    "/en/docs/claude-code/cli-reference",
    "/en/docs/claude-code/interactive-mode",
    "/en/docs/claude-code/slash-commands",
    "/en/docs/claude-code/settings",
    "/en/docs/claude-code/hooks",
    
    # Resources
    "/en/docs/claude-code/data-usage",
    "/en/docs/claude-code/legal-and-compliance"
]

# Headers to bypass caching and identify the script
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/1.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def fetch_markdown_content(path: str, session: requests.Session) -> Tuple[str, str]:
    """
    Fetch markdown content for a given documentation path.
    
    Args:
        path: The documentation path (e.g., "/en/docs/claude-code/overview")
        session: The requests session to use
        
    Returns:
        Tuple of (filename, content)
        
    Raises:
        Exception: If the content cannot be fetched after retries
    """
    # Convert path to markdown URL
    markdown_url = f"{BASE_URL}{path}.md"
    
    # Extract filename from path
    filename = path.split('/')[-1] + '.md'
    
    logger.info(f"Fetching: {markdown_url}")
    
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(markdown_url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            
            # Verify we got markdown content
            content = response.text
            if not content or content.startswith('<!DOCTYPE') or '<html' in content[:100]:
                raise ValueError("Received HTML instead of markdown")
            
            # Additional validation - markdown files should have some content
            if len(content.strip()) < 50:
                raise ValueError(f"Content too short ({len(content)} bytes) - might be an error page")
            
            logger.info(f"Successfully fetched {filename} ({len(content)} bytes)")
            return filename, content
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {filename}: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY * (attempt + 1))
            else:
                raise Exception(f"Failed to fetch {filename} after {MAX_RETRIES} attempts: {e}")
        
        except ValueError as e:
            logger.error(f"Content validation failed for {filename}: {e}")
            raise


def save_markdown_file(docs_dir: Path, filename: str, content: str) -> None:
    """
    Save markdown content to a file.
    
    Args:
        docs_dir: The directory to save files in
        filename: The filename to save as
        content: The markdown content to save
    """
    file_path = docs_dir / filename
    
    try:
        file_path.write_text(content, encoding='utf-8')
        logger.info(f"Saved: {filename}")
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise


def cleanup_old_files(docs_dir: Path, current_files: set) -> None:
    """
    Remove markdown files that no longer exist in the documentation.
    
    Args:
        docs_dir: The directory containing documentation files
        current_files: Set of filenames that should exist
    """
    existing_files = set(f.name for f in docs_dir.glob('*.md'))
    files_to_remove = existing_files - current_files
    
    for filename in files_to_remove:
        file_path = docs_dir / filename
        logger.info(f"Removing obsolete file: {filename}")
        file_path.unlink()


def main():
    """Main function to orchestrate the documentation fetching."""
    start_time = datetime.now()
    logger.info("Starting Claude Code documentation fetch")
    
    # Create docs directory
    docs_dir = Path(__file__).parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {docs_dir}")
    
    # Statistics
    successful = 0
    failed = 0
    failed_pages = []
    fetched_files = set()
    
    # Create a session for connection pooling
    with requests.Session() as session:
        for i, page_path in enumerate(DOCUMENTATION_PAGES, 1):
            logger.info(f"Processing {i}/{len(DOCUMENTATION_PAGES)}: {page_path}")
            
            try:
                filename, content = fetch_markdown_content(page_path, session)
                save_markdown_file(docs_dir, filename, content)
                fetched_files.add(filename)
                successful += 1
                
                # Rate limiting
                if i < len(DOCUMENTATION_PAGES):
                    time.sleep(RATE_LIMIT_DELAY)
                    
            except Exception as e:
                logger.error(f"Failed to process {page_path}: {e}")
                failed += 1
                failed_pages.append(page_path)
                # Continue processing other pages instead of stopping
    
    # Clean up old files that no longer exist
    cleanup_old_files(docs_dir, fetched_files)
    
    # Summary
    duration = datetime.now() - start_time
    logger.info("\n" + "="*50)
    logger.info(f"Fetch completed in {duration}")
    logger.info(f"Successful: {successful}/{len(DOCUMENTATION_PAGES)}")
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