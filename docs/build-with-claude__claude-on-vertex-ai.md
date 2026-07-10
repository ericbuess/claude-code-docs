# Claude on Google Cloud

Anthropic's Claude models are available through [Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai).

---

The API for accessing Claude on Google Cloud's Agent Platform is nearly identical to the [Messages API](/docs/en/api/messages/create), with two key differences in request format:

* On Agent Platform, `model` is not passed in the request body. Instead, it is specified in the Google Cloud endpoint URL.
* On Agent Platform, `anthropic_version` is passed in the request body (rather than as a header), and must be set to the value `vertex-2023-10-16`.

Agent Platform is also supported by Anthropic's official [client SDKs](/docs/en/cli-sdks-libraries/overview). This guide walks you through making a request to Claude on Agent Platform using one of Anthropic's client SDKs.

Note that this guide assumes you already have a Google Cloud project that is able to use Agent Platform. See [Anthropic Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) for more information on the setup required and a full walkthrough.

## Install an SDK for accessing Agent Platform

First, install Anthropic's [client SDK](/docs/en/cli-sdks-libraries/overview) for your language of choice.

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U google-cloud-aiplatform "anthropic[vertex]"
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/vertex-sdk
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Vertex
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="Java">
    <CodeGroup>
      ```groovy Gradle
      implementation("com.anthropic:anthropic-java-vertex:2.47.1")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-vertex</artifactId>
          <version>2.47.1</version>
      </dependency>
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.vertex.backends.VertexBackend;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.Model;
      // ...
              AnthropicClient client = AnthropicOkHttpClient.builder()
                  .backend(VertexBackend.fromEnv())
                  .build();

              MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_8)
                  .maxTokens(1024L)
                  .addUserMessage("What is the capital of France?")
                  .build();

              Message response = client.messages().create(params);
              response.content().stream()
                  .flatMap(block -> block.text().stream())
                  .forEach(textBlock -> System.out.println(textBlock.text()));
      ```
    </CodeGroup>
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk google/auth
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    # Gemfile
    gem "anthropic"
    gem "googleauth"
    ```
  </Tab>
</Tabs>

## Accessing Agent Platform

### Model availability

Note that Anthropic model availability varies by region. Search for "Claude" in the [Model Garden](https://cloud.google.com/model-garden) or go to [Anthropic Claude models](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) for the latest information.

#### API model IDs

Lifecycle terms (Deprecated, Retired) are defined in [Model deprecations](/docs/en/about-claude/model-deprecations). Lifecycle dates on partner-operated platforms are set by the partner and can differ from the Claude API schedule. For the current retirement date of any model on Agent Platform, see [Google Cloud's documentation for Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude).

| Model                        | Agent Platform API model ID |
| ---------------------------- | --------------------------- |
| Claude Fable 5               | claude-fable-5              |
| Claude Opus 4.8              | claude-opus-4-8             |
| Claude Opus 4.7              | claude-opus-4-7             |
| Claude Opus 4.6              | claude-opus-4-6             |
| Claude Sonnet 5              | `claude-sonnet-5`           |
| Claude Sonnet 4.6            | claude-sonnet-4-6           |
| Claude Sonnet 4.5            | claude-sonnet-4-5\@20250929 |
| Claude Sonnet 4 Deprecated.  | claude-sonnet-4\@20250514   |
| Claude Sonnet 3.7 Retired.   | claude-3-7-sonnet\@20250219 |
| Claude Opus 4.5              | claude-opus-4-5\@20251101   |
| Claude Opus 4.1 Deprecated.  | claude-opus-4-1\@20250805   |
| Claude Opus 4 Deprecated.    | claude-opus-4\@20250514     |
| Claude Haiku 4.5             | claude-haiku-4-5\@20251001  |
| Claude Haiku 3.5 Deprecated. | claude-3-5-haiku\@20241022  |

<Tip>
  Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform. See [Migrating to a newer Claude model](/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

### Making requests

Before running requests you may need to run `gcloud auth application-default login` to authenticate with Google Cloud.

The following examples show how to generate text from Claude on Agent Platform:

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-4-8
  LOCATION=global
  PROJECT_ID=MY_PROJECT_ID

  curl \
  -X POST \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  https://$LOCATION-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/anthropic/models/${MODEL_ID}:streamRawPredict -d \
  '{
    "anthropic_version": "vertex-2023-10-16",
    "messages": [{
      "role": "user",
      "content": "Hey Claude!"
    }],
    "max_tokens": 100
  }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "global";

  // Goes through the standard `google-auth-library` flow.
  const client = new AnthropicVertex({
    projectId,
    region
  });

  async function main() {
    const result = await client.messages.create({
      model: "claude-opus-4-8",
      max_tokens: 100,
      messages: [
        {
          role: "user",
          content: "Hey Claude!"
        }
      ]
    });
    console.log(JSON.stringify(result, null, 2));
  }

  main();
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicClient
  {
      Backend = new VertexBackend(projectId, region)
  };

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"
  	"fmt"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Uses default Google Cloud credentials
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Printf("%+v\n", message)
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;
  // ...
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
        .backend(VertexBackend.fromEnv())
        .build();

      Message message = client
        .messages()
        .create(
          MessageCreateParams.builder()
            .model("claude-opus-4-8")
            .maxTokens(100)
            .addUserMessage("Hey Claude!")
            .build()
        );

      System.out.println(message);
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      location: 'global',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

See the [client SDKs](/docs/en/cli-sdks-libraries/overview) and the official [Agent Platform docs](https://cloud.google.com/vertex-ai/docs) for more details.

Claude is also available through [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry).

## Data retention

Data handling for this offering is governed by Google Cloud. For details, see [Agent Platform and zero data retention](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance).

## Activity logging

Agent Platform provides a [request-response logging service](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) that allows customers to log the prompts and completions associated with your usage.

Anthropic recommends that you log your activity on at least a 30-day rolling basis in order to understand your activity and investigate any potential misuse.

<Note>
  Turning on this service does not give Google or Anthropic any access to your content.
</Note>

## Feature support

For the full feature list with Google Cloud availability, see [Features overview](/docs/en/build-with-claude/overview).

### Supported feature highlights

* [Messages API](/docs/en/api/messages/create)
* [Prompt caching](/docs/en/build-with-claude/prompt-caching)
* [Extended thinking](/docs/en/build-with-claude/extended-thinking)
* [Tool use](/docs/en/agents-and-tools/tool-use/overview), including the [Bash tool](/docs/en/agents-and-tools/tool-use/bash-tool), [Computer use tool](/docs/en/agents-and-tools/tool-use/computer-use-tool), [Memory tool](/docs/en/agents-and-tools/tool-use/memory-tool), and [Text editor tool](/docs/en/agents-and-tools/tool-use/text-editor-tool)
* [Web search tool](/docs/en/agents-and-tools/tool-use/web-search-tool)
* [Citations](/docs/en/build-with-claude/citations)
* [Structured outputs](/docs/en/build-with-claude/structured-outputs)

### Features not supported

* Input sources (URL sources for images and documents, Files API)
* Server-side tools (code execution, web fetch, advisor)
* Agent infrastructure (Agent Skills, MCP connector, programmatic tool calling)
* API endpoints (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Server-side fallback (the [`fallbacks` parameter](/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback); use the [client-side fallback pattern](/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead)

### Context window

Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, and Claude Sonnet 4.6 have a [1M-token context window](/docs/en/build-with-claude/context-windows) on Agent Platform. Other Claude models, including Sonnet 4.5 and Sonnet 4 (deprecated), have a 200k-token context window.

Agent Platform limits request payloads to 30 MB. When sending large documents or many images, you may reach this limit before the token limit.

## Global, multi-region, and regional endpoints

Agent Platform offers three endpoint types:

* **Global endpoints:** Dynamic routing for maximum availability
* **Multi-region endpoints:** Dynamic routing within a geographic area (for example, the United States or the European Union) for data residency with high availability
* **Regional endpoints:** Guaranteed data routing through specific geographic regions

Regional and multi-region endpoints include a 10% pricing premium over global endpoints.

<Note>
  This applies to Claude Sonnet 4.5 and future models only. Older models (Claude Sonnet 4 (deprecated), Opus 4 (deprecated), and earlier) maintain their existing pricing structures.
</Note>

### When to use each option

**Global endpoints (recommended):**

* Provide maximum availability and uptime
* Dynamically route requests to regions with available capacity
* No pricing premium
* Best for applications where data residency is flexible
* Only supports pay-as-you-go traffic (provisioned throughput requires regional endpoints)

**Multi-region endpoints:**

* Dynamically route requests across regions within a geographic area (currently `us` and `eu`)
* Useful when you need data residency within a broad geography but want higher availability than a single region
* 10% pricing premium over global endpoints
* Only supports pay-as-you-go traffic (provisioned throughput requires regional endpoints)

**Regional endpoints:**

* Route traffic through specific geographic regions
* Required for single-region data residency, strict compliance mandates, or provisioned throughput
* Support both pay-as-you-go and provisioned throughput
* 10% pricing premium reflects infrastructure costs for dedicated regional capacity

### Implementation

**Using global endpoints (recommended):**

Set the `region` parameter to `"global"` when initializing the client:

<CodeGroup>
  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "global"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "global";

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicClient
  {
      Backend = new VertexBackend(projectId, region)
  };

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Uses default Google Cloud credentials
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "global", "MY_PROJECT_ID"),
  	)

  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	_ = message
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .region("global")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model("claude-opus-4-8")
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      location: 'global',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-4-8',
  );

  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

**Using multi-region endpoints:**

Set the `region` parameter to a multi-region identifier: `"us"` for the United States or `"eu"` for the European Union. The SDK routes requests to the corresponding multi-region endpoint (`https://aiplatform.us.rep.googleapis.com` or `https://aiplatform.eu.rep.googleapis.com`), which dynamically balances traffic across regions within that geography.

