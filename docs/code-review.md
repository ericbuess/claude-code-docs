> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Catch bugs in GitHub pull requests with Code Review: Claude reviews each change, verifies its findings, and comments inline. For Team and Enterprise plans

With Code Review, Claude reviews the pull requests in your GitHub repositories. Several agents read each change alongside the surrounding code, looking for issues such as logic errors, security vulnerabilities, or broken edge cases. A verification step checks findings against the code before they're reported.

Findings arrive as inline comments on the lines concerned, ranked by [severity](/docs/en/code-review-pull-requests.md#severity-levels), with a summary and a check run on the pull request. A review never approves or blocks the pull request, so the decision to merge stays with your team.

![Diagram of a review in four stages. A pull request on GitHub goes to several agents that search in parallel on Anthropic infrastructure. A verification step drops false positives, the remaining findings are deduplicated and ranked by severity, and the review posts inline comments, a summary, and a check run back on GitHub.](https://mintcdn.com/claude-code/gLJVaPQEgKC8ZyUD/images/code-review-pipeline.svg?fit=max\&auto=format\&n=gLJVaPQEgKC8ZyUD\&q=85\&s=0351c96df9efa3105172eb00a672f130)

> [!NOTE]
>
> Code Review uses AI to review code and may miss bugs, security vulnerabilities, or other issues. A review with no findings doesn't mean your code is error-free or secure.

To turn on Code Review, an Owner of your Claude organization follows [Set up Code Review](/docs/en/code-review-setup.md). Claude can also review code without this service. Run [`/code-review`](/docs/en/code-review-local) in your Claude Code session on any plan, or [compare all the options](#compare-ways-to-get-a-review).

## Availability

Check that your organization qualifies before you set up Code Review:

* **Plans**: [Team and Enterprise](/docs/en/feature-availability.md)
* **Code hosts**: repositories hosted on GitHub, including [GitHub Enterprise Server](/docs/en/github-enterprise-server.md) and GitHub Enterprise Cloud with data residency. For data residency, have an Owner follow the [GitHub Enterprise Server admin setup](/docs/en/github-enterprise-server.md#admin-setup) and enter your enterprise's `ghe.com` hostname.
* **Data retention**: Code Review isn't available to organizations with [Zero Data Retention](/docs/en/zero-data-retention.md) enabled or with the [HIPAA configuration](/docs/en/hipaa-setup.md) applied, and isn't covered under Anthropic's Business Associate Agreement (BAA).
* **Encryption keys**: Code Review isn't yet available for organizations that use customer-managed encryption keys (CMEK).
* **Cloud providers**: you need a Claude organization on one of these plans even if your developers use Claude Code through Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry

## Set up and use Code Review

Pick the page for what you need to do:

> **[Set up Code Review](/docs/en/code-review-setup.md)**
>
> Check the requirements, install the Claude GitHub App, and choose repositories, a review level, and when reviews run

> **[Customize Code Review](/docs/en/code-review-customize.md)**
>
> Tune what gets flagged with `REVIEW.md` and `CLAUDE.md` files in your repository

> **[Read and request reviews on a pull request](/docs/en/code-review-pull-requests.md)**
>
> Read the findings and their severities, and request another review with a comment

> **[Troubleshoot Code Review](/docs/en/code-review-troubleshooting.md)**
>
> Fix a review that didn't start, failed, or was skipped for budget

> **[Code Review costs and usage](/docs/en/code-review-costs.md)**
>
> See how reviews are billed, estimate spend, set the monthly spend limit, and track review activity

## How reviews work

By default, Code Review focuses on correctness: bugs that would break production, not formatting preferences or missing test coverage. To change what it flags, [add guidance files](/docs/en/code-review-customize.md) to your repository.

A review runs on Anthropic infrastructure in four stages:

1. **Find**: several agents examine the diff and the surrounding code in parallel.
2. **Verify**: a verification step checks the candidate findings against the code and filters out false positives.
3. **Rank**: the findings that remain are deduplicated and ranked by severity.
4. **Post**: the review posts its results on the pull request.

Each review leaves these on the pull request:

* **Findings**: inline comments on the lines concerned, with a summary in the review body
* **A check run**: named **Claude Code Review**, with the findings listed in its [details](/docs/en/code-review-pull-requests.md#check-run-output). The check run doesn't conclude as a failure.
* **When it finds nothing**: the check run's title reads **Code review found no issues**, and Claude posts the same short note on the pull request

Code Review chooses the Claude models that reviews run on, and its admin settings don't offer a model choice. To make reviews more or less thorough, change the [review level](#review-levels).

After an Owner turns on Code Review, each repository has a setting for [when reviews run](/docs/en/code-review-setup.md#set-when-reviews-run): once when a pull request opens, after every push, or only on request. Whichever it is, someone with write access to the repository can comment `@claude review` on a pull request to [start a review](/docs/en/code-review-pull-requests.md#comment-commands).

### Review levels

The review level sets how thorough each review is, and a more thorough review costs more:

* **Quick**: a lighter pass. The fastest level, at the lowest cost.
* **Standard**: balanced depth, speed, and cost. The default level.
* **Deep**: the most thorough pass. Takes the longest and costs the most.

An Owner [chooses one level for the organization](/docs/en/code-review-setup.md#set-the-default-review-level) and can give an individual repository its own, such as Quick for a routine codebase and Deep for a critical one. For what else drives the cost of each review, see [Code Review costs and usage](/docs/en/code-review-costs.md).

### What a review can access

A review reaches your repository through the Claude GitHub App that an Owner [installs during setup](/docs/en/code-review-setup.md#turn-on-code-review):

* **Where it runs**: on Anthropic infrastructure, in a managed environment. Reviews don't run in [self-hosted environments](/docs/en/self-hosted-environments).
* **What it reads and writes**: inside a review, access to your repository is read-only, and a review doesn't push commits. On the pull request, it posts comments and the [check run](/docs/en/code-review-pull-requests.md#check-run-output), resolves its own earlier comment threads, and can react to a comment command with 👀. The app itself holds a [broader permission set](/docs/en/github-actions.md#github-app-permissions) that other Claude features share.
* **How it examines your code**: a review works from reading the diff and the surrounding code, without building or running your code.

### Who controls a review

* **Who can start one**: where reviews run automatically, opening or pushing to a pull request starts a review, [except on drafts and forks](/docs/en/code-review-pull-requests.md#review-drafts-and-pull-requests-from-forks). After some pushes, Code Review [keeps the earlier result](/docs/en/code-review-pull-requests.md#when-a-push-keeps-the-earlier-result) instead. A [comment command](/docs/en/code-review-pull-requests.md#comment-commands) starts one only when it comes from a person with write access to the repository.
* **Which instructions it follows**: `REVIEW.md` from the base or default branch and [never from the pull request's own changes](/docs/en/code-review-customize.md#which-branch-review-md-is-read-from).

## Compare ways to get a review

To find the options open to you, check the **Who can use it** column against your plan and code host:

| Option | What starts a review | Where it runs | Who can use it |
| :- | :- | :- | :- |
| [Code Review](#how-reviews-work) | Pull request activity, as each repository is set, or an `@claude review` comment | Anthropic infrastructure | Organizations on a Team or Enterprise plan with GitHub repositories, once an Owner turns it on |
| [`/code-review`](/docs/en/code-review-local) | You run the command on your branch | Your Claude Code session | Anyone, on any plan |
| [Ultrareview](/docs/en/ultrareview.md) | You start it from Claude Code | A cloud sandbox | Requires signing in with a claude.ai account. See [Ultrareview](/docs/en/ultrareview.md) for where it isn't available |
| Claude in your own CI, with [GitHub Actions](/docs/en/github-actions.md) or [GitLab CI/CD](/docs/en/gitlab-ci-cd.md) | Your pipeline's events, such as every pull request or merge request | Your own CI runners | Anyone with a Claude API key or cloud provider credentials, on GitHub or GitLab |
| Your own reviewer, as a [subagent](/docs/en/sub-agents.md) or [skill](/docs/en/skills.md) | You or Claude invoke it during a session | Wherever you run Claude Code | Anyone who writes one |

## Related resources

* [GitHub Enterprise Server](/docs/en/github-enterprise-server.md): use Code Review with a self-hosted GitHub instance
* [GitHub App permissions](/docs/en/github-actions.md#github-app-permissions): the full permission set the Claude GitHub App requests
* [How Anthropic secures its AI-native software development lifecycle](https://claude.com/blog/how-anthropic-secures-its-ai-native-software-development-lifecycle): how automated review fits as one layer of Anthropic's secure development process
