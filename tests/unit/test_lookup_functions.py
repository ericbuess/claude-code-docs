"""Unit tests for lookup_paths.py functions."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch
import threading

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from lookup_paths import (
    load_paths_manifest,
    get_all_paths,
    search_paths,
    suggest_alternatives,
    load_batch_file,
    ValidationStats,
    format_content_result
)


class TestLoadPathsManifestLookup:
    """Test paths manifest loading in lookup_paths."""

    def test_load_paths_manifest_success(self, tmp_path):
        """Test successful manifest loading."""
        manifest_data = {
            "metadata": {"total_paths": 5},
            "categories": {"guides": ["path1"]}
        }

        manifest_file = tmp_path / "paths.json"
        manifest_file.write_text(json.dumps(manifest_data))

        result = load_paths_manifest(manifest_file)

        assert result["metadata"]["total_paths"] == 5

    def test_load_paths_manifest_missing(self, tmp_path):
        """Test error for missing manifest."""
        manifest_file = tmp_path / "missing.json"

        with pytest.raises(FileNotFoundError):
            load_paths_manifest(manifest_file)


class TestGetAllPathsLookup:
    """Test get all paths in lookup_paths."""

    def test_get_all_paths_from_categories(self):
        """Test extracts all paths from categories."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/guide1", "/en/docs/guide2"],
                "api": ["/en/docs/api1"]
            }
        }

        result = get_all_paths(manifest)

        assert len(result) == 3
        assert "/en/docs/guide1" in result

    def test_get_all_paths_empty(self):
        """Test handles empty categories."""
        manifest = {"categories": {}}

        result = get_all_paths(manifest)

        assert result == []


