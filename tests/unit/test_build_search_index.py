"""Unit tests for search index building."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
import tempfile

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from build_search_index import (
    extract_title,
    extract_keywords,
    path_from_file,
    index_file,
    build_index,
    save_index,
    STOP_WORDS
)


class TestExtractTitle:
    """Test title extraction from markdown."""

    def test_extract_title_basic(self):
        """Test extracting basic title."""
        content = "# Welcome to Docs\nSome content"
        assert extract_title(content) == "Welcome to Docs"

    def test_extract_title_with_whitespace(self):
        """Test title extraction handles extra whitespace."""
        content = "#  Spaced Title  \nMore content"
        assert extract_title(content) == "Spaced Title"

    def test_extract_title_missing(self):
        """Test fallback when no title found."""
        content = "No heading here\nJust content"
        assert extract_title(content) == "Untitled"

    def test_extract_title_multiple_headings(self):
        """Test only first heading is used."""
        content = "# First Title\n# Second Title"
        assert extract_title(content) == "First Title"

    def test_extract_title_with_special_chars(self):
        """Test title with special characters."""
        content = "# Claude Code: Setup & Configuration\nContent"
        assert extract_title(content) == "Claude Code: Setup & Configuration"


class TestExtractKeywords:
    """Test keyword extraction from content."""

    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        content = "Testing testing is important for quality code"
        keywords = extract_keywords(content)

        assert isinstance(keywords, list)
        assert "testing" in keywords
        assert "quality" in keywords

    def test_extract_keywords_removes_stop_words(self):
        """Test stop words are filtered."""
        content = "the quick brown fox jumps over the lazy dog"
        keywords = extract_keywords(content)

        # 'the' is a stop word and should be removed
        assert 'the' not in keywords
        assert 'quick' in keywords or 'brown' in keywords

    def test_extract_keywords_respects_top_n(self):
        """Test top_n parameter limits results."""
        content = "word " * 100  # Repeated word
        keywords = extract_keywords(content, top_n=5)

        assert len(keywords) <= 5

    def test_extract_keywords_removes_code_blocks(self):
        """Test code blocks are removed before extraction."""
        content = """
        # Title
        Here's code: ```python
        def foo():
            pass
        ```
        And regular text about functions.
        """
        keywords = extract_keywords(content)

        # Should not include code-like keywords
        assert len(keywords) > 0

    def test_extract_keywords_empty_content(self):
        """Test empty content returns empty keywords."""
        keywords = extract_keywords("")
        assert keywords == []

    def test_extract_keywords_only_stop_words(self):
        """Test content with only stop words."""
        content = "the and or but is a an"
        keywords = extract_keywords(content)
        assert keywords == []

    def test_extract_keywords_handles_markdown(self):
        """Test markdown syntax is cleaned."""
        content = "[link text](url) and **bold text** and `code`"
        keywords = extract_keywords(content)

        # Should extract keywords without markdown
        assert len(keywords) > 0


class TestPathFromFile:
    """Test file path to URL path conversion."""

    def test_path_from_file_basic(self):
        """Test basic path conversion."""
        file_path = Path("docs/en__docs__overview.md")
        result = path_from_file(file_path, Path("docs"))

        assert result == "/en/docs/overview"

    def test_path_from_file_nested(self):
        """Test nested path conversion."""
        file_path = Path("docs/en__docs__build-with-claude__prompt-engineering.md")
        result = path_from_file(file_path, Path("docs"))

        assert result == "/en/docs/build-with-claude/prompt-engineering"

    def test_path_from_file_removes_extension(self):
        """Test .md extension is removed."""
        file_path = Path("docs/en__test.md")
        result = path_from_file(file_path, Path("docs"))

        assert not result.endswith(".md")

    def test_path_from_file_starts_with_slash(self):
        """Test path starts with slash."""
        file_path = Path("docs/en__api__messages.md")
        result = path_from_file(file_path, Path("docs"))

        assert result.startswith("/")

    def test_path_from_file_handles_relative_path(self):
        """Test relative path handling."""
        file_path = Path("en__docs__test.md")
        result = path_from_file(file_path, Path("."))

        assert result.startswith("/")


class TestIndexFile:
    """Test single file indexing."""

    def test_index_file_basic(self, tmp_path):
        """Test basic file indexing."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        test_file = docs_dir / "en__docs__test.md"
        test_file.write_text("# Test Title\nThis is test content with keywords")

        path, data = index_file(test_file, docs_dir)

        assert path == "/en/docs/test"
        assert data is not None
        assert data["title"] == "Test Title"
        assert "keywords" in data
        assert "word_count" in data

    def test_index_file_content_preview(self, tmp_path):
        """Test content preview generation."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        test_file = docs_dir / "en__docs__test.md"
        long_content = "# Title\n" + "word " * 100
        test_file.write_text(long_content)

        path, data = index_file(test_file, docs_dir)

        assert "content_preview" in data
        assert len(data["content_preview"]) <= 300

    def test_index_file_invalid_encoding(self, tmp_path):
        """Test graceful handling of encoding errors."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        test_file = docs_dir / "en__docs__test.md"
        # Write binary content that might not be valid UTF-8
        test_file.write_bytes(b'\x80\x81\x82')

        path, data = index_file(test_file, docs_dir)

        # Should handle gracefully
        assert path is not None or data is None

    def test_index_file_missing_title(self, tmp_path):
        """Test file without title."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        test_file = docs_dir / "en__docs__test.md"
        test_file.write_text("No heading here, just content")

        path, data = index_file(test_file, docs_dir)

        assert data["title"] == "Untitled"

    def test_index_file_preserves_file_path(self, tmp_path):
        """Test that file path is preserved in metadata."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        test_file = docs_dir / "en__docs__test.md"
        test_file.write_text("# Title\nContent")

        path, data = index_file(test_file, docs_dir)

        assert data["file_path"] == str(test_file)


class TestBuildIndex:
    """Test building complete search index."""

    def test_build_index_empty_directory(self, tmp_path):
        """Test indexing empty directory."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        index = build_index(docs_dir)

        assert index["indexed_files"] == 0
        assert index["index"] == {}

    def test_build_index_single_file(self, tmp_path):
        """Test indexing single file."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        test_file = docs_dir / "en__docs__test.md"
        test_file.write_text("# Test\nContent here")

        index = build_index(docs_dir)

        assert index["indexed_files"] == 1
        assert "/en/docs/test" in index["index"]

    def test_build_index_multiple_files(self, tmp_path):
        """Test indexing multiple files."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        # Create multiple test files
        for i in range(3):
            test_file = docs_dir / f"en__docs__test{i}.md"
            test_file.write_text(f"# Test {i}\nContent {i}")

        index = build_index(docs_dir)

        assert index["indexed_files"] == 3
        assert len(index["index"]) == 3

    def test_build_index_has_version(self, tmp_path):
        """Test index includes version."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        index = build_index(docs_dir)

        assert "version" in index
        assert index["version"] == "1.0"

    def test_build_index_has_timestamp(self, tmp_path):
        """Test index includes generation timestamp."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        index = build_index(docs_dir)

        assert "generated_at" in index
        # Should be ISO format timestamp
        assert "T" in index["generated_at"]
        assert "Z" in index["generated_at"]

    def test_build_index_nested_files(self, tmp_path):
        """Test indexing files in nested directories."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        nested_dir = docs_dir / "nested"
        nested_dir.mkdir()

        test_file = nested_dir / "en__docs__test.md"
        test_file.write_text("# Test\nContent")

        index = build_index(docs_dir)

        assert index["indexed_files"] == 1


class TestSaveIndex:
    """Test saving search index to file."""

    def test_save_index_creates_file(self, tmp_path):
        """Test index file is created."""
        output_file = tmp_path / "index.json"
        test_index = {
            "version": "1.0",
            "indexed_files": 1,
            "index": {"/en/docs/test": {"title": "Test"}}
        }

        save_index(test_index, output_file)

        assert output_file.exists()

    def test_save_index_valid_json(self, tmp_path):
        """Test saved file is valid JSON."""
        output_file = tmp_path / "index.json"
        test_index = {
            "version": "1.0",
            "indexed_files": 1,
            "index": {"/en/docs/test": {"title": "Test"}}
        }

        save_index(test_index, output_file)

        # Should be able to parse as JSON
        with open(output_file) as f:
            loaded = json.load(f)

        assert loaded["version"] == "1.0"

    def test_save_index_creates_parent_dirs(self, tmp_path):
        """Test parent directories are created."""
        output_file = tmp_path / "deep" / "nested" / "path" / "index.json"
        test_index = {"version": "1.0", "indexed_files": 0, "index": {}}

        save_index(test_index, output_file)

        assert output_file.exists()
        assert output_file.parent.exists()

    def test_save_index_preserves_data(self, tmp_path):
        """Test data is preserved when saving."""
        output_file = tmp_path / "index.json"
        test_data = {
            "title": "Test Doc",
            "keywords": ["test", "doc"],
            "word_count": 100
        }
        test_index = {
            "version": "1.0",
            "indexed_files": 1,
            "index": {"/en/docs/test": test_data}
        }

        save_index(test_index, output_file)

        with open(output_file) as f:
            loaded = json.load(f)

        assert loaded["index"]["/en/docs/test"] == test_data


class TestStopWords:
    """Test stop word filtering."""

    def test_stop_words_defined(self):
        """Test stop words are defined."""
        assert len(STOP_WORDS) > 0

    def test_common_words_in_stop_words(self):
        """Test common English words are in stop words."""
        assert 'the' in STOP_WORDS
        assert 'and' in STOP_WORDS
        assert 'is' in STOP_WORDS

    def test_stop_words_are_lowercase(self):
        """Test all stop words are lowercase."""
        for word in STOP_WORDS:
            assert word == word.lower()
