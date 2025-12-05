"""
Sitemap discovery and parsing functionality.

This module handles:
- Discovering sitemaps from multiple URLs
- Parsing XML sitemaps safely (XXE prevention)
- Extracting English documentation paths
"""

import xml.etree.ElementTree as ET
from typing import List, Tuple
from urllib.parse import urlparse

import requests

from .config import SITEMAP_URLS, HEADERS, logger


def discover_from_all_sitemaps(session: requests.Session) -> List[str]:
    """
    Discover documentation paths from ALL sitemaps and combine results.

    Args:
        session: Requests session for connection pooling

    Returns:
        List of unique English documentation paths discovered from all sitemaps

    Raises:
        Exception: If no sitemaps could be discovered from
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

    Args:
        session: Requests session for connection pooling

    Returns:
        Tuple of (sitemap_url, base_url)

    Raises:
        Exception: If no valid sitemap could be found
    """
    for sitemap_url in SITEMAP_URLS:
        try:
            logger.info(f"Trying sitemap: {sitemap_url}")
            response = session.get(sitemap_url, headers=HEADERS, timeout=30)
            if response.status_code == 200:
                # Extract base URL from the first URL in sitemap
                root = _parse_xml_safely(response.content)

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

    Args:
        session: Requests session for connection pooling
        sitemap_url: URL of the sitemap to parse

    Returns:
        List of English documentation paths
    """
    logger.info("Discovering documentation pages from sitemap...")

    try:
        response = session.get(sitemap_url, headers=HEADERS, timeout=30)
        response.raise_for_status()

        # Parse XML sitemap safely
        root = _parse_xml_safely(response.content)

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


def _parse_xml_safely(content: bytes) -> ET.Element:
    """
    Parse XML content safely to prevent XXE attacks.

    Args:
        content: Raw XML content bytes

    Returns:
        Parsed XML root element
    """
    try:
        # Try with security parameters (Python 3.8+)
        parser = ET.XMLParser(forbid_dtd=True, forbid_entities=True, forbid_external=True)
        return ET.fromstring(content, parser=parser)
    except TypeError:
        # Fallback for older Python versions
        logger.warning("XMLParser security parameters not available, using default parser")
        return ET.fromstring(content)
