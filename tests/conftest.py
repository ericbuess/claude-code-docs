"""Pytest configuration and fixtures."""

import pytest
from pathlib import Path
import json
import tempfile
import shutil


@pytest.fixture
def sample_html():
    """Sample HTML for testing."""
    return """
    <html>
    <head><title>Test Page - Claude Documentation</title></head>
    <body>
        <article>
            <h1>Test Title</h1>
            <p>This is test content about Claude.</p>
            <h2>Code Example</h2>
            <pre><code class="language-python">
import anthropic

client = anthropic.Anthropic(api_key="test-key")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
print(message.content)
            </code></pre>
            <h2>Features</h2>
            <ul>
                <li>Feature 1</li>
                <li>Feature 2</li>
            </ul>
        </article>
    </body>
    </html>
    """


@pytest.fixture
def sample_markdown():
    """Sample markdown content."""
    return """# Test Title

This is test content about Claude.

## Code Example

```python
import anthropic

client = anthropic.Anthropic(api_key="test-key")
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
)
print(message.content)
```

## Features

- Feature 1
- Feature 2
"""


@pytest.fixture
def sample_paths():
    """Sample paths for testing."""
    return [
        '/en/docs/build-with-claude/prompt-engineering',
        '/en/api/messages',
        '/en/docs/claude-code/mcp/overview',
        '/en/prompt-library/code-consultant'
    ]


@pytest.fixture
def sample_paths_with_fragments():
    """Sample paths with URL fragments."""
    return [
        '/en/docs/build-with-claude#overview',
        '/en/api/messages#streaming',
        '/en/docs/claude-code/mcp/overview#installation'
    ]


@pytest.fixture
def invalid_paths():
    """Invalid/noise paths for testing."""
    return [
        '/en/docs/:slug*',
        '/en/api/),',
        '/en/docs/test\\',
        '/en/docs/test\\\\',
        '',
        '   ',
        '/en/docs//double-slash'
    ]


@pytest.fixture
def mock_http_success(monkeypatch):
    """Mock successful HTTP requests."""
    import requests

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            text = "# Mock Documentation\n\nThis is mock content."
            content = b"# Mock Documentation\n\nThis is mock content."
            url = args[0] if args else kwargs.get('url', '')

            def raise_for_status(self):
                pass

            def json(self):
                return {"status": "ok"}

        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'head', mock_get)


@pytest.fixture
def mock_http_404(monkeypatch):
    """Mock 404 HTTP responses."""
    import requests

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 404
            text = "Not Found"
            url = args[0] if args else kwargs.get('url', '')

            def raise_for_status(self):
                raise requests.HTTPError("404 Not Found")

        return MockResponse()

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'head', mock_get)


@pytest.fixture
def mock_http_timeout(monkeypatch):
    """Mock timeout errors."""
    import requests

    def mock_get(*args, **kwargs):
        raise requests.Timeout("Request timed out")

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'head', mock_get)


@pytest.fixture
def paths_manifest():
    """Load paths manifest for tests."""
    manifest_path = Path(__file__).parent.parent / 'paths_manifest.json'
    if manifest_path.exists():
        return json.loads(manifest_path.read_text())

    # Return minimal structure if file doesn't exist
    return {
        'metadata': {
            'generated_at': '2025-11-03T00:00:00',
            'total_paths': 0,
            'source': 'test'
        },
        'categories': {
            'core_documentation': [],
            'api_reference': [],
            'claude_code': [],
            'prompt_library': []
        }
    }


@pytest.fixture
def temp_docs_dir(tmp_path):
    """Create temporary docs directory."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    # Create some sample doc files
    (docs_dir / "en__docs__test.md").write_text("# Test Doc\n\nTest content")
    (docs_dir / "en__api__messages.md").write_text("# Messages API\n\nAPI content")

    return docs_dir


@pytest.fixture
def temp_manifest(tmp_path):
    """Create temporary manifest file."""
    manifest_path = tmp_path / "paths_manifest.json"
    manifest_data = {
        'metadata': {
            'generated_at': '2025-11-03T00:00:00',
            'total_paths': 4,
            'source': 'test.html'
        },
        'categories': {
            'core_documentation': [
                '/en/docs/build-with-claude',
                '/en/docs/test-page'
            ],
            'api_reference': [
                '/en/api/messages',
                '/en/api/streaming'
            ],
            'claude_code': [],
            'prompt_library': []
        }
    }
    manifest_path.write_text(json.dumps(manifest_data, indent=2))
    return manifest_path


@pytest.fixture
def project_root():
    """Get project root directory."""
    return Path(__file__).parent.parent


# Configure pytest
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "network: marks tests requiring network access"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
