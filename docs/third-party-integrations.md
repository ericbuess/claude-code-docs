> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Enterprise deployment overview

> Learn how Claude Code can integrate with various third-party services and infrastructure to meet enterprise deployment requirements.

Organizations can deploy Claude Code through Anthropic directly or through a cloud provider. This page helps you choose the right configuration.

**Deploying Claude Code across your organization?** Talk to sales about enterprise plans, SSO, and centralized billing.

View plans
Contact sales

## Compare deployment options

For most organizations, Claude for Teams or Claude for Enterprise provides the best experience. Team members get access to both Claude Code and Claude on the web with a single subscription, centralized billing, and no infrastructure setup required.

**Claude for Teams** is self-service and includes collaboration features, admin tools, SSO, billing management, and [server-managed settings](/docs/en/server-managed-settings.md) for organization-wide Claude Code configuration. Best for smaller teams that need to get started quickly.

**Claude for Enterprise** adds domain capture, role-based permissions, and compliance API access. Best for larger organizations with security and compliance requirements.

Learn more about [Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) and [Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

The deployment options compared below cover where model inference runs. To run Claude Code [cloud sessions](/docs/en/claude-code-on-the-web.md) on compute your organization operates, see [self-hosted environments](/docs/en/self-hosted-environments).

If your organization has specific infrastructure requirements, compare the options below:

<table>
  <thead>
    <tr>
      <th>Feature</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform, formerly Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Best for</td>
      <td>Most organizations (recommended)</td>
      <td>Individual developers</td>
      <td>AWS-native deployments</td>
      <td>AWS Marketplace billing with Claude API features</td>
      <td>GCP-native deployments</td>
      <td>Azure-native deployments</td>
    </tr>

    <tr>
      <td>Billing</td>
      <td>**Teams:** per-seat subscription with PAYG available, see [pricing](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=third_party_pricing#team-&-enterprise)\
      **Enterprise:** [Contact Sales](https://claude.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=third_party_enterprise)</td>
      <td>PAYG</td>
      <td>PAYG through AWS</td>
      <td>PAYG through AWS Marketplace</td>
      <td>PAYG through GCP</td>
      <td>PAYG through Azure</td>
    </tr>

    <tr>
      <td>Regions</td>
      <td>Supported [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Supported [countries](https://www.anthropic.com/supported-countries)</td>
      <td>Multiple AWS [regions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Multiple AWS regions</td>
      <td>Multiple GCP [regions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Multiple Azure [regions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
      <td>Enabled by default</td>
    </tr>

    <tr>
      <td>Authentication</td>
      <td>claude.ai SSO or email</td>
      <td>API key or a [Console sign-in without one](/docs/en/authentication.md#sign-in-without-an-api-key)</td>
      <td>API key or AWS credentials</td>
      <td>API key or AWS credentials</td>
      <td>GCP credentials</td>
      <td>API key or Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Cost tracking</td>
      <td>Usage dashboard</td>
      <td>Usage dashboard</td>
      <td>AWS Cost Explorer</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Includes Claude on web</td>
      <td>Yes</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
    </tr>

    <tr>
      <td>Enterprise features</td>
      <td>Team management, SSO, usage monitoring</td>
      <td>None</td>
      <td>IAM policies, CloudTrail</td>
      <td>IAM policies, CloudTrail</td>
      <td>IAM roles, Cloud Audit Logs</td>
      <td>RBAC policies, Azure Monitor</td>
    </tr>
  </tbody>
</table>

For a feature-by-feature breakdown of what's available on each option, see [Feature availability](/docs/en/feature-availability.md).

Select a deployment option to view setup instructions:

* [Claude for Teams or Enterprise](/docs/en/authentication.md#claude-for-teams-or-enterprise)
* [Anthropic Console](/docs/en/authentication.md#claude-console-authentication)
* [Claude apps gateway](/docs/en/claude-apps-gateway), a self-hosted gateway that adds IdP sign-in in front of Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, Microsoft Foundry, or the Anthropic API
* [Amazon Bedrock](/docs/en/amazon-bedrock.md)
* [Claude Platform on AWS](/docs/en/claude-platform-on-aws.md)
* [Google Cloud's Agent Platform](/docs/en/google-vertex-ai.md)
* [Microsoft Foundry](/docs/en/microsoft-foundry.md)

For Amazon Bedrock and Google Vertex AI, you can also run `claude` and select **3rd-party platform** at the login prompt to launch an interactive setup wizard.

## Configure proxies and gateways

Most organizations can use a cloud provider directly without additional configuration. However, you may need to configure a corporate proxy or LLM gateway if your organization has specific network or management requirements. These are different configurations that can be used together:

* **Corporate proxy**: Routes traffic through an HTTP/HTTPS proxy. Use this if your organization requires all outbound traffic to pass through a proxy server for security monitoring, compliance, or network policy enforcement. Configure with the `HTTPS_PROXY` or `HTTP_PROXY` environment variables. Learn more in [Enterprise network configuration](/docs/en/network-config.md).
* **LLM Gateway**: A service that sits between Claude Code and the cloud provider to handle authentication and routing. Use this if you need centralized usage tracking across teams, custom rate limiting or budgets, or centralized authentication management. Configure with the `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL`, `ANTHROPIC_AWS_BASE_URL`, `ANTHROPIC_VERTEX_BASE_URL`, or `ANTHROPIC_FOUNDRY_BASE_URL` environment variables. Learn more in [LLM gateways](/docs/en/llm-gateway).

For the per-provider environment variables that route Amazon Bedrock, Microsoft Foundry, or Google Cloud's Agent Platform through an LLM gateway, see [route to a cloud provider through a gateway](/docs/en/llm-gateway-connect.md#route-to-a-cloud-provider-through-a-gateway). Run `/status` in Claude Code to verify which provider, base URL, and proxy a session is using.

If your organization uses [customer-managed encryption keys](https://platform.claude.com/docs/en/manage-claude/cmek) (CMEK) and routes Claude Code through an LLM gateway or a custom `ANTHROPIC_BASE_URL`, CMEK doesn't apply to Claude Code's operational telemetry on those sessions. To turn telemetry off for every developer, deliver `DISABLE_TELEMETRY` through managed settings as shown in [Turn telemetry off for your organization](/docs/en/managed-settings.md#turn-telemetry-off-for-your-organization).

## Best practices for organizations

### Invest in documentation and memory

Invest in documentation so that Claude Code understands your codebase. Organizations can deploy CLAUDE.md files at multiple levels. See [where CLAUDE.md files can live](/docs/en/memory.md#choose-where-to-put-claude-md-files) and [how to deploy an organization-wide CLAUDE.md](/docs/en/memory.md#deploy-organization-wide-claude-md).

### Simplify deployment

If you have a custom development environment, creating a "one click" way to install Claude Code is key to growing adoption across an organization.

### Start with guided usage

Encourage new users to try Claude Code for codebase Q\&A, or on smaller bug fixes or feature requests. Ask Claude Code to make a plan. Check Claude's suggestions and give feedback if it's off-track. Over time, as users understand this new paradigm better, then they'll be more effective at letting Claude Code run more agentically.

### Pin model versions for cloud providers

If you deploy through [Amazon Bedrock](/docs/en/amazon-bedrock.md), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai.md), [Microsoft Foundry](/docs/en/microsoft-foundry.md), or [Claude Platform on AWS](/docs/en/claude-platform-on-aws.md), pin specific model versions using `ANTHROPIC_DEFAULT_FABLE_MODEL`, `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL`, and `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Without pinning, model aliases resolve to Claude Code's built-in default for that provider, which can lag the newest release and may not yet be enabled in your account. Pinning lets you control when your users move to a new model. See [Model configuration](/docs/en/model-config.md#pin-models-for-third-party-deployments) for what each provider does when the default is unavailable.

### Configure security policies

Security teams can configure managed permissions for what Claude Code is and is not allowed to do, which cannot be overwritten by local configuration. [Learn more](/docs/en/security.md).

To limit which of these deployment options a managed machine may use, set [`allowedProviders`](/docs/en/settings-reference#allowedproviders) in managed settings. For example, `["bedrock"]` allows Amazon Bedrock and nothing else; a Bedrock fleet that also enables the Mantle endpoint lists `"mantle"` too. The entry says which endpoint variables also need a managed `env` pin. Requires Claude Code v2.1.285 or later.

### Use MCP for integrations

MCP is a great way to give Claude Code more information, such as connecting to ticket management systems or error logs. Have one central team configure MCP servers and check a `.mcp.json` configuration into the codebase so that all users benefit. [Learn more](/docs/en/mcp.md).

## Next steps

Once you've chosen a deployment option and configured access for your team:

1. **Roll out to your team**: Share installation instructions and have team members [install Claude Code](/docs/en/setup.md) and authenticate with their credentials.
2. **Set up shared configuration**: Create a [CLAUDE.md file](/docs/en/memory.md) in your repositories to help Claude Code understand your codebase and coding standards.
3. **Configure permissions**: Review [security settings](/docs/en/security.md) to define what Claude Code can and cannot do in your environment.
