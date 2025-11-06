"""Integration tests for GitHub Actions workflow simulation."""

import pytest
import sys
from pathlib import Path
import json
import subprocess

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))


class TestScheduledUpdateWorkflow:
    """Test scheduled update workflow (simulated)."""

    @pytest.mark.integration
    def test_workflow_file_exists(self, project_root):
        """Test update-docs.yml workflow file exists."""
        workflow_file = project_root / ".github" / "workflows" / "update-docs.yml"
        assert workflow_file.exists()

    @pytest.mark.integration
    def test_workflow_syntax_valid(self, project_root):
        """Test workflow file has valid YAML syntax."""
        workflow_file = project_root / ".github" / "workflows" / "update-docs.yml"

        # Try to parse YAML
        import yaml
        try:
            with open(workflow_file) as f:
                workflow_data = yaml.safe_load(f)

            assert workflow_data is not None
            assert 'name' in workflow_data
            # YAML parses 'on:' as True (boolean key)
            assert 'on' in workflow_data or True in workflow_data
        except ImportError:
            # If PyYAML not available, just check file is readable
            content = workflow_file.read_text()
            assert len(content) > 0

    @pytest.mark.integration
    def test_test_workflow_exists(self, project_root):
        """Test test.yml workflow exists."""
        workflow_file = project_root / ".github" / "workflows" / "test.yml"
        assert workflow_file.exists()

    @pytest.mark.integration
    def test_validate_workflow_exists(self, project_root):
        """Test validate.yml workflow exists."""
        workflow_file = project_root / ".github" / "workflows" / "validate.yml"
        assert workflow_file.exists()


class TestManualTrigger:
    """Test manual workflow trigger (workflow_dispatch)."""

    @pytest.mark.integration
    def test_workflow_has_manual_trigger(self, project_root):
        """Test workflow supports manual triggering."""
        workflow_file = project_root / ".github" / "workflows" / "update-docs.yml"
        content = workflow_file.read_text()

        # Check for workflow_dispatch
        assert 'workflow_dispatch' in content


class TestCommitAndPush:
    """Test git commit and push simulation."""

    @pytest.mark.integration
    def test_git_available(self):
        """Test git is available in environment."""
        try:
            result = subprocess.run(
                ['git', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            assert result.returncode == 0
        except FileNotFoundError:
            pytest.skip("git not available")

    @pytest.mark.integration
    def test_repo_is_git_repo(self, project_root):
        """Test current directory is a git repository."""
        git_dir = project_root / ".git"
        assert git_dir.exists()
        assert git_dir.is_dir()

    @pytest.mark.integration
    def test_can_check_git_status(self, project_root):
        """Test can check git status."""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=project_root,
                capture_output=True,
                text=True,
                timeout=5
            )
            # Should succeed (return code 0)
            assert result.returncode == 0
        except FileNotFoundError:
            pytest.skip("git not available")


class TestWorkflowEnvironment:
    """Test workflow environment setup."""

    @pytest.mark.integration
    def test_python_version_file_exists(self, project_root):
        """Test .python-version file exists."""
        python_version_file = project_root / ".python-version"
        assert python_version_file.exists()

    @pytest.mark.integration
    def test_requirements_or_pyproject(self, project_root):
        """Test dependency specification exists."""
        pyproject = project_root / "pyproject.toml"
        requirements = project_root / "scripts" / "requirements.txt"

        # At least one should exist
        assert pyproject.exists() or requirements.exists()

    @pytest.mark.integration
    def test_scripts_are_executable(self, project_root):
        """Test main scripts exist and are readable."""
        scripts = [
            project_root / "scripts" / "main.py",
            project_root / "scripts" / "extract_paths.py",
            project_root / "scripts" / "lookup_paths.py"
        ]

        for script in scripts:
            assert script.exists()
            assert script.is_file()


class TestWorkflowOutputs:
    """Test workflow outputs and artifacts."""

    @pytest.mark.integration
    def test_docs_directory_structure(self, project_root):
        """Test docs directory exists for workflow output."""
        docs_dir = project_root / "docs"
        assert docs_dir.exists()
        assert docs_dir.is_dir()

    @pytest.mark.integration
    def test_manifest_can_be_created(self, tmp_path):
        """Test manifest file can be created as workflow artifact."""
        manifest_path = tmp_path / "paths_manifest.json"

        manifest_data = {
            'metadata': {'total_paths': 0},
            'categories': {}
        }

        manifest_path.write_text(json.dumps(manifest_data, indent=2))

        assert manifest_path.exists()
        loaded = json.loads(manifest_path.read_text())
        assert loaded == manifest_data
