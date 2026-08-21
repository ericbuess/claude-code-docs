---
title: Prompting Claude Sonnet 5
url: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5
description: Behavioral differences and prompting patterns for Claude Sonnet 5, covering effort, adaptive thinking defaults, tool use, and migration from Claude Sonnet 4.6.
---

This guide covers the prompting patterns specific to Claude Sonnet 5. For the model's capabilities and API changes, see [What's new in Claude Sonnet 5](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5). For techniques that apply across all current Claude models, see [Prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

Claude Sonnet 5 has particular strengths in coding and agentic tasks. It performs well out of the box on existing Claude Sonnet 4.6 prompts. The patterns in this guide cover the behaviors that most often require tuning.

<Note>
  For API parameter changes when migrating from Claude Sonnet 4.6 (adaptive thinking on by default, sampling parameters not accepted, manual extended thinking removed, and the new tokenizer), see the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5).
</Note>

## Response length and verbosity

Claude Sonnet 5 calibrates response length to the complexity of the task rather than defaulting to a fixed verbosity. This usually means shorter answers on simple lookups and longer ones on open-ended analysis.

If your product depends on a certain style or verbosity of output, you may need to tune your prompts. As an example, to decrease verbosity, you might add:

```text wrap
Provide concise, focused responses. Skip non-essential context, and keep examples minimal.
```

If you see specific kinds of verbosity (such as over-explaining), you can add additional instructions in your prompt to prevent them. Positive examples showing how Claude can communicate with the appropriate level of concision tend to be more effective than negative examples or instructions that tell the model what not to do.

## Calibrating effort and thinking depth

The [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) allows you to tune Claude's intelligence versus token spend, trading off capability for faster speed and lower costs. On Claude Sonnet 5, effort defaults to `high`, the same as on Claude Sonnet 4.6. For the hardest coding and agentic tasks, raise effort to `xhigh`. Experiment with other effort levels to further tune token usage and intelligence:

* **`max`:** Absolute maximum capability with no constraints on token spending.
* **`xhigh`:** Extra high effort is the recommended setting for the hardest coding and agentic use cases.
* **`high`:** The default. This setting balances token usage and intelligence for most use cases.
* **`medium`:** Good for cost-sensitive use cases that need to reduce token usage while trading off intelligence.
* **`low`:** Reserve for short, scoped tasks and latency-sensitive workloads that are not intelligence-sensitive.

As a rough cross-model mapping when migrating: Claude Sonnet 5 at medium is comparable in intelligence to Claude Sonnet 4.6 at high, and Claude Sonnet 5 at high is comparable to Claude Sonnet 4.6 at max. When benchmarking, match by observed thinking length rather than effort name.

Claude Sonnet 5 respects effort levels strictly, especially at the low end. At `low` and `medium`, the model scopes its work to what was asked rather than going above and beyond. This is good for latency and cost, but on moderately complex tasks running at `low` effort there is some risk of under-thinking.

If you observe shallow reasoning on complex problems, raise effort to `high` or `xhigh` rather than prompting around it. If you need to keep effort at `low` for latency, add targeted guidance:

```text wrap
This task involves multistep reasoning. Think carefully through the problem before responding.
```

On Claude Sonnet 5, [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) is on by default. Requests without a `thinking` field run with adaptive thinking. This is a change from Claude Sonnet 4.6, where the same requests ran without thinking. To turn thinking off entirely, pass `thinking: {type: "disabled"}`. Because `max_tokens` is a hard limit on total output (thinking plus response text), revisit it for workloads that ran without thinking on Claude Sonnet 4.6. If you were previously using thinking off with Claude Sonnet 4.6, try thinking on with lower effort levels for Claude Sonnet 5.

The triggering behavior for adaptive thinking is steerable. If you find the model emitting thinking blocks more often than you'd like, which can happen with large or complex system prompts, add guidance to steer it. As always, measure the effect of any prompting changes on performance. Example:

```text wrap
Thinking adds latency and should only be used when it will meaningfully improve answer quality, typically for problems that require multistep reasoning. When in doubt, respond directly.
```

Conversely, if you're running hard workloads at `medium` and seeing under-thinking, the first lever is to raise effort. If you need finer control, prompt for it directly.

Manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) is not supported on Claude Sonnet 5 and returns a 400 error. It was deprecated on Claude Sonnet 4.6 and is now removed. Use adaptive thinking with the effort parameter instead.

<Note>
  If you are running Claude Sonnet 5 at `high`, `xhigh`, or `max` effort, leave headroom in `max_tokens` so the model has room for thinking and tool calls. On long tasks, adaptive thinking can use a large share of the budget; if the budget is tight, you may see a response that is almost entirely thinking followed by a truncated answer and `stop_reason: "max_tokens"`. Raising `max_tokens` or dropping to `medium` effort resolves this. Because Claude Sonnet 5 uses a [new tokenizer](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5#new-tokenizer) that produces approximately 30% more tokens for the same text, `max_tokens` limits tuned for Claude Sonnet 4.6 may truncate equivalent output. The exact increase depends on the content and workload shape.
</Note>

## Tool use triggering

Claude Sonnet 5 is more agentic than Claude Sonnet 4.6 by default and will reach for tools and run self-verification loops more readily. With thinking disabled, the model is less likely to reach for tools or consider searching; if you rely on tool calls with thinking off, add an explicit nudge in the system prompt. Effort is also a lever for tool usage: `high` or `xhigh` effort settings show substantially more tool usage in agentic search and coding. For scenarios where you want more tool use, you can also adjust your prompt to explicitly instruct the model about when and how to properly use its tools. For instance, if you find that the model is not using your web search tools, clearly describe why and how it should.

## User-facing progress updates

Claude Sonnet 5 provides regular, higher-quality updates to the user throughout long agentic traces. If you've added scaffolding to force interim status messages ("After every 3 tool calls, summarize progress"), try removing it. If you find that the length or contents of Claude Sonnet 5's user-facing updates are not well-calibrated to your use case, explicitly describe what these updates should look like in the prompt and provide examples.

## More literal instruction following

Claude Sonnet 5 interprets prompts literally and explicitly, particularly at lower effort levels. It does not silently generalize an instruction from one item to another, and it does not infer requests you didn't make. The upside of this literalism is precision, and it generally performs better for API use cases with carefully tuned prompts, structured extraction, and pipelines where you want predictable behavior. If you need Claude to apply an instruction broadly, state the scope explicitly (for example, "Apply this formatting to every section, not just the first one").

## Tone and writing style

As with any new model, prose style on long-form writing may shift. If your product relies on a specific voice, re-evaluate style prompts against the new baseline.

For instance, if your product voice is warmer or more conversational, add:

```text wrap
Use a warm, collaborative tone. Acknowledge the user's framing before answering.
```

If you previously relied on `temperature` for stylistic variety, note that setting `temperature`, `top_p`, or `top_k` to a non-default value returns a 400 error on Claude Sonnet 5. This constraint is new for Sonnet-class models. Remove these parameters when migrating, and use system-prompt instructions to guide tone and variety instead.

## Design and frontend defaults

Claude Sonnet 5 may settle into a consistent default visual style on open-ended frontend and design briefs. A default house style can read well for some briefs but feel off for dashboards, dev tools, fintech, healthcare, or enterprise apps.

Generic instructions ("don't use that color," "make it clean and minimal") tend to shift the model to a different fixed palette rather than producing variety. Two approaches work reliably:

**1. Specify a concrete alternative.** The model follows explicit specs precisely:

```text wrap
Design a desktop landing page for a supplement brand called AEFRM.

The visual direction should come from a cold monochrome atmosphere using pale silver-gray tones that gradually deepen into blue-gray and near-black, similar to a misted metallic surface.

The page should feel sharp and controlled, with a strong sense of structure and restraint.

Use this tonal system across the full page instead of introducing bright accent colors.

Use the uploaded image on the hero design in black and white.

The layout should be built with clear horizontal sections and a centered max-width container. Use 4px corner radius consistently across cards, buttons, inputs, and media frames. Margins should feel generous, with enough empty space around each section so the page breathes.

Typography should use a square, angular sans-serif with wider letter spacing than usual, especially in headings and navigation, so the text feels more engineered and less compressed. Headline text can be large and uppercase, while supporting copy remains short and sparse. The sub texts should be written with Alumni Sans SC in 4-6px like tiny little texts on corners bottom centre like that.

For the structure, start with a hero section containing a strong product statement, one short supporting paragraph, and a clean product placeholder or packshot frame. Below that, add a benefit grid with three or four blocks, then a formulation or ingredients section, and finally a cta.

Buttons should be flat and precise, with subtle hover changes using transition: all 160ms ease out where brightness and border contrast shift slightly rather than using dramatic motion.

Color palette should stay within this range:
#E9ECEC, #C9D2D4, #8C9A9E, #44545B, #11171B.
```

**2. Have the model propose options before building.** This breaks the default and gives users control. Because `temperature` is not accepted on Claude Sonnet 5, this approach is the recommended way to produce meaningfully different design directions across runs. Example prompt:

```text wrap
Before building, propose 4 distinct visual directions tailored to this brief (each as: bg hex / accent hex / typeface, plus a one-line rationale). Ask the user to pick one, then implement only that direction.
```

To steer away from generic patterns that users call the "AI slop" aesthetic, you can include a short directive in your system prompt. The [frontend-design skill](https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md) provides a fuller treatment, but this snippet works well alongside the preceding variety approaches:

```text wrap
<frontend_aesthetics>
NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white or dark backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character. Use unique fonts, cohesive colors and themes, and animations for effects and micro-interactions.
</frontend_aesthetics>
```

## Interactive coding products

Token usage and behavior can differ between autonomous, asynchronous coding agents with a single user turn and interactive, synchronous coding agents with multiple user turns. To maximize both performance and token efficiency in coding products, use `xhigh` or `high` effort, add autonomous features like an auto mode, and reduce the number of human interactions required from your users.

When limiting the number of required user interactions, it's important to specify the task, intent, and relevant constraints upfront in the first human turn. Providing well-specified, clear, and accurate task descriptions upfront can help maximize autonomy and intelligence while minimizing extra token usage after user turns. In contrast, ambiguous or underspecified prompts conveyed progressively over multiple user turns tend to relatively reduce token efficiency and sometimes performance.

## Code review harnesses

If your code-review harness was tuned for an earlier model, you may initially see lower recall on Claude Sonnet 5. This is likely a harness effect, not a capability regression. When a review prompt says things like "only report high-severity issues," "be conservative," or "don't nitpick," Claude Sonnet 5 may follow that instruction more faithfully than earlier models did: it may investigate the code just as thoroughly, identify the bugs, and then not report findings it judges to be below your stated bar. This can show up as the model doing the same depth of investigation but converting fewer investigations into reported findings, especially on lower-severity bugs. Precision typically rises, but measured recall can fall even though the model's underlying bug-finding ability has improved.

Some recommended prompt language:

```text wrap
Report every issue you find, including ones you are uncertain about or consider low-severity. Do not filter for importance or confidence at this stage - a separate verification step will do that. Your goal here is coverage: it is better to surface a finding that later gets filtered out than to silently drop a real bug. For each finding, include your confidence level and an estimated severity so a downstream filter can rank them.
```

This prompt can be used without having an actual second step, but moving confidence filtering out of the finding step often helps. If your harness has a separate verification, deduplication, or ranking stage, tell the model explicitly that its job at the finding stage is coverage rather than filtering.

If you do want the model to self-filter in a single pass, be concrete about where the bar is rather than using qualitative terms like "important": for example, "report any bugs that could cause incorrect behavior, a test failure, or a misleading result; only omit nits like pure style or naming preferences."

Iterate on prompts against a subset of your evals or test cases to validate recall or F1 score gains.

## Computer use

On the Claude API, Claude Sonnet 5 supports the `computer_toolset_20260801` toolset and the earlier `computer_20251124` tool version. For tasks inside webpages, Claude Sonnet 5 also supports the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) (`browser_toolset_20260801`). [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) capability works across resolutions, up to a maximum resolution of 2576px / 3.75MP. Internal computer use testing shows that sending images at 1080p provides a good balance of performance and cost.

For particularly cost-sensitive workloads, 720p or 1366×768 are lower-cost options with strong performance. Conduct your own testing to find the ideal settings for your use case; experimenting with effort settings can also help tune the model's behavior.
