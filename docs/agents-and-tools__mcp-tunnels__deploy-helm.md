# Deploy MCP tunnels with Helm

Install the tunnel stack on a Kubernetes cluster using the Anthropic Helm chart.

---

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them.
</Note>

The Anthropic Helm chart installs the [tunnel stack](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) as a single Deployment and attaches it to your tunnel: one the chart's setup hook creates for you, or an existing tunnel you created in the [Console](/docs/en/agents-and-tools/mcp-tunnels/console#create-a-tunnel).

## Before you begin

You need:

* **A tunnel.** With programmatic access, the chart's setup hook creates one for you when you don't supply a tunnel ID; to attach to an existing tunnel instead, [create it in the Console](/docs/en/agents-and-tools/mcp-tunnels/console#create-a-tunnel) and record the tunnel ID (`tnl_...`). Manual provisioning always starts from a Console-created tunnel; you'll also need its tunnel token and tunnel domain.

* **A way for the chart to authenticate to the Tunnels API.**

  * **[Programmatic access](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) (recommended).** The [setup component](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) authenticates through Workload Identity Federation, fetches the tunnel token, generates a CA, registers it with Anthropic, and stores everything in a Secret. You'll need a federation rule scoped to `workspace:manage_tunnels`.
  * **[Manual](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning).** Skip programmatic access. You'll [get the tunnel token from the Console](/docs/en/agents-and-tools/mcp-tunnels/console#get-the-connection-details), generate a CA and server certificate yourself, [register the CA in the Console](/docs/en/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate), and supply the credentials to the cluster as Secrets.

* **A Kubernetes cluster** you can deploy to with `helm` and `kubectl`. The **Without programmatic access** tab also uses `openssl` (1.1.1 or later).

* **Outbound network connectivity** from the cluster to `api.anthropic.com` (443 TCP) and the [tunnel edge](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) (7844 TCP and UDP). See the full [network requirements](/docs/en/agents-and-tools/mcp-tunnels/overview#network-requirements).

* **One or more MCP servers** running and reachable from the cluster on the addresses you'll configure under `gateway.config.routes`. If you don't have one yet, [use the sample server](#optional-use-a-sample-mcp-server).

## Optional: Use a sample MCP server

If you don't have an MCP server available for testing, use this minimal one:

```bash
kubectl create namespace mcp-tunnel --dry-run=client -o yaml | kubectl apply -f -
kubectl -n mcp-tunnel apply -f - <<'EOF'
apiVersion: v1
kind: ConfigMap
metadata:
  name: hello-mcp-src
data:
  hello_server.py: |
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP("hello-server", host="0.0.0.0", port=9000)


    @mcp.tool()
    def hello(name: str = "world") -> str:
        """Say hello to someone."""
        return f"Hello, {name}!"


    if __name__ == "__main__":
        mcp.run(transport="streamable-http")
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-mcp
spec:
  replicas: 1
  selector:
    matchLabels: { app: hello-mcp }
  template:
    metadata:
      labels: { app: hello-mcp }
    spec:
      containers:
        - name: hello-mcp
          image: python:3.13-slim
          command: ["sh", "-c", "pip install --quiet mcp && python /app/hello_server.py"]
          volumeMounts:
            - { name: src, mountPath: /app }
          ports:
            - { containerPort: 9000 }
      volumes:
        - name: src
          configMap: { name: hello-mcp-src }
---
apiVersion: v1
kind: Service
metadata:
  name: hello-mcp
spec:
  selector: { app: hello-mcp }
  ports:
    - { port: 9000, targetPort: 9000 }
EOF
```

The Install steps that follow note where to add the corresponding route.

## Install

<Tabs>
  <Tab title="With programmatic access">
    The setup component exchanges the cluster's projected ServiceAccount token through your federation rule, fetches the tunnel token, generates a CA and server certificate, and registers the CA with Anthropic. A daily CronJob renews the server certificate as needed, so you don't handle any secrets by hand.

    <Steps>
      <Step title="Set up Workload Identity Federation for the cluster">
        Follow [Use WIF with Kubernetes](/docs/en/manage-claude/wif-providers/kubernetes) to register your cluster's OIDC issuer and create a federation rule. The setup component runs under its own ServiceAccount in the release namespace; the exact name follows Helm's `fullname` convention, so for any release name other than `mcp-tunnel`, run `helm template <release> ... | grep -A2 'kind: ServiceAccount'` to confirm it before creating the rule. The rest of this guide assumes release name `mcp-tunnel` in namespace `mcp-tunnel`, where the ServiceAccount is `mcp-tunnel-setup`.

        | Field    | Value                                                |
        | -------- | ---------------------------------------------------- |
        | Subject  | `system:serviceaccount:mcp-tunnel:mcp-tunnel-setup`  |
        | Audience | `api.anthropic.com` (the chart's default; no scheme) |
        | Scope    | `workspace:manage_tunnels`                           |

        <Note>
          The chart's default audience is `api.anthropic.com` with no scheme, but the Console's federation-rule form suggests `https://api.anthropic.com`. The two must match byte-for-byte or authentication fails. Either set the rule's audience to `api.anthropic.com`, or set `api.wif.audience` in `values.yaml` to `https://api.anthropic.com`.
        </Note>

        If the tunnel is in a workspace other than the organization's default, also add the rule's service account as a member of that workspace under **Settings > Workspaces** (the Tunnels API authorizes against the service account's workspace memberships).

        Note the rule's ID (`fdrl_...`); you'll set it as `api.wif.federationRuleId`.

        <Note>
          The daily certificate-renewal CronJob uses a separate ServiceAccount (also derived from the Helm `fullname`) but does not call the Tunnels API; it renews the certificate locally and only needs Kubernetes RBAC, which the chart grants. The federation rule does not need to cover it.
        </Note>
      </Step>

      <Step title="Fetch the default values">
        ```bash
        helm show values \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 > values.yaml
        ```
      </Step>

      <Step title="Configure tunnel attachment and routes">
        Edit `values.yaml` and set the `api.wif.*` keys with the federation rule ID and organization ID, plus a `routes` entry for each [upstream MCP server](/docs/en/agents-and-tools/mcp-tunnels/concepts#components):

        ```yaml values.yaml
        api:
          wif:
            federationRuleId: "fdrl_..."
            organizationId: "00000000-0000-0000-0000-000000000000"
            # Set when the tunnel is in a non-default workspace and the
            # rule's service account is a member of that workspace.
            # workspaceId: "wrkspc_..."

        tunnel:
          # Leave empty to have the setup hook create a tunnel during install.
          # Set to attach to an existing tunnel from the Console.
          id: ""
          # Increment to rotate the tunnel token on the next upgrade.
          # See the "Rotate the tunnel token" section.
          tokenVersion: "1"

        gateway:
          config:
            routes:
              docs: http://docs-mcp.internal:8080
              search: http://search-mcp.internal:8080
        ```

        With these routes, Claude reaches the servers at `docs.<your-tunnel-domain>` and `search.<your-tunnel-domain>`. Some managed Kubernetes distributions allocate the Service CIDR outside the standard private ranges; if your routes target in-cluster Services, add `gateway.config.upstream.allowed_ips` here per [Upstream IP validation](/docs/en/agents-and-tools/mcp-tunnels/troubleshooting#upstream-ip-validation).

        <Note>
          If you're using the [sample MCP server](#optional-use-a-sample-mcp-server), set `routes` to `echo: http://hello-mcp:9000` instead.
        </Note>
      </Step>

      <Step title="Review the rendered manifests">
        Render the chart and review the output according to your organization's vetting practices:

        ```bash
        helm template mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          -n mcp-tunnel \
          -f values.yaml > rendered.yaml
        ```
      </Step>

      <Step title="Install">
        ```bash
        helm install mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          --namespace mcp-tunnel --create-namespace \
          -f values.yaml
        ```

        The setup component runs as a Helm pre-install hook Job, so `helm install` blocks until it completes. On success Helm deletes the Job automatically. If `helm install` fails with a hook error, see [Setup component authentication failures](/docs/en/agents-and-tools/mcp-tunnels/troubleshooting#setup-component-authentication-failures).

        When `tunnel.id` is empty, the setup component creates the tunnel in the workspace your federation rule targets (the organization's default workspace unless you set `api.wif.workspaceId`) and stores its ID and domain in the `mcp-tunnel` Secret. Find the domain you'll need for [verification](#verify-the-deployment) on the tunnel's detail page in the Console under **Manage > MCP tunnels**, or read it from the Secret:

        ```bash
        kubectl -n mcp-tunnel get secret mcp-tunnel \
          -o jsonpath='{.data.tunnel-domain}' | base64 -d
        ```

        Re-running the setup component (during [upgrades](#upgrades) or [token rotation](#rotate-the-tunnel-token)) reuses the tunnel ID stored in this Secret; it never creates a second tunnel.

        <Warning>
          The `api.wif.*` values are identifiers, not secrets, so storing them in Helm release-history Secrets is not a risk. The sensitive data at rest is the `mcp-tunnel` Secret the setup component creates, which holds the tunnel token and TLS private keys. Apply your organization's standard practices for protecting Kubernetes Secrets to this namespace.
        </Warning>
      </Step>
    </Steps>
  </Tab>

  <Tab title="Without programmatic access">
    In this mode (`setup.enabled: false`) the chart makes no API calls; the setup component does not run and there is no cert-renew CronJob. Use this path if you'd rather not set up Workload Identity Federation.

    <Steps>
      <Step title="Get the tunnel token and domain">
        [Create the tunnel](/docs/en/agents-and-tools/mcp-tunnels/console#create-a-tunnel) and [get the tunnel token from the Console](/docs/en/agents-and-tools/mcp-tunnels/console#get-the-connection-details).

        <Note>
          Record the tunnel domain from the detail page. You'll set it as `gateway.config.tunnel_domain`.
        </Note>
      </Step>

      <Step title="Generate a CA and server certificate">
        The proxy listens on plain WebSocket, with [inner TLS](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) carried inside that stream using the certificate you generate here. The server certificate's SAN must include `*.<tunnel-domain>` per the [certificate requirements](/docs/en/agents-and-tools/mcp-tunnels/reference#certificate-requirements).

        ```bash
        export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
        mkdir -p mcp-tunnel/data
        cd mcp-tunnel

        # Self-signed CA. Explicit extensions so it satisfies the certificate
        # requirements regardless of distro openssl.cnf defaults.
        openssl req -x509 -newkey rsa:2048 -nodes \
          -keyout data/ca.key -out data/ca.crt \
          -days 3650 -subj "/CN=mcp-tunnel-ca" \
          -addext "basicConstraints=critical,CA:TRUE" \
          -addext "keyUsage=critical,keyCertSign,cRLSign" \
          -addext "subjectKeyIdentifier=hash"

        # Extension file for the server certificate. Using -extfile (instead of
        # -copy_extensions, which is OpenSSL 3.0+ only) keeps this working on
        # OpenSSL 1.1.x.
        cat > data/tls.ext <<EOF
        subjectAltName = DNS:${TUNNEL_DOMAIN},DNS:*.${TUNNEL_DOMAIN}
        authorityKeyIdentifier = keyid,issuer
        extendedKeyUsage = serverAuth
        EOF

        # Server certificate signed by the CA
        openssl req -newkey rsa:2048 -nodes \
          -keyout data/tls.key -out /tmp/server.csr \
          -subj "/CN=${TUNNEL_DOMAIN}"
        openssl x509 -req -in /tmp/server.csr \
          -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
          -out data/tls.crt -days 90 \
          -extfile data/tls.ext
        ```

        [Register `data/ca.crt` in the Console](/docs/en/agents-and-tools/mcp-tunnels/console#add-a-ca-certificate). Keep `data/ca.key` somewhere durable and secure; you'll need it to sign a fresh server certificate at renewal time.
      </Step>

      <Step title="Create the two Secrets">
        The chart reads specific keys; the Secret names are configurable but the keys are not. The following namespace-creation command is a no-op if the namespace already exists (for example, from the [sample MCP server](#optional-use-a-sample-mcp-server) step).

        ```bash
        kubectl create namespace mcp-tunnel --dry-run=client -o yaml | kubectl apply -f -
        kubectl -n mcp-tunnel create secret generic mcp-tunnel-token \
          --from-literal=tunnel-token='eyJ...'
        kubectl -n mcp-tunnel create secret generic mcp-tunnel-cert \
          --from-file=tls.crt=data/tls.crt \
          --from-file=tls.key=data/tls.key
        ```
      </Step>

      <Step title="Fetch the default values">
        ```bash
        helm show values \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 > values.yaml
        ```
      </Step>

      <Step title="Configure values for manual provisioning">
        Edit `values.yaml` and set the following keys:

        ```yaml values.yaml
        setup:
          enabled: false

        external:
          tunnelTokenSecretName: mcp-tunnel-token   # must contain key: tunnel-token
          serverCertSecretName: mcp-tunnel-cert     # must contain keys: tls.crt, tls.key

        gateway:
          config:
            # Required when setup.enabled is false. Replace the placeholder with
            # the $TUNNEL_DOMAIN value you exported earlier. When setup.enabled
            # is true the chart injects this from the Secret as a -tunnel-domain
            # flag instead.
            tunnel_domain: YOUR_TUNNEL_DOMAIN_HERE
            routes:
              docs: http://docs-mcp.internal:8080
              search: http://search-mcp.internal:8080
        ```

        Some managed Kubernetes distributions allocate the Service CIDR outside the standard private ranges; if your routes target in-cluster Services, add `gateway.config.upstream.allowed_ips` here per [Upstream IP validation](/docs/en/agents-and-tools/mcp-tunnels/troubleshooting#upstream-ip-validation).

        <Note>
          If you're using the [sample MCP server](#optional-use-a-sample-mcp-server), set `routes` to `echo: http://hello-mcp:9000` instead.
        </Note>
      </Step>

      <Step title="Review the rendered manifests">
        ```bash
        helm template mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          -n mcp-tunnel \
          -f values.yaml > rendered.yaml
        ```
      </Step>

      <Step title="Install">
        ```bash
        helm install mcp-tunnel \
          oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
          --version 2.0.1 \
          --namespace mcp-tunnel --create-namespace \
          -f values.yaml
        ```
      </Step>
    </Steps>
  </Tab>
</Tabs>

## Verify the deployment

Verify end to end from Anthropic's side: use `https://<route>.<your-tunnel-domain>/<path>` in a Managed Agent session or a Messages API request, where `<route>` is a key from `gateway.config.routes` and `<path>` is whatever the upstream MCP server serves at. With the [sample MCP server](#optional-use-a-sample-mcp-server), that's `https://echo.<your-tunnel-domain>/mcp`. See [Use the tunneled MCP servers](/docs/en/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers) for the request shapes.

If that fails, check the pod logs (`kubectl -n mcp-tunnel logs deploy/mcp-tunnel -c mcp-proxy` and `-c cloudflared`) and consult [Troubleshooting](/docs/en/agents-and-tools/mcp-tunnels/troubleshooting).

## Optional configuration

### Restrict egress with NetworkPolicy

Ingress to the proxy pod is denied by default (`networkPolicy.ingress.enabled: true`). To additionally restrict pod egress, set `networkPolicy.egress.enabled: true` and populate `networkPolicy.egress.mcpServers` with pod label selectors or CIDR ranges that cover your upstream MCP servers. Egress from cloudflared to the tunnel edge is allowed separately through `networkPolicy.egress.cloudflaredEgressCIDRs`.

### Tune the proxy

Fields under `gateway.config.*` pass through to the proxy configuration file. Common adjustments include `upstream.allowed_ips`, `log_level`, and `upstream.tls`. See the [proxy configuration](/docs/en/agents-and-tools/mcp-tunnels/reference#proxy-configuration) reference for the full field list. The chart always sets `listen_addr`, `tls.cert_file`, and `tls.key_file`; setting them in `gateway.config` has no effect.

### Supply your own OIDC token

By default the chart projects a Kubernetes ServiceAccount token for the setup component. To use a token from a different identity provider (such as [SPIFFE](/docs/en/manage-claude/wif-providers/spiffe), Vault, or a cloud-SDK sidecar), mount it with `setup.extraVolumes` and `setup.extraVolumeMounts`. Then point `api.wif.tokenFile` at the mount path. The chart sets `ANTHROPIC_IDENTITY_TOKEN_FILE` to that path, and the setup component reads the token from there.

## Upgrades

Always pass `--version` to `helm upgrade` so you don't pull a newer chart unexpectedly.

### Upgrade from chart 1.x

Chart 2.0.0 moves the tunnel ID from `api.wif.tunnelId` to `tunnel.id`. Before upgrading, edit your `values.yaml`: move the `tnl_...` value to `tunnel.id` and remove `api.wif.tunnelId`. Leaving `tunnel.id` unset is safe (the setup component reuses the tunnel ID already stored in the `mcp-tunnel` Secret on re-run), but the explicit move keeps your `values.yaml` accurate. Also update your federation rule's scope from `org:manage_tunnels` to `workspace:manage_tunnels` in the Console.

### Change configuration

For routine changes such as routes, replica count, or NetworkPolicy:

```bash
helm upgrade mcp-tunnel \
  oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
  --version 2.0.1 \
  -n mcp-tunnel \
  -f values.yaml
```

<Warning>
  Maintain a complete `values.yaml` rather than relying on `--reuse-values`. Helm's deep-merge behavior can silently fail to remove deleted routes.
</Warning>

### Rotate the tunnel token

With programmatic access, increment `tunnel.tokenVersion` in `values.yaml` and upgrade with `--set setup.force=true`. The setup component only re-runs on upgrades when forced:

```bash
helm upgrade mcp-tunnel \
  oci://us-docker.pkg.dev/anthropic-public-registry/charts/mcp-tunnel \
  --version 2.0.1 \
  -n mcp-tunnel \
  -f values.yaml \
  --set setup.force=true
```

The setup component authenticates with Workload Identity Federation; there is no API token to revoke.

Without programmatic access, click **Rotate token** on the tunnel detail page in the Console, then update the `mcp-tunnel-token` Secret:

```bash
kubectl -n mcp-tunnel create secret generic mcp-tunnel-token \
  --from-literal=tunnel-token='eyJ...' --dry-run=client -o yaml | kubectl apply -f -
kubectl -n mcp-tunnel rollout restart deploy/mcp-tunnel
```

<Warning>
  Clicking **Rotate token** invalidates the current token immediately. Until the Secret is updated and the rollout completes, any pod that restarts with the old token (eviction, node drain, OOM) cannot reconnect. Update the Secret promptly after rotating; for stricter availability requirements, use programmatic access so the chart handles the rotation atomically.
</Warning>

### Certificate renewal

The chart provides automation, but you remain responsible for monitoring expiry and confirming renewal completes.

With programmatic access, certificate renewal is automatic. The chart deploys a CronJob (named after the Helm `fullname`, suffixed `-cert-renew`) that runs `setup renew-cert` daily (at `serverCert.cronSchedule`, default `0 0 * * *` UTC). The job is a no-op unless the certificate is within `serverCert.renewBefore` of expiry (default 30 days). Renewal is local: the job signs a fresh certificate with the CA already stored in the Secret, makes no API calls, and only needs the Kubernetes RBAC the chart grants. The proxy hot-reloads the certificate from the Secret mount, so no Deployment restart is needed.

Without programmatic access there is no CronJob. From inside the `mcp-tunnel/` directory you kept after install, sign a fresh server certificate with the existing CA (do not regenerate the CA):

```bash
export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE
openssl req -new -key data/tls.key -out /tmp/server.csr \
  -subj "/CN=${TUNNEL_DOMAIN}"
openssl x509 -req -in /tmp/server.csr \
  -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
  -out data/tls.crt -days 90 -extfile data/tls.ext

kubectl -n mcp-tunnel create secret generic mcp-tunnel-cert \
  --from-file=tls.crt=data/tls.crt --from-file=tls.key=data/tls.key \
  --dry-run=client -o yaml | kubectl apply -f -
```

The proxy hot-reloads the certificate from the Secret mount.

## Next steps

<CardGroup cols={2}>
  <Card title="Use the tunneled MCP servers" icon="link" href="/docs/en/agents-and-tools/mcp-tunnels/overview#use-the-tunneled-mcp-servers">
    Attach an upstream MCP server to a Managed Agent or the Messages API.
  </Card>

  <Card title="Security" icon="lock" href="/docs/en/agents-and-tools/mcp-tunnels/security">
    Hardening guidance, credential rotation, and breach response.
  </Card>

  <Card title="Troubleshooting" icon="wrench" href="/docs/en/agents-and-tools/mcp-tunnels/troubleshooting">
    Diagnose connectivity, TLS, and routing issues.
  </Card>
</CardGroup>
