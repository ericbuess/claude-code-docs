> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Create custom subagents

> Create and use specialized AI subagents in Claude Code for task-specific workflows and improved context management.

Subagents are specialized AI assistants that handle specific types of tasks. Use one when a side task would flood your main conversation with search results, logs, or file contents you won't reference again: the subagent does that work in its own context and returns only the summary. Define a custom subagent when you keep spawning the same kind of worker with the same instructions.

Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent, which works independently and returns results. To see the context savings in practice, the [context window visualization](/en/context-window) walks through a session where a subagent handles research in its own separate window.

<Note>
  If you need multiple agents working in parallel and communicating with each other, see [agent teams](/en/agent-teams) instead. Subagents work within a single session; agent teams coordinate across separate sessions.
</Note>

Subagents help you:

* **Preserve context** by keeping exploration and implementation out of your main conversation
* **Enforce constraints** by limiting which tools a subagent can use
* **Reuse configurations** across projects with user-level subagents
* **Specialize behavior** with focused system prompts for specific domains
* **Control costs** by routing tasks to faster, cheaper models like Haiku

Claude uses each subagent's description to decide when to delegate tasks. When you create a subagent, write a clear description so Claude knows when to use it.

Claude Code includes several built-in subagents like **Explore**, **Plan**, and **general-purpose**. You can also create custom subagents to handle specific tasks. This page covers:

