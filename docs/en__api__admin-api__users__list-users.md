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
