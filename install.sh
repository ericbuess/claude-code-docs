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
cat > ~/.claude/commands/docs.md << 'EOF'
${DOCS_PATH}/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: $ARGUMENTS
EOF
sed -i.bak "s|\${DOCS_PATH}|$DOCS_PATH|g" ~/.claude/commands/docs.md
rm ~/.claude/commands/docs.md.bak

# Run hook setup
bash setup-hook.sh

cd ..
echo "Installation complete with auto-updates!"
echo "Docs location: $DOCS_PATH"
echo "Command: /user:docs"