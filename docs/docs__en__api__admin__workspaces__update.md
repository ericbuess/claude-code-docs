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
