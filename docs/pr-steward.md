> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# PR Steward

> Let PR Steward push fixes to your GitHub pull requests for failing checks, merge conflicts, and review feedback

PR Steward is an agent that works on your team's open GitHub pull requests. It pushes commits to address review feedback, and attempts to fix failing checks and resolve merge conflicts. With it on, you can open a pull request and start your next change while PR Steward works on the failing checks, conflicts, and review comments that follow. It's in public beta on Team and Enterprise plans.

> [!TIP]
>
> To turn on PR Steward, follow [Set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md), which takes an Owner role in your Claude organization.

PR Steward picks up a problem on GitHub, works on it in a cloud session, and reports back on the pull request:

![Diagram of PR Steward: a failing check, review comment, or merge conflict goes to PR Steward in a cloud session, and its commits and replies appear on GitHub.](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/pr-steward-flow.svg?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=4a1de46fbee43c2a00ef78c3dca36e59)

To stop PR Steward on a pull request, remove the `claude-pr-steward-watching` label or [comment `@claude stop`](https://code.claude.com/docs/en/pr-steward-pull-requests#start-or-stop-pr-steward-on-one-pull-request).

Steward is designed not to approve or merge pull requests. Use branch protection to require the approvals you want before anything merges. See [Limits on approvals and merges](https://code.claude.com/docs/en/pr-steward-security.md#limits-on-approvals-and-merges).

## What PR Steward does on a pull request

While PR Steward watches a pull request, it pushes commits and replies to comments without asking first, and the pull request has the `claude-pr-steward-watching` label. See [what PR Steward adds to a pull request](https://code.claude.com/docs/en/pr-steward-pull-requests.md#what-pr-steward-adds-to-a-pull-request).

### When PR Steward starts

In a repository where an Owner set PR Steward to **On**, it starts when you open a pull request, reopen one, or mark a draft as ready for review. It also starts at the next push to an open pull request that it hasn't started on before.

PR Steward skips drafts, pull requests from forks, pull requests that a bot opened, and authors without write access to the repository. An Owner can [change the repository's setting](https://code.claude.com/docs/en/pr-steward-setup.md#choose-when-pr-steward-starts-in-each-repository) so that PR Steward includes drafts, or normally starts only when someone asks it to.

### What PR Steward fixes

PR Steward works on failing checks, merge conflicts, review feedback, and the Claude Approvals check:

* **A failing check**: attempts a fix when the cause is in code that the pull request touches
* **A merge conflict**: attempts to merge the base branch in and resolve the conflicts
* **A person's review comment**: attempts small, specific changes and replies to the comment. Can reply without pushing when the request is large or about the design
* **A review bot's finding**: works on the findings that [Code Review](https://code.claude.com/docs/en/code-review.md) marks **Important**. For other bots, works on lint findings and bugs
* **The [Claude Approvals](https://code.claude.com/docs/en/approvals.md) check**: where the check waits for something that a commit can fix, such as open Code Review findings, works on that. Where the check waits for people's approvals, leaves it. After PR Steward pushes, the check can [ask for approvals again](https://code.claude.com/docs/en/approvals-policy.md#earlier-approvals-after-a-new-push)

### Stop or limit PR Steward

To stop PR Steward on one pull request, remove the `claude-pr-steward-watching` label or [comment `@claude stop`](https://code.claude.com/docs/en/pr-steward-pull-requests#start-or-stop-pr-steward-on-one-pull-request). To turn off or limit PR Steward on the pull requests that you open later, go to [**PR Steward**](https://claude.ai/settings/claude-code#pr-steward) in **Settings > Code** or **Settings > Claude Code**.

## Decide whether PR Steward fits your team

PR Steward is one of the [Claude Ship](https://code.claude.com/docs/en/claude-ship.md) agents, alongside Code Review and Claude Approvals. Before you turn it on, compare it with auto-fix and `/steward`, check that your organization qualifies, and see how it's billed.

### How PR Steward differs from auto-fix and /steward

[Auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests) and the [`/steward` command](https://code.claude.com/docs/en/ship-command#start-a-watch-with-%2Fsteward) also work on failing checks and review comments. They run in your own sessions, and they act as you and count against your own usage. PR Steward acts as the [Claude GitHub App](https://github.com/apps/claude) and bills your organization.

If you ask to auto-fix a pull request that PR Steward is watching, the request fails. See [Auto-fix is unavailable](https://code.claude.com/docs/en/pr-steward-troubleshooting.md#auto-fix-is-unavailable).

### Availability

PR Steward works with repositories on github.com or a connected [GitHub Enterprise Server](https://code.claude.com/docs/en/github-enterprise-server.md) instance on port 443. You need a Claude organization on a [Team or Enterprise plan](https://code.claude.com/docs/en/feature-availability.md#features-that-require-a-claude-subscription).

PR Steward isn't available to organizations with [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention.md) enabled, the [HIPAA configuration](https://code.claude.com/docs/en/hipaa-setup.md) applied, or customer-managed encryption keys.

### What PR Steward costs

PR Steward's usage is billed by tokens to your organization's [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans). It has no spend limit of its own until you [set one](https://code.claude.com/docs/en/pr-steward-setup.md#set-pr-steward’s-spend-limits), which takes an Owner role.

## Next steps

* [Set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md), which takes an Owner
* [Work with PR Steward](https://code.claude.com/docs/en/pr-steward-pull-requests.md) on your pull requests
* [What PR Steward can access](https://code.claude.com/docs/en/pr-steward-security.md)
* [Troubleshoot PR Steward](https://code.claude.com/docs/en/pr-steward-troubleshooting.md)
