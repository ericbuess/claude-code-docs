> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage multiple agents with agent view

> Dispatch and manage many Claude Code sessions from one screen. Agent view shows what every session is doing and which ones need your input.

Agent view, opened with `claude agents`, is one screen for all your background sessions: what's running, what needs your input, and what's done. Dispatch new sessions, watch their state at a glance instead of scrolling through transcripts, and step in only when one needs you. Each background session is a full Claude Code conversation that keeps running without a terminal attached, so you can open it, reply, and leave whenever you want.

<img src="https://mintcdn.com/claude-code/1B48Qz2Z9hac4SLG/images/agent-view-light.png?fit=max&auto=format&n=1B48Qz2Z9hac4SLG&q=85&s=7a186c96ed47d6700d084d77e786be65" className="dark:hidden" alt="Agent view in a terminal: the header shows Claude Code v2.1.140, the model, the working directory, and a summary count. Sessions are grouped under Needs input, Working, and Completed, with a dispatch input at the bottom and a footer of keyboard hints." width="1772" height="780" data-path="images/agent-view-light.png" />

<img src="https://mintcdn.com/claude-code/1B48Qz2Z9hac4SLG/images/agent-view-dark.png?fit=max&auto=format&n=1B48Qz2Z9hac4SLG&q=85&s=a5bed7434bae368faea3a8f023b52aa2" className="hidden dark:block" alt="Agent view in a terminal: the header shows Claude Code v2.1.140, the model, the working directory, and a summary count. Sessions are grouped under Needs input, Working, and Completed, with a dispatch input at the bottom and a footer of keyboard hints." width="1772" height="780" data-path="images/agent-view-dark.png" />

Use agent view when you have several independent tasks Claude can work on without you watching every step. Dispatch a bug fix, a pull request review, and a flaky-test investigation as three rows, keep working in another window, and check back when a row shows it needs you or has a result.

When you want to work more directly in any agent's session, attach to the row to enter the full conversation.

To compare agent view with subagents, agent teams, and worktrees, see [Run agents in parallel](/docs/en/agents).

<Note>
  Agent view is in research preview and requires Claude Code v2.1.139 or later. Check your version with `claude --version`. The interface and keyboard shortcuts may change as the feature evolves.
</Note>

## Quick start

This walkthrough covers the core agent view loop: dispatch a task, watch its row update as Claude works, peek to check on it and reply, and attach for the full conversation. The session you dispatch keeps running after you close agent view, so you can leave and come back to it.

