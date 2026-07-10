# Token counting

Count the tokens in a message before you send it to Claude. Use token counts to manage rate limits and costs, make model routing decisions, and fit prompts to a target length.

---

Token counting lets you determine the number of tokens in a message before you send it to Claude. This helps you make informed decisions about your prompts and usage. With token counting, you can:

* Proactively manage rate limits and costs
* Make smart model routing decisions
* Optimize prompts to a specific length

<Note>
  This feature is eligible for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.
</Note>

***

## How to count message tokens

The [token counting](/docs/en/api/messages-count-tokens) endpoint accepts the same structured list of inputs for creating a message, including support for system prompts, [tools](/docs/en/agents-and-tools/tool-use/overview), [images](/docs/en/build-with-claude/vision), and [PDFs](/docs/en/build-with-claude/pdf-support). The response contains the total number of input tokens.

<Note>
  The token count should be considered an **estimate**. In some cases, the actual number of input tokens used when creating a message may differ by a small amount.

  Token counts may include tokens added automatically by Anthropic for system optimizations. **You are not billed for system-added tokens**. Billing reflects only your content.
</Note>

### Supported models

All [active models](/docs/en/about-claude/models/overview) support token counting, including Claude Sonnet 5.

<Note>
  Claude Opus 4.7 and later Opus models, Claude Fable 5, Claude Mythos 5, Claude Mythos Preview, and Claude Sonnet 5 use a newer tokenizer. The same input text produces approximately 30% more tokens than on earlier models. The exact increase depends on the content and workload shape. Recount prompts against the model you plan to use rather than reusing counts measured against earlier models.
</Note>

