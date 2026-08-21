---
title: Compliance API FAQ
url: https://platform.claude.com/docs/en/manage-claude/compliance-faq
description: Answers to common questions about Compliance API access, scopes, retention, and integration.
---

<Note>
  To enable the Compliance API, see [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access).
</Note>

## Access and scopes

<AccordionGroup>
  <Accordion title="Who can enable the Compliance API?">
    For a Claude Enterprise organization, the primary owner enables the Compliance API at [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), and enablement cascades from the parent organization to every linked organization. For an eligible standalone Claude Console organization (one with no parent organization), an organization admin enables it at [Claude Console > Settings > Security](https://platform.claude.com/settings/security). A Claude Console organization that is linked to a parent organization does not enable the Compliance API itself; it is enabled from the parent organization. See [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) for the steps.
  </Accordion>

  <Accordion title="Can I turn the Compliance API off after enabling it in Claude Console?">
    Yes. For a standalone Claude Console organization, an organization admin can turn the **Compliance API** toggle off at [Claude Console > Settings > Security](https://platform.claude.com/settings/security), the same place it is turned on. While the Compliance API is off, no activity events are recorded for your organization, so the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) receives no new events. If your organization is enrolled in [Access Transparency](https://platform.claude.com/docs/en/manage-claude/access-transparency), turning the Compliance API off also stops Access Transparency event delivery. Activity that is not recorded while the Compliance API is off cannot be recovered later. Turning the Compliance API back on resumes recording from that point forward; activity that was already recorded is not deleted.
  </Accordion>

  <Accordion title="Does turning the Compliance API off delete events that were already captured?">
    No. Turning the Compliance API off stops new activity events from being recorded, but it does not delete events that were already captured while it was on. Recording resumes from the point the Compliance API is turned back on.
  </Accordion>

  <Accordion title="Is turning the Compliance API off in Claude Console recorded anywhere?">
    Yes. When the Compliance API is turned off (or back on) in Claude Console, the change is recorded as an organization settings-updated activity in the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed), so your audit trail shows who changed the setting and when. This activity is an exception to the recording stop: the disable is recorded even though no other activity is recorded while the Compliance API is off.
  </Accordion>

  <Accordion title="Why doesn't my parent organization appear in Claude Console when creating an Admin API key?">
    This is expected. A Claude Enterprise parent organization centralizes identity across all linked organizations; it does not carry workloads, and it does not appear in Claude Console at all. Claude Console only ever shows the Claude Console organizations linked beneath the parent.

    To call the Compliance API, you create one of two key types instead:

    * **For full Compliance API access ([Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) plus chats, files, projects, sessions, users, organization metadata, and organization settings),** the primary owner of the parent organization (or an organization owner, for a key restricted to their own organization only) creates a [Compliance Access Key](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) in claude.ai.
    * **For Activity Feed access only,** an organization admin in your Claude Console organization creates an [Admin API key](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#create-an-admin-api-key) in Claude Console. The Compliance API must already be enabled for the organization, and the admin must create the Admin API key while the Compliance API is enabled for it to carry the `read:compliance_activities` scope.
  </Accordion>

  <Accordion title="Can I use my regular Claude API key with the Compliance API?">
    No. A Claude API key (`sk-ant-api03-...`) authenticates calls to Claude models on the Claude API; it does not authenticate calls to `/v1/compliance/*`. The Compliance API accepts only Compliance Access Keys (`sk-ant-api01-...`) and Admin API keys (`sk-ant-admin01-...`). See [Which key do you need?](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#which-key-do-you-need) for the full mapping.
  </Accordion>

  <Accordion title="Why does my Admin API key return 403 on chat or file endpoints?">
    Admin API keys carry a fixed `read:compliance_activities` scope, which authorizes the Activity Feed only. Every other Compliance API endpoint requires a scope that only a Compliance Access Key created in claude.ai can carry. Calling a content or directory endpoint with an Admin API key returns a 403 naming the scope that endpoint family requires: `read:compliance_user_data` for chats, files, projects, project attachments, sessions, users, and group members, and `read:compliance_org_data` for organizations, roles, groups, and effective organization settings. For example, listing chats returns the following response.

    ```json Response
    {
      "error": {
        "type": "permission_error",
        "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
      }
    }
    ```

    To access content endpoints, the primary owner of your parent organization (or an organization owner, for their own organization only) must [create a Compliance Access Key](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) with `read:compliance_user_data` (and `delete:compliance_user_data` for deletes), or `read:compliance_org_data` for organization, role, group, and effective-settings endpoints. See [Handle Compliance API errors](https://platform.claude.com/docs/en/manage-claude/compliance-errors#403-forbidden) for the full per-endpoint catalog.
  </Accordion>
</AccordionGroup>

## Data coverage and retention

<AccordionGroup>
  <Accordion title="How far back does the Activity Feed go?">
    The Activity Feed retains 6 years of organization activity, and new events are queryable within 1 minute of occurring. Activity Feed retention is independent of your organization's content retention policy: chat, file, and project content follows the retention rules configured for your organization (indefinite by default).
  </Accordion>

  <Accordion title="Does the Activity Feed include prompt or message content?">
    No. The Activity Feed records who did what and when (authentication, chat creation, file uploads, project changes, administrative actions, and similar resource events), but it does not capture the prompt text or model responses inside chats or messages.

    To retrieve message bodies and file contents, use the chat, message, and file endpoints with a Compliance Access Key carrying `read:compliance_user_data`. The same key and scope retrieve transcripts of Cowork and Claude Code sessions on users' machines through the [local session endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions), and transcripts of Cowork sessions in the cloud through the [remote session endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-remote-sessions). These endpoints serve Claude Enterprise content only; Claude Console workloads, and Claude API workloads authenticated with an API key, expose administrative and resource events through the Activity Feed but do not expose prompt text or model responses through the Compliance API.
  </Accordion>

  <Accordion title="Do Cowork and Claude Code sessions appear in the Compliance API?">
    Yes. Cowork sessions in Claude Desktop that run on users' machines, and Claude Code sessions in the terminal, in Claude Desktop, or in an IDE extension, are captured while users are signed in with their Claude Enterprise account and are available through the [local session endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions). Cowork sessions started on claude.ai web or mobile, which run in the cloud in Anthropic-managed environments, are available through the [remote session endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-remote-sessions). Each family has a list endpoint that returns session metadata and a messages endpoint that returns the session transcript (user prompts, assistant responses, and tool calls and results). The local family adds a third endpoint that retrieves one session's metadata. All of these endpoints use your existing Compliance Access Key with `read:compliance_user_data`; no new key or scope is needed.

    Local sessions are captured as their requests reach the Claude API, so nothing is installed on the device, and on-device activity that never reaches the API is not captured. Claude Code sessions authenticated with a Claude Console API key, Claude Code sessions run through a third-party cloud platform (Amazon Bedrock, Google Cloud, or Microsoft Foundry), and Claude Code on the web are not captured. Claude Code on the web also runs in the cloud in Anthropic-managed environments, but it is not a remote session; the remote session endpoints return Cowork sessions only. Organizations with [HIPAA readiness](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#hipaa-readiness) enabled get no local session data, and sessions for which [zero data retention (ZDR)](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) is in effect are excluded.

    The local and remote session endpoints are in beta.
  </Accordion>

  <Accordion title="What do Cowork and Claude Code session transcripts include?">
    Local and remote session transcripts both carry user prompts, assistant responses, and tool calls and results. For local sessions (Cowork and Claude Code on users' machines), that is what Claude was asked to do and what it returned, not what happened on the device.

    | Data                              | Local sessions (on users' machines)                                                                                                                                                                                                                            | Remote sessions (in the cloud)                                                                                                                                          |
    | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | User prompts                      | Yes; returned as `text` blocks.                                                                                                                                                                                                                                | Yes; returned as `text` blocks.                                                                                                                                         |
    | Assistant responses               | Yes; text output only.                                                                                                                                                                                                                                         | Yes; text output only.                                                                                                                                                  |
    | Tool calls and results            | Yes; each `tool_use` input and each `text` entry in a `tool_result` is truncated to 10,000 bytes by default (up to about 1 MiB each on request).                                                                                                               | Yes; each `tool_use` input and each `text` entry in a `tool_result` is truncated to 10,000 bytes by default (up to about 1 MiB each on request).                        |
    | File contents and file names      | Yes; text that Claude reads through tools appears in the transcript, subject to the same truncation. Images, PDFs, and other binary or structured content appear only as placeholder `text` blocks. File names appear in tool-call inputs and outputs.         | Yes; file contents and file names appear in the transcript through tool-call inputs and outputs (text only; other content is omitted).                                  |
    | Artifacts                         | Yes; generated content appears inside tool-call inputs in the transcript.                                                                                                                                                                                      | Yes; generated content appears inside tool-call inputs in the transcript.                                                                                               |
    | Skills                            | Yes; skill content appears when the client sends it as message content, and it is not distinguished from other user text.                                                                                                                                      | Yes; skill content appears in the transcript.                                                                                                                           |
    | Session metadata                  | Yes; owner (`user.id` and email address), organization, workspace, `product_surface`, and `created_at`, from the list and retrieve endpoints. Local sessions carry no `status` or `updated_at`.                                                                | Yes; owner, organization, status, timestamps, and `product_surface`, from the list endpoint.                                                                            |
    | Thinking blocks                   | No.                                                                                                                                                                                                                                                            | No.                                                                                                                                                                     |
    | Images and other non-text content | No; each image, PDF, or other binary or structured block appears as a placeholder `text` block (for example, `[image content not shown]`) with `truncated` set to `true`. Raw file bytes are never returned.                                                   | No; non-text blocks are omitted, and raw file bytes are never returned.                                                                                                 |
    | Token usage, cost, and latency    | No; use [Cowork's OpenTelemetry logging](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) or [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage) for usage and performance telemetry. | No; use [OpenTelemetry logging](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) for usage and performance telemetry. |

    See [Sessions on users' machines](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions) and [Sessions in the cloud](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-remote-sessions) for the endpoints and parameters.
  </Accordion>

  <Accordion title="How does session coverage compare with OpenTelemetry logging (OTEL) for Cowork and Claude Code?">
    [Cowork's OpenTelemetry logging](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) and [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage) overlap with the session endpoints but answer different needs: OTEL streams per-event telemetry to infrastructure you run as activity happens, whereas the Compliance API lets you retrieve retained per-session transcripts from Anthropic after the fact.

    |                                                           | Local sessions (on users' machines)                                                                                         | Remote sessions (in the cloud)                                                     | OpenTelemetry logging                                                                                         |
    | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
    | Delivery                                                  | Pull: query and export over HTTPS                                                                                           | Pull: query and export over HTTPS                                                  | Push: streamed to your OTLP collector                                                                         |
    | Setup                                                     | Works with your existing Compliance Access Key                                                                              | Works with your existing Compliance Access Key                                     | Admin configures an OTLP endpoint and content-capture settings                                                |
    | Infrastructure                                            | Anthropic-hosted                                                                                                            | Anthropic-hosted                                                                   | You run the collector and storage                                                                             |
    | Retention                                                 | 6 years by default, or your organization's custom conversation retention period when a finite one is set; held by Anthropic | 6 years, held by Anthropic                                                         | Your infrastructure, your policies                                                                            |
    | User prompts and assistant responses                      | Yes                                                                                                                         | Yes                                                                                | Yes, subject to content-capture settings                                                                      |
    | Tool inputs                                               | Truncated to 10,000 bytes per input by default; up to about 1 MiB on request                                                | Truncated to 10,000 bytes per input by default; up to about 1 MiB on request       | Truncated summaries                                                                                           |
    | Tool result content                                       | Each text entry truncated to 10,000 bytes by default; up to about 1 MiB on request                                          | Each text entry truncated to 10,000 bytes by default; up to about 1 MiB on request | Metadata such as size and success; Claude Code can also capture content with an optional, size-capped setting |
    | File contents                                             | Yes, through transcript tool calls (text only; other content appears as a placeholder)                                      | Yes, through transcript tool calls (text only; other content is omitted)           | File paths; Claude Code can also capture contents with an optional, size-capped setting                       |
    | Host and device metadata (terminal type, workspace paths) | No                                                                                                                          | No                                                                                 | Yes                                                                                                           |
    | Token usage and cost                                      | No                                                                                                                          | No                                                                                 | Yes                                                                                                           |

    OTEL events and Compliance API records share organization and user identifiers, so you can join them.
  </Accordion>

  <Accordion title="Is deleted content recoverable through the Compliance API?">
    No. Deletes performed through the Compliance API are immediate, permanent, and not recoverable. Chats that a user deleted through claude.ai are soft-deleted: they remain visible through the Compliance API with `deleted_at` populated until your organization's retention window expires or you hard-delete them through this API. Pull any content you need to retain (for legal hold or archival) before issuing a `DELETE` request.
  </Accordion>

  <Accordion title="What does the Compliance API not capture?">
    The Compliance API has known coverage boundaries: the Activity Feed records resource events but not prompt or response text, Claude Console and Claude API workloads authenticated with an API key expose no message content at all, and content removed by your retention policy or by a hard delete is not recoverable. For the full coverage boundaries and delivery contract, see [Delivery guarantees and completeness](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).

    Cowork and Claude Code session transcripts have boundaries of their own. Local sessions are captured only as their requests reach the Claude API, so on-device activity that never reaches the API is not captured. Claude Code sessions authenticated with a Claude Console API key, Claude Code sessions run through a third-party cloud platform (Amazon Bedrock, Google Cloud, or Microsoft Foundry), and Claude Code on the web are not captured either; organizations with HIPAA readiness enabled get no local session data; and sessions for which zero data retention is in effect are excluded. No session transcript, local or remote, includes thinking blocks or tool definitions. Organizations that use [customer-managed encryption keys](https://platform.claude.com/docs/en/manage-claude/cmek) see local session metadata but no transcript content.
  </Accordion>
</AccordionGroup>

## Integration and pagination

<AccordionGroup>
  <Accordion title="How do I correlate Compliance API records with my SIEM?">
    Join `Activity` records to your SIEM on `actor.user_id`, `actor.email_address`, `actor.ip_address`, and `created_at`. See [Design your compliance integration](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns#correlate-with-your-siem) for the join-key table and consumption patterns.
  </Accordion>

  <Accordion title="Can one customer have multiple organizations under one parent?">
    Yes. A Claude Enterprise parent organization can have many linked organizations, including a mix of claude.ai organizations and Claude Console organizations (for example, separate production and staging Claude Console organizations). Identity, SSO, and SCIM are shared across the parent; billing, members, projects, and API keys remain separate for each organization. Compliance API enablement happens at the parent organization level and cascades to all linked organizations, and a Compliance Access Key that covers the parent organization and carries `read:compliance_org_data` can enumerate every organization beneath the parent through `GET /v1/compliance/organizations`.
  </Accordion>

  <Accordion title="Are activities returned in order, and how do I detect when I have caught up to real time?">
    Activities are returned newest first, with ties in `created_at` broken by activity ID. To catch up, walk pages forward by `before_id` until `has_more` is `false`; that final response's `first_id` is your new cursor and you have reached the present. The full loop, including initial backfill and the safety conditions on cursor persistence, is in [Cursor-driven incremental reads](https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).
  </Accordion>

  <Accordion title="How do I get a sandbox to test the Compliance API?">
    To test only the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed), you do not need a Claude Enterprise organization: an organization admin can [enable the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) on an eligible standalone Claude Console test organization and query the feed with a new Admin API key. If the **Compliance API** section is not visible in that organization's Security settings, the organization is not eligible for self-service enablement.

    To test every endpoint, set up a Claude Enterprise sandbox organization linked to a Claude Console organization under the same parent. This lets the sandbox exercise both the Activity Feed (through an Admin API key) and the chat, file, project, and session endpoints (through a Compliance Access Key).

    1. **Provision the Claude Enterprise organization.** Contact your Anthropic representative to set up a Claude Enterprise sandbox organization. On an existing Claude Enterprise organization, the primary owner can [enable the Compliance API directly in claude.ai](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api).
    2. **Create the Claude Console organization.** Create a Claude Console organization yourself at `platform.claude.com` using the same email address.
    3. **Link the two organizations.** Sign in as the primary owner of the Claude Enterprise organization, go to [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), and use **Merge Organizations** to link the two under a shared parent.

    Once linked, follow [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access) to create keys and start querying. Test organizations use the same enablement process as production organizations.
  </Accordion>
</AccordionGroup>
