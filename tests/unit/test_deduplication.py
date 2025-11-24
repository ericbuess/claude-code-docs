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
        """Ensure no unexpected duplicate content exists"""
        # Known duplicates: Anthropic publishes same content at multiple URLs (by design)
        # Tuples are sorted alphabetically to match the logic below
        EXPECTED_DUPLICATES = {
            ('en__api__overview.md', 'en__docs__build-with-claude__overview.md'),
            ('en__api__migrating-from-text-completions-to-messages.md',
             'en__docs__build-with-claude__working-with-messages.md')
        }

        hashes = {}
        duplicates = []

        for f in docs_files:
            if f.name == 'docs_manifest.json':
                continue

            file_hash = calculate_md5(f)

            if file_hash in hashes:
                dup_pair = tuple(sorted([f.name, hashes[file_hash]]))
                if dup_pair not in EXPECTED_DUPLICATES:
                    duplicates.append(dup_pair)
            else:
                hashes[file_hash] = f.name

        assert len(duplicates) == 0, \
            f"Found {len(duplicates)} unexpected duplicate files: {duplicates}"

    def test_expected_file_count(self, docs_files, docs_dir):
        """Verify file count matches manifest expectations"""
        # Load paths_manifest.json to get expected count
        manifest_path = docs_dir.parent / 'paths_manifest.json'
        if not manifest_path.exists():
            pytest.skip("paths_manifest.json not available")

        with open(manifest_path) as f:
            manifest = json.load(f)

        expected_path_count = manifest['metadata']['total_paths']

        # Exclude non-documentation files
        md_files = [f for f in docs_files if f.name != 'docs_manifest.json']

        # We expect close to manifest count, accounting for:
        # - Known unfetchable redirects (like /en/docs/mcp → external site)
        # - Possible legacy/extra files (changelog.md, etc.)
        actual_count = len(md_files)

        # Allow some variance but flag significant discrepancies
        variance = abs(actual_count - expected_path_count)
        assert variance <= 10, \
            f"File count discrepancy: {actual_count} files on disk vs {expected_path_count} in manifest (variance: {variance})"

class TestNamingConvention:
    """Verify file naming standards"""

    def test_all_docs_use_en_prefix(self, docs_files):
        """Ensure all documentation files follow en__ or docs__en__ naming convention"""
        non_standard = []

        # Allowed exceptions (project-specific files)
        allowed_exceptions = {
            'docs_manifest.json',
            'changelog.md',
            'SEARCH_GUIDE.md'
        }

        for f in docs_files:
            if f.name not in allowed_exceptions:
                # Accept both en__* (old format) and docs__en__* (new Claude Code format)
                if not (f.name.startswith('en__') or f.name.startswith('docs__en__')):
                    non_standard.append(f.name)

        assert len(non_standard) == 0, \
            f"Files not following en__ or docs__en__ convention: {non_standard}"

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

        # Should exist:
        assert (docs_dir / 'docs__en__mcp.md').exists(), \
            "Claude Code MCP guide should exist (NEW FORMAT: docs__en__)"

        # Note: en__docs__mcp.md (/en/docs/mcp) redirects to external modelcontextprotocol.io
        # and cannot be fetched as Claude documentation

    def test_overview_namespace_resolved(self, docs_dir):
        """Verify overview.md namespace collision resolved"""
        # Should not exist:
        assert not (docs_dir / 'overview.md').exists(), \
            "Legacy overview.md should be removed"

        # Should exist (different topics):
        assert (docs_dir / 'docs__en__overview.md').exists(), \
            "Claude Code overview should exist (NEW FORMAT: docs__en__)"
        assert (docs_dir / 'en__api__overview.md').exists(), \
            "API overview should exist"

class TestCriticalFiles:
    """Verify critical enhanced files exist"""

    @pytest.mark.parametrize("filename", [
        # Claude Code docs (NEW FORMAT from code.claude.com: docs__en__)
        "docs__en__cli-reference.md",
        "docs__en__hooks.md",
        "docs__en__output-styles.md",
        "docs__en__settings.md",
        "docs__en__sub-agents.md",
        "docs__en__mcp.md",
        "docs__en__overview.md",
        # General docs (from docs.claude.com)
        # Note: en__docs__mcp.md excluded (redirects to external site)
        "en__api__overview.md",
    ])
    def test_critical_file_exists(self, docs_dir, filename):
        """Verify critical enhanced files were kept"""
        assert (docs_dir / filename).exists(), \
            f"Critical file missing: {filename}"
