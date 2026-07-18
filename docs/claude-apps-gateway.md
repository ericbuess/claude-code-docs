> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude apps gateway for Amazon Bedrock, Claude Platform on AWS, Google Cloud, and Microsoft Foundry

> Run Claude Code through Amazon Bedrock, Claude Platform on AWS, Google Cloud, or Microsoft Foundry behind a self-hosted gateway with SSO sign-in, per-group model access, and OTLP telemetry.

<Note>
  The Claude apps gateway is designed for organizations that must, or prefer to, route inference through their own cloud provider, for example to meet [data residency](/en/claude-apps-gateway-deploy#compliance-posture) requirements. If you don't have this requirement, and want access to other features such as SCIM provisioning or Claude Code on web and mobile, Claude Enterprise may be a better fit. See the [feature availability](/en/feature-availability) page for a full comparison of all deployment methods.
</Note>

Claude apps gateway is a self-hosted service that sits between your developers' Claude Code clients and your model provider. Developers sign in with your corporate identity provider (IdP) instead of holding API keys or cloud credentials. The gateway holds the upstream credential, enforces model access and [managed settings](/en/permissions#managed-settings) by IdP group, and relays usage telemetry to your own observability stack.

It is included in the `claude` binary, so the same executable that runs Claude Code on a laptop runs the gateway server with `claude gateway --config gateway.yaml`.

This page covers:

* [Why Claude apps gateway](#why-claude-apps-gateway), what it adds over running your own, and when something else fits better
* A [quickstart](#quickstart) with [prerequisites](#prerequisites) that takes a gateway from zero to a signed-in developer
* [Connecting developers](#connect-developers), including setting the gateway URL through managed settings
* [Availability and limitations](#availability-and-limitations) covering which Claude Code features work through the gateway and what the server supports

Companion pages go deeper. The [configuration reference](/en/claude-apps-gateway-config) covers every option in the YAML file the quickstart writes, and the [deployment guide](/en/claude-apps-gateway-deploy) covers per-IdP setup, Kubernetes and Cloud Run deployment, and operations.

## Why Claude apps gateway

The [gateway overview](/en/gateways) covers what a gateway does and why you'd run one. Claude apps gateway is Anthropic's own gateway, built into the `claude` binary and tested alongside each Claude Code release, so it forwards the headers and request fields Claude Code sends without operators maintaining a separate allowlist. Once deployed it gives you:

* **Credentials**: the upstream API key or cloud credential lives only in your infrastructure. Developers authenticate with corporate SSO and receive short-lived bearer tokens, so offboarding happens in your IdP. Deprovision a user and their gateway access expires within the session lifetime, one hour by default.
* **Access control**: your IdP groups map to model allowlists and [managed settings](/en/permissions#managed-settings) policies. The gateway enforces model access server-side, rejecting requests for non-granted models, and selects each group's managed settings policy, which the CLI applies at the [managed settings tier](/en/settings#settings-precedence). Different teams get different models, tools, and permissions, and a developer can't override what their policy locks.
* **Settings delivery**: the gateway delivers managed settings to signed-in clients itself, taking the place of [server-managed settings](/en/server-managed-settings) from the claude.ai admin console.
* **Telemetry**: each configured destination, such as Datadog, Splunk, or ClickHouse, receives [OpenTelemetry Protocol (OTLP) metrics](/en/monitoring-usage) with token counts, model, user identity, and latency by default, with logs and traces as per-destination opt-ins.
* **Upstream routing**: clients speak the Anthropic Messages API to the gateway, and the gateway translates for each upstream, whether Amazon Bedrock, [Claude Platform on AWS](/en/claude-platform-on-aws), Google Cloud's Agent Platform, Microsoft Foundry, or the Anthropic API, with failover between them. You can change regions, providers, or failover order without developers noticing or reconfiguring.

<Frame>
  <img src="https://mintcdn.com/claude-code/st9_ZQOFsZa3cKFl/images/claude-gateway-architecture.svg?fit=max&auto=format&n=st9_ZQOFsZa3cKFl&q=85&s=560770d8f49bbd6f1ca7090ed1f13c03" alt="Diagram showing Claude Code clients connecting over HTTPS with bearer tokens to a self-hosted Claude apps gateway inside your infrastructure, which signs users in against your IdP, stores auth state in PostgreSQL, relays telemetry to your OTLP collector, and forwards inference to Amazon Bedrock, Claude Platform on AWS, Google Cloud, Microsoft Foundry, or the Anthropic API" width="760" height="320" data-path="images/claude-gateway-architecture.svg" />
</Frame>

<Note>
  The gateway's own data plane sends nothing to Anthropic infrastructure unless the Anthropic API is a configured upstream. You control where telemetry, audit logs, managed settings, and your developers' IdP identity go, and the gateway sends none of them to Anthropic. For the remaining traffic the CLI process can send and how to close it, see [Compliance posture](/en/claude-apps-gateway-deploy#compliance-posture).
</Note>

For which Claude Code features work through the gateway and what the server itself supports, see [Availability and limitations](#availability-and-limitations) below. For decisions such as cost, bypass, running multiple gateways, and serverless platforms, see the [deployment guide](/en/claude-apps-gateway-deploy#deployment).

### Other gateway implementations

If you already run an LLM gateway or API gateway that meets your needs, keep using it; [Other LLM gateways](/en/llm-gateway) covers configuring Claude Code against it.

The [gateway protocol reference](/en/llm-gateway-protocol) documents the contract Claude Code expects from any gateway: the endpoints it calls, the headers and body fields to forward, and what stops working when they're stripped. A running Claude apps gateway serves a superset of that contract at `GET /protocol`, adding the Claude apps gateway-specific endpoints for SSO sign-in, managed settings delivery, and telemetry. Fetch it with `curl https://claude-gateway.internal.example.com/protocol` from any deployed gateway, such as the one the [quickstart](#quickstart) below produces.

Breaking changes to the protocol are announced in advance, but indefinite backwards compatibility isn't guaranteed.

## Quickstart

This quickstart walks the minimal path: register an OAuth client in your IdP, write a `gateway.yaml`, run the gateway alongside Postgres with Docker Compose, and verify sign-in end to end. It uses an Amazon Bedrock upstream; Claude Platform on AWS, Google Cloud's Agent Platform, Microsoft Foundry, and the Anthropic API are equally supported by swapping the `upstreams` block as shown in the [configuration reference](/en/claude-apps-gateway-config#upstreams). At the end you have a gateway a developer can `/login` to.

<Note>
  **Deploy on your private network.** Claude Code only connects to a gateway whose address is private. This is a security guard, because a trusted gateway can push settings that run commands on developer machines. Put the gateway behind an internal load balancer or VPN and give it a hostname that resolves to private IPs only.

  Anthropic-operated public gateway endpoints are the exception: `/login` accepts them over `https://`. These are a small fixed set of gateways that Anthropic itself operates; they aren't a deployment option you can select or configure. The list is compiled into Claude Code, so no configuration can add a hostname to it and no gateway you host qualifies for the exemption. {/* min-version: 2.1.206 */}Before v2.1.206, `/login` rejected those endpoints like any other public address.
</Note>

### Prerequisites

Have these in place before you start:

| You need                                | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Claude Code v2.1.195 or later           | The `claude gateway` subcommand and the gateway sign-in flow ship in v2.1.195. Earlier public builds don't include them. Both the machine running the gateway server and each developer's machine must be on v2.1.195 or later; run `claude update` to get the latest release. {/* min-version: 2.1.198 */}The [Claude Platform on AWS upstream](/en/claude-apps-gateway-config#claude-platform-on-aws) requires Claude Code v2.1.198 or later on the gateway server.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| OpenID Connect (OIDC) identity provider | Okta, Microsoft Entra ID, Google Workspace, Keycloak, or Dex, or any other OIDC-compliant IdP such as PingFederate. The gateway runs standard OIDC discovery and the authorization-code flow against it. SAML and LDAP aren't supported.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| PostgreSQL 14 or later                  | Backs the device sign-in flow, where the browser callback writes and the polling CLI reads, plus rate-limit counters. Any managed Postgres works, including the smallest tier. Without spend limits configured, the gateway stores a few KB of short-lived auth state; with [spend limits](/en/claude-apps-gateway-spend-limits), it also holds durable spend, audit, and identity tables that should be backed up. TLS via `?sslmode=require` is recommended.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| Model upstream                          | Amazon Bedrock credentials, Claude Platform on AWS credentials, Google Cloud credentials, a Microsoft Foundry resource, or an Anthropic API key. Multiple upstreams are supported with failover.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| HTTPS                                   | The gateway must be reachable over `https://` from developer laptops and from any browser used for sign-in; the gateway serves the device-verification page on the same listener. Either provide a TLS cert via `listen.tls`, or run behind a TLS-terminating ingress and set `listen.public_url`. A plain `http://` origin is accepted only on loopback, for local development.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Private-network address                 | At `/login`, Claude Code requires the gateway's hostname or IP address to resolve only to private addresses: RFC 1918, link-local, CGNAT `100.64.0.0/10`, IPv6 ULA `fc00::/7`, or loopback for local development. For a gateway you host, any public address is rejected; see the [threat model](/en/claude-apps-gateway-deploy#threat-model-summary) in the deployment guide. The check runs on each resolved IP, so if any address the name resolves to is public, `/login` rejects the URL. If developer machines route HTTPS through a corporate proxy, sign-in also requires the proxy host to resolve to private addresses; if it doesn't, add the gateway host to `NO_PROXY` so the CLI connects directly. {/* min-version: 2.1.206 */}Anthropic-operated public gateway endpoints are exempt from the private-address and proxy checks: `/login` accepts them over `https://` by exact hostname match, so the private-network requirement applies only to a gateway you host yourself. Before v2.1.206, `/login` rejected an Anthropic-operated endpoint like any other public address. |
| Linux runtime                           | The gateway server runs only on the native Linux binary. macOS works for local development. Windows isn't supported as a server platform.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

The gateway server requires the native `claude` binary; download a pinned release as described in [Install Claude Code](/en/setup). The server uses runtime features that aren't available when Claude Code runs under Node. If you see `requires the native binary` at boot, switch to one of the standalone install methods.

### Steps

<Steps>
  <Step title="Register an OAuth client in your IdP">
    Decide the gateway's hostname first, because the redirect URI must match it. Create a new OIDC web application and set the redirect URI to `https://claude-gateway.<your-domain>/oauth/callback`, where the host is the same value you set as [`listen.public_url`](/en/claude-apps-gateway-config#listen) in step 3. Note the `client_id` and `client_secret`. Per-IdP instructions are in [Identity provider setup](/en/claude-apps-gateway-deploy#identity-provider-setup).
  </Step>

  <Step title="Provision a PostgreSQL database">
    Any Postgres 14 or later works, including the smallest managed tier. The gateway runs its own schema migrations at boot, so the database user needs `CREATE TABLE` permission. If your security policy prohibits DDL from application roles, pre-create the schema instead; see [`store`](/en/claude-apps-gateway-config#store).
  </Step>

  <Step title="Write gateway.yaml">
    Secrets are read via `${ENV_VAR}` expansion so the file itself can live in version control. Use a `public_url` hostname that resolves to a private IP on your network, because `/login` rejects public addresses. The minimal config has five sections, and every other field has a default:

    ```yaml gateway.yaml theme={null}
    listen:
      host: 0.0.0.0
      port: 8080
      # Required behind any TLS-terminating proxy. Used for the IdP
      # redirect_uri and the discovery document.
      public_url: https://claude-gateway.internal.example.com

    oidc:
      issuer: https://login.example.com        # must serve /.well-known/openid-configuration
      client_id: 0oa1example2
      client_secret: ${OIDC_CLIENT_SECRET}
      allowed_email_domains: [example.com]        # reject id_tokens outside your org
      userinfo_fallback: true                  # for IdPs whose id_token omits email/groups; harmless otherwise

    session:
      jwt_secret: ${GATEWAY_JWT_SECRET}        # openssl rand -base64 32
      ttl_hours: 1                             # also bounds revocation latency on IdP deprovision

    store:
      postgres_url: ${GATEWAY_POSTGRES_URL}    # add ?sslmode=require for managed Postgres

    upstreams:
      - provider: bedrock
        region: us-east-1
        auth: {}                               # empty: AWS default credential chain
                                               # (IRSA, EC2/ECS task role, env vars, ~/.aws)

    # Models are translated per upstream automatically. The built-in catalog
    # maps claude-opus-4-8 to us.anthropic.claude-opus-4-8 and so on for every
    # Bedrock-supported Claude model. Set false and add a `models:` list to
    # expose only specific models.
    auto_include_builtin_models: true
    ```

    This config is enough for a working sign-in loop with the default Amazon Bedrock model catalog. Once it's running, add per-group RBAC and managed settings via [`managed.policies`](/en/claude-apps-gateway-config#managed), telemetry fan-out via [`telemetry`](/en/claude-apps-gateway-config#telemetry), and multi-upstream failover, provisioned-throughput ARNs, or non-US regions via [`models`](/en/claude-apps-gateway-config#models).

    <Note>
      The Amazon Bedrock upstream needs an AWS principal with `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream` on both the `inference-profile/us.anthropic.*` ARNs and the underlying `foundation-model/anthropic.*` ARNs, and model access enabled in the Amazon Bedrock console for the Claude models you want. Supply the credential with IRSA on EKS, an ECS task role, or an EC2 instance profile rather than static keys. The [`upstreams` reference](/en/claude-apps-gateway-config#upstreams) has the full IAM details, the cross-cloud credential matrix, and the `auth` blocks for the other providers.
    </Note>
  </Step>

  <Step title="Run it">
    Build a container image around the `claude` binary that meets the [image requirements](/en/claude-apps-gateway-deploy#container-image), then run it alongside Postgres. The Compose file references the image as `registry.example.com/claude-gateway:2.1.198`; substitute your own registry and image tag:

    ```yaml docker-compose.yaml theme={null}
    services:
      gateway:
        image: registry.example.com/claude-gateway:2.1.198
        ports: ["8080:8080"]
        volumes: ["./gateway.yaml:/etc/claude/gateway.yaml:ro"]
        environment:
          OIDC_CLIENT_SECRET: ${OIDC_CLIENT_SECRET}
          GATEWAY_JWT_SECRET: ${GATEWAY_JWT_SECRET}
          GATEWAY_POSTGRES_URL: postgres://gw:pw@postgres/gateway
          # AWS credentials: in production, omit these and use an instance
          # role. For local Compose testing, pass through your own:
          AWS_ACCESS_KEY_ID: ${AWS_ACCESS_KEY_ID}
          AWS_SECRET_ACCESS_KEY: ${AWS_SECRET_ACCESS_KEY}
          AWS_SESSION_TOKEN: ${AWS_SESSION_TOKEN}
        depends_on:
          postgres:
            condition: service_healthy
      postgres:
        image: postgres:16-alpine
        environment: { POSTGRES_USER: gw, POSTGRES_PASSWORD: pw, POSTGRES_DB: gateway }
        healthcheck:
          test: ["CMD-SHELL", "pg_isready -U gw"]
          interval: 5s
        volumes: ["pgdata:/var/lib/postgresql/data"]
    volumes: { pgdata: }
    ```

    The gateway is a single Linux binary that reads the config, runs OIDC discovery against your IdP, applies its Postgres schema migrations, builds upstream clients, and starts listening. Boot is fail-closed for the config, the Postgres connection with a 5-second timeout, OIDC discovery, and upstream client construction. If any of those is unreachable or misconfigured, the gateway exits with an error rather than serving traffic in a degraded state.

    A successful boot doesn't validate the inference path, because Amazon Bedrock and Google Cloud's Agent Platform instance credentials resolve on the first request, not at boot.

    Watch stderr for the boot sequence. Log lines use the format `[gateway] <timestamp> <level> <message>`, audit events are single-line JSON with an `evt` field, and a startup banner, omitted below, prints between the migration and listening lines. You should see, in order:

    ```text theme={null}
    {"ts":"2026-06-10T17:03:21.114Z","evt":"config.load","path":"/etc/claude/gateway.yaml","sha256":"…"}
    [gateway] 2026-06-10T17:03:21.408Z info migration 1 applied
    [gateway] 2026-06-10T17:03:21.512Z info claude gateway listening on http://0.0.0.0:8080
    ```

    If boot exits before the `claude gateway listening on` line, the last line of stderr names the problem:

    * an unreachable Postgres
    * a Postgres role without DDL permission
    * an unreachable or invalid OIDC discovery document
    * a config schema violation with the offending field path

    Fix it and restart.

    If you already have a TLS-terminating ingress, skip Compose and run the binary directly with `claude gateway --config gateway.yaml`. Set `public_url` to the ingress origin and bind `listen` to a loopback or cluster-internal address.
  </Step>

  <Step title="Verify the auth surface">
    Three checks confirm the gateway can authenticate a real user before you hand it to a developer.

    The examples use the gateway's public URL; for the local Compose setup without an ingress, substitute `http://localhost:8080` in the first two checks. The third check opens `verification_uri_complete`, which is built from `public_url`, so for local Compose set `public_url: http://localhost:8080` in `gateway.yaml`, and add `http://localhost:8080/oauth/callback` as a second redirect URI on the OAuth client from step 1, because the gateway builds the IdP `redirect_uri` from `public_url`. The verification link then opens in your local browser.

    In Windows PowerShell, run `curl.exe`; the bare `curl` is an alias for `Invoke-WebRequest` and rejects these flags.

    First, fetch the discovery document, which confirms the gateway is up, the config is valid, and all boot checks passed:

    ```bash theme={null}
    curl -s https://claude-gateway.internal.example.com/.well-known/oauth-authorization-server | jq
    ```

    ```json theme={null}
    {
      "issuer": "https://claude-gateway.internal.example.com",
      "device_authorization_endpoint": "…/oauth/device_authorization",
      "token_endpoint": "…/oauth/token",
      "grant_types_supported": ["urn:ietf:params:oauth:grant-type:device_code", "refresh_token"]
    }
    ```

    The response includes additional fields, such as `response_types_supported` and `scopes_supported`.

    Second, request a device authorization, which confirms the device sign-in flow works and Postgres is reachable and writable:

    ```bash theme={null}
    curl -s -X POST https://claude-gateway.internal.example.com/oauth/device_authorization | jq
    ```

    ```json theme={null}
    {
      "device_code": "…",
      "user_code": "WDJB-MJHT",
      "verification_uri": "https://claude-gateway.internal.example.com/device",
      "verification_uri_complete": "https://claude-gateway.internal.example.com/device?user_code=WDJB-MJHT",
      "expires_in": 600,
      "interval": 5
    }
    ```

    Third, test the browser leg by opening `verification_uri_complete` in a browser and confirming the code. You should be redirected to your IdP's sign-in page, and after signing in, land back on the gateway with a signed-in confirmation.

    Use the first failing check to locate the problem:

    * **First check fails**: boot didn't complete; check stderr
    * **Second check fails**: Postgres isn't reachable from the gateway or the role can't write; check the connection string and grants
    * **Third check doesn't reach the IdP**: check that the IdP's redirect URI matches `https://<gateway>/oauth/callback` exactly
    * **Third check reaches the IdP but bounces back with an error**: read the gateway's audit log, which records every auth rejection with the reason, such as `email domain not allowed`
  </Step>

  <Step title="Log a developer in">
    This last step happens on a developer machine, not the server. Set `forceLoginMethod` to `"gateway"` and `forceLoginGatewayUrl` to your gateway's `public_url` in that machine's [managed settings file](/en/settings#settings-files), then run `/login`, press Enter on the **Cloud gateway** screen, and complete the browser sign-in. [Set the gateway URL](#set-the-gateway-url) below covers distributing both keys at scale.
  </Step>
</Steps>

## Connect developers

Developers connect from their own laptops with one browser sign-in, using their corporate work account. They don't need a claude.ai account, an API key, or a subscription, because requests to the model go through the gateway using the organization's upstream credential. Connection is driven by the [client-side managed settings](/en/claude-apps-gateway-config#client-side-managed-settings) you push via MDM, so there is no manual setup on the developer side; this section covers what the admin configures.

The CLI fingerprints the gateway's TLS leaf certificate on first connect and pins it per hostname. Publish the expected SHA-256 fingerprint alongside the gateway URL so developers have something to compare against. Get the fingerprint from the certificate file with `openssl x509 -noout -fingerprint -sha256 -in cert.pem`; the `/login` prompt shows the first 16 characters of the digest as lowercase hexadecimal with no separators.

When the certificate rotates, every developer sees the trust prompt again, so treat rotations as a planned event and republish the fingerprint.

Once signed in, the [model picker](/en/model-config) shows the models in the developer's `availableModels` allowlist, managed settings apply at startup and refresh hourly, and telemetry routes to your collector. Sessions refresh silently before `ttl_hours` expiry, and a failed refresh after IdP deprovisioning prompts a re-login.

### Set the gateway URL

Three keys go in the per-OS [managed settings file](/en/settings#settings-files) you deploy via MDM or directly on disk. `forceLoginMethod` and `forceLoginGatewayUrl` open `/login` directly on the **Cloud gateway** screen with the URL filled in, and `parentSettingsBehavior: "merge"` lets Claude Desktop deliver the gateway's policy to the Claude Code sessions it launches, explained in [Deliver policy to Claude Desktop sessions](#deliver-policy-to-claude-desktop-sessions):

```json theme={null}
{
  "forceLoginMethod": "gateway",
  "forceLoginGatewayUrl": "https://claude-gateway.internal.example.com",
  "parentSettingsBehavior": "merge"
}
```

The developer presses Enter to connect. The [first-connect TLS fingerprint prompt](#connect-developers) still appears.

A developer can't set this up manually. The login picker has no gateway option, and `forceLoginGatewayUrl` is ignored in a developer's own settings files. `forceLoginMethod` alone, without a URL, leaves the developer at a "Contact your IT administrator" message. The login keys belong in the file you push to machines, not in the gateway's `managed.policies[].cli` block, which only reaches clients that are already connected.

### Deliver policy to Claude Desktop sessions

Claude Desktop runs embedded Claude Code sessions and passes the gateway's policy to each session it launches. Claude Desktop gets that policy from the gateway itself. It's pointed at the gateway through its own managed configuration and signs in with its own flow, separate from the `forceLoginMethod` and `forceLoginGatewayUrl` keys in [Set the gateway URL](#set-the-gateway-url).

Settings passed by a launching process are parent settings. Claude Code ignores parent settings on any machine that has an admin-deployed managed source, unless the highest-priority source sets `parentSettingsBehavior: "merge"`.

#### Which machines need the opt-in

Machines that only run Claude Desktop need it, because parent settings are the only way the gateway's policy reaches embedded sessions. Without the opt-in those sessions run with none of the gateway's restrictions, and nothing warns you.

Machines where developers sign in through `/login` don't need it; every Claude Code invocation fetches its policy from the gateway directly. Fleets that configure a [`policyHelper`](/en/settings#compute-managed-settings-with-a-policy-helper) can't use it, because the helper's output replaces every other managed source and parent settings are never merged while a helper is configured.

#### Set the opt-in

Deploy the key, mirror it to the source that wins on each machine, then verify.

<Steps>
  <Step title="Deploy the opt-in in the managed settings file">
    The [snippet above](#set-the-gateway-url) already includes `parentSettingsBehavior: "merge"`, so the file you push to machines carries it.
  </Step>

  <Step title="Set the same key in any source that outranks the file">
    Only the highest-priority admin source's value counts. A managed-preferences plist on macOS or an HKLM policy on Windows outranks the `managed-settings.json` file, and the gateway's own remote managed settings outrank both, so on machines that sign in to the gateway, also set the key in the gateway policy's [`cli` block](/en/claude-apps-gateway-config#managed).
  </Step>

  <Step title="Check which source won">
    Call the Agent SDK's [`resolveSettings()`](/en/agent-sdk/typescript#resolvesettings). Its result includes a `sources` list; the managed policy entry there carries a `policyOrigin` field naming the active source. `resolveSettings()` doesn't execute a configured `policyHelper`, so on helper fleets its answer doesn't reflect the live session.
  </Step>
</Steps>

### Restrict parent settings

Once you deploy `parentSettingsBehavior: "merge"`, any host process that launches Claude Code can supply parent settings, not only Claude Desktop but also an Agent SDK application or an IDE extension.

Claude Code filters parent settings against an allowlist of restrictive keys, but some allowed keys can grant access rather than restrict it. Unless you set the `allowManaged*Only` locks, permission allow rules and sandbox allowlists supplied by the host still apply. Your policy's deny and ask rules stay in force either way; [they're evaluated before any allow rule](/en/permissions#manage-permissions).

#### Deploy the locks

To keep parent settings as close to restriction-only as the filter supports, add all five `allowManaged*Only` locks, and the allowlists they govern, to the same sources as the merge opt-in:

```json theme={null}
{
  "forceLoginMethod": "gateway",
  "forceLoginGatewayUrl": "https://claude-gateway.internal.example.com",
  "parentSettingsBehavior": "merge",
  "allowManagedPermissionRulesOnly": true,
  "allowManagedMcpServersOnly": true,
  "allowManagedHooksOnly": true,
  "allowedMcpServers": [{ "serverUrl": "https://mcp.internal.example.com/*" }],
  "sandbox": {
    "network": {
      "allowManagedDomainsOnly": true,
      "allowedDomains": ["github.com", "*.npmjs.org"]
    },
    "filesystem": {
      "allowManagedReadPathsOnly": true,
      "denyRead": ["~/"],
      "allowRead": ["~/projects"]
    }
  }
}
```

An OS policy, such as an HKLM registry policy or a managed-preferences plist, outranks this file, so deliver the whole snippet through it instead of the file. The gateway's remote managed settings outrank the OS policy and file sources but reach only connected clients. Mirror the locks, the allowlists, and the merge opt-in into the policy's [`cli` block](/en/claude-apps-gateway-config#managed) and keep this file deployed, because machines that never connect, including ones that only run Claude Desktop, get their policy from the file alone.

#### Lock behavior across sources

Setting one lock doesn't restrict the others; each key is documented in the [settings reference](/en/settings#available-settings). From an admin source below the winner, the two sandbox locks still apply, and `allowManagedPermissionRulesOnly` still blocks parent-supplied allow rules and `additionalDirectories`. The hooks and MCP server locks, and `allowManagedPermissionRulesOnly`'s effect on the developer's own rules, need the winning source. On [`policyHelper`](/en/settings#compute-managed-settings-with-a-policy-helper) fleets, the locks are read from the helper's output alone.

Each lock makes Claude Code ignore the developer's own entries for that setting, so include your organization's allowlists next to the locks. Locking network domains with an empty managed domain list blocks all sandboxed outbound traffic, and locking MCP servers with no managed or parent-supplied `allowedMcpServers` loads every server that `deniedMcpServers` doesn't block. `allowRead` entries only re-allow paths inside `denyRead` regions, so pair them with a managed `denyRead`.

#### Settings the locks don't cover

Four parent-supplied settings are honored even with all five locks set:

* **`forceLoginOrgUUID`**: Claude Code honors a parent-supplied value when no admin source sets an org UUID. Gateway sign-in doesn't check this key, so it matters only for fleets that also use first-party Anthropic logins. An org UUID in any admin source blocks the parent's value, but the value Claude Code enforces comes from the highest-priority source, so set `forceLoginOrgUUID` there.
* **`allowedMcpServers`**: Claude Code honors a parent-supplied allowlist when no admin source sets one, and `allowManagedMcpServersOnly` doesn't block it, because the lock enforces whichever list wins as the managed value, including a parent-supplied list when no admin source sets one. A list in any admin source blocks the parent's, but the list Claude Code enforces comes from the highest-priority source, so set `allowedMcpServers` there, next to the lock.
* **`availableModels`**: Claude Code honors a parent-supplied model list when the winning managed source doesn't set one. If your fleet restricts models, set `availableModels` in the winning source.
* **`strictPluginOnlyCustomization`**: this key passes the filter regardless of any lock, and it makes Claude Code ignore the developer's own customization, including protective hooks. No lock blocks it.

### CI pipelines and remote machines

There is no service-token flow for unattended pipelines. Gateway sign-in always runs the browser device flow, so a CI job with no developer to approve the sign-in can't authenticate; configure those against your provider directly.

Once a developer has signed in, every Claude Code invocation on that machine uses the gateway session, including non-interactive `claude -p` runs and sessions started by the Agent SDK, and the [gateway policy applies to all of them](/en/claude-apps-gateway-config#managed).

The device flow separates the polling CLI from the approving browser, so a remote development box with no display still works: the developer runs `/login` over SSH on the remote machine and opens the verification link in the browser on their laptop.

### What's enforced on developers

These guarantees apply to every signed-in gateway session.

* **Model access**: requests for models the policy doesn't grant return 400, and the `/model` picker is filtered to the policy's `availableModels` allowlist. Set [`enforceAvailableModels: true`](/en/model-config#default-model-behavior) in the policy so the Default option resolves to a model inside `availableModels` instead of to Claude Code's built-in default; without it, Default stays selectable and is rejected at request time if that model isn't granted.
* **Telemetry destination**: when [telemetry forwarding](/en/claude-apps-gateway-config#telemetry) is configured, the OTLP export endpoint is pinned to the gateway, and the gateway-pushed configuration overrides locally set `OTEL_*` variables.
* **Credentials**: the gateway token is the session's only credential. `ANTHROPIC_AUTH_TOKEN`, `ANTHROPIC_API_KEY`, `apiKeyHelper`, and any earlier claude.ai login are ignored while signed in, so developers don't need to log out of claude.ai first.
* **Managed settings**: locked keys can't be overridden locally. The CLI applies the policy at startup and on each hourly poll.
* **Startup**: signed-in sessions exit at startup with an error after about 10 seconds when the gateway is unreachable, rather than starting without their settings.
* **Deprovisioning**: a session whose user is disabled in the IdP expires within `ttl_hours` when the next refresh fails.

### What the organization can see

Usage telemetry carries the developer's identity, token counts, model, and latency to the organization's collector. The gateway doesn't log or store prompt or completion content. Whether richer telemetry such as logs and traces is collected, which can include commands and file paths, is the organization's [per-destination choice](/en/claude-apps-gateway-config#telemetry).

## Availability and limitations

The table covers which Claude Code features work when developers connect through the gateway, and what the gateway server itself supports. Where something isn't supported, the Notes column gives the alternative.

The gateway delivers the [`anthropic-beta`](https://platform.claude.com/docs/en/api/beta-headers) values the CLI sends to every upstream, so operators don't maintain a beta allowlist. For Amazon Bedrock, which ignores the header, the gateway moves the values into the request body's `anthropic_beta` field; the other upstreams receive the header as sent.

The CLI's gateway-session beta set omits first-party-only betas and the extended-cache-ttl beta, which is why those rows below show as not available.

| Feature                                                                                                                    | Status        | Notes                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------------------------------------------------------------------------------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Inference forwarding (Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, Microsoft Foundry, Anthropic) | Available     | With per-upstream model translation and failover. The Amazon Bedrock upstream uses the `bedrock-runtime` endpoint and the AWS default credential chain; the Amazon Bedrock [Mantle endpoint](/en/amazon-bedrock#use-the-mantle-endpoint) is not a supported upstream. The [Claude Platform on AWS upstream](/en/claude-apps-gateway-config#claude-platform-on-aws) requires Claude Code v2.1.198 or later on the gateway server. |
| Model access and managed settings by IdP group                                                                             | Available     | Model access is enforced server-side; managed settings are delivered per IdP group and applied by the CLI at the [managed settings tier](/en/settings#settings-precedence)                                                                                                                                                                                                                                                       |
| Telemetry fan-out (OTLP/HTTP)                                                                                              | Available     | Identity-stamped per export; both protobuf and JSON encodings                                                                                                                                                                                                                                                                                                                                                                    |
| OIDC identity providers                                                                                                    | Available     | Any OIDC-compliant IdP; the gateway runs standard OIDC discovery and the authorization-code flow. See [Identity provider setup](/en/claude-apps-gateway-deploy#identity-provider-setup) for per-IdP configuration                                                                                                                                                                                                                |
| Per-user and per-group spend limits                                                                                        | Available     | See [Spend limits](/en/claude-apps-gateway-spend-limits)                                                                                                                                                                                                                                                                                                                                                                         |
| Server-side web search                                                                                                     | Not available | The CLI can't see which upstream provider the gateway routes to, so it can't verify web search support and disables WebSearch on gateway sessions                                                                                                                                                                                                                                                                                |
| Standard prompt caching                                                                                                    | Available     | `cache_control` breakpoints are forwarded to every upstream                                                                                                                                                                                                                                                                                                                                                                      |
| 1-hour cache TTL                                                                                                           | Not available | The CLI omits the extended-cache-ttl beta on gateway sessions, because not every upstream the gateway can route to supports the 1-hour TTL, so prompt caching through the gateway uses the 5-minute TTL; see the beta-header note above                                                                                                                                                                                          |
| Auto mode                                                                                                                  | Available     | Follows the [third-party provider rules](/en/permission-modes#enable-auto-mode-on-bedrock-agent-platform-or-foundry): only the models eligible on third-party providers can use it. {/* min-version: 2.1.207 */}Before v2.1.207, auto mode on gateway sessions required setting `CLAUDE_CODE_ENABLE_AUTO_MODE=1`, deliverable through the managed policy `env` block                                                             |
| First-party-only optimizations such as global cache scope and token-efficient tools                                        | Not available | The CLI doesn't enable them on gateway sessions; see the beta-header note above                                                                                                                                                                                                                                                                                                                                                  |
| OTLP/gRPC                                                                                                                  | Not supported | OTLP over HTTP only                                                                                                                                                                                                                                                                                                                                                                                                              |
| SAML, LDAP, and other non-OIDC auth                                                                                        | Not supported | OIDC only. Front with an OIDC bridge if needed                                                                                                                                                                                                                                                                                                                                                                                   |
| Multi-tenant (multiple OIDC issuers)                                                                                       | Not supported | One issuer per gateway. Run separate instances                                                                                                                                                                                                                                                                                                                                                                                   |
| Windows server                                                                                                             | Not supported | Deploy on Linux. macOS for local development only                                                                                                                                                                                                                                                                                                                                                                                |
| Helm chart                                                                                                                 | Not available | The gateway runs as a standard stateless Deployment; see the [deployment guide](/en/claude-apps-gateway-deploy#kubernetes)                                                                                                                                                                                                                                                                                                       |
| Admin UI                                                                                                                   | Not available | Configuration is the YAML file; redeploy to change it                                                                                                                                                                                                                                                                                                                                                                            |

## Next steps

The quickstart leaves you with a minimal config running under Docker Compose. To take it further:

* Expand `gateway.yaml` beyond the minimal config, for example to add per-group RBAC, multi-upstream failover, or telemetry destinations. The [configuration reference](/en/claude-apps-gateway-config) covers every option.
* Move from Compose to a production deployment on Kubernetes or Cloud Run, set up your IdP properly, and review the security model. The [deployment and operations guide](/en/claude-apps-gateway-deploy) covers per-IdP setup, container image requirements, health probes, and troubleshooting.
* Put spend caps on individual developers or groups so a runaway workload can't consume your whole commitment. [Spend limits](/en/claude-apps-gateway-spend-limits) covers the admin API and how enforcement works.
* For a complete worked example on Google Cloud, with Cloud Run, Cloud SQL, and Secret Manager, see [Deploy on Google Cloud](/en/claude-apps-gateway-on-gcp).
