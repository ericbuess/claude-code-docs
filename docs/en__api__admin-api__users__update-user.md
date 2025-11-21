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
