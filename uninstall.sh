#!/bin/bash
set -euo pipefail

# Claude Code Documentation Mirror - Smart Uninstaller
# Dynamically finds and removes all installations

echo "Claude Code Documentation Mirror - Uninstaller"
echo "=============================================="
echo ""

# Find all installations from configs
find_all_installations() {
    local paths=()
    
    # From command file
    if [[ -f ~/.claude/commands/docs.md ]]; then
        while IFS= read -r line; do
            if [[ "$line" =~ Execute:.*claude-code-docs ]]; then
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
    
    # From hooks
    if [[ -f ~/.claude/settings.json ]]; then
        local hooks=$(jq -r '.hooks.PreToolUse[]?.hooks[]?.command // empty' ~/.claude/settings.json 2>/dev/null)
        while IFS= read -r cmd; do
            if [[ "$cmd" =~ claude-code-docs ]]; then
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
    
    # Deduplicate - handle empty array case
    if [[ ${#paths[@]} -gt 0 ]]; then
        printf '%s\n' "${paths[@]}" | sort -u
    fi
}

# Main uninstall logic
installations=()
while IFS= read -r line; do
    installations+=("$line")
done < <(find_all_installations)

if [[ ${#installations[@]} -gt 0 ]]; then
    echo "Found installations at:"
    for path in "${installations[@]}"; do
        echo "  📁 $path"
    done
    echo ""
fi

echo "This will remove:"
echo "  • The /docs command from ~/.claude/commands/docs.md"
echo "  • All claude-code-docs hooks from ~/.claude/settings.json"
if [[ ${#installations[@]} -gt 0 ]]; then
    echo "  • Installation directories (if safe to remove)"
fi
echo ""

read -p "Continue? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Remove command file
if [[ -f ~/.claude/commands/docs.md ]]; then
    rm -f ~/.claude/commands/docs.md
    echo "✓ Removed /docs command"
fi

# Remove hooks
if [[ -f ~/.claude/settings.json ]]; then
    cp ~/.claude/settings.json ~/.claude/settings.json.backup
    
    # Remove ALL hooks containing claude-code-docs
    jq '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.hooks[0].command | contains("claude-code-docs") | not)]' ~/.claude/settings.json > ~/.claude/settings.json.tmp
    
    # Clean up empty structures
    jq 'if .hooks.PreToolUse == [] then .hooks |= if . == {PreToolUse: []} then {} else del(.PreToolUse) end else . end | if .hooks == {} then del(.hooks) else . end' ~/.claude/settings.json.tmp > ~/.claude/settings.json.tmp2
    
    mv ~/.claude/settings.json.tmp2 ~/.claude/settings.json
    rm -f ~/.claude/settings.json.tmp
    echo "✓ Removed hooks (backup: ~/.claude/settings.json.backup)"
fi

# Remove /query feature files
echo ""
echo "Removing /query feature..."

[[ -f ~/.claude/commands/query.md ]] && rm -f ~/.claude/commands/query.md && echo "✓ Removed /query command"
[[ -f ~/.claude/agents/query-researcher.md ]] && rm -f ~/.claude/agents/query-researcher.md && echo "✓ Removed query-researcher agent"
[[ -d ~/.claude/skills/query-orchestrator ]] && rm -rf ~/.claude/skills/query-orchestrator && echo "✓ Removed query-orchestrator skill"

if [[ -d "$HOME/.claude-code-docs/query" ]] && [[ -n "$(ls -A "$HOME/.claude-code-docs/query" 2>/dev/null)" ]]; then
    echo ""
    echo "⚠️  Found query outputs at $HOME/.claude-code-docs/query/"
    read -p "Delete query history? (y/N): " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] && rm -rf "$HOME/.claude-code-docs/query" && echo "✓ Removed query history"
fi

# Remove directories
if [[ ${#installations[@]} -gt 0 ]]; then
    echo ""
    for path in "${installations[@]}"; do
        if [[ ! -d "$path" ]]; then
            continue
        fi
        
        if [[ -d "$path/.git" ]]; then
            # Save current directory
            local current_dir=$(pwd)
            cd "$path"
            
            if [[ -z "$(git status --porcelain 2>/dev/null)" ]]; then
                cd "$current_dir"
                rm -rf "$path"
                echo "✓ Removed $path (clean git repo)"
            else
                cd "$current_dir"
                echo "⚠️  Preserved $path (has uncommitted changes)"
            fi
        else
            echo "⚠️  Preserved $path (not a git repo)"
        fi
    done
fi

echo ""
echo "✅ Uninstall complete!"
echo ""
echo "To reinstall:"
echo "curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash"