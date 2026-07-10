# Fallback credit

Avoid paying the prompt-cache cost twice when you retry a refused Claude Fable 5 request on another model.

---

Prompt caches are per-model. When Claude Fable 5 declines a request and you retry on another model, the conversation prefix that was already cached for Claude Fable 5 must be written into the new model's cache from scratch. Cache writes cost more than cache reads. Fallback credit removes that extra cost. The refusal carries a credit token, you echo the token on the retry, and the retry is billed as though the conversation had been on the new model all along.

You need this page only when you build the retry yourself: on the Ruby or PHP SDK, over raw HTTP, or with custom retry logic. [Server-side fallback](/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback) and the [SDK middleware](/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) apply fallback credit automatically. If you use either, skip this page.

[Refusals and fallback](/docs/en/build-with-claude/refusals-and-fallback) covers detecting refusals and choosing a fallback approach. [Prompt caching](/docs/en/build-with-claude/prompt-caching) explains cache reads and cache writes if those terms are new.

## The basic flow

<Steps>
  <Step title="Opt in with the beta header">
    Send the request that may be refused with the `anthropic-beta: fallback-credit-2026-06-01` header. The `server-side-fallback-2026-06-01` header also grants the same fields.
  </Step>

  <Step title="Read two fields from the refusal">
    On a refusal, `stop_details` includes two fields:

    * **`fallback_credit_token`:** an opaque string that represents the credit.
    * **`fallback_has_prefill_claim`:** a Boolean that tells you which retry body shape to use.

    Both are `null` when no credit is available for the refusal.
  </Step>

  <Step title="Build the retry">
    Start from the refused request body. Set `model` to the fallback model and add the token as the top-level `fallback_credit_token` parameter. Pick the body shape from the table below.
  </Step>

  <Step title="Send the retry with the same header">
    Send the retry with the same `fallback-credit-2026-06-01` beta header. The retry needs the header to redeem the token.
  </Step>
</Steps>

The `fallback_has_prefill_claim` field tells you whether the retry can continue the refused model's partial output instead of starting over:

