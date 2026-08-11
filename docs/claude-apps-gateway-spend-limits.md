> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude apps gateway spend limits

> Cap each developer's spend through the Claude apps gateway by day, week, or month. Set limits with an Admin API and the gateway enforces them live on every request.

Spend limits cap how much each developer can spend through your [Claude apps gateway](/docs/en/claude-apps-gateway) in a given day, week, or month. When a developer passes their cap, the gateway returns `429` on their next request and blocks them until the period resets or an admin raises the cap. Use spend limits to give each developer, group, or the whole organization a ceiling on a credential everyone shares.

A Claude apps gateway forwards all inference through one shared upstream credential, so your provider's bill attributes everything to that credential, not to individual developers. Without per-developer limits, one runaway agent fleet can spend the organization's entire commitment. Spend limits are the gateway's per-developer view and circuit breaker on top of that shared bill.

## Set a cap

With the [`admin:`](/docs/en/claude-apps-gateway-config#admin) block configured in `gateway.yaml`, the gateway serves an admin API at `/v1/organizations/spend_limits` and enforces caps live on every inference request. Caps themselves are set through that API, not in `gateway.yaml`; each `POST /v1/organizations/spend_limits` request creates or replaces one cap from `{scope, amount, period}`. The API mirrors the wire shapes of Anthropic's public [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api) spend-limits endpoints, so an HTTP client written against that contract can target the gateway by changing its base URL.

This request sets an org-wide default of \$500 per month for every developer:

```bash theme={null}
curl -sS https://claude-gateway.internal.example.com/v1/organizations/spend_limits \
  -H "x-api-key: $GATEWAY_ADMIN_WRITE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"scope": {"type": "organization"}, "amount": "50000", "period": "monthly"}'
```

This request layers a tighter \$100-per-day cap on each member of the `contractors` group:

```bash theme={null}
curl -sS https://claude-gateway.internal.example.com/v1/organizations/spend_limits \
  -H "x-api-key: $GATEWAY_ADMIN_WRITE_KEY" \
  -H "Content-Type: application/json" \
  -d '{"scope": {"type": "rbac_group", "rbac_group_id": "contractors"}, "amount": "10000", "period": "daily"}'
```

| Field        | Values                                      | Description                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------ | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `scope.type` | `user`, `rbac_group`, `organization`        | `user` targets one developer by their OpenID Connect (OIDC) `sub`, the stable user ID your identity provider assigns; pass it as `scope.user_id`. `rbac_group` targets an [IdP group](/docs/en/claude-apps-gateway-config#managed) by name; pass it as `scope.rbac_group_id`. `organization` is the org-wide default. The gateway accepts all three; Anthropic's public `POST` is user-only today. |
| `amount`     | Whole-number string of USD cents, or `null` | `null` is unlimited. `"0"` is a zero cap, which blocks every request.                                                                                                                                                                                                                                                                                                                         |
| `period`     | `daily`, `weekly`, `monthly`                | A scope can hold one cap per period, and each enforces independently: a developer is blocked if over any of them.                                                                                                                                                                                                                                                                             |

A group or organization cap is a per-seat default that each member inherits, not a shared pool. Per period, a developer's effective cap resolves in this order: a per-user override, then the most restrictive of their group caps, then the org default, then unlimited. [`admin.group_limit_mode: max`](/docs/en/claude-apps-gateway-config#admin) flips the multi-group tie-break to least-restrictive instead.

### Authenticate to the admin API

Send one of:

* An `x-api-key` header matching a key in [`admin.write_keys`](/docs/en/claude-apps-gateway-config#admin) for full access, or `admin.read_keys` for `GET`-only access. Each key carries an `id` that appears in the audit log as `admin-key:<id>`, so give Terraform, CI, and each automation its own.
* A gateway bearer token whose `groups` claim includes one of [`admin.admin_groups`](/docs/en/claude-apps-gateway-config#admin). This is full access and audits as `oidc:<sub>`, so prefer it for human admins.

## How enforcement works

On each `/v1/messages` request, the gateway looks up the developer's caps and period-to-date spend in one Postgres query. A developer over any cap gets a `429` with `error.type: billing_error` and header `x-should-retry: false`.

The message names the period and reset time, such as `spend limit reached (daily; resets 2026-08-08 00:00 UTC)`, followed by your [`admin.blocked_message`](/docs/en/claude-apps-gateway-config#admin) if set. When a developer exceeds several caps at once, the message names the cap that resets last. The response also carries a `retry-after` header with the seconds remaining until that reset. Before v2.1.225 on the gateway server, the message was `spend limit reached` with no period, reset time, or `retry-after` header.

On v2.1.227 or later, the protocol reference at `<public_url>/protocol` also lists the exact usage-limit response headers and `429` body.

Caps reset on UTC calendar boundaries: daily at 00:00 UTC, weekly on Monday, and monthly on the first. The gateway never blocks `/v1/messages/count_tokens`, because token counting is free.

### How requests are priced

After each response, a usage meter reads the token counts and adds the cost to the daily, weekly, and monthly counters. It never touches the bytes sent to the client, so a metering failure can't break a response. The amounts are USD estimates, a circuit breaker rather than an invoice; for billing, reconcile against your provider's usage reporting.

The meter picks each request's rates in this order:

1. A matching [`pricing.overrides`](/docs/en/claude-apps-gateway-config#pricing) row for the upstream that served the request. Requires v2.1.227 or later.
2. List price for the upstream model ID, the string the gateway sends to the provider, when the Claude Code cost table recognizes it. The table accepts Anthropic, Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry ID forms.
3. List price for the [`models[].id`](/docs/en/claude-apps-gateway-config#models) you mapped to that upstream ID, for upstream strings that carry no model name, such as an Amazon Bedrock application-inference-profile ARN or a Microsoft Foundry deployment name. Requires v2.1.218 or later.
4. The unknown-model tier of \$5/\$25 per million input/output tokens, so an ID the meter can't place is never free. The gateway warns at boot and once per ID at runtime when it uses this tier.

Whichever rate applies, the meter then multiplies the amount by [`pricing.multiplier`](/docs/en/claude-apps-gateway-config#pricing), default `1`.

Client aborts are billed too. When a stream ends without the upstream's final usage frame, the meter bills a floor estimate of about four characters per output token for the text already sent to the client, so aborting requests early doesn't evade a cap.

### Postgres availability

The pre-check queries Postgres with a two-second timeout. If the store is unreachable or times out, enforcement fails open by default: the request proceeds, the gateway logs a warning, and the response carries no `anthropic-ratelimit-unified-*` headers. Set [`enforcement.fail_closed_on_error: true`](/docs/en/claude-apps-gateway-config#enforcement) to fail closed instead, which returns the same `429 billing_error` but with the message `spend limit unavailable` and no period, reset time, or `retry-after` header. Fail-open keeps a store outage from becoming an inference outage; fail-closed guarantees no unmetered spend.

### Usage warnings in Claude Code

Claude Code warns a developer as they approach their cap: once utilization passes 75%, and again past 95% of their fullest cap. When the gateway blocks a request, Claude Code shows the gateway's `429` message as is, including your `admin.blocked_message`.

The warning works off response headers:

* With v2.1.225 or later on the gateway server, each successful `/v1/messages` response for a developer who has a cap carries their own cap utilization and reset time in the `anthropic-ratelimit-unified-*` headers.
* With v2.1.225 or later on the developer's machine as well, Claude Code reads the headers and shows the warning.

The headers always describe the developer's own cap: the gateway strips the upstream provider's rate-limit headers, which describe your shared quota, and never forwards them.

## Admin API reference

The endpoints below are served under `/v1/organizations/spend_limits`.

| Method and path                                | Description                                                                                                                                                  |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `GET /v1/organizations/spend_limits`           | List configured caps, optionally filtered to one `scope_type` of `organization`, `rbac_group`, or `user`. Query: `?limit=&after_id=&before_id=&scope_type=`. |
| `POST /v1/organizations/spend_limits`          | Create or replace a cap for `{scope, period}`.                                                                                                               |
| `GET /v1/organizations/spend_limits/{id}`      | Fetch one cap by its `spl_`-prefixed ID.                                                                                                                     |
| `DELETE /v1/organizations/spend_limits/{id}`   | Delete one cap. Returns `{type: "spend_limit_deleted", id}`.                                                                                                 |
| `GET /v1/organizations/spend_limits/effective` | Resolved cap and to-date spend per principal per period.                                                                                                     |
| `GET /v1/organizations/spend_limits/audit`     | Admin mutation trail, newest-first. Query: `?limit=&after_id=`.                                                                                              |

Conventions mirror Anthropic's Admin API:

* A `type` on every object
* `spl_`-prefixed IDs
* Amounts as whole-number strings of USD cents; `POST` rejects any other `currency` with `400`
* The `{type: "error", error: {type, message}, request_id}` error envelope
* A `request-id` response header on every admin response, success or error; error bodies also carry it as `request_id`

Every mutation writes a before/after row to `admin_audit` in the same transaction, attributed to `admin-key:<id>` or `oidc:<sub>`.

The gateway serves the spend-limits endpoints only. Other Admin API surfaces, such as the `spend_limit_increase_requests` queue, aren't part of the gateway's admin API.

### `/effective`

`GET /v1/organizations/spend_limits/effective` returns Anthropic's `SpendSummary` schema: each row is a principal for a period, with the resolved cap, period-to-date spend, and an `actor` object. Gateway-specific differences:

* `user_id` is the OIDC `sub`.
* `actor.name` and `actor.email_address` are `null` until the principal's first inference request through the gateway. The gateway has no user directory; it records last-seen values from each user's own session JWT.
* Each row also carries a `groups` array, the principal's last-seen IdP groups. This is a gateway extension so an admin UI can show every cap tier that applies; Anthropic-shaped clients ignore it.
* Without a `user_ids[]` filter, it lists principals with recorded spend, because the gateway can't enumerate all org members.

Group-sourced caps resolve against those last-seen groups with the same `group_limit_mode` tie-break that enforcement uses, so the viewer shows the cap that actually applies.

| Query parameter  | Description                                                                                             |
| ---------------- | ------------------------------------------------------------------------------------------------------- |
| `user_ids[]`     | Repeatable. Filter to specific principals by OIDC `sub`.                                                |
| `period[]`       | Repeatable. Filter to `daily`, `weekly`, or `monthly` rows.                                             |
| `sort`           | `spend_desc` lists top spenders first. Requires exactly one `period[]`.                                 |
| `q`              | Case-insensitive substring filter over the OIDC `sub`, last-seen email, and last-seen display name.     |
| `limit` / `page` | Page size, 1–1000 with a default of 20, and the opaque cursor from the previous response's `next_page`. |

<Warning>
  `q=` and `user_ids[]=` ride GET query strings, so any fronting proxy or load balancer captures them in its access logs. If your PII log policy is strict, scrub these parameters there.
</Warning>

### `/audit`

Returns the spend-limit mutation trail: who changed which cap, with before/after snapshots, newest-first. `has_more` is exact. This endpoint follows the local Admin API conventions rather than a first-party wire shape.

### Pagination

The raw list pages by `after_id` and `before_id`, which are mutually exclusive `spl_…` IDs; results are ordered by creation and `has_more` reflects the traversal direction. `/effective` pages by the opaque `next_page` token passed back as `?page=`, with principals ordered ascending so pages stay stable while spend is being recorded. `limit` is 1–1000, default 20, on both. `/audit` pages by `after_id`, the numeric `id` of the last event on the previous page, and its `limit` defaults to 100.

## Data lifecycle

The gateway holds four spend-related tables; an hourly sweep enforces the retention windows:

| Table              | Contents                                                                      | Retention                                                                                               |
| ------------------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `spend`            | Per-principal period-to-date counters in cents                                | [`admin.spend_retention_months`](/docs/en/claude-apps-gateway-config#admin), default 13                      |
| `spend_limits`     | The configured caps                                                           | Until deleted via the API                                                                               |
| `admin_audit`      | The mutation trail                                                            | [`admin.audit_retention_days`](/docs/en/claude-apps-gateway-config#admin), default 365                       |
| `principal_emails` | Each principal's last-seen email, display name, and IdP groups. Contains PII. | [`admin.identity_retention_days`](/docs/en/claude-apps-gateway-config#admin) since last activity, default 90 |

`identity_retention_days` is deliberately shorter than `spend_retention_months`: a deprovisioned identity stops refreshing and ages out, while its anonymous spend counters remain for year-over-year reporting.

When a developer leaves, delete any per-user cap via `DELETE /v1/organizations/spend_limits/{id}`; their spend and identity rows age out on the retention windows above. To erase one person immediately, for offboarding or a data subject access request (DSAR), run `DELETE FROM principal_emails WHERE principal = '<sub>'` directly against the gateway database. That removes the only table holding their email, name, and groups. The `spend` and `admin_audit` rows reference the pseudonymous OIDC `sub` only and age out on their own windows.

## Related

* [`admin` and `enforcement` configuration](/docs/en/claude-apps-gateway-config#admin): enabling the admin API and tuning retention
* [Deployment guide](/docs/en/claude-apps-gateway-deploy#postgres): Postgres schema and backup guidance
