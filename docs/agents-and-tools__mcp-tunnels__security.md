# MCP tunnels security

Hardening guidance, credential rotation, breach response, and teardown for MCP tunnel deployments.

---

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them.
</Note>

The tunnel architecture provides strong defaults (outbound-only connectivity, end-to-end encryption, and IP validation), but the overall security of your [tunnel stack](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) also depends on how you configure and operate it. This page covers recommended hardening, breach response, and how to decommission a tunnel.

## Best practices

* **Require OAuth on every MCP server.** Configure each [upstream MCP server](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) to require OAuth as described in the [MCP authorization spec](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization). OAuth provides defense in depth on top of the tunnel's transport authentication and enables user-level authorization at the data layer.
* **Enable SSO for your organization.** Tunnels, federation rules, and service accounts are managed in the Claude Console. SSO enforces your identity provider's session controls on the admins who can change them.
* **Restrict `upstream.allowed_ips`.** Use the smallest CIDR ranges that cover your MCP servers. This is the [proxy](/docs/en/agents-and-tools/mcp-tunnels/concepts#components)'s primary SSRF defense.
* **Monitor logs.** Alert on warnings, errors, and unusual traffic patterns from the tunnel stack.
* **Rotate credentials.** Rotate the server certificate and tunnel token on a regular schedule, and immediately if you suspect compromise.
* **Keep images updated.** Track new proxy releases and pin images by SHA-256 digest.
* **Limit network reach.** The proxy and [cloudflared](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) should only be able to reach the destinations listed in the [network requirements](/docs/en/agents-and-tools/mcp-tunnels/overview#network-requirements). Use NetworkPolicy (Kubernetes) or host firewall rules (Compose).
* **Limit MCP server scope.** Each server should expose only the tools and data required for its purpose.
* **Protect credentials at rest.** Apply your organization's secrets-management practices to private keys and tunnel tokens.

## Respond to a suspected breach

If you believe your tunnel token, TLS keys, or proxy host has been compromised:

<Steps>
  <Step title="Stop the tunnel stack">
    <Tabs>
      <Tab title="Helm">
        ```bash
        helm uninstall mcp-tunnel -n mcp-tunnel
        ```
      </Tab>

      <Tab title="Docker Compose">
        ```bash
        docker compose down --timeout 0
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Detach the upstream MCP servers">
    Remove the upstream MCP servers from any Managed Agent sessions that use them, and stop passing their URLs in the `mcp_servers` block of Messages API requests.
  </Step>

  <Step title="Archive the tunnel">
    Archiving invalidates the tunnel token and detaches the domain. In the Console, [archive the tunnel](/docs/en/agents-and-tools/mcp-tunnels/console#archive-a-tunnel) from the **MCP tunnels** list. To archive over the API instead, see [Archive a tunnel](/docs/en/api/beta/tunnels/archive).
  </Step>

  <Step title="Contact Anthropic">
    Report the suspected compromise to Anthropic support.
  </Step>

  <Step title="Rotate downstream credentials">
    Re-provision a fresh tunnel and rotate any OAuth tokens that the affected MCP servers issued.
  </Step>

  <Step title="Review logs before restoring service">
    Inspect proxy, cloudflared, and MCP server logs for the window of suspected compromise before bringing the new tunnel online.
  </Step>
</Steps>

## Tear down a tunnel

Follow these steps to decommission a tunnel and remove all stored credentials.

<Steps>
  <Step title="Stop the tunnel stack">
    <Tabs>
      <Tab title="Helm">
        ```bash
        helm uninstall mcp-tunnel -n mcp-tunnel
        ```
      </Tab>

      <Tab title="Docker Compose">
        ```bash
        docker compose down
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Archive the tunnel">
    In the Console, [archive the tunnel](/docs/en/agents-and-tools/mcp-tunnels/console#archive-a-tunnel) from the **MCP tunnels** list.
  </Step>

  <Step title="Remove stored credentials">
    <Tabs>
      <Tab title="Helm">
        With programmatic access, the setup component created a single Secret named after the release. Without programmatic access, you created `mcp-tunnel-token` and `mcp-tunnel-cert` yourself. Delete whichever apply:

        ```bash
        kubectl -n mcp-tunnel delete secret \
          mcp-tunnel mcp-tunnel-token mcp-tunnel-cert \
          --ignore-not-found
        ```
      </Tab>

      <Tab title="Docker Compose">
        Private keys and certificates live in `data/`. The tunnel token lives in `data/tunnel-token` (programmatic flow) or in your shell environment (manual flow). The `config/` directory and `docker-compose.yaml` contain no secrets; keep them if you plan to re-provision, or remove them as well.

        ```bash
        sudo rm -rf data
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>
