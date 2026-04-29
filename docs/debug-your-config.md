> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Debug your configuration

> Diagnose why CLAUDE.md, settings, hooks, MCP servers, or skills aren't taking effect. Use /context, /doctor, /hooks, and /mcp to see what actually loaded.

When Claude ignores an instruction or a feature you configured doesn't appear, the cause is usually that the file didn't load, it loaded from a different location than you expected, or another file overrode it. This guide shows how to inspect what Claude Code actually loaded so you can narrow down which applies.

For installation, authentication, and connectivity problems, see [Troubleshoot installation and login](/en/troubleshoot-install) instead.

## See what loaded into context

The `/context` command shows everything occupying the context window for the current session, broken down by category: system prompt, memory files, skills, MCP tools, and conversation messages. Run it first to confirm whether your `CLAUDE.md`, rules, or skill descriptions are present at all.

For detail on a specific category, follow up with the dedicated command:

| Command        | Shows                                                                       |
| :------------- | :-------------------------------------------------------------------------- |
| `/memory`      | Which `CLAUDE.md` and rules files loaded, plus auto-memory entries          |
| `/skills`      | Available skills from project, user, and plugin sources                     |
| `/agents`      | Configured subagents and their settings                                     |
| `/hooks`       | Active hook configurations                                                  |
| `/mcp`         | Connected MCP servers and their status                                      |
| `/permissions` | Resolved allow and deny rules currently in effect                           |
| `/doctor`      | Configuration diagnostics: invalid keys, schema errors, installation health |
| `/status`      | Active settings sources, including whether managed settings are in effect   |

