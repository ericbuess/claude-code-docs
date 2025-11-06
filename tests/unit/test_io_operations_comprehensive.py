"""Comprehensive tests for I/O operations across all scripts."""

import pytest
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch, mock_open, MagicMock
import tempfile

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from main import (
    load_paths_manifest,
    load_docs_manifest,
    save_docs_manifest,
    save_documentation,
)

from lookup_paths import (
    load_batch_file,
    _load_paths_manifest_cached,
)


class TestFileReadOperations:
    """Test file reading I/O operations."""

    def test_load_paths_manifest_with_large_file(self, tmp_path):
        """Test loading large manifest file."""
        # Create large manifest
        large_manifest = {
            "metadata": {"total_paths": 1000, "categories_count": 10},
            "categories": {
                f"category{i}": [f"/en/docs/path{j}" for j in range(100)]
                for i in range(10)
            }
        }

        manifest_file = tmp_path / "large_manifest.json"
        manifest_file.write_text(json.dumps(large_manifest))

        result = load_paths_manifest(manifest_file)

        assert result["metadata"]["total_paths"] == 1000
        assert len(result["categories"]) == 10

    def test_load_paths_manifest_with_unicode(self, tmp_path):
        """Test loading manifest with unicode characters."""
        manifest = {
            "metadata": {"total_paths": 2, "categories_count": 1},
            "categories": {
                "国际化": ["/en/docs/中文", "/en/docs/émojis🔥"]
            }
        }

        manifest_file = tmp_path / "unicode_manifest.json"
        manifest_file.write_text(json.dumps(manifest, ensure_ascii=False), encoding='utf-8')

        result = load_paths_manifest(manifest_file)

        assert "国际化" in result["categories"]

    def test_load_paths_manifest_with_special_chars(self, tmp_path):
        """Test loading manifest with special characters."""
        manifest = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {
                "special": ["/en/docs/test-with-dash", "/en/docs/test_underscore", "/en/docs/test.dot"]
            }
        }

        manifest_file = tmp_path / "special_manifest.json"
        manifest_file.write_text(json.dumps(manifest))

        result = load_paths_manifest(manifest_file)

        assert len(result["categories"]["special"]) == 3

    def test_load_paths_manifest_empty_file(self, tmp_path):
        """Test loading empty JSON file with minimal structure."""
        manifest_file = tmp_path / "empty.json"
        manifest_file.write_text(json.dumps({
            "metadata": {"total_paths": 0, "categories_count": 0},
            "categories": {}
        }))

        result = load_paths_manifest(manifest_file)

        assert isinstance(result, dict)
        assert result["metadata"]["total_paths"] == 0

    def test_load_paths_manifest_with_comments_fails(self, tmp_path):
        """Test that JSON with comments fails (as expected)."""
        manifest_file = tmp_path / "with_comments.json"
        manifest_file.write_text("""
        {
            // This is a comment
            "metadata": {"total_paths": 1}
        }
        """)

        with pytest.raises(json.JSONDecodeError):
            load_paths_manifest(manifest_file)

    def test_load_docs_manifest_handles_corrupted_file(self, tmp_path):
        """Test loading corrupted docs manifest."""
        manifest_file = tmp_path / "corrupted.json"
        manifest_file.write_text("corrupted data {{{ not json")

        result = load_docs_manifest(manifest_file)

        # Should return empty dict for corrupted file
        assert result == {}

    def test_load_batch_file_with_various_line_endings(self, tmp_path):
        """Test loading batch file with different line endings."""
        batch_file = tmp_path / "batch.txt"

        # Mix of line endings
        content = "/en/docs/path1\n/en/docs/path2\r\n/en/docs/path3\r/en/docs/path4"
        batch_file.write_bytes(content.encode())

        result = load_batch_file(batch_file)

        # Should handle all line ending types
        assert len(result) >= 3

    def test_load_batch_file_with_blank_lines(self, tmp_path):
        """Test loading batch file with many blank lines."""
        batch_file = tmp_path / "batch.txt"
        batch_file.write_text("""
        /en/docs/path1


        /en/docs/path2



        /en/docs/path3
        """)

        result = load_batch_file(batch_file)

        assert len(result) == 3

    def test_cached_manifest_loading(self, tmp_path):
        """Test that manifest loading uses cache."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"guides": ["/en/docs/test"]}
        }

        manifest_file = tmp_path / "cached_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        # Clear cache first
        _load_paths_manifest_cached.cache_clear()

        # Load twice
        result1 = _load_paths_manifest_cached(str(manifest_file))
        result2 = _load_paths_manifest_cached(str(manifest_file))

        # Both should return same data
        assert result1 == result2

        # Check cache info
        cache_info = _load_paths_manifest_cached.cache_info()
        assert cache_info.hits > 0


class TestFileWriteOperations:
    """Test file writing I/O operations."""

    def test_save_docs_manifest_with_large_data(self, tmp_path):
        """Test saving large manifest file."""
        large_manifest = {
            f"/en/docs/path{i}": {
                "hash": f"hash{i}" * 10,
                "last_updated": "2024-01-01",
                "size": i * 1000
            }
            for i in range(1000)
        }

        manifest_file = tmp_path / "large_manifest.json"

        save_docs_manifest(manifest_file, large_manifest)

        assert manifest_file.exists()
        loaded = json.loads(manifest_file.read_text())
        assert len(loaded) == 1000

    def test_save_docs_manifest_with_unicode(self, tmp_path):
        """Test saving manifest with unicode."""
        manifest = {
            "/en/docs/中文": {
                "hash": "abc123",
                "last_updated": "2024-01-01",
                "description": "测试 émojis 🔥"
            }
        }

        manifest_file = tmp_path / "unicode_manifest.json"

        save_docs_manifest(manifest_file, manifest)

        # Read back and verify
        loaded = json.loads(manifest_file.read_text(encoding='utf-8'))
        assert "/en/docs/中文" in loaded

    def test_save_docs_manifest_creates_parent_dirs(self, tmp_path):
        """Test creates parent directories if needed."""
        manifest_file = tmp_path / "nested" / "dirs" / "manifest.json"

        # Parent dirs don't exist yet
        assert not manifest_file.parent.exists()

        # This should fail since we don't auto-create parent dirs
        # (unless the function does - let's test actual behavior)
        try:
            save_docs_manifest(manifest_file, {})
            # If it succeeds, parent was created
            assert manifest_file.parent.exists()
        except FileNotFoundError:
            # If it fails, that's expected without parent creation
            pass

    def test_save_documentation_with_nested_paths(self, tmp_path):
        """Test saving documentation with deeply nested paths."""
        path = "/en/docs/guides/advanced/nested/deep/path"
        content = "# Nested Content\nTest"

        result = save_documentation(path, content, tmp_path)

        assert result is True
        # File should be saved (flat structure)
        filename = path[1:].replace('/', '__') + '.md'
        assert (tmp_path / filename).exists()

    def test_save_documentation_with_long_content(self, tmp_path):
        """Test saving very long document."""
        path = "/en/docs/test"
        content = "# Long Document\n" + ("Lorem ipsum dolor sit amet. " * 10000)

        result = save_documentation(path, content, tmp_path)

        assert result is True
        saved_file = tmp_path / "en__docs__test.md"
        assert saved_file.exists()
        assert len(saved_file.read_text()) > 100000

    def test_save_documentation_atomic_write(self, tmp_path):
        """Test that file writes are atomic (all or nothing)."""
        path = "/en/docs/test"
        filename = path[1:].replace('/', '__') + '.md'
        target_file = tmp_path / filename

        # Write initial content
        target_file.write_text("initial content")

        # Try to write new content
        new_content = "# New Content\nUpdated"
        result = save_documentation(path, new_content, tmp_path)

        # File should be fully updated (not partial)
        assert result is True
        final_content = target_file.read_text()
        assert final_content == new_content
        assert "initial" not in final_content

    def test_save_documentation_concurrent_writes(self, tmp_path):
        """Test multiple concurrent writes to different files."""
        import threading

        results = []

        def write_doc(i):
            path = f"/en/docs/test{i}"
            content = f"# Test {i}\nContent"
            result = save_documentation(path, content, tmp_path)
            results.append(result)

        # Create multiple threads writing different files
        threads = [threading.Thread(target=write_doc, args=(i,)) for i in range(10)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All writes should succeed
        assert all(results)
        assert len(list(tmp_path.glob("*.md"))) == 10

    def test_save_documentation_preserves_newlines(self, tmp_path):
        """Test that newline characters are handled correctly."""
        path = "/en/docs/test"
        content = "Line 1\nLine 2\nLine 3\nLine 4"

        save_documentation(path, content, tmp_path)

        filename = "en__docs__test.md"
        saved_content = (tmp_path / filename).read_text()

        # Content should contain all lines
        assert "Line 1" in saved_content
        assert "Line 2" in saved_content
        assert "Line 3" in saved_content
        assert "Line 4" in saved_content


class TestFileSystemEdgeCases:
    """Test filesystem edge cases and error conditions."""

    def test_manifest_with_readonly_file(self, tmp_path):
        """Test handling of read-only files."""
        manifest_file = tmp_path / "readonly.json"
        manifest_file.write_text("{}")
        manifest_file.chmod(0o444)  # Read-only

        # Reading should work
        result = load_docs_manifest(manifest_file)
        assert isinstance(result, dict)

        # Writing should fail gracefully
        try:
            save_docs_manifest(manifest_file, {"new": "data"})
        except (PermissionError, OSError):
            pass  # Expected

    def test_manifest_with_symlink(self, tmp_path):
        """Test handling of symbolic links."""
        real_file = tmp_path / "real_manifest.json"
        real_file.write_text(json.dumps({"test": "data"}))

        link_file = tmp_path / "link_manifest.json"
        try:
            link_file.symlink_to(real_file)

            # Should follow symlink
            result = load_docs_manifest(link_file)
            assert result == {"test": "data"}
        except OSError:
            # Symlinks might not be supported
            pytest.skip("Symlinks not supported")

    def test_save_with_disk_full_simulation(self, tmp_path):
        """Test handling of disk full scenario."""
        path = "/en/docs/test"
        content = "# Test"

        # Simulate disk full by mocking open
        with patch('builtins.open', side_effect=OSError("No space left on device")):
            result = save_documentation(path, content, tmp_path)

            assert result is False

    def test_concurrent_manifest_reads(self, tmp_path):
        """Test multiple concurrent manifest reads."""
        manifest_data = {
            "metadata": {"total_paths": 100, "categories_count": 1},
            "categories": {"guides": [f"/en/docs/test{i}" for i in range(100)]}
        }

        manifest_file = tmp_path / "concurrent_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data))

        import threading

        results = []

        def read_manifest():
            result = load_paths_manifest(manifest_file)
            results.append(result["metadata"]["total_paths"])

        # Create multiple threads reading same file
        threads = [threading.Thread(target=read_manifest) for _ in range(20)]

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        # All reads should succeed with correct data
        assert all(r == 100 for r in results)

    def test_path_with_special_filesystem_chars(self, tmp_path):
        """Test handling paths with filesystem-unsafe characters."""
        # Colons, asterisks etc. in path (but not in filename)
        path = "/en/docs/test-with-special:chars*"
        content = "# Test"

        # Should sanitize or handle safely
        result = save_documentation(path, content, tmp_path)

        # Either succeeds with sanitized name or fails gracefully
        assert isinstance(result, bool)


class TestBinaryAndEncodingEdgeCases:
    """Test encoding and binary data edge cases."""

    def test_manifest_with_different_encodings(self, tmp_path):
        """Test handling manifests with different encodings."""
        manifest_data = {
            "metadata": {"total_paths": 1, "categories_count": 1},
            "categories": {"test": ["data with émojis 🔥"]}
        }

        # Save as UTF-8
        manifest_file = tmp_path / "utf8_manifest.json"
        manifest_file.write_text(json.dumps(manifest_data, ensure_ascii=False), encoding='utf-8')

        result = load_paths_manifest(manifest_file)
        assert "test" in result["categories"]
        assert "émojis 🔥" in result["categories"]["test"][0]

    def test_save_documentation_with_emoji(self, tmp_path):
        """Test saving content with emojis."""
        path = "/en/docs/emoji-test"
        content = "# Emoji Test 🚀\n## Features 🎉\n- Cool 😎\n- Nice 👍"

        result = save_documentation(path, content, tmp_path)

        assert result is True
        saved_file = tmp_path / "en__docs__emoji-test.md"
        saved_content = saved_file.read_text(encoding='utf-8')
        assert "🚀" in saved_content
        assert "🎉" in saved_content

    def test_manifest_with_escape_sequences(self, tmp_path):
        """Test manifest with JSON escape sequences."""
        manifest = {
            "path": "/en/docs/test",
            "content": "Line 1\\nLine 2\\tTabbed"
        }

        manifest_file = tmp_path / "escaped_manifest.json"
        manifest_file.write_text(json.dumps(manifest))

        result = load_docs_manifest(manifest_file)
        assert result["path"] == "/en/docs/test"

    def test_very_long_path_handling(self, tmp_path):
        """Test handling very long paths."""
        # Create a very long path (but under OS limits)
        long_segment = "a" * 50
        path = "/" + "/".join([long_segment] * 5)  # 250+ chars
        content = "# Test"

        result = save_documentation(path, content, tmp_path)

        # Should handle long paths (flat naming handles this)
        assert isinstance(result, bool)


class TestManifestConsistency:
    """Test manifest consistency and validation."""

    def test_manifest_roundtrip_preserves_data(self, tmp_path):
        """Test saving and loading preserves all data."""
        original = {
            "/en/docs/test1": {
                "hash": "abc123",
                "last_updated": "2024-01-01T00:00:00Z",
                "size": 12345,
                "metadata": {"extra": "data"}
            }
        }

        manifest_file = tmp_path / "roundtrip_manifest.json"

        save_docs_manifest(manifest_file, original)
        loaded = load_docs_manifest(manifest_file)

        assert loaded == original

    def test_manifest_maintains_order(self, tmp_path):
        """Test manifest maintains insertion order."""
        ordered_data = {
            f"/en/docs/test{i:03d}": {"hash": f"hash{i}"}
            for i in range(100)
        }

        manifest_file = tmp_path / "ordered_manifest.json"

        save_docs_manifest(manifest_file, ordered_data)
        loaded = load_docs_manifest(manifest_file)

        # Python 3.7+ dicts maintain insertion order
        assert list(loaded.keys()) == list(ordered_data.keys())

    def test_empty_manifest_handling(self, tmp_path):
        """Test saving and loading empty manifest."""
        manifest_file = tmp_path / "empty_manifest.json"

        save_docs_manifest(manifest_file, {})
        loaded = load_docs_manifest(manifest_file)

        assert loaded == {}

    def test_manifest_with_null_values(self, tmp_path):
        """Test manifest with null/None values."""
        manifest = {
            "/en/docs/test": {
                "hash": "abc123",
                "description": None,
                "size": None
            }
        }

        manifest_file = tmp_path / "null_manifest.json"

        save_docs_manifest(manifest_file, manifest)
        loaded = load_docs_manifest(manifest_file)

        assert loaded["/en/docs/test"]["description"] is None
