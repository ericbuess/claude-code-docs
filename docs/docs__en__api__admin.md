# Admin

# Organizations

## Me

**get** `/v1/organizations/me`

Retrieve information about the organization associated with the authenticated API key.

### Returns

- `Organization = object { id, name, type }`

  - `id: string`

    ID of the Organization.

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    - `"organization"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/me \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### Organization

- `Organization = object { id, name, type }`

  - `id: string`

    ID of the Organization.

  - `name: string`

    Name of the Organization.

  - `type: "organization"`

    Object type.

    For Organizations, this is always `"organization"`.

    - `"organization"`

# Invites

## Create

**post** `/v1/organizations/invites`

Create Invite

### Body Parameters

- `email: string`

  Email of the User.

- `role: "user" or "developer" or "billing" or "claude_code_user"`

  Role for the invited User. Cannot be "admin".

  - `"user"`

  - `"developer"`

  - `"billing"`

  - `"claude_code_user"`

### Returns

- `Invite = object { id, email, expires_at, 4 more }`

  - `id: string`

    ID of the Invite.

  - `email: string`

    Email of the User being invited.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the Invite expires.

  - `invited_at: string`

    RFC 3339 datetime string indicating when the Invite was created.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `status: "accepted" or "expired" or "deleted" or "pending"`

    Status of the Invite.

    - `"accepted"`

    - `"expired"`

    - `"deleted"`

    - `"pending"`

  - `type: "invite"`

    Object type.

    For Invites, this is always `"invite"`.

    - `"invite"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/invites \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{
          "email": "user@emaildomain.com",
          "role": "user"
        }'
```

## Retrieve

**get** `/v1/organizations/invites/{invite_id}`

Get Invite

### Path Parameters

- `invite_id: string`

  ID of the Invite.

### Returns

- `Invite = object { id, email, expires_at, 4 more }`

  - `id: string`

    ID of the Invite.

  - `email: string`

    Email of the User being invited.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the Invite expires.

  - `invited_at: string`

    RFC 3339 datetime string indicating when the Invite was created.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `status: "accepted" or "expired" or "deleted" or "pending"`

    Status of the Invite.

    - `"accepted"`

    - `"expired"`

    - `"deleted"`

    - `"pending"`

  - `type: "invite"`

    Object type.

    For Invites, this is always `"invite"`.

    - `"invite"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/invites/$INVITE_ID \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## List

**get** `/v1/organizations/invites`

List Invites

### Query Parameters

- `after_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: optional number`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `data: array of Invite`

  - `id: string`

    ID of the Invite.

  - `email: string`

    Email of the User being invited.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the Invite expires.

  - `invited_at: string`

    RFC 3339 datetime string indicating when the Invite was created.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `status: "accepted" or "expired" or "deleted" or "pending"`

    Status of the Invite.

    - `"accepted"`

    - `"expired"`

    - `"deleted"`

    - `"pending"`

  - `type: "invite"`

    Object type.

    For Invites, this is always `"invite"`.

    - `"invite"`

- `first_id: string`

  First ID in the `data` list. Can be used as the `before_id` for the previous page.

- `has_more: boolean`

  Indicates if there are more results in the requested page direction.

- `last_id: string`

  Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```http
curl https://api.anthropic.com/v1/organizations/invites \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Delete

**delete** `/v1/organizations/invites/{invite_id}`

Delete Invite

### Path Parameters

- `invite_id: string`

  ID of the Invite.

### Returns

- `id: string`

  ID of the Invite.

- `type: "invite_deleted"`

  Deleted object type.

  For Invites, this is always `"invite_deleted"`.

  - `"invite_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/invites/$INVITE_ID \
    -X DELETE \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### Invite

- `Invite = object { id, email, expires_at, 4 more }`

  - `id: string`

    ID of the Invite.

  - `email: string`

    Email of the User being invited.

  - `expires_at: string`

    RFC 3339 datetime string indicating when the Invite expires.

  - `invited_at: string`

    RFC 3339 datetime string indicating when the Invite was created.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `status: "accepted" or "expired" or "deleted" or "pending"`

    Status of the Invite.

    - `"accepted"`

    - `"expired"`

    - `"deleted"`

    - `"pending"`

  - `type: "invite"`

    Object type.

    For Invites, this is always `"invite"`.

    - `"invite"`

