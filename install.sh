#!/bin/bash
set -euo pipefail

# Claude Code Docs Installer v0.3.2 - Fixed auto-update issues
# This script installs/migrates claude-code-docs to ~/.claude-code-docs

echo "Claude Code Docs Installer v0.3.2"
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
    printf '%s\n' "${paths[@]}" | grep -v "^$INSTALL_DIR$" | sort -u
}

# Function to migrate from old location
migrate_installation() {
    local old_dir="$1"
    
    echo "📦 Found existing installation at: $old_dir"
    echo "   Migrating to: $INSTALL_DIR"
    echo ""
    
    # Check if old dir has uncommitted changes
    local should_preserve=false
    if [[ -d "$old_dir/.git" ]]; then
        cd "$old_dir"
        if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
            should_preserve=true
            echo "⚠️  Uncommitted changes detected in old installation"
        fi
        cd - >/dev/null
    fi
    
    # Fresh install at new location
    echo "Installing fresh at ~/.claude-code-docs..."
    git clone -b "$INSTALL_BRANCH" https://github.com/ericbuess/claude-code-docs.git "$INSTALL_DIR"
    cd "$INSTALL_DIR"
    
    # Remove old directory if safe
    if [[ "$should_preserve" == "false" ]]; then
        echo "Removing old installation..."
        rm -rf "$old_dir"
        echo "✓ Old installation removed"
    else
        echo ""
        echo "ℹ️  Old installation preserved at: $old_dir"
        echo "   (has uncommitted changes)"
    fi
    
    echo ""
    echo "✅ Migration complete!"
}

# Function to safely update git repository
safe_git_update() {
    local repo_dir="$1"
    cd "$repo_dir"
    
    # Check if this is a v0.3.1 installation with dirty manifest (need to upgrade to v0.3.2)
    local needs_v032_upgrade=false
    if [[ -n "$(git status --porcelain docs/docs_manifest.json 2>/dev/null)" ]]; then
        # Check if manifest has installer_version (v0.3.1 bug)
        if grep -q '"installer_version"' docs/docs_manifest.json 2>/dev/null; then
            needs_v032_upgrade=true
            echo "  Detected v0.3.1 with manifest bug, upgrading to v0.3.2..."
        fi
    fi
    
    # Determine which branch to use
    local target_branch
    if [[ "$needs_v032_upgrade" == "true" ]]; then
        # Force upgrade to v0.3.2-release for bugfix
        target_branch="$INSTALL_BRANCH"
        # Fetch the v0.3.2-release branch
        git fetch origin "$target_branch" 2>/dev/null || true
    else
        # Stay on current branch (for normal updates)
        target_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    fi
    
    # Set git config for pull strategy if not set
    if ! git config pull.rebase >/dev/null 2>&1; then
        git config pull.rebase false
    fi
    
    echo "Updating to latest version..."
    
    # For v0.3.1 upgrade, we need to handle dirty files
    if [[ "$needs_v032_upgrade" == "true" ]]; then
        # Restore manifest to clean state
        git checkout -- docs/docs_manifest.json 2>/dev/null || true
        # Switch to v0.3.2-release branch
        git checkout "$target_branch" 2>/dev/null || git checkout -b "$target_branch" origin/"$target_branch" 2>/dev/null
        # Pull latest
        git pull origin "$target_branch" 2>/dev/null || true
        echo "  ✓ Upgraded to v0.3.2 (fixed manifest bug)"
        return 0
    fi
    
    # Try regular pull first (use target branch)
    if git pull --quiet origin "$target_branch" 2>/dev/null; then
        return 0
    fi
    
    # If pull failed, try more aggressive approach
    echo "  Standard update failed, trying harder..."
    
    # Fetch latest
    if ! git fetch origin "$target_branch" 2>/dev/null; then
        echo "  ⚠️  Could not fetch from GitHub (offline?)"
        return 1
    fi
    
    # Check if we have local changes
    if [[ -n "$(git status --porcelain 2>/dev/null)" ]]; then
        echo "  ⚠️  Local changes detected, preserving them..."
        # Stash changes
        git stash push -m "Installer auto-stash $(date)" >/dev/null 2>&1
        # Reset to origin
        git reset --hard origin/"$target_branch" >/dev/null 2>&1
        echo "  ✓ Updated (local changes stashed)"
    else
        # No local changes, just reset
        git reset --hard origin/"$target_branch" >/dev/null 2>&1
        echo "  ✓ Updated successfully"
    fi
    
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
        
        # Check if it has uncommitted changes
        if [[ -d "$old_dir/.git" ]]; then
            cd "$old_dir"
            if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
                cd - >/dev/null
                rm -rf "$old_dir"
                echo "    ✓ Removed (clean)"
            else
                cd - >/dev/null
                echo "    ⚠️  Preserved (has uncommitted changes)"
            fi
        else
            echo "    ⚠️  Preserved (not a git repo)"
        fi
    done
}