* [Built-in subagents](#built-in-subagents)
* [How to create your own](#quickstart-create-your-first-subagent)
* [Full configuration options](#configure-subagents)
* [Patterns for working with subagents](#work-with-subagents)
* [Forked subagents](#fork-the-current-conversation)
* [Example subagents](#example-subagents)

## Built-in subagents

Claude Code includes built-in subagents that Claude automatically uses when appropriate. Each inherits the parent conversation's permissions with additional tool restrictions.

<Tabs>
  <Tab title="Explore">
    A fast, read-only agent optimized for searching and analyzing codebases.

    * **Model**: Haiku (fast, low-latency)
    * **Tools**: Read-only tools (denied access to Write and Edit tools)
    * **Purpose**: File discovery, code search, codebase exploration

    Claude delegates to Explore when it needs to search or understand a codebase without making changes. This keeps exploration results out of your main conversation context.

    When invoking Explore, Claude specifies a thoroughness level: **quick** for targeted lookups, **medium** for balanced exploration, or **very thorough** for comprehensive analysis.
  </Tab>

  <Tab title="Plan">
    A research agent used during [plan mode](/en/permission-modes#analyze-before-you-edit-with-plan-mode) to gather context before presenting a plan.

    * **Model**: Inherits from main conversation
    * **Tools**: Read-only tools (denied access to Write and Edit tools)
    * **Purpose**: Codebase research for planning

    When you're in plan mode and Claude needs to understand your codebase, it delegates research to the Plan subagent. This prevents infinite nesting (subagents cannot spawn other subagents) while still gathering necessary context.
  </Tab>

  <Tab title="General-purpose">
    A capable agent for complex, multi-step tasks that require both exploration and action.

    * **Model**: Inherits from main conversation
    * **Tools**: All tools
    * **Purpose**: Complex research, multi-step operations, code modifications

    Claude delegates to general-purpose when the task requires both exploration and modification, complex reasoning to interpret results, or multiple dependent steps.
  </Tab>

  <Tab title="Other">
    Claude Code includes additional helper agents for specific tasks. These are typically invoked automatically, so you don't need to use them directly.

    | Agent             | Model  | When Claude uses it                                      |
    | :---------------- | :----- | :------------------------------------------------------- |
    | statusline-setup  | Sonnet | When you run `/statusline` to configure your status line |
    | Claude Code Guide | Haiku  | When you ask questions about Claude Code features        |
  </Tab>
</Tabs>

Beyond these built-in subagents, you can create your own with custom prompts, tool restrictions, permission modes, hooks, and skills. The following sections show how to get started and customize subagents.

## Quickstart: create your first subagent

Subagents are defined in Markdown files with YAML frontmatter. You can [create them manually](#write-subagent-files) or use the `/agents` command.

This walkthrough guides you through creating a user-level subagent with the `/agents` command. The subagent reviews code and suggests improvements for the codebase.

<Steps>
  <Step title="Open the subagents interface">
    In Claude Code, run:

    ```text theme={null}
    /agents
    ```
  </Step>

  <Step title="Choose a location">
    Switch to the **Library** tab, select **Create new agent**, then choose **Personal**. This saves the subagent to `~/.claude/agents/` so it's available in all your projects.
  </Step>

  <Step title="Generate with Claude">
    Select **Generate with Claude**. When prompted, describe the subagent:

    ```text theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude generates the identifier, description, and system prompt for you.
  </Step>

  <Step title="Select tools">
    For a read-only reviewer, deselect everything except **Read-only tools**. If you keep all tools selected, the subagent inherits all tools available to the main conversation.
  </Step>

  <Step title="Select model">
    Choose which model the subagent uses. For this example agent, select **Sonnet**, which balances capability and speed for analyzing code patterns.
  </Step>

  <Step title="Choose a color">
    Pick a background color for the subagent. This helps you identify which subagent is running in the UI.
  </Step>

  <Step title="Configure memory">
    Select **User scope** to give the subagent a [persistent memory directory](#enable-persistent-memory) at `~/.claude/agent-memory/`. The subagent uses this to accumulate insights across conversations, such as codebase patterns and recurring issues. Select **None** if you don't want the subagent to persist learnings.
  </Step>

  <Step title="Save and try it out">
    Review the configuration summary. Press `s` or `Enter` to save, or press `e` to save and edit the file in your editor. The subagent is available immediately. Try it:

    ```text theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude delegates to your new subagent, which scans the codebase and returns improvement suggestions.
  </Step>
</Steps>

You now have a subagent you can use in any project on your machine to analyze codebases and suggest improvements.

You can also create subagents manually as Markdown files, define them via CLI flags, or distribute them through plugins. The following sections cover all configuration options.

## Configure subagents

### Use the /agents command

The `/agents` command opens a tabbed interface for managing subagents. The **Running** tab shows live subagents and lets you open or stop them. The **Library** tab lets you:

* View all available subagents (built-in, user, project, and plugin)
* Create new subagents with guided setup or Claude generation
* Edit existing subagent configuration and tool access
* Delete custom subagents
* See which subagents are active when duplicates exist

This is the recommended way to create and manage subagents. For manual creation or automation, you can also add subagent files directly.

To list all configured subagents from the command line without starting an interactive session, run `claude agents`. This shows agents grouped by source and indicates which are overridden by higher-priority definitions.

### Choose the subagent scope

Subagents are Markdown files with YAML frontmatter. Store them in different locations depending on scope. When multiple subagents share the same name, the higher-priority location wins.

| Location                     | Scope                   | Priority    | How to create                                 |
| :--------------------------- | :---------------------- | :---------- | :-------------------------------------------- |
| Managed settings             | Organization-wide       | 1 (highest) | Deployed via [managed settings](/en/settings) |
| `--agents` CLI flag          | Current session         | 2           | Pass JSON when launching Claude Code          |
| `.claude/agents/`            | Current project         | 3           | Interactive or manual                         |
| `~/.claude/agents/`          | All your projects       | 4           | Interactive or manual                         |
| Plugin's `agents/` directory | Where plugin is enabled | 5 (lowest)  | Installed with [plugins](/en/plugins)         |

**Project subagents** (`.claude/agents/`) are ideal for subagents specific to a codebase. Check them into version control so your team can use and improve them collaboratively.

Project subagents are discovered by walking up from the current working directory. Directories added with `--add-dir` [grant file access only](/en/permissions#additional-directories-grant-file-access-not-configuration) and are not scanned for subagents. To share subagents across projects, use `~/.claude/agents/` or a [plugin](/en/plugins).

**User subagents** (`~/.claude/agents/`) are personal subagents available in all your projects.

**CLI-defined subagents** are passed as JSON when launching Claude Code. They exist only for that session and aren't saved to disk, making them useful for quick testing or automation scripts. You can define multiple subagents in a single `--agents` call:

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

The `--agents` flag accepts JSON with the same [frontmatter](#supported-frontmatter-fields) fields as file-based subagents: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation`, and `color`. Use `prompt` for the system prompt, equivalent to the markdown body in file-based subagents.

**Managed subagents** are deployed by organization administrators. Place markdown files in `.claude/agents/` inside the [managed settings directory](/en/settings#settings-files), using the same frontmatter format as project and user subagents. Managed definitions take precedence over project and user subagents with the same name.

**Plugin subagents** come from [plugins](/en/plugins) you've installed. They appear in `/agents` alongside your custom subagents. See the [plugin components reference](/en/plugins-reference#agents) for details on creating plugin subagents.

<Note>
  For security reasons, plugin subagents do not support the `hooks`, `mcpServers`, or `permissionMode` frontmatter fields. These fields are ignored when loading agents from a plugin. If you need them, copy the agent file into `.claude/agents/` or `~/.claude/agents/`. You can also add rules to [`permissions.allow`](/en/settings#permission-settings) in `settings.json` or `settings.local.json`, but these rules apply to the entire session, not just the plugin subagent.
</Note>

Subagent definitions from any of these scopes are also available to [agent teams](/en/agent-teams#use-subagent-definitions-for-teammates): when spawning a teammate, you can reference a subagent type and the teammate uses its `tools` and `model`, with the definition's body appended to the teammate's system prompt as additional instructions. See [agent teams](/en/agent-teams#use-subagent-definitions-for-teammates) for which frontmatter fields apply on that path.

### Write subagent files

Subagent files use YAML frontmatter for configuration, followed by the system prompt in Markdown:

<Note>
  Subagents are loaded at session start. If you create a subagent by manually adding a file, restart your session or use `/agents` to load it immediately.
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

The frontmatter defines the subagent's metadata and configuration. The body becomes the system prompt that guides the subagent's behavior. Subagents receive only this system prompt (plus basic environment details like working directory), not the full Claude Code system prompt.

A subagent starts in the main conversation's current working directory. Within a subagent, `cd` commands do not persist between Bash or PowerShell tool calls and do not affect the main conversation's working directory. To give the subagent an isolated copy of the repository instead, set [`isolation: worktree`](#supported-frontmatter-fields).

#### Supported frontmatter fields

The following fields can be used in the YAML frontmatter. Only `name` and `description` are required.

| Field             | Required | Description                                                                                                                                                                                                                                                                                                                              |
| :---------------- | :------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | Unique identifier using lowercase letters and hyphens                                                                                                                                                                                                                                                                                    |
| `description`     | Yes      | When Claude should delegate to this subagent                                                                                                                                                                                                                                                                                             |
| `tools`           | No       | [Tools](#available-tools) the subagent can use. Inherits all tools if omitted                                                                                                                                                                                                                                                            |
| `disallowedTools` | No       | Tools to deny, removed from inherited or specified list                                                                                                                                                                                                                                                                                  |
| `model`           | No       | [Model](#choose-a-model) to use: `sonnet`, `opus`, `haiku`, a full model ID (for example, `claude-opus-4-7`), or `inherit`. Defaults to `inherit`                                                                                                                                                                                        |
| `permissionMode`  | No       | [Permission mode](#permission-modes): `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, or `plan`. Ignored for [plugin subagents](#choose-the-subagent-scope)                                                                                                                                                            |
| `maxTurns`        | No       | Maximum number of agentic turns before the subagent stops                                                                                                                                                                                                                                                                                |
| `skills`          | No       | [Skills](/en/skills) to load into the subagent's context at startup. The full skill content is injected, not just made available for invocation. Subagents don't inherit skills from the parent conversation                                                                                                                             |
| `mcpServers`      | No       | [MCP servers](/en/mcp) available to this subagent. Each entry is either a server name referencing an already-configured server (e.g., `"slack"`) or an inline definition with the server name as key and a full [MCP server config](/en/mcp#installing-mcp-servers) as value. Ignored for [plugin subagents](#choose-the-subagent-scope) |
| `hooks`           | No       | [Lifecycle hooks](#define-hooks-for-subagents) scoped to this subagent. Ignored for [plugin subagents](#choose-the-subagent-scope)                                                                                                                                                                                                       |
| `memory`          | No       | [Persistent memory scope](#enable-persistent-memory): `user`, `project`, or `local`. Enables cross-session learning                                                                                                                                                                                                                      |
| `background`      | No       | Set to `true` to always run this subagent as a [background task](#run-subagents-in-foreground-or-background). Default: `false`                                                                                                                                                                                                           |
| `effort`          | No       | Effort level when this subagent is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`; available levels depend on the model                                                                                                                                    |
| `isolation`       | No       | Set to `worktree` to run the subagent in a temporary [git worktree](/en/worktrees), giving it an isolated copy of the repository. The worktree is automatically cleaned up if the subagent makes no changes                                                                                                                              |
| `color`           | No       | Display color for the subagent in the task list and transcript. Accepts `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, or `cyan`                                                                                                                                                                                          |
| `initialPrompt`   | No       | Auto-submitted as the first user turn when this agent runs as the main session agent (via `--agent` or the `agent` setting). [Commands](/en/commands) and [skills](/en/skills) are processed. Prepended to any user-provided prompt                                                                                                      |

### Choose a model

The `model` field controls which [AI model](/en/model-config) the subagent uses:

* **Model alias**: Use one of the available aliases: `sonnet`, `opus`, or `haiku`
* **Full model ID**: Use a full model ID such as `claude-opus-4-7` or `claude-sonnet-4-6`. Accepts the same values as the `--model` flag
* **inherit**: Use the same model as the main conversation
* **Omitted**: If not specified, defaults to `inherit` (uses the same model as the main conversation)

When Claude invokes a subagent, it can also pass a `model` parameter for that specific invocation. Claude Code resolves the subagent's model in this order:

1. The [`CLAUDE_CODE_SUBAGENT_MODEL`](/en/model-config#environment-variables) environment variable, if set
2. The per-invocation `model` parameter
3. The subagent definition's `model` frontmatter
4. The main conversation's model

### Control subagent capabilities

You can control what subagents can do through tool access, permission modes, and conditional rules.

#### Available tools

Subagents can use any of Claude Code's [internal tools](/en/tools-reference). By default, subagents inherit all tools from the main conversation, including MCP tools.

To restrict tools, use either the `tools` field (allowlist) or the `disallowedTools` field (denylist). This example uses `tools` to exclusively allow Read, Grep, Glob, and Bash. The subagent can't edit files, write files, or use any MCP tools:

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

If `Agent` is omitted from the `tools` list entirely, the agent cannot spawn any subagents. This restriction only applies to agents running as the main thread with `claude --agent`. Subagents cannot spawn other subagents, so `Agent(agent_type)` has no effect in subagent definitions.

#### Scope MCP servers to a subagent

Use the `mcpServers` field to give a subagent access to [MCP](/en/mcp) servers that aren't available in the main conversation. Inline servers defined here are connected when the subagent starts and disconnected when it finishes. String references share the parent session's connection.

<Note>
  The `mcpServers` field applies in both contexts where an agent file can run:

  * As a subagent, spawned through the Agent tool or an @-mention
  * As the main session, launched with [`--agent`](#invoke-subagents-explicitly) or the `agent` setting

  When the agent is the main session, inline server definitions connect at startup alongside servers from [`.mcp.json`](/en/mcp) and settings files.
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

Inline definitions use the same schema as `.mcp.json` server entries (`stdio`, `http`, `sse`, `ws`), keyed by the server name.

To keep an MCP server out of the main conversation entirely and avoid its tool descriptions consuming context there, define it inline here rather than in `.mcp.json`. The subagent gets the tools; the parent conversation does not.

#### Permission modes

The `permissionMode` field controls how the subagent handles permission prompts. Subagents inherit the permission context from the main conversation and can override the mode, except when the parent mode takes precedence as described below.

| Mode                | Behavior                                                                                                                                    |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `default`           | Standard permission checking with prompts                                                                                                   |
| `acceptEdits`       | Auto-accept file edits and common filesystem commands for paths in the working directory or `additionalDirectories`                         |
| `auto`              | [Auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode): a background classifier reviews commands and protected-directory writes |
| `dontAsk`           | Auto-deny permission prompts (explicitly allowed tools still work)                                                                          |
| `bypassPermissions` | Skip permission prompts                                                                                                                     |
| `plan`              | Plan mode (read-only exploration)                                                                                                           |

<Warning>
  Use `bypassPermissions` with caution. It skips all permission prompts, allowing the subagent to execute operations without approval, including writes to `.git`, `.claude`, `.vscode`, `.idea`, and `.husky`. Root and home directory removals such as `rm -rf /` still prompt as a circuit breaker. See [permission modes](/en/permission-modes#skip-all-checks-with-bypasspermissions-mode) for details.
</Warning>

If the parent uses `bypassPermissions` or `acceptEdits`, this takes precedence and cannot be overridden. If the parent uses [auto mode](/en/permission-modes#eliminate-prompts-with-auto-mode), the subagent inherits auto mode and any `permissionMode` in its frontmatter is ignored: the classifier evaluates the subagent's tool calls with the same block and allow rules as the parent session.

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

The full content of each skill is injected into the subagent's context, not just made available for invocation. Subagents don't inherit skills from the parent conversation; you must list them explicitly.

You cannot preload skills that set [`disable-model-invocation: true`](/en/skills#control-who-invokes-a-skill), since preloading draws from the same set of skills Claude can invoke. If a listed skill is missing or disabled, Claude Code skips it and logs a warning to the debug log.

<Note>
  This is the inverse of [running a skill in a subagent](/en/skills#run-skills-in-a-subagent). With `skills` in a subagent, the subagent controls the system prompt and loads skill content. With `context: fork` in a skill, the skill content is injected into the agent you specify. Both use the same underlying system.
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

| Scope     | Location                                      | Use when                                                                                    |
| :-------- | :-------------------------------------------- | :------------------------------------------------------------------------------------------ |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | the subagent should remember learnings across all projects                                  |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | the subagent's knowledge is project-specific and shareable via version control              |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | the subagent's knowledge is project-specific but should not be checked into version control |

When memory is enabled:

* The subagent's system prompt includes instructions for reading and writing to the memory directory.
* The subagent's system prompt also includes the first 200 lines or 25KB of `MEMORY.md` in the memory directory, whichever comes first, with instructions to curate `MEMORY.md` if it exceeds that limit.
* Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files.

##### Persistent memory tips

* `project` is the recommended default scope. It makes subagent knowledge shareable via version control. Use `user` when the subagent's knowledge is broadly applicable across projects, or `local` when the knowledge should not be checked into version control.
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

Claude Code [passes hook input as JSON](/en/hooks#pretooluse-input) via stdin to hook commands. The validation script reads this JSON, extracts the Bash command, and [exits with code 2](/en/hooks#exit-code-2-behavior-per-event) to block write operations:

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

See [Hook input](/en/hooks#pretooluse-input) for the complete input schema and [exit codes](/en/hooks#exit-code-output) for how exit codes affect behavior.

#### Disable specific subagents

You can prevent Claude from using specific subagents by adding them to the `deny` array in your [settings](/en/settings#permission-settings). Use the format `Agent(subagent-name)` where `subagent-name` matches the subagent's name field.

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

See [Permissions documentation](/en/permissions#tool-specific-permission-rules) for more details on permission rules.

### Define hooks for subagents

Subagents can define [hooks](/en/hooks) that run during the subagent's lifecycle. There are two ways to configure hooks:

1. **In the subagent's frontmatter**: Define hooks that run only while that subagent is active
2. **In `settings.json`**: Define hooks that run in the main session when subagents start or stop

#### Hooks in subagent frontmatter

Define hooks directly in the subagent's markdown file. These hooks only run while that specific subagent is active and are cleaned up when it finishes.

<Note>
  Frontmatter hooks fire when the agent is spawned as a subagent through the Agent tool or an @-mention, and when the agent runs as the main session via [`--agent`](#invoke-subagents-explicitly) or the `agent` setting. In the main-session case they run alongside any hooks defined in [`settings.json`](/en/hooks).
</Note>

All [hook events](/en/hooks#hook-events) are supported. The most common events for subagents are:

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

Both events support matchers to target specific agent types by name. This example runs a setup script only when the `db-agent` subagent starts, and a cleanup script when any subagent stops:

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

See [Hooks](/en/hooks) for the complete hook configuration format.

## Work with subagents

### Understand automatic delegation

Claude automatically delegates tasks based on the task description in your request, the `description` field in subagent configurations, and current context. To encourage proactive delegation, include phrases like "use proactively" in your subagent's description field.

### Invoke subagents explicitly

When automatic delegation isn't enough, you can request a subagent yourself. Three patterns escalate from a one-off suggestion to a session-wide default:

* **Natural language**: name the subagent in your prompt; Claude decides whether to delegate
* **@-mention**: guarantees the subagent runs for one task
* **Session-wide**: the whole session uses that subagent's system prompt, tool restrictions, and model via the `--agent` flag or the `agent` setting

For natural language, there's no special syntax. Name the subagent and Claude typically delegates:

```text theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention the subagent.** Type `@` and pick the subagent from the typeahead, the same way you @-mention files. This ensures that specific subagent runs rather than leaving the choice to Claude:

```text theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Your full message still goes to Claude, which writes the subagent's task prompt based on what you asked. The @-mention controls which subagent Claude invokes, not what prompt it receives.

Subagents provided by an enabled [plugin](/en/plugins) appear in the typeahead as `<plugin-name>:<agent-name>`. Named background subagents currently running in the session also appear in the typeahead, showing their status next to the name. You can also type the mention manually without using the picker: `@agent-<name>` for local subagents, or `@agent-<plugin-name>:<agent-name>` for plugin subagents.

**Run the whole session as a subagent.** Pass [`--agent <name>`](/en/cli-reference) to start a session where the main thread itself takes on that subagent's system prompt, tool restrictions, and model:

```bash theme={null}
claude --agent code-reviewer
```

The subagent's system prompt replaces the default Claude Code system prompt entirely, the same way [`--system-prompt`](/en/cli-reference) does. `CLAUDE.md` files and project memory still load through the normal message flow. The agent name appears as `@<name>` in the startup header so you can confirm it's active.

This works with built-in and custom subagents, and the choice persists when you resume the session.

For a plugin-provided subagent, pass the scoped name: `claude --agent <plugin-name>:<agent-name>`.

To make it the default for every session in a project, set `agent` in `.claude/settings.json`:

```json theme={null}
{
  "agent": "code-reviewer"
}
```

The CLI flag overrides the setting if both are present.

### Run subagents in foreground or background

Subagents can run in the foreground (blocking) or background (concurrent):

* **Foreground subagents** block the main conversation until complete. Permission prompts and clarifying questions (like [`AskUserQuestion`](/en/tools-reference)) are passed through to you.
* **Background subagents** run concurrently while you continue working. Before launching, Claude Code prompts for any tool permissions the subagent will need, ensuring it has the necessary approvals upfront. Once running, the subagent inherits these permissions and auto-denies anything not pre-approved. If a background subagent needs to ask clarifying questions, that tool call fails but the subagent continues.

If a background subagent fails due to missing permissions, you can start a new foreground subagent with the same task to retry with interactive prompts.

Claude decides whether to run subagents in the foreground or background based on the task. You can also:

* Ask Claude to "run this in the background"
* Press **Ctrl+B** to background a running task

To disable all background task functionality, set the `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` environment variable to `1`. See [Environment variables](/en/env-vars).

When [fork mode](#fork-the-current-conversation) is enabled, every subagent spawn runs in the background regardless of the `background` field. Forks still surface permission prompts in your terminal as they occur instead of pre-approving; named subagents follow the pre-approval flow above.

### Common patterns

#### Isolate high-volume operations

One of the most effective uses for subagents is isolating operations that produce large amounts of output. Running tests, fetching documentation, or processing log files can consume significant context. By delegating these to a subagent, the verbose output stays in the subagent's context while only the relevant summary returns to your main conversation.

```text theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Run parallel research

For independent investigations, spawn multiple subagents to work simultaneously:

```text theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Each subagent explores its area independently, then Claude synthesizes the findings. This works best when the research paths don't depend on each other.

<Warning>
  When subagents complete, their results return to your main conversation. Running many subagents that each return detailed results can consume significant context.
</Warning>

For tasks that need sustained parallelism or exceed your context window, [agent teams](/en/agent-teams) give each worker its own independent context.

#### Chain subagents

For multi-step workflows, ask Claude to use subagents in sequence. Each subagent completes its task and returns results to Claude, which then passes relevant context to the next subagent.

```text theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Choose between subagents and main conversation

Use the **main conversation** when:

* The task needs frequent back-and-forth or iterative refinement
* Multiple phases share significant context (planning → implementation → testing)
* You're making a quick, targeted change
* Latency matters. Subagents start fresh and may need time to gather context

Use **subagents** when:

* The task produces verbose output you don't need in your main context
* You want to enforce specific tool restrictions or permissions
* The work is self-contained and can return a summary

Consider [Skills](/en/skills) instead when you want reusable prompts or workflows that run in the main conversation context rather than isolated subagent context.

For a quick question about something already in your conversation, use [`/btw`](/en/interactive-mode#side-questions-with-%2Fbtw) instead of a subagent. It sees your full context but has no tool access, and the answer is discarded rather than added to history.

<Note>
  Subagents cannot spawn other subagents. If your workflow requires nested delegation, use [Skills](/en/skills) or [chain subagents](#chain-subagents) from the main conversation.
</Note>

### Manage subagent context

#### Resume subagents

Each subagent invocation creates a new instance with fresh context. To continue an existing subagent's work instead of starting over, ask Claude to resume it.

Resumed subagents retain their full conversation history, including all previous tool calls, results, and reasoning. The subagent picks up exactly where it stopped rather than starting fresh.

When a subagent completes, Claude receives its agent ID. Claude uses the `SendMessage` tool with the agent's ID as the `to` field to resume it. The `SendMessage` tool is only available when [agent teams](/en/agent-teams) are enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

To resume a subagent, ask Claude to continue the previous work:

```text theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

If a stopped subagent receives a `SendMessage`, it auto-resumes in the background without requiring a new `Agent` invocation.

You can also ask Claude for the agent ID if you want to reference it explicitly, or find IDs in the transcript files at `~/.claude/projects/{project}/{sessionId}/subagents/`. Each transcript is stored as `agent-{agentId}.jsonl`.

Subagent transcripts persist independently of the main conversation:

* **Main conversation compaction**: When the main conversation compacts, subagent transcripts are unaffected. They're stored in separate files.
* **Session persistence**: Subagent transcripts persist within their session. You can [resume a subagent](#resume-subagents) after restarting Claude Code by resuming the same session.
* **Automatic cleanup**: Transcripts are cleaned up based on the `cleanupPeriodDays` setting (default: 30 days).

#### Auto-compaction

Subagents support automatic compaction using the same logic as the main conversation. By default, auto-compaction triggers at approximately 95% capacity. To trigger compaction earlier, set `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` to a lower percentage (for example, `50`). See [environment variables](/en/env-vars) for details.

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
  Forked subagents are experimental and require Claude Code v2.1.117 or later. Behavior and configuration may change in future releases. Enable them by setting the [`CLAUDE_CODE_FORK_SUBAGENT`](/en/env-vars) environment variable to `1`. The variable is honored in interactive mode and via the SDK or `claude -p`.
</Note>

A fork is a subagent that inherits the entire conversation so far instead of starting fresh. This drops the input isolation that subagents otherwise provide: a fork sees the same system prompt, tools, model, and message history as the main session, so you can hand it a side task without re-explaining the situation. The fork's own tool calls still stay out of your conversation and only its final result comes back, so your main context window stays clean. Use a fork when a named subagent would need too much background to be useful, or when you want to try several approaches in parallel from the same starting point.

Enabling fork mode changes Claude Code in three ways:

* Claude spawns a fork whenever it would otherwise use the [general-purpose](#built-in-subagents) subagent. Named subagents such as Explore still spawn as before.
* Every subagent spawn runs in the [background](#run-subagents-in-foreground-or-background), whether it is a fork or a named subagent. Set `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` to `1` to keep spawns synchronous.
* The `/fork` command spawns a fork instead of acting as an alias for [`/branch`](/en/commands).

You can start a fork yourself with `/fork` followed by a directive. Claude Code names the fork from the first words of the directive. The following example forks the conversation to draft test cases while you continue with the implementation in the main session:

```text theme={null}
/fork draft unit tests for the parser changes so far
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

### How forks differ from named subagents

A fork inherits everything the main session has at the moment it spawns. A named subagent starts from its own definition.

|                         | Fork                             | Named subagent                                                                             |
| :---------------------- | :------------------------------- | :----------------------------------------------------------------------------------------- |
| Context                 | Full conversation history        | Fresh context with the prompt you pass                                                     |
| System prompt and tools | Same as main session             | From the subagent's [definition file](#write-subagent-files)                               |
| Model                   | Same as main session             | From the subagent's `model` field                                                          |
| Permissions             | Prompts surface in your terminal | [Pre-approved](#run-subagents-in-foreground-or-background) before launch, then auto-denied |
| Prompt cache            | Shared with main session         | Separate cache                                                                             |

Because a fork's system prompt and tool definitions are identical to the parent, its first request reuses the parent's prompt cache. This makes forking cheaper than spawning a fresh subagent for tasks that need the same context.

When Claude spawns a fork through the Agent tool, it can pass `isolation: "worktree"` so the fork's file edits are written to a separate git worktree instead of your checkout.

### Limitations

Setting `CLAUDE_CODE_FORK_SUBAGENT=1` enables fork mode in interactive sessions, [non-interactive mode](/en/headless), and the Agent SDK. A fork cannot spawn further forks.

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

A read-only subagent that reviews code without modifying it. This example shows how to design a focused subagent with limited tool access (no Edit or Write) and a detailed prompt that specifies exactly what to look for and how to format output.

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

Claude Code [passes hook input as JSON](/en/hooks#pretooluse-input) via stdin to hook commands. The validation script reads this JSON, extracts the command being executed, and checks it against a list of SQL write operations. If a write operation is detected, the script [exits with code 2](/en/hooks#exit-code-2-behavior-per-event) to block execution and returns an error message to Claude via stderr.

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

Make the script executable:

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

The hook receives JSON via stdin with the Bash command in `tool_input.command`. Exit code 2 blocks the operation and feeds the error message back to Claude. See [Hooks](/en/hooks#exit-code-output) for details on exit codes and [Hook input](/en/hooks#pretooluse-input) for the complete input schema.

## Next steps

Now that you understand subagents, explore these related features:

* [Distribute subagents with plugins](/en/plugins) to share subagents across teams or projects
* [Run Claude Code programmatically](/en/headless) with the Agent SDK for CI/CD and automation
* [Use MCP servers](/en/mcp) to give subagents access to external tools and data
