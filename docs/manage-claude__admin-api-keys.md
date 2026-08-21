---
title: Create an Admin API key
url: https://platform.claude.com/docs/en/manage-claude/admin-api-keys
description: Create an Admin API key for your Claude Console or Claude Enterprise organization.
---

An Admin API key authenticates every API in the **Admin** section of this guide: the [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api), [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api), [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api), [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api), [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api), and [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api). You do not need a separate key for each API. The one exception is the Admin API's service-account, federation-issuer, and federation-rule endpoints, which accept only an OAuth bearer token with the `org:admin` scope. See [Obtain an OAuth bearer token](https://platform.claude.com/docs/en/manage-claude/admin-api#oauth-bearer-token).

Where you create the key depends on which Claude product your organization uses.

## Which key do you need?

| Your organization                                           | Create the key in                                                                         | Key prefix           | Who can create it                                                                                                                                                                          | Works with                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ----------------------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Claude Console** (Claude Platform, `platform.claude.com`) | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | `sk-ant-admin01-...` | Organization members with the **admin** role                                                                                                                                               | [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api), [Usage and Cost API](https://platform.claude.com/docs/en/manage-claude/usage-cost-api), [Rate Limits API](https://platform.claude.com/docs/en/manage-claude/rate-limits-api), [Claude Code Analytics API](https://platform.claude.com/docs/en/manage-claude/claude-code-analytics-api), and the Compliance API [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed)                                                                                             |
| **Claude Enterprise** (`claude.ai`)                         | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | `sk-ant-api01-...`   | The parent organization's **primary owner** (all linked organizations). An **organization owner** can create one carrying Compliance API scopes only, restricted to their own organization | [User management](https://platform.claude.com/docs/en/manage-claude/user-management) (the Admin API's member, invite, and group endpoints), [Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api), [Claude Enterprise Analytics API](https://platform.claude.com/docs/en/manage-claude/analytics-api), and [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api), according to the [scopes](https://platform.claude.com/docs/en/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key) you select |

A key created in one organization cannot be used to manage a different organization. If your company uses both Claude Console and Claude Enterprise, create one key in each.

## Create a key for a Claude Console organization

<Steps>
  <Step title="Sign in as an organization admin">
    Only organization members with the **admin** role can create Admin API keys. See [Organization roles and permissions](https://platform.claude.com/docs/en/manage-claude/admin-api#organization-roles-and-permissions).
  </Step>

  <Step title="Open Admin keys settings">
    Go to [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).
  </Step>

  <Step title="Create the key">
    Click **Create key**, give it a name, choose a [key expiration](https://platform.claude.com/docs/en/manage-claude/authentication#key-expiration), and click **Create**. Claude Console keys do not have selectable scopes; every key carries full access to all endpoints that accept Admin API keys (the service-account and federation endpoints noted at the top of this page do not accept Admin API keys).
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
    Name the key and select the scopes you need from the [scopes table](https://platform.claude.com/docs/en/manage-claude/admin-api-keys#choose-scopes-for-a-claude-enterprise-key). The primary owner can combine scopes from different APIs (for example, `read:analytics` and `read:spend_limits`) on a single key.
  </Step>

  <Step title="Copy and store the secret">
    Copy the displayed secret (starting with `sk-ant-api01-`) and store it in your secrets manager. The full secret is shown only once.
  </Step>
</Steps>

## Choose scopes for a Claude Enterprise key

When you create a Claude Enterprise key, select every scope that the APIs you plan to call require. Scopes are fixed at creation; to add a scope later, create a new key.

| To call...                                                                                                                                                                                                                                                                                                                                                                                                                                    | Select these scopes           |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| Admin API [user management](https://platform.claude.com/docs/en/manage-claude/user-management): list and look up members and invites; read custom roles and their permissions                                                                                                                                                                                                                                                                 | `read:members`                |
| Admin API [user management](https://platform.claude.com/docs/en/manage-claude/user-management): change member roles, remove members, create and withdraw invites                                                                                                                                                                                                                                                                              | `write:members`               |
| Admin API [user management](https://platform.claude.com/docs/en/manage-claude/user-management): read groups and their members                                                                                                                                                                                                                                                                                                                 | `read:rbac_groups`            |
| Admin API [user management](https://platform.claude.com/docs/en/manage-claude/user-management): create, rename, and delete groups; add and remove group members; assign groups on invite creation                                                                                                                                                                                                                                             | `write:rbac_groups`           |
| [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api): read members' effective spend limits and increase requests                                                                                                                                                                                                                                                                                            | `read:spend_limits`           |
| [Spend Limits API](https://platform.claude.com/docs/en/manage-claude/spend-limits-api): set or clear per-user spend limits; approve or deny increase requests                                                                                                                                                                                                                                                                                 | `write:spend_limits`          |
| [Claude Enterprise Analytics API](https://platform.claude.com/docs/en/manage-claude/analytics-api): engagement, adoption, cost, and usage reports                                                                                                                                                                                                                                                                                             | `read:analytics`              |
| [Compliance API Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed): organization-wide activity events                                                                                                                                                                                                                                                                                                 | `read:compliance_activities`  |
| [Compliance API chat, file, and project endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-content-data) and [Compliance API session endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-sessions): read chats, files, projects, Cowork and Claude Code session transcripts, and [organization users](https://platform.claude.com/docs/en/manage-claude/compliance-org-data#list-organization-users) | `read:compliance_user_data`   |
| [Compliance API chat, file, and project endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-content-data): delete chats, files, and projects                                                                                                                                                                                                                                                                              | `delete:compliance_user_data` |
| [Compliance API organization endpoints](https://platform.claude.com/docs/en/manage-claude/compliance-org-data): read organization metadata and effective settings                                                                                                                                                                                                                                                                             | `read:compliance_org_data`    |
| Admin API [user management](https://platform.claude.com/docs/en/manage-claude/user-management) read endpoints and every Compliance API read endpoint, with a single read-only scope (for security-audit integrations; does not include the Spend Limits or Analytics APIs)                                                                                                                                                                    | `read:org_audit`              |

The Compliance and Analytics APIs must be enabled for your organization before keys with those scopes can be used. See [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) and [Get access to the Claude Enterprise Analytics API](https://platform.claude.com/docs/en/manage-claude/analytics-api#get-access-to-the-claude-enterprise-analytics-api).

## Use the key

Pass the key in the `x-api-key` header on every request. See each API's documentation for complete request examples.

A call that exceeds the key's scopes returns `403 Forbidden` with a message listing the scopes the key has and the scopes the endpoint needs.

## Next steps

<CardGroup cols={2}>
  <Card title="Admin API" href="https://platform.claude.com/docs/en/manage-claude/admin-api">
    Manage organization members, workspaces, and API keys.
  </Card>

  <Card title="Spend Limits API" href="https://platform.claude.com/docs/en/manage-claude/spend-limits-api">
    Set per-member spend limits and review increase requests for your Claude Enterprise organization.
  </Card>

  <Card title="Analytics APIs" href="https://platform.claude.com/docs/en/manage-claude/analytics-api">
    Report on Claude Code productivity or Claude Enterprise engagement and adoption.
  </Card>

  <Card title="Compliance API" href="https://platform.claude.com/docs/en/manage-claude/compliance-api">
    Audit activity and retrieve or delete user content across your organization.
  </Card>
</CardGroup>
