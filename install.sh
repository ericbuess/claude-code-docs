#!/bin/bash
set -euo pipefail

# Claude Code Docs Installer v0.3.4 - Enhanced edition with extended documentation coverage
# This script installs claude-code-docs to ~/.claude-code-docs
# Installation Strategy: Always perform a fresh installation at the fixed location
#   1. Remove any existing installation at ~/.claude-code-docs (with user confirmation)
#   2. Clone fresh from GitHub
#   3. Set up commands and hooks
#   4. Clean up any old installations in other locations

echo "Claude Code Docs Installer v0.3.4"
echo "==============================="

# Fixed installation location
INSTALL_DIR="$HOME/.claude-code-docs"

# Branch to use for installation
INSTALL_BRANCH="main"

# Detect OS type
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS_TYPE="macos"
    echo "✓ Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS_TYPE="linux"
    echo "✓ Detected Linux"
else
    echo "❌ Error: Unsupported OS type: $OSTYPE"
    echo "This installer supports macOS and Linux only"
    exit 1
fi

# Check dependencies
echo "Checking dependencies..."
for cmd in git jq curl; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "❌ Error: $cmd is required but not installed"
        echo "Please install $cmd and try again"
        exit 1
    fi
done
echo "✓ All dependencies satisfied"


# Function to check and remove existing installation at ~/.claude-code-docs
check_and_remove_existing_install() {
    # Check if installation directory already exists
    if [[ ! -d "$INSTALL_DIR" ]]; then
        return 0  # Nothing to remove
    fi

    # Check for uncommitted changes if it's a git repo
    local has_uncommitted_changes=false
    if [[ -d "$INSTALL_DIR/.git" ]]; then
        local original_dir=$(pwd)
        if cd "$INSTALL_DIR" 2>/dev/null; then
            if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
                has_uncommitted_changes=true
            fi
            cd "$original_dir" || exit 1
        fi
    fi

    # Auto-proceed if no uncommitted changes OR auto-install mode enabled
    if [[ "$has_uncommitted_changes" == "false" ]] || [[ "${CLAUDE_DOCS_AUTO_INSTALL:-}" == "yes" ]]; then
        if [[ "${CLAUDE_DOCS_AUTO_INSTALL:-}" == "yes" ]]; then
            echo "🔄 Auto-install mode: Removing existing installation..."
        else
            echo "🔄 Existing installation detected - updating to latest version..."
        fi
        rm -rf "$INSTALL_DIR"
        echo "✓ Ready for fresh installation"
        echo ""
        return 0
    fi

    # Only prompt if there are uncommitted changes
    echo ""
    echo "⚠️  WARNING: Existing installation has uncommitted changes!"
    echo "   Location: $INSTALL_DIR"
    echo "   All local modifications will be lost."
    echo ""

    # Try to get user confirmation
    if [[ -t 0 ]]; then
        # Interactive terminal
        read -p "Continue and delete existing installation? [y/N]: " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "Installation cancelled. Your changes are preserved."
            exit 0
        fi
    else
        # Non-interactive (piped input, CI/CD)
        echo "❌ Cannot proceed: Non-interactive mode with uncommitted changes"
        echo ""
        echo "Options:"
        echo "  • Commit your changes: cd $INSTALL_DIR && git add . && git commit"
        echo "  • Force auto-install: CLAUDE_DOCS_AUTO_INSTALL=yes curl ... | bash"
        echo "  • Download and run interactively: curl ... -o install.sh && bash install.sh"
        echo ""
        exit 1
    fi

    # Remove the directory
    echo "Removing existing installation..."
    rm -rf "$INSTALL_DIR"
    echo "✓ Existing installation removed"
    echo ""
}


