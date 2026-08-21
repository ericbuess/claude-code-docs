---
title: Retrieve session transcripts
url: https://platform.claude.com/docs/en/manage-claude/compliance-sessions
description: List the sessions your users run in Claude apps and agents, such as Claude Cowork and Claude Code, and retrieve their transcripts through the Compliance API.
---

<Note>
  The endpoints on this page are available only to Claude Enterprise organizations and are in beta. They work with the same Compliance Access Key and `read:compliance_user_data` scope as the [chat, file, and project endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-content-data); no new key, scope, setting, or client update is required. See [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access).
</Note>

<Check>
  **Required scope:** `read:compliance_user_data` on the Compliance Access Key.

  **Prerequisite:** None for listing sessions organization-wide. To filter the remote session list (sessions in the cloud) to specific users, you need user IDs from [List organization users](https://platform.claude.com/docs/en/manage-claude/compliance-org-data#list-organization-users); the local session list has no user filter.
</Check>

The endpoints on this page expose transcripts of the sessions your users run in Claude apps and agents (today, Cowork and Claude Code) from your Claude Enterprise organizations to compliance reviewers. Each session is a single conversation with Claude; its transcript is the sequence of user prompts, assistant responses, and tool calls and results in that conversation. The endpoints support eDiscovery (electronic discovery) exports and data loss prevention (DLP) enforcement.

The Compliance API groups sessions into two endpoint families according to where they run: local session endpoints for sessions on users' machines, and remote session endpoints for sessions that run in the cloud in Anthropic-managed environments. Both families are read-only, and neither is available to Admin API keys (`sk-ant-admin01-...`): calls authenticated with an Admin API key return [403 Forbidden](https://platform.claude.com/docs/en/manage-claude/compliance-errors#403-forbidden).

The following table maps each product, and where it runs, to the endpoint family that returns its sessions and the `product_surface` value that identifies them in responses. Products are added to this table as coverage expands.

| Product and where it runs                                                                                  | Endpoint family                                                  | `product_surface` |
| ---------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------- |
| Cowork in Claude Desktop, running on the user's machine                                                    | Local session endpoints (`/v1/compliance/apps/sessions/local`)   | `cowork`          |
| Claude Code in the terminal, in Claude Desktop, or in an IDE extension, running on the user's machine      | Local session endpoints                                          | `claude_code`     |
| Cowork sessions started on claude.ai web or mobile, running in the cloud in Anthropic-managed environments | Remote session endpoints (`/v1/compliance/apps/sessions/remote`) | `cowork_remote`   |

Capture of local sessions is tied to the Compliance API being enabled for your organization and applies while users are signed in with their Claude Enterprise account. The session endpoints do not return the following:

* Claude Code sessions authenticated with a Claude Console API key, or run through a third-party cloud platform such as Amazon Bedrock, Google Cloud, or Microsoft Foundry.
* Claude Code on the web. It also runs in the cloud in Anthropic-managed environments, but it is not a remote session; the remote session endpoints return Cowork sessions only.
* Local sessions in organizations with [HIPAA readiness](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#hipaa-readiness) enabled. No local session data is captured, so the local session endpoints return no sessions for those organizations.
* Local sessions for which [zero data retention (ZDR)](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#zero-data-retention-zdr-scope) is in effect. These sessions are excluded from list results, and the retrieve and messages endpoints return 404 for them.

The following table summarizes how [local sessions](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions) and [remote sessions](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-remote-sessions) differ.

|                          | Local sessions (on users' machines)                                                                      | Remote sessions (in the cloud)                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Endpoints                | List, retrieve, and messages endpoints under `/v1/compliance/apps/sessions/local`                        | List and messages endpoints under `/v1/compliance/apps/sessions/remote` |
| ID prefix                | `clls_`                                                                                                  | `cse_`                                                                  |
| List filters             | `created_at` range only                                                                                  | Organization, user, and `created_at` range                              |
| Lifecycle fields         | None: no `status` or `updated_at`                                                                        | `status`, `updated_at`                                                  |
| Retention                | 6 years by default, or your organization's custom conversation retention period when a finite one is set | 6 years                                                                 |
| Rate limits              | Shared Compliance API limit only                                                                         | Shared Compliance API limit plus a second request budget                |
| Deletion through the API | No                                                                                                       | No                                                                      |

## Sessions on users' machines (local sessions)

Local sessions run on users' machines while they are signed in with their Claude Enterprise account: today, Cowork in Claude Desktop, and Claude Code in the terminal, in Claude Desktop, or in an IDE extension.

The Compliance API exposes local sessions through three endpoints: `GET /v1/compliance/apps/sessions/local` lists session metadata, `GET /v1/compliance/apps/sessions/local/{session_id}` retrieves one session's metadata, and `GET /v1/compliance/apps/sessions/local/{session_id}/messages` returns one session's transcript. All three require the `read:compliance_user_data` scope and count only against the shared Compliance API rate limit; they are not subject to the second request budget that applies to the remote session endpoints. See [429 Too Many Requests](https://platform.claude.com/docs/en/manage-claude/compliance-errors#429-too-many-requests). If local sessions are not available to your parent organization, all three endpoints return 404 with the message `Local sessions are not available.` (see [Local session not found](https://platform.claude.com/docs/en/manage-claude/compliance-errors#local-session-not-found)); while session listings or captured content are temporarily unavailable, they return 503 (see [Local sessions temporarily unavailable](https://platform.claude.com/docs/en/manage-claude/compliance-errors#local-sessions-temporarily-unavailable)).

For local sessions, Anthropic records each conversation server-side as its requests reach the Claude API; nothing is installed on the device, and nothing is collected beyond the requests the client already sends to the Claude API. Local session transcripts show what Claude was asked to do and what it returned, not what happened on the device. File and network activity is visible only through the tool calls and tool results in the transcript, so activity that never reaches the API (for example, local files the session never sent) is not captured.

In organizations that use [customer-managed encryption keys](https://platform.claude.com/docs/en/manage-claude/cmek), local sessions are listed and retrievable as usual, but transcript content is not currently returned; each message comes back with its content marked unavailable (see [Retrieve a local session transcript](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-a-local-session-transcript) for how such messages are marked).

The list endpoint returns session metadata, with no transcript content, for every linked organization your key can read. Unlike the remote session list, it has no organization or user filters: bound the results in time with the `created_at.gte` and `created_at.lt` parameters. Both take RFC 3339 timestamps with a required UTC offset, and when both are supplied, `created_at.lt` must be strictly after `created_at.gte` or the request returns [400 Bad Request](https://platform.claude.com/docs/en/manage-claude/compliance-errors#400-bad-request). New sessions and messages appear in results after a short processing delay, typically within minutes; a session that is missing immediately after it starts is not necessarily uncaptured. The following request lists sessions created since a given date.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "created_at.gte=2026-07-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

```json Response
{
  "data": [
    {
      "type": "compliance_local_session",
      "id": "clls_01HxKpLmNoPqRsTuVwXyZaBc",
      "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
      "workspace_id": "wrkspc_01SvYKoWVRVHoEbwESNvzYdR",
      "user": {
        "id": "user_01GpKpLmNoPqRsTuVwXyZaBc",
        "email_address": "engineer@example.com"
      },
      "product_surface": "cowork",
      "created_at": "2026-07-09T14:02:11Z"
    },
    {
      "type": "compliance_local_session",
      "id": "clls_01HyLqMnOpQrStUvWxYzAbCd",
      "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
      "workspace_id": null,
      "user": {
        "id": "user_01HqRsTuVwXyZaBcDeFgHiJk",
        "email_address": null
      },
      "product_surface": "claude_code",
      "created_at": "2026-07-08T09:15:43Z"
    }
  ],
  "next_page": "page_AAEfQx7mPdLkq9Rt2VwHbZk"
}
```

Results are sorted in reverse chronological order (newest first) by `created_at`, with ties broken in a fixed server-side order, and capped at `limit` results per response (default 100, max 500). The endpoint paginates forward only with `page` and `next_page` tokens (see [Paginate results](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed#paginate-results)): pass the response's `next_page` value back as the `page` query parameter on the next request, and stop when `next_page` is `null`. The response has no `has_more` field. Complete a list walk within 24 hours of starting it; an older list cursor is still accepted but is re-evaluated against the current retention boundary, so sessions whose oldest retained activity is about to age out of the retention period can be skipped.

In each session object, `user.id` is always set and survives account deletion; `user.email_address` is `null` when the user's account has been deleted or the user is no longer a member of an organization your key can read. `workspace_id` is `null` when the session was not associated with a workspace. A local session corresponds to one client session ID: starting a new conversation in the client, or clearing its context, begins a new session record. Treat `id` values as opaque strings; the format may change without notice.

Local sessions carry no `status` and no `updated_at`: a local session has no server-side lifecycle, and its visibility is governed by retention instead. A local session is captured as the series of Claude API calls (inference calls) that the client makes during the session, and retention applies to each captured call individually. `created_at` is the timestamp of the session's earliest retained call (UTC). As older calls age past the retention period, `created_at` advances accordingly, and once every call in a session has aged out, the session is no longer returned. Because `created_at` can shift between runs, deduplicate on `id` when you re-walk the list over time. A session's `created_at` does not move later as the session continues, and there is no `updated_at`, so a session that gains messages after you first export it does not reappear in a later `created_at` window. To keep transcripts current, re-list a trailing window at least as long as your longest-running sessions on each run and re-fetch the transcripts of the sessions it returns, deduplicating messages on `id`.

The list is built from session activity metadata, so it can include sessions whose transcript content was not captured, for example sessions that ran before capture began for your organization (as far back as your retention period allows); the transcript of such a session returns each message with its content marked unavailable (see [Retrieve a local session transcript](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-a-local-session-transcript)).

Captured local session content is stored for 6 years from capture by default. If the organization that ran the session has set a finite custom conversation retention period in [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls), that period applies instead, whether it is shorter or longer than the default; when the organization has more than one custom retention period configured, the shortest applies. A change to that setting takes effect in two different ways: the endpoints stop returning activity older than the organization's current period as soon as the setting changes, whereas each captured message is stored for the period that was in effect when it was captured, so lengthening the period later does not restore content that has already expired.

To fetch one session's metadata directly, pass its ID to `GET /v1/compliance/apps/sessions/local/{session_id}`. The response is the same session object the list endpoint returns, with no envelope and no transcript content. A malformed session ID returns [400 Bad Request](https://platform.claude.com/docs/en/manage-claude/compliance-errors#400-bad-request). A single [404 Not Found](https://platform.claude.com/docs/en/manage-claude/compliance-errors#404-not-found) covers four cases that the response does not distinguish: the session is not in an organization your key can read (including sessions under another parent organization), it does not exist, zero data retention is in effect for it, or every call in it has aged past retention.

`product_surface` (string or `null`) identifies the product that created the session: `cowork` for Cowork sessions running on the user's machine in Claude Desktop, and `claude_code` for Claude Code sessions. New values appear as coverage expands.

<Note>
  **Build forward-compatible handlers.** Pass through unrecognized `product_surface` values, and ignore fields your handler does not expect, so your integration keeps working as new product surfaces ship.
</Note>

### Retrieve a local session transcript

The messages endpoint returns the session's transcript, reconstructed from the captured Claude API calls: user prompts, assistant text, tool calls, and the text portions of tool results, all returned as they were sent apart from size truncation. Nothing masks URLs, credentials, or personal data in that content, so treat transcripts as sensitive. The transcript omits or replaces the following:

* Thinking blocks are never included.
* The request's system prompt is never returned. A marker message reading `[system prompt content not shown]` stands in for it (normally once per session; a session with no captured content carries no marker).
* Tool definitions and MCP server configuration are not part of the transcript.
* Images, PDFs, and other binary or structured blocks are not returned. Each appears as a `text` block reading `[<block type> content not shown]` (for example, `[image content not shown]`) with `truncated` set to `true`. Non-text items inside a tool result are replaced by one `[N non-text item(s) not shown]` entry, and the tool result block's `truncated` is `true`.
* Citation metadata on `text` blocks is omitted, and the affected block carries `truncated` set to `true`.

Project instruction files such as `CLAUDE.md` appear as ordinary user-role content. Skill content appears when the client sends it as message content and is not distinguished from other user text. For a coverage summary and a comparison with OpenTelemetry logging for Cowork and Claude Code, see the [Compliance API FAQ](https://platform.claude.com/docs/en/manage-claude/compliance-faq#data-coverage-and-retention).

```bash cURL
session_id="clls_01HxKpLmNoPqRsTuVwXyZaBc"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/local/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

```json Response
{
  "session": {
    "type": "compliance_local_session",
    "id": "clls_01HxKpLmNoPqRsTuVwXyZaBc",
    "organization_uuid": "9a1e0000-0000-0000-0000-000000000000",
    "workspace_id": "wrkspc_01SvYKoWVRVHoEbwESNvzYdR",
    "user": {
      "id": "user_01GpKpLmNoPqRsTuVwXyZaBc",
      "email_address": null
    },
    "product_surface": "cowork",
    "created_at": "2026-07-09T14:02:11Z"
  },
  "data": [
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBa",
      "role": "user",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": {
        "type": "synthetic_marker"
      },
      "content": [
        {
          "type": "text",
          "text": "[system prompt content not shown]",
          "truncated": true
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBc",
      "role": "user",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "Fix the failing test in tests/auth_test.py",
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBd",
      "role": "assistant",
      "created_at": "2026-07-09T14:02:11Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "I'll read the test file first.",
          "truncated": false
        },
        {
          "type": "tool_use",
          "id": "toolu_01AbCdEfGhIjKlMnOpQrSt",
          "name": "Read",
          "input": "{\"file_path\":\"tests/auth_test.py\"}",
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBe",
      "role": "user",
      "created_at": "2026-07-09T14:02:38Z",
      "provenance": null,
      "content": [
        {
          "type": "tool_result",
          "tool_use_id": "toolu_01AbCdEfGhIjKlMnOpQrSt",
          "name": "Read",
          "is_error": false,
          "content": [
            {
              "type": "text",
              "text": "def test_login_expiry():\n    ..."
            }
          ],
          "truncated": false
        }
      ]
    },
    {
      "type": "compliance_local_session_message",
      "id": "clsm_01J4KpLmNoPqRsTuVwXyZaBf",
      "role": "assistant",
      "created_at": "2026-07-09T14:02:38Z",
      "provenance": null,
      "content": [
        {
          "type": "text",
          "text": "The test was asserting on a stale expiry timestamp. I've updated it.",
          "truncated": false
        }
      ]
    }
  ],
  "next_page": null
}
```

The response embeds a `session` envelope alongside the paginated `data` array. The first record in this example is the marker that stands in for the request's system prompt; its `provenance` is described later in this section. On this endpoint `user.email_address` is always `null`: the messages endpoint does not resolve email addresses, so a `null` here does not mean the user's account was deleted. To attribute a session to an email address, join `user.id` against the [list endpoint](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions) or the retrieve endpoint (`GET /v1/compliance/apps/sessions/local/{session_id}`).

Messages are returned oldest first by default; pass `order=desc` to reverse. Pagination uses the same `page`/`next_page` scheme as the list endpoint, with a `limit` default of 100 and a max of 1,000. A page can end early when the response reaches its size limit, so a page with fewer than `limit` messages does not mean you have reached the end; keep paginating until `next_page` is `null`. Page cursors are bound to the session and sort order they were issued under, and a walk's cursors expire 24 hours after its first page: an expired cursor returns [400 Bad Request](https://platform.claude.com/docs/en/manage-claude/compliance-errors#400-bad-request) telling you to restart without the `page` parameter, and the restarted walk reflects the current retention boundary. A cursor issued for a different session or `order` also returns 400, as an invalid cursor.

Each message carries a `role` (`user` or `assistant`) and a `content` array of `text`, `tool_use`, and `tool_result` blocks. A `text` block carries `text` and `truncated`. A `tool_use` block carries `id`, `name`, `input`, and `truncated`, where `input` is a JSON-encoded string rather than an object. A `tool_result` block carries `tool_use_id`, `name`, `is_error`, a `content` array of `text` entries, and `truncated`. MCP tool calls and results, and most server tool calls and results, are normalized into these same `tool_use` and `tool_result` shapes; any other block type appears as a `[<block type> content not shown]` placeholder. A message `id` is stable while the turn is retained. Every message reconstructed from the same inference call carries that call's timestamp, so consecutive messages often share a `created_at` value; preserve the returned order rather than re-sorting by timestamp.

Each message also carries a `provenance` field describing how its content was captured. `provenance` is `null` for verified content captured by the Claude API, which is the common case. Otherwise it is an object whose `type` marks the exception:

* `content_unavailable` means the content cannot be returned. The `content` array is empty, and `provenance.reason` states why. `not_captured` means no content is available for the turn; it does not prove that no record was stored, because content withheld by a storage-side access policy is reported with the same reason (for example, in organizations that use [customer-managed encryption keys](https://platform.claude.com/docs/en/manage-claude/cmek#disabled-or-modified)), and individual turns within an otherwise captured session can be unavailable for other data-handling reasons and carry the same reason. `cmek_key_revoked` is reserved for content encrypted under your organization's customer-managed key when that key is unavailable (for example, revoked); it is not currently returned, so handle it for forward compatibility. `retention_elapsed` means the content aged past retention. `oversize` means a single message exceeded the per-message size bound; the message is still returned, with an empty `content` array.
* `client_asserted` marks assistant messages that the client supplied as conversation history and that could not be matched to a captured response; their authorship is not verified.
* `synthetic_marker` marks records generated by the endpoint itself, such as the marker that stands in for the system prompt. When the client rewrites or compacts its conversation history mid-session (for example, after context compaction), the transcript inserts a marker message at that point and continues with the new content the client sent; when your organization has a finite retention period, the rewritten history itself is withheld (a second marker notes this) and only the latest user turn and what follows are shown.

Marker and client-asserted messages begin with a bracketed explanatory `text` block flagged `truncated: true`, for example `[system prompt content not shown]`. Treat these records as present but unavailable or unverified rather than missing, and tolerate unrecognized `provenance` types and reasons.

Two parameters cap how many bytes of each tool block are returned: `tool_use_input_max_bytes` and `tool_result_max_bytes`, both defaulting to 10,000 bytes. Pass `-1` for the server maximum (about 1 MiB per string); `0` returns [400 Bad Request](https://platform.claude.com/docs/en/manage-claude/compliance-errors#400-bad-request), and values above the maximum are clamped to it. A string cut off by either cap is cut on a character boundary and has an in-band suffix appended (for example, `…[truncated; pass tool_result_max_bytes=-1 for the server max]`), and its block carries `"truncated": true`. A truncated `tool_use` `input` is therefore no longer valid JSON, so parse tool inputs only from untruncated blocks (or raise the cap and refetch). Blocks of type `text` are always capped at the same server maximum of about 1 MiB; no parameter raises it, and a `text` block at the bound also carries `"truncated": true`.

Transcript content honors the retention period described under [Sessions on users' machines](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions). When the start of a session has aged past it, the transcript begins with a single `content_unavailable` placeholder with `reason` of `retention_elapsed`, and the retained messages follow. When every call in a session has aged out, the messages endpoint returns [404 Not Found](https://platform.claude.com/docs/en/manage-claude/compliance-errors#404-not-found), as it does for sessions in organizations your key cannot read, sessions that do not exist, and sessions for which zero data retention is in effect. A malformed session ID returns [400 Bad Request](https://platform.claude.com/docs/en/manage-claude/compliance-errors#400-bad-request).

## Sessions in the cloud (remote sessions)

Cowork sessions started on claude.ai web or mobile run in the cloud in Anthropic-managed environments. The Compliance API exposes these remote sessions through two endpoints: `GET /v1/compliance/apps/sessions/remote` lists session metadata, and `GET /v1/compliance/apps/sessions/remote/{session_id}/messages` returns one session's transcript. Both require the `read:compliance_user_data` scope, and both count against the shared Compliance API rate limit plus a second request budget specific to these endpoints; see [429 Too Many Requests](https://platform.claude.com/docs/en/manage-claude/compliance-errors#429-too-many-requests).

The list endpoint defaults to organization-wide scope: leave off `organization_ids[]` to include every claude.ai organization your key can read, or pass up to 500 values to narrow the scope. To scope the list to specific users instead, pass 1–10 `user_ids[]` values (obtain the IDs from [List organization users](https://platform.claude.com/docs/en/manage-claude/compliance-org-data#list-organization-users)); the filter matches the session's owning user, so agent-owned sessions are excluded whenever `user_ids[]` is set. Bound the results in time with `created_at` range parameters (`gte`, `gt`, `lt`, `lte`, in RFC 3339 format). There is no `updated_at` filter. The following request lists sessions created since a given date.

```bash cURL
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
  --data-urlencode "created_at.gte=2026-06-01T00:00:00Z" \
  --data-urlencode "limit=100"
```

```json Response
{
  "data": [
    {
      "id": "cse_01WpQrStUvXyZaBcDeFgHjK6",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      },
      "agent_id": null,
      "started_by_user": null,
      "status": "active",
      "created_at": "2026-07-01T17:04:05Z",
      "updated_at": "2026-07-01T18:00:41Z",
      "product_surface": "cowork_remote",
      "claude_project_id": "claude_proj_01KGp4eZNug9ri4kE35RSppq"
    },
    {
      "id": "cse_01TkNpRsUvWxYzAbCdEfGhJ4",
      "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "user": null,
      "agent_id": "cagt_01MnPqRsTuVwXyZaBcDeFgH8",
      "started_by_user": {
        "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
        "email_address": "user@example.com"
      },
      "status": "archived",
      "created_at": "2026-06-28T09:15:22Z",
      "updated_at": "2026-06-28T09:47:10Z",
      "product_surface": "cowork_remote",
      "claude_project_id": null
    }
  ],
  "next_page": "page_AAEfMk93cXpYdGxrZXk"
}
```

Results are sorted in reverse chronological order (newest first) by `created_at` and capped at `limit` results per response (default 100, max 500). The endpoint paginates with `page` and `next_page` tokens (see [Paginate results](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed#paginate-results)): pass the response's `next_page` value back as the `page` query parameter on the next request, and stop when `next_page` is `null`.

A session is owned by either a user or an agent, never both. For user-owned sessions, `user` carries the owner's ID and email address (`email_address` is `null` when the user is no longer a member of an organization your key can read) and `agent_id` is `null`. For agent-owned sessions (for example, scheduled tasks), `user` is `null`, `agent_id` carries the agent's ID (prefix `cagt_`), and `started_by_user` identifies the human who initiated the run, for example by starting a scheduled task; on user-owned sessions, `started_by_user` is `null`.

`claude_project_id` is the ID of the claude.ai [project](https://platform.claude.com/docs/en/manage-claude/compliance-content-data#retrieve-projects-and-attachments) the session belongs to (prefix `claude_proj_`), or `null` when the session is not in a project.

`status` is one of `pending`, `active`, `paused`, `archived`, or `failed`. A session is `pending` while it is being provisioned; a `pending` session has no transcript yet, and the messages endpoint returns 404 for it until provisioning completes. Sessions that have been deleted are never returned.

`product_surface` (string or `null`) identifies the product that created the session. The endpoint currently returns only sessions with `product_surface` of `cowork_remote`: Cowork sessions started on claude.ai web or mobile.

<Note>
  **Build forward-compatible handlers.** Pass through unrecognized `status` and `product_surface` values, and ignore fields your handler does not expect, so your integration keeps working as new statuses and product surfaces ship.
</Note>

### Retrieve a remote session transcript

The messages endpoint returns the session's transcript: user prompts, assistant responses, and tool calls and results. Thinking blocks and images are not included. For a coverage summary and a comparison with Cowork's OpenTelemetry logging, see the [Compliance API FAQ](https://platform.claude.com/docs/en/manage-claude/compliance-faq#data-coverage-and-retention).

```bash cURL
session_id="cse_01WpQrStUvXyZaBcDeFgHjK6"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/apps/sessions/remote/$session_id/messages" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

```json Response
{
  "session": {
    "id": "cse_01WpQrStUvXyZaBcDeFgHjK6",
    "organization_uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
    "user": {
      "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "email_address": null
    },
    "agent_id": null,
    "started_by_user": null,
    "status": "active",
    "created_at": "2026-07-01T17:04:05Z",
    "updated_at": "2026-07-01T18:00:41Z",
    "product_surface": "cowork_remote",
    "claude_project_id": null
  },
  "data": [
    {
      "id": "csev_01HjKmNpQrStUvWxYzAbCdE2",
      "role": "user",
      "created_at": "2026-07-01T17:04:05Z",
      "content": [
        {
          "type": "text",
          "text": "Summarize the customer feedback in the attached spreadsheet.",
          "truncated": false
        }
      ],
      "sent_by_user_id": null,
      "content_unavailable": false
    },
    {
      "id": "csev_01BcDeFgHjKmNpQrStUvWxY4",
      "role": "assistant",
      "created_at": "2026-07-01T17:04:06Z",
      "content": [
        {
          "type": "text",
          "text": "I'll start by reading the spreadsheet...",
          "truncated": false
        }
      ],
      "sent_by_user_id": null,
      "content_unavailable": false
    }
  ],
  "next_page": null
}
```

The response embeds a `session` envelope alongside the paginated `data` array. On this endpoint the envelope always has `user.email_address`, `started_by_user`, and `claude_project_id` set to `null`; get those values from the list endpoint instead.

Messages are returned oldest first by default; pass `order=desc` to reverse. Pagination uses the same `page`/`next_page` scheme as the list endpoint, with a `limit` default of 100 and a max of 1,000. A page can end early when the response reaches its size limit, so a page with fewer than `limit` messages does not mean you have reached the end; keep paginating until `next_page` is `null`.

Each message carries a `role` (`user` or `assistant`) and a `content` array of `text`, `tool_use`, and `tool_result` blocks. Message `created_at` values are commit timestamps: consecutive messages can share a timestamp or slightly invert, so preserve the returned order rather than re-sorting by `created_at`. On agent-owned sessions, `sent_by_user_id` records the user who sent a given user message when one is attributable; it is `null` otherwise, including on all assistant messages. When a message's content cannot be returned at all (for example, it exceeds size bounds), the message carries `content_unavailable` set to `true`.

Two parameters cap how many bytes of each tool block are returned: `tool_use_input_max_bytes` and `tool_result_max_bytes`, both defaulting to 10,000 bytes. Pass `-1` for the server maximum (about 1 MiB per string); `0` returns [400 Bad Request](https://platform.claude.com/docs/en/manage-claude/compliance-errors#400-bad-request). A block cut off by either cap carries `"truncated": true`, and a truncated `tool_use` input is no longer valid JSON, so parse tool inputs only from untruncated blocks (or raise the cap and refetch).

The messages endpoint returns [404 Not Found](https://platform.claude.com/docs/en/manage-claude/compliance-errors#404-not-found) for `pending` sessions, sessions that do not exist or have been deleted, and sessions in organizations your key cannot read.

## Retention and deletion

The session endpoints are read-only; local and remote sessions cannot be deleted through the Compliance API. Local session transcripts are retained for 6 years by default, or your organization's custom conversation retention period when a finite one is set, as described under [Sessions on users' machines](https://platform.claude.com/docs/en/manage-claude/compliance-sessions#retrieve-local-sessions). Remote session transcripts are retained for 6 years. For how these periods sit alongside Anthropic's other retention arrangements, see [API and data retention](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention).

## Next steps

<CardGroup cols={2}>
  <Card title="Retrieve and delete chats, files, and projects" href="https://platform.claude.com/docs/en/manage-claude/compliance-content-data">
    Access claude.ai chat content, file attachments, and projects with the same Compliance Access Key.
  </Card>

  <Card title="Compliance API FAQ" href="https://platform.claude.com/docs/en/manage-claude/compliance-faq#data-coverage-and-retention">
    A coverage summary for session transcripts and a comparison with OpenTelemetry logging.
  </Card>

  <Card title="Handle Compliance API errors" href="https://platform.claude.com/docs/en/manage-claude/compliance-errors">
    Verbatim error payloads and the fix for each.
  </Card>

  <Card title="API reference" href="https://platform.claude.com/docs/en/api/compliance/apps">
    Endpoint paths, parameters, and response schemas for the Compliance API.
  </Card>
</CardGroup>
