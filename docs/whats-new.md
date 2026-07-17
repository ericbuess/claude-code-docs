> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# What's new

> A weekly digest of notable Claude Code features, with code snippets, demos, and context on why they matter.

The weekly dev digest highlights the features most likely to change how you work. Each entry includes runnable code, a short demo, and a link to the full docs. For every bug fix and minor improvement, see the [changelog](/en/changelog).

<Update label="Week 29" description="July 13–17, 2026" tags={["v2.1.207–v2.1.212"]}>
  **Artifacts call your MCP connectors**: a published artifact can pull live data and take actions through each viewer's own MCP connectors when they open the page, and this week also adds public sharing links, editor roles on Team and Enterprise, and artifacts created from Claude Tag sessions.

  Also this week: **screen reader mode** replaces the visual terminal interface with plain, linear text for screen readers such as VoiceOver and NVDA; **`/fork`** copies your conversation into a new background session while you keep working; and **auto mode** no longer needs an opt-in variable on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry.

  [Read the Week 29 digest →](/en/whats-new/2026-w29)
</Update>

<Update label="Week 28" description="July 6–10, 2026" tags={["v2.1.202–v2.1.206"]}>
  **In-app browser on Desktop**: Claude Code on desktop gets a built-in browser, so Claude can pull up docs, designs, or any other site and interact with pages the same way it does with your local dev server previews.

  Also this week: **`/doctor`** is a full setup checkup that diagnoses issues and can fix them, with `/checkup` as its alias; **auto mode** blocks transcript tampering and asks before `rm -rf` on unresolved variables; and **agent view rows** show a colored state word and a classifier-written headline.

  [Read the Week 28 digest →](/en/whats-new/2026-w28)
</Update>

<Update label="Week 27" description="June 29 – July 3, 2026" tags={["v2.1.195–v2.1.201"]}>
  **Claude Sonnet 5**: the new default model for Pro, Team Standard, and Enterprise subscription seats, with top-tier coding and tool use at Sonnet pricing, a native 1M-token context window, and adaptive thinking on by default.

  Also this week: **Claude in Chrome** is generally available on all direct Anthropic plans; **subagents run in the background by default** so Claude keeps working while they run; **Claude Desktop on Linux** lands in beta on Ubuntu and Debian; and **`/radio`** tunes into Claude FM lo-fi radio.

  [Read the Week 27 digest →](/en/whats-new/2026-w27)
</Update>

<Update label="Week 26" description="June 22–26, 2026" tags={["v2.1.185–v2.1.193"]}>
  **`claude mcp login`**: authenticate a configured MCP server from your shell instead of the interactive `/mcp` menu, and clear its stored credentials later with `claude mcp logout`.

  Also this week: **shell mode responds to command output** (`! npm test` gets an explanation without a second prompt); **`/rewind`** can resume a conversation from before `/clear` was run; and **background subagents** now surface permission prompts in the main session instead of auto-denying.

  [Read the Week 26 digest →](/en/whats-new/2026-w26)
</Update>

<Update label="Week 25" description="June 15–19, 2026" tags={["v2.1.178–v2.1.183"]}>
  **Artifacts**: turn a session's output into a live, shareable page on claude.ai that updates in place as the session works, now in beta on Team and Enterprise plans.

  Also this week: **deny and ask rules match tool parameters** with `Tool(param:value)`, for example `Agent(model:opus)`; **`/config key=value`** sets any setting from the prompt, in `-p` mode, and from Remote Control; and **auto mode blocks destructive git commands** when you didn't ask to discard local work.

  [Read the Week 25 digest →](/en/whats-new/2026-w25)
</Update>

<Update label="Week 24" description="June 8–12, 2026" tags={["v2.1.166–v2.1.176"]}>
  **`/cd`**: move the current session to a new working directory mid-conversation without rebuilding the prompt cache.

  Also this week: **sub-agents can spawn their own sub-agents** (background chains are capped at five levels deep); **`--safe-mode`** starts Claude Code with all customizations disabled for troubleshooting; and **`fallbackModel`** configures up to three fallback models tried in order.

  [Read the Week 24 digest →](/en/whats-new/2026-w24)
</Update>

<Update label="Week 23" description="June 1–5, 2026" tags={["v2.1.158–v2.1.165"]}>
  **Auto mode on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry**: auto mode is now available on third-party providers for Opus 4.7 and Opus 4.8, replacing permission prompts with background safety checks.

  Also this week: **safer automatic edits** prompt before writing files that can run code in `acceptEdits` mode; **`/plugin list`** prints your installed plugins inline; and **version requirements** let managed deployments require an approved Claude Code version range.

  [Read the Week 23 digest →](/en/whats-new/2026-w23)
</Update>

<Update label="Week 22" description="May 25–29, 2026" tags={["v2.1.150–v2.1.157"]}>
  **Claude Opus 4.8**: the new default model for Max, Team Premium, Enterprise pay-as-you-go, and Anthropic API accounts, with high effort by default and `/effort xhigh` for the hardest tasks.

  Also this week: **dynamic workflows** orchestrate dozens to hundreds of subagents from a script Claude writes; the **security-guidance plugin** reviews Claude's changes for vulnerabilities as it works; and **fast mode** runs on Opus 4.8 at \$10/\$50 per MTok.

  [Read the Week 22 digest →](/en/whats-new/2026-w22)
