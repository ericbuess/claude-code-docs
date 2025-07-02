#!/usr/bin/env python3
"""
Improved Claude Code documentation fetcher with better robustness.
"""

import requests
import time
from pathlib import Path
from typing import List, Tuple, Set, Optional
import logging
from datetime import datetime
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse
import json
import hashlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Sitemap URLs to try (in order of preference)
SITEMAP_URLS = [
    "https://docs.anthropic.com/sitemap.xml",
    "https://docs.anthropic.com/sitemap_index.xml",
    "https://anthropic.com/sitemap.xml"
]
MANIFEST_FILE = "docs_manifest.json"

# Base URL will be discovered from sitemap
BASE_URL = None

# Headers to bypass caching and identify the script
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/3.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def load_manifest(docs_dir: Path) -> dict:
    """Load the manifest of previously fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    if manifest_path.exists():
        try:
            return json.loads(manifest_path.read_text())
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
    return {"files": {}, "last_updated": None}


def save_manifest(docs_dir: Path, manifest: dict) -> None:
    """Save the manifest of fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    manifest["last_updated"] = datetime.now().isoformat()
    manifest["base_url"] = "https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/"
    manifest["description"] = "Claude Code documentation manifest. Keys are filenames, append to base_url for full URL."
    manifest_path.write_text(json.dumps(manifest, indent=2))


def url_to_safe_filename(url_path: str) -> str:
    """Convert a URL path to a safe filename that preserves hierarchy only when needed."""
    # Remove any known prefix patterns
    for prefix in ['/en/docs/claude-code/', '/docs/claude-code/', '/claude-code/']:
        if prefix in url_path:
            path = url_path.split(prefix)[-1]
            break
    else:
        # If no known prefix, take everything after the last occurrence of 'claude-code/'
        if 'claude-code/' in url_path:
            path = url_path.split('claude-code/')[-1]
        else:
            path = url_path
    
    # If no subdirectories, just use the filename
    if '/' not in path:
        return path + '.md' if not path.endswith('.md') else path
    
    # For subdirectories, replace slashes with double underscores
    # e.g., "advanced/setup" becomes "advanced__setup.md"
    safe_name = path.replace('/', '__')
    if not safe_name.endswith('.md'):
        safe_name += '.md'
    return safe_name


def discover_sitemap_and_base_url(session: requests.Session) -> Tuple[str, str]:
    """
    Discover the sitemap URL and extract the base URL from it.
    
    Returns:
        Tuple of (sitemap_url, base_url)
    """
    for sitemap_url in SITEMAP_URLS:
        try:
            logger.info(f"Trying sitemap: {sitemap_url}")
            response = session.get(sitemap_url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                # Extract base URL from the first URL in sitemap
                root = ET.fromstring(response.content)
                
                # Try with namespace first
                namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                first_url = None
                for url_elem in root.findall('.//ns:url', namespace):
                    loc_elem = url_elem.find('ns:loc', namespace)
                    if loc_elem is not None and loc_elem.text:
                        first_url = loc_elem.text
                        break
                
                # If no URLs found, try without namespace
                if not first_url:
                    for loc_elem in root.findall('.//loc'):
                        if loc_elem.text:
                            first_url = loc_elem.text
                            break
                
                if first_url:
                    parsed = urlparse(first_url)
                    base_url = f"{parsed.scheme}://{parsed.netloc}"
                    logger.info(f"Found sitemap at {sitemap_url}, base URL: {base_url}")
                    return sitemap_url, base_url
        except Exception as e:
            logger.warning(f"Failed to fetch {sitemap_url}: {e}")
            continue
    
    raise Exception("Could not find a valid sitemap")


def discover_claude_code_pages(session: requests.Session, sitemap_url: str) -> List[str]:
    """
    Dynamically discover all Claude Code documentation pages from the sitemap.
    Now with better pattern matching flexibility.
    """
    logger.info("Discovering documentation pages from sitemap...")
    
    try:
        response = session.get(sitemap_url, headers=HEADERS, timeout=30)
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
        
        # Filter for ENGLISH Claude Code documentation pages only
        claude_code_pages = []
        
        # Try multiple possible URL patterns for robustness
        patterns = [
            '/en/docs/claude-code/',
            '/docs/claude-code/',
            '/claude-code/',
        ]
        
        for url in urls:
            # Check if URL matches any known pattern
            if any(pattern in url for pattern in patterns):
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
                    '/api/',       # API reference pages
                    '/reference/', # Reference pages that aren't core docs
                ]
                
                if not any(skip in path for skip in skip_patterns):
                    claude_code_pages.append(path)
        
        # Remove duplicates and sort
        claude_code_pages = sorted(list(set(claude_code_pages)))
        
        logger.info(f"Discovered {len(claude_code_pages)} Claude Code documentation pages")
        
        return claude_code_pages
        
    except Exception as e:
        logger.error(f"Failed to discover pages from sitemap: {e}")
        logger.warning("Falling back to essential pages...")
        
        # More comprehensive fallback list
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
            "/en/docs/claude-code/security",
            "/en/docs/claude-code/settings",
            "/en/docs/claude-code/hooks",
            "/en/docs/claude-code/costs",
            "/en/docs/claude-code/monitoring-usage",
        ]


