> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Orchestrate subagents at scale with dynamic workflows

> Dynamic workflows orchestrate many subagents from a script Claude writes and you can rerun. Use them for codebase audits, large migrations, and cross-checked research.

> [!NOTE]
>
> Dynamic workflows are available on all paid plans, with Anthropic API access, and on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry. On Pro, turn them on from the Dynamic workflows row in `/config`.

A dynamic workflow is a JavaScript script that orchestrates many [subagents](https://code.claude.com/docs/en/sub-agents.md) at once. Claude writes the script for the task you describe, and a runtime executes it in the background while your session stays responsive.

Reach for a workflow when a task needs more agents than one conversation can coordinate, or when you want the orchestration codified as a script you can read and rerun. Examples include a codebase-wide bug sweep, a 500-file migration, a research question that needs sources cross-checked against each other, and a hard plan worth drafting from several independent angles before you commit to one.

## When to use a workflow

[Subagents](https://code.claude.com/docs/en/sub-agents.md), [skills](https://code.claude.com/docs/en/skills.md), [agent teams](https://code.claude.com/docs/en/agent-teams.md), and workflows can all run a multi-step task. The difference is who holds the plan:

| | Subagents | Skills | Agent teams | Workflows |
| :- | :- | :- | :- | :- |
| What it is | A worker Claude spawns | Instructions Claude follows | A lead agent supervising peer sessions | A script the runtime executes |
| Who decides what runs next | Claude, turn by turn | Claude, following the prompt | The lead agent, turn by turn | The script |
| Where intermediate results live | Claude's context window | Claude's context window | A shared task list | Script variables |
| What's repeatable | The worker definition | The instructions | The team definition | The orchestration itself |
| Scale | A few delegated tasks per turn | Same as subagents | A handful of long-running peers | Dozens to hundreds of agents per run |
| Interruption | Restarts the turn | Restarts the turn | Teammates keep running | Resumable in the same session |

A workflow moves the plan into code. With subagents, skills, and agent teams, Claude is the orchestrator: it decides turn by turn what to spawn or assign next, and every result goes into a context window. A workflow script holds the loop, the branching, and the intermediate results itself, so Claude's context holds only the final answer.

Moving the plan into code also lets a workflow apply a repeatable quality pattern, not just run more agents: it can have independent agents adversarially review each other's findings before they're reported, or draft a plan from several angles and weigh them against each other, so you get a more trustworthy result than a single pass.

## Run a bundled workflow

The quickest way to see a workflow in action is to run `/deep-research`, the [built-in workflow](#bundled-workflows) Claude Code includes for investigating a question across many sources. You'll see agents work through a set of phases in the background while your session stays free, and get one report at the end instead of a turn-by-turn transcript.

**1. Run the workflow**

Run `/deep-research` with a question you want investigated. It fans out web searches across several angles, fetches and cross-checks the sources it finds, and synthesizes a cited report.

```text wrap theme={null}
/deep-research What changed in the Node.js permission model between v20 and v22?
```

**2. Allow workflows**

Claude Code asks whether to allow the workflow. Select **Yes** to continue. The exact prompt depends on your permission mode. See [Approve the plan before it runs](#approve-the-plan-before-it-runs) for the per-mode options.

**3. Watch progress**

The run starts in the background. Run `/workflows` to open its progress view:

```text wrap theme={null}
/workflows
```

If `/workflows` shows a list of runs instead, select the run you just started and press Enter. The view shows each phase with its agent count. Drill into any phase to see its agents and what each one found. See [Watch the run](#watch-the-run) for the full set of controls.

You can also watch from the task panel below the input box: a one-line progress summary appears there while the run is going. Press the down arrow to focus it, then Enter to expand.

**4. Read the report**

When the run finishes, the report appears in your session. It cites the sources each claim came from, with claims that didn't survive cross-checking already filtered out.

When the verifier agents can't check a claim, such as after a rate limit or API error, the report lists that claim as unverified instead of counting it as refuted.

To run a workflow for your own task, [have Claude write one](#have-claude-write-a-workflow), and once a run does what you wanted you can [save it](#save-the-workflow-for-reuse) as a command of your own.

### Bundled workflows

Claude Code includes `/deep-research` as a built-in workflow:

| Command | What it does |
| :- | :- |
| `/deep-research <question>` | Fans out web searches on a question across several angles, fetches and cross-checks the sources it finds, votes on each claim, and returns a cited report with claims that didn't survive cross-checking filtered out. Requires the [WebSearch tool](https://code.claude.com/docs/en/tools-reference.md#websearch-tool-behavior) to be available |

`/deep-research` runs only when you invoke it.

[Workflows you save](#save-the-workflow-for-reuse) yourself become commands the same way and appear in `/` autocomplete alongside the bundled ones.

### Watch the run

Workflows run in the background, so the session stays responsive while agents work. Run `/workflows` at any time to list running and completed workflows, then select one to open its progress view. When the session has only one run, `/workflows` skips the list and opens that run. To stop a running workflow from the list without opening it, select it and press `x`.

The progress view shows each phase with its agent counts. The footer lists the key for each action:

| Key | Action |
| :- | :- |
| `↑` / `↓` | Select a phase or agent |
| `Enter` or `→` | Drill into the selected phase, then into an agent's detail. In the detail, `Enter` expands or collapses it |
| `Esc` or `←` | Back out one level |
| `j` / `k` | Scroll within the agent detail when it overflows |
| `f` | Filter the agent list in the selected phase by status. Press again to cycle |
| `p` | Pause or resume the run |
| `x` | Stop the selected agent, or stop the whole workflow when focus is on the run |
| `r` | Restart the selected running agent |
| `s` | [Save](#save-the-workflow-for-reuse) the run's script as a command |

The agent detail lists the agent's prompt, its recent tool calls, and its result. Each call shows its state, such as still running or failed. When the agent keeps a task list of its own, the detail shows it too, with each task's status.

Press `Enter` to expand the detail. The prompt and result then show in full, and each listed call shows its input and the start of its result.

## Have Claude write a workflow

You can have Claude write a workflow for your task in two ways:

* [Ask for a workflow](#ask-for-a-workflow-in-your-prompt) in your prompt, either in your own words or by including the keyword `ultracode`, and Claude writes one for the task.
* [Let Claude decide with ultracode](#let-claude-decide-with-ultracode): set `/effort ultracode` and Claude plans a workflow for every substantive task in the session.

You can also run a workflow command that already exists: a [bundled workflow](#bundled-workflows) like `/deep-research`, or one you've [saved](#save-the-workflow-for-reuse).

### Ask for a workflow in your prompt

To run a single task as a workflow without changing the session's effort level, include the keyword `ultracode` in your prompt. Asking in your own words, for example "use a workflow" or "run a workflow", also works: Claude treats a direct request as the same opt-in.

```text wrap theme={null}
ultracode: audit every API endpoint under src/routes/ for missing auth checks
```

Claude Code highlights the keyword in your input and Claude writes a workflow script for the task instead of working through it turn by turn. The keyword only chooses how Claude structures the work: the agents' tool calls receive the same permission checks and [sandboxing](https://code.claude.com/docs/en/sandboxing.md) as any other tool call in the session.

If the run does what you wanted, you can [save it as a command](#save-the-workflow-for-reuse) afterward. If you already have an orchestrator built another way, such as a folder of subagent prompts or a skill that fans work out, you can point Claude at it and ask for a workflow that does the same thing.

#### Dismiss or turn off the keyword

If you didn't mean to start a workflow, press `Option+W` on macOS or `Alt+W` on Windows and Linux to dismiss the highlight for this prompt, or press backspace while the cursor is right after the highlighted keyword. To stop the keyword from triggering at all, turn off Ultracode keyword trigger in `/config`.

#### Where the keyword works

The keyword is an opt-in only in a prompt you type yourself: at the interactive prompt, in an IDE extension panel, in a [Remote Control](https://code.claude.com/docs/en/remote-control.md) client, or in an Agent SDK application that stamps your keyboard input's [`origin`](https://code.claude.com/docs/en/agent-sdk/typescript#sdkmessageorigin) as `{ kind: "human" }`. It doesn't start a workflow when it reaches the session another way:

* a prompt passed with `-p`
* a prompt an Agent SDK application sends without stamping it as human input
* a scheduled task prompt
* a webhook payload or pull request comment relayed into the conversation

### Let Claude decide with ultracode

Ultracode is a Claude Code setting that turns on automatic workflow orchestration for the session, at whichever [effort level](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) the session runs at. With it on, Claude plans a workflow for each substantive task instead of waiting for you to ask. Turn it on at the Claude Code prompt:

```text wrap theme={null}
/effort ultracode
```

To start a session with ultracode already on, launch with `claude --effort ultracode`, which also sets the effort level to `xhigh`.

To turn it on from the `/effort` slider, press `Tab` to flip the **Ultracode** toggle, then `Enter` to apply it. [Adjust effort level](https://code.claude.com/docs/en/model-config.md#adjust-effort-level) lists the routes that turn ultracode on.

With ultracode on, Claude decides when a task warrants a workflow. A single request can turn into several workflows in a row: one to understand the code, one to make the change, and one to verify it. This applies to every task in the session, so each request uses more tokens and takes longer than the same request without a workflow. On a subscription plan those tokens draw on your usage limits, so a session with ultracode on reaches a session or weekly limit sooner than the same work with it off.

Turning ultracode on already opts you in to large runs, so these checks don't apply while it's on:

* The [`Large workflow` warning](#cost) doesn't appear on a workflow run
* The session's [concurrent subagent limit](https://code.claude.com/docs/en/sub-agents.md#concurrent-subagent-limit) isn't enforced for the subagents Claude spawns with the Agent tool
* In auto permission mode, you aren't asked to [approve the first workflow launch](#approve-the-plan-before-it-runs)

`/effort ultracode` lasts for the current session; to have every session start with it, set the [`ultracode`](https://code.claude.com/docs/en/settings-reference#ultracode) setting. Turn it off with `/effort ultracode off` when you return to routine work. The `/effort` slider offers the toggle only [when ultracode is available](https://code.claude.com/docs/en/model-config.md#when-ultracode-is-available).

### Approve the plan before it runs

In the CLI, the per-run prompt shows the planned phases and these options:

* **Yes, run it**: start the run
* **Yes, and don't ask again for `<name>` in `<path>`**: start, and skip this prompt for this workflow in this project from now on. Claude Code offers this option when you run a bundled, saved, or plugin workflow by name, not for a script Claude wrote for the current task.
* **View raw script**: read the script before deciding
* **No**: cancel

`Ctrl+G` opens the script in your editor. With **Yes, run it** or **No** selected, press `Tab` to [add a comment](https://code.claude.com/docs/en/permissions.md#add-a-comment-when-you-answer-a-permission-prompt) to your answer.

Whether you see this prompt depends on your [permission mode](https://code.claude.com/docs/en/permission-modes.md):

| Permission mode | When you're prompted |
| :- | :- |
| Auto | First launch only. Any **Yes** records consent in your user settings, and later launches start without prompting. Skipped entirely when ultracode is on |
| Manual, accept edits | Every run, unless you've selected **Yes, and don't ask again** for that workflow in this project |
| Bypass permissions | Claude Code doesn't prompt you. The run starts immediately |
| `claude -p`, Agent SDK | Claude Code doesn't prompt you |

In `claude -p` and the Agent SDK, Claude Code never shows this prompt. It runs the Workflow tool call through the same [permission evaluation](https://code.claude.com/docs/en/agent-sdk/permissions.md#how-permissions-are-evaluated) as the rest of the session, so deny rules, ask rules, and `dontAsk` mode apply to the launch as they apply to every tool call. To let the workflow start in these runs, use one of these:

* **Permission rule**: add `Workflow` to your allow rules to approve every workflow, or `Workflow(<name>)` to approve one saved workflow by name.
* **Auto permission mode**: run in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), where the classifier reviews the call and can approve it.
* **Bypass permissions mode**: run in bypass permissions mode.
* **A hook**: return `"allow"` for the call from a [`PreToolUse`](https://code.claude.com/docs/en/hooks#pretooluse) hook. In [plan mode](https://code.claude.com/docs/en/permission-modes.md#analyze-before-you-edit-with-plan-mode), the workflow doesn't start on the hook's approval alone, so use a permission rule or your host's approval there instead.
* **Your host**: a [`--permission-prompt-tool`](https://code.claude.com/docs/en/cli-reference#cli-flags) or, with the Agent SDK, a [`canUseTool`](https://code.claude.com/docs/en/agent-sdk/permissions) callback approves it.

In the Desktop app, an approval card shows the workflow name, the phase list, and a token-usage caution, with **Once**, **Always**, and **Deny** actions. The progress view appears in the Background tasks side pane.

The subagents the workflow spawns use your [permission rules](https://code.claude.com/docs/en/settings-reference.md#permission-settings), and Claude Code picks their permission mode by the rules under [which permission mode a subagent runs in](https://code.claude.com/docs/en/sub-agents.md#permission-modes). To avoid prompts on a long run, add the tools the agents need to your allow rules before starting.

### Save the workflow for reuse

When Claude writes a workflow for a task you'll repeat, you can save that run's script as a command. A process like a review you run on every branch then runs the same orchestration each time.

Run `/workflows`, select the run you want to keep, and press `s`. In the save dialog, Tab toggles between the two save locations:

* `.claude/workflows/` in your project: shared with everyone who clones the repo
* `~/.claude/workflows/` in your home directory: available in every project, visible only to you. If you set [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars), this location is the `workflows/` directory under that path.

The save dialog shows the resolved path for the personal location.

Press Enter to save. The workflow runs as `/<name>` in future sessions from either location.

Claude Code checks the save location for symlinks before writing, and shows an error instead of writing through one. What it checks depends on where you save:

* Project location: Claude Code refuses if `.claude`, `.claude/workflows`, or the target file is a symlink.
* Personal location: Claude Code refuses only if the target file itself is a symlink, so a `~/.claude` directory managed by a dotfiles tool still works.

Before v2.1.216, Claude Code followed the link, which could place the file outside the location you chose.

In a monorepo with several `.claude/` directories, you can keep workflows alongside the package they apply to. Saving to the project location writes to the closest `.claude/workflows/` directory that already exists between your working directory and the repository root, or to the repository root if none exists yet. Project workflows also load from every `.claude/workflows/` along that path, and when more than one defines the same name Claude Code runs the one closest to the working directory.

If a project workflow and a personal workflow share a name, the project one runs.

### Distribute a workflow in a plugin

To share a workflow across teams or repositories, include it in a [plugin](https://code.claude.com/docs/en/plugins/overview.md). Place the script in a `workflows/` directory at the plugin root, or point to a different location with the [`workflows` manifest field](https://code.claude.com/docs/en/plugins/manifest-reference#fields).

Plugin workflows are namespaced by the plugin name. A plugin called `acme-tools` containing a script whose `meta.name` is `release-audit` runs as `/acme-tools:release-audit`.

### Pass input to a saved workflow

A saved workflow can accept input through the `args` parameter. The script reads it as a global named `args`. Use this to supply a research question, a list of target paths, or a configuration object at invocation time instead of editing the script for each run.

The following prompt runs a saved workflow with a list of issue numbers:

```text wrap theme={null}
Run /triage-issues on issues 1024, 1025, and 1030
```

Claude passes the list as structured data, so the script can call array and object methods on `args` directly without parsing it first. If `args` is omitted, the global is `undefined` inside the script.

## Example workflow prompts

A workflow fits best when the task is larger than one agent can hold in context, or when the same step needs to run across many items. The prompts below show common shapes. Each one asks Claude to write and run a workflow for that task; you don't write the script yourself.

### Audit many files for the same issue

Fan out one agent per file, then collect and verify the findings.

```text wrap theme={null}
use a workflow to audit every route handler under src/routes/ for missing authentication checks, and adversarially verify each finding before reporting it
```

### Keep fixing until a check passes

Run a checker, fix what failed, and repeat until it passes or stops making progress.

```text wrap theme={null}
use a workflow to run npx tsc --noEmit and keep fixing the reported errors until the type check passes or two rounds in a row make no progress
```

### Migrate many files in parallel

Discover the files to migrate, transform each one in an isolated copy so edits don't conflict, and verify each result.

```text wrap theme={null}
use a workflow to migrate every component under src/components/ from JavaScript to TypeScript, working on each file in its own isolated copy
```

### Review every changed file and write one summary

Run a reviewer per file, then pass all the findings to one agent that ranks and deduplicates them.

```text wrap theme={null}
use a workflow to review every file changed in this PR for correctness issues, then merge the per-file findings into one ranked summary
```

### Research a topic across many sources

Fan out readers across changelogs, issues, and docs, then synthesize. The bundled `/deep-research` workflow does this; you can also describe a narrower version.

```text wrap theme={null}
use a workflow to research how our three competitors handle rate limiting: read their public docs and recent changelog entries in parallel, then compare the approaches
```

### Find issues until the list stops growing

Keep searching in rounds and stop when new rounds turn up nothing new.

```text wrap theme={null}
use a workflow to find flaky tests in this repo: run the suite repeatedly, record which tests fail intermittently, and stop once two rounds in a row find nothing new
```

### What the saved script looks like

When you [save a workflow](#save-the-workflow-for-reuse), the file in `.claude/workflows/` holds a `meta` block followed by a script body that orchestrates subagents. You usually don't need to edit it, but here is the shape of a small one so you can recognize what Claude generated:

```javascript theme={null}
export const meta = {
  name: 'audit-routes',
  description: 'Audit every route handler for missing auth checks',
}

const found = await agent('List every .ts file under src/routes/.', {
  schema: { type: 'object', required: ['files'], properties: { files: { type: 'array', items: { type: 'string' } } } },
})

const audits = await pipeline(found.files, file =>
  agent(`Audit ${file} for missing authentication checks.`, { label: file }),
)

return audits.filter(Boolean)
```

The body is plain JavaScript with top-level `await`. `agent()` spawns one subagent, `pipeline()` runs one per item in a list, and `parallel()` runs a set of agent tasks at the same time and waits for all of them.

An `agent()` call resolves to `null` if you stop it mid-run or it hits an unrecoverable API error. `pipeline()` keeps each `null` in the results array, which is why the example ends with `.filter(Boolean)` to drop those entries, including the slot of [an agent that stalled on every attempt](#when-an-agent-stalls-and-restarts).

In [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), the prompt your script passes to `agent()` doesn't count as a request from you when the classifier reviews that subagent's actions, because Claude Code marks it as text the script computed.

If you pass a `schema` on an `agent()` call, that subagent returns JSON matching the shape instead of prose. Claude Code checks the schema before starting the subagent: when it can prove the schema contradicts itself, the call fails with an error naming the contradiction, and the subagent never starts. One contradiction it can prove is a `required` key that `additionalProperties: false` rules out.

If the subagent's output still fails validation after five attempts, the call fails with an error that includes the last validation failure. To change the attempt count, set [`MAX_STRUCTURED_OUTPUT_RETRIES`](https://code.claude.com/docs/en/env-vars).

### Edit a saved script

To change a [workflow you saved](#save-the-workflow-for-reuse), edit its `.js` file or ask Claude to make the change. Before you edit or ask, run the `/workflow-authoring` [bundled skill](https://code.claude.com/docs/en/skills.md#bundled-skills) to load the script-writing reference Claude works from. The skill requires Claude Code v2.1.248 or later.

To run the edited version in the current session, run [`/reload-skills`](https://code.claude.com/docs/en/commands#all-commands) to re-read the workflow directories, then run `/<name>` again.

Claude Code applies these rules to each part of the file when it loads and runs the script:

* **`meta` block**: keep `export const meta` as the first statement, and keep it a plain object literal with a `name` and a `description`. If it contains anything other than literal values, such as a variable, a function call, or a spread, Claude Code drops `/<name>` from `/` autocomplete.
* **Body**: besides `agent()`, `pipeline()`, and `parallel()`, you can call `phase()` to group the agents that follow under a title in the progress view, call `log()` to show a message above the phases, and read the [`args`](#pass-input-to-a-saved-workflow) global. If the body has a syntax error, Claude Code reports it when you run the workflow.
* **`phases`**: if you list them in `meta`, give each entry exactly the title you pass to `phase()`. A `phase()` title with no entry gets a progress group of its own.
* **Timestamps and randomness**: Claude Code makes `Date.now()`, `Math.random()`, and a no-argument `new Date()` throw inside the script, so that a [relaunched run](#resume-after-a-pause) repeats the same `agent()` calls. Pass a timestamp in through `args` instead.

You can also edit [the script of a single run](#how-a-workflow-runs) rather than the saved copy. [Resume after a pause](#resume-after-a-pause) covers which agents run again when you relaunch an edited script. For the Workflow tool's inputs, see its entry in the [Agent SDK reference](https://code.claude.com/docs/en/agent-sdk/typescript.md#workflow).

## How a workflow runs

The workflow runtime executes the script in an isolated environment, separate from your conversation. Intermediate results stay in script variables instead of landing in Claude's context.

Unless Claude starts a run from a script file's path, Claude Code writes the run's script to a file under your session's directory in `~/.claude/projects/`. Claude receives the script's path when the run starts, so you can ask for it. You can open that file to read the orchestration Claude wrote, diff it against a previous run's script, or edit it and ask Claude to relaunch from the edited version.

Claude can start a workflow only from a script file the session is already allowed to read. To run a script kept outside your working directory, add its directory with [`/add-dir`](https://code.claude.com/docs/en/permissions#working-directories) or a [Read allow rule](https://code.claude.com/docs/en/permissions.md#read-and-edit) first.

The runtime tracks each agent's result as the run progresses, which is what makes a run [resumable](#resume-after-a-pause) within the same session.

### Prompt caching in a fan-out

Agents in the same run can read each other's [prompt cache](https://code.claude.com/docs/en/prompt-caching.md#subagents-and-the-cache). Two agents that run with the same model, effort level, agent type, tools, output schema, and working directory build the same tools-and-system-prompt prefix, so an agent that starts after a matching sibling's response has begun reads that sibling's cache on its first request.

A workflow agent's requests fall outside the main conversation's [cache TTL bucket](https://code.claude.com/docs/en/prompt-caching.md#which-ttl-each-request-gets), so its cache holds for five minutes by default, including on a Claude subscription. To keep it for an hour, set [`subagentPromptCacheTtl`](https://code.claude.com/docs/en/settings-reference#subagentpromptcachettl) to `1h`. The API bills 1-hour cache writes at a higher rate.

When a fan-out starts several matching agents at once, Claude Code holds all but the first until the first agent's response begins, then releases the held agents together so their first requests read the shared prefix instead of each processing it uncached. Claude Code caps the hold at [`CLAUDE_CODE_WORKFLOW_PREFIX_STAGGER_MS`](https://code.claude.com/docs/en/env-vars) milliseconds, `5000` by default. Set it to `0` to disable the hold.

### Behavior and limits

The runtime applies the following constraints:

| Constraint | Why |
| :- | :- |
| No mid-run user input | A run pauses on its own only for agent permission prompts and a [usage-limit wait](#when-a-run-hits-your-usage-limit). For sign-off between stages, run each stage as its own workflow |
| No direct filesystem or shell access from the workflow itself | Agents read, write, and run commands. The script coordinates the agents |
| No module loading: a script that contains `import()` fails before the run starts | The script body is plain JavaScript. Put work that needs a library in an agent's task |
| Up to 16 concurrent agents by default, fewer when Claude Code has fewer CPUs available, including inside a CPU-limited container. To change the limit, set [`CLAUDE_CODE_WORKFLOW_MAX_CONCURRENT_AGENTS`](https://code.claude.com/docs/en/env-vars#variables) to a value from 1 to 256, which requires Claude Code v2.1.269 or later | Bounds local resource use |
| In a fan-out, agents that share the first agent's prompt-cache prefix start up to 5 seconds after it by default | All but the first read the [prefix the first agent cached](#prompt-caching-in-a-fan-out) instead of each processing it uncached |
| Up to 4,096 items in a single `parallel()` or `pipeline()` call: the runtime rejects a longer list with an error | A silent cap would drop part of the workload without telling the script |
| 1,000 agents total per run | Prevents runaway loops |

## Manage runs

Once a run starts, you manage it from the `/workflows` view, or by expanding its progress line in the task panel below the input box.

When you stop a run, it stays in the task panel while any of its agents' processes are still running. If you stop it again, Claude Code re-signals those processes.

### Resume after a pause

Resume a paused run from `/workflows` by selecting it and pressing `p`. For a run you stopped, ask Claude to relaunch the workflow with the same script. If agents from the stopped run haven't exited yet, Claude Code refuses the relaunch until they have, so a second copy of those agents can't run alongside them.

#### Which agents run again

Claude Code replays the run in the order agents start, and each agent either returns its saved result or runs again:

* **Completed**: returns its saved result. The first agent whose prompt differs from the previous run, because you edited the script or an earlier agent returned something different, runs again, and so does every agent after it, even ones that completed.

  Before v2.1.305, completed agents could also run again when you relaunched an unedited script whose `pipeline()` items or `parallel()` tasks ran more than one agent each. To stop those reruns for new runs, update Claude Code.
* **Still running when you stopped**: starts over. Stopping the whole run doesn't count any agent as failed.
* **Failed**: runs again, and so does every agent the script starts after it, even ones that completed. Stopping one agent alone, by selecting it in [`/workflows`](#watch-the-run) and pressing `x`, counts as failing.

That last case means a failure in the middle of a fan-out reruns work that already finished. If a script starts A, B, C, and D in that order and B fails, relaunching returns A from cache and runs B, C, and D again.

If you edit a script that started A, B, C, and D so that it starts A, C, B, and D, the second agent to start is now C, where the previous run started B. Relaunching returns A from cache and runs C, B, and D again.

#### Resume after you leave the session

If you background your session or exit Claude Code while a workflow run is in progress, the run doesn't continue on its own. The run continues only when Claude relaunches it with a `Workflow` call, which [replays the run from its saved results](#which-agents-run-again).

* **You backgrounded the session or chose [`Move to background and exit`](https://code.claude.com/docs/en/agent-view#from-inside-a-session)**: if the run hasn't continued when you check the [background session](https://code.claude.com/docs/en/agent-view.md#what-carries-over-when-you-background), ask Claude there to relaunch the workflow. Depending on your [permission mode](#approve-the-plan-before-it-runs), Claude Code asks you to approve the relaunch first. If the session shows under `Needs input` in agent view, [attach to it](https://code.claude.com/docs/en/agent-view.md#attach-to-a-session) to answer the approval prompt.
* **The relaunch in the background session failed with `nothing to resume`**: ask Claude to start the workflow over as a new run. If Claude started the run from the path of a script file outside `~/.claude/projects/`, such as one in your working directory, Claude can't relaunch it in the background session.
* **You chose `Exit and stop tasks`, or weren't offered `Move to background and exit`**: the run stopped with the session, and Claude Code keeps the run's saved results under that session's directory in `~/.claude/projects/`. Resume the session with `claude --resume` in your shell, then ask Claude to relaunch the workflow. In a fresh session, Claude has no earlier run to relaunch and starts the workflow over.

In a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md), Claude Code also saves the run's results with the session's conversation history, which survives when the session's VM is reclaimed. When you [reopen such a session](https://code.claude.com/docs/en/claude-code-on-the-web.md#environment-expired) and ask Claude to relaunch the workflow, completed agents still return their saved results.

In local and cloud sessions alike, when Claude relaunches an earlier run and Claude Code can't find that run's saved results at all, the relaunch fails with a `nothing to resume` error instead of starting the run over on its own. Ask Claude to start the workflow over as a new run.

### When a run hits your usage limit

When an agent hits your claude.ai [usage limit](https://code.claude.com/docs/en/interactive-mode.md#wait-for-a-usage-limit-to-reset), the run pauses rather than failing that agent: the agents that hit the limit wait for the reset, and no new agents start. Shortly after the limit resets, the waiting agents run again and the run continues on its own. Requires Claude Code v2.1.271 or later; on earlier versions, the affected agents fail.

While the run waits, its progress line in the task panel and the [`/workflows`](#watch-the-run) header show when the limit resets.

The run pauses only when all of these hold; when one doesn't, the affected agent fails instead:

* The session is interactive and signed in with a claude.ai subscription. A run doesn't pause in [non-interactive mode](https://code.claude.com/docs/en/headless.md) with `claude -p` or the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview.md), in a [background session](https://code.claude.com/docs/en/agent-view.md), or in a [Remote Control](https://code.claude.com/docs/en/remote-control.md) or [agent team](https://code.claude.com/docs/en/agent-teams.md) teammate session.
* [`autoContinueAtUsageLimit`](https://code.claude.com/docs/en/settings-reference#autocontinueatusagelimit) is on, the same setting that lets the session itself [wait for a usage limit to reset](https://code.claude.com/docs/en/interactive-mode.md#wait-for-a-usage-limit-to-reset). If you turn it off during a wait, the wait ends and the waiting agents fail.
* The limit resets within 24 hours. A weekly limit can reset further out.
* The run hasn't already waited twice. When it hits the limit a third time, the agent fails.

### When an agent stalls and restarts

An agent whose output stops arriving for long enough starts over from the same prompt. In [`/workflows`](#watch-the-run), its name gains a `(retry 1)` suffix and its detail shows `attempt 2 (stalled)`. The restart is automatic, so you don't need to do anything.

The new attempt starts without the stalled attempt's transcript. Files the stalled attempt already changed stay changed, and the tokens it spent stay in the run's total. The stall window is how long Claude Code waits for output from an agent before it ends the attempt. Time the agent spends waiting on its own tool calls or on a [usage-limit reset](#when-a-run-hits-your-usage-limit) doesn't count toward the stall window.

An agent restarts at most five times, counting any restart you ask for with `r`. If the sixth attempt stalls as well, the `agent()` call fails, and the start of the error says why:

* `agent stalled on all 6 attempts`: every attempt went the whole window without output. If the agent's work keeps it silent that long, lengthen the window
* `agent lost its reply on all 6 attempts`: every attempt's response stream went silent and Claude Code gave up waiting on it. Lengthening the stall window doesn't help, since a [streaming idle watchdog](https://code.claude.com/docs/en/network-config.md#streaming-idle-watchdogs) ended the response first and `CLAUDE_STREAM_IDLE_TIMEOUT_MS` sets that watchdog's timeout
* `agent abandoned after 6 attempts`: the attempts ended in different ways, which the error lists in order

To give an agent more time to produce output before the window ends:

* **One agent**: pass `stallMs` in milliseconds on its `agent()` call, such as `agent(prompt, { stallMs: 1800000 })` for 30 minutes
* **Every agent**: set [`CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS`](https://code.claude.com/docs/en/env-vars#variables), which also applies to subagents outside workflows

Whether the run continues after the failure depends on how your script called the agent:

* **Inside [`parallel()` or `pipeline()`](#what-the-saved-script-looks-like)**: the run carries on with `null` in place of the agent's result
* **Awaited directly**: the run ends with the error

To try again, ask Claude to relaunch the workflow. [Resume after a pause](#resume-after-a-pause) covers what runs again.

### Cost

A workflow spawns many agents, so a single run can use meaningfully more tokens than working through the same task in conversation. Runs count toward your plan's usage and rate limits.

To gauge the spend before committing to a large task, run the workflow on a small slice first: one directory instead of the whole repo, or a narrow question instead of a broad one. The `/workflows` view shows each agent's token usage as the run progresses, and you can stop the run there at any time, usually without losing completed work. [Resume after a pause](#resume-after-a-pause) covers what a stopped run keeps. The runtime's [agent caps](#behavior-and-limits) limit how many agents a single run can spawn, which bounds the cost of a runaway script. To keep runs to fewer agents, choose the `small` [size guideline](#set-a-size-guideline).

Claude Code also flags a run that grows unusually large. When a workflow schedules more than 25 agents, or its projected token total passes 1.5 million, its progress line in the task panel below the input box shows a `Large workflow` warning. The warning points you to [`/workflows`](#watch-the-run), where you can stop the run.

The warning is advisory: it doesn't pause or limit the run. Two settings change when you see it:

* If you choose a [size guideline](#set-a-size-guideline) yourself, its agent count replaces the 25-agent threshold. The built-in default guideline leaves the threshold at 25.
* Sessions with [ultracode](#let-claude-decide-with-ultracode) on don't show the warning, because turning ultracode on already opts you in to large runs.

Claude Code picks each workflow agent's model in the same [order it uses for subagents](https://code.claude.com/docs/en/sub-agents.md#choose-a-model). A model the script names for a stage counts as the per-invocation model in that order. When nothing else assigns one, the agent runs on your session's model.

To control the model cost:

* Check `/model` before a large run if you usually switch to a smaller model for routine work
* Ask Claude to use a smaller model for stages that don't need the strongest one when you describe the task

When your organization's [`availableModels` allowlist](https://code.claude.com/docs/en/model-config#restrict-model-selection) blocks a model the script requests for an agent, that agent runs on a substituted model instead, following the same [substitution rules as subagents](https://code.claude.com/docs/en/sub-agents.md#choose-a-model).

### Set a size guideline

A size guideline tells Claude how many agents to aim for when it writes a dynamic workflow. Claude Code sends the guideline to Claude as advice, not a cap, so a prompt that calls for a different scale still overrides it.

Each value maps to an agent count:

| Value | Agent count Claude aims for |
| :- | :- |
| `unrestricted` | No guideline: Claude sizes the workflow to the task |
| `small` | Fewer than 5 agents |
| `medium` | Fewer than 10 agents |
| `large` | Fewer than 50 agents |

The default is `medium`, or `small` when you're signed in on a Pro plan with Claude Code v2.1.271 or later. Until you choose a value, the `/config` row marks the value as the default, and the workflow's `Running in background` line names the size in force. Requires Claude Code v2.1.219 or later; earlier versions default to `unrestricted`.

To change the guideline, pick a value for the Dynamic workflow size setting in `/config`, or run `/config workflowSizeGuideline=small`. On v2.1.219 and later, you can also set the [`workflowSizeGuideline` key](https://code.claude.com/docs/en/settings-reference#workflowsizeguideline) in any settings file; that value takes precedence over `/config`, and Claude Code hides the `/config` row while a settings file provides one.

Changes take effect on the next prompt. The [runtime agent caps](#behavior-and-limits) still apply regardless of the setting.

### Turn workflows off

Workflows are available in the CLI, the Desktop app, the IDE extensions, [non-interactive mode](https://code.claude.com/docs/en/headless.md) with `claude -p`, and the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview.md). The same disable settings apply on every surface.

To turn workflows off for yourself:

* Toggle Dynamic workflows off in `/config`. Persists across sessions.
* Set `"disableWorkflows": true` in `~/.claude/settings.json`. Persists across sessions.
* Set `CLAUDE_CODE_DISABLE_WORKFLOWS=1`. Read at startup, so it applies wherever you set it.

To turn workflows off for your whole organization, set `"disableWorkflows": true` in [managed settings](https://code.claude.com/docs/en/server-managed-settings.md), or use the toggle on the [Claude Code admin settings](https://claude.ai/admin-settings/claude-code) page.

When workflows are disabled:

* `/workflows`, the workflow commands, and the `/workflow-authoring` skill are unavailable
* The `ultracode` keyword no longer triggers a run, and the **Ultracode** toggle is removed from `/effort`

A run that was already in progress keeps going.

Turning workflows off also makes [ultracode](#let-claude-decide-with-ultracode) unavailable. No managed setting rules out ultracode alone: wherever it's [available](https://code.claude.com/docs/en/model-config.md#when-ultracode-is-available), users can turn it on with `/effort ultracode`. An [effort cap](https://code.claude.com/docs/en/model-config.md#organization-effort-limits) lowers the effort level a session with ultracode on runs at, but doesn't turn ultracode off.

## Related resources

* [Run agents in parallel](https://code.claude.com/docs/en/agents.md): compare subagents, agent view, agent teams, and workflows
* [Create custom subagents](https://code.claude.com/docs/en/sub-agents.md): the worker primitive workflows orchestrate
* [Manage costs](https://code.claude.com/docs/en/costs.md): how multi-agent runs count toward usage limits
