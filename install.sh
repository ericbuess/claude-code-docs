#!/bin/bash
set -euo pipefail

# Claude Code Docs Installer v0.4.2 - Enhanced edition with accurate path tracking
# This script installs claude-code-docs to ~/.claude-code-docs
# Installation Strategy: Always perform a fresh installation at the fixed location
#   1. Remove any existing installation at ~/.claude-code-docs (with user confirmation)
#   2. Clone fresh from GitHub
#   3. Set up commands and hooks
#   4. Clean up any old installations in other locations

echo "Claude Code Docs Installer v0.4.2"
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
echo "Setting up Claude Code Docs v0.4.2..."

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

# Create AI-powered docs command with intent-driven approach
cat > ~/.claude/commands/docs.md << 'EOF'
# Claude Code Documentation Assistant

You are a documentation assistant for Claude Code. Your mission: **answer the user's question directly with minimal interaction**.

## Core Philosophy

📖 **Read this first**: `~/.claude-code-docs/CLAUDE.md` contains comprehensive guidance on:
- Intent-driven documentation search
- When to synthesize vs when to ask
- Category labels and context detection
- Content search strategies
- Example workflows

**Key principles from CLAUDE.md**:
1. **Synthesize by default** - Read multiple docs silently, present unified answer
2. **Only ask when contexts are incompatible** - Different products with different workflows
3. **Content search over path matching** - Find information even without exact paths
4. **Hide complexity** - Users don't need to know document structure

## Your Workflow

### Step 1: Analyze User Intent

Extract from `$ARGUMENTS`:
- **What** they want to know (keywords, concepts)
- **Which product** context (if specified): "agent sdk", "cli", "api"
- **Type** of query: how-to, reference, integration, etc.

### Step 2: Execute Search

Use the helper script with appropriate command:

```bash
# Content search (requires Python 3.9+)
~/.claude-code-docs/claude-docs-helper.sh --search-content "<keywords>"

# Path search
~/.claude-code-docs/claude-docs-helper.sh --search "<keywords>"

# Direct topic lookup
~/.claude-code-docs/claude-docs-helper.sh <topic>

# Special commands
~/.claude-code-docs/claude-docs-helper.sh -t  # freshness check
~/.claude-code-docs/claude-docs-helper.sh "what's new"  # recent changes
```

### Step 3: Analyze Results & Decide

Check which product contexts the results span:

**Same context** (e.g., all Agent SDK) → **SYNTHESIZE**:
- Read ALL matching docs silently
- Extract relevant sections
- Present unified answer
- Cite sources at end

**Different contexts** (e.g., CLI vs API vs SDK) → **ASK**:
- Use `AskUserQuestion` tool
- Present product options with user-friendly labels (see CLAUDE.md)
- After selection → synthesize within that context

### Step 4: Present Naturally

- Don't dump raw tool output
- Synthesize information from multiple sources
- Include code examples where relevant
- Always cite sources with links
- Suggest related topics

## Quick Reference

### User-Friendly Product Labels

Use these when asking for clarification:

| When docs are in | Say to user |
|------------------|-------------|
| `/docs/en/*` | Claude Code CLI |
| `/en/api/*` | Claude API |
| `/en/docs/agent-sdk/*` | Claude Agent SDK |
| `/en/docs/build-with-claude/*` | Claude Documentation |
| `/en/resources/prompt-library/*` | Prompt Library |

### Example Interactions

**Example 1: Clear context → Synthesize**
```
User: /docs how do I use memory in agent sdk?

You:
1. Extract: intent=how-to, context=agent_sdk, keywords=["memory"]
2. Search: content search in agent_sdk for "memory"
3. Find: python.md, overview.md, sessions.md (all Agent SDK)
4. Decision: Same context → Read all three, synthesize
5. Present: "In the Claude Agent SDK, memory works as follows..."
   [Unified explanation from all three docs]
   Sources: [links]
```

**Example 2: Ambiguous → Ask, then synthesize**
```
User: /docs skills

You:
1. Extract: intent=general, context=unclear, keywords=["skills"]
2. Search: content search for "skills"
3. Find: Agent SDK (5 docs), CLI (2 docs), API (7 docs)
4. Decision: Different products → Ask user

Use AskUserQuestion:
"Skills exist in different Claude products:

○ 1. Claude Agent SDK - Build custom agent capabilities
○ 2. Claude Code CLI - Install/run pre-built skills
○ 3. Claude API - Programmatic skill management

Which are you working with?"

5. User selects: 1 (Agent SDK)
6. Filter to Agent SDK, read all 5 docs, synthesize
7. Present unified Agent SDK skills explanation
```

## Error Handling

- **No Python 3.9+**: Explain gracefully, suggest alternatives (direct lookups, list topics)
- **No results**: Suggest fuzzy matches, offer to search related terms
- **Ambiguous with no clear product boundary**: Ask for clarification

## User's Request

The user requested: "$ARGUMENTS"

**Your task**: Follow the workflow above. Reference CLAUDE.md for detailed guidance on ambiguity resolution and synthesis strategies.

