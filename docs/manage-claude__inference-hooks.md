---
title: Inference hooks
url: https://platform.claude.com/docs/en/manage-claude/inference-hooks
description: Send each governed prompt to your organization's AI security server for an allow or deny verdict before inference proceeds.
---

<Note>
  Inference hooks are in beta and available to Claude Enterprise organizations. Configuring them requires the `organization:manage` permission in claude.ai, which the built-in Admin, Owner, and Primary owner roles hold; see [Configure Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration).
</Note>

Inference hooks let a Claude Enterprise organization route every governed prompt through an AI security server, an HTTPS service that the organization or its security vendor operates, before inference runs. When a user submits a prompt, Anthropic sends the conversation transcript to your AI security server and waits for an allow or deny verdict; a denied request never reaches the model. Security and compliance teams use Inference hooks to enforce data policies inline, and developers build the AI security server that evaluates each request.

Because the hook runs on Anthropic's servers, after the request leaves the client and before the model runs, it applies to every governed request uniformly, with nothing to install or deploy on user devices.

Today the only hook event is `prompt`, which fires once per governed inference request, before inference begins. Response-side enforcement is planned as a later event.

***

## How Inference hooks work

1. A user submits a prompt on a governed surface.
2. Anthropic sends an HTTPS `POST` to your organization's configured AI security server endpoint. The request body carries the conversation transcript, and each request is signed according to the [Standard Webhooks](https://www.standardwebhooks.com/) specification once your organization generates its signing secret, so your server can verify it came from Anthropic.
3. Your AI security server evaluates the content and responds with a verdict within the verdict timeout your organization configures (5 seconds by default).
4. On `allow`, inference proceeds normally. On `deny`, the request is rejected and the user sees a blocked-by-policy message assembled from two parts: the per-request reason your AI security server supplied in the verdict's `deny_reason` field, followed by a standing message your administrators configure (for example, who to contact or where to request an exception). If your administrators haven't configured one, a built-in default directs the user to contact them. Each denial is also recorded in your organization's [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed).

The following diagram traces one example (a Cowork request where Claude also calls an O365 tool) to illustrate which parts of the flow are hooked. The hooked points are the diagram's steps 1 and 5, where the prompt arrives and the tool result returns; each results in the validation exchange with your AI security server shown in steps 2 and 6.

![Flow diagram: the AI security server validates both the prompt and the tool result before inference proceeds](https://platform.claude.com/docs/images/inference-hooks-flow.svg)

A verdict is a small JSON object: `{"action": "allow"}` lets the request proceed, and a deny carries the user-facing reason. For the full verdict schema, see [Return a verdict](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint#return-a-verdict).

Your AI security server sees what the user sees: transcript text, tool calls and their results, and text extracted from attachments. It never receives raw file or image bytes, system prompts, or Anthropic-internal context.

If your AI security server is unreachable, returns an error, or doesn't respond within the timeout, your organization's failure handling setting decides the outcome: block the request, or allow it to proceed without inspection.

Enforcement can roll out at your pace, so nobody has to be blocked on day one: shadow mode observes verdicts on live traffic without blocking anything, a rollout percentage inspects a chosen fraction of requests, and exclusions exempt members of chosen roles entirely. See [Configure Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration).

For the full request and response schemas, signature verification, and operational details, see [Develop an integration](https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint).

***

## Use cases

* **Data loss prevention (DLP).** Forward the transcript to your DLP scanner and deny prompts that carry regulated or classified material. This is the most common deployment.
* **Real-time transcript archival.** Archive each transcript as it arrives and always return `allow`, as a push-based alternative to polling the [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api).
* **Prompt telemetry.** Measure how your organization uses Claude, at the moment of use.
* **Policy engines.** Enforce your own rules before inference: model allowlists, project-scoped restrictions, or working-hours controls.

***

## Current limitations

* Attachments are represented by metadata and extracted text. Raw file and image bytes are never sent, so image-only content (for example, a screenshot of a document) is not inspected.
* Verdicts are allow or deny. Rewriting or redacting a prompt is not supported.
* Platform organizations (API access through the Claude Platform) are out of scope.

***

## Availability

Inference hooks are available to Claude Enterprise organizations. Configuring them requires the `organization:manage` permission, which the built-in Admin, Owner, and Primary owner roles hold, as does any custom role granted it.

One hook governs conversations across claude.ai, Cowork, and Claude Code sessions in your Claude Enterprise organization, whether they run on the web, in the desktop app, or in the CLI. Inference hooks are not available on Amazon Bedrock or Google Cloud.

Governed requests are the inference requests behind the user's conversation. Ancillary requests, such as conversation title generation, aren't sent to your endpoint, and system prompts and tool definitions are never included in what is sent. Voice mode is not covered.

***

## Inference hooks versus the Compliance API

Both features serve security, legal, and compliance teams at Claude Enterprise organizations.

|              | Inference hooks                                     | Compliance API                                                                                                         |
| ------------ | --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| When it acts | Inline, before inference runs                       | After the fact                                                                                                         |
| What it does | Allows or denies each governed request in real time | Retrieves activity, chats, files, projects, Cowork and Claude Code session transcripts, and users for audit and export |
| Direction    | Anthropic calls your AI security server             | You call Anthropic's API                                                                                               |

Use Inference hooks to stop a request before it reaches the model, and the [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) to audit what happened afterward.

***

## In this section

<CardGroup>
  <Card href="https://platform.claude.com/docs/en/manage-claude/inference-hooks-configuration" title="Configure Inference hooks">
    Allow Inference hooks for your organization, set up and test your AI security server, choose failure handling, and enforce verdicts.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/inference-hooks-endpoint" title="Develop an Inference hooks integration">
    The request and verdict schemas, signature verification, operational semantics, and integration patterns for building the AI security server.
  </Card>
</CardGroup>
