> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configure permissions

> Control what Claude Code can access and do with fine-grained permission rules, modes, and managed policies.

Claude Code supports fine-grained permissions so that you can specify exactly what the agent is allowed to do and what it can't. Permission settings can be checked into version control and distributed to all developers in your organization, as well as customized by individual developers.

## Permission system

Claude Code uses a tiered permission system to balance power and safety:

| Tool type         | Example          | Approval required                                                                   | "Yes, don't ask again" behavior        |
| :---------------- | :--------------- | :---------------------------------------------------------------------------------- | :------------------------------------- |
| Read-only         | File reads, Grep | No, within the [working directory and additional directories](#working-directories) | N/A                                    |
| Bash commands     | Shell execution  | Yes, except a built-in set of [read-only commands](#read-only-commands)             | Permanently per repository and command |
| File modification | Edit/write files | Yes                                                                                 | Until session end                      |

When you choose "Yes, don't ask again" and the approval saves permanently, such as for a Bash command, Claude Code saves the rule to `.claude/settings.local.json` at the root of the git repository, resolved through [worktrees](/en/worktrees) to the main checkout. The rule applies to future sessions anywhere in that repository, including sessions started in subdirectories and in worktrees. A file-modification approval isn't saved to the file: as the table shows, it lasts until the session ends. Outside a git repository, and when the repository root is your home directory, Claude Code saves the rule in the directory you started it from.

Before v2.1.211, Claude Code always saved the rule in the starting directory, so an approval granted in a worktree or subdirectory didn't apply to the rest of the repository. Rules that earlier versions saved in a subdirectory or worktree still apply to sessions started there.

On a Bash or PowerShell permission prompt, press `Ctrl+E` to show an explanation of the command: what it does, why Claude is running it, and what could go wrong, labeled **Low risk**, **Med risk**, or **High risk**. Claude Code sends the command and Claude's own description of the call to the model to generate the explanation only when you press `Ctrl+E`, not on every prompt. Showing the explanation doesn't run the command; press `Ctrl+E` again to hide it.

To turn the shortcut off, set [`permissionExplainerEnabled`](/en/settings#global-config-settings) to `false` in `~/.claude.json`.

## Manage permissions

You can view and manage Claude Code's tool permissions with `/permissions`. This UI lists all permission rules and the `settings.json` file each rule comes from.

* **Allow** rules let Claude Code use the specified tool without manual approval.
* **Ask** rules prompt for confirmation whenever Claude Code tries to use the specified tool.
* **Deny** rules prevent Claude Code from using the specified tool.

Rules are evaluated in order: deny, then ask, then allow. The first match in that order determines the outcome, and rule specificity doesn't change the order.

A broad deny rule like `Bash(aws *)` blocks every matching call, including calls that also match a narrower allow rule like `Bash(aws s3 ls)`, so a deny rule can't carry allowlist exceptions. The same precedence applies between ask and allow: a matching ask rule prompts even when a more specific allow rule also matches the same call.

Deny rules behave differently depending on whether they name a tool or scope a pattern within one. A bare tool name like `Bash` removes the tool from Claude's context entirely, so Claude never sees it. A scoped rule like `Bash(rm *)` leaves the tool available and blocks matching calls when Claude attempts them.

<Note>
  Permission rules are enforced by Claude Code, not by the model. Instructions in your prompt or `CLAUDE.md` shape what Claude tries to do, but they don't change what Claude Code allows. To grant or revoke access, use `/permissions`, the rules described here, a [permission mode](/en/permission-modes), or a [PreToolUse hook](#extend-permissions-with-hooks).
</Note>

## Permission modes

Claude Code supports several permission modes that control how it approves tool calls. See [Permission modes](/en/permission-modes) for when to use each one. Set the `defaultMode` in your [settings files](/en/settings#settings-files):

| Mode                | Description                                                                                                                                                                                                                                                                                                                                                           |
| :------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Standard behavior: prompts for permission on first use of each tool. {/* min-version: 2.1.200 */}Labeled Manual in the CLI, the VS Code and JetBrains extensions, and the desktop app, and Claude Code accepts `manual` as an alias. The label and alias require Claude Code v2.1.200 or later. The desktop app's label doesn't depend on your CLI version            |
| `acceptEdits`       | Automatically accepts file edits and common filesystem commands such as `mkdir`, `touch`, `mv`, and `cp` for paths in the working directory or `additionalDirectories`                                                                                                                                                                                                |
| `plan`              | Claude reads files and runs read-only shell commands to explore but doesn't edit your source files. Labeled Plan in the CLI and the VS Code extension                                                                                                                                                                                                                 |
| `auto`              | Auto-approves tool calls with background safety checks that verify actions align with your request                                                                                                                                                                                                                                                                    |
| `dontAsk`           | Auto-denies tools unless pre-approved via `/permissions` or `permissions.allow` rules. `AskUserQuestion`, connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools), and MCP tools marked [`requiresUserInteraction`](/en/mcp#require-approval-for-a-specific-tool) are denied even if you've allowed them                   |
| `bypassPermissions` | Skips permission prompts, except those forced by explicit `ask` rules, connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools), and MCP tools marked [`requiresUserInteraction`](/en/mcp#require-approval-for-a-specific-tool). Root and home directory removals such as `rm -rf /` also still prompt as a circuit breaker |

<Warning>
  `bypassPermissions` mode skips permission prompts, including for writes to `.git`, `.config/git`, `.claude`, `.vscode`, `.idea`, `.husky`, `.cargo`, `.devcontainer`, `.yarn`, and `.mvn`. Only use this mode in isolated environments like containers or VMs where Claude Code can't cause damage.

  A few prompts still fire in this mode. Explicit `ask` rules, connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools), and MCP tools marked [`requiresUserInteraction`](/en/mcp#require-approval-for-a-specific-tool) still prompt. Removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, also prompt as a circuit breaker against model error, {/* min-version: 2.1.208 */}including when the command contains command substitution with `$(...)` or backticks, or process substitution with `<(...)`. Before v2.1.208, only the plain form, such as `rm -rf ~` typed as its own command, prompted; commands that reached the removal through a substitution didn't.
</Warning>

To prevent `bypassPermissions` or `auto` mode from being used, set `permissions.disableBypassPermissionsMode` or `permissions.disableAutoMode` to `"disable"` in any [settings file](/en/settings#settings-files). These are most useful in [managed settings](#managed-settings) where they can't be overridden.

## Permission rule syntax

Permission rules follow the format `Tool` or `Tool(specifier)`.

### Match all uses of a tool

To match all uses of a tool, use only the tool name without parentheses:

| Rule       | Effect                         |
| :--------- | :----------------------------- |
| `Bash`     | Matches all Bash commands      |
| `WebFetch` | Matches all web fetch requests |
| `Read`     | Matches all file reads         |

`Bash(*)` is equivalent to `Bash` and matches all Bash commands. As a deny rule, both forms remove the tool from Claude's context.

### Use specifiers for fine-grained control

Add a specifier in parentheses to match specific tool uses:

| Rule                           | Effect                                                   |
| :----------------------------- | :------------------------------------------------------- |
| `Bash(npm run build)`          | Matches the exact command `npm run build`                |
| `Read(./.env)`                 | Matches reading the `.env` file in the current directory |
| `WebFetch(domain:example.com)` | Matches fetch requests to example.com                    |

### Match by input parameter

Deny and ask rules can match a top-level input parameter on any tool with `Tool(param:value)`. The rule matches when Claude calls the tool with that parameter set to that exact value. An allow rule for one parameter value wouldn't establish that the call is safe overall, so allow rules continue to use each tool's own specifier syntax. This works for any scalar parameter the tool accepts:

| Rule                           | Matches                                      |
| :----------------------------- | :------------------------------------------- |
| `Agent(model:opus)`            | Agent calls that request the Opus model tier |
| `Agent(isolation:worktree)`    | Agent calls that request a git worktree      |
| `Bash(run_in_background:true)` | Bash calls that run in the background        |

Parameter matching follows these rules:

* The parameter name must be a direct field of the tool's input, such as `model` on the Agent tool. Fields nested inside an object or array are not matchable
* Each rule names one parameter. To gate on both `model` and `isolation`, write two rules, `Agent(model:opus)` and `Agent(isolation:worktree)`, rather than combining them in one rule
* The value supports `*` as a wildcard that matches any sequence of characters, so `Agent(isolation:*)` matches any explicit isolation value. Without `*` the match is exact
* A parameter the model omits is never matched, so `Agent(model:*)` doesn't match a call that leaves `model` unset
* The value is compared against the literal input Claude sends, before any normalization. `Agent(model:opus)` matches the alias `opus` but not a full model ID. Run with [`--verbose`](/en/cli-reference) to see the exact parameter names and values in each tool call
* Whitespace around the colon is ignored

Fields that a tool already matches with its own canonicalizing rules are not matchable this way: `command` for Bash and PowerShell, `file_path` for Read, Edit, and Write, `path` for Grep and Glob, `notebook_path` for NotebookEdit, and `url` for WebFetch. A rule like `Bash(command:rm *)` would be bypassable by a compound command, so Claude Code ignores it and emits a startup warning. Use `Bash(rm *)`, `Read(./path)`, or `WebFetch(domain:host)` instead.

### Wildcard patterns

Bash rules support glob patterns with `*`. Wildcards can appear at any position in the command. This configuration allows npm and git commit commands while blocking git push:

```json theme={null}
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

The space before `*` matters: `Bash(ls *)` matches `ls -la` but not `lsof`, while `Bash(ls*)` matches both. The `:*` suffix is an equivalent way to write a trailing wildcard, so `Bash(ls:*)` matches the same commands as `Bash(ls *)`.

The permission dialog writes the space-separated form when you select "Yes, don't ask again" for a command prefix. The `:*` form is only recognized at the end of a pattern. In a pattern like `Bash(git:* push)`, the colon is treated as a literal character and won't match git commands.

### Tool name wildcards

Deny and ask rules also accept glob patterns in the tool-name position. The pattern must match the full tool name: `"*"` matches every tool, and `"mcp__*"` matches every MCP tool across all servers. A tool matched by a bare-name glob deny rule is removed from Claude's context, the same as a bare tool name. This configuration denies every MCP tool:

```json theme={null}
{
  "permissions": {
    "deny": [
      "mcp__*"
    ]
  }
}
```

Allow rules accept tool-name globs only after a literal `mcp__<server>__` prefix. The server segment must be glob-free so the rule names a specific server you configured. `mcp__puppeteer__*` matches every tool from the `puppeteer` server, and `mcp__github__get_*` matches its `get_` tools. An unanchored allow glob such as `"*"`, `"B*"`, or `"mcp__*"` is skipped with a warning and doesn't auto-approve anything.

A deny or ask rule whose tool name matches no known tool produces a startup warning to catch typos. Tool names containing `_` or `*` are exempt from the check.

The label shown for a tool in the transcript and permission dialog can differ from its canonical name. For example, the tool labeled `Stop Task` in the transcript has the canonical name `TaskStop`. Permission rules and [hook matchers](/en/hooks) match the canonical name only, so a rule written as `Stop Task` doesn't match. For deny and ask rules, the startup warning above catches the mismatch. Use the canonical names listed in the [tools reference](/en/tools-reference).

## Tool-specific permission rules

### Bash

Bash permission rules support wildcard matching with `*`. Wildcards can appear at any position in the command, including at the beginning, middle, or end:

* `Bash(npm run build)` matches the exact Bash command `npm run build`
* `Bash(npm run test *)` matches Bash commands starting with `npm run test`
* `Bash(npm *)` matches any command starting with `npm `
* `Bash(* install)` matches any command ending with ` install`
* `Bash(git * main)` matches commands like `git checkout main` and `git log --oneline main`

A single `*` matches any sequence of characters including spaces, so one wildcard can span multiple arguments. `Bash(git *)` matches `git log --oneline --all`, and `Bash(git * main)` matches `git push origin main` as well as `git merge main`.

When `*` appears at the end with a space before it (like `Bash(ls *)`), it enforces a word boundary, requiring the prefix to be followed by a space or end-of-string. For example, `Bash(ls *)` matches `ls -la` but not `lsof`. In contrast, `Bash(ls*)` without a space matches both `ls -la` and `lsof` because there's no word boundary constraint.

#### Compound commands

<Tip>
  Claude Code is aware of shell operators, so a rule like `Bash(safe-cmd *)` won't give it permission to run the command `safe-cmd && other-cmd`. The recognized command separators are `&&`, `||`, `;`, `|`, `|&`, `&`, and newlines. A rule must match each subcommand independently.
</Tip>

When you approve a compound command with "Yes, don't ask again", Claude Code saves a separate rule for each subcommand that requires approval, rather than a single rule for the full compound string. For example, approving `git status && npm test` saves a rule for `npm test`, so future `npm test` invocations are recognized regardless of what precedes the `&&`. Subcommands like `cd` into a subdirectory generate their own Read rule for that path. Up to 5 rules may be saved for a single compound command.

#### Process wrappers

Before matching Bash rules, Claude Code strips a fixed set of process wrappers so a rule like `Bash(npm test *)` also matches `timeout 30 npm test`. The recognized wrappers are `timeout`, `time`, `nice`, `nohup`, and `stdbuf`.

Bare `xargs` is also stripped, so `Bash(grep *)` matches `xargs grep pattern`. Stripping applies only when `xargs` has no flags: an invocation like `xargs -n1 grep pattern` is matched as an `xargs` command, so rules written for the inner command do not cover it.

This wrapper list is built in and is not configurable. Development environment runners such as `direnv exec`, `devbox run`, `mise exec`, `npx`, and `docker exec` are not in the list. Because these tools execute their arguments as a command, a rule like `Bash(devbox run *)` matches whatever comes after `run`, including `devbox run rm -rf .`. To approve work inside an environment runner, write a specific rule that includes both the runner and the inner command, such as `Bash(devbox run npm test)`. Add one rule per inner command you want to allow.

Exec wrappers such as `watch`, `setsid`, `ionice`, and `flock` always prompt and can't be auto-approved by a prefix rule like `Bash(watch *)`. The same applies to `find` with `-exec` or `-delete`: a `Bash(find *)` rule doesn't cover these forms. To approve a specific invocation, write an exact-match rule for the full command string.

#### Read-only commands

Claude Code recognizes a built-in set of Bash commands as read-only and runs them without a permission prompt in every mode. These include `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd`, and read-only forms of `git`. The set is not configurable; to require a prompt for one of these commands, add an `ask` or `deny` rule for it.

Unquoted glob patterns are permitted for commands whose every flag is read-only, so `ls *.ts` and `wc -l src/*.py` run without a prompt. Commands with write-capable or exec-capable flags, such as `find`, `sort`, `sed`, and `git`, still prompt when an unquoted glob is present because the glob could expand to a flag like `-delete`.

A `cd` into a path inside your working directory or an [additional directory](#working-directories) is also read-only. A compound command like `cd packages/api && ls` runs without a prompt when each part qualifies on its own. Combining `cd` with `git` in one compound command prompts when the `cd` changes into a different directory, since running `git` in a new directory can execute that directory's hooks. A `cd` whose target resolves to the current working directory is a no-op and doesn't trigger this prompt.

Combining `cd` with an output redirect in one compound command also prompts when Claude Code can't determine which directory the redirect target resolves against after the `cd` runs. A command whose only redirect target is `/dev/null`, such as `cd app; grep -r pattern . 2>/dev/null`, doesn't trigger this prompt, because `/dev/null` doesn't depend on the working directory. {/* min-version: 2.1.207 */}Before v2.1.207, a compound command containing `cd` prompted for any output redirect, including one whose only target was `/dev/null`.

<Warning>
  Bash permission patterns that try to constrain command arguments are fragile. For example, `Bash(curl http://github.com/ *)` intends to restrict curl to GitHub URLs, but won't match variations like:

  * Options before URL: `curl -X GET http://github.com/...`
  * Different protocol: `curl https://github.com/...`
  * Redirects: `curl -L http://short.example.com/xyz`, which redirects to GitHub
  * Variables: `URL=http://github.com && curl $URL`
  * Extra spaces: `curl  http://github.com`

  For more reliable URL filtering, consider:

  * **Restrict Bash network tools**: use deny rules to block `curl`, `wget`, and similar commands, then use the WebFetch tool with `WebFetch(domain:github.com)` permission for allowed domains
  * **Use PreToolUse hooks**: implement a hook that validates URLs in Bash commands and blocks disallowed domains
  * **Add CLAUDE.md guidance**: describe your allowed curl patterns in `CLAUDE.md`. This shapes what Claude tries but doesn't enforce a boundary, so pair it with one of the options above

  Note that using WebFetch alone doesn't prevent network access. If Bash is allowed, Claude can still use `curl`, `wget`, or other tools to reach any URL.
</Warning>

### PowerShell

PowerShell permission rules use the same shape as Bash rules. Wildcards with `*` match at any position, the `:*` suffix is equivalent to a trailing ` *`, and a bare `PowerShell` or `PowerShell(*)` matches every command. This configuration allows `Get-ChildItem` and `git commit` commands while blocking `Remove-Item`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Common aliases are canonicalized before matching. A rule written for the cmdlet name also matches its aliases, so `PowerShell(Get-ChildItem *)` matches `gci`, `ls`, and `dir` as well. Matching is case-insensitive.

Claude Code parses the PowerShell AST and checks each command in a compound command independently. Pipeline operators `|`, statement separators `;`, and on PowerShell 7+ the chain operators `&&` and `||` split a compound command into subcommands. A rule must match every subcommand for the compound command to be allowed.

### Read and Edit

`Edit` rules apply to all built-in tools that edit files. Claude makes a best-effort attempt to apply `Read` rules to all built-in tools that read files like Grep and Glob, to `@file` mentions in your prompts, and to the selection and open-file context that a connected [IDE](/en/vs-code#the-built-in-ide-mcp-server) shares with Claude.

{/* min-version: 2.1.208 */}A `Read` deny rule also blocks the [Edit tool](/en/errors#file-is-covered-by-a-read-deny-rule) on the same path, including creating a new file there. Write and NotebookEdit aren't covered, so add an `Edit` deny rule for paths no tool may change. Requires Claude Code v2.1.208 or later.

{/* min-version: 2.1.210 */}The file permission checks match only `Edit(path)` and `Read(path)` rules. A `Write(path)`, `NotebookEdit(path)`, or `Glob(path)` rule is accepted but never matched by those checks, so Claude Code warns at startup for each allow, deny, or ask rule in one of these unmatched forms. Use `Edit(docs/**)` in place of `Write(docs/**)` or `NotebookEdit(docs/**)`, and `Read(docs/**)` in place of `Glob(docs/**)`. A tool-name rule with no path, such as a deny rule for `Write`, isn't affected: it matches the tool everywhere and produces no warning. Requires Claude Code v2.1.210 or later.

A deny rule `Write(docs/**)` in project settings produces this startup warning:

```text theme={null}
Permission deny rule (.claude/settings.json): Write(docs/**) is not matched by file permission checks — only Edit(path) rules are. Use Edit(docs/**) instead (Edit rules cover all file-editing tools).
```

<Warning>
  Read and Edit deny rules apply to Claude's built-in file tools and to file commands Claude Code recognizes in Bash, such as `cat`, `head`, `tail`, and `sed`. They don't apply to arbitrary subprocesses that read or write files indirectly, like a Python or Node script that opens files itself. For OS-level enforcement that blocks all processes from accessing a path, [enable the sandbox](/en/sandboxing).
</Warning>

Read and Edit rules both follow the [gitignore](https://git-scm.com/docs/gitignore) specification with four distinct pattern types:

| Pattern            | Meaning                              | Example                          | Matches                                          |
| ------------------ | ------------------------------------ | -------------------------------- | ------------------------------------------------ |
| `//path`           | Absolute path from filesystem root   | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`                        |
| `~/path`           | Path from home directory             | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf`                   |
| `/path`            | Path relative to the settings source | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts` in project settings |
| `path` or `./path` | Path relative to current directory   | `Read(*.env)`                    | `<cwd>/*.env`                                    |

<Warning>
  A pattern like `/Users/alice/file` isn't an absolute path. The single leading slash anchors at the settings source, not the filesystem root. Use `//Users/alice/file` for absolute paths.
</Warning>

A `/path` pattern anchors at a directory associated with the settings source that defines it, so the same rule matches different locations depending on where you put it:

| Rule defined in                                 | `/path` resolves to        |
| :---------------------------------------------- | :------------------------- |
| Project settings at `.claude/settings.json`     | `<project root>/path`      |
| Local settings at `.claude/settings.local.json` | `<original cwd>/path`      |
| User settings at `~/.claude/settings.json`      | `~/.claude/path`           |
| A file passed with `--settings <file>`          | `<directory of file>/path` |
| CLI flags, `/permissions`, or session rules     | `<original cwd>/path`      |

Local settings rules anchor at the directory you started Claude Code from, not at the repository root where Claude Code [stores the file](#permission-system) in v2.1.211 and later. In a session started at the repository root, the two directories are the same; in a [worktree](/en/worktrees) session, a shared rule such as `Edit(/src/**)` matches that worktree's own `src/` directory.

A deny rule such as `Read(/secrets/**)` in user settings blocks `~/.claude/secrets/**`, not a `secrets` directory in your project. To write a rule in user settings that applies inside every project, use a `//` absolute path or a `~/` home-relative path instead.

On Windows, paths are normalized to POSIX form before matching. `C:\Users\alice` becomes `/c/Users/alice`, so use `//c/**/.env` to match `.env` files anywhere on that drive. To match across all drives, use `//**/.env`.

Examples:

* `Edit(/docs/**)`: edits in `<project>/docs/`, not `/docs/` or `<project>/.claude/docs/`
* `Read(~/.zshrc)`: reads your home directory's `.zshrc`
* `Edit(//tmp/scratch.txt)`: edits the absolute path `/tmp/scratch.txt`
* `Read(src/**)`: reads from `<current-directory>/src/`

A rule only matches files under its anchor, so the anchor determines how far a deny rule reaches. Bare filenames follow gitignore semantics and match at any depth, so `Read(.env)` and `Read(**/.env)` are equivalent:

| Deny rule                       | Blocks                                       | Does not block                                       |
| ------------------------------- | -------------------------------------------- | ---------------------------------------------------- |
| `Read(.env)` or `Read(**/.env)` | any `.env` at or under the current directory | `.env` in a parent directory or another project      |
| `Read(//**/.env)`               | any `.env` anywhere on the filesystem        | nothing; the rule is anchored at the filesystem root |

<Note>
  In gitignore patterns, `*` matches within a single path segment and can appear at any position in the pattern, while `**` matches across directories. To allow all file access, use only the tool name without parentheses: `Read`, `Edit`, or `Write`.
</Note>

When you approve a file path with "Yes, don't ask again", Claude Code escapes gitignore pattern characters in that path, such as `[`, `]`, and `*`, so the generated rule matches only the literal path you approved. Rules you write yourself aren't escaped. Before v2.1.202, Claude Code saved the path unescaped, so a generated rule for a directory named `[2024-06] Reports` could fail to match its own path or match unintended sibling directories.

When Claude accesses a symlink, permission rules check two paths: the symlink itself and the file it resolves to. Allow and deny rules treat that pair differently: allow rules fall back to prompting you, while deny rules block outright.

* **Allow rules**: apply only when both the symlink path and its target match. A symlink inside an allowed directory that points outside it still prompts you.
* **Deny rules**: apply when either the symlink path or its target matches. A symlink that points to a denied file is itself denied.

For example, with `Read(./project/**)` allowed and `Read(~/.ssh/**)` denied, a symlink at `./project/key` pointing to `~/.ssh/id_rsa` is blocked: the target fails the allow rule and matches the deny rule.

### WebFetch

WebFetch rules use a `domain:` prefix and match against the hostname of the requested URL. Matching is case-insensitive, supports `*` wildcards, and strips a trailing `.` from both the rule and the hostname so `example.com.` and `example.com` are treated the same.

* `WebFetch(domain:example.com)` matches requests to `example.com`
* `WebFetch(domain:*.example.com)` matches any subdomain at any depth, such as `api.example.com` or `a.b.example.com`, but not `example.com` itself
* `WebFetch(domain:*)` matches every domain and is equivalent to a bare `WebFetch` rule

In any position other than a leading `*.` or a bare `*`, the wildcard matches only the text between two dots. `WebFetch(domain:example.*)` matches `example.org`, where `*` becomes `org`, but not `example.evil.com`, where `*` would have to become `evil.com` and cross a dot. This keeps a trailing wildcard from matching domains an attacker could register.

### MCP

MCP rules use the server name as configured in Claude Code, optionally followed by the name of a tool from that server.

* `mcp__puppeteer` matches any tool provided by the `puppeteer` server
* `mcp__puppeteer__*` uses wildcard syntax and also matches all tools from the `puppeteer` server
* `mcp__puppeteer__puppeteer_navigate` matches the `puppeteer_navigate` tool provided by the `puppeteer` server

If your organization has set a [claude.ai connector](/en/mcp#organization-controls-on-connector-tools) tool to `ask`, allow rules for that tool don't take effect: Claude Code prompts on every call, even in `auto` and `bypassPermissions` modes. In `dontAsk` mode, which never prompts, Claude Code denies the call instead. Connector tools appear as `mcp__claude_ai_<server>__<tool>`.

### Agent (subagents)

Use `Agent(AgentName)` rules to control which [subagents](/en/sub-agents) Claude can use:

* `Agent(Explore)` matches the Explore subagent
* `Agent(Plan)` matches the Plan subagent
* `Agent(my-custom-agent)` matches a custom subagent named `my-custom-agent`

Add these rules to the `deny` array in your settings or use the `--disallowedTools` CLI flag to disable specific agents. To disable the Explore agent:

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

### Cd

`Cd` rules control which directories the [`/cd` command](/en/commands) can move the session to. `Cd` is not a model-invocable tool: Claude can't call it, and the rules apply only when you run `/cd` yourself.

A bare `Cd` deny rule disables `/cd` entirely. A `Cd(<path-pattern>)` deny rule blocks matching targets. Deny rules check every spelling of the target, including each symlink hop it resolves through, so a rule written for one path also blocks targets that resolve to it.

Adding any `Cd` allow rule switches `/cd` to allowlist mode: the resolved target directory must match one of your allow rules, or `/cd` refuses. With no `Cd` rules configured, `/cd` keeps its default behavior and prompts you to trust an unfamiliar directory.

Path patterns share the `//`, `~/`, and `/` anchors from [Read and Edit rules](#read-and-edit), but matching is anchored to the whole directory path rather than gitignore-style. `*` matches exactly one path segment and `**` matches across segments. A trailing `/**` also matches its named root.

| Rule                  | Matches                                   | Does not match               |
| --------------------- | ----------------------------------------- | ---------------------------- |
| `Cd(~/code/*)`        | `~/code/app`                              | `~/code/app/src`, `~/code`   |
| `Cd(~/code/**)`       | `~/code` and any directory under it       | directories outside `~/code` |
| `Cd(**/node_modules)` | any `node_modules` directory at any depth | `node_modules/pkg`           |

## Extend permissions with hooks

[Claude Code hooks](/en/hooks-guide) provide a way to register custom shell commands to perform permission evaluation at runtime. When Claude Code makes a tool call, PreToolUse hooks run before the permission prompt. The hook output can deny the tool call, force a prompt, or skip the prompt to let the call proceed.

Hook decisions don't bypass permission rules. Claude Code evaluates deny and ask rules regardless of what a PreToolUse hook returns: a matching deny rule blocks the call, and a matching ask rule still prompts even when the hook returned `"allow"` or `"ask"`. This preserves the deny-first precedence described in [Manage permissions](#manage-permissions), including deny rules set in managed settings.

Connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools) and MCP tools marked [`requiresUserInteraction`](/en/mcp#require-approval-for-a-specific-tool) also still prompt when a hook returns `"allow"`.

A blocking hook also takes precedence over allow rules. A hook that exits with code 2 stops the tool call before permission rules are evaluated, so the block applies even when an allow rule would otherwise let the call proceed. To run all Bash commands without prompts except for a few you want blocked, add `"Bash"` to your allow list and register a PreToolUse hook that rejects those specific commands. See [Block edits to protected files](/en/hooks-guide#block-edits-to-protected-files) for a hook script you can adapt.

## Working directories

By default, Claude has access to files in the directory where you launched it. You can extend this access:

* **During startup**: use `--add-dir <path>` CLI argument
* **During session**: use `/add-dir` command
* **Persistent configuration**: add to `additionalDirectories` in [settings files](/en/settings#settings-files)

Files in additional directories follow the same permission rules as the original working directory: they become readable without prompts, and file editing permissions follow the current permission mode.

In background sessions on macOS, the session host requests access to protected folders such as `~/Desktop`, `~/Documents`, and `~/Downloads` separately from your terminal when Claude needs to read or write files there; if reads there fail with `Operation not permitted`, see [how to grant folder access to background sessions](/en/agent-view#background-sessions-can’t-read-desktop-documents-or-downloads-on-macos).

To change the session's primary working directory instead of adding another, use [`/cd`](/en/commands). The `/cd` command requires Claude Code v2.1.169 or later. Unlike `/add-dir`, it relocates the session: the new directory's `CLAUDE.md` is loaded and `--resume` finds the session from there.

### Additional directories grant file access, not configuration

Adding a directory extends where Claude can read and edit files. It doesn't make that directory a full configuration root: most `.claude/` configuration is not discovered from additional directories, though a few types are loaded as exceptions.

These exceptions apply only to directories added with the `--add-dir` flag or the `/add-dir` command. Directories listed in `permissions.additionalDirectories` in a settings file grant file access only and don't load any of the configuration below.

The following configuration types are loaded from `--add-dir` directories:

| Configuration                                                                         | Loaded from `--add-dir`                                                                                                                                            |
| :------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Skills](/en/skills) in `.claude/skills/`                                             | Yes, with live reload                                                                                                                                              |
| [Subagents](/en/sub-agents) in `.claude/agents/`                                      | Yes                                                                                                                                                                |
| [Settings](/en/settings) in `.claude/settings.json` and `.claude/settings.local.json` | `enabledPlugins` and `extraKnownMarketplaces` keys only                                                                                                            |
| [CLAUDE.md](/en/memory) files, `.claude/rules/`, and `CLAUDE.local.md`                | Only when `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` is set. `CLAUDE.local.md` additionally requires the `local` setting source, which is enabled by default |

Claude Code discovers commands and output styles from the current working directory and its parents, your user directory at `~/.claude/`, and managed settings. Hooks and other `.claude/settings.json` keys load from the current working directory's `.claude/` folder with no parent-directory fallback, alongside your user `~/.claude/settings.json` and managed settings. {/* min-version: 2.1.211 */}`.claude/settings.local.json` loads from the git repository root instead, even when you start Claude Code in a subdirectory; before v2.1.211, it too loaded only from the current working directory. [Agent SDK](/en/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources) sessions load it from the working directory in all versions.

To share that configuration across projects, use one of these approaches:

* **User-level configuration**: place files in `~/.claude/agents/`, `~/.claude/output-styles/`, or `~/.claude/settings.json` to make them available in every project
* **Plugins**: package and distribute configuration as a [plugin](/en/plugins) that teams can install
* **Launch from the config directory**: run Claude Code from the directory containing the `.claude/` configuration you want

## How permissions interact with sandboxing

Permissions and [sandboxing](/en/sandboxing) are complementary security layers:

* **Permissions** control which tools Claude Code can use and which files or domains it can access. They apply to all tools, including Bash, Read, Edit, WebFetch, and MCP.
* **Sandboxing** provides OS-level enforcement that restricts the Bash tool's filesystem and network access. It applies only to Bash commands and their child processes.

Use both for defense-in-depth:

* Permission deny rules block Claude from even attempting to access restricted resources
* Sandbox restrictions prevent Bash commands from reaching resources outside defined boundaries, even if a prompt injection bypasses Claude's decision-making
* Filesystem restrictions in the sandbox combine the [`sandbox.filesystem`](/en/sandboxing) settings with Read and Edit deny rules; both are merged into the final sandbox boundary
* Network restrictions combine WebFetch permission rules with the sandbox's `allowedDomains` and `deniedDomains` lists

When sandboxing is enabled with `autoAllowBashIfSandboxed: true`, which is the default, sandboxed Bash commands run without prompting even if your permissions include a bare `Bash` ask rule, or the [equivalent `Bash(*)` form](#match-all-uses-of-a-tool): the sandbox boundary substitutes for that whole-tool prompt. These checks still apply:

* Content-scoped ask rules like `Bash(git push *)` still force a prompt
* Explicit deny rules still apply
* `rm` or `rmdir` commands that target `/`, your home directory, or other critical system paths still trigger a prompt

Commands that won't run sandboxed, such as excluded commands, respect the bare `Bash` ask rule as usual. See [sandbox modes](/en/sandboxing#sandbox-modes) to change this behavior.

## Managed settings

For organizations that need centralized control over Claude Code configuration, administrators can deploy managed settings that can't be overridden by user or project settings. These policy settings follow the same format as regular settings files and can be delivered through MDM/OS-level policies, managed settings files, [server-managed settings](/en/server-managed-settings), or a self-hosted [Claude apps gateway](/en/claude-apps-gateway). See [settings files](/en/settings#settings-files) for delivery mechanisms and file locations.

### Managed-only settings

The following settings are only read from managed settings. Placing them in user or project settings files has no effect.

| Setting                                        | Description                                                                                                                                                                                                                                                                                                                         |
| :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowAllClaudeAiMcps`                         | When `true`, claude.ai connectors load alongside a deployed `managed-mcp.json` instead of being suppressed by its exclusive control. See [Managed MCP configuration](/en/managed-mcp)                                                                                                                                               |
| `allowedChannelPlugins`                        | Allowlist of channel plugins that may push messages. Replaces the default Anthropic allowlist when set. Requires `channelsEnabled: true`. See [Restrict which channel plugins can run](/en/channels#restrict-which-channel-plugins-can-run)                                                                                         |
| `allowManagedHooksOnly`                        | When `true`, only managed hooks, SDK hooks, and hooks from plugins force-enabled in managed settings `enabledPlugins` are loaded. User, project, and all other plugin hooks are blocked                                                                                                                                             |
| `allowManagedMcpServersOnly`                   | When `true`, only `allowedMcpServers` from managed settings are respected. `deniedMcpServers` still merges from all sources. See [Managed MCP configuration](/en/managed-mcp)                                                                                                                                                       |
| `allowManagedPermissionRulesOnly`              | When `true`, prevents user and project settings from defining `allow`, `ask`, or `deny` permission rules. Only rules in managed settings apply. Doesn't affect the MCP server allowlist; for that, set `allowManagedMcpServersOnly`                                                                                                 |
| `blockedMarketplaces`                          | Blocklist of marketplace sources. Blocked sources are checked before downloading, so they never touch the filesystem. See [managed marketplace restrictions](/en/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                              |
| `channelsEnabled`                              | Allow [channels](/en/channels) for the organization. See [enterprise controls](/en/channels#enterprise-controls) for the default on each plan                                                                                                                                                                                       |
| `disableSideloadFlags`                         | {/* min-version: 2.1.193 */}Reject the `--plugin-dir`, `--plugin-url`, `--agents`, and `--mcp-config` CLI flags at startup. Without this, users can bypass `strictKnownMarketplaces` for a single run by passing these flags. See [`disableSideloadFlags`](/en/settings#available-settings). Requires Claude Code v2.1.193 or later |
| `forceRemoteSettingsRefresh`                   | When `true`, blocks CLI startup until remote managed settings are freshly fetched and exits if the fetch fails. See [fail-closed enforcement](/en/server-managed-settings#enforce-fail-closed-startup)                                                                                                                              |
| `pluginTrustMessage`                           | Custom message appended to the plugin trust warning shown before installation                                                                                                                                                                                                                                                       |
| `sandbox.filesystem.allowManagedReadPathsOnly` | When `true`, only `filesystem.allowRead` paths from managed settings are respected. `denyRead` still merges from all sources                                                                                                                                                                                                        |
| `sandbox.network.allowManagedDomainsOnly`      | When `true`, only `allowedDomains` and `WebFetch(domain:...)` allow rules from managed settings are respected. Non-allowed domains are blocked automatically without prompting the user. Denied domains still merge from all sources                                                                                                |
| `strictKnownMarketplaces`                      | Controls which plugin marketplace sources users can add and install plugins from. See [managed marketplace restrictions](/en/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                  |
| `strictPluginOnlyCustomization`                | Block skills, agents, hooks, and MCP servers from user and project sources, so they can only come from plugins or managed settings. `true` locks all four surfaces; an array such as `["skills", "hooks"]` locks only the named ones. See [`strictPluginOnlyCustomization`](/en/settings#strictpluginonlycustomization)             |
| `wslInheritsWindowsSettings`                   | When `true` in the Windows HKLM registry key or `C:\Program Files\ClaudeCode\managed-settings.json`, WSL reads managed settings from the Windows policy chain in addition to `/etc/claude-code`. See [Settings files](/en/settings#settings-files)                                                                                  |

`disableBypassPermissionsMode` is typically placed in managed settings to enforce organizational policy, but it works from any scope. A user can set it in their own settings to lock themselves out of bypass mode.

<Note>
  On Team and Enterprise plans, an Owner enables or disables [Remote Control](/en/remote-control) and [web sessions](/en/claude-code-on-the-web) organization-wide in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code). Remote Control can additionally be disabled per device with the [`disableRemoteControl`](/en/settings#available-settings) setting. Web sessions have no per-device managed settings key.
</Note>

## Settings precedence

Permission rules follow the same [settings precedence](/en/settings#settings-precedence) as all other Claude Code settings:

1. **Managed settings**: can't be overridden by any other level, including command line arguments
2. **Command line arguments**: temporary session overrides
3. **Local project settings** (`.claude/settings.local.json`)
4. **Shared project settings** (`.claude/settings.json`)
5. **User settings** (`~/.claude/settings.json`)

If a tool is denied at any level, no other level can allow it. For example, a managed settings deny can't be overridden by `--allowedTools`, and `--disallowedTools` can add restrictions beyond what managed settings define.

The same holds across settings scopes: if user settings allow a permission and project settings deny it, the deny rule blocks it. The reverse is also true: a user-level deny blocks a project-level allow, because deny rules from any scope are evaluated before allow rules.

Embedding hosts can supply additional managed policy via the SDK `managedSettings` option when [`parentSettingsBehavior`](/en/settings#settings-precedence) is set to `"merge"`; embedder values can tighten policy but not loosen it.

## Project allow rules and workspace trust

`permissions.allow` rules and `permissions.additionalDirectories` entries in a project's `.claude/settings.json` grant capability, so Claude Code applies them only after you accept the [workspace trust dialog](/en/security#additional-safeguards) for that workspace. Until then, Claude Code reads the rules but doesn't apply them. The trust dialog lists the allow rules and additional directories the folder would grant so you can review them before accepting. `deny` and `ask` rules aren't affected, since they only restrict.

Claude Code saves trust per workspace, keyed on the git repository root or, outside a repository, the directory you started Claude Code from. When you start in your home directory, trust is held for the current session only and isn't written to disk; see the [additional safeguards](/en/security#additional-safeguards) note. Trusting a parent directory doesn't apply a nested project's allow rules.

`.claude/settings.local.json` is your own file, so the workspace trust check usually doesn't apply to it. When a repository could have supplied the file, such as when it is committed to git or `.claude` is a symlink, its allow rules and additional directories go through the trust check like project settings.

Claude Code runs git to check whether the repository supplied the file, and it runs that check only in a folder covered by an accepted trust dialog, for that folder or for one of its parent directories. In an interactive session in a folder you haven't trusted yet, allow rules and additional directories in `.claude/settings.local.json` go through the trust check like project settings until you accept the dialog, unless the session runs in your own configuration home as described below. Of the two exceptions below, only the configuration-home exception applies before the dialog, because it doesn't need to run git. Determining that a directory isn't inside a git repository uses the same git check, so the not-inside-a-repository exception takes effect once a trust dialog covering the folder is accepted. Before v2.1.207, an untracked `.claude/settings.local.json` applied its allow rules in that folder before you accepted the dialog.

Allow rules and additional directories in `.claude/settings.local.json` also apply without workspace trust in two cases:

* The directory you started Claude Code from isn't inside a git repository.
* The session runs in your own configuration home: your home directory or any directory whose `.claude` subdirectory you've set as [`CLAUDE_CONFIG_DIR`](/en/env-vars).

In both cases the file is one you created rather than one a repository could have supplied, and a repository-committed `.claude/settings.local.json` still requires workspace trust. Versions 2.1.196 through 2.1.199 treated the file as repository-supplied in those workspaces, ignored its allow rules, and printed a [`this workspace has not been trusted`](/en/errors#workspace-has-not-been-trusted) warning to stderr. The two exceptions above match v2.1.195 and earlier and were restored in v2.1.200.

Also as of v2.1.200, a workspace whose allow rules or additional directories still aren't applied, but that never showed the trust dialog because a parent directory was already trusted, shows the dialog the next time you start Claude Code there interactively. The dialog offers two choices:

* **Yes, I trust this folder**: saves trust for that workspace and applies the rules in the same session.
* **No, continue without these permissions**: keeps working with those rules ignored. The dialog appears again in the next session.

In [non-interactive mode](/en/headless) with `-p`, no dialog appears and the rules stay ignored.

## Example configurations

This [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) includes starter settings configurations for common deployment scenarios. Use these as starting points and adjust them to fit your needs.

## See also

* [Settings](/en/settings): complete configuration reference including the permission settings table
* [Configure auto mode](/en/auto-mode-config): tell the auto mode classifier which infrastructure your organization trusts
* [Sandboxing](/en/sandboxing): OS-level filesystem and network isolation for Bash commands
* [Authentication](/en/authentication): set up user access to Claude Code
* [Security](/en/security): security safeguards and best practices
* [Hooks](/en/hooks-guide): automate workflows and extend permission evaluation
