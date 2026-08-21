---
title: Claude on Amazon Bedrock (Opus 4.6 and earlier)
url: https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy
description: The legacy Amazon Bedrock integration for Claude models, using InvokeModel and Converse APIs with ARN-versioned model identifiers.
---

<Note>
  This page covers the legacy Amazon Bedrock integration: the `InvokeModel` and `Converse` APIs with ARN-versioned model identifiers and AWS event-stream encoding. For models available on the Messages-API Bedrock endpoint, see [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock), which uses the Messages API at `/anthropic/v1/messages` with SSE streaming. For an Anthropic-operated alternative with AWS Marketplace billing and typically same-day feature access, see [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws). Existing Bedrock users can follow the [migration guide](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws#migrating-from-amazon-bedrock).
</Note>

Calling Claude through Bedrock slightly differs from how you would call Claude on the Claude API directly. This guide walks you through completing an API call to Claude on Bedrock using one of Anthropic's [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview).

Note that this guide assumes you have already signed up for an [AWS account](https://portal.aws.amazon.com/billing/signup) and configured programmatic access.

## Install and configure the AWS CLI

1. [Install a version of the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) at or newer than version `2.13.23`.
2. Configure your AWS credentials using the AWS configure command (see [Configure the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)) or find your credentials by navigating to "Command line or programmatic access" within your AWS dashboard and following the directions in the modal window.
3. Verify that your credentials are working:

```bash AWS CLI
aws sts get-caller-identity
```

## Install an SDK for accessing Bedrock

Anthropic's [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) support Bedrock. You can also use an AWS SDK like `boto3` directly.

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[bedrock]"
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/bedrock-sdk
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Bedrock
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go/bedrock
    ```
  </Tab>

  <Tab title="Java">
    <CodeGroup>
      ```groovy Gradle
      implementation("com.anthropic:anthropic-java-bedrock:2.57.0")
      ```

      ```xml Maven
      <dependency>
          <groupId>com.anthropic</groupId>
          <artifactId>anthropic-java-bedrock</artifactId>
          <version>2.57.0</version>
      </dependency>
      ```

      ```java Java
      import com.anthropic.client.AnthropicClient;
      import com.anthropic.client.okhttp.AnthropicOkHttpClient;
      import com.anthropic.bedrock.backends.BedrockBackend;
      import com.anthropic.models.messages.MessageCreateParams;
      import com.anthropic.models.messages.Message;
      import com.anthropic.models.messages.Model;

      public class BasicMessage {
          public static void main(String[] args) {
              AnthropicClient client = AnthropicOkHttpClient.builder()
                  .backend(BedrockBackend.fromEnv())
                  .build();

              MessageCreateParams params = MessageCreateParams.builder()
                  .model(Model.CLAUDE_OPUS_4_6)
                  .maxTokens(1024L)
                  .addUserMessage("What is the capital of France?")
                  .build();

              Message response = client.messages().create(params);
              response.content().stream()
                  .flatMap(block -> block.text().stream())
                  .forEach(textBlock -> System.out.println(textBlock.text()));
          }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk aws/aws-sdk-php
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    # Gemfile
    gem "anthropic"
    gem "aws-sdk-bedrockruntime"
    ```
  </Tab>

  <Tab title="Boto3 (Python)">
    ```bash
    pip install "boto3>=1.28.59"
    ```
  </Tab>
</Tabs>

## Accessing Bedrock

### Subscribe to Anthropic models

Go to the [AWS Console > Bedrock > Model Access](https://console.aws.amazon.com/bedrock/home?region=us-west-2#/modelaccess) and request access to Anthropic models. Note that Anthropic model availability varies by region. See [AWS documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) for latest information.

#### API model IDs

<Note>
  Claude Opus 5, Claude Sonnet 5, Claude Fable 5, Claude Opus 4.8, and Claude Opus 4.7 are reachable through `InvokeModel` on `bedrock-runtime`. These requests are served by the same infrastructure as the [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) endpoint. For the native Messages API request shape and full feature parity, use that page. These models are omitted from the model table on this page because they do not have ARN-versioned model IDs.
</Note>

Lifecycle terms (Deprecated, Retired) are defined in [Model deprecations](https://platform.claude.com/docs/en/about-claude/model-deprecations). Lifecycle dates on partner-operated platforms are set by the partner and can differ from the Claude API schedule. For the current retirement date of any model on Amazon Bedrock, see [Amazon Bedrock's model lifecycle page](https://docs.aws.amazon.com/bedrock/latest/userguide/model-lifecycle.html).

AWS offers newer Claude models through [cross-region inference](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) rather than on-demand throughput. For these models, a request that passes the base model ID fails with an HTTP 400 error like the following:

```text wrap
Invocation of model ID anthropic.claude-sonnet-4-5-20250929-v1:0 with on-demand throughput isn't supported. Retry your request with the ID or ARN of an inference profile that contains this model.
```

To invoke these models, pass an inference profile instead of the base model ID. The inference profile ID is the base model ID with a prefix from a column marked "Yes" in the following table, for example us.anthropic.claude-sonnet-4-5-20250929-v1:0. You can also pass the full inference profile ARN, in the form `arn:aws:bedrock:{region}:{account-id}:inference-profile/{inference-profile-id}`. For AWS's authoritative list of available inference profiles, see [Supported Regions and models for inference profiles](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html). For how the prefixes affect routing and pricing, see the [Global versus regional endpoints](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy#global-vs-regional-endpoints) section.

| Model                        | Base Bedrock model ID                     | `global` | `us` | `eu` | `jp` | `apac` |
| ---------------------------- | ----------------------------------------- | -------- | ---- | ---- | ---- | ------ |
| Claude Opus 4.6              | anthropic.claude-opus-4-6-v1              | Yes      | Yes  | Yes  | Yes  | Yes    |
| Claude Sonnet 4.6            | anthropic.claude-sonnet-4-6               | Yes      | Yes  | Yes  | Yes  | No     |
| Claude Sonnet 4.5            | anthropic.claude-sonnet-4-5-20250929-v1:0 | Yes      | Yes  | Yes  | Yes  | No     |
| Claude Sonnet 4 Deprecated.  | anthropic.claude-sonnet-4-20250514-v1:0   | Yes      | Yes  | Yes  | No   | Yes    |
| Claude Sonnet 3.7 Retired.   | anthropic.claude-3-7-sonnet-20250219-v1:0 | No       | No   | No   | No   | No     |
| Claude Opus 4.5              | anthropic.claude-opus-4-5-20251101-v1:0   | Yes      | Yes  | Yes  | No   | No     |
| Claude Opus 4.1 Deprecated.  | anthropic.claude-opus-4-1-20250805-v1:0   | No       | Yes  | No   | No   | No     |
| Claude Opus 4 Retired.       | anthropic.claude-opus-4-20250514-v1:0     | No       | No   | No   | No   | No     |
| Claude Haiku 4.5             | anthropic.claude-haiku-4-5-20251001-v1:0  | Yes      | Yes  | Yes  | No   | No     |
| Claude Haiku 3.5 Deprecated. | anthropic.claude-3-5-haiku-20241022-v1:0  | No       | Yes  | No   | No   | No     |

### List available models

The following examples show how to print a list of all the Claude models available through Bedrock:

<CodeGroup>
  ```bash AWS CLI
  aws bedrock list-foundation-models --region=us-west-2 --by-provider anthropic --query "modelSummaries[*].modelId"
  ```

  ```python Boto3 (Python)
  import boto3

  bedrock = boto3.client(service_name="bedrock")
  response = bedrock.list_foundation_models(byProvider="anthropic")

  for summary in response["modelSummaries"]:
      print(summary["modelId"])
  ```

  ```typescript TypeScript
  import { BedrockClient, ListFoundationModelsCommand } from "@aws-sdk/client-bedrock";

  const client = new BedrockClient({ region: "us-west-2" });

  const command = new ListFoundationModelsCommand({ byProvider: "anthropic" });
  const response = await client.send(command);

  if (response.modelSummaries) {
    for (const summary of response.modelSummaries) {
      console.log(summary.modelId);
    }
  }
  ```

  ```csharp C#
  using Amazon;
  using Amazon.Bedrock;
  using Amazon.Bedrock.Model;

  var client = new AmazonBedrockClient(RegionEndpoint.USWest2);

  var request = new ListFoundationModelsRequest
  {
      ByProvider = "anthropic"
  };

  var response = await client.ListFoundationModelsAsync(request);

  foreach (var summary in response.ModelSummaries)
  {
      Console.WriteLine(summary.ModelId);
  }
  ```

  ```go Go
  import (
  	"context"
  	"fmt"
  	"log"

  	"github.com/aws/aws-sdk-go-v2/config"
  	"github.com/aws/aws-sdk-go-v2/service/bedrock"
  )
  // ...
  	cfg, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion("us-west-2"))
  	if err != nil {
  		log.Fatal(err)
  	}

  	client := bedrock.NewFromConfig(cfg)

  	byProvider := "anthropic"
  	response, err := client.ListFoundationModels(context.TODO(), &bedrock.ListFoundationModelsInput{
  		ByProvider: &byProvider,
  	})
  	if err != nil {
  		log.Fatal(err)
  	}

  	for _, summary := range response.ModelSummaries {
  		fmt.Println(*summary.ModelId)
  	}
  ```

  ```java Java
  import software.amazon.awssdk.regions.Region;
  import software.amazon.awssdk.services.bedrock.BedrockClient;
  import software.amazon.awssdk.services.bedrock.model.ListFoundationModelsRequest;
  import software.amazon.awssdk.services.bedrock.model.ListFoundationModelsResponse;
  import software.amazon.awssdk.services.bedrock.model.FoundationModelSummary;

  public class ListAnthropicModels {
      public static void main(String[] args) {
          BedrockClient client = BedrockClient.builder()
              .region(Region.US_WEST_2)
              .build();

          ListFoundationModelsRequest request = ListFoundationModelsRequest.builder()
              .byProvider("anthropic")
              .build();

          ListFoundationModelsResponse response = client.listFoundationModels(request);

          for (FoundationModelSummary summary : response.modelSummaries()) {
              System.out.println(summary.modelId());
          }

          client.close();
      }
  }
  ```

  ```php PHP
  <?php

  use Aws\Bedrock\BedrockClient;

  $client = new BedrockClient([
      'region' => 'us-west-2',
      'version' => 'latest'
  ]);

  $result = $client->listFoundationModels([
      'byProvider' => 'anthropic'
  ]);

  foreach ($result['modelSummaries'] as $summary) {
      echo $summary['modelId'] . PHP_EOL;
  }
  ```

  ```ruby Ruby
  require "aws-sdk-bedrock"

  client = Aws::Bedrock::Client.new(region: "us-west-2")

  response = client.list_foundation_models({
    by_provider: "anthropic"
  })

  response.model_summaries.each do |summary|
    puts summary.model_id
  end
  ```
</CodeGroup>

### Making requests

The following examples show how to generate text from Claude on Bedrock:

<Tabs>
  <Tab title="cURL">
    <Note>
      Calling the `InvokeModel` API with AWS credentials requires SigV4 request signing, which the SDKs in the other tabs handle automatically. For a Bedrock endpoint you can call with a self-contained cURL command, see [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock#making-your-first-request).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      The `ant` CLI does not support Amazon Bedrock. Use one of the SDK examples instead.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(
        # Authenticate by either providing the keys below or use the default AWS credential providers, such as
        # using ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and "AWS_ACCESS_KEY_ID" environment variables.
        aws_access_key="<access key>",
        aws_secret_key="<secret key>",
        # Temporary credentials can be used with aws_session_token.
        # Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
        aws_session_token="<session_token>",
        # aws_region changes the aws region to which the request is made. By default, the SDK reads AWS_REGION,
        # and if that's not present, defaults to us-east-1. Note that the SDK does not read ~/.aws/config for the region.
        aws_region="us-west-2",
    )

    message = client.messages.create(
        model="global.anthropic.claude-opus-4-6-v1",
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    print(message.content)
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrock({
      // Authenticate by either providing the keys below or use
      // the default AWS credential providers, such as
      // ~/.aws/credentials or the "AWS_SECRET_ACCESS_KEY" and
      // "AWS_ACCESS_KEY_ID" environment variables.
      awsAccessKey: "<access key>",
      awsSecretKey: "<secret key>",

      // Temporary credentials can be used with awsSessionToken.
      // Read more at https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html.
      awsSessionToken: "<session_token>",

      // awsRegion changes the aws region to which the request
      // is made. By default, the SDK reads AWS_REGION, and if
      // that's not present, defaults to us-east-1. Note that
      // the SDK does not read ~/.aws/config for the region.
      awsRegion: "us-west-2"
    });

    const message = await client.messages.create({
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{ role: "user", content: "Hello, world" }]
    });
    console.log(message);
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    AnthropicBedrockClient client = new(
        await AnthropicBedrockCredentialsHelper.FromEnv()
        ?? throw new InvalidOperationException("AWS credentials not configured.")
    );

    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = "global.anthropic.claude-opus-4-6-v1",
        MaxTokens = 256,
        Messages = [new() { Role = Role.User, Content = "Hello, world" }],
    });

    Console.WriteLine(
        string.Join("", response.Content
            .Select(block => block.Value)
            .OfType<TextBlock>()
            .Select(textBlock => textBlock.Text)));
    ```
  </Tab>

  <Tab title="Go">
    ```go
    import (
    	"context"
    	"fmt"

    	"github.com/anthropics/anthropic-sdk-go"
    	"github.com/anthropics/anthropic-sdk-go/bedrock"
    )
    // ...
    	// Uses default AWS credential provider chain
    	client := anthropic.NewClient(
    		bedrock.WithLoadDefaultConfig(context.Background()),
    	)

    	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    		Model:     "global.anthropic.claude-opus-4-6-v1",
    		MaxTokens: 256,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
    		},
    	})
    	if err != nil {
    		panic(err)
    	}
    	fmt.Println(message.Content)
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.bedrock.backends.BedrockBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.Message;
    import com.anthropic.models.messages.MessageCreateParams;

    public class BedrockExample {

      public static void main(String[] args) {
        // Uses default AWS credential provider chain
        AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(BedrockBackend.fromEnv())
          .build();

        Message message = client
          .messages()
          .create(
            MessageCreateParams.builder()
              .model("global.anthropic.claude-opus-4-6-v1")
              .maxTokens(256)
              .addUserMessage("Hello, world")
              .build()
          );

        System.out.println(message.content());
      }
    }
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    <?php

    use Anthropic\Bedrock;

    $client = Bedrock\Client::withCredentials(
        accessKeyId: getenv("AWS_ACCESS_KEY_ID"),
        secretAccessKey: getenv("AWS_SECRET_ACCESS_KEY"),
        region: 'us-west-2',
        securityToken: getenv("AWS_SESSION_TOKEN"),
    );

    $message = $client->messages->create(
        maxTokens: 256,
        messages: [
            ['role' => 'user', 'content' => 'Hello, world']
        ],
        model: 'global.anthropic.claude-opus-4-6-v1',
    );
    echo $message->content[0]->text;
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    client = Anthropic::BedrockClient.new

    message = client.messages.create(
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{role: "user", content: "Hello, world"}]
    )

    puts message.content.first.text
    ```
  </Tab>

  <Tab title="Boto3 (Python)">
    ```python
    import boto3
    import json

    bedrock = boto3.client(service_name="bedrock-runtime")
    body = json.dumps(
        {
            "max_tokens": 256,
            "messages": [{"role": "user", "content": "Hello, world"}],
            "anthropic_version": "bedrock-2023-05-31",
        }
    )

    response = bedrock.invoke_model(
        body=body, modelId="global.anthropic.claude-opus-4-6-v1"
    )

    response_body = json.loads(response.get("body").read())
    print(response_body.get("content"))
    ```
  </Tab>
</Tabs>

See the [client SDKs](https://platform.claude.com/docs/en/cli-sdks-libraries/overview) for more details, and the [official Bedrock documentation](https://docs.aws.amazon.com/bedrock/).

### Bearer token authentication

You can authenticate with Bedrock using bearer tokens instead of AWS credentials. This is useful in corporate environments where teams need access to Bedrock without managing AWS credentials, IAM roles, or account-level permissions.

The simplest approach is to set the `AWS_BEARER_TOKEN_BEDROCK` environment variable, which each SDK detects automatically when resolving credentials from the environment.

To provide a token programmatically:

<Tabs>
  <Tab title="cURL">
    <Note>
      This section shows how to configure a bearer token in an SDK client. The SDKs also read the token from the `AWS_BEARER_TOKEN_BEDROCK` environment variable. For making direct HTTP requests with a bearer token, see the [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      The `ant` CLI does not support Amazon Bedrock. Use one of the SDK examples instead.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(
        api_key="your-bearer-token",
        aws_region="us-west-2",
    )

    message = client.messages.create(
        model="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}],
    )
    print(message.content)
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrock({
      apiKey: "your-bearer-token",
      awsRegion: "us-west-2"
    });

    const message = await client.messages.create({
      model: "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello!" }]
    });
    console.log(message);
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    var client = new AnthropicBedrockClient(
        new AnthropicBedrockApiTokenCredentials
        {
            BearerToken = "your-bearer-token",
            Region = "us-west-2",
        }
    );

    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
        MaxTokens = 1024,
        Messages = [new() { Role = Role.User, Content = "Hello!" }],
    });
    ```
  </Tab>

  <Tab title="Go">
    ```go
    import (
    	"context"
    	"fmt"

    	"github.com/anthropics/anthropic-sdk-go"
    	"github.com/anthropics/anthropic-sdk-go/bedrock"
    	"github.com/aws/aws-sdk-go-v2/aws"
    )
    // ...
    	cfg := aws.Config{
    		Region:                  "us-west-2",
    		BearerAuthTokenProvider: bedrock.NewStaticBearerTokenProvider("your-bearer-token"),
    	}
    	client := anthropic.NewClient(
    		bedrock.WithConfig(cfg),
    	)

    	message, err := client.Messages.New(context.TODO(), anthropic.MessageNewParams{
    		Model:     "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    		MaxTokens: 1024,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
    		},
    	})
    	if err != nil {
    		panic(err)
    	}
    	fmt.Println(message.Content[0].Text)
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.bedrock.backends.BedrockBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.MessageCreateParams;

    // Option 1: Set AWS_BEARER_TOKEN_BEDROCK environment variable and use fromEnv()
    AnthropicClient client = AnthropicOkHttpClient.builder()
      .backend(BedrockBackend.fromEnv())
      .build();

    // Option 2: Provide the token programmatically
    client = AnthropicOkHttpClient.builder()
      .backend(BedrockBackend.builder()
        .apiKey("your-bearer-token")
        .build())
      .build();

    MessageCreateParams params = MessageCreateParams.builder()
      .model("us.anthropic.claude-sonnet-4-5-20250929-v1:0")
      .maxTokens(1024)
      .addUserMessage("Hello!")
      .build();

    client.messages().create(params).content().stream()
      .flatMap(block -> block.text().stream())
      .forEach(textBlock -> System.out.println(textBlock.text()));
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    <?php

    use Anthropic\Bedrock;

    $client = Bedrock\Client::withApiKey('your-bearer-token', 'us-west-2');

    $message = $client->messages->create(
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Hello!']
        ],
        model: 'us.anthropic.claude-sonnet-4-5-20250929-v1:0',
    );
    echo $message->content[0]->text;
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    client = Anthropic::BedrockClient.new(
      api_key: "your-bearer-token",
      aws_region: "us-west-2"
    )

    message = client.messages.create(
      model: "us.anthropic.claude-sonnet-4-5-20250929-v1:0",
      max_tokens: 1024,
      messages: [{role: "user", content: "Hello!"}]
    )
    puts message.content.first.text
    ```
  </Tab>
</Tabs>

## Activity logging

Bedrock provides an [invocation logging service](https://docs.aws.amazon.com/bedrock/latest/userguide/model-invocation-logging.html) that allows you to log the prompts and completions associated with your usage.

Anthropic recommends that you log your activity on at least a 30-day rolling basis to understand your activity and investigate any potential misuse.

<Note>
  Turning on this service does not give AWS or Anthropic any access to your content.
</Note>

## Feature support

For the full feature list with Amazon Bedrock availability, see [Features overview](https://platform.claude.com/docs/en/build-with-claude/overview).

### Supported feature highlights

* [Messages API](https://platform.claude.com/docs/en/api/messages/create)
* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)
* [Thinking](https://platform.claude.com/docs/en/build-with-claude/thinking)
* [Tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview), including the [Bash tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/bash-tool), [Computer use tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool), [Memory tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool), and [Text editor tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/text-editor-tool)
* [Citations](https://platform.claude.com/docs/en/build-with-claude/citations)
* [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

### Features not supported

* Input sources (URL sources for images and documents, Files API)
* Server-side tools (code execution, web search, web fetch, advisor)
* Agent infrastructure (Agent Skills, MCP connector, programmatic tool calling)
* API endpoints (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Server-side fallback (the [`fallbacks` parameter](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback); use the [client-side fallback pattern](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead)
* Automatic prompt caching (the [top-level `cache_control` field](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#automatic-caching); use [explicit cache breakpoints](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#explicit-cache-breakpoints) instead)
* [Computer use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) and [browser use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/browser-use-tool) toolsets (`computer_toolset_20260801` and `browser_toolset_20260801` are not currently available on Amazon Bedrock; the beta computer use tool versions remain available)

### PDF support on Bedrock

PDF support is available on Bedrock through both the Converse API and InvokeModel API. For detailed information about PDF processing capabilities and limitations, see [Amazon Bedrock PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support#amazon-bedrock-pdf-support).

**Important considerations for Converse API users:**

* Visual PDF analysis (charts, images, layouts) requires citations to be enabled
* Without citations, only basic text extraction is available
* For full control without forced citations, use the InvokeModel API

### Mid-conversation system messages on Bedrock

[Mid-conversation system messages](https://platform.claude.com/docs/en/build-with-claude/mid-conversation-system-messages) are available through the InvokeModel API for Claude Fable 5 and Claude Opus 4.8. As described in the note under [API model IDs](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids), these requests are served by the same infrastructure as the [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock) endpoint. No beta header is required. This feature is not available on Claude Sonnet 5; use the top-level `system` field instead. It is not available for the ARN-versioned models in the model table on this page.

**For Converse API users:** the Converse API accepts system instructions through its top-level [`system` parameter](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_Converse.html). To add system instructions mid-conversation, use the InvokeModel API.

### Context window

Claude Fable 5, Claude Opus 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, and Claude Sonnet 4.6 have a [1M-token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows) on Amazon Bedrock. Other Claude models, including Sonnet 4.5 and Sonnet 4 (deprecated), have a 200k-token context window.

Bedrock limits request payloads to 20 MB. When sending large documents or many images, you may reach this limit before the token limit.

## Global versus regional endpoints

Starting with **Claude Sonnet 4.5 and all future models**, Bedrock offers two endpoint types:

* **Global endpoints:** Dynamic routing for maximum availability
* **Regional endpoints:** Guaranteed data routing through specific geographic regions

Regional endpoints include a 10% pricing premium over global endpoints.

<Note>
  This applies to Claude Sonnet 4.5 and future models only. Older models (Claude Sonnet 4 (deprecated) and earlier) maintain their existing pricing structures.
</Note>

### When to use each option

**Global endpoints (recommended):**

* Provide maximum availability and uptime
* Dynamically route requests to regions with available capacity
* No pricing premium
* Best for applications where data residency is flexible

**Regional endpoints (CRIS):**

* Route traffic through specific geographic regions
* Required for data residency and compliance requirements
* Available for US, EU, Japan, and Asia-Pacific
* 10% pricing premium reflects infrastructure costs for dedicated regional capacity

### Implementation

**Using global endpoints (default for Opus 4.6, Sonnet 4.6, and Sonnet 4.5):**

The model IDs for Claude Opus 4.6, Sonnet 4.6, and Sonnet 4.5 already include the `global.` prefix:

<Tabs>
  <Tab title="cURL">
    <Note>
      Calling the `InvokeModel` API with AWS credentials requires SigV4 request signing, which the SDKs in the other tabs handle automatically. For a Bedrock endpoint you can call with a self-contained cURL command, see [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock#making-your-first-request).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      The `ant` CLI does not support Amazon Bedrock. Use one of the SDK examples instead.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(aws_region="us-west-2")

    message = client.messages.create(
        model="global.anthropic.claude-opus-4-6-v1",
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrock({
      awsRegion: "us-west-2"
    });

    const message = await client.messages.create({
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{ role: "user", content: "Hello, world" }]
    });
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    // C# Bedrock client uses model IDs with region prefix for global routing
    AnthropicBedrockClient client = new(
        await AnthropicBedrockCredentialsHelper.FromEnv()
        ?? throw new InvalidOperationException("AWS credentials not configured.")
    );

    var response = await client.Messages.Create(new MessageCreateParams
    {
        // Use "global." prefix for global cross-region inference
        Model = "global.anthropic.claude-opus-4-6-v1",
        MaxTokens = 256,
        Messages = [new() { Role = Role.User, Content = "Hello, world" }],
    });
    ```
  </Tab>

  <Tab title="Go">
    ```go
    import (
    	"context"

    	"github.com/anthropics/anthropic-sdk-go"
    	"github.com/anthropics/anthropic-sdk-go/bedrock"
    )
    // ...
    	// Uses default AWS credential provider chain
    	client := anthropic.NewClient(
    		bedrock.WithLoadDefaultConfig(context.Background()),
    	)

    	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    		Model:     "global.anthropic.claude-opus-4-6-v1",
    		MaxTokens: 256,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
    		},
    	})
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.bedrock.backends.BedrockBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.MessageCreateParams;

    // Uses default AWS credential provider chain
    AnthropicClient client = AnthropicOkHttpClient.builder()
      .backend(BedrockBackend.fromEnv())
      .build();

    var message = client
      .messages()
      .create(
        MessageCreateParams.builder()
          .model("global.anthropic.claude-opus-4-6-v1")
          .maxTokens(256)
          .addUserMessage("Hello, world")
          .build()
      );
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    <?php

    use Anthropic\Bedrock;

    $client = Bedrock\Client::fromEnvironment();

    $message = $client->messages->create(
        maxTokens: 256,
        messages: [
            ['role' => 'user', 'content' => 'Hello, world']
        ],
        model: 'global.anthropic.claude-opus-4-6-v1',
    );
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    # Default credentials resolve region from AWS_REGION env var
    client = Anthropic::BedrockClient.new

    message = client.messages.create(
      # Use "global." prefix for global cross-region inference
      model: "global.anthropic.claude-opus-4-6-v1",
      max_tokens: 256,
      messages: [{role: "user", content: "Hello, world"}]
    )
    ```
  </Tab>
