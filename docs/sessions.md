> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage sessions

> Name, resume, branch, and switch between Claude Code conversations. Covers `--continue`, `--resume`, `--from-pr`, the `/resume` picker, session naming, exporting transcripts, and where transcripts are stored.

A session is a saved conversation tied to a project directory. Claude Code stores it locally as you work, so you can resume where you left off, branch to try a different approach, or switch between tasks.

The [desktop app](/en/desktop#work-in-parallel-with-sessions), [Claude Code on the web](/en/claude-code-on-the-web), and the [VS Code extension](/en/vs-code#resume-past-conversations) each maintain their own session history. This page covers the CLI.

## Resume a session

Sessions are saved continuously to [local transcript files](#export-and-locate-session-data) as you work, so you can return to one after exiting or running `/clear`. Use these entry points:

| Command                     | What it does                                                              |
| :-------------------------- | :------------------------------------------------------------------------ |
| `claude --continue`         | Resumes the most recent session in the current directory                  |
| `claude --resume`           | Opens the [session picker](#use-the-session-picker)                       |
| `claude --resume <name>`    | Resumes the named session directly                                        |
| `claude --from-pr <number>` | Opens the session picker filtered to sessions linked to that pull request |
| `/resume`                   | Switches to a different conversation from inside an active session        |

Sessions created with [`claude -p`](/en/headless) or the [Agent SDK](/en/agent-sdk/overview) do not appear in the session picker, but you can still resume one by passing its session ID to `claude --resume <session-id>`. Run this from the directory the session was started in: session ID lookup is scoped to the current project directory and its git worktrees, so a session created elsewhere reports `No conversation found with session ID: <session-id>`.

### What a resumed session restores

A resumed session restores the conversation along with the state saved in it:

* Conversation history: the full history, including tool calls and results.
* Model: the session continues on the model it was using. The model isn't restored when it has been retired or isn't allowed by `availableModels`, when a `--model` flag or `ANTHROPIC_MODEL`-family environment variable picks one at launch, or on providers that use provider-specific deployment IDs, such as [Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry](/en/third-party-integrations); see [model configuration](/en/model-config#setting-your-model) for the resolution order.
* Permission mode: the mode the session was in. `plan` and `bypassPermissions` are never restored; [bypassing permissions](/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) must be enabled again at launch, with one of its launch flags or `permissions.defaultMode: "bypassPermissions"` in [settings](/en/settings#permission-settings). `auto` is restored only when your account still meets the [auto mode requirements](/en/permission-modes#eliminate-prompts-with-auto-mode). Pass `--permission-mode` to override the restored mode.
* Active goal: a [goal](/en/goal#resume-with-an-active-goal) that was still active when the session ended carries over; its turn count, timer, and token-spend baseline reset.
* Scheduled tasks: [tasks that haven't expired](/en/scheduled-tasks#limitations) are restored. Background Bash and monitor tasks aren't.

Not every configuration flag from the original launch is restored. If the session depended on `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model`, or directories added with `--add-dir`, pass them again when you resume; directories added mid-session with `/add-dir` aren't restored either, though the session picker still uses them to locate the session. The standard settings files, such as `settings.json` and `settings.local.json`, are re-read at launch, so configuration that lives in them doesn't need to be passed again.

### Where the session picker looks

Sessions are stored per project directory. By default the session picker shows interactive sessions from the current worktree, plus sessions started elsewhere that added the current directory with `/add-dir`. Use `Ctrl+W` to widen to all worktrees of the repository or `Ctrl+A` to widen to every project on this machine.

{/* min-version: 2.1.211 */}Sessions whose first prompt was a [`/loop`](/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) command don't appear in the picker; running `/loop` later in a conversation doesn't hide the session. Before v2.1.211, a `/loop` run early in a conversation hid the session from the picker permanently.

{/* min-version: 2.1.169 */}From v2.1.169, moving a session with [`/cd`](/en/commands) relocates it to the new directory's project storage, so it appears in that directory's picker afterward. {/* min-version: 2.1.196 */}As of v2.1.196, a moved session stays out of the old directory's picker even after a crash or forced exit. On earlier versions, it could also reappear in the old directory's list after an exit that wasn't clean when the old path contained special characters such as underscores.

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
| On plan accept          | Accepting a plan in [plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) names the session from the plan content unless you've already set one |

Once a session is named, return to it with `claude --resume <name>` or `/resume <name>`. See [Resume a session](#resume-a-session) for how name resolution behaves across worktrees.

{/* min-version: 2.1.196 */}Interactive sessions you never name still get a default display name when they start. Requires Claude Code v2.1.196 or later. The default combines the working directory's name with a two-character suffix, for example `my-app-3f`, and identifies the session in listings of running sessions, such as [agent view](/en/agent-view) and `claude agents --json` output.

The default isn't a resume handle: `claude --resume <name>`, `/resume <name>`, and the session picker match only names you set. Naming the session replaces the default.

If you don't name a session, Claude Code generates a session title for it: a short summary of your first prompt, written by a background request to the small/fast model, normally a Haiku-class model. Naming the session with `--name` or `/rename` replaces the generated title. You see the generated title in the [session picker](#use-the-session-picker) and in the statusline [`session_name`](/en/statusline) field when no name is set; like the default display name, it isn't a resume handle.

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

## Branch a session

Branching creates a copy of the conversation so far and switches you into it, leaving the original intact. Use it to try a different approach without losing the path you were on.

From inside a session, run `/branch` with an optional name:

```text theme={null}
/branch try-streaming-approach
```

If you omit the name, Claude Code names the new branch after the first prompt in the conversation. As of v2.1.198 this also applies after [compaction](/en/how-claude-code-works#when-context-fills-up); earlier versions fell back to the literal name `Branched conversation` instead of looking past the compaction summary to the original first prompt.

From the command line, combine `--continue` or `--resume` with `--fork-session`:

```bash theme={null}
claude --continue --fork-session
```

The original session is unchanged and remains available in the session picker. The `/branch` confirmation prints two session IDs: the new branch you are now in and the original. To return to the original, pass its ID to `/resume`, use the session picker, or run `/resume <original-name>`. Permissions you approved with "allow for this session" do not carry over to the new branch. If you resume the same session in two terminals without forking, messages from both interleave into one transcript.

For checkpoint-based rewind within a single session, see [Checkpointing](/en/checkpointing).

## Manage context within a session

These commands control what's in the context window without leaving the session:

* **`/clear`**: start fresh with an empty context. Claude Code saves the previous conversation; resume it with `/resume`, or, in the same Claude Code process, {/* min-version: 2.1.191 */}from [the rewind menu's previous-session entry](/en/checkpointing#rewind-past-a-cleared-conversation). You keep a name you set with `--name` or `/rename` in the new conversation, but not an AI-generated session title
* **`/compact [instructions]`**: replace history with a summary, optionally focused on what you specify
* **`/context`**: show what is currently consuming context

For how compaction interacts with CLAUDE.md, skills, and rules, see the [context window guide](/en/context-window). For strategies on when to clear versus compact, see [Best practices](/en/best-practices#manage-your-session).

## Export and locate session data

Run `/export` to open a menu that lets you copy the current conversation to your clipboard or save it as a plain-text file, with messages and tool outputs rendered as readable text. Pass a filename to skip the menu and write directly to that file.

### Access conversations from scripts

`/export` produces a rendered transcript for a person to read. The interfaces below produce structured data for a script to parse: a JSON result from a run, the path to a session's transcript file, or a live stream of events. Pick by what triggers the script:

* **Run Claude once and capture the result**: invoke `claude -p` with [`--output-format json` or `stream-json`](/en/headless#get-structured-output) to capture the result, session ID, usage, and cost of a non-interactive run as structured JSON.
* **Ask an existing session a question**: pass a session ID to [`claude -p --resume`](/en/headless#continue-conversations) to send a follow-up prompt, such as a summary request, and capture the structured response.
* **React to session events**: read the `transcript_path` field that [hooks](/en/hooks#common-input-fields) and [status line commands](/en/statusline#available-data) receive as input. A `SessionEnd` hook can archive the transcript when a session ends.
* **Embed Claude in a TypeScript or Python app**: use the [Agent SDK](/en/agent-sdk/overview) to receive each message programmatically.

The example below uses the second interface. It sends a follow-up prompt to an existing session and reads the answer with `jq`:

```bash theme={null}
claude -p --resume <session-id> --output-format json "summarize what we changed" | jq -r '.result'
```

### Where transcripts are stored

By default, transcripts are stored as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is your working directory path with non-alphanumeric characters replaced by `-`. Each line is a JSON object for a message, tool use, or metadata entry. The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release. To build on session data, use `/export` or the [script interfaces](#access-conversations-from-scripts) instead.

The location, retention, and write behavior are configurable:

| To                                          | Set                                                    | Where                     |
| ------------------------------------------- | ------------------------------------------------------ | ------------------------- |
| Move storage off `~/.claude`                | [`CLAUDE_CONFIG_DIR`](/en/env-vars)                    | Environment variable      |
| Change the 30-day retention                 | [`cleanupPeriodDays`](/en/settings#available-settings) | `settings.json`           |
| Suppress transcript writes in all modes     | [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/en/env-vars)      | Environment variable      |
| Suppress writes for one non-interactive run | [`--no-session-persistence`](/en/cli-reference)        | CLI flag with `claude -p` |

## See also

These pages cover related session and parallelism mechanics:

* [Worktrees](/en/worktrees): run isolated parallel sessions on separate branches
* [Checkpointing](/en/checkpointing): rewind code and conversation to an earlier point
* [Context window](/en/context-window): what fills context and what survives compaction
* [Non-interactive mode](/en/headless): session behavior under `claude -p`
