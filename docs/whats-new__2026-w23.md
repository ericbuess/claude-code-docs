> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Week 23 · June 1–5, 2026

> Run auto mode on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, prompt before writing files that can run code in acceptEdits mode, list installed plugins with /plugin list, and require an approved version range for managed deployments.

Releases [v2.1.158 → v2.1.165](/docs/en/changelog.md#2-1-158)
4 features · June 1–5

Auto mode on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry
v2.1.158

Auto mode is now available on Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry for Opus 4.7 and Opus 4.8, replacing permission prompts with background safety checks on third-party providers. Opt in by setting `CLAUDE_CODE_ENABLE_AUTO_MODE=1`.

Opt in on a third-party provider, then cycle to auto mode with Shift+Tab:

```bash terminal theme={null}
export CLAUDE_CODE_ENABLE_AUTO_MODE=1
```

[Auto mode on third-party providers](/docs/en/permission-modes.md#enable-auto-mode-on-bedrock-agent-platform-or-foundry)

Safer automatic edits
v2.1.160

Claude Code now prompts before writing files that can run code, even in `acceptEdits` mode. The protected set covers shell startup files such as `.zshenv` and `.bash_login`, git config under `~/.config/git/`, and build-tool configs such as `.npmrc`, `.bazelrc`, and `.pre-commit-config.yaml`. These writes are never auto-approved in any mode except `bypassPermissions`.

Work in acceptEdits mode; Claude now pauses before writing these files:

```bash terminal theme={null}
claude --permission-mode acceptEdits
```

[Protected paths](/docs/en/permission-modes.md#protected-paths)

List installed plugins with /plugin list
v2.1.163

The new `/plugin list` command prints your installed plugins inline, without opening the `/plugin` menu, and is also available as `claude plugin list` from the shell. In the interactive form, add `--enabled` or `--disabled` to show only plugins in that state.

List the plugins that are currently turned on:

```text Claude Code theme={null}
> /plugin list --enabled
```

[Plugin commands](/docs/en/plugins/cli-reference.md#plugin-list)

Version requirements for managed deployments
v2.1.163

Two managed settings, `requiredMinimumVersion` and `requiredMaximumVersion`, let your organization require an approved Claude Code version range. A client outside the range exits at startup and tells the user to update through the organization's method. `claude update`, `claude install`, and `claude doctor` keep working so users can still recover.

Add a floor to your managed settings so older clients refuse to start:

```json managed-settings.json theme={null}
{
  "requiredMinimumVersion": "2.1.163"
}
```

[Decide what to enforce](/docs/en/admin-setup.md#decide-what-to-enforce)

Other wins

The trigger keyword for [dynamic workflows](/docs/en/workflows.md) changed from `workflow` to `ultracode`; asking for a workflow in your own words still works, and the keyword is highlighted in violet in the prompt[Stop and SubagentStop hooks](/docs/en/hooks.md) can return `hookSpecificOutput.additionalContext` to give Claude feedback and keep the turn going instead of being treated as an error`claude mcp` list, get, and add no longer print secrets: environment-variable references are not expanded, and credential headers and URL secrets are redactedA failed Bash command in a parallel tool batch no longer cancels the others; each tool returns its own result independentlyEditing a file no longer needs a separate Read first when you viewed it with a single-file `grep`, `egrep`, or `fgrep`Clicking a command in the autocomplete menu now fills it into your prompt instead of running it immediately; press Enter to runListing `Grep` or `Glob` in `--tools` now provides the dedicated search tools on native builds with embedded search, instead of silently ignoring those names`/effort` now confirms when your chosen level will persist as the default for new sessions`OTEL_RESOURCE_ATTRIBUTES` values are now attached as labels on metric datapoints, so you can slice usage metrics by custom dimensions like team or repoWindsurf is renamed to Devin Desktop in `/ide`, `/terminal-setup`, and `/scroll-speed`, following the editor's rebrand`/btw` gains a `c to copy` shortcut that copies the raw markdown answer to the clipboard

[Full changelog for v2.1.158–v2.1.165 →](/docs/en/changelog.md#2-1-158)
