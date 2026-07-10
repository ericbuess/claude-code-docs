# Design your compliance integration

Choose between polling and cursor-driven Activity Feed consumption, correlate Compliance API events with your SIEM, and plan retention.

---

<Note>
  To enable the Compliance API, see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

<Check>
  **Required scope:** `read:compliance_activities` on the Compliance Access Key or Admin API key.
</Check>

A production Compliance API integration makes three design choices: how it consumes the Activity Feed, how its output correlates with your security information and event management (SIEM) system, and where long-term copies of activity and content live. These choices are independent of the endpoints themselves; this page helps you evaluate the tradeoffs.

This page assumes you have read [Query the Activity Feed](/docs/en/manage-claude/compliance-activity-feed), which defines the parameters and pagination contract referenced throughout, and [Retrieve and delete chats, files, and projects](/docs/en/manage-claude/compliance-content-data), which defines the content endpoints and `deleted_at` semantics referenced in [Plan content retention](#plan-content-retention).

## Choose a feed-consumption pattern

The Activity Feed supports two consumption patterns: periodic window polling bounded by `created_at.gte` and `created_at.lt`, and cursor-driven incremental reads that persist a cursor from one response and pass it on the next request. Both return identical `Activity` objects; the difference is the state your client persists between calls.

Both patterns share these constraints:

* Activities are queryable within 1 minute of occurring and retained for 6 years.
* The maximum `limit` for each page is 5,000.
* Cursor values are opaque strings that you must not parse.
* Requests are limited to 600 per minute per [parent organization](/docs/en/manage-claude/compliance-api#how-the-compliance-api-works), shared across every key, every linked organization, and every `/v1/compliance/*` endpoint; see [429 Too Many Requests](/docs/en/manage-claude/compliance-errors#429-too-many-requests) for the response headers and retry contract.

| Pattern                         | Choose when                                                                                                                                                                                                     |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Window polling                  | Your pipeline runs on a fixed schedule, you prefer stateless workers, and you can tolerate replaying or overlapping windows                                                                                     |
| Cursor-driven incremental reads | You want the lowest latency between an activity occurring and your pipeline ingesting it, you want to avoid re-reading pages you already drained, and you have a durable place to persist a cursor between runs |

### Window polling

Set `created_at.lt` at least 1 minute in the past so that every activity in the window is already queryable. Use `created_at.gte` for the lower bound and `created_at.lt` for the upper bound so that consecutive windows tile without gaps or overlap; reuse the previous window's `lt` value as the next window's `gte`.

<CodeGroup>
  ```bash cURL
  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "created_at.gte=2026-04-20T07:00:00Z" \
    --data-urlencode "created_at.lt=2026-04-20T08:00:00Z" \
    --data-urlencode "limit=5000"
  ```
</CodeGroup>

When the response has `has_more: true`, the window contains more than one page of activities. Either page within the window by passing the response's `last_id` as `after_id` on the next request (stopping when `has_more` is `false`), or choose a smaller time window. See [Paginate results](/docs/en/manage-claude/compliance-activity-feed#paginate-results) for the full contract.

Even with clean tiling, an activity that indexes after its window has closed never appears in a later window. Deduplicate on the activity `id` and either widen each new window so it overlaps the previous one by a few minutes or run a periodic reconciliation pass that re-queries an older window.

<Warning>
  A `created_at.lt` bound too close to the present silently and permanently drops late-indexed activities: once `created_at.gte` advances past them, no later window can recover them. Treat the 1-minute queryability figure as the documented indexing lag, not a soft recommendation.
</Warning>

### Cursor-driven incremental reads

<CodeGroup>
  ```bash cURL
  first_id="activity_01XyDMpzjS89pFZXqSFUBDr6"  # first_id from a previous response

  curl --fail-with-body -sS -G \
    "https://api.anthropic.com/v1/compliance/activities" \
    --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY" \
    --data-urlencode "limit=5000" \
    --data-urlencode "before_id=$first_id"
  ```
</CodeGroup>

Page through until `has_more` is `false`, then persist `first_id` from the final response and pass it unchanged as `before_id` on the next run to retrieve activities newer than the saved cursor. To walk in the opposite direction for a backfill, persist `last_id` and pass it as `after_id` instead. For the full cursor-vs-page-token reference and retry semantics, see [Paginate results](/docs/en/manage-claude/compliance-activity-feed#paginate-results).

A production **catch-up** loop fetches activities recorded since your last poll by driving iteration off `has_more` and `first_id`:

```text
cursor = stored_cursor
loop:
  page = GET /v1/compliance/activities?before_id={cursor}&limit=5000
  store(page.data)
  if page.first_id is not null:
    cursor = page.first_id
  if not page.has_more: break
persist(cursor)
```

Cursors survive key rotation; see [Manage and rotate keys](/docs/en/manage-claude/compliance-api-access#manage-and-rotate-keys).

<Warning>
  Each page is adjacent to the cursor you pass: the loop walks forward toward the present, one page at a time. Do not treat a single response as caught up while `has_more` is `true`. Persist the cursor only after `has_more` is `false`; the unfetched pages are the newer ones between this response's `first_id` and the present, and they stay unread until you finish the loop or run again.
</Warning>

## Correlate with your SIEM

Each `Activity` carries fields you can join against events already in your SIEM (Splunk, Datadog, Microsoft Sentinel, Cribl, or similar):

| Compliance API field  | Join target                                     |
| --------------------- | ----------------------------------------------- |
| `actor.user_id`       | Your identity provider's stable user identifier |
| `actor.email_address` | Directory email when a stable ID is unavailable |
| `actor.ip_address`    | Network, VPN, and endpoint logs                 |
| `created_at`          | Time-window correlation across any source       |

`actor.user_id` and `actor.email_address` are present when `actor.type` is `user_actor`; check the discriminator before reading them. `user_id` is a stable, opaque identifier for the user account: it is consistent across every Compliance API endpoint and activity payload, and it does not change when the user's email or display name changes. Use `user_id`, not `email_address`, as the primary join key.

Calls to the Compliance API itself emit `compliance_api_accessed` activities. Ingest these alongside other activity types so your SIEM records who queried compliance data, and when. Pass `activity_types[]=compliance_api_accessed` to scope the query, then in your client, read `actor.api_key_id` from each activity whose `actor.type` is `api_actor` to attribute the access to a specific Compliance Access Key or Admin API key.

## Plan content retention

Three retention horizons govern what you can retrieve later:

| Data                                            | Retained for                                      | Controlled by                       |
| ----------------------------------------------- | ------------------------------------------------- | ----------------------------------- |
| Activity Feed records                           | 6 years                                           | Anthropic                           |
| Chat, file, and project content                 | Your organization's claude.ai retention policy    | Your organization                   |
| Content hard-deleted through the Compliance API | Not retained; deletion is immediate and permanent | The caller of the `DELETE` endpoint |

For how the rest of the Claude Platform handles retention, see [API and data retention](/docs/en/manage-claude/api-and-data-retention).

Decide between export-and-archive and on-demand API retrieval as follows:

* If your legal-hold or audit horizon exceeds 6 years for activity metadata, export Activity Feed pages to your own archive as you ingest them.
* If your content-retention policy is shorter than your eDiscovery horizon, export chat and file content before the retention window expires; the Compliance API cannot return content that retention has already removed.
* If a workflow might issue a Compliance API hard-delete (for example, DLP enforcement), retrieve and archive the target content first. There is no recovery window after a hard-delete; soft-deletes from claude.ai remain retrievable with `deleted_at` populated, but Compliance API deletes do not.

In every other case, rely on direct API retrieval and avoid maintaining a parallel copy.

### Delivery guarantees and completeness

Treat the Activity Feed as **at-least-once**: a correctly paginated traversal returns every activity at least once, but a retry after a partial failure can re-deliver activities you already stored. Deduplicate on the activity `id` field.

The list endpoints do not return a `total_count` field or a checksum. To attest that an export run is complete, log:

* The starting cursor and the terminal `last_id`.
* The number of records exported.
* The run timestamp and the `request-id` of the final page.

The content endpoints (chats, files, projects, and project attachments) serve claude.ai data only; the Activity Feed surfaces administrative and resource events organization-wide. The Compliance API does not include:

* Prompt text or model responses from Claude Console or Claude API workloads.
* Content removed by your organization's retention policy.
* Content hard-deleted through the Compliance API.

See the [Compliance API FAQ](/docs/en/manage-claude/compliance-faq#data-coverage-and-retention) for more on what the Compliance API does and does not capture.

For chain of custody, store the exported records with provenance metadata: source endpoint, query parameters, run timestamp, and a content hash of each record.

## Next steps

<CardGroup cols={2}>
  <Card title="Query the Activity Feed" href="/docs/en/manage-claude/compliance-activity-feed">
    Filter parameters, pagination, and the `Activity` object schema.
  </Card>

  <Card title="Retrieve and delete chats, files, and projects" href="/docs/en/manage-claude/compliance-content-data">
    The content and hard-delete endpoints.
  </Card>
</CardGroup>