### Count tokens in basic messages

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/count_tokens \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "content-type: application/json" \
      --header "anthropic-version: 2023-06-01" \
      --data '{
        "model": "claude-opus-4-8",
        "system": "You are a scientist",
        "messages": [{
          "role": "user",
          "content": "Hello, Claude"
        }]
      }'
  ```

  ```bash CLI
  ant messages count-tokens \
    --model claude-opus-4-8 \
    --system "You are a scientist" \
    --message '{role: user, content: "Hello, Claude"}'
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.count_tokens(
      model="claude-opus-4-8",
      system="You are a scientist",
      messages=[{"role": "user", "content": "Hello, Claude"}],
  )

  print(response.json())
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.countTokens({
    model: "claude-opus-4-8",
    system: "You are a scientist",
    messages: [
      {
        role: "user",
        content: "Hello, Claude"
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

          var parameters = new MessageCountTokensParams
          {
              Model = Model.ClaudeOpus4_8,
              System = "You are a scientist",
              Messages = [new() { Role = Role.User, Content = "Hello, Claude" }]
          };

          var response = await client.Messages.CountTokens(parameters);
          Console.WriteLine(response);
      }
  }
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
  	Model: anthropic.ModelClaudeOpus4_8,
  	System: anthropic.MessageCountTokensParamsSystemUnion{
  		OfString: anthropic.String("You are a scientist"),
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.MessageCountTokensParams;
  import com.anthropic.models.messages.MessageTokensCount;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      MessageCountTokensParams params = MessageCountTokensParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .system("You are a scientist")
        .addUserMessage("Hello, Claude")
        .build();

      MessageTokensCount count = client.messages().countTokens(params);
      System.out.println(count);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->countTokens(
      messages: [
          ['role' => 'user', 'content' => 'Hello, Claude']
      ],
      model: 'claude-opus-4-8',
      system: 'You are a scientist',
  );

  echo json_encode($response);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.count_tokens(
    model: "claude-opus-4-8",
    system: "You are a scientist",
    messages: [
      { role: "user", content: "Hello, Claude" }
    ]
  )

  puts response
  ```
</CodeGroup>

```json Output
{ "input_tokens": 14 }
```

### Count tokens in messages with tools

<Note>
  [Server tool](/docs/en/agents-and-tools/tool-use/server-tools) token counts only apply to the first sampling call.
</Note>

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/count_tokens \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "content-type: application/json" \
      --header "anthropic-version: 2023-06-01" \
      --data '{
        "model": "claude-opus-4-8",
        "tools": [
          {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "The city and state, e.g. San Francisco, CA"
                }
              },
              "required": ["location"]
            }
          }
        ],
        "messages": [
          {
            "role": "user",
            "content": "What'\''s the weather like in San Francisco?"
          }
        ]
      }'
  ```

  ```bash CLI
  ant messages count-tokens <<'YAML'
  model: claude-opus-4-8
  tools:
    - name: get_weather
      description: Get the current weather in a given location
      input_schema:
        type: object
        properties:
          location:
            type: string
            description: The city and state, e.g. San Francisco, CA
        required:
          - location
  messages:
    - role: user
      content: What's the weather like in San Francisco?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.count_tokens(
      model="claude-opus-4-8",
      tools=[
          {
              "name": "get_weather",
              "description": "Get the current weather in a given location",
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "location": {
                          "type": "string",
                          "description": "The city and state, e.g. San Francisco, CA",
                      }
                  },
                  "required": ["location"],
              },
          }
      ],
      messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
  )

  print(response.json())
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.countTokens({
    model: "claude-opus-4-8",
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    messages: [{ role: "user", content: "What's the weather like in San Francisco?" }]
  });

  console.log(response);
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Text.Json;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          var parameters = new MessageCountTokensParams
          {
              Model = Model.ClaudeOpus4_8,
              Tools =
              [
                  new MessageCountTokensTool(new Tool()
                  {
                      Name = "get_weather",
                      Description = "Get the current weather in a given location",
                      InputSchema = new InputSchema()
                      {
                          Properties = new Dictionary<string, JsonElement>
                          {
                              ["location"] = JsonSerializer.SerializeToElement(new { type = "string", description = "The city and state, e.g. San Francisco, CA" }),
                          },
                          Required = ["location"],
                      },
                  }),
              ],
              Messages = [new() { Role = Role.User, Content = "What's the weather like in San Francisco?" }]
          };

          var count = await client.Messages.CountTokens(parameters);
          Console.WriteLine(count);
      }
  }
  ```

  ```go Go
  response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
  	Model: anthropic.ModelClaudeOpus4_8,
  	Tools: []anthropic.MessageCountTokensToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:        "get_weather",
  			Description: anthropic.String("Get the current weather in a given location"),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"location": map[string]any{
  						"type":        "string",
  						"description": "The city and state, e.g. San Francisco, CA",
  					},
  				},
  				Required: []string{"location"},
  			},
  		}},
  	},
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("What's the weather like in San Francisco?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  jsonData, _ := json.MarshalIndent(response, "", "  ")
  fmt.Println(string(jsonData))
  ```

  ```java Java
  import com.anthropic.models.messages.MessageCountTokensParams;
  import com.anthropic.models.messages.MessageTokensCount;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      InputSchema schema = InputSchema.builder()
        .properties(
          JsonValue.from(
            Map.of(
              "location",
              Map.of(
                "type",
                "string",
                "description",
                "The city and state, e.g. San Francisco, CA"
              )
            )
          )
        )
        .putAdditionalProperty("required", JsonValue.from(List.of("location")))
        .build();

      MessageCountTokensParams params = MessageCountTokensParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .addTool(
          Tool.builder()
            .name("get_weather")
            .description("Get the current weather in a given location")
            .inputSchema(schema)
            .build()
        )
        .addUserMessage("What's the weather like in San Francisco?")
        .build();

      MessageTokensCount count = client.messages().countTokens(params);
      System.out.println(count);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->countTokens(
      messages: [
          ['role' => 'user', 'content' => "What's the weather like in San Francisco?"]
      ],
      model: 'claude-opus-4-8',
      tools: [
          [
              'name' => 'get_weather',
              'description' => 'Get the current weather in a given location',
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'location' => [
                          'type' => 'string',
                          'description' => 'The city and state, e.g. San Francisco, CA'
                      ]
                  ],
                  'required' => ['location']
              ]
          ]
      ],
  );

  echo json_encode($response, JSON_PRETTY_PRINT);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.count_tokens(
    model: "claude-opus-4-8",
    tools: [
      {
        name: "get_weather",
        description: "Get the current weather in a given location",
        input_schema: {
          type: "object",
          properties: {
            location: {
              type: "string",
              description: "The city and state, e.g. San Francisco, CA"
            }
          },
          required: ["location"]
        }
      }
    ],
    messages: [
      { role: "user", content: "What's the weather like in San Francisco?" }
    ]
  )

  puts response
  ```
</CodeGroup>

```json Output
{ "input_tokens": 403 }
```

### Count tokens in messages with images

<CodeGroup>
  ```bash cURL
  #!/bin/sh

  IMAGE_URL="https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  IMAGE_MEDIA_TYPE="image/jpeg"
  IMAGE_BASE64=$(curl -s "$IMAGE_URL" | base64 | tr -d '\n')

  curl https://api.anthropic.com/v1/messages/count_tokens \
       --header "x-api-key: $ANTHROPIC_API_KEY" \
       --header "anthropic-version: 2023-06-01" \
       --header "content-type: application/json" \
       --data @- <<EOF
  {
      "model": "claude-opus-4-8",
      "messages": [
          {"role": "user", "content": [
              {"type": "image", "source": {
                  "type": "base64",
                  "media_type": "$IMAGE_MEDIA_TYPE",
                  "data": "$IMAGE_BASE64"
              }},
              {"type": "text", "text": "Describe this image"}
          ]}
      ]
  }
  EOF
  ```

  ```bash CLI
  IMAGE_URL="https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  curl -s "$IMAGE_URL" -o ./ant.jpg

  ant messages count-tokens <<'YAML'
  model: claude-opus-4-8
  messages:
    - role: user
      content:
        - type: image
          source:
            type: base64
            media_type: image/jpeg
            data: "@./ant.jpg"
        - type: text
          text: Describe this image
  YAML
  ```

  ```python Python
  import base64
  import httpx

  image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  image_media_type = "image/jpeg"
  image_data = base64.standard_b64encode(httpx.get(image_url).content).decode("utf-8")

  client = anthropic.Anthropic()

  response = client.messages.count_tokens(
      model="claude-opus-4-8",
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "image",
                      "source": {
                          "type": "base64",
                          "media_type": image_media_type,
                          "data": image_data,
                      },
                  },
                  {"type": "text", "text": "Describe this image"},
              ],
          }
      ],
  )
  print(response.json())
  ```

  ```typescript TypeScript
  const anthropic = new Anthropic();

  const image_url =
    "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
  const image_media_type = "image/jpeg";
  const image_array_buffer = await (await fetch(image_url)).arrayBuffer();
  const image_data = Buffer.from(image_array_buffer).toString("base64");

  const response = await anthropic.messages.countTokens({
    model: "claude-opus-4-8",
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: image_media_type,
              data: image_data
            }
          },
          {
            type: "text",
            text: "Describe this image"
          }
        ]
      }
    ]
  });
  console.log(response);
  ```

  ```csharp C#
  using System;
  using System.Collections.Generic;
  using System.Net.Http;
  using System.Threading.Tasks;
  using Anthropic;
  using Anthropic.Models.Messages;

  public class Program
  {
      public static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          string imageUrl = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";

          using HttpClient httpClient = new();
          byte[] imageBytes = await httpClient.GetByteArrayAsync(imageUrl);
          string imageData = Convert.ToBase64String(imageBytes);

          var parameters = new MessageCountTokensParams
          {
              Model = Model.ClaudeOpus4_8,
              Messages =
              [
                  new()
                  {
                      Role = Role.User,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new ImageBlockParam(
                              new ImageBlockParamSource(new Base64ImageSource()
                              {
                                  Data = imageData,
                                  MediaType = MediaType.ImageJpeg,
                              })
                          )),
                          new ContentBlockParam(new TextBlockParam("Describe this image")),
                      }),
                  }
              ]
          };

          var count = await client.Messages.CountTokens(parameters);
          Console.WriteLine(count);
      }
  }
  ```

  ```go Go
  imageURL := "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"

  req, err := http.NewRequest("GET", imageURL, nil)
  if err != nil {
  	log.Fatal(err)
  }
  req.Header.Set("User-Agent", "AnthropicDocsBot/1.0")

  resp, err := http.DefaultClient.Do(req)
  if err != nil {
  	log.Fatal(err)
  }
  defer resp.Body.Close()

  imageBytes, err := io.ReadAll(resp.Body)
  if err != nil {
  	log.Fatal(err)
  }
  imageData := base64.StdEncoding.EncodeToString(imageBytes)

  client := anthropic.NewClient()

  response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
  	Model: anthropic.ModelClaudeOpus4_8,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewImageBlockBase64("image/jpeg", imageData),
  			anthropic.NewTextBlock("Describe this image"),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.Base64ImageSource;
  // ...
  import com.anthropic.models.messages.MessageCountTokensParams;
  import com.anthropic.models.messages.MessageTokensCount;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      String imageUrl =
        "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
      String imageMediaType = "image/jpeg";

      HttpClient httpClient = HttpClient.newHttpClient();
      HttpRequest request = HttpRequest.newBuilder().uri(URI.create(imageUrl)).build();
      byte[] imageBytes = httpClient
        .send(request, HttpResponse.BodyHandlers.ofByteArray())
        .body();
      String imageBase64 = Base64.getEncoder().encodeToString(imageBytes);

      ContentBlockParam imageBlock = ContentBlockParam.ofImage(
        ImageBlockParam.builder()
          .source(
            Base64ImageSource.builder()
              .mediaType(Base64ImageSource.MediaType.IMAGE_JPEG)
              .data(imageBase64)
              .build()
          )
          .build()
      );

      ContentBlockParam textBlock = ContentBlockParam.ofText(
        TextBlockParam.builder().text("Describe this image").build()
      );

      MessageCountTokensParams params = MessageCountTokensParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .addUserMessageOfBlockParams(List.of(imageBlock, textBlock))
        .build();

      MessageTokensCount count = client.messages().countTokens(params);
      System.out.println(count);
  ```

  ```php PHP
  $imageUrl = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg";
  $imageMediaType = "image/jpeg";
  $imageData = base64_encode(file_get_contents($imageUrl));

  $client = new Client();

  $response = $client->messages->countTokens(
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'image',
                      'source' => [
                          'type' => 'base64',
                          'media_type' => $imageMediaType,
                          'data' => $imageData
                      ]
                  ],
                  ['type' => 'text', 'text' => 'Describe this image']
              ]
          ]
      ],
      model: 'claude-opus-4-8',
  );
  print_r($response);
  ```

  ```ruby Ruby
  require "base64"
  require "net/http"

  image_url = "https://upload.wikimedia.org/wikipedia/commons/a/a7/Camponotus_flavomarginatus_ant.jpg"
  image_media_type = "image/jpeg"

  uri = URI(image_url)
  image_data = Base64.strict_encode64(Net::HTTP.get(uri))

  client = Anthropic::Client.new

  response = client.messages.count_tokens(
    model: "claude-opus-4-8",
    messages: [
      {
        role: "user",
        content: [
          {
            type: "image",
            source: {
              type: "base64",
              media_type: image_media_type,
              data: image_data
            }
          },
          { type: "text", text: "Describe this image" }
        ]
      }
    ]
  )
  puts response
  ```
</CodeGroup>

```json Output
{ "input_tokens": 1551 }
```

### Count tokens in messages with extended thinking

<Note>
  See [how the context window is calculated with extended thinking](/docs/en/build-with-claude/extended-thinking#how-context-window-is-calculated-with-extended-thinking) for more details

  * Thinking blocks from **previous** assistant turns are ignored and **do not** count toward your input tokens
  * **Current** assistant turn thinking **does** count toward your input tokens
</Note>

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/count_tokens \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "content-type: application/json" \
      --header "anthropic-version: 2023-06-01" \
      --data '{
        "model": "claude-sonnet-4-6",
        "thinking": {
          "type": "enabled",
          "budget_tokens": 16000
        },
        "messages": [
          {
            "role": "user",
            "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?"
          },
          {
            "role": "assistant",
            "content": [
              {
                "type": "thinking",
                "thinking": "This is a nice number theory question. Lets think about it step by step...",
                "signature": "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
              },
              {
                "type": "text",
                "text": "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
              }
            ]
          },
          {
            "role": "user",
            "content": "Can you write a formal proof?"
          }
        ]
      }'
  ```

  ```bash CLI
  ant messages count-tokens <<'YAML'
  model: claude-sonnet-4-6
  thinking:
    type: enabled
    budget_tokens: 16000
  messages:
    - role: user
      content: Are there an infinite number of prime numbers such that n mod 4 == 3?
    - role: assistant
      content:
        - type: thinking
          thinking: >-
            This is a nice number theory question. Lets think about it step by step...
          signature: >-
            EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...
        - type: text
          text: Yes, there are infinitely many prime numbers p such that p mod 4 = 3...
    - role: user
      content: Can you write a formal proof?
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.count_tokens(
      model="claude-sonnet-4-6",
      thinking={"type": "enabled", "budget_tokens": 16000},
      messages=[
          {
              "role": "user",
              "content": "Are there an infinite number of prime numbers such that n mod 4 == 3?",
          },
          {
              "role": "assistant",
              "content": [
                  {
                      "type": "thinking",
                      "thinking": "This is a nice number theory question. Let's think about it step by step...",
                      "signature": "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...",
                  },
                  {
                      "type": "text",
                      "text": "Yes, there are infinitely many prime numbers p such that p mod 4 = 3...",
                  },
              ],
          },
          {"role": "user", "content": "Can you write a formal proof?"},
      ],
  )

  print(response.json())
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.countTokens({
    model: "claude-sonnet-4-6",
    thinking: {
      type: "enabled",
      budget_tokens: 16000
    },
    messages: [
      {
        role: "user",
        content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
      },
      {
        role: "assistant",
        content: [
          {
            type: "thinking",
            thinking:
              "This is a nice number theory question. Let's think about it step by step...",
            signature:
              "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
          },
          {
            type: "text",
            text: "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
          }
        ]
      },
      {
        role: "user",
        content: "Can you write a formal proof?"
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  using System;
  using System.Threading.Tasks;
  using System.Collections.Generic;
  using Anthropic;
  using Anthropic.Models.Messages;

  public class Program
  {
      public static async Task Main(string[] args)
      {
          AnthropicClient client = new()
          {
              ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY")
          };

          var parameters = new MessageCountTokensParams
          {
              Model = Model.ClaudeSonnet4_6,
              Thinking = new ThinkingConfigEnabled(budgetTokens: 16000),
              Messages =
              [
                  new()
                  {
                      Role = Role.User,
                      Content = "Are there an infinite number of prime numbers such that n mod 4 == 3?"
                  },
                  new()
                  {
                      Role = Role.Assistant,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new ThinkingBlockParam()
                          {
                              Thinking = "This is a nice number theory question. Let's think about it step by step...",
                              Signature = "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...",
                          }),
                          new ContentBlockParam(new TextBlockParam("Yes, there are infinitely many prime numbers p such that p mod 4 = 3...")),
                      }),
                  },
                  new()
                  {
                      Role = Role.User,
                      Content = "Can you write a formal proof?"
                  }
              ]
          };

          var response = await client.Messages.CountTokens(parameters);
          Console.WriteLine(response);
      }
  }
  ```

  ```go Go
  thinkingBlock := anthropic.NewThinkingBlock(
  	"EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...",
  	"This is a nice number theory question. Let's think about it step by step...",
  )

  textBlock := anthropic.NewTextBlock(
  	"Yes, there are infinitely many prime numbers p such that p mod 4 = 3...",
  )

  response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
  	Model:    anthropic.Model("claude-sonnet-4-6"),
  	Thinking: anthropic.ThinkingConfigParamOfEnabled(16000),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Are there an infinite number of prime numbers such that n mod 4 == 3?")),
  		anthropic.NewAssistantMessage(thinkingBlock, textBlock),
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Can you write a formal proof?")),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Printf("%+v\n", response)
  ```

  ```java Java
  import com.anthropic.models.messages.MessageCountTokensParams;
  import com.anthropic.models.messages.MessageTokensCount;
  // ...
  import com.anthropic.models.messages.ThinkingBlockParam;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      List<ContentBlockParam> assistantBlocks = List.of(
        ContentBlockParam.ofThinking(
          ThinkingBlockParam.builder()
            .thinking(
              "This is a nice number theory question. Let's think about it step by step..."
            )
            .signature(
              "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
            )
            .build()
        ),
        ContentBlockParam.ofText(
          TextBlockParam.builder()
            .text("Yes, there are infinitely many prime numbers p such that p mod 4 = 3...")
            .build()
        )
      );

      MessageCountTokensParams params = MessageCountTokensParams.builder()
        .model(Model.CLAUDE_SONNET_4_6)
        .enabledThinking(16000)
        .addUserMessage("Are there an infinite number of prime numbers such that n mod 4 == 3?")
        .addAssistantMessageOfBlockParams(assistantBlocks)
        .addUserMessage("Can you write a formal proof?")
        .build();

      MessageTokensCount count = client.messages().countTokens(params);
      System.out.println(count);
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->countTokens(
      messages: [
          [
              'role' => 'user',
              'content' => 'Are there an infinite number of prime numbers such that n mod 4 == 3?'
          ],
          [
              'role' => 'assistant',
              'content' => [
                  [
                      'type' => 'thinking',
                      'thinking' => 'This is a nice number theory question. Let\'s think about it step by step...',
                      'signature' => 'EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV...'
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Yes, there are infinitely many prime numbers p such that p mod 4 = 3...'
                  ]
              ]
          ],
          [
              'role' => 'user',
              'content' => 'Can you write a formal proof?'
          ]
      ],
      model: 'claude-sonnet-4-6',
      thinking: [
          'type' => 'enabled',
          'budget_tokens' => 16000
      ],
  );

  echo json_encode($response);
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.count_tokens(
    model: "claude-sonnet-4-6",
    thinking: {
      type: "enabled",
      budget_tokens: 16000
    },
    messages: [
      {
        role: "user",
        content: "Are there an infinite number of prime numbers such that n mod 4 == 3?"
      },
      {
        role: "assistant",
        content: [
          {
            type: "thinking",
            thinking: "This is a nice number theory question. Let's think about it step by step...",
            signature: "EuYBCkQYAiJAgCs1le6/Pol5Z4/JMomVOouGrWdhYNsH3ukzUECbB6iWrSQtsQuRHJID6lWV..."
          },
          {
            type: "text",
            text: "Yes, there are infinitely many prime numbers p such that p mod 4 = 3..."
          }
        ]
      },
      {
        role: "user",
        content: "Can you write a formal proof?"
      }
    ]
  )

  puts response
  ```
</CodeGroup>

```json Output
{ "input_tokens": 88 }
```

### Count tokens in messages with PDFs

<Note>
  Token counting supports PDFs with the same [limitations](/docs/en/build-with-claude/pdf-support#pdf-support-limitations) as the Messages API.
</Note>

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages/count_tokens \
      --header "x-api-key: $ANTHROPIC_API_KEY" \
      --header "content-type: application/json" \
      --header "anthropic-version: 2023-06-01" \
      --data @- <<EOF
  {
    "model": "claude-opus-4-8",
    "messages": [{
      "role": "user",
      "content": [
        {
          "type": "document",
          "source": {
            "type": "base64",
            "media_type": "application/pdf",
            "data": "$PDF_BASE64"
          }
        },
        {
          "type": "text",
          "text": "Please summarize this document."
        }
      ]
    }]
  }
  EOF
  ```

  ```bash CLI
  ant messages count-tokens <<'YAML'
  model: claude-opus-4-8
  messages:
    - role: user
      content:
        - type: document
          source:
            type: base64
            media_type: application/pdf
            data: "@./document.pdf"
        - type: text
          text: Please summarize this document.
  YAML
  ```

  ```python Python
  import base64
  import anthropic

  client = anthropic.Anthropic()

  with open("/path/to/document.pdf", "rb") as pdf_file:
      pdf_base64 = base64.standard_b64encode(pdf_file.read()).decode("utf-8")

  response = client.messages.count_tokens(
      model="claude-opus-4-8",
      messages=[
          {
              "role": "user",
              "content": [
                  {
                      "type": "document",
                      "source": {
                          "type": "base64",
                          "media_type": "application/pdf",
                          "data": pdf_base64,
                      },
                  },
                  {"type": "text", "text": "Please summarize this document."},
              ],
          }
      ],
  )

  print(response.json())
  ```

  ```typescript TypeScript
  import { readFile } from "node:fs/promises";

  const client = new Anthropic();

  const pdfBase64 = await readFile("/path/to/document.pdf", { encoding: "base64" });

  const response = await client.messages.countTokens({
    model: "claude-opus-4-8",
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdfBase64
            }
          },
          {
            type: "text",
            text: "Please summarize this document."
          }
        ]
      }
    ]
  });

  console.log(response);
  ```

  ```csharp C#
  using System;
  using System.IO;
  using System.Threading.Tasks;
  using System.Collections.Generic;
  using Anthropic;
  using Anthropic.Models.Messages;

  class Program
  {
      static async Task Main(string[] args)
      {
          AnthropicClient client = new();

          byte[] pdfBytes = await File.ReadAllBytesAsync("/path/to/document.pdf");
          string pdfBase64 = Convert.ToBase64String(pdfBytes);

          var parameters = new MessageCountTokensParams
          {
              Model = Model.ClaudeOpus4_8,
              Messages =
              [
                  new()
                  {
                      Role = Role.User,
                      Content = new MessageParamContent(new List<ContentBlockParam>
                      {
                          new ContentBlockParam(new DocumentBlockParam(
                              new DocumentBlockParamSource(new Base64PdfSource()
                              {
                                  Data = pdfBase64,
                              })
                          )),
                          new ContentBlockParam(new TextBlockParam("Please summarize this document.")),
                      }),
                  }
              ]
          };

          var count = await client.Messages.CountTokens(parameters);
          Console.WriteLine(count);
      }
  }
  ```

  ```go Go
  pdfBytes, err := os.ReadFile("/path/to/document.pdf")
  if err != nil {
  	log.Fatal(err)
  }
  pdfBase64 := base64.StdEncoding.EncodeToString(pdfBytes)

  response, err := client.Messages.CountTokens(context.TODO(), anthropic.MessageCountTokensParams{
  	Model: anthropic.ModelClaudeOpus4_8,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(
  			anthropic.NewDocumentBlock(anthropic.Base64PDFSourceParam{
  				Data: pdfBase64,
  			}),
  			anthropic.NewTextBlock("Please summarize this document."),
  		),
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }

  fmt.Println(response)
  ```

  ```java Java
  import com.anthropic.models.messages.Base64PdfSource;
  // ...
  import com.anthropic.models.messages.DocumentBlockParam;
  import com.anthropic.models.messages.MessageCountTokensParams;
  import com.anthropic.models.messages.MessageTokensCount;
  // ...
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      byte[] fileBytes = Files.readAllBytes(Path.of("/path/to/document.pdf"));
      String pdfBase64 = Base64.getEncoder().encodeToString(fileBytes);

      ContentBlockParam documentBlock = ContentBlockParam.ofDocument(
        DocumentBlockParam.builder()
          .source(Base64PdfSource.builder().data(pdfBase64).build())
          .build()
      );

      ContentBlockParam textBlock = ContentBlockParam.ofText(
        TextBlockParam.builder().text("Please summarize this document.").build()
      );

      MessageCountTokensParams params = MessageCountTokensParams.builder()
        .model(Model.CLAUDE_OPUS_4_8)
        .addUserMessageOfBlockParams(List.of(documentBlock, textBlock))
        .build();

      MessageTokensCount count = client.messages().countTokens(params);
      System.out.println(count);
  ```

  ```php PHP
  $client = new Client();

  $pdfBase64 = base64_encode(file_get_contents("/path/to/document.pdf"));

  $response = $client->messages->countTokens(
      messages: [
          [
              'role' => 'user',
              'content' => [
                  [
                      'type' => 'document',
                      'source' => [
                          'type' => 'base64',
                          'media_type' => 'application/pdf',
                          'data' => $pdfBase64
                      ]
                  ],
                  [
                      'type' => 'text',
                      'text' => 'Please summarize this document.'
                  ]
              ]
          ]
      ],
      model: 'claude-opus-4-8',
  );

  echo json_encode($response);
  ```

  ```ruby Ruby
  require "base64"

  client = Anthropic::Client.new

  pdf_base64 = Base64.strict_encode64(File.binread("/path/to/document.pdf"))

  response = client.messages.count_tokens(
    model: "claude-opus-4-8",
    messages: [
      {
        role: "user",
        content: [
          {
            type: "document",
            source: {
              type: "base64",
              media_type: "application/pdf",
              data: pdf_base64
            }
          },
          {
            type: "text",
            text: "Please summarize this document."
          }
        ]
      }
    ]
  )

  puts response
  ```
</CodeGroup>

```json Output
{ "input_tokens": 2188 }
```

***

## Token counts on Claude Fable 5 and Claude Mythos 5

Claude Fable 5 and Claude Mythos 5 use the tokenizer introduced with Claude Opus 4.7, which produces roughly 30% more tokens than models before Claude Opus 4.7 for the same text. The exact increase depends on the content and workload shape. The token counting endpoint returns the count under the tokenizer of the `model` you pass, so to measure the difference for your workload, count the same request twice: once with your current model and once with `model: "claude-fable-5"` (or `"claude-mythos-5"`), and compare the two `input_tokens` values.

<Note>
  **Billing and migration:** Usage and billing on Claude Fable 5 and Claude Mythos 5 reflect this tokenizer's counts. If you're migrating from a model before Claude Opus 4.7, the same content consumes roughly 30% more tokens. The exact increase depends on the content and workload shape. When migrating a workload to Claude Fable 5 and Claude Mythos 5, don't reuse token counts measured on a model before Claude Opus 4.7 to estimate costs or context window fit. Count your prompts with `model: "claude-fable-5"` (or `"claude-mythos-5"`).
</Note>

***

## Pricing and rate limits

Token counting is **free to use** but subject to requests per minute rate limits based on your [usage tier](/docs/en/api/rate-limits#rate-limits). If you need higher limits, use **Request rate limit increase** on the [Limits](/settings/limits) page.

| Usage tier | Requests per minute (RPM) |
| ---------- | ------------------------- |
| Start      | 2,000                     |
| Build      | 4,000                     |
| Scale      | 8,000                     |

<Note>
  Token counting and message creation have separate and independent rate limits. Usage of one does not count against the limits of the other.
</Note>

***

## FAQ

<AccordionGroup>
  <Accordion title="Does token counting use prompt caching?">
    No, token counting provides an estimate without using caching logic. While you may provide `cache_control` blocks in your token counting request, prompt caching only occurs during actual message creation.
  </Accordion>
</AccordionGroup>

***

## Next steps

<CardGroup cols={2}>
  <Card title="Count message tokens" icon="code" href="/docs/en/api/messages-count-tokens">
    Read the full API reference for the token counting endpoint.
  </Card>

  <Card title="Context windows" icon="arrows-maximize" href="/docs/en/build-with-claude/context-windows">
    Use token counts to keep prompts within a model's context window.
  </Card>

  <Card title="Rate limits" icon="gauge" href="/docs/en/api/rate-limits">
    Check token counts before you send a request to stay within your usage tier.
  </Card>

  <Card title="Prompt caching" icon="database" href="/docs/en/build-with-claude/prompt-caching">
    Reduce cost and latency on repeated prompts by caching prompt prefixes.
  </Card>
</CardGroup>
