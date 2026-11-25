> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Work with Claude Approvals on a pull request

> Find what a Claude Approvals check title means and what to do next, use the comment commands, and handle pull requests from Claude and from forks

Where [Claude Approvals](https://code.claude.com/docs/en/approvals.md) is on, it adds a check named **Claude Approvals** to the pull requests that it evaluates. The check reports who still has to approve the pull request, following a [policy file](https://code.claude.com/docs/en/approvals-policy.md) in the repository. Where your repository requires the check, GitHub can block the merge until it passes. If your pull request has no check, for example because it's a draft, see [No Claude Approvals check appeared](https://code.claude.com/docs/en/approvals-troubleshooting.md#no-claude-approvals-check-appeared).

## Get your pull request through Claude Approvals

Approvals evaluates your pull request after events such as a push or an approval. It reports the result in two places on the pull request:

* **The Claude Approvals check**: in the list of checks at the bottom of the **Conversation** tab. The text beside its name, called its title, gives the approval status, such as **Waiting on human review from any person (1/2)**
* **Claude's comment**: in the conversation, with the reasons for the result. Approvals edits the same comment as the result changes, so it stays where it first appeared

To get to a passing check:

1. **Read the approval status**: the check's title says where your pull request stands, for example who still has to approve
2. **Do what the status calls for**: [find the title](#find-your-approval-status-and-what-to-do-next) to see what that is. For example, ask someone with write access to approve, fix the findings that Code Review posted, or wait for a review to finish
3. **Read the status again**: the title can change at the next evaluation, such as when someone approves or you push. After a push that changes the diff, [earlier approvals can stop counting](https://code.claude.com/docs/en/approvals-policy.md#earlier-approvals-after-a-new-push)
4. **Merge**: once the check passes, merge as your repository's GitHub rules allow. Where the policy allows it, Claude can also post an approving review

## Find your approval status and what to do next

The **Claude Approvals** check gives your pull request's approval status in its title, the text beside its name in the list of checks. Find your check's title in these tables to see what it means and what to do next.

For any other title, open the **Claude Approvals** check's summary, which gives the cause and the next step. To find who maintains the policy file, `.claude/approvals.yml`, see who last changed it on the default branch.

### Approvals waits for people

With these titles, Approvals is waiting for a person. Outside observe mode, GitHub lists the **Claude Approvals** check among its pending checks, marked **Action required**.

| Title | What to do |
| :- | :- |
| **Waiting on human review from any person (1/2)** | Ask someone with write access to approve. The numbers are the approvals counted so far and the approvals that the policy asks for, and the author usually [counts as one](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts) already. In place of "any person", the title can name the people or the team that a rule asks for, or name nobody |
| **Changes requested** | Have the reviewer who requested changes approve, or have a person dismiss their review |
| **Claude's approval still stands; dismiss it** | [Dismiss Claude's review](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/dismissing-a-pull-request-review), or ask someone who may dismiss reviews on the branch. GitHub didn't let Approvals dismiss it |

### Approvals waits for Code Review or a classifier

With these titles, Approvals needs an answer from [Code Review](https://code.claude.com/docs/en/code-review-pull-requests.md) or a [classifier](https://code.claude.com/docs/en/approvals-classifiers.md):

| Title | What to do |
| :- | :- |
| **Waiting for Code Review**, **Waiting for repo/change\_risk**, **Waiting for classifiers** | Wait for the result |
| **A classifier had no result**, **A classifier has not run**, or a name in place of "A classifier", as in **repo/change\_risk has not run** | [Rerun the Claude Approvals check](#comment-commands-for-approvals). See [what a rule sees without an answer](https://code.claude.com/docs/en/approvals-classifiers.md#what-a-rule-sees-when-a-classifier-run-gives-no-answer) |

### A rule or a policy file keeps Approvals from passing

With these titles, a rule holds the pull request or the policy needs a fix:

| Title | What to do |
| :- | :- |
| **Held by Code Review's findings** | Fix the findings that Code Review posted on the pull request, then push. If the policy's [`findings`](https://code.claude.com/docs/en/approvals-policy#findings) list names you, you can resolve the findings' threads. If the **Claude Approvals** check is still held after you resolve them, push a fix |
| **Held by** and a rule's purpose in quotes, **Held by a policy rule** | Ask whoever maintains the policy file what the rule in the check's summary needs, then push a fix |
| **No rule applies to** and a file's name in quotes, **No rule applies to a changed file** | Ask whoever maintains the policy file for a rule with no `if` that covers the file. Rerun the check once that rule merges |
| **This change breaks a policy file**, **Default branch policy file cannot be used** | [Fix the policy file](https://code.claude.com/docs/en/approvals-troubleshooting.md#fix-a-policy-file-that-approvals-refuses) |

A failed Code Review from an earlier commit can still hold the check after you push a fix. If no new review starts, post a new comment with only [`@claude review`](https://code.claude.com/docs/en/code-review-pull-requests#comment-commands), which takes write access.

### Approvals passed or nothing ran

With these titles, Approvals passed or didn't evaluate the pull request:

| Title | What to do |
| :- | :- |
| **Passed; no approval from Claude** | If GitHub requires an approval, ask a person |
| **Nothing ran, not blocking: no file is covered** | If someone should review the files that the pull request changes, ask whoever maintains the [policy file](https://code.claude.com/docs/en/approvals-policy.md) to cover them |
| **Observe mode ended: not evaluated yet** | Push a commit or [rerun the Claude Approvals check](#comment-commands-for-approvals). If it passes, a pull request with auto-merge on or in a merge queue can merge at once |

If you see **Passed; no approval from Claude**, check for causes such as these:

* A rule says `claude: comments`
* A changed file has no rule, or is a [symlink, submodule pointer, or `.gitattributes` file](https://code.claude.com/docs/en/approvals-policy#protected-files)
* `claude[bot]` opened the pull request, unless the [Claude Approvals GitHub App](#pull-requests-that-claude-opens) is installed and linked

## Approvals in observe mode

In observe mode, the **Claude Approvals** check ends neutral, which GitHub counts as passing, with a title that starts **(observe mode)**.

The check can wait, fail, be withheld, or be missing in cases such as these:

| Case | What the check does |
| :- | :- |
| The pull request changes a policy or classifier file | It can wait for one person, who can be the author. It fails if the change breaks one of those files |
| The default branch's policy file can't be used | It fails until you [fix the policy file](https://code.claude.com/docs/en/approvals-troubleshooting.md#fix-a-policy-file-that-approvals-refuses) |
| The title says Withheld | Approvals holds back a passing check, for example because another open pull request has the same latest commit. Read the check's summary for what clears it |
| The pull request targets another branch than the default | No check appears, unless the pull request changes a policy or classifier file |

## Comment commands for Approvals

To use a command, post it as a new comment on the pull request. You need write access to the repository. A 😕 reaction on your comment means that the command wasn't carried out in full.

| Command | What it does |
| :- | :- |
| `@claude approvals rerun` | Evaluates the latest commit again. Classifiers can run again, and are billed. Put it alone on the comment's first line. On a fork's pull request, [read the change first, then add the latest commit's full SHA and make that the comment's only text](#pull-requests-from-forks-and-outside-contributors) |
| `@claude approve` | Can count as your approval of the latest commit, for the **Claude Approvals** check. To name a commit, add its full SHA, which a pull request from a fork requires. Make it the comment's only text |
| `@claude approvals resolve <ids>` | Can close the findings with those IDs, if the policy's [`findings`](https://code.claude.com/docs/en/approvals-policy#findings) list names you. Put it alone on the first line, with one to eight finding IDs such as `f-1a2b3c4d` |

Approvals can also act on `@claude approvals rerun` from a GitHub App's bot account. That comment starts an evaluation, where classifiers can run and are billed, and doesn't vouch for a [fork's commit](#pull-requests-from-forks-and-outside-contributors).

Comment `@claude approve` on your own pull request when the check's summary says that you [don't count as an approval](https://code.claude.com/docs/en/approvals-policy.md#whether-a-pull-request’s-author-counts). To withdraw that approval, edit or delete each of your `@claude approve` comments. Approvals doesn't count an edited comment as an approval, so to approve again, post a new comment.

## Pull requests from Claude, forks, and outside contributors

Before Claude can approve a pull request that `claude[bot]` opened, you need a second GitHub App. A pull request from a fork, or from a person without write access, can need a maintainer.

### Pull requests that Claude opens

Until you add a second GitHub App, the **Claude Approvals** check on a pull request that `claude[bot]` opened can pass with the title **Passed; no approval from Claude**.

To get Claude's approval on those pull requests, add a second app:

1. **Install it**: ask an owner of your GitHub organization to install the [Claude Approvals GitHub App](https://github.com/apps/claude-approvals/installations/new) on the repository.
2. **Link it**: ask someone who is an owner of the GitHub organization and an Owner or Primary Owner of the Claude organization to [link the app to your Claude organization](https://claude.ai/settings/claude-approvals/github/finish). If they can't link it, contact [Anthropic support](https://support.claude.com).

Then [rerun the check](#comment-commands-for-approvals) on an open pull request that `claude[bot]` opened. Leave the required check's source as it is, because the [Claude GitHub App](https://github.com/apps/claude) still reports the check.

### Pull requests from forks and outside contributors

On a fork's pull request, Approvals can wait for a maintainer, meaning someone with write access:

* **Until a maintainer vouches for a commit**: no classifier's answer counts, Code Review's included. Where a rule depends on one, the **Claude Approvals** check's title can read **No classifier result counts on this commit**.
* **To vouch for a commit**: outside observe mode, if you have write access, read the change. Then comment `@claude approvals rerun` followed by the latest commit's full SHA, as the comment's only text. Classifiers can then run for that commit. With no SHA, the command can cover the commit that was latest when you commented.
* **A pass waits for a maintainer**: outside observe mode, where a rule covers a changed file, the check also needs approval from someone with write access who didn't open the pull request. That applies to a fork's pull request, and to one that a person without write access opened. Until then, Claude doesn't approve
* **A rule with `"!pr/authors"`**: no approval counts toward it on a fork's pull request, and once someone approves, the check's title can read **Cannot tell who wrote this change**. The check's summary says what whoever maintains the policy file can change

## Related resources

* [Claude Approvals](https://code.claude.com/docs/en/approvals.md): what a policy is and what it affects
* [Troubleshoot Claude Approvals](https://code.claude.com/docs/en/approvals-troubleshooting.md): when no check appears, or the check doesn't pass
* [Claude Approvals policy file reference](https://code.claude.com/docs/en/approvals-policy.md): the keys that a check's summary names
