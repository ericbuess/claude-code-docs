# Claude in Microsoft Foundry

Access Claude models through Microsoft Foundry with Azure-native endpoints and authentication.

---

This guide shows you how to set up and make API calls to Claude in Microsoft Foundry using one of Anthropic's client SDKs or direct HTTP requests. When you access Claude in Microsoft Foundry, you are billed for Claude usage in the Azure Marketplace. You can use the latest Claude models, including Claude Opus 4.8 and Claude Sonnet 5, and features such as the [1M-token context window](/docs/en/build-with-claude/context-windows), while managing costs through your Azure subscription.

Claude is available in Global Standard and US Data Zone Standard deployment types in Foundry resources, billed in Claude Consumption Units through the Azure Marketplace. Visit [Claude in Microsoft Foundry pricing](/docs/en/about-claude/pricing#claude-in-microsoft-foundry-pricing) for details.

## Hosting options

Claude models in Microsoft Foundry are available in two hosting options. You choose the hosting option when you configure the deployment.

|                      | Hosted on Azure                                            | Hosted on Anthropic                                                                                             |
| -------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Where inference runs | Anthropic-operated service running on Azure infrastructure | Anthropic-operated service running on Anthropic infrastructure                                                  |
| Model availability   | The latest models in the Opus, Sonnet, and Haiku families  | All Claude models available on Microsoft Foundry                                                                |
| Deployment types     | Global Standard, US Data Zone Standard                     | Global Standard                                                                                                 |
| Recommended for      | Most workloads                                             | [Access to features or models not yet hosted on Azure](#additional-features-not-supported-when-hosted-on-azure) |

<Note>
  Anthropic acts as an independent processor for Microsoft. Customers using Claude through Microsoft Foundry are subject to Anthropic's data use terms. For deployments hosted on Azure, prompts and completions remain within Azure. Only usage metadata and content flagged by Anthropic's safety systems egress to Anthropic. Anthropic continues to provide its safety and data commitments.
</Note>

## Prerequisites

Before you begin, ensure you have:

* An active Azure subscription
* Access to [Foundry](https://ai.azure.com/)
* The [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) installed (required for the Entra ID cURL example, optional otherwise)
* An Azure RBAC role that allows you to use the resource, such as **Foundry User** (formerly Azure AI User) or **Cognitive Services User**

## Install an SDK

Anthropic's [client SDKs](/docs/en/cli-sdks-libraries/overview) support Foundry through a platform-specific package or client class. The examples on this page also show requests with cURL and the ant CLI. To set up the CLI, see [CLI quickstart](/docs/en/cli-sdks-libraries/cli/quickstart).

<Note>
  Foundry is supported by the C#, Java, PHP, Python, and TypeScript SDKs. Foundry is not currently available in the Go and Ruby SDKs.
</Note>

<Tabs>
  <Tab title="Python">
    ```bash
    pip install -U "anthropic"

    # For Entra ID authentication, also install the Azure Identity library
    pip install azure-identity
    ```
  </Tab>

  <Tab title="TypeScript">
    ```bash
    npm install @anthropic-ai/foundry-sdk

    # For Entra ID authentication, also install the Azure Identity library
    npm install @azure/identity
    ```
  </Tab>

  <Tab title="C#">
    ```bash
    dotnet add package Anthropic.Foundry
    ```
  </Tab>

  <Tab title="Go">
    ```bash
    # The Go SDK does not yet support Foundry natively (see the Authentication
    # examples for using the standard Go SDK as a workaround)
    go get github.com/anthropics/anthropic-sdk-go
    ```
  </Tab>

  <Tab title="Java">
    <Tabs>
      <Tab title="Gradle">
        ```kotlin
        implementation("com.anthropic:anthropic-java-foundry:2.48.0")

        // For Entra ID authentication, also add the Azure Identity library
        implementation("com.azure:azure-identity:1.18.3")
        ```
      </Tab>

      <Tab title="Maven">
        ```xml
        <dependency>
            <groupId>com.anthropic</groupId>
            <artifactId>anthropic-java-foundry</artifactId>
            <version>2.48.0</version>
        </dependency>
        <!-- For Entra ID authentication, also add the Azure Identity library -->
        <dependency>
            <groupId>com.azure</groupId>
            <artifactId>azure-identity</artifactId>
            <version>1.18.3</version>
        </dependency>
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="PHP">
    ```bash
    composer require anthropic-ai/sdk
    ```
  </Tab>

  <Tab title="Ruby">
    ```bash
    # The Ruby SDK does not yet support Foundry natively (see the Authentication
    # examples for using the standard Ruby SDK as a workaround)
    # Gemfile
    gem "anthropic"
    ```
  </Tab>
</Tabs>

## Provisioning

Foundry uses a two-level hierarchy: **resources** contain your security and billing configuration, while **deployments** are the model instances you call through the API. You'll first create a Foundry resource, then create one or more Claude deployments within it.

### Provisioning Foundry resources

Create a Foundry resource, which is required to use and manage services in Azure. You can follow these instructions to create a [Foundry resource](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#create-a-new-azure-ai-foundry-resource). Alternatively, you can start by creating a [Foundry project](https://learn.microsoft.com/en-us/azure/foundry/how-to/create-projects), which involves creating a Foundry resource.

To provision your resource:

1. Navigate to the [Foundry portal](https://ai.azure.com/).
2. Create a new Foundry resource or select an existing one.
3. Configure access management using Azure-issued API keys or Entra ID (formerly Azure Active Directory) for role-based access control.
4. Optionally configure the resource to be part of a private network (Azure Virtual Network) to restrict network access to your resource.
5. Note your resource name. You'll use this as `{resource}` in API endpoints (for example, `https://{resource}.services.ai.azure.com/anthropic/v1/*`).

### Creating Foundry deployments

After creating your resource, deploy a Claude model to make it available for API calls. These steps describe the new Foundry portal (the **New Foundry** toggle is on):

1. Sign in to the Foundry portal. From the portal homepage, select **Discover** in the upper-right navigation, then **Models** in the left pane to open the model catalog.

2. Search for and select a Claude model (for example, claude-opus-4-8). Each model appears once in the catalog regardless of how many hosting options it supports.

3. On the model card, select **Deploy**, then **Custom settings** to open the deployment settings pane. If you choose **Default settings** instead, the deployment is automatically configured as Hosted on Azure for models available in both hosting options.

4. On your first Claude deployment, review the Azure Marketplace terms, select an industry, and select **Agree and Proceed** to accept the terms and subscribe to the Azure Marketplace offer.

5. Configure the deployment:

   * **Deployment name:** Defaults to the model ID, but you can customize it (for example, `my-claude-deployment`). The deployment name cannot be changed after creation.
   * **Region scope:** Select Global, or for models hosted on Azure, Data Zone. Selecting Data Zone creates a US Data Zone Standard deployment, which keeps inference within the United States and is equivalent to setting [`inference_geo: "us"`](/docs/en/manage-claude/data-residency#inference-geo) on the Claude API.
   * **Model version:** Expand **Model version settings** and select a version from the **Model version** dropdown. Each [hosting option](#hosting-options) is listed as a separate model version, labeled with its hosting option (for example, version 1 for Hosted on Anthropic, version 2 for Hosted on Azure).

6. Select **Deploy** and wait for provisioning to complete.

7. Once deployed, select **Build** in the upper-right navigation, then **Models** in the left pane, and open your deployment. The **Details** tab shows the **Target URI** (your endpoint URL) and **Key** (your API key).

If the **New Foundry** toggle is off, you are in the classic portal layout. There, open **Model catalog** in the left pane to find and deploy a model, and open **Models + endpoints** (under **My assets**) to view your deployments and their endpoint details.

<Note>
  The deployment name you choose becomes the value you pass in the `model` parameter of your API requests. You can create multiple deployments of the same model with different names to manage separate configurations or rate limits.
</Note>

## Authentication

Claude in Microsoft Foundry supports two authentication methods: API keys and Entra ID tokens. Both methods use Azure-hosted endpoints in the format `https://{resource}.services.ai.azure.com/anthropic/v1/*`.

### API key authentication

After provisioning your Foundry Claude resource, you can obtain an API key from the Foundry portal:

1. In the Foundry portal, select **Build** in the upper-right navigation, then **Models** in the left pane.
2. Open your Claude deployment and select the **Details** tab.
3. Copy the **Key** value (and note the **Target URI** for your endpoint).
4. Use either the `api-key` or `x-api-key` header in your requests, or provide it to the SDK.

The Foundry SDKs require an API key and either a resource name or base URL. The C#, Java, PHP, Python, and TypeScript SDKs automatically read these from the following environment variables if they are defined:

* `ANTHROPIC_FOUNDRY_API_KEY` - Your API key
* `ANTHROPIC_FOUNDRY_RESOURCE` - Your resource name (for example, `example-resource`)
* `ANTHROPIC_FOUNDRY_BASE_URL` - Alternative to resource name: the full base URL (for example, `https://example-resource.services.ai.azure.com/anthropic/`). The C# SDK does not read this variable: it always constructs the base URL from the resource name.

<Note>
  The `resource` and `base_url` parameters are mutually exclusive. Provide either the resource name (which the SDK uses to construct the URL as `https://{resource}.services.ai.azure.com/anthropic/`) or the full base URL directly.
</Note>

**Example using API key:**

<CodeGroup>
  ```bash cURL
  curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
    -H "content-type: application/json" \
    -H "api-key: YOUR_AZURE_API_KEY" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # ant reads ANTHROPIC_API_KEY and sends it as x-api-key, which Foundry accepts
  export ANTHROPIC_API_KEY="YOUR_AZURE_API_KEY"

  ant messages create \
    --base-url https://example-resource.services.ai.azure.com/anthropic \
    --model claude-opus-4-8 \
    --max-tokens 1024 \
    --message '{role: user, content: "Hello!"}' \
    --transform content
  ```

  ```python Python
  import os
  from anthropic import AnthropicFoundry

  client = AnthropicFoundry(
      api_key=os.environ.get("ANTHROPIC_FOUNDRY_API_KEY"),
      resource="example-resource",  # your resource name
  )

  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicFoundry from "@anthropic-ai/foundry-sdk";

  const client = new AnthropicFoundry({
    apiKey: process.env.ANTHROPIC_FOUNDRY_API_KEY,
    resource: "example-resource" // your resource name
  });

  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic.Foundry;
  using Anthropic.Models.Messages;

  var client = new AnthropicFoundryClient(
      new AnthropicFoundryApiKeyCredentials(
          Environment.GetEnvironmentVariable("ANTHROPIC_FOUNDRY_API_KEY")!,
          "example-resource"
      )
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }],
  });

  Console.WriteLine(
      string.Join("", response.Content
          .Select(block => block.Value)
          .OfType<TextBlock>()
          .Select(textBlock => textBlock.Text)));
  ```

  ```go Go
  // The Go SDK does not yet support Foundry natively. This example uses the
  // standard Go SDK as a workaround. WithoutEnvironmentDefaults keeps the
  // client from also reading ANTHROPIC_API_KEY or ANTHROPIC_AUTH_TOKEN from
  // the environment and sending a Claude API credential to your Foundry
  // endpoint. Features that Foundry does not support fail server-side rather
  // than client-side. For full Foundry support, use the C#, Java, PHP,
  // Python, or TypeScript SDKs.
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func main() {
  	client := anthropic.NewClient(
  		option.WithoutEnvironmentDefaults(),
  		option.WithBaseURL("https://example-resource.services.ai.azure.com/anthropic"),
  		option.WithAPIKey(os.Getenv("ANTHROPIC_FOUNDRY_API_KEY")),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.foundry.backends.FoundryBackend;
  import com.anthropic.models.messages.MessageCreateParams;

  void main() {
      // Requires env vars: ANTHROPIC_FOUNDRY_API_KEY, ANTHROPIC_FOUNDRY_RESOURCE
      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(FoundryBackend.fromEnv())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-opus-4-8")
          .maxTokens(1024)
          .addUserMessage("Hello!")
          .build();

      client.messages().create(params).content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> System.out.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Foundry;

  $client = Foundry\Client::withCredentials(
      apiKey: getenv('ANTHROPIC_FOUNDRY_API_KEY'),
      baseUrl: 'https://example-resource.services.ai.azure.com/anthropic',
  );

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  # The Ruby SDK does not yet support Foundry natively. This example uses the
  # standard Ruby SDK as a workaround. Pass credentials explicitly: without
  # them, the client falls back to the ANTHROPIC_API_KEY or
  # ANTHROPIC_AUTH_TOKEN environment variables and could send a Claude API
  # credential to your Foundry endpoint. Features that Foundry
  # does not support fail server-side rather than client-side. For full
  # Foundry support, use the C#, Java, PHP, Python, or TypeScript SDKs.
  require "anthropic"

  client = Anthropic::Client.new(
    base_url: "https://example-resource.services.ai.azure.com/anthropic",
    api_key: ENV.fetch("ANTHROPIC_FOUNDRY_API_KEY")
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

<Warning>
  Keep your API keys secure. Never commit them to version control or share them publicly. Anyone with access to your API key can make requests to Claude through your Foundry resource.
</Warning>

### Microsoft Entra authentication

Entra ID authentication lets you manage access with Azure RBAC, integrate with your organization's identity management, and avoid handling API keys manually. To use Entra ID tokens:

1. Enable [Microsoft Entra ID authentication](https://learn.microsoft.com/en-us/azure/ai-foundry/model-inference/how-to/configure-entra-id) for your Foundry resource.
2. Obtain an access token from Entra ID.
3. Use the token in the `Authorization: Bearer {TOKEN}` header.

**Example using Entra ID:**

<CodeGroup>
  ```bash cURL
  # Get Microsoft Entra ID token
  ACCESS_TOKEN=$(az account get-access-token --resource https://ai.azure.com --query accessToken -o tsv)

  # Make request with token. Replace {resource} with your resource name
  curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
    -H "content-type: application/json" \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "anthropic-version: 2023-06-01" \
    -d '{
      "model": "claude-opus-4-8",
      "max_tokens": 1024,
      "messages": [
        {"role": "user", "content": "Hello!"}
      ]
    }'
  ```

  ```bash CLI
  # The ant CLI can send a bearer token with --auth-token, but a set
  # ANTHROPIC_API_KEY environment variable takes precedence over it (the CLI
  # prints only a console notice), so your request could authenticate with
  # the wrong credential. For the Entra ID flow, use the cURL example or one
  # of the SDK examples instead.
  ```

  ```python Python
  from anthropic import AnthropicFoundry
  from azure.identity import DefaultAzureCredential, get_bearer_token_provider

  # Get Microsoft Entra ID token using token provider pattern
  token_provider = get_bearer_token_provider(
      DefaultAzureCredential(), "https://ai.azure.com/.default"
  )

  # Create client with Entra ID authentication
  client = AnthropicFoundry(
      resource="example-resource",  # your resource name
      azure_ad_token_provider=token_provider,  # Use token provider for Entra ID auth
  )

  # Make request
  message = client.messages.create(
      model="claude-opus-4-8",
      max_tokens=1024,
      messages=[{"role": "user", "content": "Hello!"}],
  )
  print(message.content)
  ```

  ```typescript TypeScript
  import AnthropicFoundry from "@anthropic-ai/foundry-sdk";
  import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";

  // Get Entra ID token using token provider pattern
  const credential = new DefaultAzureCredential();
  const tokenProvider = getBearerTokenProvider(credential, "https://ai.azure.com/.default");

  // Create client with Entra ID authentication
  const client = new AnthropicFoundry({
    resource: "example-resource", // your resource name
    azureADTokenProvider: tokenProvider // Use token provider for Entra ID auth
  });

  // Make request
  const message = await client.messages.create({
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{ role: "user", content: "Hello!" }]
  });
  console.log(message.content);
  ```

  ```csharp C#
  using Anthropic.Foundry;
  using Anthropic.Models.Messages;
  using Azure.Identity;

  var client = new AnthropicFoundryClient(
      new AnthropicFoundryIdentityTokenCredentials(
          new DefaultAzureCredential(),
          "example-resource"
      )
  );

  var response = await client.Messages.Create(new MessageCreateParams
  {
      Model = "claude-opus-4-8",
      MaxTokens = 1024,
      Messages = [new() { Role = Role.User, Content = "Hello!" }],
  });

  Console.WriteLine(
      string.Join("", response.Content
          .Select(block => block.Value)
          .OfType<TextBlock>()
          .Select(textBlock => textBlock.Text)));
  ```

  ```go Go
  // The Go SDK does not yet support Foundry natively. This example uses the
  // standard Go SDK as a workaround, with a static Entra ID token: automatic
  // token refresh is not built in, so your application must refresh tokens
  // itself (they typically expire after 1 hour). WithoutEnvironmentDefaults
  // keeps the client from also reading ANTHROPIC_API_KEY or
  // ANTHROPIC_AUTH_TOKEN from the environment and sending a Claude API
  // credential to your Foundry endpoint. For full Foundry support, use the
  // C#, Java, PHP, Python, or TypeScript SDKs.
  package main

  import (
  	"context"
  	"fmt"
  	"os"

  	"github.com/anthropics/anthropic-sdk-go"
  	"github.com/anthropics/anthropic-sdk-go/option"
  )

  func main() {
  	// Obtain an Entra ID access token, for example using the Azure CLI:
  	//   az account get-access-token --resource https://ai.azure.com \
  	//     --query accessToken -o tsv
  	client := anthropic.NewClient(
  		option.WithoutEnvironmentDefaults(),
  		option.WithBaseURL("https://example-resource.services.ai.azure.com/anthropic"),
  		option.WithAuthToken(os.Getenv("AZURE_ACCESS_TOKEN")),
  	)

  	message, err := client.Messages.New(context.Background(), anthropic.MessageNewParams{
  		Model:     "claude-opus-4-8",
  		MaxTokens: 1024,
  		Messages: []anthropic.MessageParam{
  			anthropic.NewUserMessage(anthropic.NewTextBlock("Hello!")),
  		},
  	})
  	if err != nil {
  		panic(err)
  	}
  	fmt.Println(message.Content)
  }
  ```

  ```java Java
  import com.anthropic.client.AnthropicClient;
  import com.anthropic.client.okhttp.AnthropicOkHttpClient;
  import com.anthropic.foundry.backends.FoundryBackend;
  import com.anthropic.models.messages.MessageCreateParams;
  import com.azure.identity.AuthenticationUtil;
  import com.azure.identity.DefaultAzureCredentialBuilder;
  import java.util.function.Supplier;

  void main() {
      Supplier<String> bearerTokenSupplier = AuthenticationUtil.getBearerTokenSupplier(
          new DefaultAzureCredentialBuilder().build(),
          "https://ai.azure.com/.default"
      );

      AnthropicClient client = AnthropicOkHttpClient.builder()
          .backend(FoundryBackend.builder()
              .bearerTokenSupplier(bearerTokenSupplier)
              .resource("example-resource")
              .build())
          .build();

      MessageCreateParams params = MessageCreateParams.builder()
          .model("claude-opus-4-8")
          .maxTokens(1024)
          .addUserMessage("Hello!")
          .build();

      client.messages().create(params).content().stream()
          .flatMap(block -> block.text().stream())
          .forEach(textBlock -> System.out.println(textBlock.text()));
  }
  ```

  ```php PHP
  <?php

  use Anthropic\Foundry;

  // Obtain an Entra ID access token, for example using the Azure CLI:
  //   az account get-access-token --resource https://ai.azure.com \
  //     --query accessToken -o tsv
  $token = getenv('AZURE_ACCESS_TOKEN');

  $client = Foundry\Client::withCredentials(
      authToken: $token,
      baseUrl: 'https://example-resource.services.ai.azure.com/anthropic',
  );

  $message = $client->messages->create(
      maxTokens: 1024,
      messages: [
          ['role' => 'user', 'content' => 'Hello!']
      ],
      model: 'claude-opus-4-8',
  );
  echo $message->content[0]->text;
  ```

  ```ruby Ruby
  # The Ruby SDK does not yet support Foundry natively. This example uses the
  # standard Ruby SDK as a workaround, with a static Entra ID token: automatic
  # token refresh is not built in, so your application must refresh tokens
  # itself (they typically expire after 1 hour). Pass credentials explicitly:
  # without them, the client falls back to the ANTHROPIC_API_KEY or
  # ANTHROPIC_AUTH_TOKEN environment variables. For full Foundry support, use
  # the C#, Java, PHP, Python, or TypeScript SDKs.
  require "anthropic"

  # Obtain an Entra ID access token, for example using the Azure CLI:
  #   az account get-access-token --resource https://ai.azure.com \
  #     --query accessToken -o tsv
  client = Anthropic::Client.new(
    base_url: "https://example-resource.services.ai.azure.com/anthropic",
    auth_token: ENV.fetch("AZURE_ACCESS_TOKEN")
  )

  message = client.messages.create(
    model: "claude-opus-4-8",
    max_tokens: 1024,
    messages: [{role: "user", content: "Hello!"}]
  )

  puts message.content.first.text
  ```
</CodeGroup>

## Correlation request IDs

Foundry includes request identifiers in HTTP response headers for debugging and tracing. When contacting support, provide both the `request-id` and `apim-request-id` (Azure API Management) values to help teams quickly locate and investigate your request across both Anthropic and Azure systems.

## Feature support

Claude in Microsoft Foundry supports most Claude features. You can find all the features currently supported in [Features overview](/docs/en/build-with-claude/overview).

### Context window

Claude Fable 5, Claude Opus 4.8, Claude Opus 4.7, Claude Opus 4.6, Claude Sonnet 5, and Claude Sonnet 4.6 have a [1M-token context window](/docs/en/build-with-claude/context-windows) on Microsoft Foundry. Other Claude models, including Claude Sonnet 4.5, have a 200k-token context window.

### Claude features not supported for Claude in Microsoft Foundry

* Admin API
* Advisor tool
* Claude Managed Agents
* Compliance API
* Models API
* Message Batches API
* Server-side fallback (the [`fallbacks` parameter](/docs/en/build-with-claude/refusals-and-fallback#server-side-fallback); use the [client-side fallback pattern](/docs/en/build-with-claude/refusals-and-fallback#client-side-fallback) instead)

### Additional features not supported when hosted on Azure

The following features are available for deployments hosted on Anthropic but are not supported for deployments hosted on Azure:

* Structured outputs
* Server-side tools (web search, web fetch, code execution, and tool search)
* MCP connector
* Agent Skills
* Programmatic tool calling
* Files API

Requests that use these features against a deployment hosted on Azure return a `400 Bad Request` error by design. Claude Code detects deployments hosted on Azure and automatically adapts its feature set.

## API responses

API responses from Claude in Microsoft Foundry follow the standard [Claude API response format](/docs/en/api/messages/create). This includes the `usage` object in response bodies, which provides detailed token consumption information for your requests. The `usage` object is consistent across all platforms (Claude API, Foundry, Claude Platform on AWS, Amazon Bedrock, and Google Cloud).

For details on response headers specific to Foundry, see [Correlation request IDs](#correlation-request-ids).

## API model IDs and deployments

Lifecycle terms (Deprecated, Retired) are defined in [Model deprecations](/docs/en/about-claude/model-deprecations). Microsoft Foundry follows the Claude API lifecycle schedule.

The following Claude models are available through Foundry:

| Model                                                | Default deployment name | Hosted on Azure | Hosted on Anthropic |
| ---------------------------------------------------- | ----------------------- | --------------- | ------------------- |
| Claude Fable 5                                       | claude-fable-5          |                 | ✓                   |
| Claude Opus 4.8                                      | claude-opus-4-8         | ✓               | ✓                   |
| Claude Opus 4.7                                      | claude-opus-4-7         |                 | ✓                   |
| Claude Opus 4.6                                      | claude-opus-4-6         |                 | ✓                   |
| Claude Opus 4.5                                      | claude-opus-4-5         |                 | ✓                   |
| Claude Opus 4.1 Deprecated. Retiring August 5, 2026. | claude-opus-4-1         |                 | ✓                   |
| Claude Sonnet 5                                      | claude-sonnet-5         | ✓               | ✓                   |
| Claude Sonnet 4.6                                    | claude-sonnet-4-6       |                 | ✓                   |
| Claude Sonnet 4.5                                    | claude-sonnet-4-5       |                 | ✓                   |
| Claude Haiku 4.5                                     | claude-haiku-4-5        | ✓               | ✓                   |

By default, deployment names match the model IDs shown in the preceding table. However, you can create custom deployments with different names in the Foundry portal to manage different configurations, versions, or rate limits. Use the deployment name (not necessarily the model ID) in your API requests.

<Info>
  [Claude Mythos Preview](https://anthropic.com/glasswing) is a research preview available to invited customers on Microsoft Foundry.
</Info>

<Tip>
  Upgrading to a newer Claude model? In Claude Code, run `/claude-api migrate` to apply model ID swaps and breaking parameter changes across your codebase. The skill detects which cloud platform your code targets and adjusts model ID formats and feature changes for that platform. See [Migrating to a newer Claude model](/docs/en/agents-and-tools/agent-skills/claude-api-skill#migrating-to-a-newer-claude-model).
</Tip>

## Billing

Claude in Microsoft Foundry bills through the [Azure Marketplace](https://azuremarketplace.microsoft.com/). Usage is denominated in Claude Consumption Units (CCUs), metered hourly, and invoiced monthly in arrears on your Azure bill. CCUs are not prepaid credits. There is no CCU balance or commitment.

For the CCU price, conversion mechanics, and per-model token rates, see [Claude in Microsoft Foundry pricing](/docs/en/about-claude/pricing#claude-in-microsoft-foundry-pricing).

## Migrating between hosting options

To move an existing deployment from one hosting option to the other:

1. Create a new deployment of the model's other hosting version (Hosted on Azure or Hosted on Anthropic). This can be in the same Foundry resource, or a new one.
2. Update your application to pass the new deployment name in the `model` parameter.
3. Delete the old deployment once traffic has moved.

If the new deployment is in the same Foundry resource, your endpoint URL and authentication are unchanged. If you created a new resource, update your application's endpoint and credentials to point to it.

## Monitoring and logging

Azure provides monitoring and logging for your Claude usage through standard Azure patterns:

* **Azure Monitor:** Track API usage, latency, and error rates
* **Azure Log Analytics:** Query and analyze request/response logs
* **Cost Management:** Monitor and forecast costs associated with Claude usage

Anthropic recommends logging your activity on at least a 30-day rolling basis to understand usage patterns and investigate any potential issues.

<Note>
  Azure's logging services are configured within your Azure subscription. Enabling logging does not provide Microsoft or Anthropic access to your content beyond what's necessary for billing and service operation.
</Note>

## Troubleshooting

### Authentication errors

**Error:** `401 Unauthorized` or `Invalid API key`

* **Solution:** Verify your API key is correct. You can find it in the Foundry portal on your deployment's **Details** tab (under **Build** > **Models**).
* **Solution:** If using Microsoft Entra ID, ensure your access token is valid and hasn't expired. Tokens typically expire after 1 hour.

**Error:** `403 Forbidden`

* **Solution:** Your Azure account may lack the necessary permissions. Ensure you have the appropriate Azure RBAC role assigned (for example, **Foundry User** (formerly Azure AI User) or **Cognitive Services User**).

### Rate limiting

**Error:** `429 Too Many Requests`

* **Solution:** You've exceeded your rate limit. Implement exponential backoff and retry logic in your application.
* **Solution:** Consider requesting rate limit increases through the Azure portal or Azure support.

#### Rate limit headers

Foundry does not include Anthropic's standard rate limit headers (`anthropic-ratelimit-tokens-limit`, `anthropic-ratelimit-tokens-remaining`, `anthropic-ratelimit-tokens-reset`, `anthropic-ratelimit-input-tokens-limit`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-input-tokens-reset`, `anthropic-ratelimit-output-tokens-limit`, `anthropic-ratelimit-output-tokens-remaining`, and `anthropic-ratelimit-output-tokens-reset`) in responses. Manage rate limiting through Azure's monitoring tools instead.

### Model and deployment errors

**Error:** `Model not found` or `Deployment not found`

* **Solution:** Verify you're using the correct deployment name. If you haven't created a custom deployment, use the default model ID (for example, claude-opus-4-8).
* **Solution:** Ensure the model/deployment is available in your Azure region.

**Error:** `Invalid model parameter`

* **Solution:** The model parameter should contain your deployment name, which can be customized in the Foundry portal. Verify the deployment exists and is properly configured.

## Next steps

<CardGroup cols={2}>
  <Card title="Features overview" icon="stack" href="/docs/en/build-with-claude/overview">
    Explore Claude's advanced features and capabilities.
  </Card>

  <Card title="Pricing" icon="chart" href="/docs/en/about-claude/pricing#claude-in-microsoft-foundry-pricing">
    Learn about Anthropic's pricing structure for models and features.
  </Card>

  <Card title="Model deprecations" icon="arrow-clockwise" href="/docs/en/about-claude/model-deprecations">
    As safer and more capable models launch, Anthropic regularly retires older ones. See all API deprecations, along with recommended replacements.
  </Card>
</CardGroup>

## Additional resources

<CardGroup cols={2}>
  <Card title="Foundry model catalog" icon="grid" href="https://ai.azure.com/catalog/publishers/anthropic">
    Browse Anthropic models in the Foundry catalog.
  </Card>

  <Card title="Azure AI Foundry pricing" icon="calculator" href="https://azure.microsoft.com/en-us/pricing/details/ai-foundry/#pricing">
    View Microsoft's pricing details for Azure AI Foundry.
  </Card>

  <Card title="Model pricing" icon="table" href="/docs/en/about-claude/pricing#model-pricing">
    View Anthropic's per-model pricing details.
  </Card>

  <Card title="Azure portal" icon="cloud" href="https://portal.azure.com/">
    Manage your Azure resources.
  </Card>
</CardGroup>
