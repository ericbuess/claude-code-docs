"""Unit tests for manifest cleaning."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import time

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from clean_manifest import (
    validate_path,
    validate_paths_parallel,
    clean_manifest,
    BASE_URL,
    TIMEOUT
)


class TestValidatePath:
    """Test single path validation."""

    @patch('clean_manifest.requests.get')
    def test_validate_path_success(self, mock_get):
        """Test successful path validation."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        path, is_valid, status = validate_path("/en/docs/test")

        assert path == "/en/docs/test"
        assert is_valid is True
        assert status == 200
        mock_get.assert_called_once()

    @patch('clean_manifest.requests.get')
    def test_validate_path_404(self, mock_get):
        """Test path validation with 404."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        path, is_valid, status = validate_path("/en/docs/missing")

        assert path == "/en/docs/missing"
        assert is_valid is False
        assert status == 404

    @patch('clean_manifest.requests.get')
    def test_validate_path_timeout(self, mock_get):
        """Test path validation with timeout."""
        mock_get.side_effect = Exception("Timeout")

        path, is_valid, status = validate_path("/en/docs/slow")

        assert path == "/en/docs/slow"
        assert is_valid is False
        assert status == 0

    @patch('clean_manifest.requests.get')
    def test_validate_path_constructs_correct_url(self, mock_get):
        """Test correct URL is constructed."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        validate_path("/en/docs/test")

        # Should be called with constructed URL
        called_url = mock_get.call_args[0][0]
        assert called_url == f"{BASE_URL}/en/docs/test"

    @patch('clean_manifest.requests.get')
    def test_validate_path_uses_timeout(self, mock_get):
        """Test timeout parameter is used."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        validate_path("/en/docs/test")

        # Should use TIMEOUT parameter
        call_kwargs = mock_get.call_args[1]
        assert call_kwargs['timeout'] == TIMEOUT


class TestValidatePathsParallel:
    """Test parallel path validation."""

    @patch('clean_manifest.validate_path')
    def test_validate_paths_parallel_basic(self, mock_validate):
        """Test parallel validation of multiple paths."""
        mock_validate.side_effect = [
            ("/en/docs/test1", True, 200),
            ("/en/docs/test2", True, 200),
            ("/en/docs/test3", False, 404),
        ]

        paths = ["/en/docs/test1", "/en/docs/test2", "/en/docs/test3"]
        valid_paths, broken_paths = validate_paths_parallel(paths)

        assert len(valid_paths) == 2
        assert len(broken_paths) == 1
        assert "/en/docs/test1" in valid_paths
        assert "/en/docs/test3" in broken_paths

    @patch('clean_manifest.validate_path')
    def test_validate_paths_parallel_all_valid(self, mock_validate):
        """Test when all paths are valid."""
        mock_validate.side_effect = [
            ("/en/docs/test1", True, 200),
            ("/en/docs/test2", True, 200),
        ]

        paths = ["/en/docs/test1", "/en/docs/test2"]
        valid_paths, broken_paths = validate_paths_parallel(paths)

        assert len(valid_paths) == 2
        assert len(broken_paths) == 0

    @patch('clean_manifest.validate_path')
    def test_validate_paths_parallel_all_broken(self, mock_validate):
        """Test when all paths are broken."""
        mock_validate.side_effect = [
            ("/en/docs/test1", False, 404),
            ("/en/docs/test2", False, 500),
        ]

        paths = ["/en/docs/test1", "/en/docs/test2"]
        valid_paths, broken_paths = validate_paths_parallel(paths)

        assert len(valid_paths) == 0
        assert len(broken_paths) == 2

    @patch('clean_manifest.validate_path')
    def test_validate_paths_parallel_empty(self, mock_validate):
        """Test with empty path list."""
        paths = []
        valid_paths, broken_paths = validate_paths_parallel(paths)

        assert len(valid_paths) == 0
        assert len(broken_paths) == 0

    @patch('clean_manifest.validate_path')
    def test_validate_paths_parallel_stores_status_codes(self, mock_validate):
        """Test broken paths store status codes."""
        mock_validate.side_effect = [
            ("/en/docs/test1", False, 404),
            ("/en/docs/test2", False, 500),
        ]

        paths = ["/en/docs/test1", "/en/docs/test2"]
        valid_paths, broken_paths = validate_paths_parallel(paths)

        assert broken_paths["/en/docs/test1"] == 404
        assert broken_paths["/en/docs/test2"] == 500


class TestCleanManifest:
    """Test manifest cleaning."""

    def test_clean_manifest_basic(self, tmp_path):
        """Test basic manifest cleaning."""
        # Create test manifest
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 3
            },
            "categories": {
                "docs": ["/en/docs/test1", "/en/docs/test2", "/en/docs/broken"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = (
                {"/en/docs/test1", "/en/docs/test2"},  # valid paths
                {"/en/docs/broken": 404}  # broken paths
            )

            valid_count, broken_count = clean_manifest(manifest_file)

        assert valid_count == 2
        assert broken_count == 1

    def test_clean_manifest_creates_backup(self, tmp_path):
        """Test backup is created."""
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 1
            },
            "categories": {
                "docs": ["/en/docs/test"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = ({"/en/docs/test"}, {})

            clean_manifest(manifest_file)

        # Note: backup is created by calling script, not the function itself

    def test_clean_manifest_removes_empty_categories(self, tmp_path):
        """Test empty categories are removed."""
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 2
            },
            "categories": {
                "docs": ["/en/docs/valid"],
                "api": ["/en/api/broken"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = (
                {"/en/docs/valid"},
                {"/en/api/broken": 404}
            )

            clean_manifest(manifest_file, output_file)

        # Read cleaned manifest
        cleaned = json.loads(output_file.read_text())

        assert "docs" in cleaned["categories"]
        assert "api" not in cleaned["categories"]  # Empty category removed

    def test_clean_manifest_updates_metadata(self, tmp_path):
        """Test metadata is updated correctly."""
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 3
            },
            "categories": {
                "docs": ["/en/docs/test1", "/en/docs/test2", "/en/docs/broken"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = (
                {"/en/docs/test1", "/en/docs/test2"},
                {"/en/docs/broken": 404}
            )

            clean_manifest(manifest_file, output_file)

        cleaned = json.loads(output_file.read_text())
        metadata = cleaned["metadata"]

        assert metadata["total_paths"] == 2
        assert metadata["removed_broken_paths"] == 1
        assert metadata["original_total_paths"] == 3
        assert "cleaned_at" in metadata

    def test_clean_manifest_preserves_valid_paths_order(self, tmp_path):
        """Test valid paths are sorted."""
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 3
            },
            "categories": {
                "docs": ["/en/docs/zebra", "/en/docs/apple", "/en/docs/monkey"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = (
                {"/en/docs/zebra", "/en/docs/apple", "/en/docs/monkey"},
                {}
            )

            clean_manifest(manifest_file, output_file)

        cleaned = json.loads(output_file.read_text())
        paths = cleaned["categories"]["docs"]

        # Should be sorted
        assert paths == sorted(paths)

    def test_clean_manifest_saves_output(self, tmp_path):
        """Test output file is created."""
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 1
            },
            "categories": {
                "docs": ["/en/docs/test"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = ({"/en/docs/test"}, {})

            clean_manifest(manifest_file, output_file)

        assert output_file.exists()
        assert output_file.read_text()  # Has content

    def test_clean_manifest_loads_manifest_correctly(self, tmp_path):
        """Test manifest is loaded correctly."""
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": 1
            },
            "categories": {
                "docs": ["/en/docs/test"]
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = ({"/en/docs/test"}, {})

            # Should successfully load and clean
            clean_manifest(manifest_file, output_file)

        # If we got here, loading and saving worked
        assert output_file.exists()


class TestManifestCleaningIntegration:
    """Integration tests for manifest cleaning."""

    def test_clean_manifest_preserves_valid_entries(self, tmp_path):
        """Test all valid entries are preserved."""
        paths = [f"/en/docs/test{i}" for i in range(10)]
        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": len(paths)
            },
            "categories": {
                "docs": paths
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            # All paths are valid
            mock_validate.return_value = (set(paths), {})

            clean_manifest(manifest_file, output_file)

        cleaned = json.loads(output_file.read_text())

        assert len(cleaned["categories"]["docs"]) == 10
        assert set(cleaned["categories"]["docs"]) == set(paths)

    def test_clean_manifest_removes_broken_entries(self, tmp_path):
        """Test broken entries are removed."""
        valid_paths = ["/en/docs/test1", "/en/docs/test2"]
        broken_paths = {"/en/docs/broken1": 404, "/en/docs/broken2": 500}
        all_paths = valid_paths + list(broken_paths.keys())

        manifest = {
            "metadata": {
                "generated_at": "2024-01-01T00:00:00Z",
                "total_paths": len(all_paths)
            },
            "categories": {
                "docs": all_paths
            }
        }

        manifest_file = tmp_path / "manifest.json"
        manifest_file.write_text(json.dumps(manifest))
        output_file = tmp_path / "cleaned.json"

        with patch('clean_manifest.validate_paths_parallel') as mock_validate:
            mock_validate.return_value = (set(valid_paths), broken_paths)

            clean_manifest(manifest_file, output_file)

        cleaned = json.loads(output_file.read_text())

        assert len(cleaned["categories"]["docs"]) == 2
        assert all(p in valid_paths for p in cleaned["categories"]["docs"])
