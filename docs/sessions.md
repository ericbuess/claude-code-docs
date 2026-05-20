> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage sessions

> Name, resume, branch, and switch between Claude Code conversations. Covers `--continue`, `--resume`, `--from-pr`, the `/resume` picker, session naming, and where transcripts are stored.

A session is a saved conversation tied to a project directory. Claude Code stores it locally as you work, so you can resume where you left off, branch to try a different approach, or switch between tasks.

The [desktop app](/en/desktop#work-in-parallel-with-sessions), [Claude Code on the web](/en/claude-code-on-the-web), and the [VS Code extension](/en/vs-code#resume-past-conversations) each maintain their own session history. This page covers the CLI:

* [Resume](#resume-a-session) a previous conversation by flag, name, or PR
* [Name](#name-your-sessions) sessions so you can find them later
* [Browse](#use-the-session-picker) sessions with the `/resume` picker
* [Branch](#branch-a-session) a conversation to try a different approach
* [Export](#export-and-locate-session-data) transcripts and find them on disk

## Resume a session

Sessions are saved continuously to [local transcript files](#export-and-locate-session-data) as you work, so you can return to one after exiting or running `/clear`. Use these entry points:

| Command                     | What it does                                                       |
| :-------------------------- | :----------------------------------------------------------------- |
| `claude --continue`         | Resumes the most recent session in the current directory           |
| `claude --resume`           | Opens the [session picker](#use-the-session-picker)                |
| `claude --resume <name>`    | Resumes the named session directly                                 |
| `claude --from-pr <number>` | Resumes the session linked to that pull request                    |
| `/resume`                   | Switches to a different conversation from inside an active session |

Sessions created with [`claude -p`](/en/headless) or the [Agent SDK](/en/agent-sdk/overview) do not appear in the session picker, but you can still resume one by passing its session ID to `claude --resume <session-id>`.

### Where the session picker looks

Sessions are stored per project directory. By default the session picker shows interactive sessions from the current worktree, plus sessions started elsewhere that added the current directory with `/add-dir`. Use `Ctrl+W` to widen to all worktrees of the repository or `Ctrl+A` to widen to every project on this machine.

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

Each row shows the session name if set, otherwise the conversation summary or first prompt, along with time since last activity, message count, and git branch. Project path appears after you widen to all projects with `Ctrl+A`.

Forked sessions created with `/branch`, `/rewind`, or `--fork-session` are grouped under their root session. Press `→` to expand a group.

## Branch a session

Branching creates a copy of the conversation so far and switches you into it, leaving the original intact. Use it to try a different approach without losing the path you were on.

From inside a session, run `/branch` with an optional name:

```text theme={null}
/branch try-streaming-approach
```

From the command line, combine `--continue` or `--resume` with `--fork-session`:

```bash theme={null}
claude --continue --fork-session
```

The original session is unchanged and remains available in the session picker. The `/branch` confirmation prints two session IDs: the new branch you are now in and the original. To return to the original, pass its ID to `/resume`, use the session picker, or run `/resume <original-name>`. Permissions you approved with "allow for this session" do not carry over to the new branch. If you resume the same session in two terminals without forking, messages from both interleave into one transcript.

For checkpoint-based rewind within a single session, see [Checkpointing](/en/checkpointing).

## Manage context within a session

These commands control what's in the context window without leaving the session:

* **`/clear`**: start fresh with an empty context. The previous conversation is saved and resumable
* **`/compact [instructions]`**: replace history with a summary, optionally focused on what you specify
* **`/context`**: show what is currently consuming context

For how compaction interacts with CLAUDE.md, skills, and rules, see the [context window guide](/en/context-window). For strategies on when to clear versus compact, see [Best practices](/en/best-practices#manage-your-session).

## Export and locate session data

Run `/export` to copy the current conversation to your clipboard or save it as a plain-text file, with messages and tool outputs rendered as readable text. Pass a filename to write directly to that file.

Transcripts are stored as JSONL at `~/.claude/projects/<project>/<session-id>.jsonl`, where `<project>` is derived from your working directory path. Each line is a JSON object for a message, tool use, or metadata entry. To store sessions somewhere other than `~/.claude`, set [`CLAUDE_CONFIG_DIR`](/en/env-vars). These local files are removed after 30 days by default; change this with [`cleanupPeriodDays`](/en/settings#available-settings).

To suppress transcript writes entirely, set [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/en/env-vars), or in non-interactive mode use `--no-session-persistence`.

## See also

These pages cover related session and parallelism mechanics:

* [Worktrees](/en/worktrees): run isolated parallel sessions on separate branches
* [Checkpointing](/en/checkpointing): rewind code and conversation to an earlier point
* [Context window](/en/context-window): what fills context and what survives compaction
* [Non-interactive mode](/en/headless): session behavior under `claude -p`
