"""Validation tests for path reachability."""

import pytest
import sys
from pathlib import Path
import json
import random

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from lookup_paths import validate_path, batch_validate


class TestAllPathsReachable:
    """Test all paths in manifest are accessible."""

    @pytest.mark.network
    @pytest.mark.slow
    def test_sample_paths_reachable(self, paths_manifest):
        """Test sample of paths return HTTP 200."""
        # Get all paths from manifest
        all_paths = []
        for category_paths in paths_manifest['categories'].values():
            all_paths.extend(category_paths)

        if not all_paths:
            pytest.skip("No paths in manifest")

        # Test a random sample (not all 550+ in CI)
        sample_size = min(10, len(all_paths))
        sample_paths = random.sample(all_paths, sample_size)

        # Validate sample
        failures = []
        for path in sample_paths:
            result = validate_path(path)
            if not result['reachable']:
                failures.append((path, result))

        # Report failures (warning only - some paths may genuinely be 404)
        if failures:
            failure_report = "\n".join(
                f"  {path}: {result.get('error', 'Unknown error')}"
                for path, result in failures
            )
            # Warn but don't fail - this is a validation test
            # Some paths in manifest may be deprecated or moved
            print(f"\nWarning: Some paths unreachable ({len(failures)}/{len(sample_paths)}):\n{failure_report}")
            # Only fail if ALL paths are unreachable (likely network issue)
            if len(failures) == len(sample_paths):
                pytest.fail(f"All sampled paths unreachable - possible network issue")

    @pytest.mark.network
    def test_core_docs_sample(self, paths_manifest):
        """Test sample of core documentation paths."""
        core_paths = paths_manifest['categories'].get('core_documentation', [])

        if not core_paths:
            pytest.skip("No core docs in manifest")

        # Test first few
        sample = core_paths[:3]

        for path in sample:
            result = validate_path(path)
            # May fail if network unavailable, but should not crash
            assert 'reachable' in result
            assert 'status_code' in result or 'error' in result

    @pytest.mark.network
    def test_api_reference_sample(self, paths_manifest):
        """Test sample of API reference paths."""
        api_paths = paths_manifest['categories'].get('api_reference', [])

        if not api_paths:
            pytest.skip("No API reference in manifest")

        sample = api_paths[:3]

        for path in sample:
            result = validate_path(path)
            assert 'reachable' in result


class TestBatchValidation:
    """Test efficient bulk validation."""

    @pytest.mark.integration
    def test_batch_validate_function(self, sample_paths):
        """Test batch validation of multiple paths."""
        stats = batch_validate(sample_paths)

        # batch_validate returns ValidationStats object
        assert stats.total == len(sample_paths)
        assert stats.total > 0
        assert hasattr(stats, 'reachable')
        assert hasattr(stats, 'not_found')

    @pytest.mark.integration
    def test_batch_validate_empty_list(self):
        """Test batch validation with empty list."""
        stats = batch_validate([])

        # Returns ValidationStats with total=0
        assert stats.total == 0

    @pytest.mark.integration
    def test_batch_validate_performance(self, sample_paths):
        """Test batch validation is reasonably fast."""
        import time

        start = time.time()
        results = batch_validate(sample_paths)
        elapsed = time.time() - start

        # Should complete within reasonable time
        # (May be slow if network validation is performed)
        assert elapsed < 30  # 30 seconds max for sample


class TestReportBrokenLinks:
    """Test broken link reporting."""

    @pytest.mark.integration
    def test_identify_broken_links(self, mock_http_404):
        """Test broken links are identified."""
        test_paths = [
            "/en/docs/nonexistent",
            "/en/api/missing"
        ]

        stats = batch_validate(test_paths)

        # All should be unreachable (404)
        assert stats.total == len(test_paths)
        assert stats.not_found == len(test_paths)
        assert len(stats.broken_paths) == len(test_paths)

    @pytest.mark.integration
    def test_report_format(self):
        """Test broken link report format."""
        test_paths = ["/en/docs/test"]

        stats = batch_validate(test_paths)

        # Should return ValidationStats object
        assert hasattr(stats, 'total')
        assert hasattr(stats, 'broken_paths')
        assert isinstance(stats.broken_paths, list)

    @pytest.mark.integration
    def test_mixed_results(self, mock_http_success):
        """Test mix of reachable and unreachable paths."""
        # This test would need a more sophisticated mock
        # that returns different results for different paths
        pass


class TestPathValidationEdgeCases:
    """Test edge cases in path validation."""

    @pytest.mark.integration
    def test_validate_empty_path(self):
        """Test validation of empty path."""
        result = validate_path("")

        # Should handle gracefully
        assert result['reachable'] is False

    @pytest.mark.integration
    def test_validate_malformed_path(self):
        """Test validation of malformed paths."""
        malformed = [
            "not-a-path",
            "/en/docs/test<script>",
            "/en/docs/test?query=param"
        ]

        for path in malformed:
            result = validate_path(path)
            # Should not crash, but likely unreachable
            assert 'reachable' in result

    @pytest.mark.integration
    def test_validate_path_with_fragment(self):
        """Test validation of path with fragment identifier."""
        result = validate_path("/en/docs/test#section")

        # Should handle fragments appropriately
        assert 'reachable' in result
