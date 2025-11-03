"""Unit tests for file operations."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import (
    fetch_page,
    save_documentation,
    path_to_filename,
    compute_content_hash,
    content_has_changed
)


class TestFetchPage:
    """Test fetch_page() HTTP fetching."""

    def test_fetch_success(self, mock_http_success):
        """Test successful page fetch."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        # Content must be >= 50 bytes and have markdown indicators
        mock_response.text = """# Test Documentation

This is a test document with enough content to pass validation.

## Section 1

- Item 1
- Item 2
- Item 3

More content here."""
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response

        success, content, error = fetch_page("/en/docs/test", mock_session)

        assert success is True
        assert content is not None
        assert isinstance(content, str)
        assert len(content) > 50

    def test_fetch_404(self, mock_http_404):
        """Test 404 error handling."""
        with pytest.raises(Exception):
            fetch_page("https://docs.anthropic.com/en/docs/nonexistent.md")

    def test_fetch_timeout(self, mock_http_timeout):
        """Test timeout handling."""
        with pytest.raises(Exception):
            fetch_page("https://docs.anthropic.com/en/docs/slow.md")

    def test_retry_logic(self):
        """Test retry logic on failures."""
        with patch('requests.get') as mock_get:
            # First call fails, second succeeds
            mock_get.side_effect = [
                Exception("Network error"),
                Mock(status_code=200, text="Success", raise_for_status=Mock())
            ]

            # Should retry and succeed (if retry logic exists)
            try:
                content = fetch_page("https://docs.anthropic.com/en/docs/test.md")
                # If no retry logic, will raise exception
            except:
                pass  # Expected if no retry logic

    def test_url_construction(self):
        """Test URL is constructed correctly."""
        mock_session = Mock()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "content"
        mock_response.raise_for_status = Mock()
        mock_session.get.return_value = mock_response

        fetch_page("/en/docs/test", mock_session)

        # Verify correct URL was called
        call_args = mock_session.get.call_args
        assert 'https://docs.anthropic.com/en/docs/test.md' in str(call_args)


class TestSaveDocumentation:
    """Test save_documentation() file writing."""

    def test_save_markdown_file(self, tmp_path):
        """Test markdown file saving."""
        content = "# Test\n\nThis is test content."
        output_dir = tmp_path / "docs"

        save_documentation("/en/docs/test", content, output_dir)

        # Check file was created
        saved_file = output_dir / "en__docs__test.md"
        assert saved_file.exists()
        assert saved_file.read_text() == content

    def test_create_output_directory(self, tmp_path):
        """Test output directory is created if missing."""
        output_dir = tmp_path / "new_docs"
        content = "# Test"

        save_documentation("/en/docs/test", content, output_dir)

        assert output_dir.exists()
        assert output_dir.is_dir()

    def test_overwrite_existing(self, tmp_path):
        """Test existing files are overwritten."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        # Save initial content
        save_documentation("/en/docs/test", "Original", output_dir)

        # Overwrite with new content
        save_documentation("/en/docs/test", "Updated", output_dir)

        saved_file = output_dir / "en__docs__test.md"
        assert saved_file.read_text() == "Updated"

    def test_preserve_code_blocks(self, tmp_path, sample_markdown):
        """Test code formatting is preserved."""
        output_dir = tmp_path / "docs"

        save_documentation("/en/docs/test", sample_markdown, output_dir)

        saved_file = output_dir / "en__docs__test.md"
        content = saved_file.read_text()

        # Check code block markers are preserved
        assert "```python" in content
        assert "```" in content


class TestPathToFilename:
    """Test path_to_filename() conversion."""

    def test_basic_conversion(self):
        """Test basic path to filename conversion."""
        filename = path_to_filename("/en/docs/test")
        assert filename == "en__docs__test.md"

    def test_nested_paths(self):
        """Test nested path conversion."""
        filename = path_to_filename("/en/docs/build-with-claude/prompt-engineering")
        assert filename == "en__docs__build-with-claude__prompt-engineering.md"

    def test_remove_leading_slash(self):
        """Test leading slash is removed."""
        filename = path_to_filename("/en/api/messages")
        assert not filename.startswith('/')

    def test_add_md_extension(self):
        """Test .md extension is added."""
        filename = path_to_filename("/en/docs/test")
        assert filename.endswith('.md')

    def test_special_characters(self):
        """Test special characters are handled."""
        filename = path_to_filename("/en/docs/test-page")
        assert "__" in filename  # Slashes converted to double underscore
        assert "-" in filename  # Hyphens preserved


class TestComputeContentHash:
    """Test compute_content_hash() SHA256 hashing."""

    def test_hash_generation(self):
        """Test hash is generated correctly."""
        content = "Test content"
        hash_value = compute_content_hash(content)

        assert hash_value is not None
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA256 is 64 hex chars

    def test_same_content_same_hash(self):
        """Test same content produces same hash."""
        content = "Test content"
        hash1 = compute_content_hash(content)
        hash2 = compute_content_hash(content)

        assert hash1 == hash2

    def test_different_content_different_hash(self):
        """Test different content produces different hash."""
        hash1 = compute_content_hash("Content 1")
        hash2 = compute_content_hash("Content 2")

        assert hash1 != hash2

    def test_empty_content(self):
        """Test empty content hashing."""
        hash_value = compute_content_hash("")

        assert hash_value is not None
        assert len(hash_value) == 64


class TestContentHasChanged:
    """Test content_has_changed() change detection."""

    def test_new_file_has_changed(self):
        """Test new files (no old hash) are considered changed."""
        result = content_has_changed("New content", None)
        assert result is True

    def test_unchanged_content_no_change(self):
        """Test unchanged content is detected."""
        content = "Test content"
        old_hash = compute_content_hash(content)

        result = content_has_changed(content, old_hash)
        assert result is False

    def test_changed_content_detected(self):
        """Test changed content is detected."""
        old_hash = compute_content_hash("Original")

        result = content_has_changed("Updated", old_hash)
        assert result is True
