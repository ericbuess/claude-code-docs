> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshoot Claude Approvals

> Fix a Claude Approvals check that didn't appear or doesn't pass, a policy file that Approvals refuses, and a classifier that gives no answer

[Claude Approvals](https://code.claude.com/docs/en/approvals.md) is a check on GitHub pull requests that reports who still has to approve. Start here when the check didn't appear or doesn't pass, when Approvals refuses a policy file, or when a classifier gives no answer.

If the **Claude Approvals** check on your pull request has a title that isn't covered here, see [Find your approval status and what to do next](https://code.claude.com/docs/en/approvals-pull-requests.md#find-your-approval-status-and-what-to-do-next).

## No Claude Approvals check appeared

When [Claude Approvals](https://code.claude.com/docs/en/approvals.md) can't run, it can post nothing at all.

### Check your pull request and policy file

Start with the causes that you can check yourself:

| Cause | What to do |
| :- | :- |
| The pull request is a draft | Mark it ready for review |
| The [policy file](https://code.claude.com/docs/en/approvals-policy.md#where-to-put-a-policy-file) isn't where Approvals looks | Put it at `.claude/approvals.yml` in the repository's root, on the default branch, with `version: 1` |
| Nothing has happened since the file merged | Push a commit to the pull request |
| The policy is in observe mode, and the pull request targets a branch other than the default branch | Expect no check, unless the pull request changes a policy or classifier file |
| The policy is enforced, and no rule covers any file that the pull request changes | See [what happens when no rule covers a file](https://code.claude.com/docs/en/approvals-policy.md#how-rules-combine-into-one-verdict) |

### Claude left a comment and no Approvals check

Find the words of Claude's comment, then take the step beside them:

| Comment says | What to do |
| :- | :- |
| Approvals "did not run on this change" | Do what the comment says. One cause is a pull request that moves a file into or out of the paths that the policy's rules cover. Make that move in two pull requests, one that adds the file under its new name and one that removes the old one |
| "More than one Claude organization is connected to this GitHub account" | Ask an Owner of the Claude organization that should run Approvals to click **Connect** next to the repository's GitHub organization on [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship). Then push a commit |
| "Claude Approvals can't start in this repository yet" | Tell an Owner that the organization has no usage credits available |

### Ask an Owner to check your Claude organization

Ask an Owner to check each of these for your Claude organization:

| What to check | Where |
| :- | :- |
| Whether the organization qualifies | [Availability](https://code.claude.com/docs/en/approvals.md#availability) |
| Whether the [Claude GitHub App](https://github.com/apps/claude) can access the repository and is linked | [**Organization settings > Git providers**](https://claude.ai/admin-settings/source-control) |
| Whether Approvals is turned off here | The **Approvals** column and the **Approve** row on [**Organization settings > Claude Ship**](https://claude.ai/admin-settings/claude-ship) |

## Approvals doesn't pass after you resolve a review thread

Check whether your policy's [`findings`](https://code.claude.com/docs/en/approvals-policy#findings) list names you.

If your resolve doesn't count, push a fix, or ask someone on the list to resolve the thread.

## Approvals passed and GitHub still blocks merging

Read the rule that GitHub's merge box names. If it asks for a review, GitHub's branch rules require one that the policy doesn't, so have someone other than the author approve in a GitHub review. For what GitHub counts, see [Required reviews and CODEOWNERS](https://code.claude.com/docs/en/approvals-github-rules.md#required-reviews-and-codeowners).

## Fix a policy file that Approvals refuses

Find the **Claude Approvals** check's title in this table:

| Title | Copy at fault | Messages | What to do |
| :- | :- | :- | :- |
| **This change breaks a policy file** | The pull request's own | **Policy files in this change**, in the check's summary | Fix it in this pull request |
| **Default branch policy file cannot be used**, **Default branch policy file must be version 1**, **Default branch policy file is too large** | The root policy file on the default branch | The check's summary | Fix it in a new pull request from a branch of this repository. Its **Policy files in this change** shows whether the new copy loads. That pull request's check fails, as every pull request's check does, in observe mode or enforced. Where the branch requires the check, ask someone who can bypass the branch rules to merge it |
| **A policy file cannot be used** | A directory's policy file on the default branch | The check's summary | Fix it as you would the root policy file |

After the fix merges, allow five minutes, then comment [`@claude approvals rerun`](https://code.claude.com/docs/en/approvals-pull-requests#comment-commands-for-approvals) on each open pull request whose check hasn't updated. On one from a fork, [read the change first and add the latest commit's full SHA](https://code.claude.com/docs/en/approvals-pull-requests.md#pull-requests-from-forks-and-outside-contributors).

### Policy file refusal messages

One refusal makes the whole policy file unusable, and a warning fails nothing.

Find the beginning of your message here:

| Message | Fix |
| :- | :- |
| "no key of this name is read at this place" | Check the key's spelling and its level against [Top-level keys](https://code.claude.com/docs/en/approvals-policy.md#top-level-keys) and [Rule keys](https://code.claude.com/docs/en/approvals-policy.md#rule-keys) |
| "this names no fact and no usable classifier" | Check the name against the [facts](https://code.claude.com/docs/en/approvals-policy.md#if). For `repo/<name>`, check that `.claude/classifiers/<name>/def.yml` loads, beside the policy file or in a directory above it |
| "a condition has no NOT" | Write the opposite operator |
| "no local has this name" | Define the local in this file or a policy file above it. Write a login or a team with no `@` |
| "this is not YAML" | Look near the line that the message names for a quote or bracket that doesn't close, or a tab. Indent with spaces |

## A classifier gave no answer or its definition is refused

To see each [classifier](https://code.claude.com/docs/en/approvals-classifiers.md) run's state and the reason for a missing answer, open **Classifier results** in Claude's comment on the pull request. If a run reached its budget, split the pull request, or raise a `time` or `cost` that is under its [maximum](https://code.claude.com/docs/en/approvals-classifiers.md#budget).

Then find the **Claude Approvals** check's title here:

| Title | What to do |
| :- | :- |
| **A classifier definition is not valid**, or **This change breaks a policy file** where a policy file names the classifier | Fix the definition in this pull request. The refusal messages are under **Policy files in this change** |
| **A classifier's definition cannot be used** | Fix the definition on the default branch. A pull request that changes it shows why it's refused |
| **Cannot evaluate: classifier outside advisory** | With a policy file in a subdirectory, some custom classifiers [belong only under `advisory`](https://code.claude.com/docs/en/approvals-policy#policy-files-in-subdirectories). Move the classifier there |
| **repo/change\_risk reached its run limit**, with your classifier's name, or **A classifier reached its run limit** | Push a change to the diff. Or comment `@claude approvals rerun` for one more run, which can drop every classifier's result, passing ones too |

## Related resources

* [Work with Claude Approvals on a pull request](https://code.claude.com/docs/en/approvals-pull-requests.md): check titles and comment commands
* [Set up Claude Approvals](https://code.claude.com/docs/en/approvals-setup.md): requirements, the starter policy, and the required check
* [Claude Approvals policy file reference](https://code.claude.com/docs/en/approvals-policy.md): the policy file's keys
