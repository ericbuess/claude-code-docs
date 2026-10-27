> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automate work with scheduled tasks

> Put Claude Code on autopilot. Create scheduled tasks, formerly routines, that run in the cloud on a schedule, on API calls, or on GitHub events.

> [!NOTE]
>
> Scheduled tasks are in research preview. Behavior, limits, and the API surface may change.

A cloud scheduled task, formerly a routine, is a saved Claude Code configuration: a prompt, one or more repositories, and a set of [connectors](https://code.claude.com/docs/en/mcp.md), packaged once and run automatically. Scheduled tasks execute on Anthropic-managed cloud infrastructure, or on your organization's [self-hosted environment](https://code.claude.com/docs/en/self-hosted-environments) when routed there, so they keep working when your laptop is closed.

Each scheduled task can have one or more triggers attached to it:

* **Schedule**: run on a recurring cadence like hourly, nightly, or weekly, or once at a specific future time
* **API**: trigger on demand by sending an HTTP POST to the task's own endpoint with a bearer token
* **GitHub**: run automatically in response to repository events such as pull requests or releases

A single scheduled task can combine triggers. For example, a PR review task can run nightly, trigger from a deploy script, and also react to every new PR.

A scheduled task doesn't need a schedule:

* A task with only an API trigger runs when you call its endpoint.
* A task with only a GitHub trigger runs when a matching repository event occurs.

Scheduled tasks are available on Pro, Max, Team, and Enterprise plans. Create and manage them at [claude.ai/code/routines](https://claude.ai/code/routines), or from the CLI with `/schedule`. The earlier name, routines, [still appears](#where-the-name-routines-still-appears).

> [!NOTE]
>
> Two other features schedule work on your machine instead of in the cloud: [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks.md) and [`/loop`](https://code.claude.com/docs/en/scheduled-tasks). To choose among all three, see [Compare scheduling options](https://code.claude.com/docs/en/scheduled-tasks.md#compare-scheduling-options).

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

Scheduled tasks run autonomously as full Claude Code cloud sessions. The session runs shell commands, uses [skills](https://code.claude.com/docs/en/skills.md), and calls any connectors you include. Outside a [project](https://code.claude.com/docs/en/claude-projects.md#what-threads-pick-up-from-your-repositories)'s threads, those skills include the ones committed to the cloned repository. You don't choose a permission mode when you create the task: see [Permission prompts during a run](#permission-prompts-during-a-run) for when a run stops to wait for you.

What a scheduled task can reach is determined by:

* The repositories you select
* The [environment's](https://code.claude.com/docs/en/cloud-environments.md) network access and variables
* The connectors you include

Scope each of those to what the task needs.

Scheduled tasks belong to your individual claude.ai account. They are not shared with teammates, and their runs count against your account's [usage and limits](#usage-and-limits). Anything a scheduled task does through your connected GitHub identity or connectors appears as you. Commits and pull requests carry your GitHub user, and Slack messages, Linear tickets, or other connector actions use your linked accounts for those services.

### Create from the web

**1. Open the creation dialog**

Go to [claude.ai/code/routines](https://claude.ai/code/routines) and click **New task** to open the **New scheduled task** dialog. Check for these screens before you continue:

* If the button reads **New routine** instead of **New task**, click **New routine** and continue with [Full-page form](#full-page-form).
* In the Desktop app, if a menu with **Local** and **Cloud** opens, go to [Full-page form](#full-page-form).
* If a menu opens with **Create with Claude** and **Set up manually**, select **Set up manually** to open the dialog. **Create with Claude** lets you describe the task in a chat and have Claude create it instead.
* If a full page opens in place of the dialog, go to [Full-page form](#full-page-form).

If **Repositories** and **Environment** are already showing when the dialog opens, see [how that dialog differs](#dialog-with-repositories-and-environment-in-the-main-view). Otherwise, this dialog also creates scheduled tasks for claude.ai chat. To make yours what the dialog calls a Claude Code task, select a repository or add a GitHub event or API trigger in the steps that follow. That kind of task runs Claude Code in a cloud session.

**2. Name the task and write the prompt**

Give the scheduled task a descriptive name and write the prompt Claude runs each time. The prompt is the most important part: the task runs autonomously, so the prompt must be self-contained and explicit about what to do and what success looks like.

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

After you select a repository, **Cloud environment** appears below it. Pick a [cloud environment](https://code.claude.com/docs/en/cloud-environments.md) for the task. Environments control what the cloud session has access to:

* **Network access**: set the level of internet access available during each run
* **Environment variables**: provide values Claude can use during each run. They're [visible to anyone who uses the environment](https://code.claude.com/docs/en/cloud-environments.md#what-carries-over-from-your-setup), so in an Anthropic-hosted environment, store keys for the APIs Claude calls during a run as [network secrets](https://code.claude.com/docs/en/cloud-environments.md#add-network-secrets) instead. That section also lists the requests that never get a secret
* **Setup script**: install dependencies and tools the task needs. The result is [cached](https://code.claude.com/docs/en/cloud-environments.md#environment-caching), so the script doesn't re-run on every session

A **Default** environment is provided with **Trusted** network access, which allows only the [default allowlist](https://code.claude.com/docs/en/cloud-environments.md#default-allowed-domains) of package registries, cloud provider APIs, container registries, and common development domains through the session's network. Connectors you add to the task reach their services through Anthropic's servers, so they don't need allowlist changes.

If your task needs to reach your own services directly, or a domain outside that list, edit the environment's [network access](https://code.claude.com/docs/en/cloud-environments.md#network-access) before running. To use a separate environment, [create one](https://code.claude.com/docs/en/cloud-environments.md#configure-your-environment) first.

**6. Select a model and effort level**

Select a model in the prompt input's model selector for Claude to use on every run. For a Claude Code task, if the model offers [effort levels](https://code.claude.com/docs/en/model-config.md#adjust-effort-level), **Effort** in the same selector shows the current level. To change it, select another level. The selector's **Default** option offers no levels.

**7. Review connectors**

Switch to the **Connectors** tab of **Advanced settings**. All of your connected [MCP connectors](https://code.claude.com/docs/en/mcp.md) are included by default. Remove any the task doesn't need: Claude can use an included connector during a run, including writes. For when a run stops to ask you first, see [Permission prompts during a run](#permission-prompts-during-a-run).

**8. Create the task**

Click **Create**. The dialog closes and the new task's detail page opens. The task runs the next time one of its triggers matches. To start a run immediately, click **Run now** on the detail page.

To see what a run did, click it in the **History** list on the detail page. The run [opens as a full session](#view-and-interact-with-runs), a new one for each run, where you can see what Claude did, review changes, and create a pull request.

#### Dialog with Repositories and Environment in the main view

Follow the [steps to create from the web](#create-from-the-web), and fill in each field in the dialog's main view rather than under **Advanced settings**. This dialog creates only Claude Code tasks.

Select the repository before you add a GitHub event trigger, because that trigger is unavailable until a repository is selected.

#### Full-page form

In the Desktop app, if a menu with **Local** and **Cloud** opens, select **Cloud**. A page titled **New routine** or **New scheduled task** opens. Fill in its fields:

* **Name**: enter one.
* **Instructions**: enter the prompt. In the same box, select the model, the effort level if the model offers one, the repositories, and the environment. For what each one controls, see the steps under [Create from the web](#create-from-the-web).
* **Select a trigger**: select **Schedule**, **GitHub event**, or **API**. For a schedule, see [Add a schedule trigger](#add-a-schedule-trigger). For a [GitHub event](#add-a-github-trigger), select a repository. For an [API trigger](#add-an-api-trigger), copy the token from the **API token** dialog that opens after you click **Create**, because it is shown once. To combine several triggers, click **Add another trigger**.
* **Connectors**: all of your connected connectors are included by default, so remove the ones the task doesn't need.

If **Create** is unavailable, hover over it to see what the form still needs. Click **Create**, and the task's detail page opens.

### Create from the CLI

Run `/schedule` in any session to create a scheduled task conversationally. You can also pass a description directly, for a recurring task like `/schedule daily PR review at 9am` or a one-off like `/schedule clean up feature flag in one week`. Claude walks through the same information the web dialog collects, then saves the task to your account. The command is also available under the alias `/routines`.

A successful start looks like a conversation: Claude asks follow-up questions about the schedule, repositories, and prompt before saving. If Claude instead replies that you need to authenticate or that it can't connect to your remote claude.ai account, no scheduled task was created; see [Troubleshooting](#troubleshooting).

A task you create with `/schedule` has a schedule trigger. You can also add the other trigger types:

* **API trigger**: edit the task on the web at [claude.ai/code/routines](https://claude.ai/code/routines)
* **[GitHub trigger](#add-a-github-trigger)**: edit the task on the web, or ask Claude in the CLI. Adding one from the CLI requires Claude Code v2.1.225 or later

A scheduled task with no schedule trigger, such as one started only by API calls or GitHub events, has no next run time. The CLI shows none when Claude saves or updates it.

## Configure triggers

A scheduled task starts when one of its triggers matches. Add or remove a task's triggers at any time in the **Trigger** row of the task's [edit dialog](#edit-and-control-scheduled-tasks).

When a task has two or more triggers, each one has a trash icon in that dialog. To remove a schedule or GitHub event trigger, click its trash icon, then **Save changes**. To remove an API trigger, [delete its token](#add-an-api-trigger) instead.

### Add a schedule trigger

A schedule trigger runs the task on a recurring cadence, or once at a specific future time. In the task's creation or edit dialog on the web, pick a preset frequency such as hourly, daily, or weekly:

* **Runs on the hour**: if you schedule a run exactly on the hour, such as 9:00, it can start several minutes late. To start close to the scheduled time, pick a few minutes past the hour, for example 9:07.
* **Custom intervals**: for a cadence the presets lack, create the task and select **Custom** in its [edit dialog](#edit-and-control-scheduled-tasks). Then enter a cron expression, such as `0 */2 * * *` for every two hours. To set one from the CLI, run [`/schedule update`](#manage-scheduled-tasks-from-the-cli). Expressions that run more often than once per hour are rejected.
* **Time zone**: when you pick a preset frequency, enter the time in your local time zone.
* **Cron expression time zone**: when the expression is five fields alone, write the hours in UTC, so `0 9 * * 1-5` runs at 9:00 AM UTC on weekdays. If the field opens with a `CRON_TZ=` prefix, keep it and write the hours in its zone, or delete it and write them in UTC.

#### Schedule a one-off run

A one-off schedule runs the task a single time at a specific timestamp. For example, use it to:

* Remind yourself later in the week
* Open a cleanup PR after a rollout finishes
* Start follow-up work after an upstream change ships

After the task runs, it turns itself off and the web UI marks it as **Completed**. To run it again, open the task's [edit dialog](#edit-and-control-scheduled-tasks) on the web and select **One-time** or **Once**, whichever label your dialog shows. Then set a new date and time in your local time zone and save.

Create a one-off run from the CLI by describing the time in natural language. Claude resolves the phrase against the current time and confirms the absolute timestamp before saving.

```text theme={null}
/schedule tomorrow at 9am, summarize yesterday's merged PRs
```

```text theme={null}
/schedule in 2 weeks, open a cleanup PR that removes the feature flag
```

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

Choose an event from any of the following categories. Within each category you can pick a specific action, such as `pull_request.opened`, or react to all actions in the category.

| Event | Triggers when |
| :- | :- |
| Pull request | A PR is opened, closed, assigned, labeled, synchronized, or otherwise updated |
| Release | A release is created, published, edited, or deleted |
| Issue | An issue is opened, edited, closed, reopened, labeled, assigned, or otherwise updated |

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

Under **History** on the task's detail page, each finished run's row ends with **Error** if the run failed, **Cancelled** if it was cancelled, and neither word if it succeeded. The **Status** filter names the same three outcomes **Failed**, **Cancelled**, and **Succeeded**. These outcomes say how the session ended, not whether Claude completed the work your prompt describes, so open the run and read its transcript to see what happened.

* **Succeeded**: the session ended without Claude Code reporting a failure. Blocked network requests, missing connector tools, and work Claude couldn't complete appear in the transcript rather than on the row
* **Failed**: the session didn't finish normally. For example, it stopped unexpectedly, ended on an error, or was archived before the run started
* **Cancelled**: the run didn't fail, and its session was archived. If you archive the session of a run that succeeded, the run changes to **Cancelled**. Nothing in the task needs to change

If a warning appears under **History**, see ["The last run" warnings](#the-last-run-didnt-start).

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
> See [GitHub authentication options](https://code.claude.com/docs/en/claude-code-on-the-web.md#github-authentication-options) for the two ways to grant access. On Team and Enterprise plans, an [Owner](https://code.claude.com/docs/en/server-managed-settings.md#access-control) of your Claude organization has to turn on each method before you can use it; see [Connect GitHub](https://code.claude.com/docs/en/web-quickstart.md#connect-github).

If your GitHub connection is missing or expired when a run is due, the scheduled task skips runs until you reconnect, for up to 72 hours. Reconnect GitHub within that window and the task resumes on its own. After 72 hours without a connection, the task turns off, and you turn it back on after reconnecting GitHub.

Each repository you add is cloned on every run. Claude starts from the repository's default branch unless your prompt specifies otherwise. If a [GitHub pull request event](#add-a-github-trigger) triggers the run and the pull request's repository is the task's first repository, that repository starts from the pull request's head commit instead.

Claude pushes its work to a branch prefixed with `claude/` unless your prompt directs it to push to another branch. To control which branches a run can push to, use branch protection rules or rulesets on GitHub. For runs on Anthropic-managed infrastructure, and for self-hosted runs that push through [Anthropic's git proxy](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#use-the-anthropic-git-proxy), GitHub applies them to the GitHub access you connected, so a rule that access can bypass doesn't block a run's push. A self-hosted run that pushes with the git credentials your deployment provides is checked against those instead. See [Configure git](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#configure-git).

### Connectors

Scheduled tasks can use your connected MCP connectors to read from and write to external services during each run. For example, a task that triages support requests might read from a Slack channel and create issues in Linear.

Connectors are the [claude.ai integrations](https://code.claude.com/docs/en/mcp.md#use-mcp-servers-from-claude-ai) on your account. MCP servers you added locally in the CLI with `claude mcp add` are stored on your machine rather than your claude.ai account, so they do not appear in the connectors list. To use one of those servers in a scheduled task:

* **As a connector**: add it as a connector at [claude.ai/customize/connectors](https://claude.ai/customize/connectors)
* **In the repository**: for a scheduled task with one repository, you can instead declare the server in a committed [`.mcp.json`](https://code.claude.com/docs/en/mcp#project-scope), unless the task runs as threads in a [project](https://code.claude.com/docs/en/claude-projects.md#what-threads-pick-up-from-your-repositories). If it does, add the server as a connector.

When you create a scheduled task, all of your currently connected connectors are included by default. Remove any that aren't needed to limit which tools Claude has access to during the run. You can also add connectors directly from the task's creation or edit dialog.

To manage or add connectors outside of that dialog, visit [claude.ai/customize/connectors](https://claude.ai/customize/connectors) or use `/schedule update` in the CLI.

### Permission prompts during a run

> [!NOTE]
>
> For a task that runs in your organization's self-hosted environment, see [Permissions and tool approval](https://code.claude.com/docs/en/self-hosted-environments-configuration.md#permissions-and-tool-approval).

When a run starts a new session on Anthropic's cloud, that session begins in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) unless auto mode is unavailable. In auto mode, a classifier model allows or blocks actions that would otherwise wait for your approval.

A run still stops and waits for an answer in cases such as these:

* **Actions that prompt even in auto mode**: for example, an action that matches an [ask rule](https://code.claude.com/docs/en/permissions.md#manage-permissions). See [How auto mode evaluates actions](https://code.claude.com/docs/en/permission-modes.md#how-auto-mode-evaluates-actions)
* **Repeated blocks**: one block doesn't end the run. Once blocks reach auto mode's [repeated-block thresholds](https://code.claude.com/docs/en/permission-modes.md#repeated-block-thresholds), a permission prompt appears in the run's session and waits until someone answers it

If auto mode is unavailable, such as when your organization turned it off or the task's model doesn't support it, the run keeps the permission mode it launched in. To answer a waiting prompt, open the run from the task's [detail page](#view-and-interact-with-runs).

In a [project](https://code.claude.com/docs/en/claude-projects.md), a run can continue a thread rather than start a new session. That run keeps whatever permission mode the thread is in at the time. When that thread was made, it started in auto mode unless auto mode was unavailable. To answer a prompt waiting in that thread, see [Unblock a thread waiting on approval](https://code.claude.com/docs/en/claude-projects.md#unblock-a-thread-waiting-on-approval).

### When a run publishes an artifact without asking

During a run in [auto mode](#permission-prompts-during-a-run), Claude publishes an [artifact](https://code.claude.com/docs/en/artifacts.md) without asking you once the classifier allows the publish. You're still asked first when, for example, the publish matches an [ask rule](https://code.claude.com/docs/en/permissions.md#manage-permissions). A new artifact is visible only to you until you [share it](https://code.claude.com/docs/en/artifacts.md#share-an-artifact). The [Accept edits rules](#artifacts-in-accept-edits-mode) that follow don't apply in auto mode.

When a scheduled task's job is to keep a page current, give it an artifact you already published.

#### Artifacts in Accept edits mode

When a scheduled task's schedule or **Run now** starts a run, Claude can publish a new [artifact](https://code.claude.com/docs/en/artifacts.md) without asking. The new artifact is visible only to you until you [share it](https://code.claude.com/docs/en/artifacts.md#share-an-artifact). If the publish declares runtime capabilities for the page, such as [connector calls](https://code.claude.com/docs/en/artifacts.md#pull-live-data-with-mcp-connectors) or [file downloads](https://code.claude.com/docs/en/artifacts.md#offer-a-file-download), Claude asks first.

In those runs, Claude republishes an existing artifact without asking only when all of these hold:

* You can edit the artifact and it belongs to your own organization
* If the publish carries more than the page, such as supporting files, you own the artifact
* The artifact isn't shared publicly
* If the artifact is shared with specific people or your organization, its viewers don't automatically see each new version
* The publish doesn't force over a newer version
* The publish doesn't declare runtime capabilities for the page
* The existing page holds no grant that reaches beyond the page, such as [connector calls](https://code.claude.com/docs/en/artifacts.md#pull-live-data-with-mcp-connectors)

In every other case, including a run that an API or GitHub trigger starts, Claude asks first.

### Environments and network access

Each scheduled task uses a [cloud environment](https://code.claude.com/docs/en/cloud-environments.md) that controls network access, environment variables, and setup scripts. The task inherits the environment's network policy on every run.

The **Default** environment uses **Trusted** network access, which allows only the [default allowlist](https://code.claude.com/docs/en/cloud-environments.md#default-allowed-domains) through the session's network. Requests on that path to hosts outside the allowlist fail with `403` and `x-deny-reason: host_not_allowed`. MCP connector traffic is routed through Anthropic's servers rather than that path, so the connectors you add to the task work without adding their hosts to **Allowed domains**. Remove any connectors you don't need under [Connectors](#connectors).

To allow additional domains on one of your own environments, follow these steps. An [organization-shared environment](https://code.claude.com/docs/en/cloud-environments.md#organization-shared-environments) opens read-only here, so an Owner changes its network access from the **Cloud environments** page in [admin settings](https://claude.ai/admin-settings) instead.

**1. Open the task for editing**

Go to [claude.ai/code/routines](https://claude.ai/code/routines), click the scheduled task, then open the menu next to its name and select **Edit**. The **Edit scheduled task** dialog opens.

**2. Open the environment selector**

Go to **Advanced settings > General > Cloud environment**, expanding **Advanced settings** first if it's collapsed. Click the cloud icon showing your environment's name, such as **Default**.

**3. Open the environment settings**

Hover over the environment in the list and click the settings icon that appears on the right.

**4. Change the network access level**

In the **Edit cloud environment** dialog, change **Network access** to **Custom** and enter your domains in **Allowed domains**. Check **Also include default list of common package managers** to keep the [default allowlist](https://code.claude.com/docs/en/cloud-environments.md#default-allowed-domains) alongside your custom domains. Select **Full** instead for unrestricted access.

**5. Save**

Click **Save changes** in the **Edit cloud environment** dialog, then close the **Edit scheduled task** dialog behind it. The new policy applies from the next run.

See [Network access](https://code.claude.com/docs/en/cloud-environments.md#network-access) for details on access levels and the default allowlist.

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

* **App**: in some accounts the sidebar entry and page title read **Routines**, the button reads **New routine**, and other labels say routine. To create a task there, see [Full-page form](#full-page-form).
* **Web address**: `claude.ai/code/routines`
* **CLI**: the `/routines` alias for `/schedule`, the command's description, and Claude's replies while it sets up a task
* **API**: the `/fire` endpoint path, its beta header, its response `type`, the `<routine-fire-payload>` tag, and the [Trigger a routine through the API](https://platform.claude.com/docs/en/api/claude-code/routines-fire) reference page
* **Organization settings**: the **Scheduled tasks (Was Routines)** toggle

## Troubleshooting

### `/schedule` returns "Unknown command"

The CLI hides `/schedule` when one of its requirements isn't met: the command menu shows `No commands match "/schedule"` while you type. Submitting it returns `Unknown command: /schedule`, except in the cases below that note a different answer.

The cause is usually one of the following:

* You are authenticated with a Console API key, an [Anthropic profile or federation credential](https://code.claude.com/docs/en/authentication.md#anthropic-profiles-and-federation-credentials), or a cloud provider such as Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry. `/schedule` requires a claude.ai subscription login. With a Console API key or a profile, and feature-flag fetching enabled, submitting `/schedule` instead shows `/schedule is available with Claude for Enterprise — ask your admin about migrating from API-key access`. With a cloud-provider login, you still see `Unknown command: /schedule`. If `ANTHROPIC_API_KEY` or `ANTHROPIC_AUTH_TOKEN` is set in your shell, or `apiKeyHelper` is set in `settings.json`, remove it first, since these take precedence over a claude.ai login. A profile or federation credential takes precedence too, so switch that off as well
* You are fully signed out, with no API key or other credential. With feature-flag fetching enabled, submitting `/schedule` shows `/schedule requires a claude.ai subscription. Run /login to sign in with your claude.ai account.` Before v2.1.268, a signed-out session showed the same Claude for Enterprise message as a Console API key
* You are inside a cloud session, where submitting `/schedule` answers that the command isn't available in that environment. Manage scheduled tasks from the [web UI](https://claude.ai/code/routines) instead
* Your organization's policy disables [cloud sessions](https://code.claude.com/docs/en/claude-code-on-the-web.md), which scheduled tasks require. In this case, submitting `/schedule` answers [`Cloud sessions are disabled by your organization's policy`](https://code.claude.com/docs/en/errors#cloud-sessions-are-disabled-by-your-organizations-policy) instead. Before v2.1.268, it returned `Unknown command: /schedule`
* An Owner [turned off scheduled tasks](#routines-are-disabled-by-your-organizations-policy) for your Team or Enterprise organization. Before v2.1.227, the command still appeared in this case, and claude.ai rejected the task when Claude tried to create or run it
* Your Enterprise organization manages your access with [custom roles](https://support.claude.com/en/articles/13930452), and none of your roles includes the scheduled tasks permission under **Remote sessions**. Ask an Owner to add it to one of your roles

If the cause is your CLI sign-in or being inside a cloud session, you can still create and manage scheduled tasks at [claude.ai/code/routines](https://claude.ai/code/routines). You need a Pro, Max, Team, or Enterprise account there. If scheduled tasks or cloud sessions are off for your organization or missing from your roles, you can't create them on the web either.

### "Routines are disabled by your organization's policy"

An Owner in your Team or Enterprise organization has likely turned off the **Scheduled tasks (Was Routines)** toggle at [**Organization settings > Capabilities > Remote sessions**](https://claude.ai/admin-settings/capabilities). On Claude Code v2.1.227 or later, the same toggle also hides `/schedule` in the CLI. This is a server-side organization setting, so it cannot be overridden from your local configuration. Ask an Owner to turn scheduled tasks back on for your organization.

### "The last run" warnings

When a warning under **History** begins with "The last run", find it in the first column and do what its row says. The warning clears once a later run starts.

| Warning | What to do |
| :- | :- |
| "The last run didn't start because your organization had reached its limit on cloud sessions running at once." | The task needs no change. Click **Run now** later, or wait for the next run |
| "The last run didn't start because its cloud environment couldn't be found or used." | On the task's detail page, open the menu next to its name, select **Edit**, and find the [cloud environment selector](#environments-and-network-access). If it reads **Unavailable environment**, that environment was archived or is no longer available to your account, so choose another one there and save your changes. Otherwise, retry with **Run now** on the detail page, or pick another environment in the selector and save your changes |
| "The last run was blocked because it couldn't access something it needs, or your organization's policy doesn't allow it." | Check that your [GitHub access](#repositories-and-branch-permissions) covers the task's repositories. If it does, ask an [Owner](https://code.claude.com/docs/en/server-managed-settings.md#access-control) of your Claude organization whether a policy blocks the task |
| "The last run didn't start because of a problem that's usually temporary." | Click **Run now** to try again, or wait for the next run |
| "The last run didn't start because its repository or branch wasn't available." | Check on GitHub that each repository in the task has the [branch the run starts from](#repositories-and-branch-permissions). Also check that your [GitHub access](#repositories-and-branch-permissions) covers each repository, and reconnect GitHub if your connection expired |
| "The last run didn't start because some of its settings weren't accepted." | On the task's detail page, open the menu next to its name and select **Edit**. The dialog doesn't mark which setting wasn't accepted, so check each one there, including the task's name, prompt, model, repositories, environment, connectors, and triggers |
| "The last run stopped because a usage limit was reached." | For when the task's runs can start again after a usage limit, see [Usage and limits](#usage-and-limits) |
| "The last run failed." | Click **Run now** to try again, or wait for the next run. The failed run has no session to open |

## Related resources

* [`/loop` and in-session scheduling](https://code.claude.com/docs/en/scheduled-tasks): schedule local tasks within an open CLI session
* [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks.md): local scheduled tasks that run on your machine with access to local files
* [Cloud environments](https://code.claude.com/docs/en/cloud-environments.md): configure network access, environment variables, and setup scripts for cloud sessions
* [Projects](https://code.claude.com/docs/en/claude-projects.md): ongoing work Claude coordinates across parallel cloud sessions; scheduled tasks created from a project appear on its **Scheduled tasks** tab
* [MCP connectors](https://code.claude.com/docs/en/mcp.md): connect external services like Slack, Linear, and Google Drive
* [GitHub Actions](https://code.claude.com/docs/en/github-actions.md): run Claude in your CI pipeline on repository events
