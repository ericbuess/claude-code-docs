# Handle Compliance API errors

Every Compliance API error message with cause and fix, organized by HTTP status code.

---

<Note>
  To enable the Compliance API, see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

This page lists the response messages each documented Compliance API endpoint returns, the cause, and the fix.

The Compliance API returns errors in an error format consistent with the rest of the [Anthropic error format](/docs/en/api/errors): a non-2xx status code, a `request-id` response header, and a JSON body with an `error` object containing `type` and `message`. Include the `request-id` header value when you escalate to support.

```json
{
  "error": {
    "type": "authentication_error",
    "message": "The API key provided is invalid or has been revoked."
  }
}
```

Match on `error.type`, not on the message string. Messages are stable enough to copy into runbooks but might be reworded over time; the type values are part of the API contract.

The following table tells you at a glance whether to retry. Each section that follows shows the verbatim error body and the fix.

| Status                                                  | Retry?                      | When                                                                                                                           |
| ------------------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [400 Bad Request](#400-bad-request)                     | No                          | Fix the request and resend.                                                                                                    |
| [401 Unauthorized](#401-unauthorized)                   | No                          | Fix or rotate the key, then resend.                                                                                            |
| [403 Forbidden](#403-forbidden)                         | No                          | Add the missing scope or use the right key type, then resend.                                                                  |
| [404 Not Found](#404-not-found)                         | No                          | The resource was deleted or never existed; remove it from your queue.                                                          |
| [409 Conflict](#409-conflict)                           | No                          | The request conflicts with the resource's current state; resolve the conflict (such as detaching child resources), then retry. |
| [429 Too Many Requests](#429-too-many-requests)         | Yes, after `retry-after`    | Wait the seconds in `retry-after`, then retry; do not advance your cursor.                                                     |
| [500 Internal Server Error](#500-internal-server-error) | Depends on `x-should-retry` | Check the `x-should-retry` response header before retrying.                                                                    |
| [502, 503, 504, 529](#500-internal-server-error)        | Yes, with backoff           | Transient; retry with exponential backoff.                                                                                     |

## 400 Bad Request

The request was syntactically valid but contained a parameter the server rejected. Fix the parameter and retry.

### Invalid timestamp format

**Type:** `invalid_request_error`

```text wrap
The `created_at.gte` parameter contains an invalid timestamp format. Timestamps must be provided in RFC 3339 format e.g., "2024-03-01T00:00:00Z". Got "2024-01-01".
```

**Cause:** A `created_at.*` or `updated_at.*` value (`.gte`, `.gt`, `.lte`, `.lt`) could not be parsed as a datetime. The message names the parameter that failed and echoes the value that was sent.

**Fix:** Send a full RFC 3339 timestamp including time and time zone, for example, `2024-03-01T00:00:00Z` or `2024-03-01T00:00:00+00:00`.

### Invalid limit

**Type:** `invalid_request_error`

```text wrap
The limit parameter must be between 1 and 1000, inclusive. Got 1500.
```

**Cause:** The `limit` query parameter was outside the accepted range. The bound named in the message reflects the maximum for the specific endpoint that was called.

**Fix:** Send a `limit` within the range the endpoint accepts. Each list endpoint has its own `limit` range; see the parameter constraints on the corresponding [Compliance API reference](/docs/en/api/compliance) page.

### Invalid pagination ID

**Type:** `invalid_request_error`

```text wrap
Invalid `after_id`. No activity found for `after_id` "activity_invalid123"
```

**Cause:** The `after_id` or `before_id` cursor could not be decoded as an opaque cursor or parsed as an activity ID.

**Fix:** Treat pagination cursors as opaque strings. Always copy the `first_id` or `last_id` value returned by the previous page; stop when `has_more` is `false`. Do not construct cursors from object IDs.

The directory and project endpoints (organizations, users, roles, role permissions, groups, group members, projects, and project attachments) paginate with an opaque `page` token rather than `after_id` and `before_id`. The same advice applies: pass the `next_page` value from the previous response unchanged, and stop when `has_more` is `false`. A malformed `page` token returns the same 400 `invalid_request_error` as a malformed `after_id` or `before_id`.

## 401 Unauthorized

The `x-api-key` header was missing or did not match a known key. A valid key with the wrong scopes returns [403 Forbidden](#403-forbidden) instead.

### Invalid API key

**Type:** `authentication_error`

```text wrap
The API key provided is invalid or has been revoked.
```

**Cause:** The key in `x-api-key` does not exist, has been deleted, or has been disabled. A missing or empty `x-api-key` header returns the same body, so check both your secret store and the key's revocation status.

**Fix:** Confirm the key value, check that it has not been deleted in claude.ai (Compliance Access Keys) or Claude Console (Admin API keys), and confirm it is enabled. See [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).

## 403 Forbidden

The key in `x-api-key` is valid but does not carry the scope the endpoint requires. The verbatim message lists the scopes the key carries (`Got:`) and the scopes the endpoint requires (`Needed:`), so you can confirm what the key carries without rechecking Claude Console or claude.ai. Compliance Access Key scopes are immutable after creation, so each insufficient-scope fix directs you to create a new key rather than edit the existing one.

### Insufficient scope: Activity Feed

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['read:compliance_activities']
```

**Cause:** A key without `read:compliance_activities` was used to call `GET /v1/compliance/activities`. There are two common paths to this error:

* A Compliance Access Key (`sk-ant-api01-...`) was created without the `read:compliance_activities` scope.
* A Claude Console Admin API key (`sk-ant-admin01-...`) was created before the Compliance API was enabled for the organization. Keys created before enablement do not carry the scope; see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api).

**Fix:** Compliance Access Key scopes are immutable after creation. Create a new key that includes `read:compliance_activities`, or use a Claude Console Admin API key. See [Which key do you need?](/docs/en/manage-claude/compliance-api-access#which-key-do-you-need) for the conditions under which an Admin API key carries this scope.

### Insufficient scope: organization data

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['read:compliance_org_data']
```

**Cause:** A key without `read:compliance_org_data` was used to call an organizations, roles, groups, or effective-settings endpoint. There are two common paths to this error:

* A Compliance Access Key (`sk-ant-api01-...`) was created without the `read:compliance_org_data` scope.
* A Claude Console Admin API key (`sk-ant-admin01-...`) was used. Admin API keys carry only `read:compliance_activities` and cannot read organization metadata.

**Fix:** [Create a new Compliance Access Key](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) with `read:compliance_org_data` selected. Admin API keys cannot read organization metadata; the Compliance Access Key is required.

### Retired scope: organization settings

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_org_settings'] Needed: ['read:compliance_org_data']
```

**Cause:** The `read:compliance_org_settings` scope was retired on June 30, 2026. `GET /v1/compliance/organizations/{organization_id}/settings` now requires `read:compliance_org_data`, the same scope as the other organization endpoints, and the retired scope no longer authorizes anything. A Compliance Access Key that carries only `read:compliance_org_settings` returns this error on every call to the settings endpoint, even though the key worked before the retirement. The retired scope can no longer be selected or granted when creating a key.

**Fix:** Compliance Access Key scopes are immutable after creation. [Create a new Compliance Access Key](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) with `read:compliance_org_data` selected, update your integration to use it, then delete the old key. A key that already carries `read:compliance_org_data` is unaffected by the retirement.

### Insufficient scope: user data

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']
```

**Cause:** A key without `read:compliance_user_data` was used to call a chats, messages, files, projects, organization users, or group-members endpoint. There are two common paths to this error:

* A Compliance Access Key (`sk-ant-api01-...`) was created without the `read:compliance_user_data` scope.
* A Claude Console Admin API key (`sk-ant-admin01-...`) was used. Admin API keys carry only `read:compliance_activities` and cannot be granted `read:compliance_user_data`, so they cannot call the chat, file, project, project attachment, user, or group-member endpoints.

**Fix:** Use a [Compliance Access Key](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) created in claude.ai with `read:compliance_user_data` selected. If the request really should be Activity Feed only, point the Admin API key at `GET /v1/compliance/activities` instead.

### Insufficient scope: delete

**Type:** `permission_error`

```text wrap
Missing required scopes. Got: ['read:compliance_user_data'] Needed: ['delete:compliance_user_data']
```

**Cause:** A Compliance Access Key without `delete:compliance_user_data` was used to call a `DELETE` endpoint on chats, files, or projects.

**Fix:** [Create a new Compliance Access Key](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) with `delete:compliance_user_data` selected. The delete scope is separate from `read:compliance_user_data` so that read-only audit keys cannot delete content.

## 404 Not Found

The endpoint resolved but the resource ID does not exist or has already been deleted. Compliance API deletes are immediate and permanent, so a 404 on a previously known ID usually means the content was hard-deleted through a Compliance API delete call or removed by a retention policy. The activity-type strings cited in each Fix (for example, `claude_chat_created`) are values you can pass to the Activity Feed `activity_types[]` filter; see [Query compliance activities](/docs/en/api/compliance/activities/list) for every supported value.

### Chat not found

**Type:** `not_found_error`

```text wrap
Chat claude_chat_01H5CWunD7RpVJ5bHa8RCkja not found.
```

**Cause:** The chat ID in the path does not match a chat readable through the Compliance API. The chat might have been hard-deleted through a previous Compliance API call or removed by your organization's retention policy, or it might belong to an organization the calling key cannot read. Chats that a user soft-deleted in claude.ai do not return 404; they remain readable with `deleted_at` populated.

**Fix:** Confirm the chat ID against a recent `claude_chat_created` or `claude_chat_viewed` activity. If the activity is recent and the read still fails, the chat has been hard-deleted (through this API or by retention-policy expiry) or belongs to an organization outside your key's scope.

### File not found

**Type:** `not_found_error`

```text wrap
No file found with provided id, or it has already been deleted.
```

**Cause:** The file ID does not exist or has been deleted. This error applies to both chat-attached files (`claude_file_...`) and project files.

**Fix:** Reconcile against recent `claude_file_uploaded` or `claude_file_deleted` activities. If the file was deleted, the binary is gone; the activity record remains in the feed for the 6-year retention window.

### Project not found

**Type:** `not_found_error`

```text wrap
No project is found with the provided id.
```

**Cause:** The project ID does not exist or has been deleted.

**Fix:** Reconcile against recent `claude_project_created` or `claude_project_deleted` activities. The Activity Feed continues to expose the project's lifecycle events even after the project itself is gone.

### Project document not found

**Type:** `not_found_error`

```text wrap
No project document found with provided id, or it has already been deleted.
```

**Cause:** The project document ID does not exist or has been deleted. This error applies to text project documents (`claude_proj_doc_...`), not to project files.

**Fix:** Use `GET /v1/compliance/apps/projects/{project_id}/attachments` to list current attachments. If the document is missing, it was deleted; retrieve it through a `claude_project_document_uploaded` activity record if you only need the metadata.

### Organization, role, or group not found

**Type:** `not_found_error`

```text wrap
The "ce86b5f3-7c16-48b3-a9f3-e1d2c4b8a0f1" organization does not exist or the requester is not authorized to access it.
```

The organization, role, and group endpoints return a 404 `not_found_error` in the standard error format. The organization message names the `org_uuid`; the role and group messages are generic (`Role not found.`, `Group not found.`). This occurs when a path ID (`org_uuid`, `role_id`, or `group_id`) does not exist or no longer belongs to a tree the calling key can read.

**Cause:** The ID in the path does not match a record readable through the Compliance API. Roles and groups can be deleted, and organizations can be unlinked from the parent tree.

**Fix:** Verify the ID against the corresponding list endpoint, and reconcile against recent organization, role, or group activities in the [Activity Feed](/docs/en/manage-claude/compliance-activity-feed).

### Organization settings not available

**Type:** `not_found_error`

```text wrap
organization `91012d09-e48b-438e-a489-1bebfd8fa6f9` not found in this organization's hierarchy
```

**Cause:** `GET /v1/compliance/organizations/{organization_id}/settings` returns this 404 in three cases that intentionally share the same body so the response does not reveal whether an organization exists: the `organization_id` is not one of your parent's linked organizations, the value is not a valid UUID, or the settings endpoint is not yet enabled for your parent organization.

**Fix:** Verify the ID against [List organizations](/docs/en/api/compliance/organizations/list). If a known-good organization ID still returns 404, the settings endpoint is not yet enabled for your parent organization; contact your Anthropic representative.

## 409 Conflict

The request is well-formed and authorized but conflicts with the resource's current state.

### Project has attached chats

**Type:** `conflict_error`

```text wrap
The "claude_proj_01KGp4eZNug9ri4kE35RSppq" project cannot be deleted as it has chats attached to it. Delete or detach all chats, and try deleting the project again.
```

**Cause:** `DELETE /v1/compliance/apps/projects/{project_id}` was called on a project that still has chats attached.

**Fix:** List the project's chats with `GET /v1/compliance/apps/chats?user_ids[]={user_id}&project_ids[]={project_id}` (the `project_ids[]` filter requires at least one `user_ids[]` value; enumerate IDs through [List organization users](/docs/en/manage-claude/compliance-org-data#list-organization-users)), delete each one with `DELETE /v1/compliance/apps/chats/{claude_chat_id}`, and then retry the project delete.

## 429 Too Many Requests

Requests to the Compliance API are limited to **600 requests per minute per [parent organization](/docs/en/manage-claude/compliance-api#how-the-compliance-api-works)**. The limit is a single budget shared across every key under the parent (Compliance Access Keys and the Admin API keys of all linked organizations) and across every `/v1/compliance/*` endpoint. Contact your Anthropic representative if your integration needs a higher limit.

Once your API key authenticates, every Compliance API response includes the standard [rate-limit response headers](/docs/en/api/rate-limits#response-headers) so your client can throttle proactively instead of waiting for a 429:

* `anthropic-ratelimit-requests-limit` is your parent organization's per-minute request budget.
* `anthropic-ratelimit-requests-remaining` is the budget left in the current window.
* `anthropic-ratelimit-requests-reset` is the RFC 3339 timestamp when the window resets and the full budget is restored.

A 429 response also carries a `retry-after` header with the number of seconds to wait before sending the next request. This value might include a small safety margin beyond `anthropic-ratelimit-requests-reset`; honor `retry-after`.

```http
HTTP/1.1 429 Too Many Requests
date: Tue, 21 Apr 2026 14:38:02 GMT
retry-after: 25
anthropic-ratelimit-requests-limit: 600
anthropic-ratelimit-requests-remaining: 0
anthropic-ratelimit-requests-reset: 2026-04-21T14:38:25Z
```

```json
{
  "error": {
    "type": "rate_limit_error",
    "message": "Compliance API rate limit of 600 requests per minute per parent organization has been exceeded. Retry after the time indicated by the retry-after header. Quote the request-id response header when contacting Anthropic support."
  }
}
```

**Cause:** Your parent organization sent more than 600 requests to `/v1/compliance/*` in a 1-minute window, across all of its keys and linked organizations.

**Fix:** Wait the number of seconds in the `retry-after` header, then retry. If the header is absent (for example, stripped by an intermediary), fall back to exponential backoff (start at 1 second, double up to 60 seconds). Do not advance your pagination cursor on a 429: the failed request returned no data, so the cursor from the last successful page is still correct.

Requests that fail authentication (a missing or unrecognized key, or a Claude API key rather than a Compliance Access Key or Admin API key) reject before the rate limiter and do not consume quota. A valid key that lacks the endpoint's required scope consumes one quota unit before the 403 is returned.

If you poll the [Activity Feed](/docs/en/manage-claude/compliance-activity-feed) on a schedule, budget your aggregate request rate (across all keys, linked organizations, and concurrent workers) below the parent-organization limit. Watch `anthropic-ratelimit-requests-remaining` to slow down before you reach it. See [Design your compliance integration](/docs/en/manage-claude/compliance-integration-patterns#choose-a-feed-consumption-pattern) for choosing between window-polling and cursor-driven ingestion.

## 500 Internal Server Error

A 500 from the Compliance API carries an `x-should-retry: false` response header when the failure is deterministic. Anthropic SDKs honor this header automatically. If you use a generic HTTP retry library that retries on every 5xx, suppress retries when `x-should-retry` is `false`; retrying this error fails identically on every attempt.

A 500 without the `x-should-retry: false` header is transient: retry with exponential backoff (start at 1 second, double up to 60 seconds). The same applies to 502, 503, 504, and 529 responses. See [Errors](/docs/en/api/errors) for the platform-wide retry semantics.

For service-wide incidents, check [status.anthropic.com](https://status.anthropic.com).

## Next steps

<CardGroup cols={2}>
  <Card title="Compliance API FAQ" href="/docs/en/manage-claude/compliance-faq">
    Common questions about access, scopes, retention, and integration.
  </Card>

  <Card title="Errors" href="/docs/en/api/errors">
    The platform-wide error catalog and retry semantics.
  </Card>
</CardGroup>
