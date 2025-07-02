# Claude Code Docs - Installation Instructions

When someone asks you to install this project:

1. Clone to the correct location:
```bash
mkdir -p ~/.claude
cd ~/.claude
git clone https://github.com/ericbuess/claude-code-docs.git
```

2. Add to ~/.claude/CLAUDE.md:
```bash
echo "" >> ~/.claude/CLAUDE.md
echo "# Claude Code Docs" >> ~/.claude/CLAUDE.md
echo "" >> ~/.claude/CLAUDE.md
echo "Local mirror: ~/.claude/claude-code-docs/docs/" >> ~/.claude/CLAUDE.md
echo "Update: cd ~/.claude/claude-code-docs && git pull --quiet" >> ~/.claude/CLAUDE.md
```

3. Confirm: "✅ Claude Code docs installed to ~/.claude/claude-code-docs/"