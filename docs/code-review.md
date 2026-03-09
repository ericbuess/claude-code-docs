> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Set up automated PR reviews that catch logic errors, security vulnerabilities, and regressions using multi-agent analysis of your full codebase

<Note>
  Code Review is in research preview, available for [Teams and Enterprise](https://claude.ai/admin-settings/claude-code) subscriptions. It is not available for organizations with [Zero Data Retention](/en/zero-data-retention) enabled.
</Note>

Code Review analyzes your GitHub pull requests and posts findings as inline comments on the lines of code where it found issues. A fleet of specialized agents examine the code changes in the context of your full codebase, looking for logic errors, security vulnerabilities, broken edge cases, and subtle regressions.

Findings are tagged by severity and don't approve or block your PR, so existing review workflows stay intact. You can tune what Claude flags by adding a `CLAUDE.md` or `REVIEW.md` file to your repository.

To run Claude in your own CI infrastructure instead of this managed service, see [GitHub Actions](/en/github-actions) or [GitLab CI/CD](/en/gitlab-ci-cd).

This page covers:

* [How reviews work](#how-reviews-work)
* [Setup](#set-up-code-review)
* [Customizing reviews](#customize-reviews) with `CLAUDE.md` and `REVIEW.md`
* [Pricing](#pricing)

## How reviews work

Once an admin [enables Code Review](#set-up-code-review) for your organization, reviews run automatically when a pull request opens or updates. Multiple agents analyze the diff and surrounding code in parallel on Anthropic infrastructure. Each agent looks for a different class of issue, then a verification step checks candidates against actual code behavior to filter out false positives. The results are deduplicated, ranked by severity, and posted as inline comments on the specific lines where issues were found. If no issues are found, Claude posts a short confirmation comment on the PR.

Reviews scale in cost with PR size and complexity, completing in 20 minutes on average. Admins can monitor review activity and spend via the [analytics dashboard](#view-usage).

### Severity levels

Each finding is tagged with a severity level:

| Marker | Severity     | Meaning                                                             |
| :----- | :----------- | :------------------------------------------------------------------ |
| 🔴     | Normal       | A bug that should be fixed before merging                           |
| 🟡     | Nit          | A minor issue, worth fixing but not blocking                        |
| 🟣     | Pre-existing | A bug that exists in the codebase but was not introduced by this PR |

Findings include a collapsible extended reasoning section you can expand to understand why Claude flagged the issue and how it verified the problem.

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
    After setup completes, the Code Review section shows your repositories in a table. For each repository, use the dropdown to choose when reviews run:

    * **After PR creation only**: review runs once when a PR is opened or marked ready for review
    * **After every push to PR branch**: review runs on every push, catching new issues as the PR evolves and auto-resolving threads when you fix flagged issues

    Reviewing on every push runs more reviews and costs more. Start with PR creation only and switch to on-push for repos where you want continuous coverage and automatic thread cleanup.
  </Step>
</Steps>

The repositories table also shows the average cost per review for each repo based on recent activity. Use the row actions menu to turn Code Review on or off per repository, or to remove a repository entirely.

To verify setup, open a test PR. A check run named **Claude Code Review** appears within a few minutes. If it doesn't, confirm the repository is listed in your admin settings and the Claude GitHub App has access to it.

## Customize reviews

Code Review reads two files from your repository to guide what it flags. Both are additive on top of the default correctness checks:

* **`CLAUDE.md`**: shared project instructions that Claude Code uses for all tasks, not just reviews. Use it when guidance also applies to interactive Claude Code sessions.
* **`REVIEW.md`**: review-only guidance, read exclusively during code reviews. Use it for rules that are strictly about what to flag or skip during review and would clutter your general `CLAUDE.md`.

### CLAUDE.md

Code Review reads your repository's `CLAUDE.md` files and treats newly-introduced violations as nit-level findings. This works bidirectionally: if your PR changes code in a way that makes a `CLAUDE.md` statement outdated, Claude flags that the docs need updating too.

Claude reads `CLAUDE.md` files at every level of your directory hierarchy, so rules in a subdirectory's `CLAUDE.md` apply only to files under that path. See the [memory documentation](/en/memory) for more on how `CLAUDE.md` works.

For review-specific guidance that you don't want applied to general Claude Code sessions, use [`REVIEW.md`](#reviewmd) instead.

### REVIEW\.md

Add a `REVIEW.md` file to your repository root for review-specific rules. Use it to encode:

* Company or team style guidelines: "prefer early returns over nested conditionals"
* Language- or framework-specific conventions not covered by linters
* Things Claude should always flag: "any new API route must have an integration test"
* Things Claude should skip: "don't comment on formatting in generated code under `/gen/`"

Example `REVIEW.md`:

```markdown  theme={null}
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude auto-discovers `REVIEW.md` at the repository root. No configuration needed.

## View usage

Go to [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) to see Code Review activity across your organization. The dashboard shows:

| Section              | What it shows                                                                            |
| :------------------- | :--------------------------------------------------------------------------------------- |
| PRs reviewed         | Daily count of pull requests reviewed over the selected time range                       |
| Cost weekly          | Weekly spend on Code Review                                                              |
| Feedback             | Count of review comments that were auto-resolved because a developer addressed the issue |
| Repository breakdown | Per-repo counts of PRs reviewed and comments resolved                                    |

The repositories table in admin settings also shows average cost per review for each repo.

## Pricing

Code Review is billed based on token usage. Reviews average \$15-25, scaling with PR size, codebase complexity, and how many issues require verification.

The review trigger you choose affects total cost:

* **After PR creation only**: runs once per PR
* **After every push**: runs on each commit, multiplying cost by the number of pushes

Costs appear on your Anthropic bill regardless of whether your organization uses AWS Bedrock or Google Vertex AI for other Claude Code features. To set a monthly spend cap for Code Review, go to [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) and configure the limit for the Claude Code Review service.

Monitor spend via the weekly cost chart in [analytics](#view-usage) or the per-repo average cost column in admin settings.

## Related resources

Code Review is designed to work alongside the rest of Claude Code. If you want to run reviews locally before opening a PR, need a self-hosted setup, or want to go deeper on how `CLAUDE.md` shapes Claude's behavior across tools, these pages are good next stops:

* [Plugins](/en/discover-plugins): browse the plugin marketplace, including a `code-review` plugin for running on-demand reviews locally before pushing
* [GitHub Actions](/en/github-actions): run Claude in your own GitHub Actions workflows for custom automation beyond code review
* [GitLab CI/CD](/en/gitlab-ci-cd): self-hosted Claude integration for GitLab pipelines
* [Memory](/en/memory): how `CLAUDE.md` files work across Claude Code
* [Analytics](/en/analytics): track Claude Code usage beyond code review
