> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 37 · September 7–11, 2026

> Test your plugins with claude plugin eval and pop Claude Code Desktop panes out into their own windows.

Releases [v2.1.263 → v2.1.269](/docs/en/changelog.md#2-1-263)
2 features · September 7–11

Test plugins with claude plugin eval
v2.1.269

`claude plugin eval` runs your plugin against a suite of test cases, scores the results, and by default runs each case again without the plugin so you can see what it contributes. `claude plugin eval init` asks you what a good result looks like, then proposes test cases and the checks that score them, tries the suite once, and writes the files. Every run, and every check that has a second model judge the reply, is a real model call on your account.

![Terminal output of claude plugin eval: a table of seven cases with each case's score with and without the plugin, the delta between them, the run count, and the cost, followed by a summary line with the mean delta, total duration, and total cost](https://mintcdn.com/claude-code/f9HTZGyMtxIFOUgt/images/whats-new/plugin-eval.jpg?fit=max\&auto=format\&n=f9HTZGyMtxIFOUgt\&q=85\&s=913066f6d4a2a15426e98a627802f47f)

From your plugin's root directory, have Claude draft the suite:

```bash terminal theme={null}
claude plugin eval init
```

When Claude tells you the suite is ready, exit the session that `claude plugin eval init` opened and run `claude plugin eval .` to score every case. The summary table prints in your terminal, and `report.html` under `evals/results/` has the per-run detail.

[Test plugins with evals](/docs/en/plugin-evals.md)

Pop Desktop panes out into their own windows
Desktop

In the Claude Code Desktop app, you can pop any pane out into its own window. Drag the diff or terminal to a second screen while Claude keeps working in the main window, then dock the pane back when you're done.

<video autoPlay muted loop playsInline src="https://mintcdn.com/claude-code/f9HTZGyMtxIFOUgt/images/whats-new/desktop-pop-out-panes.mp4?fit=max&auto=format&n=f9HTZGyMtxIFOUgt&q=85&s=ff3770dd09bb15ed9cf17a460f3d1e23" />

[Arrange your workspace](/docs/en/desktop.md#arrange-your-workspace)

Other wins

Set [`maxEffortLevel`](/docs/en/settings-reference#maxeffortlevel) at the top level or per model under `modelSettings` to cap the effort level on every provider, including Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry; any higher level runs at the capPoint `--plugin-dir` at a folder of plugins to [load each immediate subfolder that has a manifest](/docs/en/plugins/create.md#load-a-directory-or-archive-for-one-session)If WebFetch hasn't finished downloading a page within five minutes, [the fetch fails with a deadline error](/docs/en/tools-reference.md#webfetch-tool-behavior) instead of hanging; set `CLAUDE_CODE_WEBFETCH_DEADLINE_MS` to change the deadline, or to `0` to remove the limitPass `--json` to `claude plugin install`, `uninstall`, `update`, `enable`, or `disable` to print the result as [one JSON object on the last line of stdout](/docs/en/plugins/cli-reference.md#plugin-json-result)When the auto mode classifier blocks an action, the reason Claude receives [usually names the rule that matched](/docs/en/auto-mode-config.md#fix-a-denial-with-an-allow-rule-an-environment-entry-or-a-retry), such as `[Data Exfiltration]`When you type `/` partway through a prompt, you can now pick from [a list of matching commands](/docs/en/interactive-mode.md#complete-a-command-mid-prompt) instead of a single suggestion. The list opens as you type in fullscreen rendering. A plugin skill also matches on its name without the plugin prefixIn the VS Code extension, click the agent count at the bottom of the prompt box to open the [agent map](/docs/en/vs-code.md#use-the-prompt-box), where you can open a subagent's read-only transcript or stop itIn the VS Code extension, select **Hooks** or **Permissions** in the command menu's Customize section to [add or remove hooks and permission rules](/docs/en/vs-code.md#use-the-prompt-box) in your user, project, and local settingsClaude can pick a [browser-tab icon](/docs/en/artifacts.md#create-an-artifact) to match each artifact it publishesIn Claude Code on the web, take back a queued message in a cloud session before Claude reads it: remove it from the queue, or press `Esc` or `Up`, and the text returns to the message box

[Full changelog for v2.1.263–v2.1.269 →](/docs/en/changelog.md#2-1-263)
