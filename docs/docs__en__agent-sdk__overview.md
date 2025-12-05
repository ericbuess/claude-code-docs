# Agent SDK overview

Build custom AI agents with the Claude Agent SDK

---

<Note>
The Claude Code SDK has been renamed to the **Claude Agent SDK**. If you're migrating from the old SDK, see the [Migration Guide](/docs/en/agent-sdk/migration-guide).
</Note>

## Installation

<CodeGroup>

```bash TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

```bash Python
pip install claude-agent-sdk
```

</CodeGroup>

## SDK Options

The Claude Agent SDK is available in multiple forms to suit different use cases:

  - **[TypeScript SDK](/docs/en/agent-sdk/typescript)** - For Node.js and web applications
  - **[Python SDK](/docs/en/agent-sdk/python)** - For Python applications and data science
  - **[Streaming vs Single Mode](/docs/en/agent-sdk/streaming-vs-single-mode)** - Understanding input modes and best practices

## Why use the Claude Agent SDK?

Built on top of the agent harness that powers Claude Code, the Claude Agent SDK provides all the building blocks you need to build production-ready agents.

Taking advantage of the work we've done on Claude Code including:
- **Context Management**: Automatic compaction and context management to ensure your agent doesn't run out of context.
- **Rich tool ecosystem**: File operations, code execution, web search, and MCP extensibility
- **Advanced permissions**: Fine-grained control over agent capabilities
- **Production essentials**: Built-in error handling, session management, and monitoring
- **Optimized Claude integration**: Automatic prompt caching and performance optimizations

## What can you build with the SDK?

Here are some example agent types you can create:

**Coding agents:**
- SRE agents that diagnose and fix production issues
- Security review bots that audit code for vulnerabilities
- Oncall engineering assistants that triage incidents
- Code review agents that enforce style and best practices

**Business agents:**
- Legal assistants that review contracts and compliance
- Finance advisors that analyze reports and forecasts
- Customer support agents that resolve technical issues
- Content creation assistants for marketing teams

## Core Concepts

### Authentication

For basic authentication, retrieve an Claude API key from the [Claude Console](/) and set the `ANTHROPIC_API_KEY` environment variable.

The SDK also supports authentication via third-party API providers:

- **Amazon Bedrock**: Set `CLAUDE_CODE_USE_BEDROCK=1` environment variable and configure AWS credentials
- **Google Vertex AI**: Set `CLAUDE_CODE_USE_VERTEX=1` environment variable and configure Google Cloud credentials
- **Microsoft Foundry**: Set `CLAUDE_CODE_USE_FOUNDRY=1` environment variable and configure Azure credentials

For detailed configuration instructions for third-party providers, see the [Amazon Bedrock](https://code.claude.com/docs/en/amazon-bedrock), [Google Vertex AI](https://code.claude.com/docs/en/google-vertex-ai), and [Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry) documentation.

<Note>
Unless previously approved, we do not allow third party developers to apply Claude.ai rate limits for their products, including agents built on the Claude Agent SDK. Please use the API key authentication methods described in this document instead.
</Note>

### Full Claude Code Feature Support

The SDK provides access to all the default features available in Claude Code, leveraging the same file system-based configuration:

- **Subagents**: Launch specialized agents stored as Markdown files in `./.claude/agents/`
- **Agent Skills**: Extend Claude with specialized capabilities stored as `SKILL.md` files in `./.claude/skills/`
- **Hooks**: Execute custom commands configured in `./.claude/settings.json` that respond to tool events
- **Slash Commands**: Use custom commands defined as Markdown files in `./.claude/commands/`
- **Plugins**: Load custom plugins programmatically using the `plugins` option to extend Claude Code with custom commands, agents, skills, hooks, and MCP servers. See [Plugins](/docs/en/agent-sdk/plugins) for details.
- **Memory (CLAUDE.md)**: Maintain project context through `CLAUDE.md` or `.claude/CLAUDE.md` files in your project directory, or `~/.claude/CLAUDE.md` for user-level instructions. To load these files, you must explicitly set `settingSources: ['project']` (TypeScript) or `setting_sources=["project"]` (Python) in your options. See [Modifying system prompts](/docs/en/agent-sdk/modifying-system-prompts#method-1-claudemd-files-project-level-instructions) for details.

These features work identically to their Claude Code counterparts by reading from the same file system locations.

### System Prompts

System prompts define your agent's role, expertise, and behavior. This is where you specify what kind of agent you're building.

### Tool Permissions

Control which tools your agent can use with fine-grained permissions:
- `allowedTools` - Explicitly allow specific tools
- `disallowedTools` - Block specific tools
- `permissionMode` - Set overall permission strategy

### Model Context Protocol (MCP)

Extend your agents with custom tools and integrations through MCP servers. This allows you to connect to databases, APIs, and other external services.

## Building with the Claude Agent SDK

If you're building coding agents powered by the Claude Agent SDK, please note that **Claude Code** refers specifically to Anthropic's official product including the CLI, VS Code extension, web experience, and future integrations we build.

### For partners integrating Claude Agent SDK:

<Note>
The use of Claude branding for products built on Claude is optional.
</Note>

When referencing Claude in your agent selector or product:

**Allowed naming options:**
- **Claude Agent** (preferred for dropdown menus)
- **Claude** (when within a menu already labeled "Agents")
- **\{YourAgentName\} Powered by Claude** (if you have an existing agent name)

**Not permitted:**
- "Claude Code" or "Claude Code Agent"
- Claude Code-branded ASCII art or visual elements that mimic Claude Code

Your product should maintain its own branding and not appear to be Claude Code or any Anthropic product. 

For questions about branding compliance or to discuss your product's Claude integration, [contact our sales team](https://claude.com/contact-sales).

## Reporting Bugs

If you encounter bugs or issues with the Agent SDK:

- **TypeScript SDK**: [Report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-typescript/issues)
- **Python SDK**: [Report issues on GitHub](https://github.com/anthropics/claude-agent-sdk-python/issues)

## Changelog

View the full changelog for SDK updates, bug fixes, and new features:

- **TypeScript SDK**: [View CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md)
- **Python SDK**: [View CHANGELOG.md](https://github.com/anthropics/claude-agent-sdk-python/blob/main/CHANGELOG.md)

## Related Resources

- [CLI Reference](https://code.claude.com/docs/en/cli-reference) - Complete CLI documentation
- [GitHub Actions Integration](https://code.claude.com/docs/en/github-actions) - Automate your GitHub workflow
- [MCP Documentation](https://code.claude.com/docs/en/mcp) - Extend Claude with custom tools
- [Common Workflows](https://code.claude.com/docs/en/common-workflows) - Step-by-step guides
- [Troubleshooting](https://code.claude.com/docs/en/troubleshooting) - Common issues and solutions