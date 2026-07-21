> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 29 · July 13–17, 2026

> Pull live data into published artifacts through MCP connectors, and use Claude Code with a screen reader in the new screen reader mode.

<div className="digest-meta">
  <span>Releases <a href="/docs/docs/en/changelog#2-1-207">v2.1.207 → v2.1.212</a></span>
  <span>2 features · July 13–17</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Artifacts call your MCP connectors</span>
    <span className="digest-feature-pill">web</span>
  </div>

  <p className="digest-feature-lede">A published artifact can now call MCP connectors each time someone views it, so a dashboard shows live data and can take actions on demand rather than a snapshot from the session that built it. Each call runs through the viewing account's own connections, and viewers approve access before the page's first connector call. This week also adds public sharing links, editor roles for shared editing on Team and Enterprise plans, and artifacts created from Claude Tag sessions.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/ItzF3QVI6L0QypjJ/images/whats-new/artifacts-mcp.mp4?fit=max&auto=format&n=ItzF3QVI6L0QypjJ&q=85&s=ff8b81ed52b26c773899dc28cec959e6" data-path="images/whats-new/artifacts-mcp.mp4" />
  </Frame>

  <p className="digest-feature-try">Name the connector and the data you want in your prompt:</p>

  ```text Claude Code theme={null}
  > Build a dashboard artifact of open pull requests that pulls the live list through my GitHub connector when the page loads.
  ```

  <a className="digest-feature-link" href="/docs/docs/en/artifacts#pull-live-data-with-mcp-connectors">Pull live data with MCP connectors</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Screen reader mode</span>
    <span className="digest-feature-pill">CLI</span>
  </div>

  <p className="digest-feature-lede">Screen reader mode replaces the visual terminal interface with plain, linear text: instead of boxes, spinners, and in-place redraws, Claude Code prints labeled lines that a screen reader such as VoiceOver or NVDA reads in order, so you can approve permissions and review output end to end. Turn it on per session with a flag, per shell with the <code>CLAUDE\_AX\_SCREEN\_READER</code> environment variable, or everywhere with the <code>axScreenReader</code> setting.</p>

  <p className="digest-feature-try">Start a session in screen reader mode:</p>

  ```bash terminal theme={null}
  claude --ax-screen-reader
  ```

  <a className="digest-feature-link" href="/docs/docs/en/accessibility#turn-on-screen-reader-mode">Turn on screen reader mode</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><code>/fork</code> now copies your conversation into a new background session with its own row in <code>claude agents</code> while you keep working; the in-session forked subagent it used to launch is now <code>/subtask</code></div>
    <div><a href="/docs/docs/en/permission-modes#enable-auto-mode-on-bedrock-agent-platform-or-foundry">Auto mode</a> no longer needs the <code>CLAUDE\_CODE\_ENABLE\_AUTO\_MODE</code> opt-in on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry; administrators can turn it off with <code>disableAutoMode</code></div>
    <div>MCP tool calls that run longer than two minutes now move to the background automatically so the session stays usable; tune or disable the threshold with <code>CLAUDE\_CODE\_MCP\_AUTO\_BACKGROUND\_MS</code></div>
    <div>New <code>claude auto-mode reset</code> restores the default auto-mode configuration, and `--yes` skips the confirmation prompt</div>
    <div>New <a href="/docs/docs/en/corporate-launcher">corporate launcher</a> support: <code>CLAUDE\_CODE\_PROCESS\_WRAPPER</code> or the <code>processWrapper</code> setting runs the processes Claude Code starts from its own binary, such as the background service and agent view sessions, through a required wrapper executable</div>
    <div><code>vimInsertModeRemaps</code> setting maps two-key insert-mode sequences such as <code>jj</code> to Escape in vim mode</div>
    <div>`--forward-subagent-text` and <code>CLAUDE\_CODE\_FORWARD\_SUBAGENT\_TEXT</code> include subagent text and thinking blocks in <a href="/docs/docs/en/headless">stream-json output</a></div>
    <div>Session-wide caps stop runaway loops: WebSearch calls and subagent spawns each default to 200, tunable with <code>CLAUDE\_CODE\_MAX\_WEB\_SEARCHES\_PER\_SESSION</code> and <code>CLAUDE\_CODE\_MAX\_SUBAGENTS\_PER\_SESSION</code></div>
    <div>"Always allow" permission rules save at the repository root, so approvals granted in a git worktree persist across sessions and worktrees</div>
    <div>Amazon Bedrock, Google Cloud's Agent Platform, and Claude Platform on AWS now default to Claude Opus 4.8</div>
    <div>The collapsed tool summary line shows a live elapsed-time counter, so long-running tool calls visibly tick instead of looking stuck</div>
  </div>
</div>

[Full changelog for v2.1.207–v2.1.212 →](/docs/en/changelog#2-1-207)
