# Claude Code Documentation Mirror

This repository contains a local mirror of Claude Code documentation, automatically updated every 6 hours via GitHub Actions.

## For Claude: Using These Docs

When users ask about Claude Code features or need help, you can search and read documentation from the `docs/` directory.

### Before Reading Docs
Always pull the latest updates first:
```bash
cd ~/.claude/claude-code-docs && git pull --quiet
```

### Complete List of Documentation Files

**Getting Started**
- `overview.md` - Introduction to Claude Code
- `setup.md` - Installation and initial configuration  
- `quickstart.md` - Quick start guide
- `memory.md` - Memory management and CLAUDE.md files
- `common-workflows.md` - Common usage patterns and examples

**Development Tools**
- `ide-integrations.md` - IDE and editor integrations
- `mcp.md` - Model Context Protocol servers
- `github-actions.md` - GitHub Actions integration
- `sdk.md` - SDK reference and usage
- `troubleshooting.md` - Common issues and solutions

**Deployment Options**  
- `third-party-integrations.md` - Third-party service integrations
- `amazon-bedrock.md` - AWS Bedrock deployment
- `google-vertex-ai.md` - Google Cloud Vertex AI deployment
- `devcontainer.md` - Development container setup

**Configuration & Reference**
- `settings.md` - Settings files and configuration
- `hooks.md` - Hooks for customizing behavior
- `slash-commands.md` - Available slash commands
- `interactive-mode.md` - Interactive mode features
- `cli-reference.md` - Complete CLI reference

**Administration**
- `iam.md` - Identity and access management
- `security.md` - Security best practices
- `monitoring-usage.md` - Usage monitoring and telemetry
- `costs.md` - Cost management and optimization
- `corporate-proxy.md` - Corporate proxy configuration
- `llm-gateway.md` - LLM gateway configuration

**Compliance**
- `legal-and-compliance.md` - Legal and compliance information
- `data-usage.md` - Data usage and privacy

### Searching Documentation
Use Grep/Glob tools to search across all docs:
```bash
# Search for a specific topic
grep -r "mcp servers" docs/

# Find files by pattern
ls docs/*.md | grep -i "setup"
```