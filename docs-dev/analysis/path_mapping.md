# Path Mapping and Directory Structure Analysis

**Analysis Date**: 2025-11-03
**Repository**: costiash/claude-code-docs

## Path-to-File Mapping Rules

### Source URLs
Documentation lives at:
- **Base URL**: `https://docs.anthropic.com`
- **Path Pattern**: `/en/docs/claude-code/{topic}`
- **Markdown URL**: `https://docs.anthropic.com/en/docs/claude-code/{topic}.md`

### Local File Mapping

#### Simple Paths (No Subdirectories)
```
URL Path                                  → Local File
/en/docs/claude-code/hooks                → docs/hooks.md
/en/docs/claude-code/memory               → docs/memory.md
/en/docs/claude-code/mcp                  → docs/mcp.md
/en/docs/claude-code/github-actions       → docs/github-actions.md
/en/docs/claude-code/amazon-bedrock       → docs/amazon-bedrock.md
```

**Rule**: Strip prefix `/en/docs/claude-code/`, add `.md` extension

#### Nested Paths (With Subdirectories)
```
URL Path                                    → Local File
/en/docs/claude-code/advanced/setup         → docs/advanced__setup.md
/en/docs/claude-code/integrations/vscode    → docs/integrations__vscode.md
/en/docs/claude-code/sub/dir/page           → docs/sub__dir__page.md
```

**Rule**: Replace `/` with `__` (double underscore), add `.md` extension

### Filename Conversion Algorithm

```python
def url_to_safe_filename(url_path):
    # 1. Remove known prefixes
    for prefix in ['/en/docs/claude-code/', '/docs/claude-code/', '/claude-code/']:
        if prefix in url_path:
            path = url_path.split(prefix)[-1]
            break
    else:
        # Fallback: take everything after 'claude-code/'
        if 'claude-code/' in url_path:
            path = url_path.split('claude-code/')[-1]
        else:
            path = url_path

    # 2. Handle simple vs nested paths
    if '/' not in path:
        # Simple: just add .md
        return path + '.md' if not path.endswith('.md') else path

    # 3. Nested: replace / with __
    safe_name = path.replace('/', '__')
    if not safe_name.endswith('.md'):
        safe_name += '.md'
    return safe_name
```

### Naming Convention Examples

**Actual Files from Upstream**:
```
docs/
├── amazon-bedrock.md
├── analytics.md
├── changelog.md
├── checkpointing.md
├── claude-code-on-the-web.md
├── cli-reference.md
├── common-workflows.md
├── costs.md
├── data-usage.md
├── devcontainer.md
├── github-actions.md
├── gitlab-ci-cd.md
├── google-vertex-ai.md
├── headless.md
├── hooks.md
├── hooks-guide.md
├── iam.md
├── interactive-mode.md
├── jetbrains.md
├── legal-and-compliance.md
├── llm-gateway.md
├── mcp.md
├── memory.md
├── model-config.md
├── monitoring-usage.md
├── network-config.md
├── output-styles.md
├── overview.md
├── plugin-marketplaces.md
├── plugins.md
├── plugins-reference.md
├── quickstart.md
├── sandboxing.md
├── sdk__migration-guide.md   ← Note: double underscore for nested path
├── security.md
├── settings.md
├── setup.md
├── skills.md
├── slash-commands.md
├── statusline.md
├── sub-agents.md
├── terminal-config.md
├── third-party-integrations.md
├── troubleshooting.md
└── vs-code.md
```

**Special Case**: `sdk__migration-guide.md` suggests original path was `/en/docs/claude-code/sdk/migration-guide`

### Character Encoding

**Allowed Characters**:
- Letters: a-z, A-Z
- Numbers: 0-9
- Separators: `-` (hyphen), `_` (underscore)
- Extension: `.md`

**Conversion Rules**:
- Spaces in URLs → hyphens in filenames
- Forward slashes → double underscores
- All lowercase (from URL structure)

## Directory Hierarchy Strategy

### Flat Structure (Current Implementation)

```
claude-code-docs/
└── docs/              ← All files in single directory
    ├── file1.md
    ├── file2.md
    ├── nested__path.md
    └── docs_manifest.json
```

