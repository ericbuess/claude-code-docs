> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude apps gateway deployment and operations

> Register the gateway with your IdP, build the container, deploy on Kubernetes or Cloud Run, and operate it: health checks, secret rotation, upgrades, and security.

This page covers the operational side of running [Claude apps gateway](/en/claude-apps-gateway): registering an OAuth client in your identity provider (IdP), deploying the gateway as a container, and running it day-to-day. For every option in the `gateway.yaml` file the gateway reads at boot, see the [Configuration reference](/en/claude-apps-gateway-config).

A production deployment follows four steps in order, and the sections below match them. The first two are where you make choices; the second two are reference material to consult once it's running.

1. [Set up your identity provider](#identity-provider-setup): register the OAuth client and check the per-IdP notes for Okta, Entra, and Google
2. [Deploy the gateway](#deployment): build a pinned container image and run it on Kubernetes, Cloud Run, or your own platform. This section also covers cost, bypass, multiple-gateway, and serverless decisions
3. [Set up operations](#operations): logs, health probes, outage behavior, secret rotation, and upgrades. Reference for when you're setting up monitoring and runbooks
4. [Review the security posture](#security): what data flows where, the threat model, and compliance answers. Reference for a security review

If a sign-in or boot fails along the way, go straight to [Troubleshooting](#troubleshooting), which is keyed on the error you see.

<Note>
  **Deploy on your private network.** Claude Code only connects to a gateway whose address is private. This is a security guard, because a trusted gateway can push settings that run commands on developer machines. Put the gateway behind an internal load balancer or VPN and give it a hostname that resolves to private IPs only.
</Note>

## Identity provider setup

Register a confidential OAuth/OpenID Connect (OIDC) web application with a single redirect URI, `https://<gateway>/oauth/callback`, and assign it to the users or groups who should have gateway access.

Any OIDC-compliant IdP works: Okta, Microsoft Entra ID, Google Workspace, Keycloak, Dex, PingFederate, and others. The IdP must meet three requirements:

* Serves `/.well-known/openid-configuration`, over HTTPS in production; the gateway accepts an [`http://` issuer](/en/claude-apps-gateway-config#oidc), and a loopback issuer additionally requires `CLAUDE_GATEWAY_ALLOW_LOOPBACK=1`
* Supports the authorization-code flow. PKCE (Proof Key for Code Exchange) is on by default; disable it with `oidc.use_pkce: false` for IdPs that don't support it
* Returns `email` and optionally `groups` in the id\_token, or serves them from the userinfo endpoint with `oidc.userinfo_fallback: true`

For private PKI, set `oidc.ca_cert_pem`.

A few providers handle email and group claims differently:

* **Okta**: the org authorization server at `https://example.okta.com` returns a thin id\_token that omits `email` and `groups`, so set `oidc.userinfo_fallback: true` whenever you use it as `issuer`. A custom authorization server such as `https://example.okta.com/oauth2/default` that includes `email` and optionally `groups` in the id\_token emits them directly and needs no fallback. Okta emits `groups` only when the `groups` scope is requested in `oidc.scopes` and the app's groups claim filter allows it; `userinfo_fallback` can't fill a claim the IdP wasn't asked for.
* **Microsoft Entra ID**: `issuer` = `https://login.microsoftonline.com/<tenant-id>/v2.0`. Entra emits group Object IDs rather than names, so use the GUIDs in `managed.policies.match.groups`, or use App Roles for human-readable names. If your tenant emits roles under `roles` instead of `groups`, set `oidc.groups_claim: roles`.
* **Google Workspace**: `issuer` = `https://accounts.google.com`. Google's id\_token doesn't carry groups. To use group-based `allowed_groups` or `managed.policies` with Google as the IdP, configure [`oidc.google_groups`](/en/claude-apps-gateway-config#oidc), which looks up each user's groups through the Admin SDK Directory API using a service account with domain-wide delegation. Without it, use `oidc.allowed_email_domains` for membership gating and `managed.policies.match.email_domain` for policy assignment. Google also ignores the standard `offline_access` scope. For refresh tokens, set `oidc.scopes: [openid, profile, email]` and `oidc.extra_auth_params: { access_type: offline, prompt: consent }`.

For support with an identity provider not covered above, see [Troubleshooting](#troubleshooting).

<Warning>
  Refresh tokens let the gateway renew a developer's session silently, without sending the developer back to the browser. They also drive deprovisioning, because when the IdP disables a user, the next refresh fails and the session ends within `ttl_hours`. The gateway requests `offline_access` by default to get a refresh token. If your IdP requires explicit consent for offline access, configure the OAuth client to allow it.

  If your IdP can't issue refresh tokens at all, the gateway still works, but there is no silent renewal, so developers re-run the browser login when their session expires. To keep that from happening every hour, raise [`session.ttl_hours`](/en/claude-apps-gateway-config#session) to `8` or `12`. The tradeoff is deprovisioning latency, because without refresh tokens a disabled user keeps access until the longer TTL elapses.
</Warning>

## Deployment

The gateway is a single Linux binary. It scales horizontally because replicas are stateless and Postgres is the shared coordination layer. Run it however you run stateless services in your environment. The rest of this section states what the image needs, with short notes for Kubernetes and Cloud Run.

The gateway is designed to run inside your network, because it holds your upstream credential and acts as the single egress point for inference. It can run anywhere your developers and your IdP can reach over HTTPS; treat it like any other service holding a production credential.

A few decisions shape the deployment beyond where it runs:

* **Cost**: there is no separate license or per-seat fee for the gateway; it's part of the `claude` binary. You pay for inference through your existing cloud or Anthropic commitment, plus the compute for the container and your telemetry collector.
* **Bypass**: the gateway doesn't enforce that the only route to a model goes through it. A developer with their own credential can still call the provider directly, so closing that path is a network policy decision, for example blocking egress to `api.anthropic.com` except from the gateway. Blocking that egress also breaks the [WebFetch domain safety check](/en/data-usage#webfetch-domain-safety-check), which calls `api.anthropic.com` from each developer's machine; set `skipWebFetchPreflight: true` in the managed policy to disable it.
* **Multiple gateways**: each gateway is a separate deployment with its own config. The CLI stores its trust fingerprint and credentials per gateway hostname, so different teams can connect to different gateways without conflict. To serve multiple OIDC issuers, run separate instances.
* **Serverless**: Cloud Run works; set `min-instances: 1` to avoid cold OIDC discovery. Lambda and Cloud Functions don't, because the gateway is a long-running HTTP server.

Every production topology here puts an L7 proxy, such as an Ingress, Cloud Run's front end, or an ALB, in front of plain-HTTP replicas. Set [`listen.trusted_proxies`](/en/claude-apps-gateway-config#listen) to the proxy's source ranges so the gateway reads client IPs from `X-Forwarded-For`. The gateway honors the header only when the TCP peer is trusted; the [Google Cloud worked example](/en/claude-apps-gateway-on-gcp) has concrete values per topology. Without trusted proxies, every request appears to come from the proxy's IP, which collapses per-IP rate limits into one shared bucket and records the proxy's IP in audit events.

### Container image

Build your own image around the native `claude` binary from the standard Claude Code release:

1. Download the Linux build for your image architecture from a pinned release; see [Install a specific version](/en/setup#install-a-specific-version) for the download URL.
2. Verify it against the release's GPG-signed `manifest.json` as described in [Binary integrity and code signing](/en/setup#binary-integrity-and-code-signing).
3. Copy it into the build context.

Mirror the release into your internal registry if your builds can't reach the release host, and pin the version your fleet runs.

Beyond the binary, the image needs:

* **A glibc-based image**: the glibc build's only dynamic dependencies are glibc libraries. Musl-based images need the `linux-x64-musl` or `linux-arm64-musl` build plus additional packages; see [Alpine Linux setup](/en/setup#alpine-linux-and-musl-based-distributions).
* **A writable state directory**: the gateway runs as any user, but minimal images have no writable home. Set `CLAUDE_CONFIG_DIR` to a writable path such as `/tmp/.claude`.
* **The container command**: `claude gateway --config /etc/claude/gateway.yaml`, with the config file mounted read-only and secrets supplied as environment variables; the gateway listens on `listen.port`, default `8080`.

### Kubernetes

Run the gateway as a Deployment, like any stateless service:

* Mount the config from a ConfigMap and secrets from a Secret; reference secrets in the YAML via `${file:/path/to/secret}` or as environment variables
* Terminate TLS at the Ingress and set `listen.public_url` to the Ingress hostname
* Point the readiness probe at `GET /readyz` and the liveness probe at `GET /healthz`

<Note>
  **Workload identity**

  Prefer the platform's workload identity over static keys: IRSA on EKS for Amazon Bedrock and for Claude Platform on AWS, Workload Identity on GKE for Google Cloud's Agent Platform, and workload identity on AKS for Microsoft Foundry. Set `auth: {}` in the upstream block, or `use_azure_ad: true` for Microsoft Foundry, and the gateway picks up the pod's identity through that provider's default credential chain. For a cross-cloud pairing, such as an Amazon Bedrock upstream on GKE, set explicit credentials in the upstream's `auth` block instead. The [`upstreams` reference](/en/claude-apps-gateway-config#upstreams) has per-platform setup details.
</Note>

### Cloud Run

Configure the service as follows:

* Leave `listen.port` at its default of `8080`, which matches Cloud Run's default `PORT`, or set `port: ${PORT}`
* Set `public_url` to the externally reachable origin. For production this is normally an internal load balancer's hostname, because `/login` [rejects public addresses](/en/claude-apps-gateway#prerequisites) and the `*.run.app` URL resolves to one, so the Cloud Run URL alone works only for a `curl` or browser smoke test. The exception is a network where `*.run.app` resolves privately through Private Service Connect and a Cloud DNS private zone; in that topology the Cloud Run URL is a valid `public_url`. The [Google Cloud worked example](/en/claude-apps-gateway-on-gcp#deploy-the-gateway) covers both.
* Mount the config as a secret volume
* Set `min-instances: 1` to avoid a cold OIDC discovery on first request

<Note>
  For a complete worked example on Google Cloud, covering Cloud Run or GKE, Cloud SQL, and Secret Manager, see [Deploy on Google Cloud](/en/claude-apps-gateway-on-gcp).
</Note>

### Push the gateway URL to developer machines

Once the gateway is serving, push `forceLoginMethod` and `forceLoginGatewayUrl` to each developer's machine through managed settings, via MDM or by writing the per-OS `managed-settings.json` directly. Without this, `/login` shows the standard account picker with no gateway option. See [Client-side managed settings](/en/claude-apps-gateway-config#client-side-managed-settings) for the file paths.

## Operations

Once the gateway is serving traffic, day-to-day operation is reading its logs, probing its health, and rotating its secrets on your schedule. The subsections cover each, plus what Postgres holds and how upgrades and rollbacks behave.

### Logs

The gateway writes two streams to stderr, both JSON-friendly:

* **Audit events**: single-line JSON per security-relevant event. Pipe stderr to your log aggregator. The events emitted include `config.load`, `session.mint`, `session.refresh`, `device.authorize`, `device.verify`, `auth.denied`, `access.denied`, `inference`, `managed.serve`, `spend.blocked`, and `admin.denied`. Fields vary by event:
  * Successful mint and refresh events carry `sub`, `email`, `client_ip`, and the result
  * Denial events carry the reason, path, and client IP, since no identity exists at denial
  * `inference` records which upstream served the request and the response status
  * `admin.denied` records a rejected admin-API auth attempt with the reason (`invalid_key` or `no_credentials`), client IP, method, and path, without the presented key material
* **Operational logs**: human-readable `[gateway]`-prefixed lines for boot, warnings, and upstream errors. The `CLAUDE_GATEWAY_LOG_LEVEL` environment variable controls verbosity and accepts `info`, `warn`, or `error`, with `info` as the default. It doesn't affect audit events, which are always emitted.

### Health

The gateway serves `GET /healthz` as a liveness probe and `GET /readyz` as a readiness probe; `/readyz` verifies the store is reachable. Both are exempt from `access_control.allow_cidrs`, so probes keep working on a locked-down listener.

The OAuth discovery document at `/.well-known/oauth-authorization-server` also returns `200` only after config load, OIDC discovery, upstream client construction, and Postgres migration all succeed, so it doubles as an end-to-end boot check.

A running gateway also serves a description of the paths and request shapes it accepts at `<public_url>/protocol`, matched to the version you're running. The contents aren't stable across releases.

### Outage behavior

If Postgres goes down, the gateway itself keeps serving signed-in developers and new sign-ins fail. Whether developers actually keep working depends on how your orchestrator handles readiness:

* **Existing sessions**: bearer tokens validate locally with the JWT secret, session refreshes don't touch the store, and the gateway process can still serve inference
* **New sign-ins**: fail until Postgres recovers, because the device flow and its rate-limit counters live in Postgres
* **[Spend-limit enforcement](/en/claude-apps-gateway-spend-limits#postgres-availability)**: fails open by default during the outage, so inference still flows; flip it to fail closed if you'd rather block than run unmetered
* **Readiness**: `/readyz` reports not-ready during the outage, so orchestrators that gate traffic on readiness remove every replica from rotation at once. In that topology all traffic, including inference the gateway could still serve, fails at the load balancer until Postgres recovers. The liveness probe on `/healthz` keeps passing, so replicas aren't restarted. Point the readiness probe at `/healthz` instead if you'd rather signed-in developers keep working through a store outage; the cost is that new sign-ins fail against a replica that still reports ready.

If your IdP goes down, existing sessions work until `ttl_hours`, and new logins and refreshes fail. Set a longer `ttl_hours` if your IdP has frequent maintenance windows.

### JWT secret rotation

Rotate the signing secret in three steps so existing sessions stay valid:

1. Generate a new secret. Prepend it to the `session.jwt_secret` array.
2. Roll the deployment. New tokens sign with the new secret; old tokens still verify.
3. After `ttl_hours` plus a margin, remove the old secret and roll again.

Rotation is also the only way to force sessions out before they expire: bearer tokens validate locally against the JWT secret, so there is no per-session revocation. Replacing the secret outright, without keeping the old one in the array, invalidates every outstanding session at once. For individual offboarding, deprovision the user in your IdP; their session ends within `ttl_hours`.

### Postgres

The gateway holds five tables, all created by its boot-time migrations:

| Table              | Contents                                                                      | Retention                                                       |
| ------------------ | ----------------------------------------------------------------------------- | --------------------------------------------------------------- |
| `kv`               | Device grants (10-minute TTL) and rate-limit counters                         | TTL per row                                                     |
| `spend`            | Per-principal period-to-date spend counters, in cents                         | `admin.spend_retention_months`, default 13                      |
| `spend_limits`     | Configured spend caps                                                         | Until deleted via the API                                       |
| `admin_audit`      | Admin API mutation trail                                                      | `admin.audit_retention_days`, default 365                       |
| `principal_emails` | Each principal's last-seen email, display name, and IdP groups. Contains PII. | `admin.identity_retention_days` since last activity, default 90 |

A 30-second loop expires `kv` rows past their TTL, and an hourly sweep enforces the retention windows on the spend tables, so nothing grows without bound. Without [spend limits](/en/claude-apps-gateway-spend-limits) configured, only `kv` is written. If your security policy prohibits DDL from the application role, pre-create these tables and `_migrations` with an admin role and grant the app role `SELECT, INSERT, UPDATE, DELETE` on each.

With spend limits in use, a lost database means lost spend tracking and caps, not only developer re-logins, so run regular backups. To erase one departed developer immediately rather than waiting on retention, run `DELETE FROM principal_emails WHERE principal = '<sub>'` directly; that removes the only table holding their email, name, and groups. `spend` and `admin_audit` rows reference the pseudonymous OIDC `sub` only.

### Upgrades

Replicas are stateless, so a rolling restart is safe at any time. The gateway runs schema migrations at boot, which means deploying the new binary self-migrates the database. If the database role can't run DDL, pre-create the schema, including the `_migrations` table seeded to the current version; otherwise boot fails attempting `CREATE TABLE`.

Migrations are append-only, so rolling back to a prior binary that knows fewer migrations is safe; it ignores the extra rows. Rollback also re-validates the YAML against the older binary's schema, so a config that adopted a key introduced by the newer release fails boot on the older one. Remove the new key before rolling back.

Because you pin the gateway's version in your own image, fixes in new Claude Code releases, including security fixes, reach your deployment only when you update the pin and redeploy. Include the gateway in the same patching cadence you use for other services that hold production credentials.

## Security

This section answers the questions a security review asks: what data flows through the gateway and where it goes, which attacks the design defends against, and which answers belong in a compliance questionnaire.

### Data flow

| Data                                                                                              | Path                                                         | Sent to Anthropic by the gateway                   |
| ------------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| Inference (prompts, completions)                                                                  | CLI → gateway → your upstream                                | Only if the Anthropic API is a configured upstream |
| Telemetry (OTLP metrics, plus [opt-in logs and traces](/en/claude-apps-gateway-config#telemetry)) | CLI → gateway → your collector                               | Never                                              |
| Identity (email, groups, sub)                                                                     | IdP → gateway → JWT → CLI; the CLI stamps it on OTLP exports | Never                                              |
| Managed settings                                                                                  | Your gateway YAML → CLI                                      | Never                                              |
| Audit log                                                                                         | Gateway stderr → your aggregator                             | Never                                              |

### Threat model summary

The gateway sits inside your network perimeter, but individual developer laptops aren't treated as trusted. The design accounts for this in three ways:

* Developers hold short-lived JWTs instead of raw upstream keys. The CLI-to-gateway leg uses the RFC 8628 device grant, and the gateway's authorization-code exchange with the IdP runs PKCE in the default configuration, so an intercepted IdP authorization code is useless.
* The device-verification page enforces same-origin POST and a per-IP rate limit per RFC 8628 §5.1. See [User-code brute-force resistance](#user-code-brute-force-resistance).
* Outbound requests go through a server-side request forgery (SSRF) guard that resolves DNS, blocks link-local and cloud-metadata addresses plus loopback by default, and pins the connection to the resolved IP, so operator-influenced URLs such as the IdP and OTLP destinations can't be redirected to cloud metadata endpoints. RFC 1918 private ranges are deliberately allowed, because IdPs and OTLP collectors commonly live on private IPs. For local development against a loopback IdP or collector, set `CLAUDE_GATEWAY_ALLOW_LOOPBACK=1` in the gateway's environment; leave it unset in production.

If you add your own egress controls, the gateway must reach the metadata server whenever it uses instance-metadata credentials such as workload identity.

Two threats are out of scope because they are your infrastructure to secure:

* **A compromised gateway host**: the host both holds the upstream credential and distributes [managed settings](/en/claude-apps-gateway-config#managed) to every connected developer, so control over the gateway's configuration is comparable to control over your MDM. The CLI's one-time approval dialog for shell-capable settings limits silent changes but doesn't replace host security.
* **A malicious OIDC provider**: the provider signs the id\_tokens the gateway trusts, so it can assert any identity. Vetting and securing your IdP is your responsibility.

### User-code brute-force resistance

The `user_code` a developer types into the `/device` verification page is 8 characters drawn from a 20-character alphabet, which yields 20⁸ or about 2.56×10¹⁰ combinations, and it expires after 10 minutes.

The gateway applies per-IP rate limits on the device-grant endpoints, configurable via [`rate_limits`](/en/claude-apps-gateway-config#http-tuning). Raise the limits if many developers sign in from a single shared corporate NAT address. The limits apply only to the sign-in flow, not to inference.

### Compliance posture

* **Data residency**: the gateway's own data plane sends nothing to Anthropic unless the Anthropic API is a configured upstream; when it is, your existing data-handling agreement applies to the inference path. Telemetry, audit, identity, and settings go only to the destinations you configure.
* **Host-process traffic**: the host process is the Claude Code CLI, which can send startup analytics and update checks to Anthropic. For strict-egress deployments, set `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` in the gateway's container environment.
* **Client analytics**: the CLI disables its own usage analytics while signed in to a gateway, and error reporting is off by default on third-party API surfaces.
* **Client machines**: developers' CLIs still send WebFetch hostname checks and version checks to Anthropic unless `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1` and `skipWebFetchPreflight: true` are set. See [data usage](/en/data-usage).
* **Survey ratings**: the gateway credential disables the Anthropic-bound rating sink, so ratings aren't sent to Anthropic.
* **Transcript sharing**: choosing Yes on a survey's transcript-share prompt writes a local file under `~/.claude/feedback-bundles/` instead of uploading to Anthropic.
* **Client updates**: update checks are separate from gateway traffic. Pin versions through your own distribution and set `DISABLE_UPDATES` if laptops must not fetch releases. `DISABLE_AUTOUPDATER` stops only background updates while `claude update` still works.
* **TLS**: serve `public_url` over HTTPS in production, either from the gateway's own listener via `listen.tls` or from a TLS-terminating ingress in front of plain-HTTP replicas with `listen.public_url` set. The gateway doesn't refuse plain HTTP. The IdP must serve HTTPS in production, and Postgres supports `?sslmode=require`. Set `Strict-Transport-Security` at your ingress.
* **Vulnerability disclosure**: follow [Reporting security issues](/en/security#reporting-security-issues)

## Troubleshooting

For questions and feedback, use [Claude Code support](https://support.claude.com/en/collections/14445694-claude-code), or open an issue on the [Claude Code GitHub repository](https://github.com/anthropics/claude-code/issues). When reporting a problem, include:

* **Gateway issue**: the gateway's stderr for the relevant window, your `gateway.yaml` with secrets redacted, the gateway version, shown on the landing page at `/` and in the `x-cc-gateway-version` response header on `/managed/settings`, and what changed recently
* **Login issue**: the developer runs `claude --debug-file ./claude-debug.txt`, reproduces, and sends that file plus the gateway's audit log for the same window
* **Inference issue**: the model requested, the upstreams configured, and the gateway's audit log for the request, which records which upstream served it and the response status

| Symptom                                                                                                                                                                     | Cause                                                                                                                                                                                                                                                                                                                         | Fix                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A developer's `/login` shows the standard account picker instead of the **Cloud gateway** screen                                                                            | `forceLoginMethod` or `forceLoginGatewayUrl` isn't set in managed settings on that machine                                                                                                                                                                                                                                    | Deploy the [managed settings file](/en/claude-apps-gateway#set-the-gateway-url) to the device; `/login` reads the gateway URL from there                                                                                                                                                                                                                                                                                                |
| Startup shows `Gateway login is configured in managed settings, but this Claude Code build does not include Cloud gateway support.`                                         | The installed Claude Code build predates gateway support                                                                                                                                                                                                                                                                      | Have the developer update Claude Code to a release that includes Cloud gateway support                                                                                                                                                                                                                                                                                                                                                  |
| CLI `/login`: `Gateway hosts must be on your organization's private network; <host> resolves to the public (or unrecognized) address <ip>`                                  | The gateway hostname resolves to at least one public IP address. Claude Code checks each resolved address and requires every one to be private. A common cause is a dual-stack name where one family resolves to a public address, including AWS internal dual-stack load balancers, which return public-range AAAA addresses | Have the gateway name resolve only to private addresses on developer machines. For a dual-stack name, drop the public-range record or serve a separate internal-only DNS name. See the [private-network prerequisite](/en/claude-apps-gateway#prerequisites).                                                                                                                                                                           |
| CLI `/login`: `Gateway login requires a direct connection and does not support connecting through an HTTP proxy`                                                            | An `HTTPS_PROXY` or `HTTP_PROXY` applies to the gateway host and the proxy's hostname resolves to a public address. A proxy whose host resolves only to private addresses is allowed and doesn't trigger this error                                                                                                           | Add the gateway host to `NO_PROXY` on the developer's machine so the connection is direct, or use a proxy whose hostname resolves to private addresses                                                                                                                                                                                                                                                                                  |
| CLI `/login`: `Could not resolve gateway host <host>`                                                                                                                       | The machine can't resolve the gateway's internal DNS name, typically because it isn't on the corporate network                                                                                                                                                                                                                | Have the developer connect to your network or VPN, then retry `/login`                                                                                                                                                                                                                                                                                                                                                                  |
| Boot exits with a config validation error naming `store.postgres_url`                                                                                                       | No Postgres configured; the gateway requires Postgres                                                                                                                                                                                                                                                                         | Set `store.postgres_url`. For local development, use a throwaway container: `docker run --rm -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust postgres`.                                                                                                                                                                                                                                                                                 |
| Boot exits: `requires the native binary`                                                                                                                                    | Running under Node instead of the native binary                                                                                                                                                                                                                                                                               | Install Claude Code with one of the [standalone install methods](/en/setup)                                                                                                                                                                                                                                                                                                                                                             |
| Boot exits with an OIDC discovery error after `config.load`                                                                                                                 | `oidc.issuer` unreachable, or TLS chain not trusted                                                                                                                                                                                                                                                                           | Check the issuer is reachable from the pod and serves `/.well-known/openid-configuration`. Set `ca_cert_pem` for private PKI.                                                                                                                                                                                                                                                                                                           |
| Boot exits with a Postgres permission error                                                                                                                                 | App role lacks `CREATE TABLE`                                                                                                                                                                                                                                                                                                 | Pre-create the schema with an admin role and grant DML to the app role, or grant DDL temporarily for boots that apply new migrations                                                                                                                                                                                                                                                                                                    |
| `/oauth/callback` shows "Sign-in could not be completed"                                                                                                                    | Email domain rejected, id\_token validation failed, or `email_verified` is explicitly `false`, which the gateway always rejects with no override                                                                                                                                                                              | Check `allowed_email_domains` and that the IdP returns a verified `email` claim. For `email_verified: false`, fix the IdP-side verification. If your IdP emits email under a different claim name, set `oidc.email_claim`.                                                                                                                                                                                                              |
| Log: `token exchange failed: id_token missing email claim`                                                                                                                  | The IdP isn't including `email` in the id\_token by default. This rejection fires only when `allowed_email_domains` is set; without it, a missing email mints a session with no email                                                                                                                                         | Configure the IdP to emit `email` in the id\_token. Okta: add `email` to a custom authorization server's ID-token claims. Entra: add `email` as an optional claim on the app registration. PingFederate: enable an OpenID Connect Policy that emits `email`. If the IdP serves `email` from the userinfo endpoint but won't include it in the id\_token, such as the Okta org authorization server, set `oidc.userinfo_fallback: true`. |
| Every Amazon Bedrock request returns 502; log shows `Could not load credentials from any providers`                                                                         | On EC2, IMDSv2's default hop limit of 1 blocks the instance-metadata request from inside the container. Boot and `/readyz` pass anyway because the AWS SDK resolves instance credentials on the first request, not at client construction                                                                                     | Raise the hop limit with `aws ec2 modify-instance-metadata-options --instance-id <id> --http-put-response-hop-limit 2`, or set it in the launch template. The change applies to every container on the instance. Prefer ECS task roles where available, which read credentials from the ECS container-credentials endpoint and avoid the change entirely, or apply the change on a dedicated gateway instance to limit the exposure.    |
| IdP error: unknown or unsupported scope                                                                                                                                     | The IdP rejects scopes it doesn't recognize                                                                                                                                                                                                                                                                                   | Set `oidc.scopes` to exactly the list your IdP accepts; it must include `openid`. The default is `openid profile email offline_access`.                                                                                                                                                                                                                                                                                                 |
| Sessions don't silently renew after setting `oidc.scopes`                                                                                                                   | `offline_access` was dropped from the override                                                                                                                                                                                                                                                                                | Add `offline_access` back if your IdP supports it. Without a refresh token, developers re-run the browser login every `session.ttl_hours`.                                                                                                                                                                                                                                                                                              |
| Browser shows "This request came from another site and was blocked"                                                                                                         | Cross-site form POST, blocked as CSRF protection. Expected for embedded or proxied pages                                                                                                                                                                                                                                      | Open the verification link directly                                                                                                                                                                                                                                                                                                                                                                                                     |
| Chrome blocks the Approve button with "Refused to send form data … violates … Content Security Policy directive: form-action", but the same page works in Safari or Firefox | Chrome enforces `form-action` against the entire redirect chain. Your IdP redirects onward to a second host that isn't allowlisted.                                                                                                                                                                                           | Add each additional origin in the redirect chain to `oidc.form_action_origins`. Open Chrome DevTools → Console on the Approve page to see which origin was blocked.                                                                                                                                                                                                                                                                     |
| Sign-in completes at the IdP but the callback fails, with a CSP error in Chrome or "this sign-in link has expired" in Safari                                                | The IdP returned the code via `response_mode=form_post`, which auto-submits it cross-origin via POST to `/oauth/callback`. Chrome blocks that under a strict CSP; Safari allows the submit but the callback reads only the query string.                                                                                      | Make sure your IdP honors `response_mode=query`, which the gateway requests explicitly so the callback is a plain redirect                                                                                                                                                                                                                                                                                                              |
| Login works locally but fails behind an ALB                                                                                                                                 | `public_url` not set, so the IdP gets the inner `http://` origin as `redirect_uri`                                                                                                                                                                                                                                            | Set `listen.public_url` to the external `https://` origin                                                                                                                                                                                                                                                                                                                                                                               |
| Developer sees the trust prompt repeatedly                                                                                                                                  | TLS cert is rotating per replica or per request                                                                                                                                                                                                                                                                               | Use a stable cert at the ingress, or terminate TLS once and run replicas over plain HTTP internally                                                                                                                                                                                                                                                                                                                                     |
| CLI `/login`: "Could not verify the gateway's TLS certificate" or `SELF_SIGNED_CERT_IN_CHAIN`                                                                               | Gateway's TLS chain is signed by a private CA not in the CLI host's trust store                                                                                                                                                                                                                                               | Claude Code reads the OS trust store by default on the native binary and on Node 22.15 or later; [`CLAUDE_CODE_CERT_STORE`](/en/network-config#ca-certificate-store) controls this behavior. If the CA is installed in the OS trust store, ensure developers are on a current runtime. Otherwise set `NODE_EXTRA_CA_CERTS` to the CA certificate PEM before launching. The first-connect fingerprint prompt still applies.              |

## Related

* [Claude apps gateway overview](/en/claude-apps-gateway): quickstart and developer connection
* [Configuration reference](/en/claude-apps-gateway-config): every `gateway.yaml` option
