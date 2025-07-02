# Test Instructions for Claude

When a user asks you to test Claude Code docs access, follow these steps:

1. Check if the docs directory exists:
```bash
ls -la ~/.claude/claude-code-docs/docs/ 2>/dev/null | head -5 || echo "❌ Docs not found"
```

2. If docs exist, count them:
```bash
ls ~/.claude/claude-code-docs/docs/*.md 2>/dev/null | wc -l
```

3. Check if CLAUDE.md has the configuration:
```bash
grep -q "claude-code-docs" ~/.claude/CLAUDE.md 2>/dev/null && echo "✅ Configuration found" || echo "❌ Configuration missing"
```

4. Report to user:
- If everything is working: "✅ Claude Code docs are installed and accessible! I have access to [number] documentation files."
- If not installed: "❌ Claude Code docs are not installed. Run: claude 'install the claude code docs from github.com/ericbuess/claude-code-docs'"
- If partially installed: Provide specific guidance on what's missing