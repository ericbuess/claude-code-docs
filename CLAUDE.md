# Claude Code Documentation Mirror

This repository contains a local mirror of Claude Code documentation, automatically updated every 6 hours via GitHub Actions.

## For Claude: Using These Docs

When users ask about Claude Code features or need help, you can search and read documentation from the `docs/` directory.

### Before Reading Docs
Always pull the latest updates first:
```bash
cd ~/.claude/claude-code-docs && git pull --quiet
```

### Available Documentation
The `docs/` directory contains 25+ documentation files including:
- **Getting Started**: overview, setup, quickstart, memory, common-workflows
- **Development**: ide-integrations, mcp, github-actions, sdk, troubleshooting  
- **Deployment**: third-party-integrations, amazon-bedrock, google-vertex-ai
- **Administration**: iam, security, monitoring-usage, costs
- **Reference**: cli-reference, interactive-mode, slash-commands, settings, hooks
- **Compliance**: legal-and-compliance, data-usage

### Documentation Manifest
`docs/docs_manifest.json` contains metadata for all documentation files including:
- Filenames and their SHA-256 hashes
- Last update timestamps
- Source URLs from Anthropic's documentation

### Searching Documentation
Use Grep/Glob tools to search across all docs:
```bash
# Search for a specific topic
grep -r "mcp servers" docs/

# Find files by pattern
ls docs/*.md | grep -i "setup"
```

## For Users: Installation

To install these docs locally for offline access:

```bash
# Clone to Claude's directory
cd ~/.claude && git clone https://github.com/ericbuess/claude-code-docs.git

# Add these lines to ~/.claude/CLAUDE.md:
# Claude Code Documentation  
# Location: ~/.claude/claude-code-docs/
# Available: overview, setup, quickstart, memory, mcp, settings, troubleshooting, 25+ more
# Update: cd ~/.claude/claude-code-docs && git pull --quiet
# Details: See CLAUDE.md in that directory if needed
```

That's it! Claude will automatically pull updates when reading docs.