# Slash commands

> Control Claude's behavior during an interactive session with slash commands.

## Built-in slash commands

| Command                   | Purpose                                                                                                                                      |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir`                | Add additional working directories                                                                                                           |
| `/agents`                 | Manage custom AI subagents for specialized tasks                                                                                             |
| `/bashes`                 | List and manage background tasks                                                                                                             |
| `/bug`                    | Report bugs (sends conversation to Anthropic)                                                                                                |
| `/clear`                  | Clear conversation history                                                                                                                   |
| `/compact [instructions]` | Compact conversation with optional focus instructions                                                                                        |
| `/config`                 | Open the Settings interface (Config tab). Type to search and filter settings                                                                 |
| `/context`                | Visualize current context usage as a colored grid                                                                                            |
| `/cost`                   | Show token usage statistics. See [cost tracking guide](/en/costs#using-the-cost-command) for subscription-specific details.                  |
| `/doctor`                 | Checks installation health. Shows Updates section with auto-update channel and available npm versions                                        |
| `/exit`                   | Exit the REPL                                                                                                                                |
| `/export [filename]`      | Export the current conversation to a file or clipboard                                                                                       |
| `/help`                   | Get usage help                                                                                                                               |
| `/hooks`                  | Manage hook configurations for tool events                                                                                                   |
| `/ide`                    | Manage IDE integrations and show status                                                                                                      |
| `/init`                   | Initialize project with `CLAUDE.md` guide                                                                                                    |
| `/install-github-app`     | Set up Claude GitHub Actions for a repository                                                                                                |
| `/login`                  | Switch Anthropic accounts                                                                                                                    |
| `/logout`                 | Sign out from your Anthropic account                                                                                                         |
| `/mcp`                    | Manage MCP server connections and OAuth authentication                                                                                       |
| `/memory`                 | Edit `CLAUDE.md` memory files                                                                                                                |
| `/model`                  | Select or change the AI model                                                                                                                |
| `/output-style [style]`   | Set the output style directly or from a selection menu                                                                                       |
| `/permissions`            | View or update [permissions](/en/iam#configuring-permissions)                                                                                |
| `/plan`                   | Enter plan mode directly from the prompt                                                                                                     |
| `/plugin`                 | Manage Claude Code plugins                                                                                                                   |
| `/pr-comments`            | View pull request comments                                                                                                                   |
| `/privacy-settings`       | View and update your privacy settings                                                                                                        |
| `/release-notes`          | View release notes                                                                                                                           |
| `/rename <name>`          | Rename the current session for easier identification                                                                                         |
| `/remote-env`             | Configure remote session environment (claude.ai subscribers)                                                                                 |
| `/resume [session]`       | Resume a conversation by ID or name, or open the session picker                                                                              |
| `/review`                 | Request code review                                                                                                                          |
| `/rewind`                 | Rewind the conversation and/or code                                                                                                          |
| `/sandbox`                | Enable sandboxed bash tool with filesystem and network isolation for safer, more autonomous execution                                        |
| `/security-review`        | Complete a security review of pending changes on the current branch                                                                          |
| `/stats`                  | Visualize daily usage, session history, streaks, and model preferences. Press `r` to cycle date ranges (Last 7 days, Last 30 days, All time) |
| `/status`                 | Open the Settings interface (Status tab) showing version, model, account, and connectivity                                                   |
| `/statusline`             | Set up Claude Code's status line UI                                                                                                          |
| `/teleport`               | Resume a remote session from claude.ai by session ID, or open a picker (claude.ai subscribers)                                               |
| `/terminal-setup`         | Install Shift+Enter key binding for newlines (VS Code, Alacritty, Zed, Warp)                                                                 |
| `/theme`                  | Change the color theme                                                                                                                       |
| `/todos`                  | List current TODO items                                                                                                                      |
| `/usage`                  | For subscription plans only: show plan usage limits and rate limit status                                                                    |
| `/vim`                    | Enter vim mode for alternating insert and command modes                                                                                      |

## Custom slash commands

Custom slash commands allow you to define frequently used prompts as Markdown files that Claude Code can execute. Commands are organized by scope (project-specific or personal) and support namespacing through directory structures.

<Tip>
  Slash command autocomplete works anywhere in your input, not just at the beginning. Type `/` at any position to see available commands.
</Tip>

### Syntax

```
/<command-name> [arguments]
```

#### Parameters

| Parameter        | Description                                                       |
| :--------------- | :---------------------------------------------------------------- |
| `<command-name>` | Name derived from the Markdown filename (without `.md` extension) |
| `[arguments]`    | Optional arguments passed to the command                          |

### Command types

#### Project commands

Commands stored in your repository and shared with your team. When listed in `/help`, these commands show "(project)" after their description.

**Location**: `.claude/commands/`

The following example creates the `/optimize` command:

```bash  theme={null}
# Create a project command
mkdir -p .claude/commands
echo "Analyze this code for performance issues and suggest optimizations:" > .claude/commands/optimize.md
```

#### Personal commands

Commands available across all your projects. When listed in `/help`, these commands show "(user)" after their description.

**Location**: `~/.claude/commands/`

The following example creates the `/security-review` command:

```bash  theme={null}
# Create a personal command
mkdir -p ~/.claude/commands
echo "Review this code for security vulnerabilities:" > ~/.claude/commands/security-review.md
```

### Features

#### Namespacing

Use subdirectories to group related commands. Subdirectories appear in the command description but don't affect the command name.

For example:

* `.claude/commands/frontend/component.md` creates `/component` with description "(project:frontend)"
* `~/.claude/commands/component.md` creates `/component` with description "(user)"

If a project command and user command share the same name, the project command takes precedence and the user command is silently ignored. For example, if both `.claude/commands/deploy.md` and `~/.claude/commands/deploy.md` exist, `/deploy` runs the project version.

Commands in different subdirectories can share names since the subdirectory appears in the description to distinguish them. For example, `.claude/commands/frontend/test.md` and `.claude/commands/backend/test.md` both create `/test`, but show as "(project:frontend)" and "(project:backend)" respectively.

#### Arguments

Pass dynamic values to commands using argument placeholders:

##### All arguments with `$ARGUMENTS`

The `$ARGUMENTS` placeholder captures all arguments passed to the command:

```bash  theme={null}
# Command definition
echo 'Fix issue #$ARGUMENTS following our coding standards' > .claude/commands/fix-issue.md

