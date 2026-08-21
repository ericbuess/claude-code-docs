---
title: What's new in Claude Sonnet 5
url: https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5
description: Overview of new features and behavior changes in Claude Sonnet 5.
---

Claude Sonnet 5 is the next generation of Anthropic's Sonnet model family. It is a drop-in upgrade for Claude Sonnet 4.6 with three behavior changes: [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) is on by default, manual extended thinking now returns a 400 error (it was deprecated on Claude Sonnet 4.6), and setting sampling parameters (`temperature`, `top_p`, `top_k`) to non-default values returns a 400 error. This page summarizes everything new at launch, including a new tokenizer.

## New model

| Model           | API model ID      | Description                                    |
| --------------- | ----------------- | ---------------------------------------------- |
| Claude Sonnet 5 | `claude-sonnet-5` | The best combination of speed and intelligence |

Claude Sonnet 5 supports the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) by default (1M tokens is both the default and the maximum; there is no smaller context variant), 128k max output tokens, [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking), and the same set of tools and platform features as Claude Sonnet 4.6, except [Priority Tier](https://platform.claude.com/docs/en/api/service-tiers#supported-models), which is not available on Claude Sonnet 5. On the Claude API, Claude Sonnet 5 also supports the [browser use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) and the generally available `computer_toolset_20260801` version of the [computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), neither of which Claude Sonnet 4.6 supports; the earlier `computer_20251124` version is still accepted on both models. To upgrade an existing integration, see [Migrate from `computer_20251124`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool#migrate-from-computer-20251124).

For complete pricing and specs, see the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).

## Behavior changes

### Adaptive thinking on by default

On Claude Sonnet 4.6, requests without a `thinking` field run without thinking. On Claude Sonnet 5, the same requests run with [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking). To turn thinking off, pass `thinking: {type: "disabled"}`. Because `max_tokens` is a hard limit on total output (thinking plus response text), revisit it for workloads that ran without thinking on Claude Sonnet 4.6.

### Sampling parameters not accepted

Setting `temperature`, `top_p`, or `top_k` to a non-default value returns a 400 error. Remove these parameters when migrating; the default value (or omitting the parameter) is accepted. Use system-prompt instructions to guide model behavior. This is new for Sonnet-class models; the same constraint was previously introduced on Claude Opus 4.7.

### Manual extended thinking removed

Manual extended thinking (`thinking: {type: "enabled", budget_tokens: N}`) was deprecated on Claude Sonnet 4.6; on Claude Sonnet 5 it is removed and returns a 400 error, the same as on Claude Opus 4.8 and Claude Opus 4.7. Use adaptive thinking with the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) instead.

<CodeGroup exclude="shell">
  ```python Python
  # Not supported on Claude Sonnet 5 (returns 400)
  thinking = {"type": "enabled", "budget_tokens": 32000}

  # Use this instead
  thinking = {"type": "adaptive"}
  ```

  ```typescript TypeScript
  // Not supported on Claude Sonnet 5 (returns 400)
  const legacyThinking = { type: "enabled", budget_tokens: 32000 };

  // Use this instead
  const thinking = { type: "adaptive" };
  ```

  ```csharp C#
  // Not supported on Claude Sonnet 5 (returns 400)
  var legacyThinking = new ThinkingConfigEnabled(budgetTokens: 32000);

  // Use this instead
  var thinking = new ThinkingConfigAdaptive();
  ```

  ```go Go
  // Not supported on Claude Sonnet 5 (returns 400)
  legacyThinking := anthropic.ThinkingConfigParamUnion{
  	OfEnabled: &anthropic.ThinkingConfigEnabledParam{BudgetTokens: 32000},
  }

  // Use this instead
  thinking := anthropic.ThinkingConfigParamUnion{
  	OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
  }
  ```

  ```java Java
  // Not supported on Claude Sonnet 5 (returns 400)
  var legacyThinking = ThinkingConfigEnabled.builder().budgetTokens(32_000L).build();

  // Use this instead
  var thinking = ThinkingConfigAdaptive.builder().build();
  ```

  ```php PHP
  // Not supported on Claude Sonnet 5 (returns 400)
  $thinking = ['type' => 'enabled', 'budget_tokens' => 32000];

  // Use this instead
  $thinking = ['type' => 'adaptive'];
  ```

  ```ruby Ruby
  # Not supported on Claude Sonnet 5 (returns 400)
  legacy_thinking = {type: "enabled", budget_tokens: 32_000}

  # Use this instead
  thinking = {type: "adaptive"}
  ```
</CodeGroup>

## New tokenizer

Claude Sonnet 5 uses a new tokenizer. The same input text produces approximately 30% more tokens than on Claude Sonnet 4.6. The exact increase depends on the content. This is not an API change: requests, responses, and streaming events keep the same shape, and no code changes are required.

The change affects anything you measure or budget in tokens:

* **Token counts:** `usage` fields and [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting) results for the same text are higher than on Claude Sonnet 4.6. Don't reuse counts measured against earlier models; recount against Claude Sonnet 5.
* **Context window capacity in text terms:** the context window is 1M tokens, but each token covers less text on average, so the same window holds less text than on Claude Sonnet 4.6.
* **`max_tokens` budgets:** an output limit tuned for Claude Sonnet 4.6 may truncate equivalent output on Claude Sonnet 5. Revisit limits sized close to your expected output length.
* **Per-request cost:** per-token pricing is lower than Claude Sonnet 4.6's (see [Pricing](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5#pricing)), but because the same text produces more tokens, the cost of an equivalent request does not drop in direct proportion.

