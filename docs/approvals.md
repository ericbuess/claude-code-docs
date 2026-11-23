> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Approvals

> Set how many people a path in your GitHub repository needs, and where Claude may approve, with a policy file and a pull request check

Claude Approvals is a check on GitHub pull requests that reports who still has to approve. It follows a [policy](https://code.claude.com/docs/en/approvals-policy.md), a file in your repository that can set how many people have to approve a change to a path and where Claude may approve.

> [!TIP]
>
> To turn on Claude Approvals in a repository, follow [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md).

To evaluate a pull request, Approvals reads the policy, finds the rules that apply, and counts approvals:

![Diagram of how Claude Approvals evaluates a pull request. Approvals reads the policy on the default branch, finds the rules that apply and takes the strictest, and counts approvals. A check and a comment appear on the pull request. If the policy allows, an approving review appears too.](https://mintcdn.com/claude-code/sMH7RDpTvyWlAkrg/images/approvals-flow.svg?fit=max\&auto=format\&n=sMH7RDpTvyWlAkrg\&q=85\&s=29bc7cd0a0a49c1986cab5afdf57ca3b)

Use Approvals to set how many people have to approve a change, with more on risky changes and fewer on routine ones. For example, billing code can need two people, and test fixtures can need one person once [Code Review](https://code.claude.com/docs/en/code-review.md) passes.

> [!NOTE]
>
> For permission prompts in a Claude Code session, see [Configure permissions](https://code.claude.com/docs/en/permissions.md).

## Find Claude Approvals on a pull request

Approvals adds a check named **Claude Approvals** to the pull requests that it evaluates. The check's title says what's still needed, such as **Waiting on human review from any person (1/2)**. A title that starts with **(observe mode)** means that the policy wasn't enforced when the check ran. In [observe mode](#set-up-claude-approvals), the check shows what your policy would decide.

Claude also posts a comment with the reasons. Where the policy allows it, Claude can post an approving review. For the common titles and what to do about each, see [Find your approval status and what to do next](https://code.claude.com/docs/en/approvals-pull-requests.md#find-your-approval-status-and-what-to-do-next). If a pull request has no check, see [No Claude Approvals check appeared](https://code.claude.com/docs/en/approvals-troubleshooting.md#no-claude-approvals-check-appeared).

## Example policy

You write a policy as a list of rules in `.claude/approvals.yml`.

This policy has one rule, which asks for two people on every change:

```yaml theme={null}
# .claude/approvals.yml
version: 1
mode: observe
rules:
  - purpose: "A change takes two people, and Claude doesn't approve."
    paths: ["**"]
    verdict: { claude: comments, seats: 2 }
    advisory: [claude/code_review]
```

Each part of the policy sets one thing:

* **`mode: observe`**: starts the policy in [observe mode](#set-up-claude-approvals)
* **`purpose`**: says why the rule exists
* **`paths`**: names the files that the rule matches, which here is every file
* **`seats: 2`**: asks for two people, one of whom [can be the author](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts)
* **`claude: comments`**: means that Claude doesn't approve
* **`advisory`**: [keeps automatic Code Reviews](#keep-automatic-code-reviews)

You can also give a rule a condition, which can read facts about the pull request and classifiers' answers:

* **[Facts](https://code.claude.com/docs/en/approvals-policy.md#if) about the pull request**: such as how many lines changed, who opened it, and which branch it targets
* **A [classifier's](https://code.claude.com/docs/en/approvals-classifiers.md) answer**: a model's judgment on a question such as how risky the change is

A condition can't read CI results, so keep CI as its own required check in GitHub.

## Before you turn on Approvals

Before you add a policy file to a repository, check that your organization qualifies and who can turn Approvals on or off. Then see what Approvals changes for merges, Code Review, and billing.

### Availability

Approvals is in public beta for Claude organizations on [Team and Enterprise](https://code.claude.com/docs/en/feature-availability.md#features-that-require-a-claude-subscription) plans, as part of [Claude Ship](https://code.claude.com/docs/en/claude-ship.md). It works on github.com, including GitHub Enterprise Cloud. Compliance settings limit who can use it:

* **Not available**: with [Zero Data Retention](https://code.claude.com/docs/en/zero-data-retention.md) enabled, the [HIPAA configuration](https://code.claude.com/docs/en/hipaa-setup.md) applied, or customer-managed encryption keys (CMEK)
* **Can't start Approvals**: with FERPA or Access Transparency settings

### Who can turn Approvals on or off

Once the [prerequisites](https://code.claude.com/docs/en/approvals-setup.md#prerequisites) are met, anyone who can merge a policy file into the default branch can turn Approvals on. An Owner of the Claude organization can [turn Approvals off](https://code.claude.com/docs/en/approvals-setup.md#turn-off-approvals) for the whole organization, and it then stays off when a policy file merges.

### Merges without human review

A pull request can merge when nobody but its author has looked at it. Check your policy and your GitHub rules for cases such as these:

* **The check isn't required**: the **Claude Approvals** check blocks a merge only where you make it a required check in GitHub, and normally not in observe mode
* **The policy asks for nobody else**: the author can fill a seat, so with `seats: 1` nobody else has to look. With `seats: 0`, a pull request that a bot wrote can merge when no person has looked at it
* **GitHub counts Claude's approval**: where a GitHub branch rule requires one approval, Claude's approving review can be that approval
* **Claude approves with no review**: a rule with `claude: approves` starts no Code Review by itself, so Claude can approve a change that nothing has reviewed. To get a review first, [let Claude approve only when Code Review passes](https://code.claude.com/docs/en/approvals-setup.md#let-claude-approve-when-code-review-passes)

For the other cases, and a rule that asks for a person who isn't an author, see [Merges without human review](https://code.claude.com/docs/en/approvals-github-rules.md#merges-without-human-review).

### Keep automatic Code Reviews

[Code Review](https://code.claude.com/docs/en/code-review.md), another Claude Ship agent, can review each pull request automatically. Adding a policy file can stop those reviews. Where every file that a pull request changes lies under a policy file, automatic reviews normally stop, unless a rule for those files names `claude/code_review`. That holds in [observe mode](#set-up-claude-approvals) and when the policy is enforced.

To keep automatic reviews, [list `claude/code_review` in a rule](https://code.claude.com/docs/en/approvals-policy#advisory), as the [example policy](#example-policy) does under `advisory`.

### Billing for Approvals

Approvals bills your organization's [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans), by tokens, for the Code Reviews and classifier runs that a policy starts. See [what starts a charge](https://code.claude.com/docs/en/approvals-setup.md#what-approvals-costs).

## Set up Claude Approvals

To set up Approvals, start your policy in observe mode, where the **Claude Approvals** check shows what your policy would decide. Reviews and classifier runs are billed in observe mode. For starter policies and the steps, see [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md).

## Related resources

* [Work with Claude Approvals on a pull request](https://code.claude.com/docs/en/approvals-pull-requests.md): check titles and comment commands
* [Approvals and your GitHub rules](https://code.claude.com/docs/en/approvals-github-rules.md): required reviews, CODEOWNERS, and merge queues
* [Policy file reference](https://code.claude.com/docs/en/approvals-policy.md): keys and an example policy
* [Troubleshoot Claude Approvals](https://code.claude.com/docs/en/approvals-troubleshooting.md): when no check appears or a policy file is refused
* [Configure permissions](https://code.claude.com/docs/en/permissions.md): permission prompts in Claude Code
