> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage sessions

> Name, resume, branch, and switch between Claude Code conversations. Covers `--continue`, `--resume`, `--from-pr`, the `/resume` picker, session naming, exporting transcripts, and where transcripts are stored.

A [session](https://code.claude.com/docs/en/glossary.md#session) is a saved conversation tied to a project directory. Claude Code stores it locally as you work, so you can resume where you left off, branch to try a different approach, or switch between tasks.

The [desktop app](https://code.claude.com/docs/en/desktop.md#work-in-parallel-with-sessions), [claude.ai/code](https://code.claude.com/docs/en/claude-code-on-the-web.md), and the [VS Code extension](https://code.claude.com/docs/en/vs-code.md#resume-past-conversations) each keep their own session list, and the desktop app can also [resume a CLI session](https://code.claude.com/docs/en/desktop.md#coming-from-the-cli). This page covers the CLI.

## Resume a session

Sessions are saved continuously to [local transcript files](#export-and-locate-session-data) as you work, so you can return to one after exiting or running `/clear`. Use these entry points:

| Command | What it does |
| :- | :- |
| `claude --continue` | Reopens the most recent session in the current directory |
| `claude --resume` | Opens the [session picker](#use-the-session-picker) |
| `claude --resume <name>` | Resumes the named session directly |
| `claude --resume <transcript-path>` | Resumes the session stored in the `.jsonl` [transcript file](#where-transcripts-are-stored) at that absolute path |
| `claude --from-pr <number>` | Opens the session picker filtered to sessions linked to that pull request |
| `/resume` | Switches to a different session from inside an active session |

### Resume a running background session

When the conversation you resume with `claude --resume` or `/resume` belongs to a [background session](https://code.claude.com/docs/en/agent-view.md) that is still running, Claude Code opens the running session itself. With `--bg` on the command line, the resume is a [background dispatch](https://code.claude.com/docs/en/agent-view.md#from-your-shell) instead. Before v2.1.285, Claude Code refused and told you to open the session with `claude attach <id>`, or to stop it with `claude stop <id>` first.

* **From your shell**: `claude --resume <session>` runs [`claude attach`](https://code.claude.com/docs/en/agent-view#attach-to-a-session) on that session in the same terminal instead of loading the transcript itself. A prompt you pass on the command line, as in `claude --resume <session> "check the tests too"`, goes to the session as its next turn first, and Claude Code prints `Sent your prompt to the background session (<id>); opening it…` before attaching. `claude -p --resume <session> "prompt"` typed at a terminal does the same, so `-p` doesn't keep that run non-interactive.

  Claude Code doesn't open the session when the command line has any of these:

  * Piped or redirected input or output
  * Flags that configure the session, such as `--permission-mode`, `--model`, or `--settings`
  * Flags that read the output, such as `--output-format json` or `--json-schema`
  * Flags that limit or rewind the run, such as `--max-turns` or `--max-budget-usd`

  With any of these, or when [agent view is turned off](https://code.claude.com/docs/en/agent-view.md#turn-off-agent-view), Claude Code sends nothing and exits with status 1, printing that the session is running in the background along with the `claude attach <id>` command that opens it, or telling you to find it in `claude agents` when it can't determine the ID. Add `--fork-session` to resume a copy of the conversation instead. To continue the conversation itself in a session of your own, with your flags applied, run `claude stop <id>` and then repeat the command.

  A prompt that starts with `/` or `!` isn't sent, and neither is any prompt while the session waits on your answer to a question. In both cases Claude Code doesn't open the session, and the message includes `Your prompt was not sent to it` with the reason.
* **From inside a session**: `/resume` moves your current conversation to the background and attaches this terminal to the running session, printing `Opening "<title>", running in the background (<id>)`. Press `←` on an empty prompt to return to agent view, which also lists the conversation you left. When the current conversation can't move to the background, for example because you're already attached to a background session or session persistence is off, `/resume` prints the `claude attach` command to run instead.

### What a resumed session restores

When Claude Code loads a conversation from its transcript, the resumed session restores the conversation along with the state saved in it:

* Conversation history: the messages, tool calls, and results. If the session was [compacted](https://code.claude.com/docs/en/context-window.md#what-survives-compaction), the conversation opens at a `Conversation compacted` row. Claude continues with the last compaction's summary, the messages that compaction left unsummarized, and every message since. The messages that the last compaction summarized aren't loaded again.
* Interrupted tool calls: a tool that was still running when the previous process ended, for example in a crash, doesn't get rerun when you resume.
* Model: the session continues on the model it was using, except in the cases in [Setting your model](https://code.claude.com/docs/en/model-config.md#setting-your-model).
* Agent: a session started with [`--agent`](https://code.claude.com/docs/en/sub-agents#invoke-subagents-explicitly) or the `agent` setting continues as that agent, keeping its tool restrictions and model. Pass `--agent` when resuming to pick a different one; for the system prompt in either case, see [System prompt flags in resumed conversations](https://code.claude.com/docs/en/cli-reference.md#system-prompt-flags-in-resumed-conversations). Claude Code looks for the agent in two places: the session's original directory, provided you have [trusted that workspace](https://code.claude.com/docs/en/permissions.md#project-allow-rules-and-workspace-trust), and then the directory you resume from, so a project-scoped agent still loads when you resume from another directory. If Claude Code doesn't find the agent in either place, the session resumes with the default tools and shows a [warning naming the agent](https://code.claude.com/docs/en/errors.md#session-agent-no-longer-available).
* Permission mode: if you resume from a terminal with `claude --continue`, `claude --resume <session-id>`, or `claude --resume <name>` when the name matches one session, without `-p`, Claude Code restores the permission mode the session was in, except in the cases in [permission mode on resume](#permission-mode-on-resume), which also covers the session picker, `/resume`, and resuming with `claude -p`. Pass `--permission-mode` or `--dangerously-skip-permissions` to override the restored mode.
* Active goal: a [goal](https://code.claude.com/docs/en/goal.md#resume-with-an-active-goal) that was still active when the session ended carries over; its turn count, timer, and token-spend baseline reset.
* Session-scoped scheduled tasks: [tasks that haven't expired](https://code.claude.com/docs/en/scheduled-tasks.md#limitations) are restored. Background Bash and monitor tasks aren't.
* Background work: a [background subagent](https://code.claude.com/docs/en/sub-agents.md#run-subagents-in-foreground-or-background), background Bash command, or [workflow](https://code.claude.com/docs/en/workflows.md) that ended with the previous process shows up in the resumed transcript as a note that it didn't finish. Claude Code doesn't start a turn from those notes; Claude reads them with your next prompt.

Not every configuration flag from the original launch is restored. If the session depended on `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model`, or directories added with `--add-dir`, pass them again when you resume; directories added mid-session with `/add-dir` aren't restored either, though the session picker still uses them to locate the session. The standard settings files, such as `settings.json` and `settings.local.json`, are re-read at launch, so configuration that lives in them doesn't need to be passed again. For `--system-prompt` and `--append-system-prompt`, see [System prompt flags in resumed conversations](https://code.claude.com/docs/en/cli-reference.md#system-prompt-flags-in-resumed-conversations).

#### Permission mode on resume

Which permission mode Claude Code starts a resumed session in depends on how you resume. The cases below apply when Claude Code loads the conversation from its transcript; when you [open a background session that is still running](#resume-a-running-background-session) instead, that session keeps the permission mode it is in.

* Terminal: `claude --continue`, `claude --resume <session-id>`, or `claude --resume <name>` when the name matches one session, without `-p`. Claude Code restores the permission mode the session was in, except in the cases in the table. Pass `--permission-mode` or `--dangerously-skip-permissions` to override the restored mode.
* Non-interactive: `claude -p --resume` or `claude -p --continue`. Claude Code starts the run in the permission mode a new `claude -p` run would start in, except that a session that ended in plan mode resumes in plan mode under the [conditions below](#resume-in-plan-mode-with-p).
* VS Code: the extension's conversation panel. The table covers only a conversation that ended in plan mode; for the rest, see [resume past conversations](https://code.claude.com/docs/en/vs-code.md#resume-past-conversations).
* Session picker at launch: a session you select from the [session picker](#use-the-session-picker), whether you opened it with `claude --resume` alone, `claude --from-pr`, or a name that matches more than one session. Claude Code starts the session in the permission mode it would start a new session in from the same command line, except that a session that ended in plan mode resumes in plan mode. If you pass `--permission-mode`, `--dangerously-skip-permissions`, or `--fork-session`, Claude Code doesn't restore plan mode. No other stored permission mode is restored.
* `/resume` inside a session, with or without an argument: the conversation you switch to continues in the permission mode your current session is in, except that a conversation that ended in plan mode resumes in plan mode, even if you launched Claude Code with `--permission-mode` or `--dangerously-skip-permissions`. If that conversation was already open earlier in this run of Claude Code, such as the conversation you started in or one you left with `/clear` or `/resume`, it continues in your current permission mode instead.

If a [deny rule](https://code.claude.com/docs/en/permissions.md#manage-permissions) removes the [`ExitPlanMode`](https://code.claude.com/docs/en/tools-reference) tool, Claude can't present a plan for approval, so Claude Code doesn't restore plan mode. The session starts in the permission mode a new session would start in from the same command line. With `/resume`, the conversation continues in your current permission mode.

Restoring plan mode on the non-interactive and VS Code paths requires Claude Code v2.1.246 or later. Each row names the permission mode the session ended in, which of the terminal, non-interactive, and VS Code paths you resume it by, and the permission mode Claude Code starts the resumed session in.

| Session ended in | How you resume | Permission mode after you resume |
| :- | :- | :- |
| `bypassPermissions` | Terminal | The permission mode a new session would start in. To [bypass permissions](https://code.claude.com/docs/en/permission-modes.md#skip-all-checks-with-bypasspermissions-mode) again, enable it at launch with one of its launch flags or `permissions.defaultMode: "bypassPermissions"` in [user, `--settings`, or managed settings](https://code.claude.com/docs/en/settings-reference#permissions-defaultmode) |
| `plan` | Terminal | Plan mode. With `--fork-session`, the permission mode a new session would start in |
| `plan` | Terminal, when a deny rule removes `ExitPlanMode` | The permission mode a new session would start in |
| `auto` | Terminal | `auto`, only when your account still meets the [auto mode requirements](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) |
| Manual | Terminal | Manual when a new session would start in auto mode from the [built-in default](https://code.claude.com/docs/en/permission-modes.md#which-mode-a-session-starts-in). When a `defaultMode` from a settings file [takes effect](https://code.claude.com/docs/en/permission-modes.md#which-mode-a-session-starts-in), Claude Code starts the resumed session in that mode instead |
| `plan` | Non-interactive, under the [conditions below](#resume-in-plan-mode-with-p) | Plan mode |
| Any mode | Non-interactive, in any other case | The permission mode a new `claude -p` run would start in |
| `plan` | VS Code | Plan mode, with [the exceptions on the VS Code page](https://code.claude.com/docs/en/vs-code.md#resume-past-conversations) |

##### Resume in plan mode with `-p`

A `claude -p --resume` or `claude -p --continue` run resumes in plan mode only when all of these conditions hold:

* You pass [`--permission-prompt-tool`](https://code.claude.com/docs/en/cli-reference#cli-flags) and don't pass [`--permission-prompts none`](https://code.claude.com/docs/en/headless#turn-off-permission-prompts-in-unattended-runs), so that Claude Code can present the plan for approval
* You don't pass `--permission-mode` or `--dangerously-skip-permissions`
* You don't pass `--fork-session`
* The run isn't started through [channels](https://code.claude.com/docs/en/channels.md)
* No [deny rule](https://code.claude.com/docs/en/permissions.md#manage-permissions) removes the `ExitPlanMode` tool

### The "Resume this conversation?" dialog

If you see the "Resume this conversation?" dialog when resuming a session, its estimate is the share of your 5-hour usage limit that the saved conversation alone would use. The estimate doesn't count what you've already used.

On Pro, Max, and Ultra plans, the dialog can appear when you resume a long conversation [after a long break](https://code.claude.com/docs/en/prompt-caching.md#resuming-a-session) or on a different model. The estimated use comes when you send your first message after **Resume**, not when you select it. Choose by whether your next task still needs the saved conversation:

* **Resume**: keep working in the saved conversation.
* **Start a new conversation**: switch to work that doesn't need the saved conversation. To reopen it later, run [`/resume`](#use-the-session-picker) at the prompt. The estimate doesn't apply to your first message in the new conversation. If the option says that Claude can look up this conversation, you can still refer to earlier work in the new conversation.

### Where the session picker looks

Claude Code stores sessions per project directory. By default the session picker shows:

* Sessions from the current worktree, including [background sessions](https://code.claude.com/docs/en/agent-view.md), which are marked `bg` in the list
* Sessions started elsewhere that added the current directory with `/add-dir`

Use `Ctrl+W` to widen to all worktrees of the repository or `Ctrl+A` to widen to every project on this machine.

#### `/loop`, `-p`, Agent SDK, and background sessions

Sessions whose first prompt was a [`/loop`](https://code.claude.com/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) command don't appear in the picker, and `claude --continue` skips them too. Running `/loop` later in a conversation doesn't hide the session.

Claude Code leaves sessions created with [`claude -p`](https://code.claude.com/docs/en/headless) or the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview.md) out of the session picker and out of `claude --continue`. You can still resume one by passing its session ID to `claude --resume <session-id>`. When you run [`claude -p --continue`](https://code.claude.com/docs/en/headless#continue-conversations), Claude Code includes `-p`, SDK, and `/loop` sessions.

`claude --continue` opens a [background session](https://code.claude.com/docs/en/agent-view.md) that has finished, but not one that is still running; opening finished background sessions requires Claude Code v2.1.257 or later. If your most recent conversation is one you [moved to the background](https://code.claude.com/docs/en/agent-view.md#send-the-session-to-the-background) and it is still running there, Claude Code exits with `Your most recent conversation is running in the background` and that session's ID. Attach to the session from [`claude agents`](https://code.claude.com/docs/en/agent-view#attach-to-a-session), or run `claude --resume` to pick another one.

#### Sessions in other worktrees and projects

When you select a session from another worktree of the same repository, Claude Code resumes it in place; when the session's own worktree no longer exists, Claude Code [resumes it in your current directory](https://code.claude.com/docs/en/worktrees.md#resume-a-worktree-session). When you select a session from an unrelated project, Claude Code copies a `cd` and resume command to your clipboard instead. If that project's directory no longer exists, Claude Code resumes the session in your current directory rather than copying a `cd` command that would fail.

Moving a session with [`/cd`](https://code.claude.com/docs/en/commands) relocates it to the new directory's project storage, so it appears in that directory's picker afterward.

#### Resume by session ID or name

You can run `claude --resume <session-id>` from any directory, so you can resume a session that started elsewhere or moved with [`/cd`](https://code.claude.com/docs/en/commands). Claude Code looks for the ID in this order:

1. The current project directory and its git worktrees
2. Every other project on this machine

The cross-project search resolves the ID only when exactly one other project holds a transcript with messages for it, so a hand-copied duplicate makes Claude Code report not-found rather than resume an arbitrary copy. If no stored session matches the ID, Claude Code reports `No conversation found with session ID: <session-id>`.

Resuming by name resolves across the current repository and its worktrees. Both forms look for an exact match and resume it directly even if it lives in a different worktree:

| Command | Exact match | Ambiguous name |
| :- | :- | :- |
| `claude --resume <name>` | Resumes directly | Opens the session picker with the name pre-filled as a search term |
| `/resume <name>` | Resumes directly | Reports an error; run `/resume` with no argument to open the session picker |

## Name your sessions

Give sessions descriptive names so they're findable in the session picker and resumable by name. This matters most when you're working on several tasks in parallel.

| When | How to set the name |
| :- | :- |
| At startup | `claude -n auth-refactor` |
| During a session | `/rename auth-refactor`. The name also appears on the prompt bar |
| From the session picker | Highlight a session and press `Ctrl+R` |
| On plan accept | Accepting a plan in [plan mode](https://code.claude.com/docs/en/permission-modes.md#analyze-before-you-edit-with-plan-mode) gives the session a generated title based on the plan unless you've already named it |
| From claude.ai or the Claude app | Rename a [Remote Control session](https://code.claude.com/docs/en/remote-control.md#connect-from-another-device); Claude Code applies the same name in the CLI. Requires Claude Code v2.1.221 or later |
| From the desktop app | Rename a session in the [desktop app](https://code.claude.com/docs/en/desktop.md#organize-and-find-sessions) |

Once you name a session through a CLI route or from claude.ai, return to it with `claude --resume <name>` or `/resume <name>`; a desktop-app session resumes in the [desktop app](https://code.claude.com/docs/en/desktop.md#work-in-parallel-with-sessions). See [Resume a session](#resume-a-session) for how name resolution behaves across worktrees.

Sessions you don't name still get two labels that Claude Code assigns. Only the generated title works as a resume handle:

* Default display name: interactive sessions you never name still get a default display name when they start. The default combines the working directory's name with a two-character suffix, for example `my-app-3f`, and identifies the session in listings of running sessions, such as [agent view](https://code.claude.com/docs/en/agent-view.md) and `claude agents --json` output. The default isn't a resume handle. If you pass it to `claude --resume` or `/resume`, Claude Code doesn't find the session.
* Generated title: if you don't name a session, Claude Code generates a session title for it. The title is a short summary of your first prompt, written by a background request to the small/fast model, normally a Haiku-class model. A `claude -p` run you start directly from a shell or script doesn't get one.

  Accepting a plan replaces the generated title with a title based on the plan. You can pass either title to `claude --resume` or `/resume`, and Claude Code resolves it the same way as a name you set.

## Use the session picker

Run `/resume` inside a session, or `claude --resume` with no arguments, to open the interactive session picker. Use these keyboard shortcuts to navigate, search, and widen the list:

| Shortcut | Action |
| :- | :- |
| `↑` / `↓` or `k` / `j` | Navigate between sessions |
| `→` / `←` | Expand or collapse grouped sessions |
| `Enter` | Resume the highlighted session |
| `1` to `9` | Resume the session at that position in the list |
| `Space` | Preview the session content. `Ctrl+V` also works on terminals that don't capture it as paste |
| `Ctrl+R` | Rename the highlighted session |
| `/` or any printable character other than `Space`, `j`, `k`, or a digit | Enter search mode and filter sessions. Paste a GitHub, GitHub Enterprise, GitLab, or Bitbucket pull or merge request URL to find the session that created it |
| `Ctrl+A` | Show sessions from all projects on this machine. Press again to return to the current repository |
| `Ctrl+W` | Show sessions from all worktrees of the current repository. Press again to return to the current worktree. Only shown in multi-worktree repositories |
| `Ctrl+B` | Filter to sessions from the current git branch. Press again to show all branches |
| `Esc` | Exit the session picker or search mode |

Each row shows the session name if you set one, otherwise the AI-generated session title, conversation summary, or first prompt, along with time since last activity, git branch, and file size.

Sessions created with `/branch` or `--fork-session` get their own session IDs and appear as separate rows. When the picker finds more than one entry for the same session, it groups them under a single row. Press `→` to expand a group.

If Claude Code can't load the session you select from the `claude --resume` picker, it prints [`Failed to resume the conversation`](https://code.claude.com/docs/en/errors#failed-to-resume-the-conversation) with a command to retry, then exits with code 1. From the `/resume` picker inside a session, Claude Code reports the failure and your current conversation keeps running.

## Branch a session

Branching creates a copy of the conversation so far and switches you into it, leaving the original intact. Use it to try a different approach without losing the path you were on.

From inside a session, run `/branch` with an optional name:

```text theme={null}
/branch try-streaming-approach
```

If you omit the name, Claude Code names the new branch after the first prompt in the conversation.

From the command line, combine `--continue` or `--resume` with `--fork-session`:

```bash theme={null}
claude --continue --fork-session
```

The `/branch` confirmation prints two session IDs: the new branch you are now in and the original. The original is unchanged on disk and remains in the session picker; return to it with `/resume <original-name>` or by passing its ID to `/resume`.

`/branch` copies the transcript and switches the running Claude Code process to write to it. That distinction determines what the branch inherits:

| State | After `/branch` |
| :- | :- |
| Conversation history | Copied into the branch up to the point you ran `/branch` |
| "Allow for this session" permission grants | Carried over; the branch runs in the same process, so your existing grants still apply. If you fork into a separate process with `--fork-session`, the new process starts without them and you re-approve there |
| In-flight [background subagents](https://code.claude.com/docs/en/sub-agents.md#run-subagents-in-foreground-or-background) and [background Bash commands](https://code.claude.com/docs/en/interactive-mode.md#background-bash-commands) | Keep running. Their output appears in the new branch you switched into, not in the original session |
| [Remote Control](https://code.claude.com/docs/en/remote-control.md) connection | Stays connected. A phone or browser connected to the session follows you into the branch and keeps receiving new messages there |

If you resume the same session in two terminals without forking, messages from both interleave into one transcript. For checkpoint-based rewind within a single session, see [Checkpointing](https://code.claude.com/docs/en/checkpointing.md).

## Manage context within a session

These commands control what's in the context window without leaving the session:

* **`/clear`**: start fresh with an empty context. Claude Code saves the previous session; resume it with `/resume`, or, in the same Claude Code process, from [the rewind menu's previous-session entry](https://code.claude.com/docs/en/checkpointing.md#rewind-past-a-cleared-conversation). With no argument, the new session keeps a name you set with `--name` or `/rename`, but not an AI-generated session title. To name the session you're leaving instead, pass the name, as in `/clear release-prep`; the new session then starts unnamed
* **`/compact [instructions]`**: replace history with a summary, optionally focused on what you specify
* **`/context`**: show what is currently consuming context

For how compaction interacts with CLAUDE.md, skills, and rules, see the [context window guide](https://code.claude.com/docs/en/context-window.md). For strategies on when to clear versus compact, see [Best practices](https://code.claude.com/docs/en/best-practices.md#keep-cost-and-context-down).

## Export and locate session data

Run `/export` to open a menu that lets you copy the current conversation to your clipboard or save it as a plain-text file, with messages and tool outputs rendered as readable text. Pass a filename to skip the menu and write directly to that file.

### Access conversations from scripts

`/export` produces a rendered transcript for a person to read. The interfaces below produce structured data for a script to parse: a JSON result from a run, the path to a session's transcript file, or a live stream of events. Pick by what triggers the script:

* **Run Claude once and capture the result**: invoke `claude -p` with [`--output-format json` or `stream-json`](https://code.claude.com/docs/en/headless#get-structured-output) to capture the result, session ID, usage, and cost of a non-interactive run as structured JSON.
* **Ask an existing session a question**: pass a session ID to [`claude -p --resume`](https://code.claude.com/docs/en/headless#continue-conversations) to send a follow-up prompt, such as a summary request, and capture the structured response.
* **React to session events**: read the `transcript_path` field that [hooks](https://code.claude.com/docs/en/hooks.md#common-input-fields) and [status line commands](https://code.claude.com/docs/en/statusline.md#available-data) receive as input. A `SessionEnd` hook can archive the transcript when a session ends.
* **Embed Claude in a TypeScript or Python app**: use the [Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview.md) to receive each message programmatically.

The example below uses the second interface. It sends a follow-up prompt to an existing session and reads the answer with `jq`:

```bash theme={null}
claude -p --resume <session-id> --output-format json "summarize what we changed" | jq -r '.result'
```

### Where transcripts are stored

By default, Claude Code stores transcripts as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is your working directory path with non-alphanumeric characters replaced by `-`. For a working directory whose converted name exceeds 200 characters, Claude Code truncates the name to 200 characters and appends a hash of the full path, so the directory name stays within filesystem limits.

Each line is a JSON object: a message, a tool use or result, a record of a request Claude Code sent the model, or a metadata entry. The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release. To build on session data, use `/export` or the [script interfaces](#access-conversations-from-scripts) instead.

The location, retention, and write behavior are configurable:

| To | Set | Where |
| - | - | - |
| Move storage off `~/.claude` | [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/en/env-vars) | Environment variable |
| [Name the `<project>` directory yourself](#name-the-project-directory-yourself) | [`CLAUDE_CODE_PROJECT_DIR_NAME`](https://code.claude.com/docs/en/env-vars) | Environment variable |
| Change the 30-day retention | [`cleanupPeriodDays`](https://code.claude.com/docs/en/settings-reference#cleanupperioddays) | `settings.json` |
| Set an age limit for [Claude Desktop and Cowork transcripts](https://code.claude.com/docs/en/claude-directory.md#cleaned-up-automatically) | [`desktopSessionCleanupPeriodDays`](https://code.claude.com/docs/en/settings-reference#desktopsessioncleanupperioddays) | User settings, managed settings, or `--settings` |
| Limit how large a `-p` or Agent SDK session's transcript file grows | [`CLAUDE_CODE_TRANSCRIPT_LOCAL_GC`](https://code.claude.com/docs/en/env-vars) | Environment variable |
| Suppress transcript writes in all modes | [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](https://code.claude.com/docs/en/env-vars) | Environment variable |
| Suppress writes for one non-interactive run | [`--no-session-persistence`](https://code.claude.com/docs/en/cli-reference) | CLI flag with `claude -p` |

### Delete session data

Transcripts age out under the [retention sweep rules](https://code.claude.com/docs/en/claude-directory.md#cleaned-up-automatically). To delete a project's transcripts and related state sooner, run [`claude purge`](https://code.claude.com/docs/en/claude-directory#clear-local-data). If you delete a [background session](https://code.claude.com/docs/en/agent-view.md) with [`claude rm <id>`](https://code.claude.com/docs/en/agent-view#what-deleting-a-session-removes), its transcript stays on disk and remains available through `claude --resume`.

### Name the project directory yourself

By default, Claude Code derives the `<project>` name from the whole working directory path. To choose the name yourself, set `CLAUDE_CODE_PROJECT_DIR_NAME` alongside `CLAUDE_CONFIG_DIR`. Claude Code then stores that session's transcripts and [auto memory](https://code.claude.com/docs/en/memory.md#auto-memory) under your name. This suits a host that embeds Claude Code and gives each session its own config directory. Requires Claude Code v2.1.234 or later.

For example, this launch keeps tenant A's data under `/srv/tenant-a` and names its project directory `work`:

```bash theme={null}
CLAUDE_CONFIG_DIR=/srv/tenant-a CLAUDE_CODE_PROJECT_DIR_NAME=work claude
```

Claude Code writes the session's transcripts to `/srv/tenant-a/projects/work/` and its auto memory to `/srv/tenant-a/projects/work/memory/`, whatever the working directory is.

Three rules apply when you set it:

* **Set `CLAUDE_CONFIG_DIR` too**: the name doesn't vary with the working directory, so under the default `~/.claude` it would merge every project's transcripts and auto memory into one directory. Claude Code ignores `CLAUDE_CODE_PROJECT_DIR_NAME` when `CLAUDE_CONFIG_DIR` is unset.
* **Use 1-64 letters, digits, hyphens, or underscores**: don't use a Windows device name such as `con`. Claude Code ignores any other value and uses the derived name.
* **Set it in the shell environment that starts `claude`**: Claude Code reads it once at startup from that environment, so an `env` block in a settings file can't set it.

Once you've named a config directory's project directory, keep launching with that name. If you start Claude Code with the same `CLAUDE_CONFIG_DIR` but without `CLAUDE_CODE_PROJECT_DIR_NAME`, it reads and writes the derived directory again. The sessions stored under your name stay on disk: press `Ctrl+A` in the [session picker](#use-the-session-picker) to list sessions from every project directory under that config directory, the pinned one included, and whichever way you launch, [`claude --resume <session-id>`](#resume-a-session) finds a session stored under either name.

## See also

These pages cover related session and parallelism mechanics:

* [Worktrees](https://code.claude.com/docs/en/worktrees.md): run isolated parallel sessions on separate branches
* [Checkpointing](https://code.claude.com/docs/en/checkpointing.md): rewind code and conversation to an earlier point
* [Context window](https://code.claude.com/docs/en/context-window.md): what fills context and what survives compaction
* [Non-interactive mode](https://code.claude.com/docs/en/headless.md): session behavior under `claude -p`