# Function to find existing installations from configs
find_existing_installations() {
    local paths=()
    
    # Check command file for paths
    if [[ -f ~/.claude/commands/docs.md ]]; then
        # Look for paths in the command file
        # v0.1 format: LOCAL DOCS AT: /path/to/claude-code-docs/docs/
        # v0.2+ format: Execute: /path/to/claude-code-docs/helper.sh
        while IFS= read -r line; do
            # v0.1 format
            if [[ "$line" =~ LOCAL\ DOCS\ AT:\ ([^[:space:]]+)/docs/ ]]; then
                local path="${BASH_REMATCH[1]}"
                path="${path/#\~/$HOME}"
                [[ -d "$path" ]] && paths+=("$path")
            fi
            # v0.2+ format
            if [[ "$line" =~ Execute:.*claude-code-docs ]]; then
                # Extract path from various formats
                local path=$(echo "$line" | grep -o '[^ "]*claude-code-docs[^ "]*' | head -1)
                path="${path/#\~/$HOME}"
                
                # Get directory part
                if [[ -d "$path" ]]; then
                    paths+=("$path")
                elif [[ -d "$(dirname "$path")" ]] && [[ "$(basename "$(dirname "$path")")" == "claude-code-docs" ]]; then
                    paths+=("$(dirname "$path")")
                fi
            fi
        done < ~/.claude/commands/docs.md
    fi
    
    # Check settings.json hooks for paths
    if [[ -f ~/.claude/settings.json ]]; then
        local hooks=$(jq -r '.hooks.PreToolUse[]?.hooks[]?.command // empty' ~/.claude/settings.json 2>/dev/null)
        while IFS= read -r cmd; do
            if [[ "$cmd" =~ claude-code-docs ]]; then
                # Extract paths from v0.1 complex hook format
                # Look for patterns like: "/path/to/claude-code-docs/.last_check"
                local v01_paths=$(echo "$cmd" | grep -o '"[^"]*claude-code-docs[^"]*"' | sed 's/"//g' || true)
                while IFS= read -r path; do
                    [[ -z "$path" ]] && continue
                    # Extract just the directory part
                    if [[ "$path" =~ (.*/claude-code-docs)(/.*)?$ ]]; then
                        path="${BASH_REMATCH[1]}"
                        path="${path/#\~/$HOME}"
                        [[ -d "$path" ]] && paths+=("$path")
                    fi
                done <<< "$v01_paths"
                
                # Also try v0.2+ simpler format
                local found=$(echo "$cmd" | grep -o '[^ "]*claude-code-docs[^ "]*' || true)
                while IFS= read -r path; do
                    [[ -z "$path" ]] && continue
                    path="${path/#\~/$HOME}"
                    # Clean up path to get the claude-code-docs directory
                    if [[ "$path" =~ (.*/claude-code-docs)(/.*)?$ ]]; then
                        path="${BASH_REMATCH[1]}"
                    fi
                    [[ -d "$path" ]] && paths+=("$path")
                done <<< "$found"
            fi
        done <<< "$hooks"
    fi
    
    # Also check current directory if running from an installation
    if [[ -f "./docs/docs_manifest.json" && "$(pwd)" != "$INSTALL_DIR" ]]; then
        paths+=("$(pwd)")
    fi
    
    # Deduplicate and exclude new location
    if [[ ${#paths[@]} -gt 0 ]]; then
        printf '%s\n' "${paths[@]}" | grep -v "^$INSTALL_DIR$" | sort -u
    fi
}

# Function to check if Python features are available
check_python_features() {
    # Check Python version (need 3.9+ for enhanced search/validation features)
    if ! command -v python3 &> /dev/null; then
        return 1
    fi

    local python_version=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")' 2>/dev/null || echo "0.0")
    local python_major=$(echo "$python_version" | cut -d. -f1)
    local python_minor=$(echo "$python_version" | cut -d. -f2)

    if [[ "$python_major" -lt 3 ]] || [[ "$python_major" -eq 3 && "$python_minor" -lt 9 ]]; then
        return 1
    fi

    # Check if paths_manifest.json exists
    if [[ ! -f "$INSTALL_DIR/paths_manifest.json" ]]; then
        return 1
    fi

    # Python features available if we have Python 3.9+ and the manifest
    return 0
}

# Function to cleanup old installations
cleanup_old_installations() {
    # Use the global OLD_INSTALLATIONS array that was populated before config updates
    if [[ ${#OLD_INSTALLATIONS[@]} -eq 0 ]]; then
        return
    fi

    echo ""
    echo "Cleaning up old installations..."
    echo "Found ${#OLD_INSTALLATIONS[@]} old installation(s) to remove:"
    
    for old_dir in "${OLD_INSTALLATIONS[@]}"; do
        # Skip empty paths
        if [[ -z "$old_dir" ]]; then
            continue
        fi
        
        echo "  - $old_dir"

        # SAFETY CHECK 1: Never delete current working directory
        if [[ "$(pwd 2>/dev/null)" == "$old_dir" ]]; then
            echo "    ⚠️  Preserved (current working directory)"
            continue
        fi

        # SAFETY CHECK 2: Never delete development repos (pattern: /home/*/claude-code-docs)
        if [[ "$old_dir" =~ ^/home/[^/]+/claude-code-docs$ ]]; then
            echo "    ⚠️  Preserved (likely development repository)"
            continue
        fi

        # SAFETY CHECK 3: Check if it's a development repo with GitHub remote
        if [[ -d "$old_dir/.git" ]]; then
            local original_dir=$(pwd)
            if cd "$old_dir" 2>/dev/null; then
                # Check for GitHub remote pointing to main repo
                local has_github_remote=$(git remote -v 2>/dev/null | grep -c "github.com.*claude-code-docs" || echo "0")

                if [[ "$has_github_remote" -gt 0 ]]; then
                    cd "$original_dir" || exit 1
                    echo "    ⚠️  Preserved (development repository with GitHub remote)"
                    continue
                fi

                # Check if it has uncommitted changes
                if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
                    cd "$original_dir" || exit 1
                    rm -rf "$old_dir"
                    echo "    ✓ Removed (clean installation copy)"
                else
                    cd "$original_dir" || exit 1
                    echo "    ⚠️  Preserved (has uncommitted changes)"
                fi
            else
                echo "    ⚠️  Could not access directory"
            fi
        else
            echo "    ⚠️  Preserved (not a git repo)"
        fi
    done
}

# Main installation logic
echo ""

# STAGE 1: Check and remove existing installation at fixed location
check_and_remove_existing_install

# STAGE 2: Find old installations from configs (for cleanup later)
echo "Checking for existing installations in other locations..."
existing_installs=()
while IFS= read -r line; do
    [[ -n "$line" ]] && existing_installs+=("$line")
done < <(find_existing_installations)
if [[ ${#existing_installs[@]} -gt 0 ]]; then
    OLD_INSTALLATIONS=("${existing_installs[@]}")  # Save for later cleanup
else
    OLD_INSTALLATIONS=()  # Initialize empty array
fi

if [[ ${#existing_installs[@]} -gt 0 ]]; then
    echo "Found ${#existing_installs[@]} old installation(s) in other locations:"
    for install in "${existing_installs[@]}"; do
        echo "  - $install"
    done
    echo ""
    echo "These will be cleaned up after installation."
else
    echo "No installations found in other locations."
fi

# STAGE 3: Fresh installation at ~/.claude-code-docs (atomic)
echo ""
echo "Installing to ~/.claude-code-docs..."

# Create a temporary directory for atomic installation
TEMP_INSTALL_DIR=$(mktemp -d "${TMPDIR:-/tmp}/claude-code-docs.XXXXXXXXXX") || {
    echo "❌ Error: Failed to create temporary directory"
    echo "   Please check disk space and permissions"
    exit 1
}

# Ensure temp directory is cleaned up on exit
trap 'rm -rf "$TEMP_INSTALL_DIR"' EXIT

# Clone to temporary directory
echo "  Downloading from GitHub..."
if ! git clone -b "$INSTALL_BRANCH" https://github.com/costiash/claude-code-docs.git "$TEMP_INSTALL_DIR" 2>&1; then
    echo ""
    echo "❌ Error: Failed to clone repository from GitHub"
    echo "   Possible causes:"
    echo "     • No internet connection"
    echo "     • GitHub is down"
    echo "     • git is not installed correctly"
    echo ""
    echo "   Please check your network connection and try again"
    exit 1
fi

echo "  Download complete, installing..."

# Move to final location (atomic operation)
if ! mv "$TEMP_INSTALL_DIR" "$INSTALL_DIR" 2>/dev/null; then
    echo ""
    echo "❌ Error: Failed to move installation to $INSTALL_DIR"
    echo "   Please check permissions and try again"
    exit 1
fi

# Remove trap since we've successfully moved the directory
trap - EXIT

cd "$INSTALL_DIR" || {
    echo "❌ Error: Failed to access installation directory"
    exit 1
}
echo "✓ Repository cloned successfully"

# Now we're in $INSTALL_DIR, set up the new script-based system
echo ""
echo "Setting up Claude Code Docs v0.3.4..."

# Copy enhanced helper script (not the template!)
echo "Installing helper script..."
if [[ -f "$INSTALL_DIR/scripts/claude-docs-helper.sh" ]]; then
    cp "$INSTALL_DIR/scripts/claude-docs-helper.sh" "$INSTALL_DIR/claude-docs-helper.sh"
    chmod +x "$INSTALL_DIR/claude-docs-helper.sh"
    echo "✓ Enhanced helper script installed"
else
    echo "  ⚠️  Enhanced script missing, attempting recovery..."
    # Try to fetch just the enhanced script
    if curl -fsSL "https://raw.githubusercontent.com/costiash/claude-code-docs/$INSTALL_BRANCH/scripts/claude-docs-helper.sh" -o "$INSTALL_DIR/claude-docs-helper.sh" 2>/dev/null; then
        chmod +x "$INSTALL_DIR/claude-docs-helper.sh"
        echo "  ✓ Enhanced helper script downloaded directly"
    else
        echo "  ❌ Failed to install helper script"
        echo "  Please check your installation and try again"
        exit 1
    fi
fi

# Always update command (in case it points to old location)
echo "Setting up /docs command..."
mkdir -p ~/.claude/commands

# Remove old command if it exists
if [[ -f ~/.claude/commands/docs.md ]]; then
    echo "  Updating existing command..."
fi

# Create AI-powered docs command
cat > ~/.claude/commands/docs.md << 'EOF'
# Claude Code Documentation Assistant - AI-Powered Semantic Search

You are a documentation assistant for Claude Code. Use your semantic understanding to analyze user requests and route to appropriate helper functions.

## Available Helper Functions

The helper script at `~/.claude-code-docs/claude-docs-helper.sh` provides:

1. **Direct Documentation Lookup**: `<topic>` - Read a specific documentation file
2. **Content Search**: `--search-content "<query>"` - Full-text search across all documentation (requires Python 3.9+)
3. **Path Search**: `--search "<query>"` - Fuzzy search across 270 documentation paths (requires Python 3.9+)
4. **Freshness Check**: `-t` - Check if local docs are synced with GitHub
5. **What's New**: `"what's new"` - Show recent documentation changes with diffs
6. **Help**: `--help` - Show all available commands

## Request Analysis - Use Your Semantic Understanding

Analyze the user's request (`$ARGUMENTS`) semantically and classify intent:

### 1. Direct Documentation Lookup
**User wants a specific documentation page by name**

Examples:
- `/docs hooks` → wants hooks documentation
- `/docs mcp` → wants MCP documentation
- `/docs settings` → wants settings documentation
- `/docs memory` → wants memory features documentation

**Action**: Execute direct lookup
```bash
~/.claude-code-docs/claude-docs-helper.sh <topic>
```

### 2. Information Search / Questions
**User asks a question or searches for information semantically**

Examples:
- `/docs what are the best practices for Claude Code SDK in Python?`
- `/docs how do I customize Claude Code's behavior?`
- `/docs explain the differences between hooks and MCP`
- `/docs find all mentions of authentication`
- `/docs show me everything about memory features`

**Action**: Extract key concepts and use content search (if Python available)
```bash
~/.claude-code-docs/claude-docs-helper.sh --search-content "<extracted keywords>"
```

If content search is not available (no Python), explain to user:
"Content search requires Python 3.9+. You can:"
1. List available topics with: `~/.claude-code-docs/claude-docs-helper.sh`
2. Read specific docs like: `/docs hooks`, `/docs mcp`, etc.

### 3. Path Discovery
**User wants to discover available documentation paths**

Examples:
- `/docs show me all API documentation`
- `/docs list everything about agent SDK`
- `/docs what documentation is available for MCP?`

**Action**: Use path search (if Python available)
```bash
~/.claude-code-docs/claude-docs-helper.sh --search "<keywords>"
```

### 4. Freshness Check
**User wants to know if documentation is up to date**

Examples:
- `/docs -t`
- `/docs check for updates`
- `/docs are the docs current?`

**Action**: Execute freshness check
```bash
~/.claude-code-docs/claude-docs-helper.sh -t
```

You can also combine with topic: `/docs -t hooks` checks freshness then reads hooks doc

### 5. Recent Changes
**User wants to see what's new in documentation**

Examples:
- `/docs what's new`
- `/docs recent changes`
- `/docs show latest updates`

**Action**: Execute what's new command
```bash
~/.claude-code-docs/claude-docs-helper.sh "what's new"
```

### 6. Help / List Topics
**User wants to see available commands or topics**

Examples:
- `/docs` (no arguments)
- `/docs help`
- `/docs list all topics`

**Action**: Show help or list topics
```bash
~/.claude-code-docs/claude-docs-helper.sh --help
```

## Intelligent Routing Examples

**Example 1: Direct Lookup**
```
User: /docs hooks
Your Analysis: User wants hooks documentation (specific topic)
Execute: ~/.claude-code-docs/claude-docs-helper.sh hooks
```

**Example 2: Semantic Question**
```
User: /docs what are the best practices and recommended workflows using Claude Agent SDK in Python according to the official documentation?
Your Analysis: User wants information about best practices, workflows, Agent SDK, and Python
Extract Keywords: "best practices workflows Agent SDK Python"
Execute: ~/.claude-code-docs/claude-docs-helper.sh --search-content "best practices workflows Agent SDK Python"
Present Results: Naturally summarize the search results with context and provide relevant doc links
```

**Example 3: Discovery Query**
```
User: /docs show me all documentation about authentication
Your Analysis: User wants to discover authentication-related docs
Execute: ~/.claude-code-docs/claude-docs-helper.sh --search "authentication"
Present Results: List the matching paths found
```

**Example 4: Combined Workflow**
```
User: /docs what's new with extended thinking and how does it work?
Your Analysis: User wants both recent changes AND information about extended thinking
Step 1: Execute: ~/.claude-code-docs/claude-docs-helper.sh --search-content "extended thinking"
Step 2: Read the found documentation
Step 3: Check what's new: ~/.claude-code-docs/claude-docs-helper.sh "what's new"
Present Results: Combine information naturally - explain how extended thinking works based on docs, then mention any recent updates
```

## Response Guidelines

1. **Natural Presentation**: Don't just dump raw tool output - present information naturally with context
2. **Always Provide Links**: Include official documentation URLs when showing results
3. **Graceful Degradation**: If Python features aren't available, explain alternatives gracefully
4. **Auto-Update Check**: For major information requests, the helper automatically checks for updates (takes ~0.4s)
5. **Combine Sources**: When helpful, combine multiple searches or docs to give complete answers
6. **Show Confidence**: If you're unsure about routing, explain your reasoning and ask for clarification

## Expected Output Format

When reading documentation, you'll see:
```
📚 COMMUNITY MIRROR: https://github.com/costiash/claude-code-docs
📖 OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code

[Documentation content here...]

📖 Official page: https://docs.anthropic.com/en/docs/claude-code/hooks
```

When showing what's new:
```
📚 Recent documentation updates:

• 5 hours ago:
  📎 https://github.com/costiash/claude-code-docs/commit/abc123
  📄 hooks: https://docs.anthropic.com/en/docs/claude-code/hooks
     ✨ Added: New examples for pre-commit hooks
```

## User's Request

The user requested: "$ARGUMENTS"

**Your Task**: Analyze this semantically, route to the appropriate helper function(s), and present the information naturally.

Execute: ~/.claude-code-docs/claude-docs-helper.sh "$ARGUMENTS"
EOF

echo "✓ Created /docs command"

# Always update hook (remove old ones pointing to wrong location)
echo "Setting up automatic updates..."

# Simple hook that just calls the helper script
HOOK_COMMAND="~/.claude-code-docs/claude-docs-helper.sh hook-check"

if [ -f ~/.claude/settings.json ]; then
    # Update existing settings.json
    echo "  Updating Claude settings..."
    
    # First remove ALL hooks that contain "claude-code-docs" anywhere in the command
    # This catches old installations at any path
    jq '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.hooks[0].command | contains("claude-code-docs") | not)]' ~/.claude/settings.json > ~/.claude/settings.json.tmp
    
    # Then add our new hook
    jq --arg cmd "$HOOK_COMMAND" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[]] + [{"matcher": "Read", "hooks": [{"type": "command", "command": $cmd}]}]' ~/.claude/settings.json.tmp > ~/.claude/settings.json
    rm -f ~/.claude/settings.json.tmp
    echo "✓ Updated Claude settings"
else
    # Create new settings.json
    echo "  Creating Claude settings..."
    jq -n --arg cmd "$HOOK_COMMAND" '{
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Read",
                    "hooks": [
                        {
                            "type": "command",
                            "command": $cmd
                        }
                    ]
                }
            ]
        }
    }' > ~/.claude/settings.json
    echo "✓ Created Claude settings"
fi

# Note: Do NOT modify docs_manifest.json - it's tracked by git and would break updates

# Clean up old installations now that v0.3 is set up
cleanup_old_installations

# Success message
echo ""
echo "✅ Claude Code Docs v0.3.4 installed successfully!"
echo ""
echo "📚 Command: /docs (user)"
echo "📂 Location: ~/.claude-code-docs"
echo ""
echo "Usage examples:"
echo "  /docs hooks         # Read hooks documentation"
echo "  /docs -t           # Check when docs were last updated"
echo "  /docs what's new  # See recent documentation changes"
echo ""
echo "🔄 Auto-updates: Enabled - syncs automatically when GitHub has newer content"
echo ""

# Show what's installed (always the same: 268 files + Python scripts)
echo "📦 Installed Components:"
echo "  • 268 documentation files"
echo "  • 270 active documentation paths tracked"
echo "  • AI-powered /docs command"
echo ""

# Check if Python features are available and show appropriate message
if check_python_features; then
    echo "✨ Python Features: AVAILABLE (Python 3.9+ detected)"
    echo ""

    # Show category summary
    python3 -c "
import json
data = json.load(open('$INSTALL_DIR/paths_manifest.json'))
total = data['metadata']['total_paths']
cats = data['categories']

print(f'📚 Documentation Coverage: {total} paths across 7 categories')
print('')
print('Categories:')
for i, (cat, paths) in enumerate(cats.items(), 1):
    cat_name = cat.replace('_', ' ').title()
    print(f'  {i}. {cat_name}: {len(paths)} paths')

print('')
print('Python-Enhanced Commands:')
print('  ~/.claude-code-docs/claude-docs-helper.sh --search \"keyword\"')
print('  ~/.claude-code-docs/claude-docs-helper.sh --search-content \"term\"')
print('  ~/.claude-code-docs/claude-docs-helper.sh --validate')
print('  ~/.claude-code-docs/claude-docs-helper.sh --status')
" 2>/dev/null || {
        # Fallback if Python fails
        echo "📚 Python features available"
        echo "   Run: ~/.claude-code-docs/claude-docs-helper.sh --status"
    }
else
    echo "ℹ️  Python Features: NOT AVAILABLE"
    echo ""
    echo "Basic documentation reading works perfectly!"
    echo "Install Python 3.9+ to enable:"
    echo "  • Full-text content search (--search-content)"
    echo "  • Fuzzy path search (--search)"
    echo "  • Path validation (--validate)"
    echo "  • Enhanced AI routing capabilities"
    echo ""
    echo "Without Python, you can:"
    echo "  • Read all 268 documentation files via /docs command"
    echo "  • Use AI-powered semantic queries"
    echo "  • Check documentation freshness"
    echo "  • View recent changes"
fi

echo ""
echo "⚠️  Note: Restart Claude Code for auto-updates to take effect"