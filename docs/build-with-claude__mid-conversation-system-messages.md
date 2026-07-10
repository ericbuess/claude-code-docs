# Mid-conversation system messages

Add or update system instructions partway through a conversation without invalidating the cached prefix that came before them.

---

<Note>
  This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

System instructions normally live in the top-level `system` field, ahead of every message in the conversation. That position is great for [prompt caching](/docs/en/build-with-claude/prompt-caching): the system prompt is part of the stable prefix, so subsequent turns hit the cache. It is a poor position for instructions you only discover you need partway through a session, because editing the top-level `system` field changes the very beginning of the prompt and invalidates the cache for everything that follows.

Mid-conversation system messages close that gap. You append a `{"role": "system"}` message at the point in the conversation where the new instruction becomes relevant, instead of editing the top-level `system` field. The cached prefix stays the same, so the next request still reads it from cache, and the new instruction is still applied as a system instruction rather than as ordinary user text.

<Note>
  Mid-conversation system messages are available on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). They are not available on [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) or [Google Cloud](/docs/en/build-with-claude/claude-on-vertex-ai).

  This feature is available on Claude Opus 4.8 only. No beta header is required.
</Note>

## When to use a mid-conversation system message

[Prompt caching](/docs/en/build-with-claude/prompt-caching) hashes the request prefix in order: `tools`, then `system`, then `messages`. A cache hit requires the prefix to match a recent request exactly, byte for byte, up to the cache breakpoint.

That ordering means the top-level `system` field sits near the very start of the hashed prefix. Any change to it, even appending a sentence, produces a different hash, and the request misses the cache for the system prompt and every cached message after it.

Mid-conversation system messages let you add the instruction at the **end** of the message history instead. Everything before the new instruction is unchanged, so the existing cache entry still matches, and only the new message is processed as fresh input.

A few situations where this matters:

