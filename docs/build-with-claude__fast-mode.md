# Fast mode (research preview)

Get up to 2.5x higher output tokens per second from supported Claude Opus models.

---

Fast mode delivers up to 2.5x higher output tokens per second from Claude Opus 4.8 and Claude Opus 4.7 at premium pricing. Set `speed: "fast"` with the `fast-mode-2026-02-01` beta header on your request to opt in.

<Note>
  Fast mode is in research preview. Contact your account manager to request access. If you do not have an account manager, [join the waitlist](https://claude.com/fast-mode) for fast mode.
</Note>

<Note>
  This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

## Supported models

Fast mode is supported on the following models:

* Claude Opus 4.8 (claude-opus-4-8)
* Claude Opus 4.7 (claude-opus-4-7)

<Note>
  Fast mode for Claude Opus 4.8 launches as a research preview on the Claude API, including [Claude Managed Agents](/docs/en/managed-agents/overview), only. It is not available on Amazon Bedrock, Google Cloud, or Microsoft Foundry.
</Note>

<Warning>
  Fast mode for Claude Opus 4.7 is deprecated as of June 25, 2026, and will be removed on July 24, 2026. After removal, requests to `claude-opus-4-7` with `speed: "fast"` will return an error; unlike Claude Opus 4.6 (see the following note), Claude Opus 4.7 does not fall back to standard speed. The model itself remains available at standard speed. To continue using fast mode, migrate to Claude Opus 4.8.
</Warning>

<Note>
  As of June 29, 2026, fast mode is not available on Claude Opus 4.6. Requests to `claude-opus-4-6` with `speed: "fast"` do not return an error: they run at standard speed and are billed at [standard rates](/docs/en/about-claude/pricing) rather than fast mode's premium rates, and the response reports [`usage.speed: "standard"`](#checking-which-speed-was-used). To continue using fast mode, migrate to [Claude Opus 4.8](/docs/en/about-claude/models/migration-guide).
</Note>

## How fast mode works

Fast mode runs the same model with a faster inference configuration. There is no change to intelligence or capabilities.

* Up to 2.5x higher output tokens per second compared to standard speed
* Speed benefits are focused on output tokens per second (OTPS), not time to first token (TTFT)
* Same model weights and behavior (not a different model)
* Compatible with [streaming](/docs/en/build-with-claude/streaming), where the OTPS gain is most visible

## Basic usage

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: fast-mode-2026-02-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 4096,
          "speed": "fast",
          "messages": [{
              "role": "user",
              "content": "Refactor this module to use dependency injection"
          }]
      }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta fast-mode-2026-02-01 \
    --transform 'content.0.text' \
    --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 4096
  speed: fast
  messages:
    - role: user
      content: Refactor this module to use dependency injection
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      speed="fast",
      betas=["fast-mode-2026-02-01"],
      messages=[
          {"role": "user", "content": "Refactor this module to use dependency injection"}
      ],
  )

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    speed: "fast",
    betas: ["fast-mode-2026-02-01"],
    messages: [
      {
        role: "user",
        content: "Refactor this module to use dependency injection"
      }
    ]
  });

  const textBlock = response.content.find(
    (block): block is Anthropic.Beta.Messages.BetaTextBlock => block.type === "text"
  );
  console.log(textBlock?.text);
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 4096,
      Speed = Speed.Fast,
      Betas = ["fast-mode-2026-02-01"],
      Messages = [
          new() { Role = Role.User, Content = "Refactor this module to use dependency injection" }
      ],
  });

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Speed:     anthropic.BetaMessageNewParamsSpeedFast,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Refactor this module to use dependency injection")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content[0].AsText().Text)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_8)
                  .maxTokens(4096L)
                  .speed(MessageCreateParams.Speed.FAST)
                  .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                  .addUserMessage("Refactor this module to use dependency injection")
                  .build());

  IO.println(response.content().get(0).text().get().text());
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 4096,
      speed: 'fast',
      betas: ['fast-mode-2026-02-01'],
      messages: [
          ['role' => 'user', 'content' => 'Refactor this module to use dependency injection'],
      ],
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    speed: "fast",
    betas: ["fast-mode-2026-02-01"],
    messages: [{role: "user", content: "Refactor this module to use dependency injection"}]
  )

  puts response.content[0].text
  ```
</CodeGroup>

## Pricing

Fast mode is priced at a per-model multiplier on standard rates across the full context window, including requests over 200k input tokens. The following table shows fast mode pricing for each supported model:

| Model           | Input      | Output      |
| --------------- | ---------- | ----------- |
| Claude Opus 4.8 | $10 / MTok | $50 / MTok  |
| Claude Opus 4.7 | $30 / MTok | $150 / MTok |

Fast mode pricing stacks with other pricing modifiers:

* [Prompt caching multipliers](/docs/en/about-claude/pricing#prompt-caching) apply on top of fast mode pricing
* [Data residency](/docs/en/manage-claude/data-residency) multipliers apply on top of fast mode pricing

For complete pricing details, see the [pricing page](/docs/en/about-claude/pricing#fast-mode-pricing).

## Rate limits

Fast mode has a dedicated rate limit that is separate from standard Opus rate limits. When your fast mode rate limit is exceeded, the API returns a `429` error with a `retry-after` header indicating when capacity will be available.

The response includes headers that indicate your fast mode rate limit status:

| Header                                   | Description                                       |
| ---------------------------------------- | ------------------------------------------------- |
| `anthropic-fast-input-tokens-limit`      | Maximum fast mode input tokens per minute         |
| `anthropic-fast-input-tokens-remaining`  | Remaining fast mode input tokens                  |
| `anthropic-fast-input-tokens-reset`      | Time when the fast mode input token limit resets  |
| `anthropic-fast-output-tokens-limit`     | Maximum fast mode output tokens per minute        |
| `anthropic-fast-output-tokens-remaining` | Remaining fast mode output tokens                 |
| `anthropic-fast-output-tokens-reset`     | Time when the fast mode output token limit resets |

For tier-specific rate limits, see the [rate limits page](/docs/en/api/rate-limits).

## Checking which speed was used

The response `usage` object includes a `speed` field that indicates which speed was used, either `"fast"` or `"standard"`. On supported models, fast mode doesn't silently fall back to standard speed on rate limits or capacity (you'll get a `429` or `529` instead), so when you request `speed: "fast"` on Claude Opus 4.8 or Claude Opus 4.7, `usage.speed` is `"fast"`. On Claude Opus 4.6, where fast mode is [not available](#supported-models), requests with `speed: "fast"` run at standard speed and return `usage.speed: "standard"`. Check this field to confirm which speed served a request.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "anthropic-version: 2023-06-01" \
      --header "anthropic-beta: fast-mode-2026-02-01" \
      --header "content-type: application/json" \
      --data '{
          "model": "claude-opus-4-8",
          "max_tokens": 1024,
          "speed": "fast",
          "messages": [{"role": "user", "content": "Hello"}]
      }'
  ```

  ```bash CLI
  ant beta:messages create \
    --beta fast-mode-2026-02-01 \
    --transform usage.speed \
    --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  speed: fast
  messages:
    - role: user
      content: Hello
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      speed="fast",
      betas=["fast-mode-2026-02-01"],
      messages=[{"role": "user", "content": "Hello"}],
  )

  print(response.usage.speed)  # "fast" or "standard"
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    speed: "fast",
    betas: ["fast-mode-2026-02-01"],
    messages: [{ role: "user", content: "Hello" }]
  });

  console.log(response.usage.speed); // "fast" or "standard"
  ```

  ```csharp C#
  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 1024,
      Speed = Speed.Fast,
      Betas = ["fast-mode-2026-02-01"],
      Messages = [new() { Role = Role.User, Content = "Hello" }],
  });

  Console.WriteLine(response.Usage.Speed);  // "fast" or "standard"
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Speed:     anthropic.BetaMessageNewParamsSpeedFast,
  	Betas:     []anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Usage.Speed) // "fast" or "standard"
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .speed(MessageCreateParams.Speed.FAST)
          .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
          .addUserMessage("Hello")
          .build();

  BetaMessage response = client.beta().messages().create(params);
  IO.println(response.usage().speed());  // "fast" or "standard"
  ```

  ```php PHP
  $client = new Client();

  $response = $client->beta->messages->create(
      model: 'claude-opus-4-8',
      maxTokens: 1024,
      speed: 'fast',
      betas: ['fast-mode-2026-02-01'],
      messages: [['role' => 'user', 'content' => 'Hello']],
  );

  echo $response->usage->speed;  // "fast" or "standard"
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    speed: "fast",
    betas: ["fast-mode-2026-02-01"],
    messages: [{ role: "user", content: "Hello" }]
  )

  puts(response.usage.speed)  # "fast" or "standard"
  ```
