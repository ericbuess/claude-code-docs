---
title: Effort
url: https://platform.claude.com/docs/en/build-with-claude/effort
description: Control how many tokens Claude uses when responding with the effort parameter, trading off between response thoroughness and token efficiency.
---

## Compatibility
- [ZDR](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention): eligible (excludes [Covered Models](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements))
- Supported models: `claude-fable-5`, `claude-mythos-5`, `claude-mythos-preview`, `claude-opus-5`, `claude-opus-4-8`, `claude-opus-4-7`, `claude-opus-4-6`, `claude-sonnet-5`, `claude-sonnet-4-6`, `claude-opus-4-5-20251101`
- Platforms: Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud, Microsoft Foundry

The effort parameter lets you control how many tokens Claude spends when responding to requests. You can trade off between response thoroughness and token efficiency with a single model. The effort parameter is available on all supported models with no beta header required.

<Tip>
  For how effort interacts with thinking and which control to reach for, see [Thinking and effort](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-effort). Where adaptive thinking is available, effort is the recommended way to control thinking depth.
</Tip>

## How effort works

By default, Claude uses high effort, spending as many tokens as needed for excellent results. You can raise the effort level to `max` for the absolute highest capability, or lower it to be more conservative with token usage, optimizing for speed and cost while accepting some reduction in capability.

<Tip>
  Setting `effort` to `"high"` produces exactly the same behavior as omitting the `effort` parameter entirely.
</Tip>

The effort parameter affects **all tokens** in the response, including:

* Text responses and explanations
* Tool calls and function arguments
* Thinking (when active)

This approach has two major advantages:

1. It doesn't require thinking to be enabled.
2. It can affect all token spend including tool calls. For example, lower effort would mean Claude makes fewer tool calls. This gives a much greater degree of control over efficiency.

### Effort levels

| Level    | Description                                                                                                                                                                                                                                       | Typical use case                                                                           |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| `max`    | Absolute maximum capability with no constraints on token spending. Available on Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, and Claude Sonnet 4.6. | Tasks requiring the deepest possible reasoning and most thorough analysis                  |
| `xhigh`  | Extended capability for long-horizon work. Available on Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, and Claude Sonnet 5.                                                                                    | Long-running agentic and coding tasks (over 30 minutes) with token budgets in the millions |
| `high`   | High capability. Equivalent to not setting the parameter.                                                                                                                                                                                         | Complex reasoning, difficult coding problems, agentic tasks                                |
| `medium` | Balanced approach with moderate token savings.                                                                                                                                                                                                    | Agentic tasks that require a balance of speed, cost, and performance                       |
| `low`    | Most efficient. Significant token savings with some capability reduction.                                                                                                                                                                         | Simpler tasks that need the best speed and lowest costs, such as subagents                 |

`xhigh` is a newer level; some models that support `max` don't support `xhigh`.

<Note>
  Effort is a behavioral signal, not a strict token budget. At lower effort levels, Claude will still think on sufficiently difficult problems, but it will think less than it would at higher effort levels for the same problem.
</Note>

### Recommended effort levels for Claude Sonnet 5

Claude Sonnet 5 defaults to `high` effort on the Claude API and Claude Code.

