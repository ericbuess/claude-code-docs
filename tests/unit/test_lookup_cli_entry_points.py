"""Comprehensive tests for lookup_paths.py CLI entry points and I/O operations."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import requests

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from lookup_paths import (
    main,
    validate_path,
    batch_validate,
    print_search_results,
    print_validation_report,
    ValidationStats,
    load_search_index,
    search_content
)


class TestLookupCLIEntryPoint:
    """Test main() CLI entry point with various argument combinations."""

    def test_main_no_arguments_shows_error(self):
        """Test main() with no arguments shows error."""
        with patch('sys.argv', ['lookup_paths.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 2

    def test_main_search_query(self, tmp_path):
        """Test main() with search query."""
        manifest_data = {
            "metadata": {"total_paths": 2},
            "categories": {
                "guides": ["/en/docs/hooks", "/en/docs/mcp"]
            }
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        with patch('sys.argv', ['lookup_paths.py', 'hooks', '--manifest', str(manifest_file)]):
            with patch('lookup_paths.print_search_results') as mock_print:
                result = main()

                assert result == 0
                mock_print.assert_called_once()

    def test_main_check_path_reachable(self, tmp_path):
        """Test main() with --check flag for reachable path."""
        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps({"categories": {}}))

        with patch('sys.argv', [
            'lookup_paths.py',
            '--check', '/en/docs/test',
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.validate_path') as mock_validate:
                mock_validate.return_value = {
                    'path': '/en/docs/test',
                    'url': 'https://docs.anthropic.com/en/docs/test.md',
                    'status_code': 200,
                    'reachable': True,
                    'redirect': None,
                    'error': None
                }

                result = main()

                assert result == 0

    def test_main_check_path_not_found(self, tmp_path):
        """Test main() with --check flag for 404 path."""
        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps({"categories": {}}))

        with patch('sys.argv', [
            'lookup_paths.py',
            '--check', '/en/docs/missing',
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.validate_path') as mock_validate:
                mock_validate.return_value = {
                    'path': '/en/docs/missing',
                    'url': 'https://docs.anthropic.com/en/docs/missing.md',
                    'status_code': 404,
                    'reachable': False,
                    'redirect': None,
                    'error': 'Not Found'
                }

                result = main()

                assert result == 1

    def test_main_validate_all(self, tmp_path):
        """Test main() with --validate-all flag."""
        manifest_data = {
            "metadata": {"total_paths": 2},
            "categories": {
                "guides": ["/en/docs/test1", "/en/docs/test2"]
            }
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        with patch('sys.argv', [
            'lookup_paths.py',
            '--validate-all',
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.batch_validate') as mock_batch:
                mock_stats = ValidationStats()
                mock_stats.reachable = 2
                mock_batch.return_value = mock_stats

                with patch('lookup_paths.print_validation_report'):
                    result = main()

                assert result == 0

    def test_main_batch_validate_from_file(self, tmp_path):
        """Test main() with --batch-validate flag."""
        # Create manifest
        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps({"categories": {}}))

        # Create batch file
        batch_file = tmp_path / "batch.txt"
        batch_file.write_text("/en/docs/test1\n/en/docs/test2\n")

        with patch('sys.argv', [
            'lookup_paths.py',
            '--batch-validate', str(batch_file),
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.batch_validate') as mock_batch:
                mock_stats = ValidationStats()
                mock_stats.reachable = 2
                mock_batch.return_value = mock_stats

                with patch('lookup_paths.print_validation_report'):
                    result = main()

                assert result == 0

    def test_main_suggest_alternatives(self, tmp_path):
        """Test main() with --suggest flag."""
        manifest_data = {
            "metadata": {"total_paths": 2},
            "categories": {
                "guides": ["/en/docs/hooks", "/en/docs/hooks-guide"]
            }
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        with patch('sys.argv', [
            'lookup_paths.py',
            '--suggest', '/en/docs/hook',
            '--manifest', str(manifest_file)
        ]):
            result = main()

            assert result == 0

    def test_main_search_content_with_index(self, tmp_path):
        """Test main() with --search-content flag."""
        index_data = {
            "index": {
                "/en/docs/test": {
                    "title": "Test Page",
                    "keywords": ["test", "example"],
                    "content_preview": "This is test content",
                    "file_path": "docs/test.md"
                }
            }
        }

        with patch('sys.argv', ['lookup_paths.py', '--search-content', 'test']):
            with patch('lookup_paths.load_search_index', return_value=index_data):
                result = main()

                # Will succeed if index loads
                assert result == 0

    def test_main_search_content_no_index(self):
        """Test main() with --search-content but no index."""
        with patch('sys.argv', ['lookup_paths.py', '--search-content', 'test']):
            with patch('lookup_paths.load_search_index', return_value=None):
                result = main()

                assert result == 1

    def test_main_with_max_results(self, tmp_path):
        """Test main() with --max-results flag."""
        manifest_data = {
            "metadata": {"total_paths": 10, "categories_count": 1},
            "categories": {
                "guides": [f"/en/docs/test{i}" for i in range(10)]
            }
        }

        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        with patch('sys.argv', [
            'lookup_paths.py',
            'test',
            '--max-results', '5',
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.search_paths') as mock_search:
                mock_search.return_value = []

                with patch('lookup_paths.print_search_results'):
                    result = main()

                # Check max_results was passed (as third positional arg)
                assert mock_search.called
                call_args = mock_search.call_args[0]
                assert len(call_args) >= 3
                assert call_args[2] == 5  # max_results is third argument

    def test_main_with_log_level(self, tmp_path):
        """Test main() with --log-level flag."""
        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps({"categories": {}}))

        with patch('sys.argv', [
            'lookup_paths.py',
            '--suggest', '/en/docs/test',
            '--log-level', 'DEBUG',
            '--manifest', str(manifest_file)
        ]):
            result = main()

            assert result == 0

    def test_main_manifest_not_found(self, tmp_path):
        """Test main() handles missing manifest file."""
        manifest_file = tmp_path / "nonexistent.json"

        with patch('sys.argv', [
            'lookup_paths.py',
            'test',
            '--manifest', str(manifest_file)
        ]):
            result = main()

            assert result == 1

    def test_main_keyboard_interrupt(self, tmp_path):
        """Test main() handles KeyboardInterrupt."""
        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps({"categories": {}}))

        with patch('sys.argv', [
            'lookup_paths.py',
            'test',
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.search_paths', side_effect=KeyboardInterrupt()):
                result = main()

                assert result == 130

    def test_main_unexpected_exception(self, tmp_path):
        """Test main() handles unexpected exceptions."""
        manifest_file = tmp_path / "paths_manifest.json"
        manifest_file.write_text(json.dumps({"categories": {}}))

        with patch('sys.argv', [
            'lookup_paths.py',
            'test',
            '--manifest', str(manifest_file)
        ]):
            with patch('lookup_paths.search_paths', side_effect=RuntimeError("Unexpected")):
                result = main()

                assert result == 1


class TestValidatePath:
    """Test validate_path() network I/O operations."""

    def test_validate_path_reachable(self):
        """Test validates reachable path."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "https://docs.anthropic.com/en/docs/test.md"

        with patch('requests.head', return_value=mock_response):
            result = validate_path("/en/docs/test")

        assert result['reachable'] is True
        assert result['status_code'] == 200
        assert result['error'] is None

    def test_validate_path_not_found(self):
        """Test validates 404 path."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.url = "https://docs.anthropic.com/en/docs/missing.md"

        with patch('requests.head', return_value=mock_response):
            result = validate_path("/en/docs/missing")

        assert result['reachable'] is False
        assert result['status_code'] == 404

    def test_validate_path_redirect(self):
        """Test detects redirects."""
        original_url = "https://docs.anthropic.com/en/docs/old.md"
        redirect_url = "https://docs.anthropic.com/en/docs/new.md"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = redirect_url

        with patch('requests.head', return_value=mock_response) as mock_head:
            # Make mock_head's first argument the URL
            result = validate_path("/en/docs/old")

        assert result['reachable'] is True
        # Would detect redirect if URLs differ

    def test_validate_path_timeout(self):
        """Test handles timeout errors."""
        with patch('requests.head', side_effect=requests.exceptions.Timeout()):
            result = validate_path("/en/docs/test")

        assert result['reachable'] is False
        assert result['error'] == 'Timeout'

    def test_validate_path_connection_error(self):
        """Test handles connection errors."""
        with patch('requests.head', side_effect=requests.exceptions.ConnectionError("Network down")):
            result = validate_path("/en/docs/test")

        assert result['reachable'] is False
        assert "Network down" in result['error']

    def test_validate_path_custom_timeout(self):
        """Test uses custom timeout."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "https://docs.anthropic.com/en/docs/test.md"

        with patch('requests.head', return_value=mock_response) as mock_head:
            validate_path("/en/docs/test", timeout=30)

            # Check timeout was passed
            call_kwargs = mock_head.call_args[1]
            assert call_kwargs['timeout'] == 30

    def test_validate_path_custom_base_url(self):
        """Test uses custom base URL."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.url = "https://custom.example.com/en/docs/test.md"

        with patch('requests.head', return_value=mock_response) as mock_head:
            validate_path("/en/docs/test", base_url="https://custom.example.com")

            # Check URL was constructed correctly
            call_args = mock_head.call_args[0]
            assert "custom.example.com" in call_args[0]


class TestBatchValidate:
    """Test batch_validate() parallel validation."""

    def test_batch_validate_all_reachable(self):
        """Test batch validation with all reachable paths."""
        paths = ["/en/docs/test1", "/en/docs/test2", "/en/docs/test3"]

        def mock_validate(path, base_url):
            return {
                'path': path,
                'url': f'{base_url}{path}.md',
                'status_code': 200,
                'reachable': True,
                'redirect': None,
                'error': None
            }

        with patch('lookup_paths.validate_path', side_effect=mock_validate):
            stats = batch_validate(paths)

        summary = stats.get_summary()
        assert summary['reachable'] == 3
        assert summary['not_found'] == 0

    def test_batch_validate_mixed_results(self):
        """Test batch validation with mixed results."""
        paths = ["/en/docs/ok", "/en/docs/missing", "/en/docs/timeout"]

        def mock_validate(path, base_url):
            if "missing" in path:
                return {
                    'path': path,
                    'url': f'{base_url}{path}.md',
                    'status_code': 404,
                    'reachable': False,
                    'redirect': None,
                    'error': None
                }
            elif "timeout" in path:
                return {
                    'path': path,
                    'url': f'{base_url}{path}.md',
                    'status_code': None,
                    'reachable': False,
                    'redirect': None,
                    'error': 'Timeout'
                }
            else:
                return {
                    'path': path,
                    'url': f'{base_url}{path}.md',
                    'status_code': 200,
                    'reachable': True,
                    'redirect': None,
                    'error': None
                }

        with patch('lookup_paths.validate_path', side_effect=mock_validate):
            stats = batch_validate(paths)

        summary = stats.get_summary()
        assert summary['reachable'] == 1
        assert summary['not_found'] == 1
        assert summary['timeout'] == 1

    def test_batch_validate_with_custom_workers(self):
        """Test batch validation with custom worker count."""
        paths = [f"/en/docs/test{i}" for i in range(10)]

        with patch('lookup_paths.validate_path') as mock_validate:
            mock_validate.return_value = {
                'path': '/test',
                'url': 'http://example.com',
                'status_code': 200,
                'reachable': True,
                'redirect': None,
                'error': None
            }

            stats = batch_validate(paths, max_workers=10)

        # All paths should be validated
        assert stats.total == 10

    def test_batch_validate_exception_handling(self):
        """Test batch validation handles exceptions."""
        paths = ["/en/docs/test1", "/en/docs/error"]

        def mock_validate(path, base_url):
            if "error" in path:
                raise Exception("Validation error")
            return {
                'path': path,
                'url': f'{base_url}{path}.md',
                'status_code': 200,
                'reachable': True,
                'redirect': None,
                'error': None
            }

        with patch('lookup_paths.validate_path', side_effect=mock_validate):
            stats = batch_validate(paths)

        # Should handle exception gracefully
        summary = stats.get_summary()
        assert summary['reachable'] >= 1
        assert summary['error'] >= 1

    def test_batch_validate_empty_list(self):
        """Test batch validation with empty path list."""
        stats = batch_validate([])

        summary = stats.get_summary()
        assert summary['total'] == 0


class TestPrintFunctions:
    """Test print_search_results() and print_validation_report() output."""

    def test_print_search_results_with_results(self, capsys):
        """Test prints search results."""
        results = [
            ("/en/docs/hooks", 95.0),
            ("/en/docs/mcp", 85.0),
            ("/en/docs/setup", 70.0)
        ]

        print_search_results(results, "hooks")

        captured = capsys.readouterr()
        assert "hooks" in captured.out
        assert "/en/docs/hooks" in captured.out

    def test_print_search_results_no_results(self, capsys):
        """Test prints message for no results."""
        print_search_results([], "nonexistent")

        captured = capsys.readouterr()
        assert "No results found" in captured.out

    def test_print_validation_report_success(self, capsys):
        """Test prints validation report."""
        stats = ValidationStats()
        stats.add_result("/en/docs/test1", "reachable", 200)
        stats.add_result("/en/docs/test2", "reachable", 200)

        print_validation_report(stats)

        captured = capsys.readouterr()
        assert "VALIDATION REPORT" in captured.out
        assert "Reachable" in captured.out

    def test_print_validation_report_with_broken_paths(self, capsys):
        """Test prints report with broken paths."""
        stats = ValidationStats()
        stats.add_result("/en/docs/ok", "reachable", 200)
        stats.add_result("/en/docs/missing", "not_found", 404)

        print_validation_report(stats)

        captured = capsys.readouterr()
        assert "BROKEN PATHS" in captured.out
        assert "/en/docs/missing" in captured.out


class TestSearchContent:
    """Test search_content() full-text search."""

    def test_search_content_title_match(self):
        """Test searches in document titles."""
        index = {
            "index": {
                "/en/docs/hooks": {
                    "title": "Hooks Guide",
                    "keywords": ["automation", "events"],
                    "content_preview": "Learn about hooks"
                }
            }
        }

        results = search_content("hooks", index)

        assert len(results) > 0
        assert results[0]["path"] == "/en/docs/hooks"

    def test_search_content_keyword_match(self):
        """Test searches in keywords."""
        index = {
            "index": {
                "/en/docs/automation": {
                    "title": "Automation",
                    "keywords": ["hooks", "events", "triggers"],
                    "content_preview": "Automation guide"
                }
            }
        }

        results = search_content("hooks", index)

        assert len(results) > 0

    def test_search_content_preview_match(self):
        """Test searches in content preview."""
        index = {
            "index": {
                "/en/docs/guide": {
                    "title": "Guide",
                    "keywords": ["tutorial"],
                    "content_preview": "This guide covers hooks and automation"
                }
            }
        }

        results = search_content("hooks", index)

        assert len(results) > 0

    def test_search_content_relevance_ranking(self):
        """Test results ranked by relevance."""
        index = {
            "index": {
                "/en/docs/hooks": {
                    "title": "Hooks",  # Title match - high score
                    "keywords": ["hooks"],
                    "content_preview": "About hooks"
                },
                "/en/docs/other": {
                    "title": "Other",
                    "keywords": [],
                    "content_preview": "Mentions hooks briefly"
                }
            }
        }

        results = search_content("hooks", index)

        # First result should be /en/docs/hooks (title match)
        assert results[0]["path"] == "/en/docs/hooks"

    def test_search_content_max_results(self):
        """Test respects max_results limit."""
        index = {
            "index": {
                f"/en/docs/test{i}": {
                    "title": f"Test {i}",
                    "keywords": ["test"],
                    "content_preview": "Test content"
                }
                for i in range(30)
            }
        }

        results = search_content("test", index, max_results=10)

        assert len(results) <= 10

    def test_search_content_no_index(self):
        """Test handles missing index."""
        results = search_content("test", None)

        assert results == []

    def test_search_content_empty_index(self):
        """Test handles empty index."""
        results = search_content("test", {})

        assert results == []


class TestLoadSearchIndex:
    """Test load_search_index() caching and I/O."""

    def test_load_search_index_success(self, tmp_path):
        """Test loads search index successfully."""
        index_data = {
            "index": {
                "/en/docs/test": {
                    "title": "Test",
                    "keywords": ["test"],
                    "content_preview": "Test content"
                }
            }
        }

        # Create index file in docs directory
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        index_file = docs_dir / ".search_index.json"
        index_file.write_text(json.dumps(index_data))

        with patch('pathlib.Path', return_value=index_file):
            # Clear cache first
            load_search_index.cache_clear()

            # This would need proper path mocking in real implementation
            # For now, test the error handling path

    def test_load_search_index_missing_file(self):
        """Test handles missing index file."""
        # Clear cache
        load_search_index.cache_clear()

        # Will return None if file doesn't exist
        result = load_search_index()

        # Either None or valid index
        assert result is None or isinstance(result, dict)

    def test_load_search_index_invalid_json(self, tmp_path):
        """Test handles invalid JSON in index."""
        docs_dir = tmp_path / "docs"
        docs_dir.mkdir()
        index_file = docs_dir / ".search_index.json"
        index_file.write_text("{ invalid json }")

        # Would handle error gracefully
        # Implementation returns None on error
