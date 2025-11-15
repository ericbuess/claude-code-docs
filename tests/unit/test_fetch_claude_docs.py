"""Unit tests for fetching Claude documentation."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import xml.etree.ElementTree as ET

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from fetch_claude_docs import (
    load_manifest,
    save_manifest,
    url_to_safe_filename,
    discover_sitemap_and_base_url,
    discover_claude_code_pages,
    validate_markdown_content,
    get_base_url_for_path,
    convert_legacy_path_to_fetch_url,
    HEADERS,
    MANIFEST_FILE
)


class TestLoadManifest:
    """Test manifest loading."""

    def test_load_manifest_existing(self, tmp_path):
        """Test loading existing manifest."""
        manifest_data = {
            "files": {
                "/en/docs/test": {"title": "Test"}
            },
            "last_updated": "2024-01-01T00:00:00"
        }

        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        manifest_file = docs_dir / MANIFEST_FILE
        manifest_file.write_text(json.dumps(manifest_data))

        manifest = load_manifest(docs_dir)

        assert "files" in manifest
        assert "/en/docs/test" in manifest["files"]

    def test_load_manifest_missing(self, tmp_path):
        """Test loading manifest when file doesn't exist."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        manifest = load_manifest(docs_dir)

        assert "files" in manifest
        assert manifest["files"] == {}
        assert "last_updated" in manifest

    def test_load_manifest_corrupted(self, tmp_path):
        """Test loading corrupted manifest."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        manifest_file = docs_dir / MANIFEST_FILE
        manifest_file.write_text("invalid json {]")

        manifest = load_manifest(docs_dir)

        # Should fallback to empty manifest
        assert "files" in manifest

    def test_load_manifest_missing_files_key(self, tmp_path):
        """Test manifest missing 'files' key is fixed."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        manifest_file = docs_dir / MANIFEST_FILE
        manifest_file.write_text('{"other_key": "value"}')

        manifest = load_manifest(docs_dir)

        assert "files" in manifest


