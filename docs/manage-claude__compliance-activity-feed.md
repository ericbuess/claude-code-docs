# Query the Activity Feed

Retrieve, filter, and paginate your organization's Compliance API Activity Feed.

---

<Note>
  To enable the Compliance API, see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

<Check>
  **Required scope:** `read:compliance_activities` on the Compliance Access Key or Admin API key.

  Both Compliance Access Keys (`sk-ant-api01-...`) carrying this scope and Admin API keys (`sk-ant-admin01-...`) can call the Activity Feed. See [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access) for the conditions under which each key type carries the scope.
</Check>

The Activity Feed records every authentication, chat, file, project, administrative, and platform action that occurs in your organization, in reverse chronological order. Activities are queryable within 1 minute of occurring and are retained for 6 years.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/activities?limit=1" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

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

## Filter activities

Filter by organization, actor, activity type, or a `created_at` time window using the dotted sub-parameters `created_at.gte`, `.gt`, `.lte`, and `.lt`. See the [API reference](/docs/en/api/compliance/activities/list) for each parameter's type and accepted values.

Repeatable parameters use array-bracket query syntax: pass `activity_types[]=...`, `actor_ids[]=...`, or `organization_ids[]=...` once for each value.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --data-urlencode "activity_types[]=claude_file_uploaded" \
    --data-urlencode "activity_types[]=claude_chat_created" \
    --data-urlencode "created_at.gte=2026-04-01T00:00:00Z" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

The Activity Feed produces hundreds of distinct activity types. See [Query compliance activities](/docs/en/api/compliance/activities/list) in the API reference for the full list of values that `activity_types[]` accepts.

## Paginate results

Activities are returned newest first, with ties in `created_at` broken by activity ID, and capped at `limit` results in each response (default 100, max 5,000). See the [API reference](/docs/en/api/compliance/activities/list) for the full response schema.

The Compliance API uses two pagination schemes depending on the endpoint family:

| Endpoint family                                                                                     | Sort order        | Scheme     | Parameters                                                  |
| --------------------------------------------------------------------------------------------------- | ----------------- | ---------- | ----------------------------------------------------------- |
| Activities                                                                                          | Newest first      | Cursor     | `after_id`, `before_id` (returned as `first_id`, `last_id`) |
| Chats and chat messages                                                                             | Oldest first      | Cursor     | `after_id`, `before_id` (returned as `first_id`, `last_id`) |
| Organizations, projects, project attachments, users, roles, role permissions, groups, group members | Endpoint-specific | Page token | `page` (returned as `next_page`)                            |

Files do not paginate: they are retrieved individually by ID.

Pagination cursors and page tokens are opaque strings: pass them back unchanged. Their internal format is not stable, and parsing them will break without notice. Only one of `after_id` or `before_id` may be set in each request, and both schemes return `has_more` so you know when to stop.

To page through activities:

* Pass the response's `last_id` as `after_id` to advance to the next page in result order. With activities sorted newest first, the next page contains older entries.
* Pass `first_id` as `before_id` to return to the previous page.
* Stop when `has_more` is `false`.

The cursor parameter sets the page direction; the endpoint's sort order sets the time direction. The same `after_id` parameter reaches older activities here. Chats sort oldest first; see [Retrieve and delete chats, files, and projects](/docs/en/manage-claude/compliance-content-data) for the cursor semantics there.

<Note>
  **Cursors are safe to reuse on retry.** A cursor or page token from a successfully returned page remains valid; a request that fails (5xx, timeout, network error) does not advance your position. Retry the same request with the same cursor. Only move to the next cursor after you have stored the page it points past.
</Note>

<CodeGroup>
  ```bash cURL
  # Fetch the first page (newest activities first) and capture its trailing cursor.
  last_id=$(curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/activities?limit=2" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" | jq -er '.last_id')

  # Pass the cursor back unchanged to fetch the next (older) page.
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "limit=2" \
    --data-urlencode "after_id=${last_id}"
  ```
</CodeGroup>

A production **backfill** loop pages through older activities by driving iteration off `has_more` and `last_id`:

