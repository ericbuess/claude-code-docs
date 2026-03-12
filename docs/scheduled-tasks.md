> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Run prompts on a schedule

> Use /loop and the cron scheduling tools to run prompts repeatedly, poll for status, or set one-time reminders within a Claude Code session.

<Note>
  Scheduled tasks require Claude Code v2.1.72 or later. Check your version with `claude --version`.
</Note>

Scheduled tasks let Claude re-run a prompt automatically on an interval. Use them to poll a deployment, babysit a PR, check back on a long-running build, or remind yourself to do something later in the session.

Tasks are session-scoped: they live in the current Claude Code process and are gone when you exit. For durable scheduling that survives restarts and runs without an active terminal session, see [Desktop scheduled tasks](/en/desktop#schedule-recurring-tasks) or [GitHub Actions](/en/github-actions).

## Schedule a recurring prompt with /loop

The `/loop` [bundled skill](/en/skills#bundled-skills) is the quickest way to schedule a recurring prompt. Pass an optional interval and a prompt, and Claude sets up a cron job that fires in the background while the session stays open.

```text  theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude parses the interval, converts it to a cron expression, schedules the job, and confirms the cadence and job ID.

### Interval syntax

Intervals are optional. You can lead with them, trail with them, or leave them out entirely.

| Form                    | Example                               | Parsed interval              |
| :---------------------- | :------------------------------------ | :--------------------------- |
| Leading token           | `/loop 30m check the build`           | every 30 minutes             |
| Trailing `every` clause | `/loop check the build every 2 hours` | every 2 hours                |
| No interval             | `/loop check the build`               | defaults to every 10 minutes |

Supported units are `s` for seconds, `m` for minutes, `h` for hours, and `d` for days. Seconds are rounded up to the nearest minute since cron has one-minute granularity. Intervals that don't divide evenly into their unit, such as `7m` or `90m`, are rounded to the nearest clean interval and Claude tells you what it picked.

### Loop over another command

The scheduled prompt can itself be a command or skill invocation. This is useful for re-running a workflow you've already packaged.

```text  theme={null}
/loop 20m /review-pr 1234
```

Each time the job fires, Claude runs `/review-pr 1234` as if you had typed it.

## Set a one-time reminder

For one-shot reminders, describe what you want in natural language instead of using `/loop`. Claude schedules a single-fire task that deletes itself after running.

```text  theme={null}
remind me at 3pm to push the release branch
```

```text  theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude pins the fire time to a specific minute and hour using a cron expression and confirms when it will fire.

## Manage scheduled tasks

Ask Claude in natural language to list or cancel tasks, or reference the underlying tools directly.

```text  theme={null}
what scheduled tasks do I have?
```

```text  theme={null}
cancel the deploy check job
```

Under the hood, Claude uses these tools:

| Tool         | Purpose                                                                                                         |
| :----------- | :-------------------------------------------------------------------------------------------------------------- |
| `CronCreate` | Schedule a new task. Accepts a 5-field cron expression, the prompt to run, and whether it recurs or fires once. |
| `CronList`   | List all scheduled tasks with their IDs, schedules, and prompts.                                                |
| `CronDelete` | Cancel a task by ID.                                                                                            |

Each scheduled task has an 8-character ID you can pass to `CronDelete`. A session can hold up to 50 scheduled tasks at once.

## How scheduled tasks run

The scheduler checks every second for due tasks and enqueues them at low priority. A scheduled prompt fires between your turns, not while Claude is mid-response. If Claude is busy when a task comes due, the prompt waits until the current turn ends.

All times are interpreted in your local timezone. A cron expression like `0 9 * * *` means 9am wherever you're running Claude Code, not UTC.

### Jitter

To avoid every session hitting the API at the same wall-clock moment, the scheduler adds a small deterministic offset to fire times:

* Recurring tasks fire up to 10% of their period late, capped at 15 minutes. An hourly job might fire anywhere from `:00` to `:06`.
* One-shot tasks scheduled for the top or bottom of the hour fire up to 90 seconds early.

The offset is derived from the task ID, so the same task always gets the same offset. If exact timing matters, pick a minute that is not `:00` or `:30`, for example `3 9 * * *` instead of `0 9 * * *`, and the one-shot jitter will not apply.

### Three-day expiry

Recurring tasks automatically expire 3 days after creation. The task fires one final time, then deletes itself. This bounds how long a forgotten loop can run. If you need a recurring task to last longer, cancel and recreate it before it expires, or use [Desktop scheduled tasks](/en/desktop#schedule-recurring-tasks) for durable scheduling.

## Cron expression reference

`CronCreate` accepts standard 5-field cron expressions: `minute hour day-of-month month day-of-week`. All fields support wildcards (`*`), single values (`5`), steps (`*/15`), ranges (`1-5`), and comma-separated lists (`1,15,30`).

| Example        | Meaning                      |
| :------------- | :--------------------------- |
| `*/5 * * * *`  | Every 5 minutes              |
| `0 * * * *`    | Every hour on the hour       |
| `7 * * * *`    | Every hour at 7 minutes past |
| `0 9 * * *`    | Every day at 9am local       |
| `0 9 * * 1-5`  | Weekdays at 9am local        |
| `30 14 15 3 *` | March 15 at 2:30pm local     |

Day-of-week uses `0` or `7` for Sunday through `6` for Saturday. Extended syntax like `L`, `W`, `?`, and name aliases such as `MON` or `JAN` is not supported.

When both day-of-month and day-of-week are constrained, a date matches if either field matches. This follows standard vixie-cron semantics.

## Disable scheduled tasks

Set `CLAUDE_CODE_DISABLE_CRON=1` in your environment to disable the scheduler entirely. The cron tools and `/loop` become unavailable, and any already-scheduled tasks stop firing. See [Environment variables](/en/settings#environment-variables) for the full list of disable flags.

## Limitations

Session-scoped scheduling has inherent constraints:

* Tasks only fire while Claude Code is running and idle. Closing the terminal or letting the session exit cancels everything.
* No catch-up for missed fires. If a task's scheduled time passes while Claude is busy on a long-running request, it fires once when Claude becomes idle, not once per missed interval.
* No persistence across restarts. Restarting Claude Code clears all session-scoped tasks.

For cron-driven automation that needs to run unattended, use a [GitHub Actions workflow](/en/github-actions) with a `schedule` trigger, or [Desktop scheduled tasks](/en/desktop#schedule-recurring-tasks) if you want a graphical setup flow.
