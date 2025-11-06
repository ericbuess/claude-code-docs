#!/usr/bin/env python3
"""
Path Extraction and Cleaning Script

Extracts and cleans documentation paths from HTML sitemap, categorizes them,
and exports to multiple formats for downstream processing.

Usage:
    python extract_paths.py --source temp/temp.html --output paths_manifest.json
    python extract_paths.py --stats
    python extract_paths.py --validate
"""

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple


def clean_path(path: str) -> str:
    """
    Remove trailing backslashes, whitespace, and artifacts.

    Args:
        path: Raw path string

    Returns:
        Cleaned path string
    """
    # Strip whitespace
    path = path.strip()

    # Remove trailing backslashes (escaping artifacts)
    path = path.rstrip('\\')

    # Remove artifacts like ),
    path = path.rstrip('),')

    # Normalize multiple slashes to single slash
    path = re.sub(r'/+', '/', path)

    # Remove trailing slash (except for root paths)
    if len(path) > 1 and path.endswith('/'):
        path = path.rstrip('/')

    return path


def is_valid_path(path: str) -> bool:
    """
    Validate if path is a real documentation path.

    Args:
        path: Path to validate

    Returns:
        True if valid, False if noise pattern
    """
    # Filter out empty or whitespace-only paths
    if not path or not path.strip():
        return False

    # Filter out :slug* patterns (Next.js dynamic routes)
    if ':slug' in path:
        return False

    # Filter out paths with invalid characters
    if any(char in path for char in ['<', '>', '|', '*', '?']):
        return False

    # Must start with /en/
    if not path.startswith('/en/'):
        return False

    # Filter out too short paths (likely malformed)
    if len(path) < 5:  # /en/x minimum
        return False

    # Filter out paths with only /en/ or /en/api/ etc (category roots with :slug*)
    # These are captured in extracted_paths.txt as "/en/:slug*\" etc
    if path.endswith(':slug*'):
        return False

    return True


def categorize_path(path: str) -> str:
    """
    Assign category based on path prefix.

    Args:
        path: Documentation path

    Returns:
        Category name (core_documentation, api_reference, etc.)
    """
    # Must check claude-code BEFORE general docs (more specific first)
    if path.startswith('/en/docs/claude-code/'):
        return 'claude_code'

    # Core documentation (but not claude-code)
    if path.startswith('/en/docs/'):
        return 'core_documentation'

    # API reference
    if path.startswith('/en/api/'):
        return 'api_reference'

    # Prompt library
    if path.startswith('/en/prompt-library/'):
        return 'prompt_library'

    # Resources
    if path.startswith('/en/resources/'):
        return 'resources'

    # Release notes
    if path.startswith('/en/release-notes/'):
        return 'release_notes'

    # Uncategorized (should be rare)
    return 'uncategorized'


def extract_fragment(path: str) -> Tuple[str, str]:
    """
    Separate URL path from fragment identifier.

    Args:
        path: Full path with possible fragment

    Returns:
        Tuple of (path, fragment)
    """
    if '#' in path:
        parts = path.split('#', 1)
        return parts[0], parts[1]
    return path, ''


def extract_paths_from_html(html_file: Path) -> List[str]:
    """
    Extract all /en/ paths from HTML file.

    Args:
        html_file: Path to HTML file

    Returns:
        List of raw extracted paths
    """
    print(f"Reading HTML from {html_file}...")
    html_content = html_file.read_text(encoding='utf-8')

    # Extract all paths matching "/en/..." pattern
    # Matches both: "href":"/en/..." and href="/en/..."
    pattern = r'["\'](/en/[^"\']*)["\']'
    matches = re.findall(pattern, html_content)

    print(f"Found {len(matches)} raw path matches")
    return matches


