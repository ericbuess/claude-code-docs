---
title: User management
url: https://platform.claude.com/docs/en/manage-claude/user-management
description: "Manage the people in your Claude Enterprise organization with the Admin API: list members and change roles, send and withdraw invites, manage groups, and read custom roles."
---

This page covers managing the people in your **Claude Enterprise** (claude.ai) organization programmatically, using the [Admin API](https://platform.claude.com/docs/en/api/admin): list members and look them up by email address, change a member's role, remove members, send and withdraw invites, manage your enterprise's groups and their membership, and read your organization's custom roles. For Claude Console (Claude Platform) organizations, see the [Admin API guide for Claude Console](https://platform.claude.com/docs/en/manage-claude/admin-api).

<Note>
  **The endpoints on this page are generally available for Claude Enterprise organizations.** The [beta header](https://platform.claude.com/docs/en/api/beta-headers) `anthropic-beta: ce-user-management-2026-07-13` is no longer required on group and custom-role requests; requests that still send it are accepted and behave identically.
</Note>

## Which endpoints can your organization use?

The Admin API is a single set of endpoints under `https://api.anthropic.com/v1/organizations/`. Claude Console and Claude Enterprise organizations authenticate with [different keys](https://platform.claude.com/docs/en/manage-claude/admin-api-keys) and each have access to a different subset of the endpoints:

| Endpoints                                                                                                                                                                                                                                                                                                                                                                                                                                                 | Claude Console (Claude Platform)                                                                  | Claude Enterprise (claude.ai)    |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- | -------------------------------- |
| [Members](https://platform.claude.com/docs/en/manage-claude/user-management#members) and [invites](https://platform.claude.com/docs/en/manage-claude/user-management#invites)                                                                                                                                                                                                                                                                             | Available; see the [Admin API guide](https://platform.claude.com/docs/en/manage-claude/admin-api) | Available (this page)            |
| [Groups](https://platform.claude.com/docs/en/manage-claude/user-management#groups)                                                                                                                                                                                                                                                                                                                                                                        | Not available                                                                                     | Available (this page)            |
| [Custom roles](https://platform.claude.com/docs/en/manage-claude/user-management#custom-roles)                                                                                                                                                                                                                                                                                                                                                            | Not available                                                                                     | Available, read-only (this page) |
| [Spend limits](https://platform.claude.com/docs/en/manage-claude/spend-limits-api)                                                                                                                                                                                                                                                                                                                                                                        | Not available                                                                                     | Available                        |
| [Workspaces](https://platform.claude.com/docs/en/manage-claude/workspaces), [API keys](https://platform.claude.com/docs/en/manage-claude/admin-api#api-keys), [usage and cost reports](https://platform.claude.com/docs/en/manage-claude/usage-cost-api), [rate limits](https://platform.claude.com/docs/en/manage-claude/rate-limits-api), and the other endpoints in the [Admin API guide](https://platform.claude.com/docs/en/manage-claude/admin-api) | Available                                                                                         | Not available                    |

Members and invites are the same endpoints for both organization types; this page documents their Claude Enterprise behavior, including the Claude Enterprise [organization roles](https://platform.claude.com/docs/en/manage-claude/user-management#organization-roles). The group and custom-role endpoints exist only for Claude Enterprise.

<Check>
  **Scoped Admin API key required**

  These endpoints require an Admin API key with the `read:members` scope (member and invite `GET` endpoints, and all custom-role endpoints; there is no separate role scope), the `write:members` scope (member and invite `POST` and `DELETE` endpoints), the `read:rbac_groups` scope (group `GET` endpoints), or the `write:rbac_groups` scope (group `POST` and `DELETE` endpoints). A key carrying the `read:org_audit` scope (a read-only scope for security-audit integrations) can also call every `GET` endpoint on this page and the [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api) read endpoints. See [Create an Admin API key](https://platform.claude.com/docs/en/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) for where your primary owner creates one and which scopes to select. Pass the key in the `x-api-key` header on every request. Member and invite requests also require the `anthropic-version: 2023-06-01` header, as shown in the examples; group and custom-role requests do not.
</Check>

## Overview

This page covers five resources:

| Resource          | Endpoints                                                                                                                                                                                                                 | Use for                                                                                                    |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Members**       | `GET /v1/organizations/users` `GET /v1/organizations/users/{user_id}` `POST /v1/organizations/users/{user_id}` `DELETE /v1/organizations/users/{user_id}`                                                                 | List the organization's members or look one up by email; change a member's role; remove a member.          |
| **Invites**       | `POST /v1/organizations/invites` `GET /v1/organizations/invites` `GET /v1/organizations/invites/{invite_id}` `DELETE /v1/organizations/invites/{invite_id}`                                                               | Invite a person to the organization, track the invitation's status, and withdraw it before it is accepted. |
| **Groups**        | `GET /v1/organizations/rbac_groups` `GET /v1/organizations/rbac_groups/{group_id}` `POST /v1/organizations/rbac_groups` `POST /v1/organizations/rbac_groups/{group_id}` `DELETE /v1/organizations/rbac_groups/{group_id}` | Read your enterprise's groups and the custom roles attached to each; create, rename, and delete groups.    |
| **Group members** | `GET /v1/organizations/rbac_groups/{group_id}/members` `POST /v1/organizations/rbac_groups/{group_id}/members` `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`                                        | Read a group's members; add and remove members.                                                            |
| **Custom roles**  | `GET /v1/organizations/rbac_roles` `GET /v1/organizations/rbac_roles/{role_id}` `GET /v1/organizations/rbac_roles/{role_id}/permissions`                                                                                  | Read your organization's custom roles and the permissions each role grants.                                |

Custom roles and their group attachments are managed in [claude.ai organization settings](https://claude.ai/admin-settings); the API reads them but cannot change them.

## Quick start

List the organization's members, newest first:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

```json
{
  "data": [
    {
      "type": "user",
      "id": "user_01AbCdEfGhIjKlMnOpQrSt",
      "email": "jane@example.com",
      "name": "Jane Smith",
      "role": "user",
      "added_at": "2026-06-12T09:14:03Z"
    }
  ],
  "has_more": false,
  "first_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "last_id": "user_01AbCdEfGhIjKlMnOpQrSt"
}
```

## Key concepts

### Organization roles

Every member has exactly one organization role. Reads return the member's role as one of five values:

| Role               | Meaning                                                                                   |
| ------------------ | ----------------------------------------------------------------------------------------- |
| `user`             | A standard member.                                                                        |
| `managed`          | A member whose permissions are granted through the custom roles attached to their groups. |
| `owner`            | An organization owner.                                                                    |
| `membership_admin` | A member who can manage the organization's members.                                       |
| `primary_owner`    | The organization's primary owner. There is exactly one.                                   |

The API can assign only the `user` and `managed` roles, on invite creation and on role updates. The administrative roles (`owner`, `membership_admin`, and `primary_owner`) are assigned in claude.ai organization settings, and members holding them cannot be modified or removed through this API.

### Members and invites

A person becomes a member by accepting an invite (or through your organization's single sign-on, where configured). Creating an invite sends an invitation email; the invite then reads as `pending` until the recipient accepts (`accepted`) or its server-assigned `expires_at` passes (`expired`). Only a `pending` invite can be withdrawn. To change a pending invitation's email address or role, withdraw it and create a new one.

If your organization's plan draws members from a finite pool of purchased seats, a pending invite consumes a seat. The create-invite endpoint does not take a seat or tier parameter: the seat is assigned automatically from the lowest tier that has availability. Creating an invite when no seat is free fails with a 400 error rather than purchasing a seat. Withdrawing the invite, letting it expire, or removing the member later returns the seat to the pool.

### Groups and roles

Groups connect members to custom roles (role-based access control, the `rbac` in the endpoint paths and scope names). Groups are owned by your enterprise as a whole (the parent organization together with every organization under it) rather than by a single organization, so the group scopes (`read:rbac_groups` and `write:rbac_groups`) require a key created for all linked organizations. Each group carries a `source_type`: `direct` for groups created in claude.ai, `scim` for groups provisioned by your identity provider. A group's `roles` field lists the IDs of the custom roles attached to it; resolve them to names and permissions with the [custom role endpoints](https://platform.claude.com/docs/en/manage-claude/user-management#custom-roles), noting that the role catalog is per-organization while groups are enterprise-wide, so fetching a role that belongs to a different organization of your enterprise returns 404 for your key. The field is `null` (rather than `[]`) when role data was temporarily unavailable, so retry to distinguish a degraded read from a group with no roles.

## Rate limits

Admin API endpoints share a per-organization limit of **100 requests per minute**; invite creation has its own limit of **1,200 requests per hour** instead. Requests over a limit return **429 Too Many Requests**.

## Pagination

Member and invite lists use ID-based pagination: pass `limit` (default 20, max 1000) plus at most one of `before_id` or `after_id`, and page using the `first_id` and `last_id` fields of each response until `has_more` is `false`. Group and custom-role lists use an **opaque cursor** instead: the response's `next_page` value is passed unchanged as the `page` parameter on the next request, until `next_page` is `null`.

## Error responses

Error responses follow the standard shape documented in [Errors](https://platform.claude.com/docs/en/api/errors).

## Members

### List members

`GET /v1/organizations/users` returns the organization's members, most recently added first. Filter by `email` to look up a specific member; the match is case-insensitive and tolerates common variants of the same address (for example, `jane+hiring@example.com` matches `jane@example.com`). Requires the `read:members` scope.

For complete parameter details and response schemas, see [List users](https://platform.claude.com/docs/en/api/admin/users/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users?email=jane@example.com" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Get a member

`GET /v1/organizations/users/{user_id}` returns one member by ID. Requires the `read:members` scope.

For complete parameter details and response schemas, see [Get user](https://platform.claude.com/docs/en/api/admin/users/retrieve) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Change a member's role

`POST /v1/organizations/users/{user_id}` sets the member's role to `user` or `managed`. Members holding an administrative role (`owner`, `membership_admin`, or `primary_owner`) cannot be changed through this endpoint, and administrative roles cannot be assigned; both return 400 and are managed in claude.ai organization settings. If your organization's identity provider manages roles (advanced SSO or advanced SCIM provisioning), role updates return 400. Requires the `write:members` scope.

For complete parameter details and response schemas, see [Update user](https://platform.claude.com/docs/en/api/admin/users/update) in the API reference.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{"role": "managed"}'
```

### Remove a member

`DELETE /v1/organizations/users/{user_id}` removes the member from the organization, returning any purchased seat they occupied to the organization's pool. Members holding an administrative role cannot be removed through this endpoint, and if your identity provider manages membership (SCIM), removals return 400. Requires the `write:members` scope.

For complete parameter details and response schemas, see [Remove user](https://platform.claude.com/docs/en/api/admin/users/delete) in the API reference.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/users/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

```json
{
  "type": "user_deleted",
  "id": "user_01AbCdEfGhIjKlMnOpQrSt"
}
```

## Invites

### Create an invite

`POST /v1/organizations/invites` sends an invitation email and returns the invite with a server-assigned `expires_at`. `role` must be `user` or `managed`. If a pending invite already exists for the email address, or the address already belongs to a member, the request returns 400 naming the existing resource. Organizations whose identity provider provisions users automatically (JIT or SCIM) cannot create invites through the API. Requires the `write:members` scope.

On plans that draw members from a finite seat pool, the invite automatically takes a seat from the lowest tier that has availability; the API does not take a tier parameter. If no seat is free, the request fails with a 400 error rather than purchasing a seat. Add seats through the organization's plan management and retry.

The optional `rbac_group_ids` field lists groups (by `rbac_group_`-prefixed ID) to assign to the member when they accept. Passing a non-empty `rbac_group_ids` additionally requires the key to carry the `write:rbac_groups` scope, because group assignment can grant the permissions attached to the group's roles.

For complete parameter details and response schemas, see [Create invite](https://platform.claude.com/docs/en/api/admin/invites/create) in the API reference.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/invites" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "email": "newhire@example.com",
    "role": "managed",
    "rbac_group_ids": ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
  }'
```

```json
{
  "type": "invite",
  "id": "invite_01QrStUvWxYzAbCdEfGhIj",
  "email": "newhire@example.com",
  "role": "managed",
  "invited_at": "2026-07-06T16:20:11Z",
  "expires_at": "2026-07-27T16:20:11Z",
  "accepted_at": null,
  "status": "pending",
  "rbac_group_ids": ["rbac_group_01UvWxYzAbCdEfGhIjKlMn"]
}
```

### List invites

`GET /v1/organizations/invites` returns the organization's invites, most recent first, across the `pending`, `accepted`, and `expired` states; there is no status filter. Requires the `read:members` scope.

For complete parameter details and response schemas, see [List invites](https://platform.claude.com/docs/en/api/admin/invites/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/invites?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Get an invite

`GET /v1/organizations/invites/{invite_id}` returns one invite by ID. Requires the `read:members` scope.

For complete parameter details and response schemas, see [Get invite](https://platform.claude.com/docs/en/api/admin/invites/retrieve) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

### Withdraw an invite

`DELETE /v1/organizations/invites/{invite_id}` withdraws a `pending` invite, deactivating the link in the invitation email. Withdrawing an `accepted` invite returns 400 (remove the member instead); withdrawing an `expired` invite returns 400. Requires the `write:members` scope.

For complete parameter details and response schemas, see [Delete invite](https://platform.claude.com/docs/en/api/admin/invites/delete) in the API reference.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/invites/invite_01QrStUvWxYzAbCdEfGhIj" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -H "anthropic-version: 2023-06-01"
```

## Groups

Groups your enterprise creates directly, in [claude.ai organization settings](https://claude.ai/admin-settings) or through this API (`source_type: "direct"`), support every endpoint in this section. Groups provisioned by your identity provider (`source_type: "scim"`) can be read but not modified: renaming or deleting a SCIM group, or changing its membership, returns 400, because your identity provider owns it. Unlike member and invite requests, group requests do not require the `anthropic-version` header.

### List groups

`GET /v1/organizations/rbac_groups` returns your enterprise's groups, including identity-provider-managed (`scim`) groups. Requires the `read:rbac_groups` scope.

For complete parameter details and response schemas, see [List groups](https://platform.claude.com/docs/en/api/admin/rbac_groups/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_group",
      "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      "name": "Engineering",
      "source_type": "direct",
      "roles": ["rbac_role_01CdEfGhIjKlMnOpQrStUv"],
      "created_at": "2026-03-18T10:01:42Z",
      "updated_at": "2026-05-02T08:55:09Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Get a group

`GET /v1/organizations/rbac_groups/{group_id}` returns one group by ID. Requires the `read:rbac_groups` scope.

For complete parameter details and response schemas, see [Get group](https://platform.claude.com/docs/en/api/admin/rbac_groups/retrieve) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Create a group

`POST /v1/organizations/rbac_groups` creates a group with the given `name` (1–255 characters) and no roles or members. Requires the `write:rbac_groups` scope.

For complete parameter details and response schemas, see [Create group](https://platform.claude.com/docs/en/api/admin/rbac_groups/create) in the API reference.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -d '{"name": "Engineering"}'
```

```json
{
  "type": "rbac_group",
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "name": "Engineering",
  "source_type": "direct",
  "roles": [],
  "created_at": "2026-07-09T18:00:00Z",
  "updated_at": "2026-07-09T18:00:00Z"
}
```

### Rename a group

`POST /v1/organizations/rbac_groups/{group_id}` updates the group. `name` is the only field this endpoint can change. Requires the `write:rbac_groups` scope.

For complete parameter details and response schemas, see [Update group](https://platform.claude.com/docs/en/api/admin/rbac_groups/update) in the API reference.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -d '{"name": "Platform Engineering"}'
```

### Delete a group

`DELETE /v1/organizations/rbac_groups/{group_id}` deletes the group. Its members remain members of their organizations, but they lose the permissions of its attached roles, and a group [spend limit](https://platform.claude.com/docs/en/manage-claude/spend-limits-api), if one existed, stops applying to them. Requires the `write:rbac_groups` scope.

For complete parameter details and response schemas, see [Delete group](https://platform.claude.com/docs/en/api/admin/rbac_groups/delete) in the API reference.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "type": "rbac_group_deleted"
}
```

### List a group's members

`GET /v1/organizations/rbac_groups/{group_id}/members` returns the group's members (each with their `user_id` and email), oldest first. Only current members of your enterprise's organizations are returned, so a page might contain fewer than `limit` entries while `has_more` is `true`. Requires the `read:rbac_groups` scope.

For complete parameter details and response schemas, see [List group members](https://platform.claude.com/docs/en/api/admin/rbac_groups/members/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members?limit=100" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_group_member",
      "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
      "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
      "email": "jane@example.com",
      "created_at": "2026-04-07T12:30:00Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Add a member to a group

`POST /v1/organizations/rbac_groups/{group_id}/members` adds an organization member to the group by `user_id`. The user must already be a member of one of your enterprise's organizations (the request returns 404 otherwise), and adding someone who is already in the group returns 400. For `scim` groups, membership is managed in your identity provider and this request returns 400. To assign groups to a person who has not joined yet, use `rbac_group_ids` on [invite creation](https://platform.claude.com/docs/en/manage-claude/user-management#create-an-invite) instead. Requires the `write:rbac_groups` scope.

For complete parameter details and response schemas, see [Add group member](https://platform.claude.com/docs/en/api/admin/rbac_groups/members/create) in the API reference.

```bash cURL
curl -X POST "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members" \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  -d '{"user_id": "user_01AbCdEfGhIjKlMnOpQrSt"}'
```

```json
{
  "type": "rbac_group_member",
  "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "email": "jane@example.com",
  "created_at": "2026-07-09T18:00:00Z"
}
```

### Remove a member from a group

`DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}` removes the member from the group; they remain a member of their organization. The request returns 404 if the user is not a member of the group, and 400 for `scim` groups, whose membership is managed in your identity provider. Requires the `write:rbac_groups` scope.

For complete parameter details and response schemas, see [Remove group member](https://platform.claude.com/docs/en/api/admin/rbac_groups/members/delete) in the API reference.

```bash cURL
curl -X DELETE "https://api.anthropic.com/v1/organizations/rbac_groups/rbac_group_01UvWxYzAbCdEfGhIjKlMn/members/user_01AbCdEfGhIjKlMnOpQrSt" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "group_id": "rbac_group_01UvWxYzAbCdEfGhIjKlMn",
  "user_id": "user_01AbCdEfGhIjKlMnOpQrSt",
  "type": "rbac_group_member_deleted"
}
```

## Custom roles

Custom roles are read-only through the API: these endpoints catalog your organization's custom roles (defined in [claude.ai organization settings](https://claude.ai/admin-settings) or provisioned by Anthropic) and the permissions each role grants. Custom-role reads use the `read:members` scope (there is no separate role scope) and work with an organization-level key: unlike the group endpoints, they do not require a key created for all linked organizations, and the catalog returned is your organization's own.

### List roles

`GET /v1/organizations/rbac_roles` returns your organization's custom roles. Requires the `read:members` scope.

For complete parameter details and response schemas, see [List roles](https://platform.claude.com/docs/en/api/admin/rbac_roles/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_role",
      "id": "rbac_role_01CdEfGhIjKlMnOpQrStUv",
      "name": "Engineering base",
      "created_at": "2026-03-18T10:01:42Z",
      "updated_at": "2026-05-02T08:55:09Z"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

### Get a role

`GET /v1/organizations/rbac_roles/{role_id}` returns one role by ID. Requires the `read:members` scope.

For complete parameter details and response schemas, see [Get role](https://platform.claude.com/docs/en/api/admin/rbac_roles/retrieve) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### List a role's permissions

`GET /v1/organizations/rbac_roles/{role_id}/permissions` returns the role's permissions. Each permission pairs a `resource` (what it applies to: the organization's product features, a connector tool, a connector OAuth scope, one connector, or every connector) with an `action` (what it grants on that resource). Rows for features not enabled for your organization are omitted, so a page might contain fewer than `limit` rows while `has_more` is `true`. Requires the `read:members` scope.

Two `action` values need special care: an `organization` permission whose action is `capability_access_all` (every product feature) or `capability_access_all_ga` (every generally available product feature) is a blanket grant (one that covers neither model access nor the `permission_`-prefixed admin-panel permissions) and is listed as that single row rather than expanded. When you tally what a role grants, treat a blanket row as covering everything its variant describes, not just the features named in other rows.

For complete parameter details and response schemas, see [List role permissions](https://platform.claude.com/docs/en/api/admin/rbac_roles/permissions/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/rbac_roles/rbac_role_01CdEfGhIjKlMnOpQrStUv/permissions?limit=20" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "type": "rbac_role_permission",
      "resource": {
        "type": "organization",
        "organization_id": "12345678-1234-5678-1234-567812345678"
      },
      "action": "capability_access_all_ga"
    },
    {
      "type": "rbac_role_permission",
      "resource": {
        "type": "connector_tool",
        "connector_id": "mcpsrv_01WxYzAbCdEfGhIjKlMnOp",
        "tool_name": "search_tickets"
      },
      "action": "use"
    }
  ],
  "has_more": false,
  "next_page": null
}
```

## Example workflows

### Offboard a departing employee

1. Look up the member by email:

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/users?email=departing@example.com" \
     -H "x-api-key: $ANTHROPIC_ADMIN_KEY" \
     -H "anthropic-version: 2023-06-01"
   ```

2. Remove them with `DELETE /v1/organizations/users/{user_id}`, using the `id` from the response. Their seat, if any, returns to the pool.

3. If the person had not yet joined, the lookup returns no member; list invites and withdraw their `pending` invite instead.

### Audit group membership

1. List groups and record each group's `id`, `name`, and `roles`.

2. For each group that carries sensitive roles, page through `GET /v1/organizations/rbac_groups/{group_id}/members` and compare the member emails against your identity provider's roster.

3. Remove members who should no longer be in the group with `DELETE /v1/organizations/rbac_groups/{group_id}/members/{user_id}`. For `scim` groups, make the change in your identity provider instead.

## Frequently asked questions

### Is this a different API from the Admin API?

No. The member and invite endpoints are the same `/v1/organizations/` endpoints that Claude Console organizations use; this page documents their Claude Enterprise behavior. The group and custom-role endpoints are part of the same API and exist only for Claude Enterprise organizations. The [availability table](https://platform.claude.com/docs/en/manage-claude/user-management#which-endpoints-can-your-organization-use) shows which endpoints each organization type can call.

### Can I assign the owner or membership admin role through the API?

No. The API assigns only `user` and `managed`, on invite creation and role updates. Administrative roles are assigned in claude.ai organization settings, and members holding them cannot be modified or removed through the API.

### Can I create or modify groups through the API?

Yes, with the `write:rbac_groups` scope: create, rename, and delete groups, and add or remove their members. Two things the API cannot change: groups provisioned by your identity provider (`source_type: "scim"`), whose name and membership are owned by the identity provider, and custom roles, which are managed in claude.ai organization settings (the API [reads them](https://platform.claude.com/docs/en/manage-claude/user-management#custom-roles)).

### Does an unaccepted invite consume a seat?

On plans with a finite seat pool, yes: a `pending` invite holds a seat. Withdrawing the invite or letting it expire frees the seat. On plans without a seat pool, invites consume nothing.

### My organization uses single sign-on. Which operations work?

If your identity provider provisions users automatically (JIT or SCIM), invite creation returns 400. If it manages roles (advanced SSO or advanced SCIM provisioning), role updates return 400. If it manages membership (SCIM provisioning), member removals return 400. Reads work regardless.

### What happens to an Admin API key when the person who created it leaves?

The key keeps working. Admin API keys are scoped to the organization, not to individual users, and a key created in claude.ai does not expire. Removing the creator from the organization or deprovisioning them through your identity provider ends their own access, but not the keys they created. Downgrading their role does not change the keys either: each key stays active with its original scopes. When you offboard someone who created Admin API keys, delete those keys in the **Keys** section of [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) and create replacements.

## See also

<CardGroup cols={2}>
  <Card title="Create an Admin API key" href="https://platform.claude.com/docs/en/manage-claude/admin-api-keys">
    Where your primary owner creates a scoped key and which scopes to select.
  </Card>

  <Card title="Compliance API" href="https://platform.claude.com/docs/en/manage-claude/compliance-api">
    Audit activity and retrieve or delete user content across your organization.
  </Card>

  <Card title="Analytics APIs" href="https://platform.claude.com/docs/en/manage-claude/analytics-api">
    Per-user and time-bucketed usage and cost reporting for Claude Enterprise.
  </Card>

  <Card title="Spend Limits API" href="https://platform.claude.com/docs/en/manage-claude/spend-limits-api">
    Set per-member spend limits and review increase requests.
  </Card>
</CardGroup>