# Users

## Retrieve

**get** `/v1/organizations/users/{user_id}`

Get User

### Path Parameters

- `user_id: string`

  ID of the User.

### Returns

- `User = object { id, added_at, email, 3 more }`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## List

**get** `/v1/organizations/users`

List Users

### Query Parameters

- `after_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `email: optional string`

  Filter by user email.

- `limit: optional number`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `data: array of User`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`

- `first_id: string`

  First ID in the `data` list. Can be used as the `before_id` for the previous page.

- `has_more: boolean`

  Indicates if there are more results in the requested page direction.

- `last_id: string`

  Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```http
curl https://api.anthropic.com/v1/organizations/users \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Update

**post** `/v1/organizations/users/{user_id}`

Update User

### Path Parameters

- `user_id: string`

  ID of the User.

### Body Parameters

- `role: "user" or "developer" or "billing" or "claude_code_user"`

  New role for the User. Cannot be "admin".

  - `"user"`

  - `"developer"`

  - `"billing"`

  - `"claude_code_user"`

### Returns

- `User = object { id, added_at, email, 3 more }`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{
          "role": "user"
        }'
```

## Delete

**delete** `/v1/organizations/users/{user_id}`

Remove User

### Path Parameters

- `user_id: string`

  ID of the User.

### Returns

- `id: string`

  ID of the User.

- `type: "user_deleted"`

  Deleted object type.

  For Users, this is always `"user_deleted"`.

  - `"user_deleted"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/users/$USER_ID \
    -X DELETE \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### User

- `User = object { id, added_at, email, 3 more }`

  - `id: string`

    ID of the User.

  - `added_at: string`

    RFC 3339 datetime string indicating when the User joined the Organization.

  - `email: string`

    Email of the User.

  - `name: string`

    Name of the User.

  - `role: "user" or "developer" or "billing" or 2 more`

    Organization role of the User.

    - `"user"`

    - `"developer"`

    - `"billing"`

    - `"admin"`

    - `"claude_code_user"`

  - `type: "user"`

    Object type.

    For Users, this is always `"user"`.

    - `"user"`

# Workspaces

## Create

**post** `/v1/organizations/workspaces`

Create Workspace

### Body Parameters

- `name: string`

  Name of the Workspace.

### Returns

- `Workspace = object { id, archived_at, created_at, 3 more }`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or null if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{
          "name": "x"
        }'
```

## Retrieve

**get** `/v1/organizations/workspaces/{workspace_id}`

Get Workspace

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Returns

- `Workspace = object { id, archived_at, created_at, 3 more }`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or null if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## List

**get** `/v1/organizations/workspaces`

List Workspaces

### Query Parameters

- `after_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `include_archived: optional boolean`

  Whether to include Workspaces that have been archived in the response

- `limit: optional number`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `data: array of Workspace`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or null if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`

- `first_id: string`

  First ID in the `data` list. Can be used as the `before_id` for the previous page.

- `has_more: boolean`

  Indicates if there are more results in the requested page direction.

- `last_id: string`

  Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Update

**post** `/v1/organizations/workspaces/{workspace_id}`

Update Workspace

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Body Parameters

- `name: string`

  Name of the Workspace.

### Returns

- `Workspace = object { id, archived_at, created_at, 3 more }`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or null if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{
          "name": "x"
        }'
```

## Archive

**post** `/v1/organizations/workspaces/{workspace_id}/archive`

Archive Workspace

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Returns

- `Workspace = object { id, archived_at, created_at, 3 more }`

  - `id: string`

    ID of the Workspace.

  - `archived_at: string`

    RFC 3339 datetime string indicating when the Workspace was archived, or null if the Workspace is not archived.

  - `created_at: string`

    RFC 3339 datetime string indicating when the Workspace was created.

  - `display_color: string`

    Hex color code representing the Workspace in the Anthropic Console.

  - `name: string`

    Name of the Workspace.

  - `type: "workspace"`

    Object type.

    For Workspaces, this is always `"workspace"`.

    - `"workspace"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/archive \
    -X POST \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