def process_paths(raw_paths: List[str]) -> Dict[str, List[str]]:
    """
    Clean, validate, deduplicate, and categorize paths.

    Args:
        raw_paths: List of raw extracted paths

    Returns:
        Dictionary with categories as keys and sorted path lists as values
    """
    print("\nProcessing paths...")

    # Track statistics
    stats = {
        'raw_count': len(raw_paths),
        'cleaned_count': 0,
        'valid_count': 0,
        'with_fragments': 0,
        'duplicates_removed': 0
    }

    # Clean and validate
    cleaned_paths = []
    for raw_path in raw_paths:
        cleaned = clean_path(raw_path)
        if cleaned:
            stats['cleaned_count'] += 1
            if is_valid_path(cleaned):
                stats['valid_count'] += 1
                cleaned_paths.append(cleaned)

    # Remove duplicates while preserving order
    seen: Set[str] = set()
    unique_paths = []
    for path in cleaned_paths:
        if path not in seen:
            seen.add(path)
            unique_paths.append(path)
        else:
            stats['duplicates_removed'] += 1

    print(f"  - Raw paths: {stats['raw_count']}")
    print(f"  - After cleaning: {stats['cleaned_count']}")
    print(f"  - After validation: {stats['valid_count']}")
    print(f"  - Duplicates removed: {stats['duplicates_removed']}")
    print(f"  - Unique paths: {len(unique_paths)}")

    # Categorize paths
    categorized: Dict[str, List[str]] = {}
    fragment_paths = []

    for path in unique_paths:
        # Separate fragments
        path_without_fragment, fragment = extract_fragment(path)
        if fragment:
            stats['with_fragments'] += 1
            fragment_paths.append((path, path_without_fragment, fragment))
            # Use the path without fragment for categorization
            path = path_without_fragment

        category = categorize_path(path)
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(path)

    # Sort within categories
    for category in categorized:
        categorized[category] = sorted(set(categorized[category]))

    # Print category statistics
    print("\nCategory breakdown:")
    total = sum(len(paths) for paths in categorized.values())
    for category, paths in sorted(categorized.items()):
        percentage = (len(paths) / total * 100) if total > 0 else 0
        print(f"  - {category}: {len(paths)} paths ({percentage:.1f}%)")

    if fragment_paths:
        print(f"\nNote: {len(fragment_paths)} paths had fragment identifiers (e.g., #section)")

    return categorized


def export_manifest(paths_dict: Dict[str, List[str]], output_file: Path, source_file: Path):
    """
    Export categorized paths to JSON manifest.

    Args:
        paths_dict: Dictionary with categories and paths
        output_file: Path to output JSON file
        source_file: Path to source HTML file (for metadata)
    """
    print(f"\nExporting manifest to {output_file}...")

    total_paths = sum(len(paths) for paths in paths_dict.values())

    manifest = {
        "metadata": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total_paths": total_paths,
            "source": str(source_file),
            "categories_count": len(paths_dict)
        },
        "categories": paths_dict
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"Manifest exported successfully ({total_paths} paths)")


def export_clean_txt(paths_dict: Dict[str, List[str]], output_file: Path):
    """
    Export all paths to plain text file (one path per line).

    Args:
        paths_dict: Dictionary with categories and paths
        output_file: Path to output text file
    """
    print(f"Exporting clean paths to {output_file}...")

    # Collect all paths and sort
    all_paths = []
    for paths in paths_dict.values():
        all_paths.extend(paths)
    all_paths = sorted(set(all_paths))

    # Ensure parent directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        for path in all_paths:
            f.write(f"{path}\n")

    print(f"Clean paths exported ({len(all_paths)} paths)")


