---
title: Usage and Cost API
url: https://platform.claude.com/docs/en/manage-claude/usage-cost-api
description: Programmatically access your organization's API usage and cost data with the Usage & Cost Admin API.
---

<Tip>
  **The Admin API is unavailable for individual accounts.** To collaborate with teammates and add members, set up your organization in **Console → Settings → Organization**.
</Tip>

The Usage & Cost Admin API provides programmatic and granular access to historical API usage and cost data for your organization. This data is similar to the information available in the [Usage](https://platform.claude.com/usage) and [Cost](https://platform.claude.com/cost) pages of the Claude Console.

This API enables you to better monitor, analyze, and optimize your Claude implementations:

* **Accurate usage tracking:** Get precise token counts and usage patterns instead of relying solely on response token counting
* **Cost reconciliation:** Match internal records with Anthropic billing for finance and accounting teams
* **Product performance and improvement:** Monitor product performance while measuring if changes to the system have improved it, or set up alerting
* **[Rate limit](https://platform.claude.com/docs/en/api/rate-limits) optimization:** Optimize features like [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) or specific prompts to make the most of your allocated capacity.
* **Advanced analysis:** Perform deeper data analysis than what's available in Console

<Check>
  **Admin API key required.** These endpoints require an Admin API key, which is different from a standard Claude API key. See [Create an Admin API key](https://platform.claude.com/docs/en/manage-claude/admin-api-keys) to find where to create one for your organization type and which scopes to select.
</Check>

Claude Enterprise organizations use an Analytics API key with a different API instead; see [Which API do you need?](https://platform.claude.com/docs/en/manage-claude/usage-cost-api#which-api-do-you-need).

<Note>
  **Claude Platform on AWS:** The programmatic Usage and Cost API endpoints are not currently available. View usage and cost data on the **Usage** and **Cost** pages in the Claude Console instead.
</Note>

## Which API do you need?

Anthropic provides cost and usage reporting through two APIs, depending on which Claude product your organization manages:

| Your organization                | API                                                                                                                     | Key type                             |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ------------------------------------ |
| Claude Console (Claude Platform) | The Usage and Cost Admin API described on this page                                                                     | Admin API key (`sk-ant-admin01-...`) |
| Claude Enterprise (claude.ai)    | The [Claude Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics) cost and usage endpoints | Analytics API key                    |

Claude Enterprise parent organizations do not appear in Claude Console and carry no Admin API keys, so for them the Analytics API key is the only path to this data. See [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api) for how to create each key type and which plans the Claude Enterprise cost data applies to.

## Partner solutions

Leading observability platforms offer ready-to-use integrations for monitoring your Claude API usage and cost, without writing custom code. These integrations provide dashboards, alerting, and analytics to help you manage your API usage effectively.

<CardGroup cols={3}>
  <Card title="CloudZero" icon="chart" href="https://docs.cloudzero.com/docs/connections-anthropic">
    Cloud intelligence platform for tracking and forecasting costs
  </Card>

  <Card title="Datadog" icon="chart" href="https://docs.datadoghq.com/integrations/anthropic/">
    LLM Observability with automatic tracing and monitoring
  </Card>

  <Card title="Grafana Cloud" icon="chart" href="https://grafana.com/docs/grafana-cloud/monitor-infrastructure/integrations/integration-reference/integration-anthropic/">
    Agentless integration for easy LLM observability with out-of-the-box dashboards and alerts
  </Card>

  <Card title="Honeycomb" icon="polygon" href="https://docs.honeycomb.io/integrations/anthropic-usage-monitoring/">
    Advanced querying and visualization through OpenTelemetry
  </Card>

  <Card title="Vantage" icon="chart" href="https://docs.vantage.sh/connecting_anthropic">
    FinOps platform for LLM cost & usage observability
  </Card>
</CardGroup>

## Quick start

Get your organization's daily usage for the last 7 days:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-08T00:00:00Z&\
ending_at=2025-01-15T00:00:00Z&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Tip>
  **Set a User-Agent header for integrations**

  If you're building an integration, set your User-Agent header to help Anthropic understand usage patterns:

  ```text wrap
  User-Agent: YourApp/1.0.0 (https://yourapp.com)
  ```
</Tip>

## Usage API

Track token consumption across your organization with detailed breakdowns by model, workspace, and service tier with the `/v1/organizations/usage_report/messages` endpoint.

### Key concepts

* **Time buckets:** Aggregate usage data in fixed intervals (`1m`, `1h`, or `1d`)
* **Token tracking:** Measure uncached input, cached input, cache creation, and output tokens
* **Filtering & grouping:** Filter by API key, workspace, model, service tier, context window, [data residency](https://platform.claude.com/docs/en/manage-claude/data-residency), or speed (beta), and group results by these dimensions
* **Server tool usage:** Track usage of server-side tools such as web search

For complete parameter details and response schemas, see the [Usage API reference](https://platform.claude.com/docs/en/api/admin-api/usage-cost/get-messages-usage-report).

### Basic examples

#### Daily usage by model

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

#### Hourly usage with filtering

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-15T00:00:00Z&\
ending_at=2025-01-15T23:59:59Z&\
models[]=claude-opus-5&\
service_tiers[]=batch&\
context_window[]=0-200k&\
bucket_width=1h" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

#### Filter usage by API keys and workspaces

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
api_key_ids[]=apikey_01Rj2N8SVvo6BePZj99NhmiT&\
api_key_ids[]=apikey_01ABC123DEF456GHI789JKL&\
workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
workspace_ids[]=wrkspc_01XYZ789ABC123DEF456MNO&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Tip>
  To retrieve your organization's API key IDs, use the [List API Keys](https://platform.claude.com/docs/en/api/admin-api/apikeys/list-api-keys) endpoint.

  To retrieve your organization's workspace IDs, use the [List Workspaces](https://platform.claude.com/docs/en/api/admin-api/workspaces/list-workspaces) endpoint, or find your organization's workspace IDs in the Claude Console.
</Tip>

#### Data residency

Track your [data residency controls](https://platform.claude.com/docs/en/manage-claude/data-residency) by grouping and filtering usage with the `inference_geo` dimension. This is useful for verifying geographic routing across your organization.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
group_by[]=inference_geo&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

You can also filter to a specific geo. Valid values are `global`, `us`, and `not_available`:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
inference_geos[]=us&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Note>
  Models released before February 2026 (prior to Claude Opus 4.6 and Claude Sonnet 4.6) don't support the `inference_geo` request parameter, so their usage reports return `"not_available"` for this dimension. You can use `not_available` as a filter value in `inference_geos[]` to target those models.
</Note>

#### Fast mode (research preview)

Track [fast mode](https://platform.claude.com/docs/en/build-with-claude/fast-mode) usage by grouping and filtering with the `speed` dimension. This is useful for monitoring standard versus fast mode usage.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
group_by[]=speed&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: fast-mode-2026-02-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

You can also filter to a specific speed. Valid values are `standard` and `fast`:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2026-02-01T00:00:00Z&\
ending_at=2026-02-08T00:00:00Z&\
speeds[]=fast&\
group_by[]=model&\
bucket_width=1d" \
  -H "anthropic-version: 2023-06-01" \
  -H "anthropic-beta: fast-mode-2026-02-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

<Note>
  Both the `speeds[]` filter and the `speed` group\_by value require the `fast-mode-2026-02-01` beta header.
</Note>

### Time granularity limits

| Granularity | Default limit | Maximum limit | Use case               |
| ----------- | ------------- | ------------- | ---------------------- |
| `1m`        | 60 buckets    | 1,440 buckets | Real-time monitoring   |
| `1h`        | 24 buckets    | 168 buckets   | Daily patterns         |
| `1d`        | 7 buckets     | 31 buckets    | Weekly/monthly reports |

## Cost API

Retrieve service-level cost breakdowns in USD with the `/v1/organizations/cost_report` endpoint.

### Key concepts

* **Currency:** All costs in USD, reported as decimal strings in lowest units (cents)
* **Cost types:** Track token usage, web search, and code execution costs
* **Grouping:** Group costs by workspace or description for detailed breakdowns. When grouping by `description`, responses include parsed fields such as `model` and `inference_geo`
* **Time buckets:** Daily granularity only (`1d`)

For complete parameter details and response schemas, see the [Cost API reference](https://platform.claude.com/docs/en/api/admin-api/usage-cost/get-cost-report).

<Warning>
  Priority Tier costs use a different billing model and are not included in the cost endpoint. Track Priority Tier usage through the usage endpoint instead.
</Warning>

### Basic example

```bash cURL
curl "https://api.anthropic.com/v1/organizations/cost_report?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
group_by[]=workspace_id&\
group_by[]=description" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Pagination

Both endpoints support pagination for large datasets:

1. Make your initial request.
2. If `has_more` is `true`, use the `next_page` value in your next request.
3. Continue until `has_more` is `false`.

```bash cURL
# First request
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
limit=7" \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Response includes: "has_more": true, "next_page": "page_xyz..."

# Next request with pagination
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-31T00:00:00Z&\
limit=7&\
page=page_xyz..." \
  -H "anthropic-version: 2023-06-01" \
  -H "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Common use cases

Explore detailed implementations in [Claude Cookbook](https://platform.claude.com/cookbook):

* **Daily usage reports:** Track token consumption trends
* **Cost attribution:** Allocate expenses by workspace for chargebacks
* **Cache efficiency:** Measure and optimize prompt caching
* **Budget monitoring:** Set up alerts for spending thresholds
* **CSV export:** Generate reports for finance teams

## Frequently asked questions

### How fresh is the data?

Usage and cost data typically appears within 5 minutes of API request completion, though delays may occasionally be longer.

### What's the recommended polling frequency?

The API supports polling once per minute for sustained use. For short bursts (for example, downloading paginated data), more frequent polling is acceptable. Cache results for dashboards that need frequent updates.

### How do I track code execution usage?

Code execution costs appear in the cost endpoint grouped under `Code Execution Usage` in the description field. Code execution is not included in the usage endpoint.

### How do I track Priority Tier usage?

Filter or group by `service_tier` in the usage endpoint and look for the `priority` value. Priority Tier costs are not available in the cost endpoint.

### What happens with Playground usage?

API usage from Playground in the Claude Console (and from the legacy Workbench before it) is not associated with an API key, so `api_key_id` will be `null` even when grouping by that dimension.

### How is the default workspace represented?

Usage and costs attributed to the default workspace have a `null` value for `workspace_id`.

### How do I get per-user cost breakdowns for Claude Code?

Use the [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api), which provides per-user estimated costs and productivity metrics without the performance limitations of breaking down costs by many API keys. For general API usage with many keys, use the [Usage API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api#usage-api) to track token consumption as a cost proxy.

## See also

Use the Usage and Cost APIs to deliver a better experience for your users, manage costs, and preserve your rate limit. Learn more about some of these other features:

* [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api)
* [Admin API reference](https://platform.claude.com/docs/en/api/admin)
* [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api) - Which analytics API and key type your organization needs
* [Pricing](https://platform.claude.com/docs/en/about-claude/pricing)
* [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) - Optimize costs with caching
* [Batch processing](https://platform.claude.com/docs/en/build-with-claude/batch-processing) - 50% discount on batch requests
* [Rate limits](https://platform.claude.com/docs/en/api/rate-limits) - Understand usage tiers
* [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api) - Read your configured rate limits
* [Data residency](https://platform.claude.com/docs/en/manage-claude/data-residency) - Control inference geography