**Advantages**:
- Simple to manage
- Easy glob patterns
- No directory creation needed
- Flat namespace

**Trade-offs**:
- Can't preserve original hierarchy visually
- Long filenames for nested paths
- Less intuitive browsing

### Alternative: Nested Structure (Not Used)

```
claude-code-docs/
└── docs/
    ├── core/
    │   ├── overview.md
    │   └── setup.md
    ├── integrations/
    │   ├── vscode.md
    │   └── jetbrains.md
    └── advanced/
        └── hooks.md
```

**Why Not Used**:
- More complex directory management
- Requires category mapping
- More complicated path resolution
- Current docs don't have deep nesting

## Reverse Mapping: File to URL

### From Filename to Official URL

```python
# Given filename: hooks.md
topic = filename.replace('.md', '')  # → "hooks"

# For simple filenames (no __)
if '__' not in topic:
    official_url = f"https://docs.anthropic.com/en/docs/claude-code/{topic}"
    # → https://docs.anthropic.com/en/docs/claude-code/hooks

# For nested filenames (with __)
else:
    nested_path = topic.replace('__', '/')
    official_url = f"https://docs.anthropic.com/en/docs/claude-code/{nested_path}"
    # sdk__migration-guide → https://docs.anthropic.com/en/docs/claude-code/sdk/migration-guide
```

### Manifest-Based URL Lookup

**Preferred Method** (more reliable):
```python
manifest = json.load(open('docs/docs_manifest.json'))
file_info = manifest['files']['hooks.md']
official_url = file_info['original_url']
markdown_url = file_info['original_md_url']
```

**Manifest Entry Structure**:
```json
{
  "hooks.md": {
    "original_url": "https://docs.anthropic.com/en/docs/claude-code/hooks",
    "original_md_url": "https://docs.anthropic.com/en/docs/claude-code/hooks.md",
    "hash": "a2b34e93f4ec393eeefbd65a15a7c1b7cbc238e3e63eaaff951564306b0edf82",
    "last_updated": "2025-11-01T21:01:25.235828"
  }
}
```

## .claude/ Integration Details

### Slash Command Configuration

**Location**: `~/.claude/commands/docs.md`

**Structure**:
```markdown
Execute the Claude Code Docs helper script at ~/.claude-code-docs/claude-docs-helper.sh

Usage:
- /docs - List all available documentation topics
- /docs <topic> - Read specific documentation with link to official docs
- /docs -t - Check sync status without reading a doc
- /docs -t <topic> - Check freshness then read documentation
- /docs whats new - Show recent documentation changes

[Examples...]

Execute: ~/.claude-code-docs/claude-docs-helper.sh "$ARGUMENTS"
```

**Key Points**:
- Command file tells Claude to execute helper script
- `$ARGUMENTS` passes user input to script
- Helper script handles all logic (search, validation, output)

### Hook Configuration

**Location**: `~/.claude/settings.json`

**Hook Structure**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "~/.claude-code-docs/claude-docs-helper.sh hook-check"
          }
        ]
      }
    ]
  }
}
```

**Purpose**:
- Triggers before Read tool is used
- Runs `hook-check` command
- Automatically updates docs from GitHub if changes available
- Transparent to user (happens in background)

### Helper Script Integration

**Location**: `~/.claude-code-docs/claude-docs-helper.sh`

**Key Functions**:

1. **auto_update()**: Checks GitHub for updates, pulls if behind
   ```bash
   git fetch --quiet origin main
   git pull --quiet origin main
   ```

2. **read_doc()**: Read documentation file and show official URL
   ```bash
   topic=$(sanitize_input "$1")
   doc_path="$DOCS_PATH/docs/${topic}.md"
   cat "$doc_path"
   echo "📖 Official page: https://docs.anthropic.com/en/docs/claude-code/$topic"
   ```

3. **show_freshness()**: Display sync status with GitHub
   ```bash
   git fetch origin main
   git rev-list HEAD..origin/main --count  # commits behind
   git rev-list origin/main..HEAD --count  # commits ahead
   ```

## Topic Discovery

### List Available Topics

```bash
# From helper script
ls "$DOCS_PATH/docs" | grep '\.md$' | sed 's/\.md$//' | sort
```

**Output**:
```
amazon-bedrock
analytics
changelog
checkpointing
...
```

### Search for Topics

```bash
# Extract keywords from user query
keywords=$(echo "$topic" | grep -o '[a-zA-Z0-9_-]\+' |
           grep -v -E '^(tell|me|about|explain|what|...)$')

