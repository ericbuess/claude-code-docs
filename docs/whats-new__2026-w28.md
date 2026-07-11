> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 28 · July 6–10, 2026

> Browse external sites from the Desktop app's built-in browser, run a full setup checkup with /doctor, and pick up auto mode transcript protections and agent view upgrades.

<div className="digest-meta">
  <span>Releases <a href="/docs/en/changelog#2-1-202">v2.1.202 → v2.1.206</a></span>
  <span>2 features · July 6–10</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">In-app browser on Desktop</span>
    <span className="digest-feature-pill">Desktop</span>
  </div>

  <p className="digest-feature-lede">Claude Code on desktop now has a built-in browser. Claude can pull up docs, designs, or any other site, and read, click through, and interact with pages the same way it does with your local dev server previews. The browser is sandboxed and configurable: you choose whether browsing sessions persist, and safety classifiers review actions on external sites.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/x358isu_VzLnyTEN/images/whats-new/desktop-browser.mp4?fit=max&auto=format&n=x358isu_VzLnyTEN&q=85&s=8033e85a1cb0a37870a79e702c18f4e4" data-path="images/whats-new/desktop-browser.mp4" />
  </Frame>

  <a className="digest-feature-link" href="/docs/en/desktop#browse-external-sites">Browse external sites</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/doctor is a full setup checkup</span>
    <span className="digest-feature-pill">v2.1.205</span>
  </div>

  <p className="digest-feature-lede"><code>/doctor</code> now diagnoses issues and can fix them, instead of printing a read-only report. It checks installation health, finds unused skills, MCP servers, and plugins versus their context cost, deduplicates local <code>CLAUDE.md</code> files against checked-in ones, proposes trimming <code>CLAUDE.md</code> content Claude could derive from the codebase, and flags slow hooks. It reports findings first and asks for confirmation before changing anything. <code>/checkup</code> is its alias.</p>

  <p className="digest-feature-try">Run a checkup from any session:</p>

  ```text Claude Code theme={null}
  > /doctor
  ```

  <a className="digest-feature-link" href="/docs/en/commands#all-commands">All commands</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div>Auto mode now blocks tampering with session transcript files, and asks before running <code>rm -rf</code> on a variable it can't resolve from context</div>
    <div><code>/cd</code> now suggests directory paths as you type, matching <code>/add-dir</code></div>
    <div><code>/commit-push-pr</code> auto-allows <code>git push</code> to the repo's configured push remote in addition to <code>origin</code></div>
    <div>Gateway: <code>/login</code> now supports Anthropic-operated public gateway endpoints</div>
    <div><code>EnterWorktree</code> asks for confirmation before entering a git worktree outside the project's <code>.claude/worktrees/</code> directory</div>
    <div>Background agents upgrade to a new version in the background right after a Claude Code update, instead of paying a slow stale-session upgrade when you attach</div>
    <div>Agent view rows now show a colored state word and a classifier-written headline instead of raw tool call text, and sessions that edit, merge, comment on, or push to an existing PR link it in <code>claude agents</code></div>
    <div>Auto-update binary downloads now stream to disk instead of buffering in memory, cutting the updater's peak memory usage by roughly 400 MB</div>
    <div>Background task notifications now explicitly state that no human input has occurred, preventing fabricated in-transcript approvals from being acted on</div>
    <div>Improved <code>/code-review</code> findings quality on Opus 4.8 across all effort levels</div>
  </div>
</div>

[Full changelog for v2.1.202–v2.1.206 →](/en/changelog#2-1-202)
