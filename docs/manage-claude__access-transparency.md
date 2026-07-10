# Access Transparency

Receive an audit record of human access to your organization's data by Anthropic personnel through the Compliance API.

---

Learn how Access Transparency creates a record of human access to your organization's data by Anthropic personnel, what it covers, and how to receive events through the Compliance API.

<Note>
  When Access Transparency is enabled for your organization:

  * Each human view of your retained data (see [covered content](#what-access-transparency-covers)) by an Anthropic employee writes an `anthropic_access` activity to your [Compliance API Activity Feed](/docs/en/manage-claude/compliance-activity-feed).
  * Access occurs only for safety review or incident response. See [Reason codes](#reason-codes).

  Access Transparency is available to eligible customers on request and is not self-serve. For eligibility, refer to your contract terms or contact your Anthropic account representative.
</Note>

## How Access Transparency works

Anthropic personnel access customer content only under defined conditions. Access Transparency is designed to make such access visible to you. The design rests on the following principles:

* **Human access happens only under a published reason code.**
* **Human views of your covered content are recorded.** Anthropic's internal tooling that can reach your covered content is instrumented to emit an event on each view.
* **Events represent human access, not automated processing.** Anthropic's automated safety systems process your content in a secured pipeline with no interactive human access; that processing does not write to this feed.
* **Events arrive on your existing feed.** Activities are accessible through your [Compliance API Activity Feed](/docs/en/manage-claude/compliance-activity-feed). Existing credentials, audit, export, and SIEM integrations for the Compliance API will still apply.

## What Access Transparency covers

* **Covered content:** Access Transparency covers prompt and response content sent through the Claude Messages API or Claude Code sessions. Anthropic's [general ZDR documentation](/docs/en/manage-claude/api-and-data-retention) and [ZDR for Claude Code documentation](https://code.claude.com/docs/en/zero-data-retention) explain which APIs and features are covered by ZDR. The same APIs and features are covered by Access Transparency.
* **Manual views by Anthropic personnel:** Manual views of your covered content by Anthropic reviewers generate events.

## What Access Transparency does not cover

* **Automated processing:** Model serving, safety classifiers, and abuse-detection pipelines process your content as part of normal operation and do not generate events.
* **Your own organization's activity:** Your API calls, admin actions, and Compliance API reads are covered by standard [Activity Feed](/docs/en/manage-claude/compliance-activity-feed) event types.
* **Claude for Enterprise and Claude Apps:** claude.ai Enterprise seats, Claude for Work, Cowork, and Claude in Chrome are not covered.
* **Claude consumer products:** Claude Free, Pro, or Max plans.
* **Partner-operated platforms:** Amazon Bedrock and Google Cloud; refer to those platforms' transparency controls.
* **Anything ZDR does not cover:** Products that are not covered by ZDR (for example, the Files API, Anthropic-hosted stateful applications, and the Batch API) are not covered by Access Transparency. See [ZDR documentation](https://code.claude.com/docs/en/zero-data-retention#what-zdr-does-not-cover) for additional details.

## Getting started

To enable Access Transparency:

<Steps>
  <Step title="Request Access Transparency">
    Contact your Anthropic account representative.
  </Step>

  <Step title="Anthropic reviews eligibility">
    Anthropic confirms your organization meets the eligibility criteria and enables the capability at the organization level.
  </Step>

  <Step title="Receive events through the Compliance API">
    `anthropic_access` activities appear in your existing Activity Feed under your existing Compliance Access Key; no new endpoint or credentials are required.
  </Step>
</Steps>

Access Transparency is enabled at the organization level and covers all workspaces. Per-workspace enrollment is not currently available.

## Receiving Access Transparency events

Access Transparency events are delivered as the `anthropic_access` activity type on the Compliance API Activity Feed. Filter with `activity_types[]`:

```bash
curl --fail-with-body -sS -G \
  "https://api.anthropic.com/v1/compliance/activities" \
  --data-urlencode "activity_types[]=anthropic_access" \
  --data-urlencode "limit=50" \
  --header "x-api-key: $ANTHROPIC_COMPLIANCE_ACCESS_KEY"
```

Pagination, date-range filtering (`created_at.gte` / `.lt`), and the response envelope (`has_more`, `first_id`, `last_id`) are shared with the rest of the Activity Feed. See [Query the Activity Feed](/docs/en/manage-claude/compliance-activity-feed).

Each `anthropic_access` activity carries the standard Activity fields plus the following:

| Field                     | Type            | Description                                                                                                                                                      |
| ------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `id`                      | string          | Unique identifier for this activity                                                                                                                              |
| `accessed_at`             | RFC 3339 string | When the access occurred. Might be earlier than when the activity becomes visible in your feed                                                                   |
| `created_at`              | RFC 3339 string | When the activity became visible in your feed                                                                                                                    |
| `actor`                   | object          | Always `{ "type": "anthropic_actor", "email_address": null }`. Individual employee identity is not disclosed                                                     |
| `accessor_department`     | string          | The Anthropic team that performed the access (for example, `Safeguards`)                                                                                         |
| `reason_code`             | enum            | See [Reason codes](#reason-codes)                                                                                                                                |
| `resource_details.type`   | enum            | A resource type, currently only `message`. Extensible for future resource types                                                                                  |
| `resource_details.id`     | string or null  | Identifier of the content accessed                                                                                                                               |
| `resource_details.parent` | string or null  | Identifier of the content's parent, for example the conversation ID containing a message. Currently `null` or omitted until resources with parents are supported |
| `organization_id`         | string          | The organization the content belongs to. Tagged ID format (`org_...`)                                                                                            |
| `organization_uuid`       | string          | The organization the content belongs to. UUID format                                                                                                             |
| `workspace_id`            | string or null  | The workspace the content belongs to                                                                                                                             |

Example JSON message:

```json
{
  "id": "activity_013b013744txqZtFHLUaRqLr",
  "type": "anthropic_access",
  "created_at": "2026-06-08T17:12:09.812446Z",
  "accessed_at": "2026-06-08T17:12:06.478035Z",
  "organization_id": "org_0910d9133038914eta7i3vt",
  "actor": { "type": "anthropic_actor", "email_address": null },
  "resource_details": { "type": "message", "id": "msg_1234ABCD" },
  "accessor_department": "Safeguards",
  "reason_code": "safety_review",
  "organization_uuid": "5b236db4-3fb4-4bf3-a560-b5e266038a15"
}
```

## Reason codes

The set of reason codes is closed. Anthropic will update this page in the event it introduces a new code.

| Code                | Meaning                                                                        |
| ------------------- | ------------------------------------------------------------------------------ |
| `safety_review`     | Content was viewed as part of a usage-policy or safety investigation           |
| `incident_response` | Content was viewed while investigating an incident affecting your organization |

## CMEK content preservation

In rare cases, Anthropic preserves specific content beyond the standard retention window (for example, when a safety review confirms severely harmful content that must be retained for an ongoing investigation). Preservation is itself a logged, customer-visible action:

* **A preservation event is written to your feed.** When content is preserved, an event with type `cmek_preserve` is written to your Compliance API Activity Feed, carrying a reason code from the same closed set and the same fields as an access event.
* **Preservation follows review.** A preservation event always follows an `anthropic_access` event, because preservation is initiated from a human review.
* **For CMEK organizations, preservation is a visible key movement.** Preserved content is re-encrypted outside your customer-managed key so that the investigation can continue independent of your key. The preservation event is your record that this occurred. All other retained content remains under your key.

## Surface eligibility

The following table lists which surfaces are covered by Access Transparency. Coverage means human access to content from that surface generates `anthropic_access` events.

| Surface                                         | Covered | Details                                                                                                    |
| ----------------------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------- |
| Claude API (`api.anthropic.com`)                | Yes     | Prompts, completions, and data directly embedded in the API inputs                                         |
| Claude Code (using an API key)                  | Yes     | API traffic from Claude Code is covered as Claude API traffic                                              |
| Claude Platform on AWS                          | Yes     | Claude Platform on AWS generates Access Transparency events within the Compliance API (not AWS CloudTrail) |
| Claude API (`api.anthropic.com`) (Batch, Files) | No      | The Claude API Batch and Files APIs are not covered, just like they are not covered by ZDR                 |
| Claude for Enterprise (claude.ai seats)         | No      | Not covered                                                                                                |
| Claude for Work                                 | No      | Not covered                                                                                                |
| Claude Free, Pro, Max                           | No      | Consumer plans are not eligible                                                                            |
| Anthropic Workbench                             | No      | The Workbench stores data in data stores that are not covered by Access Transparency                       |
| Microsoft Foundry                               | No      | Not available                                                                                              |
| Amazon Bedrock, Google Cloud                    | No      | Partner-operated platforms; refer to those platforms' transparency controls                                |

## Limitations and exclusions

### Coverage timing

Access Transparency applies from the time it is enabled for your organization. Content already in your retention window at enablement might also generate events when accessed, but Anthropic does not guarantee coverage for content written before enablement. Treat your enablement date as the start of reliable coverage. There might be a delay of up to two hours between enabling Access Transparency and your content being covered.

### Notification timing

`anthropic_access` events are delivered to your Compliance API feed within two business days of the access they record. This feed should not be treated as a real-time alerting channel, and the `accessed_at` timestamp reflects when the access occurred, which might be up to two business days before the activity becomes visible in your feed. The `created_at` field reflects the time that the event became visible.

### Automated processing is not logged

Access Transparency records human access only. Anthropic's automated safety systems and classifiers continue to process your content as part of normal operation, and that processing does not generate `anthropic_access` events. An empty feed means no human at Anthropic has viewed your content; it does not mean your content was not processed by automated systems.

### Access Transparency does not change what Anthropic can access

Access Transparency records access; it does not grant or restrict it. The purposes for which Anthropic personnel may access your content are governed by your agreement with Anthropic and the [Usage Policies](https://www.anthropic.com/legal/aup), and are the same regardless of whether Access Transparency is enabled.

### CMEK key-use logs are not a per-read record

For organizations that also enable CMEK, your cloud KMS audit log (CloudTrail, Cloud Audit Logs, or Azure Monitor) records Anthropic's use of your key. Because keys are cached for short periods during operation, an individual human read does not necessarily produce a distinct KMS decryption entry. Use the Access Transparency feed as the per-access record; your KMS log independently confirms key usage patterns.

## Frequently asked questions

<AccordionGroup>
  <Accordion title="How do I know if my organization has Access Transparency enabled?">
    Contact your Anthropic account representative.
  </Accordion>

  <Accordion title="Will I see an event each time a safety classifier runs on my traffic?">
    No. Automated processing does not generate Access Transparency events. You will see an event only if a human reviewer subsequently views the content.
  </Accordion>

  <Accordion title="We are a platform that serves Claude to our own end users. Can we enable Access Transparency?">
    Access Transparency is not available for platform deployments. Contact your Anthropic account representative to discuss your use case.
  </Accordion>

  <Accordion title="Will I see events for access that happened before we enrolled, or for our older data?">
    Access Transparency is not guaranteed to be retroactive. It covers human access to content written to the Claude API on or after your enrollment date. You might see events for access to content that was written before enrollment.
  </Accordion>

  <Accordion title="How soon after an access will I see the event?">
    Within two business days of the access. Configure any SIEM alerting or scheduled exports with a matching lookback window rather than assuming real-time arrival.
  </Accordion>

  <Accordion title="How do I know which request an anthropic_access event refers to?">
    Use the `resource_details.id` field. It contains the same message ID (`msg_...`) that the [Messages API](/docs/en/api/messages/create) returns in the `id` field of every response body. To make this useful, log `id` in your own systems alongside your internal metadata, such as the application, end user, or conversation that produced the request. When an event arrives, join its `resource_details.id` against your logs to identify exactly which request was viewed.
  </Accordion>

  <Accordion title="Can I enable Access Transparency for a single workspace?">
    Access Transparency is enabled at the organization level and covers all workspaces.
  </Accordion>

  <Accordion title="How does Access Transparency relate to CMEK?">
    They are independent. With CMEK, safety preservation outside your key emits a separate `cmek_preserve` event on the same feed. See [CMEK](/docs/en/manage-claude/cmek).
  </Accordion>

  <Accordion title="How do I request Access Transparency?">
    Contact your Anthropic account representative.
  </Accordion>
</AccordionGroup>

## Related resources

* [Compliance API overview](/docs/en/manage-claude/compliance-api)
* [Activity Feed](/docs/en/manage-claude/compliance-activity-feed)
* [API and data retention](/docs/en/manage-claude/api-and-data-retention)
* [Customer-Managed Encryption Keys (CMEK)](/docs/en/manage-claude/cmek)
* [Claude Code data usage](https://code.claude.com/docs/en/data-usage)
* [Trust Center](https://trust.anthropic.com/resources)
