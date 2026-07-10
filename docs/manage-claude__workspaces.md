# Workspaces

Organize API keys, manage team access, and control costs with workspaces.

---

Workspaces provide a way to organize your API usage within an organization. Use workspaces to separate different projects, environments, or teams while maintaining centralized billing and administration.

## How workspaces work

Every organization has a **Default Workspace** that cannot be renamed, archived, or deleted. When you create additional workspaces, you can assign API keys, members, and resource limits to each one.

Key characteristics:

* **Workspace identifiers** use the `wrkspc_` prefix (for example, `wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ`)
* **Maximum 100 workspaces** per organization (archived workspaces don't count)
* **Default Workspace** has no ID and doesn't appear in list endpoints
* **API keys** are scoped to a single workspace and can only access resources within that workspace

### Claude Code workspace

When a member of your organization first signs in to [Claude Code](https://code.claude.com/docs/en/overview) with their Claude Console account, Anthropic automatically creates a **Claude Code** workspace in the organization and adds that member to it. Every subsequent member who signs in to Claude Code is added the same way.

The Claude Code workspace keeps Claude Code traffic separate from your other API workloads:

* Claude Code mints a per-user API key in this workspace at sign-in. You cannot create keys in it manually from the Console.
* A Claude Code key stops working if its owner is removed from the workspace or organization, unlike standard workspace keys.
* Claude Code usage is rate-limited separately, and admins can cap its share of the organization's limits under [Settings > Workspaces](/settings/workspaces).
* It is the only workspace that supports per-user monthly spend limits.

<Warning>
  Archiving the Claude Code workspace disables Claude Code sign-in through Console billing for the whole organization.
</Warning>

## Workspace roles and permissions

Members can have different roles in each workspace, allowing fine-grained access control.

| Role                        | Permissions                                                                                     |
| --------------------------- | ----------------------------------------------------------------------------------------------- |
| Workspace User              | Use the Workbench only                                                                          |
| Workspace Limited Developer | Create and manage API keys, use the API. Cannot access session tracing views or download files. |
| Workspace Developer         | Create and manage API keys, use the API                                                         |
| Workspace Admin             | Full control over workspace settings and members                                                |
| Workspace Billing           | View workspace billing information (inherited from organization billing role)                   |

### Role inheritance

* **Organization admins** automatically receive Workspace Admin access to all workspaces
* **Organization billing members** automatically receive Workspace Billing access to all workspaces
* **Organization users and developers** must be explicitly added to each workspace

<Note>
  The Workspace Billing role cannot be manually assigned. It's inherited from having the organization billing role.
</Note>

## Managing workspaces

<Note>
  Only organization admins can create workspaces. Organization users and developers must be added to workspaces by an admin.
</Note>

### Using the Console

Create and manage workspaces in the [Claude Console](/settings/workspaces).

#### Create a workspace

<Steps>
  <Step title="Open workspace settings">
    In the Claude Console, go to **Settings > Workspaces**.
  </Step>

  <Step title="Create a workspace">
    Click **Create workspace**.
  </Step>

  <Step title="Configure the workspace">
    Enter a workspace name and select a color for visual identification.
  </Step>

  <Step title="Create the workspace">
    Click **Create** to finalize.
  </Step>
</Steps>

<Tip>
  To switch between workspaces in the Console, use the **Workspaces** selector in the top-left corner.
</Tip>

#### Edit workspace details

To modify a workspace's name or color:

1. Select the workspace from the list
2. Click the ellipsis menu (**...**) and choose **Edit details**
3. Update the name or color and save your changes

<Note>
  The Default Workspace cannot be renamed or deleted.
</Note>

#### Add members to a workspace

1. Navigate to the workspace's **Members** tab
2. Click **Add to Workspace**
3. Select an organization member and assign them a [workspace role](#workspace-roles-and-permissions)
4. Confirm the addition

To remove a member, click the trash icon next to their name.

<Note>
  Organization admins and billing members cannot be removed from workspaces while they hold those organization roles.
</Note>

#### Set workspace limits

In the **Limits** tab, you can configure:

* **Rate limits:** Set limits per model tier for requests per minute, input tokens, or output tokens
* **Spend notifications:** Configure alerts when spending reaches certain thresholds

#### Archive a workspace

To archive a workspace, click the ellipsis menu (**...**) and select **Archive**. Archiving:

* Preserves historical data for reporting
* Deactivates the workspace and all associated API keys
* Cannot be undone

<Warning>
  Archiving a workspace immediately revokes all API keys in that workspace. This action cannot be undone. If you archive the [Claude Code workspace](#claude-code-workspace), members of your organization can no longer sign in to Claude Code through Console billing.
</Warning>

### Using the Admin API

Programmatically manage workspaces using the [Admin API](/docs/en/manage-claude/admin-api).

<Note>
  Admin API endpoints require an Admin API key (starting with `sk-ant-admin...`) that differs from standard API keys. See [Create an Admin API key](/docs/en/manage-claude/admin-api-keys) for how to provision one.
</Note>

```bash cURL
# Create a workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"name": "Production"}'

# List workspaces
curl "https://api.anthropic.com/v1/organizations/workspaces?limit=10&include_archived=false" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"

# Archive a workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/archive" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

For complete parameter details and response schemas, see the [Workspaces API reference](/docs/en/api/admin-api/workspaces/get-workspace).

### Managing workspace members

Add, update, or remove members from a workspace:

```bash cURL
# Add a member to a workspace
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{
    "user_id": "user_xxx",
    "workspace_role": "workspace_developer"
  }'

# Update a member's role
curl --request POST "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY" \
  --data '{"workspace_role": "workspace_admin"}'

# Remove a member from a workspace
curl --request DELETE "https://api.anthropic.com/v1/organizations/workspaces/{workspace_id}/members/{user_id}" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

For complete parameter details, see the [Workspace Members API reference](/docs/en/api/admin-api/workspace_members/get-workspace-member).

## API keys and resource scoping

API keys are scoped to a specific workspace. When you create an API key in a workspace, it can only access resources within that workspace.

Resources scoped to workspaces include:

* **Files** created through the [Files API](/docs/en/build-with-claude/files)
* **Message Batches** created through the [Batch API](/docs/en/build-with-claude/batch-processing)
* **Skills** created through the [Skills API](/docs/en/build-with-claude/skills-guide)

Some resources cannot be managed with a workspace API key:

* **[MCP tunnels](/docs/en/agents-and-tools/mcp-tunnels/overview)** are managed with a `workspace:manage_tunnels` OAuth token obtained through [Workload Identity Federation](/docs/en/manage-claude/workload-identity-federation), not a workspace API key. Tunnels are created in a workspace, and the Console **MCP tunnels** list and the Managed Agent server picker show tunnels in the current workspace only; the cap of 10 active tunnels applies organization-wide. Tunnel management requires a role with tunnel management permissions; organization developers can view but not change them.
* **Workspaces** themselves and **organization members** are managed at the organization level through the [Admin API](/docs/en/manage-claude/admin-api), which requires an Admin API key.

<Note>
  [Prompt caches](/docs/en/build-with-claude/prompt-caching) are also isolated per workspace on the Claude API, [Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws), and [Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry). On Amazon Bedrock and Google Cloud, prompt caches are isolated per organization.
</Note>

<Tip>
  To retrieve your organization's workspace IDs, use the [List Workspaces](/docs/en/api/admin-api/workspaces/list-workspaces) endpoint, or find them in the [Claude Console](/settings/workspaces).
</Tip>

## Workspace limits

You can set custom spend and rate limits for each workspace to protect against overuse and ensure fair resource distribution.

### Setting workspace limits

Workspace limits can be set lower than (but not higher than) your organization's limits:

* **Spend limits:** Cap monthly spending for a workspace
* **Rate limits:** Limit requests per minute, input tokens per minute, or output tokens per minute

<Note>
  - You cannot set limits on the Default Workspace
  - If not set, workspace limits match the organization's limits
  - Organization-wide limits always apply, even if workspace limits add up to more
</Note>

For detailed information on rate limits and how they work, see [Rate limits](/docs/en/api/rate-limits). You can also read your current organization and workspace rate limits programmatically with the [Rate Limits API](/docs/en/manage-claude/rate-limits-api).

## Usage and cost tracking

Track usage and costs by workspace using the [Usage and Cost API](/docs/en/manage-claude/usage-cost-api):

```bash cURL
curl "https://api.anthropic.com/v1/organizations/usage_report/messages?\
starting_at=2025-01-01T00:00:00Z&\
ending_at=2025-01-08T00:00:00Z&\
workspace_ids[]=wrkspc_01JwQvzr7rXLA5AGx3HKfFUJ&\
group_by[]=workspace_id&\
bucket_width=1d" \
  --header "anthropic-version: 2023-06-01" \
  --header "x-api-key: $ANTHROPIC_ADMIN_KEY"
```

Usage and costs attributed to the Default Workspace have a `null` value for `workspace_id`.

## Common use cases

### Environment separation

Create separate workspaces for development, staging, and production:

| Workspace   | Purpose                                            |
| ----------- | -------------------------------------------------- |
| Development | Testing and experimentation with lower rate limits |
| Staging     | Pre-production testing with production-like limits |
| Production  | Live traffic with full rate limits and monitoring  |

### Team or department isolation

Assign workspaces to different teams for cost allocation and access control:

* **Engineering team** with developer access
* **Data science team** with their own API keys
* **Support team** with limited access for customer tools

### Project-based organization

Create workspaces for specific projects or products to track usage and costs separately.

## Best practices

<Steps>
  <Step title="Plan your workspace structure">
    Consider how you'll organize workspaces before creating them. Think about billing, access control, and usage tracking needs.
  </Step>

  <Step title="Use meaningful names">
    Name workspaces clearly to indicate their purpose (for example, "Production - Customer Chatbot", "Dev - Internal Tools").
  </Step>

  <Step title="Set appropriate limits">
    Configure spend and rate limits to prevent unexpected costs and ensure fair resource distribution.
  </Step>

  <Step title="Audit access regularly">
    Review workspace membership periodically to ensure only appropriate users have access.
  </Step>

  <Step title="Monitor usage">
    Use the [Usage and Cost API](/docs/en/manage-claude/usage-cost-api) to track workspace-level consumption.
  </Step>
</Steps>

## FAQ

<AccordionGroup>
  <Accordion title="What's the Default Workspace?">
    Every organization has a "Default Workspace" that cannot be edited, renamed, or removed. This workspace has no ID and doesn't appear in workspace list endpoints. Usage attributed to the Default Workspace shows a `null` value for `workspace_id` in API responses.
  </Accordion>

  <Accordion title="What's the Claude Code workspace?">
    Anthropic creates the Claude Code workspace automatically the first time a member of your organization signs in to Claude Code with their Console account. It isolates Claude Code's API keys, usage, and rate limits from your other workloads. See [Claude Code workspace](#claude-code-workspace) for details.
  </Accordion>

  <Accordion title="Are there limits on workspaces?">
    Yes, you can have a maximum of 100 workspaces per organization. Archived workspaces do not count toward this limit.
  </Accordion>

  <Accordion title="How do organization roles affect workspace access?">
    Organization admins automatically get the Workspace Admin role in all workspaces. Organization billing members automatically get the Workspace Billing role. Organization users and developers must be manually added to each workspace.
  </Accordion>

  <Accordion title="Which roles can be assigned in workspaces?">
    Organization users and developers can be assigned Workspace Admin, Workspace Developer, Workspace Limited Developer, or Workspace User roles. The Workspace Billing role cannot be manually assigned; it's inherited from having the organization `billing` role.
  </Accordion>

  <Accordion title="Can organization admin or billing members' workspace roles be changed?">
    Organization admins and billing members cannot have their workspace roles changed or be removed from workspaces while they hold those organization roles (with one exception: billing members can be upgraded to a Workspace Admin role). For everyone else covered by this constraint, change their organization role first to change their workspace access.
  </Accordion>

  <Accordion title="What happens to workspace access when organization roles change?">
    If an organization admin or billing member is demoted to user or developer, they lose access to all workspaces except ones where they were manually assigned roles. When users are promoted to admin or billing roles, they gain automatic access to all workspaces.
  </Accordion>

  <Accordion title="What happens to API keys when a user is removed from a workspace?">
    API keys persist in their current state as they are scoped to the organization and workspace, not to individual users. The exception is the [Claude Code workspace](#claude-code-workspace), where each key is bound to the member who created it and stops working when that member is removed.
  </Accordion>
</AccordionGroup>

## See also

* [Admin API](/docs/en/manage-claude/admin-api)
* [Admin API reference](/docs/en/api/admin)
* [Rate limits](/docs/en/api/rate-limits)
* [Usage and Cost API](/docs/en/manage-claude/usage-cost-api)
