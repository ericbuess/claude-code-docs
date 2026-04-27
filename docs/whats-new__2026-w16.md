> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 16 · April 13–17, 2026

> Claude Opus 4.7 with the new xhigh effort level, Routines on Claude Code on the web, /ultrareview cloud code review, a /usage breakdown that shows what's driving your limits, and native binaries replacing the bundled JavaScript.

<div className="digest-meta">
  <span>Releases <a href="/docs/en/changelog#2-1-105">v2.1.105 → v2.1.113</a></span>
  <span>5 features · April 13–17</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Claude Opus 4.7</span>
    <span className="digest-feature-pill">new model</span>
  </div>

  <p className="digest-feature-lede">Anthropic's strongest coding model yet is now the default on Max and Team Premium, and available everywhere else from <code>/model</code>. It adds a new <code>xhigh</code> effort level that sits between <code>high</code> and <code>max</code>: best results for most coding and agentic tasks, applied as the default the first time you switch to 4.7. <code>/effort</code> now opens an interactive arrow-key slider when you call it without arguments, so you can dial intelligence against speed without remembering the level names.</p>

  <p className="digest-feature-try">Switch model and effort in one go:</p>

  ```text Claude Code theme={null}
  > /model opus
  > /effort xhigh
  ```

  <a className="digest-feature-link" href="/docs/en/model-config#adjust-effort-level">Model config: effort levels</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Routines</span>
    <span className="digest-feature-pill">web</span>
  </div>

  <p className="digest-feature-lede">Templated cloud agents that fire on a schedule, a GitHub event, or an API call. Define a routine once on Claude Code on the web with a prompt, the repos it can touch, and the connectors it needs, then let PR-opened, release-published, or your own webhook trigger it without your machine running. The trigger picker now covers GitHub events with optional filters and gives every routine a tokened <code>/fire</code> endpoint for external systems.</p>

  <Frame>
    <img className="w-full" src="https://mintcdn.com/claude-code/FTi4SBJ9YRs7d-5X/images/whats-new/routines.png?fit=max&auto=format&n=FTi4SBJ9YRs7d-5X&q=85&s=2ba818ea9280c549511cb48b9b4d1dc5" alt="Creating a routine on Claude Code on the web with schedule, GitHub event, and API triggers" width="1440" height="810" data-path="images/whats-new/routines.png" />
  </Frame>

  <p className="digest-feature-try">Create one from the web UI, or scaffold from your terminal:</p>

  ```text Claude Code theme={null}
  > /schedule daily PR review at 9am
  ```

  <a className="digest-feature-link" href="/docs/en/routines">Routines guide</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/usage breakdown</span>
    <span className="digest-feature-pill">CLI</span>
  </div>

  <p className="digest-feature-lede">More visibility into where your Claude Code usage goes. <code>/usage</code> now shows what's driving your limits: parallel sessions, subagents, cache misses, and long context, each with a percentage of your last 24 hours and a tip to optimize it. Press <code>d</code> or <code>w</code> to switch between day and week views.</p>

  <Frame>
    <img className="w-full" src="https://mintcdn.com/claude-code/FTi4SBJ9YRs7d-5X/images/whats-new/usage.png?fit=max&auto=format&n=FTi4SBJ9YRs7d-5X&q=85&s=792a4b43cbef4e2931974831f076bca6" alt="The /usage command showing a breakdown of what's contributing to limits usage" width="1204" height="1182" data-path="images/whats-new/usage.png" />
  </Frame>

  <p className="digest-feature-try">Run it any time:</p>

  ```text Claude Code theme={null}
  > /usage
  ```

  <a className="digest-feature-link" href="/docs/en/commands">Commands reference</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/ultrareview</span>
    <span className="digest-feature-pill">v2.1.111</span>
  </div>

  <p className="digest-feature-lede">Comprehensive code review in the cloud. Ultrareview fans your branch out across parallel reviewers on Claude Code on the web, runs an adversarial critique pass over each finding, and returns a verified findings report while your terminal stays free. Call it with no arguments to review your current branch, or pass a PR number to fetch and review that PR. The launch dialog now shows a diffstat so you know what's going up before you confirm.</p>

  <p className="digest-feature-try">Review the branch you're on:</p>

  ```text Claude Code theme={null}
  > /ultrareview
  ```

  <p className="digest-feature-try">Or point it at a PR:</p>

  ```text Claude Code theme={null}
  > /ultrareview 1234
  ```

  <a className="digest-feature-link" href="/docs/en/ultrareview">Ultrareview guide</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Native binaries</span>
    <span className="digest-feature-pill">v2.1.113</span>
  </div>

  <p className="digest-feature-lede">The <code>claude</code> CLI now spawns a native per-platform binary instead of bundled JavaScript, so the installed <code>claude</code> command no longer invokes Node. The npm package pulls the right binary in through an optional dependency such as <code>@anthropic-ai/claude-code-darwin-arm64</code>, so your install command doesn't change. The standalone installer already shipped this binary; npm now matches it.</p>

  <p className="digest-feature-try">Upgrade and check what you're running:</p>

  ```bash theme={null}
  claude update
  claude --version
  ```

  <a className="digest-feature-link" href="/docs/en/setup">Setup guide</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><a href="/docs/en/permission-modes#eliminate-prompts-with-auto-mode">Auto mode</a> is now available for Max subscribers on Opus 4.7, and the <code>--enable-auto-mode</code> flag is no longer required</div>
    <div><a href="/docs/en/interactive-mode#session-recap">Session recap</a> shows a one-line summary of what happened while you were away; run <code>/recap</code> on demand or turn it off from <code>/config</code></div>
    <div>New <code>/tui</code> command and <code>tui</code> setting switch between classic and flicker-free rendering mid-conversation; focus view moved from <code>Ctrl+O</code> to its own <code>/focus</code> command</div>
    <div>Push notification tool: with <a href="/docs/en/remote-control">Remote Control</a> connected and "Push when Claude decides" enabled, Claude can ping your phone when it needs you</div>
    <div>Plugins can ship background watchers via a top-level <code>monitors</code> manifest key that auto-arms at session start or on skill invoke</div>
    <div>"Auto (match terminal)" option in <code>/theme</code> follows your terminal's dark/light mode</div>
    <div><code>/fewer-permission-prompts</code> scans your transcripts for common read-only Bash and MCP calls and proposes an allowlist for <code>.claude/settings.json</code></div>
    <div>Claude can now discover and run built-in commands like <code>/init</code>, <code>/review</code>, and <code>/security-review</code> via the Skill tool</div>
    <div><code>PreCompact</code> hooks can block compaction by exiting with code 2 or returning <code>{"{"}"decision":"block"{"}"}</code></div>
    <div><code>ENABLE\_PROMPT\_CACHING\_1H</code> opts API key, Bedrock, Vertex, and Foundry users into 1-hour prompt cache TTL</div>
    <div><code>sandbox.network.deniedDomains</code> setting carves specific domains out of a broader <code>allowedDomains</code> wildcard</div>
    <div><code>/undo</code> is now an alias for <code>/rewind</code>, and <code>/proactive</code> is an alias for <code>/loop</code></div>
    <div>Hardened Bash permissions: deny rules now match through <code>env</code>/<code>sudo</code>/<code>watch</code> wrappers, and <code>Bash(find:\*)</code> allow rules no longer auto-approve <code>-exec</code> or <code>-delete</code></div>
  </div>
</div>

[Full changelog for v2.1.105–v2.1.113 →](/en/changelog#2-1-105)
