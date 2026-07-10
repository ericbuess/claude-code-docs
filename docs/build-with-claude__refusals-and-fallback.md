# Refusals and fallback

How Claude Fable 5 returns classifier refusals and how to retry refused requests on a fallback model.

---

Claude Fable 5 includes safety classifiers that can decline a request. When that happens, you receive a normal response, not an error, with `stop_reason: "refusal"`. You can usually still get an answer by sending the same request to another Claude model. This page shows you how to recognize a refusal and how to set up that retry.

Read this page when you build on Claude Fable 5 and want declined requests to fall through to another model automatically. It also applies when you have just seen `"refusal"` in a response and want to know what to do next.

Related pages:

* [Stop reasons and fallback](/docs/en/build-with-claude/handling-stop-reasons): the full list of `stop_reason` values.
* [Fallback credit](/docs/en/build-with-claude/fallback-credit): how refused requests are billed, and how to avoid paying twice for prompt caching on a retry.
* [SDK middleware](/docs/en/cli-sdks-libraries/middleware): the SDK helper that wraps all of this.
* [Fallback and billing cookbook](https://platform.claude.com/cookbook/fable-5-fallback-billing-guide): a worked end-to-end example.

The simplest setup: name a fallback model on the request, and the API handles the retry.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": [{"model": "claude-opus-4-8"}],
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallback '[{"model":"claude-opus-4-8"}]' \
    --beta server-side-fallback-2026-06-01
  ```

  ```python Python
  client = Anthropic()

  client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks=[{"model": "claude-opus-4-8"}],
      betas=["server-side-fallback-2026-06-01"],
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: [{ model: "claude-opus-4-8" }],
    betas: ["server-side-fallback-2026-06-01"]
  });
  ```

  ```csharp C#
  AnthropicClient client = new();

  await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
          Fallbacks = [new(Messages::Model.ClaudeOpus4_8)],
          Betas = [AnthropicBeta.ServerSideFallback2026_06_01],
      }
  );
  ```

  ```go Go
  client := anthropic.NewClient()

  client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: []anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_06_01},
  })
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  client.beta().messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .addFallback(BetaFallbackParam.builder().model(Model.CLAUDE_OPUS_4_8).build())
      .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_06_01)
      .build());
  ```

  ```php PHP
  $client = new Client();

  $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-fable-5',
      fallbacks: [['model' => 'claude-opus-4-8']],
      betas: ['server-side-fallback-2026-06-01'],
  );
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: [{model: "claude-opus-4-8"}],
    betas: ["server-side-fallback-2026-06-01"]
  )
  ```
</CodeGroup>

The sections below cover what a refusal response contains, when to use server-side or client-side fallback, and how each is billed.

## What a refusal looks like

A refusal is a successful HTTP 200 response with `stop_reason: "refusal"`:

```json
{
  "id": "msg_01XFUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "model": "claude-fable-5",
  "content": [],
  "stop_reason": "refusal",
  "stop_details": {
    "type": "refusal",
    "category": "cyber",
    "explanation": "This request was declined because it could enable cyber harm."
  },
  "usage": {
    "input_tokens": 412,
    "output_tokens": 0
  }
}
```

The `stop_details` object explains the decline:

* **`category`:** names the policy area that triggered the classifier.
* **`explanation`:** a human-readable description. The text is not stable, so display it rather than parse it.
* Both fields are `null` when the refusal does not map to a named category. That `null` is a normal, permanent value, not a placeholder.
* `stop_details` itself is `null` for every stop reason other than `refusal`.

| `category`               | What it means                                                                                                                                                                                                                             |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"cyber"`                | The request could enable cyber harm, such as malware or exploit development. Benign cybersecurity work can also trigger this category.                                                                                                    |
| `"bio"`                  | The request could enable biological harm, such as dangerous lab methods. Beneficial life sciences work can also trigger this category.                                                                                                    |
| `"frontier_llm"`         | The request could assist the development of competing AI models, which is restricted under [Anthropic's commercial terms](https://www.anthropic.com/legal/commercial-terms). Benign machine learning work can also trigger this category. |
| `"reasoning_extraction"` | The request asks the model to reproduce its internal reasoning in the response text. To get reasoning in a structured form instead, use [adaptive thinking](/docs/en/build-with-claude/adaptive-thinking).                                |

A refusal can arrive before any output, or mid-stream after partial output. In either case, treat any partial output as incomplete and discard it.

<Note>
  **How refusals are billed:** You are not billed for a refusal that arrives before any output. `content` is empty, token counts appear in `usage` but are not charged, and the request does not count against rate limits. A mid-stream refusal bills the input tokens and the output already streamed at normal rates.
</Note>

## Picking a fallback approach

There are three ways to retry a refused request on another model. The right one depends on where you are running and how much control you need.

| Your situation                                                 | Use                                                                             | Why                                                         |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Claude API or Claude Platform on AWS, simplest setup           | [Server-side fallback](#server-side-fallback)                                   | One request, one response. The API handles the retry.       |
| Any platform, with the TypeScript, Python, Go, Java, or C# SDK | [The SDK middleware](#client-side-fallback)                                     | Configure once on the client. Retries happen automatically. |
| Ruby, PHP, raw HTTP, or custom retry logic                     | Manual retry with [fallback credit](/docs/en/build-with-claude/fallback-credit) | Full control. Fallback credit keeps the cost down.          |

Server-side fallback and the SDK middleware apply fallback credit for you. You only need the [Fallback credit](/docs/en/build-with-claude/fallback-credit) page when you build the retry yourself.

## Server-side fallback

Server-side fallback retries a refused request inside a single API call. You name up to three fallback models, and when Claude Fable 5 declines, the API runs the next model in the chain on the same request. You get back one response that names the model that answered, so your user gets an answer in one round trip.

<Note>
  Server-side fallback is in beta on the Claude API and Claude Platform on AWS. The `fallbacks` parameter is rejected on the [Message Batches API](/docs/en/build-with-claude/batch-processing) and is not available on Amazon Bedrock, Google Cloud, or Microsoft Foundry. On those platforms, use the [SDK middleware](#client-side-fallback) instead.
</Note>

### Making the request

Name the fallback models in the `fallbacks` parameter and send the `server-side-fallback-2026-06-01` beta header.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": [{"model": "claude-opus-4-8"}],
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -c '{stop_reason, model}'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallback '[{"model":"claude-opus-4-8"}]' \
    --beta server-side-fallback-2026-06-01 \
    --format json |
    jq -c '{stop_reason, model}'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks=[{"model": "claude-opus-4-8"}],
      betas=["server-side-fallback-2026-06-01"],
  )

  # A fallback_message entry in usage.iterations means a fallback model ran;
  # pair it with stop_reason to confirm the fallback served the response.
  fallback_ran = any(
      iteration.type == "fallback_message"
      for iteration in response.usage.iterations or []
  )
  served_by_fallback = fallback_ran and response.stop_reason != "refusal"

  print(
      json.dumps(
          {
              "stop_reason": response.stop_reason,
              "model": response.model,
              "served_by_fallback": served_by_fallback,
          }
      )
  )
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: [{ model: "claude-opus-4-8" }],
    betas: ["server-side-fallback-2026-06-01"]
  });

  // A fallback_message entry in usage.iterations means a fallback model ran;
  // pair it with stop_reason to confirm the fallback served the response.
  const { stop_reason, model, usage } = response;
  const servedByFallback =
    (usage.iterations ?? []).some((entry) => entry.type === "fallback_message") &&
    stop_reason !== "refusal";

  console.log(
    JSON.stringify({
      stop_reason,
      model,
      served_by_fallback: servedByFallback
    })
  );
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages =
          [
              new() { Content = "Hello, Claude", Role = Role.User },
          ],
          Fallbacks = [new(Messages::Model.ClaudeOpus4_8)],
          Betas = [AnthropicBeta.ServerSideFallback2026_06_01],
      }
  );

  // A fallback_message entry in usage.iterations means a fallback model ran;
  // pair it with stop_reason to confirm the fallback served the response.
  bool fallbackRan = (response.Usage.Iterations ?? []).Any(iteration =>
      iteration.TryPickFallbackMessageIterationUsage(out _)
  );
  bool servedByFallback =
      fallbackRan && response.StopReason?.Value() != BetaStopReason.Refusal;

  Console.WriteLine(
      JsonSerializer.Serialize(
          new
          {
              stop_reason = response.StopReason?.Raw(),
              model = response.Model.Raw(),
              served_by_fallback = servedByFallback,
          }
      )
  );
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: []anthropic.BetaFallbackParam{
  		{Model: anthropic.ModelClaudeOpus4_8},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_06_01},
  })
  if err != nil {
  	panic(err)
  }

  // A fallback_message entry in usage.iterations means a fallback model ran;
  // pair it with stop_reason to confirm the fallback served the response.
  fallbackRan := slices.ContainsFunc(
  	response.Usage.Iterations,
  	func(iteration anthropic.BetaIterationsUsageItemUnion) bool {
  		_, isFallback := iteration.AsAny().(anthropic.BetaFallbackMessageIterationUsage)
  		return isFallback
  	},
  )
  servedByFallback := fallbackRan && response.StopReason != anthropic.BetaStopReasonRefusal

  summary, err := json.Marshal(struct {
  	StopReason       anthropic.BetaStopReason `json:"stop_reason"`
  	Model            anthropic.Model          `json:"model"`
  	ServedByFallback bool                     `json:"served_by_fallback"`
  }{response.StopReason, response.Model, servedByFallback})
  if err != nil {
  	panic(err)
  }
  fmt.Println(string(summary))
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_FABLE_5)
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .addFallback(BetaFallbackParam.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .build())
          .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_06_01)
          .build()
  );

  // A fallback_message usage entry means a fallback model produced the
  // response; a refusal stop reason means no model served it.
  List<BetaUsage.BetaIterationsUsageItems> iterations =
      response.usage().iterations().orElse(List.of());
  boolean servedByFallback =
      iterations.stream().anyMatch(BetaUsage.BetaIterationsUsageItems::isFallbackMessage)
          && !response.stopReason().map(BetaStopReason.REFUSAL::equals).orElse(false);

  IO.println("""
      {"stop_reason":"%s","model":"%s","served_by_fallback":%b}\
      """.formatted(
          response.stopReason().map(BetaStopReason::asString).orElse("null"),
          response.model().asString(),
          servedByFallback));
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      model: 'claude-fable-5',
      fallbacks: [['model' => 'claude-opus-4-8']],
      betas: ['server-side-fallback-2026-06-01'],
  );

  // A fallback_message entry in usage.iterations means a fallback model ran;
  // pair it with stop_reason to confirm the fallback served the response.
  $iterations = $response->usage->iterations ?? [];
  $servedByFallback = array_any($iterations, fn($entry) => $entry->type === 'fallback_message')
      && $response->stopReason !== 'refusal';

  echo json_encode([
      'stop_reason' => $response->stopReason,
      'model' => $response->model,
      'served_by_fallback' => $servedByFallback,
  ]), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: [{model: "claude-opus-4-8"}],
    betas: ["server-side-fallback-2026-06-01"]
  )

  # A fallback_message entry in usage.iterations means a fallback model ran;
  # pair it with stop_reason to confirm the fallback served the response.
  iterations = response.usage.iterations || []
  served_by_fallback = iterations.any? { it.type == :fallback_message } &&
    response.stop_reason != :refusal

  stop_reason = response.stop_reason
  model = response.model
  puts JSON.generate({stop_reason:, model:, served_by_fallback:})
  ```
</CodeGroup>

A few rules apply to the `fallbacks` list:

* Entries are tried in order. Each must be distinct from the other entries and from the requested model.
* Each entry must be one of the requested model's permitted targets. With the beta header set, that list is published as `allowed_fallback_models` on the model's entry in the [Models API](/docs/en/api/models/list).
* Each entry names a `model` and can override `max_tokens` and `thinking` for that attempt only.
* The request must be valid as a direct request to every model named. If a fallback model does not support a feature the request uses, the API rejects the request up front.
* Only a safety classifier decline triggers the fallback. A rate limit, overload, or server error on the requested model is returned to you as-is.

<Note>
  The beta header must carry exactly the date `2026-06-01`. Under any other `server-side-fallback-*` value, the `fallbacks` parameter is rejected with a 400 error. If you built against an earlier preview of this feature, update the beta header and the request and response shapes together to the ones on this page.
</Note>

### What the response contains

The response looks like any other message, with two additions:

* The top-level `model` field reports the model that produced the returned message, whether that is the requested model or a fallback.

* A `fallback` content block marks each point in `content` where one model's output gives way to the next: `{"type": "fallback", "from": {"model": ...}, "to": {"model": ...}}`.

  * `from.model` echoes the model string you sent when the declining hop is the requested model.
  * `to.model` is always the resolved ID of the model that continues.

On a refusal before any output, the `fallback` block is the first content block:

```json
{
  "id": "msg_01XFUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "model": "claude-opus-4-8",
  "content": [
    {
      "type": "fallback",
      "from": { "model": "claude-fable-5" },
      "to": { "model": "claude-opus-4-8" }
    },
    { "type": "text", "text": "Hi! How can I help you today?" }
  ],
  "stop_reason": "end_turn",
  "stop_details": null,
  "usage": {
    "input_tokens": 412,
    "output_tokens": 264,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "iterations": [
      {
        "type": "message",
        "model": "claude-fable-5",
        "input_tokens": 535,
        "output_tokens": 0,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0
      },
      {
        "type": "fallback_message",
        "model": "claude-opus-4-8",
        "input_tokens": 412,
        "output_tokens": 264,
        "cache_read_input_tokens": 0,
        "cache_creation_input_tokens": 0
      }
    ]
  }
}
```

The `usage.iterations` array records every attempt. A model that declined appears as an ordinary `message` entry, and the model that served the turn appears as a `fallback_message` entry. If every model in the chain declines, the response is the last model's refusal, with a `message` entry for each earlier hop and a `fallback_message` entry for the last.

### Continuing the conversation

On the next turn, send the assistant content back as you received it. After a mid-output fallback, `content` can include block types the declining model produced before the handoff; the table below covers which to keep and which to drop when you echo the turn.

| Block type                                                                             | On the next turn                                                                                                                                                                                                               |
| -------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fallback`                                                                             | Keep it exactly where it appeared. The API uses its position to validate the thinking blocks around it, so a request that echoes thinking blocks from both sides of the boundary is rejected if the block is omitted or moved. |
| `text`                                                                                 | Keep.                                                                                                                                                                                                                          |
| Any block after the final `fallback` block                                             | Keep.                                                                                                                                                                                                                          |
| `thinking`, `redacted_thinking`, or `connector_text` before the final `fallback` block | Drop.                                                                                                                                                                                                                          |
| Client-side `tool_use` before the final `fallback` block                               | Drop.                                                                                                                                                                                                                          |
| `server_tool_use` before the final `fallback` block                                    | Keep when paired with its result. Drop when it has no matching result.                                                                                                                                                         |

