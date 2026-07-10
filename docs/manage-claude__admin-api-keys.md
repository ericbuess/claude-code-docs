# Create an Admin API key

Create an Admin API key for your Claude Console or Claude Enterprise organization.

---

Every API in the **Admin** section of this guide (the [Admin API](/docs/en/manage-claude/admin-api), [Analytics APIs](/docs/en/manage-claude/analytics-api), [Compliance API](/docs/en/manage-claude/compliance-api), [Spend Limits API](/docs/en/manage-claude/spend-limits-api), [Usage and Cost API](/docs/en/manage-claude/usage-cost-api), and [Rate Limits API](/docs/en/manage-claude/rate-limits-api)) is authenticated with an Admin API key. You do not need a separate key for each API.

Where you create the key depends on which Claude product your organization uses.

## Which key do you need?

| Your organization                                           | Create the key in                                                                         | Key prefix           | Who can create it                                                                                                                                                                          | Works with                                                                                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Console** (Claude Platform, `platform.claude.com`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | `sk-ant-admin01-...` | Organization members with the **admin** role                                                                                                                                               | [Admin API](/docs/en/manage-claude/admin-api), [Usage and Cost API](/docs/en/manage-claude/usage-cost-api), [Rate Limits API](/docs/en/manage-claude/rate-limits-api), [Claude Code Analytics API](/docs/en/manage-claude/claude-code-analytics-api), and the Compliance API [Activity Feed](/docs/en/manage-claude/compliance-activity-feed) |
| **Claude Enterprise** (`claude.ai`)                         | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | `sk-ant-api01-...`   | The parent organization's **primary owner** (all linked organizations). An **organization owner** can create one carrying Compliance API scopes only, restricted to their own organization | [Compliance API](/docs/en/manage-claude/compliance-api), [Claude Enterprise Analytics API](/docs/en/manage-claude/analytics-api), and [Spend Limits API](/docs/en/manage-claude/spend-limits-api), according to the [scopes](#choose-scopes-for-a-claude-enterprise-key) you select                                                           |

A key created in one organization cannot be used to manage a different organization. If your company uses both Claude Console and Claude Enterprise, create one key in each.

## Create a key for a Claude Console organization

<Steps>
  <Step title="Sign in as an organization admin">
    Only organization members with the **admin** role can create Admin API keys. See [Organization roles and permissions](/docs/en/manage-claude/admin-api#organization-roles-and-permissions).
  </Step>

  <Step title="Open Admin keys settings">
    Go to [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).
  </Step>

  <Step title="Create the key">
    Click **Create key**, give it a name, choose an [expiration](/docs/en/manage-claude/authentication#key-expiration), and click **Create**. Claude Console keys do not have selectable scopes; every key carries full Admin API access.
  </Step>

  <Step title="Copy and store the secret">
    Copy the displayed secret (starting with `sk-ant-admin01-`) and store it in your secrets manager. The full secret is shown only once.
  </Step>
</Steps>

## Create a key for a Claude Enterprise organization

<Steps>
  <Step title="Sign in as the primary owner or an organization owner">
    The **primary owner** of the Claude Enterprise parent organization can create a key that can access every linked organization, or one restricted to a single organization. An **organization owner** can create a key with Compliance API scopes only, restricted to their own organization.
  </Step>

  <Step title="Open API settings">
    Go to [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) and find the **Keys** section.
  </Step>

  <Step title="Click + Create key">
    Name the key and select the scopes you need from the [scopes table](#choose-scopes-for-a-claude-enterprise-key). The primary owner can combine scopes from different APIs (for example, `read:analytics` and `read:spend_limits`) on a single key.
  </Step>

  <Step title="Copy and store the secret">
    Copy the displayed secret (starting with `sk-ant-api01-`) and store it in your secrets manager. The full secret is shown only once.
  </Step>
</Steps>

## Choose scopes for a Claude Enterprise key

When you create a Claude Enterprise key, select every scope that the APIs you plan to call require. Scopes are fixed at creation; to add a scope later, create a new key.

| To call...                                                                                                                             | Select these scopes           |
| -------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| [Spend Limits API](/docs/en/manage-claude/spend-limits-api): read members' effective spend limits and increase requests                | `read:spend_limits`           |
| [Spend Limits API](/docs/en/manage-claude/spend-limits-api): set or clear per-user spend limits; approve or deny increase requests     | `write:spend_limits`          |
| [Claude Enterprise Analytics API](/docs/en/manage-claude/analytics-api): engagement, adoption, cost, and usage reports                 | `read:analytics`              |
| [Compliance API Activity Feed](/docs/en/manage-claude/compliance-activity-feed): organization-wide activity events                     | `read:compliance_activities`  |
| [Compliance API content endpoints](/docs/en/manage-claude/compliance-content-data): read chats, files, projects, and users             | `read:compliance_user_data`   |
| [Compliance API content endpoints](/docs/en/manage-claude/compliance-content-data): delete chats, files, and projects                  | `delete:compliance_user_data` |
| [Compliance API organization endpoints](/docs/en/manage-claude/compliance-org-data): read organization metadata and effective settings | `read:compliance_org_data`    |

The Compliance and Analytics APIs must be enabled for your organization before keys with those scopes can be used. See [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) and [Analytics APIs](/docs/en/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).

## Use the key

Pass the key in the `x-api-key` header on every request. See each API's documentation for complete request examples.

A call that exceeds the key's scopes returns `403 Forbidden` with a message listing the scopes the key has and the scopes the endpoint needs.

## Next steps

<CardGroup cols={2}>
  <Card title="Admin API" href="/docs/en/manage-claude/admin-api">
    Manage organization members, workspaces, and API keys.
  </Card>

  <Card title="Spend Limits API" href="/docs/en/manage-claude/spend-limits-api">
    Set per-member spend limits and review increase requests for your Claude Enterprise organization.
  </Card>

  <Card title="Analytics APIs" href="/docs/en/manage-claude/analytics-api">
    Report on Claude Code productivity or Claude Enterprise engagement and adoption.
  </Card>

  <Card title="Compliance API" href="/docs/en/manage-claude/compliance-api">
    Audit activity and retrieve or delete user content across your organization.
  </Card>
</CardGroup>
