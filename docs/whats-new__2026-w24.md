> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 24 · June 8–12, 2026

> Move a session to a new directory with /cd, let subagents spawn their own subagents, and troubleshoot a broken configuration with safe mode.

Releases [v2.1.166 → v2.1.176](/docs/en/changelog#2-1-166)
3 features · June 8–12

Move a session with /cd
v2.1.169

The new `/cd` command moves the current session to a different working directory without rebuilding the prompt cache: the new directory's `CLAUDE.md` is appended as a message instead of replacing the system prompt. The session relocates to the new directory's project storage, so `--resume` and `--continue` find it there. Claude prompts you to trust the directory if you haven't worked in it before.

Move the session into another project without restarting:

```text Claude Code theme={null}
> /cd ../other-project
```

[Commands reference](/docs/en/commands#all-commands)

Subagents can spawn subagents
v2.1.172

Subagents can now spawn their own subagents. The subagent panel below the prompt shows the full tree: each row carries a count of its descendants and a path back to `main`. Subagent chains are capped at five levels deep to prevent runaway concurrent trees.

Open the agents view to watch the nested tree as work fans out:

```text Claude Code theme={null}
> /agents
```

[Spawn nested subagents](/docs/en/sub-agents#let-subagents-spawn-their-own-subagents)

Troubleshoot with safe mode
v2.1.169

Start Claude Code with `--safe-mode`, or set `CLAUDE_CODE_SAFE_MODE`, to launch with all customizations disabled: `CLAUDE.md`, skills, plugins, hooks, MCP servers, and custom commands and agents do not load. Authentication, model selection, built-in tools, and permissions still work. If a problem disappears in safe mode, one of those surfaces is the cause.

Launch a clean session to isolate a broken configuration:

```bash terminal theme={null}
claude --safe-mode
```

[Test against a clean configuration](/docs/en/debug-your-config#test-against-a-clean-configuration)

Other wins

[`fallbackModel`](/docs/en/model-config#fallback-model-chains) configures up to three fallback models tried in order when the primary is overloaded or unavailable, and `--fallback-model` now applies to interactive sessions tooSession titles are now generated in the language of your conversation; pin a specific one with the `language` setting`claude agents --json` adds `--all` to include completed sessions plus new `id` and `state` fields, and no longer omits blocked or newly dispatched sessionsBrowsing a marketplace's plugins in `/plugin` now has a search barNew `disableBundledSkills` setting and `CLAUDE_CODE_DISABLE_BUNDLED_SKILLS` hide bundled skills, workflows, and built-in commands from the modelDeny rules accept a glob in the tool-name position, so `"*"` denies all tools, and unknown tool names in deny rules now warn at startupAgent messaging is hardened: messages relayed via `SendMessage` from other agents no longer carry user authority, and auto mode blocks themAmazon Bedrock reads the AWS region from `~/.aws` config files when `AWS_REGION` is unset, and `/status` shows where the region came fromNew `enforceAvailableModels` managed setting makes the `availableModels` allowlist also constrain the Default modelClaude in Chrome browser tools now load in a single batched call instead of one per tool`claude update` announces the target version before downloading instead of going silentNew `footerLinksRegexes` setting adds regex-matched link badges to the footer row

[Full changelog for v2.1.166–v2.1.176 →](/docs/en/changelog#2-1-166)
