# Admin API

Manage organization members, workspaces, invites, and API keys programmatically with the Admin API, using an Admin API key or an `org:admin` OAuth token.

---

<Tip>
  **The Admin API is unavailable for individual accounts.** To collaborate with teammates and add members, set up your organization in **Console → Settings → Organization**.
</Tip>

The [Admin API](/docs/en/api/admin) allows you to programmatically manage your organization's resources, including organization members, workspaces, and API keys. This provides programmatic control over administrative tasks that would otherwise require manual configuration in the [Claude Console](/).

<Check>
  **The Admin API requires special access**

  The Admin API accepts two credentials: an Admin API key (starting with `sk-ant-admin...`) sent in the `x-api-key` header or an OAuth bearer token with the `org:admin` scope sent in the `authorization: Bearer` header. Only organization members with the admin role can provision Admin API keys, and only members with the admin, owner, or primary owner role can obtain `org:admin` tokens. See [Create an Admin API key](/docs/en/manage-claude/admin-api-keys).
</Check>

<Note>
  **Claude Platform on AWS:** Most of the Admin API is not available on Claude Platform on AWS. Workspace endpoints (create, get, list, update, and archive on `/v1/organizations/workspaces`) are available. Other endpoints including organization members, workspace members, invites, API keys, usage reports, cost reports, and rate limit reports are not available. See [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws) for details.
</Note>

## Authentication

