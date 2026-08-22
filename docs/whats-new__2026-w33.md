> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 33 · August 10–14, 2026

> Claude Code Desktop auto-continues after a usage limit resets, fork mode turns on by default, and GitLab merge requests and marketplaces join GitHub.

<div className="digest-meta">
  <span>Releases <a href="/docs/docs/en/changelog#2-1-225">v2.1.225 → v2.1.233</a></span>
  <span>3 features · August 10–14</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Auto-continue after a usage limit on Desktop</span>
    <span className="digest-feature-pill">Desktop</span>
  </div>

  <p className="digest-feature-lede">When you hit your session limit in the Code tab of Claude Code Desktop, the limit card now offers an <strong>Auto-continue when limits reset</strong> checkbox. Check it, and the Desktop app retries the interrupted turn after the reset. The card shows the retry time. The weekly-limit card doesn't offer it.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/desktop-auto-continue.mp4?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=1937f489695feaea715e48ecfd7e62cd" data-path="images/whats-new/desktop-auto-continue.mp4" />
  </Frame>

  <p className="digest-feature-try">The next time a session-limit card appears, check <strong>Auto-continue when limits reset</strong> and leave the session open. The card shows <code>Auto-resuming at</code> followed by the reset time, and the turn picks up on its own once the limit resets.</p>

  <a className="digest-feature-link" href="/docs/docs/en/errors#youve-hit-your-session-limit">What to do when you hit a usage limit</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Fork mode on by default</span>
    <span className="digest-feature-pill">v2.1.232</span>
  </div>

  <p className="digest-feature-lede">Fork mode is now on by default in interactive sessions. Claude can request the <code>fork</code> subagent type, which inherits the full conversation and prompt cache instead of starting fresh, so you don't have to re-explain the context for a side task. Subagents Claude spawns in interactive sessions, apart from the ones an agent-team teammate spawns, also run in the background by default.</p>

  <p className="digest-feature-try">Start a fork yourself with a task that needs everything you've discussed so far:</p>

  ```text Claude Code theme={null}
  > /subtask draft unit tests for the parser changes so far
  ```

  <p className="digest-feature-try">The fork appears in the panel below your prompt and its result arrives in your conversation when it finishes. To turn fork mode off, set <code>CLAUDE\_CODE\_FORK\_SUBAGENT=0</code>.</p>

  <a className="digest-feature-link" href="/docs/docs/en/sub-agents#turn-fork-mode-on-or-off">Turn fork mode on or off</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">GitLab merge requests and marketplaces</span>
    <span className="digest-feature-pill">v2.1.232</span>
  </div>

  <p className="digest-feature-lede">Plugin marketplaces clone bare <code>gitlab.com</code> URLs, including nested subgroups. On v2.1.233 or later, pass a GitLab merge request URL to <code>--worktree</code> to branch from it, and the <code>claude agents</code> view labels sessions linked to a merge request as <code>!N</code>. Claude Code also redacts GitLab token families such as <code>glpat-</code> and <code>glrt-</code>, and protects the <code>glab</code> CLI's config store the same way it protects <code>gh</code>.</p>

  <p className="digest-feature-try">Start a session in a worktree branched from a merge request:</p>

  ```bash terminal theme={null}
  claude --worktree https://gitlab.com/group/project/-/merge_requests/42
  ```

  <p className="digest-feature-try">When <code>origin</code> is on gitlab.com, Claude Code fetches <code>merge-requests/42/head</code> and opens the session on that branch in its own worktree.</p>

  <a className="digest-feature-link" href="/docs/docs/en/worktrees#branch-from-a-pull-request">Branch a worktree from a pull or merge request</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div>Type <code>@</code> in the prompt to <a href="/docs/docs/en/cross-session-messaging#message-another-session">mention another Claude session</a> by name, and Claude messages it directly with <code>SendMessage</code>; a bare name that matches exactly one live session now delivers without a confirmation step</div>
    <div>Interactive sessions on one machine keep <a href="/docs/docs/en/cross-session-messaging#see-which-sessions-claude-can-reach">unique names</a>: if you start or rename a session with a name another live session already uses, Claude Code gives yours a <code>name-word-word</code> variant and tells you</div>
    <div>Plugin marketplaces accept <a href="/docs/docs/en/plugin-marketplaces#command-sources"><code>command</code> sources</a>: a local command prints the plugin directory, which Claude Code re-resolves each session and applies without a restart</div>
    <div>On Linux and WSL, set <a href="/docs/docs/en/tools-reference#memory-limit-on-linux-and-wsl"><code>CLAUDE\_CODE\_TOOL\_MEMORY\_LIMIT</code></a> to a size such as <code>4G</code> to cap the memory Bash and PowerShell tool commands can use</div>
    <div>The task-tracking tools, such as <code>TaskCreate</code>, <code>TaskUpdate</code>, and <code>TodoWrite</code>, are <a href="/docs/docs/en/tools-reference#task-tool-availability">no longer available on Opus 4.8, Sonnet 5, Fable 5, Mythos 5, and later models in those families</a>; set <code>CLAUDE\_CODE\_ENABLE\_TODO\_TOOLS=1</code> to re-enable them</div>
    <div><a href="/docs/docs/en/code-review#review-a-diff-locally"><code>/code-review</code></a> at high, xhigh, and max effort now runs in a background agent like the other levels</div>
    <div><a href="/docs/docs/en/discover-plugins#install-plugins"><code>/plugin install plugin\@marketplace</code></a> refreshes the marketplace first, so newly published plugins install without a manual marketplace update</div>
    <div>Settings accept <a href="/docs/docs/en/settings-reference#marketplace-key-aliases"><code>additionalMarketplaces</code> and <code>allowedMarketplaces</code></a> as aliases for <code>extraKnownMarketplaces</code> and <code>strictKnownMarketplaces</code></div>
    <div>On newer models, Claude can <a href="/docs/docs/en/tools-reference#write-tool-behavior">overwrite an existing file with the Write tool</a> without reading it first this session, matching the Edit tool's rules; older models require the read</div>
    <div>The VS Code extension can <a href="/docs/docs/en/vs-code#organize-sessions-into-groups">organize the sessions list into groups</a>: right-click to create, rename, or delete a group, and Cmd/Ctrl- or Shift-click to move several sessions at once</div>
    <div>If your organization routes Claude Code through a <a href="/docs/docs/en/claude-apps-gateway-spend-limits">Claude apps gateway with spend limits</a>, Claude Code shows the limit period, its reset time, and the operator's message when you reach the limit</div>
  </div>
</div>

[Full changelog for v2.1.225–v2.1.233 →](/docs/en/changelog#2-1-225)
