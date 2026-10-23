> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 17 · April 20–24, 2026

> /ultrareview opens as a research preview, automatic session recaps when you return to a terminal, custom color themes you can build and ship in plugins, and a redesigned Claude Code on the web.

Releases [v2.1.114 → v2.1.119](https://code.claude.com/docs/en/changelog.md#2-1-114)
4 features · April 20–24

/ultrareview
research preview

Now in public research preview. Ultrareview runs a fleet of bug-hunting agents in the cloud against your branch or a PR, and findings land back in the CLI or Desktop automatically. Run it before merging critical changes such as auth or data migrations.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/FTi4SBJ9YRs7d-5X/images/whats-new/ultrareview.mp4?fit=max&auto=format&n=FTi4SBJ9YRs7d-5X&q=85&s=0fb1271365d38f414ad155aeb8edb08e" />

Review the branch you're on:

```text Claude Code theme={null}
> /ultrareview
```

Or point it at a PR:

```text Claude Code theme={null}
> /ultrareview 1234
```

[Ultrareview guide](https://code.claude.com/docs/en/ultrareview.md)

Session recap
CLI

Switch focus away from a session and come back to a one-line recap of what happened while you were gone. Helpful for staying in flow while running several Claude sessions at once.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/FTi4SBJ9YRs7d-5X/images/whats-new/session-recap.mp4?fit=max&auto=format&n=FTi4SBJ9YRs7d-5X&q=85&s=0a8db1470bd0161a47efeb2f322af76f" />

Generate a recap on demand, or turn the automatic one off from `/config`:

```text Claude Code theme={null}
> /recap
```

[Interactive mode: session recap](https://code.claude.com/docs/en/interactive-mode.md#session-recap)

Custom themes
v2.1.118

Build and switch between named color themes from `/theme`, or hand-edit JSON files in `~/.claude/themes/`. Each theme picks a base preset and overrides only the tokens you care about. Plugins can ship themes too.

Open the theme picker and create a new one:

```text Claude Code theme={null}
> /theme
```

[Terminal config: create a custom theme](https://code.claude.com/docs/en/terminal-config.md#create-a-custom-theme)

Claude Code on the web
web

A new look for [claude.ai/code](https://claude.ai/code) that matches the redesigned desktop app: sessions sidebar, drag-and-drop layout, and a refreshed routines view. Key parts were rebuilt for quicker responses and a more reliable experience.

![Claude Code on the web redesign overview: new UI, speed and reliability, work across web, mobile, and CLI](https://mintcdn.com/claude-code/FTi4SBJ9YRs7d-5X/images/whats-new/web-redesign.jpeg?fit=max\&auto=format\&n=FTi4SBJ9YRs7d-5X\&q=85\&s=a2aca1b49e295b7337f5779038db8e2c)

[Claude Code on the web](https://code.claude.com/docs/en/claude-code-on-the-web.md)

Other wins

[Vim visual mode](https://code.claude.com/docs/en/interactive-mode.md#vim-editor-mode): press `v` for character selection or `V` for line selection in the prompt input, with operators and visual feedbackHooks can now call MCP tools directly via [`type: "mcp_tool"`](https://code.claude.com/docs/en/hooks#mcp-tool-hook-fields), so a hook can hit an already-connected server without spawning a process`/cost` and `/stats` are merged into [`/usage`](https://code.claude.com/docs/en/commands); the old names still work as typing shortcuts that open the relevant tab`/config` changes (theme, editor mode, verbose, and similar) now persist to `~/.claude/settings.json` and follow the same project/local/policy precedence as other [settings](https://code.claude.com/docs/en/settings.md)[Forked subagents](https://code.claude.com/docs/en/sub-agents.md#fork-the-current-conversation) can be enabled on external builds with `CLAUDE_CODE_FORK_SUBAGENT=1`: a fork inherits your full conversation context instead of starting freshDefault [effort level](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) for Pro and Max subscribers on Opus 4.6 and Sonnet 4.6 is now `high` (was `medium`)Native macOS and Linux builds replace the `Glob` and `Grep` tools with embedded `bfs` and `ugrep` available through Bash, for faster searches without a separate tool round-trip`--from-pr` now accepts GitLab merge request, Bitbucket pull request, and GitHub Enterprise PR URLs in addition to github.comAuto mode: include `"$defaults"` in [`autoMode.allow`, `soft_deny`, or `environment`](https://code.claude.com/docs/en/auto-mode-config) to add custom rules alongside the built-in list instead of replacing itNew [`claude plugin tag`](https://code.claude.com/docs/en/plugins/dependencies#tag-plugin-releases-for-version-resolution) command creates release git tags for plugins with version validationOpus 4.7 sessions now compute against the model's native 1M context window, fixing inflated `/context` percentages and premature autocompaction`/resume` on large sessions is up to 67% faster and now offers to summarize stale, large sessions before re-reading them

[Full changelog for v2.1.114–v2.1.119 →](https://code.claude.com/docs/en/changelog.md#2-1-114)
