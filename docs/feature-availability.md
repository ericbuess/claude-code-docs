> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Feature availability

> Compare which Claude Code features are available across Anthropic subscription plans, the Anthropic Console, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry.

The Claude Code CLI and everything that runs locally work on every provider. For setup instructions per provider, see the [Enterprise deployment overview](/docs/en/third-party-integrations.md). To skip straight to what is missing on your provider, see the [summary by provider](#summary-by-provider) tabs.

In the tables below, ✓ means available, ✗ means not available, and "See note" links to a footnote for partial support. A qualifier after ✓ narrows availability to that subset, and "Admin-enabled" means the feature is off until an organization admin turns it on.

## Availability by model provider

How you authenticate determines which features Claude Code can reach. For a single list of what is missing on your provider, see the [summary by provider](#summary-by-provider) tabs. To find your column in the tables:

* **Claude subscription**: you sign in with a claude.ai account on the Pro, Max, Team, or Enterprise plan
* **Anthropic Console**: you authenticate with an Anthropic API key or by [signing in to a Console account without one](/docs/en/authentication.md#sign-in-without-an-api-key)
* **Amazon Bedrock**: you use Claude models from the Amazon Bedrock model catalog and set `CLAUDE_CODE_USE_BEDROCK`. The [Mantle endpoint](/docs/en/amazon-bedrock.md#use-the-mantle-endpoint) (`CLAUDE_CODE_USE_MANTLE`) is covered by this column
* **Claude Platform on AWS**: you bought Claude through AWS Marketplace but call the Anthropic API, and set `CLAUDE_CODE_USE_ANTHROPIC_AWS`
* **Google Cloud's Agent Platform**: Google-operated; you set `CLAUDE_CODE_USE_VERTEX`
* **Microsoft Foundry**: Anthropic-operated; you set `CLAUDE_CODE_USE_FOUNDRY`

### Features available on every provider

These work on every provider:

* [CLI](/docs/en/quickstart.md) and [Agent SDK](/docs/en/agent-sdk/overview.md)
* [VS Code](/docs/en/vs-code.md) and [JetBrains](/docs/en/jetbrains.md) extensions
* [Subagents](/docs/en/sub-agents.md), [hooks](/docs/en/hooks-guide.md), [commands](/docs/en/commands.md), and [skills](/docs/en/skills.md)
* [CLAUDE.md memory](/docs/en/memory.md), [plugins](/docs/en/plugins/overview.md), and [MCP servers](/docs/en/mcp.md)
* [Checkpoints](/docs/en/checkpointing.md), [sandboxing](/docs/en/sandboxing.md), and [Workflows](/docs/en/workflows.md)
* [OpenTelemetry metrics](/docs/en/monitoring-usage.md) and the [managed settings file](/docs/en/managed-settings.md#delivery-mechanisms)

These have provider-specific differences:

* **MCP servers**: [connectors from claude.ai](/docs/en/mcp.md#use-mcp-servers-from-claude-ai) load only when your claude.ai subscription is the active authentication method. [Tool search](/docs/en/mcp.md#configure-tool-search) isn't supported on Microsoft Foundry [deployments hosted on Azure](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options). On Google Cloud's Agent Platform, tool search isn't supported on models earlier than Claude Opus 4.5, Claude Sonnet 4.5, and Claude Haiku 4.5
* **Subagents**: when the main conversation runs Fable, the built-in [Explore subagent](/docs/en/sub-agents.md#built-in-subagents) runs on Opus with a Claude subscription, an Anthropic Console account, or an [LLM gateway](/docs/en/llm-gateway) reached through `ANTHROPIC_BASE_URL`. On other providers, including Claude Platform on AWS, it runs on Fable
* **[Commands](/docs/en/commands.md#all-commands)**:
  * `/design-sync` and `/import` with its `claude import` subcommand form are unavailable on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS, and through a [Claude apps gateway](/docs/en/claude-apps-gateway#availability-and-limitations)
  * `/voice` requires a claude.ai account
  * `/list-agents` and its alias `/peers` are available only in sessions where [cross-session messaging is enabled](/docs/en/cross-session-messaging.md#availability)

### Features that require a Claude subscription

These require signing in with a claude.ai account and are not reachable with an Anthropic Console API key or from a third-party provider:

* [Cloud sessions](/docs/en/claude-code-on-the-web.md) and Claude Code on mobile
* [Claude Code in Slack](/docs/en/slack.md): Pro and Max plans
* [Claude Code Desktop](/docs/en/desktop.md)
* [Cloud scheduled tasks](/docs/en/routines.md) (`/schedule`)
* [Ultrareview](/docs/en/ultrareview.md)
* [Code Review](/docs/en/code-review.md): Team and Enterprise plans
* [Remote Control](/docs/en/remote-control.md)
* [Chrome extension](/docs/en/chrome.md)
* [Computer use](/docs/en/computer-use.md): Pro and Max plans
* [Artifacts](/docs/en/artifacts.md): Pro, Max, Team, and Enterprise plans
* [Voice dictation](/docs/en/voice-dictation.md)

Desktop is the partial exception: [gateway routing can be configured in the app or by an administrator](/docs/en/llm-gateway-connect.md#desktop-app). [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) also runs the Code tab on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or a self-hosted LLM gateway. It also runs the Code tab on the [Claude API](https://claude.com/docs/third-party/claude-desktop/claude-api) with an Anthropic Console API key. For per-plan availability of these features, see [Availability by subscription plan](#availability-by-subscription-plan).

### CLI capabilities that vary by provider

These features work in the local CLI but depend on a server-side capability that not every provider exposes.

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Claude subscription</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>[Web search](/docs/en/tools-reference.md#websearch-tool-behavior)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
      <td>See note <sup>[1](#fn1)</sup></td>
      <td>✓</td>
    </tr>

    <tr>
      <td>[Fast mode](/docs/en/fast-mode.md)</td>
      <td>✓ ([Owner-enabled](/docs/en/fast-mode.md#enable-fast-mode-for-your-organization) on Team and Enterprise)</td>
      <td>✓ (provisioned organizations)</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Auto mode](/docs/en/auto-mode-config.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>See note <sup>[2](#fn2)</sup></td>
      <td>✓</td>
      <td>See note <sup>[2](#fn2)</sup></td>
      <td>See note <sup>[2](#fn2)</sup></td>
    </tr>

    <tr>
      <td>[Advisor](/docs/en/advisor.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Cross-session messaging](/docs/en/cross-session-messaging.md)</td>
      <td>✓ <sup>[5](#fn5)</sup></td>
      <td>✓ (same machine) <sup>[5](#fn5)</sup></td>
      <td>✓ (same machine) <sup>[5](#fn5)</sup></td>
      <td>✓ (same machine) <sup>[5](#fn5)</sup></td>
      <td>✓ (same machine) <sup>[5](#fn5)</sup></td>
      <td>✓ (same machine) <sup>[5](#fn5)</sup></td>
    </tr>

    <tr>
      <td>[Channels](/docs/en/channels.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[GitHub Actions](/docs/en/github-actions.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
      <td>✓</td>
    </tr>

    <tr>
      <td>[GitLab CI/CD](/docs/en/gitlab-ci-cd.md)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
    </tr>
  </tbody>
</table>

### Admin and analytics

Organization-level controls and usage visibility.

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Claude subscription</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>[Analytics dashboard and API](/docs/en/analytics.md)</td>
      <td>✓ (dashboard: Team and Enterprise; API: Enterprise)</td>
      <td>✓ <sup>[4](#fn4)</sup></td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Server-managed settings](/docs/en/server-managed-settings.md)</td>
      <td>✓ (Team and Enterprise)</td>
      <td>See [Platform availability](/docs/en/server-managed-settings.md#platform-availability)</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Zero Data Retention](/docs/en/zero-data-retention.md)</td>
      <td>✓ (qualified Enterprise accounts)</td>
      <td>✓ (qualified accounts)</td>
      <td>See note <sup>[3](#fn3)</sup></td>
      <td>✓ (qualified accounts)</td>
      <td>See note <sup>[3](#fn3)</sup></td>
      <td>See note <sup>[3](#fn3)</sup></td>
    </tr>
  </tbody>
</table>

<sup>1</sup> On Google Cloud's Agent Platform, web search is available for Opus 4, Sonnet 4, Haiku 4.5, and later models.\

<sup>2</sup> On these providers, auto mode supports only Claude Sonnet 5 or later, Opus 4.7 or later, Haiku 5.5, and the Fable models. See [Auto mode configuration](/docs/en/auto-mode-config.md). For the permission mode a session on these providers starts in, see [Which mode a session starts in](/docs/en/permission-modes.md#which-mode-a-session-starts-in).\

<sup>3</sup> Subject to your agreement with the cloud provider.\

<sup>4</sup> Dashboard and API only. [Contribution metrics](/docs/en/analytics.md#enable-contribution-metrics) requires a claude.ai Team or Enterprise organization.\

<sup>5</sup> Requires Claude Code v2.1.224 or later on macOS and Linux, including Linux inside WSL 2. On native Windows, requires Claude Code v2.1.234 or later. With API key authentication, messaging is same-machine only. On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry, messaging is same-machine only and requires Claude Code v2.1.248 or later. Claude can find your [cloud sessions](/docs/en/claude-code-on-the-web.md) and your sessions on other machines only from a session that is connected to [Remote Control](/docs/en/remote-control.md). To connect, you need a claude.ai sign-in and the other [Remote Control requirements](/docs/en/remote-control.md#requirements). See [Message sessions on other machines](/docs/en/cross-session-messaging.md#message-sessions-on-other-machines).

> [!NOTE]
>
> If you authenticate through an [LLM gateway](/docs/en/llm-gateway), feature availability matches the underlying provider the gateway forwards to, except for the features Claude Code itself turns off. Whenever `ANTHROPIC_BASE_URL` points at a host other than `api.anthropic.com`, Claude Code turns off features such as [Remote Control](/docs/en/remote-control.md#requirements) and [server-managed settings](/docs/en/server-managed-settings.md#platform-availability), whatever the gateway forwards. Some Anthropic-only features such as the [Advisor](/docs/en/advisor.md) work only if the gateway forwards requests intact to the Anthropic API.
>
> For how the requests Claude Code sends differ between an Amazon Bedrock- or Agent Platform-format gateway, an `ANTHROPIC_BASE_URL` gateway, and a Claude apps gateway sign-in, see [client behavior by connection method](/docs/en/llm-gateway-protocol.md#how-the-connection-method-changes-client-behavior).

### Summary by provider

Each tab lists what is unavailable or partially supported on that provider, with alternatives where one exists. Everything not listed works the same as on a Claude subscription, apart from the [provider-specific differences](#features-available-on-every-provider) noted above. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS, error reporting and telemetry to Anthropic are off by default. See [default behaviors by API provider](/docs/en/data-usage.md#default-behaviors-by-api-provider) for what traffic still reaches Anthropic and how to opt out.

**Amazon Bedrock**

**Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [web search](/docs/en/tools-reference.md#websearch-tool-behavior), [fast mode](/docs/en/fast-mode.md), [Advisor](/docs/en/advisor.md), [Channels](/docs/en/channels.md), the [analytics dashboard](/docs/en/analytics.md), [server-managed settings](/docs/en/server-managed-settings.md), and the [`/design-sync` and `/import` commands](/docs/en/commands#all-commands).

**Partial support:**

* [Desktop](/docs/en/desktop.md): only via [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
* [Auto mode](/docs/en/auto-mode-config.md): Sonnet 5 or later, Opus 4.7 or later, Haiku 5.5, and Fable models only
* [Cross-session messaging](/docs/en/cross-session-messaging.md): between your sessions on this machine only <sup>[5](#fn5)</sup>
* [Zero Data Retention](/docs/en/zero-data-retention.md): subject to your AWS agreement

**Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) instead of `/schedule`. For cloud sessions, use [GitHub Actions](/docs/en/github-actions.md) or [GitLab CI/CD](/docs/en/gitlab-ci-cd.md). For web lookups, use the [WebFetch tool](/docs/en/tools-reference.md#webfetch-tool-behavior) with a specific URL.

**Claude Platform on AWS**

**Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [fast mode](/docs/en/fast-mode.md), [Advisor](/docs/en/advisor.md), [Channels](/docs/en/channels.md), [GitHub Actions](/docs/en/github-actions.md), the [analytics dashboard](/docs/en/analytics.md), [server-managed settings](/docs/en/server-managed-settings.md), and the [`/design-sync` and `/import` commands](/docs/en/commands#all-commands).

**Available where Amazon Bedrock is not:** [web search](/docs/en/tools-reference.md#websearch-tool-behavior).

**Partial support:**

* [Cross-session messaging](/docs/en/cross-session-messaging.md): between your sessions on this machine only <sup>[5](#fn5)</sup>

**Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) instead of `/schedule`. For cloud sessions, use [GitLab CI/CD](/docs/en/gitlab-ci-cd.md).

**Google Cloud's Agent Platform**

**Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [fast mode](/docs/en/fast-mode.md), [Advisor](/docs/en/advisor.md), [Channels](/docs/en/channels.md), the [analytics dashboard](/docs/en/analytics.md), [server-managed settings](/docs/en/server-managed-settings.md), and the [`/design-sync` and `/import` commands](/docs/en/commands#all-commands).

**Partial support:**

* [Desktop](/docs/en/desktop.md): via [managed settings](https://claude.com/docs/third-party/claude-desktop/configuration) or [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
* [Web search](/docs/en/tools-reference.md#websearch-tool-behavior): Opus 4, Sonnet 4, Haiku 4.5, and later models
* [Auto mode](/docs/en/auto-mode-config.md): Sonnet 5 or later, Opus 4.7 or later, Haiku 5.5, and Fable models only
* [Cross-session messaging](/docs/en/cross-session-messaging.md): between your sessions on this machine only <sup>[5](#fn5)</sup>
* [Zero Data Retention](/docs/en/zero-data-retention.md): subject to your Google Cloud agreement

**Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) instead of `/schedule`. For cloud sessions, use [GitHub Actions](/docs/en/github-actions.md) or [GitLab CI/CD](/docs/en/gitlab-ci-cd.md).

**Microsoft Foundry**

**Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [fast mode](/docs/en/fast-mode.md), [Advisor](/docs/en/advisor.md), [Channels](/docs/en/channels.md), [GitLab CI/CD](/docs/en/gitlab-ci-cd.md), the [analytics dashboard](/docs/en/analytics.md), [server-managed settings](/docs/en/server-managed-settings.md), and the [`/design-sync` and `/import` commands](/docs/en/commands#all-commands).

**Partial support:**

* [Desktop](/docs/en/desktop.md): only via [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
* [Auto mode](/docs/en/auto-mode-config.md): Sonnet 5 or later, Opus 4.7 or later, Haiku 5.5, and Fable models only
* [Cross-session messaging](/docs/en/cross-session-messaging.md): between your sessions on this machine only <sup>[5](#fn5)</sup>
* [Zero Data Retention](/docs/en/zero-data-retention.md): subject to your Azure agreement

**Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) instead of `/schedule`. For cloud sessions, use [GitHub Actions](/docs/en/github-actions.md).

**Anthropic Console**

**Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription).

Everything in [CLI capabilities that vary by provider](#cli-capabilities-that-vary-by-provider) is available, except that [fast mode](/docs/en/fast-mode.md) requires [provisioned access](/docs/en/fast-mode.md#enable-fast-mode-for-your-organization). [Server-managed settings](/docs/en/server-managed-settings.md) that you configure in a claude.ai Team or Enterprise organization don't reach a session that authenticates with a Console API key. See [Platform availability](/docs/en/server-managed-settings.md#platform-availability) for how to cover those sessions.

**Partial support:**

* [Desktop](/docs/en/desktop.md): via [Claude Desktop on 3P with the Claude API](https://claude.com/docs/third-party/claude-desktop/claude-api)

## Availability by subscription plan

If you authenticate through Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or an Anthropic Console API key, this section does not apply to you. When you sign in with a claude.ai account, your plan determines which of the features below are available.

In Enterprise organizations with the [HIPAA configuration](/docs/en/hipaa-setup.md) applied, some features in this table are turned off.

| Feature | Pro | Max | Team | Enterprise |
| :- | :- | :- | :- | :- |
| [Cloud sessions](/docs/en/claude-code-on-the-web.md) | ✓ | ✓ | ✓ | ✓ <sup>[6](#fn6)</sup> |
| [Cloud scheduled tasks](/docs/en/routines.md) | ✓ | ✓ | ✓ | ✓ |
| [Remote Control](/docs/en/remote-control.md) | ✓ | ✓ | Admin-enabled | Admin-enabled |
| [Channels](/docs/en/channels.md) | ✓ | ✓ | Admin-enabled | Admin-enabled |
| [Computer use](/docs/en/computer-use.md) | ✓ | ✓ | ✗ | ✗ |
| Dispatch ([Desktop](/docs/en/desktop.md#sessions-from-dispatch)) | ✓ | ✓ | ✗ | ✗ |
| [Code Review](/docs/en/code-review.md) | ✗ | ✗ | ✓ | ✓ |
| [Artifacts](/docs/en/artifacts.md) | ✓ | ✓ | ✓ | ✓ |
| [Analytics dashboard and contribution metrics](/docs/en/analytics.md) | ✗ | ✗ | ✓ | ✓ |
| [Enterprise Analytics API](/docs/en/analytics.md#access-data-programmatically) | ✗ | ✗ | ✗ | ✓ |
| [Server-managed settings](/docs/en/server-managed-settings.md) | ✗ | ✗ | ✓ | ✓ |
| [SSO](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) | ✗ | ✗ | ✓ | ✓ |
| SCIM | ✗ | ✗ | ✗ | ✓ |
| [Compliance API](https://platform.claude.com/docs/en/api/compliance) | ✗ | ✗ | ✗ | ✓ |
| [Zero Data Retention](/docs/en/zero-data-retention.md) | ✗ | ✗ | ✗ | ✓ <sup>[7](#fn7)</sup> |

<sup>6</sup> On Enterprise, requires a premium seat or a Chat + Claude Code seat. See [Use Claude Code in the cloud](/docs/en/claude-code-on-the-web.md).\

<sup>7</sup> Not included in the standard Enterprise plan. Requires separate enablement by Anthropic for qualified accounts. See [Zero Data Retention](/docs/en/zero-data-retention.md).

For pricing and the full plan comparison, see [Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) and [Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

## Model availability

For which Claude models and context-window sizes are available per provider and region, see [Model configuration](/docs/en/model-config.md) and the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Vision, PDF input, and extended thinking are model capabilities rather than Claude Code features and work on every provider that offers the model. [Prompt caching](/docs/en/prompt-caching.md) works the same way on most providers; on Amazon Bedrock, support varies by model.

## Related resources

* [Enterprise deployment overview](/docs/en/third-party-integrations.md): compare authentication, billing, and regions across providers
* Provider setup guides: [Amazon Bedrock](/docs/en/amazon-bedrock.md), [Claude Platform on AWS](/docs/en/claude-platform-on-aws.md), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai.md), [Microsoft Foundry](/docs/en/microsoft-foundry.md)
* [Platforms and integrations](/docs/en/platforms.md): where Claude Code runs, including the CLI, Desktop, IDE extensions, web, mobile, and CI/CD
