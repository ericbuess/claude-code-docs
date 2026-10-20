> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Schedule recurring tasks in Claude Code Desktop

> Set up scheduled tasks in Claude Code Desktop to run Claude automatically on a recurring basis for daily code reviews, dependency audits, or morning briefings.

Scheduled tasks start a new session automatically at a time and frequency you choose. Use them for recurring work like daily code reviews, dependency update checks, or morning briefings that pull from your calendar and inbox.

The Desktop app's **Scheduled tasks** page lists both local scheduled tasks and [cloud scheduled tasks](/docs/en/routines), formerly routines:

* **Local task**: runs on your machine with direct access to your files and tools, but only fires while the app is open and your computer is awake
* **Cloud task**: runs even when your computer is off, and can also start on API calls or GitHub events

This page covers local scheduled tasks; for cloud scheduled tasks and their trigger options, see [Automate work with scheduled tasks](/docs/en/routines).

## Compare scheduling options

Claude Code offers three ways to schedule recurring or one-off work:

| | [Cloud](/docs/en/routines) | [Desktop](/docs/en/desktop-scheduled-tasks) | [`/loop`](/docs/en/scheduled-tasks) |
| :- | :- | :- | :- |
| Runs on | Cloud, Anthropic-managed by default | Your machine | Your machine |
| Requires machine on | No | Yes | Yes |
| Requires open session | No | No | Yes |
| Persistent across restarts | Yes | Yes | Restored on `--resume`, with [exceptions](/docs/en/scheduled-tasks#limitations) |
| Access to local files | No (fresh clone) | Yes | Yes |
| MCP servers | Connectors configured per task | [Config files](/docs/en/mcp) and connectors | Inherits from session |
| Permission prompts | No (runs autonomously) | Configurable per task | Inherits from session |
| Customizable schedule | Via `/schedule` in the CLI | Yes | Yes |
| Minimum interval | 1 hour | 1 minute | 1 minute |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

<Note>
  By default, local scheduled tasks run against whatever state your working directory is in, including uncommitted changes. To give each run its own [isolated Git worktree](/docs/en/desktop#run-a-session-in-its-own-worktree) instead, select **Worktree** in the task's [**Edit** form](#manage-scheduled-tasks) after you create it. The checkbox is available when the task's folder is a Git repository.
</Note>

## Create a scheduled task

Local scheduled tasks require Claude Desktop 1.1.5368 or later.

<Steps>
  <Step title="Open the Scheduled tasks page">
    In the [**Code** tab](/docs/en/desktop), click **Scheduled** in the sidebar or in the sidebar's **More** menu.
  </Step>

  <Step title="Start a new task">
    Click **New task**. If a menu opens with **Create with Claude** and **Set up manually**, select **Set up manually**. The **New scheduled task** dialog opens. If **Only on this computer** is at the top of the dialog, go to [Dialog with Only on this computer at the top](#dialog-with-only-on-this-computer-at-the-top) before you enter anything.
  </Step>

  <Step title="Name the task">
    Enter a name in the **Name** field. Desktop converts it to lowercase kebab-case and uses it as the task's folder name on disk, so the name must be unique across your tasks.
  </Step>

  <Step title="Write the instructions">
    In the box below the name, enter what Claude should do when the task runs.
  </Step>

  <Step title="Turn on Only on this computer">
    Skip past the **Trigger** card for now and expand **Advanced settings** below it. On the **General** tab, turn on **Only on this computer**. With it on, the task runs on your machine in a local folder, and the **Trigger** card offers the presets listed in [Schedule options](#schedule-options).

    If the switch is unavailable, clear the repository or the GitHub event or API trigger, because those make the task a [cloud scheduled task](/docs/en/routines).
  </Step>

  <Step title="Pick the local folder">
    In the **Local folder** row, select a folder. **Create** stays unavailable until you pick one.
  </Step>

  <Step title="Set the schedule">
    Back in the **Trigger** card, select a [schedule preset](#schedule-options).
  </Step>

  <Step title="Choose the permission mode and model">
    In the instructions box's toolbar, select a [permission mode](#permissions-for-scheduled-tasks) and model. If you leave them unchanged, runs use your Claude Code settings and the default model.
  </Step>

  <Step title="Create the task">
    Click **Create**. If you haven't trusted the folder yet, Desktop asks you to trust it at this point. The task's detail page opens.
  </Step>
</Steps>

On the detail page, click the pencil icon to open the [**Edit** form](#manage-scheduled-tasks). There you can change the **Description** that Desktop filled in from your instructions, select **Worktree**, or switch the schedule to **Manual**.

You can also create a task by describing what you want in any session. For example, "set up a daily code review that runs every morning at 9am" creates a recurring task. A request like "remind me at 3pm tomorrow to check the deploy" creates a one-time task that disables itself after it fires.

### Dialog with Only on this computer at the top

If **Only on this computer** is at the top of the **New scheduled task** dialog when it opens, turn it on before you enter anything. When you turn it on, a separate blank form for a local task replaces the form.

Then fill in the local form's fields:

* **Name**: enter a name, as in the [steps to create a scheduled task](#create-a-scheduled-task).
* **Description**: enter a description. **Create** stays unavailable until you do.
* **The instructions box**: enter what Claude should do when the task runs. Select the permission mode and model from the menus in the box.
* **Working folder**: select the folder the task runs in. **Create** stays unavailable until you select one.
* **Trigger**: select a schedule. **Custom** takes a cron expression. For the other presets, see [Schedule options](#schedule-options).

Click **Create**. The task's detail page opens.

## Schedule options

When you turn on **Only on this computer** under **Advanced settings**, the **Trigger** card offers Hourly, Daily, Weekdays, and Weekly. The task's [**Edit** form](#manage-scheduled-tasks) also offers **Manual**.

* **Hourly**: runs every hour
* **Daily**: runs every day at the local time you pick
* **Weekdays**: same as Daily but skips Saturday and Sunday
* **Weekly**: shows a time picker and a day picker
* **Manual**: no schedule, only runs when you click **Run now**. Useful for saving a prompt you trigger on demand

For intervals the picker doesn't offer, such as every 15 minutes, the first of each month, or a single run at a specific future time, ask Claude in any Desktop session to set the schedule. Use plain language; for example, "schedule a task to run all the tests every 6 hours."

## How scheduled tasks run

Local scheduled tasks run on your machine. Desktop checks the schedule every minute while the app is open and starts a fresh session when a task is due, independent of any manual sessions you have open. Each task gets a small delay of a few minutes after the scheduled time to stagger API traffic. The delay is deterministic: the same task always starts at the same offset.

Tasks only run while the desktop app is running and your computer is awake. If your computer sleeps through a scheduled time, the run is skipped. To prevent idle-sleep, turn on **Keep computer awake** in **Settings > This computer > System**. Closing the laptop lid still puts it to sleep.

<Note>
  For tasks that need to run even when your computer is off, or that should trigger on an API call or GitHub event, create a [cloud scheduled task](/docs/en/routines) instead.
</Note>

When a local task fires, a new session appears under a **Scheduled** section in the sidebar. Open it to see what Claude did, review changes, or respond to permission prompts. Claude can edit files, run commands, create commits, and open pull requests, the same as in a session you start yourself.

## Missed runs

When the app starts or your computer wakes, Desktop checks whether each task missed any runs in the last seven days. If it did, Desktop starts exactly one catch-up run for the most recently missed time and discards anything older. A daily task that missed six days runs once on wake. Desktop shows a notification when a catch-up run starts.

Keep this in mind when writing prompts. A task scheduled for 9am might run at 11pm if your computer was asleep all day. If timing matters, add guardrails to the prompt itself, for example: "Only review today's commits. If it's after 5pm, skip the review and post a summary of what was missed."

## Permissions for scheduled tasks

Each task has its own permission mode, which you set when creating or editing the task. Allow rules from `~/.claude/settings.json` also apply to scheduled task sessions. If a task runs in [Manual mode](/docs/en/desktop#choose-a-permission-mode) and needs to run a tool it doesn't have permission for, the run stalls until you approve it. The session stays open in the sidebar so you can answer later.

To avoid stalls, click **Run now** after creating a task, watch for permission prompts, and select "always allow" for each one. Future runs of that task auto-approve the same tools without prompting. You can review and revoke these approvals from the task's detail page.

MCP tools marked [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool) prompt on every call and don't offer an always-allow option. Runs that call these tools stall each time.

## Manage scheduled tasks

In the **Code** tab, click **Scheduled** in the sidebar, then click a task in the list to open its detail page. From here you can:

* **Run now**: start the task immediately without waiting for the next scheduled time
* **Status**: toggle between Active and Paused to pause or resume scheduled runs without deleting the task
* **Edit**: change the instructions, schedule, folder, or other settings
* **Review history**: see every past run, including skipped runs. Hover a skipped entry to see why: your computer was asleep, the previous run was still in progress, or other scheduled tasks were already running. Click **Show more** to load older entries.
* **Review allowed permissions**: see and revoke saved tool approvals for this task from the **Always allowed** panel
* **Delete**: remove the task and archive all sessions it created. An **Also delete files on disk** checkbox appears in the confirmation dialog; check it to also remove the task's `SKILL.md` file and associated data from `~/.claude/scheduled-tasks/`.

You can also list, create, edit, and pause tasks by asking Claude in any Desktop session. For example, "pause my dependency-audit task" or "show me my scheduled tasks." To delete a task, use the **Delete** button on its detail page.

A scheduled task can also modify its own schedule or prompt from within a running session using the `update_scheduled_task` MCP tool. This lets a task reschedule itself based on what it finds, for example, rescheduling a code review to run earlier when it detects a release branch has been created.

To edit a task's prompt on disk, open `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (or under [`CLAUDE_CONFIG_DIR`](/docs/en/env-vars) if set). The file uses YAML frontmatter for `name` and `description`, with the prompt as the body. Changes take effect on the next run. Schedule, folder, model, and enabled state are not in this file: change them through the Edit form or ask Claude.

## Related resources

* [Cloud scheduled tasks](/docs/en/routines): run tasks in the cloud on a schedule, via API call, or in response to GitHub events, even when your computer is off
* [Run prompts on a schedule](/docs/en/scheduled-tasks): session-scoped scheduling with `/loop` in the CLI
* [Claude Code GitHub Actions](/docs/en/github-actions): run Claude on a schedule in CI instead of on your machine
* [Use Claude Code Desktop](/docs/en/desktop): the full Desktop app guide
