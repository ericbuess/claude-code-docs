#!/bin/bash
# Add Claude Code docs instructions to ~/.claude/CLAUDE.md

# Check if instructions already exist
if grep -q "Claude Code Docs" ~/.claude/CLAUDE.md 2>/dev/null; then
    echo "✅ Claude Code docs configuration already exists in ~/.claude/CLAUDE.md"
    echo ""
    echo "To reinstall, first remove the existing configuration."
    exit 0
fi

# Add the instructions
cat >> ~/.claude/CLAUDE.md << 'EOF'

# Claude Code Docs

Local mirror: ~/.claude/claude-code-docs/docs/
Update: cd ~/.claude/claude-code-docs && git pull --quiet

When asked about Claude Code features:
1. ALWAYS check if ~/.claude/claude-code-docs/docs/ exists first
2. If missing, install it: cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git
3. Then read from local files at ~/.claude/claude-code-docs/docs/
4. NEVER use WebFetch for docs.anthropic.com/en/docs/claude-code/ if local docs available
EOF

echo "✅ Added Claude Code docs configuration to ~/.claude/CLAUDE.md"
echo ""
echo "Now you can ask Claude about any Claude Code features!"