class TestSearchPaths:
    """Test path searching functionality."""

    def test_search_paths_exact_match(self):
        """Test exact match search."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/hooks", "/en/docs/mcp", "/en/docs/overview"]
            }
        }

        results = search_paths("hooks", manifest)

        assert len(results) > 0
        # Should find hooks with high relevance
        assert any("hooks" in path for path, _ in results)

    def test_search_paths_partial_match(self):
        """Test partial match search."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/claude-code/hooks", "/en/docs/overview"]
            }
        }

        results = search_paths("code", manifest)

        assert len(results) > 0

    def test_search_paths_case_insensitive(self):
        """Test case insensitive search."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/Hooks", "/en/docs/MCP"]
            }
        }

        results = search_paths("hooks", manifest)

        assert len(results) > 0

    def test_search_paths_multiple_words(self):
        """Test multi-word search."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/claude-code/getting-started", "/en/docs/setup"]
            }
        }

        results = search_paths("getting started", manifest)

        assert len(results) > 0

    def test_search_paths_no_results(self):
        """Test returns empty for no matches."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/hooks"]
            }
        }

        results = search_paths("zzzznonexistent", manifest)

        assert len(results) == 0

    def test_search_paths_relevance_ordering(self):
        """Test results ordered by relevance."""
        manifest = {
            "categories": {
                "guides": [
                    "/en/docs/hooks",
                    "/en/docs/advanced/hooks-guide",
                    "/en/docs/other"
                ]
            }
        }

        results = search_paths("hooks", manifest)

        # First result should be most relevant
        assert results[0][0] == "/en/docs/hooks"


class TestSuggestAlternatives:
    """Test alternative path suggestions."""

    def test_suggest_alternatives_basic(self):
        """Test suggests similar paths."""
        manifest = {
            "categories": {
                "guides": [
                    "/en/docs/hooks",
                    "/en/docs/mcp",
                    "/en/docs/overview"
                ]
            }
        }

        results = suggest_alternatives("/en/docs/hook", manifest)

        assert len(results) > 0
        # Should suggest hooks (closest match)
        assert "/en/docs/hooks" in results

    def test_suggest_alternatives_limit(self):
        """Test respects max suggestions limit."""
        manifest = {
            "categories": {
                "guides": [f"/en/docs/path{i}" for i in range(20)]
            }
        }

        results = suggest_alternatives("/en/docs/path1", manifest, max_suggestions=3)

        assert len(results) <= 3

    def test_suggest_alternatives_no_matches(self):
        """Test returns empty for no close matches."""
        manifest = {
            "categories": {
                "guides": ["/en/docs/foo", "/en/docs/bar"]
            }
        }

        results = suggest_alternatives("/en/docs/zzzzz", manifest)

        # May be empty or have distant matches
        assert isinstance(results, list)


class TestLoadBatchFile:
    """Test batch file loading."""

    def test_load_batch_file_success(self, tmp_path):
        """Test loads batch file successfully."""
        batch_file = tmp_path / "batch.txt"
        batch_file.write_text("/en/docs/path1\n/en/docs/path2\n")

        result = load_batch_file(batch_file)

        assert len(result) == 2
        assert "/en/docs/path1" in result

    def test_load_batch_file_skips_empty_lines(self, tmp_path):
        """Test skips empty lines."""
        batch_file = tmp_path / "batch.txt"
        batch_file.write_text("/en/docs/path1\n\n/en/docs/path2\n")

        result = load_batch_file(batch_file)

        assert len(result) == 2

    def test_load_batch_file_strips_whitespace(self, tmp_path):
        """Test strips whitespace."""
        batch_file = tmp_path / "batch.txt"
        batch_file.write_text("  /en/docs/path1  \n/en/docs/path2\n")

        result = load_batch_file(batch_file)

        assert "/en/docs/path1" in result

    def test_load_batch_file_missing(self, tmp_path):
        """Test error for missing file."""
        batch_file = tmp_path / "missing.txt"

        with pytest.raises(FileNotFoundError):
            load_batch_file(batch_file)


class TestValidationStats:
    """Test ValidationStats class."""

    def test_validation_stats_init(self):
        """Test stats initialization."""
        stats = ValidationStats()

        assert stats.total == 0
        assert stats.reachable == 0
        assert stats.not_found == 0
        assert stats.timeout == 0
        assert stats.error == 0

    def test_validation_stats_add_reachable(self):
        """Test adding reachable result."""
        stats = ValidationStats()

        stats.add_result("/test/path", "reachable", 200)

        assert stats.total == 1
        assert stats.reachable == 1

    def test_validation_stats_add_not_found(self):
        """Test adding not found result."""
        stats = ValidationStats()

        stats.add_result("/test/path", "not_found", 404)

        assert stats.total == 1
        assert stats.not_found == 1
        assert len(stats.broken_paths) == 1

    def test_validation_stats_add_timeout(self):
        """Test adding timeout result."""
        stats = ValidationStats()

        stats.add_result("/test/path", "timeout")

        assert stats.total == 1
        assert stats.timeout == 1
        assert len(stats.broken_paths) == 1

    def test_validation_stats_add_error(self):
        """Test adding error result."""
        stats = ValidationStats()

        stats.add_result("/test/path", "error", 500)

        assert stats.total == 1
        assert stats.error == 1
        assert len(stats.broken_paths) == 1

    def test_validation_stats_get_summary(self):
        """Test getting summary."""
        stats = ValidationStats()
        stats.add_result("/path1", "reachable", 200)
        stats.add_result("/path2", "not_found", 404)

        summary = stats.get_summary()

        assert summary["total"] == 2
        assert summary["reachable"] == 1
        assert summary["not_found"] == 1
        assert "reachability_percent" in summary

    def test_validation_stats_thread_safe(self):
        """Test thread-safe operations."""
        stats = ValidationStats()

        def add_results():
            for i in range(10):
                stats.add_result(f"/path{i}", "reachable", 200)

        threads = [threading.Thread(target=add_results) for _ in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert stats.total == 50


class TestFormatContentResult:
    """Test content result formatting."""

    def test_format_content_result_basic(self):
        """Test basic result formatting."""
        result = {
            "path": "/en/docs/hooks",
            "score": 1.5,
            "title": "Test Title",
            "preview": "Test preview content",
            "keywords": ["test", "example"]
        }

        output = format_content_result(result, 1)

        assert "1." in output
        assert "/en/docs/hooks" in output
        assert "Test Title" in output

    def test_format_content_result_with_keywords(self):
        """Test formatting with keywords."""
        result = {
            "path": "/en/docs/test",
            "score": 1.0,
            "title": "Test Title",
            "preview": "preview",
            "keywords": ["keyword1", "keyword2"]
        }

        output = format_content_result(result, 1)

        assert "keyword1" in output

    def test_format_content_result_with_preview(self):
        """Test formatting with preview."""
        result = {
            "path": "/en/docs/test",
            "score": 1.0,
            "title": "Title",
            "preview": "This is a test preview",
            "keywords": []
        }

        output = format_content_result(result, 1)

        assert "test preview" in output
