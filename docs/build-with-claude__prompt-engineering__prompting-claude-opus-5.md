---
title: Prompting Claude Opus 5
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
description: Behavioral differences and prompting patterns for Claude Opus 5, covering response verbosity, agentic narration, task scoping, subagent delegation, self-correction, and output artifacts when thinking is disabled.
---

This guide covers the prompting patterns specific to Claude Opus 5. For the model's capabilities and API changes, see [What's new in Claude Opus 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5). For techniques that apply across all current Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Opus 5 is built for complex agentic coding and enterprise work, with particular strengths in long-horizon agentic tasks. It performs well out of the box on existing Claude Opus 4.8 prompts. The following patterns cover the behaviors that most often require tuning.

<Note>
  For API changes when migrating from Claude Opus 4.8 (thinking on by default, and disabling thinking capped at `high` effort), see the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5).
</Note>

## Capability improvements

Compared with Claude Opus 4.8, the improvements most relevant to prompting are:

* **Agentic coding:** Claude Opus 5 is strongest on difficult coding tasks: multi-file features, larger refactors, and end-to-end feature work. It completes full tasks rather than leaving stubs or placeholders, and it performs best when given the complete task specification up front and left to run. It also performs well on easier tasks like single-turn edits, where the difference from prior models is smaller.
* **Code review and bug-finding:** Claude Opus 5 reviews code with high precision and recall: it finds real bugs at a high rate per pass, and its additional findings are mostly real issues rather than false positives. Accuracy holds at lower effort settings, which supports a fast pass at review time and a more thorough pass later. If your review prompt says "only report high-severity issues" or "be conservative," the model may follow that instruction literally and report less; ask it to report everything and filter in a separate pass instead.
* **Efficiency at lower effort:** `low` and `medium` [effort](https://platform.claude.com/docs/en/build-with-claude/effort) produce strong quality at a fraction of the tokens and latency of higher settings. Start with the default (`high`) and adjust based on your evals: use `low` and `medium` liberally as your primary control for token cost and response time wherever quality holds, and step up to `xhigh` for demanding coding and agentic work. If you carried effort defaults over from a prior model, re-run an effort sweep on your own evals. See [Effort](https://platform.claude.com/docs/en/build-with-claude/effort#recommended-effort-levels-for-claude-opus-5) for the full recommendations.
* **Vision:** Claude Opus 5 is strong on chart, document, and diagram understanding, and on UI and frontend visual replication. Re-validate any prompt-side vision workarounds you tuned for prior models; they may no longer be needed. Vision performance is strongest when the model has tools to iteratively analyze, crop, and visually verify its work, and tool use is a more cost-effective lever than thinking alone.
* **Long-context work:** Claude Opus 5 has a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) as both the default and the maximum, and its instruction following, tool calling, and reasoning stay consistent throughout the window.
* **Office and document tasks:** Claude Opus 5 generates and works with complex, multi-sheet spreadsheets with non-trivial formulas, and it produces well-structured slide decks. Prompt it with any specific styles or templates it needs to follow.
* **Multi-agent coordination:** Claude Opus 5 coordinates teams of subagents well, with effective writer-verifier patterns and few cases of agents overwriting each other's work. For cost-sensitive workloads, cap delegation; see [Controlling subagent spawning](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#controlling-subagent-spawning).

## Response length and verbosity

Claude Opus 5's default user-facing responses run longer than prior Opus models'. The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) controls how much the model [thinks](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost) rather than how much it says: lowering effort can reduce thinking volume without reliably shortening the visible response. To control response length, prompt for it explicitly.

A short conciseness instruction is effective. For example, for a user-facing multi-turn product:

```text wrap
Keep responses focused, brief, and concise. Keep disclaimers and caveats short, and spend most of the response on the main answer. When asked to explain something, give a high-level summary unless an in-depth explanation is specifically requested.
```

In a long system prompt, pair the instruction with a short reminder near the end of the prompt:

```text wrap
<tone_preference>
Keep outputs reasonably concise.
</tone_preference>
```

## User-facing progress updates

Claude Opus 5 narrates readily during agentic work: it tends to announce what it is about to do, and its per-message output in agentic sessions is often longer than prior models'. It benefits from explicit guidance on how to communicate with the user during a task. To tune narration down, describe the cadence and shape you want:

```text wrap
Before your first tool call, say in one sentence what you're about to do. While working, give a brief update only when you find something important or change direction. When you finish, lead with the outcome: your first sentence should answer "what happened" or "what did you find," with supporting detail after it for readers who want it.
```

