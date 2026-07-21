> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 26 · June 22–26, 2026

> Authenticate MCP servers from your shell with claude mcp login, get a response to shell mode command output with the ! prefix, and resume a conversation from before /clear with /rewind.

<div className="digest-meta">
  <span>Releases <a href="/docs/docs/en/changelog#2-1-185">v2.1.185 → v2.1.193</a></span>
  <span>2 features · June 22–26</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Authenticate MCP servers from the CLI</span>
    <span className="digest-feature-pill">v2.1.186</span>
  </div>

  <p className="digest-feature-lede">New `claude mcp login <name>` and `claude mcp logout <name>` commands authenticate a configured MCP server from your shell instead of the interactive <code>/mcp</code> menu. `claude mcp login` runs the server's OAuth flow directly, and `claude mcp logout` clears the stored credentials.</p>

  <p className="digest-feature-try">Run the OAuth flow for a configured server without opening a session:</p>

  ```bash terminal theme={null}
  claude mcp login sentry
  ```

  <a className="digest-feature-link" href="/docs/docs/en/mcp#authenticate-from-the-command-line">Authenticate from the command line</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Shell mode responds to command output</span>
    <span className="digest-feature-pill">v2.1.186</span>
  </div>

  <p className="digest-feature-lede">Commands you run with the <code>!</code> prefix now get a response from Claude once the output lands in the transcript, so you can run <code>! npm test</code> and get an explanation of the failures without a second prompt. The response costs the same as sending a normal prompt. To keep the earlier behavior, where the output is added to context without a response, set <code>respondToBashCommands</code> to <code>false</code> in <code>settings.json</code>.</p>

  <p className="digest-feature-try">Run a command and get a response to its output:</p>

  ```text Claude Code theme={null}
  > ! npm test
  ```

  <a className="digest-feature-link" href="/docs/docs/en/interactive-mode#shell-mode-with-prefix">Shell mode with the ! prefix</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">Other wins</p>

  <div className="digest-wins-grid">
    <div><code>/rewind</code> can now resume a conversation from before <code>/clear</code> was run</div>
    <div>New <code>sandbox.credentials</code> setting blocks sandboxed commands from reading credential files and secret environment variables</div>
    <div>Org-configured model restrictions now apply to the model picker, `--model`, <code>/model</code>, and <code>ANTHROPIC\_MODEL</code>, with a "restricted by your organization's settings" message when a restricted model is selected</div>
    <div>New <code>autoMode.classifyAllShell</code> setting routes all Bash and PowerShell commands through the auto-mode classifier, and denial reasons now show in the transcript, the denial toast, and <code>/permissions</code></div>
    <div>New <code>claude\_code.assistant\_response</code> OpenTelemetry log event carries the model's response text; deployments that already log prompt content start receiving it on upgrade, so set <code>OTEL\_LOG\_ASSISTANT\_RESPONSES=0</code> to keep prompts only</div>
    <div>Background subagents now surface permission prompts in the main session instead of auto-denying; the dialog shows which agent is asking, and Esc denies only that tool</div>
    <div><code>/install-github-app</code> can now install only the GitHub App and skip the Actions workflow and secret steps</div>
    <div>Hosts you allow in the sandbox network permission dialog are remembered for the rest of the session instead of re-prompting on every connection</div>
    <div>Streaming responses use about 37% less CPU, and long-session memory growth from the terminal output cache is reduced</div>
    <div>`/review <pr>` now uses the same review engine as <code>/code-review medium</code></div>
    <div>Bash mode <code>!</code> commands get live file path autocomplete</div>
  </div>
</div>

[Full changelog for v2.1.185–v2.1.193 →](/docs/en/changelog#2-1-185)
