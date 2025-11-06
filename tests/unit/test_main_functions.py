"""Unit tests for main.py functions."""

import pytest
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import hashlib

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import (
    load_paths_manifest,
    load_docs_manifest,
    save_docs_manifest,
    compute_content_hash,
    content_has_changed,
    validate_markdown_content,
    path_to_filename,
    get_category_paths,
    get_all_paths,
    FetchStats
)


class TestLoadPathsManifest:
    """Test paths manifest loading."""

    def test_load_paths_manifest_success(self, tmp_path):
        """Test successful manifest loading."""
        manifest_data = {
            "metadata": {
                "total_paths": 10,
                "categories_count": 3
            },
            "categories": {
                "guides": ["path1", "path2"]
            }
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        result = load_paths_manifest(manifest_file)

        assert result["metadata"]["total_paths"] == 10
        assert result["metadata"]["categories_count"] == 3
        assert "guides" in result["categories"]

    def test_load_paths_manifest_missing_file(self, tmp_path):
        """Test error when manifest file doesn't exist."""
        manifest_file = tmp_path / "nonexistent.json"

        with pytest.raises(FileNotFoundError):
            load_paths_manifest(manifest_file)

    def test_load_paths_manifest_invalid_json(self, tmp_path):
        """Test error when manifest has invalid JSON."""
        manifest_file = tmp_path / "invalid.json"
        manifest_file.write_text("{ invalid json }")

        with pytest.raises(json.JSONDecodeError):
            load_paths_manifest(manifest_file)


class TestLoadDocsManifest:
    """Test docs manifest loading."""

    def test_load_docs_manifest_success(self, tmp_path):
        """Test successful docs manifest loading."""
        manifest_data = {
            "/en/docs/test": {
                "hash": "abc123",
                "last_updated": "2024-01-01"
            }
        }

        manifest_file = tmp_path / "docs_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        result = load_docs_manifest(manifest_file)

        assert "/en/docs/test" in result
        assert result["/en/docs/test"]["hash"] == "abc123"

    def test_load_docs_manifest_missing_file(self, tmp_path):
        """Test returns empty dict when file doesn't exist."""
        manifest_file = tmp_path / "nonexistent.json"

        result = load_docs_manifest(manifest_file)

        assert result == {}

    def test_load_docs_manifest_invalid_json(self, tmp_path):
        """Test returns empty dict for invalid JSON."""
        manifest_file = tmp_path / "invalid.json"
        manifest_file.write_text("{ invalid json }")

        result = load_docs_manifest(manifest_file)

        assert result == {}


class TestSaveDocsManifest:
    """Test docs manifest saving."""

    def test_save_docs_manifest_success(self, tmp_path):
        """Test successful manifest saving."""
        manifest_data = {
            "/en/docs/test": {
                "hash": "abc123",
                "last_updated": "2024-01-01"
            }
        }

        manifest_file = tmp_path / "docs_manifest.json"

        save_docs_manifest(manifest_file, manifest_data)

        assert manifest_file.exists()
        saved = json.loads(manifest_file.read_text())
        assert "/en/docs/test" in saved

    def test_save_docs_manifest_creates_file(self, tmp_path):
        """Test creates file if it doesn't exist."""
        manifest_file = tmp_path / "new_manifest.json"

        save_docs_manifest(manifest_file, {})

        assert manifest_file.exists()


class TestComputeContentHash:
    """Test content hash computation."""

    def test_compute_content_hash_basic(self):
        """Test basic hash computation."""
        content = "test content"
        result = compute_content_hash(content)

        # Should be valid SHA256 hash
        assert len(result) == 64
        assert all(c in '0123456789abcdef' for c in result)

    def test_compute_content_hash_consistent(self):
        """Test hash is consistent for same content."""
        content = "test content"
        hash1 = compute_content_hash(content)
        hash2 = compute_content_hash(content)

        assert hash1 == hash2

    def test_compute_content_hash_different(self):
        """Test different content produces different hash."""
        hash1 = compute_content_hash("content1")
        hash2 = compute_content_hash("content2")

        assert hash1 != hash2

    def test_compute_content_hash_empty(self):
        """Test hash for empty content."""
        result = compute_content_hash("")

        assert len(result) == 64

    def test_compute_content_hash_unicode(self):
        """Test hash with unicode content."""
        content = "test 中文 émojis 🔥"
        result = compute_content_hash(content)

        assert len(result) == 64


class TestContentHasChanged:
    """Test content change detection."""

    def test_content_has_changed_no_old_hash(self):
        """Test returns True when no old hash exists."""
        result = content_has_changed("new content", None)

        assert result is True

    def test_content_has_changed_same_content(self):
        """Test returns False for identical content."""
        content = "test content"
        old_hash = compute_content_hash(content)

        result = content_has_changed(content, old_hash)

        assert result is False

    def test_content_has_changed_different_content(self):
        """Test returns True for different content."""
        old_hash = compute_content_hash("old content")

        result = content_has_changed("new content", old_hash)

        assert result is True


class TestValidateMarkdownContent:
    """Test markdown content validation."""

    def test_validate_markdown_valid(self):
        """Test validates correct markdown."""
        content = "# Title\n## Subtitle\nContent with **bold** and [links](url) and `code`\n- List item"

        result = validate_markdown_content(content, "test.md")

        assert result is True

    def test_validate_markdown_rejects_html(self):
        """Test rejects HTML content."""
        content = "<!DOCTYPE html><html><body>test</body></html>"

        result = validate_markdown_content(content, "test.md")

        assert result is False

    def test_validate_markdown_rejects_short(self):
        """Test rejects too-short content."""
        content = "short"

        result = validate_markdown_content(content, "test.md")

        assert result is False

    def test_validate_markdown_requires_indicators(self):
        """Test requires markdown indicators."""
        content = "Just plain text without any markdown formatting whatsoever " * 10

        result = validate_markdown_content(content, "test.md")

        assert result is False

    def test_validate_markdown_with_code_blocks(self):
        """Test validates markdown with code blocks."""
        content = "# Code\n```python\nprint('hello')\n```\nMore text with **formatting**"

        result = validate_markdown_content(content, "test.md")

        assert result is True


class TestPathToFilename:
    """Test path to filename conversion."""

    def test_path_to_filename_basic(self):
        """Test basic conversion."""
        result = path_to_filename("/en/docs/overview")

        assert result == "en__docs__overview.md"

    def test_path_to_filename_nested(self):
        """Test nested path conversion."""
        result = path_to_filename("/en/docs/claude-code/hooks")

        assert result == "en__docs__claude-code__hooks.md"

    def test_path_to_filename_removes_leading_slash(self):
        """Test removes leading slash."""
        result = path_to_filename("/en/docs/test")

        assert not result.startswith("/")

    def test_path_to_filename_no_leading_slash(self):
        """Test path without leading slash."""
        result = path_to_filename("en/docs/test")

        assert result == "en__docs__test.md"

    def test_path_to_filename_adds_md_extension(self):
        """Test adds .md extension."""
        result = path_to_filename("/en/docs/test")

        assert result.endswith(".md")


class TestGetCategoryPaths:
    """Test category path extraction."""

    def test_get_category_paths_existing_category(self):
        """Test get paths for existing category."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/guide1", "/en/docs/guide2"],
                "reference": ["/en/docs/ref1"]
            }
        }

        result = get_category_paths(manifest, "guides")

        assert len(result) == 2
        assert "/en/docs/guide1" in result

    def test_get_category_paths_nonexistent_category(self):
        """Test raises error for nonexistent category."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/guide1"]
            }
        }

        with pytest.raises(ValueError):
            get_category_paths(manifest, "nonexistent")

    def test_get_category_paths_empty_manifest(self):
        """Test raises error for empty manifest."""
        manifest = {}

        with pytest.raises(ValueError):
            get_category_paths(manifest, "guides")


