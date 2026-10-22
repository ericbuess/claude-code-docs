> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 22 · May 25–29, 2026

> Run Claude Code on Claude Opus 4.8, orchestrate large tasks with dynamic workflows, catch security issues with the security-guidance plugin, and use fast mode on Opus 4.8 at a lower price.

Releases [v2.1.150 → v2.1.157](/docs/en/changelog.md#2-1-150)
4 features · May 25–29

Claude Opus 4.8
new model

Opus 4.8 is now the default on Max, Team Premium, Enterprise pay-as-you-go, and the Anthropic API. It defaults to high effort; use `/effort xhigh` for harder tasks. Requires v2.1.154 or later.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/QsIrGXGFg6xd7joy/images/whats-new/opus-4-8.mp4?fit=max&auto=format&n=QsIrGXGFg6xd7joy&q=85&s=6ebcf5fe136467da2b254de1fe749ea7" />

Switch to Opus 4.8 by name, or pick it from the model picker:

```text title="Claude Code" wrap theme={null}
/model claude-opus-4-8
```

[Model configuration](/docs/en/model-config.md#available-models)

Dynamic workflows
research preview

A workflow is an orchestration script Claude writes for your task and runs across many subagents in the background. Use one when a task is too large for one conversation to coordinate: a codebase-wide audit, a large migration, a research question that needs cross-checking. Manage runs with `/workflows`.

![Claude Code on Opus 4.8 showing a Dynamic workflow requested indicator for a prompt that asks for a workflow to migrate every internal fetch() call](https://mintcdn.com/claude-code/QsIrGXGFg6xd7joy/images/whats-new/dynamic-workflows.png?fit=max\&auto=format\&n=QsIrGXGFg6xd7joy\&q=85\&s=26671fa8607cec3453ed9753f821bd4f)

Describe the task and ask for a workflow:

```text title="Claude Code" wrap theme={null}
create a workflow that migrates every internal fetch() call to the new HttpClient wrapper
```

[Dynamic workflows](/docs/en/workflows.md)

Security guidance plugin
plugin

The security-guidance plugin reviews Claude's code changes for vulnerabilities and fixes them in the same session. It runs a fast pattern check on each edit, a model review at the end of each turn, and a deeper agentic review on commit or push. Add project rules in `.claude/claude-security-guidance.md`.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/QsIrGXGFg6xd7joy/images/whats-new/security-guidance.mp4?fit=max&auto=format&n=QsIrGXGFg6xd7joy&q=85&s=c91d865936411586f42b24c558bcdd1d" />

Install it from the official Anthropic marketplace:

```text title="Claude Code" wrap theme={null}
/plugin install security-guidance@claude-plugins-official
```

Then activate it in the current session:

```text title="Claude Code" wrap theme={null}
/reload-plugins
```

[Security guidance plugin](/docs/en/security-guidance.md)

Fast mode on Opus 4.8
research preview

Fast mode now defaults to Opus 4.8 at \$10/\$50 per MTok: 2x the standard rate for about 2.5x the speed. Opus 4.7 and 4.6 stay at \$30/\$150. Opus 4.6 fast mode is deprecated.

Toggle fast mode, now on Opus 4.8:

```text title="Claude Code" wrap theme={null}
/fast
```

[Fast mode pricing](/docs/en/fast-mode.md#understand-the-cost-tradeoff)

Other wins

In `claude agents`, prefix a shell command with `!` to run it as a background job you can attach to and detach from; also available as `claude --bg --exec 'pytest -x'`Plugins in `.claude/skills` directories are now loaded automatically, no marketplace required, and `claude plugin init <name>` scaffolds a new pluginNew `/reload-skills` command re-scans skill directories without restarting, and `SessionStart` hooks can return `reloadSkills: true` to make skills they install available in the same sessionSkills and commands can set `disallowed-tools` in frontmatter to remove tools from the model while the skill is activeNew `MessageDisplay` hook event lets hooks transform or hide assistant message text as it is displayedClaude Code now switches to your configured `--fallback-model` for the rest of the session when the primary model is not found, instead of failing every requestPlugins can declare `defaultEnabled: false` in `plugin.json` or a marketplace entry, so they install without turning on until you enable themVim mode: `/` in NORMAL mode opens reverse history search, matching Bash and Zsh vi-modeStreaming tool execution is now always enabled, including with telemetry disabled and on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry`←←` to open the agents view now works on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and with telemetry disabledClaude in Chrome: pick which connected browser to use via `/chrome` → "Select browser…", or in-chat when a browser action runs with multiple connected`claude mcp list` and `claude mcp get` now show unapproved `.mcp.json` servers as pending approval instead of auto-approving and connecting when output is piped

[Full changelog for v2.1.150–v2.1.157 →](/docs/en/changelog.md#2-1-150)
