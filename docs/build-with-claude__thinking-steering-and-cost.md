---
title: Steering thinking
url: https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost
description: Steer how often and how deeply Claude thinks with effort levels, system prompt guidance, and per-message steering, and understand thinking's cost and pricing.
---

<Note>
  For how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

Claude's thinking is adaptive: the model evaluates each request and decides for itself whether to think and how much. You set an intent, optionally specify the effort, and the model allocates reasoning where it judges reasoning will help.

This makes thinking a strong fit for workloads that mix trivial and complex requests, and for long-horizon agentic workflows where the right amount of reasoning varies from step to step.

For how to turn thinking on, how to read thinking output, and [thinking output on Claude Fable 5 and Claude Mythos 5](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5), see the [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) overview. This page covers how Claude decides when to think, how to steer that decision, and the caching, cost, and pricing mechanics that follow from it.

## How Claude decides when to think

Thinking is optional for the model. On each request, Claude weighs the complexity of the input and decides whether deeper reasoning would improve the answer. A simple factual question may get a direct response with no thinking block at all; a multistep math problem or a tricky debugging task triggers deeper reasoning.

The decision happens per request. The same conversation can contain turns with and without thinking, and a turn where Claude chose not to think contains no thinking block. Don't build application logic that assumes every assistant turn starts with one.

