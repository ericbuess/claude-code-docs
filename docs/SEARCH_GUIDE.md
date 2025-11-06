# Search Guide

Quick reference for searching the Claude Code Documentation Mirror.

## Two Search Types

### 1. Path Search (Default)

Searches **URL path names** only.

```bash
python scripts/lookup_paths.py "your query"
```

**Use when**:
- You know the general topic/section
- Looking for specific API endpoints
- Finding documentation categories

**Examples**:
```bash
python scripts/lookup_paths.py "prompt engineering"
python scripts/lookup_paths.py "mcp"
python scripts/lookup_paths.py "api messages"
```

**Output**: List of paths matching query

---

### 2. Content Search (Full-Text)

Searches **document content** (title, keywords, text).

```bash
python scripts/lookup_paths.py --search-content "your query"
```

**Use when**:
- Looking for specific concepts mentioned in content
- Don't know exact section name
- Want relevance-ranked results

**Examples**:
```bash
python scripts/lookup_paths.py --search-content "extended thinking"
python scripts/lookup_paths.py --search-content "batch processing"
python scripts/lookup_paths.py --search-content "tool use"
```

**Output**: Documents with title, keywords, preview, relevance score

---

## Quick Start

### First Time Setup

Build the search index (run once):

```bash
python scripts/build_search_index.py
```

This creates `docs/.search_index.json` (38KB for 49 files).

### Rebuilding Index

Rebuild after updating documentation:

```bash
python scripts/build_search_index.py
```

---

## Search Comparison

| Feature | Path Search | Content Search |
|---------|-------------|----------------|
| **Searches** | URL paths only | Title, keywords, content |
| **Results** | Paths matching query | Documents with relevance score |
| **Speed** | Very fast (< 10ms) | Fast (< 100ms) |
| **Use Case** | Know section/topic | Know concept/term |
| **Command** | `lookup_paths.py "query"` | `lookup_paths.py --search-content "query"` |

---

## Examples

### Example 1: Find MCP Documentation

**Path Search**:
```bash
$ python scripts/lookup_paths.py "mcp"

Found 8 results:
1. /en/docs/agents-and-tools/mcp
2. /en/docs/claude-code/mcp/overview
...
```

**Content Search**:
```bash
$ python scripts/lookup_paths.py --search-content "mcp"

✅ Found 8 matching documents:

1. Connect Claude Code to tools via MCP (score: 135)
   Path: /mcp
   Keywords: mcp, servers, server, true, https
   Preview: # Connect Claude Code to tools via MCP...
```

### Example 2: Find Prompt Engineering Docs

**Path Search**:
```bash
python scripts/lookup_paths.py "prompt engineering"
# Returns paths with "prompt" or "engineering" in URL
```

**Content Search**:
```bash
python scripts/lookup_paths.py --search-content "prompt engineering"
# Returns docs mentioning prompt engineering in content
```

---

## Tips

### Path Search Tips

1. **Use specific terms**: "api messages" instead of "api"
2. **Try variations**: "mcp" or "model context protocol"
3. **Check categories**: Results show category (core_documentation, api_reference, etc.)

### Content Search Tips

1. **Use descriptive terms**: "extended thinking" instead of "thinking"
2. **Multi-word queries work**: "tool use", "batch processing"
3. **Check relevance scores**: Higher score = more relevant
4. **Review keywords**: Shows main topics in document

---

## Advanced Usage

### Limit Results

```bash
python scripts/lookup_paths.py "query" --max-results 10
python scripts/lookup_paths.py --search-content "query" --max-results 10
```

### Validate Paths

```bash
python scripts/lookup_paths.py --check /en/docs/path
python scripts/lookup_paths.py --validate-all
```

### Get Help

```bash
python scripts/lookup_paths.py --help
```

---

## Troubleshooting

### "Search index not found"

**Problem**: Content search fails with "Search index not found"

**Solution**:
```bash
python scripts/build_search_index.py
```

### No Results Found

**Problem**: Search returns no results

**Try**:
1. Use simpler query terms
2. Try path search instead of content search (or vice versa)
3. Check for typos
4. Use `--max-results 50` for more results

### Index Out of Date

**Problem**: New documentation not appearing in content search

**Solution**: Rebuild index
```bash
python scripts/build_search_index.py
```

---

## For Developers

### Index Structure

Location: `docs/.search_index.json`

```json
{
  "version": "1.0",
  "generated_at": "2025-11-03T20:36:29Z",
  "indexed_files": 49,
  "index": {
    "/path": {
      "title": "Document Title",
      "content_preview": "Preview text...",
      "keywords": ["keyword1", "keyword2", ...],
      "word_count": 1234,
      "file_path": "docs/path.md"
    }
  }
}
```

### Relevance Scoring

- Title match: +100 points
- Keyword match: +10 points per keyword
- Preview match: +20 points
- Exact word in keywords: +5 points bonus

---

**Last Updated**: 2025-11-03
**Search Index**: 49 files indexed
**Index Size**: 38KB