To tune narration up, or change its style, the same lever applies in the other direction: explicitly describe what updates should look like and provide examples. Positive examples of the communication style you want tend to be more effective than instructions about what not to do.

## Written deliverable length

Separate from conversational verbosity, files that Claude Opus 5 writes to disk (reports, Markdown documents, summaries) are often longer than on prior models. If your product includes Claude-authored documents, add explicit length calibration:

```text wrap
Match the length of written documents to what the task needs: cover the substance, but do not pad with filler sections, redundant summaries, or boilerplate.
```

## Task scope and over-verification

Claude Opus 5 verifies its own work without being told to. If your prompt contains explicit verification instructions ("include a final verification step for any non-trivial task," "use a subagent to verify"), remove them: instructions like these cause over-verification on Claude Opus 5, and removing them reduces wasted tokens with no loss in quality. The same applies to legacy harness scaffolding that adds separate verification steps.

Claude Opus 5 can also expand the scope of a task, adding steps that weren't requested or applying its own judgment about what the task should be. For narrow tasks, constrain scope explicitly:

```text wrap
Deliver what was asked, at the scope intended. Make routine judgment calls yourself, and check in only when different readings of the request would lead to materially different work. If the request seems mistaken or a better approach exists, say so in a sentence and continue with the task as asked rather than quietly narrowing, widening, or transforming it. Finish the whole task, and stop short of actions that are clearly beyond what was asked.
```

## Controlling subagent spawning

Claude Opus 5 delegates to subagents more readily than prior models. Delegation pays off on genuinely independent, sizeable tracks of work, but it multiplies cost and time when applied to small tasks. If your harness supports subagents, give explicit guidance on which scenarios warrant delegation, or set deterministic caps on how many agents can be launched. For example:

```text wrap
Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low.
```

If your harness is Claude Code or the Claude Agent SDK, the deterministic caps are the `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH` and `CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS` environment variables and the SDK's `max_budget_usd` option. They require Claude Code 2.1.217 or later, so update a pinned SDK before pointing it at Claude Opus 5. Claude Code adds a delegation instruction of its own on Claude Opus 5 only when you use its `claude_code` system prompt preset; with a custom or omitted system prompt, add a delegation instruction such as the example in this section yourself. See [Cap subagent depth, concurrency, and spend](https://code.claude.com/docs/en/agent-sdk/subagents#cap-subagent-depth-concurrency-and-spend) in the Agent SDK docs.

## Self-correction

Claude Opus 5 catches and fixes its own mistakes well without prompting. Avoid instructing re-checks it already performs ("double-check your answer," "re-verify before responding"); like verification instructions, these compound with the model's own behavior and add cost without improving results.

The model also narrates corrections to its earlier statements more than prior models do, which can be undesirable in user-facing products. To limit correction narration to corrections that matter:

```text wrap
Only correct an earlier statement when the error would change the user's code, conclusions, or decisions. State corrections plainly and briefly, then continue the task. For slips that change nothing for the user, make the fix and move on without noting it.
```

## Running with thinking disabled

Claude Opus 5 runs with [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) on by default, and thinking can be disabled only at [effort](https://platform.claude.com/docs/en/build-with-claude/effort) `high` or below; see the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5). With thinking disabled, two artifacts can occasionally appear in the model's visible output. The primary mitigation for both is to keep thinking enabled and control token cost with lower effort levels instead of disabling thinking: for most tasks, thinking enabled at `low` effort performs better than thinking disabled at similar cost.

**Tool calls as text.** With thinking disabled, the model occasionally writes a tool call into its user-facing text instead of emitting a structured `tool_use` block. The turn completes normally and the call never runs, and in agentic loops the leaked text stays in the conversation history, so later turns are affected as well. This is most common on tool-heavy workloads such as search.

**Internal XML tags in output.** With thinking disabled, the model can emit `<thinking>` tags or other internal XML tags into its visible response. If your system prompt contains a rule instructing the model not to think or not to reason, remove it; that kind of instruction increases tag leakage.

For integrations that must keep thinking disabled, a single combined instruction mitigates both artifacts: it gives the model explicit permission to speak before a tool call, an alternative to forcing a call when no tool fits, and a general rule against internal tags:

```text wrap
When you use a tool, you may say a brief sentence first. If no tool can express what the user asked for, say so instead of guessing. Do not include internal or system XML tags in your response.
```

Instructions that call out thinking tags by name are less effective than the general form, so avoid naming them specifically.
