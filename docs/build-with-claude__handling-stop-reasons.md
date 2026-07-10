# Stop reasons and fallback

Learn what each stop_reason value means and how to handle truncation, tool use, paused turns, and refusals in your application.

---

Every Messages API response includes a `stop_reason` field that tells you why Claude stopped generating. Check this field to decide whether to use the response as-is, continue the conversation, retry, or fall back to another model.

For the full response schema, see the [Messages API reference](/docs/en/api/messages/create).

## Quick reference

| Value                                                             | When it occurs                                  | What to do                                                                                                           |
| ----------------------------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| [`end_turn`](#end-turn)                                           | Claude finished its response naturally.         | Use the response.                                                                                                    |
| [`max_tokens`](#max-tokens)                                       | The response reached your `max_tokens` limit.   | Raise `max_tokens` or [continue the response](#ensuring-complete-responses).                                         |
| [`stop_sequence`](#stop-sequence)                                 | Claude emitted one of your `stop_sequences`.    | Read `stop_sequence` to see which one fired.                                                                         |
| [`tool_use`](#tool-use)                                           | Claude is calling a tool.                       | Run the tool and return the result. A server tool call still missing its result block completes in a later response. |
| [`pause_turn`](#pause-turn)                                       | A server-tool loop reached its iteration limit. | Send the assistant content back to continue.                                                                         |
| [`refusal`](#refusal)                                             | Claude declined to respond.                     | Read `stop_details` and [retry on a fallback model](/docs/en/build-with-claude/refusals-and-fallback).               |
| [`model_context_window_exceeded`](#model-context-window-exceeded) | The response filled the model's context window. | Treat the response as truncated.                                                                                     |

## The stop\_reason field

The `stop_reason` field is part of every successful Messages API response. Unlike errors, which indicate failures in processing your request, `stop_reason` tells you why Claude completed its response generation.

```json Example response
{
  "id": "msg_01234",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Here's the answer to your question..."
    }
  ],
  "stop_reason": "end_turn",
  "stop_sequence": null,
  "stop_details": null,
  "usage": {
    "input_tokens": 100,
    "output_tokens": 50
  }
}
```

## Stop reason values

### end\_turn

The most common stop reason. Indicates Claude finished its response naturally.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello!"}]
    }' | jq 'if .stop_reason == "end_turn" then .content[0].text else . end'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello!"}' \
    --format json | jq 'if .stop_reason == "end_turn" then .content[0].text else . end'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  if response.stop_reason == "end_turn":
      # Process the complete response
      print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });

  if (response.stop_reason === "end_turn") {
    // Process the complete response
    const block = response.content[0];
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  if (response.StopReason == "end_turn")
  {
      // Process the complete response
      if (response.Content[0].TryPickText(out var textBlock))
      {
          Console.WriteLine(textBlock.Text);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "end_turn" {
  	// Process the complete response
  	if block, ok := response.Content[0].AsAny().(anthropic.TextBlock); ok {
  		fmt.Println(block.Text)
  	}
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("Hello!")
          .build()
  );

  if (response.stopReason().map(StopReason.END_TURN::equals).orElse(false)) {
      // Process the complete response
      response.content().get(0).text().ifPresent(block -> IO.println(block.text()));
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello!']],
      model: 'claude-opus-4-8',
  );

  if ($response->stopReason === 'end_turn') {
      // Process the complete response
      echo $response->content[0]->text, PHP_EOL;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  )

  if response.stop_reason == :end_turn
    # Process the complete response
    puts response.content.first.text
  end
  ```
</CodeGroup>

<Accordion title="Empty responses with end_turn">
  Sometimes Claude returns an empty response (exactly 2-3 tokens with no content) with `stop_reason: "end_turn"`. This typically happens when Claude interprets that the assistant turn is complete, particularly after tool results.

  **Common causes:**

  * Adding text blocks immediately after tool results (Claude learns to expect the user to always insert text after tool results, so it ends its turn to follow the pattern)
  * Sending Claude's completed response back without adding anything (Claude already decided it's done, so it will remain done)

  **How to prevent empty responses:**

  <CodeGroup>
    ```python Python
    # INCORRECT: Adding text immediately after tool_result
    messages = [
        {"role": "user", "content": "Calculate the sum of 1234 and 5678"},
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "toolu_123",
                    "name": "calculator",
                    "input": {"operation": "add", "a": 1234, "b": 5678},
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": "toolu_123", "content": "6912"},
                {
                    "type": "text",
                    "text": "Here's the result",  # Don't add text after tool_result
                },
            ],
        },
    ]

    # CORRECT: Send tool results directly without additional text
    messages = [
        {"role": "user", "content": "Calculate the sum of 1234 and 5678"},
        {
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "toolu_123",
                    "name": "calculator",
                    "input": {"operation": "add", "a": 1234, "b": 5678},
                }
            ],
        },
        {
            "role": "user",
            "content": [
                {"type": "tool_result", "tool_use_id": "toolu_123", "content": "6912"}
            ],
        },  # Just the tool_result, no additional text
    ]
    ```

    ```typescript TypeScript
    // INCORRECT: Adding text immediately after tool_result
    let messages: Anthropic.MessageParam[] = [
      { role: "user", content: "Calculate the sum of 1234 and 5678" },
      {
        role: "assistant",
        content: [
          {
            type: "tool_use",
            id: "toolu_123",
            name: "calculator",
            input: { operation: "add", a: 1234, b: 5678 }
          }
        ]
      },
      {
        role: "user",
        content: [
          { type: "tool_result", tool_use_id: "toolu_123", content: "6912" },
          { type: "text", text: "Here's the result" } // Don't add text after tool_result
        ]
      }
    ];

    // CORRECT: Send tool results directly without additional text
    messages = [
      { role: "user", content: "Calculate the sum of 1234 and 5678" },
      {
        role: "assistant",
        content: [
          {
            type: "tool_use",
            id: "toolu_123",
            name: "calculator",
            input: { operation: "add", a: 1234, b: 5678 }
          }
        ]
      },
      {
        role: "user",
        // Just the tool_result, no additional text
        content: [{ type: "tool_result", tool_use_id: "toolu_123", content: "6912" }]
      }
    ];
    ```

    ```csharp C#
    using System.Text.Json;
    using Anthropic.Models.Messages;

    var input = JsonSerializer.Deserialize<Dictionary<string, JsonElement>>(
        """{"operation":"add","a":1234,"b":5678}"""
    )!;

    // INCORRECT: Adding text immediately after tool_result
    List<MessageParam> messages =
    [
        new() { Role = Role.User, Content = "Calculate the sum of 1234 and 5678" },
        new()
        {
            Role = Role.Assistant,
            Content = new List<ContentBlockParam>
            {
                new ToolUseBlockParam { ID = "toolu_123", Name = "calculator", Input = input }
            }
        },
        new()
        {
            Role = Role.User,
            Content = new List<ContentBlockParam>
            {
                new ToolResultBlockParam { ToolUseID = "toolu_123", Content = "6912" },
                new TextBlockParam { Text = "Here's the result" } // Don't add text after tool_result
            }
        }
    ];

    // CORRECT: Send tool results directly without additional text
    messages =
    [
        new() { Role = Role.User, Content = "Calculate the sum of 1234 and 5678" },
        new()
        {
            Role = Role.Assistant,
            Content = new List<ContentBlockParam>
            {
                new ToolUseBlockParam { ID = "toolu_123", Name = "calculator", Input = input }
            }
        },
        new()
        {
            Role = Role.User,
            // Just the tool_result, no additional text
            Content = new List<ContentBlockParam>
            {
                new ToolResultBlockParam { ToolUseID = "toolu_123", Content = "6912" }
            }
        }
    ];
    ```

    ```go Go
    input := map[string]any{"operation": "add", "a": 1234, "b": 5678}

    // INCORRECT: Adding text immediately after tool_result
    messages := []anthropic.MessageParam{
    	anthropic.NewUserMessage(anthropic.NewTextBlock("Calculate the sum of 1234 and 5678")),
    	anthropic.NewAssistantMessage(
    		anthropic.NewToolUseBlock("toolu_123", input, "calculator"),
    	),
    	anthropic.NewUserMessage(
    		anthropic.NewToolResultBlock("toolu_123", "6912", false),
    		anthropic.NewTextBlock("Here's the result"), // Don't add text after tool_result
    	),
    }

    // CORRECT: Send tool results directly without additional text
    messages = []anthropic.MessageParam{
    	anthropic.NewUserMessage(anthropic.NewTextBlock("Calculate the sum of 1234 and 5678")),
    	anthropic.NewAssistantMessage(
    		anthropic.NewToolUseBlock("toolu_123", input, "calculator"),
    	),
    	// Just the tool_result, no additional text
    	anthropic.NewUserMessage(
    		anthropic.NewToolResultBlock("toolu_123", "6912", false),
    	),
    }
    ```

    ```java Java
    ToolUseBlockParam toolUse = ToolUseBlockParam.builder()
        .id("toolu_123")
        .name("calculator")
        .input(ToolUseBlockParam.Input.builder()
            .putAdditionalProperty("operation", JsonValue.from("add"))
            .putAdditionalProperty("a", JsonValue.from(1234))
            .putAdditionalProperty("b", JsonValue.from(5678))
            .build())
        .build();

    // INCORRECT: Adding text immediately after tool_result
    List<MessageParam> messages = List.of(
        MessageParam.builder().role(MessageParam.Role.USER)
            .content("Calculate the sum of 1234 and 5678").build(),
        MessageParam.builder().role(MessageParam.Role.ASSISTANT)
            .contentOfBlockParams(List.of(ContentBlockParam.ofToolUse(toolUse))).build(),
        MessageParam.builder().role(MessageParam.Role.USER)
            .contentOfBlockParams(List.of(
                ContentBlockParam.ofToolResult(
                    ToolResultBlockParam.builder().toolUseId("toolu_123").content("6912").build()),
                // Don't add text after tool_result
                ContentBlockParam.ofText(TextBlockParam.builder().text("Here's the result").build())
            )).build()
    );

    // CORRECT: Send tool results directly without additional text
    messages = List.of(
        MessageParam.builder().role(MessageParam.Role.USER)
            .content("Calculate the sum of 1234 and 5678").build(),
        MessageParam.builder().role(MessageParam.Role.ASSISTANT)
            .contentOfBlockParams(List.of(ContentBlockParam.ofToolUse(toolUse))).build(),
        // Just the tool_result, no additional text
        MessageParam.builder().role(MessageParam.Role.USER)
            .contentOfBlockParams(List.of(
                ContentBlockParam.ofToolResult(
                    ToolResultBlockParam.builder().toolUseId("toolu_123").content("6912").build())
            )).build()
    );
    ```

    ```php PHP
    // INCORRECT: Adding text immediately after tool_result
    $messages = [
        ['role' => 'user', 'content' => 'Calculate the sum of 1234 and 5678'],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'tool_use',
                    'id' => 'toolu_123',
                    'name' => 'calculator',
                    'input' => ['operation' => 'add', 'a' => 1234, 'b' => 5678],
                ],
            ],
        ],
        [
            'role' => 'user',
            'content' => [
                ['type' => 'tool_result', 'tool_use_id' => 'toolu_123', 'content' => '6912'],
                // Don't add text after tool_result
                ['type' => 'text', 'text' => "Here's the result"],
            ],
        ],
    ];

    // CORRECT: Send tool results directly without additional text
    $messages = [
        ['role' => 'user', 'content' => 'Calculate the sum of 1234 and 5678'],
        [
            'role' => 'assistant',
            'content' => [
                [
                    'type' => 'tool_use',
                    'id' => 'toolu_123',
                    'name' => 'calculator',
                    'input' => ['operation' => 'add', 'a' => 1234, 'b' => 5678],
                ],
            ],
        ],
        [
            'role' => 'user',
            // Just the tool_result, no additional text
            'content' => [
                ['type' => 'tool_result', 'tool_use_id' => 'toolu_123', 'content' => '6912'],
            ],
        ],
    ];
    ```

    ```ruby Ruby
    # INCORRECT: Adding text immediately after tool_result
    messages = [
      { role: "user", content: "Calculate the sum of 1234 and 5678" },
      {
        role: "assistant",
        content: [
          {
            type: "tool_use",
            id: "toolu_123",
            name: "calculator",
            input: { operation: "add", a: 1234, b: 5678 }
          }
        ]
      },
      {
        role: "user",
        content: [
          { type: "tool_result", tool_use_id: "toolu_123", content: "6912" },
          # Don't add text after tool_result
          { type: "text", text: "Here's the result" }
        ]
      }
    ]

    # CORRECT: Send tool results directly without additional text
    messages = [
      { role: "user", content: "Calculate the sum of 1234 and 5678" },
      {
        role: "assistant",
        content: [
          {
            type: "tool_use",
            id: "toolu_123",
            name: "calculator",
            input: { operation: "add", a: 1234, b: 5678 }
          }
        ]
      },
      {
        role: "user",
        # Just the tool_result, no additional text
        content: [
          { type: "tool_result", tool_use_id: "toolu_123", content: "6912" }
        ]
      }
    ]
    ```
  </CodeGroup>

  If you still get empty responses after fixing the message structure, add a continuation prompt in a new user message rather than retrying with the empty response:

  <CodeGroup>
    ```python Python
    def handle_empty_response(client, messages):
        response = client.messages.create(
            model="claude-opus-4-8", max_tokens=1024, messages=messages
        )

        # Check if response is empty
        if response.stop_reason == "end_turn" and not response.content:
            # INCORRECT: Don't just retry with the empty response
            # This won't work because Claude already decided it's done

            # CORRECT: Add a continuation prompt in a NEW user message
            messages.append({"role": "user", "content": "Please continue"})

            response = client.messages.create(
                model="claude-opus-4-8", max_tokens=1024, messages=messages
            )

        return response
    ```

    ```typescript TypeScript
    async function handleEmptyResponse(
      client: Anthropic,
      messages: Anthropic.MessageParam[]
    ): Promise<Anthropic.Message> {
      let response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages
      });

      // Check if response is empty
      if (response.stop_reason === "end_turn" && response.content.length === 0) {
        // INCORRECT: Don't just retry with the empty response
        // This won't work because Claude already decided it's done

        // CORRECT: Add a continuation prompt in a NEW user message
        messages.push({ role: "user", content: "Please continue" });

        response = await client.messages.create({
          model: "claude-opus-4-8",
          max_tokens: 1024,
          messages
        });
      }

      return response;
    }
    ```

    ```csharp C#
    static async Task<Message> HandleEmptyResponse(AnthropicClient client, List<MessageParam> messages)
    {
        var response = await client.Messages.Create(new MessageCreateParams
        {
            Model = Model.ClaudeOpus4_8,
            MaxTokens = 1024,
            Messages = messages
        });

        // Check if response is empty
        if (response.StopReason == "end_turn" && response.Content.Count == 0)
        {
            // CORRECT: Add a continuation prompt in a NEW user message
            messages.Add(new() { Role = Role.User, Content = "Please continue" });

            response = await client.Messages.Create(new MessageCreateParams
            {
                Model = Model.ClaudeOpus4_8,
                MaxTokens = 1024,
                Messages = messages
            });
        }

        return response;
    }
    ```

    ```go Go
    func handleEmptyResponse(client anthropic.Client, messages []anthropic.MessageParam) (*anthropic.Message, error) {
    	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_8,
    		MaxTokens: 1024,
    		Messages:  messages,
    	})
    	if err != nil {
    		return nil, err
    	}

    	// Check if response is empty
    	if response.StopReason == "end_turn" && len(response.Content) == 0 {
    		// CORRECT: Add a continuation prompt in a NEW user message
    		messages = append(messages, anthropic.NewUserMessage(anthropic.NewTextBlock("Please continue")))

    		response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    			Model:     anthropic.ModelClaudeOpus4_8,
    			MaxTokens: 1024,
    			Messages:  messages,
    		})
    		if err != nil {
    			return nil, err
    		}
    	}

    	return response, nil
    }
    ```

    ```java Java
    static Message handleEmptyResponse(AnthropicClient client, List<MessageParam> messages) {
        Message response = client.messages().create(
            MessageCreateParams.builder()
                .model(Model.CLAUDE_OPUS_4_8)
                .maxTokens(1024L)
                .messages(messages)
                .build()
        );

        // Check if response is empty
        boolean isEndTurn = response.stopReason().map(StopReason.END_TURN::equals).orElse(false);
        if (isEndTurn && response.content().isEmpty()) {
            // CORRECT: Add a continuation prompt in a NEW user message
            List<MessageParam> extended = new ArrayList<>(messages);
            extended.add(MessageParam.builder()
                .role(MessageParam.Role.USER)
                .content("Please continue")
                .build());

            response = client.messages().create(
                MessageCreateParams.builder()
                    .model(Model.CLAUDE_OPUS_4_8)
                    .maxTokens(1024L)
                    .messages(extended)
                    .build()
            );
        }

        return response;
    }
    ```

    ```php PHP
    function handle_empty_response(Client $client, array $messages)
    {
        $response = $client->messages->create(
            maxTokens: 1024,
            messages: $messages,
            model: 'claude-opus-4-8',
        );

        // Check if response is empty
        if ($response->stopReason === 'end_turn' && count($response->content) === 0) {
            // CORRECT: Add a continuation prompt in a NEW user message
            $messages[] = ['role' => 'user', 'content' => 'Please continue'];

            $response = $client->messages->create(
                maxTokens: 1024,
                messages: $messages,
                model: 'claude-opus-4-8',
            );
        }

        return $response;
    }
    ```

    ```ruby Ruby
    def handle_empty_response(client, messages)
      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: messages
      )

      # Check if response is empty
      if response.stop_reason == :end_turn && response.content.empty?
        # CORRECT: Add a continuation prompt in a NEW user message
        messages << { role: "user", content: "Please continue" }

        response = client.messages.create(
          model: "claude-opus-4-8",
          max_tokens: 1024,
          messages: messages
        )
      end

      response
    end
    ```
  </CodeGroup>

  **Best practices:**

  1. **Never add text blocks immediately after tool results:** This teaches Claude to expect user input after every tool use.
  2. **Don't retry empty responses without modification:** Sending the empty response back won't help.
  3. **Use continuation prompts as a last resort:** Only if these fixes don't resolve the issue.
</Accordion>

### max\_tokens

Claude stopped because it reached the `max_tokens` limit specified in your request.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 10,
      "messages": [{"role": "user", "content": "Explain quantum physics"}]
    }' | jq '.stop_reason'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 10 \
    --message '{role: user, content: "Explain quantum physics"}' \
    --format json | jq '.stop_reason'
  ```

  ```python Python
  client = anthropic.Anthropic()
  # Request with limited tokens
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=10,
      messages=[{"role": "user", "content": "Explain quantum physics"}],
  )

  if response.stop_reason == "max_tokens":
      # Response was truncated
      print("Response was cut off at token limit")
      # Consider making another request to continue
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Request with limited tokens
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 10,
    messages: [{ role: "user", content: "Explain quantum physics" }]
  });

  if (response.stop_reason === "max_tokens") {
    // Response was truncated
    console.log("Response was cut off at token limit");
    // Consider making another request to continue
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Request with limited tokens
  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 10,
      Messages = [new() { Role = Role.User, Content = "Explain quantum physics" }]
  });

  if (response.StopReason == "max_tokens")
  {
      // Response was truncated
      Console.WriteLine("Response was cut off at token limit");
      // Consider making another request to continue
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  // Request with limited tokens
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 10,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Explain quantum physics")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "max_tokens" {
  	// Response was truncated
  	fmt.Println("Response was cut off at token limit")
  	// Consider making another request to continue
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // Request with limited tokens
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(10L)
          .addUserMessage("Explain quantum physics")
          .build()
  );

  if (response.stopReason().map(StopReason.MAX_TOKENS::equals).orElse(false)) {
      // Response was truncated
      IO.println("Response was cut off at token limit");
      // Consider making another request to continue
  }
  ```

  ```php PHP
  $client = new Client();

  // Request with limited tokens
  $response = $client->messages->create(
      maxTokens: 10,
      messages: [['role' => 'user', 'content' => 'Explain quantum physics']],
      model: 'claude-opus-4-8',
  );

  if ($response->stopReason === 'max_tokens') {
      // Response was truncated
      echo 'Response was cut off at token limit', PHP_EOL;
      // Consider making another request to continue
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  # Request with limited tokens
  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 10,
    messages: [{ role: "user", content: "Explain quantum physics" }]
  )

  if response.stop_reason == :max_tokens
    # Response was truncated
    puts "Response was cut off at token limit"
    # Consider making another request to continue
  end
  ```
