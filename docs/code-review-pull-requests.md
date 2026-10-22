> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Read and request reviews on a pull request

> Read Code Review findings on your GitHub pull request, respond to or dismiss them, and request a review with `@claude review`.

Code Review is a managed service that an Owner in your Claude organization turns on for a set of GitHub repositories. Once it's on, Claude reviews pull requests in those repositories and posts its findings as inline comments, a summary in the review body, and a check run named **Claude Code Review**. A review never approves or blocks your pull request, and the check run never concludes as a failure.

An Owner controls [when reviews run](/docs/en/code-review-setup.md#set-when-reviews-run) and [how thorough they are](/docs/en/code-review-setup.md#set-the-default-review-level) for each repository.

> [!NOTE]
>
> If your plan doesn't include Code Review, you can still have Claude review your branch from a Claude Code session: see [Review locally with `/code-review`](/docs/en/code-review-local).

## Severity levels

Claude posts each finding as an inline comment on the lines concerned and marks it with one of three severity levels:

| Marker | Severity | Meaning |
| :- | :- | :- |
| 🔴 | Important | A bug that should be fixed before merging |
| 🟡 | Nit | A minor issue, worth fixing but not blocking |
| 🟣 | Pre-existing | A bug that exists in the codebase but wasn't introduced by this PR |

When the review recorded its reasoning, the finding has a collapsed **Why this was flagged** section. Expand it to read why Claude flagged the issue and how it verified the problem.

To change what Claude flags in your repository or how it ranks severity, see [Customize Code Review](/docs/en/code-review-customize.md).

## Respond to findings

You can merge without responding to a finding, unless your repository's own rules require it. If its branch protection [requires conversation resolution](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-conversation-resolution-before-merging), resolve each finding's thread before you merge.

To clear a finding, resolve its thread or push a fix.

* **Dismiss it without a code change**: resolve the thread yourself on GitHub. Replying alone doesn't dismiss a finding.
* **Fix the issue**: change the code and push. The next review of the pull request resolves its earlier thread when it judges the issue fixed, whether that review runs automatically on your push or you request it.
* **Explain or disagree**: reply to the comment. Claude doesn't respond right away, and a reply doesn't start a review. The next review of the pull request reads the replies on its earlier findings, and can resolve the thread or post one follow-up reply. If the same kind of finding keeps coming back, ask a maintainer to add a rule to [`REVIEW.md`](/docs/en/code-review-customize#choose-what-to-write-in-review-md).

To get that next review without pushing, comment `@claude review` as a [top-level pull request comment](#comment-commands).

## Check run output

The **Details** link on the **Claude Code Review** check run opens the findings in one table sorted by severity, including any finding whose inline comment GitHub didn't accept:

| Severity | File:Line | Issue |
| - | - | - |
| 🔴 Important | `src/auth/session.ts:142` | Token refresh races with logout, leaving stale sessions active |
| 🟡 Nit | `src/auth/session.ts:88` | `parseExpiry` silently returns 0 on malformed input |

A finding that has a line but wasn't posted as an inline comment appears as an annotation in the **Files changed** tab, on the lines concerned. Important findings show in red, nits in yellow, and pre-existing bugs in gray.

The check run concludes as neutral, or as skipped after some pushes that change no files and [keep the earlier result](#when-a-push-keeps-the-earlier-result). It never concludes as a failure, so a finished review doesn't fail a required check. If you don't see findings, or a review didn't run, see [Troubleshoot Code Review](/docs/en/code-review-troubleshooting.md).

### When a push keeps the earlier result

If the check run has one of these titles after you push, Code Review kept the result of an earlier review instead of starting a new one:

* **Code review skipped — no new changes**: no [Important](#severity-levels) finding from the earlier review is still open, so you don't need a new review
* **Code review not repeated — earlier findings still open**: to start a new review, push a fix for an open Important finding, or [resolve its thread](#respond-to-findings) and push again

On github.com, Code Review can keep a result when both of these hold:

* The pull request still adds and removes the same lines, as after an empty commit, a clean merge of the base branch, or a clean rebase
* Nobody has resolved an Important finding's thread since that review

To get a review without a code change, comment [`@claude review`](#comment-commands) or click **Re-run** on the check run.

### Read the result from a script

To gate a merge or post a summary from your own CI, parse the last line of the Details text with `gh` and jq. That line is an HTML comment that holds the severity counts as JSON:

```text theme={null}
<!-- bughunter-severity: {"nit":1,"normal":2,"pre_existing":0} -->
```

The lines above it can include file names from the pull request. If you parse the text your own way, take the counts from the last line only, as the command in these steps does.

**1. Find the check run ID**

From your shell, list the commit's check runs and take the `id` of the `Claude Code Review` run. Replace `OWNER` and `REPO` with your repository owner and name, and `<commit-sha>` with the pull request's head commit:

```bash theme={null}
gh api repos/OWNER/REPO/commits/<commit-sha>/check-runs --jq '.check_runs[] | {id, name}'
```

If the commit has had more than one `Claude Code Review` run, such as after a **Re-run**, GitHub lists only the newest.

**2. Read the severity counts**

Read the counts from the check run's `output.text` field, which holds the Details text. Replace `CHECK_RUN_ID` with the ID:

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID --jq '
  (.output.text | split("\n") | last
    | scan("^<!-- bughunter-severity: (.*) -->$")[0] | fromjson)?
  // error("no severity line")'
```

This prints a JSON object with a count per severity and its keys in alphabetical order, for example `{"nit": 1, "normal": 2, "pre_existing": 0}`. Except on a check run that [kept an earlier result](#when-a-push-keeps-the-earlier-result), the counts include findings from earlier reviews of the pull request whose threads are still open.

Under the title `Code review skipped — no new changes`, the counts leave out nits and pre-existing findings from earlier reviews that are still open. No Important finding from the earlier review is still open then.

**3. Act on the result**

Have your script handle these cases in order:

* **The title starts with `Code review not repeated`**: Code Review [kept an earlier result](#when-a-push-keeps-the-earlier-result) whose Important findings are still open, and the check run has no severity line. Read the title before the counts, with `gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID --jq .output.title`. Fail the job if you want to gate the merge.
* **The title ends with `no new changes`**: let the job pass without reading the counts
* **`normal` is above zero**: fail the job if you want to gate the merge. The `normal` key holds the count of Important findings, so Claude found at least one bug worth fixing before merge. To print only that count, add `| .normal` before the closing single quote.
* **The line is missing**: the command prints an error that contains `no severity line` instead of counts, and exits with a non-zero status. Treat that as no verdict rather than as zero findings. A check run for a review that failed, timed out, was canceled, or was superseded by a newer one has no such line, and some completed reviews have none either.

## Request a review

If your pull request is a draft or comes from a fork, automatic reviews skip it, so [request the review with a comment command](#review-drafts-and-pull-requests-from-forks). To get a review on your pull request, do one of these:

* **Open it or mark it ready**: in a repository set to **Once after PR creation** or **After every push**, a review starts when you open or reopen the pull request, or mark a draft ready for review.
* **Comment a command**: post [`@claude review`](#comment-commands) on the pull request.
* **Push a commit**: a push starts a review in a repository set to **After every push**, or on a pull request you subscribed with `@claude review always`. If your pull request still adds and removes the same lines after the push, Code Review can [keep the earlier result](#when-a-push-keeps-the-earlier-result) instead.
* **Click Re-run**: after a review fails or times out on a pull request that isn't from a fork, [run it again](/docs/en/code-review-troubleshooting.md#retrigger-a-failed-or-timed-out-review) from the check run. On a pull request that isn't from a fork, you can also click **Re-run** after a push that [kept the earlier result](#when-a-push-keeps-the-earlier-result).
* **Wait for the automatic retry**: a review whose session was interrupted is retried once automatically. The [check run's summary](/docs/en/code-review-troubleshooting.md#retrigger-a-failed-or-timed-out-review) says when that's happening.

### Comment commands

Post one of these commands as a comment on the pull request:

| Command | What it does | When to use it |
| :- | :- | :- |
| `@claude review` | Starts a single review without subscribing the PR to future pushes | You want one review now, such as on a pull request in a repository set to **Manual**, or another review right away in the other modes |
| `@claude review always` | Starts a review and subscribes the PR to push-triggered reviews going forward | You want subsequent pushes to start reviews, such as on a high-priority PR in a repository set to **Manual** |
| `@claude review once` | Same as `@claude review`: starts a single review without subscribing | The same cases as `@claude review` |
| `@claude review stop` | Ends the PR's subscription to push-triggered reviews, without starting a review or canceling one that's already running. Claude replies with a comment instead of a check run. | You subscribed a PR with `@claude review always` in a repository set to **Manual** or **Once after PR creation**, and no longer want each push to start a review |
| `@claude review off` or `@claude review pause` | Same as `@claude review stop` | The same cases as `@claude review stop` |

In a repository set to **After every push**, you can't stop reviews with a comment, because pushes there start reviews with or without a subscription. To stop pushes from starting reviews on one pull request there, convert it to a [draft](#review-drafts-and-pull-requests-from-forks). When you mark it ready for review again, a review starts.

For any comment command to take effect, all of these conditions have to hold:

* Post it as a new top-level pull request comment, not an inline comment on a diff line and not the body of a review. Editing an earlier comment doesn't count.
* Put the whole command on one line at the start of the comment. Other text can follow it. If `always` or `stop` is misspelled or on a later line, Claude reads the comment as a plain `@claude review` and starts a single review. Capitalization doesn't matter.
* You need write, maintain, or admin permission on the repository. Claude checks this with GitHub for each person who comments, and comments from bots don't start reviews.
* The pull request must be open.

When a command that starts a review is accepted, a **Claude Code Review** check run appears on the pull request with the title **Code review queued...**. The title changes to **Code review in progress...** when the review starts. Claude may also react to your comment with 👀, but that reaction can appear when no review starts, so look for the check run instead.

If a review is already running on the pull request's latest commit, a new request doesn't start a second one.

> [!NOTE]
>
> Before a July 2026 update, `@claude review` subscribed the PR to push-triggered reviews. If you relied on that behavior, comment `@claude review always` instead.

### What a later review covers

A later review that starts on its own, such as after a push, focuses on what changed since the last review and posts fewer nits and pre-existing findings. Its summary counts what it left out, in a line that ends "found and not posted" or "outside the scope of this re-review and not posted."

To get a review that leaves none of these out, comment [`@claude review`](#comment-commands). It covers the whole pull request again.

### Review drafts and pull requests from forks

Automatic reviews skip both of these, so request the review with a comment command:

* **Draft pull requests**: a comment command runs on a draft, so you can request a review before you mark the pull request ready. Pushes to a draft don't start reviews, even after `@claude review always`. The subscription takes effect once you mark the pull request ready.
* **Pull requests from forks**: Claude doesn't review a pull request from a fork automatically, regardless of the repository's **Review runs** setting. To start one, comment `@claude review` on the pull request. The [conditions for comment commands](#comment-commands) still apply, and the write access you need is to the base repository, not the fork.

On a pull request from a fork, `@claude review always` works too, but doesn't subscribe the pull request to reviews on later pushes. Clicking **Re-run** on the check run doesn't start a review there.

### Use Code Review alongside the Claude Code GitHub Action

If the repository also runs the [Claude Code GitHub Action](/docs/en/github-actions.md) in interactive mode with its default `@claude` trigger phrase, an `@claude review` comment starts the Action as well. To keep the two apart, set the Action's `trigger_phrase` input to a different phrase.

## Related resources

* [Troubleshoot Code Review](/docs/en/code-review-troubleshooting.md): a review that didn't start, failed, or was skipped for budget
* [Code Review](/docs/en/code-review.md): what the service is and how a review runs
* [Set up Code Review](/docs/en/code-review-setup.md): for Owners, turn on Code Review and choose when reviews run and at what level
* [Customize Code Review](/docs/en/code-review-customize.md): change what Claude flags with `REVIEW.md` and `CLAUDE.md`
* [Code Review costs and usage](/docs/en/code-review-costs.md): how reviews are billed and where the spend limit is set
* [Review locally with `/code-review`](/docs/en/code-review-local): run a review of your branch from a Claude Code session