# Members

## Create

**post** `/v1/organizations/workspaces/{workspace_id}/members`

Create Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Body Parameters

- `user_id: string`

  ID of the User.

- `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin"`

  Role of the new Workspace Member. Cannot be "workspace_billing".

  - `"workspace_user"`

  - `"workspace_developer"`

  - `"workspace_admin"`

### Returns

- `WorkspaceMember = object { type, user_id, workspace_id, workspace_role }`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    - `"workspace_member"`

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

    Role of the Workspace Member.

    - `"workspace_user"`

    - `"workspace_developer"`

    - `"workspace_admin"`

    - `"workspace_billing"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{
          "user_id": "user_01WCz1FkmYMm4gnmykNKUu3Q",
          "workspace_role": "workspace_user"
        }'
```

## Retrieve

**get** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Get Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

### Returns

- `WorkspaceMember = object { type, user_id, workspace_id, workspace_role }`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    - `"workspace_member"`

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

    Role of the Workspace Member.

    - `"workspace_user"`

    - `"workspace_developer"`

    - `"workspace_admin"`

    - `"workspace_billing"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members/$USER_ID \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## List

**get** `/v1/organizations/workspaces/{workspace_id}/members`

List Workspace Members

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

### Query Parameters

- `after_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `limit: optional number`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

### Returns

- `data: array of WorkspaceMember`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    - `"workspace_member"`

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

    Role of the Workspace Member.

    - `"workspace_user"`

    - `"workspace_developer"`

    - `"workspace_admin"`

    - `"workspace_billing"`

- `first_id: string`

  First ID in the `data` list. Can be used as the `before_id` for the previous page.

- `has_more: boolean`

  Indicates if there are more results in the requested page direction.

- `last_id: string`

  Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Update

**post** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Update Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

### Body Parameters

- `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

  New workspace role for the User.

  - `"workspace_user"`

  - `"workspace_developer"`

  - `"workspace_admin"`

  - `"workspace_billing"`

### Returns

- `WorkspaceMember = object { type, user_id, workspace_id, workspace_role }`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    - `"workspace_member"`

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

    Role of the Workspace Member.

    - `"workspace_user"`

    - `"workspace_developer"`

    - `"workspace_admin"`

    - `"workspace_billing"`

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members/$USER_ID \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{
          "workspace_role": "workspace_user"
        }'
```

## Delete

**delete** `/v1/organizations/workspaces/{workspace_id}/members/{user_id}`

Delete Workspace Member

### Path Parameters

- `workspace_id: string`

  ID of the Workspace.

- `user_id: string`

  ID of the User.

### Returns

- `type: "workspace_member_deleted"`

  Deleted object type.

  For Workspace Members, this is always `"workspace_member_deleted"`.

  - `"workspace_member_deleted"`

- `user_id: string`

  ID of the User.

- `workspace_id: string`

  ID of the Workspace.

### Example

```http
curl https://api.anthropic.com/v1/organizations/workspaces/$WORKSPACE_ID/members/$USER_ID \
    -X DELETE \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### Workspace Member

- `WorkspaceMember = object { type, user_id, workspace_id, workspace_role }`

  - `type: "workspace_member"`

    Object type.

    For Workspace Members, this is always `"workspace_member"`.

    - `"workspace_member"`

  - `user_id: string`

    ID of the User.

  - `workspace_id: string`

    ID of the Workspace.

  - `workspace_role: "workspace_user" or "workspace_developer" or "workspace_admin" or "workspace_billing"`

    Role of the Workspace Member.

    - `"workspace_user"`

    - `"workspace_developer"`

    - `"workspace_admin"`

    - `"workspace_billing"`

# API Keys

## Retrieve

**get** `/v1/organizations/api_keys/{api_key_id}`

Get Api Key

### Path Parameters

- `api_key_id: string`

  ID of the API key.

### Returns

- `APIKey = object { id, created_at, created_by, 5 more }`

  - `id: string`

    ID of the API key.

  - `created_at: string`

    RFC 3339 datetime string indicating when the API Key was created.

  - `created_by: object { id, type }`

    The ID and type of the actor that created the API key.

    - `id: string`

      ID of the actor that created the object.

    - `type: string`

      Type of the actor that created the object.

  - `name: string`

    Name of the API key.

  - `partial_key_hint: string`

    Partially redacted hint for the API key.

  - `status: "active" or "inactive" or "archived"`

    Status of the API key.

    - `"active"`

    - `"inactive"`

    - `"archived"`

  - `type: "api_key"`

    Object type.

    For API Keys, this is always `"api_key"`.

    - `"api_key"`

  - `workspace_id: string`

    ID of the Workspace associated with the API key, or null if the API key belongs to the default Workspace.

### Example

```http
curl https://api.anthropic.com/v1/organizations/api_keys/$API_KEY_ID \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## List

