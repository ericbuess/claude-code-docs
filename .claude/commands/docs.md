---
description: Access Claude Code documentation (standard and enhanced features)
---

Execute the Claude Code Docs helper script with enhanced features support.

This command supports both explicit flags (for power users) and natural language (for intuitive use).

## 🎯 Intent Detection Instructions (for Claude)

When the user invokes `/docs` with arguments, analyze their intent and execute accordingly:

### Priority Rules (check in this order):

1. **Explicit flags** - If arguments start with `--`, pass them directly:
   - `--search`, `--search-content`, `--validate`, `--update-all`, `--version`, `--status`, `--help`
   - Example: `/docs --search "mcp"` → Execute with `--search "mcp"`

2. **Standard special commands** - If arguments match these exactly, pass them directly:
   - `-t` (freshness check)
   - `-t <topic>` (check freshness then read)
   - `whats new` or `what's new` (recent changes)
   - `changelog` (release notes)
   - `uninstall` (uninstall instructions)

3. **Natural language search intent** - If user indicates they want to search:
   - Keywords: "search for", "find", "look for", "search", "locate", "where is"
   - Action: Extract the query after the keyword and execute with `--search "query"`
   - Examples:
     - `/docs search for mcp` → `--search "mcp"`
     - `/docs find prompt engineering` → `--search "prompt engineering"`
     - `/docs look for hooks` → `--search "hooks"`

4. **Natural language content search** - If user wants to search document content:
   - Keywords: "search content", "find content", "find in docs", "search inside"
   - Action: Extract the query and execute with `--search-content "query"`
   - Examples:
     - `/docs search content about tool use` → `--search-content "tool use"`
     - `/docs find content extended thinking` → `--search-content "extended thinking"`

5. **Natural language validation** - If user wants to check paths:
   - Keywords: "validate", "check all", "test paths", "verify"
   - Action: Execute with `--validate`
   - Examples:
     - `/docs validate all paths` → `--validate`
     - `/docs check if everything works` → `--validate`

6. **Natural language update** - If user wants to fetch documentation:
   - Keywords: "update all", "fetch all", "sync all", "download all", "refresh all"
   - Action: Execute with `--update-all`
   - Examples:
     - `/docs update everything` → `--update-all`
     - `/docs fetch all documentation` → `--update-all`

7. **Topic reading** - If none of the above match, treat as a topic name:
   - Action: Pass the entire argument string to read that topic
   - Examples:
     - `/docs hooks` → read "hooks" documentation
     - `/docs prompt engineering` → read "prompt engineering" topic

8. **List all topics** - If no arguments at all:
   - Action: Execute with no arguments to list all topics

### Handling Ambiguities

**When in doubt, favor topic reading over search** to avoid false positives:
- `/docs search history` → Could be search OR topic name
  - If "search" is the ONLY first word followed by content: treat as search command
  - Otherwise: treat as topic name "search history"

**For update commands**, require explicit "all" or "everything":
- `/docs update hooks` → Read "update hooks" topic (not update command)
- `/docs update all` → Execute `--update-all` (update command)

## Standard Commands (Always Available)

All users get these commands regardless of Python availability:

- `/docs` - List all available documentation topics
- `/docs <topic>` - Read specific documentation with link to official docs
- `/docs -t` - Check sync status without reading a doc
- `/docs -t <topic>` - Check freshness then read documentation
- `/docs whats new` - Show recent documentation changes

## Enhanced Commands (Python 3.12+ Required)

If enhanced features are installed, these additional commands are available:

**Search & Discovery:**
- `/docs --search "mcp"` - Fuzzy search across 449 paths
- `/docs --search-content "tool use"` - Full-text content search across all docs

**Maintenance:**
- `/docs --validate` - Validate all 449 paths for reachability
- `/docs --update-all` - Fetch all 449 documentation pages

**Status:**
- `/docs --version` - Show version information
- `/docs --status` - Show installation and feature status
- `/docs --help` - Show all available commands

## Natural Language Examples

You can use natural language instead of explicit flags:

**Search examples:**
```
/docs search for mcp integration
/docs find prompt engineering
/docs look for tool use examples
/docs where is the hooks documentation
```

**Content search examples:**
```
/docs search content about extended thinking
/docs find in docs how to use computer use
/docs search inside documentation for batch API
```

**Validation examples:**
```
/docs validate all paths
/docs check if everything is reachable
/docs verify paths work
```

**Update examples:**
```
/docs update all documentation
/docs fetch everything
/docs sync all docs
/docs refresh all
```

**Topic reading examples:**
```
/docs hooks
/docs prompt engineering
/docs mcp overview
/docs what's new
```

## Installation Modes

### Standard Mode (Shell-only, no Python required)
- 47 documentation topics
- Basic search by topic name
- Auto-updates via git pull
- Works offline after initial install

### Enhanced Mode (Python 3.12+ required)
- 449 documentation paths (10x more coverage)
- Fuzzy search with relevance ranking
- Full-text content search
- Path validation and testing
- Search index optimization
- Advanced update features

## How to Enable Enhanced Features

If you see "Enhanced features: NOT AVAILABLE" when running `/docs --status`, reinstall with:

```bash
curl -fsSL https://raw.githubusercontent.com/costiash/claude-code-docs/main/install.sh | bash
# Answer 'y' when prompted for enhanced features
```

## Example Usage

**Read documentation (standard):**
```
/docs hooks              # Read hooks documentation
/docs -t                 # Check when docs were last updated
/docs what's new         # See recent documentation changes
```

**Enhanced search (requires Python 3.12+):**
```
/docs --search "prompt engineering"     # Fuzzy search 449 paths
/docs --search-content "extended thinking"  # Full-text search
/docs --validate                        # Check all paths
/docs --update-all                      # Fetch all docs
```

**Natural language (works with both modes):**
```
/docs search for mcp                    # Natural language search
/docs find content about tool use       # Natural language content search
/docs validate all paths                # Natural language validation
/docs update everything                 # Natural language update
```

## Auto-Updates

Every request checks for the latest documentation from GitHub (takes ~0.4s).
Enhanced features include automatic search index rebuilding after updates.

## Documentation Location

- **Installation**: `~/.claude-code-docs/`
- **Helper Script**: `~/.claude-code-docs/scripts/claude-docs-helper.sh`
- **Template**: `~/.claude-code-docs/scripts/claude-docs-helper.sh.template`
- **Documentation**: `~/.claude-code-docs/docs/`
- **Manifest**: `~/.claude-code-docs/paths_manifest.json`

## Execution Logic

Based on the intent analysis above, execute the appropriate command:

- **Explicit flags**: Pass directly to helper script
- **Natural language search**: Convert to `--search "query"`
- **Natural language content search**: Convert to `--search-content "query"`
- **Natural language validate**: Convert to `--validate`
- **Natural language update**: Convert to `--update-all`
- **Topic name or special command**: Pass as-is to helper script
- **No arguments**: Execute with no arguments (list topics)

Execute: ~/.claude-code-docs/scripts/claude-docs-helper.sh "$ARGUMENTS"
