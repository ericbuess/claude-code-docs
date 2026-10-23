> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Schedule recurring tasks in Claude Code Desktop

> Set up scheduled tasks in Claude Code Desktop to run Claude automatically on a recurring basis for daily code reviews, dependency audits, or morning briefings.

Scheduled tasks start a new session automatically at a time and frequency you choose. Use them for recurring work like daily code reviews, dependency update checks, or morning briefings that pull from your calendar and inbox.

The Desktop app's **Scheduled tasks** page lists both local scheduled tasks and [cloud scheduled tasks](https://code.claude.com/docs/en/routines.md), formerly routines:

* **Local task**: runs on your machine with direct access to your files and tools, but only fires while the app is open and your computer is awake
* **Cloud task**: runs even when your computer is off, and can also start on API calls or GitHub events

This page covers local scheduled tasks; for cloud scheduled tasks and their trigger options, see [Automate work with scheduled tasks](https://code.claude.com/docs/en/routines.md).

## Compare scheduling options

Claude Code offers three ways to schedule recurring or one-off work:

| | [Cloud](https://code.claude.com/docs/en/routines.md) | [Desktop](https://code.claude.com/docs/en/desktop-scheduled-tasks.md) | [`/loop`](https://code.claude.com/docs/en/scheduled-tasks) |
| :- | :- | :- | :- |
| Runs on | Cloud, Anthropic-managed by default | Your machine | Your machine |
| Requires machine on | No | Yes | Yes |
| Requires open session | No | No | Yes |
| Persistent across restarts | Yes | Yes | Restored on `--resume`, with [exceptions](https://code.claude.com/docs/en/scheduled-tasks.md#limitations) |
| Access to local files | No (fresh clone) | Yes | Yes |
| MCP servers | Connectors configured per task | [Config files](https://code.claude.com/docs/en/mcp.md) and connectors | Inherits from session |
| Permission prompts | [Auto mode](https://code.claude.com/docs/en/routines.md#permission-prompts-during-a-run) by default | Configurable per task | Inherits from session |
| Customizable schedule | Yes | Yes | Yes |
| Minimum interval | 1 hour | 1 minute when Claude sets it, [1 hour in the forms](https://code.claude.com/docs/en/desktop-scheduled-tasks.md#schedule-options) | 1 minute |

> [!TIP]
>
> Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.

> [!NOTE]
>
> By default, local scheduled tasks run against whatever state your working directory is in, including uncommitted changes. To give each run its own [isolated Git worktree](https://code.claude.com/docs/en/desktop.md#run-a-session-in-its-own-worktree) instead, select **Worktree** in the task's [**Edit** form](#manage-scheduled-tasks) after you create it. The checkbox is available when the task's folder is a Git repository.

## Create a scheduled task

Local scheduled tasks require Claude Desktop 1.1.5368 or later.

**1. Open the Scheduled tasks page**

In the [**Code** tab](https://code.claude.com/docs/en/desktop.md), click **Scheduled** in the sidebar or in the sidebar's **More** menu.

**2. Start a new task**

Click **New task**. If a menu opens with **Create with Claude** and **Set up manually**, select **Set up manually**. The **New scheduled task** dialog opens. If **Only on this computer** is at the top of the dialog, go to [Dialog with Only on this computer at the top](#dialog-with-only-on-this-computer-at-the-top) before you enter anything.

**3. Name the task**

Enter a name in the **Name** field. Desktop converts it to lowercase kebab-case and uses it as the task's folder name on disk, so the name must be unique across your tasks.

**4. Write the instructions**

In the box below the name, enter what Claude should do when the task runs.

**5. Turn on Only on this computer**

Skip past the **Trigger** card for now and expand **Advanced settings** below it. On the **General** tab, turn on **Only on this computer**. With it on, the task runs on your machine in a local folder.

If the switch is unavailable, clear the repository or the GitHub event or API trigger, because those make the task a [cloud scheduled task](https://code.claude.com/docs/en/routines.md).

**6. Pick the local folder**

In the **Local folder** row, select a folder. **Create** stays unavailable until you pick one.

**7. Set the schedule**

Back in the **Trigger** card, select a [schedule preset](#schedule-options).

**8. Choose the permission mode and model**

In the instructions box's toolbar, select a [permission mode](#permissions-for-scheduled-tasks) and model. If you leave them unchanged, runs use your Claude Code settings and the default model.

**9. Create the task**

Click **Create**. If you haven't trusted the folder yet, Desktop asks you to trust it at this point. The task's detail page opens.

On the detail page, click the pencil icon to open the [**Edit** form](#manage-scheduled-tasks). There you can change the **Description** that Desktop filled in from your instructions, select **Worktree**, or switch the schedule to **Manual** or **Custom**.

You can also create a task by describing what you want in any session. For example, "set up a daily code review that runs every morning at 9am" creates a recurring task. A request like "remind me at 3pm tomorrow to check the deploy" creates a one-time task that disables itself after it fires.

### Dialog with Only on this computer at the top

If **Only on this computer** is at the top of the **New scheduled task** dialog when it opens, turn it on before you enter anything. When you turn it on, a separate blank form for a local task replaces the form.

Then fill in the local form's fields:

* **Name**: enter a name, as in the [steps to create a scheduled task](#create-a-scheduled-task).
* **Description**: enter a description. **Create** stays unavailable until you do.
* **The instructions box**: enter what Claude should do when the task runs. Select the permission mode and model from the menus in the box.
* **Working folder**: select the folder the task runs in. **Create** stays unavailable until you select one.
* **Trigger**: select a schedule. For the presets, see [Schedule options](#schedule-options).

Click **Create**. The task's detail page opens.

## Schedule options

When you turn on **Only on this computer** under **Advanced settings**, the **Trigger** card offers Hourly, Daily, Weekdays, and Weekly. To get **Manual** or **Custom** for such a task, open its [**Edit** form](#manage-scheduled-tasks) after you create it. That form and the [dialog with **Only on this computer** at the top](#dialog-with-only-on-this-computer-at-the-top) offer these six options:

* **Hourly**: runs every hour
* **Daily**: runs every day at the local time you pick
* **Weekdays**: same as Daily but skips Saturday and Sunday
* **Weekly**: shows a time picker and a day picker
* **Manual**: no schedule, only runs when you click **Run now**. Useful for saving a prompt you trigger on demand
* **Custom**: runs on a cron expression that you enter and that is evaluated in your local time, such as `0 9 * * *` for 9:00 AM each day. Write days of the week and months as numbers, since their names aren't accepted. Sunday is `0`, not `7`. The form rejects an expression that runs more often than once per hour.

You can also ask Claude in any Desktop session to set the schedule. Claude isn't held to the once-per-hour limit and can set a single run at a future time. For example, ask "run the test suite every 30 minutes" or "next Monday at 9am, summarize the pull requests merged since Friday."

## How scheduled tasks run

Local scheduled tasks run on your machine. Desktop checks the schedule every minute while the app is open and starts a fresh session when a task is due, independent of any manual sessions you have open. Each task gets a small delay of a few minutes after the scheduled time to stagger API traffic. The delay is deterministic: the same task always starts at the same offset.

Tasks only run while the desktop app is running and your computer is awake. If your computer sleeps through a scheduled time, the run is skipped. To prevent idle-sleep, turn on **Keep computer awake** in **Settings > This computer > System**. Closing the laptop lid still puts it to sleep.

> [!NOTE]
>
> For tasks that need to run even when your computer is off, or that should trigger on an API call or GitHub event, create a [cloud scheduled task](https://code.claude.com/docs/en/routines.md) instead.

### Find a run's session

To open the session a run started, go to the task's [detail page](#manage-scheduled-tasks) and click that run's row in the **History** list.

The sidebar's session list can show a **Scheduled** group as well, with one row per task. To open the session of a task's latest run, click the task's row in that group. To show the group, [check which layout you have](https://code.claude.com/docs/en/desktop.md#check-which-layout-you-have):

* **Current layout**: open the [**Group and sort** menu](https://code.claude.com/docs/en/desktop.md#organize-and-find-sessions), select **Show**, then select **Scheduled**. The group starts collapsed, so click its heading to expand it. **Show** lists **Scheduled** when at least one of your tasks is **Active**, the **Status** a task's detail page shows. If it isn't listed, use the **History** list, which works whether or not the group shows.
* **Earlier layout**: the group is in the session list with nothing to turn on

In a run's session, whichever way you reached it, you can see what Claude did, review changes, and respond to permission prompts. Claude can edit files, run commands, create commits, and open pull requests, the same as in a session you start yourself.

## Missed runs

When the app starts or your computer wakes, Desktop checks whether each task missed any runs in the last seven days. If it did, Desktop starts exactly one catch-up run for the most recently missed time and discards anything older. A daily task that missed six days runs once on wake. Desktop shows a notification when a catch-up run starts.

Keep this in mind when writing prompts. A task scheduled for 9am might run at 11pm if your computer was asleep all day. If timing matters, add guardrails to the prompt itself, for example: "Only review today's commits. If it's after 5pm, skip the review and post a summary of what was missed."

## Permissions for scheduled tasks

Each task has its own permission mode, which you set when creating or editing the task. Allow rules from `~/.claude/settings.json` also apply to scheduled task sessions. If a task runs in [Manual mode](https://code.claude.com/docs/en/desktop.md#choose-a-permission-mode) and needs to run a tool it doesn't have permission for, the run stalls until you approve it. To approve it, [find the run's session](#find-a-runs-session) and answer the permission prompt there.

To avoid stalls, click **Run now** after creating a task, watch for permission prompts, and select "always allow" for each one. Future runs of that task auto-approve the same tools without prompting. You can review and revoke these approvals from the task's detail page.

MCP tools marked [`requiresUserInteraction`](https://code.claude.com/docs/en/mcp#require-approval-for-a-specific-tool) prompt on every call and don't offer an always-allow option. Runs that call these tools stall each time.

## Manage scheduled tasks

In the **Code** tab, click **Scheduled** in the sidebar, then click a task in the list to open its detail page. From here you can:

* **Run now**: start the task immediately without waiting for the next scheduled time
* **Status**: toggle between Active and Paused to pause or resume scheduled runs without deleting the task
* **Edit**: change the instructions, schedule, folder, or other settings
* **Review history**: see every past run, including skipped runs. Hover a skipped entry to see why: your computer was asleep, the previous run was still in progress, or other scheduled tasks were already running. Click **Show more** to load older entries.
* **Review allowed permissions**: see and revoke saved tool approvals for this task from the **Always allowed** panel
* **Delete**: remove the task. The sessions the task created are [archived](https://code.claude.com/docs/en/desktop.md#organize-and-find-sessions), not deleted. The folder holding the task's `SKILL.md` file stays on disk at `~/.claude/scheduled-tasks/<task-name>/`, or at `scheduled-tasks/<task-name>/` under [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars) if you set that variable. To remove that folder, delete it yourself.

You can also list, create, edit, and pause tasks by asking Claude in any Desktop session. For example, "pause my dependency-audit task" or "show me my scheduled tasks." To delete a task, use the **Delete** button on its detail page.

A scheduled task can also modify its own schedule or prompt from within a running session using the `update_scheduled_task` MCP tool. This lets a task reschedule itself based on what it finds, for example, rescheduling a code review to run earlier when it detects a release branch has been created.

To edit a task's prompt on disk, open `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (or under [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars) if set). The file uses YAML frontmatter for `name` and `description`, with the prompt as the body. Changes take effect on the next run. Schedule, folder, model, and enabled state are not in this file: change them through the Edit form or ask Claude.

## Related resources

* [Cloud scheduled tasks](https://code.claude.com/docs/en/routines.md): run tasks in the cloud on a schedule, via API call, or in response to GitHub events, even when your computer is off
* [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks.md): session-scoped scheduling with `/loop` in the CLI
* [Claude Code GitHub Actions](https://code.claude.com/docs/en/github-actions.md): run Claude on a schedule in CI instead of on your machine
* [Use Claude Code Desktop](https://code.claude.com/docs/en/desktop.md): the full Desktop app guide