**get** `/v1/organizations/api_keys`

List Api Keys

### Query Parameters

- `after_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately after this object.

- `before_id: optional string`

  ID of the object to use as a cursor for pagination. When provided, returns the page of results immediately before this object.

- `created_by_user_id: optional string`

  Filter by the ID of the User who created the object.

- `limit: optional number`

  Number of items to return per page.

  Defaults to `20`. Ranges from `1` to `1000`.

- `status: optional "active" or "inactive" or "archived"`

  Filter by API key status.

  - `"active"`

  - `"inactive"`

  - `"archived"`

- `workspace_id: optional string`

  Filter by Workspace ID.

### Returns

- `data: array of APIKey`

  - `id: string`

    ID of the API key.

  - `created_at: string`

    RFC 3339 datetime string indicating when the API Key was created.

  - `created_by: object { id, type }`

    The ID and type of the actor that created the API key.

    - `id: string`

      ID of the actor that created the object.

    - `type: string`

      Type of the actor that created the object.

  - `name: string`

    Name of the API key.

  - `partial_key_hint: string`

    Partially redacted hint for the API key.

  - `status: "active" or "inactive" or "archived"`

    Status of the API key.

    - `"active"`

    - `"inactive"`

    - `"archived"`

  - `type: "api_key"`

    Object type.

    For API Keys, this is always `"api_key"`.

    - `"api_key"`

  - `workspace_id: string`

    ID of the Workspace associated with the API key, or null if the API key belongs to the default Workspace.

- `first_id: string`

  First ID in the `data` list. Can be used as the `before_id` for the previous page.

- `has_more: boolean`

  Indicates if there are more results in the requested page direction.

- `last_id: string`

  Last ID in the `data` list. Can be used as the `after_id` for the next page.

### Example

```http
curl https://api.anthropic.com/v1/organizations/api_keys \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Update

**post** `/v1/organizations/api_keys/{api_key_id}`

Update Api Key

### Path Parameters

- `api_key_id: string`

  ID of the API key.

### Body Parameters

- `name: optional string`

  Name of the API key.

- `status: optional "active" or "inactive" or "archived"`

  Status of the API key.

  - `"active"`

  - `"inactive"`

  - `"archived"`

### Returns

- `APIKey = object { id, created_at, created_by, 5 more }`

  - `id: string`

    ID of the API key.

  - `created_at: string`

    RFC 3339 datetime string indicating when the API Key was created.

  - `created_by: object { id, type }`

    The ID and type of the actor that created the API key.

    - `id: string`

      ID of the actor that created the object.

    - `type: string`

      Type of the actor that created the object.

  - `name: string`

    Name of the API key.

  - `partial_key_hint: string`

    Partially redacted hint for the API key.

  - `status: "active" or "inactive" or "archived"`

    Status of the API key.

    - `"active"`

    - `"inactive"`

    - `"archived"`

  - `type: "api_key"`

    Object type.

    For API Keys, this is always `"api_key"`.

    - `"api_key"`

  - `workspace_id: string`

    ID of the Workspace associated with the API key, or null if the API key belongs to the default Workspace.

### Example

```http
curl https://api.anthropic.com/v1/organizations/api_keys/$API_KEY_ID \
    -H 'Content-Type: application/json' \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY" \
    -d '{}'
```

# Usage Report

## Retrieve Messages

**get** `/v1/organizations/usage_report/messages`

Get Messages Usage Report

### Query Parameters