The primary control over this decision is the [effort](https://platform.claude.com/docs/en/build-with-claude/effort) parameter, which acts as soft guidance for how willing Claude should be to think and how deeply; see [Effort levels](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#effort-levels) on this page for what each level does.

If you want Claude to think less often, lower the effort level before reaching for prompt-based steering.

Thinking also interleaves with tool use automatically: Claude can think between tool calls, reflecting on each tool result before deciding what to do next ([interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#interleaved-thinking)). You don't need a beta header or any additional configuration for this.

For the full picture of how the thinking configuration and the effort parameter interact, see [Thinking and effort](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-effort).

## Steering how often Claude thinks

Whether Claude thinks on a given turn is promptable. Effort sets the overall posture, but you can also shape the decision directly with natural-language guidance, either globally in the system prompt or per message from the user turn.

Use the two levers together in this order:

1. Set the effort level that matches your workload's default balance of quality and latency.
2. Add prompt guidance only if Claude's triggering still doesn't match your needs at that level.

For broader prompting guidance with thinking, see [leverage thinking and interleaved thinking capabilities](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#leverage-thinking-and-interleaved-thinking-capabilities).

### Effort levels

Effort is the primary steering lever for thinking. Each level sets a different default for how often Claude thinks and how deeply:

| Effort level     | Thinking behavior                                                                    |
| ---------------- | ------------------------------------------------------------------------------------ |
| `max`            | Claude always thinks with no constraints on thinking depth.                          |
| `xhigh`          | Claude always thinks deeply with extended exploration.                               |
| `high` (default) | Claude almost always thinks. Provides deep reasoning on complex tasks.               |
| `medium`         | Claude uses moderate thinking. May skip thinking for simple queries.                 |
| `low`            | Claude minimizes thinking. Skips thinking for simple tasks where speed matters most. |

This table describes how each level changes thinking behavior. For guidance on which level to choose for a given workload, including per-model recommendations, see [When to adjust the effort parameter](https://platform.claude.com/docs/en/build-with-claude/effort#when-to-adjust-the-effort-parameter) on the effort page.

Effort is set at `output_config.effort`, not inside the `thinking` object; for full per-language examples, see [Effort](https://platform.claude.com/docs/en/build-with-claude/effort#basic-usage).

```json
{
  "model": "claude-opus-4-8",
  "max_tokens": 4096,
  "output_config": { "effort": "medium" },
  "messages": [{ "role": "user", "content": "..." }]
}
```

Level availability varies by model; the [effort availability table](https://platform.claude.com/docs/en/build-with-claude/effort#effort-levels) on the effort page is the authority for which levels each model supports.

### System prompt guidance

System prompt guidance shifts Claude's thinking threshold for every request in the conversation. If Claude is thinking more often than your workload needs, add guidance like this to your system prompt:

```text wrap
Extended thinking adds latency and should only be used when it
will meaningfully improve answer quality, typically for problems
that require multistep reasoning. When in doubt, respond directly.
```

To encourage thinking instead, use a phrase like:

```text wrap
This task involves multistep reasoning. Think carefully before responding.
```

Steering effectiveness can be sensitive to exact wording. If one phrasing doesn't produce the behavior you want, try a more direct variant.

### Per-message steering

You can also steer thinking on a per-message basis from the user turn, independently of the system prompt. Appending `"Please think hard before responding."` to a user message encourages Claude to think on that turn; `"Answer directly without deliberating."` suppresses it.

Per-message steering is useful when only some requests in a conversation warrant extended reasoning. An agent harness, for example, can append the encouraging phrase on planning steps and the suppressing phrase on routine confirmations, without touching the system prompt or changing any request parameters between turns.

### Verify steering on your workload

Prompt-based steering changes model behavior, so treat it like any other prompt change: measure before you ship. Run a representative sample of your traffic with and without the guidance, and compare how often thinking triggers (the presence of thinking blocks in responses), output token usage, latency, and answer quality on the cases that matter to you.

<Warning>
  Steering Claude to think less often may reduce quality on tasks that benefit from reasoning. Lowering the [effort](https://platform.claude.com/docs/en/build-with-claude/effort) level is usually the better first lever, since it is a calibrated control rather than a wording-sensitive instruction. Measure the impact on your specific workloads before deploying prompt-based tuning to production.
</Warning>

## Mechanics

Three mechanics follow from Claude managing its own thinking: turn validation, prompt caching, and how you bound cost.

### Turn validation

Assistant turns don't need to start with a thinking block. (Models using a legacy manual thinking budget enforce that the final assistant turn of a thinking-enabled request begins with one; see [Turn structure in manual mode](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#turn-structure-in-manual-mode).)

For multi-turn applications, this means you can pass back conversation history in whatever shape you have it:

* Assistant turns where Claude chose not to think are valid history as-is.
* You can resume a conversation that began without thinking, or that used a different thinking configuration, without rewriting its history.
* History assembled from mixed sources doesn't need thinking blocks reinserted at the start of each assistant turn to pass validation.

The relaxation is about validation, not about what you should send. When you have thinking blocks, pass them back unmodified, particularly during tool use, where they carry the reasoning behind Claude's tool calls. See the [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) overview for the full rules.

### Prompt caching

Consecutive requests that keep the same thinking configuration and effort level preserve prompt caching; see [Thinking and prompt caching](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-and-prompt-caching) for the full rules. The resolved effort value is rendered into the prompt, so changing it between requests invalidates cache breakpoints, just as changing the legacy [`budget_tokens`](https://platform.claude.com/docs/en/build-with-claude/extended-thinking#extended-thinking-with-prompt-caching) parameter does on models that use it. Setting `effort` explicitly to the model's default is equivalent to omitting it and does not break the cache.

The practical consequence: pick a thinking configuration and an effort level per conversation and keep them. If some turns need more or less thinking, steer with [per-message prompting](https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost#tuning-thinking-behavior): guidance appended to the newest user message leaves earlier cache breakpoints intact, where a configuration or effort change does not.

The following example demonstrates the invalidation with a multi-turn script you can run yourself:

<Accordion title="Effort changes invalidate the prompt cache">
  <Tabs>
    <Tab title="cURL">
      <Note>
        This workflow doesn't translate well to a one-off shell command. See the SDK tabs for the multi-turn pattern; per-turn HTTP requests follow the examples on the [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) page.
      </Note>
    </Tab>

    <Tab title="CLI">
      <Note>
        This workflow doesn't translate well to a one-off shell command. See the SDK tabs for the multi-turn pattern; per-turn CLI invocations follow the examples on the [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) page.
      </Note>
    </Tab>

    <Tab title="Python">
      ```python
      import requests

      client = Anthropic()


      def fetch_article_content(url):
          text = requests.get(url).text
          lines = (line.strip() for line in text.splitlines())
          return "\n".join(line for line in lines if line)


      # Fetch the content of the article
      book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      book_content = fetch_article_content(book_url)
      # Use just enough text for caching (first few chapters)
      LARGE_TEXT = book_content[:10000]

      # No system prompt - caching in messages instead
      MESSAGES = [
          {
              "role": "user",
              "content": [
                  {
                      "type": "text",
                      "text": LARGE_TEXT,
                      "cache_control": {"type": "ephemeral"},
                  },
                  {"type": "text", "text": "Analyze the tone of this passage."},
              ],
          }
      ]

      # First request - establish cache
      print("First request - establishing cache")
      response1 = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          messages=MESSAGES,
      )

      print(f"First response usage: {response1.usage}")

      MESSAGES.append({"role": "assistant", "content": response1.content})
      MESSAGES.append({"role": "user", "content": "Analyze the characters in this passage."})

      # Second request - same configuration (cache hit expected)
      print("\nSecond request - same configuration (cache hit expected)")
      response2 = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          messages=MESSAGES,
      )

      print(f"Second response usage: {response2.usage}")

      MESSAGES.append({"role": "assistant", "content": response2.content})
      MESSAGES.append({"role": "user", "content": "Analyze the setting in this passage."})

      # Third request - different effort level (cache miss expected)
      print("\nThird request - different effort level (cache miss expected)")
      response3 = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          output_config={"effort": "medium"},
          messages=MESSAGES,
      )

      print(f"Third response usage: {response3.usage}")
      ```
    </Tab>

    <Tab title="TypeScript">
      ```typescript

      const client = new Anthropic();

      async function fetchArticleContent(url: string): Promise<string> {
        const response = await fetch(url);
        const text = await response.text();
        const lines = text.split("\n").map((line) => line.trim());
        return lines.filter((line) => line).join("\n");
      }

      const bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      const bookContent = await fetchArticleContent(bookUrl);
      const LARGE_TEXT = bookContent.substring(0, 10000);

      // No system prompt - caching in messages instead
      const messages: Anthropic.MessageParam[] = [
        {
          role: "user",
          content: [
            {
              type: "text",
              text: LARGE_TEXT,
              cache_control: { type: "ephemeral" }
            },
            {
              type: "text",
              text: "Analyze the tone of this passage."
            }
          ]
        }
      ];

      // First request - establish cache
      console.log("First request - establishing cache");
      const response1 = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: { type: "adaptive" },
        messages
      });

      console.log("First response usage: ", response1.usage);

      messages.push(
        { role: "assistant", content: response1.content },
        { role: "user", content: "Analyze the characters in this passage." }
      );

      // Second request - same configuration (cache hit expected)
      console.log("\nSecond request - same configuration (cache hit expected)");
      const response2 = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: { type: "adaptive" },
        messages
      });

      console.log("Second response usage: ", response2.usage);

      messages.push(
        { role: "assistant", content: response2.content },
        { role: "user", content: "Analyze the setting in this passage." }
      );

      // Third request - different effort level (cache miss expected)
      console.log("\nThird request - different effort level (cache miss expected)");
      const response3 = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: { type: "adaptive" },
        output_config: { effort: "medium" },
        messages
      });

      console.log("Third response usage: ", response3.usage);
      ```
    </Tab>

    <Tab title="C#">
      ```csharp
      AnthropicClient client = new();

      string bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      string bookContent = await FetchArticleContent(bookUrl);
      string largeText = bookContent.Substring(0, Math.Min(10000, bookContent.Length));

      Console.WriteLine("First request - establishing cache");
      var parameters1 = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = largeText,
                          CacheControl = new CacheControlEphemeral(),
                      }),
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = "Analyze the tone of this passage."
                      }),
                  })
              }
          ]
      };

      var response1 = await client.Messages.Create(parameters1);
      Console.WriteLine($"First response usage: {response1.Usage}");

      Console.WriteLine("\nSecond request - same configuration (cache hit expected)");
      var parameters2 = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = largeText,
                          CacheControl = new CacheControlEphemeral(),
                      }),
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = "Analyze the tone of this passage."
                      }),
                  })
              },
              new()
              {
                  Role = Role.Assistant,
                  Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new()
              {
                  Role = Role.User,
                  Content = "Analyze the characters in this passage."
              }
          ]
      };

      var response2 = await client.Messages.Create(parameters2);
      Console.WriteLine($"Second response usage: {response2.Usage}");

      Console.WriteLine("\nThird request - different effort level (cache miss expected)");
      var parameters3 = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          OutputConfig = new OutputConfig
          {
              Effort = Effort.Medium
          },
          Messages =
          [
              new()
              {
                  Role = Role.User,
                  Content = new MessageParamContent(new List<ContentBlockParam>
                  {
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = largeText,
                          CacheControl = new CacheControlEphemeral(),
                      }),
                      new ContentBlockParam(new TextBlockParam()
                      {
                          Text = "Analyze the tone of this passage."
                      }),
                  })
              },
              new()
              {
                  Role = Role.Assistant,
                  Content = response1.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new()
              {
                  Role = Role.User,
                  Content = "Analyze the characters in this passage."
              },
              new()
              {
                  Role = Role.Assistant,
                  Content = response2.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              },
              new()
              {
                  Role = Role.User,
                  Content = "Analyze the setting in this passage."
              }
          ]
      };

      var response3 = await client.Messages.Create(parameters3);
      Console.WriteLine($"Third response usage: {response3.Usage}");

      static async Task<string> FetchArticleContent(string url)
      {
          using HttpClient httpClient = new();
          string content = await httpClient.GetStringAsync(url);
          return content;
      }
      ```
    </Tab>

    <Tab title="Go">
      ```go
      client := anthropic.NewClient()

      bookURL := "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      bookContent, err := fetchArticleContent(bookURL)
      if err != nil {
      	log.Fatal(err)
      }

      largeText := bookContent
      if len(largeText) > 10000 {
      	largeText = largeText[:10000]
      }

      // No system prompt - caching in messages instead
      messages := []anthropic.MessageParam{
      	anthropic.NewUserMessage(
      		anthropic.ContentBlockParamUnion{OfText: &anthropic.TextBlockParam{
      			Text:         largeText,
      			CacheControl: anthropic.NewCacheControlEphemeralParam(),
      		}},
      		anthropic.NewTextBlock("Analyze the tone of this passage."),
      	),
      }

      // First request - establish cache
      fmt.Println("First request - establishing cache")
      response1, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Messages: messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("First response usage: %s\n", response1.Usage.RawJSON())

      messages = append(messages, response1.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the characters in this passage.")))

      // Second request - same configuration (cache hit expected)
      fmt.Println("\nSecond request - same configuration (cache hit expected)")
      response2, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Messages: messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("Second response usage: %s\n", response2.Usage.RawJSON())

      messages = append(messages, response2.ToParam())
      messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Analyze the setting in this passage.")))

      // Third request - different effort level (cache miss expected)
      fmt.Println("\nThird request - different effort level (cache miss expected)")
      response3, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	OutputConfig: anthropic.OutputConfigParam{
      		Effort: anthropic.OutputConfigEffortMedium,
      	},
      	Messages: messages,
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Printf("Third response usage: %s\n", response3.Usage.RawJSON())
      ```
    </Tab>

    <Tab title="Java">
      ```java
      import com.anthropic.models.messages.CacheControlEphemeral;
      // ...
      void main() throws Exception {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
          String bookContent = fetchArticleContent(bookUrl);
          String largeText = bookContent.substring(0, Math.min(10000, bookContent.length()));

          // First request - establishing cache
          IO.println("First request - establishing cache");
          MessageCreateParams params1 = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text(largeText)
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text("Analyze the tone of this passage.")
                      .build())
              ))
              .build();

          Message response1 = client.messages().create(params1);
          IO.println("First response usage: " + response1.usage());

          // Second request - same configuration (cache hit expected)
          IO.println("\nSecond request - same configuration (cache hit expected)");
          MessageCreateParams params2 = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text(largeText)
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text("Analyze the tone of this passage.")
                      .build())
              ))
              .addAssistantMessageOfBlockParams(response1.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the characters in this passage.")
              .build();

          Message response2 = client.messages().create(params2);
          IO.println("Second response usage: " + response2.usage());

          // Third request - different effort level (cache miss expected)
          IO.println("\nThird request - different effort level (cache miss expected)");
          MessageCreateParams params3 = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .outputConfig(OutputConfig.builder()
                  .effort(OutputConfig.Effort.MEDIUM)
                  .build())
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text(largeText)
                      .cacheControl(CacheControlEphemeral.builder().build())
                      .build()),
                  ContentBlockParam.ofText(TextBlockParam.builder()
                      .text("Analyze the tone of this passage.")
                      .build())
              ))
              .addAssistantMessageOfBlockParams(response1.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the characters in this passage.")
              .addAssistantMessageOfBlockParams(response2.content().stream()
                  .map(block -> block.toParam())
                  .collect(java.util.stream.Collectors.toList()))
              .addUserMessage("Analyze the setting in this passage.")
              .build();

          Message response3 = client.messages().create(params3);
          IO.println("Third response usage: " + response3.usage());
      }

      String fetchArticleContent(String url) throws Exception {
          HttpClient client = HttpClient.newHttpClient();
          HttpRequest request = HttpRequest.newBuilder()
              .uri(URI.create(url))
              .build();
          HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
          return response.body();
      }
      ```
    </Tab>

    <Tab title="PHP">
      ```php
      function fetchArticleContent($url) {
          $content = file_get_contents($url);
          $lines = explode("\n", $content);
          $cleanedLines = array_filter(array_map('trim', $lines));
          return implode("\n", $cleanedLines);
      }

      $client = new Client();

      $bookUrl = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt";
      $bookContent = fetchArticleContent($bookUrl);
      $largeText = substr($bookContent, 0, 10000);

      echo "First request - establishing cache\n";
      $response1 = $client->messages->create(
          maxTokens: 16000,
          messages: [[
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => $largeText,
                      'cache_control' => ['type' => 'ephemeral']
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Analyze the tone of this passage.'
                  ]
              ]
          ]],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
      );

      echo "First response usage: " . json_encode($response1->usage) . "\n";

      echo "\nSecond request - same configuration (cache hit expected)\n";
      $response2 = $client->messages->create(
          maxTokens: 16000,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'text',
                          'text' => $largeText,
                          'cache_control' => ['type' => 'ephemeral']
                      ],
                      [
                          'type' => 'text',
                          'text' => 'Analyze the tone of this passage.'
                      ]
                  ]
              ],
              [
                  'role' => 'assistant',
                  'content' => $response1->content
              ],
              [
                  'role' => 'user',
                  'content' => 'Analyze the characters in this passage.'
              ]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
      );

      echo "Second response usage: " . json_encode($response2->usage) . "\n";

      echo "\nThird request - different effort level (cache miss expected)\n";
      $response3 = $client->messages->create(
          maxTokens: 16000,
          messages: [
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'text',
                          'text' => $largeText,
                          'cache_control' => ['type' => 'ephemeral']
                      ],
                      [
                          'type' => 'text',
                          'text' => 'Analyze the tone of this passage.'
                      ]
                  ]
              ],
              [
                  'role' => 'assistant',
                  'content' => $response1->content
              ],
              [
                  'role' => 'user',
                  'content' => 'Analyze the characters in this passage.'
              ],
              [
                  'role' => 'assistant',
                  'content' => $response2->content
              ],
              [
                  'role' => 'user',
                  'content' => 'Analyze the setting in this passage.'
              ]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          outputConfig: ['effort' => 'medium'],
      );

      echo "Third response usage: " . json_encode($response3->usage) . "\n";
      ```
    </Tab>

    <Tab title="Ruby">
      ```ruby
      require "net/http"
      require "uri"

      def fetch_article_content(url)
        uri = URI.parse(url)
        response = Net::HTTP.get_response(uri)
        text = response.body

        lines = text.split("\n").map(&:strip)
        lines.reject(&:empty?).join("\n")
      end

      client = Anthropic::Client.new

      book_url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
      book_content = fetch_article_content(book_url)
      large_text = book_content[0...10000]

      puts "First request - establishing cache"
      response1 = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        messages: [{
          role: "user",
          content: [
            {
              type: "text",
              text: large_text,
              cache_control: { type: "ephemeral" }
            },
            {
              type: "text",
              text: "Analyze the tone of this passage."
            }
          ]
        }]
      )

      puts "First response usage: #{response1.usage}"

      puts "\nSecond request - same configuration (cache hit expected)"
      response2 = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: large_text,
                cache_control: { type: "ephemeral" }
              },
              {
                type: "text",
                text: "Analyze the tone of this passage."
              }
            ]
          },
          {
            role: "assistant",
            content: response1.content
          },
          {
            role: "user",
            content: "Analyze the characters in this passage."
          }
        ]
      )

      puts "Second response usage: #{response2.usage}"

      puts "\nThird request - different effort level (cache miss expected)"
      response3 = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        output_config: {
          effort: "medium"
        },
        messages: [
          {
            role: "user",
            content: [
              {
                type: "text",
                text: large_text,
                cache_control: { type: "ephemeral" }
              },
              {
                type: "text",
                text: "Analyze the tone of this passage."
              }
            ]
          },
          {
            role: "assistant",
            content: response1.content
          },
          {
            role: "user",
            content: "Analyze the characters in this passage."
          },
          {
            role: "assistant",
            content: response2.content
          },
          {
            role: "user",
            content: "Analyze the setting in this passage."
          }
        ]
      )

      puts "Third response usage: #{response3.usage}"
      ```
    </Tab>
  </Tabs>

  Here is the output of the script (you may see slightly different numbers):

  ```text Output wrap
  First request - establishing cache
  First response usage: { cache_creation_input_tokens: 3546, cache_read_input_tokens: 0, input_tokens: 15, output_tokens: 1033 }

  Second request - same configuration (cache hit expected)
  Second response usage: { cache_creation_input_tokens: 0, cache_read_input_tokens: 3546, input_tokens: 1062, output_tokens: 1630 }

  Third request - different effort level (cache miss expected)
  Third response usage: { cache_creation_input_tokens: 3546, cache_read_input_tokens: 0, input_tokens: 2706, output_tokens: 1468 }
  ```

  With the cache breakpoint in the messages array, changing effort from the default `high` to `medium` invalidates it: the third request shows `cache_creation_input_tokens=3546` and `cache_read_input_tokens=0` where the second showed a full cache read.
</Accordion>

### Cost control

You don't set a thinking token budget. Two controls bound cost:

* `max_tokens` is a hard cap on total output for the request, thinking and response text combined. Claude never generates past it. In a tool-use loop, each request in the turn has its own `max_tokens`, so it doesn't bound the whole turn's spend.
* `effort` is soft guidance on how much of that output Claude allocates to thinking. It shapes behavior but doesn't guarantee a token count.

Because thinking counts toward `max_tokens`, set it high enough to leave room for both the reasoning and the answer. A `max_tokens` sized for a response with no thinking is often too small once Claude starts thinking on hard requests.

At `high` effort and above, Claude may think extensively and is more likely to exhaust the budget. If you see [`stop_reason: "max_tokens"`](https://platform.claude.com/docs/en/build-with-claude/thinking-troubleshooting#stopped-at-max-tokens) in responses, you have two remedies:

* Raise `max_tokens` to give the model more room for thinking plus the answer.
* Lower the effort level so Claude thinks less and leaves more of the budget for response text.

Which one is right depends on whether the truncated responses needed the reasoning. If quality on those requests matters, raise the cap; if they were over-thought, lower the effort.

## Pricing

Thinking incurs charges for:

* Tokens Claude uses while thinking (billed as output tokens)
* Thinking blocks from prior assistant turns that remain in context, per the [preservation default](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-block-preservation-by-model): all turns by default on keep-all models, only the last turn elsewhere (billed as input tokens)
* Standard text output tokens

<Note>
  When thinking is active, a specialized system prompt is automatically included to support this feature.
</Note>

What you're billed for is the same regardless of the `display` setting; only what you see changes:

|                             | `display: "summarized"`                              | `display: "omitted"`                                 |
| --------------------------- | ---------------------------------------------------- | ---------------------------------------------------- |
| **Input tokens**            | Tokens in your original request                      | Same as summarized                                   |
| **Output tokens (billed)**  | The full thinking tokens Claude generated internally | Same as summarized                                   |
| **Output tokens (visible)** | The summarized thinking text                         | Zero thinking tokens (the `thinking` field is empty) |
| **Summary generation**      | No charge                                            | Not applicable                                       |

<Warning>
  The billed output token count does **not** match the visible token count in the response. You are billed for the full thinking process, not the thinking content visible in the response.
</Warning>

To see how many billed output tokens were spent on internal reasoning, read `usage.output_tokens_details.thinking_tokens` in the response. This value reflects the raw reasoning the model generated (not the summarized text returned in the body) and is always less than or equal to `output_tokens`. Subtract it from `output_tokens` to approximate the non-reasoning portion of the output. When streaming, this breakdown appears only on the final `message_delta` event.

```json
{
  "usage": {
    "input_tokens": 25,
    "output_tokens": 348,
    "output_tokens_details": {
      "thinking_tokens": 312
    }
  }
}
```

`output_tokens` remains the inclusive, authoritative total used for billing. `output_tokens_details` is a read-only breakdown for observability. For complete pricing information including base rates, cache writes, cache hits, and output tokens, see [Pricing](https://platform.claude.com/docs/en/about-claude/pricing).

## Next steps

<CardGroup cols={3}>
  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/en/build-with-claude/thinking">
    Turn thinking on, read thinking output, and check per-model support.
  </Card>

  <Card title="Thinking in tool and multi-turn workflows" icon="wrench" href="https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows">
    Preserve thinking blocks across tool calls and manage thinking in multi-turn conversations.
  </Card>

  <Card title="Effort" icon="sliders" href="https://platform.claude.com/docs/en/build-with-claude/effort">
    Control how much thinking and output Claude allocates per request.
  </Card>
</CardGroup>
