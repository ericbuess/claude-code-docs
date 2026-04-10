> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# What's new

> A weekly digest of notable Claude Code features, with code snippets, demos, and context on why they matter.

The weekly dev digest highlights the features most likely to change how you work. Each entry includes runnable code, a short demo, and a link to the full docs. For every bug fix and minor improvement, see the [changelog](/en/changelog).

<Update label="Week 14" description="March 30 – April 3, 2026" tags={["v2.1.86–v2.1.91"]}>
  **Computer use** comes to the CLI in research preview: Claude can open native apps, click through UI, and verify changes from your terminal. Best for closing the loop on things only a GUI can verify.

  Also this week: `/powerup` interactive lessons, flicker-free alt-screen rendering, a per-tool MCP result-size override up to 500K, and plugin executables on the Bash tool's `PATH`.

  [Read the Week 14 digest →](/en/whats-new/2026-w14)
</Update>

<Update label="Week 13" description="March 23–27, 2026" tags={["v2.1.83–v2.1.85"]}>
  **Auto mode** lands in research preview: a classifier handles your permission prompts so safe actions run without interruption and risky ones get blocked. The middle ground between approving everything and `--dangerously-skip-permissions`.

  Also this week: computer use in the Desktop app, PR auto-fix on Web, transcript search with `/`, a native PowerShell tool for Windows, and conditional `if` hooks.

  [Read the Week 13 digest →](/en/whats-new/2026-w13)
</Update>
