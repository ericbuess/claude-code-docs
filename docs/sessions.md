> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage sessions

> Name, resume, branch, and switch between Claude Code conversations. Covers `--continue`, `--resume`, `--from-pr`, the `/resume` picker, session naming, exporting transcripts, and where transcripts are stored.

A session is a saved conversation tied to a project directory. Claude Code stores it locally as you work, so you can resume where you left off, branch to try a different approach, or switch between tasks.

The [desktop app](/docs/en/desktop#work-in-parallel-with-sessions), [Claude Code on the web](/docs/en/claude-code-on-the-web), and the [VS Code extension](/docs/en/vs-code#resume-past-conversations) each maintain their own session history. This page covers the CLI.

## Resume a session

Sessions are saved continuously to [local transcript files](#export-and-locate-session-data) as you work, so you can return to one after exiting or running `/clear`. Use these entry points:

| Command                     | What it does                                                              |
| :-------------------------- | :------------------------------------------------------------------------ |
| `claude --continue`         | Resumes the most recent session in the current directory                  |
| `claude --resume`           | Opens the [session picker](#use-the-session-picker)                       |
| `claude --resume <name>`    | Resumes the named session directly                                        |
| `claude --from-pr <number>` | Opens the session picker filtered to sessions linked to that pull request |
| `/resume`                   | Switches to a different conversation from inside an active session        |

Sessions created with [`claude -p`](/docs/en/headless) or the [Agent SDK](/docs/en/agent-sdk/overview) do not appear in the session picker, but you can still resume one by passing its session ID to `claude --resume <session-id>`. Run this from the directory the session was started in: session ID lookup is scoped to the current project directory and its git worktrees, so a session created elsewhere reports `No conversation found with session ID: <session-id>`.

### What a resumed session restores

A resumed session restores the conversation along with the state saved in it:

* Conversation history: the full history, including tool calls and results.
* Model: the session continues on the model it was using. The model isn't restored when it has been retired or isn't allowed by `availableModels`, when a `--model` flag or `ANTHROPIC_MODEL`-family environment variable picks one at launch, or on providers that use provider-specific deployment IDs, such as [Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry](/docs/en/third-party-integrations); see [model configuration](/docs/en/model-config#setting-your-model) for the resolution order.
* Agent: a session started with [`--agent`](/docs/en/sub-agents#invoke-subagents-explicitly) or the `agent` setting continues as that agent, keeping its system prompt, tool restrictions, and model. Pass `--agent` when resuming to pick a different one. {/* min-version: 2.1.216 */}If the agent no longer exists in the session's original directory or the one you resume from, the session resumes with the default tools and system prompt and shows a [warning naming the agent](/docs/en/errors#session-agent-no-longer-available).
* Permission mode: the mode the session was in. `plan` and `bypassPermissions` are never restored; [bypassing permissions](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) must be enabled again at launch, with one of its launch flags or `permissions.defaultMode: "bypassPermissions"` in [settings](/docs/en/settings#permission-settings). `auto` is restored only when your account still meets the [auto mode requirements](/docs/en/permission-modes#eliminate-prompts-with-auto-mode). Pass `--permission-mode` to override the restored mode.
* Active goal: a [goal](/docs/en/goal#resume-with-an-active-goal) that was still active when the session ended carries over; its turn count, timer, and token-spend baseline reset.
* Scheduled tasks: [tasks that haven't expired](/docs/en/scheduled-tasks#limitations) are restored. Background Bash and monitor tasks aren't.

Not every configuration flag from the original launch is restored. If the session depended on `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model`, or directories added with `--add-dir`, pass them again when you resume; directories added mid-session with `/add-dir` aren't restored either, though the session picker still uses them to locate the session. The standard settings files, such as `settings.json` and `settings.local.json`, are re-read at launch, so configuration that lives in them doesn't need to be passed again.

### Where the session picker looks

Claude Code stores sessions per project directory. By default the session picker shows:

* Sessions from the current worktree, including [background sessions](/docs/en/agent-view), which are marked `bg` in the list
* Sessions started elsewhere that added the current directory with `/add-dir`

Use `Ctrl+W` to widen to all worktrees of the repository or `Ctrl+A` to widen to every project on this machine.

{/* min-version: 2.1.211 */}Sessions whose first prompt was a [`/loop`](/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) command don't appear in the picker; running `/loop` later in a conversation doesn't hide the session. Before v2.1.211, a `/loop` run early in a conversation hid the session from the picker permanently.

{/* min-version: 2.1.169 */}From v2.1.169, moving a session with [`/cd`](/docs/en/commands) relocates it to the new directory's project storage, so it appears in that directory's picker afterward. {/* min-version: 2.1.196 */}As of v2.1.196, a moved session stays out of the old directory's picker even after a crash or forced exit. On earlier versions, it could also reappear in the old directory's list after an exit that wasn't clean when the old path contained special characters such as underscores.

Selecting a session from another worktree of the same repository resumes it in place. Selecting a session from an unrelated project copies a `cd` and resume command to your clipboard instead.

Resuming by name resolves across the current repository and its worktrees. Both forms look for an exact match and resume it directly even if it lives in a different worktree:

| Command                  | Exact match      | Ambiguous name                                                              |
| :----------------------- | :--------------- | :-------------------------------------------------------------------------- |
| `claude --resume <name>` | Resumes directly | Opens the session picker with the name pre-filled as a search term          |
| `/resume <name>`         | Resumes directly | Reports an error; run `/resume` with no argument to open the session picker |

## Name your sessions

Give sessions descriptive names so they're findable in the session picker and resumable by name. This matters most when you're working on several tasks in parallel.

| When                    | How to set the name                                                                                                                                                |
| :---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| At startup              | `claude -n auth-refactor`                                                                                                                                          |
| During a session        | `/rename auth-refactor`. The name also appears on the prompt bar                                                                                                   |
| From the session picker | Highlight a session and press `Ctrl+R`                                                                                                                             |
| On plan accept          | Accepting a plan in [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) names the session from the plan content unless you've already set one |

Once a session is named, return to it with `claude --resume <name>` or `/resume <name>`. See [Resume a session](#resume-a-session) for how name resolution behaves across worktrees.

{/* min-version: 2.1.196 */}Interactive sessions you never name still get a default display name when they start. Requires Claude Code v2.1.196 or later. The default combines the working directory's name with a two-character suffix, for example `my-app-3f`, and identifies the session in listings of running sessions, such as [agent view](/docs/en/agent-view) and `claude agents --json` output.

The default isn't a resume handle: `claude --resume <name>`, `/resume <name>`, and the session picker match only names you set. Naming the session replaces the default.

If you don't name a session, Claude Code generates a session title for it: a short summary of your first prompt, written by a background request to the small/fast model, normally a Haiku-class model. Naming the session with `--name` or `/rename` replaces the generated title. You see the generated title in the [session picker](#use-the-session-picker) and in the statusline [`session_name`](/docs/en/statusline) field when no name is set; like the default display name, it isn't a resume handle.

## Use the session picker

Run `/resume` inside a session, or `claude --resume` with no arguments, to open the interactive session picker. Use these keyboard shortcuts to navigate, search, and widen the list:

| Shortcut                                          | Action                                                                                                                                                       |
| :------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `↑` / `↓`                                         | Navigate between sessions                                                                                                                                    |
| `→` / `←`                                         | Expand or collapse grouped sessions                                                                                                                          |
| `Enter`                                           | Resume the highlighted session                                                                                                                               |
| `Space`                                           | Preview the session content. `Ctrl+V` also works on terminals that don't capture it as paste                                                                 |
| `Ctrl+R`                                          | Rename the highlighted session                                                                                                                               |
| `/` or any printable character other than `Space` | Enter search mode and filter sessions. Paste a GitHub, GitHub Enterprise, GitLab, or Bitbucket pull or merge request URL to find the session that created it |
| `Ctrl+A`                                          | Show sessions from all projects on this machine. Press again to return to the current repository                                                             |
| `Ctrl+W`                                          | Show sessions from all worktrees of the current repository. Press again to return to the current worktree. Only shown in multi-worktree repositories         |
| `Ctrl+B`                                          | Filter to sessions from the current git branch. Press again to show all branches                                                                             |
| `Esc`                                             | Exit the session picker or search mode                                                                                                                       |

Each row shows the session name if you set one, otherwise the AI-generated session title, conversation summary, or first prompt, along with time since last activity, git branch, and file size. Widen to all projects with `Ctrl+A` to also see each session's project path.

Sessions created with `/branch` or `--fork-session` get their own session IDs and appear as separate rows. When the picker finds more than one entry for the same session, it groups them under a single row. Press `→` to expand a group.

If Claude Code can't load the session you select from the `claude --resume` picker, it prints [`Failed to resume the conversation`](/docs/en/errors#failed-to-resume-the-conversation) with a command to retry, then exits with code 1. From the `/resume` picker inside a session, Claude Code reports the failure and your current conversation keeps running.

## Branch a session

Branching creates a copy of the conversation so far and switches you into it, leaving the original intact. Use it to try a different approach without losing the path you were on.

From inside a session, run `/branch` with an optional name:

```text theme={null}
/branch try-streaming-approach
```

If you omit the name, Claude Code names the new branch after the first prompt in the conversation. As of v2.1.198 this also applies after [compaction](/docs/en/how-claude-code-works#when-context-fills-up); earlier versions fell back to the literal name `Branched conversation` instead of looking past the compaction summary to the original first prompt.

From the command line, combine `--continue` or `--resume` with `--fork-session`:

```bash theme={null}
claude --continue --fork-session
```

The `/branch` confirmation prints two session IDs: the new branch you are now in and the original. The original is unchanged on disk and remains in the session picker; return to it with `/resume <original-name>` or by passing its ID to `/resume`.

`/branch` copies the transcript and switches the running Claude Code process to write to it. That distinction determines what the branch inherits:

| State                                                                                                                                                                    | After `/branch`                                                                                                                                                                                                 |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Conversation history                                                                                                                                                     | Copied into the branch up to the point you ran `/branch`                                                                                                                                                        |
| "Allow for this session" permission grants                                                                                                                               | Carried over; the branch runs in the same process, so your existing grants still apply. If you fork into a separate process with `--fork-session`, the new process starts without them and you re-approve there |
| In-flight [background subagents](/docs/en/sub-agents#run-subagents-in-foreground-or-background) and [background Bash commands](/docs/en/interactive-mode#background-bash-commands) | Keep running. Their output appears in the new branch you switched into, not in the original session                                                                                                             |

If you resume the same session in two terminals without forking, messages from both interleave into one transcript. For checkpoint-based rewind within a single session, see [Checkpointing](/docs/en/checkpointing).

## Manage context within a session

These commands control what's in the context window without leaving the session:

* **`/clear`**: start fresh with an empty context. Claude Code saves the previous conversation; resume it with `/resume`, or, in the same Claude Code process, {/* min-version: 2.1.191 */}from [the rewind menu's previous-session entry](/docs/en/checkpointing#rewind-past-a-cleared-conversation). You keep a name you set with `--name` or `/rename` in the new conversation, but not an AI-generated session title
* **`/compact [instructions]`**: replace history with a summary, optionally focused on what you specify
* **`/context`**: show what is currently consuming context

For how compaction interacts with CLAUDE.md, skills, and rules, see the [context window guide](/docs/en/context-window). For strategies on when to clear versus compact, see [Best practices](/docs/en/best-practices#manage-your-session).

## Export and locate session data

Run `/export` to open a menu that lets you copy the current conversation to your clipboard or save it as a plain-text file, with messages and tool outputs rendered as readable text. Pass a filename to skip the menu and write directly to that file.

### Access conversations from scripts

`/export` produces a rendered transcript for a person to read. The interfaces below produce structured data for a script to parse: a JSON result from a run, the path to a session's transcript file, or a live stream of events. Pick by what triggers the script:

* **Run Claude once and capture the result**: invoke `claude -p` with [`--output-format json` or `stream-json`](/docs/en/headless#get-structured-output) to capture the result, session ID, usage, and cost of a non-interactive run as structured JSON.
* **Ask an existing session a question**: pass a session ID to [`claude -p --resume`](/docs/en/headless#continue-conversations) to send a follow-up prompt, such as a summary request, and capture the structured response.
* **React to session events**: read the `transcript_path` field that [hooks](/docs/en/hooks#common-input-fields) and [status line commands](/docs/en/statusline#available-data) receive as input. A `SessionEnd` hook can archive the transcript when a session ends.
* **Embed Claude in a TypeScript or Python app**: use the [Agent SDK](/docs/en/agent-sdk/overview) to receive each message programmatically.

The example below uses the second interface. It sends a follow-up prompt to an existing session and reads the answer with `jq`:

```bash theme={null}
claude -p --resume <session-id> --output-format json "summarize what we changed" | jq -r '.result'
```

### Where transcripts are stored

By default, transcripts are stored as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is your working directory path with non-alphanumeric characters replaced by `-`. Each line is a JSON object for a message, tool use, or metadata entry. The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release. To build on session data, use `/export` or the [script interfaces](#access-conversations-from-scripts) instead.

The location, retention, and write behavior are configurable:

| To                                          | Set                                                    | Where                     |
| ------------------------------------------- | ------------------------------------------------------ | ------------------------- |
| Move storage off `~/.claude`                | [`CLAUDE_CONFIG_DIR`](/docs/en/env-vars)                    | Environment variable      |
| Change the 30-day retention                 | [`cleanupPeriodDays`](/docs/en/settings#available-settings) | `settings.json`           |
| Suppress transcript writes in all modes     | [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/en/env-vars)      | Environment variable      |
| Suppress writes for one non-interactive run | [`--no-session-persistence`](/docs/en/cli-reference)        | CLI flag with `claude -p` |

## See also

These pages cover related session and parallelism mechanics:

* [Worktrees](/docs/en/worktrees): run isolated parallel sessions on separate branches
* [Checkpointing](/docs/en/checkpointing): rewind code and conversation to an earlier point
* [Context window](/docs/en/context-window): what fills context and what survives compaction
* [Non-interactive mode](/docs/en/headless): session behavior under `claude -p`
