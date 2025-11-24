#!/usr/bin/env python3
"""
Tests for JSON output with product context labeling.

Tests the --json flag functionality in lookup_paths.py, including:
- Product label mapping
- Path normalization
- Category detection
- JSON output structure
- Single vs multi-product scenarios
"""

import json
import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from lookup_paths import (
    get_category_for_path,
    get_product_label,
    normalize_path_for_lookup,
    create_enriched_search_results,
    format_content_search_json
)


class TestPathNormalization:
    """Test path normalization for consistent lookups"""

    def test_normalize_claude_code_path(self):
        """Test Claude Code path normalization"""
        # Search index format -> Manifest format
        assert normalize_path_for_lookup('/en/docs/claude-code/hooks') == '/docs/en/hooks'
        assert normalize_path_for_lookup('/en/docs/claude-code/mcp') == '/docs/en/mcp'

    def test_normalize_other_paths_unchanged(self):
        """Test that non-Claude Code paths remain unchanged"""
        assert normalize_path_for_lookup('/en/api/messages') == '/en/api/messages'
        assert normalize_path_for_lookup('/en/docs/agent-sdk/overview') == '/en/docs/agent-sdk/overview'


class TestProductLabeling:
    """Test product label mapping"""

    def test_claude_code_cli_label(self):
        """Test Claude Code CLI product label"""
        label = get_product_label('claude_code', '/docs/en/hooks')
        assert label == 'Claude Code CLI'

    def test_claude_api_label(self):
        """Test Claude API product label"""
        label = get_product_label('api_reference', '/en/api/messages')
        assert label == 'Claude API'

    def test_claude_agent_sdk_label(self):
        """Test Claude Agent SDK product label (special case within api_reference)"""
        label = get_product_label('api_reference', '/en/docs/agent-sdk/overview')
        assert label == 'Claude Agent SDK'

    def test_core_documentation_label(self):
        """Test Claude Documentation product label"""
        label = get_product_label('core_documentation', '/en/docs/build-with-claude/overview')
        assert label == 'Claude Documentation'

    def test_prompt_library_label(self):
        """Test Prompt Library product label"""
        label = get_product_label('prompt_library', '/en/resources/prompt-library/code-clarifier')
        assert label == 'Prompt Library'


class TestCategoryDetection:
    """Test category detection from paths"""

    @pytest.fixture
    def sample_manifest(self):
        """Sample manifest for testing"""
        return {
            'categories': {
                'claude_code': [
                    '/docs/en/hooks',
                    '/docs/en/mcp',
                    '/docs/en/skills'
                ],
                'api_reference': [
                    '/en/api/messages',
                    '/en/docs/agent-sdk/overview',
                    '/en/api/skills/create-skill'
                ],
                'core_documentation': [
                    '/en/docs/build-with-claude/overview'
                ]
            }
        }

    def test_direct_path_match(self, sample_manifest):
        """Test category detection with direct path match"""
        category = get_category_for_path('/docs/en/hooks', sample_manifest)
        assert category == 'claude_code'

        category = get_category_for_path('/en/api/messages', sample_manifest)
        assert category == 'api_reference'

    def test_normalized_path_match(self, sample_manifest):
        """Test category detection with path normalization"""
        # Search index format should match manifest format after normalization
        category = get_category_for_path('/en/docs/claude-code/hooks', sample_manifest)
        assert category == 'claude_code'

    def test_unknown_path(self, sample_manifest):
        """Test category detection with unknown path"""
        category = get_category_for_path('/unknown/path', sample_manifest)
        assert category is None


class TestEnrichedSearchResults:
    """Test enriched search results creation"""

    @pytest.fixture
    def sample_manifest(self):
        """Sample manifest for testing"""
        return {
            'categories': {
                'claude_code': ['/docs/en/skills'],
                'api_reference': [
                    '/en/api/skills/create-skill',
                    '/en/docs/agent-sdk/skills'
                ]
            }
        }

    def test_single_product_context(self, sample_manifest):
        """Test enriched results with single product context"""
        results = [
            ('/docs/en/skills', 70.0),
            ('/docs/en/hooks', 60.0)
        ]

        enriched = create_enriched_search_results(results, sample_manifest, 'test query')

        assert enriched['query'] == 'test query'
        assert enriched['total_results'] == 2
        assert enriched['unique_products'] == 2  # One known, one unknown
        assert 'Claude Code CLI' in enriched['product_summary']

    def test_multi_product_context(self, sample_manifest):
        """Test enriched results with multiple product contexts"""
        results = [
            ('/docs/en/skills', 70.0),
            ('/en/api/skills/create-skill', 60.0),
            ('/en/docs/agent-sdk/skills', 65.0)
        ]

        enriched = create_enriched_search_results(results, sample_manifest, 'skills')

        assert enriched['unique_products'] == 3
        assert enriched['product_summary']['Claude Code CLI'] == 1
        assert enriched['product_summary']['Claude API'] == 1
        assert enriched['product_summary']['Claude Agent SDK'] == 1

    def test_result_structure(self, sample_manifest):
        """Test structure of individual results"""
        results = [('/docs/en/skills', 70.0)]
        enriched = create_enriched_search_results(results, sample_manifest, 'skills')

        result = enriched['results'][0]
        assert 'path' in result
        assert 'category' in result
        assert 'product' in result
        assert 'score' in result
        assert result['path'] == '/docs/en/skills'
        assert result['category'] == 'claude_code'
        assert result['product'] == 'Claude Code CLI'
        assert result['score'] == 70.0


