> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create custom subagents

> Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

Subagents are specialized AI assistants that handle specific types of tasks. Use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary. Define a custom subagent when you keep spawning the same kind of worker with the same instructions.

Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent, which works independently and returns results. To see the context savings in practice, the [context window visualization](/docs/en/context-window) walks through a session where a subagent handles research in its own separate window.

<Note>
  Subagents work within a single session. To run many independent sessions in parallel and monitor them from one place, see [background agents](/docs/en/agent-view). For sessions that communicate with each other, see [agent teams](/docs/en/agent-teams).
</Note>

Subagents help you:

* **Preserve context** by keeping exploration and implementation out of your main conversation
* **Enforce constraints** by limiting which tools a subagent can use
* **Reuse configurations** across projects with user-level subagents
* **Specialize behavior** with focused system prompts for specific domains
* **Control costs** by routing tasks to faster, cheaper models like Haiku

Claude uses each subagent's description to decide when to delegate tasks. When you create a subagent, write a clear description so Claude knows when to use it.

Claude Code includes several built-in subagents such as Explore, Plan, and general-purpose. You can also create custom subagents to handle specific tasks.

## Built-in subagents

Claude Code includes built-in subagents that Claude automatically uses when appropriate. Each inherits the parent conversation's permissions with additional tool restrictions.

Explore and Plan skip your CLAUDE.md files and the parent session's git status to keep research fast and inexpensive. Every other built-in and [custom subagent](#configure-subagents) loads both. For the full breakdown of what reaches a subagent, see [what loads at startup](#what-loads-at-startup).

