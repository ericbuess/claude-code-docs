# Manage WIF with the Admin API

Create and manage Workload Identity Federation service accounts, issuers, and rules programmatically for infrastructure-as-code and CI workflows.

---

The Admin API lets you create and manage [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation) resources programmatically: service accounts, federation issuers, and federation rules. Use it to keep your federation configuration in infrastructure as code, provision it from CI, and reproduce it across organizations instead of clicking through the Claude Console. These endpoints share the `/v1/organizations` path prefix with the rest of the [Admin API](/docs/en/manage-claude/admin-api).

## Prerequisites

Every request on this page authenticates with an OAuth bearer token that carries the `org:admin` scope. The scope is granted only to organization members with the admin, owner, or primary owner role, and it grants access to the whole organization: any workspace binding is ignored. There are two ways to obtain a token, and they carry different permissions: a token from your own login acts as a user, while a federated token acts as a service account and cannot perform every operation on this page.

**Interactive (your terminal):** Log in with the [`ant` CLI](/docs/en/cli-sdks-libraries/cli/quickstart) under a dedicated profile, requesting the `org:admin` scope (see [Admin access](/docs/en/cli-sdks-libraries/cli/authentication#admin-access)), then export the bearer token:

```bash CLI
ant auth login --profile admin --scope "org:admin"
export ANTHROPIC_OAUTH_TOKEN=$(ant auth print-credentials --profile admin --access-token)
```

Interactive tokens are short-lived; if requests start returning 401, re-run the export command (it refreshes the token automatically).

**Workload (CI and automation):** Create a federation rule with `oauth_scope: org:admin` that targets a service account whose `organization_role` is `admin`. The rule itself must be created in the Claude Console: granting a workload organization-admin access is a deliberate human action, not something automation can bootstrap for itself. The next section walks through this once-per-organization setup.

## Bootstrap a workload to manage WIF

One Console-created rule is enough to put the rest of your federation configuration under infrastructure as code: grant a single trusted workload the `org:admin` scope, and let that workload manage federation issuers and every workspace-scoped federation rule through this API.

<Steps>
  <Step title="Create the org:admin rule in the Console">
    In the Claude Console, go to **Settings → Workload identity** and select **Connect workload** to create one federation rule for your automation workload, for example a GitHub Actions workflow in your infrastructure repository. Under **Advanced rule options**, set the rule's OAuth scope to `org:admin`: the wizard then creates the new service account with the Admin organization role (or asks you to pick an existing admin service account as the target).

    <Warning>
      Match the rule to one exact workload identity, not a broad pattern. `subject_prefix` is an exact match unless it ends in `*`. For GitHub Actions, pin the subject to a protected branch, such as `repo:my-org/my-repo:ref:refs/heads/main`. A trailing wildcard such as `repo:my-org/my-repo:*` also matches `pull_request` runs, including runs triggered from forks, so anyone who could open a pull request against the repository could mint an `org:admin` token. See [Restrict which workflows can authenticate](/docs/en/manage-claude/wif-providers/github-actions#restrict-which-workflows-can-authenticate).
    </Warning>
  </Step>

  <Step title="Exchange the workload's identity token">
    At runtime, the workload exchanges the JWT from its identity provider for a short-lived `org:admin` bearer token using the same [token exchange](/docs/en/manage-claude/workload-identity-federation#authenticate-from-your-workload) as any other federated workload.
  </Step>

  <Step title="Manage issuers and workspace-scoped rules through the API">
    With the minted token in `ANTHROPIC_OAUTH_TOKEN`, the workload creates and manages your federation configuration using the endpoints on this page.
  </Step>
</Steps>

For the operations a workload-minted token can and cannot perform, see [Permissions and constraints](#permissions-and-constraints). If you already created issuers, service accounts, or rules with the Connect workload wizard, list them with the following endpoints and import them into your infrastructure-as-code state instead of recreating them.

## Authentication

All endpoints live under `https://api.anthropic.com/v1/organizations/`. Every request to the federation and service-account endpoints needs the API version header and the bearer token:

```bash cURL
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

Admin API keys are not accepted on these endpoints; the Admin API page's `x-api-key` examples do not apply here.

## Service accounts

A [service account](/docs/en/manage-claude/workload-identity-federation#service-accounts) (`svac_...`) is the non-human identity that a federated token acts as. Set `organization_role` to `developer`.

```bash cURL
# Create a service account
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN" \
  --header "content-type: application/json" \
  --data '{
    "name": "inference-worker",
    "organization_role": "developer"
  }'

# List service accounts
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/service_accounts?limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"

# Archive a service account
curl --fail-with-body -sS --request POST "https://api.anthropic.com/v1/organizations/service_accounts/svac_.../archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

The create endpoint returns the new service account:

```json
{
  "id": "svac_...",
  "name": "inference-worker",
  "organization_role": "developer",
  "created_at": "...",
  "type": "service_account",
  "...": "..."
}
```

To read or update a single service account, use `GET` and `POST` on `/v1/organizations/service_accounts/{service_account_id}`. A service account must be a member of a workspace before federated tokens can act in it. Every service account has an implicit membership in your organization's default workspace; add explicit memberships for other workspaces with `GET`, `POST`, and `DELETE` on `/v1/organizations/service_accounts/{service_account_id}/workspaces`, where `DELETE` targets `.../workspaces/{workspace_id}`.

For complete parameter details and response schemas, see the [Service accounts API reference](/docs/en/api/admin/service_accounts).

## Federation issuers

A [federation issuer](/docs/en/manage-claude/workload-identity-federation#federation-issuers) (`fdis_...`) registers an OIDC identity provider with your organization. The `jwks` field is a discriminated union that controls how Anthropic fetches the provider's signing keys:

| `jwks` value                             | When to use                                                                       |
| ---------------------------------------- | --------------------------------------------------------------------------------- |
| `{"type": "discovery"}`                  | The provider serves `/.well-known/openid-configuration` at the issuer URL.        |
| `{"type": "explicit_url", "url": "..."}` | Point at a JWKS endpoint directly.                                                |
| `{"type": "inline", "keys": [...]}`      | Upload the key set for providers that are not reachable from the public internet. |

```bash cURL
# Register an issuer (GitHub Actions, with JWKS discovery)
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN" \
  --header "content-type: application/json" \
  --data '{
    "name": "github-actions",
    "issuer_url": "https://token.actions.githubusercontent.com",
    "jwks": {"type": "discovery"}
  }'

# List issuers
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_issuers?limit=20" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"

# Archive an issuer
curl --fail-with-body -sS --request POST "https://api.anthropic.com/v1/organizations/federation_issuers/fdis_.../archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

To read or update a single issuer, use `GET` and `POST` on `/v1/organizations/federation_issuers/{issuer_id}`. An OAuth caller cannot update an issuer that backs a rule whose `oauth_scope` is anything other than `workspace:developer` or `workspace:inference`; see [Permissions and constraints](#permissions-and-constraints).

For complete parameter details and response schemas, see the [Federation issuers API reference](/docs/en/api/admin/federation_issuers).

## Federation rules

A [federation rule](/docs/en/manage-claude/workload-identity-federation#federation-rules) (`fdrl_...`) binds an issuer to a service account: JWTs from the issuer that satisfy the rule's match conditions can mint tokens that act as the rule's target. The `workspace_id` in the create request enables the rule in that workspace at creation; add more workspaces later through the `/federation_rules/{rule_id}/workspaces` sub-resource. Either `workspace_id` or `applies_to_all_workspaces: true` is required on create.

```bash cURL
# Create a rule (GitHub Actions deploys from the main branch)
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN" \
  --header "content-type: application/json" \
  --data '{
    "name": "gha-deploy",
    "issuer_id": "fdis_...",
    "match": {
      "subject_prefix": "repo:my-org/my-repo:ref:refs/heads/main",
      "claims": {"repository_owner": "my-org"}
    },
    "target": {
      "type": "service_account",
      "service_account_id": "svac_..."
    },
    "workspace_id": "wrkspc_...",
    "oauth_scope": "workspace:developer",
    "token_lifetime_seconds": 600
  }'

# List rules, optionally filtered by issuer
curl --fail-with-body -sS "https://api.anthropic.com/v1/organizations/federation_rules?issuer_id=fdis_..." \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"

# Archive a rule
curl --fail-with-body -sS --request POST "https://api.anthropic.com/v1/organizations/federation_rules/fdrl_.../archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "authorization: Bearer $ANTHROPIC_OAUTH_TOKEN"
```

The list endpoint returns a page of rules and the cursor for the next page:

```json
{
  "data": [{ "id": "fdrl_...", "name": "gha-deploy", "...": "..." }],
  "next_page": "..."
}
```

To read or update a single rule, use `GET` and `POST` on `/v1/organizations/federation_rules/{rule_id}`. To manage the workspaces a rule can mint tokens in, use `GET` and `POST` on `/v1/organizations/federation_rules/{rule_id}/workspaces`, and `DELETE` on `/v1/organizations/federation_rules/{rule_id}/workspaces/{workspace_id}`.

For complete parameter details and response schemas, see the [Federation rules API reference](/docs/en/api/admin/federation_rules).

## Permissions and constraints

<Note>
  * OAuth-authenticated callers can only create or modify rules whose `oauth_scope` is `workspace:developer` or `workspace:inference`. To create or modify a rule with any other scope (such as `org:admin` or `workspace:manage_tunnels`), use the Console.
  * An OAuth caller cannot update a federation issuer that backs a rule whose `oauth_scope` is anything other than `workspace:developer` or `workspace:inference` (such as `org:admin` or `workspace:manage_tunnels`). Consider registering a dedicated issuer for the bootstrap rule so the issuers behind workspace-scoped rules stay updatable through the API.
  * Admin API keys are not accepted on these endpoints, for reads or writes; use an `org:admin` OAuth token.
</Note>

A rule with `oauth_scope: org:admin` must target a service account whose `organization_role` is `admin`. Resource names must match `^[a-z0-9-]+$`, be 1 to 255 characters, and be unique within an organization for each resource type; for the full field-level constraints, see [Validation rules](/docs/en/manage-claude/wif-reference#validation-rules).

## Pagination and archiving

The service-account, federation-issuer, and federation-rule list endpoints accept `limit` (1 to 100, default 20) and a `page` cursor taken from the previous response. Pass the response's `next_page` value as the `page` query parameter on the next request. The rule-workspaces sub-resource list returns the full set without pagination. Archived resources are hidden from lists by default; pass `include_archived=true` to include them.

Archiving is a soft delete and is idempotent: archiving an already-archived resource succeeds. Archiving an issuer or a service account returns `400` while a live federation rule still references it; archive the rule first.

## See also

* [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation): concepts and the Console setup walkthrough
* [WIF reference](/docs/en/manage-claude/wif-reference): environment variables, validation rules, OAuth scopes, and error codes
* [Admin API](/docs/en/manage-claude/admin-api): the rest of the organization management surface
* [Admin API reference](/docs/en/api/admin): generated request and response schemas for every Admin API endpoint