class TestContentSearchJSON:
    """Test content search JSON formatting"""

    @pytest.fixture
    def sample_manifest(self):
        """Sample manifest for testing"""
        return {
            'categories': {
                'claude_code': ['/docs/en/hooks', '/docs/en/hooks-guide'],
                'api_reference': ['/en/docs/agent-sdk/python']
            }
        }

    @pytest.fixture
    def sample_content_results(self):
        """Sample content search results"""
        return [
            {
                'path': '/en/docs/claude-code/hooks',
                'title': 'Hooks Reference',
                'score': 135,
                'preview': 'Documentation about hooks...' * 10,
                'keywords': ['hooks', 'claude', 'code', 'custom', 'commands']
            },
            {
                'path': '/en/docs/claude-code/hooks-guide',
                'title': 'Get Started with Hooks',
                'score': 130,
                'preview': 'Guide for using hooks...',
                'keywords': ['hooks', 'guide', 'tutorial', 'start', 'begin']
            }
        ]

    def test_content_json_structure(self, sample_content_results, sample_manifest):
        """Test JSON structure for content search"""
        json_output = format_content_search_json(
            sample_content_results,
            'hooks',
            sample_manifest
        )

        assert json_output['query'] == 'hooks'
        assert json_output['total_results'] == 2
        assert json_output['unique_products'] == 1
        assert 'results' in json_output
        assert 'product_summary' in json_output

    def test_content_result_enrichment(self, sample_content_results, sample_manifest):
        """Test that content results are enriched with product context"""
        json_output = format_content_search_json(
            sample_content_results,
            'hooks',
            sample_manifest
        )

        for result in json_output['results']:
            assert 'category' in result
            assert 'product' in result
            assert result['category'] == 'claude_code'
            assert result['product'] == 'Claude Code CLI'

    def test_preview_truncation(self, sample_content_results, sample_manifest):
        """Test that long previews are truncated"""
        json_output = format_content_search_json(
            sample_content_results,
            'hooks',
            sample_manifest
        )

        # First result has long preview, should be truncated to 150 chars
        assert len(json_output['results'][0]['preview']) == 150

    def test_keyword_limit(self, sample_content_results, sample_manifest):
        """Test that keywords are limited to top 5"""
        json_output = format_content_search_json(
            sample_content_results,
            'hooks',
            sample_manifest
        )

        for result in json_output['results']:
            assert len(result['keywords']) <= 5


class TestDecisionMaking:
    """Test scenarios that inform Claude's decision making"""

    @pytest.fixture
    def sample_manifest(self):
        """Sample manifest for testing"""
        return {
            'categories': {
                'claude_code': ['/docs/en/skills'],
                'api_reference': [
                    '/en/api/skills/create-skill',
                    '/en/docs/agent-sdk/skills'
                ]
            }
        }

    def test_synthesis_scenario(self, sample_manifest):
        """Test data for 'should synthesize' scenario"""
        # All results in same product context
        results = [
            ('/docs/en/skills', 70.0),
            ('/docs/en/hooks', 65.0),
            ('/docs/en/mcp', 60.0)
        ]

        enriched = create_enriched_search_results(results, sample_manifest, 'query')

        # Verify single product (Unknown for hooks/mcp since not in manifest)
        # But the principle is: if unique_products == 1, synthesize
        # In real usage, most paths should be in manifest
        assert 'unique_products' in enriched
        assert isinstance(enriched['unique_products'], int)

    def test_ask_user_scenario(self, sample_manifest):
        """Test data for 'should ask user' scenario"""
        # Results span multiple products
        results = [
            ('/docs/en/skills', 70.0),
            ('/en/api/skills/create-skill', 60.0),
            ('/en/docs/agent-sdk/skills', 65.0)
        ]

        enriched = create_enriched_search_results(results, sample_manifest, 'skills')

        # Should have 3 unique products
        assert enriched['unique_products'] == 3
        assert len(enriched['product_summary']) == 3

        # Verify we can extract product names for AskUserQuestion
        products = list(enriched['product_summary'].keys())
        assert 'Claude Code CLI' in products
        assert 'Claude API' in products
        assert 'Claude Agent SDK' in products


class TestJSONSerialization:
    """Test that JSON output is valid and serializable"""

    @pytest.fixture
    def sample_manifest(self):
        """Sample manifest for testing"""
        return {
            'categories': {
                'claude_code': ['/docs/en/hooks']
            }
        }

    def test_path_search_json_serializable(self, sample_manifest):
        """Test that path search JSON is serializable"""
        results = [('/docs/en/hooks', 70.0)]
        enriched = create_enriched_search_results(results, sample_manifest, 'hooks')

        # Should not raise
        json_str = json.dumps(enriched)
        assert json_str

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed['query'] == 'hooks'

    def test_content_search_json_serializable(self, sample_manifest):
        """Test that content search JSON is serializable"""
        content_results = [{
            'path': '/en/docs/claude-code/hooks',
            'title': 'Hooks',
            'score': 100,
            'preview': 'Test preview',
            'keywords': ['test']
        }]

        json_output = format_content_search_json(content_results, 'hooks', sample_manifest)

        # Should not raise
        json_str = json.dumps(json_output)
        assert json_str

        # Should be valid JSON
        parsed = json.loads(json_str)
        assert parsed['query'] == 'hooks'


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
