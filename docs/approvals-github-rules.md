> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Approvals and your GitHub rules

> See how the Claude Approvals check works with required reviews, CODEOWNERS, and merge queues, what can merge with no person, and who can change a policy

[Claude Approvals](https://code.claude.com/docs/en/approvals.md) adds a check to the GitHub pull requests that it evaluates. The check reports who has to approve a pull request, following a [policy](https://code.claude.com/docs/en/approvals-policy.md), a file in your repository. The check blocks a merge only where you make it a required check in GitHub, and your branch rules decide what merges.

If you administer a repository or review its security, check how your policy and your GitHub settings work together before you [enforce the policy](https://code.claude.com/docs/en/approvals-setup.md#enforce-your-policy-and-require-claude-approvals):

* **[Merges without human review](#merges-without-human-review)**: settings that let a pull request merge with no review but its author's, and a rule that asks for a person who isn't an author
* **[Required reviews and CODEOWNERS](#required-reviews-and-codeowners)**: how GitHub's own review rules count Claude's approving review, and what to set
* **[Auto-merge and merge queues](#auto-merge-and-merge-queues)**: what can merge without anyone acting
* **[Who can change or loosen a policy](#who-can-change-or-loosen-a-policy)**: who can edit the policy file, stop requiring the check, or steer a classifier's answer

## Merges without human review

With Approvals on, a pull request can merge with no person but its author looking at it, or with no person at all if a bot wrote it. That can happen if GitHub doesn't require the **Claude Approvals** check. It can also happen if the check passes with no person besides the author, for example with:

* `seats: 0`
* `seats: 1`, which the author can fill
* A [`from` list](https://code.claude.com/docs/en/approvals-policy#people-lists) that admits bots
* A machine user, a user account that a script or an agent drives, which [can count as a person](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts)
* A [`reuse`](https://code.claude.com/docs/en/approvals-policy#reuse) that keeps seats after a push
* Files that no rule covers, where GitHub counts the neutral result as passing
* A condition that reads a [classifier's](https://code.claude.com/docs/en/approvals-classifiers.md) answer, in a rule's `if`, an override's `if`, or a `reuse`. That answer is one that [a pull request's text can steer](#classifier-answers-that-a-pull-request-can-steer)

A push directly to the default branch gets no check. Require pull requests there in GitHub.

Claude's [approving review](https://code.claude.com/docs/en/approvals.md#find-claude-approvals-on-a-pull-request) can meet a GitHub branch rule that requires one approval.

### Ask for a person who isn't an author

To have the **Claude Approvals** check ask for one person who isn't an author on every path, add this file's rule to a root [policy file](https://code.claude.com/docs/en/approvals-policy.md) that you [enforce](https://code.claude.com/docs/en/approvals-setup.md#enforce-your-policy-and-require-claude-approvals):

```yaml theme={null}
# .claude/approvals.yml
version: 1
rules:
  - purpose: "A change takes one person who isn't an author."
    paths: ["**"]
    nested: inherit
    verdict:
      claude: comments
      seats: [{ count: 1, from: [humans, "!pr/authors"] }]
    advisory: [claude/code_review]
```

Each part of that rule does a job:

| Part of the rule | What it does |
| :- | :- |
| No `if` or `override` | No classifier's answer changes the rule |
| `claude: comments` | Approvals doesn't post Claude's approval |
| `nested: inherit` | The rule also applies under [policy files in subdirectories](https://code.claude.com/docs/en/approvals-policy.md#policy-files-in-subdirectories) |
| `humans` | A [machine user](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts), a user account that a script or an agent drives, can fill this seat. To keep one out, add its login, as in `[humans, "!pr/authors", "!acme-ci"]` |
| `"!pr/authors"` | Excludes the pull request's authors. On a [fork's pull request](https://code.claude.com/docs/en/approvals-pull-requests.md#pull-requests-from-forks-and-outside-contributors), no approval counts toward this seat |
| `advisory` | [Keeps automatic Code Reviews](https://code.claude.com/docs/en/approvals.md#keep-automatic-code-reviews) |

For paths that need more people, copy the rule, narrow `paths`, and raise `count`.

## Required reviews and CODEOWNERS

Check how each GitHub setting works beside your policy, and what to set:

| GitHub setting | How it works with Approvals | What to do |
| :- | :- | :- |
| Required approvals | GitHub can count Claude's approving review as one approval. GitHub doesn't count an author who fills a seat, or an [`@claude approve`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals) comment | Where you require the **Claude Approvals** check, require no more than one approval in GitHub, and ask for more people in `seats`. Otherwise a pull request can stay blocked after the **Claude Approvals** check passes |
| CODEOWNERS | A branch rule can require a Code Owner's review | To name owners in your policy, use a [people list](https://code.claude.com/docs/en/approvals-policy.md#people-lists) in `seats` on their paths |
| Stale approvals | Claude posts its approving review on one commit, and GitHub can continue to count that review until it's dismissed. Approvals normally asks GitHub to dismiss the review when Approvals evaluates the next push, and GitHub can [refuse](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-waits-for-people) | Where GitHub requires approvals, turn on **Dismiss stale pull request approvals when new commits are pushed** or **Require approval of the most recent reviewable push** |

## Auto-merge and merge queues

If you use GitHub auto-merge or a merge queue with a policy that doesn't require a person's approval, a change can merge without anyone acting. To have the check ask for a person who isn't an author on every path, [add this rule](#ask-for-a-person-who-isn’t-an-author), and require the **Claude Approvals** check.

Approvals doesn't evaluate the commits that a merge queue creates:

* **The queue's commits**: Approvals normally marks them as passed, with the title **Stamped for merge queue**, except for a pull request that was evaluated only in [observe mode](https://code.claude.com/docs/en/approvals-pull-requests.md#approvals-in-observe-mode)
* **Entry to the queue**: GitHub's own rule decides it, normally after the pull request's required checks pass. A pull request can also enter while the check is still running. If the check doesn't pass after that, remove the pull request from the queue
* **Pull requests that were only observed**: after you start enforcing the policy, [rerun the check](https://code.claude.com/docs/en/approvals-setup.md#enforce-your-policy-and-require-claude-approvals) on each open pull request before you queue it. Until its latest commit passes under the policy, its commit in the queue normally gets no check, and where the check is required, it can wait there
* **The app's permission**: ask an owner of your GitHub organization to accept the Claude GitHub App's [**Merge queues** permission](https://code.claude.com/docs/en/github-actions.md#github-app-permissions). Without it, the queue's commits get no check, so where GitHub requires the check, entries wait

## Who can change or loosen a policy

A policy is a file in your repository, so your GitHub permissions decide who can change it.

| Who | What they can do |
| :- | :- |
| Anyone who can merge into the default branch | Change a policy file. A policy file is a [protected file](https://code.claude.com/docs/en/approvals-policy.md#protected-files): a pull request that changes it can need a person with write access, who can be the pull request's author. A [machine user](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts) counts as a person |
| A GitHub repository admin | Stop requiring the **Claude Approvals** check in the repository's own branch rules |
| Anyone who can bypass every rule that requires the check | Merge past the check |
| An [Owner role](https://code.claude.com/docs/en/server-managed-settings.md#access-control) in the Claude organization | [Turn off Approvals](https://code.claude.com/docs/en/approvals-setup.md#turn-off-approvals) for a GitHub organization, a repository whose **Edit** dialog shows **Claude Approvals**, or the whole Claude organization |

### Classifier answers that a pull request can steer

Approvals applies the policy files and your classifier definitions from the default branch. A pull request's [author's text](https://code.claude.com/docs/en/approvals-classifiers.md#what-a-classifier-run-can-read-and-change) can steer a classifier's answer.

Where a rule's `if`, an override's `if`, or a `reuse` condition reads an answer, a steered answer can lower what the pull request needs. To ask for one person who isn't an author on every path, [add this rule](#ask-for-a-person-who-isn’t-an-author).

## Related resources

* [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md): enforce a policy and require the **Claude Approvals** check
* [Claude Approvals policy file reference](https://code.claude.com/docs/en/approvals-policy.md): seats, people lists, and protected files
* [Claude Approvals classifiers](https://code.claude.com/docs/en/approvals-classifiers.md): what a classifier's run can read and change
