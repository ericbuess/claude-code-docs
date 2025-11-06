"""Tests for manifest validation and consistency

Verifies:
- No 404 paths in paths_manifest.json
- Manifest metadata accuracy
- No duplicate paths
- docs_manifest.json matches actual files
"""
import pytest
import json
from pathlib import Path

@pytest.fixture
def project_root():
    """Path to project root"""
    return Path(__file__).parent.parent.parent

@pytest.fixture
def paths_manifest(project_root):
    """Load paths_manifest.json"""
    with open(project_root / 'paths_manifest.json') as f:
        return json.load(f)

@pytest.fixture
def docs_manifest(project_root):
    """Load docs/docs_manifest.json"""
    with open(project_root / 'docs' / 'docs_manifest.json') as f:
        return json.load(f)

@pytest.fixture
def broken_paths(project_root):
    """Load categorized broken paths if available"""
    broken_file = project_root / 'analysis' / 'broken_paths_categorized.json'
    if broken_file.exists():
        with open(broken_file) as f:
            return json.load(f)
    return {}

class TestPathsManifest:
    """Tests for paths_manifest.json"""

    def test_no_deprecated_paths(self, paths_manifest, broken_paths):
        """Ensure manifest doesn't contain deprecated paths"""
        if not broken_paths:
            pytest.skip("broken_paths_categorized.json not available")

        deprecated = set(broken_paths.get('deprecated_paths', []))

        # Check all categories
        for category, paths in paths_manifest['categories'].items():
            for path in paths:
                assert path not in deprecated, \
                    f"Deprecated path found: {path} in {category}"

    def test_metadata_accuracy(self, paths_manifest):
        """Ensure metadata reflects actual content"""
        # Count actual paths
        actual_count = sum(
            len(paths) for paths in paths_manifest['categories'].values()
        )
        stated_count = paths_manifest['metadata']['total_paths']

        assert actual_count == stated_count, \
            f"Metadata mismatch: stated {stated_count}, actual {actual_count}"

    def test_no_duplicate_paths(self, paths_manifest):
        """Ensure no path appears multiple times"""
        all_paths = []
        for paths in paths_manifest['categories'].values():
            all_paths.extend(paths)

        # Find duplicates
        duplicates = [p for p in set(all_paths) if all_paths.count(p) > 1]

        assert len(duplicates) == 0, \
            f"Duplicate paths in manifest: {duplicates}"

    def test_cleaned_metadata_exists(self, paths_manifest):
        """Verify manifest was cleaned (has cleaning metadata)"""
        metadata = paths_manifest['metadata']

        # Should have cleaning info after Task 1.5
        if 'cleaned_at' in metadata:
            assert 'removed_broken_paths' in metadata
            assert 'original_total_paths' in metadata

            removed = metadata.get('removed_broken_paths', 0)
            assert removed > 0, "Should have removed some broken paths"

class TestDocsManifest:
    """Tests for docs/docs_manifest.json"""

    def test_matches_actual_files(self, docs_manifest, project_root):
        """Ensure manifest matches actual files in docs/"""
        docs_dir = project_root / 'docs'
        actual_files = set(
            f.name for f in docs_dir.glob('*.md')
            if f.name != 'docs_manifest.json'
        )
        manifest_files = set(docs_manifest.keys())

        # Files in manifest but not on disk
        missing = manifest_files - actual_files
        # Files on disk but not in manifest
        extra = actual_files - manifest_files

        assert len(missing) == 0, \
            f"Manifest references missing files: {missing}"

        # Extra files are okay (might be new), but should be few
        if len(extra) > 5:
            pytest.fail(f"Many files not in manifest: {extra}")

    def test_expected_file_count(self, docs_manifest):
        """Verify manifest has expected number of files"""
        # After deduplication: 269 files
        file_count = len(docs_manifest)

        assert file_count == 269, \
            f"Expected 269 files in manifest, found {file_count}"

    def test_all_entries_have_required_fields(self, docs_manifest):
        """Ensure all manifest entries have required fields"""
        required_fields = {'original_url', 'original_md_url', 'hash', 'last_updated'}

        for filename, entry in docs_manifest.items():
            missing_fields = required_fields - set(entry.keys())
            assert len(missing_fields) == 0, \
                f"{filename} missing fields: {missing_fields}"

class TestSearchIndex:
    """Tests for search index consistency"""

    def test_search_index_exists(self, project_root):
        """Verify search index file exists"""
        search_index = project_root / 'docs' / '.search_index.json'
        assert search_index.exists(), "Search index not found"

    def test_search_index_valid_json(self, project_root):
        """Verify search index is valid JSON"""
        search_index = project_root / 'docs' / '.search_index.json'

        with open(search_index) as f:
            data = json.load(f)

        assert 'indexed_files' in data
        assert 'index' in data

    def test_search_index_file_count(self, project_root):
        """Verify search index has correct file count"""
        search_index = project_root / 'docs' / '.search_index.json'

        with open(search_index) as f:
            data = json.load(f)

        indexed_files = data.get('indexed_files', 0)

        # Should match actual file count (269)
        assert indexed_files == 269, \
            f"Search index shows {indexed_files} files, expected 269"