<CodeGroup>
  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us"  # Multi-region identifier: "us" or "eu"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "us"; // Multi-region identifier: "us" or "eu"

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us"; // Multi-region identifier: "us" or "eu"

  var client = new AnthropicClient
  {
      Backend = new VertexBackend(projectId, region)
  };

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Multi-region identifier: "us" or "eu"
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us", "MY_PROJECT_ID"),
  	)

  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	_ = message
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Multi-region identifier: "us" or "eu"
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .region("us")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model("claude-opus-4-8")
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      location: 'us', // Multi-region identifier: "us" or "eu"
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us", # Multi-region identifier: "us" or "eu"
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

**Using regional endpoints:**

Specify a specific region like `"us-east1"` or `"europe-west1"`:

<CodeGroup>
  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us-east1"  # Specify a specific region

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=100,
      messages=[
          {
              "role": "user",
              "content": "Hey Claude!",
          }
      ],
  )
  print(message)
  ```

  ```typescript TypeScript
  import { AnthropicVertex } from "@anthropic-ai/vertex-sdk";

  const projectId = "MY_PROJECT_ID";
  const region = "us-east1"; // Specify a specific region

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us-east1";

  AnthropicClient client = new()
  {
      Backend = new VertexBackend(projectId, region)
  };

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus4_8,
      MaxTokens = 100,
      Messages = [new() { Role = Role.User, Content = "Hey Claude!" }]
  };

  var message = await client.Messages.Create(parameters);
  Console.WriteLine(message);
  ```

  ```go Go
  import (
  	"context"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/vertex"
  )
  // ...
  	// Specify a specific region
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us-east1", "MY_PROJECT_ID"),
  	)

  	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 100,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hey Claude!")),
  		},
  	})
  	_ = message
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Uses default Google Cloud credentials with specific region
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .region("us-east1") // Specify a specific region
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model("claude-opus-4-8")
                  .maxTokens(100)
                  .addUserMessage("Hey Claude!")
                  .build()
          );

      IO.println(message);
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Vertex;

  $client = Vertex\Client::fromEnvironment(
      location: 'us-east1',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us-east1", # Specify a specific region
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

<Note>
  Claude Mythos Preview is a research preview available to invited customers on Agent Platform. For more information, see [Project Glasswing](https://anthropic.com/glasswing).
</Note>

## Additional resources

* **Agent Platform pricing:** [Generative AI pricing on cloud.google.com](https://cloud.google.com/vertex-ai/generative-ai/pricing)
* **Claude models documentation:** [Claude on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude)
* **Google blog post:** [Global endpoint for Claude models](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai)
* **Anthropic pricing details:** [Cloud platform pricing](/docs/en/about-claude/pricing#cloud-platform-pricing)
