> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Identity and Access Management

> Learn how to configure user authentication, authorization, and access controls for Claude Code in your organization.

## Authentication methods

Setting up Claude Code requires access to Anthropic models. For teams, you can set up Claude Code access in one of these ways:

* [Claude for Teams or Enterprise](/en/setup#for-teams-and-organizations) (recommended)
* [Claude Console with team billing](/en/setup#for-teams-and-organizations)
* [Amazon Bedrock](/en/amazon-bedrock)
* [Google Vertex AI](/en/google-vertex-ai)
* [Microsoft Foundry](/en/microsoft-foundry)

### Claude for Teams or Enterprise (recommended)

[Claude for Teams](https://claude.com/pricing#team-&-enterprise) and [Claude for Enterprise](https://anthropic.com/contact-sales) provide the best experience for organizations using Claude Code. Team members get access to both Claude Code and Claude on the web with centralized billing and team management.

* **Claude for Teams**: Self-service plan with collaboration features, admin tools, and billing management. Best for smaller teams.
* **Claude for Enterprise**: Adds SSO, domain capture, role-based permissions, compliance API, and managed policy settings for organization-wide Claude Code configurations. Best for larger organizations with security and compliance requirements.

**To set up Claude Code access:**

1. Subscribe to [Claude for Teams](https://claude.com/pricing#team-&-enterprise) or contact sales for [Claude for Enterprise](https://anthropic.com/contact-sales)
2. Invite team members from the admin dashboard
3. Team members install Claude Code and log in with their Claude.ai accounts

### Claude Console authentication

For organizations that prefer API-based billing, you can set up access through the Claude Console.

**To set up Claude Code access for your team via Claude Console:**

1. Use your existing Claude Console account or create a new Claude Console account
2. You can add users through either method below:
   * Bulk invite users from within the Console (Console -> Settings -> Members -> Invite)
   * [Set up SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)
3. When inviting users, they need one of the following roles:
   * "Claude Code" role means users can only create Claude Code API keys
   * "Developer" role means users can create any kind of API key
4. Each invited user needs to complete these steps:
   * Accept the Console invite
   * [Check system requirements](/en/setup#system-requirements)
   * [Install Claude Code](/en/setup#installation)
   * Login with Console account credentials

### Cloud provider authentication

**To set up Claude Code access for your team via Bedrock, Vertex, or Azure:**

1. Follow the [Bedrock docs](/en/amazon-bedrock), [Vertex docs](/en/google-vertex-ai), or [Microsoft Foundry docs](/en/microsoft-foundry)
2. Distribute the environment variables and instructions for generating cloud credentials to your users. Read more about how to [manage configuration here](/en/settings).
3. Users can [install Claude Code](/en/setup#installation)

## Access control and permissions

We support fine-grained permissions so that you're able to specify exactly what the agent is allowed to do (e.g. run tests, run linter) and what it is not allowed to do (e.g. update cloud infrastructure). These permission settings can be checked into version control and distributed to all developers in your organization, as well as customized by individual developers.

### Permission system

Claude Code uses a tiered permission system to balance power and safety:

| Tool Type         | Example          | Approval Required | "Yes, don't ask again" Behavior               |
| :---------------- | :--------------- | :---------------- | :-------------------------------------------- |
| Read-only         | File reads, Grep | No                | N/A                                           |
| Bash Commands     | Shell execution  | Yes               | Permanently per project directory and command |
| File Modification | Edit/write files | Yes               | Until session end                             |

### Configuring permissions

You can view & manage Claude Code's tool permissions with `/permissions`. This UI lists all permission rules and the settings.json file they are sourced from.

* **Allow** rules let Claude Code use the specified tool without manual approval.
* **Ask** rules prompt for confirmation whenever Claude Code tries to use the specified tool.
* **Deny** rules prevent Claude Code from using the specified tool.

Rules are evaluated in order: **deny → ask → allow**. The first matching rule wins, so deny rules always take precedence.

* **Additional directories** extend Claude's file access to directories beyond the initial working directory.
* **Default mode** controls Claude's permission behavior when encountering new requests.

Permission rules use the format: `Tool` or `Tool(optional-specifier)`

A rule that is just the tool name matches any use of that tool. For example, adding `Bash` to the allow list allows Claude Code to use the Bash tool without requiring user approval. `Bash(*)` is equivalent to `Bash` and can be used interchangeably.

<Note>
  For a quick reference on permission rule syntax including wildcards, see [Permission rule syntax](/en/settings#permission-rule-syntax) in the settings documentation.
</Note>

#### Permission modes

Claude Code supports several permission modes that can be set as the `defaultMode` in [settings files](/en/settings#settings-files):

| Mode                | Description                                                                                                               |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------ |
| `default`           | Standard behavior - prompts for permission on first use of each tool                                                      |
| `acceptEdits`       | Automatically accepts file edit permissions for the session                                                               |
| `plan`              | Plan Mode - Claude can analyze but not modify files or execute commands                                                   |
| `dontAsk`           | Auto-denies tools unless pre-approved via `/permissions` or [`permissions.allow`](/en/settings#permission-settings) rules |
| `bypassPermissions` | Skips all permission prompts (requires safe environment - see warning below)                                              |

#### Working directories

By default, Claude has access to files in the directory where it was launched. You can extend this access:

* **During startup**: Use `--add-dir <path>` CLI argument
* **During session**: Use `/add-dir` command
* **Persistent configuration**: Add to `additionalDirectories` in [settings files](/en/settings#settings-files)

Files in additional directories follow the same permission rules as the original working directory - they become readable without prompts, and file editing permissions follow the current permission mode.

#### Tool-specific permission rules

Some tools support more fine-grained permission controls:

**Bash**

Bash permission rules support wildcard matching with `*`. Wildcards can appear at any position in the command, including at the beginning, middle, or end:

* `Bash(npm run build)` Matches the exact Bash command `npm run build`
* `Bash(npm run test *)` Matches Bash commands starting with `npm run test`
* `Bash(npm *)` Matches any command starting with `npm ` (e.g., `npm install`, `npm run build`)
* `Bash(* install)` Matches any command ending with ` install` (e.g., `npm install`, `yarn install`)
* `Bash(git * main)` Matches commands like `git checkout main`, `git merge main`
* `Bash(* --help *)` Matches any command with `--help` followed by additional arguments

When `*` appears at the end with a space before it (like `Bash(ls *)`), it enforces a word boundary, requiring the prefix to be followed by a space or end-of-string. For example, `Bash(ls *)` matches `ls -la` but not `lsof`. In contrast, `Bash(ls*)` without a space matches both `ls -la` and `lsof` because there's no word boundary constraint. The legacy `:*` suffix syntax is equivalent to ` *` but is deprecated.

<Tip>
  Claude Code is aware of shell operators (like `&&`) so a prefix match rule like `Bash(safe-cmd *)` won't give it permission to run the command `safe-cmd && other-cmd`
</Tip>

<Warning>
  Important limitations of Bash permission patterns:

  1. The space before `*` matters: `Bash(ls *)` matches `ls -la` but not `lsof`, while `Bash(ls*)` matches both
  2. The `*` wildcard can appear at any position and matches any sequence of characters
  3. Patterns like `Bash(curl http://github.com/ *)` can be bypassed in many ways:
     * Options before URL: `curl -X GET http://github.com/...` won't match
     * Different protocol: `curl https://github.com/...` won't match
     * Redirects: `curl -L http://bit.ly/xyz` (redirects to github)
     * Variables: `URL=http://github.com && curl $URL` won't match
     * Extra spaces: `curl  http://github.com` won't match

  For more reliable URL filtering, consider:

  * **Restrict Bash network tools**: Use deny rules to block `curl`, `wget`, and similar commands, then use the WebFetch tool with `WebFetch(domain:github.com)` permission for allowed domains
  * **Use PreToolUse hooks**: Implement a hook that validates URLs in Bash commands and blocks disallowed domains
  * Instructing Claude Code about your allowed curl patterns via CLAUDE.md

  Note that using WebFetch alone does not prevent network access. If Bash is allowed, Claude can still use `curl`, `wget`, or other tools to reach any URL.
</Warning>

**Read & Edit**

`Edit` rules apply to all built-in tools that edit files. Claude will make a best-effort attempt to apply `Read` rules to all built-in tools that read files like Grep and Glob.

Read & Edit rules both follow the [gitignore](https://git-scm.com/docs/gitignore) specification with four distinct pattern types:

| Pattern            | Meaning                                | Example                          | Matches                            |
| ------------------ | -------------------------------------- | -------------------------------- | ---------------------------------- |
| `//path`           | **Absolute** path from filesystem root | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`          |
| `~/path`           | Path from **home** directory           | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf`     |
| `/path`            | Path **relative to settings file**     | `Edit(/src/**/*.ts)`             | `<settings file path>/src/**/*.ts` |
| `path` or `./path` | Path **relative to current directory** | `Read(*.env)`                    | `<cwd>/*.env`                      |

<Warning>
  A pattern like `/Users/alice/file` is NOT an absolute path - it's relative to your settings file! Use `//Users/alice/file` for absolute paths.
</Warning>

* `Edit(/docs/**)` - Edits in `<project>/docs/` (NOT `/docs/`!)
* `Read(~/.zshrc)` - Reads your home directory's `.zshrc`
* `Edit(//tmp/scratch.txt)` - Edits the absolute path `/tmp/scratch.txt`
* `Read(src/**)` - Reads from `<current-directory>/src/`

<Note>
  In gitignore patterns, `*` matches files in a single directory while `**` matches recursively across directories. To allow all file access, use just the tool name without parentheses: `Read`, `Edit`, or `Write`.
</Note>

**WebFetch**

* `WebFetch(domain:example.com)` Matches fetch requests to example.com

**MCP**

* `mcp__puppeteer` Matches any tool provided by the `puppeteer` server (name configured in Claude Code)
* `mcp__puppeteer__*` Wildcard syntax that also matches all tools from the `puppeteer` server
* `mcp__puppeteer__puppeteer_navigate` Matches the `puppeteer_navigate` tool provided by the `puppeteer` server

**Task (Subagents)**

Use `Task(AgentName)` rules to control which [subagents](/en/sub-agents) Claude can use:

* `Task(Explore)` Matches the Explore subagent
* `Task(Plan)` Matches the Plan subagent
* `Task(Verify)` Matches the Verify subagent

Add these rules to the `deny` array in your [settings](/en/settings#permission-settings) or use the `--disallowedTools` CLI flag to disable specific agents. For example, to disable the Explore agent:

```json  theme={null}
{
  "permissions": {
    "deny": ["Task(Explore)"]
  }
}
```

### Additional permission control with hooks

[Claude Code hooks](/en/hooks-guide) provide a way to register custom shell commands to perform permission evaluation at runtime. When Claude Code makes a tool call, PreToolUse hooks run before the permission system runs, and the hook output can determine whether to approve or deny the tool call in place of the permission system.

### Managed settings

For organizations that need centralized control over Claude Code configuration, administrators can deploy `managed-settings.json` files to [system directories](/en/settings#settings-files). These policy files follow the same format as regular settings files and cannot be overridden by user or project settings.

### Settings precedence

When multiple settings sources exist, they are applied in the following order (highest to lowest precedence):

1. Managed settings (`managed-settings.json`)
2. Command line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

This hierarchy ensures that organizational policies are always enforced while still allowing flexibility at the project and user levels where appropriate.

## Credential management

Claude Code securely manages your authentication credentials:

* **Storage location**: On macOS, API keys, OAuth tokens, and other credentials are stored in the encrypted macOS Keychain.
* **Supported authentication types**: Claude.ai credentials, Claude API credentials, Azure Auth, Bedrock Auth, and Vertex Auth.
* **Custom credential scripts**: The [`apiKeyHelper`](/en/settings#available-settings) setting can be configured to run a shell script that returns an API key.
* **Refresh intervals**: By default, `apiKeyHelper` is called after 5 minutes or on HTTP 401 response. Set `CLAUDE_CODE_API_KEY_HELPER_TTL_MS` environment variable for custom refresh intervals.
