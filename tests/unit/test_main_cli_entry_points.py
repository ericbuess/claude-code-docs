"""Comprehensive tests for main.py CLI entry points and I/O operations."""

import pytest
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, mock_open
from io import StringIO
import requests

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import (
    main,
    save_documentation,
    fetch_page,
    update_documentation,
    FetchStats,
    path_to_filename,
    compute_content_hash
)


class TestMainCLIEntryPoint:
    """Test main() CLI entry point with various argument combinations."""

    def test_main_no_arguments_shows_error(self):
        """Test main() with no arguments shows error."""
        with patch('sys.argv', ['main.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 2  # argparse error code

    def test_main_update_all_success(self, tmp_path):
        """Test main() with --update-all flag."""
        manifest_data = {
            "metadata": {"total_paths": 2, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test1", "/en/docs/test2"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation') as mock_update:
                mock_stats = FetchStats()
                mock_stats.success_count = 2
                mock_update.return_value = mock_stats

                result = main()

                assert result == 0
                mock_update.assert_called_once()

    def test_main_update_category_success(self, tmp_path):
        """Test main() with --update-category flag."""
        manifest_data = {
            "metadata": {"total_paths": 2, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test1"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-category', 'guides',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation') as mock_update:
                mock_stats = FetchStats()
                mock_stats.success_count = 1
                mock_update.return_value = mock_stats

                result = main()

                assert result == 0

    def test_main_verify_mode(self, tmp_path):
        """Test main() with --verify flag."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        docs_manifest_file = tmp_path / "docs_manifest.json"
        docs_manifest_file.write_text(json.dumps({"/en/docs/test": {"hash": "abc"}}))

        with patch('sys.argv', [
            'main.py',
            '--verify',
            '--manifest', str(manifest_file),
            '--docs-manifest', str(docs_manifest_file)
        ]):
            result = main()

            assert result == 0

    def test_main_with_force_flag(self, tmp_path):
        """Test main() with --force flag."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--force',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation') as mock_update:
                mock_stats = FetchStats()
                mock_update.return_value = mock_stats

                result = main()

                # Check force parameter was passed
                call_kwargs = mock_update.call_args[1]
                assert call_kwargs['force'] is True

    def test_main_with_custom_rate_limit(self, tmp_path):
        """Test main() with custom --rate-limit."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--rate-limit', '2.0',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation') as mock_update:
                mock_stats = FetchStats()
                mock_update.return_value = mock_stats

                result = main()

                call_kwargs = mock_update.call_args[1]
                assert call_kwargs['rate_limit'] == 2.0

    def test_main_manifest_not_found(self, tmp_path):
        """Test main() handles missing manifest file."""
        manifest_file = tmp_path / "nonexistent.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--manifest', str(manifest_file)
        ]):
            result = main()

            assert result == 1

    def test_main_invalid_category(self, tmp_path):
        """Test main() handles invalid category."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-category', 'nonexistent',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            result = main()

            assert result == 1

    def test_main_keyboard_interrupt(self, tmp_path):
        """Test main() handles KeyboardInterrupt gracefully."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation', side_effect=KeyboardInterrupt()):
                result = main()

                assert result == 130

    def test_main_with_failures_exits_with_error(self, tmp_path):
        """Test main() exits with error code when there are failures."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation') as mock_update:
                mock_stats = FetchStats()
                mock_stats.failed_count = 1
                mock_update.return_value = mock_stats

                result = main()

                assert result == 1

    def test_main_with_log_level_debug(self, tmp_path):
        """Test main() with DEBUG log level."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        output_dir = tmp_path / "docs"
        docs_manifest = tmp_path / "docs" / "docs_manifest.json"

        with patch('sys.argv', [
            'main.py',
            '--update-all',
            '--log-level', 'DEBUG',
            '--manifest', str(manifest_file),
            '--output-dir', str(output_dir),
            '--docs-manifest', str(docs_manifest)
        ]):
            with patch('main.update_documentation') as mock_update:
                mock_stats = FetchStats()
                mock_update.return_value = mock_stats

                result = main()

                assert result == 0


class TestSaveDocumentation:
    """Test save_documentation() I/O operations."""

    def test_save_documentation_success(self, tmp_path):
        """Test successful file save."""
        content = "# Test\nContent here"
        path = "/en/docs/test"

        result = save_documentation(path, content, tmp_path)

        assert result is True
        saved_file = tmp_path / "en__docs__test.md"
        assert saved_file.exists()
        assert saved_file.read_text() == content

    def test_save_documentation_creates_directory(self, tmp_path):
        """Test creates output directory if needed."""
        output_dir = tmp_path / "new" / "nested" / "dir"
        content = "# Test"
        path = "/en/docs/test"

        result = save_documentation(path, content, output_dir)

        assert result is True
        assert output_dir.exists()

    def test_save_documentation_overwrites_existing(self, tmp_path):
        """Test overwrites existing file."""
        path = "/en/docs/test"
        filename = path_to_filename(path)
        existing_file = tmp_path / filename
        existing_file.write_text("old content")

        new_content = "# New Content"
        result = save_documentation(path, new_content, tmp_path)

        assert result is True
        assert existing_file.read_text() == new_content

    def test_save_documentation_with_unicode(self, tmp_path):
        """Test saves unicode content correctly."""
        content = "# 测试\n中文内容 émojis 🔥"
        path = "/en/docs/unicode-test"

        result = save_documentation(path, content, tmp_path)

        assert result is True
        saved_file = tmp_path / "en__docs__unicode-test.md"
        assert saved_file.read_text(encoding='utf-8') == content

    def test_save_documentation_io_error(self, tmp_path):
        """Test handles I/O errors gracefully."""
        path = "/en/docs/test"
        content = "# Test"

        # Create a directory with the target filename to cause an error
        filename = path_to_filename(path)
        (tmp_path / filename).mkdir()

        result = save_documentation(path, content, tmp_path)

        assert result is False

    def test_save_documentation_permission_error(self):
        """Test handles permission errors."""
        path = "/en/docs/test"
        content = "# Test"
        readonly_dir = Path("/readonly/dir")

        with patch('pathlib.Path.mkdir'):
            with patch('builtins.open', side_effect=PermissionError()):
                result = save_documentation(path, content, readonly_dir)

                assert result is False


class TestFetchPage:
    """Test fetch_page() network I/O operations."""

    def test_fetch_page_success(self):
        """Test successful page fetch."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "# Test Page\nValid markdown content with **formatting** and [links](url)"

        mock_session = Mock()
        mock_session.get.return_value = mock_response

        success, content, error = fetch_page("/en/docs/test", mock_session)

        assert success is True
        assert content is not None
        assert error is None

    def test_fetch_page_not_found(self):
        """Test handles 404 responses."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()

        mock_session = Mock()
        mock_session.get.return_value = mock_response

        success, content, error = fetch_page("/en/docs/nonexistent", mock_session)

        assert success is False
        assert content is None
        assert error == "404 Not Found"

    def test_fetch_page_rate_limited(self):
        """Test handles rate limiting (429)."""
        # First call: rate limited
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_response_429.headers = {'Retry-After': '1'}

        # Second call: success
        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.text = "# Test\nValid markdown **content** with `code` and - lists"

        mock_session = Mock()
        mock_session.get.side_effect = [mock_response_429, mock_response_200]

        with patch('time.sleep'):  # Don't actually sleep in tests
            success, content, error = fetch_page("/en/docs/test", mock_session)

        assert success is True
        assert mock_session.get.call_count == 2

    def test_fetch_page_timeout(self):
        """Test handles timeout errors."""
        mock_session = Mock()
        mock_session.get.side_effect = requests.exceptions.Timeout()

        with patch('time.sleep'):
            success, content, error = fetch_page("/en/docs/test", mock_session)

        assert success is False
        assert error == "Timeout after retries"

    def test_fetch_page_connection_error(self):
        """Test handles connection errors."""
        mock_session = Mock()
        mock_session.get.side_effect = requests.exceptions.ConnectionError("Network error")

        with patch('time.sleep'):
            success, content, error = fetch_page("/en/docs/test", mock_session)

        assert success is False
        assert "Network error" in error

    def test_fetch_page_retries_on_timeout(self):
        """Test retries after timeout."""
        mock_session = Mock()
        mock_session.get.side_effect = requests.exceptions.Timeout()

        with patch('time.sleep'):
            fetch_page("/en/docs/test", mock_session)

        # Should retry MAX_RETRIES times (3 by default)
        assert mock_session.get.call_count == 3

    def test_fetch_page_invalid_content(self):
        """Test rejects invalid content."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<!DOCTYPE html><html>HTML content</html>"

        mock_session = Mock()
        mock_session.get.return_value = mock_response

        success, content, error = fetch_page("/en/docs/test", mock_session)

        assert success is False
        assert error == "Content validation failed"


class TestUpdateDocumentation:
    """Test update_documentation() orchestration function."""

    def test_update_documentation_success(self, tmp_path):
        """Test successful documentation update."""
        paths = ["/en/docs/test"]
        output_dir = tmp_path / "docs"
        manifest_path = tmp_path / "docs_manifest.json"

        with patch('main.fetch_page') as mock_fetch:
            mock_fetch.return_value = (
                True,
                "# Test\nValid markdown **content**",
                None
            )

            stats = update_documentation(
                paths,
                output_dir,
                manifest_path,
                force=False,
                rate_limit=0.1
            )

        assert stats.success_count == 1
        assert stats.failed_count == 0

    def test_update_documentation_skips_unchanged(self, tmp_path):
        """Test skips unchanged content."""
        paths = ["/en/docs/test"]
        output_dir = tmp_path / "docs"
        manifest_path = tmp_path / "docs_manifest.json"

        # Setup existing manifest with hash
        content = "# Test\nContent"
        existing_manifest = {
            "/en/docs/test": {
                "hash": compute_content_hash(content),
                "last_updated": "2024-01-01"
            }
        }
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(existing_manifest))

        with patch('main.fetch_page') as mock_fetch:
            mock_fetch.return_value = (True, content, None)

            stats = update_documentation(
                paths,
                output_dir,
                manifest_path,
                force=False,
                rate_limit=0.1
            )

        assert stats.skipped_count == 1

    def test_update_documentation_force_mode(self, tmp_path):
        """Test force mode re-fetches all pages."""
        paths = ["/en/docs/test"]
        output_dir = tmp_path / "docs"
        manifest_path = tmp_path / "docs_manifest.json"

        # Setup existing manifest
        content = "# Test\nContent"
        existing_manifest = {
            "/en/docs/test": {
                "hash": compute_content_hash(content),
                "last_updated": "2024-01-01"
            }
        }
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(existing_manifest))

        with patch('main.fetch_page') as mock_fetch:
            mock_fetch.return_value = (True, content, None)

            stats = update_documentation(
                paths,
                output_dir,
                manifest_path,
                force=True,  # Force mode
                rate_limit=0.1
            )

        # Should process (not skip) even though unchanged
        assert stats.success_count == 1
        assert stats.skipped_count == 0

    def test_update_documentation_handles_failures(self, tmp_path):
        """Test handles fetch failures."""
        paths = ["/en/docs/test"]
        output_dir = tmp_path / "docs"
        manifest_path = tmp_path / "docs_manifest.json"

        with patch('main.fetch_page') as mock_fetch:
            mock_fetch.return_value = (False, None, "Network error")

            stats = update_documentation(
                paths,
                output_dir,
                manifest_path,
                force=False,
                rate_limit=0.1
            )

        assert stats.failed_count == 1
        assert len(stats.errors) == 1

    def test_update_documentation_updates_manifest(self, tmp_path):
        """Test updates manifest after successful fetch."""
        paths = ["/en/docs/test"]
        output_dir = tmp_path / "docs"
        manifest_path = tmp_path / "docs_manifest.json"

        with patch('main.fetch_page') as mock_fetch:
            content = "# Test\nValid **markdown**"
            mock_fetch.return_value = (True, content, None)

            update_documentation(
                paths,
                output_dir,
                manifest_path,
                force=False,
                rate_limit=0.1
            )

        # Check manifest was saved
        assert manifest_path.exists()
        manifest = json.loads(manifest_path.read_text())
        assert "/en/docs/test" in manifest
        assert "hash" in manifest["/en/docs/test"]

    def test_update_documentation_rate_limiting(self, tmp_path):
        """Test applies rate limiting between requests."""
        paths = ["/en/docs/test1", "/en/docs/test2"]
        output_dir = tmp_path / "docs"
        manifest_path = tmp_path / "docs_manifest.json"

        with patch('main.fetch_page') as mock_fetch:
            mock_fetch.return_value = (True, "# Test\n**Valid**", None)
            with patch('time.sleep') as mock_sleep:
                update_documentation(
                    paths,
                    output_dir,
                    manifest_path,
                    force=False,
                    rate_limit=0.5
                )

                # Should sleep between requests (but not after last one)
                assert mock_sleep.call_count == 1
                mock_sleep.assert_called_with(0.5)
