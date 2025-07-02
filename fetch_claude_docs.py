#!/usr/bin/env python3
"""
Fetch all Claude Code documentation pages as markdown files.
This script dynamically discovers pages from the sitemap and downloads the latest versions.
"""

import requests
import time
from pathlib import Path
from typing import List, Tuple, Set
import logging
from datetime import datetime
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Base URL for the documentation
BASE_URL = "https://docs.anthropic.com"
SITEMAP_URL = f"{BASE_URL}/sitemap.xml"

# Headers to bypass caching and identify the script
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/2.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def discover_claude_code_pages(session: requests.Session) -> List[str]:
    """
    Dynamically discover all Claude Code documentation pages from the sitemap.
    
    Args:
        session: The requests session to use
        
    Returns:
        List of documentation page paths
    """
    logger.info("Fetching sitemap to discover documentation pages...")
    
    try:
        response = session.get(SITEMAP_URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # Parse XML sitemap
        root = ET.fromstring(response.content)
        
        # Extract all URLs from sitemap
        urls = []
        
        # Try with namespace first
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        for url_elem in root.findall('.//ns:url', namespace):
            loc_elem = url_elem.find('ns:loc', namespace)
            if loc_elem is not None and loc_elem.text:
                urls.append(loc_elem.text)
        
        # If no URLs found, try without namespace
        if not urls:
            for loc_elem in root.findall('.//loc'):
                if loc_elem.text:
                    urls.append(loc_elem.text)
        
        logger.info(f"Found {len(urls)} total URLs in sitemap")
        
        # Filter for English Claude Code documentation pages
        claude_code_pages = []
        claude_code_urls = 0
        
        for url in urls:
            # Check if it's a Claude Code page in English
            if '/en/docs/claude-code/' in url:
                claude_code_urls += 1
                # Convert full URL to path
                parsed = urlparse(url)
                path = parsed.path
                
                # Remove any file extension
                if path.endswith('.html'):
                    path = path[:-5]
                elif path.endswith('/'):
                    path = path[:-1]
                
                # Skip certain types of pages
                skip_patterns = [
                    '/tool-use/',  # Tool-specific pages
                    '/examples/',  # Example pages
                    '/legacy/',    # Legacy documentation
                ]
                
                if not any(pattern in path for pattern in skip_patterns):
                    claude_code_pages.append(path)
        
        logger.info(f"Found {claude_code_urls} Claude Code URLs, kept {len(claude_code_pages)} after filtering")
        
        # Sort for consistent ordering
        claude_code_pages.sort()
        
        logger.info(f"Discovered {len(claude_code_pages)} Claude Code documentation pages")
        
        return claude_code_pages
        
    except Exception as e:
        logger.error(f"Failed to discover pages from sitemap: {e}")
        logger.warning("Falling back to hardcoded list...")
        
        # Fallback to essential pages if sitemap fails
        return [
            "/en/docs/claude-code/overview",
            "/en/docs/claude-code/setup",
            "/en/docs/claude-code/quickstart",
            "/en/docs/claude-code/memory",
            "/en/docs/claude-code/common-workflows",
            "/en/docs/claude-code/ide-integrations",
            "/en/docs/claude-code/mcp",
            "/en/docs/claude-code/github-actions",
            "/en/docs/claude-code/sdk",
            "/en/docs/claude-code/troubleshooting",
        ]


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


def cleanup_old_files(docs_dir: Path, current_files: Set[str]) -> None:
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
    logger.info("Starting Claude Code documentation fetch (dynamic discovery)")
    
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
        # Discover documentation pages dynamically
        documentation_pages = discover_claude_code_pages(session)
        
        if not documentation_pages:
            logger.error("No documentation pages discovered!")
            sys.exit(1)
        
        # Fetch each discovered page
        for i, page_path in enumerate(documentation_pages, 1):
            logger.info(f"Processing {i}/{len(documentation_pages)}: {page_path}")
            
            try:
                filename, content = fetch_markdown_content(page_path, session)
                save_markdown_file(docs_dir, filename, content)
                fetched_files.add(filename)
                successful += 1
                
                # Rate limiting
                if i < len(documentation_pages):
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