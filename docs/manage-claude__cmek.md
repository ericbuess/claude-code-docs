# Customer-managed encryption keys

Encrypt Claude workspace data at rest with a key you control.

---

```bash Learn more with the /claude-api skill in Claude Code
claude "/claude-api tell me about customer-managed encryption keys"
```

A customer-managed encryption key (CMEK) lets you provision an encryption key in your own [AWS KMS](https://aws.amazon.com/kms/), [Google Cloud KMS](https://cloud.google.com/security/products/security-key-management), or [Azure Key Vault](https://azure.microsoft.com/en-us/products/key-vault) and have Anthropic use it to encrypt certain workspace data at rest. You retain full control of the key, including rotation, audit, and revocation, and the key operations Anthropic performs against your key are recorded in your cloud provider's audit logs.

The use of CMEK is optional. Eligible organizations can **opt in** to use customer-managed encryption keys instead of the default encryption that Anthropic provides. To activate CMEK, contact your Anthropic account team.

<Accordion title="Enabling CMEK is permanent and can cause irreversible data loss" className="!border-warning-200 bg-warning-900 text-warning-000 [&_button:hover]:bg-warning-200/10">
  Enabling CMEK is permanent. Anthropic keeps no copy of your key, so misconfiguration or key loss can permanently destroy your CMEK-protected data. If you are uncertain about any step, contact your Anthropic representative before applying changes.

  * **Permanent data loss:** If your encryption key is deleted, scheduled for deletion, or has its key material destroyed, Anthropic cannot recover your data.
  * **Identifier verification is mandatory:** Granting key access to an incorrect or spoofed principal can expose your data to an unauthorized party. Always verify the Anthropic identifier against the published production identities in each configuration guide. Never trust an identifier provided over email, chat, or any onboarding channel.
</Accordion>

## How it works

Only admins can configure CMEK. On Claude Platform, CMEK is scoped per workspace and configured with the Admin API. On Claude Enterprise, CMEK is scoped per organization and configured in [claude.ai > Organization settings > Data and privacy](https://claude.ai/admin-settings/data-privacy-controls). On either product, CMEK protects data written after the key is enabled. Existing data (prior chats, files, and sessions) remains encrypted with Anthropic-managed keys and is not re-encrypted under your key.

CMEK admin configuration events appear in the [Compliance API Activity Feed](/docs/en/manage-claude/compliance-activity-feed). The key operations Anthropic performs against your key (such as wrapping and unwrapping data keys) do not appear in the Compliance API; they appear in your cloud provider's audit logs.

Anthropic calls your key management service from its standard public IP range. If you restrict access to your key management service by IP, allow the addresses listed in [IP addresses](/docs/en/api/ip-addresses).

## Prerequisites

* Cloud Admin access in the account, project, or subscription that will host the encryption key.
* An admin role in your Anthropic organization: an Organization Admin role in the Claude Console on Claude Platform, or an Owner or Primary Owner role on Claude Enterprise.
* Data retention configuration: CMEK is allowed with [Zero data retention (ZDR)](/docs/en/manage-claude/api-and-data-retention) for both Claude Platform and Claude Enterprise.

## Availability and regions

CMEK is currently available in US regions only, and all encryption operations are processed in US regions. Multi-region keys and EU key residency are not yet supported.

On [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), CMEK is available with AWS KMS keys only; Google Cloud KMS and Azure Key Vault keys cannot be registered. Create, validate, and attach keys in the Claude Console; the `external_keys` API endpoints are not currently available on Claude Platform on AWS. The key must be in the same AWS region as the workspace it is attached to.

For minimal latency, choose a region close to Anthropic's US infrastructure:

| Provider     | Recommended regions         |
| ------------ | --------------------------- |
| AWS          | `us-east-2`                 |
| Google Cloud | `us-central1`, `us-east5`   |
| Azure        | `northcentralus`, `eastus2` |

## What CMEK protects

What CMEK covers depends on which product you use.

### Encrypted

**Claude Platform**

* Message content, files and attachments (both inline attachments sent with a request and Files API uploads), and MCP and tool configuration.

**Claude Enterprise**

* Chat content, including skills, plugins, and artifacts.
* Chat attachments and project attachments.
* Claude Code on the CLI, including message content.
* Cowork in Claude Desktop.
* Office agents.

On both products, backups and snapshots inherit the key.

### Disabled or modified

Some features are turned off or substantially modified when CMEK is enabled. This list is not exhaustive; review it with your team before enabling CMEK.

**Claude Platform**

* Workbench in the Claude Console is disabled.
* Portions of the Compliance API that return raw content, such as prompts, responses, and files, are disabled.
* Beta and research preview features may not be covered by CMEK. This includes Claude Managed Agents, a beta feature that is disabled as a whole, including agent memory and agent dreaming.

**Claude Enterprise**

* Conversation history search is disabled. Conversation titles are encrypted, so searching by title or content returns no results.
* Search across large numbers of files is slower.
* The Analytics API and in-product analytics are degraded. Some usage views and reports may be incomplete.
* Audit log exports are disabled.
* Signed URLs for temporary file exchanges are disabled. These back claude.ai admin data exports and Claude Code Remote file flows such as screenshot updates.
* Personal preferences are disabled for users who belong to a CMEK-protected organization, across all organizations under the same parent. Users who do not belong to a CMEK-protected organization can still use them across all organizations.

### Not encrypted

These features remain available, but their data is not encrypted under your key. You can disable any feature that is not appropriate for your use case in Settings.

**Claude Platform**

* Data that is not at rest (such as cache) and data with a TTL shorter than 24 hours.
* Activity Feed, audit logs, and telemetry network traffic such as OTEL, so customers can maintain compliance even if a key is revoked.

**Claude Enterprise**

* Claude Code Desktop, Claude Code on the web, and Claude in Slack. Anthropic recommends disabling any of these that are not appropriate for your use case in the admin console.
* Beta and research preview features may not be covered by CMEK and can break in CMEK organizations, for example Claude Security and Claude Design.
* On-demand data export under Settings > Privacy.

On both products, account data for users in your organization (such as names, email addresses, and profile pictures) is not encrypted under your key.

### Feature support

The following Claude Platform APIs and tools store data at rest under your key when CMEK is enabled:

| APIs          | Tools and features                                               |
| ------------- | ---------------------------------------------------------------- |
| Messages      | Web search                                                       |
| Models        | Web fetch                                                        |
| Files         | Code execution                                                   |
| Batch         | Bash tool                                                        |
| Skills        | Text editor tool                                                 |
| User profiles | MCP connector                                                    |
|               | Structured outputs (Claude Sonnet 4.6 and Claude Haiku 4.5 only) |
|               | Advisor tool                                                     |
|               | Computer use                                                     |
|               | Context management                                               |

## Limited preservation outside your key

In three narrow cases, Anthropic may preserve specific records under Anthropic-managed encryption:

* Where Anthropic is required by law to retain records (for example, material reported to NCMEC under 18 U.S.C. § 2258A).
* Exigent risk of serious harm (for example, CBRNE weapons development, offensive cyberattacks, or imminent threats of violence).
* Violations of Section D.4 of Anthropic's [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) or equivalent terms in a customer's other applicable agreement with Anthropic.

Outside of [CSAM screening](https://support.claude.com/en/articles/9020328-csam-detection-and-reporting), preservation requires a human reviewer's explicit decision and follows Anthropic's [retention policy for commercial data](https://privacy.claude.com/en/articles/10023548-how-long-do-you-store-my-data). For every instance of preservation, a corresponding [Compliance API Activity Feed](/docs/en/manage-claude/compliance-activity-feed) event is generated with a reason code conveying the purpose of the preservation. See [CMEK content preservation](/docs/en/manage-claude/access-transparency#cmek-content-preservation) for details. Safety screening metadata (records derived from Anthropic's automated safety scans, such as pattern identifiers and match indicators, not conversation content) is retained under Anthropic-managed encryption and remains readable after key revocation.

## Limitations

* **Irreversible action:** Once a key is attached to a workspace, it cannot be detached or swapped. On Claude Platform, attaching a key also locks the workspace's data retention setting: you cannot turn off 30-day data retention for that workspace, and returning to zero data retention requires creating a new workspace and moving your traffic to it. Rotating the key material within the same key (for example, AWS KMS automatic rotation, a Cloud KMS rotation schedule, or an Azure Key Vault rotation policy) is supported transparently and requires no change in Anthropic. Switching to a *different* key requires creating a new workspace with the new key and migrating your data. Revoking or disabling the key makes all CMEK-protected data in that workspace permanently inaccessible, with no backout path.
* **No retroactive encryption:** CMEK only protects data written after the key is enabled.
* **Latency:** Operations that wrap or unwrap data keys make a round-trip to your key management service, which can add a small amount of latency to actions that read or write data at rest.
* **Revocation delay:** Key revocation can take up to one hour (the cache TTL). Requests already in flight during that window may continue to succeed.
* **KMS costs:** CMEK requires a key in a third-party key management service (AWS KMS, Google Cloud KMS, or Azure Key Vault), which may incur separate charges billed by your KMS provider.

## Configure your provider

Follow the guide for the key management service you use.

<CardGroup cols={3}>
  <Card href="/docs/en/manage-claude/cmek-aws-kms" title="AWS KMS">
    Create an AWS KMS key with a cross-account key policy, then register and validate it.
  </Card>

  <Card href="/docs/en/manage-claude/cmek-google-cloud-kms" title="Google Cloud KMS">
    Create a Cloud KMS crypto key, grant Anthropic's service account access, then register it.
  </Card>

  <Card href="/docs/en/manage-claude/cmek-azure-key-vault" title="Azure Key Vault">
    Create an RSA key, grant the Anthropic service principal access, then register and validate it.
  </Card>
</CardGroup>