- `starting_at: string`

  Time buckets that start on or after this RFC 3339 timestamp will be returned.
  Each time bucket will be snapped to the start of the minute/hour/day in UTC.

- `api_key_ids: optional array of string`

  Restrict usage returned to the specified API key ID(s).

- `bucket_width: optional "1d" or "1m" or "1h"`

  Time granularity of the response data.

  - `"1d"`

  - `"1m"`

  - `"1h"`

- `context_window: optional array of "0-200k" or "200k-1M"`

  Restrict usage returned to the specified context window(s).

  - `"0-200k"`

  - `"200k-1M"`

- `ending_at: optional string`

  Time buckets that end before this RFC 3339 timestamp will be returned.

- `group_by: optional array of "api_key_id" or "workspace_id" or "model" or 2 more`

  Group by any subset of the available options.

  - `"api_key_id"`

  - `"workspace_id"`

  - `"model"`

  - `"service_tier"`

  - `"context_window"`

- `limit: optional number`

  Maximum number of time buckets to return in the response.

  The default and max limits depend on `bucket_width`:
  • `"1d"`: Default of 7 days, maximum of 31 days
  • `"1h"`: Default of 24 hours, maximum of 168 hours
  • `"1m"`: Default of 60 minutes, maximum of 1440 minutes

- `models: optional array of string`

  Restrict usage returned to the specified model(s).

- `page: optional string`

  Optionally set to the `next_page` token from the previous response.

- `service_tiers: optional array of "standard" or "batch" or "priority" or 3 more`

  Restrict usage returned to the specified service tier(s).

  - `"standard"`

  - `"batch"`

  - `"priority"`

  - `"priority_on_demand"`

  - `"flex"`

  - `"flex_discount"`

- `workspace_ids: optional array of string`

  Restrict usage returned to the specified workspace ID(s).

### Returns

- `MessagesUsageReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { api_key_id, cache_creation, cache_read_input_tokens, 7 more }`

      List of usage items for this time bucket.  There may be multiple items if one or more `group_by[]` parameters are specified.

      - `api_key_id: string`

        ID of the API key used. Null if not grouping by API key or for usage in the Anthropic Console.

      - `cache_creation: object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens }`

        The number of input tokens for cache creation.

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_read_input_tokens: number`

        The number of input tokens read from the cache.

      - `context_window: "0-200k" or "200k-1M"`

        Context window used. Null if not grouping by context window.

        - `"0-200k"`

        - `"200k-1M"`

      - `model: string`

        Model used. Null if not grouping by model.

      - `output_tokens: number`

        The number of output tokens generated.

      - `server_tool_use: object { web_search_requests }`

        Server-side tool usage metrics.

        - `web_search_requests: number`

          The number of web search requests made.

      - `service_tier: "standard" or "batch" or "priority" or 3 more`

        Service tier used. Null if not grouping by service tier.

        - `"standard"`

        - `"batch"`

        - `"priority"`

        - `"priority_on_demand"`

        - `"flex"`

        - `"flex_discount"`

      - `uncached_input_tokens: number`

        The number of uncached input tokens processed.

      - `workspace_id: string`

        ID of the Workspace used. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.

### Example

```http
curl https://api.anthropic.com/v1/organizations/usage_report/messages \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Retrieve Claude Code

**get** `/v1/organizations/usage_report/claude_code`

Retrieve daily aggregated usage metrics for Claude Code users.
Enables organizations to analyze developer productivity and build custom dashboards.

### Query Parameters

- `starting_at: string`

  UTC date in YYYY-MM-DD format. Returns metrics for this single day only.

- `limit: optional number`

  Number of records per page (default: 20, max: 1000).

- `page: optional string`

  Opaque cursor token from previous response's `next_page` field.

### Returns

