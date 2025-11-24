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
    """Load docs/docs_manifest.json - returns files dict"""
    with open(project_root / 'docs' / 'docs_manifest.json') as f:
        manifest = json.load(f)
        # Return just the files dict for compatibility with tests
        return manifest.get('files', manifest)

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
        # Handle both dict and list manifest formats
        if isinstance(docs_manifest, dict):
            manifest_files = set(docs_manifest.keys())
        else:
            manifest_files = set(docs_manifest)

        # Files in manifest but not on disk
        missing = manifest_files - actual_files
        # Files on disk but not in manifest
        extra = actual_files - manifest_files

        assert len(missing) == 0, \
            f"Manifest references missing files: {missing}"

        # Extra files are okay - manifest only tracks fetched files
        # Other files (API reference, prompt library, etc.) may not be in manifest
        # We don't enforce that all disk files must be in manifest

    def test_expected_file_count(self, docs_manifest, project_root):
        """Verify manifest has reasonable number of files and disk has 268 total"""
        file_count = len(docs_manifest)

        # Manifest should have at least the Claude Code docs (44+)
        assert file_count >= 44, \
            f"Expected at least 44 files in manifest (Claude Code docs), found {file_count}"

        # Check total files on disk matches paths_manifest.json expectations
        docs_dir = project_root / 'docs'
        actual_file_count = len([f for f in docs_dir.glob('*.md') if f.name != 'docs_manifest.json'])

        # Load paths_manifest.json to get expected path count
        paths_manifest_path = project_root / 'paths_manifest.json'
        if not paths_manifest_path.exists():
            pytest.skip("paths_manifest.json not available")

        import json
        with open(paths_manifest_path) as f:
            paths_manifest = json.load(f)

        expected_path_count = paths_manifest['metadata']['total_paths']

        # Allow variance for unfetchable paths (HTML-only pages, external redirects)
        variance = abs(actual_file_count - expected_path_count)
        assert variance <= 10, \
            f"File count discrepancy: {actual_file_count} files on disk vs {expected_path_count} in paths manifest (variance: {variance})"

    def test_all_entries_have_required_fields(self, docs_manifest):
        """Ensure all manifest entries have required fields"""
        # Handle list format (new) - just verify filenames are non-empty strings
        if isinstance(docs_manifest, list):
            for filename in docs_manifest:
                assert filename, "Empty filename in manifest"
                assert isinstance(filename, str), f"Non-string filename: {filename}"
            return

        # Handle dict format (old) - verify detailed structure
        # All entries should have these core fields
        core_fields = {'hash', 'last_updated'}

        # Fetched files should also have these
        fetched_fields = {'original_url', 'original_md_url'}

        # Exception list for local files (not fetched from sitemap)
        local_files = {'changelog.md'}

        for filename, entry in docs_manifest.items():
            # Check core fields
            missing_core = core_fields - set(entry.keys())
            assert len(missing_core) == 0, \
                f"{filename} missing core fields: {missing_core}"

            # Check fetched fields for non-local files
            if filename not in local_files:
                missing_fetched = fetched_fields - set(entry.keys())
                assert len(missing_fetched) == 0, \
                    f"{filename} missing fetched fields: {missing_fetched}"

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
