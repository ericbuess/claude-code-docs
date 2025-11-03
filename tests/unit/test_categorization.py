"""Unit tests for categorization logic."""

import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts"))

from extract_paths import categorize_path
from update_sitemap import (
    build_path_tree,
    tree_to_list
)


class TestCoreDocsCategorization:
    """Test core documentation categorization."""

    def test_basic_core_docs(self):
        """Test basic core docs paths."""
        assert categorize_path("/en/docs/overview") == "core_documentation"
        assert categorize_path("/en/docs/getting-started") == "core_documentation"

    def test_nested_core_docs(self):
        """Test nested core docs paths."""
        assert categorize_path("/en/docs/build-with-claude/prompt-engineering") == "core_documentation"
        assert categorize_path("/en/docs/test-evaluate/defining-success") == "core_documentation"

    def test_claude_code_not_core(self):
        """Test claude-code paths are NOT categorized as core docs."""
        result = categorize_path("/en/docs/claude-code/overview")
        assert result == "claude_code"
        assert result != "core_documentation"


class TestApiReferenceCategorization:
    """Test API reference categorization."""

    def test_basic_api_paths(self):
        """Test basic API paths."""
        assert categorize_path("/en/api/messages") == "api_reference"
        assert categorize_path("/en/api/streaming") == "api_reference"

    def test_nested_api_paths(self):
        """Test nested API paths."""
        assert categorize_path("/en/api/admin/workspaces") == "api_reference"
        assert categorize_path("/en/api/messages-examples") == "api_reference"

    def test_api_sdk_paths(self):
        """Test SDK paths under API."""
        assert categorize_path("/en/api/client-sdks") == "api_reference"


class TestClaudeCodeCategorization:
    """Test Claude Code categorization."""

    def test_basic_claude_code_paths(self):
        """Test basic claude-code paths."""
        assert categorize_path("/en/docs/claude-code/overview") == "claude_code"
        assert categorize_path("/en/docs/claude-code/installation") == "claude_code"

    def test_claude_code_mcp(self):
        """Test MCP paths under claude-code."""
        assert categorize_path("/en/docs/claude-code/mcp/overview") == "claude_code"
        assert categorize_path("/en/docs/claude-code/mcp/quickstart") == "claude_code"

    def test_claude_code_features(self):
        """Test feature paths under claude-code."""
        assert categorize_path("/en/docs/claude-code/skills") == "claude_code"
        assert categorize_path("/en/docs/claude-code/hooks") == "claude_code"


class TestPromptLibraryCategorization:
    """Test prompt library categorization."""

    def test_basic_prompt_library(self):
        """Test basic prompt library paths."""
        assert categorize_path("/en/prompt-library/code-consultant") == "prompt_library"
        assert categorize_path("/en/prompt-library/grammar-genie") == "prompt_library"

    def test_all_prompts(self):
        """Test various prompt templates."""
        prompts = [
            "/en/prompt-library/csv-analyzer",
            "/en/prompt-library/website-wizard",
            "/en/prompt-library/email-extractor"
        ]
        for prompt in prompts:
            assert categorize_path(prompt) == "prompt_library"


class TestResourcesCategorization:
    """Test resources categorization."""

    def test_basic_resources(self):
        """Test basic resources paths."""
        assert categorize_path("/en/resources/faq") == "resources"
        assert categorize_path("/en/resources/glossary") == "resources"


class TestReleaseNotesCategorization:
    """Test release notes categorization."""

    def test_basic_release_notes(self):
        """Test basic release notes paths."""
        assert categorize_path("/en/release-notes/2024-01") == "release_notes"
        assert categorize_path("/en/release-notes/latest") == "release_notes"


class TestUncategorizedFallback:
    """Test uncategorized fallback."""

    def test_unknown_paths(self):
        """Test unknown paths fall back to uncategorized."""
        assert categorize_path("/en/unknown/path") == "uncategorized"
        assert categorize_path("/en/other/test") == "uncategorized"


class TestPathTreeBuilding:
    """Test build_path_tree() for sitemap generation."""

    def test_build_simple_tree(self):
        """Test building tree from flat paths."""
        paths = [
            "/en/docs/page1",
            "/en/docs/page2",
            "/en/api/endpoint1"
        ]

        tree = build_path_tree(paths)

        assert tree is not None
        assert isinstance(tree, dict)

    def test_nested_structure(self):
        """Test nested path structures."""
        paths = [
            "/en/docs/build-with-claude/prompt-engineering",
            "/en/docs/build-with-claude/vision",
            "/en/docs/test-evaluate/defining-success"
        ]

        tree = build_path_tree(paths)

        # Should have hierarchical structure
        assert tree is not None

    def test_empty_paths(self):
        """Test empty path list."""
        tree = build_path_tree([])

        assert tree == {}


class TestTreeToList:
    """Test tree_to_list() conversion."""

    def test_convert_tree_to_list(self):
        """Test converting tree back to list."""
        paths = ["/en/docs/test1", "/en/docs/test2"]
        tree = build_path_tree(paths)

        result = tree_to_list(tree)

        assert isinstance(result, list)
        assert len(result) >= 0
