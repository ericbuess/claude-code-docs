---
title: Claude on Google Cloud
url: https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai
description: Anthropic's Claude models are available through [Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai).
---

The API for accessing Claude on Google Cloud's Agent Platform is nearly identical to the [Messages API](https://platform.claude.com/docs/en/api/messages/create), with two key differences in request format:

* On Agent Platform, `model` is not passed in the request body. Instead, it is specified in the Google Cloud endpoint URL.
* On Agent Platform, `anthropic_version` is passed in the request body (rather than as a header), and must be set to the value `vertex-2023-10-16`.

Agent Platform is also supported by Anthropic's official [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview). This guide walks you through making a request to Claude on Agent Platform using one of Anthropic's client SDKs.

Note that this guide assumes you already have a Google Cloud project that is able to use Agent Platform. See [Anthropic Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude) for more information on the setup required and a full walkthrough.

## Install an SDK for accessing Agent Platform

First, install Anthropic's [client SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) for your language of choice.

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[vertex]"
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
    <CodeGroup exclude="shell, python, typescript, csharp, go, php, ruby">
      ```groovy Gradle
      implementation("com.anthropic:anthropic-java:2.57.0")
      implementation("com.anthropic:anthropic-java-vertex:2.57.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java</artifactId>
          <version>2.57.0</version>
      </dependency>
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-vertex</artifactId>
          <version>2.57.0</version>
      </dependency>
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Model;
      import com.anthropic.vertex.backends.VertexBackend;

      void main() {
          AnthropicClient client = AnthropicOkHttpClient.builder()
              .backend(VertexBackend.fromEnv())
              .build();

          MessageCreateParams params = MessageCreateParams.builder()
              .model(Model.CLAUDE_OPUS_5)
              .maxTokens(1024L)
              .addUserMessage("What is the capital of France?")
              .build();

          Message response = client.messages().create(params);
          response.content().stream()
              .flatMap(block -> block.text().stream())
              .forEach(textBlock -> IO.println(textBlock.text()));
      }
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

Lifecycle terms (Deprecated, Retired) are defined in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations). Lifecycle dates on partner-operated platforms are set by the partner and can differ from the Claude API schedule. For the current retirement date of any model on Agent Platform, see [Google Cloud's documentation for Claude models on Agent Platform](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/partner-models/claude).

| Model                        | Agent Platform API model ID |
| ---------------------------- | --------------------------- |
| Claude Fable 5               | claude-fable-5              |
| Claude Opus 5                | claude-opus-5               |
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
  Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform. See [Migrating to a newer Claude model](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

### Making requests

Before running requests you might need to run `gcloud auth application-default login` to authenticate with Google Cloud.

The following examples show how to generate text from Claude on Agent Platform:

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-5
  PROJECT_ID=MY_PROJECT_ID

  curl https://aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
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
      model="claude-opus-5",
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

  const result = await client.messages.create({
    model: "claude-opus-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
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
  		Model:     anthropic.ModelClaudeOpus5,
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
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;

  void main() {
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(VertexBackend.fromEnv())
          .build();

      Message message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
  );
  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

See the [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) and the official [Agent Platform docs](https://cloud.google.com/vertex-ai/docs) for more details.

Claude is also available through [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry).

## Data retention

Data handling for this offering is governed by Google Cloud. For details, see [Agent Platform and zero data retention](https://cloud.google.com/vertex-ai/generative-ai/docs/data-governance).

## Activity logging

Agent Platform provides a [request-response logging service](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/request-response-logging) that allows you to log the prompts and completions associated with your usage.

Anthropic recommends that you log your activity on at least a 30-day rolling basis to understand your activity and investigate any potential misuse.

<Note>
  Turning on this service does not give Google or Anthropic any access to your content.
</Note>

## Feature support

For the full feature list with Google Cloud availability, see [Features overview](https://platform.claude.com/docs/en/build-with-claude/overview).

### Supported feature highlights

* [Messages API](https://platform.claude.com/docs/en/api/messages/create)
* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
* [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
* [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), including the [Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool), [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool), and [Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool)
* [Web search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)
* [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
* [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

### Features not supported

* Input sources (URL sources for images and documents, Files API)
* Server-side tools (code execution, web fetch, advisor)
* Agent infrastructure (Agent Skills, MCP connector, programmatic tool calling)
* API endpoints (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Server-side fallback (the [`fallbacks` parameter](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback); use the [client-side fallback pattern](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead)
* [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) and [browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) toolsets (`computer_toolset_20260801` and `browser_toolset_20260801` are not currently available on Google Cloud; the beta computer use tool versions remain available)

### Context window

Claude Fable 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, and Claude Sonnet 4.6 have a [1M-token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) on Agent Platform. Other Claude models, including Sonnet 4.5 and Sonnet 4 (deprecated), have a 200k-token context window.

Agent Platform limits request payloads to 30 MB. When sending large documents or many images, you might reach this limit before the token limit.

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
  ```bash cURL
  MODEL_ID=claude-opus-5
  PROJECT_ID=MY_PROJECT_ID

  curl https://aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/global/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
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
      model="claude-opus-5",
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
    model: "claude-opus-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "global";

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
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
  		Model:     anthropic.ModelClaudeOpus5,
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
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Uses default Google Cloud credentials
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("global")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
  );

  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "global",
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