* **Mid-session policy or persona changes.** A long agentic session needs a new constraint ("from now on, write all SQL as parameterized queries") after dozens of cached turns. Adding it to the top-level `system` field would re-process the entire history.
* **Per-turn context that must be authoritative.** You want to inject a freshness note, a session deadline, or a tool-availability change with system-level weight, and it changes too often to live in the cached prefix.
* **State changes your application observes.** Your application notices something Claude should treat as an operator-level fact: files changed on disk, the user toggled an auto-approve setting, available tools changed, or the remaining token budget dropped below a threshold.
* **User input that should not interrupt an agentic loop.** A user types a follow-up while Claude is still executing tools for the previous request. Relaying it as a system message after the next tool result lets Claude fold the new input into the work it is already doing, instead of treating it as a fresh request to switch to. See [Placement after tool results](#placement-after-tool-results) below.
* **Mode switches that grant standing permissions.** A session-level mode can use a mid-conversation system message to grant standing consent to an expensive capability, such as automatically launching multi-agent workflows, with a short refresher every several turns and an exit notice when the mode is turned off. For a worked example, see [Build an orchestration mode](/docs/en/build-with-claude/mid-conversation-effort-example).

In all of these cases you could put the instruction in a regular `user` message, and Claude does follow instructions that arrive in user turns. The difference is priority: a `user` message is treated as coming from the end user, while a `system` message is treated as coming from you, the application operator. When the two conflict, system instructions take precedence, so use the `system` role for operator-level facts and constraints that should hold even if the end user asks for something different. A mid-conversation system message keeps that operator-level priority without paying the cache-miss cost of editing the top-level `system` field.

## How it works

Add a message with `"role": "system"` to the `messages` array. Use a plain string or content blocks for `content`, the same as a `user` or `assistant` turn. The instruction applies from that point in the conversation onward. When instructions conflict, later system messages take precedence over earlier ones, and mid-conversation system messages take precedence over the top-level `system` field for the turns that follow them.

You can still set the top-level `system` field for instructions that should apply to the entire conversation. Reserve mid-conversation system messages for instructions that only become relevant later, or that you want to add without invalidating the cached prefix.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "cache_control": {"type": "ephemeral"},
      "system": "You are a code review assistant. Be concise.",
      "messages": [
        {
          "role": "user",
          "content": "Review process() in utils.py for performance issues."
        },
        {
          "role": "assistant",
          "content": "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
        },
        {
          "role": "user",
          "content": "Now review the calling code that invokes process()."
        },
        {
          "role": "system",
          "content": "From now on, every suggestion must include explicit type annotations."
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create --transform 'content.0.text' --raw-output <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  cache_control:
    type: ephemeral
  system: You are a code review assistant. Be concise.
  messages:
    - role: user
      content: Review process() in utils.py for performance issues.
    - role: assistant
      content: >-
        The list comprehension is fine for small inputs. For large inputs,
        consider a generator to avoid materializing the full list.
    - role: user
      content: Now review the calling code that invokes process().
    - role: system
      content: From now on, every suggestion must include explicit type annotations.
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      # Automatic prompt caching: each request caches the conversation so far,
      # and the next request reads the unchanged prefix from cache.
      cache_control={"type": "ephemeral"},
      system="You are a code review assistant. Be concise.",
      messages=[
          {
              "role": "user",
              "content": "Review process() in utils.py for performance issues.",
          },
          {
              "role": "assistant",
              "content": "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.",
          },
          {
              "role": "user",
              "content": "Now review the calling code that invokes process().",
          },
          # The reviewer realizes mid-session that all suggestions must
          # also pass the team's strict typing policy. Appending the
          # instruction here keeps earlier turns byte-identical, so the
          # prefix cached by the previous request is still read from cache.
          {
              "role": "system",
              "content": "From now on, every suggestion must include explicit type annotations.",
          },
      ],
  )

  print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    // Automatic prompt caching: each request caches the conversation so far,
    // and the next request reads the unchanged prefix from cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      {
        role: "user",
        content: "Review process() in utils.py for performance issues."
      },
      {
        role: "assistant",
        content:
          "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
      },
      {
        role: "user",
        content: "Now review the calling code that invokes process()."
      },
      // The reviewer realizes mid-session that all suggestions must also pass
      // the team's strict typing policy. Appending the instruction here keeps
      // earlier turns byte-identical, so the prefix cached by the previous
      // request is still read from cache.
      {
        role: "system",
        content: "From now on, every suggestion must include explicit type annotations."
      }
    ]
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
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      // Automatic prompt caching: each request caches the conversation so far,
      // and the next request reads the unchanged prefix from cache.
      CacheControl = new CacheControlEphemeral(),
      System = "You are a code review assistant. Be concise.",
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = "Review process() in utils.py for performance issues."
          },
          new()
          {
              Role = Role.Assistant,
              Content = "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list."
          },
          new()
          {
              Role = Role.User,
              Content = "Now review the calling code that invokes process()."
          },
          // The reviewer realizes mid-session that all suggestions must also pass
          // the team's strict typing policy. Appending the instruction here keeps
          // earlier turns byte-identical, so the prefix cached by the previous
          // request is still read from cache.
          new()
          {
              Role = Role.System,
              Content = "From now on, every suggestion must include explicit type annotations."
          }
      ]
  };

  var response = await client.Messages.Create(parameters);
  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	// Automatic prompt caching: each request caches the conversation so far,
  	// and the next request reads the unchanged prefix from cache.
  	CacheControl: anthropic.NewCacheControlEphemeralParam(),
  	System: []anthropic.TextBlockParam{
  		{Text: "You are a code review assistant. Be concise."},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Review process() in utils.py for performance issues.")),
  		anthropic.NewAssistantMessage(anthropic.NewTextBlock("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")),
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Now review the calling code that invokes process().")),
  		// The reviewer realizes mid-session that all suggestions must also
  		// pass the team's strict typing policy. Appending the instruction
  		// here keeps earlier turns byte-identical, so the prefix cached by
  		// the previous request is still read from cache.
  		{
  			Role: anthropic.MessageParamRoleSystem,
  			Content: []anthropic.ContentBlockParamUnion{
  				anthropic.NewTextBlock("From now on, every suggestion must include explicit type annotations."),
  			},
  		},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  import com.anthropic.models.messages.CacheControlEphemeral;
  // ...
  import com.anthropic.models.messages.MessageParam;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          // Automatic prompt caching: each request caches the conversation so far,
          // and the next request reads the unchanged prefix from cache.
          .cacheControl(CacheControlEphemeral.builder().build())
          .system("You are a code review assistant. Be concise.")
          .addUserMessage("Review process() in utils.py for performance issues.")
          .addAssistantMessage("The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.")
          .addUserMessage("Now review the calling code that invokes process().")
          // The reviewer realizes mid-session that all suggestions must also pass
          // the team's strict typing policy. Appending the instruction here keeps
          // earlier turns byte-identical, so the prefix cached by the previous
          // request is still read from cache.
          .addMessage(MessageParam.builder()
              .role(MessageParam.Role.SYSTEM)
              .content("From now on, every suggestion must include explicit type annotations.")
              .build())
          .build();

      Message response = client.messages().create(params);
      response.content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> System.out.println(textBlock.text()));
  ```

  ```php PHP
  use Anthropic\Messages\CacheControlEphemeral;
  // ...
  $client = new Client(apiKey: getenv("ANTHROPIC_API_KEY"));

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Review process() in utils.py for performance issues.'],
          ['role' => 'assistant', 'content' => 'The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list.'],
          ['role' => 'user', 'content' => 'Now review the calling code that invokes process().'],
          // The reviewer realizes mid-session that all suggestions must also pass
          // the team's strict typing policy. Appending the instruction here keeps
          // earlier turns byte-identical, so the prefix cached by the previous
          // request is still read from cache.
          ['role' => 'system', 'content' => 'From now on, every suggestion must include explicit type annotations.']
      ],
      model: 'claude-opus-4-8',
      // Automatic prompt caching: each request caches the conversation so far,
      // and the next request reads the unchanged prefix from cache.
      cacheControl: CacheControlEphemeral::with(),
      system: 'You are a code review assistant. Be concise.',
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    # Automatic prompt caching: each request caches the conversation so far,
    # and the next request reads the unchanged prefix from cache.
    cache_control: { type: "ephemeral" },
    system: "You are a code review assistant. Be concise.",
    messages: [
      { role: "user", content: "Review process() in utils.py for performance issues." },
      { role: "assistant", content: "The list comprehension is fine for small inputs. For large inputs, consider a generator to avoid materializing the full list." },
      { role: "user", content: "Now review the calling code that invokes process()." },
      # The reviewer realizes mid-session that all suggestions must also pass
      # the team's strict typing policy. Appending the instruction here keeps
      # earlier turns byte-identical, so the prefix cached by the previous
      # request is still read from cache.
      { role: "system", content: "From now on, every suggestion must include explicit type annotations." }
    ]
  )

  puts response.content.first.text
  ```
</CodeGroup>

This example enables [automatic caching](/docs/en/build-with-claude/prompt-caching#automatic-caching) with the top-level `cache_control` field. Prompt caching is opt-in: if a request has no `cache_control` field (automatic or an [explicit breakpoint](/docs/en/build-with-claude/prompt-caching#explicit-cache-breakpoints)), nothing is cached and every request pays the regular input token price for the full conversation. With caching enabled, appending the system message leaves the already-cached turns unchanged, so the request that carries the new instruction still reads them from cache instead of processing them again. Caching also requires the conversation to meet the [minimum cacheable prompt length](/docs/en/build-with-claude/prompt-caching#cache-limitations); an example as short as this one falls below it, so `cache_creation_input_tokens` and `cache_read_input_tokens` stay at 0 until the conversation grows.

A mid-conversation system message must immediately follow a `user` turn (or an `assistant` turn ending in a server tool use), and must either be the last entry in `messages` or be immediately followed by an `assistant` turn. A `user` message that carries `tool_result` blocks counts: in an agentic loop you can place the system message right after the tool results, before Claude's next turn. The one position that is not allowed is between an `assistant` `tool_use` block and the `tool_result` that answers it.

### Placement after tool results

In an [agentic loop](/docs/en/agents-and-tools/tool-use/overview), the system message goes after the `user` message that delivers the tool results. This is also where your application can relay input that the user typed while Claude was working, so the new context is absorbed without restarting the turn:

```json
[
  { "role": "user", "content": "Run the test suite and fix any failures." },
  {
    "role": "assistant",
    "content": [{ "type": "tool_use", "id": "toolu_01", "name": "run_tests", "input": {} }]
  },
  {
    "role": "user",
    "content": [
      { "type": "tool_result", "tool_use_id": "toolu_01", "content": "12 passed, 0 failed" }
    ]
  },
  {
    "role": "system",
    "content": "The user sent the following message while you were working: also update the changelog before you finish."
  }
]
```

Phrase the system content as context rather than as a command that overrides the user. State the fact ("new input arrived from the user: X", "the remaining token budget is now Y") and let Claude act on it. Claude is trained to resist instructions that appear to work against the user, and that protection still applies to the system role, so language such as "ignore what the user said" is less effective than stating what changed.

This pattern is for relaying input from the conversation's own end user. Do not use it to pass tool output, retrieved documents, or other third-party content; keep that content in `tool_result` blocks (see [Limitations](#limitations)).

## Combining with prompt caching

Mid-conversation system messages and [prompt caching](/docs/en/build-with-claude/prompt-caching) are designed to be used together:

* **Enable caching explicitly.** Caching only happens when the request includes `cache_control`, either the top-level [automatic caching](/docs/en/build-with-claude/prompt-caching#automatic-caching) field or an [explicit breakpoint](/docs/en/build-with-claude/prompt-caching#explicit-cache-breakpoints) on a content block. A mid-conversation system message does not create a cache entry on its own, and without caching enabled there are no savings to preserve.
* **Cache the stable prefix as usual.** Place `cache_control` on the last block that stays the same across requests, whether that is the end of the top-level `system` field, the end of your tool definitions, or a stable point in the message history.
* **Append the system message after the breakpoint.** Because it comes after the cached prefix, it does not change the prefix hash and the cache still hits.
* **A mid-conversation system message is itself cacheable.** Once it is in the conversation, it becomes part of the stable history. On the next turn you can move your cache breakpoint past it (or rely on [automatic caching](/docs/en/build-with-claude/prompt-caching#automatic-caching) to do so) and the system message is read from cache like any other turn.

Avoid editing or removing a mid-conversation system message that has already been sent. Like any other change to earlier messages, that invalidates the cache from that point forward. If the instruction needs to evolve, append a new system message rather than rewriting the old one. Consecutive system messages are not allowed; merge instructions into one message or wait for the next user turn before appending.

## Limitations

* **Not for the first message.** A `system` message cannot be the first entry in `messages`. Use the top-level `system` field for instructions that apply from the very start.
* **Placement is constrained.** A `system` message must immediately follow a `user` turn (including a `user` turn that carries `tool_result` blocks) or an `assistant` turn ending in server tool use, and must precede an `assistant` turn or end the array. It cannot sit between a `tool_use` block and its `tool_result`. Placing it elsewhere returns a 400 error.
* **Not a place for untrusted content.** Claude treats system content as operator instructions and follows it. Do not place text from outside the conversation, such as raw tool output, retrieved documents, or web content, directly in a system message; doing so gives that text operator-level authority. Keep that data in `tool_result` blocks and continue to follow [Mitigate jailbreaks and prompt injections](/docs/en/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks).

## Related

<CardGroup cols={2}>
  <Card title="Prompt caching" icon="bolt" href="/docs/en/build-with-claude/prompt-caching">
    How caching works, where to place breakpoints, and how to read cache usage fields.
  </Card>

  <Card title="Cache diagnostics" icon="magnifying-glass" href="/docs/en/build-with-claude/cache-diagnostics">
    Find out exactly where two requests diverged when a cache hit you expected does not happen.
  </Card>

  <Card title="Using the Messages API" icon="message" href="/docs/en/build-with-claude/working-with-messages">
    Message structure, multi-turn conversations, and the `system` field.
  </Card>

  <Card title="Prompting best practices" icon="text" href="/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices">
    Writing effective prompts and system instructions.
  </Card>

  <Card title="Tool use with Claude" icon="wrench" href="/docs/en/agents-and-tools/tool-use/overview">
    How `tool_use` and `tool_result` blocks are structured in the `messages` array.
  </Card>
</CardGroup>
