> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Set up Claude Code (local mode) for a HIPAA-ready organization

> Prepare developers' computers to run Claude Code (local mode) under the HIPAA configuration. Covers versions, network access, managed settings, and local data.

The HIPAA configuration is an organization setting on Claude Enterprise plans, for organizations that handle protected health information (PHI) and have a [Business Associate Agreement (BAA)](https://support.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers) with Anthropic. It applies to Claude Code (local mode) and Cowork (local mode), and it restricts features in both products.

<Note>
  "(local mode)" means a local session, not a [cloud session](/docs/en/claude-code-on-the-web). Local sessions run in one of these places:

  * Claude Code in the terminal
  * Claude Code in the Code tab of Claude Desktop
  * Cowork in Claude Desktop

  The Claude Code extensions for VS Code and JetBrains aren't part of (local mode). They keep working with the HIPAA configuration applied, but your BAA doesn't cover them. See the [Implementation Guide](https://trust.anthropic.com/resources?s=l1wrssd9hsbi4gak0tp5a6\&name=%5Banthropic%5D-hipaa-ready-offering-implementation-guide) for the full list of Eligible Services.
</Note>

This page is for the IT or security administrator who prepares developers' computers. The Primary Owner of your Claude organization applies the configuration itself. [Use Claude Code (local mode) and Cowork (local mode) on a HIPAA-ready Enterprise plan](https://support.claude.com/en/articles/17318731) explains what your BAA includes, how the configuration is applied, and how to schedule the date it's applied.

If members of your organization also use Cowork, follow [Set up Cowork (local mode) for a HIPAA-ready organization](https://claude.com/docs/cowork/hipaa-setup) as well. It covers the Claude Desktop policy and Cowork's local data.

The table shows when to do each part of the setup:

| When | What to do |
| :- | :- |
| Before the configuration is applied | [Prepare computers](#prepare-computers-before-the-hipaa-configuration-is-applied): check how developers connect, update the apps, allow network access, and deploy managed settings |
| After it's applied | The Code tab is off until an Owner turns it back on. [Confirm the configuration on a computer](#confirm-the-configuration-on-a-computer) |
| Ongoing | [Manage local session data](#manage-local-session-data) |

## Prepare computers before the HIPAA configuration is applied

We recommend you start with the tasks in this section and complete them before the configuration is applied.

### Check how developers sign in and connect

The HIPAA configuration takes effect only in sessions where a developer signs in with a Claude Enterprise account and Claude Code connects directly to the Claude API. On any other connection, developers can keep using Claude Code, but it doesn't apply the [HIPAA configuration](#what-developers-see-in-claude-code).

The table shows which connections are eligible. To find out whether your BAA covers a session in a "No" row, see [Use Claude Code (local mode) and Cowork (local mode) on a HIPAA-ready Enterprise plan](https://support.claude.com/en/articles/17318731).

| How Claude Code connects | Eligible for the HIPAA configuration |
| :- | :- |
| A Claude Enterprise account, connecting directly to the Claude API | Yes |
| Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, Claude Platform on AWS, or a [Claude apps gateway](/docs/en/claude-apps-gateway) | No |
| An [LLM gateway](/docs/en/llm-gateway) or any other custom `ANTHROPIC_BASE_URL` | No |
| `ANTHROPIC_AUTH_TOKEN` or `apiKeyHelper`, on a computer with no Claude Enterprise sign-in | No |
| A Claude Console API key or [federation credentials](/docs/en/authentication#anthropic-profiles-and-federation-credentials) | No. These sessions belong to a Claude Console organization, which has its own agreement and settings |

#### Check how a computer connects

Open a terminal on the computer, run `claude`, and enter `/status` at the prompt. The **Status** tab shows these lines:

| Line | When it appears |
| :- | :- |
| `Login method` and `Organization` | The session is signed in with a claude.ai account. For a Claude Enterprise account, `Login method` reads `Claude Enterprise account` and `Organization` shows your organization |
| `API provider` | Only when the session uses a cloud provider or a Claude apps gateway |
| `Anthropic base URL` | Only when `ANTHROPIC_BASE_URL` is set |

If a computer uses a connection that isn't eligible for the HIPAA configuration, you can use [managed settings](#deploy-managed-settings) to block cloud providers, gateways, and credentials set with `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `apiKeyHelper`.

### Update Claude Code and Claude Desktop

The HIPAA configuration requires Claude Code v2.1.285 or later and Claude Desktop v2.19675.0 or later. If your organization uses both the terminal and the [Claude Desktop app](/docs/en/desktop), update both.

To read the installed Claude Code version, run this command in a terminal. It's the same in Bash, Zsh, and PowerShell:

```bash theme={null}
claude --version
```

A supported installation prints `2.1.285 (Claude Code)` or a higher number.

To read the installed Claude Desktop version, see [Check your version](/docs/en/desktop#check-your-version).

#### What developers see on an older version

For organizations with the HIPAA configuration, Anthropic's servers reject requests from versions older than the minimum version. Anthropic raises the minimum version over time, and there's nothing for you to configure.

| App | What a developer sees on an older version |
| :- | :- |
| Claude Code | Each request fails with an [`API Error`](/docs/en/errors#claude-code-does-not-support-this-model) that says the version is older than the minimum version your organization's policy requires |
| Claude Desktop | An **Update required** dialog that tells the developer to update Claude Desktop to continue using the **Code** tab |

To keep developers on a supported version, [keep Claude Code updated](/docs/en/setup#update-claude-code). For Claude Desktop, see [Update Claude Desktop](https://claude.com/docs/cowork/hipaa-setup#update-claude-desktop).

### Allow network access

Allow the hosts in this table through your proxy and firewall, over HTTPS on port 443. Allow each whole host, not individual paths.

| Host | Needed for |
| :- | :- |
| `api.anthropic.com` | Claude API requests, telemetry, and the organization policy that tells Claude Code the HIPAA configuration is on |
| `claude.ai`, `claude.com`, `platform.claude.com` | Sign-in and token refresh |
| `downloads.claude.ai` | The native installer and its updates |
| `mcp-proxy.anthropic.com` | [Connectors from claude.ai](/docs/en/mcp#use-mcp-servers-from-claude-ai) |

This table lists the hosts a native install of Claude Code needs in the terminal to sign in, run, and update. These pages list the rest:

* **Other install methods and optional features**: [Network access requirements](/docs/en/network-config#network-access-requirements) lists the hosts that npm and Homebrew installs check for updates, and the hosts for features such as plugin installs
* **The Code tab and Cowork**: [Desktop network access requirements](/docs/en/desktop#network-access-requirements) lists the additional hosts Claude Desktop needs
* **Proxies that inspect TLS**: [Custom CA certificates](/docs/en/network-config#custom-ca-certificates) shows how to trust your proxy's certificate

Sessions that go through a corporate HTTPS proxy are still eligible for the HIPAA configuration, as long as the proxy can reach the hosts in the table.

Claude Code learns that your organization has the HIPAA configuration by fetching your organization's policy from `api.anthropic.com`, when it starts and again about every hour while the session is in use. The policy is a record of your organization's HIPAA status and the feature restrictions that follow from it.

To check whether one computer has fetched the policy, see [Confirm the configuration on a computer](#confirm-the-configuration-on-a-computer).

### Deploy managed settings

You can use [managed settings](/docs/en/managed-settings) to direct developers to sign in with a Claude Enterprise account, to block cloud providers and gateways, and to set how many days every computer keeps local session data. The settings apply whether or not the HIPAA configuration is in effect.

The settings in this section are a sample that we recommend as a starting point. Your organization is responsible for deciding what its own environment needs and for confirming that its configuration meets those needs.

The following sample sets four keys that you could add to the [managed settings](/docs/en/managed-settings#choose-a-delivery-mechanism) your organization deploys:

```json theme={null}
{
  "forceLoginMethod": "claudeai",
  "forceLoginOrgUUID": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "allowedProviders": ["anthropic"],
  "cleanupPeriodDays": 30
}
```

#### What each key does

The table shows what to set each key to and what Claude Code enforces for it.

| Key | Set it to | What Claude Code enforces |
| :- | :- | :- |
| [`forceLoginMethod`](/docs/en/settings-reference#forceloginmethod) | `"claudeai"` | Claude Code directs developers to claude.ai sign-in instead of Claude Console |
| [`forceLoginOrgUUID`](/docs/en/settings-reference#forceloginorguuid) | Your organization ID, which an [Owner](/docs/en/server-managed-settings#access-control) can copy from [claude.ai admin settings](https://claude.ai/admin-settings/organization) | Claude Code exits at startup when the claude.ai sign-in belongs to another organization |
| [`allowedProviders`](/docs/en/settings-reference#allowedproviders) | `["anthropic"]` | Claude Code refuses to start on a cloud provider or a gateway |
| [`cleanupPeriodDays`](/docs/en/settings-reference#cleanupperioddays) | The number of days your records policy lets a computer keep session data | Every computer deletes old session data after the same number of days |

<Warning>
  Check the `forceLoginOrgUUID` value before you deploy it. If it doesn't match your organization ID, Claude Code exits at startup for every developer who signs in with a claude.ai account.
</Warning>

The HIPAA configuration doesn't limit `cleanupPeriodDays`, so a developer can raise it in their own settings. When you set it in managed settings, Claude Code ignores the developer's value.

With `forceLoginMethod` or `forceLoginOrgUUID` set, Claude Code also refuses sessions that authenticate with `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, or `apiKeyHelper`.

#### Confirm the settings loaded

On a computer that has the settings, run `claude`, sign in with a Claude Enterprise account, and enter `/status`. The `Setting sources` line lists `Enterprise managed settings` followed by the source in parentheses, such as `(file)`, and the `Allowed providers` line reads `Anthropic API (managed allowedProviders)`. If `Setting sources` doesn't list it, or the `Allowed providers` line is missing, see [Check that a policy is in force](/docs/en/managed-settings#check-that-a-policy-is-in-force).

#### Sessions the managed settings keys don't block

Even with these keys deployed, some sessions can still run without the HIPAA configuration:

* **Claude Console sign-ins and federation credentials**: `forceLoginOrgUUID` checks only claude.ai sign-ins. [Restrict login to your organization](/docs/en/authentication#restrict-login-to-your-organization) lists what Claude Code checks for each sign-in path and credential.
* **Server-managed settings**: if your organization also uses [server-managed settings](/docs/en/server-managed-settings), have an Owner add the same keys there. [How Claude Code combines managed sources](/docs/en/managed-settings#how-claude-code-combines-managed-sources) explains which source applies.
* **Versions older than v2.1.285**: these versions ignore `allowedProviders`, so they can still start on a cloud provider or a gateway. To make v2.1.163 through v2.1.284 refuse to start, you can add [`requiredMinimumVersion`](/docs/en/settings-reference#requiredminimumversion) set to `"2.1.285"` to the same managed settings as the [sample keys](#deploy-managed-settings). Versions before v2.1.163 ignore `requiredMinimumVersion` as well as `allowedProviders`, so [update those computers](#update-claude-code-and-claude-desktop).

To find out whether your BAA covers a session that runs without the HIPAA configuration, see [Use Claude Code (local mode) and Cowork (local mode) on a HIPAA-ready Enterprise plan](https://support.claude.com/en/articles/17318731).

## Confirm the configuration on a computer

Run this check on one managed computer after the configuration is applied to your organization.

<Steps>
  <Step title="Restart Claude Code">
    Quit any running session, open a terminal, and run `claude`. A running session that's in use picks up the configuration within about an hour without a restart. When you restart, Claude Code fetches it right away.
  </Step>

  <Step title="Check the startup notice">
    Confirm that Claude Code prints `Per your organization's policy, some features are limited · /status for details` when it starts.
  </Step>

  <Step title="Check the footer">
    Confirm that a `HIPAA configured` tag appears at the right of the footer, below the prompt. Before v2.1.286, the tag read `HIPAA`.
  </Step>

  <Step title="Run /status">
    Enter `/status` at the prompt. Confirm that the **Status** tab lists `HIPAA` on the `Organization configuration` line.
  </Step>

  <Step title="Check Claude Desktop">
    Applying the HIPAA configuration turns the Code tab off for your organization. If your organization uses it, ask an Owner to go to [**Organization settings > Claude Code**](https://claude.ai/admin-settings/claude-code) and turn on the **Desktop** toggle. For Cowork, see [Confirm the HIPAA configuration in Claude Desktop](https://claude.com/docs/cowork/hipaa-setup#confirm-the-hipaa-configuration-in-claude-desktop).

    Reload Claude Desktop or sign in again. Confirm that the title bar shows a **HIPAA configured** label. On a Mac, open the sidebar to see it.
  </Step>
</Steps>

If `HIPAA` is missing from `/status`, check these causes in order:

1. **The wrong account or connection**: confirm that `/status` shows your organization on the `Organization` line, and shows no `API provider` or `Anthropic base URL` line. [Check how developers sign in and connect](#check-how-developers-sign-in-and-connect) lists the connections that aren't eligible for the configuration.
2. **A blocked policy fetch**: look for an `Organization policy` line in `/status`, which gives the cause. Outside a session, run `claude doctor` and read the same line, which says where Claude Code loaded the policy from or why the policy didn't load. Allow `api.anthropic.com` through your proxy, then restart Claude Code.
3. **The configuration isn't applied yet**: ask the Primary Owner whether they have applied the configuration.

## What developers see in Claude Code

With the HIPAA configuration applied, some Claude Code features are off or behave differently in the terminal. The table lists the changes developers are most likely to ask you about. The [HIPAA feature availability table](https://support.claude.com/en/articles/8114513-business-associate-agreements-baa-for-commercial-customers) lists every Claude Code and Cowork feature, including the ones an Owner can turn back on.

| What a developer notices | Why |
| :- | :- |
| The WebFetch tool is unavailable | WebFetch is off. Web search still works |
| `--cloud`, `/teleport`, and [Remote Control](/docs/en/remote-control) are refused | [Cloud sessions](/docs/en/claude-code-on-the-web) and Remote Control are off |
| `/feedback` and `/bug` are unavailable | Feedback submission is off |
| Claude can't publish an [artifact](/docs/en/artifacts) | Artifact publishing is off |
| An MCP server or hook that reads `ANTHROPIC_API_KEY` stops authenticating | Claude Code [removes Anthropic credentials](#anthropic-credentials-in-commands-hooks-and-mcp-servers) from the processes it starts |
| Restrictions remain after `/login` to a different organization | The HIPAA status lasts until Claude Code restarts |

### Anthropic credentials in commands, hooks, and MCP servers

With the HIPAA configuration applied, Claude Code removes the credentials it uses to reach Anthropic, such as `ANTHROPIC_API_KEY` and `ANTHROPIC_AUTH_TOKEN`, from the environment of the shell commands, hooks, and MCP servers it starts.

The HIPAA configuration doesn't remove cloud provider or GitHub credentials, so a command that pushes to GitHub or calls another service still works with that developer's access. Your BAA with Anthropic doesn't cover the data it sends there. See the [Implementation Guide](https://trust.anthropic.com/resources?s=l1wrssd9hsbi4gak0tp5a6\&name=%5Banthropic%5D-hipaa-ready-offering-implementation-guide) for the full list of Eligible Services.

To limit which commands and hosts Claude can use, see [permission rules](/docs/en/permissions) and the [sandbox](/docs/en/sandboxing).

## Manage local session data

Claude Code (local mode) and Cowork (local mode) store session data on each developer's computer. Securing and deleting that data is your organization's responsibility.

### Claude Code data

[Application data](/docs/en/claude-directory#application-data) lists what Claude Code (local mode) stores on a computer, what its retention sweep deletes after `cleanupPeriodDays`, and what stays until someone deletes it. The same page states what differs in an organization with the HIPAA configuration applied.

The retention sweep runs only when someone starts Claude Code, so a computer where nobody starts it keeps its data.

### Code tab data

The Code tab stores data in these places:

* **Transcripts**: in `~/.claude/projects/`, alongside terminal transcripts. [Cleaned up automatically](/docs/en/claude-directory#cleaned-up-automatically) states when the retention sweep deletes them.
* **The Claude Desktop data folder**: `~/Library/Application Support/Claude` on macOS. On Windows, `%APPDATA%\Claude`, or `%LOCALAPPDATA%\Packages\Claude_pzs8sxrjxfjjc\LocalCache\Roaming\Claude` for the installer downloaded from Anthropic, so check both. With the HIPAA configuration applied, Claude Desktop deletes local Code tab sessions that have been inactive for longer than `cleanupPeriodDays`, including starred ones. It deletes them only while it's running. Claude Desktop handles a deleted session's worktree in one of these ways:
  * **No uncommitted changes, the session isn't starred or pinned, and no other session is using the worktree**: Claude Desktop removes the worktree
  * **Any other case**: the worktree stays on the computer

On Windows, `~` means `%USERPROFILE%`.

### Cowork data

[Manage Cowork data on each computer](https://claude.com/docs/cowork/hipaa-setup#manage-cowork-data-on-each-computer) lists where Cowork (local mode) stores data and what Claude Desktop deletes.

### Delete session data right away

If your organization needs a developer's session data removed before the retention sweep deletes it, you can remove most of it with one command. Sign in to the computer as that developer, open any shell, and run the command for the installed Claude Code version.

On Claude Code v2.1.288 or later, run `claude purge`:

```bash theme={null}
claude purge --all --yes
```

On v2.1.126 through v2.1.287, run `claude project purge`, which takes the same flags:

```bash theme={null}
claude project purge --all --yes
```

Either command deletes every project's transcripts and auto memory, the entries in `tasks/`, `debug/`, and `file-history/`, `history.jsonl`, and the project entries in `~/.claude.json`. Without `--yes`, it prints the plan and asks first.

The purge leaves other paths that can hold session content, such as pasted text in `paste-cache/`. [Clear local data](/docs/en/claude-directory#clear-local-data) lists the paths you can delete by hand. To clear a computer completely, for example before you reassign it, [wipe it](#offboard-a-developer).

### Offboard a developer

Removing a developer's seat or account deletes nothing on their computer, and `/logout` doesn't delete session data either. To remove all of it, you can wipe the computer with your device management tool.

## Related resources

* [Set up Cowork (local mode) for a HIPAA-ready organization](https://claude.com/docs/cowork/hipaa-setup)
* [Deploy managed settings](/docs/en/managed-settings)
* [Enterprise network configuration](/docs/en/network-config)
* [Zero data retention](/docs/en/zero-data-retention)
* [Legal and compliance](/docs/en/legal-and-compliance)
* [Data usage](/docs/en/data-usage)