<Tabs>
  <Tab title="Explore">
    A fast, read-only agent optimized for searching and analyzing codebases.

    * **Model**: inherits from the main conversation, capped at Opus on the Claude API, so Explore never runs on a more expensive model than the one you already chose for the session
    * **Tools**: read-only tools; Write and Edit are denied
    * **Purpose**: file discovery, code search, codebase exploration

    {/* min-version: 2.1.198 */}As of v2.1.198, Explore inherits the main conversation's model instead of always running on Haiku. On the Claude API, the inherited model is capped at Opus: a main conversation on a higher tier runs Explore on Opus, and a main conversation on Sonnet or Haiku runs Explore on that same model. On any other provider, such as [Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, or Claude Platform on AWS](/docs/en/third-party-integrations), Explore inherits the main conversation's model directly.

    A [user or project subagent](#choose-the-subagent-scope) named `Explore` overrides the built-in and keeps its own `model` field, so define one with `model: haiku` to keep exploration on a lower-cost model.

    Claude delegates to Explore when it needs to search or understand a codebase without making changes. This keeps exploration results out of your main conversation context.

    When invoking Explore, Claude specifies a thoroughness level: **quick** for targeted lookups, **medium** for balanced exploration, or **very thorough** for comprehensive analysis.
  </Tab>

  <Tab title="Plan">
    A research agent used during [plan mode](/docs/en/permission-modes#analyze-before-you-edit-with-plan-mode) to gather context before presenting a plan.

    * **Model**: inherits from the main conversation
    * **Tools**: read-only tools; Write and Edit are denied
    * **Purpose**: codebase research for planning

    When you're in plan mode and Claude needs to understand your codebase, it delegates research to the Plan subagent so that exploration output stays in a separate context window while the main conversation remains read-only.
  </Tab>

  <Tab title="General-purpose">
    A capable agent for complex, multi-step tasks that require both exploration and action.

    * **Model**: inherits from the main conversation
    * **Tools**: all tools
    * **Purpose**: complex research, multi-step operations, code modifications

    Claude delegates to general-purpose when the task requires both exploration and modification, complex reasoning to interpret results, or multiple dependent steps.
  </Tab>

  <Tab title="Other">
    Claude Code includes additional helper agents for specific tasks. These are typically invoked automatically, so you don't need to use them directly.

    | Agent             | Model  | When Claude uses it                                      |
    | :---------------- | :----- | :------------------------------------------------------- |
    | statusline-setup  | Sonnet | When you run `/statusline` to configure your status line |
    | claude-code-guide | Haiku  | When you ask questions about Claude Code features        |
  </Tab>
</Tabs>

Built-in subagents are registered by default in interactive sessions. To restrict them:

* To block a specific built-in type, add it to `permissions.deny` as shown in [Disable specific subagents](#disable-specific-subagents).
* To prevent Claude from delegating to any subagent, deny the `Agent` tool itself with [`permissions.deny`](/docs/en/permissions#tool-specific-permission-rules).
* {/* min-version: 2.1.198 */}To remove only the built-in `Explore` and `Plan` subagents, set [`CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`](/docs/en/env-vars). Claude reads and explores files directly instead of delegating to them. Requires Claude Code v2.1.198 or later.
* In [non-interactive mode](/docs/en/headless) and the [Agent SDK](/docs/en/agent-sdk/overview), set [`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`](/docs/en/env-vars) to remove all built-in types and supply only your own.

Beyond these built-in subagents, you can create your own with custom prompts, tool restrictions, permission modes, hooks, and skills. The following sections show how to get started and customize subagents.

## Quickstart: create your first subagent

Subagents are Markdown files with YAML frontmatter. To create one, ask Claude to write it for you, or [write the file yourself](#write-subagent-files).

{/* min-version: 2.1.198 */}As of v2.1.198, the `/agents` command no longer opens the interactive creation wizard; running it prints a reminder to ask Claude or edit `.claude/agents/` directly. Subagent files, frontmatter fields, and the `.claude/agents/` and `~/.claude/agents/` locations are unchanged; only the terminal wizard is removed.

This walkthrough creates a user-level subagent that reviews code and suggests improvements.

<Steps>
  <Step title="Ask Claude to create the subagent">
    In Claude Code, describe the subagent you want and where to save it:

    ```text wrap theme={null}
    Create a personal code-improver subagent in ~/.claude/agents/ that scans
    files and suggests improvements for readability, performance, and best
    practices. It should explain each issue, show the current code, and
    provide an improved version. Make it read-only and have it use Sonnet.
    ```

    Claude writes the file with a `name`, a `description`, a `tools` list, a `model`, and a system prompt.
  </Step>

  <Step title="Review the file">
    Open `~/.claude/agents/code-improver.md` and confirm the frontmatter matches what you asked for. The result looks like this:

    ```markdown theme={null}
    ---
    name: code-improver
    description: Scans files and suggests improvements for readability, performance, and best practices. Use after writing or modifying code.
    tools: Read, Grep, Glob
    model: sonnet
    ---

    You are a code improvement specialist. For each issue you find, explain
    the problem, show the current code, and provide an improved version.
    ```

    Because the file lives in `~/.claude/agents/`, the subagent is available in every project on your machine. To scope it to one project instead, move it to that project's `.claude/agents/` directory. [Choose the subagent scope](#choose-the-subagent-scope) compares the two.
  </Step>

  <Step title="Try it out">
    Ask Claude to delegate to the new subagent:

    ```text wrap theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude delegates to your new subagent, which scans the codebase and returns improvement suggestions.

    If Claude can't find the new subagent, restart Claude Code and try again. This happens only when `~/.claude/agents/` didn't exist before the session started, because a running session doesn't detect a newly created `agents` directory.
  </Step>
</Steps>

You now have a subagent you can use in any project on your machine to analyze codebases and suggest improvements.

You can also write subagent files by hand, define them via CLI flags, or distribute them through plugins. The following sections cover all configuration options.

<Note>
  On Claude Code v2.1.197 and earlier, `/agents` opens an interactive wizard with a **Running** tab that lists live subagents and a **Library** tab for creating, editing, and deleting them. {/* max-version: 2.1.197 */}
</Note>

## Configure subagents

A subagent's file location determines who it's available to, and its frontmatter determines what it can do. This section covers where subagent files live and every field they support.

### Choose the subagent scope

Store subagent files in different locations depending on scope. When multiple subagents share the same name, Claude Code uses the one from the higher-priority location.

| Location                     | Scope                   | Priority    | How to create                                 |
| :--------------------------- | :---------------------- | :---------- | :-------------------------------------------- |
| Managed settings             | Organization-wide       | 1 (highest) | Deployed via [managed settings](/docs/en/settings) |
| `--agents` CLI flag          | Current session         | 2           | Pass JSON when launching Claude Code          |
| `.claude/agents/`            | Current project         | 3           | Ask Claude, or create the file manually       |
| `~/.claude/agents/`          | All your projects       | 4           | Ask Claude, or create the file manually       |
| Plugin's `agents/` directory | Where plugin is enabled | 5 (lowest)  | Installed with [plugins](/docs/en/plugins)         |

**Project subagents** (`.claude/agents/`) are ideal for subagents specific to a codebase. Check them into version control so your team can use and improve them collaboratively.

Project subagents are discovered by walking up from the current working directory, so every `.claude/agents/` between there and the repository root is scanned. {/* min-version: 2.1.178 */}As of v2.1.178, when more than one of these nested directories defines the same `name`, Claude Code uses the definition closest to the working directory.

Directories added with `--add-dir` are also scanned: a `.claude/agents/` folder inside an added directory loads alongside project subagents. See [Additional directories](/docs/en/permissions#additional-directories-grant-file-access-not-configuration) for which other configuration types load from `--add-dir`. To share subagents across projects without `--add-dir`, use `~/.claude/agents/` or a [plugin](/docs/en/plugins).

**User subagents** (`~/.claude/agents/`) are personal subagents available in all your projects.

Claude Code scans `.claude/agents/` and `~/.claude/agents/` recursively, so you can organize definitions into subfolders such as `agents/review/` or `agents/research/`. The subdirectory path doesn't affect how a subagent is identified or invoked, because identity comes only from the `name` frontmatter field.

Keep `name` values unique across the whole tree: if two files under the same `.claude/agents/` directory, including its subfolders, declare the same name, Claude Code loads only one of them, chosen by filesystem read order rather than a documented precedence. Across nested project directories, the definition closest to the working directory wins, as described above. {/* min-version: 2.1.205 */}The [`/doctor`](/docs/en/commands#all-commands) setup checkup reports files in the same directory that share a name and proposes renaming or removing all but one. Before v2.1.205, `/doctor` opened a diagnostics screen that listed duplicates and showed which definition was active.

Plugin `agents/` directories are also scanned recursively. Unlike project and user scopes, a subfolder inside a plugin's `agents/` directory becomes part of the [scoped identifier](#invoke-subagents-explicitly): a file at `agents/review/security.md` in plugin `my-plugin` registers as `my-plugin:review:security`.

**CLI-defined subagents** are passed as JSON when launching Claude Code. They exist only for that session and aren't saved to disk, making them useful for quick testing or automation scripts. You can define multiple subagents in a single `--agents` call:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    claude --agents '{
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }'
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    claude --agents @'
    {
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }
    '@
    ```
  </Tab>
</Tabs>

The `--agents` flag accepts JSON with the same [frontmatter](#supported-frontmatter-fields) fields as file-based subagents: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, and `color`. Use `prompt` for the system prompt, equivalent to the markdown body in file-based subagents.

**Managed subagents** are deployed by organization administrators. Place markdown files in `.claude/agents/` inside the [managed settings directory](/docs/en/settings#settings-files), using the same frontmatter format as project and user subagents. Managed definitions take precedence over project and user subagents with the same name.

**Plugin subagents** come from [plugins](/docs/en/plugins) you've installed. They load automatically alongside your custom subagents and appear in the @-mention typeahead under their scoped name. See the [plugin components reference](/docs/en/plugins-reference#agents) for details on creating plugin subagents.

<Note>
  For security reasons, plugin subagents don't support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored when loading agents from a plugin. If you need them, copy the agent file into `.claude/agents/` or `~/.claude/agents/`. You can also add rules to [`permissions.allow`](/docs/en/settings#permission-settings) in `settings.json` or `settings.local.json`, but these rules apply to the entire session, not only the plugin subagent.
</Note>

Subagent definitions from any of these scopes are also available to [agent teams](/docs/en/agent-teams#use-subagent-definitions-for-teammates): when spawning a teammate, you can reference a subagent type and the teammate uses its `tools` and `model`, with the definition's body appended to the teammate's system prompt as additional instructions. See [agent teams](/docs/en/agent-teams#use-subagent-definitions-for-teammates) for which frontmatter fields apply on that path.

### Write subagent files

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:

<Note>
  Claude Code watches `~/.claude/agents/` and `.claude/agents/`. When you add or edit a subagent file on disk, or ask Claude to write one for you, Claude Code detects the change within a few seconds and the next delegation uses the updated definition, with no restart needed.

  Two cases still need a restart:

  * The watcher covers only directories that existed when the session started, so after creating a scope's first agent file in a new `agents` directory, restart to load it.
  * Sessions started with `--disable-slash-commands` don't watch these directories at all.
</Note>

```markdown theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

The frontmatter defines the subagent's metadata and configuration. The body becomes the system prompt that guides the subagent's behavior. Subagents receive only this system prompt plus basic environment details like the working directory, not the full Claude Code system prompt.

In [non-interactive mode](/docs/en/headless), the [`--append-subagent-system-prompt`](/docs/en/cli-reference#cli-flags) flag appends the text you provide to the end of every subagent's system prompt, including nested subagents. Requires Claude Code v2.1.205 or later.

A subagent starts in the main conversation's current working directory. Within a subagent, `cd` commands don't persist between Bash or PowerShell tool calls and don't affect the main conversation's working directory. To give the subagent an isolated copy of the repository instead, set [`isolation: worktree`](#supported-frontmatter-fields).

{/* min-version: 2.1.203 */}A subagent with `isolation: worktree` runs its Bash and PowerShell commands inside its worktree. A command whose working directory resolves to your main checkout instead, for example because the worktree directory was removed while the subagent was running, fails with an error. Before v2.1.203, such a command could run in the main checkout.

{/* min-version: 2.1.210 */}This working-directory check covers the whole repository containing the directory you launched Claude Code from. When your session runs in a linked [worktree](/docs/en/worktrees) of its own, the check also covers the main checkout that worktree is linked from. Before v2.1.210, the check covered only the launch directory itself. A command whose working directory resolved elsewhere in the same repository, such as the repository root when you launched Claude Code from a monorepo subdirectory, ran there instead of failing.

#### Supported frontmatter fields

The following fields can be used in the YAML frontmatter. Only `name` and `description` are required.

| Field             | Required | Description                                                                                                                                                                                                                                                                                                                              |
| :---------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | Unique identifier using lowercase letters and hyphens. [Hooks](/docs/en/hooks#subagentstart) receive this value as `agent_type`. The filename doesn't have to match                                                                                                                                                                           |
| `description`     | Yes      | When Claude should delegate to this subagent                                                                                                                                                                                                                                                                                             |
| `tools`           | No       | [Tools](#available-tools) the subagent can use. Inherits all tools if omitted. If no entry in the list resolves to a tool, the subagent fails to launch with an error naming the entries. To preload Skills into context, use the `skills` field rather than listing `Skill` here                                                        |
| `disallowedTools` | No       | Tools to deny, removed from inherited or specified list                                                                                                                                                                                                                                                                                  |
| `model`           | No       | [Model](#choose-a-model) to use: `sonnet`, `opus`, `haiku`, `fable`, a full model ID (for example, `claude-opus-4-8`), or `inherit`. Defaults to `inherit`                                                                                                                                                                               |
| `permissionMode`  | No       | [Permission mode](#permission-modes): `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`, or {/* min-version: 2.1.200 */}`manual` as an alias for `default`. The `manual` alias requires Claude Code v2.1.200 or later. Ignored for [plugin subagents](#choose-the-subagent-scope)                                 |
| `maxTurns`        | No       | Maximum number of agentic turns before the subagent stops                                                                                                                                                                                                                                                                                |
| `skills`          | No       | [Skills](/docs/en/skills) to preload into the subagent's context at startup. The full skill content is injected, not only the description. Subagents can still invoke unlisted project, user, and plugin skills through the Skill tool                                                                                                        |
| `mcpServers`      | No       | [MCP servers](/docs/en/mcp) available to this subagent. Each entry is either a server name referencing an already-configured server (e.g., `"slack"`) or an inline definition with the server name as key and a full [MCP server config](/docs/en/mcp#installing-mcp-servers) as value. Ignored for [plugin subagents](#choose-the-subagent-scope) |
| `hooks`           | No       | [Lifecycle hooks](#define-hooks-for-subagents) scoped to this subagent. Ignored for [plugin subagents](#choose-the-subagent-scope)                                                                                                                                                                                                       |
| `memory`          | No       | [Persistent memory scope](#enable-persistent-memory): `user`, `project`, or `local`. Enables cross-session learning                                                                                                                                                                                                                      |
| `background`      | No       | Set to `true` to always run this subagent as a [background task](#run-subagents-in-foreground-or-background), even when Claude needs its result right away. When unset, Claude chooses, and {/* min-version: 2.1.198 */}as of v2.1.198 it runs subagents in the background by default                                                    |
| `effort`          | No       | Effort level when this subagent is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model                                                                                                                                    |
| `isolation`       | No       | Set to `worktree` to run the subagent in a temporary [git worktree](/docs/en/worktrees), giving it an isolated copy of the repository branched by default from your [default branch](/docs/en/worktrees#choose-the-base-branch) rather than the parent session's `HEAD`. The worktree is automatically cleaned up if the subagent makes no changes |
| `color`           | No       | Display color for the subagent in the task list and transcript. Accepts `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`                                                                                                                                                                                          |
| `initialPrompt`   | No       | Auto-submitted as the first user turn when this agent runs as the main session agent (via `--agent` or the `agent` setting). [Commands](/docs/en/commands) and [skills](/docs/en/skills) are processed. Prepended to any user-provided prompt                                                                                                      |

### Choose a model

The `model` field controls which [AI model](/docs/en/model-config) the subagent uses:

* **Model alias**: use one of the available aliases: `sonnet`, `opus`, `haiku`, or `fable`
* **Full model ID**: use a full model ID such as `claude-opus-4-8` or `claude-sonnet-5`. Accepts the same values as the `--model` flag
* **inherit**: use the same model as the main conversation
* **Omitted**: defaults to `inherit` and uses the same model as the main conversation

When Claude invokes a subagent, it can also pass a `model` parameter for that specific invocation. Claude Code resolves the subagent's model in this order:

1. The [`CLAUDE_CODE_SUBAGENT_MODEL`](/docs/en/model-config#environment-variables) environment variable, when set to a model alias or model ID
2. The per-invocation `model` parameter
3. The subagent definition's `model` frontmatter
4. The main conversation's model

{/* min-version: 2.1.196 */}As of v2.1.196, setting `CLAUDE_CODE_SUBAGENT_MODEL` to `inherit` is the same as leaving it unset: resolution continues with the per-invocation `model` parameter, then the frontmatter. In earlier versions, `inherit` forced subagents onto the main conversation's model and ignored both of those sources.

Claude Code checks the environment variable, per-invocation parameter, and frontmatter values against your organization's [`availableModels`](/docs/en/model-config#restrict-model-selection) allowlist. It skips a value that resolves to an excluded model and runs the subagent on the inherited model instead.

{/* min-version: 2.1.211 */}A per-invocation `model` parameter also applies when the subagent is [resumed or sent a follow-up message](#resume-subagents), so the subagent stays on that model. Before v2.1.211, resuming dropped the per-invocation value and the subagent reverted to its definition's `model` field or, without one, the main conversation's model.

{/* min-version: 2.1.198 */}As of v2.1.198, subagents also inherit the main conversation's [extended thinking](/docs/en/model-config#extended-thinking) configuration: if thinking is on in your session, it's on for the subagent, and if it's off, it stays off. There is no per-subagent thinking setting. Before v2.1.198, subagents ran with extended thinking disabled regardless of the main conversation's setting.

### Control subagent capabilities

You can control what subagents can do through tool access, permission modes, and conditional rules.

#### Available tools

Subagents inherit the [internal tools](/docs/en/tools-reference) and MCP tools available in the main conversation by default. The following tools depend on the main conversation's UI or session state and aren't available to subagents, even when listed in the `tools` field:

* `AskUserQuestion`
* `EndConversation`, which can end only the main conversation; see [EndConversation tool behavior](/docs/en/tools-reference#endconversation-tool-behavior)
* `EnterPlanMode`
* `ExitPlanMode`, unless the subagent's [`permissionMode`](#permission-modes) is `plan`
* `ScheduleWakeup`
* `WaitForMcpServers`

The `Agent` tool itself is inherited, so a subagent can [spawn nested subagents](#spawn-nested-subagents).

To restrict tools, use the `tools` field as an allowlist or the `disallowedTools` field as a denylist. This example uses `tools` to allow only Read, Grep, Glob, and Bash. The subagent can't edit files, write files, or use any MCP tools:

```yaml theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

This example uses `disallowedTools` to inherit every tool from the main conversation except Write and Edit. The subagent keeps Bash, MCP tools, and everything else:

```yaml theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

If both are set, `disallowedTools` is applied first, then `tools` is resolved against the remaining pool. A tool listed in both is removed.

When nothing in the `tools` list resolves to a tool, for example because every entry is misspelled or names a tool that isn't available to subagents, Claude Code refuses to launch the subagent and the Agent tool returns an error naming the unresolved entries. {/* min-version: 2.1.208 */}Before v2.1.208, that subagent launched with no tools and could return an empty or confusing result.

Both fields accept MCP server-level patterns in addition to exact tool names: `mcp__<server>` or `mcp__<server>__*` grants or removes every tool from the named server. In `disallowedTools`, `mcp__*` also removes every MCP tool from any server. This example removes every tool from the `github` MCP server while keeping tools from other servers and every built-in tool:

```yaml theme={null}
---
name: local-only
description: Inherits every tool except those from the github MCP server
disallowedTools: mcp__github
---
```

#### Restrict which subagents can be spawned

When an agent runs as the main thread with `claude --agent`, it can spawn subagents using the Agent tool. To restrict which subagent types it can spawn, use `Agent(agent_type)` syntax in the `tools` field.

<Note>In version 2.1.63, the Task tool was renamed to Agent. Existing `Task(...)` references in settings and agent definitions still work as aliases.</Note>

```yaml theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

This is an allowlist: only the `worker` and `researcher` subagents can be spawned. If the agent tries to spawn any other type, the request fails and the agent sees only the allowed types in its prompt. To block specific agents while allowing all others, use [`permissions.deny`](#disable-specific-subagents) instead.

To allow spawning any subagent without restrictions, use `Agent` without parentheses:

```yaml theme={null}
tools: Agent, Read, Bash
```

If `Agent` is omitted from the `tools` list entirely, the agent can't spawn any subagents.

The `Agent(agent_type)` allowlist syntax applies only to an agent running as the main thread with `claude --agent`. In a subagent definition, listing `Agent` in `tools` lets that subagent [spawn nested subagents](#spawn-nested-subagents), but any type list inside the parentheses is ignored.

#### Scope MCP servers to a subagent

Use the `mcpServers` field to give a subagent access to [MCP](/docs/en/mcp) servers that aren't available in the main conversation. Inline servers defined here are connected when the subagent starts and disconnected when it finishes. String references share the parent session's connection.

<Note>
  The `mcpServers` field applies in both contexts where an agent file can run:

  * As a subagent, spawned through the Agent tool or an @-mention
  * As the main session, launched with [`--agent`](#invoke-subagents-explicitly) or the `agent` setting

  When the agent is the main session, inline server definitions connect at startup alongside servers from [`.mcp.json`](/docs/en/mcp) and settings files.
</Note>

Each entry in the list is either an inline server definition or a string referencing an MCP server already configured in your session:

```yaml theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Inline definitions use the same schema as `.mcp.json` server entries, keyed by the server name, and support the `stdio`, `http`, `sse`, and `ws` types.

To keep an MCP server out of the main conversation entirely and avoid its tool descriptions consuming context there, define it inline here rather than in `.mcp.json`. The subagent gets the tools; the parent conversation doesn't.

As of v2.1.153, the MCP restrictions that apply to the main session also cover servers declared in subagent frontmatter:

* [`--strict-mcp-config`](/docs/en/cli-reference) and [`--bare`](/docs/en/cli-reference)
* [Enterprise managed MCP configuration](/docs/en/managed-mcp)
* [`allowedMcpServers` and `deniedMcpServers` policies](/docs/en/managed-mcp#policy-based-control-with-allowlists-and-denylists)

When one of these blocks a server, Claude Code skips it and shows a warning naming the blocked servers.

Managed-settings restrictions apply to every subagent regardless of how it is defined. `--strict-mcp-config` doesn't filter servers you pass inline via `--agents` or the SDK `agents` option, since those are explicit caller input.

#### Permission modes

The `permissionMode` field controls how the subagent handles permission prompts. Subagents inherit the permission context from the main conversation and can override the mode, except when the parent mode takes precedence as described below.

| Mode                | Behavior                                                                                                                                                                                                                                                                                                                        |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `default`           | Standard permission checking with prompts                                                                                                                                                                                                                                                                                       |
| `acceptEdits`       | Auto-accept file edits and common filesystem commands for paths in the working directory or `additionalDirectories`                                                                                                                                                                                                             |
| `auto`              | [Auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode): a background classifier reviews commands and protected-directory writes                                                                                                                                                                                     |
| `dontAsk`           | Auto-deny permission prompts. Explicitly allowed tools still work; `AskUserQuestion`, connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools), and MCP tools marked [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool) are denied even if you've allowed them |
| `bypassPermissions` | Skip permission prompts                                                                                                                                                                                                                                                                                                         |
| `plan`              | Plan mode (read-only exploration)                                                                                                                                                                                                                                                                                               |

<Warning>
  Use `bypassPermissions` with caution. It skips permission prompts, allowing the subagent to execute operations without approval, including writes to `.git`, `.config/git`, `.claude`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, and `.mvn`.

  Explicit [`ask` rules](/docs/en/permissions#manage-permissions), connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools), MCP tools marked [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool), and root and home directory removals such as `rm -rf /` still prompt. See [permission modes](/docs/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) for details.
</Warning>

If the parent uses `bypassPermissions` or `acceptEdits`, this takes precedence and can't be overridden. If the parent uses [auto mode](/docs/en/permission-modes#eliminate-prompts-with-auto-mode), the subagent inherits auto mode and any `permissionMode` in its frontmatter is ignored: the classifier evaluates the subagent's tool calls with the same block and allow rules as the parent session.

#### Preload skills into subagents

Use the `skills` field to inject skill content into a subagent's context at startup. This gives the subagent domain knowledge without requiring it to discover and load skills during execution.

```yaml theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

The full content of each listed skill is injected into the subagent's context at startup. This field controls which skills are preloaded, not which skills the subagent can access: without it, the subagent can still discover and invoke project, user, and plugin skills through the Skill tool during execution. To prevent a subagent from invoking skills entirely, omit `Skill` from the [`tools`](#available-tools) list or add it to `disallowedTools`.

You can't preload skills that set [`disable-model-invocation: true`](/docs/en/skills#control-who-invokes-a-skill), since preloading draws from the same set of skills Claude can invoke. If a listed skill is missing or disabled, Claude Code skips it and logs a warning to the debug log.

<Note>
  This is the inverse of [running a skill in a subagent](/docs/en/skills#run-skills-in-a-subagent). With `skills` in a subagent, the subagent controls the system prompt and loads skill content. With `context: fork` in a skill, the skill content is injected into the agent you specify. Both use the same underlying system.
</Note>

#### Enable persistent memory

The `memory` field gives the subagent a persistent directory that survives across conversations. The subagent uses this directory to build up knowledge over time, such as codebase patterns, debugging insights, and architectural decisions.

```yaml theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Choose a scope based on how broadly the memory should apply:

| Scope     | Location                                      | Use when                                                                                   |
| :-------- | :-------------------------------------------- | :----------------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | the subagent should remember learnings across all projects                                 |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | the subagent's knowledge is project-specific and shareable via version control             |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | the subagent's knowledge is project-specific but shouldn't be checked into version control |

When memory is enabled:

* The subagent's system prompt includes instructions for reading and writing to the memory directory.
* The subagent's system prompt also includes the first 200 lines or 25KB of `MEMORY.md` in the memory directory, whichever comes first, with instructions to curate `MEMORY.md` if it exceeds that limit.
* Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files.

##### Persistent memory tips

* `project` is the recommended default scope. It makes subagent knowledge shareable via version control.
* Ask the subagent to consult its memory before starting work: "Review this PR, and check your memory for patterns you've seen before."
* Ask the subagent to update its memory after completing a task: "Now that you're done, save what you learned to your memory." Over time, this builds a knowledge base that makes the subagent more effective.
* Include memory instructions directly in the subagent's markdown file so it proactively maintains its own knowledge base:

  ```markdown theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Conditional rules with hooks

For more dynamic control over tool usage, use `PreToolUse` hooks to validate operations before they execute. This is useful when you need to allow some operations of a tool while blocking others.

This example creates a subagent that only allows read-only database queries. The `PreToolUse` hook runs the script specified in `command` before each Bash command executes:

```yaml theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [passes hook input as JSON](/docs/en/hooks#pretooluse-input) via stdin to hook commands. The validation script reads this JSON, extracts the Bash command, and [exits with code 2](/docs/en/hooks#exit-code-2-behavior-per-event) to block write operations:

```bash theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

See [Hook input](/docs/en/hooks#pretooluse-input) for the complete input schema and [exit codes](/docs/en/hooks#exit-code-output) for how exit codes affect behavior. On Windows, write hook scripts in PowerShell and add `shell: powershell` to the hook entry as shown in [running hooks in PowerShell](/docs/en/hooks#windows-powershell-tool).

#### Disable specific subagents

You can prevent Claude from using specific subagents by adding them to the `deny` array in your [settings](/docs/en/settings#permission-settings). Use the format `Agent(subagent-name)` where `subagent-name` matches the subagent's name field.

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

This works for both built-in and custom subagents. You can also use the `--disallowedTools` CLI flag:

```bash theme={null}
claude --disallowedTools "Agent(Explore)"
```

See [Permissions documentation](/docs/en/permissions#tool-specific-permission-rules) for more details on permission rules.

### Define hooks for subagents

Subagents can define [hooks](/docs/en/hooks) that run during the subagent's lifecycle. There are two ways to configure hooks:

* **In the subagent's frontmatter**: define hooks that run only while that subagent is active
* **In `settings.json`**: define hooks that run in the main session when subagents start or stop

#### Hooks in subagent frontmatter

Define hooks directly in the subagent's markdown file. These hooks only run while that specific subagent is active and are cleaned up when it finishes.

<Note>
  Frontmatter hooks fire when the agent is spawned as a subagent through the Agent tool or an @-mention, and when the agent runs as the main session via [`--agent`](#invoke-subagents-explicitly) or the `agent` setting. In the main-session case they run alongside any hooks defined in [`settings.json`](/docs/en/hooks).
</Note>

All [hook events](/docs/en/hooks#hook-events) are supported. The most common events for subagents are:

| Event         | Matcher input | When it fires                                                       |
| :------------ | :------------ | :------------------------------------------------------------------ |
| `PreToolUse`  | Tool name     | Before the subagent uses a tool                                     |
| `PostToolUse` | Tool name     | After the subagent uses a tool                                      |
| `Stop`        | (none)        | When the subagent finishes (converted to `SubagentStop` at runtime) |

This example validates Bash commands with the `PreToolUse` hook and runs a linter after file edits with `PostToolUse`:

```yaml theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

When the agent is invoked as a subagent, `Stop` hooks in frontmatter are automatically converted to `SubagentStop` events.

#### Project-level hooks for subagent events

Configure hooks in `settings.json` that respond to subagent lifecycle events in the main session.

| Event           | Matcher input   | When it fires                    |
| :-------------- | :-------------- | :------------------------------- |
| `SubagentStart` | Agent type name | When a subagent begins execution |
| `SubagentStop`  | Agent type name | When a subagent completes        |

Both events support matchers to target specific agent types by name. The matcher value is the agent's frontmatter `name` for project-level and user-level subagents, or the plugin-scoped identifier such as `my-plugin:db-agent` for [plugin subagents](/docs/en/plugins). A scoped name contains a colon, so it is evaluated as an [unanchored regular expression](/docs/en/hooks#matcher-patterns); anchor it with `^` and `$`, as in `^my-plugin:db-agent$`, to match only that agent.

This example runs a setup script only when the `db-agent` subagent starts, and a cleanup script when any subagent stops:

```json theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

A hyphenated matcher like `db-agent` matches exactly on Claude Code v2.1.195 or later. On earlier versions it is evaluated as an unanchored regular expression and also fires for any agent type that contains it, such as `prod-db-agent`; anchor it as `^db-agent$` on those versions.

See [Hooks](/docs/en/hooks) for the complete hook configuration format.

## Work with subagents

### Understand automatic delegation

Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like "use proactively" in your subagent's description field.

### Invoke subagents explicitly

When automatic delegation isn't enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:

* **Natural language**: name the subagent in your prompt; Claude decides whether to delegate
* **@-mention**: guarantees the subagent runs for one task
* **Session-wide**: the whole session uses that subagent's system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting

For natural language, there's no special syntax. Name the subagent and Claude typically delegates:

```text wrap theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention the subagent.** Type `@` and pick the subagent from the typeahead, the same way you @-mention files. This ensures that specific subagent runs rather than leaving the choice to Claude:

```text wrap theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Your full message still goes to Claude, which writes the subagent's task prompt based on what you asked. The @-mention controls which subagent Claude invokes, not what prompt it receives.

Subagents provided by an enabled [plugin](/docs/en/plugins) appear in the typeahead under their scoped name, such as `my-plugin:code-reviewer` or `my-plugin:review:security` when the plugin [organizes agents into subfolders](#choose-the-subagent-scope). Named background subagents currently running in the session also appear in the typeahead, showing their status next to the name.

You can also type the mention manually without using the picker: `@agent-<name>` for local subagents, or `@agent-` followed by the scoped name for plugin subagents, for example `@agent-my-plugin:code-reviewer`. While you type this form the typeahead shows file matches rather than agents. The agent mention still resolves when you submit.

**Run the whole session as a subagent.** Pass [`--agent <name>`](/docs/en/cli-reference) to start a session where the main thread itself takes on that subagent's system prompt, tool restrictions, and model:

```bash theme={null}
claude --agent code-reviewer
```

The subagent's system prompt replaces the default Claude Code system prompt entirely, the same way [`--system-prompt`](/docs/en/cli-reference) does. `CLAUDE.md` files and project memory still load through the normal message flow. The agent name appears as `@<name>` in the startup header so you can confirm it's active.

This works with built-in and custom subagents, and the choice persists when you resume the session.

For a plugin-provided subagent, you can pass only the agent name and Claude Code finds it:

```bash theme={null}
claude --agent security-reviewer
```

If multiple plugins provide agents with the same name, pass the scoped name to disambiguate:

```bash theme={null}
claude --agent my-plugin:security-reviewer
```

If the plugin places the agent in a subfolder of its `agents/` directory, include the subfolder in the scoped name, for example `claude --agent my-plugin:review:security`.

To make it the default for every session in a project, set `agent` in `.claude/settings.json`:

```json theme={null}
{
  "agent": "code-reviewer"
}
```

The CLI flag overrides the setting if both are present.

### Run subagents in foreground or background

Subagents can run in the foreground or the background:

* **Foreground subagents** block the main conversation until complete. Permission prompts are passed through to you as they come up.
* **Background subagents** run concurrently while you continue working. {/* min-version: 2.1.186 */}As of v2.1.186, when a background subagent reaches a tool call that needs permission, the prompt surfaces in your main session and names the subagent that is asking. Approve to let the subagent continue, or press Esc to deny that one tool call without stopping the subagent. Before v2.1.186, background subagents auto-denied any tool call that would have prompted.

{/* min-version: 2.1.198 */}As of v2.1.198, subagents run in the background by default. Claude runs a subagent in the foreground when it needs the result before continuing. The default changes where a subagent runs, not what it's allowed to do: background subagents still surface every permission prompt in your main session. Before v2.1.198, Claude chose between foreground and background based on the task.

{/* min-version: 2.1.211 */}A background subagent's results reach Claude as a completion notification in a later turn. Claude waits for that notification before reporting the subagent's results, and if you ask about progress first, it reports that the subagent is still running. Before v2.1.211, Claude sometimes reported results for a background subagent that hadn't finished.

You can also steer this yourself:

* Ask Claude to run a task in the background or in the foreground
* Press **Ctrl+B** to background a running task

{/* min-version: 2.1.208 */}A background subagent that completes stays listed in [`/tasks`](/docs/en/commands), marked done and sorted below running work, until the session cleans up its task list. Its detail view stays open when the subagent finishes. Subagents that fail or that you stop leave the list. Before v2.1.208, a completed subagent left the list the moment it finished and its detail view closed.

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`. See [Environment variables](/docs/en/env-vars).

When [`CLAUDE_CODE_FORK_SUBAGENT`](#fork-the-current-conversation) is set to `1`, every subagent runs in the background and the frontmatter `background` field has no effect, because fork mode removes the `run_in_background` parameter from the `Agent` tool. `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` takes precedence over fork mode and keeps subagents in the foreground.

### API errors in subagents

{/* min-version: 2.1.199 */}As of v2.1.199, a subagent whose run ends on an API error, such as a usage limit or a repeated server error, reports that failure back to Claude instead of returning the error text as if it were the subagent's findings. What Claude receives depends on where the subagent ran:

* **Foreground**: if a rate limit, overload, or server error cuts off a subagent that already produced text output, the Agent tool returns that partial output with a note that the subagent was cut off and didn't finish its task. {/* min-version: 2.1.200 */}A subagent that produced nothing, or whose only output was tool calls, fails with [`Agent terminated early due to an API error`](/docs/en/errors#agent-terminated-early-due-to-an-api-error), followed by the error detail. In v2.1.199, a rate limit, overload, or server error that cut off the tool-calls-only shape returned an empty partial result containing only the cut-off note instead.
* **Background**: the subagent is marked failed, and the message Claude receives when it ends names the API error and includes the subagent's last output, so partial work isn't lost.

Once the underlying API error clears, ask Claude to retry the task or [resume the subagent](#resume-subagents).

### Subagent output scanning

Claude Code scans each subagent's final report before Claude reads it. A subagent may have read files, web pages, or command output you never reviewed, and text from those sources can carry instructions aimed at the main conversation. The scan never removes or rewords anything; it makes two kinds of change you may notice in a report:

* **Backslash insertion**: the scan inserts a backslash into text that imitates Claude Code's own output, such as a `<system-reminder>` tag or a line starting with `Human:` or `Assistant:`, so the imitation reads as ordinary text instead of being mistaken for part of the conversation.
* **Marker line**: the scan prepends a line starting with `[harness: subagent output matched instruction-shaped pattern(s):` when the report imitates a tag like `<system-reminder>` or mentions permission settings such as `bypassPermissions` or `--dangerously-skip-permissions`. Permission-setting mentions get the marker line, but the text itself stays as written.

The scan doesn't judge whether content is malicious, and it doesn't change what an instruction in a report can do: a tool call the report leads Claude to make still goes through the session's [permission checks](/docs/en/permissions) and [sandboxing](/docs/en/sandboxing). It isn't a substitute for [restricting what a subagent can reach](#control-subagent-capabilities).

<Note>
  Subagent output scanning requires Claude Code v2.1.210 or later.
</Note>

### Common patterns

#### Isolate high-volume operations

One of the most effective uses for subagents is isolating operations that produce large amounts of output. Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent's context while only the relevant summary returns to your main conversation.

```text wrap theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Run parallel research

For independent investigations, spawn multiple subagents to work simultaneously:

```text wrap theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Each subagent explores its area independently, then Claude synthesizes the findings. This works best when the research paths don't depend on each other.

<Warning>
  When subagents complete, their results return to your main conversation. Running many subagents that each return detailed results can consume significant context.
</Warning>

For tasks that need sustained parallelism or exceed your context window, [agent teams](/docs/en/agent-teams) give each worker its own independent context.

#### Chain subagents

For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.

```text wrap theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Choose between subagents and main conversation

Use the **main conversation** when:

* The task needs frequent back-and-forth or iterative refinement
* Multiple phases share significant context, such as planning, implementation, and testing
* You're making a quick, targeted change
* Latency matters. Subagents start fresh and may need time to gather context

Use **subagents** when:

* The task produces verbose output you don't need in your main context
* You want to enforce specific tool restrictions or permissions
* The work is self-contained and can return a summary

Consider [Skills](/docs/en/skills) instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context.

For a quick question about something already in your conversation, use [`/btw`](/docs/en/interactive-mode#side-questions-with-%2Fbtw) instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history.

### Spawn nested subagents

{/* min-version: 2.1.172 */}As of Claude Code v2.1.172, a subagent can spawn its own subagents. Use this when a delegated task itself splits into parallel subtasks, such as a reviewer subagent that dispatches a verifier per finding, so the intermediate output never reaches your main conversation. Only the top-level subagent's summary returns to you.

A nested subagent is configured the same way as a top-level one and resolves from the same [scopes](#choose-the-subagent-scope).

The subagent panel below the prompt input shows the full tree: each row displays a `(+N)` count of descendants, and {/* min-version: 2.1.193 */}as of v2.1.193, opening a row shows that subagent's siblings and direct children with a path back to `main`.

Depth is counted as the number of subagent levels below the main conversation, regardless of whether each level runs in the [foreground or background](#run-subagents-in-foreground-or-background). A subagent at depth five doesn't receive the Agent tool and can't spawn further. The limit is fixed and not configurable.

As of Claude Code v2.1.187, a background subagent's depth is fixed when it is first spawned, and [resuming](#resume-subagents) it later doesn't change that depth. For example, if your main conversation spawns subagent A, and A spawns a background subagent B at depth two, B is still at depth two when you resume it directly from the main conversation. Resuming a subagent from a shallower context doesn't let it spawn additional levels that the depth limit already prevented.

To prevent a specific subagent from spawning others, omit `Agent` from its [`tools`](#available-tools) list or add it to `disallowedTools`.

A [fork](#fork-the-current-conversation) still can't spawn another fork. It can spawn other subagent types, and those count toward the depth limit.

### Session subagent limit

By default, Claude can spawn at most 200 subagents per session. To raise the limit, set [`CLAUDE_CODE_MAX_SUBAGENTS_PER_SESSION`](/docs/en/env-vars) to any positive whole number; there is no upper bound, but the limit can't be turned off. Requires Claude Code v2.1.212 or later.

Every subagent Claude spawns with the Agent tool counts toward the limit: nested subagents, [forks](#fork-the-current-conversation), and background subagents, including subagents that a [workflow](/docs/en/workflows)'s agents spawn with the Agent tool. An in-session fork you start yourself with `/subtask` counts too: it spends the same budget, though the limit blocks only subagents Claude spawns with the Agent tool, so your own `/subtask` still starts after Claude reaches the limit. A session you create with `/fork` doesn't count; it runs as a separate background session with its own budget. Before v2.1.212, the in-session fork was named `/fork`. Agents a workflow script spawns with `agent()` don't count; workflows have their own per-run limit. A finished subagent still counts.

When Claude reaches the limit, the Agent tool fails with `Subagent spawn limit reached`, and the error tells Claude to complete the remaining work directly with its own tools.

Run [`/clear`](/docs/en/commands#all-commands) to reset the count and start a new conversation with the full budget. If work that can still spawn subagents survives the clear, such as a running workflow, the count carries over instead.

This limit is separate from the [depth limit](#spawn-nested-subagents), which caps how deeply subagents nest.

### Manage subagent context

#### What loads at startup

Each subagent starts with a fresh, isolated context window. It doesn't see your conversation history, the skills you've already invoked, or the files Claude has already read. Claude composes a delegation message that summarizes the task, and the subagent works from there. The exception is a [fork](#fork-the-current-conversation), which inherits the parent conversation instead of starting fresh.

A non-fork subagent's initial context contains:

* **System prompt**: the agent's own prompt plus environment details that Claude Code appends, not the full Claude Code system prompt. Custom subagents define theirs in the [markdown body](#write-subagent-files) or `prompt` field. Built-in agents have predefined prompts.
* **Task message**: the delegation prompt Claude writes when it hands off the work.
* **CLAUDE.md files**: every level of the [CLAUDE.md hierarchy](/docs/en/memory#how-claude-md-files-load) the main conversation loads, including `~/.claude/CLAUDE.md`, project rules, `CLAUDE.local.md`, and managed policy files. The built-in Explore and Plan agents skip this.
* **Git status**: a snapshot taken at the start of the parent session. Absent when the working directory isn't a Git repository or when [`includeGitInstructions`](/docs/en/settings#available-settings) is `false`. Explore and Plan skip it regardless.
* **Preloaded skills**: full content of any skill named in the agent's [`skills` field](#preload-skills-into-subagents). Built-in agents don't preload skills.
* **Sibling roster**: a system reminder listing `main` and every other named agent in the session, each a valid `to` value for [`SendMessage`](#resume-subagents). {/* min-version: 2.1.206 */}Requires Claude Code v2.1.206 or later. The roster appears only when the subagent's tools include `SendMessage` and at least one other agent has a name, whether Claude named it when spawning it or it runs as an [agent team](/docs/en/agent-teams) teammate. It is a snapshot taken when the subagent starts, so agents named later don't appear.

Explore and Plan are the only subagents that omit CLAUDE.md and git status. There is no frontmatter field or per-agent setting to change which agents skip them.

The main conversation reads Explore and Plan results with full CLAUDE.md context, so most rules don't need to reach the subagent itself. If a rule must, such as "ignore the `vendor/` directory," restate it in the prompt you give Claude when delegating.

Some main-conversation state never reaches a non-fork subagent:

* **Output style**: a subagent runs its own system prompt, so your [output style](/docs/en/output-styles) doesn't shape its responses, except in a [fork](#fork-the-current-conversation).
* **Auto memory**: the main conversation's [auto memory](/docs/en/memory#auto-memory) isn't loaded. To give a subagent persistent memory of its own, use the [`memory` field](#enable-persistent-memory).
* **Context window size**: a subagent's context window is sized by its own model, not the parent's. Delegating to a model with a smaller window gives that subagent the smaller window.

#### Resume subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent's work instead of starting over, ask Claude to resume it.

Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh.

When a subagent completes, Claude receives its agent ID. The built-in Explore and Plan agents are one-shot and return no agent ID, so they can't be resumed; use `general-purpose` or a custom subagent when you need to continue the work.

Claude uses the `SendMessage` tool with the agent's ID or name as the `to` field to resume it. `SendMessage` doesn't require [agent teams](/docs/en/agent-teams) to be enabled; only structured team-protocol messages such as `shutdown_request` and `plan_approval_response` do.

To resume a subagent, ask Claude to continue the previous work:

```text wrap theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

A completed subagent that receives a `SendMessage` auto-resumes in the background without a new `Agent` invocation. The same applies to a subagent that Claude stopped with the `TaskStop` tool.

{/* min-version: 2.1.191 */}As of v2.1.191, a subagent you stopped yourself, with `x` in `/tasks` or an SDK `stop_task` request, doesn't auto-resume. The `SendMessage` call returns a refusal telling Claude the agent was cancelled. Type into that subagent's transcript in the subagent panel to resume it yourself, which clears the stop so later `SendMessage` calls can auto-resume it again.

Resuming starts a new run of the agent under the same ID, so a subagent that had already failed or completed shows as running again in the task list and in the Agent SDK's task events. Before v2.1.205, it kept showing its earlier failed or completed status while the resumed run was working.

{/* min-version: 2.1.199 */}As of v2.1.199, `SendMessage` checks that a name still refers to the same agent it reached earlier in the conversation. If a newer agent has taken the name, such as a re-spawned background agent that reused it, Claude Code refuses the send rather than delivering it to the wrong agent, and the error reports which agent the name now reaches so Claude can retarget. To reach the earlier agent while it's still running, Claude addresses it by the agent ID it received when it spawned that agent. The check is scoped to the current conversation and resets on `/clear`.

{/* min-version: 2.1.198 */}As of v2.1.198, a subagent treats messages from the agent that launched it as normal task direction, including mid-task course corrections, and acts on them within its own permission settings. Two limits still hold regardless of who sent the message: no message from any agent counts as your approval for a pending permission prompt, and no agent message can change a subagent's permission settings, `CLAUDE.md`, or configuration. Only the permission system or your own messages can grant approval.

You can also ask Claude for the agent ID if you want to reference it explicitly, or find IDs in the transcript files at `~/.claude/projects/{project}/{sessionId}/subagents/`. Each transcript is stored as `agent-{agentId}.jsonl`.

Subagent transcripts persist independently of the main conversation:

* **Main conversation compaction**: when the main conversation compacts, subagent transcripts are unaffected. They're stored in separate files.
* **Session persistence**: subagent transcripts persist within their session. You can [resume a subagent](#resume-subagents) after restarting Claude Code by resuming the same session.
* **Automatic cleanup**: transcripts are cleaned up based on the `cleanupPeriodDays` setting, which defaults to 30 days.

#### Auto-compaction

Subagents support automatic compaction using the same logic as the main conversation. Compaction triggers under the same conditions, and `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` applies to subagents as well. See [environment variables](/docs/en/env-vars) for when the override takes effect.

Compaction events are logged in subagent transcript files:

```json theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

The `preTokens` value shows how many tokens were used before compaction occurred.

## Fork the current conversation

<Note>
  {/* min-version: 2.1.212 */}Run a forked subagent with `/subtask`, which requires Claude Code v2.1.212 or later. When [agent view is turned off](/docs/en/agent-view#turn-off-agent-view), `/subtask` isn't available and `/fork` starts the forked subagent instead; otherwise `/fork` copies the whole session into a new [background session](/docs/en/agent-view#from-inside-a-session).

  {/* min-version: 2.1.161 */}Before v2.1.212, the forked-subagent command was `/fork`. It was enabled by default on v2.1.161 or later; on v2.1.117 through v2.1.160 it required setting the [`CLAUDE_CODE_FORK_SUBAGENT`](/docs/en/env-vars) environment variable to `1`, unless a server-side rollout enabled it.

  Letting Claude itself spawn forks is experimental and may change in future releases. This capability may also be enabled in interactive sessions as part of a staged rollout.
</Note>

A fork is a subagent that inherits the entire conversation so far instead of starting fresh. This drops the input isolation that subagents otherwise provide: a fork sees the same system prompt, tools, model, and message history as the main session, so you can hand it a side task without re-explaining the situation. The fork's own tool calls still stay out of your conversation and only its final result comes back, so your main context window stays clean. Use a fork when a named subagent would need too much background to be useful, or when you want to try several approaches in parallel from the same starting point.

To control fork mode regardless of the staged rollout, set [`CLAUDE_CODE_FORK_SUBAGENT`](/docs/en/env-vars) to `1` to enable it explicitly or to `0` to disable it. The variable is honored in interactive mode and via the SDK or `claude -p`.

Enabling fork mode changes Claude Code in two ways:

* Claude can spawn a fork by requesting the `fork` subagent type explicitly. When Claude doesn't request a type, it still gets the [general-purpose](#built-in-subagents) subagent, and named subagents such as Explore still spawn as before.
* Every subagent runs in the [background](#run-subagents-in-foreground-or-background), whether it is a fork or a named subagent. Set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` to `1` to keep subagents synchronous.

You can start a fork yourself with `/subtask` followed by a task, with or without the variable set. On v2.1.161 through v2.1.211 the command is `/fork`. Claude Code names the fork from the first words of the task. The following example forks the conversation to draft test cases while you continue with the implementation in the main session:

```text wrap theme={null}
/subtask draft unit tests for the parser changes so far
```

The fork appears in a panel below your prompt and runs in the background while you keep working. When it finishes, its result arrives as a message in your main conversation. The next section covers the panel controls for watching and steering forks while they run.

### Observe and steer running forks

Running forks appear in a panel below the prompt input, with one row for the main session and one for each fork. Use these keys to interact with the panel:

| Key       | Action                                                             |
| :-------- | :----------------------------------------------------------------- |
| `↑` / `↓` | Move between rows                                                  |
| `Enter`   | Open the selected fork's transcript and send it follow-up messages |
| `x`       | Dismiss a finished fork or stop a running one                      |
| `Esc`     | Return focus to the prompt input                                   |

With a fork's or subagent's transcript open, follow-up messages and [skills](/docs/en/skills) go to that agent, but built-in commands still run in your main conversation. {/* min-version: 2.1.199 */}As of v2.1.199, typing `/model` or `/fast` in that view shows a notice that it changes the main conversation's model or fast mode, not the viewed agent's, instead of running it silently.

### How forks differ from named subagents

A fork inherits everything the main session has at the moment it spawns. A named subagent starts from its own definition.

|                         | Fork                             | Named subagent                                                                                                    |
| :---------------------- | :------------------------------- | :---------------------------------------------------------------------------------------------------------------- |
| Context                 | Full conversation history        | Fresh context with the prompt you pass                                                                            |
| System prompt and tools | Same as main session             | From the subagent's [definition file](#write-subagent-files)                                                      |
| Model                   | Same as main session             | From the subagent's `model` field                                                                                 |
| Permissions             | Prompts surface in your terminal | [Prompts surface in your main session](#run-subagents-in-foreground-or-background) when running in the background |
| Prompt cache            | Shared with main session         | Separate cache                                                                                                    |

Because a fork's system prompt and tool definitions are identical to the parent, its first request reuses the parent's [prompt cache](/docs/en/prompt-caching#subagents-and-the-cache). This makes forking cheaper than spawning a fresh subagent for tasks that need the same context.

When Claude spawns a fork through the Agent tool, it can pass `isolation: "worktree"` so the fork's file edits are written to a separate git worktree instead of your checkout.

### Limitations

Setting `CLAUDE_CODE_FORK_SUBAGENT=1` enables fork mode in interactive sessions, [non-interactive mode](/docs/en/headless), and the Agent SDK; setting it to `0` disables fork mode everywhere, including any server-side rollout. A fork can't spawn further forks.

## Example subagents

These examples demonstrate effective patterns for building subagents. Use them as starting points, or generate a customized version with Claude.

<Tip>
  **Best practices:**

  * **Design focused subagents:** each subagent should excel at one specific task
  * **Write detailed descriptions:** Claude uses the description to decide when to delegate
  * **Limit tool access:** grant only necessary permissions for security and focus
  * **Check into version control:** share project subagents with your team
</Tip>

### Code reviewer

A read-only subagent that reviews code without modifying it. This example shows how to design a focused subagent with limited tool access that excludes Edit and Write, and a detailed prompt that specifies exactly what to look for and how to format output.

```markdown theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

A subagent that can both analyze and fix issues. Unlike the code reviewer, this one includes Edit because fixing bugs requires modifying code. The prompt provides a clear workflow from diagnosis to verification.

```markdown theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data scientist

A domain-specific subagent for data analysis work. This example shows how to create subagents for specialized workflows outside of typical coding tasks. It explicitly sets `model: sonnet` for more capable analysis.

```markdown theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Database query validator

A subagent that allows Bash access but validates commands to permit only read-only SQL queries. This example shows how to use `PreToolUse` hooks for conditional validation when you need finer control than the `tools` field provides.

```markdown theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [passes hook input as JSON](/docs/en/hooks#pretooluse-input) via stdin to hook commands. The validation script reads this JSON, extracts the command being executed, and checks it against a list of SQL write operations. If a write operation is detected, the script [exits with code 2](/docs/en/hooks#exit-code-2-behavior-per-event) to block execution and returns an error message to Claude via stderr.

Create the validation script anywhere in your project. The path must match the `command` field in your hook configuration:

```bash theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

On macOS and Linux, make the script executable:

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

On Windows, write the validation script in PowerShell and add `shell: powershell` to the hook entry. See [running hooks in PowerShell](/docs/en/hooks#windows-powershell-tool).

The hook receives JSON via stdin with the Bash command in `tool_input.command`. Exit code 2 blocks the operation and feeds the error message back to Claude. See [Hooks](/docs/en/hooks#exit-code-output) for details on exit codes and [Hook input](/docs/en/hooks#pretooluse-input) for the complete input schema.

## Next steps

Now that you understand subagents, explore these related features:

* [Distribute subagents with plugins](/docs/en/plugins) to share subagents across teams or projects
* [Run Claude Code programmatically](/docs/en/headless) with the Agent SDK for CI/CD and automation
* [Use MCP servers](/docs/en/mcp) to give subagents access to external tools and data
