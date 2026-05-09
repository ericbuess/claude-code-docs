> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 18 · April 27 – May 1, 2026

> Claude Code on Windows runs without Git Bash, claude auth login accepts a pasted OAuth code when the browser callback can't reach localhost, claude project purge cleans up local state per project, and pasting a PR URL into /resume finds the session that created it.

<div className="digest-meta">
  <span>Releases <a href="/docs/en/changelog#2-1-120">v2.1.120 → v2.1.126</a></span>
  <span>4 features · April 27 – May 1</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Sign in without a browser callback</span>
    <span className="digest-feature-pill">v2.1.126</span>
  </div>

  <p className="digest-feature-lede"><code>claude auth login</code> now accepts the OAuth code pasted directly into the terminal when the browser callback can't reach localhost. That covers WSL2, SSH sessions, and containers, where the redirect to a local port doesn't work. The same release also fixes login timeouts on slow or proxied connections and in IPv6-only devcontainers.</p>

  <p className="digest-feature-try">Sign in, then paste the code from the browser:</p>

  ```bash theme={null}
  claude auth login
  ```

  <a className="digest-feature-link" href="/docs/en/cli-reference#cli-commands">CLI reference</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">claude project purge</span>
    <span className="digest-feature-pill">v2.1.126</span>
  </div>

  <p className="digest-feature-lede">Delete all Claude Code state for a project: transcripts, tasks, file history, and the project's config entry. Supports `--dry-run` to preview, `-y`/`--yes` to skip confirmation, `-i`/`--interactive` to choose, and `--all` to clear every project.</p>

  <p className="digest-feature-try">Preview what would be removed:</p>

  ```bash theme={null}
  claude project purge --dry-run
  ```

  <p className="digest-feature-try">Then run it for real:</p>

  ```bash theme={null}
  claude project purge
  ```

  <a className="digest-feature-link" href="/docs/en/cli-reference">CLI reference</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Resume by PR URL</span>
    <span className="digest-feature-pill">v2.1.122</span>
  </div>

  <p className="digest-feature-lede">When you create a pull request with <code>gh pr create</code>, Claude Code links it to the session that produced it. Now you can get back to that session from the PR URL alone, without remembering its name.</p>

  <p className="digest-feature-try">Open the session picker:</p>

  ```text Claude Code theme={null}
  > /resume
  ```

  <p className="digest-feature-try">Paste the PR URL into the picker. The first character of the paste drops you into search mode, and the list filters to the session that created that PR. Press Enter to resume it. GitHub, GitHub Enterprise, GitLab, and Bitbucket pull and merge request URLs all work.</p>

  ```text Claude Code theme={null}
  https://github.com/your-org/your-repo/pull/1234
  ```

  <p className="digest-feature-try">To skip the picker, pass the PR number on the command line instead:</p>

  ```bash theme={null}
  claude --from-pr 1234
  ```

  <a className="digest-feature-link" href="/docs/en/sessions#use-the-session-picker">Sessions: use the session picker</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Windows without Git Bash</span>
    <span className="digest-feature-pill">Windows</span>
  </div>

  <p className="digest-feature-lede">Git for Windows is no longer required. When Bash is absent, Claude Code uses PowerShell as the shell tool, and when the PowerShell tool is enabled it is treated as the primary shell. PowerShell 7 installed via the Microsoft Store, MSI without PATH, or a <code>.NET</code> global tool is now detected automatically.</p>

  <a className="digest-feature-link" href="/docs/en/setup">Setup guide</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div>MCP servers can opt out of tool-search deferral with <code>alwaysLoad: true</code> in their config so all of that server's tools are always available</div>
    <div>New <code>claude plugin prune</code> removes orphaned auto-installed plugin dependencies, and <code>plugin uninstall --prune</code> cascades</div>
    <div><code>/skills</code> now has a type-to-filter search box so you can find a skill in a long list without scrolling</div>
    <div><code>PostToolUse</code> hooks can replace tool output for any tool via <code>hookSpecificOutput.updatedToolOutput</code>, not only MCP tools</div>
    <div>New <a href="/docs/en/ultrareview"><code>claude ultrareview</code></a> subcommand runs <code>/ultrareview</code> non-interactively from CI or scripts: prints findings to stdout (<code>--json</code> for raw output) and exits 0 on completion or 1 on failure</div>
    <div><code>--dangerously-skip-permissions</code> now bypasses prompts for writes to <code>.claude/</code>, <code>.git/</code>, <code>.vscode/</code>, shell config files, and other previously protected paths, while catastrophic removal commands still prompt as a safety net</div>
    <div>The <code>/model</code> picker can list models from your gateway's <code>/v1/models</code> endpoint when <code>ANTHROPIC\_BASE\_URL</code> points at an Anthropic-compatible gateway; opt in with <code>CLAUDE\_CODE\_ENABLE\_GATEWAY\_MODEL\_DISCOVERY=1</code> since v2.1.129</div>
    <div>MCP servers that hit a transient error during startup now auto-retry up to 3 times instead of staying disconnected</div>
    <div><code>ANTHROPIC\_BEDROCK\_SERVICE\_TIER</code> selects a Bedrock service tier: <code>default</code>, <code>flex</code>, or <code>priority</code></div>
    <div><code>/terminal-setup</code> enables iTerm2's clipboard access setting so <code>/copy</code> works, including from tmux</div>
    <div>Vertex AI now supports X.509 certificate-based Workload Identity Federation (mTLS ADC)</div>
    <div>Significant memory leak fixes: image-heavy sessions, <code>/usage</code> on large transcript histories, and long-running tools without progress events</div>
  </div>
</div>

[Full changelog for v2.1.120–v2.1.126 →](/en/changelog#2-1-120)
