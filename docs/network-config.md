> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Enterprise network configuration

> Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.

Claude Code supports various enterprise network and security configurations through environment variables. This includes routing traffic through corporate proxy servers, trusting custom Certificate Authorities (CA), and authenticating with mutual Transport Layer Security (mTLS) certificates for enhanced security.

<Note>
  All environment variables shown on this page can also be configured in [`settings.json`](/en/settings).
</Note>

## Proxy configuration

### Environment variables

Claude Code respects standard proxy environment variables:

```bash theme={null}
# HTTPS proxy (recommended)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP proxy (if HTTPS not available)
export HTTP_PROXY=http://proxy.example.com:8080

# Bypass proxy for specific requests - space-separated format
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Bypass proxy for specific requests - comma-separated format
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Bypass proxy for all requests
export NO_PROXY="*"
```

<Note>
  Claude Code does not support SOCKS proxies.
</Note>

### Basic authentication

If your proxy requires basic authentication, include credentials in the proxy URL:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Avoid hardcoding passwords in scripts. Use environment variables or secure credential storage instead.
</Warning>

<Tip>
  For proxies requiring advanced authentication (NTLM, Kerberos, etc.), consider using an LLM Gateway service that supports your authentication method.
</Tip>

## CA certificate store

By default, Claude Code trusts both its bundled Mozilla CA certificates and your operating system's certificate store. Reading the OS store requires a runtime with `tls.getCACertificates`: the native installer always has it, and npm installs need Node 22.15 or later. On older Node versions, only the bundled set and `NODE_EXTRA_CA_CERTS` apply. Enterprise TLS-inspection proxies such as CrowdStrike Falcon and Zscaler work without additional configuration when their root certificate is installed in the OS trust store and the runtime can read it.

`CLAUDE_CODE_CERT_STORE` accepts a comma-separated list of sources. Recognized values are `bundled` for the Mozilla CA set shipped with Claude Code and `system` for the operating system trust store. The default is `bundled,system`.

To trust only the bundled Mozilla CA set:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

To trust only the OS certificate store:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` has no dedicated `settings.json` schema key. Set it via the `env` block in `~/.claude/settings.json` or directly in the process environment.
</Note>

## Custom CA certificates

If your enterprise environment uses a custom CA, configure Claude Code to trust it directly:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## mTLS authentication

For enterprise environments requiring client certificate authentication:

```bash theme={null}
# Client certificate for authentication
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Client private key
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optional: Passphrase for encrypted private key
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

Claude Code reads the certificate and key files at startup and re-reads them each time it applies settings, including when settings change during a session. To rotate the certificate and key, replace the files at the same paths.

## Apply network settings to background agents

[Background agents](/en/agent-view) don't run inside the terminal that dispatched them. A per-user supervisor process starts on demand, outlives your shell, and hosts every `claude agents`, `--bg`, and `/background` session. See [How background sessions are hosted](/en/agent-view#how-background-sessions-are-hosted). This changes how the configuration on this page reaches those sessions.

### Set network variables in settings, not the shell

The supervisor is one process shared by every terminal. It inherits the environment of whichever shell starts it first, and an OS-installed supervisor receives no shell environment at all. If you export a proxy, CA path, or mTLS variable only in your shell, it reaches background agents when that shell happened to cold-start the supervisor, and silently doesn't when a different shell did.

Put the same variables in the `env` block of `~/.claude/settings.json` or [managed settings](/en/settings) instead. Every variable on this page can be set there, and settings are the only configuration that reaches every background session on every machine.

### Configure a corporate launcher as a setting

Some organizations require every Claude Code process to start through a corporate launcher that applies sandboxing, network controls, or credential injection. The supervisor and its workers start Claude Code from a fixed path rather than by looking up `claude` on `PATH`, so every background agent bypasses a wrapper you place earlier on `PATH`.