</CodeGroup>

<Accordion title="Incomplete tool use blocks">
  If Claude's response is cut off due to hitting the `max_tokens` limit, and the truncated response contains an incomplete tool use block, you'll need to retry the request with a higher `max_tokens` value to get the full tool use.

  <CodeGroup>
    ```bash CLI
    RESPONSE=$(ant messages create --max-tokens 1024 \
      --format jsonl < request.yaml)

    # Check if the response was truncated mid tool use
    STOP_REASON=$(jq -r '.stop_reason' <<<"$RESPONSE")
    LAST_TYPE=$(jq -r '.content[-1].type' <<<"$RESPONSE")
    if [ "$STOP_REASON" = "max_tokens" ] && [ "$LAST_TYPE" = "tool_use" ]; then
      # Retry with a higher max_tokens
      ant messages create --max-tokens 4096 < request.yaml
    fi
    ```

    ```python Python
    # Check if response was truncated during tool use
    if response.stop_reason == "max_tokens":
        # Check if the last content block is an incomplete tool_use
        last_block = response.content[-1]
        if last_block.type == "tool_use":
            # Send the request with higher max_tokens
            response = client.messages.create(
                model="claude-opus-4-8",
                max_tokens=4096,  # Increased limit
                messages=messages,
                tools=tools,
            )
    ```

    ```typescript TypeScript
    // Check if response was truncated during tool use
    if (response.stop_reason === "max_tokens") {
      // Check if the last content block is an incomplete tool_use
      const lastBlock = response.content[response.content.length - 1];
      if (lastBlock.type === "tool_use") {
        // Send the request with higher max_tokens
        response = await client.messages.create({
          model: "claude-opus-4-8",
          max_tokens: 4096, // Increased limit
          messages: messages,
          tools: tools
        });
      }
    }
    ```

    ```csharp C#
    using System.Linq;
    using Anthropic;
    using Anthropic.Models.Messages;

    AnthropicClient client = new();

    var parameters = new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages = messages,
        Tools = tools
    };

    var response = await client.Messages.Create(parameters);

    if (response.StopReason == "max_tokens")
    {
        var lastBlock = response.Content.Last();
        if (lastBlock.TryPickToolUse(out _))
        {
            response = await client.Messages.Create(parameters with { MaxTokens = 4096 });
        }
    }
    ```

    ```go Go
    response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    	Model:     anthropic.ModelClaudeOpus4_8,
    	MaxTokens: 1024,
    	Messages:  messages,
    	Tools:     tools,
    })
    if err != nil {
    	log.Fatal(err)
    }

    if response.StopReason == "max_tokens" {
    	lastBlock := response.Content[len(response.Content)-1]
    	switch lastBlock.AsAny().(type) {
    	case anthropic.ToolUseBlock:
    		response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    			Model:     anthropic.ModelClaudeOpus4_8,
    			MaxTokens: 4096,
    			Messages:  messages,
    			Tools:     tools,
    		})
    		if err != nil {
    			log.Fatal(err)
    		}
    	}
    }
    ```

    ```java Java
    // Check if response was truncated during tool use
    if (response.stopReason().isPresent() && response.stopReason().get().equals(StopReason.MAX_TOKENS)) {
        ContentBlock lastBlock = response.content().get(response.content().size() - 1);
        if (lastBlock.toolUse().isPresent()) {
            // Send the request with higher max_tokens
            response = client.messages().create(
                MessageCreateParams.builder()
                    .model(Model.CLAUDE_OPUS_4_8)
                    .maxTokens(4096L) // Increased limit
                    .messages(messages)
                    .tools(tools)
                    .build()
            );
        }
    }
    ```

    ```php PHP
    $response = $client->messages->create(
        maxTokens: 1024,
        messages: $messages,
        model: 'claude-opus-4-8',
        tools: $tools,
    );

    if ($response->stopReason === 'max_tokens') {
        $lastBlock = end($response->content);
        if ($lastBlock->type === 'tool_use') {
            $response = $client->messages->create(
                maxTokens: 4096,
                messages: $messages,
                model: 'claude-opus-4-8',
                tools: $tools,
            );
        }
    }
    ```

    ```ruby Ruby
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: messages,
      tools: tools
    )

    if response.stop_reason == :max_tokens
      last_block = response.content.last
      if last_block.type == :tool_use
        response = client.messages.create(
          model: "claude-opus-4-8",
          max_tokens: 4096,
          messages: messages,
          tools: tools
        )
      end
    end
    ```
  </CodeGroup>