## Execution Steps

1. **Analyze the user's request** to determine routing:
   - **Simple keyword** (e.g., "hooks", "mcp", "memory"): Route to content search
   - **Question** (e.g., "how do I...", "what are..."): Route to content search
   - **Exact filename** (e.g., "docs__en__hooks"): Route to direct lookup
   - **Special flags** (e.g., "-t", "what's new"): Pass through directly

2. **Execute appropriate command:**
   - **For keywords/questions**: `~/.claude-code-docs/claude-docs-helper.sh --search-content "$ARGUMENTS"`
   - **For exact filenames**: `~/.claude-code-docs/claude-docs-helper.sh "$ARGUMENTS"`
   - **For special flags**: `~/.claude-code-docs/claude-docs-helper.sh "$ARGUMENTS"`

3. **Analyze search results** (if using --search-content):
   - Check which product contexts the results span
   - **Same context**: Read ALL matching docs using exact filenames, synthesize unified answer
   - **Different contexts**: Use AskUserQuestion with **ANTHROPIC PRODUCT NAMES** users know:
     - "Claude Code" (NOT "CLI" or "claude_code")
     - "Claude API" (NOT "api_reference")
     - "Agent SDK" (NOT "agent-sdk paths")
     - "Prompt Library", etc.

4. **Always present naturally** - don't dump raw output, add context and links
EOF

echo "✓ Created /docs command"

# Clean up any old hooks from previous installations
if [ -f ~/.claude/settings.json ]; then
    echo "Cleaning up old hooks..."
    # Remove ALL hooks that contain "claude-code-docs" anywhere in the command
    # This catches old installations at any path
    jq '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.hooks[0].command | contains("claude-code-docs") | not)]' ~/.claude/settings.json > ~/.claude/settings.json.tmp

    # Clean up empty structures
    jq 'if .hooks.PreToolUse == [] then .hooks |= del(.PreToolUse) else . end | if .hooks == {} then del(.hooks) else . end' ~/.claude/settings.json.tmp > ~/.claude/settings.json
    rm -f ~/.claude/settings.json.tmp
    echo "✓ Cleaned up old hooks"
fi

# Note: Do NOT modify docs_manifest.json - it's tracked by git and would break updates

# Clean up old installations now that v0.3 is set up
cleanup_old_installations

# Verify installation
echo ""
echo "Verifying installation..."
VERIFY_FAILED=false

# Check critical files exist
if [[ ! -f "$INSTALL_DIR/claude-docs-helper.sh" ]]; then
    echo "  ❌ Helper script missing"
    VERIFY_FAILED=true
else
    echo "  ✓ Helper script installed"
fi

if [[ ! -f "$INSTALL_DIR/scripts/claude-docs-helper.sh.template" ]]; then
    echo "  ❌ Template script missing"
    VERIFY_FAILED=true
else
    echo "  ✓ Template script installed"
fi

if [[ ! -d "$INSTALL_DIR/docs" ]]; then
    echo "  ❌ Documentation directory missing"
    VERIFY_FAILED=true
else
    DOC_COUNT=$(find "$INSTALL_DIR/docs" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
    if [[ "$DOC_COUNT" -lt 100 ]]; then
        echo "  ⚠️  Only $DOC_COUNT documentation files found (expected ~267)"
    else
        echo "  ✓ Documentation files installed ($DOC_COUNT files)"
    fi
fi

if [[ ! -f ~/.claude/commands/docs.md ]]; then
    echo "  ❌ /docs command not created"
    VERIFY_FAILED=true
else
    echo "  ✓ /docs command created"
fi

# Test that helper script executes
if ! "$INSTALL_DIR/claude-docs-helper.sh" --help >/dev/null 2>&1; then
    echo "  ❌ Helper script fails to execute"
    VERIFY_FAILED=true
else
    echo "  ✓ Helper script executes correctly"
fi

if [[ "$VERIFY_FAILED" == "true" ]]; then
    echo ""
    echo "⚠️  Installation completed with warnings. Some components may not work correctly."
    echo "    Try reinstalling or check the issues above."
else
    echo "  ✓ All verification checks passed"
fi

# Success message
echo ""
echo "✅ Claude Code Docs v0.4.2 installed successfully!"
echo ""
echo "📚 Command: /docs (user)"
echo "📂 Location: ~/.claude-code-docs"
echo ""
echo "Usage examples:"
echo "  /docs hooks         # Read hooks documentation"
echo "  /docs -t           # Check when docs were last updated"
echo "  /docs what's new  # See recent documentation changes"
echo ""
echo "🔄 Updates: Run '/docs -t' to check for and pull latest documentation"
echo ""

# Show what's installed (273 paths tracked in manifest)
echo "📦 Installed Components:"
echo "  • 273 documentation paths tracked"
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
    echo "  • Read all 273 documentation paths via /docs command"
    echo "  • Use AI-powered semantic queries"
    echo "  • Check documentation freshness"
    echo "  • View recent changes"
fi

echo ""
echo "💡 Tip: Run '/docs -t' periodically to get latest documentation updates"