> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Authentication

> Log in to Claude Code and configure authentication for individuals, teams, and organizations.

Claude Code supports multiple authentication methods depending on your setup. Individual users can log in with a Claude.ai account, while teams can use Claude for Teams or Enterprise, the Claude Console, or a cloud provider like Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry.

## Log in to Claude Code

After [installing Claude Code](/docs/en/setup#install-claude-code), run `claude` in your terminal. On first launch, Claude Code opens a browser window for you to log in.

If the browser doesn't open automatically, press `c` to copy the login URL to your clipboard, then paste it into your browser.

If your browser shows a login code instead of redirecting back after you sign in, paste it into the terminal at the `Paste code here if prompted` prompt. This happens when the browser can't reach Claude Code's local callback server, which is common in WSL2, SSH sessions, and containers.

When login completes, the terminal shows `Login successful` and prompts you to press `Enter` to continue.

You can authenticate with any of these account types:

* **Claude Pro or Max subscription**: log in with your Claude.ai account. Subscribe at [claude.com/pricing](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_pro_max).
* **Claude for Teams or Enterprise**: log in with the Claude.ai account your team admin invited you to.
* **Claude Console**: log in with your Console credentials. Your admin must have [invited you](#claude-console-authentication) first.
* **Cloud providers**: if your organization uses [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), or [Microsoft Foundry](/docs/en/microsoft-foundry), set the required environment variables before running `claude`, or select **3rd-party platform** at the login prompt, which launches an interactive setup wizard for Bedrock and Vertex AI. No browser login is needed.
* **Cloud gateway**: if your organization runs a self-hosted [Claude apps gateway](/docs/en/claude-apps-gateway), sign in with corporate SSO through `/login`. The gateway-issued token is the session's only credential.

Admins can restrict which login methods and organizations are accepted; see [Restrict login to your organization](#restrict-login-to-your-organization).

To log out and re-authenticate, type `/logout` at the Claude Code prompt. Logging out also resets your first-launch setup state, so the next time you run `claude` it walks you through login and setup again.

If you're having trouble logging in, see [authentication troubleshooting](/docs/en/troubleshoot-install#login-and-authentication).

## Set up team authentication

For teams and organizations, you can configure Claude Code access in one of these ways:

* [Claude for Teams or Enterprise](#claude-for-teams-or-enterprise), recommended for most teams
* [Claude Console](#claude-console-authentication)
* [Claude apps gateway](/docs/en/claude-apps-gateway), a self-hosted gateway that signs developers in with your IdP and routes inference to the cloud provider you configure
* [Amazon Bedrock](/docs/en/amazon-bedrock)
* [Google Cloud's Agent Platform](/docs/en/google-vertex-ai)
* [Microsoft Foundry](/docs/en/microsoft-foundry)

### Claude for Teams or Enterprise

[Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_teams#team-&-enterprise) and [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_enterprise) provide the best experience for organizations using Claude Code. Team members get access to both Claude Code and Claude on the web with centralized billing and team management.

* **Claude for Teams**: self-service plan with collaboration features, admin tools, and billing management. Best for smaller teams.
* **Claude for Enterprise**: adds SSO, domain capture, role-based permissions, compliance API, and managed policy settings for organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements.

<Steps>
  <Step title="Subscribe">
    Subscribe to [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_teams_step#team-&-enterprise) or contact sales for [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_enterprise_step).
  </Step>

  <Step title="Invite team members">
    Invite team members from the admin dashboard.
  </Step>

  <Step title="Install and log in">
    Team members install Claude Code and log in with their Claude.ai accounts.
  </Step>
</Steps>

### Claude Console authentication

For organizations that prefer API-based billing, you can set up access through the Claude Console.

<Steps>
  <Step title="Create or use a Console account">
    Use your existing Claude Console account or create a new one.
  </Step>

  <Step title="Add users">
    You can add users through either method:

    * Bulk invite users from within the Console: Settings -> Members -> Invite
    * [Set up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)
  </Step>

  <Step title="Assign roles">
    When inviting users, assign one of:

    * **Claude Code** role: users can only create Claude Code API keys
    * **Developer** role: users can create any kind of API key
  </Step>

  <Step title="Users complete setup">
    Each invited user needs to:

    * Accept the Console invite
    * [Check system requirements](/docs/en/setup#system-requirements)
    * [Install Claude Code](/docs/en/setup#install-claude-code)
    * Log in with Console account credentials
  </Step>
</Steps>

### Cloud provider authentication

For teams using Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry:

<Steps>
  <Step title="Follow provider setup">
    Follow the [Amazon Bedrock docs](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform docs](/docs/en/google-vertex-ai), or [Microsoft Foundry docs](/docs/en/microsoft-foundry).
  </Step>

  <Step title="Distribute configuration">
    Distribute the environment variables and instructions for generating cloud credentials to your users. Read more about how to [manage configuration here](/docs/en/settings).
  </Step>

  <Step title="Install Claude Code">
    Users can [install Claude Code](/docs/en/setup#install-claude-code).
  </Step>
</Steps>

### Restrict login to your organization

To require that developer sessions authenticate into a specific Anthropic organization, set [`forceLoginMethod` and `forceLoginOrgUUID`](/docs/en/settings#available-settings) in [managed settings](/docs/en/settings#settings-files). Set `forceLoginOrgUUID` to your organization ID, shown in [claude.ai admin settings](https://claude.ai/admin-settings/organization) for Claude for Teams or Enterprise organizations, or at [platform.claude.com/settings/organization](https://platform.claude.com/settings/organization) for Console organizations. With both keys set, Claude Code restricts login to the listed organization and exits at startup if the active credential belongs to a different one.

Developers can log in from several paths: the terminal `/login` flow, the [VS Code extension](/docs/en/vs-code), the Agent SDK, `claude setup-token`, `/install-github-app`, and [gateway](/docs/en/claude-apps-gateway) sign-in for organizations that route through a cloud gateway. On Claude Code v2.1.212 or later, every path enforces `forceLoginMethod`; before v2.1.212, only terminal logins enforced either key. The paths differ on `forceLoginOrgUUID`:

* **Terminal, VS Code extension, and Agent SDK logins**: enforce both keys
* **`claude setup-token` and `/install-github-app`**: enforce only `forceLoginMethod`, so they can mint a token in a different organization
* **[Gateway](/docs/en/claude-apps-gateway) sign-in**: selected by `forceLoginMethod: "gateway"` rather than restricted by it, and doesn't authenticate against an Anthropic organization, so `forceLoginOrgUUID` doesn't apply; use your gateway identity provider to restrict access

Deploy the keys through your device management tooling. [Server-managed settings](/docs/en/server-managed-settings) reach only accounts that are already authenticated into your organization, so they can't redirect a developer's first login. If your organization distributes server-managed settings as well, set the keys in both places: managed-settings sources [don't merge](/docs/en/server-managed-settings#settings-precedence), and cached server-managed settings replace the device-managed file entirely.

The keys also block sessions authenticated by `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `apiKeyHelper`, since organization membership can't be verified for an environment credential. Cloud provider sessions such as Amazon Bedrock authenticate against your cloud provider and aren't blocked; restrict those through your cloud IAM policies. See [`forceLoginOrgUUID`](/docs/en/settings#available-settings) in the settings reference for the full behavior. Before v2.1.146, the pin applied only to the login flow and didn't block API-key credentials.

## Credential management

Claude Code securely manages your authentication credentials:

* **Storage location**:
  * On macOS, credentials are stored in the encrypted macOS Keychain.
  * On Linux, credentials are stored in `~/.claude/.credentials.json` with file mode `0600`.
  * On Windows, credentials are stored in `%USERPROFILE%\.claude\.credentials.json` and inherit the access controls of your user profile directory, which restricts the file to your user account by default.
  * If you've set the `CLAUDE_CONFIG_DIR` environment variable on Linux or Windows, the `.credentials.json` file lives under that directory instead.
  * Claude Code manages `.credentials.json` through `/login` and `/logout`. To route requests through a custom API endpoint, set the [`ANTHROPIC_BASE_URL`](/docs/en/env-vars) environment variable instead.
* **Supported authentication types**: Claude.ai credentials, Claude API credentials, Microsoft Foundry Auth, Bedrock Auth, Vertex Auth, and [Claude apps gateway](/docs/en/claude-apps-gateway) session tokens.
* **Custom credential scripts**: the [`apiKeyHelper`](/docs/en/settings#available-settings) setting can be configured to run a shell script that returns an API key.
* **Refresh intervals**: by default, `apiKeyHelper` is called after 5 minutes or on HTTP 401 response. Set `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` environment variable for custom refresh intervals.
* **Slow helper notice**: if `apiKeyHelper` takes longer than 10 seconds to return a key, Claude Code displays a warning notice in the prompt bar showing the elapsed time. If you see this notice regularly, check whether your credential script can be optimized.
* **Helper failures**: {/* min-version: 2.1.208 */}when the script exits with an error, times out, or prints nothing, requests fail with [`Your apiKeyHelper script is failing`](/docs/en/errors#your-apikeyhelper-script-is-failing) within three attempts. Before v2.1.208, helper failures surfaced as a generic 401 after about ten silent retries.

`apiKeyHelper`, `ANTHROPIC_API_KEY`, and `ANTHROPIC_AUTH_TOKEN` apply to the CLI and the surfaces that wrap it, including the VS Code extension, the Agent SDK, and GitHub Actions. Claude Desktop and cloud sessions do not call `apiKeyHelper` or read these environment variables: they use OAuth, except desktop sessions running a [third-party inference configuration](/docs/en/llm-gateway-connect#desktop-app), which authenticate with that configuration's credential.

### Renew an expiring login

When the login you created with `/login` is within five days of expiring, Claude Code shows a warning at startup: `Your login expires in 3 days · run /login to renew`. Requires Claude Code v2.1.203 or later.

Run `/login` to renew. The warning is informational and never blocks a request: authentication keeps working until the login actually expires. The login lifetime itself is unchanged; the advance warning is what v2.1.203 adds.

{/* min-version: 2.1.206 */}Once the stored login expires and can't be refreshed, each request fails with [`Login expired · Please run /login`](/docs/en/errors#login-expired) until you sign in again. Before v2.1.206, an expired login surfaced as a model error instead.

{/* min-version: 2.1.210 */}You can check for this state before a request fails: [`/status`](/docs/en/commands) shows a `Login` row reading `Expired — log in again`, plus the organization and email it has saved for the expired login. The row appears only when the saved claude.ai or Claude Console login is the active credential. The row requires Claude Code v2.1.210 or later.

The warning appears only when a claude.ai or Claude Console login is the active credential, and not when a cloud provider, `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `apiKeyHelper` supplies the credential.

Renewing early matters most for sessions that run unattended. A [background session in agent view](/docs/en/agent-view) or a [Remote Control](/docs/en/remote-control) session that outlives the login stops making progress once the credential expires and can't recover until you sign in again.

### Authentication precedence

When multiple credentials are present, Claude Code chooses one in this order:

1. Cloud provider credentials, when `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, or `CLAUDE_CODE_USE_FOUNDRY` is set. See [third-party integrations](/docs/en/third-party-integrations) for setup.
2. `ANTHROPIC_AUTH_TOKEN` environment variable. Sent as the `Authorization: Bearer` header. Use this when routing through an [LLM gateway or proxy](/docs/en/llm-gateway) that authenticates with bearer tokens rather than Anthropic API keys.
3. `ANTHROPIC_API_KEY` environment variable. Sent as the `X-Api-Key` header. Use this for direct Anthropic API access with a key from the [Claude Console](https://platform.claude.com). In interactive mode, you are prompted once to approve or decline the key, and your choice is remembered. To change it later, use the "Use custom API key" toggle in `/config`. The toggle only appears while `ANTHROPIC_API_KEY` is set in your environment. In non-interactive mode (`-p`), the key is always used when present.
4. [`apiKeyHelper`](/docs/en/settings#available-settings) script output. Use this for dynamic or rotating credentials, such as short-lived tokens fetched from a vault.
5. `CLAUDE_CODE_OAUTH_TOKEN` environment variable. A long-lived OAuth token generated by [`claude setup-token`](#generate-a-long-lived-token). Use this for CI pipelines and scripts where browser login isn't available.
6. Subscription OAuth credentials from `/login`. This is the default for Claude Pro, Max, Team, and Enterprise users.

A signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) session sits outside this list: it is a provider selection like Amazon Bedrock or Google Cloud's Agent Platform, and it outranks them. When a gateway session exists, the CLI authenticates with the gateway token even if `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, or `CLAUDE_CODE_USE_FOUNDRY` is set, and the bearer token, API key, and `apiKeyHelper` entries above are not used.

If you have an active Claude subscription but also have `ANTHROPIC_API_KEY` set in your environment, the API key takes precedence once approved. This can cause authentication failures if the key belongs to a disabled or expired organization. Run `unset ANTHROPIC_API_KEY` to fall back to your subscription, and check `/status` to confirm which method is active. The `Login method` row shows your subscription account, and an `API key` row appears when an API key is in use.

[Claude Code on the Web](/docs/en/claude-code-on-the-web) always uses your subscription credentials. If you set `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` in the sandbox environment, it doesn't override your subscription credentials.

### Generate a long-lived token

For CI pipelines, scripts, or other environments where interactive browser login isn't available, generate a one-year OAuth token with `claude setup-token`:

```bash theme={null}
claude setup-token
```

The command opens the same browser authorization flow as `/login`, and the token prints to the terminal after you approve access in the browser. It does not save the token anywhere; copy it and set it as the `CLAUDE_CODE_OAUTH_TOKEN` environment variable wherever you want to authenticate:

```bash theme={null}
export CLAUDE_CODE_OAUTH_TOKEN=your-token
```

This token authenticates with your Claude subscription and requires a Pro, Max, Team, or Enterprise plan. It can only make model requests, so it can't establish [Remote Control](/docs/en/remote-control) sessions or fetch [claude.ai connectors](/docs/en/mcp#use-mcp-servers-from-claude-ai). MCP servers you configure locally still work.

[Bare mode](/docs/en/headless#start-faster-with-bare-mode) does not read `CLAUDE_CODE_OAUTH_TOKEN`. If your script passes `--bare`, authenticate with `ANTHROPIC_API_KEY` or an `apiKeyHelper` instead.
