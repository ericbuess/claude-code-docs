> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automate work with routines

> Put Claude Code on autopilot. Define routines that run on a schedule, trigger on API calls, or react to GitHub events from Anthropic-managed cloud infrastructure.

<Note>
  Routines are in research preview. Behavior, limits, and the API surface may change.
</Note>

A routine is a saved Claude Code configuration: a prompt, one or more repositories, and a set of [connectors](/en/mcp), packaged once and run automatically. Routines execute on Anthropic-managed cloud infrastructure, so they keep working when your laptop is closed.

Each routine can have one or more triggers attached to it:

* **Scheduled**: run on a recurring cadence like hourly, nightly, or weekly
* **API**: trigger on demand by sending an HTTP POST to a per-routine endpoint with a bearer token
* **GitHub**: run automatically in response to repository events such as pull requests, pushes, issues, or workflow runs

A single routine can combine triggers. For example, a PR review routine can run nightly, trigger from a deploy script, and also react to every new PR.

Routines are available on Pro, Max, Team, and Enterprise plans with [Claude Code on the web](/en/claude-code-on-the-web) enabled. Create and manage them at [claude.ai/code/routines](https://claude.ai/code/routines), or from the CLI with `/schedule`.

This page covers creating a routine, configuring each trigger type, managing runs, and how usage limits apply.

## Example use cases

Each example pairs a trigger type with the kind of work routines are suited to: unattended, repeatable, and tied to a clear outcome.

**Backlog maintenance.** A schedule trigger runs every weeknight against your issue tracker via a connector. The routine reads issues opened since the last run, applies labels, assigns owners based on the area of code referenced, and posts a summary to Slack so the team starts the day with a groomed queue.

**Alert triage.** Your monitoring tool calls the routine's API endpoint when an error threshold is crossed, passing the alert body as `text`. The routine pulls the stack trace, correlates it with recent commits in the repository, and opens a draft pull request with a proposed fix and a link back to the alert. On-call reviews the PR instead of starting from a blank terminal.

**Bespoke code review.** A GitHub trigger runs on `pull_request.opened`. The routine applies your team's own review checklist, leaves inline comments for security, performance, and style issues, and adds a summary comment so human reviewers can focus on design instead of mechanical checks.

**Deploy verification.** Your CD pipeline calls the routine's API endpoint after each production deploy. The routine runs smoke checks against the new build, scans error logs for regressions, and posts a go or no-go to the release channel before the deploy window closes.

**Docs drift.** A schedule trigger runs weekly. The routine scans merged PRs since the last run, flags documentation that references changed APIs, and opens update PRs against the docs repository for an editor to review.

**Library port.** A GitHub trigger runs on `pull_request.closed` filtered to merged PRs in one SDK repository. The routine ports the change to a parallel SDK in another language and opens a matching PR, keeping the two libraries in step without a human re-implementing each change.

The sections below walk through creating a routine and configuring each of these trigger types.

## Create a routine

Create a routine from the web, the Desktop app, or the CLI. All three surfaces write to the same cloud account, so a routine you create in the CLI shows up at claude.ai/code/routines immediately. In the Desktop app, click **New task** and choose **New remote task**; choosing **New local task** instead creates a [local Desktop scheduled task](/en/desktop-scheduled-tasks), which runs on your machine and is not a routine.

The creation form sets up the routine's prompt, repositories, environment, connectors, and triggers.

Routines run autonomously as full Claude Code cloud sessions: there is no permission-mode picker and no approval prompts during a run. The session can run shell commands, use [skills](/en/skills) committed to the cloned repository, and call any connectors you include. What a routine can reach is determined by the repositories you select and their branch-push setting, the [environment's](/en/claude-code-on-the-web#the-cloud-environment) network access and variables, and the connectors you include. Scope each of those to what the routine actually needs.

Routines belong to your individual claude.ai account. They are not shared with teammates, and they count against your account's daily run allowance. Anything a routine does through your connected GitHub identity or connectors appears as you: commits and pull requests carry your GitHub user, and Slack messages, Linear tickets, or other connector actions use your linked accounts for those services.

### Create from the web

<Steps>
  <Step title="Open the creation form">
    Visit [claude.ai/code/routines](https://claude.ai/code/routines) and click **New routine**.
  </Step>

  <Step title="Name the routine and write the prompt">
    Give the routine a descriptive name and write the prompt Claude runs each time. The prompt is the most important part: the routine runs autonomously, so the prompt must be self-contained and explicit about what to do and what success looks like.

    The prompt input includes a model selector. Claude uses the selected model on every run.
  </Step>

  <Step title="Select repositories">
    Add one or more GitHub repositories for Claude to work in. Each repository is cloned at the start of a run, starting from the default branch. Claude creates `claude/`-prefixed branches for its changes. To allow pushes to any branch, enable **Allow unrestricted branch pushes** for that repository.
  </Step>

  <Step title="Select an environment">
    Pick a [cloud environment](/en/claude-code-on-the-web#the-cloud-environment) for the routine. Environments control what the cloud session has access to:

    * **Network access**: set the level of internet access available during each run
    * **Environment variables**: provide API keys, tokens, or other secrets Claude can use
    * **Setup script**: run install commands before each session starts, like installing dependencies or configuring tools

    A **Default** environment is provided. To use a custom environment, [create one](/en/claude-code-on-the-web#the-cloud-environment) before creating the routine.
  </Step>

  <Step title="Select a trigger">
    Under **Select a trigger**, choose how the routine starts. You can pick one trigger type or combine several.

    <Tabs>
      <Tab title="Schedule">
        Pick a preset frequency: hourly, daily, weekdays, or weekly. See [Add a schedule trigger](#add-a-schedule-trigger) for timezone handling, stagger, and custom cron intervals.
      </Tab>

      <Tab title="GitHub event">
        Select the repository, the event to react to, and optional filters. See [Add a GitHub trigger](#add-a-github-trigger) for the full list of supported events and filter fields.
      </Tab>

      <Tab title="API">
        Select **API** here, then save the routine. The URL and token are generated after the routine is saved, since they depend on the routine ID. See [Add an API trigger](#add-an-api-trigger) to copy the URL and generate a token.
      </Tab>
    </Tabs>
  </Step>

  <Step title="Review connectors">
    All of your connected [MCP connectors](/en/mcp) are included by default. Remove any that the routine doesn't need. Connectors give Claude access to external services like Slack, Linear, or Google Drive during each run.
  </Step>

  <Step title="Create the routine">
    Click **Create**. The routine appears in the list and runs the next time one of its triggers matches. To start a run immediately, click **Run now** on the routine's detail page.

    Each run creates a new session alongside your other sessions, where you can see what Claude did, review changes, and create a pull request.
  </Step>
</Steps>

### Create from the CLI

Run `/schedule` in any session to create a scheduled routine conversationally. You can also pass a description directly, as in `/schedule daily PR review at 9am`. Claude walks through the same information the web form collects, then saves the routine to your account.

`/schedule` in the CLI creates scheduled routines only. To add an API or GitHub trigger, edit the routine on the web at [claude.ai/code/routines](https://claude.ai/code/routines).

The CLI also supports managing existing routines. Run `/schedule list` to see all routines, `/schedule update` to change one, or `/schedule run` to trigger it immediately.

### Create from the Desktop app

Open the **Schedule** page in the Desktop app, click **New task**, and choose **New remote task**. The Desktop app shows both local scheduled tasks and routines in the same grid. See [Desktop scheduled tasks](/en/desktop-scheduled-tasks) for details on the local option.

## Configure triggers

A routine starts when one of its triggers matches. You can attach any combination of schedule, API, and GitHub triggers to the same routine, and add or remove them at any time from the **Select a trigger** section of the routine's edit form.

### Add a schedule trigger

A schedule trigger runs the routine on a recurring cadence. Pick a preset frequency in the **Select a trigger** section: hourly, daily, weekdays, or weekly. Times are entered in your local zone and converted automatically, so the routine runs at that wall-clock time regardless of where the cloud infrastructure is located.

Runs may start a few minutes after the scheduled time due to stagger. The offset is consistent for each routine.

For a custom interval such as every two hours or the first of each month, pick the closest preset in the form, then run `/schedule update` in the CLI to set a specific cron expression. The minimum interval is one hour; expressions that run more frequently are rejected.

### Add an API trigger

An API trigger gives a routine a dedicated HTTP endpoint. POSTing to the endpoint with the routine's bearer token starts a new session and returns a session URL. Use this to wire Claude Code into alerting systems, deploy pipelines, internal tools, or anywhere you can make an authenticated HTTP request.

API triggers are added to an existing routine from the web. The CLI cannot currently create or revoke tokens.

<Steps>
  <Step title="Open the routine for editing">
    Go to [claude.ai/code/routines](https://claude.ai/code/routines), click the routine you want to trigger via API, then click the pencil icon to open **Edit routine**.
  </Step>

  <Step title="Add an API trigger">
    Scroll to the **Select a trigger** section below the prompt, click **Add another trigger**, and choose **API**.
  </Step>

  <Step title="Copy the URL and generate a token">
    The modal shows the URL for this routine along with a sample curl command. Copy the URL, then click **Generate token** and copy the token immediately. The token is shown once and cannot be retrieved later, so store it somewhere secure such as your alerting tool's secret store.
  </Step>

  <Step title="Call the endpoint">
    Send the token in the `Authorization: Bearer` header when you POST to the URL. The [Trigger a routine](#trigger-a-routine) section below shows a complete example.
  </Step>
</Steps>

Each routine has its own token, scoped to triggering that routine only. To rotate or revoke it, return to the same modal and click **Regenerate** or **Revoke**.

#### Trigger a routine

Send a POST request to the `/fire` endpoint with the bearer token in the `Authorization` header. The request body accepts an optional `text` field that's appended to the routine's configured prompt as a one-shot user turn. Use `text` to pass context like an alert body or a failing log.

The example below triggers a routine from a shell:

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

<Warning>
  The `/fire` endpoint ships under the `experimental-cc-routine-2026-04-01` beta header. Request and response shapes, rate limits, and token semantics may change while the feature is in research preview. Breaking changes ship behind new dated beta header versions, and the two most recent previous header versions continue to work so that callers have time to migrate.
</Warning>

#### API reference

For the full API reference, including all error responses, validation rules, and field limits, see [Trigger a routine via API](https://platform.claude.com/docs/en/api/claude-code/routines-fire) in the Claude Platform documentation.

The `/fire` endpoint is available to claude.ai users only and is not part of the Claude Platform API surface.

### Add a GitHub trigger

A GitHub trigger starts a new session automatically when a matching event occurs on a connected repository. Each matching event starts its own session.

<Note>
  During the research preview, GitHub webhook events are subject to per-routine and per-account hourly caps. Events beyond the limit are dropped until the window resets. See your current limits at [claude.ai/code/routines](https://claude.ai/code/routines).
</Note>

GitHub triggers are configured from the web UI only.

<Steps>
  <Step title="Open the routine for editing">
    Go to [claude.ai/code/routines](https://claude.ai/code/routines), click the routine, then click the pencil icon to open **Edit routine**.
  </Step>

  <Step title="Add a GitHub event trigger">
    Scroll to the **Select a trigger** section, click **Add another trigger**, and choose **GitHub event**.
  </Step>

  <Step title="Install the Claude GitHub App">
    The Claude GitHub App must be installed on the repository you want to subscribe to. The trigger setup prompts you to install it if it isn't already.

    <Note>
      Running `/web-setup` in the CLI grants repository access for cloning, but it does not install the Claude GitHub App and does not enable webhook delivery. GitHub triggers require installing the Claude GitHub App, which the trigger setup prompts you to do.
    </Note>
  </Step>

  <Step title="Configure the trigger">
    Select the repository, choose an event from the [supported events](#supported-events) list, and optionally add filters. Save the trigger.
  </Step>
</Steps>

#### Supported events

GitHub triggers can subscribe to any of the following event categories. Within each category you can pick a specific action, such as `pull_request.opened`, or react to all actions in the category.

| Event                       | Triggers when                                                                 |
| :-------------------------- | :---------------------------------------------------------------------------- |
| Pull request                | A PR is opened, closed, assigned, labeled, synchronized, or otherwise updated |
| Pull request review         | A PR review is submitted, edited, or dismissed                                |
| Pull request review comment | A comment on a PR diff is created, edited, or deleted                         |
| Push                        | Commits are pushed to a branch                                                |
| Release                     | A release is created, published, edited, or deleted                           |
| Issues                      | An issue is opened, edited, closed, labeled, or otherwise updated             |
| Issue comment               | A comment on an issue or PR is created, edited, or deleted                    |
| Sub issues                  | A sub-issue or parent issue is added or removed                               |
| Commit comment              | A commit or diff is commented on                                              |
| Discussion                  | A discussion is created, edited, answered, or otherwise updated               |
| Discussion comment          | A discussion comment is created, edited, or deleted                           |
| Check run                   | A check run is created, requested, rerequested, or completed                  |
| Check suite                 | A check suite completes or is requested                                       |
| Merge queue entry           | A PR enters or leaves the merge queue                                         |
| Workflow run                | A GitHub Actions workflow run starts or completes                             |
| Workflow job                | A GitHub Actions job is queued or completes                                   |
| Workflow dispatch           | A workflow is manually triggered                                              |
| Repository dispatch         | A custom repository\_dispatch event is sent                                   |

#### Filter pull requests

Use filters to narrow which pull requests start a new session. All filter conditions must match for the routine to trigger. The available filter fields are:

| Filter      | Matches                          |
| :---------- | :------------------------------- |
| Author      | PR author's GitHub username      |
| Title       | PR title text                    |
| Body        | PR description text              |
| Base branch | Branch the PR targets            |
| Head branch | Branch the PR comes from         |
| Labels      | Labels applied to the PR         |
| Is draft    | Whether the PR is in draft state |
| Is merged   | Whether the PR has been merged   |
| From fork   | Whether the PR comes from a fork |

A few example filter combinations:

* **Auth module review**: base branch `main`, head branch contains `auth-provider`. Sends any PR that touches authentication to a focused reviewer.
* **External contributor triage**: from fork is `true`. Routes every fork-based PR through an extra security and style review before a human looks at it.
* **Ready-for-review only**: is draft is `false`. Skips drafts so the routine only runs when the PR is ready for review.
* **Label-gated backport**: labels include `needs-backport`. Triggers a port-to-another-branch routine only when a maintainer tags the PR.

#### How sessions map to events

Each matching GitHub event starts a new session. Session reuse across events is not available for GitHub-triggered routines, so two pushes or two PR updates produce two independent sessions.

## Manage routines

Click a routine in the list to open its detail page. The detail page shows the routine's repositories, connectors, prompt, schedule, API tokens, GitHub triggers, and a list of past runs.

### View and interact with runs

Click any run to open it as a full session. From there you can see what Claude did, review changes, create a pull request, or continue the conversation. Each run session works like any other session: use the dropdown menu next to the session title to rename, archive, or delete it.

### Edit and control routines

From the routine detail page you can:

* Click **Run now** to start a run immediately without waiting for the next scheduled time.
* Use the toggle in the **Repeats** section to pause or resume the schedule. Paused routines keep their configuration but don't run until you re-enable them.
* Click the pencil icon to open **Edit routine** and change the name, prompt, repositories, environment, connectors, or any of the routine's triggers. The **Select a trigger** section is where you add or remove schedules, API tokens, and GitHub event triggers.
* Click the delete icon to remove the routine. Past sessions created by the routine remain in your session list.

### Repositories and branch permissions

Routines need GitHub access to clone repositories. When you create a routine from the CLI with `/schedule`, Claude checks whether your account has GitHub connected and prompts you to run `/web-setup` if it doesn't. See [GitHub authentication options](/en/claude-code-on-the-web#github-authentication-options) for the two ways to grant access.

Each repository you add is cloned on every run. Claude starts from the repository's default branch unless your prompt specifies otherwise.

By default, Claude can only push to branches prefixed with `claude/`. This prevents routines from accidentally modifying protected or long-lived branches. To remove this restriction for a specific repository, enable **Allow unrestricted branch pushes** for that repository when creating or editing the routine.

### Connectors

Routines can use your connected MCP connectors to read from and write to external services during each run. For example, a routine that triages support requests might read from a Slack channel and create issues in Linear.

When you create a routine, all of your currently connected connectors are included by default. Remove any that aren't needed to limit which tools Claude has access to during the run. You can also add connectors directly from the routine form.

To manage or add connectors outside of the routine form, visit **Settings > Connectors** on claude.ai or use `/schedule update` in the CLI.

### Environments

Each routine runs in a [cloud environment](/en/claude-code-on-the-web#the-cloud-environment) that controls network access, environment variables, and setup scripts. Configure environments before creating a routine to give Claude access to APIs, install dependencies, or restrict network scope. See [cloud environment](/en/claude-code-on-the-web#the-cloud-environment) for the full setup guide.

## Usage and limits

Routines draw down subscription usage the same way interactive sessions do. In addition to the standard subscription limits, routines have a daily cap on how many runs can start per account. See your current consumption and remaining daily routine runs at [claude.ai/code/routines](https://claude.ai/code/routines) or [claude.ai/settings/usage](https://claude.ai/settings/usage).

When a routine hits the daily cap or your subscription usage limit, organizations with extra usage enabled can keep running routines on metered overage. Without extra usage, additional runs are rejected until the window resets. Enable extra usage from **Settings > Billing** on claude.ai.

## Related resources

* [`/loop` and in-session scheduling](/en/scheduled-tasks): schedule local tasks within an open CLI session
* [Desktop scheduled tasks](/en/desktop-scheduled-tasks): local scheduled tasks that run on your machine with access to local files
* [Cloud environment](/en/claude-code-on-the-web#the-cloud-environment): configure the runtime environment for cloud sessions
* [MCP connectors](/en/mcp): connect external services like Slack, Linear, and Google Drive
* [GitHub Actions](/en/github-actions): run Claude in your CI pipeline on repository events
