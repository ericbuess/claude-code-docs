> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Schedule tasks on the web

> Automate recurring work with cloud scheduled tasks

A scheduled task runs a prompt on a recurring cadence using Anthropic-managed infrastructure. Tasks keep working even when your computer is off.

A few examples of recurring work you can automate:

* Reviewing open pull requests each morning
* Analyzing CI failures overnight and surfacing summaries
* Syncing documentation after PRs merge
* Running dependency audits every week

Scheduled tasks are available to all Claude Code on the web users, including Pro, Max, Team, and Enterprise.

## Compare scheduling options

<Snippet file="scheduling-comparison.mdx" />

## Create a scheduled task

You can create a scheduled task from three places:

* **Web**: visit [claude.ai/code/scheduled](https://claude.ai/code/scheduled) and click **New scheduled task**
* **Desktop app**: open the **Schedule** page, click **New task**, and choose **New remote task**. See [Desktop scheduled tasks](/en/desktop#schedule-recurring-tasks) for details.
* **CLI**: run `/schedule` in any session. Claude walks you through the setup conversationally. You can also pass a description directly, like `/schedule daily PR review at 9am`.

The web and Desktop entry points open a form. The CLI collects the same information through a guided conversation.

The steps below walk through the web interface.

<Steps>
  <Step title="Open the creation form">
    Visit [claude.ai/code/scheduled](https://claude.ai/code/scheduled) and click **New scheduled task**.
  </Step>

  <Step title="Name the task and write the prompt">
    Give the task a descriptive name and write the prompt Claude runs each time. The prompt is the most important part: the task runs autonomously, so the prompt must be self-contained and explicit about what to do and what success looks like.

    The prompt input includes a model selector. Claude uses this model for each run of the task.
  </Step>

  <Step title="Select repositories">
    Add one or more GitHub repositories for Claude to work in. Each repository is cloned at the start of a run, starting from the default branch. Claude creates `claude/`-prefixed branches for its changes. To allow pushes to any branch, enable **Allow unrestricted branch pushes** for that repository.
  </Step>

  <Step title="Select an environment">
    Select a [cloud environment](/en/claude-code-on-the-web#cloud-environment) for the task. Environments control what the cloud session has access to:

    * **Network access**: set the level of internet access available during each run
    * **Environment variables**: provide API keys, tokens, or other secrets Claude can use
    * **Setup script**: run install commands before each session starts, like installing dependencies or configuring tools

    A **Default** environment is available out of the box. To use a custom environment, [create one](/en/claude-code-on-the-web#cloud-environment) before creating the task.
  </Step>

  <Step title="Choose a schedule">
    Pick how often the task runs from the [frequency options](#frequency-options). The default is daily at 9:00 AM in your local time zone. Tasks may run a few minutes after their scheduled time due to stagger.

    If the preset options don't fit your needs, pick the closest one and update the schedule from the CLI with `/schedule update` to set a specific schedule.
  </Step>

  <Step title="Review connectors">
    All of your connected [MCP connectors](/en/mcp) are included by default. Remove any that the task doesn't need. Connectors give Claude access to external services like Slack, Linear, or Google Drive during each run.
  </Step>

  <Step title="Create the task">
    Click **Create**. The task appears in the scheduled tasks list and runs automatically at the next scheduled time. Each run creates a new session alongside your other sessions, where you can see what Claude did, review changes, and create a pull request. To trigger a run immediately, click **Run now** from the task's detail page.
  </Step>
</Steps>

### Frequency options

The schedule picker offers preset frequencies that handle time zone conversion for you. Pick a time in your local zone and the task runs at that wall-clock time regardless of where the cloud infrastructure is located.

<Note>
  Tasks may run a few minutes after their scheduled time. The offset is consistent for each task.
</Note>

| Frequency | Description                                                                |
| :-------- | :------------------------------------------------------------------------- |
| Hourly    | Runs every hour.                                                           |
| Daily     | Runs once per day at the time you specify. Defaults to 9:00 AM local time. |
| Weekdays  | Same as Daily but skips Saturday and Sunday.                               |
| Weekly    | Runs once per week on the day and time you specify.                        |

For custom intervals like every 2 hours or first of each month, pick the closest preset and update the schedule from the CLI with `/schedule update` to set a specific schedule.

### Repositories and branch permissions

Each repository you add is cloned on every run. Claude starts from the repository's default branch unless your prompt specifies otherwise.

By default, Claude can only push to branches prefixed with `claude/`. This prevents scheduled tasks from accidentally modifying protected or long-lived branches.

To remove this restriction for a specific repository, enable **Allow unrestricted branch pushes** for that repository when creating or editing the task.

### Connectors

Scheduled tasks can use your connected MCP connectors to read from and write to external services during each run. For example, a task that triages support requests might read from a Slack channel and create issues in Linear.

When you create a task, all of your currently connected connectors are included by default. Remove any that aren't needed to limit which tools Claude has access to during the run. You can also add connectors directly from the task form.

To manage or add connectors outside of the task form, visit **Settings > Connectors** on claude.ai or use `/schedule update` in the CLI.

### Environments

Each task runs in a [cloud environment](/en/claude-code-on-the-web#cloud-environment) that controls network access, environment variables, and setup scripts. Configure environments before creating a task to give Claude access to APIs, install dependencies, or restrict network scope. See [cloud environment](/en/claude-code-on-the-web#cloud-environment) for the full setup guide.

## Manage scheduled tasks

Click a task in the **Scheduled** list to open its detail page. The detail page shows the task's repositories, connectors, prompt, schedule, and a list of past runs.

### View and interact with runs

Click any run to open it as a full session. From there you can see what Claude did, review changes, create a pull request, or continue the conversation. Each run session works like any other session: use the dropdown menu next to the session title to rename, archive, or delete it.

### Edit and control tasks

From the task detail page you can:

* Click **Run now** to start a run immediately without waiting for the next scheduled time.
* Use the toggle in the **Repeats** section to pause or resume the schedule. Paused tasks keep their configuration but don't run until you re-enable them.
* Click the edit icon to change the name, prompt, schedule, repositories, environment, or connectors.
* Click the delete icon to remove the task. Past sessions created by the task remain in your session list.

You can also manage tasks from the CLI with `/schedule`. Run `/schedule list` to see all tasks, `/schedule update` to change a task, or `/schedule run` to trigger one immediately.

## Related resources

* [Desktop scheduled tasks](/en/desktop#schedule-recurring-tasks): schedule tasks that run on your machine with access to local files. The Desktop app's **Schedule** page shows both local and remote tasks in the same grid.
* [`/loop` and CLI scheduled tasks](/en/scheduled-tasks): lightweight scheduling within a CLI session
* [Cloud environment](/en/claude-code-on-the-web#cloud-environment): configure the runtime environment for cloud tasks
* [MCP connectors](/en/mcp): connect external services like Slack, Linear, and Google Drive
* [GitHub Actions](/en/github-actions): run Claude in your CI pipeline on repo events