<Note>
  A `connector_text` block carries narration text that some tool-using responses include between tool calls.
</Note>

### Streaming

On a streaming request, the retry happens on the same stream, and nothing you have already received is invalidated. What you see depends on when the decline happens.

**When the decline happens before any output:**

* `message_start` names the fallback model, and the `fallback` block is the first content block.
* Because `message_start` waits for the fallback attempt to start, time to first byte includes the declined attempt.

**When the decline happens mid-output:**

* The open content block closes, and the `fallback` block (an ordinary `content_block_start` and `content_block_stop` pair with no deltas) marks the boundary.
* The fallback model continues from the partial output. Only the partial output's `text` blocks are passed to the fallback model as context; other block types remain in `content`.
* `message_start` already named the requested model, so read the serving model from the `fallback` block's `to.model` and from the `fallback_message` entry in the final `message_delta`'s `usage.iterations`.

### Non-streaming responses

On a non-streaming request, a mid-output decline behaves differently: the response omits the declined model's partial output, and the fallback model answers from scratch. The result looks like a decline before any output, with the `fallback` block first. The declined attempt and its output tokens still appear in `usage.iterations`.

<Note>
  **Declines after server tools run:** when a decline fires after server tools (for example, web search or code execution) have already executed within a request, the API returns the refusal instead of advancing to a fallback model. If the `fallback-credit-2026-06-01` header is also set, that refusal carries a credit token redeemable by continuing the partial response, so the completed tool work is not lost. This applies only to server tools iterating within a single request. Conversations that use client-side tools fall back normally.
