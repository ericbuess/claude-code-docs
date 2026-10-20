> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 18 · April 27 – May 1, 2026

> Claude Code on Windows runs without Git Bash, claude auth login accepts a pasted OAuth code when the browser callback can't reach localhost, claude project purge cleans up local state per project, and pasting a PR URL into /resume finds the session that created it.

Releases [v2.1.120 → v2.1.126](/docs/en/changelog#2-1-120)
4 features · April 27 – May 1

Sign in without a browser callback
v2.1.126

`claude auth login` now accepts the OAuth code pasted directly into the terminal when the browser callback can't reach localhost. That covers WSL2, SSH sessions, and containers, where the redirect to a local port doesn't work. The same release also fixes login timeouts on slow or proxied connections and in IPv6-only devcontainers.

Sign in, then paste the code from the browser:

```bash theme={null}
claude auth login
```

[CLI reference](/docs/en/cli-reference#cli-commands)

claude project purge
v2.1.124

Delete all Claude Code state for a project: transcripts, tasks, file history, and the project's config entry. Supports `--dry-run` to preview, `-y`/`--yes` to skip confirmation, `-i`/`--interactive` to choose, and `--all` to clear every project.

Preview what would be removed:

```bash theme={null}
claude project purge --dry-run
```

Then run it for real:

```bash theme={null}
claude project purge
```

[CLI reference](/docs/en/cli-reference)

Resume by PR URL
v2.1.122

When you create a pull request with `gh pr create`, Claude Code links it to the session that produced it. Now you can get back to that session from the PR URL alone, without remembering its name.

Open the session picker:

```text Claude Code theme={null}
> /resume
```

Paste the PR URL into the picker. The first character of the paste drops you into search mode, and the list filters to the session that created that PR. Press Enter to resume it. GitHub, GitHub Enterprise, GitLab, and Bitbucket pull and merge request URLs all work.

```text Claude Code theme={null}
https://github.com/your-org/your-repo/pull/1234
```

To open the picker already filtered to the PR, pass the PR number on the command line:

```bash theme={null}
claude --from-pr 1234
```

[Sessions: use the session picker](/docs/en/sessions#use-the-session-picker)

Windows without Git Bash
Windows

Git for Windows is no longer required. When Bash is absent, Claude Code uses PowerShell as the shell tool, and when the PowerShell tool is enabled it is treated as the primary shell. PowerShell 7 installed via the Microsoft Store, MSI without PATH, or a `.NET` global tool is now detected automatically.

[Setup guide](/docs/en/setup)

Other wins

MCP servers can opt out of tool-search deferral with `alwaysLoad: true` in their config so all of that server's tools are always availableNew `claude plugin prune` removes orphaned auto-installed plugin dependencies, and `plugin uninstall --prune` cascades`/skills` now has a type-to-filter search box so you can find a skill in a long list without scrolling`PostToolUse` hooks can replace tool output for any tool via `hookSpecificOutput.updatedToolOutput`, not only MCP toolsNew [`claude ultrareview`](/docs/en/ultrareview) subcommand runs `/ultrareview` non-interactively from CI or scripts: prints findings to stdout (`--json` for raw output) and exits 0 on completion or 1 on failure`--dangerously-skip-permissions` now bypasses prompts for writes to `.claude/`, `.git/`, `.vscode/`, shell config files, and other previously protected paths, while catastrophic removal commands still prompt as a safety netThe `/model` picker can list models from your gateway's `/v1/models` endpoint when `ANTHROPIC_BASE_URL` points at an Anthropic-compatible gateway; opt in with `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` since v2.1.129MCP servers that hit a transient error during startup now auto-retry up to 3 times instead of staying disconnected`ANTHROPIC_BEDROCK_SERVICE_TIER` selects an Amazon Bedrock service tier: `default`, `flex`, or `priority``/terminal-setup` enables iTerm2's clipboard access setting so `/copy` works, including from tmuxGoogle Cloud's Agent Platform now supports X.509 certificate-based Workload Identity Federation (mTLS ADC)Significant memory leak fixes: image-heavy sessions, `/usage` on large transcript histories, and long-running tools without progress events

[Full changelog for v2.1.120–v2.1.126 →](/docs/en/changelog#2-1-120)
