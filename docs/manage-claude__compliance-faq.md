# Compliance API FAQ

Answers to common questions about Compliance API access, scopes, retention, and integration.

---

<Note>
  To enable the Compliance API, see [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access).
</Note>

## Access and scopes

<AccordionGroup>
  <Accordion title="Why doesn't my parent organization appear in Claude Console when creating an Admin API key?">
    This is expected. A Claude Enterprise parent organization centralizes identity across all linked organizations; it does not carry workloads, and it does not appear in Claude Console at all. Claude Console only ever shows the Claude Console organizations linked beneath the parent.

    To call the Compliance API, you create one of two key types instead:

    * **For full Compliance API access ([Activity Feed](/docs/en/manage-claude/compliance-activity-feed) plus chats, files, projects, users, organization metadata, and organization settings),** the primary owner of the parent organization (or an organization owner, for a key restricted to their own organization only) creates a [Compliance Access Key](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) in claude.ai.
    * **For Activity Feed access only,** an organization admin in your Claude Console organization creates an [Admin API key](/docs/en/manage-claude/compliance-api-access#create-an-admin-api-key) in Claude Console. The Compliance API must already be enabled for the organization, and the admin must create the Admin API key after enablement for it to carry the `read:compliance_activities` scope.
  </Accordion>

  <Accordion title="Can I use my regular Claude API key with the Compliance API?">
    No. A Claude API key (`sk-ant-api03-...`) authenticates calls to Claude models on the Claude API; it does not authenticate calls to `/v1/compliance/*`. The Compliance API accepts only Compliance Access Keys (`sk-ant-api01-...`) and Admin API keys (`sk-ant-admin01-...`). See [Which key do you need?](/docs/en/manage-claude/compliance-api-access#which-key-do-you-need) for the full mapping.
  </Accordion>

  <Accordion title="Why does my Admin API key return 403 on chat or file endpoints?">
    Admin API keys carry a fixed `read:compliance_activities` scope, which authorizes the Activity Feed only. Every other Compliance API endpoint requires a scope that only a Compliance Access Key created in claude.ai can carry. Calling a content or directory endpoint with an Admin API key returns a 403 naming the scope that endpoint family requires: `read:compliance_user_data` for chats, files, projects, project attachments, users, and group members, and `read:compliance_org_data` for organizations, roles, groups, and effective organization settings. For example, listing chats returns the following response.

    ```json Response
    {
      "error": {
        "type": "permission_error",
        "message": "Missing required scopes. Got: ['read:compliance_activities'] Needed: ['read:compliance_user_data']"
      }
    }
    ```

    To access content endpoints, the primary owner of your parent organization (or an organization owner, for their own organization only) must [create a Compliance Access Key](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api) with `read:compliance_user_data` (and `delete:compliance_user_data` for deletes), or `read:compliance_org_data` for organization, role, group, and effective-settings endpoints. See [Handle Compliance API errors](/docs/en/manage-claude/compliance-errors#403-forbidden) for the full per-endpoint catalog.
  </Accordion>
</AccordionGroup>

## Data coverage and retention

<AccordionGroup>
  <Accordion title="How far back does the Activity Feed go?">
    The Activity Feed retains 6 years of organization activity, and new events are queryable within 1 minute of occurring. Activity Feed retention is independent of your organization's content retention policy: chat, file, and project content follows the retention rules configured for your organization (indefinite by default).
  </Accordion>

  <Accordion title="Does the Activity Feed include prompt or message content?">
    No. The Activity Feed records who did what and when (authentication, chat creation, file uploads, project changes, administrative actions, and similar resource events), but it does not capture the prompt text or model responses inside chats or messages.

    To retrieve message bodies and file contents, use the chat, message, and file endpoints with a Compliance Access Key carrying `read:compliance_user_data`. Those endpoints serve claude.ai content only; Claude Console and Claude API workloads expose administrative and resource events through the Activity Feed but do not expose prompt text or model responses through the Compliance API.
  </Accordion>

  <Accordion title="Is deleted content recoverable through the Compliance API?">
    No. Deletes performed through the Compliance API are immediate, permanent, and not recoverable. Chats that a user deleted through claude.ai are soft-deleted: they remain visible through the Compliance API with `deleted_at` populated until your organization's retention window expires or you hard-delete them through this API. Pull any content you need to retain (for legal hold or archival) before issuing a `DELETE` request.
  </Accordion>

  <Accordion title="What does the Compliance API not capture?">
    The Compliance API has known coverage boundaries: the Activity Feed records resource events but not prompt or response text, Claude Console and Claude API workloads expose no message content at all, and content removed by your retention policy or by a hard delete is not recoverable. For the full coverage boundaries and delivery contract, see [Delivery guarantees and completeness](/docs/en/manage-claude/compliance-integration-patterns#delivery-guarantees-and-completeness).
  </Accordion>
</AccordionGroup>

## Integration and pagination

<AccordionGroup>
  <Accordion title="How do I correlate Compliance API records with my SIEM?">
    Join `Activity` records to your SIEM on `actor.user_id`, `actor.email_address`, `actor.ip_address`, and `created_at`. See [Design your compliance integration](/docs/en/manage-claude/compliance-integration-patterns#correlate-with-your-siem) for the join-key table and consumption patterns.
  </Accordion>

  <Accordion title="Can one customer have multiple organizations under one parent?">
    Yes. A Claude Enterprise parent organization can have many linked organizations, including a mix of claude.ai organizations and Claude Console organizations (for example, separate production and staging Claude Console organizations). Identity, SSO, and SCIM are shared across the parent; billing, members, projects, and API keys remain separate for each organization. Compliance API enablement happens at the parent organization level and cascades to all linked organizations, and a Compliance Access Key that covers the parent organization and carries `read:compliance_org_data` can enumerate every organization beneath the parent through `GET /v1/compliance/organizations`.
  </Accordion>

  <Accordion title="Are activities returned in order, and how do I detect when I have caught up to real time?">
    Activities are returned newest first, with ties in `created_at` broken by activity ID. To catch up, walk pages forward by `before_id` until `has_more` is `false`; that final response's `first_id` is your new cursor and you have reached the present. The full loop, including initial backfill and the safety conditions on cursor persistence, is in [Cursor-driven incremental reads](/docs/en/manage-claude/compliance-integration-patterns#cursor-driven-incremental-reads).
  </Accordion>

  <Accordion title="How do I get a sandbox to test the Compliance API?">
    Set up a Claude Enterprise sandbox organization linked to a Claude Console organization under the same parent. This lets the sandbox exercise both the Activity Feed (through an Admin API key) and the chat, file, and project endpoints (through a Compliance Access Key).

    1. **Provision the Claude Enterprise organization.** Contact your Anthropic representative to set up a Claude Enterprise sandbox organization. On an existing Claude Enterprise organization, the primary owner can [enable the Compliance API directly in claude.ai](/docs/en/manage-claude/compliance-api-access#set-up-the-compliance-api).
    2. **Create the Claude Console organization.** Create a Claude Console organization yourself at `platform.claude.com` using the same email address.
    3. **Link the two organizations.** Sign in as the primary owner of the Claude Enterprise organization, go to [claude.ai > Organization settings > Identity and access](https://claude.ai/admin-settings/identity), and use **Merge Organizations** to link the two under a shared parent.

    Once linked, follow [Set up the Compliance API](/docs/en/manage-claude/compliance-api-access) to create keys and start querying. Test organizations use the same enablement process as production organizations.
  </Accordion>
</AccordionGroup>
