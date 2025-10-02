#!/usr/bin/env python3
"""
Migration script to rename documentation files using the new consistent naming scheme.

This script:
1. Reads the existing manifest
2. Calculates new filenames using the improved logic
3. Renames files on disk
4. Updates the manifest with new filenames
"""

import json
import sys
from pathlib import Path
from typing import Dict


def new_url_to_safe_filename(url_path: str) -> str:
    """
    New consistent filename logic.
    Strip /en/ prefix and preserve full path structure with __ separators.
    """
    # Strip universal language prefix (all docs are English)
    if url_path.startswith('/en/'):
        path = url_path[4:]  # Remove '/en/'
    else:
        path = url_path

    # Clean leading/trailing slashes
    path = path.strip('/')

    # Convert path separators to double underscores
    safe_name = path.replace('/', '__')

    # Ensure .md extension
    if not safe_name.endswith('.md'):
        safe_name += '.md'

    return safe_name


def main():
    # Get docs directory
    docs_dir = Path(__file__).parent.parent / 'docs'
    manifest_path = docs_dir / 'docs_manifest.json'

    print("Claude Docs Filename Migration Script")
    print("=" * 60)
    print(f"Docs directory: {docs_dir}")
    print()

    # Load existing manifest
    if not manifest_path.exists():
        print("ERROR: docs_manifest.json not found!")
        sys.exit(1)

    with open(manifest_path, 'r') as f:
        manifest = json.load(f)

    print(f"Loaded manifest with {len(manifest['files'])} files")
    print()

    # Calculate renames
    renames = []
    new_manifest_files = {}

    for old_filename, file_data in manifest['files'].items():
        # Extract URL path from original_url
        original_url = file_data.get('original_url', '')

        # Remove the base domain and .md extension to get path
        url_path = original_url.replace('https://docs.claude.com', '').replace('.md', '')

        # Calculate new filename
        new_filename = new_url_to_safe_filename(url_path)

        # Track if rename is needed
        if old_filename != new_filename:
            old_path = docs_dir / old_filename
            new_path = docs_dir / new_filename

            if old_path.exists():
                renames.append((old_path, new_path, old_filename, new_filename))

        # Update manifest with new filename
        new_manifest_files[new_filename] = file_data

    print(f"Files to rename: {len(renames)}")
    print(f"Files unchanged: {len(manifest['files']) - len(renames)}")
    print()

    if not renames:
        print("No files need renaming. Migration complete!")
        return

    # Show sample renames
    print("Sample renames (first 10):")
    print("-" * 60)
    for old_path, new_path, old_name, new_name in renames[:10]:
        print(f"  {old_name}")
        print(f"    → {new_name}")
    if len(renames) > 10:
        print(f"  ... and {len(renames) - 10} more")
    print()

    # Confirm
    response = input("Proceed with renaming? [y/N]: ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return

    # Perform renames
    print()
    print("Renaming files...")
    success = 0
    failed = 0

    for old_path, new_path, old_name, new_name in renames:
        try:
            old_path.rename(new_path)
            success += 1
            if success <= 5 or success % 10 == 0:
                print(f"  ✓ Renamed {success}/{len(renames)}: {old_name}")
        except Exception as e:
            print(f"  ✗ Failed to rename {old_name}: {e}")
            failed += 1

    print()
    print(f"Renamed: {success} files")
    if failed > 0:
        print(f"Failed: {failed} files")

    # Update manifest
    print()
    print("Updating manifest...")
    manifest['files'] = new_manifest_files

    # Add migration metadata
    from datetime import datetime
    if 'migrations' not in manifest:
        manifest['migrations'] = []

    manifest['migrations'].append({
        'timestamp': datetime.now().isoformat(),
        'type': 'filename_consistency_update',
        'files_renamed': success,
        'description': 'Updated all filenames to use consistent /en/ stripping logic'
    })

    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print("✓ Manifest updated")
    print()
    print("=" * 60)
    print("Migration complete!")
    print(f"  Files renamed: {success}")
    print(f"  Files failed: {failed}")
    print(f"  Total files: {len(manifest['files'])}")


if __name__ == '__main__':
    main()
