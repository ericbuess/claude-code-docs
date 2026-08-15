> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Keep Claude working toward a goal

> Set a completion condition with /goal and Claude keeps working across turns until the condition is met or judged impossible.

The `/goal` command sets a completion condition and Claude keeps working toward it without you prompting each step. After each turn, a small fast model checks whether the condition holds. If the model judges it not yet met, Claude starts another turn instead of returning control to you. The goal clears automatically once the condition is met, or if the model judges the condition impossible to satisfy.

Use a goal for substantial work with a verifiable end state:

* Migrating a module to a new API until every call site compiles and tests pass
* Implementing a design doc until all acceptance criteria hold
* Splitting a large file into focused modules until each is under a size budget
* Working through a labeled issue backlog until the queue is empty

## Compare ways to keep a session running

Three approaches keep the current session running between prompts. Pick based on what should start the next turn:

| Approach                                                            | Next turn starts when      | Stops when                                                    |
| :------------------------------------------------------------------ | :------------------------- | :------------------------------------------------------------ |
| `/goal`                                                             | The previous turn finishes | A model confirms the condition is met or judges it impossible |
| [`/loop`](/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) | A time interval elapses    | You stop it, or Claude decides the work is done               |
| [Stop hook](/docs/en/hooks-guide#prompt-based-hooks)                     | The previous turn finishes | Your own script or prompt decides                             |

`/goal` and a Stop hook both fire after every turn. `/goal` is a session-scoped shortcut: you type a condition and it's active for the current session only. A Stop hook lives in your settings file, applies to every session in its scope, and can run a script for deterministic checks or a prompt for model-evaluated ones.

[Auto mode](/docs/en/auto-mode-config) on its own approves tool calls within a single turn but doesn't start a new one. Claude stops when it judges the work done. `/goal` adds a separate evaluator that checks your condition after every turn, so completion is decided by a fresh model rather than the one doing the work. The two are complementary: auto mode removes per-tool prompts, and `/goal` removes per-turn prompts.

<Tip>
  The approaches above keep the current session running. You can also schedule work that runs independent of any open session, such as nightly tests or morning triage. See [scheduling options](/docs/en/scheduled-tasks#compare-scheduling-options) for cloud routines and desktop scheduled tasks.
</Tip>

## Use `/goal`

One goal can be active per session. The same command sets, checks, and clears it depending on the argument.

### Set a goal

Run `/goal` followed by the condition you want satisfied. If a goal is already active, the new one replaces it.

```text theme={null}
/goal all tests in test/auth pass and the lint step is clean
```

Setting a goal starts a turn immediately, with the condition itself as the directive. You don't need to send a separate prompt. While the goal is active, a `◎ /goal active` indicator shows how long the goal has been running.

A goal doesn't change your permission mode. To let goal turns run unattended, run `/goal` in [auto mode](/docs/en/auto-mode-config). In [Manual mode](/docs/en/permission-modes), Claude still asks before tool calls that your settings don't already allow, such as the test command above.

While the goal is active, the transcript shows each verdict the evaluator returns, and you can press Ctrl+O to see the reason behind it. The status view also shows the most recent reason, so you can see what Claude is working toward next.

### Write an effective condition

The [evaluator](#how-evaluation-works) judges your condition against what Claude has surfaced in the conversation. It doesn't run commands or read files independently, so write the condition as something Claude's own output can demonstrate. "All tests in `test/auth` pass" works because Claude runs the tests and the result lands in the transcript for the evaluator to read.

A condition that holds up across many turns usually has:

* **One measurable end state**: a test result, a build exit code, a file count, an empty queue
* **A stated check**: how Claude should prove it, such as "`npm test` exits 0" or "`git status` is clean"
* **Constraints that matter**: anything that must not change on the way there, such as "no other test file is modified"

The condition can be up to 4,000 characters.

To bound how long a goal runs, include a turn or time clause in the condition, such as `or stop after 20 turns`. Claude reports progress against that clause each turn and the evaluator judges it from the conversation.

### Check status

Run `/goal` with no arguments to see the current state.

```text theme={null}
/goal
```

If a goal is active, the status shows:

* The condition
* How long it has been running
* How many turns have been evaluated
* The current token spend
* The evaluator's most recent reason

The turn count and the most recent reason appear after the first evaluation has run.

If no goal is active but one was achieved earlier in the session, the status shows the achieved condition along with its duration, turn count, and token spend.

### Clear a goal

Run `/goal clear` to remove an active goal before it resolves.

```text theme={null}
/goal clear
```

Claude prints `Goal cleared:` followed by the condition to confirm, or `No goal set` if nothing was active.

`stop`, `off`, `reset`, `none`, and `cancel` are accepted as aliases for `clear`. Running `/clear` to start a new conversation also removes any active goal.

### Resume with an active goal

A goal that was still active when a session ended is restored when you resume that session with `--resume` or `--continue`. The condition carries over, but the turn count, timer, and token-spend baseline all reset on resume. A goal that was already achieved or cleared is not restored.

### Run non-interactively

`/goal` works in [non-interactive mode](/docs/en/headless), in the [desktop app](/docs/en/desktop), and through [Remote Control](/docs/en/remote-control). Setting a goal with `-p` runs the loop to completion in a single invocation:

```bash theme={null}
claude -p "/goal CHANGELOG.md has an entry for every PR merged this week"
```

With the default text output, nothing prints until the run ends, so a goal that runs many turns can look stuck. Add `--output-format stream-json --verbose` to emit each message as the loop runs.

Interrupt the process with Ctrl+C to stop a non-interactive goal before it resolves.

## How evaluation works

`/goal` is a wrapper around a session-scoped [prompt-based Stop hook](/docs/en/hooks#prompt-based-hooks). Each time Claude finishes a turn, Claude Code sends the condition and the conversation so far to your configured [small fast model](/docs/en/model-config), which defaults to Haiku on the Claude API; on a third-party provider, check your [provider page](/docs/en/third-party-integrations) for the platform's default. The model returns one of three verdicts, each with a short reason:

* **Not yet met**: Claude keeps working and takes the reason as guidance for the next turn.
* **Met**: Claude Code clears the goal and records an achieved entry in the transcript.
* **Impossible**: the evaluator judged that the condition can never be satisfied. Claude Code clears the goal and records a failed entry in the transcript along with the reason. You don't need to clear it yourself.

If Claude keeps answering the evaluator without making progress (no tool use for several turns in a row), Claude Code stops the loop, prints a warning, and returns control to you with the goal still set. Evaluation resumes after your next prompt. The [hooks guide](/docs/en/hooks-guide#stop-hook-hits-the-block-cap) explains the underlying mechanism.

If a subagent or a background shell command is still running when a turn ends, Claude Code skips the evaluation for that turn and evaluates when the next turn ends.

To evaluate on a different model, set [`ANTHROPIC_DEFAULT_HAIKU_MODEL`](/docs/en/model-config#environment-variables).

<Warning>
  Claude Code reads `ANTHROPIC_DEFAULT_HAIKU_MODEL` everywhere it uses the small fast model, not only for `/goal` evaluation. When you set it, Claude Code also resolves the [`haiku` alias](/docs/en/model-config#model-aliases) to that model and runs [background functionality](/docs/en/costs#background-token-usage), such as conversation summarization, on it.
</Warning>

The evaluator runs on whichever provider your session is configured for. It does not call tools, so it can only judge what Claude has already surfaced in the conversation.

<Note>
  Evaluation tokens are billed on the small fast model configured for your provider and are typically negligible compared to main-turn spend.
</Note>

## Requirements

Claude Code makes `/goal` available under the same [workspace trust rule as hooks in settings files](/docs/en/permissions#what-runs-before-you-trust-a-folder), because the evaluator is part of the hooks system. `/goal` is also unavailable when [`disableAllHooks`](/docs/en/hooks#disable-or-remove-hooks) is `true` after settings precedence applies, or when [`allowManagedHooksOnly`](/docs/en/settings#hook-configuration) is set in managed settings. In each case, the command tells you why instead of silently doing nothing.

## See also

* [Run a prompt repeatedly with `/loop`](/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop): re-run on a time interval instead of toward a condition
* [Prompt-based hooks](/docs/en/hooks-guide#prompt-based-hooks): write your own Stop hook when you need custom evaluation logic
* [Auto mode](/docs/en/auto-mode-config): approve tool calls automatically so each goal turn runs unattended
* [Scheduling comparison](/docs/en/scheduled-tasks#compare-scheduling-options): run work on a schedule independent of any open session
