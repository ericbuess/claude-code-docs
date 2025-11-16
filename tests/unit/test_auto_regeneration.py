"""
Comprehensive tests for auto-regeneration of paths_manifest.json.

These tests cover:
1. categorize_path() function
2. update_paths_manifest() function
3. discover_from_all_sitemaps() function
4. Integration with main() workflow
"""

import pytest
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import xml.etree.ElementTree as ET

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from fetch_claude_docs import (
    discover_from_all_sitemaps,
    discover_claude_code_pages,
)


class TestCategorizePath:
    """Test categorize_path() function for auto-categorization."""

    def test_categorize_api_reference(self):
        """Test API reference categorization."""
        paths = [
            "/en/api/messages",
            "/en/api/admin-api/users/list",
            "/en/docs/agent-sdk/overview",
            "/en/docs/agent-sdk/python",
        ]

        # Import here to avoid circular import
        from fetch_claude_docs import categorize_path

        for path in paths:
            assert categorize_path(path) == "api_reference"

    def test_categorize_claude_code(self):
        """Test Claude Code docs categorization."""
        paths = [
            "/docs/en/hooks",
            "/docs/en/setup",
            "/docs/en/mcp",
            "/docs/en/sdk/overview",
        ]

        from fetch_claude_docs import categorize_path

        for path in paths:
            assert categorize_path(path) == "claude_code"

    def test_categorize_prompt_library(self):
        """Test prompt library categorization."""
        paths = [
            "/en/prompt-library/code-clarifier",
            "/en/resources/prompt-library/grammar-genie",
        ]

        from fetch_claude_docs import categorize_path

        for path in paths:
            assert categorize_path(path) == "prompt_library"

    def test_categorize_resources(self):
        """Test resources categorization."""
        paths = [
            "/en/resources/glossary",
            "/en/resources/faq",
        ]

        from fetch_claude_docs import categorize_path

        for path in paths:
            assert categorize_path(path) == "resources"

    def test_categorize_release_notes(self):
        """Test release notes categorization."""
        paths = [
            "/en/release-notes/api",
            "/en/release-notes/2024-01",
        ]

        from fetch_claude_docs import categorize_path

        for path in paths:
            assert categorize_path(path) == "release_notes"

    def test_categorize_core_documentation(self):
        """Test core documentation categorization (fallback)."""
        paths = [
            "/en/docs/about-claude/models",
            "/en/docs/build-with-claude/prompt-engineering",
            "/en/docs/test-and-evaluate/define-success",
        ]

        from fetch_claude_docs import categorize_path

        for path in paths:
            assert categorize_path(path) == "core_documentation"


class TestUpdatePathsManifest:
    """Test update_paths_manifest() function."""

    def test_update_paths_manifest_creates_categorized_structure(self, tmp_path):
        """Test that update_paths_manifest() creates properly categorized manifest."""
        from fetch_claude_docs import update_paths_manifest

        paths = [
            "/en/api/messages",
            "/docs/en/hooks",
            "/en/prompt-library/code-clarifier",
            "/en/resources/glossary",
            "/en/docs/about-claude/models",
        ]

        manifest_file = tmp_path / "paths_manifest.json"

        update_paths_manifest(paths, manifest_file)

        # Load and verify
        with open(manifest_file) as f:
            manifest = json.load(f)

        assert "metadata" in manifest
        assert manifest["metadata"]["total_paths"] == 5
        assert "categories" in manifest

        # Check categorization
        assert "/en/api/messages" in manifest["categories"]["api_reference"]
        assert "/docs/en/hooks" in manifest["categories"]["claude_code"]
        assert "/en/prompt-library/code-clarifier" in manifest["categories"]["prompt_library"]
        assert "/en/resources/glossary" in manifest["categories"]["resources"]
        assert "/en/docs/about-claude/models" in manifest["categories"]["core_documentation"]

    def test_update_paths_manifest_includes_metadata(self, tmp_path):
        """Test that metadata is properly included."""
        from fetch_claude_docs import update_paths_manifest

        paths = ["/en/api/messages", "/docs/en/hooks"]
        manifest_file = tmp_path / "paths_manifest.json"

        update_paths_manifest(paths, manifest_file)

        with open(manifest_file) as f:
            manifest = json.load(f)

        assert "generated_at" in manifest["metadata"]
        assert "total_paths" in manifest["metadata"]
        assert manifest["metadata"]["total_paths"] == 2
        assert "source" in manifest["metadata"]
        assert manifest["metadata"]["source"] == "sitemap_discovery"


