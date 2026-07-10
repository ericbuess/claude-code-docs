# Claude in Amazon Bedrock

Access Claude models through Amazon Bedrock with AWS-native authentication, billing, and security boundaries.

---

This guide walks you through setting up and making API calls to Claude in Amazon Bedrock. Claude in Amazon Bedrock runs on AWS-managed infrastructure with zero operator access (Anthropic personnel have no access to the inference infrastructure), letting you build sensitive applications entirely inside the AWS security boundary while using the same Messages API shape you use with Anthropic's first-party API.

<Note>
  This page covers Claude in Amazon Bedrock, which serves Claude through the Messages API at `/anthropic/v1/messages` on AWS-managed infrastructure. The previous Amazon Bedrock integration (the `InvokeModel` and `Converse` APIs with ARN-versioned model identifiers) remains available and is documented at [Claude on Amazon Bedrock (legacy)](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy). For an Anthropic-operated alternative on AWS with AWS Marketplace billing and typically same-day feature access, see [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws).
</Note>

## Access

Claude Fable 5, Claude Opus 4.8, Claude Sonnet 5, Claude Opus 4.7, and Claude Haiku 4.5 are open to all Amazon Bedrock customers. Claude Mythos Preview requires an invitation; see [Project Glasswing](https://anthropic.com/glasswing). For region availability, see [Regions](#regions).

## Prerequisites

Before you begin, ensure you have:

* An AWS account with [Amazon Bedrock model access](https://console.aws.amazon.com/bedrock/home#/modelaccess) enabled for the Claude models you intend to use.
* The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) installed and configured (optional, for credential management).

Claude Mythos Preview additionally requires a dedicated AWS account that has been allowlisted by the Bedrock Marketplace team. Your Anthropic account executive can submit your account ID for allowlisting (typically processed within 24 hours), and AWS sends a welcome email once it's complete.

## Authentication

Claude in Amazon Bedrock supports three authentication paths. Choose the one that best fits your security requirements.

### Bedrock service role (recommended)

Use a Bedrock service role with AWS-managed keys for the most secure, long-lived access:

<Steps>
  <Step title="Admin: provision the service role">
    An AWS administrator provisions a Bedrock service role and grants developers `iam:PassRole` permission on the service role ARN.
  </Step>

  <Step title="Developer: pass the role">
    When calling the API, Bedrock assumes the service role on your behalf. See the [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-mantle.html) for how to associate the role with your requests.
  </Step>
</Steps>

### IAM assumed roles

For identity-federated access with a 12-hour maximum session:

<Steps>
  <Step title="Admin: configure the IAM role">
    Create an IAM role scoped to your Claude models. The trust policy names your identity provider (SAML, OIDC, or AWS Identity Center). The permissions policy grants `bedrock-mantle:CreateInference` only on the allowed model ARNs.
  </Step>

  <Step title="Developer: authenticate and assume">
    Authenticate through your corporate identity provider, then assume the IAM role. AWS STS issues temporary credentials that the SDK or CLI uses to sign requests.
  </Step>
</Steps>

### Bearer tokens

For short-term access without IAM roles (12-hour maximum, least preferred):

<Steps>
  <Step title="Admin: restrict token types">
    Block long-term keys by attaching a policy that denies `bedrock:CallWithBearerToken` unless the `bedrock:BearerTokenType` condition matches a short-term token.
  </Step>

  <Step title="Developer: mint a token">
    Use the `aws-bedrock-token-generator` CLI to mint a bearer token. Pass it in the `x-api-key` header on each request.
  </Step>
</Steps>

## Install an SDK

Anthropic's [client SDKs](/docs/en/cli-sdks-libraries/overview) support Claude in Amazon Bedrock through a Bedrock-specific package or module.

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
    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java-bedrock:2.47.1")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-bedrock</artifactId>
            <version>2.47.1</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
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
    gem "aws-sdk-core"
    ```
  </Tab>
</Tabs>

## Making your first request

The endpoint follows the pattern `https://bedrock-mantle.{region}.api.aws/anthropic/v1/messages`. Unlike the `InvokeModel`-based integration, this endpoint uses standard SSE streaming and the same request body shape as Anthropic's first-party API.

The SDK resolves credentials and region using the standard AWS precedence: constructor arguments, then environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION`), then the AWS config file and credential chain (SSO, assumed roles, ECS task role, IMDS).

<Tabs>
  <Tab title="cURL">
    ```bash
    curl https://bedrock-mantle.us-east-1.api.aws/anthropic/v1/messages \
      --aws-sigv4 "aws:amz:us-east-1:bedrock-mantle" \
      --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
      -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
      -H "content-type: application/json" \
      -H "anthropic-version: 2023-06-01" \
      -d '{
        "model": "anthropic.claude-opus-4-8",
        "max_tokens": 1024,
        "messages": [
          {"role": "user", "content": "Hello, Claude"}
        ]
      }'
    ```
  </Tab>

  <Tab title="CLI">
    The `ant` CLI does not support Amazon Bedrock. Use either cURL or an SDK.
  </Tab>

  <Tab title="Python">
    ```python
    from anthropic import AnthropicBedrockMantle

    client = AnthropicBedrockMantle(aws_region="us-east-1")

    message = client.messages.create(
        model="anthropic.claude-opus-4-8",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello, Claude"}],
    )

    print(message.content[0].text)
    ```
  </Tab>

  <Tab title="TypeScript">
    ```typescript
    import { AnthropicBedrockMantle } from "@anthropic-ai/bedrock-sdk";

    const client = new AnthropicBedrockMantle({
      awsRegion: "us-east-1"
    });

    const message = await client.messages.create({
      model: "anthropic.claude-opus-4-8",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello, Claude" }]
    });

    const block = message.content[0];
    if (block.type === "text") {
      console.log(block.text);
    }
    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using Anthropic.Bedrock;
    using Anthropic.Models.Messages;

    var client = new AnthropicBedrockMantleClient(new() { AwsRegion = "us-east-1" });

    var message = await client.Messages.Create(new()
    {
        Model = "anthropic.claude-opus-4-8",
        MaxTokens = 1024,
        Messages = [new() { Role = Role.User, Content = "Hello, Claude" }],
    });

    if (message.Content[0].Value is TextBlock block)
        Console.WriteLine(block.Text);
    ```
  </Tab>

  <Tab title="Go">
    ```go
    client, err := bedrock.NewMantleClient(context.Background(), bedrock.MantleClientConfig{
    	AWSRegion: "us-east-1",
    })
    if err != nil {
    	panic(err)
    }

    message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
    	Model:     "anthropic.claude-opus-4-8",
    	MaxTokens: 1024,
    	Messages: []anthropic.MessageParam{
    		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello, Claude")),
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
    import com.anthropic.bedrock.backends.BedrockMantleBackend;
    import com.anthropic.client.AnthropicClient;
    import com.anthropic.client.okhttp.AnthropicOkHttpClient;
    import com.anthropic.models.messages.Message;
    import com.anthropic.models.messages.MessageCreateParams;

    void main() {
        AnthropicClient client = AnthropicOkHttpClient.builder()
            .backend(BedrockMantleBackend.fromEnv())
            .build();

        Message message = client.messages().create(
            MessageCreateParams.builder()
                .model("anthropic.claude-opus-4-8")
                .maxTokens(1024)
                .addUserMessage("Hello, Claude")
                .build()
        );

        IO.println(message.content().getFirst().asText().text());
    }
    ```
  </Tab>

  <Tab title="PHP">
    ```php
    use Anthropic\Bedrock\MantleClient;

    $client = new MantleClient(awsRegion: 'us-east-1');

    $message = $client->messages->create(
        model: 'anthropic.claude-opus-4-8',
        maxTokens: 1024,
        messages: [
            ['role' => 'user', 'content' => 'Hello, Claude'],
        ],
    );

    echo $message->content[0]->text;
    ```
  </Tab>

  <Tab title="Ruby">
    ```ruby
    require "anthropic"

    client = Anthropic::BedrockMantleClient.new(aws_region: "us-east-1")

    message = client.messages.create(
      model: "anthropic.claude-opus-4-8",
      max_tokens: 1024,
      messages: [{role: "user", content: "Hello, Claude"}]
    )

    puts message.content[0].text
    ```
  </Tab>
</Tabs>

<Tip>
  You can also use the standard `Anthropic` client: set `base_url` to `https://bedrock-mantle.{region}.api.aws/anthropic` and pass your bearer token as `api_key`. This path supports bearer-token authentication only. SigV4 signing requires the dedicated client.
</Tip>

## Supported models

Model IDs in Claude in Amazon Bedrock carry an `anthropic.` provider prefix. Model capabilities and behaviors are documented on the [Models overview](/docs/en/about-claude/models/overview) page.

| Model                 | Model ID                        | Access                                                                 |
| --------------------- | ------------------------------- | ---------------------------------------------------------------------- |
| Claude Fable 5        | anthropic.claude-fable-5        | Open                                                                   |
| Claude Opus 4.8       | anthropic.claude-opus-4-8       | Open                                                                   |
| Claude Opus 4.7       | anthropic.claude-opus-4-7       | Open                                                                   |
| Claude Sonnet 5       | `anthropic.claude-sonnet-5`     | Open                                                                   |
| Claude Haiku 4.5      | anthropic.claude-haiku-4-5      | Open                                                                   |
| Claude Mythos Preview | anthropic.claude-mythos-preview | Invitation only ([Project Glasswing](https://anthropic.com/glasswing)) |

<Tip>
  Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform. See [Migrating to a newer Claude model](/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Feature support

For the full feature list with Amazon Bedrock availability, see [Features overview](/docs/en/build-with-claude/overview).

### Supported feature highlights

* [Messages API](/docs/en/api/messages/create) (`/anthropic/v1/messages`)
* [Prompt caching](/docs/en/build-with-claude/prompt-caching)
* [Extended thinking](/docs/en/build-with-claude/extended-thinking)
* [Tool use](/docs/en/agents-and-tools/tool-use/overview), including the [Bash tool](/docs/en/agents-and-tools/tool-use/bash-tool), [Computer use tool](/docs/en/agents-and-tools/tool-use/computer-use-tool), [Memory tool](/docs/en/agents-and-tools/tool-use/memory-tool), and [Text editor tool](/docs/en/agents-and-tools/tool-use/text-editor-tool)
* [Citations](/docs/en/build-with-claude/citations)
* [Structured outputs](/docs/en/build-with-claude/structured-outputs)

### Features not supported

* Input sources (URL sources for images and documents, Files API)
* Server-side tools (code execution, web search, web fetch, advisor)
* Agent infrastructure (Agent Skills, MCP connector, programmatic tool calling)
* API endpoints (Message Batches, Models, Admin, Compliance, Usage and Cost)
* Claude Managed Agents
* Server-side fallback (the [`fallbacks` parameter](/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback); use the [client-side fallback pattern](/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead)

## Regions

Claude in Amazon Bedrock is available in the following AWS regions. Amazon Bedrock offers two endpoint types:

* **Global:** dynamic routing across all available regions for maximum availability. No pricing premium.
* **Regional:** the endpoint resolves to the single AWS region you specify, for data-residency requirements. Regional endpoints carry a 10% pricing premium over global endpoints. To route across multiple regions within a geography, use an [inference profile](https://docs.aws.amazon.com/bedrock/latest/userguide/cross-region-inference.html) (US, EU, JP, or AU). Regions marked **In-region only** in the table support direct single-region routing without an inference profile.

The global endpoint is available for Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Sonnet 5, and Claude Haiku 4.5. Claude Mythos Preview is regional only and is available in `us-east-1`.

| AWS region       | Location                  | Endpoint types             |
| ---------------- | ------------------------- | -------------------------- |
| `af-south-1`     | Africa (Cape Town)        | Global                     |
| `ap-northeast-1` | Asia Pacific (Tokyo)      | Global, JP, In-region only |
| `ap-northeast-2` | Asia Pacific (Seoul)      | Global                     |
| `ap-northeast-3` | Asia Pacific (Osaka)      | Global, JP                 |
| `ap-south-1`     | Asia Pacific (Mumbai)     | Global                     |
| `ap-south-2`     | Asia Pacific (Hyderabad)  | Global                     |
| `ap-southeast-1` | Asia Pacific (Singapore)  | Global                     |
| `ap-southeast-2` | Asia Pacific (Sydney)     | Global, AU                 |
| `ap-southeast-3` | Asia Pacific (Jakarta)    | Global                     |
| `ap-southeast-4` | Asia Pacific (Melbourne)  | Global, AU, In-region only |
| `ca-central-1`   | Canada (Central)          | Global, US                 |
| `ca-west-1`      | Canada West (Calgary)     | Global                     |
| `eu-central-1`   | Europe (Frankfurt)        | Global, EU                 |
| `eu-central-2`   | Europe (Zurich)           | Global, EU                 |
| `eu-north-1`     | Europe (Stockholm)        | Global, EU, In-region only |
| `eu-south-1`     | Europe (Milan)            | Global, EU                 |
| `eu-south-2`     | Europe (Spain)            | Global, EU                 |
| `eu-west-1`      | Europe (Ireland)          | Global, EU, In-region only |
| `eu-west-2`      | Europe (London)           | Global, EU                 |
| `eu-west-3`      | Europe (Paris)            | Global, EU                 |
| `il-central-1`   | Israel (Tel Aviv)         | Global                     |
| `me-central-1`   | Middle East (UAE)         | Global                     |
| `sa-east-1`      | South America (São Paulo) | Global                     |
| `us-east-1`      | US East (N. Virginia)     | Global, US, In-region only |
| `us-east-2`      | US East (Ohio)            | Global, US, In-region only |
| `us-west-1`      | US West (N. California)   | Global, US                 |
| `us-west-2`      | US West (Oregon)          | Global, US, In-region only |

## Quotas

Default quota is 2 million input tokens per minute (TPM). You can request up to 4 million input TPM without additional Anthropic approval. AWS enforces requests-per-minute (RPM) limits on the Bedrock side; contact AWS support for RPM adjustments.

## Data retention

Data handling for this offering is governed by Amazon Bedrock. For details, see [Data protection in Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/data-protection.html).

## Monitoring and logging

Claude in Amazon Bedrock emits logs to both CloudWatch and CloudTrail. Anthropic recommends retaining activity logs on at least a 30-day rolling basis to understand usage patterns and investigate potential issues.

## Support

For support, contact **[bedrock-ant-eap@amazon.com](mailto:bedrock-ant-eap@amazon.com)**. Include your AWS account ID and the `request-id` from any failed API responses.

<Note>
  **Claude Mythos Preview** is a research preview model available to invited customers on Amazon Bedrock. For more information, see [Project Glasswing](https://anthropic.com/glasswing).
</Note>
