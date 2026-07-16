> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Debug your configuration

> Diagnose why CLAUDE.md, settings, hooks, MCP servers, or skills aren't taking effect. Use /context, /doctor, /hooks, and /mcp to see what actually loaded.

When Claude ignores an instruction or a feature you configured doesn't appear, the cause is usually that the file didn't load, it loaded from a different location than you expected, or another file overrode it. This guide shows how to inspect what Claude Code actually loaded so you can narrow down which applies.

For installation, authentication, and connectivity problems, see [Troubleshoot installation and login](/en/troubleshoot-install) instead.

## See what loaded into context

The `/context` command shows everything occupying the context window for the current session, broken down by category: system prompt, system tools, MCP tools, custom subagents with the source each loaded from, memory files, skills, and conversation messages. Run it first to confirm whether your `CLAUDE.md`, rules, or skill descriptions are present at all.

For detail on a specific category, follow up with the dedicated command:

| Command          | Shows                                                                                                                                                                                                                                        |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/memory`        | Memory file locations across user and project scopes with the option to open each in your editor, plus access to the auto memory folder and the auto memory toggle                                                                           |
| `/skills`        | Available skills from project, user, and plugin sources                                                                                                                                                                                      |
| `/hooks`         | Active hook configurations                                                                                                                                                                                                                   |
| `/mcp`           | Connected MCP servers and their status                                                                                                                                                                                                       |
| `/permissions`   | Resolved allow and deny rules currently in effect                                                                                                                                                                                            |
| `/doctor`        | Setup checkup: installation health, invalid settings files, unused extensions, duplicate [subagent](/en/sub-agents) names in the same directory, and checked-in `CLAUDE.md` content Claude can derive from the codebase, with proposed fixes |
| `/debug [issue]` | Enables debug logging for the session and prompts Claude to diagnose using the log output and settings paths                                                                                                                                 |
| `/status`        | Active settings sources, including whether managed settings are in effect                                                                                                                                                                    |

If a memory file is missing from the `/context` breakdown, check its location against [how CLAUDE.md files load](/en/memory#how-claude-md-files-load). Subdirectory `CLAUDE.md` files load on demand when Claude reads a file in that directory with the Read tool, not at session start.

If `/context` confirms the file loaded but Claude still isn't following a particular instruction, the issue is likely how the instruction is written rather than whether it loaded. CLAUDE.md works well for the kinds of guidance you'd give a new teammate, such as project conventions, build commands, and where files belong.

Adherence drops when an instruction is vague enough to interpret multiple ways, when two files give conflicting direction, or when the file has grown long enough that individual rules get less attention. [Write effective instructions](/en/memory#write-effective-instructions) covers the specificity, size, and structure patterns that keep adherence high.

<Note>
  CLAUDE.md and permissions solve different problems. CLAUDE.md tells Claude how your project works so it makes good decisions. [Permissions](/en/permissions) and [hooks](/en/hooks) enforce limits regardless of what Claude decides. Use CLAUDE.md for "we do it this way here." Use permissions or hooks for security boundaries and anything that must never happen, where you need a guarantee instead of guidance.
</Note>

## Check resolved settings

Settings merge across managed, user, project, and local scopes. Managed settings always win when present. Among the rest, the closer scope overrides the broader one in the order local, then project, then user. Some settings can also be set by command-line flags or [environment variables](/en/env-vars), which act as another override layer. When a setting doesn't seem to apply, the value you set is usually being overridden by another scope or an environment variable.

Run `/doctor` to check your configuration and installation. It reports what it finds, including invalid settings files, duplicate installations, unused extensions, and {/* min-version: 2.1.206 */}checked-in `CLAUDE.md` content Claude can derive from the codebase, then proposes fixes it applies only after you confirm. The `CLAUDE.md` trim check requires Claude Code v2.1.206 or later. Before v2.1.205, `/doctor` opened a read-only diagnostics screen and pressing `f` sent the report to Claude to fix.

From the terminal, `claude doctor` prints read-only installation and settings diagnostics without starting a session.

Run `/status` to see which settings sources are active, including whether managed settings are in effect. To understand which scope wins for a given key, see [How scopes interact](/en/settings#how-scopes-interact).

## Check MCP servers

Run `/mcp` to see every configured server, its connection status, and whether you have approved it for the current project. A server can be defined correctly but still not provide tools for a few common reasons:

* Project-scoped servers in `.mcp.json` require a one-time approval. If the prompt was dismissed, the server stays disabled until you approve it from `/mcp`.
* A server that fails to start shows as failed in `/mcp`. Relative file paths in `command` or `args` are a frequent cause, since they resolve against the directory you launched Claude Code from rather than the location of `.mcp.json`.
* A server that shows as connected but lists zero tools has started successfully but isn't returning a tool list. Select **Reconnect** from `/mcp`. If the count stays at zero, run `claude --debug mcp` to see the server's stderr output.

For configuration locations and scope rules, see [MCP](/en/mcp).

## Check hooks

Run `/hooks` to list every hook registered for the current session, grouped by event. If a hook you defined doesn't appear, it isn't being read: hooks go under the `"hooks"` key in a settings file, not in a standalone file.

If the hook appears but doesn't fire, the matcher is the usual cause. Check it for these mistakes:

* The `matcher` field is a single string that uses `|` to match multiple tool names, for example `"Edit|Write"`. {/* min-version: 2.1.191 */}A `,` separator is equivalent, so `"Edit,Write"` matches the same tools. Before v2.1.191, a comma fell through to regex evaluation and the matcher never matched, so use `|` if you aren't on v2.1.191 yet.
* A misspelled tool name produces a matcher that matches nothing, so the hook fails silently.
* An array value is a schema error: Claude Code shows a settings error notice and rejects the whole user, project, or local settings file, `claude doctor` reports the validation failure, and no hook from that file appears in `/hooks`. In [managed settings](/en/settings#settings-files), only the invalid entry is stripped and the file's other hooks still apply.

Edits to `settings.json` take effect in the running session after a brief file-stability delay. You don't need to restart. If `/hooks` still shows the old definition a few seconds after saving, run `/hooks` again to refresh the view.

If `/hooks` shows the hook but it still does not fire, the next step is to watch hook evaluation live. Start a session with `claude --debug hooks` and trigger the tool call. The debug log records each event, which matchers were checked, and the hook's exit code and output. See [Debug hooks](/en/hooks#debug-hooks) for the log format and [hooks troubleshooting](/en/hooks-guide#limitations-and-troubleshooting) for common failure patterns.

## Test against a clean configuration

{/* min-version: 2.1.169 */}Start with [`claude --safe-mode`](/en/cli-reference#cli-flags), which launches a session with all customizations disabled, including `CLAUDE.md`, skills, plugins, hooks, MCP servers, and custom commands and agents. Authentication, model selection, built-in tools, and permissions work normally. If the problem disappears in safe mode, one of those surfaces is the cause; use the targeted checks above to find which. Safe mode still applies managed hooks and settings policy from your organization. Managed plugins, skills, CLAUDE.md, and MCP servers are turned off.

If the problem persists in safe mode, or your settings themselves are suspect, compare against a session that loads nothing from your usual setup. Point [`CLAUDE_CONFIG_DIR`](/en/env-vars) at an empty directory to bypass everything under `~/.claude`, and launch from a directory that has no `.claude` folder, `.mcp.json`, or `CLAUDE.md` so project configuration is also skipped.

```bash theme={null}
cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-clean claude
```

The clean session has no user or project settings, hooks, MCP servers, plugins, or memory. On the first launch, expect the first-run setup screens, starting with theme selection. If you see them, the clean configuration directory is in effect. Later launches with the same directory skip these screens because Claude Code saves onboarding state there.

* Managed settings still apply if your organization deploys them, since they live at a system path outside `~/.claude`
* On Linux and Windows, you'll be prompted to log in again because credentials are stored under the configuration directory
* On macOS, credentials are in the Keychain and carry over to the clean session

If the problem disappears here, the cause is somewhere in your real `~/.claude` or project `.claude` files. Reintroduce them one at a time, by copying files into the temporary directory or by launching from your project, to find which one. If it persists in the clean session, the cause is outside your user and project configuration. Run `/status` to check whether managed settings are in effect, look for [environment variables](/en/env-vars) that affect Claude Code, then see [Troubleshooting](/en/troubleshooting).

## Check common causes

Most configuration surprises trace back to a small set of location and syntax rules. Check these before assuming a bug:

| Symptom                                                              | Cause                                                                                                                      | Fix                                                                                                                                                                                                                                                          |
| :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Hook never fires                                                     | `matcher` is a JSON array instead of a string                                                                              | Use a single string with `\|` to match multiple tools, for example `"Edit\|Write"`. See [matcher patterns](/en/hooks#matcher-patterns).                                                                                                                      |
| Hook never fires                                                     | `matcher` uses `,` as a separator on a version before v2.1.191                                                             | {/* min-version: 2.1.191 */}Claude Code v2.1.191 or later treats `,` as a list separator like `\|`. Earlier versions evaluate a comma as a literal character, so `"Edit,Write"` matches nothing. Use `\|` instead, or upgrade Claude Code.                   |
| Hook never fires                                                     | `matcher` value is lowercase, for example `"bash"`                                                                         | Matching is case-sensitive. Tool names are capitalized: `Bash`, `Edit`, `Write`, `Read`.                                                                                                                                                                     |
| Hook never fires                                                     | Hooks are defined in a standalone file instead of `settings.json`                                                          | There is no standalone hooks file for project or user config. Define hooks under the `"hooks"` key in `settings.json`. Only [plugins](/en/plugins-reference#hooks) load a separate `hooks/hooks.json`. See [hook configuration](/en/hooks).                  |
| Permissions, hooks, or env set globally are ignored                  | Configuration was added to `~/.claude.json`                                                                                | `~/.claude.json` holds app state and UI toggles. `permissions`, `hooks`, and `env` belong in `~/.claude/settings.json`. These are two different files.                                                                                                       |
| A `settings.json` value seems ignored                                | The same key is set in `settings.local.json`                                                                               | `settings.local.json` overrides `settings.json`, and both override `~/.claude/settings.json`. See [settings precedence](/en/settings#how-scopes-interact).                                                                                                   |
| Skill doesn't appear in `/skills`                                    | Skill file is at `.claude/skills/name.md` instead of in a folder                                                           | Use a folder with `SKILL.md` inside: `.claude/skills/name/SKILL.md`.                                                                                                                                                                                         |
| Skill appears in `/skills` but Claude never invokes it               | Skill has `disable-model-invocation: true` in its frontmatter, or its description doesn't match how you phrase the request | Check the badge in `/skills`: a "user-only" label means Claude won't trigger it on its own. See [skill invocation](/en/skills).                                                                                                                              |
| Subdirectory `CLAUDE.md` instructions seem ignored                   | Subdirectory files load on demand, not at session start                                                                    | They load when Claude reads a file in that directory with the Read tool, not at launch and not when writing or creating files there. See [how CLAUDE.md files load](/en/memory#how-claude-md-files-load).                                                    |
| Subagent ignores `CLAUDE.md` instructions                            | The built-in Explore and Plan agents skip `CLAUDE.md`. Custom subagents load it the same way the main conversation does    | For Explore or Plan, restate the instruction in your delegating prompt. For a custom subagent, put critical instructions in the agent file body, which becomes the agent's system prompt. See [what loads at startup](/en/sub-agents#what-loads-at-startup). |
| Cleanup logic never runs at session end                              | No `SessionEnd` hook configured                                                                                            | Add a `SessionEnd` hook in `settings.json`. See the [hook events list](/en/hooks#hook-events).                                                                                                                                                               |
| MCP servers in `.mcp.json` never load                                | File is under `.claude/` or uses Claude Desktop's config format                                                            | Project MCP config goes at the repository root as `.mcp.json`, not inside `.claude/`. See [MCP configuration](/en/mcp).                                                                                                                                      |
| MCP servers added under `mcpServers` in `settings.json` never appear | `settings.json` does not read an `mcpServers` key                                                                          | Define project servers in `.mcp.json` at the repository root, or run `claude mcp add --scope user` for user-scoped servers. See [MCP configuration](/en/mcp).                                                                                                |
| Project MCP server added but doesn't appear                          | The one-time approval prompt was dismissed                                                                                 | Project-scoped servers require approval. Run `/mcp` to see status and approve.                                                                                                                                                                               |
| MCP server fails to start from some directories                      | `command` or `args` uses a relative file path                                                                              | Use absolute paths for local scripts. Executables on your `PATH` like `npx` or `uvx` work as-is.                                                                                                                                                             |
| MCP server starts without expected environment variables             | Variables are in `settings.json` `env`, which doesn't propagate to MCP child processes                                     | Set per-server `env` inside `.mcp.json` instead.                                                                                                                                                                                                             |
| `Bash(rm *)` deny rule doesn't block `/bin/rm` or `find -delete`     | Prefix rules match the literal command string, not the underlying executable                                               | Add explicit patterns for each variant, or use a [PreToolUse hook](/en/hooks-guide) or the [sandbox](/en/sandboxing) for a hard guarantee.                                                                                                                   |

## Related resources

For full reference on each configuration surface, see the dedicated page:

* **[`.claude` directory reference](/en/claude-directory)**: every config file location and what reads it
* **[Settings](/en/settings)**: precedence order and the full key list
* **[Hooks reference](/en/hooks)**: event names, payloads, and `--debug hooks` output format
* **[MCP](/en/mcp)**: server configuration, approval, and `/mcp` output
* **[Troubleshoot installation and login](/en/troubleshoot-install)**: `command not found`, PATH, and authentication problems
* **[Troubleshooting](/en/troubleshooting)**: performance, hangs, and search issues