def fetch_markdown_content(path: str, session: requests.Session, base_url: str) -> Tuple[str, str]:
    """
    Fetch markdown content with better error handling.
    """
    markdown_url = f"{base_url}{path}.md"
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
            
            # Verify we got markdown content
            content = response.text
            if not content or content.startswith('<!DOCTYPE') or '<html' in content[:100]:
                raise ValueError("Received HTML instead of markdown")
            
            # Additional validation
            if len(content.strip()) < 50:
                raise ValueError(f"Content too short ({len(content)} bytes)")
            
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


def content_has_changed(content: str, old_hash: str) -> bool:
    """Check if content has changed based on hash."""
    new_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return new_hash != old_hash


def save_markdown_file(docs_dir: Path, filename: str, content: str) -> str:
    """Save markdown content and return its hash."""
    file_path = docs_dir / filename
    
    try:
        file_path.write_text(content, encoding='utf-8')
        content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        logger.info(f"Saved: {filename}")
        return content_hash
    except Exception as e:
        logger.error(f"Failed to save {filename}: {e}")
        raise


def cleanup_old_files(docs_dir: Path, current_files: Set[str], manifest: dict) -> None:
    """
    Remove only files that were previously fetched but no longer exist.
    Preserves manually added files.
    """
    previous_files = set(manifest.get("files", {}).keys())
    files_to_remove = previous_files - current_files
    
    for filename in files_to_remove:
        if filename == MANIFEST_FILE:  # Never delete the manifest
            continue
            
        file_path = docs_dir / filename
        if file_path.exists():
            logger.info(f"Removing obsolete file: {filename}")
            file_path.unlink()


def main():
    """Main function with improved robustness."""
    start_time = datetime.now()
    logger.info("Starting Claude Code documentation fetch (improved version)")
    
    # Create docs directory
    docs_dir = Path(__file__).parent / 'docs'
    docs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {docs_dir}")
    
    # Load manifest
    manifest = load_manifest(docs_dir)
    
    # Statistics
    successful = 0
    failed = 0
    failed_pages = []
    fetched_files = set()
    new_manifest = {"files": {}}
    
    # Create a session for connection pooling
    with requests.Session() as session:
        # Discover sitemap and base URL
        try:
            sitemap_url, base_url = discover_sitemap_and_base_url(session)
            global BASE_URL
            BASE_URL = base_url
        except Exception as e:
            logger.error(f"Failed to discover sitemap: {e}")
            logger.info("Using fallback configuration...")
            BASE_URL = "https://docs.anthropic.com"
            sitemap_url = None
        
        # Discover documentation pages dynamically
        if sitemap_url:
            documentation_pages = discover_claude_code_pages(session, sitemap_url)
        else:
            # Use fallback pages if sitemap discovery failed
            documentation_pages = [
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
                "/en/docs/claude-code/security",
                "/en/docs/claude-code/settings",
                "/en/docs/claude-code/hooks",
                "/en/docs/claude-code/costs",
                "/en/docs/claude-code/monitoring-usage",
            ]
        
        if not documentation_pages:
            logger.error("No documentation pages discovered!")
            sys.exit(1)
        
        # Fetch each discovered page
        for i, page_path in enumerate(documentation_pages, 1):
            logger.info(f"Processing {i}/{len(documentation_pages)}: {page_path}")
            
            try:
                filename, content = fetch_markdown_content(page_path, session, BASE_URL)
                
                # Check if content has changed
                old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
                if content_has_changed(content, old_hash):
                    content_hash = save_markdown_file(docs_dir, filename, content)
                    logger.info(f"Updated: {filename}")
                else:
                    content_hash = old_hash
                    logger.info(f"Unchanged: {filename}")
                
                new_manifest["files"][filename] = {
                    "original_url": f"{BASE_URL}{page_path}",
                    "original_md_url": f"{BASE_URL}{page_path}.md",
                    "hash": content_hash,
                    "last_updated": datetime.now().isoformat()
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
    
    # Clean up old files (only those we previously fetched)
    cleanup_old_files(docs_dir, fetched_files, manifest)
    
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