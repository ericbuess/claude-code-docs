> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 19 · May 4–8, 2026

> Load plugins from .zip archives and URLs, search command history across every project with Ctrl+R, branch new worktrees from local HEAD or the remote default, and block actions unconditionally with auto mode hard deny rules.

<div className="digest-meta">
  <span>Releases <a href="/en/changelog#2-1-128">v2.1.128 → v2.1.136</a></span>
  <span>2 features · May 4–8</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Plugins from .zip archives and URLs</span>
  </div>

  <p className="digest-feature-lede">`--plugin-dir` now accepts a <code>.zip</code> plugin archive in addition to a directory, and the new `--plugin-url` flag fetches a plugin archive from a URL for the current session. Useful for trying a plugin before adding it to a marketplace, or for shipping internal plugins from an artifact store.</p>

  <p className="digest-feature-try">Load a plugin straight from a URL:</p>

  ```bash terminal theme={null}
  claude --plugin-url https://example.com/my-plugin.zip
  ```

  <a className="digest-feature-link" href="/en/plugins">Plugins guide</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">History search across all your projects</span>
    <span className="digest-feature-pill">v2.1.129</span>
  </div>

  <p className="digest-feature-lede"><code>Ctrl+R</code> reverse-search now defaults to all prompts across every project, restoring the behavior from before v2.1.124. Press <code>Ctrl+S</code> while searching to narrow back to the current project or session. Handy when you remember a command you ran in another repo last week and don't want to go digging for it.</p>

  <a className="digest-feature-link" href="/en/interactive-mode#command-history">Interactive mode: command history</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div>New <code>worktree.baseRef</code> setting (<code>fresh</code> | <code>head</code>) controls whether <code>--worktree</code>, the <code>EnterWorktree</code> tool, and agent-isolation worktrees branch from the remote default branch or local <code>HEAD</code>; the default <code>fresh</code> keeps unpushed commits out of new worktrees</div>
    <div>New <code>settings.autoMode.hard\_deny</code> rules block matching actions unconditionally in auto mode, regardless of allow exceptions, for actions that should never run automatically even when broader allow rules apply</div>
    <div>Hooks now receive the active effort level via the `effort.level` JSON input field and the `$CLAUDE_EFFORT` environment variable, and Bash tool commands can read <code>\$CLAUDE\_EFFORT</code></div>
    <div><code>CLAUDE\_CODE\_DISABLE\_ALTERNATE\_SCREEN=1</code> opts out of the fullscreen alternate-screen renderer and keeps the conversation in the terminal's native scrollback</div>
    <div><code>CLAUDE\_CODE\_PACKAGE\_MANAGER\_AUTO\_UPDATE</code> lets Homebrew or WinGet installations run the upgrade in the background and prompt to restart</div>
    <div><code>CLAUDE\_CODE\_SESSION\_ID</code> is now in the Bash tool subprocess environment, matching the <code>session\_id</code> passed to hooks</div>
    <div><code>/mcp</code> now shows the tool count for connected servers and flags servers that connected with 0 tools</div>
    <div><code>--channels</code> now works with console (API key) authentication</div>
    <div>Subprocesses such as Bash, hooks, MCP, and LSP no longer inherit <code>OTEL\_\*</code> environment variables, so OTEL-instrumented apps run via the Bash tool no longer pick up the CLI's own OTLP endpoint</div>
    <div>Sub-agent progress summaries now hit the prompt cache, cutting <code>cache\_creation</code> token cost by roughly 3x</div>
    <div>Several OAuth and credential reliability fixes: parallel sessions no longer dead-end at 401 after a refresh-token race, MCP OAuth refresh tokens are no longer lost when multiple servers refresh concurrently, and a rare login loop from a concurrent credential write is fixed</div>
    <div>New <code>parentSettingsBehavior</code> admin key lets admins opt SDK <code>managedSettings</code> into the policy merge</div>
  </div>
</div>

[Full changelog for v2.1.128–v2.1.136 →](/en/changelog#2-1-128)
