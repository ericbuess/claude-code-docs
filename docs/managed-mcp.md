> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Control MCP server access for your organization

> Restrict which MCP servers users can add or connect to with managed configuration files, allowlists, and denylists.

By default, anyone running Claude Code can connect any [MCP server](/docs/en/mcp) they choose. Anthropic reviews connectors against its [listing criteria](https://claude.com/docs/connectors/building/review-criteria) before adding them to the [Anthropic Directory](https://claude.ai/directory), but doesn't security-audit or manage any MCP server. As an administrator, you can restrict which servers run in your organization, from deploying a fixed approved set to disabling MCP entirely.

This page covers how to:

* [Choose a pattern](#choose-a-pattern) that matches how much control you need
* [Deploy a fixed server set with `managed-mcp.json`](#exclusive-control-with-managed-mcp-json), including how to [disable MCP entirely](#disable-mcp-entirely)
* [Control servers with allowlists and denylists](#policy-based-control-with-allowlists-and-denylists)
* [Tell users what to expect](#how-restrictions-appear-to-users) when a restriction blocks a server
* [Monitor which servers your organization actually uses](#monitor-mcp-usage)

<Note>
  The [Security](/docs/en/security) page covers the MCP threat model and how to evaluate a server before approving it. [Decide what to enforce](/docs/en/admin-setup#decide-what-to-enforce) covers MCP restrictions alongside the other administrative controls.
</Note>

## Choose a pattern

Claude Code supports a range of restriction levels. Each pattern uses one or both of the mechanisms covered below: `managed-mcp.json` for deploying a fixed set, and `allowedMcpServers`/`deniedMcpServers` for filtering what users configure.

| Pattern                 | What it does                                                                               | Configure                                                                                            |
| :---------------------- | :----------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| **Disable MCP**         | No servers load anywhere                                                                   | `managed-mcp.json` with an empty server map                                                          |
| **Fixed deployment**    | Every user gets the same servers and can't add others                                      | `managed-mcp.json` with the servers you want                                                         |
| **Approved catalog**    | Publish a list of approved servers; users add the ones they want, anything else is blocked | `allowedMcpServers` + `allowManagedMcpServersOnly: true`                                             |
| **Plugin servers only** | Servers can only come from plugins; users can't add their own                              | [`strictPluginOnlyCustomization`](/docs/en/settings#strictpluginonlycustomization) with `mcp` in the list |
| **Soft allowlist**      | Enforce an allowlist that users can broaden in their own settings                          | `allowedMcpServers` without `allowManagedMcpServersOnly`                                             |
| **Denylist only**       | Block known-bad servers, allow everything else                                             | `deniedMcpServers`                                                                                   |
| **No restrictions**     | Users add anything                                                                         | Don't deploy any managed MCP configuration                                                           |

<Note>
  Claude Code doesn't have a built-in MCP server registry that users can browse and install from. For the approved-catalog pattern, share the approved list and its `claude mcp add` commands somewhere your users will find them, such as an internal wiki, or distribute the servers as plugins through a [managed plugin marketplace](/docs/en/plugin-marketplaces#managed-marketplace-restrictions) so users can browse and install them from `/plugin`.
</Note>

## Exclusive control with managed-mcp.json

If you deploy a `managed-mcp.json` file, Claude Code loads only the servers that file defines. Users cannot add, modify, or use any other MCP servers, including plugin-provided servers. The file also suppresses claude.ai connectors unless you [allow them alongside the managed set](#allow-claude-ai-connectors-alongside-the-managed-set).

Two other settings can further filter the managed set:

* `allowedMcpServers` and `deniedMcpServers` apply to managed servers too, so a managed server that doesn't pass them won't load.
* A user's own `deniedMcpServers` merges in from their settings, so users can block a managed server for themselves.

See [How a server is evaluated](#how-a-server-is-evaluated) for the full order of checks.

`managed-mcp.json` is a standalone file, so it cannot be delivered through [server-managed settings](/docs/en/server-managed-settings). Any process that can write to a system path with administrator privileges can deploy it. At scale, that's usually through device management tooling, such as Jamf or a configuration profile on macOS, Group Policy or Intune on Windows, or your fleet management of choice on Linux. Claude Code looks for the file at one of these paths:

| Platform      | Path                                                       |
| :------------ | :--------------------------------------------------------- |
| macOS         | `/Library/Application Support/ClaudeCode/managed-mcp.json` |
| Linux and WSL | `/etc/claude-code/managed-mcp.json`                        |
| Windows       | `C:\Program Files\ClaudeCode\managed-mcp.json`             |

The file uses the same format as a project [`.mcp.json`](/docs/en/mcp#project-scope) file:

```json theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.example.com"
      }
    }
  }
}
```

### Authenticate with per-user credentials

Any user on the machine can read this file, so don't store API keys or other credentials in `env` blocks. Pass per-user credentials with one of these instead:

* [`${VAR}` expansion](/docs/en/mcp#environment-variable-expansion-in-mcp-json) to read secrets from each user's environment.
* [OAuth or per-user headers](/docs/en/mcp#authenticate-with-remote-mcp-servers) so each user authenticates as themselves.
* [`headersHelper`](/docs/en/mcp#use-dynamic-headers-for-custom-authentication) to generate credentials at connection time.

### Validate the configuration

To confirm the file is in effect, run two checks on a managed machine:

1. `claude mcp list` shows only the servers in `managed-mcp.json`. If a user's own servers still appear, the file isn't being read; check the path and permissions.
2. `claude mcp add --transport http test https://example.com/mcp` fails with `Cannot add MCP server: enterprise MCP configuration is active and has exclusive control over MCP servers`. The URL doesn't need to be a real server, since the policy check rejects the command before anything is contacted.

### Disable MCP entirely

Deploy a `managed-mcp.json` containing an empty server map to block every MCP server:

```json theme={null}
{
  "mcpServers": {}
}
```

Users see no MCP servers in `/mcp`, and `claude mcp add` fails with the enterprise-policy error above. Servers users had previously configured stop loading the next time they start a session, with no warning that policy is the reason.

### Allow claude.ai connectors alongside the managed set

Deploying `managed-mcp.json` suppresses [claude.ai connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) by default, including connectors an administrator configured for the organization in the claude.ai admin console. To load those connectors alongside the servers in `managed-mcp.json`, set `"allowAllClaudeAiMcps": true` in a [managed settings source](/docs/en/admin-setup#decide-how-settings-reach-devices). Requires Claude Code v2.1.149 or later.

With the setting enabled, Claude Code loads the same claude.ai connectors it would load if `managed-mcp.json` were not deployed. [Allowlists and denylists](#policy-based-control-with-allowlists-and-denylists) still apply to those connectors, so you can block specific ones with `deniedMcpServers`. The setting affects only claude.ai connectors; plugin-provided servers stay suppressed.

Claude Code reads this setting only from admin-controlled policy tiers: server-managed settings, an MDM-deployed plist or HKLM registry key, or a system `managed-settings.json` file. Placing it in user or project settings has no effect, so users cannot re-enable connectors that exclusive control suppressed.

## Policy-based control with allowlists and denylists

Allowlists and denylists filter which configured servers are allowed to load. They aren't a registry: a server still has to be added by a user, a plugin, or `managed-mcp.json` before the allowlist or denylist applies to it. To deploy servers to users, use [`managed-mcp.json`](#exclusive-control-with-managed-mcp-json). Both lists also filter servers passed with the [`--mcp-config` CLI flag](/docs/en/cli-reference#cli-flags); `--strict-mcp-config` limits which configuration files load and doesn't bypass either list.

To make the allowlist authoritative, set `allowedMcpServers` and `allowManagedMcpServersOnly: true` together in a [managed settings source](/docs/en/admin-setup#decide-how-settings-reach-devices), such as server-managed settings or a deployed `managed-settings.json` file. [Restrict the allowlist to managed settings only](#restrict-the-allowlist-to-managed-settings-only) shows the configuration. Without `allowManagedMcpServersOnly`, allowlists from every settings source merge, including a user's own `~/.claude/settings.json`, so a user can broaden what your allowlist permits. Denylists merge from every source regardless.

<Note>
  `allowManagedMcpServersOnly` is separate from `allowManagedPermissionRulesOnly`, which locks down [permission rules](/docs/en/permissions#managed-settings) only. Setting that flag does not enforce the MCP allowlist.
</Note>

### Match servers by URL, command, or name

`allowedMcpServers` and `deniedMcpServers` are lists of entries. Each entry is an object with a single key that identifies servers by their URL, their command, or their name:

| Key             | Matches                                                               | Use for                                |
| :-------------- | :-------------------------------------------------------------------- | :------------------------------------- |
| `serverUrl`     | A remote server URL, exact or with `*` wildcards                      | HTTP and SSE servers                   |
| `serverCommand` | The exact command and arguments that start a stdio server             | Stdio servers                          |
| `serverName`    | The user-assigned label. Exact match only; wildcards are not expanded | Either type, but see the Warning below |

Leaving `allowedMcpServers` unset is different from setting it to an empty array:

| Setting             | Unset (default)     | Empty array `[]`   | Populated                     |
| :------------------ | :------------------ | :----------------- | :---------------------------- |
| `allowedMcpServers` | All servers allowed | No servers allowed | Only matching servers allowed |
| `deniedMcpServers`  | No servers blocked  | No servers blocked | Matching servers blocked      |

See [Invalid entries in managed settings](/docs/en/settings#invalid-entries-in-managed-settings) for what happens when an entry fails schema validation.

<Warning>
  A `serverName` entry, in either list, is not a security control. The name is the label a user assigns when running `claude mcp add` or editing a config file, not the underlying server, so a user can call any server `github`. For claude.ai connectors the name is the display name returned by claude.ai, which can change. To enforce which servers actually run, add `serverCommand` or `serverUrl` entries.
</Warning>

The `serverName` validation differs between the two lists:

* {/* min-version: 2.1.182 */}In `deniedMcpServers`, `serverName` accepts any non-empty string, so you can block [claude.ai connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai) by their display name. For example, `{ "serverName": "claude.ai Slack" }` blocks the Slack connector. Prefer a `serverUrl` entry when you need the deny to be robust to renames, or when a connector name collides and gains a ` (N)` suffix.
* In `allowedMcpServers`, `serverName` is limited to letters, numbers, hyphens, and underscores. Use `serverUrl` to allowlist a claude.ai connector.

To turn off all claude.ai connectors, see [`disableClaudeAiConnectors`](/docs/en/mcp#disable-claude-ai-connectors).

### How a server is evaluated

Before loading a server, including one from `managed-mcp.json`, Claude Code runs three checks in order:

1. **Merge the lists.** Allowlist and denylist entries from every settings source combine into one allowlist and one denylist. When `allowManagedMcpServersOnly` is `true`, only the managed allowlist is kept; the denylist always merges from every source.
2. **Check the denylist.** A server that matches any denylist entry, by URL, command, or name, is blocked. Nothing overrides a denylist match.
3. **Check the allowlist.** If `allowedMcpServers` isn't set anywhere, every server that passed the denylist loads. If it is set, what the server must match depends on its type, shown in the table below.

| Server type          | Allowed when it matches                                                                                          |
| :------------------- | :--------------------------------------------------------------------------------------------------------------- |
| Remote (HTTP or SSE) | A `serverUrl` entry. A `serverName` match counts only when the allowlist contains no `serverUrl` entries         |
| Stdio                | A `serverCommand` entry. A `serverName` match counts only when the allowlist contains no `serverCommand` entries |

Three matching rules apply inside those checks:

* **Commands match exactly.** Every argument, in order. `["npx", "-y", "server"]` does not match `["npx", "server"]` or `["npx", "-y", "server", "--flag"]`.
* **`serverCommand` and `serverUrl` values expand before matching.** Both the policy entry and the server's configured value go through the same [`${VAR}` and `${VAR:-default}` expansion](/docs/en/mcp#environment-variable-expansion-in-mcp-json) as `.mcp.json`, so an entry written as `["${HOME}/bin/server"]` matches a server config that uses either the same reference or the expanded path. On Windows, reference an environment variable that is set there, such as `${USERPROFILE}` instead of `${HOME}`. `serverName` values match literally and never expand.
* **URLs support `*` wildcards** anywhere in the pattern, including the scheme. Hostname matching is case-insensitive and ignores a trailing FQDN dot, so `https://Mcp.Example.com/*` matches `https://mcp.example.com/api`. Paths stay case-sensitive.

| Pattern                     | Allows                                                                 |
| :-------------------------- | :--------------------------------------------------------------------- |
| `https://mcp.example.com/*` | All paths on a specific domain                                         |
| `https://mcp.example.com`   | Also all paths on that domain. A pattern with no path matches any path |
| `https://*.example.com/*`   | Any subdomain of `example.com`                                         |
| `http://localhost:*/*`      | Any port on localhost                                                  |
| `*://mcp.example.com/*`     | Any scheme to a specific domain                                        |

Because `${VAR}` expansion reads Claude Code's own process environment, a `serverCommand` or `serverUrl` policy entry that references a variable expands to whatever value a user sets. Use literal URLs and commands for entries you rely on for enforcement.

### Example configuration

The configuration below sets up a hard allowlist with a denylist. The highlighted lines change how the rest of the list is evaluated, and the callouts after the block explain each one:

```json {3,5,11} theme={null}
{
  "allowedMcpServers": [
    { "serverUrl": "https://api.githubcopilot.com/*" },
    { "serverUrl": "https://mcp.sentry.dev/*" },
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "."] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },
    { "serverUrl": "https://mcp.example.com/*" },
    { "serverUrl": "https://*.internal.example.com/*" }
  ],
  "deniedMcpServers": [
    { "serverName": "dangerous-server" },
    { "serverCommand": ["npx", "-y", "unapproved-package"] },
    { "serverUrl": "https://*.untrusted.example.com/*" }
  ]
}
```

* **Line 3**: the first `serverUrl` entry. Once one exists, every remote server must match a URL pattern, so a user can't get an unlisted remote server through by giving it an allowed name.
* **Line 5**: the first `serverCommand` entry. Same effect for stdio servers, so every local server must match a listed command exactly.
* **Line 11**: a `serverName` entry in the denylist. Denylist entries always apply, so any server named `dangerous-server` is blocked regardless of its URL or command.

A `serverName` entry in this allowlist would never match anything, since both transport types already have stricter entries.

The accordions below walk through how a server is evaluated against other allowlist and denylist combinations.

<Accordion title="URL-only allowlist">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.example.com/*" },
      { "serverUrl": "https://*.internal.example.com/*" }
    ]
  }
  ```

  | Server                                                | Result                                       |
  | :---------------------------------------------------- | :------------------------------------------- |
  | HTTP server at `https://mcp.example.com/api`          | Allowed: matches URL pattern                 |
  | HTTP server at `https://api.internal.example.com/mcp` | Allowed: matches wildcard subdomain          |
  | HTTP server at `https://external.example.com/mcp`     | Blocked: doesn't match any URL pattern       |
  | Stdio server with any command                         | Blocked: no name or command entries to match |
</Accordion>

<Accordion title="Command-only allowlist">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  | Server                                                | Result                            |
  | :---------------------------------------------------- | :-------------------------------- |
  | Stdio server with `["npx", "-y", "approved-package"]` | Allowed: matches command          |
  | Stdio server with `["node", "server.js"]`             | Blocked: doesn't match command    |
  | HTTP server named `my-api`                            | Blocked: no name entries to match |
</Accordion>

<Accordion title="Mixed name and command allowlist">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  | Server                                                                   | Result                                                                |
  | :----------------------------------------------------------------------- | :-------------------------------------------------------------------- |
  | Stdio server named `local-tool` with `["npx", "-y", "approved-package"]` | Allowed: matches command                                              |
  | Stdio server named `local-tool` with `["node", "server.js"]`             | Blocked: command entries exist but doesn't match                      |
  | Stdio server named `github` with `["node", "server.js"]`                 | Blocked: stdio servers must match commands when command entries exist |
  | HTTP server named `github`                                               | Allowed: matches name                                                 |
  | HTTP server named `other-api`                                            | Blocked: name doesn't match                                           |
</Accordion>

<Accordion title="Name-only allowlist">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  | Server                                              | Result                           |
  | :-------------------------------------------------- | :------------------------------- |
  | Stdio server named `github` with any command        | Allowed: no command restrictions |
  | Stdio server named `internal-tool` with any command | Allowed: no command restrictions |
  | HTTP server named `github`                          | Allowed: matches name            |
  | Any server named `other`                            | Blocked: name doesn't match      |
</Accordion>

<Accordion title="Allowlist with denylist override">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://*.example.com/*" }
    ],
    "deniedMcpServers": [
      { "serverUrl": "https://staging.example.com/*" }
    ]
  }
  ```

  | Server                                           | Result                                                    |
  | :----------------------------------------------- | :-------------------------------------------------------- |
  | HTTP server at `https://mcp.example.com/api`     | Allowed: matches allowlist URL pattern, no denylist match |
  | HTTP server at `https://staging.example.com/api` | Blocked: matches both, but the denylist takes precedence  |
  | HTTP server at `https://other.com/mcp`           | Blocked: doesn't match the allowlist                      |
</Accordion>

### Restrict the allowlist to managed settings only

To make the managed allowlist the only one that applies, set `allowManagedMcpServersOnly` in the managed settings file:

```json theme={null}
{
  "allowManagedMcpServersOnly": true,
  "allowedMcpServers": [
    { "serverUrl": "https://api.githubcopilot.com/*" },
    { "serverUrl": "https://*.internal.example.com/*" }
  ]
}
```

When `allowManagedMcpServersOnly` is `true`, allowlists from user, project, and local settings are ignored. The denylist still merges from all sources, so users can always block servers for themselves.

## How restrictions appear to users

When a restriction blocks a server, the user either sees an error from `claude mcp add` or the server silently stops loading. Use this table to recognize those reports and to tell users what to expect before you roll out a change:

| Restriction                                                          | What the user sees                                                                                         |
| :------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- |
| `managed-mcp.json` is present and the user runs `claude mcp add`     | `Cannot add MCP server: enterprise MCP configuration is active and has exclusive control over MCP servers` |
| The server is on a denylist and the user runs `claude mcp add`       | `Cannot add MCP server "<name>": server is explicitly blocked by enterprise policy`                        |
| The server isn't on the allowlist and the user runs `claude mcp add` | `Cannot add MCP server "<name>": not allowed by enterprise policy`                                         |
| A previously configured server is now blocked by policy              | The server silently disappears from `/mcp` and `claude mcp list` with no warning                           |

In the last case, the user gets no signal that policy is the reason their server disappeared, so tell affected users which servers are blocked when you roll out a new restriction.

## Monitor MCP usage

When [OpenTelemetry export](/docs/en/monitoring-usage) is configured, Claude Code can record which MCP servers and tools users invoke. Set `OTEL_LOG_TOOL_DETAILS=1` to include MCP server and tool names in tool events, then aggregate them in your collector to see which servers your users actually connect to. See [Monitoring](/docs/en/monitoring-usage) to set up the exporter and for the full event schema.

## Configuration summary

Every file and setting this page covers, what it controls, and how to deliver it:

| Surface                      | What it controls                                                                    | Where it lives                                                                                                               | How to deliver                                                                                                                                                              |
| :--------------------------- | :---------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `managed-mcp.json`           | Fixed server set, exclusive control                                                 | System path: `/Library/Application Support/ClaudeCode/`, `/etc/claude-code/`, or `C:\Program Files\ClaudeCode\`              | MDM, GPO, fleet management, or any process with administrator privileges. Cannot be set through server-managed settings                                                     |
| `allowedMcpServers`          | Allowlist of permitted servers                                                      | Any [settings file](/docs/en/settings#settings-files); entries from every source merge unless `allowManagedMcpServersOnly` is set | For enforcement, a [managed settings source](/docs/en/admin-setup#decide-how-settings-reach-devices): server-managed settings, `managed-settings.json`, MDM profile, or registry |
| `deniedMcpServers`           | Denylist of blocked servers                                                         | Any settings file; entries from every source merge                                                                           | Same as `allowedMcpServers`                                                                                                                                                 |
| `allowManagedMcpServersOnly` | Locks the allowlist to managed sources only                                         | Managed settings sources only; the setting has no effect elsewhere                                                           | Same as `allowedMcpServers`                                                                                                                                                 |
| `allowAllClaudeAiMcps`       | Loads claude.ai connectors alongside `managed-mcp.json` instead of suppressing them | Managed settings sources only; the setting has no effect elsewhere                                                           | Same as `allowedMcpServers`                                                                                                                                                 |

## Related resources

* [Decide what to enforce](/docs/en/admin-setup#decide-what-to-enforce): MCP restrictions alongside permission rules, sandboxing, and the other admin controls
* [Connect Claude Code to tools via MCP](/docs/en/mcp): the full MCP reference, including transports, scopes, and authentication
* [Settings](/docs/en/settings): the settings hierarchy and how managed settings take precedence
* [Server-managed settings](/docs/en/server-managed-settings): deliver `allowedMcpServers` and `deniedMcpServers` from the Claude.ai admin console
* [Security](/docs/en/security): the threat model these controls defend against
* [Claude Enterprise Administrator Guide](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide): SSO, SCIM, seat management, and rollout playbook
