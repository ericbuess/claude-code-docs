# Claude in Microsoft Foundry

Access Claude models through Microsoft Foundry with Azure-native endpoints and authentication.

---

This guide will walk you through the process of setting up and making API calls to Claude in Foundry in Python, TypeScript, or using direct HTTP requests. When you can access Claude in Foundry, you will be billed for Claude usage in the Microsoft Marketplace with your Azure subscription, allowing you to access Claude's latest capabilities while managing costs through your Azure subscription.

Regional availability: At launch, Claude is available as a Global Standard deployment type in Foundry resources with US DataZone coming soon. Pricing for Claude in the Microsoft Marketplace uses Anthropic's standard API pricing. Visit our [pricing page](https://claude.com/pricing#api) for details.

## Preview

In this preview platform integration, Claude models run on Anthropic's infrastructure. This is a commercial integration for billing and access through Azure. As an independent processor for Microsoft, customers using Claude through Microsoft Foundry are subject to Anthropic's data use terms. Anthropic continues to provide its industry-leading safety and data commitments, including zero data retention availability.

## Prerequisites

Before you begin, ensure you have:

- An active Azure subscription
- Access to [Foundry](https://ai.azure.com/)
- The [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli) installed (optional, for resource management)

## Install an SDK

Anthropic's [client SDKs](/docs/en/api/client-sdks) support Foundry through platform-specific packages.

```bash
# Python
pip install -U "anthropic"

# Typescript
npm install @anthropic-ai/foundry-sdk
```

## Provisioning

Foundry uses a two-level hierarchy: **resources** contain your security and billing configuration, while **deployments** are the model instances you call via API. You'll first create a Foundry resource, then create one or more Claude deployments within it.

### Provisioning Foundry resources

Create a Foundry resource, which is required to use and manage services in Azure. You can follow these instructions to create a [Foundry resource](https://learn.microsoft.com/en-us/azure/ai-services/multi-service-resource?pivots=azportal#create-a-new-azure-ai-foundry-resource). Alternatively, you can start by creating a [Foundry project](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/create-projects?tabs=ai-foundry), which involves creating a Foundry resource.

To provision your resource:

1. Navigate to the [Foundry portal](https://ai.azure.com/)
2. Create a new Foundry resource or select an existing one
3. Configure access management using Azure-issued API keys or Entra ID for role-based access control
4. Optionally configure the resource to be part of a private network (Azure Virtual Network) for enhanced security
5. Note your resource name—you'll use this as `{resource}` in API endpoints (e.g., `https://{resource}.services.ai.azure.com/anthropic/v1/*`)

### Creating Foundry deployments

After creating your resource, deploy a Claude model to make it available for API calls:

1. In the Foundry portal, navigate to your resource
2. Go to **Models + endpoints** and select **+ Deploy model** > **Deploy base model**
3. Search for and select a Claude model (e.g., `claude-sonnet-4-5`)
4. Configure deployment settings:
   - **Deployment name**: Defaults to the model ID, but you can customize it (e.g., `my-claude-deployment`). The deployment name cannot be changed after it has been created.
   - **Deployment type**: Select Global Standard (recommended for Claude)
5. Select **Deploy** and wait for provisioning to complete
6. Once deployed, you can find your endpoint URL and keys under **Keys and Endpoint**

<Note>
  The deployment name you choose becomes the value you pass in the `model` parameter of your API requests. You can create multiple deployments of the same model with different names to manage separate configurations or rate limits.
</Note>

## Authentication

Claude on Foundry supports two authentication methods: API keys and Entra ID tokens. Both methods use Azure-hosted endpoints in the format `https://{resource}.services.ai.azure.com/anthropic/v1/*`.

### API key authentication

After provisioning your Foundry Claude resource, you can obtain an API key from the Foundry portal:

1. Navigate to your resource in the Foundry portal
2. Go to **Keys and Endpoint** section
3. Copy one of the provided API keys
4. Use either the `api-key` or `x-api-key` header in your requests, or provide it to the SDK

The Python and TypeScript SDKs require an API key and either a resource name or base URL. The SDKs will automatically read these from the following environment variables if they are defined:

- `ANTHROPIC_FOUNDRY_API_KEY` - Your API key
- `ANTHROPIC_FOUNDRY_RESOURCE` - Your resource name (e.g., `example-resource`)
- `ANTHROPIC_FOUNDRY_BASE_URL` - Alternative to resource name; the full base URL (e.g., `https://example-resource.services.ai.azure.com/anthropic/`)

<Note>
The `resource` and `base_url` parameters are mutually exclusive. Provide either the resource name (which the SDK uses to construct the URL as `https://{resource}.services.ai.azure.com/anthropic/`) or the full base URL directly.
</Note>

**Example using API key:**

<CodeGroup>
```python Python
import os
from anthropic import AnthropicFoundry

client = AnthropicFoundry(
    api_key=os.environ.get("ANTHROPIC_FOUNDRY_API_KEY"),
    resource='example-resource', # your resource name
)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content)
```

```typescript TypeScript
import AnthropicFoundry from "@anthropic-ai/foundry-sdk";

const client = new AnthropicFoundry({
  apiKey: process.env.ANTHROPIC_FOUNDRY_API_KEY,
  resource: 'example-resource', // your resource name
});

const message = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(message.content);
```

```bash Shell
curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
  -H "content-type: application/json" \
  -H "api-key: YOUR_AZURE_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```
</CodeGroup>

<Warning>
Keep your API keys secure. Never commit them to version control or share them publicly. Anyone with access to your API key can make requests to Claude through your Foundry resource.
</Warning>

## Microsoft Entra authentication

For enhanced security and centralized access management, you can use Entra ID (formerly Azure Active Directory) tokens:

1. Enable Entra authentication for your Foundry resource
2. Obtain an access token from Entra ID
3. Use the token in the `Authorization: Bearer {TOKEN}` header

**Example using Entra ID:**

<CodeGroup>
```python Python
import os
from anthropic import AnthropicFoundry
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# Get Azure Entra ID token using token provider pattern
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

# Create client with Entra ID authentication
client = AnthropicFoundry(
    resource='example-resource', # your resource name
    azure_ad_token_provider=token_provider  # Use token provider for Entra ID auth
)

# Make request
message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
print(message.content)
```

```typescript TypeScript
import AnthropicFoundry from "@anthropic-ai/foundry-sdk";
import {
  DefaultAzureCredential,
  getBearerTokenProvider,
} from "@azure/identity";

// Get Entra ID token using token provider pattern
const credential = new DefaultAzureCredential();
const tokenProvider = getBearerTokenProvider(
  credential,
  "https://cognitiveservices.azure.com/.default"
);

// Create client with Entra ID authentication
const client = new AnthropicFoundry({
  resource: 'example-resource', // your resource name
  azureADTokenProvider: tokenProvider, // Use token provider for Entra ID auth
});

// Make request
const message = await client.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(message.content);
```

```bash Shell
# Get Azure Entra ID token
ACCESS_TOKEN=$(az account get-access-token --resource https://cognitiveservices.azure.com --query accessToken -o tsv)

# Make request with token. Replace {resource} with your resource name
curl https://{resource}.services.ai.azure.com/anthropic/v1/messages \
  -H "content-type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```
</CodeGroup>

<Note>
Azure Entra ID authentication allows you to manage access using Azure RBAC, integrate with your organization's identity management, and avoid managing API keys manually.
</Note>

## Correlation request IDs

Foundry includes request identifiers in HTTP response headers for debugging and tracing. When contacting support, provide both the `request-id` and `apim-request-id` values to help teams quickly locate and investigate your request across both Anthropic and Azure systems.

## Supported features

Claude on Foundry supports most of Claude's powerful features. You can find all the features currently supported [here](/docs/en/build-with-claude/overview).

### Features not supported

- Admin API (`/v1/organizations/*` endpoints)
- Models API (`/v1/models`)
- Message Batch API (`/v1/messages/batches`)

## API responses

API responses from Claude on Foundry follow the standard [Anthropic API response format](/docs/en/api/messages). This includes the `usage` object in response bodies, which provides detailed token consumption information for your requests. The `usage` object is consistent across all platforms (first-party API, Foundry, Amazon Bedrock, and Google Vertex AI).

For details on response headers specific to Foundry, see the [correlation request IDs section](#correlation-request-ids).

## API model IDs and deployments

The following Claude models are available through Foundry. The latest generation models (Sonnet 4.5, Opus 4.1, and Haiku 4.5) offer the most advanced capabilities:

| Model             | Default Deployment Name     |
| :---------------- | :-------------------------- |
| Claude Opus 4.5   | `claude-opus-4-5`  |
| Claude Sonnet 4.5 | `claude-sonnet-4-5`         |
| Claude Opus 4.1   | `claude-opus-4-1`           |
| Claude Haiku 4.5  | `claude-haiku-4-5`          |

By default, deployment names match the model IDs shown above. However, you can create custom deployments with different names in the Foundry portal to manage different configurations, versions, or rate limits. Use the deployment name (not necessarily the model ID) in your API requests.

## Monitoring and logging

Azure provides comprehensive monitoring and logging capabilities for your Claude usage through standard Azure patterns:

- **Azure Monitor**: Track API usage, latency, and error rates
- **Azure Log Analytics**: Query and analyze request/response logs
- **Cost Management**: Monitor and forecast costs associated with Claude usage

Anthropic recommends logging your activity on at least a 30-day rolling basis to understand usage patterns and investigate any potential issues.

<Note>
Azure's logging services are configured within your Azure subscription. Enabling logging does not provide Microsoft or Anthropic access to your content beyond what's necessary for billing and service operation.
</Note>

## Troubleshooting

### Authentication errors

**Error**: `401 Unauthorized` or `Invalid API key`

- **Solution**: Verify your API key is correct. You can obtain a new API key from the Azure portal under **Keys and Endpoint** for your Claude resource.
- **Solution**: If using Azure Entra ID, ensure your access token is valid and hasn't expired. Tokens typically expire after 1 hour.

**Error**: `403 Forbidden`

- **Solution**: Your Azure account may lack the necessary permissions. Ensure you have the appropriate Azure RBAC role assigned (e.g., "Cognitive Services OpenAI User").

### Rate limiting

**Error**: `429 Too Many Requests`

- **Solution**: You've exceeded your rate limit. Implement exponential backoff and retry logic in your application.
- **Solution**: Consider requesting rate limit increases through the Azure portal or Azure support.

#### Rate limit headers

Foundry does not include Anthropic's standard rate limit headers (`anthropic-ratelimit-tokens-limit`, `anthropic-ratelimit-tokens-remaining`, `anthropic-ratelimit-tokens-reset`, `anthropic-ratelimit-input-tokens-limit`, `anthropic-ratelimit-input-tokens-remaining`, `anthropic-ratelimit-input-tokens-reset`, `anthropic-ratelimit-output-tokens-limit`, `anthropic-ratelimit-output-tokens-remaining`, and `anthropic-ratelimit-output-tokens-reset`) in responses. Manage rate limiting through Azure's monitoring tools instead.

### Model and deployment errors

**Error**: `Model not found` or `Deployment not found`

- **Solution**: Verify you're using the correct deployment name. If you haven't created a custom deployment, use the default model ID (e.g., `claude-sonnet-4-5`).
- **Solution**: Ensure the model/deployment is available in your Azure region.

**Error**: `Invalid model parameter`

- **Solution**: The model parameter should contain your deployment name, which can be customized in the Foundry portal. Verify the deployment exists and is properly configured.

## Additional resources

- **Foundry documentation**: [ai.azure.com/catalog](https://ai.azure.com/catalog/publishers/anthropic)
- **Azure pricing**: [azure.microsoft.com/en-us/pricing](https://azure.microsoft.com/en-us/pricing/)
- **Anthropic pricing details**: [Pricing documentation](/docs/en/about-claude/pricing#third-party-platform-pricing)
- **Authentication guide**: See the [authentication section](#authentication) above
- **Azure portal**: [portal.azure.com](https://portal.azure.com/)