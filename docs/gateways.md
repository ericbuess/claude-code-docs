> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Run Claude Code through a gateway

> Route Claude Code through a self-hosted gateway for centralized credentials, usage tracking, and cost controls. Covers the architecture, Anthropic's Claude apps gateway, and using other gateway products.

A gateway is a proxy your organization runs between Claude Code and a model provider. Claude Code sends API traffic to the gateway instead of directly to the provider, and the gateway forwards it using a credential your organization holds. Developers authenticate to the gateway rather than holding provider credentials, so authentication, usage tracking, budgets, and audit logging happen in one place you control.

Claude Code includes a self-hosted gateway, [Claude apps gateway](/en/claude-apps-gateway), in the `claude` binary, so you don't have to adopt a separate gateway product to run one. If your organization already runs an [LLM gateway](/en/llm-gateway), Claude Code works with that too.

This page covers:

* [How a gateway sits between Claude Code and your provider](#how-a-gateway-works)
* [Choosing between Claude apps gateway and a gateway you already run](#choose-a-gateway)
* [How gateways interact with claude.ai subscriptions](#subscriptions-and-gateways)
* [What's configured separately from the gateway](#configure-separately-from-the-gateway)

## How a gateway works

Each developer's Claude Code is pointed at the gateway's address and authenticates with a gateway-issued credential.

The gateway authenticates the developer, applies whatever access and budget rules you configure, and forwards the request to your provider with the organization's credential. The provider can be Anthropic's API or a [cloud provider](/en/third-party-integrations) such as Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry; the gateway's configuration decides. With Claude apps gateway, or another gateway that exposes a single Anthropic-format endpoint, changing provider doesn't require touching developer machines.

<Frame>
  <img src="https://mintcdn.com/claude-code/-uq-4JE0W_JO5Er5/images/llm-gateway-flow.svg?fit=max&auto=format&n=-uq-4JE0W_JO5Er5&q=85&s=1c1a8dcc0cfcc3a58652cc8e28cd3e20" alt="Diagram showing Claude Code routing through a gateway. In a developer machines zone, the Claude Code CLI and VS Code extension send requests to the gateway address with a per-developer credential. In a zone labeled your infrastructure, the gateway handles authentication, usage tracking, budgets, and routing, and forwards requests with your organization's credential. In a model providers zone, a solid arrow leads to the provider you configure, shown as the Anthropic API, and dashed arrows lead to other provider options, illustrated with Amazon Bedrock, Google Cloud, and Microsoft Foundry as examples." width="780" height="322" data-path="images/llm-gateway-flow.svg" />
</Frame>

Two kinds of credential are involved:

* **Developer credential**: each developer holds their own, issued by the gateway. It authenticates them to the gateway and identifies them in usage tracking
* **Provider credential**: the gateway holds one credential for your provider account, shared by all forwarded traffic

## Choose a gateway

Claude Code works with Anthropic's own gateway or with a gateway your organization already runs.

### Claude apps gateway

Claude apps gateway is Anthropic's self-hosted gateway, included in the `claude` binary. It routes to Amazon Bedrock, Google Cloud, Microsoft Foundry, or the Anthropic API as the upstream. Developers sign in with your corporate identity provider through `/login`, the gateway enforces model access and [managed settings](/en/permissions#managed-settings) by IdP group, and it emits [OpenTelemetry Protocol (OTLP)](/en/monitoring-usage) usage metrics to your own observability stack.

Because it is built and tested alongside each Claude Code release, it forwards the headers and request fields Claude Code sends. A gateway maintained separately needs its [forwarding rules updated](/en/llm-gateway-protocol#forward-as-open-lists) as those headers and fields change with each release; Claude apps gateway releases with the CLI, so there is no list to keep current. See [Availability and limitations](/en/claude-apps-gateway#availability-and-limitations) for the small set of features that behave differently on a gateway session.

The gateway sign-in is a browser SSO step, and there is no service-token flow, so a CI pipeline with no developer to approve the sign-in can't authenticate through it; configure those against your provider directly. Agent SDK sessions and `claude -p` runs on a machine where a developer has signed in use that machine's gateway session and are governed by its policies. See [CI pipelines and remote machines](/en/claude-apps-gateway#ci-pipelines-and-remote-machines).

See [Claude apps gateway](/en/claude-apps-gateway) to deploy it.

### Other gateways

If your organization already runs an LLM gateway or API gateway, you can use it instead. Anthropic doesn't endorse, maintain, or audit other gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway. See [Other LLM gateways](/en/llm-gateway) for the admin rollout checklist, what a gateway must implement, and how to point Claude Code at it.

## Subscriptions and gateways

When developers connect through a gateway with a gateway credential, usage is billed to your organization's provider account at API rates, and their claude.ai subscriptions aren't used or charged. Setting [`ANTHROPIC_AUTH_TOKEN`](/en/env-vars) for a gateway you run, or signing in to a Claude apps gateway with `/login`, turns off subscription login for that session. Every request forwarded under that credential is charged to the account behind the gateway's provider credential.

The exception is setting only `ANTHROPIC_BASE_URL`, with no gateway credential. Requests still route through the gateway, but a saved claude.ai login stays the active credential, so the subscription's usage limits and billing apply. [Other LLM gateways](/en/llm-gateway#subscriptions-and-gateways) covers that configuration and what the gateway has to forward for it to work.

## Configure separately from the gateway

A gateway routes model API requests. A few things you might expect it to handle are configured elsewhere:

* **Which model answers**: pick the model with the `/model` command or [model environment variables](/en/model-config#setting-your-model). The gateway decides where requests go, not which model the developer selects. Claude apps gateway can bound the choice with a per-group `availableModels` allowlist, but the developer still picks within it.
* **Other network traffic**: Claude Code itself sends version checks and downloads directly to Anthropic, separate from the gateway path. Whether the optional client telemetry stream is also on depends on your provider; the [telemetry defaults table](/en/data-usage#telemetry-services) covers each case. On a signed-in Claude apps gateway session, the gateway credential disables the Anthropic-bound analytics and, when [telemetry forwarding](/en/claude-apps-gateway-config#telemetry) is configured, pins OTLP export to the gateway. Your network still needs egress to the [required domains](/en/network-config), or set [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/en/env-vars) to turn off the optional streams.
* **Corporate HTTP proxies**: an `HTTPS_PROXY` sits between Claude Code and every server it talks to, including the gateway. If your network requires one, [configure the proxy](/en/network-config) in addition to the gateway. For Claude apps gateway specifically, [sign-in checks that the proxy host is also on a private network](/en/claude-apps-gateway#prerequisites); if it isn't, add the gateway host to `NO_PROXY` so the CLI connects to it directly.

## Next steps

The next page depends on who runs the gateway. Anthropic's gateway runs from the `claude` binary and has its own setup guide; a gateway your organization already runs has a protocol to implement and an admin rollout checklist.

* [Claude apps gateway](/en/claude-apps-gateway) to deploy Anthropic's self-hosted gateway with SSO sign-in and OTLP telemetry
* [Other LLM gateways](/en/llm-gateway) for what a gateway your organization already runs must implement, and how to point Claude Code at it
* [Set up Claude Code for your organization](/en/admin-setup) for the wider rollout decisions a gateway is one part of
