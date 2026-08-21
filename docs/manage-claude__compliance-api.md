---
title: Compliance API
url: https://platform.claude.com/docs/en/manage-claude/compliance-api
description: Programmatic access to your organization's Claude activity, chats, files, projects, Claude Cowork and Claude Code sessions, and users for compliance, audit, and governance.
---

The Compliance API gives Claude Enterprise and Claude Console customers programmatic access to their organization's Activity Feed. For Claude Enterprise organizations, it also covers the directory of users, roles, and groups across every linked organization; the effective settings in force for each organization; the underlying chats, files, and projects in claude.ai organizations; and Cowork and Claude Code sessions. Security, legal, and compliance teams use it to audit activity, retrieve or delete content, and feed events into downstream tooling.

<Note>
  Two key types unlock the Compliance API. A **Compliance Access Key** (created in claude.ai) reaches every endpoint, and an **Admin API key** (created in Claude Console) reaches the Activity Feed only. See [Which key do you need?](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#which-key-do-you-need) for the full key-type comparison.
</Note>

The following call returns the most recent activity event in your organization. Any key with the `read:compliance_activities` scope can make it. To create a key and grant it that scope, see [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access).

```bash cURL
curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/activities?limit=1" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

A successful response returns a JSON object containing `data` (an array of `Activity` records), `has_more`, `first_id`, and `last_id`:

```json Response
{
  "data": [
    {
      "id": "activity_01XyDMpzjS89pFZXqSFUBDr6",
      "created_at": "2026-04-10T08:09:10Z",
      "organization_id": "org_01Wv6QeBcDfGhJkLmNpQrSt8",
      "organization_uuid": "abcdef01-2345-6789-abcd-ef0123456789",
      "actor": {
        "type": "user_actor",
        "email_address": "user@example.com",
        "user_id": "user_01TuVwXyZaBcDeFgH2JkLmN4",
        "ip_address": "192.0.2.34",
        "user_agent": "Mozilla/5.0..."
      },
      "type": "claude_chat_created",
      "claude_chat_id": "claude_chat_01XyDMpzjS89pFZXqSFUBDr6",
      "claude_project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq"
    }
  ],
  "has_more": true,
  "first_id": "activity_01XyDMpzjS89pFZXqSFUBDr6",
  "last_id": "activity_01XyDMpzjS89pFZXqSFUBDr6"
}
```

***

## How the Compliance API works

Every endpoint lives under `/v1/compliance/*` on `https://api.anthropic.com` and authenticates through the `x-api-key` header. To provision a key, see [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access).

The Activity Feed (`GET /v1/compliance/activities`) is available to any key that carries the `read:compliance_activities` scope; see [Query the Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) for filters, pagination, and the full `Activity` object. The remaining endpoints require a Compliance Access Key carrying the relevant scope.

A Claude Enterprise tenant has one parent organization (the top-level container that centralizes identity) with linked organizations of two kinds: claude.ai organizations, where users chat and store content, and Claude Console organizations, where users manage Claude API workloads. For a key that covers the parent organization, the directory endpoints (organizations, users, roles, and groups) return data from every linked organization of either kind. The content endpoints (chats, files, projects, project attachments, and sessions) serve Claude Enterprise data only. The chat, file, and project endpoints return claude.ai chats, files, and projects. The session endpoints return transcripts of Cowork and Claude Code sessions on users' machines (local sessions), captured while users are signed in with their Claude Enterprise account. They also return transcripts of Cowork sessions started on claude.ai web or mobile, which run in the cloud in Anthropic-managed environments (remote sessions). A standalone Claude Console organization (one with no parent organization) is not part of a Claude Enterprise tenant; it uses Admin API keys and can query the Activity Feed only.

All `/v1/compliance/*` endpoints share a rate limit of 600 requests per minute per parent organization (for a standalone Claude Console organization, per organization). The local session endpoints count only against that shared limit, and the remote session endpoints carry a second request budget on top. See [429 Too Many Requests](https://platform.claude.com/docs/en/manage-claude/compliance-errors#429-too-many-requests) for the response headers and retry contract.

***

## Compliance API versus related features

A few adjacent features overlap with the Compliance API; here is how to choose.

### Export audit logs

The audit log export is a separate feature in [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls) that lets owners and primary owners download a CSV of organization events. It's significantly narrower than the Compliance API: a capped lookback window, CSV download only, and no access to chat, file, or project content. Standardize on the Compliance API for ongoing programmatic use.

### Analytics API

Anthropic provides two analytics APIs: the Claude Enterprise Analytics API and the [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api). Both return aggregated usage and cost figures for IT, FinOps, and platform teams, whereas the Compliance API returns per-event records for security, legal, and compliance teams. The two API families answer different questions, use different keys, and are provisioned separately.

### OpenTelemetry logging

[Cowork's OpenTelemetry logging](https://support.claude.com/en/articles/14477985-monitor-claude-cowork-activity-with-opentelemetry) and [Claude Code monitoring](https://code.claude.com/docs/en/monitoring-usage) stream per-event telemetry, including token, cost, and host metadata, to a collector you run as activity happens, whereas the Compliance API returns retained per-session transcripts from Anthropic on request and works with your existing Compliance Access Key. For a side-by-side comparison, see the [Compliance API FAQ](https://platform.claude.com/docs/en/manage-claude/compliance-faq#data-coverage-and-retention).

### Inference hooks

[Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks) (beta) act inline: your organization's AI security server receives each governed prompt before inference and can deny it in real time, whereas the Compliance API retrieves records after the fact and returns richer data, such as organization settings and full non-text files.

***

## In this section

<CardGroup>
  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-api-access" title="Set up the Compliance API">
    Enable the Compliance API for your organization, then create a Compliance Access Key (with scoped permissions) or an Admin API key, and learn which to use.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed" title="Query the Activity Feed">
    Retrieve, filter, and paginate the shared Activity Feed. Supported by both key types.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-content-data" title="Retrieve and delete chats, files, and projects">
    Read chat content, files, and project attachments; delete chats, files, and projects on demand. Compliance Access Key required.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-sessions" title="Retrieve session transcripts">
    List the sessions your users run in Claude apps and agents, such as Cowork and Claude Code, and retrieve their transcripts. Compliance Access Key required.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-org-data" title="List organizations, users, roles, groups, and settings">
    Enumerate linked organizations, members, roles, and directory groups, and read each organization's effective settings.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-integration-patterns" title="Design your compliance integration">
    Choose a feed-consumption pattern, plan SIEM correlation, and decide your retention approach.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-errors" title="Handle Compliance API errors">
    Every 400, 401, 403, 404, 409, 429, and 5xx response the Compliance API returns, with the fix for each.
  </Card>

  <Card href="https://platform.claude.com/docs/en/api/compliance" title="API reference">
    Endpoint paths, parameters, and response schemas for every Compliance API call.
  </Card>

  <Card href="https://platform.claude.com/docs/en/manage-claude/compliance-faq" title="Compliance API FAQ">
    Answers to common key, scope, availability, and integration questions.
  </Card>
</CardGroup>