</Note>

<Accordion title="Sticky routing">
  After a conversation falls back, the API records which model served it. Later requests for that conversation that include `fallbacks` go directly to that fallback model, without running the requested model. This avoids paying for an attempt that would predictably be declined again on every turn.

  A few properties of the routing decision:

  * It is retained for approximately one hour and is scoped to your organization.
  * It is stored as a content hash of the conversation prefix plus the model that served it. The message content itself is not stored.
  * It is best-effort, so your code must handle the requested model being tried again at any time.

  A sticky-served turn carries no `fallback` content block, because no model declined that turn. Identify it by the `fallback_message` entry in `usage.iterations`, the absence of a `message` entry for the requested model, and the response's `model` field.

  In the current release, sticky routing applies only to non-streaming requests. A streaming request that falls back still records the decision for later non-streaming turns.
</Accordion>

<Accordion title="How server-side fallback is billed">
  You pay for the model that actually serves the request. An attempt that declined before producing output costs nothing and consumes no rate limits.

  Each attempt is billed separately, at the rates of the model that ran it. The `usage.iterations` array is the per-attempt record of what you are billed. The top-level `usage` counts describe only the attempt that produced the returned message; tokens from different models are never summed into one field.

  Each attempt that runs counts against its own model's rate limits. If the fallback model is rate limited or overloaded, the fallback attempt is not made and the preceding refusal is returned instead. Size the fallback model's rate limits for the refusal volume you expect, or fallbacks degrade to refusals under load.

  When a fallback attempt is skipped this way, `stop_details.recommended_model` names a model to retry directly. The recommendation is a hint, not a guarantee, and it is `null` when no recommendation is available.