If a memory file is missing from `/memory`, check its location against [how CLAUDE.md files load](/en/memory#how-claude-md-files-load). Subdirectory `CLAUDE.md` files load on demand when Claude reads a file in that directory with the Read tool, not at session start.

If `/memory` confirms the file loaded but Claude still isn't following a particular instruction, the issue is likely how the instruction is written rather than whether it loaded. CLAUDE.md works well for the kinds of guidance you'd give a new teammate, such as project conventions, build commands, and where files belong.

Adherence drops when an instruction is vague enough to interpret multiple ways, when two files give conflicting direction, or when the file has grown long enough that individual rules get less attention. [Write effective instructions](/en/memory#write-effective-instructions) covers the specificity, size, and structure patterns that keep adherence high.

<Note>
  CLAUDE.md and permissions solve different problems. CLAUDE.md tells Claude how your project works so it makes good decisions. [Permissions](/en/permissions) and [hooks](/en/hooks) enforce limits regardless of what Claude decides. Use CLAUDE.md for "we do it this way here." Use permissions or hooks for security boundaries and anything that must never happen, where you need a guarantee instead of guidance.
</Note>

## Check resolved settings

Settings merge across managed, user, project, and local scopes. Managed settings always win when present. Among the rest, the closer scope overrides the broader one in the order local, then project, then user. Some settings can also be set by command-line flags or [environment variables](/en/env-vars), which act as another override layer. When a setting doesn't seem to apply, the value you set is usually being overridden by another scope or an environment variable.

Run `/doctor` to validate your configuration files and surface invalid keys or schema errors. Run `/status` to see which settings sources are active, including whether managed settings are in effect. To understand which scope wins for a given key, see [How scopes interact](/en/settings#how-scopes-interact).

## Check MCP servers

Run `/mcp` to see every configured server, its connection status, and whether you have approved it for the current project. A server can be defined correctly but still not provide tools for a few common reasons:

* Project-scoped servers in `.mcp.json` require a one-time approval. If the prompt was dismissed, the server stays disabled until you approve it from `/mcp`.
* A server that fails to start shows as failed in `/mcp`. Relative file paths in `command` or `args` are a frequent cause, since they resolve against the directory you launched Claude Code from rather than the location of `.mcp.json`.
* A server that shows as connected but lists zero tools has started successfully but isn't returning a tool list. Select **Reconnect** from `/mcp`. If the count stays at zero, run `claude --debug mcp` to see the server's stderr output.

For configuration locations and scope rules, see [MCP](/en/mcp).

## Check hooks

Run `/hooks` to list every hook registered for the current session, grouped by event. If a hook you defined doesn't appear, it isn't being read: hooks go under the `"hooks"` key in a settings file, not in a standalone file.

If the hook appears but doesn't fire, the matcher is the usual cause. The `matcher` field is a single string that uses `|` to match multiple tool names, for example `"Edit|Write"`. A misspelled tool name fails silently because the matcher never matches. An array value is a schema error: Claude Code shows a settings error notice, `/doctor` reports the validation failure, and the hook entry is dropped so it won't appear in `/hooks`.

Edits to `settings.json` take effect in the running session after a brief file-stability delay. You don't need to restart. If `/hooks` still shows the old definition a few seconds after saving, run `/hooks` again to refresh the view.

If `/hooks` shows the hook but it still does not fire, the next step is to watch hook evaluation live. Start a session with `claude --debug hooks` and trigger the tool call. The debug log records each event, which matchers were checked, and the hook's exit code and output. See [Debug hooks](/en/hooks#debug-hooks) for the log format and [hooks troubleshooting](/en/hooks-guide#limitations-and-troubleshooting) for common failure patterns.

## Common causes

Most configuration surprises trace back to a small set of location and syntax rules. Check these before assuming a bug:

| Symptom                                                          | Cause                                                                                                                      | Fix                                                                                                                                                                                                       |
| :--------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hook never fires                                                 | `matcher` is a JSON array instead of a string                                                                              | Use a single string with `\|` to match multiple tools, for example `"Edit\|Write"`. See [matcher patterns](/en/hooks#matcher-patterns).                                                                   |
| Hook never fires                                                 | `matcher` value is lowercase, for example `"bash"`                                                                         | Matching is case-sensitive. Tool names are capitalized: `Bash`, `Edit`, `Write`, `Read`.                                                                                                                  |
| Hook never fires                                                 | Hooks are in a standalone `.claude/hooks.json` file                                                                        | There is no standalone hooks file. Define hooks under the `"hooks"` key in `settings.json`. See [hook configuration](/en/hooks).                                                                          |
| Permissions, hooks, or env set globally are ignored              | Configuration was added to `~/.claude.json`                                                                                | `~/.claude.json` holds app state and UI toggles. `permissions`, `hooks`, and `env` belong in `~/.claude/settings.json`. These are two different files.                                                    |
| A `settings.json` value seems ignored                            | The same key is set in `settings.local.json`                                                                               | `settings.local.json` overrides `settings.json`, and both override `~/.claude/settings.json`. See [settings precedence](/en/settings#how-scopes-interact).                                                |
| Skill doesn't appear in `/skills`                                | Skill file is at `.claude/skills/name.md` instead of in a folder                                                           | Use a folder with `SKILL.md` inside: `.claude/skills/name/SKILL.md`.                                                                                                                                      |
| Skill appears in `/skills` but Claude never invokes it           | Skill has `disable-model-invocation: true` in its frontmatter, or its description doesn't match how you phrase the request | Check the badge in `/skills`: a "user-only" label means Claude won't trigger it on its own. See [skill invocation](/en/skills).                                                                           |
| Subdirectory `CLAUDE.md` instructions seem ignored               | Subdirectory files load on demand, not at session start                                                                    | They load when Claude reads a file in that directory with the Read tool, not at launch and not when writing or creating files there. See [how CLAUDE.md files load](/en/memory#how-claude-md-files-load). |
| Subagent ignores `CLAUDE.md` instructions                        | Subagents don't always inherit project memory                                                                              | Put critical rules in the agent file body, which becomes the subagent's system prompt. See [subagent configuration](/en/sub-agents).                                                                      |
| Cleanup logic never runs at session end                          | No `SessionEnd` hook configured                                                                                            | Add a `SessionEnd` hook in `settings.json`. See the [hook events list](/en/hooks#hook-events).                                                                                                            |
| MCP servers in `.mcp.json` never load                            | File is under `.claude/` or uses Claude Desktop's config format                                                            | Project MCP config goes at the repository root as `.mcp.json`, not inside `.claude/`. See [MCP configuration](/en/mcp).                                                                                   |
| Project MCP server added but doesn't appear                      | The one-time approval prompt was dismissed                                                                                 | Project-scoped servers require approval. Run `/mcp` to see status and approve.                                                                                                                            |
| MCP server fails to start from some directories                  | `command` or `args` uses a relative file path                                                                              | Use absolute paths for local scripts. Executables on your `PATH` like `npx` or `uvx` work as-is.                                                                                                          |
| MCP server starts without expected environment variables         | Variables are in `settings.json` `env`, which doesn't propagate to MCP child processes                                     | Set per-server `env` inside `.mcp.json` instead.                                                                                                                                                          |
| `Bash(rm *)` deny rule doesn't block `/bin/rm` or `find -delete` | Prefix rules match the literal command string, not the underlying executable                                               | Add explicit patterns for each variant, or use a [PreToolUse hook](/en/hooks-guide) or the [sandbox](/en/sandboxing) for a hard guarantee.                                                                |

## Related resources

For full reference on each configuration surface, see the dedicated page:

* **[`.claude` directory reference](/en/claude-directory)**: every config file location and what reads it
* **[Settings](/en/settings)**: precedence order and the full key list
* **[Hooks reference](/en/hooks)**: event names, payloads, and `--debug hooks` output format
* **[MCP](/en/mcp)**: server configuration, approval, and `/mcp` output
* **[Troubleshoot installation and login](/en/troubleshoot-install)**: `command not found`, PATH, and authentication problems
* **[Troubleshooting](/en/troubleshooting)**: performance, hangs, and search issues
