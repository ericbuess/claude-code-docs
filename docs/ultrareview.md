> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Find bugs with ultrareview

> Run a deep, multi-agent code review in the cloud with /ultrareview to find and verify bugs before you merge.

<Note>
  Ultrareview is a research preview feature available in Claude Code v2.1.86 and later. The feature, pricing, and availability may change based on feedback.
</Note>

Ultrareview is a deep code review that runs on Claude Code on the web infrastructure. When you run `/ultrareview`, Claude Code launches a fleet of reviewer agents in a remote sandbox to find bugs in your branch or pull request.

Compared to a local `/review`, ultrareview offers:

* **Higher signal**: every reported finding is independently reproduced and verified, so the results focus on real bugs rather than style suggestions
* **Broader coverage**: many reviewer agents explore the change in parallel, which surfaces issues that a single-pass review can miss
* **No local resource use**: the review runs entirely in a remote sandbox, so your terminal stays free for other work while it runs

Ultrareview requires authentication with a Claude.ai account because it runs on Claude Code on the web infrastructure. If you are signed in with an API key only, run `/login` and authenticate with Claude.ai first. Ultrareview is not available when using Claude Code with Amazon Bedrock, Google Cloud Vertex AI, or Microsoft Foundry, and it is not available to organizations that have enabled Zero Data Retention.

## Run ultrareview from the CLI

Start a review from any git repository in the Claude Code CLI.

```text theme={null}
/ultrareview
```

Without arguments, ultrareview reviews the diff between your current branch and the default branch, including any uncommitted and staged changes in your working tree. Claude Code bundles the repository state and uploads it to a remote sandbox for the review.

To review a GitHub pull request instead, pass the PR number.

```text theme={null}
/ultrareview 1234
```

In PR mode, the remote sandbox clones the pull request directly from GitHub rather than bundling your local working tree. PR mode requires a `github.com` remote on the repository.

<Tip>
  If your repository is too large to bundle, Claude Code prompts you to use PR mode instead. Push your branch and open a draft PR, then run `/ultrareview <PR-number>`.
</Tip>

Before launching, Claude Code shows a confirmation dialog with the review scope (including the file and line count when reviewing a branch), your remaining free runs, and the estimated cost. After you confirm, the review continues in the background and you can keep using your session. The command runs only when you invoke it with `/ultrareview`; Claude does not start an ultrareview on its own.

## Pricing and free runs

Ultrareview is a premium feature that bills against extra usage rather than your plan's included usage.

| Plan                | Included free runs    | After free runs                                                                                            |
| ------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------- |
| Pro                 | 3 free runs, one-time | billed as [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Max                 | 3 free runs, one-time | billed as [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Team and Enterprise | none                  | billed as [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |

Pro and Max subscribers receive three free ultrareview runs to try the feature. These three runs are a one-time allotment per account and do not refresh. After you use them, each review is billed to extra usage and typically costs \$5 to \$20 depending on the size of the change.

Because ultrareview always bills as extra usage outside the free runs, your account or organization must have extra usage enabled before you can launch a paid review. If extra usage is not enabled, Claude Code blocks the launch and links you to the billing settings where you can turn it on. You can also run `/extra-usage` to check or change your current setting.

## Track a running review

A review typically takes 5 to 10 minutes. The review runs as a background task, so you can keep working in your session, start other commands, or close the terminal entirely.

Use `/tasks` to see running and completed reviews, open the detail view for a review, or stop a review that is in progress. Stopping a review archives the cloud session, and partial findings are not returned. When the review finishes, the verified findings appear as a notification in your session. Each finding includes the file location and an explanation of the issue so you can ask Claude to fix it directly.

## How ultrareview compares to /review

Both commands review code, but they target different stages of your workflow.

|          | `/review`                      | `/ultrareview`                                                |
| -------- | ------------------------------ | ------------------------------------------------------------- |
| Runs     | locally in your session        | remotely in a cloud sandbox                                   |
| Depth    | single-pass review             | multi-agent fleet with independent verification               |
| Duration | seconds to a few minutes       | roughly 5 to 10 minutes                                       |
| Cost     | counts toward normal usage     | free runs, then roughly \$5 to \$20 per review as extra usage |
| Best for | quick feedback while iterating | pre-merge confidence on substantial changes                   |

Use `/review` for fast feedback as you work. Use `/ultrareview` before merging a substantial change when you want a deeper pass that catches issues a single review might miss.

## Related resources

* [Claude Code on the web](/en/claude-code-on-the-web): learn how remote sessions and cloud sandboxes work
* [Plan complex changes with ultraplan](/en/ultraplan): the planning counterpart to ultrareview for upfront design work
* [Manage costs effectively](/en/costs): track usage and set spending limits
