> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 20 · May 11–15, 2026

> Manage every Claude Code session from one screen with agent view, keep Claude working toward a goal until a condition holds, and run fast mode on Opus 4.7 by default.

Releases [v2.1.139 → v2.1.142](https://code.claude.com/docs/en/changelog.md#2-1-139)
3 features · May 11–15

Agent view
research preview

`claude agents` opens one screen for every Claude Code session: what's running, what's blocked on your input, and what's done. Dispatch a bug fix, a pull request review, and a flaky-test investigation as three rows, keep working in another window, and step in only when a row needs you. Attach to any row to drop into its full conversation, then press `←` to return to the list. Each background session keeps running without a terminal attached.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/agent-view.mp4?fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=0eefe6cbe75464c8f7902bba630ab7a4" />

Open the dashboard from your shell:

```bash terminal theme={null}
claude agents
```

[Agent view](https://code.claude.com/docs/en/agent-view.md)

/goal
v2.1.139

Set a completion condition and Claude keeps working toward it across turns without you prompting each step. After every turn, a fast model checks whether the condition holds; if not, Claude starts another turn instead of handing control back. Useful for substantial work with a verifiable end state, like migrating a module until every call site compiles and tests pass. The goal clears once the condition is met, and works in interactive, `-p`, and Remote Control.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/goal.mp4?fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=6806df3780c548b93a02d6fa71da276b" />

Set a goal and let Claude run until it holds:

```text Claude Code theme={null}
> /goal all tests in test/auth pass and the lint step is clean
```

[Goals](https://code.claude.com/docs/en/goal.md)

Fast mode on Opus 4.7
research preview

`/fast` now runs on Opus 4.7 by default instead of Opus 4.6. Fast mode is a high-speed Opus configuration: the same model quality at about 2.5x the speed for a higher per-token cost, useful for rapid iteration and live debugging. Pricing is unchanged at \$30/\$150 per MTok, the same as Opus 4.6 fast mode. To pin fast mode to Opus 4.6, set `CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1`.

![The Claude Code model picker showing Opus 4.7 Fast 1M as the default with the Fast toggle on](https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/fast-mode-opus-47.png?fit=max\&auto=format\&n=ITvjicPxe1SM3GX7\&q=85\&s=6b6d92f7748ce5328a1ee9a269fb1a87)

Toggle fast mode, now running on Opus 4.7:

```text Claude Code theme={null}
> /fast
```

[Fast mode on Opus 4.7](https://code.claude.com/docs/en/fast-mode.md#understand-the-cost-tradeoff)

Other wins

`claude agents` gained dispatch flags (`--add-dir`, `--settings`, `--mcp-config`, `--plugin-dir`, `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions`) to configure background sessions, and `claude agents --cwd <path>` scopes the session list to a directoryNew hook `args: string[]` exec form spawns the command directly without a shell, so path placeholders never need quotingNew `continueOnBlock` config option for `PostToolUse` hooks feeds the hook's rejection reason back to Claude and continues the turn instead of ending itNew `terminalSequence` field in hook JSON output lets hooks emit desktop notifications, window titles, and bells without a controlling terminalThe Rewind menu added "Summarize up to here" to compress earlier context while keeping recent turns intactRemote Control, `/schedule`, claude.ai MCP connectors, and notification preferences are now disabled when `ANTHROPIC_API_KEY`, `apiKeyHelper`, or `ANTHROPIC_AUTH_TOKEN` is set, even alongside a claude.ai login; unset the API key to use these featuresMCP stdio servers now receive `CLAUDE_PROJECT_DIR` in their environment, matching hooks, and plugin configs can reference `${CLAUDE_PROJECT_DIR}` in commands`claude plugin details <name>` shows a plugin's component inventory and projected per-session token cost, and the `/plugin` details pane now also lists the LSP servers a plugin providesPlugins with a root-level `SKILL.md` and no `skills/` subdirectory are now surfaced as a skill`/feedback` can now include recent sessions from the last 24 hours or 7 days for issues spanning more than the current sessionAgent tool `subagent_type` now matches case- and separator-insensitively, so `"Code Reviewer"` resolves to `code-reviewer`

[Full changelog for v2.1.139–v2.1.142 →](https://code.claude.com/docs/en/changelog.md#2-1-139)