**Using multi-region endpoints:**

Set the `region` parameter to a multi-region identifier: `"us"` for the United States or `"eu"` for the European Union. The SDK routes requests to the corresponding multi-region endpoint (`https://aiplatform.us.rep.googleapis.com` or `https://aiplatform.eu.rep.googleapis.com`), which dynamically balances traffic across regions within that geography.

<CodeGroup>
  ```bash cURL
  MODEL_ID=claude-opus-5
  LOCATION=us # Multi-region identifier: "us" or "eu"
  PROJECT_ID=MY_PROJECT_ID

  curl https://aiplatform.${LOCATION}.rep.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us"  # Multi-region identifier: "us" or "eu"

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      model="claude-opus-5",
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
    model: "claude-opus-5",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us"; // Multi-region identifier: "us" or "eu"

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      Model = Model.ClaudeOpus5,
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
  	// Multi-region identifier: "us" or "eu"
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeOpus5,
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
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Multi-region identifier: "us" or "eu"
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("us")
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_5)
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
      model: 'claude-opus-5',
  );
  $textBlock = array_find($message->content, static fn ($block): bool => $block->type === 'text');
  echo $textBlock->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us", # Multi-region identifier: "us" or "eu"
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    model: "claude-opus-5",
    max_tokens: 100,
    messages: [{role: "user", content: "Hey Claude!"}]
  )

  puts message.content.find { it.type == :text }.text
  ```
</CodeGroup>

**Using regional endpoints:**

Specify a specific region such as `"us-east5"` or `"europe-west1"`:

<CodeGroup>
  ```bash cURL
  # Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
  MODEL_ID=claude-sonnet-4-6
  LOCATION=us-east5 # Specify a specific region
  PROJECT_ID=MY_PROJECT_ID

  curl https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT_ID}/locations/${LOCATION}/publishers/anthropic/models/${MODEL_ID}:rawPredict \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json" \
    -d '{
      "anthropic_version": "vertex-2023-10-16",
      "messages": [{"role": "user", "content": "Hey Claude!"}],
      "max_tokens": 100
    }'
  ```

  ```bash CLI
  # The ant CLI does not support Agent Platform.
  ```

  ```python Python
  from anthropic import AnthropicVertex

  project_id = "MY_PROJECT_ID"
  region = "us-east5"  # Specify a specific region

  client = AnthropicVertex(project_id=project_id, region=region)

  message = client.messages.create(
      # Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
      model="claude-sonnet-4-6",
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
  const region = "us-east5"; // Specify a specific region

  const client = new AnthropicVertex({
    projectId,
    region
  });

  const result = await client.messages.create({
    // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
    model: "claude-sonnet-4-6",
    max_tokens: 100,
    messages: [
      {
        role: "user",
        content: "Hey Claude!"
      }
    ]
  });
  console.log(JSON.stringify(result, null, 2));
  ```

  ```csharp C#
  using Anthropic.Models.Messages;
  using Anthropic.Vertex;

  var projectId = "MY_PROJECT_ID";
  var region = "us-east5"; // Specify a specific region

  var client = new AnthropicVertexClient(new AnthropicVertexCredentials(region, projectId));

  var parameters = new MessageCreateParams
  {
      // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
      Model = Model.ClaudeSonnet4_6,
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
  	// Specify a specific region
  	client := anthropic.NewClient(
  		vertex.WithGoogleAuth(context.Background(), "us-east5", "MY_PROJECT_ID"),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		// Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
  		Model:     anthropic.ModelClaudeSonnet4_6,
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
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;
  import com.anthropic.vertex.backends.VertexBackend;
  import com.google.auth.oauth2.GoogleCredentials;

  void main() throws Exception {
      // Uses default Google Cloud credentials with specific region
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(
              VertexBackend.builder()
                  .googleCredentials(GoogleCredentials.getApplicationDefault())
                  .region("us-east5") // Specify a specific region
                  .project("MY_PROJECT_ID")
                  .build()
          )
          .build();

      var message = client
          .messages()
          .create(
              MessageCreateParams.builder()
                  // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
                  .model(Model.CLAUDE_SONNET_4_6)
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
      location: 'us-east5',
      projectId: 'MY_PROJECT_ID',
  );

  $message = $client->messages->create(
      maxTokens: 100,
      messages: [
          ['role' => 'user', 'content' => 'Hey Claude!']
      ],
      // Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
      model: 'claude-sonnet-4-6',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::VertexClient.new(
    region: "us-east5", # Specify a specific region
    project_id: "MY_PROJECT_ID"
  )

  message = client.messages.create(
    # Specific regional endpoints support Claude Sonnet 4.6 and earlier; newer models use the global or multi-region endpoints
    model: "claude-sonnet-4-6",
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
* **Anthropic pricing details:** [Cloud platform pricing](https://platform.claude.com/docs/en/about-claude/pricing#cloud-platform-pricing)