Authenticate with either credential. To create an Admin API key for your organization type, see [Create an Admin API key](/docs/en/manage-claude/admin-api-keys). The following examples call the [organization info endpoint](#accessing-organization-info) both ways:

**OAuth bearer:**

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

An `org:admin` token grants access to the whole organization, regardless of the workspace the underlying profile or federation rule is bound to. To obtain one, see the prerequisites in [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api#prerequisites).

**Admin API key:**

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## How the Admin API works

When you use the Admin API:

1. You make requests using either credential from the [Authentication](#authentication) section

2. The API allows you to manage:

   * Organization members and their roles
   * Organization member invites
   * Workspaces and their members
   * API keys
   * Service accounts, federation issuers, and federation rules (these endpoints require an `org:admin` OAuth token; Admin API keys are not accepted)

This is useful for:

* Automating user onboarding/offboarding
* Programmatically managing workspace access
* Monitoring and managing API key usage

## Organization roles and permissions

There are five organization-level roles. See more details in the [API Console roles and permissions](https://support.claude.com/en/articles/10186004-api-console-roles-and-permissions) article.

| Role               | Permissions                                                                   |
| ------------------ | ----------------------------------------------------------------------------- |
| user               | Can use Workbench                                                             |
| claude\_code\_user | Can use Workbench and [Claude Code](https://code.claude.com/docs/en/overview) |
| developer          | Can use Workbench and manage API keys                                         |
| billing            | Can use Workbench and manage billing details                                  |
| admin              | Can do all of the preceding, plus manage users                                |

Organization owners and primary owners have all admin permissions and can additionally manage admins. All references to the admin role on this page also apply to owners and primary owners.

## Key concepts

### Organization members

You can list [organization members](/docs/en/api/admin-api/users/get-user), update member roles, and remove members.

<CodeGroup>
  ```bash cURL
  # List organization members
  curl "https://api.anthropic.com/v1/organizations/users?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Update member role
  curl "https://api.anthropic.com/v1/organizations/users/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{"role": "developer"}'

  # Remove member
  curl --request DELETE "https://api.anthropic.com/v1/organizations/users/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### Organization invites

You can invite users to organizations and manage those [invites](/docs/en/api/admin-api/invites/get-invite).

<CodeGroup>
  ```bash cURL
  # Create invite
  curl --request POST "https://api.anthropic.com/v1/organizations/invites" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "email": "newuser@domain.com",
      "role": "developer"
    }'

  # List invites
  curl "https://api.anthropic.com/v1/organizations/invites?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Delete invite
  curl --request DELETE "https://api.anthropic.com/v1/organizations/invites/{invite_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### Workspaces

For a comprehensive guide to workspaces, including Console and API examples, see [Workspaces](/docs/en/manage-claude/workspaces).

### Workspace members

Manage [user access to specific workspaces](/docs/en/api/admin-api/workspace_members/get-workspace-member):

<CodeGroup>
  ```bash cURL
  # Add member to workspace
  curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "user_id": "user_xxx",
      "workspace_role": "workspace_developer"
    }'

  # List workspace members
  curl "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members?limit=10" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Update member role
  curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "workspace_role": "workspace_admin"
    }'

  # Remove member from workspace
  curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
  ```
</CodeGroup>

### API keys

Monitor and manage [API keys](/docs/en/api/admin/api_keys/list). Each key in the response includes its `expires_at` timestamp (`null` for keys without an [expiration](/docs/en/manage-claude/authentication#key-expiration)):

<CodeGroup>
  ```bash cURL
  # List API keys
  curl "https://api.anthropic.com/v1/organizations/api_keys?limit=10&status=active&workspace_id=wrkspc_xxx" \
    --header "anthropic-version: 2023-06-01" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

  # Update API key
  curl --request POST "https://api.anthropic.com/v1/organizations/api_keys/{api_key_id}" \
    --header "anthropic-version: 2023-06-01" \
    --header "content-type: application/json" \
    --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
    --data '{
      "status": "inactive",
      "name": "New Key Name"
    }'
  ```
</CodeGroup>

### Service accounts

Create and manage service accounts (`svac_...`), the non-human identities that [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation) tokens act as. Admin API keys are not accepted on the service-account, federation-issuer, or federation-rule endpoints; use an `org:admin` OAuth token. See [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api#service-accounts).

### Federation issuers

Register the OIDC identity providers (`fdis_...`) whose tokens may assert workload identity for your organization. See [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api#federation-issuers).

### Federation rules

Manage the rules (`fdrl_...`) that map issuer tokens to service accounts and scopes. See [Manage WIF with the Admin API](/docs/en/manage-claude/wif-admin-api#federation-rules).

## Accessing organization info

Get information about your organization programmatically with the `/v1/organizations/me` endpoint.

For example:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/me" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "id": "12345678-1234-5678-1234-567812345678",
  "type": "organization",
  "name": "Organization Name"
}
```

This endpoint is useful for programmatically determining which organization an Admin API key belongs to.

For complete parameter details and response schemas, see the [Organization Info API reference](/docs/en/api/admin-api/organization/get-me).

## Usage and cost reports

Track your organization's usage and costs with the [Usage and Cost API](/docs/en/manage-claude/usage-cost-api).

## Claude Code analytics

Monitor developer productivity and Claude Code adoption with the [Claude Code Analytics API](/docs/en/manage-claude/claude-code-analytics-api).

## Rate limits

Read the rate limits configured for your organization and its workspaces with the [Rate Limits API](/docs/en/manage-claude/rate-limits-api).

## Compliance API

Retrieve audit and activity data for your organization with the [Compliance API](/docs/en/manage-claude/compliance-api). Admin API keys can read the Activity Feed only; for full access, see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).

## Best practices

To effectively use the Admin API:

* Use meaningful names and descriptions for workspaces and API keys
* Implement proper error handling for failed operations
* Regularly audit member roles and permissions
* Clean up unused workspaces and expired invites
* Monitor API key usage, audit each key's [`expires_at`](/docs/en/manage-claude/authentication#key-expiration), and rotate keys periodically

## FAQ

<AccordionGroup>
  <Accordion title="What permissions are needed to use the Admin API?">
    The Admin API accepts either an Admin API key (starting with `sk-ant-admin`) or an OAuth bearer token with the `org:admin` scope. Only organization members with the admin role can provision Admin API keys, and only members with the admin, owner, or primary owner role can obtain `org:admin` tokens. See [Authentication](#authentication).
  </Accordion>

  <Accordion title="Can I create new API keys through the Admin API?">
    No, new API keys can only be created through the Claude Console for security reasons. The Admin API can only manage existing API keys.
  </Accordion>

  <Accordion title="What happens to API keys when removing a user?">
    API keys persist in their current state as they are scoped to the Organization, not to individual users.
  </Accordion>

  <Accordion title="Can organization admins be removed through the API?">
    No, organization members with the admin role cannot be removed through the API for security reasons.
  </Accordion>

  <Accordion title="How long do organization invites last?">
    Organization invites expire after 21 days. There is currently no way to modify this expiration period.
  </Accordion>
</AccordionGroup>

For workspace-specific questions, see the [Workspaces FAQ](/docs/en/manage-claude/workspaces#faq).
