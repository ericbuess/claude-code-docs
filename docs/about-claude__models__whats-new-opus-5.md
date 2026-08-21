---
title: What's new in Claude Opus 5
url: https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5
description: Overview of new features and behavior changes in Claude Opus 5.
---

Claude Opus 5 is a step-change improvement over Claude Opus 4.8, with the largest gains in deep reasoning, agentic and long-horizon tasks, and test-time compute scaling. This page summarizes everything new in Claude Opus 5, including thinking on by default, mid-conversation tool changes, and a breaking change to when thinking can be disabled.

## New model

| Model         | API model ID    | Description                                    |
| ------------- | --------------- | ---------------------------------------------- |
| Claude Opus 5 | `claude-opus-5` | For complex agentic coding and enterprise work |

Claude Opus 5 has a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) (1M tokens is both the default and the maximum; there is no smaller context variant), 128k max output tokens, and [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) on by default.

For complete pricing and specs, see the [models overview](https://platform.claude.com/docs/en/about-claude/models/overview).

## New features

### Mid-conversation tool changes (beta)

You can add or remove tools between turns of a conversation while preserving the prompt cache, instead of resending a fixed tool list for the life of a session. Mid-conversation tool changes are in beta: include the `mid-conversation-tool-changes-2026-07-01` beta header in your requests. See [Mid-conversation tool changes](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages#mid-conversation-tool-changes) for usage.

### Default fallbacks mode

The `fallbacks` parameter supports a new `"default"` mode, which applies Anthropic's recommended fallback models by refusal category instead of a model list you maintain yourself. The entire `fallbacks` parameter is in beta. Use the `server-side-fallback-2026-07-01` beta header, which supports both the `"default"` mode and explicit model lists (the earlier `server-side-fallback-2026-06-01` header accepts only explicit lists). See [Refusals and fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback).

### Lower prompt cache minimum

The minimum cacheable prompt length on Claude Opus 5 is 512 tokens, down from 1,024 tokens on Claude Opus 4.8. Prompts that were too short to cache on Claude Opus 4.8 can now create cache entries with no code changes. See [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#cache-limitations) for per-model minimums.

### Fast mode

[Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) (research preview) is available for Claude Opus 5 on the Claude API only; it is not currently available on Amazon Bedrock, Google Cloud, or Microsoft Foundry. Fast mode for Claude Opus 5 is priced at $10 USD per million input tokens and $50 USD per million output tokens. See [Fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) for access, supported models, and pricing.

## Behavior changes

### Thinking on by default

On Claude Opus 4.8, requests run without thinking unless you set `thinking: {"type": "adaptive"}`. On Claude Opus 5, the same requests run with [thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) on: the model decides when and how much to think on each turn, and the [effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort) is the control for thinking depth. The wire value is unchanged; `thinking: {"type": "adaptive"}` remains valid and equivalent to the default.

Because `max_tokens` is a hard limit on total output (thinking plus response text), revisit it for workloads that ran without thinking on Claude Opus 4.8.

The API keeps the option to disable thinking, subject to the effort restriction below.

### Effort matters more

Claude Opus 5 converts additional [effort](https://platform.claude.com/docs/en/build-with-claude/effort) into better results more reliably than any earlier Opus model, so the effort level you choose carries more weight. The full ladder is available: `low`, `medium`, `high`, `xhigh`, and `max`, with `max` as the top tier for the deepest possible reasoning. Start at the default, `high`, and adjust in either direction based on your evals: step down where quality holds to save tokens and latency, or step up for the most demanding work. When running at `xhigh` or `max` effort, set a large `max_tokens` so the model has room to think and act across subagents and tool calls.

This request turns effort all the way up to `max`:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 64000,
      "stream": true,
      "output_config": {
        "effort": "max"
      },
      "messages": [
        {
          "role": "user",
          "content": "Explain why the sum of two even numbers is always even."
        }
      ]
    }'
  ```

  ```bash CLI
  # 64k max_tokens can run past the non-streaming time limit; stream the events.
  ant messages create --stream --format jsonl <<'YAML'
  model: claude-opus-5
  max_tokens: 64000
  output_config:
    effort: max
  messages:
    - role: user
      content: Explain why the sum of two even numbers is always even.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-5",
      max_tokens=64000,
      output_config={"effort": "max"},
      messages=[
          {
              "role": "user",
              "content": "Explain why the sum of two even numbers is always even.",
          }
      ],
  ) as stream:
      response = stream.get_final_message()

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-5",
    max_tokens: 64000,
    output_config: {
      effort: "max"
    },
    messages: [
      {
        role: "user",
        content: "Explain why the sum of two even numbers is always even."
      }
    ]
  });

  const response = await stream.finalMessage();
  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 64000,
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Max
      },
      Messages = [new() { Role = Role.User, Content = "Explain why the sum of two even numbers is always even." }]
  };

  var response = await client.Messages.CreateStreaming(parameters).Aggregate();
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 64000,
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMax,
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Explain why the sum of two even numbers is always even.")),
  	},
  })

  response := anthropic.Message{}
  for stream.Next() {
  	event := stream.Current()
  	if err := response.Accumulate(event); err != nil {
  		log.Fatal(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_5)
      .maxTokens(64000L)
      .outputConfig(OutputConfig.builder()
          .effort(OutputConfig.Effort.MAX)
          .build())
      .addUserMessage("Explain why the sum of two even numbers is always even.")
      .build();

  MessageAccumulator accumulator = MessageAccumulator.create();
  try (var streamResponse = client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(accumulator::accumulate);
  }

  Message response = accumulator.message();
  IO.println(response);
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 64000,
      messages: [
          ['role' => 'user', 'content' => 'Explain why the sum of two even numbers is always even.']
      ],
      model: Model::CLAUDE_OPUS_5,
      outputConfig: ['effort' => Effort::MAX],
  );

  $accumulator = MessageAccumulator::forMessages();
  foreach ($stream as $event) {
      $accumulator->accumulate($event);
  }

  echo $accumulator->message();
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.stream(
    model: Anthropic::Model::CLAUDE_OPUS_5,
    max_tokens: 64000,
    output_config: {
      effort: :max
    },
    messages: [
      { role: "user", content: "Explain why the sum of two even numbers is always even." }
    ]
  ).accumulated_message

  puts response
  ```
</CodeGroup>

Thinking is [on by default](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5#thinking-on-by-default) on Claude Opus 5, so no `thinking` field is needed.

### Disabling thinking requires effort `high` or below

On Claude Opus 5, `thinking: {"type": "disabled"}` is accepted only when the effort level is `high` or below. Setting `thinking: {"type": "disabled"}` with effort `xhigh` or `max` returns a 400 error. This is generally available behavior on Claude Opus 5 onward, enforced on each request, and it is a breaking change from Claude Opus 4.8, where disabling thinking was independent of the effort level. If you disable thinking at high effort levels today, either keep thinking disabled and set effort to `high` or below, or keep the effort level and remove the `thinking` field.

With thinking disabled, Claude Opus 5 can occasionally write a tool call into its text output instead of emitting a `tool_use` block, or include internal XML tags in its visible response. Where possible, keep thinking enabled and control token cost with lower effort levels; for integrations that must keep thinking disabled, see [Running with thinking disabled](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#running-with-thinking-disabled) for prompting mitigations.

### Model behavior differences

Beyond the API changes above, Claude Opus 5 behaves differently from Claude Opus 4.8 in ways you may notice without changing any code. Default user-facing responses and written deliverables run longer. In agentic sessions, the model narrates its progress to the user more often. In multi-agent frameworks, it delegates to subagents more readily. It also verifies its own work without being told to, so remove verification instructions carried over from earlier models ("include a final verification step," "use a subagent to verify"); they cause over-verification on Claude Opus 5. For prompting patterns that tune each of these behaviors, see [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5).

## Capability improvements

Compared with Claude Opus 4.8, Claude Opus 5 is a step-change improvement rather than an incremental one, and it delivers frontier intelligence at half the cost of Claude Fable 5. The largest gains are in:

* **Deep reasoning**, sustaining multistep analysis across long problem chains.
* **Agentic coding and long-horizon tasks**, staying on task across extended tool-use loops and completing multi-file features, larger refactors, and end-to-end feature work without leaving stubs or placeholders.
* **Test-time compute scaling**, converting additional effort (up to the `max` level) into better results.
* **Efficiency at lower effort levels**, with `low` and `medium` [effort](https://platform.claude.com/docs/en/build-with-claude/effort) producing strong quality at a fraction of the tokens and latency of higher settings.
* **Code review and bug-finding**, surfacing real bugs at a high rate per pass with few false positives, and staying accurate at lower effort levels.
* **Vision**, understanding charts, documents, and diagrams and replicating UI and frontend visuals, strongest when given tools to iteratively analyze, crop, and verify its work.
* **Long-context work**, with a [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) as both the default and the maximum, and consistent instruction following, tool calling, and reasoning throughout the window.
* **Office and document tasks**, generating and editing complex multi-sheet spreadsheets with non-trivial formulas, and producing well-structured slide decks.
* **Multi-agent coordination**, running teams of subagents with effective writer-verifier patterns and few cases of agents overwriting each other's work.

For the prompting patterns that get the most out of these capabilities, see [Prompting Claude Opus 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#capability-improvements).

## Pricing

Claude Opus 5 is priced at $5 USD per million input tokens and $25 USD per million output tokens, unchanged from Claude Opus 4.8.

See [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) for complete pricing, including batch processing, prompt caching, and fast mode rates.

## Availability

Claude Opus 5 is available on:

* **Claude API:** available to all customers, as `claude-opus-5`.
* **AWS:** available through [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), as `anthropic.claude-opus-5`. Claude Opus 5 is also reachable through the `InvokeModel` API on `bedrock-runtime`, served by the same infrastructure; the [Claude on Amazon Bedrock (legacy)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy) integration does not include it in its ARN-versioned model ID table.
* **Google Cloud:** available through [Claude on Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai), as `claude-opus-5`.
* **Microsoft Foundry:** available through [Claude in Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry).

Claude Opus 4.8 remains available on all of these platforms.

## Migration guide

To migrate from Claude Opus 4.8, update your model ID:

<CodeGroup exclude="shell">
  ```python Python
  model = "claude-opus-4-8"  # Before
  model = "claude-opus-5"  # After
  ```

  ```typescript TypeScript
  let model = "claude-opus-4-8"; // Before
  model = "claude-opus-5"; // After
  ```

  ```csharp C#
  var model = Model.ClaudeOpus4_8; // Before
  model = Model.ClaudeOpus5; // After
  ```

  ```go Go
  model := anthropic.ModelClaudeOpus4_8 // Before
  model = anthropic.ModelClaudeOpus5    // After
  ```

  ```java Java
  Model model = Model.CLAUDE_OPUS_4_8; // Before
  model = Model.CLAUDE_OPUS_5; // After
  ```

  ```php PHP
  $model = Model::CLAUDE_OPUS_4_8; // Before
  $model = Model::CLAUDE_OPUS_5; // After
  ```

  ```ruby Ruby
  model = Anthropic::Model::CLAUDE_OPUS_4_8 # Before
  model = Anthropic::Model::CLAUDE_OPUS_5 # After
  ```
</CodeGroup>

Then review the two [behavior changes](https://platform.claude.com/docs/en/about-claude/models/whats-new-opus-5#behavior-changes): thinking is on by default, and disabling thinking with effort `xhigh` or `max` returns a 400 error. See the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-opus-4-8-to-claude-opus-5) for step-by-step instructions.

## Next steps

<CardGroup cols={3}>
  <Card title="Models overview" icon="arrow-right" href="https://platform.claude.com/docs/en/about-claude/models/overview">
    Complete specs and pricing for all current Claude models.
  </Card>

  <Card title="Prompting Claude Opus 5" icon="terminal" href="https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5">
    Behavioral differences and prompting patterns specific to Claude Opus 5.
  </Card>

  <Card title="Effort" icon="gauge" href="https://platform.claude.com/docs/en/build-with-claude/effort">
    Control how many tokens Claude uses when responding, from low to max.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/en/build-with-claude/thinking">
    How thinking works when it's on by default, and when it can be disabled.
  </Card>

  <Card title="Task budgets" icon="database" href="https://platform.claude.com/docs/en/build-with-claude/task-budgets">
    Give Claude an advisory token budget to pace its work against.
  </Card>

  <Card title="Migration guide" icon="code" href="https://platform.claude.com/docs/en/about-claude/models/migration-guide">
    Guide for migrating to the latest Claude models from previous Claude versions.
  </Card>

  <Card title="Fast mode" icon="bolt" href="https://platform.claude.com/docs/en/build-with-claude/fast-mode">
    Get higher output tokens per second from Claude Opus models at premium pricing.
  </Card>
</CardGroup>
