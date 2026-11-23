> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Get a pull request ready with /ship and /steward

> Run `/ship` to open a GitHub pull request, get a review, and have Claude work on feedback and failing checks, or `/steward` to skip the review on an open one.

`/ship` is a Claude Code command that opens a GitHub pull request for your change if your branch doesn't have one. Claude reviews your change and works on feedback and failing checks to help get it ready to merge.

If your pull request is already open and you don't want a review, type [`/steward`](#start-a-watch-with-%2Fsteward). It skips the review, and Claude does the same work on feedback and failing checks.

> [!NOTE]
>
> Run either command from the Claude Code CLI in a terminal, in your local clone of the repository. Cloud sessions don't have them.

After you type `/ship`, your change goes through these steps:

![Diagram of what happens after you type /ship. In your session, Claude Code opens a pull request and reviews it with /code-review. Then the watch starts: Claude pushes fixes to your branch and responds to checks, comments, and conflicts. When the pull request is ready, you merge it.](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/ship-flow.svg?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=ccfa7e5848711d691b8cdf65ac22b26e)

1. **Pull request**: `/ship` can [commit your work, push your branch, and open the pull request](#what-%2Fship-commits-and-pushes) as you
2. **Review**: Claude reviews your change with [`/code-review`](https://code.claude.com/docs/en/code-review-local)
3. **Watch**: Claude keeps checking the pull request from your Claude Code session. It works on failing checks, merge conflicts, reviewers' comments, and the findings from its review, and pushes fixes. This ongoing work is called a watch
4. **Merge**: once the pull request is ready, merge it yourself

`/steward` skips steps 1 and 2 and starts the watch.

## When to use /ship and /steward

With either command, Claude works on your pull request's feedback and failing checks. Choose between `/ship` and `/steward` by where your change is:

* **`/ship`**: your change is finished, and you want Claude to review it and then work on the feedback and failing checks that follow
* **`/steward`**: your pull request is already open and you don't want a review first, or a watch ended and you want to start it again

Both commands run in your session, so their work counts against your usage.

If you want something else, such as a review alone or fixes from a cloud session, use one of these:

| You want | Use |
| :- | :- |
| A review alone | [`/code-review`](https://code.claude.com/docs/en/code-review-local) |
| Fixes as feedback arrives, from a cloud session | [Auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests) or `/autofix-pr` |
| Agents for whole repositories, billed to an organization | [Claude Ship](https://code.claude.com/docs/en/claude-ship.md) |

## Prerequisites for /ship and /steward

Install or update these tools:

* Claude Code v2.1.330 or later. If `/ship` is missing, see [/ship isn't available in your session](https://code.claude.com/docs/en/ship-command-troubleshooting.md#%2Fship-isn’t-available-in-your-session)
* The [GitHub CLI](https://cli.github.com) 2.63 or later, signed in with `gh auth login`. With an older version, Claude can't push fixes
* git 2.38 or later, to merge new commits into your branch. With an older git, Claude leaves those merges to you

Then get your change and your session ready:

* **A finished change, for `/ship`**: have it in your local clone of a repository on GitHub. It can be uncommitted, committed on a branch other than the default branch, or already in an open pull request of yours. If the repository is hosted somewhere other than GitHub, `/ship` opens no pull request, and Claude reviews your change
* **Only the files that you want in the pull request, for `/ship`**: `/ship` can commit all your uncommitted changes, new files included. In your shell, run `git status`. Delete each new file that you don't want in the pull request, or stash the file with `git stash push -u -- <file>`
* **No secrets in those files, for `/ship`**: `/ship` looks for secrets by file name, such as `.env`, so look inside your files yourself. A deny rule such as `Read(./notes.txt)` doesn't keep a file out of the commit
* **An open pull request on GitHub, for `/steward`**: it has to be your own, with its branch checked out in your local clone
* **Permission mode**: choose [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode) if you want Claude to work on the pull request unattended. In most other permission modes, Claude waits at each prompt. In `bypassPermissions` mode, no watch starts

On native Windows, [no watch starts](https://code.claude.com/docs/en/ship-command-troubleshooting.md#cases-where-no-watch-can-start).

> [!WARNING]
>
> Run a watch only where you trust everyone who can merge to the base branch or push to your branch. Any of them can run programs on your computer with your credentials.

## Run /ship or /steward

In a terminal, open Claude Code in your clone, then type `/ship` or `/steward` at the prompt. Both take [arguments](#arguments-for-%2Fship-and-%2Fsteward), such as a pull request's number.

### Run /ship on a finished change

If you made the change with Claude, use that same session, because Claude writes the commit message from the session's conversation. Anyone who can see the pull request can read that message.

> [!NOTE]
>
> `/ship` proceeds with no confirmation prompt. After you press Enter, it can [commit your work, push your branch, and open the pull request](#what-%2Fship-commits-and-pushes) as you. Before the commit, and again before the push, a line that ends `Esc to cancel` says what's about to happen. If you do nothing, `/ship` continues after a few seconds.

If you cancel before the push, a commit that `/ship` made stays. To undo it and keep your files, run `git reset HEAD~1` in your shell.

### What /ship commits and pushes

In a repository on github.com that isn't a fork, `/ship` can commit your uncommitted changes, push the branch, and open the pull request before the review. On the default branch, it commits on a new branch and switches your checkout to that branch. If your work is already committed on another branch, `/ship` pushes that branch and opens the pull request.

`/ship` doesn't commit your uncommitted changes in these cases. Take the first one that fits:

* **A pull request is already open for the branch**: commit and push anything that you want in the pull request
* **The repository is public**: if you're on a branch other than the default branch and it has commits of its own, `/ship` pushes those and opens a pull request without your uncommitted changes. Otherwise, commit your work on a branch other than the default branch, then run `/ship` again
* **An uncommitted file's name suggests a secret, such as `.env`**: in a repository that isn't public, `/ship` doesn't commit or push anything. See [/ship committed or pushed nothing](https://code.claude.com/docs/en/ship-command-troubleshooting.md#%2Fship-committed-or-pushed-nothing)

Open the pull request yourself, then run `/ship`, if you want any of these:

* A draft pull request
* Another base branch
* Your repository's pull request template
* A pull request on [GitHub Enterprise or from a fork](https://code.claude.com/docs/en/ship-command-troubleshooting.md#github-enterprise-and-forks)

If `/ship` commits or pushes nothing and these cases don't say why, see [/ship committed or pushed nothing](https://code.claude.com/docs/en/ship-command-troubleshooting.md#%2Fship-committed-or-pushed-nothing).

### Start a watch with /steward

To start a watch with no review first, type `/steward` at the Claude Code prompt. Use it on your own open pull request, or to start again after a watch ends. Before you leave a watch alone, see [Code that a watch runs on your computer](#code-that-a-watch-runs-on-your-computer).

`/steward` is separate from [PR Steward](https://code.claude.com/docs/en/pr-steward.md), the agent that an organization sets up. Where PR Steward is already working on your pull request, no watch starts.

## What Claude does during a watch

A watch is Claude's ongoing work on your pull request, which starts after `/ship`'s review or when you type `/steward`. Claude uses your `gh` and `git` sign-ins, so its work on GitHub appears under your name.

In auto mode, Claude takes these actions without asking:

* Works on the review findings that it judges to be problems
* Can post one comment that sums up its review
* Pushes commits to your branch
* Merges the base branch into yours, to resolve conflicts or bring your branch up to date
* Works on failing checks, and re-runs failed ones
* Answers review comments, resolves threads, and re-requests reviews

Claude reads comments from you and from people with write access. On github.com, it also reads comments from Claude's bot. To have Claude read another bot's comments, type `/steward +` and the bot's name, as in `/steward +my-lint-bot`.

When checks pass and comments are answered, Claude says so in the session. Merge the pull request yourself. What can merge depends on your permissions and your repository's branch rules. See [When a watch can lead to a merge](#when-a-watch-can-lead-to-a-merge).

### Keep working while a watch runs

While a watch runs, keep the session open and [in the foreground](https://code.claude.com/docs/en/agent-view.md#send-the-session-to-the-background), the computer awake, and your pull request's branch checked out. Claude edits files in the same checkout as you.

* **To start your next change**: work in another folder, such as a second clone of the repository, and open another Claude Code session there
* **To push your own commits**: name the remote and branch, as in `git push origin <branch>`. If you change git's settings, for example with `git push -u` or `git branch -u`, the watch ends
* **Commits that you haven't pushed**: they can go up with Claude's next push
* **Your uncommitted work**: Claude can edit a file that you're working on, and can commit it. When Claude acts without a message from you, Claude Code refuses these commands from Claude: `git stash`, `git reset`, `git checkout`, `git add -A`, and `git commit -a`

### Ask Claude to check with you first

To see `/ship`'s review findings or a reviewer's comment before Claude acts on them, say so in a message at the Claude Code prompt. To see the findings before Claude fixes anything, send the message while the review is running.

This example asks Claude to show you its findings, and to ask before it pushes or replies:

```text theme={null}
From now on, don't push code changes or reply to reviewers without asking me first. Show me the review findings and wait.
```

That message is a request to Claude, and Claude Code doesn't enforce it.

### Save instructions for watches in a repository

To tell Claude how to look after pull requests in a repository, save a file at `.claude/skills/steward/SKILL.md` in the repository's top folder. [PR Steward reads the same file](https://code.claude.com/docs/en/pr-steward-pull-requests.md#save-pr-steward-instructions-for-everyone-in-a-repository), so one file can serve both, and that section has an example.

During a watch, Claude reads the copy in your checkout and follows it as instructions, for example on which checks matter and how to run the tests, within these limits:

* **Installs and downloads**: Claude can skip a line that installs or downloads something, such as the `npm install` line in that example
* **Blocked commands**: the file doesn't change [what Claude Code blocks during a watch](#what-claude-code-blocks-during-a-watch)
* **Changes to the file**: if you add or edit it yourself while a watch runs, the watch ends. For whose other changes can reach it, see [Code that a watch runs on your computer](#code-that-a-watch-runs-on-your-computer)

## Check, stop, or restart a watch

A watch is Claude's ongoing work on your pull request, which starts after `/ship`'s review or when you type `/steward`. It runs in your session, so you check it and stop it at the Claude Code prompt.

### Check whether a watch is running

Type `/tasks` at the Claude Code prompt. Once the review is done and while Claude isn't working, a running watch appears in the list as a scheduled task whose name starts with `/steward --tend`.

### What ends a watch

After a watch ends, look for a line that starts `Stopped watching pull request`. [A watch stopped](https://code.claude.com/docs/en/ship-command-troubleshooting.md#a-watch-stopped) lists reasons that it gives.

The watch ends in cases such as these:

| Where | What ends the watch |
| :- | :- |
| On the pull request | It's merged or closed, [PR Steward](https://code.claude.com/docs/en/pr-steward.md) labels it, or seven days pass |
| At the keyboard | You press `Esc` or `Ctrl+C` at the prompt or while Claude is working. One press can end the watch, with no confirmation |
| In your checkout | You check out another branch, or change git's settings |
| In the session | The session ends, you send it to the background, you start another watch or a `/loop` with a task, or you run `/clear`, `/resume`, or `/branch` |
| After a failure | An error, a declined prompt, or a usage limit can end it early |

### Stop or restart a watch

To end a watch, type `/ship stop` at the Claude Code prompt in the session that runs it. If Claude is working when you type it, the watch ends when the current turn does, so what Claude pushes or posts in that turn still reaches the pull request. To stop the turn as well, press `Esc`.

To start a watch again, type [`/steward`](#start-a-watch-with-%2Fsteward).

## Decide where to run a watch

A watch is Claude's ongoing work on your pull request, which starts after `/ship`'s review or when you type `/steward`. Claude works with your `gh` and `git` sign-ins. Before you leave a watch alone, check what Claude Code blocks, which code can run on your computer, and what can still lead to a merge.

### What Claude Code blocks during a watch

When Claude acts without a message from you, Claude Code blocks `gh` and `git` commands that merge the pull request, approve it, turn on auto-merge, or force-push. At those times, Claude Code also limits Claude's `gh` and `git` commands to a short list, and refuses tools that the watch doesn't need, such as connectors, `WebFetch`, and `WebSearch`. To see these limits in Claude Code, type `/ship terms` at the prompt.

> [!WARNING]
>
> The limits on a watch don't cover everything. The watch uses your `gh` and `git` sign-ins, so it could merge a pull request that your repository's branch rules let you merge without another person's approval. See [When a watch can lead to a merge](#when-a-watch-can-lead-to-a-merge). A setting in your session, such as a permission rule or a hook, can [let commands past the limits](https://code.claude.com/docs/en/ship-command-troubleshooting.md#messages-during-a-watch).

### Code that a watch runs on your computer

Code from each of these sources can run on your computer during a watch, with your credentials:

| Source | What happens |
| :- | :- |
| The base branch | To resolve conflicts or bring your branch up to date, Claude merges the base branch into yours, including scripts that run by themselves |
| Other people's pushes to your branch | Claude is instructed to merge them in |
| Programs from your branch, such as your tests | Claude runs them. They can merge or force-push with your credentials. Claude Code checks only the command that starts them, under the session's permission mode |
| Your Claude Code hooks | They run without asking, and may run a file that Claude has edited |
| [`.claude/skills/steward/SKILL.md`](https://code.claude.com/docs/en/pr-steward-pull-requests#save-pr-steward-instructions-for-everyone-in-a-repository) | Claude follows it if your checkout has one. Anyone who can merge to the repository can write that file |

If Claude Code sees that a merge of the base branch or of other people's pushes would change its settings, `.mcp.json`, or git's config files, Claude leaves that merge to you.

### When a watch can lead to a merge

Cases such as these can lead to a merge:

| Case | What happens |
| :- | :- |
| Auto-merge is on for the pull request | GitHub merges once the checks and reviews allow. What Claude does during the watch, such as pushing a fix, can bring that about. To turn it off, run `gh pr merge --disable-auto <number>` in your shell |
| In a terminal session, you type a message while Claude is idle | [Claude Code's limits](#what-claude-code-blocks-during-a-watch) are off while Claude answers your message. They're also off while Claude handles a background task's result that arrives during that time. In auto mode, Claude may then be allowed to merge |
| You send a session that you started in your terminal to the background during the review or the watch, for example by pressing `←` | The watch ends. Work under way can go on there without these limits. To end that work, [stop that session](https://code.claude.com/docs/en/agent-view.md#manage-sessions-from-the-shell) |

### Permission rules and hooks that apply to /ship and /steward

Claude Code runs `/ship`'s own commit, push, and pull request commands itself, [outside the sandbox](https://code.claude.com/docs/en/sandboxing.md#what-runs-outside-the-sandbox). During a watch, when Claude acts without a message from you, it writes its git fetches, merges, commits, and pushes in the form `git -c core.hooksPath=/dev/null push`.

Rules and hooks apply this way, whether they're in your own settings or in managed settings:

| Setting | For `/ship`'s own commit and push | During a watch |
| :- | :- | :- |
| A [deny rule](https://code.claude.com/docs/en/permissions.md#manage-permissions) such as `Bash(git push *)` | `/ship` leaves those steps to you | No watch starts |
| A rule that asks on `Bash(git push *)` | Claude Code doesn't consult it | It [doesn't match](https://code.claude.com/docs/en/permissions.md#bash-rule-limits) that form, so it adds no prompt |
| A rule that asks on `Bash(git *)` | Claude Code doesn't consult it | It matches, and the watch waits at each prompt, including in auto mode |
| Auto mode's check, and tool hooks such as `PreToolUse` | They don't run | They don't apply to the `gh` and `git` commands that Claude Code runs itself, outside the sandbox, for example to read the pull request |
| Git hooks in the repository's hooks folder | They run | They don't run for Claude's fetches, merges, commits, and pushes on those turns |

## Turn off /ship and /steward for your organization

To turn off both commands, set these keys under [`skillOverrides`](https://code.claude.com/docs/en/skills#override-skill-visibility-from-settings) in [managed settings](https://code.claude.com/docs/en/managed-settings.md). `ship-local` is the skill behind `/ship`.

This example turns off both:

```json theme={null}
{
  "skillOverrides": {
    "ship-local": "off",
    "steward": "off"
  }
}
```

To stop `/ship`'s own pushes, put a [deny rule](https://code.claude.com/docs/en/permissions.md#manage-permissions) such as `Bash(git push *)` in managed settings. With that rule, no watch starts.

## Arguments for /ship and /steward

Type an argument after `/ship` or `/steward` at the Claude Code prompt. To combine arguments, put the effort level first, as in `/ship low 41 +my-lint-bot`.

| You type | Commands | What it does |
| :- | :- | :- |
| `low`, `medium`, `high`, `xhigh`, or `max` | `/ship` | Asks for a review at that effort level. The default is `high` |
| `41`, or a pull request's URL | `/ship`, `/steward` | Works on that pull request. For a watch, it has to be your own, with its branch checked out |
| `+botname` | `/ship`, `/steward` | Also reads that bot's comments. Repeat it when you start a watch again |
| `stop` | `/ship`, `/steward` | Ends the watch |
| `terms` | `/ship`, `/steward` | Shows what Claude may do during a watch and what limits it |

## Related resources

* [Troubleshoot `/ship` and `/steward`](https://code.claude.com/docs/en/ship-command-troubleshooting): messages that the commands print, and what to do
* [Review code locally](https://code.claude.com/docs/en/code-review-local.md): the review that `/ship` runs
* [Permission modes](https://code.claude.com/docs/en/permission-modes.md): auto mode and the other permission modes
