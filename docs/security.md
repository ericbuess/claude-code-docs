> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Security

> Learn about Claude Code's security safeguards and best practices for safe usage.

## How we approach security

### Security foundation

Your code's security is paramount. Claude Code is built with security at its core, developed according to Anthropic's comprehensive security program. Learn more and access resources (SOC 2 Type 2 report, ISO 27001 certificate, etc.) at [Anthropic Trust Center](https://trust.anthropic.com).

### Permission-based architecture

A session's permission mode sets which actions Claude can take without asking you first. Auto mode is the built-in starting permission mode for interactive terminal and VS Code sessions. [Which mode a session starts in](/docs/en/permission-modes#which-mode-a-session-starts-in) covers earlier versions, other surfaces, and the settings that change the starting permission mode.

* **Auto mode**: A separate classifier model reviews actions instead of you and blocks the ones it judges unsafe. [How the classifier evaluates actions](/docs/en/permission-modes#how-the-classifier-evaluates-actions) lists which actions Claude Code approves outright, which it sends to the classifier, and which Claude Code still asks you about. Your explicit ask and deny rules still apply, and your organization can [turn auto mode off](/docs/en/permission-modes#eliminate-prompts-with-auto-mode)
* **Manual mode**: Claude Code starts with read-only permissions. When it needs to edit files, run tests, or execute commands, it asks you first, and you choose whether to approve the action once or allow it from then on. It runs a built-in set of [read-only commands](/docs/en/permissions#read-only-commands) such as `ls`, `cat`, and `git status` without asking

You and your organization configure these permissions directly. For detailed permission configuration, see [Permissions](/docs/en/permissions).

### Built-in protections

To mitigate risks in agentic systems:

* **Sandboxed bash tool**: [Sandbox](/docs/en/sandboxing) bash commands with filesystem and network isolation, reducing permission prompts while maintaining security. Configure with `/sandbox` to define boundaries where Claude Code can work autonomously
* **Working directory boundary**: In Manual mode, Claude Code asks you before its file tools read or write outside the folder where it was started and its subfolders. The boundary is a permission prompt, so a Bash command you approve can still write anywhere your user account can
  * To read a folder without the prompt, add it as an [additional directory](/docs/en/permissions#working-directories)
  * To restrict Bash commands at the operating system level, turn on [sandboxing](/docs/en/sandboxing#filesystem-isolation)
* **Prompt fatigue mitigation**: Support for allowlisting frequently used safe commands per-user, per-codebase, or per-organization
* **Accept Edits mode**: Auto-approves file edits and a fixed set of filesystem Bash commands like `mkdir`, `touch`, `rm`, `mv`, `cp`, and `sed` for paths in the working directory. Other Bash commands and out-of-scope paths still prompt

### User responsibility

You're responsible for reviewing proposed code and commands for safety before approval.

## Protect against prompt injection

Prompt injection is a technique where an attacker attempts to override or manipulate an AI assistant's instructions by inserting malicious text. Claude Code includes several safeguards against these attacks:

### Core protections

* **Permission system**: In Manual mode, sensitive operations require explicit approval
* **Network command approval**: Commands that fetch content from the web such as `curl` and `wget` are not auto-approved by default. In Manual mode they prompt like any other non-read-only Bash command, so you can still approve once or add an explicit allow rule like `Bash(curl *)`. To stop Claude from running them, add them to [`permissions.deny`](/docs/en/permissions#tool-specific-permission-rules). A deny rule matches the command [as written](/docs/en/permissions#bash-rule-limits); for network enforcement that doesn't depend on the command text, see [sandbox network isolation](/docs/en/sandboxing#network-isolation)

### Privacy safeguards

We have implemented several safeguards to protect your data, including:

* Limited retention periods for sensitive information (see the [Privacy Center](https://privacy.anthropic.com/en/articles/10023548-how-long-do-you-store-my-data) to learn more)
* Restricted access to user session data
* User control over data training preferences. Consumer users can change their [privacy settings](https://claude.ai/settings/privacy) at any time.

For full details, please review our [Commercial Terms of Service](https://www.anthropic.com/legal/commercial-terms) (for Team, Enterprise, and API users) or [Consumer Terms](https://www.anthropic.com/legal/consumer-terms) (for Free, Pro, and Max users) and [Privacy Policy](https://www.anthropic.com/legal/privacy).

### Additional safeguards

* **Network request approval**: In Manual mode, most tools that make network requests require user approval by default
* **Web page summaries**: For most fetches, WebFetch runs a separate model call over the page, and Claude receives that call's answer instead of the raw page. See [WebFetch tool behavior](/docs/en/tools-reference#webfetch-tool-behavior)
* **Trust verification**: In an interactive session, Claude Code shows the workspace trust dialog when you start it in a folder you haven't trusted. Servers in a project's `.mcp.json` have their own approval prompt, and [Project scope](/docs/en/mcp#project-scope) lists the sessions that skip it
  * Note: A `-p` session shows neither prompt. [What runs before you trust a folder](/docs/en/permissions#what-runs-before-you-trust-a-folder) lists what a repository's files can run there
  * Note: When you start Claude Code directly in your home directory, trust acceptance is held for the current session only and is not written to disk, so the prompt reappears on each launch. There is no setting to persist it. Start Claude Code from a project subdirectory instead, where trust acceptance is saved per directory
* **Command injection detection**: In Manual mode, Claude Code asks before running a Bash command it can't fully analyze. An allow rule for part of a command, such as `Bash(git *)`, doesn't skip that prompt. [Sandboxed commands](/docs/en/permissions#how-permissions-interact-with-sandboxing) can run without it
* **Fail-closed matching**: In Manual mode, unmatched commands require approval by default
* **Secure credential storage**: API keys and tokens are stored in the macOS Keychain when available. On Linux they're stored in a file with mode `0600`, and on Windows in a file that inherits the access controls of your user profile directory. See [Credential Management](/docs/en/authentication#credential-management)

<Warning>
  **Windows WebDAV security risk**: When running Claude Code on Windows, we recommend against enabling WebDAV or allowing Claude Code to access paths such as `\\*` that may contain WebDAV subdirectories. [WebDAV has been deprecated by Microsoft](https://learn.microsoft.com/en-us/windows/whats-new/deprecated-features#:~:text=The%20Webclient%20\(WebDAV\)%20service%20is%20deprecated) due to security risks. Enabling WebDAV may allow Claude Code to trigger network requests to remote hosts, bypassing the permission system.
</Warning>

**Best practices for working with untrusted content**:

1. Review suggested commands before approval
2. Avoid piping untrusted content directly to Claude
3. Verify proposed changes to critical files
4. Use virtual machines (VMs) to run scripts and make tool calls, especially when interacting with external web services
5. Report suspicious behavior with `/feedback`

<Warning>
  While these protections significantly reduce risk, no system is completely
  immune to all attacks. Always maintain good security practices when working
  with any AI tool.
</Warning>

## MCP security

You can connect Claude Code to Model Context Protocol (MCP) servers. Project-scoped servers are defined in `.mcp.json`, which you can check into source control. Servers at [other scopes](/docs/en/mcp#mcp-installation-scopes) and [claude.ai connectors](/docs/en/mcp#how-connectors-reach-claude-code) are configured outside the repository, and plugins can add servers too, so reviewing `.mcp.json` doesn't show every server a session can load. To restrict which servers run in your organization, see [Managed MCP configuration](/docs/en/managed-mcp).

We encourage either writing your own MCP servers or using MCP servers from providers that you trust. You are able to configure Claude Code permissions for MCP servers. Anthropic reviews connectors against its [listing criteria](https://claude.com/docs/connectors/building/review-criteria) before adding them to the [Anthropic Directory](https://claude.ai/directory), but does not security-audit or manage any MCP server.

## IDE security

See [VS Code security and privacy](/docs/en/vs-code#security-and-privacy) for more information on running Claude Code in an IDE.

## Cloud execution security

When you use [cloud sessions](/docs/en/claude-code-on-the-web), additional security controls are in place. Sessions your organization routes to a [self-hosted environment](/docs/en/self-hosted-environments) run on your own infrastructure, where isolation, network egress, and git credentials are your deployment's responsibility. In Anthropic-hosted environments:

* **Isolated virtual machines**: Each cloud session runs in an isolated, Anthropic-managed VM
* **Network access controls**: Network access is limited by default and can be configured to be disabled or allow only specific domains
* **Credential protection**: GitHub credentials are stored encrypted on Anthropic's servers and never enter the session VM. The VM holds a short-lived credential scoped to that session, and GitHub traffic goes through an [Anthropic proxy](/docs/en/cloud-environments#github-proxy) that attaches the GitHub credential on the server side. See [GitHub authentication options](/docs/en/claude-code-on-the-web#github-authentication-options) for how you grant access
* **Push restrictions**: The [GitHub proxy](/docs/en/cloud-environments#github-proxy) rejects branch deletions and pushes of anything other than a branch, such as a tag. GitHub decides which branches a session can update by applying your repository's branch protection rules and rulesets to the GitHub access you connected. A rule that access can bypass doesn't block a session's push
* **Audit logging**: All operations in cloud sessions are logged for compliance and audit purposes
* **Automatic cleanup**: Session VMs are reclaimed after a period of inactivity
* **Deletion**: You can [delete a session](/docs/en/claude-code-on-the-web#delete-sessions) at any time. See [Cloud execution data flow](/docs/en/data-usage#cloud-execution-data-flow-and-dependencies) for what Anthropic stores for a cloud session

For more details on cloud execution, see [Use Claude Code in the cloud](/docs/en/claude-code-on-the-web); to configure network access for cloud sessions, see [Configure cloud environments](/docs/en/cloud-environments#network-access).

[Remote Control](/docs/en/remote-control) sessions work differently: the web interface connects to a Claude Code process running on your local machine. All code execution and file access stays local, and session traffic travels through the Anthropic API over TLS; while connected, the session transcript is stored on Anthropic servers to sync the conversation across devices, as described in [Connection and security](/docs/en/remote-control#connection-and-security). No cloud VMs or sandboxing are involved. The connection uses multiple short-lived, narrowly scoped credentials, each limited to a specific purpose and expiring independently, to limit the blast radius of any single compromised credential.

## Security best practices

### Working with sensitive code

* Review all suggested changes before approval
* Use project-specific permission settings for sensitive repositories
* For additional isolation, run the whole Claude Code (local mode) process inside the [sandbox runtime](/docs/en/sandbox-environments#sandbox-runtime) or a [dev container](/docs/en/devcontainer)
* Regularly audit your permission settings with `/permissions`

### Team security

* Use [managed settings](/docs/en/settings#where-settings-live) to enforce organizational standards
* Share approved permission configurations through version control
* Train team members on security best practices
* Monitor Claude Code usage through [OpenTelemetry metrics](/docs/en/monitoring-usage)
* Audit or block settings changes during sessions with [`ConfigChange` hooks](/docs/en/hooks#configchange)

### Reporting security issues

If you discover a security vulnerability in Claude Code:

1. Do not disclose it publicly
2. Report it through our [HackerOne program](https://hackerone.com/4f1f16ba-10d3-4d09-9ecc-c721aad90f24/embedded_submissions/new)
3. Include detailed reproduction steps
4. Allow time for us to address the issue before public disclosure

## Related resources

* [Security guidance plugin](/docs/en/security-guidance): have Claude review and fix vulnerabilities in its own code changes during the session
* [`/security-review`](/docs/en/commands#all-commands): run an on-demand security pass over the changes on your current branch
* [Sandbox environments](/docs/en/sandbox-environments): compare isolation approaches and choose one for your threat model
* [Sandboxing](/docs/en/sandboxing): filesystem and network isolation for Bash commands
* [Permissions](/docs/en/permissions): configure permissions and access controls
* [Monitoring usage](/docs/en/monitoring-usage): track and audit Claude Code activity
* [Development containers](/docs/en/devcontainer): secure, isolated environments
* [Anthropic Trust Center](https://trust.anthropic.com): security certifications and compliance
* [CISO's guide to agentic AI](https://claude.com/blog/ciso-guide-to-agentic-ai): a security leader's framework for assessing agentic AI deployments
