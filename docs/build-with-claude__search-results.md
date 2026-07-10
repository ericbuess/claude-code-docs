# Search results

Enable natural citations for RAG applications by providing search results with source attribution

---

<Note>
  This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

Search result content blocks enable natural citations with proper source attribution, bringing web search-quality citations to your custom applications. This feature is particularly powerful for RAG (Retrieval-Augmented Generation) applications where you need Claude to cite sources accurately.

The search results feature is available on the following models:

* Claude Opus 4.8 (claude-opus-4-8)
* Claude Opus 4.7 (`claude-opus-4-7`)
* Claude Opus 4.6 (`claude-opus-4-6`)
* Claude Sonnet 5 (`claude-sonnet-5`)
* Claude Sonnet 4.6 (`claude-sonnet-4-6`)
* Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`)
* Claude Opus 4.5 (`claude-opus-4-5-20251101`)
* Claude Opus 4.1 ([deprecated](/docs/en/about-claude/model-deprecations)) (`claude-opus-4-1-20250805`)
* Claude Opus 4 ([retired, except on Google Cloud](/docs/en/about-claude/model-deprecations)) (`claude-opus-4-20250514`)
* Claude Sonnet 4 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) (`claude-sonnet-4-20250514`)
* Claude Haiku 4.5 (`claude-haiku-4-5-20251001`)
* Claude Haiku 3.5 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) (`claude-3-5-haiku-20241022`)

## Key benefits

* **Natural citations:** Achieve the same citation quality as web search for any content
* **Flexible integration:** Use in tool returns for dynamic RAG or as top-level content for pre-fetched data
* **Proper source attribution:** Each result includes source and title information for clear attribution
* **No document workarounds needed:** Eliminates the need for document-based workarounds
* **Consistent citation format:** Matches the citation quality and format of Claude's web search functionality

## How it works

Search results can be provided in two ways:

1. **From tool calls:** Your custom tools return search results, enabling dynamic RAG applications
2. **As top-level content:** You provide search results directly in user messages for pre-fetched or cached content

In both cases, Claude can automatically cite information from the search results with proper source attribution.

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

| Field     | Type   | Description                                           |
| --------- | ------ | ----------------------------------------------------- |
| `type`    | string | Must be `"search_result"`                             |
| `source`  | string | The source URL or identifier for the content          |
| `title`   | string | A descriptive title for the search result             |
| `content` | array  | An array of text blocks containing the actual content |

### Optional fields

| Field           | Type   | Description                                            |
| --------------- | ------ | ------------------------------------------------------ |
| `citations`     | object | Citation configuration with `enabled` boolean field    |
| `cache_control` | object | Cache control settings (e.g., `{"type": "ephemeral"}`) |

Each item in the `content` array must be a text block with:

* `type`: Must be `"text"`
* `text`: The actual text content (non-empty string)

## Method 1: Search results from tool calls

The most powerful use case is returning search results from your custom tools. This enables dynamic RAG applications where tools fetch and return relevant content with automatic citations.

### Example: Knowledge base tool

<CodeGroup>
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


  # Create a message with the tool
  response = client.messages.create(
      model="claude-opus-4-8",  # Works with all supported models
      max_tokens=1024,
      tools=[knowledge_base_tool],
      messages=[
          MessageParam(role="user", content="How do I configure the timeout settings?")
      ],
  )

  # When Claude calls the tool, provide the search results
  if response.content[0].type == "tool_use":
      tool_result = search_knowledge_base(response.content[0].input["query"])

      # Send the tool result back
      final_response = client.messages.create(
          model="claude-opus-4-8",  # Works with all supported models
          max_tokens=1024,
          messages=[
              MessageParam(
                  role="user", content="How do I configure the timeout settings?"
              ),
              MessageParam(role="assistant", content=response.content),
              MessageParam(
                  role="user",
                  content=[
                      ToolResultBlockParam(
                          type="tool_result",
                          tool_use_id=response.content[0].id,
                          content=tool_result,  # Search results go here
                      )
                  ],
              ),
          ],
      )
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  // Define a knowledge base search tool
  const knowledgeBaseTool: Anthropic.Messages.Tool = {
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

  // Create a message with the tool
  const response = await anthropic.messages.create({
    model: "claude-opus-4-8", // Works with all supported models
    max_tokens: 1024,
    tools: [knowledgeBaseTool],
    messages: [
      {
        role: "user",
        content: "How do I configure the timeout settings?"
      }
    ]
  });

  // Handle tool use and provide results
  if (response.content[0].type === "tool_use") {
    const input = response.content[0].input as { query: string };
    const toolResult = searchKnowledgeBase(input.query);

    const finalResponse = await anthropic.messages.create({
      model: "claude-opus-4-8", // Works with all supported models
      max_tokens: 1024,
      messages: [
        { role: "user", content: "How do I configure the timeout settings?" },
        { role: "assistant", content: response.content },
        {
          role: "user",
          content: [
            {
              type: "tool_result" as const,
              tool_use_id: response.content[0].id,
              content: toolResult // Search results go here
            }
          ]
        }
      ]
    });
  }
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  public class Program
  {
      public static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var knowledgeBaseTool = new Tool
          {
              Name = "search_knowledge_base",
              Description = "Search the company knowledge base for information",
              InputSchema = new
              {
                  type = "object",
                  properties = new
                  {
                      query = new
                      {
                          type = "string",
                          description = "The search query"
                      }
                  },
                  required = new[] { "query" }
              }
          };

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Tools = new[] { knowledgeBaseTool },
              Messages = new[]
              {
                  new MessageParam
                  {
                      Role = Role.User,
                      Content = "How do I configure the timeout settings?"
                  }
              }
          };

          var response = await client.Messages.Create(parameters);

          if (response.Content[0] is ToolUseBlock toolUse)
          {
              var toolResult = SearchKnowledgeBase(toolUse.Input["query"].ToString());

              var finalParameters = new MessageCreateParams
              {
                  Model = Model.ClaudeOpus4_8,
                  MaxTokens = 1024,
                  Messages = new[]
                  {
                      new MessageParam { Role = Role.User, Content = "How do I configure the timeout settings?" },
                      new MessageParam { Role = Role.Assistant, Content = response.Content },
                      new MessageParam
                      {
                          Role = Role.User,
                          Content = new[]
                          {
                              new ToolResultBlockParam
                              {
                                  ToolUseID = toolUse.Id,
                                  Content = toolResult
                              }
                          }
                      }
                  }
              };

              var finalResponse = await client.Messages.Create(finalParameters);
              Console.WriteLine(finalResponse);
          }
      }

      private static List<SearchResultBlockParam> SearchKnowledgeBase(string query)
      {
          return new List<SearchResultBlockParam>
          {
              new SearchResultBlockParam
              {
                  Source = "https://docs.company.com/product-guide",
                  Title = "Product Configuration Guide",
                  Content = new[]
                  {
                      new TextBlockParam
                      {
                          Text = "To configure the product, navigate to Settings > Configuration. The default timeout is 30 seconds, but can be adjusted between 10-120 seconds based on your needs."
                      }
                  },
                  Citations = new CitationsConfigParam { Enabled = true }
              },
              new SearchResultBlockParam
              {
                  Source = "https://docs.company.com/troubleshooting",
                  Title = "Troubleshooting Guide",
                  Content = new[]
                  {
                      new TextBlockParam
                      {
                          Text = "If you encounter timeout errors, first check the configuration settings. Common causes include network latency and incorrect timeout values."
                      }
                  },
                  Citations = new CitationsConfigParam { Enabled = true }
              }
          };
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

  	response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Tools:     []anthropic.ToolUnionParam{knowledgeBaseTool},
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("How do I configure the timeout settings?")),
  		},
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for _, block := range response.Content {
  		switch variant := block.AsAny().(type) {
  		case anthropic.ToolUseBlock:
  			var input struct {
  				Query string `json:"query"`
  			}
  			if err := json.Unmarshal(variant.Input, &input); err != nil {
  				log.Fatal(err)
  			}
  			toolResults := searchKnowledgeBase(input.Query)

  			// Build assistant message from the response
  			assistantParam := response.ToParam()

  			finalResponse, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  				Model:     anthropic.ModelClaudeOpus4_8,
  				MaxTokens: 1024,
  				Messages: []anthropic.MessageParam{
  					anthropic.NewUserMessage(anthropic.NewTextBlock("How do I configure the timeout settings?")),
  					assistantParam,
  					anthropic.NewUserMessage(anthropic.ContentBlockParamUnion{
  						OfToolResult: &anthropic.ToolResultBlockParam{
  							ToolUseID: variant.ID,
  							Content:   toolResults,
  						},
  					}),
  				},
  			})
  			if err != nil {
  				log.Fatal(err)
  			}
  			fmt.Println(finalResponse)
  		}
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
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.SearchResultBlockParam;
  // ...
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

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .addTool(knowledgeBaseTool)
              .addUserMessage("How do I configure the timeout settings?")
              .build();

          Message response = client.messages().create(params);

          response.content().get(0).toolUse().ifPresent(toolUse -> {
              List<ContentBlockParam> toolResult = searchKnowledgeBase(
                  (String) ((Map<?, ?>) toolUse._input()).get("query")
              );

              MessageCreateParams finalParams = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_8)
                  .maxTokens(1024L)
                  .addUserMessage("How do I configure the timeout settings?")
                  .addAssistantMessageOfBlockParams(List.of(
                      ContentBlockParam.ofToolUse(ToolUseBlockParam.builder()
                          .id(toolUse.id())
                          .name(toolUse.name())
                          .input(toolUse._input())
                          .build())
                  ))
                  .addUserMessageOfBlockParams(List.of(
                      ContentBlockParam.ofToolResult(
                          ToolResultBlockParam.builder()
                              .toolUseId(toolUse.id())
                              .contentOfBlockParams(toolResult)
                              .build()
                      )
                  ))
                  .build();

              Message finalResponse = client.messages().create(finalParams);
              System.out.println(finalResponse);
          });
      }
  // ...
          return List.of(
              ContentBlockParam.ofSearchResult(
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
              ContentBlockParam.ofSearchResult(
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

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'How do I configure the timeout settings?']
      ],
      model: 'claude-opus-4-8',
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

      $finalResponse = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'How do I configure the timeout settings?'],
              ['role' => 'assistant', 'content' => $response->content],
              [
                  'role' => 'user',
                  'content' => [
                      [
                          'type' => 'tool_result',
                          'tool_use_id' => $toolUseBlock->id,
                          'content' => $toolResult
                      ]
                  ]
              ]
          ],
          model: 'claude-opus-4-8',
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

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    tools: [knowledge_base_tool],
    messages: [
      { role: "user", content: "How do I configure the timeout settings?" }
    ]
  )

  if response.content.first.type == :tool_use
    tool_result = search_knowledge_base(response.content.first.input["query"])

    final_response = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        { role: "user", content: "How do I configure the timeout settings?" },
        { role: "assistant", content: response.content },
        {
          role: "user",
          content: [
            {
              type: "tool_result",
              tool_use_id: response.content.first.id,
              content: tool_result
            }
          ]
        }
      ]
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
  #!/bin/sh
  curl https://api.anthropic.com/v1/messages \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data \
  '{
      "model": "claude-opus-4-8",
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
  model: claude-opus-4-8
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
      model="claude-opus-4-8",
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
  const anthropic = new Anthropic();

  // Provide search results directly in the user message
  const response = await anthropic.messages.create({
    model: "claude-opus-4-8",
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
  using System;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var parameters = new MessageCreateParams
          {
              Model = Model.ClaudeOpus4_8,
              MaxTokens = 1024,
              Messages =
              [
                  new()
                  {
                      Role = Role.User,
                      Content =
                      [
                          new SearchResultBlockParam
                          {
                              Source = "https://docs.company.com/api-reference",
                              Title = "API Reference - Authentication",
                              Content =
                              [
                                  new TextBlockParam
                                  {
                                      Text = "All API requests must include an API key in the Authorization header. Keys can be generated from the dashboard. Rate limits: 1000 requests per hour for standard tier, 10000 for premium."
                                  }
                              ],
                              Citations = new CitationsConfigParam { Enabled = true }
                          },
                          new SearchResultBlockParam
                          {
                              Source = "https://docs.company.com/quickstart",
                              Title = "Getting Started Guide",
                              Content =
                              [
                                  new TextBlockParam
                                  {
                                      Text = "To get started: 1) Sign up for an account, 2) Generate an API key from the dashboard, 3) Install our SDK using pip install company-sdk, 4) Initialize the client with your API key."
                                  }
                              ],
                              Citations = new CitationsConfigParam { Enabled = true }
                          },
                          new TextBlockParam
                          {
                              Text = "Based on these search results, how do I authenticate API requests and what are the rate limits?"
                          }
                      ]
                  }
              ]
          };

          var message = await client.Messages.Create(parameters);
          Console.WriteLine(message);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
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
  import com.anthropic.models.messages.CitationsConfigParam;
  // ...
  import com.anthropic.models.messages.SearchResultBlockParam;
  // ...
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
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
      model: 'claude-opus-4-8',
  );

  echo json_encode($message, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
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

The block indices identify a slice of the search result's `content` array, and `cited_text` is the full text of that slice. The text block is the minimal citable unit: Claude cites whole blocks, not substrings within a block. To get finer-grained citations, split your search result content into smaller blocks (see [Multiple content blocks](#multiple-content-blocks)).

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
  ]
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

When this search result is cited, `start_block_index` and `end_block_index` identify which of these blocks the citation covers, and `cited_text` contains exactly those blocks' text. Splitting content into smaller, focused blocks gives Claude finer citation boundaries; combining content into one block means every citation returns the full text. This is the same model used by [custom content documents](/docs/en/build-with-claude/citations#custom-content-documents) in the Citations feature.

## Advanced usage

### Combining both methods

You can use both tool-based and top-level search results in the same conversation:

```python
from anthropic.types import MessageParam, SearchResultBlockParam, TextBlockParam

