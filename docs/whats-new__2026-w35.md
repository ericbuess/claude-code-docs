> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 35 · August 24–28, 2026

> Resume terminal sessions in the Claude Code Desktop app, review feedback reports that Claude drafts for you, and start a session in restricted mode.

Releases [v2.1.240 → v2.1.250](/docs/en/changelog#2-1-240)
3 features · August 24–28

Resume terminal sessions in the Desktop app
Desktop

Type `/resume` in the Claude Code Desktop prompt box to pick up any session you started from the CLI and continue it in the app with the full conversation and context intact. Search your sessions by title, folder, or branch, and preview where you left off before you resume.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/f9HTZGyMtxIFOUgt/images/whats-new/desktop-resume-cli-session.mp4?fit=max&auto=format&n=f9HTZGyMtxIFOUgt&q=85&s=41e4a5fda6b9d63280589f2cbdabf44f" />

In a Desktop session, run the command to list your terminal sessions:

```text Claude Code theme={null}
> /resume
```

Select a session and press `Enter`. The conversation opens in the app where you left off.

[Move between the CLI and Desktop](/docs/en/desktop#coming-from-the-cli)

Claude-drafted feedback
CLI

When a tool keeps failing, Claude can't help with a request, or you point out a mistake, Claude now drafts a feedback report for you with the `SendFeedback` tool. A card above your prompt shows the draft, and you can review, send, or dismiss it from there. Nothing reaches Anthropic until you send it. Requires v2.1.238 or later.

![A Claude Code session where Claude has drafted a bug report titled Sandbox image pull fails behind proxy, shown as a card above the prompt with options to review, send, or dismiss](https://mintcdn.com/claude-code/f9HTZGyMtxIFOUgt/images/whats-new/claude-drafted-feedback.jpg?fit=max\&auto=format\&n=f9HTZGyMtxIFOUgt\&q=85\&s=5cacb3be0dffd1cbd417381f3721637e)

Run `/feedback` with no argument to open your queue of drafts from every session:

```text Claude Code theme={null}
> /feedback
```

Select a draft, then edit, send, or discard it. To turn drafting off, set **Claude-drafted feedback** to `off` in `/config`.

[SendFeedback tool behavior](/docs/en/tools-reference#sendfeedback-tool-behavior)

Restricted mode
v2.1.248

Restricted mode starts Claude Code without the built-in tools that run commands or code. Use it when an evaluation harness drives `claude` on a shared machine. Start it with `--restricted` or set `CLAUDE_CODE_RESTRICTED=1`. Claude Code also removes `WebFetch`, confines the file tools to the working directories, loads only managed settings and `--settings`, and refuses the `bypassPermissions` permission mode.

Run a non-interactive query without the command-running tools:

```bash terminal theme={null}
claude --restricted -p "review src/ for SQL injection risks"
```

To give Claude one of the removed tools back, list it in `--tools` together with the other built-in tools you want, for example `--tools "Bash,Read,Edit"`. `--tools` is an allowlist, and its `default` preset doesn't restore the removed tools.

[CLI flags](/docs/en/cli-reference#cli-flags)

Other wins

Set the new [`modelPicker`](/docs/en/settings-reference#modelpicker) setting to extend or replace the `/model` picker's built-in list with your own ordered, labeled entries, including Amazon Bedrock or Google Cloud's Agent Platform model IDsSet [`promptCacheTtl`](/docs/en/prompt-caching#choose-the-ttl-yourself) to `1h` to keep a one-hour prompt cache on the main conversation when you use an API key or a cloud provider; `subagentPromptCacheTtl` sets the TTL for subagents and all other requests outside the main conversationOn Pro, Max, Team, and Enterprise plans, [`/usage`](/docs/en/costs#plan-usage-breakdown) adds a Loops breakdown: run count, total tokens, tokens per run, and last run for the `/loop` and scheduled tasks that used the most tokensOrganizations on contracted rates can set the [`modelPricing`](/docs/en/costs#report-spend-at-your-contracted-rates) managed setting so `/usage`, the status line, and OpenTelemetry report cost at those rates instead of list price`/login` offers **Sign in with your Console account** under the **Anthropic Console account** option, so members of Console organizations that don't allow API keys can sign in without creating oneRun `/permissions` and open the new [**Auto mode** tab](/docs/en/auto-mode-config#edit-rules-from-permissions) to view and edit auto mode classifier rules without opening a settings fileWhen auto mode is available, Bash permission prompts in the Manual and `acceptEdits` permission modes offer a [**Yes, and switch to auto mode**](/docs/en/permission-modes#switch-permission-modes) option; select it to approve the command and switch the session to auto modeAfter you [move a session with `/cd`](/docs/en/permissions#move-the-session-to-another-directory), the new directory's project settings, hooks, `.mcp.json` servers, skills, and subagents take effect immediately instead of on the next `--resume`In non-interactive sessions, including `-p` runs, Agent SDK runs, and cloud sessions, Claude Code [continues a response](/docs/en/errors#the-response-above-may-be-incomplete) that a server error, dropped connection, or stall cut off mid-stream, when the partial response contains text and no tool callsA subagent that stops at its `maxTurns` limit returns its output marked as partial, with a hint that Claude can [continue it with `SendMessage`](/docs/en/sub-agents#resume-subagents), instead of appearing finishedOn Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, sessions on the same machine can now [message each other](/docs/en/cross-session-messaging#availability), `/loop` can [choose its own interval](/docs/en/scheduled-tasks#let-claude-choose-the-interval), and `/model` and `/effort` apply immediately instead of after the turn endsThe native installer and auto-updater download a zstd-compressed build, about 75 MB instead of 340 MB on Linux x64, and native builds load code on demand, using roughly 40 to 70 MB less memory per session

[Full changelog for v2.1.240–v2.1.250 →](/docs/en/changelog#2-1-240)