</Accordion>

## Client-side fallback with the SDK middleware

The TypeScript, Python, Go, Java, and C# SDKs include a refusal-fallback middleware. You configure it once on the client with your list of fallback models. Calls through `client.beta.messages` then retry refused requests automatically, on any platform. The middleware also sends the `fallback-credit-2026-06-01` beta header on every request it handles, so retries are repriced without per-request setup.

<Note>
  The refusal-fallback middleware helper is not yet available in the Ruby and PHP SDKs. On those SDKs, implement the detect-and-retry pattern directly.
</Note>

### Setting it up

Pass the middleware to the client constructor, and share one `BetaFallbackState` instance across the requests of a conversation.

<CodeGroup>
  ```bash cURL
  # The refusal-fallback middleware is an SDK feature. See the
  # server-side fallback section for the equivalent single-request approach,
  # or the fallback credit page for the raw HTTP retry pattern.
  ```

  ```bash CLI
  # The refusal-fallback middleware is an SDK feature. See the
  # server-side fallback section for the equivalent single-request approach,
  # or the fallback credit page for the raw HTTP retry pattern.
  ```

  ```python Python
  # On a refusal, the middleware retries on the listed fallback model and
  # automatically sends the fallback-credit beta header on every request it handles.
  client = Anthropic(
      middleware=[BetaRefusalFallbackMiddleware([{"model": "claude-opus-4-8"}])],
  )

  state = BetaFallbackState()  # pins follow-ups to the model that accepted

  # Streaming: on a refusal the middleware retries on the fallback model and
  # splices its events onto the open stream.
  with (
      state,
      client.beta.messages.stream(
          max_tokens=1024,
          model="claude-fable-5",
          messages=[{"role": "user", "content": "Hello, Claude"}],
      ) as stream,
  ):
      for event in stream:
          if event.type == "text":
              print(event.text, end="", flush=True)
      final_message = stream.get_final_message()
  print(f"\nserved by: {final_message.model}")

  # Non-streaming: reusing the state keeps the conversation pinned.
  with state:
      message = client.beta.messages.create(
          max_tokens=1024,
          model="claude-fable-5",
          messages=[{"role": "user", "content": "Hello, Claude"}],
      )
  print(f"served by: {message.model}")
  ```

  ```typescript TypeScript
  // On a refusal, the middleware retries the request down the fallback chain.
  // It sends the fallback-credit beta header on every request it handles.
  const client = new Anthropic({
    middleware: [betaRefusalFallbackMiddleware([{ model: "claude-opus-4-8" }])]
  });

  // Share one state across the conversation so follow-up requests stay
  // pinned to the model that accepted.
  const fallbackState = new BetaFallbackState();

  // Streaming: on a refusal the middleware splices the fallback model's
  // events onto the still-open stream.
  const stream = client.beta.messages.stream(
    {
      model: "claude-fable-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { fallbackState }
  );
  stream.on("text", (text) => process.stdout.write(text));

  const finalMessage = await stream.finalMessage();
  console.log("\nserved by:", finalMessage.model);

  // Non-streaming: reusing the state keeps the conversation pinned to the model that accepted.
  const message = await client.beta.messages.create(
    {
      model: "claude-fable-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { fallbackState }
  );
  console.log("served by:", message.model);
  ```

  ```csharp C#
  // On a refusal, the handler retries on the listed fallback model and
  // automatically sends the fallback-credit beta header on every request it handles.
  AnthropicClient client = new()
  {
      Handlers =
      [
          new BetaRefusalFallbackHandler { Fallbacks = [new(Messages::Model.ClaudeOpus4_8)] },
      ],
  };

  // Pins follow-up requests sharing this state to the model that accepted.
  BetaFallbackState fallbackState = BetaFallbackState.Create();

  MessageCreateParams parameters = new()
  {
      Model = Messages::Model.ClaudeFable5,
      MaxTokens = 1024,
      Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
  };

  // Streaming: if the stream ends in a refusal, the handler splices the fallback
  // model's events onto the still-open stream.
  BetaMessageContentAggregator aggregator = new();
  using (fallbackState.Use())
  {
      var responseUpdates = client.Beta.Messages.CreateStreaming(parameters);
      await foreach (BetaRawMessageStreamEvent rawEvent in responseUpdates.CollectAsync(aggregator))
      {
          if (
              rawEvent.TryPickContentBlockDelta(out var deltaEvent)
              && deltaEvent.Delta.TryPickText(out var textDelta)
          )
          {
              Console.Write(textDelta.Text);
          }
      }
  }
  BetaMessage streamedMessage = aggregator.Message();
  Console.WriteLine($"\nserved by: {streamedMessage.Model.Raw()}");

  // Non-streaming: reusing the state keeps the conversation pinned to the model that accepted.
  using (fallbackState.Use())
  {
      BetaMessage message = await client.Beta.Messages.Create(parameters);
      Console.WriteLine($"served by: {message.Model.Raw()}");
  }
  ```

  ```go Go
  ctx := context.Background()

  // The middleware retries a refused request on each fallback model in
  // turn, and opts requests into the fallback-credit beta automatically.
  client := anthropic.NewClient(
  	option.WithMiddleware(betafallback.BetaRefusalFallbackMiddleware(
  		[]anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  	)),
  )

  // One state per conversation: requests sharing it stay pinned to the
  // model that accepted, so a follow-up never re-asks a model that refused.
  state := &betafallback.BetaFallbackState{}
  conversation := betafallback.WithBetaFallbackState(state)

  params := anthropic.BetaMessageNewParams{
  	MaxTokens: 1024,
  	Model:     anthropic.ModelClaudeFable5,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  }

  // Streaming: on a refusal the middleware retries in place, splicing the
  // fallback model's events onto the open stream as one continuous message.
  stream := client.Beta.Messages.NewStreaming(ctx, params, conversation)
  var streamed anthropic.BetaMessage
  for stream.Next() {
  	event := stream.Current()
  	if err := streamed.Accumulate(event); err != nil {
  		panic(err)
  	}
  	switch eventVariant := event.AsAny().(type) {
  	case anthropic.BetaRawContentBlockDeltaEvent:
  		if textDelta, ok := eventVariant.Delta.AsAny().(anthropic.BetaTextDelta); ok {
  			fmt.Print(textDelta.Text)
  		}
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }
  fmt.Println("\nserved by:", streamed.Model)

  // Non-streaming: the shared state pins this follow-up to the model that
  // served the streamed turn.
  message, err := client.Beta.Messages.New(ctx, params, conversation)
  if err != nil {
  	panic(err)
  }
  fmt.Println("served by:", message.Model)
  ```

  ```java Java
  // The interceptor retries refused requests on the fallback model. It automatically
  // adds the fallback-credit beta header to every request it handles.
  AnthropicClient client = AnthropicOkHttpClient.builder()
      .fromEnv()
      .addInterceptor(BetaRefusalFallbackInterceptor.builder()
          .addFallback(Model.CLAUDE_OPUS_4_8)
          .build())
      .build();

  // Share one state across requests so follow-ups stay pinned to the model that accepted.
  BetaFallbackState state = BetaFallbackState.create();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024)
      .addUserMessage("Hello, Claude")
      .build();

  // Streaming: on a refusal, the fallback model's events are spliced onto the open stream.
  BetaMessageAccumulator accumulator = BetaMessageAccumulator.create();
  try (StreamResponse<BetaRawMessageStreamEvent> streamResponse = client.beta()
          .messages()
          .createStreaming(params, RequestOptions.builder().fallbackState(state).build())) {
      streamResponse.stream()
          .peek(accumulator::accumulate)
          .forEach(event -> event.contentBlockDelta()
              .flatMap(deltaEvent -> deltaEvent.delta().text())
              .ifPresent(textDelta -> IO.print(textDelta.text())));
  }
  IO.println("\nserved by: " + accumulator.message().model().asString());

  // Non-streaming: reusing the same state keeps the conversation pinned.
  BetaMessage message = client.beta()
      .messages()
      .create(params, RequestOptions.builder().fallbackState(state).build());
  IO.println("served by: " + message.model().asString());
  ```

  ```php PHP
  // The refusal-fallback middleware is not currently available in the PHP SDK.
  // See the server-side fallback section for the equivalent single-request
  // approach, or the fallback credit page for the underlying retry pattern.
  ```

  ```ruby Ruby
  # The refusal-fallback middleware is not currently available in the Ruby SDK.
  # See the server-side fallback section for the equivalent single-request
  # approach, or the fallback credit page for the underlying retry pattern.
  ```
