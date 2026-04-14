> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 14 · March 30 – April 3, 2026

> Computer use in the CLI, interactive in-product lessons, flicker-free rendering, per-tool MCP result-size overrides, and plugin executables on PATH.

<div className="digest-meta">
  <span>Releases <a href="/en/changelog#2-1-86">v2.1.86 → v2.1.91</a></span>
  <span>5 features · March 30 – April 3</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Computer use in the CLI</span>
    <span className="digest-feature-pill">research preview</span>
  </div>

  <p className="digest-feature-lede">Last week computer use landed in the Desktop app. This week it's in the CLI: Claude can open native apps, click through UI, test its own changes, and fix what breaks, all from your terminal. Web apps already had verification loops; native iOS, macOS, and other GUI-only apps didn't. Now they do. Best for closing the loop on apps and tools where there's no API to call. Still early; expect rough edges.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/cli-computer-use.mp4?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=c17a337902308d7c9121013ded0494db" data-path="images/whats-new/cli-computer-use.mp4" />
  </Frame>

  <p className="digest-feature-try">Run <code>/mcp</code>, find <code>computer-use</code>, and toggle it on. Then ask Claude to verify a change end to end:</p>

  ```text Claude Code theme={null}
  > Open the iOS simulator, tap through onboarding, and screenshot each step
  ```

  <a className="digest-feature-link" href="/en/computer-use">Computer use guide</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/powerup</span>
    <span className="digest-feature-pill">v2.1.90</span>
  </div>

  <p className="digest-feature-lede">Interactive lessons that teach Claude Code features through animated demos, right inside your terminal. Claude Code releases frequently, and features that would have changed how you work last month can slip by. Run <code>/powerup</code> once and you'll know what's there.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/powerup.mp4?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=fb88beddc0ecc8029da5ab029e4b28f1" data-path="images/whats-new/powerup.mp4" />
  </Frame>

  <p className="digest-feature-try">Run it:</p>

  ```text Claude Code theme={null}
  > /powerup
  ```

  <a className="digest-feature-link" href="/en/commands">Commands reference</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Flicker-free rendering</span>
    <span className="digest-feature-pill">v2.1.89</span>
  </div>

  <p className="digest-feature-lede">Opt into a new alt-screen renderer with virtualized scrollback. The prompt input stays pinned to the bottom, mouse selection works across long conversations, and the flicker on redraw is gone. Unset <code>CLAUDE\_CODE\_NO\_FLICKER</code> to roll back.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/CfffsX01JHFnIKvD/images/whats-new/flicker-free.mp4?fit=max&auto=format&n=CfffsX01JHFnIKvD&q=85&s=7719e35e52a3f9734b0cf69edac333ad" data-path="images/whats-new/flicker-free.mp4" />
  </Frame>

  <p className="digest-feature-try">Set the env var and restart Claude Code:</p>

  ```bash theme={null}
  export CLAUDE_CODE_NO_FLICKER=1
  claude
  ```

  <a className="digest-feature-link" href="/en/fullscreen">Fullscreen rendering</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">MCP result-size override</span>
    <span className="digest-feature-pill">v2.1.91</span>
  </div>

  <p className="digest-feature-lede">MCP server authors can now raise the truncation cap on a specific tool by setting <code>anthropic/maxResultSizeChars</code> in the tool's <code>tools/list</code> entry, up to a hard ceiling of 500K characters. The cap used to be global, so tools that occasionally returned inherently large payloads like database schemas or full file trees hit the default limit and got persisted to disk with a file reference. Per-tool overrides keep those results inline when the tool really needs them.</p>

  <p className="digest-feature-try">Annotate the tool in your server's <code>tools/list</code> response:</p>

  ```json highlight={5} theme={null}
  {
    "name": "get_schema",
    "description": "Returns the full database schema",
    "_meta": {
      "anthropic/maxResultSizeChars": 500000
    }
  }
  ```

  <a className="digest-feature-link" href="/en/mcp#raise-the-limit-for-a-specific-tool">MCP reference</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Plugin executables on PATH</span>
    <span className="digest-feature-pill">v2.1.91</span>
  </div>

  <p className="digest-feature-lede">Place an executable in a <code>bin/</code> directory at your plugin root and Claude Code adds that directory to the Bash tool's <code>PATH</code> while the plugin is enabled. Claude can then invoke the binary as a bare command from any Bash tool call, with no absolute path or wrapper script needed. Handy for packaging CLI helpers next to the commands, agents, and hooks that call them.</p>

  <p className="digest-feature-try">Add a <code>bin/</code> directory at the plugin root:</p>

  ```text highlight={4, 5} theme={null}
  my-plugin/
  ├── .claude-plugin/
  │   └── plugin.json
  └── bin/
      └── my-tool
  ```

  <a className="digest-feature-link" href="/en/plugins-reference#file-locations-reference">Plugins reference</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div>Auto mode follow-ups: new <code>PermissionDenied</code> hook fires on classifier denials (return <code>retry: true</code> to let Claude try a different approach), and <code>/permissions</code> → Recent lets you retry manually with <code>r</code></div>
    <div>New <code>defer</code> value for <code>permissionDecision</code> in <code>PreToolUse</code> hooks: <code>-p</code> sessions pause at a tool call and exit with a <code>deferred\_tool\_use</code> payload so an SDK app or custom UI can surface it, then resume with <code>--resume</code></div>
    <div><code>/buddy</code>: hatch a small creature that watches you code (April 1st)</div>
    <div><code>disableSkillShellExecution</code> setting blocks inline shell from skills, slash commands, and plugin commands</div>
    <div>Edit tool now works on files viewed via <code>cat</code> or <code>sed -n</code> without a separate Read</div>
    <div>Hook output over 50K saved to disk with a path + preview instead of injected into context</div>
    <div>Thinking summaries off by default in interactive sessions (<code>showThinkingSummaries: true</code> to restore)</div>
    <div>Voice mode: push-to-talk modifier combos, Windows WebSocket, macOS Apple Silicon mic permission</div>
    <div><code>claude-cli://</code> deep links accept multi-line prompts (encoded <code>%0A</code>)</div>
  </div>
</div>

[Full changelog for v2.1.86–v2.1.91 →](/en/changelog#2-1-86)
