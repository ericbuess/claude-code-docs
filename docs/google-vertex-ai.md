> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on Google Cloud's Agent Platform

> Learn about configuring Claude Code through Google Cloud's Agent Platform, formerly Vertex AI, including setup, IAM configuration, and troubleshooting.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

<ContactSalesCard surface="vertex" />

## Prerequisites

Before configuring Claude Code with Google Cloud's Agent Platform, formerly Vertex AI, ensure you have:

* A Google Cloud Platform (GCP) account with billing enabled
* A GCP project with Google Cloud's Agent Platform API enabled
* Access to desired Claude models (for example, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installed and configured
* Quota allocated in desired GCP region

To sign in with your own Google Cloud's Agent Platform credentials, follow [Sign in with Google Cloud's Agent Platform](#sign-in-with-agent-platform) below. To deploy Claude Code across a team, use the [manual setup](#set-up-manually) steps and [pin your model versions](#5-pin-model-versions) before rolling out.

## Sign in with Agent Platform

If you have Google Cloud credentials and want to start using Claude Code through Google Cloud's Agent Platform, the login wizard walks you through it. You complete the GCP-side prerequisites once per project; the wizard handles the Claude Code side.

<Note>
  The Google Cloud's Agent Platform setup wizard requires Claude Code v2.1.98 or later. Run `claude --version` to check.
</Note>

<Steps>
  <Step title="Enable Claude models in your GCP project">
    [Enable Google Cloud's Agent Platform API](#1-enable-agent-platform-api) for your project, then request access to the Claude models you want in the [Google Cloud's Agent Platform Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). See [IAM configuration](#iam-configuration) for the permissions your account needs.
  </Step>

  <Step title="Start Claude Code and choose Google Cloud's Agent Platform">
    Run `claude`. At the login prompt, select **3rd-party platform**, then **Google Vertex AI**, the label the login prompt still uses for Google Cloud's Agent Platform.
  </Step>

  <Step title="Follow the wizard prompts">
    Choose how you authenticate to Google Cloud: Application Default Credentials from `gcloud`, a service account key file, or credentials already in your environment. The wizard detects your project and region, verifies which Claude models your project can invoke, and lets you pin them. It saves the result to the `env` block of your [user settings file](/en/settings), so you don't need to export environment variables yourself.
  </Step>
</Steps>

After you've signed in, run `/setup-vertex` any time to reopen the wizard and change your credentials, project, region, or model pins.

## Region configuration

Claude Code supports Google Cloud's Agent Platform [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multi-region, and regional endpoints. Set `CLOUD_ML_REGION` to `global`, a multi-region location such as `eu` or `us`, or a specific region such as `us-east5`. Claude Code selects the correct Google Cloud's Agent Platform hostname for each form, including the `aiplatform.eu.rep.googleapis.com` and `aiplatform.us.rep.googleapis.com` hosts for multi-region locations.

<Note>
  Google Cloud's Agent Platform may not support the Claude Code default models on every endpoint type. Model availability varies across [specific regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), multi-region locations, and [global endpoints](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). You may need to switch to a supported location or specify a supported model.
</Note>

## Set up manually

To configure Google Cloud's Agent Platform through environment variables instead of the wizard, for example in CI or a scripted enterprise rollout, follow the steps below.

### 1. Enable Agent Platform API

Enable Google Cloud's Agent Platform API in your GCP project:

```bash theme={null}
# Set your project ID
gcloud config set project YOUR-PROJECT-ID

# Enable Agent Platform API
gcloud services enable aiplatform.googleapis.com
```

### 2. Request model access

Request access to Claude models in Google Cloud's Agent Platform:

1. Navigate to the [Google Cloud's Agent Platform Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Search for "Claude" models
3. Request access to desired Claude models (for example, Claude Sonnet 4.6)
4. Wait for approval (may take 24-48 hours)

### 3. Configure GCP credentials

Claude Code uses standard Google Cloud authentication.

For more information, see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).

Claude Code v2.1.121 or later supports [X.509 certificate-based Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) through the same Application Default Credentials chain. Set `GOOGLE_APPLICATION_CREDENTIALS` to the path of your credential configuration file.

<Note>
  Claude Code uses `ANTHROPIC_VERTEX_PROJECT_ID` as the project ID for Google Cloud's Agent Platform requests. The `GCLOUD_PROJECT` and `GOOGLE_CLOUD_PROJECT` environment variables and the credential file referenced by `GOOGLE_APPLICATION_CREDENTIALS` take precedence over it. If none of these are set, the project ID is resolved from your `gcloud` configuration or the attached service account.
</Note>

#### Advanced credential configuration

Claude Code supports automatic credential refresh for GCP through the `gcpAuthRefresh` setting. When Claude Code detects that your GCP credentials are expired or cannot be loaded, it runs the configured command to obtain new credentials before retrying the request.

```json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

The command's output is displayed to the user, but interactive input isn't supported. This works well for browser-based authentication flows where the CLI shows a URL and you complete authentication in the browser. The refresh command times out after three minutes if authentication does not complete. If you set `gcpAuthRefresh` in project settings such as `.claude/settings.json`, the command runs only after you accept the workspace trust prompt.

### 4. Configure Claude Code

Set the following environment variables:

```bash theme={null}
# Enable Agent Platform integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Override the Agent Platform endpoint URL for custom endpoints or gateways
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Request 1-hour prompt cache TTL instead of the 5-minute default
export ENABLE_PROMPT_CACHING_1H=1

# When CLOUD_ML_REGION=global, override region for models that don't support global endpoints
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Most model versions have a corresponding `VERTEX_REGION_CLAUDE_*` variable. See the [Environment variables reference](/en/env-vars) for the full list. Check [Google Cloud's Agent Platform Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) to determine which models support global endpoints versus regional only.

[Prompt caching](/en/prompt-caching) is enabled automatically. To disable it, set `DISABLE_PROMPT_CACHING=1`. To request a 1-hour cache TTL instead of the 5-minute default, set `ENABLE_PROMPT_CACHING_1H=1`; cache writes with a 1-hour TTL are billed at a higher rate. For heightened rate limits, contact Google Cloud support. When using Google Cloud's Agent Platform, the `/logout` command is unavailable since authentication is handled through Google Cloud credentials.

Claude Code disables [MCP tool search](/en/mcp#scale-with-mcp-tool-search) by default on Google Cloud's Agent Platform, so MCP tool definitions load upfront. Google Cloud's Agent Platform supports tool search for Claude Sonnet 4.5 and later and Claude Opus 4.5 and later. Set `ENABLE_TOOL_SEARCH=true` to enable it on those models. Earlier models on Google Cloud's Agent Platform do not accept the required beta header, and requests fail if you enable tool search with them.

### 5. Pin model versions

<Warning>
  Pin specific model versions when deploying to multiple users. Without pinning, model aliases such as `sonnet` and `opus` resolve to Claude Code's built-in default for Google Cloud's Agent Platform, which can lag the newest release and may not yet be enabled in your project. Claude Code [falls back](#startup-model-checks) to the previous version at startup when the default is unavailable, but pinning lets you control when your users move to a new model.
</Warning>

Set these environment variables to specific Google Cloud's Agent Platform model IDs.

Without these variables, the `opus` alias on Google Cloud's Agent Platform resolves to Opus 4.8 and the `sonnet` alias resolves to Sonnet 4.5. Set each variable to pin its alias to a specific version:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

For current and legacy model IDs, see [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). See [Model configuration](/en/model-config#pin-models-for-third-party-deployments) for the full list of environment variables.

Claude Code uses these default models when no pinning variables are set:

| Model type       | Default value         |
| :--------------- | :-------------------- |
| Primary model    | `claude-opus-4-8`     |
| Small/fast model | Same as primary model |

Background tasks such as session title generation use the small/fast model, normally a Haiku-class model. On Google Cloud's Agent Platform, Claude Code defaults this to the primary model because Haiku may not be enabled in every project or region. To use Haiku for background tasks, set `ANTHROPIC_DEFAULT_HAIKU_MODEL` to a model ID that is available in your project.

To customize models further:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-8'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Startup model checks

When Claude Code starts with Google Cloud's Agent Platform configured, it verifies that the models it intends to use are accessible in your project. This check requires Claude Code v2.1.98 or later.

If you have pinned a model version that is older than the current Claude Code default, and your project can invoke the newer version, Claude Code prompts you to update the pin. Accepting writes the new model ID to your [user settings file](/en/settings) and restarts Claude Code. Declining is remembered until the next default version change.

If you have not pinned a model and the current default is unavailable in your project, Claude Code falls back to the previous version for the current session and shows a notice. The fallback is not persisted. Enable the newer model in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) or [pin a version](#5-pin-model-versions) to make the choice permanent.

## IAM configuration

Assign the required IAM permissions:

The `roles/aiplatform.user` role includes the required permissions:

* `aiplatform.endpoints.predict` - Required for model invocation and token counting

For more restrictive permissions, create a custom role with only the permissions above.

For details, see [Google Cloud's Agent Platform IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Create a dedicated GCP project for Claude Code to simplify cost tracking and access control.
</Note>

## 1M token context window

Claude Sonnet 5, Opus 4.6 and later, and Sonnet 4.6 support the [1M token context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) on Google Cloud's Agent Platform. Sonnet 5 always runs with the 1M window, with no `[1m]` variant to select. For the other models, Claude Code automatically enables the extended context window when you select a 1M model variant.

The [setup wizard](#sign-in-with-agent-platform) offers a 1M context option when it pins models. To enable it for a manually pinned model instead, append `[1m]` to the model ID. See [Pin models for third-party deployments](/en/model-config#pin-models-for-third-party-deployments) for details.

## Troubleshooting

If you encounter "Could not load the default credentials" errors:

* Run `gcloud auth application-default login` to set up Application Default Credentials
* Set `GOOGLE_APPLICATION_CREDENTIALS` to a service account key file path
* See [Configure GCP credentials](#3-configure-gcp-credentials) for all options

If you encounter quota issues:

* Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter "model not found" 404 errors:

* Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verify the model is available in the location you specified. Some models are offered only on `global` or multi-region locations such as `eu` and `us`, not in specific regions
* If using `CLOUD_ML_REGION=global`, check that your models support global endpoints in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) under "Supported features". For models that don't support global endpoints, either:
  * Specify a supported model via `ANTHROPIC_MODEL` or `ANTHROPIC_DEFAULT_HAIKU_MODEL`, or
  * Set a region or multi-region location using `VERTEX_REGION_<MODEL_NAME>` environment variables

If you encounter 429 errors:

* For regional endpoints, ensure the primary model and small/fast model are supported in your selected region
* Consider switching to `CLOUD_ML_REGION=global` for better availability

## Additional resources

* [Google Cloud's Agent Platform documentation](https://cloud.google.com/vertex-ai/docs)
* [Google Cloud's Agent Platform pricing](https://cloud.google.com/vertex-ai/pricing)
* [Google Cloud's Agent Platform quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)
