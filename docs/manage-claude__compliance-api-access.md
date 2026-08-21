---
title: Set up the Compliance API
url: https://platform.claude.com/docs/en/manage-claude/compliance-api-access
description: Enable the Compliance API for your organization, then create a Compliance Access Key (with scoped permissions) or an Admin API key, and learn which to use.
---

<Note>
  Claude Enterprise organizations and eligible standalone Claude Console organizations have self-service access to the Compliance API. This page describes how to enable the Compliance API for your organization and create API keys.
</Note>

<Check>
  **Required role:** organization admin (Claude Console), or primary owner or organization owner (claude.ai).
</Check>

The Compliance API uses two key types, and which one you create depends on which Claude product your organization uses. Primary owners and organization owners create Compliance Access Keys in claude.ai; these keys unlock the full Compliance API. A primary owner's key can cover every organization under the parent organization; an organization owner's key covers their own organization only. Organization admins create Admin API keys in Claude Console; these keys unlock the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) only.

## Which key do you need?

| Key type                                       | Created in                                                                                | Used for                                                                                                                        | Works with the Compliance API? |
| ---------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| **Compliance Access Key** (`sk-ant-api01-...`) | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | Activity Feed, chats, files, projects, Cowork and Claude Code sessions, users, organization metadata, and organization settings | Yes (all endpoints)            |
| **Admin API key** (`sk-ant-admin01-...`)       | [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys) | The [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api) and the Compliance API Activity Feed               | Activity Feed only             |
| **Analytics API key**                          | [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access)    | The Claude Enterprise Analytics API (see [Analytics APIs](https://platform.claude.com/docs/en/manage-claude/analytics-api))     | No                             |
| **Claude API key** (`sk-ant-api03-...`)        | [Claude Console > Settings > API keys](https://platform.claude.com/settings/keys)         | Calling Claude models through the [Claude API](https://platform.claude.com/docs/en/api/overview)                                | No                             |

A Claude Enterprise tenant has one **parent organization** that centralizes identity, SSO, and SCIM for every workload organization beneath it. These workload organizations are the parent's **linked organizations**.

<Warning>
  **Claude Enterprise parent organizations do not appear in Claude Console (`platform.claude.com`).** The parent carries no workloads, no Claude API keys, and no Admin API keys. Create Compliance Access Keys in claude.ai **Organization settings**, not in Claude Console.
</Warning>

## Set up the Compliance API

Setup is one flow: enable the Compliance API for your organization, then create a Compliance Access Key in claude.ai. A Claude Console organization instead [creates an Admin API key](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#create-an-admin-api-key) after enablement; Admin API keys reach the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) only.

<Warning>
  A Compliance Access Key with `read:compliance_user_data` can read every chat, file, project, and Cowork and Claude Code session transcript in every linked organization, including content the primary owner has not seen. A key with `delete:compliance_user_data` can permanently delete chats, files, and projects. Treat Compliance Access Keys like production database credentials: store them in a secrets manager, never in source control or SIEM forwarder configuration.
</Warning>

<Steps>
  <Step title="Enable the Compliance API">
    Where you enable the Compliance API depends on how your organization is set up:

    * **Claude Enterprise organizations:** The primary owner enables the Compliance API at [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Enablement happens at the parent organization level and cascades to every linked organization, both claude.ai and Claude Console.
    * **Standalone Claude Console organizations:** An organization admin turns on the **Compliance API** toggle at [Claude Console > Settings > Security](https://platform.claude.com/settings/security). Enablement is self-service for eligible organizations, and the change takes effect immediately. If the **Compliance API** section is not visible, you do not have the admin role, your organization is linked to a parent organization (the Compliance API is enabled from the parent organization instead), or your organization is not eligible for self-service enablement; contact your account team or [Anthropic support](https://support.claude.com) if you are not sure which applies.
    * **Claude Console organizations linked to a parent organization:** There is nothing to turn on in Claude Console. Ask the primary owner of your parent organization to enable the Compliance API in claude.ai, or contact your account team.

    <Warning>
      **Turning the Compliance API off stops activity recording.** An organization admin can turn the Compliance API off at any time with the same **Compliance API** toggle that turns it on. While the Compliance API is off, no activity events are recorded for your organization, so the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) receives no new events. If your organization is enrolled in [Access Transparency](https://platform.claude.com/docs/en/manage-claude/access-transparency), turning the Compliance API off also stops Access Transparency event delivery. Activity that is not recorded while the Compliance API is off cannot be recovered later. Turning the Compliance API back on resumes recording from that point forward; activity that was already recorded is not deleted. For Claude Enterprise organizations, the Compliance API setting in claude.ai also governs transcript capture for Cowork and Claude Code sessions on users' machines (local sessions): capture starts when the Compliance API is enabled and stops while it is off, and transcript content from sessions that run while it is off is not captured and cannot be recovered later.
    </Warning>

    A standalone Claude Console organization uses Admin API keys rather than Compliance Access Keys: after enablement, skip the remaining steps and [create a new Admin API key](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#create-an-admin-api-key) instead. The remaining steps provision Compliance Access Keys, which are available only to organizations that are part of a Claude Enterprise tenant.
  </Step>

  <Step title="Decide the key's scope">
    A key's access is set when it is created. Decide which organizations the key covers:

    * A key for the **parent organization** can access every organization under the parent organization.
    * A key for a **single organization** can access that organization only.
  </Step>

  <Step title="Sign in with the matching role">
    Sign in to claude.ai. The primary owner of the parent organization can create a key with either scope. An organization owner can create a key restricted to their own organization only.

    If the **API** page described in the next step is not visible, or compliance scopes are unavailable when creating a key, either your role cannot create Compliance Access Keys, or the Compliance API has not been enabled for your organization yet (return to the first step).
  </Step>

  <Step title="Open API settings">
    Go to [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access) and find the **Keys** section.
  </Step>

  <Step title="Create the key">
    Click **Create key**, name the key, and select one or more scopes from the following table. Click **Create**.

    | Scope                         | Grants                                                                                                                                                                                                                    |
    | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `read:compliance_activities`  | Read the Activity Feed. A key covering the parent organization reads events for the parent organization and all linked organizations.                                                                                     |
    | `read:compliance_user_data`   | Read user chats, messages, files, projects, Cowork and Claude Code sessions and their transcripts, organization users, and group members                                                                                  |
    | `delete:compliance_user_data` | Delete user chats, files, and projects                                                                                                                                                                                    |
    | `read:compliance_org_data`    | Read organization metadata (names, types, roles, and groups) and the effective settings in force for organizations under the parent organization. User listings and group membership require `read:compliance_user_data`. |

    Choose the smallest scope set that your integration needs:

    * An audit pipeline that reads the Activity Feed only needs `read:compliance_activities`.
    * An eDiscovery tool that reads chats and files but never deletes them does not need `delete:compliance_user_data`.
    * If your workflow both reads and deletes, use **two keys** with separate scopes so a leaked read key cannot delete data.

    Compliance Access Key scopes are immutable after creation. To change scopes, create a new key with the scopes you want, then delete the old one.
  </Step>

  <Step title="Copy and store the secret">
    Copy the displayed secret key (starting with `sk-ant-api01-`) and store it in your secrets manager. The full secret is displayed only once.
  </Step>

  <Step title="Export the key for the examples in this guide">
    Set the key as an environment variable so the shell samples in this guide can read it:

    ```bash
    export ANTHROPIC_COMPLIANCE_ACCESS_KEY=sk-ant-api01-...
    ```
  </Step>
</Steps>

## Create an Admin API key

<Note>
  The Compliance API must already be [enabled for your Claude Console organization](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) before an Admin API key can call the Activity Feed.
</Note>

Follow the steps in [Create an Admin API key](https://platform.claude.com/docs/en/manage-claude/admin-api-keys#create-a-key-for-a-claude-console-organization), then set the key as an environment variable:

```bash
export ANTHROPIC_ADMIN_KEY=sk-ant-admin01-...
```

The distinct variable name keeps the Admin API key from overwriting a Compliance Access Key if you provision both. The cURL examples in this guide read the key from `$ANTHROPIC_COMPLIANCE_ACCESS_KEY`; substitute `$ANTHROPIC_ADMIN_KEY` when calling the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) with an Admin API key.

Admin API keys carry the `read:compliance_activities` scope only if the Compliance API was enabled for the organization at the time the key was created; see [Set up the Compliance API](https://platform.claude.com/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api). They cannot be granted any other Compliance API scope, so calls to any endpoint other than the Activity Feed return [403 Forbidden](https://platform.claude.com/docs/en/manage-claude/compliance-errors#403-forbidden).

For the same key's role in managing your Claude Console organization, see [Admin API](https://platform.claude.com/docs/en/manage-claude/admin-api).

## Check your key's scopes

To inspect the scopes on a key you already have, use one of the following signals.

* **Key prefix.** `sk-ant-admin01-` is an Admin API key (carries `read:compliance_activities` only, subject to the enablement timing in the preceding section). `sk-ant-api01-` is a Compliance Access Key; its scopes are the subset you selected at creation.
* **Settings UI.** Open the **Keys** section in [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access), or the **Admin keys** section in [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys), and read the **Scopes** column for the key.
* **Error responses.** A call that exceeds the key's scopes returns a 403 with a message in the format `Missing required scopes. Got: [<scopes the key carries>] Needed: [<scopes the endpoint requires>]`. See [Handle Compliance API errors](https://platform.claude.com/docs/en/manage-claude/compliance-errors#403-forbidden) for the full error catalog.

```json
{
  "error": {
    "type": "permission_error",
    "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
  }
}
```

## Manage and rotate keys

Delete a Compliance Access Key from the same **Keys** table where you created it: go to [claude.ai > Organization settings > API](https://claude.ai/admin-settings/api-access). Delete an Admin API key from [Claude Console > Settings > Admin keys](https://platform.claude.com/settings/admin-keys).

Deleting a key takes effect on the next request: there is no grace period. Compliance Access Keys do not expire on their own.

To rotate a key without an outage:

1. Create a new key with the same scopes.
2. Update your integration to use the new key.
3. Verify the integration succeeds with the new key.
4. Delete the old key.

Pagination cursors stored before a rotation remain valid: cursors are scoped to the organization, not the key.

If a Compliance Access Key leaks, delete it immediately, audit the [Activity Feed](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed) for `compliance_api_accessed` activities by the compromised key, and rotate any downstream credentials that the leaked key could reach. Pass `activity_types[]=compliance_api_accessed` to scope the query, then in your client, keep the activities whose `actor.type` is `api_actor` and whose `actor.api_key_id` matches the compromised key; see [Understand the Activity object](https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed#understand-the-activity-object) for the actor schema.

## Next steps

<CardGroup cols={2}>
  <Card title="Query the Activity Feed" href="https://platform.claude.com/docs/en/manage-claude/compliance-activity-feed">
    Read organization-wide activity events with any key that has `read:compliance_activities`.
  </Card>

  <Card title="Retrieve and delete chats, files, and projects" href="https://platform.claude.com/docs/en/manage-claude/compliance-content-data">
    Use a Compliance Access Key with `read:compliance_user_data` to retrieve claude.ai chats, files, and projects, and `delete:compliance_user_data` to delete them.
  </Card>

  <Card title="Retrieve session transcripts" href="https://platform.claude.com/docs/en/manage-claude/compliance-sessions">
    Use a Compliance Access Key with `read:compliance_user_data` to list the sessions your users run in Claude apps and agents, such as Cowork and Claude Code, and retrieve their transcripts.
  </Card>
</CardGroup>
