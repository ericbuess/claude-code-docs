> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Find bugs with ultrareview

> Run a deep, multi-agent code review in the cloud with /code-review ultra to find and verify bugs before you merge.

<Note>
  Ultrareview is a research preview feature. The feature, pricing, and availability may change based on feedback. The command is `/code-review ultra`. When ultrareview is available to your account, `/ultrareview` is an alias.
</Note>

Ultrareview is a deep code review that runs on Claude Code on the web infrastructure. When you run `/code-review ultra`, Claude Code launches a fleet of reviewer agents in a remote sandbox to find bugs in your branch or pull request.

Compared to a local `/code-review` or `/review`, ultrareview offers:

* **Higher signal**: every reported finding is independently reproduced and verified, so the results focus on real bugs rather than style suggestions
* **Broader coverage**: a larger fleet of reviewer agents explores the change in parallel, which surfaces issues that a local review can miss
* **No local resource use**: the review runs entirely in a remote sandbox, so your terminal stays free for other work while it runs

Ultrareview requires authentication with a claude.ai account because it runs on Claude Code on the web infrastructure. If you are signed in with an API key only, run `/login` and authenticate with claude.ai first. Ultrareview is not available when using Claude Code with Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, and it is not available to organizations that have enabled Zero Data Retention. When ultrareview is not available, `/code-review ultra` runs a local review in your session instead.

## Run ultrareview from the CLI

Start a review from any git repository:

```text theme={null}
/code-review ultra
```