def show_statistics(manifest_file: Path):
    """
    Display statistics from existing manifest file.

    Args:
        manifest_file: Path to paths_manifest.json
    """
    if not manifest_file.exists():
        print(f"Error: Manifest file not found: {manifest_file}")
        print("Run without --stats flag to generate the manifest first.")
        return

    with open(manifest_file, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    metadata = manifest.get('metadata', {})
    categories = manifest.get('categories', {})

    print("\n" + "=" * 60)
    print("PATH STATISTICS")
    print("=" * 60)

    print("\nMetadata:")
    print(f"  Generated: {metadata.get('generated_at', 'Unknown')}")
    print(f"  Source: {metadata.get('source', 'Unknown')}")
    print(f"  Total paths: {metadata.get('total_paths', 0)}")
    print(f"  Categories: {metadata.get('categories_count', 0)}")

    print("\nCategory Breakdown:")
    total = sum(len(paths) for paths in categories.values())
    for category, paths in sorted(categories.items(), key=lambda x: len(x[1]), reverse=True):
        percentage = (len(paths) / total * 100) if total > 0 else 0
        print(f"  {category:20s}: {len(paths):4d} paths ({percentage:5.1f}%)")

    # Sample paths from each category
    print("\nSample paths (first 3 from each category):")
    for category, paths in sorted(categories.items()):
        print(f"\n  {category}:")
        for path in paths[:3]:
            print(f"    {path}")
        if len(paths) > 3:
            print(f"    ... and {len(paths) - 3} more")

    print("\n" + "=" * 60)


def validate_manifest(manifest_file: Path):
    """
    Validate the manifest file structure and content.

    Args:
        manifest_file: Path to paths_manifest.json
    """
    if not manifest_file.exists():
        print(f"Error: Manifest file not found: {manifest_file}")
        return False

    print(f"Validating manifest: {manifest_file}")

    try:
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    except json.JSONDecodeError as e:
        print(f"  ✗ Invalid JSON: {e}")
        return False

    # Check required fields
    if 'metadata' not in manifest:
        print("  ✗ Missing 'metadata' field")
        return False

    if 'categories' not in manifest:
        print("  ✗ Missing 'categories' field")
        return False

    metadata = manifest['metadata']
    categories = manifest['categories']

    # Validate metadata fields
    required_meta_fields = ['generated_at', 'total_paths', 'source']
    for field in required_meta_fields:
        if field not in metadata:
            print(f"  ✗ Missing metadata field: {field}")
            return False

    # Validate categories
    expected_categories = ['core_documentation', 'api_reference', 'claude_code', 'prompt_library']
    issues = []

    for expected in expected_categories:
        if expected not in categories:
            issues.append(f"Missing expected category: {expected}")

    # Validate paths
    total_paths = 0
    invalid_paths = []

    for category, paths in categories.items():
        if not isinstance(paths, list):
            issues.append(f"Category '{category}' does not contain a list")
            continue

        total_paths += len(paths)

        for path in paths:
            if not isinstance(path, str):
                invalid_paths.append(f"Non-string path in {category}")
                continue

            if not is_valid_path(path):
                invalid_paths.append(f"Invalid path: {path}")

            # Check for artifacts
            if '\\' in path:
                invalid_paths.append(f"Path contains backslash: {path}")
            if ':slug' in path:
                invalid_paths.append(f"Path contains :slug: {path}")

    # Report results
    print("\nValidation Results:")
    print(f"  ✓ JSON structure valid")
    print(f"  ✓ Required fields present")
    print(f"  ✓ Total paths: {total_paths}")

    if issues:
        print("\n  Issues found:")
        for issue in issues:
            print(f"    - {issue}")

    if invalid_paths:
        print("\n  Invalid paths found:")
        for invalid in invalid_paths[:10]:  # Show first 10
            print(f"    - {invalid}")
        if len(invalid_paths) > 10:
            print(f"    ... and {len(invalid_paths) - 10} more")

    if not issues and not invalid_paths:
        print("  ✓ No issues found")
        print("\n✓ Manifest is valid!")
        return True
    else:
        print(f"\n✗ Validation failed with {len(issues) + len(invalid_paths)} issues")
        return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description='Extract and clean documentation paths from HTML sitemap',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract paths and generate manifest
  python extract_paths.py --source temp/temp.html --output paths_manifest.json

  # Show statistics from existing manifest
  python extract_paths.py --stats

  # Validate existing manifest
  python extract_paths.py --validate
        """
    )

    parser.add_argument(
        '--source',
        type=Path,
        default=Path('temp/temp.html'),
        help='Input HTML file (default: temp/temp.html)'
    )

    parser.add_argument(
        '--output',
        type=Path,
        default=Path('paths_manifest.json'),
        help='Output JSON manifest file (default: paths_manifest.json)'
    )

    parser.add_argument(
        '--stats',
        action='store_true',
        help='Show statistics from existing manifest (no extraction)'
    )

    parser.add_argument(
        '--validate',
        action='store_true',
        help='Validate existing manifest (no extraction)'
    )

    args = parser.parse_args()

    # Handle stats mode
    if args.stats:
        show_statistics(args.output)
        return

    # Handle validate mode
    if args.validate:
        valid = validate_manifest(args.output)
        exit(0 if valid else 1)

    # Normal extraction mode
    if not args.source.exists():
        print(f"Error: Source file not found: {args.source}")
        exit(1)

    print("=" * 60)
    print("PATH EXTRACTION AND CLEANING")
    print("=" * 60)

    # Extract paths from HTML
    raw_paths = extract_paths_from_html(args.source)

    # Process (clean, validate, deduplicate, categorize)
    categorized_paths = process_paths(raw_paths)

    # Export to JSON manifest
    export_manifest(categorized_paths, args.output, args.source)

    # Export to clean text file
    clean_txt_file = Path('temp/extracted_paths_clean.txt')
    export_clean_txt(categorized_paths, clean_txt_file)

    print("\n" + "=" * 60)
    print("EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"\nOutput files:")
    print(f"  - {args.output} (JSON manifest with categories)")
    print(f"  - {clean_txt_file} (plain text, one path per line)")
    print(f"\nNext steps:")
    print(f"  - Review statistics: python extract_paths.py --stats")
    print(f"  - Validate output: python extract_paths.py --validate")


if __name__ == '__main__':
    main()
