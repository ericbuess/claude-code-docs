> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Set up automated PR reviews that catch logic errors, security vulnerabilities, and regressions using multi-agent analysis of your full codebase

<Note>
  Code Review is in research preview, available for [Team and Enterprise](https://claude.ai/admin-settings/claude-code) subscriptions. It is not available for organizations with [Zero Data Retention](/en/zero-data-retention) enabled.
</Note>

Code Review analyzes your GitHub pull requests and posts findings as inline comments on the lines of code where it found issues. A fleet of specialized agents examine the code changes in the context of your full codebase, looking for logic errors, security vulnerabilities, broken edge cases, and subtle regressions.

Findings are tagged by severity and don't approve or block your PR, so existing review workflows stay intact. You can tune what Claude flags by adding a `CLAUDE.md` or `REVIEW.md` file to your repository.

To run Claude in your own CI infrastructure instead of this managed service, see [GitHub Actions](/en/github-actions) or [GitLab CI/CD](/en/gitlab-ci-cd). For repositories on a self-hosted GitHub instance, see [GitHub Enterprise Server](/en/github-enterprise-server).

This page covers:

* [How reviews work](#how-reviews-work)
* [Setup](#set-up-code-review)
* [Triggering reviews manually](#manually-trigger-reviews) with `@claude review` and `@claude review once`
* [Customizing reviews](#customize-reviews) with `CLAUDE.md` and `REVIEW.md`
* [Pricing](#pricing)
* [Troubleshooting](#troubleshooting) failed runs and missing comments

## How reviews work

Once an admin [enables Code Review](#set-up-code-review) for your organization, reviews trigger when a PR opens, on every push, or when manually requested, depending on the repository's configured behavior. Commenting `@claude review` [starts reviews on a PR](#manually-trigger-reviews) in any mode.

When a review runs, multiple agents analyze the diff and surrounding code in parallel on Anthropic infrastructure. Each agent looks for a different class of issue, then a verification step checks candidates against actual code behavior to filter out false positives. The results are deduplicated, ranked by severity, and posted as inline comments on the specific lines where issues were found, with a summary in the review body. If no issues are found, Claude posts a short confirmation comment on the PR.

Reviews scale in cost with PR size and complexity, completing in 20 minutes on average. Admins can monitor review activity and spend via the [analytics dashboard](#view-usage).

### Severity levels

Each finding is tagged with a severity level:

| Marker | Severity     | Meaning                                                             |
| :----- | :----------- | :------------------------------------------------------------------ |
| 🔴     | Important    | A bug that should be fixed before merging                           |
| 🟡     | Nit          | A minor issue, worth fixing but not blocking                        |
| 🟣     | Pre-existing | A bug that exists in the codebase but was not introduced by this PR |

Findings include a collapsible extended reasoning section you can expand to understand why Claude flagged the issue and how it verified the problem.

### Rate and reply to findings

Each review comment from Claude arrives with 👍 and 👎 already attached so both buttons appear in the GitHub UI for one-click rating. Click 👍 if the finding was useful or 👎 if it was wrong or noisy. Anthropic collects reaction counts after the PR merges and uses them to tune the reviewer. Reactions do not trigger a re-review or change anything on the PR.

Replying to an inline comment does not prompt Claude to respond or update the PR. To act on a finding, fix the code and push. If the PR is subscribed to push-triggered reviews, the next run resolves the thread when the issue is fixed. To request a fresh review without pushing, comment `@claude review once` as a [top-level PR comment](#manually-trigger-reviews).

### Check run output

Beyond the inline review comments, each review populates the **Claude Code Review** check run that appears alongside your CI checks. Expand its **Details** link to see a summary of every finding in one place, sorted by severity:

| Severity     | File:Line                 | Issue                                                          |
| ------------ | ------------------------- | -------------------------------------------------------------- |
| 🔴 Important | `src/auth/session.ts:142` | Token refresh races with logout, leaving stale sessions active |
| 🟡 Nit       | `src/auth/session.ts:88`  | `parseExpiry` silently returns 0 on malformed input            |

Each finding also appears as an annotation in the **Files changed** tab, marked directly on the relevant diff lines. Important findings render with a red marker, nits with a yellow warning, and pre-existing bugs with a gray notice. Annotations and the severity table are written to the check run independently of inline review comments, so they remain available even if GitHub rejects an inline comment on a line that moved.

The check run always completes with a neutral conclusion so it never blocks merging through branch protection rules. If you want to gate merges on Code Review findings, read the severity breakdown from the check run output in your own CI. The last line of the Details text is a machine-readable comment your workflow can parse with `gh` and jq:

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

This returns a JSON object with counts per severity, for example `{"normal": 2, "nit": 1, "pre_existing": 0}`. The `normal` key holds the count of Important findings; a non-zero value means Claude found at least one bug worth fixing before merge.

### What Code Review checks

By default, Code Review focuses on correctness: bugs that would break production, not formatting preferences or missing test coverage. You can expand what it checks by [adding guidance files](#customize-reviews) to your repository.

## Set up Code Review

An admin enables Code Review once for the organization and selects which repositories to include.

<Steps>
  <Step title="Open Claude Code admin settings">
    Go to [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) and find the Code Review section. You need admin access to your Claude organization and permission to install GitHub Apps in your GitHub organization.
  </Step>

  <Step title="Start setup">
    Click **Setup**. This begins the GitHub App installation flow.
  </Step>

  <Step title="Install the Claude GitHub App">
    Follow the prompts to install the Claude GitHub App to your GitHub organization. The app requests these repository permissions:

    * **Contents**: read and write
    * **Issues**: read and write
    * **Pull requests**: read and write

    Code Review uses read access to contents and write access to pull requests. The broader permission set also supports [GitHub Actions](/en/github-actions) if you enable that later.
  </Step>

  <Step title="Select repositories">
    Choose which repositories to enable for Code Review. If you don't see a repository, make sure you gave the Claude GitHub App access to it during installation. You can add more repositories later.
  </Step>

  <Step title="Set review triggers per repo">
    After setup completes, the Code Review section shows your repositories in a table. For each repository, use the **Review Behavior** dropdown to choose when reviews run:

    * **Once after PR creation**: review runs once when a PR is opened or marked ready for review
    * **After every push**: review runs on every push to the PR branch, catching new issues as the PR evolves and auto-resolving threads when you fix flagged issues
    * **Manual**: reviews start only when someone [comments `@claude review` or `@claude review once` on a PR](#manually-trigger-reviews); `@claude review` also subscribes the PR to reviews on subsequent pushes

    Reviewing on every push runs the most reviews and costs the most. Manual mode is useful for high-traffic repos where you want to opt specific PRs into review, or to only start reviewing your PRs once they're ready.
  </Step>
</Steps>

The repositories table also shows the average cost per review for each repo based on recent activity. Use the row actions menu to turn Code Review on or off per repository, or to remove a repository entirely.

To verify setup, open a test PR. If you chose an automatic trigger, a check run named **Claude Code Review** appears within a few minutes. If you chose Manual, comment `@claude review` on the PR to start the first review. If no check run appears, confirm the repository is listed in your admin settings and the Claude GitHub App has access to it.

## Manually trigger reviews

Two comment commands start a review on demand. Both work regardless of the repository's configured trigger, so you can use them to opt specific PRs into review in Manual mode or to get an immediate re-review in other modes.

| Command               | What it does                                                                  |
| :-------------------- | :---------------------------------------------------------------------------- |
| `@claude review`      | Starts a review and subscribes the PR to push-triggered reviews going forward |
| `@claude review once` | Starts a single review without subscribing the PR to future pushes            |

Use `@claude review once` when you want feedback on the current state of a PR but don't want every subsequent push to incur a review. This is useful for long-running PRs with frequent pushes, or when you want a one-off second opinion without changing the PR's review behavior.

For either command to trigger a review:

* Post it as a top-level PR comment, not an inline comment on a diff line
* Put the command at the start of the comment, with `once` on the same line if you're using the one-shot form
* You must have owner, member, or collaborator access to the repository
* The PR must be open

Unlike automatic triggers, manual triggers run on draft PRs, since an explicit request signals you want the review now regardless of draft status.

If a review is already running on that PR, the request is queued until the in-progress review completes. You can monitor progress via the check run on the PR.

## Customize reviews

Code Review reads two files from your repository to guide what it flags. They differ in how strongly they influence the review:

* **`CLAUDE.md`**: shared project instructions that Claude Code uses for all tasks, not just reviews. Code Review reads it as project context and flags newly introduced violations as nits.
* **`REVIEW.md`**: review-only instructions, injected directly into every agent in the review pipeline as highest priority. Use it to change what gets flagged, at what severity, and how findings are reported.

### CLAUDE.md

Code Review reads your repository's `CLAUDE.md` files and treats newly introduced violations as [nit-level](#severity-levels) findings. This works bidirectionally: if your PR changes code in a way that makes a `CLAUDE.md` statement outdated, Claude flags that the docs need updating too.

Claude reads `CLAUDE.md` files at every level of your directory hierarchy, so rules in a subdirectory's `CLAUDE.md` apply only to files under that path. See the [memory documentation](/en/memory) for more on how `CLAUDE.md` works.

For review-specific guidance that you don't want applied to general Claude Code sessions, use [`REVIEW.md`](#review-md) instead.

### REVIEW\.md

`REVIEW.md` is a file at your repository root that overrides how Code Review behaves on your repo. Its contents are injected into the system prompt of every agent in the review pipeline as the highest-priority instruction block, taking precedence over the default review guidance.

Because it's pasted verbatim, `REVIEW.md` is plain instructions: [`@` import syntax](/en/memory#import-additional-files) is not expanded, and referenced files are not read into the prompt. Put the rules you want enforced directly in the file.

#### What you can tune

`REVIEW.md` is freeform markdown, so anything you can express as a review instruction is in scope. The patterns below have the most impact in practice.

**Severity**: redefine what 🔴 Important means for your repo. The default calibration targets production code; a docs repo, a config repo, or a prototype might want a much narrower definition. State explicitly which classes of finding are Important and which are Nit at most. You can also escalate in the other direction, for example treating any `CLAUDE.md` violation as Important rather than the default nit.

**Nit volume**: cap how many 🟡 Nit comments a single review posts. Prose and config files can be polished forever. A cap like "report at most five nits, mention the rest as a count in the summary" keeps reviews actionable.

**Skip rules**: list paths, branch patterns, and finding categories where Claude should post no findings. Common candidates are generated code, lockfiles, vendored dependencies, and machine-authored branches, along with anything your CI already enforces like linting or spellcheck. For paths that warrant some review but not full scrutiny, set a higher bar instead of skipping entirely: "in `scripts/`, only report if near-certain and severe."

**Repo-specific checks**: add rules you want flagged on every PR, like "new API routes must have an integration test." Because `REVIEW.md` is injected as highest priority, these land more reliably than the same rules in a long `CLAUDE.md`.

**Verification bar**: require evidence before a class of finding is posted. For example, "behavior claims need a `file:line` citation in the source, not an inference from naming" cuts false positives that would otherwise cost the author a round trip.

**Re-review convergence**: tell Claude how to behave when a PR has already been reviewed. A rule like "after the first review, suppress new nits and post Important findings only" stops a one-line fix from reaching round seven on style alone.

**Summary shape**: ask for the review body to open with a one-line tally such as `2 factual, 4 style`, and to lead with "no factual issues" when that's the case. The author wants to know the shape of the work before the details.

#### Example

This `REVIEW.md` recalibrates severity for a backend service, caps nits, skips generated files, and adds repo-specific checks.

```markdown theme={null}
# Review instructions

## What Important means here

Reserve Important for findings that would break behavior, leak data,
or block a rollback: incorrect logic, unscoped database queries, PII
in logs or error messages, and migrations that aren't backward
compatible. Style, naming, and refactoring suggestions are Nit at
most.

## Cap the nits

Report at most five Nits per review. If you found more, say "plus N
similar items" in the summary instead of posting them inline. If
everything you found is a Nit, lead the summary with "No blocking
issues."

## Do not report

- Anything CI already enforces: lint, formatting, type errors
- Generated files under `src/gen/` and any `*.lock` file
- Test-only code that intentionally violates production rules

## Always check

- New API routes have an integration test
- Log lines don't include email addresses, user IDs, or request bodies
- Database queries are scoped to the caller's tenant
```

#### Keep it focused

Length has a cost: a long `REVIEW.md` dilutes the rules that matter most. Keep it to instructions that change review behavior, and leave general project context in `CLAUDE.md`.

## View usage

Go to [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) to see Code Review activity across your organization. The dashboard shows:

| Section              | What it shows                                                                            |
| :------------------- | :--------------------------------------------------------------------------------------- |
| PRs reviewed         | Daily count of pull requests reviewed over the selected time range                       |
| Cost weekly          | Weekly spend on Code Review                                                              |
| Feedback             | Count of review comments that were auto-resolved because a developer addressed the issue |
| Repository breakdown | Per-repo counts of PRs reviewed and comments resolved                                    |

The repositories table in admin settings also shows average cost per review for each repo. Dashboard cost figures are estimates for monitoring activity; for invoice-accurate spend, refer to your Anthropic bill.

## Pricing

Code Review is billed based on token usage. Each review averages \$15-25 in cost, scaling with PR size, codebase complexity, and how many issues require verification. Code Review usage is billed separately through [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) and does not count against your plan's included usage.

The review trigger you choose affects total cost:

* **Once after PR creation**: runs once per PR
* **After every push**: runs on each push, multiplying cost by the number of pushes
* **Manual**: no reviews until someone comments `@claude review` on a PR

In any mode, commenting `@claude review` [opts the PR into push-triggered reviews](#manually-trigger-reviews), so additional cost accrues per push after that comment. To run a single review without subscribing to future pushes, comment `@claude review once` instead.

Costs appear on your Anthropic bill regardless of whether your organization uses AWS Bedrock or Google Vertex AI for other Claude Code features. To set a monthly spend cap for Code Review, go to [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) and configure the limit for the Claude Code Review service.

Monitor spend via the weekly cost chart in [analytics](#view-usage) or the per-repo average cost column in admin settings.

## Troubleshooting

Review runs are best-effort. A failed run never blocks your PR, but it also doesn't retry on its own. This section covers how to recover from a failed run and where to look when the check run reports issues you can't find.

### Retrigger a failed or timed-out review

When the review infrastructure hits an internal error or exceeds its time limit, the check run completes with a title of **Code review encountered an error** or **Code review timed out**. The conclusion is still neutral, so nothing blocks your merge, but no findings are posted.

To run the review again, comment `@claude review once` on the PR. This starts a fresh review without subscribing the PR to future pushes. If the PR is already subscribed to push-triggered reviews, pushing a new commit also starts a new review.

The **Re-run** button in GitHub's Checks tab does not retrigger Code Review. Use the comment command or a new push instead.

### Review didn't run and the PR shows a spend-cap message

When your organization's monthly spend cap is reached, Code Review posts a single comment on the PR explaining that the review was skipped. Reviews resume automatically at the start of the next billing period, or immediately when an admin raises the cap at [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage).

### Find issues that aren't showing as inline comments

If the check run title says issues were found but you don't see inline review comments on the diff, look in these other locations where findings are surfaced:

* **Check run Details**: click **Details** next to the Claude Code Review check in the Checks tab. The severity table lists every finding with its file, line, and summary regardless of whether the inline comment was accepted.
* **Files changed annotations**: open the **Files changed** tab on the PR. Findings render as annotations attached directly to the diff lines, separate from review comments.
* **Review body**: if you pushed to the PR while a review was running, some findings may reference lines that no longer exist in the current diff. Those appear under an **Additional findings** heading in the review body text rather than as inline comments.

## Related resources

Code Review is designed to work alongside the rest of Claude Code. If you want to run reviews locally before opening a PR, need a self-hosted setup, or want to go deeper on how `CLAUDE.md` shapes Claude's behavior across tools, these pages are good next stops:

* [Plugins](/en/discover-plugins): browse the plugin marketplace, including a `code-review` plugin for running on-demand reviews locally before pushing
* [GitHub Actions](/en/github-actions): run Claude in your own GitHub Actions workflows for custom automation beyond code review
* [GitLab CI/CD](/en/gitlab-ci-cd): self-hosted Claude integration for GitLab pipelines
* [Memory](/en/memory): how `CLAUDE.md` files work across Claude Code
* [Analytics](/en/analytics): track Claude Code usage beyond code review