Without arguments, ultrareview reviews the diff between your current branch and the default branch, including uncommitted and staged changes. For a branch review, Claude Code bundles the repository state and uploads it to a remote sandbox; when you [review a pull request](#review-a-pull-request), Claude Code uploads nothing from your machine.

Before launching, Claude Code shows a confirmation dialog with the review scope, your remaining free runs, and the estimated cost; for a branch review, the scope includes the file and line count. After you confirm, the review continues in the background while you keep using your session.

The command runs only when you invoke it with `/code-review ultra`; Claude doesn't start an ultrareview on its own.

### Review against a different base

To compare against a base other than the default branch, pass the branch name. This example reviews your current branch against `develop` instead:

```text theme={null}
/code-review ultra develop
```

The base branch doesn't need to exist in your local clone; Claude Code fetches it from `origin`. If the name has a typo, Claude Code suggests the closest branch name in the error.

### Review a pull request

To review a GitHub pull request instead of a local branch, pass the PR number:

```text theme={null}
/code-review ultra 1234
```

The command also accepts `#1234`, `PR 1234`, and pasted PR URLs; a pasted URL must point to the repository in your current directory.

In PR mode, the remote sandbox clones the pull request directly from the host rather than bundling your local working tree. PR mode works with repositories on `github.com` and on [GitHub Enterprise Server](/docs/en/github-enterprise-server) instances that an Owner has connected to Claude Code.

### Pass a request in plain words

On Claude Code v2.1.218 or later, you can also describe what you're working on in plain words:

```text theme={null}
/code-review ultra check my auth changes
```

The review still covers your current branch, the same scope as running with no argument. Claude keeps your text as a note, shown in the launch dialog, and relates the findings to it when they arrive.

Claude Code treats your text as a note only when it has more than one word and isn't a branch name or PR reference. It reads a single word as a branch name or PR reference, so a mistyped branch name gets the closest-branch error from [Review against a different base](#review-against-a-different-base) instead of launching with a note. If your text combines a PR reference with other words, such as `check PR 123 again`, Claude Code doesn't launch either; it asks you to rerun with the PR number alone to review that PR, or without the reference to review your current branch.

<Tip>
  If your repository is too large to bundle, Claude Code prompts you to use PR mode instead. Push your branch and open a draft PR, then run `/code-review ultra <PR-number>`.
</Tip>

### Diff limits and fallbacks

Ultrareview checks the diff before any review work runs and tells you when it can't review it as-is:

* **Diff too large**: a branch review can include up to 500 changed files and 8,000 changed lines by default. The exact values can change, and the [refusal](/docs/en/errors#diff-is-too-large-for-ultrareview) names the ones in effect, the size of your diff, and the files with the most changed lines. Claude Code refuses a too-large pull request the same way, naming its file and line counts but not the per-file breakdown
* **Nothing to review**: when the diff against the base is empty, Claude Code says so and suggests staging or committing local edits, or passing a different base
* **No merge base**: when your branch shares no history with the base branch, Claude Code offers to review every tracked file in the repository instead; the fallback requires a full clone and applies the same size limits

## Pricing and free runs

Ultrareview is a premium feature that bills against usage credits rather than your plan's included usage.

| Plan                | Included free runs | After free runs                                                                                              |
| ------------------- | ------------------ | ------------------------------------------------------------------------------------------------------------ |
| Pro                 | 3 free runs        | billed as [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Max                 | 3 free runs        | billed as [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Team and Enterprise | none               | billed as [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |

* **Free runs**: the three Pro and Max runs are a one-time allotment per account and don't refresh.
* **Cost per review**: after you use the free runs, or after the free-run period ends, typically \$5 to \$25 in usage credits depending on the size of the change, matching the estimate the launch dialog shows before each run.
* **When a run counts**: once the cloud session starts. A review you stop early or that fails to complete still uses a free run; a paid review bills only for the portion that ran.

Because ultrareview always bills as usage credits outside the free runs, your account or organization must have usage credits turned on before you can launch a paid review. If usage credits aren't turned on, Claude Code blocks the launch, and how you turn them on depends on your billing access:

* If you can manage billing for your account, Claude Code links you to the billing settings where you can turn on usage credits.
* On Team and Enterprise plans, members without billing access send a request from the CLI asking their admin to turn on usage credits.

You can also run `/usage-credits` to check or change your usage-credits setting.

Claude Code asks you to confirm usage-credits billing once per conversation: when you start a new conversation, for example with `/clear`, Claude Code shows the confirmation again for the next paid review.

## Track a running review

A review typically takes 5 to 10 minutes. The review runs as a background task, so you can keep working in your session, start other commands, or close the terminal entirely.

Use `/tasks` to see running and completed reviews, open the detail view for a review, or stop a review that is in progress. Stopping a review archives the cloud session, and partial findings are not returned. When the review finishes, the verified findings appear as a notification in your session. Each finding includes the file location and an explanation of the issue so you can ask Claude to fix it directly.

## Run ultrareview non-interactively

Use the `claude ultrareview` subcommand to start an ultrareview from CI or a script without an interactive session. The subcommand launches the same review as `/code-review ultra`, blocks until the remote review finishes, prints the findings to stdout, and exits with code 0 on success or 1 on failure.

```bash theme={null}
claude ultrareview
claude ultrareview 1234
claude ultrareview origin/main
```

Without arguments, the subcommand reviews the diff between your current branch and the default branch, with the same [whole-repository fallback](#diff-limits-and-fallbacks) as `/code-review ultra` when no merge base exists. Pass a PR number to review a pull request, or a base branch to review against it; [base-branch handling](#review-against-a-different-base) matches the interactive command.

You consent to the whole-repository fallback and to the billing and terms prompt when you run the subcommand, so the run starts without waiting for input.

{/* min-version: 2.1.218 */}On Claude Code v2.1.218 or later, you can also start the cloud review by running `/code-review ultra` in a non-interactive session, for example `claude -p '/code-review ultra'`. Claude Code launches the review and prints a tracking link without waiting for the findings, unlike `claude ultrareview`, which blocks until they arrive. When the review would bill usage credits, Claude Code stops before launching and points you to `claude ultrareview`, because the billing confirmation needs an interactive session. Before v2.1.218, `/code-review ultra` in a non-interactive session ran a local review.

Progress messages and the live session URL go to stderr so stdout stays parseable. Use these flags to control the output and timeout:

| Flag                  | Description                                                         |
| --------------------- | ------------------------------------------------------------------- |
| `--json`              | Print the raw `bugs.json` payload instead of the formatted findings |
| `--timeout <minutes>` | Maximum minutes to wait for the review to finish. Defaults to 30    |

Running `claude ultrareview` requires the same authentication and usage credit configuration as `/code-review ultra`. The subcommand exits with code 0 when the review completes with or without findings, code 1 when the review fails to launch, the cloud session errors, or the timeout elapses, and code 130 when interrupted with Ctrl-C. The remote review keeps running if you interrupt the subcommand; follow the session URL printed to stderr to watch it in the browser.

For automatic reviews on GitHub pull requests, [Code Review](/docs/en/code-review) integrates with your repository directly and posts findings as inline PR comments without a CLI step.

## How ultrareview compares to /code-review and /review

All three commands review code, but they target different stages of your workflow.

|          | `/code-review`                  | `/review <pr>`                               | `/code-review ultra`                                            |
| -------- | ------------------------------- | -------------------------------------------- | --------------------------------------------------------------- |
| Target   | your working diff               | a GitHub pull request                        | your working diff or a pull request                             |
| Runs     | locally in your session         | locally in your session                      | remotely in a cloud sandbox                                     |
| Depth    | scales with the effort argument | a single-pass review at the session's effort | multi-agent fleet with independent verification                 |
| Duration | seconds to a few minutes        | seconds to a few minutes                     | roughly 5 to 10 minutes                                         |
| Cost     | counts toward normal usage      | counts toward normal usage                   | free runs, then roughly \$5 to \$25 per review as usage credits |
| Best for | quick feedback while iterating  | reviewing a teammate's PR before approving   | pre-merge confidence on substantial changes                     |

Use `/code-review` for fast feedback as you work. Use `/review <pr>` to look over a pull request the same way you would before approving it. Use `/code-review ultra` before merging a substantial change when you want a deeper pass that catches issues a local review might miss.

## Related resources

* [Claude Code on the web](/docs/en/claude-code-on-the-web): learn how cloud sessions and cloud sandboxes work
* [Plan complex changes with ultraplan](/docs/en/ultraplan): the planning counterpart to ultrareview for upfront design work
* [Manage costs effectively](/docs/en/costs): track usage and set spending limits
