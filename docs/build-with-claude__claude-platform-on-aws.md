# Claude Platform on AWS

Access Claude's full platform capabilities through AWS with Anthropic-managed infrastructure.

---

Claude Platform on AWS gives you the full Anthropic platform experience, including the Messages API, Agent Skills, code execution, and beta features, accessible through your AWS account. Unlike [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock), where AWS operates the inference stack, Anthropic operates Claude Platform on AWS. AWS provides the authentication layer (SigV4 or API key), IAM-based access control, and billing integration through AWS Marketplace.

<Note>
  The Anthropic SDKs support Claude Platform on AWS.
</Note>

## How the platform integration works

Claude models run on Anthropic-managed infrastructure. This is a commercial integration for billing and access through AWS. Anthropic is the data processor for inference inputs and outputs; AWS processes billing and identity metadata under the marketplace model. Customers using Claude through Claude Platform on AWS are subject to Anthropic's [data use terms](https://www.anthropic.com/legal). Anthropic continues to provide its industry-leading safety and data commitments.

Note the following operational characteristics: data may not reside in AWS; inference may route to Anthropic's primary cloud; and subservices may move under the hood without notice. Set the [`inference_geo`](#data-residency) parameter per request to pin inference to a specific geography.

Claude Platform on AWS follows the same data retention policy as the first-party Claude API. Zero Data Retention (ZDR) is available on request. Contact your Anthropic account representative to enable it for your organization.

## Claude Platform on AWS vs Amazon Bedrock

Both offerings let you use Claude through AWS, but they differ significantly in architecture, API surface, and feature availability.

