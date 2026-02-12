> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure server-managed settings (public beta)

> Centrally configure Claude Code for your organization through server-delivered settings, without requiring device management infrastructure.

Server-managed settings allow administrators to centrally configure Claude Code through a web-based interface on Claude.ai. Claude Code clients automatically receive these settings when users authenticate with their organization credentials.

This approach is designed for organizations that do not have device management infrastructure in place, or need to manage settings for users on unmanaged devices.

<Note>
  Server-managed settings are in public beta and available for [Claude for Teams](https://claude.com/pricing#team-&-enterprise) and [Claude for Enterprise](https://anthropic.com/contact-sales) customers. Features may evolve before general availability.
</Note>

## Requirements

To use server-managed settings, you need:

* Claude for Teams or Claude for Enterprise plan
* Claude Code version 2.1.38 or later for Claude for Teams, or version 2.1.30 or later for Claude for Enterprise
* Network access to `api.anthropic.com`

## Choose between server-managed and endpoint-managed settings

Claude Code supports two approaches for centralized configuration. Server-managed settings deliver configuration from Anthropic's servers. [Endpoint-managed settings](/en/permissions#managed-settings) deploy a `managed-settings.json` file to system directories via MDM (mobile device management).

| Approach                                                          | Best for                                                 | Security model                                                     |
| :---------------------------------------------------------------- | :------------------------------------------------------- | :----------------------------------------------------------------- |
| **Server-managed settings**                                       | Organizations without MDM, or users on unmanaged devices | Settings delivered from Anthropic's servers at authentication time |
| **[Endpoint-managed settings](/en/permissions#managed-settings)** | Organizations with MDM or endpoint management            | Settings deployed to protected system directories by IT            |

If your devices are enrolled in an MDM or endpoint management solution, endpoint-managed settings provide stronger security guarantees because the settings file can be protected from user modification at the OS level.

## Configure server-managed settings

<Steps>
  <Step title="Open the admin console">
    In [Claude.ai](https://claude.ai), navigate to **Admin Settings > Claude Code > Managed settings**.
  </Step>

  <Step title="Define your settings">
    Add your configuration as JSON. All [settings available in `settings.json`](/en/settings#available-settings) are supported, including [managed-only settings](/en/permissions#managed-only-settings) like `disableBypassPermissionsMode`.

    This example enforces a permission deny list and prevents users from bypassing permissions:

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ]
      },
      "disableBypassPermissionsMode": "disable"
    }
    ```
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

### Current limitations

Server-managed settings have the following limitations during the beta period:

* Settings apply uniformly to all users in the organization. Per-group configurations are not yet supported.
* [MCP server configurations](/en/mcp#managed-mcp-configuration) cannot be distributed through server-managed settings.

## Settings delivery

### Settings precedence

Server-managed settings and [endpoint-managed settings](/en/permissions#managed-settings) both occupy the highest tier in the Claude Code [settings hierarchy](/en/settings#settings-precedence), and user or project settings cannot override them. When both are present, server-managed settings take precedence and the local `managed-settings.json` file is not used.

### Fetch and caching behavior

Claude Code fetches settings from Anthropic's servers at startup and polls for updates hourly during active sessions.

**First launch without cached settings:**

* Claude Code fetches settings asynchronously
* If the fetch fails, Claude Code continues without managed settings
* There is a brief window before settings load where restrictions are not yet enforced

**Subsequent launches with cached settings:**

* Cached settings apply immediately at startup
* Claude Code fetches fresh settings in the background
* Cached settings persist through network failures

Claude Code applies settings updates automatically without a restart, except for advanced settings like OpenTelemetry configuration, which require a full restart to take effect.

### Security approval dialogs

Certain settings that could pose security risks require explicit user approval before being applied:

* **Shell command settings**: settings that execute shell commands
* **Custom environment variables**: variables not in the known safe allowlist
* **Hook configurations**: any hook definition

When these settings are present, users see a security dialog explaining what is being configured. Users must approve to proceed. If a user rejects the settings, Claude Code exits.

<Note>
  In non-interactive mode with the `-p` flag, Claude Code skips security dialogs and applies settings without user approval.
</Note>

## Platform availability

Server-managed settings require a direct connection to `api.anthropic.com` and are not available when using third-party model providers:

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* Custom API endpoints via `ANTHROPIC_BASE_URL` or [LLM gateways](/en/llm-gateway)

## Audit logging

Audit log events for settings changes are available through the compliance API or audit log export. Contact your Anthropic account team for access.

Audit events include the type of action performed, the account and device that performed the action, and references to the previous and new values.

## Security considerations

Server-managed settings provide centralized policy enforcement, but they operate as a client-side control. On unmanaged devices, users with admin or sudo access can modify the Claude Code binary, filesystem, or network configuration.

| Scenario                                         | Behavior                                                                                                        |
| :----------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| User edits the cached settings file              | Tampered file applies at startup, but correct settings restore on the next server fetch                         |
| User deletes the cached settings file            | First-launch behavior occurs: settings fetch asynchronously with a brief unenforced window                      |
| API is unavailable                               | Cached settings apply if available, otherwise managed settings are not enforced until the next successful fetch |
| User authenticates with a different organization | Settings are not delivered for accounts outside the managed organization                                        |
| User sets a non-default `ANTHROPIC_BASE_URL`     | Server-managed settings are bypassed when using third-party API providers                                       |

For stronger enforcement guarantees, use [endpoint-managed settings](/en/permissions#managed-settings) on devices enrolled in an MDM solution.

## See also

Related pages for managing Claude Code configuration:

* [Settings](/en/settings): complete configuration reference including all available settings
* [Endpoint-managed settings](/en/permissions#managed-settings): file-based managed settings deployed by IT
* [Authentication](/en/authentication): set up user access to Claude Code
* [Security](/en/security): security safeguards and best practices