| `fallback_has_prefill_claim` | Retry body                                                                                                                                                                                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true`                       | The refused request body, unchanged, plus one appended assistant message whose `content` echoes the refused response's `content`. The retry model continues the response from where the refused model stopped, and completed server tool calls are not re-executed. |
| `false`                      | The refused request body, unchanged.                                                                                                                                                                                                                                |

## Example

The following example makes a request that may be refused and redeems the credit token on a retry against Claude Opus 4.8. When a retry attempt is rejected, the example degrades through the rejection ladder: the sequence of progressively simpler retry shapes covered in [When a retry is rejected](#when-a-retry-is-rejected).

<CodeGroup>
  ```bash cURL
  # Initial request (may be refused)
  response=$(curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: fallback-credit-2026-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-fable-5",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}]
    }')

  token=$(jq -r '.stop_details.fallback_credit_token // empty' <<<"$response")

  if [[ -n "$token" ]]; then
    # Retry on the fallback model with the credit token (same body)
    response=$(curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "anthropic-version: 2023-06-01" \
      -H "anthropic-beta: fallback-credit-2026-06-01" \
      -H "content-type: application/json" \
      -d "$(jq -n --arg t "$token" '{
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{"role": "user", "content": "Hello, Claude"}],
        fallback_credit_token: $t
      }')")
  fi

  # See the SDK examples for the full rejection-handling ladder.
  jq -c '{stop_reason, model}' <<<"$response"
  ```

  ```bash CLI
  # Initial request (may be refused)
  response=$(ant beta:messages create \
    --model claude-fable-5 \
    --max-tokens 1024 \
    --message '{"role":"user","content":"Hello, Claude"}' \
    --beta fallback-credit-2026-06-01 \
    --format json)

  # A refusal carries a one-time credit token in stop_details
  token=$(jq -r '.stop_details.fallback_credit_token // empty' <<<"${response}")

  # Retry on the fallback model with the credit token
  if [[ -n "${token}" ]]; then
    response=$(ant beta:messages create \
      --model claude-opus-4-8 \
      --max-tokens 1024 \
      --message '{"role":"user","content":"Hello, Claude"}' \
      --fallback-credit-token "${token}" \
      --beta fallback-credit-2026-06-01 \
      --format json)
  fi

  jq -c '{stop_reason, model}' <<<"${response}"
  # See the SDK examples for the full rejection-handling ladder.
  ```

  ```python Python
  client = Anthropic()

  request = {
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello, Claude"}],
  }


  def send(model, body):
      return client.beta.messages.create(
          model=model, betas=["fallback-credit-2026-06-01"], **body
      )


  response = send("claude-fable-5", request)

  if (
      response.stop_reason == "refusal"
      and (details := response.stop_details)
      and (token := details.fallback_credit_token)
  ):
      exact_body = request | {"fallback_credit_token": token}
      # Prefer the continuation shape unless the claim is False
      if details.fallback_has_prefill_claim is not False:
          # Echo the refusal's content, stripping trailing whitespace from a
          # final text block (the prefill validator rejects it; the server-side
          # match tolerates the edit). Tool-using requests also omit unpaired
          # tool_use blocks, then re-strip whitespace after any omissions.
          echoed = [block.model_dump() for block in response.content]
          match echoed:
              case [*_, {"type": "text"} as final_block]:
                  final_block["text"] = final_block["text"].rstrip()
          attempt = exact_body | {
              "messages": [
                  *request["messages"],
                  {"role": "assistant", "content": echoed},
              ]
          }
      else:
          attempt = exact_body

      try:
          response = send("claude-opus-4-8", attempt)
      except BadRequestError as error:
          if "redemption temporarily unavailable" in str(error):
              raise  # Transient: retry with the token within its five-minute window
          try:
              # Fall back to the unchanged body, still with the token
              response = send("claude-opus-4-8", exact_body)
          except BadRequestError as error:
              if "redemption temporarily unavailable" in str(error):
                  raise  # Transient: retry with the token within its five-minute window
              # The token itself was rejected: forfeit it and retry without.
              response = send("claude-opus-4-8", request)

  print(json.dumps({"stop_reason": response.stop_reason, "model": response.model}))
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const request: Anthropic.Beta.MessageCreateParamsNonStreaming = {
    model: "claude-fable-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello, Claude" }],
    betas: ["fallback-credit-2026-06-01"]
  };

  let response = await client.beta.messages.create(request);

  if (
    response.stop_reason === "refusal" &&
    response.stop_details?.type === "refusal" &&
    response.stop_details.fallback_credit_token
  ) {
    const { fallback_credit_token, fallback_has_prefill_claim } = response.stop_details;
    const fallbackModel = "claude-opus-4-8";

    const exactRetry: Anthropic.Beta.MessageCreateParamsNonStreaming = {
      ...request,
      model: fallbackModel,
      fallback_credit_token
    };

    // Richest shape first, degrading on each rejection: the continuation
    // shape (unless the claim is false), the unchanged body still carrying
    // the token, and finally forfeiting the token.
    let attempt = exactRetry;
    if (fallback_has_prefill_claim !== false) {
      // Echo the refusal's content as an assistant turn, stripping trailing
      // whitespace from a final text block (the prefill validator rejects it;
      // the server-side match tolerates the edit). Tool-using requests also
      // omit unpaired tool_use blocks, then re-strip after any omissions.
      const finalIndex = response.content.length - 1;
      const echoed: Anthropic.Beta.BetaContentBlockParam[] = response.content.map(
        (block, index) =>
          block.type === "text" && index === finalIndex
            ? { ...block, text: block.text.trimEnd() }
            : block
      );
      attempt = {
        ...exactRetry,
        messages: [...request.messages, { role: "assistant", content: echoed }]
      };
    }

    try {
      response = await client.beta.messages.create(attempt);
    } catch (error) {
      // Degrade only on a shape-related 400. "redemption temporarily
      // unavailable" is transient: retry the same way within the token's
      // five-minute window instead.
      if (
        !(error instanceof Anthropic.BadRequestError) ||
        error.message.includes("redemption temporarily unavailable")
      ) {
        throw error;
      }
      try {
        response = await client.beta.messages.create(exactRetry);
      } catch (retryError) {
        if (
          !(retryError instanceof Anthropic.BadRequestError) ||
          retryError.message.includes("redemption temporarily unavailable")
        ) {
          throw retryError;
        }
        response = await client.beta.messages.create({ ...request, model: fallbackModel });
      }
    }
  }

  const { stop_reason, model } = response;
  console.log(JSON.stringify({ stop_reason, model }));
  ```

  ```csharp C#
  using Anthropic.Exceptions;
  using Anthropic.Models.Beta.Messages;

  var client = new AnthropicClient();
  const string beta = "fallback-credit-2026-06-01";

  List<BetaMessageParam> requestMessages =
  [
      new() { Role = Role.User, Content = "Hello, Claude" },
  ];
  MessageCreateParams Request(string model) => new()
  {
      Model = model,
      MaxTokens = 1024,
      Messages = requestMessages,
      Betas = [beta],
  };
  var response = await client.Beta.Messages.Create(Request("claude-fable-5"));

  if (
      response.StopReason == BetaStopReason.Refusal
      && response.StopDetails is { FallbackCreditToken: string token } details
  )
  {
      var exactBody = Request("claude-opus-4-8") with { FallbackCreditToken = token };
      var attempt = exactBody;
      // Prefer the continuation shape unless the claim is false
      if (details.FallbackHasPrefillClaim is not false)
      {
          // Echo the refusal's content, stripping trailing whitespace from a
          // final text block (the prefill validator rejects it; the match
          // tolerates the edit). Tool-using requests also omit unpaired
          // tool_use blocks, then re-strip whitespace after any omissions.
          var echoed = JsonNode.Parse(response.RawData["content"].GetRawText())!.AsArray();
          if (
              echoed is [.., JsonObject lastBlock]
              && lastBlock["type"]?.GetValue<string>() == "text"
              && lastBlock["text"]?.GetValue<string>() is string text
          )
          {
              lastBlock["text"] = text.TrimEnd();
          }
          attempt = exactBody with
          {
              Messages =
              [
                  .. requestMessages,
                  new()
                  {
                      Role = Role.Assistant,
                      Content = new BetaMessageParamContent(
                          JsonSerializer.SerializeToElement(echoed)
                      ),
                  },
              ],
          };
      }
      // A transient "redemption temporarily unavailable" rejection propagates out of
      // each of the following catch filters: retry with the token within its five-minute window.
      try
      {
          response = await client.Beta.Messages.Create(attempt);
      }
      catch (AnthropicBadRequestException e)
          when (!e.Message.Contains("redemption temporarily unavailable"))
      {
          try
          {
              // Fall back to the unchanged body, still with the token
              response = await client.Beta.Messages.Create(exactBody);
          }
          catch (AnthropicBadRequestException retryError)
              when (!retryError.Message.Contains("redemption temporarily unavailable"))
          {
              // The token itself was rejected: forfeit it and retry without.
              response = await client.Beta.Messages.Create(Request("claude-opus-4-8"));
          }
      }
  }

  Console.WriteLine(
      JsonSerializer.Serialize(
          new { stop_reason = response.StopReason?.Raw(), model = response.Model.Raw() }
      )
  );
  ```

  ```go Go
  ctx := context.Background()
  client := anthropic.NewClient()

  request := anthropic.BetaMessageNewParams{
  	MaxTokens: 1024,
  	Betas:     []anthropic.AnthropicBeta{"fallback-credit-2026-06-01"},
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Hello, Claude")),
  	},
  }

  send := func(model anthropic.Model, body anthropic.BetaMessageNewParams) (*anthropic.BetaMessage, error) {
  	body.Model = model
  	return client.Beta.Messages.New(ctx, body)
  }
  // A non-transient 400 means this attempt shape or token was rejected and
  // the next rung of the ladder should run. "redemption temporarily
  // unavailable" is transient: surface it and retry with the token within
  // its five-minute window.
  canFallBack := func(err error) bool {
  	apiErr, ok := errors.AsType[*anthropic.Error](err)
  	return ok && apiErr.StatusCode == 400 &&
  		!strings.Contains(apiErr.Error(), "redemption temporarily unavailable")
  }

  response, err := send(anthropic.ModelClaudeFable5, request)
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == anthropic.BetaStopReasonRefusal {
  	details := response.StopDetails
  	if token := details.FallbackCreditToken; token != "" {
  		exactBody := request
  		exactBody.FallbackCreditToken = anthropic.String(token)
  		attempt := exactBody
  		// Prefer the continuation shape unless the claim is false
  		if details.FallbackHasPrefillClaim || !details.JSON.FallbackHasPrefillClaim.Valid() {
  			// Echo the refusal's content, stripping trailing whitespace from a
  			// final text block (the prefill validator rejects it; the match
  			// tolerates the edit). Tool-using requests also omit unpaired
  			// tool_use blocks, then re-strip whitespace after any omissions.
  			echoed := response.ToParam()
  			if len(echoed.Content) > 0 {
  				if text := echoed.Content[len(echoed.Content)-1].OfText; text != nil {
  					text.Text = strings.TrimRightFunc(text.Text, unicode.IsSpace)
  				}
  			}
  			attempt.Messages = append(slices.Clone(request.Messages), echoed)
  		}
  		response, err = send(anthropic.ModelClaudeOpus4_8, attempt)
  		if err != nil && canFallBack(err) {
  			// Fall back to the unchanged body, still with the token
  			response, err = send(anthropic.ModelClaudeOpus4_8, exactBody)
  			if err != nil && canFallBack(err) {
  				// The token itself was rejected: forfeit it and retry without.
  				response, err = send(anthropic.ModelClaudeOpus4_8, request)
  			}
  		}
  		if err != nil {
  			log.Fatal(err)
  		}
  	}
  }

  summary, err := json.Marshal(struct {
  	StopReason anthropic.BetaStopReason `json:"stop_reason"`
  	Model      anthropic.Model          `json:"model"`
  }{response.StopReason, response.Model})
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(string(summary))
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams.Builder request() {
      return MessageCreateParams.builder()
          .maxTokens(1024L)
          .addUserMessage("Hello, Claude")
          .addBeta("fallback-credit-2026-06-01");
  }

  BetaMessage send(String model, MessageCreateParams.Builder body) {
      return client.beta().messages().create(body.model(model).build());
  }

  void main() {
      BetaMessage response = send("claude-fable-5", request());

      if (response.stopReason().map(BetaStopReason.REFUSAL::equals).orElse(false)
              && response.stopDetails().orElse(null) instanceof BetaRefusalStopDetails details
              && details.fallbackCreditToken().orElse(null) instanceof String creditToken) {
          MessageCreateParams.Builder attempt = request().fallbackCreditToken(creditToken);
          // Prefer the continuation shape unless the claim is false
          if (details.fallbackHasPrefillClaim().orElse(true)) {
              // Echo the refusal's content, stripping trailing whitespace from a
              // final text block (the prefill validator rejects it; the match
              // tolerates the edit). Tool-using requests also omit unpaired
              // tool_use blocks, then re-strip whitespace after any omissions.
              List<BetaContentBlockParam> echoed = new ArrayList<>(
                  response.content().stream().map(BetaContentBlock::toParam).toList());
              if (!echoed.isEmpty() && echoed.getLast().isText()) {
                  var lastText = echoed.removeLast().asText();
                  echoed.addLast(BetaContentBlockParam.ofText(
                      lastText.toBuilder().text(lastText.text().stripTrailing()).build()));
              }
              attempt.addAssistantMessageOfBetaContentBlockParams(echoed);
          }
          try {
              response = send("claude-opus-4-8", attempt);
          } catch (BadRequestException badRequest) {
              // Transient: retry with the token within its five-minute window
              if (badRequest.getMessage().contains("redemption temporarily unavailable")) {
                  throw badRequest;
              }
              try {
                  // Fall back to the unchanged body, still with the token
                  response = send("claude-opus-4-8", request().fallbackCreditToken(creditToken));
              } catch (BadRequestException retryBadRequest) {
                  if (retryBadRequest.getMessage().contains("redemption temporarily unavailable")) {
                      throw retryBadRequest;
                  }
                  // The token itself was rejected: forfeit it and retry without.
                  response = send("claude-opus-4-8", request());
              }
          }
      }

      IO.println("{\"stop_reason\": \"%s\", \"model\": \"%s\"}"
          .formatted(response.stopReason().orElseThrow(), response.model()));
  }
  ```

  ```php PHP
  $client = new Client();
  $beta = 'fallback-credit-2026-06-01';
  $messages = [['role' => 'user', 'content' => 'Hello, Claude']];

  $send = fn (string $model, array $messages, ?string $token = null) => $client->beta->messages->create(
      maxTokens: 1024,
      messages: $messages,
      model: $model,
      fallbackCreditToken: $token,
      betas: [$beta],
  );
  $response = $send('claude-fable-5', $messages);

  if ($response->stopReason === 'refusal' && $response->stopDetails !== null) {
      $token = $response->stopDetails->fallbackCreditToken;
      if ($token !== null) {
          $attemptMessages = $messages;
          // Prefer the continuation shape unless the claim is false
          if ($response->stopDetails->fallbackHasPrefillClaim !== false) {
              // Echo the refusal's content, stripping trailing whitespace from a
              // final text block (the prefill validator rejects it; the match
              // tolerates the edit). Tool-using requests also omit unpaired
              // tool_use blocks, then re-strip whitespace after any omissions.
              $echoed = $response->content
                  |> json_encode(...)
                  |> (fn (string $json): array => json_decode($json, associative: true));
              $lastIndex = array_key_last($echoed);
              if ($lastIndex !== null && $echoed[$lastIndex]['type'] === 'text') {
                  $echoed[$lastIndex]['text'] = rtrim($echoed[$lastIndex]['text']);
              }
              $attemptMessages[] = ['role' => 'assistant', 'content' => $echoed];
          }
          // Transient: retry with the token within its five-minute window
          $isTransientRedemption = fn (BadRequestException $error): bool =>
              str_contains($error->getMessage(), 'redemption temporarily unavailable');
          try {
              $response = $send('claude-opus-4-8', $attemptMessages, $token);
          } catch (BadRequestException $error) {
              if ($isTransientRedemption($error)) {
                  throw $error;
              }
              try {
                  // Fall back to the unchanged body, still with the token
                  $response = $send('claude-opus-4-8', $messages, $token);
              } catch (BadRequestException $retryError) {
                  if ($isTransientRedemption($retryError)) {
                      throw $retryError;
                  }
                  // The token itself was rejected: forfeit it and retry without.
                  $response = $send('claude-opus-4-8', $messages);
              }
          }
      }
  }

  echo json_encode(['stop_reason' => $response->stopReason, 'model' => $response->model]), PHP_EOL;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  request = {
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello, Claude"}]
  }

  send_message = lambda do |model, body|
    client.beta.messages.create(model:, betas: ["fallback-credit-2026-06-01"], **body)
  end

  response = send_message.call("claude-fable-5", request)

  if response in {stop_reason: :refusal,
                  stop_details: {fallback_credit_token: String => credit_token} => details}
    exact_body = request.merge(fallback_credit_token: credit_token)

    # Prefer the continuation shape unless the claim is false
    if details.fallback_has_prefill_claim != false
      # Echo the refusal's content, stripping trailing whitespace from a final
      # text block (the prefill validator rejects it; the match tolerates the
      # edit). Tool-using requests also omit unpaired tool_use blocks, then
      # re-strip whitespace after any omissions.
      echoed = response.content.map(&:to_h)
      if echoed.last in {type: :text, text: String => final_text}
        echoed[-1] = echoed[-1].merge(text: final_text.rstrip)
      end
      attempt = exact_body.merge(
        messages: [*request[:messages], {role: "assistant", content: echoed}]
      )
    else
      attempt = exact_body
    end

    begin
      response = send_message.call("claude-opus-4-8", attempt)
    rescue Anthropic::Errors::BadRequestError => error
      # Transient: retry with the token within its five-minute window
      raise if error.message.include?("redemption temporarily unavailable")
      begin
        # Fall back to the unchanged body, still with the token
        response = send_message.call("claude-opus-4-8", exact_body)
      rescue Anthropic::Errors::BadRequestError => error
        # Transient: retry with the token within its five-minute window
        raise if error.message.include?("redemption temporarily unavailable")
        # The token itself was rejected: forfeit it and retry without.
        response = send_message.call("claude-opus-4-8", request)
      end
    end
  end

  puts JSON.generate({stop_reason: response.stop_reason, model: response.model})
  ```
</CodeGroup>

## Where it works

Fallback credit is in beta on the Claude API, Claude Platform on AWS, Amazon Bedrock, Google Cloud, and Microsoft Foundry. Credit tokens returned in [Message Batches](/docs/en/build-with-claude/batch-processing) results cannot be redeemed. Redemption applies only to direct Messages API requests.

The retry model must be one of the refused model's permitted fallback targets. At launch, Claude Fable 5's permitted target is Claude Opus 4.8 (`claude-opus-4-8`).

<Accordion title="Looking up permitted fallback targets programmatically">
  On the Claude API and Claude Platform on AWS, the target list is published as `allowed_fallback_models` on each model's entry in the [Models API](/docs/en/api/models/list) when the `server-side-fallback-2026-06-01` beta header is set. The list is not yet visible under the `fallback-credit-*` header alone. It is not exposed on Amazon Bedrock, Google Cloud, or Microsoft Foundry.
</Accordion>

## Checking that the credit applied

The refund is visible in the retry's `usage`. Compared with what the same request would report without the token, `cache_creation_input_tokens` is lower, and `cache_read_input_tokens` is higher by the same amount. A shift of zero means the token was honored but there was nothing to reprice, for example because the retry model's cache was already warm.

## When a retry is rejected

Most retries redeem on the first attempt. When one does not, the API returns a 400 error that tells you what to try next.

<Steps>
  <Step title="Continuation rejected: resend the unchanged body">
    If the retry that appends the assistant message is rejected with a 400 error, resend the refused request body unchanged, still with the token.
  </Step>

  <Step title="Token rejected: drop the token">
    If the unchanged body is also rejected with a 400 error whose message names `fallback_credit_token`, retry without the token. The credit is forfeited, but the retry itself goes through.
  </Step>
</Steps>

<Note>
  If the refused request executed server tools, a tokenless retry re-runs and re-bills those tools. In that case, surface the 400 error to your caller instead of falling through to a tokenless retry.
</Note>

<Accordion title="If the error says 'redemption temporarily unavailable'">
  This rejection is transient, not a verdict on your retry shape. Retry the same request, with the same token, within the token's five-minute window. Do not move to the next step of the ladder.
</Accordion>

## Reference

The sections below cover edge cases and the complete redemption rules. Most integrations do not need them.

<Accordion title="Fields that must match the refused request">
  Redemption compares the retry against the refused request. Every field that shapes the prompt must match exactly. Fields that do not shape the prompt may change on the retry.

  | Rule                    | Fields                                                                                                                                                                      |
  | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | Must match exactly      | `system`, `messages`, `tools`, `tool_choice`, `thinking`, and `cache_control`, plus `output_config`, `mcp_servers`, `context_management`, and `container` when you use them |
  | May change on the retry | `model`, `max_tokens`, `stop_sequences`, `temperature`, `top_p`, `top_k`, `stream`, `metadata`, and `service_tier`                                                          |

  The continuation shape (`fallback_has_prefill_claim: true`) is the one exception to the `messages` match: it adds exactly one assistant message at the end of `messages`.

  Do not strip `thinking` or `redacted_thinking` blocks from earlier turns on the retry, even though a plain retry without a token usually strips them. The body must match the refused request, and the server handles those blocks itself.
</Accordion>

<Accordion title="Beta headers must match too">
  Send the same `anthropic-beta` headers on the retry as on the refused request. A beta header present on one of the two requests but not the other can fail the match even when the bodies are identical. The resulting 400 error carries the same `request body ... does not match` message as a body difference, so a header difference is easy to misread as a body problem. In particular, do not add or drop beta headers based on which model the request targets.

  Two header families are exempt from the match, for the retry's sake:

  * **`server-side-fallback-*`:** a retry must drop the `fallbacks` parameter, and dropping this header along with it does not cause a mismatch.
  * **`fallback-credit-*`:** keep this header on both requests. The retry needs it to redeem the token.

  <Note>
    On models that include the 1M token context window by default, such as Claude Fable 5 and Claude Opus 4.8, the `context-1m-2025-08-07` beta header has no effect. The most robust way to keep the two requests identical is to omit that header on both, rather than sending it on one request and not the other.
  </Note>
</Accordion>

<Accordion title="When fallback_has_prefill_claim is absent">
  The field is `null` only when the token is also `null`, so a value you observe while holding a token is never `null`. It can still surface as absent (`None` in the typed SDKs) on Amazon Bedrock, Google Cloud, and Microsoft Foundry while their support for the field rolls out. In that case, treat the retry shape as unknown rather than as `false`. Try the appended-assistant-message shape first, and rely on the rejection handling in [When a retry is rejected](#when-a-retry-is-rejected), which falls back to the unchanged body.
</Accordion>

<Accordion title="Echoing the refused response's content">
  When a refusal's token supports the continuation shape, the response `content` carries only the model's own output, and the refusal explanation is delivered in `stop_details.explanation`. You can therefore echo `content` into the appended assistant message as-is.

  Two adjustments may still be needed before sending:

  * If the final block you send is a `text` block, strip its trailing whitespace.
  * Omit any client-side `tool_use` block that has no matching `tool_result`.

  If the echoed content includes a `fallback` block from an earlier [server-side fallback](/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback), keep the block exactly where it appeared. It is accepted on any request without a beta header. The API uses its position to validate the thinking blocks around it, so a request that echoes thinking blocks from both sides of that boundary is rejected if the block is omitted or moved.
</Accordion>

<Accordion title="Token scope and lifetime">
  The token redeems only from the organization and workspace that received the refusal, including on Microsoft Foundry. On Amazon Bedrock and Google Cloud, which do not have workspaces, the token is bound to the platform's caller identity instead.

  The token expires five minutes after the refusal. After that, send the retry without it. The token is also stateless: the server stores nothing about it, and there is no endpoint to inspect or revoke it.
</Accordion>

<Accordion title="When a token cannot be redeemed by either shape">
  When the refusal arrived after server tools had already executed within the request, the token redeems only by continuing the partial response. That restriction is what prevents the completed tool calls from running, and billing, again.

  One combination can therefore leave the token unredeemable by either shape, when both of the following are true:

  * The request used `output_config.format` or a `tool_choice` that forces tool use. Either one rules out the appended-assistant-message shape.
  * The refusal arrived after server tools had executed. That rules out the unchanged body.

  If the unchanged-body retry is rejected with a 400 error saying the token must be redeemed by continuing the partial response, discard the token. A retry without it goes through, but it re-runs and re-bills the completed server tools. Surface the cost or the error to your caller rather than retrying silently.
</Accordion>

## Next steps

<CardGroup>
  <Card title="Refusals and fallback" icon="shield" href="/docs/en/build-with-claude/refusals-and-fallback">
    Detect refusals and choose between server-side fallback, the SDK middleware, and a manual retry.
  </Card>

  <Card title="Prompt caching" icon="bolt" href="/docs/en/build-with-claude/prompt-caching">
    How cache reads and cache writes are billed.
  </Card>

  <Card title="Stop reasons and fallback" icon="code" href="/docs/en/build-with-claude/handling-stop-reasons">
    Every `stop_reason` value and how to handle it.
  </Card>

  <Card title="SDK middleware" icon="settings" href="/docs/en/cli-sdks-libraries/middleware">
    The SDK helper that applies fallback credit automatically.
  </Card>
</CardGroup>