# Usage
> /fix-issue 123 high-priority
# $ARGUMENTS becomes: "123 high-priority"
```

##### Individual arguments with `$1`, `$2`, etc.

Access specific arguments individually using positional parameters (similar to shell scripts):

```bash  theme={null}
# Command definition  
echo 'Review PR #$1 with priority $2 and assign to $3' > .claude/commands/review-pr.md

# Usage
> /review-pr 456 high alice
# $1 becomes "456", $2 becomes "high", $3 becomes "alice"
```

Use positional arguments when you need to:

* Access arguments individually in different parts of your command
* Provide defaults for missing arguments
* Build more structured commands with specific parameter roles

#### Bash command execution

Execute bash commands before the slash command runs using the `!` prefix. The output is included in the command context. You *must* include `allowed-tools` with the `Bash` tool, but you can choose the specific bash commands to allow.

For example:

```markdown  theme={null}
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
description: Create a git commit
---

## Context

- Current git status: !`git status`
- Current git diff (staged and unstaged changes): !`git diff HEAD`
- Current branch: !`git branch --show-current`
- Recent commits: !`git log --oneline -10`

## Your task

Based on the above changes, create a single git commit.
```

#### File references

Include file contents in commands using the `@` prefix to [reference files](/en/common-workflows#reference-files-and-directories).

For example:

```markdown  theme={null}
# Reference a specific file

Review the implementation in @src/utils/helpers.js

# Reference multiple files

Compare @src/old-version.js with @src/new-version.js
```

#### Thinking mode

Slash commands can trigger extended thinking by including [extended thinking keywords](/en/common-workflows#use-extended-thinking).

### Frontmatter

Command files support frontmatter, useful for specifying metadata about the command:

| Frontmatter                | Purpose                                                                                                                                                                               | Default                             |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :---------------------------------- |
| `allowed-tools`            | List of tools the command can use                                                                                                                                                     | Inherits from the conversation      |
| `argument-hint`            | The arguments expected for the slash command. Example: `argument-hint: add [tagId] \| remove [tagId] \| list`. This hint is shown to the user when auto-completing the slash command. | None                                |
| `context`                  | Set to `fork` to run the command in a forked sub-agent context with its own conversation history.                                                                                     | Inline (no fork)                    |
| `agent`                    | Specify which [agent type](/en/sub-agents#built-in-subagents) to use when `context: fork` is set. Only applicable when combined with `context: fork`.                                 | `general-purpose`                   |
| `description`              | Brief description of the command                                                                                                                                                      | Uses the first line from the prompt |
| `model`                    | Specific model string (see [Models overview](https://docs.claude.com/en/docs/about-claude/models/overview))                                                                           | Inherits from the conversation      |
| `disable-model-invocation` | Whether to prevent the `Skill` tool from calling this command                                                                                                                         | false                               |
| `hooks`                    | Define hooks scoped to this command's execution. See [Define hooks for commands](#define-hooks-for-commands).                                                                         | None                                |

For example:

```markdown  theme={null}
---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
argument-hint: [message]
description: Create a git commit
model: claude-3-5-haiku-20241022
---

