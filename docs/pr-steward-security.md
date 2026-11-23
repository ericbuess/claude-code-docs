> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# What PR Steward can access

> Check which GitHub identity, permissions, and repositories PR Steward uses, where its sessions run, and what limits approvals and merges

[PR Steward](https://code.claude.com/docs/en/pr-steward.md) is an agent that works on your team's open GitHub pull requests. It acts on GitHub as the [Claude GitHub App](https://github.com/apps/claude) and works on each pull request in a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md). On GitHub Enterprise Server, it acts as [the app that your organization created](https://code.claude.com/docs/en/github-enterprise-server.md#admin-setup).

The access and limits here are those of a session in an Anthropic-hosted environment. For a self-hosted one, see [Run PR Steward in a self-hosted environment](https://code.claude.com/docs/en/pr-steward-setup.md#run-pr-steward-in-a-self-hosted-environment). For how session data is handled, see [Data usage](https://code.claude.com/docs/en/data-usage.md).

## PR Steward's identity and permissions

Check what a PR Steward session can reach on GitHub, then how the session itself is set up.

### PR Steward's GitHub access

As its GitHub App, a PR Steward session acts on GitHub with these repositories, permissions, and token:

| Topic | What PR Steward uses |
| :- | :- |
| Repositories | A session starts with the pull request's own repository, which it reads and writes. GitHub search on github.com can return results from other github.com repositories that your organization has added for PR Steward. A session can fetch public repositories on github.com |
| Permissions | Read and write on contents, pull requests, and issues. Where your installation of the app grants them, it also has read on checks and statuses and write on Actions. On github.com, the installation can also grant write on workflows, which lets PR Steward push changes to workflow files. See the app's [permission list](https://code.claude.com/docs/en/github-actions.md#github-app-permissions) |
| Token | The app's token is kept outside the session's sandbox. By default, the session's `gh` and `git` requests go through Anthropic's service, which adds the token |

### PR Steward's session environment

Check where a PR Steward session runs, how it handles permission prompts, and which comments and instruction files it reads:

| Topic | How a session works |
| :- | :- |
| Where the code runs | In a [cloud session](https://code.claude.com/docs/en/claude-code-on-the-web.md). See [the environment that PR Steward runs in](https://code.claude.com/docs/en/pr-steward-setup.md#choose-the-environment-pr-steward-runs-in) |
| Permission prompts | The session is started in [auto mode](https://code.claude.com/docs/en/permission-modes.md#eliminate-prompts-with-auto-mode), and a request for permission is denied |
| Comments | Anthropic's service sends a session the comments and reviews of the pull request's author, people with write access to the repository, and bots. When a session reads the pull request directly, it can also see what anyone else wrote there |
| Instruction files | PR Steward [reads them from the default branch](https://code.claude.com/docs/en/pr-steward-pull-requests.md#save-pr-steward-instructions-for-everyone-in-a-repository) |

## Limits on approvals and merges

Steward is designed not to approve or merge pull requests. Use branch protection to require the approvals you want before anything merges.

In an Anthropic-hosted environment, Anthropic's service refuses some requests that a PR Steward session makes as its GitHub App, and leaves others to GitHub's branch rules.

### Requests that Anthropic's service refuses

Anthropic's service refuses these requests from a PR Steward session that acts as its GitHub App:

* Approving a pull request
* Changing branch protection, rulesets, or statuses, or writing check runs
* Deleting a branch
* Pushing tags

### Requests left to GitHub's branch rules

Anthropic's service allows requests such as these. GitHub's branch rules control them, on the branches that have rules:

* **Merging, turning on auto-merge, and force-pushing**: before GitHub's branch rules apply, two checks run on the commands that Claude runs
* **Pushing to a branch other than the pull request's**: a session can push to any branch in that repository that GitHub lets the Claude GitHub App push to
* **Dismissing a review**: to limit who can do it, use GitHub's branch rules, for example **Restrict who can dismiss pull request reviews** in a classic branch protection rule

Two checks run on a command that merges, turns on auto-merge, or force-pushes. Permission rules deny the usual commands for these actions. [Auto mode's check](https://code.claude.com/docs/en/permission-modes.md#how-auto-mode-evaluates-actions) judges commands that no rule matches. The rules match a command's text and the check is a model's judgment, so a command that's written another way can pass both.

To have GitHub enforce reviews on what PR Steward pushes, [require reviews with branch rules](https://code.claude.com/docs/en/pr-steward-setup.md#require-reviews-with-branch-rules) and keep the Claude GitHub App off each ruleset's bypass list. In a classic branch protection rule, keep it off the **Allow specified actors to bypass required pull requests** list.

## Related resources

* [Set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md)
* [PR Steward](https://code.claude.com/docs/en/pr-steward.md)
* [Data usage](https://code.claude.com/docs/en/data-usage.md)
