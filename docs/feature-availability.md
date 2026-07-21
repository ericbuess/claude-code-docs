> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Feature availability

> Compare which Claude Code features are available across Anthropic subscription plans, the Anthropic Console, Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry.

The Claude Code CLI and everything that runs locally work on every provider. For setup instructions per provider, see the [Enterprise deployment overview](/docs/en/third-party-integrations). To skip straight to what is missing on your provider, see the [summary by provider](#summary-by-provider) tabs.

In the tables below, ✓ means available, ✗ means not available, and "See note" links to a footnote for partial support. A qualifier after ✓ narrows availability to that subset, and "Admin-enabled" means the feature is off until an organization admin turns it on.

## Availability by model provider

How you authenticate determines which features Claude Code can reach. For a single list of what is missing on your provider, see the [summary by provider](#summary-by-provider) tabs. To find your column in the tables:

* **Claude subscription**: you sign in with a claude.ai account on the Pro, Max, Team, or Enterprise plan
* **Anthropic Console**: you authenticate with an Anthropic API key
* **Amazon Bedrock**: you use Claude models from the Amazon Bedrock model catalog and set `CLAUDE_CODE_USE_BEDROCK`. The [Mantle endpoint](/docs/en/amazon-bedrock#use-the-mantle-endpoint) (`CLAUDE_CODE_USE_MANTLE`) is covered by this column
* **Claude Platform on AWS**: you bought Claude through AWS Marketplace but call the Anthropic API, and set `CLAUDE_CODE_USE_ANTHROPIC_AWS`
* **Google Cloud's Agent Platform**: Google-operated; you set `CLAUDE_CODE_USE_VERTEX`
* **Microsoft Foundry**: Anthropic-operated on Azure; you set `CLAUDE_CODE_USE_FOUNDRY`

### Features available on every provider

These work on every provider:

* [CLI](/docs/en/quickstart) and [Agent SDK](/docs/en/agent-sdk/overview)
* [VS Code](/docs/en/vs-code) and [JetBrains](/docs/en/jetbrains) extensions
* [Subagents](/docs/en/sub-agents), [hooks](/docs/en/hooks-guide), [commands](/docs/en/commands), and [skills](/docs/en/skills)
* [CLAUDE.md memory](/docs/en/memory), [plugins](/docs/en/plugins), and [MCP servers](/docs/en/mcp)
* [Checkpoints](/docs/en/checkpointing), [sandboxing](/docs/en/sandboxing), and [Workflows](/docs/en/workflows)
* [OpenTelemetry metrics](/docs/en/monitoring-usage) and the [managed settings file](/docs/en/settings#settings-files)

Three of these have provider-specific differences:

* **MCP servers**: [connectors from claude.ai](/docs/en/mcp#use-mcp-servers-from-claude-ai) load only when your claude.ai subscription is the active authentication method, and [tool search](/docs/en/mcp#configure-tool-search) is off by default on Google Cloud's Agent Platform and when `ANTHROPIC_BASE_URL` points to a non-first-party host
* **Subagents**: the built-in [Explore subagent](/docs/en/sub-agents#built-in-subagents) caps its inherited model at Opus on the Claude API, and inherits the main conversation's model directly on any other provider, including Claude Platform on AWS
* **[Commands](/docs/en/commands#all-commands)**: `/design-sync` and `/radio` are unavailable on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS, and `/voice` requires a claude.ai account

### Features that require a Claude subscription

These require signing in with a claude.ai account and are not reachable with an Anthropic Console API key or from a third-party provider:

* [Claude Code on the web](/docs/en/claude-code-on-the-web), Claude Code on mobile, and [Claude Code in Slack](/docs/en/slack)
* [Claude Code Desktop](/docs/en/desktop)
* [Routines](/docs/en/routines) (`/schedule`)
* [Ultraplan](/docs/en/ultraplan) and [Ultrareview](/docs/en/ultrareview)
* [Code Review](/docs/en/code-review): Team and Enterprise plans
* [Remote Control](/docs/en/remote-control)
* [Chrome extension](/docs/en/chrome)
* [Computer use](/docs/en/computer-use): Pro and Max plans
* [Artifacts](/docs/en/artifacts): Pro, Max, Team, and Enterprise plans
* [Voice dictation](/docs/en/voice-dictation)

Desktop is the partial exception: [gateway routing can be configured in the app or by an administrator](/docs/en/llm-gateway-connect#desktop-app), Enterprise deployments can route Desktop to Google Cloud's Agent Platform or a gateway provider via [managed settings](https://claude.com/docs/third-party/claude-desktop/configuration), and [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) runs the Code tab on Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or a self-hosted LLM gateway. For per-plan availability of these features, see [Availability by subscription plan](#availability-by-subscription-plan).

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
      <td>[Web search](/docs/en/tools-reference#websearch-tool-behavior)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
      <td>See note <sup><a href="#fn1">1</a></sup></td>
      <td>✓</td>
    </tr>

    <tr>
      <td>[Fast mode](/docs/en/fast-mode)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Auto mode](/docs/en/auto-mode-config)</td>
      <td>✓</td>
      <td>✓</td>
      <td>See note <sup><a href="#fn2">2</a></sup></td>
      <td>✓</td>
      <td>See note <sup><a href="#fn2">2</a></sup></td>
      <td>See note <sup><a href="#fn2">2</a></sup></td>
    </tr>

    <tr>
      <td>[Advisor](/docs/en/advisor)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Channels](/docs/en/channels)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[`/loop` scheduled tasks](/docs/en/scheduled-tasks)</td>
      <td>✓</td>
      <td>✓</td>
      <td>See note <sup><a href="#fn3">3</a></sup></td>
      <td>See note <sup><a href="#fn3">3</a></sup></td>
      <td>See note <sup><a href="#fn3">3</a></sup></td>
      <td>See note <sup><a href="#fn3">3</a></sup></td>
    </tr>

    <tr>
      <td>[GitHub Actions](/docs/en/github-actions) and [GitLab CI/CD](/docs/en/gitlab-ci-cd)</td>
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
      <td>[Analytics dashboard and API](/docs/en/analytics)</td>
      <td>✓ (dashboard: Team and Enterprise; API: Enterprise)</td>
      <td>✓ <sup><a href="#fn5">5</a></sup></td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Server-managed settings](/docs/en/server-managed-settings)</td>
      <td>✓ (Team and Enterprise)</td>
      <td>✓ (Team and Enterprise)</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Zero Data Retention](/docs/en/zero-data-retention)</td>
      <td>✓ (qualified Enterprise accounts)</td>
      <td>✓ (qualified accounts)</td>
      <td>See note <sup><a href="#fn4">4</a></sup></td>
      <td>✓ (qualified accounts)</td>
      <td>See note <sup><a href="#fn4">4</a></sup></td>
      <td>See note <sup><a href="#fn4">4</a></sup></td>
    </tr>
  </tbody>
</table>

<span id="fn1" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>1</sup> On Google Cloud's Agent Platform, web search is available for Claude 4 models and later.<br />
<span id="fn2" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>2</sup> On these providers, auto mode supports only Claude Sonnet 5, Opus 4.7, Opus 4.8, and Fable 5. See [Auto mode configuration](/docs/en/auto-mode-config). {/* min-version: 2.1.207 */}In v2.1.158 through v2.1.206, auto mode on these providers also required setting `CLAUDE_CODE_ENABLE_AUTO_MODE=1`; v2.1.207 removed the requirement.<br />
<span id="fn3" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>3</sup> Explicit intervals such as `/loop every 2 hours` work on every provider. On Amazon Bedrock, Claude Platform on AWS, Google Cloud's Agent Platform, and Microsoft Foundry, `/loop` cannot pick its own interval or supply the default maintenance prompt, so a prompt with no interval runs every 10 minutes, and `/loop` with no arguments shows the usage message. See [Scheduled tasks](/docs/en/scheduled-tasks).<br />
<span id="fn4" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>4</sup> Subject to your agreement with the cloud provider.<br />
<span id="fn5" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>5</sup> Dashboard and API only. [Contribution metrics](/docs/en/analytics#enable-contribution-metrics) requires a claude.ai Team or Enterprise organization.

<Note>
  If you authenticate through an [LLM gateway](/docs/en/llm-gateway), feature availability matches the underlying provider the gateway forwards to. Some Anthropic-only features such as the [Advisor](/docs/en/advisor) work only if the gateway forwards requests intact to the Anthropic API.
</Note>

### Summary by provider

Each tab lists what is unavailable or partially supported on that provider, with alternatives where one exists. Everything not listed works the same as on a Claude subscription, apart from the [provider-specific differences](#features-available-on-every-provider) noted above. On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and Claude Platform on AWS, error reporting and telemetry to Anthropic are off by default. See [default behaviors by API provider](/docs/en/data-usage#default-behaviors-by-api-provider) for what traffic still reaches Anthropic and how to opt out.

<Tabs>
  <Tab title="Amazon Bedrock">
    **Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [web search](/docs/en/tools-reference#websearch-tool-behavior), [fast mode](/docs/en/fast-mode), [Advisor](/docs/en/advisor), [Channels](/docs/en/channels), the [analytics dashboard](/docs/en/analytics), [server-managed settings](/docs/en/server-managed-settings), and the [`/design-sync` and `/radio` commands](/docs/en/commands#all-commands).

    **Partial support:**

    * [Desktop](/docs/en/desktop): only via [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
    * [Auto mode](/docs/en/auto-mode-config): Sonnet 5, Opus 4.7, Opus 4.8, and Fable 5 only
    * [`/loop`](/docs/en/scheduled-tasks): explicit intervals only
    * [Zero Data Retention](/docs/en/zero-data-retention): subject to your AWS agreement

    **Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) with an explicit interval instead of `/schedule`. For cloud sessions, use [GitHub Actions](/docs/en/github-actions) or [GitLab CI/CD](/docs/en/gitlab-ci-cd). For web lookups, use the [WebFetch tool](/docs/en/tools-reference#webfetch-tool-behavior) with a specific URL.
  </Tab>

  <Tab title="Claude Platform on AWS">
    **Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [fast mode](/docs/en/fast-mode), [Advisor](/docs/en/advisor), [Channels](/docs/en/channels), the [analytics dashboard](/docs/en/analytics), [server-managed settings](/docs/en/server-managed-settings), and the [`/design-sync` and `/radio` commands](/docs/en/commands#all-commands).

    **Available where Amazon Bedrock is not:** [web search](/docs/en/tools-reference#websearch-tool-behavior).

    **Partial support:**

    * [`/loop`](/docs/en/scheduled-tasks): explicit intervals only

    **Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) with an explicit interval instead of `/schedule`. For cloud sessions, use [GitHub Actions](/docs/en/github-actions) or [GitLab CI/CD](/docs/en/gitlab-ci-cd).
  </Tab>

  <Tab title="Google Cloud's Agent Platform">
    **Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [fast mode](/docs/en/fast-mode), [Advisor](/docs/en/advisor), [Channels](/docs/en/channels), the [analytics dashboard](/docs/en/analytics), [server-managed settings](/docs/en/server-managed-settings), and the [`/design-sync` and `/radio` commands](/docs/en/commands#all-commands).

    **Partial support:**

    * [Desktop](/docs/en/desktop): via [managed settings](https://claude.com/docs/third-party/claude-desktop/configuration) or [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
    * [Web search](/docs/en/tools-reference#websearch-tool-behavior): Claude 4 models and later
    * [Auto mode](/docs/en/auto-mode-config): Sonnet 5, Opus 4.7, Opus 4.8, and Fable 5 only
    * [`/loop`](/docs/en/scheduled-tasks): explicit intervals only
    * [Zero Data Retention](/docs/en/zero-data-retention): subject to your Google Cloud agreement

    **Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) with an explicit interval instead of `/schedule`. For cloud sessions, use [GitHub Actions](/docs/en/github-actions) or [GitLab CI/CD](/docs/en/gitlab-ci-cd).
  </Tab>

  <Tab title="Microsoft Foundry">
    **Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription), plus [fast mode](/docs/en/fast-mode), [Advisor](/docs/en/advisor), [Channels](/docs/en/channels), [GitHub Actions](/docs/en/github-actions) and [GitLab CI/CD](/docs/en/gitlab-ci-cd), the [analytics dashboard](/docs/en/analytics), [server-managed settings](/docs/en/server-managed-settings), and the [`/design-sync` and `/radio` commands](/docs/en/commands#all-commands).

    **Partial support:**

    * [Desktop](/docs/en/desktop): only via [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
    * [Auto mode](/docs/en/auto-mode-config): Sonnet 5, Opus 4.7, Opus 4.8, and Fable 5 only
    * [`/loop`](/docs/en/scheduled-tasks): explicit intervals only
    * [Zero Data Retention](/docs/en/zero-data-retention): subject to your Azure agreement

    **Alternatives:** for scheduling, use [`/loop`](/docs/en/scheduled-tasks) with an explicit interval instead of `/schedule`.
  </Tab>

  <Tab title="Anthropic Console">
    **Not available:** all [features that require a Claude subscription](#features-that-require-a-claude-subscription).

    Everything in [CLI capabilities that vary by provider](#cli-capabilities-that-vary-by-provider) is available, as are [server-managed settings](/docs/en/server-managed-settings) when the API key belongs to a Team or Enterprise organization.
  </Tab>
</Tabs>

## Availability by subscription plan

If you authenticate through Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or an Anthropic Console API key, this section does not apply to you. When you sign in with a claude.ai account, your plan determines which of the features below are available.

| Feature                                                                     | Pro | Max | Team          | Enterprise                        |
| :-------------------------------------------------------------------------- | :-- | :-- | :------------ | :-------------------------------- |
| [Claude Code on the web](/docs/en/claude-code-on-the-web)                        | ✓   | ✓   | ✓             | ✓ <sup><a href="#fn6">6</a></sup> |
| [Routines](/docs/en/routines)                                                    | ✓   | ✓   | ✓             | ✓                                 |
| [Remote Control](/docs/en/remote-control)                                        | ✓   | ✓   | Admin-enabled | Admin-enabled                     |
| [Channels](/docs/en/channels)                                                    | ✓   | ✓   | Admin-enabled | Admin-enabled                     |
| [Computer use](/docs/en/computer-use)                                            | ✓   | ✓   | ✗             | ✗                                 |
| Dispatch ([Desktop](/docs/en/desktop#sessions-from-dispatch))                    | ✓   | ✓   | ✗             | ✗                                 |
| [Code Review](/docs/en/code-review)                                              | ✗   | ✗   | ✓             | ✓                                 |
| [Artifacts](/docs/en/artifacts)                                                  | ✓   | ✓   | ✓             | Admin-enabled                     |
| [Analytics dashboard and contribution metrics](/docs/en/analytics)               | ✗   | ✗   | ✓             | ✓                                 |
| [Enterprise Analytics API](/docs/en/analytics#access-data-programmatically)      | ✗   | ✗   | ✗             | ✓                                 |
| [Server-managed settings](/docs/en/server-managed-settings)                      | ✗   | ✗   | ✓             | ✓                                 |
| [SSO](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) | ✗   | ✗   | ✓             | ✓                                 |
| SCIM                                                                        | ✗   | ✗   | ✗             | ✓                                 |
| [Compliance API](https://platform.claude.com/docs/en/api/compliance)        | ✗   | ✗   | ✗             | ✓                                 |
| [Zero Data Retention](/docs/en/zero-data-retention)                              | ✗   | ✗   | ✗             | ✓ <sup><a href="#fn7">7</a></sup> |

<span id="fn6" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>6</sup> On Enterprise, requires a premium seat or a Chat + Claude Code seat. See [Claude Code on the web](/docs/en/claude-code-on-the-web).<br />
<span id="fn7" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>7</sup> Not included in the standard Enterprise plan. Requires separate enablement by Anthropic for qualified accounts. See [Zero Data Retention](/docs/en/zero-data-retention).

For pricing and the full plan comparison, see [Team plans](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) and [Enterprise plans](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

## Model availability

For which Claude models and context-window sizes are available per provider and region, see [Model configuration](/docs/en/model-config) and the [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). Vision, PDF input, and extended thinking are model capabilities rather than Claude Code features and work on every provider that offers the model. [Prompt caching](/docs/en/prompt-caching) works the same way on most providers; on Amazon Bedrock, support varies by model.

## Related resources

* [Enterprise deployment overview](/docs/en/third-party-integrations): compare authentication, billing, and regions across providers
* Provider setup guides: [Amazon Bedrock](/docs/en/amazon-bedrock), [Claude Platform on AWS](/docs/en/claude-platform-on-aws), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), [Microsoft Foundry](/docs/en/microsoft-foundry)
* [Platforms and integrations](/docs/en/platforms): where Claude Code runs, including the CLI, Desktop, IDE extensions, web, mobile, and CI/CD
