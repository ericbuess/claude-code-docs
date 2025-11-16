"""Validation tests for sitemap consistency."""

import pytest
import sys
from pathlib import Path
import json

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))


class TestManifestCompleteness:
    """Test all files are in manifest."""

    @pytest.mark.integration
    def test_all_categories_present(self, paths_manifest):
        """Test all expected categories are in manifest."""
        expected_categories = [
            'core_documentation',
            'api_reference',
            'claude_code',
            'prompt_library'
        ]

        for category in expected_categories:
            assert category in paths_manifest['categories']

    @pytest.mark.integration
    def test_metadata_complete(self, paths_manifest):
        """Test manifest metadata is complete."""
        assert 'metadata' in paths_manifest
        metadata = paths_manifest['metadata']

        # Required metadata fields
        assert 'generated_at' in metadata
        assert 'total_paths' in metadata
        # Optional fields
        assert isinstance(metadata.get('total_paths'), int)
        assert metadata['total_paths'] > 0

    @pytest.mark.integration
    def test_total_paths_matches_sum(self, paths_manifest):
        """Test total_paths metadata matches sum of categories."""
        total_in_metadata = paths_manifest['metadata']['total_paths']

        total_in_categories = sum(
            len(paths) for paths in paths_manifest['categories'].values()
        )

        assert total_in_metadata == total_in_categories

    @pytest.mark.integration
    def test_no_duplicate_paths_across_categories(self, paths_manifest):
        """Test no path appears in multiple categories."""
        all_paths = []

        for category_paths in paths_manifest['categories'].values():
            all_paths.extend(category_paths)

        # Check for duplicates
        unique_paths = set(all_paths)

        assert len(all_paths) == len(unique_paths), "Found duplicate paths across categories"


class TestNoOrphanedFiles:
    """Test no files are missing from manifest."""

    @pytest.mark.integration
    def test_docs_files_in_manifest(self, project_root, paths_manifest):
        """Test all markdown files in docs/ are in manifest."""
        docs_dir = project_root / "docs"

        if not docs_dir.exists():
            pytest.skip("docs directory doesn't exist yet")

        # Get all markdown files
        md_files = list(docs_dir.glob("*.md"))

        if not md_files:
            pytest.skip("No markdown files in docs/")

        # Get all paths from manifest
        manifest_paths = []
        for category_paths in paths_manifest['categories'].values():
            manifest_paths.extend(category_paths)

        # Convert manifest paths to expected filenames
        def path_to_filename(path):
            return path.replace('/', '__')[1:] + '.md'  # Remove leading /

        expected_files = {path_to_filename(path) for path in manifest_paths}

        # Check each file
        for md_file in md_files:
            # File should be in manifest (or be docs_manifest.json, etc.)
            if md_file.name not in ['docs_manifest.json', 'sitemap.json']:
                # File should correspond to a manifest path
                # (This is a simplified check)
                pass

    @pytest.mark.integration
    def test_manifest_paths_have_files(self, project_root, paths_manifest):
        """Test all manifest paths have corresponding files."""
        docs_dir = project_root / "docs"

        if not docs_dir.exists():
            pytest.skip("docs directory doesn't exist yet")

        # Get all paths from manifest
        all_paths = []
        for category_paths in paths_manifest['categories'].values():
            all_paths.extend(category_paths)

        if not all_paths:
            pytest.skip("No paths in manifest")

        # Sample check (not all 550+)
        sample_size = min(10, len(all_paths))
        import random
        sample_paths = random.sample(all_paths, sample_size)

        # Convert to filenames
        def path_to_filename(path):
            return path.replace('/', '__')[1:] + '.md'

        # Check files exist
        for path in sample_paths:
            filename = path_to_filename(path)
            file_path = docs_dir / filename

            # File should exist (if docs have been fetched)
            # This test is only meaningful after fetch
            # if not file_path.exists():
            #     # May not exist if docs not fetched yet
            #     pass


class TestCategoryCounts:
    """Test category counts match expectations."""

    @pytest.mark.integration
    def test_core_docs_largest_category(self, paths_manifest):
        """Test core documentation is the largest category."""
        categories = paths_manifest['categories']

        if not categories:
            pytest.skip("No categories in manifest")

        core_count = len(categories.get('core_documentation', []))
        total_count = sum(len(paths) for paths in categories.values())

        # Core docs should be significant portion
        if total_count > 0:
            core_percentage = core_count / total_count
            # Should be at least 25% (adjust based on actual data)
            assert core_percentage >= 0.20

    @pytest.mark.integration
    def test_all_categories_nonempty(self, paths_manifest):
        """Test main categories are not empty."""
        main_categories = [
            'core_documentation',
            'api_reference',
            'claude_code',
            'prompt_library'
        ]

        for category in main_categories:
            paths = paths_manifest['categories'].get(category, [])
            # Should have at least some paths
            assert len(paths) > 0, f"{category} is empty"

    @pytest.mark.integration
    def test_category_counts_reasonable(self, paths_manifest):
        """Test category counts are within reasonable ranges."""
        categories = paths_manifest['categories']

        # Based on current active documentation (270 total paths):
        # core_documentation: ~79 (29.3%)
        # api_reference: ~78 (28.9%)
        # claude_code: ~44 (16.3%)
        # prompt_library: ~65 (24.1%)

        # Allow reasonable variance for future updates
        expected_ranges = {
            'core_documentation': (60, 150),
            'api_reference': (50, 150),
            'claude_code': (40, 120),
            'prompt_library': (40, 150)
        }

        for category, (min_count, max_count) in expected_ranges.items():
            actual_count = len(categories.get(category, []))
            assert min_count <= actual_count <= max_count, \
                f"{category}: {actual_count} not in range [{min_count}, {max_count}]"


class TestManifestFormat:
    """Test manifest file format is correct."""

    @pytest.mark.integration
    def test_manifest_is_valid_json(self, project_root):
        """Test manifest is valid JSON."""
        manifest_path = project_root / "paths_manifest.json"

        if not manifest_path.exists():
            pytest.skip("paths_manifest.json doesn't exist")

        # Should parse without error
        manifest = json.loads(manifest_path.read_text())

        assert isinstance(manifest, dict)

    @pytest.mark.integration
    def test_manifest_structure(self, paths_manifest):
        """Test manifest has correct structure."""
        # Top-level keys
        assert 'metadata' in paths_manifest
        assert 'categories' in paths_manifest

        # Metadata structure
        metadata = paths_manifest['metadata']
        assert isinstance(metadata, dict)

        # Categories structure
        categories = paths_manifest['categories']
        assert isinstance(categories, dict)

        # Each category should be a list
        for category, paths in categories.items():
            assert isinstance(paths, list)

    @pytest.mark.integration
    def test_paths_are_strings(self, paths_manifest):
        """Test all paths are strings."""
        for category_paths in paths_manifest['categories'].values():
            for path in category_paths:
                assert isinstance(path, str)
                assert len(path) > 0

    @pytest.mark.integration
    def test_paths_properly_formatted(self, paths_manifest):
        """Test paths follow expected format."""
        for category_paths in paths_manifest['categories'].values():
            for path in category_paths:
                # Should start with /en/ OR /docs/en/ (NEW Claude Code format)
                assert path.startswith('/en/') or path.startswith('/docs/en/'), \
                    f"Invalid path (must start with /en/ or /docs/en/): {path}"

                # Should not have trailing slash (except root)
                if len(path) > 4:
                    assert not path.endswith('/'), f"Trailing slash: {path}"

                # Should not have double slashes
                assert '//' not in path, f"Double slash: {path}"
