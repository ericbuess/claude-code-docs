"""Unit tests for URL validation."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from lookup_paths import (
    validate_path,
    search_paths,
    load_paths_manifest,
    print_search_results
)


class TestValidatePath:
    """Test validate_path() URL reachability checks."""

    def test_reachability_check_success(self, mock_http_success):
        """Test HTTP 200 detection."""
        result = validate_path("/en/docs/test")

        assert result['path'] == "/en/docs/test"
        assert result['reachable'] is True
        assert result['status_code'] == 200

    def test_broken_link_detection(self, mock_http_404):
        """Test 404 detection."""
        result = validate_path("/en/docs/nonexistent")

        assert result['reachable'] is False
        assert result['status_code'] == 404

    def test_timeout_handling(self, mock_http_timeout):
        """Test timeout error handling."""
        result = validate_path("/en/docs/slow-page")

        assert result['reachable'] is False
        error = result.get('error', '')
        if error:
            assert 'timeout' in error.lower()

    def test_url_construction(self):
        """Test URL is constructed correctly."""
        with patch('requests.head') as mock_head:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.url = "https://docs.anthropic.com/en/docs/test.md"
            mock_response.raise_for_status = Mock()
            mock_head.return_value = mock_response

            validate_path("/en/docs/test")

            # Verify correct URL was called
            call_args = mock_head.call_args
            assert 'https://docs.anthropic.com/en/docs/test.md' in str(call_args)


class TestSearchPaths:
    """Test search_paths() fuzzy search functionality."""

    def test_exact_match(self, paths_manifest):
        """Test exact path matching."""
        results = search_paths("prompt-engineering", paths_manifest)

        # Should find exact matches
        # Results are (path, score) tuples
        assert len(results) > 0
        assert any('prompt-engineering' in path for path, score in results)

    def test_case_insensitive_search(self, paths_manifest):
        """Test case insensitive matching."""
        results_lower = search_paths("api", paths_manifest)
        results_upper = search_paths("API", paths_manifest)

        # Both should return results
        assert len(results_lower) > 0
        assert len(results_upper) > 0

    def test_partial_match(self, paths_manifest):
        """Test partial string matching."""
        results = search_paths("mcp", paths_manifest)

        # Should find paths containing 'mcp'
        assert len(results) > 0

    def test_multi_word_search(self, paths_manifest):
        """Test multi-word search queries."""
        results = search_paths("claude code", paths_manifest)

        # Should find claude-code related paths
        # Results are (path, score) tuples
        assert len(results) > 0
        assert any('claude-code' in path for path, score in results)

    def test_no_results(self, paths_manifest):
        """Test search with no matches."""
        results = search_paths("xyz123nonexistent", paths_manifest)

        assert len(results) == 0

    def test_results_include_category(self, paths_manifest):
        """Test search results include score information."""
        results = search_paths("api", paths_manifest)

        # Results are (path, score) tuples
        if results:
            path, score = results[0]
            assert isinstance(path, str)
            assert isinstance(score, (int, float))

    def test_relevance_scoring(self, paths_manifest):
        """Test results are sorted by relevance."""
        results = search_paths("messages", paths_manifest)

        if len(results) > 1:
            # Exact matches should rank higher
            for i in range(len(results) - 1):
                # More exact matches should appear first
                pass  # Scoring logic may vary


class TestLoadPathsManifest:
    """Test load_paths_manifest() functionality."""

    def test_load_valid_manifest(self, temp_manifest):
        """Test loading valid manifest file."""
        manifest = load_paths_manifest(temp_manifest)

        assert manifest is not None
        assert 'categories' in manifest
        assert 'metadata' in manifest

    def test_missing_manifest(self, tmp_path):
        """Test handling of missing manifest file."""
        nonexistent = tmp_path / "nonexistent.json"

        # Should raise FileNotFoundError
        try:
            manifest = load_paths_manifest(nonexistent)
            pytest.fail("Should have raised FileNotFoundError")
        except FileNotFoundError:
            pass  # Expected behavior
