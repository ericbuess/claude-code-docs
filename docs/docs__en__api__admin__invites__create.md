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
