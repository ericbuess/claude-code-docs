"""Tests for file deduplication validation

Verifies that Phase 1 deduplication was successful:
- No duplicate content (MD5 hashes)
- Consistent naming conventions
- Namespace collisions resolved
"""
import pytest
from pathlib import Path
import hashlib
import json

@pytest.fixture
def docs_dir():
    """Path to docs directory"""
    return Path(__file__).parent.parent.parent / 'docs'

@pytest.fixture
def docs_files(docs_dir):
    """List of all markdown files in docs/"""
    return list(docs_dir.glob('*.md'))

def calculate_md5(filepath):
    """Calculate MD5 hash of file"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

class TestNoDuplicateContent:
    """Verify no duplicate file content exists"""

    def test_no_duplicate_md5_hashes(self, docs_files):
        """Ensure no two files have identical content"""
        hashes = {}
        duplicates = []

        for f in docs_files:
            if f.name == 'docs_manifest.json':
                continue

            file_hash = calculate_md5(f)

            if file_hash in hashes:
                duplicates.append((f.name, hashes[file_hash]))
            else:
                hashes[file_hash] = f.name

        assert len(duplicates) == 0, f"Found {len(duplicates)} duplicate files: {duplicates}"

    def test_expected_file_count(self, docs_files):
        """Verify expected number of files after dedup"""
        # Exclude docs_manifest.json
        md_files = [f for f in docs_files if f.name != 'docs_manifest.json']

        # Expected: 270 files (314 - 44 duplicates)
        assert len(md_files) == 270, f"Expected 270 files, found {len(md_files)}"

class TestNamingConvention:
    """Verify file naming standards"""

    def test_all_docs_use_en_prefix(self, docs_files):
        """Ensure all documentation files follow en__ naming convention"""
        non_standard = []

        # Allowed exceptions (project-specific files)
        allowed_exceptions = {
            'docs_manifest.json',
            'changelog.md',
            'SEARCH_GUIDE.md'
        }

        for f in docs_files:
            if f.name not in allowed_exceptions and not f.name.startswith('en__'):
                non_standard.append(f.name)

        assert len(non_standard) == 0, \
            f"Files not following en__ convention: {non_standard}"

    def test_no_legacy_duplicates(self, docs_dir):
        """Ensure legacy format files don't coexist with en__ versions"""
        # These legacy files should not exist
        removed_legacy = [
            'hooks.md', 'mcp.md', 'overview.md',
            'cli-reference.md', 'settings.md', 'sub-agents.md',
            'output-styles.md', 'checkpointing.md', 'hooks-guide.md'
        ]

        found_legacy = []
        for legacy_file in removed_legacy:
            if (docs_dir / legacy_file).exists():
                found_legacy.append(legacy_file)

        assert len(found_legacy) == 0, \
            f"Found removed legacy files still present: {found_legacy}"

    def test_filename_matches_path_convention(self, docs_files):
        """Verify filenames can be converted to valid paths"""
        import sys
        sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

        try:
            from main import path_to_filename
        except ImportError:
            pytest.skip("main.py not available")

        for f in docs_files:
            if not f.name.startswith('en__'):
                continue

            # Convert filename to path
            path = '/' + f.name.replace('__', '/').replace('.md', '')

            # Convert back to filename
            regenerated = path_to_filename(path)

            assert regenerated == f.name, \
                f"Path conversion mismatch: {f.name} != {regenerated}"

class TestNamespaceCollisions:
    """Verify namespace collisions were resolved"""

    def test_mcp_namespace_resolved(self, docs_dir):
        """Verify mcp.md namespace collision resolved"""
        # Should not exist:
        assert not (docs_dir / 'mcp.md').exists(), \
            "Legacy mcp.md should be removed"

        # Should exist (different topics):
        assert (docs_dir / 'en__docs__claude-code__mcp.md').exists(), \
            "Claude Code MCP guide should exist"
        assert (docs_dir / 'en__docs__mcp.md').exists(), \
            "General MCP overview should exist"

    def test_overview_namespace_resolved(self, docs_dir):
        """Verify overview.md namespace collision resolved"""
        # Should not exist:
        assert not (docs_dir / 'overview.md').exists(), \
            "Legacy overview.md should be removed"

        # Should exist (different topics):
        assert (docs_dir / 'en__docs__claude-code__overview.md').exists(), \
            "Claude Code overview should exist"
        assert (docs_dir / 'en__api__overview.md').exists(), \
            "API overview should exist"

class TestCriticalFiles:
    """Verify critical enhanced files exist"""

    @pytest.mark.parametrize("filename", [
        "en__docs__claude-code__cli-reference.md",
        "en__docs__claude-code__hooks.md",
        "en__docs__claude-code__output-styles.md",
        "en__docs__claude-code__settings.md",
        "en__docs__claude-code__sub-agents.md",
        "en__docs__claude-code__mcp.md",
        "en__docs__mcp.md",
        "en__docs__claude-code__overview.md",
        "en__api__overview.md",
    ])
    def test_critical_file_exists(self, docs_dir, filename):
        """Verify critical enhanced files were kept"""
        assert (docs_dir / filename).exists(), \
            f"Critical file missing: {filename}"
