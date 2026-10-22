> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 26 · June 22–26, 2026

> Authenticate MCP servers from your shell with claude mcp login, get a response to shell mode command output with the ! prefix, and resume a conversation from before /clear with /rewind.

Releases [v2.1.185 → v2.1.193](/docs/en/changelog.md#2-1-185)
2 features · June 22–26

Authenticate MCP servers from the CLI
v2.1.186

New `claude mcp login <name>` and `claude mcp logout <name>` commands authenticate a configured MCP server from your shell instead of the interactive `/mcp` menu. `claude mcp login` runs the server's OAuth flow directly, and `claude mcp logout` clears the stored credentials.

Run the OAuth flow for a configured server without opening a session:

```bash terminal theme={null}
claude mcp login sentry
```

[Authenticate from the command line](/docs/en/mcp.md#authenticate-from-the-command-line)

Shell mode responds to command output
v2.1.186

Commands you run with the `!` prefix now get a response from Claude once the output lands in the transcript, so you can run `! npm test` and get an explanation of the failures without a second prompt. The response costs the same as sending a normal prompt. To keep the earlier behavior, where the output is added to context without a response, set `respondToBashCommands` to `false` in `settings.json`.

Run a command and get a response to its output:

```text Claude Code theme={null}
> ! npm test
```

[Shell mode with the ! prefix](/docs/en/interactive-mode.md#shell-mode-with-prefix)

Other wins

`/rewind` can now resume a conversation from before `/clear` was runNew `sandbox.credentials` setting blocks sandboxed commands from reading credential files and secret environment variablesOrg-configured model restrictions now apply to the model picker, `--model`, `/model`, and `ANTHROPIC_MODEL`, with a "restricted by your organization's settings" message when a restricted model is selectedNew `autoMode.classifyAllShell` setting routes all Bash and PowerShell commands through the auto-mode classifier, and denial reasons now show in the transcript, the denial toast, and `/permissions`New `claude_code.assistant_response` OpenTelemetry log event carries the model's response text; deployments that already log prompt content start receiving it on upgrade, so set `OTEL_LOG_ASSISTANT_RESPONSES=0` to keep prompts onlyBackground subagents now surface permission prompts in the main session instead of auto-denying; the dialog shows which agent is asking, and Esc denies only that tool`/install-github-app` can now install only the GitHub App and skip the Actions workflow and secret stepsHosts you allow in the sandbox network permission dialog are remembered for the rest of the session instead of re-prompting on every connectionStreaming responses use about 37% less CPU, and long-session memory growth from the terminal output cache is reduced`/review <pr>` now uses the same review engine as `/code-review medium`Bash mode `!` commands get live file path autocomplete

[Full changelog for v2.1.185–v2.1.193 →](/docs/en/changelog.md#2-1-185)
