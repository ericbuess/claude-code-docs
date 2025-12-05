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
