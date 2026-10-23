> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review costs and usage

> Estimate and cap what your organization spends on Claude Code Review: how reviews are billed through usage credits, what drives cost, and where to track usage.

[Code Review](https://code.claude.com/docs/en/code-review.md) has no flat per-review price. What you spend depends on the cost of each review and on how many reviews run:

* **Cost of each review**: scales with the [review level](https://code.claude.com/docs/en/code-review-setup.md#set-the-default-review-level), the size of the change, the complexity of the surrounding code, and how many candidate issues need verification
* **Number of reviews**: set by [how often reviews run](#how-often-reviews-run) in each repository

## Pricing

Code Review is billed on token usage through [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans), separately from your plan's included usage. Reviews are billed to your organization, not to the developer who opened the PR or requested the review. Costs appear on your Anthropic bill regardless of whether your organization uses Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry for other Claude Code features.

### How often reviews run

A repository you add from the admin page starts at **After every push**, which runs the most reviews. Each repository's [**Review runs** setting](https://code.claude.com/docs/en/code-review-setup.md#set-when-reviews-run) decides how many reviews a pull request gets:

* **Once after PR creation**: a review runs when the pull request is opened, reopened, or marked ready for review
* **After every push**: runs on each push, multiplying cost by the number of pushes
* **Manual (@claude review)**: no reviews on open or push

Comment commands, drafts, and pull requests from forks adjust those counts:

* **`@claude review always` in Once after PR creation or Manual mode**: [opts the PR into push-triggered reviews](https://code.claude.com/docs/en/code-review-pull-requests.md#comment-commands), so additional cost accrues per push after that comment
* **`@claude review always` in After every push mode**: pushes already trigger reviews, so the subscription doesn't change per-push cost
* **`@claude review`**: runs a single review without subscribing to future pushes
* **Drafts and pull requests from forks**: [automatic reviews skip both](https://code.claude.com/docs/en/code-review-pull-requests.md#review-drafts-and-pull-requests-from-forks), so pushes to them don't add reviews

## Estimate your spend

Before a wide rollout, run a small pilot to estimate monthly spend from your own pull requests.

1. Set a [monthly spend limit](#limit-your-spend) for the pilot.
2. Turn on Code Review for a few representative repositories with **Review runs** set to **Once after PR creation** or **Manual (@claude review)**.
3. After several reviews have run, read each repository's average cost per review in the **Average cost** column of the **Repositories** table, in the **Code review** section of [**Admin settings > Claude Code**](https://claude.ai/admin-settings/claude-code#code-review).
4. Multiply that average by the number of pull requests the repository opens in a month. For **After every push**, multiply again by the typical number of pushes per pull request.

A repository's average moves with the size of its pull requests and with the review level you choose.

## Limit your spend

To set a monthly spend limit for Code Review, go to [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) and configure the limit for the Claude Code Review service. The limit applies to the whole organization.

Code Review skips reviews when any of these runs out:

* **Code Review spend limit**: the monthly limit you set for the Claude Code Review service. It resets at the start of the next billing period, and reviews resume sooner if you raise it.
* **Organization spend limit**: your organization's overall monthly spend limit for usage credits. Raise it on the same page.
* **Usage credits balance**: your organization's balance of usage credits. Add credits on the same page.

Code Review also skips reviews once what's left is less than the expected cost of one review. When a review is skipped, developers see a [comment on the PR](https://code.claude.com/docs/en/code-review-troubleshooting.md#review-didn’t-run-and-the-pr-shows-a-budget-message) that names the cause and links to the usage settings.

To monitor spend, use the [analytics dashboard](#view-usage).

## View usage

Go to [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) to see Code Review activity across your organization.

| Section | What it shows |
| :- | :- |
| PRs reviewed | Daily count of pull requests reviewed over the selected time range |
| Code Review cost | Code Review spend so far this month |
| Feedback | Count of review comments that were auto-resolved because a developer addressed the issue |
| Repository breakdown | Per-repo counts of PRs reviewed, comments resolved, and review runs, with estimated cost and a per-PR view |

The Code Review cost card shows an amount only when the current month is selected. Cost figures in analytics can differ from your invoice. Repository breakdown costs are estimated at list price, before any discounts or credits, and cover only reviews that Claude posted on a pull request. For invoice-accurate spend, refer to your Anthropic bill.

## Related resources

* [Set up Code Review](https://code.claude.com/docs/en/code-review-setup.md): where to choose the review level and when reviews run in each repository
* [Read and request reviews on a pull request](https://code.claude.com/docs/en/code-review-pull-requests.md): the comment commands, pull requests from forks, and the budget message developers see when a review is skipped
* [Code Review](https://code.claude.com/docs/en/code-review.md): what a review checks and what it posts
* [Manage costs effectively](https://code.claude.com/docs/en/costs.md): spend controls and usage tracking for the rest of Claude Code
