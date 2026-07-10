# Cache diagnostics

Diagnose unexpected prompt cache misses by comparing consecutive requests and identifying exactly where the prompt prefix diverged.

---

<Note>
  This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

[Prompt caching](/docs/en/build-with-claude/prompt-caching) cuts latency and cost significantly, but only when the beginning of your prompt is byte-for-byte identical to a recent request. A reordered tool, a timestamp interpolated into your system prompt, or an edit to an earlier message can silently invalidate the cache. Without cache diagnostics, the only signal is `usage.cache_read_input_tokens` dropping to zero, with no indication of what changed.

Cache diagnostics closes that gap. Pass the `id` of your previous response, and the API compares the two requests and tells you where they diverged (the model, the system prompt, the tools, or the message history) so you can fix the root cause instead of guessing.

<Note>
  Cache diagnostics is in beta. Include the [beta header](/docs/en/api/beta-headers) `cache-diagnosis-2026-04-07` in your API requests to use this feature.

  Cache diagnostics is currently available on the Claude API only. It is not supported on Amazon Bedrock or Google Cloud.
</Note>

## How cache diagnostics works

When the beta header is present, the API stores a lightweight fingerprint of each request, keyed by the response `id`. On your next request, include that `id` as `diagnostics.previous_message_id`. The API rebuilds the fingerprint for the new request, compares it against the stored one, and attaches a `diagnostics` object to the response describing the first point of divergence.

