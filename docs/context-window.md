> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Explore the context window

> An interactive simulation of how Claude Code's context window fills during a session. See what loads automatically, what each file read costs, and when rules and hooks fire.

Claude Code's context window holds everything Claude knows about your session: your instructions, the files it reads, its own responses, and content that never appears in your terminal. The timeline below plays a full session from startup to compaction: what loads before you type, what each file read, rule, and hook adds as Claude works, and how a subagent keeps large reads out of your context. See [the written breakdown](#what-the-timeline-shows) for the same content as a list.

## What the timeline shows

The session walks through a realistic flow with representative token counts:

* **Before you type anything**: CLAUDE.md, auto memory, MCP tool names, and skill descriptions all load into context. [AGENTS.md files](https://code.claude.com/docs/en/memory.md#agents-md) can load in place of CLAUDE.md. Your own setup may add more here, like an [output style](https://code.claude.com/docs/en/output-styles.md) or text from [`--append-system-prompt`](https://code.claude.com/docs/en/cli-reference).
* **As Claude works**: each file read adds to context, [path-scoped rules](https://code.claude.com/docs/en/memory.md#path-specific-rules) load automatically alongside matching files, and a [PostToolUse hook](https://code.claude.com/docs/en/hooks-guide.md) fires after each edit.
* **The follow-up prompt**: a [subagent](https://code.claude.com/docs/en/sub-agents.md) handles the research in its own separate context window, so the large file reads stay out of yours. Only the summary and a small metadata trailer come back.
* **At the end of the walkthrough**: you run `/compact`, which replaces the conversation with a structured summary. Most startup content reloads automatically; the table below shows what happens to each mechanism.

## What survives compaction

When a long session compacts, Claude Code summarizes the conversation history to fit the context window. As of v2.1.198, the summarization request inherits your session's [extended thinking](https://code.claude.com/docs/en/model-config.md#extended-thinking) configuration, so it reasons with thinking enabled when your session has it enabled and stays off otherwise. Thinking affects only how the summary is produced; your session settings are unchanged afterward. What happens to each kind of content depends on how it was loaded:

| Mechanism | After compaction |
| :- | :- |
| System prompt and output style | Both still apply |
| Project-root CLAUDE.md and unscoped rules | Re-injected from disk |
| Auto memory | Re-injected from disk |
| Skill descriptions | Rebuilt from your current [skills](https://code.claude.com/docs/en/skills.md) and re-injected. Requires Claude Code v2.1.304 or later |
| [Git status snapshot](https://code.claude.com/docs/en/settings-reference.md#includegitinstructions) | If the session started with one, Claude Code reads a fresh one from your repository |
| The plan Claude wrote in [plan mode](https://code.claude.com/docs/en/permission-modes.md#analyze-before-you-edit-with-plan-mode) | Re-injected from disk |
| Rules with `paths:` frontmatter | Claude Code reloads them [on demand](https://code.claude.com/docs/en/memory.md#path-specific-rules) |
| Nested CLAUDE.md in subdirectories | Claude Code reloads them [on demand](https://code.claude.com/docs/en/memory.md#how-claude-md-files-load) |
| Files Claude read or edited | Claude Code re-reads up to five, most recently modified first |
| Invoked skill bodies | Re-injected, capped at 5,000 tokens per skill and 25,000 tokens total; oldest dropped first |
| [Background commands](https://code.claude.com/docs/en/interactive-mode.md#background-bash-commands) and background [subagents](https://code.claude.com/docs/en/sub-agents.md#run-subagents-in-foreground-or-background) | Keep running. Claude Code reminds Claude which ones are still running so it doesn't start a duplicate |
| Context that hooks added earlier | Summarized with the rest of the conversation |
| [SessionStart hooks](https://code.claude.com/docs/en/hooks-guide.md#re-inject-context-after-compaction) that match the `compact` source | Claude Code runs them and adds their output to the compacted context |

Right after compaction, Claude Code re-reads up to five of the files Claude has read or edited in the session, choosing the ones modified most recently. A file over 5,000 tokens comes back as a path reference without its content, shown as `Referenced file` instead of `Read`.

Path-scoped rules and nested CLAUDE.md files load into message history when Claude reads, writes, or edits their trigger file, so compaction summarizes them away with everything else. If a rule must persist across compaction, drop the `paths:` frontmatter or move it to the project-root CLAUDE.md.

Skill bodies are re-injected after compaction, but large skills are truncated to fit the per-skill cap, and the oldest invoked skills are dropped once the total budget is exceeded. Truncation keeps the start of the file, so put the most important instructions near the top of `SKILL.md`.

## When your context fills up

Claude Code compacts automatically as you approach the limit, so a full context window doesn't end your session. The automatic pass works the same way as the `/compact` step in the timeline. See [When context fills up](https://code.claude.com/docs/en/how-claude-code-works.md#when-context-fills-up) for what it preserves. For when Claude Code also compacts a conversation you leave idle, see [idle compaction](https://code.claude.com/docs/en/settings-reference.md#idlecompaction).

You can also act before the automatic pass runs:

* **Compact with a focus**: run `/compact` with instructions, like `/compact focus on the auth bug fix`, before starting a long new task. The summary keeps what you choose instead of what the automatic pass guesses is important.
* **Compact part of the conversation**: run `/rewind`, select a message, and choose **Summarize from here** or **Summarize up to here**. See [Rewind and summarize](https://code.claude.com/docs/en/checkpointing.md#rewind-and-summarize) for what each option keeps and how to guide the summary.
* **Compact earlier**: run [`/autocompact`](https://code.claude.com/docs/en/commands#all-commands) with a token count, like `/autocompact 500k`, to set how full the context window gets before the automatic pass runs. See [Set the auto-compact window](https://code.claude.com/docs/en/model-config.md#set-the-auto-compact-window) for accepted values and overrides.
* **Clear between tasks**: run `/clear` when switching to unrelated work. Old conversation crowds out the files you need next and costs tokens on every message.
* **Delegate large reads**: send research to a [subagent](https://code.claude.com/docs/en/sub-agents.md) so the file contents stay in its context window, not yours.

If you need a larger window rather than a smaller conversation, Fable models, Sonnet 5 and later, Haiku 5.5, Opus 4.6 and later, and Sonnet 4.6 support a 1 million token context window. See [Extended context](https://code.claude.com/docs/en/model-config.md#extended-context) for availability by plan and how to select a `[1m]` model variant. Compaction works the same way at the larger limit.

The point where automatic compaction runs depends on your model and configuration. See [Default auto-compact thresholds](https://code.claude.com/docs/en/model-config.md#default-auto-compact-thresholds) for the boundaries per model, and [Correct the window for a gateway or custom model ID](https://code.claude.com/docs/en/model-config.md#correct-the-window-for-a-gateway-or-custom-model-id) if Claude Code assumes the wrong window for your model ID, such as an [LLM gateway](https://code.claude.com/docs/en/llm-gateway) alias.

## Check your own session

The visualization uses representative numbers. To see your actual context usage at any point, run `/context` for a live breakdown by category with optimization suggestions, including which CLAUDE.md and auto memory files loaded. Run `/memory` to open and edit those files.

## Related resources

For deeper coverage of the features shown in the timeline, see these pages:

* [Extend Claude Code](https://code.claude.com/docs/en/features-overview.md): when to use CLAUDE.md vs skills vs rules vs hooks vs MCP
* [Store instructions and memories](https://code.claude.com/docs/en/memory.md): CLAUDE.md hierarchy and auto memory
* [Subagents](https://code.claude.com/docs/en/sub-agents.md): delegate research to a separate context window
* [Best practices](https://code.claude.com/docs/en/best-practices.md#keep-cost-and-context-down): keep sessions focused and costs down
* [Prompt caching](https://code.claude.com/docs/en/prompt-caching.md): which actions invalidate the cached prefix
* [Reduce token usage](https://code.claude.com/docs/en/costs.md#reduce-token-usage): strategies for keeping context usage low
