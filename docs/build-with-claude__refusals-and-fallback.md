---
title: Refusals and fallback
url: https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback
description: How Claude Fable 5 and Claude Opus 5 return classifier refusals and how to retry refused requests on a fallback model.
---

Claude Fable 5 and Claude Opus 5 include safety classifiers that can decline a request. When that happens, you receive a normal response, not an error, with `stop_reason: "refusal"`. You can usually still get an answer by sending the same request to another Claude model. This page shows you how to recognize a refusal and how to set up that retry.

Read this page when you build on Claude Fable 5 or Claude Opus 5 and want declined requests to fall through to another model automatically. It also applies when you have just seen `"refusal"` in a response and want to know what to do next.

Related pages:

* [Stop reasons and fallback](https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons): the full list of `stop_reason` values.
* [Fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit): how refused requests are billed, and how to avoid paying twice for prompt caching on a retry.
* [SDK middleware](https://platform.claude.com/docs/en/cli-sdks-libraries/middleware): the SDK helper that wraps all of this.
* [Fallback and billing cookbook](https://platform.claude.com/cookbook/fable-5-fallback-billing-guide): a worked end-to-end example.

The simplest setup, in beta on the Claude API: set `fallbacks` to `"default"`, and the API retries a declined request on the fallback model Anthropic recommends for its refusal category. For categories with no recommended fallback, the refusal stands.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": "default",
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.model'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallbacks default \
    --beta server-side-fallback-2026-07-01 \
    --transform model --raw-output
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks="default",
      betas=["server-side-fallback-2026-07-01"],
  )
  print(response.model)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: "default",
    betas: ["server-side-fallback-2026-07-01"]
  });
  console.log(response.model);
  ```

  ```csharp C#
  AnthropicClient client = new();

  BetaMessage response = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
          Fallbacks = new Default(),
          Betas = [AnthropicBeta.ServerSideFallback2026_07_01],
      }
  );

  Console.WriteLine(response.Model.Raw());
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: anthropic.BetaFallbacksParamOfDefault(),
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(response.Model)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .fallbacksDefault()
      .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
      .build());

  IO.println(response.model().asString());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      fallbacks: 'default',
      betas: ['server-side-fallback-2026-07-01'],
  );

  echo $response->model, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: :default,
    betas: ["server-side-fallback-2026-07-01"]
  )

  puts response.model
  ```
</CodeGroup>

The following sections cover what a refusal response contains, when to use server-side or client-side fallback, and how each is billed.

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
| `"reasoning_extraction"` | The request asks the model to reproduce its internal reasoning in the response text. To get reasoning in a structured form instead, use [adaptive thinking](https://platform.claude.com/docs/en/build-with-claude/thinking).              |
| `"general_harms"`        | The request could be related to an area that was determined as harmful. Benign work might sometimes trigger this category.                                                                                                                |

A refusal can arrive before any output, or mid-stream after partial output. In either case, treat any partial output as incomplete and discard it.

<Note>
  **How refusals are billed:** You are not billed for a refusal that arrives before any output. `content` is empty, and token counts appear in `usage` but are not charged. The request still counts against your rate limits. A mid-stream refusal bills the input tokens and the output already streamed at normal rates.
</Note>

## Picking a fallback approach

There are three ways to retry a refused request on another model. The right one depends on where you are running and how much control you need.

| Your situation                       | Use                                                                                                                      | Why                                                         |
| ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| Claude API, simplest setup           | [Server-side fallback](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback) | One request, one response. The API handles the retry.       |
| Any platform, using an Anthropic SDK | [The SDK middleware](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback)   | Configure once on the client. Retries happen automatically. |
| Raw HTTP or custom retry logic       | Manual retry with [fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit)               | Full control. Fallback credit keeps the cost down.          |

Server-side fallback and the SDK middleware apply fallback credit for you. You only need the [Fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit) page when you build the retry yourself.

## Server-side fallback

Server-side fallback retries a refused request inside a single API call. In the default mode, when the primary model declines and the refusal category has a recommended fallback, the API runs the same request on the model Anthropic recommends for that category. You can instead name up to three fallback models of your own (below). Either way, you get back one response that names the model that answered, so your user gets an answer in one round trip.

<Note>
  Server-side fallback is in beta on the Claude API. The `fallbacks` parameter is not supported on the [Message Batches API](https://platform.claude.com/docs/en/build-with-claude/batch-processing) (a batch item that includes it comes back as an errored result) and is not available on Amazon Bedrock, Google Cloud, or Microsoft Foundry. On those platforms, use [client-side fallback with the SDK middleware](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead.
</Note>

### Making the request

Set the `fallbacks` parameter to the string `"default"` and send the `server-side-fallback-2026-07-01` beta header. The API then applies the requested model's server-defined default routing, which selects a recommended fallback model based on the refusal category the classifier reports, so refused requests are served without you maintaining a model list as recommendations change.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": "default",
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' |
    jq -c '{
      stop_reason,
      model,
      # A fallback_message entry in usage.iterations means a fallback model ran;
      # pair it with stop_reason to confirm the fallback served the response.
      served_by_fallback: (
        any(.usage.iterations[]?; .type == "fallback_message")
        and .stop_reason != "refusal"
      )
    }'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallbacks default \
    --beta server-side-fallback-2026-07-01 \
    --format json |
    jq -c '{
      stop_reason,
      model,
      # A fallback_message entry in usage.iterations means a fallback model ran;
      # pair it with stop_reason to confirm the fallback served the response.
      served_by_fallback: (
        any(.usage.iterations[]?; .type == "fallback_message")
        and .stop_reason != "refusal"
      )
    }'
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks="default",
      betas=["server-side-fallback-2026-07-01"],
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
    fallbacks: "default",
    betas: ["server-side-fallback-2026-07-01"]
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
          Fallbacks = new Default(),
          Betas = [AnthropicBeta.ServerSideFallback2026_07_01],
      }
  );

  // A fallback_message entry in usage.iterations means a fallback model ran;
  // pair it with stop_reason to confirm the fallback served the response.
  bool fallbackRan = (response.Usage.Iterations ?? []).Any(iteration =>
      iteration.TryPickBetaFallbackMessageIterationUsage(out _)
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
  	Fallbacks: anthropic.BetaFallbacksParamOfDefault(),
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
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
          .fallbacksDefault()
          .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
          .build()
  );

  // A fallback_message usage entry means a fallback model produced the
  // response; a refusal stop reason means no model served it.
  List<BetaUsage.Iteration> iterations =
      response.usage().iterations().orElse(List.of());
  boolean servedByFallback =
      iterations.stream().anyMatch(BetaUsage.Iteration::isFallbackMessage)
          && response.stopReason().filter(BetaStopReason.REFUSAL::equals).isEmpty();

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
      fallbacks: 'default',
      betas: ['server-side-fallback-2026-07-01'],
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
    fallbacks: :default,
    betas: ["server-side-fallback-2026-07-01"]
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

Anthropic sets safeguards for each model individually and for each policy category, in line with the model's capability: depending on the category, a flagged request may fall back to a less capable model or be declined. The `"default"` mode encodes these per-model, per-category recommendations for you, so a refused request is retried on the model Anthropic recommends for that category. Fallbacks are visible either way: the response names the model that served it, and the `fallback` content block marks the handoff.

The routing is applied server-side and is not published per model on the [Models API](https://platform.claude.com/docs/en/api/models/list). To see which model served a refused request, check the response's top-level `model` field and look for a `fallback_message` entry in `usage.iterations`, as this page's samples do.

Only a safety classifier decline triggers the fallback. A rate limit, overload, or server error on the requested model is returned to you as-is.

<Note>
  The beta header must carry exactly the date `2026-07-01`, which supports both `"default"` and the explicit-list form below, or `2026-06-01`, which accepts only the explicit-list form. Under any other `server-side-fallback-*` value, the `fallbacks` parameter is rejected with a 400 error. If you built against an earlier preview of this feature, update the beta header and the request and response shapes together to the ones on this page.
</Note>

### Naming your own fallback models

Instead of default routing, you can set `fallbacks` to a list of up to three models. When the requested model declines, the API runs the next model in the chain on the same request. Use this form when you want to control exactly which models serve refused requests, such as pinning a model your application has qualified.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: server-side-fallback-2026-07-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "fallbacks": [{"model": "claude-opus-4-8"}],
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }' | jq -r '.model'
  ```

  ```bash CLI
  ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --fallbacks '[{"model":"claude-opus-4-8"}]' \
    --beta server-side-fallback-2026-07-01 \
    --transform model --raw-output
  ```

  ```python Python
  client = Anthropic()

  response = client.beta.messages.create(
      model="claude-fable-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello, Claude"}],
      fallbacks=[{"model": "claude-opus-4-8"}],
      betas=["server-side-fallback-2026-07-01"],
  )
  print(response.model)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    fallbacks: [{ model: "claude-opus-4-8" }],
    betas: ["server-side-fallback-2026-07-01"]
  });
  console.log(response.model);
  ```

  ```csharp C#
  AnthropicClient client = new();

  BetaMessage response = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeFable5,
          MaxTokens = 1024,
          Messages = [new() { Content = "Hello, Claude", Role = Role.User }],
          Fallbacks = new([new(Messages::Model.ClaudeOpus4_8)]),
          Betas = [AnthropicBeta.ServerSideFallback2026_07_01],
      }
  );

  Console.WriteLine(response.Model.Raw());
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.Background(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeFable5,
  	MaxTokens: 1024,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  	Fallbacks: anthropic.BetaFallbacksParamUnion{
  		OfBetaFallbackArray: []anthropic.BetaFallbackParam{{Model: anthropic.ModelClaudeOpus4_8}},
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaServerSideFallback2026_07_01},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(response.Model)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(MessageCreateParams.builder()
      .model(Model.CLAUDE_FABLE_5)
      .maxTokens(1024L)
      .addUserMessage("Hello, Claude")
      .fallbacksOfFallbackParams(List.of(BetaFallbackParam.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .build()))
      .addBeta(AnthropicBeta.SERVER_SIDE_FALLBACK_2026_07_01)
      .build());

  IO.println(response.model().asString());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      fallbacks: [['model' => 'claude-opus-4-8']],
      betas: ['server-side-fallback-2026-07-01'],
  );

  echo $response->model, PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    fallbacks: [{model: "claude-opus-4-8"}],
    betas: ["server-side-fallback-2026-07-01"]
  )

  puts response.model
  ```
