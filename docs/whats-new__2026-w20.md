> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 20 · May 11–15, 2026

> Manage every Claude Code session from one screen with agent view, keep Claude working toward a goal until a condition holds, and run fast mode on Opus 4.7 by default.

<div className="digest-meta">
  <span>Releases <a href="/en/changelog#2-1-139">v2.1.139 → v2.1.142</a></span>
  <span>3 features · May 11–15</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Agent view</span>
    <span className="digest-feature-pill">research preview</span>
  </div>

  <p className="digest-feature-lede"><code>claude agents</code> opens one screen for every Claude Code session: what's running, what's blocked on your input, and what's done. Dispatch a bug fix, a pull request review, and a flaky-test investigation as three rows, keep working in another window, and step in only when a row needs you. Attach to any row to drop into its full conversation, then press <code>←</code> to return to the list. Each background session keeps running without a terminal attached.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/agent-view.mp4?fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=0eefe6cbe75464c8f7902bba630ab7a4" data-path="images/whats-new/agent-view.mp4" />
  </Frame>

  <p className="digest-feature-try">Open the dashboard from your shell:</p>

  ```bash terminal theme={null}
  claude agents
  ```

  <a className="digest-feature-link" href="/en/agent-view">Agent view</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/goal</span>
    <span className="digest-feature-pill">v2.1.139</span>
  </div>

  <p className="digest-feature-lede">Set a completion condition and Claude keeps working toward it across turns without you prompting each step. After every turn, a fast model checks whether the condition holds; if not, Claude starts another turn instead of handing control back. Useful for substantial work with a verifiable end state, like migrating a module until every call site compiles and tests pass. The goal clears once the condition is met, and works in interactive, <code>-p</code>, and Remote Control.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/goal.mp4?fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=6806df3780c548b93a02d6fa71da276b" data-path="images/whats-new/goal.mp4" />
  </Frame>

  <p className="digest-feature-try">Set a goal and let Claude run until it holds:</p>

  ```text Claude Code theme={null}
  > /goal all tests in test/auth pass and the lint step is clean
  ```

  <a className="digest-feature-link" href="/en/goal">Goals</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Fast mode on Opus 4.7</span>
    <span className="digest-feature-pill">research preview</span>
  </div>

  <p className="digest-feature-lede"><code>/fast</code> now runs on Opus 4.7 by default instead of Opus 4.6. Fast mode is a high-speed Opus configuration: the same model quality at about 2.5x the speed for a higher per-token cost, useful for rapid iteration and live debugging. Pricing is unchanged at $30/$150 per MTok, the same as Opus 4.6 fast mode. To pin fast mode to Opus 4.6, set <code>CLAUDE\_CODE\_OPUS\_4\_6\_FAST\_MODE\_OVERRIDE=1</code>.</p>

  <Frame>
    <img className="w-full" src="https://mintcdn.com/claude-code/ITvjicPxe1SM3GX7/images/whats-new/fast-mode-opus-47.png?fit=max&auto=format&n=ITvjicPxe1SM3GX7&q=85&s=6b6d92f7748ce5328a1ee9a269fb1a87" alt="The Claude Code model picker showing Opus 4.7 Fast 1M as the default with the Fast toggle on" width="3840" height="2160" data-path="images/whats-new/fast-mode-opus-47.png" />
  </Frame>

  <p className="digest-feature-try">Toggle fast mode, now running on Opus 4.7:</p>

  ```text Claude Code theme={null}
  > /fast
  ```

  <a className="digest-feature-link" href="/en/fast-mode#use-fast-mode-on-opus-4-7">Fast mode on Opus 4.7</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><code>claude agents</code> gained dispatch flags (<code>--add-dir</code>, <code>--settings</code>, <code>--mcp-config</code>, <code>--plugin-dir</code>, <code>--permission-mode</code>, <code>--model</code>, <code>--effort</code>, <code>--dangerously-skip-permissions</code>) to configure background sessions, and <code>claude agents --cwd \<path></code> scopes the session list to a directory</div>
    <div>New hook <code>args: string\[]</code> exec form spawns the command directly without a shell, so path placeholders never need quoting</div>
    <div>New <code>continueOnBlock</code> config option for <code>PostToolUse</code> hooks feeds the hook's rejection reason back to Claude and continues the turn instead of ending it</div>
    <div>New <code>terminalSequence</code> field in hook JSON output lets hooks emit desktop notifications, window titles, and bells without a controlling terminal</div>
    <div>The Rewind menu added "Summarize up to here" to compress earlier context while keeping recent turns intact</div>
    <div>Remote Control, <code>/schedule</code>, Claude.ai MCP connectors, and notification preferences are now disabled when <code>ANTHROPIC\_API\_KEY</code>, <code>apiKeyHelper</code>, or <code>ANTHROPIC\_AUTH\_TOKEN</code> is set, even alongside a Claude.ai login; unset the API key to use these features</div>
    <div>MCP stdio servers now receive <code>CLAUDE\_PROJECT\_DIR</code> in their environment, matching hooks, and plugin configs can reference <code>\${"{"}CLAUDE\_PROJECT\_DIR{"}"}</code> in commands</div>
    <div><code>claude plugin details \<name></code> shows a plugin's component inventory and projected per-session token cost, and the <code>/plugin</code> details pane now also lists the LSP servers a plugin provides</div>
    <div>Plugins with a root-level <code>SKILL.md</code> and no <code>skills/</code> subdirectory are now surfaced as a skill</div>
    <div><code>/feedback</code> can now include recent sessions from the last 24 hours or 7 days for issues spanning more than the current session</div>
    <div>Agent tool <code>subagent\_type</code> now matches case- and separator-insensitively, so <code>"Code Reviewer"</code> resolves to <code>code-reviewer</code></div>
  </div>
</div>

[Full changelog for v2.1.139–v2.1.142 →](/en/changelog#2-1-139)
