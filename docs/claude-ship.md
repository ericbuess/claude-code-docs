> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Ship

> Meet the Claude Ship agents for GitHub pull requests: Code Review, PR Steward, and Claude Approvals

Claude Ship is a set of agents that help get your team's GitHub pull requests ready to merge:

* [Code Review](https://code.claude.com/docs/en/code-review.md): looks for issues such as logic errors, security vulnerabilities, and broken edge cases
* [PR Steward](https://code.claude.com/docs/en/pr-steward.md): works on review feedback and failing checks
* [Claude Approvals](https://code.claude.com/docs/en/approvals.md): checks pull requests against an approval policy that you write

Together, they can take a pull request through review, fixes, and an approval decision, so your team doesn't have to manage each step manually. Your settings and GitHub branch rules determine what merges. Claude Ship is available on [Team and Enterprise plans](#who-can-use-claude-ship).

To turn on the agents, go to [Set up Claude Ship](#set-up-claude-ship).

> [!NOTE]
>
> To get a review and fixes locally, on one of your own pull requests, run [`/ship`](https://code.claude.com/docs/en/ship-command) in Claude Code.

## Claude Ship agents

This diagram shows each agent's part in a pull request, and the parts that stay with you and GitHub:

![Diagram of a pull request with all three Claude Ship agents on: Code Review finds problems, PR Steward pushes fixes, and a fix can start another review. Claude Approvals applies your policy, and the merge follows your branch rules.](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/claude-ship-overview.svg?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=6c972cdcb9dfc1c7a9a54e421bcf35a5)

> [!NOTE]
>
> Claude Ship uses AI and may miss bugs, security vulnerabilities, or other issues.

### Code Review finds problems

[Code Review](https://code.claude.com/docs/en/code-review.md) reads a change alongside the surrounding code. Findings arrive as inline comments on the lines concerned, ranked by severity.

### PR Steward pushes fixes

[PR Steward](https://code.claude.com/docs/en/pr-steward.md) works on failing checks, merge conflicts, and review comments from people and from review bots such as Code Review. It pushes commits with its fixes.

Steward is designed not to approve or merge pull requests. Use branch protection to require the approvals you want before anything merges. See [Limits on approvals and merges](https://code.claude.com/docs/en/pr-steward-security.md#limits-on-approvals-and-merges).

### Claude Approvals applies your policy

[Claude Approvals](https://code.claude.com/docs/en/approvals.md) is a check that reports who still has to approve. You write its policy file, which can set how many people have to approve changes to a path, and where Claude can post an approving review. The check blocks a merge only where you [make it a required check in GitHub](https://code.claude.com/docs/en/approvals-setup.md#enforce-your-policy-and-require-claude-approvals), and normally not in observe mode.

> [!WARNING]
>
> If you use GitHub auto-merge or a merge queue with a policy that doesn't require a person's approval, a change can merge without anyone acting. See [Merges without human review](https://code.claude.com/docs/en/approvals-github-rules.md#merges-without-human-review).

## Set up Claude Ship

Go to [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship) for Claude Ship's settings. You need an [Owner role](https://code.claude.com/docs/en/server-managed-settings.md#access-control).

Turn on one agent at a time in one repository, in this order:

1. [Set up Code Review](https://code.claude.com/docs/en/code-review-setup.md)
2. [Set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md). For the setting that chooses when PR Steward starts, begin with [**Manual (@claude steward)**](https://code.claude.com/docs/en/pr-steward-setup.md#choose-when-pr-steward-starts-in-each-repository). PR Steward has no spend limit of its own until you set one.
3. [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md). A policy file in the repository starts it, so see [who can turn it on](https://code.claude.com/docs/en/approvals.md#who-can-turn-approvals-on-or-off). Start in observe mode, where the **Claude Approvals** check reports what your policy would decide. Observe mode is billed. See [what Approvals costs](https://code.claude.com/docs/en/approvals-setup.md#what-approvals-costs).

### If you already use Code Review

Code Review's settings moved to [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship).

A Claude Approvals policy file, `.claude/approvals.yml`, changes which pull requests Code Review reviews automatically. Once the file is on the default branch, in observe mode or enforced, automatic reviews normally stop where no matching rule names `claude/code_review`. To keep them, [add `claude/code_review` to a rule](https://code.claude.com/docs/en/approvals-policy#advisory).

## Plans and billing

Claude Ship is for organizations on Team and Enterprise plans.

### Who can use Claude Ship

Code Review is generally available. PR Steward and Claude Approvals are in public beta. The agents aren't available to organizations with [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention.md) enabled, the [HIPAA configuration](https://code.claude.com/docs/en/hipaa-setup.md) applied, or customer-managed encryption keys. Approvals has [more limits](https://code.claude.com/docs/en/approvals.md#availability).

### How each Claude Ship agent is billed

Each agent is billed on token usage through your organization's [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans), separately from your plan's included usage. Approvals bills for [classifier](https://code.claude.com/docs/en/approvals-classifiers.md) runs and the Code Reviews that a policy asks for.

> [!NOTE]
>
> Eligible Enterprise organizations can claim promotional Claude Ship credits. For who qualifies, the amount, and the dates, see the [credit terms](https://support.claude.com/en/articles/17603594-free-code-review-promotional-credits-for-claude-enterprise).

If you turn off usage credits in [**Organization settings > Usage**](https://claude.ai/admin-settings/usage), an agent that's on keeps running and billing your organization. To stop its charges, follow [Turn off Claude Ship](#turn-off-claude-ship).

See each agent's costs:

* [Code Review](https://code.claude.com/docs/en/code-review-costs.md)
* [PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md#set-pr-steward’s-spend-limits)
* [Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md#what-approvals-costs)

## Turn off Claude Ship

Turn off Approvals before Code Review, because a policy can start billed reviews where Code Review is off:

1. [Turn off Approvals](https://code.claude.com/docs/en/approvals-setup.md#turn-off-approvals)
2. [Turn off PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md#turn-off-pr-steward)
3. [Turn off Code Review](https://code.claude.com/docs/en/code-review-setup.md#turn-off-code-review-or-remove-a-repository)

These steps leave the `/ship` and `/steward` commands on. See [how to turn them off](https://code.claude.com/docs/en/ship-command.md#turn-off-%2Fship-and-%2Fsteward-for-your-organization).

## Related resources

* [GitHub Actions](https://code.claude.com/docs/en/github-actions.md) and [GitLab CI/CD](https://code.claude.com/docs/en/gitlab-ci-cd.md): run Claude Code in your own CI
* [Review code locally](https://code.claude.com/docs/en/code-review-local.md): get a review in your terminal before you push
