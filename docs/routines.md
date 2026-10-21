> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automate work with scheduled tasks

> Put Claude Code on autopilot. Create scheduled tasks, formerly routines, that run in the cloud on a schedule, on API calls, or on GitHub events.

> [!NOTE]
>
> Scheduled tasks are in research preview. Behavior, limits, and the API surface may change.

A cloud scheduled task, formerly a routine, is a saved Claude Code configuration: a prompt, one or more repositories, and a set of [connectors](/docs/en/mcp), packaged once and run automatically. Scheduled tasks execute on Anthropic-managed cloud infrastructure, or on your organization's [self-hosted environment](/docs/en/self-hosted-environments) when routed there, so they keep working when your laptop is closed.

Each scheduled task can have one or more triggers attached to it:

* **Schedule**: run on a recurring cadence like hourly, nightly, or weekly, or once at a specific future time
* **API**: trigger on demand by sending an HTTP POST to the task's own endpoint with a bearer token
* **GitHub**: run automatically in response to repository events such as pull requests or releases

A single scheduled task can combine triggers. For example, a PR review task can run nightly, trigger from a deploy script, and also react to every new PR.

A scheduled task doesn't need a schedule:

* A task with only an API trigger runs when you call its endpoint.
* A task with only a GitHub trigger runs when a matching repository event occurs.

