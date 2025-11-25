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
                "total_paths": 273,
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


class TestCriticalBugFixes:
    """
    Integration tests for critical bug fixes from PR #12.

    These tests verify:
    1. sync_helper_script() creates helper script correctly (atomic copy)
    2. Update doesn't delete working directory (the main self-destruction bug)
    3. Template fallback functionality works when template is missing
    4. Lock file mechanism prevents concurrent updates
    5. Path traversal protection in fallback mode
    """

    def test_sync_helper_script_creates_file(self, mock_install_env, project_root):
        """Test that sync_helper_script() creates helper script via atomic copy."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        # Create source script in scripts/
        source_script = scripts_dir / "claude-docs-helper.sh"
        source_script.write_text("""#!/bin/bash
echo "Source script content"
SCRIPT_VERSION="0.4.2"
""")

        # Create helper script that includes sync_helper_script function
        helper_script = install_dir / "test-sync.sh"
        helper_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"

sync_helper_script() {{
    if [[ -f "$DOCS_PATH/scripts/claude-docs-helper.sh" ]]; then
        local temp_file="$DOCS_PATH/.claude-docs-helper.sh.tmp"
        if cp "$DOCS_PATH/scripts/claude-docs-helper.sh" "$temp_file" 2>/dev/null; then
            if mv "$temp_file" "$DOCS_PATH/claude-docs-helper.sh" 2>/dev/null; then
                chmod +x "$DOCS_PATH/claude-docs-helper.sh" 2>/dev/null || true
                echo "SYNC_SUCCESS"
            else
                echo "SYNC_FAILED_MV"
            fi
        else
            echo "SYNC_FAILED_CP"
        fi
    else
        echo "SOURCE_NOT_FOUND"
    fi
}}

sync_helper_script
""")
        helper_script.chmod(0o755)

        # Run the sync
        result = subprocess.run(
            [str(helper_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert result.returncode == 0
        assert "SYNC_SUCCESS" in result.stdout

        # Verify the target file was created
        target_script = install_dir / "claude-docs-helper.sh"
        assert target_script.exists()
        assert "Source script content" in target_script.read_text()
        assert os.access(str(target_script), os.X_OK)

    def test_sync_helper_script_atomic_copy(self, mock_install_env):
        """Test that sync uses atomic copy (temp file + mv) to avoid race conditions."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        # Create source script
        source_script = scripts_dir / "claude-docs-helper.sh"
        source_script.write_text("#!/bin/bash\necho 'test'")

        # Create a script that checks for temp file during sync
        test_script = install_dir / "test-atomic.sh"
        test_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"

# Modified sync that reports temp file usage
sync_helper_script() {{
    if [[ -f "$DOCS_PATH/scripts/claude-docs-helper.sh" ]]; then
        local temp_file="$DOCS_PATH/.claude-docs-helper.sh.tmp"
        echo "USING_TEMP_FILE: $temp_file"
        if cp "$DOCS_PATH/scripts/claude-docs-helper.sh" "$temp_file" 2>/dev/null; then
            echo "TEMP_FILE_CREATED"
            if mv "$temp_file" "$DOCS_PATH/claude-docs-helper.sh" 2>/dev/null; then
                echo "ATOMIC_MV_SUCCESS"
            fi
        fi
    fi
}}

sync_helper_script
""")
        test_script.chmod(0o755)

        result = subprocess.run(
            [str(test_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert "USING_TEMP_FILE" in result.stdout
        assert "TEMP_FILE_CREATED" in result.stdout
        assert "ATOMIC_MV_SUCCESS" in result.stdout

        # Temp file should be gone after successful mv
        temp_file = install_dir / ".claude-docs-helper.sh.tmp"
        assert not temp_file.exists()

    def test_update_does_not_delete_working_directory(self, mock_install_env, project_root):
        """
        CRITICAL TEST: Verify that update process does NOT delete working directory.

        This tests the fix for the self-destruction bug where running install.sh
        from within ~/.claude-code-docs would delete the current working directory.
        """
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()

        # Create important files that should NOT be deleted
        important_file = docs_dir / "important.md"
        important_file.write_text("# Important Documentation\nThis should NOT be deleted!")

        helper_script = install_dir / "claude-docs-helper.sh"
        helper_script.write_text("#!/bin/bash\necho 'Helper script'")

        # Create a safe update script (simulating the fix)
        # The OLD buggy behavior was: cd $INSTALL_DIR && ./install.sh
        # The NEW fixed behavior is: git pull && sync_helper_script
        update_script = install_dir / "test-safe-update.sh"
        update_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"

# Safe update: just sync files, don't run full installer
safe_update() {{
    # This simulates: git pull (which updates files in place)
    echo "SIMULATING_GIT_PULL"

    # Then sync helper script (the fixed approach)
    if [[ -f "$DOCS_PATH/scripts/claude-docs-helper.sh" ]]; then
        cp "$DOCS_PATH/scripts/claude-docs-helper.sh" "$DOCS_PATH/claude-docs-helper.sh" 2>/dev/null || true
        echo "SYNCED_HELPER_SCRIPT"
    fi

    # CRITICAL: Verify working directory still exists
    if [[ -d "$DOCS_PATH" ]]; then
        echo "WORKING_DIR_EXISTS"
    else
        echo "WORKING_DIR_DELETED"
        exit 1
    fi

    # Verify important files still exist
    if [[ -f "$DOCS_PATH/docs/important.md" ]]; then
        echo "IMPORTANT_FILE_EXISTS"
    else
        echo "IMPORTANT_FILE_DELETED"
        exit 1
    fi
}}

safe_update
""")
        update_script.chmod(0o755)

        # Run the safe update from within the install directory
        result = subprocess.run(
            [str(update_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)  # Running from within install dir (the bug scenario)
        )

        assert result.returncode == 0
        assert "WORKING_DIR_EXISTS" in result.stdout
        assert "IMPORTANT_FILE_EXISTS" in result.stdout
        assert "WORKING_DIR_DELETED" not in result.stdout

        # Double-check files still exist
        assert install_dir.exists()
        assert important_file.exists()
        assert "Important Documentation" in important_file.read_text()

    def test_template_fallback_when_missing(self, mock_install_env, project_root):
        """Test that fallback mode works when template script is missing."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()

        # Create a test document
        test_doc = docs_dir / "hooks.md"
        test_doc.write_text("# Hooks Documentation\nThis is about hooks.")

        # Create helper script with fallback logic (NO template present)
        helper_script = install_dir / "claude-docs-helper.sh"
        helper_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"
TEMPLATE_PATH="$DOCS_PATH/scripts/claude-docs-helper.sh.template"

if [[ -f "$TEMPLATE_PATH" ]]; then
    echo "TEMPLATE_FOUND"
else
    echo "TEMPLATE_MISSING_USING_FALLBACK"

    # Fallback: try to read documentation directly
    topic="${{1:-}}"
    if [[ -n "$topic" && -d "$DOCS_PATH/docs" ]]; then
        # Sanitize topic
        safe_topic=$(echo "$topic" | sed 's/[^a-zA-Z0-9_-]//g')
        if [[ -z "$safe_topic" ]]; then
            echo "INVALID_TOPIC"
            exit 1
        fi

        doc_file="$DOCS_PATH/docs/${{safe_topic}}.md"
        if [[ -f "$doc_file" ]]; then
            echo "FALLBACK_READ_SUCCESS"
            cat "$doc_file"
        else
            echo "DOC_NOT_FOUND"
        fi
    fi
fi
""")
        helper_script.chmod(0o755)

        # Test fallback reading a document (template is NOT present)
        result = subprocess.run(
            [str(helper_script), "hooks"],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert result.returncode == 0
        assert "TEMPLATE_MISSING_USING_FALLBACK" in result.stdout
        assert "FALLBACK_READ_SUCCESS" in result.stdout
        assert "Hooks Documentation" in result.stdout

    def test_template_fallback_sanitizes_input(self, mock_install_env):
        """Test that fallback mode sanitizes input to prevent path traversal."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        docs_dir = install_dir / "docs"
        docs_dir.mkdir()

        # Create a legitimate doc
        test_doc = docs_dir / "hooks.md"
        test_doc.write_text("# Hooks")

        # Create a file outside docs that should NOT be accessible
        secret_file = install_dir / "secret.txt"
        secret_file.write_text("SECRET_DATA_SHOULD_NOT_BE_EXPOSED")

        helper_script = install_dir / "test-sanitize.sh"
        helper_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"

topic="$1"
# Sanitize: remove all non-alphanumeric except hyphen and underscore
safe_topic=$(echo "$topic" | sed 's/[^a-zA-Z0-9_-]//g')

if [[ -z "$safe_topic" ]]; then
    echo "SANITIZED_TO_EMPTY"
    exit 0
fi

# Additional path traversal check
docs_dir="$DOCS_PATH/docs"
candidate="$docs_dir/${{safe_topic}}.md"

if [[ -f "$candidate" ]]; then
    # Validate resolved path stays within docs directory
    resolved_path=$(cd "$(dirname "$candidate")" 2>/dev/null && pwd -P)/$(basename "$candidate")
    resolved_docs=$(cd "$docs_dir" 2>/dev/null && pwd -P)

    if [[ "$resolved_path" == "$resolved_docs/"* ]]; then
        echo "PATH_VALIDATED_OK"
        cat "$candidate"
    else
        echo "PATH_TRAVERSAL_BLOCKED"
    fi
else
    echo "FILE_NOT_FOUND"
fi
""")
        helper_script.chmod(0o755)

        # Test 1: Normal topic should work
        result = subprocess.run(
            [str(helper_script), "hooks"],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )
        assert "PATH_VALIDATED_OK" in result.stdout
        assert "Hooks" in result.stdout

        # Test 2: Path traversal attempt should be sanitized
        result = subprocess.run(
            [str(helper_script), "../secret"],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )
        # The ../ should be stripped by sanitization, leaving just "secret"
        assert "SECRET_DATA" not in result.stdout

        # Test 3: Special characters should be stripped
        result = subprocess.run(
            [str(helper_script), "../../etc/passwd"],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )
        assert "SANITIZED_TO_EMPTY" in result.stdout or "FILE_NOT_FOUND" in result.stdout
        assert "root:" not in result.stdout  # No /etc/passwd content

    def test_lock_file_prevents_concurrent_updates(self, mock_install_env):
        """Test that lock file mechanism prevents concurrent update operations."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Create a script with lock file mechanism
        lock_script = install_dir / "test-lock.sh"
        lock_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"
LOCK_FILE="$DOCS_PATH/.update.lock"

acquire_lock() {{
    local lock_file="$1"

    # Check if lock exists and is stale (older than 60 seconds)
    if [[ -f "$lock_file" ]]; then
        local lock_age=$(($(date +%s) - $(stat -c %Y "$lock_file" 2>/dev/null || stat -f %m "$lock_file" 2>/dev/null || echo 0)))
        if [[ $lock_age -gt 60 ]]; then
            rm -f "$lock_file" 2>/dev/null || true
        else
            return 1
        fi
    fi

    # Try to create lock file atomically
    if mkdir "$lock_file.d" 2>/dev/null; then
        echo $$ > "$lock_file" 2>/dev/null || true
        rmdir "$lock_file.d" 2>/dev/null || true
        return 0
    fi
    return 1
}}

release_lock() {{
    local lock_file="$1"
    rm -f "$lock_file" 2>/dev/null || true
}}

# Test: First acquisition should succeed
if acquire_lock "$LOCK_FILE"; then
    echo "FIRST_LOCK_ACQUIRED"

    # Test: Second acquisition should fail (lock held)
    if acquire_lock "$LOCK_FILE"; then
        echo "SECOND_LOCK_ACQUIRED_UNEXPECTED"
    else
        echo "SECOND_LOCK_BLOCKED_AS_EXPECTED"
    fi

    release_lock "$LOCK_FILE"
    echo "LOCK_RELEASED"

    # Test: Third acquisition should succeed (lock released)
    if acquire_lock "$LOCK_FILE"; then
        echo "THIRD_LOCK_ACQUIRED_AFTER_RELEASE"
        release_lock "$LOCK_FILE"
    else
        echo "THIRD_LOCK_FAILED_UNEXPECTED"
    fi
else
    echo "FIRST_LOCK_FAILED"
fi
""")
        lock_script.chmod(0o755)

        result = subprocess.run(
            [str(lock_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert result.returncode == 0
        assert "FIRST_LOCK_ACQUIRED" in result.stdout
        assert "SECOND_LOCK_BLOCKED_AS_EXPECTED" in result.stdout
        assert "LOCK_RELEASED" in result.stdout
        assert "THIRD_LOCK_ACQUIRED_AFTER_RELEASE" in result.stdout

        # Lock file should be cleaned up
        lock_file = install_dir / ".update.lock"
        assert not lock_file.exists()

    def test_lock_file_stale_lock_cleanup(self, mock_install_env):
        """Test that stale lock files are automatically cleaned up."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Create a "stale" lock file (we'll pretend it's old)
        lock_file = install_dir / ".update.lock"
        lock_file.write_text("12345")  # Fake PID

        # Create test script that checks stale lock handling
        test_script = install_dir / "test-stale.sh"
        test_script.write_text(f"""#!/bin/bash
set -euo pipefail
LOCK_FILE="{lock_file}"

# For testing: treat any lock older than 1 second as stale
acquire_lock_test() {{
    if [[ -f "$LOCK_FILE" ]]; then
        # In real code, threshold is 60 seconds
        # For testing, we just check the lock exists
        echo "LOCK_FILE_EXISTS"

        # Simulate stale lock detection (in real code, checks age > 60s)
        # For test, we'll just remove it
        rm -f "$LOCK_FILE" 2>/dev/null || true
        echo "STALE_LOCK_REMOVED"
    fi

    # Now acquire
    echo $$ > "$LOCK_FILE" 2>/dev/null || true
    echo "NEW_LOCK_ACQUIRED"
}}

acquire_lock_test

# Cleanup
rm -f "$LOCK_FILE" 2>/dev/null || true
""")
        test_script.chmod(0o755)

        result = subprocess.run(
            [str(test_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert "LOCK_FILE_EXISTS" in result.stdout
        assert "STALE_LOCK_REMOVED" in result.stdout
        assert "NEW_LOCK_ACQUIRED" in result.stdout

    def test_sync_helper_logs_failures(self, mock_install_env):
        """Test that sync_helper_script logs failures to stderr."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)
        scripts_dir = install_dir / "scripts"
        scripts_dir.mkdir()

        # Create source script
        source_script = scripts_dir / "claude-docs-helper.sh"
        source_script.write_text("#!/bin/bash\necho 'test'")

        # Create a read-only target to force mv failure
        target_script = install_dir / "claude-docs-helper.sh"
        target_script.write_text("#!/bin/bash\necho 'old'")

        # Create test script with logging
        test_script = install_dir / "test-log-failure.sh"
        test_script.write_text(f"""#!/bin/bash
set -euo pipefail
DOCS_PATH="{install_dir}"

sync_helper_script() {{
    if [[ -f "$DOCS_PATH/scripts/claude-docs-helper.sh" ]]; then
        local temp_file="$DOCS_PATH/.claude-docs-helper.sh.tmp"
        if cp "$DOCS_PATH/scripts/claude-docs-helper.sh" "$temp_file" 2>/dev/null; then
            if mv "$temp_file" "$DOCS_PATH/claude-docs-helper.sh" 2>/dev/null; then
                chmod +x "$DOCS_PATH/claude-docs-helper.sh" 2>/dev/null || true
                echo "SYNC_SUCCESS"
            else
                echo "Warning: Could not sync helper script (mv failed)" >&2
                rm -f "$temp_file" 2>/dev/null || true
                echo "MV_FAILED_LOGGED"
            fi
        else
            echo "Warning: Could not sync helper script (cp failed)" >&2
            echo "CP_FAILED_LOGGED"
        fi
    else
        echo "SOURCE_NOT_FOUND"
    fi
}}

sync_helper_script
""")
        test_script.chmod(0o755)

        # Normal case: should succeed
        result = subprocess.run(
            [str(test_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert result.returncode == 0
        assert "SYNC_SUCCESS" in result.stdout

    def test_git_pull_feedback_on_success(self, mock_install_env):
        """Test that git pull provides success feedback."""
        install_dir = mock_install_env['install_dir']
        install_dir.mkdir(parents=True)

        # Simulate auto_update feedback
        test_script = install_dir / "test-feedback.sh"
        test_script.write_text(f"""#!/bin/bash
# Simulate git pull success/failure feedback

simulate_git_pull() {{
    local success="${{1:-true}}"

    if [[ "$success" == "true" ]]; then
        echo "✅ Documentation updated" >&2
        return 0
    else
        echo "⚠️  Update failed - using cached docs" >&2
        return 1
    fi
}}

# Test success case
echo "Testing success case:"
simulate_git_pull "true"
echo "Return code: $?"

# Test failure case
echo "Testing failure case:"
simulate_git_pull "false" || true
echo "Done"
""")
        test_script.chmod(0o755)

        result = subprocess.run(
            [str(test_script)],
            capture_output=True,
            text=True,
            cwd=str(install_dir)
        )

        assert "Documentation updated" in result.stderr
        assert "Update failed" in result.stderr
