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
| `claude --continue`         | Resumes the most recent interactive session in the current directory      |
| `claude --resume`           | Opens the [session picker](#use-the-session-picker)                       |
| `claude --resume <name>`    | Resumes the named session directly                                        |
| `claude --from-pr <number>` | Opens the session picker filtered to sessions linked to that pull request |
| `/resume`                   | Switches to a different conversation from inside an active session        |

Claude Code leaves sessions created with [`claude -p`](/docs/en/headless) or the [Agent SDK](/docs/en/agent-sdk/overview) out of the session picker and out of `claude --continue`. You can still resume one by passing its session ID to `claude --resume <session-id>`. With `claude --continue`, Claude Code also skips [background sessions](/docs/en/agent-view) and [sessions whose first prompt was `/loop`](#where-the-session-picker-looks). When you run [`claude -p --continue`](/docs/en/headless#continue-conversations), Claude Code includes `-p`, SDK, and `/loop` sessions and still skips background sessions.

You can run `claude --resume <session-id>` from any directory: Claude Code looks for the ID in the current project directory and its git worktrees first, then in every other project on this machine, so it finds a session that started elsewhere or moved with [`/cd`](/docs/en/commands). The cross-project search resolves the ID only when exactly one other project holds a transcript with messages for it, so a hand-copied duplicate makes Claude Code report not-found rather than resume an arbitrary copy. If no stored session matches the ID, Claude Code reports `No conversation found with session ID: <session-id>`. Before v2.1.223, the lookup stopped at the current project directory and its git worktrees, so you had to resume from the directory the session last worked in.

### What a resumed session restores

A resumed session restores the conversation along with the state saved in it:

* Conversation history: the full history, including tool calls and results.
* Model: the session continues on the model it was using. The model isn't restored when it has been retired or isn't allowed by `availableModels`, when a `--model` flag or `ANTHROPIC_MODEL`-family environment variable picks one at launch, or on providers that use provider-specific deployment IDs, such as [Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry](/docs/en/third-party-integrations); see [model configuration](/docs/en/model-config#setting-your-model) for the resolution order.
* Agent: a session started with [`--agent`](/docs/en/sub-agents#invoke-subagents-explicitly) or the `agent` setting continues as that agent, keeping its system prompt, tool restrictions, and model. Pass `--agent` when resuming to pick a different one. Claude Code looks for the agent in two places: the session's original directory, provided you have [trusted that workspace](/docs/en/permissions#project-allow-rules-and-workspace-trust), and then the directory you resume from, so a project-scoped agent still loads when you resume from another directory. If Claude Code doesn't find the agent in either place, the session resumes with the default tools and system prompt and shows a [warning naming the agent](/docs/en/errors#session-agent-no-longer-available).
* Permission mode: if you resume from a terminal with `claude --continue`, `claude --resume <session-id>`, or `claude --resume <name>` when the name matches one session, without `-p`, Claude Code restores the permission mode the session was in, except in the cases in [permission mode on resume](#permission-mode-on-resume), which also covers the session picker, `/resume`, and resuming with `claude -p`. Pass `--permission-mode` or `--dangerously-skip-permissions` to override the restored mode.
* Active goal: a [goal](/docs/en/goal#resume-with-an-active-goal) that was still active when the session ended carries over; its turn count, timer, and token-spend baseline reset.
* Scheduled tasks: [tasks that haven't expired](/docs/en/scheduled-tasks#limitations) are restored. Background Bash and monitor tasks aren't.

Not every configuration flag from the original launch is restored. If the session depended on `--mcp-config`, `--settings`, `--plugin-dir`, `--fallback-model`, or directories added with `--add-dir`, pass them again when you resume; directories added mid-session with `/add-dir` aren't restored either, though the session picker still uses them to locate the session. The standard settings files, such as `settings.json` and `settings.local.json`, are re-read at launch, so configuration that lives in them doesn't need to be passed again.

#### Permission mode on resume

Which permission mode Claude Code starts a resumed session in depends on how you resume:

* Terminal: `claude --continue`, `claude --resume <session-id>`, or `claude --resume <name>` when the name matches one session, without `-p`. Claude Code restores the permission mode the session was in, except in the cases in the table. Pass `--permission-mode` or `--dangerously-skip-permissions` to override the restored mode.
* Non-interactive: `claude -p --resume` or `claude -p --continue`. Claude Code starts the run in the permission mode a new `claude -p` run would start in, except that a session that ended in plan mode resumes in plan mode under the [conditions below](#resume-in-plan-mode-with-p).
* VS Code: the extension's conversation panel. The table covers only a conversation that ended in plan mode; for the rest, see [resume past conversations](/docs/en/vs-code#resume-past-conversations).
* Session picker at launch: a session you select from the [session picker](#use-the-session-picker), whether you opened it with `claude --resume` alone, `claude --from-pr`, or a name that matches more than one session. Claude Code doesn't restore the stored permission mode. It starts the session in the permission mode it would start a new session in from the same command line.
* `/resume` inside a session, with or without an argument: Claude Code doesn't restore the stored permission mode. The conversation you switch to continues in the permission mode your current session is in.

Restoring plan mode on the non-interactive and VS Code paths requires Claude Code v2.1.246 or later. Each row names the permission mode the session ended in, which of the terminal, non-interactive, and VS Code paths you resume it by, and the permission mode Claude Code starts the resumed session in.

| Session ended in    | How you resume                                                             | Permission mode after you resume                                                                                                                                                                                                                                                                                |
| :------------------ | :------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bypassPermissions` | Terminal                                                                   | The permission mode a new session would start in. To [bypass permissions](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) again, enable it at launch with one of its launch flags or `permissions.defaultMode: "bypassPermissions"` in [settings](/docs/en/settings-reference#permission-settings) |
| `plan`              | Terminal                                                                   | The permission mode a new session would start in                                                                                                                                                                                                                                                                |
| `auto`              | Terminal                                                                   | `auto`, only when your account still meets the [auto mode requirements](/docs/en/permission-modes#eliminate-prompts-with-auto-mode)                                                                                                                                                                                  |
| Manual              | Terminal                                                                   | Manual when a new session would start in auto mode from the [built-in default](/docs/en/permission-modes#which-mode-a-session-starts-in). When a `defaultMode` from a settings file [takes effect](/docs/en/permission-modes#which-mode-a-session-starts-in), Claude Code starts the resumed session in that mode instead |
| `plan`              | Non-interactive, under the [conditions below](#resume-in-plan-mode-with-p) | Plan mode                                                                                                                                                                                                                                                                                                       |
| Any mode            | Non-interactive, in any other case                                         | The permission mode a new `claude -p` run would start in                                                                                                                                                                                                                                                        |
| `plan`              | VS Code                                                                    | Plan mode, with [the exceptions on the VS Code page](/docs/en/vs-code#resume-past-conversations)                                                                                                                                                                                                                     |

<h5 id="resume-in-plan-mode-with-p">
  Resume in plan mode with `-p`
</h5>

A `claude -p --resume` or `claude -p --continue` run resumes in plan mode only when all four conditions hold:

* You pass [`--permission-prompt-tool`](/docs/en/cli-reference#cli-flags), so that Claude Code can present the plan for approval
* You don't pass `--permission-mode` or `--dangerously-skip-permissions`
* You don't pass `--fork-session`
* The run isn't started through [channels](/docs/en/channels)

### Resume from a summary

On a Pro or Max plan, when you resume a session that has been inactive for more than about an hour and is over 100,000 tokens, Claude Code restores the conversation and then opens a dialog before you send your first message. The session's [prompt cache](/docs/en/prompt-caching#cache-lifetime) has expired by then, so the next request processes the full history once no matter which of the dialog's options you pick.

The dialog offers three ways to continue the session. They differ in how much of the conversation each one carries forward into later requests, which is a tradeoff between keeping every detail and sending fewer tokens per request:

* **Resume from summary**: runs [`/compact`](/docs/en/context-window#what-survives-compaction) immediately. Claude Code sends one summarization request over the full history, then replaces the history with the summary, your most recent exchanges, and up to five recently read files. Later requests carry the summary instead of the full history.
* **Resume full session as-is**: loads the conversation unchanged. After you send your first message, Claude Code reprocesses and re-caches the full history, then re-reads it from the cache on later requests while the cache stays warm.
* **Don't ask me again**: resumes the full session and stops showing the dialog on all future resumes.

Resuming as-is keeps every detail of the conversation available, at a per-request cost that scales with the conversation's size. Resuming from the summary costs less on each later request because it carries the summary instead of the full history, but whatever the summary leaves out is no longer in Claude's context. See [why usage climbs in a long session](/docs/en/costs#why-usage-climbs-in-a-long-session) for where that per-request cost comes from.

### Where the session picker looks

Claude Code stores sessions per project directory. By default the session picker shows:

* Sessions from the current worktree, including [background sessions](/docs/en/agent-view), which are marked `bg` in the list
* Sessions started elsewhere that added the current directory with `/add-dir`

Use `Ctrl+W` to widen to all worktrees of the repository or `Ctrl+A` to widen to every project on this machine.

Sessions whose first prompt was a [`/loop`](/docs/en/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) command don't appear in the picker, and `claude --continue` skips them too. Running `/loop` later in a conversation doesn't hide the session. Before v2.1.211, a `/loop` run early in a conversation hid the session from the picker permanently.

From v2.1.169, moving a session with [`/cd`](/docs/en/commands) relocates it to the new directory's project storage, so it appears in that directory's picker afterward. As of v2.1.196, a moved session stays out of the old directory's picker even after a crash or forced exit. On earlier versions, it could also reappear in the old directory's list after an exit that wasn't clean when the old path contained special characters such as underscores.

When you select a session from another worktree of the same repository, Claude Code resumes it in place; when the session's own worktree no longer exists, Claude Code [resumes it in your current directory](/docs/en/worktrees#resume-a-worktree-session). When you select a session from an unrelated project, Claude Code copies a `cd` and resume command to your clipboard instead. If that project's directory no longer exists, Claude Code resumes the session in your current directory rather than copying a `cd` command that would fail.

Resuming by name resolves across the current repository and its worktrees. Both forms look for an exact match and resume it directly even if it lives in a different worktree:

| Command                  | Exact match      | Ambiguous name                                                              |
| :----------------------- | :--------------- | :-------------------------------------------------------------------------- |
| `claude --resume <name>` | Resumes directly | Opens the session picker with the name pre-filled as a search term          |
| `/resume <name>`         | Resumes directly | Reports an error; run `/resume` with no argument to open the session picker |

## Name your sessions

Give sessions descriptive names so they're findable in the session picker and resumable by name. This matters most when you're working on several tasks in parallel.

| When                             | How to set the name                                                                                                                                                               |
| :------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| At startup                       | `claude -n auth-refactor`                                                                                                                                                         |
| During a session                 | `/rename auth-refactor`. The name also appears on the prompt bar                                                                                                                  |
| From the session picker          | Highlight a session and press `Ctrl+R`                                                                                                                                            |
| On plan accept                   | Accepting a plan in [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) gives the session a generated title based on the plan unless you've already named it |
| From claude.ai or the Claude app | Rename a [Remote Control session](/docs/en/remote-control#connect-from-another-device); Claude Code applies the same name in the CLI. Requires Claude Code v2.1.221 or later           |
| From the desktop app             | Rename a session in the [desktop app](/docs/en/desktop#work-in-parallel-with-sessions)                                                                                                 |

Once you name a session through a CLI route or from claude.ai, return to it with `claude --resume <name>` or `/resume <name>`; a desktop-app session resumes in the app, which keeps its own session history. See [Resume a session](#resume-a-session) for how name resolution behaves across worktrees.

When you start or resume an interactive session with a name that another live session on this machine already uses, or rename a session into such a name, Claude Code leaves the name with the session that already has it, renames yours to a variant with a two-word suffix, such as `auth-refactor-graceful-unicorn`, and tells you. Run `/rename` with a new name if you'd rather pick one yourself. Before v2.1.232, both sessions kept the name.

In three cases Claude Code doesn't rename the duplicate, so you can still see two sessions with the same name in listings:

* It doesn't check AI-generated titles or default display names.
* It doesn't check the `--name` of a [background](/docs/en/agent-view#from-your-shell) or `-p` session at startup.
* It can't rename a session on an earlier version of Claude Code.

Sessions you don't name still get two labels that Claude Code assigns. Only the generated title works as a resume handle:

* Default display name: interactive sessions you never name still get a default display name when they start. Requires Claude Code v2.1.196 or later. The default combines the working directory's name with a two-character suffix, for example `my-app-3f`, and identifies the session in listings of running sessions, such as [agent view](/docs/en/agent-view) and `claude agents --json` output. The default isn't a resume handle. If you pass it to `claude --resume` or `/resume`, Claude Code doesn't find the session. Naming the session replaces the default in those listings, and so does accepting a plan.
* Generated title: if you don't name a session, Claude Code generates a session title for it. The title is a short summary of your first prompt, written by a background request to the small/fast model, normally a Haiku-class model. Accepting a plan replaces it with a title based on the plan. Naming the session replaces the generated title. You see the first-prompt title in the [session picker](#use-the-session-picker) and in the statusline [`session_name`](/docs/en/statusline) field when no name is set. The plan title shows in the same two places and also in the listings of running sessions, where it takes the place of the default display name. You can pass either title to `claude --resume` or `/resume`, and Claude Code resolves it the same way as a name you set.

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
| [Remote Control](/docs/en/remote-control) connection                                                                                                                          | Stays connected. A phone or browser connected to the session follows you into the branch and keeps receiving new messages there                                                                                 |

If you resume the same session in two terminals without forking, messages from both interleave into one transcript. For checkpoint-based rewind within a single session, see [Checkpointing](/docs/en/checkpointing).

## Manage context within a session

These commands control what's in the context window without leaving the session:

* **`/clear`**: start fresh with an empty context. Claude Code saves the previous conversation; resume it with `/resume`, or, in the same Claude Code process, from [the rewind menu's previous-session entry](/docs/en/checkpointing#rewind-past-a-cleared-conversation). With no argument, the new conversation keeps a name you set with `--name` or `/rename`, but not an AI-generated session title. To name the conversation you're leaving instead, pass the name, as in `/clear release-prep`; the new conversation then starts unnamed
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

By default, Claude Code stores transcripts as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is your working directory path with non-alphanumeric characters replaced by `-`. For a working directory whose converted name exceeds 200 characters, Claude Code truncates the name to 200 characters and appends a hash of the full path, so the directory name stays within filesystem limits.

Each line is a JSON object for a message, tool use, or metadata entry. The entry format is internal to Claude Code and changes between versions, so scripts that parse these files directly can break on any release. To build on session data, use `/export` or the [script interfaces](#access-conversations-from-scripts) instead.

The location, retention, and write behavior are configurable:

| To                                                                                                          | Set                                                                                         | Where                                            |
| ----------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| Move storage off `~/.claude`                                                                                | [`CLAUDE_CONFIG_DIR`](/docs/en/env-vars)                                                         | Environment variable                             |
| [Name the `<project>` directory yourself](#name-the-project-directory-yourself)                             | [`CLAUDE_CODE_PROJECT_DIR_NAME`](/docs/en/env-vars)                                              | Environment variable                             |
| Change the 30-day retention                                                                                 | [`cleanupPeriodDays`](/docs/en/settings-reference#cleanupperioddays)                             | `settings.json`                                  |
| Set an age limit for [Claude Desktop and Cowork transcripts](/docs/en/claude-directory#cleaned-up-automatically) | [`desktopSessionCleanupPeriodDays`](/docs/en/settings-reference#desktopsessioncleanupperioddays) | User settings, managed settings, or `--settings` |
| Suppress transcript writes in all modes                                                                     | [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/en/env-vars)                                           | Environment variable                             |
| Suppress writes for one non-interactive run                                                                 | [`--no-session-persistence`](/docs/en/cli-reference)                                             | CLI flag with `claude -p`                        |

### Name the project directory yourself

By default, Claude Code derives the `<project>` name from the whole working directory path. To choose the name yourself, set `CLAUDE_CODE_PROJECT_DIR_NAME` alongside `CLAUDE_CONFIG_DIR`. Claude Code then stores that session's transcripts and [auto memory](/docs/en/memory#auto-memory) under your name. This suits a host that embeds Claude Code and gives each session its own config directory. Requires Claude Code v2.1.234 or later.

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

* [Worktrees](/docs/en/worktrees): run isolated parallel sessions on separate branches
* [Checkpointing](/docs/en/checkpointing): rewind code and conversation to an earlier point
* [Context window](/docs/en/context-window): what fills context and what survives compaction
* [Non-interactive mode](/docs/en/headless): session behavior under `claude -p`