</Accordion>

### stop\_sequence

Claude encountered one of your custom stop sequences.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "stop_sequences": ["END", "STOP"],
      "messages": [{"role": "user", "content": "Generate text until you say END"}]
    }' | jq '{stop_reason, stop_sequence}'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --stop-sequence END --stop-sequence STOP \
    --message '{role: user, content: "Generate text until you say END"}' \
    --format json | jq '{stop_reason, stop_sequence}'
  ```

  ```python Python
  client = anthropic.Anthropic()
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      stop_sequences=["END", "STOP"],
      messages=[{"role": "user", "content": "Generate text until you say END"}],
  )

  if response.stop_reason == "stop_sequence":
      print(f"Stopped at sequence: {response.stop_sequence}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    stop_sequences: ["END", "STOP"],
    messages: [{ role: "user", content: "Generate text until you say END" }]
  });

  if (response.stop_reason === "stop_sequence") {
    console.log(`Stopped at sequence: ${response.stop_sequence}`);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      StopSequences = ["END", "STOP"],
      Messages = [new() { Role = Role.User, Content = "Generate text until you say END" }]
  });

  if (response.StopReason == "stop_sequence")
  {
      Console.WriteLine($"Stopped at sequence: {response.StopSequence}");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:         anthropic.ModelClaudeOpus4_8,
  	MaxTokens:     1024,
  	StopSequences: []string{"END", "STOP"},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Generate text until you say END")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "stop_sequence" {
  	fmt.Printf("Stopped at sequence: %s\n", response.StopSequence)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addStopSequence("END")
          .addStopSequence("STOP")
          .addUserMessage("Generate text until you say END")
          .build()
  );

  if (response.stopReason().map(StopReason.STOP_SEQUENCE::equals).orElse(false)) {
      IO.println("Stopped at sequence: " + response.stopSequence().orElse(""));
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Generate text until you say END']],
      model: 'claude-opus-4-8',
      stopSequences: ['END', 'STOP'],
  );

  if ($response->stopReason === 'stop_sequence') {
      echo "Stopped at sequence: {$response->stopSequence}", PHP_EOL;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    stop_sequences: ["END", "STOP"],
    messages: [{ role: "user", content: "Generate text until you say END" }]
  )

  if response.stop_reason == :stop_sequence
    puts "Stopped at sequence: #{response.stop_sequence}"
  end
  ```
</CodeGroup>

### tool\_use

Claude is calling a tool and expects you to execute it.

<Note>
  For most tool use implementations, use the [tool runner](/docs/en/agents-and-tools/tool-use/tool-runner), which automatically handles tool execution, result formatting, and conversation management.
</Note>

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "tools": [{
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {"location": {"type": "string", "description": "City and state"}},
          "required": ["location"]
        }
      }],
      "messages": [{"role": "user", "content": "What is the weather in San Francisco?"}]
    }' | jq '.stop_reason, (.content[] | select(.type == "tool_use"))'
  ```

  ```bash CLI
  ant messages create --format json <<'YAML' | jq '.stop_reason, (.content[] | select(.type == "tool_use"))'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: What is the weather in San Francisco?
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location: {type: string, description: City and state}
        required: [location]
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()
  weather_tool = {
      "name": "get_weather",
      "description": "Get the current weather in a given location",
      "input_schema": {
          "type": "object",
          "properties": {
              "location": {"type": "string", "description": "City and state"},
          },
          "required": ["location"],
      },
  }


  def execute_tool(name, tool_input):
      """Execute a tool and return the result."""
      return f"Weather in {tool_input.get('location', 'unknown')}: 72°F"


  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      tools=[weather_tool],
      messages=[{"role": "user", "content": "What is the weather in San Francisco?"}],
  )

  if response.stop_reason == "tool_use":
      # Extract and execute the tool
      for block in response.content:
          if block.type == "tool_use":
              result = execute_tool(block.name, block.input)
              # Return result to Claude for final response
  ```

  ```typescript TypeScript
  const client = new Anthropic();
  const weatherTool: Anthropic.Tool = {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: { type: "string", description: "City and state" }
      },
      required: ["location"]
    }
  };

  function executeTool(name: string, input: Record<string, string>): string {
    return `Weather in ${input.location ?? "unknown"}: 72°F`;
  }

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [weatherTool],
    messages: [{ role: "user", content: "What is the weather in San Francisco?" }]
  });

  if (response.stop_reason === "tool_use") {
    // Extract and execute the tool
    for (const block of response.content) {
      if (block.type === "tool_use") {
        const result = executeTool(block.name, block.input as Record<string, string>);
        // Return result to Claude for final response
      }
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var weatherTool = new Tool
  {
      Name = "get_weather",
      Description = "Get the current weather in a given location",
      InputSchema = new InputSchema
      {
          Properties = new Dictionary<string, JsonElement>
          {
              ["location"] = JsonSerializer.SerializeToElement(
                  new { type = "string", description = "City and state" }
              ),
          },
          Required = ["location"]
      }
  };

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Tools = [weatherTool],
      Messages = [new() { Role = Role.User, Content = "What is the weather in San Francisco?" }]
  });

  if (response.StopReason == "tool_use")
  {
      // Extract and execute the tool
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              // Execute toolUse.Name with toolUse.Input and return the result to Claude
          }
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  weatherTool := anthropic.ToolParam{
  	Name:        "get_weather",
  	Description: anthropic.String("Get the current weather in a given location"),
  	InputSchema: anthropic.ToolInputSchemaParam{
  		Properties: map[string]any{
  			"location": map[string]string{"type": "string", "description": "City and state"},
  		},
  		Required: []string{"location"},
  	},
  }

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Tools:     []anthropic.ToolUnionParam{{OfTool: &weatherTool}},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What is the weather in San Francisco?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "tool_use" {
  	// Extract and execute the tool
  	for _, block := range response.Content {
  		if toolUse, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  			fmt.Println(toolUse.Name, toolUse.Input)
  			// Return result to Claude for final response
  		}
  	}
  }
  ```

  ```java Java
  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool weatherTool = Tool.builder()
          .name("get_weather")
          .description("Get the current weather in a given location")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "location", Map.of("type", "string", "description", "City and state")
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("location")))
              .build())
          .build();

      Message response = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(weatherTool)
              .addUserMessage("What is the weather in San Francisco?")
              .build()
      );

      if (response.stopReason().map(StopReason.TOOL_USE::equals).orElse(false)) {
          // Extract and execute the tool
          for (ContentBlock block : response.content()) {
              block.toolUse().ifPresent(toolUse -> {
                  // Execute toolUse.name() with toolUse.input() and return the result to Claude
              });
          }
      }
  ```

  ```php PHP
  $client = new Client();

  $weatherTool = [
      'name' => 'get_weather',
      'description' => 'Get the current weather in a given location',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'location' => ['type' => 'string', 'description' => 'City and state'],
          ],
          'required' => ['location'],
      ],
  ];

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'What is the weather in San Francisco?']],
      model: 'claude-opus-4-8',
      tools: [$weatherTool],
  );

  if ($response->stopReason === 'tool_use') {
      // Extract and execute the tool
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              // Execute $block->name with $block->input and return the result to Claude
          }
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  weather_tool = {
    name: "get_weather",
    description: "Get the current weather in a given location",
    input_schema: {
      type: "object",
      properties: {
        location: { type: "string", description: "City and state" }
      },
      required: ["location"]
    }
  }

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [weather_tool],
    messages: [{ role: "user", content: "What is the weather in San Francisco?" }]
  )

  if response.stop_reason == :tool_use
    # Extract and execute the tool
    response.content.each do |block|
      next unless block.type == :tool_use
      # Execute block.name with block.input and return the result to Claude
    end
  end
  ```
