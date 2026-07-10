# Structured outputs

Get validated JSON results from agent workflows

---

Structured outputs constrain Claude's responses to follow a specific schema, ensuring valid, parseable output for downstream processing. Structured outputs provide two complementary features:

* **JSON outputs** (`output_config.format`): Get Claude's response in a specific JSON format
* **Strict tool use** (`strict: true`): Guarantee schema validation on tool names and inputs

You can use these features independently or together in the same request.

<Note>
  Structured outputs are generally available on the Claude API for Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, [Claude Mythos Preview](https://anthropic.com/glasswing), Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5. On Amazon Bedrock, structured outputs are generally available for Claude Opus 4.6, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5; Claude Sonnet 5, Claude Opus 4.7, and Claude Mythos Preview are available through [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) (the Messages-API Bedrock endpoint). Structured outputs are available on [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws). On [Google Cloud](/docs/en/build-with-claude/claude-on-vertex-ai), structured outputs are generally available for Claude Fable 5, Claude Mythos 5, Claude Opus 4.8, Claude Mythos Preview, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, Claude Sonnet 4.6, Claude Sonnet 4.5, Claude Opus 4.5, and Claude Haiku 4.5. Structured outputs are generally available on [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry) and require a [Hosted on Anthropic deployment](/docs/en/build-with-claude/claude-in-microsoft-foundry#additional-features-not-supported-when-hosted-on-azure).
</Note>

<Note>
  This feature qualifies for [Zero Data Retention (ZDR)](/docs/en/build-with-claude/api-and-data-retention) with limited technical retention. See the [Data retention](#data-retention) section for details on what is retained and why.
</Note>

<Tip>
  **Migrating from beta?** The `output_format` parameter has moved to `output_config.format`, and beta headers are no longer required. The old beta header (`structured-outputs-2025-11-13`) and `output_format` parameter will continue working for a transition period. See the following code examples for the updated API shape.
</Tip>

## Why use structured outputs

Without structured outputs, Claude can generate malformed JSON responses or invalid tool inputs that break your applications. Even with careful prompting, you may encounter:

* Parsing errors from invalid JSON syntax
* Missing required fields
* Inconsistent data types
* Schema violations requiring error handling and retries

Structured outputs guarantee schema-compliant responses through constrained decoding:

* **Always valid:** No more `JSON.parse()` errors
* **Type safe:** Guaranteed field types and required fields
* **Reliable:** No retries needed for schema violations

## JSON outputs

JSON outputs control Claude's response format, ensuring Claude returns valid JSON matching your schema. Use JSON outputs when you need to:

* Control Claude's response format
* Extract data from images or text
* Generate structured reports
* Format API responses

### Quick start

<CodeGroup>
  ```bash cURL
  curl https://api.anthropic.com/v1/messages \
    -H "content-type: application/json" \
    -H "x-api-key: $ANTHROPIC_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {
          "role": "user",
          "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
        }
      ],
      "output_config": {
        "format": {
          "type": "json_schema",
          "schema": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "email": {"type": "string"},
              "plan_interest": {"type": "string"},
              "demo_requested": {"type": "boolean"}
            },
            "required": ["name", "email", "plan_interest", "demo_requested"],
            "additionalProperties": false
          }
        }
      }
    }'
  ```

  ```bash CLI
  ant messages create \
    --transform 'content.0.text|@fromstr' \
    --format jsonl <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: >-
        Extract the key information from this email: John Smith
        (john@example.com) is interested in our Enterprise plan and wants
        to schedule a demo for next Tuesday at 2pm.
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          name: {type: string}
          email: {type: string}
          plan_interest: {type: string}
          demo_requested: {type: boolean}
        required: [name, email, plan_interest, demo_requested]
        additionalProperties: false
  YAML
  ```

  ```python Python
  client = anthropic.Anthropic()

  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
          }
      ],
      output_config={
          "format": {
              "type": "json_schema",
              "schema": {
                  "type": "object",
                  "properties": {
                      "name": {"type": "string"},
                      "email": {"type": "string"},
                      "plan_interest": {"type": "string"},
                      "demo_requested": {"type": "boolean"},
                  },
                  "required": ["name", "email", "plan_interest", "demo_requested"],
                  "additionalProperties": False,
              },
          }
      },
  )
  print(response.content[0].text)
  ```

  ```typescript TypeScript
  const client = new Anthropic();

  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }
    ],
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            plan_interest: { type: "string" },
            demo_requested: { type: "boolean" }
          },
          required: ["name", "email", "plan_interest", "demo_requested"],
          additionalProperties: false
        }
      }
    }
  });

  for (const block of response.content) {
    if (block.type === "text") {
      console.log(block.text);
    }
  }
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  AnthropicClient client = new();

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan." }],
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      name = new { type = "string" },
                      email = new { type = "string" },
                      plan_interest = new { type = "string" },
                      demo_requested = new { type = "boolean" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "name", "email", "plan_interest", "demo_requested" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, _ := client.Messages.New(context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(
  				anthropic.NewTextBlock("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."),
  			),
  		},
  		OutputConfig: anthropic.OutputConfigParam{
  			Format: anthropic.JSONOutputFormatParam{
  				Schema: map[string]any{
  					"type": "object",
  					"properties": map[string]any{
  						"name":           map[string]string{"type": "string"},
  						"email":          map[string]string{"type": "string"},
  						"plan_interest":  map[string]string{"type": "string"},
  						"demo_requested": map[string]string{"type": "boolean"},
  					},
  					"required":             []string{"name", "email", "plan_interest", "demo_requested"},
  					"additionalProperties": false,
  				},
  			},
  		},
  	})

  fmt.Println(response.Content[0].Text)
  ```

  ```java Java
  static class ContactInfo {
      public String name;
      public String email;
      public String plan_interest;
      public boolean demo_requested;
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      StructuredMessageCreateParams<ContactInfo> params = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.")
          .outputConfig(ContactInfo.class)
          .build();

      StructuredMessage<ContactInfo> response = client.messages().create(params);
      ContactInfo contact = response.content().stream()
          .flatMap(block -> block.text().stream())
          .findFirst().orElseThrow().text();
      IO.println(contact.name + " (" + contact.email + ")");
  }
  ```

  ```php PHP
  $client = new Client();

  $response = $client->messages->create(
      maxTokens: 1024,
      messages: [
          [
              'role' => 'user',
              'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'
          ]
      ],
      model: 'claude-opus-4-8',
      outputConfig: [
          'format' => [
              'type' => 'json_schema',
              'schema' => [
                  'type' => 'object',
                  'properties' => [
                      'name' => ['type' => 'string'],
                      'email' => ['type' => 'string'],
                      'plan_interest' => ['type' => 'string'],
                      'demo_requested' => ['type' => 'boolean']
                  ],
                  'required' => ['name', 'email', 'plan_interest', 'demo_requested'],
                  'additionalProperties' => false
              ]
          ]
      ],
  );

  echo $response->content[0]->text;
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  response = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
      }
    ],
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            plan_interest: { type: "string" },
            demo_requested: { type: "boolean" }
          },
          required: ["name", "email", "plan_interest", "demo_requested"],
          additionalProperties: false
        }
      }
    }
  )

  puts response.content[0].text
  ```
</CodeGroup>

**Response format:** Valid JSON matching your schema in `response.content[0].text`

```json Output
{
  "name": "John Smith",
  "email": "john@example.com",
  "plan_interest": "Enterprise",
  "demo_requested": true
}
```

### How it works

<Steps>
  <Step title="Define your JSON schema">
    Create a JSON schema that describes the structure you want Claude to follow. The schema uses standard JSON Schema format with some limitations (see [JSON Schema limitations](#json-schema-limitations)).
  </Step>

  <Step title="Add the output_config.format parameter">
    Include the `output_config.format` parameter in your API request with `type: "json_schema"` and your schema definition.
  </Step>

  <Step title="Parse the response">
    Claude's response is valid JSON matching your schema, returned in `response.content[0].text`.
  </Step>
</Steps>

### Working with JSON outputs in SDKs

The SDKs provide helpers that make it easier to work with JSON outputs, including schema transformation, automatic validation, and integration with popular schema libraries.

<Note>
  The Python SDK's `client.messages.parse()` still accepts `output_format` as a convenience parameter and translates it to `output_config.format` internally. Other SDKs require `output_config` directly. The following examples show the SDK helper syntax.
</Note>

#### Using native schema definitions

Instead of writing raw JSON schemas, you can use familiar schema definition tools in your language:

* **Python:** [Pydantic](https://docs.pydantic.dev/) models with `client.messages.parse()`
* **TypeScript:** [Zod](https://zod.dev/) schemas with `zodOutputFormat()` or typed JSON Schema literals with `jsonSchemaOutputFormat()`
* **Java:** Plain Java classes with automatic schema derivation through `outputConfig(Class<T>)`
* **Ruby:** `Anthropic::BaseModel` classes with `output_config: {format: Model}`
* **PHP:** Classes implementing `StructuredOutputModel` with `outputConfig: ['format' => MyClass::class]`
* **C#:** Plain C# classes with the generic `Create<T>()` overload, which derives the schema automatically
* **Go:** Go structs reflected into JSON schemas automatically on the beta API, or raw JSON schemas through `output_config`
* **CLI:** Raw JSON schemas passed through `output_config`

<CodeGroup>
  ```bash CLI
  { read -r _ NAME; read -r _ EMAIL; } < <(
    ant messages create \
      --transform 'content.0.text|@fromstr|{name,email}' \
      --format yaml <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: >-
        Extract the key information from this email: John Smith
        (john@example.com) is interested in our Enterprise plan and wants
        to schedule a demo for next Tuesday at 2pm.
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          name: {type: string}
          email: {type: string}
          plan_interest: {type: string}
          demo_requested: {type: boolean}
        required: [name, email, plan_interest, demo_requested]
        additionalProperties: false
  YAML
  )
  printf '%s (%s)\n' "$NAME" "$EMAIL"
  ```

  ```python Python
  from pydantic import BaseModel
  from anthropic import Anthropic


  class ContactInfo(BaseModel):
      name: str
      email: str
      plan_interest: str
      demo_requested: bool


  client = Anthropic()

  response = client.messages.parse(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
          }
      ],
      output_format=ContactInfo,
  )

  print(response.parsed_output)
  ```

  ```typescript TypeScript
  import { z } from "zod";
  import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

  const ContactInfoSchema = z.object({
    name: z.string(),
    email: z.string(),
    plan_interest: z.string(),
    demo_requested: z.boolean()
  });

  const client = new Anthropic();

  const response = await client.messages.parse({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content:
          "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }
    ],
    output_config: { format: zodOutputFormat(ContactInfoSchema) }
  });

  // Automatically parsed and validated
  console.log(response.parsed_output);
  ```

  ```csharp C#
  using System.Text.Json;
  using Anthropic;
  using Anthropic.Models.Messages;

  var client = new AnthropicClient();

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() {
          Role = Role.User,
          Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
      }],
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      name = new { type = "string" },
                      email = new { type = "string" },
                      plan_interest = new { type = "string" },
                      demo_requested = new { type = "boolean" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(
                      new[] { "name", "email", "plan_interest", "demo_requested" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
  });

  if (response.Content[0].TryPickText(out var textBlock))
  {
      // JSON is guaranteed to match the schema
      var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(textBlock.Text)!;
      Console.WriteLine($"{contact["name"]} ({contact["email"]})");
  }
  ```

  ```go Go
  import (
  // ...
  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/invopop/jsonschema"
  )

  type ContactInfo struct {
  	Name          string `json:"name" jsonschema:"description=Full name"`
  	Email         string `json:"email" jsonschema:"description=Email address"`
  	PlanInterest  string `json:"plan_interest" jsonschema:"description=Plan type"`
  	DemoRequested bool   `json:"demo_requested" jsonschema:"description=Whether a demo was requested"`
  }

  func generateSchema(v any) map[string]any {
  	r := jsonschema.Reflector{AllowAdditionalProperties: false, DoNotReference: true}
  	s := r.Reflect(v)
  	b, _ := json.Marshal(s)
  	var m map[string]any
  	json.Unmarshal(b, &m)
  	return m
  }
  // ...
  	schema := generateSchema(&ContactInfo{})

  	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus4_8,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock(
  				"Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.",
  			)),
  		},
  		OutputConfig: anthropic.OutputConfigParam{
  			Format: anthropic.JSONOutputFormatParam{
  				Schema: schema,
  			},
  		},
  	})

  	for _, block := range message.Content {
  		switch variant := block.AsAny().(type) {
  		case anthropic.TextBlock:
  			var contact ContactInfo
  			json.Unmarshal([]byte(variant.Text), &contact)
  			fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
  		}
  	}
  ```

  ```java Java
  static class ContactInfo {
      public String name;
      public String email;
      public String planInterest;
      public boolean demoRequested;
  }

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.fromEnv();

      StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
          .model(Model.CLAUDE_OPUS_4_8)
          .maxTokens(1024)
          .outputConfig(ContactInfo.class)
          .addUserMessage("Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.")
          .build();

      StructuredMessage<ContactInfo> response = client.messages().create(createParams);
      ContactInfo contact = response.content().stream()
          .flatMap(block -> block.text().stream())
          .findFirst().orElseThrow().text();
      IO.println(contact.name + " (" + contact.email + ")");
  }
  ```

  ```php PHP
  use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
  use Anthropic\Lib\Contracts\StructuredOutputModel;

  $client = new Client();

  class ContactInfo implements StructuredOutputModel
  {
      use StructuredOutputModelTrait;

      public string $name;
      public string $email;
      public string $plan_interest;
      public bool $demo_requested;
  }

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm.'],
      ],
      model: 'claude-opus-4-8',
      outputConfig: ['format' => ContactInfo::class],
  );

  $contact = $message->parsedOutput();
  if ($contact instanceof ContactInfo) {
      echo "{$contact->name} ({$contact->email})\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  class ContactInfo < Anthropic::BaseModel
    required :name, String
    required :email, String
    required :plan_interest, String
    required :demo_requested, Anthropic::Boolean
  end

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{
      role: "user",
      content: "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan and wants to schedule a demo for next Tuesday at 2pm."
    }],
    output_config: {format: ContactInfo}
  )

  contact = message.parsed_output
  puts "#{contact.name} (#{contact.email})"
  ```
</CodeGroup>

#### SDK-specific methods

Each SDK provides helpers that make working with structured outputs easier. See individual SDK pages for full details.

<Tabs>
  <Tab title="CLI">
    **Raw JSON schemas through heredoc body**

    The CLI passes raw JSON schemas as a YAML heredoc body. Use the GJSON `@fromstr` modifier with `--transform` to parse the JSON string returned in `content[0].text` and project specific fields.

    ```bash
    ant messages create \
      --transform 'content.0.text|@fromstr|{name,email}' \
      --format yaml <<'YAML'
    model: claude-opus-4-8
    max_tokens: 1024
    messages:
      - role: user
        content: >-
          Extract contact info: John Smith, john@example.com,
          interested in the Pro plan
    output_config:
      format:
        type: json_schema
        schema:
          type: object
          properties:
            name: {type: string}
            email: {type: string}
            plan_interest: {type: string}
          required: [name, email, plan_interest]
          additionalProperties: false
    YAML
    ```

    ```yaml Output
    name: John Smith
    email: john@example.com
    ```
  </Tab>

  <Tab title="Python">
    **`client.messages.parse()` (Recommended)**

    The `parse()` method automatically transforms your Pydantic model, validates the response, and returns a `parsed_output` attribute.

    ```python
    from pydantic import BaseModel
    # ...
    class ContactInfo(BaseModel):
        name: str
        email: str
        plan_interest: str
    # ...
    response = client.messages.parse(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Extract contact info: John Smith, john@example.com, interested in the Pro plan",
            }
        ],
        output_format=ContactInfo,
    )

    # Access the parsed output directly
    contact = response.parsed_output
    print(contact.name, contact.email)
    ```

    **`transform_schema()` helper**

    For when you need to manually transform schemas before sending, or when you want to modify a Pydantic-generated schema. Unlike `client.messages.parse()`, which transforms provided schemas automatically, this gives you the transformed schema so you can further customize it.

    ```python
    from anthropic import transform_schema
    from pydantic import TypeAdapter
    # ...

    # First convert Pydantic model to JSON schema, then transform
    schema = TypeAdapter(ContactInfo).json_schema()
    schema = transform_schema(schema)
    # Modify schema if needed
    schema["properties"]["custom_field"] = {"type": "string"}

    response = client.messages.create(
        model="claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": "..."}],
        output_config={
            "format": {"type": "json_schema", "schema": schema},
        },
    )
    ```
  </Tab>

  <Tab title="TypeScript">
    **`client.messages.parse()` with `zodOutputFormat()`**

    The `parse()` method accepts a Zod schema, validates the response, and returns a `parsed_output` attribute with the inferred TypeScript type matching the schema.

    ```typescript
    import { z } from "zod";
    import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

    const ContactInfo = z.object({
      name: z.string(),
      email: z.string(),
      planInterest: z.string()
    });

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: { format: zodOutputFormat(ContactInfo) }
    });

    // Guaranteed type-safe
    console.log(response.parsed_output!.email);
    ```

    **`client.messages.parse()` with `jsonSchemaOutputFormat()`**

    The `jsonSchemaOutputFormat()` helper accepts a JSON Schema object and integrates it with `parse()` without requiring Zod. Zod is an optional peer dependency you install separately; `jsonSchemaOutputFormat()` works out of the box because the SDK bundles `json-schema-to-ts` directly.

    For **inline schema literals** (declared with `as const` in your source), you also get compile-time type inference: `parsed_output` is typed to match the schema structure. For **imported or generated schemas** (from a JSON file or OpenAPI codegen), the helper still sends the schema and parses the response, but the inferred type is `unknown` because `as const` can only apply to literal expressions.

    ```typescript
    import { jsonSchemaOutputFormat } from "@anthropic-ai/sdk/helpers/json-schema";

    const client = new Anthropic();

    const response = await client.messages.parse({
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: {
        format: jsonSchemaOutputFormat({
          type: "object",
          properties: {
            name: { type: "string" },
            email: { type: "string" },
            planInterest: { type: "string" }
          },
          required: ["name", "email", "planInterest"],
          additionalProperties: false
        } as const)
      }
    });

    // response.parsed_output is typed as { name: string; email: string; planInterest: string } | null
    console.log(response.parsed_output!.email);
    ```

    **Type inference requires `as const`.** Use a literal object expression with a `const` assertion so TypeScript can narrow the property types. Without `as const`, the inferred type collapses to `unknown`.

    **Schema transformation.** By default, the helper transforms the schema the same way `zodOutputFormat()` does: removing unsupported constraints, adding `additionalProperties: false` to objects, and filtering string formats. Pass `jsonSchemaOutputFormat(schema, { transform: false })` to send your schema to the API unchanged. See [How SDK transformation works](#how-sdk-transformation-works).
  </Tab>

  <Tab title="C#">
    **JSON schemas through `OutputConfig`**

    The C# SDK accepts raw JSON schemas built programmatically with `JsonSerializer.SerializeToElement`, as shown here, or derives the schema from a plain C# class with the generic `Create<T>()` overload. Deserialize the response JSON with `JsonSerializer.Deserialize`.

    ```csharp
    using System.Text.Json;
    using Anthropic;
    using Anthropic.Models.Messages;

    var client = new AnthropicClient();

    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = Model.ClaudeOpus4_8,
        MaxTokens = 1024,
        Messages = [new() {
            Role = Role.User,
            Content = "Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan."
        }],
        OutputConfig = new OutputConfig
        {
            Format = new JsonOutputFormat
            {
                Schema = new Dictionary<string, JsonElement>
                {
                    ["type"] = JsonSerializer.SerializeToElement("object"),
                    ["properties"] = JsonSerializer.SerializeToElement(new
                    {
                        name = new { type = "string" },
                        email = new { type = "string" },
                        plan_interest = new { type = "string" },
                    }),
                    ["required"] = JsonSerializer.SerializeToElement(
                        new[] { "name", "email", "plan_interest" }),
                    ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                },
            },
        },
    });

    if (response.Content[0].TryPickText(out var textBlock))
    {
        // JSON is guaranteed to match the schema
        var contact = JsonSerializer.Deserialize<Dictionary<string, object>>(textBlock.Text)!;
        Console.WriteLine($"{contact["name"]} ({contact["email"]})");
    }
    ```
  </Tab>

  <Tab title="Go">
    **Raw JSON schemas through `OutputConfigParam`**

    The Go SDK works with raw JSON schemas. Define a Go struct with json tags, generate the JSON schema (for example, using `invopop/jsonschema`), and unmarshal the response text into your struct. On the beta API, passing a struct as the output format schema reflects it into a JSON schema automatically.

    ```go
    import (
    // ...
    	"github.com/anthropics/anthropic-sdk-go"
    	"github.com/invopop/jsonschema"
    )

    type ContactInfo struct {
    	Name         string `json:"name" jsonschema:"description=Full name"`
    	Email        string `json:"email" jsonschema:"description=Email address"`
    	PlanInterest string `json:"plan_interest" jsonschema:"description=Plan type"`
    }

    func generateSchema(v any) map[string]any {
    	r := jsonschema.Reflector{AllowAdditionalProperties: false, DoNotReference: true}
    	s := r.Reflect(v)
    	b, _ := json.Marshal(s)
    	var m map[string]any
    	json.Unmarshal(b, &m)
    	return m
    }
    // ...
    	schema := generateSchema(&ContactInfo{})

    	message, _ := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     anthropic.ModelClaudeOpus4_8,
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock(
    				"Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.",
    			)),
    		},
    		OutputConfig: anthropic.OutputConfigParam{
    			Format: anthropic.JSONOutputFormatParam{
    				Schema: schema,
    			},
    		},
    	})

    	for _, block := range message.Content {
    		switch variant := block.AsAny().(type) {
    		case anthropic.TextBlock:
    			var contact ContactInfo
    			json.Unmarshal([]byte(variant.Text), &contact)
    			fmt.Printf("%s (%s)\n", contact.Name, contact.Email)
    		}
    	}
    ```
  </Tab>

  <Tab title="Java">
    Java examples on this page use [JDK 25 compact source file](https://openjdk.org/jeps/512) syntax; see the [Java SDK requirements](/docs/en/cli-sdks-libraries/sdks/java#requirements) for the substitution on earlier JDKs.

    **`outputConfig(Class<T>)` method**

    Pass a Java class to `outputConfig()` and the SDK automatically derives a JSON schema, validates it, and returns a `StructuredMessageCreateParams<T>`. Access the parsed result through `response.content().stream().flatMap(block -> block.text().stream()).findFirst().orElseThrow().text()`.

    <Note>
      Declare your schema classes as top-level classes or `static` nested classes. This requirement comes from the Jackson Databind library (`com.fasterxml.jackson.databind`), which the SDK uses to deserialize JSON responses into your class instances and cannot instantiate non-static inner classes.
    </Note>

    ```java
    static class ContactInfo {
        public String name;
        public String email;
        public String planInterest;
    }

    void main() {
        AnthropicClient client = AnthropicOkHttpClient.fromEnv();

        StructuredMessageCreateParams<ContactInfo> createParams = MessageCreateParams.builder()
            .model(Model.CLAUDE_OPUS_4_8)
            .maxTokens(1024)
            .outputConfig(ContactInfo.class)
            .addUserMessage("Extract contact info: John Smith, john@example.com, interested in the Pro plan")
            .build();

        StructuredMessage<ContactInfo> response = client.messages().create(createParams);
        ContactInfo contact = response.content().stream()
            .flatMap(block -> block.text().stream())
            .findFirst().orElseThrow().text();
        IO.println(contact.name + " (" + contact.email + ")");
    }
    ```

    <Accordion title="Generic type erasure">
      Java retains generic type information for fields in the class's metadata, but generic type erasure applies in other scopes. While a JSON schema can be derived from a `BookList.books` field with type `List<Book>`, a valid JSON schema cannot be derived from a local variable of that same type.

      If an error occurs while converting a JSON response to a Java class instance, the error message includes the JSON response to assist in diagnosis. If your JSON response may contain sensitive information, avoid logging it directly, or ensure that you redact any sensitive details from the error message.
    </Accordion>

    <Accordion title="Local schema validation">
      Structured outputs support a [subset of the JSON Schema language](/docs/en/build-with-claude/structured-outputs#json-schema-limitations). The SDK generates schemas automatically from classes to align with this subset. The `outputConfig(Class<T>)` method performs a validation check on the schema derived from the specified class.

      Key points:

      * **Local validation** occurs without sending requests to the remote AI model.
      * **Remote validation** is also performed by the AI model upon receiving the JSON schema.
      * **Version compatibility:** Local validation may fail while remote validation succeeds if the SDK version is outdated.
      * **Disabling local validation:** Pass `JsonSchemaLocalValidation.NO` if you encounter compatibility issues:

      ```java
      import com.anthropic.core.JsonSchemaLocalValidation;
      // ...

      static class BookList {
          public List<String> books;
      }

      void main() {
          StructuredMessageCreateParams<BookList> createParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(2048)
              .outputConfig(BookList.class, JsonSchemaLocalValidation.NO)
              .addUserMessage("List some famous late twentieth century novels.")
              .build();
      }
      ```
    </Accordion>

    <Accordion title="Streaming">
      Structured outputs also work with streaming. As responses arrive in stream events, you need to accumulate the full response before deserializing the JSON.

      Use `MessageAccumulator` to collect the JSON strings from the stream. Once accumulated, call `MessageAccumulator.message(Class<T>)` to convert the accumulated `Message` into a `StructuredMessage`, which automatically deserializes the JSON into your Java class.
    </Accordion>

    <Accordion title="JSON schema properties">
      When the SDK derives a JSON schema from your Java classes, it includes all properties represented by `public` fields or `public` getter methods by default and excludes non-`public` fields and getter methods.

      You can control visibility with annotations:

      * `@JsonIgnore` excludes a `public` field or getter method
      * `@JsonProperty` includes a non-`public` field or getter method

      If you define `private` fields with `public` getter methods, the SDK derives the property name from the getter (for example, `private` field `myValue` with `public` method `getMyValue()` produces a `"myValue"` property). To use a non-conventional getter name, annotate the method with `@JsonProperty`.

      Each class must define at least one property for the JSON schema. A validation error occurs if no fields or getter methods can produce schema properties, such as when:

      * There are no fields or getter methods in the class
      * All `public` members are annotated with `@JsonIgnore`
      * All non-`public` members lack `@JsonProperty` annotations
      * A field uses a `Map` type, which produces an empty `"properties"` field
    </Accordion>

    <Accordion title="Composition and inheritance">
      Your Java classes can use composition and inheritance to share structure when defining JSON schemas. Each pattern affects the output structure differently.

      **Composition** produces nested JSON output. Deriving a schema from class `Composed` that composes `A` and `B`:

      ```java
      static class A {
          public String a;
      }

      static class B {
          public String b;
      }

      static class Composed {
          public A composedA;
          public B composedB;
      }
      ```

      The JSON output has this nested structure:

      ```json
      {
        "composedA": { "a": "hello" },
        "composedB": { "b": "world" }
      }
      ```

      **Inheritance** produces flat JSON output. Deriving a schema from class `Derived` that extends `Base`:

      ```java
      static class Base {
          public String a;
      }

      static class Derived extends Base {
          public String b;
      }
      ```

      The JSON output has this flat structure:

      ```json
      {
        "a": "hello",
        "b": "world"
      }
      ```
    </Accordion>

    <Accordion title="Annotations (Jackson and Swagger)">
      You can use Jackson Databind annotations to enrich the JSON schema derived from your Java classes:

      ```java
      import com.fasterxml.jackson.annotation.JsonClassDescription;
      import com.fasterxml.jackson.annotation.JsonIgnore;
      import com.fasterxml.jackson.annotation.JsonPropertyDescription;

      static class Person {

        @JsonPropertyDescription("The first name and surname of the person")
        public String name;

        public int birthYear;

        @JsonPropertyDescription("The year the person died, or 'present' if the person is living.")
        public String deathYear;
      }

      @JsonClassDescription("The details of one published book")
      static class Book {

        public String title;
        public Person author;

        @JsonPropertyDescription("The year in which the book was first published.")
        public int publicationYear;

        @JsonIgnore
        public String genre;
      }

      static class BookList {
        public List<Book> books;
      }
      ```

      Annotation summary:

      * `@JsonClassDescription`: Add a description to a class
      * `@JsonPropertyDescription`: Add a description to a field or getter method
      * `@JsonIgnore`: Exclude a `public` field or getter from the schema
      * `@JsonProperty`: Include a non-`public` field or getter in the schema

      If you use `@JsonProperty(required = false)`, the SDK ignores the `false` value. Class-derived schemas always mark all properties as required.

      You can also use Swagger Core (OpenAPI 3) `@Schema` and `@ArraySchema` annotations for type-specific constraints:

      ```java
      import io.swagger.v3.oas.annotations.media.ArraySchema;
      import io.swagger.v3.oas.annotations.media.Schema;

      static class Article {

        @ArraySchema(minItems = 1)
        public List<String> authors;

        public String title;

        @Schema(format = "date")
        public String publicationDate;

        public int pageCount;
      }
      ```

      Local validation checks that you haven't used any unsupported constraint keywords, but constraint values aren't validated locally. For example, an unsupported `"format"` value may pass local validation but cause a remote error.

      If you use both Jackson and Swagger annotations to set the same schema field, the Jackson annotation takes precedence.
    </Accordion>

    <Accordion title="Defining schemas without a Java class">
      Class-based schema derivation is the most convenient path, but for direct control over the schema structure you can build a `JsonOutputFormat.Schema` manually and wrap it in an `OutputConfig`.

      ```java
      import com.anthropic.core.JsonValue;
      import com.anthropic.models.messages.JsonOutputFormat;
      // ...
      import com.anthropic.models.messages.OutputConfig;

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          JsonOutputFormat.Schema schema = JsonOutputFormat.Schema.builder()
              .putAdditionalProperty("type", JsonValue.from("object"))
              .putAdditionalProperty("properties", JsonValue.from(Map.of(
                  "name", Map.of("type", "string"),
                  "email", Map.of("type", "string"),
                  "plan_interest", Map.of("type", "string"))))
              .putAdditionalProperty("required", JsonValue.from(
                  List.of("name", "email", "plan_interest")))
              .putAdditionalProperty("additionalProperties", JsonValue.from(false))
              .build();

          OutputConfig outputConfig = OutputConfig.builder()
              .format(JsonOutputFormat.builder().schema(schema).build())
              .build();

          MessageCreateParams createParams = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024)
              .outputConfig(outputConfig)
              .addUserMessage(
                  "John Smith (john@example.com) is interested in our Enterprise plan.")
              .build();

          client.messages().create(createParams).content().stream()
              .flatMap(contentBlock -> contentBlock.text().stream())
              .forEach(textBlock -> IO.println(textBlock.text()));
      }
      ```

      For a more extensive example that builds a nested schema with arrays and descriptions, see [`StructuredOutputsRawExample.java`](https://github.com/anthropics/anthropic-sdk-java/blob/main/anthropic-java-example/src/main/java/com/anthropic/example/StructuredOutputsRawExample.java) in the SDK repository.
    </Accordion>
  </Tab>

  <Tab title="PHP">
    **Classes through the `StructuredOutputModel` interface**

    Define a PHP class implementing `StructuredOutputModel` (using `StructuredOutputModelTrait`) and pass the class name to `outputConfig: ['format' => MyClass::class]`. The SDK derives a JSON schema from your native PHP 8 property types and returns a typed instance through `$message->parsedOutput()`.

    `parsedOutput()` returns your model instance on success, or `null` (or an error array) if parsing fails. Use `instanceof` to narrow the type before accessing fields.

    ```php
    use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
    use Anthropic\Lib\Contracts\StructuredOutputModel;

    $client = new Client();

    class ContactInfo implements StructuredOutputModel
    {
        use StructuredOutputModelTrait;

        public string $name;
        public string $email;
        public string $plan_interest;
    }

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
        ],
        model: 'claude-opus-4-8',
        outputConfig: ['format' => ContactInfo::class],
    );

    $contact = $message->parsedOutput();
    if ($contact instanceof ContactInfo) {
        echo "{$contact->name} ({$contact->email})\n";
    }
    ```

    <Accordion title="Type inference">
      The SDK maps native PHP 8 property types to JSON Schema:

      | PHP type                                   | JSON Schema                        |
      | ------------------------------------------ | ---------------------------------- |
      | `string`                                   | `"string"`                         |
      | `int`                                      | `"integer"`                        |
      | `float`                                    | `"number"`                         |
      | `bool`                                     | `"boolean"`                        |
      | `array`                                    | `"array"` (see the following note) |
      | `?type` (nullable)                         | Optional field                     |
      | Class implementing `StructuredOutputModel` | Nested object                      |

      For `array` properties, the SDK adds an `items` schema only when the element type is a nested `StructuredOutputModel`, declared with `#[Constrained(itemClass: MyModel::class)]` or a `/** @var MyModel[] */` docblock. Arrays of scalars (`string[]`, `int[]`) emit an unconstrained `{"type":"array"}`.

      All non-nullable properties become required fields.
    </Accordion>

    <Accordion title="Constraints with the #[Constrained] attribute">
      Add constraints with the `#[Constrained]` attribute:

      ```php
      use Anthropic\Lib\Attributes\Constrained;
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      class Address implements StructuredOutputModel { use StructuredOutputModelTrait; public string $street; }

      class Profile implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          #[Constrained(description: 'Age in years', minimum: 0, maximum: 150)]
          public int $age;

          #[Constrained(format: 'email')]
          public string $email;

          #[Constrained(itemClass: Address::class, minItems: 1)]
          public array $addresses;
      }
      ```

      **API-enforced constraints** (sent in the schema): `description`, `format`, `const`, `itemClass`, `minItems` (0 or 1 only).

      **SDK-validated constraints** (stripped from the wire schema, appended to the description, and validated against the response): `minimum`, `maximum`, `multipleOf`, `minLength`, `maxLength`.
    </Accordion>

    <Accordion title="Raw JSON schema fallback">
      For schemas that PHP type hints can't express, pass a raw associative array through `OutputConfig::with()`. This path skips the `parsedOutput()` helper; decode the response with `json_decode()`:

      ```php
      use Anthropic\Messages\OutputConfig;
      use Anthropic\Messages\JSONOutputFormat;

      $client = new Client();

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Extract the key information from this email: John Smith (john@example.com) is interested in our Enterprise plan.'],
          ],
          model: 'claude-opus-4-8',
          outputConfig: OutputConfig::with(format: JSONOutputFormat::with(schema: [
              'type' => 'object',
              'properties' => [
                  'name' => ['type' => 'string'],
                  'email' => ['type' => 'string'],
                  'plan_interest' => ['type' => 'string'],
              ],
              'required' => ['name', 'email', 'plan_interest'],
              'additionalProperties' => false,
          ])),
      );

      $contact = json_decode($message->content[0]->text, associative: true);
      echo "{$contact['name']} ({$contact['email']})\n";
      ```
    </Accordion>
  </Tab>

  <Tab title="Ruby">
    **`output_config: {format: Model}` with `parsed_output`**

    Define a model class extending `Anthropic::BaseModel` and pass it as the format to `messages.create()`. The response includes a `parsed_output` attribute with a typed Ruby object.

    ```ruby
    class ContactInfo < Anthropic::BaseModel
      required :name, String
      required :email, String
      required :plan_interest, String
    end

    client = Anthropic::Client.new

    message = client.messages.create(
      model: "claude-opus-4-8",
      max_tokens: 1024,
      messages: [
        {
          role: "user",
          content: "Extract contact info: John Smith, john@example.com, interested in the Pro plan"
        }
      ],
      output_config: {format: ContactInfo}
    )

    contact = message.parsed_output
    puts "#{contact.name} (#{contact.email})"
    ```

    <Accordion title="Advanced model features">
      The Ruby SDK supports additional model definition features for richer schemas:

      * **`doc:` keyword:** Add descriptions to fields for more informative schema output
      * **`Anthropic::ArrayOf[T]`:** Typed arrays. Pass array-level constraints (`min_items:`, `max_items:`) as keywords on `required`/`optional`, not on `ArrayOf` itself
      * **`Anthropic::EnumOf[:a, :b]`:** Enum fields with constrained values
      * **`Anthropic::UnionOf[T1, T2]`:** Union types mapped to `anyOf`

      ```ruby
      class FamousNumber < Anthropic::BaseModel
        required :value, Float
        optional :reason, String, doc: "why is this number mathematically significant?"
      end

      class Output < Anthropic::BaseModel
        required :numbers, Anthropic::ArrayOf[FamousNumber], min_items: 3, max_items: 5
      end

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        messages: [{role: "user", content: "give me some famous numbers"}],
        output_config: {format: Output}
      )

      message.parsed_output
      # => #<Output numbers=[#<FamousNumber value=3.14159... reason="Pi is...">...]>
      ```
    </Accordion>
  </Tab>
</Tabs>

#### How SDK transformation works

The Python, TypeScript, Ruby, and PHP SDKs automatically transform schemas with unsupported features. The C# and Go SDKs apply the same transformations when the schema is derived from a native type (`Create<T>()` in C#; struct reflection or `BetaJSONSchemaOutputFormat()` on the Go beta API). The transformation steps:

1. **Remove unsupported constraints** (for example, `minimum`, `maximum`, `minLength`, `maxLength`)
2. **Update descriptions** with constraint info (for example, "Must be at least 100"), when the constraint is not directly supported with structured outputs
3. **Add `additionalProperties: false`** to all objects
4. **Filter string formats** to supported list only
5. **Validate responses** against your original schema (with all constraints)

This means Claude receives a simplified schema, but your code still enforces all constraints through validation.

**Example:** A Pydantic field with `minimum: 100` becomes a plain integer in the sent schema, but the SDK updates the description to "Must be at least 100" and validates the response against the original constraint.

### Common use cases

<AccordionGroup>
  <Accordion title="Data extraction">
    Extract structured data from unstructured text:

    <CodeGroup>
      ```bash CLI
      ant messages create \
        --transform 'content.0.text|@fromstr' \
        --format jsonl <<'YAML'
      model: claude-opus-4-8
      max_tokens: 4096
      messages:
        - role: user
          content: "Extract invoice data from: Invoice #12345, Date: 2024-01-15, Total: $500.00"
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              invoice_number: {type: string}
              date: {type: string}
              total_amount: {type: number}
              line_items:
                type: array
                items: {type: object, additionalProperties: false}
              customer_name: {type: string}
            required: [invoice_number, date, total_amount, line_items, customer_name]
            additionalProperties: false
      YAML
      ```

      ```python Python
      from pydantic import BaseModel


      class Invoice(BaseModel):
          invoice_number: str
          date: str
          total_amount: float
          line_items: list[dict]
          customer_name: str


      client = anthropic.Anthropic()
      invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      response = client.messages.parse(
          model="claude-opus-4-8",
          max_tokens=4096,
          output_format=Invoice,
          messages=[
              {"role": "user", "content": f"Extract invoice data from: {invoice_text}"}
          ],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const InvoiceSchema = z.object({
        invoice_number: z.string(),
        date: z.string(),
        total_amount: z.number(),
        line_items: z.array(z.record(z.string(), z.any())),
        customer_name: z.string()
      });

      const invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";
      const response = await client.messages.parse({
        model: "claude-opus-4-8",
        max_tokens: 4096,
        output_config: { format: zodOutputFormat(InvoiceSchema) },
        messages: [{ role: "user", content: `Extract invoice data from: ${invoiceText}` }]
      });
      console.log(response.parsed_output);
      ```

      ```csharp C#
      AnthropicClient client = new();

      string invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 4096,
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          invoice_number = new { type = "string" },
                          date = new { type = "string" },
                          total_amount = new { type = "number" },
                          line_items = new
                          {
                              type = "array",
                              items = new
                              {
                                  type = "object",
                                  additionalProperties = false,
                              },
                          },
                          customer_name = new { type = "string" },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "invoice_number", "date", "total_amount", "line_items", "customer_name" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
          Messages = [new() { Role = Role.User, Content = $"Extract invoice data from: {invoiceText}" }]
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      invoiceText := "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      schema := map[string]any{
      	"type":                 "object",
      	"additionalProperties": false,
      	"properties": map[string]any{
      		"invoice_number": map[string]any{"type": "string"},
      		"date":           map[string]any{"type": "string"},
      		"total_amount":   map[string]any{"type": "number"},
      		"line_items": map[string]any{
      			"type": "array",
      			"items": map[string]any{
      				"type":                 "object",
      				"additionalProperties": false,
      				"properties": map[string]any{
      					"description": map[string]any{"type": "string"},
      					"quantity":    map[string]any{"type": "number"},
      					"unit_price":  map[string]any{"type": "number"},
      				},
      				"required": []string{"description", "quantity", "unit_price"},
      			},
      		},
      		"customer_name": map[string]any{"type": "string"},
      	},
      	"required": []string{"invoice_number", "date", "total_amount", "line_items", "customer_name"},
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 4096,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: schema,
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Extract invoice data from: %s", invoiceText))),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		fmt.Println(variant.Text)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class LineItem {
          @JsonProperty("description")
          public String description;

          @JsonProperty("quantity")
          public int quantity;

          @JsonProperty("unit_price")
          public double unitPrice;
      }

      static class Invoice {
          @JsonProperty("invoice_number")
          public String invoiceNumber;

          @JsonProperty("date")
          public String date;

          @JsonProperty("total_amount")
          public double totalAmount;

          @JsonProperty("line_items")
          public List<LineItem> lineItems;

          @JsonProperty("customer_name")
          public String customerName;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

          StructuredMessageCreateParams<Invoice> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(4096L)
              .outputConfig(Invoice.class)
              .addUserMessage("Extract invoice data from: " + invoiceText)
              .build();

          StructuredMessage<Invoice> response = client.messages().create(params);
          Invoice invoice = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(invoice.invoiceNumber + ": $" + invoice.totalAmount);
      }
      ```

      ```php PHP
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Invoice implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $invoice_number;
          public string $date;
          public float $total_amount;
          public array $line_items;
          public string $customer_name;
      }

      $invoiceText = "Invoice #12345, Date: 2024-01-15, Total: $500.00";

      $message = $client->messages->create(
          maxTokens: 4096,
          messages: [
              ['role' => 'user', 'content' => "Extract invoice data from: $invoiceText"]
          ],
          model: 'claude-opus-4-8',
          outputConfig: ['format' => Invoice::class],
      );

      $invoice = $message->parsedOutput();
      if ($invoice instanceof Invoice) {
          echo "Invoice {$invoice->invoice_number}: \${$invoice->total_amount}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class LineItem < Anthropic::BaseModel
        required :description, String
        required :amount, Float
      end

      class Invoice < Anthropic::BaseModel
        required :invoice_number, String
        required :date, String
        required :total_amount, Float
        required :line_items, Anthropic::ArrayOf[LineItem]
        required :customer_name, String
      end

      invoice_text = "Invoice #12345, Date: 2024-01-15, Total: $500.00"

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 4096,
        output_config: {format: Invoice},
        messages: [
          {role: "user", content: "Extract invoice data from: #{invoice_text}"}
        ]
      )

      invoice = message.parsed_output
      puts "Invoice #{invoice.invoice_number}: $#{invoice.total_amount}"
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="Classification">
    Classify content with structured categories:

    <CodeGroup>
      ```bash CLI
      ant messages create \
        --transform 'content.0.text|@fromstr' \
        --format jsonl <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      messages:
        - role: user
          content: "Classify this feedback: Great product, fast shipping!"
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              category:
                type: string
              confidence:
                type: number
              tags:
                type: array
                items:
                  type: string
              sentiment:
                type: string
            required:
              - category
              - confidence
              - tags
              - sentiment
            additionalProperties: false
      YAML
      ```

      ```python Python
      from pydantic import BaseModel

      client = Anthropic()


      class Classification(BaseModel):
          category: str
          confidence: float
          tags: list[str]
          sentiment: str


      feedback_text = "Great product, but the delivery was slow."
      response = client.messages.parse(
          model="claude-opus-4-8",
          max_tokens=1024,
          output_format=Classification,
          messages=[{"role": "user", "content": f"Classify this feedback: {feedback_text}"}],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const ClassificationSchema = z.object({
        category: z.string(),
        confidence: z.number(),
        tags: z.array(z.string()),
        sentiment: z.string()
      });

      const feedbackText = "Great product, but the delivery was slow.";
      const response = await client.messages.parse({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(ClassificationSchema) },
        messages: [{ role: "user", content: `Classify this feedback: ${feedbackText}` }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      string feedbackText = "Great product, fast shipping!";

      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = $"Classify this feedback: {feedbackText}" }],
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          category = new { type = "string" },
                          confidence = new { type = "number" },
                          tags = new { type = "array", items = new { type = "string" } },
                          sentiment = new { type = "string" },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "category", "confidence", "tags", "sentiment" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      feedbackText := "Great product, fast shipping!"

      schema := map[string]any{
      	"type": "object",
      	"properties": map[string]any{
      		"category":   map[string]any{"type": "string"},
      		"confidence": map[string]any{"type": "number"},
      		"tags":       map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
      		"sentiment":  map[string]any{"type": "string"},
      	},
      	"required":             []string{"category", "confidence", "tags", "sentiment"},
      	"additionalProperties": false,
      }

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: schema,
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock(fmt.Sprintf("Classify this feedback: %s", feedbackText))),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		var result map[string]any
      		json.Unmarshal([]byte(variant.Text), &result)
      		fmt.Println(result)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class Classification {
          @JsonProperty("category")
          public String category;

          @JsonProperty("confidence")
          public double confidence;

          @JsonProperty("tags")
          public List<String> tags;

          @JsonProperty("sentiment")
          public String sentiment;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          String feedbackText = "Great product, fast shipping!";

          StructuredMessageCreateParams<Classification> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .outputConfig(Classification.class)
              .addUserMessage("Classify this feedback: " + feedbackText)
              .build();

          StructuredMessage<Classification> response = client.messages().create(params);
          Classification result = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(result.category + " (" + result.confidence + ")");
      }
      ```

      ```php PHP
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Classification implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $category;
          public float $confidence;
          public array $tags;
          public string $sentiment;
      }

      $feedbackText = "Great product, fast shipping!";

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => "Classify this feedback: {$feedbackText}"]
          ],
          model: 'claude-opus-4-8',
          outputConfig: ['format' => Classification::class],
      );

      $result = $message->parsedOutput();
      if ($result instanceof Classification) {
          echo "{$result->category} ({$result->confidence}): {$result->sentiment}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class Classification < Anthropic::BaseModel
        required :category, String
        required :confidence, Float
        required :tags, Anthropic::ArrayOf[String]
        required :sentiment, String
      end

      feedback_text = "Great product, fast shipping!"

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: {format: Classification},
        messages: [
          {role: "user", content: "Classify this feedback: #{feedback_text}"}
        ]
      )
      puts message.parsed_output
      ```
    </CodeGroup>
  </Accordion>

  <Accordion title="API response formatting">
    Generate API-ready responses:

    <CodeGroup>
      ```bash CLI
      ant messages create \
        --transform 'content.0.text' \
        --raw-output <<'YAML'
      model: claude-opus-4-8
      max_tokens: 1024
      output_config:
        format:
          type: json_schema
          schema:
            type: object
            properties:
              status:
                type: string
              data:
                type: object
                additionalProperties: false
              errors:
                type: array
                items:
                  type: object
                  additionalProperties: false
              metadata:
                type: object
                additionalProperties: false
            required:
              - status
              - data
              - metadata
            additionalProperties: false
      messages:
        - role: user
          content: "Process this request: ..."
      YAML
      ```

      ```python Python
      from pydantic import BaseModel

      client = Anthropic()


      class APIResponse(BaseModel):
          status: str
          data: dict
          errors: list[dict] | None
          metadata: dict


      response = client.messages.parse(
          model="claude-opus-4-8",
          max_tokens=1024,
          output_format=APIResponse,
          messages=[{"role": "user", "content": "Process this request: ..."}],
      )

      print(response.parsed_output)
      ```

      ```typescript TypeScript
      import { z } from "zod";
      import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";

      const client = new Anthropic();

      const APIResponseSchema = z.object({
        status: z.string(),
        data: z.record(z.string(), z.any()),
        errors: z.array(z.record(z.string(), z.any())).optional(),
        metadata: z.record(z.string(), z.any())
      });

      const response = await client.messages.parse({
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: { format: zodOutputFormat(APIResponseSchema) },
        messages: [{ role: "user", content: "Process this request..." }]
      });

      console.log(response.parsed_output);
      ```

      ```csharp C#
      var parameters = new MessageCreateParams
      {
          Model = Model.ClaudeOpus4_8,
          MaxTokens = 1024,
          Messages = [new() { Role = Role.User, Content = "Process this request: ..." }],
          OutputConfig = new OutputConfig
          {
              Format = new JsonOutputFormat
              {
                  Schema = new Dictionary<string, JsonElement>
                  {
                      ["type"] = JsonSerializer.SerializeToElement("object"),
                      ["properties"] = JsonSerializer.SerializeToElement(new
                      {
                          status = new { type = "string" },
                          data = new { type = "object", additionalProperties = false },
                          errors = new
                          {
                              type = "array",
                              items = new { type = "object", additionalProperties = false },
                          },
                          metadata = new { type = "object", additionalProperties = false },
                      }),
                      ["required"] = JsonSerializer.SerializeToElement(new[] { "status", "data", "metadata" }),
                      ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
                  },
              },
          },
      };

      var message = await client.Messages.Create(parameters);
      Console.WriteLine(message);
      ```

      ```go Go
      client := anthropic.NewClient()

      response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
      	Model:     anthropic.ModelClaudeOpus4_8,
      	MaxTokens: 1024,
      	OutputConfig: anthropic.OutputConfigParam{
      		Format: anthropic.JSONOutputFormatParam{
      			Schema: map[string]any{
      				"type":                 "object",
      				"additionalProperties": false,
      				"properties": map[string]any{
      					"status": map[string]any{
      						"type": "string",
      					},
      					"data": map[string]any{
      						"type":                 "object",
      						"additionalProperties": false,
      					},
      					"errors": map[string]any{
      						"type": "array",
      						"items": map[string]any{
      							"type":                 "object",
      							"additionalProperties": false,
      						},
      					},
      					"metadata": map[string]any{
      						"type":                 "object",
      						"additionalProperties": false,
      					},
      				},
      				"required": []string{"status", "data", "metadata"},
      			},
      		},
      	},
      	Messages: []anthropic.MessageParam{
      		anthropic.NewUserMessage(anthropic.NewTextBlock("Process this request: ...")),
      	},
      })
      if err != nil {
      	log.Fatal(err)
      }
      for _, block := range response.Content {
      	switch variant := block.AsAny().(type) {
      	case anthropic.TextBlock:
      		fmt.Println(variant.Text)
      	}
      }
      ```

      ```java Java
      import com.fasterxml.jackson.annotation.JsonProperty;

      static class APIData {
          @JsonProperty("message")
          public String message;

          @JsonProperty("resource_id")
          public String resourceId;
      }

      static class APIError {
          @JsonProperty("code")
          public String code;

          @JsonProperty("message")
          public String message;
      }

      static class APIMetadata {
          @JsonProperty("request_id")
          public String requestId;

          @JsonProperty("timestamp")
          public String timestamp;
      }

      static class APIResponse {
          @JsonProperty("status")
          public String status;

          @JsonProperty("data")
          public APIData data;

          @JsonProperty("errors")
          public List<APIError> errors;

          @JsonProperty("metadata")
          public APIMetadata metadata;
      }

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.fromEnv();

          StructuredMessageCreateParams<APIResponse> params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_4_8)
              .maxTokens(1024L)
              .outputConfig(APIResponse.class)
              .addUserMessage("Process this request: ...")
              .build();

          StructuredMessage<APIResponse> response = client.messages().create(params);
          APIResponse result = response.content().stream()
              .flatMap(block -> block.text().stream())
              .findFirst().orElseThrow().text();
          IO.println(result.status);
      }
      ```

      ```php PHP
      use Anthropic\Lib\Attributes\Constrained;
      use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
      use Anthropic\Lib\Contracts\StructuredOutputModel;

      $client = new Client();

      class Payload implements StructuredOutputModel { use StructuredOutputModelTrait; public string $message; }

      class APIError implements StructuredOutputModel { use StructuredOutputModelTrait; public string $code; public string $detail; }

      class Metadata implements StructuredOutputModel { use StructuredOutputModelTrait; public string $request_id; }

      class APIResponse implements StructuredOutputModel
      {
          use StructuredOutputModelTrait;

          public string $status;
          public Payload $data;
          #[Constrained(itemClass: APIError::class)]
          public ?array $errors;
          public Metadata $metadata;
      }

      $message = $client->messages->create(
          maxTokens: 1024,
          messages: [
              ['role' => 'user', 'content' => 'Process this request: ...']
          ],
          model: 'claude-opus-4-8',
          outputConfig: ['format' => APIResponse::class],
      );

      $result = $message->parsedOutput();
      if ($result instanceof APIResponse) {
          echo "{$result->status}: {$result->data->message}\n";
      }
      ```

      ```ruby Ruby
      client = Anthropic::Client.new

      class Payload < Anthropic::BaseModel
        required :message, String
      end

      class APIError < Anthropic::BaseModel
        required :code, String
        required :detail, String
      end

      class Metadata < Anthropic::BaseModel
        required :request_id, String
      end

      class APIResponse < Anthropic::BaseModel
        required :status, String
        required :data, Payload
        optional :errors, Anthropic::ArrayOf[APIError]
        required :metadata, Metadata
      end

      message = client.messages.create(
        model: "claude-opus-4-8",
        max_tokens: 1024,
        output_config: {format: APIResponse},
        messages: [
          {role: "user", content: "Process this request: ..."}
        ]
      )
      puts message.parsed_output
      ```
    </CodeGroup>
  </Accordion>
</AccordionGroup>

## Strict tool use

For enforcing JSON Schema compliance on tool inputs with grammar-constrained sampling, see [Strict tool use](/docs/en/agents-and-tools/tool-use/strict-tool-use).

## Using both features together

JSON outputs and strict tool use solve different problems and work together:

* **JSON outputs** control Claude's response format (what Claude says)
* **Strict tool use** validates tool parameters (how Claude calls your functions)

When combined, Claude can call tools with guaranteed-valid parameters AND return structured JSON responses. This is useful for agentic workflows where you need both reliable tool calls and structured final outputs.

<CodeGroup>
  ```bash CLI
  ant messages create <<'YAML'
  model: claude-opus-4-8
  max_tokens: 1024
  messages:
    - role: user
      content: Help me plan a trip to Paris departing May 15, 2026
  # JSON outputs: structured response format
  output_config:
    format:
      type: json_schema
      schema:
        type: object
        properties:
          summary:
            type: string
          next_steps:
            type: array
            items:
              type: string
        required: [summary, next_steps]
        additionalProperties: false
  # Strict tool use: guaranteed tool parameters
  tools:
    - name: search_flights
      strict: true
      input_schema:
        type: object
        properties:
          destination:
            type: string
          date:
            type: string
            format: date
        required: [destination, date]
        additionalProperties: false
  YAML
  ```

  ```python Python
  response = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[
          {
              "role": "user",
              "content": "Help me plan a trip to Paris departing May 15, 2026",
          }
      ],
      # JSON outputs: structured response format
      output_config={
          "format": {
              "type": "json_schema",
              "schema": {
                  "type": "object",
                  "properties": {
                      "summary": {"type": "string"},
                      "next_steps": {"type": "array", "items": {"type": "string"}},
                  },
                  "required": ["summary", "next_steps"],
                  "additionalProperties": False,
              },
          }
      },
      # Strict tool use: guaranteed tool parameters
      tools=[
          {
              "name": "search_flights",
              "strict": True,
              "input_schema": {
                  "type": "object",
                  "properties": {
                      "destination": {"type": "string"},
                      "date": {"type": "string", "format": "date"},
                  },
                  "required": ["destination", "date"],
                  "additionalProperties": False,
              },
          }
      ],
  )

  print(response)
  ```

  ```typescript TypeScript
  const response = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Help me plan a trip to Paris departing May 15, 2026" }],
    // JSON outputs: structured response format
    output_config: {
      format: {
        type: "json_schema",
        schema: {
          type: "object",
          properties: {
            summary: { type: "string" },
            next_steps: { type: "array", items: { type: "string" } }
          },
          required: ["summary", "next_steps"],
          additionalProperties: false
        }
      }
    },
    // Strict tool use: guaranteed tool parameters
    tools: [
      {
        name: "search_flights",
        description: "Search for available flights to a destination on a specific date",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: { type: "string" },
            date: { type: "string", format: "date" }
          },
          required: ["destination", "date"],
          additionalProperties: false
        }
      }
    ]
  });

  // Claude may call the tool first (tool_use) or respond with JSON (text)
  console.log("Stop reason:", response.stop_reason);
  for (const block of response.content) {
    if (block.type === "tool_use") {
      console.log(`Tool call: ${block.name}(${JSON.stringify(block.input)})`);
    } else if (block.type === "text") {
      console.log("Response:", block.text);
    }
  }
  ```

  ```csharp C#
  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Help me plan a trip to Paris departing May 15, 2026" }],
      // JSON outputs: structured response format
      OutputConfig = new OutputConfig
      {
          Format = new JsonOutputFormat
          {
              Schema = new Dictionary<string, JsonElement>
              {
                  ["type"] = JsonSerializer.SerializeToElement("object"),
                  ["properties"] = JsonSerializer.SerializeToElement(new
                  {
                      summary = new { type = "string" },
                      next_steps = new { type = "array", items = new { type = "string" } },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "summary", "next_steps" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              },
          },
      },
      // Strict tool use: guaranteed tool parameters
      Tools =
      [
          new Tool
          {
              Name = "search_flights",
              Strict = true,
              InputSchema = new InputSchema(new Dictionary<string, JsonElement>
              {
                  ["properties"] = JsonSerializer.SerializeToElement(new Dictionary<string, object>
                  {
                      ["destination"] = new { type = "string" },
                      ["date"] = new { type = "string", format = "date" },
                  }),
                  ["required"] = JsonSerializer.SerializeToElement(new[] { "destination", "date" }),
                  ["additionalProperties"] = JsonSerializer.SerializeToElement(false),
              }),
          }
      ],
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  client := anthropic.NewClient()

  response, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeOpus4_8,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Help me plan a trip to Paris departing May 15, 2026")),
  	},
  	// JSON outputs: structured response format
  	OutputConfig: anthropic.OutputConfigParam{
  		Format: anthropic.JSONOutputFormatParam{
  			Schema: map[string]any{
  				"type":                 "object",
  				"additionalProperties": false,
  				"properties": map[string]any{
  					"summary":    map[string]any{"type": "string"},
  					"next_steps": map[string]any{"type": "array", "items": map[string]any{"type": "string"}},
  				},
  				"required": []string{"summary", "next_steps"},
  			},
  		},
  	},
  	// Strict tool use: guaranteed tool parameters
  	Tools: []anthropic.ToolUnionParam{
  		{OfTool: &anthropic.ToolParam{
  			Name:   "search_flights",
  			Strict: anthropic.Bool(true),
  			InputSchema: anthropic.ToolInputSchemaParam{
  				Properties: map[string]any{
  					"destination": map[string]any{"type": "string"},
  					"date":        map[string]any{"type": "string", "format": "date"},
  				},
  				Required: []string{"destination", "date"},
  				ExtraFields: map[string]any{
  					"additionalProperties": false,
  				},
  			}}},
  	},
  })
  if err != nil {
  	log.Fatal(err)
  }
  fmt.Println(response.Content)
  ```

  ```java Java
  AnthropicClient client = AnthropicOkHttpClient.fromEnv();

  // JSON outputs: structured response format
  JsonOutputFormat.Schema outputSchema = JsonOutputFormat.Schema.builder()
      .putAdditionalProperty("type", JsonValue.from("object"))
      .putAdditionalProperty("properties", JsonValue.from(Map.of(
          "summary", Map.of("type", "string"),
          "next_steps", Map.of("type", "array", "items", Map.of("type", "string"))
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("summary", "next_steps")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  // Strict tool use: guaranteed tool parameters
  InputSchema toolSchema = InputSchema.builder()
      .properties(JsonValue.from(Map.of(
          "destination", Map.of("type", "string"),
          "date", Map.of("type", "string", "format", "date")
      )))
      .putAdditionalProperty("required", JsonValue.from(List.of("destination", "date")))
      .putAdditionalProperty("additionalProperties", JsonValue.from(false))
      .build();

  MessageCreateParams params = MessageCreateParams.builder()
      .model(Model.CLAUDE_OPUS_4_8)
      .maxTokens(1024L)
      .addUserMessage("Help me plan a trip to Paris departing May 15, 2026")
      .outputConfig(OutputConfig.builder()
          .format(JsonOutputFormat.builder().schema(outputSchema).build())
          .build())
      .addTool(Tool.builder()
          .name("search_flights")
          .description("Search for available flights to a destination on a specific date")
          .strict(true)
          .inputSchema(toolSchema)
          .build())
      .build();

  Message response = client.messages().create(params);
  IO.println(response);
  ```

  ```php PHP
  use Anthropic\Lib\Concerns\StructuredOutputModelTrait;
  use Anthropic\Lib\Contracts\StructuredOutputModel;
  use Anthropic\Messages\ToolUseBlock;

  $client = new Client();

  class TripPlan implements StructuredOutputModel
  {
      use StructuredOutputModelTrait;

      public string $summary;
      public array $next_steps;
  }

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Help me plan a trip to Paris departing May 15, 2026']
      ],
      model: 'claude-opus-4-8',
      // JSON outputs: structured response format
      outputConfig: ['format' => TripPlan::class],
      // Strict tool use: guaranteed tool parameters
      tools: [
          [
              'name' => 'search_flights',
              'strict' => true,
              'input_schema' => [
                  'type' => 'object',
                  'properties' => [
                      'destination' => ['type' => 'string'],
                      'date' => ['type' => 'string', 'format' => 'date']
                  ],
                  'required' => ['destination', 'date'],
                  'additionalProperties' => false
              ]
          ]
      ],
  );

  // Claude may call the tool first (tool_use) or respond with JSON (text)
  $plan = $message->parsedOutput();
  if ($plan instanceof TripPlan) {
      echo $plan->summary, "\n";
  } elseif ($toolUse = array_find($message->content, fn($block) => $block instanceof ToolUseBlock)) {
      echo "Tool call: {$toolUse->name}(", json_encode($toolUse->input), ")\n";
  }
  ```

  ```ruby Ruby
  client = Anthropic::Client.new

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [
      {role: "user", content: "Help me plan a trip to Paris departing May 15, 2026"}
    ],
    # JSON outputs: structured response format
    output_config: {
      format: {
        type: :json_schema,
        schema: {
          type: "object",
          properties: {
            summary: {type: "string"},
            next_steps: {type: "array", items: {type: "string"}}
          },
          required: ["summary", "next_steps"],
          additionalProperties: false
        }
      }
    },
    # Strict tool use: guaranteed tool parameters
    tools: [
      {
        name: "search_flights",
        strict: true,
        input_schema: {
          type: "object",
          properties: {
            destination: {type: "string"},
            date: {type: "string", format: "date"}
          },
          required: ["destination", "date"],
          additionalProperties: false
        }
      }
    ]
  )
  puts message
  ```
</CodeGroup>

## Important considerations

### Grammar compilation and caching

Structured outputs use constrained sampling with compiled grammar artifacts. This introduces some performance characteristics to be aware of:

* **First request latency:** The first time you use a specific schema, there is additional latency while the grammar compiles

* **Automatic caching:** Compiled grammars are cached for 24 hours from last use, making subsequent requests much faster

* **Cache invalidation:** The cache is invalidated if you change:

  * The JSON schema structure
  * The set of tools in your request (when using both structured outputs and tool use)
  * Changing only `name` or `description` fields does not invalidate the cache

### Prompt modification and token costs

When using structured outputs, Claude automatically receives an additional system prompt explaining the expected output format. This means:

* Your input token count is slightly higher
* The injected prompt costs you tokens like any other system prompt
* Changing the `output_config.format` parameter will invalidate any [prompt cache](/docs/en/build-with-claude/prompt-caching) for that conversation thread

### JSON Schema limitations

Structured outputs support standard JSON Schema with some limitations. Both JSON outputs and strict tool use share these limitations.

<Accordion title="Supported features">
  * All basic types: object, array, string, integer, number, boolean, null
  * `enum` (strings, numbers, bools, or nulls only - no complex types; see [Invalid outputs](#invalid-outputs) for a capitalization caveat)
  * `const`
  * `anyOf` and `allOf` (with limitations - `allOf` with `$ref` not supported)
  * `$ref`, `$def`, and `definitions` (external `$ref` not supported)
  * `default` property for all supported types
  * `required` and `additionalProperties` (must be set to `false` for objects)
  * String formats: `date-time`, `time`, `date`, `duration`, `email`, `hostname`, `uri`, `ipv4`, `ipv6`, `uuid`
  * Array `minItems` (only values 0 and 1 supported)
</Accordion>

<Accordion title="Not supported">
  * Recursive schemas
  * Complex types within enums
  * External `$ref` (for example, `'$ref': 'http://...'`)
  * Numerical constraints (such as `minimum`, `maximum`, `multipleOf`)
  * String constraints (`minLength`, `maxLength`)
  * Array constraints beyond `minItems` of 0 or 1
  * `additionalProperties` set to anything other than `false`

  If you use an unsupported feature, you'll receive a 400 error with details.
</Accordion>

<Accordion title="Pattern support (regex)">
  **Supported regex features:**

  * Full matching (`^...$`) and partial matching
  * Quantifiers: `*`, `+`, `?`, simple `{n,m}` cases
  * Character classes: `[]`, `.`, `\d`, `\w`, `\s`
  * Groups: `(...)`

  **NOT supported:**

  * Backreferences to groups (for example, `\1`, `\2`)
  * Lookahead/lookbehind assertions (for example, `(?=...)`, `(?!...)`)
  * Word boundaries: `\b`, `\B`
  * Complex `{n,m}` quantifiers with large ranges

  Simple regex patterns work well. Complex patterns may result in 400 errors.
</Accordion>

<Tip>
  The Python, TypeScript, Ruby, and PHP SDKs can automatically transform schemas with unsupported features by removing them and adding constraints to field descriptions. The C# and Go SDKs do the same when the schema is derived from a native type. See [SDK-specific methods](#sdk-specific-methods) for details.
</Tip>

### Property ordering

When using structured outputs, properties in objects maintain their defined ordering from your schema, with one important caveat: **required properties appear first, followed by optional properties**.

For example, given this schema:

```json
{
  "type": "object",
  "properties": {
    "notes": { "type": "string" },
    "name": { "type": "string" },
    "email": { "type": "string" },
    "age": { "type": "integer" }
  },
  "required": ["name", "email"],
  "additionalProperties": false
}
```

The output will order properties as:

1. `name` (required, in schema order)
2. `email` (required, in schema order)
3. `notes` (optional, in schema order)
4. `age` (optional, in schema order)

This means the output might look like:

```json
{
  "name": "John Smith",
  "email": "john@example.com",
  "notes": "Interested in enterprise plan",
  "age": 35
}
```

If property order in the output is important to your application, mark all properties as required, or account for this reordering in your parsing logic.

### Invalid outputs

While structured outputs guarantee schema compliance in most cases, there are scenarios where the output may not match your schema:

**Refusals** (`stop_reason: "refusal"`)

Claude maintains its safety and helpfulness properties even when using structured outputs. If Claude refuses a request for safety reasons:

* The response has `stop_reason: "refusal"`
* You'll receive a 200 status code
* You'll be billed for the tokens generated
* The output may not match your schema because the refusal message takes precedence over schema constraints

**Token limit reached** (`stop_reason: "max_tokens"`)

If the response is cut off due to reaching the `max_tokens` limit:

* The response has `stop_reason: "max_tokens"`
* The output may be incomplete and not match your schema
* Retry with a higher `max_tokens` value to get the complete structured output

**Enum value casing**

Structured outputs don't guarantee the capitalization of string `enum` and `const` values: Claude may return a value that differs from your schema only in capitalization, typically in the first letter of a word following a space. For example, given this schema:

```json
{
  "type": "string",
  "enum": ["Conversation Topic 1", "Conversation Topic 2", "Conversation topic 3"]
}
```

The output may contain `"Conversation Topic 3"` (capital "T") even though that exact value isn't in the enum. The response completes normally, with no error and no special `stop_reason`. This applies to both JSON outputs and strict tool use. Compare enum values case-insensitively, and avoid enum values that differ only in capitalization.

### Schema complexity limits

Structured outputs work by compiling your JSON schemas into a grammar that constrains Claude's output. More complex schemas produce larger grammars that take longer to compile. To protect against excessive compilation times, the API enforces several complexity limits.

#### Explicit limits

The following limits apply to all requests with `output_config.format` or `strict: true`:

| Limit                       | Value | Description                                                                                                                                                                                              |
| --------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Strict tools per request    | 20    | Maximum number of tools with `strict: true`. Non-strict tools don't count toward this limit.                                                                                                             |
| Optional parameters         | 24    | Total optional parameters across all strict tool schemas and JSON output schemas. Each parameter not listed in `required` counts toward this limit.                                                      |
| Parameters with union types | 16    | Total parameters that use `anyOf` or type arrays (for example, `"type": ["string", "null"]`) across all strict schemas. These are especially expensive because they create exponential compilation cost. |

<Note>
  These limits apply to the combined total across all strict schemas in a single request. For example, if you have 4 strict tools with 6 optional parameters each, you'll reach the 24-parameter limit even though no single tool seems complex.
</Note>

#### Additional internal limits

Beyond the explicit limits in the preceding table, there are additional internal limits on the compiled grammar size. These limits exist because schema complexity doesn't reduce to a single dimension: features like optional parameters, union types, nested objects, and number of tools interact with each other in ways that can make the compiled grammar disproportionately large.

When these limits are exceeded, you'll receive a 400 error with the message "Schema is too complex for compilation." These errors mean the combined complexity of your schemas exceeds what can be efficiently compiled, even if each individual limit in the preceding table is satisfied. As a final stop-gap, the API also enforces a **compilation timeout of 180 seconds**. Schemas that pass all explicit checks but produce very large compiled grammars may hit this timeout.

#### Tips for reducing schema complexity

If you're hitting complexity limits, try these strategies in order:

1. **Mark only critical tools as strict.** If you have many tools, reserve it for tools where schema violations cause real problems, and rely on Claude's natural adherence for simpler tools.

2. **Reduce optional parameters.** Make parameters `required` where possible. Each optional parameter roughly doubles a portion of the grammar's state space. If a parameter always has a reasonable default, consider making it required and having Claude provide that default explicitly.

3. **Simplify nested structures.** Deeply nested objects with optional fields compound the complexity. Flatten structures where possible.

4. **Split into multiple requests.** If you have many strict tools, consider splitting them across separate requests or sub-agents.

For persistent issues with valid schemas, [contact support](https://support.claude.com/en/articles/9015913-how-to-get-support) with your schema definition.

## Data retention

Prompts and responses are processed with ZDR when using structured outputs. However, the JSON schema itself is temporarily cached for up to 24 hours since last use for optimization purposes. No prompt or response data is retained beyond the API response.

Structured outputs are HIPAA eligible, but **PHI must not be included in JSON schema definitions**. The API compiles JSON schemas into grammars that are cached separately from message content, and these cached schemas do not receive the same PHI protections as prompts and responses. Do not include PHI in schema property names, `enum` values, `const` values, or `pattern` regular expressions. PHI should only appear in message content (prompts and responses), where it is protected under HIPAA safeguards.

For ZDR and HIPAA eligibility across all features, see [API and data retention](/docs/en/manage-claude/api-and-data-retention).

## Feature compatibility

**Works with:**

* **[Batch processing](/docs/en/build-with-claude/batch-processing):** Process structured outputs at scale with 50% discount
* **[Token counting](/docs/en/build-with-claude/token-counting):** Count tokens without compilation
* **[Streaming](/docs/en/build-with-claude/streaming):** Stream structured outputs like normal responses
* **Combined usage:** Use JSON outputs (`output_config.format`) and strict tool use (`strict: true`) together in the same request

**Incompatible with:**

* **[Citations](/docs/en/build-with-claude/citations):** Citations require interleaving citation blocks with text, which conflicts with strict JSON schema constraints. Returns 400 error if citations enabled with `output_config.format`.
* **Message Prefilling:** Incompatible with JSON outputs

<Tip>
  **Grammar scope:** Grammars apply only to Claude's direct output, not to tool use calls, tool results, or thinking tags (when using [Extended Thinking](/docs/en/build-with-claude/extended-thinking)). Grammar state resets between sections, allowing Claude to think freely while still producing structured output in the final response.
</Tip>

## Next steps

<CardGroup cols={2}>
  <Card title="Citations" icon="book-bookmark" href="/docs/en/build-with-claude/citations">
    Have Claude cite its sources when answering questions about provided documents.
  </Card>

  <Card title="Strict tool use" icon="check" href="/docs/en/agents-and-tools/tool-use/strict-tool-use">
    Enforce JSON Schema compliance on Claude's tool inputs with grammar-constrained sampling.
  </Card>

  <Card title="Tool use with Claude" icon="wrench" href="/docs/en/agents-and-tools/tool-use/overview">
    Connect Claude to external tools and APIs. Learn where tools execute and how the agentic loop works.
  </Card>

  <Card title="Pricing" icon="calculator" href="/docs/en/about-claude/pricing">
    Learn about Anthropic's pricing structure for models and features.
  </Card>
</CardGroup>
