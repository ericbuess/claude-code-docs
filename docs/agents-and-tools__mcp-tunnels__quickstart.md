# MCP tunnels quickstart

Connect Claude to a private MCP server using a local Docker Compose deployment.

---

<Note>
  MCP tunnels are in research preview. [Request access](https://claude.com/form/claude-managed-agents) to try them.
</Note>

This quickstart takes you from zero to Claude calling a private MCP server through a tunnel. It uses Docker Compose with [manual](/docs/en/agents-and-tools/mcp-tunnels/concepts#credential-provisioning) credential provisioning, which is the shortest path for local testing. For production deployments, see [Deploy with Helm](/docs/en/agents-and-tools/mcp-tunnels/deploy-helm) or [Deploy with Docker Compose](/docs/en/agents-and-tools/mcp-tunnels/deploy-compose).

## What you'll build

A two-container [tunnel stack](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) (the [proxy](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) and [cloudflared](/docs/en/agents-and-tools/mcp-tunnels/concepts#components)) plus a sample MCP server running alongside it. When everything is running, the sample server is reachable from Claude at `https://echo.<your-tunnel-domain>/mcp` even though nothing is listening on a public port.

## What you need

* [Docker and Docker Compose](https://docs.docker.com/get-docker/) on a machine with outbound internet access.
* A role in the [Claude Console](https://platform.claude.com) that can manage MCP tunnels. See the [Console guide prerequisites](/docs/en/agents-and-tools/mcp-tunnels/console#prerequisites).
* [OpenSSL](https://openssl-library.org/source/) 1.1.1 or later. Preinstalled on macOS and most Linux distributions; on Windows, install it separately (the `openssl` binary must be on your `PATH`).

<Steps>
  <Step title="Create a tunnel">
    In the Claude Console sidebar, go to **Manage > MCP tunnels** and click **New tunnel**. Give it a name. Leave **Set up programmatic access** off; this quickstart uses manual credential provisioning.

    After it's created, open the tunnel. Copy two values from the **Connection** section:

    * **Domain** (looks like `abcd1234.tunnel.anthropic.com`)
    * **Token** (click the eye icon, then copy)
  </Step>

  <Step title="Set up the deployment directory">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        mkdir -p mcp-tunnel/{config,data}
        cd mcp-tunnel
        export TUNNEL_DOMAIN=YOUR_TUNNEL_DOMAIN_HERE   # from step 1
        export TUNNEL_TOKEN='eyJ...'            # from step 1
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        New-Item -ItemType Directory -Force -Path mcp-tunnel/config, mcp-tunnel/data | Out-Null
        Set-Location mcp-tunnel
        $env:TUNNEL_DOMAIN = "YOUR_TUNNEL_DOMAIN_HERE"   # from step 1
        $env:TUNNEL_TOKEN  = "eyJ..."             # from step 1
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Generate a CA and server certificate">
    The proxy terminates [inner TLS](/docs/en/agents-and-tools/mcp-tunnels/concepts#components) using a certificate signed by a CA you control. Generate both:

    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        openssl req -x509 -newkey rsa:2048 -nodes \
          -keyout data/ca.key -out data/ca.crt \
          -days 3650 -subj "/CN=mcp-tunnel-ca" \
          -addext "basicConstraints=critical,CA:TRUE" \
          -addext "keyUsage=critical,keyCertSign,cRLSign" \
          -addext "subjectKeyIdentifier=hash"

        cat > data/tls.ext <<EOF
        subjectAltName = DNS:${TUNNEL_DOMAIN},DNS:*.${TUNNEL_DOMAIN}
        authorityKeyIdentifier = keyid,issuer
        extendedKeyUsage = serverAuth
        EOF

        openssl req -newkey rsa:2048 -nodes \
          -keyout data/tls.key -out /tmp/server.csr \
          -subj "/CN=${TUNNEL_DOMAIN}"
        openssl x509 -req -in /tmp/server.csr \
          -CA data/ca.crt -CAkey data/ca.key -CAcreateserial \
          -out data/tls.crt -days 90 -extfile data/tls.ext

        chmod 644 data/tls.key
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        openssl req -x509 -newkey rsa:2048 -nodes `
          -keyout data/ca.key -out data/ca.crt `
          -days 3650 -subj "/CN=mcp-tunnel-ca" `
          -addext "basicConstraints=critical,CA:TRUE" `
          -addext "keyUsage=critical,keyCertSign,cRLSign" `
          -addext "subjectKeyIdentifier=hash"

        @"
        subjectAltName = DNS:$env:TUNNEL_DOMAIN,DNS:*.$env:TUNNEL_DOMAIN
        authorityKeyIdentifier = keyid,issuer
        extendedKeyUsage = serverAuth
        "@ | Set-Content -NoNewline -Encoding ascii -Path data/tls.ext

        openssl req -newkey rsa:2048 -nodes `
          -keyout data/tls.key -out data/server.csr `
          -subj "/CN=$env:TUNNEL_DOMAIN"
        openssl x509 -req -in data/server.csr `
          -CA data/ca.crt -CAkey data/ca.key -CAcreateserial `
          -out data/tls.crt -days 90 -extfile data/tls.ext
        ```
      </Tab>
    </Tabs>

    Back in the Console, on the tunnel detail page, click **Add certificate** and upload `data/ca.crt` (or paste its contents). The tunnel status flips to **Active**.
  </Step>

  <Step title="Write the sample MCP server">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        cat > hello_server.py <<'EOF'
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("hello-server", host="0.0.0.0", port=9000)


        @mcp.tool()
        def hello(name: str = "world") -> str:
            """Say hello to someone."""
            return f"Hello, {name}!"


        if __name__ == "__main__":
            mcp.run(transport="streamable-http")
        EOF
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        @'
        from mcp.server.fastmcp import FastMCP

        mcp = FastMCP("hello-server", host="0.0.0.0", port=9000)


        @mcp.tool()
        def hello(name: str = "world") -> str:
            """Say hello to someone."""
            return f"Hello, {name}!"


        if __name__ == "__main__":
            mcp.run(transport="streamable-http")
        '@ | Set-Content -NoNewline -Encoding ascii -Path hello_server.py
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Write the proxy config and compose file">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        cat > config/mcp-proxy.yaml <<EOF
        listen_addr: ":8080"
        tunnel_domain: ${TUNNEL_DOMAIN}
        tls:
          cert_file: /data/tls.crt
          key_file: /data/tls.key
        routes:
          echo: http://hello-mcp:9000
        EOF

        cat > docker-compose.yaml <<'EOF'
        services:
          mcp-proxy:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:9d4c80593b559fc3ca3814866418744fa94858b02a4d4a4cc52d423e732ccc81
            volumes:
              - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
              - ./data:/data:ro
            restart: unless-stopped

          cloudflared:
            image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            network_mode: "service:mcp-proxy"
            restart: unless-stopped

          hello-mcp:
            image: python:3.13-slim
            working_dir: /app
            volumes:
              - ./hello_server.py:/app/hello_server.py:ro
            command: sh -c "pip install --quiet mcp && python hello_server.py"
            restart: unless-stopped
        EOF
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        @"
        listen_addr: ":8080"
        tunnel_domain: $env:TUNNEL_DOMAIN
        tls:
          cert_file: /data/tls.crt
          key_file: /data/tls.key
        routes:
          echo: http://hello-mcp:9000
        "@ | Set-Content -NoNewline -Encoding ascii -Path config/mcp-proxy.yaml

        @'
        services:
          mcp-proxy:
            image: us-docker.pkg.dev/anthropic-public-registry/images/mcp-proxy@sha256:9d4c80593b559fc3ca3814866418744fa94858b02a4d4a4cc52d423e732ccc81
            volumes:
              - ./config/mcp-proxy.yaml:/etc/mcp-gateway/config.yaml:ro
              - ./data:/data:ro
            restart: unless-stopped

          cloudflared:
            image: cloudflare/cloudflared@sha256:6b599ca3e974349ead3286d178da61d291961182ec3fe9c505e1dd02c8ac31b0
            command: tunnel --no-autoupdate run --url http://localhost:8080
            environment:
              - TUNNEL_TOKEN
            network_mode: "service:mcp-proxy"
            restart: unless-stopped

          hello-mcp:
            image: python:3.13-slim
            working_dir: /app
            volumes:
              - ./hello_server.py:/app/hello_server.py:ro
            command: sh -c "pip install --quiet mcp && python hello_server.py"
            restart: unless-stopped
        '@ | Set-Content -NoNewline -Encoding ascii -Path docker-compose.yaml
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Start it">
    <Tabs>
      <Tab title="macOS / Linux">
        ```bash
        docker compose up -d
        docker compose logs mcp-proxy | grep "route configured"
        docker compose logs cloudflared | grep "Registered tunnel connection"
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        ```powershell
        docker compose up -d
        docker compose logs mcp-proxy | Select-String "route configured"
        docker compose logs cloudflared | Select-String "Registered tunnel connection"
        ```
      </Tab>
    </Tabs>

    You should see one `route configured` line for `echo` and four `Registered tunnel connection` lines. The containers take a few seconds to start; rerun the log commands if they come back empty.
  </Step>

  <Step title="Call it from Claude">
    In the Console, go to **Managed Agents > Sessions** and create a session. In the agent picker choose **Create new agent**, give the agent a name, and keep the pre-filled model. Click **+ MCP Server**, select your tunnel, set **Subdomain** to `echo` and **Path** to `mcp`. Then ask:

    > Use the hello tool to greet tunnel.

    You should see a tool call followed by its result.
  </Step>
</Steps>

## Next steps

The tunnel is verified end to end. To swap in your own MCP server, add it to `docker-compose.yaml` (or run it on the same Docker network), add a route for it in `config/mcp-proxy.yaml`, then restart the proxy (`docker compose restart mcp-proxy`).

For production deployments:

<CardGroup cols={2}>
  <Card title="Deploy with Docker Compose" icon="cube" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-compose">
    Hardened single-host deployment, with or without programmatic access.
  </Card>

  <Card title="Deploy with Helm" icon="stack" href="/docs/en/agents-and-tools/mcp-tunnels/deploy-helm">
    Kubernetes deployment with automatic credential management.
  </Card>
</CardGroup>
