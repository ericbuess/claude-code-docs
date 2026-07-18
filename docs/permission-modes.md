> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Choose a permission mode

> Control whether Claude asks before editing files or running commands. Cycle modes with Shift+Tab in the CLI or use the mode selector in VS Code, Desktop, and claude.ai.

When Claude wants to edit a file, run a shell command, or make a network request, it pauses and asks you to approve the action. Permission modes control how often that pause happens. The mode you pick shapes the flow of a session: Manual mode has you review each action as it comes, while looser modes let Claude work in longer uninterrupted stretches and report back when done. Pick more oversight for sensitive work, or fewer interruptions when you trust the direction.

## Available modes

Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode.

| Mode                                                                | What runs without asking                                                               | Best for                                |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------- | :-------------------------------------- |
| `default`                                                           | Reads only                                                                             | Getting started, sensitive work         |
| [`acceptEdits`](#auto-approve-file-edits-with-acceptedits-mode)     | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.) | Iterating on code you're reviewing      |
| [`plan`](#analyze-before-you-edit-with-plan-mode)                   | Reads only                                                                             | Exploring a codebase before changing it |
| [`auto`](#eliminate-prompts-with-auto-mode)                         | Everything, with background safety checks                                              | Long tasks, reducing prompt fatigue     |
| [`dontAsk`](#allow-only-pre-approved-tools-with-dontask-mode)       | Only pre-approved tools                                                                | Locked-down CI and scripts              |
| [`bypassPermissions`](#skip-all-checks-with-bypasspermissions-mode) | Everything                                                                             | Isolated containers and VMs only        |

The mode that reviews every action is named **Manual** in the CLI, in `claude --help`, in the VS Code and JetBrains extensions, and in the desktop app. Its config value is `default`, which is what hooks and SDK integrations use. The CLI accepts `manual` as an alias wherever you type the value, for example `claude --permission-mode manual` or `"defaultMode": "manual"`. The Manual label and the `manual` alias require Claude Code v2.1.200 or later. The desktop app's label doesn't depend on your CLI version.

In every mode except `bypassPermissions`, writes to [protected paths](#protected-paths) are never auto-approved, guarding repository state and Claude's own configuration against accidental corruption.

Modes set the baseline. Layer [permission rules](/en/permissions#manage-permissions) on top to pre-approve or block specific tools. Deny rules, explicit ask rules, the [org `ask` setting on connector tools](/en/mcp#organization-controls-on-connector-tools), and the [`requiresUserInteraction`](/en/mcp#require-approval-for-a-specific-tool) marker apply in every mode, including `bypassPermissions`. Allow rules have no effect in that mode because everything else is already approved.

## Switch permission modes

You can switch modes mid-session, at startup, or as a persistent default. The mode is set through these controls, not by asking Claude in chat. Select your interface below to see how to change it.

<Tabs>
  <Tab title="CLI">
    **During a session**: press `Shift+Tab` to cycle `default` → `acceptEdits` → `plan`. The status bar shows the active mode as `⏸ plan mode on`, `⏵⏵ accept edits on`, `⏵⏵ auto mode on`, `⏵⏵ don't ask on`, or `⏵⏵ bypass permissions on`. {/* min-version: 2.1.203 */}Manual mode, `default` in that cycle, shows a gray `⏸ manual mode on` badge. Before v2.1.203, the status bar showed no badge in Manual mode.

    Not every mode is in the default cycle:

    * `auto`: appears when your account meets the [auto mode requirements](#eliminate-prompts-with-auto-mode); cycling to it switches modes without a confirmation prompt
    * `bypassPermissions`: appears after you start with `--permission-mode bypassPermissions`, `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, or `permissions.defaultMode: "bypassPermissions"` in [settings](/en/settings#permission-settings); the `--allow-` variant adds the mode to the cycle without activating it
    * `dontAsk`: never appears in the cycle; set it with `--permission-mode dontAsk`

    Enabled optional modes slot in after `plan`, with `bypassPermissions` first and `auto` last. If you have both enabled, you will cycle through `bypassPermissions` on the way to `auto`.

    **At startup**: pass the mode as a flag.

    ```bash theme={null}
    claude --permission-mode plan
    ```

    **As a default**: set `defaultMode` in a [settings file](/en/settings#settings-files) such as `~/.claude/settings.json`:

    ```json theme={null}
    {
      "permissions": {
        "defaultMode": "acceptEdits"
      }
    }
    ```

    The same `--permission-mode` flag works with `-p` for [non-interactive runs](/en/headless).
  </Tab>

  <Tab title="VS Code">
    **During a session**: click the mode indicator at the bottom of the prompt box.

    **As a default**: set `claudeCode.initialPermissionMode` in VS Code settings, or use the Claude Code extension settings panel.

    The mode indicator shows these labels, mapped to the mode each one applies:

    | UI label           | Mode                |
    | :----------------- | :------------------ |
    | Manual             | `default`           |
    | Edit automatically | `acceptEdits`       |
    | Plan               | `plan`              |
    | Auto               | `auto`              |
    | Bypass permissions | `bypassPermissions` |

    Before v2.1.205, the extension labeled `plan` as Plan mode and `auto` as Auto mode.

    Auto mode appears in the mode indicator when your account meets every requirement listed in the [auto mode section](#eliminate-prompts-with-auto-mode). The `claudeCode.initialPermissionMode` setting does not accept `auto`. To start in auto mode by default, set `defaultMode` in your [user settings](/en/settings#settings-files) instead. Claude Code ignores `defaultMode: "auto"` in project and local settings.

    Bypass permissions requires the **Allow dangerously skip permissions** toggle in the extension settings before it appears in the mode indicator.

    See the [VS Code guide](/en/vs-code) for extension-specific details.
  </Tab>

  <Tab title="JetBrains">
    The JetBrains plugin runs Claude Code in the IDE terminal, so switching modes works the same as in the CLI: press `Shift+Tab` to cycle, or pass `--permission-mode` when launching.
  </Tab>

  <Tab title="Desktop">
    **During a session**: use the mode selector next to the send button. Not every mode appears in the selector:

    * **Auto**: appears when your account meets the [auto mode requirements](#eliminate-prompts-with-auto-mode)
    * **Bypass permissions**: requires the **Allow bypass permissions mode** toggle in Desktop settings on Pro and Max plans; on Team and Enterprise plans, organization policy controls it instead

    For desktop-specific details, see [Choose a permission mode](/en/desktop#choose-a-permission-mode) in the Desktop guide.

    **As a default**: set `defaultMode` in [settings](/en/settings#settings-files). The desktop app reads the same settings files as the CLI and applies the mode to new local sessions.

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

    * **Cloud sessions** on [Claude Code on the web](/en/claude-code-on-the-web): Accept edits, Plan, and Auto. Accept edits corresponds to `default` mode: the cloud environment pre-approves file edits regardless of mode, so the dropdown shows Accept edits instead of Manual. Cloud sessions still honor `defaultMode: "acceptEdits"` from settings. Auto mode appears only when your organization allows it and the selected model supports it. Bypass permissions isn't available.
    * **[Remote Control](/en/remote-control) sessions** on your local machine: Manual, Accept edits, and Plan. You can't select Auto or Bypass permissions from the app. {/* min-version: 2.1.202 */}The dropdown shows the mode the local session is in, including a mode set from the terminal, and updates when the mode changes in the app or in the terminal. The one exception is Bypass permissions: the session never reports that mode to claude.ai, so switching into it from the terminal doesn't change what the dropdown shows. Before v2.1.202, sessions connected with `/remote-control` or `claude --remote-control` didn't report their mode at all, so claude.ai and the mobile app could show a mode the session wasn't in. The mismatch affected only the label: Claude Code generated permission prompts from the session's actual mode, and they still appeared in the app for approval.

    For Remote Control, the host must be signed in with your claude.ai account; API keys are not supported. You can also set the starting mode when launching the host:

    ```bash theme={null}
    claude remote-control --permission-mode acceptEdits
    ```
  </Tab>
</Tabs>

## Auto-approve file edits with acceptEdits mode

`acceptEdits` mode lets Claude create and edit files in your working directory without prompting. The status bar shows `⏵⏵ accept edits on` while this mode is active.

In addition to file edits, `acceptEdits` mode auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`. These commands are also auto-approved when prefixed with safe environment variables such as `LANG=C` or `NO_COLOR=1`, or process wrappers such as `timeout`, `nice`, or `nohup`. Like file edits, auto-approval applies only to paths inside your working directory or `additionalDirectories`. Paths outside that scope, writes to [protected paths](#protected-paths), and all other Bash commands except the [built-in read-only set](/en/permissions#read-only-commands) still prompt.

When the [PowerShell tool](/en/tools-reference#powershell-tool) is enabled, `acceptEdits` mode also auto-approves `Set-Content`, `Add-Content`, `Clear-Content`, and `Remove-Item` on in-scope paths, along with their common aliases. The same scope and protected-path rules apply.

Use `acceptEdits` when you want to review changes in your editor or via `git diff` after the fact rather than approving each edit inline.

Press `Shift+Tab` once from Manual mode to enter it, or start with it directly:

```bash theme={null}
claude --permission-mode acceptEdits
```

## Analyze before you edit with plan mode

Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Permission prompts apply as they do in Manual mode unless [auto mode](/en/auto-mode-config) is available and `useAutoModeDuringPlan` is on, which is the default. With auto mode active, the classifier approves read-only commands such as searches and file reads without prompting. Edits stay blocked either way until you approve the plan.

Shell commands outside the [built-in read-only set](/en/permissions#read-only-commands), including file-modifying ones such as `touch` and `rm`, prompt for approval in plan mode, including when auto mode is active during planning and when the sandbox's [auto-allow mode](/en/sandboxing#sandbox-modes) is enabled.

Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`. You can also start in plan mode from the CLI:

```bash theme={null}
claude --permission-mode plan
```

Press `Shift+Tab` again to leave plan mode without approving a plan.

### Review and approve a plan

When the plan is ready, Claude presents it and asks how to proceed. From that prompt you can choose:

* **Yes, and use auto mode**: approve and start in [auto mode](#eliminate-prompts-with-auto-mode). When auto mode is unavailable, this option reads **Yes, auto-accept edits**. Sessions started with bypass permissions enabled show **Yes, and bypass permissions** instead.
* **Yes, manually approve edits**: approve and review each edit individually.
* **No, refine with Ultraplan on Claude Code on the web**: send the plan to [Ultraplan](/en/ultraplan) for browser-based review.
* **No, keep planning**: stay in plan mode and tell Claude what to change.

Approving a plan exits plan mode and switches the session to the permission mode each approve option describes, so Claude starts editing. To plan again, cycle back to plan mode with `Shift+Tab`, or prefix your next prompt with `/plan`.

Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds. When [`showClearContextOnPlanAccept`](/en/settings#available-settings) is enabled, the list gains a first option that approves the plan and clears the planning context.

Accepting a plan also names the session from the plan content automatically, unless you've already set a name with `--name` or `/rename`.

### Set plan mode as the default

To make plan mode the default for a project, set `defaultMode` in `.claude/settings.json`:

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

Auto mode lets Claude execute without routine permission prompts. A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read. Explicit [ask rules](/en/permissions#manage-permissions) still force a prompt.

Removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, prompt for approval instead of going to the classifier. {/* min-version: 2.1.208 */}This prompt also fires when the command contains command substitution with `$(...)` or backticks, or process substitution with `<(...)`, whether the removal sits inside the substitution, as in `echo "$(rm -rf ~)"`, or elsewhere in the same command. Before v2.1.208, commands containing those forms went to the classifier instead of prompting.

Auto mode also nudges Claude to keep working without stopping for clarifying questions, though Claude still asks when your prompt or a skill explicitly relies on it. For stronger autonomous behavior while keeping permission prompts, set the [Proactive output style](/en/output-styles) instead.

<Warning>
  Auto mode reduces permission prompts but does not guarantee safety. Use it for tasks where you trust the general direction, not as a replacement for review on sensitive operations.
</Warning>

Auto mode is available only when your account meets all of these requirements:

* **Plan**: All plans.
* **Owner**: on Team and Enterprise, an Owner must enable it in [Claude Code admin settings](https://claude.ai/admin-settings/claude-code) before users can turn it on. Administrators can also turn auto mode off by setting `permissions.disableAutoMode` to `"disable"` in [managed settings](/en/permissions#managed-settings). For the desktop app's Code tab, `disableAutoMode` is the organization-level control, and the admin settings toggle doesn't apply.
* **Model**: on the Anthropic API and [Claude Platform on AWS](/en/claude-platform-on-aws), Claude Opus 4.6 or later, Sonnet 4.6 or later, or [Fable 5](/en/model-config#work-with-fable-5). On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in [Claude apps gateway](/en/claude-apps-gateway) sessions, only Claude Sonnet 5, Opus 4.7, Opus 4.8, and Fable 5. Older models, including Sonnet 4.5, Opus 4.5, Haiku, and claude-3 models, are not supported on any provider.
* **Provider**: available by default on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in Claude apps gateway sessions. {/* min-version: 2.1.207 */}In v2.1.158 through v2.1.206, auto mode was off on all of these providers except the Anthropic API and Claude Platform on AWS until you set `CLAUDE_CODE_ENABLE_AUTO_MODE=1`; v2.1.207 removed the requirement.

If Claude Code reports auto mode as unavailable, one of these requirements is unmet; this is not a transient outage. A separate message that names a model and says auto mode "cannot determine the safety" of an action is a transient classifier outage; see the [error reference](/en/errors#auto-mode-cannot-determine-the-safety-of-an-action).

If you set `defaultMode: "auto"` in [settings](/en/settings#available-settings) and the session starts in `default` mode with no error, the setting is likely in `.claude/settings.json` or `.claude/settings.local.json`. Claude Code v2.1.142 and later ignore `auto` from those files so a repository cannot grant itself auto mode. Move it to `~/.claude/settings.json`.

<h3 id="enable-auto-mode-on-bedrock-agent-platform-or-foundry">
  Auto mode on Bedrock, Agent Platform, or Foundry
</h3>

On [Amazon Bedrock](/en/amazon-bedrock), [Google Cloud's Agent Platform](/en/google-vertex-ai), [Microsoft Foundry](/en/microsoft-foundry), and signed-in [Claude apps gateway](/en/claude-apps-gateway) sessions, auto mode appears in the `Shift+Tab` cycle by default. Appearing in the cycle doesn't change the mode a session starts in: sessions still start in your [`defaultMode`](/en/settings#available-settings), which is Manual unless you change it. Only Claude Sonnet 5, Opus 4.7, Opus 4.8, and Fable 5 are supported on these providers.

To make auto mode the default starting mode, set `"permissions": {"defaultMode": "auto"}` in user or managed settings.

{/* min-version: 2.1.210 */}The [`/doctor`](/en/commands#all-commands) checkup proposes this user-settings default on these providers the same way it does on the Anthropic API.

To prevent developers from using auto mode, set `disableAutoMode` to `"disable"` in [managed settings](/en/permissions#managed-settings). This removes `auto` from the `Shift+Tab` cycle and rejects `--permission-mode auto` at startup.

In v2.1.158 through v2.1.206, auto mode was off on these providers until you set `CLAUDE_CODE_ENABLE_AUTO_MODE=1`, and Claude Code ignored `defaultMode: "auto"` on these providers unless the variable was also set. The variable is still accepted for compatibility and has no effect from v2.1.207 onward.

### What the classifier blocks by default

The classifier trusts your working directory and the remotes that were configured for it when the session started. {/* min-version: 2.1.200 */}A remote added or repointed during the session with `git remote add` or `git remote set-url` isn't trusted, and everything else is treated as external until you [configure trusted infrastructure](/en/auto-mode-config). Before v2.1.200, remotes added mid-session were also trusted.

**Blocked by default**:

* Downloading and executing code, like `curl | bash`
* Sending sensitive data to external endpoints
* Production deploys and migrations
* Mass deletion on cloud storage
* Granting IAM or repo permissions
* Modifying shared infrastructure
* Irreversibly destroying files that existed before the session
* Force push
* {/* min-version: 2.1.211 */}Committing or pushing a change that would send secrets or sensitive data outside the repository when it runs, or widen what a deploy exposes. This covers a CI workflow or deploy configuration that hands a secret to a destination that doesn't already receive it, a script or setup step that reads a secret store and sends the data out, and a config change that widens what a deploy publishes, such as a registry, visibility, artifact, or sourcemap setting. The check applies on any branch, applies even when the repository is public, and fires when the change lands, whether or not that landing triggers the pipeline; clearing it requires naming the execution effect, not only the commit or push. Before v2.1.211, this check was scoped to the default branch instead: a push there was blocked when it carried sensitive content, changes concealed or misdescribed relative to what you asked for, content ported in from outside the repository, or routed around a review you asked for, and before v2.1.203 any direct push to the default branch was blocked
* {/* min-version: 2.1.182 */}`git reset --hard`, `git checkout -- .`, `git restore .`, `git clean -fd`, `git stash drop`, or `git stash clear`, which the classifier presumes would discard uncommitted changes
* `git commit --amend` when the commit at HEAD was not created in this session
* {/* min-version: 2.1.198 */}From v2.1.198, `git commit --amend` when the commit at HEAD has already been pushed. A message-only reword is not blocked: `--amend -m` with nothing newly staged, on a commit that Claude created during this session
* `terraform destroy`, `pulumi destroy`, `cdk destroy`, or `terragrunt destroy`, and applying a plan that destroys resources

Claude Code v2.1.195 and later block more categories by default. Several depend on [environment](/en/auto-mode-config#define-trusted-infrastructure) entries, such as sensitive remote targets and protected IaC scopes, that you can narrow to concrete names.

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
* Accessing a location listed as a sensitive data location in your [environment](/en/auto-mode-config#define-trusted-infrastructure), or copying data out of one. {/* min-version: 2.1.198 */}As of v2.1.198 this also blocks sending data from one to an audience the entry excludes
* Routing a package install around your internal package registry to a public registry. {/* min-version: 2.1.198 */}As of v2.1.198, this also applies when you've told Claude an internal registry or mirror exists in the conversation, not only when one is listed in your environment
* Running a command with a flag that disarms a safety guard, like `--insecure`
* Launching an autonomous agent loop that runs without human approval or a sandbox, such as one started with `--dangerously-skip-permissions` or `--no-sandbox`. {/* min-version: 2.1.198 */}As of v2.1.198 this also covers running a third-party agent or eval harness with isolation and per-action approval disabled, such as a runner started with `--yes-always`
* [Claude in Chrome](/en/chrome) browser actions that could send page content, cookies, or credentials off-origin

Claude Code v2.1.198 and later also block these by default:

* Deleting files in `/tmp`, `$TMPDIR`, or another shared scratch or cache directory by wildcard, glob, or age filter rather than by a specific named path
* Including sensitive details in content sent, uploaded, published, or written to other people or shared systems, when your own message didn't authorize those details for that recipient. {/* min-version: 2.1.200 */}PR and issue bodies, commit messages, and comments count as this kind of outbound content when the repository is outside the trust boundary or public, including your organization's own public repositories; internal file paths, code names, live API response data such as emails or account identifiers, and infrastructure identifiers count as sensitive details. The PR, issue, and commit-message scoping requires Claude Code v2.1.200 or later. {/* min-version: 2.1.203 */}Live personal data from an API response in a PR or issue body, such as an email address, an account or organization identifier, or a usage metric, requires you to name those details and the recipient regardless of the repository's visibility or trust boundary. That check requires Claude Code v2.1.203 or later
* Sending keystrokes to Claude Code's own tmux pane to drive its own interface, which the classifier treats as Claude changing its own permissions or oversight

Claude Code v2.1.200 and later also block these by default:

* Commenting out, deleting, or force-passing a test or assertion that guards security behavior, such as auth, access control, input validation, or sandboxing
* Deleting or tearing down a stateful resource Claude didn't create in the session, when no more specific deletion rule applies and you didn't name that resource
* Repointing an API base URL, proxy endpoint, webhook receiver, or registry mirror at a third-party host that doesn't fit the task, including in example files like `.env.example`
* Changing where pushes go with `git remote set-url` or `git remote add`, unless you named the new remote
* Pushing secrets or personal or entrusted data to a repository known to be public, or pushing confidential material there that isn't part of that repository's own work. {/* min-version: 2.1.203 */}A dotfiles repository's own subject matter is the one exception for personal or entrusted data, and content from a private repository reaching any public surface is blocked the same way; both refinements require Claude Code v2.1.203 or later. Before v2.1.203, personal data was grouped with confidential material and blocked only when it wasn't part of that repository's own work. When a repository's visibility isn't established, the classifier doesn't block on that alone; it judges the content against the other rules instead
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
* {/* min-version: 2.1.211 */}Pushing to any branch of the repository you're working in, including the default branch. A non-default branch whose name marks it as a deploy or publication target, such as `production` or `gh-pages`, isn't covered: the classifier judges a push there on its own terms. The push's content is still checked against the other rules, [`permissions.deny` rules](/en/permissions#manage-permissions) can still block pushes to specific branches outright in every mode, and the remote's own branch protection still applies. Before v2.1.211, only pushes to the branch you started on, branches Claude created, and routine pushes to the default branch were allowed by default, and before v2.1.203 any direct push to the default branch was blocked

Claude Code v2.1.195 and later also allow these by default:

* Deleting the exact jobs Claude created earlier in the same session
* Reading, reviewing, or writing security-related code, configs, and threat models as part of your task
* Messages between agents working together in the same multi-agent session
* Sending data to the trusted domains, buckets, and services you list in [`environment`](/en/auto-mode-config#define-trusted-infrastructure). This covers data flow only, not destructive or credential operations on the same infrastructure
* [Claude in Chrome](/en/chrome) navigation to a trusted internal domain, localhost, or a URL you named

Sandbox network access requests are routed through the classifier rather than allowed by default. {/* min-version: 2.1.198 */}As of v2.1.198, the classifier reuses its verdict for a network host and port instead of re-running on every connection:

* An allow is reused until new content enters the conversation, at which point that host is checked again
* In the interactive CLI, a deny is dropped when the turn ends
* In [non-interactive mode](/en/headless) and Agent SDK sessions there is no turn boundary, so a deny is reused for the rest of the run
* Changing your permission mode or rules drops all cached verdicts

Run `claude auto-mode defaults` to print the full rule lists as JSON. If routine actions get blocked, an administrator can add trusted repos, buckets, and services via the `autoMode.environment` setting: see [Configure auto mode](/en/auto-mode-config).

{/* min-version: 2.1.211 */}Pushing to any branch of the repository you're working in and creating a pull request that matches your request run without a prompt, with the two exceptions the lists above cover: the classifier judges a push to a deploy-named branch such as `production` or `gh-pages` on its own terms, and still blocks a push whose content carries risk. To require a human checkpoint before these actions while staying in auto mode, add `permissions.ask` rules: see [Common boundaries](/en/auto-mode-config#common-boundaries).

### Boundaries you state in conversation

The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude "don't push" or "wait until I review before deploying", the classifier blocks matching actions even when the default rules would allow them. A boundary stays in force until you lift it in a later message. Claude's own judgment that a condition was met does not lift it.

Boundaries are not stored as rules. The classifier re-reads them from the transcript on each check, so a boundary can be lost if [context compaction](/en/costs#reduce-token-usage) removes the message that stated it. For a hard guarantee, add a [deny rule](/en/permissions#permission-rule-syntax) instead.

### When auto mode falls back

Each denied action shows a notification and appears in `/permissions` under the Recently denied tab, where you can press `r` to retry it with a manual approval.

If the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode. These thresholds are not configurable. Any allowed action resets the consecutive counter, while the total counter persists for the session and resets only when its own limit triggers a fallback.

In [non-interactive mode](/en/headless) with the `-p` flag, repeated blocks abort the session since there is no user to prompt.

Repeated blocks usually mean the classifier is missing context about your infrastructure. Use `/feedback` to report false positives, or have an administrator [configure trusted infrastructure](/en/auto-mode-config).

<AccordionGroup>
  <Accordion title="How the classifier evaluates actions">
    Each action goes through a fixed decision order. The first matching step wins:

    1. Actions matching your [allow, ask, or deny rules](/en/permissions#manage-permissions) resolve immediately. Writes to [protected paths](#protected-paths) route to the classifier even when an allow rule matches. Connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools) and MCP tools marked [`requiresUserInteraction`](/en/mcp#require-approval-for-a-specific-tool) prompt you directly even when an allow rule matches. Content-scoped ask rules fall back to a permission prompt
    2. Read-only actions and file edits in your working directory are auto-approved, except writes to [protected paths](#protected-paths)
    3. Everything else goes to the classifier. A connector tool [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools) skips the classifier and prompts you directly, so an org-required approval is never auto-approved. {/* min-version: 2.1.199 */}As of v2.1.199, an MCP tool marked with [`_meta["anthropic/requiresUserInteraction"]`](/en/mcp#require-approval-for-a-specific-tool) also skips the classifier and prompts you directly, so a consent step is never auto-approved on the tool author's behalf
    4. If the classifier blocks, Claude receives the reason and tries an alternative

    On entering auto mode, broad allow rules that grant arbitrary code execution are dropped:

    * Blanket `Bash(*)` or `PowerShell(*)`
    * Wildcarded interpreters like `Bash(python*)`
    * Package-manager run commands
    * `Agent` allow rules

    Narrow rules like `Bash(npm test)` carry over. Dropped rules are restored when you leave auto mode.

    The classifier sees user messages, tool calls, and your CLAUDE.md content. Tool results are stripped, so hostile content in a file or web page cannot manipulate it directly. A separate server-side probe scans incoming tool results and flags suspicious content before Claude reads it. For more on how these layers work together, see the [auto mode announcement](https://claude.com/blog/auto-mode) and the [engineering deep dive](https://www.anthropic.com/engineering/claude-code-auto-mode).
  </Accordion>

  <Accordion title="How auto mode handles subagents">
    The classifier checks [subagent](/en/sub-agents) work at three points:

    1. Before a subagent starts, the delegated task description is evaluated, so a dangerous-looking task is blocked at spawn time.
    2. While the subagent runs, each of its actions goes through the classifier with the same rules as the parent session, and any `permissionMode` in the subagent's frontmatter is ignored.
    3. When the subagent finishes, the classifier reviews its full action history; if that return check flags a concern, a security warning is prepended to the subagent's results.

    Step 1 requires Claude Code v2.1.178 or later. Earlier versions applied the classifier at steps 2 and 3, but did not evaluate the task description before the subagent started.
  </Accordion>

  <Accordion title="Cost and latency">
    {/* min-version: 2.1.210 */}The classifier runs on Claude Sonnet 5 by default rather than on your `/model` selection. A classifier model that Anthropic configures server-side takes precedence over that default. When your session's model is Claude Sonnet 4.6, or when [`availableModels`](/en/model-config#restrict-model-selection) excludes Sonnet 5, the classifier runs on the session's model instead, or on an Opus model when the session runs on [Fable 5](/en/model-config#work-with-fable-5); on providers other than the Anthropic API, that Opus fallback is the provider's default Opus model.

    The session's first auto-mode request validates the Sonnet 5 default: if the request succeeds, Sonnet 5 stays the session's classifier model, and if it fails because the model isn't available, the session uses the fallback instead. After that validation settles, the classifier's model doesn't change for the session.

    Classifier calls count toward your token usage. Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations.

    {/* min-version: 2.1.198 */}The classifier reuses a sandbox network verdict for a host and port, so repeated connections to the same host don't each add a check. [What the classifier blocks by default](#what-the-classifier-blocks-by-default) describes how long an allow and a deny last.
  </Accordion>
</AccordionGroup>

## Allow only pre-approved tools with dontAsk mode

If you set `dontAsk` mode, Claude Code auto-denies every tool call that would otherwise prompt you. Claude runs only actions matching your `permissions.allow` rules, [read-only Bash commands](/en/permissions#read-only-commands), and calls approved by a [PreToolUse hook](/en/permissions#extend-permissions-with-hooks). Use this mode for CI pipelines or restricted environments where you pre-define exactly what Claude may do; the session never waits for input. The status bar shows `⏵⏵ don't ask on` while this mode is active.

Claude Code denies calls matching your explicit [`ask` rules](/en/permissions#manage-permissions) rather than prompting. It also denies the built-in `AskUserQuestion` tool and connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools), even if your allow rules match them. {/* min-version: 2.1.199 */}It denies MCP tools marked [`_meta["anthropic/requiresUserInteraction"]`](/en/mcp#require-approval-for-a-specific-tool) the same way, because their approval card needs an answer this mode never collects; this requires Claude Code v2.1.199 or later.

Cloud sessions on [Claude Code on the web](/en/claude-code-on-the-web) ignore `defaultMode: "dontAsk"`; see [bypassPermissions](#skip-all-checks-with-bypasspermissions-mode) for details.

Set it at startup with the flag:

```bash theme={null}
claude --permission-mode dontAsk
```

## Skip all checks with bypassPermissions mode

`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately, including writes to [protected paths](#protected-paths). Before v2.1.126, protected-path writes still prompted in this mode.

Explicit [ask rules](/en/permissions#manage-permissions) and connector tools [your organization set to `ask`](/en/mcp#organization-controls-on-connector-tools) still force a prompt in this mode. {/* min-version: 2.1.199 */}MCP tools marked with [`_meta["anthropic/requiresUserInteraction"]`](/en/mcp#require-approval-for-a-specific-tool) also still prompt; this requires Claude Code v2.1.199 or later.

Removals targeting the filesystem root or home directory, such as `rm -rf /` and `rm -rf ~`, still prompt as a circuit breaker against model error. {/* min-version: 2.1.208 */}The circuit breaker also fires when the command contains command substitution with `$(...)` or backticks, or process substitution with `<(...)`, whether the removal sits inside the substitution, as in `echo "$(rm -rf ~)"`, or elsewhere in the same command. The plain form, typed as its own command, has prompted in this mode since the circuit breaker was introduced; before v2.1.208, commands containing those forms didn't prompt.

<Warning>
  Only use this mode in isolated environments like containers, VMs, or dev containers without internet access, where Claude Code cannot damage your host system.
</Warning>

You can't enter `bypassPermissions` from a session that was started without it enabled. Enable it at launch with `permissions.defaultMode: "bypassPermissions"` in [settings](/en/settings#permission-settings) or with an enabling flag:

```bash theme={null}
claude --permission-mode bypassPermissions
```

The `--dangerously-skip-permissions` flag is equivalent.

The first time you start an interactive session with this mode enabled, Claude Code shows a warning dialog asking you to accept responsibility for actions taken without permission checks. Claude Code saves your acceptance to user settings, so the dialog appears only once. If you decline, Claude Code exits. In [non-interactive mode](/en/headless) no dialog is shown, and a [background session](/en/agent-view) started with `--bg` is refused until you've accepted the dialog in an interactive session.

On Linux and macOS, Claude Code refuses to start in this mode when running as root or under `sudo`:

```text theme={null}
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

The check is skipped automatically inside a recognized sandbox. To run autonomously in a container, use the [dev container](/en/devcontainer) configuration, which runs Claude Code as a non-root user.

[Claude Code on the web](/en/claude-code-on-the-web) does not honor `defaultMode: "bypassPermissions"` or `"dontAsk"` from your settings files, so a repository's checked-in settings cannot start a cloud session in bypass-permissions mode. The setting is ignored silently and the session starts in the mode shown in the mode dropdown instead. See [Switch permission modes](#switch-permission-modes) for which modes cloud sessions offer.

<Warning>
  `bypassPermissions` offers no protection against prompt injection or unintended actions. For background safety checks with far fewer permission prompts, use [auto mode](#eliminate-prompts-with-auto-mode) instead. Administrators can block this mode by setting `permissions.disableBypassPermissionsMode` to `"disable"` in [managed settings](/en/permissions#managed-settings).
</Warning>

## Protected paths

Writes to a small set of paths are never auto-approved, in every mode except `bypassPermissions`. This prevents accidental corruption of repository state and Claude's own configuration.

| Mode                             | Protected-path writes    |
| :------------------------------- | :----------------------- |
| `default`, `acceptEdits`, `plan` | Prompted                 |
| `auto`                           | Routed to the classifier |
| `dontAsk`                        | Denied                   |
| `bypassPermissions`              | Allowed                  |

[`permissions.allow`](/en/permissions#manage-permissions) rules in settings files do not pre-approve protected-path writes. The safety check runs before Claude Code evaluates allow rules from settings, so an entry such as `Edit(.claude/**)` in `~/.claude/settings.json` or `.claude/settings.json` does not change the per-mode outcome in the table above. In modes that prompt, the prompt for a `.claude/` write offers **Yes, and allow Claude to edit its own settings for this session**, which approves later `.claude/` writes in that session without prompting again.

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

* [Permissions](/en/permissions): allow, ask, and deny rules; managed policies
* [Configure auto mode](/en/auto-mode-config): tell the classifier which infrastructure your organization trusts
* [Hooks](/en/hooks): custom permission logic via `PreToolUse` and `PermissionRequest` hooks
* [Ultraplan](/en/ultraplan): run plan mode in a Claude Code on the web session with browser-based review
* [Security](/en/security): safeguards and best practices
* [Sandboxing](/en/sandboxing): filesystem and network isolation for Bash commands
* [Non-interactive mode](/en/headless): run Claude Code with the `-p` flag
