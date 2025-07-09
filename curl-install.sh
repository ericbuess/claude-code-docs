#!/bin/bash
# Minimal installation script optimized for curl piping
# Usage: curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/curl-install.sh | bash

set -e

# Simple error handling for piped execution
trap 'echo "Installation failed. Please check the error messages above." >&2' ERR

# Check for git
if ! command -v git &> /dev/null; then
    echo "Error: git is not installed. Please install git first." >&2
    exit 1
fi

# Clone repository
echo "Cloning Claude Code documentation..."
git clone --quiet https://github.com/ericbuess/claude-code-docs.git || exit 1

cd claude-code-docs || exit 1
DOCS_PATH=$(pwd)

# Create command directory and file
mkdir -p ~/.claude/commands

# Create docs command
echo "Creating /user:docs command..."
cat > ~/.claude/commands/docs.md << EOF
${DOCS_PATH}/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: \$ARGUMENTS
EOF

# Run hook setup if available
if [ -f "setup-hook.sh" ]; then
    echo "Setting up auto-update hook..."
    bash setup-hook.sh 2>/dev/null || echo "Note: Auto-update setup encountered issues. Docs will still work."
fi

# Return to original directory
cd .. 2>/dev/null || true

# Success message
echo
echo "✅ Installation complete!"
echo "📍 Docs location: $DOCS_PATH"
echo "🔧 Usage: /user:docs <topic>"
echo "📚 Example: /user:docs hooks"