# Main installation logic
echo ""

# Always find old installations first (before any config changes)
echo "Checking for existing installations..."
mapfile -t existing_installs < <(find_existing_installations)
OLD_INSTALLATIONS=("${existing_installs[@]}")  # Save for later cleanup

if [[ ${#existing_installs[@]} -gt 0 ]]; then
    echo "Found ${#existing_installs[@]} existing installation(s):"
    for install in "${existing_installs[@]}"; do
        echo "  - $install"
    done
    echo ""
fi

# Check if already installed at new location
if [[ -d "$INSTALL_DIR" && -f "$INSTALL_DIR/docs/docs_manifest.json" ]]; then
    echo "✓ Found installation at ~/.claude-code-docs"
    echo "  Updating to latest version..."
    
    # Update it safely
    safe_git_update "$INSTALL_DIR"
    cd "$INSTALL_DIR"
else
    # Need to install at new location
    if [[ ${#existing_installs[@]} -gt 0 ]]; then
        # Migrate from old location
        old_install="${existing_installs[0]}"
        migrate_installation "$old_install"
    else
        # Fresh installation
        echo "No existing installation found"
        echo "Installing fresh to ~/.claude-code-docs..."
        
        git clone -b "$INSTALL_BRANCH" https://github.com/ericbuess/claude-code-docs.git "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
fi

# Now we're in $INSTALL_DIR, set up the new script-based system
echo ""
echo "Setting up Claude Code Docs v0.3.2..."

# Copy helper script from template
echo "Installing helper script..."
if [[ -f "$INSTALL_DIR/scripts/claude-docs-helper.sh.template" ]]; then
    cp "$INSTALL_DIR/scripts/claude-docs-helper.sh.template" "$INSTALL_DIR/claude-docs-helper.sh"
    chmod +x "$INSTALL_DIR/claude-docs-helper.sh"
    echo "✓ Helper script installed"
else
    echo "  ⚠️  Template file missing, attempting recovery..."
    # Try to fetch just the template file
    if curl -fsSL "https://raw.githubusercontent.com/ericbuess/claude-code-docs/$INSTALL_BRANCH/scripts/claude-docs-helper.sh.template" -o "$INSTALL_DIR/claude-docs-helper.sh" 2>/dev/null; then
        chmod +x "$INSTALL_DIR/claude-docs-helper.sh"
        echo "  ✓ Helper script downloaded directly"
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

# Create simplified docs command
cat > ~/.claude/commands/docs.md << 'EOF'
Execute the Claude Code Docs helper script at ~/.claude-code-docs/claude-docs-helper.sh

Usage:
- /docs - List all available documentation topics
- /docs <topic> - Read specific documentation with link to official docs
- /docs -t - Check sync status without reading a doc
- /docs -t <topic> - Check freshness then read documentation
- /docs whats new - Show recent documentation changes (or "what's new")

Examples of expected output:

When reading a doc:
📚 COMMUNITY MIRROR: https://github.com/ericbuess/claude-code-docs
📖 OFFICIAL DOCS: https://docs.anthropic.com/en/docs/claude-code

[Doc content here...]

📖 Official page: https://docs.anthropic.com/en/docs/claude-code/hooks

When showing what's new:
📚 Recent documentation updates:

• 5 hours ago:
  📎 https://github.com/ericbuess/claude-code-docs/commit/eacd8e1
  📄 data-usage: https://docs.anthropic.com/en/docs/claude-code/data-usage
     ➕ Added: Privacy safeguards
  📄 security: https://docs.anthropic.com/en/docs/claude-code/security
     ✨ Data flow and dependencies section moved here

📎 Full changelog: https://github.com/ericbuess/claude-code-docs/commits/main/docs
📚 COMMUNITY MIRROR - NOT AFFILIATED WITH ANTHROPIC

Every request checks for the latest documentation from GitHub (takes ~0.4s).
The helper script handles all functionality including auto-updates.

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
echo "✅ Claude Code Docs v0.3.2 installed successfully!"
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
echo "Available topics:"
ls "$INSTALL_DIR/docs" | grep '\.md$' | sed 's/\.md$//' | sort | column -c 60
echo ""
echo "⚠️  Note: Restart Claude Code for auto-updates to take effect"