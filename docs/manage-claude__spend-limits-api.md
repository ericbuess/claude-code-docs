# Spend Limits API

Set a spend limit on each Claude Enterprise member, see where each member's spend limit is inherited from, and review or act on members' requests for a higher limit.

---

The Spend Limits API lets you set a spend limit on each Claude Enterprise member, see where each member's spend limit is inherited from, and review or act on members' requests for a higher limit.

For per-user and time-bucketed usage and cost *reporting*, see [Analytics APIs](/docs/en/manage-claude/analytics-api).

<Check>
  **Scoped Admin API key required**

  These endpoints require an Admin API key with the `read:spend_limits` scope (for `GET` endpoints) or the `write:spend_limits` scope (for `POST` and `DELETE` endpoints). See [Create an Admin API key](/docs/en/manage-claude/admin-api-keys#create-a-key-for-a-claude-enterprise-organization) for where your primary owner creates one and which scopes to select. Pass the key in the `x-api-key` header on every request.
</Check>

<Note>
  The Spend Limits API is available to Claude Enterprise organizations only. It is not available to Claude Platform (Claude Console) organizations.
</Note>

## Overview

The API exposes eight endpoints across two resources:

| Resource                          | Endpoints                                                                                                                                                                                                                                             | Use for                                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| **Spend limits**                  | `GET /v1/organizations/spend_limits/effective` `GET /v1/organizations/spend_limits/{spend_limit_id}` `POST /v1/organizations/spend_limits` `DELETE /v1/organizations/spend_limits/{spend_limit_id}`                                                   | Read each member's effective spend limit and period-to-date spend; set or clear a per-user override.              |
| **Spend limit increase requests** | `GET /v1/organizations/spend_limit_increase_requests` `GET /v1/organizations/spend_limit_increase_requests/{id}` `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` `POST /v1/organizations/spend_limit_increase_requests/{id}/deny` | List members' requests for a higher spend limit, with the context needed to decide; approve or deny each request. |

Use the **spend limits** endpoints to answer "what spend limit applies to each member, where does it come from, and how close are they to it?" and to set a per-user override. Use the **spend limit increase requests** endpoints to work the queue of member-submitted requests.

## Prerequisites

* Your organization must be on a Claude Enterprise plan.
* Usage credits must be turned on for your organization. Your primary owner can turn them on in claude.ai billing settings.

## Quick start

List every member's effective monthly spend limit and period-to-date spend:

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Key concepts

### The spend limit hierarchy

An **effective spend limit** applies to each member's spend, resolved from a hierarchy of scope levels. When a member has no per-user override, they inherit the spend limit configured for their group (if your organization uses group-based limits), their seat tier, or the organization-wide default. A group spend limit is a per-member default: each member inheriting it is gated against their own spend, not a pooled group budget.

Reading `GET /v1/organizations/spend_limits/effective` returns every current member with their resolved effective spend limit, where that limit was resolved from (`source`), and their period-to-date spend. Setting a per-user override with `POST /v1/organizations/spend_limits` pins a member to a specific spend limit regardless of what they would otherwise inherit. Deleting the override returns them to the inherited spend limit (or leaves them unlimited if none exists).

The `source` field on each member's row tells you which level their spend limit resolved from: `user` (a per-user override), `seat_tier`, `rbac_group`, or `organization`. Treat scope types as an open set; fall through on unknown values rather than failing.

### Period

`period` is the recurring window over which the spend limit is enforced and spend resets. A spend limit is identified by its `(scope, period)` pair. Currently `monthly` is the only supported period; monthly spend resets at 00UTC on the first of each calendar month. Treat `period` as an open set.

### Amounts and currency

All monetary values are strings in **minor units of the organization's billing currency** (cents, for USD). For example, `"50000"` represents 500.00 USD. Parse as a decimal and divide by 100 to display dollars; avoid binary floating-point for large values.

`amount` is **nullable**. In a member's effective row, `null` means **unlimited** (no spend limit) and `"0"` means the member cannot use Claude beyond their plan's included usage. On a configured spend-limit row (as returned by `GET /v1/organizations/spend_limits/{id}`), `null` only means no numeric spend limit is set; read the member's effective row to distinguish unlimited from included-usage-only.

`period_to_date_spend` is the member's spend accrued since the start of the current `period`, in the same minor-unit format; it may include a fractional part (for example, `"41280.125"`). It may read as `"0"` if the spend reading is temporarily unavailable; treat it as informational, not transactional.

### Increase request lifecycle

A **spend limit increase request** is created when a member clicks **Request more usage** in claude.ai. Requests are not created through this API. A request's `status` is one of:

| Status     | Meaning                                                                                                                                                                                                                                  |
| ---------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pending`  | Awaiting admin action. The request normally carries a live `spend_summary` so you can see the member's current effective spend limit and period-to-date spend while deciding; `spend_summary` may be `null` if it could not be computed. |
| `approved` | The request was resolved with approval: either an admin approved it explicitly, another admin action raised the member's spend limit, or Anthropic support raised a spend limit on the organization's behalf. `spend_summary` is `null`. |
| `denied`   | An admin declined. `spend_summary` is `null`. claude.ai hides that member's request button for 30 days from `resolved_at`; an admin can still raise the member's spend limit directly at any time.                                       |

Both `approved` and `denied` are terminal. A member has at most one `pending` request at a time.

Approving with `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` writes the same per-user spend limit row that `POST /v1/organizations/spend_limits` writes. Setting a spend limit directly does **not** transition a pending request; use the approve endpoint to resolve a request.

By default, Anthropic emails the member when their request is approved or denied. Pass `suppress_notification: true` on approve or deny to suppress that email (for example, when your own system notifies the member).

## Rate limiting

All eight endpoints share a single per-organization limit of **60 requests per minute**. Requests over the limit return **429 Too Many Requests**.

## Pagination

`GET /v1/organizations/spend_limits/effective` and `GET /v1/organizations/spend_limit_increase_requests` are paginated with an **opaque cursor**. The first request returns up to `limit` rows plus a `next_page` cursor; pass that cursor unchanged as the `page` parameter on the next request, and repeat until `next_page` is `null`.

**Do not change query parameters mid-sequence.** Cursors are bound to the filters that issued them. If you change `user_ids[]`, `period[]`, `status[]`, or `actor_ids[]` and pass an old cursor, you'll get a 400 with *"cursor does not match current query parameters"*. Start a new sequence from the first page instead.

## Serializing list parameters

List parameters use bracket notation: repeat the parameter name with `[]` for each value.

```text wrap
user_ids[]=user_01AbCdEfGh&user_ids[]=user_01JkLmNoPq
```

## Error responses

Error responses follow the standard shape documented in [Errors](/docs/en/api/errors). Quote the `request_id` from the response body when contacting support.

## Spend limits

### List each member's effective spend limit

`GET /v1/organizations/spend_limits/effective` returns one row per current member, reflecting each member's effective spend limit, its `source` in the scope hierarchy, and their `period_to_date_spend`. Requires the `read:spend_limits` scope.

For complete parameter details and response schemas, see [List effective spend limits](/docs/en/api/admin/spend_limits/list_effective) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?limit=20" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

```json
{
  "data": [
    {
      "scope": { "type": "user", "user_id": "user_01AbCdEfGh" },
      "actor": {
        "type": "user_actor",
        "user_id": "user_01AbCdEfGh",
        "name": "Jane Smith",
        "email_address": "jane@example.com",
        "deleted": false
      },
      "amount": "50000",
      "currency": "USD",
      "period": "monthly",
      "source": { "type": "seat_tier", "seat_tier": "enterprise_standard" },
      "spend_limit_id": "spl_01XyZaBcDeFgHiJkLmNoPq",
      "period_to_date_spend": "31402.5"
    }
  ],
  "next_page": "page_..."
}
```

### Get a single spend limit

`GET /v1/organizations/spend_limits/{spend_limit_id}` returns one configured spend limit by ID. Use it to inspect the row that a `spend_limit_id` field referenced. Requires the `read:spend_limits` scope.

For complete parameter details and response schemas, see [Retrieve a spend limit](/docs/en/api/admin/spend_limits/retrieve) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limits/spl_01AbCdEfGhIjKlMnOpQrSt" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Set a per-user override

`POST /v1/organizations/spend_limits` sets a per-user spend limit override. This is an upsert keyed on `(scope, period)`: setting a limit for a user and period that already has one overwrites it in place. This endpoint accepts only `scope.type: "user"`; seat-tier, group, and organization-level defaults are configured in claude.ai settings. Requires the `write:spend_limits` scope.

For complete parameter details and response schemas, see [Create a spend limit](/docs/en/api/admin/spend_limits/create) in the API reference.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limits" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"scope": {"type": "user", "user_id": "user_01AbCdEfGh"}, "amount": "75000"}'
```

```json
{
  "type": "spend_limit",
  "id": "spl_01RsTuVwXyZaBcDeFgHiJk",
  "created_at": "2026-05-11T10:02:44Z",
  "updated_at": "2026-05-11T10:02:44Z",
  "scope": { "type": "user", "user_id": "user_01AbCdEfGh" },
  "amount": "75000",
  "currency": "USD",
  "period": "monthly"
}
```

### Remove a per-user override

`DELETE /v1/organizations/spend_limits/{spend_limit_id}` removes a per-user override, after which the member falls back to any inherited seat-tier, group, or organization default. Seat-tier, group, and organization-level rows cannot be deleted through this endpoint. Requires the `write:spend_limits` scope.

For complete parameter details and response schemas, see [Delete a spend limit](/docs/en/api/admin/spend_limits/delete) in the API reference.

```bash cURL
curl --request DELETE "https://api.anthropic.com/v1/organizations/spend_limits/spl_01RsTuVwXyZaBcDeFgHiJk" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

## Spend limit increase requests

### List increase requests

`GET /v1/organizations/spend_limit_increase_requests` lists requests, most recent first. Filter by `status[]` (`pending`, `approved`, `denied`) and `actor_ids[]`. The list excludes requests whose requester is no longer a member of the organization. Requires the `read:spend_limits` scope.

For complete parameter details and response schemas, see [List spend limit increase requests](/docs/en/api/admin/spend_limits/increase_requests/list) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=50" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Each pending request carries a live `spend_summary` showing the requester's current effective spend limit and period-to-date spend, enough to decide without a separate lookup.

### Get a single increase request

`GET /v1/organizations/spend_limit_increase_requests/{id}` returns one request by ID. Requires the `read:spend_limits` scope.

For complete parameter details and response schemas, see [Retrieve a spend limit increase request](/docs/en/api/admin/spend_limits/increase_requests/retrieve) in the API reference.

```bash cURL
curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

### Approve an increase request

`POST /v1/organizations/spend_limit_increase_requests/{id}/approve` approves a pending request: it writes a per-user spend limit at the admin-supplied `amount` for the requester and transitions the request to `approved`. The request does not carry a requested amount; you supply the new spend limit on approval. Requires the `write:spend_limits` scope.

For complete parameter details and response schemas, see [Approve a spend limit increase request](/docs/en/api/admin/spend_limits/increase_requests/approve) in the API reference.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/approve" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"amount": "75000", "suppress_notification": true}'
```

### Deny an increase request

`POST /v1/organizations/spend_limit_increase_requests/{id}/deny` denies a pending request. Idempotent on `denied`: denying an already-denied request returns 200 with the existing resource. The endpoint rejects an attempt to deny an already-approved request so automation can distinguish a retry from a conflicting decision. Requires the `write:spend_limits` scope.

For complete parameter details and response schemas, see [Deny a spend limit increase request](/docs/en/api/admin/spend_limits/increase_requests/deny) in the API reference.

```bash cURL
curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/slir_01AbCdEfGhIjKlMnOpQrSt/deny" \
  --header "content-type: application/json" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"suppress_notification": true}'
```

## Example workflows

These workflows combine the Spend Limits API with the [Analytics APIs](/docs/en/manage-claude/analytics-api) cost endpoints. The Analytics cost endpoints are designed for organization-wide spend reporting across a date range. `GET /spend_limits/effective` returns the cap that currently applies to each member. Start a sweep with Analytics to discover which members to look at, then read their current caps with `/effective`.

Spend Limits endpoints require the `spend_limits` scopes and Analytics cost endpoints require `read:analytics`; see [Analytics APIs](/docs/en/manage-claude/analytics-api) for how to provision access. All monetary values on both are decimal strings in minor units (cents). Both APIs paginate with an opaque cursor. Set an explicit `limit` and page through `next_page` until it's `null` to cover the whole organization.

### Automate the increase-request review flow

Run a scheduled job that fetches pending requests, applies your organization's approval policy, and resolves each one.

1. List pending requests:

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests?status[]=pending&limit=100" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
   ```

   Each request carries the requester's `actor.user_id` and a live `spend_summary` with their current effective `amount` and `period_to_date_spend`, enough to decide without a separate lookup.

2. Apply your policy. For example, auto-approve when the member's current `amount` is below a threshold, and route larger caps for manual review.

3. Resolve each request. To approve, supply the new cap:

   ```bash cURL
   curl --request POST "https://api.anthropic.com/v1/organizations/spend_limit_increase_requests/{id}/approve" \
     --header "content-type: application/json" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
     --data '{"amount": "75000", "suppress_notification": true}'
   ```

   To deny, `POST` to `.../{id}/deny` instead. Pass `suppress_notification: true` when your own system notifies the requester.

### Identify members close to their spend limit

Find members approaching their cap so you can raise it before they're blocked.

1. Pull each member's month-to-date spend from the Analytics API (one row per member, highest spend first by default):

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?starting_at=2026-06-01T00:00:00Z&limit=1000" \
     --header "x-api-key: $ANALYTICS_API_KEY"
   ```

   Each row carries `actor.user_id`, `actor.email`, and `amount` (the member's spend in cents). Page through `next_page` to cover the whole organization.

2. For the top spenders (or everyone above a dollar threshold), fetch effective caps in batches:

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/spend_limits/effective?user_ids[]=user_01Ab...&user_ids[]=user_01Cd...&limit=100" \
     --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
   ```

   Each row returns the cap as `amount` (`null` = unlimited, `"0"` = included usage only) alongside `period_to_date_spend`.

3. For each member with a positive cap, compute `period_to_date_spend / amount` and flag those at or above your threshold (for example, 80 percent). Treat a `"0"` cap as already at-limit. There is no server-side filter for this ratio.

4. Act on flagged members: raise the cap with `POST /v1/organizations/spend_limits`, approve a pending increase request if one exists, or reach out to the member.

### Find members with rapidly changing usage

Surface members whose spend has jumped week over week.

1. Pull per-member daily cost for the trailing two weeks from the Analytics API:

   ```bash cURL
   curl "https://api.anthropic.com/v1/organizations/analytics/user_cost_report?starting_at=2026-06-09T00:00:00Z&ending_at=2026-06-23T00:00:00Z&bucket_width=1d&limit=1000" \
     --header "x-api-key: $ANALYTICS_API_KEY"
   ```

   With `bucket_width` set, each member spans one row per day with usage; page through `next_page` to collect every member's full series.

2. Group rows by `actor.user_id`. For each member, sum the most recent seven days and the prior seven days. Flag members whose recent week exceeds the prior week by your chosen multiple (for example, three). Recent-day cost is provisional and can be revised upward; for repeatable comparisons, set `ending_at` at or before a previously returned `data_refreshed_at` (see [Data availability and freshness](/docs/en/manage-claude/analytics-api#data-availability-and-freshness)).

3. Act on flagged members: adjust the cap with `POST /v1/organizations/spend_limits`, or reach out.

## Frequently asked questions

### Does setting a spend limit directly resolve a member's pending increase request?

No. `POST /v1/organizations/spend_limits` writes the override but leaves the pending request untouched. Use `POST /v1/organizations/spend_limit_increase_requests/{id}/approve` to resolve the request and write the override in one call.

### What happens when I delete a per-user override?

The member falls back to whatever they'd inherit from the hierarchy: their group, seat-tier, or organization default. If no default exists at any level, the member is unlimited.

### Can I set a seat-tier or organization-wide default through this API?

No. Only per-user overrides can be written through this API. Seat-tier, group, and organization-level defaults are configured in claude.ai Organization settings.

### Why does `period_to_date_spend` sometimes read as `"0"` for an active member?

The spend reading can be temporarily unavailable, in which case the field reads `"0"` rather than erroring. Treat it as informational.

## See also

<CardGroup cols={2}>
  <Card title="Spend Limits API reference" href="/docs/en/api/admin/spend_limits">
    Generated request and response schemas for every Spend Limits API endpoint.
  </Card>

  <Card title="Spend Limit Increase Requests API reference" href="/docs/en/api/admin/spend_limits/increase_requests">
    Generated request and response schemas for the increase-request endpoints.
  </Card>

  <Card title="Analytics APIs" href="/docs/en/manage-claude/analytics-api">
    Per-user and time-bucketed usage and cost reporting for Claude Enterprise.
  </Card>
</CardGroup>
