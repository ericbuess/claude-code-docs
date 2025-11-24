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
import os
import re
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Sitemap URLs to try - we'll discover from ALL of them and combine results
# Note: Claude Code docs are now split across multiple domains
SITEMAP_URLS = [
    "https://docs.claude.com/sitemap.xml",       # Agent SDK and main docs
    "https://code.claude.com/docs/sitemap.xml",  # Claude Code specific docs
    "https://docs.anthropic.com/sitemap.xml",    # Legacy/fallback
]
MANIFEST_FILE = "docs_manifest.json"

# Base URL will be discovered from sitemap
# No longer using global variable

# Headers to bypass caching and identify the script
HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/3.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

# Retry configuration
MAX_RETRIES = 3
RETRY_DELAY = 2  # initial delay in seconds
MAX_RETRY_DELAY = 30  # maximum delay in seconds
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def load_manifest(docs_dir: Path) -> dict:
    """Load the manifest of previously fetched files."""
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


def save_manifest(docs_dir: Path, manifest: dict) -> None:
    """Save the manifest of fetched files."""
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


def validate_repository_config(manifest: dict) -> None:
    """
    Validate that manifest repository matches actual git repository.
    Warns if there's a mismatch to catch configuration issues.
    """
    import subprocess

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


def update_paths_manifest(paths: List[str], manifest_file: Path = None) -> None:
    """
    Update paths_manifest.json with newly discovered paths from sitemaps.

    Args:
        paths: List of documentation paths discovered from sitemaps
        manifest_file: Optional path to manifest file (defaults to paths_manifest.json)
    """
    if manifest_file is None:
        manifest_file = Path(__file__).parent.parent / 'paths_manifest.json'
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


def discover_from_all_sitemaps(session: requests.Session) -> List[str]:
    """
    Discover documentation paths from ALL sitemaps and combine results.

    Returns:
        List of unique English documentation paths discovered from all sitemaps
    """
    all_paths = []
    successful_sitemaps = 0

    for sitemap_url in SITEMAP_URLS:
        try:
            logger.info(f"Discovering from sitemap: {sitemap_url}")
            paths = discover_claude_code_pages(session, sitemap_url)
            logger.info(f"  Found {len(paths)} paths from {sitemap_url}")
            all_paths.extend(paths)
            successful_sitemaps += 1
        except Exception as e:
            logger.warning(f"  Failed to discover from {sitemap_url}: {e}")
            continue

    if successful_sitemaps == 0:
        raise Exception("Could not discover from any sitemap")

    # Remove duplicates and sort
    unique_paths = sorted(list(set(all_paths)))
    logger.info(f"Total unique paths discovered from {successful_sitemaps} sitemaps: {len(unique_paths)}")

    return unique_paths


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
                # Parse XML safely to prevent XXE attacks
                try:
                    # Try with security parameters (Python 3.8+)
                    parser = ET.XMLParser(forbid_dtd=True, forbid_entities=True, forbid_external=True)
                    root = ET.fromstring(response.content, parser=parser)
                except TypeError:
                    # Fallback for older Python versions
                    logger.warning("XMLParser security parameters not available, using default parser")
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


