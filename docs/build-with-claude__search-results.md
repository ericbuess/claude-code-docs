---
title: Search results
url: https://platform.claude.com/docs/en/build-with-claude/search-results
description: Enable natural citations for RAG applications by providing search results with source attribution
---

<Note>
  For how zero data retention (ZDR) applies to this feature, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).
</Note>

Search result content blocks let Claude cite your own content the same way it cites web search results: each citation carries the source and title you provided. Use them in RAG (Retrieval-Augmented Generation) applications where Claude needs to attribute answers to your documents.

All [active models](https://platform.claude.com/docs/en/about-claude/models/overview) support search results with citations, with the exception of Claude Haiku 3. No beta header is required: search results are part of the standard Messages API.

## How it works

Search results can be provided in two ways:

1. **From tool calls:** Your custom tools return search results, enabling dynamic RAG applications
2. **As top-level content:** You provide search results directly in user messages for pre-fetched or cached content

In both cases, Claude cites the search results automatically when citations are enabled. No special prompting is needed: ask your question, and citations appear on the text blocks that draw on your content.

### Search result schema

Search results use the following structure:

```json
{
  "type": "search_result",
  "source": "https://example.com/article", // Required: Source URL or identifier
  "title": "Article Title", // Required: Title of the result
  "content": [
    // Required: Array of text blocks
    {
      "type": "text",
      "text": "The actual content of the search result..."
    }
  ],
  "citations": {
    // Optional: Citation configuration
    "enabled": true // Enable/disable citations for this result
  }
}
```

### Required fields

| Field     | Type   | Description                                                                                                      |
| --------- | ------ | ---------------------------------------------------------------------------------------------------------------- |
| `type`    | string | Must be `"search_result"`                                                                                        |
| `source`  | string | The source of the content. Any stable string works: a URL, or an internal identifier such as `kb://article-1234` |
| `title`   | string | A descriptive title for the search result                                                                        |
| `content` | array  | An array of text blocks containing the actual content                                                            |

### Optional fields

| Field           | Type   | Description                                                                                                                                                                                                                                                                                                                     |
| --------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `citations`     | object | Citation configuration with `enabled` Boolean field. Citations are disabled by default; every example on this page sets `"enabled": true` explicitly. All search results in a request must use the same setting (see [Citation control](https://platform.claude.com/docs/en/build-with-claude/search-results#citation-control)) |
| `cache_control` | object | Cache control settings (for example, `{"type": "ephemeral"}`)                                                                                                                                                                                                                                                                   |

Each item in the `content` array must be a text block with:

* `type`: Must be `"text"`
* `text`: The actual text content (non-empty string)

Search results hold text only. Images and other media are not supported inside the `content` array.

## Method 1: Search results from tool calls

Returning search results from your custom tools enables dynamic RAG applications: tools fetch content at runtime, and Claude cites it in the response. The following example forces the tool call with [`tool_choice`](https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools#forcing-tool-use), so the retrieval step runs every time.

### Example: Knowledge base tool

<CodeGroup>
  ```bash cURL
  # The tool-calling flow needs application-side search logic that doesn't
  # translate to a one-off shell command. See the SDK tabs for the full flow.
  # The raw shape of a tool conversation with search results is shown in the
  # Combining both methods cURL tab; Method 2 shows the top-level shape.
  ```

  ```bash CLI
  # The tool-calling flow needs application-side search logic that doesn't
  # translate to a one-off shell command. See the SDK tabs for the full flow.
  # The raw shape of a tool conversation with search results is shown in the
  # Combining both methods cURL tab; Method 2 shows the top-level shape.
  ```

  ```python Python
  from anthropic.types import (
      MessageParam,
      TextBlockParam,
      SearchResultBlockParam,
      ToolResultBlockParam,
  )

  client = Anthropic()

  # Define a knowledge base search tool
  knowledge_base_tool = {
      "name": "search_knowledge_base",
      "description": "Search the company knowledge base for information",
      "input_schema": {
          "type": "object",
          "properties": {"query": {"type": "string", "description": "The search query"}},
          "required": ["query"],
      },
  }


  # Function to handle the tool call
  def search_knowledge_base(query):
      # Your search logic here
      # Returns search results in the correct format
      return [
          SearchResultBlockParam(
              type="search_result",
              source="https://docs.company.com/product-guide",
              title="Product Configuration Guide",
              content=[
                  TextBlockParam(
                      type="text",
                      text="To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.",
                  )
              ],
              citations={"enabled": True},
          ),
          SearchResultBlockParam(
              type="search_result",
              source="https://docs.company.com/troubleshooting",
              title="Troubleshooting Guide",
              content=[
                  TextBlockParam(
                      type="text",
                      text="If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.",
                  )
              ],
              citations={"enabled": True},
          ),
      ]


  # Build up the conversation in a list, starting with the user's question
  messages = [
      MessageParam(role="user", content="How do I configure the timeout settings?")
  ]

  # Create a message with the tool
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      tools=[knowledge_base_tool],
      tool_choice={"type": "tool", "name": "search_knowledge_base"},
      messages=messages,
  )

  # When Claude calls the tool, provide the search results.
  # The tool_use block is not always first: iterate to find it.
  tool_use = next((block for block in response.content if block.type == "tool_use"), None)
  if tool_use is not None:
      tool_result = search_knowledge_base(tool_use.input["query"])

      # Append Claude's turn, then the tool result, to the running conversation
      messages.append(MessageParam(role="assistant", content=response.content))
      messages.append(
          MessageParam(
              role="user",
              content=[
                  ToolResultBlockParam(
                      type="tool_result",
                      tool_use_id=tool_use.id,
                      content=tool_result,  # Search results go here
                  )
              ],
          )
      )

      # Send the tool result back
      final_response = client.messages.create(
          model="claude-opus-5",
          max_tokens=1024,
          messages=messages,
      )
      print(final_response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Define a knowledge base search tool
  const knowledgeBaseTool: Anthropic.Tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object" as const,
      properties: {
        query: {
          type: "string",
          description: "The search query"
        }
      },
      required: ["query"]
    }
  };

  // Function to handle the tool call
  function searchKnowledgeBase(query: string) {
    // Your search logic here
    // Returns search results in the correct format
    return [
      {
        type: "search_result" as const,
        source: "https://docs.company.com/product-guide",
        title: "Product Configuration Guide",
        content: [
          {
            type: "text" as const,
            text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
          }
        ],
        citations: { enabled: true }
      },
      {
        type: "search_result" as const,
        source: "https://docs.company.com/troubleshooting",
        title: "Troubleshooting Guide",
        content: [
          {
            type: "text" as const,
            text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
          }
        ],
        citations: { enabled: true }
      }
    ];
  }

  // Build up the conversation in a list, starting with the user's question
  const messages: Anthropic.MessageParam[] = [
    { role: "user", content: "How do I configure the timeout settings?" }
  ];

  // Create a message with the tool
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [knowledgeBaseTool],
    tool_choice: { type: "tool", name: "search_knowledge_base" },
    messages
  });

  // Handle tool use and provide results.
  // The tool_use block is not always first: find it in the content array.
  const toolUse = response.content.find(
    (block): block is Anthropic.ToolUseBlock => block.type === "tool_use"
  );
  if (toolUse) {
    const input = toolUse.input as { query: string };
    const toolResult = searchKnowledgeBase(input.query);

    // Append Claude's turn, then the tool result, to the running conversation
    messages.push({ role: "assistant", content: response.content });
    messages.push({
      role: "user",
      content: [
        {
          type: "tool_result" as const,
          tool_use_id: toolUse.id,
          content: toolResult // Search results go here
        }
      ]
    });

    // Send the tool result back
    const finalResponse = await client.messages.create({
      model: "claude-opus-5",
      max_tokens: 1024,
      messages
    });
    console.log(finalResponse);
  }
  ```

  ```csharp C#
  AnthropicClient client = new();

  var tools = new List<ToolUnion>
  {
      new ToolUnion(new Tool()
      {
          Name = "search_knowledge_base",
          Description = "Search the company knowledge base for information",
          InputSchema = new InputSchema()
          {
              Properties = new Dictionary<string, JsonElement>
              {
                  ["query"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The search query" }),
              },
              Required = ["query"],
          },
      }),
  };

  // Function to handle the tool call
  static List<Block> SearchKnowledgeBase(string query)
  {
      // Your search logic here
      // Returns search results in the correct format
      return
      [
          new SearchResultBlockParam
          {
              Source = "https://docs.company.com/product-guide",
              Title = "Product Configuration Guide",
              Content = [new() { Text = "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs." }],
              Citations = new() { Enabled = true },
          },
          new SearchResultBlockParam
          {
              Source = "https://docs.company.com/troubleshooting",
              Title = "Troubleshooting Guide",
              Content = [new() { Text = "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values." }],
              Citations = new() { Enabled = true },
          },
      ];
  }

  // Build up the conversation in a list, starting with the user's question
  List<MessageParam> messages = [new() { Role = Role.User, Content = "How do I configure the timeout settings?" }];

  // Create a message with the tool
  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Tools = tools,
      ToolChoice = new ToolChoiceTool { Name = "search_knowledge_base" },
      Messages = messages,
  });

  // When Claude calls the tool, provide the search results.
  // The tool_use block is not always first: find the first one.
  foreach (var block in response.Content)
  {
      if (block.TryPickToolUse(out var toolUse))
      {
          var query = toolUse.Input["query"].GetString() ?? "";
          var toolResults = SearchKnowledgeBase(query);

          // Append Claude's turn, then the tool result, to the running conversation
          messages.Add(new() { Role = Role.Assistant, Content = response.Content.Select(contentBlock => new ContentBlockParam(contentBlock.Json)).ToList() });
          messages.Add(new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
                  [new ContentBlockParam(new ToolResultBlockParam() { ToolUseID = toolUse.ID, Content = new ToolResultBlockParamContent(toolResults) })]
              ),
          });

          // Send the tool result back
          var finalResponse = await client.Messages.Create(new()
          {
              Model = Model.ClaudeOpus5,
              MaxTokens = 1024,
              Messages = messages,
          });
          Console.WriteLine(finalResponse);
          break;
      }
  }
  ```

  ```go Go
  	client := anthropic.NewClient()

  	knowledgeBaseTool := anthropic.ToolUnionParam{
  		OfTool: &anthropic.ToolParam{
  			Name:        "search_knowledge_base",
  			Description: anthropic.String("Search the company knowledge base for information"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"query": map[string]any{
  						"type":        "string",
  						"description": "The search query",
  					},
  				},
  				Required: []string{"query"},
  			},
  		},
  	}

  	// Build up the conversation in a slice, starting with the user's question
  	messages := []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("How do I configure the timeout settings?")),
  	}

  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:      anthropic.ModelClaudeOpus5,
  		MaxTokens:  1024,
  		Tools:      []anthropic.ToolUnionParam{knowledgeBaseTool},
  		ToolChoice: anthropic.ToolChoiceUnionParam{OfTool: &anthropic.ToolChoiceToolParam{Name: "search_knowledge_base"}},
  		Messages:   messages,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	// The tool_use block is not always first: find it in the content list
  	var toolUse *anthropic.ToolUseBlock
  	for _, block := range response.Content {
  		if variant, ok := block.AsAny().(anthropic.ToolUseBlock); ok {
  			toolUse = &variant
  			break
  		}
  	}

  	if toolUse != nil {
  		var input struct {
  			Query string `json:"query"`
  		}
  		if err := json.Unmarshal(toolUse.Input, &input); err != nil {
  			log.Fatal(err)
  		}
  		toolResults := searchKnowledgeBase(input.Query)

  		// Append Claude's turn, then the tool result, to the running conversation
  		messages = append(messages, response.ToParam())
  		messages = append(messages, anthropic.NewUserMessage(anthropic.ContentBlockParamUnion{
  			OfToolResult: &anthropic.ToolResultBlockParam{
  				ToolUseID: toolUse.ID,
  				Content:   toolResults,
  			},
  		}))

  		// Send the tool result back
  		finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  			Model:     anthropic.ModelClaudeOpus5,
  			MaxTokens: 1024,
  			Messages:  messages,
  		})
  		if err != nil {
  			log.Fatal(err)
  		}
  		fmt.Println(finalResponse)
  	}
  // ...
  func searchKnowledgeBase(query string) []anthropic.ToolResultBlockParamContentUnion {
  	return []anthropic.ToolResultBlockParamContentUnion{
  		{OfSearchResult: &anthropic.SearchResultBlockParam{
  			Content: []anthropic.TextBlockParam{
  				{Text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."},
  			},
  			Source:    "https://docs.company.com/product-guide",
  			Title:     "Product Configuration Guide",
  			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  		}},
  		{OfSearchResult: &anthropic.SearchResultBlockParam{
  			Content: []anthropic.TextBlockParam{
  				{Text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."},
  			},
  			Source:    "https://docs.company.com/troubleshooting",
  			Title:     "Troubleshooting Guide",
  			Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  		}},
  	}
  }
  ```

  ```java Java
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.MessageParam;
  import com.anthropic.models.messages.Model;
  import com.anthropic.models.messages.SearchResultBlockParam;
  import com.anthropic.models.messages.TextBlockParam;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.ToolChoice;
  import com.anthropic.models.messages.ToolChoiceTool;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.core.JsonValue;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool knowledgeBaseTool = Tool.builder()
          .name("search_knowledge_base")
          .description("Search the company knowledge base for information")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "query", Map.of(
                      "type", "string",
                      "description", "The search query"
                  )
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("query")))
              .build())
          .build();

      // Build up the conversation in a list, starting with the user's question
      List<MessageParam> messages = new ArrayList<>();
      messages.add(MessageParam.builder()
          .role(MessageParam.Role.USER)
          .content("How do I configure the timeout settings?")
          .build());

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addTool(knowledgeBaseTool)
          .toolChoice(ToolChoice.ofTool(ToolChoiceTool.builder()
              .name("search_knowledge_base")
              .build()))
          .messages(messages)
          .build();

      Message response = client.messages().create(params);

      // The tool_use block is not always first: find it in the content list
      response.content().stream()
          .flatMap(contentBlock -> contentBlock.toolUse().stream())
          .findFirst()
          .ifPresent(toolUse -> {
              Map<String, JsonValue> input =
                  (Map<String, JsonValue>) toolUse._input().asObject().get();
              List<ToolResultBlockParam.Content.Block> toolResult = searchKnowledgeBase(
                  input.get("query").asStringOrThrow()
              );

              // Append Claude's entire turn to the running conversation, then the tool result.
              // Rebuilding only the tool_use block would drop any other content blocks Claude
              // returned (e.g. leading text when the tool call is not forced) — append the
              // full turn, as the other language tabs do.
              messages.add(MessageParam.builder()
                  .role(MessageParam.Role.ASSISTANT)
                  .contentOfBlockParams(
                      response.content().stream()
                          .map(block -> block.toParam())
                          .toList()
                  )
                  .build());
              messages.add(MessageParam.builder()
                  .role(MessageParam.Role.USER)
                  .contentOfBlockParams(List.of(
                      ContentBlockParam.ofToolResult(
                          ToolResultBlockParam.builder()
                              .toolUseId(toolUse.id())
                              .contentOfBlocks(toolResult)
                              .build()
                      )
                  ))
                  .build());

              // Send the tool result back
              MessageCreateParams finalParams = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
                  .maxTokens(1024L)
                  .messages(messages)
                  .build();

              Message finalResponse = client.messages().create(finalParams);
              System.out.println(finalResponse);
          });
  }

  static List<ToolResultBlockParam.Content.Block> searchKnowledgeBase(String query) {
      return List.of(
          ToolResultBlockParam.Content.Block.ofSearchResult(
              SearchResultBlockParam.builder()
                  .source("https://docs.company.com/product-guide")
                  .title("Product Configuration Guide")
                  .content(List.of(
                      TextBlockParam.builder()
                          .text("To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.")
                          .build()
                  ))
                  .citations(CitationsConfigParam.builder().enabled(true).build())
                  .build()
          ),
          ToolResultBlockParam.Content.Block.ofSearchResult(
              SearchResultBlockParam.builder()
                  .source("https://docs.company.com/troubleshooting")
                  .title("Troubleshooting Guide")
                  .content(List.of(
                      TextBlockParam.builder()
                          .text("If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.")
                          .build()
                  ))
                  .citations(CitationsConfigParam.builder().enabled(true).build())
                  .build()
          )
      );
  }
  ```

  ```php PHP
  $client = new Client();

  $knowledgeBaseTool = [
      'name' => 'search_knowledge_base',
      'description' => 'Search the company knowledge base for information',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'query' => [
                  'type' => 'string',
                  'description' => 'The search query'
              ]
          ],
          'required' => ['query']
      ]
  ];

  function searchKnowledgeBase($query) {
      return [
          [
              'type' => 'search_result',
              'source' => 'https://docs.company.com/product-guide',
              'title' => 'Product Configuration Guide',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => 'To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs.'
                  ]
              ],
              'citations' => ['enabled' => true]
          ],
          [
              'type' => 'search_result',
              'source' => 'https://docs.company.com/troubleshooting',
              'title' => 'Troubleshooting Guide',
              'content' => [
                  [
                      'type' => 'text',
                      'text' => 'If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values.'
                  ]
              ],
              'citations' => ['enabled' => true]
          ]
      ];
  }

  // Build up the conversation in a list, starting with the user's question
  $messages = [
      ['role' => 'user', 'content' => 'How do I configure the timeout settings?']
  ];

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: $messages,
      model: 'claude-opus-5',
      toolChoice: ['type' => 'tool', 'name' => 'search_knowledge_base'],
      tools: [$knowledgeBaseTool],
  );

  $toolUseBlock = null;
  foreach ($response->content as $block) {
      if ($block->type === 'tool_use') {
          $toolUseBlock = $block;
          break;
      }
  }

  if ($toolUseBlock !== null) {
      $toolResult = searchKnowledgeBase($toolUseBlock->input['query']);

      // Append Claude's turn, then the tool result, to the running conversation
      $messages[] = ['role' => 'assistant', 'content' => $response->content];
      $messages[] = [
          'role' => 'user',
          'content' => [
              [
                  'type' => 'tool_result',
                  'tool_use_id' => $toolUseBlock->id,
                  'content' => $toolResult
              ]
          ]
      ];

      // Send the tool result back
      $finalResponse = $client->messages->create(
          maxTokens: 1024,
          messages: $messages,
          model: 'claude-opus-5',
      );
      echo $finalResponse;
  } else {
      echo $response;
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  knowledge_base_tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "The search query" }
      },
      required: ["query"]
    }
  }

  def search_knowledge_base(query)
    [
      {
        type: "search_result",
        source: "https://docs.company.com/product-guide",
        title: "Product Configuration Guide",
        content: [
          {
            type: "text",
            text: "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
          }
        ],
        citations: { enabled: true }
      },
      {
        type: "search_result",
        source: "https://docs.company.com/troubleshooting",
        title: "Troubleshooting Guide",
        content: [
          {
            type: "text",
            text: "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
          }
        ],
        citations: { enabled: true }
      }
    ]
  end

  # Build up the conversation in a list, starting with the user's question
  messages = [
    { role: "user", content: "How do I configure the timeout settings?" }
  ]

  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [knowledge_base_tool],
    tool_choice: { type: "tool", name: "search_knowledge_base" },
    messages: messages
  )

  # The tool_use block is not always first: find it in the content array
  tool_use = response.content.find { |block| block.type == :tool_use }

  if tool_use
    tool_result = search_knowledge_base(tool_use.input[:query])

    # Append Claude's turn, then the tool result, to the running conversation
    messages << { role: "assistant", content: response.content }
    messages << {
      role: "user",
      content: [
        {
          type: "tool_result",
          tool_use_id: tool_use.id,
          content: tool_result
        }
      ]
    }

    # Send the tool result back
    final_response = client.messages.create(
      model: "claude-opus-5",
      max_tokens: 1024,
      messages: messages
    )
    puts final_response
  end
  ```
</CodeGroup>

## Method 2: Search results as top-level content

You can also provide search results directly in user messages. This is useful for:

* Pre-fetched content from your search infrastructure
* Cached search results from previous queries
* Content from external search services
* Testing and development

### Example: Direct search results

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "search_result",
              "source": "https://docs.company.com/api-reference",
              "title": "API Reference - Authentication",
              "content": [
                {
                  "type": "text",
                  "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                }
              ],
              "citations": {
                "enabled": true
              }
            },
            {
              "type": "search_result",
              "source": "https://docs.company.com/quickstart",
              "title": "Getting Started Guide",
              "content": [
                {
                  "type": "text",
                  "text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                }
              ],
              "citations": {
                "enabled": true
              }
            },
            {
              "type": "text",
              "text": "Based on these search results, how do I authenticate API requests and what are the rate limits?"
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  messages:
    - role: user
      content:
        - type: search_result
          source: https://docs.company.com/api-reference
          title: API Reference - Authentication
          content:
            - type: text
              text: >-
                All API requests must include an API key in the Authorization
                header. Keys can be generated from the dashboard. Rate limits:
                1000 requests per hour for standard tier, 10000 for premium.
          citations:
            enabled: true
        - type: search_result
          source: https://docs.company.com/quickstart
          title: Getting Started Guide
          content:
            - type: text
              text: >-
                To get started: 1) Sign up for an account, 2) Generate an API
                key from the dashboard, 3) Install our SDK using pip install
                company-sdk, 4) Initialize the client with your API key.
          citations:
            enabled: true
        - type: text
          text: >-
            Based on these search results, how do I authenticate API requests
            and what are the rate limits?
  YAML
  ```

  ```python Python
  from anthropic.types import MessageParam, TextBlockParam, SearchResultBlockParam

  client = Anthropic()

  # Provide search results directly in the user message
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      messages=[
          MessageParam(
              role="user",
              content=[
                  SearchResultBlockParam(
                      type="search_result",
                      source="https://docs.company.com/api-reference",
                      title="API Reference - Authentication",
                      content=[
                          TextBlockParam(
                              type="text",
                              text="All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.",
                          )
                      ],
                      citations={"enabled": True},
                  ),
                  SearchResultBlockParam(
                      type="search_result",
                      source="https://docs.company.com/quickstart",
                      title="Getting Started Guide",
                      content=[
                          TextBlockParam(
                              type="text",
                              text="To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.",
                          )
                      ],
                      citations={"enabled": True},
                  ),
                  TextBlockParam(
                      type="text",
                      text="Based on these search results, how do I authenticate API requests and what are the rate limits?",
                  ),
              ],
          )
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  // Provide search results directly in the user message
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result" as const,
            source: "https://docs.company.com/api-reference",
            title: "API Reference - Authentication",
            content: [
              {
                type: "text" as const,
                text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "search_result" as const,
            source: "https://docs.company.com/quickstart",
            title: "Getting Started Guide",
            content: [
              {
                type: "text" as const,
                text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text" as const,
            text: "Based on these search results, how do I authenticate API requests and what are the rate limits?"
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Provide search results directly in the user message
  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new SearchResultBlockParam
                  {
                      Source = "https://docs.company.com/api-reference",
                      Title = "API Reference - Authentication",
                      Content = [new() { Text = "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium." }],
                      Citations = new() { Enabled = true },
                  }),
                  new ContentBlockParam(new SearchResultBlockParam
                  {
                      Source = "https://docs.company.com/quickstart",
                      Title = "Getting Started Guide",
                      Content = [new() { Text = "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key." }],
                      Citations = new() { Enabled = true },
                  }),
                  new ContentBlockParam(new TextBlockParam { Text = "Based on these search results, how do I authenticate API requests and what are the rate limits?" }),
              ]),
          },
      ],
  });

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
  				Content: []anthropic.TextBlockParam{
  					{Text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."},
  				},
  				Source:    "https://docs.company.com/api-reference",
  				Title:     "API Reference - Authentication",
  				Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  			}},
  			anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
  				Content: []anthropic.TextBlockParam{
  					{Text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."},
  				},
  				Source:    "https://docs.company.com/quickstart",
  				Title:     "Getting Started Guide",
  				Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  			}},
  			anthropic.NewTextBlock("Based on these search results, how do I authenticate API requests and what are the rate limits?"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.ContentBlockParam;
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.SearchResultBlockParam;
  import com.anthropic.models.messages.TextBlockParam;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofSearchResult(
                  SearchResultBlockParam.builder()
                      .source("https://docs.company.com/api-reference")
                      .title("API Reference - Authentication")
                      .content(List.of(
                          TextBlockParam.builder()
                              .text("All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.")
                              .build()
                      ))
                      .citations(CitationsConfigParam.builder().enabled(true).build())
                      .build()
              ),
              ContentBlockParam.ofSearchResult(
                  SearchResultBlockParam.builder()
                      .source("https://docs.company.com/quickstart")
                      .title("Getting Started Guide")
                      .content(List.of(
                          TextBlockParam.builder()
                              .text("To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.")
                              .build()
                      ))
                      .citations(CitationsConfigParam.builder().enabled(true).build())
                      .build()
              ),
              ContentBlockParam.ofText(
                  TextBlockParam.builder()
                      .text("Based on these search results, how do I authenticate API requests and what are the rate limits?")
                      .build()
              )
          ))
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'search_result',
                      'source' => 'https://docs.company.com/api-reference',
                      'title' => 'API Reference - Authentication',
                      'content' => [
                          [
                              'type' => 'text',
                              'text' => 'All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.'
                          ]
                      ],
                      'citations' => ['enabled' => true]
                  ],
                  [
                      'type' => 'search_result',
                      'source' => 'https://docs.company.com/quickstart',
                      'title' => 'Getting Started Guide',
                      'content' => [
                          [
                              'type' => 'text',
                              'text' => 'To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.'
                          ]
                      ],
                      'citations' => ['enabled' => true]
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Based on these search results, how do I authenticate API requests and what are the rate limits?'
                  ]
              ]
          ]
      ],
      model: 'claude-opus-5',
  );

  echo json_encode($message, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result",
            source: "https://docs.company.com/api-reference",
            title: "API Reference - Authentication",
            content: [
              {
                type: "text",
                text: "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "search_result",
            source: "https://docs.company.com/quickstart",
            title: "Getting Started Guide",
            content: [
              {
                type: "text",
                text: "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "Based on these search results, how do I authenticate API requests and what are the rate limits?"
          }
        ]
      }
    ]
  )

  puts message
  ```
</CodeGroup>

## Claude's response with citations

Regardless of how search results are provided, Claude automatically includes citations when using information from them:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium.",
          "source": "https://docs.company.com/api-reference",
          "title": "API Reference - Authentication",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    },
    {
      "type": "text",
      "text": "\n\nTo set this up from scratch, you'll need to "
    },
    {
      "type": "text",
      "text": "sign up for an account, generate an API key from the dashboard, install the SDK using `pip install company-sdk`, and initialize the client with your API key.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key.",
          "source": "https://docs.company.com/quickstart",
          "title": "Getting Started Guide",
          "search_result_index": 1,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    }
  ]
}
```