Create a git commit with message: $ARGUMENTS
```

Example using positional arguments:

```markdown  theme={null}
---
argument-hint: [pr-number] [priority] [assignee]
description: Review pull request
---

Review PR #$1 with priority $2 and assign to $3.
Focus on security, performance, and code style.
```

#### Define hooks for commands

Slash commands can define hooks that run during the command's execution. Use the `hooks` field to specify `PreToolUse`, `PostToolUse`, or `Stop` handlers:

```markdown  theme={null}
---
description: Deploy to staging with validation
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-deploy.sh"
          once: true
---

Deploy the current branch to staging environment.
```

The `once: true` option runs the hook only once per session. After the first successful execution, the hook is removed.

Hooks defined in a command are scoped to that command's execution and are automatically cleaned up when the command finishes.

See [Hooks](/en/hooks) for the complete hook configuration format.

## Plugin commands

[Plugins](/en/plugins) can provide custom slash commands that integrate seamlessly with Claude Code. Plugin commands work exactly like user-defined commands but are distributed through [plugin marketplaces](/en/plugin-marketplaces).

### How plugin commands work

Plugin commands are:

* **Namespaced**: Commands can use the format `/plugin-name:command-name` to avoid conflicts (plugin prefix is optional unless there are name collisions)
* **Automatically available**: Once a plugin is installed and enabled, its commands appear in `/help`
* **Fully integrated**: Support all command features (arguments, frontmatter, bash execution, file references)

### Plugin command structure

**Location**: `commands/` directory in plugin root

**File format**: Markdown files with frontmatter

**Basic command structure**:

```markdown  theme={null}
---
description: Brief description of what the command does
---

# Command Name

Detailed instructions for Claude on how to execute this command.
Include specific guidance on parameters, expected outcomes, and any special considerations.
```

**Advanced command features**:

* **Arguments**: Use placeholders like `{arg1}` in command descriptions
* **Subdirectories**: Organize commands in subdirectories for namespacing
* **Bash integration**: Commands can execute shell scripts and programs
* **File references**: Commands can reference and modify project files

### Invocation patterns

```shell Direct command (when no conflicts) theme={null}
/command-name
```

```shell Plugin-prefixed (when needed for disambiguation) theme={null}
/plugin-name:command-name
```

```shell With arguments (if command supports them) theme={null}
/command-name arg1 arg2
```

## MCP slash commands

MCP servers can expose prompts as slash commands that become available in Claude Code. These commands are dynamically discovered from connected MCP servers.

### Command format

MCP commands follow the pattern:

```
/mcp__<server-name>__<prompt-name> [arguments]
```

### Features

#### Dynamic discovery

MCP commands are automatically available when:

* An MCP server is connected and active
* The server exposes prompts through the MCP protocol
* The prompts are successfully retrieved during connection

#### Arguments

MCP prompts can accept arguments defined by the server:

```
# Without arguments
> /mcp__github__list_prs

# With arguments
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug title" high
```

#### Naming conventions

Server and prompt names are normalized:

* Spaces and special characters become underscores
* Names are lowercase for consistency

### Managing MCP connections

Use the `/mcp` command to:

* View all configured MCP servers
* Check connection status
* Authenticate with OAuth-enabled servers
* Clear authentication tokens
* View available tools and prompts from each server

### MCP permissions and wildcards

To approve all tools from an MCP server, use either the server name alone or wildcard syntax:

* `mcp__github` (approves all GitHub tools)
* `mcp__github__*` (wildcard syntax, also approves all GitHub tools)

To approve specific tools, list each one explicitly:

* `mcp__github__get_issue`
* `mcp__github__list_issues`

See [MCP permission rules](/en/iam#tool-specific-permission-rules) for more details.

## `Skill` tool

<Note>
  In earlier versions of Claude Code, slash command invocation was provided by a separate `SlashCommand` tool. This has been merged into the `Skill` tool.
</Note>

The `Skill` tool allows Claude to programmatically invoke both [custom slash commands](/en/slash-commands#custom-slash-commands) and [Agent Skills](/en/skills) during a conversation. This gives Claude the ability to use these capabilities on your behalf when appropriate.

### What the `Skill` tool can invoke

The `Skill` tool provides access to:

| Type                  | Location                                     | Requirements                                   |
| :-------------------- | :------------------------------------------- | :--------------------------------------------- |
| Custom slash commands | `.claude/commands/` or `~/.claude/commands/` | Must have `description` frontmatter            |
| Agent Skills          | `.claude/skills/` or `~/.claude/skills/`     | Must not have `disable-model-invocation: true` |

Built-in commands like `/compact` and `/init` are *not* available through this tool.

### Encourage Claude to use specific commands

To encourage Claude to use the `Skill` tool, reference the command by name, including the slash, in your prompts or `CLAUDE.md` file:

```
> Run /write-unit-test when you are about to start writing tests.
```

This tool puts each available command's metadata into context up to the character budget limit. Use `/context` to monitor token usage.

To see which commands and Skills are available to the `Skill` tool, run `claude --debug` and trigger a query.

### Disable the `Skill` tool

To prevent Claude from programmatically invoking any commands or Skills:

```bash  theme={null}
/permissions
# Add to deny rules: Skill
```

This removes the `Skill` tool and all command/Skill descriptions from context.

### Disable specific commands or Skills

To prevent a specific command or Skill from being invoked programmatically via the `Skill` tool, add `disable-model-invocation: true` to its frontmatter. This also removes the item's metadata from context.

<Note>
  The `user-invocable` field in Skills only controls menu visibility, not `Skill` tool access. Use `disable-model-invocation: true` to block programmatic invocation. See [Control Skill visibility](/en/skills#control-skill-visibility) for details.
</Note>

### `Skill` permission rules

The permission rules support:

* **Exact match**: `Skill(commit)` (allows only `commit` with no arguments)
* **Prefix match**: `Skill(review-pr:*)` (allows `review-pr` with any arguments)

### Character budget limit

The `Skill` tool includes a character budget to limit context usage. This prevents token overflow when many commands and Skills are available.

The budget includes each item's name, arguments, and description.

* **Default limit**: 15,000 characters
* **Custom limit**: Set via `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable. The name is retained for backwards compatibility.

