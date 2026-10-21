> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshoot Code Review

> Fix a Code Review that didn't start, failed, or was skipped for budget, find missing findings, and resolve setup and `REVIEW.md` problems.

When [Code Review](/docs/en/code-review) doesn't do what you expect on a pull request, start with the **Claude Code Review** check run. Its title says how far the review got.

## Check how far the review got

Find the **Claude Code Review** check run on your pull request, then match its title to one of these common ones:

| Check run title | What it means | What to do |
| :- | :- | :- |
| **Code review queued...** or **Code review in progress...** | The review hasn't finished | Wait for the title to change |
| **Code review found no issues** | The review finished and found nothing to flag | Nothing |
| A title that says issues were found | The review finished with findings | If you don't see them on the diff, see [Find issues that aren't showing as inline comments](#find-issues-that-aren’t-showing-as-inline-comments) |
| **Code review skipped — no new changes** | An automatic review didn't run on your latest push | To get a review anyway, comment `@claude review` |
| **Code review failed** or **Code review timed out** | The review didn't finish | To run it again, see [Retrigger a failed or timed-out review](#retrigger-a-failed-or-timed-out-review) |
| **Code review declined** | The review didn't run | Read the check run's summary. If it names a budget or a spend limit, see [Review didn't run and the PR shows a budget message](#review-didn’t-run-and-the-pr-shows-a-budget-message) |
| No check run | No review started | Comment `@claude review`. If no check run appears after that, see [A comment command didn't start a review](#a-comment-command-didn’t-start-a-review) |

## A review didn't start

Check these cases when no **Claude Code Review** check run appears, or when Claude posts a comment saying the review was skipped.

### A comment command didn't start a review

After you comment `@claude review`, look for a **Claude Code Review** check run titled **Code review queued...** or **Code review in progress...** on the pull request. An 👀 reaction on your comment doesn't confirm a review is coming. If no check run appears, check for each of these causes:

* **Code Review isn't on for this repository**: Claude posts no comment and no check run in response to the command. Ask an Owner to [add the repository](/docs/en/code-review-setup#add-more-repositories).
* **The comment doesn't meet a condition**: it was an inline comment or a review body rather than a new top-level comment, or the command wasn't at the start of the comment. Editing an earlier comment instead of posting a new one doesn't count either, and the pull request has to be open. See the [conditions for comment commands](/docs/en/code-review-pull-requests#comment-commands) and post a new comment that meets them.
* **You don't have write access**: you need write, maintain, or admin permission on the repository. On a pull request from a fork, the permission that counts is on the base repository. Unless the pull request is yours, Claude can reply with a [tip](/docs/en/code-review-setup#turn-tip-comments-on-or-off): "No review was started: manual reviews can only be requested by someone with write access to this repository." Ask someone with write access to comment instead.
* **The budget ran out**: Claude posts a comment that begins with "⚠️ Code review skipped". See [Review didn't run and the PR shows a budget message](#review-didn’t-run-and-the-pr-shows-a-budget-message).

### Review didn't run and the PR shows a budget message

When your organization's budget can't cover a review, Code Review skips the review and Claude posts a comment on the pull request that begins with "⚠️ Code review skipped". In some of these cases a check run titled **Code review declined** also appears.

The comment links [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage), where an admin restores the budget. Its wording tells you which limit was reached:

* **"has reached its monthly code review spending cap"**: the [monthly spend limit for Code Review](/docs/en/code-review-costs#limit-your-spend) was reached. Reviews resume at the start of the next billing period. To get them sooner, ask an admin to raise the limit.
* **"has no extra usage available to pay for this review"**: your organization's [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) balance is empty, or its overall monthly spend limit was reached. Ask an admin to add usage credits or raise that limit.
* **"is too low to start another review"**: what's left of the budget or balance is less than the expected cost of one review. Ask an admin to raise the limit or add usage credits.

After the budget is restored, comment `@claude review` on the pull request to get the review that was skipped. The [conditions for comment commands](/docs/en/code-review-pull-requests#comment-commands) apply, so the commenter needs write access.

## Retrigger a failed or timed-out review

If the check run's summary says "The review session was interrupted before it could finish. A new review of this commit has been queued automatically.", you don't need to do anything. That review is retried once automatically.

Otherwise, when the check run's title is **Code review failed** or **Code review timed out**, run the review again with a comment or a re-run:

* **Comment `@claude review`**: post it as a top-level comment on the pull request. This starts a fresh review without subscribing the pull request to future pushes.
* **Click Re-run**: if the pull request isn't [from a fork](/docs/en/code-review-pull-requests#review-drafts-and-pull-requests-from-forks), click **Re-run** on the **Claude Code Review** check in GitHub's **Checks** tab. The re-run covers the pull request's current head commit and doesn't subscribe the pull request either.

## Find issues that aren't showing as inline comments

If the check run title says issues were found but you don't see inline review comments on the diff, look in these other locations where findings are surfaced:

* **Check run Details**: click **Details** next to the **Claude Code Review** check in the **Checks** tab. The severity table lists findings with their file, line, and summary regardless of whether the inline comment was accepted.
* **Files changed annotations**: open the **Files changed** tab on the PR. A finding that has a line but wasn't posted as an inline comment appears there as an annotation on the lines concerned.
* **Review body**: findings that have no inline location, or that fall outside the current diff, appear under an **Additional findings** heading in the review body.

## The check run mentions REVIEW\.md

These are three of the messages a check run can carry about `REVIEW.md`:

* **"This review applied the repository's review instructions (REVIEW\.md) from its default branch, which is not protected against direct pushes."**: the review read the root file only. See [Which branch REVIEW.md is read from](/docs/en/code-review-customize#which-branch-review-md-is-read-from) for what protecting the branch changes.
* **"were not applied to this review: branch protection could not be confirmed"**: the review read no `REVIEW.md`.
* **"they link to a file this pull request modifies, or carry more links than the review checks"**: the review skipped the root `REVIEW.md`, or the number of subdirectory `REVIEW.md` files the message gives. Check the skipped file for each cause. For the root `REVIEW.md`, check the [files it includes](/docs/en/code-review-customize#include-other-files-in-review-md) too:
  * **Too many links**: it carries more than 64 Markdown links. Cut links to [64 or fewer](/docs/en/code-review-customize#include-other-files-in-review-md).
  * **A link the review can't parse**: it has a malformed Markdown link. Fix or remove the link.
  * **A link to a changed file**: it links to a file or folder this pull request changes, and the review couldn't leave out only the lines with that link. Write the rule in `REVIEW.md` itself.

## Setup problems

These cases come up for an Owner while [setting up Code Review](/docs/en/code-review-setup).

### A repository isn't listed in Add a repository

Search for the repository by name first, because the dialog doesn't load a long list in full. The dialog lists a repository only if the Claude GitHub App can access it. Click **Install GitHub App** and give the app access to the repository. When no repositories are listed, **Install GitHub App** is a button in the dialog. Otherwise, it's at the bottom of the dialog's GitHub organization filter menu.

### No check run appears on the test pull request

Confirm that **Allow code review** is on, that the repository is listed under **Repositories** in the **Code review** section, and that the Claude GitHub App has access to it. Automatic reviews skip draft pull requests, and a repository set to **Manual (@claude review)** needs an `@claude review` comment to start the first review.

## Related resources

* [Read and request reviews on a pull request](/docs/en/code-review-pull-requests): what the findings and the check run mean, and the comment commands
* [Set up Code Review](/docs/en/code-review-setup): for Owners, turn on Code Review and manage repositories
* [Code Review costs and usage](/docs/en/code-review-costs): the spend limits behind a budget message
* [Customize Code Review](/docs/en/code-review-customize): which copy of `REVIEW.md` a review reads
