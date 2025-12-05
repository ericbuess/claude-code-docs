"""
Path validation functionality.

This module provides:
- Single path validation
- Batch validation with parallel execution
- Validation statistics tracking
"""

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Dict, List, Optional

import requests

from .config import REQUEST_TIMEOUT, MAX_WORKERS, get_base_url_for_path, logger


class ValidationStats:
    """Track validation statistics with thread-safety."""

    def __init__(self):
        self.total = 0
        self.reachable = 0
        self.not_found = 0
        self.timeout = 0
        self.error = 0
        self.lock = threading.Lock()
        self.broken_paths: List[Dict] = []

    def add_result(self, path: str, status: str, status_code: Optional[int] = None):
        """Thread-safe result recording."""
        with self.lock:
            self.total += 1

            if status == 'reachable':
                self.reachable += 1
            elif status == 'not_found':
                self.not_found += 1
                self.broken_paths.append({
                    'path': path,
                    'status_code': status_code,
                    'reason': '404 Not Found'
                })
            elif status == 'timeout':
                self.timeout += 1
                self.broken_paths.append({
                    'path': path,
                    'status_code': None,
                    'reason': 'Timeout'
                })
            elif status == 'error':
                self.error += 1
                self.broken_paths.append({
                    'path': path,
                    'status_code': status_code,
                    'reason': 'HTTP Error'
                })

    def get_summary(self) -> Dict:
        """Get validation summary."""
        return {
            'total': self.total,
            'reachable': self.reachable,
            'not_found': self.not_found,
            'timeout': self.timeout,
            'error': self.error,
            'reachability_percent': round((self.reachable / self.total * 100), 2)
                                   if self.total > 0 else 0,
            'broken_paths': self.broken_paths
        }


def validate_path(
    path: str,
    base_url: str = None,
    timeout: int = REQUEST_TIMEOUT
) -> Dict:
    """
    Validate that a path is reachable.

    Args:
        path: Documentation path to validate
        base_url: Base URL for documentation site (auto-detected if None)
        timeout: Request timeout in seconds

    Returns:
        Validation result dictionary
    """
    # Auto-detect the correct base URL based on path
    if base_url is None:
        base_url = get_base_url_for_path(path)

    # Note: URLs don't use .md extension for validation
    url = f"{base_url}{path}"

    try:
        response = requests.head(
            url,
            timeout=timeout,
            allow_redirects=True
        )

        return {
            'path': path,
            'url': url,
            'status_code': response.status_code,
            'reachable': response.status_code == 200,
            'redirect': response.url if response.url != url else None,
            'error': None
        }

    except requests.exceptions.Timeout:
        return {
            'path': path,
            'url': url,
            'status_code': None,
            'reachable': False,
            'redirect': None,
            'error': 'Timeout'
        }

    except requests.exceptions.RequestException as e:
        return {
            'path': path,
            'url': url,
            'status_code': None,
            'reachable': False,
            'redirect': None,
            'error': str(e)
        }


def batch_validate(
    paths: List[str],
    base_url: str = None,
    max_workers: int = MAX_WORKERS
) -> ValidationStats:
    """
    Validate multiple paths in parallel.

    Args:
        paths: List of paths to validate
        base_url: Base URL for documentation site (auto-detected per path if None)
        max_workers: Number of parallel workers

    Returns:
        ValidationStats object
    """
    stats = ValidationStats()

    logger.info(f"Validating {len(paths)} paths with {max_workers} workers...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks - pass None for base_url to auto-detect per path
        future_to_path = {
            executor.submit(validate_path, path, base_url): path
            for path in paths
        }

        # Process results as they complete
        for i, future in enumerate(as_completed(future_to_path), 1):
            path = future_to_path[future]

            try:
                result = future.result()

                # Update stats
                if result['reachable']:
                    stats.add_result(path, 'reachable')
                    logger.debug(f"✓ {path}")
                elif result['error'] == 'Timeout':
                    stats.add_result(path, 'timeout')
                    logger.warning(f"⏱ Timeout: {path}")
                elif result['status_code'] == 404:
                    stats.add_result(path, 'not_found', 404)
                    logger.warning(f"✗ 404: {path}")
                else:
                    stats.add_result(path, 'error', result['status_code'])
                    logger.warning(f"✗ Error: {path} ({result['error']})")

                # Progress indicator
                if i % 10 == 0 or i == len(paths):
                    progress = (i / len(paths)) * 100
                    logger.info(f"Progress: {i}/{len(paths)} ({progress:.1f}%)")

            except Exception as e:
                logger.error(f"Exception validating {path}: {e}")
                stats.add_result(path, 'error')

    return stats


def load_batch_file(file_path: Path) -> List[str]:
    """
    Load paths from a file (one per line).

    Args:
        file_path: Path to file

    Returns:
        List of paths
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        paths = [line.strip() for line in f if line.strip()]

    return paths
