# Claude Code Documentation Mirror

[![Last Update](https://img.shields.io/github/last-commit/ericbuess/claude-code-docs/main.svg?label=docs%20updated)](https://github.com/ericbuess/claude-code-docs/commits/main)

Local mirror of Claude Code documentation files from https://docs.anthropic.com/en/docs/claude-code/, updated every 3 hours.

## Why This Exists

- **Faster than web fetching** - Read from local files instantly
- **Works offline** - No internet required after cloning
- **Always up-to-date** - Auto-updates every 3 hours via GitHub Actions

## Installation

Run this single command from wherever you want to store the docs:

```bash
git clone https://github.com/ericbuess/claude-code-docs.git && cd claude-code-docs && DOCS_PATH="$(pwd)" && mkdir -p ~/.claude/commands && echo "$DOCS_PATH/ contains a local update copy of all docs for Claude Code and is faster for you to access. Please use a Read task to research Claude Code docs there (rather than a web fetch) and tell me about the following: \$ARGUMENTS" > ~/.claude/commands/docs.md && ([ -f ~/.claude/settings.json ] && jq --arg path "$DOCS_PATH" '.hooks.PreToolUse = [(.hooks.PreToolUse // [])[] | select(.matcher != "Read")] + [{"matcher": "Read", "hooks": [{"type": "command", "command": ("if [[ $(jq -r .tool_input.file_path 2>/dev/null) == *" + $path + "/* ]]; then cd " + $path + " && git pull --quiet; fi")}]}]' ~/.claude/settings.json > ~/.claude/settings.json.tmp && mv ~/.claude/settings.json.tmp ~/.claude/settings.json || echo '{"hooks":{"PreToolUse":[{"matcher":"Read","hooks":[{"type":"command","command":"if [[ $(jq -r .tool_input.file_path 2>/dev/null) == *'"$DOCS_PATH"'/* ]]; then cd '"$DOCS_PATH"' && git pull --quiet; fi"}]}]}}' > ~/.claude/settings.json) && cd .. && printf "✅ Installation complete!\n   📁 Docs location: $DOCS_PATH\n   💬 Command: /user:docs\n   🔄 Auto-updates: Enabled\n"
```

This single command will:
1. Clone the repository
2. Create the `/user:docs` slash command with the correct path
3. Add a hook to automatically `git pull` when reading docs
4. Return to your original directory

## Usage

Now you can use the slash command:

### Basic usage:
```
/user:docs hooks
/user:docs mcp
/user:docs memory
```

### Creative examples:
```
/user:docs what environment variables exist and how do I use them?
/user:docs recommend some useful slash commands based on my usage so far
/user:docs please explain all recent changes to the docs
/user:docs how do I trigger custom commands on demand?
/user:docs search all docs and find unique ways to use Claude Code CLI
```

Claude reads from your local docs instantly and can search across all documentation to answer complex questions!

## Keeping Docs Updated

The GitHub repository automatically updates every 3 hours. To keep your local copy in sync:

### Automatic Updates (Recommended)

Add this hook to your `~/.claude/settings.json` to automatically pull updates before reading docs:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Read",
        "hooks": [
          {
            "type": "command",
            "command": "if [[ $(jq -r '.tool_input.file_path' 2>/dev/null) == */claude-code-docs/* ]]; then cd /path/to/claude-code-docs && git pull --quiet; fi"
          }
        ]
      }
    ]
  }
}
```

Replace `/path/to/claude-code-docs` with your actual path. This hook runs `git pull` automatically whenever Claude reads from the docs directory.

### Manual Updates

To update manually:
```bash
cd /path/to/claude-code-docs && git pull
```

## License

Documentation content belongs to Anthropic.