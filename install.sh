#!/bin/bash
set -euo pipefail

# Claude Code Docs Installer - macOS only
# This script sets up local Claude Code documentation with automatic updates

echo "Claude Code Docs Installer (macOS only)"
echo "======================================"

# Check for macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This installer is only tested on macOS"
    echo "For other platforms, please install manually or submit a tested version"
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

# Get the docs path
if [ -f "docs/docs_manifest.json" ]; then
    # We're already in the claude-code-docs directory
    DOCS_PATH=$(pwd)
    echo "✓ Found existing installation at: $DOCS_PATH"
elif [ -d "claude-code-docs" ]; then
    # The directory already exists
    cd claude-code-docs || exit 1
    DOCS_PATH=$(pwd)
    echo "✓ Found existing installation at: $DOCS_PATH"
else
    # Clone it
    echo "Cloning documentation repository..."
    if ! git clone https://github.com/ericbuess/claude-code-docs.git; then
        echo "❌ Error: Failed to clone repository"
        exit 1
    fi
    cd claude-code-docs || exit 1
    DOCS_PATH=$(pwd)
    echo "✓ Documentation cloned to: $DOCS_PATH"
fi

# Escape the docs path for safe use in commands
DOCS_PATH_ESCAPED=$(printf '%q' "$DOCS_PATH")

# Create command directory
echo "Setting up /user:docs command..."
if ! mkdir -p ~/.claude/commands; then
    echo "❌ Error: Failed to create ~/.claude/commands directory"
    exit 1
fi

# Create the docs command file with quoted heredoc to prevent variable expansion
cat > ~/.claude/commands/docs.md << 'DOCS_COMMAND_EOF'
PLACEHOLDER_DOCS_PATH/docs/ contains a local updated copy of all Claude Code documentation.

Usage:
- /user:docs <topic> - Read documentation instantly (no checks)
- /user:docs -t - Check documentation freshness and sync status
- /user:docs -t <topic> - Check freshness, then read documentation

Default behavior (no -t flag):
1. Skip ALL checks for maximum speed
2. Go straight to reading the requested documentation
3. Add note: "📚 Reading from local docs (run /user:docs -t to check freshness)"

With -t flag:
1. Read PLACEHOLDER_DOCS_PATH/docs/docs_manifest.json (if it fails, suggest re-running install.sh)
2. Calculate and show when GitHub last updated and when local docs last synced
3. Then read the requested topic (if provided)

Note: The hook automatically keeps docs up-to-date by checking if GitHub has newer content before each read. You'll see "🔄 Updating docs to latest version..." when it syncs.

Error handling:
- If any files are missing or commands fail, show: "❌ Error accessing docs. Try re-running: curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/install.sh | bash"

GitHub Actions updates the docs every 3 hours. Your local copy automatically syncs at most once every 3 hours when you use this command.

