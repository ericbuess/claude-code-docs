> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 21 · May 18–22, 2026

> Use auto mode on the Pro plan and with Sonnet 4.6, see which skills, subagents, and MCP servers drive your plan limits in /usage, and review diffs with the new /code-review command.

<div className="digest-meta">
  <span>Releases <a href="/docs/en/changelog#2-1-143">v2.1.143 → v2.1.149</a></span>
  <span>1 feature · May 18–22</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Auto mode on the Pro plan</span>
    <span className="digest-feature-pill">CLI</span>
  </div>

  <p className="digest-feature-lede">Auto mode is now available on the Pro plan and supports Sonnet 4.6 alongside Opus. It replaces permission prompts with background safety checks: routine actions run without interrupting you, and destructive or suspicious ones are blocked and surfaced.</p>

  <p className="digest-feature-try">Update Claude Code, then cycle modes with Shift+Tab; auto mode appears in the cycle once your account meets the requirements:</p>

  ```bash terminal theme={null}
  claude update
  ```

  <p className="digest-feature-try">The command prints <code>Successfully updated</code> with the new version number, or <code>Claude Code is up to date</code> if no update is needed. Once auto mode is active, the prompt footer shows <code>auto mode on</code>.</p>

  <a className="digest-feature-link" href="/docs/en/permission-modes#eliminate-prompts-with-auto-mode">Auto mode requirements</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><a href="/docs/en/costs#track-your-costs"><code>/usage</code></a> now shows a per-category breakdown of what's driving your plan limits, attributing recent usage to skills, subagents, plugins, and individual MCP servers</div>
    <div>"Extra usage" is renamed to "usage credits" across the CLI, and <code>/extra-usage</code> is now <code>/usage-credits</code>. The old name still works. The command requires signing in with your claude.ai subscription through <code>/login</code> and isn't available with API key authentication.</div>
    <div>New <a href="/docs/en/code-review"><code>/code-review</code></a> command reports correctness bugs at a chosen effort level such as <code>/code-review high</code>, and <code>--comment</code> posts findings as inline GitHub PR comments. <code>/simplify</code> remains as a separate cleanup-only review.</div>
    <div>Background sessions now appear in <code>/resume</code> alongside interactive ones, marked with <code>bg</code>, and sessions pinned with <code>Ctrl+T</code> in <code>claude agents</code> stay alive when idle</div>
    <div><code>claude agents --json</code> lists live sessions as JSON for scripting, such as status bars and session pickers</div>
    <div>The PowerShell tool is now enabled by default on Windows for Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry users; opt out with <code>CLAUDE\_CODE\_USE\_POWERSHELL\_TOOL=0</code></div>
    <div><code>claude plugin disable</code> now refuses when another enabled plugin depends on the target, and <code>claude plugin enable</code> force-enables transitive dependencies</div>
    <div>The <code>/plugin</code> marketplace browse pane shows projected context cost, and the Discover and Browse screens list a plugin's commands, agents, skills, hooks, and MCP/LSP servers before installation</div>
    <div>New <code>worktree.bgIsolation: "none"</code> setting lets background sessions edit the working copy directly without <code>EnterWorktree</code>, for repos where worktrees are impractical</div>
    <div>Markdown output renders GFM task list checkboxes, and the <code>/diff</code> detail view scrolls with the keyboard</div>
    <div>Status line JSON input now includes GitHub repo and PR information when detected</div>
    <div>Enterprise: the <code>allowAllClaudeAiMcps</code> managed setting loads claude.ai cloud MCP connectors alongside <code>managed-mcp.json</code></div>
  </div>
</div>

[Full changelog for v2.1.143–v2.1.149 →](/en/changelog#2-1-143)
