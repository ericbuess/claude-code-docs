> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugins reference

> Complete technical reference for Claude Code plugin system, including schemas, CLI commands, and component specifications.

<Tip>
  Looking to install plugins? See [Discover and install plugins](/docs/en/discover-plugins). For creating plugins, see [Plugins](/docs/en/plugins). For distributing plugins, see [Plugin marketplaces](/docs/en/plugin-marketplaces).
</Tip>

A **plugin** is a self-contained directory of components that extends Claude Code with custom functionality. Plugin components include skills, agents, hooks, MCP servers, LSP servers, and monitors.

## Plugin components reference

### Skills

Plugins add skills to Claude Code, creating `/name` shortcuts that you or Claude can invoke.

**Location**: `skills/` or `commands/` directory in plugin root, or a single `SKILL.md` file at the plugin root

**File format**: Skills are directories with `SKILL.md`; commands are simple markdown files

**Skill structure**:

```text theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

Skills and commands are automatically discovered when the plugin is installed.

If a plugin has no `skills/` directory and no `skills` manifest field, a `SKILL.md` at the plugin root is loaded as a single skill. Set the frontmatter `name` field to control the skill's invocation name. Without it, Claude Code falls back to the install directory name, which for marketplace-installed plugins is a version string that changes on every update. For plugins that ship more than one skill, use the `skills/` directory layout shown above.

In plugin skills and commands, Boolean frontmatter fields such as `disable-model-invocation` accept `yes`, `no`, `on`, `off`, `1`, and `0` in any letter case, in addition to `true` and `false`. Before v2.1.218, Claude Code recognized only `true` and `false`.

For complete details, see [Skills](/docs/en/skills).

### Agents

Plugins can provide specialized subagents for specific tasks that Claude can invoke automatically when appropriate.

**Location**: `agents/` directory in plugin root

**File format**: Markdown files describing agent capabilities

**Agent structure**:

```markdown theme={null}
---
name: agent-name
description: What this agent specializes in and when Claude should invoke it
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Detailed system prompt for the agent describing its role, expertise, and behavior.
```

Plugin agents support `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background`, and `isolation` frontmatter fields. The only valid `isolation` value is `"worktree"`. For security reasons, `hooks`, `mcpServers`, and `permissionMode` are not supported for plugin-shipped agents.

Claude Code loads a plugin agent even when its frontmatter has no `name` or doesn't parse:

* No `name`: Claude Code names the agent after the file, so `agents/reviewer.md` in a plugin named `my-plugin` loads as `my-plugin:reviewer`
* Frontmatter that doesn't parse: Claude Code names the agent after the file, uses `Agent from my-plugin plugin` as its description, and ignores every field in the file

By contrast, Claude Code skips a project, user, or managed agent file whose frontmatter has no `name` or doesn't parse.

To find files in a plugin's default `agents/` directory whose frontmatter doesn't parse, run `claude plugin validate`. The path you pass depends on whether the plugin has a manifest, and both examples use `./my-plugin` as the plugin directory:

* A plugin with a manifest: `claude plugin validate ./my-plugin`
* A plugin without a manifest: `claude plugin validate ./my-plugin/agents`. Requires Claude Code v2.1.233 or later.

Agents appear in the [@-mention typeahead](/docs/en/sub-agents#invoke-subagents-explicitly) under their scoped name, such as `my-plugin:code-reviewer`, once the plugin is enabled.

For complete details, see [Subagents](/docs/en/sub-agents).

### Hooks

Plugins can provide event handlers that respond to Claude Code events automatically.

**Location**: `hooks/hooks.json` in plugin root, or inline in plugin.json

**Format**: JSON configuration with event matchers and actions

**Hook configuration**:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Plugin hooks respond to the same lifecycle events as [user-defined hooks](/docs/en/hooks):

| Event                 | When it fires                                                                                                                                                                                                                                         |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                                                                                                                      |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts                                                                                                            |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                                                                                                                  |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                                                                                                                    |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                                                                                                                             |
| `PermissionRequest`   | When a tool call needs a permission decision                                                                                                                                                                                                          |
| `PermissionDenied`    | When auto mode denies a tool call, including denials without a classifier verdict. Use JSON `hookSpecificOutput.retry: true` to tell the model it may retry the denied tool call. Claude Code ignores `retry` when the classifier produced no verdict |
| `PostToolUse`         | After a tool call succeeds                                                                                                                                                                                                                            |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                                                                                                               |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                                                                                                                        |
| `Notification`        | When Claude Code sends a notification                                                                                                                                                                                                                 |
| `MessageDisplay`      | While assistant message text is displayed                                                                                                                                                                                                             |
| `SubagentStart`       | When a subagent is spawned                                                                                                                                                                                                                            |
| `SubagentStop`        | When a subagent finishes                                                                                                                                                                                                                              |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                                                                                                                         |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                                                                                                                              |
| `Stop`                | When Claude finishes responding                                                                                                                                                                                                                       |
| `StopFailure`         | When the turn ends due to an API error                                                                                                                                                                                                                |
| `TeammateIdle`        | When an [agent team](/docs/en/agent-teams) teammate is about to go idle                                                                                                                                                                                    |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session                                                                                                        |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                                                                                                                    |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv                                                                                                |
| `DirectoryAdded`      | When a working directory is added mid-session via `/add-dir` or the SDK `register_repo_root` control request                                                                                                                                          |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                                                                                                                           |
| `WorktreeCreate`      | When a worktree is being created via `--worktree`, `isolation: "worktree"`, or for a background session. Replaces default git behavior                                                                                                                |
| `WorktreeRemove`      | When a worktree is being removed at session exit, when a subagent finishes, or when you delete a background session                                                                                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                                                                                                                             |
| `PostCompact`         | After context compaction completes                                                                                                                                                                                                                    |
| `PreModelSwitch`      | Before Claude Code applies a model switch that you or a client requested. Can block the switch                                                                                                                                                        |
| `PostModelSwitch`     | After the session's model changes, including changes Claude Code makes on its own, such as restoring the model when you resume a session                                                                                                              |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                                                                                                                             |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                                                                                                                           |
| `SessionEnd`          | When a session terminates                                                                                                                                                                                                                             |

**Hook types**:

* `command`: execute shell commands or scripts
* `http`: send the event JSON as a POST request to a URL
* `mcp_tool`: call a tool on a configured [MCP server](/docs/en/mcp)
* `prompt`: evaluate a prompt with an LLM (uses `$ARGUMENTS` placeholder for context)
* `agent`: run an agentic verifier with tools for complex verification tasks

Hooks that target the plugin's own [bundled MCP server](#mcp-servers) must use its scoped names. Tool matchers and `if` fields take the scoped tool name `mcp__plugin_<plugin-name>_<server-name>__<tool>`, and an `mcp_tool` hook's `server` field takes `plugin:<plugin-name>:<server-name>`. A matcher written against the bare server key never fires. See [Match MCP tools](/docs/en/hooks#match-mcp-tools) and [Plugin-provided MCP servers](/docs/en/mcp#plugin-provided-mcp-servers).

### MCP servers

Plugins can bundle Model Context Protocol (MCP) servers to connect Claude Code with external tools and services.

**Location**: `.mcp.json` in plugin root, or inline in plugin.json

**Format**: Standard MCP server configuration

**MCP server configuration**:

```json theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"]
    }
  }
}
```

**Integration behavior**:

* Plugin MCP servers start automatically when the plugin is enabled
* Servers appear as standard MCP tools in Claude's toolkit
* Plugin servers can be configured independently of user MCP servers
* If you run [`/reload-plugins`](/docs/en/discover-plugins#apply-plugin-changes-without-restarting) mid-session, Claude Code keeps the live connections of servers whose configuration is unchanged

### LSP servers

<Tip>
  Looking to use LSP plugins? Install them from the official marketplace: search for "lsp" in the `/plugin` Discover tab. This section documents how to create LSP plugins for languages not covered by the official marketplace.
</Tip>

Plugins can provide [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) servers to give Claude [real-time code intelligence](/docs/en/discover-plugins#code-intelligence) while working on your codebase.

**Location**: `.lsp.json` in plugin root, or inline in `plugin.json`

**Format**: JSON configuration mapping language server names to their configurations

**`.lsp.json` file format**:

```json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Inline in `plugin.json`**:

