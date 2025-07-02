# Test Instructions for Claude

When a user asks you to read the Claude Code overview from ~/.claude/claude-code-docs/docs/overview.md:

1. Try to read the file directly:
```bash
cat ~/.claude/claude-code-docs/docs/overview.md | head -20
```

2. If successful:
- Show the first few lines of the overview
- Confirm: "✅ Reading from local docs at ~/.claude/claude-code-docs/"
- Mention it's instant, no web fetch needed

3. If file not found:
- Report: "❌ Local docs not found at ~/.claude/claude-code-docs/"
- Suggest: "Install with: claude 'install the claude code docs from github.com/ericbuess/claude-code-docs'"

The key is to make it clear you're reading from LOCAL files, not fetching from the web.