- `ClaudeCodeUsageReport = object { data, has_more, next_page }`

  - `data: array of object { actor, core_metrics, customer_type, 6 more }`

    List of Claude Code usage records for the requested date.

    - `actor: object { email_address, type }  or object { api_key_name, type }`

      The user or API key that performed the Claude Code actions.

      - `UserActor = object { email_address, type }`

        - `email_address: string`

          Email address of the user who performed Claude Code actions.

        - `type: "user_actor"`

          - `"user_actor"`

      - `APIActor = object { api_key_name, type }`

        - `api_key_name: string`

          Name of the API key used to perform Claude Code actions.

        - `type: "api_actor"`

          - `"api_actor"`

    - `core_metrics: object { commits_by_claude_code, lines_of_code, num_sessions, pull_requests_by_claude_code }`

      Core productivity metrics measuring Claude Code usage and impact.

      - `commits_by_claude_code: number`

        Number of git commits created through Claude Code's commit functionality.

      - `lines_of_code: object { added, removed }`

        Statistics on code changes made through Claude Code.

        - `added: number`

          Total number of lines of code added across all files by Claude Code.

        - `removed: number`

          Total number of lines of code removed across all files by Claude Code.

      - `num_sessions: number`

        Number of distinct Claude Code sessions initiated by this actor.

      - `pull_requests_by_claude_code: number`

        Number of pull requests created through Claude Code's PR functionality.

    - `customer_type: "api" or "subscription"`

      Type of customer account (api for API customers, subscription for Pro/Team customers).

      - `"api"`

      - `"subscription"`

    - `date: string`

      UTC date for the usage metrics in YYYY-MM-DD format.

    - `model_breakdown: array of object { estimated_cost, model, tokens }`

      Token usage and cost breakdown by AI model used.

      - `estimated_cost: object { amount, currency }`

        Estimated cost for using this model

        - `amount: number`

          Estimated cost amount in minor currency units (e.g., cents for USD).

        - `currency: string`

          Currency code for the estimated cost (e.g., 'USD').

      - `model: string`

        Name of the AI model used for Claude Code interactions.

      - `tokens: object { cache_creation, cache_read, input, output }`

        Token usage breakdown for this model

        - `cache_creation: number`

          Number of cache creation tokens consumed by this model.

        - `cache_read: number`

          Number of cache read tokens consumed by this model.

        - `input: number`

          Number of input tokens consumed by this model.

        - `output: number`

          Number of output tokens generated by this model.

    - `organization_id: string`

      ID of the organization that owns the Claude Code usage.

    - `terminal_type: string`

      Type of terminal or environment where Claude Code was used.

    - `tool_actions: map[object { accepted, rejected } ]`

      Breakdown of tool action acceptance and rejection rates by tool type.

      - `accepted: number`

        Number of tool action proposals that the user accepted.

      - `rejected: number`

        Number of tool action proposals that the user rejected.

    - `subscription_type: optional "enterprise" or "team"`

      Subscription tier for subscription customers. Null for API customers.

      - `"enterprise"`

      - `"team"`

  - `has_more: boolean`

    True if there are more records available beyond the current page.

  - `next_page: string`

    Opaque cursor token for fetching the next page of results, or null if no more pages are available.

### Example

