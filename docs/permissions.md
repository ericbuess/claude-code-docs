> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure permissions

> Control what Claude Code can access and do with fine-grained permission rules, modes, and managed policies.

Claude Code supports fine-grained permissions so that you can specify exactly what the agent is allowed to do and what it cannot. Permission settings can be checked into version control and distributed to all developers in your organization, as well as customized by individual developers.

## Permission system

Claude Code uses a tiered permission system to balance power and safety:

| Tool type         | Example          | Approval required | "Yes, don't ask again" behavior               |
| :---------------- | :--------------- | :---------------- | :-------------------------------------------- |
| Read-only         | File reads, Grep | No                | N/A                                           |
| Bash commands     | Shell execution  | Yes               | Permanently per project directory and command |
| File modification | Edit/write files | Yes               | Until session end                             |

## Manage permissions

You can view and manage Claude Code's tool permissions with `/permissions`. This UI lists all permission rules and the settings.json file they are sourced from.

* **Allow** rules let Claude Code use the specified tool without manual approval.
* **Ask** rules prompt for confirmation whenever Claude Code tries to use the specified tool.
* **Deny** rules prevent Claude Code from using the specified tool.

Rules are evaluated in order: **deny -> ask -> allow**. The first matching rule wins, so deny rules always take precedence.

## Permission modes

