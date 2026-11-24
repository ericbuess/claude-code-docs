> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Work with PR Steward on a pull request

> See what PR Steward adds to your GitHub pull request, give it instructions, start or stop it with a comment or a label, and limit what it does for you

[PR Steward](https://code.claude.com/docs/en/pr-steward.md) is an agent that works on the GitHub pull requests that you open, in repositories where it's on. It pushes commits to address review feedback, and attempts to fix failing checks and resolve merge conflicts.

You can [tell it what to work on](#change-what-pr-steward-does) or [turn it off for yourself](#turn-off-or-limit-pr-steward-on-all-your-pull-requests). To stop it on one pull request, remove the `claude-pr-steward-watching` label, or comment `@claude stop`.

## What PR Steward adds to a pull request

On github.com, PR Steward posts its comments as `claude[bot]`, the account of the [Claude GitHub App](https://github.com/apps/claude).

PR Steward adds these labels, comments, and commits to a pull request:

![Diagram of what PR Steward leaves on a pull request: the claude-pr-steward-watching label while PR Steward watches, a comment headed Claude PR Steward when it first starts, progress comments before and after a piece of work, and ordinary commits on your branch by Claude.](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/pr-steward-pull-request.svg?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=2c76cf9593743c0a05718e7a90c45796)

PR Steward adds each one at these times:

| What PR Steward adds | When |
| :- | :- |
| The `claude-pr-steward-watching` label | While it watches the pull request |
| The `claude-pr-steward-is-working` label | While it works |
| A comment headed **Claude PR Steward** | When it first starts on the pull request |
| A progress comment | Before and after a piece of work |
| Commits whose author and committer are `Claude <noreply@anthropic.com>` | When it pushes a fix |

The progress comment after a push names the commits to revert if you want to [undo the push](#undo-a-fix-that-pr-steward-pushed).

### Example of a fix for a failing check

In this example, you open a pull request in a repository where PR Steward starts by itself, and a test of the code that you changed fails. Claude writes the progress comments, so their wording varies.

1. **PR Steward starts**: it adds the `claude-pr-steward-watching` label and posts a first comment. The emoji and the opening words change from one pull request to the next, and the rest reads like this:

   ```text wrap theme={null}
   🛠️ Claude PR Steward — On it. I'll chase down CI failures, work through review comments, and push fixes until it's green. Ask me anything in a comment and I'll answer or take action. I'll check for a steward skill at .claude/skills/steward/SKILL.md for any repo-specific behavior I should follow.

   Remove the claude-pr-steward-watching label any time to take over.

   React with 👍 or 👎 to provide feedback · Settings
   ```

2. **The test fails**: PR Steward adds the `claude-pr-steward-is-working` label and says what it plans to do:

   ```text wrap theme={null}
   The unit-tests check failed on test_parse_date. I'll find the cause and push a fix.

   – Claude PR steward · Settings
   ```

3. **PR Steward pushes a fix**: PR Steward can wait before it pushes, for example while other checks are still running, and says so in a comment. Then a commit by `Claude <noreply@anthropic.com>` appears on your branch. A second progress comment says what changed and how to undo it:

   ```text wrap theme={null}
   Pushed a1b2c3d: parse_date now accepts a date with no time zone, which is the case that test_parse_date covers. To undo it, revert a1b2c3d, or remove the claude-pr-steward-watching label to stop me entirely.

   – Claude PR steward · Settings
   ```

4. **The work ends**: PR Steward removes the `claude-pr-steward-is-working` label and continues to watch the pull request

## Change what PR Steward does

PR Steward starts from [default instructions](#default-instructions-for-pr-steward) on how to handle failing checks, review comments, and the base branch. You can change what it does for one pull request, for every pull request that you open, or for a whole repository:

* **For one pull request that you opened**: [start a comment with `@claude`](#give-pr-steward-instructions-in-a-comment) on that pull request
* **For every pull request that you open**: in your settings on claude.ai, [turn it off or limit it](#turn-off-or-limit-pr-steward-on-all-your-pull-requests), [choose what it works on](#choose-what-pr-steward-works-on), or [enter instructions](#save-pr-steward-instructions-for-every-pull-request-you-open)
* **For everyone's pull requests in a repository**: [save a file at `.claude/skills/steward/SKILL.md`](#save-pr-steward-instructions-for-everyone-in-a-repository) in that repository

### Default instructions for PR Steward

PR Steward's default instructions are instructions to Claude, so they describe what PR Steward aims to do.

With no instructions from you, PR Steward follows defaults such as these:

| Work | By default |
| :- | :- |
| Failing checks | Fixes and pushes when the failure is in code that the pull request touches |
| Flaky checks | Re-runs a failed job once, when the job failed before any test ran or passed earlier on the same commit |
| Base branch | Merges the base branch into yours when there's a conflict. Can also merge it when your branch is behind |
| Lockfiles and generated files | Regenerates them |
| Small review requests, such as a rename or an added test | Pushes the change and resolves the thread |
| Large or design-level review requests | Replies, and doesn't push or resolve the thread, unless the reviewer says which change to make |
| Code Review's optional findings | Replies and resolves the thread. Doesn't push for these alone |
| Choice of approach | Picks one itself, and doesn't ask you which to take |

To change most of these defaults for everyone's pull requests in a repository, [save instructions at `.claude/skills/steward/SKILL.md`](#save-pr-steward-instructions-for-everyone-in-a-repository) in that repository.

### Give PR Steward instructions in a comment

On a pull request that you opened, start a comment with `@claude` and say what you want.

This comment asks PR Steward to fix one kind of failure:

```text theme={null}
@claude only fix the lint failures. I'm still working on the tests.
```

### Turn off or limit PR Steward on all your pull requests

Go to [**PR Steward**](https://claude.ai/settings/claude-code#pr-steward) in **Settings > Code** on claude.ai and select how much PR Steward does on the pull requests that you open. To change the setting, you need a [connected GitHub account](https://code.claude.com/docs/en/web-quickstart.md#connect-github).

| Option | What PR Steward does on your pull requests |
| :- | :- |
| **Off** | Starts only when you add the `claude-pr-steward-watching` label or comment `@claude steward` yourself |
| **Only when tagged** | Starts only when you or a teammate with write access adds the `claude-pr-steward-watching` label or comments `@claude steward` |
| **Act on its own** | Starts on each [eligible pull request](https://code.claude.com/docs/en/pr-steward.md#when-pr-steward-starts), including in repositories that an Owner [set to **Manual**](https://code.claude.com/docs/en/pr-steward-setup.md#choose-when-pr-steward-starts-in-each-repository) |
| **Customize** | Follows each repository's own setting for when to start. You [choose what it works on](#choose-what-pr-steward-works-on) |

Before you choose an option, the settings page shows **Act on its own** as selected. Until you choose one, PR Steward follows each repository's own setting.

PR Steward reads your settings when it starts on a pull request, so a change applies to later starts.

### Choose what PR Steward works on

To tell PR Steward what to work on, for every pull request that you open, use the toggles in your settings. A repository's `.claude/skills/steward/SKILL.md` can say something else, so see [which instructions take priority](#which-pr-steward-instructions-take-priority).

1. Go to [**PR Steward**](https://claude.ai/settings/claude-code#pr-steward) in **Settings > Code** on claude.ai
2. For **How much should Steward do on its own?**, select [**Customize**](#turn-off-or-limit-pr-steward-on-all-your-pull-requests)
3. Turn off the toggle for each thing that you don't want PR Steward to do. Each toggle is on until you turn it off:
   * **Failing CI and merge conflicts**
   * **Issues found by Code Review and other review bots**
   * **Comments from human reviewers**
     * **Reply to reviewers and resolve their threads**, which needs **Comments from human reviewers** on
   * **Include my draft PRs**

With **Customize** selected, the settings look like this:

![PR Steward settings with Customize selected, showing switches for failing CI and merge conflicts, review bot issues, human reviewer comments, replies to reviewers, and draft PRs, and a menu for updating from the base branch.](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/pr-steward-customize.png?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=10695821d6e7766ee94cdb5706c1319f)

> [!NOTE]
>
> **Customize** also changes when PR Steward starts: it follows each repository's own setting. If you had **Off** or **Only when tagged** selected before, it can then start by itself.

While **Include my draft PRs** is on, PR Steward works on your drafts in repositories that an Owner set to include drafts. PR Steward also works on your drafts in a repository that an Owner set to **Manual**, when someone asks for it on the draft. While it's off, PR Steward doesn't start on your drafts.

While **Failing CI and merge conflicts** is on, you can also say when PR Steward merges the base branch into yours. Set **Updating my branch from the base branch** to **Whenever my branch falls behind**, **Only when there is a conflict**, or **Never, I update it myself**.

### Save PR Steward instructions for every pull request you open

To give PR Steward the same instructions on every pull request that you open, go to [**PR Steward**](https://claude.ai/settings/claude-code#pr-steward) in **Settings > Code** on claude.ai. Under **My instructions for Steward**, enter up to 1,000 characters.

These instructions ask for small commits and no replies to reviewers:

```text theme={null}
Keep commits small.
Don't reply to reviewers for me.
```

### Save PR Steward instructions for everyone in a repository

To set how PR Steward behaves for everyone in a repository, save a file at `.claude/skills/steward/SKILL.md` and merge it to the default branch.

This example tells PR Steward which work to take on, and how to handle one file and one flaky check:

```markdown theme={null}
---
name: steward
description: House rules for PR Steward in this repository
user-invocable: false
disable-model-invocation: true
---

- Work on failing checks, merge conflicts, and Important findings from Code Review.
- Leave comments from human reviewers to the author.
- Regenerate `package-lock.json` with `npm install`. Don't edit it directly.
- The `e2e-nightly` check is flaky. Re-run it once before you look for a cause.
```

To check that PR Steward follows the file:

1. Open a test pull request after the file reaches the default branch.
2. If the `claude-pr-steward-watching` label doesn't appear by itself, comment `@claude steward`.
3. Once the label is on, have a teammate leave a review comment.

The example leaves comments from human reviewers to the author, so PR Steward should push no fix for that review comment.

PR Steward also reads instructions from files such as `CLAUDE.md`, `.claude/CLAUDE.md`, `.claude/rules/`, and `AGENTS.md` at the repository's root. It reads them from the default branch.

> [!NOTE]
>
> The `/ship` and `/steward` commands in Claude Code read the same file. During a watch, Claude [follows the copy in your checkout](https://code.claude.com/docs/en/ship-command.md#save-instructions-for-watches-in-a-repository).

### Which PR Steward instructions take priority

Your settings, the repository's file, and your comments can disagree. PR Steward settles that this way:

* **Whether PR Steward starts**: [the option that you select](#turn-off-or-limit-pr-steward-on-all-your-pull-requests) and [**Include my draft PRs**](#choose-what-pr-steward-works-on) are checked before PR Steward reads any instructions
* **What PR Steward does after it starts**: where your own settings and the repository's [`.claude/skills/steward/SKILL.md`](#save-pr-steward-instructions-for-everyone-in-a-repository) disagree, that file applies. Your comments on the pull request override your own settings there, and a comment that asks PR Steward to stop or hold off also overrides that file

## Start or stop PR Steward

Use a comment or a label to start or stop PR Steward on one pull request. To turn it off or limit it on every pull request that you open, [change your settings](#turn-off-or-limit-pr-steward-on-all-your-pull-requests).

### Start or stop PR Steward on one pull request

To stop PR Steward on a pull request, remove the `claude-pr-steward-watching` label, or comment `@claude stop`.

To start or stop PR Steward with a comment, put one of these commands at the start of a top-level comment on an open pull request:

| Comment | What it does |
| :- | :- |
| `@claude stop` | Stops PR Steward. Make the command the whole comment |
| `@claude steward stop` or `@claude unwatch` | Stops PR Steward |
| `@claude steward` | Starts PR Steward |
| `@claude babysit`, `@claude watch`, `@claude babysit stop`, `@claude watch stop` | Other spellings of the start and stop commands |

After a stop command, PR Steward removes its labels and confirms in a comment. After you remove the label, it stops without a comment.

PR Steward stays stopped when you push or comment later. To restart it, comment `@claude steward` or add the label again. If it doesn't start, see [PR Steward didn't start on a pull request](https://code.claude.com/docs/en/pr-steward-troubleshooting.md#pr-steward-didn’t-start-on-a-pull-request).

### Undo a fix that PR Steward pushed

After a revert, PR Steward can make the same fix again, so take these steps in order:

1. **Hold PR Steward back**: [stop it](#start-or-stop-pr-steward-on-one-pull-request).
2. **Revert the commits**: revert the commits by `Claude <noreply@anthropic.com>` that you don't want.

### Keep PR Steward off a pull request from the start

Include this marker in the description when you open the pull request:

```html theme={null}
<!-- claude-pr-steward-disable -->
```

To start PR Steward on that pull request later, remove the marker first.

### Who can start and stop PR Steward

Starting or stopping PR Steward takes this access to the repository:

| Action | Who can do it |
| :- | :- |
| Start or stop PR Steward with a comment | A person with write access to the repository |
| Start PR Steward by adding the `claude-pr-steward-watching` label | A person with write access |
| Stop PR Steward by removing the label | Any person GitHub allows to remove labels |

## Related resources

* [PR Steward](https://code.claude.com/docs/en/pr-steward.md)
* [Troubleshoot PR Steward](https://code.claude.com/docs/en/pr-steward-troubleshooting.md)
* [What PR Steward can access](https://code.claude.com/docs/en/pr-steward-security.md)
* [Set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md)
