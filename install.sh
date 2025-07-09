#!/bin/bash
set -e

# Clone if needed
if [ ! -d "claude-code-docs" ]; then
    git clone https://github.com/ericbuess/claude-code-docs.git
fi

cd claude-code-docs
DOCS_PATH=$(pwd)

# Create command
mkdir -p ~/.claude/commands
echo "$DOCS_PATH/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: \$ARGUMENTS" > ~/.claude/commands/docs.md

# Setup hook for auto-updates
if [ -f ~/.claude/settings.json ]; then
    # Update existing settings.json
    jq --arg path "$DOCS_PATH" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.matcher != "Read")] + [{"matcher": "Read", "hooks": [{"type": "command", "command": ("if [[ $(jq -r .tool_input.file_path 2>/dev/null) == *" + $path + "/* ]]; then cd " + $path + " && git pull --quiet; fi")}]}]' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json
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
            "command": "if [[ \$(jq -r .tool_input.file_path 2>/dev/null) == *$DOCS_PATH/* ]]; then cd $DOCS_PATH && git pull --quiet; fi"
          }
        ]
      }
    ]
  }
}
EOF
fi

cd ..
echo "✓ Claude Code docs installed!"
echo "✓ Command: /user:docs"
echo "✓ Auto-updates: enabled"