Scheduled tasks are available on Pro, Max, Team, and Enterprise plans. Create and manage them at [claude.ai/code/routines](https://claude.ai/code/routines), or from the CLI with `/schedule`. The earlier name, routines, [still appears](#where-the-name-routines-still-appears) in the web address, the CLI, and the API.

> [!NOTE]
>
> Two other features schedule work on your machine instead of in the cloud: [Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks) and [`/loop`](/docs/en/scheduled-tasks). To choose among all three, see [Compare scheduling options](/docs/en/scheduled-tasks#compare-scheduling-options).

Team and Enterprise Owners can turn off scheduled tasks for all members with the **Scheduled tasks (Was Routines)** toggle at [**Organization settings > Capabilities > Remote sessions**](https://claude.ai/admin-settings/capabilities). When the toggle is off, existing scheduled tasks stop running and members can't create new ones.

If your Enterprise organization manages your access with [custom roles](https://support.claude.com/en/articles/13930452), you also need a role that includes the scheduled tasks permission. An Owner can add it in a role's **Remote sessions** section at [**Organization settings > Roles**](https://claude.ai/admin-settings/roles).

## Example use cases

Each example pairs a trigger type with the kind of work scheduled tasks are suited to: unattended, repeatable, and tied to a clear outcome.

* **Backlog maintenance**: a schedule trigger runs every weeknight in your repository, with your issue tracker added as a connector. The scheduled task reads issues opened since the last run, applies labels, and assigns owners based on the area of code referenced. It then posts a summary to Slack so the team starts the day with a groomed queue.
* **Alert triage**: your monitoring tool calls the scheduled task's API endpoint when an error threshold is crossed, passing the alert body as `text`. The task's prompt tells Claude to investigate the alert in the fire payload, so it pulls the stack trace and correlates it with recent commits in the repository. It then opens a draft pull request with a proposed fix and a link back to the alert. On-call reviews the PR instead of starting from a blank terminal.
* **Bespoke code review**: a GitHub trigger runs on `pull_request.opened`. The scheduled task applies your team's own review checklist and leaves inline comments for security, performance, and style issues. It also adds a summary comment so human reviewers can focus on design instead of mechanical checks.
* **Deploy verification**: your CD pipeline calls the scheduled task's API endpoint after each production deploy. The task runs smoke checks against the new build, scans error logs for regressions, and posts a go or no-go to the release channel before the deploy window closes.
* **Docs drift**: a schedule trigger runs weekly. The scheduled task scans merged PRs since the last run, flags documentation that references changed APIs, and opens update PRs against the docs repository for an editor to review.
* **Library port**: a GitHub trigger runs on `pull_request.closed` filtered to merged PRs in one SDK repository. The scheduled task ports the change to a parallel SDK in another language and opens a matching PR, keeping the two libraries in step without a human re-implementing each change.

## Create a scheduled task

Create a scheduled task from the web at [claude.ai/code/routines](https://claude.ai/code/routines), from the Desktop app, or from the CLI. All three surfaces write to the same cloud account, so a scheduled task you create in one shows up in the others immediately. In the Desktop app's **Code** tab, click **Scheduled** in the sidebar or in the sidebar's **More** menu, then **New task**, and continue with [Create from the web](#create-from-the-web).

Scheduled tasks run autonomously as full Claude Code cloud sessions. You don't choose a permission mode. The session runs shell commands, uses [skills](/docs/en/skills), and calls any connectors you include, all without stopping for approval apart from some [artifact actions](#when-a-run-publishes-an-artifact-without-asking). Outside a [project](/docs/en/claude-projects#what-threads-pick-up-from-your-repositories), those skills include the ones committed to the cloned repository.

What a scheduled task can reach is determined by:

* The repositories you select
* The [environment's](/docs/en/cloud-environments) network access and variables
* The connectors you include

Scope each of those to what the task needs.

Scheduled tasks belong to your individual claude.ai account. They are not shared with teammates, and their runs count against your account's [usage and limits](#usage-and-limits). Anything a scheduled task does through your connected GitHub identity or connectors appears as you. Commits and pull requests carry your GitHub user, and Slack messages, Linear tickets, or other connector actions use your linked accounts for those services.

### Create from the web

**1. Open the creation dialog**

Go to [claude.ai/code/routines](https://claude.ai/code/routines) and click **New task**. If a menu opens first, select **Set up manually**. The **New scheduled task** dialog opens. The menu's other option, **Create with Claude**, lets you describe the task in a chat and have Claude create it instead.

If **Repositories** and **Environment** are already showing when the dialog opens, see [how that dialog differs](#dialog-with-repositories-and-environment-in-the-main-view). Otherwise, this dialog also creates scheduled tasks for claude.ai chat. To make yours what the dialog calls a Claude Code task, select a repository or add a GitHub event or API trigger in the steps that follow. That kind of task runs Claude Code in a cloud session.

**2. Name the task and write the prompt**

Give the scheduled task a descriptive name and write the prompt Claude runs each time. The prompt is the most important part: the task runs autonomously, so the prompt must be self-contained and explicit about what to do and what success looks like. Select a model in the prompt input's model selector. Claude uses it on every run.

When a trigger fires, the session receives the saved prompt as its assignment and carries it out, rather than treating it as untrusted content that arrived mid-conversation. The trigger attests only that the prompt was stored ahead of time by an authorized session on your account. The fired prompt is therefore not live user input and can't act as approval or consent for actions during the run. Content the session fetches during the run keeps its normal handling.

**3. Select a trigger**

In the **Trigger** row, choose how the task starts. To combine several triggers, click **+** at the end of the row.

**Schedule**

Pick a preset frequency for a recurring run. See [Add a schedule trigger](#add-a-schedule-trigger) for timezone handling, late starts, custom cron intervals, and one-off runs.

**GitHub event**

Select the repository, the event to react to, and optional filters. See [Add a GitHub trigger](#add-a-github-trigger) for the full list of supported events and filter fields.

**API**

Select **API** here. When you click **Create**, the **API token** dialog shows the token once, so copy it before you close the dialog. See [Add an API trigger](#add-an-api-trigger) to copy the URL or generate a new token.

**4. Select repositories**

Expand **Advanced settings**. Under **Repository** on the **General** tab, select one or more GitHub repositories for Claude to work in.

Each repository is cloned at the start of a run. Claude creates `claude/`-prefixed branches for its changes.

**5. Select an environment**

After you select a repository, **Cloud environment** appears below it. Pick a [cloud environment](/docs/en/cloud-environments) for the task. Environments control what the cloud session has access to:

* **Network access**: set the level of internet access available during each run
* **Environment variables**: provide values Claude can use during each run. They're [visible to anyone who uses the environment](/docs/en/cloud-environments#what-carries-over-from-your-setup), so in an Anthropic-hosted environment, store keys for the APIs Claude calls during a run as [network secrets](/docs/en/cloud-environments#add-network-secrets) instead. That section also lists the requests that never get a secret
* **Setup script**: install dependencies and tools the task needs. The result is [cached](/docs/en/cloud-environments#environment-caching), so the script doesn't re-run on every session

A **Default** environment is provided with **Trusted** network access, which allows only the [default allowlist](/docs/en/cloud-environments#default-allowed-domains) of package registries, cloud provider APIs, container registries, and common development domains through the session's network. Connectors you add to the task reach their services through Anthropic's servers, so they don't need allowlist changes.

If your task needs to reach your own services directly, or a domain outside that list, edit the environment's [network access](/docs/en/cloud-environments#network-access) before running. To use a separate environment, [create one](/docs/en/cloud-environments#configure-your-environment) first.

**6. Review connectors**

Switch to the **Connectors** tab of **Advanced settings**. All of your connected [MCP connectors](/docs/en/mcp) are included by default. Remove any the task doesn't need: Claude can use every tool from an included connector, including writes, without asking for permission during a run.

**7. Create the task**

Click **Create**. The dialog closes and the new task's detail page opens. The task runs the next time one of its triggers matches. To start a run immediately, click **Run now** on the detail page.

Each run creates a new session alongside your other sessions, where you can see what Claude did, review changes, and create a pull request.

#### Dialog with Repositories and Environment in the main view

Follow the [steps to create from the web](#create-from-the-web), and fill in each field in the dialog's main view rather than under **Advanced settings**. This dialog creates only Claude Code tasks.

Select the repository before you add a GitHub event trigger, because that trigger is unavailable until a repository is selected.

### Create from the CLI

Run `/schedule` in any session to create a scheduled task conversationally. You can also pass a description directly, for a recurring task like `/schedule daily PR review at 9am` or a one-off like `/schedule clean up feature flag in one week`. Claude walks through the same information the web dialog collects, then saves the task to your account. The command is also available under the alias `/routines`.

A successful start looks like a conversation: Claude asks follow-up questions about the schedule, repositories, and prompt before saving. If Claude instead replies that you need to authenticate or that it can't connect to your remote claude.ai account, no scheduled task was created; see [Troubleshooting](#troubleshooting).

A task you create with `/schedule` has a schedule trigger. You can also add the other trigger types:

* **API trigger**: edit the task on the web at [claude.ai/code/routines](https://claude.ai/code/routines)
* **[GitHub trigger](#add-a-github-trigger)**: edit the task on the web, or ask Claude in the CLI. Adding one from the CLI requires Claude Code v2.1.225 or later

A scheduled task with no schedule trigger, such as one started only by API calls or GitHub events, has no next run time. The CLI shows none when Claude saves or updates it. Before v2.1.211, the CLI reported a next run time in the year 1 for these tasks.

## Configure triggers

A scheduled task starts when one of its triggers matches. Add or remove a task's triggers at any time in the **Trigger** row of the task's [edit dialog](#edit-and-control-scheduled-tasks).

When a task has two or more triggers, each one has a trash icon in that dialog. To remove a schedule or GitHub event trigger, click its trash icon, then **Save changes**. To remove an API trigger, [delete its token](#add-an-api-trigger) instead.

### Add a schedule trigger

A schedule trigger runs the task on a recurring cadence, or once at a specific future time. In the task's creation or edit dialog on the web, pick a preset frequency such as hourly, daily, or weekly:

* **Time zone**: times are entered in your local zone and converted automatically, so the task runs at that wall-clock time regardless of where the cloud infrastructure is located.
* **Runs on the hour**: if you schedule a run exactly on the hour, such as 9:00, it can start several minutes late. To start close to the scheduled time, pick a few minutes past the hour, for example 9:07.
* **Custom intervals**: for a custom interval such as every two hours, pick the closest preset in the dialog, then run `/schedule update` in the CLI to set a specific cron expression. The minimum interval is one hour; expressions that run more frequently are rejected.

#### Schedule a one-off run

A one-off schedule runs the task a single time at a specific timestamp. For example, use it to:

* Remind yourself later in the week
* Open a cleanup PR after a rollout finishes
* Start follow-up work after an upstream change ships

After the task runs, it turns itself off and the web UI marks it as **Completed**. To run it again, open the task's edit dialog on the web, which offers **One-time** for a one-off task, and set a new time.

Create a one-off run from the CLI by describing the time in natural language. Claude resolves the phrase against the current time and confirms the absolute timestamp before saving.

```text theme={null}
/schedule tomorrow at 9am, summarize yesterday's merged PRs
```

```text theme={null}
/schedule in 2 weeks, open a cleanup PR that removes the feature flag
```

The same local-to-UTC conversion as recurring schedules applies to one-off timestamps.

One-off runs count against the same hourly limit as other scheduled runs. See [Usage and limits](#usage-and-limits) for details.

### Add an API trigger

An API trigger gives a scheduled task a dedicated HTTP endpoint. POSTing to the endpoint with the task's bearer token starts a new session and returns a session URL. Use this to wire Claude Code into alerting systems, deploy pipelines, internal tools, or anywhere you can make an authenticated HTTP request.

Add an API trigger on the web, either while you [create the task](#create-from-the-web) or later with the steps below. You can't add an API trigger or manage its token from the CLI.

**1. Open the task for editing**

Go to [claude.ai/code/routines](https://claude.ai/code/routines), click the scheduled task you want to trigger via API, then open the menu next to its name and select **Edit**. The **Edit scheduled task** dialog opens.

**2. Add an API trigger**

In the **Trigger** row, click **+** and select **API** from the menu that opens. A panel with the **Fire URL** and **Token** for this task appears.

**3. Copy the URL and generate a token**

Copy the **Fire URL**. Click **Generate token**, then copy the token from the **Token generated** dialog immediately. The token is shown once and can't be retrieved later, so store it somewhere secure such as your alerting tool's secret store.

The API trigger takes effect as soon as you generate the token. You don't need to click **Save changes**, so close the dialog when you're done.

**4. Call the endpoint**

Send the token in the `Authorization: Bearer` header when you POST to the URL. [Trigger a scheduled task](#trigger-a-scheduled-task) shows a complete example.

Each scheduled task has its own token, scoped to triggering that task only. To turn off API access or rotate the token, [open the task's **Edit scheduled task** dialog](#edit-and-control-scheduled-tasks) again. Both controls are next to the token in the API trigger's panel and take effect immediately:

* **Turn off API access**: click **Delete token**, the trash icon next to **Regenerate**. This removes the API trigger
* **Rotate the token**: click **Regenerate**. The previous token stops working, and the **Token generated** dialog shows the new one once

#### Trigger a scheduled task

Send a POST request to the `/fire` endpoint with the bearer token in the `Authorization` header. The request body accepts an optional `text` field for run-specific context such as an alert body or a failing log, passed to the task alongside its saved prompt. The value is freeform text and is not parsed: if you send JSON or another structured payload, the task receives it as a literal string.

The `text` value doesn't reach the routine as a bare message. It arrives wrapped in a `<routine-fire-payload>` block that labels it as untrusted data and tells Claude not to follow instructions inside it unless the routine's own prompt says to. The same wrapping applies to text supplied with **Run now** in the web UI.

This means a routine's saved prompt must opt in to acting on fire text: write the prompt to reference the payload explicitly, for example "Investigate the alert described in the routine-fire-payload block", or the routine treats the text as inert context. Anyone holding the bearer token can send `text`, so the wrapper makes fire text from a leaked token arrive labeled as untrusted data rather than as direct instructions to your routine.

The example below triggers a scheduled task from a shell. The task ID and token shown are placeholders: replace them with the URL and token you copied when [adding the API trigger](#add-an-api-trigger), or the request fails with a `401` authentication error:

```bash theme={null}
curl -X POST https://api.anthropic.com/v1/claude_code/routines/trig_01ABCDEFGHJKLMNOPQRSTUVW/fire \
  -H "Authorization: Bearer sk-ant-oat01-xxxxx" \
  -H "anthropic-beta: experimental-cc-routine-2026-04-01" \
  -H "anthropic-version: 2023-06-01" \
  -H "Content-Type: application/json" \
  -d '{"text": "Sentry alert SEN-4521 fired in prod. Stack trace attached."}'
```

A successful request returns a JSON body with the new session ID and URL:

```json theme={null}
{
  "type": "routine_fire",
  "claude_code_session_id": "session_01HJKLMNOPQRSTUVWXYZ",
  "claude_code_session_url": "https://claude.ai/code/session_01HJKLMNOPQRSTUVWXYZ"
}
```

Open the session URL in a browser to watch the run in real time, review changes, or continue the conversation manually.

> [!WARNING]
>
> The `/fire` endpoint ships under the `experimental-cc-routine-2026-04-01` beta header. Request and response shapes, rate limits, and token semantics may change while the feature is in research preview. Breaking changes ship behind new dated beta header versions, and the two most recent previous header versions continue to work so that callers have time to migrate.

#### API reference

For the full API reference, including all error responses, validation rules, and field limits, see [Trigger a routine through the API](https://platform.claude.com/docs/en/api/claude-code/routines-fire) in the Claude Platform documentation.

The `/fire` endpoint is available to claude.ai users only and is not part of the Claude Platform API surface.

### Add a GitHub trigger

A GitHub trigger starts a new session automatically when a matching event occurs on a connected repository. Claude Code doesn't reuse sessions across events, so two PR updates produce two independent sessions.

> [!NOTE]
>
> GitHub webhook events are subject to per-task and per-account hourly caps. Events beyond the limit are dropped until the window resets.

The Claude GitHub App must be installed on the repository you want to subscribe to, whichever surface you configure the trigger from.

* Configure GitHub triggers from the web UI, which prompts you to install the app when it's missing. Follow the steps below to configure one on the web.
* From the CLI, install the app from the [GitHub App page](https://github.com/apps/claude) first, then ask Claude to attach a GitHub trigger to an existing scheduled task, for example `/schedule add a GitHub trigger to my nightly review for pull requests opened in acme/webapp`. The CLI path requires Claude Code v2.1.225 or later. When Claude adds the trigger, it replies with a link to the task the trigger fires.

**1. Open the task for editing**

Go to [claude.ai/code/routines](https://claude.ai/code/routines), click the scheduled task, then open the menu next to its name and select **Edit**. The **Edit scheduled task** dialog opens.

**2. Add a GitHub event trigger**

In the **Trigger** row, click **+** and select **GitHub event** from the menu that opens.

> [!NOTE]
>
> Running `/web-setup` in the CLI grants repository access for cloning, but it does not install the Claude GitHub App and does not enable webhook delivery.

**3. Configure the trigger**

Change the repository if needed, choose an event from the [supported events](#supported-events) list, and optionally add filters. Then click **Save changes** at the bottom of the dialog to apply the trigger.

#### Supported events

GitHub triggers can subscribe to either of the following event categories. Within each category you can pick a specific action, such as `pull_request.opened`, or react to all actions in the category.

| Event | Triggers when |
| :- | :- |
| Pull request | A PR is opened, closed, assigned, labeled, synchronized, or otherwise updated |
| Release | A release is created, published, edited, or deleted |

#### Filter pull requests

Use filters to narrow which pull requests start a new session. All filter conditions must match for the scheduled task to trigger. The available filter fields are:

| Filter | Matches |
| :- | :- |
| Author | PR author's GitHub username |
| Title | PR title text |
| Body | PR description text |
| Base branch | Branch the PR targets |
| Head branch | Branch the PR comes from |
| Labels | Labels applied to the PR |
| Is draft | Whether the PR is in draft state |
| Is merged | Whether the PR has been merged |

Each filter pairs a field with an operator: equals, contains, starts with, is one of, is not one of, or matches regex.

The `matches regex` operator tests the entire field value, not a substring within it. To match any title containing `hotfix`, write `.*hotfix.*`. Without the surrounding `.*`, the filter matches only a title that is exactly `hotfix` with nothing before or after. For literal substring matching without regex syntax, use the `contains` operator instead.

A few example filter combinations:

* **Auth module review**: base branch `main`, head branch contains `auth-provider`. Sends any PR that touches authentication to a focused reviewer.
* **Ready-for-review only**: is draft is `false`. Skips drafts so the task only runs when the PR is ready for review.
* **Label-gated backport**: labels include `needs-backport`. Triggers a port-to-another-branch task only when a maintainer tags the PR.

## Manage scheduled tasks

Click a scheduled task in the list to open its detail page. The detail page shows the task's repositories, connectors, prompt, schedule, API tokens, GitHub triggers, and a list of past runs.

### View and interact with runs

Click any run to open it as a full session. From there you can see what Claude did, review changes, create a pull request, or continue the conversation. Each run session works like any other session: use the dropdown menu next to the session title to rename, archive, or delete it.

> [!NOTE]
>
> A green status in the run list means the session started and exited without an infrastructure error. It does not mean the work your prompt describes succeeded. Open the run to read the transcript and confirm what Claude actually did. Blocked network requests, missing connector tools, and failures in the work itself all surface there rather than in the status indicator.

### Edit and control scheduled tasks

From the detail page you can:

* Click **Run now** to start a run immediately without waiting for the next scheduled time.
* Use the on/off switch at the top of the page to pause or resume the schedule. Paused tasks keep their configuration but don't run until you turn them back on.
* Open the menu next to the task's name and select **Edit** to change the name, prompt, repositories, environment, connectors, or any of the task's triggers. The **Edit scheduled task** dialog opens with the same layout as the [creation dialog](#create-from-the-web). To add a trigger, click **+** in the **Trigger** row. Click **Save changes** to apply your edits. API token actions take effect immediately, without **Save changes**.
* Open the same menu and select **Delete** to delete the task.

### Manage scheduled tasks from the CLI

Run `/schedule list` to see your scheduled tasks, `/schedule update` to change one, or `/schedule run` to start one immediately.

You can also ask about a scheduled task's run history, for example `/schedule why did my nightly review do nothing this morning?`. Claude lists the task's recent runs with their status and a link to [open each run on the web](#view-and-interact-with-runs). It also reads a run's log to explain what happened, including tool errors, permission denials, and the final result. Requires Claude Code v2.1.227 or later.

### Repositories and branch permissions

Scheduled tasks need GitHub access to clone repositories. When you create a scheduled task from the CLI with `/schedule`, Claude checks whether your account has GitHub access for the repository you ran it from. If it doesn't, Claude adds a setup note naming how to grant it.

> [!NOTE]
>
> See [GitHub authentication options](/docs/en/claude-code-on-the-web#github-authentication-options) for the two ways to grant access. On Team and Enterprise plans, an [Owner](/docs/en/server-managed-settings#access-control) of your Claude organization has to turn on each method before you can use it; see [Connect GitHub](/docs/en/web-quickstart#connect-github).

If your GitHub connection is missing or expired when a run is due, the scheduled task skips runs until you reconnect, for up to 72 hours. Reconnect GitHub within that window and the task resumes on its own. After 72 hours without a connection, the task turns off, and you turn it back on after reconnecting GitHub.

Each repository you add is cloned on every run. Claude starts from the repository's default branch unless your prompt specifies otherwise. If a [GitHub pull request event](#add-a-github-trigger) triggers the run and the pull request's repository is the task's first repository, that repository starts from the pull request's head commit instead.

Claude pushes its work to a branch prefixed with `claude/` unless your prompt directs it to push to another branch. To control which branches a run can push to, use branch protection rules or rulesets on GitHub. For runs on Anthropic-managed infrastructure, and for self-hosted runs that push through [Anthropic's git proxy](/docs/en/self-hosted-environments-deploy#use-the-anthropic-git-proxy), GitHub applies them to the GitHub access you connected, so a rule that access can bypass doesn't block a run's push. A self-hosted run that pushes with the git credentials your deployment provides is checked against those instead. See [Configure git](/docs/en/self-hosted-environments-deploy#configure-git).

### Connectors

Scheduled tasks can use your connected MCP connectors to read from and write to external services during each run. For example, a task that triages support requests might read from a Slack channel and create issues in Linear.

Connectors are the [claude.ai integrations](/docs/en/mcp#use-mcp-servers-from-claude-ai) on your account. MCP servers you added locally in the CLI with `claude mcp add` are stored on your machine rather than your claude.ai account, so they do not appear in the connectors list. To use one of those servers in a scheduled task:

* **As a connector**: add it as a connector at [claude.ai/customize/connectors](https://claude.ai/customize/connectors)
* **In the repository**: for a scheduled task with one repository outside a [project](/docs/en/claude-projects#what-threads-pick-up-from-your-repositories), you can instead declare the server in a committed [`.mcp.json`](/docs/en/mcp#project-scope). A scheduled task in a project doesn't load `.mcp.json`, so add the server as a connector

When you create a scheduled task, all of your currently connected connectors are included by default. Remove any that aren't needed to limit which tools Claude has access to during the run. You can also add connectors directly from the task's creation or edit dialog.

To manage or add connectors outside of that dialog, visit [claude.ai/customize/connectors](https://claude.ai/customize/connectors) or use `/schedule update` in the CLI.

### When a run publishes an artifact without asking

When a scheduled task's schedule or **Run now** starts a run, Claude can publish a new [artifact](/docs/en/artifacts) without asking. The new artifact is visible only to you until you [share it](/docs/en/artifacts#share-an-artifact). If the publish declares runtime capabilities for the page, such as [connector calls](/docs/en/artifacts#pull-live-data-with-mcp-connectors) or [file downloads](/docs/en/artifacts#offer-a-file-download), Claude asks first.

In those runs, Claude republishes an existing artifact without asking only when all of these hold:

* You can edit the artifact and it belongs to your own organization
* If the publish carries more than the page, such as supporting files, you own the artifact
* The artifact isn't shared publicly
* If the artifact is shared with specific people or your organization, its viewers don't automatically see each new version
* The publish doesn't force over a newer version
* The publish doesn't declare runtime capabilities for the page
* The existing page holds no grant that reaches beyond the page, such as [connector calls](/docs/en/artifacts#pull-live-data-with-mcp-connectors)

In every other case, including a run that an API or GitHub trigger starts, Claude asks first.

When a scheduled task's job is to keep a page current, give it an artifact you already published.

### Environments and network access

Each scheduled task uses a [cloud environment](/docs/en/cloud-environments) that controls network access, environment variables, and setup scripts. The task inherits the environment's network policy on every run.

The **Default** environment uses **Trusted** network access, which allows only the [default allowlist](/docs/en/cloud-environments#default-allowed-domains) through the session's network. Requests on that path to hosts outside the allowlist fail with `403` and `x-deny-reason: host_not_allowed`. MCP connector traffic is routed through Anthropic's servers rather than that path, so the connectors you add to the task work without adding their hosts to **Allowed domains**. Remove any connectors you don't need under [Connectors](#connectors).

To allow additional domains on one of your own environments, follow these steps. An [organization-shared environment](/docs/en/cloud-environments#organization-shared-environments) opens read-only here, so an Owner changes its network access from the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings) instead.

**1. Open the task for editing**

Go to [claude.ai/code/routines](https://claude.ai/code/routines), click the scheduled task, then open the menu next to its name and select **Edit**. The **Edit scheduled task** dialog opens.

**2. Open the environment selector**

Go to **Advanced settings > General > Cloud environment**, expanding **Advanced settings** first if it's collapsed. Click the cloud icon showing your environment's name, such as **Default**.

**3. Open the environment settings**

Hover over the environment in the list and click the settings icon that appears on the right.

**4. Change the network access level**

In the **Edit cloud environment** dialog, change **Network access** to **Custom** and enter your domains in **Allowed domains**. Check **Also include default list of common package managers** to keep the [default allowlist](/docs/en/cloud-environments#default-allowed-domains) alongside your custom domains. Select **Full** instead for unrestricted access.

**5. Save**

Click **Save changes** in the **Edit cloud environment** dialog, then close the **Edit scheduled task** dialog behind it. The new policy applies from the next run.

See [Network access](/docs/en/cloud-environments#network-access) for details on access levels and the default allowlist.

## Usage and limits

Scheduled tasks draw down subscription usage the same way interactive sessions do. See your current consumption at [claude.ai/settings/usage](https://claude.ai/settings/usage).

Separately from subscription usage, each way of starting a run has an hourly limit:

| Action | Limit | Counted for | Over the limit |
| :- | :- | :- | :- |
| Scheduled runs, including one-off runs | 100 per hour | Your account | The run waits until the limit resets |
| **Run now**, API fires, and setting a one-off task to run again | 30 per hour | Each scheduled task, one count shared by all three | The action fails until the limit resets |
| **Run now** and setting a one-off task to run again | 100 per hour | Your account | Same |
| API fires | 100 per hour | Your account, counted separately from **Run now** | Same |
| GitHub events | See [Add a GitHub trigger](#add-a-github-trigger) | | |

None of these hourly limits has overage.

When a scheduled task hits your subscription usage limit, organizations with usage credits turned on can keep running scheduled tasks on metered overage. Without usage credits, additional runs are rejected until your usage window resets. Turn on usage credits at [claude.ai/settings/usage](https://claude.ai/settings/usage). On Team and Enterprise plans, an admin turns them on for the organization at [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage).

While your subscription is paused, your scheduled tasks are put on hold and don't run. Once your subscription is active again, turn them back on.

## Where the name routines still appears

Scheduled tasks were previously called routines, and these places keep the earlier name. Each one refers to the same feature:

* **Web address**: `claude.ai/code/routines`
* **CLI**: the `/routines` alias for `/schedule`, the command's description, and Claude's replies while it sets up a task
* **API**: the `/fire` endpoint path, its beta header, its response `type`, the `<routine-fire-payload>` tag, and the [Trigger a routine through the API](https://platform.claude.com/docs/en/api/claude-code/routines-fire) reference page
* **Organization settings**: the **Scheduled tasks (Was Routines)** toggle

## Troubleshooting

### `/schedule` returns "Unknown command"

The CLI hides `/schedule` when one of its requirements isn't met: the command menu shows `No commands match "/schedule"` while you type. Submitting it returns `Unknown command: /schedule`, except in the cases below that note a different answer.

The cause is usually one of the following:

* You are authenticated with a Console API key, an [Anthropic profile or federation credential](/docs/en/authentication#anthropic-profiles-and-federation-credentials), or a cloud provider such as Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. `/schedule` requires a claude.ai subscription login. With a Console API key or a profile, and feature-flag fetching enabled, submitting `/schedule` instead shows `/schedule is available with Claude for Enterprise — ask your admin about migrating from API-key access`. With a cloud-provider login, you still see `Unknown command: /schedule`. If `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` is set in your shell, or `apiKeyHelper` is set in `settings.json`, remove it first, since these take precedence over a claude.ai login. A profile or federation credential takes precedence too, so switch that off as well
* You are fully signed out, with no API key or other credential. With feature-flag fetching enabled, submitting `/schedule` shows `/schedule requires a claude.ai subscription. Run /login to sign in with your claude.ai account.` Before v2.1.268, a signed-out session showed the same Claude for Enterprise message as a Console API key
* You are inside a cloud session, where submitting `/schedule` answers that the command isn't available in that environment. Manage scheduled tasks from the [web UI](https://claude.ai/code/routines) instead
* Your organization's policy disables [cloud sessions](/docs/en/claude-code-on-the-web), which scheduled tasks require. In this case, submitting `/schedule` answers [`Cloud sessions are disabled by your organization's policy`](/docs/en/errors#cloud-sessions-are-disabled-by-your-organizations-policy) instead. Before v2.1.268, it returned `Unknown command: /schedule`
* An Owner [turned off scheduled tasks](#routines-are-disabled-by-your-organizations-policy) for your Team or Enterprise organization. Before v2.1.227, the command still appeared in this case, and claude.ai rejected the task when Claude tried to create or run it
* Your Enterprise organization manages your access with [custom roles](https://support.claude.com/en/articles/13930452), and none of your roles includes the scheduled tasks permission under **Remote sessions**. Ask an Owner to add it to one of your roles

If the cause is your CLI sign-in or being inside a cloud session, you can still create and manage scheduled tasks at [claude.ai/code/routines](https://claude.ai/code/routines). You need a Pro, Max, Team, or Enterprise account there. If scheduled tasks or cloud sessions are off for your organization or missing from your roles, you can't create them on the web either.

### "Routines are disabled by your organization's policy"

An Owner in your Team or Enterprise organization has likely turned off the **Scheduled tasks (Was Routines)** toggle at [**Organization settings > Capabilities > Remote sessions**](https://claude.ai/admin-settings/capabilities). On Claude Code v2.1.227 or later, the same toggle also hides `/schedule` in the CLI. This is a server-side organization setting, so it cannot be overridden from your local configuration. Ask an Owner to turn scheduled tasks back on for your organization.

## Related resources

* [`/loop` and in-session scheduling](/docs/en/scheduled-tasks): schedule local tasks within an open CLI session
* [Desktop scheduled tasks](/docs/en/desktop-scheduled-tasks): local scheduled tasks that run on your machine with access to local files
* [Cloud environments](/docs/en/cloud-environments): configure network access, environment variables, and setup scripts for cloud sessions
* [Projects](/docs/en/claude-projects): ongoing work Claude coordinates across parallel cloud sessions; scheduled tasks created from a project appear on its **Scheduled tasks** tab
* [MCP connectors](/docs/en/mcp): connect external services like Slack, Linear, and Google Drive
* [GitHub Actions](/docs/en/github-actions): run Claude in your CI pipeline on repository events
