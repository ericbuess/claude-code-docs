> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Review locally with /code-review

> Run `/code-review` in a Claude Code session to find bugs in your branch's changes, point the review at a pull request or path, and have Claude apply the fixes.

`/code-review` is a command you type at the Claude Code prompt, in the session where you're working. Claude reviews the changes on your branch, looks for correctness bugs, and reports what it found in your conversation. Depending on your model and effort level, the review also covers reuse, simplification, and efficiency cleanups.

The command works on any plan. The review runs in your own session, so it counts toward your plan's usage or API billing the same way the rest of the session does.

<Note>
  To have every pull request in a repository reviewed automatically on GitHub, see [Code Review](/docs/en/code-review), a managed service that an Owner turns on for your organization.
</Note>

`/review` is an alias of `/code-review`. Before v2.1.223, `/review` was a separate command that ran a single-pass, read-only review of a GitHub pull request.

<Steps>
  <Step title="Run /code-review">
    Run the command:

    ```text theme={null}
    /code-review
    ```

    With no target, the review covers the changes on your current branch. To point the review at a pull request, another branch, a path, or a range of commits instead, see [Choose what to review](#choose-what-to-review).

    You can also add flags:

    * `--fix`: also asks Claude to apply the findings to your working tree after the review. Its edits go through your [permission mode](/docs/en/permission-modes).
    * `--comment`: posts the findings on a GitHub pull request as inline comments, or on a [GitLab merge request](#post-findings-to-a-gitlab-merge-request) as a single note
  </Step>

  <Step title="Keep working">
    The review runs as a background [subagent](/docs/en/sub-agents) with its own context window, so it doesn't fill your conversation. The findings arrive in your conversation when the review completes.
  </Step>

  <Step title="Act on the findings">
    Ask Claude to fix what the review found. With `--fix` or `--comment`, Claude applies or posts the findings as part of the review, and you may be asked to approve its edits.
  </Step>
</Steps>

## Choose what to review

To review something other than your current branch, type a target after the effort level and any flags. Claude receives that text as the review target. A target can be a pull request number, a branch name, a file path, or a Git revision range. Find what you want reviewed in the first column and type what the second column shows:

| To point the review at | Type |
| :- | :- |
| Your current branch and uncommitted changes | `/code-review` |
| Your last 15 commits | `/code-review HEAD~15..HEAD` |
| One branch against another | `/code-review main...my-feature` |
| A single commit, where `abc1234` is the commit's hash | `/code-review abc1234^..abc1234` |
| A pull request by number | `/code-review 1234` |
| A file or directory path | `/code-review src/auth` |

With no target, `/code-review` reviews your branch's commits ahead of its upstream branch plus your uncommitted changes. If the branch has no upstream, Claude compares against `main`, or against the previous commit.

With `ultra`, Claude Code reads the target differently, as [Text after the effort level and flags](#text-after-the-effort-level-and-flags) describes.

## What the review reads and edits

Check these before you run a review, especially with `--fix`:

* **Edits**: without `--fix`, the review's instructions ask Claude for a report only. With `--fix`, they also ask it to apply the findings to your working tree. Either way, any edit goes through your permission mode.
* **Rewinding**: a background review applies its `--fix` edits outside your session's [checkpoints](/docs/en/checkpointing#subagent-edits-not-restored). After one, `/rewind` restores only the files Claude had already edited in your conversation. The review's edits to other files stay, so use git to revert them. When the review [runs in the foreground](#run-in-the-foreground), it edits your working tree during your own turn, so `/rewind` restores its edits as usual.
* **Instructions**: the review follows your `CLAUDE.md`, including in a non-interactive `-p` run. It doesn't read `REVIEW.md`. That file configures the managed [Code Review service](/docs/en/code-review-customize#use-review-md-for-review-only-rules) on GitHub pull requests.

## How findings are reported

Claude reports the findings as text in the reply in both of these runs:

* In a terminal session, where `/code-review` runs the review as a [forked subagent](/docs/en/skills#run-skills-in-a-subagent)
* In a `-p` run with text or JSON output

In a host application that requests the findings list, such as the [desktop app](/docs/en/desktop#review-your-code), Claude reports the review's findings through the [`ReportFindings` tool](/docs/en/tools-reference) instead. The report appears as a findings list, and each entry shows the file location, a one-sentence summary, and a category tag such as `correctness` when the finding carries one. A host request applies at every effort level and requires Claude Code v2.1.218 or later.

When Claude fixes reported findings later in the session, it reports them again. Claude Code then marks each finding in the updated findings list as fixed, skipped, or no change needed.

## Tune effort and arguments

Beyond `--fix` and `--comment`, the command takes these flags:

* `--post`: on an `ultra` cloud review of a `github.com` pull request, preselects posting the finished findings to the PR in the launch dialog. See [Post findings to the pull request](/docs/en/ultrareview#post-findings-to-the-pull-request). Requires Claude Code v2.1.227 or later.
* `--max-findings <n>`, `--max-findings all`, or `--max-findings default`: reports up to `n` findings, or every finding with `all`, in place of the review's usual limit. Where the review reports through the findings tool, the limit is 32. Later reviews reuse the value you typed until you pass `--max-findings default`, but a value passed in a non-interactive `-p` run isn't remembered. Requires Claude Code v2.1.288 or later.

Pass an [effort level](/docs/en/model-config#adjust-effort-level) to trade coverage for confidence. At `low`, the review reports the findings it's most confident in, so you see fewer false positives. From `medium` through `max`, the review broadens coverage.

When you don't type a level, the review reuses the last level from `low` through `max` you typed, even in an earlier session. Claude Code shows a notice such as `Reusing high effort, the level you typed last time`. These rules decide which level a run uses:

* **Typing a level**: a level you type, like `/code-review high`, changes what later runs reuse
* **Non-interactive runs**: a level you pass in a non-interactive `-p` run doesn't update the remembered level
* **`ultra`**: the review neither uses nor updates the remembered level
* **No level ever typed**: the review uses the session's current effort

Before v2.1.223, a `/code-review` without a level always used the session's current effort.

### Post findings to a GitLab merge request

When you pass `--comment` for a GitLab merge request, Claude Code posts the findings through GitLab's `glab` CLI. Requires Claude Code v2.1.257 or later. When `glab` isn't installed, Claude prints the findings in the terminal instead.

Pass the merge request as its URL or a `!123` reference. Claude Code treats a bare number or branch name as a merge request only when the checkout's origin is on `gitlab.com`. On a self-managed GitLab instance, pass the URL or `!123` form.

### Text after the effort level and flags

After the effort level and flags, Claude Code reads the rest of the line as the review target. The `ultra` argument changes that reading:

* **With `ultra`**: Claude Code reads a single word as a base branch or PR number. Longer text that doesn't name a branch or PR becomes [a note attached to the review](/docs/en/ultrareview#pass-a-request-in-plain-words). `/code-review ultra check my auth changes` reviews your current branch, and Claude relates the findings to your note.
* **Without `ultra`**: everything left is the review target, even when it starts with another command name. `/code-review /fix-issue 123` reviews with `/fix-issue 123` as target text instead of loading `/fix-issue` as a second [stacked skill](/docs/en/skills#pass-arguments-to-skills). Before v2.1.218, a command stacked after `/code-review` expanded as its own skill.

## Run in the foreground

To make the review run in the foreground, do one of these:

* Run it in non-interactive mode, with the `-p` flag or the Agent SDK. Claude Code waits for the review and includes the findings in the response, except for `ultra`, which [doesn't wait for the cloud review](/docs/en/ultrareview#run-ultrareview-non-interactively).
* Set [`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`](/docs/en/env-vars) to `1`, which also turns off every other background task feature
* Run `/code-review` again while an earlier review is still in progress

Before v2.1.218, the review ran inside your conversation.

## Let Claude start the review

Claude can start `/code-review` on its own, without you typing the command:

* **When you ask in plain language**: ask Claude to review your changes and it can run the skill
* **From a scheduled task**: a [scheduled task](/docs/en/scheduled-tasks) with `/code-review` as its prompt runs the review

A scheduled task never launches the [cloud review](#escalate-to-ultrareview), so schedule `/code-review` without the `ultra` argument.

To stop both Claude and scheduled tasks from starting the review while keeping `/code-review` available for you to type, add a [`skillOverrides`](/docs/en/skills#override-skill-visibility-from-settings) entry to a [settings file](/docs/en/settings#where-settings-live) such as `~/.claude/settings.json`:

```json theme={null}
{
  "skillOverrides": {
    "code-review": "user-invocable-only"
  }
}
```

Before v2.1.246, Claude started `/code-review` on its own only where a feature flag fetched from Anthropic turned it on. In [sessions that don't fetch feature flags](/docs/en/env-vars#features-that-need-feature-flag-fetching), `/code-review` ran only when you typed it, and a scheduled `/code-review` reached Claude as plain text.

## Escalate to ultrareview

`/code-review ultra --fix` runs the deeper [ultrareview](/docs/en/ultrareview) in the cloud, then asks Claude to apply its findings to your working tree when they arrive back in your session.

Ultrareview uses its own scope:

* **What it compares**: your current branch against the repository's default branch, plus uncommitted and staged changes in the working tree
* **Sensitive files**: for uncommitted changes to files named like credentials or keys, such as `.env` and `*.tfvars` files, Claude Code follows the rules for [uploading a local repository to a cloud session](/docs/en/claude-code-on-the-web#send-local-repositories-without-github)
* **A different base**: pass a branch name, such as `/code-review ultra develop`, to compare against a different base

When the target is a `github.com` pull request, you can have Claude [post the finished findings to the PR](/docs/en/ultrareview#post-findings-to-the-pull-request) as a comment from your GitHub account. Requires Claude Code v2.1.227 or later.

<Note>
  Ultrareview requires authentication with a claude.ai account. It isn't available on Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, or to organizations with Zero Data Retention enabled or with the [HIPAA configuration](/docs/en/hipaa-setup) applied. In these cases, `/code-review ultra` runs a local review in your session instead. Organizations that use [customer-managed encryption keys](https://platform.claude.com/docs/en/manage-claude/cmek) (CMEK) can't run ultrareview. To review your changes locally, run `/code-review`.
</Note>

To run a cloud review from a script or CI job, use the [`claude ultrareview` subcommand](/docs/en/ultrareview#run-ultrareview-non-interactively), which waits for the findings and prints them to stdout.

## Change or build on the review

`/code-review` is a [bundled skill](/docs/en/skills#bundled-skills): its instructions are built into Claude Code, so there is no `SKILL.md` file on disk to open or edit. To give every review project rules to follow, add them to your `CLAUDE.md`. To go further, start from one of these pages:

* **Replace the command**: a project or personal skill named `code-review` runs in place of the bundled one, and the `/review` alias keeps running the bundled review. See [Resolve skills that share a name](/docs/en/skills#resolve-skills-that-share-a-name).
* **Build your own reviewer**: write a reviewer [subagent](/docs/en/sub-agents) or a review [skill](/docs/en/skills)
* **Use a neighboring command**: [`/simplify`](/docs/en/commands) reviews for cleanup only and applies its fixes, and [`/verify`](/docs/en/commands) runs your app to confirm a change works

The command was named `/simplify` before v2.1.147, when it applied fixes by default. If you scripted `/simplify` for bug-finding, switch to `/code-review --fix`.

## Related resources

* [Code Review](/docs/en/code-review): the managed service that reviews every pull request on GitHub for your organization
* [Ultrareview](/docs/en/ultrareview): setup, limits, and cost of the deeper cloud review
* [Commands](/docs/en/commands): the one-line reference for `/code-review`, `/review`, `/simplify`, and `/verify`
* [Skills](/docs/en/skills): how bundled skills work and how to write your own
