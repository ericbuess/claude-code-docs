# Uninstallation Instructions for Claude

When a user asks you to uninstall the Claude Code docs mirror, follow these steps:

1. Remove the repository:
```bash
rm -rf ~/.claude/claude-code-docs
```

2. Check if CLAUDE.md has the documentation configuration:
```bash
grep -n "Claude Code Documentation" ~/.claude/CLAUDE.md
```

3. If found, remove the configuration section:
```bash
# Create a backup first
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup

# Remove the 4-line documentation section
sed -i '' '/# Claude Code Documentation/,+3d' ~/.claude/CLAUDE.md
```

4. Verify removal:
```bash
echo "✅ Claude Code documentation mirror has been uninstalled"
echo ""
echo "Removed:"
echo "- Repository from ~/.claude/claude-code-docs" 
echo "- Configuration from ~/.claude/CLAUDE.md"
echo ""
echo "Your CLAUDE.md backup is at: ~/.claude/CLAUDE.md.backup"
echo ""
echo "⚠️ IMPORTANT: For the changes to take effect:"
echo "1. Exit any existing Claude sessions with: /exit"
echo "2. Start fresh with: claude"
```

Note: On Linux, use `sed -i` instead of `sed -i ''`