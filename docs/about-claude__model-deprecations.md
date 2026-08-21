---
title: Model deprecations
url: https://platform.claude.com/docs/en/about-claude/model-deprecations
description: See which Claude models are active, deprecated, or retired, and find retirement dates and recommended replacements for models and API parameters.
---

As safer and more capable models launch, Anthropic regularly retires older ones. Applications relying on Anthropic models may need occasional updates to keep working. Impacted customers will always be notified by email and in the documentation.

This page lists all API deprecations, along with recommended replacements.

## Overview

Anthropic uses the following terms to describe the model lifecycle:

* **Active:** The model is fully supported and recommended for use.
* **Legacy:** The model will no longer receive updates and may be deprecated in the future.
* **Deprecated:** The model is still functional but no longer recommended. Anthropic provides a recommended replacement and assigns a retirement date.
* **Retired:** The model is no longer available for use. Requests to retired models will fail.

<Warning>
  Deprecated models are likely to be less reliable than active models. Move workloads to active models to maintain the highest level of support and reliability.
</Warning>

The dates on this page apply to Anthropic-operated platforms: the Claude API, [Claude Platform on AWS](https://platform.claude.com/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry). Partner-operated platforms (Amazon Bedrock and Google Cloud) set their own retirement schedules, so a model's lifecycle status and dates can differ. See the [Amazon Bedrock](https://platform.claude.com/docs/en/build-with-claude/claude-in-amazon-bedrock#supported-models), [Amazon Bedrock (Opus 4.6 and earlier)](https://platform.claude.com/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy#api-model-ids), and [Google Cloud](https://platform.claude.com/docs/en/build-with-claude/claude-on-vertex-ai#api-model-ids) model tables.

## Migrating to replacements

Once a model is deprecated, migrate all usage to a suitable replacement before the retirement date. Requests to models past the retirement date will fail.

To help measure the performance of replacement models on your tasks, consider thorough testing of your applications with the new models well before the retirement date.

For specific instructions on migrating to the latest Claude models, see the [Migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide).

## Notifications

Anthropic notifies customers with active deployments for models with upcoming retirements, providing at least 60 days' notice before model retirement for publicly released models.

## Auditing model usage

To help identify usage of deprecated models, customers can access an audit of their API usage. Follow these steps:

1. Go to the [Usage](https://platform.claude.com/usage) page in Claude Console.
2. Click **Export**.
3. Review the downloaded CSV to see usage broken down by API key and model.

This audit will help you locate any instances where your application is still using deprecated models, allowing you to prioritize updates to newer models before the retirement date.

## Best practices

1. Regularly check the documentation for updates on model deprecations.
2. Test your applications with newer models well before the retirement date of your current model.
3. Update your code to use the recommended replacement model as soon as possible.
4. Contact the support team if you need assistance with migration or have any questions.

## Deprecation downsides and mitigations

Anthropic currently deprecates and retires models to ensure capacity for new model releases. This comes with downsides:

* Users who value specific models must migrate to new versions
* Researchers lose access to models for ongoing and comparative studies
* Model retirement introduces safety- and model welfare-related risks

At some point, Anthropic hopes to make past models publicly available again. In the meantime, Anthropic has committed to long-term preservation of model weights and other measures to help mitigate these impacts. For more details, see [Commitments on Model Deprecation and Preservation](https://www.anthropic.com/research/deprecation-commitments).

## Model status

<Note>
  [Claude Mythos Preview](https://anthropic.com/glasswing) (`claude-mythos-preview`) is deprecated. To migrate to [Claude Mythos 5](https://anthropic.com/glasswing) (`claude-mythos-5`), see the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide#migrating-from-claude-mythos-preview).
</Note>

Current and recently retired models are listed in the following table with their status:

| API model name             | Current state | Deprecated        | Tentative retirement date          |
| -------------------------- | ------------- | ----------------- | ---------------------------------- |
| claude-fable-5             | Active        | N/A               | Not sooner than June 9, 2027       |
| claude-opus-5              | Active        | N/A               | Not sooner than July 24, 2027      |
| claude-opus-4-8            | Active        | N/A               | Not sooner than May 28, 2027       |
| claude-opus-4-7            | Active        | N/A               | Not sooner than April 16, 2027     |
| claude-opus-4-6            | Active        | N/A               | Not sooner than February 5, 2027   |
| claude-opus-4-5-20251101   | Active        | N/A               | Not sooner than November 24, 2026  |
| claude-opus-4-1-20250805   | Retired       | June 5, 2026      | August 5, 2026                     |
| claude-opus-4-20250514     | Retired       | April 14, 2026    | June 15, 2026                      |
| claude-sonnet-5            | Active        | N/A               | Not sooner than June 30, 2027      |
| claude-sonnet-4-6          | Active        | N/A               | Not sooner than February 17, 2027  |
| claude-sonnet-4-5-20250929 | Active        | N/A               | Not sooner than September 29, 2026 |
| claude-sonnet-4-20250514   | Retired       | April 14, 2026    | June 15, 2026                      |
| claude-3-7-sonnet-20250219 | Retired       | October 28, 2025  | February 19, 2026                  |
| claude-haiku-4-5-20251001  | Active        | N/A               | Not sooner than October 15, 2026   |
| claude-3-5-haiku-20241022  | Retired       | December 19, 2025 | February 19, 2026                  |
| claude-3-haiku-20240307    | Retired       | February 19, 2026 | April 20, 2026                     |

## Deprecation history

All deprecations are listed in the following sections, with the most recent announcements first.

### 2026-06-05: Claude Opus 4.1 model

<Note>
  This model was retired August 5, 2026.
</Note>

On June 5, 2026, Anthropic notified developers using Claude Opus 4.1 of its upcoming retirement on the Claude API.

| Retirement date | Deprecated model           | Recommended replacement |
| --------------- | -------------------------- | ----------------------- |
| August 5, 2026  | `claude-opus-4-1-20250805` | `claude-opus-4-8`       |

### 2026-04-14: Claude Sonnet 4 and Claude Opus 4 models

<Note>
  These models were retired June 15, 2026.
</Note>

On April 14, 2026, Anthropic notified developers using Claude Sonnet 4 and Claude Opus 4 models of their upcoming retirement on the Claude API.

| Retirement date | Deprecated model           | Recommended replacement |
| --------------- | -------------------------- | ----------------------- |
| June 15, 2026   | `claude-sonnet-4-20250514` | `claude-sonnet-4-6`     |
| June 15, 2026   | `claude-opus-4-20250514`   | `claude-opus-4-8`       |

### 2026-02-19: Claude Haiku 3 model

<Note>
  This model was retired April 20, 2026.
</Note>

On February 19, 2026, Anthropic notified developers using Claude Haiku 3 model of its upcoming retirement on the Claude API.

| Retirement date | Deprecated model          | Recommended replacement     |
| --------------- | ------------------------- | --------------------------- |
| April 20, 2026  | `claude-3-haiku-20240307` | `claude-haiku-4-5-20251001` |

### 2025-12-19: Claude Haiku 3.5 model

<Note>
  This model was retired February 19, 2026.
</Note>

On December 19, 2025, Anthropic notified developers using Claude Haiku 3.5 model of its upcoming retirement on the Claude API.

| Retirement date   | Deprecated model            | Recommended replacement     |
| ----------------- | --------------------------- | --------------------------- |
| February 19, 2026 | `claude-3-5-haiku-20241022` | `claude-haiku-4-5-20251001` |

### 2025-10-28: Claude Sonnet 3.7 model

<Note>
  This model was retired February 19, 2026.
</Note>

On October 28, 2025, Anthropic notified developers using Claude Sonnet 3.7 model of its upcoming retirement on the Claude API.

| Retirement date   | Deprecated model             | Recommended replacement |
| ----------------- | ---------------------------- | ----------------------- |
| February 19, 2026 | `claude-3-7-sonnet-20250219` | `claude-sonnet-4-6`     |

### 2025-08-13: Claude Sonnet 3.5 models

<Note>
  These models were retired October 28, 2025.
</Note>

On August 13, 2025, Anthropic notified developers using Claude Sonnet 3.5 models of their upcoming retirement.

| Retirement date  | Deprecated model             | Recommended replacement |
| ---------------- | ---------------------------- | ----------------------- |
| October 28, 2025 | `claude-3-5-sonnet-20240620` | `claude-sonnet-4-6`     |
| October 28, 2025 | `claude-3-5-sonnet-20241022` | `claude-sonnet-4-6`     |

### 2025-06-30: Claude Opus 3 model

<Note>
  This model was retired January 5, 2026.
</Note>

On June 30, 2025, Anthropic notified developers using Claude Opus 3 model of its upcoming retirement.

| Retirement date | Deprecated model         | Recommended replacement |
| --------------- | ------------------------ | ----------------------- |
| January 5, 2026 | `claude-3-opus-20240229` | `claude-opus-4-8`       |

### 2025-01-21: Claude 2, Claude 2.1, and Claude Sonnet 3 models

<Note>
  These models were retired July 21, 2025.
</Note>

On January 21, 2025, Anthropic notified developers using Claude 2, Claude 2.1, and Claude Sonnet 3 models of their upcoming retirements.

| Retirement date | Deprecated model           | Recommended replacement |
| --------------- | -------------------------- | ----------------------- |
| July 21, 2025   | `claude-2.0`               | `claude-opus-4-8`       |
| July 21, 2025   | `claude-2.1`               | `claude-opus-4-8`       |
| July 21, 2025   | `claude-3-sonnet-20240229` | `claude-sonnet-4-6`     |

### 2024-09-04: Claude 1 and Instant models

<Note>
  These models were retired November 6, 2024.
</Note>

On September 4, 2024, Anthropic notified developers using Claude 1 and Instant models of their upcoming retirements.

| Retirement date  | Deprecated model     | Recommended replacement     |
| ---------------- | -------------------- | --------------------------- |
| November 6, 2024 | `claude-1.0`         | `claude-haiku-4-5-20251001` |
| November 6, 2024 | `claude-1.1`         | `claude-haiku-4-5-20251001` |
| November 6, 2024 | `claude-1.2`         | `claude-haiku-4-5-20251001` |
| November 6, 2024 | `claude-1.3`         | `claude-haiku-4-5-20251001` |
| November 6, 2024 | `claude-instant-1.0` | `claude-haiku-4-5-20251001` |
| November 6, 2024 | `claude-instant-1.1` | `claude-haiku-4-5-20251001` |
| November 6, 2024 | `claude-instant-1.2` | `claude-haiku-4-5-20251001` |

## API parameter deprecations

Anthropic occasionally deprecates request parameters that no longer apply to current models. Deprecated parameters remain in the SDK request types so existing code continues to type-check, but their behavior changes per model.

| Parameter                       | Status                                 | Behavior                                                                                                                                         | Recommended replacement                                                                                                                                     |
| ------------------------------- | -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `temperature`, `top_p`, `top_k` | Deprecated (Claude Opus 4.7 and later) | Returns a 400 error when set to a non-default value on Claude 4.7 and later models and [Claude Mythos Preview](https://anthropic.com/glasswing). | Omit and use [prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) to guide model behavior. |

For migration steps, see the [migration guide](https://platform.claude.com/docs/en/about-claude/models/migration-guide).