</CodeGroup>

### How it behaves

* Retries walk your fallback list in order. A fallback model that itself refuses passes the request to the next entry.
* The original refusal response is returned only when every model in the list has declined. The middleware does not raise an error for it.
* [Thinking blocks from Claude Fable 5](/docs/en/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) are handled for you: the middleware strips them from the retry and manages them in conversation history on later requests.
* Responses served through the middleware include a `fallback` content block at each model boundary, the same as server-side fallback responses. The middleware manages those blocks for you on later requests.
* The model that accepted is recorded in `BetaFallbackState`, so follow-up requests that share the state stay pinned to it rather than re-asking a model that refused.

<Note>
  The middleware and the server-side `fallbacks` parameter do the same job. Configure one or the other, never both on the same request. To send a server-side `fallbacks` request from an application that installs the middleware, use a separate client instance without it.
</Note>

<Accordion title="Writing the retry yourself">
  On Ruby, PHP, or raw HTTP, implement the pattern the middleware wraps:

  <Steps>
    <Step title="Detect the refusal">
      Check the response for `stop_reason: "refusal"`.
    </Step>

    <Step title="Re-send on a fallback model">
      Send the same request with `model` set to a fallback model, such as Claude Opus 4.8. A request that Claude Fable 5's classifiers decline can normally be served by another model. How you handle the conversation history depends on whether you redeem a [fallback credit](/docs/en/build-with-claude/fallback-credit):

      * **Not redeeming a credit:** you can first strip the [thinking blocks from Claude Fable 5](/docs/en/build-with-claude/adaptive-thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) out of the conversation history. Other models ignore them, and stripping keeps cross-model requests minimal.
      * **Redeeming a credit:** send the body unchanged, because redemption requires an exact match.
    </Step>

    <Step title="Stay on the fallback model">
      For multi-turn conversations, keep using the fallback model for subsequent turns rather than switching back.
    </Step>
  </Steps>

  A manual retry writes the fallback model's prompt cache from scratch, which costs more than reading an existing cache. [Fallback credit](/docs/en/build-with-claude/fallback-credit) refunds that cost; redeem it on every retry you build yourself.
