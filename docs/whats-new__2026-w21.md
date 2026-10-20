> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 21 · May 18–22, 2026

> Use auto mode on the Pro plan and with Sonnet 4.6, see which skills, subagents, and MCP servers drive your plan limits in /usage, and review diffs with the new /code-review command.

Releases [v2.1.143 → v2.1.149](/docs/en/changelog#2-1-143)
1 feature · May 18–22

Auto mode on the Pro plan
CLI

Auto mode is now available on the Pro plan and supports Sonnet 4.6 alongside Opus. It replaces permission prompts with background safety checks: routine actions run without interrupting you, and destructive or suspicious ones are blocked and surfaced.

Update Claude Code, then cycle modes with Shift+Tab; auto mode appears in the cycle once your account meets the requirements:

```bash terminal theme={null}
claude update
```

The command prints `Successfully updated` with the new version number, or `Claude Code is up to date` if no update is needed. Once auto mode is active, the prompt footer shows `auto mode on`.

[Auto mode requirements](/docs/en/permission-modes#eliminate-prompts-with-auto-mode)

Other wins

[`/usage`](/docs/en/costs#track-your-costs) now shows a per-category breakdown of what's driving your plan limits, attributing recent usage to skills, subagents, plugins, and individual MCP servers"Extra usage" is renamed to "usage credits" across the CLI, and `/extra-usage` is now `/usage-credits`. The old name still works. The command requires signing in with your claude.ai subscription through `/login` and isn't available with API key authentication.New [`/code-review`](/docs/en/code-review) command reports correctness bugs at a chosen effort level such as `/code-review high`, and `--comment` posts findings as inline GitHub PR comments. `/simplify` remains as a separate cleanup-only review\.Background sessions now appear in `/resume` alongside interactive ones, marked with `bg`, and sessions pinned with `Ctrl+T` in `claude agents` stay alive when idle`claude agents --json` lists live sessions as JSON for scripting, such as status bars and session pickersThe PowerShell tool is now enabled by default on Windows for Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry users; opt out with `CLAUDE_CODE_USE_POWERSHELL_TOOL=0``claude plugin disable` now refuses when another enabled plugin depends on the target, and `claude plugin enable` force-enables transitive dependenciesThe `/plugin` marketplace browse pane shows projected context cost, and the Discover and Browse screens list a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installationNew `worktree.bgIsolation: "none"` setting lets background sessions edit the working copy directly without `EnterWorktree`, for repos where worktrees are impracticalMarkdown output renders GFM task list checkboxes, and the `/diff` detail view scrolls with the keyboardStatus line JSON input now includes GitHub repo and PR information when detectedEnterprise: the `allowAllClaudeAiMcps` managed setting loads claude.ai cloud MCP connectors alongside `managed-mcp.json`

[Full changelog for v2.1.143–v2.1.149 →](/docs/en/changelog#2-1-143)
