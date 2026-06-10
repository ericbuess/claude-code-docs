> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Prompt library

> Copy-paste prompts for Claude Code, tagged by task and role.

This is a library of prompts to copy into Claude Code. Use it to explore ways of working you haven't tried, or when you're not sure where to start.

The prompts are collected from various Anthropic guides, including [Common workflows](/en/common-workflows), [Best practices](/en/best-practices), and [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code). They're starting points rather than scripts. Open **Why this works** under any prompt to see the pattern behind it so you can write your own.

## What makes these prompts work

The prompts above share a few patterns. Recognizing them helps you adapt any prompt here to your own task.

**Describe the outcome, not the steps.** Say what you want and let Claude find the files. The prompt below works without naming a single file path.

```text theme={null}
add rate limiting to the public API and make sure existing tests still pass
```

**Give it a way to check its own work.** Ask for run, test, compare, or verify in the same prompt so Claude iterates instead of stopping after one attempt.

```text theme={null}
write the migration, run it against the dev database, and confirm the schema matches
```

**Point at a reference.** Name an existing file, test, or pattern to match so the new code is consistent with what you already have.

```text theme={null}
add a settings page that follows the same layout as the profile page
```

**State the measurable target.** When the goal is performance or coverage, give the metric and threshold so completion is unambiguous.

```text theme={null}
get the bundle size under 200KB and show me what you removed
```

**Give it the artifact.** Paste errors, logs, screenshots, and plan output directly in the prompt, or type `@` to reference a file. Claude reads the source instead of your description of it.

```text theme={null}
why is the build failing? @build.log
```

**Say how you want the answer.** Name the format, length, or audience so the explanation fits how you'll use it. To make a format the default for every response, set an [output style](/en/output-styles).

```text theme={null}
explain how the payment retry logic works as an HTML page with a diagram, then open it in my browser
```

For more on each pattern, see [best practices](/en/best-practices).

## Where these come from

These prompts are based on patterns from published Anthropic resources. Each card links to its source:

* [Common workflows](/en/common-workflows): step-by-step guides for the core tasks
* [Best practices](/en/best-practices): prompting patterns and project setup
* [How Anthropic teams use Claude Code](https://claude.com/blog/how-anthropic-teams-use-claude-code): real workflows from engineering, product, design, and data teams, with deep dives on [legal](https://claude.com/blog/how-anthropic-uses-claude-legal), [marketing](https://claude.com/blog/how-anthropic-uses-claude-marketing), and [cybersecurity](https://claude.com/blog/how-anthropic-uses-claude-cybersecurity)
* [Scaling agentic coding guide](https://resources.anthropic.com/hubfs/Scaling%20agentic%20coding%20across%20your%20organization.pdf): the enterprise adoption guide

For video walkthroughs of these patterns, see the free [Claude Code in Action](https://anthropic.skilljar.com/claude-code-in-action) course on Anthropic Academy.

## Related resources

The prompts on this page are starting points. Once one works for your project, the next step is making it repeatable: save it as a [skill](/en/skills) so anyone on your team can run it as a `/command`, and record the conventions Claude learned in [CLAUDE.md](/en/memory) so every session starts with that context instead of Claude relearning it. For larger or riskier changes, [plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) shows you the file list before any edits happen.

If you're introducing Claude Code across a team, see [administration](/en/admin-setup) for managed settings and policy, and [costs and usage](/en/costs) for how this work is billed on your plan.
