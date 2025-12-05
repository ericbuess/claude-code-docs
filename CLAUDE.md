# Claude Code Documentation Mirror - Enhanced Edition

> **⛔ CRITICAL: UPSTREAM ISOLATION ⛔**
>
> **This repository is COMPLETELY INDEPENDENT. Do NOT:**
> - Push to, pull from, or sync with the upstream repo (ericbuess/claude-code-docs)
> - Create PRs to the upstream repo
> - Add upstream as a remote
> - Reference upstream in any git operations
>
> **All git operations must target `origin` (costiash/claude-code-docs) ONLY.**

This repository contains local copies of Claude documentation from multiple Anthropic sources:
- **Platform docs**: https://platform.claude.com (API, guides, Agent SDK, etc.)
- **Claude Code docs**: https://code.claude.com/docs (CLI-specific documentation)

The docs are periodically updated via GitHub Actions with safeguards to prevent mass deletion.

## Architecture: Single Installation with Optional Python Features

This repository uses a **graceful degradation** approach:

**Installation** (always the same):
- 573 documentation paths tracked in manifest (6 categories)
- 571 files downloaded
- Python scripts for enhanced features
- Full test suite (294 tests) and GitHub workflows

**Runtime Features** (Python-dependent):
- **Without Python 3.9+**: Basic documentation reading via shell scripts
- **With Python 3.9+**: Full-text search, path validation, fuzzy matching, auto-regeneration

There is NO separate "standard mode installation" - the full repository is always installed. Python features simply activate when Python 3.9+ is available.

## For /docs Command - AI-Powered Semantic Search

**IMPORTANT**: The `/docs` command is **AI-powered** and leverages Claude's semantic understanding instead of primitive keyword matching.

When responding to /docs commands:

1. **Read AI Instructions**: `~/.claude/commands/docs.md` contains comprehensive AI instructions on how to:
   - Analyze user intent semantically
   - Route to appropriate helper functions
   - Present results naturally with context

2. **Semantic Analysis**: Use your language understanding to classify user intent:
   - **Direct lookup**: User names a specific topic (e.g., `/docs hooks`)
   - **Information search**: User asks questions (e.g., `/docs what are best practices for SDK in Python?`)
   - **Path discovery**: User wants to find available docs (e.g., `/docs show me all MCP documentation`)
   - **Freshness check**: User wants update status (e.g., `/docs -t`)
   - **What's new**: User wants recent changes (e.g., `/docs what's new`)

3. **Intelligent Routing**: Based on semantic understanding, route to appropriate functions:
   - `--search-content "<keywords>"` for semantic information searches (requires Python 3.9+)
   - `--search "<keywords>"` for path discovery (requires Python 3.9+)
   - `<topic>` for direct documentation lookups
   - `-t` for freshness checks
   - `"what's new"` for recent changes

4. **Graceful Degradation**: The helper script automatically detects Python availability:
   - **With Python 3.9+**: Full AI-powered search with content search, path search, validation
   - **Without Python**: Basic documentation reading, explain limitations gracefully

5. **Natural Presentation**: Don't dump raw tool output - present information naturally:
   - Summarize search results with context
   - Provide official documentation links
   - Combine multiple sources when helpful
   - Explain your routing decisions if uncertain

**Example AI-Powered Workflow**:
```
User: /docs what are the best practices and recommended workflows using Claude Agent SDK in Python?

Your Analysis:
- User wants information (not a specific doc name)
- Key concepts: best practices, workflows, Agent SDK, Python
- Route to content search

Your Actions:
1. Extract keywords: "best practices workflows Agent SDK Python"
2. Execute: ~/.claude-code-docs/claude-docs-helper.sh --search-content "best practices workflows Agent SDK Python"
3. Read matching documentation sections
4. Present naturally: "Based on the official documentation, here are the best practices..."
5. Include links to relevant docs