</CodeGroup>

A `tool_use` response can also contain a `server_tool_use` block whose `id` has no matching result block. That server tool call is not finished, and this response does not carry its result. In the common case, Claude calls a [server tool](/docs/en/agents-and-tools/tool-use/server-tools) and one of your client tools in the same group of parallel tool calls: the API returns without running the server tool so that you can run the client tools first. There is no other marker for the state; detect it by checking each `server_tool_use` or `mcp_tool_use` block's `id` for a matching result block.

<Note>
  With [programmatic tool calling](/docs/en/agents-and-tools/tool-use/programmatic-tool-calling), the same response shape means something different. The client `tool_use` block comes from code that is running in the `code_execution` tool rather than from Claude directly, and its `caller` field names the `code_execution` block that called it. That code has already started: it is paused waiting for your `tool_result` blocks, and sending them resumes the execution instead of starting a deferred tool. The `code_execution` block's own result block arrives once the code finishes, which can take more than one round of tool results. The follow-up user message itself is the same in both cases; with programmatic tool calling, also pass back the `id` from the response's `container` field, as that page shows.
</Note>

```json A mixed tool_use response
{
  "stop_reason": "tool_use",
  "content": [
    {
      "type": "server_tool_use",
      "id": "srvtoolu_01HxbWnMRmbWyMfUtJKC45rA",
      "name": "web_fetch",
      "input": { "url": "https://example.com/article" }
    },
    {
      "type": "tool_use",
      "id": "toolu_01PjgRJLbXrXEMZwDNYLnBqk",
      "name": "run_command",
      "input": { "command": "uname -a" }
    }
  ]
}
```

The continuation is a user message of `tool_result` blocks, one for every `tool_use` block in the response (see [Handle tool calls](/docs/en/agents-and-tools/tool-use/handle-tool-calls)), with two extra rules: that message must contain nothing except the `tool_result` blocks, and the request must keep the same `tools` array. A resume request that no longer defines the waiting server tool fails with a 400 whose message ends ``but no `web_fetch` tool was provided``. The API attaches your results to the still-open assistant turn, runs the deferred server tool (for paused code execution, resumes it), and continues the turn. For a server tool Claude called directly, the next response's `content` starts with the result block that answers the previous response's `server_tool_use` `id`.

```json The follow-up user message
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_01PjgRJLbXrXEMZwDNYLnBqk",
      "content": "Linux demo-host 6.8.0-52-generic x86_64 GNU/Linux"
    }
  ]
}
```

Adding anything after the `tool_result` blocks in that user message, such as text, ends the assistant turn; for a server tool Claude called directly, the request then fails with a 400 `invalid_request_error` that names the unresolved server tool:

```text wrap
`web_fetch` tool use with id `srvtoolu_01HxbWnMRmbWyMfUtJKC45rA` was found without a corresponding `web_fetch_tool_result` block
```

Leaving out a `tool_result`, or putting one after other content, fails earlier with the standard `tool_use ids were found without tool_result blocks immediately after` error instead. To give Claude more input, send it as a separate user message after the turn completes.

### pause\_turn

Returned when the server-side sampling loop reaches its iteration limit while executing [server tools](/docs/en/agents-and-tools/tool-use/server-tools) like web search or web fetch. The default limit is 10 iterations per request.

When this happens, the response may contain a `server_tool_use` block without a corresponding result block. To let Claude finish processing, continue the conversation by sending the response back as-is. A response that leaves a client `tool_use` block waiting on you never has a `stop_reason` of `pause_turn`: when Claude stops to call your tools, `stop_reason` is [`tool_use`](#tool-use), and you continue it by sending the client `tool_result` blocks instead of the response itself.

<CodeGroup>
  ```bash cURL
  # The SDKs handle continuation directly. With cURL, inspect stop_reason
  # on the response and re-POST with the assistant content appended.
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 4096,
      "tools": [{"type": "web_search_20250305", "name": "web_search"}],
      "messages": [{"role": "user", "content": "Search for latest AI news"}]
    }' | jq '{stop_reason, content}'
  ```

  ```bash CLI
  # Inspect stop_reason; if it is pause_turn, re-run with the assistant
  # response appended to --message.
  ant messages create --format json <<'YAML' | jq '{stop_reason, content}'
  model: claude-opus-4-8
  max_tokens: 4096
  tools:
    - {type: web_search_20250305, name: web_search}
  messages:
    - {role: user, content: "Search for latest AI news"}
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=4096,
      tools=[{"type": "web_search_20250305", "name": "web_search"}],
      messages=[{"role": "user", "content": "Search for latest AI news"}],
  )

  if response.stop_reason == "pause_turn":
      # Continue the conversation by sending the response back
      messages = [
          {"role": "user", "content": "Search for latest AI news"},
          {"role": "assistant", "content": response.content},
      ]
      continuation = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=4096,
          messages=messages,
          tools=[{"type": "web_search_20250305", "name": "web_search"}],
      )
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 4096,
    tools: [{ type: "web_search_20250305", name: "web_search" }],
    messages: [{ role: "user", content: "Search for latest AI news" }]
  });

  if (response.stop_reason === "pause_turn") {
    // Continue the conversation by sending the response back
    const continuation = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 4096,
      tools: [{ type: "web_search_20250305", name: "web_search" }],
      messages: [
        { role: "user", content: "Search for latest AI news" },
        { role: "assistant", content: response.content }
      ]
    });
  }
  ```

  ```csharp C#
  List<ToolUnion> tools = [new ToolUnion(new WebSearchTool20250305())];
  MessageParam userMessage = new() { Role = Role.User, Content = "Search for latest AI news" };

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 4096,
      Tools = tools,
      Messages = [userMessage]
  });

  if (response.StopReason == "pause_turn")
  {
      // Continue the conversation by sending the response back
      var continuation = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 4096,
          Tools = tools,
          Messages =
          [
              userMessage,
              new()
              {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              }
          ]
      });
  }
  ```

  ```go Go
  tools := []anthropic.ToolUnionParam{
  	{OfWebSearchTool20250305: &anthropic.WebSearchTool20250305Param{}},
  }
  userMessage := anthropic.NewUserMessage(anthropic.NewTextBlock("Search for latest AI news"))

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 4096,
  	Tools:     tools,
  	Messages:  []anthropic.MessageParam{userMessage},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "pause_turn" {
  	// Continue the conversation by sending the response back
  	var contentParams []anthropic.ContentBlockParamUnion
  	for _, block := range response.Content {
  		contentParams = append(contentParams, block.ToParam())
  	}
  	continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 4096,
  		Tools:     tools,
  		Messages:  []anthropic.MessageParam{userMessage, anthropic.NewAssistantMessage(contentParams...)},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}
  	_ = continuation
  }
  ```

  ```java Java
  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(4096L)
          .addTool(WebSearchTool20250305.builder().build())
          .addUserMessage("Search for latest AI news")
          .build()
  );

  if (response.stopReason().map(StopReason.PAUSE_TURN::equals).orElse(false)) {
      // Continue the conversation by sending the response back
      Message continuation = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .addTool(WebSearchTool20250305.builder().build())
              .addUserMessage("Search for latest AI news")
              .addMessage(response)
              .build()
      );
  }
  ```

  ```php PHP
  $tools = [['type' => 'web_search_20250305', 'name' => 'web_search']];
  $userMessage = ['role' => 'user', 'content' => 'Search for latest AI news'];

  $response = $client->messages->create(
      maxTokens: 4096,
      messages: [$userMessage],
      model: 'claude-opus-4-8',
      tools: $tools,
  );

  if ($response->stopReason === 'pause_turn') {
      // Continue the conversation by sending the response back
      $continuation = $client->messages->create(
          maxTokens: 4096,
          messages: [
              $userMessage,
              ['role' => 'assistant', 'content' => $response->content],
          ],
          model: 'claude-opus-4-8',
          tools: $tools,
      );
  }
  ```

  ```ruby Ruby
  tools = [{ type: "web_search_20250305", name: "web_search" }]
  user_message = { role: "user", content: "Search for latest AI news" }

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 4096,
    tools: tools,
    messages: [user_message]
  )

  if response.stop_reason == :pause_turn
    # Continue the conversation by sending the response back
    continuation = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 4096,
      tools: tools,
      messages: [user_message, { role: "assistant", content: response.content }]
    )
  end
  ```
</CodeGroup>

<Note>
  Your application should handle `pause_turn` in any agent loop that uses server tools. Add the assistant's response to your messages array and make another API request to let Claude continue.
</Note>

### refusal

Claude declined to generate a response. On Claude Fable 5, safety classifiers return this stop reason as a normal HTTP 200 response, not an error.

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "[Unsafe request]"}]
    }' | jq '{stop_reason, stop_details}'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "[Unsafe request]"}' \
    --format json | jq '{stop_reason, stop_details}'
  ```

  ```python Python
  client = anthropic.Anthropic()
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "[Unsafe request]"}],
  )

  if response.stop_reason == "refusal":
      # Claude declined to respond
      print("Claude was unable to process this request")
      # Consider rephrasing or modifying the request
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "[Unsafe request]" }]
  });

  if (response.stop_reason === "refusal") {
    // Claude declined to respond
    console.log("Claude was unable to process this request");
    // Consider rephrasing or modifying the request
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "[Unsafe request]" }]
  });

  if (response.StopReason == "refusal")
  {
      // Claude declined to respond
      Console.WriteLine("Claude was unable to process this request");
      // Consider rephrasing or modifying the request
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("[Unsafe request]")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == "refusal" {
  	// Claude declined to respond
  	fmt.Println("Claude was unable to process this request")
  	// Consider rephrasing or modifying the request
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  Message response = client.messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024L)
          .addUserMessage("[Unsafe request]")
          .build()
  );

  if (response.stopReason().map(StopReason.REFUSAL::equals).orElse(false)) {
      // Claude declined to respond
      IO.println("Claude was unable to process this request");
      // Consider rephrasing or modifying the request
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => '[Unsafe request]']],
      model: 'claude-opus-4-8',
  );

  if ($response->stopReason === 'refusal') {
      // Claude declined to respond
      echo 'Claude was unable to process this request', PHP_EOL;
      // Consider rephrasing or modifying the request
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "[Unsafe request]" }]
  )

  if response.stop_reason == :refusal
    # Claude declined to respond
    puts "Claude was unable to process this request"
    # Consider rephrasing or modifying the request
  end
  ```
</CodeGroup>

<Tip>
  If you encounter `refusal` stop reasons frequently while using Claude Sonnet 4.5 or Opus 4.1 ([deprecated](/docs/en/about-claude/model-deprecations)), you can try updating your API calls to use Haiku 4.5 (`claude-haiku-4-5-20251001`), which has different usage restrictions. Learn more about [understanding Sonnet 4.5's API safety filters](https://support.claude.com/en/articles/12449294-understanding-sonnet-4-5-s-api-safety-filters).
</Tip>

On a refusal, the `stop_details` object identifies the policy category that triggered it. The categories and the full refusal response shape are covered on [Refusals and fallback](/docs/en/build-with-claude/refusals-and-fallback#refusal-response). `stop_details` is `null` for all stop reasons other than `refusal`.

A refused request on Claude Fable 5 can usually be served by retrying on another Claude model, and [Refusals and fallback](/docs/en/build-with-claude/refusals-and-fallback) shows how to set up that retry, server-side or in your client. [Fallback credit](/docs/en/build-with-claude/fallback-credit) covers how to avoid paying the prompt-cache cost twice when you build the retry yourself.

### model\_context\_window\_exceeded

Claude stopped because it reached the model's context window limit. This lets you request the maximum possible tokens without knowing the exact input size.

<Note>
  This stop reason is currently typed only in the SDKs' `beta` namespace, so the following examples call `client.beta.messages` and use the `Beta`-prefixed types. On Sonnet 4.5 and newer models the API returns this value without a beta header. For earlier models, add the `model-context-window-exceeded-2025-08-26` beta header to enable it.
</Note>

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 20000,
      "messages": [{"role": "user", "content": "Large input that uses most of context window..."}]
    }' | jq '.stop_reason'
  ```

  ```bash CLI
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 20000 \
    --message '{role: user, content: "Large input that uses most of context window..."}' \
    --format json | jq '.stop_reason'
  ```

  ```python Python
  # Request with maximum tokens to get as much as possible
  response = client.beta.messages.create(
      model="claude-opus-4-8",
      max_tokens=20000,  # Python SDK requires streaming for max_tokens above ~21k (Opus 4.8 supports 128k with streaming)
      messages=[
          {"role": "user", "content": "Large input that uses most of context window..."}
      ],
  )

  if response.stop_reason == "model_context_window_exceeded":
      # Response hit context window limit before max_tokens
      print("Response reached model's context window limit")
      # The response is still valid but was limited by context window
  ```

  ```typescript TypeScript
  // Request with maximum tokens to get as much as possible
  const response = await client.beta.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 20000,
    messages: [{ role: "user", content: "Large input that uses most of context window..." }]
  });

  if (response.stop_reason === "model_context_window_exceeded") {
    // Response hit context window limit before max_tokens
    console.log("Response reached model's context window limit");
    // The response is still valid but was limited by context window
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  // Request with maximum tokens to get as much as possible
  var response = await client.Beta.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 20000,
      Messages = [new() { Role = Role.User, Content = "Large input that uses most of context window..." }]
  });

  if (response.StopReason?.Value() == BetaStopReason.ModelContextWindowExceeded)
  {
      // Response hit context window limit before max_tokens
      Console.WriteLine("Response reached model's context window limit");
      // The response is still valid but was limited by context window
  }
  ```

  ```go Go
  // Request with maximum tokens to get as much as possible
  response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 20000,
  	Messages: []anthropic.BetaMessageParam{
  		anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock("Large input that uses most of context window...")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  if response.StopReason == anthropic.BetaStopReasonModelContextWindowExceeded {
  	// Response hit context window limit before max_tokens
  	fmt.Println("Response reached model's context window limit")
  	// The response is still valid but was limited by context window
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  // Request with maximum tokens to get as much as possible
  BetaMessage response = client.beta().messages().create(
      MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(20000L)
          .addUserMessage("Large input that uses most of context window...")
          .build()
  );

  if (response.stopReason().map(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED::equals).orElse(false)) {
      // Response hit context window limit before max_tokens
      IO.println("Response reached model's context window limit");
      // The response is still valid but was limited by context window
  }
  ```

  ```php PHP
  // Request with maximum tokens to get as much as possible
  $response = $client->beta->messages->create(
      maxTokens: 20000,
      messages: [['role' => 'user', 'content' => 'Large input that uses most of context window...']],
      model: 'claude-opus-4-8',
  );

  if ($response->stopReason === 'model_context_window_exceeded') {
      // Response hit context window limit before max_tokens
      echo 'Response reached model\'s context window limit', PHP_EOL;
      // The response is still valid but was limited by context window
  }
  ```

  ```ruby Ruby
  # Request with maximum tokens to get as much as possible
  response = client.beta.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 20000,
    messages: [{ role: "user", content: "Large input that uses most of context window..." }]
  )

  if response.stop_reason == :model_context_window_exceeded
    # Response hit context window limit before max_tokens
    puts "Response reached model's context window limit"
    # The response is still valid but was limited by context window
  end
  ```