<Steps>
  <Step title="Open agent view">
    From your shell, run:

    ```bash theme={null}
    claude agents
    ```

    Agent view opens with an input at the bottom and a table that fills in as sessions start. Press `Esc` at any time to return to your shell; if you opened agent view by backgrounding a session with `←`, `Esc` returns to that conversation instead. Your sessions keep running while you're away and reappear the next time you open agent view.
  </Step>

  <Step title="Dispatch a session">
    Type a prompt describing a task and press `Enter`. A new background session starts on that task and appears as a row showing whether it's working, waiting on you, or done. The new session uses the model shown in the agent view header and the same [permission mode](#permission-mode-model-and-effort) you'd get running `claude` in that directory.

    Every prompt you enter here starts its own new session. Typing another prompt and pressing `Enter` launches a second session alongside the first rather than sending a follow-up to it. You can run several in parallel this way.

    Each session uses your subscription quota independently, so see [Limitations](#limitations) before dispatching many at once.
  </Step>

  <Step title="Peek and reply">
    Select a row with the arrow keys and press `Space` to open the peek panel. It shows the session's most recent output, or the question it's waiting on, rather than the full transcript. Type a reply and press `Enter` to send it without leaving agent view.
  </Step>

  <Step title="Attach and detach">
    Press `Enter` or `→` on a row to attach when you want the full conversation. The session takes over the terminal as a full interactive Claude Code session. Press `←` on an empty prompt to detach and return to the table.
  </Step>

  <Step title="Bring an existing session in">
    This step needs a running session. If you followed the earlier steps you don't have one open in this terminal, so open a regular `claude` session in another terminal and send it a message first.

    To move a session you already have open into agent view, run `/bg` inside it, or press `←` on an empty prompt to background it and open agent view in one step. In a fresh session with no messages yet, `/bg` asks you to send a message first, while `←` works right away. The session keeps running and appears as a row alongside the ones you dispatched.
  </Step>
</Steps>

You can use `claude agents` as your primary entry point instead of `claude`: dispatch every task from agent view, attach when you want the full conversation, and press `←` to return to the table.

{/* min-version: 2.1.205 */}Inside a regular `claude` session, the prompt footer's `←` hint counts the background agents that are waiting on you, such as `← 2 agents`, and returns to `← for agents` when none need input. Counts above 99 show as `99+`. The count refreshes about every ten seconds while the terminal is focused and immediately when focus returns. It briefly changes color when it moves and when an agent completes, {/* min-version: 2.1.212 */}and when a background session finishes while none need your input it briefly shows the number completed, such as `← 2 done`. Both flashes are off when the [`prefersReducedMotion` setting](/docs/en/settings#available-settings) is on, and the hint is hidden in [screen reader mode](/docs/en/accessibility).

{/* min-version: 2.1.210 */}The count appears on every provider, including [Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry](/docs/en/third-party-integrations).

## Monitor sessions with agent view

Run `claude agents` to open agent view. It takes over the full terminal and lists every session grouped by state, with pinned sessions and the ones that need you at the top. Each row shows the session's name, current activity, and its age, counted from when the session was created; a finished session's age freezes at how long the run took.

The name is tinted with the color set by [`/color`](/docs/en/commands) in that session, {/* min-version: 2.1.199 */}including when you [background a session](#from-inside-a-session) with `←` or `/background`.

By default the list shows every background session you've started, across all your projects. A session working in one repository and another in a different worktree both appear here, regardless of which directory you opened agent view from. To narrow the list to one project, pass `--cwd`:

```bash theme={null}
claude agents --cwd ~/projects/my-app
```

This shows only sessions started under that directory. A session that has [moved into a worktree](#how-file-edits-are-isolated) under `~/projects/my-app/.claude/worktrees/` still counts as belonging to `~/projects/my-app`.

Interactive sessions you have open in other terminals don't appear until you [background them](#from-inside-a-session). [Subagents](/docs/en/sub-agents) and [teammates](/docs/en/agent-teams) a session spawns aren't listed as separate rows.

```text theme={null}
Pinned
  ✽ clawd walk cycle          Drawing the walk-cycle sprite frames          3m

Ready for review
  ∙ jump physics              Opened PR with collision fix                 #2048  2h

Needs input
  ✻ power-up design           double jump or wall climb?                    1m

Working
  ✽ collision detection       Adding swept-AABB checks to CollisionSystem   2m
  ✢ playtest level 3          run 12 · all checkpoints cleared           in 4m

Completed
  ✻ title screen              result: menu, options, and credits done       9m
  ∙ sound effects             result: 14 SFX exported to assets/audio       4h
  … 6 more
```

### Read session state

Each row starts with an icon whose color and animation show the session's state:

| State       | Icon shows as | What it means                                                                                                                                                                                                                                                                                                                                                                                                                  |
| :---------- | :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Working     | Animated      | Claude is actively running tools or generating a response                                                                                                                                                                                                                                                                                                                                                                      |
| Needs input | Yellow        | Claude is waiting on something only you can provide: an answer to a question, a permission decision, {/* min-version: 2.1.212 */}a [sandbox](/docs/en/sandboxing) prompt to allow a network host, an MCP server's [request for input](/docs/en/mcp#respond-to-mcp-elicitation-requests), a managed-settings prompt, or {/* min-version: 2.1.216 */}an MCP authentication or settings request held by a session with no terminal attached |
| Idle        | Dimmed        | The session has nothing to do and is ready for your next prompt                                                                                                                                                                                                                                                                                                                                                                |
| Completed   | Green         | The task finished successfully                                                                                                                                                                                                                                                                                                                                                                                                 |
| Failed      | Red           | The task ended with an error                                                                                                                                                                                                                                                                                                                                                                                                   |
| Stopped     | Grey          | The session was stopped with `Ctrl+X` or `claude stop`, or [its process was ended from outside Claude Code](#the-supervisor-process)                                                                                                                                                                                                                                                                                           |

Separately, the icon's shape shows whether the underlying process is running:

| Shape               | What it means                                                                                                     |
| :------------------ | :---------------------------------------------------------------------------------------------------------------- |
| `✻` or animated `✽` | The session process is alive and replies immediately                                                              |
| `∙`                 | The process has exited. You can still peek, reply, or attach, and Claude restarts from where it left off          |
| `✢`                 | A [`/loop`](/docs/en/scheduled-tasks) session sleeping between iterations. The row shows its run count and a countdown |

The `#N` label that can appear at the right edge of a row is a [pull request the session is linked to](#pull-request-status), not part of the state icon.

The terminal tab title shows the awaiting-input count while agent view is open: `2 awaiting input · claude agents` when sessions need input, or `claude agents` when none do.

While agent view is open, Claude Code also sends a notification through your configured [terminal notification channel](/docs/en/terminal-config#get-a-terminal-bell-or-notification) when a local background session starts needing your input, finishes, or fails. Sessions that run on a schedule, such as [`/loop`](/docs/en/scheduled-tasks) sessions, notify only when they need your input. Notifications use the same [`preferredNotifChannel` setting](/docs/en/settings#available-settings) as the rest of Claude Code and fire the [`Notification` hook](/docs/en/hooks#notification) with the `agent_needs_input` or `agent_completed` type.

Background sessions don't need any terminal open to keep working. A separate [supervisor process](#the-supervisor-process) runs them, so you can close agent view, close your shell, or start a new interactive session and your dispatched work keeps going.

Session state persists on disk through auto-updates and supervisor restarts. Sessions are also preserved when your machine sleeps. Their processes resume on wake and the supervisor reconnects to them instead of treating the time gap as idle. Shutting down still stops running sessions; see [Sessions show as failed after shutdown](#sessions-show-as-failed-after-shutdown) for how to recover them.

A session that was mid-response when the machine slept can come back unresponsive. When you open a session that has stopped responding, the supervisor restarts its process and the session continues the interrupted response from where it left off.

### Row summaries

The one-line summary in each row is generated by a [Haiku-class model](/docs/en/model-config) so the row can tell you what the session is doing, what it needs, or what it produced without opening the transcript. While a session is actively working, the row text updates at most once every 15 seconds from the session's own recent output without sending a model request, and the model writes a fresh summary when each turn ends.

A working row shows what the session says it's doing, and a blocked row shows the question it's asking. During a long turn, the model also rewrites the summary every few minutes so a busy row doesn't keep showing an outdated one. {/* min-version: 2.1.206 */}The summary text fills the row's remaining width; open the [peek panel](#peek-and-reply) to read a sentence the terminal edge clips.

When the list is [grouped by directory](#organize-the-list), the summary opens with the session's state as a colored word, such as `Needs input · double jump or wall climb?`. In the default state grouping, the group header already names the state, so the row shows only the summary.

The end-of-turn summary and each mid-turn rewrite are one short Haiku-class request through your normal provider, billed and handled under the same [data usage terms](/docs/en/data-usage) as the session itself. The 15-second updates between model rewrites reuse the session's own output and don't send a request. On third-party providers such as Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and custom gateways, the request falls back to the session's main model when no Haiku model is configured. Set [`ANTHROPIC_DEFAULT_HAIKU_MODEL`](/docs/en/model-config#environment-variables) to choose the model for these summaries on those providers.

### Pull request status

When a session opens a pull request, a `#1234` label appears at the right edge of the row, linked to the pull request in terminals that support hyperlinks. The label persists when you send a follow-up to the session, so the pull request remains visible while the row reverts to live progress. Background sessions that isolated their changes in a worktree open these pull requests themselves; [How file edits are isolated](#how-file-edits-are-isolated) covers when that happens and what a session never does without asking.

A session that works on an existing pull request is linked to it the same way. Editing, commenting on, closing, or marking a pull request ready with `gh` links the pull request that the command's own output names, so a `gh` command whose captured output names no pull request doesn't create a link; `gh pr merge` is the common case, because it prints its result only to an interactive terminal. Checking a pull request out with `gh pr checkout`, or pushing to a branch that has an open pull request, links it by looking up that branch with `gh pr view` instead.

When a session is linked to more than one pull request, the label shows a count instead, such as `3 PRs`, colored by the open pull request that most needs attention. Open the [peek panel](#peek-and-reply) to see them all.

The pull request number is colored by its status:

| Color  | Pull request status                           |
| :----- | :-------------------------------------------- |
| Yellow | Waiting on checks or review, or checks failed |
| Green  | Checks passed and no review is blocking       |
| Purple | Merged                                        |
| Grey   | Draft or closed                               |

For most tasks this column is where you pick up the result: review and merge the pull request when its number turns green.

### Peek and reply

Press `Space` on a selected row to open the peek panel. It opens with the sentence the row truncates at the terminal edge, and which sentence that is depends on the session's state:

* A session that's waiting on you: the exact question it's asking, above the reply input
* A finished session: its result
* A working session: its full status sentence

Any pull requests linked to the session are listed next. For a session that's waiting on you, a line such as `waiting 3m` below them shows how long it has been waiting, and it's the only time shown in the panel. The age at the right edge of the row is a different number: it counts from when the session started.

Most of the time the peek panel is enough and you don't need to open the full transcript.

Type a reply in the peek panel and press `Enter` to send it to that session. When the session asks a question with predefined choices, the peek panel shows them as a numbered list and you can press a number key to pick one. A permission prompt shows as text describing what the session wants to run, without numbered options. Type a reply to answer it, or attach to answer with the standard prompt. For other blocked sessions, press `Tab` to fill the input with a suggested reply you can edit before sending. Prefix a reply with `!` to send a Bash command instead.

A reply that can't be delivered, because the background service is unreachable or the send fails, is saved and sent to the session as its next prompt when its process starts again, and the error message says the reply was saved. A reply prefixed with `!` isn't saved, because the saved text would reach the session as a plain prompt rather than run as a Bash command.

With [voice dictation](/docs/en/voice-dictation) enabled, hold or tap your push-to-talk key while the reply input is focused to dictate a reply instead of typing it. The same works in the dispatch input at the bottom of agent view.

Use `↑` and `↓` to peek at adjacent sessions without closing the panel, or `→` to attach.

### Attach to a session

Press `Enter` or `→` on a selected row to attach. Agent view is replaced by the full interactive session. When you attach, Claude posts a short recap of what happened while you were away.

While attached, the session behaves like any other Claude Code session: [commands](/docs/en/commands), keyboard shortcuts, and features all work, with the exceptions below.

While you're attached, `/install-github-app` and the [`/mcp`](/docs/en/mcp) settings list work normally, since a human at the terminal can complete their dialogs. When nobody is attached, these commands can't open their dialogs, so the session appears under `Needs input` in agent view with a row such as `open this session to manage MCP servers`, and the transcript reply says the same. Attach and run the command again to continue; the needs-input row clears when you attach. `/mcp reconnect <server>`, `/mcp enable`, and `/mcp disable` work without attaching either way.

Attached sessions always render in [fullscreen mode](/docs/en/fullscreen), regardless of your `tui` setting, because a background session has no terminal scrollback to append to. Scroll with `PgUp`, `PgDn`, or the mouse wheel, and press `Ctrl+O` for transcript mode. Your terminal's native scroll and tmux copy mode show only the current viewport, the same as when you run any fullscreen application.

Press `←` on an empty prompt, or run `/exit`, to detach and return to agent view, whether you opened the session from agent view or with `claude attach <id>` from your shell.

On Windows, if you press `←` within about half a second of attaching, Claude Code shows `Ambiguous ←, press again to detach`, because in that window the terminal can redeliver a press from before you attached. Press `←` again to detach.

`Ctrl+Z` also detaches but goes back to where you started instead: agent view if you attached from there, or your shell if you ran `claude attach`. Use `Ctrl+Z` when a dialog has focus and isn't responding to `←`.

`Ctrl+C` keeps its standard interrupt behavior while attached: it cancels a running response or `!` shell command rather than detaching. Pressing `Ctrl+C` twice on an empty prompt detaches, the same as in any session.

Detaching never stops a background session: `←`, `Ctrl+Z`, `/exit`, and double `Ctrl+C` or double `Ctrl+D` all leave it running. To end a session from inside it, run `/stop`.

In a session running in the foreground, one you started in the terminal rather than attached to from agent view, pressing `←` on an empty prompt backgrounds it and opens agent view with that row selected, so you can switch sessions without leaving the terminal. The same single press detaches an attached session.

If you press `←` right after you delete the last of the prompt's text or move through prompt history, Claude Code asks you to confirm: the first press shows `Press ← again to open agents`, or `Press ← again to go back to agents` in an attached session, and the second press switches.

When `←` backgrounds a foreground session, agent view shows `Your conversation moved to the background` above the list, with that session's row already selected. From there:

* Press `Enter` to reopen the conversation.
* Press `Esc` to undo the switch and return to the conversation. If `Esc` shows `Still starting — try again in a moment`, the background session isn't ready yet, so press `Esc` again in a moment.
* Press `Ctrl+C` twice to exit to your shell.

When Claude Code can't reopen the conversation, it exits and prints a `claude --resume` command that resumes it.

[Claude's task list](/docs/en/interactive-mode#task-list) moves to the background session with the conversation, so the checklist is intact when you return to that row.

The row you pressed `←` from also keeps a bold, undimmed name after you move the selection with the arrow keys or the mouse, so you can tell which session you came from.

If a tool is running when you press `←`, Claude Code waits up to about ten seconds for it to finish before backgrounding, and the response continues in the background session. Press `←` again to background immediately instead of waiting. When in-flight work can't carry over to the background session, the `Background this session?` dialog appears first, the same as with [`/background`](#from-inside-a-session).

The ten-second limit doesn't apply while [subagents](/docs/en/sub-agents) are running. Claude Code keeps waiting so their work carries over, and shows a `Still backgrounding after the current tool` notice while it waits; press `←` again to background without waiting, which restarts the subagents from the beginning.

Pressing `←` creates the session's row even when the conversation has no messages yet, so `→` still returns to it.

You can turn this shortcut off with the `leftArrowOpensAgents` setting in `/config`.

### Organize the list

Agent view groups sessions so the ones that need input are at the top, with `Ready for review` and `Needs input` above `Working` and `Completed`. These group names don't map one-to-one to the [states](#read-session-state) above: a session moves to `Ready for review` when it has an open pull request, and `Completed` collects finished, failed, and stopped sessions together.

Press `Ctrl+S` to group by directory instead. Your choice persists across runs.

Within a group:

* Press `Ctrl+T` to pin a session to the top and [keep its process running](#the-supervisor-process) while idle
* Press `Shift+↑` or `Shift+↓` to reorder sessions
* Press `Ctrl+R` to rename a session
* Press `Enter` on a group header to collapse it

To remove a session from the list, press `Ctrl+X` to stop it and `Ctrl+X` again within two seconds to delete it. Pressing `Ctrl+X` on a group header deletes every session in that group after confirmation.

Deleting removes the session from agent view. If Claude [created a worktree](#how-file-edits-are-isolated) for the session, deleting removes that worktree too, including any uncommitted changes in it, so commit work you want to keep first. A worktree you created yourself and started the session inside is left in place. The conversation transcript stays on your local machine and remains available through `claude --resume`.

Deleting never removes a worktree with commits that aren't pushed anywhere, or one that another running session claims or has locked. Claude Code keeps the worktree and the session, and the footer names the kept path and the reason. Push the commits, or close the other session, then delete again.

When a delete is refused, the session's row shows `not deleted` with the reason, and a worktree that couldn't be removed is reported with the underlying git error. A worktree that git no longer recognizes, for example one removed from git's records by `git worktree prune`, doesn't block deletion: the session is deleted, the worktree directory is left untouched on disk, and the footer names its path.

Deleting also clears the session from the [supervisor's](#the-supervisor-process) session list, whether you delete with `Ctrl+X` or with [`claude rm`](#manage-sessions-from-the-shell) from the shell, so the removal persists across supervisor restarts.

To bring a session back on Claude Code v2.1.212 or later, type `/resume` in the dispatch input. A picker opens with past sessions of the repository you opened agent view from, newest first, including sessions you deleted from the list; sessions that already have a row aren't listed. `↑`/`↓` move the selection, `Enter` resumes the selected session as a background session so it rejoins the list as a row, and `Esc` closes the picker.

The picker opens only for a bare `/resume`. A targeted, scoped, or restricted resume can't be served by the picker, so agent view shows the `attach to a session to run it` hint instead when:

* `/resume` names an id or a search term
* the view is scoped with `--cwd`
* the view was started with [`--safe-mode`](/docs/en/cli-reference#cli-flags)
* the view was opened with a flag such as `--permission-mode` or `--settings`

Completed sessions that don't fit on screen fold into a `… N more` row. Failures and sessions with an open pull request always stay visible. The `Completed` group fills the vertical space left after the live groups, and on a short terminal the header compacts to a single summary line so sessions that are working or need input stay visible.

### Filter sessions

Type in the dispatch input to filter instead of dispatching:

| Filter                  | Shows                                                                                                    |
| :---------------------- | :------------------------------------------------------------------------------------------------------- |
| `a:<name>`              | Sessions running the named agent                                                                         |
| `s:<state>`             | Sessions in the given state, such as `s:working`. Also accepts `s:blocked` for everything waiting on you |
| `#<number>` or a PR URL | The session working on that pull request                                                                 |
| Any other URL           | The session whose first prompt contained that URL                                                        |

### Keyboard shortcuts

Press `?` in agent view to see every shortcut in context. The table below summarizes them.

| Shortcut              | Action                                                                                                                                                                             |
| :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `↑` / `↓`             | Move between rows                                                                                                                                                                  |
| `Enter`               | Attach to the selected session, or dispatch if there's text in the input                                                                                                           |
| `Space`               | Open or close the peek panel for the selected session                                                                                                                              |
| `Shift+Enter`         | Dispatch and attach immediately                                                                                                                                                    |
| `→`                   | Attach to the selected session                                                                                                                                                     |
| `Alt+1`..`Alt+9`      | Attach to session 1–9 in the focused session's directory                                                                                                                           |
| `Tab`                 | On an empty input, browse all subagents. Otherwise apply the highlighted suggestion                                                                                                |
| `Ctrl+S`              | Switch grouping between state and directory                                                                                                                                        |
| `Ctrl+T`              | Pin or unpin the selected session                                                                                                                                                  |
| `Ctrl+R`              | Rename the selected session                                                                                                                                                        |
| `Ctrl+G`              | Open the dispatch prompt in your `$VISUAL` or `$EDITOR`                                                                                                                            |
| `Ctrl+J`              | Insert a newline in the dispatch input. {/* min-version: 2.1.212 */}Before v2.1.212, terminals with extended key reporting ignored the keypress                                    |
| `Ctrl+X`              | Stop the session; press again within two seconds to delete it                                                                                                                      |
| `Shift+↑` / `Shift+↓` | Reorder the selected session                                                                                                                                                       |
| `Esc`                 | Close the peek panel, clear the input, or exit. When you opened agent view by backgrounding your session with `←`, the final `Esc` returns to that conversation instead of exiting |
| `Ctrl+C`              | Clear the input; press twice to exit                                                                                                                                               |
| `?`                   | Show all shortcuts                                                                                                                                                                 |

## Dispatch new agents

You can dispatch new background sessions from agent view, send or copy an existing interactive session to the background, or start one directly from the shell.

### From agent view

Type a prompt in the input at the bottom of agent view and press `Enter` to start a new background session. The session is named automatically from the prompt; rename it later with `Ctrl+R`.

The automatic name is a short label written by a [Haiku-class model](/docs/en/model-config). {/* min-version: 2.1.207 */}A name the session gets later also appears on its row, including the name Claude derives when you [accept a plan](/docs/en/permission-modes#review-and-approve-a-plan) in that session.

Paste an image into the prompt to include a screenshot or diagram with the task.

Pasted text longer than 800 characters or more than two lines collapses to a `[Pasted text #N]` placeholder so the input stays on one line; the full text is sent when you dispatch. {/* min-version: 2.1.207 */}To review or edit the collapsed text before dispatching, paste the same text again and the placeholder expands back into the input.

Prefix or mention parts of the prompt to control how the session starts:

| Input                             | Effect                                                                                                                                                         |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<agent-name> <prompt>`           | If the first word matches a custom [subagent](/docs/en/sub-agents) name, that subagent runs as the session's main agent with the configuration from its frontmatter |
| `@<agent-name>`                   | Mention a custom subagent anywhere in the prompt to run it as the main agent                                                                                   |
| `@<repo>`                         | Mention a repository to run the session there. See [Dispatch to a specific directory](#dispatch-to-a-specific-directory) for which repositories are listed     |
| `/<command>`                      | Suggest [skills](/docs/en/skills) and [commands](/docs/en/commands) to dispatch as the prompt                                                                            |
| `! <command>`                     | Run a shell command as a background job instead of starting a Claude session. The job appears as a row you can attach to, watch, and detach from               |
| `#<number>` or a pull request URL | If a session is already working on that PR, select it instead of dispatching                                                                                   |
| `Shift+Enter`                     | Dispatch and immediately attach to the new session                                                                                                             |

A small set of commands run in agent view itself instead of dispatching:

* `/exit` and `/quit` close agent view
* `/logout` signs you out
* `/model` sets the [dispatch model](#set-the-model)
* {/* min-version: 2.1.198 */}`/login` opens the sign-in dialog so you can sign in again without attaching to a session
* {/* min-version: 2.1.212 */}A bare `/resume`, or its `/continue` alias, opens a picker of the repository's past sessions to [bring one back](#organize-the-list) as a background session. Requires Claude Code v2.1.212 or later

Skills, your own commands, and prompt-expanding built-ins such as `/init` are sent to a new background session as their first prompt. Other built-in commands show an `attach to a session to run it` hint instead. {/* min-version: 2.1.203 */}Everything you typed stays in the input next to the hint so you can edit it.

Packaging a recurring task as a [skill](/docs/en/skills) lets you start the same workflow from agent view repeatedly without retyping the prompt.

When the same `@name` matches both a subagent and a sibling repository, the subagent takes precedence. The bare first-word match also applies, so a prompt that happens to begin with one of your subagent names dispatches that subagent rather than treating the word as plain text. Use the `@` form when you want to be explicit, or start the prompt with a different word to avoid the match.

#### Dispatch to a specific directory

A new session runs in the directory you opened agent view from. To target a different directory, use any of these:

* Open `claude agents` in that directory.
* Open `claude agents` in a parent directory and mention a child repository with `@<repo>` in the prompt. Typing `@` lists these targets:

  * Git repositories one level below the launch directory
  * The registered [git worktrees](/docs/en/worktrees) of the repository you launched from that live inside its directory tree, such as the ones Claude creates under `.claude/worktrees/`, labeled with their checked-out branch. Worktrees added outside the repository, such as with `git worktree add ../feature`, aren't listed
  * Any directory that already has a session in the list

  A directory whose name contains a space isn't listed.
* From the shell, `cd` into the directory and run `claude --bg "<prompt>"`.

When agent view is grouped by directory, the highlighted row's directory becomes the dispatch target, so you can scroll to a group and dispatch into it without retyping the path.

### From inside a session

Two commands move work from the session you're in to the background: `/background` sends the current conversation there and frees your terminal, and `/fork` sends a copy while you keep working where you are.

#### Send the session to the background

Run `/background` or its alias `/bg` to move the current conversation into a background session. Pass a prompt such as `/bg run the test suite and fix any failures` to give one more instruction first. If Claude is responding when you run `/bg`, the response continues in the background session.

Exiting a session that still has background work running, such as subagents, background shell commands, workflows, or [monitors](/docs/en/tools-reference#monitor-tool), shows a `Background work is running` dialog instead of quitting immediately. {/* min-version: 2.1.198 */}Choose `Move to background and exit` to background the session the same way `/background` does and return to your shell. The option isn't shown when agent view is [turned off](#turn-off-agent-view).

#### Copy the session with /fork

Run `/fork` to copy the current conversation into a new background session while the original keeps running. The copy starts with everything in the conversation up to that point, plus the working directory, model, permission mode, effort level, and any directories or "don't ask again" permission grants you added during the session, and appears as its own row in agent view. From that moment the two sessions are independent: what the copy does never reaches the original conversation. Requires Claude Code v2.1.212 or later; on v2.1.161 through v2.1.211, `/fork` starts a [forked subagent](/docs/en/sub-agents#fork-the-current-conversation) instead, which is now `/subtask`. When [agent view is turned off](#turn-off-agent-view), `/fork` keeps the forked-subagent behavior and `/subtask` isn't available.

Pass a prompt such as `/fork open a draft pull request with the work so far` and the copy starts working on it immediately. Without a prompt the copy waits for its first instruction: select its row in `claude agents` and press `Space` to send one, or run `claude attach <id>`. {/* min-version: 2.1.212 */}The selected row shows `space to send it a prompt` while it waits.

Like any dispatched session, the copy [moves into its own worktree before editing files](#how-file-edits-are-isolated). When the current session is itself running inside a linked [worktree](/docs/en/worktrees) that has a main working tree to return to, the copy runs in that main working tree, so the two sessions don't edit the same checkout. In a bare-repository layout there is no main working tree, so the copy stays where it is and the `/fork` confirmation says it edits the same checkout.

Sessions started with launch flags the copy wouldn't inherit, such as a replaced system prompt or a `--tools` allowlist, can't be forked; Claude Code says so instead of making a partial copy. A session dispatched from agent view forks normally: the copy is launched with the same [agent definition](/docs/en/sub-agents) and appended instructions as the session it came from.

#### What carries over when you background

Backgrounding starts a fresh process that resumes from the saved conversation, and in-flight work moves to it: running background shell commands, backgrounded subagents, dynamic workflows, and scheduled tasks you created with [`/loop`](/docs/en/scheduled-tasks) all carry over and keep running there. A subagent moves together with everything it started, so it carries over only when all of that work can move too. To stop in-flight work instead of carrying it over, set the [`CLAUDE_DISABLE_ADOPT=1`](/docs/en/env-vars#variables) environment variable; Claude Code then asks you to confirm before backgrounding.

Work that can't carry over, such as a running [monitor](/docs/en/tools-reference#monitor-tool), is stopped, and a backgrounded subagent that owns a monitor is stopped along with it. When any such work is running, Claude Code shows a `Background this session?` dialog so you can confirm before it's stopped.

Once in the background, the session can start new subagents, monitors, and background commands, and those keep running across later detach and reattach.

Configuration flags from the original launch carry through to the backgrounded session, so its MCP servers, settings, and fallback model remain in effect:

* `--mcp-config` and `--strict-mcp-config`
* `--settings`
* `--add-dir`
* `--plugin-dir`
* `--fallback-model`
* `--allow-dangerously-skip-permissions`

Directories you added during the session with [`/add-dir`](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) also carry through. Carrying `--allow-dangerously-skip-permissions` keeps `bypassPermissions` reachable in the backgrounded session, but it doesn't grant anything new: the mode still requires the one-time interactive acceptance described in [Permission mode, model, and effort](#permission-mode-model-and-effort).

### From your shell

Pass `--bg` or its long form `--background` to start a session that goes straight to the background:

```bash theme={null}
claude --bg "investigate the flaky SettingsChangeDetector test"
```

The prompt is the positional argument, not a `-p` value. {/* min-version: 2.1.198 */}Claude Code rejects `--bg` combined with `-p` or `--print` before any session is created, because `--print` never starts the interactive session that `claude agents` attaches to.

To run a specific [subagent](/docs/en/sub-agents) you have defined, such as a `code-reviewer`, as the session's main agent, combine `--bg` with `--agent`:

```bash theme={null}
claude --agent code-reviewer --bg "address review comments on PR 1234"
```

If the name doesn't match any of your subagents, the launch fails: Claude Code prints a `no agent named` warning and still reports the session as backgrounded, but the session exits immediately with an `--agent '<name>' not found` error. {/* min-version: 2.1.191 */}Before v2.1.191, Claude Code ran the session with the default agent instead.

Pass `--name` to set the session's display name in agent view instead of the auto-generated one:

```bash theme={null}
claude --bg --name "flaky-test-fix" "investigate the flaky SettingsChangeDetector test"
```

After backgrounding, Claude prints the session's short ID and the commands for managing it. When the service that hosts background sessions isn't already running, `--bg` may first print `Starting background service…` above this output. When you pass `--name`, the name appears after the short ID:

```text theme={null}
backgrounded · 7c5dcf5d · flaky-test-fix
  claude agents             list sessions
  claude attach 7c5dcf5d    open in this terminal
  claude logs 7c5dcf5d      show recent output
  claude stop 7c5dcf5d      stop this session
```

#### Run a shell command

To run a shell command as a background job instead of a Claude session, pass `--exec`. The following example runs `pytest -x` as a background job:

```bash theme={null}
claude --bg --exec 'pytest -x'
```

From agent view, dispatch the same kind of job by typing `!` as the first character of the dispatch input: the `!` shows as a prefix, everything after it is the command, and `Enter` starts the job.

The command runs as a PTY-backed job and appears as a row in agent view, with the most recent line of output as its status. A shell job runs the command in place of Claude, so no model is invoked and the output isn't sent to any session.

To see the output, attach to the row, press `Space` to peek without attaching, or run `claude logs <id>` from your shell. The captured output stays in memory and isn't written to disk. The row and its output clean up automatically about five minutes after the command exits, so read it before then if you need the result.

### How file edits are isolated

Every background session, whether started from agent view, `/bg`, or `claude --bg`, starts in your working directory. Before editing files, Claude moves the session into an isolated [git worktree](/docs/en/worktrees) under `.claude/worktrees/`, so parallel sessions can read the same checkout but each writes to its own.

Claude skips the worktree when:

* The session is already inside a linked git worktree, whether Claude created it under `.claude/worktrees/` or you created it with `git worktree add` somewhere else
* The working directory isn't a git repository and no [`WorktreeCreate` hook](/docs/en/hooks#worktreecreate) is configured
* The write is outside the working directory

To turn off worktree isolation for a repository where git worktrees are impractical, set [`worktree.bgIsolation`](/docs/en/settings#worktree-settings) to `"none"`. Background sessions then edit your working copy directly without moving into a worktree first. Add the setting to the project's `.claude/settings.json`:

```json theme={null}
{
  "worktree": {
    "bgIsolation": "none"
  }
}
```

Outside a git repository, sessions write to the working directory directly and aren't isolated from each other, so avoid dispatching parallel sessions that edit the same files. If you use a different version control system, configure a [`WorktreeCreate` hook](/docs/en/worktrees#non-git-version-control) and Claude isolates edits the same way it does for git.

When the hook fails in a directory that isn't a git repository, the session skips isolation for that directory and edits the working directory in place. Inside a git repository, writes stay blocked until the session isolates.

Deleting a session removes or keeps the worktree Claude created for it, depending on how you delete it and what the worktree holds:

* Deleting in agent view with `Ctrl+X` twice removes the worktree, including any uncommitted changes, so commit the changes you want to keep first.
* Deleting from the shell with [`claude rm`](#manage-sessions-from-the-shell) keeps a worktree that has uncommitted changes, along with its session row.
* Neither path removes a worktree with commits that aren't pushed anywhere: the worktree is [kept together with its session](#organize-the-list) and the output names the kept path and the reason.
* A worktree you created yourself and started the session inside is left in place either way.

To find a session's worktree path, peek the session or attach and check its working directory.

A [subagent](/docs/en/sub-agents) the background session spawns inherits the session's working directory, so its file edits land in the session's worktree rather than your working copy. To give a subagent its own separate worktree instead, set [`isolation: worktree`](/docs/en/sub-agents#supported-frontmatter-fields) in its frontmatter or pass `isolation: "worktree"` when spawning it.

A background session that isolated its code changes in a worktree also commits, pushes its own branch, and opens a draft pull request without stopping to ask. The [`#N` label](#pull-request-status) appears on its row when the pull request opens. It never pushes to `main` or `master`, never force-pushes or merges, and it skips the pull request when you told it not to open one or the repository has no remote.

A session editing a checkout it didn't isolate itself still asks before committing or switching branches. This applies when isolation is set to `"none"`, when the worktree move failed, or when the session started inside a worktree that already existed.

### Set the model

The model name shown in the agent view header is the dispatch default. New sessions you start from the input use this model, which comes from the [`model` setting](/docs/en/settings#available-settings) in your user settings. Set it by selecting a model in the [`/model` picker](/docs/en/model-config), or edit the setting directly.

To override the dispatch default for the whole agent view session, pass `--model` when opening agent view. See [Permission mode, model, and effort](#permission-mode-model-and-effort).

To change the dispatch default from inside agent view, type `/model` followed by a model name in the dispatch input and press `Enter`. The header updates to show that model with a `(session)` marker, and sessions you dispatch afterward use it. Type `/model default` to clear the override and return to the dispatch default. This override lasts for the rest of the current `claude agents` run and doesn't write to your settings file. The following example dispatches one session on Opus and the next on Sonnet:

```text theme={null}
/model opus
refactor auth
/model sonnet
run the test suite
```

Each background session can run on a different model. To override it for one session:

* From the shell, pass `--model` with `claude --bg`.
* Attach to a running session and run `/model` to switch: a pick from the picker, or a typed `/model <name>`, saves as your default for new sessions unless you press `s` in the picker for a session-only switch. A session-only switch persists if the session is respawned.
* Dispatch a [subagent](/docs/en/sub-agents) whose frontmatter sets a `model` field.

### Permission mode, model, and effort

A background session reads its [settings](/docs/en/settings) from the directory it runs in, the same as if you had started `claude` there. This includes [`env` values](/docs/en/settings#available-settings) in project settings, so an `ANTHROPIC_MODEL` or provider variable set there applies to background sessions in that directory.

Cloud provider selection, such as `CLAUDE_CODE_USE_BEDROCK` or `CLAUDE_CODE_USE_VERTEX`, and `ANTHROPIC_DEFAULT_*_MODEL` aliases follow the shell that dispatched the session. {/* min-version: 2.1.206 */}If you export a [`CLAUDE_CODE_EXTRA_BODY`](/docs/en/env-vars) request-body override in that shell, it reaches the session the same way. A gateway `ANTHROPIC_BASE_URL` exported in that shell can reach the session too; see [the supervisor process](#the-supervisor-process) for the conditions and for how background sessions source provider settings and credentials.

The [permission mode](/docs/en/permissions) depends on how you started the session. Backgrounding an existing session with `/bg` or `←` keeps the current permission mode, so a session you switched to `acceptEdits` or `auto` stays in that mode after detaching. Dispatching from the agent view input or running `claude --bg` from your shell uses the `defaultMode` from that directory's settings, or the `permissionMode` from the dispatched [subagent's frontmatter](/docs/en/sub-agents#supported-frontmatter-fields).

The permission mode, model, and effort you chose for a background session, along with the [configuration flags it carries](#what-carries-over-when-you-background), all persist when the supervisor later [stops and restarts](#the-supervisor-process) its process. A session you launched with `claude --bg --dangerously-skip-permissions` or `claude --bg --permission-mode bypassPermissions` stays in `bypassPermissions` after that restart instead of falling back to the directory's `defaultMode`, and a model or effort you changed mid-session with `/model` or `/effort` is kept.

An effort the session took from the [`effortLevel` setting](/docs/en/settings#available-settings) rather than from `--effort` or `/effort` isn't fixed at dispatch: each process started for the session reads the setting again, so editing `effortLevel` in `settings.json` reaches sessions you background with `←` or `/bg` and their later restarts.

A name you set with [`/rename`](/docs/en/commands) or `Ctrl+R` also persists across that restart, so [`claude --resume <name>`](/docs/en/sessions#name-your-sessions) still resolves the session.

To set defaults for every session you dispatch from agent view, pass any of `--permission-mode`, `--model`, `--effort`, or `--agent` when opening it:

```bash theme={null}
claude agents --permission-mode plan --model opus --effort high
```

`--effort` here accepts the same values as the [top-level `--effort` flag](/docs/en/cli-reference#cli-flags), including `ultracode`.

`--agent` sets the [subagent](/docs/en/sub-agents) used when a dispatch prompt doesn't name one, either with `@name` or as the first word. It defaults to the [`agent` setting](/docs/en/settings#available-settings) if one is set, otherwise the built-in catch-all `claude` agent. Naming a subagent in the dispatch input overrides both.

`claude agents` also accepts `--dangerously-skip-permissions` as shorthand for `--permission-mode bypassPermissions`, and `--allow-dangerously-skip-permissions` to make `bypassPermissions` available in each dispatched session's `Shift+Tab` cycle without starting in that mode. Both match the [top-level CLI flags](/docs/en/cli-reference).

The active defaults appear in the footer below the dispatch input.

Using `bypassPermissions` with `claude --bg --permission-mode` is refused until you have accepted the bypass disclaimer by running `claude --dangerously-skip-permissions` once interactively, since that mode lets a session you aren't watching act without approval. Passing `--dangerously-skip-permissions` or `--permission-mode bypassPermissions` to `claude agents` shows the same disclaimer when you haven't accepted it before, and accepting applies `bypassPermissions` to the sessions you launch from the view. Passing `--allow-dangerously-skip-permissions` shows the same disclaimer too, and accepting makes `bypassPermissions` available in the `Shift+Tab` cycle of those sessions without starting them in it.

### Settings, plugins, and MCP servers

Agent view accepts the same configuration flags as `claude` for loading settings, plugins, MCP servers, and additional directories. Each flag applies to agent view itself and is passed through to every session you dispatch from it, so a plugin or MCP server you load this way is available in those sessions too.

| Flag                                                                                             | Effect                                                                         |
| :----------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------- |
| [`--settings <file-or-json>`](/docs/en/settings)                                                      | Override settings for agent view and dispatched sessions                       |
| [`--add-dir <path>`](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) | Grant file access to an additional directory                                   |
| [`--plugin-dir <path>`](/docs/en/plugins)                                                             | Load a plugin from a local directory                                           |
| [`--mcp-config <file-or-json>`](/docs/en/mcp)                                                         | Load MCP servers from a config file or JSON string                             |
| `--strict-mcp-config`                                                                            | Use only the MCP servers from `--mcp-config`, ignoring other MCP configuration |

Repeat `--add-dir`, `--plugin-dir`, or `--mcp-config` once per value. The space-separated form, such as `--add-dir a b c`, isn't supported with `claude agents`.

The following example opens agent view with a settings override and one extra directory:

```bash theme={null}
claude agents --settings ./ci-settings.json --add-dir ../shared-lib
```

`--settings` accepts a file path or an inline JSON string. A file path must point to an existing file; Claude Code exits with a `Settings file not found` error if it doesn't.

## Manage sessions from the shell

Every background session has a short ID you can use from the shell. The ID is printed when you start a session with `claude --bg`, and each session's ID is its directory name under `~/.claude/jobs/`. These commands are useful for scripting or when you don't want to open agent view.

| Command                      | Purpose                                                                                                                                                                                                                                                                             |
| :--------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `claude agents`              | Open agent view                                                                                                                                                                                                                                                                     |
| `claude agents --cwd <path>` | Open agent view scoped to sessions started under `<path>`                                                                                                                                                                                                                           |
| `claude agents --json`       | Print sessions as a JSON array and exit. See [List sessions as JSON](#list-sessions-as-json)                                                                                                                                                                                        |
| `claude attach <id>`         | Attach to a session in this terminal                                                                                                                                                                                                                                                |
| `claude logs <id>`           | Print the session's recent output                                                                                                                                                                                                                                                   |
| `claude stop <id>`           | Stop a session. Also accepts `claude kill`                                                                                                                                                                                                                                          |
| `claude respawn <id>`        | Restart a session, running or stopped, with its conversation intact, e.g. to pick up an updated Claude Code binary                                                                                                                                                                  |
| `claude respawn --all`       | Restart every running session, e.g. to move all sessions onto an updated Claude Code binary at once                                                                                                                                                                                 |
| `claude rm <id>`             | Remove a session from the list, along with a worktree Claude created for it when that's safe to delete; see [how deleting handles worktrees](#how-file-edits-are-isolated). The conversation transcript stays on your local machine and remains available through `claude --resume` |
| `claude daemon status`       | Print the [supervisor's](#the-supervisor-process) state, version, socket directory, and worker count                                                                                                                                                                                |
| `claude daemon stop --any`   | Stop the supervisor process and the background sessions it hosts. Pass `--keep-workers` to leave background sessions running so the next supervisor reconnects to them. The next `claude agents` or `claude --bg` starts a fresh supervisor                                         |

### List sessions as JSON

`claude agents --json` prints active sessions as a JSON array and exits: every live session, plus background sessions that are still working or blocked even when their process has exited. Add `--all` to also include completed background sessions, and `--cwd <path>` to limit the list to sessions started under that directory.

Each entry describes one session:

| Field                      | Present                    | Description                                                                                                                                                                                                                                   |
| :------------------------- | :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cwd`, `kind`, `startedAt` | Always                     | The working directory, `interactive` or `background`, and the start time in Unix milliseconds                                                                                                                                                 |
| `id`                       | Background sessions        | Short ID, usable with `claude attach`, `claude logs`, and `claude stop`                                                                                                                                                                       |
| `state`                    | Background sessions        | One of `working`, `blocked`, `done`, `failed`, or `stopped`                                                                                                                                                                                   |
| `pid`, `status`            | While the process is alive | Process ID and current status                                                                                                                                                                                                                 |
| `waitingFor`               | When `status` is `waiting` | What the session is blocked on: {/* min-version: 2.1.212 */}`permission prompt` for an approval, `input needed` for a question from Claude or an MCP server's input request, `sandbox request`, `worker request`, or `dialog open`            |
| `sessionId`, `name`        | When set                   | `sessionId` is the full session UUID, usable with [`claude --resume`](/docs/en/sessions). An interactive session you never named carries a default `name` built from its working directory's name plus a two-character suffix, such as `my-app-3f` |

## How background sessions are hosted

Every session listed in agent view is considered a background session, whether or not you're currently attached to it. By contrast, a session started by running `claude` directly is tied to that terminal and ends when it closes, unless you [send it to the background](#from-inside-a-session).

### The supervisor process

Background sessions are hosted by a per-user supervisor process, separate from your terminal and from agent view. The supervisor starts automatically the first time you background a session or open agent view, and you don't manage it directly.

When an update has replaced or removed the binary a running Claude Code process was launched from, that process starts the supervisor from another installed copy, such as the installed `claude` launcher or the newest version on disk.

The supervisor keeps one pre-warmed worker process ready so a dispatch from agent view or `claude --bg` starts without the delay of a cold launch. When you dispatch, the supervisor assigns the pre-warmed worker to your session, applies that session's directory, settings, and credentials to it, and then starts a replacement for the next dispatch. If no healthy pre-warmed worker is available, the supervisor launches a fresh process instead.

The supervisor and its sessions authenticate with the same stored credentials as your interactive sessions and make no additional network connections beyond the model API. Provider selection variables such as `CLAUDE_CODE_USE_BEDROCK` and `ANTHROPIC_DEFAULT_*_MODEL` aliases are read from the shell that dispatched each session and are applied to its worker.

The dispatching shell's `PATH` is applied to the worker the same way, so shell commands the session runs find the same tools your terminal does.

A background session doesn't inherit gateway endpoint variables such as `ANTHROPIC_BASE_URL` or the equivalent Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry base URL variables from the shell that started the supervisor. Without a gateway exported in the shell you dispatch from, the session uses your stored credentials and any `env` values in the project directory's [settings](/docs/en/settings). To point every session in a project at an [LLM gateway](/docs/en/llm-gateway), set `ANTHROPIC_BASE_URL` in that project's `.claude/settings.json` `env` block.

{/* min-version: 2.1.203 */}If you export a gateway `ANTHROPIC_BASE_URL` in the shell you dispatch from, it reaches that session's worker, along with `ANTHROPIC_CUSTOM_HEADERS` and the credential exported alongside them, when both conditions hold:

* The supervisor was started from an environment with the same gateway. The supervisor captures its environment from the first shell that opens agent view or dispatches a background session, so starting from the gateway shell gives it that environment.
* The session is dispatched into the directory you're dispatching from, or is your own session backgrounded with `←` or `/background`. Dispatching into a different directory with `@repo` or `--cwd` doesn't carry the shell's gateway; that project's `settings.json` `env` block supplies the endpoint instead.

When the supervisor's environment carries a different gateway or none, the worker keeps your stored credentials against the default endpoint instead of mixing one environment's credential with another's endpoint. The forwarded endpoint applies only to that live process and is never written to disk.

When the supervisor stops an idle session and you later wake it by attaching, peeking, or replying, your environment's gateway is forwarded again under the same conditions as a fresh dispatch. Waking a session from a shell without the gateway restarts it against your settings and stored credentials instead.

Each background session is its own Claude Code process, managed by the supervisor rather than tied to your terminal. A session that's actively working, waiting for your input, or has a terminal attached keeps its process running. A running background shell command, subagent, dynamic workflow, or monitor counts as active work, so a long-running process such as a dev server keeps the session alive.

Once a session finishes and sits unattached for about an hour, the supervisor stops its process to free resources. A session you have [pinned](#organize-the-list) with `Ctrl+T` is exempt and keeps its process running while idle. The transcript and state stay on disk either way, and the next time you attach, peek, or reply to a stopped session, the supervisor starts a fresh process from where it left off. When every session has finished and no terminal is connected, the supervisor itself exits and starts again the next time you need it.

The supervisor also restarts a session whose process exits unexpectedly, with three safeguards so a restart never overrides a stop or acts on stale input:

* A session whose state on disk already shows it as done, failed, or stopped isn't restarted, unless a reply you sent is still waiting to be delivered.
* Ending the process of a session you backgrounded with `←` or [`/background`](#from-inside-a-session) yourself, for example with `kill`, marks the session stopped instead of restarting it. A session dispatched with a task, from the agent view input or `claude --bg`, is still restarted so the dispatched work completes.
* A session the supervisor restarts is told it was restarted and that you haven't sent a new message since, so it can re-verify time-sensitive context such as branch state before continuing. A restarted `←` or `/background` session also doesn't resume an interrupted response older than about an hour; it waits for your next message instead.

Background work the session itself started at the top level is handed off when its process is stopped, restarted, or updated, including on Windows. The next process started for that session picks the work back up:

* A background shell command that finished in the meantime is reported as completed with its output
* A dynamic workflow resumes from where it left off
* {/* min-version: 2.1.198 */}A [background subagent](/docs/en/sub-agents#run-subagents-in-foreground-or-background) resumes from its own transcript

Work whose state lives only inside the process itself stops with it instead of being handed off. That's shell commands a subagent started, which the resumed subagent can start again, and running [monitors](/docs/en/tools-reference#monitor-tool), whose event stream can't be moved to another process.

Deleting the session stops everything it handed off. To stop all of the session's background work with the process instead of handing it off, set the [`CLAUDE_CODE_DISABLE_BG_EXIT_HANDOFF`](/docs/en/env-vars#variables) environment variable to `1`.

A restarted process finds the conversation of a session that [moved into a worktree](#how-file-edits-are-isolated) mid-task: when the transcript isn't where the session started, Claude Code also looks under the repository's registered worktrees. {/* min-version: 2.1.212 */}When neither the session's own directory nor those worktrees has the transcript, Claude Code scans all your saved session transcripts as a last resort and resumes from the one that matches the session.

If a restarted session comes back showing only its original prompt because Claude Code misread its transcript as empty, the conversation transcript is renamed with an `.orphaned-` suffix instead of deleted, so it stays on your machine.

An empty row left over from pressing `←` that was never given a prompt is removed entirely after about five minutes so the list clears on its own. Sessions started with `claude --bg` and sessions waiting on a setup prompt such as a trust dialog aren't removed this way.

When the host runs low on memory, the supervisor stops idle non-pinned sessions first and stops idle pinned ones only if that freed nothing.

The supervisor watches the installed Claude Code binary on disk and restarts into the new version after the regular [auto-updater](/docs/en/setup#auto-updates) replaces it. This is a local file watch, not a network check. Background sessions are detached processes, so they keep running through the restart and the new supervisor reconnects to them. An idle pinned session is also restarted in place onto the new version so it picks up the update without you reattaching.

Once the new supervisor takes over, it also restarts the remaining idle sessions onto the new version, a few at a time in the background, after a short delay that lets terminals attached across the restart reconnect first. A session that is working, waiting on your input, or has a terminal attached isn't interrupted; it moves to the new version the next time its process restarts.

These restarts only ever move a session onto a newer version. A supervisor running an older Claude Code version than the one a session's process was started with leaves that process alone; the session keeps running the newer version until a newer supervisor takes over.

Running `claude attach` while the supervisor is restarting a session, whether for an update, a stall, or a migration, waits for the replacement process instead of failing. A status line such as `Agent is updating to the new Claude Code…` names what it's waiting for and counts the elapsed seconds, and the command connects as soon as the session is ready. After about 60 seconds it stops waiting and reports an error.

`claude attach` also waits while the background service itself is starting or reconnecting, and a session that finished during that wait is reported as exited rather than as an error. A terminal resize you make during a slow attach is applied when the attach completes.

### Where state is stored

Session state is stored under your Claude Code config directory. If you set [`CLAUDE_CONFIG_DIR`](/docs/en/env-vars), the supervisor uses that directory instead of `~/.claude` and runs as a separate instance with its own sessions.

| Path                             | Contents                                                                                                    |
| :------------------------------- | :---------------------------------------------------------------------------------------------------------- |
| `~/.claude/daemon.log`           | Supervisor log                                                                                              |
| `~/.claude/daemon/roster.json`   | List of running background sessions, used to reconnect after a restart                                      |
| `~/.claude/jobs/<id>/state.json` | Per-session state shown in agent view                                                                       |
| `~/.claude/jobs/<id>/tmp/`       | Per-session scratch directory. Writes here don't prompt for permission. Removed when the session is deleted |

Each background session has the `CLAUDE_JOB_DIR` environment variable set to its `~/.claude/jobs/<id>` directory, so shell commands the session runs can write temporary files to `$CLAUDE_JOB_DIR/tmp` without colliding with parallel sessions.

To inspect this state without reading the files directly, run `claude daemon status`. It reports whether the supervisor is reachable, its process ID and version, the socket directory, and how many background sessions are live.

The command also warns when the running supervisor is on a different version than the `claude` you invoked, which happens after an update the supervisor hasn't restarted into yet. The warning shows both versions and tells you to run `claude daemon stop --any` to pick up the new version. When Claude Code is installed as an OS service, the suggested command is `claude daemon stop` without the flag.

Sessions survive that version mismatch intact: an older Claude Code version that updates a session's `state.json` preserves fields it doesn't recognize and keeps the session listed. {/* min-version: 2.1.200 */}The session list in `roster.json` follows the same rule, so sessions started by the newer version stay reachable and keep accepting input after the supervisor restarts.

On Windows, `claude daemon status` surfaces the underlying file error when the daemon's pipe-key file is locked or unreadable instead of reporting a generic connection failure.

### Turn off agent view

To turn off background agents and agent view entirely, set the `disableAgentView` [setting](/docs/en/settings) to `true` or set the `CLAUDE_CODE_DISABLE_AGENT_VIEW` environment variable. Administrators can enforce this through [managed settings](/docs/en/permissions#managed-settings).

## Troubleshooting

### `claude agents` lists subagents instead of opening agent view

If `claude agents` prints a count followed by your configured subagents and then exits, agent view is unavailable in your environment. Run `claude update` to install the latest version.

If agent view still doesn't open after updating, check whether it has been [turned off](#turn-off-agent-view) by a setting or environment variable.

### Agent view opens with no sessions

Before you dispatch your first session, agent view shows the empty section headers with a description under each, plus a one-line explanation above the input, in place of the session list. Type a prompt in the input at the bottom and press `Enter` to dispatch your first session.

### Backgrounding shows a `Background this session?` dialog

If pressing `←` to background the current session shows a `Background this session?` dialog, the session has in-flight work that can't move to the background session, such as a running [monitor](/docs/en/tools-reference#monitor-tool), and Claude Code won't silently stop it. The dialog names the work that will be stopped and, separately, counts the tasks that carry over. Run `/tasks` to see everything that's running, then confirm to background anyway or choose `Stay` to let the work finish first. See [What carries over when you background](#what-carries-over-when-you-background) for which task kinds carry over and which are stopped.

### Prompt rejected as too short

The dispatch input expects a task description, not a conversational opener. A prompt shorter than four characters is rejected with a `Too short` hint so a stray keystroke doesn't start a session. Describe what you want the session to do, such as `investigate the flaky checkout test`.

### Sessions show as failed after shutdown

Shutting down or restarting your machine stops running background sessions, so they show as failed when you next open agent view. Attach, peek, or reply to any of them and the session restarts from where it left off.

Sleep alone doesn't cause this. Sessions are preserved across sleep and the supervisor reconnects to them on wake.

### Opening a session says the conversation is already open

Opening a stopped row whose conversation is also held open by another running non-interactive Claude Code process, for example a background worker for the same conversation that is still winding down, shows `This conversation is already open in another running Claude session` instead of starting the row's process, because two processes can't write to the same transcript. Reply in the session that already has the conversation open, or exit it and open the row again. A reply you typed with the refused attempt isn't lost; it's sent the next time the session starts.

### Opening a session says it has no saved transcript

A stopped session that was [backgrounded from another conversation](#from-inside-a-session) and stopped before its first response finished has nothing to resume: until that first response finishes, the conversation still lives only in the session it was backgrounded from. `claude attach` refuses to open it with `This session has no saved transcript`.

In agent view, opening that row shows `Press enter again to restart this session fresh` below the list. Press `Enter` on the same row again to restart the session with an empty conversation, or run `claude respawn <id>` from the shell.

The original conversation is intact; resume it with `claude --resume` or keep working in it. See the [error reference](/docs/en/errors#this-session-has-no-saved-transcript) for details.

### A session fails before starting with a `possibly low memory` note

When a background session's process exits before it finishes starting and the host is low on memory, the row's status names the exit and adds `possibly low memory — free some up and retry`.

The note is a hypothesis, not a confirmed cause. Claude Code adds it only when the process exited silently, without writing an error and without being stopped by a signal, and the host reported low memory at that moment. When the process did write an error before exiting, the row shows that error instead.

Free up memory on the machine, then attach, peek, or reply to the row and the supervisor starts a fresh process for the session. When memory stays low, the supervisor also [stops idle sessions](#the-supervisor-process) to free resources on its own.

### Agent view says the background service did not respond

If attaching, peeking, or `claude logs` reports that the background service did not respond, the supervisor process has likely stalled. Stop it and let the next `claude agents` start a fresh one. To keep your background sessions running through the restart, pass `--keep-workers`:

```bash theme={null}
claude daemon stop --any --keep-workers
```

The new supervisor reconnects to the running sessions. Without `--keep-workers`, the command ends the background sessions too. The `--any` flag confirms you want to stop a supervisor that started on demand rather than as an installed service, which is the default.

A supervisor that starts but can't accept connections exits and releases its lock on its own, so the next `claude agents` starts a fresh one without this manual stop. The steps above apply when a running supervisor stalls.

On Windows, if the supervisor doesn't respond to the stop request, the command prints its process ID. End that process with `taskkill /PID <pid>` to finish the recovery. Background sessions are still preserved when you passed `--keep-workers`.

### Dispatch fails with `Could not resolve authentication method`

If a background dispatch fails with `Could not resolve authentication method` while interactive sessions authenticate normally, the worker that received the dispatch didn't pick up credentials. The supervisor supplies a fresh credential snapshot when it assigns a [pre-warmed worker](#the-supervisor-process), so this error means no stored credential was available to the supervisor process itself. Confirm you have run `/login` or configured an API key, then stop the supervisor:

```bash theme={null}
claude daemon stop --any --keep-workers
```

The next `claude agents` or `claude --bg` starts a fresh supervisor that reads your stored credentials. If you authenticate with an environment variable such as `ANTHROPIC_API_KEY` rather than `/login`, run that next command from a shell where the variable is set.

See the [error reference](/docs/en/errors#could-not-resolve-authentication-method) for the full list of causes and fixes.

### Background sessions can't read Desktop, Documents, or Downloads on macOS

On macOS, the background session host runs as its own process and requests access to protected folders separately from your terminal. If a background session reports `Operation not permitted` when reading `~/Desktop`, `~/Documents`, `~/Downloads`, or another protected location, grant access in System Settings under Privacy & Security > Files and Folders, or enable Full Disk Access for the entry.

With the native installer, the entry appears as Claude Code and the grant persists across updates. With other install methods such as Homebrew or npm, the entry shows the binary path and may need to be granted again after updating.

### Background sessions can't reach local-network hosts on macOS

On macOS 15 and later, the system blocks a process from reaching devices on your local network until you grant Local Network permission, so a command targeting a LAN address can fail with `connect: no route to host` in a background session even though it works in a foreground terminal. {/* min-version: 2.1.198 */}The first command in a background session that connects to a local-network address triggers the macOS Local Network permission prompt for Claude Code. Grant it once and those commands reach LAN hosts the same way they do in a foreground terminal.

### A session is slow to respond after attaching

Once a session has finished and sat unattached for about an hour, the supervisor stops its process to free resources. Attaching starts a fresh process from where it left off and switches to the session immediately while the process restarts. Sessions that are working, waiting on you, or [pinned](#organize-the-list) aren't stopped this way, so pin a session with `Ctrl+T` to keep it responsive.

While the process starts, Claude Code shows the tail of the session's transcript formatted the way the live session renders it, with markdown, highlighted code blocks, and tool calls as dimmed rows, above a dimmed prompt area with a `Session is starting` note. The live session replaces it as soon as it's ready.

### `.claude/worktrees/` is filling up

Deleting a session in agent view removes the worktree Claude created for it, and a worktree that can't be removed safely [keeps its session row](#organize-the-list) so it isn't orphaned. {/* min-version: 2.1.211 */}A worktree directory that git no longer recognizes is left on disk when its session is deleted, so remove leftover directories you don't need by hand.

`claude rm` keeps a worktree that has uncommitted changes, and its session row, and prints the kept path.

List leftover entries with `git worktree list` in the project directory and remove each with `git worktree remove <path>`. See [Clean up worktrees](/docs/en/worktrees#clean-up-worktrees).

## Limitations

Agent view is in research preview with the following limitations:

* **Rate limits apply**: background sessions consume your subscription usage the same as interactive sessions, so running ten agents in parallel uses quota roughly ten times as fast as running one.
* **Sessions are local**: background sessions run on your machine. They are preserved across sleep but stop if the machine shuts down.
* **Claude-created worktrees are deleted with the session in agent view**: commit changes before deleting a session that edited files in its own worktree. A worktree with commits that aren't pushed anywhere is kept along with the session. `claude rm` also keeps a worktree that has uncommitted changes together with its session, and a worktree you created yourself is left in place.

## Related resources

For other ways to run Claude in parallel, see:

* [Run agents in parallel](/docs/en/agents): compare agent view with subagents, agent teams, and worktrees
* [Agent teams](/docs/en/agent-teams): coordinate multiple sessions that message each other
* [Claude Code on the web](/docs/en/claude-code-on-the-web): run sessions in a managed cloud environment instead of locally

## Version history

Agent view has evolved quickly during research preview. If you are on an older Claude Code version, some behavior on this page may differ; in particular, `claude agents` rejects flags it doesn't yet support with an `unknown option` error. The table below lists when each flag and behavior was added.

| Version  | Change                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| v2.1.218 | {/* min-version: 2.1.218 */}Pressing `←` within two seconds of a deletion that emptied the prompt, or of moving through prompt history, shows `Press ← again to open agents`, or `Press ← again to go back to agents` in an attached session, and switches only on a second press at least a second later; before this release the press switched immediately. A `←` that arrives inside pasted or scripted input no longer triggers the switch. Backgrounding a foreground session with `←` shows `Your conversation moved to the background` above the list, and `Esc` at the root of agent view returns to that conversation instead of exiting to the shell, with double `Ctrl+C` remaining the exit; if the conversation can't be reopened, Claude Code exits and prints a `claude --resume` command for it. On Windows, a `←` pressed within about half a second of attaching shows `Ambiguous ←, press again to detach` and detaches on the second press.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| v2.1.216 | {/* min-version: 2.1.216 */}A background session where `/install-github-app`, the [`/mcp`](/docs/en/mcp) settings list, or an MCP authentication action needs a terminal appears under `Needs input` with a row such as `open this session to manage MCP servers` until you attach; run the command again to continue. From v2.1.208 through v2.1.215 the command was refused with a message and no `Needs input` row.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| v2.1.213 | {/* min-version: 2.1.213 */}`/install-github-app`, the [`/mcp`](/docs/en/mcp) settings list, and MCP authentication actions work in a background session while a terminal is attached, and are refused only when nobody is attached, with a message telling you to attach and run the command again; from v2.1.208 through v2.1.212 they were refused even with a terminal attached.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| v2.1.212 | {/* min-version: 2.1.212 */}[`/fork` in an interactive session](#from-inside-a-session) copies the conversation into a new background session that appears as its own row, named after the session it came from or, for a prompted fork of an unnamed session, after the fork prompt, while the original keeps running; the earlier forked-subagent behavior of `/fork` moved to `/subtask`. With [agent view turned off](#turn-off-agent-view), `/fork` keeps the forked-subagent behavior. A focused row that is waiting for its first prompt shows `space to send it a prompt`. `Ctrl+J` inserts a newline in the dispatch input on terminals with extended key reporting, where the keypress was previously ignored, and the `?` overlay lists the shortcut. The `←` footer hint in an interactive session briefly shows `N done` when a background session finishes while none need your input. Typing a bare `/resume` in agent view opens a picker of past sessions of the repository you opened agent view from, including sessions deleted from the list, and picking one resumes it as a background session; before this release `/resume` wasn't available in agent view and deleted sessions were reachable only with `claude --resume` or `/resume` from an interactive session. Targeted, scoped, and restricted forms keep the `attach to a session to run it` hint that earlier versions showed for every form. Sessions waiting on a sandbox network-host prompt, an MCP input request, or a managed-settings prompt show as `Needs input` instead of `Working`, in agent view and in `claude agents --json`, and a question from Claude reports `waitingFor: input needed` instead of `permission prompt`. Attaching to a session whose process has stopped shows its transcript formatted the way the live session renders it, instead of as raw text. A stopped session whose transcript is in an unexpected place resumes from it via a last-resort scan of your saved transcripts, and opening a row that has no saved transcript shows `Press enter again to restart this session fresh`, restarting it fresh on the second press; v2.1.211 showed the refusal with no way to restart from agent view. |
| v2.1.211 | {/* min-version: 2.1.211 */}Waking a stopped session by attaching, peeking, or replying from the directory it runs in forwards your shell's gateway `ANTHROPIC_BASE_URL` again, under the same conditions as a fresh dispatch, so a session authenticated through a gateway `ANTHROPIC_AUTH_TOKEN` resumes on the gateway instead of reporting `Not logged in`. Attaching to a stopped session that was backgrounded from another conversation before its first response finished is refused with `This session has no saved transcript` instead of silently starting a blank conversation under the same session id; opening the same row from agent view showed the refusal in the footer. Ending the process of a `←` or `/background` session from outside Claude Code marks it stopped instead of the supervisor restarting it, a stop already recorded on disk is honored unless a reply you sent is still waiting to be delivered, a session restarted after a crash is told it was restarted, and a restarted `←` or `/background` session doesn't resume an interrupted response older than about an hour. A session-naming reply that answers or refuses the prompt instead of labeling it, such as for a prompt that's mostly a link, is discarded and the row keeps a name taken from the prompt text. Deleting a session whose worktree git no longer recognizes succeeds, leaving the worktree directory on disk and naming its path, instead of every attempt being refused. A refused delete shows the reason on the session's row, including the underlying git error when the worktree couldn't be removed, instead of the row silently reappearing.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| v2.1.210 | {/* min-version: 2.1.210 */}`claude attach` waits while the background service is starting or reconnecting instead of failing with a `job not found` or `still starting` error, reports a session that finished during the attach as exited, and applies a terminal resize made during a slow attach when the attach completes. The prompt footer's `←` needs-input count appears on every provider, including third-party providers that previously showed the plain `← for agents` form. Backgrounding a session with `←` carries Claude's task list to the background session instead of dropping it. The row you pressed `←` from keeps a bold, undimmed name after the selection moves. `claude agents --effort` accepts `ultracode` instead of silently dropping it.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| v2.1.208 | {/* min-version: 2.1.208 */}Attaching to a session whose process has stopped shows the last screenful of its transcript while the process starts, instead of only a `Session is starting` note. A reply that can't be delivered because the background service is unreachable or the send fails is saved and sent as the session's next prompt when its process starts again; before this release, a reply lost while the background service was unreachable was discarded. A process whose own binary was replaced by an update can still start the supervisor, from the installed `claude` launcher or the newest version on disk, instead of failing until Claude Code was restarted. A supervisor running an older version never restarts an idle session started by a newer version onto its own older binary. Deleting a session removes its worktree even after the session moved the worktree onto a different branch, and keeps the worktree together with the session row when the worktree has commits that aren't pushed anywhere or another session claims it, instead of destroying the commits or orphaning the worktree. `/install-github-app` and the `/mcp` settings list and its authentication actions are refused in a background session with a message naming the alternative; in v2.1.208 only, the `/model` picker was refused the same way and a typed `/model <name>` switched that session only instead of also saving your default model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| v2.1.207 | {/* min-version: 2.1.207 */}The peek panel opens with the sentence the row truncates, such as the exact question for a session that's waiting on you, and shows how long a blocked session has been waiting as a single `waiting 3m` line instead of prefixing the same timestamp to the status sentence and the question. Pasting the same text again in the dispatch input expands the collapsed `[Pasted text #N]` placeholder instead of adding a second one. A background session named by accepting a plan shows that name on its row. A background session that moved into a worktree keeps its conversation when its process is restarted from agent view.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| v2.1.206 | {/* min-version: 2.1.206 */}Row summaries fill the row's remaining width and truncate only at the terminal's right edge instead of at 64 columns. After the supervisor restarts into a new Claude Code version, it restarts the remaining idle background sessions onto that version in the background instead of a few per minute. Deleting a session with `Ctrl+X` or `claude rm` also clears it from the supervisor's session list, so the row no longer reappears after a supervisor restart. A `CLAUDE_CODE_EXTRA_BODY` request-body override exported in the dispatching shell reaches background sessions instead of being ignored.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| v2.1.205 | {/* min-version: 2.1.205 */}The prompt footer's `←` hint in a regular `claude` session counts the background agents waiting on you, such as `← 2 agents`. Row summaries show the session's own one-line report, truncated at 64 columns, instead of a raw tool invocation or a `done/total` count; directory-grouped rows open with a colored state word. The peek panel opens with the full status sentence and, for a session waiting on you, its exact question above the reply input. Sessions that edit, comment on, close, or mark a pull request ready with `gh` are linked to it, not only ones that create or check out a pull request, a push links a pull request even when the local branch name doesn't match, and a pull request whose creating command's output exceeded the inline limit is linked too. A turn with no readable text keeps the session's previous state instead of flipping it back to `Working`. `claude attach` waits up to about 60 seconds for a session that's restarting, with a status line naming why, instead of failing.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| v2.1.203 | {/* min-version: 2.1.203 */}A gateway `ANTHROPIC_BASE_URL` exported in the dispatching shell reaches the sessions dispatched from it into that same directory when the supervisor shares that gateway environment, instead of being dropped while the API key exported alongside it was kept. The dispatching shell's `PATH` is applied to each session's worker. Pressing `←` while subagents are running waits for them instead of restarting them after ten seconds. The empty list always shows the section headers with a description under each. Typing `@` in the dispatch input also lists the launch repository's registered git worktrees that live inside its directory tree. An effort inherited from the `effortLevel` setting follows later edits to that setting instead of being fixed at dispatch. Opening a stopped session whose conversation is already open in another running session is refused with a message instead of failing the row. A command that isn't available in agent view leaves the typed text in the input. A `WorktreeCreate` hook that fails outside a git repository no longer blocks the session from editing files.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| v2.1.202 | {/* min-version: 2.1.202 */}A name set with `/rename` or `Ctrl+R` on a background session persists when the supervisor stops and restarts its process, instead of reverting to the name the session was dispatched with.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| v2.1.200 | {/* min-version: 2.1.200 */}An older Claude Code version that rewrites the session list in `roster.json` preserves fields written by a newer version, matching the existing `state.json` guarantee, so sessions started by the newer version keep accepting input after the supervisor restarts. When you open a session that has stopped responding, the supervisor restarts its process and the session continues the interrupted response from where it left off.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| v2.1.199 | {/* min-version: 2.1.199 */}A background session whose process exits before it finishes starting on a low-memory host shows `possibly low memory — free some up and retry` in its row status instead of only the bare exit reason. Backgrounding a session with `←` or `/background` carries its `/color` over to the new row.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| v2.1.198 | {/* min-version: 2.1.198 */}Agent view sends a notification through `preferredNotifChannel` when a background session needs input, finishes, or fails, and fires the `Notification` hook with the `agent_needs_input` or `agent_completed` type. `←` and `/exit` inside `claude attach <id>` return to agent view instead of exiting to the shell; `Ctrl+Z` returns to the shell. A background session that isolated its work in a worktree commits, pushes its own isolated branch, never `main` or `master`, and opens a draft pull request when it finishes instead of asking first. `/login` runs in agent view and opens the sign-in dialog. The `Background work is running` exit dialog offers `Move to background and exit`. The exit handoff also covers background subagents, which resume from their transcript on the next wake instead of being reported as failed. `claude --bg` combined with `-p` or `--print` is rejected with an error. The background session host requests macOS Local Network permission on first LAN access instead of failing with `connect: no route to host`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| v2.1.196 | {/* min-version: 2.1.196 */}A single `←` press backgrounds a foreground session; earlier versions required two presses, with a footer hint and a confirm. `--dangerously-skip-permissions` passed to `claude agents` shows the bypass disclaimer instead of being silently dropped. Interactive sessions you never named carry a default name such as `my-app-3f` in session listings and `claude agents --json`. Background shell commands and dynamic workflows survive the session's process being stopped, restarted, or updated, including on Windows; set `CLAUDE_CODE_DISABLE_BG_EXIT_HANDOFF=1` to turn the handoff off. A transcript misread as empty on restart is renamed with an `.orphaned-` suffix instead of deleted.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| v2.1.195 | {/* min-version: 2.1.195 */}In-flight work carries over when you background a session on Windows too; set `CLAUDE_DISABLE_ADOPT=1` to stop it instead. The `Completed` group fills the remaining vertical space and the header compacts on short terminals. An older Claude Code version no longer drops newer sessions' `state.json` fields or hides those sessions from `claude agents`. Attaching to a stopped session switches immediately instead of showing a blank screen for up to five seconds. A supervisor that can't accept connections exits and releases its lock on its own.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| v2.1.191 | {/* min-version: 2.1.191 */}`claude --bg` with an `--agent` name that doesn't match any of your subagents fails the launch: the session exits immediately with an `--agent '<name>' not found` error instead of running with the default agent.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| v2.1.174 | {/* min-version: 2.1.174 */}Background sessions no longer inherit gateway endpoint variables such as `ANTHROPIC_BASE_URL` from the supervisor's launch shell; the supervisor supplies a fresh credential snapshot to pre-warmed workers, fixing spurious `Could not resolve authentication method` errors.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| v2.1.172 | {/* min-version: 2.1.172 */}`/model` in the dispatch input sets a session-scoped dispatch model override.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| v2.1.161 | {/* min-version: 2.1.161 */}Row summaries show a `done/total` count for parallel work items; the peek panel names the longest-running parallel work item.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| v2.1.157 | {/* min-version: 2.1.157 */}`claude agents` accepts `--agent`; dispatched sessions honor the `agent` setting.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| v2.1.145 | {/* min-version: 2.1.145 */}Voice dictation supported in the peek-panel reply input and the dispatch input.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| v2.1.143 | {/* min-version: 2.1.143 */}`worktree.bgIsolation` setting added; `claude agents` accepts `--allow-dangerously-skip-permissions`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| v2.1.142 | {/* min-version: 2.1.142 */}`claude agents` accepts `--permission-mode`, `--model`, `--effort`, `--dangerously-skip-permissions`, `--settings`, `--add-dir`, `--plugin-dir`, `--mcp-config`, and `--strict-mcp-config`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| v2.1.141 | {/* min-version: 2.1.141 */}`claude agents` accepts `--cwd` to scope the list to one project.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| v2.1.139 | {/* min-version: 2.1.139 */}Agent view introduced as a research preview.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
