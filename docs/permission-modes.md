> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Choose a permission mode

> Control whether Claude asks before editing files or running commands. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai.

When Claude wants to edit a file, run a shell command, or make a network request, it pauses and asks you to approve the action. Permission modes control how often that pause happens. The mode you pick shapes the flow of a session: Manual mode has you review each action as it comes, while looser modes let Claude work in longer uninterrupted stretches and report back when done. Pick more oversight for sensitive work, or fewer interruptions when you trust the direction.

## Available modes

Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode.

| Mode                                                                | What runs without asking                                                                                  | Best for                                |
| :------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------- | :-------------------------------------- |
| `default`                                                           | Reads only                                                                                                | Getting started, sensitive work         |
| [`acceptEdits`](#auto-approve-file-edits-with-acceptedits-mode)     | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.)                    | Iterating on code you're reviewing      |
| [`plan`](#analyze-before-you-edit-with-plan-mode)                   | Reads, plus classifier-approved commands when [auto mode](#eliminate-prompts-with-auto-mode) is available | Exploring a codebase before changing it |
| [`auto`](#eliminate-prompts-with-auto-mode)                         | Everything, with background safety checks                                                                 | Long tasks, reducing prompt fatigue     |
| [`dontAsk`](#allow-only-pre-approved-tools-with-dontask-mode)       | Only pre-approved tools                                                                                   | Locked-down CI and scripts              |
| [`bypassPermissions`](#skip-all-checks-with-bypasspermissions-mode) | Everything                                                                                                | Isolated containers and VMs only        |

The mode that reviews every action is named **Manual** in the CLI, in `claude --help`, in the VS Code and JetBrains extensions, and in the desktop app. Its config value is `default`, which is what hooks and SDK integrations use. The CLI accepts `manual` as an alias wherever you type the value, for example `claude --permission-mode manual` or `"defaultMode": "manual"`. The Manual label and the `manual` alias require Claude Code v2.1.200 or later. The desktop app's label doesn't depend on your CLI version.

Writes to [protected paths](#protected-paths) are never auto-approved except in `bypassPermissions` mode and in planning sessions with bypass permissions available.

Modes set the baseline. Layer [permission rules](/docs/en/permissions#manage-permissions) on top to pre-approve or block specific tools. These controls apply in every mode, including `bypassPermissions`:

* deny rules and explicit ask rules, which apply to every tool but can't block [`EndConversation`](/docs/en/tools-reference#endconversation-tool-behavior) while any other tool remains
* the [org `ask` setting on connector tools](/docs/en/mcp#organization-controls-on-connector-tools)
* the [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool) marker

Allow rules have no effect in `bypassPermissions` because everything else is already approved.

## Switch permission modes

You can switch modes mid-session, at startup, or as a persistent default. The mode is set through these controls, not by asking Claude in chat. Select your interface below to see how to change it.

<Tabs>
  <Tab title="CLI">
    **During a session**: press `Shift+Tab` to cycle `default` → `acceptEdits` → `plan`. The status bar shows the active mode as `⏸ plan mode on`, `⏵⏵ accept edits on`, `⏵⏵ auto mode on`, `⏵⏵ don't ask on`, or `⏵⏵ bypass permissions on`. Manual mode, `default` in that cycle, shows a gray `⏸ manual mode on` badge.

    Not every mode is in the default cycle:

    * `auto`: appears when your account meets the [auto mode requirements](#eliminate-prompts-with-auto-mode); cycling to it switches modes without a confirmation prompt
    * `bypassPermissions`: appears after you start with `--permission-mode bypassPermissions`, `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, or `permissions.defaultMode: "bypassPermissions"` in [settings](/docs/en/settings#permission-settings); the `--allow-` variant adds the mode to the cycle without activating it
    * `dontAsk`: never appears in the cycle; set it with `--permission-mode dontAsk`

    Enabled optional modes slot in after `plan`, with `bypassPermissions` first and `auto` last. If you have both enabled, you will cycle through `bypassPermissions` on the way to `auto`.

    **At startup**: pass the mode as a flag.

    ```bash theme={null}
    claude --permission-mode plan
    ```

    **As a default**: set `defaultMode` in a [settings file](/docs/en/settings#settings-files) such as `~/.claude/settings.json`:

    ```json theme={null}
    {
      "permissions": {
        "defaultMode": "acceptEdits"
      }
    }
    ```

    The same `--permission-mode` flag works with `-p` for [non-interactive runs](/docs/en/headless).
  </Tab>

  <Tab title="VS Code">
    **During a session**: click the mode indicator at the bottom of the prompt box.

    **As a default**: set `claudeCode.initialPermissionMode` in your VS Code user settings, or use the Claude Code extension settings panel.

    The mode indicator shows these labels, mapped to the mode each one applies:

    | UI label           | Mode                |
    | :----------------- | :------------------ |
    | Manual             | `default`           |
    | Edit automatically | `acceptEdits`       |
    | Plan               | `plan`              |
    | Auto               | `auto`              |
    | Bypass permissions | `bypassPermissions` |

    Auto mode appears in the mode indicator when your account meets every requirement listed in the [auto mode section](#eliminate-prompts-with-auto-mode). The `claudeCode.initialPermissionMode` setting does not accept `auto`. To switch a session into auto mode, select **Auto** from the mode indicator.

    Bypass permissions requires the **Allow dangerously skip permissions** toggle in the extension settings before it appears in the mode indicator.

    See the [VS Code guide](/docs/en/vs-code) for extension-specific details.
  </Tab>

  <Tab title="JetBrains">
    The JetBrains plugin runs Claude Code in the IDE terminal, so switching modes works the same as in the CLI: press `Shift+Tab` to cycle, or pass `--permission-mode` when launching.
  </Tab>

  <Tab title="Desktop">
    **During a session**: in the Code tab, use the mode selector next to the send button. Not every mode appears in the selector:

    * **Auto**: appears when your account meets the [auto mode requirements](#eliminate-prompts-with-auto-mode)
    * **Bypass permissions**: requires the **Allow bypass permissions mode** toggle in Desktop settings on Pro and Max plans; on Team and Enterprise plans, organization policy controls it instead

    The Cowork tab doesn't use these modes. Cowork has its own permission modes, enabled separately, and the Cowork tab shows no mode selector at all until a mode beyond its default is enabled for your account. See the [Cowork docs](https://claude.com/docs/cowork/overview).

    For desktop-specific details, see [Choose a permission mode](/docs/en/desktop#choose-a-permission-mode) in the Desktop guide.

    **As a default**: set `defaultMode` in [settings](/docs/en/settings#settings-files). The desktop app reads the same settings files as the CLI and applies the mode to new local sessions.

    A mode you pick in the mode selector is remembered per folder and takes precedence over `defaultMode` for that folder. Plan is the exception: picking it applies to the current session only.

    This example sets Plan mode as the default for new local sessions:

    ```json theme={null}
    {
      "permissions": {
        "defaultMode": "plan"
      }
    }
    ```
  </Tab>

  <Tab title="Web and mobile">
    Use the mode dropdown next to the prompt box on [claude.ai/code](https://claude.ai/code) or in the mobile app. Permission prompts appear in claude.ai for approval. Which modes appear depends on where the session runs:

    * **Cloud sessions** on [Claude Code on the web](/docs/en/claude-code-on-the-web): Accept edits, Plan, and Auto. Accept edits corresponds to `default` mode: cloud sessions pre-approve file edits regardless of mode, so the dropdown shows Accept edits instead of Manual. Cloud sessions still honor `defaultMode: "acceptEdits"` from settings. Auto mode appears only when your organization allows it and the selected model supports it. Bypass permissions isn't available.
    * **[Remote Control](/docs/en/remote-control) sessions** on your local machine: Manual, Accept edits, and Plan. You can't select Auto or Bypass permissions from the app. The dropdown shows the mode the local session is in, including a mode set from the terminal, and updates when the mode changes in the app or in the terminal. The one exception is Bypass permissions: the session never reports that mode to claude.ai, so switching into it from the terminal doesn't change what the dropdown shows. Before v2.1.202, sessions connected with `/remote-control` or `claude --remote-control` didn't report their mode at all, so claude.ai and the mobile app could show a mode the session wasn't in. The mismatch affected only the label: Claude Code generated permission prompts from the session's actual mode, and they still appeared in the app for approval.

    For Remote Control, the host must be signed in with your claude.ai account; API keys are not supported. You can also set the starting mode when launching the host:

    ```bash theme={null}
    claude remote-control --permission-mode acceptEdits
    ```
  </Tab>
</Tabs>

## Auto-approve file edits with acceptEdits mode

`acceptEdits` mode lets Claude create and edit files in your working directory without prompting. The status bar shows `⏵⏵ accept edits on` while this mode is active.

In addition to file edits, `acceptEdits` mode auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`. These commands are also auto-approved when prefixed with safe environment variables such as `LANG=C` or `NO_COLOR=1`, or process wrappers such as `timeout`, `nice`, or `nohup`. Like file edits, auto-approval applies only to paths inside your working directory or `additionalDirectories`. Paths outside that scope, writes to [protected paths](#protected-paths), and all other Bash commands except the [built-in read-only set](/docs/en/permissions#read-only-commands) still prompt.

When the [PowerShell tool](/docs/en/tools-reference#powershell-tool) is enabled, `acceptEdits` mode also auto-approves `Set-Content`, `Add-Content`, `Clear-Content`, and `Remove-Item` on in-scope paths, along with their common aliases. The same scope and protected-path rules apply. A positional argument that contains a quote character, such as the apostrophe in `Set-Content .\notes.txt "It's done"`, still prompts even on in-scope paths, because Claude Code can't statically validate an argument whose quoted and unquoted readings differ. Pass the content through a named parameter such as `-Value` to avoid the prompt.

Use `acceptEdits` when you want to review changes in your editor or via `git diff` after the fact rather than approving each edit inline.

Press `Shift+Tab` once from Manual mode to enter it, or start with it directly:

```bash theme={null}
claude --permission-mode acceptEdits
```

## Analyze before you edit with plan mode

Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Except in sessions with [bypass permissions available](#skip-all-checks-with-bypasspermissions-mode), edits stay blocked until you approve the plan.

When [auto mode](/docs/en/auto-mode-config) is available and the `useAutoModeDuringPlan` setting is on, which it is by default, the classifier reviews shell commands during planning instead of prompting you. Approved commands run, and rejected ones are blocked. Otherwise, commands outside the [built-in read-only set](/docs/en/permissions#read-only-commands) prompt for approval, including when the sandbox's [auto-allow mode](/docs/en/sandboxing#sandbox-modes) is enabled. Sessions with [bypass permissions available](#skip-all-checks-with-bypasspermissions-mode) skip both paths; that section covers what still prompts there. In sessions without them, commands outside the read-only set prompted either way in v2.1.212 through v2.1.217.

Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`. You can also start in plan mode from the CLI:

```bash theme={null}
claude --permission-mode plan
```

Press `Shift+Tab` again to leave plan mode without approving a plan.

### Review and approve a plan

When the plan is ready, Claude presents it and asks how to proceed. From that prompt you can choose:

* **Yes, and use auto mode**: approve and start in [auto mode](#eliminate-prompts-with-auto-mode). When auto mode is unavailable, this option reads **Yes, auto-accept edits**. Sessions started with bypass permissions enabled show **Yes, and bypass permissions** instead.
* **Yes, manually approve edits**: approve and review each edit individually.
* **No, keep planning**: stay in plan mode and tell Claude what to change.

Approving a plan exits plan mode and switches the session to the permission mode each approve option describes, so Claude starts editing. To plan again, cycle back to plan mode with `Shift+Tab`, or prefix your next prompt with `/plan`.

Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds. When [`showClearContextOnPlanAccept`](/docs/en/settings#available-settings) is enabled, the list gains a first option that approves the plan and clears the planning context.

Accepting a plan also names the session from the plan content automatically, unless you've already set a name with `--name` or `/rename`.

### Set plan mode as the default

In a session the [VS Code extension](/docs/en/vs-code) started, a settings-file `defaultMode` doesn't set the starting mode. Set `claudeCode.initialPermissionMode` to `plan` in your VS Code user settings instead. Elsewhere, to make plan mode the default for a project, set `defaultMode` in `.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

<h2 id="eliminate-prompts-with-auto-mode">
  Eliminate permission prompts with auto mode
</h2>

<Note>
  Starting August 14, 2026, auto mode becomes the default permission mode for new sessions on Pro, Max, and Team plans. You can switch modes at any time. A default you set yourself stays in place unless you accept the one-time switch prompt, and a default your organization manages is unchanged. For details, see [the announcement](https://claude.com/blog/auto-mode-default-in-claude-code) on the blog.
</Note>

Auto mode lets Claude execute without routine permission prompts. A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read. Explicit [ask rules](/docs/en/permissions#manage-permissions) still force a prompt.

The classifier also reviews each message Claude sends to another agent with [`SendMessage`](/docs/en/tools-reference), plain or structured, before Claude Code delivers it, both in auto mode and in [plan mode while the classifier reviews commands](#analyze-before-you-edit-with-plan-mode); the send review requires Claude Code v2.1.222 or later.

The classifier also decides removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, including when the removal sits inside command or process substitution. Before v2.1.218, the plain forms prompted for approval instead, and the substitution forms prompted in v2.1.208 through v2.1.217.

Auto mode also nudges Claude to keep working without stopping for clarifying questions, though Claude still asks when your prompt or a skill explicitly relies on it. For stronger autonomous behavior while keeping permission prompts, set the [Proactive output style](/docs/en/output-styles) instead.

<Warning>
  Auto mode reduces permission prompts but does not guarantee safety. Use it for tasks where you trust the general direction, not as a replacement for review on sensitive operations.
</Warning>

Auto mode is available only when your account meets all of these requirements:

* **Plan**: All plans.
* **Organization**: on Team and Enterprise, auto mode is available by default. Administrators can turn it off for the organization by setting `permissions.disableAutoMode` to `"disable"` in [managed settings](/docs/en/permissions#managed-settings).
* **Model**: on the Anthropic API and [Claude Platform on AWS](/docs/en/claude-platform-on-aws), Claude Opus 4.6 or later, Sonnet 4.6 or later, or [Fable 5](/docs/en/model-config#work-with-fable-5). On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) sessions, only Claude Sonnet 5, Opus 4.7 or later, and Fable 5. Older models, including Sonnet 4.5, Opus 4.5, Haiku, and claude-3 models, are not supported on any provider.
* **Provider**: available by default on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in Claude apps gateway sessions.

If Claude Code reports auto mode as unavailable, one of these requirements is unmet; this is not a transient outage. A separate message that names a model and says auto mode "cannot determine the safety" of an action means a classifier request failed; that failure is usually transient, but on Amazon Bedrock it can repeat until your account can invoke the named model. See the [error reference](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action) for the causes and what to do.

If you set `defaultMode: "auto"` in [settings](/docs/en/settings#available-settings) and the session starts in `default` mode with no error, the setting is likely in `.claude/settings.json` or `.claude/settings.local.json`. Claude Code v2.1.142 and later ignore `auto` from those files so a repository cannot grant itself auto mode. Move it to `~/.claude/settings.json`. In a session the [VS Code extension](/docs/en/vs-code) started, a settings-file `defaultMode` doesn't set the starting mode: select the mode from the extension's mode indicator instead.

<h3 id="enable-auto-mode-on-bedrock-agent-platform-or-foundry">
  Auto mode on Bedrock, Agent Platform, or Foundry
</h3>

On [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), [Microsoft Foundry](/docs/en/microsoft-foundry), and signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) sessions, auto mode appears in the `Shift+Tab` cycle by default. Appearing in the cycle doesn't change the mode a session starts in. Except in sessions the [VS Code extension](/docs/en/vs-code) starts, where the extension resolves the starting mode, sessions still start in your [`defaultMode`](/docs/en/settings#available-settings), which is Manual unless you change it. Only Claude Sonnet 5, Opus 4.7 or later, and Fable 5 are supported on these providers.

To make auto mode the default starting mode, set `"permissions": {"defaultMode": "auto"}` in user or managed settings. In sessions the VS Code extension starts, select **Auto** from the mode indicator instead.

The [`/doctor`](/docs/en/commands#all-commands) checkup proposes this user-settings default on these providers the same way it does on the Anthropic API.

To prevent developers from using auto mode, set `disableAutoMode` to `"disable"` in [managed settings](/docs/en/permissions#managed-settings). This removes `auto` from the `Shift+Tab` cycle and rejects `--permission-mode auto` at startup.

In v2.1.158 through v2.1.206, auto mode was off on these providers until you set `CLAUDE_CODE_ENABLE_AUTO_MODE=1`, and Claude Code ignored `defaultMode: "auto"` on these providers unless the variable was also set. The variable is still accepted for compatibility and has no effect from v2.1.207 onward.

### What the classifier blocks by default

The classifier trusts your working directory and the remotes that were configured for it when the session started. A remote added or repointed during the session with `git remote add` or `git remote set-url` isn't trusted, and everything else is treated as external until you [configure trusted infrastructure](/docs/en/auto-mode-config). Before v2.1.200, remotes added mid-session were also trusted.

**Blocked by default**:

* Downloading and executing code, like `curl | bash`
* Sending sensitive data to external endpoints
* Production deploys and migrations
* Mass deletion on cloud storage
* Granting IAM or repo permissions
* Modifying shared infrastructure
* Irreversibly destroying files that existed before the session
* Force push
* Committing or pushing a change that would send secrets or sensitive data outside the repository when it runs, or widen what a deploy exposes. This covers a CI workflow or deploy configuration that hands a secret to a destination that doesn't already receive it, a script or setup step that reads a secret store and sends the data out, and a config change that widens what a deploy publishes, such as a registry, visibility, artifact, or sourcemap setting. The check applies on any branch, applies even when the repository is public, and fires when the change lands, whether or not that landing triggers the pipeline; clearing it requires naming the execution effect, not only the commit or push. Before v2.1.211, this check was scoped to the default branch instead: a push there was blocked when it carried sensitive content, changes concealed or misdescribed relative to what you asked for, content ported in from outside the repository, or routed around a review you asked for, and before v2.1.203 any direct push to the default branch was blocked
* `git reset --hard`, `git checkout -- .`, `git restore .`, `git clean -fd`, `git stash drop`, or `git stash clear`, which the classifier presumes would discard uncommitted changes
* `git commit --amend` when the commit at HEAD was not created in this session
* From v2.1.198, `git commit --amend` when the commit at HEAD has already been pushed. A message-only reword is not blocked: `--amend -m` with nothing newly staged, on a commit that Claude created during this session
* `terraform destroy`, `pulumi destroy`, `cdk destroy`, or `terragrunt destroy`, and applying a plan that destroys resources

Claude Code v2.1.195 and later block more categories by default. Several depend on [environment](/docs/en/auto-mode-config#define-trusted-infrastructure) entries, such as sensitive remote targets and protected IaC scopes, that you can narrow to concrete names.

* Writing to a secret manager, or changing DNS records or TLS certificates
* Merging a pull request no human has approved, approving Claude's own pull request, or disabling CI checks
* Posting a comment that is itself a command to automation, such as `atlantis apply` or a bot's `/deploy` or `/merge`
* Toggling, ramping, or deleting a production feature flag
* Applying infrastructure changes to a protected IaC scope, or draining and removing cluster nodes
* Writes to a shared compute cluster that reach beyond the resource you named, such as a label selector or `--all` that catches other users' jobs
* Creating Kubernetes resources that run on every node or intercept cluster traffic, such as DaemonSets and admission webhooks
* Interactive shells or port-forwards into a sensitive remote target
* Opening a tunnel or reverse shell that makes a local service reachable from the public internet
* Printing a live credential or token into the transcript or a file
* Accessing a location listed as a sensitive data location in your [environment](/docs/en/auto-mode-config#define-trusted-infrastructure), or copying data out of one. As of v2.1.198 this also blocks sending data from one to an audience the entry excludes
* Routing a package install around your internal package registry to a public registry. As of v2.1.198, this also applies when you've told Claude an internal registry or mirror exists in the conversation, not only when one is listed in your environment
* Running a command with a flag that disarms a safety guard, like `--insecure`
* Launching an autonomous agent loop that runs without human approval or a sandbox, such as one started with `--dangerously-skip-permissions` or `--no-sandbox`. As of v2.1.198 this also covers running a third-party agent or eval harness with isolation and per-action approval disabled, such as a runner started with `--yes-always`
* [Claude in Chrome](/docs/en/chrome) browser actions that could send page content, cookies, or credentials off-origin

Claude Code v2.1.198 and later also block these by default:

* Deleting files in `/tmp`, `$TMPDIR`, or another shared scratch or cache directory by wildcard, glob, or age filter rather than by a specific named path
* Including sensitive details in content sent, uploaded, published, or written to other people or shared systems, when your own message didn't authorize those details for that recipient. PR and issue bodies, commit messages, and comments count as this kind of outbound content when the repository is outside the trust boundary or public, including your organization's own public repositories; internal file paths, code names, live API response data such as emails or account identifiers, and infrastructure identifiers count as sensitive details. The PR, issue, and commit-message scoping requires Claude Code v2.1.200 or later. Live personal data from an API response in a PR or issue body, such as an email address, an account or organization identifier, or a usage metric, requires you to name those details and the recipient regardless of the repository's visibility or trust boundary. That check requires Claude Code v2.1.203 or later
* Sending keystrokes to Claude Code's own tmux pane to drive its own interface, which the classifier treats as Claude changing its own permissions or oversight

Claude Code v2.1.200 and later also block these by default:

* Commenting out, deleting, or force-passing a test or assertion that guards security behavior, such as auth, access control, input validation, or sandboxing
* Deleting or tearing down a stateful resource Claude didn't create in the session, when no more specific deletion rule applies and you didn't name that resource
* Repointing an API base URL, proxy endpoint, webhook receiver, or registry mirror at a third-party host that doesn't fit the task, including in example files like `.env.example`
* Changing where pushes go with `git remote set-url` or `git remote add`, unless you named the new remote
* Pushing secrets or personal or entrusted data to a repository known to be public, or pushing confidential material there that isn't part of that repository's own work. A dotfiles repository's own subject matter is the one exception for personal or entrusted data, and content from a private repository reaching any public surface is blocked the same way; both refinements require Claude Code v2.1.203 or later. Before v2.1.203, personal data was grouped with confidential material and blocked only when it wasn't part of that repository's own work. When a repository's visibility isn't established, the classifier doesn't block on that alone; it judges the content against the other rules instead
* Opening a pull request against a different repository or organization, forking with `gh repo fork`, or pushing to a third-party repository, unless you named that external target

Claude Code v2.1.203 and later also block these by default:

* Content from a sensitive local store, or from a file whose name, path, or type marks it as sensitive, entering a commit, a push, PR or issue text, a gist or paste, or a package publish, unless you named both the source and the destination. Session transcripts and conversation logs, credential and configuration dot-folders such as SSH keys, cloud credentials, browser profiles, and shell history, and user-data exports all count, and the repository being private doesn't clear it

Claude Code v2.1.205 and later also block these by default:

* Writing to Claude Code session transcripts, the `.jsonl` history files under `~/.claude/projects/` or your configured config directory, whether directly or through a shell command. The rule also covers the metadata lines Claude Code appends to each transcript entry for its own checks. A transcript is session state that Claude Code writes, not a working file, and a tampered entry reaches every later check once you resume the session, so auto mode blocks these writes as defense in depth. Reading a transcript isn't blocked
* A recursive forced delete such as `rm -rf "$VAR"` or `Remove-Item -Recurse -Force $dir` whose target is a shell variable, or a glob rooted at one, that isn't assigned anywhere in the conversation the classifier sees. The value came only from earlier command output, which the classifier never receives, so the classifier can't verify the deletion target against the other deletion rules. The classifier reads the conversation rather than command output by design, so it blocks the call instead of guessing at the target. The block clears when you name the exact path being deleted, or when Claude re-runs the delete with the resolved literal path written into the command. Deletes whose target the classifier can resolve aren't affected

**Allowed by default**:

* Local file operations in your working directory
* Installing dependencies declared in your lock files or manifests
* Reading `.env` and sending credentials to their matching API
* Read-only HTTP requests
* Pushing to any branch of the repository you're working in, including the default branch. A non-default branch whose name marks it as a deploy or publication target, such as `production` or `gh-pages`, isn't covered: the classifier judges a push there on its own terms. The push's content is still checked against the other rules, [`permissions.deny` rules](/docs/en/permissions#manage-permissions) can still block pushes to specific branches outright in every mode, and the remote's own branch protection still applies. Before v2.1.211, only pushes to the branch you started on, branches Claude created, and routine pushes to the default branch were allowed by default, and before v2.1.203 any direct push to the default branch was blocked

Claude Code v2.1.195 and later also allow these by default:

* Deleting the exact jobs Claude created earlier in the same session
* Reading, reviewing, or writing security-related code, configs, and threat models as part of your task
* Messages between agents working together in the same multi-agent session
* Sending data to the trusted domains, buckets, and services you list in [`environment`](/docs/en/auto-mode-config#define-trusted-infrastructure). This covers data flow only, not destructive or credential operations on the same infrastructure
* [Claude in Chrome](/docs/en/chrome) navigation to a trusted internal domain, localhost, or a URL you named

Sandbox network access requests are routed through the classifier rather than allowed by default. As of v2.1.198, the classifier reuses its verdict for a network host and port instead of re-running on every connection:

* An allow is reused until new content enters the conversation, at which point that host is checked again
* In the interactive CLI, a deny is dropped when the turn ends
* In [non-interactive mode](/docs/en/headless) and Agent SDK sessions there is no turn boundary, so a deny is reused for the rest of the run
* Changing your permission mode or rules drops all cached verdicts

Run `claude auto-mode defaults` to print the full rule lists as JSON. If routine actions get blocked, an administrator can add trusted repos, buckets, and services via the `autoMode.environment` setting: see [Configure auto mode](/docs/en/auto-mode-config).

Pushing to any branch of the repository you're working in and creating a pull request that matches your request run without a prompt, with the two exceptions the lists above cover. To require a human checkpoint before these actions while staying in auto mode, add `permissions.ask` rules: see [Common boundaries](/docs/en/auto-mode-config#common-boundaries).

### Boundaries you state in conversation

The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude "don't push" or "wait until I review before deploying", the classifier blocks matching actions even when the default rules would allow them. A boundary stays in force until you lift it in a later message. Claude's own judgment that a condition was met does not lift it.

Boundaries are not stored as rules. The classifier re-reads them from the transcript on each check, so a boundary can be lost if [context compaction](/docs/en/costs#reduce-token-usage) removes the message that stated it. For a hard guarantee, add a [deny rule](/docs/en/permissions#permission-rule-syntax) instead.

### When auto mode falls back

When auto mode can't approve your session's actions, what happens depends on the case:

* **A blocked action**: Claude Code shows a notification and lists the action in `/permissions` under the **Recently denied** tab, where you can press `r` to retry it with a manual approval. When the classifier produces [no verdict on the action](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action), because a safety check separate from auto mode refused the classifier's own request or its response didn't parse, Claude Code denies the action without the notification or the **Recently denied** entry.
* **Repeated blocks**: if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode. These thresholds are not configurable. Any allowed action resets the consecutive counter, while the total counter persists for the session and resets only when its own limit triggers a fallback. Claude Code doesn't count a denial toward either threshold when [a safety check separate from auto mode refuses the classifier's own request](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action); the linked entry covers how Claude Code handles those denials.
* **Sessions that can't prompt**: a [non-interactive](/docs/en/headless) `-p` run without a [`--permission-prompt-tool`](/docs/en/cli-reference#cli-flags) has no prompt to fall back to. When repeated blocks reach a threshold, the action doesn't run and Claude keeps working, in the main conversation and in its subagents alike. The same applies when a safety check separate from auto mode refuses the classifier's request. Claude Code doesn't stop the run in either case.
* **A mode switch during a check**: if you switch permission modes while a classifier check is pending, Claude Code discards a verdict the new mode wouldn't have requested rather than applying it: you're prompted for approval instead, or the action is auto-denied in [`dontAsk` mode](#allow-only-pre-approved-tools-with-dontask-mode).

Repeated blocks usually mean the classifier is missing context about your infrastructure. Use `/feedback` to report false positives, or have an administrator [configure trusted infrastructure](/docs/en/auto-mode-config).

<AccordionGroup>
  <Accordion title="How the classifier evaluates actions">
    Each action goes through a fixed decision order. The first matching step wins:

    1. Actions matching your [allow, ask, or deny rules](/docs/en/permissions#manage-permissions) resolve immediately. Writes to [protected paths](#protected-paths) route to the classifier even when an allow rule matches. Connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools) and MCP tools marked [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool) prompt you directly even when an allow rule matches. Content-scoped ask rules fall back to a permission prompt
    2. Read-only actions and file edits in your working directory are auto-approved, except writes to [protected paths](#protected-paths)
    3. Everything else goes to the classifier. A connector tool [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools) skips the classifier and prompts you directly, so an org-required approval is never auto-approved. As of v2.1.199, an MCP tool marked with [`_meta["anthropic/requiresUserInteraction"]`](/docs/en/mcp#require-approval-for-a-specific-tool) also skips the classifier and prompts you directly, so a consent step is never auto-approved on the tool author's behalf
    4. If the classifier blocks, Claude receives the reason and tries an alternative. In most sessions the reason is the fixed text `Blocked by classifier` rather than a written explanation, in Claude Code v2.1.208 and later; see [Review denials](/docs/en/auto-mode-config#review-denials)

    On entering auto mode, broad allow rules that grant arbitrary code execution are dropped:

    * Blanket `Bash(*)` or `PowerShell(*)`
    * Wildcarded interpreters like `Bash(python*)`
    * Package-manager run commands
    * `Agent` allow rules

    Narrow rules like `Bash(npm test)` carry over. Dropped rules are restored when you leave auto mode.

    The classifier sees user messages, tool calls, and your CLAUDE.md content. Tool results are stripped, so hostile content in a file or web page cannot manipulate it directly. A separate server-side probe scans incoming tool results and flags suspicious content before Claude reads it. For more on how these layers work together, see the [auto mode announcement](https://claude.com/blog/auto-mode) and the [engineering deep dive](https://www.anthropic.com/engineering/claude-code-auto-mode).
  </Accordion>

  <Accordion title="How auto mode handles subagents">
    The classifier checks [subagent](/docs/en/sub-agents) work at three points:

    1. Before a subagent starts, the delegated task description is evaluated, so a dangerous-looking task is blocked at spawn time.
    2. While the subagent runs, each of its actions goes through the classifier with the same rules as the parent session, and any `permissionMode` in the subagent's frontmatter is ignored.
    3. When the subagent finishes, the classifier reviews its full action history; if that return check flags a concern, a security warning is prepended to the subagent's results. When a separate API safety check refuses the review request itself, Claude Code still returns the subagent's results, prepended with a warning that the work is unreviewed and should be treated as untrusted.

    Step 1 requires Claude Code v2.1.178 or later. Earlier versions applied the classifier at steps 2 and 3, but did not evaluate the task description before the subagent started.
  </Accordion>

  <Accordion title="Cost and latency">
    The classifier runs on Claude Sonnet 5 by default rather than on your `/model` selection. A classifier model that Anthropic configures server-side takes precedence over that default. When your session's model is Claude Sonnet 4.6, or when [`availableModels`](/docs/en/model-config#restrict-model-selection) excludes Sonnet 5, the classifier runs on the session's model instead, or on an Opus model when the session runs on [Fable 5](/docs/en/model-config#work-with-fable-5); on providers other than the Anthropic API, that Opus fallback is the provider's default Opus model.

    The session's first auto-mode request validates the Sonnet 5 default: if the request succeeds, Sonnet 5 stays the session's classifier model, and if it fails because the model isn't available, the session uses the fallback instead. After that validation settles, the classifier's model doesn't change for the session.

    On Enterprise plans and on accounts that use the Claude API, [Claude Platform on AWS](/docs/en/claude-platform-on-aws), Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, classifier calls count toward your token usage. Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations.

    The classifier reuses a sandbox network verdict for a host and port, so repeated connections to the same host don't each add a check. [What the classifier blocks by default](#what-the-classifier-blocks-by-default) describes how long an allow and a deny last.
  </Accordion>
</AccordionGroup>

## Allow only pre-approved tools with dontAsk mode

If you set `dontAsk` mode, Claude Code auto-denies every tool call that would otherwise prompt you. Claude runs only actions matching your `permissions.allow` rules, [read-only Bash commands](/docs/en/permissions#read-only-commands), and calls approved by a [PreToolUse hook](/docs/en/permissions#extend-permissions-with-hooks). Use this mode for CI pipelines or restricted environments where you pre-define exactly what Claude may do; the session never waits for input. The status bar shows `⏵⏵ don't ask on` while this mode is active.

Claude Code denies calls matching your explicit [`ask` rules](/docs/en/permissions#manage-permissions) rather than prompting. It also denies the built-in `AskUserQuestion` tool and connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools), even if your allow rules match them. It denies MCP tools marked [`_meta["anthropic/requiresUserInteraction"]`](/docs/en/mcp#require-approval-for-a-specific-tool) the same way, because their approval card needs an answer this mode never collects; this requires Claude Code v2.1.199 or later.

Cloud sessions on [Claude Code on the web](/docs/en/claude-code-on-the-web) ignore `defaultMode: "dontAsk"`; see [bypassPermissions](#skip-all-checks-with-bypasspermissions-mode) for details.

Set it at startup with the flag:

```bash theme={null}
claude --permission-mode dontAsk
```

## Skip all checks with bypassPermissions mode

`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately, including writes to [protected paths](#protected-paths).

Explicit [ask rules](/docs/en/permissions#manage-permissions) and connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools) still force a prompt in this mode. MCP tools marked with [`_meta["anthropic/requiresUserInteraction"]`](/docs/en/mcp#require-approval-for-a-specific-tool) also still prompt; this requires Claude Code v2.1.199 or later.

Removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, still prompt as a circuit breaker against model error. The circuit breaker also fires when the command contains command substitution with `$(...)` or backticks, or process substitution with `<(...)`, whether the removal sits inside the substitution, as in `echo "$(rm -rf ~)"`, or elsewhere in the same command. The plain form, typed as its own command, has prompted in this mode since the circuit breaker was introduced; before v2.1.208, commands containing those forms didn't prompt.

Two [cross-session messaging](/docs/en/cross-session-messaging) safeguards still apply in this mode, and in plan-mode sessions where bypass permissions are available:

* The [`isolatePeerMachines`](/docs/en/settings#available-settings) approval prompt for messages to your sessions beyond this machine still appears.
* When no [`crossSessionInbound`](/docs/en/cross-session-messaging#control-inbound-messages) value applies, Claude Code holds an inbound message from another of your sessions for your approval, and delivers without asking only when the sending session identifies itself as also bypassing permission prompts. If you leave the mode while messages are held, Claude Code re-applies the inbound rules and delivers any held message they now accept.

In sessions with bypass permissions available, Claude Code also doesn't enforce [plan mode's](#analyze-before-you-edit-with-plan-mode) blocks. Claude is still instructed to plan without editing, but a file edit or shell command it attempts during planning runs without prompting. Explicit [ask rules](/docs/en/permissions#manage-permissions) and the removal circuit breaker above still prompt.

<Warning>
  Only use this mode in isolated environments like containers, VMs, or dev containers without internet access, where Claude Code cannot damage your host system.
</Warning>

You can't enter `bypassPermissions` from a session that was started without it enabled. Enable it at launch with `permissions.defaultMode: "bypassPermissions"` in [settings](/docs/en/settings#permission-settings) or with an enabling flag:

```bash theme={null}
claude --permission-mode bypassPermissions
```

The `--dangerously-skip-permissions` flag is equivalent.

The first time you start an interactive session with this mode enabled, Claude Code shows a warning dialog asking you to accept responsibility for actions taken without permission checks. Claude Code saves your acceptance to user settings, so the dialog appears only once. If you decline, Claude Code exits. In [non-interactive mode](/docs/en/headless) no dialog is shown, and a [background session](/docs/en/agent-view) started with `--bg` is refused until you've accepted the dialog in an interactive session.

On Linux and macOS, Claude Code refuses to start in this mode when running as root or under `sudo`:

```text theme={null}
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

The check is skipped automatically inside a recognized sandbox. To run autonomously in a container, use the [dev container](/docs/en/devcontainer) configuration, which runs Claude Code as a non-root user.

[Claude Code on the web](/docs/en/claude-code-on-the-web) does not honor `defaultMode: "bypassPermissions"` or `"dontAsk"` from your settings files, so a repository's checked-in settings cannot start a cloud session in bypass-permissions mode. The setting is ignored silently and the session starts in the mode shown in the mode dropdown instead. See [Switch permission modes](#switch-permission-modes) for which modes cloud sessions offer.

<Warning>
  `bypassPermissions` offers no protection against prompt injection or unintended actions. For background safety checks with far fewer permission prompts, use [auto mode](#eliminate-prompts-with-auto-mode) instead. Administrators can block this mode by setting `permissions.disableBypassPermissionsMode` to `"disable"` in [managed settings](/docs/en/permissions#managed-settings).
</Warning>

## Protected paths

Writes to a small set of paths are never auto-approved, except in `bypassPermissions` mode and in planning sessions with [bypass permissions](#skip-all-checks-with-bypasspermissions-mode) available. This prevents accidental corruption of repository state and Claude's own configuration.

| Mode                     | Protected-path writes                                                                                                                                                                                                                |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`, `acceptEdits` | Prompted                                                                                                                                                                                                                             |
| `plan`                   | Prompted. In sessions with [bypass permissions](#skip-all-checks-with-bypasspermissions-mode) available, allowed. Otherwise, with [auto mode](#eliminate-prompts-with-auto-mode) available during planning, routed to the classifier |
| `auto`                   | Routed to the classifier                                                                                                                                                                                                             |
| `dontAsk`                | Denied                                                                                                                                                                                                                               |
| `bypassPermissions`      | Allowed                                                                                                                                                                                                                              |

[`permissions.allow`](/docs/en/permissions#manage-permissions) rules in settings files do not pre-approve protected-path writes. The safety check runs before Claude Code evaluates allow rules from settings, so an entry such as `Edit(.claude/**)` in `~/.claude/settings.json` or `.claude/settings.json` does not change the per-mode outcome in the table above. In modes that prompt, the prompt for a `.claude/` write offers **Yes, and allow Claude to edit its own settings for this session**, which approves later `.claude/` writes in that session without prompting again.

Protected directories:

* `.git`
* `.config/git`
* `.vscode`
* `.idea`
* `.husky`
* `.cargo`
* `.devcontainer`
* `.yarn`
* `.mvn`
* `.claude`, except for `.claude/worktrees` where Claude stores its own git worktrees

Protected files:

* `.gitconfig`, `.gitmodules`
* `.bashrc`, `.bash_profile`, `.bash_login`, `.bash_aliases`, `.bash_logout`, `.zshrc`, `.zprofile`, `.zshenv`, `.zlogin`, `.zlogout`, `.profile`, `.envrc`
* `.npmrc`, `.yarnrc`, `.yarnrc.yml`, `.pnp.cjs`, `.pnp.loader.mjs`, `.pnpmfile.cjs`, `bunfig.toml`, `.bunfig.toml`
* `.bazelrc`, `.bazelversion`, `.bazeliskrc`
* `.pre-commit-config.yaml`, `lefthook.yml`, `lefthook.yaml`, `.lefthook.yml`, `.lefthook.yaml`
* `gradle-wrapper.properties`, `maven-wrapper.properties`
* `.devcontainer.json`
* `.ripgreprc`, `pyrightconfig.json`
* `.mcp.json`, `.claude.json`

## See also

* [Permissions](/docs/en/permissions): allow, ask, and deny rules; managed policies
* [Configure auto mode](/docs/en/auto-mode-config): tell the classifier which infrastructure your organization trusts
* [Hooks](/docs/en/hooks): custom permission logic via `PreToolUse` and `PermissionRequest` hooks
* [Security](/docs/en/security): safeguards and best practices
* [Sandboxing](/docs/en/sandboxing): filesystem and network isolation for Bash commands
* [Non-interactive mode](/docs/en/headless): run Claude Code with the `-p` flag
