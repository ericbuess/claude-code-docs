"""Unit tests for update_sitemap.py functions."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from update_sitemap import (
    load_paths_manifest,
    load_docs_manifest,
    build_path_tree,
    count_tree_leaves,
    tree_to_list,
    path_to_filename,
    save_json
)


class TestLoadPathsManifestSitemap:
    """Test paths manifest loading in update_sitemap."""

    def test_load_paths_manifest_success(self, tmp_path):
        """Test successful manifest loading."""
        manifest_data = {
            "metadata": {"total_paths": 10},
            "categories": {"guides": ["path1"]}
        }

        manifest_file = tmp_path / "paths.json"
        manifest_file.write_text(json.dumps(manifest_data))

        result = load_paths_manifest(manifest_file)

        assert result["metadata"]["total_paths"] == 10

    def test_load_paths_manifest_missing(self, tmp_path):
        """Test error for missing manifest."""
        manifest_file = tmp_path / "missing.json"

        with pytest.raises(FileNotFoundError):
            load_paths_manifest(manifest_file)


class TestLoadDocsManifestSitemap:
    """Test docs manifest loading in update_sitemap."""

    def test_load_docs_manifest_success(self, tmp_path):
        """Test successful docs manifest loading."""
        manifest_data = {
            "files": {
                "test.md": {"title": "Test"}
            }
        }

        manifest_file = tmp_path / "docs.json"
        manifest_file.write_text(json.dumps(manifest_data))

        result = load_docs_manifest(manifest_file)

        assert "test.md" in result

    def test_load_docs_manifest_missing(self, tmp_path):
        """Test returns empty dict for missing file."""
        manifest_file = tmp_path / "missing.json"

        result = load_docs_manifest(manifest_file)

        assert result == {}

    def test_load_docs_manifest_nested_files(self, tmp_path):
        """Test handles nested files key."""
        manifest_data = {
            "files": {
                "test.md": {"title": "Test"}
            },
            "other_key": "value"
        }

        manifest_file = tmp_path / "docs.json"
        manifest_file.write_text(json.dumps(manifest_data))

        result = load_docs_manifest(manifest_file)

        # Should extract files key
        assert "test.md" in result


class TestBuildPathTree:
    """Test path tree building."""

    def test_build_path_tree_single_path(self):
        """Test builds tree for single path."""
        paths = ["/en/docs/overview"]

        result = build_path_tree(paths)

        assert "en" in result
        assert "docs" in result["en"]
        assert "overview" in result["en"]["docs"]

    def test_build_path_tree_multiple_paths(self):
        """Test builds tree for multiple paths."""
        paths = [
            "/en/docs/overview",
            "/en/docs/setup",
            "/en/api/reference"
        ]

        result = build_path_tree(paths)

        assert "en" in result
        assert "docs" in result["en"]
        assert "api" in result["en"]
        assert "overview" in result["en"]["docs"]
        assert "setup" in result["en"]["docs"]

    def test_build_path_tree_nested_paths(self):
        """Test builds tree for nested paths."""
        paths = ["/en/docs/guides/getting-started"]

        result = build_path_tree(paths)

        assert "en" in result
        assert "docs" in result["en"]
        assert "guides" in result["en"]["docs"]
        assert "getting-started" in result["en"]["docs"]["guides"]

    def test_build_path_tree_empty(self):
        """Test handles empty path list."""
        paths = []

        result = build_path_tree(paths)

        assert result == {}

    def test_build_path_tree_overlapping(self):
        """Test handles overlapping paths."""
        paths = [
            "/en/docs",
            "/en/docs/overview"
        ]

        result = build_path_tree(paths)

        assert "en" in result
        assert "docs" in result["en"]


class TestCountTreeLeaves:
    """Test tree leaf counting."""

    def test_count_tree_leaves_single_leaf(self):
        """Test counts single leaf."""
        tree = {"en": {"docs": {"overview": {}}}}

        result = count_tree_leaves(tree)

        assert result == 1

    def test_count_tree_leaves_multiple_leaves(self):
        """Test counts multiple leaves."""
        tree = {
            "en": {
                "docs": {
                    "overview": {},
                    "setup": {}
                }
            }
        }

        result = count_tree_leaves(tree)

        assert result == 2

    def test_count_tree_leaves_nested(self):
        """Test counts nested leaves."""
        tree = {
            "en": {
                "docs": {
                    "guides": {
                        "start": {},
                        "advanced": {}
                    }
                }
            }
        }

        result = count_tree_leaves(tree)

        assert result == 2

    def test_count_tree_leaves_empty(self):
        """Test counts empty tree as one leaf."""
        tree = {}

        result = count_tree_leaves(tree)

        assert result == 1


class TestTreeToList:
    """Test tree to list conversion."""

    def test_tree_to_list_single_path(self):
        """Test converts single path."""
        tree = {"en": {"docs": {"overview": {}}}}

        result = tree_to_list(tree)

        assert len(result) == 1
        assert "/en/docs/overview" in result

    def test_tree_to_list_multiple_paths(self):
        """Test converts multiple paths."""
        tree = {
            "en": {
                "docs": {
                    "overview": {},
                    "setup": {}
                }
            }
        }

        result = tree_to_list(tree)

        assert len(result) == 2
        assert "/en/docs/overview" in result
        assert "/en/docs/setup" in result

    def test_tree_to_list_nested(self):
        """Test converts nested paths."""
        tree = {
            "en": {
                "docs": {
                    "guides": {
                        "start": {}
                    }
                }
            }
        }

        result = tree_to_list(tree)

        assert "/en/docs/guides/start" in result

    def test_tree_to_list_empty(self):
        """Test handles empty tree."""
        tree = {}

        result = tree_to_list(tree)

        assert result == []

    def test_tree_to_list_preserves_slashes(self):
        """Test preserves leading slashes."""
        tree = {"en": {"docs": {}}}

        result = tree_to_list(tree)

        assert all(path.startswith("/") for path in result if path)


class TestPathToFilenameSitemap:
    """Test path to filename conversion in update_sitemap."""

    def test_path_to_filename_basic(self):
        """Test basic conversion."""
        result = path_to_filename("/en/docs/overview")

        assert result == "docs__overview.md"

    def test_path_to_filename_removes_leading_slash(self):
        """Test removes leading slash."""
        result = path_to_filename("/en/docs/test")

        assert not result.startswith("/")

    def test_path_to_filename_replaces_slashes(self):
        """Test replaces slashes with double underscores."""
        result = path_to_filename("/en/docs/guides/start")

        assert "__" in result
        assert "/" not in result

    def test_path_to_filename_removes_en_prefix(self):
        """Test removes en prefix."""
        result = path_to_filename("/en/docs/test")

        assert not result.startswith("en__")

    def test_path_to_filename_adds_extension(self):
        """Test adds .md extension."""
        result = path_to_filename("/en/docs/test")

        assert result.endswith(".md")

    def test_path_to_filename_without_leading_slash(self):
        """Test handles path without leading slash."""
        result = path_to_filename("en/docs/test")

        assert result == "docs__test.md"


class TestSaveJson:
    """Test JSON saving."""

    def test_save_json_success(self, tmp_path):
        """Test successful JSON saving."""
        data = {"key": "value", "number": 42}
        file_path = tmp_path / "test.json"

        save_json(file_path, data)

        assert file_path.exists()
        saved = json.loads(file_path.read_text())
        assert saved["key"] == "value"
        assert saved["number"] == 42

    def test_save_json_creates_parent(self, tmp_path):
        """Test creates parent directory if needed."""
        file_path = tmp_path / "subdir" / "test.json"

        save_json(file_path, {})

        assert file_path.exists()

    def test_save_json_formatted(self, tmp_path):
        """Test saves formatted JSON."""
        data = {"key": "value"}
        file_path = tmp_path / "test.json"

        save_json(file_path, data)

        content = file_path.read_text()
        # Should be pretty-printed (have newlines)
        assert "\n" in content

    def test_save_json_unicode(self, tmp_path):
        """Test handles unicode content."""
        data = {"text": "中文 émojis 🔥"}
        file_path = tmp_path / "test.json"

        save_json(file_path, data)

        saved = json.loads(file_path.read_text())
        assert saved["text"] == "中文 émojis 🔥"

    def test_save_json_overwrites(self, tmp_path):
        """Test overwrites existing file."""
        file_path = tmp_path / "test.json"
        file_path.write_text('{"old": "data"}')

        save_json(file_path, {"new": "data"})

        saved = json.loads(file_path.read_text())
        assert "new" in saved
        assert "old" not in saved