Set the [`processWrapper`](/en/settings#available-settings) setting to prefix the supervisor, its workers, and the other background processes listed under [What the launcher covers](/en/corporate-launcher#what-the-launcher-covers) with your launcher. The equivalent [`CLAUDE_CODE_PROCESS_WRAPPER`](/en/env-vars) environment variable takes precedence when both are set, and it is subject to the same rule: deliver it through managed settings or `~/.claude/settings.json`, not a shell export. [Run Claude Code behind a corporate launcher](/en/corporate-launcher) covers the contract the launcher must satisfy, what it does and doesn't reach, and how to roll it out.

<Note>
  An already-running supervisor keeps the launch configuration it started with. After deploying the launcher setting, run [`claude daemon stop --any`](/en/agent-view#the-supervisor-process) so the next `claude agents` or `--bg` starts a supervisor that honors it. An installed service takes `claude daemon stop` without `--any`.
</Note>

## Network access requirements

Claude Code requires access to the following URLs. Allowlist these in your proxy configuration and firewall rules, especially in containerized or restricted network environments.

| URL                            | Required for                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`            | Claude API requests                                                                                                                                                                                                                                                                                                                                                                                         |
| `claude.ai`                    | claude.ai account authentication                                                                                                                                                                                                                                                                                                                                                                            |
| `platform.claude.com`          | Anthropic Console account authentication                                                                                                                                                                                                                                                                                                                                                                    |
| `mcp-proxy.anthropic.com`      | [MCP connectors from claude.ai](/en/mcp#use-mcp-servers-from-claude-ai), including connectors an organization administrator configures. Connector traffic routes through this proxy; connectors are enabled by default for claude.ai-authenticated users. To disable, set [`ENABLE_CLAUDEAI_MCP_SERVERS=false`](/en/env-vars) or the [`disableClaudeAiConnectors`](/en/settings#available-settings) setting |
| `downloads.claude.ai`          | Plugin executable downloads; native installer and native auto-updater                                                                                                                                                                                                                                                                                                                                       |
| `storage.googleapis.com`       | Install counts and plugin metadata shown in `/plugin`. Signed [artifact](/en/artifacts) uploads try this host first; publishing falls back to `api.anthropic.com` when it is blocked                                                                                                                                                                                                                        |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}Native installer and native auto-updater on versions prior to 2.1.116                                                                                                                                                                                                                                                                                                           |
| `bridge.claudeusercontent.com` | [Claude in Chrome](/en/chrome) extension WebSocket bridge                                                                                                                                                                                                                                                                                                                                                   |
| `*.claudeusercontent.com`      | Viewing [artifacts](/en/artifacts) on claude.ai. The viewer loads each artifact's content from a sandboxed subdomain of this origin. Required in the viewer's browser, not by the CLI itself                                                                                                                                                                                                                |
| `raw.githubusercontent.com`    | Changelog feed for [`/release-notes`](/en/commands) and the release notes shown after updating                                                                                                                                                                                                                                                                                                              |

If you install Claude Code through npm or manage your own binary distribution, end users do not need the native installer and auto-updater uses of `downloads.claude.ai`. The other uses in the table apply regardless of install method.

Claude Code also sends optional operational telemetry by default, which you can disable with environment variables. See [Telemetry services](/en/data-usage#telemetry-services) for how to disable it before finalizing your allowlist.

When using [Amazon Bedrock](/en/amazon-bedrock), [Google Cloud's Agent Platform](/en/google-vertex-ai), [Microsoft Foundry](/en/microsoft-foundry), or a signed-in [Claude apps gateway](/en/claude-apps-gateway) session, model traffic and authentication go to your provider or gateway instead of `api.anthropic.com`, `claude.ai`, or `platform.claude.com`. The WebFetch tool still calls `api.anthropic.com` for its [domain safety check](/en/data-usage#webfetch-domain-safety-check) unless you set `skipWebFetchPreflight: true` in [settings](/en/settings).

[Claude Code on the web](/en/claude-code-on-the-web) and [Code Review](/en/code-review) connect to your repositories from Anthropic-managed infrastructure. If your GitHub Enterprise Cloud organization restricts access by IP address, enable [IP allow list inheritance for installed GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). The Claude GitHub App registers its IP ranges, so enabling this setting allows access without manual configuration. To [add the ranges to your allow list manually](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) instead, or to configure other firewalls, see the [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

For self-hosted [GitHub Enterprise Server](/en/github-enterprise-server) instances behind a firewall, allowlist the same [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses) so Anthropic infrastructure can reach your GHES host to clone repositories and post review comments.

### Desktop and claude.ai

The preceding table primarily covers the standalone CLI. The Claude Desktop app and claude.ai in a browser load their application code from additional Anthropic CDN hosts, including `assets-proxy.anthropic.com`. Allowing `claude.ai` while blocking those hosts produces a blank page rather than an error. See [network access requirements](/en/desktop#network-access-requirements) on the Desktop page.

## Additional resources

* [Claude Code settings](/en/settings)
* [Environment variables reference](/en/env-vars)
* [Troubleshooting guide](/en/troubleshooting)
