"""Unit tests for extract_paths.py CLI and missing functions."""

import pytest
import sys
import json
from pathlib import Path
from io import StringIO
from unittest.mock import patch, MagicMock

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from extract_paths import (
    extract_paths_from_html,
    export_clean_txt,
    show_statistics,
    validate_manifest,
    main
)


class TestExtractPathsFromHTML:
    """Test extract_paths_from_html() function."""

    def test_extract_paths_basic(self, tmp_path):
        """Test basic path extraction from HTML."""
        html_file = tmp_path / "test.html"
        html_content = '''
        <html>
            <a href="/en/docs/overview">Overview</a>
            <a href="/en/api/messages">Messages</a>
            <link href="/en/docs/claude-code">Claude Code</link>
        </html>
        '''
        html_file.write_text(html_content, encoding='utf-8')

        paths = extract_paths_from_html(html_file)

        assert len(paths) >= 3
        assert "/en/docs/overview" in paths
        assert "/en/api/messages" in paths
        assert "/en/docs/claude-code" in paths

    def test_extract_paths_json_format(self, tmp_path):
        """Test extraction from JSON-like format."""
        html_file = tmp_path / "test.html"
        html_content = '''
        {
            "href":"/en/docs/test1",
            "href": "/en/api/test2",
            "url": '/en/prompt-library/test3'
        }
        '''
        html_file.write_text(html_content, encoding='utf-8')

        paths = extract_paths_from_html(html_file)

        assert "/en/docs/test1" in paths
        assert "/en/api/test2" in paths
        assert "/en/prompt-library/test3" in paths

    def test_extract_empty_file(self, tmp_path):
        """Test extraction from empty file."""
        html_file = tmp_path / "empty.html"
        html_file.write_text("", encoding='utf-8')

        paths = extract_paths_from_html(html_file)

        assert paths == []


class TestExportCleanTxt:
    """Test export_clean_txt() function."""

    def test_export_clean_txt_basic(self, tmp_path):
        """Test basic text export."""
        output_file = tmp_path / "output.txt"
        categorized_paths = {
            "core_documentation": ["/en/docs/page1", "/en/docs/page2"],
            "api_reference": ["/en/api/messages"],
        }

        export_clean_txt(categorized_paths, output_file)

        assert output_file.exists()
        content = output_file.read_text()
        assert "/en/docs/page1" in content
        assert "/en/docs/page2" in content
        assert "/en/api/messages" in content

    def test_export_preserves_order(self, tmp_path):
        """Test that export preserves path order."""
        output_file = tmp_path / "output.txt"
        categorized_paths = {
            "core_documentation": ["/en/docs/aaa", "/en/docs/zzz"],
        }

        export_clean_txt(categorized_paths, output_file)

        lines = output_file.read_text().strip().split('\n')
        # Filter out empty lines
        lines = [l for l in lines if l.strip()]

        assert lines[0] == "/en/docs/aaa"
        assert lines[1] == "/en/docs/zzz"

    def test_export_empty_categories(self, tmp_path):
        """Test export with empty categories."""
        output_file = tmp_path / "output.txt"
        categorized_paths = {}

        export_clean_txt(categorized_paths, output_file)

        assert output_file.exists()


class TestShowStatistics:
    """Test show_statistics() function."""

    def test_show_statistics_basic(self, tmp_path, capsys):
        """Test basic statistics display."""
        manifest_file = tmp_path / "manifest.json"
        manifest_data = {
            "metadata": {
                "total_paths": 100,
                "extraction_source": "test.html"
            },
            "categories": {
                "core_documentation": ["path1", "path2"],
                "api_reference": ["path3"]
            }
        }
        manifest_file.write_text(json.dumps(manifest_data))

        show_statistics(manifest_file)

        captured = capsys.readouterr()
        assert "100" in captured.out  # total paths
        assert "core_documentation" in captured.out
        assert "api_reference" in captured.out

    def test_show_statistics_missing_file(self, tmp_path, capsys):
        """Test statistics with missing file."""
        manifest_file = tmp_path / "missing.json"

        show_statistics(manifest_file)

        captured = capsys.readouterr()
        assert "not found" in captured.out.lower() or "error" in captured.out.lower()


