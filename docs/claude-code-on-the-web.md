> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code on the web

> Move sessions between web and terminal with `--cloud` and `--teleport`, manage and share sessions, and auto-fix pull requests from the cloud.

<Note>
  Claude Code on the web is in research preview for Pro, Max, and Team users, and for Enterprise users with premium seats or Chat + Claude Code seats.
</Note>

Claude Code on the web runs tasks on Anthropic-managed cloud infrastructure at [claude.ai/code](https://claude.ai/code), or on your organization's [self-hosted environment](/docs/en/self-hosted-environments) when routed there. Sessions persist even if you close your browser, and you can monitor them from the Claude mobile app.

<Tip>
  New to Claude Code on the web? Start with [Get started](/docs/en/web-quickstart) to connect your GitHub account and submit your first task.
</Tip>

This page covers the web product itself:

* [Cloud environments](#cloud-environments): where sessions run, and where to configure that
* [GitHub authentication options](#github-authentication-options): two ways to connect GitHub
* [Move tasks between web and terminal](#move-tasks-between-web-and-terminal) with `--cloud` and `--teleport`
* [Work with sessions](#work-with-sessions): reviewing, sharing, archiving, deleting
* [Auto-fix pull requests](#auto-fix-pull-requests): respond automatically to CI failures and review comments
* [Security and isolation](#security-and-isolation): how sessions are isolated
* [Limitations](#limitations): rate limits and platform restrictions

## Cloud environments

Every cloud session runs in a [cloud environment](/docs/en/cloud-environments), the saved configuration that controls network access, environment variables, and setup scripts. When you onboard, Claude Code sets up a **Default** environment with [**Trusted** network access](/docs/en/cloud-environments#access-levels). See [The Default environment](/docs/en/cloud-environments#the-default-environment) for how it's created and how sessions choose an environment when you have more than one.

The same environments apply wherever you start a cloud session: the web, the terminal, [Claude Tag](https://claude.com/docs/claude-tag/overview), [routines](/docs/en/routines), and the mobile and Desktop apps. Claude Tag channel sessions use [organization-shared environments](/docs/en/cloud-environments#organization-shared-environments) only.

See [Configure cloud environments](/docs/en/cloud-environments) to change what an environment allows, set variables, or add a setup script, and [Installed tools](/docs/en/cloud-environments#installed-tools) for what sessions include without any configuration.

## GitHub authentication options

Cloud sessions need access to your GitHub repositories to clone code and push branches. You can grant access in two ways:

| Method           | How it works                                                                                | Best for                                                                |
| :--------------- | :------------------------------------------------------------------------------------------ | :---------------------------------------------------------------------- |
| **GitHub App**   | Authorize the Claude GitHub App during [web onboarding](/docs/en/web-quickstart).                | Browser onboarding; teams that want [Auto-fix](#auto-fix-pull-requests) |
| **`/web-setup`** | Run `/web-setup` in your terminal to sync your local `gh` CLI token to your Claude account. | Individual developers who already use `gh`                              |

<Note>
  With either method, a cloud session can access any repository the connecting GitHub account can see, not just the repositories the Claude GitHub App is installed on. App installation enables PR webhooks for [Auto-fix](#auto-fix-pull-requests); it is not a session-level access control. To restrict which repositories your team can reach from cloud sessions, restrict access on GitHub itself, for example by limiting team or repository membership for the connected GitHub accounts.
</Note>

Either method works. [`/schedule`](/docs/en/routines) checks for either form of access and prompts you to run `/web-setup` if neither is configured. See [Connect from your terminal](/docs/en/web-quickstart#connect-from-your-terminal) for the `/web-setup` walkthrough.

The GitHub App is required for [Auto-fix](#auto-fix-pull-requests), which uses the App to receive PR webhooks. If you connect with `/web-setup` and later want Auto-fix, install the App on those repositories.

Team and Enterprise Owners can disable `/web-setup` with the Quick web setup toggle at [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

<Note>
  Organizations with [Zero Data Retention](/docs/en/zero-data-retention) enabled can't use `/web-setup` or other cloud session features.
</Note>

## Move tasks between web and terminal

These workflows require the [Claude Code CLI](/docs/en/quickstart) signed in to the same claude.ai account. You can start new cloud sessions from your terminal, or pull cloud sessions into your terminal to continue locally. Cloud sessions persist even if you close your laptop, and you can monitor them from anywhere including the Claude mobile app.

<Note>
  From the CLI, session handoff is one-way: you can pull cloud sessions into your terminal with `--teleport`, but you can't push an existing terminal session to the web. The `--cloud` flag with a task description creates a new cloud session for your current repository; with a session ID or claude.ai/code URL it instead targets that existing session, [queueing a message or attaching your terminal](/docs/en/claude-code-on-the-web#send-follow-ups-from-the-cli). The [Desktop app](/docs/en/desktop#continue-in-another-surface) provides a Continue in menu that can send a local session to the web.
</Note>

### From terminal to web

Start a cloud session from the command line with the `--cloud` flag:

```bash theme={null}
claude --cloud "Fix the authentication bug in src/auth/login.ts"
```

This creates a new cloud session on claude.ai. The cloud VM clones your current directory's GitHub remote at your current branch, not your local checkout, so push first if you have local commits. `--cloud` works with a single repository at a time. The task runs in the cloud while you continue working locally. The older `--remote` spelling still works as a deprecated alias for `--cloud`.

While the cloud container starts, the CLI shows a live checklist of setup steps, such as cloning the repository and running your [setup script](/docs/en/cloud-environments#setup-scripts). It queues messages you type during provisioning and sends them once the session is ready.

<Note>
  `--cloud` creates cloud sessions. `--remote-control` is unrelated: it exposes a local CLI session for monitoring from the web. See [Remote Control](/docs/en/remote-control).
</Note>

Use `/tasks` in the Claude Code CLI to check progress, or open the session on claude.ai or the Claude mobile app to interact directly. From there you can steer Claude, provide feedback, or answer questions as in any other conversation.

If Claude asks a question and the session sits idle, you can still answer when you come back, up to [environment expiry](#environment-expired), and the session continues from your answer.

#### Tips for cloud tasks

**Plan locally, execute remotely**: for complex tasks, start Claude in plan mode to collaborate on the approach, then send work to the cloud:

```bash theme={null}
claude --permission-mode plan
```

In plan mode, Claude reads files, runs commands to explore, and proposes a plan without editing source code. Once you're satisfied, save the plan to the repo, commit, and push so the cloud VM can clone it. Then start a cloud session for autonomous execution:

```bash theme={null}
claude --cloud "Execute the migration plan in docs/migration-plan.md"
```

This pattern gives you control over the strategy while letting Claude execute autonomously in the cloud.

**Run tasks in parallel**: each `--cloud` command creates its own cloud session that runs independently. You can start multiple tasks and they'll all run simultaneously in separate sessions:

```bash theme={null}
claude --cloud "Fix the flaky test in auth.spec.ts"
claude --cloud "Update the API documentation"
claude --cloud "Refactor the logger to use structured output"
```

Monitor all sessions with `/tasks` in the Claude Code CLI. When a session completes, you can create a PR from the web interface or [teleport](#from-web-to-terminal) the session to your terminal to continue working.

#### Send local repositories without GitHub

When you run `claude --cloud` from a repository that isn't connected to GitHub, Claude Code bundles your local repository and uploads it directly to the cloud session. The bundle includes your full repository history across all branches, plus any uncommitted changes to tracked files.

This fallback activates automatically when GitHub access isn't available. To force it even when GitHub is connected, set `CCR_FORCE_BUNDLE=1`:

```bash theme={null}
CCR_FORCE_BUNDLE=1 claude --cloud "Run the test suite and fix any failures"
```

Bundled repositories must meet these limits:

* The directory must be a git repository with at least one commit
* The bundled repository must be under 100 MB. Larger repositories fall back to bundling only the current branch, then to a single squashed snapshot of the working tree, and fail only if the snapshot is still too large
* Untracked files are not included; run `git add` on files you want the cloud session to see
* Sessions created from a bundle can't push back to a remote unless you also have [GitHub authentication](#github-authentication-options) configured

### Send follow-ups from the CLI

Once a cloud session is running, wherever it executes, send it a follow-up message from the `claude` CLI on any machine where you're logged in with `claude auth login`. The CLI authenticates with your Anthropic account credentials and sends no local session state, so the command doesn't need to run from the machine that started the session, and it's the same in every shell, including PowerShell.

The primary form posts one message and exits:

```bash theme={null}
claude -p "your message" --cloud <session-id>
```

The CLI queues the message into the session and exits without waiting for a reply. Use it to steer a long-running session, queue the next step while the current one is still finishing, or send follow-ups from a [CI script](/docs/en/self-hosted-environments-testing#run-the-test-loop). You can also pipe the message on stdin instead of passing it as an argument: `echo "your message" | claude -p --cloud <session-id>`.

Without `-p`, `claude --cloud <session-id>` attaches your terminal to the session so you can converse with it directly. Interactive attach is rolling out gradually; if you see `Attaching to an existing cloud session is not enabled for your account`, contact your Anthropic account team. The `-p` queue-and-exit form isn't affected by this rollout.

For `<session-id>`, pass the bare ID, such as `session_...` or `cse_...`, or the session's `claude.ai/code/<id>` URL, with or without the scheme or query string. Find the ID in your session list at claude.ai/code.

<Note>
  `--cloud` requires an Anthropic account. It's not available when Claude Code is configured for Amazon Bedrock, Google Cloud's Agent Platform, or another third-party provider. An [LLM gateway](/docs/en/llm-gateway) configured only through `ANTHROPIC_BASE_URL` doesn't count as a third-party provider for this check, but you still need to sign in with `claude auth login`. Your organization's `allow_remote_sessions` policy must also be enabled. An Owner can turn it on in the Claude Code admin settings at claude.ai/admin-settings/claude-code.
</Note>

#### Output and errors

On success, the queue-and-exit form prints the session ID and a link to view the session:

```
Sent to cloud session.
Session ID: session_01DiUkqY2kzbUbDmW1w96rfi
View: https://claude.ai/code/session_01DiUkqY2kzbUbDmW1w96rfi?from=cli&m=0
```

Pass `--output-format json` for a machine-readable result: `{ok, session_id, url}` on success, or `{ok: false, session_id, error}` when the send fails, for example when the session is missing or archived. Configuration errors, such as an unsupported provider or a disabled organization policy, print to stderr without JSON. `--output-format stream-json` isn't supported with `--cloud <session-id>`.

The CLI prefixes errors with `Error: `. A failed delivery is wrapped as `failed to send message to cloud session <id>: <reason>`.

| Message                                                                                                                     | What it means                                                                                                                                                                                                                                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Cloud sessions aren't available with <provider>. They run on Anthropic's infrastructure and require an Anthropic account.` | Claude Code is configured for a third-party provider. The message names the provider with the label your configuration uses, such as `Amazon Bedrock` or `Google Vertex AI`. Remove that provider's configuration, for example by unsetting `CLAUDE_CODE_USE_BEDROCK`, and sign in with an Anthropic account (`claude auth login`). |
| `Cloud sessions are disabled by your organization's policy. Contact your organization admin to enable them.`                | The `allow_remote_sessions` organization policy is off.                                                                                                                                                                                                                                                                             |
| `Attaching to an existing cloud session is not enabled for your account.`                                                   | Interactive attach, without `-p`, is rolling out gradually and isn't available for your account yet. The queue-and-exit form, `-p "..." --cloud <session-id>`, works regardless.                                                                                                                                                    |
| `Session not found: <id>`                                                                                                   | The ID or URL doesn't match a session you can access. Check it against the session's claude.ai/code URL.                                                                                                                                                                                                                            |
| `cloud session <id> is archived and cannot accept new messages`                                                             | The session has been archived. Start a new session instead.                                                                                                                                                                                                                                                                         |

### From web to terminal

Pull a cloud session into your terminal using any of these:

* **Using `--teleport`**: from the command line, run `claude --teleport` for an interactive session picker, or `claude --teleport <session-id>` to resume a specific session directly. If you have uncommitted changes, you'll be prompted to stash them first.
* **Using `/teleport`**: inside an existing CLI session, run `/teleport` or `/tp` to open the same session picker without restarting Claude Code.
* **From `/tasks`**: run `/tasks` to see your background sessions, then press `t` to teleport into one.
* **From the web interface**: select **Open in > Terminal** from the session menu to copy a command you can paste into your terminal.
* **From inside the cloud session**: type `/teleport` and Claude Code replies with the exact `claude --teleport <session-id>` command for that session, ready to run from a checkout of the repository. Requires Claude Code v2.1.223 or later in the session's environment.

When you teleport a session, Claude verifies you're in the correct repository, fetches and checks out the branch from the cloud session, and loads the full conversation history into your terminal. The terminal gets its own copy of the session: new work there stays local and doesn't appear in the cloud session on claude.ai or the Claude mobile app. To keep steering from your phone after teleporting, start [`/remote-control`](/docs/en/remote-control) in the local session.

`--teleport` is distinct from `--resume`. `--resume` reopens a conversation from this machine's local history and doesn't list cloud sessions; `--teleport` pulls a cloud session and its branch.

#### Teleport requirements

Teleport checks these requirements before resuming a session. If any requirement isn't met, you'll see an error or be prompted to resolve the issue.

| Requirement        | Details                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Clean git state    | Your working directory must have no uncommitted changes. Teleport prompts you to stash changes if needed.                                                                                                                                                                                                                                                                                                                                                                          |
| Correct repository | You must run `--teleport` from a checkout of the same repository, not a fork. If you run it from a checkout of a different repository, Claude Code shows an error that names both the session's repository and your checkout's. If Claude Code can't parse your remote into a hostname, for example an SSH host alias like `git@work:owner/repo.git`, it asks you to confirm, and accepts the checkout when the remote's owner and repository name match the session's repository. |
| Branch available   | The branch from the cloud session must have been pushed to the remote. Teleport automatically fetches and checks it out.                                                                                                                                                                                                                                                                                                                                                           |
| Same account       | You must be authenticated to the same claude.ai account used in the cloud session.                                                                                                                                                                                                                                                                                                                                                                                                 |

#### `--teleport` is unavailable

Teleport requires claude.ai subscription authentication. If you're authenticated via API key, run `/login` to sign in with your claude.ai account instead. If the error names your provider instead, cloud sessions aren't available through third-party providers; see the [error table](#output-and-errors). If you're already signed in via claude.ai and `--teleport` is still unavailable, your organization may have disabled cloud sessions.

## Work with sessions

Sessions appear in the sidebar at claude.ai/code. From there you can review changes, share with teammates, archive finished work, or delete sessions permanently.

### Manage context

Cloud sessions support [built-in commands](/docs/en/commands) that produce text output. Commands that only run in the terminal interface, such as `/plugin` or `/resume`, aren't available. Commands that open a picker or panel in the terminal behave differently in cloud sessions:

* **`/model`, `/effort`, `/fast`, `/color`, and `/rename`**: pass the value as an argument, for example `/model sonnet`, instead of opening the terminal picker or slider. The argument forms require Claude Code v2.1.205 or later in the session's environment and follow each command's [availability notes](/docs/en/commands#all-commands): `/effort` reports `Not applied` while a model's [launch-default effort hold](/docs/en/model-config#adjust-effort-level) is in force, and `/fast` works only in a session that started with fast mode turned on.
* **`/config`**: on the web, opens the Claude Code section of your settings instead of setting a value, and text after the command, including `key=value`, is ignored. To change settings for a cloud session, use [environment variables](/docs/en/cloud-environments#set-environment-variables) or commit [settings files](/docs/en/settings) to the repository.

For context management specifically:

| Command    | Works in cloud sessions | Notes                                                                                                                    |
| :--------- | :---------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `/compact` | Yes                     | Summarizes the conversation to free up context. Accepts optional focus instructions like `/compact keep the test output` |
| `/context` | Yes                     | Shows what's currently in the context window                                                                             |
| `/clear`   | No                      | Start a new session from the sidebar instead                                                                             |

Auto-compaction runs automatically when the context window approaches capacity. Claude Code on the web sets [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/docs/en/env-vars) in cloud sessions itself, so compaction triggers partway through the [auto-compact window](/docs/en/model-config#set-the-auto-compact-window) rather than when the window fills. That value overrides one you add in your [environment variables](/docs/en/cloud-environments#set-environment-variables), so adding the variable there doesn't change when compaction triggers.

To change the auto-compact window instead, set [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/docs/en/env-vars) in your environment variables, or run [`/autocompact`](/docs/en/commands#all-commands) with a token count in a session where the variable isn't set.

[Subagents](/docs/en/sub-agents) work the same way they do locally. Claude can spawn them with the Agent tool to offload research or parallel work into a separate context window, keeping the main conversation lighter. Subagents defined in your repo's `.claude/agents/` are picked up automatically.

[Agent teams](/docs/en/agent-teams) are off by default but can be enabled by adding `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` to your [environment variables](/docs/en/cloud-environments#set-environment-variables).

### Review changes

Each session shows a diff indicator with lines added and removed, like `+42 -18`. Select it to open the diff view, leave inline comments on specific lines, and send them to Claude with your next message.

Claude Code computes these diffs, including the per-file diffs shown as Claude edits, from raw git blob content, so diff drivers and `textconv` filters configured in the repository don't apply.

See [Review and iterate](/docs/en/web-quickstart#review-and-iterate) for the full walkthrough including PR creation. To have Claude monitor the PR for CI failures and review comments automatically, see [Auto-fix pull requests](#auto-fix-pull-requests).

### Share sessions

To share a session, toggle its visibility according to the account types below. After that, share the session link as-is. Recipients see the latest state when they open the link, but their view doesn't update in real time.

#### Share from an Enterprise or Team account

For Enterprise and Team accounts, the two visibility options are **Private** and **Team**. Team visibility makes the session visible to other members of your claude.ai organization. [Claude in Slack](/docs/en/slack) sessions are automatically shared with Team visibility.

Repository access verification is enabled by default, based on the GitHub account connected to the recipient's account. Your account's display name is visible to all recipients with access.

#### Share from a Max or Pro account

For Max and Pro accounts, the two visibility options are **Private** and **Public**. Public visibility makes the session visible to any user logged into claude.ai.

Check your session for sensitive content before sharing. Sessions may contain code and credentials from private GitHub repositories. Repository access verification is not enabled by default.

To require recipients to have repository access, or to hide your name from shared sessions, go to [**Settings > Claude Code > Sharing settings**](https://claude.ai/settings/claude-code).

### Archive sessions

You can archive sessions to keep your session list organized. Archived sessions are hidden from the default session list but can be viewed by filtering for archived sessions.

To archive a session, hover over the session in the sidebar and select the archive icon.

### Delete sessions

Deleting a session permanently removes the session and its data. This action can't be undone. You can delete a session in two ways:

* **From the sidebar**: filter for archived sessions, then hover over the session you want to delete and select the delete icon
* **From the session menu**: open a session, select the dropdown next to the session title, and select **Delete**

You will be asked to confirm before a session is deleted.

## Auto-fix pull requests

Claude can watch a pull request and automatically respond to CI failures and review comments. Claude subscribes to GitHub activity on the PR, and when a check fails or a reviewer leaves a comment, Claude investigates and pushes a fix if one is clear.

<Note>
  Auto-fix requires the Claude GitHub App to be installed on your repository. If you haven't already, install it from the [GitHub App page](https://github.com/apps/claude) or when prompted during [setup](/docs/en/web-quickstart#connect-github).
</Note>

There are a few ways to turn on auto-fix depending on where the PR came from and what device you're using:

* **PRs created in Claude Code on the web**: open the CI status bar and select **Auto-fix**
* **From your terminal**: run [`/autofix-pr`](/docs/en/commands) while on the PR's branch. Claude Code detects the open PR with `gh`, spawns a web session, and turns on auto-fix in one step
* **From the mobile app**: tell Claude to auto-fix the PR, for example "watch this PR and fix any CI failures or review comments"
* **Any existing PR**: paste the PR URL into a session and tell Claude to auto-fix it

Auto-fix is a per-PR toggle. To stop monitoring, open the CI status bar in the web session and clear the **Auto-fix** toggle, or tell Claude to stop watching the PR.

### How Claude responds to PR activity

When auto-fix is active, Claude receives GitHub events for the PR including new review comments and CI check failures. For each event, Claude investigates and decides how to proceed:

* **Clear fixes**: if Claude is confident in a fix and it doesn't conflict with earlier instructions, Claude makes the change, pushes it, and explains what was done in the session
* **Ambiguous requests**: if a reviewer's comment could be interpreted multiple ways or involves something architecturally significant, Claude asks you before acting
* **Duplicate or no-action events**: if an event is a duplicate or requires no change, Claude notes it in the session and moves on

GitHub does not emit a webhook when the base branch advances and creates a merge conflict, so auto-fix can't react to conflicts on its own. To resolve a conflict, open the session and ask Claude to rebase.

Claude may reply to review comment threads on GitHub as part of resolving them. These replies are posted using your GitHub account, so they appear under your username, but each reply is labeled as coming from Claude Code so reviewers know it was written by the agent and not by you directly.

<Warning>
  If your repository uses comment-triggered automation such as Atlantis, Terraform Cloud, or custom GitHub Actions that run on `issue_comment` events, be aware that Claude can reply on your behalf, which can trigger those workflows. Review your repository's automation before enabling auto-fix, and consider disabling auto-fix for repositories where a PR comment can deploy infrastructure or run privileged operations.
</Warning>

## Security and isolation

Each cloud session is separated from your machine and from other sessions through several layers:

* **Isolated virtual machines**: each session runs in an isolated, Anthropic-managed VM. Sessions your organization routes to a [self-hosted environment](/docs/en/self-hosted-environments) run on your own infrastructure instead, where isolation is your deployment's responsibility
* **Network access controls**: in Anthropic-hosted environments, network access is limited by default and can be disabled. In a self-hosted environment, you restrict session egress at your own network boundary. When running with network access disabled, Claude Code can still communicate with the Anthropic API, which may allow data to exit the VM.
* **Credential protection**: in Anthropic-hosted environments, sensitive credentials such as git credentials or signing keys are never inside the sandbox with Claude Code; authentication is handled through a secure proxy using scoped credentials. Sessions in a self-hosted environment authenticate git with credentials your deployment provides; [Configure git](/docs/en/self-hosted-environments-deploy#configure-git) covers the options, including per-session minted credentials and the same proxy.
* **Secure analysis**: code is analyzed and modified within the session's isolated environment before creating PRs

## Troubleshooting

For runtime API errors that appear in the conversation such as `API Error: 500`, `529 Overloaded`, `429`, or `Prompt is too long`, see the [Error reference](/docs/en/errors). Those errors and their fixes are shared with the CLI and Desktop app. The sections below cover issues specific to cloud sessions.

### Session creation failed

If a new session fails to start with `Session creation failed` or stalls at provisioning, Claude Code could not allocate a VM for the session.

* Check [status.claude.com](https://status.claude.com) for cloud session incidents
* Retry after a minute, as capacity is provisioned on demand
* Confirm your repository is reachable. The connecting GitHub account must have access to the repository on GitHub, either through the Claude GitHub App authorization or a `gh` token synced via `/web-setup`. Installing the App on the repository isn't required. See [GitHub authentication options](#github-authentication-options).

### Unable to get organization UUID

`claude --cloud` and `claude --teleport` require sign-in with a claude.ai account. If you authenticate with an API key, or your stored account details are stale, these commands fail with `Unable to get organization UUID` or a message that API key authentication is not sufficient.

Run `/login` to sign in with your claude.ai account, then retry the command. If the error names your provider instead, see the [error table](#output-and-errors): cloud sessions aren't available through third-party providers.

### Remote Control session expired or access denied

`--teleport` connects through the same Remote Control session infrastructure that cloud sessions use, so authentication and session-expiry errors surface with Remote Control wording. You may see `Remote Control session expired` or `Access denied`. The connection token is short-lived and scoped to your account.

* Run `/login` locally to refresh your credentials, then reconnect
* Confirm you are signed in to the same account that owns the session
* If you see `Remote Control may not be available for this organization`, an Owner has not enabled cloud sessions for your organization

### Environment expired

Cloud sessions stop after a period of inactivity and the session's VM is reclaimed. On the web, the session is marked expired in the session list.

Reopen the session from [claude.ai/code](https://claude.ai/code) to provision a fresh VM with your conversation history restored.

## Limitations

Before relying on cloud sessions for a workflow, account for these constraints:

* **Rate limits**: Claude Code on the web shares rate limits with all other Claude and Claude Code usage within your account. Running multiple tasks in parallel consumes more rate limits proportionately. There is no separate compute charge for the cloud VM.
* **Repository authentication**: you can only move sessions from web to local when you are authenticated to the same account
* **Platform restrictions**: repository cloning and pull request creation require GitHub. Self-hosted [GitHub Enterprise Server](/docs/en/github-enterprise-server) instances are supported for Team and Enterprise plans. GitLab, Bitbucket, and other non-GitHub repositories can be sent to cloud sessions as a [local bundle](#send-local-repositories-without-github), but the session can't push results back to the remote
* **Organization IP allowlist**: cloud sessions call the Anthropic API from Anthropic-managed infrastructure, not your network, while sessions in a [self-hosted environment](/docs/en/self-hosted-environments) call it from your own network. If your organization has [IP allowlisting](https://support.claude.com/en/articles/13200993-restrict-access-to-claude-with-ip-allowlisting) enabled, every Anthropic-hosted cloud session fails with an authentication error. The same applies to [Code Review](/docs/en/code-review) and to [routines](/docs/en/routines) that run on Anthropic-hosted environments; a routine routed to a self-hosted environment calls the API from your own network. Contact [Anthropic support](https://support.claude.com/) to exempt Anthropic-hosted services from your organization's IP allowlist.

## Related resources

* [Cloud environments](/docs/en/cloud-environments): configure network access, environment variables, and setup scripts for cloud sessions
* [Ultrareview](/docs/en/ultrareview): run a deep multi-agent code review in a cloud sandbox
* [Routines](/docs/en/routines): automate work on a schedule, via API call, or in response to GitHub events
* [Hooks configuration](/docs/en/hooks): run scripts at session lifecycle events
* [Settings reference](/docs/en/settings): all configuration options
* [Security](/docs/en/security): isolation guarantees and data handling
* [Data usage](/docs/en/data-usage): what Anthropic retains from cloud sessions
* [Claude Tag](https://claude.com/docs/claude-tag/overview): an organization-managed @Claude in Slack that runs on the same cloud infrastructure