</CodeGroup>

## Best practices for handling stop reasons

### Always check stop\_reason

Make it a habit to check the `stop_reason` in your response handling logic:

<CodeGroup>
  ```python Python
  def handle_response(response):
      if response.stop_reason == "tool_use":
          return handle_tool_use(response)
      elif response.stop_reason == "max_tokens":
          return handle_truncation(response)
      elif response.stop_reason == "model_context_window_exceeded":
          return handle_context_limit(response)
      elif response.stop_reason == "pause_turn":
          return handle_pause(response)
      elif response.stop_reason == "refusal":
          return handle_refusal(response)
      else:
          # Handle end_turn and other cases
          return response.content[0].text
  ```

  ```typescript TypeScript
  function handleResponse(response: Anthropic.Beta.BetaMessage): string {
    switch (response.stop_reason) {
      case "tool_use":
        return handleToolUse(response);
      case "max_tokens":
        return handleTruncation(response);
      case "model_context_window_exceeded":
        return handleContextLimit(response);
      case "pause_turn":
        return handlePause(response);
      case "refusal":
        return handleRefusal(response);
      default: {
        // Handle end_turn and other cases
        const block = response.content[0];
        return block.type === "text" ? block.text : "";
      }
    }
  }
  ```

  ```csharp C#
  static string HandleResponse(BetaMessage response)
  {
      return response.StopReason?.Value() switch
      {
          BetaStopReason.ToolUse => HandleToolUse(response),
          BetaStopReason.MaxTokens => HandleTruncation(response),
          BetaStopReason.ModelContextWindowExceeded => HandleContextLimit(response),
          BetaStopReason.PauseTurn => HandlePause(response),
          BetaStopReason.Refusal => HandleRefusal(response),
          // Handle end_turn and other cases
          _ => response.Content[0].TryPickText(out var textBlock) ? textBlock.Text : "",
      };
  }
  ```

  ```go Go
  func handleResponse(response *anthropic.BetaMessage) string {
  	switch response.StopReason {
  	case anthropic.BetaStopReasonToolUse:
  		return handleToolUse(response)
  	case anthropic.BetaStopReasonMaxTokens:
  		return handleTruncation(response)
  	case anthropic.BetaStopReasonModelContextWindowExceeded:
  		return handleContextLimit(response)
  	case anthropic.BetaStopReasonPauseTurn:
  		return handlePause(response)
  	case anthropic.BetaStopReasonRefusal:
  		return handleRefusal(response)
  	default:
  		// Handle end_turn and other cases
  		if block, ok := response.Content[0].AsAny().(anthropic.BetaTextBlock); ok {
  			return block.Text
  		}
  		return ""
  	}
  }
  ```

  ```java Java
  static String handleResponse(BetaMessage response) {
      BetaStopReason reason = response.stopReason().orElse(BetaStopReason.END_TURN);
      if (reason.equals(BetaStopReason.TOOL_USE)) {
          return handleToolUse(response);
      } else if (reason.equals(BetaStopReason.MAX_TOKENS)) {
          return handleTruncation(response);
      } else if (reason.equals(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED)) {
          return handleContextLimit(response);
      } else if (reason.equals(BetaStopReason.PAUSE_TURN)) {
          return handlePause(response);
      } else if (reason.equals(BetaStopReason.REFUSAL)) {
          return handleRefusal(response);
      }
      // Handle end_turn and other cases
      return response.content().get(0).text().map(BetaTextBlock::text).orElse("");
  }
  ```

  ```php PHP
  function handle_response($response): string
  {
      return match ($response->stopReason) {
          'tool_use' => handle_tool_use($response),
          'max_tokens' => handle_truncation($response),
          'model_context_window_exceeded' => handle_context_limit($response),
          'pause_turn' => handle_pause($response),
          'refusal' => handle_refusal($response),
          // Handle end_turn and other cases
          default => $response->content[0]->text,
      };
  }
  ```

  ```ruby Ruby
  def handle_response(response)
    case response.stop_reason
    when :tool_use then handle_tool_use(response)
    when :max_tokens then handle_truncation(response)
    when :model_context_window_exceeded then handle_context_limit(response)
    when :pause_turn then handle_pause(response)
    when :refusal then handle_refusal(response)
    else
      # Handle end_turn and other cases
      response.content.first.text
    end
  end
  ```
</CodeGroup>

### Handle truncated responses gracefully

