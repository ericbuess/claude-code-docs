# WIF reference

Environment variables, validation rules, profile configuration, and error reference for Workload Identity Federation.

---

This page collects the configuration surfaces, validation constraints, and error mappings for [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation). For setup walkthroughs, see the [provider guides](/docs/en/manage-claude/workload-identity-federation#identity-providers).

## Token exchange request

`POST /v1/oauth/token` accepts a JSON body using the [RFC 7523](https://www.rfc-editor.org/rfc/rfc7523) `jwt-bearer` grant. The SDKs build this request for you from the [environment variables](#environment-variables); the cURL examples on each provider guide show the raw body.

| Field                | Required    | Description                                                                                                                                                                                                                                                                   |
| -------------------- | ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `grant_type`         | Yes         | Always `urn:ietf:params:oauth:grant-type:jwt-bearer`.                                                                                                                                                                                                                         |
| `assertion`          | Yes         | The OIDC JWT issued by your identity provider.                                                                                                                                                                                                                                |
| `federation_rule_id` | Yes         | Tagged ID (`fdrl_...`) of the federation rule to evaluate.                                                                                                                                                                                                                    |
| `organization_id`    | Yes         | UUID of your Anthropic organization.                                                                                                                                                                                                                                          |
| `service_account_id` | Yes         | Tagged ID (`svac_...`) of the target service account.                                                                                                                                                                                                                         |
| `workspace_id`       | Conditional | Tagged ID (`wrkspc_...`) of the workspace to scope the minted token to, or the literal `default` for the organization's default workspace. Required when the rule is enabled for more than one workspace. When omitted, the server selects the rule's sole enabled workspace. |

## Token exchange response

`POST /v1/oauth/token` returns a standard OAuth 2.0 token response ([RFC 6749 §5.1](https://www.rfc-editor.org/rfc/rfc6749#section-5.1)):

| Field          | Type    | Description                                                                                               |
| -------------- | ------- | --------------------------------------------------------------------------------------------------------- |
| `access_token` | string  | The short-lived Anthropic token, prefixed `sk-ant-oat01-...`. Pass it as `Authorization: Bearer <token>`. |
| `token_type`   | string  | Always `Bearer`.                                                                                          |
| `expires_in`   | integer | Seconds until the token expires.                                                                          |
| `scope`        | string  | The OAuth scope granted by the matched rule.                                                              |

## Environment variables

The SDK reads these variables to perform a federated token exchange with no constructor arguments.

| Variable                        | Required                         | Description                                                                                                                                                                                                                                                                                                                         | Example                                |
| ------------------------------- | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------- |
| `ANTHROPIC_FEDERATION_RULE_ID`  | Yes                              | Tagged ID of the federation rule to evaluate.                                                                                                                                                                                                                                                                                       | `fdrl_...`                             |
| `ANTHROPIC_ORGANIZATION_ID`     | Yes                              | UUID of your Anthropic organization. Find it in the Claude Console under **Settings > Organization**.                                                                                                                                                                                                                               | `00000000-0000-0000-0000-000000000000` |
| `ANTHROPIC_IDENTITY_TOKEN_FILE` | One of `_TOKEN_FILE` or `_TOKEN` | Filesystem path to the JWT issued by your identity provider (IdP). The SDK re-reads this file on every exchange so that projected tokens which rotate on disk are always current.                                                                                                                                                   | `/var/run/secrets/anthropic.com/token` |
| `ANTHROPIC_IDENTITY_TOKEN`      | One of `_TOKEN_FILE` or `_TOKEN` | The literal JWT as a string. Use when your platform injects the token as an environment variable rather than a file.                                                                                                                                                                                                                | `eyJhbGciOiJSUzI1NiIs...`              |
| `ANTHROPIC_SERVICE_ACCOUNT_ID`  | Yes                              | Tagged ID of the target Anthropic service account that the issued access token acts as.                                                                                                                                                                                                                                             | `svac_...`                             |
| `ANTHROPIC_WORKSPACE_ID`        | Conditional                      | Tagged ID of the workspace to scope the minted token to, or the literal `default`. Required when the federation rule is enabled for more than one workspace; optional when the rule is bound to a single workspace. The minted token is scoped to this workspace at exchange time, so switching workspaces requires a new exchange. | `wrkspc_...`                           |
| `ANTHROPIC_PROFILE`             | No                               | Name of a [configuration profile](#profile-configuration-file) to load. Takes precedence over the federation environment variables in this table.                                                                                                                                                                                   | `staging-profile`                      |

The direct environment-variable federation path activates only when `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, and one of `ANTHROPIC_IDENTITY_TOKEN_FILE` or `ANTHROPIC_IDENTITY_TOKEN` are all set. `ANTHROPIC_WORKSPACE_ID` is read alongside but does not gate activation.

<Warning>
  A variable that is set to an empty string still occupies its slot in the credential precedence chain. If `ANTHROPIC_API_KEY=""` is exported, the SDK selects the API-key path with an empty key rather than falling through to federation. Unset unused credential variables rather than blanking them.
</Warning>

### Credential precedence

The SDK resolves credentials in this order. The first source that yields a credential wins.

| Order | Source                                                           | Notes                                                                                                                              |
| ----- | ---------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| 1     | Constructor argument (`api_key=`, `auth_token=`, `credentials=`) | Always overrides everything else.                                                                                                  |
| 2     | `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN`                    | Shadows federation entirely. Unset these when migrating from API keys.                                                             |
| 3     | `ANTHROPIC_PROFILE`                                              | Loads `<config_dir>/configs/<name>.json`. A missing named profile is an error, not a fall-through.                                 |
| 4     | Federation environment variables                                 | `ANTHROPIC_FEDERATION_RULE_ID` + `ANTHROPIC_ORGANIZATION_ID` + `ANTHROPIC_SERVICE_ACCOUNT_ID` + `ANTHROPIC_IDENTITY_TOKEN[_FILE]`. |
| 5     | Active profile                                                   | Resolved from `<config_dir>/active_config`, falling back to a profile named `default`.                                             |

When a profile is loaded, environment variables fill any fields the profile omits but never override fields the profile sets explicitly. For example, `ANTHROPIC_WORKSPACE_ID` fills `workspace_id` only when the active profile does not set it.

## Profile configuration file

A profile is a named configuration file that the SDK and the `ant` CLI both read. Profiles let you ship federation parameters with your container image or switch between environments without changing code.

### Configuration directory

The SDK locates the configuration directory in this order:

1. `$ANTHROPIC_CONFIG_DIR`
2. `~/.config/anthropic` on Linux and macOS
3. `%APPDATA%\Anthropic` on Windows

### Active profile

The active profile name resolves in this order:

1. `$ANTHROPIC_PROFILE`
2. The contents of `<config_dir>/active_config` (a one-line file written by `ant profile activate <name>`)
3. The literal name `default`

Claude Code and the Claude Agent SDK honor this same resolution order, so a federation profile configured here also authenticates those tools without additional setup.

### File layout

| Path                                      | Contents                                                                                         | Sensitivity                                       |
| ----------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------- |
| `<config_dir>/configs/<profile>.json`     | `version`, the `authentication` block, `organization_id`, `workspace_id`, and `base_url`.        | Non-secret. Safe to commit or bake into an image. |
| `<config_dir>/credentials/<profile>.json` | `version`, the cached `access_token`, `expires_at`, and (for interactive login) `refresh_token`. | Secret. Written by the SDK with mode `0600`.      |

Both the config file and the credentials file carry a top-level string `version` field in `major.minor` format (currently `"1.0"`). The SDK writes this field automatically so future releases can detect and migrate older formats; omit it when authoring a config by hand and the SDK treats the file as the current version.

### Federation profile example

```json configs/production.json
{
  "version": "1.0",
  "authentication": {
    "type": "oidc_federation",
    "federation_rule_id": "fdrl_...",
    "service_account_id": "svac_...",
    "identity_token": {
      "source": "file",
      "path": "/var/run/secrets/anthropic.com/token"
    }
  },
  "organization_id": "00000000-0000-0000-0000-000000000000",
  "workspace_id": "wrkspc_...",
  "base_url": "https://api.anthropic.com"
}
```

If `authentication.identity_token` is omitted, the SDK falls back to `ANTHROPIC_IDENTITY_TOKEN_FILE` or `ANTHROPIC_IDENTITY_TOKEN` from the environment.

## OAuth scopes

The `oauth_scope` you set on a federation rule determines which Claude API endpoints the minted access token can call.

| Scope                      | Grants access to                                                                                                                                                                                                                                                                                                                                                                                                                    |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `workspace:developer`      | All non-administrative Claude API endpoints in the rule's workspace: [Messages](/docs/en/api/messages) (including streaming and token counting), [Models](/docs/en/api/models-list), [Managed Agents](/docs/en/managed-agents/overview) and their sessions, [Files](/docs/en/build-with-claude/files), and [Skills](/docs/en/build-with-claude/skills-guide). This matches the access an API key issued for the same workspace has. |
| `workspace:inference`      | The inference endpoints in the rule's workspace: [Messages](/docs/en/api/messages) (including streaming and token counting), [Models](/docs/en/api/models-list), and the [OpenAI-compatible chat endpoint](/docs/en/cli-sdks-libraries/libraries/openai-sdk). Use this for workloads that only need to call Claude and never need to manage Files, Skills, or other resources.                                                      |
| `workspace:manage_tunnels` | The [MCP tunnels API](/docs/en/agents-and-tools/mcp-tunnels/reference#tunnels-api): create, list, and get tunnels, register and archive CA certificates, reveal and rotate the tunnel token, and archive tunnels. The Console's create-tunnel modal locks this scope when you create a rule from it.                                                                                                                                |
| `org:admin`                | Full access to the [Admin API](/docs/en/manage-claude/admin-api) (organization members, invites, workspaces, API keys, and the rest). An OAuth `org:admin` token can only create or modify rules scoped to `workspace:developer` or `workspace:inference`, and cannot update an issuer that backs a rule with any other scope; see the [constraints](/docs/en/manage-claude/wif-admin-api#permissions-and-constraints).             |

A request to an endpoint outside the token's scope returns HTTP 403. Finer-grained scopes (per resource, or read versus write) are not currently available.

### Permission boundaries

A federation rule's `oauth_scope` is a ceiling: the minted token can never exceed it. The target service account's `organization_role` (`developer` or `admin`) determines which scopes are grantable, so a rule that grants `org:admin` must target a service account with `organization_role=admin`. Effective permissions are the intersection of the rule's scope and the service account's role.

| Rule `oauth_scope`    | Service account `organization_role` | Effective permissions                                                                                                                                                                                              |
| --------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `workspace:developer` | `admin`                             | Claude API access in the rule's workspace only. The scope caps the token below the role.                                                                                                                           |
| `org:admin`           | `admin`                             | Full Admin API access (organization members, invites, workspaces, API keys, and the rest), minus the OAuth-caller carve-outs; see [constraints](/docs/en/manage-claude/wif-admin-api#permissions-and-constraints). |

## Validation rules

Anthropic enforces these constraints when you create or update issuers and rules, and when verifying an incoming JWT at exchange time.

For complete parameter details and response schemas, see the [Service accounts API reference](/docs/en/api/admin/service_accounts), [Federation issuers API reference](/docs/en/api/admin/federation_issuers), and [Federation rules API reference](/docs/en/api/admin/federation_rules).

### Resource fields

| Field                                    | Constraint                                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Issuer, rule, and service account `name` | Must match `^[a-z0-9-]+$`, length 1 to 255 characters.                                                                                                                                                                                                                                     |
| `workspace_id`                           | Required on create unless `applies_to_all_workspaces` is true. The workspace (`wrkspc_...`) whose quota, billing, and rate limits apply to tokens minted under this rule. Must be a workspace in the same organization, and the target service account must be a member of that workspace. |
| `applies_to_all_workspaces`              | Boolean. Set `true` to enable the rule in every workspace in the organization instead of naming one; either this or `workspace_id` is required on create.                                                                                                                                  |
| `token_lifetime_seconds`                 | Integer between `60` and `86400` (1 minute to 24 hours). Default `3600`. Values outside this range are rejected at request time. See [Token lifetime and refresh](/docs/en/manage-claude/workload-identity-federation#token-lifetime-and-refresh).                                         |

### URL fields

The `issuer_url`, `jwks.discovery_base`, and `jwks.url` fields are validated:

| Constraint | Detail                                                                                                                    |
| ---------- | ------------------------------------------------------------------------------------------------------------------------- |
| Scheme     | Must be `https`.                                                                                                          |
| Port       | Must be `443` (explicit or default).                                                                                      |
| Host       | Must be a public DNS host name for your OIDC provider. Must resolve to public IP addresses; IP literals are not accepted. |

URL validation failures return `400 invalid_request_error` with the field name as a prefix on the error message (for example, `issuer_url: url must use https scheme`).

<Note>
  URL constraints apply only to URLs that Anthropic dials. In `explicit_url` and `inline` JWKS modes, and in `discovery` mode when `jwks.discovery_base` is set, the `issuer_url` is compared against the JWT `iss` claim as a string and is never fetched, so it may reference an internal hostname or non-standard port.
</Note>

### JWT verification

| Constraint        | Detail                                                                                                                                                                                     |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Maximum size      | The `assertion` JWT must be at most 16 KiB.                                                                                                                                                |
| Signing algorithm | Only asymmetric algorithms (RSA and ECDSA families: ES256, ES384, ES512, RS256, RS384, RS512, PS256, PS384, PS512) are accepted. HMAC (`HS256`, `HS384`, `HS512`) and `none` are rejected. |
| Key ID            | The JWT header must carry a `kid` that matches a key in the issuer's JWKS. Tokens without `kid` are rejected.                                                                              |
| Required claims   | `sub` must be present. `iat` must be present and not in the future. `exp` must be present and in the future.                                                                               |
| Maximum lifetime  | The token's lifetime (`exp` minus `iat`) must not exceed the issuer's configured maximum (1 hour by default, configurable for each issuer in the Claude Console).                          |
| Clock skew        | A 30-second leeway is applied to `exp`, `nbf`, and `iat`.                                                                                                                                  |

## Rule matching semantics

A federation rule's `match` block determines whether an incoming JWT is accepted. All populated fields are evaluated with AND semantics: the JWT must satisfy every populated matcher. At least one of `subject_prefix`, `claims`, or `condition` must be set; a `match` block that contains only `audience` (or no matchers at all) is rejected. This guards against rules that would accept every token from an issuer.

| Matcher          | Type                 | Semantics                                                                                                                                                                                                 |
| ---------------- | -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `subject_prefix` | string               | Exact match against the JWT `sub` claim. A trailing `*` makes it a prefix match (the `sub` value must begin with the characters before the `*`). Case-sensitive.                                          |
| `audience`       | string               | The JWT `aud` claim must contain this exact string. When `aud` is an array, any element matching exactly satisfies the check.                                                                             |
| `claims`         | map\<string, string> | Each key is a top-level claim name and each value is the required exact string value. For nested, numeric, boolean, or complex claims like lists and maps, use `condition` with a CEL expression instead. |
| `condition`      | string (CEL)         | A [CEL](https://cel.dev/) expression that must evaluate to `true`.                                                                                                                                        |

### CEL evaluation environment

The `condition` expression has access to a single variable:

| Variable | Type | Contents                                                                      |
| -------- | ---- | ----------------------------------------------------------------------------- |
| `claims` | map  | The full decoded JWT claim set. Nested objects are accessible as nested maps. |

Example:

```text wrap
claims.sub.startsWith("repo:acme-corp/") && claims.ref in ["refs/heads/main", "refs/heads/release"]
```

<Warning>
  CEL conditions are security boundaries. An expression that evaluates to `true` for more inputs than intended grants broader access than intended. Prefer the static matchers when they express your constraint.
</Warning>

## Errors

### Token exchange errors

`POST /v1/oauth/token` returns errors in the standard [API error shape](/docs/en/api/errors). The SDK wraps exchange failures in a typed `FederationExchangeError` (or language equivalent) that exposes the HTTP status, the response body, and the `request_id`.

| Status | Error             | Cause                                                                                                                            | Resolution                                                                                                                                                                                                                                                     |
| ------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 400    | `invalid_request` | `federation_rule_id` is malformed or a required request field is missing.                                                        | Verify the `fdrl_` ID and that the request body includes all required fields.                                                                                                                                                                                  |
| 400    | `invalid_request` | `workspace_id_required`: the federation rule is enabled for more than one workspace and the request omits `workspace_id`.        | Set `ANTHROPIC_WORKSPACE_ID` (or the `workspace_id` body field on a raw request) to the `wrkspc_...` ID you want the token scoped to. See [Token exchange request](#token-exchange-request).                                                                   |
| 400    | `invalid_grant`   | The JWT `iss` claim does not equal the registered `issuer_url` exactly.                                                          | Compare byte-for-byte, including trailing slashes and scheme: `jq -rR 'split(".")[1] \| gsub("-";"+") \| gsub("_";"/") \| @base64d \| fromjson \| .iss' <<< "$JWT"`.                                                                                           |
| 400    | `invalid_grant`   | JWKS fetch failed, JWKS is stale, or the JWT was signed with a key not in the JWKS.                                              | For `inline` mode, update the issuer with the rotated keys. For `discovery` and `explicit_url`, confirm the JWKS endpoint is reachable on port 443; if the issuer recently rotated its signing key, see [Key rotation and caching](#key-rotation-and-caching). |
| 400    | `invalid_grant`   | The JWT `exp` claim is in the past (beyond the 30-second skew window).                                                           | Confirm your identity provider is projecting a fresh token and the SDK is re-reading the token file.                                                                                                                                                           |
| 400    | `invalid_grant`   | The JWT was verified but its claims do not satisfy the rule's `match` block.                                                     | Decode the JWT and compare each claim against the rule. `subject_prefix` is case-sensitive. `audience` requires an exact element match.                                                                                                                        |
| 400    | `invalid_grant`   | The `federation_rule_id` does not exist, is archived, or the JWT is not authorized for it (consolidated to prevent enumeration). | Confirm the rule ID in the Claude Console and that the rule has not been archived.                                                                                                                                                                             |

All `invalid_grant` failures return HTTP 400; the specific cause is logged server-side only and not exposed in the response.

### Common SDK-side failures

| Symptom                                                      | Cause                                                                                                                                                                       | Resolution                                                            |
| ------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| SDK reports "no credentials" instead of exchanging           | One of `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_SERVICE_ACCOUNT_ID`, or `ANTHROPIC_IDENTITY_TOKEN[_FILE]` is unset and no profile is active. | Set all four variables, or configure a profile.                       |
| SDK authenticates with an API key instead of federating      | `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` is set and wins precedence.                                                                                                   | Unset the key or token variable.                                      |
| `FileNotFoundError` on first request                         | The path in `ANTHROPIC_IDENTITY_TOKEN_FILE` does not exist. The SDK opens the file lazily at exchange time.                                                                 | Confirm the projected-token volume is mounted and the path matches.   |
| Token exchange succeeds but a Claude API request returns 403 | The minted token's scope does not grant access to that endpoint.                                                                                                            | Check the rule's `oauth_scope` against [OAuth scopes](#oauth-scopes). |
| Authentication fails with empty credential                   | A credential environment variable is exported but set to an empty string. Empty values still win their precedence slot.                                                     | Unset the variable with `unset VAR` rather than `VAR=""`.             |

## Troubleshoot a failed exchange

A `400 invalid_grant` response is intentionally opaque; the specific cause is logged server-side only.

<Tip>
  Start with the [authentication history page](https://platform.claude.com/settings/workload-identity-federation?tab=history) in the Claude Console. Recent exchange attempts surface the issuer and rule that were evaluated, the JWT claims that were inspected, and which validation step failed, which usually short-circuits the following checks.
</Tip>

If you still need to debug from the JWT itself, work through these checks in order:

<Steps>
  <Step title="Decode the JWT">
    Decode the assertion you sent so you can compare each claim against your issuer and rule configuration:

    ```bash cURL
    jq -rR 'split(".")[1] | gsub("-";"+") | gsub("_";"/") | @base64d | fromjson' <<< "$JWT"
    ```
  </Step>

  <Step title="Check iss matches the issuer">
    The decoded `iss` claim must equal the registered `issuer_url` byte for byte, including scheme, port, and any trailing slash. A mismatch on a single character fails verification.
  </Step>

  <Step title="Check aud matches the rule">
    The decoded `aud` claim must contain the rule's `audience` value as an exact match. When `aud` is an array, one element must match exactly.
  </Step>

  <Step title="Check sub and each claims entry">
    Compare `sub` against the rule's `subject_prefix` (case-sensitive; a trailing `*` is a prefix match, anything else is exact). Compare every key in the rule's `claims` map against the same-named top-level claim.
  </Step>

  <Step title="Check exp, nbf, and iat">
    `exp` must be in the future and `nbf`/`iat` must be in the past, within the 30-second skew window. If the workload host's clock has drifted, an otherwise valid token is rejected.
  </Step>

  <Step title="Check JWKS reachability">
    For `discovery` mode, fetch `<jwks.discovery_base or issuer_url>/.well-known/openid-configuration` over public HTTPS on port 443 and confirm `jwks_uri` resolves. For `explicit_url`, fetch the JWKS URL directly. For `inline`, confirm the issuer's signing key has not rotated since you registered the keys.

    If the issuer rotated its signing key and immediately started signing with it, exchanges can fail for up to a minute while Anthropic's JWKS cache refreshes. See [Key rotation and caching](#key-rotation-and-caching).
  </Step>
</Steps>

## JWKS source modes

When you register a federation issuer, the `jwks` field controls how Anthropic obtains the public keys used to verify JWT signatures from that issuer. It is a discriminated union keyed on `type`:

| `jwks.type`           | `jwks` shape                                                                                                                                       | Behavior                                                                                                                                                                                               | Use when                                                                                                                                                        |
| --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `discovery` (default) | `{ "type": "discovery", "discovery_base": "https://..." }` (`discovery_base` is optional; set it when the discovery URL differs from `issuer_url`) | Anthropic fetches `<discovery_base or issuer_url>/.well-known/openid-configuration`, reads `jwks_uri` from the discovery document, and fetches the JWKS from there.                                    | Your IdP serves a standard OIDC discovery document on the public internet. Most managed providers (EKS, GKE, Cloud Run, GitHub Actions, Entra ID) support this. |
| `explicit_url`        | `{ "type": "explicit_url", "url": "https://..." }`                                                                                                 | Anthropic fetches the JWKS directly from `url`. The `issuer_url` is used only for string comparison against the JWT `iss` claim and is never dialed.                                                   | Your IdP does not serve a discovery document, or discovery is internal-only but the JWKS is publicly reachable.                                                 |
| `inline`              | `{ "type": "inline", "keys": [...] }`                                                                                                              | You supply the array of JWK objects inline (the `keys` array from the JWKS document, not the wrapper object). Anthropic makes no outbound request. The `issuer_url` is used only for `iss` comparison. | Air-gapped environments, self-managed Kubernetes clusters with cluster-internal issuer URLs, or when you want explicit control over key rotation.               |

The discriminated union makes the companion fields mutually exclusive by construction. Both `discovery` and `explicit_url` also accept an optional `ca_cert_pem` string for issuers that serve TLS from a private CA.

### Key rotation and caching

In `discovery` and `explicit_url` modes, Anthropic caches the fetched JWKS. If your identity provider publishes a new signing key and immediately starts signing tokens with it, exchanges that present those tokens may fail with a signature error for up to one minute while the cache refreshes.

To avoid this window, publish a new signing key in the JWKS at least 15 minutes before your identity provider starts signing tokens with it, and keep the superseded key in the JWKS until tokens it signed have expired. Managed identity providers typically follow this discipline on their own. If you operate your own issuer (a self-managed Kubernetes cluster, a SPIRE OIDC discovery provider, or an Okta custom authorization server with a configured rotation cadence), confirm that your rotation policy publishes new keys ahead of first use.

<Warning>
  In `inline` mode there is no automatic key refresh. When your identity provider rotates its signing keys, you must update the issuer configuration with the new JWKS or all token exchanges will fail signature verification.
</Warning>
