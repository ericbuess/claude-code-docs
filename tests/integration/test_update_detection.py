"""Integration tests for change detection."""

import pytest
import sys
from pathlib import Path
import json
import time

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import (
    compute_content_hash,
    save_documentation,
    content_has_changed
)


class TestContentChangeDetection:
    """Test content change detection mechanisms."""

    @pytest.mark.integration
    def test_detect_content_changes_via_hash(self, tmp_path):
        """Test SHA256 hash detects content changes."""
        content1 = "# Original Title\n\nOriginal content here."
        content2 = "# Updated Title\n\nUpdated content here."
        content3 = "# Original Title\n\nOriginal content here."  # Same as content1

        hash1 = compute_content_hash(content1)
        hash2 = compute_content_hash(content2)
        hash3 = compute_content_hash(content3)

        # Different content = different hash
        assert hash1 != hash2

        # Same content = same hash
        assert hash1 == hash3

    @pytest.mark.integration
    def test_whitespace_changes_detected(self):
        """Test that whitespace changes are detected."""
        content1 = "# Title\n\nContent"
        content2 = "# Title\n\n\nContent"  # Extra newline

        hash1 = compute_content_hash(content1)
        hash2 = compute_content_hash(content2)

        # Even whitespace changes should be detected
        assert hash1 != hash2

    @pytest.mark.integration
    def test_minor_changes_detected(self):
        """Test that even minor changes are detected."""
        content1 = "The quick brown fox"
        content2 = "The quick brown fox."  # Added period

        hash1 = compute_content_hash(content1)
        hash2 = compute_content_hash(content2)

        assert hash1 != hash2


class TestSkipUnchanged:
    """Test skipping unchanged documentation."""

    @pytest.mark.integration
    def test_unchanged_docs_identified(self, tmp_path):
        """Test unchanged docs are correctly identified."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        path = "/en/docs/test"
        content = "# Test\n\nTest content"

        # Save initial version
        save_documentation(path, content, output_dir)

        # Compute hash of original content
        from main import compute_content_hash
        old_hash = compute_content_hash(content)

        # Check if update needed with same content
        update_needed = content_has_changed(content, old_hash)

        # Should not need update
        assert update_needed is False

    @pytest.mark.integration
    def test_changed_docs_identified(self, tmp_path):
        """Test changed docs are correctly identified."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        path = "/en/docs/test"

        # Save initial version
        original_content = "Original content"
        save_documentation(path, original_content, output_dir)

        # Compute hash of original content
        from main import compute_content_hash
        old_hash = compute_content_hash(original_content)

        # Check if update needed with different content
        new_content = "Updated content"
        update_needed = content_has_changed(new_content, old_hash)

        # Should need update
        assert update_needed is True

    @pytest.mark.integration
    def test_new_docs_need_update(self, tmp_path):
        """Test new docs are identified as needing update."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        path = "/en/docs/new-file"
        content = "New content"

        # File doesn't exist yet - no old hash
        update_needed = content_has_changed(content, None)

        # Should need update (new file)
        assert update_needed is True


class TestChangelogGeneration:
    """Test changelog/change tracking."""

    @pytest.mark.integration
    def test_track_changes_over_time(self, tmp_path):
        """Test tracking changes across multiple updates."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        path = "/en/docs/test"
        versions = [
            "# Version 1\n\nInitial content",
            "# Version 2\n\nUpdated content",
            "# Version 3\n\nFinal content"
        ]

        hashes = []

        for version in versions:
            save_documentation(path, version, output_dir)
            hash_value = compute_content_hash(version)
            hashes.append(hash_value)

        # All versions should have different hashes
        assert len(set(hashes)) == len(hashes)

        # Final version should be saved
        saved_file = output_dir / "en__docs__test.md"
        assert saved_file.read_text() == versions[-1]

    @pytest.mark.integration
    def test_no_change_no_update(self, tmp_path):
        """Test that saving same content doesn't trigger update."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        path = "/en/docs/test"
        content = "# Unchanged\n\nStatic content"

        # Save multiple times with same content
        for i in range(3):
            save_documentation(path, content, output_dir)

        # File should exist with correct content
        saved_file = output_dir / "en__docs__test.md"
        assert saved_file.exists()
        assert saved_file.read_text() == content


class TestBatchUpdateDetection:
    """Test batch update detection for multiple files."""

    @pytest.mark.integration
    def test_identify_changed_subset(self, tmp_path):
        """Test identifying which files changed in a batch."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        # Setup: save initial versions
        from main import compute_content_hash
        initial_docs = {
            "/en/docs/doc1": "Content 1",
            "/en/docs/doc2": "Content 2",
            "/en/docs/doc3": "Content 3"
        }

        # Store initial hashes
        initial_hashes = {}
        for path, content in initial_docs.items():
            save_documentation(path, content, output_dir)
            initial_hashes[path] = compute_content_hash(content)

        # New versions: doc2 changed, others unchanged
        new_docs = {
            "/en/docs/doc1": "Content 1",  # Unchanged
            "/en/docs/doc2": "Updated Content 2",  # Changed
            "/en/docs/doc3": "Content 3"  # Unchanged
        }

        # Check which need updates
        updates_needed = {}
        for path, content in new_docs.items():
            updates_needed[path] = content_has_changed(content, initial_hashes[path])

        # Only doc2 should need update
        assert updates_needed["/en/docs/doc1"] is False
        assert updates_needed["/en/docs/doc2"] is True
        assert updates_needed["/en/docs/doc3"] is False

    @pytest.mark.integration
    def test_all_unchanged_skip_all(self, tmp_path):
        """Test all unchanged docs are skipped."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        from main import compute_content_hash
        docs = {
            "/en/docs/doc1": "Content 1",
            "/en/docs/doc2": "Content 2"
        }

        # Save initial and compute hashes
        hashes = {}
        for path, content in docs.items():
            save_documentation(path, content, output_dir)
            hashes[path] = compute_content_hash(content)

        # Check same content
        all_unchanged = all(
            not content_has_changed(content, hashes[path])
            for path, content in docs.items()
        )

        assert all_unchanged is True

    @pytest.mark.integration
    def test_all_changed_update_all(self, tmp_path):
        """Test all changed docs are updated."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        # Save initial versions
        from main import compute_content_hash
        initial = {
            "/en/docs/doc1": "Old 1",
            "/en/docs/doc2": "Old 2"
        }

        initial_hashes = {}
        for path, content in initial.items():
            save_documentation(path, content, output_dir)
            initial_hashes[path] = compute_content_hash(content)

        # New versions (all changed)
        updated = {
            "/en/docs/doc1": "New 1",
            "/en/docs/doc2": "New 2"
        }

        # Check all need updates
        all_changed = all(
            content_has_changed(content, initial_hashes[path])
            for path, content in updated.items()
        )

        assert all_changed is True
