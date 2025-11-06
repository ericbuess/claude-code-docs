"""Unit tests for update_sitemap.py CLI and missing functions."""

import pytest
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from update_sitemap import (
    generate_category_index,
    generate_search_index,
    generate_full_sitemap,
    main
)


class TestGenerateCategoryIndex:
    """Test generate_category_index() function."""

    def test_generate_basic_index(self):
        """Test basic category index generation."""
        category_name = "core_documentation"
        paths = [
            "/en/docs/overview",
            "/en/docs/quickstart",
            "/en/docs/guides/getting-started"
        ]
        docs_manifest = {
            "/en/docs/overview": {
                "size": 1000,
                "last_updated": "2024-01-01T00:00:00"
            },
            "/en/docs/quickstart": {
                "size": 2000,
                "last_updated": "2024-01-02T00:00:00"
            }
        }

        result = generate_category_index(category_name, paths, docs_manifest)

        assert result["category"] == category_name
        assert result["count"] == 3
        assert "tree" in result
        assert "paths" in result
        assert len(result["paths"]) == 3

    def test_generate_index_with_sizes(self):
        """Test index generation includes size calculations."""
        category_name = "api_reference"
        paths = ["/en/api/messages"]
        docs_manifest = {
            "/en/api/messages": {
                "size": 5000,
                "last_updated": "2024-01-01T00:00:00"
            }
        }

        result = generate_category_index(category_name, paths, docs_manifest)

        assert result["total_size_bytes"] == 5000

    def test_generate_index_finds_latest_update(self):
        """Test index finds the most recent update."""
        category_name = "guides"
        paths = ["/en/docs/guide1", "/en/docs/guide2"]
        docs_manifest = {
            "/en/docs/guide1": {"last_updated": "2024-01-01T00:00:00"},
            "/en/docs/guide2": {"last_updated": "2024-06-15T12:00:00"}
        }

        result = generate_category_index(category_name, paths, docs_manifest)

        assert result["last_updated"] is not None
        assert "2024-06-15" in result["last_updated"]

    def test_generate_index_empty_paths(self):
        """Test index generation with empty paths."""
        category_name = "empty_category"
        paths = []
        docs_manifest = {}

        result = generate_category_index(category_name, paths, docs_manifest)

        assert result["count"] == 0
        assert result["total_size_bytes"] == 0


class TestGenerateSearchIndex:
    """Test generate_search_index() function."""

    def test_generate_search_index_basic(self, tmp_path):
        """Test basic search index generation."""
        paths_manifest = {
            "categories": {
                "core_documentation": ["/en/docs/overview"],
                "api_reference": ["/en/api/messages"]
            }
        }
        docs_manifest = {
            "/en/docs/overview": {
                "size": 1000,
                "last_updated": "2024-01-01T00:00:00"
            }
        }

        result = generate_search_index(paths_manifest, docs_manifest, tmp_path)

        assert isinstance(result, dict)
        assert "/en/docs/overview" in result
        assert "/en/api/messages" in result

    def test_search_index_extracts_title(self, tmp_path):
        """Test search index extracts titles from paths."""
        paths_manifest = {
            "categories": {
                "guides": ["/en/docs/getting-started"]
            }
        }
        docs_manifest = {}

        result = generate_search_index(paths_manifest, docs_manifest, tmp_path)

        entry = result["/en/docs/getting-started"]
        assert "getting" in entry["title"].lower() or "started" in entry["title"].lower()

    def test_search_index_extracts_keywords(self, tmp_path):
        """Test search index extracts keywords from path."""
        paths_manifest = {
            "categories": {
                "claude_code": ["/en/docs/claude-code/mcp/quickstart"]
            }
        }
        docs_manifest = {}

        result = generate_search_index(paths_manifest, docs_manifest, tmp_path)

        entry = result["/en/docs/claude-code/mcp/quickstart"]
        assert "keywords" in entry
        assert "claude-code" in entry["keywords"]
        assert "mcp" in entry["keywords"]

    def test_search_index_with_file_preview(self, tmp_path):
        """Test search index extracts content preview from files."""
        # Create a test markdown file
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        doc_file = docs_dir / "en__docs__test.md"
        doc_file.write_text("# Test Page\n\nThis is test content for preview.")

        paths_manifest = {
            "categories": {
                "core": ["/en/docs/test"]
            }
        }
        docs_manifest = {}

        result = generate_search_index(paths_manifest, docs_manifest, docs_dir)

        entry = result["/en/docs/test"]
        # Content preview might be extracted
        assert "content_preview" in entry

    def test_search_index_empty_manifest(self, tmp_path):
        """Test search index with empty manifest."""
        paths_manifest = {"categories": {}}
        docs_manifest = {}

        result = generate_search_index(paths_manifest, docs_manifest, tmp_path)

        assert result == {}


