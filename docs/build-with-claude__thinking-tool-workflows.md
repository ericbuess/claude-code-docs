---
title: Thinking in tool and multi-turn workflows
url: https://platform.claude.com/docs/en/build-with-claude/thinking-tool-workflows
description: Walk through a complete two-turn tool-use round trip that preserves thinking blocks correctly, and see how interleaved thinking changes the flow.
---

<Note>
  For how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

This page walks through a complete two-turn tool-use round trip with thinking enabled: Claude thinks, requests a tool call, receives the result, and finishes its answer, with the thinking blocks handled correctly at every step. The full rules live on the [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking) page, in [Thinking with tool use](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use) and [Preserving thinking blocks](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks); this page shows those rules applied in runnable code.

## The rules this walkthrough applies

Each link leads to the full statement on the Thinking page:

* [Limit tool choice to `auto` or `none` in manual mode](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use): `tool_choice` options that force tool use return an error with manual extended thinking (`thinking: {type: "enabled"}`); adaptive thinking supports forced tool use.
* [Keep one thinking configuration per assistant turn](https://platform.claude.com/docs/en/build-with-claude/thinking#thinking-with-tool-use): a tool-use loop is one assistant turn, so change the configuration only between turns.
* [Pass thinking blocks back complete and unmodified](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks): when you return a tool result, the thinking blocks from the assistant message must come back with it.
* [Echo the assistant message exactly as received](https://platform.claude.com/docs/en/build-with-claude/thinking#preserving-thinking-blocks): rebuilding the message or filtering out `redacted_thinking` blocks triggers a 400 error.

The samples use adaptive thinking; on models that support only extended thinking, substitute `thinking: {type: "enabled", budget_tokens: N}`. The round-trip rules are identical.

## Walk through a two-turn tool-use round trip

The example defines a `get_weather` tool, lets Claude think and request a tool call, then returns the tool result along with the assistant turn echoed exactly as received, thinking block included.

<Steps>
  <Step title="Make the first request with a tool available">
    Send a request with adaptive thinking enabled and the tool defined. Apart from the `thinking` parameter, this is a standard [tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) request:

    <CodeGroup>
      ```bash CLI
      ant messages create --transform content <<'YAML'
      model: claude-opus-4-8
      max_tokens: 16000
      thinking:
        type: adaptive
      tools:
        - name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required:
              - location
      messages:
        - role: user
          content: "What's the weather in Paris?"
      YAML
      ```

      ```python Python

      client = anthropic.Anthropic()

      weather_tool = {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
              "type": "object",
              "properties": {"location": {"type": "string", "description": "City name"}},
              "required": ["location"],
          },
      }

      # First request - Claude responds with thinking and tool request
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          tools=[weather_tool],
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
      )
      print(response)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const weatherTool: Anthropic.Tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      };

      // First request - Claude responds with thinking and tool request
      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weatherTool],
        messages: [{ role: "user", content: "What's the weather in Paris?" }]
      });
      console.log(response);
      ```

      ```csharp C#
      AnthropicClient client = new();

      var weatherTool = new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get current weather for a location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
              },
              Required = ["location"],
          },
      });

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Tools = [weatherTool],
          Messages = [new() { Role = Role.User, Content = "What's the weather in Paris?" }]
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      weatherTool := anthropic.ToolUnionParam{
      	OfTool: &anthropic.ToolParam{
      		Name:        "get_weather",
      		Description: anthropic.String("Get current weather for a location"),
      		InputSchema: anthropic.ToolInputSchemaParam{
      			Properties: map[string]any{
      				"location": map[string]any{
      					"type":        "string",
      					"description": "City name",
      				},
      			},
      			Required: []string{"location"},
      		},
      	},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Tools: []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      fmt.Println(response)
      ```

      ```java Java
      import com.anthropic.models.messages.ThinkingConfigAdaptive;
      // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addTool(Tool.builder()
                  .name("get_weather")
                  .description("Get current weather for a location")
                  .inputSchema(Tool.InputSchema.builder()
                      .properties(JsonValue.from(Map.of(
                          "location", Map.of("type", "string", "description", "City name")
                      )))
                      .required(List.of("location"))
                      .build())
                  .build())
              .addUserMessage("What's the weather in Paris?")
              .build();

          Message response = client.messages().create(params);
          IO.println(response);
      ```

      ```php PHP
      $client = new Client();

      $weatherTool = [
          'name' => 'get_weather',
          'description' => 'Get current weather for a location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => ['type' => 'string', 'description' => 'City name']
              ],
              'required' => ['location']
          ]
      ];

      $message = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          tools: [$weatherTool],
      );
      echo $message;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      weather_tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" }
        ]
      )
      puts message
      ```
    </CodeGroup>
  </Step>

  <Step title="Capture the content array to echo back">
    You should see `thinking`, `text`, and `tool_use` blocks in the response content on a run where Claude chose to think (on simpler requests, adaptive mode may skip the thinking block). Keep this content array intact: the next step sends it back verbatim.

    <Note>
      To see thinking text like this output, add `display: "summarized"` to the request. On models where display defaults to omitted, including claude-opus-4-8, the `thinking` field otherwise comes back as an empty string with only the `signature` populated. Either way, echo the content array back unchanged; see [Controlling thinking display](https://platform.claude.com/docs/en/build-with-claude/thinking#controlling-thinking-display).
    </Note>

    ```json Output
    {
      "content": [
        {
          "type": "thinking",
          "thinking": "The user wants to know the current weather in Paris. I have access to a function `get_weather`...",
          "signature": "BDaL4VrbR2Oj0hO4XpJxT28J5T...."
        },
        {
          "type": "text",
          "text": "I can help you get the current weather information for Paris. Let me check that for you"
        },
        {
          "type": "tool_use",
          "id": "toolu_01CswdEQBMshySk6Y9DFKrfq",
          "name": "get_weather",
          "input": {
            "location": "Paris"
          }
        }
      ]
    }
    ```
  </Step>

  <Step title="Return the tool result, echoing the assistant turn verbatim">
    Run the tool on your side, then send a second request that appends two messages to the conversation. The first is the assistant content echoed back exactly as received, so the thinking block stays unchanged alongside the `tool_use` block. The second is a user message carrying the `tool_result`.

    Each sample is a self-contained script: it repeats the first request, then immediately sends the follow-up using the response it just received.

    <CodeGroup>
      ```bash CLI
      # First turn: write the assistant content array (thinking and tool_use
      # blocks, signatures intact) to a file. Routing model-generated text
      # through a file keeps it out of shell-expansion position later.
      ant messages create --transform content --format jsonl \
        > assistant_content.json <<'YAML'
      model: claude-opus-4-8
      max_tokens: 16000
      thinking:
        type: adaptive
      tools:
        - name: get_weather
          description: Get current weather for a location
          input_schema:
            type: object
            properties:
              location:
                type: string
                description: City name
            required: [location]
      messages:
        - role: user
          content: What's the weather in Paris?
      YAML

      # Second turn: jq fills the two null placeholders from the captured file,
      # so the blocks return verbatim as the assistant message. The thinking
      # block MUST accompany the tool_use block. The quoted delimiter keeps the
      # shell from expanding anything in the body.
      jq --slurpfile blocks assistant_content.json '
        .messages[1].content = $blocks[0] |
        .messages[2].content[0].tool_use_id =
          ($blocks[0][] | select(.type == "tool_use") | .id)
      ' <<'JSON' | ant messages create
      {
        "model": "claude-opus-4-8",
        "max_tokens": 16000,
        "thinking": {"type": "adaptive"},
        "tools": [{
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
            "type": "object",
            "properties": {
              "location": {"type": "string", "description": "City name"}
            },
            "required": ["location"]
          }
        }],
        "messages": [
          {"role": "user", "content": "What's the weather in Paris?"},
          {"role": "assistant", "content": null},
          {"role": "user", "content": [{
            "type": "tool_result",
            "tool_use_id": null,
            "content": "Current temperature: 88°F"
          }]}
        ]
      }
      JSON
      ```

      ```python Python

      client = anthropic.Anthropic()
      weather_tool = {
          "name": "get_weather",
          "description": "Get current weather for a location",
          "input_schema": {
              "type": "object",
              "properties": {"location": {"type": "string", "description": "City name"}},
              "required": ["location"],
          },
      }
      response = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          tools=[weather_tool],
          messages=[{"role": "user", "content": "What's the weather in Paris?"}],
      )
      # Extract the tool use block to get its ID for the tool result
      tool_use_block = next(block for block in response.content if block.type == "tool_use")

      # Call your actual weather API, here is where your actual API call would go
      # Let's pretend this is what we get back
      weather_data = {"temperature": 88}

      # Second request - Include the assistant turn and the tool result
      continuation = client.messages.create(
          model="claude-opus-4-8",
          max_tokens=16000,
          thinking={"type": "adaptive"},
          tools=[weather_tool],
          messages=[
              {"role": "user", "content": "What's the weather in Paris?"},
              # Echo the assistant content exactly as received. When a thinking
              # block is present, it must accompany the tool_use block.
              {"role": "assistant", "content": response.content},
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "tool_result",
                          "tool_use_id": tool_use_block.id,
                          "content": f"Current temperature: {weather_data['temperature']}°F",
                      }
                  ],
              },
          ],
      )
      print(continuation)
      ```

      ```typescript TypeScript
      const client = new Anthropic();

      const weatherTool: Anthropic.Tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      };

      const response = await client.messages.create({
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weatherTool],
        messages: [{ role: "user", content: "What's the weather in Paris?" }]
      });

      // Extract the tool use block to get its ID for the tool result
      const toolUseBlock = response.content.find(
        (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
      );

      // Call your actual weather API, here is where your actual API call would go
      // Let's pretend this is what we get back
      const weatherData = { temperature: 88 };

      if (toolUseBlock) {
        // Second request - Include the assistant turn and the tool result
        const continuation = await client.messages.create({
          model: "claude-opus-4-8",
          max_tokens: 16000,
          thinking: {
            type: "adaptive"
          },
          tools: [weatherTool],
          messages: [
            { role: "user", content: "What's the weather in Paris?" },
            // Echo the assistant content exactly as received. When a thinking
            // block is present, it must accompany the tool_use block.
            { role: "assistant", content: response.content },
            {
              role: "user",
              content: [
                {
                  type: "tool_result" as const,
                  tool_use_id: toolUseBlock.id,
                  content: `Current temperature: ${weatherData.temperature}°F`
                }
              ]
            }
          ]
        });
        console.log(continuation);
      }
      ```

      ```csharp C#
      AnthropicClient client = new();

      var weatherTool = new ToolUnion(new Tool()
      {
          Name = "get_weather",
          Description = "Get current weather for a location",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "City name" }),
              },
              Required = ["location"],
          },
      });

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Tools = [weatherTool],
          Messages = [
              new() { Role = Role.User, Content = "What's the weather in Paris?" }
          ]
      };

      var response = await client.Messages.Create(parameters);

      // Extract the tool_use block to get its ID for the tool result
      ToolUseBlock? toolUseBlock = null;
      foreach (var block in response.Content)
      {
          if (block.TryPickToolUse(out var toolUse))
          {
              toolUseBlock = toolUse;
              break;
          }
      }

      var weatherData = new { temperature = 88 };

      // Build continuation with tool result
      var continuationParams = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 16000,
          Thinking = new ThinkingConfigAdaptive(),
          Tools = [weatherTool],
          Messages = [
              new() { Role = Role.User, Content = "What's the weather in Paris?" },
              // response.Content includes the thinking blocks; passing them back is required
              new() { Role = Role.Assistant, Content = response.Content.Select(block => new ContentBlockParam(block.Json)).ToList() },
              new() { Role = Role.User, Content = new MessageParamContent(new List<ContentBlockParam>
              {
                  new ContentBlockParam(new ToolResultBlockParam()
                  {
                      ToolUseID = toolUseBlock?.ID ?? "",
                      Content = $"Current temperature: {weatherData.temperature}°F"
                  })
              })}
          ]
      };

      var continuation = await client.Messages.Create(continuationParams);
      Console.WriteLine(continuation);
      ```

      ```go Go
      client := anthropic.NewClient()

      weatherTool := anthropic.ToolUnionParam{
      	OfTool: &anthropic.ToolParam{
      		Name:        "get_weather",
      		Description: anthropic.String("Get current weather for a location"),
      		InputSchema: anthropic.ToolInputSchemaParam{
      			Properties: map[string]any{
      				"location": map[string]any{
      					"type":        "string",
      					"description": "City name",
      				},
      			},
      			Required: []string{"location"},
      		},
      	},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Tools: []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }

      var toolUseBlock anthropic.ToolUseBlock
      for _, block := range response.Content {
      	if v, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
      		toolUseBlock = v
      		break
      	}
      }

      weatherData := map[string]int{"temperature": 88}

      continuation, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 16000,
      	Thinking: anthropic.ThinkingConfigParamUnion{
      		OfAdaptive: &anthropic.ThinkingConfigAdaptiveParam{},
      	},
      	Tools: []anthropic.ToolUnionParam{weatherTool},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather in Paris?")),
      		response.ToParam(),
      		anthropic.NewUserMessage(
      			anthropic.NewToolResultBlock(toolUseBlock.ID, fmt.Sprintf("Current temperature: %d°F", weatherData["temperature"]), false),
      		),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }

      fmt.Println(continuation)
      ```

      ```java Java
      import com.anthropic.models.messages.ThinkingConfigAdaptive;
      // ...

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          Tool weatherTool = Tool.builder()
              .name("get_weather")
              .description("Get current weather for a location")
              .inputSchema(Tool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                      "location", Map.of("type", "string", "description", "City name")
                  )))
                  .required(List.of("location"))
                  .build())
              .build();

          MessageCreateParams initialParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addTool(weatherTool)
              .addUserMessage("What's the weather in Paris?")
              .build();

          Message response = client.messages().create(initialParams);

          ToolUseBlock toolUseBlock = null;
          for (var block : response.content()) {
              if (block.toolUse().isPresent()) {
                  toolUseBlock = block.toolUse().get();
                  break;
              }
          }

          int temperature = 88;

          // Second request: echo the assistant turn as received, then the tool result
          MessageCreateParams continuationParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(16000L)
              .thinking(ThinkingConfigAdaptive.builder().build())
              .addTool(weatherTool)
              .addUserMessage("What's the weather in Paris?")
              .addMessage(response)
              .addUserMessageOfBlockParams(List.of(
                  ContentBlockParam.ofToolResult(
                      ToolResultBlockParam.builder()
                          .toolUseId(toolUseBlock.id())
                          .content("Current temperature: " + temperature + "°F")
                          .build()
                  )
              ))
              .build();

          Message continuation = client.messages().create(continuationParams);
          IO.println(continuation);
      }
      ```

      ```php PHP
      $client = new Client();

      $weatherTool = [
          'name' => 'get_weather',
          'description' => 'Get current weather for a location',
          'input_schema' => [
              'type' => 'object',
              'properties' => [
                  'location' => [
                      'type' => 'string',
                      'description' => 'City name'
                  ]
              ],
              'required' => ['location']
          ]
      ];

      $response = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          tools: [$weatherTool],
      );

      $toolUseBlock = null;
      foreach ($response->content as $block) {
          if ($block->type === 'tool_use') {
              $toolUseBlock = $block;
              break;
          }
      }

      $weatherData = ['temperature' => 88];

      $continuation = $client->messages->create(
          maxTokens: 16000,
          messages: [
              ['role' => 'user', 'content' => "What's the weather in Paris?"],
              ['role' => 'assistant', 'content' => $response->content],
              ['role' => 'user', 'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => $toolUseBlock->id,
                      'content' => "Current temperature: {$weatherData['temperature']}°F"
                  ]
              ]]
          ],
          model: 'claude-opus-4-8',
          thinking: ['type' => 'adaptive'],
          tools: [$weatherTool],
      );

      echo $continuation;
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      weather_tool = {
        name: "get_weather",
        description: "Get current weather for a location",
        input_schema: {
          type: "object",
          properties: {
            location: { type: "string", description: "City name" }
          },
          required: ["location"]
        }
      }

      response = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" }
        ]
      )

      tool_use_block = response.content.find { |block| block.type == :tool_use }

      raise "No tool_use block found" unless tool_use_block

      weather_data = { temperature: 88 }

      continuation = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 16000,
        thinking: {
          type: "adaptive"
        },
        tools: [weather_tool],
        messages: [
          { role: "user", content: "What's the weather in Paris?" },
          { role: "assistant", content: response.content },
          { role: "user", content: [
            {
              type: "tool_result",
              tool_use_id: tool_use_block.id,
              content: "Current temperature: #{weather_data[:temperature]}°F"
            }
          ] }
        ]
      )

      puts continuation
      ```
    </CodeGroup>
  </Step>

  <Step title="Read the final response">
    You should see Claude complete the turn with text. Because [interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#interleaved-thinking) is automatic in adaptive mode, the continuation can also open with a new thinking block before the final text:

    ```json Output
    {
      "content": [
        {
          "type": "text",
          "text": "Currently in Paris, the temperature is 88°F (31°C)"
        }
      ]
    }
    ```
  </Step>
</Steps>

## How interleaved thinking changes the flow

Interleaved thinking lets Claude think between tool calls, reasoning about each tool result before acting on it. The concept and per-model availability are covered in [Interleaved thinking](https://platform.claude.com/docs/en/build-with-claude/thinking#interleaved-thinking) on the Thinking page; interleaving changes where thinking blocks appear, not whether tool calls can chain. The following comparison shows what interleaved thinking changes in a two-tool workflow:

<AccordionGroup>
  <Accordion title="Tool use without interleaved thinking">
    Without interleaved thinking, Claude thinks once at the start of the assistant turn. Subsequent responses after tool results continue without new thinking blocks.

    ```text
    User: "What's the total revenue if we sold 150 units at $50 each,
           and how does this compare to our average monthly revenue?"

    Response 1: [thinking] "I need to calculate 150 * $50, then check the database..."
                [tool_use: calculator] { "expression": "150 * 50" }
      ↓ tool result: "7500"

    Response 2: [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
                ↑ no thinking block
      ↓ tool result: "5200"

    Response 3: [text] "The total revenue is $7,500, which is 44% above your
                average monthly revenue of $5,200."
                ↑ no thinking block
    ```
  </Accordion>

  <Accordion title="Tool use with interleaved thinking">
    With interleaved thinking enabled, Claude can think after receiving each tool result, allowing it to reason about intermediate results before continuing.

    ```text
    User: "What's the total revenue if we sold 150 units at $50 each,
           and how does this compare to our average monthly revenue?"

    Response 1: [thinking] "I need to calculate 150 * $50 first..."
                [tool_use: calculator] { "expression": "150 * 50" }
      ↓ tool result: "7500"

    Response 2: [thinking] "Got $7,500. Now I should query the database to compare..."
                [tool_use: database_query] { "query": "SELECT AVG(revenue)..." }
                ↑ thinking after receiving calculator result
      ↓ tool result: "5200"

    Response 3: [thinking] "$7,500 vs $5,200 average - that's a 44% increase..."
                [text] "The total revenue is $7,500, which is 44% above your
                average monthly revenue of $5,200."
                ↑ thinking before final answer
    ```
  </Accordion>
</AccordionGroup>

## Next steps

<CardGroup cols={3}>
  <Card title="Thinking" icon="brain" href="https://platform.claude.com/docs/en/build-with-claude/thinking">
    The overview: turn thinking on, read thinking output, and review the full rules for tool use, caching, and streaming.
  </Card>

  <Card title="Steering thinking" icon="compass" href="https://platform.claude.com/docs/en/build-with-claude/thinking-steering-and-cost">
    Steer how often and how deeply Claude thinks with effort levels and prompt-based guidance.
  </Card>

  <Card title="Extended thinking" icon="clock" href="https://platform.claude.com/docs/en/build-with-claude/extended-thinking">
    Manual thinking budgets on older models: `budget_tokens` mechanics and migration to adaptive.
  </Card>
</CardGroup>
