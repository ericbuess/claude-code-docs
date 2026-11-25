> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshoot PR Steward

> Fix a PR Steward that didn't start, stopped, or paused on a GitHub pull request, and resolve the messages that an Owner sees while setting it up

When [PR Steward](https://code.claude.com/docs/en/pr-steward.md) doesn't do what you expect on a pull request, look for a comment from it first. If PR Steward posted one, [match the comment](#pr-steward-posted-a-comment-that-says-why). If it left nothing on the pull request, check [why it didn't start](#pr-steward-didn’t-start-on-a-pull-request).

## PR Steward didn't start on a pull request

Some causes leave nothing on the pull request, so check each of these sections.

### PR Steward didn't respond to your comment

If you commented `@claude steward` on github.com and PR Steward didn't start, look at your comment:

| What you see | What to check |
| :- | :- |
| No 👀 reaction | That it's a new comment and not an edit, and that you have write access |
| A 👀 reaction, and no `claude-pr-steward-watching` label after it | That the command is at the start of a top-level comment. Then check the other sections under [PR Steward didn't start on a pull request](#pr-steward-didn’t-start-on-a-pull-request) |

### Pull requests that PR Steward doesn't start on

Check whether your pull request is one that PR Steward skips:

| Cause | What to do |
| :- | :- |
| The pull request is a draft | Mark it ready for review. For work on drafts, see [**Include my draft PRs**](https://code.claude.com/docs/en/pr-steward-pull-requests.md#choose-what-pr-steward-works-on) |
| The pull request comes from a fork, a bot opened it, or its author lacks write access to the repository | PR Steward doesn't start on these |
| The description contains `<!-- claude-pr-steward-disable -->` | Remove the marker from the description, then comment `@claude steward` |
| Another Claude session is already watching the pull request, for example a cloud session with [auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests) on | Turn off auto-fix in that session, then comment `@claude steward` again |

### A setting keeps PR Steward off

A setting can keep PR Steward from starting:

| Cause | What to do |
| :- | :- |
| The repository is [set to **Manual**](https://code.claude.com/docs/en/pr-steward-setup.md#choose-when-pr-steward-starts-in-each-repository), or [your own option](https://code.claude.com/docs/en/pr-steward-pull-requests.md#turn-off-or-limit-pr-steward-on-all-your-pull-requests) is **Off** or **Only when tagged** | Comment `@claude steward` |
| The pull request is a teammate's, and their own option is **Off** | Ask them to comment `@claude steward` |
| PR Steward is off for the repository or for the author's GitHub account | Ask an [Owner](https://code.claude.com/docs/en/server-managed-settings.md#access-control) of your Claude organization to [add the repository](https://code.claude.com/docs/en/pr-steward-setup.md#turn-on-pr-steward-and-add-repositories) or to change [which authors PR Steward works for](https://code.claude.com/docs/en/pr-steward-setup.md#limit-which-authors-pr-steward-works-for) |

To confirm the last cause, have the author open their [PR Steward settings page](https://claude.ai/settings/claude-code#pr-steward). It shows a banner when your organization has turned off PR Steward. It also shows one when the GitHub account that they connected there is excluded.

### Many pull requests opened in a short time

If PR Steward started on many pull requests in your organization in a short time, comment `@claude steward`. If the `claude-pr-steward-watching` label still doesn't appear, comment again later.

## PR Steward posted a comment that says why

Find the words of PR Steward's comment in one of these tables.

### Comments when PR Steward can't start

If PR Steward commented and didn't start, find the comment's words here:

| Comment says | What to do |
| :- | :- |
| `PR Steward didn't start: only someone with write access` | Have a person with write access add the `claude-pr-steward-watching` label or comment `@claude steward` |
| `PR Steward hasn't started: your organization has no extra usage available` | Ask an Owner to add usage credits or raise the spend limit in [**Organization settings > Usage**](https://claude.ai/admin-settings/usage). If you asked PR Steward to start, it then starts when you ask again. Otherwise, it starts at the next push |
| `PR Steward hasn't started: billing for PR Steward isn't set up` | Ask an Owner to pick a repository where PR Steward is on and [change its **Steward** setting](https://code.claude.com/docs/en/pr-steward-setup.md#choose-when-pr-steward-starts-in-each-repository) to another option than **Off**. They can change it back straight away |
| `PR Steward hasn't started: your Claude organization hasn't picked where it runs yet` | Ask an Owner to [select an environment for PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md#choose-the-environment-pr-steward-runs-in), then comment `@claude steward` |
| `PR Steward hasn't started: it can't use the environment that your Claude organization picked for it` | Ask an Owner to [select another environment for PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md#choose-the-environment-pr-steward-runs-in), then comment `@claude steward` |
| `PR Steward hasn't started: the self-hosted runners it would run on need Claude Code 2.1.317 or newer` | Ask whoever runs your [self-hosted environment](https://code.claude.com/docs/en/pr-steward-setup.md#run-pr-steward-in-a-self-hosted-environment) to [update its runners](https://code.claude.com/docs/en/self-hosted-environments-deploy.md#pin-the-version), then comment `@claude steward` |
| `Claude PR Steward couldn't start, so it isn't watching this pull request` | Add the label or comment `@claude steward` to try again |
| `Claude PR Steward couldn't start on this pull request because the setup script` | Ask someone who can edit the [environment that PR Steward runs in](https://code.claude.com/docs/en/pr-steward-setup.md#choose-the-environment-pr-steward-runs-in) to fix its setup script, then start PR Steward again |
| `this repository has PR Steward enabled in more than one Claude workspace` | Ask the Owners to keep the repository in one Claude organization and remove it from the others |

### Comments when PR Steward stops or pauses

If PR Steward commented and then stopped or paused, find the comment's opening words here:

| Comment says | What it means | What to do |
| :- | :- | :- |
| `PR Steward is paused on this pull request` | Usage credits ran out while PR Steward was working, or billing setup is unfinished, as the comment says | Ask an Owner to add usage credits or raise the spend limit, or to finish billing setup as the comment describes. PR Steward picks up again at the next push or comment |
| `Claude PR Steward stopped watching this pull request: this session's spend reached the repository's PR Steward budget` | This session reached the [spend cap](https://code.claude.com/docs/en/pr-steward-setup.md#set-pr-steward’s-spend-limits) that's set for the repository | Finish the remaining work yourself, or add the `claude-pr-steward-watching` label again to start a new session |
| `Claude PR Steward stopped watching this pull request because your organization's PR Steward settings no longer cover it` | An Owner turned off PR Steward, or removed the repository or the author | After the settings cover the pull request again, add the label or comment `@claude steward` |
| `Claude PR Steward stopped watching this pull request because for <N> days no person has commented or reviewed here` | No person has commented or reviewed, and nobody but PR Steward has pushed, for the number of days that the comment gives | Add the label or comment `@claude steward` |

## Auto-fix is unavailable

In a repository where PR Steward works on your pull requests, the **Auto-fix** toggle on a cloud session is unavailable. If you ask to auto-fix a pull request that PR Steward is watching, the request fails. At claude.ai/code, the message is `PR Steward is already watching this PR.` To use [auto-fix](https://code.claude.com/docs/en/claude-code-on-the-web.md#auto-fix-pull-requests) in that repository, turn PR Steward off for yourself:

* **Later pull requests**: set [your own PR Steward option](https://code.claude.com/docs/en/pr-steward-pull-requests.md#turn-off-or-limit-pr-steward-on-all-your-pull-requests) to **Off**, which covers your pull requests in every repository
* **A pull request that PR Steward is already watching**: also [stop PR Steward there](https://code.claude.com/docs/en/pr-steward-pull-requests.md#start-or-stop-pr-steward-on-one-pull-request)

## Messages while you set up PR Steward

While you [set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md), you can see these messages on the [**Claude Ship**](https://claude.ai/admin-settings/claude-ship) page:

| What you see | What to do |
| :- | :- |
| **The GitHub connector is not enabled for your organization.** | Turn on the connector at [**Organization settings > Connectors**](https://claude.ai/admin-settings/connectors) |
| A repository is missing from the list of repositories when you click **Add** | Go to [**Organization settings > Git providers**](https://claude.ai/admin-settings/source-control), install the [Claude GitHub App](https://github.com/apps/claude) on your GitHub organization, and include the repository |
| A message that says your GitHub account "cannot push to that repository", or that adding it "needs write access" | Connect an account that can push, or ask an Owner who can push to do it |
| `PR Steward can't be enabled right now: billing setup is temporarily unavailable` | Try again in a few minutes |
| **PR Steward isn’t available for your organization.** | Check the [requirements](https://code.claude.com/docs/en/pr-steward.md#availability). If [**Runs for**](https://code.claude.com/docs/en/pr-steward-setup.md#turn-on-pr-steward-and-add-repositories) is **Listed users only**, add a username |
| **PR Steward is on but not watching any repositories yet.** | [Turn on PR Steward for a repository](https://code.claude.com/docs/en/pr-steward-setup.md#turn-on-pr-steward-and-add-repositories) |

## Related resources

* [Work with PR Steward on a pull request](https://code.claude.com/docs/en/pr-steward-pull-requests.md)
* [Set up PR Steward](https://code.claude.com/docs/en/pr-steward-setup.md)
* [PR Steward](https://code.claude.com/docs/en/pr-steward.md)
