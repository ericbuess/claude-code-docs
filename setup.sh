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

Local docs: ~/.claude-code-docs/docs/
When asked about Claude Code features, read from there.
If missing, tell user: cd ~ && git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs
EOF

echo "✅ Added Claude Code docs configuration to ~/.claude/CLAUDE.md"
echo ""
echo "Now install the docs:"
echo "cd ~ && git clone https://github.com/ericbuess/claude-code-docs.git .claude-code-docs"