</Accordion>

## Refusals in Message Batches

A refused request in a [Message Batch](/docs/en/build-with-claude/batch-processing) comes back as `result.type: "succeeded"` with `stop_reason: "refusal"`. The `stop_details` field may be `null` on batch results, so detect refusals by checking `stop_reason` directly.

Server-side fallback is not available for batches (a batch request that includes `fallbacks` produces a per-item errored result). To retry refused batch items:

1. Collect the refused items from the results.
2. Strip Claude Fable 5's thinking blocks from any multi-turn histories.
3. Resubmit them on a fallback model as a new batch or as direct requests.

## Common pitfalls

* **Retry on a different model.** Re-sending a refused request to the same model usually earns another refusal. Point the retry at the fallback model.
* **Budget retries per request, not per turn or per session.** A single turn can produce several refusals, for example an agent plus its sub-agents.
* **Configure fallback on every request path.** Retry handlers, error-recovery branches, and background workers all need it. A handler that re-issues a request without fallback loses the protection on exactly the requests most likely to need it.
* **Give sub-agent calls their own fallback.** The `fallbacks` parameter does not propagate into model calls made from inside tool execution.
* **Make fallback a property of the request, not of ambient state.** A shared flag, cached config value, or global toggle can drift out of sync and silently leave a request unprotected. When you cannot confirm fallback is active, configure it rather than assume it is on.
* **Instrument refusals as their own signal.** A refusal is an HTTP 200, so monitoring built on error rates or 5xx responses never sees it. Emit one event per refusal and one per fallback-served response (the `fallback_message` entry in `usage.iterations` marks the latter), then alert on the gap between the two counts.
* **Branch on `stop_reason`, not on `stop_details` or `content`.** `stop_details` is informational and can be `null` on a refusal. Check for `stop_reason` equal to `"refusal"` directly.

## Next steps

<CardGroup>
  <Card title="Fallback credit" icon="scales" href="/docs/en/build-with-claude/fallback-credit">
    Avoid paying the prompt-cache cost twice when you build the retry yourself.
  </Card>

  <Card title="Stop reasons and fallback" icon="code" href="/docs/en/build-with-claude/handling-stop-reasons">
    Every `stop_reason` value and how to handle it.
  </Card>

  <Card title="SDK middleware" icon="settings" href="/docs/en/cli-sdks-libraries/middleware">
    How SDK middleware works, including the refusal-fallback helper.
  </Card>

  <Card title="Migration guide" icon="arrow-right" href="/docs/en/about-claude/models/migration-guide">
    Move an existing application to Claude Fable 5.
  </Card>
</CardGroup>
