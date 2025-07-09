#!/bin/bash
set -e

# Get the docs path
if [ -f "docs/docs_manifest.json" ]; then
    # We're already in the claude-code-docs directory
    DOCS_PATH=$(pwd)
elif [ -d "claude-code-docs" ]; then
    # The directory already exists
    cd claude-code-docs
    DOCS_PATH=$(pwd)
else
    # Clone it
    git clone https://github.com/ericbuess/claude-code-docs.git
    cd claude-code-docs
    DOCS_PATH=$(pwd)
fi

# Create command
mkdir -p ~/.claude/commands
cat > ~/.claude/commands/docs.md << EOF
$DOCS_PATH/docs/ contains a local updated copy of all Claude Code documentation.

First, check the documentation status:
1. Read $DOCS_PATH/docs/docs_manifest.json to get the "last_updated" field
2. Check if $DOCS_PATH/.last_pull exists
3. If it doesn't exist OR if it's been more than 3 hours since last check, say:
   "Since this is the first time checking docs from this directory in a while, let me verify the documentation status..."
4. Convert the UTC timestamp to local time. First extract just the datetime part (before the decimal), then:
   TZ=\$LOCALTZ date -j -u -f "%Y-%m-%dT%H:%M:%S" "<timestamp>" "+%Y-%m-%d %I:%M %p %Z"
   where \$LOCALTZ is the user's timezone (e.g., America/Chicago for CDT)
5. If .last_pull exists, convert using: date -r <timestamp> "+%Y-%m-%d %I:%M %p %Z"
6. If .last_pull doesn't exist, note this is the first sync

GitHub Actions updates the docs every 3 hours. Your local copy automatically syncs at most once every 3 hours when you use this command.

IMPORTANT: If less than 3 hours have passed since the last check (based on .last_pull timestamp), skip the timestamp conversions entirely and just report "Documentation is up to date (last checked X time ago)" before answering the query.

Examples:
📅 Documentation last updated on GitHub: 2025-01-09 6:03 AM PST (updates every 3 hours)
📅 Your local copy last synced: 2025-01-09 12:42 AM PST (syncs automatically when needed)
   -or if first sync-
📅 Your local copy: First sync today

Then answer the user's question by reading from the docs/ subdirectory (e.g. $DOCS_PATH/docs/hooks.md).

Available docs: overview, quickstart, setup, memory, common-workflows, ide-integrations, mcp, github-actions, sdk, troubleshooting, security, settings, monitoring-usage, costs, hooks

User query: \$ARGUMENTS
EOF

# Setup hook for auto-updates (pulls at most once every 3 hours)
# The hook checks a timestamp file and only pulls if 3 hours have passed
HOOK_COMMAND="if [[ \$(jq -r .tool_input.file_path 2>/dev/null) == *$DOCS_PATH/* ]]; then LAST_PULL=\"$DOCS_PATH/.last_pull\"; NOW=\$(date +%s); if [[ -f \"\$LAST_PULL\" ]]; then LAST=\$(cat \"\$LAST_PULL\"); DIFF=\$((NOW - LAST)); if [[ \$DIFF -gt 10800 ]]; then cd $DOCS_PATH && git pull --quiet && echo \$NOW > \"\$LAST_PULL\"; fi; else cd $DOCS_PATH && git pull --quiet && echo \$NOW > \"\$LAST_PULL\"; fi; fi"

if [ -f ~/.claude/settings.json ]; then
    # Update existing settings.json
    jq --arg path "$DOCS_PATH" --arg cmd "$HOOK_COMMAND" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.matcher != "Read")] + [{"matcher": "Read", "hooks": [{"type": "command", "command": $cmd}]}]' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
else
    # Create new settings.json
    cat > ~/.claude/settings.json << EOF
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "$HOOK_COMMAND"
          }
        ]
      }
    ]
  }
}
EOF
fi

echo "✓ Claude Code docs installed!"
echo "✓ Command: /user:docs"
echo "✓ Auto-updates: enabled"