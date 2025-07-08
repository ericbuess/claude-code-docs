#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Check if settings.json exists
if [ -f ~/.claude/settings.json ]; then
    # Update existing settings.json
    jq --arg path "$SCRIPT_DIR" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.matcher != "Read")] + [{"matcher": "Read", "hooks": [{"type": "command", "command": ("if [[ $(echo $0 | jq -r .tool_input.file_path 2>/dev/null) == *" + $path + "/* ]]; then cd " + $path + " && git pull --quiet; fi")}]}]' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
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
            "command": "if [[ \$(echo \$0 | jq -r .tool_input.file_path 2>/dev/null) == *$SCRIPT_DIR/* ]]; then cd $SCRIPT_DIR && git pull --quiet; fi"
          }
        ]
      }
    ]
  }
}
EOF
fi

echo "✅ Auto-update hook installed!"
echo "   Claude will now automatically pull updates before reading docs."