The comparison is about request structure, independent of whether the cache actually hit. See [Reading diagnostics alongside usage](#reading-diagnostics-alongside-usage) for how to combine the `diagnostics` result with `usage.cache_read_input_tokens`.

Fingerprints contain only hashes and token-count estimates (never raw prompt content), are retained for a limited time, are scoped to your organization and workspace, and are not used for any other purpose.

## Basic usage

Send the beta header on every turn. On the first turn, pass `"previous_message_id": null` to opt in without a prior message to compare against. On subsequent turns, pass the `id` from the previous response.

<CodeGroup>
  ```bash cURL
  # Turn 1: establish the cache and opt in to diagnostics
  response=$(curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: cache-diagnosis-2026-04-07" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are an AI assistant analyzing a large document. <document>...</document>",
      "messages": [{"role": "user", "content": "Summarize section 1."}],
      "diagnostics": {"previous_message_id": null}
    }')
  jq '{id, diagnostics}' <<< "$response"
  message_id=$(jq -r '.id' <<< "$response")

  # Turn 2: reference the previous turn so the API can compare prefixes
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: cache-diagnosis-2026-04-07" \
    --header "content-type: application/json" \
    --data @- <<EOF | jq '{id, diagnostics}'  # diagnostics: null means no divergence was found
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "cache_control": {"type": "ephemeral"},
    "system": "You are an AI assistant analyzing a large document. <document>...</document>",
    "messages": [
      {"role": "user", "content": "Summarize section 1."},
      {"role": "assistant", "content": "Section 1 covers..."},
      {"role": "user", "content": "Now summarize section 2."}
    ],
    "diagnostics": {"previous_message_id": "$message_id"}
  }
  EOF
  ```

  ```bash CLI
  # Turn 1
  turn1=$(ant beta:messages create \
    --beta cache-diagnosis-2026-04-07 \
    --transform '{id,usage,diagnostics}' <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are an AI assistant analyzing a large document. <document>...</document>"
  messages:
    - role: user
      content: Summarize section 1.
  diagnostics:
    previous_message_id: null
  YAML
  )
  printf '%s\n' "$turn1"

  # Turn 2: pass the id from turn 1 as previous_message_id
  message_id=$(jq -r '.id' <<<"$turn1")
  ant beta:messages create \
    --beta cache-diagnosis-2026-04-07 \
    --transform '{id,usage,diagnostics}' <<YAML
  model: claude-opus-4-8
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are an AI assistant analyzing a large document. <document>...</document>"
  messages:
    - role: user
      content: Summarize section 1.
    - role: assistant
      content: Section 1 covers...
    - role: user
      content: Now summarize section 2.
  diagnostics:
    previous_message_id: $message_id
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

  # Turn 1: opt in with previous_message_id=None
  r1 = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[{"role": "user", "content": "Summarize section 1."}],
      diagnostics={"previous_message_id": None},
      betas=["cache-diagnosis-2026-04-07"],
  )

  # Turn 2: reference the previous response id
  r2 = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[
          {"role": "user", "content": "Summarize section 1."},
          {"role": "assistant", "content": r1.content},
          {"role": "user", "content": "Now summarize section 2."},
      ],
      diagnostics={"previous_message_id": r1.id},
      betas=["cache-diagnosis-2026-04-07"],
  )

  diagnostics = r2.diagnostics
  if diagnostics is None:
      print("No divergence detected.")
  elif diagnostics.cache_miss_reason is None:
      print("Comparison still pending.")
  else:
      print(f"cache_miss_reason: {diagnostics.cache_miss_reason.type}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>";

  // Turn 1: opt in with previous_message_id: null
  const r1 = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [{ role: "user", content: "Summarize section 1." }],
    diagnostics: { previous_message_id: null },
    betas: ["cache-diagnosis-2026-04-07"]
  });

  // Turn 2: reference the previous response id
  const r2 = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [
      { role: "user", content: "Summarize section 1." },
      { role: "assistant", content: r1.content },
      { role: "user", content: "Now summarize section 2." }
    ],
    diagnostics: { previous_message_id: r1.id },
    betas: ["cache-diagnosis-2026-04-07"]
  });

  if (r2.diagnostics === null) {
    console.log("No divergence detected.");
  } else if (r2.diagnostics.cache_miss_reason === null) {
    console.log("Comparison still pending.");
  } else {
    console.log(`cache_miss_reason: ${r2.diagnostics.cache_miss_reason.type}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var system = "You are an AI assistant analyzing a large document. <document>...</document>";

  var r1 = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize section 1." },
          ],
          Diagnostics = new() { PreviousMessageID = null },
          Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
      }
  );

  var r2 = await client.Beta.Messages.Create(
      new()
      {
          Model = Messages::Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize section 1." },
              new()
              {
                  Role = Role.Assistant,
                  Content = r1.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
              },
              new() { Role = Role.User, Content = "Now summarize section 2." },
          ],
          Diagnostics = new() { PreviousMessageID = r1.ID },
          Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
      }
  );

  Console.WriteLine(r2.Diagnostics switch
  {
      null => "No divergence detected.",
      { CacheMissReason: null } => "Comparison still pending.",
      { CacheMissReason.Type: var type } => $"cache_miss_reason: {type.GetString()}",
  });
  ```

  ```go Go
  client := anthropic.NewClient()
  ctx := context.Background()

  system := []anthropic.BetaTextBlockParam{
  	{Text: "You are an AI assistant analyzing a large document. <document>...</document>"},
  }

  r1, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus4_8,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: param.Null[string](),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
  })
  if err != nil {
  	panic(err)
  }

  r2, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus4_8,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  		r1.ToParam(),
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Now summarize section 2.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: anthropic.String(r1.ID),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
  })
  if err != nil {
  	panic(err)
  }

  switch {
  case !r2.JSON.Diagnostics.Valid():
  	fmt.Println("No divergence detected.")
  case !r2.Diagnostics.JSON.CacheMissReason.Valid():
  	fmt.Println("Comparison still pending.")
  default:
  	fmt.Printf("cache_miss_reason: %s\n", r2.Diagnostics.CacheMissReason.Type)
  }
  ```

  ```java Java
  var client = AnthropicOkHttpClient.fromEnv();

  var system = "You are an AI assistant analyzing a large document. <document>...</document>";

  var r1 = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .system(system)
          .addUserMessage("Summarize section 1.")
          // Pass null on the first turn to opt in without a prior message to compare.
          .diagnostics(BetaDiagnosticsParam.builder().previousMessageId((String) null).build())
          .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
          .build()
  );

  var r2 = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .cacheControl(BetaCacheControlEphemeral.builder().build())
          .system(system)
          .addUserMessage("Summarize section 1.")
          .addMessage(r1)
          .addUserMessage("Now summarize section 2.")
          .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(r1.id()).build())
          .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
          .build()
  );

  if (r2.diagnostics().isEmpty()) {
      IO.println("No divergence detected.");
  } else if (r2.diagnostics().get().cacheMissReason().isEmpty()) {
      IO.println("Comparison still pending.");
  } else {
      var reason = r2.diagnostics().get().cacheMissReason().get();
      // CacheMissReason doesn't expose a typed .type() accessor; read it from the raw JSON.
      @SuppressWarnings("unchecked")
      var json = (Map<String, JsonValue>) reason._json().orElseThrow().asObject().orElseThrow();
      IO.println("cache_miss_reason: " + json.get("type").asStringOrThrow());
  }
  ```

  ```php PHP
  $client = new Client();

  $system = 'You are an AI assistant analyzing a large document. <document>...</document>';

  $r1 = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_4_8,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID(null),
      betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
  );

  $r2 = $client->beta->messages->create(
      model: Model::CLAUDE_OPUS_4_8,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
          ['role' => 'assistant', 'content' => $r1->content],
          ['role' => 'user', 'content' => 'Now summarize section 2.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($r1->id),
      betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
  );

  echo match (true) {
      $r2->diagnostics === null => "No divergence detected.\n",
      $r2->diagnostics->cacheMissReason === null => "Comparison still pending.\n",
      default => "cache_miss_reason: {$r2->diagnostics->cacheMissReason->type}\n",
  };
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

  r1 = client.beta.messages.create(
    model: :"claude-opus-4-8",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."}
    ],
    diagnostics: {previous_message_id: nil},
    betas: ["cache-diagnosis-2026-04-07"]
  )

  r2 = client.beta.messages.create(
    model: :"claude-opus-4-8",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."},
      {role: "assistant", content: r1.content},
      {role: "user", content: "Now summarize section 2."}
    ],
    diagnostics: {previous_message_id: r1.id},
    betas: ["cache-diagnosis-2026-04-07"]
  )

  case r2.diagnostics
  in nil
    puts "No divergence detected."
  in {cache_miss_reason: nil}
    puts "Comparison still pending."
  in {cache_miss_reason: {type:}}
    puts "cache_miss_reason: #{type}"
  end
  ```
</CodeGroup>

## Streaming

In streaming responses, `diagnostics` appears on the `message_start` event.

<CodeGroup>
  ```bash cURL
  # Turn 2: stream the response. diagnostics arrives on the message_start event;
  # a null value means no divergence was found.
  curl -sS --fail-with-body https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "anthropic-beta: cache-diagnosis-2026-04-07" \
    --header "content-type: application/json" \
    --data @- <<EOF | jq -R 'select(startswith("data: ")) | ltrimstr("data: ") | fromjson | select(.type == "message_start") | .message.diagnostics'
  {
    "model": "claude-opus-4-8",
    "max_tokens": 1024,
    "stream": true,
    "cache_control": {"type": "ephemeral"},
    "system": "You are an AI assistant analyzing a large document. <document>...</document>",
    "messages": [
      {"role": "user", "content": "Summarize section 1."},
      {"role": "assistant", "content": "Section 1 covers..."},
      {"role": "user", "content": "Now summarize section 2."}
    ],
    "diagnostics": {"previous_message_id": "$message_id"}
  }
  EOF
  ```

  ```bash CLI
  # Turn 2: stream. With --stream the CLI emits each SSE event as one JSON object.
  # diagnostics arrives on the message_start event; pick it out with jq.
  ant beta:messages create \
    --beta cache-diagnosis-2026-04-07 \
    --stream --format jsonl <<YAML |
  model: claude-opus-4-8
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: "You are an AI assistant analyzing a large document. <document>...</document>"
  messages:
    - role: user
      content: Summarize section 1.
    - role: assistant
      content: Section 1 covers...
    - role: user
      content: Now summarize section 2.
  diagnostics:
    previous_message_id: $message_id
  YAML
    jq -c 'select(.type == "message_start") | .message | {id,usage,diagnostics}'
  ```

  ```python Python
  # Turn 2: stream, referencing the previous response id
  with client.beta.messages.stream(
      model="claude-opus-4-8",
      max_tokens=1024,
      cache_control={"type": "ephemeral"},
      system=SYSTEM,
      messages=[
          {"role": "user", "content": "Summarize section 1."},
          {"role": "assistant", "content": r1.content},
          {"role": "user", "content": "Now summarize section 2."},
      ],
      diagnostics={"previous_message_id": r1.id},
      betas=["cache-diagnosis-2026-04-07"],
  ) as stream:
      for text in stream.text_stream:
          print(text, end="", flush=True)
      print()
      r2 = stream.get_final_message()

  diagnostics = r2.diagnostics
  if diagnostics is None:
      print("No divergence detected.")
  elif diagnostics.cache_miss_reason is None:
      print("Comparison still pending.")
  else:
      print(f"cache_miss_reason: {diagnostics.cache_miss_reason.type}")
  ```

  ```typescript TypeScript
  const stream = client.beta.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    cache_control: { type: "ephemeral" },
    system: SYSTEM,
    messages: [
      { role: "user", content: "Summarize section 1." },
      { role: "assistant", content: r1.content },
      { role: "user", content: "Now summarize section 2." }
    ],
    diagnostics: { previous_message_id: r1.id },
    betas: ["cache-diagnosis-2026-04-07"]
  });

  for await (const event of stream) {
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
  process.stdout.write("\n");

  // diagnostics arrives on message_start and is carried through to the final message
  const r2 = await stream.finalMessage();

  if (r2.diagnostics === null) {
    console.log("No divergence detected.");
  } else if (r2.diagnostics.cache_miss_reason === null) {
    console.log("Comparison still pending.");
  } else {
    console.log(`cache_miss_reason: ${r2.diagnostics.cache_miss_reason.type}`);
  }
  ```

  ```csharp C#
  // Turn 2: stream, referencing the previous response id
  BetaDiagnostics? diagnostics = null;

  var stream = client.Beta.Messages.CreateStreaming(
      new()
      {
          Model = Messages::Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          CacheControl = new(),
          System = system,
          Messages =
          [
              new() { Role = Role.User, Content = "Summarize section 1." },
              new()
              {
                  Role = Role.Assistant,
                  Content = r1.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
              },
              new() { Role = Role.User, Content = "Now summarize section 2." },
          ],
          Diagnostics = new() { PreviousMessageID = r1.ID },
          Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
      }
  );

  await foreach (var streamEvent in stream)
  {
      if (streamEvent.TryPickStart(out var start))
      {
          // diagnostics arrives on the message_start event
          diagnostics = start.Message.Diagnostics;
      }
      else if (streamEvent.TryPickContentBlockDelta(out var delta) && delta.Delta.TryPickText(out var textDelta))
      {
          Console.Write(textDelta.Text);
      }
  }
  Console.WriteLine();

  Console.WriteLine(diagnostics switch
  {
      null => "No divergence detected.",
      { CacheMissReason: null } => "Comparison still pending.",
      { CacheMissReason.Type: var type } => $"cache_miss_reason: {type.GetString()}",
  });
  ```

  ```go Go
  // Turn 2: stream, referencing the previous response id
  stream := client.Beta.Messages.NewStreaming(ctx, anthropic.BetaMessageNewParams{
  	Model:        anthropic.ModelClaudeOpus4_8,
  	MaxTokens:    1024,
  	CacheControl: anthropic.BetaCacheControlEphemeralParam{},
  	System:       system,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Summarize section 1.")),
  		r1.ToParam(),
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Now summarize section 2.")),
  	},
  	Diagnostics: anthropic.BetaDiagnosticsParam{
  		PreviousMessageID: anthropic.String(r1.ID),
  	},
  	Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
  })
  defer stream.Close()

  // diagnostics arrives on message_start; Accumulate carries it into r2
  var r2 anthropic.BetaMessage
  for stream.Next() {
  	if err := r2.Accumulate(stream.Current()); err != nil {
  		panic(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	panic(err)
  }

  switch {
  case !r2.JSON.Diagnostics.Valid():
  	fmt.Println("No divergence detected.")
  case !r2.Diagnostics.JSON.CacheMissReason.Valid():
  	fmt.Println("Comparison still pending.")
  default:
  	fmt.Printf("cache_miss_reason: %s\n", r2.Diagnostics.CacheMissReason.Type)
  }
  ```

  ```java Java
  // Turn 2: stream, referencing the previous response id
  var params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024)
      .cacheControl(BetaCacheControlEphemeral.builder().build())
      .system(system)
      .addUserMessage("Summarize section 1.")
      .addMessage(r1)
      .addUserMessage("Now summarize section 2.")
      .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(r1.id()).build())
      .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
      .build();

  var accumulator = BetaMessageAccumulator.create();
  try (var streamResponse = client.beta().messages().createStreaming(params)) {
      streamResponse.stream()
          .peek(accumulator::accumulate)
          .flatMap(event -> event.contentBlockDelta().stream())
          .flatMap(deltaEvent -> deltaEvent.delta().text().stream())
          .forEach(textDelta -> IO.print(textDelta.text()));
      IO.println("");
  }

  // diagnostics arrives on message_start and is carried through to the accumulated message
  var diagnostics = accumulator.message().diagnostics();
  if (diagnostics.isEmpty()) {
      IO.println("No divergence detected.");
  } else if (diagnostics.get().cacheMissReason().isEmpty()) {
      IO.println("Comparison still pending.");
  } else {
      var reason = diagnostics.get().cacheMissReason().get();
      // CacheMissReason doesn't expose a typed .type() accessor; read it from the raw JSON.
      @SuppressWarnings("unchecked")
      var json = (Map<String, JsonValue>) reason._json().orElseThrow().asObject().orElseThrow();
      IO.println("cache_miss_reason: " + json.get("type").asStringOrThrow());
  }
  ```

  ```php PHP
  // Turn 2: stream, referencing the previous response id
  $stream = $client->beta->messages->createStream(
      model: Model::CLAUDE_OPUS_4_8,
      maxTokens: 1024,
      cacheControl: new BetaCacheControlEphemeral,
      system: $system,
      messages: [
          ['role' => 'user', 'content' => 'Summarize section 1.'],
          ['role' => 'assistant', 'content' => $r1->content],
          ['role' => 'user', 'content' => 'Now summarize section 2.'],
      ],
      diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($r1->id),
      betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
  );

  $diagnostics = null;
  foreach ($stream as $event) {
      if ($event instanceof BetaRawMessageStartEvent) {
          // diagnostics arrives on the message_start event's embedded BetaMessage
          $diagnostics = $event->message->diagnostics;
      } elseif ($event instanceof BetaRawContentBlockDeltaEvent && $event->delta instanceof BetaTextDelta) {
          echo $event->delta->text;
      }
  }
  echo PHP_EOL;

  echo match (true) {
      $diagnostics === null => "No divergence detected.\n",
      $diagnostics->cacheMissReason === null => "Comparison still pending.\n",
      default => "cache_miss_reason: {$diagnostics->cacheMissReason->type}\n",
  };
  ```

  ```ruby Ruby
  # Turn 2: stream, referencing the previous response id
  stream = client.beta.messages.stream(
    model: :"claude-opus-4-8",
    max_tokens: 1024,
    cache_control: {type: "ephemeral"},
    system_: SYSTEM,
    messages: [
      {role: "user", content: "Summarize section 1."},
      {role: "assistant", content: r1.content},
      {role: "user", content: "Now summarize section 2."}
    ],
    diagnostics: {previous_message_id: r1.id},
    betas: ["cache-diagnosis-2026-04-07"]
  )

  stream.each do |event|
    print(event.text) if event.is_a?(Anthropic::Streaming::TextEvent)
  end
  puts

  # diagnostics arrives on message_start and is retained on the accumulated message
  r2 = stream.accumulated_message

  case r2.diagnostics
  in nil
    puts "No divergence detected."
  in {cache_miss_reason: nil}
    puts "Comparison still pending."
  in {cache_miss_reason: {type:}}
    puts "cache_miss_reason: #{type}"
  end
  ```
</CodeGroup>

The `message_start` event carries the full `diagnostics` field; see [Response format](#response-format) for the possible values.

## Threading diagnostics through a conversation loop

In a multi-turn conversation, carry the latest response `id` forward as `previous_message_id` on every turn. The first iteration passes `null` to opt in; each subsequent iteration passes the `id` from the previous response.

<Tabs>
  <Tab title="cURL">
    <Info>
      This workflow doesn't translate well to a one-off shell command. See the SDK tabs for the loop pattern; the per-turn HTTP request is identical to [Basic usage](#basic-usage).
    </Info>
  </Tab>

  <Tab title="CLI">
    <Info>
      This workflow doesn't translate well to a one-off shell command. See the SDK tabs for the loop pattern; the per-turn CLI invocation is identical to [Basic usage](#basic-usage).
    </Info>
  </Tab>

  <Tab title="Python">
    ```python
    client = anthropic.Anthropic()

    SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

    messages = []
    prev_id = None

    for i, user_message in enumerate(
        ["Summarize section 1.", "Now section 2.", "Now section 3."]
    ):
        messages.append({"role": "user", "content": user_message})

        r = client.beta.messages.create(
            model="claude-opus-4-8",
            max_tokens=1024,
            cache_control={"type": "ephemeral"},
            system=SYSTEM,
            messages=messages,
            diagnostics={"previous_message_id": prev_id},
            betas=["cache-diagnosis-2026-04-07"],
        )

        if r.diagnostics is not None and r.diagnostics.cache_miss_reason is not None:
            print(f"Turn {i + 1} cache_miss_reason: {r.diagnostics.cache_miss_reason.type}")

        messages.append({"role": "assistant", "content": r.content})
        prev_id = r.id
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    const client = new Anthropic();

    const SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>";

    const prompts = ["Summarize section 1.", "Now section 2.", "Now section 3."];

    const messages: BetaMessageParam[] = [];
    let prevId: string | null = null;

    for (const [i, prompt] of prompts.entries()) {
      messages.push({ role: "user", content: prompt });

      const r = await client.beta.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        cache_control: { type: "ephemeral" },
        system: SYSTEM,
        messages,
        diagnostics: { previous_message_id: prevId },
        betas: ["cache-diagnosis-2026-04-07"]
      });

      if (r.diagnostics?.cache_miss_reason) {
        console.log(`Turn ${i + 1} cache_miss_reason: ${r.diagnostics.cache_miss_reason.type}`);
      }

      messages.push({ role: "assistant", content: r.content });
      prevId = r.id;
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    AnthropicClient client = new();

    var system = "You are an AI assistant analyzing a large document. <document>...</document>";

    List<BetaMessageParam> messages = [];
    string? prevId = null;
    string[] prompts = ["Summarize section 1.", "Now section 2.", "Now section 3."];

    for (int i = 0; i < prompts.Length; i++)
    {
        messages.Add(new() { Role = Role.User, Content = prompts[i] });

        var r = await client.Beta.Messages.Create(
            new()
            {
                Model = Messages::Model.ClaudeOpus4_8,
                MaxTokens = 1024,
                CacheControl = new(),
                System = system,
                Messages = messages,
                Diagnostics = new() { PreviousMessageID = prevId },
                Betas = [AnthropicBeta.CacheDiagnosis2026_04_07],
            }
        );

        if (r.Diagnostics?.CacheMissReason is { Type: var type })
        {
            Console.WriteLine($"Turn {i + 1} cache_miss_reason: {type.GetString()}");
        }

        messages.Add(
            new()
            {
                Role = Role.Assistant,
                Content = r.Content.Select(block => new BetaContentBlockParam(block.Json)).ToList(),
            }
        );
        prevId = r.ID;
    }
    ```
  </Tab>

  <Tab title="Go">
    ```go
    client := anthropic.NewClient()
    ctx := context.Background()

    system := []anthropic.BetaTextBlockParam{
    	{Text: "You are an AI assistant analyzing a large document. <document>...</document>"},
    }

    prompts := []string{"Summarize section 1.", "Now section 2.", "Now section 3."}

    var messages []anthropic.BetaMessageParam
    prevID := param.Null[string]()

    for turn, prompt := range prompts {
    	messages = append(messages, anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(prompt)))

    	r, err := client.Beta.Messages.New(ctx, anthropic.BetaMessageNewParams{
    		Model:        anthropic.ModelClaudeOpus4_8,
    		MaxTokens:    1024,
    		CacheControl: anthropic.BetaCacheControlEphemeralParam{},
    		System:       system,
    		Messages:     messages,
    		Diagnostics: anthropic.BetaDiagnosticsParam{
    			PreviousMessageID: prevID,
    		},
    		Betas: []anthropic.AnthropicBeta{anthropic.AnthropicBetaCacheDiagnosis2026_04_07},
    	})
    	if err != nil {
    		panic(err)
    	}

    	if r.JSON.Diagnostics.Valid() && r.Diagnostics.JSON.CacheMissReason.Valid() {
    		fmt.Printf("Turn %d cache_miss_reason: %s\n", turn+1, r.Diagnostics.CacheMissReason.Type)
    	}

    	messages = append(messages, r.ToParam())
    	prevID = anthropic.String(r.ID)
    }
    ```
  </Tab>

  <Tab title="Java">
    ```java
    var client = AnthropicOkHttpClient.fromEnv();

    var system = "You are an AI assistant analyzing a large document. <document>...</document>";
    var prompts = List.of("Summarize section 1.", "Now section 2.", "Now section 3.");

    var messages = new ArrayList<BetaMessageParam>();
    String prevId = null;

    for (var turn = 0; turn < prompts.size(); turn++) {
        messages.add(
            BetaMessageParam.builder()
                .role(BetaMessageParam.Role.USER)
                .content(prompts.get(turn))
                .build()
        );

        var r = client.beta().messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1024)
                .cacheControl(BetaCacheControlEphemeral.builder().build())
                .system(system)
                .messages(messages)
                .diagnostics(BetaDiagnosticsParam.builder().previousMessageId(prevId).build())
                .addBeta(AnthropicBeta.CACHE_DIAGNOSIS_2026_04_07)
                .build()
        );

        if (r.diagnostics().isPresent() && r.diagnostics().get().cacheMissReason().isPresent()) {
            var reason = r.diagnostics().get().cacheMissReason().get();
            // CacheMissReason doesn't expose a typed .type() accessor; read it from the raw JSON.
            @SuppressWarnings("unchecked")
            var json = (Map<String, JsonValue>) reason._json().orElseThrow().asObject().orElseThrow();
            IO.println("Turn " + (turn + 1) + " cache_miss_reason: " + json.get("type").asStringOrThrow());
        }

        messages.add(r.toParam());
        prevId = r.id();
    }
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    $client = new Client();

    $system = 'You are an AI assistant analyzing a large document. <document>...</document>';

    $messages = [];
    $prevId = null;

    foreach (['Summarize section 1.', 'Now section 2.', 'Now section 3.'] as $i => $userMsg) {
        $turn = $i + 1;
        $messages[] = ['role' => 'user', 'content' => $userMsg];

        $r = $client->beta->messages->create(
            model: Model::CLAUDE_OPUS_4_8,
            maxTokens: 1024,
            cacheControl: new BetaCacheControlEphemeral,
            system: $system,
            messages: $messages,
            diagnostics: (new BetaDiagnosticsParam)->withPreviousMessageID($prevId),
            betas: [AnthropicBeta::CACHE_DIAGNOSIS_2026_04_07],
        );

        if ($r->diagnostics?->cacheMissReason !== null) {
            echo "Turn {$turn} cache_miss_reason: {$r->diagnostics->cacheMissReason->type}\n";
        }

        $messages[] = ['role' => 'assistant', 'content' => $r->content];
        $prevId = $r->id;
    }
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    client = Anthropic::Client.new

    SYSTEM = "You are an AI assistant analyzing a large document. <document>...</document>"

    messages = []
    prev_id = nil

    ["Summarize section 1.", "Now section 2.", "Now section 3."].each_with_index do |user_msg, i|
      messages << {role: "user", content: user_msg}

      r = client.beta.messages.create(
        model: :"claude-opus-4-8",
        max_tokens: 1024,
        cache_control: {type: "ephemeral"},
        system_: SYSTEM,
        messages: messages,
        diagnostics: {previous_message_id: prev_id},
        betas: ["cache-diagnosis-2026-04-07"]
      )

      if (reason = r.diagnostics&.cache_miss_reason)
        puts "Turn #{i + 1} cache_miss_reason: #{reason.type}"
      end

      messages << {role: "assistant", content: r.content}
      prev_id = r.id
    end
    ```
  </Tab>
</Tabs>

## Response format

The `diagnostics` field on the response `Message` has four possible states:

| Value                          | Meaning                                                                                                                                                                                         |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| field absent                   | The request did not include `diagnostics`, or the beta header was missing.                                                                                                                      |
| `null`                         | Either `previous_message_id` was `null` (first turn, nothing to compare), or a comparison ran and found no divergence.                                                                          |
| `{"cache_miss_reason": null}`  | The comparison was still running when the response was serialized. This can happen when the response starts very quickly. Treat it as inconclusive and check the next turn.                     |
| `{"cache_miss_reason": {...}}` | A `cache_miss_reason` is attached. For `*_changed` types this identifies the first divergence point; `previous_message_not_found` and `unavailable` are cases where no comparison was produced. |

When `cache_miss_reason` is non-null, it looks like this:

```json
{
  "id": "msg_01Xyz...",
  "type": "message",
  "role": "assistant",
  "content": [{ "type": "text", "text": "..." }],
  "usage": {
    "input_tokens": 42,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 41850,
    "output_tokens": 210
  },
  "diagnostics": {
    "cache_miss_reason": {
      "type": "system_changed",
      "cache_missed_input_tokens": 41850
    }
  }
}
```

## Cache miss reason types

`cache_miss_reason` is a discriminated union on `type`. The response reports the earliest divergence only, so fix it first; later ones may be hidden behind it.

| Type                         | What it means                                                                                                                                                                                                                                                                                                                                                                                                                                   | What to change                                                                                                                                                                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model_changed`              | The `model` differs from the previous request (for example, a router, A/B test, or fallback selected a different model). The cache is per-model.                                                                                                                                                                                                                                                                                                | Hold the model constant within a cached conversation.                                                                                                                                                                                                                              |
| `system_changed`             | The `system` parameter differs. Typically a timestamp, request ID, or other per-request value was interpolated into the system prompt.                                                                                                                                                                                                                                                                                                          | Make the system prompt a byte-stable constant and move dynamic data into the first `user` message after your cache breakpoint.                                                                                                                                                     |
| `tools_changed`              | The `tools` array differs: tools were added, removed, or reordered between turns, or tool `input_schema` JSON was serialized non-deterministically.                                                                                                                                                                                                                                                                                             | Send the same tool list on every turn in a fixed order with deterministically serialized schemas (for example, sort keys).                                                                                                                                                         |
| `messages_changed`           | The model, system, and tools all match, but an earlier entry in `messages` was altered, reordered, or removed rather than appended to. Typically conversation history was truncated or edited, or assistant turns and `tool_result` blocks were re-serialized differently on resend.                                                                                                                                                            | Treat the history as append-only; echo assistant `content` and tool results back verbatim.                                                                                                                                                                                         |
| `previous_message_not_found` | No stored fingerprint exists for the supplied `previous_message_id`. This is not evidence that your request changed. Typically the previous request did not carry the beta header, it came from a different workspace, or too much time has passed since it was sent.                                                                                                                                                                           | Send the beta header on every turn and keep consecutive turns close together in time.                                                                                                                                                                                              |
| `unavailable`                | Diagnostic information was not available for this request. This includes the case where `model`, `system`, and `tools` match but another prompt-affecting request parameter (`tool_choice`, `thinking`, `context_management`, `output_config`, `output_format`, or the set of active `anthropic-beta` headers) differs, and very long conversations where the divergence is beyond the comparison horizon. Your request was processed normally. | Keep the prompt-affecting request parameters constant for the lifetime of a cached conversation. If persistent, apply the manual checks under [Troubleshooting common issues](/docs/en/build-with-claude/prompt-caching#troubleshooting-common-issues) on the prompt caching page. |

<Note>
  The four `*_changed` types also carry a `cache_missed_input_tokens` integer: an estimate of how many input tokens fell after the divergence point, giving you a sense of how much cacheable prefix was lost. It is derived from byte lengths before tokenization, so treat it as a magnitude indicator rather than a billing number. It can differ from (and occasionally exceed) `usage.input_tokens`.
</Note>

## Reading diagnostics alongside usage

`diagnostics` answers "did my request change?" while `usage.cache_read_input_tokens` answers "did the cache hit?". Combining them tells you where to look.

This matrix applies to turns where you passed a real `previous_message_id`. On the first turn (`previous_message_id: null`), `diagnostics` is always `null` and `cache_read_input_tokens` is normally zero because the cache is being written, not read; no troubleshooting is needed. The matrix also does not apply when `cache_miss_reason` is `null` (the comparison is still pending; check the next turn) or when its `type` is `previous_message_not_found` or `unavailable` (no comparison was produced).

| Diagnostics result                        | Cache read tokens | Interpretation                                                                                                                                                                                            |
| ----------------------------------------- | ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `null`                                    | high              | Working as expected. Your prefix is stable and the cache hit.                                                                                                                                             |
| `null`                                    | low or zero       | Your requests match but the cache entry was no longer available. Consider shortening gaps between turns or using the [1-hour cache TTL](/docs/en/build-with-claude/prompt-caching#1-hour-cache-duration). |
| `cache_miss_reason` is a `*_changed` type | low or zero       | Your bug. The request changed; fix the cause indicated by `type`.                                                                                                                                         |
| `cache_miss_reason` is a `*_changed` type | high              | Rare. A change occurred late in the prompt but an earlier `cache_control` breakpoint still hit. Worth fixing, but low impact.                                                                             |

## Limitations

* **Beta:** Field names and semantics may change before general availability.
* **Claude API only:** Not available on Amazon Bedrock or Google Cloud.
* **Limited retention:** Fingerprints for `previous_message_id` lookup expire after a short period. Run diagnostic comparisons between closely spaced requests.
* **Same workspace:** The previous request must have been made with an API key from the same organization and workspace.
* **Comparison horizon:** For very long conversations where the only change is deep in the message list, the response may be `unavailable` rather than a precise location.
* **Best-effort:** Diagnostics never blocks or fails your request. If diagnostic information is not available, the response returns `unavailable`, or `cache_miss_reason: null` when the comparison was still running.

## Data retention

Cache diagnostics is ZDR eligible (qualified). Anthropic does not store the raw text of your prompts or Claude's outputs for this feature.

The fingerprint stored for each request consists only of cryptographic hashes and token-count estimates, keyed by the response `id` and scoped to your organization and workspace. Fingerprints expire after a short period and are not used for any other purpose.

For ZDR eligibility across all features, see [API and data retention](/docs/en/manage-claude/api-and-data-retention).

## See also

* [Prompt caching](/docs/en/build-with-claude/prompt-caching)
* [Token counting](/docs/en/build-with-claude/token-counting)
* [Beta headers](/docs/en/api/beta-headers)
