#!/usr/bin/env python3
"""
Clean paths_manifest.json by removing broken paths.

This script:
1. Reads paths_manifest.json
2. Validates each path (HTTP request)
3. Removes 404 paths
4. Updates category counts
5. Saves cleaned manifest
"""

import json
import requests
import time
from pathlib import Path
from typing import Dict, List, Set
from concurrent.futures import ThreadPoolExecutor, as_completed


BASE_URL = "https://docs.anthropic.com"
TIMEOUT = 10
MAX_WORKERS = 10
RATE_LIMIT = 0.1  # seconds between requests


def validate_path(path: str) -> tuple[str, bool, int]:
    """
    Validate a single path.

    Returns:
        (path, is_valid, status_code) tuple
    """
    url = f"{BASE_URL}{path}"
    try:
        response = requests.get(url, timeout=TIMEOUT)
        is_valid = response.status_code == 200
        status = response.status_code
        symbol = '✓' if is_valid else '✗'
        print(f"  {symbol} {path} ({status})")
        return (path, is_valid, status)
    except Exception as e:
        print(f"  ✗ {path} (Error: {str(e)[:50]})")
        return (path, False, 0)


def validate_paths_parallel(paths: List[str]) -> tuple[Set[str], Dict[str, int]]:
    """
    Validate paths in parallel.

    Returns:
        (valid_paths_set, broken_paths_dict)
    """
    valid_paths = set()
    broken_paths = {}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(validate_path, path): path for path in paths}

        for future in as_completed(futures):
            path, is_valid, status = future.result()
            if is_valid:
                valid_paths.add(path)
            else:
                broken_paths[path] = status
            time.sleep(RATE_LIMIT)  # Rate limiting

    return valid_paths, broken_paths


def clean_manifest(manifest_path: Path, output_path: Path = None):
    """
    Clean manifest by removing broken paths.
    """
    if output_path is None:
        output_path = manifest_path

    # Load manifest
    print(f"Loading manifest from {manifest_path}...")
    with open(manifest_path) as f:
        manifest = json.load(f)

    original_total = manifest['metadata']['total_paths']
    print(f"Original manifest: {original_total} paths")

    # Collect all paths
    all_paths = []
    for category, paths in manifest["categories"].items():
        all_paths.extend(paths)

    print(f"\nValidating {len(all_paths)} paths (this will take ~5-10 minutes)...")
    print("Please be patient...\n")

    # Validate paths
    valid_paths, broken_paths = validate_paths_parallel(all_paths)

    print(f"\n{'='*60}")
    print(f"VALIDATION RESULTS:")
    print(f"  Total paths: {len(all_paths)}")
    print(f"  Valid (200 OK): {len(valid_paths)} ({len(valid_paths)/len(all_paths)*100:.1f}%)")
    print(f"  Broken (404/error): {len(broken_paths)} ({len(broken_paths)/len(all_paths)*100:.1f}%)")
    print(f"{'='*60}\n")

    # Save broken paths report
    broken_report_path = Path("reports/validation/broken_paths.txt")
    broken_report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(broken_report_path, 'w') as f:
        f.write(f"BROKEN PATHS REPORT\n")
        f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total broken: {len(broken_paths)}\n\n")
        for path, status in sorted(broken_paths.items()):
            f.write(f"[{status}] {path}\n")
    print(f"Broken paths report saved to: {broken_report_path}")

    # Create cleaned manifest
    cleaned_categories = {}
    print(f"\nCleaning categories:")
    for category, paths in manifest["categories"].items():
        cleaned_paths = [p for p in paths if p in valid_paths]
        if cleaned_paths:  # Only include non-empty categories
            cleaned_categories[category] = sorted(cleaned_paths)
        kept = len(cleaned_paths)
        removed = len(paths) - kept
        print(f"  {category}: {kept}/{len(paths)} kept ({removed} removed)")

    cleaned_manifest = {
        "metadata": {
            "generated_at": manifest["metadata"]["generated_at"],
            "total_paths": len(valid_paths),
            "cleaned_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "removed_broken_paths": len(broken_paths),
            "original_total_paths": original_total,
        },
        "categories": cleaned_categories
    }

    # Save cleaned manifest
    with open(output_path, 'w') as f:
        json.dump(cleaned_manifest, f, indent=2)

    print(f"\n{'='*60}")
    print(f"✅ CLEANED MANIFEST SAVED")
    print(f"   Output: {output_path}")
    print(f"   Original: {original_total} paths")
    print(f"   Cleaned: {len(valid_paths)} paths")
    print(f"   Removed: {len(broken_paths)} broken paths")
    print(f"   Reachability: {len(valid_paths)/original_total*100:.1f}%")
    print(f"{'='*60}")

    return len(valid_paths), len(broken_paths)


if __name__ == "__main__":
    import sys

    manifest_file = Path("paths_manifest.json")

    if len(sys.argv) > 1:
        manifest_file = Path(sys.argv[1])

    # Backup original
    backup_file = manifest_file.with_suffix('.json.backup')
    import shutil
    shutil.copy(manifest_file, backup_file)
    print(f"Backup created: {backup_file}\n")

    valid_count, broken_count = clean_manifest(manifest_file)

    print(f"\n✅ COMPLETE!")
    print(f"Next steps:")
    print(f"1. Review broken paths: cat reports/validation/broken_paths.txt")
    print(f"2. Update documentation with new count: {valid_count} paths")