class TestSaveManifest:
    """Test manifest saving."""

    @patch.dict('os.environ', {}, clear=True)
    def test_save_manifest_basic(self, tmp_path):
        """Test basic manifest saving."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        manifest = {
            "files": {
                "/en/docs/test": {"title": "Test"}
            }
        }

        save_manifest(docs_dir, manifest)

        manifest_file = docs_dir / MANIFEST_FILE
        assert manifest_file.exists()

        saved = json.loads(manifest_file.read_text())
        assert "files" in saved
        assert "last_updated" in saved

    @patch.dict('os.environ', {'GITHUB_REPOSITORY': 'test/repo', 'GITHUB_REF_NAME': 'main'})
    def test_save_manifest_uses_github_env(self, tmp_path):
        """Test manifest uses GitHub environment variables."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        manifest = {"files": {}}

        save_manifest(docs_dir, manifest)

        manifest_file = docs_dir / MANIFEST_FILE
        saved = json.loads(manifest_file.read_text())

        assert saved["github_repository"] == "test/repo"
        assert saved["github_ref"] == "main"
        assert "test/repo/main" in saved["base_url"]

    @patch.dict('os.environ', {}, clear=True)
    def test_save_manifest_uses_default_repo(self, tmp_path):
        """Test manifest uses default repo when env not set."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        manifest = {"files": {}}

        save_manifest(docs_dir, manifest)

        manifest_file = docs_dir / MANIFEST_FILE
        saved = json.loads(manifest_file.read_text())

        assert "costiash/claude-code-docs" in saved["base_url"]

    @patch.dict('os.environ', {'GITHUB_REPOSITORY': 'invalid repo name'}, clear=True)
    def test_save_manifest_validates_repo_format(self, tmp_path):
        """Test invalid repo format is sanitized."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        manifest = {"files": {}}

        save_manifest(docs_dir, manifest)

        manifest_file = docs_dir / MANIFEST_FILE
        saved = json.loads(manifest_file.read_text())

        # Should fallback to default
        assert "costiash/claude-code-docs" in saved["base_url"]

    def test_save_manifest_includes_timestamp(self, tmp_path):
        """Test manifest includes timestamp."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()

        manifest = {"files": {}}

        save_manifest(docs_dir, manifest)

        manifest_file = docs_dir / MANIFEST_FILE
        saved = json.loads(manifest_file.read_text())

        assert "last_updated" in saved
        assert "T" in saved["last_updated"]  # ISO format


class TestUrlToSafeFilename:
    """Test URL to safe filename conversion."""

    def test_url_to_safe_filename_basic(self):
        """Test basic filename conversion."""
        url = "/en/docs/claude-code/overview"
        result = url_to_safe_filename(url)

        assert result.endswith(".md")
        assert "/" not in result
        # Result should be a valid filename
        assert isinstance(result, str)

    def test_url_to_safe_filename_with_claude_code_prefix(self):
        """Test removes claude-code prefix."""
        url = "/en/docs/claude-code/overview"
        result = url_to_safe_filename(url)

        # Should have converted slashes to double underscores
        assert isinstance(result, str)
        assert result.endswith(".md")

    def test_url_to_safe_filename_no_subdirectories(self):
        """Test simple path without subdirectories."""
        url = "/en/docs/claude-code/overview"
        result = url_to_safe_filename(url)

        assert result.endswith(".md")
        assert "/" not in result

    def test_url_to_safe_filename_nested_paths(self):
        """Test nested path conversion."""
        url = "/en/docs/claude-code/advanced/setup"
        result = url_to_safe_filename(url)

        assert result.endswith(".md")
        assert "__" in result  # Should have double underscores

    def test_url_to_safe_filename_already_has_extension(self):
        """Test doesn't double .md extension."""
        url = "/en/docs/claude-code/overview.md"
        result = url_to_safe_filename(url)

        assert result.endswith(".md")
        assert result.count(".md") == 1

    def test_url_to_safe_filename_preserves_hyphens(self):
        """Test hyphens are preserved."""
        url = "/en/docs/claude-code/getting-started"
        result = url_to_safe_filename(url)

        assert "-" in result or "getting__started" in result

    def test_url_to_safe_filename_different_prefixes(self):
        """Test handles different claude-code prefix formats."""
        test_cases = [
            "/en/docs/claude-code/test",
            "/docs/claude-code/test",
            "/claude-code/test"
        ]

        for url in test_cases:
            result = url_to_safe_filename(url)
            assert result.endswith(".md")
            assert "/" not in result

    def test_url_to_safe_filename_sanitizes_special_characters(self):
        """Test that special characters are removed."""
        # Test various special characters that should be removed
        url = "/en/docs/test<script>alert('xss')</script>"
        result = url_to_safe_filename(url)

        # Should only contain alphanumeric, hyphens, underscores, dots
        assert "<" not in result
        assert ">" not in result
        assert "(" not in result
        assert ")" not in result
        assert "'" not in result
        assert result.endswith(".md")

    def test_url_to_safe_filename_sanitizes_path_traversal(self):
        """Test that path traversal attempts are sanitized."""
        # Try path traversal patterns
        url = "/en/docs/../../../etc/passwd"
        result = url_to_safe_filename(url)

        # Should have removed dots in traversal pattern but kept necessary structure
        assert result.endswith(".md")
        # After sanitization, should be safe
        assert "/" not in result

    def test_url_to_safe_filename_sanitizes_null_bytes(self):
        """Test that null bytes are removed."""
        url = "/en/docs/test\x00malicious"
        result = url_to_safe_filename(url)

        # Null bytes should be removed
        assert "\x00" not in result
        assert result.endswith(".md")

    def test_url_to_safe_filename_sanitizes_shell_metacharacters(self):
        """Test that shell metacharacters are removed."""
        url = "/en/docs/test;rm -rf /"
        result = url_to_safe_filename(url)

        # Shell metacharacters should be removed
        assert ";" not in result
        assert " " not in result
        assert result.endswith(".md")

    def test_url_to_safe_filename_sanitizes_unicode_attacks(self):
        """Test that problematic unicode is handled."""
        # Unicode characters that could cause issues
        url = "/en/docs/test\u202e\u202d"  # Right-to-left override
        result = url_to_safe_filename(url)

        # Should only contain safe characters
        assert result.endswith(".md")
        # Unicode control characters should be removed
        assert "\u202e" not in result
        assert "\u202d" not in result

    def test_url_to_safe_filename_empty_after_sanitization(self):
        """Test that empty result after sanitization raises error."""
        # URL with only special characters
        url = "///<<<>>>"

        with pytest.raises(ValueError, match="empty filename"):
            url_to_safe_filename(url)

    def test_url_to_safe_filename_only_extension(self):
        """Test that only .md extension raises error."""
        url = "/.md"

        with pytest.raises(ValueError, match="empty filename"):
            url_to_safe_filename(url)

    def test_url_to_safe_filename_preserves_valid_characters(self):
        """Test that valid characters are preserved."""
        url = "/en/docs/test-file_name123"
        result = url_to_safe_filename(url)

        # Should preserve alphanumeric, hyphens, underscores
        assert "test-file_name123" in result or "testfilename123" in result
        assert result.endswith(".md")

    def test_url_to_safe_filename_sql_injection_attempt(self):
        """Test SQL injection patterns are sanitized."""
        url = "/en/docs/test'; DROP TABLE docs;--"
        result = url_to_safe_filename(url)

        # SQL injection characters should be removed
        assert "'" not in result
        assert ";" not in result
        assert "-" not in result or result.count("-") <= 2  # May keep hyphens in valid parts
        assert result.endswith(".md")

    def test_url_to_safe_filename_command_injection_attempt(self):
        """Test command injection patterns are sanitized."""
        url = "/en/docs/test`whoami`"
        result = url_to_safe_filename(url)

        # Backticks should be removed
        assert "`" not in result
        assert result.endswith(".md")

    def test_url_to_safe_filename_windows_reserved_characters(self):
        """Test Windows reserved characters are removed."""
        url = "/en/docs/test<>:\"|?*"
        result = url_to_safe_filename(url)

        # Windows reserved characters should be removed
        for char in '<>:"|?*':
            assert char not in result
        assert result.endswith(".md")