```json theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Required fields:**

| Field                 | Description                                  |
| :-------------------- | :------------------------------------------- |
| `command`             | The LSP binary to execute (must be in PATH)  |
| `extensionToLanguage` | Maps file extensions to language identifiers |

**Optional fields:**

| Field                   | Description                                                                                                                                                              |
| :---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `args`                  | Command-line arguments for the LSP server                                                                                                                                |
| `transport`             | Communication transport: `stdio` (default) or `socket`. Claude Code accepts `socket` but runs every server over stdio, so the stdout protocol rules apply to all servers |
| `env`                   | Environment variables to set when starting the server                                                                                                                    |
| `initializationOptions` | Options passed to the server during initialization                                                                                                                       |
| `settings`              | Settings passed via `workspace/didChangeConfiguration`                                                                                                                   |
| `workspaceFolder`       | Workspace folder path for the server                                                                                                                                     |
| `startupTimeout`        | Max time to wait for server startup (milliseconds)                                                                                                                       |
| `shutdownTimeout`       | Max time to wait for graceful shutdown (milliseconds). When the timeout elapses, Claude Code terminates the server process. When unset, no timeout applies               |
| `restartOnCrash`        | Whether to restart the server after it crashes. Defaults to `true`. Set to `false` to leave a crashed server stopped instead of restarting it                            |
| `maxRestarts`           | Maximum number of restart attempts before giving up                                                                                                                      |
| `diagnostics`           | Whether to push diagnostics into Claude's context after edits (default `true`). Set to `false` to keep code navigation but suppress automatic diagnostic injection.      |

`restartOnCrash` and `shutdownTimeout` require Claude Code v2.1.205 or later. Before v2.1.205, the config schema accepted both options but setting either one caused Claude Code to skip that LSP server entirely at startup, with the reason visible only in `claude --debug` output.

**Multiple servers for the same extension**: when more than one enabled LSP server declares the same file extension in `extensionToLanguage`, whether the servers come from one plugin or from different plugins, the first server registered handles files with that extension and the others never start. The `/plugin` interface shows a warning naming the plugin whose server is active.

**Servers that fail to initialize**: Claude Code skips a server whose configuration is invalid, for example one missing `command` or `extensionToLanguage`, and the other configured servers still start. Run `claude --debug` to see why a server was skipped.

A skipped server doesn't claim its file extensions, so another valid server that declares the same extension, from the same or a different plugin, still handles those files.

**Send log output to stderr, not stdout**: Claude Code reads a server's stdout as protocol messages only, and accepts message headers up to 64 KiB and a message body up to 32 MiB. Claude Code disconnects a server that exceeds either limit or writes non-protocol output to stdout, and counts the disconnect as a crash for `restartOnCrash` and `maxRestarts`. When you run with `--debug`, Claude Code writes an error naming the cause to the debug log.

<Warning>
  **You must install the language server binary separately.** LSP plugins configure how Claude Code connects to a language server, but they don't include the server itself. If you see `Executable not found in $PATH` in the `/plugin` Errors tab, install the required binary for your language.
</Warning>

**Available LSP plugins:**

| Plugin              | Language server            | Install command                                                                            |
| :------------------ | :------------------------- | :----------------------------------------------------------------------------------------- |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` or `npm install -g pyright`                                          |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                     |
| `rust-analyzer-lsp` | rust-analyzer              | [See rust-analyzer installation](https://rust-analyzer.github.io/manual.html#installation) |

Install the language server first, then install the plugin from the marketplace.

### Monitors

Plugins can declare background monitors that Claude Code starts automatically when the plugin is active. Each monitor runs a shell command for the lifetime of the session and delivers every stdout line to Claude as a notification, so Claude can react to log entries, status changes, or polled events without being asked to start the watch itself.

Plugin monitors use the same mechanism as the [Monitor tool](/docs/en/tools-reference#monitor-tool) and share its availability constraints. They run only in interactive CLI sessions, run unsandboxed at the same trust level as [hooks](#hooks), and are skipped on hosts where the Monitor tool is unavailable.

**Location**: `monitors/monitors.json` in the plugin root, or inline in `plugin.json`

**Format**: JSON array of monitor entries

The following `monitors/monitors.json` watches a deployment status endpoint and a local error log:

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

To declare monitors inline, set `experimental.monitors` in `plugin.json` to the same array. To load from a non-default path, set `experimental.monitors` to a relative path string such as `"./config/monitors.json"`. Monitors are an [experimental component](#experimental-components).

**Required fields:**

| Field         | Description                                                                                                           |
| :------------ | :-------------------------------------------------------------------------------------------------------------------- |
| `name`        | Identifier unique within the plugin. Prevents duplicate processes when the plugin reloads or a skill is invoked again |
| `command`     | Shell command run as a persistent background process in the session working directory                                 |
| `description` | Short summary of what is being watched. Shown in the task panel and in notification summaries                         |

**Optional fields:**

| Field  | Description                                                                                                                                                                                                              |
| :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `when` | Controls when the monitor starts. `"always"` starts it at session start and on plugin reload, and is the default. `"on-skill-invoke:<skill-name>"` starts it the first time the named skill in this plugin is dispatched |

The `command` value supports the [path substitutions](#environment-variables) `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, and `${CLAUDE_PROJECT_DIR}`, plus any `${ENV_VAR}` from the environment. Prefix the command with `cd "${CLAUDE_PLUGIN_ROOT}" && ` if the script needs to run from the plugin's own directory.

A monitor `command` can't reference [`${user_config.*}`](#user-configuration) values. The command runs through a shell, so Claude Code rejects the monitor with an [error](/docs/en/errors#plugin-command-references-user-config) instead of substituting the value. Monitor processes don't receive `CLAUDE_PLUGIN_OPTION_<KEY>` environment variables, so have the monitor script read the value from a config file it owns.

If you disable a plugin mid-session, Claude Code doesn't stop monitors that are already running; they stop when the session ends.

### Themes

Plugins can ship color themes that appear in `/theme` alongside the built-in presets and the user's local themes. A theme is a JSON file in `themes/` with a `base` preset and a sparse `overrides` map of color tokens. Themes are an [experimental component](#experimental-components).

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

When a user selects a plugin theme, Claude Code saves `custom:<plugin-name>:<slug>` in their config. Plugin themes are read-only: when a user presses `Ctrl+E` on one in `/theme`, Claude Code copies it into `~/.claude/themes/` so they can edit the copy.

***

## Plugin installation scopes

When you install a plugin, you choose a **scope** that determines where the plugin is available and who else can use it:

| Scope     | Settings file                            | Use case                                                                    |
| :-------- | :--------------------------------------- | :-------------------------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                | Personal plugins available across all projects (default)                    |
| `project` | `.claude/settings.json`                  | Team plugins shared via version control                                     |
| `local`   | `.claude/settings.local.json`            | Project-specific plugins, gitignored when Claude Code saves a setting to it |
| `managed` | [Managed settings](/docs/en/managed-settings) | Managed plugins (read-only, update only)                                    |

Plugins use the same scope system as other Claude Code configurations. For installation instructions and scope flags, see [Install plugins](/docs/en/discover-plugins#install-plugins). For a complete explanation of scopes, see [Configuration scopes](/docs/en/settings#where-settings-live).

***

## Skills-directory plugins

Any folder under a skills directory that contains a `.claude-plugin/plugin.json` manifest is loaded as a plugin named `<name>@skills-dir` on the next session, with no marketplace and no install step. Scaffold one with [`plugin init`](#plugin-init). Unlike a copied marketplace install, the plugin is discovered in place rather than copied into the plugin cache.

A skills directory tree supports three distinct things:

| What you have                                 | What it is                                                                          |
| :-------------------------------------------- | :---------------------------------------------------------------------------------- |
| `<skills-dir>/foo/SKILL.md` with no manifest  | A plain [skill](/docs/en/skills) named `foo`                                             |
| `<skills-dir>/foo/.claude-plugin/plugin.json` | A plugin `foo@skills-dir`, which can bundle its own skills, agents, hooks, and more |
| `<plugin>/skills/bar/SKILL.md`                | A skill `bar` packaged inside a plugin                                              |

### Choose where the plugin loads from

| Skills directory        | Scope    | Loads                                                                                                                   |
| :---------------------- | :------- | :---------------------------------------------------------------------------------------------------------------------- |
| `~/.claude/skills/`     | personal | In every project, since the location is yours alone                                                                     |
| `<cwd>/.claude/skills/` | project  | Only after you accept the workspace [trust dialog](/docs/en/permissions#what-runs-before-you-trust-a-folder) for that folder |

A project-scope plugin is checked into the repository and reaches every collaborator who clones it. Because that content comes from the repository rather than from you, it loads only after the same trust gate that governs project allow rules in `.claude/settings.json`, so trusting a parent folder or running with `-p` isn't enough, and components that run code are restricted further:

* MCP servers it declares go through the [same per-server approval](/docs/en/mcp) as a project `.mcp.json`
* LSP servers start only after you trust the workspace
* [Background monitors](#monitors) do not load

Personal-scope plugins have none of these restrictions.

<Warning>
  Project-scope `@skills-dir` plugins load only from the `.claude/skills/` of the session's [primary working directory](/docs/en/permissions#working-directories). They don't [walk up to the repository root](/docs/en/skills#discovery-from-parent-and-nested-directories) the way plain skills and commands do, so launching from a subdirectory misses a plugin that lives at the repo root. Launch from the repository root, or [move the session there with `/cd`](/docs/en/permissions#move-the-session-to-another-directory) on v2.1.246 or later.
</Warning>

### Edit, reload, and disable a skills-directory plugin

Changes you make to a skill's `SKILL.md` take effect immediately in the current session. Changes to the plugin's other components, such as `hooks/`, `.mcp.json`, `agents/`, and `output-styles/`, do not. Run `/reload-plugins` or restart Claude Code to pick those up. See [Live change detection](/docs/en/skills#live-change-detection).

To stop loading a skills-directory plugin, delete its folder or disable it by name. There is no `uninstall` step because nothing was installed from a marketplace.

```bash theme={null}
claude plugin disable my-tool@skills-dir
```

***

<h2 id="synced-plugins">
  Plugins synced from claude.ai
</h2>

In [Cowork](https://claude.com/product/cowork) and [cloud sessions](/docs/en/cloud-environments#what-carries-over-from-your-setup), Claude Code downloads the plugins enabled for your claude.ai account into `~/.claude/plugins/synced/` in the session's own environment and loads each one as `<name>@synced`, with no marketplace and no install record. Claude Code doesn't load them in sessions you start in your own terminal. Inside that Cowork or cloud environment, `claude plugin list` shows the downloaded copies under a `Synced from claude.ai` heading. Before v2.1.239, Claude Code loaded these plugins as `<name>@inline`, the identity that `--plugin-dir` plugins use.

Manage a synced plugin by the `<name>@synced` ID that `claude plugin list` prints:

* **Turn one off**: in the synced session, run `claude plugin disable <name>@synced`, or ask Claude to run it. Claude Code saves the choice as `"<name>@synced": false` in that environment's user-level [`enabledPlugins`](/docs/en/settings-reference#enabledplugins). To turn the plugin back on, run `claude plugin enable <name>@synced` in the same session. To keep a plugin out of every synced session, [turn it off for your claude.ai account](/docs/en/desktop#extend-claude-code). To keep it out of one project's synced sessions in every environment, set `"<name>@synced": false` under `enabledPlugins` in that project's committed `.claude/settings.json`.
* **Manage the plugin itself on claude.ai**: `claude plugin install`, `update`, and `uninstall` don't apply to a synced plugin. To remove one, turn the plugin off for your claude.ai account; the next synced session starts without it.

When an enabled plugin from any other source, such as a marketplace install, a [skills-directory plugin](#skills-directory-plugins), or a `--plugin-dir` plugin, matches a synced plugin's name, Claude Code loads that plugin and reports the synced copy as not loaded. To use the claude.ai copy instead, disable your own copy. Before v2.1.239, Claude Code loaded the synced copy instead of a same-named marketplace install.

***

## Plugin manifest schema

The `.claude-plugin/plugin.json` file defines your plugin's metadata and configuration.

The manifest is optional. If omitted, Claude Code auto-discovers components in [default locations](#file-locations-reference) and derives the plugin name from the directory name. Use a manifest when you need to provide metadata or custom component paths.

### Complete schema

```json theme={null}
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "metadata": { "catalogId": "cat-123", "tier": "pro" },
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Required fields

If you include a manifest, `name` is the only required field.

| Field  | Type   | Description                                                                                                                                                                                                                                                                                         | Example              |
| :----- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------- |
| `name` | string | Unique identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters. When a [marketplace entry](/docs/en/plugin-marketplaces#plugin-entries) lists the plugin under a different name, the marketplace entry name is what `enabledPlugins` keys and `/plugin` use | `"deployment-tools"` |

This name is used for namespacing components. For example, in the UI, the
agent `agent-creator` for the plugin with name `plugin-dev` will appear as
`plugin-dev:agent-creator`.

### Unrecognized fields

Claude Code ignores top-level fields it does not recognize. You can keep
metadata from another ecosystem in `plugin.json` and the plugin still loads.
This makes it practical to maintain one manifest that doubles as a VS Code or
Cursor extension manifest, an npm `package.json`, or an MCPB/DXT bundle
manifest.

`claude plugin validate` reports unrecognized fields as warnings, not errors.
If a field is one or two characters off from a recognized one, the warning
suggests the likely intended name. A plugin with only unrecognized-field
warnings still passes validation and loads at runtime.

How Claude Code handles a recognized field whose value has the wrong type depends on the field:

* **Most fields**: the plugin fails to load. For example, a `keywords` value that is a string instead of an array is a load error, and `claude plugin validate` reports it as one.
* **`experimental` and `metadata`**: Claude Code ignores a non-object value, and `claude plugin validate` reports a warning.

Pass `--strict` to treat warnings as errors. Use it in CI to catch a misspelled
field name or a field left over from another tool's manifest before publishing,
even though the plugin would load at runtime.

```bash theme={null}
claude plugin validate ./my-plugin --strict
```

### Metadata fields

| Field            | Type    | Description                                                                                                                                                                                                                                                                                                                                                                                                          | Example                                                           |
| :--------------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`        | string  | JSON Schema URL for editor autocomplete and validation. Claude Code ignores this field at load time.                                                                                                                                                                                                                                                                                                                 | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `displayName`    | string  | Human-readable name shown in the `/plugin` picker and other UI surfaces. Falls back to `name` when omitted. Unlike `name`, may contain spaces and any casing. Not used for namespacing or lookup.                                                                                                                                                                                                                    | `"Deployment Tools"`                                              |
| `version`        | string  | Optional. Semantic version. Setting this pins the plugin to that version string, so users only receive updates when you bump it, except for a [`command` source](/docs/en/plugin-marketplaces#command-sources); see [Version management](#version-management). If also set in the marketplace entry, `plugin.json` wins. If omitted, the version comes from the next source in [Version management](#version-management). | `"2.1.0"`                                                         |
| `description`    | string  | Brief explanation of plugin purpose                                                                                                                                                                                                                                                                                                                                                                                  | `"Deployment automation tools"`                                   |
| `author`         | object  | Author information                                                                                                                                                                                                                                                                                                                                                                                                   | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`       | string  | Documentation URL                                                                                                                                                                                                                                                                                                                                                                                                    | `"https://docs.example.com"`                                      |
| `repository`     | string  | Source code URL                                                                                                                                                                                                                                                                                                                                                                                                      | `"https://github.com/user/plugin"`                                |
| `license`        | string  | License identifier                                                                                                                                                                                                                                                                                                                                                                                                   | `"MIT"`, `"Apache-2.0"`                                           |
| `keywords`       | array   | Discovery tags                                                                                                                                                                                                                                                                                                                                                                                                       | `["deployment", "ci-cd"]`                                         |
| `metadata`       | object  | Free-form object for your own data, such as entitlement or catalog fields. Claude Code doesn't read it, so the values never affect plugin behavior. Claude Code ignores a non-object value, and `claude plugin validate` reports it as a warning. Before v2.1.222, Claude Code treated the key as an [unrecognized field](#unrecognized-fields).                                                                     | `{"catalogId": "cat-123"}`                                        |
| `defaultEnabled` | boolean | Whether the plugin starts in an enabled state when the user has not set one. Defaults to `true`. See [Default enablement](#default-enablement).                                                                                                                                                                                                                                                                      | `false`                                                           |

### Default enablement

Set `defaultEnabled: false` in `plugin.json` to ship a plugin that installs disabled. The user turns it on with `claude plugin enable <plugin>` or the `/plugin` interface. Use this for plugins that add cost or scope a user should opt into, such as one that connects to an external service.

`defaultEnabled` is the fallback when nothing else has decided the plugin's state. Two things take precedence over it:

* **The user's setting**: an entry for the plugin in `enabledPlugins` at any settings scope. Once written, it persists across plugin updates and reinstalls, so changing `defaultEnabled` in a later release does not flip an existing user.
* **A dependency requirement**: when a plugin is required by another one that is active, Claude Code writes `true` for it at install or enable time. That gives it an explicit setting, so its own default no longer applies. See [Enable or disable a plugin with dependencies](/docs/en/plugin-dependencies#enable-or-disable-a-plugin-with-dependencies).

The same field can appear in a plugin's marketplace entry, where it takes precedence over the value in `plugin.json`. See [Optional plugin fields](/docs/en/plugin-marketplaces#optional-plugin-fields).

### Component path fields

| Field                   | Type                  | Description                                                                                                                                                                   | Example                                              |
| :---------------------- | :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`                | string\|array         | Custom skill directories containing `<name>/SKILL.md`. Adds to the default `skills/` scan. See [Path behavior rules](#path-behavior-rules) for the marketplace-root exception | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | Custom flat `.md` skill files or directories (replaces default `commands/`)                                                                                                   | `"./custom/cmd.md"` or `["./cmd1.md"]`               |
| `agents`                | string\|array         | Custom agent files (replaces default `agents/`)                                                                                                                               | `"./custom/agents/reviewer.md"`                      |
| `workflows`             | string\|array         | Custom [workflow](/docs/en/workflows) script files or directories (replaces default `workflows/`)                                                                                  | `"./custom/workflows/"`                              |
| `hooks`                 | string\|array\|object | Hook config paths or inline config                                                                                                                                            | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | MCP config paths or inline config                                                                                                                                             | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | Custom output style files/directories (replaces default `output-styles/`)                                                                                                     | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) configs for code intelligence (go to definition, find references, etc.)                     | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | Color theme files/directories (replaces default `themes/`). See [Themes](#themes)                                                                                             | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | Background [Monitor](/docs/en/tools-reference#monitor-tool) configurations that start automatically when the plugin is active. See [Monitors](#monitors)                           | `"./monitors.json"`                                  |
| `userConfig`            | object                | User-configurable values prompted at enable time. See [User configuration](#user-configuration)                                                                               | See below                                            |
| `channels`              | array                 | Channel declarations for message injection (Telegram, Slack, Discord style). See [Channels](#channels)                                                                        | See below                                            |
| `dependencies`          | array                 | Other plugins this plugin requires, optionally with semver version constraints. See [Constrain plugin dependency versions](/docs/en/plugin-dependencies)                           | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Experimental components

Components under the `experimental` key, `themes` and `monitors`, have a manifest schema that may change between releases while they stabilize. Where you declare them is a separate migration: the top level still works, `claude plugin validate` warns, and a future release will require `experimental.*`.

### User configuration

The `userConfig` field declares values that Claude Code prompts the user for when the plugin is enabled. Use this instead of requiring users to hand-edit `settings.json`.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

Keys must be valid identifiers. Each option supports these fields:

| Field         | Required | Description                                                                              |
| :------------ | :------- | :--------------------------------------------------------------------------------------- |
| `type`        | Yes      | One of `string`, `number`, `boolean`, `directory`, or `file`                             |
| `title`       | Yes      | Label shown in the configuration dialog                                                  |
| `description` | Yes      | Help text shown beneath the field                                                        |
| `sensitive`   | No       | If `true`, masks input and stores the value in secure storage instead of `settings.json` |
| `required`    | No       | If `true`, validation fails when the field is empty                                      |
| `default`     | No       | Value used when the user provides nothing                                                |
| `multiple`    | No       | For `string` type, allow an array of strings                                             |
| `min` / `max` | No       | Bounds for `number` type                                                                 |

Each value is available for substitution as `${user_config.KEY}` in MCP and LSP server configs and hook commands. Non-sensitive values can also be substituted in skill and agent content. All values are exported to hook processes as `CLAUDE_PLUGIN_OPTION_<KEY>` environment variables, where `<KEY>` is the option key uppercased.

Fields that run in a shell reject `${user_config.*}`: substituting a configured value into a shell command would let the shell run whatever that value contains, so the component fails with an [error](/docs/en/errors#plugin-command-references-user-config) instead. Each rejected field has an alternative way to pass the value:

| Rejected field                                                               | How to pass the value                                                                                                             |
| :--------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| Shell-form hook commands                                                     | Use [exec form](/docs/en/hooks#exec-form-and-shell-form) with `args`, or read `CLAUDE_PLUGIN_OPTION_<KEY>` from the hook's environment |
| [Monitor](#monitors) commands                                                | Read the value from a config file in the script                                                                                   |
| MCP [`headersHelper`](/docs/en/mcp#use-dynamic-headers-for-custom-authentication) | Read the value from a config file in the script                                                                                   |

Before v2.1.207, these fields substituted `${user_config.KEY}` values; update plugins that relied on this.

Non-sensitive values are stored under the [`pluginConfigs`](/docs/en/settings-reference#pluginconfigs) key in your user `settings.json` as `pluginConfigs[<plugin-id>].options`.

On macOS, Claude Code stores sensitive values in the macOS Keychain, falling back to `~/.claude/.credentials.json` when the Keychain rejects the write. On platforms without a supported keychain, it stores them in `~/.claude/.credentials.json`. Keychain storage is shared with OAuth tokens and has an approximately 2 KB total limit, so keep sensitive values small.

Claude Code reads all `pluginConfigs` values from only three settings sources:

* **User settings**: `~/.claude/settings.json`, the file the enable-time prompt writes to
* **`--settings`**: the CLI flag or SDK inline settings
* **Managed settings**: [organization-controlled policy](/docs/en/permissions#managed-settings)

When more than one source sets the same key, managed settings take precedence, then `--settings`, then user settings. The only source you can remove from this list is user settings: pass [`--setting-sources`](/docs/en/cli-reference#cli-flags) without `user` and Claude Code skips them. Managed settings and `--settings` stay whatever you pass. The SDK's [`settingSources`](/docs/en/agent-sdk/claude-code-features#what-settingsources-does-not-control) option sets the same list.

Entries in a project's `.claude/settings.json` or `.claude/settings.local.json` are ignored. Both files live in the workspace, so a cloned repository could supply values there, and those values would flow into plugin hook commands, MCP server configs, LSP commands, and monitor commands. Before v2.1.207, these entries were read. The restriction is specific to `pluginConfigs`: [`enabledPlugins`](/docs/en/settings-reference#enabledplugins) still honors project and local settings.

### Channels

The `channels` field lets a plugin declare one or more message channels that inject content into the conversation. Each channel binds to an MCP server that the plugin provides.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

The `server` field is required and must match a key in the plugin's `mcpServers`. The optional per-channel `userConfig` uses the same schema as the top-level field, letting the plugin prompt for bot tokens or owner IDs when the plugin is enabled.

### Path behavior rules

Whether a custom path replaces or extends the plugin's default directory depends on the field:

* **Replaces the default**: `commands`, `agents`, `workflows`, `outputStyles`, `experimental.themes`, `experimental.monitors`. For example, when the manifest specifies `commands`, the default `commands/` directory is not scanned. To keep the default and add more, list it explicitly: `"commands": ["./commands/", "./extras/"]`
* **Adds to the default**: `skills`. The default `skills/` directory is always scanned, and directories listed in `skills` are loaded alongside it. Exception: for a [marketplace entry whose `source` resolves to the marketplace root](/docs/en/plugin-marketplaces#advanced-plugin-entries), declaring specific subdirectories replaces the default `skills/` scan
* **Own merge rules**: [hooks](#hooks), [MCP servers](#mcp-servers), and [LSP servers](#lsp-servers). See each section for how multiple sources combine

When a plugin has both a default folder and the matching manifest key, Claude Code warns about the ignored folder in `claude plugin list` and the `/plugin` detail view. The plugin still loads using the manifest paths. Claude Code doesn't warn when the manifest key points into the default folder, for example `"commands": ["./commands/deploy.md"]`, because that path names the folder explicitly.

For all path fields:

* All paths must be relative to the plugin root and start with `./`, except that the `skills` field also accepts `"."`
  * Both `"."` and `"./"` denote the plugin root itself
  * Before v2.1.221, `"."` failed manifest validation and the plugin didn't load, so use `"./"` to support earlier versions
* Components from custom paths use the same naming and namespacing rules
* Multiple paths can be specified as arrays
* A skill path can point to a directory that contains a `SKILL.md` directly, for example `"skills": ["."]` for the plugin root
  * Claude Code takes the skill's invocation name from the frontmatter `name` field in `SKILL.md`, so the name stays stable whatever the install directory is named
  * If `name` isn't set in the frontmatter, Claude Code falls back to the directory basename

A plugin that has a `SKILL.md` at its root, no `skills/` subdirectory, and no `skills` manifest field is automatically loaded as a single-skill plugin. You do not need to set `"skills": ["./"]` in `plugin.json` for this layout.

**Path examples**:

```json theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Environment variables

Claude Code provides three variables for referencing paths:

| Variable                | Resolves to                                                                                                 | Use it for                                                                                               |
| :---------------------- | :---------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------- |
| `${CLAUDE_PLUGIN_ROOT}` | Absolute path to the plugin's installation directory                                                        | Scripts, binaries, and config files bundled with the plugin                                              |
| `${CLAUDE_PLUGIN_DATA}` | [Persistent directory](#persistent-data-directory) that survives plugin updates, created on first reference | Installed dependencies such as `node_modules` or Python virtual environments, generated code, and caches |
| `${CLAUDE_PROJECT_DIR}` | The project root                                                                                            | Project-local scripts and config files                                                                   |

All three are exported as environment variables to hook processes and to MCP and LSP server subprocesses. Which fields substitute them inline depends on the plugin component:

| Plugin component                | Fields where placeholders resolve           |
| :------------------------------ | :------------------------------------------ |
| Skill and agent content         | Anywhere the placeholder appears            |
| Hook and monitor commands       | Anywhere the placeholder appears            |
| MCP `stdio` servers             | `command`, `args`, `env`                    |
| MCP `http`, `sse`, `ws` servers | `url`, `headers`, `headersHelper`           |
| LSP servers                     | `command`, `args`, `env`, `workspaceFolder` |

In hook commands, use [exec form](/docs/en/hooks#exec-form-and-shell-form) with `args` so each path is passed as one argument with no quoting. In shell-form hooks and monitor commands, wrap the variables in double quotes, as in `"${CLAUDE_PROJECT_DIR}/scripts/server.sh"`. This shell-form hook runs a script bundled with a plugin:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

`${CLAUDE_PLUGIN_ROOT}` changes when the plugin updates. The previous version's directory remains on disk for a grace period after an update, but treat it as ephemeral and don't write state there. See [plugin caching](#plugin-caching-and-file-resolution) for cleanup semantics.

When a plugin updates mid-session, hook commands, monitors, MCP servers, and LSP servers keep using the previous version's path. Run `/reload-plugins` to switch hooks, MCP servers, and LSP servers to the new path; monitors require a session restart. For a plugin with a `command` source, Claude Code [can reload the plugin itself](/docs/en/plugin-marketplaces#when-claude-code-re-runs-the-command).

MCP servers can also call the `roots/list` request to read the session's working directories at runtime. See [what `roots/list` returns and when Claude Code notifies the server of changes](/docs/en/mcp#option-3-add-a-local-stdio-server).

#### Persistent data directory

The `${CLAUDE_PLUGIN_DATA}` directory resolves to `~/.claude/plugins/data/{id}/`, where `{id}` is the plugin identifier with characters outside `a-z`, `A-Z`, `0-9`, `_`, and `-` replaced by `-`. For a plugin installed as `formatter@my-marketplace`, the directory is `~/.claude/plugins/data/formatter-my-marketplace/`.

A common use is installing language dependencies once and reusing them across sessions and plugin updates. Use it for Python dependencies, dependencies locked with Yarn or pnpm, and packages whose lifecycle scripts must run. For a marketplace-installed plugin, you may not need it at all: Claude Code installs eligible [Node.js package dependencies](#node-js-package-dependencies) automatically when it caches the plugin.

Because the data directory outlives any single plugin version, a check for directory existence alone cannot detect when an update changes the plugin's dependency manifest. The recommended pattern compares the bundled manifest against a copy in the data directory and reinstalls when they differ.

This `SessionStart` hook installs `node_modules` on the first run and again whenever a plugin update includes a changed `package.json`:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

The `diff` exits nonzero when the stored copy is missing or differs from the bundled one, covering both first run and dependency-changing updates. If `npm install` fails, the trailing `rm` removes the copied manifest so the next session retries.

Scripts bundled in `${CLAUDE_PLUGIN_ROOT}` can then run against the persisted `node_modules`:

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

The data directory is deleted automatically when you uninstall the plugin from the last scope where it is installed. The `/plugin` interface shows the directory size and prompts before deleting. The CLI deletes by default; pass [`--keep-data`](#plugin-uninstall) to preserve it.

***

## Plugin caching and file resolution

Plugins are specified in one of two ways:

* Through `claude --plugin-dir` or `claude --plugin-url`, for the duration of a session.
* Through a marketplace, installed for future sessions.

For security and verification purposes, Claude Code copies *marketplace* plugins to the user's local **plugin cache** (`~/.claude/plugins/cache`) rather than using them in place, except for [`command` sources in link mode](/docs/en/plugin-marketplaces#copy-mode-and-link-mode), which Claude Code uses in place through links in the cache entry.

For copied plugins, each installed version is a separate directory in the cache, grouped by marketplace and plugin and named for the resolved version, with its own copy of the plugin's files and [Node.js package dependencies](#node-js-package-dependencies). A dependency resolved from a [release tag](/docs/en/plugin-dependencies#tag-plugin-releases-for-version-resolution) gets a directory name with a commit-SHA suffix.

When you update or uninstall a plugin, Claude Code marks the previous version directory as orphaned and removes it in a background sweep roughly 14 days later. The grace period lets concurrent Claude Code sessions that already loaded the old version keep running without errors. Claude Code runs the sweep only while at least one plugin is installed; after you uninstall your last plugin, orphaned directories stay on disk until you install a plugin again.

Claude Code removes a plugin or marketplace folder from the cache only when it no longer contains any directory or symlink. If you symlink a development checkout into the cache as a plugin's version entry, Claude Code never marks the link as orphaned and never removes it or the folders that hold it. Claude Code also never writes its version-tracking files inside the linked checkout.

Claude's Glob and Grep tools skip orphaned version directories during searches, so file results don't include outdated plugin code.

### Node.js package dependencies

When Claude Code copies a plugin into the cache, it also installs the plugin's Node.js package dependencies there, so the plugin's hooks and MCP servers can load them. This section covers the npm and Bun packages a plugin declares in its own `package.json`. For plugins that depend on other plugins, see [plugin dependency versions](/docs/en/plugin-dependencies).

Claude Code runs the install inside the copied version directory each time it creates one: when you install a plugin, when Claude Code updates a plugin to a new version, and at session start when an enabled plugin isn't cached yet, such as on a new machine. The install runs only when the plugin's root directory contains both a `package.json` and a supported lockfile:

| Lockfile                                     | Command                                          |
| :------------------------------------------- | :----------------------------------------------- |
| `bun.lock` or `bun.lockb`                    | `bun install --frozen-lockfile --ignore-scripts` |
| `npm-shrinkwrap.json` or `package-lock.json` | `npm ci --ignore-scripts`                        |

If a plugin contains more than one of these lockfiles, Claude Code uses the first match, checking in order: `bun.lock`, `bun.lockb`, `npm-shrinkwrap.json`, `package-lock.json`. Claude Code skips `yarn.lock` and `pnpm-lock.yaml` because Yarn and pnpm support resolution-time configuration hooks that bypass `--ignore-scripts`.

Ship an npm lockfile for the widest reach. Claude Code runs the matched lockfile's package manager from the user's PATH and doesn't fall back to the other lockfile if it's missing. For a plugin distributed through an npm source, use `npm-shrinkwrap.json`; npm excludes `package-lock.json` from published packages.

Claude Code constrains this dependency install so that no code from the plugin or its packages executes during it, and bounds how long it can run:

* **Frozen resolution:** Bun and npm install exactly what the lockfile pins, and fail rather than re-resolve versions when `package.json` and the lockfile disagree.
* **No lifecycle scripts:** `--ignore-scripts` keeps `preinstall`, `install`, and `postinstall` scripts from running, so dependencies that build native modules in those scripts download but don't compile during this install.
* **60-second timeout:** Claude Code stops an install that runs longer and treats it as failed.

Fetching an npm-source plugin itself runs `npm install` with lifecycle scripts enabled, before this dependency install runs.

A failed or skipped install never blocks the plugin. When the install fails, or Claude Code skips a yarn or pnpm lockfile, it records the reason as a warning in [debug output](#debugging-commands). A plugin with a `package.json` and no lockfile is skipped without a log entry. A timed-out install can leave a partial `node_modules` tree in the cached copy.

You can't turn the automatic install off; no setting or environment variable disables it. In restricted networks, see the [network access requirements](/docs/en/network-config#network-access-requirements) for the hosts to allow.

For dependencies the automatic install can't provide, such as packages that need their lifecycle scripts to build, Python dependencies, or a plugin locked with Yarn or pnpm, install them from a hook into the [persistent data directory](#persistent-data-directory).

### Path traversal limitations

Claude Code doesn't let a plugin reference files outside its own directory. It rejects a component path that resolves outside the plugin root, such as `../shared-utils`, whether the path is declared in `plugin.json` or in a [marketplace entry](/docs/en/plugin-marketplaces#plugin-entries). Claude Code reports a [`path escapes plugin directory`](/docs/en/errors#path-escapes-plugin-directory) error and loads the plugin without that component.

Claude Code also doesn't copy files outside the plugin directory into the cache when it installs the plugin, so when a script inside a copied plugin reads a path above the plugin root, it doesn't find those files either.

### Share files within a marketplace with symlinks

If your plugin needs to share files with other parts of the same marketplace, you can create symbolic links inside your plugin directory. How a symlink is handled when the plugin is copied into the cache depends on where its target resolves:

* **Within the plugin's own directory:** the symlink is preserved as a relative symlink in the cache, so it keeps resolving to the copied target at runtime.
* **Elsewhere within the same marketplace:** the symlink is dereferenced. The target's content is copied into the cache in its place. This lets a meta-plugin's `skills/` directory link to skills defined by other plugins in the marketplace.
* **Outside the marketplace:** the symlink is skipped for security. This prevents plugins from pulling arbitrary host files such as system paths into the cache.

For plugins installed with `--plugin-dir`, from a local path, or from a [`command` source](/docs/en/plugin-marketplaces#copy-mode-and-link-mode) in copy mode, only symlinks that resolve within the plugin's own directory are preserved. All others are skipped.

The following command creates a link from inside a marketplace plugin to a shared skill defined by a sibling plugin. On Windows, use `mklink /D` from an elevated Command Prompt or enable Developer Mode:

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

***

## Plugin directory structure

### Standard plugin layout

A complete plugin follows this structure:

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Metadata directory (optional)
│   └── plugin.json             # plugin manifest
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills as flat .md files
│   ├── status.md
│   └── logs.md
├── agents/                   # Subagent definitions
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── workflows/                # Workflow scripts
│   └── release-audit.js
├── output-styles/            # Output style definitions
│   └── terse.md
├── themes/                   # Color theme definitions
│   └── dracula.json
├── monitors/                 # Background monitor configurations
│   └── monitors.json
├── hooks/                    # Hook configurations
│   ├── hooks.json           # Main hook config
│   └── security-hooks.json  # Additional hooks
├── bin/                      # Plugin executables added to PATH
│   └── my-tool               # Invokable as bare command in Bash tool
├── settings.json            # Default settings for the plugin
├── .mcp.json                # MCP server definitions
├── .lsp.json                # LSP server configurations
├── scripts/                 # Hook and utility scripts
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # License file
└── CHANGELOG.md             # Version history
```

<Warning>
  The `.claude-plugin/` directory contains the `plugin.json` file. All other directories (commands/, agents/, skills/, workflows/, output-styles/, themes/, monitors/, hooks/) must be at the plugin root, not inside `.claude-plugin/`.
</Warning>

A `CLAUDE.md` file at the plugin root is not loaded as project context. Plugins contribute context through skills, agents, and hooks rather than CLAUDE.md. To ship instructions that load into Claude's context, put them in a [skill](#skills).

### File locations reference

| Component         | Default Location             | Purpose                                                                                                                                                                                                                                                                                    |
| :---------------- | :--------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**      | `.claude-plugin/plugin.json` | Plugin metadata and configuration (optional)                                                                                                                                                                                                                                               |
| **Skills**        | `skills/`                    | Skills with `<name>/SKILL.md` structure                                                                                                                                                                                                                                                    |
| **Commands**      | `commands/`                  | Skills as flat Markdown files. Use `skills/` for new plugins                                                                                                                                                                                                                               |
| **Agents**        | `agents/`                    | Subagent Markdown files                                                                                                                                                                                                                                                                    |
| **Workflows**     | `workflows/`                 | [Workflow](/docs/en/workflows) script files                                                                                                                                                                                                                                                     |
| **Output styles** | `output-styles/`             | Output style definitions                                                                                                                                                                                                                                                                   |
| **Themes**        | `themes/`                    | Color theme definitions                                                                                                                                                                                                                                                                    |
| **Hooks**         | `hooks/hooks.json`           | Hook configuration                                                                                                                                                                                                                                                                         |
| **MCP servers**   | `.mcp.json`                  | MCP server definitions                                                                                                                                                                                                                                                                     |
| **LSP servers**   | `.lsp.json`                  | Language server configurations                                                                                                                                                                                                                                                             |
| **Monitors**      | `monitors/monitors.json`     | Background monitor configurations                                                                                                                                                                                                                                                          |
| **Executables**   | `bin/`                       | Executables added to the Bash tool's `PATH` and invokable as bare commands while the plugin is enabled. You can't include this directory in a plugin you [distribute through claude.ai organization settings](/docs/en/plugin-marketplaces#keep-executables-out-of-the-top-level-bin-directory) |
| **Settings**      | `settings.json`              | Default configuration applied when the plugin is enabled. Only the [`agent`](/docs/en/sub-agents) and [`subagentStatusLine`](/docs/en/statusline#subagent-status-lines) keys are supported                                                                                                           |

***

## CLI commands reference

Claude Code provides CLI commands for non-interactive plugin management, useful for scripting and automation.

### plugin init

Scaffold a new plugin at `~/.claude/skills/<name>/`. On the next Claude Code session it loads automatically as `<name>@skills-dir` and appears in `/plugin` and `claude plugin list` with no install step.

See [Skills-directory plugins](#skills-directory-plugins) for scope and trust requirements.

```bash theme={null}
claude plugin init <name> [options]
```

**Arguments:**

* `<name>`: Plugin name. Becomes the skill namespace and the directory name under `~/.claude/skills/`, so it cannot contain spaces or path separators.

**Options:**

| Option                   | Description                                                                                                         | Default                 |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------ | :---------------------- |
| `--description <text>`   | Manifest description                                                                                                |                         |
| `--author <name>`        | Author name                                                                                                         | `git config user.name`  |
| `--author-email <email>` | Author email                                                                                                        | `git config user.email` |
| `--with <components...>` | Also scaffold component folders. Valid values: `skills`, `agents`, `hooks`, `mcp`, `lsp`, `output-style`, `channel` |                         |
| `-f, --force`            | Overwrite an existing `.claude-plugin/` at the target                                                               |                         |
| `-h, --help`             | Display help for command                                                                                            |                         |

**Aliases:** `new`

Each `--with` value adds a starter file for that component, ready to edit:

| Component      | What it scaffolds                                                                                         |
| :------------- | :-------------------------------------------------------------------------------------------------------- |
| `skills`       | An extra namespaced `<name>:example` skill alongside the default one                                      |
| `agents`       | An `agents/` subagent definition                                                                          |
| `hooks`        | A `hooks/hooks.json` with a sample event handler                                                          |
| `mcp`          | A `.mcp.json` with HTTP and stdio server examples                                                         |
| `lsp`          | A `.lsp.json` language-server example                                                                     |
| `output-style` | An `output-styles/<name>.md` that applies automatically while the plugin is enabled                       |
| `channel`      | An MCP-based [channel](/docs/en/channels): a stdio server (`server.ts`), its `.mcp.json`, and a `package.json` |

The scaffolded plugin uses the `@skills-dir` source rather than a marketplace. Admins can block this source with `strictKnownMarketplaces` or by adding `{"source": "skills-dir"}` to `blockedMarketplaces` in [managed settings](/docs/en/plugin-marketplaces#managed-marketplace-restrictions). When blocked, `plugin init` fails before writing.

**Examples:**

```bash theme={null}
# Scaffold a minimal plugin
claude plugin init my-helper

# Scaffold with skill and hook folders
claude plugin init my-helper --with skills hooks

# Overwrite an existing scaffold
claude plugin init my-helper --force
```

### plugin install

Install a plugin from available marketplaces.

```bash theme={null}
claude plugin install <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name` for a specific marketplace

**Options:**

| Option                 | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Default |
| :--------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `-s, --scope <scope>`  | Installation scope: `user`, `project`, or `local`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `user`  |
| `--config <key=value>` | Set a [`userConfig`](#user-configuration) option declared in the plugin's manifest. Repeat the flag to set multiple options                                                                                                                                                                                                                                                                                                                                                                                                                                           |         |
| `-y, --yes`            | Accept a command the plugin's marketplace declares, without the confirmation prompt: the command that produces a plugin with a [`command` source](/docs/en/plugin-marketplaces#command-sources), or the [`headersHelper`](/docs/en/plugin-marketplaces#authenticate-archive-downloads) that authenticates an archive download. Accepting a `headersHelper` requires Claude Code v2.1.238 or later. Claude Code still prints the command first. Required when stdin or stdout isn't a TTY. Has no effect inside a Claude Code session, so run the command from your own terminal |         |
| `-h, --help`           | Display help for command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |         |

Scope determines which settings file the installed plugin is added to. For example, `--scope project` writes to `enabledPlugins` in .claude/settings.json, making the plugin available to everyone who clones the project repository.

**Examples:**

```bash theme={null}
# Install to user scope (default)
claude plugin install formatter@my-marketplace

# Install to project scope (shared with team)
claude plugin install formatter@my-marketplace --scope project

# Install to local scope (not shared with team)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Remove an installed plugin.

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                                                                              | Default |
| :-------------------- | :------------------------------------------------------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Uninstall from scope: `user`, `project`, or `local`                                                      | `user`  |
| `--keep-data`         | Preserve the plugin's [persistent data directory](#persistent-data-directory)                            |         |
| `--prune`             | Also remove auto-installed dependencies that no other plugin requires. See [plugin prune](#plugin-prune) |         |
| `-y, --yes`           | Skip the `--prune` confirmation prompt. Required when stdin or stdout is not a TTY                       |         |
| `-h, --help`          | Display help for command                                                                                 |         |

**Aliases:** `remove`, `rm`

By default, uninstalling from the last remaining scope also deletes the plugin's `${CLAUDE_PLUGIN_DATA}` directory. Use `--keep-data` to preserve it, for example when reinstalling after testing a new version.

<Note>
  When installed plugins from different marketplaces share a name, the `plugin-name@marketplace-name` form uninstalls only the plugin from the named marketplace. Before v2.1.212, the qualified form could match and uninstall the same-named plugin from a different marketplace.
</Note>

### plugin prune

Remove auto-installed plugin dependencies that are no longer required by any installed plugin. Dependencies that Claude Code pulled in to satisfy another plugin's [`dependencies`](/docs/en/plugin-dependencies) field are removed; plugins you installed directly are never touched.

```bash theme={null}
claude plugin prune [options]
```

**Options:**

| Option                | Description                                                              | Default |
| :-------------------- | :----------------------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Prune at scope: `user`, `project`, or `local`                            | `user`  |
| `--dry-run`           | List what would be removed without removing anything                     |         |
| `-y, --yes`           | Skip the confirmation prompt. Required when stdin or stdout is not a TTY |         |
| `-h, --help`          | Display help for command                                                 |         |

**Aliases:** `autoremove`

The command lists orphaned dependencies and asks for confirmation before removing them. To remove a plugin and clean up its dependencies in one step, run `claude plugin uninstall <plugin> --prune`.

### plugin enable

Enable a disabled plugin. When the target is installed from a marketplace and declares [dependencies](/docs/en/plugin-dependencies), Claude Code enables them transitively at the same scope. The command fails under the conditions that [Enable or disable a plugin with dependencies](/docs/en/plugin-dependencies#enable-or-disable-a-plugin-with-dependencies) lists.

```bash theme={null}
claude plugin enable <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                                                                                               | Default     |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------ | :---------- |
| `-s, --scope <scope>` | Scope to enable: `user`, `project`, or `local`. When omitted, Claude Code detects the scope where the plugin is installed | Auto-detect |
| `-h, --help`          | Display help for command                                                                                                  |             |

### plugin disable

Disable a plugin without uninstalling it. When the target is installed from a marketplace, the command fails if another enabled plugin [depends on](/docs/en/plugin-dependencies#enable-or-disable-a-plugin-with-dependencies) it. The error message includes a chained command that disables every dependent first.

```bash theme={null}
claude plugin disable [plugin] [options]
```

**Arguments:**

* `[plugin]`: Plugin name or `plugin-name@marketplace-name`. Optional when using `--all`

**Options:**

| Option                | Description                                                                                                                | Default     |
| :-------------------- | :------------------------------------------------------------------------------------------------------------------------- | :---------- |
| `-a, --all`           | Disable all enabled plugins. Can't be combined with `--scope`                                                              |             |
| `-s, --scope <scope>` | Scope to disable: `user`, `project`, or `local`. When omitted, Claude Code detects the scope where the plugin is installed | Auto-detect |
| `-h, --help`          | Display help for command                                                                                                   |             |

### plugin update

Update a plugin to the latest version.

```bash theme={null}
claude plugin update <plugin> [options]
```

**Arguments:**

* `<plugin>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Default |
| :-------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------ |
| `-s, --scope <scope>` | Scope to update: `user`, `project`, `local`, or `managed`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `user`  |
| `-y, --yes`           | Accept a command the plugin's marketplace declares, without the confirmation prompt: the command that produces a plugin with a [`command` source](/docs/en/plugin-marketplaces#command-sources), or the [`headersHelper`](/docs/en/plugin-marketplaces#authenticate-archive-downloads) that authenticates an archive download. Accepting a `headersHelper` requires Claude Code v2.1.238 or later. Claude Code still prints the command first. Required when stdin or stdout isn't a TTY. Has no effect inside a Claude Code session, so run the command from your own terminal |         |
| `-h, --help`          | Display help for command                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |         |

<Note>
  Claude Code resolves a bare plugin name against your installed plugins. When installed plugins from different marketplaces share the name, Claude Code refuses the update and lists the qualified `plugin-name@marketplace-name` commands to run instead. Before v2.1.246, Claude Code accepted only the qualified form and rejected a bare name as not found.
</Note>

***

### plugin list

List installed plugins with their version, source marketplace, and enable status.

```bash theme={null}
claude plugin list [options]
```

**Options:**

| Option        | Description                                                    | Default |
| :------------ | :------------------------------------------------------------- | :------ |
| `--json`      | Output as JSON                                                 |         |
| `--available` | Include available plugins from marketplaces. Requires `--json` |         |
| `-h, --help`  | Display help for command                                       |         |

Within an interactive session, `/plugin list` prints a similar listing inline, but it covers marketplace-installed plugins only:

* Plugins loaded from skills directories appear in the `/plugin` interface and in `claude plugin list`, but not in the inline `/plugin list` output.
* On Claude Code v2.1.239 or later, [plugins synced from claude.ai](#synced-plugins) appear in `claude plugin list` when you run it in the environment where a synced session downloaded them. They don't appear in the inline `/plugin list` output.
* Plugins loaded for the session with `--plugin-dir` or `--plugin-url` appear in the `/plugin` interface, and in `claude plugin list` only when the same flag precedes the subcommand, as in `claude --plugin-dir <dir> plugin list`. Only the flag names their location, so a bare `claude plugin list` can't find them, unlike synced plugins and skills-directory plugins, whose fixed directories Claude Code scans.

The interactive form accepts `--enabled` or `--disabled` to show only plugins in that state, and `ls` as a shorthand for `list`.

### plugin details

Show a plugin's component inventory and projected token cost. The output lists all components the plugin contributes, grouped as Skills, Agents, Hooks, MCP servers, and LSP servers, along with an estimate of how many tokens it adds to each session. The Skills group includes both `skills/` and `commands/` entries.

```bash theme={null}
claude plugin details <name>
```

**Arguments:**

* `<name>`: Plugin name or `plugin-name@marketplace-name`

**Options:**

| Option       | Description              | Default |
| :----------- | :----------------------- | :------ |
| `-h, --help` | Display help for command |         |

The output shows two cost figures for each component:

* **Always-on:** tokens added to every session by the plugin's listing text, such as skill descriptions, agent descriptions, and command names, regardless of whether any component fires.
* **On-invoke:** tokens a component costs when it fires. Shown per component, not as a plugin total, because a typical session invokes only a subset of components.

This example shows what the output looks like for a plugin with two skills:

```
dependency-guard 1.2.0
  Dependency analysis for Claude Code sessions
  Source: dependency-guard@example-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  SessionStart  (harness-only — no model context cost)
  MCP servers (0)
  LSP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

The always-on total is computed via the `count_tokens` API for your active model. Per-component numbers are proportionally scaled from that total. If the API is unreachable, the command falls back to a character-based estimate.

### plugin validate

Check a plugin or a marketplace for syntax and schema errors before publishing.

The command exits 0 when validation passes, 1 when it fails, and 2 when the validation run itself fails, such as when the path you pass is unreadable.

```bash theme={null}
claude plugin validate <path> [options]
```

**Arguments:**

* `<path>`: Path to a plugin directory or a marketplace directory. See [Validate a plugin or a directory without a manifest](/docs/en/plugin-marketplaces#validate-a-plugin-or-a-directory-without-a-manifest) for which files a plugin run covers.

**Options:**

| Option       | Description                                                                                                                                       | Default |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------ | :------ |
| `--strict`   | Treat warnings as errors and exit 1 on them. Use in CI to catch issues the runtime tolerates, such as [unrecognized fields](#unrecognized-fields) |         |
| `--json`     | Output the validation report as one JSON object with the same exit codes. Requires Claude Code v2.1.259 or later                                  |         |
| `-h, --help` | Display help for command                                                                                                                          |         |

With `--json`, Claude Code writes the report to stdout as one JSON object with these top-level fields:

* `success`: the same verdict the exit code gives
* `strict`: whether the run treated warnings as errors
* `target`: the resolved path Claude Code validated
* `manifest`: the manifest's own result, or `null` for a [run without a manifest](/docs/en/plugin-marketplaces#validate-a-plugin-or-a-directory-without-a-manifest)
* `contents`: per-file results, each naming its `file` and carrying `errors`, `warnings`, and `notes` arrays

On exit 2, the command writes nothing to stdout; the error message goes to stderr.

Within an interactive session, `/plugin validate <path>` runs the same checks inline.

### plugin tag

Create a release git tag for a plugin. By default the command tags the plugin in the current directory; pass a path to tag a plugin elsewhere. See [Tag plugin releases](/docs/en/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```bash theme={null}
claude plugin tag [path] [options]
```

**Arguments:**

* `[path]`: Path to the plugin directory. Defaults to the current directory.

**Options:**

| Option                | Description                                                                | Default  |
| :-------------------- | :------------------------------------------------------------------------- | :------- |
| `--push`              | Push the tag to the remote after creating it                               |          |
| `--dry-run`           | Print what would be tagged without creating the tag                        |          |
| `-f, --force`         | Create the tag even if the working tree is dirty or the tag already exists |          |
| `-m, --message <msg>` | Tag annotation message. Use `%s` as a placeholder for the version          |          |
| `--remote <name>`     | Remote to push to with `--push`                                            | `origin` |
| `-h, --help`          | Display help for command                                                   |          |

***

## Debugging and development tools

### Debugging commands

Use `claude --debug` to see plugin loading details:

This shows:

* Which plugins are being loaded
* Any errors in plugin manifests
* Skill, agent, and hook registration
* MCP server initialization

### Common issues

| Issue                               | Cause                           | Solution                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| :---------------------------------- | :------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plugin not loading                  | Invalid `plugin.json`           | Run `claude plugin validate ./my-plugin` or `/plugin validate ./my-plugin`, where `./my-plugin` is your plugin directory, to check `plugin.json`, `hooks/hooks.json`, and the frontmatter of the skills, agents, and commands in the plugin's default directories for syntax and schema errors. See [Validate a plugin or a directory without a manifest](/docs/en/plugin-marketplaces#validate-a-plugin-or-a-directory-without-a-manifest) for what a run covers |
| Skills not appearing                | Wrong directory structure       | Ensure `skills/` or `commands/` is at the plugin root, not inside `.claude-plugin/`                                                                                                                                                                                                                                                                                                                                                                          |
| Hooks not firing                    | Script not executable           | Run `chmod +x script.sh`                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| MCP server fails                    | Missing `${CLAUDE_PLUGIN_ROOT}` | Use variable for all plugin paths                                                                                                                                                                                                                                                                                                                                                                                                                            |
| Path errors                         | Absolute paths used             | Make paths relative, starting with `./`; see [Path behavior rules](#path-behavior-rules), which cover the `skills` field's `"."` exception                                                                                                                                                                                                                                                                                                                   |
| LSP `Executable not found in $PATH` | Language server not installed   | Install the binary (e.g., `npm install -g typescript-language-server typescript`)                                                                                                                                                                                                                                                                                                                                                                            |

### Example error messages

**Manifest validation errors**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: check for missing commas, extra commas, or unquoted strings
* `Plugin <name> has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Invalid input: expected string, received undefined`: a required field is missing
* `Plugin <name> has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON syntax error. Before v2.1.246, Claude Code also produced this error for a `plugin.json` saved as UTF-8 with a leading byte-order mark (BOM), even when the JSON was otherwise valid.

**Plugin loading errors**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: command path exists but contains no valid command files
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: the `source` path in marketplace.json points to a non-existent directory
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: remove duplicate component definitions or remove `strict: false` in marketplace entry

### Hook troubleshooting

**Hook script not executing**:

1. Check the script is executable: `chmod +x ./scripts/your-script.sh`
2. Verify the shebang line: First line should be `#!/bin/bash` or `#!/usr/bin/env bash`
3. Check the path uses `${CLAUDE_PLUGIN_ROOT}`: `"command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/your-script.sh"`
4. Test the script manually: `./scripts/your-script.sh`

**Hook not triggering on expected events**:

1. Verify the event name is correct (case-sensitive): `PostToolUse`, not `postToolUse`
2. Check the matcher pattern matches your tools: `"matcher": "Write|Edit"` for file operations
3. Confirm the hook type is valid: `command`, `http`, `mcp_tool`, `prompt`, or `agent`

### MCP server troubleshooting

**Server not starting**:

1. Check the command exists and is executable
2. Verify all paths use `${CLAUDE_PLUGIN_ROOT}` variable
3. Check the MCP server logs: `claude --debug` shows initialization errors
4. Test the server manually outside of Claude Code

**Server tools not appearing**:

1. Ensure the server is properly configured in `.mcp.json` or `plugin.json`
2. Verify the server implements the MCP protocol correctly
3. Check for connection timeouts in debug output

### Directory structure mistakes

**Symptoms**: Plugin loads but components (skills, agents, hooks) are missing.

**Correct structure**: Components must be at the plugin root, not inside `.claude-plugin/`. Only `plugin.json` belongs in `.claude-plugin/`.

**Debug checklist**:

1. Run `claude --debug` and look for "loading plugin" messages
2. Check that each component directory is listed in the debug output
3. Verify file permissions allow reading the plugin files

***

## Distribution and versioning reference

### Version management

Claude Code uses the plugin's version as the cache key that determines whether an update is available. When you run `/plugin update` or auto-update fires, Claude Code computes the current version and skips the update if it matches what's already installed.

For every source type except `command`, Claude Code resolves the version from the first of these that is set:

1. The `version` field in the plugin's `plugin.json`
2. The `version` field in the plugin's marketplace entry in `marketplace.json`
3. The git commit SHA of the plugin's source, for `github`, `url`, `git-subdir`, and relative-path sources in a git-hosted marketplace
4. The SHA-256 digest, for [`archive` sources](/docs/en/plugin-marketplaces#zip-archives): the `sha256` pin in the marketplace entry, or the digest of the downloaded file when you set no pin. Claude Code shortens it to the first 12 characters
5. `unknown`, for `npm` sources or local directories not inside a git repository

For a [`command` source](/docs/en/plugin-marketplaces#command-sources), Claude Code always derives the version from what the command produced: a 12-character content hash on its own, or appended to the `plugin.json` version as `<version>-<hash>` when one is set. Claude Code ignores the marketplace entry's `version` field for command sources. A command whose hashed output changes therefore produces a new version, even when the authored version string stays the same. In [link mode](/docs/en/plugin-marketplaces#copy-mode-and-link-mode), the hash covers the printed directory's real path and its top-level entries rather than the file contents.

For those source types, this gives you three ways to version a plugin:

| Approach               | How                                                                                                                                  | Update behavior                                                                                                                                                      | Best for                                                                 |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------- |
| **Explicit version**   | Set `"version": "2.1.0"` in `plugin.json`                                                                                            | Users get updates only when you bump this field. Pushing new commits without bumping it has no effect, and `/plugin update` reports "already at the latest version". | Published plugins with stable release cycles                             |
| **Commit-SHA version** | Omit `version` from both `plugin.json` and the marketplace entry                                                                     | Users get updates whenever the source's resolved commit changes                                                                                                      | Internal or team plugins under active development                        |
| **Digest version**     | Use an [`archive` source](/docs/en/plugin-marketplaces#zip-archives) and omit `version` from both `plugin.json` and the marketplace entry | With a `sha256` pin, users get updates when you change the pin. Without one, users get updates whenever the hosted zip file's bytes change                           | Plugins published as zip files to a static server or artifact repository |

If you use explicit versions, follow [semantic versioning](https://semver.org) (`MAJOR.MINOR.PATCH`): bump MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes. Document changes in a `CHANGELOG.md`.

***

## See also

* [Plugins](/docs/en/plugins) - Tutorials and practical usage
* [Plugin marketplaces](/docs/en/plugin-marketplaces) - Creating and managing marketplaces
* [Skills](/docs/en/skills) - Skill development details
* [Subagents](/docs/en/sub-agents) - Agent configuration and capabilities
* [Hooks](/docs/en/hooks) - Event handling and automation
* [MCP](/docs/en/mcp) - External tool integration
* [Settings](/docs/en/settings) - Configuration options for plugins
