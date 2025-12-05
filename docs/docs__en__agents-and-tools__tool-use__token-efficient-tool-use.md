# Token-efficient tool use

---

Starting with Claude Sonnet 3.7, Claude is capable of calling tools in a token-efficient manner. Requests save an average of 14% in output tokens, up to 70%, which also reduces latency. Exact token reduction and latency improvements depend on the overall response shape and size.

<Info>
Token-efficient tool use is a beta feature that **only works with Claude 3.7 Sonnet**. To use this beta feature, add the beta header `token-efficient-tools-2025-02-19` to a tool use request. This header has no effect on other Claude models.

All [Claude 4 models](/docs/en/about-claude/models/overview) support token-efficient tool use by default. No beta header is needed.
</Info>

<Warning>
Token-efficient tool use does not currently work with [`disable_parallel_tool_use`](/docs/en/agents-and-tools/tool-use/implement-tool-use).
</Warning>

Here's an example of how to use token-efficient tools with the API in Claude Sonnet 3.7:

<CodeGroup>

  ```bash Shell
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-beta: token-efficient-tools-2025-02-19" \
    -d '{
      "model": "claude-3-7-sonnet-20250219",
      "max_tokens": 1024,
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
            "required": [
              "location"
            ]
          }
        }
      ],
      "messages": [
        {
          "role": "user",
          "content": "Tell me the weather in San Francisco."
        }
      ]
    }' | jq '.usage'
  ```

  ```python Python
  import anthropic

  client = anthropic.Anthropic()

  response = client.beta.messages.create(
      max_tokens=1024,
      model="claude-3-7-sonnet-20250219",
      tools=[{
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
          "required": [
            "location"
          ]
        }
      }],
      messages=[{
        "role": "user",
        "content": "Tell me the weather in San Francisco."
      }],
      betas=["token-efficient-tools-2025-02-19"]
  )

  print(response.usage)
  ```

  ```typescript TypeScript
  import Anthropic from '@anthropic-ai/sdk';

  const anthropic = new Anthropic();

  const message = await anthropic.beta.messages.create({
    model: "claude-3-7-sonnet-20250219",
    max_tokens: 1024,
    tools: [{
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
    }],
    messages: [{ 
      role: "user", 
      content: "Tell me the weather in San Francisco." 
    }],
    betas: ["token-efficient-tools-2025-02-19"]
  });

  console.log(message.usage);
  ```

  ```java Java
  import java.util.List;
  import java.util.Map;

  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.JsonValue;
  import com.anthropic.models.beta.messages.BetaMessage;
  import com.anthropic.models.beta.messages.BetaTool;
  import com.anthropic.models.beta.messages.MessageCreateParams;

  import static com.anthropic.models.beta.AnthropicBeta.TOKEN_EFFICIENT_TOOLS_2025_02_19;

  public class TokenEfficientToolsExample {

      public static void main(String[] args) {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          BetaTool.InputSchema schema = BetaTool.InputSchema.builder()
                  .properties(JsonValue.from(Map.of(
                          "location",
                          Map.of(
                                  "type", "string",
                                  "description", "The city and state, e.g. San Francisco, CA"
                          )
                  )))
                  .putAdditionalProperty("required", JsonValue.from(List.of("location")))
                  .build();

          MessageCreateParams params = MessageCreateParams.builder()
                  .model("claude-3-7-sonnet-20250219")
                  .maxTokens(1024)
                  .betas(List.of(TOKEN_EFFICIENT_TOOLS_2025_02_19))
                  .addTool(BetaTool.builder()
                          .name("get_weather")
                          .description("Get the current weather in a given location")
                          .inputSchema(schema)
                          .build())
                  .addUserMessage("Tell me the weather in San Francisco.")
                  .build();

          BetaMessage message = client.beta().messages().create(params);
          System.out.println(message.usage());
      }
  }
  ```
</CodeGroup>

The above request should, on average, use fewer input and output tokens than a normal request. To confirm this, try making the same request but remove `token-efficient-tools-2025-02-19` from the beta headers list.

<Tip>
To keep the benefits of prompt caching, use the beta header consistently for requests you'd like to cache. If you selectively use it, prompt caching will fail. 
</Tip>