</Update>

<Update label="Week 21" description="May 18–22, 2026" tags={["v2.1.143–v2.1.149"]}>
  **Auto mode on the Pro plan**: auto mode now runs on Pro accounts and supports Sonnet 4.6 alongside Opus, replacing permission prompts with background safety checks.

  Also this week: **`/usage`** breaks down what drives your plan limits by skill, subagent, plugin, and MCP server; the new **`/code-review`** command reports correctness bugs; and **background sessions** appear in `/resume` and stay alive when pinned.

  [Read the Week 21 digest →](/en/whats-new/2026-w21)
</Update>

<Update label="Week 20" description="May 11–15, 2026" tags={["v2.1.139–v2.1.142"]}>
  **Agent view**: `claude agents` opens one screen for every Claude Code session, showing what's running, what's blocked on you, and what's done.

  Also this week: **`/goal`** keeps Claude working across turns until a completion condition holds; **fast mode** now runs on Opus 4.7 by default; and the **Rewind menu** can compress earlier context with "Summarize up to here".

  [Read the Week 20 digest →](/en/whats-new/2026-w20)
</Update>

<Update label="Week 19" description="May 4–8, 2026" tags={["v2.1.128–v2.1.136"]}>
  **Plugins load from `.zip` archives and URLs**: `--plugin-dir` now accepts `.zip` files, and `--plugin-url` fetches a plugin archive for the current session.

  Also this week: **`worktree.baseRef`** chooses whether new worktrees branch from the remote default or local `HEAD`; **auto mode hard deny rules** block actions unconditionally regardless of allow exceptions; and **hooks see the active effort level** via `effort.level` and `$CLAUDE_EFFORT`.

  [Read the Week 19 digest →](/en/whats-new/2026-w19)
</Update>

<Update label="Week 18" description="April 27 – May 1, 2026" tags={["v2.1.120–v2.1.126"]}>
  **Windows without Git Bash**: Git for Windows is no longer required, and Claude Code uses PowerShell as the shell tool when Bash is absent.

  Also this week: **`claude ultrareview`** brings cloud code review to CI and scripts; **`claude project purge`** cleans up local state for a project; and pasting a **PR URL into `/resume`** finds the session that created it.

  [Read the Week 18 digest →](/en/whats-new/2026-w18)
</Update>

<Update label="Week 17" description="April 20–24, 2026" tags={["v2.1.114–v2.1.119"]}>
  **`/ultrareview`** opens as a public research preview: a fleet of bug-hunting agents runs in the cloud and findings land back in your CLI or Desktop automatically.

  Also this week: **session recap** shows you what happened while a terminal was unfocused; **custom themes** let you build and ship color palettes from `/theme` or a plugin; and **Claude Code on the web** gets a redesign with a new sessions sidebar and drag-and-drop layout.

  [Read the Week 17 digest →](/en/whats-new/2026-w17)
</Update>

<Update label="Week 16" description="April 13–17, 2026" tags={["v2.1.105–v2.1.113"]}>
  **Claude Opus 4.7** lands as the new default on Max and Team Premium, with a new `xhigh` effort level that's the recommended setting for most coding work and an interactive `/effort` slider to dial it in.

  Also this week: **Routines** on Claude Code on the web fire templated cloud agents from a schedule, GitHub event, or API call; **mobile push notifications** ping your phone when a long task finishes or Claude needs you; `/usage` shows what's driving your limits; and the CLI moves to native binaries.

  [Read the Week 16 digest →](/en/whats-new/2026-w16)
</Update>

<Update label="Week 15" description="April 6–10, 2026" tags={["v2.1.92–v2.1.101"]}>
  **Ultraplan** enters early preview: draft a plan in the cloud from your CLI, review and comment on it in a web editor, then run it remotely or pull it back local. The first run now auto-creates a cloud environment for you.

  Also this week: the **Monitor** tool streams background events into the conversation so Claude can tail logs and react live, `/loop` self-paces when you omit the interval, `/team-onboarding` packages your setup into a replayable guide, and `/autofix-pr` turns on PR auto-fix from your terminal.

  [Read the Week 15 digest →](/en/whats-new/2026-w15)
</Update>

<Update label="Week 14" description="March 30 – April 3, 2026" tags={["v2.1.86–v2.1.91"]}>
  **Computer use** comes to the CLI in research preview: Claude can open native apps, click through UI, and verify changes from your terminal. Best for closing the loop on things only a GUI can verify.

  Also this week: `/powerup` interactive lessons, flicker-free alt-screen rendering, a per-tool MCP result-size override up to 500K, and plugin executables on the Bash tool's `PATH`.

  [Read the Week 14 digest →](/en/whats-new/2026-w14)
</Update>

<Update label="Week 13" description="March 23–27, 2026" tags={["v2.1.83–v2.1.85"]}>
  **Auto mode** lands in research preview: a classifier handles your permission prompts so safe actions run without interruption and risky ones get blocked. The middle ground between approving everything and `--dangerously-skip-permissions`.

  Also this week: computer use in the Desktop app, PR auto-fix on Web, transcript search with `/`, a native PowerShell tool for Windows, and conditional `if` hooks.

  [Read the Week 13 digest →](/en/whats-new/2026-w13)
</Update>