### Citation fields

Each citation includes:

| Field                 | Type           | Description                                                                                                                                                               |
| --------------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`                | string         | Always `"search_result_location"` for search result citations                                                                                                             |
| `source`              | string         | The source from the original search result                                                                                                                                |
| `title`               | string or null | The title from the original search result                                                                                                                                 |
| `cited_text`          | string         | The full text of the cited block(s), concatenated. Equals the contents of `content[start_block_index:end_block_index]` joined together. Not counted toward output tokens. |
| `search_result_index` | integer        | 0-based index of the cited search result among all `search_result` blocks in the request, in the order they appear (across all messages and tool results).                |
| `start_block_index`   | integer        | 0-based index of the first cited block in the search result's `content` array.                                                                                            |
| `end_block_index`     | integer        | Exclusive end index of the cited block range in the search result's `content` array. Always greater than `start_block_index`.                                             |

The block indices identify a slice of the search result's `content` array, and `cited_text` is the full text of that slice. The text block is the minimal citable unit: Claude cites whole blocks, not substrings within a block. To get finer-grained citations, split your search result content into smaller blocks (see [Multiple content blocks](https://platform.claude.com/docs/en/build-with-claude/search-results#multiple-content-blocks)).

## Multiple content blocks

Search results can contain multiple text blocks in the `content` array:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/api-guide",
  "title": "API Documentation",
  "content": [
    {
      "type": "text",
      "text": "Authentication: All API requests require an API key."
    },
    {
      "type": "text",
      "text": "Rate Limits: The API allows 1000 requests per hour per key."
    },
    {
      "type": "text",
      "text": "Error Handling: The API returns standard HTTP status codes."
    }
  ],
  "citations": { "enabled": true }
}
```

