# Enhanced Features Usage Examples

This guide provides practical examples for using the enhanced documentation features in claude-code-docs.

## Table of Contents

1. [Using Enhancements in Claude Code](#using-enhancements-in-claude-code)
2. [Using the /docs Command](#using-the-docs-command)
3. [Command-Line Reference](#command-line-reference)

## Using Enhancements in Claude Code

The enhanced edition is designed primarily for use within Claude Code via the `/docs` command. This section shows how to effectively leverage the expanded documentation coverage.

### Finding Documentation Topics

**Search for specific topics**:

```
/docs mcp
```

Returns all MCP-related documentation including:
- Build with Claude: MCP integration guide
- Claude Code: MCP configuration
- Agent SDK: MCP server implementation
- Agents and Tools: MCP overview

**Search for API documentation**:

```
/docs api messages
```

Finds:
- API Reference: Messages endpoint
- API Reference: Messages streaming
- Build with Claude: Working with messages

**Search Claude Code specific docs**:

```
/docs claude code hooks
```

Locates:
- Claude Code: Hooks overview
- Claude Code: Hooks guide
- Claude Code: Hook configuration

### Browsing by Category

**View core documentation**:

```
/docs --category core_documentation
```

Lists all 151 core documentation paths including:
- About Claude (models, pricing, security)
- Build with Claude (prompt engineering, streaming, files)
- Test and Evaluate (guardrails, testing)
- Use case guides

**Browse API reference**:

```
/docs --category api_reference
```

Shows all 91 API reference paths:
- Administration API
- Agent SDK
- Messages API
- Files API
- Skills API

**Explore prompt library**:

```
/docs --category prompt_library
```

Lists 64 prompt templates for various use cases.

### Finding Specific Features

**Looking for tool use documentation**:

```
/docs tool use
```

Returns:
- Build with Claude: Tool use overview
- Agents and Tools: Tool use implementation
- API Reference: Tool definitions
- Claude Code: Custom tools

**Finding prompt engineering guides**:

```
/docs prompt engineering
```

Locates:
- Build with Claude: Prompt engineering overview
- Chain of thought prompting
- System prompts guide
- Claude 4 best practices

**Searching for integration guides**:

```
/docs github actions
```
or
```
/docs vs code
```

Finds integration-specific documentation.

### Natural Language Queries

The enhanced search understands natural language:

```
/docs how to use extended thinking
```

Finds:
- About Claude: Extended thinking models
- Build with Claude: Extended thinking guide
- Prompt Engineering: Extended thinking tips

```
/docs batch processing api
```

Locates:
- Build with Claude: Batch processing
- API Reference: Creating message batches
- API Reference: Retrieving batch results

## Using the /docs Command

### Basic Search

**Simple topic search**:

```bash
/docs hooks
```

**Response includes**:
- Claude Code: Hooks guide
- Claude Code: Hooks reference
- API Reference: Hook configuration

### Search with Options

**Search in specific category**:

```bash
/docs --category claude_code hooks
```

Only returns results from Claude Code documentation.

**List all categories**:

```bash
/docs --list-categories
```

Shows:
- core_documentation (151)
- api_reference (91)
- claude_code (68)
- resources (68)
- prompt_library (64)
- release_notes (4)
- uncategorized (3)

### Viewing Documentation

**Open specific documentation**:

```bash
/docs mcp
```

Claude Code displays the content of matching documentation files.

**Multiple matches**:

When multiple documents match, you'll see:
1. List of all matching paths
2. Option to view specific document
3. Related documentation suggestions

### Advanced Search Features

**Content-based search** (searches within documentation text):

```bash
/docs --search-content "streaming responses"
```

Finds documents containing the phrase "streaming responses" in their content, not just in path names.

**Fuzzy matching**:

If you mistype or use approximate terms:

```bash
/docs promt engeneering
```

The system suggests:
- Did you mean: "prompt engineering"?
- Showing results for: prompt engineering

### Validation

**Check documentation availability**:

```bash
/docs --validate
```

Validates that all 449 documentation paths are reachable on docs.anthropic.com.

**Output includes**:
- Total paths checked: 449
- Successful: 449
- Failed: 0
- Validation time: ~30s

**Verify specific path**:

```bash
/docs --validate /en/docs/build-with-claude/mcp
```

Checks if specific path is reachable.

## Command-Line Reference

### Direct Script Usage

For advanced users or automation, you can use the Python scripts directly.

#### Search Operations

**Path search**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --search "mcp"
```

**Content search**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --search-content "model context protocol"
```

**Category filtering**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --search "hooks" --category claude_code
```

#### Validation Operations

**Full validation**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --validate
```

**Parallel validation** (adjust concurrency):

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --validate --workers 20
```

**Quiet validation** (errors only):

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --validate --quiet
```

#### Update Operations

**Update all documentation**:

```bash
python ~/.claude-code-docs/scripts/main.py --update-all
```

**Update specific category**:

```bash
python ~/.claude-code-docs/scripts/main.py --update-category core_documentation
```

**Check what needs updating** (dry run):

```bash
python ~/.claude-code-docs/scripts/main.py --verify
```

**Force update** (ignore hashes):

```bash
python ~/.claude-code-docs/scripts/main.py --update-all --force
```

#### Path Management

**Build search index**:

```bash
python ~/.claude-code-docs/scripts/build_search_index.py
```

**Extract paths from sitemap**:

```bash
python ~/.claude-code-docs/scripts/extract_paths.py
```

**Clean broken paths**:

```bash
python ~/.claude-code-docs/scripts/clean_manifest.py
```

**Update sitemap**:

```bash
python ~/.claude-code-docs/scripts/update_sitemap.py
```

### Common Patterns

#### Daily Workflow

**Morning documentation check**:

```bash
# Update any changed docs
python ~/.claude-code-docs/scripts/main.py --update-all

# Validate all paths
python ~/.claude-code-docs/scripts/lookup_paths.py --validate
```

#### Integration Testing

**In CI/CD pipeline**:

```bash
# Validate docs are accessible
python ~/.claude-code-docs/scripts/lookup_paths.py --validate || exit 1

# Update docs
python ~/.claude-code-docs/scripts/main.py --update-all

# Rebuild search index
python ~/.claude-code-docs/scripts/build_search_index.py
```

#### Content Analysis

**Find all documents mentioning a topic**:

```bash
# Search content
python ~/.claude-code-docs/scripts/lookup_paths.py --search-content "extended thinking" > results.txt

# Count matches
cat results.txt | grep -c "Found"
```

#### Maintenance

**Clean and rebuild**:

```bash
# Clean broken paths
python ~/.claude-code-docs/scripts/clean_manifest.py

# Rebuild everything
python ~/.claude-code-docs/scripts/main.py --update-all --force

# Rebuild search index
python ~/.claude-code-docs/scripts/build_search_index.py

# Validate all paths
python ~/.claude-code-docs/scripts/lookup_paths.py --validate
```

### Flag Reference

#### Common Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--search <query>` | Search path names | `--search mcp` |
| `--search-content <query>` | Search content | `--search-content "streaming"` |
| `--category <cat>` | Filter by category | `--category api_reference` |
| `--validate` | Validate paths | `--validate` |
| `--list-categories` | List all categories | `--list-categories` |
| `--quiet` | Minimal output | `--validate --quiet` |
| `--verbose` | Detailed output | `--update-all --verbose` |

#### Update Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--update-all` | Update all docs | `--update-all` |
| `--update-category <cat>` | Update category | `--update-category core` |
| `--verify` | Check for changes | `--verify` |
| `--force` | Force update | `--update-all --force` |

#### Validation Flags

| Flag | Description | Example |
|------|-------------|---------|
| `--workers <n>` | Concurrent requests | `--validate --workers 10` |
| `--timeout <s>` | Request timeout | `--validate --timeout 15` |
| `--report` | Generate report | `--validate --report` |

### Tips and Tricks

**1. Combining flags for precise results**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py \
  --search "streaming" \
  --category api_reference
```

**2. Using wildcards in searches**:

```bash
/docs "claude code*"
```

**3. Excluding categories**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py \
  --search "api" \
  --exclude-category prompt_library
```

**4. Export search results**:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py \
  --search "mcp" \
  --format json > mcp_docs.json
```

**5. Batch operations**:

```bash
# Update multiple categories
for cat in core_documentation api_reference claude_code; do
  python ~/.claude-code-docs/scripts/main.py --update-category $cat
done
```

## Frequently Asked Questions

### How do I find all documentation about a topic?

Use both path and content search:

```bash
/docs --search "topic"
/docs --search-content "topic"
```

### How do I know if a document exists?

Use validation:

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py \
  --validate /en/docs/path/to/doc
```

### How do I update just one category?

```bash
python ~/.claude-code-docs/scripts/main.py \
  --update-category category_name
```

### How do I see what changed?

```bash
python ~/.claude-code-docs/scripts/main.py --verify
```

This shows which documents have changed (by hash) without fetching them.

### How do I search for exact phrases?

Use quotes:

```bash
/docs "exact phrase here"
```

### How do I get a list of all available paths?

```bash
python ~/.claude-code-docs/scripts/lookup_paths.py --list-all
```

or view the paths_manifest.json directly:

```bash
jq '.categories' ~/.claude-code-docs/paths_manifest.json
```

## Getting Help

For additional help:

1. **Feature questions**: See `CAPABILITIES.md`
2. **Installation help**: See `README.md`
3. **Contributing**: See `CONTRIBUTING.md`
4. **Upstream compatibility**: See root `CLAUDE.md`

## Examples Repository

More examples and use cases: See the test suite in `tests/` directory for programmatic usage patterns.
