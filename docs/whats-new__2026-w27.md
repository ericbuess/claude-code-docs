> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 27 · June 29 – July 3, 2026

> Claude Sonnet 5 becomes the default model, Claude in Chrome reaches general availability, subagents run in the background by default, Claude Desktop arrives on Linux in beta, and /radio tunes into Claude FM.

<div className="digest-meta">
  <span>Releases <a href="/docs/en/changelog#2-1-195">v2.1.195 → v2.1.201</a></span>
  <span>5 features · June 29 – July 3</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Claude Sonnet 5</span>
    <span className="digest-feature-pill">new model</span>
  </div>

  <p className="digest-feature-lede">Sonnet 5 is the new default model for Pro, Team Standard, and Enterprise subscription seats: top-tier coding and tool use at Sonnet pricing, with a native 1M-token context window and adaptive thinking on by default. API pricing is promotional at \$2/\$10 per MTok through August 31. Requires v2.1.197 or later.</p>

  <p className="digest-feature-try">Switch to Sonnet 5 by name, or pick it from the model picker:</p>

  ```text Claude Code theme={null}
  > /model claude-sonnet-5
  ```

  <a className="digest-feature-link" href="/docs/en/model-config#available-models">Model configuration</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Claude in Chrome is generally available</span>
    <span className="digest-feature-pill">v2.1.198</span>
  </div>

  <p className="digest-feature-lede">The Chrome integration is out of preview for everyone on a direct Anthropic plan. Claude Code drives your browser through the Claude in Chrome extension: it opens tabs, clicks through pages, fills forms, reads console logs, and shares your login state, so it can test the app it builds without you switching contexts.</p>

  <a className="digest-feature-link" href="/docs/en/chrome">Use Claude Code with Chrome</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Subagents run in the background by default</span>
    <span className="digest-feature-pill">v2.1.198</span>
  </div>

  <p className="digest-feature-lede">Claude now keeps working while subagents run and picks up their results when they finish, instead of pausing the conversation to wait. Claude still runs a subagent in the foreground when it needs the result before continuing, and background subagents surface every permission prompt in your main session. Pin a subagent's behavior with the <code>background</code> frontmatter field.</p>

  <a className="digest-feature-link" href="/docs/en/sub-agents#run-subagents-in-foreground-or-background">Run subagents in foreground or background</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Claude Desktop on Linux</span>
    <span className="digest-feature-pill">Desktop</span>
  </div>

  <p className="digest-feature-lede">The Claude desktop app is now available on Ubuntu 22.04+ and Debian 12+ in beta, on x86\_64 and arm64. You get the same Chat, Cowork, and Claude Code experience as macOS and Windows: parallel sessions, visual diff review, an integrated terminal and editor, and live app preview. Installs from Anthropic's apt repository, so updates arrive through regular package updates.</p>

  <a className="digest-feature-link" href="/docs/en/desktop-linux">Claude Desktop on Linux</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/radio</span>
    <span className="digest-feature-pill">CLI</span>
  </div>

  <p className="digest-feature-lede">Claude FM is on the air. <code>/radio</code> opens the lo-fi radio stream in your browser for something to code to, and prints the stream URL when no browser is available. Not available on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/x358isu_VzLnyTEN/images/whats-new/radio.mp4?fit=max&auto=format&n=x358isu_VzLnyTEN&q=85&s=36a0c33859cef119c7192dceea8bcbd3" data-path="images/whats-new/radio.mp4" />
  </Frame>

  <p className="digest-feature-try">Tune in from any session:</p>

  ```text Claude Code theme={null}
  > /radio
  ```

  <a className="digest-feature-link" href="/docs/en/commands#all-commands">All commands</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><a href="/docs/en/artifacts">Artifacts</a> are now generally available and included on Pro and Max plans, joining Team and Enterprise</div>
    <div>Admins can set an <a href="/docs/en/model-config#organization-default-model">organization default model</a> in the org console; it shows as "Org default" in <code>/model</code> when you haven't picked a model yourself</div>
    <div>Stacked skill invocations like <code>/skill-a /skill-b do XYZ</code> now load all leading skills (up to 5), not only the first</div>
    <div><code>AskUserQuestion</code> dialogs no longer auto-continue by default; opt into an idle timeout via <code>/config</code></div>
    <div>The "default" permission mode is now named "Manual" across the CLI, `--help`, VS Code, and JetBrains; `--permission-mode manual` is accepted alongside `default`</div>
    <div>New <code>/dataviz</code> skill gives chart and dashboard design guidance, with a runnable color-palette validator</div>
    <div>The built-in Explore agent now inherits the main session's model (capped at Opus) instead of running on Haiku</div>
    <div>Background agents launched from <code>claude agents</code> now commit, push, and open a draft PR when they finish code work in a worktree, instead of stopping to ask</div>
    <div>Hook matchers with hyphenated identifiers like <code>code-reviewer</code> now exact-match instead of substring-matching; use <code>mcp\_\_brave-search\_\_.\*</code> to match all tools from a hyphenated MCP server</div>
    <div>Transient server rate-limit errors unrelated to your usage limit are now retried automatically with backoff for subscribers instead of failing the turn</div>
    <div>The streaming idle watchdog is now on by default for all providers: it aborts and retries when a response stream produces no events for 5 minutes (<code>CLAUDE\_ENABLE\_STREAM\_WATCHDOG=0</code> to disable)</div>
  </div>
</div>

[Full changelog for v2.1.195–v2.1.201 →](/en/changelog#2-1-195)
