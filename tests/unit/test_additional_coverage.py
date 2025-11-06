"""Additional unit tests to increase coverage to 70%+."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from datetime import datetime

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import (
    compute_content_hash,
    content_has_changed,
    path_to_filename,
    FetchStats
)

from lookup_paths import (
    get_all_paths,
    ValidationStats
)

from update_sitemap import (
    build_path_tree,
    count_tree_leaves,
    tree_to_list,
    path_to_filename as sitemap_path_to_filename
)


# ============================================================================
# Additional main.py tests
# ============================================================================

class TestComputeContentHashExtended:
    """Extended tests for compute_content_hash."""

    def test_hash_long_content(self):
        """Test hash with very long content."""
        content = "x" * 100000
        result = compute_content_hash(content)
        assert len(result) == 64

    def test_hash_special_characters(self):
        """Test hash with special characters."""
        content = "!@#$%^&*()_+-={}[]|\\:\";<>?,./\n\t"
        result = compute_content_hash(content)
        assert len(result) == 64

    def test_hash_multiline(self):
        """Test hash with multiline content."""
        content = "line1\nline2\nline3"
        result = compute_content_hash(content)
        assert len(result) == 64

    def test_hash_unicode_symbols(self):
        """Test hash with unicode symbols."""
        content = "♠♣♥♦→←↑↓"
        result = compute_content_hash(content)
        assert len(result) == 64


class TestContentHashChangedExtended:
    """Extended tests for content_has_changed."""

    def test_whitespace_change_detected(self):
        """Test detects whitespace changes."""
        old_hash = compute_content_hash("content")
        new_content = "content "  # Added space
        assert content_has_changed(new_content, old_hash) is True

    def test_case_change_detected(self):
        """Test detects case changes."""
        old_hash = compute_content_hash("Content")
        new_content = "content"
        assert content_has_changed(new_content, old_hash) is True

    def test_empty_to_content(self):
        """Test change from empty to content."""
        old_hash = compute_content_hash("")
        new_content = "new content"
        assert content_has_changed(new_content, old_hash) is True


class TestPathToFilenameExtended:
    """Extended tests for path_to_filename."""

    def test_path_with_hyphens(self):
        """Test path with hyphens."""
        result = path_to_filename("/en/docs/getting-started")
        assert "getting-started" in result

    def test_path_with_numbers(self):
        """Test path with numbers."""
        result = path_to_filename("/en/docs/v2/guide")
        assert "v2" in result

    def test_deeply_nested_path(self):
        """Test deeply nested path."""
        result = path_to_filename("/en/docs/a/b/c/d/e")
        assert result.count("__") >= 5

    def test_path_already_has_md(self):
        """Test path that already ends with .md."""
        result = path_to_filename("/en/docs/test.md")
        assert result.count(".md") == 1


class TestFetchStatsExtended:
    """Extended tests for FetchStats."""

    def test_multiple_successes(self):
        """Test tracking multiple successes."""
        stats = FetchStats()
        for i in range(10):
            stats.add_success(f"/path{i}")

        assert stats.success_count == 10

    def test_multiple_errors(self):
        """Test tracking multiple errors."""
        stats = FetchStats()
        for i in range(5):
            stats.add_error(f"/path{i}", f"error{i}")

        assert stats.failed_count == 5
        assert len(stats.errors) == 5

    def test_mixed_operations(self):
        """Test tracking mixed operations."""
        stats = FetchStats()
        stats.add_success("/p1", updated=True)
        stats.add_success("/p2", updated=False)
        stats.add_skip("/p3")
        stats.add_error("/p4", "error")

        summary = stats.get_summary()
        assert summary["success"] == 2
        assert summary["updated"] == 1
        assert summary["skipped"] == 1
        assert summary["failed"] == 1
        assert summary["total_processed"] == 3

    def test_elapsed_time(self):
        """Test elapsed time tracking."""
        stats = FetchStats()
        import time
        time.sleep(0.1)
        summary = stats.get_summary()

        assert summary["elapsed_seconds"] > 0


# ============================================================================
# Additional lookup_paths.py tests
# ============================================================================

class TestGetAllPathsExtended:
    """Extended tests for get_all_paths."""

    def test_multiple_categories(self):
        """Test with multiple categories."""
        manifest = {
            "categories": {
                "guides": ["/p1", "/p2"],
                "api": ["/p3", "/p4"],
                "reference": ["/p5"]
            }
        }

        result = get_all_paths(manifest)
        assert len(result) == 5

    def test_empty_category(self):
        """Test with empty category."""
        manifest = {
            "categories": {
                "guides": [],
                "api": ["/p1"]
            }
        }

        result = get_all_paths(manifest)
        assert len(result) == 1

    def test_single_category(self):
        """Test with single category."""
        manifest = {
            "categories": {
                "only": ["/p1", "/p2", "/p3"]
            }
        }

        result = get_all_paths(manifest)
        assert len(result) == 3


class TestValidationStatsExtended:
    """Extended tests for ValidationStats."""

    def test_reachability_percent_zero(self):
        """Test reachability percent with no results."""
        stats = ValidationStats()
        summary = stats.get_summary()
        assert summary["reachability_percent"] == 0

    def test_reachability_percent_full(self):
        """Test 100% reachability."""
        stats = ValidationStats()
        for i in range(10):
            stats.add_result(f"/p{i}", "reachable", 200)

        summary = stats.get_summary()
        assert summary["reachability_percent"] == 100.0

    def test_reachability_percent_partial(self):
        """Test partial reachability."""
        stats = ValidationStats()
        stats.add_result("/p1", "reachable", 200)
        stats.add_result("/p2", "not_found", 404)

        summary = stats.get_summary()
        assert summary["reachability_percent"] == 50.0

    def test_broken_paths_list(self):
        """Test broken paths are tracked."""
        stats = ValidationStats()
        stats.add_result("/broken1", "not_found", 404)
        stats.add_result("/broken2", "timeout")
        stats.add_result("/broken3", "error", 500)

        assert len(stats.broken_paths) == 3
        assert any(p["path"] == "/broken1" for p in stats.broken_paths)


# ============================================================================
# Additional update_sitemap.py tests
# ============================================================================

class TestBuildPathTreeExtended:
    """Extended tests for build_path_tree."""

    def test_complex_tree(self):
        """Test with complex nested structure."""
        paths = [
            "/en/docs/guides/getting-started",
            "/en/docs/guides/advanced",
            "/en/docs/api/reference",
            "/en/docs/api/examples"
        ]

        tree = build_path_tree(paths)
        assert "en" in tree
        assert "docs" in tree["en"]
        assert "guides" in tree["en"]["docs"]
        assert "api" in tree["en"]["docs"]

    def test_single_level(self):
        """Test with single level paths."""
        paths = ["/en"]
        tree = build_path_tree(paths)
        assert "en" in tree

    def test_many_paths(self):
        """Test with many paths."""
        paths = [f"/en/docs/path{i}" for i in range(100)]
        tree = build_path_tree(paths)
        assert len(tree["en"]["docs"]) == 100


class TestCountTreeLeavesExtended:
    """Extended tests for count_tree_leaves."""

    def test_deep_nested(self):
        """Test with deeply nested tree."""
        tree = {"a": {"b": {"c": {"d": {}}}}}
        assert count_tree_leaves(tree) == 1

    def test_wide_tree(self):
        """Test with wide tree."""
        tree = {
            "a": {},
            "b": {},
            "c": {},
            "d": {},
            "e": {}
        }
        assert count_tree_leaves(tree) == 5

    def test_mixed_depth(self):
        """Test with mixed depth tree."""
        tree = {
            "shallow": {},
            "deep": {
                "level2": {
                    "level3": {}
                }
            }
        }
        assert count_tree_leaves(tree) == 2


class TestTreeToListExtended:
    """Extended tests for tree_to_list."""

    def test_reconstructs_original(self):
        """Test can reconstruct original paths."""
        original = ["/en/docs/test", "/en/docs/example"]
        tree = build_path_tree(original)
        result = tree_to_list(tree)

        assert set(result) == set(original)

    def test_single_node(self):
        """Test with single node."""
        tree = {"en": {}}
        result = tree_to_list(tree)
        assert "/en" in result

    def test_many_nodes(self):
        """Test with many nodes."""
        tree = {f"node{i}": {} for i in range(50)}
        result = tree_to_list(tree)
        assert len(result) == 50


class TestSitemapPathToFilename:
    """Test path_to_filename in update_sitemap."""

    def test_removes_en_prefix(self):
        """Test removes en prefix in sitemap version."""
        result = sitemap_path_to_filename("/en/docs/test")
        # Sitemap version removes en__ prefix
        assert not result.startswith("en__")

    def test_preserves_structure(self):
        """Test preserves path structure."""
        result = sitemap_path_to_filename("/en/docs/guide/advanced")
        assert "__" in result

    def test_adds_extension(self):
        """Test adds .md extension."""
        result = sitemap_path_to_filename("/en/docs/test")
        assert result.endswith(".md")