* **High effort (default):** Suitable for complex reasoning, coding, and agentic tasks where quality matters more than speed or cost.
* **Xhigh effort:** For the hardest coding and agentic tasks. See [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5#calibrating-effort-and-thinking-depth).
* **Medium effort:** Cost-saving step-down from the default. Comparable to Claude Sonnet 4.6 at high effort.
* **Low effort:** For high-volume or latency-sensitive workloads. Suitable for chat and non-coding use cases where faster turnaround is prioritized.
* **Max effort:** For tasks requiring the absolute highest capability with no constraints on token spending.

### Recommended effort levels for Claude Sonnet 4.6

Sonnet 4.6 defaults to `high` effort. Explicitly set effort when using Sonnet 4.6 to avoid unexpected latency:

* **Medium effort** (recommended default): Best balance of speed, cost, and performance for most applications. Suitable for agentic coding, tool-heavy workflows, and code generation.
* **Low effort:** For high-volume or latency-sensitive workloads. Suitable for chat and non-coding use cases where faster turnaround is prioritized.
* **High effort:** For complex reasoning and tasks where quality matters more than speed or cost.
* **Max effort:** For tasks requiring the absolute highest capability with no constraints on token spending.

### Recommended effort levels for Claude Opus 4.7

**Start with `xhigh` for coding and agentic use cases**, and use `high` as the minimum for most intelligence-sensitive workloads. Step down to `medium` for cost-sensitive workloads, or up to `max` only when your evals show measurable headroom at `xhigh`.

The API default is `high`. To use `xhigh`, set `effort` explicitly; the value you pass overrides the default.

| Effort   | Guidance for Claude Opus 4.7                                                                                                                                                                                               |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `low`    | Efficient, but best for short, scoped tasks. Pair `low` with explicit checklists if your task has multiple sections.                                                                                                       |
| `medium` | The drop-in for the average workflow where you want good results while reducing costs.                                                                                                                                     |
| `high`   | Advanced use cases that still need a balance of intelligence and token consumption. This is often the best balance of quality and token efficiency.                                                                        |
| `xhigh`  | The recommended starting point for coding and agentic work, and for exploratory tasks such as repeated tool calling, detailed web search, and knowledge-base search. Expect meaningfully higher token usage than `high`.   |
| `max`    | Reserve for genuinely frontier problems. On most workloads `max` adds significant cost for relatively small quality gains, and on some structured-output or less intelligence-sensitive tasks it can lead to overthinking. |

Claude Opus 4.7 also respects effort levels more strictly than Claude Opus 4.6, especially at `low` and `medium`. At lower effort levels, the model scopes its work to what was asked rather than doing more than requested. If you observe shallow reasoning on complex problems with Claude Opus 4.7, raise effort rather than prompting around it. If you must keep effort low for latency, add targeted guidance like "This task involves multistep reasoning. Think carefully before responding."

When running Claude Opus 4.7 at `xhigh` or `max` effort, set a large `max_tokens` so the model has room to think and act across subagents and tool calls. Starting at 64k tokens and tuning from there is a reasonable default.

### Recommended effort levels for Claude Opus 4.8

The guidance for Claude Opus 4.7 also applies to Claude Opus 4.8. **Start with `xhigh` for coding and agentic use cases**, use `high` for most other intelligence-sensitive workloads, and step down to `medium` or `low` only when you've measured that the lower level holds quality on your evals.

The API default is `high`. Set `effort` explicitly to use a different level; the value you pass overrides the default.

When running Claude Opus 4.8 at `xhigh` or `max` effort, set a large `max_tokens` so the model has room to think and act across subagents and tool calls. Starting at 64k tokens and tuning from there is a reasonable default.

### Recommended effort levels for Claude Opus 5

Claude Opus 5 supports all five effort levels. **Start with `high`, the default**, and adjust based on your evals: step up to `xhigh` for demanding coding and agentic work, or to `max` when a task justifies unconstrained token spending, and use `low` and `medium` liberally as your primary control for token cost and response time wherever your evals show quality holds. If you carried effort settings over from an earlier model, run a fresh effort sweep on your evals rather than reusing them.

Effort controls thinking volume, not visible response length: on Claude Opus 5, changing effort does not reliably shorten responses, so [prompt for length](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5#response-length-and-verbosity) instead.

The API default is `high`. Set `effort` explicitly to use a different level; the value you pass overrides the default.

On Claude Opus 5, thinking cannot be disabled at `xhigh` or `max` effort: requests that set `thinking: {"type": "disabled"}` at those levels return a 400 error. See [Effort with thinking](https://platform.claude.com/docs/en/build-with-claude/effort#effort-with-thinking).

When running Claude Opus 5 at `xhigh` or `max` effort, set a large `max_tokens` so the model has room to think and act across subagents and tool calls. Starting at 64k tokens and tuning from there is a reasonable default.

### Recommended effort levels for Claude Fable 5

Effort is the primary control for trading off intelligence, latency, and cost on Claude Fable 5. **Start with `high`, the default, for most tasks**, use `xhigh` for the most capability-sensitive workloads, and step down to `medium` or `low` for routine work. Lower effort settings on Claude Fable 5 still perform well and often exceed `xhigh` performance on prior models. At `high` and `xhigh`, set a large `max_tokens`: it is a hard limit on total output, thinking plus response text. See [Cost control](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#cost-control).

Reduce effort if a task completes but takes longer than necessary, or if you want a faster, more interactive working style. The same recommendations apply to Claude Mythos 5. For fuller guidance, see [Prompting Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5).

## Basic usage

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 4096,
      "messages": [{
        "role": "user",
        "content": "Analyze the trade-offs between microservices and monolithic architectures"
      }],
      "output_config": {
        "effort": "medium"
      }
    }'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-5 \
    --max-tokens 4096 \
    --output-config '{effort: medium}' \
    --message '{role: user, content: "Analyze the trade-offs between microservices and monolithic architectures"}' \
    --transform 'content.#(type=="text").text' \
    --raw-output
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=4096,
      messages=[
          {
              "role": "user",
              "content": "Analyze the trade-offs between microservices and monolithic architectures",
          }
      ],
      output_config={"effort": "medium"},
  )

  for block in response.content:
      if block.type == "text":
          print(block.text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 4096,
    messages: [
      {
        role: "user",
        content: "Analyze the trade-offs between microservices and monolithic architectures"
      }
    ],
    output_config: {
      effort: "medium"
    }
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.TextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 4096,
      Messages = [
          new() {
              Role = Role.User,
              Content = "Analyze the trade-offs between microservices and monolithic architectures"
          }
      ],
      OutputConfig = new OutputConfig
      {
          Effort = Effort.Medium
      }
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 4096,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the trade-offs between microservices and monolithic architectures")),
  	},
  	OutputConfig: anthropic.OutputConfigParam{
  		Effort: anthropic.OutputConfigEffortMedium,
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  for _, block := range response.Content {
  	if textBlock, ok := block.AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(textBlock.Text)
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.OutputConfig;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(4096L)
          .addUserMessage("Analyze the trade-offs between microservices and monolithic architectures")
          .outputConfig(OutputConfig.builder()
              .effort(OutputConfig.Effort.MEDIUM)
              .build())
          .build();

      Message response = client.messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> IO.println(textBlock.text()));
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 4096,
      messages: [
          ['role' => 'user', 'content' => 'Analyze the trade-offs between microservices and monolithic architectures']
      ],
      model: 'claude-opus-5',
      outputConfig: ['effort' => 'medium'],
  );

  foreach ($message->content as $block) {
      if ($block->type === 'text') {
          echo $block->text, PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 4096,
    messages: [
      { role: "user", content: "Analyze the trade-offs between microservices and monolithic architectures" }
    ],
    output_config: {
      effort: "medium"
    }
  )

  message.content.each do |block|
    puts block.text if block.type == :text
  end
  ```
</CodeGroup>

## When to adjust the effort parameter

* Use **max effort** when you need the absolute highest capability with no constraints: the most thorough reasoning and deepest analysis. Available on Claude 4.6 and later models and Claude Mythos Preview.
* Use **xhigh effort** for advanced coding and complex agentic work requiring extended exploration, such as repeated tool calling and detailed search. Available on Claude Fable 5, Claude Mythos 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, and Claude Sonnet 5.
* Use **high effort** (the default) for complex reasoning, nuanced analysis, difficult coding problems, or any task where quality matters more than speed or cost.
* Use **medium effort** as a balanced option when you want solid performance without the full token expenditure of high effort.
* Use **low effort** when you're optimizing for speed (because Claude answers with fewer tokens) or cost. For example, simple classification tasks, quick lookups, or high-volume use cases where marginal quality improvements don't justify additional latency or spend.

## Effort with tool use

When using tools, the effort parameter affects both the explanations around tool calls and the tool calls themselves. Lower effort levels tend to:

* Combine multiple operations into fewer tool calls
* Make fewer tool calls
* Proceed directly to action without preamble
* Use terse confirmation messages after completion

Higher effort levels may:

* Make more tool calls
* Explain the plan before taking action
* Provide detailed summaries of changes
* Include more comprehensive code comments

## Effort with thinking

The `thinking` parameter controls whether Claude thinks in [thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking) before answering; the `effort` parameter controls how much work Claude puts into the whole response, which in adaptive mode includes how often and how deeply it thinks. Don't pass `adaptive` as an `effort` value: `adaptive` is a thinking mode, not an effort level.

At higher effort levels, Claude thinks on most requests and at greater length; at lower levels, it can skip thinking entirely for simpler problems. See [Thinking and effort](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-effort) for full guidance on how the two controls work together.

On Claude Opus 4.5, the only extended-thinking-only model that supports effort, it works alongside [`budget_tokens`](https://platform.claude.com/docs/en/build-with-claude/extended-thinking): set the effort level for your task, then set the thinking token budget based on how much reasoning depth the task needs.

For per-model thinking availability, see the [per-model configuration table](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#supported-models). Effort works with or without thinking; see [How effort works](https://platform.claude.com/docs/en/build-with-claude/effort#how-effort-works).

## Changing effort mid-conversation

`output_config.effort` is a request-level setting: each request carries its own value, so to run a later part of a conversation at a different effort level, set the new value on the next request. The effort level applies to the whole request. Because effort shapes the rendered prompt, changing it between requests does not preserve cached prefixes from earlier turns; if you rely on [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) across a long session, pick an effort level at the start and keep it constant.

## Best practices

1. **Set effort explicitly:** The API defaults to `high`, but the right starting point depends on your model and workload.
2. **Use low for speed-sensitive or simple tasks:** When latency matters or tasks are straightforward, low effort can significantly reduce response times and costs.
3. **Test your use case:** The impact of effort levels varies by task type. Evaluate performance on your specific use cases before deploying.
4. **Consider dynamic effort:** Adjust effort based on task complexity. Simple queries may warrant low effort while agentic coding and complex reasoning benefit from high effort. See the next item before varying it within one conversation.
5. **Hold effort constant within cached conversations:** Changing the effort value between requests invalidates [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching), so vary effort across workloads rather than within a conversation that relies on cache hits. See [Thinking and prompt caching](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-prompt-caching).

## Next steps

<CardGroup>
  <Card title="Task budgets" icon="gauge" href="https://platform.claude.com/docs/en/build-with-claude/task-budgets">
    Give Claude an advisory token budget for the full agentic loop to help the model self-regulate on long agentic tasks.
  </Card>

  <Card title="Steering thinking" icon="compass" href="https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost">
    Understand adaptive thinking, where Claude decides when and how much to think, and steer it with effort and prompting.
  </Card>

  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/en/build-with-claude/thinking">
    Understand how thinking works, when Claude thinks by default, and how thinking interacts with effort.
  </Card>
</CardGroup>