A citation referencing the rate limits block looks like:

```json
{
  "type": "search_result_location",
  "cited_text": "Rate Limits: The API allows 1000 requests per hour per key.",
  "source": "https://docs.company.com/api-guide",
  "title": "API Documentation",
  "search_result_index": 0,
  "start_block_index": 1,
  "end_block_index": 2
}
```

When this search result is cited, `start_block_index` and `end_block_index` identify which of these blocks the citation covers, and `cited_text` contains exactly those blocks' text. Splitting content into smaller, focused blocks gives Claude finer citation boundaries; combining content into one block means every citation returns the full text. This is the same model used by [custom content documents](https://platform.claude.com/docs/en/build-with-claude/citations#custom-content-documents) in the Citations feature.

## Advanced usage

### Combining both methods

You can mix both methods in the same conversation. Claude cites from either source, and `search_result_index` counts all `search_result` blocks in request order, regardless of source.

The following example replays a complete conversation. The first user message carries a pre-fetched search result, the assistant turn calls a knowledge base tool, and the tool result returns a second search result. Claude's answer cites both sources:

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "content-type: application/json" \
    -d '{
      "model": "claude-opus-5",
      "max_tokens": 1024,
      "tools": [
        {
          "name": "search_knowledge_base",
          "description": "Search the company knowledge base for information",
          "input_schema": {
            "type": "object",
            "properties": {
              "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "search_result",
              "source": "https://docs.company.com/overview",
              "title": "Product Overview",
              "content": [
                {
                  "type": "text",
                  "text": "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."
                }
              ],
              "citations": {"enabled": true}
            },
            {
              "type": "text",
              "text": "What does Acme Dashboard do, and what plans is it available on?"
            }
          ]
        },
        {
          "role": "assistant",
          "content": [
            {
              "type": "text",
              "text": "Let me check the pricing information."
            },
            {
              "type": "tool_use",
              "id": "toolu_01A09q90qw90lq917835lq9",
              "name": "search_knowledge_base",
              "input": {"query": "Acme Dashboard pricing plans"}
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "tool_result",
              "tool_use_id": "toolu_01A09q90qw90lq917835lq9",
              "content": [
                {
                  "type": "search_result",
                  "source": "https://docs.company.com/pricing",
                  "title": "Pricing Plans",
                  "content": [
                    {
                      "type": "text",
                      "text": "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."
                    }
                  ],
                  "citations": {"enabled": true}
                }
              ]
            }
          ]
        }
      ]
    }'
  ```

  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-5
  max_tokens: 1024
  tools:
    - name: search_knowledge_base
      description: Search the company knowledge base for information
      input_schema:
        type: object
        properties:
          query:
            type: string
            description: The search query
        required: [query]
  messages:
    - role: user
      content:
        - type: search_result
          source: https://docs.company.com/overview
          title: Product Overview
          content:
            - type: text
              text: >-
                Acme Dashboard is a monitoring tool for distributed systems.
                It supports real-time alerting and custom metric dashboards.
          citations:
            enabled: true
        - type: text
          text: What does Acme Dashboard do, and what plans is it available on?
    - role: assistant
      content:
        - type: text
          text: Let me check the pricing information.
        - type: tool_use
          id: toolu_01A09q90qw90lq917835lq9
          name: search_knowledge_base
          input:
            query: Acme Dashboard pricing plans
    - role: user
      content:
        - type: tool_result
          tool_use_id: toolu_01A09q90qw90lq917835lq9
          content:
            - type: search_result
              source: https://docs.company.com/pricing
              title: Pricing Plans
              content:
                - type: text
                  text: >-
                    Acme Dashboard is available on the Starter plan at $10 per
                    user per month and the Enterprise plan with custom pricing.
              citations:
                enabled: true
  YAML
  ```

  ```python Python
  from anthropic.types import (
      MessageParam,
      SearchResultBlockParam,
      TextBlockParam,
      ToolResultBlockParam,
      ToolUseBlockParam,
  )

  client = Anthropic()

  knowledge_base_tool = {
      "name": "search_knowledge_base",
      "description": "Search the company knowledge base for information",
      "input_schema": {
          "type": "object",
          "properties": {"query": {"type": "string", "description": "The search query"}},
          "required": ["query"],
      },
  }

  # Replay a conversation that provides search results both ways: the first
  # user message carries a pre-fetched result, the tool result returns another
  response = client.messages.create(
      model="claude-opus-5",
      max_tokens=1024,
      tools=[knowledge_base_tool],
      messages=[
          MessageParam(
              role="user",
              content=[
                  SearchResultBlockParam(
                      type="search_result",
                      source="https://docs.company.com/overview",
                      title="Product Overview",
                      content=[
                          TextBlockParam(
                              type="text",
                              text="Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.",
                          )
                      ],
                      citations={"enabled": True},
                  ),
                  TextBlockParam(
                      type="text",
                      text="What does Acme Dashboard do, and what plans is it available on?",
                  ),
              ],
          ),
          MessageParam(
              role="assistant",
              content=[
                  TextBlockParam(
                      type="text", text="Let me check the pricing information."
                  ),
                  ToolUseBlockParam(
                      type="tool_use",
                      id="toolu_01A09q90qw90lq917835lq9",
                      name="search_knowledge_base",
                      input={"query": "Acme Dashboard pricing plans"},
                  ),
              ],
          ),
          MessageParam(
              role="user",
              content=[
                  ToolResultBlockParam(
                      type="tool_result",
                      tool_use_id="toolu_01A09q90qw90lq917835lq9",
                      content=[
                          SearchResultBlockParam(
                              type="search_result",
                              source="https://docs.company.com/pricing",
                              title="Pricing Plans",
                              content=[
                                  TextBlockParam(
                                      type="text",
                                      text="Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.",
                                  )
                              ],
                              citations={"enabled": True},
                          )
                      ],
                  )
              ],
          ),
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const knowledgeBaseTool: Anthropic.Tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object" as const,
      properties: {
        query: { type: "string", description: "The search query" }
      },
      required: ["query"]
    }
  };

  // Replay a conversation that provides search results both ways: the first
  // user message carries a pre-fetched result, the tool result returns another
  const response = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [knowledgeBaseTool],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result" as const,
            source: "https://docs.company.com/overview",
            title: "Product Overview",
            content: [
              {
                type: "text" as const,
                text: "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text" as const,
            text: "What does Acme Dashboard do, and what plans is it available on?"
          }
        ]
      },
      {
        role: "assistant",
        content: [
          { type: "text" as const, text: "Let me check the pricing information." },
          {
            type: "tool_use" as const,
            id: "toolu_01A09q90qw90lq917835lq9",
            name: "search_knowledge_base",
            input: { query: "Acme Dashboard pricing plans" }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result" as const,
            tool_use_id: "toolu_01A09q90qw90lq917835lq9",
            content: [
              {
                type: "search_result" as const,
                source: "https://docs.company.com/pricing",
                title: "Pricing Plans",
                content: [
                  {
                    type: "text" as const,
                    text: "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."
                  }
                ],
                citations: { enabled: true }
              }
            ]
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  AnthropicClient client = new();

  // Replay a conversation that provides search results both ways: the first
  // user message carries a pre-fetched result, the tool result returns another
  var response = await client.Messages.Create(new()
  {
      Model = Model.ClaudeOpus5,
      MaxTokens = 1024,
      Tools =
      [
          new ToolUnion(new Tool()
          {
              Name = "search_knowledge_base",
              Description = "Search the company knowledge base for information",
              InputSchema = new InputSchema()
              {
                  Properties = new Dictionary<string, JsonElement>
                  {
                      ["query"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The search query" }),
                  },
                  Required = ["query"],
              },
          }),
      ],
      Messages =
      [
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new SearchResultBlockParam
                  {
                      Source = "https://docs.company.com/overview",
                      Title = "Product Overview",
                      Content = [new() { Text = "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards." }],
                      Citations = new() { Enabled = true },
                  }),
                  new ContentBlockParam(new TextBlockParam { Text = "What does Acme Dashboard do, and what plans is it available on?" }),
              ]),
          },
          new()
          {
              Role = Role.Assistant,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new TextBlockParam { Text = "Let me check the pricing information." }),
                  new ContentBlockParam(new ToolUseBlockParam
                  {
                      ID = "toolu_01A09q90qw90lq917835lq9",
                      Name = "search_knowledge_base",
                      Input = new Dictionary<string, JsonElement>
                      {
                          ["query"] = JsonSerializer.SerializeToElement("Acme Dashboard pricing plans"),
                      },
                  }),
              ]),
          },
          new()
          {
              Role = Role.User,
              Content = new MessageParamContent(
              [
                  new ContentBlockParam(new ToolResultBlockParam()
                  {
                      ToolUseID = "toolu_01A09q90qw90lq917835lq9",
                      Content = new ToolResultBlockParamContent(
                      [
                          new SearchResultBlockParam
                          {
                              Source = "https://docs.company.com/pricing",
                              Title = "Pricing Plans",
                              Content = [new() { Text = "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing." }],
                              Citations = new() { Enabled = true },
                          },
                      ]),
                  }),
              ]),
          },
      ],
  });

  Console.WriteLine(response);
  ```

  ```go Go
  client := anthropic.NewClient()

  knowledgeBaseTool := anthropic.ToolUnionParam{
  	OfTool: &anthropic.ToolParam{
  		Name:        "search_knowledge_base",
  		Description: anthropic.String("Search the company knowledge base for information"),
  		InputSchema: anthropic.ToolInputSchemaParam{
  			Properties: map[string]any{
  				"query": map[string]any{"type": "string", "description": "The search query"},
  			},
  			Required: []string{"query"},
  		},
  	},
  }

  // Replay a conversation that provides search results both ways: the first
  // user message carries a pre-fetched result, the tool result returns another
  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus5,
  	MaxTokens: 1024,
  	Tools:     []anthropic.ToolUnionParam{knowledgeBaseTool},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{OfSearchResult: &anthropic.SearchResultBlockParam{
  				Content: []anthropic.TextBlockParam{
  					{Text: "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."},
  				},
  				Source:    "https://docs.company.com/overview",
  				Title:     "Product Overview",
  				Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  			}},
  			anthropic.NewTextBlock("What does Acme Dashboard do, and what plans is it available on?"),
  		),
  		anthropic.NewAssistantMessage(
  			anthropic.NewTextBlock("Let me check the pricing information."),
  			anthropic.ContentBlockParamUnion{OfToolUse: &anthropic.ToolUseBlockParam{
  				ID:    "toolu_01A09q90qw90lq917835lq9",
  				Name:  "search_knowledge_base",
  				Input: map[string]any{"query": "Acme Dashboard pricing plans"},
  			}},
  		),
  		anthropic.NewUserMessage(
  			anthropic.ContentBlockParamUnion{OfToolResult: &anthropic.ToolResultBlockParam{
  				ToolUseID: "toolu_01A09q90qw90lq917835lq9",
  				Content: []anthropic.ToolResultBlockParamContentUnion{
  					{OfSearchResult: &anthropic.SearchResultBlockParam{
  						Content: []anthropic.TextBlockParam{
  							{Text: "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."},
  						},
  						Source:    "https://docs.company.com/pricing",
  						Title:     "Pricing Plans",
  						Citations: anthropic.CitationsConfigParam{Enabled: anthropic.Bool(true)},
  					}},
  				},
  			}},
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.messages.CitationsConfigParam;
  import com.anthropic.models.messages.ContentBlockParam;
  // ...
  import com.anthropic.models.messages.SearchResultBlockParam;
  import com.anthropic.models.messages.TextBlockParam;
  import com.anthropic.models.messages.Tool;
  import com.anthropic.models.messages.ToolResultBlockParam;
  import com.anthropic.models.messages.ToolUseBlockParam;
  // ...

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      Tool knowledgeBaseTool = Tool.builder()
          .name("search_knowledge_base")
          .description("Search the company knowledge base for information")
          .inputSchema(Tool.InputSchema.builder()
              .properties(JsonValue.from(Map.of(
                  "query", Map.of("type", "string", "description", "The search query")
              )))
              .putAdditionalProperty("required", JsonValue.from(List.of("query")))
              .build())
          .build();

      // Replay a conversation that provides search results both ways: the first
      // user message carries a pre-fetched result, the tool result returns another
      MessageCreateParams params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_5)
          .maxTokens(1024L)
          .addTool(knowledgeBaseTool)
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofSearchResult(SearchResultBlockParam.builder()
                  .source("https://docs.company.com/overview")
                  .title("Product Overview")
                  .content(List.of(TextBlockParam.builder()
                      .text("Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.")
                      .build()))
                  .citations(CitationsConfigParam.builder().enabled(true).build())
                  .build()),
              ContentBlockParam.ofText(TextBlockParam.builder()
                  .text("What does Acme Dashboard do, and what plans is it available on?")
                  .build())
          ))
          .addAssistantMessageOfBlockParams(List.of(
              ContentBlockParam.ofText(TextBlockParam.builder()
                  .text("Let me check the pricing information.")
                  .build()),
              ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                  .id("toolu_01A09q90qw90lq917835lq9")
                  .name("search_knowledge_base")
                  .input(JsonValue.from(Map.of("query", "Acme Dashboard pricing plans")))
                  .build())
          ))
          .addUserMessageOfBlockParams(List.of(
              ContentBlockParam.ofToolResult(ToolResultBlockParam.builder()
                  .toolUseId("toolu_01A09q90qw90lq917835lq9")
                  .contentOfBlocks(List.of(
                      ToolResultBlockParam.Content.Block.ofSearchResult(SearchResultBlockParam.builder()
                          .source("https://docs.company.com/pricing")
                          .title("Pricing Plans")
                          .content(List.of(TextBlockParam.builder()
                              .text("Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.")
                              .build()))
                          .citations(CitationsConfigParam.builder().enabled(true).build())
                          .build())
                  ))
                  .build())
          ))
          .build();

      Message response = client.messages().create(params);
      System.out.println(response);
  }
  ```

  ```php PHP
  $client = new Client();

  $knowledgeBaseTool = [
      'name' => 'search_knowledge_base',
      'description' => 'Search the company knowledge base for information',
      'input_schema' => [
          'type' => 'object',
          'properties' => [
              'query' => ['type' => 'string', 'description' => 'The search query']
          ],
          'required' => ['query']
      ]
  ];

  // Replay a conversation that provides search results both ways: the first
  // user message carries a pre-fetched result, the tool result returns another
  $response = $client->messages->create(
      maxTokens: 1024,
      tools: [$knowledgeBaseTool],
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'search_result',
                      'source' => 'https://docs.company.com/overview',
                      'title' => 'Product Overview',
                      'content' => [
                          [
                              'type' => 'text',
                              'text' => 'Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.'
                          ]
                      ],
                      'citations' => ['enabled' => true]
                  ],
                  [
                      'type' => 'text',
                      'text' => 'What does Acme Dashboard do, and what plans is it available on?'
                  ]
              ]
          ],
          [
              'role' => 'assistant',
              'content' => [
                  ['type' => 'text', 'text' => 'Let me check the pricing information.'],
                  [
                      'type' => 'tool_use',
                      'id' => 'toolu_01A09q90qw90lq917835lq9',
                      'name' => 'search_knowledge_base',
                      'input' => ['query' => 'Acme Dashboard pricing plans']
                  ]
              ]
          ],
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'tool_result',
                      'tool_use_id' => 'toolu_01A09q90qw90lq917835lq9',
                      'content' => [
                          [
                              'type' => 'search_result',
                              'source' => 'https://docs.company.com/pricing',
                              'title' => 'Pricing Plans',
                              'content' => [
                                  [
                                      'type' => 'text',
                                      'text' => 'Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.'
                                  ]
                              ],
                              'citations' => ['enabled' => true]
                          ]
                      ]
                  ]
              ]
          ]
      ],
      model: 'claude-opus-5',
  );

  echo json_encode($response, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  knowledge_base_tool = {
    name: "search_knowledge_base",
    description: "Search the company knowledge base for information",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "The search query" }
      },
      required: ["query"]
    }
  }

  # Replay a conversation that provides search results both ways: the first
  # user message carries a pre-fetched result, the tool result returns another
  response = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 1024,
    tools: [knowledge_base_tool],
    messages: [
      {
        role: "user",
        content: [
          {
            type: "search_result",
            source: "https://docs.company.com/overview",
            title: "Product Overview",
            content: [
              {
                type: "text",
                text: "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards."
              }
            ],
            citations: { enabled: true }
          },
          {
            type: "text",
            text: "What does Acme Dashboard do, and what plans is it available on?"
          }
        ]
      },
      {
        role: "assistant",
        content: [
          { type: "text", text: "Let me check the pricing information." },
          {
            type: "tool_use",
            id: "toolu_01A09q90qw90lq917835lq9",
            name: "search_knowledge_base",
            input: { query: "Acme Dashboard pricing plans" }
          }
        ]
      },
      {
        role: "user",
        content: [
          {
            type: "tool_result",
            tool_use_id: "toolu_01A09q90qw90lq917835lq9",
            content: [
              {
                type: "search_result",
                source: "https://docs.company.com/pricing",
                title: "Pricing Plans",
                content: [
                  {
                    type: "text",
                    text: "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing."
                  }
                ],
                citations: { enabled: true }
              }
            ]
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

The response cites both sources. The pre-fetched result is `search_result_index: 0` and the tool-returned result is `search_result_index: 1`, matching the order the `search_result` blocks appear in the conversation:

```json
{
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Here's what I found about Acme Dashboard:\n\n**What it does:** "
    },
    {
      "type": "text",
      "text": "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "Acme Dashboard is a monitoring tool for distributed systems. It supports real-time alerting and custom metric dashboards.",
          "source": "https://docs.company.com/overview",
          "title": "Product Overview",
          "search_result_index": 0,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    },
    {
      "type": "text",
      "text": "\n\n**Available plans:** "
    },
    {
      "type": "text",
      "text": "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.",
      "citations": [
        {
          "type": "search_result_location",
          "cited_text": "Acme Dashboard is available on the Starter plan at $10 per user per month and the Enterprise plan with custom pricing.",
          "source": "https://docs.company.com/pricing",
          "title": "Pricing Plans",
          "search_result_index": 1,
          "start_block_index": 0,
          "end_block_index": 1
        }
      ]
    }
  ]
}
```

### Mixing with other content types

In user messages, `search_result` blocks can sit alongside any other content block. The Method 2 example pairs search results with a `text` question, and image or document blocks can join them the same way.

Tool results are stricter: if any block in a `tool_result` content array is a `search_result`, all of its blocks must be `search_result`. Mixing search results with other block types in the same tool result returns a validation error. To return supporting text alongside tool-sourced search results, include it as a text block inside one of the search results' `content` arrays, where it also becomes citable.

### Cache control

Add `cache_control` on the search result block to cache it for reuse across requests. It sits alongside `citations` on the same block:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "..." }],
  "citations": { "enabled": true },
  "cache_control": { "type": "ephemeral" }
}
```

