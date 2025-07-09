# Testing Guide for claude-code-docs

This guide provides detailed steps to test and verify the claude-code-docs installation and functionality.

## Prerequisites
- Claude Code CLI installed
- This repository cloned locally
- You're in the claude-code-docs directory

## Step-by-Step Testing Process

### 1. Manual Installation Test
From the claude-code-docs directory, run these commands:

```bash
# Store the current directory path
DOCS_PATH=$(pwd)

# Create the commands directory
mkdir -p ~/.claude/commands

# Create the docs command
echo "$DOCS_PATH/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: \$ARGUMENTS" > ~/.claude/commands/docs.md

# Run the hook setup
bash setup-hook.sh

# Verify the command was created
cat ~/.claude/commands/docs.md
```

### 2. Test the /user:docs Command
Start Claude Code CLI and test the command:

```bash
# Start Claude Code from any directory
claude

# In the Claude Code session, test the command
/user:docs hooks

# Try other queries
/user:docs memory
/user:docs what is mcp
/user:docs how do I use slash commands?
```

### 3. Verify Hook Installation
Check that the hook was properly installed:

```bash
# Check if settings.json exists
ls -la ~/.claude/settings.json

# View the hook configuration
cat ~/.claude/settings.json | jq '.hooks.PreToolUse'

# Verify the hook contains the correct path
cat ~/.claude/settings.json | jq -r '.hooks.PreToolUse[].hooks[].command'
```

Expected output should show a command like:
```
if [[ $(jq -r .tool_input.file_path 2>/dev/null) == */your/path/to/claude-code-docs/* ]]; then cd /your/path/to/claude-code-docs && git pull --quiet; fi
```

### 4. Test Automatic Git Pull
To verify the hook triggers git pull:

```bash
# Make a test commit to simulate an update
echo "test" > test-file.txt
git add test-file.txt
git commit -m "Test commit"
git push

# In a Claude Code session, use the docs command
/user:docs hooks

# Check if git pull was executed
git log --oneline -1

# Clean up
rm test-file.txt
git add test-file.txt
git commit -m "Remove test file"
git push
```

### 5. Test Fresh Installation
Test the curl installation from a different directory:

```bash
# Go to a temporary directory
cd /tmp

# Run the installation
curl -fsSL https://raw.githubusercontent.com/ericbuess/claude-code-docs/main/quick-install.sh | bash

# Verify the docs were cloned
ls -la claude-code-docs/

# Start Claude Code and test
claude
/user:docs settings
```

### 6. Debug Hook Execution
If the hook isn't working, debug it:

```bash
# Start Claude Code with debug logging
claude --debug

# Use the docs command
/user:docs test

# Look for lines like:
# [DEBUG] Executing hooks for PreToolUse:Read
# [DEBUG] Hook command completed with status 0
```

### 7. Manual Hook Test
Test the hook command directly:

```bash
# Create a test JSON input
echo '{"tool_input":{"file_path":"'$(pwd)'/docs/hooks.md"}}' > test-input.json

# Run the hook command manually
cat test-input.json | if [[ $(jq -r .tool_input.file_path 2>/dev/null) == *$(pwd)/* ]]; then echo "Hook would trigger git pull"; fi

# Clean up
rm test-input.json
```

## Troubleshooting

### Command Not Found
If `/user:docs` returns "command not found":
1. Check ~/.claude/commands/docs.md exists
2. Verify the path in the file is correct
3. Restart Claude Code CLI

### Hook Not Triggering
If git pull doesn't run automatically:
1. Check ~/.claude/settings.json has the PreToolUse hook
2. Verify the path pattern in the hook matches your docs location
3. Use `claude --debug` to see hook execution
4. Check that jq is installed: `which jq`

### Quote/Escaping Issues
If you get shell errors during installation:
1. Use the curl installation method instead
2. Or run the install.sh script directly: `bash install.sh`

## Expected Behavior

When everything is working correctly:
1. `/user:docs <query>` searches the local documentation
2. Before reading any docs file, git pull runs automatically (silently)
3. You always get the latest documentation content
4. The command works from any directory

## Validation Checklist

- [ ] ~/.claude/commands/docs.md exists
- [ ] The docs.md file contains the correct path
- [ ] ~/.claude/settings.json exists
- [ ] The settings.json contains a PreToolUse hook for Read
- [ ] The hook command contains the correct docs path
- [ ] `/user:docs` command works in Claude Code
- [ ] Git pull runs automatically (check with git log timestamps)
- [ ] Documentation is accessible from any project directory