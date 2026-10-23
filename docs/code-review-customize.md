> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Customize Code Review

> Tune what Code Review flags on your pull requests with REVIEW.md and CLAUDE.md: recalibrate severity, skip paths, add checks, and see which copy applies.

You can change what [Code Review](https://code.claude.com/docs/en/code-review.md) flags on your repository by committing instructions to it. This is how you cut nit volume, stop comments on generated files, or add a rule your team cares about. Put them in one of two files:

* **`CLAUDE.md`**: [project instructions](https://code.claude.com/docs/en/memory.md) that Claude Code reads for every task, reviews included. Code Review reads them as project context and flags changes that violate them.
* **`REVIEW.md`**: instructions for reviews alone. Use it to say what your team wants flagged, at what severity, and what to skip.

Add `REVIEW.md` at your repository root and merge it. Then [protect your default branch](#which-branch-review-md-is-read-from).

> [!NOTE]
>
> To change how thorough reviews are or when they run, ask an Owner to change the [review level](https://code.claude.com/docs/en/code-review-setup.md#set-the-default-review-level) or the [**Review runs** setting](https://code.claude.com/docs/en/code-review-setup.md#set-when-reviews-run).

## Use CLAUDE.md for project-wide rules

Code Review reads your repository's `CLAUDE.md` files as project context. A change that violates one of their rules becomes a finding at whichever [severity level](https://code.claude.com/docs/en/code-review-pull-requests.md#severity-levels) fits the issue.

A review reads the `CLAUDE.md` at your repository root and the `CLAUDE.md` files in the parent directories of each changed file. A subdirectory's `CLAUDE.md` is read when the pull request changes a file under that path.

## Use REVIEW\.md for review-only rules

`REVIEW.md` is a file at your repository root that tailors Code Review to your repository. You can also add a `REVIEW.md` in a subdirectory to add checks for changes under that path, on top of the root file.

The agents that find issues and the agents that verify them receive its contents as your repository's review instructions, alongside Code Review's default review guidance. The step that writes the final review consults it before settling severity and writing the summary.

This example layout has a root file and one subdirectory file:

```text theme={null}
your-repo/
├── REVIEW.md            # Root file
├── services/
│   └── billing/
│       └── REVIEW.md    # Adds checks for changes under services/billing/
└── src/
```

Before you rely on a subdirectory file, protect your default branch and check [what a review reads for your branch setup](#what-a-review-reads-for-each-branch-setup).

> [!NOTE]
>
> The Code Review service and the local [`/code-review` command](https://code.claude.com/docs/en/code-review-local) are two separate tools, and they read different files. The service reads both `CLAUDE.md` and `REVIEW.md`. The `/code-review` command, which you run inside a Claude Code session on your own machine, reads your `CLAUDE.md` files and not `REVIEW.md`. Put guidance you want applied in both places in `CLAUDE.md`, and keep `REVIEW.md` for rules specific to pull request review.

### Example REVIEW\.md

This `REVIEW.md` recalibrates severity for a backend service, caps nits, skips generated files, and adds repo-specific checks.

```markdown theme={null}
# Review instructions

## What Important means here

Reserve Important for findings that would break behavior, leak data,
or block a rollback: incorrect logic, unscoped database queries, PII
in logs or error messages, and migrations that aren't backward
compatible. Style, naming, and refactoring suggestions are Nit at
most.

## Cap the nits

Report at most five Nits per review.

## Do not report

- Anything CI already enforces: lint, formatting, type errors
- Generated files under `src/gen/` and any `*.lock` file
- Test-only code that intentionally violates production rules

## Always check

- New API routes have an integration test
- Log lines don't include email addresses, user IDs, or request bodies
- Database queries are scoped to the caller's tenant
```

### Choose what to write in REVIEW\.md

`REVIEW.md` is freeform Markdown that changes what a review finds and reports. It doesn't change the format of the review. Find the problem you're seeing, then add an instruction like the one shown. The [example](#example-review-md) uses the first four.

* **The wrong things are marked Important**: redefine what 🔴 Important means for your repository. The default calibration targets production code, and a docs repository, a config repository, or a prototype might want a much narrower definition. State which classes of finding are Important and which are Nit at most. You can also escalate, for example treating any `CLAUDE.md` violation as Important.
* **Too many nits**: cap how many 🟡 Nit comments a single review posts. A cap like "report at most five nits" keeps reviews actionable.
* **Comments on generated files or on what CI already checks**: list paths and finding categories where Claude should skip findings. Common candidates are generated code, lockfiles, and vendored dependencies, along with anything your CI already enforces like linting or spellcheck. For paths that warrant some review but not full scrutiny, set a higher bar instead: "in `scripts/`, only report if near-certain and severe."
* **A team rule isn't being checked**: add rules you want flagged on every pull request, like "new API routes must have an integration test."
* **Findings that turn out to be wrong**: require evidence before a class of finding is posted. For example, "behavior claims need a `file:line` citation in the source, not an inference from naming" cuts false positives that would otherwise cost the author a round trip.

Some of these instructions [need the root file on a protected default branch](#which-branch-review-md-is-read-from).

Keep `REVIEW.md` to instructions that change review behavior, and leave general project context in `CLAUDE.md`.

### Include other files in REVIEW\.md

You can split review instructions across several files and pull them into your root `REVIEW.md`. Use this when `REVIEW.md` grows long or when you already keep review rules in another file.

To include a file, add a line to the root `REVIEW.md` with only `@` and the file name on it. Code Review puts the file's contents in place of that line, so they apply as part of `REVIEW.md`. In this example, the root file gives one instruction of its own and then includes two rule files:

```markdown theme={null}
# Review instructions

Report at most five Nits per review.

@review-security.md
@review-api.md
```

Save the included files at the repository root, beside `REVIEW.md`:

```text theme={null}
your-repo/
├── REVIEW.md
├── review-security.md
└── review-api.md
```

Code Review includes the files when it reads `REVIEW.md` from a protected branch, so check [which branch a review reads for your repository](#what-a-review-reads-for-each-branch-setup):

* **Protected branch**: Code Review puts the included file in place of its `@` line
* **Unprotected default branch**: the `@` line stays in `REVIEW.md` as plain text. If the pull request changes the file the line names, the line is left out.

When a review doesn't apply an included file, check each of these:

* **Location**: move the file to the repository root. A path into a subdirectory such as `@docs/review-rules.md` isn't included.
* **Name**: match the file name exactly, including case, and use a name without spaces. A line whose name matches no file beside `REVIEW.md` stays in `REVIEW.md` as plain text, and the check run doesn't report it as a skipped include.
* **One level**: list every file in the root `REVIEW.md`. An `@` line in an included file or in a subdirectory `REVIEW.md` stays as plain text, and a Markdown link to another file isn't an include.
* **Limits**: include at most eight different files, and keep `REVIEW.md` and the files it includes under 150,000 bytes combined. A file that would reach the byte limit is skipped whole, not cut short. The check run reports how many include lines it skipped for either limit.
* **Links**: keep Markdown links at 64 or fewer across `REVIEW.md` and the files it includes. Links to `http`, `https`, or `mailto` addresses and to `#` anchors don't count. Past that limit, the review skips your whole root `REVIEW.md`, not only the included files. The check run then [says the instructions weren't applied](https://code.claude.com/docs/en/code-review-troubleshooting.md#the-check-run-mentions-review-md).
* **Merged copy**: merge the included file into the [branch `REVIEW.md` is read from](#which-branch-review-md-is-read-from). The review reads both from the same commit, never from the pull request's own changes.

### Which branch REVIEW\.md is read from

Code Review reads `REVIEW.md` from the pull request's base branch or from the default branch, never from the pull request's own changes. To change review behavior, merge the `REVIEW.md` change first.

Keep `REVIEW.md` on your default branch and protect that branch. When a review reads the copy on a protected default branch, the first row of the table below, it honors these instructions from the root file:

* Lowering a finding's severity
* Excluding paths, files, or classes of issue
* Capping nit comments

#### What counts as branch protection

Code Review counts these settings as protection:

* **Default branch**: a classic branch protection rule or a ruleset
* **Any other branch**: a ruleset only

A ruleset counts when it restricts updates or requires pull requests with at least one approval. If it requires pull requests, it must also dismiss that approval on a new push or require the approval to come after the last push.

#### What a review reads for each branch setup

Find your repository's situation in the first column of the table below.

| Branch protection | Copy read | Files read |
| :- | :- | :- |
| The default branch is protected, and the pull request targets it or targets a branch no ruleset protects | Default branch | Root file, the files it includes, and subdirectory files |
| The pull request targets another branch that a ruleset protects | That base branch | Root file, the files it includes, and subdirectory files |
| The default branch isn't protected, and the base branch has no protection rule of either kind | Default branch | Root file |
| Code Review can't confirm the protection settings. This includes an unprotected default branch with a base branch that has only a classic rule | None | None |

If the check run mentions `REVIEW.md`, see [The check run mentions REVIEW.md](https://code.claude.com/docs/en/code-review-troubleshooting.md#the-check-run-mentions-review-md).

## Related resources

* [Code Review](https://code.claude.com/docs/en/code-review.md): what the service is and how a review runs
* [Read and request reviews on a pull request](https://code.claude.com/docs/en/code-review-pull-requests.md#severity-levels): what each severity level means and how findings appear
* [Set up Code Review](https://code.claude.com/docs/en/code-review-setup.md): the review level and when reviews run, which an Owner sets
* [Review locally with `/code-review`](https://code.claude.com/docs/en/code-review-local): the `/code-review` command, its arguments, and effort levels
* [Memory](https://code.claude.com/docs/en/memory.md): how `CLAUDE.md` files work across Claude Code