| Aspect                       | Claude Platform on AWS                                                                          | [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) | [Amazon Bedrock (legacy)](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy) |
| ---------------------------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| **Who operates the stack**   | Anthropic                                                                                       | AWS                                                                             | AWS                                                                                   |
| **API surface**              | Claude API (`/v1/{endpoint}`)                                                                   | Messages API at `/anthropic/v1/messages`                                        | Bedrock Converse / InvokeModel                                                        |
| **Feature availability**     | Typically same-day as Claude API (see [feature limitations](#features-not-supported))           | Per Amazon Bedrock release schedule                                             | Per Amazon Bedrock release schedule                                                   |
| **Agent Skills**             | Available (beta)                                                                                | Not available (requires code execution)                                         | Not available                                                                         |
| **Beta features**            | Pass through with `anthropic-beta` headers (see [feature limitations](#features-not-supported)) | `anthropic-beta` header not supported                                           | `anthropic-beta` header not supported                                                 |
| **Authentication**           | AWS IAM / SigV4 or API key                                                                      | AWS IAM / SigV4                                                                 | AWS IAM / SigV4 or bearer token                                                       |
| **Billing**                  | AWS Marketplace                                                                                 | AWS (native service)                                                            | AWS (native service)                                                                  |
| **Base URL**                 | `aws-external-anthropic.{region}.api.aws`                                                       | `bedrock-mantle.{region}.api.aws`                                               | `bedrock-runtime.{region}.amazonaws.com`                                              |
| **SDK client**               | Platform-specific client class (for example, `AnthropicAWS` in Python), in beta                 | `AnthropicBedrockMantle`                                                        | `AnthropicBedrock` / Bedrock SDK                                                      |
| **Console**                  | Claude Console (`platform.claude.com`, access through the AWS Console)                          | Bedrock Console                                                                 | Bedrock Console                                                                       |
| **Rate limits and quotas**   | Managed by Anthropic                                                                            | Managed by AWS                                                                  | Managed by AWS                                                                        |
| **Inference data processor** | Anthropic                                                                                       | AWS                                                                             | AWS                                                                                   |

If you need AWS-operated Claude, see [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock). Claude Platform on AWS uses a separate capacity pool from both the first-party Claude API and Amazon Bedrock. You can run workloads on more than one platform and fail over between them.

[AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html) is supported for connecting your VPC to the Claude Platform on AWS endpoint.

**When to choose Bedrock:** Organizations in regulated industries that require FedRAMP High, IL4, IL5, or HIPAA-ready compliance, or that need AWS to be the sole data processor, should use [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock). Bedrock runs entirely on AWS-controlled infrastructure with AWS as the operating party.

## Set up your account

Setting up Claude Platform on AWS happens in four phases: sign up on the AWS Console service page, complete your Anthropic organization setup, note your workspace ID, and sign in to the Claude Console.

<Note>
  Signing up through the AWS Console provisions a new Anthropic organization tied to your AWS account. This organization is separate from any existing organizations your company has with Anthropic, including Claude Enterprise organizations procured through AWS Marketplace. API keys, workspaces, and Claude Console settings from a first-party Anthropic organization don't carry over.

  If you have an existing Amazon Bedrock private offer, contact your Anthropic or AWS account representative before signing up so your discount applies from your first request. Discounts cannot be applied retroactively to usage incurred before your private offer is accepted. See [Private offers](/docs/en/about-claude/pricing#private-offers).
</Note>

<Steps>
  <Step title="Sign up in the AWS Console">
    1. Open the [AWS Console](https://console.aws.amazon.com/) and navigate to the **Claude Platform on AWS** service page.
    2. Choose **Sign up**.
    3. On the Sign-up page, review the terms (Anthropic's End User License Agreement, the AWS Privacy Notice, and the AWS Customer Agreement) and select the agreement checkbox.
    4. Choose **Continue**.

    The page shows a **Sign-up in progress** banner. Stay on the page. Sign-up takes a few minutes while AWS handles the AWS Marketplace subscription for you, then redirects you automatically.

    If your organization has a private offer from Anthropic, the Console looks it up and prompts you to accept it in AWS Marketplace. See [Private offers](/docs/en/about-claude/pricing#private-offers) for details.

    <Note>
      If you use Claude Platform on AWS, your content (such as prompts and completions) is processed by Anthropic outside of AWS. See Anthropic's [data use policies](https://www.anthropic.com/legal) for details on how content and metadata are processed and stored.
    </Note>
  </Step>

  <Step title="Set up your Anthropic organization">
    After sign-up completes, you're redirected to `platform.claude.com/partner-signup`.

    1. Enter the email address of your organization's owner and choose **Get started**.
    2. Check that email inbox for a setup link and follow it. If your browser shows a **Signed in as a different account** page, choose **Log out and continue**.
    3. Complete the organization details form (organization name, entity type, country, intended use) and choose **Complete setup**.

    Completing setup creates your Anthropic organization and accepts Anthropic's Commercial Terms of Service and Usage Policy. The AWS Console service page now shows a left navigation with **Home**, **API keys**, **Quickstart**, and **Workspaces**.
  </Step>

  <Step title="Create your workspace and note its ID">
    After you complete setup, the AWS Console prompts you to create a workspace. See [Workspaces](#workspaces) for details on region binding, IAM resource scoping, and creating additional workspaces.

    Find the workspace ID under **Workspaces** on the AWS Console **Claude Platform on AWS** service page or in the [Claude Console](#using-the-claude-console). Workspace IDs use the format `wrkspc_` followed by an alphanumeric identifier.
  </Step>

  <Step title="Sign in to the Claude Console">
    Access to the Claude Console is federated through AWS IAM:

    1. Assume an IAM role with the `aws-external-anthropic:AssumeConsole` permission. See [IAM actions for Claude Platform on AWS](/docs/en/api/claude-platform-on-aws-iam-actions#console-access).
    2. From the **Claude Platform on AWS** service page, choose **Open Claude Console**. The AWS Console issues a JWT and redirects you to `platform.claude.com`.
    3. On first sign-in, you're prompted for an email address. Enter your work email. The platform provisions your Claude Console user just-in-time.

    When you're signed in through the AWS Console, the Claude Console scopes to your Claude Platform on AWS organization. An **Account managed by AWS** indicator appears in the bottom-left of the Claude Console sidebar.
  </Step>
</Steps>

### Troubleshooting account setup

* **"Sign-up failed: Failed to enable OutboundWebIdentityFederation":** If you see this banner on first submit, choose **Continue** again. The IAM enablement can take a moment to take effect.
* **No progress indicator during sign-up:** Sign-up takes a few minutes. The page shows a static **Sign-up in progress** banner without a progress bar while AWS provisions your account.
* **"Signed in as a different account" after following the setup link:** Choose **Log out and continue**. The page reauthenticates you with the email address you entered.
* **"Not found" message during sign-in:** This message might appear briefly during redirect. You can dismiss it.
* **Usage page shows no data after your first API call:** Usage data can take a few minutes to appear in the Claude Console.

## Before making API calls

Ensure you have:

1. An active AWS account with a subscription to Claude Platform on AWS (see [Set up your account](#set-up-your-account))
2. The [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) installed and configured
3. **Outbound web identity federation enabled** on your AWS account (a one-time setup step; see [Enable outbound web identity federation](#enable-outbound-web-identity-federation))
4. Your workspace ID (see [Obtain your workspace ID](#obtain-your-workspace-id))

### Enable outbound web identity federation

The Claude Platform on AWS gateway calls `sts:GetWebIdentityToken` server-side to mint a JWT it forwards to Anthropic. This STS capability is **disabled by default** on every AWS account. Enable it once per account:

```bash CLI
aws iam enable-outbound-web-identity-federation
```

If the response is `[ERROR] (FeatureEnabled) ... already enabled`, the setting is already on for your account and you can move on. Verify and retrieve your account's issuer URL:

```bash CLI
aws iam get-outbound-web-identity-federation-info
```

<Warning>
  Without this step, every request returns `"Outbound web identity federation is disabled for your account"`. This is the most common setup error.
</Warning>

### Obtain your workspace ID

You create a workspace from the AWS Console after completing account setup (see [Set up your account](#set-up-your-account)). Workspaces are bound to a single AWS region. You can find the workspace ID in the [Claude Console](#using-the-claude-console) under **Workspaces** or in the **Workspaces** section of the AWS Console service page.

Set the `ANTHROPIC_AWS_WORKSPACE_ID` and `AWS_REGION` environment variables so the SDK clients read them automatically:

```bash CLI
export ANTHROPIC_AWS_WORKSPACE_ID='wrkspc_01AbCdEf23GhIj'
export AWS_REGION='us-west-2'  # Your workspace's AWS region
```

The region is required. The SDK client raises an error if no region is set. Pass `aws_region`/`awsRegion` to the constructor, or set `AWS_REGION` (or `AWS_DEFAULT_REGION`). All AWS commercial regions are supported.

## Authentication

Claude Platform on AWS supports two authentication methods: AWS IAM with SigV4 request signing (primary) and API key authentication. Both use the same base URL and request format.

### SigV4 authentication

SigV4 is the enterprise-native path and integrates with your existing AWS IAM policies, roles, and auditing. Configure AWS credentials using any method supported by the [AWS default credential provider chain](https://docs.aws.amazon.com/sdkref/latest/guide/standardized-credentials.html):

* Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`)
* Shared credentials file (`~/.aws/credentials`)
* Shared config file (`~/.aws/config`) including SSO and `credential_process`
* Web identity (`AWS_WEB_IDENTITY_TOKEN_FILE` and `AWS_ROLE_ARN`) for IRSA and GitHub Actions
* ECS container credentials
* EC2 instance metadata service (IMDS)

Verify that your credentials are working:

```bash CLI
aws sts get-caller-identity
```

### API key authentication

For simpler integration paths (local development and scripts), you can authenticate with an API key instead of SigV4. Set the `ANTHROPIC_AWS_API_KEY` environment variable or pass `apiKey` to the SDK constructor.

Generate API keys in the **AWS Console** under **Claude Platform on AWS → API keys**. Choose **Generate a key**, then copy the key value. Grant the `aws-external-anthropic:CallWithBearerToken` IAM action to the principals that should be allowed to use API key authentication.

<Note>
  API keys for Claude Platform on AWS are managed in the AWS Console, not the Claude Console. Keys created in the standard [Claude Console](https://platform.claude.com/) (for first-party API access) don't work with the Claude Platform on AWS endpoint.
</Note>

#### Short-term API keys

For workloads that need to hand a credential to a separate process (such as an LLM gateway, a serverless function, or a tool that supports bearer-token authentication but not SigV4), generate a short-term API key from your AWS credentials instead of provisioning a long-lived key in the AWS Console.

AWS publishes token-generator libraries for [JavaScript](https://github.com/aws/token-generator-for-aws-external-anthropic-js), [Python](https://github.com/aws/token-generator-for-aws-external-anthropic-python), and [Java](https://github.com/aws/token-generator-for-aws-external-anthropic-java). Each library reads your AWS credentials through the standard provider chain and returns a time-limited token that works with the `x-api-key` header. Token lifetime defaults to 12 hours and is capped at the lesser of your requested duration, your AWS credentials' expiry, and 12 hours. See the linked repository READMEs for installation and full configuration options.

Pass the generated token to the SDK the same way you'd pass an AWS Console-generated API key:

<CodeGroup>
  ```python Python
  from token_generator_for_aws_external_anthropic import TokenGenerator
  from anthropic import AnthropicAWS

  token = TokenGenerator(region="us-west-2").get_token()

  client = AnthropicAWS(api_key=token, aws_region="us-west-2")
  ```

  ```typescript TypeScript
  import { getTokenProvider } from "@aws/token-generator-for-aws-external-anthropic";
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const tokenProvider = getTokenProvider({ region: "us-west-2" });
  const token = await tokenProvider();

  const client = new AnthropicAws({ apiKey: token, awsRegion: "us-west-2" });
  ```

  ```java Java
  import software.amazon.awsexternalanthropic.TokenGenerator;
  import software.amazon.awssdk.regions.Region;
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;

  void main() {
      String token = TokenGenerator.builder().region(Region.US_WEST_2).build().getToken();

      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.builder()
              .apiKey(token)
              .region(Region.US_WEST_2)
              .workspaceId(System.getenv("ANTHROPIC_AWS_WORKSPACE_ID"))
              .build())
          .build();
  }
  ```
</CodeGroup>

If you can generate the token locally, your process already has SigV4 credentials, and SigV4 authentication is usually the simpler choice. Use short-term keys when the process making API calls is separate from the process that holds AWS credentials.

The SDK does not refresh short-term keys automatically. When a token expires, generate a new one and construct a new client. The principal that uses the token still needs the `aws-external-anthropic:CallWithBearerToken` IAM action.

### Credential precedence

The platform-specific client resolves authentication in the following order. Argument names vary by language convention (TypeScript and PHP use camelCase as shown; Python and Ruby use snake\_case; Go uses PascalCase with capitalized acronyms; C# and Java use the language's property or builder idioms).

1. `apiKey` constructor argument → `x-api-key` header
2. `awsAccessKey` + `awsSecretAccessKey` constructor arguments → AWS SigV4
3. `awsProfile` constructor argument → AWS SigV4 with named profile
4. `ANTHROPIC_AWS_API_KEY` environment variable → `x-api-key` header
5. Default AWS credential provider chain → AWS SigV4

### Region resolution

The client reads `AWS_REGION` from the environment if `aws_region`/`awsRegion` is not passed to the constructor, falling back to `AWS_DEFAULT_REGION` for compatibility with the standard AWS SDKs. Region is required; there is no fallback default. Unlike `AnthropicBedrock`, which falls back to `us-east-1`, the `AnthropicAWS`/`AnthropicAws` client raises an error if neither the constructor argument nor the environment variable is set.

## Install an SDK

Anthropic's [client SDKs](/docs/en/cli-sdks-libraries/overview) support Claude Platform on AWS. Each SDK provides a platform-specific client class that handles SigV4 signing, region-based base URL construction, and the `anthropic-workspace-id` header.

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic[aws]"
    ```

    <Tip>
      On macOS with Homebrew Python or other externally managed Python environments, `pip install` can fail with a PEP 668 `externally-managed-environment` error. Create and activate a virtual environment first: `python3 -m venv .venv && source .venv/bin/activate`.
    </Tip>
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/aws-sdk
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Aws
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="Java">
    ```kotlin Gradle
    implementation("com.anthropic:anthropic-java-aws:2.47.1")
    ```

    ```xml Maven
    <dependency>
      <groupId>com.anthropic</groupId>
      <artifactId>anthropic-java-aws</artifactId>
      <version>2.47.1</version>
    </dependency>
    ```
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk aws/aws-sdk-php
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    gem install anthropic aws-sdk-core
    ```
  </Tab>
</Tabs>

<Note>
  SDK clients for Claude Platform on AWS are in beta.
</Note>

## Available models

The following models are available on Claude Platform on AWS:

| Model             | Model ID          |
| ----------------- | ----------------- |
| Claude Fable 5    | claude-fable-5    |
| Claude Opus 4.8   | claude-opus-4-8   |
| Claude Opus 4.7   | claude-opus-4-7   |
| Claude Opus 4.6   | claude-opus-4-6   |
| Claude Sonnet 5   | claude-sonnet-5   |
| Claude Sonnet 4.6 | claude-sonnet-4-6 |
| Claude Opus 4.5   | claude-opus-4-5   |
| Claude Sonnet 4.5 | claude-sonnet-4-5 |
| Claude Haiku 4.5  | claude-haiku-4-5  |

Model IDs are identical to the first-party Claude API. There are no Bedrock-style ARNs or `anthropic.` prefixes.

New models launch on Claude Platform on AWS simultaneously with the first-party Claude API.

<Tip>
  Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform. See [Migrating to a newer Claude model](/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Making requests

Claude Platform on AWS uses the same API endpoints as the first-party Claude API. The differences are the base URL, the authentication method, and a required `anthropic-workspace-id` header that identifies which [workspace](#workspaces) the request targets.

<CodeGroup>
  ```bash cURL
  # Replace us-west-2 with your AWS region in both the URL and --aws-sigv4
  curl "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
    --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```python Python
  from anthropic import AnthropicAWS

  client = AnthropicAWS()

  message = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message)
  ```

  ```typescript TypeScript
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const client = new AnthropicAws();

  const message = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Aws;

  var client = new AnthropicAwsClient();

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
  if err != nil {
  	panic(err)
  }

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:     anthropic.ModelClaudeSonnet5,
  	MaxTokens: 1024,
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.fromEnv())
          .build();

      Message message = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .addUserMessage("Hello!")
              .build()
      );

      IO.println(message);
  }
  ```

  ```php PHP
  use Anthropic\Aws\Client;

  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-sonnet-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello!']],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::AWSClient.new

  message = client.messages.create(
    model: "claude-sonnet-5",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  )

  puts message
  ```
</CodeGroup>

The client reads `AWS_REGION` (or `AWS_DEFAULT_REGION`) and `ANTHROPIC_AWS_WORKSPACE_ID` from the environment. You can override either by passing `aws_region` / `awsRegion` or `workspace_id` / `workspaceId` to the constructor. Both region and workspace ID are required. The constructor raises an error if the workspace ID cannot be resolved; a missing region likewise raises an error.

<Note>
  The `x-amz-security-token` header (cURL) is only required for temporary credentials such as IAM roles, SSO, or STS. Omit it when using long-term IAM user credentials. The SDK clients handle this automatically based on the credential source.
</Note>

The `--aws-sigv4` value follows the format `aws:amz:<region>:<service>`. The SigV4 service name is `aws-external-anthropic`, and the region must match the region in your endpoint URL. A mismatch in either produces a generic signature-rejection error rather than a specific diagnostic.

### Context window

Context-window sizes on Claude Platform on AWS are identical to the first-party Claude API. See [Context windows](/docs/en/build-with-claude/context-windows) for per-model limits.

## Feature support

Claude Platform on AWS uses Claude API endpoints directly, which means you get full feature parity with the first-party Claude API (except where noted in the [feature limitations](#features-not-supported)):

* **Feature access:** Because Anthropic operates both platforms, most new features and beta headers become available on Claude Platform on AWS without a separate integration step. See [feature limitations](#features-not-supported) for exceptions.
* **Beta features:** Pass the standard `anthropic-beta` header to access beta features, just as you would with the Claude API.
* **Agent Skills:** Use pre-built and custom [Agent Skills](/docs/en/agents-and-tools/agent-skills/overview) with the same `container.skills` parameter and beta headers as the Claude API. All pre-built Skills (PowerPoint, Excel, Word, PDF) work out of the box.
* **Code execution:** Run code in Anthropic's managed sandbox using the [code execution tool](/docs/en/agents-and-tools/tool-use/code-execution-tool).
* **Tool use:** Computer use and all other [tool use capabilities](/docs/en/agents-and-tools/tool-use/overview) are available.
* **Extended thinking:** Enable extended thinking with the same parameters as the Claude API.
* **Streaming:** Full SSE streaming support for real-time responses.
* **Batch processing:** Submit batch requests for high-throughput workloads.
* **Prompt caching:** Cache tools, system prompts, and message history to reduce latency and cost. All prompt caching capabilities (5-minute TTL, 1-hour TTL, and automatic caching) are available.
* **Files API:** Upload and reference files across requests.
* **Customer-managed encryption keys (CMEK):** [CMEK](/docs/en/manage-claude/cmek) is available with [AWS KMS](/docs/en/manage-claude/cmek-aws-kms) keys only; Google Cloud KMS and Azure Key Vault keys cannot be registered. Create, validate, and attach keys in the [Claude Console](#using-the-claude-console); the `external_keys` Admin API endpoints are not currently available. The key must be in the same AWS region as the workspace it is attached to.
* **Compliance API:** The [Compliance API](/docs/en/manage-claude/compliance-api) is available. Access is authorized through AWS IAM.

See the [comparison table](#claude-platform-on-aws-vs-amazon-bedrock) for feature-availability differences from Amazon Bedrock.

### Claude Managed Agents

[Claude Managed Agents](/docs/en/managed-agents/overview) is available on Claude Platform on AWS, including [agents](/docs/en/managed-agents/agent-setup), [environments](/docs/en/managed-agents/environments), [sessions](/docs/en/managed-agents/sessions), [credential vaults](/docs/en/managed-agents/vaults), [memory stores](/docs/en/managed-agents/memory), [webhooks](/docs/en/managed-agents/webhooks), [multiagent orchestration](/docs/en/managed-agents/multi-agent), and [self-hosted sandboxes](/docs/en/managed-agents/self-hosted-sandboxes).

Session behavior on Claude Platform on AWS differs from first-party Claude Managed Agents in one way:

* **Autonomous-session reauthentication:** A session can run autonomously, without any [user events](/docs/en/managed-agents/reference#event-types), for up to 6 hours. After 6 hours, the session requires reauthentication before it continues. To reauthenticate, send any user-role event to the session (see [Events and streaming](/docs/en/managed-agents/events-and-streaming)). First-party Claude Managed Agents has no autonomous-session runtime limit.

### Features not supported

The following capabilities are not currently available on Claude Platform on AWS:

* **HIPAA readiness:** Anthropic's HIPAA-ready program is not available. See [API and data retention](/docs/en/manage-claude/api-and-data-retention).

- **Admin API:** Workspace endpoints (create, get, list, update, and archive on `/v1/organizations/workspaces`) are available. Other Admin API endpoints (organization members, workspace members, invites, API keys, usage reports, cost reports, rate limit reports, and external keys) are not currently available. Manage [CMEK](/docs/en/manage-claude/cmek) keys in the Claude Console instead. View usage and cost data in the [Claude Console](#using-the-claude-console) instead. AWS IAM manages organization membership.
- **Workspace member management:** Adding or removing users from individual workspaces is not available. AWS IAM policies on workspace ARNs control access.
- **Spend limits:** Not available. Rely on AWS billing controls instead.
- **Claude Code workspace and Analytics API:** The Claude Code workspace with automatic rate limits is not available. Claude Code usage appears in the general usage view rather than a dedicated screen.
- **OAuth authentication:** Not supported. Use SigV4 or API key authentication.
- **Fast mode:** Not available on Claude Platform on AWS.
- **OpenAI-compatible API endpoints:** Not available on Claude Platform on AWS.
- **MCP tunnels:** Only MCP servers exposed over the public internet are supported.

## Data residency

Claude Platform on AWS supports the following inference geographies:

* **US:** Inference stays within US data centers. A 1.1x pricing multiplier applies.
* **Global:** Inference can route to any Anthropic-operated data center worldwide. Standard pricing applies.

<Note>
  The AWS region your workspace is bound to controls which gateway endpoint you call and where AWS-side resources (IAM, CloudTrail, billing) are scoped. It does not pin where model inference runs. To pin inference to a specific geography, set `inference_geo` on each request or configure a workspace default.
</Note>

Set the inference geography per request with the `inference_geo` parameter:

<Note>
  The `inference_geo` parameter is supported on Claude Opus 4.6, Claude Sonnet 4.6, and later models. Requests with `inference_geo` on Claude Opus 4.5, Claude Sonnet 4.5, or Claude Haiku 4.5 return a 400 error. See [Data residency](/docs/en/manage-claude/data-residency) for model availability details.
</Note>

<CodeGroup>
  ```bash cURL
  # Replace us-west-2 with your AWS region in both the URL and --aws-sigv4
  curl "https://aws-external-anthropic.us-west-2.api.aws/v1/messages" \
    --aws-sigv4 "aws:amz:us-west-2:aws-external-anthropic" \
    --user "$AWS_ACCESS_KEY_ID:$AWS_SECRET_ACCESS_KEY" \
    -H "x-amz-security-token: $AWS_SESSION_TOKEN" \
    -H "content-type: application/json" \
    -H "anthropic-version: 2023-06-01" \
    -H "anthropic-workspace-id: $ANTHROPIC_AWS_WORKSPACE_ID" \
    -d '{
      "model": "claude-sonnet-5",
      "max_tokens": 1024,
      "inference_geo": "us",
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```python Python
  from anthropic import AnthropicAWS

  client = AnthropicAWS()
  message = client.messages.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      inference_geo="us",
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message)
  ```

  ```typescript TypeScript
  import AnthropicAws from "@anthropic-ai/aws-sdk";
  const client = new AnthropicAws();
  const message = await client.messages.create({
    model: "claude-sonnet-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Aws;

  var client = new AnthropicAwsClient();

  var message = await client.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      InferenceGeo = "us",
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  Console.WriteLine(message);
  ```

  ```go Go
  client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
  if err != nil {
  	panic(err)
  }

  message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  	Model:        anthropic.ModelClaudeSonnet5,
  	MaxTokens:    1024,
  	InferenceGeo: anthropic.String("us"),
  	Messages: []anthropic.MessageParam{
  		anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  	},
  })
  if err != nil {
  	panic(err)
  }

  fmt.Println(message)
  ```

  ```java Java
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.fromEnv())
          .build();

      Message message = client.messages().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .inferenceGeo("us")
              .addUserMessage("Hello!")
              .build()
      );

      IO.println(message);
  }
  ```

  ```php PHP
  use Anthropic\Aws\Client;

  $client = new Client();

  $message = $client->messages->create(
      model: 'claude-sonnet-5',
      maxTokens: 1024,
      inferenceGeo: 'us',
      messages: [['role' => 'user', 'content' => 'Hello!']],
  );

  echo $message;
  ```

  ```ruby Ruby
  require "anthropic"

  client = Anthropic::AWSClient.new

  message = client.messages.create(
    model: "claude-sonnet-5",
    max_tokens: 1024,
    inference_geo: "us",
    messages: [{ role: "user", content: "Hello!" }]
  )

  puts message
  ```
</CodeGroup>

If you omit `inference_geo`, the request uses the workspace's `default_inference_geo` if one is configured, otherwise `global`.

Workspace-level inference geography controls (`allowed_inference_geos` and `default_inference_geo`) are also available on Claude Platform on AWS. See [Workspace-level restrictions](/docs/en/manage-claude/data-residency#workspace-level-restrictions).

## Workspaces

Inference and resource requests on Claude Platform on AWS target a workspace. You pass the workspace's ID in the `anthropic-workspace-id` header on these API calls. Workspace IDs use the tagged format `wrkspc_` followed by an alphanumeric identifier (for example, `wrkspc_01AbCdEf23GhIj`). See [Obtain your workspace ID](#obtain-your-workspace-id) if you don't have it yet.

### Workspace scoping

Workspaces are bound to a single AWS region. A workspace created in `us-west-2` can only be accessed through the `us-west-2` endpoint. Usage, quotas, cost, files, batches, and Skills all roll up per workspace, giving you per-region breakdowns in the Claude Console.

Workspaces also serve as the primary IAM resource for Claude Platform on AWS. You grant or deny access to specific workspaces through AWS IAM policies using the workspace ARN. The ARN's resource segment is the same `wrkspc_`-prefixed ID you pass in the `anthropic-workspace-id` header:

```text wrap
arn:aws:aws-external-anthropic:{region}:{account-id}:workspace/{workspace-id}
```

For example:

```text wrap
arn:aws:aws-external-anthropic:us-west-2:123456789012:workspace/wrkspc_01AbCdEf23GhIj
```

See [IAM policies](#iam-policies) for policy examples.

### Managing workspaces

Create additional workspaces, rename a workspace, or archive a workspace from the AWS Console **Workspaces** page or with the [Admin API](/docs/en/manage-claude/admin-api) workspace endpoints. A new workspace is bound to the AWS region of the endpoint you call to create it (see [Workspace scoping](#workspace-scoping)). The Claude Console Workspaces page is read-only.

## Using the Claude Console

Claude Platform on AWS uses the standard Claude Console at [platform.claude.com](https://platform.claude.com). When you sign in from the AWS Console, an **Account managed by AWS** indicator appears in the bottom-left of the Claude Console sidebar and the Console scopes to your Claude Platform on AWS organization. It provides usage analytics, cost breakdowns, rate limit visibility, workspace visibility, and pages for managing files, Agent Skills, batch jobs, and Claude Managed Agents resources (agents, sessions, environments, credential vaults, memory stores, and webhooks).

### Signing in

Access to the Claude Console is federated through AWS IAM. See [Set up your account](#set-up-your-account) for the full first-time sign-in flow. In short:

1. Assume an IAM role with the `aws-external-anthropic:AssumeConsole` permission. See [IAM actions for Claude Platform on AWS](/docs/en/api/claude-platform-on-aws-iam-actions#console-access).
2. Navigate to the Claude Platform on AWS page in the [AWS Console](https://console.aws.amazon.com/).
3. Choose **Open Claude Console**. The AWS Console issues a JWT and redirects you to `platform.claude.com`.
4. On first sign-in, you're prompted for an email address; enter your work email. The platform provisions your Claude Console user just-in-time.

Two Claude Console roles are available: **Admin** and **Developer**. The Admin role grants access to all Claude Console pages and settings available for Claude Platform on AWS. The Developer role grants read access to usage, cost, rate limit, and workspace information. Contact your Anthropic account representative to assign the Admin or Developer role to a principal.

### Available pages

The **Through AWS gateway** column indicates whether the page reads and writes data through the AWS gateway (and is therefore governed by [IAM actions](/docs/en/api/claude-platform-on-aws-iam-actions)). Pages marked **No** read organization-level metadata directly from Anthropic and bypass IAM action checks.

| Page                  | Available | Through AWS gateway | Notes                                                                                                                                    |
| --------------------- | --------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Usage**             | Yes       | No                  | View token usage by model, workspace, and dimension. Data can take a few minutes to appear after a request.                              |
| **Cost**              | Yes       | No                  | View cost breakdowns by model and workspace. AWS Cost Explorer shows the aggregated [Claude Consumption Unit (CCU)](#billing) line item. |
| **Limits**            | Yes       | No                  | View rate limits (read-only).                                                                                                            |
| **Workspaces**        | Yes       | No                  | View per-region workspaces (read-only).                                                                                                  |
| **Files**             | Yes       | Yes                 | View and manage uploaded files.                                                                                                          |
| **Skills**            | Yes       | Yes                 | View and manage Agent Skills.                                                                                                            |
| **Batches**           | Yes       | Yes                 | View and manage batch processing jobs.                                                                                                   |
| **Agents**            | Yes       | Yes                 | View and manage agent definitions.                                                                                                       |
| **Sessions**          | Yes       | Yes                 | View agent sessions and event history.                                                                                                   |
| **Environments**      | Yes       | Yes                 | View and manage cloud sandbox configurations for sessions.                                                                               |
| **Credential vaults** | Yes       | Yes                 | View and manage credential vaults for session authentication.                                                                            |
| **Memory stores**     | Yes       | Yes                 | View and manage persistent agent memory.                                                                                                 |
| **Webhooks**          | Yes       | Yes                 | View and manage webhook endpoints under **Settings → Webhooks**.                                                                         |
| **API keys**          | No        | N/A                 | Manage API keys in the AWS Console (**Claude Platform on AWS → API keys**). See [API key authentication](#api-key-authentication).       |
| **Members**           | No        | N/A                 | Not applicable. AWS IAM manages access.                                                                                                  |
| **Billing**           | No        | N/A                 | Not applicable. AWS Marketplace manages billing and invoicing. View cost breakdowns on the Cost page.                                    |
| **Claude Code**       | No        | N/A                 | View Claude Code usage on the Usage page.                                                                                                |

### Switching organizations

The Claude Console does not support organization switching for Claude Platform on AWS. To access a different organization, sign out and reauthenticate through the AWS Console using the IAM role for that organization's AWS account.

## Rate limits and quotas

Organizations on Claude Platform on AWS are placed on the Start tier. Anthropic manages rate limits directly, not through AWS quota systems.

Organizations on Claude Platform on AWS do not move between usage tiers automatically. To request higher limits, contact your Anthropic account representative. For tier details and per-model limits, see [Rate limits](/docs/en/api/rate-limits).

## Billing

Claude Platform on AWS bills through [AWS Marketplace](https://aws.amazon.com/marketplace). Usage is denominated in Claude Consumption Units (CCUs), metered hourly, and invoiced monthly in arrears on your AWS bill. CCUs are not prepaid credits; there is no CCU balance or commitment.

For the CCU price, conversion mechanics, discount application, and per-model token rates, see [Claude Platform on AWS pricing](/docs/en/about-claude/pricing#claude-platform-on-aws-pricing).

## Monitoring and logging

AWS CloudTrail can capture all requests to Claude Platform on AWS. Workspace, vault, and webhook operations are logged as Management events by default. Inference, batch, file, skill, model, user profile, and Claude Managed Agents operations (other than vaults and webhooks) are classified as Data events and require explicit data event logging configuration, which incurs additional CloudTrail charges. See the [IAM actions reference](/docs/en/api/claude-platform-on-aws-iam-actions#route-to-action-mapping) for the full event type classification and the [AWS CloudTrail documentation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/) for configuration details.

### Request IDs

Each response includes two request IDs in the response headers:

* **AWS request ID (`x-amzn-requestid`):** The primary ID, indexed in CloudTrail. Use this when investigating requests through AWS tooling or when contacting AWS support.
* **Anthropic request ID (`request-id`):** The secondary ID. Use this when contacting Anthropic support.

<CodeGroup>
  ```python Python
  from anthropic import AnthropicAWS

  client = AnthropicAWS()

  response = client.messages.with_raw_response.create(
      model="claude-sonnet-5",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )

  print(response.headers.get("x-amzn-requestid"))  # AWS request ID
  print(response.headers.get("request-id"))  # Anthropic request ID

  message = response.parse()
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicAws from "@anthropic-ai/aws-sdk";

  const client = new AnthropicAws();

  const { data: message, response } = await client.messages
    .create({
      model: "claude-sonnet-5",
      max_tokens: 1024,
      messages: [{ role: "user", content: "Hello!" }]
    })
    .withResponse();

  console.log(response.headers.get("x-amzn-requestid")); // AWS request ID
  console.log(response.headers.get("request-id")); // Anthropic request ID
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic;
  using Anthropic.Aws;

  var client = new AnthropicAwsClient();

  var response = await client.WithRawResponse.Messages.Create(new()
  {
      Model = Model.ClaudeSonnet5,
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }]
  });

  Console.WriteLine(response.Headers.GetValues("x-amzn-requestid").First()); // AWS request ID
  Console.WriteLine(response.Headers.GetValues("request-id").First()); // Anthropic request ID
  Console.WriteLine(response.Value.Content);
  ```

  ```go Go
  client, err := anthropicaws.NewClient(context.Background(), anthropicaws.ClientConfig{})
  if err != nil {
  	panic(err)
  }

  var response *http.Response
  message, err := client.Messages.New(
  	context.Background(),
  	anthropic.MessageNewParams{
  		Model:     anthropic.ModelClaudeSonnet5,
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  		},
  	},
  	option.WithResponseInto(&response),
  )
  if err != nil {
  	panic(err)
  }

  fmt.Println(response.Header.Get("x-amzn-requestid")) // AWS request ID
  fmt.Println(response.Header.Get("request-id"))       // Anthropic request ID
  fmt.Println(message.Content)
  ```

  ```java Java
  import com.anthropic.aws.backends.AwsBackend;
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.core.http.HttpResponseFor;
  import com.anthropic.models.messages.Message;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.anthropic.models.messages.Model;

  void main() {
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(AwsBackend.fromEnv())
          .build();

      HttpResponseFor<Message> response = client.messages().withRawResponse().create(
          MessageCreateParams.builder()
              .model(Model.CLAUDE_SONNET_5)
              .maxTokens(1024)
              .addUserMessage("Hello!")
              .build()
      );

      IO.println(response.headers().values("x-amzn-requestid").get(0)); // AWS request ID
      IO.println(response.requestId().orElse(null)); // Anthropic request ID
      IO.println(response.parse().content());
  }
  ```

  ```php PHP
  use Anthropic\Aws\Client;

  $client = new Client();

  $response = $client->messages->raw->create(
      model: 'claude-sonnet-5',
      maxTokens: 1024,
      messages: [['role' => 'user', 'content' => 'Hello!']],
  );

  echo $response->getHeaderLine('x-amzn-requestid') . "\n"; // AWS request ID
  echo $response->getHeaderLine('request-id') . "\n"; // Anthropic request ID
  echo $response->parse()->content;
  ```

  ```ruby Ruby
  # Accessing raw response headers is not currently supported in the Ruby SDK.
  # To inspect the x-amzn-requestid header, use one of the other SDK examples.
  ```
</CodeGroup>

Anthropic recommends logging your activity on at least a 30-day rolling basis to understand usage patterns and investigate any potential issues.

<Note>
  AWS CloudTrail is configured within your AWS account. Enabling logging does not provide AWS or Anthropic access to your content beyond what is necessary for billing and service operation.
</Note>

## Migrating from Amazon Bedrock

If you currently use Claude on Bedrock, migrating to Claude Platform on AWS requires changes throughout your integration. SigV4 signing remains supported, but the signing context, base URL, API format, model IDs, SDK client and package, streaming format, request headers, and region availability all change. The following table summarizes the differences.

### What changes

The migration delta depends on which Bedrock integration you're coming from. The following table shows both the [current Bedrock integration](/docs/en/build-with-claude/claude-in-amazon-bedrock) (Messages API at `bedrock-mantle.{region}.api.aws`) and the [legacy InvokeModel integration](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy).

| Aspect                  | From [Claude in Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock)                    | From [Amazon Bedrock (legacy)](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy)              | To Claude Platform on AWS                                                                     |
| ----------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| **Base URL**            | `bedrock-mantle.{region}.api.aws`                                                                       | `bedrock-runtime.{region}.amazonaws.com`                                                                | `aws-external-anthropic.{region}.api.aws`                                                     |
| **API format**          | Messages API at `/anthropic/v1/messages`                                                                | Bedrock Converse / InvokeModel                                                                          | Claude API (`/v1/{endpoint}`)                                                                 |
| **Model IDs**           | `anthropic.claude-haiku-4-5`                                                                            | `anthropic.claude-haiku-4-5-20251001-v1:0` (with a `us.` or `global.` inference profile prefix)         | `claude-haiku-4-5`                                                                            |
| **SDK client**          | `AnthropicBedrockMantle`                                                                                | `AnthropicBedrock` / Bedrock SDK                                                                        | Platform-specific client (see [Install an SDK](#install-an-sdk)), in beta                     |
| **SDK package**         | `anthropic[bedrock]`, `@anthropic-ai/bedrock-sdk`, and others                                           | `anthropic[bedrock]`, `@anthropic-ai/bedrock-sdk`, or AWS SDK                                           | `anthropic[aws]`, `@anthropic-ai/aws-sdk`, and others (see [Install an SDK](#install-an-sdk)) |
| **SigV4 service name**  | `bedrock-mantle`                                                                                        | `bedrock`                                                                                               | `aws-external-anthropic`                                                                      |
| **Streaming format**    | SSE                                                                                                     | AWS EventStream                                                                                         | SSE (same as Claude API)                                                                      |
| **Workspace header**    | Not applicable                                                                                          | Not applicable                                                                                          | `anthropic-workspace-id` required                                                             |
| **Region availability** | See [Amazon Bedrock regions](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) | See [Amazon Bedrock regions](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) | All AWS commercial regions                                                                    |

If you're on the current Bedrock integration, the request body format is already the Messages API; the changes are the base URL, SigV4 service name, model IDs, and adding the `anthropic-workspace-id` header. If you're on the legacy InvokeModel or Converse API, you'll also rewrite the request and response shapes to the Messages API format. See [Claude on Amazon Bedrock (legacy)](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy) for the request-shape mapping.

### What you gain

* Typically same-day access to new models and features (see [feature limitations](#features-not-supported))
* Agent Skills for document generation (PowerPoint, Excel, Word, PDF)
* Code execution in Anthropic's managed sandbox
* Beta features through the `anthropic-beta` header (see [feature limitations](#features-not-supported))
* Claude Console for quota visibility and usage analytics
* Direct Anthropic support
* API key authentication as an alternative to SigV4 (see [API key authentication](#api-key-authentication))

### What stays the same

* AWS IAM authentication (SigV4)
* AWS as the invoicing party (the billing channel changes from native AWS service to AWS Marketplace; see [Commercial considerations](#commercial-considerations))
* AWS commitment retirement

### Migration pitfalls

<Warning>
  **Enable outbound web identity federation first.** If your AWS account has not previously used Claude Platform on AWS, you must [enable outbound web identity federation](#enable-outbound-web-identity-federation) once per account before making requests. Without this step, all requests fail with a federation error (see [Enable outbound web identity federation](#enable-outbound-web-identity-federation) for the exact error and remediation). This step is not required for Bedrock.
</Warning>

<Warning>
  **Zero Data Retention (ZDR) is opt-in on Claude Platform on AWS.** On Bedrock, AWS is the data processor and Anthropic does not retain inference inputs or outputs; Anthropic's ZDR program does not apply there. On Claude Platform on AWS, Anthropic processes inference data as an independent data processor, and ZDR follows the first-party Claude API model: it is available on request through your Anthropic account representative. Confirm ZDR enrollment before migrating production workloads that depend on data-retention guarantees.
</Warning>

### Commercial considerations

* **Anthropic terms of service:** Using Claude Platform on AWS requires accepting Anthropic's Commercial Terms of Service and Usage Policy. If your organization hasn't already accepted these (for example, if you've only used Claude through Bedrock), you're prompted during account setup. See [Set up your account](#set-up-your-account).
* **Discounts and private offers:** Negotiated discounts and AWS Marketplace private offers don't transfer automatically between Bedrock and Claude Platform on AWS. Work with your Anthropic account representative to set up commercial terms for Claude Platform on AWS.

## IAM policies

Claude Platform on AWS integrates with AWS IAM for access control. You grant or deny access to specific API actions on specific workspaces using standard IAM policy syntax.

The SigV4 service name and IAM action namespace is `aws-external-anthropic`. Actions follow the pattern `aws-external-anthropic:<Action>` (for example, `aws-external-anthropic:CreateInference`).

### Example: deny batch inference

The following policy allows real-time inference while blocking batch processing:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "aws-external-anthropic:CreateInference",
        "aws-external-anthropic:CountTokens",
        "aws-external-anthropic:GetModel",
        "aws-external-anthropic:ListModels",
        "aws-external-anthropic:GetWorkspace"
      ],
      "Resource": "arn:aws:aws-external-anthropic:*:*:workspace/*"
    },
    {
      "Effect": "Allow",
      "Action": "aws-external-anthropic:ListWorkspaces",
      "Resource": "*"
    },
    {
      "Effect": "Deny",
      "Action": [
        "aws-external-anthropic:CreateBatchInference",
        "aws-external-anthropic:GetBatchInference",
        "aws-external-anthropic:ListBatchInferences"
      ],
      "Resource": "*"
    }
  ]
}
```

The `GetBatchInference` action authorizes both the batch metadata route and the batch results route. Denying it blocks both reads. For a Deny-only policy suitable for ZDR-sensitive workloads, see [Feature lockdown for a ZDR-sensitive workspace](/docs/en/api/claude-platform-on-aws-iam-actions#feature-lockdown-for-a-zdr-sensitive-workspace).

<Note>
  `ListWorkspaces` is account-scoped, so it appears in a separate Allow statement with `"Resource": "*"`. Specifying a workspace ARN on an account-scoped action has no effect (see [Provisioning automation](/docs/en/api/claude-platform-on-aws-iam-actions#provisioning-automation)).

  This policy assumes AWS SigV4 authentication. If the principal authenticates with an API key, also add `aws-external-anthropic:CallWithBearerToken` to the `"Resource": "*"` Allow statement. `CallWithBearerToken` is a route-less authentication-layer action that does not bind to a workspace ARN. See [Per-customer workspace isolation](/docs/en/api/claude-platform-on-aws-iam-actions#per-customer-workspace-isolation) for the two-statement pattern.
</Note>

### Managed policies

AWS provides five managed policies (`AnthropicFullAccess`, `AnthropicReadOnlyAccess`, `AnthropicInferenceAccess`, `AnthropicLimitedAccess`, and `AnthropicSelfHostedEnvironmentAccess`) for common access patterns. For the actions each policy grants, the complete list of IAM actions, the route-to-action mapping, and additional policy examples, see [IAM actions for Claude Platform on AWS](/docs/en/api/claude-platform-on-aws-iam-actions#managed-policies).

## Next steps

<CardGroup cols={2}>
  <Card title="Features overview" icon="stack" href="/docs/en/build-with-claude/overview">
    Explore Claude's advanced features and capabilities.
  </Card>

  <Card title="Pricing" icon="chart" href="/docs/en/about-claude/pricing#claude-platform-on-aws-pricing">
    Learn about Claude Platform on AWS pricing and Claude Consumption Unit rates.
  </Card>

  <Card title="Model deprecations" icon="arrow-clockwise" href="/docs/en/about-claude/model-deprecations">
    As safer and more capable models launch, Anthropic regularly retires older ones. See all API deprecations, along with recommended replacements.
  </Card>
</CardGroup>

## Additional resources

<CardGroup cols={2}>
  <Card title="Claude Console" icon="browser" href="https://platform.claude.com">
    View usage, cost, and workspaces in the Claude Console. Sign in through the AWS Console.
  </Card>

  <Card title="Claude in Amazon Bedrock" icon="cloud" href="/docs/en/build-with-claude/claude-in-amazon-bedrock">
    Use AWS-operated Claude if you need AWS as the sole data processor.
  </Card>

  <Card title="AWS Marketplace" icon="coins" href="https://aws.amazon.com/marketplace">
    Manage your AWS Marketplace subscription and billing.
  </Card>
</CardGroup>