# First message with top-level search results
messages = [
    MessageParam(
        role="user",
        content=[
            SearchResultBlockParam(
                type="search_result",
                source="https://docs.company.com/overview",
                title="Product Overview",
                content=[
                    TextBlockParam(
                        type="text", text="Our product helps teams collaborate..."
                    )
                ],
                citations={"enabled": True},
            ),
            TextBlockParam(
                type="text",
                text="Tell me about this product and search for pricing information",
            ),
        ],
    )
]

# Claude might respond and call a tool to search for pricing
# Then you provide tool results with more search results
```

### Combining with other content types

Both methods support mixing search results with other content:

```python
from anthropic.types import SearchResultBlockParam, TextBlockParam

# In tool results
tool_result = [
    SearchResultBlockParam(
        type="search_result",
        source="https://docs.company.com/guide",
        title="User Guide",
        content=[TextBlockParam(type="text", text="Configuration details...")],
        citations={"enabled": True},
    ),
    TextBlockParam(
        type="text", text="Additional context: This applies to version 2.0 and later."
    ),
]

# In top-level content
user_content = [
    SearchResultBlockParam(
        type="search_result",
        source="https://research.com/paper",
        title="Research Paper",
        content=[TextBlockParam(type="text", text="Key findings...")],
        citations={"enabled": True},
    ),
    {
        "type": "image",
        "source": {"type": "url", "url": "https://example.com/chart.png"},
    },
    TextBlockParam(
        type="text", text="How does the chart relate to the research findings?"
    ),
]
```

### Cache control

Add cache control for better performance:

```json
{
  "type": "search_result",
  "source": "https://docs.company.com/guide",
  "title": "User Guide",
  "content": [{ "type": "text", "text": "..." }],
  "cache_control": {
    "type": "ephemeral"
  }
}
```

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

When `citations.enabled` is set to `true`, Claude includes citation references when using information from the search result. This enables:

* Natural citations for your custom RAG applications
* Source attribution when interfacing with proprietary knowledge bases
* Web search-quality citations for any custom tool that returns search results

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

3. **Handle errors gracefully:**

   ```python
   def search_with_fallback(query):
       try:
           results = perform_search(query)
           if not results:
               return {"type": "text", "text": "No results found."}
           return format_as_search_results(results)
       except Exception as e:
           return {"type": "text", "text": f"Search error: {str(e)}"}
   ```

## Limitations

* Search result content blocks are available on Claude API, Amazon Bedrock, and Google Cloud
* Only text content is supported within search results (no images or other media)
* The `content` array must contain at least one text block

## Next steps

<CardGroup cols={2}>
  <Card title="Citations" icon="book" href="/docs/en/build-with-claude/citations">
    Learn how citations work across documents, custom content, and search results.
  </Card>

  <Card title="Web search tool" icon="magnifying-glass" href="/docs/en/agents-and-tools/tool-use/web-search-tool">
    Let Claude search the web and cite sources automatically using a server tool.
  </Card>

  <Card title="Messages API reference" icon="code" href="/docs/en/api/messages/create">
    See the complete Messages API documentation, including content block types.
  </Card>

  <Card title="Prompt caching" icon="database" href="/docs/en/build-with-claude/prompt-caching">
    Cache search results with `cache_control` to reduce cost and latency on repeated requests.
  </Card>
</CardGroup>
