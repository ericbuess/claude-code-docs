# Analytics APIs

Understand which analytics API and API key your organization needs, then provision access to Claude Code productivity metrics or Claude Enterprise engagement and adoption data.

---

Anthropic provides two analytics APIs, and which one you use depends on which Claude product your organization manages:

* The **Claude Code Analytics API** reports daily Claude Code productivity metrics for organizations that use the Claude Platform. It is part of the [Admin API](/docs/en/manage-claude/admin-api) and uses an Admin API key.
* The **Claude Enterprise Analytics API** reports organization-wide engagement, adoption, and cost data across Claude products (chat, projects, Claude Code, and more) for Claude Enterprise organizations. It uses an Analytics API key created in claude.ai.

The two APIs use different key types, created in different places by different roles. This page describes which API fits your organization and how to create the right key.

## Which API do you need?

| API                                 | Key type                             | Created in                                                                                | Who can create it  | What it covers                                                                                                                                     |
| ----------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Code Analytics API**       | Admin API key (`sk-ant-admin01-...`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | Organization admin | Daily Claude Code metrics per user: sessions, lines of code, commits, pull requests, tool acceptance, and estimated cost by model                  |
| **Claude Enterprise Analytics API** | Analytics API key                    | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Primary owner      | Organization-wide engagement and adoption (user activity, active-user summaries, project, skill, and connector usage), plus cost and usage reports |

The key types are not interchangeable: an Admin API key cannot call the Claude Enterprise Analytics API, and an Analytics API key cannot call the Admin API. Both APIs appear under the [Admin API reference](/docs/en/api/admin), but they are separate APIs with separate key types. If your organization uses both the Claude Platform and Claude Enterprise, you can provision both keys and use each API for its own data.

<Note>
  Looking for API usage and cost data rather than product analytics? See the [Usage and Cost API](/docs/en/manage-claude/usage-cost-api), which explains the right path for both Claude Console and Claude Enterprise organizations.
</Note>

<Note>
  If you want to view engagement and adoption data in the product rather than programmatically, use the [Analytics dashboard](https://claude.ai/analytics/activity) in claude.ai. For governance and auditing use cases (individual user actions, raw activity events, conversation content), see the [Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

## Get access to the Claude Code Analytics API

The Claude Code Analytics API is available to every organization with access to the [Admin API](/docs/en/manage-claude/admin-api), and is free to use.

<Steps>
  <Step title="Create an Admin API key">
    Follow the steps in [Create an Admin API key](/docs/en/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization).
  </Step>

  <Step title="Call the API">
    Pass the key in the `x-api-key` header:

    ```bash
    curl "https://api.anthropic.com/v1/organizations/usage_report/claude_code?starting_at=2025-09-08" \
      --header "anthropic-version: 2023-06-01" \
      --header "x-api-key: $ADMIN_API_KEY"
    ```
  </Step>
</Steps>

For the available metrics, request parameters, and response schema, see the [Claude Code Analytics API guide](/docs/en/manage-claude/claude-code-analytics-api) and the [API reference](/docs/en/api/admin/usage_report/retrieve_claude_code).

## Get access to the Claude Enterprise Analytics API

The Claude Enterprise Analytics API is available to Claude Enterprise organizations. Engagement and adoption data is available on all Enterprise plans. The cost and usage endpoints apply to usage-based Enterprise plans; for seat-based Enterprise plans, they reflect usage credits only.

<Steps>
  <Step title="Sign in as the primary owner">
    Only the primary owner of the organization can enable API access and create Analytics API keys.
  </Step>

  <Step title="Enable API access and create a key">
    Go to [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) and enable public API access, then create an Analytics API key. Keys carry the `read:analytics` scope. Copy the displayed secret and store it in your secrets manager.
  </Step>

  <Step title="Call the API">
    Pass the key in the `x-api-key` header. Endpoints live under `https://api.anthropic.com/v1/organizations/analytics/`. For request examples, parameters, and response schemas, see the [Claude Enterprise Analytics API reference](/docs/en/api/admin/analytics).
  </Step>
</Steps>

The Claude Enterprise Analytics API provides:

* **User activity:** per-user daily metrics across chat (conversations, messages, projects, files, artifacts), Claude Code (sessions, commits, pull requests, lines of code, tool actions), and other Claude products
* **Activity summaries:** organization-level daily, weekly, and monthly active users, seat counts, and pending invites
* **Project, skill, and connector usage:** adoption breakdowns for chat projects, skills, and connectors
* **Cost and usage reports:** per-user and organization-level token usage and cost over time (usage-based Enterprise plans)

For endpoint details, parameters, and response schemas, see the [Claude Enterprise Analytics API reference](/docs/en/api/admin/analytics). The following sections cover data freshness, metric definitions, and operational guidance that apply across those endpoints.

## Data availability and freshness

Claude Enterprise Analytics API data is available for dates on or after January 1, 2026.

**Engagement and adoption endpoints** (user activity, summaries, projects, skills, connectors) return a per-day snapshot for the date you specify. Data for a given day is aggregated at 10UTC the following day and becomes available for querying three days after aggregation. If data is not available within that timeline, it usually indicates a data pipeline failure on Anthropic's side; contact support if the gap persists.

**Cost and usage endpoints** follow a different freshness model. Data is typically available within four hours of the underlying usage but may take up to 24 hours. Values for a given date can be revised for up to 30 days as late events arrive and reconciliation runs. For invoicing-grade totals, query dates at least 30 days in the past.

<Note>
  Cost and usage responses include a `data_refreshed_at` timestamp. When `ending_at` is omitted (the default is the current time), the response includes a tail of data after `data_refreshed_at` that is incomplete. For stable results across repeated calls, set `ending_at` to a value at or before a previously returned `data_refreshed_at`.
</Note>

## How metrics are defined

**Active users.** A user counts as active for a day if any of the following is true: they sent at least one chat message in Claude, they had at least one Claude Code session (local or remote) associated with your Claude Enterprise organization that included tool use or git activity, or they had at least one Cowork session with tool use or message activity.

**Per-product metric blocks.** Per-product metric objects (for example, Office Agent or Cowork metrics on a user-activity record) are always present on every record. Organizations without usage of that product see all-zero values rather than `null`.

**Connector names.** Connector names are normalized across sources. For example, `Atlassian MCP server`, `mcp-atlassian`, and `atlassian_MCP` all appear as `atlassian` in the connector usage endpoint.

## Working with the API

**Pagination cursors are bound to the query that issued them.** On the cost and usage endpoints, do not change query parameters mid-sequence: if you change `products[]`, `group_by[]`, `order_by`, the date range, or any filter and pass an old cursor, the request returns a 400 error. To change parameters, restart from the first page without a cursor.

**List parameters use bracket notation.** Repeat the parameter for each value, for example `products[]=chat&products[]=claude_code`.

**Amount fields are decimal strings in cents.** Currency amounts are returned as decimal strings such as `"41280.000000"` (which represents $412.80). To convert to dollars, parse as a decimal and divide by 100. Avoid binary floating-point parsing for values that may exceed several million dollars.

**Rate limits apply at the organization level**, not per key, with a default of 60 requests per minute across all endpoints in this API. If that is not sufficient for your use case, contact your Anthropic account team to discuss adjusting the limit.

## Known limitations

If your organization uses Claude Code through Amazon Bedrock, the Claude Enterprise Analytics API does not return Claude Code activity for that usage.

## Next steps

<CardGroup cols={2}>
  <Card title="Claude Code Analytics API" href="/docs/en/manage-claude/claude-code-analytics-api">
    Track Claude Code sessions, code changes, and tool usage with an Admin API key.
  </Card>

  <Card title="Usage and Cost API" href="/docs/en/manage-claude/usage-cost-api">
    Track API token usage and costs for your organization.
  </Card>

  <Card title="Claude Enterprise Analytics API reference" href="/docs/en/api/admin/analytics">
    Endpoint reference for engagement, adoption, and cost data.
  </Card>

  <Card title="Set up the Compliance API" href="/docs/en/manage-claude/compliance-api-access">
    Audit and compliance data uses its own key types.
  </Card>
</CardGroup>
