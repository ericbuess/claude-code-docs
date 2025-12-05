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
