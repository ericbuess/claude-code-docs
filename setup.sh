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

When asked about Claude Code features:
1. Check if .claude-code-docs/ exists in current directory or any parent
2. If not found, suggest: git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
3. Then read from .claude-code-docs/docs/
4. The docs auto-update every 3 hours via GitHub
EOF

echo "✅ Added Claude Code docs configuration to ~/.claude/CLAUDE.md"
echo ""
echo "Now clone the docs in any project where you want to use them:"
echo "git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs"