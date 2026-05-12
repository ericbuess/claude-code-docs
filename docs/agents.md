> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Run agents in parallel

> Compare the ways Claude Code can take on multiple tasks at once: subagents, agent view, agent teams, and isolated worktree sessions.

[Subagents](/en/sub-agents), [agent view](/en/agent-view), [agent teams](/en/agent-teams), and [worktrees](/en/worktrees) each parallelize work in a different way. The right one depends on whether you want to stay in each conversation yourself, hand tasks off and check back later, or have Claude coordinate a group of workers for you.

| Approach                       | What it gives you                                                                                                                        | Use it when                                                                                                                 |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| [Subagents](/en/sub-agents)    | Delegated workers inside one session that do a side task in their own context and return a summary                                       | A side task would flood your main conversation with search results, logs, or file contents you won't reference again        |
| [Agent view](/en/agent-view)   | One screen to dispatch and monitor sessions running in the background, opened with `claude agents`. Research preview                     | You have several independent tasks and want to hand them off, check status at a glance, and step in only when one needs you |
| [Agent teams](/en/agent-teams) | Multiple coordinated sessions with a shared task list and inter-agent messaging, managed by a lead. Experimental and disabled by default | You want Claude to split a project into pieces, assign them, and keep the workers in sync                                   |
| [Worktrees](/en/worktrees)     | Separate git checkouts so parallel sessions never touch each other's files                                                               | You're running several sessions yourself, or your subagents edit overlapping files                                          |
| [`/batch`](/en/commands)       | A planned split of one large change into 5 to 30 worktree-isolated subagents that each open a pull request                               | A repo-wide migration or mechanical refactor you can describe in one instruction                                            |

In every approach the workers are Claude sessions. To involve a different tool, expose it to Claude as an [MCP server](/en/mcp).

You can combine these approaches. Agent view automatically moves each dispatched session into its own worktree when it needs to edit files, and a session you're working in can spawn subagents that each get their own worktree.

<Note>
  Running several sessions or subagents at once multiplies token usage. See [Costs](/en/costs) for usage and rate-limit details.
</Note>

## Choose an approach

The right approach depends on who coordinates the work, whether the workers need to communicate, and whether they edit the same files:

* **Who coordinates the work?** If you want Claude to delegate and collect results inside one conversation, use [subagents](/en/sub-agents). If you're handing off independent tasks and checking back on them, use [agent view](/en/agent-view). If you want Claude to plan, assign, and supervise a group of workers, use [agent teams](/en/agent-teams), which are experimental and disabled by default.
* **Do the workers need to talk to each other?** Subagents report results back to the conversation that spawned them, and agent view sessions report only to you. Teammates in an agent team share a task list and message each other directly.
* **Do the tasks touch the same files?** Isolate the work with [worktrees](/en/worktrees). Subagents and sessions you run yourself can each use a separate worktree. Agent teams don't isolate teammates in worktrees, so [partition the work](/en/agent-teams#avoid-file-conflicts) so each teammate owns a different set of files.

## Check on running work

The command for checking on running work depends on which approach you used:

* For background sessions, `claude agents` opens [agent view](/en/agent-view): one screen showing every session, its state, and which ones need your input.
* For subagents in the current session, `/agents` opens a panel with a **Running** tab listing live subagents and a **Library** tab where you [create and edit custom subagents](/en/sub-agents#use-the-%2Fagents-command). Despite the similar name, this is separate from `claude agents`.
* For anything running in the background of the current session, `/tasks` lists each item and lets you check on, attach to, or stop it.

For a desktop view of all your sessions, see [parallel sessions in the desktop app](/en/desktop#work-in-parallel-with-sessions).

## Learn more

Each guide below covers setup and configuration for one approach:

* [Create custom subagents](/en/sub-agents): define reusable specialists and control which tools they can use.
* [Manage agents with agent view](/en/agent-view): dispatch sessions, watch their state, and attach when one needs you.
* [Orchestrate agent teams](/en/agent-teams): set up a lead and teammates, assign tasks, and review their work.
* [Run parallel sessions with worktrees](/en/worktrees): start Claude in an isolated checkout, control what gets copied in, and clean up afterward.