Claude Code supports several permission modes that control how tools are approved. Set the `defaultMode` in your [settings files](/en/settings#settings-files):

| Mode                | Description                                                                                                                                                                                                                                                  |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Standard behavior: prompts for permission on first use of each tool                                                                                                                                                                                          |
| `acceptEdits`       | Automatically accepts file edit permissions for the session                                                                                                                                                                                                  |
| `plan`              | Plan Mode: Claude can analyze but not modify files or execute commands                                                                                                                                                                                       |
| `delegate`          | Coordination-only mode for agent team leads. Restricts the lead to team management tools, so all implementation work happens through teammates. Only available when an agent team is active. See [delegate mode](/en/agent-teams#delegate-mode) for details. |
| `dontAsk`           | Auto-denies tools unless pre-approved via `/permissions` or `permissions.allow` rules                                                                                                                                                                        |
| `bypassPermissions` | Skips all permission prompts (requires safe environment, see warning below)                                                                                                                                                                                  |

<Warning>
  `bypassPermissions` mode disables all permission checks. Only use this in isolated environments like containers or VMs where Claude Code cannot cause damage. Administrators can prevent this mode by setting `disableBypassPermissionsMode` to `"disable"` in [managed settings](#managed-settings).
</Warning>

## Permission rule syntax

Permission rules follow the format `Tool` or `Tool(specifier)`.

### Match all uses of a tool

To match all uses of a tool, use just the tool name without parentheses:

| Rule       | Effect                         |
| :--------- | :----------------------------- |
| `Bash`     | Matches all Bash commands      |
| `WebFetch` | Matches all web fetch requests |
| `Read`     | Matches all file reads         |

`Bash(*)` is equivalent to `Bash` and matches all Bash commands.

### Use specifiers for fine-grained control

Add a specifier in parentheses to match specific tool uses:

| Rule                           | Effect                                                   |
| :----------------------------- | :------------------------------------------------------- |
| `Bash(npm run build)`          | Matches the exact command `npm run build`                |
| `Read(./.env)`                 | Matches reading the `.env` file in the current directory |
| `WebFetch(domain:example.com)` | Matches fetch requests to example.com                    |

### Wildcard patterns

Bash rules support glob patterns with `*`. Wildcards can appear at any position in the command. This configuration allows npm and git commit commands while blocking git push:

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

The space before `*` matters: `Bash(ls *)` matches `ls -la` but not `lsof`, while `Bash(ls*)` matches both. The legacy `:*` suffix syntax is equivalent to ` *` but is deprecated.

## Tool-specific permission rules

### Bash

Bash permission rules support wildcard matching with `*`. Wildcards can appear at any position in the command, including at the beginning, middle, or end:

* `Bash(npm run build)` matches the exact Bash command `npm run build`
* `Bash(npm run test *)` matches Bash commands starting with `npm run test`
* `Bash(npm *)` matches any command starting with `npm `
* `Bash(* install)` matches any command ending with ` install`
* `Bash(git * main)` matches commands like `git checkout main`, `git merge main`

When `*` appears at the end with a space before it (like `Bash(ls *)`), it enforces a word boundary, requiring the prefix to be followed by a space or end-of-string. For example, `Bash(ls *)` matches `ls -la` but not `lsof`. In contrast, `Bash(ls*)` without a space matches both `ls -la` and `lsof` because there's no word boundary constraint.

<Tip>
  Claude Code is aware of shell operators (like `&&`) so a prefix match rule like `Bash(safe-cmd *)` won't give it permission to run the command `safe-cmd && other-cmd`.
</Tip>

<Warning>
  Bash permission patterns that try to constrain command arguments are fragile. For example, `Bash(curl http://github.com/ *)` intends to restrict curl to GitHub URLs, but won't match variations like:

  * Options before URL: `curl -X GET http://github.com/...`
  * Different protocol: `curl https://github.com/...`
  * Redirects: `curl -L http://bit.ly/xyz` (redirects to github)
  * Variables: `URL=http://github.com && curl $URL`
  * Extra spaces: `curl  http://github.com`

  For more reliable URL filtering, consider:

  * **Restrict Bash network tools**: use deny rules to block `curl`, `wget`, and similar commands, then use the WebFetch tool with `WebFetch(domain:github.com)` permission for allowed domains
  * **Use PreToolUse hooks**: implement a hook that validates URLs in Bash commands and blocks disallowed domains
  * Instructing Claude Code about your allowed curl patterns via CLAUDE.md

  Note that using WebFetch alone does not prevent network access. If Bash is allowed, Claude can still use `curl`, `wget`, or other tools to reach any URL.
</Warning>

### Read and Edit

`Edit` rules apply to all built-in tools that edit files. Claude makes a best-effort attempt to apply `Read` rules to all built-in tools that read files like Grep and Glob.

Read and Edit rules both follow the [gitignore](https://git-scm.com/docs/gitignore) specification with four distinct pattern types:

| Pattern            | Meaning                                | Example                          | Matches                            |
| ------------------ | -------------------------------------- | -------------------------------- | ---------------------------------- |
| `//path`           | **Absolute** path from filesystem root | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`          |
| `~/path`           | Path from **home** directory           | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf`     |
| `/path`            | Path **relative to settings file**     | `Edit(/src/**/*.ts)`             | `<settings file path>/src/**/*.ts` |
| `path` or `./path` | Path **relative to current directory** | `Read(*.env)`                    | `<cwd>/*.env`                      |

<Warning>
  A pattern like `/Users/alice/file` is NOT an absolute path. It's relative to your settings file. Use `//Users/alice/file` for absolute paths.
</Warning>

Examples:

* `Edit(/docs/**)`: edits in `<project>/docs/` (NOT `/docs/`)
* `Read(~/.zshrc)`: reads your home directory's `.zshrc`
* `Edit(//tmp/scratch.txt)`: edits the absolute path `/tmp/scratch.txt`
* `Read(src/**)`: reads from `<current-directory>/src/`

<Note>
  In gitignore patterns, `*` matches files in a single directory while `**` matches recursively across directories. To allow all file access, use just the tool name without parentheses: `Read`, `Edit`, or `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` matches fetch requests to example.com

### MCP

* `mcp__puppeteer` matches any tool provided by the `puppeteer` server (name configured in Claude Code)
* `mcp__puppeteer__*` wildcard syntax that also matches all tools from the `puppeteer` server
* `mcp__puppeteer__puppeteer_navigate` matches the `puppeteer_navigate` tool provided by the `puppeteer` server

### Task (subagents)

Use `Task(AgentName)` rules to control which [subagents](/en/sub-agents) Claude can use:

* `Task(Explore)` matches the Explore subagent
* `Task(Plan)` matches the Plan subagent
* `Task(my-custom-agent)` matches a custom subagent named `my-custom-agent`

Add these rules to the `deny` array in your settings or use the `--disallowedTools` CLI flag to disable specific agents. To disable the Explore agent:

```json  theme={null}
{
  "permissions": {
    "deny": ["Task(Explore)"]
  }
}
```

## Extend permissions with hooks

[Claude Code hooks](/en/hooks-guide) provide a way to register custom shell commands to perform permission evaluation at runtime. When Claude Code makes a tool call, PreToolUse hooks run before the permission system, and the hook output can determine whether to approve or deny the tool call in place of the permission system.

## Working directories

By default, Claude has access to files in the directory where it was launched. You can extend this access:

* **During startup**: use `--add-dir <path>` CLI argument
* **During session**: use `/add-dir` command
* **Persistent configuration**: add to `additionalDirectories` in [settings files](/en/settings#settings-files)

Files in additional directories follow the same permission rules as the original working directory: they become readable without prompts, and file editing permissions follow the current permission mode.

## How permissions interact with sandboxing

Permissions and [sandboxing](/en/sandboxing) are complementary security layers:

* **Permissions** control which tools Claude Code can use and which files or domains it can access. They apply to all tools (Bash, Read, Edit, WebFetch, MCP, and others).
* **Sandboxing** provides OS-level enforcement that restricts the Bash tool's filesystem and network access. It applies only to Bash commands and their child processes.

Use both for defense-in-depth:

* Permission deny rules block Claude from even attempting to access restricted resources
* Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude's decision-making
* Filesystem restrictions in the sandbox use Read and Edit deny rules, not separate sandbox configuration
* Network restrictions combine WebFetch permission rules with the sandbox's `allowedDomains` list

## Managed settings

For organizations that need centralized control over Claude Code configuration, administrators can deploy `managed-settings.json` files to system directories. These policy files follow the same format as regular settings files and cannot be overridden by user or project settings. For organizations without device management infrastructure, [server-managed settings](/en/server-managed-settings) provide an alternative that delivers configurations from Anthropic's servers.

**Managed settings file locations**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux and WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

<Note>
  These are system-wide paths (not user home directories like `~/Library/...`) that require administrator privileges. They are designed to be deployed by IT administrators.
</Note>

### Managed-only settings

Some settings are only effective in managed settings:

| Setting                           | Description                                                                                                                                        |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`    | Set to `"disable"` to prevent `bypassPermissions` mode and the `--dangerously-skip-permissions` flag                                               |
| `allowManagedPermissionRulesOnly` | When `true`, prevents user and project settings from defining `allow`, `ask`, or `deny` permission rules. Only rules in managed settings apply     |
| `allowManagedHooksOnly`           | When `true`, prevents loading of user, project, and plugin hooks. Only managed hooks and SDK hooks are allowed                                     |
| `strictKnownMarketplaces`         | Controls which plugin marketplaces users can add. See [managed marketplace restrictions](/en/plugin-marketplaces#managed-marketplace-restrictions) |

## Settings precedence

Permission rules follow the same [settings precedence](/en/settings#settings-precedence) as all other Claude Code settings: managed settings have the highest precedence, followed by command line arguments, local project, shared project, and user settings.

If a permission is allowed in user settings but denied in project settings, the project setting takes precedence and the permission is blocked.

## Example configurations

This [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) includes starter settings configurations for common deployment scenarios. Use these as starting points and adjust them to fit your needs.

## See also

* [Settings](/en/settings): complete configuration reference including the permission settings table
* [Sandboxing](/en/sandboxing): OS-level filesystem and network isolation for Bash commands
* [Authentication](/en/authentication): set up user access to Claude Code
* [Security](/en/security): security safeguards and best practices
* [Hooks](/en/hooks-guide): automate workflows and extend permission evaluation