</CodeGroup>

```json Output
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
// ...
  "usage": {
    "input_tokens": 8,
    "output_tokens": 12,
    "speed": "fast"
  }
}
```

To track fast mode usage and costs across your organization, see the [Usage and Cost API](/docs/en/manage-claude/usage-cost-api).

## Retries and fallback

### Automatic retries

When fast mode rate limits are exceeded, the API returns a `429` error with a `retry-after` header. The Anthropic SDKs automatically retry these requests up to 2 times by default (configurable with `max_retries`), waiting for the server-specified delay before each retry. Because fast mode uses continuous token replenishment, the `retry-after` delay is typically short and requests succeed once capacity is available.

### Falling back to standard speed

<Note>
  This section covers an opt-in client-side fallback when fast mode is rate limited. It is separate from the behavior on [Claude Opus 4.6](#supported-models), where fast mode is not available and requests run at standard speed automatically.
</Note>

If you'd prefer to fall back to standard speed rather than wait for fast mode capacity, catch the rate limit error and retry without `speed: "fast"`. Set `max_retries` to `0` on the initial fast request to skip automatic retries and fail immediately on rate limit errors.

<Note>
  Falling back from fast to standard speed will result in a [prompt cache](/docs/en/build-with-claude/prompt-caching) miss. Requests at different speeds do not share cached prefixes.
</Note>

Because setting `max_retries` to `0` also disables retries for other transient errors (overloaded, internal server errors), the following examples reissue the original request with default retries for those cases.

<CodeGroup>
  ```bash CLI
  # `ant` retries 429/5xx automatically and has no per-request max_retries
  # override, so on a fast-mode 429 the fallback runs after the built-in
  # retries exhaust. --transform-error surfaces error.type for branching.
  create_message_with_fast_fallback() {
    local speed="$1" max_attempts="${2:-3}" body out
    body=${3:-$(cat)}
    out=$(
      ant beta:messages create --beta fast-mode-2026-02-01 \
        ${speed:+--speed "$speed"} \
        --transform-error error.type --format-error yaml <<<"$body" 2>/dev/null
    ) && { printf '%s\n' "$out"; return; }
    case "$out" in
      rate_limit_error)
        if [[ -n "$speed" ]]; then
          create_message_with_fast_fallback "" "$max_attempts" "$body"
          return
        fi ;;
      overloaded_error | api_error | "")
        if (( max_attempts > 1 )); then
          create_message_with_fast_fallback "$speed" $((max_attempts - 1)) "$body"
          return
        fi ;;
    esac
    printf '%s\n' "${out:-connection_error}" >&2
    return 1
  }

  MESSAGE=$(
    create_message_with_fast_fallback fast <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: Hello
  YAML
  )
  ```

  ```python Python
  client = anthropic.Anthropic()


  def create_message_with_fast_fallback(max_retries=0, max_attempts=3, **params):
      try:
          return client.with_options(max_retries=max_retries).beta.messages.create(
              **params
          )
      except anthropic.RateLimitError:
          if params.get("speed") == "fast":
              del params["speed"]
              return create_message_with_fast_fallback(max_retries=max_retries, **params)
          raise
      except (
          anthropic.APIStatusError,
          anthropic.APIConnectionError,
      ) as error:
          if isinstance(error, anthropic.APIStatusError) and error.status_code < 500:
              raise
          if max_attempts > 1:
              return create_message_with_fast_fallback(
                  max_retries=max_retries, max_attempts=max_attempts - 1, **params
              )
          raise


  message = create_message_with_fast_fallback(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello"}],
      betas=["fast-mode-2026-02-01"],
      speed="fast",
      max_retries=0,
  )
  ```

  ```typescript TypeScript
  async function createMessageWithFastFallback(
    params: Anthropic.Beta.MessageCreateParams,
    requestOptions?: Anthropic.RequestOptions,
    maxAttempts: number = 3
  ): Promise<Anthropic.Beta.Messages.BetaMessage> {
    try {
      return (await client.beta.messages.create(
        params,
        requestOptions
      )) as Anthropic.Beta.Messages.BetaMessage;
    } catch (e) {
      if (e instanceof Anthropic.RateLimitError && params.speed === "fast") {
        const { speed, ...rest } = params;
        return createMessageWithFastFallback(rest);
      }
      if (
        e instanceof Anthropic.InternalServerError ||
        e instanceof Anthropic.APIConnectionError
      ) {
        if (maxAttempts > 1) {
          return createMessageWithFastFallback(params, undefined, maxAttempts - 1);
        }
      }
      throw e;
    }
  }

  const message = await createMessageWithFastFallback(
    {
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello" }],
      betas: ["fast-mode-2026-02-01"],
      speed: "fast"
    },
    { maxRetries: 0 }
  );
  ```

  ```csharp C#
  async Task<BetaMessage> CreateMessageWithFastFallback(
      MessageCreateParams parameters,
      int? maxRetries = null,
      int maxAttempts = 3)
  {
      try
      {
          var requestClient = maxRetries is int retries
              ? client.WithOptions(options => options with { MaxRetries = retries })
              : client;
          return await requestClient.Beta.Messages.Create(parameters);
      }
      catch (AnthropicRateLimitException)
      {
          if (parameters.Speed is not null)
          {
              return await CreateMessageWithFastFallback(
                  parameters with { Speed = null });
          }
          throw;
      }
      catch (Anthropic5xxException)
      {
          if (maxAttempts > 1)
          {
              return await CreateMessageWithFastFallback(
                  parameters, maxAttempts: maxAttempts - 1);
          }
          throw;
      }
  }

  var message = await CreateMessageWithFastFallback(
      new MessageCreateParams
      {
          Model = "claude-opus-4-8",
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello" }],
          Betas = ["fast-mode-2026-02-01"],
          Speed = Speed.Fast,
      },
      maxRetries: 0);
  ```

  ```go Go
  func createMessageWithFastFallback(
  	ctx context.Context,
  	client *anthropic.Client,
  	params anthropic.BetaMessageNewParams,
  	maxAttempts int,
  	opts ...option.RequestOption,
  ) (*anthropic.BetaMessage, error) {
  	message, err := client.Beta.Messages.New(ctx, params, opts...)
  	if err != nil {
  		var apierr *anthropic.Error
  		if errors.As(err, &apierr) && apierr.StatusCode == 429 && params.Speed != "" {
  			params.Speed = ""
  			return createMessageWithFastFallback(ctx, client, params, maxAttempts)
  		}
  		if (errors.As(err, &apierr) && apierr.StatusCode >= 500) || !errors.As(err, &apierr) {
  			if maxAttempts > 1 {
  				return createMessageWithFastFallback(ctx, client, params, maxAttempts-1)
  			}
  		}
  		return nil, err
  	}
  	return message, nil
  }

  func main() {
  	client := anthropic.NewClient()
  	message, err := createMessageWithFastFallback(
  		context.TODO(),
  		&client,
  		anthropic.BetaMessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 1024,
  			Messages: []anthropic.BetaMessageParam{
  				anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello")),
  			},
  			Speed: "fast",
  			Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaFastMode2026_02_01},
  		},
  		3,
  		option.WithMaxRetries(0),
  	)
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message)
  }
  ```

  ```java Java
  import com.anthropic.errors.InternalServerException;
  import com.anthropic.errors.RateLimitException;
  // ...
  // Disable SDK auto-retry so the fallback logic below handles it
  AnthropicClient client =
          AnthropicOkHttpClient.builder().fromEnv().maxRetries(0).build();

  BetaMessage createMessageWithFastFallback(
          MessageCreateParams params, int maxAttempts) {
      try {
          return client.beta().messages().create(params);
      } catch (RateLimitException e) {
          if (params.speed().isPresent()) {
              MessageCreateParams retryParams = params.toBuilder()
                      .speed(Optional.empty())
                      .build();
              return createMessageWithFastFallback(retryParams, maxAttempts);
          }
          throw e;
      } catch (InternalServerException e) {
          if (maxAttempts > 1) {
              return createMessageWithFastFallback(params, maxAttempts - 1);
          }
          throw e;
      }
  }

  void main() {
      BetaMessage message = createMessageWithFastFallback(
              MessageCreateParams.builder()
                      .model(Model.CLAUDE_OPUS_4_8)
                      .maxTokens(1024L)
                      .addUserMessage("Hello")
                      .addBeta(AnthropicBeta.FAST_MODE_2026_02_01)
                      .speed(MessageCreateParams.Speed.FAST)
                      .build(),
              3);
      IO.println(message.content().get(0).text().get().text());
  }
  ```

  ```php PHP
  use Anthropic\Core\Exceptions\APIConnectionException;
  use Anthropic\Core\Exceptions\InternalServerException;
  use Anthropic\Core\Exceptions\RateLimitException;
  use Anthropic\RequestOptions;
  // ...
  $client = new Client();

  function createMessageWithFastFallback(
      Client $client,
      array $params,
      ?RequestOptions $requestOptions = null,
      int $maxAttempts = 3,
  ) {
      try {
          return $client->beta->messages->create(
              ...$params,
              requestOptions: $requestOptions,
          );
      } catch (RateLimitException $e) {
          if (isset($params['speed'])) {
              unset($params['speed']);
              return createMessageWithFastFallback($client, $params);
          }
          throw $e;
      } catch (InternalServerException | APIConnectionException $e) {
          if ($maxAttempts > 1) {
              return createMessageWithFastFallback(
                  $client, $params, maxAttempts: $maxAttempts - 1
              );
          }
          throw $e;
      }
  }

  $message = createMessageWithFastFallback(
      $client,
      [
          'model' => 'claude-opus-4-8',
          'maxTokens' => 1024,
          'messages' => [['role' => 'user', 'content' => 'Hello']],
          'betas' => ['fast-mode-2026-02-01'],
          'speed' => 'fast',
      ],
      RequestOptions::with(maxRetries: 0),
  );
  ```

  ```ruby Ruby
  anthropic = Anthropic::Client.new

  def create_message_with_fast_fallback(client, request_options: {}, max_attempts: 3, **params)
    client.beta.messages.create(**params, request_options: request_options)
  rescue Anthropic::Errors::RateLimitError
    raise unless params[:speed] == "fast"
    params.delete(:speed)
    create_message_with_fast_fallback(client, **params)
  rescue Anthropic::Errors::InternalServerError, Anthropic::Errors::APIConnectionError
    raise unless max_attempts > 1
    create_message_with_fast_fallback(client, max_attempts: max_attempts - 1, **params)
  end

  message = create_message_with_fast_fallback(
    anthropic,
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello" }],
    betas: ["fast-mode-2026-02-01"],
    speed: "fast",
    request_options: { max_retries: 0 }
  )
  ```
</CodeGroup>

## Considerations

* **Prompt caching:** Switching between fast and standard speed invalidates the prompt cache. Requests at different speeds do not share cached prefixes.
* **Supported models:** Fast mode is supported on Claude Opus 4.8 and Claude Opus 4.7 (fast mode deprecated; removal on July 24, 2026, with the model itself unaffected). On Claude Opus 4.6, requests with `speed: "fast"` do not return an error: they run at standard speed and are billed at standard rates. On any other model, sending `speed: "fast"` returns an error.
* **TTFT:** Fast mode's benefits are focused on output tokens per second (OTPS), not time to first token (TTFT).
* **Batch API:** Fast mode is not available with the [Batch API](/docs/en/build-with-claude/batch-processing).
* **Priority Tier:** Fast mode is not available with a [Priority Tier](/docs/en/api/service-tiers) commitment.
* **Claude Platform on AWS:** Fast mode is not currently available on [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws).

## Next steps

<CardGroup cols={2}>
  <Card title="Structured outputs" icon="code-brackets" href="/docs/en/build-with-claude/structured-outputs">
    Get validated JSON results from agent workflows.
  </Card>

  <Card title="Pricing" icon="calculator" href="/docs/en/about-claude/pricing#fast-mode-pricing">
    Learn about Anthropic's pricing structure for models and features.
  </Card>

  <Card title="Effort" icon="gauge" href="/docs/en/build-with-claude/effort">
    Control how many tokens Claude uses when responding with the effort parameter, trading off between response thoroughness and token efficiency.
  </Card>

  <Card title="Streaming messages" icon="arrow-right" href="/docs/en/build-with-claude/streaming">
    Stream Messages API responses incrementally with server-sent events, including text, tool use, and extended thinking deltas.
  </Card>
</CardGroup>