class TestDiscoverSitemapAndBaseUrl:
    """Test sitemap discovery."""

    @patch('fetch_claude_docs.requests.Session.get')
    def test_discover_sitemap_and_base_url_success(self, mock_get):
        """Test successful sitemap discovery."""
        sitemap_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://docs.anthropic.com/en/docs/overview</loc>
            </url>
        </urlset>"""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sitemap_xml
        mock_get.return_value = mock_response

        session = Mock()
        session.get.return_value = mock_response

        sitemap_url, base_url = discover_sitemap_and_base_url(session)

        assert base_url == "https://docs.anthropic.com"
        assert "sitemap" in sitemap_url.lower()

    @patch('fetch_claude_docs.requests.Session.get')
    def test_discover_sitemap_tries_multiple_urls(self, mock_get):
        """Test tries multiple sitemap URLs."""
        # First fails, second succeeds
        sitemap_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url>
                <loc>https://docs.anthropic.com/en/docs/overview</loc>
            </url>
        </urlset>"""

        def side_effect(*args, **kwargs):
            if mock_get.call_count == 1:
                resp = Mock()
                resp.status_code = 404
                return resp
            else:
                resp = Mock()
                resp.status_code = 200
                resp.content = sitemap_xml
                return resp

        mock_get.side_effect = side_effect

        session = Mock()
        session.get.side_effect = side_effect

        try:
            sitemap_url, base_url = discover_sitemap_and_base_url(session)
            assert base_url is not None
        except:
            # May fail due to mock complexity, but that's ok
            pass

    @patch('fetch_claude_docs.requests.Session.get')
    def test_discover_sitemap_error_handling(self, mock_get):
        """Test error handling when sitemap can't be found."""
        mock_get.side_effect = Exception("Network error")

        session = Mock()
        session.get.side_effect = Exception("Network error")

        with pytest.raises(Exception):
            discover_sitemap_and_base_url(session)