Result: User gets semantic answer with documentation context, not raw file paths
```

## Intent-Driven Documentation Search - ENHANCED APPROACH

**Philosophy**: Hide complexity from users. Synthesize aggressively. Minimize interaction.

### Core Principles

1. **Intent-driven, not path-driven** - Understand WHAT the user wants, not WHERE it might be located
2. **Content search over path matching** - Find relevant information even without exact path matches
3. **Synthesize by default** - Read multiple docs silently, present one unified answer
4. **Only ask when contexts are incompatible** - Different products with fundamentally different workflows

### Category Labels (User-Facing)

When presenting options to users, always use these user-friendly labels:

| Internal Category | User-Facing Label |
|-------------------|-------------------|
| `claude_code` | Claude Code CLI |
| `api_reference` | Claude API |
| `core_documentation` | Claude Documentation |
| Agent SDK paths (`/en/docs/agent-sdk/*`) | Claude Agent SDK |
| `prompt_library` | Prompt Library |
| `release_notes` | Release Notes |
| `resources` | Resources |

**Why this matters**: Users think in product names ("I'm using Claude Agent SDK"), not internal category identifiers.

### Ambiguity Resolution Strategy

#### SYNTHESIZE (default behavior):

**When**: Multiple documents in the same product context

**Action**:
- Read ALL matching documents silently (no asking user which to read)
- Extract relevant sections related to query intent
- Synthesize one unified, coherent answer
- Cite all sources at the end

**Example**:
```
User: /docs hooks in agent sdk

Search finds:
- /en/docs/agent-sdk/python.md (15 mentions of "hooks")
- /en/docs/agent-sdk/overview.md (3 mentions of "hooks")
- /en/docs/agent-sdk/plugins.md (8 mentions of "hooks")

Decision: All in same context (Agent SDK) → SYNTHESIZE

Action:
1. Read all three documents silently
2. Extract all hook-related content
3. Synthesize unified explanation

Present:
"In the Claude Agent SDK, hooks provide intercept points in the agent lifecycle...

[Unified explanation combining insights from all three sources]

You can configure hooks in Python like this:
[Code example from python.md]

Common use cases for hooks include:
[Use cases from overview.md]

When integrating with plugins:
[Integration details from plugins.md]

Sources:
• Agent SDK Python Guide: https://docs.claude.com/en/docs/agent-sdk/python
• Agent SDK Overview: https://docs.claude.com/en/docs/agent-sdk/overview
• Plugins Integration: https://docs.claude.com/en/docs/agent-sdk/plugins"
```

**Never show**: "Found 3 documents about hooks, which do you want to read?" ❌

#### ASK (minimal - only for cross-context ambiguity):

**When**: Matches span fundamentally different product contexts with incompatible workflows

**Action**:
- Use AskUserQuestion tool
- Present options with user-friendly product labels
- Explain WHY contexts are different
- After selection → synthesize within chosen context

**Example**:
```
User: /docs skills

Search finds matches in 3 different products:
- Claude Agent SDK (5 docs) - Building custom agent capabilities
- Claude Code CLI (2 docs) - Installing/running pre-built skills locally
- Claude API (7 docs) - Programmatic skill management endpoints

Decision: Different products, incompatible workflows → ASK

Present:
"Skills exist in different Claude products with different purposes:

○ 1. Claude Agent SDK
     Build custom agent capabilities in Python/TypeScript
     (For developers creating new agent skills)

○ 2. Claude Code CLI
     Install and run pre-built skills locally
     (For using existing skills in command-line interface)

○ 3. Claude API
     Programmatic skill management endpoints
     (For API integration and automation)

Which are you working with?"

After user selects option 1 (Agent SDK):
→ Read all 5 Agent SDK docs about skills
→ Synthesize unified answer within that context
→ Present with sources
```

### Content Search Strategies

**Priority order for finding relevant information**:

1. **Explicit context in query** → Filter to that product first
   - "hooks in agent sdk" → Search only agent-sdk category
   - "cli memory features" → Search only claude_code category
   - "api authentication" → Search only api_reference category

2. **Keyword extraction** → Full-text content search across all docs
   - "best practices for extended thinking"
   - Extract: ["best practices", "extended thinking"]
   - Search document content, not just paths

3. **No exact path match** → Search document content anyway
   - Query: "how do I use memory in agent sdk?"
   - No `/agent-sdk/memory.md` path exists
   - But `/agent-sdk/python.md` contains extensive memory documentation
   - Find it via content search, read it, extract relevant sections

### Decision Logic (Pseudo-code)

```python
def handle_docs_query(user_query):
    # Step 1: Extract intent and context from query
    intent = extract_intent(user_query)  # what they want to know
    context = extract_context(user_query)  # which product (if specified)
    keywords = extract_keywords(user_query)

    # Step 2: Search with context filter if available
    if context:  # e.g., "in agent sdk", "cli hooks"
        matches = search_content(keywords, category_filter=context)
    else:
        matches = search_content(keywords)  # search everywhere

    # Step 3: Analyze results
    if len(matches) == 0:
        return suggest_alternatives()

    categories = get_product_contexts(matches)

    # Step 4: Decide action based on context analysis
    if len(categories) == 1:
        # ✅ Same product context → SYNTHESIZE
        docs = read_all_matching_docs(matches)
        answer = synthesize_unified_answer(docs, intent)
        return present_with_sources(answer, matches)

    else:
        # ❓ Different product contexts → ASK
        options = format_product_options(categories)
        selected_category = ask_user_question(options)

        # Then synthesize within selected context
        filtered_matches = filter_by_category(matches, selected_category)
        docs = read_all_matching_docs(filtered_matches)
        answer = synthesize_unified_answer(docs, intent)
        return present_with_sources(answer, filtered_matches)
```

### Example Workflows

#### Example 1: Clear context, multiple docs (synthesize)
```
User: /docs how do I use memory in the agent sdk?

Analysis:
- Intent: how-to question about memory
- Context: agent sdk (explicitly stated)
- Type: implementation guidance

Search: Content search in agent_sdk category for "memory"
Found:
- /en/docs/agent-sdk/python.md (12 mentions)
- /en/docs/agent-sdk/overview.md (5 mentions)
- /en/docs/agent-sdk/sessions.md (8 mentions)

Decision: All same context (Agent SDK) → SYNTHESIZE

Action:
1. Read all three docs silently
2. Extract memory-related sections
3. Combine into unified explanation

Output:
"In the Claude Agent SDK, memory allows agents to maintain state across interactions...

[Unified explanation from all three docs]
[Code examples from python.md]
[Architecture details from overview.md]
[Session persistence from sessions.md]

Sources:
• Agent SDK Python Guide: https://docs.claude.com/en/docs/agent-sdk/python
• Agent SDK Overview: https://docs.claude.com/en/docs/agent-sdk/overview
• Sessions: https://docs.claude.com/en/docs/agent-sdk/sessions"
```

#### Example 2: Ambiguous context (ask, then synthesize)
```
User: /docs memory

Analysis:
- Intent: general query about memory
- Context: UNCLEAR (not specified)
- Type: general information

Search: Content search across all categories for "memory"
Found in multiple product contexts:
- claude_code (2 docs) - CLI memory management features
- api_reference (3 docs) - Memory API endpoints
- core_documentation (4 docs) - Memory tool for agents

Decision: Different products, different use cases → ASK

Ask:
"Memory features exist in different Claude products:

○ 1. Claude Code CLI
     Local memory management for command-line interface

○ 2. Claude API
     Memory API endpoints for programmatic access

○ 3. Claude Documentation
     Memory tool for building agents

Which are you interested in?"

User selects: 1 (Claude Code CLI)

Then:
→ Filter to claude_code category only
→ Read both CLI memory docs
→ Synthesize unified CLI memory answer
→ Present with sources
```

#### Example 3: Complex integration question (synthesize)
```
User: /docs how do agent sdk skills interact with mcp servers?

Analysis:
- Intent: integration/how-to
- Context: agent sdk (explicit)
- Keywords: ["skills", "mcp", "integration"]

Search: Content search in agent_sdk for "skills" AND "mcp"
Found:
- /en/docs/agent-sdk/skills.md
- /en/docs/agent-sdk/mcp.md
- /en/docs/agent-sdk/plugins.md

Decision: All same context (Agent SDK) → SYNTHESIZE

Action:
1. Read all three docs
2. Find sections about skills+MCP integration
3. Synthesize unified integration guide

Output:
"Agent SDK skills can interact with MCP servers in several ways:

[Unified explanation showing integration patterns]
[Skill configuration examples from skills.md]
[MCP server setup from mcp.md]
[Plugin considerations from plugins.md]

Sources: ..."
```

### Implementation Checklist

- [ ] Content search is the default (not just path matching)
- [ ] Read multiple docs silently without asking user
- [ ] Synthesize aggressively within same product context
- [ ] Only ask when crossing product boundaries
- [ ] Extract context hints from query ("in agent sdk", "cli hooks")
- [ ] Cite all sources at the end
- [ ] Graceful degradation if Python unavailable (basic path matching + suggestions)

## Python-Enhanced Features

When Python 3.9+ is installed, these additional capabilities are available:

- **Full-text search**: `--search "keyword"` searches across all documentation content
- **Category filtering**: `--category api` lists paths in specific categories
- **Path validation**: `--validate` checks documentation integrity
- **Active documentation**: Access to 573 paths across 6 categories:
  - API Reference (377 paths, 65.8%) - Includes multi-language SDK docs (Python, TypeScript, Go, Java, Kotlin, Ruby)
  - Core Documentation (82 paths, 14.3%)
  - Prompt Library (65 paths, 11.3%)
  - Claude Code (46 paths, 8.0%)
  - Release Notes (2 paths)
  - Resources (1 path)

See `enhancements/` directory for comprehensive feature documentation and examples.

## Repository Structure

```
/
├── docs/                   # 571 documentation files (.md format)
│   ├── docs_manifest.json  # File tracking manifest
│   └── .search_index.json  # Full-text search index (Python-generated)
├── scripts/
│   ├── claude-docs-helper.sh       # Main helper (feature detection)
│   ├── fetch_claude_docs.py        # Thin wrapper for fetcher package
│   ├── lookup_paths.py             # Thin wrapper for lookup package
│   ├── build_search_index.py       # Index builder (Python)
│   ├── fetcher/                    # Documentation fetching package
│   │   ├── __init__.py             # Package exports
│   │   ├── config.py               # Constants and safety thresholds
│   │   ├── manifest.py             # Manifest file operations
│   │   ├── paths.py                # Path conversion and categorization
│   │   ├── sitemap.py              # Sitemap discovery and parsing
│   │   ├── content.py              # Content fetching and validation
│   │   ├── safeguards.py           # Safety checks (deletion prevention)
│   │   └── cli.py                  # Main entry point
│   └── lookup/                     # Search and validation package
│       ├── __init__.py             # Package exports
│       ├── config.py               # Configuration constants
│       ├── manifest.py             # Manifest loading utilities
│       ├── search.py               # Search functionality
│       ├── validation.py           # Path validation
│       ├── formatting.py           # Output formatting
│       └── cli.py                  # Main entry point
├── paths_manifest.json     # Active paths manifest (573 paths, 6 categories)
├── archive/               # Archived/deprecated scripts (git-ignored)
├── enhancements/          # Feature documentation
│   ├── README.md          # Overview
│   ├── FEATURES.md        # Technical specs
│   ├── CAPABILITIES.md    # Detailed capabilities
│   └── EXAMPLES.md        # Usage examples
├── tests/                 # Test suite (294 tests, 294 passing)
├── install.sh            # Installation script
└── CLAUDE.md             # This file (AI context)

```

## Files to Think About

When working on this repository:

### Core Files
@install.sh - Installation script
@README.md - User documentation
@CONTRIBUTING.md - Contribution guidelines
@scripts/claude-docs-helper.sh - Main entry point (feature detection)
@uninstall.sh - Clean removal

### Python Features
@scripts/fetch_claude_docs.py - Thin wrapper for fetcher package (backwards compatible)
@scripts/lookup_paths.py - Thin wrapper for lookup package (backwards compatible)
@scripts/fetcher/ - Documentation fetching package (8 modules)
@scripts/lookup/ - Search & validation package (7 modules)
@scripts/build_search_index.py - Full-text search indexing
@paths_manifest.json - Active paths manifest (573 paths, 6 categories)
@tests/ - Test suite (294 tests)

### Automation
@.github/workflows/ - Auto-update workflows (runs every 3 hours)

## Documentation Deletion Safeguards

The automated sync system includes multiple safeguards to prevent catastrophic documentation loss. These were implemented after a critical bug where 80%+ of documentation was deleted due to broken sitemap URLs.

### Safety Thresholds (in `scripts/fetcher/config.py`)

| Constant | Value | Purpose |
|----------|-------|---------|
| `MIN_DISCOVERY_THRESHOLD` | 200 | Minimum paths that must be discovered from sitemaps |
| `MAX_DELETION_PERCENT` | 10 | Maximum percentage of files that can be deleted in one sync |
| `MIN_EXPECTED_FILES` | 250 | Minimum files that must remain after sync |

### How Safeguards Work

1. **Discovery Validation**: Before fetching, validates that sitemap discovery found enough paths
2. **Deletion Limiting**: `cleanup_old_files()` refuses to delete more than 10% of existing files
3. **File Count Validation**: Refuses to proceed if result would have fewer than 250 files
4. **Workflow Validation**: GitHub Actions validates sync success before committing

### Sitemap Sources

Documentation is discovered from two sitemaps:
- `https://platform.claude.com/sitemap.xml` - Platform documentation (API, guides, etc.)
- `https://code.claude.com/docs/sitemap.xml` - Claude Code CLI documentation

### Filename Conventions

Files are named based on their source:
- Platform docs: `en__docs__section__page.md` (double underscore for path separators)
- Claude Code docs: `docs__en__page.md` (prefixed with `docs__`)

## Working on This Repository

**Critical Rule**: Changes must maintain graceful degradation - work with AND without Python.

### Feature Detection
The helper script checks Python availability at runtime:
```bash
if command -v python3 &> /dev/null && [ -f "$SCRIPTS_DIR/lookup_paths.py" ]; then
    # Python features available - use enhanced search/validation
else
    # Python not available - use basic shell features only
fi
```

### Testing
```bash
# Test basic features (always works)
./scripts/claude-docs-helper.sh hooks

# Test Python features (requires Python 3.9+)
python3 scripts/lookup_paths.py --search "mcp"
pytest tests/ -v

# Run full test suite
pytest tests/ -q  # Should see: 294 passed, 2 skipped
```

## Upstream Compatibility

This enhanced edition maintains compatibility with upstream (ericbuess/claude-code-docs):
- Same installation location (~/.claude-code-docs)
- Same `/docs` command interface
- Python features are additive, not breaking
- Works without Python (graceful degradation)
