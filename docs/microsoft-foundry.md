> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on Microsoft Foundry

> Learn about configuring Claude Code through Microsoft Foundry, including setup, configuration, and troubleshooting.

**Deploying Claude Code across your organization?** Talk to sales about enterprise plans, SSO, and centralized billing.

View plans
Contact sales

## Prerequisites

Before configuring Claude Code with Microsoft Foundry, ensure you have:

* An Azure subscription with access to Microsoft Foundry
* RBAC permissions to create Microsoft Foundry resources and deployments
* Azure CLI installed and configured (optional - only needed if you don't have another mechanism for getting credentials)

> [!NOTE]
>
> If you are deploying Claude Code to multiple users, [pin your model versions](#4-pin-model-versions) before rolling out.

## Setup

### 1. Provision Microsoft Foundry resource

First, create a Claude resource in Azure:

1. Go to the [Microsoft Foundry portal](https://ai.azure.com/)
2. Create a new resource, noting your resource name
3. Create deployments for the Claude models, noting the deployment name you give each; you'll set these names as the model variables in step 4:

   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

   When you configure a deployment, you also choose its [hosting option](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options), which determines whether inference runs on Azure or on Anthropic infrastructure.

### 2. Configure Azure credentials

Claude Code supports three authentication methods for Microsoft Foundry. Choose the method that best fits your security requirements:

* [API key](#use-an-api-key): you copy a key from the Microsoft Foundry portal and set it as `ANTHROPIC_FOUNDRY_API_KEY`
* [Microsoft Entra ID](#use-microsoft-entra-id): Claude Code gets tokens through the Azure SDK default credential chain, for example from an `az login` session, so there's no API key to store
* [Bearer token](#use-a-bearer-token): another process obtains a Microsoft Entra ID access token and you pass it in `ANTHROPIC_FOUNDRY_AUTH_TOKEN`

> [!NOTE]
>
> When using Microsoft Foundry, the `/logout` command is unavailable since authentication is handled through Azure credentials.

#### Use an API key

Copy a key from the Microsoft Foundry portal, then set it as an environment variable:

1. Go to your resource in the Microsoft Foundry portal
2. Open the **Endpoints and keys** section
3. Copy **API Key**
4. Set the environment variable, replacing `your-azure-api-key` with the key you copied:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

#### Use Microsoft Entra ID

Leave `ANTHROPIC_FOUNDRY_API_KEY` and `ANTHROPIC_FOUNDRY_AUTH_TOKEN` unset. Claude Code then uses the Azure SDK [default credential chain](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
This supports a variety of methods for authenticating local and remote workloads.

On a local machine, sign in with the Azure CLI:

```bash theme={null}
az login
```

For the roles your identity needs, see [Azure RBAC configuration](#azure-rbac-configuration).

#### Use a bearer token

Claude Code sends the value of `ANTHROPIC_FOUNDRY_AUTH_TOKEN` on every request as the `Authorization: Bearer` header. Use this option when another process, such as a host application or a sign-in script, has already obtained an access token for you.

Set the variable to a bearer token that Microsoft Entra ID issued for your resource:

```bash theme={null}
export ANTHROPIC_FOUNDRY_AUTH_TOKEN=your-entra-access-token
```

`ANTHROPIC_FOUNDRY_AUTH_TOKEN` takes precedence over `ANTHROPIC_FOUNDRY_API_KEY` and over the default credential chain.

### 3. Configure Claude Code

Set the following environment variables to enable Microsoft Foundry:

```bash theme={null}
# Enable Microsoft Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

Set `ANTHROPIC_FOUNDRY_RESOURCE` to the resource name alone, such as `my-resource`. Claude Code [refuses a URL or host name](https://code.claude.com/docs/en/errors.md#anthropic-foundry-resource-must-be-a-foundry-resource-name) when you send a message.

### 4. Pin model versions

> [!WARNING]
>
> Pin specific model versions for every deployment. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code's built-in default for Microsoft Foundry, which can lag the newest release and may not yet be available in your account. Microsoft Foundry has no startup model check, so requests fail when the default is unavailable. When you create Azure deployments, select a specific model version rather than "auto-update to latest."

Set the model variables to match the deployment names you created in step 1.

Without `ANTHROPIC_DEFAULT_OPUS_MODEL`, the `opus` alias on Microsoft Foundry resolves to Opus 4.6. Set it to the ID of a newer Opus model, such as Opus 4.8:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Microsoft Foundry, Claude Code defaults this to the primary model because not every account has a Haiku deployment. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a Haiku deployment that is available in your account, as shown above.

For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](https://code.claude.com/docs/en/model-config.md#pin-models-for-third-party-deployments) for the full list of environment variables.

[Prompt caching](https://code.claude.com/docs/en/prompt-caching.md) is enabled automatically. To request a 1-hour cache TTL instead of the 5-minute default, set the following variable; cache writes with a 1-hour TTL are billed at a higher rate:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

To set different TTLs for your main conversation and for the requests Claude Code makes outside it, [choose the TTL yourself](https://code.claude.com/docs/en/prompt-caching.md#choose-the-ttl-yourself).

### 5. Run Claude Code

With the environment variables set, start Claude Code from your project directory:

```bash theme={null}
claude
```

Claude Code reads `CLAUDE_CODE_USE_FOUNDRY` and the other Microsoft Foundry variables from the environment and connects to your Azure resource on the first prompt. Unlike Amazon Bedrock and Google Cloud's Agent Platform, Microsoft Foundry has no interactive setup wizard, so the environment variables in steps 3 and 4 are the only configuration path.

To verify your setup, run `/status` inside Claude Code. The API provider line shows `Microsoft Foundry`, along with the resource name or base URL you configured.

## Azure RBAC configuration

The `Azure AI User` and `Cognitive Services User` default roles include all required permissions for invoking Claude models.

For more restrictive permissions, create a custom role with the following:

```json theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

For details, see [Microsoft Foundry RBAC documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## 1M token context window

On Microsoft Foundry, when Claude Code can tell which model your deployment serves, Fable models, Sonnet 5 and later, and Opus 4.7 and later run with the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#context-window-sizes-by-model) by default, with no `[1m]` suffix needed. Claude Code reads the model from the deployment name in your model variables. Name each deployment with its model ID, such as `claude-opus-4-8`, or map the model to your deployment name with [`modelOverrides`](https://code.claude.com/docs/en/model-config#override-model-ids-per-version). For a deployment name it can't match to a model, Claude Code assumes a 200K window unless you [declare a different one](https://code.claude.com/docs/en/model-config.md#correct-the-window-for-a-gateway-or-custom-model-id).

This `settings.json` entry tells Claude Code that a deployment named `team-opus-prod` serves Opus 4.8:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-8": "team-opus-prod"
  }
}
```

To keep a 200K window instead, set [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](https://code.claude.com/docs/en/model-config#turn-off-1m-context).

Opus 4.6 and Sonnet 4.6 reach the 1M window when you append `[1m]` to the deployment name in `ANTHROPIC_DEFAULT_OPUS_MODEL` or `ANTHROPIC_DEFAULT_SONNET_MODEL`, as [Pin models for third-party deployments](https://code.claude.com/docs/en/model-config.md#pin-models-for-third-party-deployments) describes. Before v2.1.287, the Fable models and Opus 4.7 and later also needed that suffix on Microsoft Foundry and ran with a 200K window by default without it.

## Troubleshooting

If you receive an error "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Configure Entra ID on the environment, or set `ANTHROPIC_FOUNDRY_API_KEY`.

If requests fail with repeated connection errors on the first prompt:

* Check that `ANTHROPIC_FOUNDRY_RESOURCE` is set to your actual resource name rather than a placeholder. Claude Code builds the endpoint URL from this value, so an incorrect name points at a host that doesn't exist.

## Additional resources

* [Microsoft Foundry documentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Microsoft Foundry models](https://ai.azure.com/explore/models)
* [Microsoft Foundry pricing](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
