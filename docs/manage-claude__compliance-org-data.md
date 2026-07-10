# List organizations, users, roles, groups, and settings

Enumerate organizations under your parent organization (their users, roles, and groups) and read each organization's effective settings through the Compliance API.

---

<Note>
  To enable the Compliance API, see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

<Check>
  **Required scope:** `read:compliance_org_data` on the Compliance Access Key. The user and group-member endpoints require `read:compliance_user_data` instead.

  Compliance Access Keys (`sk-ant-api01-...`) created in claude.ai are the only key type accepted; see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access) to provision one. Calls authenticated with an Admin API key (`sk-ant-admin01-...`) return [403 Forbidden](/docs/en/manage-claude/compliance-errors#403-forbidden).
</Check>

The endpoints on this page expose the directory side of a Claude Enterprise organization: its linked organizations, the users in each one, the roles defined on each, and its role-based access control (RBAC) or SCIM (System for Cross-domain Identity Management)-provisioned groups and their members. Use them to seed eDiscovery user lists, build reporting dashboards, and reconcile group membership against an external system of record. A Compliance Access Key that covers the parent organization returns data from every linked organization underneath, so a single key reaches the entire tree. The [effective-settings endpoint](#get-effective-organization-settings) complements the directory: it returns the data-privacy, security, and capability settings actually in force for one organization.

## List organizations

The [List organizations](/docs/en/api/compliance/organizations/list) endpoint returns every organization under the parent the key is bound to.

The following call lists every organization under your parent. The response is a `data` array of organization records sorted by `created_at` ascending, plus `has_more` and `next_page` for pagination. When `has_more` is `true`, pass the returned `next_page` token back unchanged as the `page` query parameter on your next request. See [List organizations](/docs/en/api/compliance/organizations/list) in the API reference for the `limit` and `page` parameter defaults and ranges.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/organizations" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "uuid": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
      "name": "Acme Engineering",
      "created_at": "2025-06-01T10:00:00Z"
    },
    {
      "uuid": "5a1b2c3d-4e5f-6789-abcd-ef0123456789",
      "name": "Acme Legal",
      "created_at": "2025-07-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

The `uuid` field is the canonical identifier for downstream lookups. The following table maps it to the other organization identifiers across the Compliance API:

| Field                | Where                                                                                                                                                                                              | Relationship to `uuid`                                                                                                                                    |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `{org_uuid}`         | Path parameter on per-organization endpoints on this page                                                                                                                                          | Same value                                                                                                                                                |
| `organization_uuid`  | Activity Feed, chat, and project records                                                                                                                                                           | Same value; join on these two fields directly                                                                                                             |
| `organization_id`    | Activity Feed, chat, and project records                                                                                                                                                           | Same organization, `org_`-prefixed. Deprecated on chat and project records; use `organization_uuid` instead.                                              |
| `organization_ids[]` | Filter on [Query the Activity Feed](/docs/en/manage-claude/compliance-activity-feed) and [Retrieve chats and messages](/docs/en/manage-claude/compliance-content-data#retrieve-chats-and-messages) | Accepts `uuid` or the `org_`-prefixed form                                                                                                                |
| `organization_id`    | [Get effective organization settings](#get-effective-organization-settings) response                                                                                                               | Same value, bare UUID; this response does **not** use the `org_`-prefixed form that `organization_id` carries on Activity Feed, chat, and project records |

Most other Anthropic APIs use the `org_`-prefixed form.

To track organization-membership changes over time, relist this endpoint periodically, following the `next_page` token through every page on each pass. The Activity Feed also surfaces membership events through the `org_deletion_requested`, `org_deleted_via_bulk`, `org_parent_join_proposal_created`, and `org_join_proposal_decided` activity types; see [Query the Activity Feed](/docs/en/manage-claude/compliance-activity-feed).

## List organization users

The [List organization users](/docs/en/api/compliance/organizations/users/list) endpoint returns a paginated list of user records for one organization.

This endpoint requires `read:compliance_user_data`, not `read:compliance_org_data`. Create the Compliance Access Key with both scopes when you intend to use it for directory enumeration; otherwise the call returns [403 Forbidden](/docs/en/manage-claude/compliance-errors#403-forbidden).

See [List organization users](/docs/en/api/compliance/organizations/users/list) in the API reference for the `limit` and `page` query parameter defaults and ranges.

Results are sorted by organization join date ascending. Unlike the Activity Feed's `before_id`/`after_id` cursors (see [Paginate results](/docs/en/manage-claude/compliance-activity-feed#paginate-results)), the directory endpoints paginate with a `next_page` token: when `has_more` is `true`, pass `next_page` back unchanged as the `page` query parameter on the next request.

<CodeGroup>
  ```bash cURL
  org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/users" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "limit=500"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "full_name": "Priya Sharma",
      "email": "priya@example.com",
      "organization_role": "admin",
      "created_at": "2025-06-01T10:00:00Z"
    }
  ],
  "has_more": true,
  "next_page": "page_8aW5kZXgicG9zaXRpb25fdG9rZW5fOTE0"
}
```

The user IDs returned here are the same `user_...` identifiers accepted by the [Query the Activity Feed](/docs/en/manage-claude/compliance-activity-feed) `actor_ids[]` filter and the [Retrieve chats and messages](/docs/en/manage-claude/compliance-content-data#retrieve-chats-and-messages) `user_ids[]` filter. The `organization_role` field carries the user's built-in membership level within the listed organization (one of `admin`, `billing`, `claude_code_user`, `developer`, `managed`, `membership_admin`, `owner`, `primary_owner`, or `user`), an axis independent of any custom RBAC role assignments returned by [List roles](#list-roles). A typical eDiscovery flow lists users for one or more organizations, filters against your own external records, and feeds the resulting IDs into chat and project queries.

A user only appears here while they are an active member of the organization. Removed users are dropped from the list immediately. Their historical activity remains queryable through the Activity Feed for the full retention window, indexed by the same `user_...` ID.

## List roles

The [List Compliance Roles](/docs/en/api/compliance/organizations/roles/list) endpoint returns a paginated list of role records defined on one organization, and [Get Compliance Role](/docs/en/api/compliance/organizations/roles/retrieve) returns one role by ID.

Both role endpoints require `read:compliance_org_data`. The list endpoint accepts the same `limit` and `page` parameters as [List organization users](#list-organization-users).

<CodeGroup>
  ```bash cURL
  org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

  curl --fail-with-body -sS \
    "https://api.anthropic.com/v1/compliance/organizations/${org_uuid}/roles" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "rbac_role_01N2pQrS8tUvWxYz5AbCdEfGh",
      "name": "Compliance Reviewer",
      "description": "Read-only access to chat and project content for legal review.",
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-06-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

See the [List Compliance Roles](/docs/en/api/compliance/organizations/roles/list) response schema for the full role record shape. To list the permissions currently granted to a role, use [List Compliance Role Permissions](/docs/en/api/compliance/organizations/roles/permissions/list). To audit historical role assignments and permission changes, query the RBAC activity types (for example, `rbac_role_assigned` and `rbac_role_permission_added`) through the Activity Feed; see [Filter activities](/docs/en/manage-claude/compliance-activity-feed#filter-activities).

## List groups and members

The [List Compliance Groups](/docs/en/api/compliance/groups/list) endpoint returns a paginated list of RBAC and SCIM-provisioned groups, and [Get Compliance Group](/docs/en/api/compliance/groups/retrieve) returns one group by ID. The [List Compliance Group Members](/docs/en/api/compliance/groups/members/list) endpoint returns the members of one group.

The group list and retrieval endpoints require `read:compliance_org_data`. The members endpoint requires `read:compliance_user_data`. Create the key with both scopes to walk groups end to end. Both list endpoints accept the same `limit` and `page` parameters as [List organization users](#list-organization-users).

See the [List Compliance Groups](/docs/en/api/compliance/groups/list) response schema for the full group record shape. The `roles` array lists role IDs assigned to the group, matching IDs from [List roles](#list-roles). `source_type` is the discriminator between groups created manually through claude.ai (`direct`) and groups synced from an external identity provider through SCIM (`scim`).

List groups, then for each group list its members:

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/groups" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "id": "rbac_group_01P9qRsTuVwXyZa2BcDeFgHjK",
      "name": "Engineering",
      "description": "Engineering team members",
      "source_type": "scim",
      "roles": ["rbac_role_01N2pQrS8tUvWxYz5AbCdEfGh"],
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-06-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

For each group ID, list its members:

<CodeGroup>
  ```bash cURL
  group_id="rbac_group_01P9qRsTuVwXyZa2BcDeFgHjK"

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/groups/$group_id/members" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
  ```
</CodeGroup>

```json Response
{
  "data": [
    {
      "user_id": "user_01XyDMpzjS89pFZXqSFUBDr6",
      "email": "priya@example.com",
      "created_at": "2025-06-01T10:00:00Z",
      "updated_at": "2025-06-15T14:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

See the [List Compliance Group Members](/docs/en/api/compliance/groups/members/list) response schema for the full member record shape. The `user_id` field is the same `user_...` identifier the Activity Feed and chat list accept. To get a member's full name, look it up through the organization users list.

## Get effective organization settings

The [Get effective organization settings](/docs/en/api/compliance/organizations/settings/retrieve) endpoint returns the settings in force for one organization under your parent: the enforced state after regulatory restrictions (such as HIPAA), feature-availability rules, organization-type defaults, and inter-feature dependencies are applied, which can differ from what an administrator configured. Use it to attest that retention windows, content redaction, single sign-on enforcement, the IP allowlist, and session-duration controls match your documented baseline, without administrator Console access.

This endpoint requires `read:compliance_org_data`; a key without that scope returns [403 Forbidden](/docs/en/manage-claude/compliance-errors#403-forbidden). The target must be one of the parent's linked organizations: the parent organization itself is not a valid target. An unknown organization, an organization ID that is not a valid UUID, an organization outside your parent's tree, and a parent organization that does not yet have access to this endpoint all return the same [404 Not Found](/docs/en/manage-claude/compliance-errors#404-not-found), so a 404 does not reveal whether an organization exists. The settings endpoint is enabled per parent organization separately from the rest of the Compliance API; if every request returns 404, contact your Anthropic representative.

<Note>
  Before June 30, 2026, this endpoint required the separate `read:compliance_org_settings` scope. That scope has been retired: it can no longer be selected or granted when creating a key, and a key that carries only the retired scope returns [403 Forbidden](/docs/en/manage-claude/compliance-errors#403-forbidden) — create a new Compliance Access Key with `read:compliance_org_data` instead.
</Note>

```bash cURL
org_uuid="91012d09-e48b-438e-a489-1bebfd8fa6f9"

curl --fail-with-body -sS \
  "https://api.anthropic.com/v1/compliance/organizations/$org_uuid/settings" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

The response is a list of typed setting rows, and which rows appear varies by organization: a setting the organization's administrators cannot change, because it is controlled by Anthropic policy or not available to the organization, is omitted from the list. Treat a missing row as "not controllable by this organization's administrators", not as "off". The following abridged example shows three of the rows a response can contain:

```json Response
{
  "type": "effective_organization_settings",
  "organization_id": "91012d09-e48b-438e-a489-1bebfd8fa6f9",
  "settings": [
    {
      "name": "data_retention_periods",
      "type": "data_retention",
      "value": {
        "chat": {
          "type": "fixed",
          "timescale": "day",
          "duration": 90
        }
      }
    },
    {
      "name": "content_redaction_enabled",
      "type": "boolean",
      "value": true
    },
    {
      "name": "ip_allowlist_ip_ranges",
      "type": "string_list",
      "value": ["10.0.0.0/8", "203.0.113.0/24"]
    }
  ],
  "api_keys": [
    {
      "type": "compliance_api_key",
      "id": "apikey_01Hx7k2mP9nQ4rS6tU8vW0xY",
      "name": "Compliance Export Key",
      "scopes": ["read:compliance_activities", "read:compliance_org_data"],
      "is_active": true,
      "created_at": "2026-03-14T09:30:00Z",
      "created_by_id": "user_01Jz3a4bC5dE6fG7hI8jK9lM",
      "expires_at": null
    }
  ]
}
```

Each row carries `name`, `type`, and `value`; the `type` field (`boolean`, `integer`, `string_list`, `provisioning_mode`, or `data_retention`) tells you the shape of `value`. The full list of setting names, and the `value` schema for each type, is in [Get effective organization settings](/docs/en/api/compliance/organizations/settings/retrieve) in the API reference.

The `api_keys` array lists every Compliance Access Key configured for your parent organization, so the same list is returned regardless of which linked organization you query. Each entry carries the key's `type` (`compliance_api_key`), `id`, `name`, `scopes`, `is_active` flag, `created_at` and `expires_at` timestamps, and `created_by_id` (the ID of the user who created the key; may be `null`). The key's secret value is never returned. Deactivated keys are included with `is_active: false` so you can review keys that previously had access, and keys that carry only the retired `read:compliance_org_settings` scope remain in the list for audit and cleanup visibility even though that scope no longer grants access.

The top-level `organization_id` is the organization's bare UUID: the same value as `uuid` in the organizations list, not the `org_`-prefixed form that `organization_id` carries on Activity Feed, chat, and project records (see the identifier table in [List organizations](#list-organizations)).

Rows reflect the enforced state rather than the last-stored configuration: for example, `sso_provisioning_mode` reports a configured SCIM mode only while directory sync is enabled, `ip_allowlist_enabled` is `true` only while the allowlist is on and has at least one active range, and `code_execution_network_egress_enabled` is `false` whenever code execution is off.

The response reflects the state at read time; nothing is snapshotted. Changes to most of these settings surface as events in the [Activity Feed](/docs/en/manage-claude/compliance-activity-feed); use this endpoint for the current resolved state and the feed to audit who changed what, and when.

## Next steps

<CardGroup cols={2}>
  <Card title="Compliance organizations API reference" href="/docs/en/api/compliance/organizations">
    The full request and response schema for every organization, user, role, group, and settings endpoint.
  </Card>

  <Card title="Handle Compliance API errors" href="/docs/en/manage-claude/compliance-errors">
    Verbatim error payloads and the fix for each.
  </Card>
</CardGroup>