</CodeGroup>

A few rules apply to the `fallbacks` list:

* Entries are tried in order. Each must be distinct from the other entries and from the requested model.
* Each entry must be one of the requested model's permitted targets. With the beta header set, that list is published as `allowed_fallback_models` on the model's entry in the [Models API](https://platform.claude.com/docs/en/api/models/list).
* Each entry names a `model` and can override `max_tokens`, `thinking`, `output_config`, and `speed` for that attempt only.
* The request must be valid as a direct request to every model named. If a fallback model does not support a feature the request uses, the API rejects the request up front.
* As with the default mode, only a safety classifier decline triggers the fallback. A rate limit, overload, or server error on the requested model is returned to you as-is.

The explicit-list form also works under the `server-side-fallback-2026-06-01` beta header; the `"default"` mode does not.

The response has the same shape in both modes: the model that served the turn appears in the top-level `model` field, a `fallback` content block marks the handoff, and `usage.iterations` records each attempt.

### What the response contains

The response looks like any other message, with two additions:

* The top-level `model` field reports the model that produced the returned message, whether that is the requested model or a fallback.

* A `fallback` content block marks each point in `content` where one model's output gives way to the next: `{"type": "fallback", "from": {"model": ...}, "to": {"model": ...}}`.

  * `from.model` echoes the model string you sent when the declining hop is the requested model.
  * `to.model` is always the resolved ID of the model that continues.

On a refusal before any output, the `fallback` block is the first content block. For example, when default routing selects Claude Opus 4.8 for the refusal's category:

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

On the next turn, send the assistant content back as you received it. After a mid-output fallback, `content` can include block types the declining model produced before the handoff; the following table covers which to keep and which to drop when you echo the turn.

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
  **Declines during tool use:** completed tool work does not block fallback. When a decline fires after server tools (for example, web search or code execution) have finished executing within a request, the fallback attempt proceeds: the completed tool results carry over, and the fallback model can keep invoking server tools. The one case that does not retry is a streaming decline that fires while a tool-use block of any type (a client tool, a server tool, or an MCP tool call) is still open on the stream: that refusal is returned directly, and if the `fallback-credit-2026-07-01` header is set it still carries a credit token redeemable by continuing the partial response. Non-streaming requests are unaffected; the API clears the partial work and retries before responding.
</Note>

<Accordion title="Sticky routing">
  After a conversation falls back, the API records which model served it. Later requests for that conversation that include `fallbacks` go directly to that fallback model, without running the requested model. This avoids paying for an attempt that would predictably be declined again on every turn.

  A few properties of the routing decision:

  * It is retained for approximately 1 hour and is scoped to your organization.
  * It is stored as a content hash of the conversation prefix plus the model that served it. The message content itself is not stored.
  * It is best-effort, so your code must handle the requested model being tried again at any time.

  A sticky-served turn carries no `fallback` content block, because no model declined that turn. Identify it by the `fallback_message` entry in `usage.iterations`, the absence of a `message` entry for the requested model, and the response's `model` field.

  Sticky routing applies to both streaming and non-streaming requests. On a streaming request, the routing decision is made before the stream opens, so the `message_start` event's `model` field already carries the fallback model's ID.
</Accordion>

<Accordion title="How server-side fallback is billed">
  You pay for the model that actually serves the request. An attempt that declined before producing output is not billed: its tokens are reported on its `usage.iterations` entry but not charged. Declined attempts still count against rate limits (see below).

  Each attempt is billed separately, at the rates of the model that ran it. The `usage.iterations` array is the per-attempt record of what you are billed. The top-level `usage` counts describe only the attempt that produced the returned message; tokens from different models are never summed into one field.

  Each attempt that runs counts against its own model's rate limits. If the fallback model is rate limited or overloaded, the fallback attempt is not made and the preceding refusal is returned instead. Size the fallback model's rate limits for the refusal volume you expect, or fallbacks degrade to refusals under load.

  When a fallback attempt is skipped this way, `stop_details.recommended_model` names a model to retry directly. The recommendation is a hint, not a guarantee, and it is `null` when no recommendation is available.
</Accordion>

## Client-side fallback with the SDK middleware

Every Anthropic SDK includes a refusal-fallback middleware. You configure it once on the client with your list of fallback models. Calls through `client.beta.messages` then retry refused requests automatically, on any platform. The middleware also sends the `fallback-credit-2026-07-01` beta header on every request it handles, so retries are repriced without per-request setup.

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
  from anthropic import Anthropic, BetaFallbackState, BetaRefusalFallbackMiddleware

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
      for text in stream.text_stream:
          print(text, end="", flush=True)
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
  import { BetaFallbackState, betaRefusalFallbackMiddleware } from "@anthropic-ai/sdk";

  // On a refusal, the middleware retries on the listed fallback model and
  // automatically sends the fallback-credit beta header on every request it handles.
  const client = new Anthropic({
    middleware: [betaRefusalFallbackMiddleware([{ model: "claude-opus-4-8" }])]
  });

  // Share one state across the conversation so follow-up requests stay
  // pinned to the model that accepted.
  const fallbackState = new BetaFallbackState();

  // Streaming: on a refusal the middleware retries on the fallback model and
  // splices its events onto the open stream.
  const stream = client.beta.messages
    .stream(
      {
        max_tokens: 1024,
        model: "claude-fable-5",
        messages: [{ role: "user", content: "Hello, Claude" }]
      },
      { fallbackState }
    )
    .on("text", (text) => process.stdout.write(text));

  const finalMessage = await stream.finalMessage();
  console.log("\nserved by:", finalMessage.model);

  // Non-streaming: reusing the state keeps the conversation pinned.
  const message = await client.beta.messages.create(
    {
      max_tokens: 1024,
      model: "claude-fable-5",
      messages: [{ role: "user", content: "Hello, Claude" }]
    },
    { fallbackState }
  );
  console.log("served by:", message.model);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Helpers;
  using Anthropic.Models.Beta.Messages;
  using Messages = Anthropic.Models.Messages;

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
  import (
  // ...
  	"github.com/anthropics/anthropic-sdk-go/lib/betafallback"
  // ...
  )

  func main() {
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
  	defer stream.Close()
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
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.RequestOptions;
  import com.anthropic.core.http.StreamResponse;
  import com.anthropic.helpers.BetaFallbackState;
  import com.anthropic.helpers.BetaMessageAccumulator;
  import com.anthropic.helpers.BetaRefusalFallbackInterceptor;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaRawMessageStreamEvent;
  import com.anthropic.models.beta.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
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
  }
  ```

  ```php PHP
  use Anthropic\Beta\Messages\BetaRawContentBlockDeltaEvent;
  use Anthropic\Beta\Messages\BetaTextDelta;
  use Anthropic\Client;
  use Anthropic\Lib\Middleware\BetaFallbackState;
  use Anthropic\Lib\Middleware\RefusalFallbackMiddleware;
  use Anthropic\Lib\Streaming\MessageAccumulator;

  // Configure the fallback chain once. On a refusal, the middleware retries the
  // request down the chain and sends the fallback-credit beta header for you.
  $client = new Client(
      requestOptions: [
          'middleware' => [new RefusalFallbackMiddleware([['model' => 'claude-opus-4-8']])],
      ],
  );

  // Share one state across the conversation so follow-up requests stay pinned
  // to the model that accepted.
  $state = new BetaFallbackState();

  // Streaming: on a refusal the middleware splices the fallback model's events
  // onto the still-open stream. The accumulator's model is the serving model.
  $stream = $client->beta->messages->createStream(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      requestOptions: ['fallbackState' => $state],
  );
  $accumulator = MessageAccumulator::forBetaMessages();
  foreach ($stream as $event) {
      $accumulator->accumulate($event);
      if ($event instanceof BetaRawContentBlockDeltaEvent
          && $event->delta instanceof BetaTextDelta) {
          echo $event->delta->text;
      }
  }
  echo "\nserved by: {$accumulator->message()->model}\n";

  // Non-streaming: same middleware. Reusing the state keeps the conversation
  // pinned to the model that accepted.
  $message = $client->beta->messages->create(
      model: 'claude-fable-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello, Claude']],
      requestOptions: ['fallbackState' => $state],
  );
  echo "served by: {$message->model}\n";
  ```

  ```ruby Ruby
  # On a refusal, the middleware retries the request down the fallback chain.
  # It sends the fallback-credit beta header on every request it handles.
  client = Anthropic::Client.new(
    middleware: [Anthropic::BetaRefusalFallbackMiddleware.new([{model: "claude-opus-4-8"}])]
  )

  # Share one state across the conversation so follow-up requests stay
  # pinned to the model that accepted.
  state = Anthropic::BetaFallbackState.new

  # Streaming: on a refusal the middleware splices the fallback model's
  # events onto the still-open stream.
  stream = client.beta.messages.stream(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {fallback_state: state}
  )
  stream.text.each { print it }
  puts "\nserved by: #{stream.accumulated_message.model}"

  # Non-streaming: reusing the state keeps the conversation pinned to the model that accepted.
  message = client.beta.messages.create(
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}],
    request_options: {fallback_state: state}
  )
  puts "served by: #{message.model}"
  ```
</CodeGroup>

### How it behaves

* Retries walk your fallback list in order. A fallback model that itself refuses passes the request to the next entry.
* When every model in the list has declined, the middleware returns the final refusal (the last model's refusal response) rather than raising an error.
* [Thinking blocks from Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) pass through unchanged: each retry re-sends your original request body, and the only blocks the middleware removes from conversation history on later requests are the `fallback` boundary blocks it added itself.
* Responses served through the middleware include a `fallback` content block at each model boundary, the same as server-side fallback responses. The middleware manages those blocks for you on later requests.
* The model that accepted is recorded in `BetaFallbackState`, so follow-up requests that share the state stay pinned to it rather than re-asking a model that refused.

<Note>
  The middleware and the server-side `fallbacks` parameter do the same job. Configure one or the other, never both on the same request. To send a server-side `fallbacks` request from an application that installs the middleware, use a separate client instance without it.
</Note>

<Accordion title="Writing the retry yourself">
  Over raw HTTP or with custom retry logic, implement the pattern the middleware wraps:

  <Steps>
    <Step title="Detect the refusal">
      Check the response for `stop_reason: "refusal"`.
    </Step>

    <Step title="Re-send on a fallback model">
      Send the same request with `model` set to a fallback model, such as Claude Opus 4.8. A request that Claude Fable 5's classifiers decline can normally be served by another model. How you handle the conversation history depends on whether you redeem a [fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit):

      * **Not redeeming a credit:** you can first strip the [thinking blocks from Claude Fable 5](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-output-on-claude-fable-5-and-claude-mythos-5) out of the conversation history. Other models ignore them, and stripping keeps cross-model requests minimal.
      * **Redeeming a credit:** send the body unchanged, because redemption requires an exact match.
    </Step>

    <Step title="Stay on the fallback model">
      For multi-turn conversations, keep using the fallback model for subsequent turns rather than switching back.
    </Step>
  </Steps>

  A manual retry writes the fallback model's prompt cache from scratch, which costs more than reading an existing cache. [Fallback credit](https://platform.claude.com/docs/en/build-with-claude/fallback-credit) refunds that cost; redeem it on every retry you build yourself.
</Accordion>

## Refusals in Message Batches

A refused request in a [Message Batch](https://platform.claude.com/docs/en/build-with-claude/batch-processing) comes back as `result.type: "succeeded"` with `stop_reason: "refusal"`. Batch results carry the same `stop_details` object as synchronous responses, so you can detect refusals through either `stop_reason` or `stop_details.type`. One difference: batch refusals don't mint fallback credits, so `stop_details` on a batch result never includes a `fallback_credit_token`.

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
* **Branch on `stop_reason` or `stop_details.type`, not on `content` or the inner `stop_details` fields.** The `stop_details` object is always present on a refusal, but its `category` and `explanation` fields can be `null`. Check for `stop_reason` equal to `"refusal"` directly.

## Next steps

<CardGroup>
  <Card title="Fallback credit" icon="scales" href="https://platform.claude.com/docs/en/build-with-claude/fallback-credit">
    Avoid paying the prompt-cache cost twice when you build the retry yourself.
  </Card>

  <Card title="Stop reasons and fallback" icon="code" href="https://platform.claude.com/docs/en/build-with-claude/handling-stop-reasons">
    Every `stop_reason` value and how to handle it.
  </Card>

  <Card title="SDK middleware" icon="settings" href="https://platform.claude.com/docs/en/cli-sdks-libraries/middleware">
    How SDK middleware works, including the refusal-fallback helper.
  </Card>

  <Card title="Migration guide" icon="arrow-right" href="https://platform.claude.com/docs/en/about-claude/models/migration-guide">
    Move an existing application to Claude Fable 5.
  </Card>
</CardGroup>
