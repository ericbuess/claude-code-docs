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