When a response is truncated because of token limits or the context window, append a notice so the reader knows the output is incomplete. To continue generating from where the response left off instead, see [Ensuring complete responses](#ensuring-complete-responses).

<CodeGroup>
  ```python Python
  def handle_truncated_response(response):
      if response.stop_reason in ["max_tokens", "model_context_window_exceeded"]:
          if response.stop_reason == "max_tokens":
              note = "[Response truncated due to max_tokens limit]"
          else:
              note = "[Response truncated due to context window limit]"
          return f"{response.content[0].text}\n\n{note}"
      return response.content[0].text
  ```

  ```typescript TypeScript
  function handleTruncatedResponse(response: Anthropic.Beta.BetaMessage): string {
    const text = response.content[0].type === "text" ? response.content[0].text : "";

    if (
      response.stop_reason === "max_tokens" ||
      response.stop_reason === "model_context_window_exceeded"
    ) {
      const note =
        response.stop_reason === "max_tokens"
          ? "[Response truncated due to max_tokens limit]"
          : "[Response truncated due to context window limit]";
      return `${text}\n\n${note}`;
    }
    return text;
  }
  ```

  ```csharp C#
  static string HandleTruncatedResponse(BetaMessage response)
  {
      var text = response.Content[0].TryPickText(out var textBlock) ? textBlock.Text : "";
      var reason = response.StopReason?.Value();

      if (reason is BetaStopReason.MaxTokens or BetaStopReason.ModelContextWindowExceeded)
      {
          var note = reason == BetaStopReason.MaxTokens
              ? "[Response truncated due to max_tokens limit]"
              : "[Response truncated due to context window limit]";
          return $"{text}\n\n{note}";
      }
      return text;
  }
  ```

  ```go Go
  func handleTruncatedResponse(response *anthropic.BetaMessage) string {
  	text := ""
  	if block, ok := response.Content[0].AsAny().(anthropic.BetaTextBlock); ok {
  		text = block.Text
  	}

  	if response.StopReason == anthropic.BetaStopReasonMaxTokens ||
  		response.StopReason == anthropic.BetaStopReasonModelContextWindowExceeded {
  		note := "[Response truncated due to context window limit]"
  		if response.StopReason == anthropic.BetaStopReasonMaxTokens {
  			note = "[Response truncated due to max_tokens limit]"
  		}
  		return text + "\n\n" + note
  	}
  	return text
  }
  ```

  ```java Java
  static String handleTruncatedResponse(BetaMessage response) {
      String text = response.content().get(0).text().map(BetaTextBlock::text).orElse("");
      BetaStopReason reason = response.stopReason().orElse(BetaStopReason.END_TURN);

      if (reason.equals(BetaStopReason.MAX_TOKENS)
              || reason.equals(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED)) {
          String note = reason.equals(BetaStopReason.MAX_TOKENS)
              ? "[Response truncated due to max_tokens limit]"
              : "[Response truncated due to context window limit]";
          return text + "\n\n" + note;
      }
      return text;
  }
  ```

  ```php PHP
  function handle_truncated_response($response): string
  {
      $text = $response->content[0]->text;

      if (in_array($response->stopReason, ['max_tokens', 'model_context_window_exceeded'], true)) {
          $note = $response->stopReason === 'max_tokens'
              ? '[Response truncated due to max_tokens limit]'
              : '[Response truncated due to context window limit]';
          return "{$text}\n\n{$note}";
      }
      return $text;
  }
  ```

  ```ruby Ruby
  def handle_truncated_response(response)
    text = response.content.first.text

    if [:max_tokens, :model_context_window_exceeded].include?(response.stop_reason)
      note = if response.stop_reason == :max_tokens
        "[Response truncated due to max_tokens limit]"
      else
        "[Response truncated due to context window limit]"
      end
      return "#{text}\n\n#{note}"
    end
    text
  end
  ```
</CodeGroup>

### Implement retry logic for pause\_turn

When using [server tools](/docs/en/agents-and-tools/tool-use/server-tools), the API may return `pause_turn` if the server-side sampling loop reaches its iteration limit (default 10). Handle this by continuing the conversation:

<CodeGroup>
  ```python Python
  def handle_server_tool_conversation(client, user_query, tools, max_continuations=5):
      """
      Handle server tool conversations that may require multiple continuations.

      The server runs a sampling loop when executing server tools. If the loop
      reaches its iteration limit, the API returns pause_turn. Continue the
      conversation by sending the response back to let Claude finish.
      """
      messages = [{"role": "user", "content": user_query}]

      for _ in range(max_continuations):
          response = client.messages.create(
              model="claude-opus-4-8", max_tokens=4096, messages=messages, tools=tools
          )

          if response.stop_reason != "pause_turn":
              # Claude finished processing - return the final response
              return response

          # pause_turn: replace the full message list to maintain alternating roles
          messages = [
              {"role": "user", "content": user_query},
              {"role": "assistant", "content": response.content},
          ]

      # Reached max continuations - return the last response
      return response
  ```

  ```typescript TypeScript
  async function handleServerToolConversation(
    client: Anthropic,
    userQuery: string,
    tools: Anthropic.ToolUnion[],
    maxContinuations = 5
  ): Promise<Anthropic.Message> {
    let messages: Anthropic.MessageParam[] = [{ role: "user", content: userQuery }];
    let response: Anthropic.Message;

    for (let i = 0; i < maxContinuations; i++) {
      response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 4096,
        messages,
        tools
      });

      if (response.stop_reason !== "pause_turn") {
        // Claude finished processing - return the final response
        return response;
      }

      // pause_turn: replace the full message list to maintain alternating roles
      messages = [
        { role: "user", content: userQuery },
        { role: "assistant", content: response.content }
      ];
    }

    // Reached max continuations - return the last response
    return response!;
  }
  ```

  ```csharp C#
  static async Task<Message> HandleServerToolConversation(
      AnthropicClient client,
      string userQuery,
      List<ToolUnion> tools,
      int maxContinuations = 5)
  {
      List<MessageParam> messages = [new() { Role = Role.User, Content = userQuery }];
      Message response = null!;

      for (var i = 0; i < maxContinuations; i++)
      {
          response = await client.Messages.Create(new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 4096,
              Messages = messages,
              Tools = tools
          });

          if (response.StopReason != "pause_turn")
          {
              // Claude finished processing - return the final response
              return response;
          }

          // pause_turn: replace the full message list to maintain alternating roles
          messages =
          [
              new() { Role = Role.User, Content = userQuery },
              new()
              {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              }
          ];
      }

      // Reached max continuations - return the last response
      return response;
  }
  ```

  ```go Go
  func handleServerToolConversation(
  	client anthropic.Client,
  	userQuery string,
  	tools []anthropic.ToolUnionParam,
  	maxContinuations int,
  ) (*anthropic.Message, error) {
  	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(userQuery))}
  	var response *anthropic.Message
  	var err error

  	for range maxContinuations {
  		response, err = client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 4096,
  			Messages:  messages,
  			Tools:     tools,
  		})
  		if err != nil {
  			return nil, err
  		}

  		if response.StopReason != "pause_turn" {
  			// Claude finished processing - return the final response
  			return response, nil
  		}

  		// pause_turn: replace the full message list to maintain alternating roles
  		var contentParams []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			contentParams = append(contentParams, block.ToParam())
  		}
  		messages = []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(userQuery)),
  			anthropic.NewAssistantMessage(contentParams...),
  		}
  	}

  	// Reached max continuations - return the last response
  	return response, nil
  }
  ```

  ```java Java
  static Message handleServerToolConversation(
      AnthropicClient client,
      String userQuery,
      List<Tool> tools,
      int maxContinuations
  ) {
      Message response = null;

      for (int i = 0; i < maxContinuations; i++) {
          // Rebuild the params each iteration so messages aren't accumulated
          MessageCreateParams.Builder params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .addUserMessage(userQuery);
          tools.forEach(params::addTool);
          if (response != null) {
              params.addMessage(response);
          }

          response = client.messages().create(params.build());

          if (!response.stopReason().map(StopReason.PAUSE_TURN::equals).orElse(false)) {
              // Claude finished processing - return the final response
              return response;
          }
          // pause_turn: loop again and send the response back
      }

      // Reached max continuations - return the last response
      return response;
  }
  ```

  ```php PHP
  function handle_server_tool_conversation(
      Client $client,
      string $userQuery,
      array $tools,
      int $maxContinuations = 5
  ) {
      $messages = [['role' => 'user', 'content' => $userQuery]];
      $response = null;

      for ($i = 0; $i < $maxContinuations; $i++) {
          $response = $client->messages->create(
              maxTokens: 4096,
              messages: $messages,
              model: 'claude-opus-4-8',
              tools: $tools,
          );

          if ($response->stopReason !== 'pause_turn') {
              // Claude finished processing - return the final response
              return $response;
          }

          // pause_turn: replace the full message list to maintain alternating roles
          $messages = [
              ['role' => 'user', 'content' => $userQuery],
              ['role' => 'assistant', 'content' => $response->content],
          ];
      }

      // Reached max continuations - return the last response
      return $response;
  }
  ```

  ```ruby Ruby
  def handle_server_tool_conversation(client, user_query, tools, max_continuations: 5)
    messages = [{ role: "user", content: user_query }]
    response = nil

    max_continuations.times do
      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 4096,
        messages: messages,
        tools: tools
      )

      # Claude finished processing - return the final response
      return response unless response.stop_reason == :pause_turn

      # pause_turn: replace the full message list to maintain alternating roles
      messages = [
        { role: "user", content: user_query },
        { role: "assistant", content: response.content }
      ]
    end

    # Reached max continuations - return the last response
    response
  end
  ```
</CodeGroup>

## Stop reasons vs. errors

It's important to distinguish between `stop_reason` values and actual errors:

### Stop reasons (successful responses)

* Part of the response body
* Indicate why generation stopped normally
* Response contains valid content

### Errors (failed requests)

* HTTP status codes 4xx or 5xx
* Indicate request processing failures
* Response contains error details

<CodeGroup>
  ```bash cURL
  # cURL exits non-zero on HTTP errors with --fail-with-body; inspect
  # $? for errors and stop_reason for successful responses.
  curl --fail-with-body -sS https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [{"role": "user", "content": "Hello!"}]
    }' | jq '.stop_reason'
  ```

  ```bash CLI
  # The CLI exits non-zero on API errors; stop_reason appears on success.
  ant messages create \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello!"}' \
    --format json | jq '.stop_reason'
  ```

  ```python Python
  client = anthropic.Anthropic()

  try:
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=1024,
          messages=[{"role": "user", "content": "Hello!"}],
      )

      # Handle successful response with stop_reason
      if response.stop_reason == "max_tokens":
          print("Response was truncated")

  except anthropic.APIStatusError as e:
      # Handle actual errors
      if e.status_code == 429:
          print("Rate limit exceeded")
      elif e.status_code == 500:
          print("Server error")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  try {
    const response = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello!" }]
    });

    // Handle successful response with stop_reason
    if (response.stop_reason === "max_tokens") {
      console.log("Response was truncated");
    }
  } catch (err) {
    // Handle actual errors
    if (err instanceof Anthropic.APIError) {
      if (err.status === 429) {
        console.log("Rate limit exceeded");
      } else if (err.status === 500) {
        console.log("Server error");
      }
    } else {
      throw err;
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  try
  {
      var response = await client.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Hello!" }]
      });

      // Handle successful response with stop_reason
      if (response.StopReason == "max_tokens")
      {
          Console.WriteLine("Response was truncated");
      }
  }
  catch (AnthropicRateLimitException)
  {
      // Handle actual errors
      Console.WriteLine("Rate limit exceeded");
  }
  catch (Anthropic5xxException)
  {
      Console.WriteLine("Server error");
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })
  if err != nil {
  	// Handle actual errors
  	var apiErr *anthropic.Error
  	if errors.As(err, &apiErr) {
  		switch apiErr.StatusCode {
  		case 429:
  			fmt.Println("Rate limit exceeded")
  		case 500:
  			fmt.Println("Server error")
  		}
  	}
  	log.Fatal(err)
  }

  // Handle successful response with stop_reason
  if response.StopReason == "max_tokens" {
  	fmt.Println("Response was truncated")
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  try {
      Message response = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addUserMessage("Hello!")
              .build()
      );

      // Handle successful response with stop_reason
      if (response.stopReason().map(StopReason.MAX_TOKENS::equals).orElse(false)) {
          IO.println("Response was truncated");
      }
  } catch (RateLimitException e) {
      // Handle actual errors
      IO.println("Rate limit exceeded");
  } catch (AnthropicServiceException e) {
      if (e.statusCode() == 500) {
          IO.println("Server error");
      }
  }
  ```

  ```php PHP
  $client = new Client();

  try {
      $response = $client->messages->create(
          maxTokens: 1024,
          messages: [['role' => 'user', 'content' => 'Hello!']],
          model: 'claude-opus-4-8',
      );

      // Handle successful response with stop_reason
      if ($response->stopReason === 'max_tokens') {
          echo 'Response was truncated', PHP_EOL;
      }
  } catch (RateLimitException $e) {
      // Handle actual errors
      echo 'Rate limit exceeded', PHP_EOL;
  } catch (InternalServerException $e) {
      echo 'Server error', PHP_EOL;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  begin
    response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello!" }]
    )

    # Handle successful response with stop_reason
    if response.stop_reason == :max_tokens
      puts "Response was truncated"
    end
  rescue Anthropic::Errors::RateLimitError
    # Handle actual errors
    puts "Rate limit exceeded"
  rescue Anthropic::Errors::APIStatusError => e
    puts "Server error" if e.status == 500
  end
  ```
</CodeGroup>

## Streaming considerations

When using streaming, `stop_reason` is:

* `null` in the initial `message_start` event
* Provided in the `message_delta` event
* Not provided in any other events

<CodeGroup>
  ```bash cURL
  # The message_delta event in the SSE stream carries stop_reason.
  curl --no-buffer https://api.anthropic.com/v1/messages \
    --header "x-api-key: $ANTHROPIC_API_KEY" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --data '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "stream": true,
      "messages": [{"role": "user", "content": "Hello!"}]
    }'
  ```

  ```bash CLI
  # stop_reason appears in the message_delta event.
  ant messages create --stream --format jsonl \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello!"}' |
    jq -c 'select(.type == "message_delta") | .delta.stop_reason'
  ```

  ```python Python
  client = anthropic.Anthropic()

  with client.messages.stream(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  ) as stream:
      for event in stream:
          if event.type == "message_delta":
              stop_reason = event.delta.stop_reason
              if stop_reason:
                  print(f"Stream ended with: {stop_reason}")
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });

  for await (const event of stream) {
    if (event.type === "message_delta" && event.delta.stop_reason) {
      console.log(`Stream ended with: ${event.delta.stop_reason}`);
    }
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  };

  await foreach (var streamEvent in client.Messages.CreateStreaming(parameters))
  {
      switch (streamEvent.Value)
      {
          case RawMessageDeltaEvent deltaEvent when deltaEvent.Delta.StopReason is not null:
              Console.WriteLine($"Stream ended with: {deltaEvent.Delta.StopReason}");
              break;
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  stream := client.Messages.NewStreaming(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })

  // Accumulate events into the final Message, which carries stop_reason.
  message := anthropic.Message{}
  for stream.Next() {
  	if err := message.Accumulate(stream.Current()); err != nil {
  		log.Fatal(err)
  	}
  }
  if err := stream.Err(); err != nil {
  	log.Fatal(err)
  }

  if message.StopReason != "" {
  	fmt.Printf("Stream ended with: %s\n", message.StopReason)
  }
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addUserMessage("Hello!")
      .build();

  // Accumulate events into the final Message, which carries stop_reason.
  MessageAccumulator accumulator = MessageAccumulator.create();
  try (StreamResponse<RawMessageStreamEvent> streamResponse =
          client.messages().createStreaming(params)) {
      streamResponse.stream().forEach(accumulator::accumulate);
  }

  accumulator.message().stopReason().ifPresent(stopReason ->
      IO.println("Stream ended with: " + stopReason)
  );
  ```

  ```php PHP
  $client = new Client();

  $stream = $client->messages->createStream(
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello!']],
      model: 'claude-opus-4-8',
  );

  foreach ($stream as $event) {
      if ($event instanceof RawMessageDeltaEvent && $event->delta->stopReason !== null) {
          echo "Stream ended with: {$event->delta->stopReason}", PHP_EOL;
      }
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  stream = client.messages.stream(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  )

  stream.each do |event|
    next unless event.type == :message_delta
    stop_reason = event.delta.stop_reason
    puts "Stream ended with: #{stop_reason}" if stop_reason
  end
  ```
</CodeGroup>

## Common patterns

### Handling tool use workflows

<Tip>
  **Simpler with tool runner:** The following example shows manual tool handling. For most use cases, the [tool runner](/docs/en/agents-and-tools/tool-use/tool-runner) automatically handles tool execution with much less code.
</Tip>

<CodeGroup>
  ```python Python
  def complete_tool_workflow(client, user_query, tools):
      messages = [{"role": "user", "content": user_query}]

      while True:
          response = client.messages.create(
              model="claude-opus-4-8", max_tokens=1024, messages=messages, tools=tools
          )

          if response.stop_reason == "tool_use":
              # Execute tools and continue
              tool_results = execute_tools(response.content)
              messages.append({"role": "assistant", "content": response.content})
              messages.append({"role": "user", "content": tool_results})
          else:
              # Final response
              return response
  ```

  ```typescript TypeScript
  async function completeToolWorkflow(
    client: Anthropic,
    userQuery: string,
    tools: Anthropic.ToolUnion[]
  ): Promise<Anthropic.Message> {
    const messages: Anthropic.MessageParam[] = [{ role: "user", content: userQuery }];

    while (true) {
      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages,
        tools
      });

      if (response.stop_reason === "tool_use") {
        // Execute tools and continue
        const toolResults = executeTools(response.content);
        messages.push({ role: "assistant", content: response.content });
        messages.push({ role: "user", content: toolResults });
      } else {
        // Final response
        return response;
      }
    }
  }
  ```

  ```csharp C#
  static async Task<Message> CompleteToolWorkflow(
      AnthropicClient client,
      string userQuery,
      List<ToolUnion> tools)
  {
      List<MessageParam> messages = [new() { Role = Role.User, Content = userQuery }];

      while (true)
      {
          var response = await client.Messages.Create(new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages = messages,
              Tools = tools
          });

          if (response.StopReason == "tool_use")
          {
              // Execute tools and continue
              var toolResults = ExecuteTools(response.Content);
              messages.Add(new()
              {
                  Role = Role.Assistant,
                  Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList()
              });
              messages.Add(new() { Role = Role.User, Content = toolResults });
          }
          else
          {
              // Final response
              return response;
          }
      }
  }
  ```

  ```go Go
  func completeToolWorkflow(
  	client anthropic.Client,
  	userQuery string,
  	tools []anthropic.ToolUnionParam,
  ) (*anthropic.Message, error) {
  	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(userQuery))}

  	for {
  		response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 1024,
  			Messages:  messages,
  			Tools:     tools,
  		})
  		if err != nil {
  			return nil, err
  		}

  		if response.StopReason != "tool_use" {
  			// Final response
  			return response, nil
  		}

  		// Execute tools and continue
  		toolResults := executeTools(response.Content)
  		var contentParams []anthropic.ContentBlockParamUnion
  		for _, block := range response.Content {
  			contentParams = append(contentParams, block.ToParam())
  		}
  		messages = append(messages, anthropic.NewAssistantMessage(contentParams...))
  		messages = append(messages, anthropic.NewUserMessage(toolResults...))
  	}
  }
  ```

  ```java Java
  static Message completeToolWorkflow(
      AnthropicClient client,
      String userQuery,
      List<Tool> tools
  ) {
      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder().role(MessageParam.Role.USER).content(userQuery).build());

      while (true) {
          MessageCreateParams.Builder params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .messages(messages);
          tools.forEach(params::addTool);

          Message response = client.messages().create(params.build());

          if (!response.stopReason().map(StopReason.TOOL_USE::equals).orElse(false)) {
              // Final response
              return response;
          }

          // Execute tools and continue
          List<ToolResultBlockParam> toolResults = executeTools(response.content());
          messages.add(response.toParam());
          messages.add(MessageParam.builder()
              .role(MessageParam.Role.USER)
              .contentOfBlockParams(toolResults.stream().map(ContentBlockParam::ofToolResult).toList())
              .build());
      }
  }
  ```

  ```php PHP
  function complete_tool_workflow(Client $client, string $userQuery, array $tools)
  {
      $messages = [['role' => 'user', 'content' => $userQuery]];

      while (true) {
          $response = $client->messages->create(
              maxTokens: 1024,
              messages: $messages,
              model: 'claude-opus-4-8',
              tools: $tools,
          );

          if ($response->stopReason !== 'tool_use') {
              // Final response
              return $response;
          }

          // Execute tools and continue
          $toolResults = execute_tools($response->content);
          $messages[] = ['role' => 'assistant', 'content' => $response->content];
          $messages[] = ['role' => 'user', 'content' => $toolResults];
      }
  }
  ```

  ```ruby Ruby
  def complete_tool_workflow(client, user_query, tools)
    messages = [{ role: "user", content: user_query }]

    loop do
      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: messages,
        tools: tools
      )

      # Final response
      return response unless response.stop_reason == :tool_use

      # Execute tools and continue
      tool_results = execute_tools(response.content)
      messages << { role: "assistant", content: response.content }
      messages << { role: "user", content: tool_results }
    end
  end
  ```
</CodeGroup>

### Ensuring complete responses

<CodeGroup>
  ```python Python
  def get_complete_response(client, prompt, max_attempts=3):
      messages = [{"role": "user", "content": prompt}]
      full_response = ""

      for _ in range(max_attempts):
          response = client.messages.create(
              model="claude-opus-4-8", messages=messages, max_tokens=4096
          )

          full_response += response.content[0].text

          if response.stop_reason != "max_tokens":
              break

          # Continue from where it left off
          messages = [
              {"role": "user", "content": prompt},
              {"role": "assistant", "content": full_response},
              {"role": "user", "content": "Please continue from where you left off."},
          ]

      return full_response
  ```

  ```typescript TypeScript
  async function getCompleteResponse(
    client: Anthropic,
    prompt: string,
    maxAttempts = 3
  ): Promise<string> {
    let messages: Anthropic.MessageParam[] = [{ role: "user", content: prompt }];
    let fullResponse = "";

    for (let i = 0; i < maxAttempts; i++) {
      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 4096,
        messages
      });

      const block = response.content[0];
      fullResponse += block.type === "text" ? block.text : "";

      if (response.stop_reason !== "max_tokens") {
        break;
      }

      // Continue from where it left off
      messages = [
        { role: "user", content: prompt },
        { role: "assistant", content: fullResponse },
        { role: "user", content: "Please continue from where you left off." }
      ];
    }

    return fullResponse;
  }
  ```

  ```csharp C#
  static async Task<string> GetCompleteResponse(AnthropicClient client, string prompt, int maxAttempts = 3)
  {
      List<MessageParam> messages = [new() { Role = Role.User, Content = prompt }];
      var fullResponse = "";

      for (var i = 0; i < maxAttempts; i++)
      {
          var response = await client.Messages.Create(new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 4096,
              Messages = messages
          });

          if (response.Content[0].TryPickText(out var textBlock))
          {
              fullResponse += textBlock.Text;
          }

          if (response.StopReason != "max_tokens")
          {
              break;
          }

          // Continue from where it left off
          messages =
          [
              new() { Role = Role.User, Content = prompt },
              new() { Role = Role.Assistant, Content = fullResponse },
              new() { Role = Role.User, Content = "Please continue from where you left off." }
          ];
      }

      return fullResponse;
  }
  ```

  ```go Go
  func getCompleteResponse(client anthropic.Client, prompt string, maxAttempts int) (string, error) {
  	messages := []anthropic.MessageParam{anthropic.NewUserMessage(anthropic.NewTextBlock(prompt))}
  	fullResponse := ""

  	for range maxAttempts {
  		response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus4_8,
  			MaxTokens: 4096,
  			Messages:  messages,
  		})
  		if err != nil {
  			return "", err
  		}

  		if block, ok := response.Content[0].AsAny().(anthropic.TextBlock); ok {
  			fullResponse += block.Text
  		}

  		if response.StopReason != "max_tokens" {
  			break
  		}

  		// Continue from where it left off
  		messages = []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(prompt)),
  			anthropic.NewAssistantMessage(anthropic.NewTextBlock(fullResponse)),
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Please continue from where you left off.")),
  		}
  	}

  	return fullResponse, nil
  }
  ```

  ```java Java
  static String getCompleteResponse(AnthropicClient client, String prompt, int maxAttempts) {
      List<MessageParam> messages = List.of(
          MessageParam.builder().role(MessageParam.Role.USER).content(prompt).build()
      );
      StringBuilder fullResponse = new StringBuilder();

      for (int i = 0; i < maxAttempts; i++) {
          Message response = client.messages().create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_8)
                  .maxTokens(4096L)
                  .messages(messages)
                  .build()
          );

          response.content().get(0).text().ifPresent(block -> fullResponse.append(block.text()));

          if (!response.stopReason().map(StopReason.MAX_TOKENS::equals).orElse(false)) {
              break;
          }

          // Continue from where it left off
          messages = List.of(
              MessageParam.builder().role(MessageParam.Role.USER).content(prompt).build(),
              MessageParam.builder().role(MessageParam.Role.ASSISTANT).content(fullResponse.toString()).build(),
              MessageParam.builder().role(MessageParam.Role.USER).content("Please continue from where you left off.").build()
          );
      }

      return fullResponse.toString();
  }
  ```

  ```php PHP
  function get_complete_response(Client $client, string $prompt, int $maxAttempts = 3): string
  {
      $messages = [['role' => 'user', 'content' => $prompt]];
      $fullResponse = '';

      for ($i = 0; $i < $maxAttempts; $i++) {
          $response = $client->messages->create(
              maxTokens: 4096,
              messages: $messages,
              model: 'claude-opus-4-8',
          );

          $fullResponse .= $response->content[0]->text;

          if ($response->stopReason !== 'max_tokens') {
              break;
          }

          // Continue from where it left off
          $messages = [
              ['role' => 'user', 'content' => $prompt],
              ['role' => 'assistant', 'content' => $fullResponse],
              ['role' => 'user', 'content' => 'Please continue from where you left off.'],
          ];
      }

      return $fullResponse;
  }
  ```

  ```ruby Ruby
  def get_complete_response(client, prompt, max_attempts: 3)
    messages = [{ role: "user", content: prompt }]
    full_response = +""

    max_attempts.times do
      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 4096,
        messages: messages
      )

      full_response << response.content.first.text

      break unless response.stop_reason == :max_tokens

      # Continue from where it left off
      messages = [
        { role: "user", content: prompt },
        { role: "assistant", content: full_response },
        { role: "user", content: "Please continue from where you left off." }
      ]
    end

    full_response
  end
  ```
</CodeGroup>

### Getting maximum tokens without knowing input size

With the `model_context_window_exceeded` stop reason, you can request the maximum possible tokens without calculating input size:

<CodeGroup>
  ```python Python
  def get_max_possible_tokens(client, prompt):
      """
      Get as many tokens as possible within the model's context window
      without needing to calculate input token count
      """
      response = client.beta.messages.create(
          model="claude-opus-4-8",
          messages=[{"role": "user", "content": prompt}],
          max_tokens=20000,  # Python SDK requires streaming for max_tokens above ~21k
      )

      if response.stop_reason == "model_context_window_exceeded":
          # Got the maximum possible tokens given input size
          print(
              f"Generated {response.usage.output_tokens} tokens (context limit reached)"
          )
      elif response.stop_reason == "max_tokens":
          # Got exactly the requested tokens
          print(f"Generated {response.usage.output_tokens} tokens (max_tokens reached)")
      else:
          # Natural completion
          print(f"Generated {response.usage.output_tokens} tokens (natural completion)")

      return response.content[0].text
  ```

  ```typescript TypeScript
  async function getMaxPossibleTokens(client: Anthropic, prompt: string): Promise<string> {
    const response = await client.beta.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 20000,
      messages: [{ role: "user", content: prompt }]
    });

    const tokens = response.usage.output_tokens;
    if (response.stop_reason === "model_context_window_exceeded") {
      // Got the maximum possible tokens given input size
      console.log(`Generated ${tokens} tokens (context limit reached)`);
    } else if (response.stop_reason === "max_tokens") {
      // Got exactly the requested tokens
      console.log(`Generated ${tokens} tokens (max_tokens reached)`);
    } else {
      // Natural completion
      console.log(`Generated ${tokens} tokens (natural completion)`);
    }

    const block = response.content[0];
    return block.type === "text" ? block.text : "";
  }
  ```

  ```csharp C#
  using Anthropic.Models.Beta.Messages;
  using Model = Anthropic.Models.Messages.Model;

  static async Task<string> GetMaxPossibleTokens(AnthropicClient client, string prompt)
  {
      var response = await client.Beta.Messages.Create(new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 20000,
          Messages = [new() { Role = Role.User, Content = prompt }]
      });

      var tokens = response.Usage.OutputTokens;
      var reason = response.StopReason?.Value();
      if (reason == BetaStopReason.ModelContextWindowExceeded)
      {
          // Got the maximum possible tokens given input size
          Console.WriteLine($"Generated {tokens} tokens (context limit reached)");
      }
      else if (reason == BetaStopReason.MaxTokens)
      {
          // Got exactly the requested tokens
          Console.WriteLine($"Generated {tokens} tokens (max_tokens reached)");
      }
      else
      {
          // Natural completion
          Console.WriteLine($"Generated {tokens} tokens (natural completion)");
      }

      return response.Content[0].TryPickText(out var textBlock) ? textBlock.Text : "";
  }
  ```

  ```go Go
  func getMaxPossibleTokens(client anthropic.Client, prompt string) (string, error) {
  	response, err := client.Beta.Messages.New(context.TODO(), anthropic.BetaMessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 20000,
  		Messages: []anthropic.BetaMessageParam{
  			anthropic.NewBetaUserMessage(anthropic.NewBetaTextBlock(prompt)),
  		},
  	})
  	if err != nil {
  		return "", err
  	}

  	tokens := response.Usage.OutputTokens
  	switch response.StopReason {
  	case anthropic.BetaStopReasonModelContextWindowExceeded:
  		// Got the maximum possible tokens given input size
  		fmt.Printf("Generated %d tokens (context limit reached)\n", tokens)
  	case anthropic.BetaStopReasonMaxTokens:
  		// Got exactly the requested tokens
  		fmt.Printf("Generated %d tokens (max_tokens reached)\n", tokens)
  	default:
  		// Natural completion
  		fmt.Printf("Generated %d tokens (natural completion)\n", tokens)
  	}

  	if block, ok := response.Content[0].AsAny().(anthropic.BetaTextBlock); ok {
  		return block.Text, nil
  	}
  	return "", nil
  }
  ```

  ```java Java
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaStopReason;
  import com.anthropic.models.beta.messages.BetaTextBlock;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  static String getMaxPossibleTokens(AnthropicClient client, String prompt) {
      BetaMessage response = client.beta().messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(20000L)
              .addUserMessage(prompt)
              .build()
      );

      long tokens = response.usage().outputTokens();
      BetaStopReason reason = response.stopReason().orElse(BetaStopReason.END_TURN);
      if (reason.equals(BetaStopReason.MODEL_CONTEXT_WINDOW_EXCEEDED)) {
          // Got the maximum possible tokens given input size
          IO.println("Generated " + tokens + " tokens (context limit reached)");
      } else if (reason.equals(BetaStopReason.MAX_TOKENS)) {
          // Got exactly the requested tokens
          IO.println("Generated " + tokens + " tokens (max_tokens reached)");
      } else {
          // Natural completion
          IO.println("Generated " + tokens + " tokens (natural completion)");
      }

      return response.content().get(0).text().map(BetaTextBlock::text).orElse("");
  }
  ```

  ```php PHP
  function get_max_possible_tokens(Client $client, string $prompt): string
  {
      $response = $client->beta->messages->create(
          maxTokens: 20000,
          messages: [['role' => 'user', 'content' => $prompt]],
          model: 'claude-opus-4-8',
      );

      $tokens = $response->usage->outputTokens;
      echo match ($response->stopReason) {
          // Got the maximum possible tokens given input size
          'model_context_window_exceeded' => "Generated {$tokens} tokens (context limit reached)",
          // Got exactly the requested tokens
          'max_tokens' => "Generated {$tokens} tokens (max_tokens reached)",
          // Natural completion
          default => "Generated {$tokens} tokens (natural completion)",
      }, PHP_EOL;

      return $response->content[0]->text;
  }
  ```

  ```ruby Ruby
  def get_max_possible_tokens(client, prompt)
    response = client.beta.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 20000,
      messages: [{ role: "user", content: prompt }]
    )

    tokens = response.usage.output_tokens
    case response.stop_reason
    when :model_context_window_exceeded
      # Got the maximum possible tokens given input size
      puts "Generated #{tokens} tokens (context limit reached)"
    when :max_tokens
      # Got exactly the requested tokens
      puts "Generated #{tokens} tokens (max_tokens reached)"
    else
      # Natural completion
      puts "Generated #{tokens} tokens (natural completion)"
    end

    response.content.first.text
  end
  ```
</CodeGroup>

## Next steps

<CardGroup cols={2}>
  <Card title="Refusals and fallback" icon="arrows-clockwise" href="/docs/en/build-with-claude/refusals-and-fallback">
    Retry refused requests on a fallback model, server-side or in your client.
  </Card>

  <Card title="Tool Runner (SDK)" icon="wrench" href="/docs/en/agents-and-tools/tool-use/tool-runner">
    Let the SDK manage the `tool_use` loop, result formatting, and retries for you.
  </Card>

  <Card title="Streaming messages" icon="lightning" href="/docs/en/build-with-claude/streaming">
    Read `stop_reason` from the `message_delta` event when streaming.
  </Card>

  <Card title="Errors" icon="info" href="/docs/en/api/errors">
    Handle 4xx and 5xx HTTP errors, which are distinct from stop reasons.
  </Card>
</CardGroup>
