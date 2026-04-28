> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Tools reference

> Complete reference for the tools Claude Code can use, including permission requirements.

Claude Code has access to a set of built-in tools that help it understand and modify your codebase. The tool names are the exact strings you use in [permission rules](/en/permissions#tool-specific-permission-rules), [subagent tool lists](/en/sub-agents), and [hook matchers](/en/hooks). To disable a tool entirely, add its name to the `deny` array in your [permission settings](/en/permissions#tool-specific-permission-rules).

To add custom tools, connect an [MCP server](/en/mcp). To extend Claude with reusable prompt-based workflows, write a [skill](/en/skills), which runs through the existing `Skill` tool rather than adding a new tool entry.

| Tool                   | Description                                                                                                                                                                                                                                                               | Permission Required |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------ |
| `Agent`                | Spawns a [subagent](/en/sub-agents) with its own context window to handle a task                                                                                                                                                                                          | No                  |
| `AskUserQuestion`      | Asks multiple-choice questions to gather requirements or clarify ambiguity                                                                                                                                                                                                | No                  |
| `Bash`                 | Executes shell commands in your environment. See [Bash tool behavior](#bash-tool-behavior)                                                                                                                                                                                | Yes                 |
| `CronCreate`           | Schedules a recurring or one-shot prompt within the current session. Tasks are session-scoped and restored on `--resume` or `--continue` if unexpired. See [scheduled tasks](/en/scheduled-tasks)                                                                         | No                  |
| `CronDelete`           | Cancels a scheduled task by ID                                                                                                                                                                                                                                            | No                  |
| `CronList`             | Lists all scheduled tasks in the session                                                                                                                                                                                                                                  | No                  |
| `Edit`                 | Makes targeted edits to specific files                                                                                                                                                                                                                                    | Yes                 |
| `EnterPlanMode`        | Switches to plan mode to design an approach before coding                                                                                                                                                                                                                 | No                  |
| `EnterWorktree`        | Creates an isolated [git worktree](/en/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) and switches into it. Pass a `path` to switch into an existing worktree of the current repository instead of creating a new one. Not available to subagents | No                  |
| `ExitPlanMode`         | Presents a plan for approval and exits plan mode                                                                                                                                                                                                                          | Yes                 |
| `ExitWorktree`         | Exits a worktree session and returns to the original directory. Not available to subagents                                                                                                                                                                                | No                  |
| `Glob`                 | Finds files based on pattern matching                                                                                                                                                                                                                                     | No                  |
| `Grep`                 | Searches for patterns in file contents                                                                                                                                                                                                                                    | No                  |
| `ListMcpResourcesTool` | Lists resources exposed by connected [MCP servers](/en/mcp)                                                                                                                                                                                                               | No                  |
| `LSP`                  | Code intelligence via language servers: jump to definitions, find references, report type errors and warnings. See [LSP tool behavior](#lsp-tool-behavior)                                                                                                                | No                  |
| `Monitor`              | Runs a command in the background and feeds each output line back to Claude, so it can react to log entries, file changes, or polled status mid-conversation. See [Monitor tool](#monitor-tool)                                                                            | Yes                 |
| `NotebookEdit`         | Modifies Jupyter notebook cells                                                                                                                                                                                                                                           | Yes                 |
| `PowerShell`           | Executes PowerShell commands natively. See [PowerShell tool](#powershell-tool) for availability                                                                                                                                                                           | Yes                 |
| `Read`                 | Reads the contents of files                                                                                                                                                                                                                                               | No                  |
| `ReadMcpResourceTool`  | Reads a specific MCP resource by URI                                                                                                                                                                                                                                      | No                  |
| `SendMessage`          | Sends a message to an [agent team](/en/agent-teams) teammate, or [resumes a subagent](/en/sub-agents#resume-subagents) by its agent ID. Stopped subagents auto-resume in the background. Only available when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set              | No                  |
| `Skill`                | Executes a [skill](/en/skills#control-who-invokes-a-skill) within the main conversation                                                                                                                                                                                   | Yes                 |
| `TaskCreate`           | Creates a new task in the task list                                                                                                                                                                                                                                       | No                  |
| `TaskGet`              | Retrieves full details for a specific task                                                                                                                                                                                                                                | No                  |
| `TaskList`             | Lists all tasks with their current status                                                                                                                                                                                                                                 | No                  |
| `TaskOutput`           | (Deprecated) Retrieves output from a background task. Prefer `Read` on the task's output file path                                                                                                                                                                        | No                  |
| `TaskStop`             | Kills a running background task by ID                                                                                                                                                                                                                                     | No                  |
| `TaskUpdate`           | Updates task status, dependencies, details, or deletes tasks                                                                                                                                                                                                              | No                  |
| `TeamCreate`           | Creates an [agent team](/en/agent-teams) with multiple teammates. Only available when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set                                                                                                                                     | No                  |
| `TeamDelete`           | Disbands an agent team and cleans up teammate processes. Only available when `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` is set                                                                                                                                              | No                  |
| `TodoWrite`            | Manages the session task checklist. Available in non-interactive mode and the [Agent SDK](/en/headless); interactive sessions use TaskCreate, TaskGet, TaskList, and TaskUpdate instead                                                                                   | No                  |
| `ToolSearch`           | Searches for and loads deferred tools when [tool search](/en/mcp#scale-with-mcp-tool-search) is enabled                                                                                                                                                                   | No                  |
| `WebFetch`             | Fetches content from a specified URL                                                                                                                                                                                                                                      | Yes                 |
| `WebSearch`            | Performs web searches                                                                                                                                                                                                                                                     | Yes                 |
| `Write`                | Creates or overwrites files                                                                                                                                                                                                                                               | Yes                 |

Permission rules can be configured using `/permissions` or in [permission settings](/en/settings#available-settings). Also see [Tool-specific permission rules](/en/permissions#tool-specific-permission-rules).

## Bash tool behavior

The Bash tool runs each command in a separate process with the following persistence behavior:

* When Claude runs `cd` in the main session, the new working directory carries over to later Bash commands as long as it stays inside the project directory or an [additional working directory](/en/permissions#working-directories) you added with `--add-dir`, `/add-dir`, or `additionalDirectories` in settings. Subagent sessions never carry over working directory changes.
  * If `cd` lands outside those directories, Claude Code resets to the project directory and appends `Shell cwd was reset to <dir>` to the tool result.
  * To disable this carry-over so every Bash command starts in the project directory, set `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`.
* Environment variables do not persist. An `export` in one command will not be available in the next.

Activate your virtualenv or conda environment before launching Claude Code. To make environment variables persist across Bash commands, set [`CLAUDE_ENV_FILE`](/en/env-vars) to a shell script before launching Claude Code, or use a [SessionStart hook](/en/hooks#persist-environment-variables) to populate it dynamically.

## LSP tool behavior

The LSP tool gives Claude code intelligence from a running language server. After each file edit, it automatically reports type errors and warnings so Claude can fix issues without a separate build step. Claude can also call it directly to navigate code:

* Jump to a symbol's definition
* Find all references to a symbol
* Get type information at a position
* List symbols in a file or workspace
* Find implementations of an interface
* Trace call hierarchies

The tool is inactive until you install a [code intelligence plugin](/en/discover-plugins#code-intelligence) for your language. The plugin bundles the language server configuration, and you install the server binary separately.

## Monitor tool

<Note>
  The Monitor tool requires Claude Code v2.1.98 or later.
</Note>

The Monitor tool lets Claude watch something in the background and react when it changes, without pausing the conversation. Ask Claude to:

* Tail a log file and flag errors as they appear
* Poll a PR or CI job and report when its status changes
* Watch a directory for file changes
* Track output from any long-running script you point it at

Claude writes a small script for the watch, runs it in the background, and receives each output line as it arrives. You keep working in the same session and Claude interjects when an event lands. Stop a monitor by asking Claude to cancel it or by ending the session.

Monitor uses the same [permission rules as Bash](/en/permissions#tool-specific-permission-rules), so `allow` and `deny` patterns you have set for Bash apply here too. It is not available on Amazon Bedrock, Google Vertex AI, or Microsoft Foundry. It is also not available when `DISABLE_TELEMETRY` or `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` is set.

Plugins can declare monitors that start automatically when the plugin is active, instead of asking Claude to start them. See [plugin monitors](/en/plugins-reference#monitors).

## PowerShell tool

The PowerShell tool lets Claude run PowerShell commands natively. On Windows, this means commands run in PowerShell instead of routing through Git Bash. The tool is rolling out progressively on Windows and is opt-in on Linux, macOS, and WSL.

### Enable the PowerShell tool

Set `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` in your environment or in `settings.json`:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_USE_POWERSHELL_TOOL": "1"
  }
}
```

On Windows, set the variable to `0` to opt out of the rollout. On Linux, macOS, and WSL, the tool requires PowerShell 7 or later: install `pwsh` and ensure it is on your `PATH`.

On Windows, Claude Code auto-detects `pwsh.exe` for PowerShell 7+ with a fallback to `powershell.exe` for PowerShell 5.1. The Bash tool remains registered alongside the PowerShell tool, so you may need to ask Claude to use PowerShell.

### Shell selection in settings, hooks, and skills

Three additional settings control where PowerShell is used:

* `"defaultShell": "powershell"` in [`settings.json`](/en/settings#available-settings): routes interactive `!` commands through PowerShell. Requires the PowerShell tool to be enabled.
* `"shell": "powershell"` on individual [command hooks](/en/hooks#command-hook-fields): runs that hook in PowerShell. Hooks spawn PowerShell directly, so this works regardless of `CLAUDE_CODE_USE_POWERSHELL_TOOL`.
* `shell: powershell` in [skill frontmatter](/en/skills#frontmatter-reference): runs `` !`command` `` blocks in PowerShell. Requires the PowerShell tool to be enabled.

The same main-session working-directory reset behavior described under the Bash tool section applies to PowerShell commands, including the `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR` environment variable.

### Preview limitations

The PowerShell tool has the following known limitations during the preview:

* PowerShell profiles are not loaded
* On Windows, sandboxing is not supported

## Check which tools are available

Your exact tool set depends on your provider, platform, and settings. To check what's loaded in a running session, ask Claude directly:

```text theme={null}
What tools do you have access to?
```

Claude gives a conversational summary. For exact MCP tool names, run `/mcp`.

## See also

* [MCP servers](/en/mcp): add custom tools by connecting external servers
* [Permissions](/en/permissions): permission system, rule syntax, and tool-specific patterns
* [Subagents](/en/sub-agents): configure tool access for subagents
* [Hooks](/en/hooks-guide): run custom commands before or after tool execution
