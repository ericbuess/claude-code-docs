> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Run agents in parallel

> Compare the ways Claude Code can take on multiple tasks at once: subagents, agent view, agent teams, and dynamic workflows.

[Subagents](/en/sub-agents), [agent view](/en/agent-view), [agent teams](/en/agent-teams), and [dynamic workflows](/en/workflows) each parallelize work in a different way. The right one depends on whether you want to stay in each conversation yourself, hand tasks off and check back later, or have Claude coordinate a group of workers for you.

| Approach                           | What it gives you                                                                                                                                         | Use it when                                                                                                                                                                                         |
| :--------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Subagents](/en/sub-agents)        | Delegated workers inside one session that do a side task in their own context and return a summary                                                        | A side task would flood your main conversation with search results, logs, or file contents you won't reference again                                                                                |
| [Agent view](/en/agent-view)       | One screen to dispatch and monitor sessions running in the background, opened with `claude agents`. Research preview                                      | You have several independent tasks and want to hand them off, check status at a glance, and step in only when one needs you                                                                         |
| [Agent teams](/en/agent-teams)     | Multiple coordinated sessions with a shared task list and inter-agent messaging, managed by a lead. Experimental and disabled by default                  | You want Claude to split a project into pieces, assign them, and keep the workers in sync                                                                                                           |
| [Dynamic workflows](/en/workflows) | A script that runs many subagents and cross-checks their results, for work too big to coordinate one turn at a time or that needs more than a single pass | A job outgrows a handful of subagents, or you want findings verified against each other: a codebase-wide audit, a 500-file migration, cross-checked research, or a plan drafted from several angles |

In every approach the workers are Claude sessions. To involve a different tool, expose it to Claude as an [MCP server](/en/mcp).

Two more tools support this work without being a way to run agents themselves:

* [Worktrees](/en/worktrees) give each session a separate git checkout, so parallel sessions never edit the same files. Use them for sessions you run yourself. Agent view moves each dispatched session into its own worktree automatically, and subagents you spawn can each get one too.
* [`/batch`](/en/commands) is a [skill](/en/skills) that has Claude split one large change into 5 to 30 worktree-isolated subagents that each open a pull request. It's a packaged use of subagents and worktrees, not a separate coordination style.

A few other features run Claude without you driving each step, but they solve a different problem than splitting work across agents:

* A [background bash command](/en/interactive-mode#background-bash-commands) runs one shell command without blocking the conversation. It doesn't spawn an agent.
* A [forked subagent](/en/sub-agents#fork-the-current-conversation) is a subagent that inherits your full conversation context instead of starting fresh. It's a way to spawn a subagent, not a separate surface.
* A [routine](/en/routines) runs a session on a schedule in Anthropic's cloud, not in parallel on your machine.

<Note>
  Running several sessions or subagents at once multiplies token usage. See [Costs](/en/costs) for usage and rate-limit details.
</Note>

## Choose an approach

The right approach depends on who coordinates the work, whether the workers need to communicate, and whether they edit the same files:

* **Who coordinates the work?**
  * Claude delegates and collects results inside one conversation: [subagents](/en/sub-agents)
  * You hand off independent tasks and check back later: [agent view](/en/agent-view)
  * Claude plans, assigns, and supervises a group of workers: [agent teams](/en/agent-teams), experimental and disabled by default
  * A script holds the plan instead of Claude's turn-by-turn judgment: [dynamic workflows](/en/workflows). See [how workflows compare to subagents and skills](/en/workflows#when-to-use-a-workflow)
* **Do the workers need to talk to each other?** Subagents report results back to the conversation that spawned them, and agent view sessions report only to you. Teammates in an agent team share a task list and message each other directly.
* **Do the tasks touch the same files?** Isolate the work with [worktrees](/en/worktrees). Subagents and sessions you run yourself can each use a separate worktree. Agent teams don't isolate teammates in worktrees, so [partition the work](/en/agent-teams#avoid-file-conflicts) so each teammate owns a different set of files.

## Check on running work

The command for checking on running work depends on which approach you used:

* For background sessions, `claude agents` opens [agent view](/en/agent-view): one screen showing every session, its state, and which ones need your input.
* For subagents in the current session, named background subagents appear in the @-mention typeahead with their status. {/* min-version: 2.1.198 */}As of v2.1.198, `/agents` no longer opens a panel; it prints a notice pointing to the subagent file locations. To [create and edit custom subagents](/en/sub-agents#configure-subagents), ask Claude or edit the files directly. Despite the similar name, `/agents` is separate from `claude agents`.
* For anything running in the background of the current session, `/tasks` lists each item and lets you check on, attach to, or stop it. The list also includes subagents that have finished.
* For dynamic workflows, `/workflows` lists running and completed runs, the phase each is in, and how many agents have finished.

For a desktop view of all your sessions, see [parallel sessions in the desktop app](/en/desktop#work-in-parallel-with-sessions).

## Learn more

Each guide below covers setup and configuration for one approach:

* [Create custom subagents](/en/sub-agents): define reusable specialists and control which tools they can use.
* [Manage agents with agent view](/en/agent-view): dispatch sessions, watch their state, and attach when one needs you.
* [Orchestrate agent teams](/en/agent-teams): set up a lead and teammates, assign tasks, and review their work.
* [Orchestrate dynamic workflows](/en/workflows): run a bundled workflow or have Claude write one that runs many subagents and verifies their findings against each other.
* [Run parallel sessions with worktrees](/en/worktrees): start Claude in an isolated checkout, control what gets copied in, and clean up afterward.
