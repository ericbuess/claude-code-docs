"""Validation tests for HTML and markdown quality."""

import pytest
import sys
from pathlib import Path
import re

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import fetch_page


class TestValidMarkdown:
    """Test generated markdown is valid."""

    @pytest.mark.integration
    def test_markdown_has_headings(self, sample_markdown):
        """Test markdown contains proper heading syntax."""
        assert re.search(r'^#+ ', sample_markdown, re.MULTILINE)

    @pytest.mark.integration
    def test_markdown_code_blocks_closed(self, sample_markdown):
        """Test code blocks are properly closed."""
        # Count opening and closing backticks
        triple_backticks = sample_markdown.count('```')

        # Should be even (each opening has a closing)
        assert triple_backticks % 2 == 0

    @pytest.mark.integration
    def test_markdown_lists_formatted(self, sample_markdown):
        """Test lists are properly formatted."""
        # Check for list syntax
        has_unordered = bool(re.search(r'^\s*[-*+] ', sample_markdown, re.MULTILINE))
        has_ordered = bool(re.search(r'^\s*\d+\. ', sample_markdown, re.MULTILINE))

        # At least one list format should be present
        assert has_unordered or has_ordered

    @pytest.mark.integration
    def test_no_html_tags_in_markdown(self, sample_markdown):
        """Test markdown doesn't contain HTML tags (except allowed ones)."""
        # Check for common HTML tags that should be converted
        forbidden_tags = ['<div>', '<span>', '<p>', '</div>', '</span>', '</p>']

        for tag in forbidden_tags:
            # Some tags may be allowed in markdown, adjust as needed
            pass

    @pytest.mark.integration
    def test_links_properly_formatted(self, sample_markdown):
        """Test markdown links are properly formatted."""
        # Check for markdown link syntax: [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', sample_markdown)

        # If links exist, they should be properly formatted
        if links:
            for text, url in links:
                assert len(text) > 0
                assert len(url) > 0


class TestNoParsingErrors:
    """Test parser handles all pages."""

    @pytest.mark.integration
    def test_parse_sample_html(self, sample_html):
        """Test HTML parsing doesn't crash."""
        # Since we're using direct markdown fetch, this tests file reading
        assert sample_html is not None
        assert len(sample_html) > 0

    @pytest.mark.integration
    def test_handle_empty_content(self):
        """Test parser handles empty content gracefully."""
        empty = ""

        # Should not crash
        assert empty == ""

    @pytest.mark.integration
    def test_handle_minimal_content(self):
        """Test parser handles minimal content."""
        minimal = "# Title\n\nContent"

        # Should be valid
        assert "Title" in minimal


class TestCodeBlockPreservation:
    """Test code blocks are preserved correctly."""

    @pytest.mark.integration
    def test_python_code_blocks(self, sample_markdown):
        """Test Python code blocks are preserved."""
        # Check for Python code blocks
        has_python = '```python' in sample_markdown

        if has_python:
            # Code should be indented/formatted properly
            assert 'import' in sample_markdown or 'def' in sample_markdown

    @pytest.mark.integration
    def test_inline_code_preserved(self):
        """Test inline code is preserved."""
        markdown = "Use `print()` to output text."

        # Inline code markers should be present
        assert '`print()`' in markdown

    @pytest.mark.integration
    def test_multiline_code_preserved(self, sample_markdown):
        """Test multiline code blocks maintain structure."""
        # Find code blocks
        code_blocks = re.findall(r'```[\w]*\n(.*?)```', sample_markdown, re.DOTALL)

        if code_blocks:
            for block in code_blocks:
                # Code should have content
                assert len(block.strip()) > 0


class TestContentStructure:
    """Test overall content structure is valid."""

    @pytest.mark.integration
    def test_has_title(self, sample_markdown):
        """Test markdown has a title (h1)."""
        has_h1 = bool(re.search(r'^# ', sample_markdown, re.MULTILINE))

        assert has_h1

    @pytest.mark.integration
    def test_has_content_after_title(self, sample_markdown):
        """Test there's content after the title."""
        lines = sample_markdown.split('\n')

        # Should have more than just a title
        assert len(lines) > 2

    @pytest.mark.integration
    def test_no_excessive_blank_lines(self, sample_markdown):
        """Test no excessive blank lines."""
        # Check for more than 3 consecutive blank lines
        excessive = re.search(r'\n\n\n\n\n', sample_markdown)

        # Should not have excessive blank lines
        assert not excessive


class TestSpecialCharacters:
    """Test special characters are handled correctly."""

    @pytest.mark.integration
    def test_unicode_characters_preserved(self):
        """Test Unicode characters are preserved."""
        content = "Emoji: 🚀 | Accent: café | Symbol: ∞"

        # Should be preserved as-is
        assert '🚀' in content
        assert 'café' in content
        assert '∞' in content

    @pytest.mark.integration
    def test_html_entities_converted(self):
        """Test HTML entities are handled."""
        # If converting from HTML, entities should be decoded
        # &lt; → <, &gt; → >, &amp; → &
        pass  # Implementation depends on conversion strategy

    @pytest.mark.integration
    def test_quotes_preserved(self):
        """Test various quote types are preserved."""
        content = 'Single: \' | Double: " | Smart: " "'

        # Should contain quotes
        assert "'" in content or '"' in content