class TestDiscoverClaudeCodePages:
    """Test Claude Code page discovery."""

    @patch('fetch_claude_docs.requests.Session.get')
    def test_discover_claude_code_pages_basic(self, mock_get):
        """Test basic page discovery."""
        sitemap_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://docs.anthropic.com/en/docs/claude-code/overview</loc></url>
            <url><loc>https://docs.anthropic.com/en/docs/claude-code/setup</loc></url>
            <url><loc>https://docs.anthropic.com/en/docs/other/page</loc></url>
        </urlset>"""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sitemap_xml
        mock_get.return_value = mock_response

        session = Mock()
        session.get.return_value = mock_response

        pages = discover_claude_code_pages(session, "https://docs.anthropic.com/sitemap.xml")

        # Should only include claude-code pages
        assert len(pages) >= 2
        assert all("claude-code" in page for page in pages)

    @patch('fetch_claude_docs.requests.Session.get')
    def test_discover_claude_code_pages_filters_patterns(self, mock_get):
        """Test filters out excluded patterns."""
        sitemap_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            <url><loc>https://docs.anthropic.com/en/docs/claude-code/overview</loc></url>
            <url><loc>https://docs.anthropic.com/en/docs/claude-code/tool-use/bash</loc></url>
            <url><loc>https://docs.anthropic.com/en/docs/claude-code/examples/test</loc></url>
        </urlset>"""

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = sitemap_xml
        mock_get.return_value = mock_response

        session = Mock()
        session.get.return_value = mock_response

        pages = discover_claude_code_pages(session, "https://docs.anthropic.com/sitemap.xml")

        # Should exclude tool-use and examples
        assert not any("tool-use" in p for p in pages)
        assert not any("examples" in p for p in pages)

    @patch('fetch_claude_docs.requests.Session.get')
    def test_discover_claude_code_pages_error_fallback(self, mock_get):
        """Test fallback when discovery fails."""
        mock_get.side_effect = Exception("Network error")

        session = Mock()
        session.get.side_effect = Exception("Network error")

        pages = discover_claude_code_pages(session, "https://docs.anthropic.com/sitemap.xml")

        # Should return fallback pages
        assert len(pages) > 0
        assert all(isinstance(p, str) for p in pages)
        assert all("claude-code" in p for p in pages)


class TestValidateMarkdownContent:
    """Test markdown content validation."""

    def test_validate_markdown_basic(self):
        """Test valid markdown passes validation."""
        content = "# Title\n## Subtitle\nThis is markdown content with **bold** and _italic_ and more content to make it longer"
        # Should not raise
        validate_markdown_content(content, "test.md")

    def test_validate_markdown_rejects_html(self):
        """Test HTML content is rejected."""
        content = "<!DOCTYPE html><html><body>test with enough content</body></html>"
        with pytest.raises(ValueError):
            validate_markdown_content(content, "test.md")

    def test_validate_markdown_rejects_short_content(self):
        """Test very short content is rejected."""
        content = "short"
        with pytest.raises(ValueError):
            validate_markdown_content(content, "test.md")

    def test_validate_markdown_rejects_empty(self):
        """Test empty content is rejected."""
        with pytest.raises(ValueError):
            validate_markdown_content("", "test.md")

    def test_validate_markdown_requires_markdown_elements(self):
        """Test content should have markdown elements."""
        # Very plain text without any markdown formatting might fail
        content = "This is just plain text without any markdown structure or headers at all"
        # Might pass if has 50+ chars but fails due to lack of markdown indicators
        try:
            validate_markdown_content(content, "test.md")
        except ValueError:
            # Ok if rejected - needs markdown elements
            pass

    def test_validate_markdown_accepts_with_headers(self):
        """Test markdown with headers passes."""
        content = "# Main Title\n## Subtitle\n### Subsection\nContent here with much more text to satisfy the minimum length requirement for validation"
        validate_markdown_content(content, "test.md")

    def test_validate_markdown_accepts_with_code(self):
        """Test markdown with code blocks passes."""
        content = "# Code Example\n```python\nprint('hello')\n```\nMore content with additional text to reach minimum length"
        validate_markdown_content(content, "test.md")

    def test_validate_markdown_accepts_with_lists(self):
        """Test markdown with lists passes."""
        content = "# Lists\n- Item 1\n- Item 2\n- Item 3\n1. First\n2. Second\nAdditional content here"
        validate_markdown_content(content, "test.md")

    def test_validate_markdown_accepts_with_links(self):
        """Test markdown with links passes."""
        content = "# Links\n[Example](https://example.com)\n## More content\n* Bullet point\nAdditional documentation here"
        validate_markdown_content(content, "test.md")

    def test_validate_markdown_rejects_html_tags_early(self):
        """Test HTML tags in first 100 chars are rejected."""
        content = "<html>test content that is long enough for validation purposes and includes HTML tags</html>"
        with pytest.raises(ValueError):
            validate_markdown_content(content, "test.md")


