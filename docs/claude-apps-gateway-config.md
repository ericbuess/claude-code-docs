> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude apps gateway configuration

> Reference for every gateway.yaml option: listener and TLS, OIDC, session, Postgres store, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry upstreams, model routing, managed policies, and telemetry.

A Claude apps gateway deployment is configured by one YAML file, conventionally `gateway.yaml`. The file defines everything the gateway does: where it listens, how developers sign in, where inference goes, and which policies and telemetry apply. This page is the reference for every option in that file.

To write your first one, start from the [quickstart](/docs/en/claude-apps-gateway#quickstart), which builds a minimal working config and runs it. Once you have a config you're happy with, the [deployment guide](/docs/en/claude-apps-gateway-deploy) covers containerizing and hosting it on Kubernetes, Cloud Run, or your own platform.

The gateway reads the file once, at startup, with `claude gateway --config /path/to/gateway.yaml`. Every option is validated against a schema at boot, so a malformed config fails at start with a field-level error rather than at first use.

The [complete example](#complete-example) at the end of this page exercises every section.

## File structure

Five sections are [required](#required-sections). Every other section is [optional](#optional-sections), and an omitted section takes its defaults. Unknown keys fail boot, so a typo surfaces as a named error rather than a silently ignored setting.

**Required sections:**

* [`listen`](#listen): bind address, public URL, TLS termination
* [`oidc`](#oidc): your identity provider (IdP), including issuer, client, claim mapping, and who may sign in
* [`session`](#session): the bearer tokens the gateway mints, with secret and lifetime
* [`store`](#store): PostgreSQL, for device grants and rate-limit counters
* [`upstreams`](#upstreams): where inference goes, whether Anthropic, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, or Microsoft Foundry

**Optional sections:**

* [`admin`](#admin): Admin API auth and retention for spend limits
* [`enforcement`](#enforcement): spend-limit fail-open or fail-closed behavior
* [`pricing`](#pricing): contracted rates and a discount multiplier for the spend meter
* [`models`](#models) and `auto_include_builtin_models`: admin-curated model list and per-upstream IDs
* [`managed`](#managed): managed settings policies by IdP group
* [`telemetry`](#telemetry): OTLP forwarding to your observability stack
* [`access_control`, `limits`, `timeouts`, `rate_limits`](#http-tuning): IP allow/deny, request size caps, upstream time-to-first-byte, and per-IP sign-in limits

## Secret expansion

Don't write secrets such as `client_secret`, `jwt_secret`, or `postgres_url` directly in `gateway.yaml`. Reference them with one of the forms below, and the gateway resolves the value at boot from an environment variable or a file:

| Form            | Resolves to                                                                                                                                                                                                                                                 | Use for                                                                |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `${VAR}`        | The environment variable `VAR`. Boot fails if undefined.                                                                                                                                                                                                    | Container environment variables, AWS Secrets Manager via env injection |
| `${file:/path}` | Contents of the file at that absolute path, trimmed. The reference must be the field's entire value: unlike `${VAR}`, it isn't expanded inside a longer string, so for a database password set `store.password` rather than embedding it in `postgres_url`. | Kubernetes Secret volume mounts, Vault Agent, SOPS                     |

## Required sections

### `listen`

The `listen` block controls where the gateway serves: the bind address and port, the externally visible origin, and optional TLS termination.

| Field                  | Required                  | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---------------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `host`                 | No                        | Bind address. Default `0.0.0.0`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `port`                 | No                        | Bind port. Default `8080`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `public_url`           | Unless `host` is loopback | The externally visible `https://` origin, used to build the IdP `redirect_uri` and discovery metadata. Required whenever `host` isn't a loopback address, whether TLS terminates at a proxy such as an ALB, Ingress, or Cloud Run or at the gateway itself through `tls`, because the gateway never derives its own origin from `X-Forwarded-*` headers; they are client-spoofable. Boot fails without it. `trusted_proxies` below governs client-IP resolution only. Also required to enable [telemetry](#telemetry), because the gateway builds the OTLP endpoint it pushes to clients from this URL. |
| `tls.cert` / `tls.key` | No                        | PEM paths if the gateway terminates TLS itself                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `trusted_proxies`      | No                        | CIDRs or IPs of load balancers in front of the gateway. When set, the gateway trusts `X-Forwarded-For` only from these peers and records the real client IP for per-IP rate limiting and audit. Equivalent to nginx `set_real_ip_from`.                                                                                                                                                                                                                                                                                                                                                                 |

### `oidc`

The `oidc` block connects the gateway to your identity provider and decides who can sign in. It names the issuer and OAuth client, maps the claims that carry email and groups, and restricts sign-in by email domain or group.

OpenID Connect (OIDC) is the SSO protocol the gateway uses with your identity provider; see [Identity provider setup](/docs/en/claude-apps-gateway-deploy#identity-provider-setup) for what to register on the IdP side.

| Field                           | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `issuer`                        | Yes      | OIDC discovery base. Must serve discovery at `/.well-known/openid-configuration`. Use HTTPS in production; the gateway accepts an `http://` issuer. A loopback issuer such as `http://localhost:8081` is rejected by the [SSRF guard](/docs/en/claude-apps-gateway-deploy#threat-model-summary) unless `CLAUDE_GATEWAY_ALLOW_LOOPBACK=1` is set in the gateway's environment.                                                                                                                                                                                                                             |
| `client_id` / `client_secret`   | Yes      | From your OAuth client registration                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| `allowed_email_domains`         | No       | Reject id\_tokens whose `email` claim isn't in one of these domains, case-insensitive. Defense-in-depth against multi-tenant IdP misconfiguration. Independent of this setting, an id\_token whose `email_verified` claim is explicitly `false` is always rejected.                                                                                                                                                                                                                                                                                                                                  |
| `allowed_groups`                | No       | Restrict sign-in to members of these IdP groups, matched against `groups_claim`. A user in an allowed email domain but in none of these groups is rejected. Requires the IdP to emit the groups claim. Matching is an exact, case-sensitive string comparison against the values in that claim, and the gateway doesn't expand nested groups: to admit members of a sub-group, list the sub-group here or configure the IdP to emit flattened membership.                                                                                                                                            |
| `groups_claim`                  | No       | Which id\_token claim carries group membership. Default `groups`. Microsoft Entra emits app roles under `roles`. Accepts a flat key or an RFC 6901 JSON Pointer such as `/resource_access/gateway/roles` for nested claims.                                                                                                                                                                                                                                                                                                                                                                          |
| `google_groups`                 | No       | Look up the signed-in user's groups through the Google Workspace Admin SDK Directory API, because Google's id\_token carries no groups claim. Set `service_account_json_path` to a service-account key file with domain-wide delegation on the `https://www.googleapis.com/auth/admin.directory.group.readonly` scope, and `admin_email` to a Workspace administrator the service account impersonates; the Directory API requires a real admin subject. Each user's group email addresses become their groups claim, so `allowed_groups` and `managed.policies.match.groups` match on group emails. |
| `email_claim`                   | No       | Which id\_token claim carries the user's email. Default `email`. Some IdPs, such as ADFS and Entra B2C, emit `upn` or `preferred_username` instead. Accepts a flat key, a JSON Pointer, or a list of fallback keys where the first present key is used.                                                                                                                                                                                                                                                                                                                                              |
| `scopes`                        | No       | Full override of the OIDC scopes the gateway requests. Default `[openid, profile, email, offline_access]`. Set when your IdP rejects scopes it doesn't recognize, or requires a custom scope to emit groups or email. Must include `openid`. Dropping `offline_access` disables refresh tokens, so developers re-run the browser login every `session.ttl_hours`. See [Identity provider setup](/docs/en/claude-apps-gateway-deploy#identity-provider-setup) for per-IdP scope recipes such as Google's refresh-token flow.                                                                               |
| `extra_auth_params`             | No       | Extra query parameters appended to the IdP authorization request, verbatim. This is the override mechanism for IdP-specific behavior, such as `access_type: offline` for Google refresh tokens, `domain_hint` for some Entra tenants, or `acr_values` for step-up flows. Cannot override the gateway-managed protocol params: `state`, `nonce`, `redirect_uri`, PKCE, `scope`, `response_type`, `response_mode`, and `client_id`.                                                                                                                                                                    |
| `userinfo_fallback`             | No       | When the id\_token omits email or groups, fetch them from `/userinfo`. Needed for Keycloak lightweight access tokens, the Okta org server, and ADFS minimal tokens. The id\_token stays authoritative; userinfo only fills gaps. Default `false`.                                                                                                                                                                                                                                                                                                                                                    |
| `use_pkce`                      | No       | Send a PKCE (S256) challenge on the authorization request. Default `true`. Set `false` only if your IdP rejects PKCE for this confidential client.                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `clock_skew_seconds`            | No       | Tolerate clock drift when validating id\_token time claims. Default `0`, which is strict. Raise if you see "token expired / not yet valid" errors right after sign-in due to host/IdP clock skew.                                                                                                                                                                                                                                                                                                                                                                                                    |
| `token_endpoint_auth_method`    | No       | Override the token-endpoint auth method. Accepts `client_secret_basic` or `client_secret_post`. Auto-negotiated by default.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `id_token_signed_response_alg`  | No       | Expected id\_token signing algorithm. Default `RS256`. Set for IdPs that sign with ES256, PS256, or EdDSA.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| `additional_authorized_parties` | No       | Extra `azp` values to accept beyond `client_id`, for Keycloak broker and token-exchange flows                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `discovery_url`                 | No       | Fetch the discovery document from this URL instead of deriving it from `issuer`, for IdPs behind a proxy that rewrites the issuer host. The path must contain `/.well-known/`.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `use_proxy`                     | No       | Send the gateway's own IdP requests through the forward proxy in `HTTPS_PROXY` or `HTTP_PROXY`, honoring `NO_PROXY`. Unset or `false`, those requests go direct. Requires v2.1.227 or later; see [IdP requests through a forward proxy](#idp-requests-through-a-forward-proxy) below.                                                                                                                                                                                                                                                                                                                |
| `form_action_origins`           | No       | Additional origins for the `/device` page's `Content-Security-Policy: form-action` directive. The gateway already allows `'self'` and the discovered `authorization_endpoint` origin, but Chrome enforces `form-action` against the entire redirect chain. If your IdP redirects through a second host, such as Azure AD federated to ADFS, hub-spoke Okta, or a corporate SSO interceptor, list every origin the authorization request may redirect through.                                                                                                                                        |
| `ca_cert_pem`                   | No       | The PEM-encoded CA certificate itself, not a path to a file. It replaces the system trust store for IdP requests only. To load a mounted file, write `${file:/etc/gateway/idp-ca.pem}`. Use for Keycloak or Dex behind corporate PKI.                                                                                                                                                                                                                                                                                                                                                                |

#### IdP requests through a forward proxy

The inference upstreams honor `HTTPS_PROXY` and `HTTP_PROXY` on every version. The gateway's own requests to the IdP, discovery, JWKS, token, and userinfo, go direct unless you set `oidc.use_proxy: true`, which requires v2.1.227 or later. When a proxy variable is set, `use_proxy` is unset, and the issuer isn't covered by `NO_PROXY`, the gateway keeps those requests direct and logs a notice at boot asking you to choose; `use_proxy: false` keeps them direct and silences the notice.

With `use_proxy: true`, the pod resolves each IdP endpoint's hostname itself and asks the proxy to `CONNECT` to the resolved IP address, so the proxy must accept `CONNECT` to the IP address of every host the discovery document names, not only the issuer. Use an `http://` proxy URL. `ca_cert_pem` and the [SSRF guard](/docs/en/claude-apps-gateway-deploy#threat-model-summary) apply on the proxied path as well.

### `session`

The `session` block shapes the bearer tokens the gateway mints after sign-in: the secret that signs them and how long they live.

| Field        | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                           |
| ------------ | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `jwt_secret` | Yes      | At least 32 bytes of entropy, for example from `openssl rand -base64 32`. Signs the gateway's HS256 bearer tokens. Accepts a single string or an array for rotation: index 0 signs and all entries verify. To rotate, prepend a new secret, wait `ttl_hours`, then drop the old one.                                                                                                                                  |
| `ttl_hours`  | No       | Gateway bearer token lifetime. Default `1`. The CLI silently refreshes before expiry when the IdP issues refresh tokens. A shorter lifetime deprovisions faster; a longer one makes fewer IdP round-trips. If your IdP can't issue refresh tokens because `offline_access` is unavailable, there is no silent refresh, so raise this to `8` or `12` to avoid sending developers back to the browser login every hour. |

### `store`

The `store` block points the gateway at its PostgreSQL database, which holds device grants and rate-limit counters.

| Field             | Required | Description                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `postgres_url`    | Yes      | `postgres://` or `postgresql://` URL. Required: the device-grant rendezvous, where the browser callback writes and the polling CLI reads, needs cross-replica state. The gateway runs its own schema migrations at boot and on upgrade, so the role needs rights to create and alter tables on the target schema. See [Upgrades](/docs/en/claude-apps-gateway-deploy#upgrades) and [Postgres](/docs/en/claude-apps-gateway-deploy#postgres). |
| `username`        | No       | Overrides the user in `postgres_url`                                                                                                                                                                                                                                                                                                                                                                                               |
| `password`        | No       | Database credential. Set it here rather than in `postgres_url` so the credential stays out of the URL. Accepts any characters and takes precedence over URL credentials.                                                                                                                                                                                                                                                           |
| `max_connections` | No       | Postgres connection-pool size per replica. Default `5`, which is conservative and friendly to shared databases. With [spend limits](#admin) enabled, the hot path does a few operations per inference request, so raise it for a dedicated database under load, and keep replicas × this below the database's `max_connections`.                                                                                                   |

For local development, point `postgres_url` at a throwaway Postgres container, for example `docker run --rm -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres`.

### `upstreams`

`upstreams` is an ordered list. The gateway forwards inference to the first upstream that resolves the requested model. On `5xx`, `429`, `401`, `403`, `404`, or timeout it fails over to the next; other `4xx` doesn't, because those errors are attributable to the request rather than the upstream. A `401` or `403` means the gateway's own credential failed against that upstream, and a `404` means that upstream doesn't serve the requested model, so a later upstream in the list still can.

Failover on `404` requires gateway v2.1.198 or later. Earlier releases returned the first `404` to the client even when a later upstream in the list served the model.

Multiple upstreams of the same provider must set a distinct `name:`.

Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry clients are built once at startup, and their SDKs refresh credentials internally, so rotating cloud credentials doesn't require a restart. Static Anthropic API keys and bearers are read at startup; see [Anthropic API](#anthropic-api).

#### Anthropic API

The minimal Anthropic upstream is an API key from the [Claude Console](https://platform.claude.com):

```yaml theme={null}
upstreams:
  - provider: anthropic
    auth:
      api_key: ${ANTHROPIC_API_KEY}
    # OR an OAuth bearer (e.g. a Workload-Identity-Federation-exchanged token):
    #   oauth_token: ${file:/var/run/secrets/anthropic-oauth-token}
    # base_url: https://api.anthropic.com   # default; override for a forward proxy
```

The two credential forms differ in the header they send:

* **`api_key`**: sends `x-api-key`. Rotate it in the Claude Console and update the env var.
* **`oauth_token`**: sends `Authorization: Bearer`. Use the bearer form when your org issues short-lived tokens instead of long-lived API keys. The bearer is read once at startup, so refresh by remounting the secret and restarting.

Instead of a static key or bearer, you can use Workload Identity Federation. Create a federation rule by following the [Workload Identity Federation guide](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation), then mount your workload's OIDC JWT as a file, such as a Kubernetes projected service-account token or a CI platform's id-token. The gateway exchanges the JWT for a short-lived bearer and refreshes it automatically. The token file is re-read on every exchange, so rotated projected tokens are picked up without a restart.

```yaml theme={null}
upstreams:
  - provider: anthropic
    auth:
      federation_rule_id: ${ANTHROPIC_FEDERATION_RULE_ID}
      organization_id: ${ANTHROPIC_ORGANIZATION_ID}
      identity_token_file: /var/run/secrets/anthropic/id-token
      # workspace_id: wrkspc_...       # required if the rule covers >1 workspace
      # service_account_id: svac_...   # optional expected-target check
```

<a id="per-user-identity-headers-for-a-proxy-you-run" />

##### Per-user identity headers for a proxy you run

You can point a `provider: anthropic` upstream's `base_url` at a proxy you run instead of at the Anthropic API. To tell that proxy which developer sent each request, set `forward_user_identity: true` on that upstream. The proxy can then attribute spend per developer. Requires a gateway running Claude Code v2.1.233 or later.

For example, for a proxy at `upstream-gateway.internal.example.com`:

```yaml theme={null}
upstreams:
  - provider: anthropic
    base_url: https://upstream-gateway.internal.example.com
    auth:
      api_key: ${PROXY_KEY}
    forward_user_identity: true        # default false
```

The gateway adds these headers to every request it forwards to that upstream.

| Header                        | Value                                                      |
| ----------------------------- | ---------------------------------------------------------- |
| `x-litellm-end-user-id`       | The developer's email, when the IdP supplied one.          |
| `x-claude-gateway-user-id`    | The developer's IdP subject, from the token's `sub` claim. |
| `x-claude-gateway-user-email` | The developer's email, when the IdP supplied one.          |

When the IdP token carries no email, the gateway sends only `x-claude-gateway-user-id` and omits the two email headers. If your IdP puts the email in a different claim, set [`oidc.email_claim`](#oidc) to that claim.

Set `forward_user_identity` only on an upstream whose `base_url` is a proxy you operate. The gateway sends developer emails to whatever server that `base_url` names. If the `base_url` is the Anthropic API, which is the default, the gateway refuses to start.

#### Amazon Bedrock

For the client-side Amazon Bedrock deployment that the gateway replaces or fronts, see [Claude Code on Amazon Bedrock](/docs/en/amazon-bedrock). The gateway-side upstream:

```yaml theme={null}
upstreams:
  - provider: bedrock
    region: us-east-1
    auth: {}                           # preferred: AWS default credential chain
    # OR explicit credentials:
    # auth:
    #   aws_access_key_id: ${AWS_AKID}
    #   aws_secret_access_key: ${AWS_SK}
    #   aws_session_token: ${AWS_ST}
    # OR a Bedrock API bearer token:
    # auth:
    #   aws_bearer_token: ${AWS_BEARER_TOKEN}
    # Override the bedrock-runtime endpoint for FIPS or VPC-endpoint deployments:
    # base_url: https://bedrock-runtime-fips.us-east-1.amazonaws.com
```

An empty `auth` block uses the AWS SDK's default credential chain: env vars, `~/.aws/credentials`, ECS task role, EC2 instance metadata, or IRSA on EKS. In production, give the gateway pod an IAM role instead of embedding static keys in a container image.

Explicit credentials must be complete: the gateway fails at boot when `aws_access_key_id` and `aws_secret_access_key` aren't set together, or when `aws_session_token` is set without them. Before v2.1.207, a partial `auth:` block passed validation.

| Setup           | How                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IAM permissions | Grant the gateway's principal `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on both the inference-profile ARNs and the underlying foundation-model ARNs. For the built-in catalog in US regions: `arn:aws:bedrock:<region>:<account>:inference-profile/us.anthropic.*` and `arn:aws:bedrock:*::foundation-model/anthropic.*`.                                                                                                           |
| Model access    | Amazon Bedrock enables model access by default in commercial regions. The remaining account-level gate is Anthropic's one-time use case form: if no one in your AWS account has submitted it, open the Amazon Bedrock console, select an Anthropic model from the Model catalog, and complete the form. See [Submit use case details](/docs/en/amazon-bedrock#1-submit-use-case-details) for the AWS Organizations form and the permissions the submitter needs. |
| EKS (IRSA)      | Create an IAM role with the policy above and a trust policy for your cluster's OIDC provider scoped to the gateway's service account. Annotate the service account with `eks.amazonaws.com/role-arn: arn:aws:iam::<acct>:role/claude-gateway`. `auth: {}` picks it up.                                                                                                                                                                                      |
| ECS / EC2       | Attach the IAM role to the task definition or instance profile. `auth: {}` picks it up.                                                                                                                                                                                                                                                                                                                                                                     |
| Anywhere else   | Pass credentials via the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_SESSION_TOKEN` env vars, or set them explicitly in `auth:` with `${VAR}` expansion                                                                                                                                                                                                                                                                                          |
| Region          | `region:` is the API endpoint region. Cross-region inference profiles route across the geo (US, EU, APAC) regardless of which one you pick. For non-US regions or provisioned-throughput ARNs, add a [`models:`](#models) block with the right per-upstream IDs.                                                                                                                                                                                            |

#### Claude Platform on AWS

Claude Platform on AWS serves the first-party Anthropic API on AWS infrastructure at `aws-external-anthropic.<region>.api.aws`. It uses first-party model IDs, honors `anthropic-beta` headers as sent, and serves `count_tokens`, so none of the Bedrock-specific translation applies. The `anthropicAws` provider requires Claude Code v2.1.198 or later; earlier gateway releases reject it at boot.

For the client-side deployment of the same platform, see [Claude Code on Claude Platform on AWS](/docs/en/claude-platform-on-aws). The gateway-side upstream:

```yaml theme={null}
upstreams:
  - provider: anthropicAws
    region: us-east-1
    workspace_id: wrkspc_...
    auth:
      api_key: ${ANTHROPIC_AWS_API_KEY}   # sent as x-api-key
    # OR SigV4 via the AWS default credential chain:
    # auth: {}
    # OR explicit SigV4 credentials:
    # auth:
    #   aws_access_key_id: ${AWS_ACCESS_KEY_ID}
    #   aws_secret_access_key: ${AWS_SECRET_ACCESS_KEY}
    # Override the derived endpoint:
    # base_url: https://aws-external-anthropic.us-east-1.api.aws
```

The platform runs in a separate AWS account from Amazon Bedrock and signs SigV4 requests for its own service name, `aws-external-anthropic`, so a Bedrock-scoped IAM role doesn't authorize it. An API key in `auth.api_key` takes precedence when SigV4 credentials are also set. An empty `auth` block uses the AWS SDK's default credential chain, the same chain the [Amazon Bedrock](#amazon-bedrock) upstream uses.

| Field                                                   | Required | Description                                                                                                                                        |
| ------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| `region`                                                | Yes      | AWS region, lowercase letters, digits, and hyphens. The gateway derives the endpoint from it as `https://aws-external-anthropic.<region>.api.aws`. |
| `workspace_id`                                          | Yes      | Sent as a header on every request; the platform requires it                                                                                        |
| `auth.api_key`                                          | No       | API key for the platform, sent as `x-api-key`. Not a bearer token: the two auth modes are an API key or SigV4.                                     |
| `auth.aws_access_key_id` / `auth.aws_secret_access_key` | No       | Explicit SigV4 credentials. Setting one without the other fails at boot. `auth.aws_session_token` is accepted alongside them.                      |
| `base_url`                                              | No       | Override the derived endpoint                                                                                                                      |

Because the platform resolves first-party model IDs, the built-in catalog routes to it with no [`models:`](#models) block. When you curate a `models:` list, key the entry `anthropicAws:` with the first-party ID.

#### Google Cloud Agent Platform

For the equivalent client-side setup, see [Claude Code on Google Cloud](/docs/en/google-vertex-ai). The gateway-side upstream:

```yaml theme={null}
upstreams:
  - provider: vertex
    region: us-east5
    project_id: example-prod
    auth: {}                           # preferred: Application Default Credentials
    # OR a service account key file:
    # auth: { service_account_json: /secrets/sa.json }
    # Override the aiplatform endpoint for Private Service Connect:
    # base_url: https://us-east5-aiplatform.p.googleapis.com
```

An empty `auth` block uses Application Default Credentials: `GOOGLE_APPLICATION_CREDENTIALS`, GCE metadata, or GKE Workload Identity. Service-account JSON key files are supported but discouraged; use Workload Identity or attach a service account to the GCE or Cloud Run instance.

Set `region: global` to use the [global endpoint for Google Cloud's Agent Platform](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) instead of a regional one. Google then routes each request to an available region, so you don't track per-region model availability. Setting a specific region pins every request to it.

| Setup                   | How                                                                                                                                                                                                       |
| ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IAM permissions         | Grant the gateway's service account `roles/aiplatform.user` on the project, or a custom role with `aiplatform.endpoints.predict`. Enable Google Cloud's Agent Platform API (`aiplatform.googleapis.com`). |
| Model access            | In Model Garden, enable the Claude models for your project. They publish to specific regions; check the model card for supported regions.                                                                 |
| GKE (Workload Identity) | Bind a GCP service account to the gateway's Kubernetes service account and annotate the KSA with `iam.gke.io/gcp-service-account: claude-gateway@<proj>.iam.gserviceaccount.com`. `auth: {}` picks it up. |
| Cloud Run / GCE         | Set the service's service account to one with `roles/aiplatform.user`. `auth: {}` picks it up.                                                                                                            |
| Anywhere else           | `auth: { service_account_json: /secrets/sa.json }`, the path to a JSON key file mounted as a secret. The field takes a file path, not the key contents, so no `${file:…}` expansion is involved.          |

#### Microsoft Foundry

For the client-side Microsoft Foundry deployment, see [Claude Code on Microsoft Foundry](/docs/en/microsoft-foundry). The gateway-side upstream:

```yaml theme={null}
upstreams:
  - provider: foundry
    resource: example-foundry              # https://example-foundry.services.ai.azure.com
    auth: { use_azure_ad: true }        # preferred: DefaultAzureCredential / Managed Identity
    # OR an API key:
    # auth:
    #   api_key: ${FOUNDRY_API_KEY}
```

`use_azure_ad: true` resolves through `DefaultAzureCredential`: Managed Identity on AKS, ACI, or App Service; the Azure CLI; or environment credentials. API keys work but are project-wide and don't rotate automatically. Microsoft Foundry's endpoint is derived from `resource:`; set the optional `base_url` to override it for sovereign clouds such as Azure Government.

| Setup                   | How                                                                                                                                                                                       |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RBAC                    | Grant the gateway's identity `Azure AI User` or `Cognitive Services User` on the Microsoft Foundry resource                                                                               |
| Deployments             | Microsoft Foundry uses admin-chosen deployment names, not canonical model IDs. Add a [`models:`](#models) block mapping each canonical ID to your deployment name.                        |
| AKS (workload identity) | Federate a User-Assigned Managed Identity with the cluster's OIDC issuer and bind it to the gateway's service account. `use_azure_ad: true` picks it up via `WorkloadIdentityCredential`. |
| ACI / App Service       | Enable system-assigned or user-assigned managed identity on the resource. `use_azure_ad: true` picks it up.                                                                               |
| Anywhere else           | `auth: { api_key: "${FOUNDRY_API_KEY}" }`. Quote `${…}` inside `{ }`.                                                                                                                     |

#### Multiple upstreams

The same provider can appear more than once with a distinct `name:`. This covers different regions, different accounts via different credential chains, provisioned throughput versus on-demand, and cross-provider fallback.

The gateway tries upstreams in order. `5xx`, `429`, `401`, `403`, `404`, timeouts, and missing-endpoint (`501`) fail over; other `4xx` doesn't.

`429` is per-upstream capacity, so provisioned-throughput (PT) exhaustion fails over to on-demand. `404` is per-upstream model availability, so an upstream that hasn't enabled a model doesn't block a later upstream that serves it. An upstream that can't resolve the requested model is skipped without a network round-trip.

This example routes a provisioned-throughput Amazon Bedrock allotment first, overflows to on-demand and a second account, and falls back to the Anthropic API last:

```yaml theme={null}
upstreams:
  # Primary: provisioned throughput in your home region.
  - name: bedrock-pt
    provider: bedrock
    region: us-east-1
    auth: {}
  # Overflow: on-demand cross-region.
  - name: bedrock-od
    provider: bedrock
    region: us-west-2
    auth: {}
  # Different account: a separate Bedrock allotment via assumed-role creds.
  - name: bedrock-acct2
    provider: bedrock
    region: us-east-1
    auth:
      aws_access_key_id: ${ACCT2_AKID}
      aws_secret_access_key: ${ACCT2_SK}
  # Last resort: direct Anthropic API.
  - name: anthropic-fallback
    provider: anthropic
    auth:
      api_key: ${ANTHROPIC_API_KEY}

# Per-upstream model IDs are keyed on the upstream's `name:`.
models:
  - id: claude-opus-4-8
    label: Claude Opus 4.8
    upstream_model:
      bedrock-pt: arn:aws:bedrock:us-east-1:111111111111:provisioned-model/abcdef
      bedrock-od: us.anthropic.claude-opus-4-8
      bedrock-acct2: us.anthropic.claude-opus-4-8
      anthropic-fallback: claude-opus-4-8
```

| Lever                  | How                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Different regions      | One Amazon Bedrock upstream per region, each with its own `region:`. With [`auto_include_builtin_models: true`](#models) the cross-region inference profiles route automatically; for region-pinned deployments use a `models:` block.                                                                                                                                                                                                                                    |
| Different accounts     | One Amazon Bedrock upstream per account, each with its own credentials in `auth:`. The default chain (`auth: {}`) uses the pod's identity; for a second account, set explicit credentials or a bearer token.                                                                                                                                                                                                                                                              |
| Provisioned throughput | Map the model to the provisioned-throughput ARN in `models:` for that upstream's name. Other upstreams keep the on-demand ID, so PT capacity is exhausted before failing over.                                                                                                                                                                                                                                                                                            |
| VPC / FIPS endpoints   | Set `base_url:` on the upstream to your VPC endpoint or FIPS endpoint URL                                                                                                                                                                                                                                                                                                                                                                                                 |
| Model-scoped routing   | Only a custom model `id`, one that isn't a built-in Claude model, skips the upstreams absent from its `upstream_model:` map. The gateway tries built-in models on every upstream in order and uses the provider's default ID where the map has no entry, so for built-in models the map changes which ID an upstream receives rather than whether it is tried; an upstream that rejects the ID follows the same [failover rules](#upstreams) as any other upstream error. |

Failing over between cloud providers, or to the direct Anthropic API, changes which agreement, geography, and other terms govern the request.

The CLI applies the same feature gating to gateways regardless of which upstream serves a given request, so failover doesn't send a body field an upstream would reject.

## Optional sections

### `admin`

Optional. Enables `/v1/organizations/spend_limits`, which mirrors Anthropic's public Admin API, and per-developer spend enforcement on `/v1/messages`. See [Spend limits](/docs/en/claude-apps-gateway-spend-limits) for how caps are set and enforced; this section covers the `gateway.yaml` keys that turn the feature on and tune it.

```yaml theme={null}
admin:
  # Named static API keys for the admin endpoints, sent as x-api-key.
  # The id appears in the audit log as admin-key:<id> so each key is
  # attributable. Array for rotation: add the new key, roll clients,
  # remove the old.
  write_keys:
    - { id: terraform, key: "${GATEWAY_ADMIN_WRITE_KEY_TF}" }
    - { id: ci,        key: "${GATEWAY_ADMIN_WRITE_KEY_CI}" }
  read_keys:
    - { id: reporting, key: "${GATEWAY_ADMIN_READ_KEY}" }
  # IdP groups granted full admin via the normal gateway JWT (no API key).
  admin_groups: [platform-finops]
  blocked_message: request an increase at https://go.example.com/claude-limits
```

| Field                     | Required | Description                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `write_keys`              | No       | Array of `{id, key}`. An `x-api-key` matching one of these can list, set, and delete spend limits. Key values must be at least 32 characters; `id`s must be unique across `read_keys` and `write_keys`.                                                                                                                                                      |
| `read_keys`               | No       | Array of `{id, key}`. Read-only: every `GET` endpoint, including listing caps, fetching one by ID, and reading [`/effective`](/docs/en/claude-apps-gateway-spend-limits#%2Feffective) and [`/audit`](/docs/en/claude-apps-gateway-spend-limits#%2Faudit).                                                                                                              |
| `admin_groups`            | No       | IdP group names. A gateway JWT whose `groups` claim includes one of these has full admin access, read and write, and audits as `oidc:<sub>`. Use this for human admins; use API keys for machines. An empty entry in this list stops the gateway at boot. See [Matcher values that stop the gateway at boot](#matcher-values-that-stop-the-gateway-at-boot). |
| `blocked_message`         | No       | Appended verbatim to the `429 billing_error` a blocked developer sees. Write the whole instruction, such as a URL or a Slack channel. When unset, the gateway sends only the default message. See [How enforcement works](/docs/en/claude-apps-gateway-spend-limits#how-enforcement-works).                                                                       |
| `audit_retention_days`    | No       | Default `365`. Older `admin_audit` rows are swept.                                                                                                                                                                                                                                                                                                           |
| `spend_retention_months`  | No       | Default `13`. `spend` counter rows older than this are swept. The default keeps a full year plus the current partial month for year-over-year reporting.                                                                                                                                                                                                     |
| `identity_retention_days` | No       | Default `90`. Last-seen TTL for `principal_emails` rows, which hold each developer's email, display name, and groups (PII). Deliberately shorter than spend retention so a deprovisioned identity ages out while its anonymous spend counters remain.                                                                                                        |
| `group_limit_mode`        | No       | `min` (default) or `max`. When a developer is in several groups with caps, `min` enforces the most restrictive and `max` the least. Used by both enforcement and `/effective`.                                                                                                                                                                               |

### `enforcement`

The `enforcement` block controls how spend-limit checks behave when the store is unavailable.

| Field                  | Required | Description                                                                                                                                                                                                                                                                                                                                                                    |
| ---------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `fail_closed_on_error` | No       | Default `false`. Spend enforcement fails open on a Postgres outage, so inference stays up. Set `true` to fail closed: over-cap developers are blocked, but so is everyone else if the store is unreachable. Requires an [`admin:`](#admin) block: spend enforcement only runs when `admin` is configured, and the gateway refuses to start if you set this `true` without one. |

### `pricing`

The `pricing` block tells the spend meter what to charge instead of USD list price, so caps and [`/effective`](/docs/en/claude-apps-gateway-spend-limits#%2Feffective) reflect your contracted rates. Amounts stay in USD and remain an estimate, not an invoice. Two prerequisites:

* Claude Code v2.1.227 or later on the gateway server. Earlier versions reject the unknown key at boot.
* An [`admin:`](#admin) block, because only the spend meter reads `pricing`. The gateway refuses to start with `pricing` set and no `admin`.

```yaml theme={null}
pricing:
  multiplier: 0.85
  overrides:
    - upstream: bedrock-eu
      model: claude-sonnet-4-6
      input: 3.30
      output: 16.50
      cache_read: 0.33
      cache_write: 4.125
```

| Field        | Required | Description                                                                                                                                                                |
| ------------ | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `multiplier` | No       | Default `1`. The meter multiplies every metered amount by this, whether list-priced or overridden, so `0.85` bills 85% of the price. Must be greater than 0 and at most 1. |
| `overrides`  | No       | Rows of `{upstream, model, input, output, cache_read, cache_write}` in USD per million tokens. All four rates are required and must be positive.                           |

How the meter matches an override row:

* A row replaces list price for requests that `upstream`, an [`upstreams[].name`](#upstreams), serves for `model`. That includes the higher [fast mode](/docs/en/fast-mode#understand-the-cost-tradeoff) rate, so fast and standard requests meter at the same four rates.
* A built-in ID such as `claude-sonnet-4-6`, matched like [`models[].id`](#models), covers every dated form, regional Amazon Bedrock form, or Google Cloud's Agent Platform form the meter prices as that model. Any other string, such as an alias or an inference-profile ARN, matches the ID the client sent or the string sent upstream, case-insensitively.
* Where rows overlap, the meter picks the most specific row rather than the first row: a row whose `model` is the exact model string sent upstream, then a row matching the exact ID the client sent, then a row naming the built-in model.
* An unknown upstream name fails boot, and so do two rows for one upstream that name the same model, including two spellings of one built-in model. The gateway warns at boot about a row no requestable model can use.
* Web-search requests stay at the \$0.01 list price; the multiplier still applies to them.

For per-region rates, give each region its own named upstream and one row per upstream.

### `models`

The `models` block is an optional admin-curated model list, served at `/v1/models` and used to translate model IDs per upstream. It is required for non-US Amazon Bedrock regions, Amazon Bedrock provisioned-throughput ARNs, and Microsoft Foundry deployment names.

```yaml theme={null}
auto_include_builtin_models: true   # false: expose only the list below
models:
  - id: claude-opus-4-8
    label: Claude Opus 4.8
    # description: optional text shown in clients that surface it
    upstream_model:
      anthropic: claude-opus-4-8
      bedrock: us.anthropic.claude-opus-4-8   # or an inference-profile ARN
      foundry: your-opus-deployment-name
```

Each key under `upstream_model` must match the `name` of a configured upstream, which defaults to the provider name. A key that matches no upstream fails boot, so omit the lines for providers you don't use.

### `managed`

The `managed` block defines role-based access policies keyed on IdP groups or email domain. Policies are evaluated in order; the first match is selected, then merged onto the `match: {}` catch-all base described below. They are served per-user at `GET /managed/settings` with ETag/304 caching.

```yaml theme={null}
managed:
  policies:
    # Specific groups first.
    - match: { groups: [eng-contractors] }
      cli:
        availableModels: [claude-sonnet-4-6]
        permissions: { deny: ["WebFetch", "WebSearch"] }
    # Default catch-all last: matches everyone who authenticated.
    - match: {}
      cli:
        availableModels: [claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5]
```

A `match: {}` catch-all, conventionally listed last, is treated as a base layer. Every other policy inherits any key it doesn't set from the catch-all, so per-role entries only need to list what differs from the org default. The merge rules depend on the key type:

* **Allow-lists**: `availableModels` and `permissions.allow`. A specific policy's list fully replaces the base's.
* **Deny-lists and hook arrays**: `permissions.deny`, `permissions.ask`, `disabledMcpjsonServers`, `deniedMcpServers`, `blockedMarketplaces`, and every `hooks` event-type array. These take the union of base and policy, so an org-wide deny or audit hook can't be accidentally dropped by a per-role override.
* **Record-typed keys**: `env`, `modelOverrides`, and `skillOverrides`. These shallow-merge, so a per-role `env` block overrides keys it sets and inherits the rest from the base.

`availableModels` is also enforced server-side at `/v1/messages`, so a denied model returns `400` regardless of what the client sends.

The gateway validates the `model` value itself before it relays a request, so a malformed value never reaches an upstream. It rejects the request with a `400` in two cases:

* When the value is missing or empty, the gateway rejects the request with the message `model is required`. That check requires a gateway running Claude Code v2.1.228 or later.
* When the value is present but isn't a string, the gateway rejects the request with the message `model must be a string`. Requires a gateway running Claude Code v2.1.221 or later.

| Matcher                                             | Behavior                                                                                                                         |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `match: {}`                                         | Matches every authenticated user. Start with one of these and add group-scoped policies above it later.                          |
| `match: { groups: [a, b] }`                         | Matches if the JWT's `groups` claim contains any of the listed groups. Case-sensitive: groups must match the IdP's exact casing. |
| `match: { email_domain: example.com }`              | Matches the part after the last `@` in the JWT's `email` claim, case-insensitive. Accepts one domain per policy.                 |
| `match: { groups: [a], email_domain: example.com }` | Both conditions must match                                                                                                       |

An authenticated user who matches no policy gets the gateway's defaults, which means every model in the catalog and no managed settings. Add a `match: {}` catch-all last if you want a guaranteed default policy.

<Note>
  The gateway keeps no user directory of its own. It authorizes each request from the user's IdP token, reading group membership from the token's `groups` claim and evaluating policies against it. There is no roster to enumerate and no accounts to pre-create, and therefore no SCIM endpoint, because there is nothing for SCIM to sync into.

  Run user and group lifecycle management at the source of truth, which is your IdP's native SCIM provisioning or a dedicated identity-governance platform. Membership and deprovisioning governed there flow into the gateway automatically through the token. If you want SCIM provisioning of Claude accounts themselves, that is a [Claude for Enterprise](/docs/en/admin-setup) capability.

  Two propagation clocks apply:

  * **Policy contents**: editing a policy and redeploying reaches connected clients on their next managed-settings poll, within an hour
  * **Group membership**: changing a user's group membership changes which policy matches them. This takes effect on the next session re-mint, meaning the next silent refresh, bounded by `session.ttl_hours`.
</Note>

#### Matcher values that stop the gateway at boot

At boot, the gateway checks the `match` block of every policy and the [`admin_groups`](#admin) list. Any of these values stops the gateway with an error that names the field:

* An empty `groups` list
* An empty entry in `groups` or in `admin_groups`
* An empty `email_domain`
* An `email_domain` that contains `@`, whitespace, or a comma. The gateway trims the value and strips one leading `@` before this check. Write one bare domain, such as `example.com`.

Before v2.1.232, the gateway started with these values. Each value had this effect:

* An empty `email_domain`: the gateway skipped the domain check, so a policy with an empty `email_domain` and no `groups` list matched every authenticated user
* An empty `groups` list: the policy matched no one
* An `email_domain` containing `@`, whitespace, or a comma: the policy matched no one
* An empty entry in `groups` or in `admin_groups`: the entry matched a user only when that user's IdP `groups` claim also contained an empty entry. In `admin_groups`, that match granted admin access. If your `admin_groups` list never contained an empty entry, no one gained admin access this way.

#### What goes in `cli`

Each `cli` value is a complete Claude Code `managed-settings.json` document, the same schema you would deploy via MDM or `/etc/claude-code/managed-settings.json`, expressed here as YAML. The CLI applies the delivered document at the managed tier, above user and project settings.

The gateway validates each document against the CLI's settings schema at boot, so an unrecognized top-level key or a recognized key with a malformed value fails boot with an error naming every offending key. Deliberately open parts of the schema still accept arbitrary values, because newer clients may recognize entries the gateway's schema doesn't. These open keys are `env`, `pluginConfigs`, and keys nested under `permissions`.

Because validation uses the schema bundled with the gateway's installed version, putting a top-level settings key introduced by a newer Claude Code release into managed config requires upgrading the gateway first. Smoke-test a new policy on one client before rolling it out.

The full key reference is in [Claude Code settings](/docs/en/settings#available-settings). The keys most operators reach for first:

```yaml theme={null}
managed:
  policies:
    - match: {}
      cli:
        # Model access (also enforced server-side at /v1/messages)
        availableModels: [claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5]

        # Permission policy
        permissions:
          deny:
            - "WebFetch"
            - "Read(./.env)"
            - "Read(./secrets/**)"
          disableBypassPermissionsMode: disable   # blocks --dangerously-skip-permissions
        allowManagedPermissionRulesOnly: true     # ignore user/project permission rules

        # Environment pushed into the CLI process. DISABLE_UPDATES blocks
        # background and manual updates; DISABLE_AUTOUPDATER stops only
        # background updates.
        env:
          DISABLE_UPDATES: "1"                    # pin versions via your own distribution

        # Org-wide hooks. Hook commands run on developer machines, not the
        # gateway, so the path must exist on every client OS in the policy.
        hooks:
          PostToolUse:
            - matcher: "Edit|Write"
              hooks:
                - { type: command, command: /usr/local/bin/audit-edit.sh }
```

| Key                                        | Enforced by   | Effect                                                                                                                                                                                                   |
| ------------------------------------------ | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `availableModels`                          | Gateway + CLI | Model allowlist. Also checked at `/v1/messages`, so a patched client can't bypass it.                                                                                                                    |
| `permissions.allow` / `.deny`              | CLI           | Tool and command rules. See [Permissions](/docs/en/permissions).                                                                                                                                              |
| `permissions.disableBypassPermissionsMode` | CLI           | Set to `disable` to block [`bypassPermissions`](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode), the mode that skips permission prompts, and the `--dangerously-skip-permissions` flag |
| `allowManagedPermissionRulesOnly`          | CLI           | When `true`, user and project permission rules are ignored; only rules from this document apply                                                                                                          |
| `env`                                      | CLI           | Environment variables merged into the CLI process. Use for telemetry, auto-update, and model-name overrides.                                                                                             |
| `hooks`                                    | CLI           | Org-wide [hooks](/docs/en/hooks)                                                                                                                                                                              |

Because these settings arrive over the network, the CLI shows each developer a security approval dialog before applying the settings listed below:

* `hooks`
* `env` variables that require the developer's approval, such as proxy and base-URL variables
* shell-execution settings such as `apiKeyHelper` and `statusLine`
* the sandbox binary settings `sandbox.bwrapPath`, `sandbox.socatPath`, and `sandbox.ripgrep`
* managed CLAUDE.md content

[Approval memory](/docs/en/server-managed-settings#approval-memory) covers how long an approval lasts and when the dialog appears again.

Claude Code applies some delivered `env` variables without showing the developer the approval dialog, such as model selection settings and numeric limits. Other delivered variables can require the developer's approval before they take effect; a non-empty proxy, base-URL, or `OTEL_EXPORTER_OTLP_ENDPOINT` value always does. When a delivered variable needs approval, the dialog names it.

[Environment variables and the approval dialog](/docs/en/server-managed-settings#environment-variables-and-the-approval-dialog) has the details, including four privacy toggles whose delivered value decides whether they need approval. Before v2.1.218, Claude Code applied fewer variables without asking the developer, so more delivered variables triggered the dialog.

The gateway's [telemetry](#telemetry) configuration pushes `OTEL_EXPORTER_OTLP_ENDPOINT`, so setting `telemetry.forward_to` triggers the dialog on each interactive client. The dialog protects the developer's machine from a compromised or hostile gateway, not the organization from the developer.

A non-interactive run with the `-p` flag can't show the dialog. It applies the pushed settings for that run only and doesn't record them as approved, so the developer's next interactive session still shows the dialog. Before v2.1.207, a non-interactive run saved the settings as approved and no later interactive session showed the dialog for them.

If a developer declines, Claude Code exits rather than applying the policy. Pushing a new hook, or any env var that triggers the dialog, to a broad policy therefore means an approval prompt on every matching developer's next startup.

The `cli` key was named `settings` in earlier releases. That spelling is still accepted as an alias, but new deployments should use `cli`.

#### Claude Desktop overlay

If your organization also deploys [Claude Desktop](/docs/en/desktop), the same gateway serves both clients. Point `bootstrapUrl`, in Claude Desktop's [managed configuration](https://claude.com/docs/third-party/claude-desktop/configuration), at `<listen.public_url>/user/bootstrap`. Claude Desktop derives the OAuth issuer from that URL, runs the same device-code sign-in against this gateway, and fetches its configuration from the response.

<Note>
  Requires Claude Code v2.1.203 or later on the gateway server, and an explicit opt-in: `/user/bootstrap` returns 404 unless the policy matching the user carries a `desktop` key. An empty `desktop: {}` opts a policy in, and a `desktop` key on the `match: {}` base layer opts in every policy that inherits it. The audit log records each request as `desktop_bootstrap.serve` or `desktop_bootstrap.denied`.
</Note>

The gateway derives much of the response from the matched policy's `cli` block and from top-level gateway config:

* The model list, from `availableModels`
* Disabled tools, from bare tool-name `permissions.deny` entries. If you set `disabledBuiltinTools` in the policy's `desktop` block, the gateway serves the union of your value and the derived list, so you can disable more tools this way but can't re-enable one you disabled through `permissions.deny`
* The egress allowlist, from `sandbox.network.allowedDomains`. If you set `coworkEgressAllowedHosts` in the policy's `desktop` block, the gateway uses that value instead of the derived list
* An OTLP endpoint that points at the gateway itself, which fans out to your destinations, included when [`telemetry`](#telemetry) forwarding is configured

To set `disabledBuiltinTools` or `coworkEgressAllowedHosts` in a policy's `desktop` block, you need Claude Code v2.1.232 or later on the gateway server.

The gateway omits keys with no Claude Desktop equivalent, such as `hooks` and scoped permission rules like `Bash(npm *)`, from the bootstrap response.

Add the optional `desktop` block alongside `cli` to set Claude Desktop settings directly. Write settings from Claude Desktop's [managed configuration reference](https://claude.com/docs/third-party/claude-desktop/configuration) as flat key names. Leave out keys Claude Desktop reads only from MDM or local files, such as `bootstrapUrl`; the gateway rejects them at boot. Before v2.1.232, the gateway accepted a fixed list of 11 feature-gate keys, such as `chatTabEnabled` and `disableAutoUpdates`, and rejected every other key at boot. Before v2.1.227, the gateway also rejected `chatTabEnabled` and `chatAdvancedFileAnalysisEnabled` at boot.

```yaml theme={null}
managed:
  policies:
    - match: { groups: [eng-contractors] }
      cli:
        availableModels: [claude-sonnet-4-6]
      desktop:
        isLocalDevMcpEnabled: false
        disableAutoUpdates: true
        banner: { text: "Contractor build: internal use only" }
```

Every key is optional; Claude Desktop applies its own default for any key you omit. The gateway validates each `desktop` block at boot against the configuration schema Claude Desktop itself uses, so a mistake surfaces at gateway start as an error naming the key rather than reaching every connected desktop. The gateway fails at boot when a block contains:

* An unknown key
* A recognized key whose value Claude Desktop would reject or silently drop, such as an empty value or a misspelled sub-key inside a nested entry
* A key the gateway computes itself: the inference connection, the model list, and the OTLP relay. Configure those through [`upstreams`](#upstreams), [`models`](#models), and the [`telemetry`](#telemetry) section's `forward_to`.
* A legacy alias of a current key. In the boot error, the gateway names the canonical key to write.

As with the `cli` block, the gateway validates against the schema bundled with its installed version. To deliver a setting introduced by a newer Claude Desktop release, upgrade the gateway first.

The gateway fills in keys a policy's `desktop` block doesn't set from the `match: {}` catch-all's `desktop` block, the same way it fills in a policy's `cli` block from the base. If you set `disabledBuiltinTools` or `builtinToolPolicy` in both the base and a role policy, the gateway keeps the base's restriction:

* `disabledBuiltinTools`: the gateway uses the union of the base's list and the policy's list
* `builtinToolPolicy`: if you set a tool to a value other than `allow` in the base, the gateway keeps that value even if you set `allow` for the same tool in a role policy

For every other key, if you set it in the role policy, the gateway uses the role policy's value. The gateway replaces an array or a nested object such as `banner` whole, so if you set `banner.text` in a role policy, the gateway drops the base's `banner.backgroundColor`.

If you don't deploy Claude Desktop, leave `desktop` out of your policies entirely; the gateway then returns 404 from `/user/bootstrap` for every user.

#### Precedence with other managed sources

If a device also has a local `managed-settings.json` or MDM-delivered policy, the managed sources don't merge, with two per-key exceptions:

* The `env` block, in Claude Code v2.1.223 or later
* The [cross-source lock keys](/docs/en/settings#precedence-within-the-managed-tier)

Both are covered in the list later in this section. The highest-priority source provides all policy settings, ranked in this order with highest priority first:

1. Gateway-delivered settings
2. MDM, via the HKLM registry on Windows or a plist on macOS
3. The `managed-settings.json` file
4. The HKCU registry, on Windows only

When an MDM or file-based source wins and configures a [`policyHelper`](/docs/en/settings#compute-managed-settings-with-a-policy-helper), the helper's output replaces that source and neither per-key exception applies. A `policyHelper` in those sources doesn't run while the gateway delivers a non-empty configuration.

Embedding hosts such as [Claude Desktop](/docs/en/desktop) can supply policy through the SDK `managedSettings` option. Whether it applies depends on the machine's managed configuration:

* On machines with an admin-deployed managed source, it is ignored unless the highest-priority source opts in with [`parentSettingsBehavior: "merge"`](/docs/en/settings#available-settings).
* It is never merged when an MDM or file-based source wins and configures a [`policyHelper`](/docs/en/settings#compute-managed-settings-with-a-policy-helper).
* When merged, it passes through a restrictive-only allowlist. [Restrict parent settings](/docs/en/claude-apps-gateway#restrict-parent-settings) lists which allow-direction settings still apply without the `allowManaged*Only` locks.

The following keys are honored when any admin source above the user-writable HKCU tier sets them, regardless of which source provides the rest of the policy. When an MDM or file-based source wins and configures a [`policyHelper`](/docs/en/settings#compute-managed-settings-with-a-policy-helper), the helper's output is the only source these checks read:

* `sandbox.network.allowManagedDomainsOnly` and `sandbox.filesystem.allowManagedReadPathsOnly`: when locked, the corresponding allowlists are unioned across sources
* [`allowAllClaudeAiMcps`](/docs/en/settings#available-settings): allow-only override for the claude.ai MCP server allowlist
* `sandbox.bwrapPath` and `sandbox.socatPath`: filesystem paths to the [sandbox](/docs/en/sandboxing) helper binaries
* [`sandbox.ripgrep`](/docs/en/settings#sandbox-settings): the `ripgrep` binary the sandbox uses
* [`forceRemoteSettingsRefresh`](/docs/en/server-managed-settings): blocks startup until remote managed settings are freshly fetched, so an MDM or file policy that sets it is honored even when a cached remote payload that lacks the key is the highest-priority source
* `env`: each variable comes from the highest-priority admin source that defines it, and lower admin sources fill in variables the higher sources leave unset. The telemetry unit and credential-paired routing variables follow their own rules; see [Per-key exceptions across managed sources](/docs/en/server-managed-settings#per-key-exceptions-across-managed-sources). Requires Claude Code v2.1.223 or later

Every other key, including `disableBypassPermissionsMode`, comes from the highest-priority source only. One [parent-settings](/docs/en/claude-apps-gateway#restrict-parent-settings) check reads every admin source: when any admin source sets `allowManagedPermissionRulesOnly`, Claude Code drops parent-supplied permission allow rules and `additionalDirectories`. The key's effect on the developer's own rules still follows the highest-priority source.

A `forceLoginOrgUUID` or `allowedMcpServers` value in the highest-priority admin source blocks a parent-supplied one and is the value Claude Code enforces. A value in a non-winning admin source neither applies nor blocks the parent's. Before v2.1.223, a value in any admin source blocked the parent's.

See [Settings precedence](/docs/en/settings#settings-precedence) for the same rules on the settings page.

Gateway policies apply to every Claude Code invocation on the machine, including non-interactive `claude -p` runs and sessions spawned by the Agent SDK. If the gateway is unreachable at startup, signed-in sessions exit with an error rather than running without their policy.

<Warning>
  At boot, the gateway rejects `mcpServers` inside a policy's `cli` block. You can't distribute MCP servers per group to Claude Code clients; deploy MCP servers via the file-based `managed-mcp.json` on each device or let developers add them locally. You can deliver Claude Desktop's `managedMcpServers` setting to Claude Desktop clients through a policy's `desktop` block. To set it, you need Claude Code v2.1.232 or later on the gateway server.
</Warning>

### `telemetry`

The CLI sends OpenTelemetry Protocol (OTLP) over HTTP metrics, logs, and, when enabled, traces to the gateway, which relays them verbatim to each configured destination. See [Monitoring usage](/docs/en/monitoring-usage) for the metrics and events the CLI emits.

The CLI stamps each export with the authenticated user's identity, read from the gateway-issued JWT: the `user.id`, `user.email`, and `user.groups` attributes. Per-developer cost and usage attribution therefore works with no developer-side configuration.

```yaml theme={null}
telemetry:
  forward_to:
    - url: https://otel-collector.internal.example.com
      headers:
        Authorization: ${OTLP_TOKEN}
      # Per-signal opt-in. Default: metrics only.
      metrics: true
      logs: false
      traces: false
    - url: https://api.datadoghq.com/api/v2/otlp
      headers:
        DD-API-KEY: ${DD_API_KEY}
```

<Warning>
  Each destination opts into `metrics`, `logs`, and `traces` independently, and the default is metrics only. The signals differ in sensitivity:

  * **Metrics**: aggregate counters such as token counts, request counts, and latency
  * **Logs and traces**: can carry full bash commands, tool inputs, and file paths, covering anything Claude Code does on a developer's machine

  Enable logs and traces only on destinations with the access controls and retention policy that data warrants.
</Warning>

Each `forward_to` URL must use `https://`, with one exception for a collector on the gateway's own loopback interface:

* `http://localhost:<port>` passes config validation, but the [SSRF guard](/docs/en/claude-apps-gateway-deploy#threat-model-summary) blocks every export with `ECONNREFUSED_SSRF` unless you set `CLAUDE_GATEWAY_ALLOW_LOOPBACK=1` in the gateway's environment
* `http://127.0.0.1:<port>` or `http://[::1]:<port>` fails boot unless that variable is set

For an in-cluster collector, expose it over HTTPS at its own internal address, or run it as a sidecar with the variable set.

Telemetry is off in the CLI by default. Configuring `telemetry.forward_to` together with `listen.public_url` turns it on. The gateway pushes six env vars to every connected client through `/managed/settings`:

* `CLAUDE_CODE_ENABLE_TELEMETRY=1`
* `OTEL_METRICS_EXPORTER=otlp`
* `OTEL_LOGS_EXPORTER=otlp`
* `OTEL_TRACES_EXPORTER=otlp`
* `OTEL_EXPORTER_OTLP_ENDPOINT=<public_url>`
* `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf`

The pushed endpoint is built from the public URL, so metrics and logs need no OTEL configuration from developers or policies. The pushed configuration is applied at the managed tier, overriding `OTEL_*` variables a developer sets locally. Whether or not the gateway pushes these variables, a CLI signed in through `/login` that has OTLP/HTTP export enabled sends its exports to the gateway rather than to a locally configured endpoint, and without a `forward_to` destination for a signal the gateway accepts and discards it; if you already collect Claude Code telemetry directly, add your collector as a `forward_to` destination.

[Traces](/docs/en/monitoring-usage#traces-beta) additionally require `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1` on each client. The gateway doesn't push that variable, so set it through a managed policy's `env` block. It isn't among the variables Claude Code applies without the developer's approval, so delivering it through a policy is covered by the same [security approval dialog](#managed) that the pushed OTLP endpoint already triggers.

Both protobuf and JSON OTLP encodings are relayed, and any OpenTelemetry-compatible backend works as a destination.

### HTTP tuning

Four optional top-level blocks, `access_control`, `limits`, `timeouts`, and `rate_limits`, tune the HTTP surface. The defaults suit most deployments.

| Block            | Key                                            | Default  | Description                                                                                                                                                                                                                                                                                                                         |
| ---------------- | ---------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `access_control` | `allow_cidrs` / `deny_cidrs`                   | empty    | Inbound IP allow/deny by client address, after `trusted_proxies` resolution. `deny_cidrs` is checked first; a client it matches is rejected even if `allow_cidrs` also matches. If `allow_cidrs` is non-empty the gateway is default-deny. `/healthz` and `/readyz` are exempt from `allow_cidrs`.                                  |
| `limits`         | `max_request_bytes`                            | 32 MiB   | Max inbound request body; oversize requests get `413` before the body is buffered. Raise for large file or image requests.                                                                                                                                                                                                          |
| `limits`         | `max_request_header_bytes`                     | unset    | When set, oversize headers return `431`                                                                                                                                                                                                                                                                                             |
| `limits`         | `max_url_length`                               | unset    | When set, an over-long URL returns `414`                                                                                                                                                                                                                                                                                            |
| `timeouts`       | `upstream_ttfb_ms`                             | 120000   | Max wait for the upstream's response headers (time to first byte). The response body then streams with no wall-clock cap. Applies to the direct Anthropic upstream path; every other provider is bounded by its provider SDK's own timeout.                                                                                         |
| `rate_limits`    | `device_authorization.max` / `.window_seconds` | 30 / 600 | Per-IP rate limit on the unauthenticated device-authorization endpoint. Raise for a large org behind a shared egress IP or NAT. These limits apply only to the device-grant sign-in flow, not to `/v1/messages` inference. See [User-code brute-force resistance](/docs/en/claude-apps-gateway-deploy#user-code-brute-force-resistance). |
| `rate_limits`    | `device_verify.max` / `.window_seconds`        | 10 / 600 | Per-IP rate limit on `user_code` submissions at `/device`                                                                                                                                                                                                                                                                           |

## Complete example

This full reference config exercises every core section; the [HTTP tuning blocks](#http-tuning) keep their defaults. Copy it, delete what you don't need, and fill in your values. The config in the [Quickstart](/docs/en/claude-apps-gateway#quickstart) is a minimal version of this.

```yaml gateway.yaml theme={null}
# Run with:
#   claude gateway --config gateway.yaml
#
# Operational log verbosity is controlled by the CLAUDE_GATEWAY_LOG_LEVEL
# environment variable (debug | info | warn | error; default info). debug
# also logs the claim names in each id_token, for groups_claim diagnosis.
# It does not affect audit events, which are always emitted.

listen:
  host: 0.0.0.0
  port: 8080
  public_url: https://claude-gateway.internal.example.com
  # Omit the tls block when running behind a TLS-terminating ingress.
  # tls:
  #   cert: /certs/gateway.crt
  #   key: /certs/gateway.key
  # trusted_proxies:
  #   - 10.0.0.0/8

oidc:
  issuer: https://example.okta.com
  client_id: 0oa1example2
  client_secret: ${OIDC_CLIENT_SECRET}
  allowed_email_domains:
    - example.com
  # Required when the issuer is the Okta org server, whose id_tokens
  # can omit email and groups; the gateway fills them from /userinfo.
  userinfo_fallback: true
  # allowed_groups: [claude-code-users]
  # Okta emits groups only when the `groups` scope is requested and the
  # app's groups claim filter allows them. The contractors policy below
  # matches on groups, so the scope is requested here.
  scopes: [openid, profile, email, offline_access, groups]
  # extra_auth_params: { access_type: offline, prompt: consent }  # Google
  # groups_claim: groups          # Entra app roles: use `roles`
  # email_claim: email

session:
  jwt_secret: ${GATEWAY_JWT_SECRET}   # openssl rand -base64 32
  # ttl_hours: 1

store:
  postgres_url: ${GATEWAY_POSTGRES_URL}
  # max_connections: 5

# Enables /v1/organizations/spend_limits (mirrors the Anthropic Admin API)
# and per-developer spend enforcement on /v1/messages. Omit to disable.
# Caps themselves are set via the admin API, not here.
# admin:
#   write_keys:
#     - { id: terraform, key: "${GATEWAY_ADMIN_WRITE_KEY_TF}" }
#   read_keys:
#     - { id: reporting, key: "${GATEWAY_ADMIN_READ_KEY}" }
#   admin_groups: [platform-finops]
#   blocked_message: request an increase at https://go.example.com/claude-limits
#   # audit_retention_days: 365
#   # spend_retention_months: 13
#   # identity_retention_days: 90
#   # group_limit_mode: min

# enforcement:
#   fail_closed_on_error: false

# Meter at contracted rates instead of USD list price. Requires admin:.
# Rates below are placeholders, not real contract prices.
# pricing:
#   multiplier: 0.85
#   overrides:
#     - { upstream: anthropic, model: claude-sonnet-4-6, input: 3.30, output: 16.50, cache_read: 0.33, cache_write: 4.125 }

upstreams:
  - provider: anthropic
    auth:
      api_key: ${ANTHROPIC_API_KEY}

  # - provider: bedrock
  #   region: us-east-1
  #   auth: {}

  # - provider: anthropicAws
  #   region: us-east-1
  #   workspace_id: wrkspc_...
  #   auth:
  #     api_key: ${ANTHROPIC_AWS_API_KEY}

  # - provider: vertex
  #   region: us-east5
  #   project_id: example-prod
  #   auth: {}

  # - provider: foundry
  #   resource: example-foundry
  #   auth: { use_azure_ad: true }

auto_include_builtin_models: true
models:
  - id: claude-opus-4-8
    label: Claude Opus 4.8
    upstream_model:
      anthropic: claude-opus-4-8
      # bedrock: us.anthropic.claude-opus-4-8
      # anthropicAws: claude-opus-4-8
      # vertex: claude-opus-4-8
      # foundry: <your-opus-deployment-name>
  - id: claude-sonnet-4-6
    label: Claude Sonnet 4.6
    upstream_model:
      anthropic: claude-sonnet-4-6
  - id: claude-haiku-4-5
    label: Claude Haiku 4.5
    upstream_model:
      anthropic: claude-haiku-4-5

managed:
  policies:
    - match: { groups: [contractors] }
      cli:
        availableModels: [claude-haiku-4-5]
        # Constrain the Default picker option to availableModels instead of
        # the tier default, so contractors don't get a 400 on the default.
        enforceAvailableModels: true
        # allow auto-approves these tools; it does not block the rest.
        # Add deny rules to restrict tools.
        permissions: { allow: [Read, Grep] }
    - match: {}
      cli:
        availableModels: [claude-opus-4-8, claude-sonnet-4-6, claude-haiku-4-5]
        permissions:
          allow: [Read, Grep, Bash, Edit]
          deny: ["WebFetch"]
        env: { HTTP_PROXY: http://proxy.example.com:8080 }

telemetry:
  forward_to:
    - url: https://otel.internal.example.com:4318
      headers:
        Authorization: Bearer ${OTEL_TOKEN}
```

## Client-side managed settings

Everything above configures the gateway server. You point developer machines at the gateway separately, on each device, through Claude Code's [managed settings](/docs/en/settings#settings-files). The gateway can't push the login keys itself, because they're what tell the client where the gateway is.

For the CLI, set these keys in the per-OS `managed-settings.json`. The two login keys route each developer's `/login` to your gateway:

```json theme={null}
{
  "forceLoginMethod": "gateway",
  "forceLoginGatewayUrl": "https://claude-gateway.internal.example.com",
  "parentSettingsBehavior": "merge"
}
```

`parentSettingsBehavior: "merge"` keeps Claude Desktop's delivery of the egress allowlist to its embedded Claude Code sessions working; [Deliver policy to Claude Desktop sessions](/docs/en/claude-apps-gateway#deliver-policy-to-claude-desktop-sessions) explains the mechanism and where the opt-in must sit.

Deploy the `managed-settings.json` file to each device, typically via your MDM platform. The file path differs by platform:

| Platform      | Path                                                                                                                          |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| macOS         | `/Library/Application Support/ClaudeCode/managed-settings.json`, or the `com.anthropic.claudecode` managed preferences domain |
| Linux and WSL | `/etc/claude-code/managed-settings.json`                                                                                      |
| Windows       | `C:\Program Files\ClaudeCode\managed-settings.json`, or Group Policy via the HKLM registry                                    |

A registry policy on Windows or a managed-preferences plist on macOS replaces the `managed-settings.json` file rather than merging with it, apart from the [exception keys and cross-source checks above](#precedence-with-other-managed-sources). All three keys in this snippet follow the highest-priority-source rule, so fleets that deliver policy through Group Policy or configuration profiles must put all three in that mechanism instead.

For Claude Desktop, set the `bootstrapUrl` key in Claude Desktop's own [managed configuration](https://claude.com/docs/third-party/claude-desktop/configuration) to `<listen.public_url>/user/bootstrap`. The sign-in flow and per-group policy then match the CLI's once a policy opts in server-side with a `desktop` key; without the opt-in, `/user/bootstrap` returns 404. See [Claude Desktop overlay](#claude-desktop-overlay) for the server-side half.

`forceLoginGatewayUrl`, and the `"gateway"` value of `forceLoginMethod`, are honored only from the admin-controlled managed tier. A developer setting them in their own `~/.claude/settings.json` has no effect.

## Related

* [Claude apps gateway overview](/docs/en/claude-apps-gateway): quickstart and developer connection
* [Deployment guide](/docs/en/claude-apps-gateway-deploy): IdP setup, container image, Kubernetes and Cloud Run, and operations
* [Spend limits](/docs/en/claude-apps-gateway-spend-limits): per-developer caps and the Admin API
