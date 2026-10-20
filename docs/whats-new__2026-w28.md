> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 28 · July 6–10, 2026

> Browse external sites from the Desktop app's built-in browser, run a full setup checkup with /doctor, and pick up auto mode transcript protections and agent view upgrades.

Releases [v2.1.202 → v2.1.206](/docs/en/changelog#2-1-202)
2 features · July 6–10

In-app browser on Desktop
Desktop

Claude Code on desktop now has a built-in browser. Claude can pull up docs, designs, or any other site, and read, click through, and interact with pages the same way it does with your local dev server previews. The browser is sandboxed and configurable: you choose whether browsing sessions persist, and safety classifiers review actions on external sites.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/x358isu_VzLnyTEN/images/whats-new/desktop-browser.mp4?fit=max&auto=format&n=x358isu_VzLnyTEN&q=85&s=8033e85a1cb0a37870a79e702c18f4e4" />

[Browse external sites](/docs/en/desktop#browse-external-sites)

/doctor is a full setup checkup
v2.1.205

`/doctor` now diagnoses issues and can fix them, instead of printing a read-only report. It checks installation health, finds unused skills, MCP servers, and plugins versus their context cost, deduplicates local `CLAUDE.md` files against checked-in ones, proposes trimming `CLAUDE.md` content Claude could derive from the codebase, and flags slow hooks. It reports findings first and asks for confirmation before changing anything. `/checkup` is its alias.

Run a checkup from any session:

```text Claude Code theme={null}
> /doctor
```

[All commands](/docs/en/commands#all-commands)

Other wins

Auto mode now blocks tampering with session transcript files, and asks before running `rm -rf` on a variable it can't resolve from context`/cd` now suggests directory paths as you type, matching `/add-dir``/commit-push-pr` auto-allows `git push` to the repo's configured push remote in addition to `origin`Gateway: `/login` now supports Anthropic-operated public gateway endpoints`EnterWorktree` asks for confirmation before entering a git worktree outside the project's `.claude/worktrees/` directoryBackground agents upgrade to a new version in the background right after a Claude Code update, instead of paying a slow stale-session upgrade when you attachAgent view rows now show a colored state word and a classifier-written headline instead of raw tool call text, and sessions that edit, merge, comment on, or push to an existing PR link it in `claude agents`Auto-update binary downloads now stream to disk instead of buffering in memory, cutting the updater's peak memory usage by roughly 400 MBBackground task notifications now explicitly state that no human input has occurred, preventing fabricated in-transcript approvals from being acted onImproved `/code-review` findings quality on Opus 4.8 across all effort levels

[Full changelog for v2.1.202–v2.1.206 →](/docs/en/changelog#2-1-202)
