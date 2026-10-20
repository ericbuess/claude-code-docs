> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Set up Code Review

> Turn on Code Review for your Claude organization: connect GitHub, install the Claude GitHub App, choose repositories, and set when reviews run

As an Owner of your Claude organization, you turn on Code Review in [**Admin settings > Claude Code**](https://claude.ai/admin-settings/claude-code#code-review) on claude.ai. Reviews run on Anthropic infrastructure, so you don't add workflow files to your repositories.

After setup, you choose how thorough reviews are and when they run in each repository. You spend more at a higher review level and when reviews run more often. See [Code Review costs](/docs/en/code-review-costs#pricing).

## What you need to turn on Code Review

First check that your organization [qualifies for Code Review](/docs/en/code-review#availability). Then make sure you have this access, or someone who does:

| Access | Needed for |
| :- | :- |
| [Owner role](/docs/en/server-managed-settings#access-control) in your Claude organization | Every step on the admin page |
| Owner of the GitHub organization | Installing the Claude GitHub App and [linking it to your Claude organization](/docs/en/admin-setup#connected-github-accounts). If you aren't an owner, have one install and link the app before you start |
| Write access to each repository you add, from the GitHub account you connect to Claude | Adding the repository |

## Turn on Code Review

**1. Click the Allow code review switch**

Go to the **Code review** section of [**Admin settings > Claude Code**](https://claude.ai/admin-settings/claude-code#code-review) and click the **Allow code review** switch.

If Code Review turns on right away with no dialog, your organization already has the Claude GitHub App linked or repositories added. Go to [Add more repositories](#add-more-repositories), then come back for the last step.

**2. Connect your GitHub account**

If a **Connect GitHub** dialog opens, click **Connect**. If your organization uses GitHub Enterprise Server, select your instance in the dialog first. GitHub asks you to authorize Claude, then returns you to the admin page with the **Add a repository** dialog open.

If **Add a repository** opened straight away, your account is already connected, so go on to the next step.

**3. Install the Claude GitHub App**

If the repositories you want are listed in the **Add a repository** dialog, or you find them by searching there, go on to the next step. The dialog lists a repository only if the Claude GitHub App can access it, so if they aren't there, install the app:

* Click **Install GitHub App**. When no repositories are listed, it's a button in the dialog. Otherwise, it's at the bottom of the dialog's GitHub organization filter menu. GitHub's install page opens in a new tab.
* Pick the GitHub organization that owns the repositories.
* Choose which repositories the app can access.
* Approve the requested permissions. The set is broader than a review uses and is shared by other Claude features, such as [GitHub Actions](/docs/en/github-actions). See [what a review can access](/docs/en/code-review#what-a-review-can-access) and the [full permission list](/docs/en/github-actions#github-app-permissions).
* When the install completes, the tab returns to Claude. If it shows a **Finish connecting GitHub** button, click it to link the installation to your Claude organization.
* Go back to the admin page's tab, where the list in the dialog refreshes.

**4. Choose repositories**

Select the repositories you want reviewed, then click **Continue**. Adding a repository needs write access to it from the GitHub account you connected. You can [add more repositories](#add-more-repositories) later.

**5. Click Finish**

A **Code review is set up** dialog follows. Click **Finish** to turn Code Review on. If you close the dialog any other way, your repositories stay added but **Allow code review** stays off, and you turn it on from the switch.

Each repository starts set to review after every push, which runs the most reviews. To run fewer, [set when reviews run](#set-when-reviews-run).

**6. Verify with a test pull request**

Open a test pull request in one of the repositories you added, and don't mark it as a draft. A check run named **Claude Code Review** appears within a few minutes. If you already set the repository to **Manual (@claude review)**, comment `@claude review` on the pull request to start the first review.

If no check run appears, see [No check run appears on the test pull request](/docs/en/code-review-troubleshooting#no-check-run-appears-on-the-test-pull-request).

Once the review arrives, send your developers [Read and request reviews on a pull request](/docs/en/code-review-pull-requests), which covers the severity levels, the comment commands, and how to respond to findings.

## Set defaults for your organization

As an Owner, you decide how thorough reviews are and how often they run. Both are in the **Code review** section of [**Admin settings > Claude Code**](https://claude.ai/admin-settings/claude-code#code-review).

### Set the default review level

The review level sets how thorough each review is, and a more thorough review costs more. You set one default for the organization and can override it for individual repositories.

| Level | What it trades |
| :- | :- |
| Quick | A lighter pass. The fastest level, at the lowest cost |
| Standard | Balanced depth, speed, and cost. The default level |
| Deep | The most thorough pass. Takes the longest and costs the most |

* **Organization default**: select a level under **Review level** and confirm with **Change level**. Every repository uses it unless you give that repository its own.
* **One repository**: click **Edit** on the repository's row, then select a **Review level** there. The first option, **Default**, follows the organization. The level saves as soon as you select it.

A new level applies to reviews that start after the change. For what else drives the cost of each review, see [Code Review costs and usage](/docs/en/code-review-costs).

### Set when reviews run

Each repository has its own **Review runs** setting, which decides when its pull requests get reviewed.

* **Once after PR creation**: a review runs when a pull request is opened, reopened, or marked ready for review
* **After every push**: a review runs on pushes to the pull request branch, catching new issues as the pull request evolves and auto-resolving threads when you fix flagged issues
* **Manual (@claude review)**: opening or pushing to a pull request doesn't start a review. Comment [`@claude review`](/docs/en/code-review-pull-requests#comment-commands) to request one, or `@claude review always` to also subscribe the pull request to reviews on subsequent pushes.

Manual is useful for high-traffic repositories where you want to opt specific pull requests into review, or to start reviewing pull requests only once they're ready. To compare what each option does to spend, see [How often reviews run](/docs/en/code-review-costs#how-often-reviews-run).

To change the setting, click **Edit** on the repository's row in the **Repositories** table and select a **Review runs** option. The choice saves as soon as you select it, and the table's **Review runs** column shows it shortened to Once per PR, Every push, or Manual.

* **Drafts and pull requests from forks**: whichever option you choose, [automatic reviews skip both](/docs/en/code-review-pull-requests#review-drafts-and-pull-requests-from-forks)
* **New repositories**: a repository you add from the **Add a repository** dialog starts at **After every push**. If its GitHub organization is [covered as a whole](#cover-a-whole-github-organization), it takes that organization row's setting instead.

### Turn tip comments on or off

A tip comment is a short comment Claude posts on a pull request when no review starts, saying why and what to do next. **Show tips on pull requests** is on by default. With it on, Claude posts a tip in each of these cases, explaining:

* **The repository is set to Manual**: how to request a review with a comment
* **The pull request comes from a fork**: that a maintainer can request the review
* **A bot, or someone without write access who isn't the pull request's author, comments `@claude review`**: that no review was started, and who can request one
* **The GitHub organization isn't linked to your Claude organization**: that reviews are paused, and how to link it

Turn the setting off to stop these comments.

### What developers can change

Developers come to you to change the review level, the **Review runs** setting, or which repositories get reviews. From GitHub, without the Owner role, they can do these:

* **Request a review**: comment [`@claude review`](/docs/en/code-review-pull-requests#comment-commands) on a pull request. This needs write access to the repository, and it works on [drafts and pull requests from forks](/docs/en/code-review-pull-requests#review-drafts-and-pull-requests-from-forks), which automatic reviews skip.
* **Subscribe one pull request to a review on each push**: comment `@claude review always` on a pull request that isn't [a draft or from a fork](/docs/en/code-review-pull-requests#review-drafts-and-pull-requests-from-forks), such as in a repository set to Manual
* **Change what reviews flag**: commit [`REVIEW.md` and `CLAUDE.md` files](/docs/en/code-review-customize) to the repository, for example to add a check

Reviews that developers request are [billed to your organization](/docs/en/code-review-costs#pricing). To limit what Code Review spends in a month, see [Limit your spend](/docs/en/code-review-costs#limit-your-spend).

## Manage repositories

You can add repositories one at a time or cover a whole GitHub organization at once, and stop reviews wherever you don't want them.

### Add more repositories

To add repositories after setup, click **Add** above the **Repositories** table in the **Code review** section. The **Add a repository** dialog opens. Select repositories and click **Continue**.

* **A repository isn't listed**: see [A repository isn't listed in Add a repository](/docs/en/code-review-troubleshooting#a-repository-isn’t-listed-in-add-a-repository).
* **You want every repository in a GitHub organization**: [cover the organization](#cover-a-whole-github-organization) instead of selecting repositories one at a time

### Cover a whole GitHub organization

To turn on Code Review for every repository in a GitHub organization, set **Review runs** on the organization's row in the **Repositories** table. That covers every repository there that the Claude GitHub App can access, including repositories added later. This can raise spend significantly. It requires all of these:

* The GitHub account you connected to Claude is an owner of that GitHub organization.
* The organization is on github.com. GitHub Enterprise Server instances and personal GitHub accounts aren't eligible.
* A [monthly spend limit](/docs/en/code-review-costs#limit-your-spend) is set, for your Claude organization or for Code Review.

To cover the organization, click **Edit** on its row, select a **Review runs** option, and confirm. The options are the three from [Set when reviews run](#set-when-reviews-run) plus **Off**.

After you confirm, these changes take effect:

* **Coverage**: each repository is covered from its next pull request. If the Claude GitHub App was installed on selected repositories rather than all of them, Claude reviews those repositories; change the app's repository access on GitHub to cover the rest.
* **Existing settings**: every repository in that GitHub organization takes the option you select, including repositories you had set individually. Setting the row again does the same. Repositories you turned off on their own rows stay off.
* **Individual changes afterward**: a repository you later set differently from its organization is marked **Custom** in the table.
* **Review level**: an organization row has no review level of its own.

### Turn off Code Review or remove a repository

In the **Code review** section of [**Admin settings > Claude Code**](https://claude.ai/admin-settings/claude-code#code-review), pick the control that matches what you want to stop:

* **One repository, keeping it in the list**: click **Edit** on its row and turn off **Code review**. The table shows the repository as Off.
* **One repository, removing it**: click **Edit** on its row, then **Remove repository** at the bottom of the dialog. Reviews stop there, and another Claude organization can then set that repository up. While the repository's GitHub organization is covered as a whole, you can't remove it; turn off its **Code review** switch instead.
* **A whole GitHub organization**: click **Edit** on the organization's row and select **Off**. This also turns off repositories in that organization that you added one at a time.
* **Everything**: turn off **Allow code review**. No new reviews start in any repository, and your repository list stays so you can turn it back on later.

## Related resources

* [Code Review costs and usage](/docs/en/code-review-costs): how the review level and when reviews run affect spend, how to set a spend limit, and where to see usage
* [Read and request reviews on a pull request](/docs/en/code-review-pull-requests): what developers see on a pull request and the comment commands
* [Customize Code Review](/docs/en/code-review-customize): tune what Claude flags with `REVIEW.md` and `CLAUDE.md`
* [GitHub Enterprise Server](/docs/en/github-enterprise-server): connect a self-hosted GitHub instance before setup
