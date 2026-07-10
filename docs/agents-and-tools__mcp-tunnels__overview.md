# MCP tunnels

Securely connect Claude to MCP servers running in your private network without opening inbound ports or exposing services to the public internet.

---

MCP tunnels let you connect Claude to Model Context Protocol (MCP) servers that run inside your private network. Traffic flows over an outbound-only connection, so you don't need to open inbound firewall ports, expose services to the public internet, or allowlist Anthropic's IP ranges on your origin.

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them. They are provided "as-is" without any uptime, support, or continuity commitment, and they depend on a third-party network provider (Cloudflare) that makes no availability commitment for the underlying transport. Anthropic may modify or discontinue MCP tunnels at any time.
</Note>

For Zero Data Retention and HIPAA BAA eligibility, see [API and data retention](/docs/en/manage-claude/api-and-data-retention#feature-eligibility).

## How it works

The [tunnel stack](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) is two components that run inside your network:

* **[cloudflared](/docs/en/agents-and-tools/mcp-tunnels/concepts#components):** Cloudflare's open-source tunnel connector. It initiates outbound-only connections to the [tunnel edge](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) and carries encrypted traffic from Anthropic to your proxy.
* **[Proxy](/docs/en/agents-and-tools/mcp-tunnels/concepts#components):** Anthropic's routing component. It terminates [inner TLS](/docs/en/agents-and-tools/mcp-tunnels/concepts#components), validates that upstream IPs fall within an allowed range, and routes each request to the correct [upstream MCP server](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) based on hostname.

Each MCP server you expose gets a hostname under your tunnel domain (for example, `docs.<your-tunnel-domain>`). You attach these hostnames to a Managed Agent session in the Console, or pass them to the Messages API through the [MCP connector](/docs/en/agents-and-tools/mcp-connector).

## Prerequisites

Before deploying, make sure you have:

* A deployment target: a Kubernetes cluster, or a VM with Docker and Docker Compose.

* A tunnel. Create one in the Claude Console (see [Create a tunnel](/docs/en/agents-and-tools/mcp-tunnels/console#create-a-tunnel)) or through the API; the Helm chart's setup hook can also create one for you during install.

* A way for your stack to authenticate to the Tunnels API. Choose one:

  * **[Programmatic access](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (recommended).** Set up [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation) when you create the tunnel. Your stack mints short-lived API tokens from your identity provider, fetches the tunnel token, and generates and registers a CA certificate automatically. Requires permission to manage federation rules, a registered OIDC issuer, and a federation rule with the `workspace:manage_tunnels` scope.
  * **[Manual](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Supply static credentials yourself: the tunnel token from the Console and a server certificate signed by a CA you register there. See [Get the connection details](/docs/en/agents-and-tools/mcp-tunnels/console#get-the-connection-details) and [Add a CA certificate](/docs/en/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate).

* One or more MCP servers running in your private network. See [Remote MCP servers](/docs/en/agents-and-tools/remote-mcp-servers) for examples.

* Outbound connectivity as listed under [Network requirements](#network-requirements).

### Network requirements

| Component       | Destination                                          | Port / protocol  | Used during                     |
| --------------- | ---------------------------------------------------- | ---------------- | ------------------------------- |
| Setup component | `api.anthropic.com`                                  | 443 TCP          | Provisioning and token rotation |
| cloudflared     | Tunnel edge (`198.41.192.0/19`, `2606:4700:a0::/44`) | 7844 TCP and UDP | Runtime                         |
| Proxy           | Your upstream MCP servers                            | As configured    | Runtime                         |

## Security model

### Security layers

Three independent layers protect every request:

| Layer                                                                       | Protects against                                                         |
| --------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Outer mTLS between Anthropic and the transport provider, with IP validation | Unauthorized clients reaching the tunnel                                 |
| Inner TLS from Anthropic's backend to your proxy                            | Payload inspection by the transport provider or any network intermediary |
| OAuth on each MCP server                                                    | Unauthorized use of MCP tools by authenticated tunnel traffic            |

The tunnel transport runs on Cloudflare's network. Because the proxy terminates inner TLS using a certificate that only you hold, Cloudflare cannot read request or response payloads. Anthropic does not connect to a tunnel until a CA certificate is registered, so payloads are always encrypted when they cross Cloudflare's network. Cloudflare does receive connection metadata; see [What the transport provider can observe](#what-the-transport-provider-can-observe).

### Shared responsibility model

| Anthropic handles                                                         | Your organization handles                                                                                                                      |
| ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| Tunnel access control                                                     | All content and traffic that transits your tunnel, and compliance with applicable third-party acceptable-use policies (including Cloudflare's) |
| Validating your CA certificate before connecting to your proxy            | Adherence to the deployment guidance on these pages                                                                                            |
| Ensuring Claude only sends requests to tunnels owned by your organization | Securing tunnel tokens and TLS private keys                                                                                                    |
|                                                                           | Managing the server certificate and renewing it before it expires                                                                              |
|                                                                           | Configuring OAuth on each MCP server                                                                                                           |
|                                                                           | Restricting network access for the proxy and MCP servers                                                                                       |
|                                                                           | Notifying Anthropic if you suspect a breach                                                                                                    |

<Warning>
  If an attacker obtains your tunnel token **and** one of your TLS private keys, they could impersonate your proxy and read MCP request payloads. Treat both as high-value secrets. See [MCP tunnels security](/docs/en/agents-and-tools/mcp-tunnels/security) for hardening guidance.
</Warning>

### What the transport provider can observe

Cloudflare provides the outbound transport. It cannot read MCP request or response payloads, but it does receive the following connection metadata:

* the egress IP address of the host running cloudflared
* a cloudflared host fingerprint
* connection timing and byte-volume
* the `*.tunnel.anthropic.com` subdomain assigned to your tunnel

Anthropic's agreement with Cloudflare restricts Cloudflare's use of this telemetry. Cloudflare acts as a subprocessor for this research preview.

## Deploy a tunnel

If you're new to MCP tunnels, start with the quickstart to get a working tunnel locally before configuring a production deployment.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/docs/en/agents-and-tools/mcp-tunnels/quickstart">
    The shortest path to a working tunnel: Docker Compose with a sample MCP server.
  </Card>

  <Card title="Deploy with Helm" icon="stack" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-helm">
    Install on a Kubernetes cluster using the Anthropic Helm chart.
  </Card>

  <Card title="Deploy with Docker Compose" icon="cube" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-compose">
    Install on a VM using Docker Compose.
  </Card>
</CardGroup>

Choosing between them:

* **Deployment target**

  * **Helm** when deploying to Kubernetes.
  * **Docker Compose** for a single host or local testing.

* **Authentication for setup**

  * **Programmatic access** (through Workload Identity Federation) when you have an OIDC identity provider such as a Kubernetes cluster, cloud IAM, or SPIFFE.
  * **Manual credentials** when you don't, or when you're testing.

## Use the tunneled MCP servers

Once your tunnel is active (it has an active CA certificate and your tunnel stack is connected), the upstream MCP servers are reachable from Claude Managed Agents and the Messages API.

<Note>
  MCP tunnels created through the Console are not available as connectors in claude.ai.
</Note>

In both cases, the tunnel carries encrypted traffic to your MCP server but does not authenticate to it. If the upstream MCP server requires its own authentication (OAuth, bearer token), supply it the same way you would for any other MCP server; it is independent of the tunnel.

### Managed Agents (Console)

1. In **Managed Agents > Sessions**, create a session and choose **Create new agent** so you can edit the MCP server list.
2. Click **+ MCP Server** and open the dropdown. Tunnels in the session's workspace that have at least one active certificate appear at the top of the list, above the public connector catalog.
3. Select the tunnel and supply the **Subdomain** that your proxy routes to a specific MCP server, and the **Path** the upstream MCP server expects. The **Resolves to** line shows the exact URL.

### Messages API

Pass the upstream MCP server's URL in the `mcp_servers` array, the same way as any other remote MCP server. The request body and `anthropic-beta` header follow the standard [MCP connector](/docs/en/agents-and-tools/mcp-connector) format; only the `url` is tunnel-specific. The following example uses the MCP connector's `mcp-client` beta header, which is separate from the `mcp-tunnels` beta used by the [Tunnels API](/docs/en/agents-and-tools/mcp-tunnels/reference). Use an API key for the workspace the tunnel was created in (Console **Settings > API keys**).

The URL's host is `<subdomain>.<your-tunnel-domain>`. The path depends on your upstream MCP server, not the tunnel: FastMCP's `streamable-http` transport serves at `/mcp`, and other servers may use `/` or a custom path (check the server's documentation). The proxy forwards the path untouched.

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: mcp-client-2025-11-20" \
  -d '{
    "model": "claude-opus-4-8",
    "max_tokens": 1000,
    "messages": [{"role": "user", "content": "Use the hello tool to greet tunnel."}],
    "mcp_servers": [
      {
        "type": "url",
        "url": "https://echo.YOUR_TUNNEL_DOMAIN_HERE/mcp",
        "name": "echo"
      }
    ],
    "tools": [{"type": "mcp_toolset", "mcp_server_name": "echo"}]
  }'
```

For SDK examples in every language, see [MCP connector](/docs/en/agents-and-tools/mcp-connector); the only tunnel-specific value is the `url`.

## Next steps

<CardGroup cols={2}>
  <Card title="Security" icon="lock" href="/docs/en/agents-and-tools/mcp-tunnels/security">
    Hardening guidance, credential rotation, and breach response.
  </Card>

  <Card title="Troubleshooting" icon="wrench" href="/docs/en/agents-and-tools/mcp-tunnels/troubleshooting">
    Diagnose connectivity, TLS, and routing issues.
  </Card>

  <Card title="Reference" icon="book" href="/docs/en/agents-and-tools/mcp-tunnels/reference">
    Proxy config fields, the Tunnels API, certificate requirements, and the setup component.
  </Card>

  <Card title="MCP connector" icon="link" href="/docs/en/agents-and-tools/mcp-connector">
    Use tunneled servers from the Messages API.
  </Card>
</CardGroup>