# Search filenames
matches=$(ls "$DOCS_PATH/docs" | grep '\.md$' | sed 's/\.md$//' |
          grep -i -E "$(echo "$keywords" | tr ' ' '|')")
```

**Example**:
- User: `/docs tell me about hooks`
- Keywords: `hooks`
- Matches: `hooks.md`, `hooks-guide.md`

## Path Resolution Flow

### User Input → File Path

```
User: /docs hooks
  ↓
Command: ~/.claude-code-docs/claude-docs-helper.sh hooks
  ↓
Sanitize: "hooks" → "hooks" (no special chars)
  ↓
Construct: $DOCS_PATH/docs/hooks.md
  ↓
Resolve: ~/.claude-code-docs/docs/hooks.md
  ↓
Verify: File exists? Yes
  ↓
Read & Display
```

### User Input → Official URL

```
Filename: hooks.md
  ↓
Load manifest: docs_manifest.json
  ↓
Lookup: manifest['files']['hooks.md']['original_url']
  ↓
Display: https://docs.anthropic.com/en/docs/claude-code/hooks
```

## Special Paths

### Changelog (Special Case)
```
Source: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
Local: docs/changelog.md
Display: Different header and footer attribution
```

**Manifest Entry**:
```json
{
  "changelog.md": {
    "original_url": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
    "original_raw_url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
    "hash": "...",
    "last_updated": "...",
    "source": "claude-code-repository"
  }
}
```

### Manifest File
```
Path: docs/docs_manifest.json
Purpose: Metadata, not documentation
Never deleted by cleanup
Not listed in topic listings
```

## Path Sanitization

### Input Sanitization (Security)

```bash
sanitize_input() {
    # Remove ALL shell metacharacters
    # Only allow: alphanumeric, spaces, hyphens, underscores, periods, commas, apostrophes, question marks
    echo "$1" | sed 's/[^a-zA-Z0-9 _.,'\''?-]//g' |
                sed 's/  */ /g' |
                sed 's/^ *//;s/ *$//'
}
```

**Example**:
- Input: `/docs hooks; rm -rf /`
- Sanitized: `hooks rm rf`
- Result: No file match, safe error

### .md Extension Handling

```bash
# User can provide or omit .md extension
topic="${topic%.md}"  # Strip .md if present
doc_path="$DOCS_PATH/docs/${topic}.md"  # Always add .md
```

**Examples**:
- `/docs hooks` → `docs/hooks.md` ✓
- `/docs hooks.md` → `docs/hooks.md` ✓
- `/docs hooks.txt` → `docs/hooks.md` ✓ (txt stripped, md added)

## GitHub Raw URLs (Manifest)

### Base URL Construction

```python
github_repo = os.environ.get('GITHUB_REPOSITORY', 'ericbuess/claude-code-docs')
github_ref = os.environ.get('GITHUB_REF_NAME', 'main')

manifest["base_url"] = f"https://raw.githubusercontent.com/{github_repo}/{github_ref}/docs/"
```

**Example**:
```
base_url: https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/
filename: hooks.md
full_url: https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/docs/hooks.md
```

**Purpose**:
- Allows direct linking to raw markdown files
- Used by consumers of the manifest
- Alternative access method to git clone

## Key Takeaways

1. **Flat Structure**: All docs in single `/docs/` directory
2. **Double Underscore**: Nested paths use `__` separator
3. **Manifest-Driven**: URLs stored in manifest for reliable reverse lookup
4. **Sanitization**: Input cleaned to prevent command injection
5. **Simple Mapping**: URL path suffix → filename with `.md`
6. **Helper Script**: Centralized logic for all path operations
7. **Git-Based Updates**: Auto-sync via git pull in hooks
8. **Dual URLs**: Both official docs and raw GitHub URLs available
9. **Extension Flexibility**: `.md` can be included or omitted by user
10. **Security First**: Multiple layers of input validation