class TestGenerateFullSitemap:
    """Test generate_full_sitemap() function."""

    def test_generate_full_sitemap_basic(self):
        """Test basic sitemap generation."""
        paths_manifest = {
            "categories": {
                "core_documentation": ["/en/docs/page1", "/en/docs/page2"],
                "api_reference": ["/en/api/messages"]
            }
        }
        docs_manifest = {
            "/en/docs/page1": {"last_updated": "2024-01-01T00:00:00"}
        }
        category_indexes = {
            "core_documentation": {
                "count": 2,
                "last_updated": "2024-01-01T00:00:00"
            },
            "api_reference": {
                "count": 1,
                "last_updated": None
            }
        }

        result = generate_full_sitemap(paths_manifest, docs_manifest, category_indexes)

        assert result["total_paths"] == 3
        assert result["documented_paths"] == 1
        assert "coverage_percent" in result
        assert "categories" in result
        assert "generated_at" in result

    def test_sitemap_calculates_coverage(self):
        """Test sitemap calculates coverage percentage."""
        paths_manifest = {
            "categories": {
                "core": [f"/en/docs/page{i}" for i in range(10)]
            }
        }
        docs_manifest = {
            f"/en/docs/page{i}": {} for i in range(5)
        }
        category_indexes = {}

        result = generate_full_sitemap(paths_manifest, docs_manifest, category_indexes)

        assert result["total_paths"] == 10
        assert result["documented_paths"] == 5
        assert result["coverage_percent"] == 50.0

    def test_sitemap_finds_latest_update(self):
        """Test sitemap finds most recent update."""
        paths_manifest = {"categories": {}}
        docs_manifest = {
            "page1": {"last_updated": "2024-01-01T00:00:00"},
            "page2": {"last_updated": "2024-06-15T00:00:00"},
            "page3": {"last_updated": "2024-03-10T00:00:00"}
        }
        category_indexes = {}

        result = generate_full_sitemap(paths_manifest, docs_manifest, category_indexes)

        assert result["last_updated"] is not None
        assert "2024-06-15" in result["last_updated"]

    def test_sitemap_handles_zero_paths(self):
        """Test sitemap handles zero total paths."""
        paths_manifest = {"categories": {}}
        docs_manifest = {}
        category_indexes = {}

        result = generate_full_sitemap(paths_manifest, docs_manifest, category_indexes)

        assert result["total_paths"] == 0
        assert result["documented_paths"] == 0
        assert result["coverage_percent"] == 0

    def test_sitemap_includes_category_summaries(self):
        """Test sitemap includes category summaries."""
        paths_manifest = {"categories": {"core": ["/en/docs/test"]}}
        docs_manifest = {}
        category_indexes = {
            "core": {
                "count": 1,
                "last_updated": "2024-01-01T00:00:00"
            }
        }

        result = generate_full_sitemap(paths_manifest, docs_manifest, category_indexes)

        assert "categories" in result
        assert "core" in result["categories"]
        assert result["categories"]["core"]["count"] == 1


class TestMainCLI:
    """Test main() CLI entry point."""

    def test_main_requires_manifests(self, tmp_path):
        """Test main requires manifest files."""
        manifest_file = tmp_path / "missing.json"
        docs_manifest_file = tmp_path / "docs_missing.json"

        test_args = [
            "update_sitemap.py",
            "--manifest", str(manifest_file),
            "--docs-manifest", str(docs_manifest_file)
        ]

        with patch('sys.argv', test_args):
            result = main()
            # Should return error code
            assert result == 1

    def test_main_generates_outputs(self, tmp_path, monkeypatch):
        """Test main generates output files."""
        # Create input manifests
        paths_manifest = {
            "categories": {
                "core": ["/en/docs/test1", "/en/docs/test2"]
            }
        }
        docs_manifest_data = {
            "files": {
                "test1.md": {
                    "original_url": "https://example.com/test1",
                    "last_updated": "2024-01-01T00:00:00"
                }
            }
        }

        manifest_file = tmp_path / "paths.json"
        docs_manifest_file = tmp_path / "docs.json"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        manifest_file.write_text(json.dumps(paths_manifest))
        docs_manifest_file.write_text(json.dumps(docs_manifest_data))

        test_args = [
            "update_sitemap.py",
            "--manifest", str(manifest_file),
            "--docs-manifest", str(docs_manifest_file),
            "--output-dir", str(output_dir),
            "--docs-dir", str(tmp_path)
        ]

        with patch('sys.argv', test_args):
            result = main()

        # Should succeed
        assert result == 0

        # Check outputs created
        assert (output_dir / ".search_index.json").exists()
        assert (output_dir / "sitemap.json").exists()

    def test_main_sitemap_only_mode(self, tmp_path):
        """Test main with --sitemap-only flag."""
        paths_manifest = {"categories": {"core": ["/en/docs/test"]}}
        docs_manifest_data = {"files": {}}

        manifest_file = tmp_path / "paths.json"
        docs_manifest_file = tmp_path / "docs.json"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        manifest_file.write_text(json.dumps(paths_manifest))
        docs_manifest_file.write_text(json.dumps(docs_manifest_data))

        test_args = [
            "update_sitemap.py",
            "--manifest", str(manifest_file),
            "--docs-manifest", str(docs_manifest_file),
            "--output-dir", str(output_dir),
            "--sitemap-only"
        ]

        with patch('sys.argv', test_args):
            result = main()

        assert result == 0

        # Sitemap should be created
        assert (output_dir / "sitemap.json").exists()

        # Category indexes directory might not be created in sitemap-only mode
        # Just check that the command completed successfully

    def test_main_with_invalid_json(self, tmp_path):
        """Test main handles invalid JSON gracefully."""
        manifest_file = tmp_path / "invalid.json"
        docs_manifest_file = tmp_path / "docs.json"
        output_dir = tmp_path / "output"
        output_dir.mkdir()

        manifest_file.write_text("{ invalid json }")
        docs_manifest_file.write_text("{}")

        test_args = [
            "update_sitemap.py",
            "--manifest", str(manifest_file),
            "--docs-manifest", str(docs_manifest_file),
            "--output-dir", str(output_dir)
        ]

        with patch('sys.argv', test_args):
            result = main()

        # Should return error code
        assert result == 1