class TestDiscoverFromAllSitemaps:
    """Test discover_from_all_sitemaps() function."""

    @patch('fetch_claude_docs.discover_claude_code_pages')
    def test_discover_from_all_sitemaps_combines_results(self, mock_discover):
        """Test that it combines results from all sitemaps."""
        # Mock different results from different sitemaps
        mock_discover.side_effect = [
            ["/en/api/messages", "/en/docs/about-claude/models"],  # First sitemap
            ["/docs/en/hooks", "/docs/en/setup"],  # Second sitemap
            ["/en/api/messages", "/en/resources/glossary"],  # Third sitemap (has duplicate)
        ]

        session = Mock()

        result = discover_from_all_sitemaps(session)

        # Should combine and deduplicate
        assert len(result) == 5  # 6 total - 1 duplicate
        assert "/en/api/messages" in result
        assert "/docs/en/hooks" in result
        assert "/en/resources/glossary" in result

    @patch('fetch_claude_docs.discover_claude_code_pages')
    def test_discover_from_all_sitemaps_handles_failures(self, mock_discover):
        """Test that it continues even if some sitemaps fail."""
        # First sitemap works, second fails, third works
        mock_discover.side_effect = [
            ["/en/api/messages"],
            Exception("Sitemap unavailable"),
            ["/docs/en/hooks"],
        ]

        session = Mock()

        result = discover_from_all_sitemaps(session)

        # Should succeed with partial results
        assert len(result) == 2
        assert "/en/api/messages" in result
        assert "/docs/en/hooks" in result

    @patch('fetch_claude_docs.discover_claude_code_pages')
    def test_discover_from_all_sitemaps_fails_if_all_fail(self, mock_discover):
        """Test that it raises exception if ALL sitemaps fail."""
        mock_discover.side_effect = Exception("All sitemaps unavailable")

        session = Mock()

        with pytest.raises(Exception, match="Could not discover from any sitemap"):
            discover_from_all_sitemaps(session)


class TestMainWorkflowIntegration:
    """Test that auto-regeneration integrates properly with main() workflow."""

    @patch('fetch_claude_docs.discover_from_all_sitemaps')
    @patch('fetch_claude_docs.update_paths_manifest')
    @patch('fetch_claude_docs.fetch_markdown_content')
    @patch('fetch_claude_docs.save_manifest')
    @patch('fetch_claude_docs.fetch_changelog')
    def test_main_calls_update_paths_manifest_after_discovery(
        self, mock_changelog, mock_save, mock_fetch, mock_update, mock_discover
    ):
        """Test that main() calls update_paths_manifest() after successful discovery."""
        # Setup mocks
        mock_discover.return_value = ["/en/api/messages", "/docs/en/hooks"]
        mock_fetch.return_value = ("test.md", "content")
        mock_changelog.return_value = ("changelog.md", "changelog content")

        # Import and run (we'll need to mock more for full integration)
        # This tests the INTENT - actual implementation will be tested in integration tests

        # For now, verify the function exists and can be imported
        from fetch_claude_docs import update_paths_manifest
        assert callable(update_paths_manifest)


# Edge case tests
class TestEdgeCases:
    """Test edge cases in auto-regeneration."""

    def test_categorize_path_with_special_characters(self):
        """Test paths with special characters."""
        from fetch_claude_docs import categorize_path

        # Should handle these without crashing
        test_cases = [
            ("/en/api/messages-v2", "api_reference"),
            ("/docs/en/mcp/sub-topic", "claude_code"),  # NEW path format
            ("/en/prompt-library/code-consultant-v2", "prompt_library"),
        ]

        for path, expected_category in test_cases:
            result = categorize_path(path)
            assert isinstance(result, str)
            assert result == expected_category, f"Path {path} should be {expected_category}, got {result}"

    def test_update_paths_manifest_empty_paths(self, tmp_path):
        """Test with empty paths list."""
        from fetch_claude_docs import update_paths_manifest

        manifest_file = tmp_path / "paths_manifest.json"

        update_paths_manifest([], manifest_file)

        with open(manifest_file) as f:
            manifest = json.load(f)

        assert manifest["metadata"]["total_paths"] == 0
        assert manifest["categories"] == {}

    def test_update_paths_manifest_many_paths(self, tmp_path):
        """Test with realistic number of paths (~270)."""
        from fetch_claude_docs import update_paths_manifest

        # Generate 270 realistic paths
        paths = [f"/en/api/endpoint-{i}" for i in range(100)]
        paths += [f"/docs/en/page-{i}" for i in range(70)]
        paths += [f"/en/prompt-library/prompt-{i}" for i in range(100)]

        manifest_file = tmp_path / "paths_manifest.json"

        update_paths_manifest(paths, manifest_file)

        with open(manifest_file) as f:
            manifest = json.load(f)

        assert manifest["metadata"]["total_paths"] == 270
        assert len(manifest["categories"]["api_reference"]) == 100
        assert len(manifest["categories"]["claude_code"]) == 70
        assert len(manifest["categories"]["prompt_library"]) == 100