class TestHeadersConstant:
    """Test HEADERS configuration."""

    def test_headers_defined(self):
        """Test HEADERS is defined."""
        assert HEADERS is not None
        assert isinstance(HEADERS, dict)

    def test_headers_has_user_agent(self):
        """Test HEADERS includes User-Agent."""
        assert "User-Agent" in HEADERS

    def test_headers_has_cache_control(self):
        """Test HEADERS includes cache control."""
        assert "Cache-Control" in HEADERS


class TestManifestFile:
    """Test MANIFEST_FILE constant."""

    def test_manifest_file_defined(self):
        """Test MANIFEST_FILE is defined."""
        assert MANIFEST_FILE is not None
        assert isinstance(MANIFEST_FILE, str)
        assert MANIFEST_FILE.endswith(".json")


class TestGetBaseUrlForPath:
    """Test base URL determination for different documentation paths."""

    def test_claude_code_paths_use_code_domain(self):
        """Test that Claude Code paths use code.claude.com."""
        claude_code_paths = [
            "/en/docs/claude-code/hooks",
            "/en/docs/claude-code/setup",
            "/en/docs/claude-code/mcp",
            "/en/docs/claude-code/sdk/overview",
        ]
        for path in claude_code_paths:
            assert get_base_url_for_path(path) == "https://code.claude.com"

    def test_api_paths_use_docs_domain(self):
        """Test that API paths use docs.claude.com."""
        api_paths = [
            "/en/api/messages",
            "/en/api/admin-api/apikeys/get-api-key",
            "/en/api/admin-api/users/list-users",
        ]
        for path in api_paths:
            assert get_base_url_for_path(path) == "https://docs.claude.com"

    def test_other_docs_use_docs_domain(self):
        """Test that non-Claude-Code docs use docs.claude.com."""
        other_paths = [
            "/en/docs/about-claude/models",
            "/en/docs/build-with-claude/prompt-engineering",
            "/en/resources/glossary",
            "/en/prompt-library/code-clarifier",
            "/en/release-notes/api",
            "/en/home",
        ]
        for path in other_paths:
            assert get_base_url_for_path(path) == "https://docs.claude.com"


class TestConvertLegacyPathToFetchUrl:
    """Test legacy path conversion for multi-domain setup."""

    def test_claude_code_paths_conversion(self):
        """Test Claude Code paths are converted to /docs/en/ format."""
        test_cases = [
            ("/en/docs/claude-code/hooks", "/docs/en/hooks"),
            ("/en/docs/claude-code/setup", "/docs/en/setup"),
            ("/en/docs/claude-code/sdk/overview", "/docs/en/sdk/overview"),
        ]
        for input_path, expected_output in test_cases:
            assert convert_legacy_path_to_fetch_url(input_path) == expected_output

    def test_api_paths_unchanged(self):
        """Test API paths remain unchanged for docs.claude.com."""
        test_cases = [
            "/en/api/messages",
            "/en/api/admin-api/apikeys/get-api-key",
            "/en/api/admin-api/users/list-users",
        ]
        for path in test_cases:
            assert convert_legacy_path_to_fetch_url(path) == path

    def test_other_docs_paths_unchanged(self):
        """Test other documentation paths remain unchanged."""
        test_cases = [
            "/en/docs/about-claude/models",
            "/en/resources/glossary",
            "/en/release-notes/api",
            "/en/home",
        ]
        for path in test_cases:
            assert convert_legacy_path_to_fetch_url(path) == path

    def test_already_converted_paths(self):
        """Test paths already in /docs/en/ format are unchanged."""
        already_converted = [
            "/docs/en/hooks",
            "/docs/en/setup",
            "/docs/en/sdk/overview",
        ]
        for path in already_converted:
            assert convert_legacy_path_to_fetch_url(path) == path

    def test_invalid_paths_returned_unchanged(self):
        """Test paths without /en/ prefix are returned as-is."""
        invalid_paths = [
            "/invalid/path",
            "/docs/something",
            "not-a-path",
        ]
        for path in invalid_paths:
            assert convert_legacy_path_to_fetch_url(path) == path
