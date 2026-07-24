> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Enterprise network configuration

> Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.

Claude Code supports various enterprise network and security configurations through environment variables. This includes routing traffic through corporate proxy servers, trusting custom Certificate Authorities (CA), and authenticating with mutual Transport Layer Security (mTLS) certificates for enhanced security.

<Note>
  All environment variables shown on this page can also be configured in [`settings.json`](/docs/en/settings).
</Note>

## Proxy configuration

### Environment variables

Claude Code respects standard proxy environment variables. {/* min-version: 2.1.217 */}In Claude Desktop sessions where the app manages the provider connection, Claude Code reads them only from managed settings and `~/.claude/settings.json`; see [mTLS authentication](#mtls-authentication) for the scope rules.

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

In [cloud sessions](/docs/en/claude-code-on-the-web), the hosting environment manages the connection to the API, so Claude Code ignores the following variables when they come from a settings file `env` block:

* `CLAUDE_CODE_CLIENT_CERT`
* `CLAUDE_CODE_CLIENT_KEY`
* `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`
* `NODE_EXTRA_CA_CERTS`
* `NODE_TLS_REJECT_UNAUTHORIZED`
* `CLAUDE_CODE_OAUTH_SCOPES`

Claude Code notes each ignored key in the session's debug log.

In [Claude Desktop](/docs/en/desktop) sessions where the app manages the provider connection, such as the Code tab on a [third-party provider](/docs/en/third-party-integrations) and Cowork sessions, Claude Code reads these variables and the proxy variables `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` only from [managed settings](/docs/en/settings#settings-files) and `~/.claude/settings.json`: it ignores them in a repository's own settings files, so a checked-out repository can't redirect the TLS or proxy path of a session whose credentials come from the app. In a local, SSH, or WSL Code tab session signed in through claude.ai, the app doesn't manage the connection, and Claude Code reads these variables from every settings scope, like any terminal session; [cloud sessions](/docs/en/claude-code-on-the-web) follow the cloud-session rules above wherever you start them. Before v2.1.217, Claude Code ignored these variables in every settings file when the app managed the connection.

## Apply network settings to background agents

[Background agents](/docs/en/agent-view) don't run inside the terminal that dispatched them. A per-user supervisor process starts on demand, outlives your shell, and hosts every `claude agents`, `--bg`, and `/background` session. See [How background sessions are hosted](/docs/en/agent-view#how-background-sessions-are-hosted). This changes how the configuration on this page reaches those sessions.

### Set network variables in settings, not the shell

The supervisor is one process shared by every terminal. It inherits the environment of whichever shell starts it first, and an OS-installed supervisor receives no shell environment at all. If you export a proxy, CA path, or mTLS variable only in your shell, it reaches background agents when that shell happened to cold-start the supervisor, and silently doesn't when a different shell did.

Put the same variables in the `env` block of `~/.claude/settings.json` or [managed settings](/docs/en/settings) instead. Every variable on this page can be set there, and settings are the only configuration that reaches every background session on every machine.

### Configure a corporate launcher as a setting

Some organizations require every Claude Code process to start through a corporate launcher that applies sandboxing, network controls, or credential injection. The supervisor and its workers start Claude Code from a fixed path rather than by looking up `claude` on `PATH`, so every background agent bypasses a wrapper you place earlier on `PATH`.

Set the [`processWrapper`](/docs/en/settings#available-settings) setting to prefix the supervisor, its workers, and the other background processes listed under [What the launcher covers](/docs/en/corporate-launcher#what-the-launcher-covers) with your launcher. The equivalent [`CLAUDE_CODE_PROCESS_WRAPPER`](/docs/en/env-vars) environment variable takes precedence when both are set, and it is subject to the same rule: deliver it through managed settings or `~/.claude/settings.json`, not a shell export. [Run Claude Code behind a corporate launcher](/docs/en/corporate-launcher) covers the contract the launcher must satisfy, what it does and doesn't reach, and how to roll it out.

<Note>
  An already-running supervisor keeps the launch configuration it started with. After deploying the launcher setting, run [`claude daemon stop --any`](/docs/en/agent-view#the-supervisor-process) so the next `claude agents` or `--bg` starts a supervisor that honors it. An installed service takes `claude daemon stop` without `--any`.
</Note>

## Network access requirements

Claude Code requires access to the following URLs. Allowlist these in your proxy configuration and firewall rules, especially in containerized or restricted network environments.

| URL                                  | Required for                                                                                                                                                                                                                                                                                                                                                                                                |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`                  | Claude API requests, including the WebFetch [domain safety check](/docs/en/data-usage#webfetch-domain-safety-check), feature flag fetches, and telemetry event logging                                                                                                                                                                                                                                           |
| `claude.ai`                          | claude.ai account authentication                                                                                                                                                                                                                                                                                                                                                                            |
| `claude.com`                         | claude.ai account sign-in opens a `claude.com` page in the browser, which redirects to `claude.ai`; pre-approved WebFetch documentation lookups also reach this host from the CLI                                                                                                                                                                                                                           |
| `platform.claude.com`                | Anthropic Console account authentication. OAuth token exchange, refresh, and revocation also go to this host for claude.ai accounts, so both Console and claude.ai sign-ins require it                                                                                                                                                                                                                      |
| `mcp-proxy.anthropic.com`            | [MCP connectors from claude.ai](/docs/en/mcp#use-mcp-servers-from-claude-ai), including connectors an organization administrator configures. Connector traffic routes through this proxy; connectors are enabled by default for claude.ai-authenticated users. To disable, set [`ENABLE_CLAUDEAI_MCP_SERVERS=false`](/docs/en/env-vars) or the [`disableClaudeAiConnectors`](/docs/en/settings#available-settings) setting |
| `downloads.claude.ai`                | Plugin executable downloads; native installer, native auto-updater, and update version checks                                                                                                                                                                                                                                                                                                               |
| `storage.googleapis.com`             | Install counts and plugin metadata shown in `/plugin`. Signed [artifact](/docs/en/artifacts) uploads try this host first; publishing falls back to `api.anthropic.com` when it is blocked                                                                                                                                                                                                                        |
| `storage.googleapis.com`             | {/* max-version: 2.1.115 */}Native installer and native auto-updater on versions prior to 2.1.116                                                                                                                                                                                                                                                                                                           |
| `bridge.claudeusercontent.com`       | [Claude in Chrome](/docs/en/chrome) extension WebSocket bridge                                                                                                                                                                                                                                                                                                                                                   |
| `raw.githubusercontent.com`          | Changelog feed for [`/release-notes`](/docs/en/commands) and the release notes shown after updating                                                                                                                                                                                                                                                                                                              |
| `http-intake.logs.us5.datadoghq.com` | Operational telemetry events, sent only when the CLI uses the Anthropic API directly, never for Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. Optional: disable with [`DISABLE_TELEMETRY`](/docs/en/data-usage#telemetry-services) or `DO_NOT_TRACK`                                                                                                                                      |
| `browser-intake-us5-datadoghq.com`   | Operational error reports, sent when the CLI uses the Anthropic API directly and a server-side rollout gate enables them. Optional: disable with `DISABLE_ERROR_REPORTING` or `DISABLE_TELEMETRY`; see [Telemetry services](/docs/en/data-usage#telemetry-services)                                                                                                                                              |
| `formulae.brew.sh`                   | Update version checks on Homebrew installs. Other install methods don't contact this host                                                                                                                                                                                                                                                                                                                   |
| `code.claude.com`                    | Claude Code documentation lookups by the built-in claude-code-guide agent and pre-approved WebFetch requests. Blocking this host only affects documentation lookups                                                                                                                                                                                                                                         |

If you install Claude Code through npm or manage your own binary distribution, end users don't need the native installer and auto-updater uses of `downloads.claude.ai`, but npm and bun installs need their package registry, `registry.npmjs.org`, unless your organization mirrors it. The other uses in the table apply regardless of install method.

The two Datadog intake hosts carry only optional operational telemetry, and setting [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/en/env-vars) disables both. Sessions on third-party providers never send to these hosts, even when a platform sets [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/en/env-vars) and telemetry metrics default on. See [Telemetry services](/docs/en/data-usage#telemetry-services) for everything Claude Code sends and how to disable it before finalizing your allowlist.

When using [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), [Microsoft Foundry](/docs/en/microsoft-foundry), or a signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) session, model traffic and authentication go to your provider or gateway instead of `api.anthropic.com`, `claude.ai`, or `platform.claude.com`. The WebFetch tool still calls `api.anthropic.com` for its [domain safety check](/docs/en/data-usage#webfetch-domain-safety-check) unless you set `skipWebFetchPreflight: true` in [settings](/docs/en/settings).

When routing through an [LLM gateway](/docs/en/llm-gateway) with [`ANTHROPIC_BASE_URL`](/docs/en/llm-gateway-connect#set-the-base-url-and-credential), the [fast mode](/docs/en/fast-mode) availability check still calls `api.anthropic.com` rather than the gateway base URL. The check does honor a configured HTTP proxy, so where a network block is the cause, an allowlist entry for `api.anthropic.com` in the proxy is the fix. A network block fails the check only where the host is unreachable even through the proxy, and fast mode then reports a connectivity error. The same connectivity error appears when the check presents a gateway-issued credential that Anthropic rejects; allowlisting doesn't help there, since nothing is blocked. See [use fast mode behind proxies and LLM gateways](/docs/en/fast-mode#use-fast-mode-behind-proxies-and-llm-gateways) for the variables that restore it.

[Claude Code on the web](/docs/en/claude-code-on-the-web) and [Code Review](/docs/en/code-review) connect to your repositories from Anthropic-managed infrastructure. If your GitHub Enterprise Cloud organization restricts access by IP address, enable [IP allow list inheritance for installed GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). The Claude GitHub App registers its IP ranges, so enabling this setting allows access without manual configuration. To [add the ranges to your allow list manually](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) instead, or to configure other firewalls, see the [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

For self-hosted [GitHub Enterprise Server](/docs/en/github-enterprise-server) instances behind a firewall, allowlist the same [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses) so Anthropic infrastructure can reach your GHES host to clone repositories and post review comments.

### Desktop and claude.ai

The preceding table covers the standalone CLI. The Claude Desktop app and claude.ai in a browser load their application code and user content from additional Anthropic CDN hosts, including `assets-proxy.anthropic.com` and the `*.claudeusercontent.com` origins that serve [artifacts](/docs/en/artifacts). Allowing `claude.ai` while blocking those hosts produces a blank page rather than an error. See [network access requirements](/docs/en/desktop#network-access-requirements) on the Desktop page.

## Additional resources

* [Claude Code settings](/docs/en/settings)
* [Environment variables reference](/docs/en/env-vars)
* [Troubleshooting guide](/docs/en/troubleshooting)
