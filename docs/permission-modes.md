> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Choose a permission mode

> Control whether Claude asks before acting. Switch permission modes with Shift+Tab in the CLI, the mode indicator in VS Code, or the mode selector in Desktop.

A permission mode sets which actions Claude can take in a session without asking you first. In Manual mode, Claude Code stops and asks you before most actions that edit files, run shell commands, or reach the network. In [auto mode](#eliminate-prompts-with-auto-mode), a second model, the classifier, reviews actions instead of you; [how the classifier evaluates actions](#how-the-classifier-evaluates-actions) lists which actions it reviews and which skip it.

On Pro, Max, and Team plans, the built-in starting permission mode is auto mode. [Which mode a session starts in](#which-mode-a-session-starts-in) covers the surfaces and settings that change the starting permission mode. You can also change a running session's permission mode at any time.

## Available modes

Each mode makes a different tradeoff between convenience and oversight. The table below shows what Claude can do without a permission prompt in each mode. Manual mode appears under its config value, `default`.

| Mode                                                                | What runs without asking                                                                                  | Best for                                        |
| :------------------------------------------------------------------ | :-------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| `default`                                                           | Reads only                                                                                                | Reviewing every action yourself, sensitive work |
| [`acceptEdits`](#auto-approve-file-edits-with-acceptedits-mode)     | Reads, file edits, and common filesystem commands (`mkdir`, `touch`, `mv`, `cp`, etc.)                    | Iterating on code you're reviewing              |
| [`plan`](#analyze-before-you-edit-with-plan-mode)                   | Reads, plus classifier-approved commands when [auto mode](#eliminate-prompts-with-auto-mode) is available | Exploring a codebase before changing it         |
| [`auto`](#eliminate-prompts-with-auto-mode)                         | Everything, with background safety checks                                                                 | Long tasks, reducing prompt fatigue             |
| [`dontAsk`](#allow-only-pre-approved-tools-with-dontask-mode)       | Reads and pre-approved tools; anything that would prompt is denied                                        | Locked-down CI and scripts                      |
| [`bypassPermissions`](#skip-all-checks-with-bypasspermissions-mode) | Everything                                                                                                | Isolated containers and VMs only                |

The mode that reviews every action is named **Manual** in the CLI, in `claude --help`, in the VS Code and JetBrains extensions, and in the desktop app. Its config value is `default`, which is what hooks and SDK integrations use. The CLI accepts `manual` as an alias wherever you type the value, for example `claude --permission-mode manual` or `"defaultMode": "manual"`. The Manual label and the `manual` alias require Claude Code v2.1.200 or later. The desktop app's label doesn't depend on your CLI version.

Writes to [protected paths](#protected-paths) are never auto-approved except in `bypassPermissions` mode and in plan-mode sessions where bypass permissions are available, meaning interactive terminal sessions started in a way that [puts `bypassPermissions` in the mode cycle](#switch-permission-modes).

Modes set the baseline. Layer [permission rules](/docs/en/permissions#manage-permissions) on top to pre-approve or block specific tools. Deny rules block in every mode, including `bypassPermissions`. Deny and ask rules don't apply to [`EndConversation`](/docs/en/tools-reference#endconversation-tool-behavior) as long as Claude still has at least one other tool it can call. Allow rules have no effect in `bypassPermissions`.

<h3 id="actions-no-mode-auto-approves">
  Actions no mode auto-approves
</h3>

Claude Code doesn't auto-approve the following in any mode, including `bypassPermissions`. Each bullet links to the section that says what happens instead in each mode:

* Tools matched by an explicit [ask rule](/docs/en/permissions#manage-permissions)
* Connector tools your organization [set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools), in sessions where that setting reaches Claude Code
* Tools that require user interaction: the built-in `AskUserQuestion` tool and MCP tools marked [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool)
* `rm` and `rmdir` removals targeting a [critical path](#critical-paths), which no allow rule or `PreToolUse` hook `"allow"` approves
* The [cross-session messaging safeguards](#skip-all-checks-with-bypasspermissions-mode)
* Reads outside the working directories while [`permissions.blockReadsOutsideWorkingDirectories`](/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories) is on: recognized file-reading Bash commands prompt even in auto mode and `bypassPermissions` mode, and so does any [unsandboxed retry](/docs/en/sandboxing#the-unsandboxed-retry-escape-hatch) that needs approval to run outside the sandbox. Requires Claude Code v2.1.257 or later.

  A command the shell parser can't trace, such as one that changes directory more than once or runs a subshell, prompts the same way even when it names no outside path. This prompt doesn't apply when the command runs in the [sandbox](/docs/en/sandboxing) and the sandbox enforces the block.

## Common setups

Permission modes decide whether Claude asks before an action, and the [Bash sandbox](/docs/en/sandboxing) and outer [isolation boundaries](/docs/en/sandbox-environments) decide what an action can reach once it runs. Each row below pairs a goal with the flags or settings that get you there and the isolation it needs, as a starting point. [Available modes](#available-modes) lists what runs without a prompt in each mode.

| You want to                                              | Start with                                                                                                                                                          | Isolation needed                                                                                                                                                                             | Notes                                                                                                                                                                                                                               |
| :------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Review every action yourself                             | Manual mode: `claude --permission-mode default`                                                                                                                     | None                                                                                                                                                                                         | Sensitive work, unfamiliar code                                                                                                                                                                                                     |
| Iterate locally with fewer prompts, without a classifier | Manual mode plus the Bash sandbox in [auto-allow mode](/docs/en/sandboxing#sandbox-modes): `claude --permission-mode default`, then run `/sandbox` and select auto-allow | The built-in Bash sandbox, on macOS, Linux, and WSL2                                                                                                                                         | Deny rules still apply, and ask rules that name a command, such as `Bash(git push *)`, still prompt. To turn the sandbox on from a settings file instead, set [`sandbox.enabled`](/docs/en/settings-reference#sandbox-enabled) to `true` |
| Explore before changing anything                         | `claude --permission-mode plan`                                                                                                                                     | None                                                                                                                                                                                         | Claude Code blocks edits until you [approve a plan](#review-and-approve-a-plan)                                                                                                                                                     |
| Work hands-off in auto mode                              | `claude --permission-mode auto`, the [built-in starting permission mode](#which-mode-a-session-starts-in) on Pro, Max, and Team                                     | None; a sandbox or container adds defense in depth                                                                                                                                           | Requires a [supported model](#eliminate-prompts-with-auto-mode), and your organization can [turn auto mode off](#eliminate-prompts-with-auto-mode)                                                                                  |
| Run in CI with an exact allowlist                        | `claude -p "run the test suite" --permission-mode dontAsk --allowedTools "Bash(npm test)" "Read"`                                                                   | None beyond what your CI runner provides                                                                                                                                                     | [Cloud sessions](/docs/en/claude-code-on-the-web) ignore `dontAsk` from settings files                                                                                                                                                   |
| Run fully unattended inside a container                  | `claude -p "<prompt>" --dangerously-skip-permissions`                                                                                                               | Required: a container, VM, or the [sandbox runtime](/docs/en/sandbox-environments#sandbox-runtime); on Linux and macOS, run it as a [non-root user](#skip-all-checks-with-bypasspermissions-mode) | Cloud sessions ignore this mode from settings files. In this `-p` run, the [few calls that would still prompt](#skip-all-checks-with-bypasspermissions-mode) are denied instead                                                     |

The Bash sandbox and auto mode work independently and combine, with the exceptions listed under [Sandbox modes](/docs/en/sandboxing#sandbox-modes). For the full interaction, see [How sandboxing relates to permissions and permission modes](/docs/en/sandboxing#how-sandboxing-relates-to-permissions-and-permission-modes) and [How isolation relates to permission modes](/docs/en/sandbox-environments#how-isolation-relates-to-permission-modes).

<h2 id="which-mode-a-session-starts-in">
  Which mode a session starts in
</h2>

When you start a new session in a terminal, Claude Code takes the permission mode from the first of these that applies:

1. The `--permission-mode` flag, or `--dangerously-skip-permissions`

2. `permissions.defaultMode` in a [settings file](/docs/en/settings#where-settings-live)

   If you set `"auto"` in `.claude/settings.json` or `.claude/settings.local.json`, the value doesn't take effect, and Claude Code then uses the built-in default rather than a `defaultMode` from `~/.claude/settings.json`. If you set `"bypassPermissions"` in those two files, it doesn't take effect either, and the session starts in Manual mode. The other values apply from any settings file.

3. The built-in default

Conversations the VS Code extension starts follow the extension's own list in [Switch permission modes](#switch-permission-modes). For the permission mode Claude Code starts a resumed session in, see [permission mode on resume](/docs/en/sessions#permission-mode-on-resume).

The built-in `auto` default requires Claude Code v2.1.228 or later on macOS, Linux, and WSL, and v2.1.233 or later on native Windows. On earlier versions, the built-in default is Manual.

The built-in default depends on how you run Claude Code, on your plan, and on whether Claude Code could fetch its feature flags. The first row that matches your session applies. The table covers sessions you start in a terminal or through the VS Code extension; for the desktop app and claude.ai, see the Desktop and Web tabs in [Switch permission modes](#switch-permission-modes).

| How you run Claude Code                                                                                                                                                                                                         | Built-in starting permission mode |
| :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-------------------------------- |
| Any settings file sets `disableAutoMode` to `"disable"`                                                                                                                                                                         | `default`                         |
| [Feature-flag fetching](/docs/en/env-vars#features-that-need-feature-flag-fetching) is off                                                                                                                                           | `default`                         |
| Your [first session after you install Claude Code or upgrade](/docs/en/env-vars#first-session-after-an-install-or-upgrade) to a version that adds this default, unless, after a fresh install, Claude Code fetches the flags in time | `default`                         |
| `claude -p` or the [Agent SDK](/docs/en/agent-sdk/permissions)                                                                                                                                                                       | `default`                         |
| Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, [Claude Platform on AWS](/docs/en/claude-platform-on-aws), or a signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) session                                   | `default`                         |
| A Pro, Max, or Team plan, in a terminal or through the [VS Code extension](/docs/en/vs-code)                                                                                                                                         | `auto`                            |
| An Enterprise plan or a Claude Console API key                                                                                                                                                                                  | `default`                         |

When feature-flag fetching is off, or in a [first session after an install or upgrade](/docs/en/env-vars#first-session-after-an-install-or-upgrade) where the flags haven't arrived yet, the VS Code extension ignores every settings file when choosing the starting permission mode.

When the flag, a settings file, or the built-in default selects `auto` but auto mode isn't available to the session, Claude Code starts the session in Manual instead. Auto mode is unavailable when the session doesn't meet the [availability requirements](#eliminate-prompts-with-auto-mode), such as a settings file turning it off or a model that doesn't support it, or when Anthropic has temporarily turned it off server-side.

The first time the built-in default starts one of your sessions in auto mode, Claude Code shows a notice that links to this page:

* In a terminal, once, at the top of the session
* In the VS Code extension, as a card on the new-conversation screen that stays until you dismiss it

On Pro, Max, and Team plans, if your `~/.claude/settings.json` sets a `defaultMode` other than `auto` and no other settings file sets one, your sessions keep starting in that mode. Claude Code asks once, in the terminal or in the VS Code extension, whether to change the setting to auto mode. If you decline, your setting stays as it is.

<h3 id="start-in-a-different-mode">
  Start in a different permission mode
</h3>

You can set the starting permission mode for one session, or as a default for every session on a machine, in a project, or in an organization. When more than one settings file sets `permissions.defaultMode`, [settings precedence](/docs/en/settings#settings-precedence) decides, so a project or managed value outranks `~/.claude/settings.json`. To change the permission mode of a session that's already running, see [Switch permission modes](#switch-permission-modes).

| To set the starting permission mode for          | Do this                                                                                                                                                                                                                                                                                                                                                        |
| :----------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One session you're about to start                | Pass the permission mode as a flag, for example `claude --permission-mode default`                                                                                                                                                                                                                                                                             |
| Every terminal session you start on this machine | Set `permissions.defaultMode` in `~/.claude/settings.json`. For what the VS Code extension reads, see [Switch permission modes](#switch-permission-modes)                                                                                                                                                                                                      |
| Every terminal session you start in one project  | Set `permissions.defaultMode` in the project's `.claude/settings.json`. Sessions you start in a terminal honor every value except `auto` and `bypassPermissions`; sessions the VS Code extension starts don't read project settings for the starting permission mode                                                                                           |
| Every terminal session in your organization      | Set `permissions.defaultMode` in [managed settings](/docs/en/managed-settings). Terminal sessions start in that mode and people can still switch to auto mode; for what the VS Code extension reads, see [Switch permission modes](#switch-permission-modes). To remove auto mode so nobody can select it, set `permissions.disableAutoMode` to `"disable"` instead |

This example makes every terminal session on your machine start in Manual mode, whose config value is `default`. Save it in `~/.claude/settings.json`:

```json theme={null}
{
  "permissions": {
    "defaultMode": "default"
  }
}
```

The next session you start shows `⏸ manual mode on` in the status bar.

## Switch permission modes

Each interface has its own control for switching permission modes during a session and its own way of choosing the permission mode new sessions start in. Select your interface to see its controls.

<Tabs>
  <Tab title="CLI">
    **During a session**: press `Shift+Tab` to cycle permission modes. From `auto`, the first press switches to `default`, and the cycle then runs `default` → `acceptEdits` → `plan` → back to `default`. Optional modes, described below, slot in after `plan`. The status bar shows the active mode as a gray `⏸ manual mode on` for `default`, or as `⏵⏵ accept edits on`, `⏸ plan mode on`, `⏵⏵ auto mode on`, `⏵⏵ don't ask on`, or `⏵⏵ bypass permissions on`.

    Not every mode is in the default cycle:

    * `auto`: appears when [auto mode is available](#eliminate-prompts-with-auto-mode); cycling to it switches permission modes without a confirmation prompt
    * `bypassPermissions`: appears after you start with `--permission-mode bypassPermissions`, `--dangerously-skip-permissions`, `--allow-dangerously-skip-permissions`, or `permissions.defaultMode: "bypassPermissions"` in [user, `--settings`, or managed settings](/docs/en/settings-reference#permissions-defaultmode). The `--allow-` variant adds the permission mode to the cycle without activating it
    * `dontAsk`: never appears in the cycle; set it with `--permission-mode dontAsk`

    Enabled optional modes slot in after `plan`, with `bypassPermissions` first and `auto` last. If you have both enabled, you will cycle through `bypassPermissions` on the way to `auto`.

    **From a Bash permission prompt**: in the Manual and `acceptEdits` permission modes, when [auto mode](#eliminate-prompts-with-auto-mode) is available, Claude Code adds **Yes, and switch to auto mode** to a Bash command's permission prompt. Select it to approve the command and switch the session to auto mode. [PowerShell tool](/docs/en/tools-reference#powershell-tool) prompts don't offer the option. Requires Claude Code v2.1.247 or later.

    Claude Code doesn't add the option to prompts forced by one of your [`ask` rules](/docs/en/permissions#manage-permissions) or by a [hook](/docs/en/hooks#pretooluse-decision-control), because auto mode still shows you those prompts, so switching wouldn't remove them.

    **At startup**: pass the permission mode as a flag.

    ```bash theme={null}
    claude --permission-mode plan
    ```

    **As a default**: set `permissions.defaultMode` at the scope you want, as described in [Start in a different permission mode](#start-in-a-different-mode).

    The same `--permission-mode` flag works with `-p` for [non-interactive runs](/docs/en/headless).
  </Tab>

  <Tab title="VS Code">
    **During a session**: click the mode indicator at the bottom of the prompt box. It uses these labels for the modes on this page:

    | UI label           | Mode                |
    | :----------------- | :------------------ |
    | Manual             | `default`           |
    | Edit automatically | `acceptEdits`       |
    | Plan               | `plan`              |
    | Auto               | `auto`              |
    | Bypass permissions | `bypassPermissions` |

    **As a default**: to pin the permission mode conversations start in, set `claudeCode.initialPermissionMode` in your VS Code user settings to `default`, `manual`, `acceptEdits`, `plan`, or `bypassPermissions`. The setting doesn't accept `auto`; to start in Auto, leave it unset and pick **Auto** from the mode indicator once, as item 2 below describes. The extension starts each new conversation in the first of these that applies:

    1. `claudeCode.initialPermissionMode`
    2. The mode you last picked from the mode indicator, if it was Manual, Edit automatically, or Auto. Picking Plan or Bypass permissions applies to that conversation only
    3. `permissions.defaultMode` from [managed settings](/docs/en/managed-settings) or `~/.claude/settings.json`, on Pro, Max, and Team plans with [feature-flag fetching](#which-mode-a-session-starts-in) available
    4. The [built-in default](#which-mode-a-session-starts-in) for your plan, provider, and organization settings

    The extension never reads a project's `.claude/settings.json` or `.claude/settings.local.json` for the starting permission mode, and in conversations that don't meet item 3's conditions it reads no settings file at all. When `claudeCode.claudeProcessWrapper` is set, items 3 and 4 don't apply either: those conversations start in Manual unless item 1 or item 2 sets a permission mode.

    Auto appears in the mode indicator when [auto mode is available](#eliminate-prompts-with-auto-mode).

    Bypass permissions requires the **Allow dangerously skip permissions** toggle in the extension settings. Without it, the permission mode doesn't appear in the indicator, and a `bypassPermissions` value from item 1 or item 3 starts the conversation in Manual instead. Auto from any item likewise starts the conversation in Manual when auto mode isn't available.

    See the [VS Code guide](/docs/en/vs-code) for extension-specific details.
  </Tab>

  <Tab title="JetBrains">
    The JetBrains plugin runs Claude Code in the IDE terminal, so switching permission modes works the same as in the CLI: press `Shift+Tab` to cycle, or pass `--permission-mode` when launching.
  </Tab>

  <Tab title="Desktop">
    **During a session**: in the Code tab, use the mode selector next to the send button. Not every mode appears in the selector:

    * **Auto**: appears when [auto mode is available](#eliminate-prompts-with-auto-mode)
    * **Bypass permissions**: requires the **Allow bypass permissions mode** toggle in Desktop settings on Pro and Max plans; on Team and Enterprise plans, organization policy controls it instead

    The Cowork tab doesn't use these modes. Cowork has its own permission modes, enabled separately, and the Cowork tab shows no mode selector at all until a mode beyond its default is enabled for your account. See the [Cowork docs](https://claude.com/docs/cowork/overview).

    For desktop-specific details, see [Choose a permission mode](/docs/en/desktop#choose-a-permission-mode) in the Desktop guide.

    **As a default**: set `defaultMode` in [settings](/docs/en/settings#where-settings-live). The desktop app reads the same settings files as the CLI and applies the permission mode to new local sessions.

    A mode you pick in the mode selector is remembered per folder and takes precedence over `defaultMode` for that folder. Plan is the exception: picking it applies to the current session only.

    For where `defaultMode` goes in a settings file, see the example under [Start in a different permission mode](#start-in-a-different-mode).
  </Tab>

  <Tab title="Web and mobile">
    Use the mode dropdown next to the prompt box on [claude.ai/code](https://claude.ai/code) or in the mobile app. Permission prompts appear in claude.ai for approval. Which modes appear depends on where the session runs:

    * **[Cloud sessions](/docs/en/claude-code-on-the-web)**: Accept edits, Plan, and Auto. Accept edits corresponds to `default` mode: cloud sessions pre-approve file edits regardless of mode, so the dropdown shows Accept edits instead of Manual. Cloud sessions still honor `defaultMode: "acceptEdits"` from settings. Auto mode appears only when your organization allows it and the selected model supports it. Bypass permissions isn't available.
    * **[Remote Control](/docs/en/remote-control) sessions** on your local machine: Manual, Accept edits, and Plan. You can't select Auto or Bypass permissions from the app.
      * Except for Bypass permissions, the dropdown shows the permission mode the local session is in, including one set from the terminal. It updates when the permission mode changes in the app or in the terminal. The session never reports Bypass permissions to claude.ai, so switching into it from the terminal doesn't change what the dropdown shows.
      * Sessions hosted by the [desktop app](/docs/en/desktop) or the [VS Code extension](/docs/en/vs-code) report permission mode changes to claude.ai as they happen, the same as sessions hosted in a terminal.
      * Before v2.1.202, sessions connected with `/remote-control` or `claude --remote-control` didn't report their permission mode at all, so claude.ai and the mobile app could show a permission mode the session wasn't in. The mismatch affected only the label. Claude Code generated permission prompts from the session's actual permission mode, and they still appeared in the app for approval.

    For Remote Control, the local machine running the session must be signed in with your claude.ai account; API keys aren't supported. You can also set the starting permission mode when launching that local session:

    ```bash theme={null}
    claude remote-control --permission-mode acceptEdits
    ```
  </Tab>
</Tabs>

## Auto-approve file edits with acceptEdits mode

`acceptEdits` mode lets Claude create and edit files in your working directory without prompting. The status bar shows `⏵⏵ accept edits on` while this mode is active.

In addition to file edits, `acceptEdits` mode auto-approves common filesystem Bash commands: `mkdir`, `touch`, `rm`, `rmdir`, `mv`, `cp`, and `sed`. These commands are also auto-approved when prefixed with safe environment variables such as `LANG=C` or `NO_COLOR=1`, or process wrappers such as `timeout`, `nice`, or `nohup`. Like file edits, auto-approval applies only to paths inside your working directory or `additionalDirectories`. Paths outside that scope, writes to [protected paths](#protected-paths), `rm` and `rmdir` removals targeting a [critical path](#critical-paths), and all other Bash commands except the [built-in read-only set](/docs/en/permissions#read-only-commands) still prompt.

When the [PowerShell tool](/docs/en/tools-reference#powershell-tool) is enabled, `acceptEdits` mode also auto-approves `Set-Content`, `Add-Content`, `Clear-Content`, and `Remove-Item` on in-scope paths, along with their common aliases. The same scope and protected-path rules apply, and `Remove-Item` gets [its own check](#remove-item-in-powershell). A positional argument that contains a quote character, such as the apostrophe in `Set-Content .\notes.txt "It's done"`, still prompts even on in-scope paths, because Claude Code can't statically validate an argument whose quoted and unquoted readings differ. Pass the content through a named parameter such as `-Value` to avoid the prompt.

Use `acceptEdits` when you want to review changes in your editor or via `git diff` after the fact rather than approving each edit inline.

Press `Shift+Tab` once from Manual mode to enter it, or start with it directly:

```bash theme={null}
claude --permission-mode acceptEdits
```

## Analyze before you edit with plan mode

Plan mode tells Claude to research and propose changes without making them. Claude reads files, runs shell commands to explore, and writes a plan, but does not edit your source. Except in interactive terminal sessions with [bypass permissions available](#skip-all-checks-with-bypasspermissions-mode), edits stay blocked until you approve the plan.

When [auto mode](/docs/en/auto-mode-config) is available and the `useAutoModeDuringPlan` setting is on, which it is by default, the classifier reviews shell commands during planning instead of prompting you. Approved commands run, and rejected ones are blocked. Otherwise, commands outside the [built-in read-only set](/docs/en/permissions#read-only-commands) prompt for approval, including when the sandbox's [auto-allow mode](/docs/en/sandboxing#sandbox-modes) is enabled. In interactive terminal sessions with bypass permissions available, neither the classifier nor a prompt applies to planning commands; [Skip all checks with bypassPermissions mode](#skip-all-checks-with-bypasspermissions-mode) covers the few things that still prompt there. In v2.1.212 through v2.1.217, sessions without bypass permissions prompted for every command outside the read-only set, whether or not auto mode was available.

Enter plan mode by pressing `Shift+Tab` or prefixing a single prompt with `/plan`. You can also start in plan mode from the CLI:

```bash theme={null}
claude --permission-mode plan
```

Press `Shift+Tab` again to leave plan mode without approving a plan.

### Review and approve a plan

When the plan is ready, Claude presents it and asks how to proceed. From that prompt you can choose:

* **Yes, and use auto mode**: approve and start in [auto mode](#eliminate-prompts-with-auto-mode). When auto mode is unavailable, this option reads **Yes, auto-accept edits**. If you started the session with bypass permissions enabled, the option reads **Yes, and switch to BYPASS PERMISSIONS (no further prompts) for this session** instead.
* **Yes, manually approve edits**: approve and review each edit individually.
* **No, keep planning**: stay in plan mode and tell Claude what to change.

Approving a plan exits plan mode and switches the session to the permission mode each approve option describes, so Claude starts editing. To plan again, cycle back to plan mode with `Shift+Tab`, or prefix your next prompt with `/plan`.

Press `Ctrl+G` to open the proposed plan in your default text editor and edit it directly before Claude proceeds. When [`showClearContextOnPlanAccept`](/docs/en/settings-reference#showclearcontextonplanaccept) is enabled, the list gains a first option that approves the plan and clears the planning context.

Accepting a plan also gives the session a [generated title](/docs/en/sessions#name-your-sessions) based on the plan, unless you've already named the session.

### Set plan mode as the default

To make plan mode the default for a project's terminal sessions, set `defaultMode` to `plan` in `.claude/settings.json`, placed as the example under [Start in a different permission mode](#start-in-a-different-mode) shows. Conversations the [VS Code extension](/docs/en/vs-code) starts don't read project settings for the starting permission mode. There, set `claudeCode.initialPermissionMode` to `plan` in your VS Code user settings instead.

<h2 id="eliminate-prompts-with-auto-mode">
  Eliminate permission prompts with auto mode
</h2>

Auto mode lets Claude execute without routine permission prompts. A separate classifier model reviews actions before they run, blocking anything that escalates beyond your request, targets unrecognized infrastructure, or appears driven by hostile content Claude read. Explicit [ask rules](/docs/en/permissions#manage-permissions) still force a prompt.

On Pro, Max, and Team plans, auto mode is the [built-in starting permission mode](#which-mode-a-session-starts-in).

The classifier also reviews each message Claude sends to another agent with [`SendMessage`](/docs/en/tools-reference), whether plain text or a structured [agent team](/docs/en/agent-teams) message, before Claude Code delivers it, both in auto mode and in [plan mode while the classifier reviews commands](#analyze-before-you-edit-with-plan-mode); the send review requires Claude Code v2.1.222 or later.

The classifier also reviews and approves or blocks `rm` and `rmdir` removals targeting a [critical path](#critical-paths), such as `rm -rf /` and `rm -rf ~`, including when the removal sits inside command or process substitution.

Auto mode also nudges Claude to keep working without stopping for clarifying questions, though Claude still asks when your prompt or a skill explicitly relies on it. For stronger autonomous behavior in a mode that still prompts you, set the [Proactive output style](/docs/en/output-styles) instead.

<Warning>
  Auto mode reduces permission prompts but does not guarantee safety. Use it for tasks where you trust the general direction, not as a replacement for review on sensitive operations.
</Warning>

Auto mode is available only when your account meets all of these requirements:

* **Plan**: All plans.
* **Organization**: on Team and Enterprise, auto mode is available by default. Administrators can turn it off for the organization by setting `permissions.disableAutoMode` to `"disable"` in [managed settings](/docs/en/managed-settings).
* **Model**: on the Anthropic API and [Claude Platform on AWS](/docs/en/claude-platform-on-aws), Claude Opus 4.6 or later, Sonnet 4.6 or later, or a [Fable model](/docs/en/model-config#work-with-fable). On Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) sessions, only Claude Sonnet 5, Opus 4.7 or later, and the Fable models. Older models, including Sonnet 4.5, Opus 4.5, Haiku, and claude-3 models, are not supported on any provider.
* **Provider**: available by default on the Anthropic API, Claude Platform on AWS, Amazon Bedrock, Google Cloud's Agent Platform, Microsoft Foundry, and signed-in Claude apps gateway sessions.

If Claude Code reports auto mode as unavailable, first check these requirements and whether any settings file sets [`disableAutoMode`](/docs/en/settings-reference#disableautomode). Anthropic may also have turned auto mode off server-side, or the server may have rejected auto mode for your account. A session that received either answer keeps auto mode off until the session ends, so start a new session later.

A separate message that names a model and says auto mode "cannot determine the safety" of an action means a classifier request failed. That failure is usually transient, but on Amazon Bedrock it can repeat until your account can invoke the named model. See the [error reference](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action) for the causes and what to do.

If you set `defaultMode: "auto"` in [settings](/docs/en/settings-reference#all-settings) and a terminal session starts in Manual mode with no error, the setting is likely in `.claude/settings.json` or `.claude/settings.local.json`. `auto` doesn't take effect from those files. Move it to `~/.claude/settings.json`. For a conversation the VS Code extension started, check the extension's own list in [Switch permission modes](#switch-permission-modes) instead.

<h3 id="enable-auto-mode-on-bedrock-agent-platform-or-foundry">
  Auto mode on Bedrock, Agent Platform, or Foundry
</h3>

On [Amazon Bedrock](/docs/en/amazon-bedrock), [Google Cloud's Agent Platform](/docs/en/google-vertex-ai), [Microsoft Foundry](/docs/en/microsoft-foundry), and signed-in [Claude apps gateway](/docs/en/claude-apps-gateway) sessions, auto mode appears in the `Shift+Tab` cycle by default. Appearing in the cycle doesn't change the permission mode a session starts in: on these providers, terminal sessions start in your [`defaultMode`](/docs/en/settings-reference#permissions-defaultmode), which is Manual unless you change it, and conversations in the [VS Code extension](/docs/en/vs-code) start in Manual unless `claudeCode.initialPermissionMode` or a mode you picked in the extension sets one. Only Claude Sonnet 5, Opus 4.7 or later, and the Fable models are supported on these providers.

To make auto mode the default starting permission mode, set `"permissions": {"defaultMode": "auto"}` in user or managed settings. In sessions the VS Code extension starts, select **Auto** from the mode indicator instead. [Switch permission modes](#switch-permission-modes) covers what outranks that pick.

The [`/doctor`](/docs/en/commands#all-commands) checkup proposes this user-settings default on these providers the same way it does on the Anthropic API.

To prevent developers from using auto mode, set `disableAutoMode` to `"disable"` in [managed settings](/docs/en/managed-settings). This removes `auto` from the `Shift+Tab` cycle, and a session started with `--permission-mode auto` starts in Manual instead. A session already running in auto mode leaves it when the setting reaches that session from an [admin-deployed source](/docs/en/managed-settings#which-managed-source-claude-code-uses), and shows `auto mode disabled by settings`. Before v2.1.251, a running session kept auto mode until it ended.

In v2.1.158 through v2.1.206, auto mode was off on these providers until you set `CLAUDE_CODE_ENABLE_AUTO_MODE=1`, and Claude Code ignored `defaultMode: "auto"` on these providers unless the variable was also set. The variable is still accepted for compatibility and has no effect from v2.1.207 onward.

### Server-side classifier review

On Enterprise plans and accounts that use the Claude API, on [Claude Platform on AWS](/docs/en/claude-platform-on-aws), Amazon Bedrock, Google Cloud's Agent Platform, and Microsoft Foundry, and whenever you point `ANTHROPIC_BASE_URL` at an [LLM gateway or proxy](/docs/en/llm-gateway), Claude Code in auto mode asks the server to review [the actions that go to the classifier](#how-the-classifier-evaluates-actions) as part of the session's model requests. Where the server reviews them, its verdicts decide those actions. Where it doesn't, most often because an LLM gateway or proxy interferes with the traffic, or because the platform, region, or credential doesn't have server-side checks yet, Claude Code falls back to its own classifier requests, and once that fallback holds for the rest of the session it shows a [notice about classifier request charges](/docs/en/auto-mode-classifier-billing) on accounts where those requests are billed. To skip asking the server and always use Claude Code's own classifier requests, set [`CLAUDE_CODE_AUTO_MODE_SERVER=0`](/docs/en/env-vars). The variable isn't read on a direct connection to the Anthropic API. If you set `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` and leave `CLAUDE_CODE_AUTO_MODE_SERVER` unset, Claude Code also stops asking the server.

Asking the server by default requires Claude Code v2.1.278 or later.

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
* Committing or pushing a change that would send secrets or sensitive data outside the repository when it runs, or widen what a deploy exposes. This covers a CI workflow or deploy configuration that passes a secret to a destination that doesn't already receive it, a script or setup step that reads a secret store and sends the data out, and a config change that widens what a deploy publishes, such as a registry, visibility, artifact, or sourcemap setting. The check applies on any branch, applies even when the repository is public, and fires when the change is committed or pushed, whether or not that commit or push triggers the pipeline; clearing it requires naming the execution effect, not only the commit or push. Before v2.1.211, this check was scoped to the default branch instead: a push there was blocked when it carried sensitive content, changes concealed or misdescribed relative to what you asked for, content ported in from outside the repository, or routed around a review you asked for
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

* Writing to Claude Code session transcripts, the `.jsonl` history files under `~/.claude/projects/` or your configured config directory, whether directly or through a shell command. The rule also covers the metadata lines Claude Code appends to each transcript entry for its own checks. Reading a transcript isn't blocked
* A recursive forced delete such as `rm -rf "$VAR"` or `Remove-Item -Recurse -Force $dir` whose target is a shell variable, or a glob rooted at one, that isn't assigned anywhere in the conversation the classifier sees. The value came only from earlier command output, which the classifier never receives, so the classifier can't verify the deletion target against the other deletion rules. The block clears when you name the exact path being deleted, or when Claude re-runs the delete with the resolved literal path written into the command. Deletes whose target the classifier can resolve aren't affected. `Remove-Item` targets that are a bare `*` or end in `/*` or `\*` never reach the classifier: Claude Code [denies them outright](#remove-item-in-powershell)

Claude Code v2.1.257 and later also block these by default:

* Requesting credentials from the cloud instance-metadata endpoint, such as `169.254.169.254`, or explicitly authenticating a cloud, cluster, or registry call with the machine's own service-account or node identity
* Reaching a public host by a route other than a direct request, such as a tunnel, a reverse shell, or a resolver or proxy configuration rewritten to point outside
* Reading credentials that belong to the host rather than to your task, such as node certificates or the node's container-registry auth
* Connecting to or scanning sibling containers, pods, or VMs that Claude didn't start, or the node beneath the container

If Claude Code runs somewhere that is meant to allow one of these, describe that setup in a [Host containment entry](/docs/en/auto-mode-config#define-trusted-infrastructure) in `autoMode.environment`.

Claude Code v2.1.261 and later also block these by default:

* Posting or writing a link to a public paste, diagram, or data-sharing service in a message, PR or issue text, a document, or anywhere else the link will be opened or fetched, when the URL itself carries the content being shared, unless you named that service

**Allowed by default**:

* Local file operations in your working directory
* Installing dependencies declared in your lock files or manifests
* Reading `.env` and sending credentials to their matching API
* Read-only HTTP requests
* Pushing to any branch of the repository you're working in, including the default branch. A non-default branch whose name marks it as a deploy or publication target, such as `production` or `gh-pages`, isn't covered: the classifier judges a push there on its own terms. The push's content is still checked against the other rules, [`permissions.deny` rules](/docs/en/permissions#manage-permissions) can still block push commands [as written](/docs/en/permissions#bash-rule-limits) in every mode, and the remote's own branch protection still applies. Before v2.1.211, only pushes to the branch you started on, branches Claude created, and routine pushes to the default branch were allowed by default, and before v2.1.203 any direct push to the default branch was blocked

Claude Code v2.1.195 and later also allow these by default:

* Deleting the exact jobs Claude created earlier in the same session
* Reading, reviewing, or writing security-related code, configs, and threat models as part of your task
* Messages between agents working together in the same multi-agent session
* Sending data to the trusted domains, buckets, and services you list in [`environment`](/docs/en/auto-mode-config#define-trusted-infrastructure). This covers data flow only, not destructive or credential operations on the same infrastructure
* [Claude in Chrome](/docs/en/chrome) navigation to a trusted internal domain, localhost, or a URL you named

Sandboxed commands don't get network access by default. Claude names the hosts a command needs on the command itself, the classifier reviews them with the command, and an approved list opens those hosts for that one command alone. [Per-command allowed domains](/docs/en/sandboxing#per-command-allowed-domains-in-auto-mode) covers what a list can and can't open and what happens when a command reaches for an unlisted host.

Run `claude auto-mode defaults` to print the full rule lists as JSON. If routine actions get blocked, an administrator can add trusted repos, buckets, and services via the `autoMode.environment` setting: see [Configure auto mode](/docs/en/auto-mode-config).

Pushing to any branch of the repository you're working in and creating a pull request that matches your request run without a prompt, unless the push or pull request falls under the [blocked list](#what-the-classifier-blocks-by-default), such as secrets or sensitive data leaving the repository, or a pull request that targets a different repository or organization. To require a human checkpoint before these commands while staying in auto mode, add `permissions.ask` rules, which match the command [as written](/docs/en/permissions#bash-rule-limits): see [Common boundaries](/docs/en/auto-mode-config#common-boundaries).

<h3 id="first-read-outside-the-working-directories">
  The first read outside the working directories
</h3>

While [`permissions.blockReadsOutsideWorkingDirectories`](/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories) is off, file reads run without a prompt in auto mode, including reads outside the [working directories](/docs/en/permissions#working-directories). The first time Claude uses the Read, Grep, or Glob tool on a path outside them, Claude Code asks you whether to keep allowing those reads.

The prompt doesn't appear in non-interactive `-p` runs or background sessions; reads there run as before.

Whatever you answer, Claude keeps working:

* **Keep allowing**: the read runs, later reads outside the working directories run as before, and Claude Code records your answer so the prompt doesn't appear again
* **Block from now on**: the read is refused, and Claude Code sets [`permissions.blockReadsOutsideWorkingDirectories`](/docs/en/settings-reference#permissions-blockreadsoutsideworkingdirectories) to `true` in your user settings, which makes the file tools refuse such reads in every later session and every permission mode. To let Claude read such a path later, add its directory with `/add-dir` or remove the setting.
* **Ask again next time**: the read is refused, and the next read outside the working directories prompts again

### Boundaries you state in conversation

The classifier treats boundaries you state in the conversation as a block signal. If you tell Claude "don't push" or "wait until I review before deploying", the classifier blocks matching actions even when the default rules would allow them. A boundary stays in force until you lift it in a later message. Claude's own judgment that a condition was met does not lift it.

Boundaries are not stored as rules. The classifier re-reads them from the transcript on each check, so a boundary can be lost if [context compaction](/docs/en/costs#reduce-token-usage) removes the message that stated it. For a hard guarantee, add a [deny rule](/docs/en/permissions#permission-rule-syntax) instead.

### Approvals you state in conversation

If you tell Claude that a blocked action is allowed, the classifier reads that as your approval and can clear the block. How you worded it decides whether the action runs, and how far the approval reaches:

* **Name the action and its specifics**: your message has to name the action and the specific thing that makes it dangerous, such as the branch of a force push. Naming the verb alone clears nothing, so "you can force-push" leaves the block in place.
* **Expect it to cover one action**: an approval covers the destructive action you named, so a later action is blocked again unless you granted the approval as standing. To stop approving a routine pattern one action at a time, add it to [`autoMode.allow`](/docs/en/auto-mode-config#override-the-block-and-allow-rules).
* **Some blocks stay in place**: [the classifier's precedence order](/docs/en/auto-mode-config#override-the-block-and-allow-rules) sets out which blocks your approval can reach. To run a step it won't clear, [leave auto mode](#switch-permission-modes) and answer the permission prompt.

### When auto mode falls back

When auto mode can't approve your session's actions, what happens depends on the case:

* **A blocked action**: Claude Code shows a notification and lists the action in `/permissions` under the **Recently denied** tab, where you can press `r` to retry it with a manual approval. When the classifier produces [no verdict on the action](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action), because a safety check separate from auto mode refused the classifier's own request or its response didn't parse, Claude Code denies the action without the notification or the **Recently denied** entry.
* **Repeated blocks**: if the classifier blocks an action 3 times in a row or 20 times total, auto mode pauses and Claude Code resumes prompting. Approving the prompted action resumes auto mode. These thresholds are not configurable. Any allowed action resets the consecutive counter, while the total counter persists for the session and resets only when its own limit triggers a fallback. Claude Code doesn't count a denial toward either threshold when [a safety check separate from auto mode refuses the classifier's own request](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action); the linked entry covers how Claude Code handles those denials.
* **Sessions that can't prompt**: a [non-interactive](/docs/en/headless) `-p` run without a [`--permission-prompt-tool`](/docs/en/cli-reference#cli-flags) has no prompt to fall back to. When repeated blocks reach a threshold, the action doesn't run and Claude keeps working. The same applies when [a safety check separate from auto mode refuses the classifier's request](/docs/en/errors#auto-mode-cannot-determine-the-safety-of-an-action). Claude Code doesn't stop the run in either case.
* **A mode switch during a check**: if you switch permission modes while a classifier check is pending, Claude Code discards a verdict the new mode wouldn't have requested rather than applying it: you're prompted for approval instead, or the action is auto-denied in [`dontAsk` mode](#allow-only-pre-approved-tools-with-dontask-mode).

Repeated blocks usually mean the classifier is missing context about your infrastructure. Use `/feedback` to report false positives, or have an administrator [configure trusted infrastructure](/docs/en/auto-mode-config).

<span id="how-the-classifier-evaluates-actions" />

<AccordionGroup>
  <Accordion title="How the classifier evaluates actions">
    Each action goes through a fixed decision order. The first matching step wins:

    1. Actions matching your [allow, ask, or deny rules](/docs/en/permissions#manage-permissions) resolve immediately, with these exceptions:
       * Writes to [protected paths](#protected-paths) route to the classifier even when an allow rule matches, and so do `rm` and `rmdir` removals targeting a [critical path](#critical-paths) in Claude Code v2.1.218 and later
       * MCP tools marked [`requiresUserInteraction`](/docs/en/mcp#require-approval-for-a-specific-tool) prompt you directly even when an allow rule matches, and so do connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools) in sessions where that setting reaches Claude Code
       * A shell command that carries [per-command allowed domains](/docs/en/sandboxing#per-command-allowed-domains-in-auto-mode) also routes to the classifier even when an allow rule matches, because a rule approves the command, not its hosts
       * Ask rules that match on a command's content, such as `Bash(git push *)`, fall back to a permission prompt
    2. Read-only actions and file edits in your working directory are auto-approved, except writes to [protected paths](#protected-paths) and [the first read outside the working directories](#first-read-outside-the-working-directories), which prompts you
    3. Everything else goes to the classifier. The connector tools and `requiresUserInteraction` MCP tools that prompt you directly in step 1 never reach the classifier, so neither an org-required approval nor a consent step is auto-approved
    4. If the classifier blocks, Claude receives the reason and tries an alternative. In most sessions the reason names the rule the classifier matched, such as `[Data Exfiltration]`, rather than giving a written explanation; see [Review denials](/docs/en/auto-mode-config#review-denials)

    On entering auto mode, broad allow rules that grant arbitrary code execution are dropped:

    * Blanket `Bash(*)` or `PowerShell(*)`
    * Wildcarded interpreters like `Bash(python*)`
    * Package-manager run commands
    * `Agent` allow rules
    * [`Monitor`](/docs/en/tools-reference#monitor-tool) allow rules, because Claude Code runs Monitor commands through the shell

    Narrow rules like `Bash(npm test)` stay in effect. Claude Code restores the dropped rules when you leave auto mode. Before v2.1.236, Claude Code left `Monitor` allow rules in effect in auto mode, so a rule that matched the whole tool approved Monitor commands without classifier review.

    Claude Code also runs `git status` itself before a command that would discard uncommitted work, such as `git reset --hard` or `rm -rf`, and shows the classifier whether staged, modified, or untracked work is present. Claude Code reports untracked files in that check even when the repository's git configuration sets `status.showUntrackedFiles=no`.

    In the classifier requests sent by Claude Code itself, the classifier sees user messages, tool calls other than read-only lookups such as file reads and searches, and your CLAUDE.md content. Tool results are stripped from those requests, so hostile content in a file or web page can't manipulate the classifier directly.

    You can annotate a call's result with a [PostToolUse hook's `classifierContext` field](/docs/en/hooks#annotate-a-result-for-the-auto-mode-classifier), which the classifier reads as application-provided context. The field requires Claude Code v2.1.236 or later.

    A separate server-side probe scans incoming tool results and flags suspicious content before Claude reads it. For more on how these layers work together, see the [auto mode announcement](https://claude.com/blog/auto-mode) and the [engineering deep dive](https://www.anthropic.com/engineering/claude-code-auto-mode).
  </Accordion>

  <Accordion title="How auto mode handles subagents">
    The classifier checks [subagent](/docs/en/sub-agents) work at three points:

    1. Before a subagent starts, the delegated task description is evaluated, so a dangerous-looking task is blocked at spawn time.
    2. While the subagent runs, each of its actions goes through the classifier with the same rules as the parent session, and any `permissionMode` in the subagent's frontmatter is ignored.
    3. When the subagent finishes, the classifier reviews its work and its final report before the parent reads the report. When the classifier flags the subagent's work or report, or a separate API safety check refuses the review, the report is still delivered, prepended with a security warning. When the classifier is unavailable for the review, the report arrives with a note to verify the subagent's work before acting on it.
  </Accordion>

  <Accordion title="Cost and latency">
    The classifier runs on Claude Sonnet 5 by default rather than on your `/model` selection. A classifier model that Anthropic configures server-side takes precedence over that default. When your session's model is Claude Sonnet 4.6, or when [`availableModels`](/docs/en/model-config#restrict-model-selection) excludes Sonnet 5, the classifier runs on the session's model instead, or on an Opus model when the session runs on a [Fable model](/docs/en/model-config#work-with-fable); on providers other than the Anthropic API, that Opus fallback is the provider's default Opus model.

    The session's first auto-mode request validates the Sonnet 5 default: if the request succeeds, Sonnet 5 stays the session's classifier model, and if it fails because the model isn't available, the session uses the fallback instead. After that validation settles, the classifier's model doesn't change for the session.

    On Enterprise plans and on accounts that use the Claude API, [Claude Platform on AWS](/docs/en/claude-platform-on-aws), Amazon Bedrock, Google Cloud's Agent Platform, or Microsoft Foundry, classifier calls count toward your token usage. Each check sends a portion of the transcript plus the pending action, adding a round-trip before execution. Reads and working-directory edits outside protected paths skip the classifier, so the overhead comes mainly from shell commands and network operations. Where the server reviews the actions as part of the session's model requests, there are no separate classifier calls to count; see [Server-side classifier review](#server-side-classifier-review).

    Sandboxed network access adds no per-connection classifier requests. The classifier judges [the hosts a command names](/docs/en/sandboxing#per-command-allowed-domains-in-auto-mode) together with the command in one review, and Claude Code checks each connection against the approved list without calling the classifier again.
  </Accordion>
</AccordionGroup>

## Allow only pre-approved tools with dontAsk mode

If you set `dontAsk` mode, Claude Code auto-denies every tool call that would otherwise prompt you. Claude still runs actions that need no approval in Manual mode, such as file reads inside your working directories and [read-only Bash commands](/docs/en/permissions#read-only-commands), plus actions matching your `permissions.allow` rules and calls approved by a [PreToolUse hook](/docs/en/permissions#extend-permissions-with-hooks). Use this mode for CI pipelines or restricted environments where you pre-define what Claude may do; the session never waits for input. The status bar shows `⏵⏵ don't ask on` while this mode is active.

Claude Code denies calls matching your explicit [`ask` rules](/docs/en/permissions#manage-permissions) rather than prompting. It also denies the built-in `AskUserQuestion` tool even if your allow rules match it, and does the same to connector tools [your organization set to `ask`](/docs/en/mcp#organization-controls-on-connector-tools) in sessions where that setting reaches Claude Code. It denies MCP tools marked [`_meta["anthropic/requiresUserInteraction"]`](/docs/en/mcp#require-approval-for-a-specific-tool) the same way, because their approval card needs an answer this mode never collects; this requires Claude Code v2.1.199 or later.

`rm` and `rmdir` removals targeting a [critical path](#critical-paths), such as `rm -rf /` and `rm -rf ~`, are denied even when an allow rule matches them or a `PreToolUse` hook allows them.

[Cloud sessions](/docs/en/claude-code-on-the-web) ignore `defaultMode: "dontAsk"`; see [bypassPermissions](#skip-all-checks-with-bypasspermissions-mode) for details.

Set it at startup with the flag:

```bash theme={null}
claude --permission-mode dontAsk
```

## Skip all checks with bypassPermissions mode

`bypassPermissions` mode disables permission prompts and safety checks so tool calls execute immediately, including writes to [protected paths](#protected-paths).

The [actions no mode auto-approves](#actions-no-mode-auto-approves) still prompt in this mode.

Two [cross-session messaging](/docs/en/cross-session-messaging) safeguards still apply in this mode, and in interactive terminal plan-mode sessions where bypass permissions are available:

* The [`isolatePeerMachines`](/docs/en/settings-reference#isolatepeermachines) approval prompt for messages to your sessions beyond this machine still appears.
* When no [`crossSessionInbound`](/docs/en/cross-session-messaging#control-inbound-messages) value applies, Claude Code holds an inbound message from another of your sessions for your approval, and delivers without asking only when the sending session identifies itself as also bypassing permission prompts. If you leave the permission mode while messages are held, Claude Code re-applies the inbound rules and delivers any held message they now accept.

In interactive terminal sessions with bypass permissions available, Claude Code also doesn't enforce [plan mode's](#analyze-before-you-edit-with-plan-mode) blocks. Claude is still instructed to plan without editing, but a file edit or shell command it attempts during planning runs without prompting. Explicit [ask rules](/docs/en/permissions#manage-permissions) and `rm` and `rmdir` removals targeting a [critical path](#critical-paths) still prompt.

Plan mode keeps its blocks wherever Claude Code runs without an interactive terminal, including [non-interactive runs](/docs/en/headless) with `-p`, [Agent SDK](/docs/en/agent-sdk/permissions#plan-mode-plan) sessions, and conversations in the [VS Code extension](/docs/en/vs-code)'s chat panel. There, `--allow-dangerously-skip-permissions` makes `bypassPermissions` selectable later.

<Warning>
  Only use this mode in isolated environments like containers, VMs, or dev containers without internet access, where Claude Code cannot damage your host system.
</Warning>

You can't enter `bypassPermissions` from a session you started without it enabled. Enable it at launch with [`permissions.defaultMode: "bypassPermissions"`](/docs/en/settings-reference#permissions-defaultmode) or with an enabling flag:

```bash theme={null}
claude --permission-mode bypassPermissions
```

The `--dangerously-skip-permissions` flag is equivalent.

Claude Code refuses `bypassPermissions` in a session you start with [`--restricted`](/docs/en/cli-reference#cli-flags). `--restricted` requires Claude Code v2.1.248 or later.

The first time you start an interactive session with this mode enabled, Claude Code shows a warning dialog asking you to accept responsibility for actions taken without permission checks. Claude Code saves your acceptance to user settings, so the dialog appears only once. If you decline, Claude Code exits. In [non-interactive mode](/docs/en/headless) no dialog is shown, and a [background session](/docs/en/agent-view) started with `--bg` is refused until you've accepted the dialog in an interactive session.

On Linux and macOS, Claude Code refuses to start in this mode when running as root or under `sudo`:

```text theme={null}
--dangerously-skip-permissions cannot be used with root/sudo privileges for security reasons
```

The check is skipped automatically inside a recognized sandbox. To run autonomously in a container, use the [dev container](/docs/en/devcontainer) configuration, which runs Claude Code as a non-root user.

[Cloud sessions](/docs/en/claude-code-on-the-web) don't honor `defaultMode: "bypassPermissions"` or `"dontAsk"` from your settings files, so a repository's checked-in settings can't start a cloud session in bypass-permissions mode. The setting is ignored silently and the session starts in the permission mode shown in the mode dropdown instead. See [Switch permission modes](#switch-permission-modes) for which modes cloud sessions offer.

<Warning>
  `bypassPermissions` offers no protection against prompt injection or unintended actions. For background safety checks with far fewer permission prompts, use [auto mode](#eliminate-prompts-with-auto-mode) instead. Administrators can block this mode by setting `permissions.disableBypassPermissionsMode` to `"disable"` in [managed settings](/docs/en/managed-settings).
</Warning>

## Protected paths

Writes to a small set of paths are never auto-approved, except in `bypassPermissions` mode and in interactive terminal sessions in plan mode with [bypass permissions](#skip-all-checks-with-bypasspermissions-mode) available. This prevents accidental corruption of repository state and Claude's own configuration.

| Mode                     | Protected-path writes                                                                                                                                                                                                                                                        |
| :----------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`, `acceptEdits` | Prompted                                                                                                                                                                                                                                                                     |
| `plan`                   | Allowed in interactive terminal sessions with [bypass permissions](#skip-all-checks-with-bypasspermissions-mode) available. Otherwise, routed to the classifier when [auto mode](#eliminate-prompts-with-auto-mode) is available during planning, and prompted when it isn't |
| `auto`                   | Routed to the classifier                                                                                                                                                                                                                                                     |
| `dontAsk`                | Denied                                                                                                                                                                                                                                                                       |
| `bypassPermissions`      | Allowed                                                                                                                                                                                                                                                                      |

In a session started with [`--restricted`](/docs/en/cli-reference#cli-flags), which requires Claude Code v2.1.248 or later, the classifier can't approve protected-path writes.

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

## Critical paths

Claude Code never lets a [`permissions.allow`](/docs/en/permissions#manage-permissions) rule or a [`PreToolUse` hook](/docs/en/permissions#extend-permissions-with-hooks) that returns `"allow"` approve an `rm` or `rmdir` command that targets a critical path, even in modes that skip other prompts. This circuit breaker guards against model error. A matching deny rule still blocks the command outright.

What happens instead depends on your permission mode:

| Mode                     | What Claude Code does with a critical-path removal                                                                                                                                  |
| :----------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`, `acceptEdits` | Asks you to approve it                                                                                                                                                              |
| `plan`                   | Asks you to approve it. With [auto mode available during planning](#analyze-before-you-edit-with-plan-mode) and no bypass permissions available, sends it to the classifier instead |
| `auto`                   | Sends it to the [classifier](#eliminate-prompts-with-auto-mode)                                                                                                                     |
| `dontAsk`                | Denies it                                                                                                                                                                           |
| `bypassPermissions`      | Asks you to approve it                                                                                                                                                              |

If an explicit [ask rule](/docs/en/permissions#manage-permissions) matches the command, Claude Code asks you even in `auto` mode. In modes that ask, a [`PermissionRequest` hook](/docs/en/hooks#permissionrequest) can answer the prompt the way it answers any other.

Claude Code treats an `rm` or `rmdir` target as a critical path when it is any of the following:

* The filesystem root
* Top-level directories, meaning any direct child of the root, such as `/usr`, `/etc`, or `/data`
* Your home directory
* Windows drive roots and their top-level directories, such as `C:\` and `C:\Windows`
* Your working directory and its parents
* Your additional working directories and their parents, but only when the removal is a glob under one of them, such as `rm -rf <dir>/*`. `rm -rf <dir>` on the directory itself doesn't trigger this check

Claude Code also treats a glob or trailing slash directly under a shell variable, such as `rm -rf "$DIR"/*`, as a critical-path removal, because the command becomes a removal from the filesystem root when the variable is empty.

The prompt for this variable case names the flagged `rm` and says how to rewrite it so the check passes:

* For a variable such as `$DIR`, guard each expansion so the shell stops with an error when the variable is unset or empty, as in `rm -rf "${DIR:?}"/*`, or use a literal path
* For a variable that is normally set, such as `$HOME`, use a literal path

A removal whose expansions are all guarded that way isn't a critical-path removal, so in `bypassPermissions` mode it runs without a prompt.

Hiding the removal inside a subshell with `(...)`, a brace group with `{ ...; }`, command substitution with `$(...)` or backticks, or process substitution with `<(...)`, doesn't skip the check. Claude Code finds a critical-path removal whether it sits inside the nested form, as in `(rm -rf ~)` or `echo "$(rm -rf ~)"`, or elsewhere in the same command.

### Remove-Item in PowerShell

When you enable the [PowerShell tool](/docs/en/tools-reference#powershell-tool), Claude Code gives `Remove-Item` its own check, separate from the `rm` critical-path list. The outcome depends on the target, and the first matching case applies:

* **System paths**: the filesystem root and its top-level directories, drive roots and their top-level directories, and your home directory. Claude Code denies the command in every mode, without asking you.
* **Wildcards**: a bare `*`, or any target ending in `/*` or `\*`, including a glob under a shell variable such as `$dir/*`. Claude Code denies the command in every mode, without asking you, before the [classifier](#eliminate-prompts-with-auto-mode) sees it.
* **Your working directory or one of its parents, with `-Recurse`**: Claude Code treats the command like any other that needs approval in your permission mode, so it asks you in modes that ask, sends it to the classifier in `auto` mode, and denies it in `dontAsk` mode. `bypassPermissions` mode skips this check.

## See also

* [Permissions](/docs/en/permissions): allow, ask, and deny rules; managed policies
* [Configure auto mode](/docs/en/auto-mode-config): tell the classifier which infrastructure your organization trusts
* [Hooks](/docs/en/hooks): custom permission logic via `PreToolUse` and `PermissionRequest` hooks
* [Security](/docs/en/security): safeguards and best practices
* [Sandboxing](/docs/en/sandboxing): filesystem and network isolation for Bash commands
* [Non-interactive mode](/docs/en/headless): run Claude Code with the `-p` flag
