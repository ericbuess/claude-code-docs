> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Other LLM gateways

> Route Claude Code through an LLM gateway your organization already runs. Covers connecting Claude Code to a gateway, rolling one out for your organization, and what Claude Code sends to a gateway.

This section covers using a gateway product your organization already runs, rather than [Claude apps gateway](/en/claude-apps-gateway). For what a gateway is, how it sits between Claude Code and your provider, and how to choose between Claude apps gateway and another product, see the [gateway overview](/en/gateways).

<Note>
  * If you're a developer connecting to an existing gateway: [connect Claude Code to your gateway](/en/llm-gateway-connect)
  * If you're an admin rolling out a gateway for your organization: [deploy and distribute a gateway](/en/llm-gateway-rollout)
  * If you're configuring a gateway product: the [gateway protocol reference](/en/llm-gateway-protocol)
</Note>

Any gateway that exposes a [supported API format](/en/llm-gateway-protocol#api-formats) works. Anthropic doesn't endorse, maintain, or audit third-party gateway products, and doesn't support routing Claude Code to non-Claude models through any gateway. Deploy the gateway following its own documentation, then complete the Claude Code side with the [rollout steps below](#roll-out-a-gateway).

## What a gateway provides

A gateway gives your organization one place to manage:

* **Credentials**: the provider key stays server-side; developers hold gateway credentials instead
* **Usage tracking**: attribute usage by developer or team, regardless of which provider serves the request
* **Cost controls**: enforce budgets and rate limits in one place
* **Audit logging**: log every model request for compliance
* **Provider switching**: change the provider in gateway configuration, without touching developer machines

All of these except provider switching apply whether the upstream is Anthropic's API or a [cloud provider](/en/third-party-integrations). Provider switching without reconfiguring developer machines also depends on the gateway exposing a single [Anthropic-format endpoint](/en/llm-gateway-protocol#api-formats) regardless of upstream; a gateway that exposes a provider's own format ties the client configuration to that provider.

The tradeoff is that the gateway becomes infrastructure your organization operates. Claude Code adds capabilities with each release, and a gateway that doesn't forward them breaks the corresponding features, so the gateway product needs to be kept updated as Claude Code evolves. The [gateway protocol reference](/en/llm-gateway-protocol) covers what to forward.

## Roll out a gateway

When you're ready to roll out an LLM gateway to your organization, the sequence is the same whichever gateway product you choose:

1. Deploy the gateway and give it your provider credential, so it can authenticate the requests it forwards.
2. Issue each developer a gateway credential, so usage is attributed to the developer and offboarding revokes one credential.
3. Distribute the configuration through a [managed settings file](/en/settings#settings-files) and your secrets tooling, so every machine receives the base URL and a credential. When both are distributed, developers don't configure anything. If you don't have settings distribution in place, developers follow the [connect page](/en/llm-gateway-connect) to set the variables themselves.
4. Have each developer [check for the configuration in Claude Code](/en/llm-gateway-connect#check-for-an-existing-configuration), so distribution problems surface before they depend on the gateway.

[Roll out an LLM gateway for your organization](/en/llm-gateway-rollout) walks each step and shows the configuration files to distribute at each one. The gateway is one part of organization setup; for policy enforcement, usage visibility, and data handling decisions, see [Set up Claude Code for your organization](/en/admin-setup).

## Subscriptions and gateways

While a [gateway credential variable](/en/llm-gateway-connect#set-the-credential-variable) or `apiKeyHelper` is active, a developer's claude.ai subscription isn't used: the credential replaces the subscription login for that session, and the subscription's usage limits don't apply. That traffic is billed per token to whoever owns the credential the gateway forwards, such as your organization's Anthropic Console account, or your Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry account when the gateway routes there.

[`ANTHROPIC_BASE_URL`](/en/llm-gateway-connect#set-the-base-url-and-credential) is the variable that points Claude Code at the gateway. Setting only that variable, without a gateway credential, doesn't replace the subscription. Requests still route through the gateway, but a saved claude.ai login remains the active credential, so its usage limits and billing apply. Gateways that pass this traffic on to Anthropic must forward the OAuth capability in `anthropic-beta`; see the [request headers reference](/en/llm-gateway-protocol#request-headers).

## Related pages

* [Gateway overview](/en/gateways): how a gateway works and how to choose between Claude apps gateway and another product
* [Claude apps gateway](/en/claude-apps-gateway): Anthropic's self-hosted gateway with SSO sign-in and OTLP telemetry
* [Connect Claude Code to an LLM gateway](/en/llm-gateway-connect): set the base URL and credential on your own machine, with per-surface configuration and a troubleshooting table
* [Roll out an LLM gateway for your organization](/en/llm-gateway-rollout): the admin checklist for deploying a gateway, issuing developer credentials, and distributing managed settings
* [Gateway protocol reference](/en/llm-gateway-protocol): what Claude Code sends to a gateway, for operators configuring one, covering endpoints, headers to forward, and feature pass-through
