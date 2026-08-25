> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Enterprise network configuration

> Configure Claude Code for enterprise environments with proxy servers, custom Certificate Authorities (CA), and mutual Transport Layer Security (mTLS) authentication.

Claude Code supports various enterprise network and security configurations through environment variables. This includes routing traffic through corporate proxy servers, trusting custom Certificate Authorities (CA), and authenticating with mutual Transport Layer Security (mTLS) certificates for enhanced security.

Set these environment variables before you launch Claude Code. Variables exported in your shell are read once at startup, so a running session doesn't pick up later changes to your shell environment.

<Note>
  All environment variables shown on this page can also be configured in [`settings.json`](/docs/en/settings).
</Note>

## Proxy configuration

### Environment variables

Claude Code respects standard proxy environment variables. In Claude Desktop sessions where the app manages the provider connection, Claude Code reads them only from managed settings and `~/.claude/settings.json`; see [mTLS authentication](#mtls-authentication) for the scope rules.

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

Lowercase variants also work, and Claude Code uses the first one that's set in the order `https_proxy`, `HTTPS_PROXY`, `http_proxy`, `HTTP_PROXY`.

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

Claude Code reads the certificate and key files at startup and re-reads them each time it applies settings, such as when your organization changes the `env` block in [managed settings](/docs/en/server-managed-settings) mid-session.

To rotate the certificate and key, replace the files at the same paths. Claude Code picks up the replacement in a running session without a restart. When an API request fails with a connection-level error, such as a connection reset or a TLS handshake error, it re-reads both files and retries the request with the new pair. Before v2.1.232, Claude Code didn't re-read on connection errors, so it kept the pair it had already loaded until it next applied settings or you restarted.

Claude Code re-reads the files in response to failed requests, not by watching them for changes:

* **Timing**: Claude Code does nothing at the moment you replace the files. It presents the new pair on the retry after a qualifying failure, or on the next request after it applies settings, whichever comes first.
* **Gateway rejections**: Claude Code re-reads when your gateway resets the connection or rejects the TLS handshake after it stops accepting the old pair. It doesn't re-read when the gateway completes the handshake and answers with an HTTP error. In that case, Claude Code loads the new pair when it next applies settings or when you restart it.
* **Half-written rotations**: when Claude Code re-reads while your rotation is mid-write, such as reading a certificate and key that don't match each other, it keeps the previous pair and re-reads on the next failure.
* **OTLP telemetry exporters**: Claude Code keeps the certificate the [exporters](/docs/en/monitoring-usage#mtls-authentication) loaded at first use, so restart Claude Code for a rotated certificate to reach your telemetry collector.
* **Turn the reload off**: set [`CLAUDE_CODE_DISABLE_MTLS_RELOAD_ON_STALE_CONNECTION=1`](/docs/en/env-vars#variables) to turn off the connection-error re-read. Claude Code then picks up rotated files only when it next applies settings or at the next startup.

To confirm Claude Code picked up a rotation, [start the session with debug logging](#verify-your-configuration) and look for `Stale connection — reloaded rotated mTLS client material` in the log. Claude Code doesn't log this line when it picks up the rotation while applying settings instead, so a missing line alone doesn't mean the rotation failed.

Replace the files before the current pair expires so Claude Code doesn't load an already-expired pair at the next startup.

In [cloud sessions](/docs/en/claude-code-on-the-web), the hosting environment manages the connection to the API, so Claude Code ignores the following variables when they come from a settings file `env` block:

* `CLAUDE_CODE_CLIENT_CERT`
* `CLAUDE_CODE_CLIENT_KEY`
* `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`
* `NODE_EXTRA_CA_CERTS`
* `NODE_TLS_REJECT_UNAUTHORIZED`
* `CLAUDE_CODE_OAUTH_SCOPES`

Claude Code notes each ignored key in the session's debug log.

In [Claude Desktop](/docs/en/desktop) sessions where the app manages the provider connection, such as the Code tab on a [third-party provider](/docs/en/third-party-integrations) and Cowork sessions, Claude Code reads these variables and the proxy variables `HTTP_PROXY`, `HTTPS_PROXY`, and `NO_PROXY` only from [managed settings](/docs/en/managed-settings) and `~/.claude/settings.json`: it ignores them in a repository's own settings files, so a checked-out repository can't redirect the TLS or proxy path of a session whose credentials come from the app. In a local, SSH, or WSL Code tab session signed in through claude.ai, the app doesn't manage the connection, and Claude Code reads these variables from every settings scope, like any terminal session; [cloud sessions](/docs/en/claude-code-on-the-web) follow the cloud-session rules above wherever you start them. Before v2.1.217, Claude Code ignored these variables in every settings file when the app managed the connection.

## Verify your configuration

You usually find out about a wrong proxy address or a bad certificate path from a [connection or certificate error](/docs/en/errors#network-and-connection-errors) on a later request, since Claude Code doesn't validate most of these settings when it reads them. The one setting it checks at startup is the proxy URL: when it can't parse the value, such as one missing the `http://` scheme, Claude Code stops launch with an error naming the variable to fix.

To confirm your configuration loaded before you send a request, start Claude Code with debug logging:

```bash theme={null}
claude --debug
```

Debug output goes to `~/.claude/debug/<session-id>.txt` rather than the terminal, or to a path you set with `--debug-file <path>`. In the log, look for the lines that confirm each file loaded:

```text theme={null}
CA certs: Appended extra certificates from NODE_EXTRA_CA_CERTS (/etc/ssl/certs/corp-ca.pem)
mTLS: Loaded client certificate from CLAUDE_CODE_CLIENT_CERT
mTLS: Loaded client key from CLAUDE_CODE_CLIENT_KEY
```

If Claude Code can't read one of these files, the log shows a `Failed to read` or `Failed to load` line with the reason instead.

You can also run `/status` in an interactive session and check these rows:

* **Proxy**: shows the active proxy URL, and marks a value it can't parse as invalid and ignored.
* **mTLS client cert** and **mTLS client key**: appear only when the files loaded, so a missing row means the load failed and the debug log has the reason.
* **Additional CA cert(s)**: shows the `NODE_EXTRA_CA_CERTS` path without checking that the file loaded, so confirm this one in the debug log.

## Apply network settings to background agents

[Background agents](/docs/en/agent-view) don't run inside the terminal that dispatched them. A per-user supervisor process starts on demand, outlives your shell, and hosts every `claude agents`, `--bg`, and `/background` session. See [How background sessions are hosted](/docs/en/agent-view#how-background-sessions-are-hosted). This changes how the configuration on this page reaches those sessions.

### Set network variables in settings, not the shell

The supervisor is one process shared by every terminal. It inherits the environment of whichever shell starts it first, and an OS-installed supervisor receives no shell environment at all. If you export a proxy, CA path, or mTLS variable only in your shell, it reaches background agents when that shell happened to cold-start the supervisor, and silently doesn't when a different shell did.

Put the same variables in the `env` block of `~/.claude/settings.json` or [managed settings](/docs/en/settings) instead. Every variable on this page can be set there, and settings are the only configuration that reaches every background session on every machine.

### Configure a corporate launcher as a setting

Some organizations require every Claude Code process to start through a corporate launcher that applies sandboxing, network controls, or credential injection. The supervisor and its workers start Claude Code from a fixed path rather than by looking up `claude` on `PATH`, so every background agent bypasses a wrapper you place earlier on `PATH`.

Set the [`processWrapper`](/docs/en/settings-reference#processwrapper) setting to prefix the supervisor, its workers, and the other background processes listed under [What the launcher covers](/docs/en/corporate-launcher#what-the-launcher-covers) with your launcher. The equivalent [`CLAUDE_CODE_PROCESS_WRAPPER`](/docs/en/env-vars) environment variable takes precedence when both are set, and it is subject to the same rule: deliver it through managed settings or `~/.claude/settings.json`, not a shell export. [Run Claude Code behind a corporate launcher](/docs/en/corporate-launcher) covers the contract the launcher must satisfy, what it does and doesn't reach, and how to roll it out.

<Note>
  An already-running supervisor keeps the launch configuration it started with. After deploying the launcher setting, run [`claude daemon stop --any`](/docs/en/agent-view#the-supervisor-process) so the next `claude agents` or `--bg` starts a supervisor that honors it. An installed service takes `claude daemon stop` without `--any`.
</Note>

## Streaming idle watchdogs

Claude Code runs three independent timers that abort a streaming model response when it goes quiet, so a dead connection fails and retries instead of hanging. Each timer watches a different signal:

| Timer                | Aborts when                                                                                                                                                                                            | Runs on                                                                                                                                                                                                                                                                                                                                   | Default timeout                                                |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| Event-level watchdog | No response events parse. On connections where the byte-level watchdog runs, arriving bytes, including keep-alive pings, also reset this watchdog, for up to about five minutes without a parsed event | Every provider                                                                                                                                                                                                                                                                                                                            | 300 seconds                                                    |
| Byte-level watchdog  | No bytes arrive on the wire, including SSE keep-alive pings                                                                                                                                            | Direct Anthropic API, [Claude Platform on AWS](/docs/en/claude-platform-on-aws), and [gateway](/docs/en/gateways) connections, including a custom `ANTHROPIC_BASE_URL`. Opt-in on Amazon Bedrock `vnd.amazon.eventstream` responses with `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK=1`; doesn't run on Google Cloud's Agent Platform or Microsoft Foundry | 180 seconds on the direct Anthropic API, 300 seconds elsewhere |
| Body idle timeout    | No bytes arrive for 5 minutes                                                                                                                                                                          | Providers other than the direct Anthropic API and Claude Platform on AWS, unless [`API_FORCE_IDLE_TIMEOUT`](/docs/en/env-vars) changes that                                                                                                                                                                                                    | 5 minutes                                                      |

Configure the timers with these variables, each detailed in the [environment variables reference](/docs/en/env-vars):

* `CLAUDE_ENABLE_STREAM_WATCHDOG` and `CLAUDE_ENABLE_BYTE_WATCHDOG` force the corresponding watchdog on with `1` or off with `0`, within the connections the table lists; neither variable extends a watchdog to a connection type it doesn't cover.
* `CLAUDE_STREAM_IDLE_TIMEOUT_MS` sets both watchdogs' timeout. Claude Code raises values below 5 minutes to 5 minutes, and caps the value at 30 minutes for the byte-level watchdog.
* `CLAUDE_BYTE_STREAM_IDLE_TIMEOUT_MS` sets the byte-level watchdog's timeout alone, clamped to between 10 seconds and 30 minutes, and takes precedence over `CLAUDE_STREAM_IDLE_TIMEOUT_MS` for that watchdog.
* `API_FORCE_IDLE_TIMEOUT` set to `0` turns the body idle timeout off, and set to `1` turns it on for every provider. The watchdogs run independently of it, so to let a stream pause longer than their thresholds, also raise or disable them.

When a timer aborts a stalled stream, Claude Code handles it like any other mid-stream failure: it retries, keeps completed output with an [incomplete-response notice](/docs/en/errors#the-response-above-may-be-incomplete), or ends the turn, depending on where the response stood.

## Network access requirements

Claude Code requires access to the following URLs. Allowlist these in your proxy configuration and firewall rules, especially in containerized or restricted network environments. The first-run setup connectivity check points here when it can't reach `api.anthropic.com` or `platform.claude.com`; see [Unable to connect to Anthropic services](/docs/en/errors#unable-to-connect-to-anthropic-services) for the check's messages and recovery steps.

| URL                                  | Required for                                                                                                                                                                                                                                                                                                                                                                                                                 |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`                  | Claude API requests, including the WebFetch [domain safety check](/docs/en/data-usage#webfetch-domain-safety-check), feature flag fetches, and telemetry event logging                                                                                                                                                                                                                                                            |
| `claude.ai`                          | claude.ai account authentication                                                                                                                                                                                                                                                                                                                                                                                             |
| `claude.com`                         | claude.ai account sign-in opens a `claude.com` page in the browser, which redirects to `claude.ai`; pre-approved WebFetch documentation lookups also reach this host from the CLI                                                                                                                                                                                                                                            |
| `platform.claude.com`                | Anthropic Console account authentication. OAuth token exchange, refresh, and revocation also go to this host for claude.ai accounts, so both Console and claude.ai sign-ins require it                                                                                                                                                                                                                                       |
| `mcp-proxy.anthropic.com`            | [MCP connectors from claude.ai](/docs/en/mcp#use-mcp-servers-from-claude-ai), including connectors an organization administrator configures. Connector traffic routes through this proxy; connectors are enabled by default for claude.ai-authenticated users. To disable, set [`ENABLE_CLAUDEAI_MCP_SERVERS=false`](/docs/en/env-vars) or the [`disableClaudeAiConnectors`](/docs/en/settings-reference#disableclaudeaiconnectors) setting |
| `downloads.claude.ai`                | Plugin executable downloads; native installer, native auto-updater, and update version checks                                                                                                                                                                                                                                                                                                                                |
| `storage.googleapis.com`             | Plugin install counts and metadata shown in `/plugin`                                                                                                                                                                                                                                                                                                                                                                        |
| `storage.googleapis.com`             | Native installer and native auto-updater on versions prior to 2.1.116                                                                                                                                                                                                                                                                                                                                                        |
| `registry.npmjs.org`                 | Plugin installs (fetching npm-source plugin packages and installing plugins' Node.js package dependencies), `npx`-launched MCP servers, and the package registry for npm and bun installs of Claude Code itself                                                                                                                                                                                                              |
| `bridge.claudeusercontent.com`       | [Claude in Chrome](/docs/en/chrome) extension WebSocket bridge                                                                                                                                                                                                                                                                                                                                                                    |
| `*.frame.claudeusercontent.com`      | [Artifact](/docs/en/artifacts) content reads. The CLI fetches an artifact's files from this host when Claude opens one, and only when the Artifact tool is [available](/docs/en/artifacts#availability) for your account. To disable the tool and drop this requirement, set [`CLAUDE_CODE_DISABLE_ARTIFACT=1`](/docs/en/env-vars) or the [`disableArtifact`](/docs/en/settings-reference#disableartifact) setting                               |
| `raw.githubusercontent.com`          | Changelog feed for [`/release-notes`](/docs/en/commands) and the release notes shown after updating                                                                                                                                                                                                                                                                                                                               |
| `http-intake.logs.us5.datadoghq.com` | Operational telemetry events, sent only when the CLI uses the Anthropic API directly, never for Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. Optional: disable with [`DISABLE_TELEMETRY`](/docs/en/data-usage#telemetry-services) or `DO_NOT_TRACK`                                                                                                                                                       |
| `browser-intake-us5-datadoghq.com`   | Operational error reports, sent when the CLI uses the Anthropic API directly and a server-side rollout gate enables them. Optional: disable with `DISABLE_ERROR_REPORTING` or `DISABLE_TELEMETRY`; see [Telemetry services](/docs/en/data-usage#telemetry-services)                                                                                                                                                               |
| `formulae.brew.sh`                   | Update version checks on Homebrew installs. Other install methods don't contact this host                                                                                                                                                                                                                                                                                                                                    |
| `code.claude.com`                    | Claude Code documentation lookups by the built-in claude-code-guide agent and pre-approved WebFetch requests. Blocking this host only affects documentation lookups                                                                                                                                                                                                                                                          |

If you install Claude Code through npm or manage your own binary distribution, end users don't need the native installer and auto-updater uses of `downloads.claude.ai`, but npm and bun installs need their package registry, `registry.npmjs.org`, unless your organization mirrors it. The other uses in the table apply regardless of install method.

The two Datadog intake hosts carry only optional operational telemetry, and setting [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/en/env-vars) disables both. Sessions on third-party providers never send to these hosts, even when a platform sets [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/en/env-vars) and telemetry metrics default on. See [Telemetry services](/docs/en/data-usage#telemetry-services) for everything Claude Code sends and how to disable it before finalizing your allowlist.

When using [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), [Microsoft Foundry](/docs/en/microsoft-foundry), or a signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) session, model traffic and authentication go to your provider or gateway instead of `api.anthropic.com`, `claude.ai`, or `platform.claude.com`. The WebFetch tool still calls `api.anthropic.com` for its [domain safety check](/docs/en/data-usage#webfetch-domain-safety-check) unless you set `skipWebFetchPreflight: true` in [settings](/docs/en/settings).

When routing through an [LLM gateway](/docs/en/llm-gateway) with [`ANTHROPIC_BASE_URL`](/docs/en/llm-gateway-connect#set-the-base-url-and-credential), the [fast mode](/docs/en/fast-mode) availability check still calls `api.anthropic.com` rather than the gateway base URL. The check does honor a configured HTTP proxy, so where a network block is the cause, an allowlist entry for `api.anthropic.com` in the proxy is the fix. A network block fails the check only where the host is unreachable even through the proxy, and fast mode then reports a connectivity error. The same connectivity error appears when the check presents a gateway-issued credential that Anthropic rejects; allowlisting doesn't help there, since nothing is blocked. See [use fast mode behind proxies and LLM gateways](/docs/en/fast-mode#use-fast-mode-behind-proxies-and-llm-gateways) for the variables that restore it.

### GitHub allow lists and firewalls

[Claude Code on the web](/docs/en/claude-code-on-the-web) in Anthropic-hosted environments and [Code Review](/docs/en/code-review) connect to your repositories from Anthropic-managed infrastructure; sessions in a [self-hosted environment](/docs/en/self-hosted-environments) connect from inside your network, unless the runner opts into the [Anthropic git proxy](/docs/en/self-hosted-environments-deploy#use-the-anthropic-git-proxy), which fetches from Anthropic's side.

If your GitHub Enterprise Cloud organization restricts access by IP address, enable [IP allow list inheritance for installed GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps) and also [add an allow list entry](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) for Anthropic's [outbound IP addresses](https://platform.claude.com/docs/en/api/ip-addresses#outbound-ip-addresses). Inheritance covers only the requests the Claude GitHub App makes as an installation, not the requests it makes on your users' behalf. For other firewalls, see the [Anthropic API IP addresses](https://platform.claude.com/docs/en/api/ip-addresses).

For self-hosted [GitHub Enterprise Server](/docs/en/github-enterprise-server) instances behind a firewall, allowlist Anthropic's [outbound IP addresses](https://platform.claude.com/docs/en/api/ip-addresses#outbound-ip-addresses) so Anthropic infrastructure can reach your GHES host to clone repositories and post review comments. Sessions in a [self-hosted environment](/docs/en/self-hosted-environments-deploy#configure-git) reach your GHES host from inside your network instead, so that exposure applies only to Anthropic-hosted sessions, to hosted pre-session flows such as the repository picker, and to self-hosted runners that opt into the [Anthropic git proxy](/docs/en/self-hosted-environments-deploy#use-the-anthropic-git-proxy), which fetches from Anthropic's side. For a GHES host that's only routable inside your network, the [SCM connector](/docs/en/self-hosted-environments-reference#scm-connector-flags) carries the hosted pre-session flows over an outbound connection instead, so the allowlist isn't needed for them.

### Desktop and claude.ai

The preceding table covers the standalone CLI. The Claude Desktop app and claude.ai in a browser load their application code and user content from additional Anthropic CDN hosts, including `assets-proxy.anthropic.com` and the other `*.claudeusercontent.com` origins that serve [artifacts](/docs/en/artifacts) in those apps. Allowing `claude.ai` while blocking those hosts produces a blank page rather than an error. See [network access requirements](/docs/en/desktop#network-access-requirements) on the Desktop page.

An [artifact](/docs/en/artifacts) that loads a typeface from [Google Fonts](/docs/en/artifacts#improve-the-visual-design) also requests `fonts.googleapis.com` and `fonts.gstatic.com`. Both hosts are optional. If you block them, artifacts render in fallback typefaces. Block with a fast rejection rather than a silent drop so the font request fails immediately instead of delaying the page's first render.

## Additional resources

* [Claude Code settings](/docs/en/settings)
* [Environment variables reference](/docs/en/env-vars)
* [Troubleshooting guide](/docs/en/troubleshooting)
