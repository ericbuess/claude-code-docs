# Upstream Repository Structure Analysis

**Repository**: costiash/claude-code-docs
**Clone Location**: /home/rudycosta3/claude-code-docs/upstream/
**Analysis Date**: 2025-11-03

## Directory Tree

```
claude-code-docs/
├── .git/                   # Git repository metadata
├── .github/
│   └── workflows/
│       ├── claude-code-review.yml    # Claude Code PR review automation
│       ├── claude.yml                # Claude integration workflow
│       └── update-docs.yml           # Main documentation update workflow (runs every 3 hours)
├── docs/                   # Mirrored documentation files (47 markdown files)
│   ├── *.md                # Individual documentation pages
│   └── docs_manifest.json  # Manifest tracking all fetched files with hashes and URLs
├── scripts/
│   ├── fetch_claude_docs.py           # Main documentation fetcher (646 lines, Python 3.11+)
│   ├── claude-docs-helper.sh.template # Template for user-facing helper script
│   └── requirements.txt               # Python dependencies (requests==2.32.4)
├── CLAUDE.md               # Instructions for Claude Code when working in this repo
├── README.md               # User-facing documentation (216 lines)
├── LICENSE                 # Project license
├── .gitignore              # Git ignore rules
├── install.sh              # Installation script (538 lines, bash)
├── uninstall.sh            # Uninstallation script (147 lines, bash)
└── UNINSTALL.md            # Uninstallation instructions
```

## File Counts

- **Total Markdown Docs**: 47 files in `/docs/`
- **Workflows**: 3 GitHub Actions workflows
- **Scripts**: 2 main scripts (Python fetcher + bash helper template)
- **Installation Files**: 2 scripts (install.sh + uninstall.sh)

## Key Directories

### `/docs/` - Documentation Mirror
- **Purpose**: Local mirror of Claude Code documentation from docs.anthropic.com
- **Contents**: 47 markdown files representing individual documentation topics
- **Special File**: `docs_manifest.json` - tracks metadata for each file:
  - Original URL (HTML version)
  - Original markdown URL (.md version)
  - SHA256 content hash for change detection
  - Last update timestamp
- **Update Strategy**: Files only updated when content hash changes
- **Coverage**: Claude Code documentation only (not full Anthropic docs)

### `/scripts/` - Automation Scripts
- **fetch_claude_docs.py**: Main documentation fetcher (646 lines)
  - Discovers pages from sitemap.xml
  - Fetches markdown content from docs.anthropic.com
  - Validates content before saving
  - Tracks changes with SHA256 hashing
  - Handles rate limiting and retries
  - Generates manifest file
  - Also fetches CHANGELOG.md from GitHub

- **claude-docs-helper.sh.template**: User-facing helper script template
  - Handles `/docs` command functionality
  - Auto-updates from GitHub
  - Sanitizes user input
  - Shows documentation freshness
  - Provides search functionality

- **requirements.txt**: Single dependency
  - requests==2.32.4

### `/.github/workflows/` - CI/CD Automation
Three GitHub Actions workflows:

1. **update-docs.yml** (Primary workflow)
   - Runs every 3 hours via cron schedule
   - Manual trigger supported
   - Fetches latest documentation
   - Commits changes if detected
   - Creates issue on failure

2. **claude.yml**: Claude integration workflow
   - Purpose: TBD (need to examine file)

3. **claude-code-review.yml**: PR review automation
   - Purpose: Automated code review via Claude

### Installation System
- **install.sh** (538 lines): Comprehensive installer
  - Detects OS (macOS/Linux)
  - Checks dependencies (git, jq, curl)
  - Finds and migrates old installations
  - Clones to fixed location: `~/.claude-code-docs`
  - Creates `/docs` slash command
  - Sets up auto-update hook in `~/.claude/settings.json`
  - Handles version upgrades gracefully

- **uninstall.sh** (147 lines): Smart uninstaller
  - Discovers installations from config files
  - Removes slash command
  - Removes hooks from settings.json
  - Optionally removes installation directory
  - Preserves uncommitted changes

## Key Files

### `docs_manifest.json`
- **Purpose**: Tracks all fetched documentation files
- **Structure**:
  ```json
  {
    "files": {
      "filename.md": {
        "original_url": "...",
        "original_md_url": "...",
        "hash": "sha256...",
        "last_updated": "ISO timestamp"
      }
    },
    "fetch_metadata": {
      "last_fetch_completed": "...",
      "fetch_duration_seconds": ...,
      "total_pages_discovered": ...,
      ...
    },
    "base_url": "https://raw.githubusercontent.com/...",
    "last_updated": "..."
  }
  ```
- **Usage**: Change detection, URL mapping, status tracking

### `CLAUDE.md`
- **Purpose**: Instructions for Claude Code when working in the repository
- **Contents**: Brief project description and key files to examine
- **Philosophy**: Helps Claude understand project context

### `README.md`
- **Purpose**: User-facing documentation
- **Sections**:
  - Installation instructions
  - Usage examples
  - Update mechanism explanation
  - Troubleshooting
  - Platform compatibility
  - Contributing guidelines
  - Version history

## File Organization Patterns

1. **Flat Documentation Structure**: All docs in single `/docs/` directory with no subdirectories
   - Simplifies access and management
   - File naming uses underscores (e.g., `amazon-bedrock.md`, `google-vertex-ai.md`)

2. **Template-Based Installation**: Helper script uses template approach
   - `claude-docs-helper.sh.template` → `claude-docs-helper.sh` during install
   - No runtime path placeholders needed (uses fixed `~/.claude-code-docs`)

3. **Git-Based Updates**: Leverages git for synchronization
   - Auto-update via `git pull` in hook
   - Change tracking via git commits
   - GitHub Actions for scheduled updates

4. **Metadata-Driven**: Manifest file drives functionality
   - Available topics list
   - Change detection
   - URL mapping for official docs links

## Design Philosophy

1. **Simplicity**: Minimal dependencies (just requests for Python, jq for bash)
2. **Robustness**: Extensive error handling and retry logic
3. **Safety**: Input sanitization, validation, uncommitted change preservation
4. **Transparency**: Clear status messages, links to official docs
5. **User-Focused**: Natural language commands, helpful error messages
6. **Git-Native**: Leverages git for versioning and distribution

## Notable Implementation Details

- **Fixed Installation Path**: Always `~/.claude-code-docs` (v0.3+)
- **Version Tracking**: Script version embedded in helper script
- **Cross-Platform**: macOS and Linux support (Windows not yet supported)
- **Offline Capable**: Works with cached docs if GitHub unavailable
- **Search Feature**: Keyword-based doc search in helper script
- **Changelog Integration**: Fetches Claude Code CHANGELOG.md from GitHub

## Differences from Typical Documentation Mirrors

1. **Integration Focus**: Designed specifically for Claude Code integration
2. **Auto-Update Hooks**: Uses Claude Code hooks for transparent updates
3. **Slash Command Interface**: `/docs` command rather than manual file access
4. **Metadata Rich**: Extensive manifest with hashes, timestamps, URLs
5. **Smart Updates**: Only fetches changed content, not full refresh
