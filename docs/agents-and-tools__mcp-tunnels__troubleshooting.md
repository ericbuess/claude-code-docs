# Troubleshoot MCP tunnels

Diagnose connectivity, TLS, IP validation, and OAuth routing issues in a tunnel stack.

---

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them.
</Note>

A request through the tunnel can fail at one of three layers; diagnose them in order: the outbound connection to the [tunnel edge](/docs/en/agents-and-tools/mcp-tunnels/concepts#components), the [inner TLS](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) from Anthropic to your [proxy](/docs/en/agents-and-tools/mcp-tunnels/concepts#components), then routing and IP validation toward the [upstream MCP server](/docs/en/agents-and-tools/mcp-tunnels/concepts#components).

## Quick reference

| Symptom                                                                                                                             | Cause                                                                                               | Fix                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Tunnel doesn't appear in the agent **+ MCP Server** picker                                                                          | The picker only lists tunnels in the session's workspace that have at least one active certificate. | Register a CA certificate, or open the session in the workspace the tunnel was created in.                                                 |
| Caller sees HTTP 500; [cloudflared](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) logs `No ingress rules were defined` | cloudflared has no local target.                                                                    | Add `--url http://localhost:8080` and `network_mode: "service:mcp-proxy"` to the cloudflared service.                                      |
| Proxy logs `no route for host`                                                                                                      | `tunnel_domain` doesn't match the assigned domain, or `config.yaml` was edited without restarting.  | Set `tunnel_domain` to the exact domain shown on the tunnel detail page, then restart the proxy (`docker compose restart mcp-proxy`).      |
| Proxy logs `IP validation failed: <ip> is not a private address`                                                                    | Upstream MCP server resolves outside RFC1918.                                                       | See [Upstream IP validation](#upstream-ip-validation).                                                                                     |
| Proxy exits with `cannot unmarshal !!seq into map[string]string`                                                                    | `routes` is a YAML list.                                                                            | Use `routes: { name: http://host:port }`.                                                                                                  |
| Proxy exits with `open /data/tls.key: permission denied`                                                                            | The key is `0600`; the proxy container runs non-root.                                               | `chmod 644 data/tls.key`.                                                                                                                  |
| `curl https://<proxy>:8080` fails with `wrong version number`                                                                       | Expected; the listener is plaintext WebSocket. TLS happens inside the WS stream.                    | Verify through a [Managed Agent or the Messages API](/docs/en/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers) instead. |

The following sections cover failures that need more than a one-line fix.

## OAuth fails behind a source-IP allowlist

OAuth flows fail when your authorization server's source-IP allowlist blocks Anthropic's backend from reaching `/token`, `/register`, and the discovery endpoints. If you'd rather not allowlist Anthropic's egress ranges, you can route the backend-to-backend OAuth calls through the tunnel while keeping the browser-facing `/authorize` endpoint on your existing public hostname.

<Steps>
  <Step title="Add a proxy route for the authorization server">
    ```yaml
    routes:
      mcp: http://your-mcp-server:8080
      auth: http://your-auth-server:8080
    ```

    Restart the proxy after editing `routes` (`docker compose restart mcp-proxy`, or `helm upgrade`).
  </Step>

  <Step title="Serve split-endpoint discovery metadata">
    Your authorization server's `/.well-known/oauth-authorization-server` response should point `authorization_endpoint` at your existing allowlisted hostname and everything else at the tunnel:

    ```json
    {
      "issuer": "https://auth.<tunnel-domain>",
      "authorization_endpoint": "https://<your-allowlisted-host>/authorize",
      "token_endpoint": "https://auth.<tunnel-domain>/token",
      "registration_endpoint": "https://auth.<tunnel-domain>/register",
      "code_challenge_methods_supported": ["S256"]
    }
    ```
  </Step>

  <Step title="Point the MCP server at the tunnel issuer">
    Your MCP server's `/.well-known/oauth-protected-resource` response should reference the tunnel hostname as its authorization server:

    ```json
    {
      "resource": "https://mcp.<tunnel-domain>",
      "authorization_servers": ["https://auth.<tunnel-domain>"]
    }
    ```
  </Step>
</Steps>

With this configuration, the user's browser hits `/authorize` on your existing hostname (which your allowlist already permits), while Anthropic's backend reaches `/token`, `/register`, and the discovery documents through the tunnel.

## Setup component authentication failures

The [setup component](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) (Helm Job or Compose `setup` service) authenticates to the Tunnels API by exchanging an OIDC JWT through your federation rule. When the exchange fails, see [Troubleshoot a failed exchange](/docs/en/manage-claude/wif-reference#troubleshoot-a-failed-exchange) in the Workload Identity Federation reference; the failure modes (subject, audience, issuer, JWKS, lifetime) are the same.

Tunnels-specific causes:

* The chart's default audience is `api.anthropic.com` (no scheme). If your rule's audience is `https://api.anthropic.com`, set `api.wif.audience` to match.
* A `403` from the Tunnels API after a successful exchange means the rule's scope doesn't include `workspace:manage_tunnels`, or the rule's service account isn't a member of the tunnel's workspace. Set the scope and add the service account to the workspace.

On Helm, the setup component runs as a pre-install hook Job. On failure, the Job is left behind for inspection (`kubectl logs job/mcp-tunnel-setup -n mcp-tunnel`). Helm doesn't manage hook resources, so delete it before retrying:

```bash
helm uninstall mcp-tunnel -n mcp-tunnel
kubectl -n mcp-tunnel delete job mcp-tunnel-setup
```

## Tunnel won't connect

Check the cloudflared logs first. Common causes:

* The `TUNNEL_TOKEN` is missing, expired, or copied incorrectly.
* A firewall is blocking outbound TCP/UDP on port 7844 to the tunnel edge.

cloudflared may also log warnings about UDP receive buffer sizes; this is a QUIC tuning hint, not an error.

## Certificate errors

When Anthropic rejects the proxy's certificate during inner TLS, the proxy logs `tls handshake failed`. Verify that:

* The server certificate has not expired.
* The certificate's Subject Alternative Name matches `*.<tunnel-domain>`.
* The signing CA is registered with Anthropic for this tunnel.

See the [certificate requirements](/docs/en/agents-and-tools/mcp-tunnels/reference#certificate-requirements) for the full validation rules.

## Upstream IP validation

For SSRF protection, the proxy only dials addresses in the RFC1918 private ranges (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) by default. Only IPv4 is supported for the proxy-to-upstream connection. (The cloudflared-to-edge egress range in [Network requirements](/docs/en/agents-and-tools/mcp-tunnels/overview#network-requirements) is a different hop.)

If the proxy logs `IP validation failed: <ip> is not a private address`, the upstream hostname resolved outside that set. On Kubernetes, some managed distributions allocate the Service CIDR outside RFC1918; if `kubectl get svc kubernetes -n default -o jsonpath='{.spec.clusterIP}'` returns an address outside the private ranges, look up your cluster's Service CIDR and add it.

If the address is legitimate, add the narrowest covering CIDR to `upstream.allowed_ips`. Setting `allowed_ips` **replaces** the RFC1918 default rather than extending it, so include the private ranges your other upstream MCP servers use:

```yaml config/mcp-proxy.yaml
upstream:
  allowed_ips:
    - 10.0.0.0/8
    - 172.16.0.0/12
    - 192.168.0.0/16
    - 127.0.0.0/8       # loopback, for local testing only
```

<Warning>
  Avoid `0.0.0.0/0` outside of local testing; it disables SSRF protection entirely.
</Warning>
