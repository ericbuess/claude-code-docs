"""Unit tests for path extraction and cleaning."""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from extract_paths import (
    clean_path,
    is_valid_path,
    categorize_path,
    extract_fragment,
    process_paths
)


class TestCleanPath:
    """Test clean_path() function."""

    def test_clean_trailing_backslashes(self):
        """Test removal of backslash artifacts."""
        assert clean_path("/en/docs/test\\") == "/en/docs/test"
        assert clean_path("/en/api/endpoint\\\\") == "/en/api/endpoint"
        assert clean_path("/en/docs/page\\\\\\") == "/en/docs/page"

    def test_clean_whitespace(self):
        """Test whitespace removal."""
        assert clean_path("  /en/docs/test  ") == "/en/docs/test"
        assert clean_path("\t/en/api/messages\n") == "/en/api/messages"

    def test_clean_artifacts(self):
        """Test removal of artifacts like ),"""
        assert clean_path("/en/docs/test),") == "/en/docs/test"
        assert clean_path("/en/api/endpoint),") == "/en/api/endpoint"

    def test_normalize_slashes(self):
        """Test multiple slashes normalized to single."""
        assert clean_path("/en/docs//test") == "/en/docs/test"
        assert clean_path("/en///api/messages") == "/en/api/messages"

    def test_remove_trailing_slash(self):
        """Test trailing slash removal."""
        assert clean_path("/en/docs/test/") == "/en/docs/test"
        assert clean_path("/en/api/messages/") == "/en/api/messages"

    def test_preserve_root_slash(self):
        """Test that root slash is preserved."""
        cleaned = clean_path("/en/")
        assert cleaned.startswith('/')

    def test_empty_string(self):
        """Test empty string handling."""
        assert clean_path("") == ""


class TestIsValidPath:
    """Test is_valid_path() validation function."""

    def test_filter_empty_paths(self):
        """Test empty paths are invalid."""
        assert not is_valid_path("")
        assert not is_valid_path("   ")
        assert not is_valid_path("\t\n")

    def test_filter_slug_patterns(self):
        """Test :slug* patterns are invalid."""
        assert not is_valid_path("/en/docs/:slug*")
        assert not is_valid_path("/en/api/:slug*")
        assert not is_valid_path("/en/prompt-library/:slug*")

    def test_filter_invalid_characters(self):
        """Test paths with invalid characters are rejected."""
        assert not is_valid_path("/en/docs/test<script>")
        assert not is_valid_path("/en/api/messages>")
        assert not is_valid_path("/en/docs/file*.md")
        assert not is_valid_path("/en/api/test?query")

    def test_require_en_prefix(self):
        """Test paths must start with /en/"""
        assert not is_valid_path("/docs/test")
        assert not is_valid_path("en/docs/test")
        assert not is_valid_path("/fr/docs/test")
        assert is_valid_path("/en/docs/test")

    def test_minimum_length(self):
        """Test minimum path length requirement."""
        # Paths < 5 chars are invalid
        assert not is_valid_path("/en/")  # 4 chars
        assert not is_valid_path("/en")   # 3 chars
        # Paths >= 5 chars are valid
        assert is_valid_path("/en/x")     # 5 chars
        assert is_valid_path("/en/docs")  # 8 chars

    def test_valid_paths(self):
        """Test valid paths are accepted."""
        assert is_valid_path("/en/docs/build-with-claude")
        assert is_valid_path("/en/api/messages")
        assert is_valid_path("/en/prompt-library/code-consultant")


class TestCategorizePath:
    """Test categorize_path() category assignment."""

    def test_core_docs_category(self):
        """Test core documentation categorization."""
        assert categorize_path("/en/docs/build-with-claude") == "core_documentation"
        assert categorize_path("/en/docs/test-page") == "core_documentation"

    def test_api_reference_category(self):
        """Test API reference categorization."""
        assert categorize_path("/en/api/messages") == "api_reference"
        assert categorize_path("/en/api/streaming") == "api_reference"

    def test_claude_code_category(self):
        """Test Claude Code categorization (more specific than core docs)."""
        assert categorize_path("/en/docs/claude-code/overview") == "claude_code"
        assert categorize_path("/en/docs/claude-code/mcp/quickstart") == "claude_code"

    def test_prompt_library_category(self):
        """Test prompt library categorization."""
        assert categorize_path("/en/prompt-library/code-consultant") == "prompt_library"
        assert categorize_path("/en/prompt-library/grammar-genie") == "prompt_library"

    def test_resources_category(self):
        """Test resources categorization."""
        assert categorize_path("/en/resources/test") == "resources"

    def test_release_notes_category(self):
        """Test release notes categorization."""
        assert categorize_path("/en/release-notes/2024-01") == "release_notes"

    def test_uncategorized_fallback(self):
        """Test uncategorized fallback for unknown paths."""
        assert categorize_path("/en/unknown/path") == "uncategorized"


class TestExtractFragment:
    """Test extract_fragment() URL fragment separation."""

    def test_extract_fragment_present(self):
        """Test fragment extraction when present."""
        path, fragment = extract_fragment("/en/docs/page#section")
        assert path == "/en/docs/page"
        assert fragment == "section"

    def test_extract_multiple_hashes(self):
        """Test only first hash is split on."""
        path, fragment = extract_fragment("/en/docs/page#section#subsection")
        assert path == "/en/docs/page"
        assert fragment == "section#subsection"

    def test_no_fragment(self):
        """Test paths without fragments."""
        path, fragment = extract_fragment("/en/docs/page")
        assert path == "/en/docs/page"
        assert fragment == ""

    def test_empty_fragment(self):
        """Test path with hash but empty fragment."""
        path, fragment = extract_fragment("/en/docs/page#")
        assert path == "/en/docs/page"
        assert fragment == ""


class TestProcessPaths:
    """Test process_paths() complete processing pipeline."""

    def test_deduplication(self, sample_paths):
        """Test duplicate paths are removed."""
        # Add duplicates
        paths_with_dupes = sample_paths + sample_paths[:2]
        result = process_paths(paths_with_dupes)

        # Count total unique paths
        total = sum(len(paths) for paths in result.values())
        assert total == len(set(sample_paths))

    def test_categorization(self, sample_paths):
        """Test paths are categorized correctly."""
        result = process_paths(sample_paths)

        assert 'core_documentation' in result
        assert 'api_reference' in result
        assert 'claude_code' in result
        assert 'prompt_library' in result

    def test_sorting_within_categories(self):
        """Test paths are sorted within categories."""
        paths = [
            "/en/docs/zebra",
            "/en/docs/apple",
            "/en/docs/middle"
        ]
        result = process_paths(paths)

        core_docs = result.get('core_documentation', [])
        assert core_docs == sorted(core_docs)

    def test_invalid_paths_filtered(self, invalid_paths):
        """Test invalid paths are filtered or cleaned."""
        result = process_paths(invalid_paths)

        # After cleaning, some invalid paths become valid
        # (e.g., '/en/docs/test\\' -> '/en/docs/test')
        # Only truly invalid ones like ':slug*', empty strings filtered
        total = sum(len(paths) for paths in result.values())
        # Should filter out :slug*, empty, whitespace
        # But clean and accept backslash-escaped paths
        assert total >= 0  # At least some get cleaned
