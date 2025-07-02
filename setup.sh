#!/bin/bash
# Add Claude Code docs instructions to ~/.claude/CLAUDE.md

cat >> ~/.claude/CLAUDE.md << 'EOF'

# Claude Code Docs

Local mirror: ~/.claude/claude-code-docs/docs/
Update: cd ~/.claude/claude-code-docs && git pull --quiet

If user asks about Claude Code features and docs not found locally:
1. Check if ~/.claude/claude-code-docs exists
2. If not, install: cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git
3. Then read from ~/.claude/claude-code-docs/docs/
EOF

echo "✅ Added Claude Code docs configuration to ~/.claude/CLAUDE.md"
echo ""
echo "Now you can ask Claude about any Claude Code features!"