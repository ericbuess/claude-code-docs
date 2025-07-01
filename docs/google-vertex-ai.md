# Claude Code on Google Vertex AI

> Learn about configuring Claude Code through Google Vertex AI, including setup, IAM configuration, and troubleshooting.

## Prerequisites

Before configuring Claude Code with Vertex AI, ensure you have:

* A Google Cloud Platform (GCP) account with billing enabled
* A GCP project with Vertex AI API enabled
* Access to desired Claude models (e.g., Claude Sonnet 4)
* Google Cloud SDK (`gcloud`) installed and configured
* Quota allocated in desired GCP region

<Warning>
  Vertex AI may not support the Claude Code default models on non-`us-east5` regions. Ensure you are using `us-east5` and have quota allocated, or switch to supported models.
</Warning>

## Setup

### 1. Enable Vertex AI API

Enable the Vertex AI API in your GCP project:

```bash
# Set your project ID
gcloud config set project YOUR-PROJECT-ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Request model access

Request access to Claude models in Vertex AI:

1. Navigate to the [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Search for "Claude" models
3. Request access to desired Claude models (e.g., Claude Sonnet 4)
4. Wait for approval (may take 24-48 hours)

### 3. Configure GCP credentials

Claude Code uses standard Google Cloud authentication.

For more information, see [Google Cloud authentication documentation](https://cloud.google.com/docs/authentication).

### 4. Configure Claude Code

Set the following environment variables:

```bash
# Enable Vertex AI integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1
```

<Note>
  [Prompt caching](/en/docs/build-with-claude/prompt-caching) is automatically supported when you specify the `cache_control` ephemeral flag. To disable it, set `DISABLE_PROMPT_CACHING=1`. For heightened rate limits, contact Google Cloud support.
</Note>

### 5. Model configuration

Claude Code uses these default models for Vertex AI:

| Model type       | Default value               |
| :--------------- | :-------------------------- |
| Primary model    | `claude-sonnet-4@20250514`  |
| Small/fast model | `claude-3-5-haiku@20241022` |

To customize models:

```bash
export ANTHROPIC_MODEL='claude-opus-4@20250514'
export ANTHROPIC_SMALL_FAST_MODEL='claude-3-5-haiku@20241022'
```

## IAM configuration

Grant the required IAM roles for Claude Code.

For details, see [Vertex IAM documentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  We recommend creating a dedicated GCP project for Claude Code to simplify cost tracking and access control.
</Note>

## Troubleshooting

If you encounter quota issues:

* Check current quotas or request quota increase through [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

If you encounter "model not found" 404 errors:

* Verify you have access to the specified region
* Confirm model is Enabled in [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)

If you encounter 429 errors:

* Ensure the primary model and small/fast model are supported in your selected region

## Additional resources

* [Vertex AI documentation](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI pricing](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI quotas and limits](https://cloud.google.com/vertex-ai/docs/quotas)