```http
curl https://api.anthropic.com/v1/organizations/usage_report/claude_code \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### Claude Code Usage Report

- `ClaudeCodeUsageReport = object { data, has_more, next_page }`

  - `data: array of object { actor, core_metrics, customer_type, 6 more }`

    List of Claude Code usage records for the requested date.

    - `actor: object { email_address, type }  or object { api_key_name, type }`

      The user or API key that performed the Claude Code actions.

      - `UserActor = object { email_address, type }`

        - `email_address: string`

          Email address of the user who performed Claude Code actions.

        - `type: "user_actor"`

          - `"user_actor"`

      - `APIActor = object { api_key_name, type }`

        - `api_key_name: string`

          Name of the API key used to perform Claude Code actions.

        - `type: "api_actor"`

          - `"api_actor"`

    - `core_metrics: object { commits_by_claude_code, lines_of_code, num_sessions, pull_requests_by_claude_code }`

      Core productivity metrics measuring Claude Code usage and impact.

      - `commits_by_claude_code: number`

        Number of git commits created through Claude Code's commit functionality.

      - `lines_of_code: object { added, removed }`

        Statistics on code changes made through Claude Code.

        - `added: number`

          Total number of lines of code added across all files by Claude Code.

        - `removed: number`

          Total number of lines of code removed across all files by Claude Code.

      - `num_sessions: number`

        Number of distinct Claude Code sessions initiated by this actor.

      - `pull_requests_by_claude_code: number`

        Number of pull requests created through Claude Code's PR functionality.

    - `customer_type: "api" or "subscription"`

      Type of customer account (api for API customers, subscription for Pro/Team customers).

      - `"api"`

      - `"subscription"`

    - `date: string`

      UTC date for the usage metrics in YYYY-MM-DD format.

    - `model_breakdown: array of object { estimated_cost, model, tokens }`

      Token usage and cost breakdown by AI model used.

      - `estimated_cost: object { amount, currency }`

        Estimated cost for using this model

        - `amount: number`

          Estimated cost amount in minor currency units (e.g., cents for USD).

        - `currency: string`

          Currency code for the estimated cost (e.g., 'USD').

      - `model: string`

        Name of the AI model used for Claude Code interactions.

      - `tokens: object { cache_creation, cache_read, input, output }`

        Token usage breakdown for this model

        - `cache_creation: number`

          Number of cache creation tokens consumed by this model.

        - `cache_read: number`

          Number of cache read tokens consumed by this model.

        - `input: number`

          Number of input tokens consumed by this model.

        - `output: number`

          Number of output tokens generated by this model.

    - `organization_id: string`

      ID of the organization that owns the Claude Code usage.

    - `terminal_type: string`

      Type of terminal or environment where Claude Code was used.

    - `tool_actions: map[object { accepted, rejected } ]`

      Breakdown of tool action acceptance and rejection rates by tool type.

      - `accepted: number`

        Number of tool action proposals that the user accepted.

      - `rejected: number`

        Number of tool action proposals that the user rejected.

    - `subscription_type: optional "enterprise" or "team"`

      Subscription tier for subscription customers. Null for API customers.

      - `"enterprise"`

      - `"team"`

  - `has_more: boolean`

    True if there are more records available beyond the current page.

  - `next_page: string`

    Opaque cursor token for fetching the next page of results, or null if no more pages are available.

### Messages Usage Report

- `MessagesUsageReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { api_key_id, cache_creation, cache_read_input_tokens, 7 more }`

      List of usage items for this time bucket.  There may be multiple items if one or more `group_by[]` parameters are specified.

      - `api_key_id: string`

        ID of the API key used. Null if not grouping by API key or for usage in the Anthropic Console.

      - `cache_creation: object { ephemeral_1h_input_tokens, ephemeral_5m_input_tokens }`

        The number of input tokens for cache creation.

        - `ephemeral_1h_input_tokens: number`

          The number of input tokens used to create the 1 hour cache entry.

        - `ephemeral_5m_input_tokens: number`

          The number of input tokens used to create the 5 minute cache entry.

      - `cache_read_input_tokens: number`

        The number of input tokens read from the cache.

      - `context_window: "0-200k" or "200k-1M"`

        Context window used. Null if not grouping by context window.

        - `"0-200k"`

        - `"200k-1M"`

      - `model: string`

        Model used. Null if not grouping by model.

      - `output_tokens: number`

        The number of output tokens generated.

      - `server_tool_use: object { web_search_requests }`

        Server-side tool usage metrics.

        - `web_search_requests: number`

          The number of web search requests made.

      - `service_tier: "standard" or "batch" or "priority" or 3 more`

        Service tier used. Null if not grouping by service tier.

        - `"standard"`

        - `"batch"`

        - `"priority"`

        - `"priority_on_demand"`

        - `"flex"`

        - `"flex_discount"`

      - `uncached_input_tokens: number`

        The number of uncached input tokens processed.

      - `workspace_id: string`

        ID of the Workspace used. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.

# Cost Report

## Retrieve

**get** `/v1/organizations/cost_report`

Get Cost Report

### Query Parameters

- `starting_at: string`

  Time buckets that start on or after this RFC 3339 timestamp will be returned.
  Each time bucket will be snapped to the start of the minute/hour/day in UTC.

- `bucket_width: optional "1d"`

  Time granularity of the response data.

  - `"1d"`

- `ending_at: optional string`

  Time buckets that end before this RFC 3339 timestamp will be returned.

- `group_by: optional array of "workspace_id" or "description"`

  Group by any subset of the available options.

  - `"workspace_id"`

  - `"description"`

- `limit: optional number`

  Maximum number of time buckets to return in the response.

- `page: optional string`

  Optionally set to the `next_page` token from the previous response.

### Returns

- `CostReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { amount, context_window, cost_type, 6 more }`

      List of cost items for this time bucket. There may be multiple items if one or more `group_by[]` parameters are specified.

      - `amount: string`

        Cost amount in lowest currency units (e.g. cents) as a decimal string. For example, `"123.45"` in `"USD"` represents `$1.23`.

      - `context_window: "0-200k" or "200k-1M"`

        Input context window used. Null if not grouping by description or for non-token costs.

        - `"0-200k"`

        - `"200k-1M"`

      - `cost_type: "tokens" or "web_search" or "code_execution"`

        Type of cost. Null if not grouping by description.

        - `"tokens"`

        - `"web_search"`

        - `"code_execution"`

      - `currency: string`

        Currency code for the cost amount. Currently always `"USD"`.

      - `description: string`

        Description of the cost item. Null if not grouping by description.

      - `model: string`

        Model name used. Null if not grouping by description or for non-token costs.

      - `service_tier: "standard" or "batch"`

        Service tier used. Null if not grouping by description or for non-token costs.

        - `"standard"`

        - `"batch"`

      - `token_type: "uncached_input_tokens" or "output_tokens" or "cache_read_input_tokens" or 2 more`

        Type of token. Null if not grouping by description or for non-token costs.

        - `"uncached_input_tokens"`

        - `"output_tokens"`

        - `"cache_read_input_tokens"`

        - `"cache_creation.ephemeral_1h_input_tokens"`

        - `"cache_creation.ephemeral_5m_input_tokens"`

      - `workspace_id: string`

        ID of the Workspace this cost is associated with. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.

### Example

```http
curl https://api.anthropic.com/v1/organizations/cost_report \
    -H "X-Api-Key: $ANTHROPIC_ADMIN_API_KEY"
