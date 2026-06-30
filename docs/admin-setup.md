> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Set up Claude Code for your organization

> A decision map for administrators deploying Claude Code, covering API providers, managed settings, policy enforcement, usage monitoring, and data handling.

Claude Code enforces organization policy through managed settings that take precedence over local developer configuration. You deliver those settings from the Claude admin console, your mobile device management (MDM) system, or a file on disk. The settings control which tools, commands, servers, and network destinations Claude can reach.

This page walks through the deployment decisions in order. Each row links to the section below and to the reference page for that area.

<Note>
  SSO, SCIM provisioning, and seat assignment are configured at the Claude account level. See the [Claude Enterprise Administrator Guide](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide) and [seat assignment](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan) for those steps.
</Note>

| Decision                                                                | What you're choosing                                | Reference                                                                                                                                |
| :---------------------------------------------------------------------- | :-------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- |
| [Choose your API provider](#choose-your-api-provider)                   | Where Claude Code authenticates and how it's billed | [Authentication](/en/authentication), [Bedrock](/en/amazon-bedrock), [Vertex AI](/en/google-vertex-ai), [Foundry](/en/microsoft-foundry) |
| [Decide how settings reach devices](#decide-how-settings-reach-devices) | How managed policy reaches developer machines       | [Server-managed settings](/en/server-managed-settings), [Settings files](/en/settings#settings-files)                                    |
| [Decide what to enforce](#decide-what-to-enforce)                       | Which tools, commands, and integrations are allowed | [Permissions](/en/permissions), [Sandboxing](/en/sandboxing)                                                                             |
| [Set up usage visibility](#set-up-usage-visibility)                     | How you track spend and adoption                    | [Analytics](/en/analytics), [Monitoring](/en/monitoring-usage), [Costs](/en/costs)                                                       |
| [Review data handling](#review-data-handling)                           | Data retention and compliance posture               | [Data usage](/en/data-usage), [Security](/en/security)                                                                                   |

## Choose your API provider

Claude Code connects to Claude through one of several API providers. Your choice affects billing, authentication, which compliance posture you inherit, and which Claude Code features your developers can use.

| Provider                      | Choose this when                                                                                                                      |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| Claude for Teams / Enterprise | You want Claude Code and claude.ai under one per-seat subscription with no infrastructure to run. This is the default recommendation. |
| Claude Console                | You're API-first or want pay-as-you-go billing                                                                                        |
| Amazon Bedrock                | You want to inherit existing AWS compliance controls and billing                                                                      |
| Google Vertex AI              | You want to inherit existing GCP compliance controls and billing                                                                      |
| Microsoft Foundry             | You want to inherit existing Azure compliance controls and billing                                                                    |

Some Claude Code features require a claude.ai account. [Claude Code on the web](/en/claude-code-on-the-web), [Routines](/en/routines), [Code Review](/en/code-review), [Remote Control](/en/remote-control), and the [Chrome extension](/en/chrome) aren't available through Console API keys or cloud-provider credentials alone. If you deploy through Bedrock, Vertex, or Foundry, plan whether developers also need Claude for Teams or Enterprise seats. Each feature page lists its plan requirements.

For the full provider comparison covering authentication, regions, and feature parity, see the [enterprise deployment overview](/en/third-party-integrations). Each provider's auth setup is in [Authentication](/en/authentication).

Proxy and firewall requirements in [Network configuration](/en/network-config) apply regardless of provider. If you want a single endpoint in front of multiple providers or centralized request logging, see [LLM gateway](/en/llm-gateway).

## Decide how settings reach devices

Managed settings define policy that takes precedence over local developer configuration. Claude Code checks the four sources below in priority order and applies the first one that returns a non-empty configuration, with one exception: a small set of [cross-source lock keys](/en/settings#settings-precedence), such as the sandbox allowlist locks, is honored when any admin-controlled source sets them.

| Mechanism               | Delivery                                                                                                                                                                                              | Priority | Platforms      |
| :---------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------- | :------------- |
| Server-managed          | claude.ai admin console, or a self-hosted [Claude apps gateway](/en/claude-apps-gateway) for gateway sign-ins                                                                                         | Highest  | All            |
| plist / registry policy | macOS: `com.anthropic.claudecode` plist<br />Windows: `HKLM\SOFTWARE\Policies\ClaudeCode`                                                                                                             | High     | macOS, Windows |
| File-based managed      | macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`<br />Linux and WSL: `/etc/claude-code/managed-settings.json`<br />Windows: `C:\Program Files\ClaudeCode\managed-settings.json` | Medium   | All            |
| Windows user registry   | `HKCU\SOFTWARE\Policies\ClaudeCode`                                                                                                                                                                   | Lowest   | Windows only   |

A configured [`policyHelper`](/en/settings#compute-managed-settings-with-a-policy-helper) preempts all four sources: its output becomes the only managed configuration for the run. See [Settings precedence](/en/settings#settings-precedence).

Server-managed settings reach devices at authentication time and refresh hourly during active sessions, with no endpoint infrastructure. Delivery through the claude.ai admin console requires a Claude for Teams or Enterprise plan. Deployments on Bedrock, Vertex AI, or Foundry can get the same remote delivery by running a [Claude apps gateway](/en/claude-apps-gateway), or use one of the file-based or OS-level mechanisms instead.

If your organization mixes providers, configure [server-managed settings](/en/server-managed-settings) for claude.ai users plus a [file-based or plist/registry fallback](/en/settings#settings-files) so other users still receive managed policy.

The plist and HKLM registry locations work with any provider and resist tampering because they require admin privileges to write. The Windows user registry at HKCU is writable without elevation, so treat it as a convenience default rather than an enforcement channel.

By default, WSL reads only the Linux file path at `/etc/claude-code`. To extend your Windows registry and `C:\Program Files\ClaudeCode` policy to WSL on the same machine, set [`wslInheritsWindowsSettings: true`](/en/settings#available-settings) in either of those admin-only Windows sources.

Whichever mechanism you choose, managed values take precedence over user and project settings. Array settings such as `permissions.allow` and `permissions.deny` merge entries from all sources, so developers can extend managed lists but not remove from them. For [two exceptions](/en/settings#settings-precedence), `fallbackModel` and `availableModels`, the managed value replaces lower layers rather than merging.

See [Server-managed settings](/en/server-managed-settings) and [Settings files and precedence](/en/settings#settings-files).

## Decide what to enforce

Managed settings can lock down tools, sandbox execution, restrict MCP servers and plugin sources, and control which hooks run. Each row is a control surface with the setting keys that drive it.

| Control                                                                                | What it does                                                                                                                                                                                                                                               | Key settings                                                                                                 |
| :------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------- |
| [Permission rules](/en/permissions)                                                    | Allow, ask, or deny specific tools and commands                                                                                                                                                                                                            | `permissions.allow`, `permissions.deny`                                                                      |
| [Permission lockdown](/en/permissions#managed-only-settings)                           | Only managed permission rules apply; disable `--dangerously-skip-permissions`                                                                                                                                                                              | `allowManagedPermissionRulesOnly`, `permissions.disableBypassPermissionsMode`                                |
| [Sandboxing](/en/sandboxing)                                                           | OS-level filesystem and network isolation with domain allowlists                                                                                                                                                                                           | `sandbox.enabled`, `sandbox.network.allowedDomains`                                                          |
| [Managed policy CLAUDE.md](/en/memory#deploy-organization-wide-claude-md)              | Org-wide instructions loaded in every session, can't be excluded                                                                                                                                                                                           | File at the managed policy path                                                                              |
| [MCP server control](/en/managed-mcp)                                                  | Restrict which MCP servers users can add or connect to, or deploy a fixed set                                                                                                                                                                              | `allowedMcpServers`, `deniedMcpServers`, `allowManagedMcpServersOnly`, or a deployed `managed-mcp.json` file |
| [Plugin marketplace control](/en/plugin-marketplaces#managed-marketplace-restrictions) | Restrict which marketplace sources users can add and install from, and reject the CLI flags that sideload plugins, agents, and MCP servers for a single run                                                                                                | `strictKnownMarketplaces`, `blockedMarketplaces`, `disableSideloadFlags`                                     |
| [Customization lockdown](/en/settings#strictpluginonlycustomization)                   | Block skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings                                                                                                                         | `strictPluginOnlyCustomization`                                                                              |
| [Hook restrictions](/en/settings#hook-configuration)                                   | Only managed hooks load; restrict HTTP hook URLs                                                                                                                                                                                                           | `allowManagedHooksOnly`, `allowedHttpHookUrls`                                                               |
| [Disable agent view](/en/agent-view#how-background-sessions-are-hosted)                | Turn off `claude agents`, `--bg`, `/background`, and the on-demand supervisor                                                                                                                                                                              | `disableAgentView`                                                                                           |
| [Model restrictions](/en/model-config#restrict-model-selection)                        | `availableModels` filters which models appear in the picker. Adding `enforceAvailableModels` also constrains the auto-selected default model. See [surface coverage](/en/model-config#surface-coverage) for how this setting reaches the CLI, web, and IDE | `availableModels`, `enforceAvailableModels`                                                                  |
| [Version floor](/en/settings)                                                          | Prevent auto-update from installing below an org-wide minimum                                                                                                                                                                                              | `minimumVersion`                                                                                             |
| [Required version range](/en/settings)                                                 | Refuse to start at all when the running version is outside an org-approved range. Stronger than `minimumVersion`, which only blocks downgrades                                                                                                             | `requiredMinimumVersion`, `requiredMaximumVersion`                                                           |

Permission rules and sandboxing cover different layers. Denying WebFetch blocks Claude's fetch tool, but if Bash is allowed, `curl` and `wget` can still reach any URL. Sandboxing closes that gap with a network domain allowlist enforced at the OS level.

For the threat model these controls defend against, see [Security](/en/security).

## Set up usage visibility

Choose monitoring based on what you need to report on.

| Capability          | What you get                                         | Availability                                                                                                                                                              | Where to start                           |
| :------------------ | :--------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------- |
| Usage monitoring    | OpenTelemetry export of sessions, tools, and tokens  | All providers                                                                                                                                                             | [Monitoring usage](/en/monitoring-usage) |
| Analytics dashboard | Per-user metrics, contribution tracking, leaderboard | Anthropic only                                                                                                                                                            | [Analytics](/en/analytics)               |
| Cost tracking       | Spend limits, rate limits, and usage attribution     | Anthropic; on third-party clouds, a [Claude apps gateway](/en/claude-apps-gateway) provides per-user attribution and [spend limits](/en/claude-apps-gateway-spend-limits) | [Costs](/en/costs)                       |

Cloud providers expose spend through AWS Cost Explorer, GCP Billing, or Azure Cost Management. Claude for Teams and Enterprise plans include a usage dashboard at [claude.ai/analytics/claude-code](https://claude.ai/analytics/claude-code).

## Review data handling

On Team, Enterprise, Claude API, and cloud provider plans, Anthropic doesn't train models on your code or prompts. Your API provider determines retention and compliance posture.

| Topic                     | What to know                                                                                         | Where to start                                 |
| :------------------------ | :--------------------------------------------------------------------------------------------------- | :--------------------------------------------- |
| Data usage policy         | What Anthropic collects, how long it's retained, what's never used for training                      | [Data usage](/en/data-usage)                   |
| Zero Data Retention (ZDR) | Nothing stored after the request completes. Available to qualified accounts on Claude for Enterprise | [Zero data retention](/en/zero-data-retention) |
| Security architecture     | Network model, encryption, authentication, audit trail                                               | [Security](/en/security)                       |

If you need request-level audit logging or to route traffic by data sensitivity, place a gateway between developers and your provider: a self-hosted [Claude apps gateway](/en/claude-apps-gateway) records a per-request audit log with IdP identity, or use another [LLM gateway](/en/llm-gateway). For regulatory requirements and certifications, see [Legal and compliance](/en/legal-and-compliance).

## Verify and onboard

After configuring managed settings, have a developer run `/status` inside Claude Code. On the **Status** tab, the `Setting sources` line shows `Enterprise managed settings` followed by the source in parentheses, one of `(remote)`, `(plist)`, `(HKLM)`, `(HKCU)`, or `(file)`. See [Verify active settings](/en/settings#verify-active-settings).

Share these resources to help developers get started:

* [Quickstart](/en/quickstart): first-session walkthrough from install to working with a project
* [Common workflows](/en/common-workflows): patterns for everyday tasks like code review, refactoring, and debugging
* [Claude 101](https://anthropic.skilljar.com/claude-101) and [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action): self-paced Anthropic Academy courses

For login issues, point developers to [authentication troubleshooting](/en/troubleshoot-install#login-and-authentication). The most common fixes are:

* Run `/logout` then `/login` to switch accounts
* Run `claude update` if the enterprise auth option is missing
* Restart the terminal after updating

If a developer sees "You haven't been added to your organization yet," their seat doesn't include Claude Code access and needs to be updated in the admin console.

## Next steps

With provider and delivery mechanism chosen, move on to detailed configuration:

* [Server-managed settings](/en/server-managed-settings): deliver managed policy from the Claude admin console
* [Settings reference](/en/settings): every setting key, file location, and precedence rule
* [Monorepos and large repos](/en/large-codebases): per-directory configuration patterns for organizations deploying into a monorepo
* [Amazon Bedrock](/en/amazon-bedrock), [Google Vertex AI](/en/google-vertex-ai), [Microsoft Foundry](/en/microsoft-foundry): provider-specific deployment
* [Claude Enterprise Administrator Guide](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide): SSO, SCIM, seat management, and rollout playbook
