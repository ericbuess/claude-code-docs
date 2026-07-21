> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 25 · June 15–19, 2026

> Publish a live, shareable page from your session with Artifacts, match tool parameters in deny and ask rules, and set any setting from the prompt with /config.

<div className="digest-meta">
  <span>Releases <a href="/docs/docs/en/changelog#2-1-178">v2.1.178 → v2.1.183</a></span>
  <span>3 features · June 15–19</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Artifacts</span>
  </div>

  <p className="digest-feature-lede">An artifact is a live, interactive page that Claude Code publishes from your session to a private URL on claude.ai, and it updates in place as the session keeps working. Ask for one when terminal text is the wrong medium, such as a PR walkthrough with the diff annotated inline or a dashboard built from session data. Artifacts are in beta on Team and Enterprise plans.</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/1ylKDoQynT1UgfEK/images/whats-new/artifacts.mp4?fit=max&auto=format&n=1ylKDoQynT1UgfEK&q=85&s=7f5391559d2bc69989621b36322fcff1" data-path="images/whats-new/artifacts.mp4" />
  </Frame>

  <p className="digest-feature-try">Ask Claude for a page, then approve the publish prompt:</p>

  ```text Claude Code theme={null}
  > Make an artifact that walks through this PR with the diff annotated inline.
  ```

  <a className="digest-feature-link" href="/docs/docs/en/artifacts#create-an-artifact">Create an artifact</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Match by input parameter</span>
    <span className="digest-feature-pill">v2.1.178</span>
  </div>

  <p className="digest-feature-lede">Deny and ask permission rules can now match a tool's input parameters with the <code>Tool(param:value)</code> syntax. For example, <code>Agent(model:opus)</code> matches subagent spawns that request the Opus model tier. The value accepts `*` as a wildcard, so `Agent(isolation:*)` matches any explicit isolation value.</p>

  <p className="digest-feature-try">Add a parameter rule to the deny list in <code>settings.json</code>:</p>

  ```json .claude/settings.json {3} theme={null}
  {
    "permissions": {
      "deny": ["Agent(model:opus)"]
    }
  }
  ```

  <a className="digest-feature-link" href="/docs/docs/en/permissions#match-by-input-parameter">Match by input parameter</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Set any setting from the prompt</span>
    <span className="digest-feature-pill">v2.1.181</span>
  </div>

  <p className="digest-feature-lede">Pass <code>key=value</code> to <code>/config</code> to change a setting directly without opening the Settings interface. The syntax also works in non-interactive mode with the <code>-p</code> flag and from Remote Control.</p>

  <p className="digest-feature-try">Set the <code>thinking</code> setting from the prompt:</p>

  ```text Claude Code theme={null}
  > /config thinking=false
  ```

  <a className="digest-feature-link" href="/docs/docs/en/commands#all-commands">Commands reference</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div>Auto mode now blocks destructive git commands (`git reset --hard`, `git clean -fd`, `git stash drop`) when you didn't ask to discard local work, and blocks <code>terraform destroy</code> unless you asked for the specific stack</div>
    <div>Set the new <code>attribution.sessionUrl</code> setting to <code>false</code> to omit the claude.ai session link from commits and PRs in web and Remote Control sessions</div>
    <div>In the <code>/config</code> interface, Enter and Space both change the selected setting, and Esc now saves and closes instead of reverting</div>
    <div>New <code>sandbox.allowAppleEvents</code> opt-in setting lets sandboxed commands send Apple Events on macOS</div>
    <div>Point <code>CLAUDE\_CLIENT\_PRESENCE\_FILE</code> at a marker file to suppress mobile push notifications while you're at the machine</div>
    <div>Long paragraphs now stream line by line instead of waiting for the first line break</div>
    <div>API connection drops mid-thinking now retry automatically instead of showing "Connection closed while thinking"</div>
    <div>With <code>CLAUDE\_CODE\_EXPERIMENTAL\_AGENT\_TEAMS=1</code> set, every session has one implicit team, so you spawn teammates directly with the Agent tool's <code>name</code> parameter</div>
    <div>Skills in nested <code>.claude/skills</code> directories load when working on files there; on a name clash the nested skill appears as `<dir>:<name>` so both stay available</div>
    <div>Fixed prompt caching not reading on a custom <code>ANTHROPIC\_BASE\_URL</code> and on Microsoft Foundry</div>
    <div>Fixed Write and Edit producing zero-byte or truncated files on network drives and cloud-synced folders</div>
  </div>
</div>

[Full changelog for v2.1.178–v2.1.183 →](/docs/en/changelog#2-1-178)