```

## Domain Types

### Cost Report

- `CostReport = object { data, has_more, next_page }`

  - `data: array of object { ending_at, results, starting_at }`

    - `ending_at: string`

      End of the time bucket (exclusive) in RFC 3339 format.

    - `results: array of object { amount, context_window, cost_type, 6 more }`

      List of cost items for this time bucket. There may be multiple items if one or more `group_by[]` parameters are specified.

      - `amount: string`

        Cost amount in lowest currency units (e.g. cents) as a decimal string. For example, `"123.45"` in `"USD"` represents `$1.23`.

      - `context_window: "0-200k" or "200k-1M"`

        Input context window used. Null if not grouping by description or for non-token costs.

        - `"0-200k"`

        - `"200k-1M"`

      - `cost_type: "tokens" or "web_search" or "code_execution"`

        Type of cost. Null if not grouping by description.

        - `"tokens"`

        - `"web_search"`

        - `"code_execution"`

      - `currency: string`

        Currency code for the cost amount. Currently always `"USD"`.

      - `description: string`

        Description of the cost item. Null if not grouping by description.

      - `model: string`

        Model name used. Null if not grouping by description or for non-token costs.

      - `service_tier: "standard" or "batch"`

        Service tier used. Null if not grouping by description or for non-token costs.

        - `"standard"`

        - `"batch"`

      - `token_type: "uncached_input_tokens" or "output_tokens" or "cache_read_input_tokens" or 2 more`

        Type of token. Null if not grouping by description or for non-token costs.

        - `"uncached_input_tokens"`

        - `"output_tokens"`

        - `"cache_read_input_tokens"`

        - `"cache_creation.ephemeral_1h_input_tokens"`

        - `"cache_creation.ephemeral_5m_input_tokens"`

      - `workspace_id: string`

        ID of the Workspace this cost is associated with. Null if not grouping by workspace or for the default workspace.

    - `starting_at: string`

      Start of the time bucket (inclusive) in RFC 3339 format.

  - `has_more: boolean`

    Indicates if there are more results.

  - `next_page: string`

    Token to provide in as `page` in the subsequent request to retrieve the next page of data.