See [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) for minimum cacheable lengths and other requirements.

### Citation control

By default, citations are disabled for search results. You can enable citations by explicitly setting the `citations` configuration:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "Important documentation..." }],
  "citations": {
    "enabled": true // Enable citations for this result
  }
}
```

When `citations.enabled` is set to `true`, Claude attaches citation references to the text blocks that draw on the search result.

<Warning>
  Citations are all-or-nothing: either all search results in a request must have citations enabled, or all must have them disabled. Mixing search results with different citation settings results in an error.
</Warning>

## Best practices

### For tool-based search (Method 1)

* **Dynamic content:** Use for real-time searches and dynamic RAG applications
* **Error handling:** Return appropriate messages when searches fail
* **Result limits:** Return only the most relevant results to avoid context overflow

### For top-level search (Method 2)

* **Pre-fetched content:** Use when you already have search results
* **Batch processing:** Ideal for processing multiple search results at once
* **Testing:** Great for testing citation behavior with known content

### General best practices

1. **Structure results effectively:**

   * Use clear, permanent source URLs
   * Provide descriptive titles
   * Break long content into logical text blocks to give Claude finer citation boundaries

2. **Maintain consistency:**

   * Use consistent source formats across your application
   * Ensure titles accurately reflect content
   * Keep formatting consistent

3. **Handle errors gracefully:** when a search fails or returns nothing, return a plain text block describing the outcome (for example, `{"type": "text", "text": "No results found."}`) instead of raising an error: Claude explains the empty result to the user, and the conversation continues.

## Limitations

* Search result content blocks are available on Claude API, Amazon Bedrock, and Google Cloud.
* Only text content is supported within search results (no images or other media).
* `search_result` blocks can only appear in user messages (including inside tool results). Assistant messages with search results are rejected.
* When the [web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool) is enabled in the same request, citations must be enabled on all `search_result` blocks.

## Next steps

<CardGroup cols={2}>
  <Card title="Streaming refusals" icon="lock" href="https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals">
    Detect and handle refusal stop reasons in streaming responses, and retry refused requests on a fallback model.
  </Card>

  <Card title="Citations" icon="book" href="https://platform.claude.com/docs/en/build-with-claude/citations">
    Ground Claude's responses in your source documents. Citations return the exact passages that support each claim, so you can verify answers and surface sources to your users.
  </Card>

  <Card title="Web search tool" icon="magnifying-glass" href="https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool">
    Give Claude access to current web content with cited sources, optional dynamic filtering, and domain controls.
  </Card>

  <Card title="Messages API reference" icon="code" href="https://platform.claude.com/docs/en/api/messages/create">
    See the complete Messages API documentation, including content block types.
  </Card>

  <Card title="Prompt caching" icon="database" href="https://platform.claude.com/docs/en/build-with-claude/prompt-caching">
    Cache search results with `cache_control` to reduce cost and latency on repeated requests.
  </Card>
</CardGroup>
