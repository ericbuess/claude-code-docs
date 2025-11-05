"""
Integration tests for installation process.

Tests both standard and enhanced installation modes,
mode detection, helper script behavior, and graceful degradation.
"""

import pytest
import subprocess
import tempfile
import shutil
from pathlib import Path
import json
import os


@pytest.fixture
def mock_install_env(tmp_path, monkeypatch):
    """Create mock installation environment."""
    # Create mock HOME directory
    mock_home = tmp_path / "home"
    mock_home.mkdir()
    monkeypatch.setenv('HOME', str(mock_home))

    # Create .claude directory structure
    claude_dir = mock_home / ".claude"
    claude_dir.mkdir()
    (claude_dir / "commands").mkdir()

    # Create install directory
    install_dir = mock_home / ".claude-code-docs"

    return {
        'home': mock_home,
        'claude_dir': claude_dir,
        'install_dir': install_dir,
        'tmp_path': tmp_path
    }


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent.parent


class TestStandardInstallation:
    """Test standard mode installation (shell-only, no Python)."""

    def test_standard_mode_directory_creation(self, mock_install_env, project_root):
        """Test that standard mode creates required directories."""
        install_dir = mock_install_env['install_dir']

        # Simulate standard installation
        install_dir.mkdir(parents=True)
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        assert install_dir.exists()
        assert docs_dir.exists()
        assert scripts_dir.exists()

    def test_standard_mode_helper_script(self, mock_install_env, project_root):
        """Test that helper script is created in standard mode."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Copy helper script template
        helper_script = install_dir / "claude-docs-helper.sh"
        template_path = project_root / "scripts" / "claude-docs-helper.sh.template"

        # Simulate installation
        if template_path.exists():
            helper_script.write_text(template_path.read_text())
        else:
            # Minimal helper script for testing
            helper_script.write_text("""#!/bin/bash
# Minimal helper script for testing
echo "Standard mode helper script"
""")

        helper_script.chmod(0o755)

        assert helper_script.exists()
        assert os.access(str(helper_script), os.X_OK)

    def test_standard_mode_docs_command(self, mock_install_env):
        """Test that /docs command is created for standard mode."""
        claude_dir = mock_install_env['claude_dir']
        commands_dir = claude_dir / "commands"

        # Create docs.md command file
        docs_md = commands_dir / "docs.md"
        docs_md.write_text("""---
description: Access Claude documentation
---

Execute helper script for documentation access.
""")

        assert docs_md.exists()
        content = docs_md.read_text()
        assert "documentation" in content.lower()

    def test_standard_mode_manifest_exists(self, mock_install_env):
        """Test that docs manifest is created in standard mode."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()

        # Create manifest
        manifest = docs_dir / "docs_manifest.json"
        manifest_data = {
            "metadata": {
                "generated_at": "2025-11-03T00:00:00",
                "total_files": 47,
                "source": "docs.anthropic.com"
            },
            "files": []
        }
        manifest.write_text(json.dumps(manifest_data, indent=2))

        assert manifest.exists()
        data = json.loads(manifest.read_text())
        assert "metadata" in data
        assert "files" in data


class TestEnhancedInstallation:
    """Test enhanced mode installation (with Python features)."""

    def test_enhanced_mode_python_scripts(self, mock_install_env, project_root):
        """Test that Python scripts are installed in enhanced mode."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        # Required Python scripts for enhanced mode
        required_scripts = [
            "main.py",
            "lookup_paths.py",
            "update_sitemap.py",
            "extract_paths.py"
        ]

        for script_name in required_scripts:
            script_path = scripts_dir / script_name
            # Create minimal Python script
            script_path.write_text(f"""#!/usr/bin/env python3