class TestGetAllPaths:
    """Test get all paths from manifest."""

    def test_get_all_paths_from_categories(self):
        """Test gets all paths from categories."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/guide1", "/en/docs/guide2"],
                "reference": ["/en/docs/ref1"]
            }
        }

        result = get_all_paths(manifest)

        assert len(result) == 3
        assert "/en/docs/guide1" in result
        assert "/en/docs/ref1" in result

    def test_get_all_paths_includes_duplicates(self):
        """Test includes all paths (may have duplicates)."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/test1", "/en/docs/test2"],
                "reference": ["/en/docs/test3"]
            }
        }

        result = get_all_paths(manifest)

        # Should include all paths from all categories
        assert len(result) == 3

    def test_get_all_paths_empty_manifest(self):
        """Test handles empty manifest."""
        manifest = {}

        result = get_all_paths(manifest)

        assert result == []


class TestFetchStats:
    """Test FetchStats class."""

    def test_fetch_stats_init(self):
        """Test stats initialization."""
        stats = FetchStats()

        assert stats.success_count == 0
        assert stats.failed_count == 0
        assert stats.skipped_count == 0
        assert stats.updated_count == 0
        assert len(stats.errors) == 0

    def test_fetch_stats_add_success(self):
        """Test adding success."""
        stats = FetchStats()

        stats.add_success("/test/path")

        assert stats.success_count == 1
        assert stats.updated_count == 0

    def test_fetch_stats_add_success_updated(self):
        """Test adding updated success."""
        stats = FetchStats()

        stats.add_success("/test/path", updated=True)

        assert stats.success_count == 1
        assert stats.updated_count == 1

    def test_fetch_stats_add_skip(self):
        """Test adding skip."""
        stats = FetchStats()

        stats.add_skip("/test/path")

        assert stats.skipped_count == 1

    def test_fetch_stats_add_error(self):
        """Test adding error."""
        stats = FetchStats()

        stats.add_error("/test/path", "error message")

        assert stats.failed_count == 1
        assert len(stats.errors) == 1
        assert stats.errors[0]["path"] == "/test/path"

    def test_fetch_stats_get_summary(self):
        """Test getting summary."""
        stats = FetchStats()
        stats.add_success("/path1")
        stats.add_skip("/path2")
        stats.add_error("/path3", "error")

        summary = stats.get_summary()

        assert summary["success"] == 1
        assert summary["skipped"] == 1
        assert summary["failed"] == 1
        assert summary["total_processed"] == 2
        assert "elapsed_seconds" in summary
