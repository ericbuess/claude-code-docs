> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure server-managed settings

> Centrally configure Claude Code for your organization through server-delivered settings, without requiring device management infrastructure.

Server-managed settings let organization Owners centrally configure Claude Code from [**Admin Settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code) in the claude.ai console. Claude Code clients fetch these settings automatically when users authenticate with an organization OAuth login or a directly configured API key, on platforms where server-managed delivery is supported. See [Platform availability](#platform-availability).

This approach is designed for organizations that don't have device management infrastructure in place, or that need to manage settings for users on unmanaged devices.

<Note>
  Server-managed settings are available for [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) and [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise) customers.
</Note>

## Requirements

To use server-managed settings, you need:

* Claude for Teams or Claude for Enterprise plan
* The Owner or Primary Owner role in your Claude organization, to view and edit the configuration
* Network access to `api.anthropic.com`

## Choose between server-managed and endpoint-managed settings

Claude Code supports two approaches for centralized configuration. Server-managed settings deliver configuration from Anthropic's servers. [Endpoint-managed settings](/docs/en/settings#settings-files) are deployed directly to devices through native OS policies (macOS managed preferences, Windows registry) or managed settings files.

| Approach                                                     | Best for                                                 | Security model                                                                                            |
| :----------------------------------------------------------- | :------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------- |
| **Server-managed settings**                                  | Organizations without MDM, or users on unmanaged devices | Settings delivered from Anthropic's servers at authentication time                                        |
| **[Endpoint-managed settings](/docs/en/settings#settings-files)** | Organizations with MDM or endpoint management            | Settings deployed to devices via MDM configuration profiles, registry policies, or managed settings files |

If your devices are enrolled in an MDM or endpoint management solution, endpoint-managed settings provide stronger security guarantees because the settings file can be protected from user modification at the OS level. Endpoint-managed settings don't reach [cloud sessions](/docs/en/model-config#surface-coverage), so organizations using Claude Code on the web should configure server-managed settings as well.

## Configure server-managed settings

<Steps>
  <Step title="Open the admin console">
    In the claude.ai console, go to [**Admin Settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code).

    If the link redirects you to a different Admin Settings page instead of the Claude Code page, your account doesn't have the required role. Admin and other non-Owner roles can't view or edit managed settings, so ask an Owner or Primary Owner in your organization to make the change. See [Access control](#access-control).
  </Step>

  <Step title="Define your settings">
    Add your configuration as JSON. All [settings available in `settings.json`](/docs/en/settings#available-settings) are supported except those restricted to OS-level policy delivery; see [Current limitations](#current-limitations) for that short list. This includes [hooks](/docs/en/hooks), [environment variables](/docs/en/env-vars), and [managed-only settings](/docs/en/permissions#managed-only-settings) like `allowManagedPermissionRulesOnly`.

    This example enforces a permission deny list, prevents users from bypassing permissions, and restricts permission rules to those defined in managed settings:

    ```json theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      },
      "allowManagedPermissionRulesOnly": true
    }
    ```

    Hooks use the same format as in `settings.json`.

    This example runs an audit script after every file edit across the organization:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    To configure the [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode) classifier so it knows which repos, buckets, and domains your organization trusts:

    ```json theme={null}
    {
      "autoMode": {
        "environment": [
          "Source control: github.example.com/acme-corp and all repos under it",
          "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
          "Trusted internal domains: *.corp.example.com"
        ]
      }
    }
    ```

    Because hooks execute shell commands, users see a [security approval dialog](#security-approval-dialogs) before they're applied. See [Configure auto mode](/docs/en/auto-mode-config) for how the `autoMode` entries affect what the classifier blocks and important warnings about the `environment`, `allow`, `soft_deny`, and `hard_deny` fields.
  </Step>

  <Step title="Save and deploy">
    Save your changes. Claude Code clients receive the updated settings on their next startup or hourly polling cycle.
  </Step>
</Steps>

### Verify settings delivery

To confirm that settings are being applied, ask a user to restart Claude Code. If the configuration includes settings that trigger the [security approval dialog](#security-approval-dialogs), the user sees a prompt describing the managed settings on startup. You can also verify that managed permission rules are active by having a user run `/permissions` to view their effective permission rules.

### Access control

The following roles can manage server-managed settings:

* **Primary Owner**
* **Owner**

Restrict access to trusted personnel, as settings changes apply to all users in the organization.

### Managed-only settings

Most [settings keys](/docs/en/settings#available-settings) work in any scope. A handful of keys are only read from managed settings and have no effect when placed in user or project settings files. See [managed-only settings](/docs/en/permissions#managed-only-settings) for the full list. Any setting not on that list can still be placed in managed settings and takes the highest precedence.

### Current limitations

Server-managed settings have the following limitations:

* Settings apply uniformly to all users in the organization. Per-group configurations are not yet supported.
* A [`managed-mcp.json`](/docs/en/managed-mcp) file can't be distributed through server-managed settings. Deliver the `allowedMcpServers` and `deniedMcpServers` policy keys there instead.
* Settings restricted to OS-level policy sources, such as `policyHelper` and `wslInheritsWindowsSettings`, are not honored. Deploy them through MDM or a system `managed-settings.json` file instead.

## Settings delivery

### Settings precedence

Server-managed settings and [endpoint-managed settings](/docs/en/settings#settings-files) both occupy the highest tier in the Claude Code [settings hierarchy](/docs/en/settings#settings-precedence). No other settings level can override them, including command line arguments.

Within the managed tier, a configured [`policyHelper`](/docs/en/settings#compute-managed-settings-with-a-policy-helper) preempts every other managed source, including server-managed settings: its output becomes the only managed configuration for the run.

Otherwise, Claude Code uses the first source that delivers a non-empty configuration. Server-managed settings are checked first, then endpoint-managed settings. Sources don't merge: if server-managed settings deliver any keys at all, other endpoint-managed settings are ignored. If server-managed settings deliver nothing, endpoint-managed settings apply.

A small set of [cross-source lock keys](/docs/en/settings#settings-precedence), such as the sandbox allowlist locks, is honored when any admin-controlled managed source sets them; the user-writable HKCU registry tier is excluded, and when a [`policyHelper`](/docs/en/settings#compute-managed-settings-with-a-policy-helper) is configured, its output is the only source these checks read.

If you clear your server-managed configuration in the admin console with the intent of falling back to an endpoint-managed plist or registry policy, be aware that [cached settings](#fetch-and-caching-behavior) persist on client machines until the next successful fetch. Run `/status` to see which managed source is active.

### Fetch and caching behavior

Claude Code fetches settings from Anthropic's servers at startup and polls for updates hourly during active sessions.

**First launch without cached settings:**

* Claude Code fetches settings asynchronously
* If the fetch fails, Claude Code continues without managed settings
* There is a brief window before settings load where restrictions are not yet enforced

**Subsequent launches with cached settings:**

* Cached settings apply immediately at startup, except for the transport, routing, and authentication environment variables described below
* Claude Code fetches fresh settings in the background
* Cached settings persist through network failures. The withheld environment variables remain withheld until a fetch succeeds

As of v2.1.198, Claude Code withholds three categories of variables in the cached `env` block until the server confirms the payload for the session. This keeps a cached proxy, certificate authority, endpoint, or credential value from redirecting, intercepting, or re-authenticating the settings fetch that confirms the payload. The hardening applies only to the server-fetched settings cache: [endpoint-managed settings](/docs/en/settings#settings-files) deployed through MDM or `managed-settings.json` are unaffected. The withheld categories are:

* Proxy and TLS configuration, such as `HTTPS_PROXY`, `NODE_EXTRA_CA_CERTS`, and the mTLS client certificate variables `CLAUDE_CODE_CLIENT_CERT` and `CLAUDE_CODE_CLIENT_KEY`
* API routing and provider selection, including `ANTHROPIC_BASE_URL`, the provider selection variables such as `CLAUDE_CODE_USE_BEDROCK` and `CLAUDE_CODE_USE_VERTEX`, and the provider endpoint URLs such as `ANTHROPIC_BEDROCK_BASE_URL`
* Authentication credentials, such as `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, and `CLAUDE_CODE_OAUTH_TOKEN`

Every other key in the cached `env` block, such as telemetry and OpenTelemetry configuration, applies at startup as before. Once the fetch succeeds, the withheld variables apply for the rest of the session.

If your organization needs a proxy to reach `api.anthropic.com`, set it in the shell environment or in [user settings](/docs/en/settings#settings-files) rather than only in the managed `env` block. The first launch has no cache, so those sources were already required for the initial fetch.

Claude Code applies settings updates automatically without a restart, except for advanced settings like OpenTelemetry configuration, which require a full restart to take effect.

### Invalid entries in delivered settings

Delivered payloads parse tolerantly with the same rules as the other managed sources. When a payload contains an entry that fails schema validation, Claude Code strips that entry, surfaces a validation error, and applies every remaining valid setting. See [Invalid entries in managed settings](/docs/en/settings#invalid-entries-in-managed-settings) for the field-level behavior, including how security-enforcement fields are handled. Requires Claude Code v2.1.169 or later.

Server-managed delivery adds these behaviors:

* The cache at `~/.claude/remote-settings.json` stores the salvaged payload with invalid entries removed. The raw invalid payload is never persisted.
* When no field in the payload can be salvaged, Claude Code keeps the last-accepted cached settings and records a fatal error.
* The [security approval dialog](#security-approval-dialogs) evaluates the salvaged payload, so a stripped invalid entry is never presented for approval and never executes.

To debug delivery issues, run `claude --debug-file <path>` and search the log for `Remote settings`. Validate a payload change with `claude doctor` on a test machine before rolling it out to the organization.

### Enforce fail-closed startup

By default, if the remote settings fetch fails at startup, the CLI continues without managed settings. For environments where this brief unenforced window is unacceptable, set `forceRemoteSettingsRefresh: true` in your managed settings.

When this setting is active, the CLI blocks at startup until remote settings are freshly fetched. If the fetch fails, the CLI exits rather than proceeding without the policy. This setting self-perpetuates: once delivered from the server, it is also cached locally so that subsequent startups enforce the same behavior even before the first successful fetch of a new session.

To enable this, add the key to your managed settings configuration:

```json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

You can also set this key in an [endpoint-managed](/docs/en/settings#settings-files) MDM profile or system `managed-settings.json` file to enforce fail-closed behavior on first launch, before any server payload has been delivered. As of v2.1.191, this flag is an exception to the [precedence rule](#settings-precedence) above: it is honored when set in any admin-controlled managed source even if a cached server-managed payload is also present, so an MDM-delivered value is not ignored when server-managed settings exist. When a [`policyHelper`](/docs/en/settings#compute-managed-settings-with-a-policy-helper) is configured, its output replaces every other managed source, this key included.

The settings fetch also sends a `Cache-Control: no-cache` header so intermediate HTTP proxies don't serve a stale response.

Before enabling this setting, ensure your network policies allow connectivity to `api.anthropic.com`. If that endpoint is unreachable, the CLI exits at startup and users cannot start Claude Code.

As of v2.1.139, the `claude auth` subcommands such as `claude auth login` are exempt from this check, so users can re-authenticate when expired credentials are the reason the settings fetch fails.

### Security approval dialogs

Certain settings that could pose security risks require explicit user approval before Claude Code applies them:

* **Shell command settings**: settings that execute shell commands
* **Custom environment variables**: variables not in the known safe allowlist
* **Hook configurations**: any hook definition
* **Managed CLAUDE.md content**: a `claudeMd` value delivered through managed settings

When these settings are present, users see a security dialog explaining what is being configured. Users must approve to proceed. If a user rejects the settings, Claude Code exits.

If an interactive session can't show the dialog, Claude Code doesn't apply the delivered settings and keeps the last-approved settings; the dialog appears in the next session that can show it. Requires Claude Code v2.1.211 or later.

<Note>
  A non-interactive run, such as `claude -p` or an Agent SDK session, can't show the dialog. When the delivered settings would require approval, Claude Code applies them for that run only: it doesn't record them as approved or write them to the [local cache](#fetch-and-caching-behavior), and the next interactive session shows the dialog. Until a user approves in an interactive session, each non-interactive run fetches the settings again at startup. Before v2.1.207, a non-interactive run saved the settings as approved, so later interactive sessions never showed the dialog for them.
</Note>

## Platform availability

Server-managed settings require a direct connection to `api.anthropic.com`, and delivery requires the session to authenticate with an organization OAuth login or a directly configured API key. Keys returned by an [`apiKeyHelper`](/docs/en/settings#available-settings) script don't trigger the settings fetch.

Server-managed settings are not available when using third-party model providers:

* Amazon Bedrock
* Google Cloud's Agent Platform
* Microsoft Foundry
* [Claude Platform on AWS](/docs/en/claude-platform-on-aws)
* Custom API endpoints via `ANTHROPIC_BASE_URL` or third-party [LLM gateways](/docs/en/llm-gateway)

If you export a `CLAUDE_CODE_USE_*` provider variable or a non-default `ANTHROPIC_BASE_URL` in your shell, Claude Code skips the settings fetch for your sessions. You can't clear the export with a server-managed `env` block, because the block arrives through the fetch that the export prevents. An [endpoint-managed settings](/docs/en/settings#settings-files) `env` block doesn't restore the fetch either: Claude Code checks eligibility before it applies managed `env` blocks, so the override changes the session's provider selection but the fetch stays skipped.

To restore server-managed delivery, remove the export from your shell, or set the variable to `""` in your user settings `env` block, which applies before the eligibility check. To enforce policy without relying on users to change their shells, deliver the settings through the endpoint-managed channel instead.

For Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry deployments, a self-hosted [Claude apps gateway](/docs/en/claude-apps-gateway) provides the equivalent remote managed-settings delivery: gateway-signed-in clients fetch managed settings from the gateway instead of `api.anthropic.com`. The failure semantics differ at startup: a gateway client that can't reach the gateway exits with an error instead of falling back to cached settings, while the hourly background refresh is fail-open on both channels.

## Audit logging

Audit log events for settings changes are available through the compliance API or audit log export. Contact your Anthropic account team for access.

Audit events include the type of action performed, the account and device that performed the action, and references to the previous and new values.

## Security considerations

Server-managed settings provide centralized policy enforcement, but they operate as a client-side control, not a security boundary. On unmanaged devices, a user doesn't need admin or sudo access to bypass them.

| Scenario                                                               | Behavior                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| :--------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| User edits the cached settings file                                    | Tampered file applies at startup, but correct settings restore on the next server fetch. {/* min-version: 2.1.198 */}As of v2.1.198, the transport, API-routing, and authentication environment variables in the `env` block are [withheld until the server confirms the payload](#fetch-and-caching-behavior)                                                                                                                                                                                                    |
| User deletes the cached settings file                                  | First-launch behavior occurs: settings fetch asynchronously with a brief unenforced window                                                                                                                                                                                                                                                                                                                                                                                                                        |
| User runs a modified Claude Code binary                                | A user who can run a modified client can bypass any client-side control                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| User runs an older Claude Code version                                 | Versions that predate server-managed settings don't fetch or apply them                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| API is unavailable                                                     | Cached settings apply if available, otherwise managed settings are not enforced until the next successful fetch. {/* min-version: 2.1.198 */}As of v2.1.198, the transport, API-routing, and authentication environment variables in the cached `env` block are [withheld on fetch failure](#fetch-and-caching-behavior); the rest of the cache still applies. With `forceRemoteSettingsRefresh: true`, the CLI exits instead of continuing, except for [`claude auth` subcommands](#enforce-fail-closed-startup) |
| User authenticates with a different organization                       | Settings are not delivered for accounts outside the managed organization                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| User configures a [third-party model provider](#platform-availability) | Server-managed settings are bypassed. This includes setting `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_MANTLE`, `CLAUDE_CODE_USE_VERTEX`, `CLAUDE_CODE_USE_FOUNDRY`, `CLAUDE_CODE_USE_ANTHROPIC_AWS`, or a non-default `ANTHROPIC_BASE_URL`                                                                                                                                                                                                                                                                      |
| Network traffic is intercepted or redirected                           | Disabled TLS validation or intercepted traffic can alter the settings the client receives                                                                                                                                                                                                                                                                                                                                                                                                                         |

To detect runtime configuration changes, use [`ConfigChange` hooks](/docs/en/hooks#configchange) to log modifications or block unauthorized changes before they take effect.

To restrict which organizations your users can access with credentials the client supplies, see [Enforce network-level access control with Tenant Restrictions](https://support.claude.com/en/articles/13198485-enforce-network-level-access-control-with-tenant-restrictions) in the Claude Help Center. For stronger enforcement guarantees, use [endpoint-managed settings](/docs/en/settings#settings-files) on devices enrolled in an MDM solution.

## See also

Related pages for managing Claude Code configuration:

* [Settings](/docs/en/settings): complete configuration reference including all available settings
* [Endpoint-managed settings](/docs/en/settings#settings-files): managed settings deployed to devices by IT
* [Authentication](/docs/en/authentication): set up user access to Claude Code
* [Security](/docs/en/security): security safeguards and best practices