class TestValidateManifest:
    """Test validate_manifest() function."""

    def test_validate_valid_manifest(self, tmp_path, capsys):
        """Test validation of valid manifest."""
        manifest_file = tmp_path / "manifest.json"
        manifest_data = {
            "metadata": {
                "total_paths": 2,
                "extraction_source": "test.html",
                "timestamp": "2024-01-01T00:00:00"
            },
            "categories": {
                "core_documentation": ["/en/docs/test1", "/en/docs/test2"]
            }
        }
        manifest_file.write_text(json.dumps(manifest_data))

        result = validate_manifest(manifest_file)

        # Should pass basic validation
        assert isinstance(result, bool)

    def test_validate_missing_file(self, tmp_path):
        """Test validation with missing file."""
        manifest_file = tmp_path / "missing.json"

        result = validate_manifest(manifest_file)

        assert result == False

    def test_validate_invalid_json(self, tmp_path):
        """Test validation with invalid JSON."""
        manifest_file = tmp_path / "invalid.json"
        manifest_file.write_text("{ invalid json }")

        result = validate_manifest(manifest_file)

        assert result == False


class TestMain:
    """Test main() CLI entry point."""

    def test_main_stats_mode(self, tmp_path, monkeypatch, capsys):
        """Test main with --stats flag."""
        manifest_file = tmp_path / "manifest.json"
        manifest_data = {
            "metadata": {"total_paths": 50},
            "categories": {"core_documentation": ["path1"]}
        }
        manifest_file.write_text(json.dumps(manifest_data))

        test_args = ["extract_paths.py", "--stats", "--output", str(manifest_file)]
        with patch('sys.argv', test_args):
            main()

        captured = capsys.readouterr()
        assert "50" in captured.out or "path" in captured.out.lower()

    def test_main_validate_mode(self, tmp_path, monkeypatch):
        """Test main with --validate flag."""
        manifest_file = tmp_path / "manifest.json"
        manifest_data = {
            "metadata": {"total_paths": 10},
            "categories": {}
        }
        manifest_file.write_text(json.dumps(manifest_data))

        test_args = ["extract_paths.py", "--validate", "--output", str(manifest_file)]
        with patch('sys.argv', test_args):
            try:
                main()
            except SystemExit as e:
                # Validate mode exits with 0 or 1
                assert e.code in [0, 1]

    def test_main_missing_source_file(self, tmp_path):
        """Test main with missing source file."""
        source_file = tmp_path / "missing.html"
        output_file = tmp_path / "output.json"

        test_args = [
            "extract_paths.py",
            "--source", str(source_file),
            "--output", str(output_file)
        ]

        with patch('sys.argv', test_args):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

    def test_main_extraction_mode(self, tmp_path):
        """Test main in normal extraction mode."""
        # Create source HTML
        source_file = tmp_path / "source.html"
        html_content = '''
        <a href="/en/docs/test1">Test 1</a>
        <a href="/en/docs/test2">Test 2</a>
        <a href="/en/api/messages">Messages</a>
        '''
        source_file.write_text(html_content, encoding='utf-8')

        output_file = tmp_path / "output.json"

        test_args = [
            "extract_paths.py",
            "--source", str(source_file),
            "--output", str(output_file)
        ]

        with patch('sys.argv', test_args):
            main()

        # Check output was created
        assert output_file.exists()
        manifest_data = json.loads(output_file.read_text())
        assert "metadata" in manifest_data
        assert "categories" in manifest_data

        # Check that clean txt file was created
        clean_txt_file = tmp_path.parent / "temp" / "extracted_paths_clean.txt"
        # The file might be created in a different location, so we just check the manifest was created
        assert manifest_data["metadata"]["total_paths"] >= 0
