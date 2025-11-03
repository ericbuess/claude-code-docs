---
description: Access Claude Code documentation (standard and enhanced features)
---

Execute the Claude Code Docs helper script with enhanced features support.

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

## Auto-Updates

Every request checks for the latest documentation from GitHub (takes ~0.4s).
Enhanced features include automatic search index rebuilding after updates.

## Documentation Location

- **Installation**: `~/.claude-code-docs/`
- **Helper Script**: `~/.claude-code-docs/scripts/claude-docs-helper.sh`
- **Template**: `~/.claude-code-docs/scripts/claude-docs-helper.sh.template`
- **Documentation**: `~/.claude-code-docs/docs/`
- **Manifest**: `~/.claude-code-docs/paths_manifest.json`

Execute: ~/.claude-code-docs/scripts/claude-docs-helper.sh "$ARGUMENTS"
