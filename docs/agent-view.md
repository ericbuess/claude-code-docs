> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Manage multiple agents with agent view

> Dispatch and manage many Claude Code sessions from one screen. Agent view shows what every session is doing and which ones need your input.

Agent view, opened with `claude agents`, is one screen for all your background sessions: what's running, what needs your input, and what's done. Dispatch new sessions, watch their state at a glance instead of scrolling through transcripts, and step in only when one needs you. Sessions keep running in the background without a terminal attached.

Use agent view when you have several independent tasks Claude can work on at once, such as fixing a bug, reviewing a pull request, or investigating a log. When you want to work through a problem together, attach to a session and use Claude Code interactively as usual.

Sessions in agent view run independently and report only to you. To compare with subagents, agent teams, and worktrees, see [Run agents in parallel](/en/agents).

<Note>
  Agent view is a research preview and requires Claude Code v2.1.139 or later. Check your version with `claude --version`. The interface and keyboard shortcuts may change as the feature evolves, and administrators can disable agent view for an organization with the [`disableAgentView`](#how-background-sessions-are-hosted) managed setting.
</Note>

This page covers:

* [Quick start](#quick-start)
* [Monitor sessions with agent view](#monitor-sessions-with-agent-view), including state icons, peeking and replying, attaching, organizing, and keyboard shortcuts
* [Dispatch new agents](#dispatch-new-agents) from agent view, from inside a session, or from the shell
* [Manage sessions from the shell](#manage-sessions-from-the-shell)
* [How background sessions are hosted](#how-background-sessions-are-hosted) by the supervisor process

## Quick start

This walkthrough opens agent view, dispatches a session, replies from the peek panel, and attaches for the full conversation.

<Steps>
  <Step title="Open agent view">
    From your shell, run:

    ```bash theme={null}
    claude agents
    ```

    Agent view opens with an input at the bottom and a table that fills in as sessions start. Press `Esc` at any time to exit. Your sessions keep running.
  </Step>

  <Step title="Dispatch a session">
    Type a prompt in the input and press `Enter`. A new session starts and appears as a row showing whether it's working, waiting on you, or done. Repeat to run several sessions in parallel. Each one uses your subscription quota independently, so see [Limitations](#limitations) before dispatching many at once.
  </Step>

  <Step title="Peek and reply">
    Select a row with the arrow keys and press `Space` to see what the session is doing or what it needs from you. Type a reply and press `Enter` to send it without leaving agent view.
  </Step>

  <Step title="Attach and detach">
    Press `Enter` or `→` on a row to attach when you want the full conversation. The session takes over the terminal exactly as if you had run `claude`. Press `←` on an empty prompt to detach and return to the table.
  </Step>
</Steps>

To bring an existing interactive session into agent view, run `/bg` inside it, or press `←` on an empty prompt to background the session and open agent view in one step. The session keeps running in the background and appears as a row. To start a new background session directly from the shell, run `claude --bg "<prompt>"`.

You can use `claude agents` as your primary entry point instead of `claude`: dispatch every task from agent view, attach when you want the full conversation, and press `←` to return to the table.

## Monitor sessions with agent view

Run `claude agents` to open agent view. It takes over the full terminal and lists every session grouped by state, with pinned sessions and the ones that need you at the top. Each row shows the session's name, current activity, and how long ago it last changed.

The list covers every background session under your [config directory](#how-background-sessions-are-hosted), regardless of which project or worktree it's working in, so a session started in one repository and another started in a different worktree both appear together. Interactive sessions you have open in other terminals don't appear until you [background them](#from-inside-a-session), and [subagents](/en/sub-agents) running inside a session aren't listed as separate rows.

```text theme={null}
Pinned
  ✽ clawd walk cycle          Write assets/sprites/clawd-walk.png           3m

Ready for review
  ∙ jump physics              github.com/anthropics/example/pull/2048       2h

Needs input
  ✻ power-up design           needs input: double jump or wall climb?       1m

Working
  ✽ collision detection       Edit src/physics/CollisionSystem.ts           2m
  ✢ playtest level 3          run 12 · all checkpoints cleared           in 4m

Completed
  ✻ title screen              result: menu, options, and credits done       9m
  ∙ sound effects             result: 14 SFX exported to assets/audio       4h
  … 6 more
```

Each row's icon carries two signals. The indicator tells you the session's state, and the icon's shape tells you whether the underlying process is still running. The states are:

| Indicator | State       | What it means                                                                |
| :-------- | :---------- | :--------------------------------------------------------------------------- |
| Animated  | Working     | Claude is actively running tools or generating a response                    |
| Yellow    | Needs input | Claude is waiting for your input, usually a permission decision or an answer |
| Dimmed    | Idle        | The session is waiting for input but isn't blocked on a specific question    |
| Green     | Completed   | The task finished successfully                                               |
| Red       | Failed      | The task ended with an error                                                 |
| Grey      | Stopped     | The session was stopped with `Ctrl+X` or `claude stop`                       |

The icon's shape tells you whether the underlying process is still running. A `✻`, or an animated `✽` while Claude is working, means the session is alive and you can reply to it immediately. A `∙` means the process has exited, but you can still peek, reply, or attach: Claude restarts the session from where it left off. A `✢` is a [`/loop`](/en/commands) session sleeping between iterations, with the row showing its run count and a countdown to the next iteration.

Background sessions don't need any terminal open to keep working. A separate [supervisor process](#how-background-sessions-are-hosted) runs them, so you can close agent view, close your shell, or start a new interactive session and your dispatched work keeps going.

Sessions persist on disk: closing your terminal or an auto-update doesn't lose them, and reopening `claude agents` shows them all. If your machine sleeps or shuts down, running sessions stop; restart them with `claude respawn --all`.

The one-line summary in each row is generated by your configured [Haiku-class model](/en/model-config) so the row can tell you what the session is doing, what it needs, or what it produced without opening the transcript. While a session is actively working, the summary refreshes at most once every 15 seconds, plus once when each turn ends. Each refresh is one short Haiku-class request through your normal provider, billed and handled under the same [data usage terms](/en/data-usage) as the session itself.

When a session opens a pull request, the row shows the PR link and a status indicator for its CI checks. For most tasks this row is where you pick up the result: review and merge the pull request when its checks pass.

### Peek and reply

Press `Space` on a selected row to open the peek panel. It shows what the session needs from you, its most recent output, and any pull requests it opened. Most of the time this is enough, and you never need to open the full transcript.

Type a reply in the peek panel and press `Enter` to send it to that session. When the session is asking a multiple-choice question, the peek panel shows the options and you can press a number key to pick one. For other blocked sessions, press `Tab` to fill the input with a suggested reply you can edit before sending. Prefix a reply with `!` to send a Bash command instead.

Use `↑` and `↓` to peek at adjacent sessions without closing the panel, or `→` to attach.

### Attach to a session

Press `Enter` or `→` on a selected row to attach, or press `Alt+1` through `Alt+9` to attach directly to the Nth session in the focused group. Agent view is replaced by the full interactive session, exactly as if you had run `claude` in that directory. When you attach, Claude posts a short recap of what happened while you were away.

While attached, the session behaves like any other Claude Code session: every [command](/en/commands), keyboard shortcut, and feature works.

Press `←` on an empty prompt to detach and return to agent view. If a dialog has focus and isn't responding to `←`, press `Ctrl+Z` to detach immediately.

Detaching never stops a background session: `←`, `Ctrl+C`, `Ctrl+D`, `Ctrl+Z`, and `/exit` all leave it running. To end a session from inside it, run `/stop`.

After you've dispatched or backgrounded a session, pressing `←` on an empty prompt works from any Claude Code session, not only ones you attached to from agent view. It backgrounds the current session and opens agent view with that session pre-selected, so you can switch sessions without leaving the terminal. You can turn this shortcut off in `/config`.

### Organize the list

Agent view groups sessions by state, with sessions that need input above sessions that are working or done. Press `Ctrl+S` to switch to grouping by directory instead. Your choice is saved across runs. Within a group, pin a session to the top with `Ctrl+T`, reorder with `Shift+↑` and `Shift+↓`, or press `Enter` on a group header to collapse it. To remove a session, press `Ctrl+X` to stop it and `Ctrl+X` again within two seconds to delete it. Pressing `Ctrl+X` on a group header deletes every session in that group after confirmation.

Older completed sessions fold into a "… N more" row to keep the list short. Failures and sessions with an open pull request always stay visible.

### Filter the list

Type in the dispatch input to filter instead of dispatching:

| Filter                  | Shows                                                                       |
| :---------------------- | :-------------------------------------------------------------------------- |
| `a:<name>`              | Sessions running the named agent                                            |
| `s:<state>`             | Sessions in the given state, such as `s:blocked` for sessions that need you |
| `#<number>` or a PR URL | The session working on that pull request                                    |

### Keyboard shortcuts

Press `?` in agent view to see every shortcut. The most common ones:

| Shortcut              | Action                                                                   |
| :-------------------- | :----------------------------------------------------------------------- |
| `↑` / `↓`             | Move between rows                                                        |
| `Enter`               | Attach to the selected session, or dispatch if there's text in the input |
| `Space`               | Open or close the peek panel for the selected session                    |
| `Shift+Enter`         | Dispatch and attach immediately                                          |
| `→`                   | Attach to the selected session                                           |
| `Alt+1`..`Alt+9`      | Attach to the Nth session in the focused group                           |
| `Tab`                 | Browse all subagents, or apply the highlighted suggestion                |
| `Ctrl+S`              | Switch grouping between state and directory                              |
| `Ctrl+T`              | Pin or unpin the selected session                                        |
| `Ctrl+R`              | Rename the selected session                                              |
| `Ctrl+G`              | Open the dispatch prompt in your `$EDITOR`                               |
| `Ctrl+X`              | Stop the session; press again within two seconds to delete it            |
| `Shift+↑` / `Shift+↓` | Reorder the selected session                                             |
| `Esc`                 | Close the peek panel, clear the input, or exit                           |
| `Ctrl+C`              | Clear the input; press twice to exit                                     |
| `?`                   | Show all shortcuts                                                       |

## Dispatch new agents

You can dispatch new background sessions from agent view, send an existing interactive session to the background, or start one directly from the shell.

### From agent view

Type a prompt in the input at the bottom of agent view and press `Enter` to start a new background session. The session is named automatically from the prompt. You can rename it later with `Ctrl+R`. Paste an image into the prompt to include a screenshot or diagram with the task.

Prefix or mention parts of the prompt to control how the session starts:

| Input                             | Effect                                                                                                                                                         |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `<agent-name> <prompt>`           | If the first word matches a custom [subagent](/en/sub-agents) name, that subagent runs as the session's main agent with the configuration from its frontmatter |
| `@<agent-name>`                   | Mention a custom subagent anywhere in the prompt to run it as the main agent                                                                                   |
| `@<repo>`                         | Mention a repository under the directory you opened agent view from to run the session there                                                                   |
| `/<skill>`                        | Suggest [skills](/en/skills) to dispatch as the prompt                                                                                                         |
| `#<number>` or a pull request URL | If a session is already working on that PR, select it instead of dispatching                                                                                   |
| `Shift+Enter`                     | Dispatch and immediately attach to the new session                                                                                                             |

Type `/` to dispatch a [skill](/en/skills). Packaging a recurring task as a skill lets you start the same workflow many times from agent view without retyping the prompt. Press `Tab` on an empty input to browse every dispatchable subagent, or to apply the highlighted suggestion when suggestions are showing.

When the same `@name` matches both a subagent and a sibling repository, the subagent takes precedence. The first-word form without `@` also applies to any subagent name, so a prompt that begins with a word matching one of your subagent names dispatches that subagent. Use the `@` form when you want to be explicit.

#### Dispatch to a specific directory

A new session runs in the directory you opened agent view from. To target a different directory:

* Open `claude agents` in that directory.
* Open `claude agents` in a parent directory that holds several repositories and mention one with `@<repo>` in the prompt to run the session there.
* From the shell, `cd` into the directory and run `claude --bg "<prompt>"`.

When agent view is grouped by directory, the highlighted row's directory becomes the dispatch target, so you can scroll to a group and dispatch into it without retyping the path.

### From inside a session

Run `/background` or its alias `/bg` to detach the current conversation and keep it running. Pass a prompt such as `/bg run the test suite and fix any failures` to send one more instruction before detaching.

### From the shell

Pass `--bg` to start a session that goes straight to the background:

```bash theme={null}
claude --bg "investigate the flaky SettingsChangeDetector test"
```

To run a specific subagent as the session's main agent, combine `--bg` with `--agent`:

```bash theme={null}
claude --agent code-reviewer --bg "address review comments on PR 1234"
```

After backgrounding, Claude prints the session's short ID and the commands for managing it:

```text theme={null}
backgrounded · 7c5dcf5d
  claude agents             list sessions
  claude attach 7c5dcf5d    open in this terminal
  claude logs 7c5dcf5d      show recent output
  claude stop 7c5dcf5d      stop this session
```

### How file edits are isolated

Every background session, whether started from agent view, `/bg`, or `claude --bg`, starts in your working directory but is blocked from writing files there. When the session needs to edit files, Claude moves it into an isolated [git worktree](/en/worktrees) under `.claude/worktrees/` automatically, so parallel sessions can read the same checkout but each writes to its own. The block doesn't apply when the session is already inside a worktree, when the working directory isn't a git repository, or to writes outside the working directory.

The worktree is removed when you delete the session, so merge or push the changes you want to keep before you delete. To find a session's worktree path, peek the session or attach and check its working directory.

To make a subagent always run in its own worktree regardless of how it was started, set [`isolation: worktree`](/en/sub-agents#supported-frontmatter-fields) in its frontmatter.

### Permission mode and settings

A dispatched session reads its [settings](/en/settings) and [permission mode](/en/permissions) from the directory it runs in, the same as if you had started `claude` there. Dispatching from the agent view input doesn't pass a permission mode, so the session uses the `defaultMode` from that directory's settings or the `permissionMode` from the dispatched [subagent's frontmatter](/en/sub-agents#supported-frontmatter-fields).

To set the mode from the shell, pass `--permission-mode` with `claude --bg`. Using `bypassPermissions` or `auto` this way is refused until you have accepted that mode by running `claude` with it once interactively, since those modes let a session you aren't watching act without approval.

## Manage sessions from the shell

Every background session has a short ID you can use from the shell. These commands are useful for scripting or when you don't want to open agent view.

| Command                | Purpose                                                |
| :--------------------- | :----------------------------------------------------- |
| `claude agents`        | Open agent view                                        |
| `claude attach <id>`   | Attach to a session in this terminal                   |
| `claude logs <id>`     | Print the session's recent output                      |
| `claude stop <id>`     | Stop a session. Also accepts `claude kill`             |
| `claude respawn <id>`  | Restart a stopped session with its conversation intact |
| `claude respawn --all` | Restart every stopped session                          |
| `claude rm <id>`       | Remove a session from the list                         |

## How background sessions are hosted

Background sessions are hosted by a per-user supervisor process, separate from your terminal and from agent view. It starts automatically the first time you background a session or open agent view, and you don't manage it directly. The supervisor and its sessions authenticate with the same credentials as your interactive sessions and make no additional network connections beyond the model API.

Each background session is its own Claude Code process, parented to the supervisor rather than to your terminal. A session that's actively working, waiting for your input, or has a terminal attached keeps its process running. Once a session finishes and sits unattached for about an hour, the supervisor stops its process to free resources. The transcript and state stay on disk, and the next time you attach, peek, or reply, the supervisor starts a fresh process from where it left off. When every session has finished and no terminal is connected, the supervisor itself exits and starts again the next time you background a session or open agent view.

The supervisor watches the installed Claude Code binary on disk and restarts into the new version after the regular [auto-updater](/en/setup#auto-updates) replaces it. This is a local file watch, not a network check. Background sessions are detached processes, so they keep running through the restart and the new supervisor reconnects to them.

Session state is stored under your Claude Code config directory. If you set [`CLAUDE_CONFIG_DIR`](/en/env-vars), the supervisor uses that directory instead of `~/.claude` and runs as a separate instance with its own sessions.

| Path                             | Contents                                                               |
| :------------------------------- | :--------------------------------------------------------------------- |
| `~/.claude/daemon.log`           | Supervisor log                                                         |
| `~/.claude/daemon/roster.json`   | List of running background sessions, used to reconnect after a restart |
| `~/.claude/jobs/<id>/state.json` | Per-session state shown in agent view                                  |

To turn off background agents and agent view entirely, set the `disableAgentView` [setting](/en/settings) to `true` or set the `CLAUDE_CODE_DISABLE_AGENT_VIEW` environment variable. Administrators can enforce this through [managed settings](/en/permissions#managed-settings).

## Troubleshooting

### Agent view opens with no sessions

Agent view is empty until you dispatch your first session. Type a prompt in the input at the bottom and press `Enter`.

### Sessions show as stopped after waking your machine

Background sessions don't survive sleep or shutdown. Attach, peek, or reply to any stopped session and it restarts from where it left off. To restart all of them at once, run `claude respawn --all`.

### A session is slow to respond after attaching

Once a session has finished and sat unattached for about an hour, the supervisor stops its process to free resources. Attaching starts a fresh process from where it left off, which takes a moment. Sessions that are working or waiting on you are never stopped this way.

### `.claude/worktrees/` is filling up

Worktrees are removed when you delete the session that created them. If a session ended without cleaning up, list leftover entries with `git worktree list` in the project directory and remove each with `git worktree remove <path>`. See [Clean up worktrees](/en/worktrees#clean-up-worktrees).

## Limitations

Agent view is a research preview. Current limitations to be aware of:

* **Rate limits apply**: background sessions consume your subscription usage the same as interactive sessions, so running ten agents in parallel uses quota roughly ten times as fast as running one.
* **Sessions are local**: background sessions run on your machine and stop if it sleeps or shuts down.
* **Worktrees are deleted with the session**: merge or push changes before deleting a session that edited files in its own worktree.

## Next steps

Now that you understand agent view, explore these related features:

* [Run agents in parallel](/en/agents): compare agent view with subagents, agent teams, and worktrees
* [Subagents](/en/sub-agents): define reusable agent configurations with custom prompts, tools, and isolation
* [Agent teams](/en/agent-teams): coordinate multiple sessions that message each other
* [Claude Code on the web](/en/claude-code-on-the-web): run sessions in a managed cloud environment instead of locally