1. Start from your stored cursor (or omit `after_id` to start from the beginning).
2. Page through with `after_id=<last_id>` until `has_more` is `false`.
3. Persist the final `last_id` only after you've stored every page it covers.

```text
cursor = stored_cursor
loop:
  if cursor is not null:
    page = GET /v1/compliance/activities?after_id={cursor}&limit=100
  else:
    page = GET /v1/compliance/activities?limit=100
  store(page.data)
  if page.last_id is not null:
    cursor = page.last_id
  if not page.has_more: break
persist(cursor)
```

## Understand the Activity object

Every entry in `data` is an Activity with this top-level shape:

| Field               | Type            | Description                                                                                                                                                                                                                  |
| ------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                | string          | Unique identifier for the activity.                                                                                                                                                                                          |
| `created_at`        | RFC 3339 string | When the activity occurred.                                                                                                                                                                                                  |
| `organization_id`   | string or null  | Organization where the activity occurred, or `null` for events not tied to an organization (sign-in, sign-out, Compliance API calls).                                                                                        |
| `organization_uuid` | string or null  | Same scoping as `organization_id`, expressed as a UUID.                                                                                                                                                                      |
| `actor`             | Actor union     | Who or what performed the activity. See the following actor table.                                                                                                                                                           |
| `type`              | string          | The activity type, for example `claude_chat_created`.                                                                                                                                                                        |
| *additional fields* | varies          | Type-specific fields, for example `claude_chat_id` on chat events or `filename` on file events. See [Query compliance activities](/docs/en/api/compliance/activities/list) in the API reference for the per-type field list. |

The `actor` field is a discriminated union. The `type` discriminator tells you which other fields are present:

| `actor.type`                 | When it appears                                                                                                                                                                        | Key fields                                                                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `user_actor`                 | A signed-in claude.ai or Claude Console user took the action.                                                                                                                          | `email_address`, `user_id`, `ip_address`, `user_agent`                                                                                              |
| `api_actor`                  | A request called the Claude API or the Compliance API with a customer-issued API key. Compliance API calls produce this actor type for both Compliance Access Keys and Admin API keys. | `api_key_id`, `ip_address`, `user_agent`                                                                                                            |
| `admin_api_key_actor`        | An organization admin used an Admin API key to manage users, invites, workspaces, or API keys.                                                                                         | `admin_api_key_id`                                                                                                                                  |
| `unauthenticated_user_actor` | An action occurred before sign-in completed, for example `sso_login_initiated`.                                                                                                        | `unauthenticated_email_address`, `ip_address`, `user_agent`                                                                                         |
| `anthropic_actor`            | Anthropic acted on the organization, for example through internal tooling.                                                                                                             | `email_address` (always `null`; present for shape consistency with `user_actor`, since Anthropic operators are not represented by individual email) |
| `scim_directory_sync_actor`  | An identity provider (such as Okta, Microsoft Entra ID, or JumpCloud) pushed a change through SCIM directory sync.                                                                     | `workos_event_id`, `directory_id`, `idp_connection_type` (nullable; for example `OktaSCIMV2`, `AzureSCIMV2`)                                        |

<Note>
  **Build forward-compatible handlers.** Pass through unrecognized `type` and `actor.type` values, and ignore fields your handler does not expect, so your integration keeps working when new activity types ship.
</Note>

## Next steps

<CardGroup cols={2}>
  <Card title="API reference" href="/docs/en/api/compliance/activities/list">
    The full request and response schema for `GET /v1/compliance/activities`, including every supported `activity_types[]` value.
  </Card>

  <Card title="Retrieve and delete chats, files, and projects" href="/docs/en/manage-claude/compliance-content-data">
    Query and delete the underlying content for activities you find in the feed (Compliance Access Key required).
  </Card>

  <Card title="Design your compliance integration" href="/docs/en/manage-claude/compliance-integration-patterns">
    Choose a polling or batch consumption pattern and plan SIEM correlation.
  </Card>

  <Card title="Handle Compliance API errors" href="/docs/en/manage-claude/compliance-errors">
    The full error catalog.
  </Card>
</CardGroup>
