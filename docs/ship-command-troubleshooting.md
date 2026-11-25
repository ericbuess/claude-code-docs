> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshoot /ship and /steward

> Look up a message or a symptom from `/ship` or `/steward`: a missing command, nothing committed or pushed, a watch that didn't start, or one that stopped.

[`/ship`](https://code.claude.com/docs/en/ship-command) is a Claude Code command that opens a GitHub pull request for your change and has Claude review it. Claude then keeps working on the pull request from your session. This ongoing work is called a watch. `/steward` starts a watch on a pull request that's already open.

Find what happened in the first column, or search for words from the message that Claude Code printed:

| What happened | Go to |
| :- | :- |
| `/ship` isn't in the `/` menu, or Claude Code doesn't recognize it | [/ship isn't available in your session](#%2Fship-isn’t-available-in-your-session) |
| You typed the command and it printed a message without starting | [/ship or /steward printed a message and didn't start](#%2Fship-or-%2Fsteward-printed-a-message-and-didn’t-start) |
| It ran, and nothing was committed or pushed | [/ship committed or pushed nothing](#%2Fship-committed-or-pushed-nothing) |
| The pull request is open, and Claude isn't following up on it | [No watch started](#no-watch-started) |
| Claude was following up, and stopped | [A watch stopped](#a-watch-stopped) |
| A message appeared while Claude was following up | [Messages during a watch](#messages-during-a-watch) |
| The pull request isn't what you expected | [Pull request results that you didn't expect](#pull-request-results-that-you-didn’t-expect) |
| A custom `/ship` or `/steward` command stopped working | [A custom /ship or /steward command stopped loading](#a-custom-%2Fship-or-%2Fsteward-command-stopped-loading) |

## /ship or /steward is missing or doesn't start

Start here when the command isn't offered, or when it prints a message.

### /ship isn't available in your session

`/ship` is missing from the `/` menu, typing it starts `/code-review`, or you see `Unknown command: /ship`. Cloud sessions don't have `/ship`.

On your own machine, take these steps:

1. Run `claude update` in your shell, then quit and start `claude` again.
2. If `/ship` is still missing, quit and start `claude` once more, because a new feature [can take a second start](https://code.claude.com/docs/en/env-vars.md#first-session-after-an-install-or-upgrade) to show.
3. Run `/status` at the Claude Code prompt. Its `Setting sources` line lists the settings that loaded. In each one that's your own [settings file](https://code.claude.com/docs/en/settings.md#find-or-create-your-settings-files), remove [`disableBundledSkills`](https://code.claude.com/docs/en/settings-reference#disablebundledskills) and any `ship-local` entry under [`skillOverrides`](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings). To change managed settings, ask your administrator.
4. Check whether your session [skips feature-flag fetching](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching). On a third-party provider or in a Claude apps gateway session, `/ship` requires Claude Code v2.1.331 or later. In any other session, unset any variable that turns fetching off, such as `DISABLE_TELEMETRY`.
5. Check whether [`CLAUDE_CODE_DISABLE_SHIP`](https://code.claude.com/docs/en/env-vars#variables) is set, in your shell or under `env` in a settings file. Unset it, then quit and start `claude` again. The variable requires Claude Code v2.1.331 or later.

### A skillOverrides entry turns off /ship or /steward

`Skill "ship-local" is disabled via skillOverrides`, or the same message for `steward`, means that a [`skillOverrides`](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings) entry in your settings turns off the command. Remove the entry. To change an entry in managed settings, ask your administrator.

### /ship or /steward printed a message and didn't start

Find the opening words of the message:

| Message | What to do |
| :- | :- |
| `This session was started by another session` | Run it in a session that you started yourself |
| `Usage: /ship` or `Usage: /steward` | Check what you typed against [the arguments](https://code.claude.com/docs/en/ship-command.md#arguments-for-%2Fship-and-%2Fsteward) |
| `Nothing started. /ship starts only from a line that you type`, or the same for `/steward` | Type the command yourself at the Claude Code prompt. It doesn't start from `claude -p` or from a program |
| `Nothing started. This line counts only if you type it yourself` | You accepted a [prompt suggestion](https://code.claude.com/docs/en/interactive-mode.md#prompt-suggestions). Type the command yourself at the Claude Code prompt |
| `Nothing started. Claude Code's built-in /ship is turned off while`, or the same for `/steward` | Unset the variable that the message names, such as `CLAUDE_CODE_DISABLE_SHIP`, then start Claude Code again |
| `Nothing started. Claude Code's built-in /ship doesn't start in this kind of session`, or the same for `/steward` | You typed it somewhere such as `claude -p`. Run `claude` in a terminal and type the command there |
| `Nothing started. /ship is a command built into Claude Code`, or the same for `/steward` | Another command, such as a plugin's, has the same name. To run the built-in command, type the same line again. To run the other one, follow the message, which gives its name or says where to find it |
| `/ship didn't start:` or `/steward didn't start:` | The rest of the message says what to check. In plan mode, for example, press `Shift+Tab` to leave plan mode, then run the command again |
| `/ship is turned off right now`, or the same for `/steward` | If the message says to run `/login`, do that at the Claude Code prompt, then run the command again. Otherwise, one cause is that `CLAUDE_CODE_DISABLE_SHIP` was set after the session started, for example under `env` in a settings file. Unset it, quit and start `claude` again, then run the command |
| `/ship can't start from a queued message` or `/steward can't start from a queued message` | Wait until Claude has finished, then run it again |

### The GitHub CLI isn't ready

`/ship` and `/steward` reach GitHub through the GitHub CLI, `gh`:

| Message | What to do |
| :- | :- |
| `GitHub CLI (gh) isn't installed` or `GitHub CLI (gh) isn't signed in` | Install it, run `gh auth login` in your shell, then run the command again |
| `gh couldn't tell me about a pull request here` | The words in parentheses say what failed. To see `gh`'s own error, run `gh pr view` in your shell. One cause is that none of your checkout's remotes is on a GitHub host that `gh` is signed in to. For GitHub Enterprise, run `gh auth login --hostname HOST` in your shell |
| `I can't watch the branch with git alone` | None of your checkout's remotes is on a GitHub host that `gh` is signed in to. For GitHub Enterprise, run `gh auth login --hostname HOST` in your shell, then run the command again. On another host, the words after the colon say what to fix, such as pushing the branch first. See [Watch a branch on another host](https://code.claude.com/docs/en/ship-command.md#watch-a-branch-on-another-host) |

## /ship committed or pushed nothing

In some cases, `/ship` leaves the commit or the push to you and says why. Its message can start with `Nothing committed or pushed`, `Nothing pushed`, `I didn't push anything`, `There is no pull request to watch`, or `This branch has no open pull request`. On a host other than GitHub, `/ship` doesn't commit or push when it starts, so see [Watch a branch on another host](https://code.claude.com/docs/en/ship-command.md#watch-a-branch-on-another-host).

Find your case, take the step in its row, then run `/ship` again. In these cases, if nothing is pushed and the branch has no pull request, Claude reviews your change and [no watch starts](#no-watch-started).

### Public repositories and files that /ship doesn't commit

`/ship` looks at the repository and at each changed file's name before it commits:

| Case | What to do |
| :- | :- |
| `For a public repository /ship doesn't commit anything for you` | Commit your work yourself, on a branch other than the default branch |
| `By its name, this file may hold secrets` or `By their names, these files may hold secrets`, for a changed file such as `.env` or `password.txt` | If it holds no secret, commit your work yourself, on a branch other than the default branch. Otherwise, set it aside, for example with `git stash push -u -- <file>` in your shell |
| The message names empty files that you didn't create, such as `.bashrc` or `.gitconfig` | On Linux and WSL2, the [sandbox](https://code.claude.com/docs/en/sandboxing.md) keeps empty files in your checkout while a sandboxed command runs. The sandbox needs them until the command ends, so don't stash, commit, or delete them before then. Stop the command, for example from [`/tasks`](https://code.claude.com/docs/en/commands#all-commands), or wait for it to end, and the sandbox removes them. If they stay with no sandboxed command running, [remove the leftover files](https://code.claude.com/docs/en/errors.md#stale-sandbox-mask-files-left-by-a-killed-session) |
| You changed a file that configures git, CI, or a coding agent, such as `.gitignore`, `CLAUDE.md`, or anything under `.github/` | Commit your work yourself, on a branch other than the default branch |

### Branches that /ship can't commit to or push

`/ship` needs a branch that it can commit to and push:

| Case | What to do |
| :- | :- |
| `there is nothing here to open one for`: you have no uncommitted changes, and every commit on the branch is already on the default branch, or merging them would change nothing there | Make a change, or check out the branch that holds your work |
| `you're on the default branch, which /ship never pushes` | Move your commits to a new branch, for example with `git switch -c <branch>` in your shell |
| You're in detached HEAD state, or in the middle of a rebase | Check out a branch, or finish the rebase |

### Deny rules that forbid a commit or push

A [deny rule](https://code.claude.com/docs/en/permissions.md#manage-permissions), such as `Bash(git push *)`, can forbid the commit, the push, or opening the pull request. If whoever set the rule agrees, take those steps yourself.

A watch needs `git commit` and `git push` as well. If the rule forbids one of them, [have it removed](#a-tool-rule-or-hook-blocks-a-watch) before you run `/ship` again.

### Your pull request is already open

Messages such as these mean that `/ship` left newer work off your open pull request:

| Message | What it means | What to do |
| :- | :- | :- |
| `/ship didn't commit your uncommitted work` | Causes include a public repository, auto-merge turned on, and a merge or cherry-pick in progress. If [no watch can start](#no-watch-started), the review covers your uncommitted work. Otherwise, a review doesn't cover it, and your unpushed commits [can go up with Claude's next push](https://code.claude.com/docs/en/ship-command.md#keep-working-while-a-watch-runs) | If the message gives a `git push` line, commit the work yourself, then run that line. Otherwise, run `/ship` again when the message says to |
| `Nothing pushed` or `Nothing committed or pushed`, with a sentence about your unpushed commits | `/ship` held those commits back. No review or watch starts, and a running watch on that pull request ends. One cause is a file in them with a name such as `password.txt` | If the commits should go up, run the `git push` line in the message. If not, take the file out of every unpushed commit. Then run `/ship` again |

Before v2.1.331, `/ship` prints neither message. It doesn't commit your uncommitted work once a pull request is open, so commit it, then push it, as in `git push origin <branch>` in your shell. It doesn't hold back your unpushed commits, which [can go up with Claude's next push](https://code.claude.com/docs/en/ship-command.md#keep-working-while-a-watch-runs).

### GitHub Enterprise and forks

`/ship` doesn't open a pull request on GitHub Enterprise or from a fork. Push the branch and open the pull request yourself, then run `/ship`. From a fork, the checkout also needs a remote for the repository that the pull request goes to, or no watch starts.

## No watch started

A watch is Claude's ongoing work on your pull request, which starts after `/ship`'s review or when you type `/steward`. In some cases, no watch starts and Claude says why. Its message can contain `/steward didn't start.`, `I can't watch`, or `is running on pull request`.

Fix the cause, then type `/steward` to start the watch with no second review. On a host other than GitHub, add any base that you named, as in `/steward origin/main`. If a branch on GitHub still has no pull request, type `/ship`.

### Your pull request or branch isn't ready for a watch

Check the pull request and your checkout first:

| Cause | What to do |
| :- | :- |
| On GitHub, the branch has no pull request, and `/steward` doesn't open one | See [/ship committed or pushed nothing](#%2Fship-committed-or-pushed-nothing) |
| The pull request's branch isn't checked out in this session | Check it out |
| The pull request carries one of [PR Steward](https://code.claude.com/docs/en/pr-steward.md)'s labels, such as `claude-pr-steward-watching` | To take over, remove the label and pull the branch, as Claude's message says |

### A session setting blocks a watch

Some settings of the session keep a watch from starting:

| Cause | What to do |
| :- | :- |
| The session is in `bypassPermissions` mode | Press `Shift+Tab` to switch to a permission mode other than plan mode |
| [Remote Control](https://code.claude.com/docs/en/remote-control.md) is on | Run `/rc`, then select **Disconnect this session** |
| `this session runs in the background` | Open a new terminal in the checkout that holds the branch, run `claude`, and type `/steward` there |
| A message about an entry `on your PATH`, such as `entry 2 of 9 on your PATH is empty (a stray colon)` | Take the entry out of `PATH`, or write it as a full path, in your shell's profile and in any `env` block of your Claude Code settings that sets `PATH`. Quit Claude Code, start it again from a new terminal, then type `/steward` |
| `your PATH has a relative or empty entry` | Before v2.1.331, `/ship` with no pull request number reviews your change, and doesn't commit, push, or look for a pull request. Take the empty or relative entry out of `PATH`, such as a trailing `:`, or `;` on Windows. Start `claude` again, then run `/ship` |
| Your `PATH` holds a folder inside the checkout. This happens, for example, when you activate a Python virtual environment that's in the checkout, or start `claude` through `npx` or a package script | To start a session without that folder, run `deactivate` in your shell if you use a virtual environment, then start `claude` directly |

### A tool, rule, or hook blocks a watch

A watch on a GitHub pull request needs `gh`, `git commit`, and `git push`, and it doesn't start where a project's hook could approve commands:

| Cause | What to do |
| :- | :- |
| `gh` isn't installed or signed in | See [The GitHub CLI isn't ready](#the-github-cli-isn’t-ready) |
| `this gh is too old for a watch` | Update the GitHub CLI to 2.63 or later, then type `/steward` |
| A deny rule forbids a command that the watch needs, such as `git push` | Claude's message names the command and the settings that hold the rule. If whoever set it agrees, remove it there. To change a rule in managed settings, ask your administrator |
| The project sets a hook that could approve commands, for example a `PreToolUse` or `PermissionRequest` [hook](https://code.claude.com/docs/en/hooks.md) on shell commands in the checkout's `.claude/settings.json` | The message names the file and says what to change |

### Cases where no watch can start

In these cases, `/ship` can still review your change:

* You're on native Windows
* On GitHub, someone else opened the pull request
* On GitHub, you can't push to the repository that the pull request goes to, and another person has commented or reviewed. If this happens while a watch is running, the watch ends

## A watch stopped

A watch is Claude's ongoing work on your pull request, which starts after `/ship`'s review or when you type `/steward`. After one ends, look for a line that starts `Stopped watching`, which gives the reason.

To start the watch again, type the command that the line gives, if it gives one. To check whether a watch is still running, type [`/tasks`](https://code.claude.com/docs/en/ship-command#check-whether-a-watch-is-running) at the Claude Code prompt while Claude is idle.

Find the words that follow "because" in that line:

| Reason | What happened |
| :- | :- |
| `the watch was cancelled`, or `its check-in was cancelled` | You pressed `Esc` or `Ctrl+C` at the prompt or while Claude was working, or stopped the task in `/tasks`. Claude's messages call its work on the pull request a check-in. An `Esc` that closes the `/tasks` list leaves a watch running |
| `the watch couldn't go on` | Claude's reply may give the cause. One cause is that the pull request's branch is no longer checked out. Check it out in the folder where you started, then start the watch again |
| `a watch doesn't carry over when a session is resumed` | The process that ran the watch has ended, for example because you closed the terminal. Running `claude --continue` in your shell brings back the conversation without the watch |
| `you moved to another session` | `/clear`, `/resume`, or `/branch` can do that |
| `another loop took its place`, or `its check-ins were replaced` | You started a `/loop` |
| `your new command took over this session` | You ran `/ship` or `/steward` again |
| `a deny rule now blocks a command that the watch runs`, or `a deny rule now forbids a command that the watch runs` | Type `/permissions` at the Claude Code prompt to see the rule. See [A tool, rule, or hook blocks a watch](#a-tool-rule-or-hook-blocks-a-watch) |
| `the watch reached its time limit` | About seven days passed |
| `the watch stalled`, or `no next check-in was set` | A declined permission prompt, an error, or a usage limit can do that |
| `this session is in plan mode` | Press `Shift+Tab` to leave plan mode, then type the command that the line gives |
| `this session runs in the background` | Open a new terminal in the checkout that holds the branch, run `claude`, and type the command that the line gives |
| `you asked` | You typed `/ship stop` or `/steward stop` |
| `a file that gh, git, or /steward relies on changed` | See [A file that the watch relies on changed](#a-file-that-the-watch-relies-on-changed) |
| `a file that git or /steward relies on changed` | The same message, for a [watch on another host](https://code.claude.com/docs/en/ship-command.md#watch-a-branch-on-another-host). See [A file that the watch relies on changed](#a-file-that-the-watch-relies-on-changed) |

Where a row gives two wordings, the second is the one from before v2.1.331.

`Nothing to stop. This session isn't watching a pull request`, or `No pull request is being watched in this session`, means that you typed `/ship stop` or `/steward stop` and no watch was running. Scroll up for a `Stopped watching` line.

### A file that the watch relies on changed

A watch ends when something changes a file that `gh`, `git`, or `/steward` relies on. Files such as these count:

* **Git's settings**: `git push -u`, `git branch -u`, and `git remote add` change them. An editor such as VS Code can also add a setting to `.git/config` when it opens the repository or you switch back to it
* **`.claude/settings.local.json`**: Claude Code writes it when you answer a permission prompt with "Yes, and don't ask again"

Review the change, then type the command that the `Stopped watching` line gives to start the watch again.

If you changed none, one cause on Linux and WSL2 is a [sandboxed](https://code.claude.com/docs/en/sandboxing.md) command that starts or ends during the watch. Stop the command or wait for it to end.

## Messages during a watch

These messages appear in your session during a watch:

| Message, or what you see | What to do |
| :- | :- |
| `Claude Code did not run this`, or `Not run · permission denied` | Claude tried a step, and a [limit on the watch](https://code.claude.com/docs/en/ship-command.md#what-claude-code-blocks-during-a-watch) or one of your rules or hooks refused it. The message also appears when the watch had already ended. Claude's messages call those limits "the fence" |
| `In this session there's a way around`, followed by `the watch's limits`, `these limits`, or `my limits` | A setting in your session, such as a rule, a hook, a plugin, or the sandbox, lets some commands past the [limits on the watch](https://code.claude.com/docs/en/ship-command.md#what-claude-code-blocks-during-a-watch). The text after the message names it. To see your rules, type `/permissions` at the Claude Code prompt. To end the watch while you decide, type `/steward stop` |
| A line such as `1 comment not read (no write access, or a bot that you haven't named)` | Claude [skipped a comment](https://code.claude.com/docs/en/ship-command.md#what-claude-does-during-a-watch). Open the link in the message to read it. For a bot on GitHub that you want Claude to read, type `/steward +botname`. For a person's comment that you agree with, tell Claude what to change |
| `gh couldn't say where the pull request's head and base stand` | Claude Code refused one of Claude's pushes. To see `gh`'s own error, run `gh pr view` in your shell. Before v2.1.331, one cause is a GitHub CLI older than 2.63. Run `gh --version` in your shell to check. Update it, then type `/steward` to start the watch again |
| `A watch is on`, `The watch's limits still hold`, or `/ship is still starting` or the same for `/steward`, after you press `←` or type `/background` | Claude Code doesn't move a session to the background while a watch is on. To move it, first take the step that the message names, such as typing `/steward stop`, which ends the watch. Before v2.1.331, the session moves, and [the watch ends](https://code.claude.com/docs/en/ship-command.md#when-a-watch-can-lead-to-a-merge) |
| `Claude resuming /loop wakeup` or `/steward --tend` in the session | Claude Code enters them when Claude checks the pull request during a watch. You can keep working as you are |

## Pull request results that you didn't expect

Start here when `/ship` ran, and something on GitHub or in your repository surprised you:

| What you see | Why, and what to do |
| :- | :- |
| The pull request's title, or the commit message, is a line such as `Update greet.py and 1 more` | `/ship` falls back to that line when Claude can't write one from the session's conversation, for example in a session where you didn't discuss the change. Edit the title and description on GitHub. Next time, run `/ship` in the session where you made the change, or commit your work yourself first, on a branch other than the default branch |
| Claude pushed commits or answered a reviewer before you saw them | In auto mode, or where your rules or the sandbox allow a command, a watch works that way. See [Ask Claude to check with you first](https://code.claude.com/docs/en/ship-command.md#ask-claude-to-check-with-you-first) |
| New uncommitted changes didn't reach the open pull request | See [Your pull request is already open](#your-pull-request-is-already-open) |
| `git pull` or `git push` asks for an upstream branch | `/ship` sets no upstream. Name the remote and branch, as in `git push origin <branch>`. Setting an upstream changes git's settings, which [ends a running watch](https://code.claude.com/docs/en/ship-command.md#keep-working-while-a-watch-runs) |

## A custom /ship or /steward command stopped loading

These messages are about a custom skill or command. Its name is one that the built-in commands reserve, such as `ship`, `ship-local`, or `steward`:

| Message | What to do |
| :- | :- |
| `Not loaded: a custom /ship` or `Not loaded: custom /ship, /steward` | Rename it, then restart Claude Code |
| `Nothing started. A custom /ship isn't loaded`, or the same for `/steward` | To run the built-in command, type the same line again. To run the custom one, rename it, then restart Claude Code |

Leave a repository's `.claude/skills/steward/SKILL.md` as it is, because PR Steward and the watch read it as instructions. Neither message counts that file, so one that names `/steward` is about another skill or command.

### Keep a custom /ship or /steward without renaming

If you've already created your own skill or command called `/ship` or `/steward` and don't want the built-in versions to override it, you can turn them off. To do that, use the `CLAUDE_CODE_DISABLE_SHIP` environment variable, which turns off both together and requires Claude Code v2.1.331 or later. Before you set it, [remove any `"off"` entry](#a-skilloverrides-entry-turns-off-%2Fship-or-%2Fsteward) for your command under `skillOverrides`.

Add this [`env`](https://code.claude.com/docs/en/settings-reference#env) entry to your [user settings file](https://code.claude.com/docs/en/settings.md#settings-files-and-who-they-affect), or to a project's `.claude/settings.json` for everyone who starts sessions in its top folder, then restart Claude Code:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_DISABLE_SHIP": "1"
  }
}
```

To check that your command loaded, type `/` at the Claude Code prompt and look for its description or first line.

If your command is named `steward` and the repository has a `.claude/skills/steward/SKILL.md` file, check [which one runs](https://code.claude.com/docs/en/skills.md#resolve-skills-that-share-a-name).

## Related resources

* [`/ship` and `/steward`](https://code.claude.com/docs/en/ship-command): what the commands do, how to run them, and what limits Claude during a watch
* [Permission modes](https://code.claude.com/docs/en/permission-modes.md): auto mode and the other permission modes
* [Hooks](https://code.claude.com/docs/en/hooks.md): the `PreToolUse` and `PermissionRequest` hooks
