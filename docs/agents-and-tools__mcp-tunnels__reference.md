# MCP tunnels reference

Proxy configuration fields, the Tunnels REST API, certificate requirements, and the setup component.

---

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them.
</Note>

## Proxy configuration

The [proxy](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) reads its configuration from `/etc/mcp-gateway/config.yaml` (Compose) or the rendered ConfigMap (Helm, populated from `gateway.config.*`).

| Field                             | Description                                                                                                                                                                                                     | Default                                         |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------- |
| `listen_addr`                     | Address and port to listen on.                                                                                                                                                                                  | Required                                        |
| `log_level`                       | Logging verbosity: `debug`, `info`, `warn`, or `error`.                                                                                                                                                         | `info`                                          |
| `shutdown_timeout`                | How long to wait for in-flight requests during graceful shutdown.                                                                                                                                               | `30s`                                           |
| `tunnel_domain`                   | Base domain assigned to the tunnel. When set, route lookup strips this suffix from incoming hostnames so `routes` keys can be bare subdomains (`wiki`). When empty, `routes` keys must be exact full hostnames. | Required when `routes` keys are bare subdomains |
| `tls.cert_file`                   | Path to the server TLS certificate.                                                                                                                                                                             | Required                                        |
| `tls.key_file`                    | Path to the server TLS private key.                                                                                                                                                                             | Required                                        |
| `routes`                          | Map of subdomain or full hostname to upstream URL. See [Route matching](#route-matching).                                                                                                                       | Required                                        |
| `upstream.allowed_ips`            | IPv4 CIDR ranges or single addresses the proxy is permitted to connect to. Mutually exclusive with `disable_ip_validation`.                                                                                     | RFC1918 private ranges                          |
| `upstream.disable_ip_validation`  | Disable upstream IP validation entirely. Mutually exclusive with `allowed_ips`.                                                                                                                                 | `false`                                         |
| `upstream.tls.ca_file`            | CA bundle for validating upstream TLS.                                                                                                                                                                          | None                                            |
| `upstream.tls.include_system_cas` | Also trust the system CA bundle for upstream TLS.                                                                                                                                                               | `false`                                         |

For `https://` upstream routes, set at least one of `upstream.tls.ca_file` or `upstream.tls.include_system_cas`; otherwise the proxy has no trust anchor for the upstream certificate.

### Route matching

`routes` is a flat string map (`map[string]string`), not a list. The proxy looks up the incoming hostname by exact match first, then by stripping the `tunnel_domain` suffix and matching the remaining subdomain. The match considers only the hostname; the request path and query string are forwarded to the [upstream MCP server](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) unchanged.

Each upstream value must be exactly `scheme://host:port`. The port is mandatory. Including a path is rejected at config load with `invalid upstream (must be scheme://host:port)`.

## Tunnels API

The Tunnels REST API lives at `/v1/tunnels` and supports creating, listing, and archiving tunnels, registering CA certificates, and revealing or rotating the tunnel token. See the [Tunnels API reference](/docs/en/api/beta/tunnels/list) for all endpoints, request and response schemas, and examples.

<Note>
  The previous Admin API surface at `/v1/organizations/tunnels` (beta header `mcp-tunnels-2026-05-19`, scope `org:manage_tunnels`) continues to work during a migration window and remains documented in the [Admin API reference](/docs/en/api/admin/mcp_tunnels) with a deprecation notice. To migrate, update the path to `/v1/tunnels`, the beta header to `mcp-tunnels-2026-06-22`, and your WIF token scope to `workspace:manage_tunnels`.
</Note>

<Warning>
  All MCP tunnels endpoints require a bearer token with the `workspace:manage_tunnels` scope obtained through [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation). Admin API keys are not accepted.
</Warning>

Required headers on every request:

| Header              | Value                                      |
| ------------------- | ------------------------------------------ |
| `Authorization`     | `Bearer <token>` (the WIF-exchanged token) |
| `anthropic-version` | `2023-06-01`                               |
| `anthropic-beta`    | `mcp-tunnels-2026-06-22`                   |

## Certificate requirements

The [setup component](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) generates compliant certificates automatically. These requirements apply only if you issue certificates through your own PKI.

### CA certificate

Upload with `POST /v1/tunnels/{tunnel_id}/certificates`. A tunnel can hold up to two active CA certificates at a time, which allows zero-downtime rotation.

* PEM-encoded, single certificate, up to 8 kB.
* `BasicConstraints` extension present with `CA:TRUE`, marked critical.
* `SubjectKeyIdentifier` extension present.
* `KeyUsage` includes `keyCertSign`.
* Within its validity period.
* RSA 2048-bit or larger, or ECDSA P-256 or larger, with a SHA-256 or stronger signature.

### Server certificate

Presented by the proxy during [inner TLS](/docs/en/agents-and-tools/mcp-tunnels/concepts#components).

* Signed directly by a registered CA (no intermediates).
* `AuthorityKeyIdentifier` extension present and matching the CA's `SubjectKeyIdentifier`.
* Subject Alternative Name includes a DNS name matching `<route>.<tunnel-domain>`. A wildcard `*.<tunnel-domain>` covers all routes.
* If the `ExtendedKeyUsage` extension is present, it includes `serverAuth`.
* Within its validity period.
* RSA 2048-bit or larger, or ECDSA P-256 or larger, with a SHA-256 or stronger signature.

The setup component generates an ECDSA P-256 CA with five-year validity and an RSA 4096-bit server certificate with a wildcard SAN and 90-day validity.

## Setup component

The setup component ships inside the `mcp-proxy` image as the `setup` binary. Run it with `docker compose run --rm setup <subcommand>` (Compose) or rely on the chart's hooks and CronJobs (Helm).

### `setup init`

Attaches to an existing tunnel (or creates one when no tunnel ID is supplied), then generates a CA and server certificate, registers the CA, retrieves the tunnel token, and writes all outputs to the destination.

| Flag              | Description                                                                                                                                                           | Default                                                                                      |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `--api-url`       | Claude API base URL. Also read from `API_URL`.                                                                                                                        | Required                                                                                     |
| `--tunnel-id`     | Tunnel ID to attach to (`tnl_...`). Also read from `TUNNEL_ID`. When omitted, a new tunnel is created; a tunnel ID already stored in the output is reused on re-runs. | None (create a tunnel)                                                                       |
| `--output`        | Output destination: `dir:/path` or `k8s-secret:NAME`. The Helm chart passes `k8s-secret:<release>`.                                                                   | `k8s-secret:mcp-tunnel` (auto-detected when running in a Kubernetes pod; required otherwise) |
| `--cert-duration` | Server certificate validity period.                                                                                                                                   | `2160h` (90 days)                                                                            |
| `--token-version` | Change-detection string. A new value triggers token rotation on re-run. The Helm chart and the Compose example both pass `1` as the initial value.                    | None                                                                                         |

The command authenticates through [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation). It reads `ANTHROPIC_FEDERATION_RULE_ID`, `ANTHROPIC_ORGANIZATION_ID`, `ANTHROPIC_WORKSPACE_ID` (optional), and exactly one of `ANTHROPIC_IDENTITY_TOKEN_FILE` or `ANTHROPIC_IDENTITY_TOKEN`. See the [WIF reference](/docs/en/manage-claude/wif-reference) for the current semantics of these variables; the setup component derives the service account from the federation rule, so it does not require `ANTHROPIC_SERVICE_ACCOUNT_ID` separately.

### `setup renew-cert`

Issues a new server certificate signed by the stored CA. Makes no API calls.

| Flag              | Description                                                                                         | Default                                                                                      |
| ----------------- | --------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `--output`        | Output destination: `dir:/path` or `k8s-secret:NAME`. The Helm chart passes `k8s-secret:<release>`. | `k8s-secret:mcp-tunnel` (auto-detected when running in a Kubernetes pod; required otherwise) |
| `--cert-duration` | New certificate validity period.                                                                    | `2160h` (90 days)                                                                            |
| `--renew-before`  | Skip renewal if the existing certificate has more than this duration remaining.                     | `0` (always renew)                                                                           |

Setting `--renew-before=720h` makes the command a no-op when more than 30 days of validity remain, so it's safe to run on a fixed schedule.