</Tabs>

**Using regional endpoints (CRIS):**

To use regional endpoints, replace the `global.` prefix with a regional prefix such as `us.`:

<Tabs>
  <Tab title="cURL">
    <Note>
      Calling the `InvokeModel` API with AWS credentials requires SigV4 request signing, which the SDKs in the other tabs handle automatically. For a Bedrock endpoint you can call with a self-contained cURL command, see [Claude in Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock#making-your-first-request).
    </Note>
  </Tab>

  <Tab title="CLI">
    <Note>
      The `ant` CLI does not support Amazon Bedrock. Use one of the SDK examples instead.
    </Note>
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrock

    client = AnthropicBedrock(aws_region="us-west-2")

    # Using US regional endpoint (CRIS)
    message = client.messages.create(
        model="us.anthropic.claude-opus-4-6-v1",  # Regional prefix
        max_tokens=256,
        messages=[{"role": "user", "content": "Hello, world"}],
    )
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import AnthropicBedrock from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrock({
      awsRegion: "us-west-2"
    });

    // Using US regional endpoint (CRIS)
    const message = await client.messages.create({
      model: "us.anthropic.claude-opus-4-6-v1", // Regional prefix
      max_tokens: 256,
      messages: [{ role: "user", content: "Hello, world" }]
    });
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    AnthropicBedrockClient client = new(
        new AnthropicBedrockPrivateKeyCredentials { Region = "us-west-2" }
    );

    // Using US regional endpoint (CRIS)
    var response = await client.Messages.Create(new MessageCreateParams
    {
        Model = "us.anthropic.claude-opus-4-6-v1", // Regional prefix
        MaxTokens = 256,
        Messages = [new() { Role = Role.User, Content = "Hello, world" }],
    });
    ```
  </Tab>

  <Tab title="Go">
    ```go
    import (
    	"context"

    	"github.com/anthropics/anthropic-sdk-go"
    	"github.com/anthropics/anthropic-sdk-go/bedrock"
    )
    // ...
    	// Uses default AWS credential provider chain
    	client := anthropic.NewClient(
    		bedrock.WithLoadDefaultConfig(context.Background()),
    	)

    	// Using US regional endpoint (CRIS)
    	message, _ := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    		Model:     "us.anthropic.claude-opus-4-6-v1", // Regional prefix
    		MaxTokens: 256,
    		Messages: []anthropic.MessageParam{
    			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, world")),
    		},
    	})
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.anthropic.bedrock.backends.BedrockBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.MessageCreateParams;

    // Uses default AWS credential provider chain
    AnthropicClient client = AnthropicOkHttpClient.builder()
      .backend(BedrockBackend.fromEnv())
      .build();

    // Using US regional endpoint (CRIS)
    var message = client
      .messages()
      .create(
        MessageCreateParams.builder()
          .model("us.anthropic.claude-opus-4-6-v1") // Regional prefix
          .maxTokens(256)
          .addUserMessage("Hello, world")
          .build()
      );
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    <?php

    use Anthropic\Bedrock;

    $client = Bedrock\Client::fromEnvironment();

    $message = $client->messages->create(
        maxTokens: 256,
        messages: [
            ['role' => 'user', 'content' => 'Hello, world']
        ],
        model: 'us.anthropic.claude-opus-4-6-v1',
    );
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    # Using US regional endpoint (CRIS)
    client = Anthropic::BedrockClient.new(aws_region: "us-west-2")

    message = client.messages.create(
      model: "us.anthropic.claude-opus-4-6-v1", # Regional prefix
      max_tokens: 256,
      messages: [{role: "user", content: "Hello, world"}]
    )
    ```
  </Tab>
</Tabs>

<Note>
  **Claude Mythos Preview** is a research preview model available to invited customers on Amazon Bedrock. For more information, see [Project Glasswing](https://anthropic.com/glasswing).
</Note>

## Additional resources

* **Bedrock pricing:** [Amazon Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/)
* **AWS pricing documentation:** [Bedrock pricing guide](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-pricing.html)
* **AWS blog post:** [Introducing Claude Sonnet 4.5 in Amazon Bedrock](https://aws.amazon.com/blogs/aws/introducing-claude-sonnet-4-5-in-amazon-bedrock-anthropics-most-intelligent-model-best-for-coding-and-complex-agents/)
* **Anthropic pricing details:** [Cloud platform pricing](https://platform.claude.com/docs/en/about-claude/pricing#cloud-platform-pricing)
