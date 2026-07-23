> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 24 · June 8–12, 2026

> Move a session to a new directory with /cd, let subagents spawn their own subagents, and troubleshoot a broken configuration with safe mode.

<div className="digest-meta">
  <span>Releases <a href="/docs/docs/en/changelog#2-1-166">v2.1.166 → v2.1.176</a></span>
  <span>3 features · June 8–12</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Move a session with /cd</span>
    <span className="digest-feature-pill">v2.1.169</span>
  </div>

  <p className="digest-feature-lede">The new <code>/cd</code> command moves the current session to a different working directory without rebuilding the prompt cache: the new directory's <code>CLAUDE.md</code> is appended as a message instead of replacing the system prompt. The session relocates to the new directory's project storage, so `--resume` and `--continue` find it there. Claude prompts you to trust the directory if you haven't worked in it before.</p>

  <p className="digest-feature-try">Move the session into another project without restarting:</p>

  ```text Claude Code theme={null}
  > /cd ../other-project
  ```

  <a className="digest-feature-link" href="/docs/docs/en/commands#all-commands">Commands reference</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Subagents can spawn subagents</span>
    <span className="digest-feature-pill">v2.1.172</span>
  </div>

  <p className="digest-feature-lede">Subagents can now spawn their own subagents. The subagent panel below the prompt shows the full tree: each row carries a count of its descendants and a path back to <code>main</code>. Subagent chains are capped at five levels deep to prevent runaway concurrent trees.</p>

  <p className="digest-feature-try">Open the agents view to watch the nested tree as work fans out:</p>

  ```text Claude Code theme={null}
  > /agents
  ```

  <a className="digest-feature-link" href="/docs/docs/en/sub-agents#let-subagents-spawn-their-own-subagents">Spawn nested subagents</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Troubleshoot with safe mode</span>
    <span className="digest-feature-pill">v2.1.169</span>
  </div>

  <p className="digest-feature-lede">Start Claude Code with `--safe-mode`, or set <code>CLAUDE\_CODE\_SAFE\_MODE</code>, to launch with all customizations disabled: <code>CLAUDE.md</code>, skills, plugins, hooks, MCP servers, and custom commands and agents do not load. Authentication, model selection, built-in tools, and permissions still work. If a problem disappears in safe mode, one of those surfaces is the cause.</p>

  <p className="digest-feature-try">Launch a clean session to isolate a broken configuration:</p>

  ```bash terminal theme={null}
  claude --safe-mode
  ```

  <a className="digest-feature-link" href="/docs/docs/en/debug-your-config#test-against-a-clean-configuration">Test against a clean configuration</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><a href="/docs/docs/en/model-config#fallback-model-chains"><code>fallbackModel</code></a> configures up to three fallback models tried in order when the primary is overloaded or unavailable, and `--fallback-model` now applies to interactive sessions too</div>
    <div>Session titles are now generated in the language of your conversation; pin a specific one with the <code>language</code> setting</div>
    <div>`claude agents --json` adds `--all` to include completed sessions plus new <code>id</code> and <code>state</code> fields, and no longer omits blocked or newly dispatched sessions</div>
    <div>Browsing a marketplace's plugins in <code>/plugin</code> now has a search bar</div>
    <div>New <code>disableBundledSkills</code> setting and <code>CLAUDE\_CODE\_DISABLE\_BUNDLED\_SKILLS</code> hide bundled skills, workflows, and built-in commands from the model</div>
    <div>Deny rules accept a glob in the tool-name position, so <code>"\*"</code> denies all tools, and unknown tool names in deny rules now warn at startup</div>
    <div>Cross-session messaging is hardened: messages relayed via <code>SendMessage</code> from other sessions no longer carry user authority, and auto mode blocks them</div>
    <div>Amazon Bedrock reads the AWS region from <code>\~/.aws</code> config files when <code>AWS\_REGION</code> is unset, and <code>/status</code> shows where the region came from</div>
    <div>New <code>enforceAvailableModels</code> managed setting makes the <code>availableModels</code> allowlist also constrain the Default model</div>
    <div>Claude in Chrome browser tools now load in a single batched call instead of one per tool</div>
    <div><code>claude update</code> announces the target version before downloading instead of going silent</div>
    <div>New <code>footerLinksRegexes</code> setting adds regex-matched link badges to the footer row</div>
  </div>
</div>

[Full changelog for v2.1.166–v2.1.176 →](/docs/en/changelog#2-1-166)
