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
