#!/bin/bash
git clone https://github.com/ericbuess/claude-code-docs.git
cd claude-code-docs
DOCS_PATH=$(pwd)
mkdir -p ~/.claude/commands
echo "$DOCS_PATH/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: \$ARGUMENTS" > ~/.claude/commands/docs.md
bash setup-hook.sh
cd ..
echo "Installation complete!"