def convert_legacy_path_to_fetch_url(path: str) -> str:
    """
    Convert legacy manifest paths to correct fetch URLs.

    Documentation is now split across two domains:
    1. code.claude.com - Claude Code docs with URL structure: /docs/en/{page}
    2. docs.claude.com - Everything else with URL structure: /en/{category}/{page}

    Mapping rules:
        Claude Code (code.claude.com):
            /en/docs/claude-code/hooks → /docs/en/hooks

        Everything else (docs.claude.com):
            /en/api/messages → /en/api/messages (no change)
            /en/docs/about-claude/models → /en/docs/about-claude/models (no change)
            /en/prompt-library/code-clarifier → /en/prompt-library/code-clarifier (no change)
            /en/resources/glossary → /en/resources/glossary (no change)
            /en/release-notes/api → /en/release-notes/api (no change)
            /en/home → /en/home (no change)

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

    # All other paths stay in /en/* format for docs.claude.com
    # This includes:
    # - /en/api/* → /en/api/*
    # - /en/docs/* (non-claude-code) → /en/docs/*
    # - /en/prompt-library/* → /en/prompt-library/*
    # - /en/resources/* → /en/resources/*
    # - /en/release-notes/* → /en/release-notes/*
    # - /en/home → /en/home
    return path


def load_paths_from_manifest() -> List[str]:
    """
    Load paths for files that already exist locally in ./docs/

    This is a FALLBACK used only if sitemap discovery fails.
    Normally, we discover ~273 active paths from sitemaps and fetch all of them.

    Returns:
        List of paths corresponding to existing local files (~266-270 files)
    """
    try:
        docs_dir = Path(__file__).parent.parent / 'docs'
        manifest_path = Path(__file__).parent.parent / 'paths_manifest.json'

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


def discover_claude_code_pages(session: requests.Session, sitemap_url: str) -> List[str]:
    """
    Dynamically discover all Claude Code documentation pages from the sitemap.
    Now with better pattern matching flexibility.
    """
    logger.info("Discovering documentation pages from sitemap...")
    
    try:
        response = session.get(sitemap_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        
        # Parse XML sitemap safely
        try:
            # Try with security parameters (Python 3.8+)
            parser = ET.XMLParser(forbid_dtd=True, forbid_entities=True, forbid_external=True)
            root = ET.fromstring(response.content, parser=parser)
        except TypeError:
            # Fallback for older Python versions
            logger.warning("XMLParser security parameters not available, using default parser")
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
        
        # Filter for ENGLISH documentation pages only
        claude_code_pages = []

        for url in urls:
            parsed = urlparse(url)
            path = parsed.path

            # Remove any file extension
            if path.endswith('.html'):
                path = path[:-5]
            elif path.endswith('/'):
                path = path[:-1]

            # ONLY accept paths that start with /en/ or /docs/en/
            # This excludes /de/, /fr/, /ja/, etc. (other languages)
            if path.startswith('/en/') or path.startswith('/docs/en/'):
                # Skip certain types of pages
                skip_patterns = [
                    '/examples/',  # Example pages
                    '/legacy/',    # Legacy documentation
                ]

                if not any(skip in path for skip in skip_patterns):
                    # Keep original path - normalization happens during fetch
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


def validate_markdown_content(content: str, filename: str) -> None:
    """
    Validate that content is proper markdown.
    Raises ValueError if validation fails.
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


def get_base_url_for_path(path: str) -> str:
    """
    Determine the correct base URL for a given documentation path.

    Documentation is hosted on two different domains:
    - code.claude.com: Paths starting with /docs/en/ (Claude Code docs)
    - docs.claude.com: Paths starting with /en/ (API, agent-sdk, prompt library, etc.)

    Args:
        path: Documentation path (e.g., /en/api/messages or /docs/en/analytics)

    Returns:
        Base URL (either https://code.claude.com or https://docs.claude.com)
    """
    # Claude Code docs on code.claude.com use /docs/en/ prefix
    if path.startswith('/docs/en/'):
        return 'https://code.claude.com'

    # Everything else (starting with /en/) is on docs.claude.com
    # This includes: /en/api/, /en/docs/agent-sdk/, /en/docs/about-claude/, etc.
    return 'https://docs.claude.com'


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


def content_has_changed(content: str, old_hash: str) -> bool:
    """Check if content has changed based on hash."""
    new_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
    return new_hash != old_hash


def fetch_changelog(session: requests.Session) -> Tuple[str, str]:
    """
    Fetch Claude Code changelog from GitHub repository.
    Returns tuple of (filename, content).
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
    logger.info("Starting documentation update (updating existing local files only)")
    
    # Log configuration
    github_repo = os.environ.get('GITHUB_REPOSITORY', 'costiash/claude-code-docs')
    logger.info(f"GitHub repository: {github_repo}")
    
    # Create docs directory at repository root
    docs_dir = Path(__file__).parent.parent / 'docs'
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
            base_url = "https://code.claude.com/docs"
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

        # If both failed, use minimal fallback
        if not documentation_pages:
            logger.warning("All discovery methods failed, using minimal fallback...")
            documentation_pages = [
                "/en/docs/claude-code/overview",
                "/en/docs/claude-code/setup",
                "/en/docs/claude-code/quickstart",
                "/en/docs/claude-code/hooks",
            ]
        
        if not documentation_pages:
            logger.error("No documentation pages discovered!")
            sys.exit(1)
        
        # Fetch each discovered page
        for i, page_path in enumerate(documentation_pages, 1):
            logger.info(f"Processing {i}/{len(documentation_pages)}: {page_path}")
            
            try:
                filename, content = fetch_markdown_content(page_path, session, base_url)
                
                # Check if content has changed
                old_hash = manifest.get("files", {}).get(filename, {}).get("hash", "")
                old_entry = manifest.get("files", {}).get(filename, {})
                
                if content_has_changed(content, old_hash):
                    content_hash = save_markdown_file(docs_dir, filename, content)
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