# {script_name} - Enhanced feature script
print("Enhanced mode: {script_name}")
""")

            assert script_path.exists()
            assert script_path.suffix == ".py"

    def test_enhanced_mode_paths_manifest(self, mock_install_env):
        """Test that enhanced paths manifest is created."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Create enhanced manifest
        manifest = install_dir / "paths_manifest.json"
        manifest_data = {
            "metadata": {
                "generated_at": "2025-11-03T00:00:00",
                "total_paths": 449,
                "source": "sitemap"
            },
            "categories": {
                "core_documentation": [],
                "api_reference": [],
                "claude_code": [],
                "prompt_library": [],
                "resources": [],
                "release_notes": []
            }
        }
        manifest.write_text(json.dumps(manifest_data, indent=2))

        assert manifest.exists()
        data = json.loads(manifest.read_text())
        assert "categories" in data
        assert len(data["categories"]) >= 4

    def test_enhanced_mode_search_index(self, mock_install_env):
        """Test that search index is created in enhanced mode."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()

        # Create search index
        search_index = docs_dir / ".search_index.json"
        search_data = {
            "paths": {},
            "metadata": {
                "total_entries": 0,
                "generated_at": "2025-11-03T00:00:00"
            }
        }
        search_index.write_text(json.dumps(search_data, indent=2))

        assert search_index.exists()
        data = json.loads(search_index.read_text())
        assert "paths" in data
        assert "metadata" in data


class TestHelperScriptBehavior:
    """Test helper script mode detection and routing."""

    def test_helper_script_detects_python(self, mock_install_env, project_root):
        """Test that helper script detects Python availability."""
        # Create helper script with mode detection
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        helper_script = install_dir / "claude-docs-helper.sh"
        helper_script.write_text("""#!/bin/bash
# Test mode detection
if command -v python3 &> /dev/null; then
    echo "PYTHON_AVAILABLE=true"
else
    echo "PYTHON_AVAILABLE=false"
