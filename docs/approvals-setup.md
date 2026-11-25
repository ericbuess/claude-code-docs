> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Set up Claude Approvals

> Turn on Claude Approvals in a GitHub repository: start in observe mode, enforce the policy, require the check, limit what it spends, and turn it off

[Claude Approvals](https://code.claude.com/docs/en/approvals.md) is a check on GitHub pull requests that reports who still has to approve. To turn it on in a repository, commit a [policy file](https://code.claude.com/docs/en/approvals-policy.md) at `.claude/approvals.yml` in the repository's root, on its default branch. Once the file is on the default branch, Approvals can start [billing](#what-approvals-costs).

## Prerequisites

Setting up and enforcing Approvals takes each of these:

* A Claude organization that [qualifies](https://code.claude.com/docs/en/approvals.md#availability), with [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) to pay for the model runs that a policy starts
* The [Claude GitHub App](https://github.com/apps/claude), installed on the repository and [linked to your Claude organization](https://code.claude.com/docs/en/admin-setup.md#connected-github-accounts)
* Permission to merge into the default branch
* Admin access to the repository on GitHub, to require the **Claude Approvals** check. A private repository also needs a [paid GitHub plan](https://docs.github.com/en/get-started/learning-about-github/githubs-plans)
* Two people with write access, before you enforce either policy on this page. Both policies require two people on a change under `.claude/`, which includes the policy file

## Plan your first policy

In a [policy file](https://code.claude.com/docs/en/approvals-policy.md), you set who has to approve a pull request. For your first one, decide whether Claude can approve, then copy the starter policy that matches:

* **[Let Claude approve when Code Review passes](#let-claude-approve-when-code-review-passes)**: a pull request that passes Claude's review usually needs only its author
* **[Keep two people on each change](#keep-two-people-on-each-change)**: a pull request usually needs one person besides the author, and Claude only comments

Both policies start in observe mode, where the **Claude Approvals** check shows what the policy would decide and [normally counts as passing](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-in-observe-mode).

Both also name `claude/code_review`. Keep it in a rule that matches the files you want reviewed, so that [automatic Code Reviews continue](https://code.claude.com/docs/en/approvals.md#keep-automatic-code-reviews) in observe mode and once you enforce.

> [!TIP]
>
> To have Claude write or change a policy file for you, type [`/claude-approvals`](https://code.claude.com/docs/en/commands) at the Claude Code prompt in your repository, followed by what you want. Requires Claude Code v2.1.331 or later and [feature-flag fetching](https://code.claude.com/docs/en/env-vars.md#features-that-need-feature-flag-fetching).

### Let Claude approve when Code Review passes

Once you enforce this starter policy, a pull request that passes Claude's review usually needs only its author, except for changes under `.claude/`. Other pull requests usually need one person [besides the author](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts).

In this policy, the first rule asks for two people on a change. Its `override` lowers that to one and lets Claude approve when `claude/code_review` reads `pass`. The second rule asks for two people on a change under `.claude/`:

```yaml theme={null}
# .claude/approvals.yml
version: 1
mode: observe
rules:
  - purpose: "A change takes two people. When Claude's review passes, one is enough and Claude approves."
    paths: ["**"]
    verdict: { claude: comments, seats: 2 }
    override:
      - { if: "claude/code_review = pass", verdict: { claude: approves, seats: 1 } }
  - purpose: "A change to the review rules takes two people."
    paths: ["**/.claude/**"]
    nested: inherit
    verdict: { claude: comments, seats: 2 }
```

This policy can start a billed Code Review at each push, and observe mode is billed. If your [Code Review settings](https://code.claude.com/docs/en/code-review-setup.md#set-when-reviews-run) ask for fewer reviews, the policy adds to them.

### Keep two people on each change

Use this starter policy to ask for two people on each change. Once you enforce it, a pull request usually needs one person besides the author, and Claude only comments.

In this policy, both rules ask for two people. The first rule lists `claude/code_review` under [`advisory`](https://code.claude.com/docs/en/approvals-policy#advisory), so reviews follow your Code Review settings:

```yaml theme={null}
# .claude/approvals.yml
version: 1
mode: observe
rules:
  - purpose: "A change takes two people."
    paths: ["**"]
    verdict: { claude: comments, seats: 2 }
    advisory: [claude/code_review]
  - purpose: "A change to the review rules takes two people."
    paths: ["**/.claude/**"]
    nested: inherit
    verdict: { claude: comments, seats: 2 }
```

## Turn on Approvals in observe mode

Add your policy file in a pull request of its own, then open a second pull request to see the **Claude Approvals** check:

**1. Add the policy file**

In a pull request of its own, from a branch in the repository, add the policy at `.claude/approvals.yml` in the repository's root.

**2. Merge the pull request**

Merge when Claude comments that it "found the policy file in this change valid". If the file is invalid, a failed check titled **This change breaks a policy file** appears. [Fix it](https://code.claude.com/docs/en/approvals-troubleshooting.md#fix-a-policy-file-that-approvals-refuses) in this pull request.

**3. Open another pull request**

Open one into the default branch that isn't a draft. A **Claude Approvals** check appears with a title that starts **(observe mode)**.

If nothing appears, see [No Claude Approvals check appeared](https://code.claude.com/docs/en/approvals-troubleshooting.md#no-claude-approvals-check-appeared).

## Enforce your policy and require Claude Approvals

Enforce the policy once the **Claude Approvals** check titles that you see in observe mode match what your reviewers decide. From then on, the check can block a merge, and [Claude can approve](https://code.claude.com/docs/en/approvals-github-rules.md#merges-without-human-review) where the policy allows it.

### Decide which files and branches to protect

Before you [switch your policy from observe mode to enforcement](#switch-from-observe-mode-to-enforcement), decide which files need a person, which branches the check gates, and when to change GitHub's required approvals:

* **Files**: decide which ones need a person's approval whatever Claude finds, then copy [this rule](https://code.claude.com/docs/en/approvals-github-rules.md#ask-for-a-person-who-isn’t-an-author) and narrow its `paths` list
* **Branches**: an enforced policy also covers pull requests into branches other than the default branch, so list each branch whose merges the **Claude Approvals** check should gate. On those branches, a pull request with no covered file gets no check, so a required check waits
* **GitHub's required approvals**: [change the number of approvals that GitHub requires](https://code.claude.com/docs/en/approvals-github-rules.md#required-reviews-and-codeowners) only after the last step of the switch

### Switch from observe mode to enforcement

A policy file's [`mode`](https://code.claude.com/docs/en/approvals-policy#top-level-keys) key is one of these:

* **`observe`**: the **Claude Approvals** check shows what the policy would decide, Claude doesn't approve, and the check [normally counts as passing](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-in-observe-mode)
* **`enforce`**: the check can block a merge, and Claude can approve where the policy allows it. This is the default, so a policy file with no `mode` line is enforced

To enforce your policy, follow these steps. After the first step, an open pull request can keep a check that GitHub counts as passing until you rerun Approvals on it. Keep open pull requests out of the merge queue until you have rerun Approvals on them in step 2.

**1. Delete the mode: observe line**

Delete `mode: observe` and merge that change.

**2. Rerun Approvals on open pull requests**

Five minutes after the merge, comment `@claude approvals rerun` on each one whose check title starts with **(observe mode)** or **Observe mode ended**. On a pull request from a fork, [read the change first and add the latest commit's full SHA](https://code.claude.com/docs/en/approvals-pull-requests.md#pull-requests-from-forks-and-outside-contributors).

**3. Require Claude Approvals in GitHub**

For the default branch and each branch you listed, [require status checks to pass](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#require-status-checks-before-merging) and add **Claude Approvals**. As its source, select the Claude app that reported it.

**4. Confirm that Approvals blocks a merge**

Open a pull request that changes a file under `.claude/`. When the check finishes, the title reads **Waiting on human review from any person (1/2)**, and GitHub's merge box lists the check as required.

Approvals later evaluates some of the pull requests that you didn't rerun, which can start [billed runs](#what-approvals-costs).

### Set the source that GitHub accepts for Claude Approvals

Set the required check's source to the Claude app. If you allow **any source**, GitHub accepts a check named **Claude Approvals** from elsewhere. To set the source through GitHub's API, put the Claude app's ID, `1236702`, in `integration_id` in a ruleset or `app_id` in a branch protection rule.

## Control what Approvals spends

Approvals bills your organization's usage credits for the model runs that a policy starts, and observe mode is billed. Billing can start, and [continues, while usage credits are turned off](https://code.claude.com/docs/en/claude-ship.md#how-each-claude-ship-agent-is-billed). To keep any policy file from starting billing, an Owner can [turn off Approvals](#turn-off-approvals) for the whole organization.

### What Approvals costs

A policy with `claude/code_review` in an `if` condition can start a [billed Code Review](https://code.claude.com/docs/en/code-review-costs.md) when a pull request opens and at each push. To stop those reviews, move it from the conditions to `advisory`. When `claude/code_review` is only under `advisory`, with no [`level`](https://code.claude.com/docs/en/approvals-classifiers#read-a-classifier’s-answer-from-a-rule), reviews follow your Code Review settings.

A rule can also read other [classifiers](https://code.claude.com/docs/en/approvals-classifiers.md). For `claude/diff` and custom classifiers, each [run that calls a model](https://code.claude.com/docs/en/approvals-classifiers.md#what-a-classifier-run-costs) is billed. To limit each run of a custom classifier, set its [`budget`](https://code.claude.com/docs/en/approvals-classifiers#budget) key.

### Limit what a policy costs

To cap what your organization pays for the Code Reviews and classifier runs that a policy starts, set a spend limit. Set any of these limits at [**Organization settings > Usage**](https://claude.ai/admin-settings/usage), which takes an Owner role:

* **Your organization's spend limit for usage credits**: covers Approvals
* **Code Review's spend limit**: covers a policy's reviews together with Code Review's other reviews. Under **Services**, open the **Claude Code Review** row's menu and select **Edit spend limit**
* **Classifier runs' spend limit**: under **Services**, open the Approvals row's menu and select **Edit spend limit**. The row has no limit when it appears

On that page, the **Claude Code Review** row under **Services** can start without a limit:

* **The row shows a dash where the limit goes**: a monthly limit is set for you when a policy's first billed review starts. Change it once the amount shows
* **Code Review was turned on before your policy**: the row has no limit until you set one

If a reseller bills your organization, ask your reseller for a limit.

At Code Review's limit, a check that needs Claude's review can stop passing. Raise the limit or wait for the [next billing period](https://code.claude.com/docs/en/code-review-costs.md#limit-your-spend).

## Turn off Approvals

You can turn off Approvals for one repository, for a GitHub organization, or for your whole Claude organization.

> [!WARNING]
>
> Suspend or uninstall the Claude GitHub App, or unlink your GitHub organization, only after you turn off Approvals. If you take any of those steps first, a required **Claude Approvals** check can block merges. GitHub can also continue to count Claude's approving reviews that are left on open pull requests.

Follow this order:

1. **Check how GitHub treats stale approvals**: where GitHub requires approvals, turn on [**Dismiss stale pull request approvals when new commits are pushed**](https://code.claude.com/docs/en/approvals-github-rules.md#required-reviews-and-codeowners). Otherwise, GitHub can continue to count Claude's approving review after a new push, until you dismiss the review in the last step.
2. **Stop requiring the check**: in GitHub, remove **Claude Approvals** from the required checks of each branch protection rule and ruleset.
3. **Turn Approvals off**: [choose how](#ways-to-turn-off-approvals), by the scope that you want.
4. **Dismiss Claude's reviews**: on open pull requests that Claude approved, dismiss that review in GitHub.

To keep Approvals on and stop the check from blocking, first stop requiring it on branches other than the default branch. Then put `mode: observe` in every policy file. The check then [normally stops blocking](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-in-observe-mode), and classifiers still run and bill.

### Ways to turn off Approvals

To turn off Approvals, find the scope that you want in this table:

| Scope | How to turn off Approvals |
| :- | :- |
| One repository, without an Owner | Delete every policy file from the default branch |
| A GitHub organization, or a repository whose **Edit** dialog shows **Claude Approvals** | With an [Owner role](https://code.claude.com/docs/en/server-managed-settings.md#access-control), go to [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship), click **Edit** on its row, and turn off **Claude Approvals** |
| The whole Claude organization | With an Owner role, go to [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship) and click **Block globally** in the **Approve** row. To turn it back on, click **Allow policy files** in the same row |

After you turn off Approvals for the whole Claude organization, it stays off when a policy file merges later. If you're turning off Code Review too, turn off Approvals first, because a policy can start billed reviews where Code Review is off.

## Related resources

* [Claude Approvals policy file reference](https://code.claude.com/docs/en/approvals-policy.md): keys and an example policy
* [Approvals and your GitHub rules](https://code.claude.com/docs/en/approvals-github-rules.md): what can merge without a person, and who can change the policy
* [Troubleshoot Claude Approvals](https://code.claude.com/docs/en/approvals-troubleshooting.md): when no check appears, or the check refuses a policy file
