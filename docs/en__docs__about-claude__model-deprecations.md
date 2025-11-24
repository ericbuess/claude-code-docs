# Model deprecations

---

As we launch safer and more capable models, we regularly retire older models. Applications relying on Anthropic models may need occasional updates to keep working. Impacted customers will always be notified by email and in our documentation.

This page lists all API deprecations, along with recommended replacements.

## Overview

Anthropic uses the following terms to describe the lifecycle of our models:
- **Active**: The model is fully supported and recommended for use.
- **Legacy**: The model will no longer receive updates and may be deprecated in the future.
- **Deprecated**: The model is no longer available for new customers but continues to be available for existing users until retirement. We assign a retirement date at this point.
- **Retired**: The model is no longer available for use. Requests to retired models will fail.

<Warning>
Please note that deprecated models are likely to be less reliable than active models. We urge you to move workloads to active models to maintain the highest level of support and reliability.
</Warning>

## Migrating to replacements

Once a model is deprecated, please migrate all usage to a suitable replacement before the retirement date. Requests to models past the retirement date will fail.

To help measure the performance of replacement models on your tasks, we recommend thorough testing of your applications with the new models well before the retirement date.

For specific instructions on migrating from Claude 3.7 to Claude 4.5 models, see [Migrating to Claude 4.5](/docs/en/about-claude/models/migrating-to-claude-4).

## Notifications

Anthropic notifies customers with active deployments for models with upcoming retirements. We provide at least 60 days notice before model retirement for publicly released models.

## Auditing model usage

To help identify usage of deprecated models, customers can access an audit of their API usage. Follow these steps:

1. Go to the [Usage](/settings/usage) page in Console
2. Click the "Export" button
3. Review the downloaded CSV to see usage broken down by API key and model

This audit will help you locate any instances where your application is still using deprecated models, allowing you to prioritize updates to newer models before the retirement date.

## Best practices

1. Regularly check our documentation for updates on model deprecations.
2. Test your applications with newer models well before the retirement date of your current model.
3. Update your code to use the recommended replacement model as soon as possible.
4. Contact our support team if you need assistance with migration or have any questions.

## Deprecation downsides and mitigations

We currently deprecate and retire models to ensure capacity for new model releases. We recognize that this comes with downsides:
- Users who value specific models must migrate to new versions
- Researchers lose access to models for ongoing and comparative studies
- Model retirement introduces safety- and model welfare-related risks

At some point, we hope to make past models publicly available again. In the meantime, we've committed to long-term preservation of model weights and other measures to help mitigate these impacts. For more details, see [Commitments on Model Deprecation and Preservation](https://www.anthropic.com/research/deprecation-commitments).

## Model status

All publicly released models are listed below with their status:

| API Model Name              | Current State       | Deprecated        | Tentative Retirement Date |
|:----------------------------|:--------------------|:------------------|:-------------------------|
| `claude-3-opus-20240229`    | Deprecated          | June 30, 2025     | January 5, 2026          |
| `claude-3-haiku-20240307`   | Active              | N/A               | Not sooner than March 7, 2025 |
| `claude-3-5-haiku-20241022` | Active              | N/A               | Not sooner than October 22, 2025 |
| `claude-3-7-sonnet-20250219`| Deprecated          | October 28, 2025  | February 19, 2026          |
| `claude-sonnet-4-20250514`  | Active              | N/A               | Not sooner than May 14, 2026 |
| `claude-opus-4-20250514`    | Active              | N/A               | Not sooner than May 14, 2026 |
| `claude-opus-4-1-20250805`  | Active              | N/A               | Not sooner than August 5, 2026 |
| `claude-sonnet-4-5-20250929`| Active              | N/A               | Not sooner than September 29, 2026 |
| `claude-haiku-4-5-20251001` | Active              | N/A               | Not sooner than October 15, 2026 |
| `claude-opus-4-5-20251101`  | Active              | N/A               | Not sooner than November 24, 2026 |

## Deprecation history

All deprecations are listed below, with the most recent announcements at the top.

### 2025-10-28: Claude Sonnet 3.7 model

On October 28, 2025, we notified developers using Claude Sonnet 3.7 model of its upcoming retirement on the Claude API.

| Retirement Date             | Deprecated Model            | Recommended Replacement         |
|:----------------------------|:----------------------------|:--------------------------------|
| February 19, 2026           | `claude-3-7-sonnet-20250219`| `claude-sonnet-4-5-20250929`     |

### 2025-08-13: Claude Sonnet 3.5 models

<Note>
These models were retired October 28, 2025.
</Note>

On August 13, 2025, we notified developers using Claude Sonnet 3.5 models of their upcoming retirement.

| Retirement Date             | Deprecated Model            | Recommended Replacement         |
|:----------------------------|:----------------------------|:--------------------------------|
| October 28, 2025            | `claude-3-5-sonnet-20240620`| `claude-sonnet-4-5-20250929`     |
| October 28, 2025            | `claude-3-5-sonnet-20241022`| `claude-sonnet-4-5-20250929`     |

### 2025-06-30: Claude Opus 3 model

On June 30, 2025, we notified developers using Claude Opus 3 model of its upcoming retirement.

| Retirement Date             | Deprecated Model            | Recommended Replacement         |
|:----------------------------|:----------------------------|:--------------------------------|
| January 5, 2026             | `claude-3-opus-20240229`    | `claude-opus-4-1-20250805`      |

### 2025-01-21: Claude 2, Claude 2.1, and Claude Sonnet 3 models

<Note>
These models were retired July 21, 2025.
</Note>

On January 21, 2025, we notified developers using Claude 2, Claude 2.1, and Claude Sonnet 3 models of their upcoming retirements. 

| Retirement Date             | Deprecated Model            | Recommended Replacement         |
|:----------------------------|:----------------------------|:--------------------------------|
| July 21, 2025               | `claude-2.0`                | `claude-sonnet-4-5-20250929`      |
| July 21, 2025               | `claude-2.1`                | `claude-sonnet-4-5-20250929`      |
| July 21, 2025               | `claude-3-sonnet-20240229`  | `claude-sonnet-4-5-20250929`      |

### 2024-09-04: Claude 1 and Instant models

<Note>
These models were retired November 6, 2024.
</Note>

On September 4, 2024, we notified developers using Claude 1 and Instant models of their upcoming retirements.

| Retirement Date             | Deprecated Model          | Recommended Replacement    |
|:----------------------------|:--------------------------|:---------------------------|
| November 6, 2024            | `claude-1.0`              | `claude-3-5-haiku-20241022`|
| November 6, 2024            | `claude-1.1`              | `claude-3-5-haiku-20241022`|
| November 6, 2024            | `claude-1.2`              | `claude-3-5-haiku-20241022`|
| November 6, 2024            | `claude-1.3`              | `claude-3-5-haiku-20241022`|
| November 6, 2024            | `claude-instant-1.0`      | `claude-3-5-haiku-20241022`|
| November 6, 2024            | `claude-instant-1.1`      | `claude-3-5-haiku-20241022`|
| November 6, 2024            | `claude-instant-1.2`      | `claude-3-5-haiku-20241022`|