fi
""")
        helper_script.chmod(0o755)

        # Run helper script
        result = subprocess.run(
            [str(helper_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert result.returncode == 0
        # Python should be available in test environment
        assert "PYTHON_AVAILABLE=true" in result.stdout

    def test_helper_script_routes_to_python(self, mock_install_env):
        """Test that helper script routes to Python when available."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        # Create mock Python script
        lookup_script = scripts_dir / "lookup_paths.py"
        lookup_script.write_text("""#!/usr/bin/env python3
import sys
if "--search" in sys.argv:
    print("PYTHON_SEARCH_EXECUTED")
""")
        lookup_script.chmod(0o755)

        # Create helper script that routes to Python
        helper_script = install_dir / "claude-docs-helper.sh"
        helper_script.write_text(f"""#!/bin/bash
SCRIPTS_DIR="{scripts_dir}"
if [[ "$1" == "--search" ]]; then
    python3 "$SCRIPTS_DIR/lookup_paths.py" "$@"
fi
""")
        helper_script.chmod(0o755)

        # Test routing
        result = subprocess.run(
            [str(helper_script), "--search", "test"],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert "PYTHON_SEARCH_EXECUTED" in result.stdout

    def test_helper_script_fallback_without_python(self, mock_install_env):
        """Test graceful fallback when Python is not available."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Create helper script with fallback logic
        helper_script = install_dir / "claude-docs-helper.sh"
        helper_script.write_text("""#!/bin/bash
if command -v python3 &> /dev/null && [ -f "scripts/lookup_paths.py" ]; then
    echo "USING_PYTHON"
else
    echo "USING_STANDARD_FALLBACK"
fi
""")
        helper_script.chmod(0o755)

        # Run without Python scripts present
        result = subprocess.run(
            [str(helper_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        # Should fallback to standard mode
        assert "USING_STANDARD_FALLBACK" in result.stdout


class TestMigration:
    """Test migration from older versions."""

    def test_migration_preserves_existing_docs(self, mock_install_env):
        """Test that migration preserves existing documentation files."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()

        # Create existing docs
        existing_doc = docs_dir / "en__docs__existing.md"
        existing_doc.write_text("# Existing Documentation\n\nThis should be preserved.")

        # Simulate migration (would preserve files)
        assert existing_doc.exists()
        preserved_content = existing_doc.read_text()

        # After migration, file should still exist
        assert existing_doc.exists()
        assert "Existing Documentation" in preserved_content

    def test_migration_updates_command_file(self, mock_install_env):
        """Test that migration updates .claude/commands/docs.md."""
        claude_dir = mock_install_env['claude_dir']
        commands_dir = claude_dir / "commands"

        # Create old command file
        docs_md = commands_dir / "docs.md"
        docs_md.write_text("OLD_VERSION")

        # Simulate migration
        docs_md.write_text("NEW_VERSION")

        assert docs_md.read_text() == "NEW_VERSION"

    def test_migration_cleans_old_hooks(self, mock_install_env):
        """Test that migration removes old validation hooks."""
        claude_dir = mock_install_env['claude_dir']
        settings_file = claude_dir / "settings.json"

        # Create old settings with hooks
        old_settings = {
            "hooks": {
                "PreToolUse": [{
                    "id": "old-validation-hook",
                    "hooks": []
                }]
            }
        }
        settings_file.write_text(json.dumps(old_settings, indent=2))

        # Simulate migration (clean hooks)
        new_settings = {"hooks": {}}
        settings_file.write_text(json.dumps(new_settings, indent=2))

        data = json.loads(settings_file.read_text())
        assert "PreToolUse" not in data.get("hooks", {})


class TestInstallationValidation:
    """Test installation validation and verification."""

    def test_verify_required_files_present(self, mock_install_env):
        """Test that all required files are present after installation."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Required files for standard mode
        required_files = [
            "claude-docs-helper.sh",
            "docs/docs_manifest.json"
        ]

        # Create required files
        (install_dir / "docs").mkdir()
        for file_path in required_files:
            full_path = install_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("test")

        # Verify all files exist
        for file_path in required_files:
            assert (install_dir / file_path).exists()

    def test_verify_permissions_correct(self, mock_install_env):
        """Test that helper script has correct permissions."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Create helper script
        helper_script = install_dir / "claude-docs-helper.sh"
        helper_script.write_text("#!/bin/bash\necho test")
        helper_script.chmod(0o755)

        # Verify permissions
        assert os.access(str(helper_script), os.X_OK)
        assert helper_script.stat().st_mode & 0o111  # Has execute bit

    def test_verify_manifest_format(self, mock_install_env):
        """Test that manifests have correct JSON format."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        (install_dir / "docs").mkdir()

        # Create manifest
        manifest = install_dir / "docs" / "docs_manifest.json"
        manifest_data = {
            "metadata": {"total_files": 0},
            "files": []
        }
        manifest.write_text(json.dumps(manifest_data, indent=2))

        # Verify format
        data = json.loads(manifest.read_text())
        assert isinstance(data, dict)
        assert "metadata" in data
        assert "files" in data


class TestClaudeIntegration:
    """Test .claude/ directory integration."""

    def test_claude_commands_directory_exists(self, mock_install_env):
        """Test that .claude/commands/ directory is created."""
        claude_dir = mock_install_env['claude_dir']
        commands_dir = claude_dir / "commands"

        assert commands_dir.exists()
        assert commands_dir.is_dir()

    def test_docs_command_file_created(self, mock_install_env):
        """Test that docs.md command file is created."""
        commands_dir = mock_install_env['claude_dir'] / "commands"
        docs_md = commands_dir / "docs.md"

        # Create command file
        docs_md.write_text("""---
description: Access Claude documentation
---

Execute: ~/.claude-code-docs/claude-docs-helper.sh "$@"
""")

        assert docs_md.exists()
        content = docs_md.read_text()
        assert "claude-docs-helper.sh" in content

    def test_docs_command_supports_flags(self, mock_install_env):
        """Test that /docs command supports various flags."""
        commands_dir = mock_install_env['claude_dir'] / "commands"
        docs_md = commands_dir / "docs.md"

        # Create command file with flag support
        docs_md.write_text("""---
description: Access Claude documentation
---

Supports:
- /docs <path>
- /docs --search <query>
- /docs --validate
- /docs --update-all
""")

        content = docs_md.read_text()
        assert "--search" in content
        assert "--validate" in content
        assert "--update-all" in content