## API constraints inherited from Claude Sonnet 4.6

<Note>
  This constraint is unchanged from Claude Sonnet 4.6. Aside from the three [behavior changes](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5#behavior-changes) (see [Migration guide](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5#migration-guide)), code that already runs on Claude Sonnet 4.6 needs no other changes.
</Note>

### Assistant message prefilling not supported

Prefilling the assistant message returns a `400` error, unchanged from Claude Sonnet 4.6. Use [structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs), system prompt instructions, or `output_config.format` instead.

## Capability improvements

Claude Sonnet 5 is a capability upgrade over Claude Sonnet 4.6 at a lower price. It is also an option for workloads that need more capability than Claude Sonnet 4.6 provides without moving to an Opus-class model.

The largest gains over Claude Sonnet 4.6 are in coding and agentic tasks. For benchmark results, see [Anthropic's Transparency Hub](https://www.anthropic.com/transparency).

## Cybersecurity safeguards

Claude Sonnet 5 is the first Sonnet-tier model with real-time cybersecurity safeguards. Requests that involve prohibited or high-risk cybersecurity topics may be refused. Refusals return as a successful HTTP 200 response with `stop_reason: "refusal"`, not an error. See [Real-time cyber safeguards on Claude Opus and Sonnet](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude-opus-and-sonnet) for what the safeguards block and how legitimate security work can apply to the Cyber Verification Program.

## Pricing

Claude Sonnet 5 is priced at $2 per million input tokens and $10 per million output tokens, lower per-token pricing than Claude Sonnet 4.6's $3/$15. Because the [new tokenizer](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5#new-tokenizer) produces approximately 30% more tokens for the same text, the cost of an equivalent request does not drop in direct proportion to the per-token prices when comparing with Claude Sonnet 4.6. The exact difference depends on the content and workload shape.

See [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) for complete pricing, including batch processing and prompt caching rates.

## Availability

At launch, Claude Sonnet 5 is available on:

* **Claude API:** available to all customers.
* **AWS:** available through [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) and [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws). On Amazon Bedrock, Claude Sonnet 5 is also reachable through the `InvokeModel` API, served by the same infrastructure as Claude in Amazon Bedrock. The legacy [Claude on Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy) integration does not include Claude Sonnet 5.
* **Google Cloud:** available through [Claude on Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai).
* **Microsoft Foundry:** available through [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry).

Claude Sonnet 5 supports [zero data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention) for organizations with ZDR agreements.

## Migration guide

Claude Sonnet 5 is a drop-in replacement for Claude Sonnet 4.6. Update your model ID:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-sonnet-4-6"  # Before
  model = "claude-sonnet-5"  # After
  ```

  ```typescript TypeScript
  const legacyModel = "claude-sonnet-4-6"; // Before
  const model = "claude-sonnet-5"; // After
  ```

  ```csharp C#
  var legacyModel = Model.ClaudeSonnet4_6; // Before
  var model = Model.ClaudeSonnet5; // After
  ```

  ```go Go
  // Before
  legacyModel := anthropic.ModelClaudeSonnet4_6
  // After
  model := anthropic.ModelClaudeSonnet5
  ```

  ```java Java
  var legacyModel = Model.CLAUDE_SONNET_4_6; // Before
  var model = Model.CLAUDE_SONNET_5; // After
  ```

  ```php PHP
  $model = 'claude-sonnet-4-6'; // Before
  $model = 'claude-sonnet-5'; // After
  ```

  ```ruby Ruby
  legacy_model = "claude-sonnet-4-6" # Before
  model = "claude-sonnet-5" # After
  ```
</CodeGroup>

Then review the following:

1. **Token budgets and counts:** the [new tokenizer](https://platform.claude.com/docs/en/about-claude/models/whats-new-sonnet-5#new-tokenizer) produces approximately 30% more tokens for the same text. The exact increase depends on the content and workload shape. Recount prompts with [token counting](https://platform.claude.com/docs/en/build-with-claude/token-counting), and revisit `max_tokens` limits sized close to your expected output length.
2. **Extended thinking:** if you still set `budget_tokens`, migrate to [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking). Manual extended thinking (`thinking: {type: "enabled"}`) is not supported and returns a 400 error.
3. **Sampling parameters:** requests that set sampling parameters (`temperature`, `top_p`, `top_k`) to a non-default value return a 400 error; remove them when migrating. Tool definitions and response shapes are unchanged, and assistant message prefilling was already unsupported on Claude Sonnet 4.6.

See the [Claude Sonnet 5 section of the migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-sonnet-4-6-to-claude-sonnet-5) for details.

## Next steps

<CardGroup>
  <Card title="Models overview" icon="arrow-right" href="https://platform.claude.com/docs/en/about-claude/models/overview">
    Complete specs and pricing for all current Claude models.
  </Card>

  <Card title="Token counting" icon="database" href="https://platform.claude.com/docs/en/build-with-claude/token-counting">
    Measure your prompts under the new tokenizer before you migrate.
  </Card>

  <Card title="Adaptive thinking" icon="brain" href="https://platform.claude.com/docs/en/build-with-claude/thinking">
    The recommended thinking-on mode on Claude Sonnet 5.
  </Card>

  <Card title="Context windows" icon="sliders" href="https://platform.claude.com/docs/en/build-with-claude/context-windows">
    How the 1M token context window works.
  </Card>

  <Card title="Pricing" icon="shield" href="https://platform.claude.com/docs/en/about-claude/pricing">
    Complete pricing, including batch processing and prompt caching rates.
  </Card>
</CardGroup>
