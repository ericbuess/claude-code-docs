# Installation Instructions for Claude

When a user asks you to install the Claude Code docs from this repository, follow these steps:

1. Create ~/.claude directory if it doesn't exist:
```bash
mkdir -p ~/.claude
```

2. Clone the repository:
```bash
cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git
```

3. Check if CLAUDE.md exists and back it up if it does:
```bash
[ -f ~/.claude/CLAUDE.md ] && cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup
```

4. Append the documentation configuration:
```bash
echo "" >> ~/.claude/CLAUDE.md
echo "# Claude Code Docs" >> ~/.claude/CLAUDE.md
echo "" >> ~/.claude/CLAUDE.md
echo "Local mirror of Claude Code documentation." >> ~/.claude/CLAUDE.md
echo "" >> ~/.claude/CLAUDE.md
echo "Pull latest: cd ~/.claude/claude-code-docs && git pull --quiet" >> ~/.claude/CLAUDE.md
echo "Docs location: ~/.claude/claude-code-docs/docs/" >> ~/.claude/CLAUDE.md
```

5. Verify installation:
```bash
ls -la ~/.claude/claude-code-docs/docs/ | head -5
```

6. Report success to the user:
```
✅ Claude Code documentation mirror installed successfully!

⚠️ IMPORTANT: For the changes to take effect in other Claude sessions:
1. Exit any existing Claude sessions with: /exit
2. Start fresh with: claude

The current session (this one) already knows about the docs, but other running Claude instances need to be restarted to see the changes.

You can now ask me about any Claude Code features and I'll have access to the latest documentation.

Try asking: "How do I use MCP servers?" or "What are Claude Code hooks?"
```

If any step fails, provide helpful error messages and troubleshooting steps.