When the budget is exceeded, Claude sees only a subset of available items. In `/context`, a warning shows how many are included.

## Skills vs slash commands

**Slash commands** and **Agent Skills** serve different purposes in Claude Code:

### Use slash commands for

**Quick, frequently used prompts**:

* Simple prompt snippets you use often
* Quick reminders or templates
* Frequently used instructions that fit in one file

**Examples**:

* `/review` → "Review this code for bugs and suggest improvements"
* `/explain` → "Explain this code in simple terms"
* `/optimize` → "Analyze this code for performance issues"

### Use Skills for

**Comprehensive capabilities with structure**:

* Complex workflows with multiple steps
* Capabilities requiring scripts or utilities
* Knowledge organized across multiple files
* Team workflows you want to standardize

**Examples**:

* PDF processing Skill with form-filling scripts and validation
* Data analysis Skill with reference docs for different data types
* Documentation Skill with style guides and templates

### Key differences

| Aspect         | Slash Commands                   | Agent Skills                        |
| -------------- | -------------------------------- | ----------------------------------- |
| **Complexity** | Simple prompts                   | Complex capabilities                |
| **Structure**  | Single .md file                  | Directory with SKILL.md + resources |
| **Discovery**  | Explicit invocation (`/command`) | Automatic (based on context)        |
| **Files**      | One file only                    | Multiple files, scripts, templates  |
| **Scope**      | Project or personal              | Project or personal                 |
| **Sharing**    | Via git                          | Via git                             |

### Example comparison

**As a slash command**:

```markdown  theme={null}
# .claude/commands/review.md
Review this code for:
- Security vulnerabilities
- Performance issues
- Code style violations
```

Usage: `/review` (manual invocation)

**As a Skill**:

```
.claude/skills/code-review/
├── SKILL.md (overview and workflows)
├── SECURITY.md (security checklist)
├── PERFORMANCE.md (performance patterns)
├── STYLE.md (style guide reference)
└── scripts/
    └── run-linters.sh
```

Usage: "Can you review this code?" (automatic discovery)

The Skill provides richer context, validation scripts, and organized reference material.

### When to use each

**Use slash commands**:

* You invoke the same prompt repeatedly
* The prompt fits in a single file
* You want explicit control over when it runs

**Use Skills**:

* Claude should discover the capability automatically
* Multiple files or scripts are needed
* Complex workflows with validation steps
* Team needs standardized, detailed guidance

Both slash commands and Skills can coexist. Use the approach that fits your needs.

Learn more about [Agent Skills](/en/skills).

## See also

* [Plugins](/en/plugins) - Extend Claude Code with custom commands through plugins
* [Identity and Access Management](/en/iam) - Complete guide to permissions, including MCP tool permissions
* [Interactive mode](/en/interactive-mode) - Shortcuts, input modes, and interactive features
* [CLI reference](/en/cli-reference) - Command-line flags and options
* [Settings](/en/settings) - Configuration options
* [Memory management](/en/memory) - Managing Claude's memory across sessions


---

> To find navigation and other pages in this documentation, fetch the llms.txt file at: https://code.claude.com/docs/llms.txt