IMPORTANT: Show relative times only (no timezone conversions needed):
- GitHub last updated: Extract timestamp from manifest (it's in UTC!), convert with: date -j -u -f "%Y-%m-%dT%H:%M:%S" "TIMESTAMP" "+%s", then calculate (current_time - github_time) / 3600 for hours or / 60 for minutes
- Local docs last synced: Read .last_pull timestamp, then calculate (current_time - last_pull) / 60 for minutes
- If GitHub hasn't updated in >3 hours, add note "(normally updates every 3 hours)"
- Be clear about wording: "local docs last synced" not "last checked"
- For calculations: Use proper parentheses like $(((NOW - GITHUB) / 3600)) for hours

First, check if user passed -t flag:
- If "$ARGUMENTS" starts with "-t", extract it and treat the rest as the topic
- Parse carefully: "-t hooks" → flag=true, topic=hooks; "hooks" → flag=false, topic=hooks

Examples:

Default usage (no -t):
> /user:docs hooks
📚 Reading from local docs (run /user:docs -t to check freshness)
[Immediately shows hooks documentation]

With -t flag:
> /user:docs -t
📅 Documentation last updated on GitHub: 2 hours ago
📅 Your local docs last synced: 25 minutes ago

> /user:docs -t hooks  
📅 Documentation last updated on GitHub: 5 hours ago (normally updates every 3 hours)
📅 Your local docs last synced: 3 hours 15 minutes ago
🔄 Syncing latest documentation...
[Then shows hooks documentation]

Then answer the user's question by reading from the docs/ subdirectory (e.g. PLACEHOLDER_DOCS_PATH/docs/hooks.md).

Available docs: overview, quickstart, setup, memory, common-workflows, ide-integrations, mcp, github-actions, sdk, troubleshooting, security, settings, monitoring-usage, costs, hooks

IMPORTANT: This freshness check only happens when using /user:docs command. If continuing a conversation from a previous session, use /user:docs again to ensure docs are current.

User query: $ARGUMENTS
DOCS_COMMAND_EOF

# Replace the placeholder with the actual escaped path
sed -i '' "s|PLACEHOLDER_DOCS_PATH|$DOCS_PATH|g" ~/.claude/commands/docs.md

echo "✓ Created /user:docs command"

# Setup hook for auto-updates (checks if GitHub has newer content)
echo "Setting up automatic updates..."

# Create the hook command with proper escaping
# Using printf to safely construct the command with escaped variables
# Note: Using pushd/popd to avoid cd restrictions in Claude Code
HOOK_COMMAND=$(printf 'if [[ $(jq -r .tool_input.file_path 2>/dev/null) == *%s/* ]]; then LAST_PULL="%s/.last_pull" && NOW=$(date +%%s) && GITHUB_TS=$(jq -r .last_updated "%s/docs/docs_manifest.json" 2>/dev/null | cut -d. -f1) && GITHUB_UNIX=$(date -j -u -f "%%Y-%%m-%%dT%%H:%%M:%%S" "$GITHUB_TS" "+%%s" 2>/dev/null || echo 0) && if [[ -f "$LAST_PULL" ]]; then LAST=$(cat "$LAST_PULL"); if [[ $GITHUB_UNIX -gt $LAST ]]; then echo "🔄 Updating docs to latest version..." >&2 && (cd %s && git pull --quiet) && echo $NOW > "$LAST_PULL"; fi; else echo "🔄 Syncing docs for the first time..." >&2 && (cd %s && git pull --quiet) && echo $NOW > "$LAST_PULL"; fi; fi' "$DOCS_PATH_ESCAPED" "$DOCS_PATH_ESCAPED" "$DOCS_PATH_ESCAPED" "$DOCS_PATH_ESCAPED" "$DOCS_PATH_ESCAPED")

if [ -f ~/.claude/settings.json ]; then
    # Update existing settings.json
    echo "Updating existing Claude settings..."
    if jq --arg cmd "$HOOK_COMMAND" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.matcher != "Read")] + [{"matcher": "Read", "hooks": [{"type": "command", "command": $cmd}]}]' ~/.claude/settings.json > ~/.claude/settings.json.tmp; then
        mv ~/.claude/settings.json.tmp ~/.claude/settings.json
        echo "✓ Updated Claude settings"
    else
        echo "❌ Error: Failed to update settings.json"
        echo "Please check ~/.claude/settings.json manually"
        exit 1
    fi
else
    # Create new settings.json
    echo "Creating Claude settings..."
    if jq -n --arg cmd "$HOOK_COMMAND" '{
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
    }' > ~/.claude/settings.json; then
        echo "✓ Created Claude settings"
    else
        echo "❌ Error: Failed to create settings.json"
        exit 1
    fi
fi

echo ""
echo "✅ Claude Code docs installed successfully!"
echo ""
echo "📚 Command: /user:docs (not /docs)"
echo "📂 Location: $DOCS_PATH"
echo ""
echo "Usage examples:"
echo "  /user:docs hooks         # Read hooks documentation"
echo "  /user:docs -t           # Check when docs were last updated"
echo "  /user:docs -t memory    # Check updates, then read memory docs"
echo ""
echo "🔄 Auto-updates: Enabled - syncs automatically when GitHub has newer content"
echo ""
echo "Available topics: overview, quickstart, memory, hooks, mcp, settings, etc."
echo ""
echo "Note: This installer is macOS-only. For other platforms, please contribute a tested version."